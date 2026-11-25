#!/usr/bin/env python3
"""HOS 013 take-2 retake receipt and 0.5 s contact sheets (J3747). Spends nothing.

Reads the retake runner's ledger (~/_desk/state/flow/hos013-retake1/ledger.jsonl),
re-hashes every take-2 clip in raw/v01_retake1 and its copy in archive_v01_retake1,
builds one contact sheet per clip (a frame every 0.5 s) under
archive_v01_retake1/sheets/, and writes jobs/reviews/J3747/RETAKE1_RECEIPT.json and
SHEETS_INDEX.json. Every row stays keep: false / PENDING_REVIEW: keep marks are the
Chief's. Never writes into archive_v01_pass1 and never touches REVIEW_STATE.json.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

JOB = "J3747"
ROWS = ["P1:03a_unlabelled_birds", "P1:07_darwin_1837_desk", "P3:02a_malthus_lamplight",
        "P3:05a_chicks_deep_beaks", "P4:10_fairness_25_june", "P4:12_lyell_hooker_bundle",
        "P5:05a_darwin_writes_origin", "P6:06a_origin_fifth_edition"]
ARCHIVE_NAME = "archive_v01_retake1"
DEFAULT_MEDIA = Path("/Volumes/data/studio-live/History Of Science/02_Video-Projects/013_Darwin-Wallace-Evolution")
DEFAULT_LEDGER = Path.home() / "_desk/state/flow/hos013-retake1/ledger.jsonl"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def latest_by_row(ledger: Path) -> dict[str, dict]:
    latest: dict[str, dict] = {}
    for line in ledger.read_text().splitlines():
        if line.strip():
            entry = json.loads(line)
            latest[entry["row_id"]] = entry
    return latest


def build_sheet(clip: Path, sheet: Path) -> None:
    sheet.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-i", str(clip),
         "-vf", "fps=2,scale=480:-2,tile=4x4", "-frames:v", "1", "-q:v", "3", str(sheet)],
        check=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=str(Path(__file__).resolve().parents[3]))
    ap.add_argument("--media", default=str(DEFAULT_MEDIA))
    ap.add_argument("--ledger", default=str(DEFAULT_LEDGER))
    args = ap.parse_args()
    media, repo = Path(args.media), Path(args.repo)
    archive = media / "04_Generated-Clips" / ARCHIVE_NAME
    if archive.name != ARCHIVE_NAME or not archive.is_dir():
        raise SystemExit(f"STOP missing retake archive: {archive}")
    latest = latest_by_row(Path(args.ledger))
    rows, sheets, credits = [], [], 0
    for row_id in ROWS:
        entry = latest.get(row_id)
        if entry is None:
            rows.append({"row_id": row_id, "take": 2, "status": "NOT_SUBMITTED", "keep": False})
            continue
        if entry.get("take") != 2 or entry.get("keep") is not False:
            raise SystemExit(f"STOP {row_id}: ledger line is not a take-2 keep:false line")
        out = {"row_id": row_id, "take": 2, "status": entry.get("status"), "file_state": entry.get("file_state"),
               "review": "PENDING_REVIEW", "keep": False, "flow_model": entry.get("flow_model"),
               "prompt_sha256": entry.get("prompt_sha256"), "start_still": entry.get("input"),
               "shared_charge": entry.get("shared_charge"), "credits_used": entry.get("credits_used", 0)}
        clip = Path(entry.get("file", ""))
        if entry.get("file_state") == "GENERATED" and clip.is_file():
            copy = archive / clip.name
            raw_sha, copy_sha = sha256_file(clip), sha256_file(copy) if copy.is_file() else None
            if not (raw_sha == copy_sha == entry.get("sha256")):
                raise SystemExit(f"STOP {row_id}: sha256 mismatch between ledger, raw clip and archive copy")
            technical = entry.get("technical") or {}
            sheet = archive / "sheets" / (clip.stem + "_sheet_0.5s.jpg")
            build_sheet(copy, sheet)
            out.update(file=str(clip), archive=str(copy), sha256=raw_sha, sha256_verified=True,
                       technical_ok=technical.get("ok"), duration_s=technical.get("duration_s"))
            sheets.append({"row_id": row_id, "clip": clip.name, "clip_sha256": raw_sha, "sheet": str(sheet),
                           "sheet_sha256": sha256_file(sheet), "step_s": 0.5, "grid": "4x4"})
            credits += int(entry.get("credits_used") or 0)
        rows.append(out)
    if credits > 800:
        raise SystemExit("STOP credits over the 800 cap")
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    generated = sum(1 for r in rows if r.get("sha256_verified"))
    receipt = {"job": JOB, "film": "HOS:013", "ref": "J3738", "option": "A", "built_at": now,
               "model": "Veo 3.1 - Quality", "take": 2, "rows_authorised": 8, "rows_generated": generated,
               "flow_credits_used": credits, "flow_credit_cap": 800, "gbp": 0,
               "archive": str(archive), "keep": False, "review": "PENDING_REVIEW (keep marks are the Chief's)",
               "rows": rows}
    out_dir = repo / "jobs" / "reviews" / JOB
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "RETAKE1_RECEIPT.json").write_text(json.dumps(receipt, indent=2) + "\n")
    (out_dir / "SHEETS_INDEX.json").write_text(json.dumps(
        {"job": JOB, "film": "HOS:013", "built_at": now, "sheets": sheets}, indent=2) + "\n")
    print(f"{generated}/8 take-2 clips verified, {credits} credits, {len(sheets)} sheets -> {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
