#!/usr/bin/env python3
"""Frame-0 sheet for HOS 005 Shorts v01 (THUMBNAIL_AND_TITLE_RULES.md §3: frame 0 is the
feed thumbnail). Frame 0 of each passed v01 file at phone width (390 px, an iPhone in points),
with the hook caption as built, the gate verdict and the 14-day uniqueness line.

  python3 _frame0_sheet_v01.py --gate-json <dir with s01_the_sum.json …> --line "<text>" …
"""
from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
OUT = HERE / "covers_v01" / "hos_005_shorts_v01_frame0_sheet.jpg"
SHORTS = [
    ("s01_the_sum", "A", "MORE THAN YOU HAVE"),
    ("s02_the_tied_arm", "B", "ONE TIGHT BAND"),
    ("s03_never_saw", "C", "HE NEVER SAW THIS"),
]
PW, PH, GAP, PAD = 390, 693, 24, 28


def font(size: int) -> ImageFont.FreeTypeFont:
    for f in ("/System/Library/Fonts/Helvetica.ttc", "/System/Library/Fonts/Supplemental/Arial.ttf"):
        if Path(f).exists():
            return ImageFont.truetype(f, size)
    return ImageFont.load_default()


def frame0(mp4: Path) -> Image.Image:
    with tempfile.TemporaryDirectory() as td:
        png = Path(td) / "f0.png"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(mp4), "-frames:v", "1", str(png)], check=True)
        return Image.open(png).convert("RGB").resize((PW, PH), Image.LANCZOS)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--gate-json", type=Path, required=True)
    ap.add_argument("--line", action="append", default=[])
    args = ap.parse_args()

    f_lab, f_small = font(22), font(17)
    head = 70
    foot = 30 + 26 * len(args.line)
    sheet = Image.new("RGB", (PAD * 2 + 3 * PW + 2 * GAP, PAD + head + PH + 64 + foot), (245, 242, 236))
    d = ImageDraw.Draw(sheet)
    for i, (sid, letter, hook) in enumerate(SHORTS):
        g = json.loads((args.gate_json / f"{sid}.json").read_text())[0]
        x = PAD + i * (PW + GAP)
        d.text((x, PAD), f"{letter} · {sid}", font=f_lab, fill=(20, 20, 20))
        d.text((x, PAD + 30), f"hook: {hook}", font=f_small, fill=(70, 70, 70))
        sheet.paste(frame0(HERE / f"hos_005_{sid}_v01.mp4"), (x, PAD + head))
        y = PAD + head + PH + 10
        d.text((x, y), f"{g['verdict']} air {g['air_date']} · motion {g['motion_0_1s']}", font=f_small,
               fill=(0, 110, 40) if g["verdict"] == "PASS" else (180, 0, 0))
        d.text((x, y + 24), f"dhash {g['dhash']} · near opens ±14 d: {len(g['near_opens'])}", font=f_small, fill=(40, 40, 40))
    y = PAD + head + PH + 64 + 14
    for ln in args.line:
        d.text((PAD, y), ln, font=f_small, fill=(30, 30, 30))
        y += 26
    OUT.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(OUT, quality=90)
    print(OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
