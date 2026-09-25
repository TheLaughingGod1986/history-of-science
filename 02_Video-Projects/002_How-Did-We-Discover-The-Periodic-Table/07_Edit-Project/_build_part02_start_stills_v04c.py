#!/usr/bin/env python3
"""Build finished-looking jar-free Part 02 start stills (v04c).

NOT flat placeholders: vignette, grain, soft candle bloom, contact shadows,
wood grain noise. ZERO jars/pots/canisters. Max cards per plate. Candle OK.
"""
from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

OUT = (
    Path(__file__).resolve().parents[1]
    / "04_Generated-Clips/part02/refs/v04c_stills"
)
W, H = 1280, 720
RNG = random.Random(42)


def _noise(w: int, h: int, scale: float = 1.0) -> Image.Image:
    im = Image.new("L", (w, h))
    px = im.load()
    for y in range(h):
        for x in range(w):
            px[x, y] = int(RNG.randrange(0, 256) * scale) & 255
    return im.filter(ImageFilter.GaussianBlur(radius=1.2))


def _wood(w: int, h: int, base=(92, 58, 32)) -> Image.Image:
    im = Image.new("RGB", (w, h), base)
    px = im.load()
    grain = _noise(w, h, 0.35)
    gp = grain.load()
    for y in range(h):
        wave = 6 * math.sin(y / 28.0) + 3 * math.sin(y / 9.0)
        for x in range(w):
            g = gp[x, y] / 255.0
            stripe = 0.85 + 0.15 * math.sin((x + wave) / 11.0)
            shade = 0.78 + 0.22 * ((y / h) ** 0.7)
            n = 0.92 + 0.16 * g
            r = int(base[0] * stripe * shade * n)
            gch = int(base[1] * stripe * shade * n * 0.98)
            b = int(base[2] * stripe * shade * n * 0.95)
            px[x, y] = (min(255, r), min(255, gch), min(255, b))
    # plank lines
    d = ImageDraw.Draw(im)
    for y in range(48, h, 54):
        d.line([(0, y), (w, y + RNG.randint(-2, 2))], fill=(48, 30, 16), width=2)
    return im


def _wall(w: int, h: int) -> Image.Image:
    im = Image.new("RGB", (w, h), (48, 34, 24))
    px = im.load()
    for y in range(h):
        for x in range(w):
            # soft window light from right
            t = x / w
            lift = 18 + int(70 * (t**1.4))
            plank = 8 if (y % 42) < 2 else 0
            px[x, y] = (
                min(255, 40 + lift - plank),
                min(255, 28 + int(lift * 0.7) - plank),
                min(255, 18 + int(lift * 0.4)),
            )
    return im


def _card(draw: ImageDraw.ImageDraw, box, fill=(236, 224, 196)):
    x0, y0, x1, y1 = box
    # contact shadow
    draw.rounded_rectangle(
        [x0 + 3, y0 + 5, x1 + 3, y1 + 5], radius=6, fill=(20, 12, 8, 90)
    )
    draw.rounded_rectangle([x0, y0, x1, y1], radius=6, fill=fill)
    draw.rounded_rectangle([x0, y0, x1, y1], radius=6, outline=(120, 96, 64), width=2)


def _candle(im: Image.Image, cx: int, cy: int):
    d = ImageDraw.Draw(im, "RGBA")
    # stick
    d.rectangle([cx - 5, cy - 70, cx + 5, cy + 8], fill=(230, 220, 190, 255))
    d.rectangle([cx - 14, cy + 4, cx + 14, cy + 18], fill=(160, 120, 60, 255))  # holder
    # flame
    d.ellipse([cx - 7, cy - 95, cx + 7, cy - 68], fill=(255, 200, 80, 220))
    d.ellipse([cx - 3, cy - 90, cx + 3, cy - 74], fill=(255, 255, 210, 230))
    # bloom
    bloom = Image.new("RGBA", im.size, (0, 0, 0, 0))
    bd = ImageDraw.Draw(bloom)
    bd.ellipse([cx - 55, cy - 130, cx + 55, cy - 40], fill=(255, 170, 60, 40))
    bloom = bloom.filter(ImageFilter.GaussianBlur(18))
    im.alpha_composite(bloom)


