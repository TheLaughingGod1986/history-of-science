#!/usr/bin/env python3
"""Local chapter card for Part 02 — no Flow lab, no flaming jars.

Ben UAT: opening seconds of v04 still showed vessels on fire because
01_chapter_card_v01.mp4 was a Flow clip that drifts into an alchemy bench.
Replace with the same local parchment-card style as the triad teach card.
"""
from __future__ import annotations

import random
import subprocess
import time
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

PROJ = Path(__file__).resolve().parents[1]
EDIT = Path(__file__).resolve().parent
OUT_RAW = PROJ / "04_Generated-Clips/part02/raw/v01_fast"
STILLS = EDIT / "_qa_part02_v05/card_stills"
REJECT = PROJ / "04_Generated-Clips/part02/raw/_rejected_v05_chapter_fire"
W, H = 1280, 720
FPS = 24
DUR_S = 8.0
FONT_REG = "/System/Library/Fonts/Supplemental/Times New Roman.ttf"
FONT_BOLD = "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf"

PID = "01_chapter_card"
KICKER = "CHAPTER 2"
TITLE = "FIRST PATTERNS, STILL WRONG"


def wood_bg(seed: int = 11) -> Image.Image:
    rnd = random.Random(seed)
    img = Image.new("RGB", (W, H), (42, 28, 18))
    px = img.load()
    for y in range(H):
        for x in range(W):
            band = (y // 48) % 2
            base = 38 + band * 8 + (y % 48) // 12
            n = rnd.randint(-6, 6)
            r = max(0, min(255, base + 8 + n))
            g = max(0, min(255, base - 2 + n // 2))
            b = max(0, min(255, base - 12 + n // 3))
            px[x, y] = (r, g, b)
    return img.filter(ImageFilter.GaussianBlur(0.6))


def parchment(size, seed: int = 5) -> Image.Image:
    rnd = random.Random(seed)
    w, h = size
    img = Image.new("RGB", (w, h), (232, 214, 178))
    px = img.load()
    for y in range(h):
        for x in range(w):
            n = rnd.randint(-10, 8)
            stain = 12 if ((x * 17 + y * 13) % 211) < 3 else 0
            r = max(180, min(245, 232 + n - stain))
            g = max(160, min(230, 214 + n - stain))
            b = max(130, min(200, 178 + n - stain // 2))
            px[x, y] = (r, g, b)
    return img


def draw_card() -> Image.Image:
    bg = wood_bg()
    card_w, card_h = 980, 520
    card = parchment((card_w, card_h))
    draw = ImageDraw.Draw(card)
    ink = (72, 48, 28)
    for inset, width in [(18, 3), (28, 1)]:
        draw.rectangle(
            [inset, inset, card_w - inset - 1, card_h - inset - 1],
            outline=ink,
            width=width,
        )
    for cx, cy, sx, sy in [
        (40, 40, 1, 1),
        (card_w - 40, 40, -1, 1),
        (40, card_h - 40, 1, -1),
        (card_w - 40, card_h - 40, -1, -1),
    ]:
        draw.line([(cx, cy), (cx + sx * 22, cy)], fill=ink, width=2)
        draw.line([(cx, cy), (cx, cy + sy * 22)], fill=ink, width=2)

    kicker_font = ImageFont.truetype(FONT_REG, 28)
    title_font = ImageFont.truetype(FONT_BOLD, 44)
    kw = draw.textlength(KICKER, font=kicker_font)
    draw.text(((card_w - kw) / 2, 120), KICKER, font=kicker_font, fill=ink)
    y = 175
    draw.line([(160, y), (card_w - 160, y)], fill=ink, width=2)
    draw.polygon(
        [
            (card_w // 2, y - 6),
            (card_w // 2 + 6, y),
            (card_w // 2, y + 6),
            (card_w // 2 - 6, y),
        ],
        fill=ink,
    )
    # Title may wrap to two lines
    words = TITLE.split()
    lines: list[str] = []
    cur = words[0]
    for word in words[1:]:
        trial = f"{cur} {word}"
        if draw.textlength(trial, font=title_font) <= card_w - 160:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    lines.append(cur)
    line_h = 56
    total_h = len(lines) * line_h
    y0 = 230 + max(0, (160 - total_h) // 2)
    for i, line in enumerate(lines):
        lw = draw.textlength(line, font=title_font)
        draw.text(((card_w - lw) / 2, y0 + i * line_h), line, font=title_font, fill=ink)
    yb = card_h - 80
    draw.line([(200, yb), (card_w - 200, yb)], fill=ink, width=1)

    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    ox, oy = (W - card_w) // 2 + 8, (H - card_h) // 2 + 10
    sd.rounded_rectangle(
        [ox, oy, ox + card_w, oy + card_h], radius=6, fill=(0, 0, 0, 90)
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(10))
    out = bg.convert("RGBA")
    out = Image.alpha_composite(out, shadow)
    out.paste(card, ((W - card_w) // 2, (H - card_h) // 2))
    return out.convert("RGB")


def still_to_mp4(still: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    frames = int(DUR_S * FPS)
    vf = (
        f"scale={W}:{H},"
        f"zoompan=z='min(1.05,1+0.05*on/{frames})':"
        f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
        f"d={frames}:s={W}x{H}:fps={FPS}"
    )
    subprocess.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-loop", "1", "-i", str(still),
            "-vf", vf, "-t", f"{DUR_S}", "-r", str(FPS),
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
            "-preset", "medium", "-an", str(dest),
        ],
        check=True,
    )


def main() -> None:
    STILLS.mkdir(parents=True, exist_ok=True)
    OUT_RAW.mkdir(parents=True, exist_ok=True)
    REJECT.mkdir(parents=True, exist_ok=True)
    still = STILLS / f"{PID}_card.png"
    dest = OUT_RAW / f"{PID}_v01.mp4"
    if dest.exists() and dest.stat().st_size > 200_000:
        ts = time.strftime("%Y%m%d_%H%M%S")
        dest.rename(REJECT / f"{PID}_v01_flow_lab_fire_{ts}.mp4")
        print(f"archived flaming chapter clip → {REJECT.name}", flush=True)
    img = draw_card()
    img.save(still)
    print(f"still {still.name} · {KICKER} / {TITLE}", flush=True)
    still_to_mp4(still, dest)
    dur = float(
        subprocess.check_output(
            [
                "ffprobe", "-v", "error", "-show_entries", "format=duration",
                "-of", "default=nw=1:nk=1", str(dest),
            ],
            text=True,
        ).strip()
    )
    size = dest.stat().st_size
    assert size >= 200_000 and 7.5 <= dur <= 8.5, (PID, size, dur)
    print(f"OK {dest.name} size={size} dur={dur:.2f}", flush=True)


if __name__ == "__main__":
    main()
