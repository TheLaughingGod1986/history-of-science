#!/usr/bin/env python3
"""Letter HOS 007 long thumbs A and B at £0 / 0 Flow credits (J0946).

No thumb plates existed (08_Thumbnail was a README only). These use two painted
stills already in the approved master v04 (the milking-dawn plate and the
lancet plate). Lettering is the house Georgia serif, cream plus one gold punch
word, with the 005 scroll ornaments. No new image generation.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageEnhance

HERE = Path(__file__).resolve().parent
FILM = HERE.parent
REPO = FILM.parents[1]
SELECTED = HERE / "Selected"
ASSETS = HERE / "_assets_v01"
NAS = Path("/Volumes/data/mac-mini-archive/hos-007-vaccine/master_v04_J0925/stills")
PLATE_A_SRC = NAS / "01_milking_dawn_v03b.png"
PLATE_B_SRC = NAS / "04_lancet_touch_v04.png"
COMPOSE = (
    REPO
    / "02_Video-Projects/006_Trees-Are-Made-Of-Air/08_Thumbnail/_compose_hos_006_thumbs_v01.py"
)
TOOLS = REPO / "00_Brand/Channel-Setup/tools"
W, H = 1280, 720


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_compose():
    spec = importlib.util.spec_from_file_location("hos006compose", COMPOSE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def cover(src: Path) -> Image.Image:
    im = Image.open(src).convert("RGB")
    im = ImageEnhance.Color(im).enhance(1.08)
    im = ImageEnhance.Contrast(im).enhance(1.06)
    # Full-bleed 16:9, biased so the hero sits right of a left lettering band.
    scale = max(W / im.width, H / im.height)
    nw, nh = int(im.width * scale), int(im.height * scale)
    im = im.resize((nw, nh), Image.Resampling.LANCZOS)
    left = max(0, min(nw - W, int((nw - W) * 0.15)))
    top = max(0, (nh - H) // 2)
    return im.crop((left, top, left + W, top + H))


def scrim(im: Image.Image, width: int) -> Image.Image:
    """Darken the left lettering band so cream type reads, and leave the hero."""
    arr = np.array(im, dtype=np.float32)
    shade = np.array([28, 16, 8], dtype=np.float32)
    xs = np.arange(W, dtype=np.float32)
    alpha = np.clip(1 - xs / width, 0, 1) ** 1.4
    alpha = (alpha * 150 / 255).astype(np.float32)
    alpha[width:] = 0
    # Soften the falloff.
    kernel = np.array([1, 4, 6, 4, 1], dtype=np.float32)
    kernel /= kernel.sum()
    alpha = np.convolve(alpha, kernel, mode="same")
    out = arr * (1 - alpha)[None, :, None] + shade * alpha[None, :, None]
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), "RGB")


def main() -> int:
    for p in (PLATE_A_SRC, PLATE_B_SRC, COMPOSE):
        if not p.exists():
            raise SystemExit(f"missing {p}")
    c = load_compose()
    SELECTED.mkdir(parents=True, exist_ok=True)
    ASSETS.mkdir(parents=True, exist_ok=True)
    top_orn, bot_orn = c.extract_scroll_ornaments(c.ORNAMENT_REF)

    plate_a = scrim(cover(PLATE_A_SRC), 560)
    plate_b = scrim(cover(PLATE_B_SRC), 520)
    plate_a.save(ASSETS / "hos_007_thumb_A_plate.jpg", quality=92)
    plate_b.save(ASSETS / "hos_007_thumb_B_plate.jpg", quality=92)

    lines_a = [
        ("THE", "cream", 72, 0.90),
        ("MILKMAID'S", "cream", 58, 0.82),
        ("SECRET", "gold", 96, 0.90),
    ]
    im_a, meta_a = c.compose_variant(
        plate_a, lines_a, cx=250, top_y=48, line_gap=2,
        top_orn=top_orn, bot_orn=bot_orn,
        hero_box=(560, 40, 1260, 700),
        explorer_box=(40, 520, 280, 710),
    )
    out_a = SELECTED / "hos_007_thumb_A_milkmaids_secret_v01.jpg"
    im_a.save(out_a, "JPEG", quality=93, optimize=True, subsampling=1)

    lines_b = [
        ("IMMUNE", "gold", 108, 0.90),
    ]
    im_b, meta_b = c.compose_variant(
        plate_b, lines_b, cx=250, top_y=70, line_gap=6,
        top_orn=top_orn, bot_orn=bot_orn,
        hero_box=(540, 80, 1260, 700),
        explorer_box=(40, 540, 280, 710),
    )
    out_b = SELECTED / "hos_007_thumb_B_immune_v01.jpg"
    im_b.save(out_b, "JPEG", quality=93, optimize=True, subsampling=1)

    for label, path in (("A", out_a), ("B", out_b)):
        subprocess.check_call([
            sys.executable, str(TOOLS / "thumb_preview.py"), "long", str(path),
            "--out", str(SELECTED / f"{path.stem}_preview.jpg"),
        ])
        subprocess.check_call([
            sys.executable, str(TOOLS / "style_sheet.py"), "long", str(path),
            "--out", str(SELECTED / f"{path.stem}_style_sheet.jpg"),
        ])
    index = {
        "job": "J0946",
        "spend": "£0, 0 Flow credits. No new generation. Plates are painted stills from master v04.",
        "A": {"file": out_a.name, "words": "THE / MILKMAID'S / SECRET", "sha256": sha256(out_a), "meta": meta_a},
        "B": {"file": out_b.name, "words": "IMMUNE", "sha256": sha256(out_b), "meta": meta_b},
        "plates": {
            "A": str(PLATE_A_SRC),
            "B": str(PLATE_B_SRC),
        },
    }
    (HERE / "THUMBS_INDEX_v01.json").write_text(json.dumps(index, indent=2) + "\n")
    print("A", out_a.name, sha256(out_a), "clear", meta_a["clearOfHero"], meta_a["clearOfBadge"])
    print("B", out_b.name, sha256(out_b), "clear", meta_b["clearOfHero"], meta_b["clearOfBadge"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
