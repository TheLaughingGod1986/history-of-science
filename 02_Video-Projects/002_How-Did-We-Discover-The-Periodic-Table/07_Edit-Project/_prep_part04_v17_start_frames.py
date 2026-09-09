#!/usr/bin/env python3
"""Prep Part 04 v17 I2V start frames — PUBLISH THE GAPS sharp (no v01 ghost DNA).

Parent KEEP: hos_002_part04_rough_v16.mp4
  sha256 7e083fc440879209bbc69459fbaf21dc29dbfc1f77b370ec92ee931bec82cb3c

Remint ONLY: 11_publish_gaps · 11b_wait_and_hunt
KEEP: 10_family_before_weight · Explorer 06 · CLEAN LIGHT 09/09b · written cards ~40

Critical: do NOT restore pre-deghost v01 DNA (v16 UAT still failed on ghosts).
Paint fresh single-exposure desk from KEEP room DNA + opaque props.
"""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

PROJ = Path(__file__).resolve().parents[1]
OUT = PROJ / "04_Generated-Clips/part04/refs/v17_start_frames"
QA = PROJ / "07_Edit-Project/_qa_part04_v17_prep"
META = OUT / "compose_meta.json"
ASSETS = Path.home() / ".cursor/projects/Users-benjaminoats-YouTube-History-Of-Science/assets"

KEEP_T105 = ASSETS / "keep_t105_lamp.jpg"
KEEP_T110 = ASSETS / "keep_t110_family.jpg"
CUT_T110 = PROJ / "07_Edit-Project/_qa_part04_v16_cut/cut_t110.jpg"
W, H = 1920, 1080
PARENT_V16_SHA = "7e083fc440879209bbc69459fbaf21dc29dbfc1f77b370ec92ee931bec82cb3c"


def _font(size: int):
    for path in (
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Supplemental/Georgia Bold.ttf",
        "/Library/Fonts/Arial Bold.ttf",
    ):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def load_keep_room() -> Image.Image:
    for cand in (KEEP_T105, KEEP_T110, CUT_T110):
        if cand.exists() and cand.stat().st_size > 20_000:
            return Image.open(cand).convert("RGB").resize((W, H), Image.Resampling.LANCZOS)
    raise SystemExit("missing KEEP room DNA (keep_t105 / keep_t110)")


