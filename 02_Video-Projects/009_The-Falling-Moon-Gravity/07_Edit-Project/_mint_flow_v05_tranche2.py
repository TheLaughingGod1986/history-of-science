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
import inspect
import json
import math
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
# Chief price pass, 10 Nov 2026 (J2481): Flow replaced "Nano Banana 2" with "Nano Banana 2.1" in place in the model
# menu, and live Flow reads "Generating will use 0 credits" for one 16:9 image on Ultra. One exact name is approved;
# the zero-price line and the balance-did-not-drop check below still gate every still, whatever the model is called.
REQUIRED_STILL_MODEL = "Nano Banana 2.1"
REQUIRED_OUTPUTS = "x1"
SUBMIT_ENV = "HOS009_TRANCHE2_SUBMIT"
FLOW_HOST = "flow.google.com"
I2V_RE = re.compile(r"^P(\d+):([A-Za-z0-9_]+) last frame$")
GENERATE_LINE_RE = re.compile(r"^Generating will use (\d+) credits$")

EDIT_REL = Path("02_Video-Projects/009_The-Falling-Moon-Gravity/07_Edit-Project")
SCOPE_NAME = "TRANCHE2_SCOPE_J2026.json"
PLAN_NAME = "PICTURE_PLAN_v04.json"


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
    here = start or Path(__file__).resolve()
    for parent in [here, *here.parents]:
        if (parent / "AGENTS.md").exists() and (parent / EDIT_REL).exists():
            return parent
    env = os.environ.get("HOS_REPO")
    if env:
        return Path(env)
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


def load_plan_style_refs(repo: Path | None = None) -> list[str]:
    plan_path = (repo or repo_root_from()) / EDIT_REL / PLAN_NAME
    payload = json.loads(plan_path.read_text())
    refs = payload.get("style_refs") if isinstance(payload, dict) else None
    if not isinstance(refs, list) or not refs or not all(isinstance(r, str) and r.strip() for r in refs):
        raise GuardError(f"film plan {plan_path} is missing non-empty style_refs")
    return [r.strip() for r in refs]


def build_plan(rows: list[Row], *, repo: Path | None = None) -> dict:
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
        "style_refs": load_plan_style_refs(repo),
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
            if clip is not None and not technical_report(clip, required_s=4.99)["ok"]:
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
        if width < 1280 or height < 720 or abs(width / height - 16 / 9) >= 0.02:
            raise GuardError(f"inventory still is not 16:9 HD: {path}")
        if digest != sha256_file(path):
            raise GuardError(f"inventory changed while reading: {path}")
        pin = path.with_suffix(".sha256")
        if pin.exists() and pin.read_text().strip() != digest:
            raise GuardError(f"inventory differs from pinned start still: {path}")
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


def shared_flow_state_dir() -> Path:
    """One account ledger for both channels and all checkouts; never repo-local."""
    return Path.home() / "_desk/state/flow/shared"


