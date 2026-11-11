#!/usr/bin/env python3
"""HOS 013 Darwin & Wallace pass-1 Flow mint runner (J2499).

Built on the J2200 shared Flow accounting guards and the repaired HOS 009
tranche-2 runner (history-of-science #445, #468, #470, #477). Never marks any
take KEEP; every output is saved as file_state=GENERATED, status=PENDING_REVIEW.

Default commands (`plan`, `dry-run`) never open Chrome/CDP, never click Create,
and spend 0 credits (£0). `submit` is refused unless HOS013_PASS1_SUBMIT=1 after
the Chief reviews the runner against the live Flow panel and queues the mint.

Scope & guards (J2499 / J2558):
- Exact 66 flow-first mint rows of PICTURE_PLAN_v02.json (66 Quality @ 100 = 6600,
  0 Fast; total cap = 6600 credits), locked by row_id, board sha256,
  plan sha256, and prompt sha256 in PASS1_SCOPE_J2499.json.
- Order inside pass 1: Part 01 first (first 30s + Shorts openings), then Parts 02..06.
- Right account & plan: the studio Ultra account on flow.google.com (verified by
  SHA-256 digest so no personal email address is stored in code or receipts) + ULTRA.
- Right model & length per row: Veo 3.1 - Quality (8s, 16:9, x1, 100 credits);
  Veo 3.1 - Fast is refused; Nano Banana 2.1 (16:9, x1, 0 credits)
  for missing start stills.
- Live price (100 credits) verified before each batch AND atomically
  re-verified per row right before the trusted CDP mouse click on Create.
- Live balance, pending charges, and other films' reservations counted via
  canonical ~/_desk/state/flow/shared accounting; cap 6600, at most 1 take/row,
  at most 5 rows and 1000 credits per batch.
- Shared writer lock, duplicate-process refusal, missing/corrupt style reference
  refusal (house style_refs + Explorer sheet), scope/prompt drift refusal,
  and sha256-verified NAS copies + receipts.
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
import subprocess
import sys
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

# SHA-256 digests of lowercase account strings (no personal email stored in repo or receipts).
REQUIRED_ACCOUNT_SHA256 = "81a01c9d841483f444008cd69e98b26019e032ed75b5e33e17409a76c6525ce9"
FORBIDDEN_ACCOUNT_SHA256 = "93b0f97ef00986fa90ead10a83be910d43707ddc8023daa2018ed1d95cbbb9d4"

FILM_ID = "HOS:013"
FILM_FOLDER = "013_Darwin-Wallace-Evolution"
EXPECTED_ROW_COUNT = 66
EXPECTED_QUALITY_COUNT = 66
EXPECTED_FAST_COUNT = 0
MAX_TOTAL_CREDITS = 6600
MAX_TAKES_PER_ROW = 1
MAX_BATCH_ROWS = 5
MAX_BATCH_CREDITS = 1000
HEADROOM_FLOOR = 0

MODEL_BY_QUALITY = {
    "Quality": "Veo 3.1 - Quality",
}
PRICE_BY_QUALITY = {
    "Quality": 100,
}
# Chief price pass, 10 Nov 2026 (#470): one approved 0-credit 16:9 image model on Ultra.
REQUIRED_STILL_MODEL = "Nano Banana 2.1"
REQUIRED_OUTPUTS = "x1"
REQUIRED_ASPECT = "16:9"
REQUIRED_DURATION = "8s"
REQUIRED_CLIP_S = 8
SUBMIT_ENV = "HOS013_PASS1_SUBMIT"
# A take Flow refused under its content policy: no output and no credits (Chief rulings on J2033,
# desk 6784299215, 6785508086 and 6785808071). It uses up the row's one pass-1 take: the row is
# not submitted again and goes to the picture review as refused.
POLICY_REFUSED = "FAILED_POLICY"
DEFAULT_RESERVATION = "HOS013_PASS1"
FLOW_HOST = "flow.google.com"
GENERATE_LINE_RE = re.compile(r"^Generating will use (\d+) credits$")

EDIT_REL = Path("02_Video-Projects/013_Darwin-Wallace-Evolution/07_Edit-Project")
SCOPE_NAME = "PASS1_SCOPE_J2499.json"
PLAN_NAME = "PICTURE_PLAN_v02.json"
EXPLORER_REF_REL = Path("01_Character/05_Generation-References/hos-explorer-reference-v01.jpg")
DEFAULT_NAS_MEDIA = Path(
    "/Volumes/data/studio-live/History Of Science/02_Video-Projects/013_Darwin-Wallace-Evolution"
)

EXPLORER_LOCK = (
    "Exactly ONE Explorer: young boy, messy brown hair, round thin gold glasses, "
    "teal long coat, tan vest, brown bow tie, satchel. Acts then leaves."
)


class GuardError(RuntimeError):
    """A credit, scope, lock, style-ref, account or status rule refused the run before any submit."""


@dataclass(frozen=True)
class Row:
    index: int
    row_id: str
    part: int
    plate_id: str
    board: str
    quality: str
    flow_model: str
    max_takes: int
    try1_credits: int
    flow_clip_s: int
    t_s: float
    t_end_s: float
    use_s: float
    explorer: bool
    prompt: str
    prompt_sha256: str
    normalized_prompt_sha256: str

    @property
    def key(self) -> tuple[int, str]:
        return (self.part, self.plate_id)


@dataclass(frozen=True)
class PriceEvidence:
    quality: str
    model: str
    outputs: str
    aspect: str
    duration: str
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


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def account_sha256(account: str | None) -> str:
    if not isinstance(account, str) or not account.strip():
        return ""
    return sha256_bytes(account.strip().lower().encode("utf-8"))


def verify_account_list(accounts: object) -> str:
    if not isinstance(accounts, list) or len(accounts) != 1 or not isinstance(accounts[0], str):
        raise GuardError("live Flow account is missing or ambiguous")
    digest = account_sha256(accounts[0])
    if digest == FORBIDDEN_ACCOUNT_SHA256 or digest != REQUIRED_ACCOUNT_SHA256:
        raise GuardError("Flow account is not the studio Ultra account")
    return REQUIRED_ACCOUNT_SHA256


def expected_model_for(row_or_quality: Row | str) -> str:
    quality = row_or_quality.quality if isinstance(row_or_quality, Row) else str(row_or_quality)
    if quality in ("Fast", "Veo 3.1 - Fast", "Veo 3.1 Fast"):
        raise GuardError(f"Veo 3.1 - Fast is refused ({quality!r})")
    if quality not in MODEL_BY_QUALITY:
        raise GuardError(f"unsupported row quality {quality!r}")
    return MODEL_BY_QUALITY[quality]


def expected_credits_for(row_or_quality: Row | str) -> int:
    quality = row_or_quality.quality if isinstance(row_or_quality, Row) else str(row_or_quality)
    if quality in ("Fast", "Veo 3.1 - Fast", "Veo 3.1 Fast"):
        raise GuardError(f"Veo 3.1 - Fast is refused ({quality!r})")
    if quality not in PRICE_BY_QUALITY:
        raise GuardError(f"unsupported row quality {quality!r}")
    return PRICE_BY_QUALITY[quality]


def load_scope(repo: Path) -> list[Row]:
    """Load and verify the exact 66 pass-1 mint rows against PICTURE_PLAN_v02 and all 6 part boards."""
    scope_path = repo / EDIT_REL / SCOPE_NAME
    if not scope_path.is_file():
        raise GuardError(f"missing scope file: {scope_path}")
    scope = json.loads(scope_path.read_text())
    if scope.get("film") != FILM_ID:
        raise GuardError(f"scope film {scope.get('film')!r} != {FILM_ID}")

    plan_rel = Path(str(scope.get("plan_file") or ""))
    if plan_rel != EDIT_REL / PLAN_NAME:
        raise GuardError(f"unexpected plan_file {plan_rel}")
    plan_path = repo / plan_rel
    if not plan_path.is_file():
        raise GuardError(f"missing film picture plan: {plan_path}")
    if sha256_file(plan_path) != scope.get("plan_sha256"):
        raise GuardError("scope drift: PICTURE_PLAN_v02.json sha256 mismatch")

    plan = json.loads(plan_path.read_text())
    totals = plan.get("totals") or {}
    if int(totals.get("Fast") or 0) != 0:
        raise GuardError("Veo 3.1 - Fast is refused in PICTURE_PLAN_v02 totals")
    if (
        int(totals.get("mint_rows") or 0) != EXPECTED_ROW_COUNT
        or int(totals.get("Quality") or 0) != EXPECTED_QUALITY_COUNT
        or int(totals.get("Fast") or 0) != EXPECTED_FAST_COUNT
        or int(totals.get("flow_credits_try1") or 0) != MAX_TOTAL_CREDITS
    ):
        raise GuardError("scope drift: PICTURE_PLAN_v02 totals do not match 66 rows (66Q/0F = 6600)")

    caps = scope.get("caps") or {}
    cap_models = caps.get("models") or {}
    cap_prices = caps.get("prices") or {}
    if (
        "Fast" in cap_models
        or "Veo 3.1 - Fast" in cap_models.values()
        or "Fast" in cap_prices
    ):
        raise GuardError("Veo 3.1 - Fast is refused in scope caps")
    if (
        int(caps.get("max_total_credits") or 0) != MAX_TOTAL_CREDITS
        or int(caps.get("max_takes_per_row") or 0) != MAX_TAKES_PER_ROW
        or int(caps.get("max_batch_rows") or 0) != MAX_BATCH_ROWS
        or int(caps.get("max_batch_credits") or 0) != MAX_BATCH_CREDITS
    ):
        raise GuardError("scope caps do not match J2499 constants")

    raw_rows = scope.get("rows") or []
    for raw in raw_rows:
        if raw.get("quality") in ("Fast", "Veo 3.1 - Fast") or "Fast" in str(raw.get("flow_model") or ""):
            raise GuardError(f"Veo 3.1 - Fast row is refused in scope: {raw.get('row_id')!r}")
    if len(raw_rows) != EXPECTED_ROW_COUNT:
        raise GuardError(f"scope drift: scope has {len(raw_rows)} rows, expected {EXPECTED_ROW_COUNT}")

    # Independently scan all 6 part boards to ensure no flow-first row was dropped or added.
    boards_meta = scope.get("boards") or {}
    if set(boards_meta.keys()) != {str(part) for part in range(1, 7)}:
        raise GuardError("scope must pin all 6 part boards (parts 1..6)")

    discovered_flow_rows: list[tuple[int, dict, Path, str]] = []
    boards_by_part: dict[int, tuple[Path, str, dict[str, dict]]] = {}
    for part in range(1, 7):
        meta = boards_meta[str(part)]
        board_rel = Path(str(meta.get("path") or ""))
        expected_name = f"part-0{part}_plates_v02.json"
        if board_rel != EDIT_REL / "parts" / expected_name:
            raise GuardError(f"unexpected board path for part {part}: {board_rel}")
        board_path = repo / board_rel
        if not board_path.is_file():
            raise GuardError(f"missing board file: {board_path}")
        digest = sha256_file(board_path)
        if digest != meta.get("sha256"):
            raise GuardError(f"scope drift: board hash mismatch for {board_rel}")
        board = json.loads(board_path.read_text())
        plates = board.get("plates") or []
        by_id: dict[str, dict] = {}
        for plate in plates:
            pid = str(plate.get("id") or "")
            if not pid or pid in by_id:
                raise GuardError(f"invalid or duplicate plate id {pid!r} on {board_rel}")
            if plate.get("quality") in ("Fast", "Veo 3.1 - Fast") or "Fast" in str(plate.get("flow_model") or ""):
                raise GuardError(f"Veo 3.1 - Fast row is refused on {board_rel}:{pid}")
            by_id[pid] = plate
            if plate.get("route") == "flow-first":
                discovered_flow_rows.append((part, plate, board_rel, digest))
            elif plate.get("route") not in ("code-graphic", "archive", "reuse"):
                raise GuardError(f"unknown plate route {plate.get('route')!r} on {board_rel}:{pid}")
        boards_by_part[part] = (board_rel, digest, by_id)

    if len(discovered_flow_rows) != EXPECTED_ROW_COUNT:
        raise GuardError(
            f"scope drift: boards contain {len(discovered_flow_rows)} flow-first rows, expected {EXPECTED_ROW_COUNT}"
        )

    rows: list[Row] = []
    seen_row_ids: set[str] = set()
    seen_plate_ids: set[str] = set()
    for expected_index, raw in enumerate(raw_rows, start=1):
        part = int(raw.get("part") or 0)
        if part < 1 or part > 6:
            raise GuardError(f"row {raw.get('row_id')!r} has invalid part {part}")
        plate_id = str(raw.get("id") or "")
        row_id = str(raw.get("row_id") or "")
        if row_id != f"P{part}:{plate_id}":
            raise GuardError(f"scope drift: malformed row_id {row_id!r} for part {part} id {plate_id!r}")
        if int(raw.get("index") or 0) != expected_index:
            raise GuardError(f"scope drift: row {row_id} index {raw.get('index')} != {expected_index}")
        if row_id in seen_row_ids or plate_id in seen_plate_ids:
            raise GuardError(f"scope drift: duplicate row {row_id}")
        seen_row_ids.add(row_id)
        seen_plate_ids.add(plate_id)

        board_rel, board_digest, by_id = boards_by_part[part]
        if str(raw.get("board")) != str(board_rel) or raw.get("board_sha256") != board_digest:
            raise GuardError(f"scope drift: board binding mismatch on {row_id}")
        plate = by_id.get(plate_id)
        if plate is None:
            raise GuardError(f"scope drift: {row_id} does not exist on {board_rel}")
        if plate.get("route") != "flow-first":
            raise GuardError(f"scope drift: {row_id} has non-mint route {plate.get('route')!r}")

        quality = str(plate.get("quality") or "")
        if quality not in MODEL_BY_QUALITY or raw.get("quality") != quality:
            raise GuardError(f"scope drift: {row_id} quality mismatch ({quality!r} vs {raw.get('quality')!r})")

        expected_model = expected_model_for(quality)
        expected_cost = expected_credits_for(quality)
        board_model = str(plate.get("flow_model") or "")
        if quality not in board_model or "Veo 3.1" not in board_model:
            raise GuardError(f"scope drift: {row_id} board flow_model {board_model!r} does not match {quality}")
        if raw.get("flow_model") != expected_model:
            raise GuardError(f"scope drift: {row_id} scope flow_model {raw.get('flow_model')!r} != {expected_model!r}")

        try1 = int(plate.get("flow_credits_try1") or 0)
        if try1 != expected_cost or int(raw.get("try1_credits") or 0) != expected_cost:
            raise GuardError(f"scope drift: {row_id} price mismatch ({try1} / {raw.get('try1_credits')})")
        if int(raw.get("max_takes") or 0) != MAX_TAKES_PER_ROW:
            raise GuardError(f"scope drift: {row_id} max_takes {raw.get('max_takes')} != {MAX_TAKES_PER_ROW}")

        clip_s = int(plate.get("flow_clip_s") or 0)
        use_s = float(plate.get("use_s") or 0.0)
        if clip_s != REQUIRED_CLIP_S or int(raw.get("flow_clip_s") or 0) != REQUIRED_CLIP_S:
            raise GuardError(f"scope drift: {row_id} flow_clip_s must be {REQUIRED_CLIP_S}s")
        if use_s <= 0.0 or use_s > float(REQUIRED_CLIP_S) or abs(use_s - float(raw.get("use_s") or 0.0)) > 1e-6:
            raise GuardError(f"scope drift: {row_id} use_s {use_s} invalid or drifted")

        prompt = str(plate.get("prompt") or "")
        if not prompt.strip():
            raise GuardError(f"scope drift: {row_id} has an empty prompt")
        prompt_sha = sha256_bytes(prompt.encode("utf-8"))
        norm_sha = sha256_bytes(" ".join(prompt.split()).encode("utf-8"))
        if prompt_sha != raw.get("prompt_sha256") or norm_sha != raw.get("normalized_prompt_sha256"):
            raise GuardError(f"scope drift: prompt hash mismatch on {row_id}")

        explorer = bool(plate.get("explorer", False))
        if explorer is not bool(raw.get("explorer", False)):
            raise GuardError(f"scope drift: explorer flag mismatch on {row_id}")

        rows.append(
            Row(
                index=expected_index,
                row_id=row_id,
                part=part,
                plate_id=plate_id,
                board=str(board_rel),
                quality=quality,
                flow_model=expected_model,
                max_takes=MAX_TAKES_PER_ROW,
                try1_credits=expected_cost,
                flow_clip_s=REQUIRED_CLIP_S,
                t_s=float(plate.get("t_s") or 0.0),
                t_end_s=float(plate.get("t_end_s") or 0.0),
                use_s=use_s,
                explorer=explorer,
                prompt=prompt,
                prompt_sha256=prompt_sha,
                normalized_prompt_sha256=norm_sha,
            )
        )

    expected_discovered_ids = [f"P{part}:{plate['id']}" for part, plate, _, _ in discovered_flow_rows]
    if [row.row_id for row in rows] != expected_discovered_ids:
        raise GuardError("scope drift: row order or membership differs from Part 01 -> Part 06 board order")

    q_count = sum(1 for row in rows if row.quality == "Quality")
    f_count = sum(1 for row in rows if row.quality == "Fast")
    total_credits = sum(row.try1_credits for row in rows)
    if q_count != EXPECTED_QUALITY_COUNT or f_count != EXPECTED_FAST_COUNT or total_credits != MAX_TOTAL_CREDITS:
        raise GuardError(
            f"scope drift: counts {q_count}Q/{f_count}F/{total_credits} credits != 66Q/0F/6600"
        )
    return rows


def order_rows(rows: list[Row]) -> list[Row]:
    """Order strictly Part 01 first (first 30s + Shorts openings), then Parts 02..06 by timeline."""
    if not rows:
        raise GuardError("cannot order empty row list")
    ordered = sorted(rows, key=lambda row: (row.part, row.t_s, row.index))
    if ordered[0].part != 1:
        raise GuardError("first pass must start with Part 01")
    seen_keys: set[tuple[int, str]] = set()
    prev_key = (0, -1.0)
    for row in ordered:
        if row.key in seen_keys:
            raise GuardError(f"duplicate row in order: {row.row_id}")
        seen_keys.add(row.key)
        cur = (row.part, row.t_s)
        if cur < prev_key:
            raise GuardError(f"out-of-order row {row.row_id}")
        prev_key = cur
    return ordered


def assert_batch_limits(batch: list[Row]) -> int:
    if not batch:
        raise GuardError("empty batch is not allowed")
    if len(batch) > MAX_BATCH_ROWS:
        raise GuardError(f"batch of {len(batch)} rows exceeds MAX_BATCH_ROWS={MAX_BATCH_ROWS}")
    seen: set[str] = set()
    prev_order = (0, -1.0, 0)
    credits = 0
    for row in batch:
        if row.row_id in seen:
            raise GuardError(f"duplicate row in batch: {row.row_id}")
        seen.add(row.row_id)
        cur_order = (row.part, row.t_s, row.index)
        if cur_order < prev_order:
            raise GuardError(f"batch violates Part 01 -> Part 06 order at {row.row_id}")
        prev_order = cur_order
        expected_cost = expected_credits_for(row)
        if row.try1_credits != expected_cost or row.max_takes != MAX_TAKES_PER_ROW:
            raise GuardError(f"invalid row cost or max_takes on {row.row_id}")
        credits += row.try1_credits
    if credits > MAX_BATCH_CREDITS:
        raise GuardError(
            f"batch of {len(batch)} rows / {credits} credits exceeds {MAX_BATCH_CREDITS} credits"
        )
    return credits


def batch_rows(rows: list[Row]) -> list[list[Row]]:
    """Pack ordered rows into batches of at most 5 rows and at most 1,000 credits."""
    if not rows:
        return []
    ordered = order_rows(rows)
    batches: list[list[Row]] = []
    idx = 0
    while idx < len(ordered):
        batch: list[Row] = []
        credits = 0
        while (
            idx < len(ordered)
            and len(batch) < MAX_BATCH_ROWS
            and credits + ordered[idx].try1_credits <= MAX_BATCH_CREDITS
        ):
            batch.append(ordered[idx])
            credits += ordered[idx].try1_credits
            idx += 1
        if not batch:
            raise GuardError(f"row {ordered[idx].row_id} alone exceeds batch limits")
        assert_batch_limits(batch)
        batches.append(batch)
    return batches


def accept_price(price: PriceEvidence, *, quality: str | None = None,
                 now: datetime | None = None, max_age_s: int = 900) -> int:
    target_quality = quality or price.quality
    expected_model = expected_model_for(target_quality)
    expected_cost = expected_credits_for(target_quality)
    if price.quality != target_quality:
        raise GuardError(f"price quality {price.quality!r} != {target_quality!r}")
    if price.model != expected_model:
        raise GuardError(f"model {price.model!r} is not {expected_model!r}")
    if price.outputs != REQUIRED_OUTPUTS:
        raise GuardError(f"outputs {price.outputs!r} are not {REQUIRED_OUTPUTS}")
    if price.aspect != REQUIRED_ASPECT:
        raise GuardError(f"aspect {price.aspect!r} is not {REQUIRED_ASPECT}")
    if price.duration != REQUIRED_DURATION:
        raise GuardError(f"duration {price.duration!r} is not {REQUIRED_DURATION}")
    if type(price.credits) is not int or price.credits != expected_cost:
        raise GuardError(f"price {price.credits!r} is not {expected_cost} for {target_quality}")
    match = GENERATE_LINE_RE.match((price.generate_line or "").strip())
    if not match or int(match.group(1)) != expected_cost:
        raise GuardError(f"generate line is not an exact {expected_cost}-credit charge")
    if not price.read_at:
        raise GuardError("price evidence has no read time")
    stamp = datetime.fromisoformat(price.read_at)
    if stamp.tzinfo is None:
        stamp = stamp.replace(tzinfo=timezone.utc)
    if now is not None:
        age = (now - stamp).total_seconds()
        if age < 0 or age > max_age_s:
            raise GuardError(f"price read is not fresh ({int(age)}s)")
    return expected_cost


def accept_batch_prices(prices_by_quality: dict[str, PriceEvidence] | None, *,
                        now: datetime | None = None, max_age_s: int = 900) -> dict[str, int]:
    """Require fresh live price reading for Quality (100) before each batch; refuse Fast."""
    if not isinstance(prices_by_quality, dict):
        raise GuardError("missing pre-batch live price readings")
    if "Fast" in prices_by_quality or "Veo 3.1 - Fast" in prices_by_quality:
        raise GuardError("Veo 3.1 - Fast is refused in pre-batch live price readings")
    verified: dict[str, int] = {}
    for quality in ("Quality",):
        ev = prices_by_quality.get(quality)
        if not isinstance(ev, PriceEvidence):
            raise GuardError(f"missing pre-batch live price reading for {quality}")
        verified[quality] = accept_price(ev, quality=quality, now=now, max_age_s=max_age_s)
    return verified


def accept_account(account_or_sha256: str | None, read_at: str | None, *,
                   now: datetime, max_age_s: int = 900) -> str:
    if not read_at:
        raise GuardError("balance read timestamp is missing")
    stamp = datetime.fromisoformat(read_at)
    if stamp.tzinfo is None:
        stamp = stamp.replace(tzinfo=timezone.utc)
    age = (now - stamp).total_seconds()
    if age < 0 or age > max_age_s:
        raise GuardError(f"balance read is not fresh ({int(age)}s)")
    if not isinstance(account_or_sha256, str) or not account_or_sha256.strip():
        raise GuardError("Flow account is missing")
    candidate = account_or_sha256.strip().lower()
    digest = candidate if re.fullmatch(r"[0-9a-f]{64}", candidate) else account_sha256(candidate)
    if digest == FORBIDDEN_ACCOUNT_SHA256 or digest != REQUIRED_ACCOUNT_SHA256:
        raise GuardError("Flow account is not the studio Ultra account")
    return REQUIRED_ACCOUNT_SHA256


def load_plan_style_refs(repo: Path | None = None) -> list[str]:
    plan_path = (repo or repo_root_from()) / EDIT_REL / PLAN_NAME
    payload = json.loads(plan_path.read_text())
    refs = payload.get("style_refs") if isinstance(payload, dict) else None
    if not isinstance(refs, list) or not refs or not all(isinstance(r, str) and r.strip() for r in refs):
        raise GuardError(f"film plan {plan_path} is missing non-empty style_refs")
    return [r.strip() for r in refs]


def _probe_image_16x9_or_valid(path: Path, *, require_16x9: bool = False) -> tuple[int, int, str]:
    if not path.is_file() or path.stat().st_size == 0:
        raise GuardError(f"missing or empty reference image: {path}")
    digest = sha256_file(path)
    try:
        probe = subprocess.run(
            ["ffprobe", "-v", "error", "-show_streams", "-of", "json", str(path)],
            check=True,
            capture_output=True,
            text=True,
        )
        streams = json.loads(probe.stdout).get("streams") or []
        if len(streams) != 1 or streams[0].get("codec_type") != "video":
            raise GuardError(f"reference image needs one image stream: {path}")
        width, height = int(streams[0]["width"]), int(streams[0]["height"])
        subprocess.run(
            ["ffmpeg", "-v", "error", "-xerror", "-i", str(path), "-frames:v", "1", "-f", "null", "-"],
            check=True,
            capture_output=True,
        )
    except GuardError:
        raise
    except Exception as exc:
        raise GuardError(f"corrupt or unreadable reference image: {path}") from exc
    if width < 640 or height < 360:
        raise GuardError(f"reference image resolution too small ({width}x{height}): {path}")
    if require_16x9 and abs(width / height - 16 / 9) > 0.02:
        raise GuardError(f"reference image is not 16:9 ({width}x{height}): {path}")
    return width, height, digest


def verify_style_references(repo: Path, media: Path, rows: list[Row] | None = None, *,
                            check_scope_hashes: bool = True) -> dict:
    """Verify every house style_ref (under media) and Explorer ref (under repo) before any Flow call."""
    plan_path = repo / EDIT_REL / PLAN_NAME
    if not plan_path.is_file():
        raise GuardError(f"missing film picture plan: {plan_path}")
    still_dir = repo / "02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project"
    if not still_dir.is_dir():
        still_dir = repo_root_from() / "02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project"
    if str(still_dir) not in sys.path:
        sys.path.insert(0, str(still_dir))
    import _flow_still_v01 as still_tool

    try:
        resolved_house = still_tool.style_refs_from_plan(plan_path, media)
    except Exception as exc:
        raise GuardError(f"style reference configuration invalid: {exc}") from exc

    scope_house_hashes: dict[str, str] = {}
    scope_explorer_hash: str | None = None
    scope_path = repo / EDIT_REL / SCOPE_NAME
    if check_scope_hashes and scope_path.is_file():
        scope = json.loads(scope_path.read_text())
        srefs = scope.get("style_refs") or {}
        for item in srefs.get("house") or []:
            scope_house_hashes[str(item.get("path"))] = str(item.get("sha256"))
        exp_meta = srefs.get("explorer") or {}
        if exp_meta.get("sha256"):
            scope_explorer_hash = str(exp_meta["sha256"])

    raw_rels = load_plan_style_refs(repo)
    house_verified = []
    for rel, path in zip(raw_rels, resolved_house):
        if not path.is_file() or path.stat().st_size == 0:
            raise GuardError(f"missing style reference image: {path}")
        width, height, digest = _probe_image_16x9_or_valid(path, require_16x9=True)
        expected_sha = scope_house_hashes.get(rel)
        if expected_sha and digest != expected_sha:
            raise GuardError(f"style reference sha256 drift on {rel}: {digest} != {expected_sha}")
        house_verified.append({
            "rel": rel,
            "path": str(path),
            "sha256": digest,
            "width": width,
            "height": height,
        })

    needs_explorer = True if rows is None else any(row.explorer for row in rows)
    explorer_verified = None
    if needs_explorer:
        plan_payload = json.loads(plan_path.read_text())
        exp_rel_str = str(plan_payload.get("explorer_ref") or EXPLORER_REF_REL)
        exp_rel = Path(exp_rel_str)
        if exp_rel.is_absolute():
            raise GuardError(f"explorer_ref must be repo-relative: {exp_rel_str!r}")
        exp_path = (repo / exp_rel).resolve()
        if repo.resolve() not in exp_path.parents or not exp_path.is_file():
            raise GuardError(f"missing Explorer style reference: {exp_path}")
        width, height, digest = _probe_image_16x9_or_valid(exp_path, require_16x9=False)
        if scope_explorer_hash and digest != scope_explorer_hash:
            raise GuardError(f"Explorer reference sha256 drift: {digest} != {scope_explorer_hash}")
        explorer_verified = {
            "rel": str(exp_rel),
            "path": str(exp_path),
            "sha256": digest,
            "width": width,
            "height": height,
        }

    return {"house": house_verified, "explorer": explorer_verified}


def ledger_totals(entries: list[dict]) -> tuple[int, int, bool, dict[str, int]]:
    """Sum spent/pending credits and per-row take counts. Reject KEEP, unknown status, or >1 take."""
    latest: dict[tuple[str, int], dict] = {}
    for entry in entries:
        status = entry.get("status")
        if status == "KEEP" or entry.get("keep") is True or entry.get("review") == "KEEP":
            raise GuardError("ledger contains KEEP; pass-1 runner never auto-KEEPs")
        if status not in ("SUBMITTING", "PENDING_REVIEW", "GENERATED", "FAILED", POLICY_REFUSED):
            raise GuardError(f"unknown ledger status {status!r}")
        if status == POLICY_REFUSED and (entry.get("credits_used") != 0 or type(entry.get("credits_used")) is not int
                                         or not str(entry.get("reason") or "").strip()):
            raise GuardError(f"{POLICY_REFUSED} needs credits_used 0 and a reason")
        row_id = str(entry.get("row_id") or "")
        if not row_id:
            part = entry.get("part")
            plate_id = entry.get("plate_id")
            if part is not None and plate_id:
                row_id = f"P{int(part)}:{plate_id}"
        take = int(entry.get("take") or 0)
        if not row_id or take < 1:
            raise GuardError(f"invalid ledger row/take identity in {entry!r}")
        latest[(row_id, take)] = entry

    spent = 0
    pending = 0
    unknown = False
    takes: dict[str, int] = {}
    for (row_id, _take), entry in latest.items():
        takes[row_id] = takes.get(row_id, 0) + 1
        status = entry.get("status")
        if status == "SUBMITTING":
            reserved = entry.get("credits_reserved")
            if type(reserved) is not int or reserved <= 0:
                unknown = True
            else:
                pending += reserved
        elif status == POLICY_REFUSED:
            pass  # refused by Flow, 0 credits; it still used the row's take
        else:
            amount = entry.get("credits_used")
            if amount is None:
                amount = entry.get("credits_reserved")
            if type(amount) is not int or amount <= 0:
                unknown = True
            else:
                spent += amount
    if any(count > MAX_TAKES_PER_ROW for count in takes.values()):
        raise GuardError(f"a row already exceeds MAX_TAKES_PER_ROW={MAX_TAKES_PER_ROW}")
    if spent + pending > MAX_TOTAL_CREDITS:
        raise GuardError(f"ledger {spent}+{pending} exceeds MAX_TOTAL_CREDITS={MAX_TOTAL_CREDITS}")
    return spent, pending, unknown, takes


def headroom(live: int | None, spent: int, pending: int, other: int, *,
             posted: int = 0, floor: int = HEADROOM_FLOOR) -> int:
    if type(live) is not int or live < 0 or type(other) is not int or other < 0 or type(floor) is not int or floor < 0:
        raise GuardError("unknown or invalid balance, floor, or other reservations")
    if min(spent, pending, posted) < 0 or posted > spent:
        raise GuardError("invalid posted/unposted accounting")
    remaining_cap = MAX_TOTAL_CREDITS - spent - pending
    if remaining_cap < 0 or spent + pending > MAX_TOTAL_CREDITS:
        raise GuardError(f"spend {spent}+{pending} exceeds the {MAX_TOTAL_CREDITS} pass-1 cap")
    unposted = spent - posted + pending
    left = live - unposted - remaining_cap - other
    if left < floor:
        raise GuardError(
            f"headroom {left} < {floor} after reserving remaining cap {remaining_cap} and other {other}"
        )
    return left


def can_take(*, row: Row, live: int | None, spent: int, pending: int, other: int,
             takes_done: int, unknown_pending: bool, cost: int, posted: int = 0,
             floor: int = HEADROOM_FLOOR) -> int:
    if unknown_pending:
        raise GuardError("unknown outstanding charges")
    if takes_done >= MAX_TAKES_PER_ROW:
        raise GuardError(f"{row.row_id} already has {takes_done} take(s); pass-1 cap is {MAX_TAKES_PER_ROW}")
    expected_cost = expected_credits_for(row)
    if type(cost) is not int or cost != expected_cost or cost != row.try1_credits:
        raise GuardError(f"refusing cost {cost!r} for {row.row_id} ({row.quality} expects {expected_cost})")
    if spent + pending + cost > MAX_TOTAL_CREDITS:
        raise GuardError(f"cap {MAX_TOTAL_CREDITS}: spent {spent} pending {pending} cost {cost}")
    return headroom(live, spent, pending + cost, other, posted=posted, floor=floor)


def build_plan(rows: list[Row], *, repo: Path | None = None) -> dict:
    root = repo or repo_root_from()
    plan_rel = EDIT_REL / PLAN_NAME
    plan_path = root / plan_rel
    ordered = order_rows(rows)
    batches = batch_rows(ordered)
    per_part: dict[str, dict] = {}
    for part in range(1, 7):
        prows = [r for r in ordered if r.part == part]
        per_part[f"part_{part:02d}"] = {
            "rows": len(prows),
            "Quality": sum(1 for r in prows if r.quality == "Quality"),
            "Fast": sum(1 for r in prows if r.quality == "Fast"),
            "explorer": sum(1 for r in prows if r.explorer),
            "credits_try1": sum(r.try1_credits for r in prows),
        }
    return {
        "job": "J2499",
        "film": FILM_ID,
        "plan_file": str(plan_rel),
        "plan_sha256": sha256_file(plan_path),
        "submissions": 0,
        "create_clicks": 0,
        "credits_spent": 0,
        "keep": False,
        "review": "PENDING_REVIEW",
        "file_state_when_written": "GENERATED",
        "row_count": len(ordered),
        "quality_count": sum(1 for r in ordered if r.quality == "Quality"),
        "fast_count": sum(1 for r in ordered if r.quality == "Fast"),
        "explorer_count": sum(1 for r in ordered if r.explorer),
        "style_refs": load_plan_style_refs(root),
        "explorer_ref": str(EXPLORER_REF_REL),
        "caps": {
            "prices": dict(PRICE_BY_QUALITY, Still=0),
            "models": dict(MODEL_BY_QUALITY, Still=REQUIRED_STILL_MODEL),
            "duration": REQUIRED_DURATION,
            "aspect": REQUIRED_ASPECT,
            "outputs": REQUIRED_OUTPUTS,
            "takes_per_row": MAX_TAKES_PER_ROW,
            "total_credits": MAX_TOTAL_CREDITS,
            "batch_rows": MAX_BATCH_ROWS,
            "batch_credits": MAX_BATCH_CREDITS,
            "floor": HEADROOM_FLOOR,
        },
        "per_part": per_part,
        "order": [
            {
                "index": row.index,
                "row_id": row.row_id,
                "part": row.part,
                "id": row.plate_id,
                "quality": row.quality,
                "flow_model": row.flow_model,
                "flow_clip_s": row.flow_clip_s,
                "try1_credits": row.try1_credits,
                "explorer": row.explorer,
                "prompt_sha256": row.prompt_sha256,
            }
            for row in ordered
        ],
        "batches": [
            {
                "batch_index": idx,
                "rows": [row.row_id for row in batch],
                "row_count": len(batch),
                "credits": sum(row.try1_credits for row in batch),
            }
            for idx, batch in enumerate(batches, start=1)
        ],
    }


def versioned_output(media: Path, part: int, plate_id: str, take: int = 1) -> Path:
    return (
        media
        / "04_Generated-Clips"
        / f"part{part:02d}"
        / "raw"
        / "v01_pass1"
        / f"P{part:02d}_{plate_id}_t{take}.mp4"
    )


def next_version(media: Path, part: int, plate_id: str, used=()) -> tuple[int, Path]:
    """The first take number with no file and no ledger line. `used` holds the take numbers the pass
    ledger already has for this row: a take Flow refused leaves no file, and numbering a new take
    the same would collide with the refused take's shared charge."""
    for take in range(1, MAX_TAKES_PER_ROW + 1):
        dest = versioned_output(media, part, plate_id, take)
        if take not in used and not dest.exists():
            return take, dest
    raise GuardError(
        f"P{part}:{plate_id} already has {MAX_TAKES_PER_ROW} versioned file(s); pass 1 refuses a second take"
    )


