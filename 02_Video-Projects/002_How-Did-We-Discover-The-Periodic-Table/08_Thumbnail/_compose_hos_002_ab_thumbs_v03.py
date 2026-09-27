#!/usr/bin/env python3
"""Compose HOS 002 A/B-test long thumbs B + C (v03).

Reuse live listing art (gallium / empty slot). No remint. No Flow. No Studio.
Rules: THUMBNAIL_AND_TITLE_RULES.md §2 — heavy sans caps, yellow hook word,
text off subject and out of bottom-right duration badge.
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
SELECTED = HERE / "Selected"
# Live art lives on the Mini checkout (gitignored); fall back to worktree if present.
MAIN_SEL = Path(
    "/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/"
    "002_How-Did-We-Discover-The-Periodic-Table/08_Thumbnail/Selected"
)
ASSETS = Path("/Users/benjaminoats/.local/share/cursor-mac-mini-hos-worker/artifacts/assets")

WHITE = (255, 255, 255)
YELLOW = (255, 214, 46)
INK = (18, 12, 8)
SHADOW = (10, 6, 4, 220)

# Heavy sans — house lock for phone-readable thumbs.
FONT = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
FONT_FALLBACK = "/System/Library/Fonts/Supplemental/Impact.ttf"


def font(size: int) -> ImageFont.FreeTypeFont:
    for path in (FONT, FONT_FALLBACK):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def load_src(candidates: list[Path]) -> Image.Image:
    for p in candidates:
        if p.exists():
            return Image.open(p).convert("RGB")
    raise SystemExit(f"missing source among {[str(c) for c in candidates]}")


def wash(im: Image.Image, box: tuple[int, int, int, int], sample: tuple[int, int, int, int], blur: int = 14) -> None:
    """Paint a soft scene-matched wash over a region (covers old type / garnish)."""
    x0, y0, x1, y1 = box
    patch = im.crop(sample).resize((x1 - x0, y1 - y0), Image.Resampling.LANCZOS)
    patch = patch.filter(ImageFilter.GaussianBlur(blur))
    mask = Image.new("L", (x1 - x0, y1 - y0), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle((0, 0, x1 - x0 - 1, y1 - y0 - 1), radius=28, fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(10))
    im.paste(patch, (x0, y0), mask)


def grade_left(im: Image.Image, width: int = 560, alpha: int = 110) -> Image.Image:
    """Smooth left darken for type legibility — no hard rectangle."""
    overlay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for i in range(width):
        a = int(alpha * (1.0 - i / width) ** 1.4)
        if a <= 0:
            continue
        od.line([(i, 0), (i, im.height)], fill=(16, 10, 6, a))
    return Image.alpha_composite(im.convert("RGBA"), overlay).convert("RGB")


def draw_words(
    im: Image.Image,
    lines: list[list[tuple[str, tuple[int, int, int]]]],
    *,
    x: int,
    y: int,
    size: int,
    max_w: int,
    gap: float = 1.02,
) -> None:
    """Draw stacked lines of coloured words. Every word must read at 168×94."""
    draw = ImageDraw.Draw(im)
    cy = y
    for line in lines:
        text = " ".join(w for w, _ in line)
        fsize = size
        f = font(fsize)
        while f.getlength(text) > max_w and fsize > 40:
            fsize -= 2
            f = font(fsize)
        stroke = max(7, fsize // 9)
        cx = x
        for w, color in line:
            draw.text((cx + 4, cy + 5), w, font=f, fill=SHADOW, stroke_width=stroke + 3, stroke_fill=SHADOW)
            draw.text((cx, cy), w, font=f, fill=color, stroke_width=stroke, stroke_fill=INK)
            cx += int(f.getlength(w + " "))
        cy += int(fsize * gap)


def save_jpg(im: Image.Image, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    rgb = im.convert("RGB").resize((1280, 720), Image.Resampling.LANCZOS)
    q = 90
    rgb.save(dest, "JPEG", quality=q, optimize=True, subsampling=1)
    while dest.stat().st_size > 1_900_000 and q > 70:
        q -= 4
        rgb.save(dest, "JPEG", quality=q, optimize=True, subsampling=1)
    print(f"{dest.name}  {dest.stat().st_size} B  {rgb.size}  q={q}", flush=True)


def compose_b() -> Path:
    """Gallium blob only — HE PREDICTED THIS (PREDICTED yellow). No Explorer."""
    src = load_src(
        [
            MAIN_SEL / "hos_002_thumb_A_gallium_live_v02.png",
            ASSETS / "hos_002_thumb_A_gallium_live_v02b.png",
            ASSETS / "hos_002_thumb_A_gallium_live_v02.png",
            SELECTED / "hos_002_thumb_A_gallium_live_v02.png",
        ]
    )
    # Crop out Explorer (lower-left) and most baked title — blob becomes sole hero.
    # Source layout: Explorer ~x0–380, blob ~x420–1180.
    im = src.resize((1280, 720), Image.Resampling.LANCZOS)
    im = im.crop((360, 40, 1240, 700)).resize((1280, 720), Image.Resampling.LANCZOS)
    # Kill any leftover title fragment on the far left of the crop
    wash(im, (0, 0, 280, 220), sample=(400, 40, 700, 200), blur=22)
    im = grade_left(im, width=520, alpha=130)
    draw_words(
        im,
        [[("HE", WHITE)], [("PREDICTED", YELLOW)], [("THIS", WHITE)]],
        x=40,
        y=48,
        size=110,
        max_w=620,
        gap=0.98,
    )
    dest = SELECTED / "hos_002_thumb_B_predicted_v03.jpg"
    save_jpg(im, dest)
    return dest


def compose_c() -> Path:
    """Glowing empty slot — LEFT EMPTY ON PURPOSE (EMPTY yellow)."""
    src = load_src(
        [
            MAIN_SEL / "hos_002_thumb_C_empty_slot_live_v02.png",
            ASSETS / "hos_002_thumb_C_empty_slot_live_v02b.png",
            ASSETS / "hos_002_thumb_C_empty_slot_live_v02.png",
            SELECTED / "hos_002_thumb_C_empty_slot_live_v02.png",
        ]
    )
    im = src.resize((1280, 720), Image.Resampling.LANCZOS)
    # Cover baked title thoroughly (cream + gold flourishes + TABLE?)
    wash(im, (0, 0, 700, 380), sample=(720, 80, 1080, 300), blur=20)
    wash(im, (40, 200, 620, 420), sample=(780, 200, 1050, 360), blur=18)
    im = grade_left(im, width=600, alpha=140)
    draw_words(
        im,
        [[("LEFT", WHITE)], [("EMPTY", YELLOW)], [("ON PURPOSE", WHITE)]],
        x=36,
        y=40,
        size=96,
        max_w=640,
        gap=0.96,
    )
    dest = SELECTED / "hos_002_thumb_C_empty_on_purpose_v03.jpg"
    save_jpg(im, dest)
    return dest


def main() -> None:
    SELECTED.mkdir(parents=True, exist_ok=True)
    b = compose_b()
    c = compose_c()
    print("DONE", b.name, c.name, flush=True)


if __name__ == "__main__":
    main()