class SharedFlowAccounting:
    """Durable liabilities, serialized across channels, with explicit reconciliation.

    A caller must hold this context from the live browser read through Create and
    outcome persistence. Pending intents survive a crash and block every writer.
    This component does not infer posted charges from a falling UI balance.
    Production stays interlocked until all Flow writers adopt this protocol.
    """

    def __init__(self, state: Path | None = None):
        self.state = state if state is not None else shared_flow_state_dir()
        self.lock = WriterLock(self.state / "writer.lock")
        self.path = self.state / "account.jsonl"
        self.held = False

    def __enter__(self):
        self.lock.__enter__()
        self.held = True
        try:
            self.snapshot()
        except BaseException:
            self.__exit__(None, None, None)
            raise
        return self

    def __exit__(self, *args):
        self.held = False
        return self.lock.__exit__(*args)

    def _assert_held(self):
        if not self.held:
            raise GuardError("shared Flow writer lock is not held")

    @staticmethod
    def _amount(value):
        if type(value) is not int or value < 0:
            raise GuardError("invalid shared credit amount")
        return value

    def snapshot(self) -> dict:
        self._assert_held()
        reservations, charges = {}, {}
        try:
            data = self.path.read_bytes() if self.path.exists() else b""
            if data and not data.endswith(b"\n"):
                raise GuardError("torn shared Flow ledger; reconcile before any Create")
            for line in data.splitlines():
                event = json.loads(line)
                if not isinstance(event, dict):
                    raise GuardError("shared Flow event is not an object")
                kind, key = event["kind"], event["id"]
                if not isinstance(key, str) or not key:
                    raise GuardError("invalid shared event identity")
                if kind == "reserve":
                    cap = self._amount(event["cap"])
                    if not event.get("film") or key in reservations:
                        raise GuardError("duplicate or unowned reservation")
                    reservations[key] = dict(cap=cap, film=event["film"], active=True)
                elif kind == "release":
                    if key not in reservations or not reservations[key]["active"]:
                        raise GuardError("unknown/repeated reservation release")
                    if any(c["reservation"] == key and c["status"] == "PENDING" for c in charges.values()):
                        raise GuardError("cannot release unresolved pending charge")
                    reservations[key]["active"] = False
                elif kind == "intent":
                    reservation = event["reservation"]
                    if key in charges or reservation not in reservations or not reservations[reservation]["active"]:
                        raise GuardError("duplicate charge or inactive reservation")
                    amount = self._amount(event["amount"])
                    used = sum(c["amount"] for c in charges.values() if c["reservation"] == reservation)
                    if amount <= 0 or used + amount > reservations[reservation]["cap"]:
                        raise GuardError("charge exceeds reservation cap")
                    charges[key] = dict(reservation=reservation, amount=amount, status="PENDING", posted=False)
                elif kind in ("charged", "not_submitted"):
                    charge = charges[key]
                    if charge["status"] != "PENDING" or not event.get("evidence"):
                        raise GuardError("invalid pending charge resolution")
                    charge["status"] = "CHARGED" if kind == "charged" else "NOT_SUBMITTED"
                    if kind == "not_submitted":
                        charge["amount"] = 0
                elif kind == "posted":
                    charge = charges[key]
                    if charge["status"] != "CHARGED" or charge["posted"] or not event.get("evidence"):
                        raise GuardError("invalid posted charge reconciliation")
                    charge["posted"] = True
                else:
                    raise GuardError(f"unknown shared Flow event {kind!r}")
        except (ValueError, KeyError, TypeError) as exc:
            raise GuardError("unreadable shared Flow ledger; no Create permitted") from exc
        # Each unposted charge remains a liability even after its reservation is
        # released. Active reservations cover only their not-yet-used capacity.
        unposted = sum(c["amount"] for c in charges.values() if not c["posted"])
        remaining = sum(
            r["cap"] - sum(c["amount"] for c in charges.values() if c["reservation"] == key)
            for key, r in reservations.items() if r["active"])
        return dict(reservations=reservations, charges=charges,
                    liability=unposted + remaining,
                    pending=any(c["status"] == "PENDING" for c in charges.values()))

    def _event(self, event):
        self._assert_held()
        append_ledger(self.path, {**event, "at": now_iso()})
        # Persist the first directory entry as well as the file contents.
        directory = os.open(self.state, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)

    def reserve(self, key: str, film: str, cap: int, *, live: int, floor: int = HEADROOM_FLOOR):
        state = self.snapshot()
        self._amount(cap)
        self._amount(live)
        self._amount(floor)
        if not isinstance(key, str) or not key or not isinstance(film, str) or not film or cap <= 0:
            raise GuardError("reservation needs an identity, film and positive cap")
        existing = state["reservations"].get(key)
        if existing:
            if existing != dict(cap=cap, film=film, active=True):
                raise GuardError("reservation identity collision")
            return
        if state["pending"] or live - state["liability"] - cap < floor:
            raise GuardError("pending charge or insufficient shared Flow headroom")
        self._event(dict(kind="reserve", id=key, film=film, cap=cap))

    def intent(self, key: str, reservation: str, amount: int, *, live: int,
               floor: int = HEADROOM_FLOOR):
        state = self.snapshot()
        self._amount(amount)
        self._amount(live)
        self._amount(floor)
        if state["pending"] or live - state["liability"] < floor:
            raise GuardError("pending charge or insufficient shared Flow headroom")
        record = state["reservations"].get(reservation)
        if not isinstance(key, str) or not key or key in state["charges"] or not record or not record["active"]:
            raise GuardError("duplicate intent or inactive reservation")
        used = sum(c["amount"] for c in state["charges"].values() if c["reservation"] == reservation)
        if amount <= 0 or used + amount > record["cap"]:
            raise GuardError("charge exceeds reservation cap")
        self._event(dict(kind="intent", id=key, reservation=reservation, amount=amount))

    def resolve(self, key: str, *, submitted: bool, evidence: dict):
        charge = self.snapshot()["charges"].get(key)
        if type(submitted) is not bool or not charge or charge["status"] != "PENDING" or not evidence:
            raise GuardError("resolution needs a pending charge and evidence")
        self._event(dict(kind="charged" if submitted else "not_submitted", id=key, evidence=evidence))

    def reconcile_posted(self, key: str, *, evidence: dict):
        charge = self.snapshot()["charges"].get(key)
        if not charge or charge["status"] != "CHARGED" or charge["posted"] or not evidence:
            raise GuardError("posted reconciliation needs an unposted charge and evidence")
        self._event(dict(kind="posted", id=key, evidence=evidence))

    def export_ai_spend(self, target: Path, *, by: str) -> int:
        """Replay confirmed charges into the shared ai_spend schema, exactly once.

        The destination is explicit: never guess a checkout or commit from a
        generation process. The caller retains account ownership; an additional
        destination lock serializes exporters from different account stores.
        Unknown submissions stay pending, never fabricated as confirmed spend.
        Export does not reconcile billing or reduce any reserved liability.
        """
        self._assert_held()
        state = self.snapshot()
        if not isinstance(by, str) or not by.strip():
            raise GuardError("spend export needs a recorder identity")
        target = Path(target).resolve()
        if target == self.path.resolve():
            raise GuardError("spend destination aliases the account ledger")
        rows = []
        events = [json.loads(line) for line in self.path.read_text().splitlines()] if self.path.exists() else []
        for event in events:
            if event['kind'] != 'charged':
                continue
            key = event['id']
            charge = state['charges'][key]
            film = state['reservations'][charge['reservation']]['film']
            evidence = event['evidence']
            # Actual guarded Create evidence contains only the already-validated
            # balance needed by the report. Never export the account address.
            balances = evidence.get('ui', {}).get('balances', [])
            base = dict(at=event['at'], pool='flow', by=by,
                        source='shared-flow', charge=key)
            if balances:
                if len(balances) != 1 or type(balances[0]) is not int or balances[0] < 0:
                    raise GuardError("invalid confirmed charge balance evidence")
                rows.append(dict(base, id='flow:read:'+key, kind='record',
                                 left=balances[0], note='Configured UI before Create'))
            rows.append(dict(base, id='flow:spend:'+key, kind='spend',
                             amount=charge['amount'], film=film, what=key))
        target.parent.mkdir(parents=True, exist_ok=True)
        with WriterLock(target.with_name(target.name+'.lock')):
            data = target.read_bytes() if target.exists() else b''
            if data and not data.endswith(b'\n'):
                raise GuardError("torn ai_spend ledger; reconcile before export")
            try:
                existing = [json.loads(line) for line in data.splitlines()]
                if any(not isinstance(row, dict) for row in existing):
                    raise ValueError('non-object row')
            except (ValueError, TypeError) as exc:
                raise GuardError("unreadable ai_spend ledger") from exc
            indexed = {}
            for row in existing:
                if 'id' in row:
                    if row['id'] in indexed:
                        raise GuardError("duplicate ai_spend receipt identity")
                    indexed[row['id']] = row
            missing = []
            for row in rows:
                previous = indexed.get(row['id'])
                # A recovery worker may differ; preserve the first recorder.
                if previous is not None:
                    if {k:v for k,v in previous.items() if k != 'by'} != {k:v for k,v in row.items() if k != 'by'}:
                        raise GuardError("ai_spend receipt identity collision")
                else:
                    missing.append(row)
            if missing:
                with target.open('ab') as handle:
                    handle.write(b''.join((json.dumps(row, sort_keys=True)+'\n').encode() for row in missing))
                    handle.flush()
                    os.fsync(handle.fileno())
                directory = os.open(target.parent, os.O_RDONLY)
                try:
                    os.fsync(directory)
                finally:
                    os.close(directory)
            return len(missing)

    def release(self, key: str):
        state = self.snapshot()
        record = state["reservations"].get(key)
        if not record or not record["active"] or any(
                c["reservation"] == key and c["status"] == "PENDING" for c in state["charges"].values()):
            raise GuardError("cannot release inactive reservation or pending charge")
        self._event(dict(kind="release", id=key))


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


def runner_state_dir() -> Path:
    """Runner ownership is independent of the film checkout and worktree."""
    return Path.home() / "_desk/state/flow/hos009-tranche2"


