#!/usr/bin/env python3
"""Compose sparse phone-readable atomic-weight marks onto Part 03 v06 I2V starts.

Props ONLY: H 1 · O 16 · C 12 · N 14 · S 32 — dark ink on cream.
Most sheets stay blank. Desk hero + optional swirl starts for Flow I2V.
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

STILL = Path(__file__).resolve().parents[1] / "04_Generated-Clips/part03/refs/v06_stills"
MARKS = [("H", "1"), ("O", "16"), ("C", "12"), ("N", "14"), ("S", "32")]
INK = (28, 22, 16, 235)
INK_SOFT = (40, 32, 24, 200)


def font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in (
        "/System/Library/Fonts/Supplemental/Georgia Bold.ttf",
        "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf",
        "/Library/Fonts/Arial Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def draw_mark(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    symbol: str,
    number: str,
    *,
    size: int,
    fill=INK,
) -> None:
    f = font(size)
    text = f"{symbol} {number}"
    # slight charcoal shadow for phone readability
    x, y = xy
    draw.text((x + 2, y + 2), text, font=f, fill=(0, 0, 0, 90))
    draw.text((x, y), text, font=f, fill=fill)


def compose_desk_hero(src: Path, dest: Path) -> None:
    """Upright hero + 1–2 stack marks; rest blank."""
    im = Image.open(src).convert("RGBA")
    w, h = im.size
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)

    # Coordinates tuned for 1280x720 desk settle stills (upright left, stack right).
    # Hero upright face — huge phone-readable.
    draw_mark(d, (int(w * 0.34), int(h * 0.38)), "H", "1", size=max(54, w // 18))
    draw_mark(d, (int(w * 0.34), int(h * 0.52)), "O", "16", size=max(48, w // 20))
    # Top of stack — one or two marks only
    draw_mark(d, (int(w * 0.58), int(h * 0.48)), "C", "12", size=max(36, w // 28), fill=INK_SOFT)
    draw_mark(d, (int(w * 0.62), int(h * 0.58)), "N", "14", size=max(32, w // 30), fill=INK_SOFT)

    out = Image.alpha_composite(im, overlay).convert("RGB")
    dest.parent.mkdir(parents=True, exist_ok=True)
    out.save(dest, quality=95)
    print(f"desk_hero {dest.name} {out.size}", flush=True)


def compose_swirl(src: Path, dest: Path) -> None:
    """≈3–6 marked sheets in aisle swirl; most stay blank."""
    im = Image.open(src).convert("RGBA")
    w, h = im.size
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)

    # Sparse placements across mid-air / floor papers (wide aisle).
    placements = [
        (0.28, 0.42, "H", "1", max(40, w // 24)),
        (0.48, 0.36, "O", "16", max(38, w // 26)),
        (0.62, 0.48, "C", "12", max(36, w // 28)),
        (0.38, 0.62, "N", "14", max(34, w // 30)),
        (0.55, 0.58, "S", "32", max(34, w // 30)),
    ]
    for fx, fy, sym, num, sz in placements:
        draw_mark(d, (int(w * fx), int(h * fy)), sym, num, size=sz)

    out = Image.alpha_composite(im, overlay).convert("RGB")
    dest.parent.mkdir(parents=True, exist_ok=True)
    out.save(dest, quality=95)
    print(f"swirl {dest.name} {out.size}", flush=True)


def compose_desk_from_assembled(src: Path, dest: Path) -> None:
    """1920x1080 ATOMIC WEIGHTS desk still from rough v05."""
    im = Image.open(src).convert("RGBA")
    w, h = im.size
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    # Soft-focus foreground sheet + upright mid + stack
    draw_mark(d, (int(w * 0.42), int(h * 0.55)), "H", "1", size=max(72, w // 20))
    draw_mark(d, (int(w * 0.42), int(h * 0.66)), "O", "16", size=max(64, w // 22))
    draw_mark(d, (int(w * 0.58), int(h * 0.52)), "C", "12", size=max(48, w // 28), fill=INK_SOFT)
    draw_mark(d, (int(w * 0.62), int(h * 0.62)), "S", "32", size=max(44, w // 30), fill=INK_SOFT)
    out = Image.alpha_composite(im, overlay).convert("RGB")
    dest.parent.mkdir(parents=True, exist_ok=True)
    out.save(dest, quality=95)
    print(f"assembled_desk {dest.name} {out.size}", flush=True)


def main() -> None:
    desk_src = STILL / "03_pamphlet_v02_t65.jpg"
    desk_mid = STILL / "03_pamphlet_v02_t40.jpg"
    swirl_src = STILL / "04_zoo_v02_t20.jpg"
    assembled = STILL / "v05_atomic_weights_t17.jpg"

    compose_desk_hero(desk_src, STILL / "03_desk_hero_marked_i2v.jpg")
    compose_desk_hero(desk_mid, STILL / "03_desk_mid_marked_i2v.jpg")
    compose_swirl(swirl_src, STILL / "03_swirl_marked_i2v.jpg")
    if assembled.exists():
        compose_desk_from_assembled(assembled, STILL / "03_assembled_desk_marked_i2v.jpg")
    print(f"OK marked stills → {STILL}", flush=True)


if __name__ == "__main__":
    main()
