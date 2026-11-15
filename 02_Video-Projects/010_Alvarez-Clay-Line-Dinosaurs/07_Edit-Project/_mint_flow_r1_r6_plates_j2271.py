#!/usr/bin/env python3
"""HOS 010 Alvarez clay line R1-R6 Short replacement-plate Flow adapter (J2271 / desk 6893169788 / 6893259531).

Consumes ONLY the bounded 6-plate replacement scope in
`02_Video-Projects/010_Alvarez-Clay-Line-Dinosaurs/10_Shorts/R1_R6_REPLACEMENT_SCOPE_J2271.json`
(`R1`..`R6`, 100 Flow credits each, 600 credits total) cross-verified against
`10_Shorts/J2271_TWELVE_PLATE_REVIEW_v01.json`.

Satisfies Check 4 of Chief ruling `6893169788` / `6893259531`:
- Lists exactly six rows (`R1`..`R6`) at 100 credits each (`600` total).
- Assigns one named 100-credit charge per row (`HOS:010:R1:P02:05_almost_none:t2` .. `HOS:010:R6:P05:09_robin:t2`).
- Uses a new reservation id `HOS010_R1_R6_PLATES_J2271` (`cap=600`) and refuses released `HOS010_TWELVE_PLATES_J2270`.
- Enforces the 3,000-credit live-balance floor through `SharedFlowAccounting` without hand-editing `account.jsonl`.
- Default commands (`plan`, `dry-run`) never open Chrome/CDP, never click Create, never modify NAS media, and spend 0 credits (£0).
- `submit` is interlocked behind BOTH `HOS010_R1_R6_PLATES_SUBMIT=1` AND the signed Chief authorization file for desk go `6898337122` (scope hash pin, cap 600). Flipping `generation_authorized` in the committed scope is not enough.
- The Create click is `guarded_create` from the twelve-plate adapter. This file does not invent a second clicker, does not load the twelve-plate scope, and does not reuse `HOS010_TWELVE_PLATES_J2270`.
- Before each batch the shared writer lock is held, the live Flow balance is read, and any cash prompt or unusual-activity banner stops the run before Create.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import _mint_flow_twelve_plates_j2268 as base  # noqa: E402
from _mint_flow_twelve_plates_j2268 import (  # noqa: E402
    CANONICAL_HOUSE_STYLE_REFS,
    DEFAULT_NAS_MEDIA,
    EXPLORER_REF_REL,
    FILM_ID,
    GuardError,
    HEADROOM_FLOOR,
    REQUIRED_ASPECT,
    REQUIRED_DURATION,
    REQUIRED_MODEL,
    REQUIRED_OUTPUTS,
    REQUIRED_QUALITY,
    REQUIRED_STILL_MODEL,
    SharedFlowAccounting,
    latest_recorded_flow_balance,
    now_iso,
    repo_root_from,
    resolve_external_reservations,
    sha256_file,
    verify_explorer_reference,
    verify_nas_archive_mounted,
    verify_nas_volume_mounted,
    verify_style_references,
    verify_vo_and_option_a1,
)

JOB_ID = "J2271"
SCOPE_REL = Path("02_Video-Projects/010_Alvarez-Clay-Line-Dinosaurs/10_Shorts/R1_R6_REPLACEMENT_SCOPE_J2271.json")
REVIEW_REL = Path("02_Video-Projects/010_Alvarez-Clay-Line-Dinosaurs/10_Shorts/J2271_TWELVE_PLATE_REVIEW_v01.json")
SUBMIT_ENV = "HOS010_R1_R6_PLATES_SUBMIT"
DEFAULT_RESERVATION = "HOS010_R1_R6_PLATES_J2271"
FORBIDDEN_RESERVATIONS = ("HOS010_TWELVE_PLATES_J2270",)

EXPECTED_REPAIR_IDS = ("R1", "R2", "R3", "R4", "R5", "R6")
EXPECTED_ROW_IDS = (
    "P2:05_almost_none",
    "P4:06_dust_veil",
    "P5:08_all_at_once",
    "P5:12_clay_callback",
    "P5:10_explorer_robin",
    "P5:09_robin",
)
EXPECTED_NAMED_CHARGES = (
    "HOS:010:R1:P02:05_almost_none:t2",
    "HOS:010:R2:P04:06_dust_veil:t2",
    "HOS:010:R3:P05:08_all_at_once:t2",
    "HOS:010:R4:P05:12_clay_callback:t2",
    "HOS:010:R5:P05:10_explorer_robin:t2",
    "HOS:010:R6:P05:09_robin:t2",
)
CREDITS_PER_ROW = 100
MAX_TAKES_PER_ROW = 1
TOTAL_CAP_CREDITS = 600
MAX_BATCH_ROWS = 5
MAX_BATCH_CREDITS = 500
GO_COMMENT = "6898337122"
MIN_DISK_FREE_BYTES = 10 * 1024**3
OUTPUT_DIR_NAME = "v02_r1_r6_plates"

# A buy / top-up / card dialog. Ordinary "N credits" and "Generating will use 100 credits" do not match.
CASH_PROMPT_RE = re.compile(
    r"(?i)(?:"
    r"\bbuy(?:\s+more)?\s+credits\b|"
    r"\bget\s+more\s+credits\b|"
    r"\bextra\s+credits?\b|"
    r"\bpaid\s+tier\b|"
    r"\btop[\s-]?up\b|"
    r"\bupgrade\s+(?:your\s+)?(?:plan|account|to\s+(?:ultra|pro))\b|"
    r"\badd(?:\s+a)?\s+payment\b|"
    r"\bpurchase\s+credits\b|"
    r"\bout\s+of\s+(?:ai\s+|flow\s+)?credits\b|"
    r"\bpayment\s+(?:method|required|failed)\b|"
    r"\bbilling\s+(?:account|details|info)\b|"
    r"\benter\s+(?:your\s+)?card\b"
    r")"
)
UNUSUAL_RE = re.compile(
    r"(?i)(?:"
    r"unusual activity|suspicious activity|verify it.?s you|"
    r"confirm you.?re not a robot|too many (?:requests|attempts)|unusual traffic|"
    r"couldn.?t verify|(?<!re)captcha|are you a robot"
    r")"
)


def submit_armed(env: dict | None = None) -> bool:
    return (env if env is not None else os.environ).get(SUBMIT_ENV) == "1"


def load_r1_r6_scope(repo: Path) -> tuple[dict, list[dict]]:
    """Load and cross-verify the 6 R1-R6 replacement rows and their named 100-credit charges."""
    scope_path = repo / SCOPE_REL
    review_path = repo / REVIEW_REL
    if not scope_path.is_file():
        raise GuardError(f"missing R1-R6 scope file: {scope_path}")
    if not review_path.is_file():
        raise GuardError(f"missing J2271 review manifest: {review_path}")

    scope = json.loads(scope_path.read_text())
    review = json.loads(review_path.read_text())

    if scope.get("job") != JOB_ID or scope.get("film") != FILM_ID:
        raise GuardError("R1-R6 scope job/film mismatch")
    reservation_id = scope.get("reservation_id")
    if reservation_id != DEFAULT_RESERVATION or reservation_id in FORBIDDEN_RESERVATIONS:
        raise GuardError(f"invalid or forbidden reservation_id: {reservation_id!r}")

    budget = scope.get("budget") or {}
    if (
        budget.get("row_count") != 6
        or budget.get("credits_per_row") != CREDITS_PER_ROW
        or budget.get("max_takes_per_row") != MAX_TAKES_PER_ROW
        or budget.get("total_cap_credits") != TOTAL_CAP_CREDITS
        or budget.get("minimum_balance_after_cap_and_other_reservations") != HEADROOM_FLOOR
        or budget.get("max_rows_per_batch") != MAX_BATCH_ROWS
        or budget.get("max_credits_per_batch") != MAX_BATCH_CREDITS
    ):
        raise GuardError("R1-R6 budget block drifted from 6x100=600 cap / 3000 floor")

    raw_rows = scope.get("rows") or []
    if len(raw_rows) != 6:
        raise GuardError(f"expected exactly 6 R1-R6 rows, found {len(raw_rows)}")

    review_repairs = {
        str(item.get("repair_id")): item
        for item in (review.get("scoped_repairs_for_chief_authorization") or [])
    }
    if tuple(review_repairs.keys()) != EXPECTED_REPAIR_IDS:
        raise GuardError("J2271 review scoped_repairs_for_chief_authorization does not match R1..R6")

    verified_rows: list[dict] = []
    seen_charges: set[str] = set()
    for idx, (row, exp_r, exp_row_id, exp_charge) in enumerate(
        zip(raw_rows, EXPECTED_REPAIR_IDS, EXPECTED_ROW_IDS, EXPECTED_NAMED_CHARGES), start=1
    ):
        if row.get("repair_id") != exp_r or row.get("row_id") != exp_row_id:
            raise GuardError(f"row {idx} mismatch: {row.get('repair_id')}/{row.get('row_id')}")
        charge_id = row.get("charge_id")
        if charge_id != exp_charge or charge_id in seen_charges:
            raise GuardError(f"invalid or duplicate named charge on {exp_r}: {charge_id!r}")
        seen_charges.add(charge_id)
        if (
            row.get("quality") != REQUIRED_QUALITY
            or row.get("model") != REQUIRED_MODEL
            or row.get("aspect") != REQUIRED_ASPECT
            or row.get("duration") != REQUIRED_DURATION
            or row.get("clip_s") != 8
            or row.get("outputs") != REQUIRED_OUTPUTS
            or row.get("max_takes") != MAX_TAKES_PER_ROW
            or row.get("credits") != CREDITS_PER_ROW
            or row.get("take") != 2
        ):
            raise GuardError(f"model/price/take guard mismatch on {exp_r}")
        rev_item = review_repairs[exp_r]
        if row.get("prompt") != rev_item.get("proposed_prompt") or row.get("credits") != rev_item.get("credits"):
            raise GuardError(f"prompt/credits drift between R1-R6 scope and J2271 review on {exp_r}")
        is_explorer = bool(row.get("explorer", False))
        if is_explorer != (exp_row_id == "P5:10_explorer_robin"):
            raise GuardError(f"Explorer reference allowed only on R5 P5:10_explorer_robin, failed on {exp_r}")
        verified_rows.append(dict(row, index=idx, prompt_sha256=base.sha256_bytes(row["prompt"].encode("utf-8"))))

    return scope, verified_rows


def require_r1_r6_authorization(repo: Path, authorization_file: Path | None = None) -> dict:
    scope_path = repo / SCOPE_REL
    live_scope_sha = sha256_file(scope_path)
    scope, rows = load_r1_r6_scope(repo)

    if authorization_file is not None:
        auth_path = Path(authorization_file)
        if not auth_path.is_file():
            raise GuardError(f"missing Chief authorization file: {auth_path}")
        payload = json.loads(auth_path.read_text())
        if (
            not isinstance(payload, dict)
            or payload.get("job") != JOB_ID
            or payload.get("film") != FILM_ID
            or payload.get("reservation_id") != DEFAULT_RESERVATION
            or payload.get("generation_authorized") is not True
            or payload.get("scope_sha256") != live_scope_sha
            or payload.get("authorized_cap_credits") != TOTAL_CAP_CREDITS
            or int(payload.get("minimum_headroom_floor", 0)) < HEADROOM_FLOOR
        ):
            raise GuardError("R1-R6 authorization file failed validation")
        return {
            "authorized": True,
            "job": JOB_ID,
            "reservation_id": DEFAULT_RESERVATION,
            "scope_sha256": live_scope_sha,
            "authorized_cap_credits": TOTAL_CAP_CREDITS,
            "minimum_headroom_floor": int(payload["minimum_headroom_floor"]),
            "source": str(auth_path.resolve()),
        }

    row_flags = [bool(r.get("generation_authorized", False)) for r in rows]
    if scope.get("generation_authorized") is True and all(row_flags):
        return {
            "authorized": True,
            "job": JOB_ID,
            "reservation_id": DEFAULT_RESERVATION,
            "scope_sha256": live_scope_sha,
            "authorized_cap_credits": TOTAL_CAP_CREDITS,
            "minimum_headroom_floor": HEADROOM_FLOOR,
            "source": str(scope_path.resolve()),
        }

    raise GuardError(
        "generation is NOT authorized: R1_R6_REPLACEMENT_SCOPE_J2271.json has generation_authorized=false "
        "(awaiting Chief go on HOS desk #180 after Check 4 dry-run review)"
    )


def build_r1_r6_plan(repo: Path) -> dict:
    scope, rows = load_r1_r6_scope(repo)
    vo_report = verify_vo_and_option_a1(repo)
    explorer_info = verify_explorer_reference(repo)
    batches = [rows[:5], rows[5:]]
    return {
        "job": JOB_ID,
        "film": FILM_ID,
        "scope_file": str(SCOPE_REL),
        "scope_sha256": sha256_file(repo / SCOPE_REL),
        "reservation_id": DEFAULT_RESERVATION,
        "forbidden_released_reservations": list(FORBIDDEN_RESERVATIONS),
        "generation_authorized": bool(scope.get("generation_authorized", False)),
        "submissions": 0,
        "create_clicks": 0,
        "credits_spent": 0,
        "keep": False,
        "review": "PENDING_REVIEW",
        "file_state_when_written": "GENERATED",
        "row_count": len(rows),
        "credits_per_row": CREDITS_PER_ROW,
        "total_cap_credits": TOTAL_CAP_CREDITS,
        "max_takes_per_row": MAX_TAKES_PER_ROW,
        "floor": HEADROOM_FLOOR,
        "house_style_refs": [rel for rel, _sha in CANONICAL_HOUSE_STYLE_REFS],
        "explorer_ref": explorer_info["rel"] if explorer_info else str(EXPLORER_REF_REL),
        "vo_and_option_a1": vo_report,
        "named_charges": [
            {
                "repair_id": r["repair_id"],
                "row_id": r["row_id"],
                "part": r["part"],
                "plate_id": r["plate_id"],
                "take": r["take"],
                "charge_id": r["charge_id"],
                "model": r["model"],
                "aspect": r["aspect"],
                "duration": r["duration"],
                "outputs": r["outputs"],
                "credits": r["credits"],
                "explorer": r["explorer"],
                "short_targets": r["short_targets"],
                "prompt_sha256": r["prompt_sha256"],
            }
            for r in rows
        ],
        "batches": [
            {
                "batch_index": idx,
                "repair_ids": [r["repair_id"] for r in batch],
                "rows": [r["row_id"] for r in batch],
                "named_charges": [r["charge_id"] for r in batch],
                "row_count": len(batch),
                "credits": sum(r["credits"] for r in batch),
            }
            for idx, batch in enumerate(batches, start=1)
        ],
    }


def build_r1_r6_dry_run_report(
    repo: Path,
    *,
    media: Path = DEFAULT_NAS_MEDIA,
    archive_dir: Path | None = None,
    other: int | dict[str, int] = 0,
    floor: int = HEADROOM_FLOOR,
    authorization_file: Path | None = None,
    accounting_state: Path | None = None,
    spend_ledger: Path | None = None,
) -> dict:
    if type(floor) is not int or floor < HEADROOM_FLOOR:
        raise GuardError(f"headroom floor cannot be below {HEADROOM_FLOOR}")
    archive_target = archive_dir or (media / "04_Generated-Clips/archive_v02_r1_r6_plates")
    plan = build_r1_r6_plan(repo)
    vo_report = verify_vo_and_option_a1(repo, media, require_audio_files=False)
    explorer_ref = verify_explorer_reference(repo)

    staging_blockers: list[str] = []
    try:
        auth_info = require_r1_r6_authorization(repo, authorization_file)
    except GuardError as exc:
        auth_info = {"authorized": False, "reason": str(exc)}
        staging_blockers.append(str(exc))

    try:
        style_refs = verify_style_references(repo, media)
    except GuardError as exc:
        style_refs = {"house": [], "explorer": explorer_ref, "staged": False, "reason": str(exc)}
        staging_blockers.append(str(exc))

    nas_media = verify_nas_volume_mounted(media)
    if not nas_media.is_dir():
        raise GuardError(f"NAS media directory missing: {nas_media}")
    verify_nas_volume_mounted(archive_target)
    archive_status = {
        "path": str(archive_target),
        "exists": archive_target.is_dir(),
        "mounted_under_volumes": True,
    }

    shared = SharedFlowAccounting.peek_readonly(accounting_state)
    for forbidden_id in FORBIDDEN_RESERVATIONS:
        if shared["reservations"].get(forbidden_id, {}).get("active"):
            raise GuardError(f"forbidden prior reservation {forbidden_id} is still marked active")
    if DEFAULT_RESERVATION in shared["reservations"] and not shared["reservations"][DEFAULT_RESERVATION].get("active"):
        raise GuardError(f"reservation {DEFAULT_RESERVATION} was already released and cannot be reused")

    resolved_other = resolve_external_reservations(
        shared, other, own_reservation=DEFAULT_RESERVATION, own_film=FILM_ID
    )
    recorded = latest_recorded_flow_balance(spend_ledger)
    balance_left = recorded["left"] if recorded else None
    liability = shared["liability"]
    own_already_active = DEFAULT_RESERVATION in {
        k for k, v in shared["reservations"].items() if v.get("active")
    }
    own_additional = 0 if own_already_active else TOTAL_CAP_CREDITS
    projected_after_600 = (
        balance_left - liability - resolved_other - own_additional if balance_left is not None else None
    )
    active_reservations = {
        key: {"film": val["film"], "cap": val["cap"]}
        for key, val in shared["reservations"].items()
        if val["active"]
    }

    return {
        "job": JOB_ID,
        "film": FILM_ID,
        "generated_at": now_iso(),
        "mode": "dry-run (no browser, no Create click, no NAS writes, 0 submissions, 0 credits spent, no ledger edit)",
        "submissions": 0,
        "create_clicks": 0,
        "credits_spent": 0,
        "keep": False,
        "submit_armed": submit_armed(),
        "submit_env": SUBMIT_ENV,
        "reservation_id": DEFAULT_RESERVATION,
        "released_j2270_reused": False,
        "authorization": auth_info,
        "scope_verified": {
            "scope_file": plan["scope_file"],
            "scope_sha256": plan["scope_sha256"],
            "rows": plan["row_count"],
            "repair_ids": [c["repair_id"] for c in plan["named_charges"]],
            "credits_per_row": CREDITS_PER_ROW,
            "total_cap_credits": TOTAL_CAP_CREDITS,
            "max_takes_per_row": MAX_TAKES_PER_ROW,
            "batch_count": len(plan["batches"]),
            "max_batch_rows": MAX_BATCH_ROWS,
            "max_batch_credits": MAX_BATCH_CREDITS,
            "first_charge": plan["named_charges"][0]["charge_id"],
            "last_charge": plan["named_charges"][-1]["charge_id"],
        },
        "named_charges": plan["named_charges"],
        "batches": plan["batches"],
        "vo_and_option_a1_verified": vo_report,
        "style_refs_verified": style_refs,
        "nas_archive_status": archive_status,
        "staging_blockers": staging_blockers,
        "shared_accounting_readonly": {
            "active_reservations": active_reservations,
            "unposted_charges": shared["unposted"],
            "remaining_reservations": shared["remaining_reservations"],
            "total_liability": liability,
            "has_pending_charge": shared["pending"],
            "external_reservations_deduplicated": resolved_other,
            "floor": floor,
            "new_reservation_id": DEFAULT_RESERVATION,
            "new_reservation_cap_credits": TOTAL_CAP_CREDITS,
            "latest_recorded_flow_balance": recorded,
            "projected_headroom_after_600_cap": projected_after_600,
            "would_allow_600_reserve_at_recorded_balance": bool(
                not shared["pending"] and projected_after_600 is not None and projected_after_600 >= floor
            ),
        },
    }


def refuse_flow_banners(text: str) -> None:
    """Stop before Create on a cash prompt or an unusual-activity banner. Do not click either one."""
    if not (text or "").strip():
        raise GuardError("Flow page text is empty; stopping before Create")
    if text and CASH_PROMPT_RE.search(text):
        raise GuardError("cash prompt on Flow; stopping before Create (£0, nothing for Ben)")
    if not text or not UNUSUAL_RE.search(text):
        return
    recaptcha_only = re.search(r"protected by recaptcha", text, re.I) and not re.search(
        r"unusual activity|suspicious activity|verify it.?s you", text, re.I
    )
    if not recaptcha_only:
        raise GuardError("unusual-activity banner on Flow; stopping before Create")


def _string_values(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from _string_values(item)
    elif isinstance(value, list):
        for item in value:
            yield from _string_values(item)


def require_signed_go(repo: Path, authorization_file: Path | None) -> dict:
    """The go is the signed file from desk 6898337122. A scope flag alone does not submit."""
    if authorization_file is None:
        raise GuardError(
            "submit requires the signed Chief authorization file for desk "
            f"{GO_COMMENT}; flipping generation_authorized in the scope is not enough"
        )
    payload = json.loads(Path(authorization_file).read_text())
    if any(item in FORBIDDEN_RESERVATIONS for item in _string_values(payload)):
        raise GuardError("authorization file names the released J2270 reservation")
    if str(payload.get("desk_comment") or "") != GO_COMMENT:
        raise GuardError(f"authorization file must point at Chief go {GO_COMMENT}")
    if payload.get("cash_stop") is not True:
        raise GuardError("authorization file must set cash_stop true")
    auth = require_r1_r6_authorization(repo, Path(authorization_file))
    if auth.get("authorized_cap_credits") != TOTAL_CAP_CREDITS:
        raise GuardError("signed go cap is not 600")
    auth["desk_comment"] = GO_COMMENT
    return auth


def authorization_template(repo: Path) -> dict:
    """JSON for the signed file. It does not edit the scope and it does not submit."""
    load_r1_r6_scope(repo)
    return {
        "job": JOB_ID,
        "film": FILM_ID,
        "reservation_id": DEFAULT_RESERVATION,
        "generation_authorized": True,
        "scope_sha256": sha256_file(repo / SCOPE_REL),
        "authorized_cap_credits": TOTAL_CAP_CREDITS,
        "minimum_headroom_floor": HEADROOM_FLOOR,
        "desk_comment": GO_COMMENT,
        "cash_stop": True,
        "signed_by": "chief",
        "note": f"Chief go {GO_COMMENT}. Subscription credits only. Stop on any cash prompt.",
    }


def write_authorization_template(repo: Path, out: Path | None) -> dict:
    payload = authorization_template(repo)
    text = json.dumps(payload, indent=2) + "\n"
    if out is None:
        sys.stdout.write(text)
        return payload
    resolved = out.resolve()
    root = repo.resolve()
    if resolved == root or root in resolved.parents:
        raise GuardError("refusing to write the authorization file inside the repo")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text)
    return payload


def to_base_row(row: dict) -> base.Row:
    prompt = row["prompt"]
    return base.Row(
        index=int(row["index"]),
        row_id=row["row_id"],
        part=int(row["part"]),
        plate_id=row["plate_id"],
        board=str(SCOPE_REL),
        board_sha256=row["prompt_sha256"],
        quality=REQUIRED_QUALITY,
        flow_model=REQUIRED_MODEL,
        max_takes=MAX_TAKES_PER_ROW,
        try1_credits=CREDITS_PER_ROW,
        planning_cap=CREDITS_PER_ROW,
        flow_clip_s=8,
        t_s=None,
        long_use_s=8.0,
        max_short_use_s=8.0,
        required_decode_s=8.0,
        shorts_only=False,
        explorer=bool(row["explorer"]),
        reference=str(row.get("reference") or ""),
        uses=(),
        prompt=prompt,
        prompt_sha256=row["prompt_sha256"],
        normalized_prompt_sha256=base.sha256_bytes(" ".join(prompt.split()).encode("utf-8")),
    )


def r1_r6_output(media: Path, row: base.Row) -> Path:
    """Take 2 under v02, so the twelve-plate v01 t1 clips stay where they are."""
    return (
        media
        / "04_Generated-Clips"
        / f"part{row.part:02d}"
        / "raw"
        / OUTPUT_DIR_NAME
        / f"P{row.part:02d}_{row.plate_id}_t2.mp4"
    )


def r1_r6_state_dir() -> Path:
    return Path.home() / "_desk/state/flow/hos010-r1-r6"


def next_r1_r6_batch(rows: list[base.Row], entries: list[dict]) -> list[base.Row]:
    if any(entry.get("status") == "SUBMITTING" for entry in entries):
        raise GuardError("unresolved local SUBMITTING take; reconcile before the batch")
    done = {
        entry.get("row_id")
        for entry in entries
        if entry.get("charge_id") in EXPECTED_NAMED_CHARGES or entry.get("charge") in EXPECTED_NAMED_CHARGES
    }
    if any(row.row_id not in done for row in rows[:5]):
        return [row for row in rows[:5] if row.row_id not in done]
    return [row for row in rows[5:] if row.row_id not in done]


def projected_headroom(live: int, snap: dict, resolved_other: int) -> int:
    own_active = DEFAULT_RESERVATION in {key for key, val in snap["reservations"].items() if val.get("active")}
    own_additional = 0 if own_active else TOTAL_CAP_CREDITS
    return live - snap["liability"] - resolved_other - own_additional


class BatchHarness:
    """Readers and the one submit callable for a batch. Tests pass fakes; the live session does not."""

    def __init__(self, page_text, live_balance, live_prices, submit, disk_free):
        self.page_text = page_text
        self.live_balance = live_balance
        self.live_prices = live_prices
        self.submit = submit
        self.disk_free = disk_free


def _page_text(page) -> str:
    try:
        return page.locator("body").inner_text(timeout=8000)[:12000]
    except Exception as exc:
        raise GuardError("live Flow page text could not be read; stopping before Create") from exc


def live_named_charge_submit(
    row: base.Row,
    dest: Path,
    frame: Path,
    *,
    accounting: SharedFlowAccounting,
    reservation: str,
    charge: str,
    evidence_path: Path,
    floor: int,
    page,
):
    """Call the existing guarded Create. This function does not click Create itself."""
    if os.environ.get(SUBMIT_ENV) != "1":
        raise GuardError("live submit is not armed")
    accounting._assert_held()
    if reservation != DEFAULT_RESERVATION or reservation in FORBIDDEN_RESERVATIONS:
        raise GuardError("refusing a reservation other than HOS010_R1_R6_PLATES_J2271")
    if charge not in EXPECTED_NAMED_CHARGES:
        raise GuardError(f"refusing an unguarded charge id {charge!r}")
    refuse_flow_banners(_page_text(page))
    if not frame.is_file():
        raise GuardError(f"missing start still for {row.row_id}; not minting a still")
    dest.parent.mkdir(parents=True, exist_ok=True)
    repo = repo_root_from()
    sys.path.insert(0, str(repo / "04_Audio/tools"))
    import orbit_flow_veo_ui as flow

    model = base.expected_model_for(row)
    os.environ["ORBIT_FLOW_VEO_MODEL"] = model
    prompt = base.video_prompt_for_row(row)
    evidence: dict = {}

    def create_guard(configured_page):
        refuse_flow_banners(_page_text(configured_page))
        live_balance = base.read_live_balance(configured_page)
        snap = accounting.snapshot()
        if snap["pending"]:
            raise GuardError("unresolved shared Create; no submission")
        if type(live_balance) is not int or live_balance - snap["liability"] < floor:
            raise GuardError("live headroom fell under the floor before Create")
        base.read_live_evidence(
            configured_page,
            quality=row.quality,
            balance=live_balance,
            open_overlay=True,
        )
        refuse_flow_banners(_page_text(configured_page))
        evidence.update(
            base.guarded_create(
                configured_page,
                accounting,
                row=row,
                reservation=reservation,
                charge=charge,
                evidence_path=evidence_path,
                floor=floor,
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
    if evidence.get("charge") != charge:
        raise GuardError("guarded Create did not return the named charge")
    before_balance = evidence["ui"]["balances"][0]
    after_balance = base.read_live_balance(page)
    delta = before_balance - after_balance
    expected_cost = base.expected_credits_for(row)
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
    evidence["keep"] = False
    evidence["create_clicks"] = 1
    return evidence


@contextmanager
def live_batch_session(media: Path, archive_dir: Path):
    """One Flow tab for the batch. The click stays inside guarded_create."""
    free = shutil.disk_usage("/").free
    if type(free) is not int or free <= MIN_DISK_FREE_BYTES:
        raise GuardError("disk free on / is not above 10 GiB; stopping before Create")
    verify_nas_volume_mounted(media)
    if not media.is_dir():
        raise GuardError(f"NAS media directory missing: {media}")
    verify_nas_volume_mounted(archive_dir)
    archive_dir.mkdir(parents=True, exist_ok=True)
    repo = repo_root_from()
    sys.path.insert(0, str(repo / "04_Audio/tools"))
    import orbit_flow_veo_ui as flow
    from playwright.sync_api import sync_playwright

    cdp = os.environ.get("ORBIT_FLOW_CDP", "http://127.0.0.1:9222")
    with sync_playwright() as playwright:
        try:
            browser = playwright.chromium.connect_over_cdp(cdp)
        except Exception as exc:
            raise GuardError("live Flow browser is not reachable; no Create") from exc
        page = base.open_flow_page(
            browser,
            flow.FLOW_HOME,
            lambda current, url: current.goto(url, wait_until="domcontentloaded", timeout=120_000),
        )
        if "/project/" not in (page.url or ""):
            flow.ensure_project(page)

        def submit(row, dest, frame, *, accounting, reservation, charge, evidence_path, floor):
            return live_named_charge_submit(
                row,
                dest,
                frame,
                accounting=accounting,
                reservation=reservation,
                charge=charge,
                evidence_path=evidence_path,
                floor=floor,
                page=page,
            )

        yield BatchHarness(
            page_text=lambda: _page_text(page),
            live_balance=lambda: base.read_live_balance(page),
            live_prices=lambda: base.read_live_batch_prices_on_page(
                page,
                configure_model=lambda current, model: flow.configure_veo_settings(
                    current, model=model, frames_mode=True, ingredients_mode=False
                ),
            ),
            submit=submit,
            disk_free=lambda: shutil.disk_usage("/").free,
        )


def execute_r1_r6_batch(
    repo: Path,
    *,
    authorization_file: Path,
    media: Path,
    archive_dir: Path,
    ledger_path: Path,
    accounting_state: Path,
    harness: BatchHarness,
    other: int = 0,
    floor: int = HEADROOM_FLOOR,
    test_archive: bool = False,
) -> list[dict]:
    """One R1-R6 batch under the shared writer lock. Named charges only. No twelve-plate scope."""
    if not submit_armed():
        raise SystemExit(
            f"refusing submit: generation is not armed ({SUBMIT_ENV} is not 1). "
            "Plan / dry-run only until the signed Chief file is used on the Mini."
        )
    if type(floor) is not int or floor < HEADROOM_FLOOR:
        raise GuardError(f"headroom floor cannot be below {HEADROOM_FLOOR}")
    require_signed_go(repo, authorization_file)
    _scope, verified = load_r1_r6_scope(repo)
    rows = [to_base_row(row) for row in verified]
    charge_of = {row["row_id"]: row["charge_id"] for row in verified}
    repair_of = {row["row_id"]: row["repair_id"] for row in verified}
    if list(charge_of.values()) != list(EXPECTED_NAMED_CHARGES):
        raise GuardError("named charges drifted from the guarded R1-R6 list")
    batch = next_r1_r6_batch(rows, base.read_ledger(ledger_path))
    if not batch:
        return []
    batch_credits = sum(row.try1_credits for row in batch)
    if (
        len(batch) > MAX_BATCH_ROWS
        or batch_credits > MAX_BATCH_CREDITS
        or any(row.max_takes != MAX_TAKES_PER_ROW or row.try1_credits != CREDITS_PER_ROW for row in batch)
    ):
        raise GuardError("batch exceeds one take, 5 rows or 500 credits")
    free = harness.disk_free()
    if type(free) is not int or free <= MIN_DISK_FREE_BYTES:
        raise GuardError("disk free on / is not above 10 GiB; stopping before Create")
    if test_archive:
        archive_dir.mkdir(parents=True, exist_ok=True)

    with SharedFlowAccounting(accounting_state) as accounting:
        if not accounting.held:
            raise GuardError("shared Flow writer lock is not held")
        snap = accounting.snapshot()
        for forbidden in FORBIDDEN_RESERVATIONS:
            if snap["reservations"].get(forbidden, {}).get("active"):
                raise GuardError(f"forbidden prior reservation {forbidden} is still marked active")
        if snap["pending"]:
            raise GuardError("unresolved shared Create; refusing the batch")
        refuse_flow_banners(harness.page_text())
        live = harness.live_balance()
        if type(live) is not int or live < 0:
            raise GuardError("live Flow balance read is required before the batch")
        resolved_other = resolve_external_reservations(
            snap, other, own_reservation=DEFAULT_RESERVATION, own_film=FILM_ID
        )
        if projected_headroom(live, snap, resolved_other) < floor:
            raise GuardError(
                f"live headroom {projected_headroom(live, snap, resolved_other)} is under the {floor} floor "
                "after the 600 cap; stopping before Create"
            )
        prices = harness.live_prices()
        base.accept_batch_prices(prices, now=datetime.now(timezone.utc))
        refuse_flow_banners(harness.page_text())
        live = harness.live_balance()
        snap = accounting.snapshot()
        if type(live) is not int or projected_headroom(live, snap, resolved_other) < floor:
            raise GuardError("live headroom fell under the floor before reserve; stopping before Create")
        accounting.reserve(
            DEFAULT_RESERVATION,
            FILM_ID,
            TOTAL_CAP_CREDITS,
            live=live - resolved_other,
            floor=floor,
        )
        written: list[dict] = []
        for row in batch:
            refuse_flow_banners(harness.page_text())
            charge = charge_of[row.row_id]
            if charge not in EXPECTED_NAMED_CHARGES:
                raise GuardError(f"refusing an unguarded charge id {charge!r}")
            prior = [
                entry
                for entry in base.read_ledger(ledger_path)
                if entry.get("row_id") == row.row_id or entry.get("charge_id") == charge
            ]
            if prior:
                raise GuardError(f"{row.row_id} already used its one take")
            dest = r1_r6_output(media, row)
            if dest.exists():
                raise GuardError(f"{row.row_id} t2 file already exists; refusing a second take")
            frame = base.still_path(media, row.part, row.plate_id)
            if not test_archive and not frame.is_file():
                raise GuardError(f"missing start still for {row.row_id}; not minting a still")
            evidence_path = archive_dir / f"{repair_of[row.row_id]}.create.json"
            evidence = harness.submit(
                row,
                dest,
                frame,
                accounting=accounting,
                reservation=DEFAULT_RESERVATION,
                charge=charge,
                evidence_path=evidence_path,
                floor=floor,
            )
            if not accounting.held:
                raise GuardError("shared Flow writer lock dropped during Create")
            if not isinstance(evidence, dict) or evidence.get("charge") != charge or evidence.get("keep") is not False:
                raise GuardError("submitter did not return the guarded named charge with keep false")
            if not test_archive:
                shared_charge = accounting.snapshot()["charges"].get(charge)
                if (
                    not shared_charge
                    or shared_charge["status"] != "CHARGED"
                    or shared_charge["amount"] != CREDITS_PER_ROW
                ):
                    raise GuardError("submitter returned without the guarded 100-credit charge")
                if not dest.is_file():
                    raise GuardError("charged output missing; stopping the batch")
                base.strip_audio(dest)
                technical = base.technical_report(dest, required_s=8)
                if not technical["ok"]:
                    base.append_ledger(
                        ledger_path,
                        {
                            "job": JOB_ID,
                            "row_id": row.row_id,
                            "repair_id": repair_of[row.row_id],
                            "charge_id": charge,
                            "take": 2,
                            "status": "FAILED",
                            "file_state": "FAILED_TECHNICAL",
                            "keep": False,
                            "review": "PENDING_REVIEW",
                            "credits": CREDITS_PER_ROW,
                            "technical": technical,
                            "at": now_iso(),
                        },
                    )
                    raise GuardError(f"technical validation failed on {row.row_id}; stopping the batch")
                base.archive_verified(dest, archive_dir / dest.name)
            entry = {
                "job": JOB_ID,
                "row_id": row.row_id,
                "repair_id": repair_of[row.row_id],
                "plate_id": row.plate_id,
                "part": row.part,
                "take": 2,
                "charge_id": charge,
                "status": "PENDING_REVIEW",
                "file_state": "GENERATED",
                "generated": True,
                "review": "PENDING_REVIEW",
                "keep": False,
                "credits": CREDITS_PER_ROW,
                "reservation_id": DEFAULT_RESERVATION,
                "at": now_iso(),
            }
            base.append_ledger(ledger_path, entry)
            written.append(entry)
        return written


def cmd_submit(
    repo: Path,
    *,
    authorization_file: Path | None,
    media: Path,
    archive_dir: Path,
    ledger_path: Path | None = None,
    accounting_state: Path | None = None,
    other: int = 0,
    harness: BatchHarness | None = None,
) -> list[dict]:
    if not submit_armed():
        raise SystemExit(
            f"refusing submit: generation is not armed ({SUBMIT_ENV} is not 1). "
            "Plan / dry-run only until the signed Chief file is used on the Mini."
        )
    if authorization_file is None:
        raise GuardError(
            "submit requires the signed Chief authorization file for desk "
            f"{GO_COMMENT}; flipping generation_authorized in the scope is not enough"
        )
    require_signed_go(repo, authorization_file)
    ledger = ledger_path or (r1_r6_state_dir() / "ledger.jsonl")
    _scope, verified = load_r1_r6_scope(repo)
    batch = next_r1_r6_batch([to_base_row(row) for row in verified], base.read_ledger(ledger))
    if not batch:
        return []
    state = accounting_state if harness is not None else base.shared_flow_state_dir()
    if harness is None and accounting_state is not None:
        if Path(accounting_state).resolve() != base.shared_flow_state_dir().resolve():
            raise GuardError("live submit requires the shared Flow accounting directory")
    if harness is None:
        with live_batch_session(media, archive_dir) as live:
            return execute_r1_r6_batch(
                repo,
                authorization_file=authorization_file,
                media=media,
                archive_dir=archive_dir,
                ledger_path=ledger,
                accounting_state=state,
                harness=live,
                other=other,
                test_archive=False,
            )
    if accounting_state is None:
        raise GuardError("a test harness requires an explicit accounting directory")
    return execute_r1_r6_batch(
        repo,
        authorization_file=authorization_file,
        media=media,
        archive_dir=archive_dir,
        ledger_path=ledger,
        accounting_state=accounting_state,
        harness=harness,
        other=other,
        test_archive=True,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="HOS 010 Alvarez clay line R1-R6 replacement-plate guarded Flow adapter (J2271)"
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    plan_p = sub.add_parser("plan", help="verify 6-row R1-R6 scope, named charges, and 2 batches; submit nothing")
    plan_p.add_argument("--repo")
    plan_p.add_argument("--out")

    dry_p = sub.add_parser("dry-run", help="verify R1-R6 scope, 6 named 100-credit charges, new reservation id, and 3000 floor; submit nothing")
    dry_p.add_argument("--repo")
    dry_p.add_argument("--media", default=str(DEFAULT_NAS_MEDIA))
    dry_p.add_argument("--archive")
    dry_p.add_argument("--other-reservations", type=int, default=0)
    dry_p.add_argument("--floor", type=int, default=HEADROOM_FLOOR)
    dry_p.add_argument("--authorization-file")
    dry_p.add_argument("--out")

    sub_p = sub.add_parser(
        "submit",
        help=f"refused unless {SUBMIT_ENV}=1 AND the signed Chief file for {GO_COMMENT} is present",
    )
    sub_p.add_argument("--repo")
    sub_p.add_argument("--authorization-file")
    sub_p.add_argument("--media", default=str(DEFAULT_NAS_MEDIA))
    sub_p.add_argument("--archive")
    sub_p.add_argument("--other-reservations", type=int, default=0)
    sub_p.add_argument("--ledger")
    sub_p.add_argument("--accounting-state")

    auth_p = sub.add_parser(
        "authorization-template",
        help="print the signed-go JSON for the live scope hash; writes nothing inside the repo",
    )
    auth_p.add_argument("--repo")
    auth_p.add_argument("--out")

    args = parser.parse_args(argv)
    repo = Path(args.repo).resolve() if getattr(args, "repo", None) else repo_root_from()

    if args.cmd == "plan":
        plan = build_r1_r6_plan(repo)
        text = json.dumps(plan, indent=2) + "\n"
        if args.out:
            Path(args.out).write_text(text)
        else:
            sys.stdout.write(text)
        return 0

    if args.cmd == "dry-run":
        report = build_r1_r6_dry_run_report(
            repo,
            media=Path(args.media),
            archive_dir=Path(args.archive) if args.archive else None,
            other=args.other_reservations,
            floor=args.floor,
            authorization_file=Path(args.authorization_file) if args.authorization_file else None,
        )
        text = json.dumps(report, indent=2) + "\n"
        if args.out:
            Path(args.out).write_text(text)
        else:
            sys.stdout.write(text)
        return 0

    if args.cmd == "authorization-template":
        out = Path(args.out) if args.out else None
        write_authorization_template(repo, out)
        return 0

    if args.cmd == "submit":
        if not submit_armed():
            raise SystemExit(
                f"refusing submit: generation is not armed ({SUBMIT_ENV} is not 1). "
                "Plan / dry-run only until the signed Chief file is used on the Mini."
            )
        archive = (
            Path(args.archive)
            if args.archive
            else Path(args.media) / "04_Generated-Clips/archive_v02_r1_r6_plates"
        )
        written = cmd_submit(
            repo,
            authorization_file=Path(args.authorization_file) if args.authorization_file else None,
            media=Path(args.media),
            archive_dir=archive,
            ledger_path=Path(args.ledger) if args.ledger else None,
            accounting_state=Path(args.accounting_state) if args.accounting_state else None,
            other=args.other_reservations,
        )
        sys.stdout.write(json.dumps({"submissions": len(written), "keep": False, "rows": [row["row_id"] for row in written]}) + "\n")
        return 0

    return 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except GuardError as exc:
        print(f"STOP {exc}", file=sys.stderr)
        raise SystemExit(2)
