#!/usr/bin/env python3
"""Compose Part 04 v11 I2V start frames — Ben FAIL remint locks.

Ben blockers (HARD):
  1. Explorer: round gold/wire glasses ALWAYS visible (profile/back OK but glasses readable)
  2. Lamp clean: warm glow ONLY — no fire spit, sparks, candle flames
  3. Cards have writing: H/C/O/Eka-/atomic marks — never blank cream stacks

Starts bake writing + glasses into the still so Veo I2V inherits them.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

PROJ = Path(__file__).resolve().parents[1]
DNA = PROJ / "04_Generated-Clips/part04/refs/v11_dna"
OUT_DIR = PROJ / "04_Generated-Clips/part04/refs/v11_start_frames"
META = OUT_DIR / "compose_meta.json"

RAW_V10 = PROJ / "04_Generated-Clips/part04/raw/v10_fast"
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
    for y in range(int(h * 0.30), int(h * 0.72)):
        for x in range(int(w * 0.25), int(w * 0.70)):
            r, g, b = px[x, y]
            # tight candle core: near-white-yellow / orange tip, very bright
            if r >= 230 and g >= 170 and b <= 90 and (r - b) >= 140:
                wr, wg, wb = wp[x, y]
                op[x, y] = (wr, wg, wb)
            elif r >= 245 and g >= 220 and b <= 120 and (r + g) >= 470:
                wr, wg, wb = wp[x, y]
                op[x, y] = (
                    int(0.2 * r + 0.8 * wr),
                    int(0.2 * g + 0.8 * wg),
                    int(0.1 * b + 0.9 * wb),
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


def compose_desk(pid: str, clip: Path, t: float, regions: list[tuple[float, float, float, float]], *, scrub_window: bool) -> Path:
    base = OUT_DIR / f"_raw_{pid}.jpg"
    extract_frame(clip, t, base)
    im = Image.open(base)
    im = scrub_side_label(im)
    im = scrub_fire_hotspots(im)
    if scrub_window:
        im = indoor_bookcase_fill(im)
    im = paint_card_marks(im, regions)
    out = OUT_DIR / f"{pid}_start_v11.jpg"
    im.save(out, quality=94)
    return out


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    outs: dict[str, str] = {}

    outs["06_explorer_leaves_gap"] = str(compose_06())

    # Eka-boron FAIL was 05b still language (scalloped blank hero + moon)
    outs["05b_families_settle"] = str(
        compose_desk(
            "05b_families_settle",
            RAW_V01 / "05b_families_settle_v01.mp4",
            4.0,
            [
                (0.38, 0.55, 0.62, 0.88),
                (0.18, 0.48, 0.30, 0.68),
                (0.64, 0.50, 0.76, 0.70),
                (0.30, 0.42, 0.40, 0.58),
            ],
            scrub_window=True,
        )
    )
    outs["07_eka_placeholders"] = str(
        compose_desk(
            "07_eka_placeholders",
            RAW_V01 / "07_eka_placeholders_v01.mp4",
            2.0,
            [
                (0.35, 0.50, 0.55, 0.82),
                (0.15, 0.45, 0.28, 0.68),
                (0.58, 0.48, 0.72, 0.72),
            ],
            scrub_window=True,
        )
    )
    outs["07b_eka_names_rotate"] = str(
        compose_desk(
            "07b_eka_names_rotate",
            RAW_V01 / "07b_eka_names_rotate_v01.mp4",
            1.0,
            [
                (0.40, 0.52, 0.60, 0.85),
                (0.20, 0.40, 0.32, 0.62),
                (0.62, 0.42, 0.74, 0.64),
                (0.48, 0.35, 0.58, 0.50),
            ],
            scrub_window=True,
        )
    )
    outs["09_risk_bet"] = str(
        compose_desk(
            "09_risk_bet",
            RAW_V07 / "09_risk_bet_v07.mp4",
            1.0,
            [
                (0.12, 0.48, 0.26, 0.72),
                (0.40, 0.55, 0.52, 0.72),
                (0.52, 0.58, 0.64, 0.74),
                (0.34, 0.62, 0.46, 0.78),
                (0.58, 0.62, 0.70, 0.78),
            ],
            scrub_window=False,
        )
    )
    outs["09b_risk_hold"] = str(
        compose_desk(
            "09b_risk_hold",
            RAW_V07 / "09b_risk_hold_v07.mp4",
            4.0,
            [
                (0.35, 0.58, 0.48, 0.74),
                (0.48, 0.60, 0.60, 0.76),
                (0.22, 0.55, 0.34, 0.70),
                (0.55, 0.52, 0.66, 0.68),
            ],
            scrub_window=False,
        )
    )

    meta = {
        "out_dir": str(OUT_DIR),
        "starts": outs,
        "locks": [
            "glasses_visible_on_explorer",
            "lamp_clean_no_fire_spit_no_candle",
            "cards_have_writing_H_C_O_Eka",
            "explorer_profile_back_only",
            "indoor_wood_bookcase_prefer",
        ],
        "dna": [str(SHEET), str(GERMS), str(P03)],
        "ben_fail_refs": [
            "fail_explorer_no_glasses.png",
            "fail_eka_boron_blank_fire.png",
            "fail_abet_blank_cards.png",
            "fail_blank_card_hero.png",
        ],
    }
    META.write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta, indent=2), flush=True)
    for k, v in outs.items():
        print(f"OK {k} → {v}", flush=True)


if __name__ == "__main__":
    main()
