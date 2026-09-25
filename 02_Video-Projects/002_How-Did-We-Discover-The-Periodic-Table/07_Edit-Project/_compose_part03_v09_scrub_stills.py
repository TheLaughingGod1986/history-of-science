#!/usr/bin/env python3
"""Compose I2V start frames for Part 03 v09 city-plan scrub.

Ben FAIL v08 ~68s: glowing yellow house-blocks + black house icons/pins on board.
v09: flat postcard = grid INK only (no 3D, no house shapes) OR papers-only stack.
Reuse hall DNA stills from v08 refs.
"""
from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

PROJ = Path(__file__).resolve().parents[1]
STILL_V08 = PROJ / "04_Generated-Clips/part03/refs/v08_stills"
STILL = PROJ / "04_Generated-Clips/part03/refs/v09_stills"
HALL = STILL_V08 / "01_hall_dna_t40.jpg"
HALL_DESK = STILL_V08 / "01_hall_dna_deskish.jpg"
ALT_HALL = STILL_V08 / "01_hall_dna_t65.jpg"


def _load(path: Path) -> Image.Image:
    if not path.exists():
        raise SystemExit(f"missing still {path}")
    return Image.open(path).convert("RGBA")


def compose_10_flat_ink_grid(src: Path, dest: Path) -> None:
    """Palm-sized flat postcard: street grid as INK lines only + flat vacant washes.

    HARD REJECT in the still itself: no house polygons, no pins, no 3D blocks.
    """
    base = _load(src)
    w, h = base.size
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)

    pw, ph = int(w * 0.18), int(h * 0.12)
    px, py = int(w * 0.40), int(h * 0.70)
    # Soft wood-shadow under card
    d.rounded_rectangle(
        (px + 5, py + 7, px + pw + 9, py + ph + 11),
        radius=5,
        fill=(40, 24, 12, 65),
    )
    # Flat cream postcard board
    d.rounded_rectangle(
        (px, py, px + pw, py + ph),
        radius=4,
        fill=(236, 228, 210, 248),
        outline=(95, 72, 48, 230),
        width=2,
    )

    # Flat ink street grid ONLY — no house shapes.
    cols, rows = 8, 5
    margin = 10
    gw = pw - 2 * margin
    gh = ph - 2 * margin
    ink = (55, 48, 40, 210)
    # Vacant lots = flat paint washes (never buildings)
    vacant = {(1, 1), (4, 2), (6, 1), (2, 3), (5, 3)}
    for r in range(rows):
        for c in range(cols):
            x0 = px + margin + int(c * gw / cols)
            y0 = py + margin + int(r * gh / rows)
            x1 = px + margin + int((c + 1) * gw / cols)
            y1 = py + margin + int((r + 1) * gh / rows)
            if (c, r) in vacant:
                # Soft flat wash — reads as empty lot ink, not a glowing house block
                d.rectangle((x0 + 1, y0 + 1, x1 - 1, y1 - 1), fill=(210, 190, 150, 120))
            # Cell border as thin ink
            d.rectangle((x0, y0, x1, y1), outline=ink, width=1)

    # A few thicker street lines across the plan (still flat ink)
    for frac in (0.33, 0.66):
        yy = py + margin + int(gh * frac)
        d.line((px + margin, yy, px + pw - margin, yy), fill=ink, width=2)
    for frac in (0.25, 0.50, 0.75):
        xx = px + margin + int(gw * frac)
        d.line((xx, py + margin, xx, py + ph - margin), fill=ink, width=2)

    # Optional tidy paper stack to the right (papers OK; no second town)
    sx, sy = px + pw + int(w * 0.02), py + int(ph * 0.15)
    sw, sh = int(w * 0.07), int(h * 0.09)
    d.rectangle((sx + 3, sy + 4, sx + sw + 3, sy + sh + 4), fill=(40, 24, 12, 50))
    d.rectangle((sx, sy, sx + sw, sy + sh), fill=(242, 236, 222, 245), outline=(150, 130, 100, 200))

    soft = overlay.filter(ImageFilter.GaussianBlur(radius=0.4))
    out = Image.alpha_composite(base, soft).convert("RGB")
    dest.parent.mkdir(parents=True, exist_ok=True)
    out.save(dest, quality=95)
    print(f"wrote {dest} {dest.stat().st_size}", flush=True)


def compose_10_papers_only(src: Path, dest: Path) -> None:
    """Papers-only desk prop — no city-plan board at all (sheet option 2)."""
    base = _load(src)
    w, h = base.size
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)

    # Neat cream pamphlet stack on foreground desk
    sx, sy = int(w * 0.42), int(h * 0.72)
    sw, sh = int(w * 0.14), int(h * 0.10)
    d.rectangle((sx + 6, sy + 8, sx + sw + 8, sy + sh + 10), fill=(40, 24, 12, 60))
    for i, lift in enumerate((0, 2, 4, 6)):
        d.rectangle(
            (sx - lift // 2, sy - lift, sx + sw + lift // 2, sy + sh - lift // 2),
            fill=(240 - i * 3, 232 - i * 2, 216 - i, 245),
            outline=(140, 118, 90, 200),
        )
    soft = overlay.filter(ImageFilter.GaussianBlur(radius=0.5))
    out = Image.alpha_composite(base, soft).convert("RGB")
    dest.parent.mkdir(parents=True, exist_ok=True)
    out.save(dest, quality=95)
    print(f"wrote {dest} {dest.stat().st_size}", flush=True)


def main() -> None:
    hall = HALL if HALL.exists() else ALT_HALL
    desk = HALL_DESK if HALL_DESK.exists() else hall
    STILL.mkdir(parents=True, exist_ok=True)

    compose_10_flat_ink_grid(desk, STILL / "10_flat_ink_grid_i2v.jpg")
    if ALT_HALL.exists() and ALT_HALL.resolve() != desk.resolve():
        compose_10_flat_ink_grid(ALT_HALL, STILL / "10_flat_ink_grid_alt.jpg")
    compose_10_papers_only(desk, STILL / "10_papers_only_i2v.jpg")
    if ALT_HALL.exists():
        compose_10_papers_only(ALT_HALL, STILL / "10_papers_only_alt.jpg")

    # Clean hall fallback (no props) for attach retries
    clean = _load(hall).convert("RGB")
    clean.save(STILL / "10_hall_dna_fallback.jpg", quality=95)
    print(f"wrote {STILL / '10_hall_dna_fallback.jpg'}", flush=True)

    # Archive Ben FAIL stills already copied under ben_fail/
    fail_dir = STILL / "ben_fail"
    if fail_dir.exists():
        for p in sorted(fail_dir.glob("*.jpg")):
            print(f"FAIL ref kept {p.name} {p.stat().st_size}", flush=True)


if __name__ == "__main__":
    main()
