#!/usr/bin/env python3
"""HOS 009 tranche-2 Flow mint runner (J2200).

Plans and, only when generation is explicitly armed, mints the 20 approved v05
rows in TRANCHE2_SCOPE_J2026.json. This file does not import or modify
the v04 tranche-1 mint script.

Default command is `plan`. It reads the scope, checks board hashes, orders the
rows and writes a plan. It does not open Chrome, Flow, or a socket, and it
spends nothing.

`submit` is refused unless HOS009_TRANCHE2_SUBMIT=1. J2033 stays blocked until
Chief passes this runner. A submit run still has to pass the credit guards
below before it can call Flow.

Guards (J2033_PREFLIGHT.md / J2026):
- only those 20 v05 rows
- parents P02:10_how_high and P03:07_ball_to_moon first
- continuation start frames are the last frame of the named parent clip
- file state GENERATED and review PENDING_REVIEW; never KEEP
- writer lock, one live process, detached log/.done
- fresh required Flow account and an exact Veo 3.1 Quality x1 price of 100
- pending submits count at full cost; unknown pending charges stop the run
- reserve the unused part of the 6000 cap plus other reservations
- balance after that reservation stays at or above 3000
- a batch is at most 5 rows and 1500 credits; at most 3 takes a row
"""
from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

PARENTS = ((2, "10_how_high"), (3, "07_ball_to_moon"))
REQUIRED_ACCOUNT = "benoats@googlemail.com"
FORBIDDEN_ACCOUNT = "benoats86@gmail.com"
MAX_CREDITS_PER_TAKE = 100
MAX_TAKES_PER_ROW = 3
MAX_TOTAL_CREDITS = 6000
MAX_BATCH_ROWS = 5
MAX_BATCH_CREDITS = 1500
HEADROOM_FLOOR = 3000
REQUIRED_MODEL = "Veo 3.1 - Quality"
REQUIRED_OUTPUTS = "x1"
SUBMIT_ENV = "HOS009_TRANCHE2_SUBMIT"
FLOW_HOST = "flow.google.com"
I2V_RE = re.compile(r"^P(\d+):([A-Za-z0-9_]+) last frame$")
GENERATE_LINE_RE = re.compile(r"^Generating will use (\d+) credits$")

EDIT_REL = Path("02_Video-Projects/009_The-Falling-Moon-Gravity/07_Edit-Project")
SCOPE_NAME = "TRANCHE2_SCOPE_J2026.json"


class GuardError(RuntimeError):
    """A credit, scope, lock or status rule refused the run before any submit."""


@dataclass(frozen=True)
class ParentRef:
    part: int
    plate_id: str
    raw: str

    @property
    def key(self) -> tuple[int, str]:
        return (self.part, self.plate_id)


@dataclass(frozen=True)
class Row:
    part: int
    plate_id: str
    board: str
    quality: str
    max_takes: int
    try1_credits: int
    i2v: str | None
    parent: ParentRef | None
    prompt: str
    use_s: float = 8.0

    @property
    def key(self) -> tuple[int, str]:
        return (self.part, self.plate_id)


@dataclass(frozen=True)
class PriceEvidence:
    model: str
    outputs: str
    credits: int
    generate_line: str
    read_at: str


def repo_root_from(start: Path | None = None) -> Path:
    env = os.environ.get("HOS_REPO")
    if env:
        return Path(env)
    here = start or Path(__file__).resolve()
    for parent in [here, *here.parents]:
        if (parent / "AGENTS.md").exists() and (parent / EDIT_REL).exists():
            return parent
    return Path(__file__).resolve().parents[3]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_parent(i2v: str | None) -> ParentRef | None:
    if not i2v:
        return None
    match = I2V_RE.match(i2v.strip())
    if not match:
        raise GuardError(f"continuation reference is not a named parent clip: {i2v!r}")
    return ParentRef(part=int(match.group(1)), plate_id=match.group(2), raw=i2v.strip())