def paint_flask(
    canvas: Image.Image,
    cx: int,
    cy: int,
    *,
    liquid: tuple[int, int, int],
    scale: float = 1.0,
    sphere: bool = False,
) -> None:
    """Single solid flask — no ghost layers."""
    fw, fh = int(110 * scale), int(150 * scale)
    flask = Image.new("RGBA", (fw, fh), (0, 0, 0, 0))
    d = ImageDraw.Draw(flask)
    # body
    d.ellipse((8, int(fh * 0.28), fw - 9, fh - 8), fill=(220, 235, 245, 90), outline=(70, 90, 110, 220), width=3)
    # liquid
    ly0 = int(fh * 0.48)
    d.ellipse((14, ly0, fw - 15, fh - 14), fill=(*liquid, 210))
    if sphere:
        for i, (ox, oy) in enumerate(((0.35, 0.62), (0.55, 0.70), (0.42, 0.78))):
            r = max(6, int(10 * scale) - i)
            sx, sy = int(fw * ox), int(fh * oy)
            d.ellipse((sx - r, sy - r, sx + r, sy + r), fill=(*liquid, 255), outline=(40, 40, 50, 180), width=2)
    # neck
    nx0, nx1 = int(fw * 0.38), int(fw * 0.62)
    d.rectangle((nx0, 6, nx1, int(fh * 0.36)), fill=(210, 225, 235, 80), outline=(70, 90, 110, 220), width=2)
    d.ellipse((nx0 - 2, 2, nx1 + 2, 16), fill=(230, 235, 240, 120), outline=(70, 90, 110, 220), width=2)
    canvas.alpha_composite(flask, (cx - fw // 2, cy - fh // 2))


def paint_lamp(canvas: Image.Image, cx: int, cy: int, *, scale: float = 1.0) -> None:
    """One solid warm desk lamp."""
    lw, lh = int(160 * scale), int(280 * scale)
    lamp = Image.new("RGBA", (lw, lh), (0, 0, 0, 0))
    d = ImageDraw.Draw(lamp)
    # base
    d.ellipse((int(lw * 0.22), int(lh * 0.82), int(lw * 0.78), int(lh * 0.96)), fill=(120, 85, 45, 255))
    d.ellipse((int(lw * 0.30), int(lh * 0.78), int(lw * 0.70), int(lh * 0.88)), fill=(140, 100, 55, 255))
    # stem
    d.rectangle((int(lw * 0.46), int(lh * 0.28), int(lw * 0.54), int(lh * 0.82)), fill=(150, 110, 60, 255))
    # shade
    d.polygon(
        [
            (int(lw * 0.18), int(lh * 0.34)),
            (int(lw * 0.82), int(lh * 0.34)),
            (int(lw * 0.70), int(lh * 0.12)),
            (int(lw * 0.30), int(lh * 0.12)),
        ],
        fill=(185, 145, 75, 255),
        outline=(90, 65, 35, 255),
    )
    # warm bulb glow (soft, not lava)
    glow = Image.new("RGBA", (lw, lh), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse((int(lw * 0.28), int(lh * 0.28), int(lw * 0.72), int(lh * 0.55)), fill=(255, 230, 160, 90))
    glow = glow.filter(ImageFilter.GaussianBlur(6))
    lamp = Image.alpha_composite(lamp, glow)
    canvas.alpha_composite(lamp, (cx - lw // 2, cy - lh // 2))


def paint_magnifier(canvas: Image.Image, cx: int, cy: int, *, scale: float = 1.0) -> None:
    mw, mh = int(220 * scale), int(90 * scale)
    mag = Image.new("RGBA", (mw, mh), (0, 0, 0, 0))
    d = ImageDraw.Draw(mag)
    r = int(38 * scale)
    d.ellipse((8, mh // 2 - r, 8 + 2 * r, mh // 2 + r), outline=(150, 115, 55, 255), width=6)
    d.ellipse((12, mh // 2 - r + 4, 4 + 2 * r, mh // 2 + r - 4), fill=(200, 230, 240, 40))
    d.line((8 + 2 * r - 4, mh // 2 + 4, mw - 10, mh // 2 + 18), fill=(90, 60, 35, 255), width=10)
    canvas.alpha_composite(mag, (cx - mw // 2, cy - mh // 2))


def paint_mortar(canvas: Image.Image, cx: int, cy: int, *, scale: float = 1.0, color=(235, 230, 220)) -> None:
    mw, mh = int(90 * scale), int(70 * scale)
    m = Image.new("RGBA", (mw, mh), (0, 0, 0, 0))
    d = ImageDraw.Draw(m)
    d.ellipse((4, int(mh * 0.25), mw - 5, mh - 4), fill=(*color, 255), outline=(90, 80, 70, 220), width=3)
    d.ellipse((int(mw * 0.18), int(mh * 0.08), int(mw * 0.82), int(mh * 0.45)), fill=(*color, 255), outline=(90, 80, 70, 200), width=2)
    # pestle
    d.line((int(mw * 0.55), 4, int(mw * 0.78), int(mh * 0.55)), fill=(200, 195, 185, 255), width=8)
    canvas.alpha_composite(m, (cx - mw // 2, cy - mh // 2))


def paint_card_stack(canvas: Image.Image, cx: int, cy: int, *, n: int = 5, scale: float = 1.0) -> None:
    cw, ch = int(70 * scale), int(90 * scale)
    for i in range(n):
        card = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
        d = ImageDraw.Draw(card)
        d.rounded_rectangle((1, 1, cw - 2, ch - 2), radius=6, fill=(248, 242, 228, 255), outline=(55, 45, 35, 220), width=2)
        canvas.alpha_composite(card, (cx - cw // 2 + i * 2, cy - ch // 2 - i * 2))


def paint_grid_sheet(
    canvas: Image.Image,
    x0: int,
    y0: int,
    x1: int,
    y1: int,
    *,
    holes: bool = False,
) -> None:
    """One solid parchment grid — single ink lines only."""
    sheet = Image.new("RGBA", (x1 - x0, y1 - y0), (0, 0, 0, 0))
    d = ImageDraw.Draw(sheet)
    w, h = sheet.size
    d.rounded_rectangle((2, 2, w - 3, h - 3), radius=8, fill=(245, 236, 215, 255), outline=(60, 50, 40, 230), width=3)
    cols, rows = 6, 4
    pad = 18
    cell_w = (w - 2 * pad) / cols
    cell_h = (h - 2 * pad) / rows
    ink = (35, 30, 28, 255)
    for c in range(cols + 1):
        x = int(pad + c * cell_w)
        d.line((x, pad, x, h - pad), fill=ink, width=3)
    for r in range(rows + 1):
        y = int(pad + r * cell_h)
        d.line((pad, y, w - pad, y), fill=ink, width=3)
    # empty seats / gaps
    gap_cells = {(1, 1), (2, 2), (4, 1), (3, 3), (5, 2)} if holes else {(1, 1), (3, 2), (4, 1)}
    for (cc, rr) in gap_cells:
        cx = int(pad + (cc + 0.5) * cell_w)
        cy = int(pad + (rr + 0.5) * cell_h)
        rad = int(min(cell_w, cell_h) * 0.28)
        if holes:
            d.ellipse((cx - rad, cy - rad, cx + rad, cy + rad), fill=(120, 85, 50, 255), outline=ink, width=2)
        else:
            d.ellipse((cx - rad, cy - rad, cx + rad, cy + rad), outline=ink, width=3)
    canvas.alpha_composite(sheet, (x0, y0))


def soft_empty_chairs_glow(canvas: Image.Image) -> Image.Image:
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    x0, y0, x1, y1 = int(W * 0.40), int(H * 0.22), int(W * 0.60), int(H * 0.42)
    for pad, a in ((22, 35), (10, 60), (0, 88)):
        d.rounded_rectangle(
            (x0 - pad, y0 - pad, x1 + pad, y1 + pad),
            radius=14,
            fill=(255, 236, 190, a),
        )
    return Image.alpha_composite(canvas, ov.filter(ImageFilter.GaussianBlur(2.0)))


def paint_night_window(canvas: Image.Image) -> None:
    """Simple night window + moon (upper band) — single exposure."""
    d = ImageDraw.Draw(canvas)
    # window frame
    wx0, wy0, wx1, wy1 = int(W * 0.34), int(H * 0.02), int(W * 0.66), int(H * 0.36)
    d.rectangle((wx0, wy0, wx1, wy1), fill=(25, 40, 70, 255), outline=(70, 50, 35, 255), width=8)
    # panes
    mx = (wx0 + wx1) // 2
    my = (wy0 + wy1) // 2
    d.line((mx, wy0, mx, wy1), fill=(70, 50, 35, 255), width=6)
    d.line((wx0, my, wx1, my), fill=(70, 50, 35, 255), width=6)
    # moon
    moon_r = 48
    mcx, mcy = int(W * 0.55), int(H * 0.14)
    d.ellipse((mcx - moon_r, mcy - moon_r, mcx + moon_r, mcy + moon_r), fill=(240, 235, 210, 255))


def paint_publish_desk(*, holes: bool) -> Image.Image:
    """Full opaque rebuild — KEEP upper room DNA + solid desk props. Zero ghost layers."""
    keep = load_keep_room()
    rgba = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    # keep upper shelves / lamp area from KEEP (already sharp)
    top = keep.crop((0, 0, W, int(H * 0.38))).convert("RGBA")
    rgba.paste(top, (0, 0))
    # night window override for publish beat (moon / night)
    paint_night_window(rgba)

    # solid warm desk surface (lower 65%)
    desk = Image.new("RGBA", (W, int(H * 0.68)), (78, 52, 32, 255))
    dd = ImageDraw.Draw(desk)
    for i in range(0, desk.size[1], 5):
        shade = 78 + (i % 16) - 5
        dd.rectangle((0, i, W, i + 4), fill=(shade, int(shade * 0.68), int(shade * 0.42), 255))
    # warm lamp pool
    dd.ellipse(
        (int(W * 0.08), int(desk.size[1] * 0.02), int(W * 0.72), int(desk.size[1] * 0.70)),
        fill=(165, 120, 65, 190),
    )
    desk = desk.filter(ImageFilter.GaussianBlur(1.0))
    rgba.alpha_composite(desk, (0, int(H * 0.34)))

    rgba = soft_empty_chairs_glow(rgba)

    # ONE solid lamp
    paint_lamp(rgba, int(W * 0.14), int(H * 0.42), scale=1.15)

    # card stacks
    paint_card_stack(rgba, int(W * 0.22), int(H * 0.72), n=6, scale=1.1)
    paint_card_stack(rgba, int(W * 0.86), int(H * 0.68), n=5, scale=1.0)

    # ONE solid grid
    if holes:
        paint_grid_sheet(rgba, int(W * 0.28), int(H * 0.52), int(W * 0.78), int(H * 0.92), holes=True)
    else:
        paint_grid_sheet(rgba, int(W * 0.30), int(H * 0.50), int(W * 0.72), int(H * 0.88), holes=False)

    # flasks — single solids
    paint_flask(rgba, int(W * 0.38), int(H * 0.42), liquid=(210, 90, 140), scale=0.95)
    paint_flask(rgba, int(W * 0.48), int(H * 0.40), liquid=(70, 150, 210), scale=1.0)
    paint_flask(rgba, int(W * 0.60), int(H * 0.41), liquid=(60, 180, 90), scale=1.08, sphere=holes)
    paint_flask(rgba, int(W * 0.72), int(H * 0.40), liquid=(150, 70, 200), scale=1.12, sphere=holes)

    paint_mortar(rgba, int(W * 0.52), int(H * 0.48), scale=0.95, color=(235, 230, 220))
    paint_mortar(rgba, int(W * 0.58), int(H * 0.50), scale=1.05, color=(170, 170, 165))
    paint_magnifier(rgba, int(W * 0.78), int(H * 0.58), scale=1.05)

    out = rgba.convert("RGB")
    return ImageEnhance.Sharpness(out).enhance(1.35)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QA.mkdir(parents=True, exist_ok=True)
    meta: dict = {
        "parent_v16_sha": PARENT_V16_SHA,
        "bible_main": "25bdefd",
        "plates": {},
        "method": (
            "painted_sharp_publish_from_KEEP_room_DNA — NOT v01 restore, "
            "NOT temporal-median deghost"
        ),
        "note": "v16 restored v01 for 11/11b and UAT still failed ghosts; fresh paint only",
    }

    im11 = paint_publish_desk(holes=False)
    out11 = OUT / "11_publish_gaps_start_v17.jpg"
    im11.save(out11, quality=95)
    im11.save(QA / "start_11_publish_sharp_v17.jpg", quality=92)
    meta["plates"]["11_publish_gaps"] = str(out11)

    im11b = paint_publish_desk(holes=True)
    # slight camera push / alternate prop placement for 11b
    out11b = OUT / "11b_wait_and_hunt_start_v17.jpg"
    im11b.save(out11b, quality=95)
    im11b.save(QA / "start_11b_hunt_sharp_v17.jpg", quality=92)
    meta["plates"]["11b_wait_and_hunt"] = str(out11b)

    # stash KEEP refs (do not remint 10 / 09b)
    for src, name in ((KEEP_T110, "keep_t110_family_ref.jpg"), (KEEP_T105, "keep_t105_lamp_ref.jpg")):
        if src.exists():
            Image.open(src).convert("RGB").resize((W, H), Image.Resampling.LANCZOS).save(
                OUT / name, quality=92
            )

    META.write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta, indent=2), flush=True)
    print("PREP OK", flush=True)


if __name__ == "__main__":
    main()
