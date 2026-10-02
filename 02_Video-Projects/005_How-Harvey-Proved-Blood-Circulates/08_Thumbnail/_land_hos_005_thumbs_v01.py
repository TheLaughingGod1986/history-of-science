#!/usr/bin/env python3
"""Land HOS 005 long thumbs v01 (desk task from Claude, PR #180 comment 5948700711).

Live 001–004 grammar: painted key art, the tied arm as the giant hero object on the
right, the Explorer small lower left, cream + gold painted serif lettering.

  A = ONE TIGHT BAND  (generated painting, used as is)
  B = IT GOES ROUND   (A's painting with the lettering panel from the B lettering pass;
                       the B pass lost the red artery, so only its lettering is kept)

Then thumb_preview.py (168×94) and style_sheet.py (vs live) for each. Nothing to Studio.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
ASSETS = HERE / "_assets_v01"
SELECTED = HERE / "Selected"
GEN = Path.home() / ".cursor/projects/Users-benjaminoats-YouTube-History-Of-Science/assets"
TOOLS = ROOT / "00_Brand/Channel-Setup/tools"

W, H = 1280, 720
SRC_A = "hos_005_thumb_A_one_tight_band_v01c.jpg"
SRC_B_LETTERS = "hos_005_thumb_B_it_goes_round_v01d.jpg"
# Lettering panel on the 1280×720 painting; stops above the Explorer's hair.
PANEL = (40, 0, 540, 378)
FEATHER = 8


def src(name: str) -> Path:
    ASSETS.mkdir(parents=True, exist_ok=True)
    local = ASSETS / name
    if not local.exists():
        local.write_bytes((GEN / name).read_bytes())
    return local


def save_jpg(im: Image.Image, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.convert("RGB").resize((W, H), Image.Resampling.LANCZOS).save(
        dest, "JPEG", quality=92, optimize=True, subsampling=1
    )
    print(f"  {dest.name}  {dest.stat().st_size} B", flush=True)
    return dest


def splice_lettering(base: Image.Image, letters: Image.Image) -> Image.Image:
    mask = Image.new("L", base.size, 0)
    ImageDraw.Draw(mask).rectangle(PANEL, fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(FEATHER))
    out = base.copy()
    out.paste(letters, (0, 0), mask)
    return out


def check(kind: str, tool: str, jpg: Path, out: Path) -> None:
    cmd = [sys.executable, str(TOOLS / tool), kind, str(jpg), "--out", str(out)]
    print("$", " ".join(cmd[1:]), flush=True)
    subprocess.check_call(cmd)


def main() -> None:
    a = Image.open(src(SRC_A)).convert("RGB")
    b_letters = Image.open(src(SRC_B_LETTERS)).convert("RGB")
    a_jpg = save_jpg(a, SELECTED / "hos_005_thumb_A_one_tight_band_v01.jpg")
    b_jpg = save_jpg(splice_lettering(a, b_letters), SELECTED / "hos_005_thumb_B_it_goes_round_v01.jpg")

    for jpg in (a_jpg, b_jpg):
        check("long", "thumb_preview.py", jpg, SELECTED / f"{jpg.stem}_preview.jpg")
    subprocess.check_call(
        [sys.executable, str(TOOLS / "style_sheet.py"), "long", str(a_jpg), str(b_jpg),
         "--out", str(SELECTED / "hos_005_thumbs_v01_style_sheet.jpg")]
    )

    idx = {
        "parentTitle": "The Tied Arm That Proved Your Blood Circulates",
        "version": "v01",
        "status": "STOP for Ben pick. Proposed only. Nothing to Studio.",
        "composer": HERE.name + "/" + Path(__file__).name,
        "factLock": "Tight linen band on the upper arm; red (artery) only on the shoulder side, "
                    "stopping at the band; no red below it (De Motu Cordis ch. 11, FACT_NOTES_v01 row 26).",
        "thumbs": [
            {"id": "A", "hook": "ONE TIGHT BAND", "jpg": f"Selected/{a_jpg.name}",
             "sha256": hashlib.sha256(a_jpg.read_bytes()).hexdigest()},
            {"id": "B", "hook": "IT GOES ROUND", "jpg": f"Selected/{b_jpg.name}",
             "sha256": hashlib.sha256(b_jpg.read_bytes()).hexdigest()},
        ],
        "sources": [SRC_A, SRC_B_LETTERS],
        "upload": False,
        "studio": False,
    }
    (HERE / "THUMBS_INDEX_v01.json").write_text(json.dumps(idx, indent=2) + "\n")
    print("  INDEX THUMBS_INDEX_v01.json", flush=True)


if __name__ == "__main__":
    main()