def detached_command(script: Path, log_path: Path, done_path: Path, *,
                     repo: Path, media: Path, archive: Path, other: int,
                     ledger: Path, lock: Path, pid: Path,
                     session: str = "hos009-tranche2") -> list[str]:
    """Print-only launch recipe; never arms generation or overwrites logs."""
    paths = [script, repo, media, archive, ledger, lock, pid, log_path, done_path]
    if not all(path.is_absolute() for path in paths):
        raise GuardError("detached inputs and state paths must be absolute")
    if not script.is_file() or not repo.is_dir() or not media.is_dir() or not archive.is_dir():
        raise GuardError("detached script/repo/media/archive must already exist")
    if other < 0 or not re.fullmatch(r"[A-Za-z0-9_-]+", session):
        raise GuardError("invalid reservation or tmux session")
    resolved = [path.resolve() for path in (ledger, lock, pid, log_path, done_path)]
    if len(set(resolved)) != len(resolved):
        raise GuardError("detached state/log/done paths must be distinct")
    if log_path.exists() or done_path.exists():
        raise GuardError("use fresh per-run log and done paths; existing files are preserved")
    args = [sys.executable, str(script), "launch-worker", "--repo", str(repo),
            "--media", str(media), "--archive", str(archive),
            "--other-reservations", str(other), "--ledger", str(ledger),
            "--lock", str(lock), "--pid", str(pid), "--log", str(log_path),
            "--done", str(done_path)]
    return ["tmux", "new", "-d", "-s", session, shlex.join(args)]


def launch_once(command: list[str], *, ownership: Path, pid: Path,
                log: Path, done: Path) -> int:
    """Own the runner for the child's entire lifetime, including failures.

    flock is acquired before inspecting PID/done or starting a child. A stale
    .done file never bypasses ownership. SIGKILL leaves a live child's PID for
    the next owner to refuse; an unreadable PID fails closed.
    """
    with WriterLock(ownership):
        refuse_duplicate(pid, done)
        if done.exists():
            raise GuardError("done file already exists; use a fresh run id")
        log.parent.mkdir(parents=True, exist_ok=True)
        done.parent.mkdir(parents=True, exist_ok=True)
        # Exclusive open prevents two launch recipes sharing a log path.
        with log.open("xb") as handle:
            gate = ("import os,sys; token=os.read(0,1); "
                    "sys.exit(125) if token != b'1' else None; "
                    "os.execvp(sys.argv[1], sys.argv[1:])")
            child = subprocess.Popen([sys.executable, "-c", gate, *command],
                                     stdin=subprocess.PIPE, stdout=handle,
                                     stderr=subprocess.STDOUT)
            signalled = False
            try:
                claim_pid(pid, child.pid)
                child.stdin.write(b"1")
                child.stdin.close()
                signalled = True
                code = child.wait()
            except BaseException:
                if child.stdin and not child.stdin.closed:
                    child.stdin.close()  # unsignalled child exits without executing
                if not signalled:
                    child.wait(timeout=5)
                # Preserve child pid and ownership evidence on interrupted waits.
                raise
        immutable_bytes(done, (str(code) + "\n").encode())
        return code


def claim_pid(pid_path: Path, pid: int | None = None) -> None:
    pid_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = pid_path.with_name(pid_path.name + f".{os.getpid()}.tmp")
    immutable_bytes(temporary, (str(os.getpid() if pid is None else pid) + "\n").encode())
    os.replace(temporary, pid_path)


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
                        len(videos) == 1 and audio == 0 and duration >= required_s - 0.09 and
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


def canonical_spend_ledger() -> Path:
    """The installed OWB report source, independent of cwd and repo overrides."""
    return Path.home() / "YouTube/orbit-with-ben/05_Analytics/ai_spend/ledger.jsonl"


def production_batch_paths(*, accounting_state: Path | None,
                           spend_ledger: Path | None,
                           inventory_rows: list[Row] | None) -> tuple[Path, Path]:
    """Reject per-worktree accounting and incomplete inventory before side effects.

    This only supplies mandatory production inputs. It does not enable submit or
    establish adoption of the protocol by other writers / the report CLI.
    """
    state = shared_flow_state_dir()
    target = canonical_spend_ledger()
    if accounting_state is not None and Path(accounting_state).resolve() != state.resolve():
        raise GuardError("production requires canonical shared Flow accounting")
    if spend_ledger is not None and Path(spend_ledger).resolve() != target.resolve():
        raise GuardError("production requires canonical OWB spend report")
    if inventory_rows is None:
        raise GuardError("production requires the full locked inventory scope")
    # Compare the exact scope, including duplicate/missing rows. load_scope also
    # validates board hashes and accepted trims; no caller can invent a subset.
    locked = load_scope(repo_root_from())
    if sorted(inventory_rows, key=lambda row: row.key) != sorted(locked, key=lambda row: row.key):
        raise GuardError("production inventory differs from the full locked scope")
    return state, target


def next_still_evidence_path(archive_dir: Path, still_filename: str) -> Path:
    """Return an unused immutable still Create evidence path in archive_dir."""
    first = archive_dir / f"{still_filename}.still.create.json"
    if not first.exists():
        return first
    attempt = 2
    while True:
        candidate = archive_dir / f"{still_filename}.still.attempt{attempt}.create.json"
        if not candidate.exists():
            return candidate
        attempt += 1


