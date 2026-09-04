#!/usr/bin/env python3
"""Part 02 v04 start stills — finished wood study desks, ZERO jars/pots.

Base = Part 01 PASS empty-chairs wood/window light, desk-banded so chair seats
vanish. Overlay blank specimen cards + candle / ruler / toy piano only.
Never draw jar/pot cylinders.
"""
from __future__ import annotations

import random
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

PROJ = Path(__file__).resolve().parents[1]
OUT = PROJ / "04_Generated-Clips/part02/refs/v04_stills"
BASE_CLIP = PROJ / "04_Generated-Clips/part01/raw/v01_fast/01_empty_chairs_open_v01.mp4"
W, H = 1280, 720

# Must match part-02_plates_v04.json scenery remint ids
SCENES = {
    "02_lavoisier_list": "neat_cards",
    "03_not_a_map": "messy_cards",
    "05_explorer_triad_break": "triad_break",
    "06_rhymes_run_out": "card_shelves",
    "07_newlands_octave": "cards_piano",
    "08_piano_gag_fail": "piano_scatter",
    "09_almost_right": "gap_cards",
    "10_ruler_crooked": "crooked_ruler",
    "11_shared_stick": "matching_sticks",
}


def wood_base() -> Image.Image:
    if BASE_CLIP.exists():
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
            tmp_path = Path(tmp.name)
        subprocess.run(
            [
                "ffmpeg", "-y", "-ss", "2.5", "-i", str(BASE_CLIP),
                "-frames:v", "1", "-q:v", "2", str(tmp_path),
            ],
            check=True,
            capture_output=True,
        )
        img = Image.open(tmp_path).convert("RGB")
        tmp_path.unlink(missing_ok=True)
    else:
        img = Image.new("RGB", (W, H), (48, 34, 26))
    img = img.resize((W, H), Image.Resampling.LANCZOS)
    img = ImageEnhance.Brightness(img).enhance(0.72)
    img = ImageEnhance.Color(img).enhance(0.85)
    img = img.filter(ImageFilter.GaussianBlur(0.8))
    # Desk band covers glowing chair seats — warm wood study plane.
    desk = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(desk)
    d.rectangle([0, int(H * 0.48), W, H], fill=(62, 42, 28, 215))
    for y in range(int(H * 0.50), H, 28):
        d.line([(0, y), (W, y)], fill=(40, 28, 18, 70), width=2)
    return Image.alpha_composite(img.convert("RGBA"), desk).convert("RGB")


def parchment_card(w=70, h=100, seed=0) -> Image.Image:
    rnd = random.Random(seed)
    card = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(card)
    fill = (
        236 + rnd.randint(-8, 4),
        222 + rnd.randint(-8, 4),
        190 + rnd.randint(-8, 4),
        255,
    )
    d.rounded_rectangle(
        [0, 0, w - 1, h - 1],
        radius=4,
        fill=fill,
        outline=(90, 60, 35, 255),
        width=2,
    )
    d.rounded_rectangle(
        [5, 5, w - 6, h - 6],
        radius=2,
        outline=(140, 105, 70, 180),
        width=1,
    )
    return card