def still_path(media: Path, part: int, plate_id: str) -> Path:
    return (
        media
        / "04_Generated-Clips"
        / f"part{part:02d}"
        / "refs"
        / "v01_flow_stills"
        / f"P{part:02d}_{plate_id}_t1.png"
    )


def verify_still_inventory(rows: list[Row], media: Path) -> list[dict]:
    """Validate every start still before paid video batch spending starts."""
    inventory = []
    for row in rows:
        path = still_path(media, row.part, row.plate_id)
        if not path.is_file():
            raise GuardError(f"missing inventory start still for {row.row_id}: {path}")
        width, height, digest = _probe_image_16x9_or_valid(path, require_16x9=True)
        if width < 1280 or height < 720:
            raise GuardError(f"inventory still below 1280x720 HD ({width}x{height}): {path}")
        if digest != sha256_file(path):
            raise GuardError(f"inventory still changed while reading: {path}")
        pin = path.with_suffix(".sha256")
        if pin.exists() and pin.read_text().strip() != digest:
            raise GuardError(f"inventory differs from pinned start still: {path}")
        inventory.append({
            "row_id": row.row_id,
            "part": row.part,
            "plate_id": row.plate_id,
            "path": str(path.resolve()),
            "sha256": digest,
            "width": width,
            "height": height,
        })
    return inventory


