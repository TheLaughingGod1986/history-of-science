#!/usr/bin/env python3
"""HOS 013 Darwin & Wallace take-2 retake Flow runner (J3747, Option A).

Chief price pass and mint go: acting Chief `gemini`, J3738, 25 Nov 2026 (HOS PR #789).

This file adds no new Flow or accounting code. It loads `_mint_flow_v01_pass1.py`
and reuses every guard there (studio Ultra account SHA-256, SharedFlowAccounting,
WriterLock, duplicate-process refusal, live price check before the batch and again
per row right before Create, Veo 3.1 - Fast refusal, FAILED_POLICY and
SESSION_BLOCKED handling, sha256-verified NAS copies, keep: false / PENDING_REVIEW
on every output). It only narrows them to the retake scope:

- Exactly the 8 RETAKE rows 3, 10, 24, 28, 47, 49, 54, 63 of RETAKE_BOARD_v01.json,
  pinned by the board's sha256, each row's `prompt_retake_sha256` and its take-1
  `start_still_sha256`. No still is ever minted here (all 8 exist): a missing or
  changed start still refuses the batch.
- Veo 3.1 - Quality, 8 s, 16:9, x1, 100 credits a row. Take 2 only, one take a row.
- Hard cap 800 credits; at most 4 rows / 400 credits a batch (2 batches).
- Armed submit floor 3000 (projected balance after the reservation).
- Refuses to submit on or after 2026-12-05T00:00:00Z, when Veo 3.1 - Quality retires.
- Own state (~/_desk/state/flow/hos013-retake1), own reservation HOS013_RETAKE1,
  own raw folder raw/v01_retake1 and own archive archive_v01_retake1. It never
  writes to archive_v01_pass1.

`plan` and `dry-run` open no browser, click nothing and spend 0 credits.
`submit` is refused unless HOS013_RETAKE1_SUBMIT=1.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("hos013_pass1_runner", HERE / "_mint_flow_v01_pass1.py")
p1 = importlib.util.module_from_spec(_spec)
sys.modules["hos013_pass1_runner"] = p1
_spec.loader.exec_module(p1)

GuardError = p1.GuardError

JOB = "J3747"
BOARD_NAME = "RETAKE_BOARD_v01.json"
BOARD_SHA256 = "19f6f9c1faad96e247b694fc40d7c7a8f71ddec173e74d024e1f27adbf92be58"
RETAKE_ROWS = {
    3: "P1:03a_unlabelled_birds",
    10: "P1:07_darwin_1837_desk",
    24: "P3:02a_malthus_lamplight",
    28: "P3:05a_chicks_deep_beaks",
    47: "P4:10_fairness_25_june",
    49: "P4:12_lyell_hooker_bundle",
    54: "P5:05a_darwin_writes_origin",
    63: "P6:06a_origin_fifth_edition",
}
RETAKE_TAKE = 2
CUTOFF_UTC = datetime(2026, 12, 5, 0, 0, 0, tzinfo=timezone.utc)
ARCHIVE_DIRNAME = "archive_v01_retake1"
RAW_DIRNAME = "v01_retake1"
ARMED_FLOOR = 3000
DEFAULT_ARCHIVE = p1.DEFAULT_NAS_MEDIA / "04_Generated-Clips" / ARCHIVE_DIRNAME

# Narrow the pass-1 constants. Functions in p1 read these at call time.
p1.EXPECTED_ROW_COUNT = 8
p1.EXPECTED_QUALITY_COUNT = 8
p1.EXPECTED_FAST_COUNT = 0
p1.MAX_TOTAL_CREDITS = 800
p1.MAX_TAKES_PER_ROW = 1
p1.MAX_BATCH_ROWS = 4
p1.MAX_BATCH_CREDITS = 400
p1.DETACHED_HEADROOM_FLOOR = ARMED_FLOOR
p1.DEFAULT_RESERVATION = "HOS013_RETAKE1"
p1.SUBMIT_ENV = "HOS013_RETAKE1_SUBMIT"

_STILL_PINS: dict[str, tuple[str, str]] = {}


def refuse_after_cutoff(now: datetime | None = None) -> None:
    now = now or datetime.now(timezone.utc)
    if now >= CUTOFF_UTC:
        raise GuardError(
            "Veo 3.1 - Quality retires 2026-12-05T00:00:00Z; retake submit refused. "
            "Park for Chief to re-price on Option B/C."
        )


def load_retake_scope(repo: Path) -> list:
    """The exact 8 retake rows, verified against the pinned board and the part plate boards."""
    board_path = repo / p1.EDIT_REL / BOARD_NAME
    if not board_path.is_file():
        raise GuardError(f"missing retake board: {board_path}")
    if p1.sha256_file(board_path) != BOARD_SHA256:
        raise GuardError("scope drift: RETAKE_BOARD_v01.json sha256 mismatch")
    board = json.loads(board_path.read_text())
    if board.get("film") != p1.FILM_ID:
        raise GuardError(f"retake board film {board.get('film')!r} != {p1.FILM_ID}")
    if list(board.get("rows_in_board") or []) != sorted(RETAKE_ROWS):
        raise GuardError("scope drift: retake board row list differs from the 8 authorised rows")
    raw_rows = board.get("rows") or []
    if [int(r.get("n") or 0) for r in raw_rows] != sorted(RETAKE_ROWS):
        raise GuardError("scope drift: retake board rows differ from the 8 authorised rows")

    rows = []
    _STILL_PINS.clear()
    for raw in raw_rows:
        n = int(raw["n"])
        row_id = str(raw.get("row_id") or "")
        if RETAKE_ROWS[n] != row_id:
            raise GuardError(f"scope drift: row {n} is {row_id!r}, expected {RETAKE_ROWS[n]!r}")
        if raw.get("take") != RETAKE_TAKE:
            raise GuardError(f"{row_id}: only take {RETAKE_TAKE} is authorised")
        price = (raw.get("price") or {}).get("pre_5_dec") or {}
        if price != {"model": "Veo 3.1 - Quality", "clip_s": 8, "credits": 100}:
            raise GuardError(f"{row_id}: price is not Veo 3.1 - Quality / 8 s / 100 credits")
        part = int(row_id[1:row_id.index(":")])
        plate_id = row_id.split(":", 1)[1]
        board_rel = p1.EDIT_REL / str(raw.get("plate_board") or "")
        if board_rel != p1.EDIT_REL / "parts" / f"part-0{part}_plates_v02.json":
            raise GuardError(f"{row_id}: unexpected plate board {board_rel}")
        plates = json.loads((repo / board_rel).read_text()).get("plates") or []
        match = [p for p in plates if p.get("id") == plate_id]
        if len(match) != 1:
            raise GuardError(f"{row_id}: not found exactly once on {board_rel}")
        plate = match[0]
        if plate.get("route") != "flow-first" or plate.get("quality") != "Quality":
            raise GuardError(f"{row_id}: plate is not a flow-first Quality row")
        if "Fast" in str(plate.get("flow_model") or ""):
            raise GuardError(f"{row_id}: Veo 3.1 - Fast is refused")
        if int(plate.get("flow_clip_s") or 0) != p1.REQUIRED_CLIP_S:
            raise GuardError(f"{row_id}: flow_clip_s must be {p1.REQUIRED_CLIP_S}")
        use_s = float(plate.get("use_s") or 0.0)
        if use_s <= 0 or use_s > p1.REQUIRED_CLIP_S or abs(use_s - float(raw.get("use_s") or 0)) > 1e-6:
            raise GuardError(f"{row_id}: use_s invalid or drifted")
        prompt = str(raw.get("prompt_retake") or "")
        if not prompt.strip():
            raise GuardError(f"{row_id}: empty prompt_retake")
        prompt_sha = p1.sha256_bytes(prompt.encode("utf-8"))
        if prompt_sha != raw.get("prompt_retake_sha256"):
            raise GuardError(f"scope drift: prompt_retake hash mismatch on {row_id}")
        still, still_sha = str(raw.get("start_still") or ""), str(raw.get("start_still_sha256") or "")
        if not still or len(still_sha) != 64:
            raise GuardError(f"{row_id}: start still is not pinned")
        _STILL_PINS[row_id] = (still, still_sha)
        rows.append(p1.Row(
            index=n, row_id=row_id, part=part, plate_id=plate_id, board=str(board_rel),
            quality="Quality", flow_model=p1.expected_model_for("Quality"),
            max_takes=1, try1_credits=p1.expected_credits_for("Quality"),
            flow_clip_s=p1.REQUIRED_CLIP_S,
            t_s=float(plate.get("t_s") or 0.0), t_end_s=float(plate.get("t_end_s") or 0.0),
            use_s=use_s, explorer=bool(plate.get("explorer", False)),
            prompt=prompt, prompt_sha256=prompt_sha,
            normalized_prompt_sha256=p1.sha256_bytes(" ".join(prompt.split()).encode("utf-8")),
        ))
    if len(rows) != 8 or sum(r.try1_credits for r in rows) != p1.MAX_TOTAL_CREDITS:
        raise GuardError("scope drift: retake scope is not 8 rows / 800 credits")
    return rows


def versioned_output(media: Path, part: int, plate_id: str, take: int = RETAKE_TAKE) -> Path:
    if take != RETAKE_TAKE:
        raise GuardError(f"P{part}:{plate_id}: only take {RETAKE_TAKE} is authorised, not take {take}")
    return (media / "04_Generated-Clips" / f"part{part:02d}" / "raw" / RAW_DIRNAME
            / f"P{part:02d}_{plate_id}_t{take}.mp4")


def next_version(media: Path, part: int, plate_id: str, used=(), blocked=()):
    """Take 2, once. Any ledger line or file for this row's take 2 refuses a further take."""
    if set(int(t) for t in used) | set(int(t) for t in blocked):
        raise GuardError(f"P{part}:{plate_id} already has a take-2 ledger line; take 3 is refused")
    dest = versioned_output(media, part, plate_id, RETAKE_TAKE)
    if dest.exists():
        raise GuardError(f"P{part}:{plate_id} take-2 file already exists; take 3 is refused: {dest}")
    return RETAKE_TAKE, dest