def _vignette(im: Image.Image, strength=0.45) -> Image.Image:
    w, h = im.size
    vig = Image.new("L", (w, h), 0)
    px = vig.load()
    cx, cy = w / 2, h / 2
    maxr = math.hypot(cx, cy)
    for y in range(h):
        for x in range(w):
            r = math.hypot(x - cx, y - cy) / maxr
            px[x, y] = int(255 * (1.0 - strength * (r**1.8)))
    return Image.composite(im, Image.new("RGB", (w, h), (10, 6, 4)), vig)


def _finish(im: Image.Image) -> Image.Image:
    im = im.convert("RGB")
    im = ImageEnhance.Color(im).enhance(1.08)
    im = ImageEnhance.Contrast(im).enhance(1.12)
    grain = _noise(W, H, 0.5).convert("RGB")
    im = Image.blend(im, grain, 0.04)
    im = _vignette(im, 0.38)
    return im.filter(ImageFilter.SMOOTH_MORE)


def build(kind: str) -> Image.Image:
    wall = _wall(W, int(H * 0.48))
    desk = _wood(W, int(H * 0.62), base=(102, 66, 38))
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    canvas.paste(wall, (0, 0))
    canvas.paste(desk, (0, H - desk.size[1]))
    d = ImageDraw.Draw(canvas, "RGBA")

    # books stack (no jars)
    d.rounded_rectangle([70, 250, 210, 430], radius=4, fill=(90, 40, 30, 255))
    d.rounded_rectangle([80, 235, 220, 255], radius=3, fill=(160, 120, 70, 255))
    d.rounded_rectangle([90, 218, 225, 238], radius=3, fill=(50, 70, 90, 255))

    # quill
    d.line([(240, 400), (310, 300)], fill=(230, 220, 200, 255), width=3)
    d.polygon([(308, 292), (318, 305), (300, 308)], fill=(210, 200, 170, 255))

    cards = {
        "02_lavoisier_list": [(360, 360), (430, 350), (500, 355), (570, 348), (640, 358)],
        "03_not_a_map": [(400, 340), (470, 380), (520, 350), (580, 400), (450, 420)],
        "05_explorer_triad_break": [(420, 360), (500, 360), (580, 360), (640, 340)],
        "06_rhymes_run_out": [
            (300 + i * 40, 320 + (i % 3) * 20) for i in range(10)
        ],
        "07_newlands_octave": [(280 + i * 70, 370) for i in range(8)],
        "08_piano_gag_fail": [(360, 380), (430, 400), (500, 360), (560, 410)],
        "09_almost_right": [(400, 360), (470, 358), (540, 362), (610, 355)],
        "10_ruler_crooked": [(420, 370), (500, 390), (560, 360)],
        "11_shared_stick": [(380, 380), (460, 380), (540, 380)],
    }[kind]

    for i, (x, y) in enumerate(cards[:8]):
        _card(d, [x, y, x + 52, y + 78], fill=(238, 226, 198) if i % 2 == 0 else (232, 218, 186))

    if kind in {"07_newlands_octave", "08_piano_gag_fail"}:
        # toy piano (wood only)
        d.rounded_rectangle([820, 390, 1120, 500], radius=8, fill=(70, 45, 28, 255))
        for i in range(10):
            x0 = 835 + i * 28
            d.rectangle([x0, 405, x0 + 22, 485], fill=(245, 240, 230, 255), outline=(40, 30, 20, 255))
        if kind == "08_piano_gag_fail":
            d.polygon([(900, 400), (940, 470), (880, 470)], fill=(245, 240, 230, 255))

    if kind in {"10_ruler_crooked", "11_shared_stick"}:
        # wooden sticks/ruler
        d.line([(320, 450), (980, 420)], fill=(190, 150, 90, 255), width=10)
        if kind == "10_ruler_crooked":
            d.line([(340, 500), (900, 560)], fill=(170, 130, 70, 255), width=10)
        else:
            d.line([(330, 500), (970, 500)], fill=(190, 150, 90, 255), width=10)

    _candle(canvas, 1080, 340)
    return _finish(canvas)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    ids = [
        "02_lavoisier_list",
        "03_not_a_map",
        "05_explorer_triad_break",
        "06_rhymes_run_out",
        "07_newlands_octave",
        "08_piano_gag_fail",
        "09_almost_right",
        "10_ruler_crooked",
        "11_shared_stick",
    ]
    for pid in ids:
        path = OUT / f"{pid}_start.jpg"
        build(pid).save(path, quality=92)
        print("wrote", path, path.stat().st_size)


if __name__ == "__main__":
    main()
