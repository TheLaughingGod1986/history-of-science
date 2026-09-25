#!/usr/bin/env python3
"""Compose I2V start frames for Part 04 v03 — scrub glowing house props on books.

UAT FAIL v02 ~19–21s: glowing yellow house / model-town props on leather book stack
under ATOMIC WEIGHT (plate 02b_cards_sixty_three). Paint clean book-top leather over
the props region. Do not touch 05/06 window KEEP.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

PROJ = Path(__file__).resolve().parents[1]
RAW_V01 = PROJ / "04_Generated-Clips/part04/raw/v01_fast"
STILLS = PROJ / "04_Generated-Clips/part04/refs/v03_stills"
FAIL = STILLS / "ben_fail"
ROUGH = PROJ / "09_Final-Export/hos_002_part04_rough_v02.mp4"
QA = PROJ / "07_Edit-Project/_qa_part04_v03_spot"

# Glowing yellow props on book-stack top (measured from 02b t5 + rough ~19–21s)
BOOK_PROP_BOX = (0.68, 0.38, 0.88, 0.58)


def grab(src: Path, ss: float, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-ss", str(ss), "-i", str(src), "-frames:v", "1", str(dest),
        ],
        check=True,
    )


def scrub_book_props(src: Path, dest: Path, box_frac=BOOK_PROP_BOX) -> None:
    """Opaque leather fill over glowing house / model-town props on book top."""
    im = Image.open(src).convert("RGB")
    w, h = im.size
    x0 = int(w * box_frac[0])
    y0 = int(h * box_frac[1])
    x1 = int(w * box_frac[2])
    y1 = int(h * box_frac[3])

    # Sample leather colour from book body just below the props
    samples = []
    sy0 = min(h - 2, y1 + 4)
    sy1 = min(h - 1, y1 + 28)
    sx0 = max(0, x0 + 8)
    sx1 = min(w - 1, x1 - 8)
    for y in range(sy0, sy1):
        for x in range(sx0, sx1, 3):
            r, g, b = im.getpixel((x, y))
            # skip remaining yellow glow / bright highlights
            if r > 190 and g > 150 and b < 130:
                continue
            samples.append((r, g, b))
    if samples:
        leather = tuple(sum(c[i] for c in samples) // len(samples) for i in range(3))
    else:
        leather = (92, 58, 38)

    cover = Image.new("RGB", (w, h), leather)
    cd = ImageDraw.Draw(cover)
    # Soft strap / book-top edge so the patch reads as leather, not a flat stamp
    mid_y = (y0 + y1) // 2
    strap = tuple(max(0, c - 18) for c in leather)
    cd.rectangle((x0, mid_y - 3, x1, mid_y + 3), fill=strap)
    highlight = tuple(min(255, c + 22) for c in leather)
    cd.rectangle((x0 + 6, y0 + 4, x1 - 6, y0 + 10), fill=highlight)

    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle((x0, y0, x1, y1), radius=10, fill=255)
    soft = mask.filter(ImageFilter.GaussianBlur(radius=2.5))
    out = Image.composite(cover, im, soft)

    dest.parent.mkdir(parents=True, exist_ok=True)
    out.save(dest, quality=95)
    print(
        f"wrote {dest.name} box=({x0},{y0},{x1},{y1}) leather={leather} "
        f"bytes={dest.stat().st_size}",
        flush=True,
    )


def main() -> None:
    STILLS.mkdir(parents=True, exist_ok=True)
    FAIL.mkdir(parents=True, exist_ok=True)
    QA.mkdir(parents=True, exist_ok=True)

    plate = RAW_V01 / "02b_cards_sixty_three_v01.mp4"
    if not plate.exists():
        raise SystemExit(f"missing {plate}")

    for t in (1.0, 3.0, 5.0, 7.0):
        grab(plate, t, FAIL / f"02b_fail_t{int(t)}.jpg")
    if ROUGH.exists():
        for t in (19.0, 20.0, 21.0):
            grab(ROUGH, t, FAIL / f"rough_t{int(t)}_atomic_weight.jpg")

    scrub_book_props(FAIL / "02b_fail_t5.jpg", STILLS / "02b_books_scrub_i2v.jpg")
    scrub_book_props(FAIL / "02b_fail_t3.jpg", STILLS / "02b_books_scrub_alt.jpg")
    scrub_book_props(FAIL / "02b_fail_t1.jpg", STILLS / "02b_books_scrub_t1.jpg")
    if (FAIL / "rough_t20_atomic_weight.jpg").exists():
        scrub_book_props(
            FAIL / "rough_t20_atomic_weight.jpg",
            STILLS / "02b_books_scrub_from_rough.jpg",
        )

    for name in (
        "02b_books_scrub_i2v.jpg",
        "02b_books_scrub_alt.jpg",
        "02b_books_scrub_from_rough.jpg",
    ):
        src = STILLS / name
        if src.exists():
            (QA / f"scrub_{name}").write_bytes(src.read_bytes())

    print(f"OK v03 scrub stills → {STILLS}", flush=True)


if __name__ == "__main__":
    main()