_orig_verify_still_inventory = p1.verify_still_inventory


def verify_still_inventory(rows: list, media: Path) -> list[dict]:
    inventory = _orig_verify_still_inventory(rows, media)
    for item in inventory:
        pin = _STILL_PINS.get(item["row_id"])
        if pin is None:
            raise GuardError(f"{item['row_id']}: no pinned start still (load the retake scope first)")
        if Path(pin[0]).resolve() != Path(item["path"]) or pin[1] != item["sha256"]:
            raise GuardError(f"{item['row_id']}: start still differs from the take-1 still pinned on the board")
    return inventory


def refuse_still_mint(row, dest, **_kwargs):
    raise GuardError(f"{row.row_id}: start still missing; the retake runner mints no stills (0 credits for stills)")


_orig_require_archive = p1.require_archive


def require_archive(archive_dir, *, nas: bool = True):
    if archive_dir is None or Path(archive_dir).name != ARCHIVE_DIRNAME:
        raise GuardError(f"retake archive must be {ARCHIVE_DIRNAME}; never archive_v01_pass1")
    Path(archive_dir).mkdir(exist_ok=True)
    return _orig_require_archive(archive_dir, nas=nas)


def _cutoff_wrap(fn):
    def wrapped(*args, **kwargs):
        refuse_after_cutoff()
        return fn(*args, **kwargs)
    wrapped.__name__ = fn.__name__
    wrapped.__signature__ = __import__("inspect").signature(fn)
    return wrapped


