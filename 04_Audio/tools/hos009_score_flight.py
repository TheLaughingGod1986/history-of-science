#!/usr/bin/env python3
"""Disabled HOS 009 music flight. Preparation only. It does not open an allowance.

The production entry points below do not accept a transport, a fetch callable,
or a desk path. The socket, when a later Chief decision turns it on, is one
HTTP response: status, Date, raw bytes. Until that decision the activation
constant stays false, so the socket function returns before any network call.

The billing guard is the reviewed J3147 file, loaded by hash. This module does
not re-implement findings A–D, does not consult the pause bypass switch, does
not delete the single-use file, and does not retry.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import socket
import sys
from datetime import datetime, timezone
from pathlib import Path

# Fail closed. Not an environment switch. A later Chief job would change this
# only after the missing price evidence in jobs/reviews/J3150/PRICING_EVIDENCE.md
# is replaced by a proven bound. This preparation does not do that.
ACTIVATION_AUTHORIZED = False

GUARD_SHA256 = "930d987783055d1f73e80fd9ae770f1ecde63d79b397706df74e9492b4029308"
SHAPE_SHA256 = "ba290b64740c96c3407af17da80d043be3bf840d1863518bfb011e047f9e647e"
QUERY = "output_format=mp3_44100_128"
MUSIC_URL = "https://api.elevenlabs.io/v1/music?" + QUERY
SUBSCRIPTION_URL = "https://api.elevenlabs.io/v1/user/subscription"
_BANNED = frozenset(
    {
        "transport",
        "fetch",
        "get_subscription",
        "post_music",
        "store_path",
        "lock_path",
        "pause_path",
        "ledger_path",
        "desk",
        "root",
        "path",
        "headers",
        "date_header",
        "raw",
        "http_status",
        "token",
        "mode",
        "estimated_credits",
        "cash_gbp",
        "attempt",
        "bind_desk",
    }
)

_PINNED = Path(__file__).resolve().parents[2] / "jobs" / "reviews" / "J3150" / "pinned"


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_guard():
    guard_path = _PINNED / "score_billing_guard.py"
    shape_path = _PINNED / "subscription_shape.json"
    if _sha(guard_path) != GUARD_SHA256 or _sha(shape_path) != SHAPE_SHA256:
        raise RuntimeError("pinned HOS 009 guard hash does not match the J3147 review")
    spec = importlib.util.spec_from_file_location("hos009_pinned_guard_j3150", guard_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("pinned HOS 009 guard could not be loaded")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


guard = _load_guard()


def _reject_kwargs(forbidden: dict) -> None:
    if forbidden:
        raise guard.GuardRefused("caller_supplied_transport")


def _same_hold(fd: int, ino: int, started: str) -> None:
    if guard._held_fd != fd or guard._held_ino != ino or guard._held_started != started:
        raise guard.GuardRefused("shared_meter")
    try:
        current = os.fstat(fd).st_ino
    except OSError:
        raise guard.GuardRefused("shared_meter") from None
    if current != ino:
        raise guard.GuardRefused("shared_meter")


def _refuse_used_store() -> None:
    """A burned single-use file stops a second flight before another GET.

    This does not delete or rewrite the file. Clearing it is a Chief ruling.
    """
    store = guard._paths()["store"]
    if store.is_symlink():
        raise guard.GuardRefused("retry_or_shared_meter")
    if not store.exists():
        return
    try:
        raw = store.read_bytes()
    except OSError:
        raise guard.GuardRefused("retry_or_shared_meter") from None
    if raw.strip() == b"":
        return
    try:
        state = json.loads(raw.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError):
        raise guard.GuardRefused("retry_or_shared_meter") from None
    reqs = state.get("used_requests") if type(state) is dict else None
    bodies = state.get("used_bodies") if type(state) is dict else None
    if type(reqs) is not list or type(bodies) is not list or reqs or bodies:
        raise guard.GuardRefused("retry_or_shared_meter")


def _approved_request() -> dict:
    """Budget, cash, attempt and endpoint are fixed here. Callers cannot set them."""
    return {
        "holder": "hos009-score",
        "attempt": 1,
        "endpoint": "/v1/music",
        "model_id": "music_v2",
        "force_instrumental": True,
        "music_length_ms": 180_000,
        "query": QUERY,
        "estimated_credits": guard.MIN_ESTIMATED_CREDITS,
        "cash_gbp": "0",
    }


def _subscription_get():
    """The only subscription read. Called by read_subscription, not by a caller."""
    status, date, raw = _read_one_response("GET", None)
    return status, {"Date": date}, raw


def _post_bytes(prompt: str) -> bytes:
    payload = {
        "prompt": prompt,
        "music_length_ms": 180_000,
        "model_id": "music_v2",
        "force_instrumental": True,
    }
    return json.dumps(payload, separators=(",", ":")).encode("utf-8")


def _append_ledger(status: int) -> None:
    """Record the one POST. Does not waive a pause, a pending line, or a non-200."""
    if type(status) is not int:
        raise guard.GuardRefused("http_status")
    ledger = guard._paths()["ledger"]
    if ledger.is_symlink() or not ledger.is_file():
        raise guard.GuardRefused("pending_spend")
    entry = {
        "time": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "pid": os.getpid(),
        "host": socket.gethostname(),
        "script": "hos009-score-flight",
        "endpoint": "/v1/music",
        "status": status,
    }
    with ledger.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, separators=(",", ":")) + "\n")


def _read_one_response(method: str, body: bytes | None) -> tuple[int, str, bytes]:
    """One response object. No caller path and no second try.

    Activation false returns before the socket. The socket branch reads one
    status, one Date header and one body.
    """
    if method not in ("GET", "POST"):
        raise guard.GuardRefused("endpoint")
    if method == "GET" and body is not None:
        raise guard.GuardRefused("endpoint")
    if method == "POST" and type(body) is not bytes:
        raise guard.GuardRefused("malformed_request")
    if ACTIVATION_AUTHORIZED is not True:
        raise guard.GuardRefused("activation_closed")
    return _socket_once(method, body)


def _socket_once(method: str, body: bytes | None) -> tuple[int, str, bytes]:
    import urllib.error
    import urllib.request

    from el_auth import auth_headers, load_token

    token, mode = load_token()
    if method == "GET":
        url = SUBSCRIPTION_URL
        payload = None
        accept = "application/json"
    else:
        url = MUSIC_URL
        payload = body
        accept = "audio/mpeg"
    headers = auth_headers(token, mode, accept=accept)
    if payload is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=payload, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            date = response.headers.get("Date")
            raw = response.read()
            status = response.status
    except urllib.error.HTTPError as error:
        date = error.headers.get("Date") if error.headers is not None else None
        raw = error.read()
        status = error.code
    if type(status) is not int or type(raw) is not bytes or type(date) is not str or date.strip() == "":
        raise guard.GuardRefused("untrusted_receipt")
    return status, date, raw


def _flight(*, prompt: str, length_ms: int) -> tuple[int, bytes, dict[str, str]]:
    if type(prompt) is not str or prompt.strip() == "" or len(prompt) > 4000:
        raise guard.GuardRefused("malformed_request")
    if type(length_ms) is not int or length_ms != 180_000:
        raise guard.GuardRefused("duration")
    if guard._desk is None:
        raise guard.GuardRefused("unbound_desk")
    _refuse_used_store()
    guard.hold_recorder()
    fd = guard._held_fd
    ino = guard._held_ino
    started = guard._held_started
    if type(fd) is not int or type(ino) is not int or type(started) is not str:
        raise guard.GuardRefused("shared_meter")
    _same_hold(fd, ino, started)
    board = guard.MeterBoard()
    receipt = guard.read_subscription(_subscription_get)
    _same_hold(fd, ino, started)
    token = board.decide(receipt, request=_approved_request())
    _same_hold(fd, ino, started)
    spent = board.consume(token, body_sha256=token["body_sha256"])
    _same_hold(fd, ino, started)
    if (
        spent.get("consumed") is not True
        or spent.get("authorizes_generation") is not False
        or spent.get("opens_allowance") is not False
        or spent.get("integrated") is not False
    ):
        raise guard.GuardRefused("scope")
    status, date, raw = _read_one_response("POST", _post_bytes(prompt))
    _same_hold(fd, ino, started)
    if not guard.recorder_held():
        raise guard.GuardRefused("shared_meter")
    _append_ledger(status)
    return status, raw, {"date": date}


def from_generator(*, prompt: str, length_ms: int, **forbidden: object) -> tuple[int, bytes, dict[str, str]]:
    """Generator entry. No transport, path, token or budget argument."""
    _reject_kwargs(forbidden)
    return _flight(prompt=prompt, length_ms=length_ms)


def from_client(*, data: object, query: str = "", **forbidden: object) -> tuple[int, bytes, dict[str, str]]:
    """el_client music entry. The nested subscription GET is not used."""
    _reject_kwargs(forbidden)
    if query not in ("", QUERY):
        raise guard.GuardRefused("malformed_request")
    if type(data) is not dict:
        raise guard.GuardRefused("malformed_request")
    allowed = {"prompt", "music_length_ms", "model_id", "force_instrumental"}
    if set(data) - allowed:
        raise guard.GuardRefused("caller_supplied_transport")
    if data.get("model_id") != "music_v2":
        raise guard.GuardRefused("model")
    if data.get("force_instrumental") is not True:
        raise guard.GuardRefused("not_instrumental")
    prompt = data.get("prompt")
    length = data.get("music_length_ms")
    if type(prompt) is not str or type(length) is not int:
        raise guard.GuardRefused("malformed_request")
    return _flight(prompt=prompt, length_ms=length)


def from_multipart(*, fields: object, files: object, **forbidden: object) -> tuple[int, bytes]:
    """Multipart music entry. The uploaded file is not read and not posted."""
    _reject_kwargs(forbidden)
    if type(fields) is not dict or type(files) is not list:
        raise guard.GuardRefused("malformed_request")
    for item in files:
        if type(item) is not tuple or len(item) != 2:
            raise guard.GuardRefused("malformed_request")
    allowed = {"prompt", "music_length_ms", "model_id", "force_instrumental"}
    if set(fields) - allowed:
        raise guard.GuardRefused("caller_supplied_transport")
    if fields.get("model_id") != "music_v2":
        raise guard.GuardRefused("model")
    if str(fields.get("force_instrumental")).lower() != "true":
        raise guard.GuardRefused("not_instrumental")
    if fields.get("music_length_ms") != "180000":
        raise guard.GuardRefused("duration")
    prompt = fields.get("prompt")
    if type(prompt) is not str:
        raise guard.GuardRefused("malformed_request")
    status, body, _headers = _flight(prompt=prompt, length_ms=180_000)
    return status, body