def execute_shared_batch(batch: list[Row], *, media: Path, ledger_path: Path,
                         archive_dir: Path, accounting_state: Path | None = None,
                         spend_ledger: Path | None = None, recorder: str = "codex",
                         reservation: str = "J2033", other: int = 0, submitter=None,
                         still_maker=None,
                         in_scope_keys: set[tuple[int, str]] | None = None,
                         test_archive: bool = False,
                         inventory_rows: list[Row] | None = None) -> list[dict]:
    """Production accounting integration; no caller-supplied balance/price.

    Each actual configured Create obtains its own UI evidence and durable shared
    charge through live_video_submit. The shared lock covers preparation, Create,
    download, archive and receipts. This remains behind cmd_submit's interlock.
    """
    if type(other) is not int or other < 0:
        raise GuardError("invalid other reservations")
    assert_batch_limits(batch)
    if not test_archive:
        accounting_state, spend_ledger = production_batch_paths(
            accounting_state=accounting_state, spend_ledger=spend_ledger,
            inventory_rows=inventory_rows)
        if any(row not in inventory_rows for row in batch):
            raise GuardError("batch contains a row outside the locked inventory scope")
    archive_dir = require_archive(archive_dir, nas=not test_archive)
    submitter = submitter or live_video_submit
    accepts_other = "other" in inspect.signature(submitter).parameters
    written = []
    with SharedFlowAccounting(accounting_state) as accounting:
        # Replay known charges before refusing recovery on a local output hold.
        if spend_ledger is not None:
            accounting.export_ai_spend(spend_ledger, by=recorder)
        if accounting.snapshot()['pending']:
            raise GuardError('unresolved shared Create; no batch or retry')
        scope_rows = inventory_rows if inventory_rows is not None else batch
        if still_maker is not None:
            for srow in scope_rows:
                if srow.parent is not None:
                    continue
                spath = still_path(media, srow.part, srow.plate_id)
                if not spath.is_file():
                    made = Path(still_maker(
                        srow, spath, accounting=accounting, reservation=reservation,
                        evidence_path=next_still_evidence_path(archive_dir, spath.name),
                        other=other,
                    ))
                    if not made.is_file():
                        raise GuardError(f"zero-price still for {srow.plate_id} was not written")
                    archive_verified(made, archive_dir / made.name)
        # Check the whole supplied scope before any charge, including later rows.
        # Archive the inventory before browser entry; a missing later asset must
        # never spend the first row's credits.
        inventory = verify_still_inventory(scope_rows, media)
        inventory_bytes = json.dumps(inventory, sort_keys=True).encode()
        inventory_id = hashlib.sha256(inventory_bytes).hexdigest()
        immutable_bytes(archive_dir / ("inventory-" + inventory_id + ".json"), inventory_bytes)
        inventory_by_key = {(item["part"], item["plate_id"]): item for item in inventory}
        entries = read_ledger(ledger_path)
        if any(e.get('status') == 'SUBMITTING' for e in latest_entries(entries)):
            raise GuardError('unresolved local output; reconcile before batch')
        _, _, _, takes = ledger_totals(entries)
        for row in batch:
            if takes.get(row.plate_id, 0) >= MAX_TAKES_PER_ROW:
                raise GuardError(f'{row.plate_id}: take cap reached')
            frame = prepare_start_frame(row, media, in_scope_keys=in_scope_keys or set(),
                                        still_price=None, still_maker=None, ledger=entries)
            expected = inventory_by_key.get(row.key)
            if row.parent is None and (expected is None or
                    Path(expected["path"]) != frame.resolve() or
                    sha256_file(frame) != expected["sha256"]):
                raise GuardError("start still changed after inventory; no Create")
            take, dest = next_version(media, row.part, row.plate_id)
            dest.parent.mkdir(parents=True, exist_ok=True)
            charge = f'HOS:009:P{row.part:02d}:{row.plate_id}:t{take}'
            # Persist local intent before entering the browser; failures cannot
            # silently skip a take or erase an unknown submission.
            intent = submitting_record(row.plate_id, row.part, take, dest)
            intent['shared_charge'] = charge
            intent['inventory'] = inventory_id
            intent['input'] = {'file': str(frame.resolve()), 'sha256': sha256_file(frame)}
            append_ledger(ledger_path, intent)
            submit_kwargs = dict(
                accounting=accounting,
                reservation=reservation,
                charge=charge,
                evidence_path=archive_dir / (dest.name + '.create.json'),
            )
            if accepts_other:
                submit_kwargs['other'] = other
            try:
                evidence = submitter(row, dest, frame, **submit_kwargs)
            finally:
                # A known click may have charged even when download raised.
                # Ambiguous PENDING intents remain absent from confirmed spend.
                if spend_ledger is not None:
                    accounting.export_ai_spend(spend_ledger, by=recorder)
            shared = accounting.snapshot()['charges'].get(charge)
            if not shared or shared['status'] != 'CHARGED' or shared['amount'] != MAX_CREDITS_PER_TAKE:
                raise GuardError('submitter returned without exact shared charge; no advancement')
            if not isinstance(evidence, dict) or evidence.get('charge') != charge:
                raise GuardError('submitter returned without per-Create evidence')
            if not dest.is_file():
                raise GuardError('charged output missing; reconcile before retry')
            strip_audio(dest)
            technical = technical_report(dest, required_s=max(8.0, row.use_s))
            entry = review_record(row.plate_id, row.part, take, dest, technical)
            entry.update(shared_charge=charge, create_evidence=evidence,
                         inventory=inventory_id, input=intent["input"],
                         archive=archive_verified(dest, archive_dir/dest.name))
            if not technical['ok']:
                entry['status'] = 'FAILED'
            write_receipt(archive_dir/(dest.name+'.receipt.json'),[row.plate_id],[entry])
            append_ledger(ledger_path, entry)
            entries.append(entry)
            written.append(entry)
            takes[row.plate_id] = takes.get(row.plate_id, 0) + 1
            if not technical['ok']:
                raise GuardError('technical output failed; no batch advancement')
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


def live_video_submit(row: Row, dest: Path, frame: Path, *,
                      accounting: SharedFlowAccounting, reservation: str,
                      charge: str, evidence_path: Path, other: int = 0) -> dict:
    """Real Flow call. Unreachable unless submit was armed. Tests never call this."""
    if os.environ.get(SUBMIT_ENV) != "1":
        raise GuardError("live submit is not armed")
    if type(other) is not int or other < 0:
        raise GuardError("invalid other reservations")
    accounting._assert_held()
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
    floor = HEADROOM_FLOOR + other
    with sync_playwright() as playwright:
        browser = playwright.chromium.connect_over_cdp(cdp)
        page = open_flow_page(
            browser,
            flow.FLOW_HOME,
            lambda current, url: current.goto(url, wait_until="domcontentloaded", timeout=120_000),
        )
        evidence = {}
        def create_guard(configured_page):
            # Read the balance in its own step before model and aspect, since
            # Account details and Settings overlays cannot be open together,
            # and carry the value to the submit guard.
            live_balance = read_live_balance(configured_page)
            ui = read_live_evidence(configured_page, balance=live_balance, open_overlay=True)
            accounting.reserve(reservation, 'HOS:009', MAX_TOTAL_CREDITS, live=ui['balances'][0], floor=floor)
            evidence.update(guarded_create(
                configured_page, accounting, reservation=reservation, charge=charge,
                evidence_path=evidence_path, floor=floor, balance=live_balance))
        flow.generate_clip(
            page, prompt, dest, model=model, timeout_s=700,
            start_frame=frame, attempts=1, reuse_project=False, create_guard=create_guard,
        )

    return evidence


def cmd_plan(repo: Path, out: Path | None) -> dict:
    plan = build_plan(load_scope(repo), repo=repo)
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
               pid_path: Path, done_path: Path, archive_dir: Path | None,
               accounting_state: Path | None = None, spend_ledger: Path | None = None,
               recorder: str = "codex", submitter=None, still_maker=None,
               test_archive: bool = False) -> list[dict]:
    """Run one guarded tranche-2 batch when explicitly armed."""
    if not submit_armed():
        raise SystemExit(
            "refusing submit: generation is not armed "
            f"({SUBMIT_ENV} is not 1). Plan only. J2033 stays blocked until Chief passes this runner."
        )
    refuse_duplicate(pid_path, done_path)
    with WriterLock(lock_path):
        claim_pid(pid_path)
        rows = load_scope(repo)
        entries = read_ledger(ledger_path)
        batch = next_batch(rows, entries)
        if not batch:
            return []
        return execute_shared_batch(
            batch,
            media=media,
            ledger_path=ledger_path,
            archive_dir=archive_dir,
            accounting_state=accounting_state,
            spend_ledger=spend_ledger,
            recorder=recorder,
            reservation="J2033",
            other=other,
            submitter=submitter,
            still_maker=still_maker or live_still_maker,
            in_scope_keys={r.key for r in rows},
            test_archive=test_archive,
            inventory_rows=rows,
        )


