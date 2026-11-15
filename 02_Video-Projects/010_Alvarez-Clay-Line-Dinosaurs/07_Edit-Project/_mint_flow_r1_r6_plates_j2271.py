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
- `submit` is interlocked behind BOTH `HOS010_R1_R6_PLATES_SUBMIT=1` AND explicit Chief authorization (`generation_authorized=true` or signed `--authorization-file` pinning `scope_sha256` and `authorized_cap_credits=600`).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
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

    sub_p = sub.add_parser("submit", help=f"refused unless {SUBMIT_ENV}=1 AND Chief R1-R6 authorization is present")
    sub_p.add_argument("--repo")
    sub_p.add_argument("--authorization-file")

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

    if args.cmd == "submit":
        if not submit_armed():
            raise SystemExit(
                f"refusing submit: generation is not armed ({SUBMIT_ENV} is not 1). "
                "Plan / dry-run only until Chief go on HOS desk #180."
            )
        require_r1_r6_authorization(
            repo,
            Path(args.authorization_file) if args.authorization_file else None,
        )
        raise SystemExit("submit requires live Flow browser worker invocation after Chief authorization.")

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
