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
import uuid
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


def headroom(live: int | None, spent: int, pending: int, other: int) -> int:
    if live is None or other is None or min(live, spent, pending, other) < 0:
        raise GuardError("unknown or negative balance/spend/reservations")
    remaining_cap = MAX_TOTAL_CREDITS - spent - pending
    if remaining_cap < 0 or spent + pending > MAX_TOTAL_CREDITS:
        raise GuardError(f"spend {spent}+{pending} exceeds the {MAX_TOTAL_CREDITS} cap")
    # Until a charge is explicitly reconciled to a balance reading, it is an
    # additional liability. Never assume billing has caught up.
    left = int(live) - spent - pending - remaining_cap - int(other)
    if left < HEADROOM_FLOOR:
        raise GuardError(
            f"headroom {left} < {HEADROOM_FLOOR} after reserving remaining cap {remaining_cap} "
            f"and other {other}"
        )
    return left


def can_take(*, live: int | None, spent: int, pending: int, other: int, takes_done: int,
             unknown_pending: bool, cost: int = MAX_CREDITS_PER_TAKE) -> int:
    if unknown_pending:
        raise GuardError("unknown outstanding charges")
    if takes_done >= MAX_TAKES_PER_ROW:
        raise GuardError("row already has 3 takes")
    if cost != MAX_CREDITS_PER_TAKE:
        raise GuardError(f"refusing cost {cost}")
    if spent + pending + cost > MAX_TOTAL_CREDITS:
        raise GuardError(f"cap {MAX_TOTAL_CREDITS}: spent {spent} pending {pending} cost {cost}")
    # The impending take is already inside the remaining cap. Do not release
    # its reservation before the UI has charged it.
    return headroom(live, spent, pending, other)


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


def resolve_parent_clip(media: Path, parent: ParentRef, *, in_scope: bool,
                        ledger: list[dict] | None = None) -> Path | None:
    # In-scope parents must be a proven version from this runner, never a
    # guessed t1 or an older tranche substituted for a failed parent.
    if in_scope:
        for entry in reversed(ledger or []):
            if (entry.get("part"), entry.get("plate_id")) != parent.key:
                continue
            if not verified_entry(entry):
                continue
            return Path(entry["file"])
        return None
    for candidate in parent_clip_candidates(media, parent, in_scope=False):
        if technical_report(candidate)["ok"]:
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
        clip = resolve_parent_clip(media, row.parent, in_scope=in_scope, ledger=ledger)
        if clip is None:
            raise GuardError(f"missing parent clip for {row.parent.raw}")
        dest = (media / "04_Generated-Clips" / f"part{row.part:02d}" / "refs" / "v05_flow_stills"
                / f"{row.plate_id}_from_{row.parent.plate_id}.png")
        return extract_last_frame(clip, dest)
    existing = still_path(media, row.part, row.plate_id)
    if existing.exists() and existing.stat().st_size > 0:
        return existing
    displayed = None if still_price is None else still_price.get("displayed_credits")
    if displayed != 0:
        raise GuardError(f"{row.plate_id} has no start still and Nano Banana price is not a verified 0")
    made = still_maker(row, existing)
    if not Path(made).exists():
        raise GuardError(f"zero-price still for {row.plate_id} was not written")
    return Path(made)



def verify_still_inventory(rows: list[Row], media: Path) -> list[dict]:
    """Validate every independent start still before batch spending is enabled.

    In-scope continuations are derived from proven parent outputs later. Missing
    independent stills stop here; this is not permission to mint a replacement.
    """
    inventory = []
    for row in rows:
        if row.parent is not None:
            continue
        path = still_path(media, row.part, row.plate_id)
        if not path.is_file():
            raise GuardError(f"missing inventory start still P{row.part:02d}:{row.plate_id}")
        digest = sha256_file(path)
        try:
            probe = subprocess.run(
                ["ffprobe", "-v", "error", "-show_streams", "-of", "json", str(path)],
                check=True, capture_output=True, text=True)
            streams = json.loads(probe.stdout)["streams"]
            if len(streams) != 1 or streams[0].get("codec_type") != "video":
                raise GuardError("still needs exactly one image stream")
            width, height = int(streams[0]["width"]), int(streams[0]["height"])
            subprocess.run(["ffmpeg", "-v", "error", "-xerror", "-i", str(path),
                            "-frames:v", "1", "-f", "null", "-"],
                           check=True, capture_output=True)
        except Exception as exc:
            raise GuardError(f"invalid inventory still {path}") from exc
        if width < 1280 or height < 720 or abs(width / height - 16 / 9) > 0.01:
            raise GuardError(f"inventory still is not 16:9 HD: {path}")
        if digest != sha256_file(path):
            raise GuardError(f"inventory changed while reading: {path}")
        inventory.append({"part": row.part, "plate_id": row.plate_id,
                          "path": str(path.resolve()), "sha256": digest,
                          "width": width, "height": height})
    return inventory

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



