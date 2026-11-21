#!/usr/bin/env python3
"""Letter HOS 009 long thumbs A and B (J3262). £0. No new generation.

Plates are the 0-credit Flow Nano Banana 2.1 stills. Lettering is the house
Georgia serif: cream words, one gold punch word, gold scroll flourishes.
A: IT / MISSES. B: ONE / APPLE. Neither line repeats the title.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
FILM = HERE.parent
REPO = FILM.parents[1]
ASSETS = HERE / "_assets_v01"
SELECTED = HERE / "Selected"
TOOLS = REPO / "00_Brand/Channel-Setup/tools"
COMPOSE = (
    REPO
    / "02_Video-Projects/006_Trees-Are-Made-Of-Air/08_Thumbnail/_compose_hos_006_thumbs_v01.py"
)
W, H = 1280, 720


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_compose():
    spec = importlib.util.spec_from_file_location("hos006compose", COMPOSE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def scrim(im: Image.Image, width: int, strength: float) -> Image.Image:
    arr = np.array(im.convert("RGB"), dtype=np.float32)
    shade = np.array([18, 12, 8], dtype=np.float32)
    xs = np.arange(W, dtype=np.float32)
    alpha = np.clip(1 - xs / width, 0, 1) ** 1.35
    alpha = alpha * strength
    alpha[width:] = 0
    kernel = np.array([1, 4, 6, 4, 1], dtype=np.float32)
    kernel /= kernel.sum()
    alpha = np.convolve(alpha, kernel, mode="same")
    out = arr * (1 - alpha)[None, :, None] + shade * alpha[None, :, None]
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), "RGB")


def main() -> int:
    c = load_compose()
    SELECTED.mkdir(parents=True, exist_ok=True)
    plate_a = ASSETS / "hos_009_thumb_A_it_misses_plate01.jpg"
    plate_b = ASSETS / "hos_009_thumb_B_one_apple_plate01.jpg"
    for p in (plate_a, plate_b, COMPOSE):
        if not p.exists():
            raise SystemExit(f"missing {p}")
    top_orn, bot_orn = c.extract_scroll_ornaments(c.ORNAMENT_REF)

    base_a = scrim(Image.open(plate_a).convert("RGB").resize((W, H), Image.Resampling.LANCZOS), 560, 0.42)
    lines_a = [
        ("IT", "cream", 92, 0.92),
        ("MISSES", "gold", 108, 0.90),
    ]
    hero_a = (620, 10, 1260, 640)
    explorer_a = (70, 400, 380, 710)
    im_a, meta_a = c.compose_variant(
        base_a, lines_a, cx=250, top_y=78, line_gap=6,
        top_orn=top_orn, bot_orn=bot_orn,
        hero_box=hero_a, explorer_box=explorer_a,
    )
    out_a = SELECTED / "hos_009_thumb_A_it_misses_v01.jpg"
    im_a.save(out_a, "JPEG", quality=93, optimize=True, subsampling=1)

    base_b = scrim(Image.open(plate_b).convert("RGB").resize((W, H), Image.Resampling.LANCZOS), 520, 0.55)
    lines_b = [
        ("ONE", "cream", 92, 0.92),
        ("APPLE", "gold", 108, 0.90),
    ]
    hero_b = (680, 20, 1240, 560)
    explorer_b = (160, 390, 520, 710)
    im_b, meta_b = c.compose_variant(
        base_b, lines_b, cx=230, top_y=70, line_gap=6,
        top_orn=top_orn, bot_orn=bot_orn,
        hero_box=hero_b, explorer_box=explorer_b,
    )
    out_b = SELECTED / "hos_009_thumb_B_one_apple_v01.jpg"
    im_b.save(out_b, "JPEG", quality=93, optimize=True, subsampling=1)

    for path in (out_a, out_b):
        subprocess.check_call([
            sys.executable, str(TOOLS / "thumb_preview.py"), "long", str(path),
            "--out", str(SELECTED / f"{path.stem}_preview.jpg"),
        ])
        subprocess.check_call([
            sys.executable, str(TOOLS / "style_sheet.py"), "long", str(path),
            "--out", str(SELECTED / f"{path.stem}_style.jpg"),
        ])
    family = SELECTED / "hos_009_thumbs_v01_family.jpg"
    subprocess.check_call([
        sys.executable, str(TOOLS / "style_sheet.py"), "long", str(out_a), str(out_b),
        "--out", str(family),
    ])
    index = {
        "job": "J3262",
        "film": "009",
        "spend": "£0 cash. Flow Nano Banana 2.1 stills, 0 credits (23450 before and after).",
        "titleNotRepeated": [
            "Why Doesn't the Moon Fall to Earth?",
            "The Moon Is Falling Right Now",
        ],
        "A": {
            "file": out_a.name,
            "words": "IT / MISSES",
            "gold": "MISSES",
            "sha256": sha256(out_a),
            "meta": meta_a,
        },
        "B": {
            "file": out_b.name,
            "words": "ONE / APPLE",
            "gold": "APPLE",
            "sha256": sha256(out_b),
            "meta": meta_b,
        },
    }
    (HERE / "THUMBS_INDEX_v01.json").write_text(json.dumps(index, indent=2) + "\n")
    print("A", out_a.name, meta_a["clearOfHero"], meta_a["clearOfExplorer"], meta_a["clearOfBadge"], meta_a["letteringBox"])
    print("B", out_b.name, meta_b["clearOfHero"], meta_b["clearOfExplorer"], meta_b["clearOfBadge"], meta_b["letteringBox"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
