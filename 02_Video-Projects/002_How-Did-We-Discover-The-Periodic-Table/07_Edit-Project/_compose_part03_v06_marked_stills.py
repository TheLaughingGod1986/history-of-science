#!/usr/bin/env python3
"""Compose sparse phone-readable atomic-weight marks onto Part 03 v06 I2V starts.

Props ONLY: H 1 · O 16 · C 12 · N 14 · S 32 — dark ink on cream.
Most sheets stay blank. Prefer Ben FAIL stills (exact hall DNA).
Strip review UI chrome (top-right brown ATOMIC WEIGHTS pill) so Flow does not bake it.
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter

STILL = Path(__file__).resolve().parents[1] / "04_Generated-Clips/part03/refs/v06_stills"
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
    """Draw mark; if angle!=0 and canvas given, paste a rotated text layer."""
    text = f"{symbol} {number}"
    f = font(size)
    if abs(angle) < 0.5 or canvas is None:
        x, y = xy
        draw.text((x + 2, y + 2), text, font=f, fill=(0, 0, 0, 100))
        draw.text((x, y), text, font=f, fill=fill)
        return
    # Rotated glyph for mid-air papers
    tmp = Image.new("RGBA", (size * 6, size * 3), (0, 0, 0, 0))
    td = ImageDraw.Draw(tmp)
    td.text((4, 4), text, font=f, fill=(0, 0, 0, 90))
    td.text((2, 2), text, font=f, fill=fill)
    rot = tmp.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
    # Crop transparent margins
    bbox = rot.getbbox()
    if bbox:
        rot = rot.crop(bbox)
    x, y = xy
    canvas.alpha_composite(rot, dest=(max(0, x), max(0, y)))


def strip_top_right_chrome(im: Image.Image) -> Image.Image:
    """Cover review pill / brown blob top-right with sampled hall wood."""
    out = im.convert("RGB").copy()
    w, h = out.size
    # Sample warm wood mid-wall (away from windows / pill).
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
    """Center-crop ultra-wide review captures to 16:9, then downscale for Flow."""
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


def to_flow_still(im: Image.Image, dest: Path, *, max_w: int = 1920) -> None:
    im = crop_16x9(im, max_w=max_w)
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.save(dest, quality=95)
    print(f"wrote {dest.name} {im.size}", flush=True)


def compose_ben_fail_desk(src: Path, dest: Path) -> None:
    """Upright hero + 1–2 stack marks on Ben's blank desk FAIL.

    Crop to 16:9 FIRST so mark coords match the Flow start frame.
    """
    raw = crop_16x9(strip_top_right_chrome(Image.open(src)))
    im = raw.convert("RGBA")
    w, h = im.size
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)

    # After 16:9 crop of FAIL_ben_desk_blank: upright cream hero ~center,
    # tidy stack immediately right. Marks ON paper faces only.
    hx = int(w * 0.455)
    draw_mark(d, (hx, int(h * 0.36)), "H", "1", size=max(70, w // 24))
    draw_mark(d, (hx, int(h * 0.48)), "O", "16", size=max(64, w // 26))
    draw_mark(d, (hx, int(h * 0.60)), "C", "12", size=max(60, w // 28))
    # Top of stack — one soft mark only (most of stack blank)
    draw_mark(
        d,
        (int(w * 0.585), int(h * 0.40)),
        "N",
        "14",
        size=max(34, w // 44),
        fill=INK_SOFT,
    )

    out = Image.alpha_composite(im, overlay).convert("RGB")
    dest.parent.mkdir(parents=True, exist_ok=True)
    out.save(dest, quality=95)
    print(f"wrote {dest.name} {out.size}", flush=True)


def compose_ben_fail_swirl(src: Path, dest: Path) -> None:
    """≈3–6 marked sheets in Ben's blank aisle swirl FAIL; most stay blank."""
    raw = crop_16x9(strip_top_right_chrome(Image.open(src)))
    im = raw.convert("RGBA")
    w, h = im.size
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))

    # Mid-aisle paper faces (swirl is lower/center, not on the far windows).
    # (fx, fy, sym, num, size, angle)
    placements = [
        (0.36, 0.48, "H", "1", max(38, w // 36), -16),
        (0.52, 0.40, "O", "16", max(36, w // 38), 12),
        (0.62, 0.52, "C", "12", max(34, w // 40), -8),
        (0.44, 0.60, "N", "14", max(32, w // 42), 18),
        (0.56, 0.66, "S", "32", max(32, w // 42), -12),
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


def compose_desk_hero(src: Path, dest: Path) -> None:
    """Legacy v02 desk settle stills."""
    im = Image.open(src).convert("RGBA")
    w, h = im.size
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    draw_mark(d, (int(w * 0.34), int(h * 0.38)), "H", "1", size=max(54, w // 18))
    draw_mark(d, (int(w * 0.34), int(h * 0.52)), "O", "16", size=max(48, w // 20))
    draw_mark(d, (int(w * 0.58), int(h * 0.48)), "C", "12", size=max(36, w // 28), fill=INK_SOFT)
    draw_mark(d, (int(w * 0.62), int(h * 0.58)), "N", "14", size=max(32, w // 30), fill=INK_SOFT)
    out = Image.alpha_composite(im, overlay).convert("RGB")
    dest.parent.mkdir(parents=True, exist_ok=True)
    out.save(dest, quality=95)
    print(f"desk_hero {dest.name} {out.size}", flush=True)


def compose_swirl(src: Path, dest: Path) -> None:
    im = Image.open(src).convert("RGBA")
    w, h = im.size
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    placements = [
        (0.28, 0.42, "H", "1", max(40, w // 24), -16),
        (0.48, 0.36, "O", "16", max(38, w // 26), 10),
        (0.62, 0.48, "C", "12", max(36, w // 28), -6),
        (0.38, 0.62, "N", "14", max(34, w // 30), 18),
        (0.55, 0.58, "S", "32", max(34, w // 30), -12),
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
    print(f"swirl {dest.name} {out.size}", flush=True)


def compose_desk_from_assembled(src: Path, dest: Path) -> None:
    im = Image.open(src).convert("RGBA")
    w, h = im.size
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    draw_mark(d, (int(w * 0.42), int(h * 0.55)), "H", "1", size=max(72, w // 20))
    draw_mark(d, (int(w * 0.42), int(h * 0.66)), "O", "16", size=max(64, w // 22))
    draw_mark(d, (int(w * 0.58), int(h * 0.52)), "C", "12", size=max(48, w // 28), fill=INK_SOFT)
    draw_mark(d, (int(w * 0.62), int(h * 0.62)), "S", "32", size=max(44, w // 30), fill=INK_SOFT)
    out = Image.alpha_composite(im, overlay).convert("RGB")
    dest.parent.mkdir(parents=True, exist_ok=True)
    out.save(dest, quality=95)
    print(f"assembled_desk {dest.name} {out.size}", flush=True)


def main() -> None:
    desk_fail = STILL / "FAIL_ben_desk_blank.jpg"
    swirl_fail = STILL / "FAIL_ben_swirl_blank.jpg"
    if not desk_fail.exists():
        desk_fail = STILL / "FAIL_ben_desk_blank.png"
    if not swirl_fail.exists():
        swirl_fail = STILL / "FAIL_ben_swirl_blank.png"

    if desk_fail.exists():
        compose_ben_fail_desk(desk_fail, STILL / "03_FAIL_desk_marked_i2v.jpg")
    if swirl_fail.exists():
        compose_ben_fail_swirl(swirl_fail, STILL / "03_FAIL_swirl_marked_i2v.jpg")

    desk_src = STILL / "03_pamphlet_v02_t65.jpg"
    desk_mid = STILL / "03_pamphlet_v02_t40.jpg"
    swirl_src = STILL / "04_zoo_v02_t20.jpg"
    assembled = STILL / "v05_atomic_weights_t17.jpg"

    if desk_src.exists():
        compose_desk_hero(desk_src, STILL / "03_desk_hero_marked_i2v.jpg")
    if desk_mid.exists():
        compose_desk_hero(desk_mid, STILL / "03_desk_mid_marked_i2v.jpg")
    if swirl_src.exists():
        compose_swirl(swirl_src, STILL / "03_swirl_marked_i2v.jpg")
    if assembled.exists():
        compose_desk_from_assembled(assembled, STILL / "03_assembled_desk_marked_i2v.jpg")
    print(f"OK marked stills → {STILL}", flush=True)


if __name__ == "__main__":
    main()
