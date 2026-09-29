#!/usr/bin/env python3
"""HOS 004 long thumbs A/B/C v03 — film 3D look + v02 fixes.

Ben override 29 Sep 2026. Nothing to Studio. No KEEP/LOCKED.

v02 went flat/graphic. v03 keeps the channel's 3D cartoon plates, full-bleed,
no split panels, no flat vector tiles. Keeps v02 fixes: correct Z numbers,
one clear idea, text off the subject (§2.5).

B: full-frame coin/knife from film (v01 look). Only move CUT GOLD? clear of blade.
A: close-up two 3D Te/I cubes from film; blank baked glyphs; overlay Te 52 / I 53.
C: Part 04 foil plate (dark 1909); composite ONE bright rebound particle + trail.

1280×720. Facts: Te Z=52, I Z=53. No atomic weights.
"""
from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
FRAMES = HERE / "_frames_v03"
SELECTED = HERE / "Selected"
DRAFTS = HERE / "Drafts"
PREVIEWS = HERE / "Previews"
ART = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts"

WHITE = (255, 255, 255)
YELLOW = (255, 214, 46)
INK = (18, 12, 8)
SHADOW = (10, 6, 4, 220)
GOLD_HOT = (255, 220, 120)

FONT = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
FONT_FALLBACK = "/System/Library/Fonts/Supplemental/Impact.ttf"
W, H = 1280, 720
TE_Z, I_Z = 52, 53


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
    if box:
        x0, y0, x1, y1 = box
        im = im.crop((int(x0 * im.width), int(y0 * im.height), int(x1 * im.width), int(y1 * im.height)))
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
    elif side == "top":
        for i in range(width):
            a = int(alpha * (1.0 - i / width) ** 1.2)
            if a > 0:
                od.line([(0, i), (im.width, i)], fill=(14, 8, 4, a))
    elif side == "bottom":
        for i in range(width):
            y = im.height - 1 - i
            a = int(alpha * (1.0 - i / width) ** 1.2)
            if a > 0:
                od.line([(0, y), (im.width, y)], fill=(14, 8, 4, a))
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
) -> tuple[int, int, int, int]:
    """Draw hook words. Returns bounding box (x0,y0,x1,y1) of the block."""
    draw = ImageDraw.Draw(im)
    cy = y
    max_right = x
    for line in lines:
        text = " ".join(w for w, _ in line)
        fsize = size
        f = font(fsize)
        while f.getlength(text) > max_w and fsize > 40:
            fsize -= 2
            f = font(fsize)
        stroke = max(8, fsize // 8)
        cx = x
        for w, color in line:
            draw.text((cx + 4, cy + 5), w, font=f, fill=SHADOW, stroke_width=stroke + 3, stroke_fill=SHADOW)
            draw.text((cx, cy), w, font=f, fill=color, stroke_width=stroke, stroke_fill=INK)
            cx += int(f.getlength(w + " "))
        max_right = max(max_right, cx)
        cy += int(fsize * gap)
    return (x, y, max_right, cy)


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


def blank_face_region(im: Image.Image, box: tuple[int, int, int, int], sample: tuple[int, int, int, int]) -> None:
    """Paint a wood-sampled patch over baked glyphs (blurred so it stays 3D)."""
    x0, y0, x1, y1 = box
    sx0, sy0, sx1, sy1 = sample
    patch = im.crop((sx0, sy0, sx1, sy1)).resize((x1 - x0, y1 - y0), Image.Resampling.LANCZOS)
    patch = patch.filter(ImageFilter.GaussianBlur(1.2))
    # slight noise so it doesn't look flat
    rng = random.Random(x0 * 17 + y0)
    px = patch.load()
    for yy in range(patch.height):
        for xx in range(0, patch.width, 3):
            r, g, b = px[xx, yy]
            d = rng.randint(-6, 6)
            px[xx, yy] = (max(0, min(255, r + d)), max(0, min(255, g + d)), max(0, min(255, b + d)))
    im.paste(patch, (x0, y0))


def draw_tile_overlay(
    im: Image.Image,
    *,
    symbol: str,
    number: int,
    box: tuple[int, int, int, int],
    glow: bool,
) -> None:
    """House-font Te/I + Z only. Never AI-baked."""
    x0, y0, x1, y1 = box
    tw, th = x1 - x0, y1 - y0
    draw = ImageDraw.Draw(im)
    n_size = max(34, th // 8)
    nf = font(n_size)
    num = str(number)
    nx = x0 + tw // 9
    ny = y0 + th // 9
    stroke = max(4, n_size // 8)
    ncol = GOLD_HOT if glow else WHITE
    draw.text((nx + 2, ny + 2), num, font=nf, fill=SHADOW, stroke_width=stroke + 2, stroke_fill=SHADOW)
    draw.text((nx, ny), num, font=nf, fill=ncol, stroke_width=stroke, stroke_fill=INK)

    s_size = max(70, th // 3)
    sf = font(s_size)
    while sf.getlength(symbol) > tw * 0.72 and s_size > 48:
        s_size -= 2
        sf = font(s_size)
    sw = sf.getlength(symbol)
    sx = int(x0 + (tw - sw) / 2)
    sy = int(y0 + th * 0.36)
    stroke = max(8, s_size // 8)
    scol = GOLD_HOT if glow else WHITE
    draw.text((sx + 3, sy + 4), symbol, font=sf, fill=SHADOW, stroke_width=stroke + 3, stroke_fill=SHADOW)
    draw.text((sx, sy), symbol, font=sf, fill=scol, stroke_width=stroke, stroke_fill=INK)


def compose_a() -> Path:
    """Close-up two 3D film tiles; blank baked glyphs; overlay Te 52 / I 53; I glowing."""
    # Part 02 hall cubes (frame_18) — full 3D cartoon wood tiles filling frame
    src = load(FRAMES / "frame_18.0.jpg")
    # Tight on the two foreground Te + I cube faces (fill frame; drop far hall)
    im = cover_crop(src, (0.20, 0.50, 0.60, 0.88))
    im = glow_boost(im, 1.08)

    # Face boxes after that crop (measured for 1280×720 cover)
    te_box = (40, 80, 600, 680)
    i_box = (640, 40, 1240, 640)

    # Blank baked Te/I + wrong Z/weight glyphs (28/319 · 21/39) — wood sample
    blank_face_region(
        im,
        (te_box[0] + 30, te_box[1] + 30, te_box[2] - 30, te_box[3] - 40),
        (te_box[0] + 40, te_box[1] + 10, te_box[0] + 160, te_box[1] + 80),
    )
    blank_face_region(
        im,
        (i_box[0] + 30, i_box[1] + 30, i_box[2] - 30, i_box[3] - 40),
        (i_box[0] + 40, i_box[1] + 10, i_box[0] + 160, i_box[1] + 80),
    )

    # Warm gold glow on I tile (hero)
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.rounded_rectangle(
        [i_box[0] - 8, i_box[1] - 8, i_box[2] + 8, i_box[3] + 8],
        radius=18,
        outline=(255, 200, 80, 170),
        width=12,
    )
    glow = glow.filter(ImageFilter.GaussianBlur(10))
    im = Image.alpha_composite(im.convert("RGBA"), glow).convert("RGB")
    wash = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(wash).rounded_rectangle(i_box, radius=12, fill=(255, 190, 70, 55))
    im = Image.alpha_composite(im.convert("RGBA"), wash).convert("RGB")

    draw_tile_overlay(im, symbol="Te", number=TE_Z, box=te_box, glow=False)
    draw_tile_overlay(im, symbol="I", number=I_Z, box=i_box, glow=True)

    # Soft top-left grade only — no side panel
    im = grade_band(im, side="top", width=220, alpha=120)
    im = grade_band(im, side="left", width=280, alpha=55)
    draw_words(
        im,
        [
            [("THE", WHITE), ("HIDDEN", YELLOW)],
            [("NUMBER", WHITE)],
        ],
        x=24,
        y=14,
        size=58,
        max_w=600,
        gap=1.0,
    )
    return save_jpg(im, SELECTED / "hos_004_thumb_A_hidden_number_v03.jpg")


def compose_b() -> Path:
    """Full-bleed coin+knife (v01 look). Only move CUT GOLD? clear of the blade."""
    src = load(FRAMES / "frame_3.0.jpg")
    # Exact v01 crop language — full-bleed subject, no black side panel
    im = cover_crop(src, (0.18, 0.12, 0.92, 0.88))
    im = glow_boost(im, 1.1)
    # Soft readability grade only (not a split panel)
    im = grade_band(im, side="top", width=200, alpha=120)
    im = grade_band(im, side="left", width=300, alpha=70)
    # Two-line hook hard top-left; short of the blade
    draw_words(
        im,
        [
            [("CUT", WHITE)],
            [("GOLD?", YELLOW)],
        ],
        x=22,
        y=12,
        size=80,
        max_w=360,
        gap=0.95,
    )
    return save_jpg(im, SELECTED / "hos_004_thumb_B_cut_gold_v03.jpg")


def compose_c() -> Path:
    """Part 04 foil (dark 1909) + ONE bright rebound particle with short trail."""
    src = load(FRAMES / "p04_foil_2.0.jpg")
    # Crop tight so foil owns the frame (no beds / constellations)
    im = cover_crop(src, (0.22, 0.18, 0.82, 0.82))
    im = glow_boost(im, 1.08)
    im = ImageEnhance.Color(im).enhance(1.1)
    im = ImageEnhance.Contrast(im).enhance(1.05)

    # Mild edge vignette — keep 3D foil centre
    vig = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    vd = ImageDraw.Draw(vig)
    for i in range(140):
        a = int(100 * (i / 140) ** 1.6)
        vd.rectangle([i, i, W - 1 - i, H - 1 - i], outline=(6, 4, 2, a))
    im = Image.alpha_composite(im.convert("RGBA"), vig).convert("RGB")

    particles = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pd = ImageDraw.Draw(particles)
    # Impact on foil face → hero arcs back toward camera (lower-left)
    impact_x, impact_y = 640, 360
    hero_x, hero_y = 280, 560
    for i in range(16):
        t = i / 15
        x = int(impact_x + (hero_x - impact_x) * t)
        y = int(impact_y + (hero_y - impact_y) * t - math.sin(t * math.pi) * 40)
        r = int(5 + t * 16)
        a = int(60 + t * 180)
        pd.ellipse([x - r, y - r, x + r, y + r], fill=(255, 230, 120, a))
    hx, hy, hr = hero_x, hero_y, 38
    pd.ellipse([hx - hr - 24, hy - hr - 24, hx + hr + 24, hy + hr + 24], fill=(255, 200, 80, 95))
    pd.ellipse([hx - hr, hy - hr, hx + hr, hy + hr], fill=(255, 245, 190, 255))
    pd.ellipse([hx - hr // 2, hy - hr // 2, hx + hr // 2, hy + hr // 2], fill=(255, 255, 255, 255))

    bloom = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(bloom).ellipse([hx - 90, hy - 90, hx + 90, hy + 90], fill=(255, 210, 90, 110))
    bloom = bloom.filter(ImageFilter.GaussianBlur(22))
    im = Image.alpha_composite(im.convert("RGBA"), bloom)
    im = Image.alpha_composite(im, particles).convert("RGB")

    im = grade_band(im, side="top", width=220, alpha=110)
    im = grade_band(im, side="left", width=300, alpha=70)
    draw_words(
        im,
        [
            [("IT", WHITE)],
            [("BOUNCED", YELLOW)],
            [("BACK", WHITE)],
        ],
        x=24,
        y=18,
        size=70,
        max_w=460,
        gap=1.0,
    )
    return save_jpg(im, SELECTED / "hos_004_thumb_C_bounced_back_v03.jpg")


def main() -> None:
    assert TE_Z == 52 and I_Z == 53
    SELECTED.mkdir(parents=True, exist_ok=True)
    DRAFTS.mkdir(parents=True, exist_ok=True)
    PREVIEWS.mkdir(parents=True, exist_ok=True)
    paths = [compose_a(), compose_b(), compose_c()]
    for p in paths:
        (DRAFTS / p.name).write_bytes(p.read_bytes())
        (ART / p.name).write_bytes(p.read_bytes())
    print("DONE", [p.name for p in paths])
    print(f"FACT_LOCK Te={TE_Z} I={I_Z} · full-bleed 3D film plates · no Studio")


if __name__ == "__main__":
    main()
