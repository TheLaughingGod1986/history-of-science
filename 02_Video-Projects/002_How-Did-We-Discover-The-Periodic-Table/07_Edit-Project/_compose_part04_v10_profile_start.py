#!/usr/bin/env python3
"""Compose Part 04 plate 06 I2V start for v10 — PROFILE / back garnish only.

UAT FAIL v09: Explorer flipped to face-on / ¾ hero mid-clip (~51–52s).
v10 start MUST be profile or back — never face-on stills (fail_faceon_51/52).

Sources (priority):
  1. Clean profile still from v09 plate (~t4 lean) — no side label
  2. ok_profile_49.jpg with EMPTY SEATS label scrubbed
  3. P03 keep garnish crop (profile/back language)

Forbidden starts: fail_faceon_*, character-sheet front hero, Germs face peek.
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

PROJ = Path(__file__).resolve().parents[1]
DNA = PROJ / "04_Generated-Clips/part04/refs/v10_dna"
OUT_DIR = PROJ / "04_Generated-Clips/part04/refs/v10_start_frames"
OUT = OUT_DIR / "06_explorer_leaves_gap_start_v10.jpg"
META = OUT_DIR / "compose_meta.json"

REF_PROFILE_T4 = OUT_DIR / "_ref_profile_from_v09_t4.jpg"
OK_PROFILE_49 = DNA / "ok_profile_49.jpg"
P03 = DNA / "p03_keep.jpg"
FAIL_51 = DNA / "fail_faceon_51.jpg"
FAIL_52 = DNA / "fail_faceon_52.jpg"


def scrub_side_label(im: Image.Image) -> Image.Image:
    """Cover top-right EMPTY SEATS / EKA plaque with nearby bookshelf pixels."""
    rgb = im.convert("RGB")
    W, H = rgb.size
    # Plaque sits ~top-right; clone from bookshelf above-left of plaque.
    x0, y0 = int(W * 0.72), int(H * 0.02)
    x1, y1 = int(W * 0.99), int(H * 0.14)
    src = rgb.crop((int(W * 0.55), int(H * 0.02), int(W * 0.70), int(H * 0.14)))
    src = src.resize((x1 - x0, y1 - y0), Image.Resampling.LANCZOS)
    out = rgb.copy()
    out.paste(src, (x0, y0))
    # Soft edge
    mask = Image.new("L", (x1 - x0, y1 - y0), 0)
    d = ImageDraw.Draw(mask)
    d.rounded_rectangle((0, 0, x1 - x0 - 1, y1 - y0 - 1), radius=12, fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(4))
    blended = Image.composite(src, out.crop((x0, y0, x1, y1)), mask)
    out.paste(blended, (x0, y0))
    return out


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for banned in (FAIL_51, FAIL_52):
        if banned.exists():
            print(f"  note: refuse face-on still as start ({banned.name})", flush=True)

    src_name = None
    if REF_PROFILE_T4.exists() and REF_PROFILE_T4.stat().st_size > 20_000:
        # Clean plate-internal profile lean — preferred (no plaque).
        shutil.copy2(REF_PROFILE_T4, OUT)
        src_name = "v09_plate_t4_profile_lean"
        print(f"OK start from clean profile still → {OUT.name}", flush=True)
    elif OK_PROFILE_49.exists():
        scrubbed = scrub_side_label(Image.open(OK_PROFILE_49))
        scrubbed.save(OUT, quality=94)
        src_name = "ok_profile_49_label_scrubbed"
        print(f"OK start from ok_profile_49 (label scrubbed) → {OUT.name}", flush=True)
    elif P03.exists():
        # Last resort: P03 keep as composition reference (house garnish pose).
        Image.open(P03).convert("RGB").save(OUT, quality=92)
        src_name = "p03_keep_fallback"
        print(f"OK start from P03 keep fallback → {OUT.name}", flush=True)
    else:
        raise SystemExit("STOP: no profile/back start source available")

    meta = {
        "out": str(OUT),
        "source": src_name,
        "pose_lock": "profile_or_back_only",
        "forbidden_starts": ["fail_faceon_51", "fail_faceon_52", "sheet_front_hero"],
        "colour_dna_keep": [
            "bare_head_no_hat",
            "fair_warm_tan_skin",
            "dark_teal_trenchcoat",
            "full_messy_wavy_chestnut_hair",
            "toy_scale_on_desk",
        ],
    }
    META.write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta, indent=2), flush=True)


if __name__ == "__main__":
    main()
