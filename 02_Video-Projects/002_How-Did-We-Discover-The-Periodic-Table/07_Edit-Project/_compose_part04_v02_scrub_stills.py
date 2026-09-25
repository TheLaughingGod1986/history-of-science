#!/usr/bin/env python3
"""Compose I2V start frames for Part 04 v02 — scrub model-town window.

UAT FAIL v01 ~40–45s: glowing yellow-window toy houses outside lab window.
v02: hard-fill window glass with night sky + moon/stars ONLY (opaque).
"""
from __future__ import annotations

import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

PROJ = Path(__file__).resolve().parents[1]
RAW_V01 = PROJ / "04_Generated-Clips/part04/raw/v01_fast"
STILLS_V01 = PROJ / "04_Generated-Clips/part04/refs/v01_stills"
STILLS = PROJ / "04_Generated-Clips/part04/refs/v02_stills"
FAIL = STILLS / "ben_fail"
ROUGH = PROJ / "09_Final-Export/hos_002_part04_rough_v01.mp4"
QA = PROJ / "07_Edit-Project/_qa_part04_v02_spot"


def grab(src: Path, ss: float, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-ss", str(ss), "-i", str(src), "-frames:v", "1", str(dest),
        ],
        check=True,
    )


def hard_scrub_window(
    src: Path,
    dest: Path,
    box_frac: tuple[float, float, float, float],
    moon_frac: tuple[float, float] = (0.55, 0.11),
    strip_label: bool = False,
) -> None:
    """Opaque night-sky fill over window glass — removes model-town houses."""
    im = Image.open(src).convert("RGB")
    w, h = im.size
    x0 = int(w * box_frac[0])
    y0 = int(h * box_frac[1])
    x1 = int(w * box_frac[2])
    y1 = int(h * box_frac[3])

    sky_rgb = Image.new("RGB", (w, h), (26, 40, 82))
    sd = ImageDraw.Draw(sky_rgb)
    mx, my = int(w * moon_frac[0]), int(h * moon_frac[1])
    rad = max(20, int(min(w, h) * 0.034))
    sd.ellipse((mx - rad, my - rad, mx + rad, my + rad), fill=(236, 236, 250))
    for sx, sy in (
        (mx - rad * 2.8, my + 10),
        (mx + rad * 2.0, my - 8),
        (mx + 12, my + rad * 1.8),
        (mx - rad, my + rad * 2.2),
    ):
        sd.ellipse((int(sx), int(sy), int(sx) + 2, int(sy) + 2), fill=(220, 225, 240))

    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rectangle((x0, y0, x1, y1), fill=255)
    soft = mask.filter(ImageFilter.GaussianBlur(radius=3))
    inset = Image.new("L", (w, h), 0)
    ImageDraw.Draw(inset).rectangle((x0 + 6, y0 + 6, x1 - 6, y1 - 6), fill=255)
    mask = Image.composite(inset, soft, inset)

    out = Image.composite(sky_rgb, im, mask)
    if strip_label:
        # Rough frames bake PERIODIC TABLE / EMPTY SEATS overlays — strip for I2V.
        d = ImageDraw.Draw(out)
        d.rectangle((int(w * 0.68), int(h * 0.01), int(w * 0.99), int(h * 0.13)), fill=(26, 40, 82))

    dest.parent.mkdir(parents=True, exist_ok=True)
    out.save(dest, quality=95)
    print(f"wrote {dest.name} box=({x0},{y0},{x1},{y1}) bytes={dest.stat().st_size}", flush=True)


def main() -> None:
    STILLS.mkdir(parents=True, exist_ok=True)
    FAIL.mkdir(parents=True, exist_ok=True)
    QA.mkdir(parents=True, exist_ok=True)

    plate05 = RAW_V01 / "05_columns_families_v01.mp4"
    plate06 = RAW_V01 / "06_explorer_leaves_gap_v01.mp4"
    if plate05.exists():
        grab(plate05, 1.0, FAIL / "05_fail_t1.jpg")
        grab(plate05, 4.0, FAIL / "05_fail_t4.jpg")
        grab(plate05, 7.0, FAIL / "05_fail_t7.jpg")
    if plate06.exists():
        grab(plate06, 1.0, FAIL / "06_fail_t1.jpg")
        grab(plate06, 4.0, FAIL / "06_fail_t4.jpg")
        grab(plate06, 7.0, FAIL / "06_fail_t7.jpg")
    if ROUGH.exists():
        grab(ROUGH, 40.0, FAIL / "rough_t40_periodic_table.jpg")
        grab(ROUGH, 45.0, FAIL / "rough_t45_empty_seats.jpg")

    # Full-width opaque window cover (houses leaked on right with smaller boxes).
    box05 = (0.12, 0.00, 0.95, 0.55)
    hard_scrub_window(FAIL / "05_fail_t4.jpg", STILLS / "05_columns_scrub_i2v.jpg", box05)
    hard_scrub_window(FAIL / "05_fail_t1.jpg", STILLS / "05_columns_scrub_alt.jpg", box05)

    box_r = (0.15, 0.00, 0.92, 0.52)
    hard_scrub_window(
        FAIL / "rough_t40_periodic_table.jpg",
        STILLS / "05_columns_scrub_from_rough.jpg",
        box_r,
        strip_label=True,
    )

    explorer = STILLS_V01 / "explorer_on_desk.jpg"
    if explorer.exists():
        hard_scrub_window(
            explorer,
            STILLS / "06_explorer_scrub_i2v.jpg",
            (0.48, 0.00, 0.995, 0.45),
            moon_frac=(0.78, 0.10),
        )
    if (FAIL / "06_fail_t7.jpg").exists():
        hard_scrub_window(
            FAIL / "06_fail_t7.jpg",
            STILLS / "06_explorer_scrub_alt.jpg",
            (0.40, 0.00, 0.995, 0.48),
            moon_frac=(0.75, 0.10),
        )

    # QA previews
    for name in (
        "05_columns_scrub_i2v.jpg",
        "05_columns_scrub_from_rough.jpg",
        "06_explorer_scrub_i2v.jpg",
    ):
        src = STILLS / name
        if src.exists():
            (QA / f"scrub_{name}").write_bytes(src.read_bytes())

    print(f"OK v02 scrub stills → {STILLS}", flush=True)


if __name__ == "__main__":
    main()
