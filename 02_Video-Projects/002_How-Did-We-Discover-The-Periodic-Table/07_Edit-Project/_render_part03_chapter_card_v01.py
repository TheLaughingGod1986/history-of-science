#!/usr/bin/env python3
"""Render Part 03 local chapter card (parchment) — no Flow credits."""
from __future__ import annotations

import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

PROJ = Path(__file__).resolve().parents[1]
OUT_STILL = PROJ / "04_Generated-Clips/part03/refs/v01_stills/01_chapter_card.png"
OUT_MP4 = PROJ / "04_Generated-Clips/part03/raw/v01_fast/01_chapter_card_v01.mp4"
TITLE = "A Ruler for Atoms"
SUB = "Part 03"


def main() -> None:
    OUT_STILL.parent.mkdir(parents=True, exist_ok=True)
    OUT_MP4.parent.mkdir(parents=True, exist_ok=True)
    w, h = 1920, 1080
    im = Image.new("RGB", (w, h), (42, 28, 18))
    d = ImageDraw.Draw(im)
    # parchment panel
    d.rounded_rectangle((220, 180, 1700, 900), radius=28, fill=(232, 214, 180))
    d.rounded_rectangle((240, 200, 1680, 880), radius=22, outline=(120, 82, 42), width=4)
    try:
        font_title = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia Bold.ttf", 84)
        font_sub = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia.ttf", 40)
    except OSError:
        font_title = ImageFont.load_default()
        font_sub = font_title
    tb = d.textbbox((0, 0), TITLE, font=font_title)
    tw = tb[2] - tb[0]
    d.text(((w - tw) / 2, 430), TITLE, fill=(48, 28, 12), font=font_title)
    sb = d.textbbox((0, 0), SUB, font=font_sub)
    sw = sb[2] - sb[0]
    d.text(((w - sw) / 2, 560), SUB, fill=(96, 64, 36), font=font_sub)
    im.save(OUT_STILL, quality=95)
    subprocess.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-loop", "1", "-i", str(OUT_STILL),
            "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
            "-c:v", "libx264", "-tune", "stillimage", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-shortest", "-t", "8.0", str(OUT_MP4),
        ],
        check=True,
    )
    print(f"SAVED {OUT_MP4}", flush=True)


if __name__ == "__main__":
    main()
