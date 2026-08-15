#!/usr/bin/env python3
"""Remaster published Orbit masters to YouTube-safe CFR without touching audio.

Does **not** upload. Does **not** create new YouTube videos (that would reset
view counts). Writes CFR files you then push through Studio **Replace**, which
keeps the original video id, URL, views, comments and publish date.

Usage:
  python3 04_Audio/tools/fix_published_playback_lag.py
  python3 04_Audio/tools/fix_published_playback_lag.py --apply
  python3 04_Audio/tools/fix_published_playback_lag.py --root /path/to/Orbit-YouTube --apply
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from orbit_cfr_delivery import assess_file, needs_remaster, remaster_cfr  # noqa: E402

REPO = TOOLS.parents[1]
BACKUP_DIRNAME = "_pre_cfr_fix"
FIXED_SUFFIX = "_cfr_fixed"
SKIP_STEM_PARTS = (FIXED_SUFFIX, BACKUP_DIRNAME, "_qc_", "PROOF", "_proof", "_work_")


def discover_masters(root: Path) -> list[Path]:
    files: list[Path] = []
    projects = root / "02_Video-Projects"
    if not projects.is_dir():
        return files
    patterns = [
        "*/09_Final-Export/*.mp4",
        "*/10_Shorts/06_Final-Exports/*.mp4",
        "*/07_Edit-Project/01_Masters/*UPLOAD_READY*.mp4",
    ]
    for pattern in patterns:
        for path in projects.glob(pattern):
            name = path.name
            if path.suffix.lower() != ".mp4":
                continue
            if any(part in path.as_posix() or part in name for part in SKIP_STEM_PARTS):
                continue
            if name.startswith("_"):
                continue
            files.append(path)
    return sorted(set(files))


def load_studio_replace_targets(root: Path) -> list[dict]:
    """Map remastered files back to existing YouTube ids (never new uploads)."""
    targets: list[dict] = []
    projects = root / "02_Video-Projects"
    if not projects.is_dir():
        return targets
    for index_path in sorted(projects.glob("*/10_Shorts/SHORTS_UPLOAD_INDEX.json")):
        data = json.loads(index_path.read_text())
        project = index_path.parents[2].name
        long_id = data.get("long_id") or data.get("related_to_long")
        if long_id:
            targets.append(
                {
                    "kind": "longform",
                    "project": project,
                    "video_id": long_id,
                    "title": data.get("long_title") or "",
                    "studio_url": f"https://studio.youtube.com/video/{long_id}/edit",
                    "file": None,
                }
            )
        for item in data.get("shorts") or []:
            vid = item.get("youtube_video_id") or item.get("video_id")
            if not vid:
                continue
            rel = item.get("file")
            targets.append(
                {
                    "kind": "short",
                    "project": project,
                    "video_id": vid,
                    "title": item.get("title") or "",
                    "studio_url": f"https://studio.youtube.com/video/{vid}/edit",
                    "file": rel,
                }
            )
    return targets


def backup_and_replace(original: Path, remastered: Path) -> Path:
    backup_dir = original.parent / BACKUP_DIRNAME
    backup_dir.mkdir(parents=True, exist_ok=True)
    backup = backup_dir / original.name
    if not backup.exists():
        shutil.copy2(original, backup)
    shutil.copy2(remastered, original)
    return backup


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=REPO)
    ap.add_argument(
        "--apply",
        action="store_true",
        help="Overwrite originals in place after backing up to _pre_cfr_fix/ (same filename → same Studio Replace).",
    )
    ap.add_argument(
        "--force",
        action="store_true",
        help="Remaster even if the file already looks like CFR libx264.",
    )
    args = ap.parse_args()
    root = args.root.expanduser().resolve()
    files = discover_masters(root)
    report: dict = {
        "ran_at": datetime.now(timezone.utc).isoformat(),
        "root": str(root),
        "apply": args.apply,
        "files": [],
        "studio_replace": load_studio_replace_targets(root),
        "note": (
            "Do not upload these as new YouTube videos. Use Studio Replace on the "
            "existing video id so views/comments/URL stay put. See docs/PLAYBACK_LAG_FIX.md."
        ),
    }
    if not files:
        print("No delivery masters found (mp4s are gitignored; run on the production workspace).")
        out = root / "00_Brand/Channel-Setup/audits/playback_lag_remaster_report.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, indent=2) + "\n")
        print(out)
        return 0

    for src in files:
        row: dict = {"src": str(src.relative_to(root)) if src.is_relative_to(root) else str(src)}
        try:
            before = assess_file(src)
            row["before"] = {
                "ok": before["ok"],
                "vfr": before["variable_frame_rate"],
                "videotoolbox": before["videotoolbox"],
                "r_frame_rate": before.get("r_frame_rate"),
                "avg_frame_rate": before.get("avg_frame_rate"),
                "encoder": before.get("encoder"),
                "errors": before.get("errors"),
            }
            if not args.force and not needs_remaster(before):
                row["skipped"] = "already_cfr"
                print(f"OK  {row['src']}")
            else:
                dest = src.with_name(src.stem + FIXED_SUFFIX + src.suffix)
                result = remaster_cfr(src, dest)
                after = result["output"]
                row["dest"] = str(dest.relative_to(root)) if dest.is_relative_to(root) else str(dest)
                row["after"] = {
                    "ok": after["ok"],
                    "vfr": after["variable_frame_rate"],
                    "r_frame_rate": after.get("r_frame_rate"),
                    "avg_frame_rate": after.get("avg_frame_rate"),
                    "encoder": after.get("encoder"),
                    "errors": after.get("errors"),
                }
                row["copied_audio"] = result["copied_audio"]
                if args.apply:
                    backup = backup_and_replace(src, dest)
                    row["applied"] = True
                    row["backup"] = str(backup.relative_to(root)) if backup.is_relative_to(root) else str(backup)
                if not after["ok"]:
                    row["ok"] = False
                    print(f"FAIL {row['src']} → still unhealthy: {after.get('errors')}")
                else:
                    row["ok"] = True
                    print(f"FIX {row['src']} → {dest.name} (audio {'copied' if result['copied_audio'] else 're-encoded AAC'})")
        except Exception as exc:
            row["ok"] = False
            row["error"] = str(exc)[:400]
            print(f"ERR {row['src']}: {exc}")
        report["files"].append(row)

    out = root / "00_Brand/Channel-Setup/audits/playback_lag_remaster_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n")
    print(out)
    print(
        "Next: python3 00_Brand/Channel-Setup/audits/_replace_media_in_place.py "
        "(Studio Replace — keeps view counts). Do NOT run _replace_shorts_v02_youtube.py."
    )
    failed = sum(1 for f in report["files"] if f.get("ok") is False)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
