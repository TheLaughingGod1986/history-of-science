#!/usr/bin/env python3
"""Compose v07 mid-air Atomic Weights marks for plate 03 I2V starts.

KEEP desk marks from v06 (H 1 / O 16 / C 12 on upright hero).
ADD phone-readable dark ink on 2–3 mid-air cream sheets only: H 1 · C 12 · O 16.
MOST flying sheets stay blank. No N 14 / S 32 wall — swirl stays sparse.
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

STILL_V06 = Path(__file__).resolve().parents[1] / "04_Generated-Clips/part03/refs/v06_stills"
STILL = Path(__file__).resolve().parents[1] / "04_Generated-Clips/part03/refs/v07_stills"
INK = (28, 22, 16, 245)
INK_SOFT = (36, 28, 20, 210)


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
    angle: float = 0.0,
    canvas: Image.Image | None = None,
) -> None:
    text = f"{symbol} {number}"
    f = font(size)
    if abs(angle) < 0.5 or canvas is None:
        x, y = xy
        draw.text((x + 2, y + 2), text, font=f, fill=(0, 0, 0, 100))
        draw.text((x, y), text, font=f, fill=fill)
        return
    tmp = Image.new("RGBA", (size * 6, size * 3), (0, 0, 0, 0))
    td = ImageDraw.Draw(tmp)
    td.text((4, 4), text, font=f, fill=(0, 0, 0, 90))
    td.text((2, 2), text, font=f, fill=fill)
    rot = tmp.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
    bbox = rot.getbbox()
    if bbox:
        rot = rot.crop(bbox)
    x, y = xy
    canvas.alpha_composite(rot, dest=(max(0, x), max(0, y)))


def strip_top_right_chrome(im: Image.Image) -> Image.Image:
    out = im.convert("RGB").copy()
    w, h = out.size
    wood = out.getpixel((int(w * 0.55), int(h * 0.08)))
    for fx0, fy0, fx1, fy1 in (
        (0.70, 0.0, 1.0, 0.18),
        (0.82, 0.0, 1.0, 0.24),
    ):
        x0, y0 = int(w * fx0), int(h * fy0)
        x1, y1 = int(w * fx1), int(h * fy1)
        ImageDraw.Draw(out).rectangle((x0, y0, x1, y1), fill=wood)
    return out


def crop_16x9(im: Image.Image, *, max_w: int = 1920) -> Image.Image:
    im = im.convert("RGB")
    w, h = im.size
    target_ratio = 16 / 9
    ratio = w / h
    if ratio > target_ratio * 1.02:
        new_w = int(h * target_ratio)
        left = (w - new_w) // 2
        im = im.crop((left, 0, left + new_w, h))
        w, h = im.size
    elif ratio < target_ratio * 0.98:
        new_h = int(w / target_ratio)
        top = max(0, (h - new_h) // 2)
        im = im.crop((0, top, w, top + new_h))
        w, h = im.size
    if w > max_w:
        nh = int(h * (max_w / w))
        im = im.resize((max_w, nh), Image.Resampling.LANCZOS)
    return im


def compose_swirl_hco_only(src: Path, dest: Path) -> None:
    """2–3 mid-air marks only: H 1 · C 12 · O 16. Most sheets blank."""
    raw = crop_16x9(strip_top_right_chrome(Image.open(src)))
    im = raw.convert("RGBA")
    w, h = im.size
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    placements = [
        (0.34, 0.46, "H", "1", max(44, w // 32), -14),
        (0.54, 0.38, "O", "16", max(42, w // 34), 11),
        (0.64, 0.54, "C", "12", max(40, w // 36), -7),
    ]
    for fx, fy, sym, num, sz, ang in placements:
        draw_mark(
            ImageDraw.Draw(overlay),
            (int(w * fx), int(h * fy)),
            sym,
            num,
            size=sz,
            angle=ang,
            canvas=overlay,
        )
    out = Image.alpha_composite(im, overlay).convert("RGB")
    dest.parent.mkdir(parents=True, exist_ok=True)
    out.save(dest, quality=95)
    print(f"wrote {dest.name} {out.size}", flush=True)


def compose_desk_keep_plus_midair(src: Path, dest: Path) -> None:
    """KEEP upright desk H/O/C; add 2–3 mid-air H/C/O on blank flying sheets."""
    raw = crop_16x9(Image.open(src))
    im = raw.convert("RGBA")
    w, h = im.size
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    # Mid-air only — desk marks already baked in v06 plate frame.
    placements = [
        (0.22, 0.28, "H", "1", max(36, w // 40), -18),
        (0.48, 0.22, "O", "16", max(34, w // 42), 14),
        (0.70, 0.34, "C", "12", max(34, w // 42), -10),
    ]
    for fx, fy, sym, num, sz, ang in placements:
        draw_mark(
            ImageDraw.Draw(overlay),
            (int(w * fx), int(h * fy)),
            sym,
            num,
            size=sz,
            angle=ang,
            canvas=overlay,
            fill=INK_SOFT if sz < 40 else INK,
        )
    out = Image.alpha_composite(im, overlay).convert("RGB")
    dest.parent.mkdir(parents=True, exist_ok=True)
    out.save(dest, quality=95)
    print(f"wrote {dest.name} {out.size}", flush=True)


def main() -> None:
    STILL.mkdir(parents=True, exist_ok=True)

    swirl_fail = STILL_V06 / "FAIL_ben_swirl_blank.jpg"
    if not swirl_fail.exists():
        swirl_fail = STILL / "FAIL_ben_swirl_blank.jpg"
    if swirl_fail.exists():
        compose_swirl_hco_only(swirl_fail, STILL / "03_FAIL_swirl_v07_midair_hco.jpg")

    # Prefer v06 plate frames that already KEEP desk marks + blank flyers.
    for name, out_name in (
        ("v06_plate03_t3_0.jpg", "03_desk_keep_plus_midair_t3.jpg"),
        ("v06_plate03_t4_0.jpg", "03_swirl_plus_midair_t4.jpg"),
        ("v06_plate03_t2_0.jpg", "03_desk_keep_plus_midair_t2.jpg"),
    ):
        src = STILL / name
        if src.exists():
            compose_desk_keep_plus_midair(src, STILL / out_name)

    desk_marked = STILL_V06 / "03_FAIL_desk_marked_i2v.jpg"
    if desk_marked.exists():
        # Desk KEEP still as I2V alt (prompt asks mid-air marks to appear in motion).
        dest = STILL / "03_FAIL_desk_marked_keep_v07.jpg"
        Image.open(desk_marked).convert("RGB").save(dest, quality=95)
        print(f"copied desk KEEP → {dest.name}", flush=True)

    print(f"OK v07 marked stills → {STILL}", flush=True)


if __name__ == "__main__":
    main()
