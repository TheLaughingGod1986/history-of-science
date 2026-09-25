#!/usr/bin/env python3
"""Compose Part 04 I2V start frames from plate-01 desk DNA.

After 01_chapter_empty_chairs_v01.mp4 exists, extract DNA frames and draw
cream-card layouts / Explorer overlay for downstream I2V plates.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

PROJ = Path(__file__).resolve().parents[1]
RAW = PROJ / "04_Generated-Clips/part04/raw/v01_fast"
STILLS = PROJ / "04_Generated-Clips/part04/refs/v01_stills"
EXPLORER_LOCK = PROJ / "04_Generated-Clips/part01/refs/explorer_germs_part01_lock.jpg"
PLATE01 = RAW / "01_chapter_empty_chairs_v01.mp4"


def grab(ss: float, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 20_000:
        return
    if not PLATE01.exists():
        raise SystemExit(f"STOP: missing plate-01 DNA source {PLATE01}")
    subprocess.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-ss", str(ss), "-i", str(PLATE01), "-frames:v", "1", str(dest),
        ],
        check=True,
    )


def cream_card(draw: ImageDraw.ImageDraw, xy, wh, mark: str | None = None) -> None:
    x, y = xy
    w, h = wh
    draw.rounded_rectangle((x, y, x + w, y + h), radius=8, fill=(245, 232, 205, 255))
    draw.rounded_rectangle(
        (x, y, x + w, y + h), radius=8, outline=(180, 150, 110, 255), width=2
    )
    if mark:
        try:
            font = ImageFont.truetype(
                "/System/Library/Fonts/Supplemental/Georgia Bold.ttf", 28
            )
        except OSError:
            font = ImageFont.load_default()
        bb = draw.textbbox((0, 0), mark, font=font)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        draw.text(
            (x + (w - tw) / 2, y + (h - th) / 2 - 2),
            mark,
            fill=(90, 60, 35, 255),
            font=font,
        )


def glow_slot(draw: ImageDraw.ImageDraw, xy, wh) -> None:
    x, y = xy
    w, h = wh
    for i, a in ((18, 40), (10, 90), (0, 140)):
        draw.rounded_rectangle(
            (x - i, y - i, x + w + i, y + h + i),
            radius=10 + i // 2,
            outline=(255, 220, 120, a),
            width=3,
        )
    draw.rounded_rectangle(
        (x, y, x + w, y + h), radius=8, outline=(255, 230, 150, 220), width=3
    )


def compose_layout(base: Path, dest: Path, kind: str) -> None:
    im = Image.open(base).convert("RGBA")
    W, H = im.size
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    cw, ch = int(W * 0.07), int(H * 0.11)
    desk_y = int(H * 0.58)
    desk_x0 = int(W * 0.18)

    if kind == "desk_hero_card":
        cream_card(d, (int(W * 0.42), int(H * 0.38)), (int(W * 0.16), int(H * 0.28)), "O 16")
    elif kind == "desk_weight_line":
        for i in range(10):
            cream_card(d, (desk_x0 + i * int(cw * 1.15), desk_y), (cw, ch))
        # soft line glow
        d.rectangle(
            (desk_x0, desk_y + ch + 6, desk_x0 + 10 * int(cw * 1.15), desk_y + ch + 14),
            fill=(255, 210, 120, 90),
        )
    elif kind == "desk_columns":
        for col in range(5):
            for row in range(4):
                cream_card(
                    d,
                    (desk_x0 + col * int(cw * 1.35), desk_y - row * int(ch * 1.15)),
                    (cw, ch),
                )
    elif kind == "desk_empty_seats":
        for col in range(5):
            for row in range(4):
                if (col, row) in {(1, 2), (2, 1), (3, 3)}:
                    glow_slot(
                        d,
                        (desk_x0 + col * int(cw * 1.35), desk_y - row * int(ch * 1.15)),
                        (cw, ch),
                    )
                else:
                    cream_card(
                        d,
                        (desk_x0 + col * int(cw * 1.35), desk_y - row * int(ch * 1.15)),
                        (cw, ch),
                    )
    elif kind == "desk_one_gap":
        for col in range(5):
            for row in range(4):
                xy = (desk_x0 + col * int(cw * 1.35), desk_y - row * int(ch * 1.15))
                if (col, row) == (2, 2):
                    glow_slot(d, xy, (cw, ch))
                else:
                    cream_card(d, xy, (cw, ch))
    elif kind == "desk_swap_cards":
        for col in range(4):
            for row in range(4):
                mark = None
                if col == 2 and row == 1:
                    mark = "Te"
                if col == 2 and row == 2:
                    mark = "I"
                cream_card(
                    d,
                    (desk_x0 + col * int(cw * 1.35), desk_y - row * int(ch * 1.15)),
                    (cw, ch),
                    mark,
                )
    elif kind == "desk_publish_papers":
        # flat sheet with holes
        sheet = (int(W * 0.28), int(H * 0.35), int(W * 0.72), int(H * 0.78))
        d.rounded_rectangle(sheet, radius=12, fill=(236, 224, 200, 235))
        d.rounded_rectangle(sheet, radius=12, outline=(160, 130, 95, 255), width=3)
        for col in range(6):
            for row in range(5):
                x = sheet[0] + 28 + col * 55
                y = sheet[1] + 28 + row * 48
                if (col, row) in {(1, 2), (3, 1), (4, 3)}:
                    d.rectangle((x, y, x + 40, y + 34), outline=(255, 210, 120, 220), width=3)
                else:
                    d.rounded_rectangle((x, y, x + 40, y + 34), radius=4, fill=(245, 232, 205, 255))
    else:
        raise SystemExit(f"unknown layout kind {kind}")

    out = Image.alpha_composite(im, overlay).convert("RGB")
    dest.parent.mkdir(parents=True, exist_ok=True)
    out.save(dest, quality=92)
    print(f"  wrote {dest.name}", flush=True)


def compose_explorer(base: Path, dest: Path) -> None:
    if not EXPLORER_LOCK.exists():
        raise SystemExit(f"STOP: missing explorer lock {EXPLORER_LOCK}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    # Overlay Explorer mid-frame on desk DNA; also draw a glowing gap.
    bed = Image.open(base).convert("RGBA")
    W, H = bed.size
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    cw, ch = int(W * 0.07), int(H * 0.11)
    glow_slot(d, (int(W * 0.48), int(H * 0.55)), (cw, ch))
    bed = Image.alpha_composite(bed, overlay)
    tmp_bed = STILLS / "_tmp_desk_gap.png"
    bed.convert("RGB").save(tmp_bed)
    subprocess.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(tmp_bed), "-i", str(EXPLORER_LOCK),
            "-filter_complex",
            "[1:v]scale=520:-1[ch];[0:v][ch]overlay=(W-w)/2+40:(H-h)/2+80",
            "-frames:v", "1", str(dest),
        ],
        check=True,
    )
    tmp_bed.unlink(missing_ok=True)
    print(f"  wrote {dest.name}", flush=True)


def main() -> None:
    STILLS.mkdir(parents=True, exist_ok=True)
    dna_t1 = STILLS / "desk_dna_t1.jpg"
    dna_t4 = STILLS / "desk_dna_t4.jpg"
    dna_t65 = STILLS / "desk_dna_t65.jpg"
    grab(1.0, dna_t1)
    grab(4.0, dna_t4)
    grab(6.5, dna_t65)

    compose_layout(dna_t4, STILLS / "desk_hero_card.jpg", "desk_hero_card")
    compose_layout(dna_t1, STILLS / "desk_weight_line.jpg", "desk_weight_line")
    compose_layout(dna_t4, STILLS / "desk_columns.jpg", "desk_columns")
    compose_layout(dna_t65, STILLS / "desk_empty_seats.jpg", "desk_empty_seats")
    compose_layout(dna_t4, STILLS / "desk_one_gap.jpg", "desk_one_gap")
    compose_layout(dna_t1, STILLS / "desk_swap_cards.jpg", "desk_swap_cards")
    compose_layout(dna_t65, STILLS / "desk_publish_papers.jpg", "desk_publish_papers")
    compose_explorer(dna_t4, STILLS / "explorer_on_desk.jpg")
    print("OK part04 desk stills ready", flush=True)


if __name__ == "__main__":
    main()
