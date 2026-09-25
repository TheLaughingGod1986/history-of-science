#!/usr/bin/env python3
"""Compose the Bold Explainer v05 thumbnail from the generated hero artwork."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


SOURCE = Path(
    "/Users/ben/.codex/generated_images/"
    "019fa448-9e8b-7c43-a9cc-91d8a1b15ece/"
    "call_j9yaFXmzmfLT42KXenrdLujK.png"
)
OUT_DIR = Path(
    "/Users/ben/code/Orbit-YouTube/02_Video-Projects/"
    "001_Will-We-Ever-Meet-Aliens/08_Thumbnail"
)
BACKGROUND = OUT_DIR / "aliens_thumbnail_bold-v05_background.png"
OUTPUT = OUT_DIR / "aliens_thumbnail_bold-v05_where-is-everyone.png"
W, H = 1280, 720


def load_font(size: int) -> ImageFont.FreeTypeFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Supplemental/Arial Black.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size=size)
        except OSError:
            continue
    raise RuntimeError("No suitable bold font found")


def fit_cover(image: Image.Image) -> Image.Image:
    scale = max(W / image.width, H / image.height)
    resized = image.resize(
        (round(image.width * scale), round(image.height * scale)),
        Image.Resampling.LANCZOS,
    )
    left = max(0, (resized.width - W) // 2)
    top = max(0, (resized.height - H) // 2)
    return resized.crop((left, top, left + W, top + H))


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    base = fit_cover(Image.open(SOURCE).convert("RGB"))
    base.save(BACKGROUND, quality=95)

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pixels = overlay.load()
    for x in range(720):
        alpha = int(150 * (1 - x / 720) ** 1.7)
        for y in range(H):
            pixels[x, y] = (2, 10, 22, alpha)
    composed = Image.alpha_composite(base.convert("RGBA"), overlay)
    draw = ImageDraw.Draw(composed)

    font = load_font(106)
    lines = [("WHERE IS", (244, 246, 239, 255)), ("EVERYONE?", (255, 126, 38, 255))]
    x, y = 72, 180
    for text, colour in lines:
        draw.text(
            (x, y),
            text,
            font=font,
            fill=colour,
            stroke_width=5,
            stroke_fill=(3, 10, 22, 235),
        )
        bounds = draw.textbbox((x, y), text, font=font, stroke_width=5)
        y = bounds[3] + 12

    composed.convert("RGB").save(OUTPUT, quality=96)
    print(OUTPUT)


if __name__ == "__main__":
    main()
