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
    """One solid warm desk lamp — no separate glow silhouette."""
    lw, lh = int(150 * scale), int(260 * scale)
    lamp = Image.new("RGBA", (lw, lh), (0, 0, 0, 0))
    d = ImageDraw.Draw(lamp)
    # base
    d.ellipse((int(lw * 0.24), int(lh * 0.84), int(lw * 0.76), int(lh * 0.96)), fill=(115, 80, 42, 255))
    d.ellipse((int(lw * 0.32), int(lh * 0.80), int(lw * 0.68), int(lh * 0.90)), fill=(135, 95, 50, 255))
    # stem
    d.rectangle((int(lw * 0.46), int(lh * 0.30), int(lw * 0.54), int(lh * 0.84)), fill=(145, 105, 55, 255))
    # shade (solid single)
    d.polygon(
        [
            (int(lw * 0.16), int(lh * 0.36)),
            (int(lw * 0.84), int(lh * 0.36)),
            (int(lw * 0.68), int(lh * 0.10)),
            (int(lw * 0.32), int(lh * 0.10)),
        ],
        fill=(175, 135, 70, 255),
        outline=(85, 60, 32, 255),
    )
    # warm underside only (inside shade, not a second lamp)
    d.ellipse(
        (int(lw * 0.34), int(lh * 0.28), int(lw * 0.66), int(lh * 0.40)),
        fill=(255, 235, 170, 200),
    )
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


def paint_bookshelf(canvas: Image.Image) -> None:
    """Procedural bookshelf — no KEEP banner bleed."""
    d = ImageDraw.Draw(canvas)
    x0, y0, x1, y1 = int(W * 0.66), 0, W, int(H * 0.42)
    d.rectangle((x0, y0, x1, y1), fill=(55, 38, 26, 255))
    rng_colors = [
        (92, 62, 38), (110, 75, 45), (78, 52, 32), (130, 90, 55),
        (70, 48, 30), (100, 68, 42), (120, 82, 50), (85, 58, 35),
    ]
    col_w = 18
    x = x0 + 10
    ci = 0
    while x < x1 - 12:
        bw = col_w + (ci % 5) - 2
        d.rectangle((x, y0 + 8, min(x1 - 8, x + bw), y1 - 8), fill=(*rng_colors[ci % len(rng_colors)], 255))
        # shelf lines
        for sy in (y0 + 70, y0 + 150, y0 + 230, y0 + 310):
            if sy < y1 - 10:
                d.line((x0 + 6, sy, x1 - 6, sy), fill=(40, 28, 18, 255), width=4)
        x += bw + 3
        ci += 1


def paint_publish_desk(*, holes: bool) -> Image.Image:
    """Full opaque procedural rebuild — zero KEEP composite ghosts / banners."""
    rgba = Image.new("RGBA", (W, H), (28, 22, 18, 255))
    d0 = ImageDraw.Draw(rgba)
    d0.rectangle((0, 0, W, int(H * 0.42)), fill=(42, 30, 22, 255))

    # left wood panelling
    d0.rectangle((0, 0, int(W * 0.34), int(H * 0.42)), fill=(48, 34, 24, 255))
    for i in range(0, int(H * 0.42), 28):
        d0.line((0, i, int(W * 0.34), i), fill=(58, 40, 28, 255), width=2)

    paint_bookshelf(rgba)
    paint_night_window(rgba)

    # solid warm desk surface (lower 65%) — fully opaque
    desk = Image.new("RGBA", (W, int(H * 0.68)), (78, 52, 32, 255))
    dd = ImageDraw.Draw(desk)
    for i in range(0, desk.size[1], 5):
        shade = 78 + (i % 16) - 5
        dd.rectangle((0, i, W, i + 4), fill=(shade, int(shade * 0.68), int(shade * 0.42), 255))
    dd.ellipse(
        (int(W * 0.10), int(desk.size[1] * 0.05), int(W * 0.68), int(desk.size[1] * 0.65)),
        fill=(160, 118, 62, 170),
    )
    desk = desk.filter(ImageFilter.GaussianBlur(0.8))
    rgba.alpha_composite(desk, (0, int(H * 0.34)))

    # soft Empty Chairs glow (behind props, low alpha)
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gx0, gy0, gx1, gy1 = int(W * 0.42), int(H * 0.24), int(W * 0.58), int(H * 0.40)
    for pad, a in ((16, 28), (6, 48), (0, 70)):
        gd.rounded_rectangle(
            (gx0 - pad, gy0 - pad, gx1 + pad, gy1 + pad),
            radius=12,
            fill=(255, 236, 190, a),
        )
    rgba = Image.alpha_composite(rgba, glow.filter(ImageFilter.GaussianBlur(2.5)))

    # ONE solid lamp
    paint_lamp(rgba, int(W * 0.13), int(H * 0.40), scale=1.10)

    paint_card_stack(rgba, int(W * 0.22), int(H * 0.72), n=6, scale=1.1)
    paint_card_stack(rgba, int(W * 0.86), int(H * 0.68), n=5, scale=1.0)

    if holes:
        paint_grid_sheet(rgba, int(W * 0.28), int(H * 0.52), int(W * 0.78), int(H * 0.92), holes=True)
    else:
        paint_grid_sheet(rgba, int(W * 0.30), int(H * 0.50), int(W * 0.72), int(H * 0.88), holes=False)

    paint_flask(rgba, int(W * 0.38), int(H * 0.42), liquid=(210, 90, 140), scale=0.95)
    paint_flask(rgba, int(W * 0.48), int(H * 0.40), liquid=(70, 150, 210), scale=1.0)
    paint_flask(rgba, int(W * 0.60), int(H * 0.41), liquid=(60, 180, 90), scale=1.08, sphere=holes)
    paint_flask(rgba, int(W * 0.72), int(H * 0.40), liquid=(150, 70, 200), scale=1.12, sphere=holes)

    paint_mortar(rgba, int(W * 0.52), int(H * 0.48), scale=0.95, color=(235, 230, 220))
    paint_mortar(rgba, int(W * 0.58), int(H * 0.50), scale=1.05, color=(170, 170, 165))
    paint_magnifier(rgba, int(W * 0.78), int(H * 0.58), scale=1.05)

    out = rgba.convert("RGB")
    return ImageEnhance.Sharpness(out).enhance(1.30)


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