def load_scope(repo: Path) -> list[Row]:
    """Return the 20 approved v05 rows, after the board files match the scope hashes."""
    scope_path = repo / EDIT_REL / SCOPE_NAME
    scope = json.loads(scope_path.read_text())
    raw_rows = scope.get("rows") or []
    if len(raw_rows) != 20:
        raise GuardError(f"scope has {len(raw_rows)} rows, expected 20")
    rows: list[Row] = []
    seen: set[tuple[int, str]] = set()
    for raw in raw_rows:
        board_rel = Path(raw["board"])
        if "v05" not in board_rel.name:
            raise GuardError(f"{raw.get('id')} is not a v05 board row")
        board_path = repo / board_rel
        digest = sha256_file(board_path)
        if digest != raw["board_sha256"]:
            raise GuardError(f"board hash mismatch for {board_rel}")
        board = json.loads(board_path.read_text())
        plate = next((item for item in board.get("plates") or [] if item.get("id") == raw["id"]), None)
        if plate is None:
            raise GuardError(f"{raw['id']} is not on {board_rel}")
        if int(raw["part"]) != int(plate.get("part") or raw["part"]):
            # Boards identify the part by filename (part-0N). The scope part is the authority.
            pass
        part = int(raw["part"])
        if part < 1 or part > 5:
            raise GuardError(f"{raw['id']} part {part} is outside parts 1-5")
        if f"part-0{part}_plates_v05.json" not in board_rel.name:
            raise GuardError(f"{raw['id']} board file does not match part {part}")
        if plate.get("tranche") != 2 or plate.get("route") != "flow-first":
            raise GuardError(f"{raw['id']} is not an authorised flow-first tranche-2 plate")
        if plate.get("quality") != "Quality" or raw.get("quality") != "Quality":
            raise GuardError(f"{raw['id']} is not Quality")
        if "Quality" not in str(plate.get("flow_model") or ""):
            raise GuardError(f"{raw['id']} flow model is not Quality")
        try1 = int(plate.get("flow_credits_try1") or 0)
        if try1 != MAX_CREDITS_PER_TAKE or int(raw.get("max_takes") or 0) != MAX_TAKES_PER_ROW:
            raise GuardError(f"{raw['id']} price or take cap does not match the scope")
        key = (part, raw["id"])
        if key in seen:
            raise GuardError(f"duplicate scope row {key}")
        seen.add(key)
        i2v = plate.get("i2v_from")
        rows.append(Row(
            part=part,
            plate_id=raw["id"],
            board=str(board_rel),
            quality="Quality",
            max_takes=MAX_TAKES_PER_ROW,
            try1_credits=try1,
            i2v=i2v,
            parent=parse_parent(i2v),
            prompt=str(plate.get("prompt") or ""),
            use_s=float(raw["use_s"]),
        ))
    missing = [f"P{part:02d}:{plate_id}" for part, plate_id in PARENTS if (part, plate_id) not in seen]
    if missing:
        raise GuardError("scope is missing parents " + ", ".join(missing))
    return rows


def order_rows(rows: list[Row]) -> list[Row]:
    """Parents first, then the remaining scope order, with in-scope continuations after their parent."""
    pending = list(rows)
    ordered: list[Row] = []
    for key in PARENTS:
        match = next((row for row in pending if row.key == key), None)
        if match is None:
            raise GuardError(f"missing parent P{key[0]:02d}:{key[1]}")
        pending.remove(match)
        ordered.append(match)
    guard = 0
    while pending:
        guard += 1
        if guard > len(rows) + 2:
            raise GuardError("continuation order did not settle")
        ready = None
        done = {row.key for row in ordered}
        scope_keys = {row.key for row in rows}
        for row in pending:
            parent = row.parent
            if parent is None or parent.key not in scope_keys or parent.key in done:
                ready = row
                break
        if ready is None:
            raise GuardError("in-scope continuation has no ordered parent")
        pending.remove(ready)
        ordered.append(ready)
    return ordered


def batch_rows(rows: list[Row], cost: int = MAX_CREDITS_PER_TAKE, *,
               parents_already_done: bool = False) -> list[list[Row]]:
    """First batch is the two parents. Later batches hold at most 5 rows and 1500 credits."""
    if not rows:
        return []
    if parents_already_done:
        pending = list(rows)
        batches = []
    else:
        if len(rows) < 2 or rows[0].key != PARENTS[0] or rows[1].key != PARENTS[1]:
            raise GuardError("batches require the two parents first")
        batches = [list(rows[:2])]
        pending = list(rows[2:])
    index = 0
    while index < len(pending):
        batch: list[Row] = []
        credits = 0
        while index < len(pending) and len(batch) < MAX_BATCH_ROWS and credits + cost <= MAX_BATCH_CREDITS:
            batch.append(pending[index])
            credits += cost
            index += 1
        if not batch:
            raise GuardError("empty batch")
        batches.append(batch)
    for batch in batches:
        assert_batch_limits(batch, cost)
    return batches


def assert_batch_limits(batch: list[Row], cost: int = MAX_CREDITS_PER_TAKE) -> None:
    if len(batch) > MAX_BATCH_ROWS or len(batch) * cost > MAX_BATCH_CREDITS:
        raise GuardError(
            f"batch of {len(batch)} rows / {len(batch) * cost} credits exceeds "
            f"{MAX_BATCH_ROWS} rows / {MAX_BATCH_CREDITS} credits"
        )


def accept_price(price: PriceEvidence) -> int:
    if price.model != REQUIRED_MODEL:
        raise GuardError(f"model {price.model!r} is not {REQUIRED_MODEL}")
    if price.outputs != REQUIRED_OUTPUTS:
        raise GuardError(f"outputs {price.outputs!r} are not {REQUIRED_OUTPUTS}")
    if int(price.credits) != MAX_CREDITS_PER_TAKE:
        raise GuardError(f"price {price.credits} is not {MAX_CREDITS_PER_TAKE}")
    match = GENERATE_LINE_RE.match(price.generate_line.strip())
    if not match or int(match.group(1)) != MAX_CREDITS_PER_TAKE:
        raise GuardError(f"generate line is not an exact {MAX_CREDITS_PER_TAKE}-credit charge")
    if not price.read_at:
        raise GuardError("price evidence has no read time")
    return MAX_CREDITS_PER_TAKE