# Machine-wide paths: independent of channel, checkout, HOS_REPO and cwd.
# Production remains disabled until all Flow writers adopt this contract.
SHARED_FLOW_ROOT = Path.home() / "_desk" / "state" / "flow"
SHARED_FLOW_LOCK = Path.home() / "_desk" / "locks" / "flow-generation.lock"


class SharedFlowState:
    """Crash-safe reservation journal. Caller owns the machine-wide writer lock.

    A SUBMITTING take is uncertain after any interruption; it is never retried or
    silently released. A completed download does not prove a charge is posted.
    Only an explicit reconciliation with external evidence marks a charge posted.
    """

    def __init__(self, root: Path = SHARED_FLOW_ROOT, lock: Path = SHARED_FLOW_LOCK):
        self.root = root
        self.lock_path = lock
        self.lock = None
        self.state = None

    def __enter__(self):
        self.lock = WriterLock(self.lock_path)
        self.lock.__enter__()
        try:
            self.root.mkdir(parents=True, exist_ok=True)
            path = self.root / "state.json"
            self.state = json.loads(path.read_text()) if path.exists() else {
                "schema": 1, "reservations": {}, "takes": {}}
            if (self.state.get("schema") != 1
                    or not isinstance(self.state.get("reservations"), dict)
                    or not isinstance(self.state.get("takes"), dict)):
                raise GuardError("unknown shared Flow journal schema")
            return self
        except BaseException:
            self.lock.__exit__(*sys.exc_info())
            self.lock = None
            raise

    def __exit__(self, *args):
        self.state = None
        if self.lock:
            self.lock.__exit__(*args)
            self.lock = None

    def _save(self):
        if self.state is None or self.lock is None:
            raise GuardError("shared Flow state requires its writer lock")
        dest = self.root / "state.json"
        temp = self.root / (".state-" + uuid.uuid4().hex)
        with temp.open("x") as handle:
            json.dump(self.state, handle, sort_keys=True)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp, dest)
        fd = os.open(self.root, os.O_RDONLY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)

    def reserve(self, owner: str, cap: int):
        if not owner or not isinstance(cap, int) or cap < 0:
            raise GuardError("invalid shared reservation")
        old = self.state["reservations"].get(owner)
        if old is not None and old != cap:
            raise GuardError("reservation cannot change implicitly")
        self.state["reservations"][owner] = cap
        self._save()

    def liabilities(self, owner: str) -> tuple[int, int, int]:
        if owner not in self.state["reservations"]:
            raise GuardError("missing shared reservation")
        consumed = {key: 0 for key in self.state["reservations"]}
        unposted = 0
        for take in self.state["takes"].values():
            who, amount = take["owner"], take["credits"]
            if who not in consumed or not isinstance(amount, int) or amount <= 0:
                raise GuardError("invalid shared charge")
            if take["status"] not in ("SUBMITTING", "COMPLETED", "FAILED"):
                raise GuardError("unknown shared charge status")
            consumed[who] += amount
            if not take.get("posted"):
                unposted += amount
        remaining = {}
        for who, cap in self.state["reservations"].items():
            if not isinstance(cap, int) or cap < consumed[who]:
                raise GuardError("shared reservation cap exceeded")
            remaining[who] = cap - consumed[who]
        return remaining[owner], sum(v for k, v in remaining.items() if k != owner), unposted

    def begin(self, owner: str, take_id: str, live: int, evidence: dict, credits: int = 100):
        if take_id in self.state["takes"]:
            raise GuardError("take already recorded; never retry an uncertain Create")
        if any(t["status"] == "SUBMITTING" for t in self.state["takes"].values()):
            raise GuardError("unresolved shared Create; reconcile before another submit")
        if not evidence or not isinstance(live, int) or live < 0 or credits != 100:
            raise GuardError("invalid live submit evidence")
        own, other, unposted = self.liabilities(owner)
        # The impending charge is INCLUDED in own, not subtracted first.
        if own < credits or live - own - other - unposted < HEADROOM_FLOOR:
            raise GuardError("shared reservation or floor refuses next take")
        self.state["takes"][take_id] = {
            "owner": owner, "credits": credits, "status": "SUBMITTING",
            "posted": False, "evidence": evidence, "at": now_iso()}
        self._save()  # durable BEFORE Create; exceptions leave an uncertain take

    def complete(self, take_id: str, receipt: dict, *, failed: bool = False):
        take = self.state["takes"][take_id]
        if take["status"] != "SUBMITTING" or not receipt:
            raise GuardError("completion requires one pending take and evidence")
        take.update(status="FAILED" if failed else "COMPLETED", receipt=receipt)
        self._save()

    def reconcile_posted(self, take_id: str, proof: dict):
        take = self.state["takes"][take_id]
        if take["status"] == "SUBMITTING" or not proof.get("external_charge_id") or not proof.get("balance_read_at"):
            raise GuardError("posted charge needs resolved take and external charge/balance proof")
        if take.get("posted") and take.get("reconciliation") != proof:
            raise GuardError("posted reconciliation is immutable")
        if any(t.get("reconciliation", {}).get("external_charge_id") == proof["external_charge_id"]
               for key, t in self.state["takes"].items() if key != take_id):
            raise GuardError("external charge already reconciles another take")
        take.update(posted=True, reconciliation=proof)
        self._save()

    def spend_receipt(self, take_id: str) -> dict:
        """Stable outbox payload for idempotent ai_spend integration, not delivery."""
        take = self.state["takes"][take_id]
        return {"id": "flow:" + take_id, "pool": "flow", "amount": take["credits"],
                "film": take["owner"], "at": take["at"]}