BALANCE_EVIDENCE_JS = r"""(expected) => {
  const visible = e => { const r = e.getBoundingClientRect();
    const s = getComputedStyle(e);
    return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none'; };
  const unique = a => [...new Set(a)];
  const body = document.body.innerText;
  const accounts = unique([...document.querySelectorAll('[aria-label]')].filter(visible)
    .map(e => e.getAttribute('aria-label')).filter(t => /Google Account|Account details/i.test(t))
    .flatMap(t => t.match(/[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}/ig) || [])
    .map(t => t.toLowerCase()));
  const balances = unique([...body.matchAll(/(?:^|\n)\s*([\d,]+)\s+(?:AI|Google Flow) credits\s*(?=\n|$)/g)]
    .map(m => Number(m[1].replace(/,/g, ''))));
  return {
    host: location.hostname,
    accounts,
    balances,
    ultra: body.split('\n').some(t => t.trim() === 'ULTRA')
  };
}"""


def _close_flow_overlays(page) -> None:
    try:
        page.evaluate(
            "() => { for (const b of document.querySelectorAll('.cdk-overlay-backdrop')) b.click(); }",
            None,
        )
    except Exception:
        pass
    try:
        page.keyboard.press("Escape")
    except Exception:
        pass
    try:
        page.wait_for_timeout(300)
    except Exception:
        pass


def read_live_balance(page, *, open_overlay: bool = True) -> int:
    """Read and validate the Flow credit balance in its own step before model and aspect.

    Account details and Settings trigger overlays are mutually exclusive on Flow;
    when Account details is opened here, it is closed before returning.
    """
    evidence = page.evaluate(BALANCE_EVIDENCE_JS, None)
    opened = False
    if open_overlay and isinstance(evidence, dict) and not evidence.get("balances"):
        try:
            clicked = page.evaluate(
                """() => {
                  const e = document.querySelector('[aria-label="Account details"], [aria-label*="Account details" i], [aria-label*="Google Account" i]');
                  if (e) { e.click(); return true; }
                  return false;
                }""",
                None,
            )
        except Exception:
            clicked = False
        if clicked:
            opened = True
            try:
                page.wait_for_timeout(600)
            except Exception:
                pass
            evidence = page.evaluate(BALANCE_EVIDENCE_JS, None)
    try:
        required = dict(host=FLOW_HOST, accounts=[REQUIRED_ACCOUNT], ultra=True)
        if not isinstance(evidence, dict) or any(evidence.get(k) != v for k, v in required.items()):
            raise GuardError('live Flow selected controls/account/entitlement/price are missing or changed')
        balances = evidence.get('balances')
        if not isinstance(balances, list) or len(balances) != 1 or type(balances[0]) is not int or balances[0] < 0:
            raise GuardError('live Flow balance is missing or ambiguous')
        allowed_keys = set(required) | {'balances'}
        extra_keys = set(evidence) - allowed_keys
        if extra_keys and extra_keys not in (
            {'models', 'outputs', 'aspects', 'durations', 'prices', 'create_count'},
            {'models', 'outputs', 'aspects', 'prices', 'create_count'},
        ):
            raise GuardError('unknown live Flow balance evidence schema')
        return balances[0]
    finally:
        if opened:
            _close_flow_overlays(page)


def _open_settings_trigger_if_needed(page) -> bool:
    try:
        clicked = page.evaluate(
            """() => {
              if (document.querySelector('button[aria-label="Select model family"]')) return false;
              const e = document.querySelector('button[aria-label="Settings trigger"]');
              if (e) { e.click(); return true; }
              return false;
            }""",
            None,
        )
    except Exception:
        return False
    if clicked:
        try:
            page.wait_for_timeout(600)
        except Exception:
            pass
    return bool(clicked)


# One synchronous DOM turn rechecks the evidence and resolves the exact center
# of the unique enabled unobstructed Create control for a trusted CDP mouse
# click. Never call element.click() here: Flow's FLOW-BASE-PROMPT-BOX.submit(a)
# drops untrusted synthetic DOM clicks (a.isTrusted === false).
CREATE_EVIDENCE_JS = r"""(expected) => {
  const visible = e => { const r = e.getBoundingClientRect();
    const s = getComputedStyle(e);
    return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none'; };
  const text = e => (e.innerText || e.getAttribute('aria-label') || '').trim().replace(/\s+/g, ' ');
  const unique = a => [...new Set(a)];
  const selected = [...document.querySelectorAll(
    '[aria-selected="true"],[aria-checked="true"],[aria-pressed="true"],select option:checked')]
    .filter(visible).map(text);
  const allButtons = [...document.querySelectorAll('button')].filter(visible);
  const modelButtons = allButtons
    .filter(e => e.getAttribute('aria-label') === 'Select model family' &&
      !e.disabled && e.getAttribute('aria-disabled') !== 'true')
    .map(e => (e.innerText || '').trim().replace(/\s+/g, ' ').replace(/\s+arrow_drop_down$/, ''));
  const knownVideoModels = new Set(['Veo 3.1 - Quality', 'Veo 3.1 - Fast', 'Veo 3.1 - Lite']);
  const models = modelButtons.some(t => !knownVideoModels.has(t))
    ? []
    : unique([...selected.filter(t => knownVideoModels.has(t)), ...modelButtons]);
  const aspectMap = {
    '16:9': '16:9', 'crop_16_9 16:9': '16:9',
    '9:16': '9:16', 'crop_9_16 9:16': '9:16',
    '4:3': '4:3', 'crop_landscape 4:3': '4:3',
    '1:1': '1:1', 'crop_square 1:1': '1:1',
    '3:4': '3:4', 'crop_portrait 3:4': '3:4'
  };
  const body = document.body.innerText;
  const accounts = unique([...document.querySelectorAll('[aria-label]')].filter(visible)
    .map(e => e.getAttribute('aria-label')).filter(t => /Google Account|Account details/i.test(t))
    .flatMap(t => t.match(/[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}/ig) || [])
    .map(t => t.toLowerCase()));
  const prices = unique(body.split('\n').map(t => t.trim())
    .filter(t => /^Generating will use \d+ credits$/.test(t)));
  const balances = unique([...body.matchAll(/(?:^|\n)\s*([\d,]+)\s+(?:AI|Google Flow) credits\s*(?=\n|$)/g)]
    .map(m => Number(m[1].replace(/,/g, ''))));
  const buttons = allButtons.filter(e => {
    const t = text(e); return (t === 'Create' || t === 'Start generation' || t === 'arrow_forward') &&
      !e.disabled && e.getAttribute('aria-disabled') !== 'true'; });
  const evidence = {
    host: location.hostname,
    models,
    outputs: unique(selected.filter(t => /^x[1234]$/.test(t))),
    aspects: unique(selected.map(t => aspectMap[t]).filter(Boolean)),
    durations: unique(selected.filter(t => /^\d+s$/.test(t))),
    accounts, prices, balances,
    ultra: body.split('\n').some(t => t.trim() === 'ULTRA'),
    create_count: buttons.length
  };
  if (expected === null) return evidence;
  if (JSON.stringify(evidence) !== JSON.stringify(expected))
    return {ready: false, reason: 'live UI changed', evidence};
  if (buttons.length !== 1) return {ready: false, reason: 'Create not unique', evidence};
  const rect = buttons[0].getBoundingClientRect();
  if (!Number.isFinite(rect.left) || !Number.isFinite(rect.top) || !(rect.width > 0 && rect.height > 0))
    return {ready: false, reason: 'Create geometry invalid', evidence};
  const cx = rect.left + rect.width / 2;
  const cy = rect.top + rect.height / 2;
  if (typeof innerWidth === 'number' && typeof innerHeight === 'number' &&
      (cx < 0 || cy < 0 || cx > innerWidth || cy > innerHeight))
    return {ready: false, reason: 'Create outside viewport', evidence};
  if (typeof document.elementFromPoint === 'function') {
    const hit = document.elementFromPoint(cx, cy);
    if (!hit || (hit !== buttons[0] && !(typeof buttons[0].contains === 'function' && buttons[0].contains(hit))))
      return {ready: false, reason: 'Create obstructed', evidence};
  }
  return {ready: true, target: {x: cx, y: cy}, evidence};
}"""


