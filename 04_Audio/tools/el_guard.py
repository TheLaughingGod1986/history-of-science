#!/usr/bin/env python3
"""Guard rails for every ElevenLabs credit spend (Ben, 4–5 Oct 2026).

`el_client.request` calls `before_spend` / `after_spend` around any POST that
spends credit (text-to-speech, sound effects, music). Generators need no change.

- **One recorder at a time.** The first spend in a process takes a lock file
  (`<locks>/elevenlabs.lock`) and keeps it until the process exits. A second
  process is refused while the first is alive. A lock left by a dead process on
  the same machine is taken over.
- **Pause file.** If `<desk>/elevenlabs/TTS_PAUSE` exists, nothing is spent.
- **Credit floor.** A spend that would leave fewer than `EL_CREDIT_FLOOR`
  characters (default 0: no floor, Ben 9 Oct 2026, "keep going until the credit
  runs out") is refused, so a request never asks for more than is left.
- **Ledger.** Every spend is appended to `<desk>/elevenlabs/ledger.jsonl`:
  time, pid, script, endpoint, characters, HTTP status, credits before.

`<desk>` is `$HOS_DESK_DIR` or `~/_desk`; `<locks>` is `<desk>/locks`.
Set `EL_GUARD_OFF=1` only for a test with no network.
"""
from __future__ import annotations

import atexit
import datetime as dt
import json
import os
import socket
import sys
from pathlib import Path
from typing import Any, Callable

SPEND_PREFIXES = (
    "/v1/text-to-speech",
    "/v1/sound-generation",
    "/v1/music",
    "/v1/speech-to-speech",
    "/v1/speech-to-text",  # Scribe bills the same pool
)
DEFAULT_FLOOR = 0  # Ben, 9 Oct 2026: no floor; spend until the credit runs out


class SpendRefused(RuntimeError):
    """Raised instead of spending ElevenLabs credit."""


def desk_dir() -> Path:
    return Path(os.environ.get("HOS_DESK_DIR", Path.home() / "_desk"))


def lock_path() -> Path:
    return desk_dir() / "locks" / "elevenlabs.lock"


def ledger_path() -> Path:
    return desk_dir() / "elevenlabs" / "ledger.jsonl"


def pause_path() -> Path:
    return desk_dir() / "elevenlabs" / "TTS_PAUSE"


def floor() -> int:
    return int(os.environ.get("EL_CREDIT_FLOOR", DEFAULT_FLOOR))


def is_spend(method: str, path: str) -> bool:
    return method.upper() == "POST" and path.startswith(SPEND_PREFIXES)


def _pid_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


_held = False


def acquire_lock() -> None:
    """Take the one-recorder lock for this process (idempotent)."""
    global _held
    if _held:
        return
    path = lock_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    me = {
        "pid": os.getpid(),
        "host": socket.gethostname(),
        "script": Path(sys.argv[0]).name if sys.argv and sys.argv[0] else "?",
        "started": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
    }
    for _ in range(2):
        try:
            fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
        except FileExistsError:
            try:
                holder = json.loads(path.read_text() or "{}")
            except (OSError, json.JSONDecodeError):
                holder = {}
            same_host = holder.get("host") == me["host"]
            pid = int(holder.get("pid", 0) or 0)
            if same_host and pid and not _pid_alive(pid):
                path.unlink(missing_ok=True)  # stale lock from a dead process
                continue
            raise SpendRefused(
                "Another ElevenLabs recorder holds the lock "
                f"({holder.get('script', '?')} pid {holder.get('pid', '?')} on {holder.get('host', '?')}, "
                f"since {holder.get('started', '?')}). One recorder at a time: wait for it, "
                f"or remove {path} only if that process is gone."
            )
        with os.fdopen(fd, "w") as fh:
            json.dump(me, fh)
        _held = True
        atexit.register(release_lock)
        return
    raise SpendRefused(f"Could not take the ElevenLabs lock at {path}")


def release_lock() -> None:
    global _held
    if not _held:
        return
    path = lock_path()
    try:
        holder = json.loads(path.read_text() or "{}")
        if int(holder.get("pid", 0)) == os.getpid():
            path.unlink(missing_ok=True)
    except (OSError, json.JSONDecodeError, ValueError):
        pass
    _held = False


def characters_in(data: dict[str, Any] | None) -> int:
    if not data:
        return 0
    text = data.get("text") or data.get("prompt") or ""
    return len(text) if isinstance(text, str) else 0


def remaining_credits(fetch: Callable[[], tuple[int, bytes]]) -> int | None:
    """Characters left on the plan, from GET /v1/user/subscription."""
    status, body = fetch()
    if status != 200:
        return None
    sub = json.loads(body)
    return int(sub["character_limit"]) - int(sub["character_count"])


_last: dict[str, Any] = {}


def before_spend(
    path: str,
    data: dict[str, Any] | None,
    fetch_subscription: Callable[[], tuple[int, bytes]],
) -> None:
    """Refuse the spend, or record what we need to log it afterwards."""
    if os.environ.get("EL_GUARD_OFF") == "1":
        return
    if pause_path().exists():
        raise SpendRefused(f"ElevenLabs spending is paused ({pause_path()} exists).")
    acquire_lock()
    chars = characters_in(data)
    left = remaining_credits(fetch_subscription)
    if left is None:
        raise SpendRefused("Couldn't read the ElevenLabs balance, so nothing was spent.")
    if left - chars < floor():
        raise SpendRefused(
            f"ElevenLabs floor: {left:,} left, this request needs about {chars:,}, "
            f"floor is {floor():,}. Stop and post on the desk."
        )
    _last.update({"path": path, "chars": chars, "left_before": left})


def after_spend(status: int) -> None:
    if os.environ.get("EL_GUARD_OFF") == "1" or not _last:
        return
    entry = {
        "time": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "pid": os.getpid(),
        "host": socket.gethostname(),
        "script": Path(sys.argv[0]).name if sys.argv and sys.argv[0] else "?",
        "endpoint": _last["path"].split("?")[0],
        "chars": _last["chars"],
        "status": status,
        "left_before": _last["left_before"],
    }
    ledger = ledger_path()
    ledger.parent.mkdir(parents=True, exist_ok=True)
    with ledger.open("a") as fh:
        fh.write(json.dumps(entry) + "\n")
    _last.clear()
