#!/usr/bin/env python3
"""HOS 004 long thumbs A/B/C v02 — Ben review (29 Sep 2026).

Nothing to Studio. UAT only.

B KEEP as main — move CUT GOLD? up/left so no letter touches the knife (§2.5).
A REDO — close-up TWO blank tiles; house-font overlays "Te 52" / "I 53" only (never baked).
C REDO — dark simple bg, gold foil, thin stream, ONE bright rebound particle toward camera.

1280×720. Facts: Te Z=52, I Z=53. No atomic weights on tiles.
"""
from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
PROJ = HERE.parent
FRAMES = HERE / "_frames_v02"
if not FRAMES.exists():
    FRAMES = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts/hos004_thumb_frames"
DRAFTS = HERE / "Drafts"
SELECTED = HERE / "Selected"
PREVIEWS = HERE / "Previews"
ART = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts"

WHITE = (255, 255, 255)
YELLOW = (255, 214, 46)
INK = (18, 12, 8)
SHADOW = (10, 6, 4, 220)
GOLD = (232, 176, 64)
GOLD_HOT = (255, 220, 120)

FONT = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
FONT_FALLBACK = "/System/Library/Fonts/Supplemental/Impact.ttf"

W, H = 1280, 720

# Atomic numbers (fact lock — overlay only, never baked into a generated plate)
TE_Z = 52
I_Z = 53


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
        while f.getlength(text) > max_w and fsize > 40:
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