def _resolve_evidence_balances(raw: dict, balance: int | None) -> list[int]:
    balances = raw.get('balances')
    if not isinstance(balances, list):
        raise GuardError('live Flow balance is missing or ambiguous')
    if len(balances) == 0 and balance is not None:
        if type(balance) is not int or balance < 0:
            raise GuardError('live Flow balance is missing or ambiguous')
        return [balance]
    if len(balances) == 1 and type(balances[0]) is int and balances[0] >= 0:
        if balance is not None and (type(balance) is not int or balances[0] != balance):
            raise GuardError('live Flow balance is missing or ambiguous')
        return list(balances)
    raise GuardError('live Flow balance is missing or ambiguous')


def _read_and_validate_live_evidence(page, *, balance: int | None = None,
                                     open_overlay: bool = False) -> tuple[dict, dict]:
    raw = page.evaluate(CREATE_EVIDENCE_JS, None)
    if (
        open_overlay
        and isinstance(raw, dict)
        and not raw.get('models')
        and not raw.get('prices')
        and _open_settings_trigger_if_needed(page)
    ):
        raw = page.evaluate(CREATE_EVIDENCE_JS, None)
    required = dict(host=FLOW_HOST, models=[REQUIRED_MODEL], outputs=[REQUIRED_OUTPUTS],
                    aspects=['16:9'], durations=['8s'], accounts=[REQUIRED_ACCOUNT],
                    prices=[f'Generating will use {MAX_CREDITS_PER_TAKE} credits'],
                    ultra=True, create_count=1)
    if not isinstance(raw, dict) or any(raw.get(k) != v for k, v in required.items()):
        raise GuardError('live Flow selected controls/account/entitlement/price are missing or changed')
    # Reject extra fields so the atomic comparison has one exact schema.
    if set(raw) != set(required) | {'balances'}:
        raise GuardError('unknown live Flow evidence schema')
    balances = _resolve_evidence_balances(raw, balance)
    return raw, dict(raw, balances=balances)


def read_live_evidence(page, *, balance: int | None = None, open_overlay: bool = False) -> dict:
    """Strict selected-state DOM evidence, never environment or menu-option text.

    Unknown UI layouts fail closed. Deployment still needs a reviewed live DOM
    fixture; this reader must not be loosened by guessing at a missing field.
    """
    _raw, evidence = _read_and_validate_live_evidence(page, balance=balance, open_overlay=open_overlay)
    return evidence


def _extract_trusted_click_target(target: object) -> tuple[float, float] | None:
    if not isinstance(target, dict):
        return None
    x, y = target.get('x'), target.get('y')
    if (
        isinstance(x, bool)
        or isinstance(y, bool)
        or not isinstance(x, (int, float))
        or not isinstance(y, (int, float))
        or not math.isfinite(x)
        or not math.isfinite(y)
    ):
        return None
    return float(x), float(y)


def guarded_create(page, accounting: SharedFlowAccounting, *, reservation: str,
                   charge: str, evidence_path: Path, floor: int = HEADROOM_FLOOR,
                   balance: int | None = None) -> dict:
    """Real browser adapter; caller owns shared writer lock through persistence.

    The intent is durable before the trusted CDP mouse click. Any ambiguous
    browser failure around the click leaves it pending, blocking both channels
    until explicit reconciliation. No retry.
    """
    accounting._assert_held()
    raw, evidence = _read_and_validate_live_evidence(page, balance=balance)
    record = dict(read_at=now_iso(), ui=evidence, charge=charge, reservation=reservation)
    immutable_bytes(evidence_path, (json.dumps(record, sort_keys=True) + '\n').encode())
    accounting.intent(charge, reservation, MAX_CREDITS_PER_TAKE, live=evidence['balances'][0], floor=floor)
    outcome = page.evaluate(CREATE_EVIDENCE_JS, raw)
    if not isinstance(outcome, dict) or type(outcome.get('ready')) is not bool:
        raise GuardError('ambiguous Create precheck outcome; shared charge remains pending')
    if not outcome['ready']:
        accounting.resolve(charge, submitted=False,
                           evidence=dict(reason=outcome.get('reason'), read_at=record['read_at']))
        raise GuardError('live UI drift before Create; no submission')
    coords = _extract_trusted_click_target(outcome.get('target'))
    mouse = getattr(page, 'mouse', None)
    if coords is None or mouse is None or not callable(getattr(mouse, 'click', None)):
        accounting.resolve(charge, submitted=False,
                           evidence=dict(reason='missing trusted click target or mouse adapter',
                                         read_at=record['read_at']))
        raise GuardError('missing trusted Create click target or mouse adapter; no submission')
    mouse.click(coords[0], coords[1])
    accounting.resolve(charge, submitted=True,
                       evidence=dict(ui=evidence, target=dict(x=coords[0], y=coords[1]),
                                     read_at=record['read_at']))
    return record