class WriterLock:
    """Exclusive non-blocking flock. Any concurrent second process raises GuardError."""

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
            self.handle = None
            raise GuardError(f"writer lock held: {self.path}") from exc
        return self

    def __exit__(self, exc_type, exc, tb):
        if self.handle is not None:
            fcntl.flock(self.handle.fileno(), fcntl.LOCK_UN)
            self.handle.close()
            self.handle = None
        return False


def shared_flow_state_dir() -> Path:
    """Canonical cross-channel Flow accounting directory (~/_desk/state/flow/shared)."""
    return Path.home() / "_desk/state/flow/shared"


class SharedFlowAccounting:
    """Durable cross-channel Flow reservation & charge accounting (J2200 protocol)."""

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

    @classmethod
    def _parse_ledger_bytes(cls, data: bytes) -> dict:
        reservations, charges = {}, {}
        try:
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
                    cap = cls._amount(event["cap"])
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
                    amount = cls._amount(event["amount"])
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
                elif kind == "policy_refused":
                    # Flow refused the prompt under its content policy and charged
                    # nothing: a reversal event, appended, never a history rewrite.
                    charge = charges[key]
                    if charge["status"] != "CHARGED" or charge["posted"] or not event.get("evidence"):
                        raise GuardError("invalid policy-refusal reversal")
                    charge["status"] = "POLICY_REFUSED"
                    charge["amount"] = 0
                else:
                    raise GuardError(f"unknown shared Flow event {kind!r}")
        except GuardError:
            raise
        except (ValueError, KeyError, TypeError) as exc:
            raise GuardError("unreadable shared Flow ledger; no Create permitted") from exc

        unposted = sum(c["amount"] for c in charges.values() if not c["posted"])
        remaining = sum(
            r["cap"] - sum(c["amount"] for c in charges.values() if c["reservation"] == key)
            for key, r in reservations.items()
            if r["active"]
        )
        return dict(
            reservations=reservations,
            charges=charges,
            unposted=unposted,
            remaining_reservations=remaining,
            liability=unposted + remaining,
            pending=any(c["status"] == "PENDING" for c in charges.values()),
        )

    def snapshot(self) -> dict:
        self._assert_held()
        data = self.path.read_bytes() if self.path.exists() else b""
        return self._parse_ledger_bytes(data)

    @classmethod
    def peek_readonly(cls, state: Path | None = None) -> dict:
        """Read-only inspection for dry-run reporting without mutating lock or ledger."""
        base = state if state is not None else shared_flow_state_dir()
        path = base / "account.jsonl"
        data = path.read_bytes() if path.exists() else b""
        return cls._parse_ledger_bytes(data)

    def _event(self, event: dict) -> None:
        self._assert_held()
        append_ledger(self.path, {**event, "at": now_iso()})
        directory = os.open(self.state, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)

    def reserve(self, key: str, film: str, cap: int, *, live: int, floor: int = HEADROOM_FLOOR) -> None:
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
            if state["pending"] or live - state["liability"] < floor:
                raise GuardError("pending charge or insufficient shared Flow headroom")
            return
        if state["pending"] or live - state["liability"] - cap < floor:
            raise GuardError("pending charge or insufficient shared Flow headroom")
        self._event(dict(kind="reserve", id=key, film=film, cap=cap))

    def intent(self, key: str, reservation: str, amount: int, *, live: int,
               floor: int = HEADROOM_FLOOR) -> None:
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

    def resolve(self, key: str, *, submitted: bool, evidence: dict) -> None:
        charge = self.snapshot()["charges"].get(key)
        if type(submitted) is not bool or not charge or charge["status"] != "PENDING" or not evidence:
            raise GuardError("resolution needs a pending charge and evidence")
        self._event(dict(kind="charged" if submitted else "not_submitted", id=key, evidence=evidence))

    def reconcile_posted(self, key: str, *, evidence: dict) -> None:
        charge = self.snapshot()["charges"].get(key)
        if not charge or charge["status"] != "CHARGED" or charge["posted"] or not evidence:
            raise GuardError("posted reconciliation needs an unposted charge and evidence")
        self._event(dict(kind="posted", id=key, evidence=evidence))

    def release(self, key: str) -> None:
        state = self.snapshot()
        record = state["reservations"].get(key)
        if not record or not record["active"] or any(
            c["reservation"] == key and c["status"] == "PENDING" for c in state["charges"].values()
        ):
            raise GuardError("cannot release inactive reservation or pending charge")
        self._event(dict(kind="release", id=key))

    def reverse_policy_refusal(self, key: str, *, evidence: dict) -> bool:
        """Reverse an unposted CHARGED take that Flow refused under its content policy.

        Appends one ``policy_refused`` event (net charge 0). Re-running for an
        already reversed take is a no-op and returns False. A posted charge, a
        PENDING intent or a missing evidence record is refused.
        """
        charge = self.snapshot()["charges"].get(key)
        if charge and charge["status"] == "POLICY_REFUSED":
            return False
        if not charge or charge["status"] != "CHARGED" or charge["posted"] or not evidence:
            raise GuardError("policy-refusal reversal needs an unposted CHARGED take and evidence")
        self._event(dict(kind="policy_refused", id=key, evidence=evidence))
        return True

    def export_ai_spend(self, target: Path, *, by: str) -> int:
        """Idempotently export confirmed charges into the shared OWB ai_spend ledger."""
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
            if event["kind"] != "charged":
                continue
            key = event["id"]
            charge = state["charges"][key]
            if charge["status"] == "POLICY_REFUSED":
                continue
            film = state["reservations"][charge["reservation"]]["film"]
            evidence = event["evidence"]
            balances = evidence.get("ui", {}).get("balances", [])
            base = dict(at=event["at"], pool="flow", by=by, source="shared-flow", charge=key)
            if balances:
                if len(balances) != 1 or type(balances[0]) is not int or balances[0] < 0:
                    raise GuardError("invalid confirmed charge balance evidence")
                rows.append(
                    dict(base, id="flow:read:" + key, kind="record", left=balances[0], note="Configured UI before Create")
                )
            rows.append(
                dict(base, id="flow:spend:" + key, kind="spend", amount=charge["amount"], film=film, what=key)
            )
        target.parent.mkdir(parents=True, exist_ok=True)
        with WriterLock(target.with_name(target.name + ".lock")):
            data = target.read_bytes() if target.exists() else b""
            if data and not data.endswith(b"\n"):
                raise GuardError("torn ai_spend ledger; reconcile before export")
            try:
                existing = [json.loads(line) for line in data.splitlines()]
                if any(not isinstance(row, dict) for row in existing):
                    raise ValueError("non-object row")
            except (ValueError, TypeError) as exc:
                raise GuardError("unreadable ai_spend ledger") from exc
            indexed = {}
            for row in existing:
                if "id" in row:
                    if row["id"] in indexed:
                        raise GuardError("duplicate ai_spend receipt identity")
                    indexed[row["id"]] = row
            # A refused take that reached the report before it was reversed is taken back
            # by one more receipt, for exactly the amount written, so the report nets to
            # zero. A refused take that never reached the report writes nothing. Nor does
            # one already taken back, by this receipt or by a correction entered by hand
            # with the ai_spend tool that names the charge.
            for event in events:
                if event["kind"] != "policy_refused":
                    continue
                key = event["id"]
                spent = indexed.get("flow:spend:" + key)
                taken_back = any(
                    row.get("kind") == "spend" and type(row.get("amount")) in (int, float)
                    and row["amount"] < 0 and key in f"{row.get('charge', '')} {row.get('what', '')}"
                    for row in existing)
                if spent is not None and not taken_back:
                    rows.append(dict(at=event["at"], pool="flow", by=by, source="shared-flow",
                                     charge=key, id="flow:reversal:" + key, kind="spend",
                                     amount=-spent["amount"], film=spent["film"],
                                     what=key + " refused by Flow policy, not charged"))
            missing = []
            for row in rows:
                previous = indexed.get(row["id"])
                if previous is not None:
                    if {k: v for k, v in previous.items() if k != "by"} != {k: v for k, v in row.items() if k != "by"}:
                        raise GuardError("ai_spend receipt identity collision")
                else:
                    missing.append(row)
            if missing:
                with target.open("ab") as handle:
                    handle.write(b"".join((json.dumps(row, sort_keys=True) + "\n").encode() for row in missing))
                    handle.flush()
                    os.fsync(handle.fileno())
                directory = os.open(target.parent, os.O_RDONLY)
                try:
                    os.fsync(directory)
                finally:
                    os.close(directory)
            return len(missing)