def accept_account(account: str | None, read_at: str | None, *, now: datetime, max_age_s: int = 900) -> None:
    if not read_at:
        raise GuardError("balance read is missing")
    stamp = datetime.fromisoformat(read_at)
    if stamp.tzinfo is None:
        stamp = stamp.replace(tzinfo=timezone.utc)
    age = (now - stamp).total_seconds()
    if age < 0 or age > max_age_s:
        raise GuardError(f"balance read is not fresh ({int(age)}s)")
    if account != REQUIRED_ACCOUNT or account == FORBIDDEN_ACCOUNT:
        raise GuardError("Flow account is not the required HOS Ultra account")


def ledger_totals(entries: list[dict], cost: int = MAX_CREDITS_PER_TAKE) -> tuple[int, int, bool, dict[str, int]]:
    """The later line for a take wins, so SUBMITTING then PENDING_REVIEW counts once."""
    latest: dict[tuple[str, int], dict] = {}
    for entry in entries:
        status = entry.get("status")
        if status == "KEEP" or entry.get("keep") is True:
            raise GuardError("ledger contains KEEP; tranche 2 never auto-KEEP")
        if status not in ("SUBMITTING", "PENDING_REVIEW", "GENERATED", "FAILED"):
            raise GuardError(f"unknown ledger status {status!r}")
        plate_id = str(entry.get("plate_id") or "")
        take = int(entry.get("take") or 0)
        latest[(plate_id, take)] = entry
    spent = 0
    pending = 0
    unknown = False
    takes: dict[str, int] = {}
    for (plate_id, _take), entry in latest.items():
        takes[plate_id] = takes.get(plate_id, 0) + 1
        status = entry.get("status")
        if status == "SUBMITTING":
            reserved = entry.get("credits_reserved")
            if reserved is None:
                unknown = True
            else:
                pending += int(reserved)
        else:
            amount = entry.get("credits_used")
            if amount is None:
                amount = entry.get("credits_reserved")
            if amount is None:
                unknown = True
            else:
                spent += int(amount)
    if any(count > MAX_TAKES_PER_ROW for count in takes.values()):
        raise GuardError("a row already has more than 3 takes")
    return spent, pending, unknown, takes


def headroom(live: int | None, spent: int, pending: int, other: int, *,
             posted: int = 0) -> int:
    if live is None or other is None or other < 0:
        raise GuardError("unknown balance or other reservations")
    if min(spent, pending, posted) < 0 or posted > spent:
        raise GuardError("invalid posted/unposted accounting")
    remaining_cap = MAX_TOTAL_CREDITS - spent - pending
    if remaining_cap < 0 or spent + pending > MAX_TOTAL_CREDITS:
        raise GuardError(f"spend {spent}+{pending} exceeds the {MAX_TOTAL_CREDITS} cap")
    # Only reconciled posted charges may already be reflected in the UI balance.
    # Every other charge remains a liability, including the impending take.
    unposted = spent - posted + pending
    left = int(live) - unposted - remaining_cap - int(other)
    if left < HEADROOM_FLOOR:
        raise GuardError(
            f"headroom {left} < {HEADROOM_FLOOR} after reserving remaining cap {remaining_cap} "
            f"and other {other}"
        )
    return left


def can_take(*, live: int | None, spent: int, pending: int, other: int, takes_done: int,
             unknown_pending: bool, cost: int = MAX_CREDITS_PER_TAKE, posted: int = 0) -> int:
    if unknown_pending:
        raise GuardError("unknown outstanding charges")
    if takes_done >= MAX_TAKES_PER_ROW:
        raise GuardError("row already has 3 takes")
    if cost != MAX_CREDITS_PER_TAKE:
        raise GuardError(f"refusing cost {cost}")
    if spent + pending + cost > MAX_TOTAL_CREDITS:
        raise GuardError(f"cap {MAX_TOTAL_CREDITS}: spent {spent} pending {pending} cost {cost}")
    # The new take joins pending charges before Flow is clicked.
    return headroom(live, spent, pending + cost, other, posted=posted)


def start_plan(row: Row) -> dict:
    if row.parent is None:
        return {
            "kind": "existing_still_or_zero_price",
            "plate_id": row.plate_id,
            "part": row.part,
        }
    return {
        "kind": "parent_last_frame",
        "plate_id": row.plate_id,
        "part": row.part,
        "parent_part": row.parent.part,
        "parent_id": row.parent.plate_id,
        "reference": row.parent.raw,
    }