def _load_mint006(repo: Path):
    import importlib.util
    path = repo / "02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project/_mint_flow_cdp_v01.py"
    spec = importlib.util.spec_from_file_location("hos006_mint_tranche2", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


STILL_EVIDENCE_JS = r"""(expected) => {
  const visible = e => { const r = e.getBoundingClientRect();
    const s = getComputedStyle(e);
    return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none'; };
  const text = e => (e.innerText || e.getAttribute('aria-label') || '').trim().replace(/\s+/g, ' ');
  const unique = a => [...new Set(a)];
  const selected = [...document.querySelectorAll(
    '[aria-selected="true"],[aria-checked="true"],[aria-pressed="true"],select option:checked')]
    .filter(visible).map(text);
  const allButtons = [...document.querySelectorAll('button')].filter(visible);
  const modelButtons = allButtons
    .filter(e => e.getAttribute('aria-label') === 'Select model family' &&
      !e.disabled && e.getAttribute('aria-disabled') !== 'true')
    .map(e => (e.innerText || '').trim().replace(/\s+/g, ' ')
      .replace(/\s+arrow_drop_down$/, '').replace(/^🍌\s+/, ''));
  const knownStillModels = new Set(['Nano Banana 2', 'Nano Banana 2.1']);
  const models = modelButtons.some(t => !knownStillModels.has(t))
    ? []
    : unique([...selected.map(t => t.replace(/^🍌\s+/, '')).filter(t => knownStillModels.has(t)), ...modelButtons]);
  const aspectMap = {
    '16:9': '16:9', 'crop_16_9 16:9': '16:9',
    '9:16': '9:16', 'crop_9_16 9:16': '9:16',
    '4:3': '4:3', 'crop_landscape 4:3': '4:3',
    '1:1': '1:1', 'crop_square 1:1': '1:1',
    '3:4': '3:4', 'crop_portrait 3:4': '3:4'
  };
  const body = document.body.innerText;
  const accounts = unique([...document.querySelectorAll('[aria-label]')].filter(visible)
    .map(e => e.getAttribute('aria-label')).filter(t => /Google Account|Account details/i.test(t))
    .flatMap(t => t.match(/[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}/ig) || [])
    .map(t => t.toLowerCase()));
  const prices = unique(body.split('\n').map(t => t.trim())
    .filter(t => /^Generating will use \d+ credits$/.test(t)));
  const balances = unique([...body.matchAll(/(?:^|\n)\s*([\d,]+)\s+(?:AI|Google Flow) credits\s*(?=\n|$)/g)]
    .map(m => Number(m[1].replace(/,/g, ''))));
  const buttons = allButtons.filter(e => {
    const t = text(e); return (t === 'Create' || t === 'Start generation' || t === 'arrow_forward') &&
      !e.disabled && e.getAttribute('aria-disabled') !== 'true'; });
  const evidence = {
    host: location.hostname,
    models,
    outputs: unique(selected.filter(t => /^x[1234]$/.test(t))),
    aspects: unique(selected.map(t => aspectMap[t]).filter(Boolean)),
    accounts, prices, balances,
    ultra: body.split('\n').some(t => t.trim() === 'ULTRA'),
    create_count: buttons.length
  };
  if (expected === null) return evidence;
  if (JSON.stringify(evidence) !== JSON.stringify(expected))
    return {ready: false, reason: 'live UI changed', evidence};
  if (buttons.length !== 1) return {ready: false, reason: 'Create not unique', evidence};
  const rect = buttons[0].getBoundingClientRect();
  if (!Number.isFinite(rect.left) || !Number.isFinite(rect.top) || !(rect.width > 0 && rect.height > 0))
    return {ready: false, reason: 'Create geometry invalid', evidence};
  const cx = rect.left + rect.width / 2;
  const cy = rect.top + rect.height / 2;
  if (typeof innerWidth === 'number' && typeof innerHeight === 'number' &&
      (cx < 0 || cy < 0 || cx > innerWidth || cy > innerHeight))
    return {ready: false, reason: 'Create outside viewport', evidence};
  if (typeof document.elementFromPoint === 'function') {
    const hit = document.elementFromPoint(cx, cy);
    if (!hit || (hit !== buttons[0] && !(typeof buttons[0].contains === 'function' && buttons[0].contains(hit))))
      return {ready: false, reason: 'Create obstructed', evidence};
  }
  return {ready: true, target: {x: cx, y: cy}, evidence};
}"""


def _read_and_validate_live_still_evidence(page, *, balance: int | None = None,
                                           open_overlay: bool = False) -> tuple[dict, dict]:
    raw = page.evaluate(STILL_EVIDENCE_JS, None)
    if (
        open_overlay
        and isinstance(raw, dict)
        and not raw.get('models')
        and not raw.get('prices')
        and _open_settings_trigger_if_needed(page)
    ):
        raw = page.evaluate(STILL_EVIDENCE_JS, None)
    required = dict(host=FLOW_HOST, models=[REQUIRED_STILL_MODEL], outputs=[REQUIRED_OUTPUTS],
                    aspects=['16:9'], accounts=[REQUIRED_ACCOUNT],
                    prices=['Generating will use 0 credits'],
                    ultra=True, create_count=1)
    if not isinstance(raw, dict) or any(raw.get(k) != v for k, v in required.items()):
        raise GuardError('live Flow still selected controls/account/entitlement/zero-price are missing or changed')
    if set(raw) != set(required) | {'balances'}:
        raise GuardError('unknown live Flow still evidence schema')
    balances = _resolve_evidence_balances(raw, balance)
    return raw, dict(raw, balances=balances)


def read_live_still_evidence(page, *, balance: int | None = None, open_overlay: bool = False) -> dict:
    """Strict selected-state DOM evidence for 0-credit 16:9 start stills on the one approved still model."""
    _raw, evidence = _read_and_validate_live_still_evidence(page, balance=balance, open_overlay=open_overlay)
    return evidence


def guarded_still_create(page, accounting: SharedFlowAccounting, *, reservation: str,
                         plate_id: str, evidence_path: Path, floor: int = HEADROOM_FLOOR,
                         balance: int | None = None) -> dict:
    """Zero-price still adapter for the one approved still model; caller owns shared writer lock."""
    accounting._assert_held()
    state = accounting.snapshot()
    raw, evidence = _read_and_validate_live_still_evidence(page, balance=balance)
    if state['pending'] or evidence['balances'][0] - state['liability'] < floor:
        raise GuardError('pending charge or insufficient shared Flow headroom for still')
    record = dict(read_at=now_iso(), ui=evidence, plate_id=plate_id, reservation=reservation, credits=0)
    immutable_bytes(evidence_path, (json.dumps(record, sort_keys=True) + '\n').encode())
    outcome = page.evaluate(STILL_EVIDENCE_JS, raw)
    if not isinstance(outcome, dict) or type(outcome.get('ready')) is not bool:
        raise GuardError('ambiguous still Create precheck outcome; stopping before video generation')
    if not outcome['ready']:
        raise GuardError('live UI drift before still Create; no submission')
    coords = _extract_trusted_click_target(outcome.get('target'))
    mouse = getattr(page, 'mouse', None)
    if coords is None or mouse is None or not callable(getattr(mouse, 'click', None)):
        raise GuardError('missing trusted still Create click target or mouse adapter; no submission')
    mouse.click(coords[0], coords[1])
    return record


def live_still_maker(row: Row, dest: Path, *, accounting: SharedFlowAccounting | None = None,
                     reservation: str = "J2033", evidence_path: Path | None = None,
                     other: int = 0) -> Path:
    """Zero-credit stills only, guarded under SharedFlowAccounting with verified 0 on screen."""
    if os.environ.get(SUBMIT_ENV) != "1":
        raise GuardError(
            f"no start still for {row.plate_id}. A Nano Banana still needs a verified on-screen price of 0 "
            "and a separate still call; stopping rather than guessing."
        )
    if type(other) is not int or other < 0:
        raise GuardError("invalid other reservations")
    if accounting is None or evidence_path is None:
        raise GuardError(
            f"no start still for {row.plate_id}. A Nano Banana still needs shared Flow accounting, "
            "a verified on-screen price of 0 and an evidence path; stopping rather than guessing."
        )
    accounting._assert_held()
    repo = repo_root_from()
    sys.path.insert(0, str(repo / "04_Audio/tools"))
    sys.path.insert(0, str(repo / "02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project"))
    import orbit_flow_veo_ui as flow
    import _flow_still_v01 as still_tool
    from playwright.sync_api import sync_playwright

    cdp = os.environ.get("ORBIT_FLOW_CDP", "http://127.0.0.1:9222")
    floor = HEADROOM_FLOOR + other
    plan_path = repo / EDIT_REL / PLAN_NAME
    media_root = still_tool.infer_media_root(dest)
    prompt = still_tool.still_prompt(
        "History of Science locked look: premium Animistry-class 3D cartoon, finished materials, warm cinematic period light.",
        " ".join(row.prompt.split()) + " Opening frame only. No readable words, numbers, letters or text anywhere.",
    )
    with sync_playwright() as playwright:
        browser = playwright.chromium.connect_over_cdp(cdp)
        page = open_flow_page(
            browser,
            flow.FLOW_HOME,
            lambda current, url: current.goto(url, wait_until="domcontentloaded", timeout=120_000),
        )
        evidence = {}
        def create_guard(configured_page):
            live_balance = read_live_balance(configured_page)
            ui = read_live_still_evidence(configured_page, balance=live_balance, open_overlay=True)
            accounting.reserve(reservation, "HOS:009", MAX_TOTAL_CREDITS, live=ui["balances"][0], floor=floor)
            evidence.update(guarded_still_create(
                configured_page, accounting, reservation=reservation,
                plate_id=row.plate_id, evidence_path=evidence_path, floor=floor,
                balance=live_balance))
        still_tool.make_still(
            page, prompt, dest, timeout_s=300, create_guard=create_guard,
            plan_path=plan_path, media_root=media_root,
        )
        after_balance = read_live_balance(page)
        if after_balance < evidence["ui"]["balances"][0]:
            raise GuardError("zero-price still reduced Flow balance")
    if not dest.is_file():
        raise GuardError(f"zero-price still for {row.plate_id} was not written")
    immutable_bytes(dest.with_suffix(".sha256"), (sha256_file(dest) + "\n").encode())
    return dest


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
    state = runner_state_dir()
    for name, help_text in (("detach-command", "print a tmux command; start nothing"),
                            ("launch-worker", "exclusive detached process owner")):
        launch = sub.add_parser(name, help=help_text)
        launch.add_argument("--repo", required=True)
        launch.add_argument("--media", required=True)
        launch.add_argument("--archive", required=True)
        launch.add_argument("--other-reservations", type=int, required=True)
        launch.add_argument("--ledger", default=str(state / "ledger.jsonl"))
        launch.add_argument("--lock", default=str(state / "writer.lock"))
        launch.add_argument("--pid", default=str(state / "runner.pid"))
        launch.add_argument("--log", required=True)
        launch.add_argument("--done", required=True)
    args = parser.parse_args(argv)
    if args.cmd == "plan":
        repo = Path(args.repo) if args.repo else repo_root_from()
        cmd_plan(repo, Path(args.out) if args.out else None)
        return 0
    if args.cmd in ("detach-command", "launch-worker"):
        # Validation is shared by the printer and the detached entry point.
        command = detached_command(
            Path(__file__).resolve(), Path(args.log), Path(args.done),
            repo=Path(args.repo), media=Path(args.media), archive=Path(args.archive),
            other=args.other_reservations, ledger=Path(args.ledger),
            lock=Path(args.lock), pid=Path(args.pid))
        load_scope(Path(args.repo))
        if args.cmd == "detach-command":
            sys.stdout.write(json.dumps(command) + "\n")
            return 0
        # PID evidence must also be canonical for recovery after an owner crash.
        if Path(args.pid).resolve() != (state / "runner.pid").resolve():
            raise GuardError("launch-worker requires the canonical runner pid path")
        # The canonical ownership lock cannot be overridden by another worktree.
        child_args = shlex.split(command[-1])
        child_args[2] = "submit"
        log_index = child_args.index("--log")
        del child_args[log_index:log_index + 2]
        return launch_once(child_args, ownership=state / "runner.lock",
                           pid=Path(args.pid), log=Path(args.log), done=Path(args.done))
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
        ledger_path=Path(args.ledger) if args.ledger else runner_state_dir() / "ledger.jsonl",
        lock_path=Path(args.lock) if args.lock else runner_state_dir() / "writer.lock",
        pid_path=Path(args.pid) if args.pid else runner_state_dir() / "runner.pid",
        done_path=Path(args.done) if args.done else runner_state_dir() / "runner.done",
        archive_dir=Path(args.archive) if args.archive else None,
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except GuardError as exc:
        print(f"STOP {exc}", file=sys.stderr)
        raise SystemExit(2)
