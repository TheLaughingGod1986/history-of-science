#!/usr/bin/env python3
"""Prep Part 04 v20 Flow start frames — UAT HARD FAIL bible 43d9405 (parent v19).

Parent FAIL: hos_002_part04_rough_v19.mp4
  sha256 69d48f6e5fac419df5c23c17df5d0ef628cb4e8d533ba085bb3c8a173016bcdf

Heal DNA before I2V:
  06 — dense finished crown (fill scalp black-hole pits), smooth warm lamp,
       stamp readable H1 / C12 / N14 / O16 cards (never C1/N12)
  11 / 11b — single-exposure desk DNA, soft lamp, locked-camera friendly

NO paint on finished gallery mp4s. Start-frame hygiene only.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

PROJ = Path(__file__).resolve().parents[1]
OUT = PROJ / "04_Generated-Clips/part04/refs/v20_start_frames"
QA = PROJ / "07_Edit-Project/_qa_part04_v20_prep"
META = OUT / "compose_meta.json"
SRC19 = PROJ / "04_Generated-Clips/part04/refs/v19_start_frames"
KEEP_EXPLORER = PROJ / "04_Generated-Clips/part04/refs/v19_fail_keep/keep_explorer_back.jpg"
PARENT_V19_SHA = "69d48f6e5fac419df5c23c17df5d0ef628cb4e8d533ba085bb3c8a173016bcdf"
W, H = 1920, 1080


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


def fit_cover(src: Path) -> Image.Image:
    im = Image.open(src).convert("RGB")
    sw, sh = im.size
    scale = max(W / sw, H / sh)
    nw, nh = int(sw * scale), int(sh * scale)
    im = im.resize((nw, nh), Image.Resampling.LANCZOS)
    left = (nw - W) // 2
    top = (nh - H) // 2
    return im.crop((left, top, left + W, top + H))


def heal_scalp_pits(im: Image.Image) -> Image.Image:
    """Fill near-black circular pits in the crown with local hair colour."""
    rgb = im.convert("RGB")
    w, h = rgb.size
    px = rgb.load()
    x0, x1 = int(w * 0.28), int(w * 0.72)
    y0, y1 = int(h * 0.08), int(h * 0.48)
    healed = 0
    for y in range(y0, y1):
        for x in range(x0, x1):
            r, g, b = px[x, y]
            if max(r, g, b) <= 42 and abs(r - g) < 18 and abs(g - b) < 18:
                samples = []
                for rad in (6, 10, 14, 18):
                    for ang in range(0, 360, 30):
                        sx = int(x + rad * math.cos(math.radians(ang)))
                        sy = int(y + rad * math.sin(math.radians(ang)))
                        if x0 <= sx < x1 and y0 <= sy < y1:
                            sr, sg, sb = px[sx, sy]
                            if max(sr, sg, sb) > 55:
                                samples.append((sr, sg, sb))
                if samples:
                    n = len(samples)
                    px[x, y] = (
                        sum(s[0] for s in samples) // n,
                        sum(s[1] for s in samples) // n,
                        sum(s[2] for s in samples) // n,
                    )
                    healed += 1
    if healed:
        blur = rgb.filter(ImageFilter.GaussianBlur(1.1))
        out = rgb.copy()
        opx = out.load()
        bpx = blur.load()
        for y in range(y0, y1):
            for x in range(x0, x1):
                r, g, b = opx[x, y]
                if max(r, g, b) < 120:
                    br, bg, bb = bpx[x, y]
                    opx[x, y] = (
                        int(0.55 * r + 0.45 * br),
                        int(0.55 * g + 0.45 * bg),
                        int(0.55 * b + 0.45 * bb),
                    )
        rgb = out
    print(f"  scalp pits healed pixels≈{healed}", flush=True)
    return rgb


def densify_crown(im: Image.Image) -> Image.Image:
    rgb = im.convert("RGB")
    px = rgb.load()
    w, h = rgb.size
    x0, x1 = int(w * 0.30), int(w * 0.70)
    y0, y1 = int(h * 0.10), int(h * 0.46)
    for y in range(y0, y1):
        for x in range(x0, x1):
            r, g, b = px[x, y]
            if 45 < r < 140 and 25 < g < 110 and b < 90 and (r - b) > 15:
                px[x, y] = (
                    min(255, int(r * 1.06)),
                    min(255, int(g * 1.04)),
                    min(255, int(b * 1.02)),
                )
    return rgb


def smooth_lamp_glow(im: Image.Image) -> Image.Image:
    rgb = im.convert("RGB")
    warm = rgb.copy()
    px = warm.load()
    w, h = warm.size
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            if r > 150 and g > 100 and b < 140 and (r - b) > 40:
                continue
            px[x, y] = (0, 0, 0)
    soft = warm.filter(ImageFilter.GaussianBlur(12))
    bp = rgb.load()
    sp = soft.load()
    for y in range(h):
        for x in range(w):
            sr, sg, sb = sp[x, y]
            if sr + sg + sb < 30:
                continue
            r, g, b = bp[x, y]
            bp[x, y] = (
                int(0.35 * r + 0.65 * sr),
                int(0.35 * g + 0.65 * sg),
                int(0.45 * b + 0.55 * sb),
            )
    return rgb


def paint_element_card(
    canvas: Image.Image,
    center: tuple[int, int],
    symbol: str,
    number: str,
    *,
    angle: float = 0.0,
    scale: float = 1.0,
) -> None:
    cw, ch = int(150 * scale), int(200 * scale)
    card = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    d = ImageDraw.Draw(card)
    d.rounded_rectangle((2, 2, cw - 3, ch - 3), radius=14, fill=(252, 248, 236, 255))
    d.rounded_rectangle((2, 2, cw - 3, ch - 3), radius=14, outline=(40, 32, 24, 240), width=3)
    f_sym = _font(max(40, int(72 * scale)))
    f_num = _font(max(24, int(40 * scale)))
    bb = d.textbbox((0, 0), symbol, font=f_sym)
    tw = bb[2] - bb[0]
    d.text(((cw - tw) / 2, ch * 0.18), symbol, fill=(24, 20, 16, 255), font=f_sym)
    bb2 = d.textbbox((0, 0), number, font=f_num)
    tw2 = bb2[2] - bb2[0]
    d.text(((cw - tw2) / 2, ch * 0.58), number, fill=(40, 34, 28, 255), font=f_num)
    if abs(angle) > 0.1:
        card = card.rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)
    cx, cy = center
    canvas.alpha_composite(card, (cx - card.size[0] // 2, cy - card.size[1] // 2))


def stamp_correct_cards(im: Image.Image) -> Image.Image:
    rgba = im.convert("RGBA")
    cover = Image.new("RGBA", rgba.size, (0, 0, 0, 0))
    cd = ImageDraw.Draw(cover)
    cd.rounded_rectangle(
        (int(W * 0.30), int(H * 0.58), int(W * 0.78), int(H * 0.92)),
        radius=18,
        fill=(92, 64, 40, 235),
    )
    rgba = Image.alpha_composite(rgba, cover.filter(ImageFilter.GaussianBlur(0.8)))
    paint_element_card(rgba, (int(W * 0.36), int(H * 0.74)), "H", "1", angle=-6, scale=0.92)
    paint_element_card(rgba, (int(W * 0.48), int(H * 0.72)), "C", "12", angle=4, scale=0.95)
    paint_element_card(rgba, (int(W * 0.60), int(H * 0.73)), "N", "14", angle=-3, scale=0.95)
    paint_element_card(rgba, (int(W * 0.72), int(H * 0.75)), "O", "16", angle=7, scale=0.92)
    return rgba.convert("RGB")


def deghost_desk(im: Image.Image) -> Image.Image:
    rgb = im.convert("RGB")
    soft = rgb.filter(ImageFilter.GaussianBlur(0.7))
    sharp = ImageEnhance.Sharpness(rgb).enhance(1.15)
    return Image.blend(soft, sharp, 0.72)


def prep_explorer() -> Path:
    src = KEEP_EXPLORER if KEEP_EXPLORER.exists() else SRC19 / "06_explorer_leaves_gap_start_v19.jpg"
    if not src.exists():
        raise SystemExit(f"missing explorer source {src}")
    im = fit_cover(src)
    im = heal_scalp_pits(im)
    im = densify_crown(im)
    im = smooth_lamp_glow(im)
    im = stamp_correct_cards(im)
    im = ImageEnhance.Sharpness(im).enhance(1.12)
    dest = OUT / "06_explorer_leaves_gap_start_v20.jpg"
    im.save(dest, quality=95)
    im.save(QA / "start_06_explorer_leaves_gap.jpg", quality=92)
    return dest


def prep_publish(pid: str) -> Path:
    src = SRC19 / f"{pid}_start_v19.jpg"
    if not src.exists():
        raise SystemExit(f"missing {src}")
    im = fit_cover(src)
    im = smooth_lamp_glow(im)
    im = deghost_desk(im)
    im = ImageEnhance.Sharpness(im).enhance(1.18)
    dest = OUT / f"{pid}_start_v20.jpg"
    im.save(dest, quality=95)
    im.save(QA / f"start_{pid}.jpg", quality=92)
    return dest


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QA.mkdir(parents=True, exist_ok=True)
    meta = {
        "parent_v19_sha": PARENT_V19_SHA,
        "bible_main": "43d9405",
        "plates": {},
        "method": (
            "explorer=heal scalp pits + densify crown + smooth lamp + stamp H1/C12/N14/O16; "
            "publish=v19 desk DNA + smooth lamp + mild deghost; locked-camera prompts in mint"
        ),
        "remint": ["06_explorer_leaves_gap", "11_publish_gaps", "11b_wait_and_hunt"],
        "keep_assemble": ["10_family_before_weight", "09_risk_bet", "09b_risk_hold"],
    }
    d06 = prep_explorer()
    meta["plates"]["06_explorer_leaves_gap"] = str(d06)
    print(f"wrote {d06.name}", flush=True)
    for pid in ("11_publish_gaps", "11b_wait_and_hunt"):
        d = prep_publish(pid)
        meta["plates"][pid] = str(d)
        print(f"wrote {d.name}", flush=True)
    META.write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta, indent=2), flush=True)
    print("PREP OK", flush=True)


if __name__ == "__main__":
    main()