def process_alive(pid: int) -> bool:
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


def refuse_duplicate(pid_path: Path, done_path: Path) -> None:
    """Refuse a second runner process if a live PID is recorded, even if a stale .done exists."""
    if not pid_path.exists():
        return
    try:
        pid = int(pid_path.read_text().strip())
    except ValueError as exc:
        raise GuardError(f"unreadable pid file {pid_path}") from exc
    if process_alive(pid) and pid != os.getpid():
        raise GuardError(f"runner already live as pid {pid}; {done_path.name} will not override active owner")


def runner_state_dir() -> Path:
    return Path.home() / "_desk/state/flow/hos013-pass1"


def detached_command(script: Path, log_path: Path, done_path: Path, *,
                     repo: Path, media: Path, archive: Path, other: int,
                     ledger: Path, lock: Path, pid: Path,
                     session: str = "hos013-pass1") -> list[str]:
    """Print-only detached tmux command; never arms generation or overwrites logs."""
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
    args = [
        sys.executable,
        str(script),
        "launch-worker",
        "--repo",
        str(repo),
        "--media",
        str(media),
        "--archive",
        str(archive),
        "--other-reservations",
        str(other),
        "--ledger",
        str(ledger),
        "--lock",
        str(lock),
        "--pid",
        str(pid),
        "--log",
        str(log_path),
        "--done",
        str(done_path),
    ]
    return ["tmux", "new", "-d", "-s", session, shlex.join(args)]