def process_alive(pid: int) -> bool:
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


def refuse_duplicate(pid_path: Path, done_path: Path) -> None:
    """A live PID always wins over old completion output."""
    if not pid_path.exists():
        return
    try:
        pid = int(pid_path.read_text().strip())
    except ValueError as exc:
        raise GuardError(f"unreadable pid file {pid_path}") from exc
    if process_alive(pid) and pid != os.getpid():
        raise GuardError(f"runner already live as pid {pid}; completion files cannot override a live PID")


def detached_command(script: Path, log_path: Path, done_path: Path,
                     session: str = "hos009-tranche2", *, media: Path,
                     archive: Path, ledger: Path, lock: Path, pid: Path,
                     other: int, repo: Path) -> list[str]:
    if other < 0 or not media.is_dir() or not archive.is_dir():
        raise GuardError("detach needs existing media/archive and nonnegative reservations")
    # Each invocation has immutable logs and completion output. A running PID
    # is checked inside the runner under its process lock, regardless of .done.
    token = uuid.uuid4().hex
    log_path = log_path.with_name(log_path.name + "." + token)
    done_path = done_path.with_name(done_path.name + "." + token)
    argv = [sys.executable, str(script), "submit", "--repo", str(repo),
            "--media", str(media), "--archive", str(archive), "--ledger", str(ledger),
            "--lock", str(lock), "--pid", str(pid), "--done", str(done_path),
            "--other-reservations", str(other)]
    inner = (shlex.join(argv) + " > " + shlex.quote(str(log_path)) + " 2>&1; "
             + "result=$?; printf '%s\\n' \"$result\" > " + shlex.quote(str(done_path))
             + "; exit \"$result\"")
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


def technical_report(path: Path, *, required_duration: float = 8.0) -> dict:
    report = {"ok": False, "review": "PENDING_REVIEW", "keep": False}
    if not path.exists() or path.stat().st_size < 500:
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
        streams = payload["streams"]
        videos = [v for v in streams if v.get("codec_type") == "video"]
        audio = [v for v in streams if v.get("codec_type") == "audio"]
        width, height = int(videos[0]["width"]), int(videos[0]["height"])
    except (ValueError, KeyError, IndexError, TypeError):
        return report | {"reason": "unreadable video stream"}
    report.update(duration_s=duration, width=width, height=height, audio_streams=len(audio))
    if (probe.returncode or len(videos) != 1 or audio or duration < required_duration - 0.1
            or duration > required_duration + 0.25 or width < 1280 or height < 720
            or abs(width / height - 16 / 9) > 0.01):
        return report | {"reason": "duration, streams or dimensions outside approved 8s 16:9 HD output"}
    decode = subprocess.run(
        ["ffmpeg", "-v", "error", "-xerror", "-i", str(path), "-map", "0:v:0",
         "-f", "null", "-"], capture_output=True, text=True, check=False,
    )
    return report | {"ok": decode.returncode == 0 and not decode.stderr.strip(),
                     "decode_ok": decode.returncode == 0 and not decode.stderr.strip()}


