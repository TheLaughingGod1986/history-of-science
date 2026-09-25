#!/usr/bin/env python3
"""Prep Part 04 v19 Flow start frames — UAT HARD FAIL bible 43d9405.

Parent FAIL: hos_002_part04_rough_v18.mp4
  sha256 05fb0a2b34dba1a8347ab74b2abc987fd406bef356b82b55f1a0e8ddb88cc6b5

Remint I2V starts: 06_explorer_leaves_gap · 11_publish_gaps · 11b_wait_and_hunt
KEEP untouched in assemble: 10_family (v18) · CLEAN LIGHT 09/09b · written cards ~40

Explorer start = KEEP back-view still (hair already cleared) — do not reintroduce blot.
Publish starts = clean single-exposure v18 procedural desks (opaque props, no ghost DNA).
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path

from PIL import Image

PROJ = Path(__file__).resolve().parents[1]
OUT = PROJ / "04_Generated-Clips/part04/refs/v19_start_frames"
QA = PROJ / "07_Edit-Project/_qa_part04_v19_prep"
V18 = PROJ / "04_Generated-Clips/part04/refs/v18_start_frames"
KEEP_EXPLORER = PROJ / "04_Generated-Clips/part04/refs/v19_fail_keep/keep_explorer_back.jpg"
META = OUT / "compose_meta.json"
W, H = 1920, 1080
PARENT_V18_SHA = "05fb0a2b34dba1a8347ab74b2abc987fd406bef356b82b55f1a0e8ddb88cc6b5"


def fit_cover(src: Path, dest: Path) -> None:
    im = Image.open(src).convert("RGB")
    sw, sh = im.size
    scale = max(W / sw, H / sh)
    nw, nh = int(sw * scale), int(sh * scale)
    im = im.resize((nw, nh), Image.Resampling.LANCZOS)
    left = (nw - W) // 2
    top = (nh - H) // 2
    im = im.crop((left, top, left + W, top + H))
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.save(dest, quality=95)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QA.mkdir(parents=True, exist_ok=True)
    if not KEEP_EXPLORER.exists():
        raise SystemExit(f"missing KEEP explorer still {KEEP_EXPLORER}")

    meta: dict = {
        "parent_v18_sha": PARENT_V18_SHA,
        "bible_main": "43d9405",
        "plates": {},
        "method": (
            "publish desks = v18 single-exposure procedural starts; "
            "explorer = KEEP back-view still cover-fit 1920x1080"
        ),
        "remint": ["06_explorer_leaves_gap", "11_publish_gaps", "11b_wait_and_hunt"],
        "keep_assemble": ["10_family_before_weight", "09_risk_bet", "09b_risk_hold"],
    }

    for pid in ("11_publish_gaps", "11b_wait_and_hunt"):
        src = V18 / f"{pid}_start_v18.jpg"
        if not src.exists():
            raise SystemExit(f"missing v18 start {src} — run _prep_part04_v18_start_frames.py first")
        dest = OUT / f"{pid}_start_v19.jpg"
        shutil.copy2(src, dest)
        Image.open(dest).save(QA / f"start_{pid}.jpg", quality=92)
        meta["plates"][pid] = str(dest)
        print(f"copied {dest.name} from v18", flush=True)

    dest06 = OUT / "06_explorer_leaves_gap_start_v19.jpg"
    fit_cover(KEEP_EXPLORER, dest06)
    Image.open(dest06).save(QA / "start_06_explorer_leaves_gap.jpg", quality=92)
    meta["plates"]["06_explorer_leaves_gap"] = str(dest06)
    print(f"wrote {dest06.name} from KEEP back-view", flush=True)

    META.write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta, indent=2), flush=True)
    print("PREP OK", flush=True)


if __name__ == "__main__":
    main()