def claim_pid(pid_path: Path, pid: int | None = None) -> None:
    pid_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = pid_path.with_name(pid_path.name + f".{os.getpid()}.tmp")
    immutable_bytes(temporary, (str(os.getpid() if pid is None else pid) + "\n").encode())
    os.replace(temporary, pid_path)


def launch_once(command: list[str], *, ownership: Path, pid: Path,
                log: Path, done: Path) -> int:
    """Exclusive detached runner owner: claims PID under flock before releasing gated child."""
    with WriterLock(ownership):
        refuse_duplicate(pid, done)
        if done.exists():
            raise GuardError("done file already exists; use a fresh run id")
        log.parent.mkdir(parents=True, exist_ok=True)
        done.parent.mkdir(parents=True, exist_ok=True)
        with log.open("xb") as handle:
            gate = (
                "import os,sys; token=os.read(0,1); "
                "sys.exit(125) if token != b'1' else None; "
                "os.execvp(sys.argv[1], sys.argv[1:])"
            )
            child = subprocess.Popen(
                [sys.executable, "-c", gate, *command],
                stdin=subprocess.PIPE,
                stdout=handle,
                stderr=subprocess.STDOUT,
            )
            signalled = False
            try:
                claim_pid(pid, child.pid)
                assert child.stdin is not None
                child.stdin.write(b"1")
                child.stdin.close()
                signalled = True
                code = child.wait()
            except BaseException:
                if child.stdin and not child.stdin.closed:
                    child.stdin.close()
                if not signalled:
                    child.wait(timeout=5)
                raise
        immutable_bytes(done, (str(code) + "\n").encode())
        return code


def append_ledger(path: Path, entry: dict) -> None:
    if entry.get("status") == "KEEP" or entry.get("keep") is True or entry.get("review") == "KEEP":
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


def latest_entries(entries: list[dict]) -> list[dict]:
    latest = {}
    for entry in entries:
        row_id = entry.get("row_id") or f"P{int(entry.get('part') or 0)}:{entry.get('plate_id')}"
        latest[(row_id, int(entry.get("take") or 0))] = entry
    return list(latest.values())


def _entry_row_id(entry: dict) -> str:
    return entry.get("row_id") or f"P{int(entry.get('part') or 0)}:{entry.get('plate_id')}"


def takes_recorded(entries: list[dict], row_id: str) -> set[int]:
    return {int(e.get("take") or 0) for e in entries if _entry_row_id(e) == row_id}


def refused_rows(entries: list[dict]) -> list[str]:
    """Rows whose take Flow refused under its content policy, in ledger order."""
    return [_entry_row_id(e) for e in latest_entries(entries) if e.get("status") == POLICY_REFUSED]


def policy_refusal_record(row_id: str, plate_id: str, part: int, take: int, *, reason: str, evidence: dict) -> dict:
    """Close a SUBMITTING take that Flow refused under its content policy at 0 credits."""
    if not str(reason or "").strip() or not evidence:
        raise GuardError("a policy refusal needs a reason and evidence")
    return {
        "row_id": row_id,
        "plate_id": plate_id,
        "part": part,
        "take": take,
        "status": POLICY_REFUSED,
        "file_state": "REFUSED",
        "generated": False,
        "review": "PENDING_REVIEW",
        "keep": False,
        "credits_used": 0,
        "reason": reason,
        "evidence": evidence,
        "at": now_iso(),
    }


def reconcile_policy_refusal(*, accounting_state: Path, ledger_path: Path, lock_path: Path,
                             key: str, plate_id: str, part: int, take: int,
                             reason: str, evidence: dict) -> dict:
    """Append the shared reversal and the pass ledger's FAILED_POLICY line; idempotent.

    Both ledgers only gain lines, and nothing is submitted. The pass line is skipped when the
    take's latest entry is already FAILED_POLICY, so a second run changes nothing.
    """
    row_id = f"P{int(part)}:{plate_id}"
    if key != f"{FILM_ID}:P{int(part):02d}:{plate_id}:t{int(take)}":
        raise GuardError("the shared charge id does not belong to this row and take")
    with WriterLock(lock_path), SharedFlowAccounting(accounting_state) as account:
        entries = read_ledger(ledger_path)
        latest = {(_entry_row_id(e), int(e.get("take") or 0)): e for e in entries}
        current = latest.get((row_id, take))
        if current is None or current.get("status") not in ("SUBMITTING", POLICY_REFUSED):
            raise GuardError("policy refusal applies only to a SUBMITTING take")
        if current.get("status") == "SUBMITTING" and current.get("shared_charge") not in (None, key):
            raise GuardError("the pass ledger names a different shared charge for this take")
        shared = account.reverse_policy_refusal(key, evidence=evidence)
        local = current.get("status") != POLICY_REFUSED
        if local:
            closed = policy_refusal_record(row_id, plate_id, part, take, reason=reason, evidence=evidence)
            closed["shared_charge"] = key
            append_ledger(ledger_path, closed)
            entries.append(closed)
        return {"shared_appended": shared, "pass_appended": local, "refused_rows": refused_rows(entries)}


def submitting_record(row: Row, take: int, dest: Path) -> dict:
    return {
        "row_id": row.row_id,
        "plate_id": row.plate_id,
        "part": row.part,
        "quality": row.quality,
        "flow_model": row.flow_model,
        "take": take,
        "status": "SUBMITTING",
        "file_state": "SUBMITTING",
        "generated": False,
        "review": "PENDING_REVIEW",
        "keep": False,
        "file": str(dest),
        "prompt_sha256": row.prompt_sha256,
        "credits_reserved": row.try1_credits,
        "at": now_iso(),
    }


def review_record(row: Row, take: int, dest: Path, technical: dict) -> dict:
    """Saved as GENERATED / PENDING_REVIEW, never KEEP."""
    return {
        "row_id": row.row_id,
        "plate_id": row.plate_id,
        "part": row.part,
        "quality": row.quality,
        "flow_model": row.flow_model,
        "take": take,
        "status": "PENDING_REVIEW",
        "file_state": "GENERATED",
        "generated": True,
        "review": "PENDING_REVIEW",
        "keep": False,
        "file": str(dest),
        "sha256": technical.get("sha256"),
        "prompt_sha256": row.prompt_sha256,
        "technical": technical,
        "credits_reserved": row.try1_credits,
        "credits_used": row.try1_credits,
        "at": now_iso(),
    }


def technical_report(path: Path, *, required_s: float = 8.0,
                     min_width: int = 1280, min_height: int = 720) -> dict:
    """Decode/format validation only; never implies perceptual KEEP."""
    report = {"ok": False, "review": "PENDING_REVIEW", "keep": False}
    if not path.is_file() or path.stat().st_size < 500:
        return report | {"reason": "missing or tiny"}
    report.update(sha256=sha256_file(path), bytes=path.stat().st_size)
    probe = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration:stream=codec_type,width,height",
            "-of",
            "json",
            str(path),
        ],
        capture_output=True,
        text=True,
        check=False,
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
        ["ffmpeg", "-v", "error", "-xerror", "-i", str(path), "-map", "0:v:0", "-f", "null", "-"],
        capture_output=True,
        check=False,
    )
    report.update(
        duration_s=duration,
        audio_streams=audio,
        width=width,
        height=height,
        decode_ok=decode.returncode == 0,
    )
    report["ok"] = bool(
        probe.returncode == 0
        and decode.returncode == 0
        and len(videos) == 1
        and audio == 0
        and duration >= required_s - 0.09
        and width >= min_width
        and height >= min_height
        and abs(width / max(height, 1) - 16 / 9) < 0.02
    )
    return report


def strip_audio(path: Path) -> None:
    silent = path.with_suffix(".silent.mp4")
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", str(path), "-c:v", "copy", "-an", str(silent)],
        check=True,
    )
    silent.replace(path)


def immutable_bytes(path: Path, data: bytes) -> None:
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
    src_hash = sha256_file(src)
    immutable_bytes(dest, src.read_bytes())
    dest_hash = sha256_file(dest)
    if src_hash != dest_hash:
        raise GuardError(f"hash mismatch for {dest}; archive preserved")
    evidence = {"sha256": dest_hash, "dest": str(dest), "verified": True}
    immutable_bytes(
        dest.with_suffix(dest.suffix + ".sha256.json"),
        (json.dumps(evidence, sort_keys=True) + "\n").encode(),
    )
    return evidence


def verify_nas_archive_mounted(archive_dir: Path) -> Path:
    archive = archive_dir.resolve()
    if not archive.is_dir():
        raise GuardError(f"archive directory must already exist: {archive}")
    volumes = Path("/Volumes")
    if volumes not in archive.parents:
        raise GuardError("production archive must be on the mounted NAS (/Volumes/...)")
    mount = volumes / archive.relative_to(volumes).parts[0]
    if not os.path.ismount(mount):
        raise GuardError(f"archive volume is not mounted: {mount}")
    return archive


def require_archive(archive_dir: Path | None, *, nas: bool = True) -> Path:
    if archive_dir is None:
        raise GuardError("a verified NAS archive directory is mandatory before submit")
    archive = verify_nas_archive_mounted(archive_dir) if nas else archive_dir.resolve()
    if not archive.is_dir():
        raise GuardError("archive directory must already exist")
    probe = archive / (".hos013-pass1-write-probe-" + uuid.uuid4().hex)
    immutable_bytes(probe, b"hos013 pass1 archive writable\n")
    if probe.read_bytes() != b"hos013 pass1 archive writable\n":
        raise GuardError("archive write verification failed")
    return archive