def build_plan(rows: list[Row]) -> dict:
    ordered = order_rows(rows)
    batches = batch_rows(ordered)
    return {
        "job": "J2200",
        "film": "HOS:009",
        "submissions": 0,
        "keep": False,
        "review": "PENDING_REVIEW",
        "file_state_when_written": "GENERATED",
        "row_count": len(ordered),
        "caps": {
            "per_take": MAX_CREDITS_PER_TAKE,
            "takes_per_row": MAX_TAKES_PER_ROW,
            "total": MAX_TOTAL_CREDITS,
            "batch_rows": MAX_BATCH_ROWS,
            "batch_credits": MAX_BATCH_CREDITS,
            "floor": HEADROOM_FLOOR,
        },
        "order": [start_plan(row) | {"id": row.plate_id, "part": row.part} for row in ordered],
        "batches": [[row.plate_id for row in batch] for batch in batches],
    }


def versioned_output(media: Path, part: int, plate_id: str, take: int) -> Path:
    return (media / "04_Generated-Clips" / f"part{part:02d}" / "raw" / "v05_tranche2"
            / f"{plate_id}_t{take}.mp4")


def next_version(media: Path, part: int, plate_id: str) -> tuple[int, Path]:
    for take in range(1, MAX_TAKES_PER_ROW + 1):
        dest = versioned_output(media, part, plate_id, take)
        if not dest.exists():
            return take, dest
    raise GuardError(f"{plate_id} already has {MAX_TAKES_PER_ROW} versioned files; none will be overwritten")


def still_path(media: Path, part: int, plate_id: str) -> Path:
    return media / "04_Generated-Clips" / f"part{part:02d}" / "refs" / "v05_flow_stills" / f"{plate_id}_t1.png"


def parent_clip_candidates(media: Path, parent: ParentRef, *, in_scope: bool) -> list[Path]:
    root = media / "04_Generated-Clips" / f"part{parent.part:02d}" / "raw"
    found = []
    if in_scope:
        found.append(root / "v05_tranche2" / f"{parent.plate_id}_t1.mp4")
    found.append(root / "v01" / f"{parent.plate_id}_t1.mp4")
    return found


def resolve_parent_clip(media: Path, parent: ParentRef, *, in_scope: bool) -> Path | None:
    for candidate in parent_clip_candidates(media, parent, in_scope=in_scope):
        if candidate.exists() and candidate.stat().st_size > 0:
            return candidate
    return None