p1.load_scope = load_retake_scope
p1.versioned_output = versioned_output
p1.next_version = next_version
p1.verify_still_inventory = verify_still_inventory
p1.live_still_maker = refuse_still_mint
p1.require_archive = require_archive
p1.runner_state_dir = lambda: Path.home() / "_desk/state/flow/hos013-retake1"
p1.execute_shared_batch = _cutoff_wrap(p1.execute_shared_batch)
p1.live_video_submit = _cutoff_wrap(p1.live_video_submit)
p1.guarded_create = _cutoff_wrap(p1.guarded_create)


def dry_run_report(repo: Path, *, media: Path, archive_dir: Path, other: int, floor: int) -> dict:
    if Path(archive_dir).name != ARCHIVE_DIRNAME:
        raise GuardError(f"retake archive must be {ARCHIVE_DIRNAME}; never archive_v01_pass1")
    rows = load_retake_scope(repo)
    stills = verify_still_inventory(rows, media)
    # The archive folder is made by the armed submit; the dry-run checks the mounted parent only.
    report = p1.build_dry_run_report(repo, media=media, archive_dir=Path(archive_dir).parent,
                                     other=other, floor=floor)
    report["job"] = JOB
    report["retake"] = {
        "board": BOARD_NAME, "board_sha256": BOARD_SHA256, "take": RETAKE_TAKE,
        "rows": [{"n": r.index, "row_id": r.row_id, "prompt_retake_sha256": r.prompt_sha256} for r in rows],
        "start_stills_match_board": [{"row_id": s["row_id"], "sha256": s["sha256"]} for s in stills],
        "archive": str(archive_dir), "raw_dir": RAW_DIRNAME,
        "cutoff_utc": CUTOFF_UTC.isoformat(), "before_cutoff": datetime.now(timezone.utc) < CUTOFF_UTC,
        "armed_floor": ARMED_FLOOR, "reservation": p1.DEFAULT_RESERVATION,
    }
    if report["submissions"] != 0 or report["create_clicks"] != 0 or report["keep"] is not False:
        raise GuardError("dry-run tried to submit or keep")
    return report


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    cmd = argv[0] if argv else ""
    if cmd == "dry-run":
        import argparse
        ap = argparse.ArgumentParser(prog="retake1 dry-run")
        ap.add_argument("--repo")
        ap.add_argument("--media", default=str(p1.DEFAULT_NAS_MEDIA))
        ap.add_argument("--archive", default=str(DEFAULT_ARCHIVE))
        ap.add_argument("--other-reservations", type=int, default=0)
        ap.add_argument("--floor", type=int, default=ARMED_FLOOR)
        ap.add_argument("--out")
        a = ap.parse_args(argv[1:])
        report = dry_run_report(Path(a.repo) if a.repo else p1.repo_root_from(HERE), media=Path(a.media),
                                archive_dir=Path(a.archive), other=a.other_reservations, floor=a.floor)
        text = json.dumps(report, indent=2) + "\n"
        if a.out:
            Path(a.out).parent.mkdir(parents=True, exist_ok=True)
            Path(a.out).write_text(text)
        else:
            sys.stdout.write(text)
        return 0
    if cmd == "plan":
        return p1.main(argv)
    if cmd == "submit":
        refuse_after_cutoff()
        if "--archive" not in argv:
            argv += ["--archive", str(DEFAULT_ARCHIVE)]
        return p1.main(argv)
    if cmd == "reconcile-policy-refusal":
        return p1.main(argv)
    raise GuardError(f"command {cmd!r} is not offered by the retake runner (plan, dry-run, submit, "
                     "reconcile-policy-refusal). Run submit inside tmux for a detached batch.")


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except GuardError as exc:
        print(f"STOP {exc}", file=sys.stderr)
        raise SystemExit(2)