def write_receipt(path: Path, row_ids: list[str], entries: list[dict]) -> None:
    if any(e.get("keep") is True or e.get("status") == "KEEP" for e in entries):
        raise GuardError("refusing to write KEEP receipt")
    payload = {
        "film": FILM_ID,
        "rows": row_ids,
        "keep": False,
        "file_state": "GENERATED",
        "review": "PENDING_REVIEW",
        "entries": entries,
    }
    immutable_bytes(path, (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode())


def canonical_spend_ledger() -> Path:
    return Path.home() / "YouTube/orbit-with-ben/05_Analytics/ai_spend/ledger.jsonl"


def production_batch_paths(*, repo: Path, accounting_state: Path | None,
                           spend_ledger: Path | None,
                           inventory_rows: list[Row] | None) -> tuple[Path, Path]:
    state = shared_flow_state_dir()
    target = canonical_spend_ledger()
    if accounting_state is not None and Path(accounting_state).resolve() != state.resolve():
        raise GuardError("production requires canonical shared Flow accounting")
    if spend_ledger is not None and Path(spend_ledger).resolve() != target.resolve():
        raise GuardError("production requires canonical OWB spend report")
    if inventory_rows is None:
        raise GuardError(f"production requires the full locked {EXPECTED_ROW_COUNT}-row scope")
    locked = load_scope(repo)
    if inventory_rows != locked:
        raise GuardError(f"production inventory differs from the locked {EXPECTED_ROW_COUNT}-row scope")
    return state, target


def next_still_evidence_path(archive_dir: Path, still_filename: str) -> Path:
    first = archive_dir / f"{still_filename}.still.create.json"
    if not first.exists():
        return first
    attempt = 2
    while True:
        candidate = archive_dir / f"{still_filename}.still.attempt{attempt}.create.json"
        if not candidate.exists():
            return candidate
        attempt += 1


def verified_output(entry: dict) -> bool:
    if not (
        entry.get("status") == "PENDING_REVIEW"
        and entry.get("file_state") == "GENERATED"
        and entry.get("generated") is True
        and entry.get("keep") is False
        and (entry.get("technical") or {}).get("ok") is True
        and (entry.get("archive") or {}).get("verified") is True
    ):
        return False
    path = Path(entry.get("file", ""))
    archive = Path(entry["archive"].get("dest", ""))
    return (
        path.is_file()
        and archive.is_file()
        and sha256_file(path) == entry.get("sha256") == sha256_file(archive) == entry["archive"].get("sha256")
    )


def next_batch(rows: list[Row], ledger: list[dict]) -> list[Row]:
    done = {
        entry.get("row_id") or f"P{int(entry.get('part') or 0)}:{entry.get('plate_id')}"
        for entry in latest_entries(ledger)
        if verified_output(entry)
    }
    # A refused row has used its one pass-1 take. Left in, it would stop every later batch on
    # the take cap, so it is set aside here and reported by `refused_rows` for the picture review.
    refused = set(refused_rows(ledger))
    remaining = [row for row in order_rows(rows) if row.row_id not in done and row.row_id not in refused]
    if not remaining:
        return []
    return batch_rows(remaining)[0]


def execute_shared_batch(
    batch: list[Row],
    *,
    repo: Path,
    media: Path,
    ledger_path: Path,
    archive_dir: Path,
    accounting_state: Path | None = None,
    spend_ledger: Path | None = None,
    recorder: str = "gemini",
    reservation: str = DEFAULT_RESERVATION,
    other: int = 0,
    floor: int = HEADROOM_FLOOR,
    batch_price_reader=None,
    submitter=None,
    still_maker=None,
    test_archive: bool = False,
    inventory_rows: list[Row] | None = None,
) -> list[dict]:
    """Execute one guarded pass-1 batch under SharedFlowAccounting."""
    if type(other) is not int or other < 0 or type(floor) is not int or floor < 0:
        raise GuardError("invalid floor or other reservations")
    assert_batch_limits(batch)
    if not test_archive:
        accounting_state, spend_ledger = production_batch_paths(
            repo=repo,
            accounting_state=accounting_state,
            spend_ledger=spend_ledger,
            inventory_rows=inventory_rows,
        )
    if inventory_rows is not None and any(row not in inventory_rows for row in batch):
        raise GuardError(f"batch contains a row outside the locked {EXPECTED_ROW_COUNT}-row scope")

    # Refuse missing or drifted style references BEFORE opening Flow or spending anything.
    style_manifest = verify_style_references(repo, media, inventory_rows or batch, check_scope_hashes=not test_archive)
    archive_dir = require_archive(archive_dir, nas=not test_archive)
    submitter = submitter or live_video_submit
    batch_price_reader = batch_price_reader or live_batch_price_reader
    accepts_other = "other" in inspect.signature(submitter).parameters
    accepts_floor = "floor" in inspect.signature(submitter).parameters

    written: list[dict] = []
    with SharedFlowAccounting(accounting_state) as accounting:
        if spend_ledger is not None:
            accounting.export_ai_spend(spend_ledger, by=recorder)
        if accounting.snapshot()["pending"]:
            raise GuardError("unresolved shared Create; refusing batch")

        entries = read_ledger(ledger_path)
        if any(e.get("status") == "SUBMITTING" for e in latest_entries(entries)):
            raise GuardError("unresolved local SUBMITTING take; reconcile before batch")
        spent, pending, unknown, takes = ledger_totals(entries)
        if unknown:
            raise GuardError("unknown pending charge in local ledger")
        for row in batch:
            if takes.get(row.row_id, 0) >= MAX_TAKES_PER_ROW:
                raise GuardError(f"{row.row_id}: pass-1 take cap ({MAX_TAKES_PER_ROW}) already reached")
            if spent + pending + row.try1_credits > MAX_TOTAL_CREDITS:
                raise GuardError(f"{row.row_id}: batch would exceed {MAX_TOTAL_CREDITS} pass-1 cap")
            pending += row.try1_credits

        # Pre-batch live price check for Quality (100); Fast is refused.
        batch_prices = batch_price_reader()
        verified_prices = accept_batch_prices(batch_prices, now=datetime.now(timezone.utc))

        # Prepare/verify start stills for this batch's rows before any paid video Create.
        if still_maker is not None:
            for srow in batch:
                spath = still_path(media, srow.part, srow.plate_id)
                if not spath.is_file():
                    made = Path(
                        still_maker(
                            srow,
                            spath,
                            repo=repo,
                            media=media,
                            accounting=accounting,
                            reservation=reservation,
                            evidence_path=next_still_evidence_path(archive_dir, spath.name),
                            other=other,
                            floor=floor,
                        )
                    )
                    if not made.is_file():
                        raise GuardError(f"zero-price still for {srow.row_id} was not written")
                    archive_verified(made, archive_dir / made.name)

        inventory = verify_still_inventory(batch, media)
        inventory_payload = {
            "style_refs": style_manifest,
            "batch_prices": verified_prices,
            "stills": inventory,
        }
        inventory_bytes = (json.dumps(inventory_payload, sort_keys=True) + "\n").encode()
        inventory_id = sha256_bytes(inventory_bytes)
        immutable_bytes(archive_dir / f"inventory-{inventory_id}.json", inventory_bytes)
        inventory_by_row = {item["row_id"]: item for item in inventory}

        for row in batch:
            frame = still_path(media, row.part, row.plate_id)
            expected_still = inventory_by_row.get(row.row_id)
            if (
                expected_still is None
                or Path(expected_still["path"]) != frame.resolve()
                or sha256_file(frame) != expected_still["sha256"]
            ):
                raise GuardError(f"start still changed after inventory on {row.row_id}; refusing Create")

            take, dest = next_version(media, row.part, row.plate_id, takes_recorded(entries, row.row_id))
            dest.parent.mkdir(parents=True, exist_ok=True)
            charge = f"{FILM_ID}:P{row.part:02d}:{row.plate_id}:t{take}"
            intent = submitting_record(row, take, dest)
            intent["shared_charge"] = charge
            intent["inventory"] = inventory_id
            intent["input"] = {"file": str(frame.resolve()), "sha256": expected_still["sha256"]}
            append_ledger(ledger_path, intent)

            submit_kwargs = dict(
                accounting=accounting,
                reservation=reservation,
                charge=charge,
                evidence_path=archive_dir / (dest.name + ".create.json"),
            )
            if accepts_other:
                submit_kwargs["other"] = other
            if accepts_floor:
                submit_kwargs["floor"] = floor

            try:
                evidence = submitter(row, dest, frame, **submit_kwargs)
            finally:
                if spend_ledger is not None:
                    accounting.export_ai_spend(spend_ledger, by=recorder)

            shared = accounting.snapshot()["charges"].get(charge)
            if not shared or shared["status"] != "CHARGED" or shared["amount"] != row.try1_credits:
                raise GuardError(f"submitter returned without exact {row.try1_credits}-credit shared charge")
            if not isinstance(evidence, dict) or evidence.get("charge") != charge:
                raise GuardError("submitter returned without matching per-Create evidence")
            if not dest.is_file():
                raise GuardError("charged output missing; reconcile before retry")

            strip_audio(dest)
            technical = technical_report(dest, required_s=max(float(REQUIRED_CLIP_S), row.use_s))
            entry = review_record(row, take, dest, technical)
            entry.update(
                shared_charge=charge,
                create_evidence=evidence,
                batch_prices=verified_prices,
                inventory=inventory_id,
                input=intent["input"],
                archive=archive_verified(dest, archive_dir / dest.name),
            )
            if not technical["ok"]:
                entry["status"] = "FAILED"
                entry["file_state"] = "FAILED_TECHNICAL"
            write_receipt(archive_dir / (dest.name + ".receipt.json"), [row.row_id], [entry])
            append_ledger(ledger_path, entry)
            entries.append(entry)
            written.append(entry)
            if not technical["ok"]:
                raise GuardError(f"technical validation failed on {row.row_id}: {dest}; stopping batch")

    batch_ids = [r.row_id for r in batch]
    batch_tag = sha256_bytes(",".join(batch_ids).encode("utf-8"))[:12]
    write_receipt(archive_dir / f"batch-{batch_tag}.receipt.json", batch_ids, written)
    return written


def open_flow_page(browser, flow_home: str, goto):
    """Reuse the open Flow tab via cdp_tabs.reuse_page; never spawn duplicate Flow tabs."""
    owb = Path(os.environ.get("OWB_REPO", str(Path.home() / "YouTube/orbit-with-ben")))
    sys.path.insert(0, str(owb / "scripts"))
    from cdp_tabs import reuse_page

    page = reuse_page(browser.contexts[0], FLOW_HOST)
    url = page.url or ""
    if FLOW_HOST in url and "/about" not in url:
        return page
    goto(page, flow_home)
    return page


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
    """Read and validate the studio Ultra account + Flow credit balance in its own step."""
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
        if not isinstance(evidence, dict) or evidence.get("host") != FLOW_HOST or evidence.get("ultra") is not True:
            raise GuardError("live Flow host or ULTRA entitlement is missing or changed")
        verify_account_list(evidence.get("accounts"))
        balances = evidence.get("balances")
        if not isinstance(balances, list) or len(balances) != 1 or type(balances[0]) is not int or balances[0] < 0:
            raise GuardError("live Flow balance is missing or ambiguous")
        allowed_keys = {"host", "accounts", "ultra", "balances"}
        extra_keys = set(evidence) - allowed_keys
        if extra_keys and extra_keys not in (
            {"models", "outputs", "aspects", "durations", "prices", "create_count"},
            {"models", "outputs", "aspects", "prices", "create_count"},
        ):
            raise GuardError("unknown live Flow balance evidence schema")
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


# Synchronous DOM check + trusted CDP mouse target resolution (never untrusted element.click()).
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
    balances = raw.get("balances")
    if not isinstance(balances, list):
        raise GuardError("live Flow balance is missing or ambiguous")
    if len(balances) == 0 and balance is not None:
        if type(balance) is not int or balance < 0:
            raise GuardError("live Flow balance is missing or ambiguous")
        return [balance]
    if len(balances) == 1 and type(balances[0]) is int and balances[0] >= 0:
        if balance is not None and (type(balance) is not int or balances[0] != balance):
            raise GuardError("live Flow balance is missing or ambiguous")
        return list(balances)
    raise GuardError("live Flow balance is missing or ambiguous")


def _scrub_evidence_accounts(raw: dict, balances: list[int], account_digest: str) -> dict:
    clean = {k: v for k, v in raw.items() if k != "accounts"}
    clean["balances"] = balances
    clean["account_sha256"] = account_digest
    clean["account_verified"] = True
    return clean


def _read_and_validate_live_evidence(page, *, quality: str = "Quality",
                                     balance: int | None = None,
                                     open_overlay: bool = False,
                                     require_enabled_create: bool = True) -> tuple[dict, dict]:
    expected_model = expected_model_for(quality)
    expected_cost = expected_credits_for(quality)
    raw = page.evaluate(CREATE_EVIDENCE_JS, None)
    if (
        open_overlay
        and isinstance(raw, dict)
        and not raw.get("models")
        and not raw.get("prices")
        and _open_settings_trigger_if_needed(page)
    ):
        raw = page.evaluate(CREATE_EVIDENCE_JS, None)
    if not isinstance(raw, dict):
        raise GuardError("live Flow evidence is not an object")
    expected_keys = {
        "host",
        "models",
        "outputs",
        "aspects",
        "durations",
        "accounts",
        "prices",
        "balances",
        "ultra",
        "create_count",
    }
    if set(raw) != expected_keys:
        raise GuardError("unknown live Flow evidence schema")
    account_digest = verify_account_list(raw.get("accounts"))
    required = dict(
        host=FLOW_HOST,
        models=[expected_model],
        outputs=[REQUIRED_OUTPUTS],
        aspects=[REQUIRED_ASPECT],
        durations=[REQUIRED_DURATION],
        prices=[f"Generating will use {expected_cost} credits"],
        ultra=True,
    )
    if any(raw.get(k) != v for k, v in required.items()):
        raise GuardError(
            f"live Flow selected controls/entitlement/price do not match {quality} ({expected_model}, {expected_cost} credits)"
        )
    if require_enabled_create and raw.get("create_count") != 1:
        raise GuardError("live Flow Create button is missing, disabled or ambiguous")
    balances = _resolve_evidence_balances(raw, balance)
    return raw, _scrub_evidence_accounts(raw, balances, account_digest)


def read_live_evidence(page, *, quality: str = "Quality", balance: int | None = None,
                       open_overlay: bool = False) -> dict:
    """Validate selected-state DOM evidence for Quality (100) or Fast (10) 8s 16:9 x1."""
    _raw, evidence = _read_and_validate_live_evidence(
        page, quality=quality, balance=balance, open_overlay=open_overlay
    )
    return evidence


def _extract_trusted_click_target(target: object) -> tuple[float, float] | None:
    if not isinstance(target, dict):
        return None
    x, y = target.get("x"), target.get("y")
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


def guarded_create(page, accounting: SharedFlowAccounting, *, row: Row,
                   reservation: str, charge: str, evidence_path: Path,
                   floor: int = HEADROOM_FLOOR, balance: int | None = None) -> dict:
    """Atomic per-row Create guard: validates row's exact model/price, logs intent, then trusted mouse clicks."""
    accounting._assert_held()
    expected_cost = expected_credits_for(row)
    if row.try1_credits != expected_cost:
        raise GuardError(f"row {row.row_id} cost {row.try1_credits} != {expected_cost}")
    raw, evidence = _read_and_validate_live_evidence(page, quality=row.quality, balance=balance)
    record = dict(
        read_at=now_iso(),
        row_id=row.row_id,
        quality=row.quality,
        credits=expected_cost,
        ui=evidence,
        charge=charge,
        reservation=reservation,
    )
    immutable_bytes(evidence_path, (json.dumps(record, sort_keys=True) + "\n").encode())
    accounting.intent(charge, reservation, expected_cost, live=evidence["balances"][0], floor=floor)
    outcome = page.evaluate(CREATE_EVIDENCE_JS, raw)
    if not isinstance(outcome, dict) or type(outcome.get("ready")) is not bool:
        raise GuardError("ambiguous Create precheck outcome; shared charge remains pending")
    if not outcome["ready"]:
        accounting.resolve(
            charge,
            submitted=False,
            evidence=dict(reason=outcome.get("reason"), read_at=record["read_at"]),
        )
        raise GuardError("live UI drift before Create; no submission")
    coords = _extract_trusted_click_target(outcome.get("target"))
    mouse = getattr(page, "mouse", None)
    if coords is None or mouse is None or not callable(getattr(mouse, "click", None)):
        accounting.resolve(
            charge,
            submitted=False,
            evidence=dict(reason="missing trusted click target or mouse adapter", read_at=record["read_at"]),
        )
        raise GuardError("missing trusted Create click target or mouse adapter; no submission")
    mouse.click(coords[0], coords[1])
    accounting.resolve(
        charge,
        submitted=True,
        evidence=dict(ui=evidence, target=dict(x=coords[0], y=coords[1]), read_at=record["read_at"]),
    )
    return record


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
        and not raw.get("models")
        and not raw.get("prices")
        and _open_settings_trigger_if_needed(page)
    ):
        raw = page.evaluate(STILL_EVIDENCE_JS, None)
    if not isinstance(raw, dict):
        raise GuardError("live Flow still evidence is not an object")
    expected_keys = {
        "host",
        "models",
        "outputs",
        "aspects",
        "accounts",
        "prices",
        "balances",
        "ultra",
        "create_count",
    }
    if set(raw) != expected_keys:
        raise GuardError("unknown live Flow still evidence schema")
    account_digest = verify_account_list(raw.get("accounts"))
    required = dict(
        host=FLOW_HOST,
        models=[REQUIRED_STILL_MODEL],
        outputs=[REQUIRED_OUTPUTS],
        aspects=[REQUIRED_ASPECT],
        prices=["Generating will use 0 credits"],
        ultra=True,
        create_count=1,
    )
    if any(raw.get(k) != v for k, v in required.items()):
        raise GuardError("live Flow still selected controls/entitlement/zero-price are missing or changed")
    balances = _resolve_evidence_balances(raw, balance)
    return raw, _scrub_evidence_accounts(raw, balances, account_digest)


