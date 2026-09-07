#!/usr/bin/env python3
"""Compose I2V start frames for Part 04 v02 — scrub model-town window.

UAT FAIL v01 ~40–45s: glowing yellow-window toy houses outside lab window.
v02: same desk DNA; through window = night sky + moon/stars ONLY (no houses).
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


def _is_sky(r: int, g: int, b: int) -> bool:
    return b > r + 18 and b > g + 8 and b > 85 and r < 130


def _is_house_glow(r: int, g: int, b: int) -> bool:
    # Glowing yellow rectangular house windows (not warm lamp cream).
    return r > 175 and g > 145 and b < 115 and (r - b) > 55 and (g - b) > 35


def _is_house_body(r: int, g: int, b: int) -> bool:
    # Dark brown / silhouette house walls near glow.
    return r < 95 and g < 75 and b < 70 and (r + g + b) < 200 and max(r, g, b) > 25


def scrub_window_sky(im: Image.Image) -> Image.Image:
    """Remove glowing model-town houses in the night window → sky + moon only."""
    rgb = im.convert("RGB")
    w, h = rgb.size
    pix = rgb.load()

    # 1) Sky seed pixels in upper 55%.
    sky_pts: list[tuple[int, int]] = []
    for y in range(0, int(h * 0.55), 2):
        for x in range(0, w, 2):
            r, g, b = pix[x, y]
            if _is_sky(r, g, b):
                sky_pts.append((x, y))
    if not sky_pts:
        # Fallback night blue
        sky_color = (32, 48, 92)
        sky_bbox = (int(w * 0.25), int(h * 0.02), int(w * 0.78), int(h * 0.45))
    else:
        sx = [p[0] for p in sky_pts]
        sy = [p[1] for p in sky_pts]
        # Sky color = median-ish of seeds
        samples = [pix[x, y] for x, y in sky_pts[:: max(1, len(sky_pts) // 400)]]
        samples.sort(key=lambda c: c[2])
        sky_color = samples[len(samples) // 2]
        sky_bbox = (
            max(0, min(sx) - 8),
            max(0, min(sy) - 4),
            min(w - 1, max(sx) + 8),
            min(h - 1, max(sy) + 70),
        )

    x0, y0, x1, y1 = sky_bbox

    # 2) Mark house-glow + adjacent dark body pixels INSIDE sky bbox only.
    mask = Image.new("L", (w, h), 0)
    mp = mask.load()
    glow_n = 0
    for y in range(y0, y1):
        for x in range(x0, x1):
            r, g, b = pix[x, y]
            if _is_house_glow(r, g, b):
                mp[x, y] = 255
                glow_n += 1
            elif _is_house_body(r, g, b):
                # Only keep body if a glow is nearby (same window row-ish)
                near_glow = False
                for dy in range(-18, 19, 3):
                    for dx in range(-18, 19, 3):
                        xx, yy = x + dx, y + dy
                        if xx < x0 or xx >= x1 or yy < y0 or yy >= y1:
                            continue
                        rr, gg, bb = pix[xx, yy]
                        if _is_house_glow(rr, gg, bb):
                            near_glow = True
                            break
                    if near_glow:
                        break
                if near_glow:
                    mp[x, y] = 255

    # Dilate mask so whole house + roof is covered
    mask = mask.filter(ImageFilter.MaxFilter(15))
    mask = mask.filter(ImageFilter.MaxFilter(11))
    mask = mask.filter(ImageFilter.GaussianBlur(radius=2.2))

    # 3) Paint sky color through mask (opaque where mask strong)
    sky_layer = Image.new("RGB", (w, h), sky_color)
    # Soft moon disc near top-center of scrub region if no bright moon already
    moon_box = (int((x0 + x1) / 2) - 22, y0 + 8, int((x0 + x1) / 2) + 22, y0 + 52)
    moon_crop = rgb.crop(
        (
            max(0, moon_box[0] - 40),
            max(0, moon_box[1] - 10),
            min(w, moon_box[2] + 40),
            min(h, moon_box[3] + 30),
        )
    )
    bright = sum(
        1
        for p in moon_crop.getdata()
        if p[0] > 200 and p[1] > 200 and p[2] > 185 and (p[0] + p[1] + p[2]) > 620
    )
    md = ImageDraw.Draw(sky_layer)
    if bright < 120:
        cx = (moon_box[0] + moon_box[2]) // 2
        cy = (moon_box[1] + moon_box[3]) // 2
        rad = max(16, int(min(w, h) * 0.028))
        md.ellipse((cx - rad, cy - rad, cx + rad, cy + rad), fill=(236, 236, 248))
        for sx, sy in (
            (cx - rad * 3, cy + 6),
            (cx + rad * 2, cy - 4),
            (cx + rad, cy + rad + 10),
        ):
            if x0 <= sx < x1 and y0 <= sy < y1:
                md.ellipse((sx, sy, sx + 2, sy + 2), fill=(220, 225, 240))

    out = Image.composite(sky_layer, rgb, mask)

    # 4) If glow count was high, also force-fill a horizontal band under moon
    # (catches leftover rooflines the mask missed).
    if glow_n > 80:
        band = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        bd = ImageDraw.Draw(band)
        # Lower third of sky bbox = typical house row
        by0 = y0 + int((y1 - y0) * 0.35)
        bd.rectangle((x0, by0, x1, y1), fill=(*sky_color, 210))
        # Re-mask band by only painting where original still looks like house/glow
        band_rgb = Image.new("RGB", (w, h), sky_color)
        band_mask = Image.new("L", (w, h), 0)
        bmp = band_mask.load()
        for y in range(by0, y1):
            for x in range(x0, x1):
                r, g, b = pix[x, y]
                if _is_house_glow(r, g, b) or _is_house_body(r, g, b):
                    bmp[x, y] = 255
                # also mid-brown roofs
                elif 40 < r < 140 and 25 < g < 110 and b < 90 and r > b + 15:
                    bmp[x, y] = 200
        band_mask = band_mask.filter(ImageFilter.MaxFilter(13))
        band_mask = band_mask.filter(ImageFilter.GaussianBlur(radius=2.0))
        out = Image.composite(band_rgb, out, band_mask)

    return out.convert("RGB")


def save_scrub(src: Path, dest: Path) -> None:
    im = Image.open(src)
    out = scrub_window_sky(im)
    dest.parent.mkdir(parents=True, exist_ok=True)
    out.save(dest, quality=95)
    print(f"wrote {dest} bytes={dest.stat().st_size}", flush=True)


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

    save_scrub(FAIL / "05_fail_t4.jpg", STILLS / "05_columns_scrub_i2v.jpg")
    save_scrub(FAIL / "05_fail_t1.jpg", STILLS / "05_columns_scrub_alt.jpg")
    save_scrub(FAIL / "rough_t40_periodic_table.jpg", STILLS / "05_columns_scrub_from_rough.jpg")

    # Prefer clean desk_columns still (already night-sky) as extra start option
    clean_cols = STILLS_V01 / "desk_columns.jpg"
    if clean_cols.exists():
        # Still run scrub in case of faint leak
        save_scrub(clean_cols, STILLS / "05_desk_columns_clean.jpg")

    explorer_src = STILLS_V01 / "explorer_on_desk.jpg"
    if not explorer_src.exists():
        explorer_src = FAIL / "06_fail_t4.jpg"
    save_scrub(explorer_src, STILLS / "06_explorer_scrub_i2v.jpg")
    if (FAIL / "06_fail_t7.jpg").exists():
        save_scrub(FAIL / "06_fail_t7.jpg", STILLS / "06_explorer_scrub_alt.jpg")

    dna = STILLS_V01 / "desk_dna_t4.jpg"
    if dna.exists():
        save_scrub(dna, STILLS / "desk_dna_scrub_t4.jpg")

    # QA copies
    for name in (
        "05_columns_scrub_i2v.jpg",
        "05_columns_scrub_from_rough.jpg",
        "06_explorer_scrub_i2v.jpg",
        "05_desk_columns_clean.jpg",
    ):
        src = STILLS / name
        if src.exists():
            (QA / f"scrub_{name}").write_bytes(src.read_bytes())

    print(f"OK v02 scrub stills → {STILLS}", flush=True)


if __name__ == "__main__":
    main()