def extract_last_frame(src: Path, dest: Path) -> Path:
    """Copy the closing picture of a named parent clip. No Flow call."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-sseof", "-0.08", "-i", str(src),
         "-frames:v", "1", str(dest)],
        check=True,
    )
    if not dest.exists() or dest.stat().st_size < 100:
        raise GuardError(f"could not extract a last frame from {src}")
    return dest


def prepare_start_frame(row: Row, media: Path, *, in_scope_keys: set[tuple[int, str]],
                         still_price: dict | None, still_maker, ledger: list[dict] | None = None) -> Path:
    if row.parent is not None:
        in_scope = row.parent.key in in_scope_keys
        if in_scope:
            candidates = [entry for entry in latest_entries(ledger or [])
                          if entry.get("plate_id") == row.parent.plate_id and
                          entry.get("part") == row.parent.part and verified_output(entry)]
            if not candidates:
                raise GuardError(f"no technically verified parent: {row.parent.raw}")
            clip = Path(max(candidates, key=lambda entry: entry["take"])["file"])
        else:
            clip = resolve_parent_clip(media, row.parent, in_scope=False)
            if clip is not None and not technical_report(clip)["ok"]:
                raise GuardError(f"invalid external parent: {clip}")
        if clip is None:
            raise GuardError(f"missing parent clip for {row.parent.raw}")
        dest = (media / "04_Generated-Clips" / f"part{row.part:02d}" / "refs" / "v05_flow_stills"
                / f"{row.plate_id}_from_{row.parent.plate_id}.png")
        return extract_last_frame(clip, dest)
    existing = still_path(media, row.part, row.plate_id)
    if existing.exists() and existing.stat().st_size > 0:
        probe = subprocess.run(["ffmpeg", "-v", "error", "-xerror", "-i", str(existing),
                                "-frames:v", "1", "-f", "null", "-"], capture_output=True)
        if probe.returncode:
            raise GuardError(f"start still does not decode: {existing}")
        immutable_bytes(existing.with_suffix(".sha256"), (sha256_file(existing) + "\n").encode())
        return existing
    displayed = None if still_price is None else still_price.get("displayed_credits")
    if displayed != 0:
        raise GuardError(f"{row.plate_id} has no start still and Nano Banana price is not a verified 0")
    made = still_maker(row, existing)
    if not Path(made).exists():
        raise GuardError(f"zero-price still for {row.plate_id} was not written")
    return Path(made)


def accept_zero_still_price(still_price: dict | None) -> None:
    if not still_price or still_price.get("displayed_credits") != 0:
        raise GuardError("Nano Banana still price is not a verified 0")
    if int(still_price.get("displayed_credits")) > 0:
        raise GuardError("charged stills need a revised scope")


class WriterLock:
    """Exclusive non-blocking lock. A second process gets GuardError."""

    def __init__(self, path: Path):
        self.path = Path(path)
        self.handle = None

    def __enter__(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.handle = self.path.open("a+")
        try:
            fcntl.flock(self.handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            self.handle.close()
            raise GuardError(f"writer lock held: {self.path}") from exc
        return self

    def __exit__(self, exc_type, exc, tb):
        if self.handle is not None:
            fcntl.flock(self.handle.fileno(), fcntl.LOCK_UN)
            self.handle.close()
            self.handle = None
        return False


def process_alive(pid: int) -> bool:
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


def refuse_duplicate(pid_path: Path, done_path: Path) -> None:
    """A live pid wins even when a stale .done file is present."""
    if not pid_path.exists():
        return
    try:
        pid = int(pid_path.read_text().strip())
    except ValueError as exc:
        raise GuardError(f"unreadable pid file {pid_path}") from exc
    if process_alive(pid) and pid != os.getpid():
        raise GuardError(f"runner already live as pid {pid}; {done_path.name} is absent")


def detached_command(script: Path, log_path: Path, done_path: Path,
                     session: str = "hos009-tranche2") -> list[str]:
    python = shlex.quote(sys.executable)
    inner = (
        f"cd {shlex.quote(str(script.parent))} && {python} {shlex.quote(str(script))} submit "
        f"> {shlex.quote(str(log_path))} 2>&1; echo $? > {shlex.quote(str(done_path))}"
    )
    return ["tmux", "new", "-d", "-s", session, inner]


def claim_pid(pid_path: Path) -> None:
    pid_path.parent.mkdir(parents=True, exist_ok=True)
    pid_path.write_text(str(os.getpid()) + "\n")


def append_ledger(path: Path, entry: dict) -> None:
    if entry.get("status") == "KEEP" or entry.get("keep") is True:
        raise GuardError("refusing to record KEEP")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as handle:
        handle.write(json.dumps(entry, sort_keys=True) + "\n")
        handle.flush()
        os.fsync(handle.fileno())


def read_ledger(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text().splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def review_record(plate_id: str, part: int, take: int, dest: Path, technical: dict) -> dict:
    """Generated and review are separate. Review stays PENDING_REVIEW."""
    return {
        "plate_id": plate_id,
        "part": part,
        "take": take,
        "status": "PENDING_REVIEW",
        "file_state": "GENERATED",
        "generated": True,
        "review": "PENDING_REVIEW",
        "keep": False,
        "file": str(dest),
        "sha256": technical.get("sha256"),
        "technical": technical,
        "credits_reserved": MAX_CREDITS_PER_TAKE,
        "credits_used": MAX_CREDITS_PER_TAKE,
        "at": now_iso(),
    }


def submitting_record(plate_id: str, part: int, take: int, dest: Path) -> dict:
    return {
        "plate_id": plate_id,
        "part": part,
        "take": take,
        "status": "SUBMITTING",
        "generated": False,
        "review": "PENDING_REVIEW",
        "keep": False,
        "file": str(dest),
        "credits_reserved": MAX_CREDITS_PER_TAKE,
        "at": now_iso(),
    }


def technical_report(path: Path, *, required_s: float = 8.0,
                     min_width: int = 1280, min_height: int = 720) -> dict:
    """Decode/format checks only; these never imply perceptual KEEP."""
    report = {"ok": False, "review": "PENDING_REVIEW", "keep": False}
    if not path.is_file() or path.stat().st_size < 500:
        return report | {"reason": "missing or tiny"}
    report.update(sha256=sha256_file(path), bytes=path.stat().st_size)
    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "format=duration:stream=codec_type,width,height", "-of", "json", str(path)],
        capture_output=True, text=True, check=False,
    )
    try:
        payload = json.loads(probe.stdout)
        duration = float(payload["format"]["duration"])
        videos = [v for v in payload["streams"] if v["codec_type"] == "video"]
        audio = sum(v["codec_type"] == "audio" for v in payload["streams"])
        video = videos[0] if len(videos) == 1 else {}
        width, height = int(video.get("width", 0)), int(video.get("height", 0))
    except (ValueError, KeyError, TypeError):
        return report | {"reason": "invalid probe"}
    decode = subprocess.run(
        ["ffmpeg", "-v", "error", "-xerror", "-i", str(path),
         "-map", "0:v:0", "-f", "null", "-"], capture_output=True, check=False,
    )
    report.update(duration_s=duration, audio_streams=audio, width=width, height=height,
                  decode_ok=decode.returncode == 0)
    report["ok"] = bool(probe.returncode == 0 and decode.returncode == 0 and
                        len(videos) == 1 and audio == 0 and duration >= required_s - 0.08 and
                        width >= min_width and height >= min_height and
                        abs(width / max(height, 1) - 16 / 9) < 0.02)
    return report


def strip_audio(path: Path) -> None:
    silent = path.with_suffix(".silent.mp4")
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", str(path), "-c:v", "copy", "-an", str(silent)],
        check=True,
    )
    silent.replace(path)


def immutable_bytes(path: Path, data: bytes) -> None:
    """Exclusive create; identical retries are idempotent, collisions are errors."""
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("xb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
    except FileExistsError:
        if path.read_bytes() != data:
            raise GuardError(f"immutable destination differs: {path}")


def archive_verified(src: Path, dest: Path) -> dict:
    """Never overwrite or delete an archive, including failed copies."""
    src_hash = sha256_file(src)
    immutable_bytes(dest, src.read_bytes())
    dest_hash = sha256_file(dest)
    if src_hash != dest_hash:
        raise GuardError(f"hash mismatch for {dest}; archive preserved")
    evidence = {"sha256": dest_hash, "dest": str(dest), "verified": True}
    immutable_bytes(dest.with_suffix(dest.suffix + ".sha256.json"),
                    (json.dumps(evidence, sort_keys=True) + "\n").encode())
    return evidence


def require_archive(archive_dir: Path | None, *, nas: bool = True) -> Path:
    if archive_dir is None:
        raise GuardError("a verified archive is mandatory before submit")
    archive = archive_dir.resolve()
    if not archive.is_dir():
        raise GuardError("archive directory must already exist")
    if nas:
        volumes = Path("/Volumes")
        if volumes not in archive.parents:
            raise GuardError("production archive must be on the mounted NAS")
        mount = volumes / archive.relative_to(volumes).parts[0]
        if not os.path.ismount(mount):
            raise GuardError("archive volume is not mounted")
    # Persist/read back a unique sentinel, without touching an existing file.
    import uuid
    probe = archive / (".tranche2-write-probe-" + uuid.uuid4().hex)
    immutable_bytes(probe, b"tranche2 archive writable\n")
    if probe.read_bytes() != b"tranche2 archive writable\n":
        raise GuardError("archive write verification failed")
    return archive


def write_receipt(path: Path, batch_ids: list[str], entries: list[dict]) -> None:
    payload = {"rows": batch_ids, "keep": False, "review": "PENDING_REVIEW", "entries": entries}
    immutable_bytes(path, (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode())


def execute_batch(batch: list[Row], *, media: Path, ledger_path: Path, lock_path: Path,
                  live: int, other: int, price: PriceEvidence, account: str, read_at: str,
                  now: datetime, submitter, still_price: dict | None = None, still_maker=None,
                  archive_dir: Path | None = None, receipt_path: Path | None = None,
                  in_scope_keys: set[tuple[int, str]] | None = None,
                  test_archive: bool = False) -> list[dict]:
    """Mint one guarded batch. submitter is the only Flow video call, and tests pass a fake."""
    assert_batch_limits(batch)
    archive_dir = require_archive(archive_dir, nas=not test_archive)
    accept_price(price)
    accept_account(account, read_at, now=now)
    keys = in_scope_keys or set()
    written: list[dict] = []
    with WriterLock(lock_path):
        entries = read_ledger(ledger_path)
        spent, pending, unknown, takes = ledger_totals(entries)
        latest = {}
        for entry in entries:
            latest[(entry.get("plate_id"), int(entry.get("take") or 0))] = entry.get("status")
        open_plates = {plate for (plate, _take), status in latest.items() if status == "SUBMITTING"}
        for row in batch:
            if row.plate_id in open_plates:
                raise GuardError(f"{row.plate_id} still has an unresolved submit")
            can_take(live=live, spent=spent, pending=pending, other=other,
                     takes_done=takes.get(row.plate_id, 0), unknown_pending=unknown,
                     cost=price.credits)
            pending += price.credits
        for row in batch:
            # All unresolved submits stop retries after a crash.
            if any(item.get("status") == "SUBMITTING" for item in latest_entries(entries)):
                raise GuardError("unresolved submit; reconcile before retry")
            frame = prepare_start_frame(
                row, media, in_scope_keys=keys, still_price=still_price, still_maker=still_maker,
                ledger=entries,
            )
            take, dest = next_version(media, row.part, row.plate_id)
            dest.parent.mkdir(parents=True, exist_ok=True)
            submit_entry = submitting_record(row.plate_id, row.part, take, dest)
            append_ledger(ledger_path, submit_entry)
            submitter(row, dest, frame)
            if dest.exists():
                strip_audio(dest)
            technical = technical_report(dest, required_s=max(8.0, row.use_s))
            if not dest.exists():
                raise GuardError("submitted output missing; charge remains unresolved")
            entry = review_record(row.plate_id, row.part, take, dest, technical)
            entry["archive"] = archive_verified(dest, archive_dir / dest.name)
            entry["price_evidence"] = vars(price)
            entry["balance_evidence"] = {"live": live, "account": account, "read_at": read_at}
            if not technical["ok"]:
                entry["status"] = "FAILED"
            write_receipt(archive_dir / (dest.name + ".receipt.json"), [row.plate_id], [entry])
            append_ledger(ledger_path, entry)
            entries.append(entry)
            written.append(entry)
            if not technical["ok"]:
                raise GuardError(f"technical validation failed: {dest}; no advancement")
    if receipt_path is not None:
        write_receipt(receipt_path, [row.plate_id for row in batch], written)
    return written


def open_flow_page(browser, flow_home: str, goto):
    """Reuse the open Flow tab via the shared Orbit helper. Does not open a second Flow tab."""
    owb = Path(os.environ.get("OWB_REPO", str(Path.home() / "YouTube/orbit-with-ben")))
    sys.path.insert(0, str(owb / "scripts"))
    from cdp_tabs import reuse_page
    page = reuse_page(browser.contexts[0], FLOW_HOST)
    url = page.url or ""
    if FLOW_HOST in url and "/about" not in url:
        return page
    goto(page, flow_home)
    return page


def live_video_submit(row: Row, dest: Path, frame: Path) -> None:
    """Real Flow call. Unreachable unless submit was armed. Tests never call this."""
    if os.environ.get(SUBMIT_ENV) != "1":
        raise GuardError("live submit is not armed")
    repo = repo_root_from()
    sys.path.insert(0, str(repo / "04_Audio/tools"))
    import orbit_flow_veo_ui as flow
    from playwright.sync_api import sync_playwright

    model = REQUIRED_MODEL
    os.environ["ORBIT_FLOW_VEO_MODEL"] = model
    prompt = (
        "Animate the attached start frame; keep its exact cartoon look, objects and light. "
        + " ".join(row.prompt.split())
        + " Silent picture only. Continuous real camera and subject motion through the final frame."
        + " No readable handwriting, letters or numbers anywhere."
    )
    cdp = os.environ.get("ORBIT_FLOW_CDP", "http://127.0.0.1:9222")
    with sync_playwright() as playwright:
        browser = playwright.chromium.connect_over_cdp(cdp)
        page = open_flow_page(
            browser,
            flow.FLOW_HOME,
            lambda current, url: current.goto(url, wait_until="domcontentloaded", timeout=120_000),
        )
        flow.generate_clip(
            page, prompt, dest, model=model, timeout_s=700,
            start_frame=frame, attempts=1, reuse_project=False,
        )


def cmd_plan(repo: Path, out: Path | None) -> dict:
    plan = build_plan(load_scope(repo))
    if plan["submissions"] != 0 or plan["keep"] is not False:
        raise GuardError("plan tried to submit or keep")
    text = json.dumps(plan, indent=2) + "\n"
    if out is not None:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text)
    else:
        sys.stdout.write(text)
    return plan


def submit_armed(env: dict | None = None) -> bool:
    return (env if env is not None else os.environ).get(SUBMIT_ENV) == "1"


def latest_entries(entries: list[dict]) -> list[dict]:
    latest = {}
    for entry in entries:
        latest[(entry.get("part"), entry.get("plate_id"), entry.get("take"))] = entry
    return list(latest.values())


def verified_output(entry: dict) -> bool:
    if not (entry.get("status") == "PENDING_REVIEW" and entry.get("generated") is True
            and entry.get("keep") is False and (entry.get("technical") or {}).get("ok") is True
            and (entry.get("archive") or {}).get("verified") is True):
        return False
    path = Path(entry.get("file", ""))
    archive = Path(entry["archive"].get("dest", ""))
    return (path.is_file() and archive.is_file() and
            sha256_file(path) == entry.get("sha256") == sha256_file(archive) ==
            entry["archive"].get("sha256"))


def next_batch(rows: list[Row], ledger: list[dict]) -> list[Row]:
    """Parents first until both are pending review. Then at most five continuations."""
    done = {
        entry.get("plate_id")
        for entry in latest_entries(ledger)
        if verified_output(entry)
    }
    ordered = [row for row in order_rows(rows) if row.plate_id not in done]
    if not ordered:
        return []
    parents = [row for key in PARENTS for row in ordered if row.key == key]
    if parents:
        return parents
    return batch_rows(ordered, parents_already_done=True)[0]


def cmd_submit(repo: Path, *, other: int, media: Path, ledger_path: Path, lock_path: Path,
               pid_path: Path, done_path: Path, archive_dir: Path | None) -> list[dict]:
    """Production interlock until the remaining J2275 repairs are reviewed."""
    if not submit_armed():
        raise SystemExit(
            "refusing submit: generation is not armed "
            f"({SUBMIT_ENV} is not 1). Plan only. J2033 stays blocked until Chief passes this runner."
        )
    raise GuardError("J2275 repair checkpoint: live per-Create UI guard and shared accounting still pending; no generation")


def read_live_evidence() -> dict:
    """Fresh account, balance and the exact Quality x1 price. Stops before any generate."""
    if not submit_armed():
        raise GuardError("refusing to read Flow because generation is not armed")
    repo = repo_root_from()
    sys.path.insert(0, str(repo / "04_Audio/tools"))
    sys.path.insert(0, str(repo / "02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project"))
    import orbit_flow_veo_ui as flow
    from playwright.sync_api import sync_playwright
    mint006 = _load_mint006(repo)
    cdp = os.environ.get("ORBIT_FLOW_CDP", "http://127.0.0.1:9222")
    with sync_playwright() as playwright:
        browser = playwright.chromium.connect_over_cdp(cdp)
        page = open_flow_page(
            browser,
            flow.FLOW_HOME,
            lambda current, url: current.goto(url, wait_until="domcontentloaded", timeout=120_000),
        )
        credits, account = mint006.read_account(page)
        text = ""
        try:
            text = page.locator("body").inner_text(timeout=8000)
        except Exception as exc:
            raise GuardError(f"could not read the Flow price: {exc}") from exc
    read_at = now_iso()
    lines = [line.strip() for line in text.splitlines() if line.strip().startswith("Generating will use")]
    if len(lines) != 1:
        raise GuardError("Flow price line is missing or not unique; refusing to guess")
    # The selected model and outputs have to be passed as their own fields. A menu
    # that also lists x2/x4 is not evidence that x1 is selected.
    model = os.environ.get("HOS009_TRANCHE2_SELECTED_MODEL", "")
    outputs = os.environ.get("HOS009_TRANCHE2_SELECTED_OUTPUTS", "")
    if model != REQUIRED_MODEL or outputs != REQUIRED_OUTPUTS:
        raise GuardError(
            "set HOS009_TRANCHE2_SELECTED_MODEL and HOS009_TRANCHE2_SELECTED_OUTPUTS "
            "from the selected Flow controls (Veo 3.1 - Quality and x1) before submit"
        )
    price = PriceEvidence(
        model=model, outputs=outputs, credits=MAX_CREDITS_PER_TAKE,
        generate_line=lines[0], read_at=read_at,
    )
    accept_price(price)
    accept_account(account, read_at, now=datetime.now(timezone.utc))
    if credits is None:
        raise GuardError("Flow balance was not readable")
    return {"live": int(credits), "account": account, "read_at": read_at, "price": price, "still_price": None}


def _load_mint006(repo: Path):
    import importlib.util
    path = repo / "02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project/_mint_flow_cdp_v01.py"
    spec = importlib.util.spec_from_file_location("hos006_mint_tranche2", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


def live_still_maker(row: Row, dest: Path) -> Path:
    """Zero-credit stills only. This build does not call it unless a verified 0 is on screen."""
    raise GuardError(
        f"no start still for {row.plate_id}. A Nano Banana still needs a verified on-screen price of 0 "
        "and a separate still call; stopping rather than guessing."
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="HOS 009 tranche-2 Flow runner")
    sub = parser.add_subparsers(dest="cmd", required=True)
    plan = sub.add_parser("plan", help="write the mint order; submit nothing")
    plan.add_argument("--out")
    plan.add_argument("--repo")
    submit = sub.add_parser("submit", help="refused unless HOS009_TRANCHE2_SUBMIT=1")
    submit.add_argument("--repo")
    submit.add_argument("--media", required=False)
    submit.add_argument("--other-reservations", type=int, required=False)
    submit.add_argument("--ledger", required=False)
    submit.add_argument("--lock", required=False)
    submit.add_argument("--pid", required=False)
    submit.add_argument("--done", required=False)
    submit.add_argument("--archive", required=False)
    detach = sub.add_parser("detach-command", help="print the tmux command; start nothing")
    detach.add_argument("--log", required=True)
    detach.add_argument("--done", required=True)
    args = parser.parse_args(argv)
    if args.cmd == "plan":
        repo = Path(args.repo) if args.repo else repo_root_from()
        cmd_plan(repo, Path(args.out) if args.out else None)
        return 0
    if args.cmd == "detach-command":
        command = detached_command(Path(__file__).resolve(), Path(args.log), Path(args.done))
        sys.stdout.write(json.dumps(command) + "\n")
        return 0
    if not submit_armed():
        raise SystemExit(
            "refusing submit: generation is not armed "
            f"({SUBMIT_ENV} is not 1). Plan only. J2033 stays blocked until Chief passes this runner."
        )
    if args.other_reservations is None or not args.media:
        raise GuardError("armed submit needs --other-reservations and --media")
    repo = Path(args.repo) if args.repo else repo_root_from()
    edit = repo / EDIT_REL
    cmd_submit(
        repo,
        other=args.other_reservations,
        media=Path(args.media),
        ledger_path=Path(args.ledger) if args.ledger else edit / "FLOW_MINT_LEDGER_v05_tranche2.jsonl",
        lock_path=Path(args.lock) if args.lock else edit / "tranche2_writer.lock",
        pid_path=Path(args.pid) if args.pid else edit / "tranche2_runner.pid",
        done_path=Path(args.done) if args.done else edit / "tranche2_runner.done",
        archive_dir=Path(args.archive) if args.archive else None,
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except GuardError as exc:
        print(f"STOP {exc}", file=sys.stderr)
        raise SystemExit(2)