def verified_entry(entry: dict) -> bool:
    if (entry.get("status") != "PENDING_REVIEW" or entry.get("generated") is not True
            or entry.get("keep") is not False or not (entry.get("technical") or {}).get("ok")
            or not (entry.get("archive") or {}).get("verified")):
        return False
    path = Path(entry.get("file") or "")
    archived = Path(entry["archive"].get("dest") or "")
    digest = entry.get("sha256")
    return (path.is_file() and archived.is_file() and digest is not None
            and sha256_file(path) == digest == sha256_file(archived)
            and technical_report(path)["ok"])


def strip_audio(path: Path) -> None:
    silent = path.with_suffix(".silent.mp4")
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", str(path), "-c:v", "copy", "-an", str(silent)],
        check=True,
    )
    silent.replace(path)


def archive_verified(src: Path, dest: Path) -> dict:
    """Exclusive creation; identical retries succeed, collisions are never replaced."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    src_hash = sha256_file(src)
    try:
        with dest.open("xb") as target, src.open("rb") as source:
            shutil.copyfileobj(source, target)
            target.flush()
            os.fsync(target.fileno())
    except FileExistsError:
        if not dest.is_file() or sha256_file(dest) != src_hash:
            raise GuardError(f"archive collision: {dest}; existing bytes preserved")
    dest_hash = sha256_file(dest)
    if src_hash != dest_hash:
        raise GuardError(f"archive hash mismatch: {dest}; preserved for investigation")
    sums = dest.parent / "SHA256SUMS.txt"
    line = f"{dest_hash}  {dest.name}\n"
    existing = sums.read_text() if sums.exists() else ""
    if line not in existing:
        with sums.open("a") as handle:
            handle.write(line)
            handle.flush()
            os.fsync(handle.fileno())
    return {"sha256": dest_hash, "dest": str(dest), "verified": True}


def verify_archive_root(archive: Path | None) -> None:
    if archive is None or not archive.is_dir():
        raise GuardError("verified archive is required before any spend")
    # Production additionally enforces the mounted NAS root in cmd_submit.
    # Probe immutable write/read before any submit; never remove NAS evidence.
    probe = archive / (".tranche2-preflight-" + uuid.uuid4().hex + ".json")
    value = {"at": now_iso(), "purpose": "archive writable/readable preflight", "submissions": 0}
    write_receipt(probe, [], [value])
    if json.loads(probe.read_text())["entries"] != [value]:
        raise GuardError("archive write/read verification failed")


def write_receipt(path: Path, batch_ids: list[str], entries: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"rows": batch_ids, "keep": False, "review": "PENDING_REVIEW", "entries": entries}
    text = json.dumps(payload, indent=2) + "\n"
    try:
        with path.open("x") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
    except FileExistsError:
        if path.read_text() != text:
            raise GuardError(f"immutable receipt collision: {path}")


def execute_batch(batch: list[Row], *, media: Path, ledger_path: Path, lock_path: Path,
                  live: int, other: int, price: PriceEvidence, account: str, read_at: str,
                  now: datetime, submitter, still_price: dict | None = None, still_maker=None,
                  archive_dir: Path | None = None, receipt_path: Path | None = None,
                  in_scope_keys: set[tuple[int, str]] | None = None) -> list[dict]:
    """Mint one guarded batch. submitter is the only Flow video call, and tests pass a fake."""
    assert_batch_limits(batch)
    verify_archive_root(archive_dir)
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
            frame = prepare_start_frame(
                row, media, in_scope_keys=keys, still_price=still_price, still_maker=still_maker,
                ledger=read_ledger(ledger_path),
            )
            previous = read_ledger(ledger_path)
            recorded = [int(e.get("take") or 0) for e in previous
                        if (e.get("part"), e.get("plate_id")) == row.key]
            take, dest = next_version(media, row.part, row.plate_id)
            take = max(take, max(recorded, default=0) + 1)
            if take > MAX_TAKES_PER_ROW:
                raise GuardError(f"{row.plate_id} has exhausted its three immutable takes")
            dest = versioned_output(media, row.part, row.plate_id, take)
            if dest.exists():
                raise GuardError(f"output collision: {dest}")
            dest.parent.mkdir(parents=True, exist_ok=True)
            submit_entry = submitting_record(row.plate_id, row.part, take, dest)
            submit_entry["input"] = {"file": str(frame), "sha256": sha256_file(frame)}
            append_ledger(ledger_path, submit_entry)
            submitter(row, dest, frame)
            strip_error = None
            if dest.exists():
                try:
                    strip_audio(dest)
                except subprocess.CalledProcessError as exc:
                    strip_error = str(exc)
            technical = technical_report(dest)
            if strip_error:
                technical.update(ok=False, reason="audio stripping failed: " + strip_error)
            if not dest.exists():
                raise GuardError("submit has no output; charge unresolved, no automatic retry")
            entry = review_record(row.plate_id, row.part, take, dest, technical)
            entry["input"] = submit_entry["input"]
            entry["evidence"] = {"live": live, "account": account, "read_at": read_at,
                                 "price": price.__dict__}
            entry["archive"] = archive_verified(dest, archive_dir / f"part{row.part:02d}" / dest.name)
            if not technical["ok"]:
                entry["status"] = "FAILED"
            write_receipt(archive_dir / "receipts" / f"p{row.part}_{row.plate_id}_t{take}.json",
                          [row.plate_id], [entry])
            append_ledger(ledger_path, entry)
            written.append(entry)
            if not technical["ok"]:
                raise GuardError(f"technical failure for {row.plate_id}; no advancement")
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


def next_batch(rows: list[Row], ledger: list[dict]) -> list[Row]:
    """Parents first until both are pending review. Then at most five continuations."""
    done = {entry.get("plate_id") for entry in ledger if verified_entry(entry)}
    ordered = [row for row in order_rows(rows) if row.plate_id not in done]
    if not ordered:
        return []
    parents = [row for key in PARENTS for row in ordered if row.key == key]
    if parents:
        return parents
    return batch_rows(ordered, parents_already_done=True)[0]


def cmd_submit(repo: Path, **kwargs) -> list[dict]:
    with WriterLock(Path(str(kwargs["pid_path"]) + ".lock")):
        return _cmd_submit_locked(repo, **kwargs)


def _cmd_submit_locked(repo: Path, *, other: int, media: Path, ledger_path: Path, lock_path: Path,
               pid_path: Path, done_path: Path, archive_dir: Path | None) -> list[dict]:
    """One guarded batch. Caller must already have armed HOS009_TRANCHE2_SUBMIT."""
    # J2275 checkpoint: live control verification and cross-channel accounting
    # remain unresolved. No partial repair may accidentally enable production.
    raise GuardError("J2275 incomplete: live pre-Create proof and canonical shared accounting still require repair")
    if not submit_armed():
        raise SystemExit(
            "refusing submit: generation is not armed "
            f"({SUBMIT_ENV} is not 1). Plan only. J2033 stays blocked until Chief passes this runner."
        )
    nas_root = Path("/Volumes/data/mac-mini-archive")
    if (archive_dir is None or not nas_root.is_dir()
            or not Path("/Volumes/data").is_mount()
            or not archive_dir.resolve().is_relative_to(nas_root.resolve())):
        raise GuardError("submit requires mounted approved NAS archive")
    verify_archive_root(archive_dir)
    refuse_duplicate(pid_path, done_path)
    claim_pid(pid_path)
    rows = load_scope(repo)
    inventory = verify_still_inventory(rows, media)
    write_receipt(archive_dir / "receipts" / ("inventory-" + uuid.uuid4().hex + ".json"),
                  [item["plate_id"] for item in inventory], inventory)
    batch = next_batch(rows, read_ledger(ledger_path))
    if not batch:
        return []
    evidence = read_live_evidence()
    return execute_batch(
        batch,
        media=media,
        ledger_path=ledger_path,
        lock_path=lock_path,
        live=evidence["live"],
        other=other,
        price=evidence["price"],
        account=evidence["account"],
        read_at=evidence["read_at"],
        now=datetime.now(timezone.utc),
        submitter=live_video_submit,
        still_price=evidence.get("still_price"),
        still_maker=live_still_maker,
        archive_dir=archive_dir,
        receipt_path=repo / EDIT_REL / "receipts" / f"tranche2_{uuid.uuid4().hex}.json",
        in_scope_keys={row.key for row in rows},
    )


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
    for name in ("media", "archive", "ledger", "lock", "pid", "repo"):
        detach.add_argument("--" + name, required=True)
    detach.add_argument("--other-reservations", type=int, required=True)
    detach.add_argument("--log", required=True)
    detach.add_argument("--done", required=True)
    args = parser.parse_args(argv)
    if args.cmd == "plan":
        repo = Path(args.repo) if args.repo else repo_root_from()
        cmd_plan(repo, Path(args.out) if args.out else None)
        return 0
    if args.cmd == "detach-command":
        command = detached_command(Path(__file__).resolve(), Path(args.log), Path(args.done),
                                   media=Path(args.media), archive=Path(args.archive),
                                   ledger=Path(args.ledger), lock=Path(args.lock), pid=Path(args.pid),
                                   other=args.other_reservations, repo=Path(args.repo))
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