def read_live_still_evidence(page, *, balance: int | None = None, open_overlay: bool = False) -> dict:
    _raw, evidence = _read_and_validate_live_still_evidence(page, balance=balance, open_overlay=open_overlay)
    return evidence


def guarded_still_create(page, accounting: SharedFlowAccounting, *, reservation: str,
                         row: Row, evidence_path: Path, floor: int = HEADROOM_FLOOR,
                         balance: int | None = None) -> dict:
    accounting._assert_held()
    state = accounting.snapshot()
    raw, evidence = _read_and_validate_live_still_evidence(page, balance=balance)
    if state["pending"] or evidence["balances"][0] - state["liability"] < floor:
        raise GuardError("pending charge or insufficient shared Flow headroom for still")
    record = dict(
        read_at=now_iso(),
        row_id=row.row_id,
        plate_id=row.plate_id,
        ui=evidence,
        reservation=reservation,
        credits=0,
    )
    immutable_bytes(evidence_path, (json.dumps(record, sort_keys=True) + "\n").encode())
    outcome = page.evaluate(STILL_EVIDENCE_JS, raw)
    if not isinstance(outcome, dict) or type(outcome.get("ready")) is not bool:
        raise GuardError("ambiguous still Create precheck outcome; stopping before video generation")
    if not outcome["ready"]:
        raise GuardError("live UI drift before still Create; no submission")
    coords = _extract_trusted_click_target(outcome.get("target"))
    mouse = getattr(page, "mouse", None)
    if coords is None or mouse is None or not callable(getattr(mouse, "click", None)):
        raise GuardError("missing trusted still Create click target or mouse adapter; no submission")
    mouse.click(coords[0], coords[1])
    return record


def read_live_batch_prices_on_page(page, *, configure_model) -> dict[str, PriceEvidence]:
    """Read live Quality (100) price on Flow without clicking Create."""
    live_balance = read_live_balance(page)
    out: dict[str, PriceEvidence] = {}
    for quality in ("Quality",):
        model = expected_model_for(quality)
        configure_model(page, model)
        _raw, evidence = _read_and_validate_live_evidence(
            page,
            quality=quality,
            balance=live_balance,
            open_overlay=True,
            require_enabled_create=False,
        )
        _close_flow_overlays(page)
        price_line = evidence["prices"][0]
        credits = int(GENERATE_LINE_RE.match(price_line).group(1))
        out[quality] = PriceEvidence(
            quality=quality,
            model=evidence["models"][0],
            outputs=evidence["outputs"][0],
            aspect=evidence["aspects"][0],
            duration=evidence["durations"][0],
            credits=credits,
            generate_line=price_line,
            read_at=now_iso(),
        )
    accept_batch_prices(out, now=datetime.now(timezone.utc))
    return out


def live_batch_price_reader() -> dict[str, PriceEvidence]:
    """Live pre-batch price reader via CDP :9222. Unreachable unless submit is armed."""
    if os.environ.get(SUBMIT_ENV) != "1":
        raise GuardError("live batch price reader is not armed")
    repo = repo_root_from()
    sys.path.insert(0, str(repo / "04_Audio/tools"))
    import orbit_flow_veo_ui as flow
    from playwright.sync_api import sync_playwright

    cdp = os.environ.get("ORBIT_FLOW_CDP", "http://127.0.0.1:9222")
    with sync_playwright() as playwright:
        browser = playwright.chromium.connect_over_cdp(cdp)
        page = open_flow_page(
            browser,
            flow.FLOW_HOME,
            lambda current, url: current.goto(url, wait_until="domcontentloaded", timeout=120_000),
        )
        if "/project/" not in (page.url or ""):
            flow.ensure_project(page)
        return read_live_batch_prices_on_page(
            page,
            configure_model=lambda p, m: flow.configure_veo_settings(
                p, model=m, frames_mode=True, ingredients_mode=False
            ),
        )


def still_prompt_for_row(still_tool, row: Row) -> str:
    core = " ".join(row.prompt.split())
    if row.explorer:
        core = core.replace("No Explorer.", "") + " " + EXPLORER_LOCK
    return still_tool.still_prompt(
        "History of Science locked look: premium Animistry-class 3D cartoon, finished materials, warm cinematic period light.",
        core + " Opening frame only. No readable words, numbers, letters or text anywhere.",
    )


def video_prompt_for_row(row: Row) -> str:
    core = " ".join(row.prompt.split())
    if row.explorer:
        core = core.replace("No Explorer.", "") + " " + EXPLORER_LOCK
    return (
        "Animate the attached start frame; keep its exact cartoon look, objects and light. "
        + core
        + " Silent picture only. Continuous real camera and subject motion through the final frame."
        + " No readable handwriting, letters or numbers anywhere."
    )


def live_still_maker(row: Row, dest: Path, *, repo: Path, media: Path,
                     accounting: SharedFlowAccounting | None = None,
                     reservation: str = DEFAULT_RESERVATION,
                     evidence_path: Path | None = None,
                     other: int = 0, floor: int = HEADROOM_FLOOR) -> Path:
    """Zero-credit start still maker under SharedFlowAccounting."""
    if os.environ.get(SUBMIT_ENV) != "1":
        raise GuardError(f"live still generation is not armed for {row.row_id}")
    if type(other) is not int or other < 0 or type(floor) is not int or floor < 0:
        raise GuardError("invalid floor or other reservations")
    if accounting is None or evidence_path is None:
        raise GuardError(f"still generation for {row.row_id} requires SharedFlowAccounting and evidence_path")
    accounting._assert_held()

    verified_refs = verify_style_references(repo, media, [row])
    style_paths = [Path(item["path"]) for item in verified_refs["house"]]
    if row.explorer and verified_refs["explorer"] is not None:
        style_paths.append(Path(verified_refs["explorer"]["path"]))

    sys.path.insert(0, str(repo / "04_Audio/tools"))
    sys.path.insert(0, str(repo / "02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project"))
    import orbit_flow_veo_ui as flow
    import _flow_still_v01 as still_tool
    from playwright.sync_api import sync_playwright

    cdp = os.environ.get("ORBIT_FLOW_CDP", "http://127.0.0.1:9222")
    effective_floor = floor + other
    prompt = still_prompt_for_row(still_tool, row)

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
            accounting.reserve(reservation, FILM_ID, MAX_TOTAL_CREDITS, live=ui["balances"][0], floor=effective_floor)
            evidence.update(
                guarded_still_create(
                    configured_page,
                    accounting,
                    reservation=reservation,
                    row=row,
                    evidence_path=evidence_path,
                    floor=effective_floor,
                    balance=live_balance,
                )
            )

        still_tool.make_still(
            page,
            prompt,
            dest,
            timeout_s=300,
            create_guard=create_guard,
            style_refs=style_paths,
            media_root=media,
        )
        after_balance = read_live_balance(page)
        if after_balance < evidence["ui"]["balances"][0]:
            raise GuardError(f"zero-price still reduced Flow balance on {row.row_id}")

    if not dest.is_file():
        raise GuardError(f"zero-price still for {row.row_id} was not written")
    immutable_bytes(dest.with_suffix(".sha256"), (sha256_file(dest) + "\n").encode())
    return dest


def live_video_submit(row: Row, dest: Path, frame: Path, *,
                      accounting: SharedFlowAccounting, reservation: str,
                      charge: str, evidence_path: Path, other: int = 0,
                      floor: int = HEADROOM_FLOOR) -> dict:
    """Real Flow video submission. Unreachable unless HOS013_PASS1_SUBMIT=1."""
    if os.environ.get(SUBMIT_ENV) != "1":
        raise GuardError("live submit is not armed")
    if type(other) is not int or other < 0 or type(floor) is not int or floor < 0:
        raise GuardError("invalid floor or other reservations")
    accounting._assert_held()
    repo = repo_root_from()
    sys.path.insert(0, str(repo / "04_Audio/tools"))
    import orbit_flow_veo_ui as flow
    from playwright.sync_api import sync_playwright

    model = expected_model_for(row)
    os.environ["ORBIT_FLOW_VEO_MODEL"] = model
    prompt = video_prompt_for_row(row)
    cdp = os.environ.get("ORBIT_FLOW_CDP", "http://127.0.0.1:9222")
    effective_floor = floor + other

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
            ui = read_live_evidence(configured_page, quality=row.quality, balance=live_balance, open_overlay=True)
            accounting.reserve(reservation, FILM_ID, MAX_TOTAL_CREDITS, live=ui["balances"][0], floor=effective_floor)
            evidence.update(
                guarded_create(
                    configured_page,
                    accounting,
                    row=row,
                    reservation=reservation,
                    charge=charge,
                    evidence_path=evidence_path,
                    floor=effective_floor,
                    balance=live_balance,
                )
            )

        flow.generate_clip(
            page,
            prompt,
            dest,
            model=model,
            timeout_s=700,
            start_frame=frame,
            attempts=1,
            reuse_project=False,
            create_guard=create_guard,
        )
        before_balance = evidence["ui"]["balances"][0]
        after_balance = read_live_balance(page)
        delta = before_balance - after_balance
        expected_cost = expected_credits_for(row)
        if delta > expected_cost:
            raise GuardError(
                f"Flow balance dropped by {delta} credits (> expected {expected_cost}) on {row.row_id}"
            )
        if delta == expected_cost:
            accounting.reconcile_posted(
                charge,
                evidence=dict(
                    before=before_balance,
                    after=after_balance,
                    delta=delta,
                    reconciled_at=now_iso(),
                ),
            )
    return evidence


