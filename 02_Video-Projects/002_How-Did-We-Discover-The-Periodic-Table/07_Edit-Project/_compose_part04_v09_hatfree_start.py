#!/usr/bin/env python3
"""Compose hat-free on-colour I2V start for Part 04 plate 06 (v09).

DNA sources (LOCKED — never v08 hat FAIL stills):
  - character sheet / Germs lock / P03 keep Explorer
  - indoor desk bed with glowing vacant seat

Output: refs/v09_start_frames/06_explorer_leaves_gap_start_v09.jpg
"""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw

PROJ = Path(__file__).resolve().parents[1]
DNA = PROJ / "04_Generated-Clips/part04/refs/v09_dna"
OUT_DIR = PROJ / "04_Generated-Clips/part04/refs/v09_start_frames"
OUT = OUT_DIR / "06_explorer_leaves_gap_start_v09.jpg"
META = OUT_DIR / "compose_meta.json"

GERMS = DNA / "germs_lock.jpg"
P03 = DNA / "p03_keep.jpg"
SHEET = DNA / "character_sheet.jpg"
DESK_GAP = PROJ / "04_Generated-Clips/part04/refs/v01_stills/desk_one_gap.jpg"
DESK_BED = OUT_DIR / "_desk_bed_t2.jpg"
FALLBACK_DESK = PROJ / "04_Generated-Clips/part04/refs/v01_stills/desk_dna_t4.jpg"


def glow_slot(draw: ImageDraw.ImageDraw, xy, wh) -> None:
    x, y = xy
    w, h = wh
    for i, a in ((18, 40), (10, 90), (0, 140)):
        draw.rounded_rectangle(
            (x - i, y - i, x + w + i, y + h + i),
            radius=10 + i // 2,
            outline=(255, 220, 120, a),
            width=3,
        )
    draw.rounded_rectangle(
        (x, y, x + w, y + h), radius=8, outline=(255, 230, 150, 220), width=3
    )


def crop_explorer_germs(src: Path) -> Image.Image:
    """Crop Germs lock Explorer (door peek) — bare head, fair skin, dark teal."""
    im = Image.open(src).convert("RGBA")
    W, H = im.size
    # Explorer occupies roughly right-centre doorway; crop torso+head.
    box = (int(W * 0.28), int(H * 0.08), int(W * 0.78), int(H * 0.98))
    return im.crop(box)


def crop_explorer_p03(src: Path) -> Image.Image:
    """Crop P03 keep Explorer (kneeling) — bare head, fair skin, dark teal."""
    im = Image.open(src).convert("RGBA")
    W, H = im.size
    # Label is top-right; Explorer is lower-centre. Crop out label.
    box = (int(W * 0.18), int(H * 0.22), int(W * 0.78), int(H * 0.98))
    return im.crop(box)


def crop_explorer_sheet(src: Path) -> Image.Image:
    """Crop full-body from character sheet (left figure)."""
    im = Image.open(src).convert("RGBA")
    W, H = im.size
    box = (int(W * 0.02), int(H * 0.02), int(W * 0.42), int(H * 0.98))
    return im.crop(box)


def place_toy(bed: Image.Image, fig: Image.Image, *, target_h_frac: float = 0.16) -> Image.Image:
    W, H = bed.size
    target_h = int(H * target_h_frac)
    scale = target_h / float(fig.height)
    nw, nh = max(1, int(fig.width * scale)), max(1, target_h)
    fig_s = fig.resize((nw, nh), Image.Resampling.LANCZOS)
    # Profile garnish left of glowing gap — not face-hero centre.
    x = int(W * 0.34) - nw // 2
    y = int(H * 0.62) - nh
    out = bed.copy()
    out.paste(fig_s, (x, y), fig_s if fig_s.mode == "RGBA" else None)
    return out


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for p in (GERMS, P03, SHEET):
        if not p.exists():
            raise SystemExit(f"STOP: missing DNA ref {p}")

    desk_src = DESK_GAP if DESK_GAP.exists() else (
        DESK_BED if DESK_BED.exists() else FALLBACK_DESK
    )
    if not desk_src.exists():
        raise SystemExit(f"STOP: missing desk bed {desk_src}")

    bed = Image.open(desk_src).convert("RGBA")
    W, H = bed.size
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    cw, ch = int(W * 0.07), int(H * 0.11)
    glow_slot(d, (int(W * 0.48), int(H * 0.52)), (cw, ch))
    bed = Image.alpha_composite(bed, overlay)

    # Prefer Germs lock (live film DNA), then P03, then sheet.
    fig = crop_explorer_germs(GERMS)
    fig_src = "germs_lock"
    # Soft-alpha edges: convert near-white sheet leftover if any — germs is full scene.
    out = place_toy(bed, fig, target_h_frac=0.17)
    # Also write alt with P03 crop for visual compare
    alt_p03 = place_toy(bed, crop_explorer_p03(P03), target_h_frac=0.15)
    alt_sheet = place_toy(bed, crop_explorer_sheet(SHEET), target_h_frac=0.16)
    alt_p03.convert("RGB").save(OUT_DIR / "06_alt_p03_compose.jpg", quality=92)
    alt_sheet.convert("RGB").save(OUT_DIR / "06_alt_sheet_compose.jpg", quality=92)

    rgb = out.convert("RGB")
    rgb.save(OUT, quality=94)
    meta = {
        "out": str(OUT),
        "desk_src": str(desk_src),
        "explorer_src": fig_src,
        "dna_refs": [str(GERMS), str(P03), str(SHEET)],
        "forbidden": "never use v08 hat FAIL stills as start frame",
        "locks": [
            "NO HAT — bare messy wavy chestnut-brown hair",
            "skin: light-medium warm tan / fair boy",
            "coat: house dark teal / blue-green trenchcoat",
            "toy-scale garnish profile/OTS — not face-hero",
        ],
    }
    META.write_text(json.dumps(meta, indent=2) + "\n")
    print(f"OK wrote {OUT}", flush=True)
    print(f"  desk={desk_src.name} explorer={fig_src}", flush=True)


if __name__ == "__main__":
    main()
