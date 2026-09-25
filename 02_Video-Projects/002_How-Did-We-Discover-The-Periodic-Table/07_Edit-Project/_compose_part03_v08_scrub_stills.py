#!/usr/bin/env python3
"""Compose I2V start frames for Part 03 v08 scrub (no toy blocks / no model-town).

08: plate-01 hall DNA + soft colour pulse aura along blank glowing mass-line (aisle).
10: plate-01 hall DNA + palm-sized FLAT postcard city-plan on existing desk only.
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

PROJ = Path(__file__).resolve().parents[1]
STILL = PROJ / "04_Generated-Clips/part03/refs/v08_stills"
HALL = STILL / "01_hall_dna_t40.jpg"
HALL_DESK = STILL / "01_hall_dna_deskish.jpg"
# Prefer aisle-forward desk crop if deskish is weak; fall back to hall.
ALT_HALL = STILL / "01_hall_dna_t65.jpg"


def _load(path: Path) -> Image.Image:
    if not path.exists():
        raise SystemExit(f"missing still {path}")
    return Image.open(path).convert("RGBA")


def compose_08_massline_pulses(src: Path, dest: Path) -> None:
    """Soft translucent colour pulses along a blank glowing aisle mass-line — NOT blocks."""
    base = _load(src)
    w, h = base.size
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)

    # Glowing blank mass-line down the aisle (center floor band).
    x0, x1 = int(w * 0.46), int(w * 0.54)
    y0, y1 = int(h * 0.42), int(h * 0.98)
    for i, alpha in enumerate((28, 48, 70, 48, 28)):
        pad = 10 - i * 2
        d.rectangle(
            (x0 - pad, y0, x1 + pad, y1),
            fill=(255, 236, 180, alpha),
        )

    # Soft colour pulse blobs along the line (aura only — no brick geometry).
    pulses = [
        (0.50, 0.52, (120, 210, 255), 90, 38),
        (0.50, 0.62, (180, 140, 255), 85, 34),
        (0.50, 0.72, (255, 210, 120), 80, 32),
        (0.50, 0.82, (140, 230, 200), 75, 30),
        (0.50, 0.90, (160, 180, 255), 70, 28),
    ]
    for cx_f, cy_f, rgb, a, r in pulses:
        cx, cy = int(w * cx_f), int(h * cy_f)
        for k, aa in ((1.0, a), (1.55, a // 2), (2.2, a // 4)):
            rr = int(r * k)
            d.ellipse((cx - rr, cy - rr // 2, cx + rr, cy + rr // 2), fill=(*rgb, aa))

    glow = overlay.filter(ImageFilter.GaussianBlur(radius=10))
    out = Image.alpha_composite(base, glow).convert("RGB")
    # Slight warmth to match hall DNA
    out = ImageEnhance.Color(out).enhance(1.05)
    dest.parent.mkdir(parents=True, exist_ok=True)
    out.save(dest, quality=95)
    print(f"wrote {dest} {dest.stat().st_size}", flush=True)


def compose_10_postcard_flat(src: Path, dest: Path) -> None:
    """Tiny flat postcard city-plan on existing desk — HARD REJECT model-town sprawl."""
    base = _load(src)
    w, h = base.size
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)

    # Postcard sits on a foreground desk surface (lower third, slightly left of center).
    pw, ph = int(w * 0.16), int(h * 0.11)
    px, py = int(w * 0.42), int(h * 0.72)
    # Soft wood-shadow under card
    d.rounded_rectangle(
        (px + 6, py + 8, px + pw + 10, py + ph + 12),
        radius=6,
        fill=(40, 24, 12, 70),
    )
    # Flat cream postcard board
    d.rounded_rectangle(
        (px, py, px + pw, py + ph),
        radius=5,
        fill=(232, 220, 198, 245),
        outline=(120, 92, 60, 220),
        width=2,
    )

    # Flat grid of blank house marks (2D cells) — not toy bricks.
    cols, rows = 7, 4
    margin = 8
    gw = pw - 2 * margin
    gh = ph - 2 * margin
    cw, ch = gw / cols, gh / rows
    vacant = {(1, 1), (4, 2), (5, 1), (2, 3)}  # a few glowing vacant lots
    for r in range(rows):
        for c in range(cols):
            x0 = px + margin + int(c * cw) + 1
            y0 = py + margin + int(r * ch) + 1
            x1 = px + margin + int((c + 1) * cw) - 1
            y1 = py + margin + int((r + 1) * ch) - 1
            if (c, r) in vacant:
                d.rectangle((x0, y0, x1, y1), fill=(255, 220, 140, 210))
                d.rectangle((x0 + 1, y0 + 1, x1 - 1, y1 - 1), fill=(255, 245, 200, 90))
            else:
                d.rectangle((x0, y0, x1, y1), fill=(210, 198, 175, 200))
                # Tiny blank house mark (flat chevron roof hint — 2D only)
                mx = (x0 + x1) // 2
                d.polygon(
                    [(mx, y0 + 2), (x0 + 2, y0 + ch * 0.35), (x1 - 2, y0 + ch * 0.35)],
                    fill=(170, 150, 125, 180),
                )
                d.rectangle(
                    (x0 + 3, y0 + int(ch * 0.32), x1 - 3, y1 - 2),
                    fill=(185, 168, 145, 180),
                )

    soft = overlay.filter(ImageFilter.GaussianBlur(radius=0.6))
    out = Image.alpha_composite(base, soft).convert("RGB")
    dest.parent.mkdir(parents=True, exist_ok=True)
    out.save(dest, quality=95)
    print(f"wrote {dest} {dest.stat().st_size}", flush=True)


def main() -> None:
    hall = HALL if HALL.exists() else ALT_HALL
    desk = HALL_DESK if HALL_DESK.exists() else hall
    compose_08_massline_pulses(hall, STILL / "08_massline_pulse_i2v.jpg")
    # Also keep a clean hall fallback (no props) for I2V attach retries.
    clean = _load(hall).convert("RGB")
    (STILL / "08_hall_dna_fallback.jpg").parent.mkdir(parents=True, exist_ok=True)
    clean.save(STILL / "08_hall_dna_fallback.jpg", quality=95)
    clean.save(STILL / "10_hall_dna_fallback.jpg", quality=95)
    print(f"wrote {STILL / '08_hall_dna_fallback.jpg'}", flush=True)
    compose_10_postcard_flat(desk, STILL / "10_postcard_flat_i2v.jpg")
    # Copy preferred alt: if deskish is too similar, also compose on hall t65.
    if ALT_HALL.exists() and ALT_HALL.resolve() != desk.resolve():
        compose_10_postcard_flat(ALT_HALL, STILL / "10_postcard_flat_alt.jpg")


if __name__ == "__main__":
    main()
