#!/usr/bin/env python3
"""Compose I2V start frames for Part 04 v04 — both house-silhouette blockers.

A) 02b books ~18–21: RECTANGULAR plain leather / blank-card tops only.
   NEVER adaptive / house-contour fills (v03 mistake left peaked-roof masks).
B) 09 / 09b A BET ~91–97: hard night-sky window fill (moon/clouds).
   KEEP glowing vacant chair. No rooftop / model-town sill line.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

PROJ = Path(__file__).resolve().parents[1]
RAW_V01 = PROJ / "04_Generated-Clips/part04/raw/v01_fast"
STILLS = PROJ / "04_Generated-Clips/part04/refs/v04_stills"
FAIL = STILLS / "ben_fail"
ROUGH = PROJ / "09_Final-Export/hos_002_part04_rough_v03.mp4"
QA = PROJ / "07_Edit-Project/_qa_part04_v04_spot"

# Hard rectangular book-top cover on 02b (measured from v01 plate + rough ~18–21)
BOOK_BOX = (0.66, 0.32, 0.94, 0.62)

# Window glass on glowing-chair beat — leave chair glow intact (lower-right)
WIN_09 = (0.18, 0.00, 0.82, 0.52)
WIN_09B = (0.12, 0.00, 0.92, 0.55)
WIN_ROUGH = (0.20, 0.00, 0.78, 0.50)


def grab(src: Path, ss: float, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-ss", str(ss), "-i", str(src), "-frames:v", "1", str(dest),
        ],
        check=True,
    )


def rect_leather_book_top(src: Path, dest: Path, box_frac=BOOK_BOX) -> None:
    """Plain rectangular leather / blank card top — never house-shaped masks."""
    im = Image.open(src).convert("RGB")
    w, h = im.size
    x0 = int(w * box_frac[0])
    y0 = int(h * box_frac[1])
    x1 = int(w * box_frac[2])
    y1 = int(h * box_frac[3])

    samples: list[tuple[int, int, int]] = []
    sy0 = min(h - 2, y1 + 2)
    sy1 = min(h - 1, y1 + 36)
    for y in range(sy0, sy1):
        for x in range(x0 + 10, x1 - 10, 2):
            r, g, b = im.getpixel((x, y))
            # skip yellow house glow + white cards
            if r > 200 and g > 170 and b < 140:
                continue
            if r > 210 and g > 210 and b > 200:
                continue
            samples.append((r, g, b))
    leather = (
        tuple(sum(c[i] for c in samples) // len(samples) for i in range(3))
        if samples
        else (96, 62, 42)
    )

    cover = Image.new("RGB", (w, h), leather)
    cd = ImageDraw.Draw(cover)
    mid_y = (y0 + y1) // 2
    strap = tuple(max(0, c - 16) for c in leather)
    hi = tuple(min(255, c + 20) for c in leather)
    # flat book-top only — rectangles, no peaks / chimneys
    cd.rectangle((x0 + 6, mid_y - 3, x1 - 6, mid_y + 3), fill=strap)
    cd.rectangle((x0 + 10, y0 + 8, x1 - 10, y0 + 16), fill=hi)

    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle((x0, y0, x1, y1), radius=12, fill=255)
    soft = mask.filter(ImageFilter.GaussianBlur(radius=1.8))
    out = Image.composite(cover, im, soft)

    dest.parent.mkdir(parents=True, exist_ok=True)
    out.save(dest, quality=95)
    print(
        f"wrote {dest.name} book_box=({x0},{y0},{x1},{y1}) leather={leather} "
        f"bytes={dest.stat().st_size}",
        flush=True,
    )


def hard_scrub_window(
    src: Path,
    dest: Path,
    box_frac: tuple[float, float, float, float],
    moon_frac: tuple[float, float] = (0.58, 0.12),
    *,
    strip_label: bool = False,
    keep_clouds: bool = True,
) -> None:
    """Opaque night sky + moon (+ soft clouds) over window glass. Chair untouched."""
    im = Image.open(src).convert("RGB")
    w, h = im.size
    x0 = int(w * box_frac[0])
    y0 = int(h * box_frac[1])
    x1 = int(w * box_frac[2])
    y1 = int(h * box_frac[3])

    sky = Image.new("RGB", (w, h), (24, 40, 86))
    sd = ImageDraw.Draw(sky)
    if keep_clouds:
        for cx, cy, cr, col in (
            (0.35, 0.18, 0.055, (70, 95, 140)),
            (0.48, 0.22, 0.07, (85, 110, 155)),
            (0.62, 0.16, 0.05, (65, 90, 135)),
            (0.40, 0.30, 0.045, (55, 80, 125)),
        ):
            px, py = int(w * cx), int(h * cy)
            r = int(min(w, h) * cr)
            sd.ellipse((px - r, py - r, px + r, py + int(r * 0.6)), fill=col)

    mx, my = int(w * moon_frac[0]), int(h * moon_frac[1])
    rad = max(18, int(min(w, h) * 0.036))
    sd.ellipse((mx - rad, my - rad, mx + rad, my + rad), fill=(236, 236, 250))
    for sx, sy in (
        (mx - rad * 2.6, my + 10),
        (mx + rad * 1.9, my - 6),
        (mx + 10, my + rad * 1.7),
        (mx - rad * 0.8, my + rad * 2.1),
        (mx + rad * 2.4, my + rad),
    ):
        sd.ellipse((int(sx), int(sy), int(sx) + 2, int(sy) + 2), fill=(220, 225, 240))

    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rectangle((x0, y0, x1, y1), fill=255)
    soft = mask.filter(ImageFilter.GaussianBlur(radius=1.4))
    inset = Image.new("L", (w, h), 0)
    # Hard bottom edge — no soft fade that leaves rooftop sill line
    ImageDraw.Draw(inset).rectangle((x0 + 3, y0 + 3, x1 - 3, y1), fill=255)
    mask = Image.composite(inset, soft, inset)
    out = Image.composite(sky, im, mask)

    if strip_label:
        d = ImageDraw.Draw(out)
        d.rectangle(
            (int(w * 0.70), int(h * 0.01), int(w * 0.995), int(h * 0.12)),
            fill=(40, 28, 18),
        )

    dest.parent.mkdir(parents=True, exist_ok=True)
    out.save(dest, quality=95)
    print(
        f"wrote {dest.name} win=({x0},{y0},{x1},{y1}) bytes={dest.stat().st_size}",
        flush=True,
    )


def main() -> None:
    STILLS.mkdir(parents=True, exist_ok=True)
    FAIL.mkdir(parents=True, exist_ok=True)
    QA.mkdir(parents=True, exist_ok=True)

    plate02b = RAW_V01 / "02b_cards_sixty_three_v01.mp4"
    plate09 = RAW_V01 / "09_risk_bet_v01.mp4"
    plate09b = RAW_V01 / "09b_risk_hold_v01.mp4"
    if not plate02b.exists():
        raise SystemExit(f"missing {plate02b}")
    if not plate09.exists():
        raise SystemExit(f"missing {plate09}")
    if not plate09b.exists():
        raise SystemExit(f"missing {plate09b}")

    for t in (1.0, 3.0, 5.0, 7.0):
        grab(plate02b, t, FAIL / f"02b_fail_t{int(t)}.jpg")
        grab(plate09, t, FAIL / f"09_fail_t{int(t)}.jpg")
        grab(plate09b, t, FAIL / f"09b_fail_t{int(t)}.jpg")
    if ROUGH.exists():
        for t in (18.0, 19.0, 20.0, 21.0, 91.0, 95.0, 97.0):
            grab(ROUGH, t, FAIL / f"rough_t{int(t)}.jpg")

    # --- A) books: rectangular leather only ---
    rect_leather_book_top(FAIL / "02b_fail_t5.jpg", STILLS / "02b_books_clean_i2v.jpg")
    rect_leather_book_top(FAIL / "02b_fail_t3.jpg", STILLS / "02b_books_clean_alt.jpg")
    rect_leather_book_top(FAIL / "02b_fail_t1.jpg", STILLS / "02b_books_clean_t1.jpg")
    if (FAIL / "rough_t19.jpg").exists():
        rect_leather_book_top(
            FAIL / "rough_t19.jpg",
            STILLS / "02b_books_clean_from_rough.jpg",
            box_frac=(0.62, 0.30, 0.92, 0.60),
        )

    # --- B) A BET window: sky only, chair glow stays ---
    hard_scrub_window(
        FAIL / "09_fail_t5.jpg",
        STILLS / "09_risk_sky_i2v.jpg",
        WIN_09,
        moon_frac=(0.62, 0.12),
    )
    hard_scrub_window(
        FAIL / "09_fail_t3.jpg",
        STILLS / "09_risk_sky_alt.jpg",
        WIN_09,
        moon_frac=(0.60, 0.11),
    )
    hard_scrub_window(
        FAIL / "09b_fail_t3.jpg",
        STILLS / "09b_risk_sky_i2v.jpg",
        WIN_09B,
        moon_frac=(0.70, 0.14),
    )
    hard_scrub_window(
        FAIL / "09b_fail_t5.jpg",
        STILLS / "09b_risk_sky_alt.jpg",
        WIN_09B,
        moon_frac=(0.68, 0.13),
    )
    if (FAIL / "rough_t95.jpg").exists():
        hard_scrub_window(
            FAIL / "rough_t95.jpg",
            STILLS / "09_risk_sky_from_rough.jpg",
            WIN_ROUGH,
            moon_frac=(0.58, 0.12),
            strip_label=True,
        )

    for name in (
        "02b_books_clean_i2v.jpg",
        "02b_books_clean_alt.jpg",
        "09_risk_sky_i2v.jpg",
        "09b_risk_sky_i2v.jpg",
        "09_risk_sky_from_rough.jpg",
    ):
        src = STILLS / name
        if src.exists():
            (QA / f"scrub_{name}").write_bytes(src.read_bytes())

    print(f"OK v04 scrub stills → {STILLS}", flush=True)


if __name__ == "__main__":
    main()
