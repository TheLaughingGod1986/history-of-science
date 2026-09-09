#!/usr/bin/env python3
"""Compose Part 04 v12 I2V start frames — CLEAN LIGHT + WRITTEN CARDS remint.

Parent FAIL: hos_002_part04_rough_v12.mp4 sha 96a0f41e…
HARD locks on reminted plates:
  1. CLEAN LIGHT — warm lamp glow ONLY (no chair fire, sparks, smoke, candle-lamp)
  2. WRITTEN CARDS — every visible card shows readable H/C/O/N/Eka marks
  3. Empty Chairs glow = soft chair glow NOT fire
  4. Prefer indoor wood/bookcase (no flat blue sky fills)

KEEP 06_explorer_leaves_gap. Starts bake writing + clean lamp into the still.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

PROJ = Path(__file__).resolve().parents[1]
DNA = PROJ / "04_Generated-Clips/part04/refs/v11_dna"
OUT_DIR = PROJ / "04_Generated-Clips/part04/refs/v13_start_frames"
META = OUT_DIR / "compose_meta.json"

RAW_V11 = PROJ / "04_Generated-Clips/part04/raw/v11_fast"
RAW_V12 = PROJ / "04_Generated-Clips/part04/raw/v12_fast"
RAW_V07 = PROJ / "04_Generated-Clips/part04/raw/v07_fast"
RAW_V01 = PROJ / "04_Generated-Clips/part04/raw/v01_fast"

SHEET = DNA / "character_sheet.jpg"
GERMS = DNA / "germs_lock.jpg"
P03 = DNA / "p03_keep.jpg"

# Element marks — short, phone-readable, period-table DNA
CARD_MARKS = [
    ("H", "1"),
    ("C", "12"),
    ("O", "16"),
    ("N", "14"),
    ("Li", "7"),
    ("Be", "9"),
    ("B", "11"),
    ("F", "19"),
    ("Na", "23"),
    ("Mg", "24"),
    ("Al", "27"),
    ("Si", "28"),
    ("Eka", "Al"),
    ("Eka", "B"),
    ("Eka", "Si"),
]


def extract_frame(clip: Path, t: float, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-ss", f"{t:.3f}", "-i", str(clip),
            "-frames:v", "1", "-q:v", "2", str(dest),
        ],
        check=True,
    )


def font(size: int) -> ImageFont.ImageFont:
    for path in (
        "/System/Library/Fonts/Supplemental/Georgia Bold.ttf",
        "/System/Library/Fonts/Supplemental/Times New Roman.ttf",
        "/Library/Fonts/Arial.ttf",
    ):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def scrub_fire_hotspots(im: Image.Image) -> Image.Image:
    """Kill candle flames / spark blobs only — leave warm lamp glow and skin alone."""
    rgb = im.convert("RGB")
    w, h = rgb.size
    px = rgb.load()
    wood = rgb.crop((int(w * 0.35), int(h * 0.55), int(w * 0.55), int(h * 0.75)))
    wood = wood.resize((w, h), Image.Resampling.BILINEAR)
    wp = wood.load()
    out = rgb.copy()
    op = out.load()
    for y in range(int(h * 0.18), int(h * 0.82)):
        for x in range(int(w * 0.15), int(w * 0.85)):
            r, g, b = px[x, y]
            # tight candle / chair-fire core: near-white-yellow / orange tip
            if r >= 225 and g >= 150 and b <= 100 and (r - b) >= 120:
                wr, wg, wb = wp[x, y]
                op[x, y] = (wr, wg, wb)
            elif r >= 245 and g >= 210 and b <= 130 and (r + g) >= 460:
                wr, wg, wb = wp[x, y]
                op[x, y] = (
                    int(0.15 * r + 0.85 * wr),
                    int(0.15 * g + 0.85 * wg),
                    int(0.08 * b + 0.92 * wb),
                )
    return out


def scrub_side_label(im: Image.Image) -> Image.Image:
    rgb = im.convert("RGB")
    w, h = rgb.size
    x0, y0 = int(w * 0.72), int(h * 0.02)
    x1, y1 = int(w * 0.99), int(h * 0.14)
    src = rgb.crop((int(w * 0.55), int(h * 0.02), int(w * 0.70), int(h * 0.14)))
    src = src.resize((x1 - x0, y1 - y0), Image.Resampling.LANCZOS)
    out = rgb.copy()
    out.paste(src, (x0, y0))
    mask = Image.new("L", (x1 - x0, y1 - y0), 0)
    d = ImageDraw.Draw(mask)
    d.rounded_rectangle((0, 0, x1 - x0 - 1, y1 - y0 - 1), radius=12, fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(4))
    blended = Image.composite(src, out.crop((x0, y0, x1, y1)), mask)
    out.paste(blended, (x0, y0))
    return out


def paint_card_marks(im: Image.Image, regions: list[tuple[float, float, float, float]]) -> Image.Image:
    """Draw readable element marks onto cream card stack regions (norm coords)."""
    out = im.convert("RGB")
    d = ImageDraw.Draw(out)
    w, h = out.size
    big = font(max(28, int(h * 0.045)))
    small = font(max(16, int(h * 0.028)))
    ink = (42, 28, 18)
    ink2 = (70, 48, 32)
    for i, (nx0, ny0, nx1, ny1) in enumerate(regions):
        x0, y0 = int(nx0 * w), int(ny0 * h)
        x1, y1 = int(nx1 * w), int(ny1 * h)
        cw, ch = max(8, x1 - x0), max(8, y1 - y0)
        # fill a cream card face then ink
        d.rounded_rectangle((x0, y0, x1, y1), radius=max(2, cw // 12), fill=(236, 226, 206))
        d.rounded_rectangle((x0, y0, x1, y1), radius=max(2, cw // 12), outline=(180, 160, 130), width=2)
        sym, num = CARD_MARKS[i % len(CARD_MARKS)]
        # center symbol
        bb = d.textbbox((0, 0), sym, font=big)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        tx = x0 + (cw - tw) // 2
        ty = y0 + max(2, (ch - th) // 2 - int(ch * 0.08))
        d.text((tx, ty), sym, fill=ink, font=big)
        bb2 = d.textbbox((0, 0), num, font=small)
        tw2 = bb2[2] - bb2[0]
        d.text((x0 + (cw - tw2) // 2, ty + th + 1), num, fill=ink2, font=small)
    return out


def paste_glasses_on_profile(desk: Image.Image, face_ref: Image.Image) -> Image.Image:
    """Draw clean round gold wire-rim glasses on Explorer head (no face-crop paste).

    Prefer PROFILE lean so both rims read. Avoid Germs face stamp (causes glitch).
    """
    del face_ref  # identity lock lives in prompt + DNA refs; start uses drawn rims only
    out = desk.convert("RGB")
    w, h = out.size
    d = ImageDraw.Draw(out, "RGBA")
    # Toy-scale Explorer head — mid frame on plate 06 back/profile
    hx, hy = int(w * 0.47), int(h * 0.36)
    r = max(9, int(h * 0.022))
    gold = (210, 175, 85, 255)
    dark = (55, 40, 25, 220)
    # Profile: one clear round lens on the visible side + thin temple arm
    d.ellipse((hx - r, hy - r, hx + r, hy + r), outline=gold, width=3)
    d.ellipse((hx - r + 2, hy - r + 2, hx + r - 2, hy + r - 2), outline=dark, width=1)
    # second rim slightly behind (depth)
    d.ellipse((hx + int(r * 0.9), hy - r + 1, hx + int(2.7 * r), hy + r - 1), outline=gold, width=2)
    d.line((hx + r - 1, hy, hx + int(r * 0.9), hy), fill=gold, width=2)
    # temple along head toward ear
    d.line((hx + int(2.7 * r), hy, hx + int(3.6 * r), hy + 2), fill=gold, width=2)
    return out


def indoor_bookcase_fill(im: Image.Image) -> Image.Image:
    """Replace night-window / moon band with wood/bookcase clone (full cover)."""
    rgb = im.convert("RGB")
    w, h = rgb.size
    # Prefer right bookcase; fallback mid wood
    src = rgb.crop((int(w * 0.58), int(h * 0.02), int(w * 0.98), int(h * 0.62)))
    x0, y0 = int(w * 0.00), int(h * 0.00)
    x1, y1 = int(w * 0.48), int(h * 0.58)
    patch = src.resize((x1 - x0, y1 - y0), Image.Resampling.LANCZOS)
    out = rgb.copy()
    # Soft full paste for window half, then keep warm desk objects by luminance gate
    mask = Image.new("L", (x1 - x0, y1 - y0), 0)
    md = ImageDraw.Draw(mask)
    md.rectangle((0, 0, x1 - x0 - 1, y1 - y0 - 1), fill=255)
    # Feather right edge so desk props survive
    for i in range(40):
        alpha = int(255 * (1.0 - i / 40.0))
        md.rectangle((x1 - x0 - 40 + i, 0, x1 - x0 - 39 + i, y1 - y0 - 1), fill=alpha)
    mask = mask.filter(ImageFilter.GaussianBlur(6))
    region = out.crop((x0, y0, x1, y1))
    # Only replace cool/dark sky & bright moon pixels inside mask
    rp = region.load()
    pp = patch.load()
    mp = mask.load()
    for y in range(y1 - y0):
        for x in range(x1 - x0):
            a = mp[x, y]
            if a < 8:
                continue
            r, g, b = rp[x, y]
            lum = (r + g + b) / 3.0
            is_sky = b > r + 12 and b > g + 6 and b > 55 and lum < 170
            is_moon = lum > 190 and abs(r - g) < 25 and abs(g - b) < 25
            is_frame_glass = lum < 90 and b >= r
            if is_sky or is_moon or is_frame_glass:
                sr, sg, sb = pp[x, y]
                t = a / 255.0
                rp[x, y] = (
                    int(r * (1 - t) + sr * t),
                    int(g * (1 - t) + sg * t),
                    int(b * (1 - t) + sb * t),
                )
    out.paste(region, (x0, y0))
    return out



def soft_chair_glow(im: Image.Image) -> Image.Image:
    """Soft Empty-Chairs rectangular backrest glow — NEVER flames / seat fire."""
    out = im.convert("RGBA")
    w, h = out.size
    # scrub any residual bright fire cores in chair band before painting glow
    rgb = out.convert("RGB")
    px = rgb.load()
    for y in range(int(h * 0.20), int(h * 0.70)):
        for x in range(int(w * 0.30), int(w * 0.70)):
            r, g, b = px[x, y]
            if r >= 220 and g >= 200 and b >= 180 and (r + g + b) >= 640:
                px[x, y] = (int(r * 0.35 + 90), int(g * 0.35 + 70), int(b * 0.35 + 50))
            elif r >= 230 and g >= 160 and b <= 110 and (r - b) >= 110:
                px[x, y] = (110, 85, 60)
    out = rgb.convert("RGBA")
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    # soft RECTANGULAR backrest panel glow only (not seat fire)
    d.rounded_rectangle(
        (int(w * 0.40), int(h * 0.18), int(w * 0.60), int(h * 0.42)),
        radius=10,
        fill=(255, 236, 190, 70),
    )
    glow = overlay.filter(ImageFilter.GaussianBlur(14))
    return Image.alpha_composite(out, glow).convert("RGB")


def compose_06() -> Path:
    clip = RAW_V10 / "06_explorer_leaves_gap_v10.mp4"
    base = OUT_DIR / "_raw_06_t1.jpg"
    extract_frame(clip, 1.0, base)
    im = Image.open(base)
    im = scrub_side_label(im)
    im = scrub_fire_hotspots(im)
    # card stacks in foreground of plate 06
    im = paint_card_marks(
        im,
        [
            (0.16, 0.58, 0.28, 0.78),
            (0.28, 0.56, 0.40, 0.76),
            (0.40, 0.54, 0.52, 0.74),
            (0.18, 0.74, 0.30, 0.90),
            (0.32, 0.72, 0.44, 0.88),
            (0.44, 0.70, 0.56, 0.86),
            (0.52, 0.52, 0.62, 0.68),
        ],
    )
    face = Image.open(GERMS if GERMS.exists() else SHEET)
    im = paste_glasses_on_profile(im, face)
    out = OUT_DIR / "06_explorer_leaves_gap_start_v11.jpg"
    im.save(out, quality=94)
    return out


def compose_desk(
    pid: str,
    clip: Path,
    t: float,
    regions: list[tuple[float, float, float, float]],
    *,
    scrub_window: bool,
    chair_glow: bool = False,
) -> Path:
    base = OUT_DIR / f"_raw_{pid}.jpg"
    extract_frame(clip, t, base)
    im = Image.open(base)
    im = scrub_side_label(im)
    im = scrub_fire_hotspots(im)
    if chair_glow:
        im = scrub_fire_hotspots(im)
        im = soft_chair_glow(im)
    if scrub_window:
        im = indoor_bookcase_fill(im)
    im = paint_card_marks(im, regions)
    out = OUT_DIR / f"{pid}_start_v13.jpg"
    im.save(out, quality=94)
    return out


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    outs: dict[str, str] = {}

    # Remint ONLY failing plates — KEEP 06 + cleared v12 takes
    jobs = [
        (
            "04_sort_atomic_weight",
            RAW_V12 / "04_sort_atomic_weight_v12.mp4",
            2.0,
            [
                # five stack tops across desk
                (0.18, 0.52, 0.30, 0.70),
                (0.32, 0.50, 0.44, 0.68),
                (0.46, 0.50, 0.58, 0.68),
                (0.60, 0.52, 0.72, 0.70),
                (0.74, 0.54, 0.86, 0.72),
                # flat cards
                (0.10, 0.72, 0.22, 0.88),
                (0.78, 0.74, 0.90, 0.90),
                # mid uprights
                (0.36, 0.34, 0.48, 0.52),
                (0.50, 0.34, 0.62, 0.52),
            ],
            True,
            False,
        ),
        (
            "05_columns_families",
            RAW_V12 / "05_columns_families_v12.mp4",
            3.0,
            [
                # every stack top + outer blanks from fail_blank_40/42
                (0.16, 0.50, 0.28, 0.70),
                (0.30, 0.48, 0.42, 0.68),
                (0.44, 0.48, 0.56, 0.68),
                (0.58, 0.48, 0.70, 0.68),
                (0.72, 0.50, 0.84, 0.70),
                # flat left/right blanks
                (0.08, 0.74, 0.20, 0.90),
                (0.80, 0.74, 0.92, 0.90),
                # upright heroes
                (0.34, 0.30, 0.46, 0.48),
                (0.48, 0.30, 0.60, 0.48),
                (0.62, 0.32, 0.74, 0.50),
            ],
            False,
            False,
        ),
        (
            "09_risk_bet",
            RAW_V12 / "09_risk_bet_v12.mp4",
            2.0,
            [
                # large foreground hero cards (fail_blank_98)
                (0.08, 0.62, 0.28, 0.92),
                (0.30, 0.62, 0.50, 0.92),
                (0.52, 0.62, 0.72, 0.92),
                (0.18, 0.48, 0.34, 0.66),
                (0.40, 0.48, 0.56, 0.66),
            ],
            False,
            True,
        ),
        (
            "09b_risk_hold",
            RAW_V12 / "09b_risk_hold_v12.mp4",
            2.0,
            [
                (0.20, 0.58, 0.36, 0.78),
                (0.38, 0.56, 0.54, 0.76),
                (0.56, 0.58, 0.72, 0.78),
                (0.12, 0.72, 0.28, 0.90),
                (0.68, 0.72, 0.84, 0.90),
            ],
            False,
            True,
        ),
    ]

    for pid, clip, t, regions, scrub_window, chair_glow in jobs:
        if not clip.exists():
            raise SystemExit(f"missing source clip for {pid}: {clip}")
        outs[pid] = str(
            compose_desk(
                pid,
                clip,
                t,
                regions,
                scrub_window=scrub_window,
                chair_glow=chair_glow,
            )
        )
        print(f"OK {pid} → {Path(outs[pid]).name}", flush=True)

    meta = {
        "out_dir": str(OUT_DIR),
        "starts": outs,
        "remint_plates": list(outs.keys()),
        "keep": ["06_explorer_leaves_gap", "05b_families_settle", "07_eka_placeholders", "08_prediction_navigation", "08b_navigation_walk", "10_family_before_weight", "02b_cards_sixty_three", "P01-P03"],
        "locks": [
            "lamp_clean_no_fire_sparks_smoke",
            "cards_have_writing_H_C_O_N_Eka",
            "soft_chair_glow_not_fire",
            "indoor_wood_bookcase_prefer",
        ],
        "parent_fail": "hos_002_part04_rough_v12.mp4",
        "parent_sha": "175c40a948a24899507266d3f4bccf39f9f51a2906441cae4557bcbd312fe6c2",
    }
    META.write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps({"starts": list(outs)}, indent=2), flush=True)


if __name__ == "__main__":
    main()
