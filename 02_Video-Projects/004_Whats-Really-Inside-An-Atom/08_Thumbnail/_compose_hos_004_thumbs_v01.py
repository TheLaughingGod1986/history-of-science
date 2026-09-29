#!/usr/bin/env python3
"""HOS 004 long thumbs A/B/C v01 — from the film's own plates.

Rules: THUMBNAIL_AND_TITLE_RULES.md §2
  A: Te/I swapped+glowing · THE HIDDEN NUMBER (HIDDEN yellow) · no Explorer
  B: gold coin + knife · CUT GOLD? (GOLD yellow) · no Explorer
  C: gold-foil bounce · IT BOUNCED BACK (BOUNCED yellow) · subject-only

1280×720. thumb_preview.py long sheet for each.
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
PROJ = HERE.parent
FRAMES = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts/hos004_thumb_frames"
DRAFTS = HERE / "Drafts"
SELECTED = HERE / "Selected"
PREVIEWS = HERE / "Previews"
ART = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts"

WHITE = (255, 255, 255)
YELLOW = (255, 214, 46)
INK = (18, 12, 8)
SHADOW = (10, 6, 4, 220)

FONT = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
FONT_FALLBACK = "/System/Library/Fonts/Supplemental/Impact.ttf"

W, H = 1280, 720


def font(size: int) -> ImageFont.FreeTypeFont:
    for path in (FONT, FONT_FALLBACK):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def load(path: Path) -> Image.Image:
    if not path.exists():
        raise SystemExit(f"missing {path}")
    return Image.open(path).convert("RGB")


def cover_crop(im: Image.Image, box: tuple[float, float, float, float] | None = None) -> Image.Image:
    """Crop fractional box then fit 1280×720."""
    if box:
        x0, y0, x1, y1 = box
        im = im.crop((int(x0 * im.width), int(y0 * im.height), int(x1 * im.width), int(y1 * im.height)))
    # fit cover
    scale = max(W / im.width, H / im.height)
    nw, nh = int(im.width * scale), int(im.height * scale)
    im = im.resize((nw, nh), Image.Resampling.LANCZOS)
    left = (nw - W) // 2
    top = (nh - H) // 2
    return im.crop((left, top, left + W, top + H))


def grade_band(im: Image.Image, *, side: str = "left", width: int = 620, alpha: int = 130) -> Image.Image:
    overlay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    if side == "left":
        for i in range(width):
            a = int(alpha * (1.0 - i / width) ** 1.35)
            if a > 0:
                od.line([(i, 0), (i, im.height)], fill=(14, 8, 4, a))
    elif side == "bottom":
        for i in range(width):
            y = im.height - 1 - i
            a = int(alpha * (1.0 - i / width) ** 1.2)
            if a > 0:
                od.line([(0, y), (im.width, y)], fill=(14, 8, 4, a))
    elif side == "top":
        for i in range(width):
            a = int(alpha * (1.0 - i / width) ** 1.2)
            if a > 0:
                od.line([(0, i), (im.width, i)], fill=(14, 8, 4, a))
    return Image.alpha_composite(im.convert("RGBA"), overlay).convert("RGB")


def glow_boost(im: Image.Image, amount: float = 1.15) -> Image.Image:
    im = ImageEnhance.Color(im).enhance(1.12)
    im = ImageEnhance.Contrast(im).enhance(1.08)
    im = ImageEnhance.Brightness(im).enhance(amount)
    return im


def draw_words(
    im: Image.Image,
    lines: list[list[tuple[str, tuple[int, int, int]]]],
    *,
    x: int,
    y: int,
    size: int,
    max_w: int,
    gap: float = 1.05,
) -> None:
    draw = ImageDraw.Draw(im)
    cy = y
    for line in lines:
        text = " ".join(w for w, _ in line)
        fsize = size
        f = font(fsize)
        while f.getlength(text) > max_w and fsize > 44:
            fsize -= 2
            f = font(fsize)
        stroke = max(8, fsize // 8)
        cx = x
        for w, color in line:
            draw.text((cx + 4, cy + 5), w, font=f, fill=SHADOW, stroke_width=stroke + 3, stroke_fill=SHADOW)
            draw.text((cx, cy), w, font=f, fill=color, stroke_width=stroke, stroke_fill=INK)
            cx += int(f.getlength(w + " "))
        cy += int(fsize * gap)


def save_jpg(im: Image.Image, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    rgb = im.convert("RGB").resize((W, H), Image.Resampling.LANCZOS)
    q = 92
    rgb.save(dest, "JPEG", quality=q, optimize=True, subsampling=1)
    while dest.stat().st_size > 1_900_000 and q > 72:
        q -= 4
        rgb.save(dest, "JPEG", quality=q, optimize=True, subsampling=1)
    print(f"{dest.name}  {dest.stat().st_size} B  q={q}", flush=True)
    return dest


def compose_a() -> Path:
    """Te + I boxes swapped/glowing — THE HIDDEN NUMBER."""
    # Prefer frame_18 (Te + I crates both readable) over wide 22.0 hall
    for name, box in (
        ("frame_18.0.jpg", (0.12, 0.28, 0.78, 0.92)),
        ("frame_22.0.jpg", (0.00, 0.28, 0.72, 0.95)),
        ("plate_05_hand_tap_te_i_v01.jpg", (0.05, 0.25, 0.75, 0.95)),
    ):
        path = FRAMES / name
        if path.exists():
            src = load(path)
            im = cover_crop(src, box)
            break
    else:
        raise SystemExit("no Te/I frame for thumb A")
    im = glow_boost(im, 1.18)
    glow = im.filter(ImageFilter.GaussianBlur(18))
    im = Image.blend(im, glow, 0.18)
    im = grade_band(im, side="bottom", width=300, alpha=155)
    im = grade_band(im, side="left", width=480, alpha=110)
    draw_words(
        im,
        [
            [("THE", WHITE), ("HIDDEN", YELLOW)],
            [("NUMBER", WHITE)],
        ],
        x=40,
        y=420,
        size=96,
        max_w=860,
    )
    return save_jpg(im, SELECTED / "hos_004_thumb_A_hidden_number_v01.jpg")


def compose_b() -> Path:
    """Coin halves + knife — CUT GOLD?"""
    src = load(FRAMES / "frame_3.0.jpg")
    # ECU on coin/knife; bias right so text can sit left
    im = cover_crop(src, (0.18, 0.12, 0.92, 0.88))
    im = glow_boost(im, 1.1)
    im = grade_band(im, side="left", width=560, alpha=145)
    draw_words(
        im,
        [[("CUT", WHITE), ("GOLD?", YELLOW)]],
        x=40,
        y=280,
        size=118,
        max_w=700,
    )
    return save_jpg(im, SELECTED / "hos_004_thumb_B_cut_gold_v01.jpg")


def compose_c() -> Path:
    """Gold foil bounce — IT BOUNCED BACK. Subject only (no Explorer)."""
    # Prefer film frame with clear particle spray
    candidates = [
        FRAMES / "frame_50.5.jpg",
        FRAMES / "frame_51.0.jpg",
        FRAMES / "frame_49.0.jpg",
        FRAMES / "11_one_bounces_v02.jpg" if False else FRAMES / "frame_50.5.jpg",
    ]
    src = None
    for c in candidates:
        if c.exists():
            src = load(c)
            break
    assert src is not None
    im = cover_crop(src, (0.08, 0.15, 0.92, 0.88))
    im = glow_boost(im, 1.12)
    im = grade_band(im, side="bottom", width=300, alpha=160)
    im = grade_band(im, side="left", width=380, alpha=100)
    draw_words(
        im,
        [
            [("IT", WHITE)],
            [("BOUNCED", YELLOW)],
            [("BACK", WHITE)],
        ],
        x=40,
        y=320,
        size=96,
        max_w=780,
    )
    return save_jpg(im, SELECTED / "hos_004_thumb_C_bounced_back_v01.jpg")


def main() -> None:
    DRAFTS.mkdir(parents=True, exist_ok=True)
    SELECTED.mkdir(parents=True, exist_ok=True)
    PREVIEWS.mkdir(parents=True, exist_ok=True)
    paths = [compose_a(), compose_b(), compose_c()]
    # Also copy drafts
    for p in paths:
        (DRAFTS / p.name).write_bytes(p.read_bytes())
    print("DONE", [p.name for p in paths])


if __name__ == "__main__":
    main()
