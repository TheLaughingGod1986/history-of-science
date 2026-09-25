#!/usr/bin/env python3
"""Stamp a Related-style parent-title pill onto HOS 002 punch Shorts.

Rebuilds from caption-free raw.mp4 so the old Didot title is not stacked under
the pill. Studio Related ▶ still needs the long YouTube id after upload.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
WORK = HERE / "_work"
ICLOUD = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT"
PARENT_LINES = ["How Did We Discover", "the Periodic Table?"]
W, H = 1080, 1920
BROWN = (61, 41, 28, 235)
CREAM = (245, 232, 210, 255)
INK = (42, 28, 18, 255)
FONT = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"

IDS = [
    "s01_empty_chairs",
    "s02_predict_metal",
    "s03_gallium",
    "s04_tellurium",
    "s05_other_table",
]


def probe(p: Path) -> float:
    r = subprocess.run(
        [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(p),
        ],
        check=True, capture_output=True, text=True,
    )
    return float(r.stdout.strip())


def render_pill(dest: Path) -> None:
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT, 38)
    pad_x, pad_y, gap = 40, 24, 6
    widths = [font.getlength(line) for line in PARENT_LINES]
    heights = [font.getbbox(line)[3] - font.getbbox(line)[1] for line in PARENT_LINES]
    text_w = max(widths)
    text_h = sum(heights) + gap
    box_w = int(text_w + pad_x * 2)
    box_h = int(text_h + pad_y * 2)
    x0 = (W - box_w) // 2
    y0 = 176
    draw.rounded_rectangle((x0, y0, x0 + box_w, y0 + box_h), radius=30, fill=BROWN)
    draw.rounded_rectangle(
        (x0 + 2, y0 + 2, x0 + box_w - 2, y0 + box_h - 2),
        radius=28, outline=CREAM, width=3,
    )
    cy = y0 + pad_y - 4
    for line, tw, lh in zip(PARENT_LINES, widths, heights):
        tx = x0 + (box_w - tw) / 2
        draw.text((tx + 1, cy + 1), line, font=font, fill=INK)
        draw.text((tx, cy), line, font=font, fill=CREAM)
        cy += lh + gap
    dest.parent.mkdir(parents=True, exist_ok=True)
    img.save(dest)


def stamp(sid: str, pill: Path) -> Path:
    raw = WORK / sid / "raw.mp4"
    line = WORK / sid / "cap_line.png"
    cta = WORK / sid / "cap_cta.png"
    if not raw.exists() or not line.exists() or not cta.exists():
        raise SystemExit(f"missing work files for {sid}")
    total = probe(raw)
    cta_in = max(total - 4.0, 14.4)
    dest = HERE / f"hos_002_{sid}_punch_pill_v01.mp4"
    subprocess.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(raw),
            "-loop", "1", "-i", str(line),
            "-loop", "1", "-i", str(pill),
            "-loop", "1", "-i", str(cta),
            "-filter_complex",
            (
                f"[0:v][1:v]overlay=0:0:enable='between(t,0.20,{cta_in - 0.10:.2f})'[v1];"
                f"[v1][2:v]overlay=0:0:enable='between(t,9.00,14.00)'[v2];"
                f"[v2][3:v]overlay=0:0:enable='between(t,{cta_in:.2f},{total - 0.12:.2f})'[vout]"
            ),
            "-map", "[vout]", "-map", "0:a",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "18",
            "-r", "24",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
            "-t", f"{total:.3f}",
            "-movflags", "+faststart",
            str(dest),
        ],
        check=True,
    )
    out_d = probe(dest)
    if out_d < 22.0 or out_d >= 28.0:
        raise SystemExit(f"{sid}: {out_d:.2f}s — abort")
    return dest


def main() -> None:
    pill = WORK / "related_pill" / "related_pill.png"
    render_pill(pill)
    meta = []
    for sid in IDS:
        dest = stamp(sid, pill)
        print(f"OK {dest.name} {probe(dest):.2f}s", flush=True)
        meta.append({"id": sid, "file": dest.name, "duration": probe(dest)})
    (WORK / "related_pill" / "pill_stamp.json").write_text(json.dumps(meta, indent=2) + "\n")


if __name__ == "__main__":
    main()
