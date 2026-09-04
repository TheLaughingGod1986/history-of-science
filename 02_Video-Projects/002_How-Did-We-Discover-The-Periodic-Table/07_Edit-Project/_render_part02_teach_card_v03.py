#!/usr/bin/env python3
"""Render Part 02's ONE teach pop-up (Döbereiner triads) — sparse card budget."""
from __future__ import annotations

import random
import subprocess
import time
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

PROJ = Path(__file__).resolve().parents[1]
EDIT = Path(__file__).resolve().parent
OUT_RAW = PROJ / "04_Generated-Clips/part02/raw/v01_fast"
STILLS = EDIT / "_qa_part02_v03/card_stills"
REJECT = PROJ / "04_Generated-Clips/part02/raw/_rejected_v02_card_wall"
W, H = 1280, 720
FPS = 24
DUR_S = 8.0
FONT_REG = "/System/Library/Fonts/Supplemental/Times New Roman.ttf"
FONT_BOLD = "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf"

PID = "04_triad_cards"
TITLE = "DÖBEREINER'S TRIADS"
BODY = (
    "Lithium, sodium, potassium.\n"
    "Chlorine, bromine, iodine.\n"
    "Three cousins — the middle often sat between the others in mass."
)


def wood_bg(seed: int = 7) -> Image.Image:
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


def parchment(size, seed: int = 3) -> Image.Image:
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


def wrap_text(draw, text, font, max_w):
    lines = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for word in words[1:]:
            trial = f"{cur} {word}"
            if draw.textlength(trial, font=font) <= max_w:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        lines.append(cur)
    return lines


def draw_card(title: str, body: str, seed: int = 3) -> Image.Image:
    bg = wood_bg(seed)
    card_w, card_h = 980, 560
    card = parchment((card_w, card_h), seed=seed)
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

    title_font = ImageFont.truetype(FONT_BOLD, 42)
    body_font = ImageFont.truetype(FONT_REG, 28)
    tw = draw.textlength(title, font=title_font)
    draw.text(((card_w - tw) / 2, 70), title, font=title_font, fill=ink)
    y = 130
    draw.line([(120, y), (card_w - 120, y)], fill=ink, width=2)
    draw.polygon(
        [
            (card_w // 2, y - 6),
            (card_w // 2 + 6, y),
            (card_w // 2, y + 6),
            (card_w // 2 - 6, y),
        ],
        fill=ink,
    )
    lines = wrap_text(draw, body, body_font, card_w - 160)
    line_h = 40
    total_h = len(lines) * line_h
    y0 = 180 + max(0, (280 - total_h) // 2)
    for i, line in enumerate(lines):
        lw = draw.textlength(line, font=body_font)
        draw.text(((card_w - lw) / 2, y0 + i * line_h), line, font=body_font, fill=ink)
    yb = card_h - 70
    draw.line([(160, yb), (card_w - 160, yb)], fill=ink, width=1)

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
        f"zoompan=z='min(1.06,1+0.06*on/{frames})':"
        f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
        f"d={frames}:s={W}x{H}:fps={FPS},"
        f"eq=brightness='0.01*sin(2*PI*t/4)':saturation=1.05"
    )
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-loop",
            "1",
            "-i",
            str(still),
            "-vf",
            vf,
            "-t",
            f"{DUR_S}",
            "-r",
            str(FPS),
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-crf",
            "18",
            "-preset",
            "medium",
            "-an",
            str(dest),
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
        dest.rename(REJECT / f"{PID}_v01_pre_teach_{ts}.mp4")
        print(f"archived old {PID}", flush=True)
    img = draw_card(TITLE, BODY, seed=14)
    img.save(still)
    print(f"still {still.name} · {TITLE}", flush=True)
    still_to_mp4(still, dest)
    dur = float(
        subprocess.check_output(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=nw=1:nk=1",
                str(dest),
            ],
            text=True,
        ).strip()
    )
    size = dest.stat().st_size
    assert size >= 200_000 and 7.5 <= dur <= 8.5, (PID, size, dur)
    print(f"OK {dest.name} size={size} dur={dur:.2f}", flush=True)


if __name__ == "__main__":
    main()