def latest_recorded_flow_balance(spend_ledger: Path | None = None) -> dict | None:
    target = spend_ledger or canonical_spend_ledger()
    if not target.is_file():
        return None
    latest = None
    for line in target.read_text().splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        left = row.get("left")
        if (
            row.get("pool") == "flow"
            and row.get("kind") == "record"
            and isinstance(left, (int, float))
            and not isinstance(left, bool)
            and float(left).is_integer()
        ):
            # Intentionally omit free-text `note` so legacy personal emails in ledger notes never leak into dry-run reports.
            latest = {"left": int(left), "at": row.get("at"), "by": row.get("by", "")}
    return latest


def build_dry_run_report(repo: Path, *, media: Path, archive_dir: Path,
                         other: int = 0, floor: int = HEADROOM_FLOOR,
                         accounting_state: Path | None = None,
                         spend_ledger: Path | None = None) -> dict:
    """Zero-browser, zero-spend dry-run verification of scope, style refs, NAS archive, and accounting."""
    rows = load_scope(repo)
    plan = build_plan(rows, repo=repo)
    style_refs = verify_style_references(repo, media, rows)
    archive = verify_nas_archive_mounted(archive_dir)
    shared = SharedFlowAccounting.peek_readonly(accounting_state)
    recorded = latest_recorded_flow_balance(spend_ledger)
    balance_left = recorded["left"] if recorded else None
    liability = shared["liability"]
    projected_after_013 = (
        balance_left - liability - other - MAX_TOTAL_CREDITS if balance_left is not None else None
    )
    active_reservations = {
        key: {"film": val["film"], "cap": val["cap"]}
        for key, val in shared["reservations"].items()
        if val["active"]
    }
    return {
        "job": "J2499",
        "film": FILM_ID,
        "generated_at": now_iso(),
        "mode": "dry-run (no browser, no Create click, 0 submissions, 0 credits spent)",
        "submissions": 0,
        "create_clicks": 0,
        "credits_spent": 0,
        "keep": False,
        "submit_armed": submit_armed(),
        "scope_verified": {
            "rows": plan["row_count"],
            "Quality": plan["quality_count"],
            "Fast": plan["fast_count"],
            "explorer": plan["explorer_count"],
            "total_try1_credits": MAX_TOTAL_CREDITS,
            "max_takes_per_row": MAX_TAKES_PER_ROW,
            "batch_count": len(plan["batches"]),
            "max_batch_rows": MAX_BATCH_ROWS,
            "max_batch_credits": MAX_BATCH_CREDITS,
            "first_row": plan["order"][0]["row_id"],
            "last_row": plan["order"][-1]["row_id"],
        },
        "style_refs_verified": style_refs,
        "nas_archive_verified": {
            "path": str(archive),
            "mounted_under_volumes": True,
        },
        "shared_accounting_readonly": {
            "active_reservations": active_reservations,
            "unposted_charges": shared["unposted"],
            "remaining_reservations": shared["remaining_reservations"],
            "total_liability": liability,
            "has_pending_charge": shared["pending"],
            "other_reservations_arg": other,
            "floor": floor,
            "latest_recorded_flow_balance": recorded,
            "projected_headroom_after_013_cap": projected_after_013,
            "would_allow_reserve_at_recorded_balance": (
                bool(not shared["pending"] and projected_after_013 is not None and projected_after_013 >= floor)
            ),
        },
        "per_part": plan["per_part"],
        "batches": plan["batches"],
    }


def cmd_plan(repo: Path, out: Path | None) -> dict:
    plan = build_plan(load_scope(repo), repo=repo)
    if plan["submissions"] != 0 or plan["create_clicks"] != 0 or plan["keep"] is not False:
        raise GuardError("plan tried to submit or keep")
    text = json.dumps(plan, indent=2) + "\n"
    if out is not None:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text)
    else:
        sys.stdout.write(text)
    return plan


def cmd_dry_run(repo: Path, *, media: Path, archive_dir: Path, other: int,
                floor: int, out: Path | None) -> dict:
    report = build_dry_run_report(repo, media=media, archive_dir=archive_dir, other=other, floor=floor)
    if report["submissions"] != 0 or report["create_clicks"] != 0 or report["keep"] is not False:
        raise GuardError("dry-run tried to submit or keep")
    text = json.dumps(report, indent=2) + "\n"
    if out is not None:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text)
    else:
        sys.stdout.write(text)
    return report


def submit_armed(env: dict | None = None) -> bool:
    return (env if env is not None else os.environ).get(SUBMIT_ENV) == "1"


def cmd_submit(
    repo: Path,
    *,
    other: int,
    floor: int = HEADROOM_FLOOR,
    reservation: str = DEFAULT_RESERVATION,
    media: Path,
    ledger_path: Path,
    lock_path: Path,
    pid_path: Path,
    done_path: Path,
    archive_dir: Path | None,
    accounting_state: Path | None = None,
    spend_ledger: Path | None = None,
    recorder: str = "gemini",
    batch_price_reader=None,
    submitter=None,
    still_maker=None,
    test_archive: bool = False,
) -> list[dict]:
    """Run one guarded pass-1 batch when explicitly armed via HOS013_PASS1_SUBMIT=1."""
    if not submit_armed():
        raise SystemExit(
            "refusing submit: generation is not armed "
            f"({SUBMIT_ENV} is not 1). Dry-run / plan only until Chief reviews the guards and queues the mint."
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
            repo=repo,
            media=media,
            ledger_path=ledger_path,
            archive_dir=archive_dir,
            accounting_state=accounting_state,
            spend_ledger=spend_ledger,
            recorder=recorder,
            reservation=reservation,
            other=other,
            floor=floor,
            batch_price_reader=batch_price_reader,
            submitter=submitter,
            still_maker=still_maker or live_still_maker,
            test_archive=test_archive,
            inventory_rows=rows,
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="HOS 013 Darwin & Wallace pass-1 Flow mint runner (J2499)")
    sub = parser.add_subparsers(dest="cmd", required=True)

    plan_p = sub.add_parser("plan", help="write the 71-row mint order and 15 batches; submit nothing")
    plan_p.add_argument("--repo")
    plan_p.add_argument("--out")

    dry_p = sub.add_parser("dry-run", help="verify scope, hashes, style refs, NAS archive and shared ledger; submit nothing")
    dry_p.add_argument("--repo")
    dry_p.add_argument("--media", default=str(DEFAULT_NAS_MEDIA))
    dry_p.add_argument(
        "--archive",
        default=str(DEFAULT_NAS_MEDIA / "04_Generated-Clips/archive_v01_pass1"),
    )
    dry_p.add_argument("--other-reservations", type=int, default=0)
    dry_p.add_argument("--floor", type=int, default=HEADROOM_FLOOR)
    dry_p.add_argument("--out")

    submit_p = sub.add_parser("submit", help=f"refused unless {SUBMIT_ENV}=1")
    submit_p.add_argument("--repo")
    submit_p.add_argument("--media", required=False)
    submit_p.add_argument("--archive", required=False)
    submit_p.add_argument("--other-reservations", type=int, required=False)
    submit_p.add_argument("--floor", type=int, default=HEADROOM_FLOOR)
    submit_p.add_argument("--reservation", default=DEFAULT_RESERVATION)
    submit_p.add_argument("--recorder", default="gemini")
    submit_p.add_argument("--ledger", required=False)
    submit_p.add_argument("--lock", required=False)
    submit_p.add_argument("--pid", required=False)
    submit_p.add_argument("--done", required=False)

    state = runner_state_dir()
    for name, help_text in (
        ("detach-command", "print a tmux launch command; start nothing"),
        ("launch-worker", "exclusive detached process owner"),
    ):
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

    refusal = sub.add_parser("reconcile-policy-refusal",
                             help="close a take Flow refused under its content policy at 0 credits; submits nothing")
    refusal.add_argument("--key", required=True, help="shared charge id, e.g. HOS:013:P01:07_darwin_1837_desk:t1")
    refusal.add_argument("--plate", required=True)
    refusal.add_argument("--part", type=int, required=True)
    refusal.add_argument("--take", type=int, default=1)
    refusal.add_argument("--reason", required=True)
    refusal.add_argument("--evidence", required=True, help="JSON file: the Chief ruling and the balance arithmetic")
    refusal.add_argument("--accounting-state", default=None)
    refusal.add_argument("--ledger", default=None)
    refusal.add_argument("--lock", default=None)

    args = parser.parse_args(argv)
    if args.cmd == "reconcile-policy-refusal":
        evidence = json.loads(Path(args.evidence).read_text())
        result = reconcile_policy_refusal(
            accounting_state=Path(args.accounting_state) if args.accounting_state else shared_flow_state_dir(),
            ledger_path=Path(args.ledger) if args.ledger else state / "ledger.jsonl",
            lock_path=Path(args.lock) if args.lock else state / "writer.lock",
            key=args.key, plate_id=args.plate, part=args.part, take=args.take,
            reason=args.reason, evidence=evidence)
        sys.stdout.write(json.dumps(result, sort_keys=True) + "\n")
        return 0
    if args.cmd == "plan":
        repo = Path(args.repo) if args.repo else repo_root_from()
        cmd_plan(repo, Path(args.out) if args.out else None)
        return 0
    if args.cmd == "dry-run":
        repo = Path(args.repo) if args.repo else repo_root_from()
        cmd_dry_run(
            repo,
            media=Path(args.media),
            archive_dir=Path(args.archive),
            other=args.other_reservations,
            floor=args.floor,
            out=Path(args.out) if args.out else None,
        )
        return 0
    if args.cmd in ("detach-command", "launch-worker"):
        command = detached_command(
            Path(__file__).resolve(),
            Path(args.log),
            Path(args.done),
            repo=Path(args.repo),
            media=Path(args.media),
            archive=Path(args.archive),
            other=args.other_reservations,
            ledger=Path(args.ledger),
            lock=Path(args.lock),
            pid=Path(args.pid),
        )
        load_scope(Path(args.repo))
        if args.cmd == "detach-command":
            sys.stdout.write(json.dumps(command) + "\n")
            return 0
        if Path(args.pid).resolve() != (state / "runner.pid").resolve():
            raise GuardError("launch-worker requires the canonical runner pid path")
        child_args = shlex.split(command[-1])
        child_args[2] = "submit"
        log_index = child_args.index("--log")
        del child_args[log_index : log_index + 2]
        return launch_once(
            child_args,
            ownership=state / "runner.lock",
            pid=Path(args.pid),
            log=Path(args.log),
            done=Path(args.done),
        )
    if not submit_armed():
        raise SystemExit(
            "refusing submit: generation is not armed "
            f"({SUBMIT_ENV} is not 1). Dry-run / plan only until Chief reviews the guards and queues the mint."
        )
    if args.other_reservations is None or not args.media:
        raise GuardError("armed submit needs --other-reservations and --media")
    repo = Path(args.repo) if args.repo else repo_root_from()
    cmd_submit(
        repo,
        other=args.other_reservations,
        floor=args.floor,
        reservation=args.reservation,
        media=Path(args.media),
        ledger_path=Path(args.ledger) if args.ledger else state / "ledger.jsonl",
        lock_path=Path(args.lock) if args.lock else state / "writer.lock",
        pid_path=Path(args.pid) if args.pid else state / "runner.pid",
        done_path=Path(args.done) if args.done else state / "runner.done",
        archive_dir=Path(args.archive) if args.archive else None,
        recorder=args.recorder,
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except GuardError as exc:
        print(f"STOP {exc}", file=sys.stderr)
        raise SystemExit(2)