def paste_card(
    base: Image.Image,
    x: int,
    y: int,
    *,
    w: int = 70,
    h: int = 100,
    seed: int = 0,
    angle: int = 0,
) -> Image.Image:
    card = parchment_card(w, h, seed)
    if angle:
        card = card.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
    sh = Image.new("RGBA", base.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    sd.rectangle(
        [x + 4, y + 6, x + card.size[0] + 2, y + card.size[1] + 4],
        fill=(0, 0, 0, 60),
    )
    sh = sh.filter(ImageFilter.GaussianBlur(4))
    out = Image.alpha_composite(base.convert("RGBA"), sh)
    out.paste(card, (x, y), card)
    return out.convert("RGB")


def candle(base: Image.Image, x: int, y: int, lit: bool = True) -> Image.Image:
    out = base.convert("RGBA")
    d = ImageDraw.Draw(out)
    # Thin candlestick only — never a jar cylinder.
    d.rectangle(
        [x + 3, y - 70, x + 9, y],
        fill=(210, 195, 160, 255),
        outline=(90, 60, 35, 255),
    )
    d.ellipse(
        [x - 4, y - 4, x + 16, y + 8],
        fill=(150, 110, 55, 255),
        outline=(70, 45, 25, 255),
    )
    if lit:
        glow = Image.new("RGBA", base.size, (0, 0, 0, 0))
        gd = ImageDraw.Draw(glow)
        gd.ellipse([x - 14, y - 118, x + 24, y - 58], fill=(255, 180, 80, 36))
        out = Image.alpha_composite(out, glow)
        d = ImageDraw.Draw(out)
        d.ellipse([x + 2, y - 96, x + 10, y - 74], fill=(255, 210, 90, 255))
        d.ellipse([x + 4, y - 92, x + 8, y - 78], fill=(255, 245, 200, 255))
    return out.convert("RGB")


def ruler(
    base: Image.Image, x: int, y: int, *, length: int = 520, crooked: bool = False
) -> Image.Image:
    out = base.convert("RGBA")
    d = ImageDraw.Draw(out)
    fill = (190, 150, 90, 255)
    outline = (70, 45, 25, 255)
    if crooked:
        mid = length // 2
        d.polygon(
            [(x, y), (x + mid, y - 12), (x + mid, y + 8), (x, y + 20)],
            fill=fill,
            outline=outline,
        )
        d.polygon(
            [
                (x + mid, y - 12),
                (x + length, y + 10),
                (x + length, y + 30),
                (x + mid, y + 8),
            ],
            fill=fill,
            outline=outline,
        )
    else:
        d.rounded_rectangle(
            [x, y, x + length, y + 18], radius=3, fill=fill, outline=outline
        )
    return out.convert("RGB")


def piano_keys(base: Image.Image, x: int, y: int, n: int = 8) -> Image.Image:
    out = base.convert("RGBA")
    d = ImageDraw.Draw(out)
    for i in range(n):
        kx = x + i * 22
        d.rectangle(
            [kx, y, kx + 20, y + 68],
            fill=(245, 240, 230, 255),
            outline=(40, 30, 20, 255),
        )
        if i % 2 == 1 and i < n - 1:
            d.rectangle([kx + 14, y, kx + 26, y + 40], fill=(25, 20, 15, 255))
    return out.convert("RGB")


def render(kind: str, seed: int = 7) -> Image.Image:
    rnd = random.Random(seed)
    img = wood_base()
    desk_y = int(H * 0.58)

    if kind == "neat_cards":
        for i in range(7):
            img = paste_card(img, 140 + i * 95, desk_y - 10, seed=seed + i)
        img = candle(img, 1080, desk_y + 40, lit=True)
    elif kind == "messy_cards":
        poses = [
            (160, -10, 12),
            (240, -40, -18),
            (320, 5, 25),
            (420, -20, -8),
            (520, -55, 15),
            (620, -5, -22),
            (720, -30, 10),
        ]
        for i, (x, dy, ang) in enumerate(poses):
            img = paste_card(img, x, desk_y + dy, seed=seed + i, angle=ang)
        img = candle(img, 100, desk_y + 30, lit=True)
    elif kind == "triad_break":
        for i in range(3):
            img = paste_card(
                img, 320 + i * 130, desk_y - 30, w=90, h=120, seed=seed + i
            )
        img = paste_card(
            img, 740, desk_y - 70, w=90, h=120, seed=seed + 9, angle=20
        )
        img = candle(img, 140, desk_y + 20, lit=True)
    elif kind == "card_shelves":
        for row, yy in enumerate([160, 300, 440]):
            for i in range(9):
                img = paste_card(
                    img,
                    60 + i * 130,
                    yy,
                    w=55,
                    h=80,
                    seed=seed + row * 10 + i,
                )
        img = candle(img, 1180, 520, lit=True)
    elif kind == "cards_piano":
        for i in range(9):
            img = paste_card(img, 50 + i * 80, desk_y - 15, seed=seed + i)
        img = piano_keys(img, 980, desk_y - 50, n=7)
        img = candle(img, 900, desk_y + 30, lit=True)
    elif kind == "piano_scatter":
        img = piano_keys(img, 180, desk_y - 30, n=9)
        for i in range(6):
            img = paste_card(
                img,
                450 + i * 95,
                desk_y + rnd.randint(0, 35),
                seed=seed + i,
                angle=rnd.randint(-25, 25),
            )
    elif kind == "gap_cards":
        for i in range(7):
            gap = 40 if i >= 4 else 0
            img = paste_card(
                img,
                140 + i * 110 + gap,
                desk_y - 25,
                w=75,
                h=105,
                seed=seed + i,
            )
        img = candle(img, 1120, desk_y + 25, lit=True)
    elif kind == "crooked_ruler":
        img = ruler(img, 200, desk_y + 10, length=720, crooked=True)
        for i in range(5):
            img = paste_card(
                img,
                180 + i * 150,
                desk_y - 100,
                seed=seed + i,
                angle=rnd.randint(-6, 6),
            )
        img = candle(img, 80, desk_y + 20, lit=True)
    elif kind == "matching_sticks":
        for i in range(5):
            img = ruler(
                img,
                200 + i * 25,
                desk_y - 30 + i * 16,
                length=540,
                crooked=False,
            )
        img = candle(img, 1100, desk_y + 20, lit=True)

    vig = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    vd = ImageDraw.Draw(vig)
    for i in range(40):
        a = int(i * 1.2)
        vd.rectangle([i, i, W - 1 - i, H - 1 - i], outline=(0, 0, 0, a))
    img = Image.alpha_composite(img.convert("RGBA"), vig).convert("RGB")
    return img.filter(ImageFilter.SMOOTH)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for i, (pid, kind) in enumerate(SCENES.items()):
        dest = OUT / f"{pid}_start.jpg"
        img = render(kind, seed=11 + i)
        img.save(dest, quality=92)
        print(f"wrote {dest.name} size={dest.stat().st_size}", flush=True)


if __name__ == "__main__":
    main()
