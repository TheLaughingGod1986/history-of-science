#!/usr/bin/env python3
"""Pull painted-in cover type into a Shorts-feed safe zone.

Does not remint the scene. Scales the locked Animistry cover and fills the new
top/side margin from edge colours so letters sit inside the feed UI crop.
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

HERE = Path(__file__).resolve().parent
SHORTS = HERE / "Shorts"
W, H = 1080, 1920
# Shorts feed: status / island / header on top; rounded corners + side UI.
TOP = 176
SIDE = 100
SCALE = (W - 2 * SIDE) / W  # 0.8148
JOBS = [
    {
        "src": SHORTS / "hos_001_s01_shadow_cover_animistry_v01.png",
        "png": SHORTS / "hos_001_s01_shadow_cover_animistry_v02.png",
        "jpg": SHORTS / "hos_001_s01_shadow_cover_animistry_v02.jpg",
    },
    {
        "src": SHORTS / "hos_001_s02_pond_cover_animistry_v02.png",
        "png": SHORTS / "hos_001_s02_pond_cover_animistry_v03.png",
        "jpg": SHORTS / "hos_001_s02_pond_cover_animistry_v03.jpg",
    },
    {
        "src": SHORTS / "hos_001_s03_vector_cover_animistry_v01.png",
        "png": SHORTS / "hos_001_s03_vector_cover_animistry_v02.png",
        "jpg": SHORTS / "hos_001_s03_vector_cover_animistry_v02.jpg",
    },
    {
        "src": SHORTS / "hos_001_s04_flask_cover_animistry_v02.png",
        "png": SHORTS / "hos_001_s04_flask_cover_animistry_v03.png",
        "jpg": SHORTS / "hos_001_s04_flask_cover_animistry_v03.jpg",
    },
    {
        "src": SHORTS / "hos_001_s05_soap_cover_animistry_v01.png",
        "png": SHORTS / "hos_001_s05_soap_cover_animistry_v02.png",
        "jpg": SHORTS / "hos_001_s05_soap_cover_animistry_v02.jpg",
    },
]


def sample(im: Image.Image, box: tuple[int, int, int, int]) -> tuple[int, int, int]:
    c = im.crop(box).resize((1, 1), Image.Resampling.BOX)
    px = c.getpixel((0, 0))
    return int(px[0]), int(px[1]), int(px[2])


def fill_canvas(im: Image.Image) -> Image.Image:
    """Full-bleed wash from the scene edges — not a blurred clone of the type."""
    w, h = im.size
    # Prefer side/bottom scene, not the title band.
    left = sample(im, (0, int(h * 0.45), 28, int(h * 0.72)))
    right = sample(im, (w - 28, int(h * 0.45), w, int(h * 0.72)))
    top_l = sample(im, (0, int(h * 0.22), 36, int(h * 0.34)))
    top_r = sample(im, (w - 36, int(h * 0.22), w, int(h * 0.34)))
    bot = sample(im, (int(w * 0.35), h - 48, int(w * 0.65), h))
    canvas = Image.new("RGB", (W, H), bot)
    draw = ImageDraw.Draw(canvas)
    # Vertical wash: ceiling-ish into lower scene.
    for y in range(H):
        t = y / max(H - 1, 1)
        # Ease so the top pad (where type used to clip) stays darker/quieter.
        u = t ** 0.72
        r = int(top_l[0] * (1 - u) + bot[0] * u)
        g = int(top_l[1] * (1 - u) + bot[1] * u)
        b = int(top_l[2] * (1 - u) + bot[2] * u)
        draw.line([(0, y), (W, y)], fill=(r, g, b))
    # Soft left/right vignette toward sampled wall colours.
    overlay = Image.new("RGB", (W, H), left)
    od = ImageDraw.Draw(overlay)
    for x in range(W):
        t = x / max(W - 1, 1)
        r = int(left[0] * (1 - t) + right[0] * t)
        g = int(left[1] * (1 - t) + right[1] * t)
        b = int(left[2] * (1 - t) + right[2] * t)
        od.line([(x, 0), (x, H)], fill=(r, g, b))
    canvas = Image.blend(canvas, overlay, 0.28)
    # Keep the pad in the same grade as the scene — not a black letterbox.
    canvas = ImageEnhance.Brightness(canvas).enhance(0.94)
    canvas = canvas.filter(ImageFilter.GaussianBlur(radius=14))
    body = im.crop((0, int(h * 0.42), w, h)).resize((W, H), Image.Resampling.LANCZOS)
    body = ImageEnhance.Brightness(body).enhance(0.78)
    body = body.filter(ImageFilter.GaussianBlur(radius=36))
    canvas = Image.blend(canvas, body, 0.22)
    return canvas


def compose(src: Path) -> Image.Image:
    im = Image.open(src).convert("RGB")
    if im.size != (W, H):
        im = im.resize((W, H), Image.Resampling.LANCZOS)
    nw = int(round(W * SCALE))
    nh = int(round(H * SCALE))
    small = im.resize((nw, nh), Image.Resampling.LANCZOS)
    x = (W - nw) // 2
    y = TOP
    canvas = fill_canvas(im)
    canvas.paste(small, (x, y))
    return canvas


def save_jpg(png_im: Image.Image, dest: Path) -> None:
    rgb = png_im.convert("RGB")
    dest.parent.mkdir(parents=True, exist_ok=True)
    q = 88
    rgb.save(dest, "JPEG", quality=q, optimize=True, subsampling=1)
    while dest.stat().st_size > 1_800_000 and q > 70:
        q -= 4
        rgb.save(dest, "JPEG", quality=q, optimize=True, subsampling=1)


def main() -> None:
    for job in JOBS:
        src = job["src"]
        if not src.exists():
            src = src.with_suffix(".jpg")
        assert src.exists(), src
        out = compose(src)
        job["png"].parent.mkdir(parents=True, exist_ok=True)
        out.save(job["png"], "PNG")
        save_jpg(out, job["jpg"])
        print(
            f"WROTE {job['jpg'].name}  {job['jpg'].stat().st_size}  "
            f"png={job['png'].stat().st_size}  scale={SCALE:.3f} top={TOP} side={SIDE}"
        )


if __name__ == "__main__":
    main()