def _wood_tile(size: int, *, glow: bool = False) -> Image.Image:
    """Blank wooden element tile — NO letters/numbers baked in."""
    tile = Image.new("RGB", (size, size), (92, 58, 28))
    d = ImageDraw.Draw(tile)
    # face panel
    inset = int(size * 0.07)
    face = (inset, inset, size - inset, size - inset)
    base = (118, 78, 42) if not glow else (160, 110, 48)
    d.rounded_rectangle(face, radius=int(size * 0.04), fill=base)
    # subtle grain
    rng = random.Random(52 if not glow else 53)
    for _ in range(180):
        x = rng.randint(inset + 4, size - inset - 4)
        y = rng.randint(inset + 4, size - inset - 4)
        shade = rng.randint(-18, 14)
        c = tuple(max(0, min(255, base[i] + shade)) for i in range(3))
        d.point((x, y), fill=c)
    # brass rim
    rim = (210, 170, 70) if glow else (168, 130, 55)
    d.rounded_rectangle(face, radius=int(size * 0.04), outline=rim, width=max(4, size // 48))
    inner = (inset + 8, inset + 8, size - inset - 8, size - inset - 8)
    d.rounded_rectangle(inner, radius=int(size * 0.03), outline=(70, 42, 20), width=2)
    if glow:
        # warm gold wash on face only (still blank — labels come later)
        wash = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        wd = ImageDraw.Draw(wash)
        wd.rounded_rectangle(face, radius=int(size * 0.04), fill=(255, 200, 80, 70))
        tile = Image.alpha_composite(tile.convert("RGBA"), wash).convert("RGB")
        glow_layer = tile.filter(ImageFilter.GaussianBlur(10))
        tile = Image.blend(tile, glow_layer, 0.22)
        tile = ImageEnhance.Brightness(tile).enhance(1.12)
        tile = ImageEnhance.Color(tile).enhance(1.2)
    return tile


def _draw_tile_labels(im: Image.Image, *, symbol: str, number: int, box: tuple[int, int, int, int], glow: bool) -> None:
    """House-font overlays AFTER — symbol + atomic number only. No weights."""
    x0, y0, x1, y1 = box
    tw, th = x1 - x0, y1 - y0
    draw = ImageDraw.Draw(im)
    # number top-left of face
    n_size = max(36, th // 7)
    nf = font(n_size)
    num = str(number)
    nx = x0 + tw // 10
    ny = y0 + th // 10
    stroke = max(4, n_size // 8)
    ncol = GOLD_HOT if glow else WHITE
    draw.text((nx + 2, ny + 2), num, font=nf, fill=SHADOW, stroke_width=stroke + 2, stroke_fill=SHADOW)
    draw.text((nx, ny), num, font=nf, fill=ncol, stroke_width=stroke, stroke_fill=INK)
    # symbol centred
    s_size = max(72, th // 3)
    sf = font(s_size)
    while sf.getlength(symbol) > tw * 0.7 and s_size > 48:
        s_size -= 2
        sf = font(s_size)
    sw = sf.getlength(symbol)
    sx = int(x0 + (tw - sw) / 2)
    sy = int(y0 + th * 0.38)
    stroke = max(8, s_size // 8)
    scol = GOLD_HOT if glow else WHITE
    draw.text((sx + 3, sy + 4), symbol, font=sf, fill=SHADOW, stroke_width=stroke + 3, stroke_fill=SHADOW)
    draw.text((sx, sy), symbol, font=sf, fill=scol, stroke_width=stroke, stroke_fill=INK)


def compose_a() -> Path:
    """TWO blank tiles fill the frame; Te 52 + I 53 overlaid; I glowing; hook top-left."""
    # Warm dark desk / void behind the two tiles
    bg = Image.new("RGB", (W, H), (28, 18, 10))
    # soft vignette light
    light = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(light)
    for i in range(280):
        a = int(90 * (1 - i / 280) ** 1.4)
        ld.ellipse(
            [W // 2 - 520 - i, H // 2 - 300 - i, W // 2 + 520 + i, H // 2 + 340 + i],
            outline=(80, 50, 20, a),
        )
    bg = Image.alpha_composite(bg.convert("RGBA"), light).convert("RGB")

    tile_h = 560
    gap = 36
    tile_w = tile_h
    total_w = tile_w * 2 + gap
    left_x = (W - total_w) // 2
    top_y = (H - tile_h) // 2 + 30  # leave headroom for hook text

    te = _wood_tile(tile_w, glow=False).resize((tile_w, tile_h), Image.Resampling.LANCZOS)
    iod = _wood_tile(tile_w, glow=True).resize((tile_w, tile_h), Image.Resampling.LANCZOS)

    # soft drop shadows
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    for dx, dy, a in ((18, 22, 110), (8, 10, 80)):
        sd.rounded_rectangle(
            [left_x + dx, top_y + dy, left_x + tile_w + dx, top_y + tile_h + dy],
            radius=18,
            fill=(0, 0, 0, a),
        )
        sd.rounded_rectangle(
            [left_x + tile_w + gap + dx, top_y + dy, left_x + total_w + dx, top_y + tile_h + dy],
            radius=18,
            fill=(0, 0, 0, a),
        )
    shadow = shadow.filter(ImageFilter.GaussianBlur(16))
    bg = Image.alpha_composite(bg.convert("RGBA"), shadow).convert("RGB")

    bg.paste(te, (left_x, top_y))
    bg.paste(iod, (left_x + tile_w + gap, top_y))

    # I warm gold rim glow (behind labels)
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    ix0 = left_x + tile_w + gap
    gd.rounded_rectangle(
        [ix0 - 12, top_y - 12, ix0 + tile_w + 12, top_y + tile_h + 12],
        radius=22,
        outline=(255, 200, 80, 160),
        width=10,
    )
    glow = glow.filter(ImageFilter.GaussianBlur(8))
    bg = Image.alpha_composite(bg.convert("RGBA"), glow).convert("RGB")

    # FACT overlays — house font only
    _draw_tile_labels(bg, symbol="Te", number=TE_Z, box=(left_x, top_y, left_x + tile_w, top_y + tile_h), glow=False)
    _draw_tile_labels(
        bg,
        symbol="I",
        number=I_Z,
        box=(left_x + tile_w + gap, top_y, left_x + total_w, top_y + tile_h),
        glow=True,
    )

    # Hook top-left, clear of tiles
    draw_words(
        bg,
        [
            [("THE", WHITE), ("HIDDEN", YELLOW)],
            [("NUMBER", WHITE)],
        ],
        x=28,
        y=18,
        size=64,
        max_w=700,
        gap=1.0,
    )
    return save_jpg(bg, SELECTED / "hos_004_thumb_A_hidden_number_v02.jpg")


def compose_b() -> Path:
    """KEEP subject from v01; CUT GOLD? moved up/left — clear of knife blade."""
    src = load(FRAMES / "frame_3.0.jpg")
    # Tight on coin; push subject right so hook stays in a free left column
    subject = cover_crop(src, (0.30, 0.30, 0.98, 0.95))
    subject = glow_boost(subject, 1.08)
    canvas = Image.new("RGB", (W, H), (16, 10, 8))
    # Subject starts past the hook column — text must never enter this x
    ox, oy = 460, 60
    sw, sh = W - ox, H - oy
    sub = subject.resize((sw, sh), Image.Resampling.LANCZOS)
    canvas.paste(sub, (ox, oy))
    im = grade_band(canvas, side="left", width=480, alpha=40)
    # Hook confined to left column (< ox) — §2.5 text off subject
    draw_words(
        im,
        [
            [("CUT", WHITE)],
            [("GOLD?", YELLOW)],
        ],
        x=28,
        y=40,
        size=80,
        max_w=ox - 48,
        gap=0.95,
    )
    return save_jpg(im, SELECTED / "hos_004_thumb_B_cut_gold_v02.jpg")


def _gold_foil_square(w: int, h: int) -> Image.Image:
    """Procedural gold foil only — no room, no constellations, no baked text."""
    foil = Image.new("RGB", (w, h), (180, 140, 55))
    d = ImageDraw.Draw(foil)
    rng = random.Random(1909)
    # crumpled foil noise
    for _ in range(w * h // 8):
        x = rng.randint(0, w - 1)
        y = rng.randint(0, h - 1)
        shade = rng.randint(-40, 50)
        c = (
            max(40, min(255, 190 + shade)),
            max(30, min(230, 150 + shade // 2)),
            max(20, min(120, 50 + shade // 3)),
        )
        d.point((x, y), fill=c)
    # soft diagonal highlights
    for i in range(0, w, 3):
        y0 = int((i / w) * h * 0.4)
        d.line([(i, y0), (i, min(h - 1, y0 + 40))], fill=(240, 210, 120), width=1)
    foil = foil.filter(ImageFilter.GaussianBlur(0.8))
    foil = ImageEnhance.Contrast(foil).enhance(1.15)
    foil = ImageEnhance.Color(foil).enhance(1.1)
    # thin dark edge
    d = ImageDraw.Draw(foil)
    d.rectangle([0, 0, w - 1, h - 1], outline=(70, 50, 20), width=3)
    return foil


def compose_c() -> Path:
    """Dark simple bg · gold foil square · thin stream · ONE bright rebound toward camera."""
    # Dark charcoal void — nothing else
    bg = Image.new("RGB", (W, H), (10, 9, 12))
    wash = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(wash)
    for i in range(180):
        a = int(40 * (1 - i / 180) ** 1.5)
        wd.ellipse(
            [W // 2 - 160 - i, H // 2 - 140 - i, W // 2 + 200 + i, H // 2 + 180 + i],
            outline=(50, 35, 12, a),
        )
    bg = Image.alpha_composite(bg.convert("RGBA"), wash).convert("RGB")

    foil = _gold_foil_square(320, 460)
    fx = W // 2 - foil.width // 2 + 50
    fy = H // 2 - foil.height // 2 + 24
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle(
        [fx + 12, fy + 16, fx + foil.width + 12, fy + foil.height + 16],
        radius=6,
        fill=(0, 0, 0, 150),
    )
    sh = sh.filter(ImageFilter.GaussianBlur(14))
    bg = Image.alpha_composite(bg.convert("RGBA"), sh).convert("RGB")
    bg.paste(foil, (fx, fy))

    # Particle layer
    particles = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pd = ImageDraw.Draw(particles)
    rng = random.Random(1909)
    # Thin stream left → through foil → right (most pass through)
    y_stream = H // 2 + 10
    for i in range(55):
        t = i / 54
        x = int(40 + t * (W - 80))
        # slight jitter
        y = int(y_stream + rng.uniform(-6, 6) + math.sin(t * 6) * 3)
        # skip dense core inside foil so bounce reads
        r = 3 if 0.35 < t < 0.55 else 4
        col = (120, 255, 160, 200) if t < 0.55 else (140, 255, 170, 160)
        pd.ellipse([x - r, y - r, x + r, y + r], fill=col)
        # soft bloom
        pd.ellipse([x - r - 2, y - r - 2, x + r + 2, y + r + 2], outline=(80, 220, 120, 40))

    # ONE bright hero particle flying straight back toward camera (larger = closer)
    impact_x = fx + 8
    impact_y = y_stream
    hero_x, hero_y = 240, 480
    for i in range(16):
        t = i / 15
        # mostly linear toward camera (slight down)
        x = int(impact_x + (hero_x - impact_x) * t)
        y = int(impact_y + (hero_y - impact_y) * t)
        r = int(4 + t * 16)
        a = int(90 + t * 150)
        pd.ellipse([x - r, y - r, x + r, y + r], fill=(255, 235, 130, a))
    hx, hy, hr = hero_x, hero_y, 32
    pd.ellipse([hx - hr - 20, hy - hr - 20, hx + hr + 20, hy + hr + 20], fill=(255, 220, 100, 80))
    pd.ellipse([hx - hr, hy - hr, hx + hr, hy + hr], fill=(255, 248, 200, 255))
    pd.ellipse([hx - hr // 2, hy - hr // 2, hx + hr // 2, hy + hr // 2], fill=(255, 255, 255, 255))

    particles = particles.filter(ImageFilter.GaussianBlur(0.6))
    # Extra bloom on hero
    bloom = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(bloom).ellipse([hx - 70, hy - 70, hx + 70, hy + 70], fill=(255, 210, 80, 90))
    bloom = bloom.filter(ImageFilter.GaussianBlur(18))
    bg = Image.alpha_composite(bg.convert("RGBA"), bloom)
    bg = Image.alpha_composite(bg, particles).convert("RGB")

    # Hook clear of the rebound particle (top-left, away from lower-left hero)
    draw_words(
        bg,
        [
            [("IT", WHITE)],
            [("BOUNCED", YELLOW)],
            [("BACK", WHITE)],
        ],
        x=28,
        y=36,
        size=78,
        max_w=520,
        gap=1.0,
    )
    return save_jpg(bg, SELECTED / "hos_004_thumb_C_bounced_back_v02.jpg")


def main() -> None:
    DRAFTS.mkdir(parents=True, exist_ok=True)
    SELECTED.mkdir(parents=True, exist_ok=True)
    PREVIEWS.mkdir(parents=True, exist_ok=True)
    assert TE_Z == 52 and I_Z == 53
    paths = [compose_a(), compose_b(), compose_c()]
    for p in paths:
        (DRAFTS / p.name).write_bytes(p.read_bytes())
        (ART / p.name).write_bytes(p.read_bytes())
    print("DONE", [p.name for p in paths])
    print(f"FACT_LOCK Te={TE_Z} I={I_Z} (overlays only; no baked tile text)")


if __name__ == "__main__":
    main()
