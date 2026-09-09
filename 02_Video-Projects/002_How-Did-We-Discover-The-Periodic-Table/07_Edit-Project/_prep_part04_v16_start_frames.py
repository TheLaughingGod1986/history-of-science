#!/usr/bin/env python3
"""Prep Part 04 v16 I2V start frames — LATE SHOTS SHARP (ghost-free).

Parent FAIL: hos_002_part04_rough_v15.mp4
  sha256 cd7a57b2979478a34ac7cc5fe5639aa156ae603b437674ccd724ab3fe994748c

Remint only: 10_family_before_weight · 11_publish_gaps · 11b_wait_and_hunt
Prefer clean sharp DNA (v01 publish / painted family) — never temporal-median mush.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

PROJ = Path(__file__).resolve().parents[1]
OUT = PROJ / "04_Generated-Clips/part04/refs/v16_start_frames"
QA = PROJ / "07_Edit-Project/_qa_part04_v16_prep"
META = OUT / "compose_meta.json"
ASSETS = Path.home() / ".cursor/projects/Users-benjaminoats-YouTube-History-Of-Science/assets"

FAIL_T110 = ASSETS / "fail_t110_family_ghost.jpg"
KEEP_T105 = ASSETS / "keep_t105_lamp.jpg"
RAW_11 = PROJ / "04_Generated-Clips/part04/raw/v01_fast/11_publish_gaps_v01.mp4"
RAW_11B = PROJ / "04_Generated-Clips/part04/raw/v01_fast/11b_wait_and_hunt_v01.mp4"
CUT_V15 = PROJ / "09_Final-Export/hos_002_part04_rough_v15.mp4"
W, H = 1920, 1080


def extract(clip: Path, t: float, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-ss", f"{t:.3f}", "-i", str(clip),
            "-frames:v", "1", "-vf", f"scale={W}:{H}:flags=lanczos",
            "-q:v", "2", str(dest),
        ],
        check=True,
    )


def cream_scrub_hot(im: Image.Image) -> Image.Image:
    rgb = im.convert("RGB")
    w, h = rgb.size
    px = rgb.load()
    wood, cream = (168, 122, 78), (242, 228, 198)
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            hot = (r >= 200 and g >= 90 and b <= 90 and (r - b) >= 110) or (
                r >= 230 and g >= 140 and b <= 110 and (r - b) >= 100
            )
            if not hot:
                continue
            if y < int(h * 0.28) and x < int(w * 0.28) and r > 245 and g > 235:
                continue
            t = 0.78
            target = cream if y < int(h * 0.45) else wood
            px[x, y] = (
                int((1 - t) * r + t * target[0]),
                int((1 - t) * g + t * target[1]),
                int((1 - t) * b + t * target[2]),
            )
    return rgb


def heal_left_mush(im: Image.Image) -> Image.Image:
    """Replace left-edge pixel mush with blurred right-neighbor wood/shelf DNA."""
    rgb = im.convert("RGB")
    w, h = rgb.size
    px = rgb.load()
    # sample clean band from mid-left → center
    for y in range(h):
        for x in range(0, int(w * 0.28)):
            r, g, b = px[x, y]
            # detect blocky/high-contrast mush: near-white jagged OR neon edges
            mush = (
                (r > 235 and g > 235 and b > 230 and y > int(h * 0.05))
                or (abs(r - g) > 70 and abs(r - b) > 70 and max(r, g, b) > 180)
                or (r > 210 and g < 120 and b > 160)  # magenta blotch
            )
            if not mush:
                # also heal ultra-jagged dark/light checker near left edge
                if x < int(w * 0.08) and ((x + y) % 7 == 0) and max(r, g, b) - min(r, g, b) > 90:
                    mush = True
            if not mush:
                continue
            sx = min(w - 1, int(w * 0.38) + (x % 40))
            sr, sg, sb = px[sx, y]
            # bias toward warm wood under desk, cooler shelf above
            if y > int(h * 0.55):
                sr, sg, sb = int(0.7 * sr + 0.3 * 160), int(0.7 * sg + 0.3 * 115), int(0.7 * sb + 0.3 * 70)
            px[x, y] = (sr, sg, sb)
    out = rgb.filter(ImageFilter.GaussianBlur(0.6))
    # re-blend center-right sharp over mild blur
    sharp = im.convert("RGB")
    mask = Image.new("L", (w, h), 0)
    md = ImageDraw.Draw(mask)
    md.rectangle((int(w * 0.22), 0, w, h), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(18))
    return Image.composite(sharp, out, mask)


def soft_panel_glow(im: Image.Image) -> Image.Image:
    rgba = im.convert("RGBA")
    w, h = rgba.size
    ov = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    x0, y0, x1, y1 = int(w * 0.42), int(h * 0.30), int(w * 0.58), int(h * 0.50)
    for pad, a in ((20, 30), (10, 55), (0, 85)):
        d.rounded_rectangle(
            (x0 - pad, y0 - pad, x1 + pad, y1 + pad),
            radius=12,
            fill=(255, 236, 190, a),
        )
    return Image.alpha_composite(rgba, ov.filter(ImageFilter.GaussianBlur(2.0))).convert("RGB")


def _font(size: int):
    for path in (
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Supplemental/Georgia Bold.ttf",
        "/Library/Fonts/Arial Bold.ttf",
    ):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def paint_element_card(
    canvas: Image.Image,
    center: tuple[int, int],
    symbol: str,
    number: str,
    *,
    angle: float = 0.0,
    scale: float = 1.0,
) -> None:
    """Paint one sharp cream element card (no ghost layers)."""
    cw, ch = int(210 * scale), int(280 * scale)
    card = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    d = ImageDraw.Draw(card)
    d.rounded_rectangle((2, 2, cw - 3, ch - 3), radius=18, fill=(248, 242, 228, 255))
    d.rounded_rectangle((2, 2, cw - 3, ch - 3), radius=18, outline=(55, 45, 35, 230), width=4)
    f_sym = _font(max(48, int(92 * scale)))
    f_num = _font(max(28, int(48 * scale)))
    bb = d.textbbox((0, 0), symbol, font=f_sym)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    d.text(((cw - tw) / 2, ch * 0.22), symbol, fill=(28, 24, 20, 255), font=f_sym)
    bb2 = d.textbbox((0, 0), number, font=f_num)
    tw2, th2 = bb2[2] - bb2[0], bb2[3] - bb2[1]
    d.text(((cw - tw2) / 2, ch * 0.62), number, fill=(45, 40, 35, 255), font=f_num)
    if abs(angle) > 0.1:
        card = card.rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)
    cx, cy = center
    x = cx - card.size[0] // 2
    y = cy - card.size[1] // 2
    canvas.alpha_composite(card, (x, y))


def paint_family_start(base: Image.Image) -> Image.Image:
    """Desk DNA + four sharp floating H/C/N/O cards — zero ghost doubles."""
    im = base.convert("RGB").resize((W, H), Image.Resampling.LANCZOS)
    im = cream_scrub_hot(im)
    im = heal_left_mush(im)
    # Fully rebuild mid/foreground so ZERO ghost layers from FAIL DNA remain.
    rgba = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    # keep upper background (lamp / shelves) from cleaned base
    top = im.crop((0, 0, W, int(H * 0.42))).convert("RGBA")
    rgba.paste(top, (0, 0))
    # paint solid warm desk surface for lower 60%
    desk = Image.new("RGBA", (W, int(H * 0.62)), (78, 52, 32, 255))
    dd = ImageDraw.Draw(desk)
    for i in range(0, desk.size[1], 6):
        shade = 78 + (i % 18) - 6
        dd.rectangle((0, i, W, i + 5), fill=(shade, int(shade * 0.68), int(shade * 0.42), 255))
    # warm lamp pool
    dd.ellipse(
        (int(W * 0.22), int(desk.size[1] * 0.05), int(W * 0.78), int(desk.size[1] * 0.75)),
        fill=(160, 115, 60, 200),
    )
    desk = desk.filter(ImageFilter.GaussianBlur(1.2))
    rgba.alpha_composite(desk, (0, int(H * 0.38)))
    # soft Empty Chairs panel behind cards
    panel = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pd = ImageDraw.Draw(panel)
    x0, y0, x1, y1 = int(W * 0.42), int(H * 0.26), int(W * 0.58), int(H * 0.44)
    for pad, a in ((18, 40), (8, 70), (0, 95)):
        pd.rounded_rectangle(
            (x0 - pad, y0 - pad, x1 + pad, y1 + pad),
            radius=12,
            fill=(255, 236, 190, a),
        )
    rgba = Image.alpha_composite(rgba, panel.filter(ImageFilter.GaussianBlur(1.5)))
    # sharp single cards only — no ghost layers underneath
    paint_element_card(rgba, (int(W * 0.18), int(H * 0.55)), "H", "1", angle=-8, scale=1.08)
    paint_element_card(rgba, (int(W * 0.38), int(H * 0.50)), "C", "12", angle=6, scale=1.10)
    paint_element_card(rgba, (int(W * 0.58), int(H * 0.52)), "N", "14", angle=-4, scale=1.12)
    paint_element_card(rgba, (int(W * 0.78), int(H * 0.56)), "O", "16", angle=10, scale=1.08)
    out = rgba.convert("RGB")
    return ImageEnhance.Sharpness(out).enhance(1.40)


def sharpen(im: Image.Image) -> Image.Image:
    return ImageEnhance.Sharpness(im.convert("RGB")).enhance(1.30)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QA.mkdir(parents=True, exist_ok=True)
    meta: dict = {
        "parent_v15_sha": "cd7a57b2979478a34ac7cc5fe5639aa156ae603b437674ccd724ab3fe994748c",
        "bible_main": "25bdefd",
        "plates": {},
        "method": "painted_sharp_family + clean_v01_publish_starts",
    }

    # --- plate 10: paint sharp floating cards on KEEP desk DNA (not fail ghosts) ---
    src10 = OUT / "_src_10_keep_desk.jpg"
    if KEEP_T105.exists():
        Image.open(KEEP_T105).convert("RGB").resize((W, H), Image.Resampling.LANCZOS).save(
            src10, quality=95
        )
    elif FAIL_T110.exists():
        # last resort — paint_family_start rebuilds mid band opaque
        Image.open(FAIL_T110).convert("RGB").resize((W, H), Image.Resampling.LANCZOS).save(
            src10, quality=95
        )
    else:
        extract(CUT_V15, 105.0, src10)
    family = paint_family_start(Image.open(src10))
    out10 = OUT / "10_family_before_weight_start_v16.jpg"
    family.save(out10, quality=95)
    family.save(QA / "start_10_family_sharp_v16.jpg", quality=92)
    meta["plates"]["10_family_before_weight"] = str(out10)

    # also stash KEEP lamp DNA reference (do not remint 09b)
    if KEEP_T105.exists():
        keep = Image.open(KEEP_T105).convert("RGB").resize((W, H), Image.Resampling.LANCZOS)
        keep.save(OUT / "keep_t105_lamp_ref.jpg", quality=92)
        keep.save(QA / "keep_t105_lamp_ref.jpg", quality=92)

    # --- plate 11: clean v01 publish desk (already sharp / no ghost) ---
    src11 = OUT / "_src_11_v01.jpg"
    extract(RAW_11, 1.5, src11)
    im11 = cream_scrub_hot(Image.open(src11))
    im11 = sharpen(im11)
    out11 = OUT / "11_publish_gaps_start_v16.jpg"
    im11.save(out11, quality=95)
    im11.save(QA / "start_11_publish_sharp_v16.jpg", quality=92)
    meta["plates"]["11_publish_gaps"] = str(out11)

    # --- plate 11b: clean v01 hunt desk ---
    src11b = OUT / "_src_11b_v01.jpg"
    extract(RAW_11B, 3.0, src11b)
    im11b = cream_scrub_hot(Image.open(src11b))
    im11b = sharpen(im11b)
    out11b = OUT / "11b_wait_and_hunt_start_v16.jpg"
    im11b.save(out11b, quality=95)
    im11b.save(QA / "start_11b_hunt_sharp_v16.jpg", quality=92)
    meta["plates"]["11b_wait_and_hunt"] = str(out11b)

    META.write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta, indent=2), flush=True)
    print("PREP OK", flush=True)


if __name__ == "__main__":
    main()
