#!/usr/bin/env python3
"""Letter HOS 008 Franklin long thumbs A and B at £0 / 0 Flow credits (J3500).

No thumb plates existed (08_Thumbnail was a README only). Following the HOS 007
J0946 £0 master-frame precedent, these use two clean, unlabelled painted 3D
cartoon frames extracted directly from the Ben-approved master v05
(hos_008_master_v05.mp4, sha256 d1ffb78d...841b):
  - Plate A (t = 4.20 s, 01_kite_open): giant iron key on wet kite string,
    blue-white spark jumping to Franklin's knuckle under storm clouds.
    Words: THE KEY / SPARKED (gold SPARKED).
  - Plate B (t = 290.50 s, 19_kite_climb): silk kite soaring into rolling
    storm clouds, glowing wet twine down to Franklin by the lantern-lit shed.
    Words: NO BOLT / STRUCK (gold STRUCK).

Neither variant repeats any word of Title A ("Benjamin Franklin's Kite
Experiment Explained") or Title B ("Why Did Franklin Fly a Kite in a Storm?").
Lettering uses the house Georgia bold serif (cream + one gold punch word) and
gold scroll flourishes from _compose_hos_006_thumbs_v01.py. No new image
generation, no Flow/Vertex spend, £0.
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
MASTER_V05 = Path(
    "/Volumes/data/studio-live/History Of Science/02_Video-Projects/"
    "008_Lightning-Franklin/07_Edit-Project/_precheck/master_v05/"
    "hos_008_master_v05.mp4"
)
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
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def extract_frame(t_s: float, out_png: Path) -> None:
    if out_png.exists():
        return
    if not MASTER_V05.exists():
        raise SystemExit(f"missing master v05: {MASTER_V05}")
    subprocess.check_call([
        "ffmpeg", "-y", "-v", "error",
        "-ss", f"{t_s:.2f}", "-i", str(MASTER_V05),
        "-frames:v", "1", str(out_png),
    ])


def prepare_plate(src: Path, *, zoom: float = 1.0, pan_x: float = 0.0, pan_y: float = 0.0) -> Image.Image:
    im = Image.open(src).convert("RGB")
    # Gentle clarity/contrast lift in warm period palette (no Orbit saturation push).
    im = ImageEnhance.Contrast(im).enhance(1.06)
    im = ImageEnhance.Sharpness(im).enhance(1.10)
    nw = int(round(W * zoom))
    nh = int(round(H * zoom))
    im = im.resize((nw, nh), Image.Resampling.LANCZOS)
    max_x = max(0, nw - W)
    max_y = max(0, nh - H)
    left = int(round(max_x * pan_x))
    top = int(round(max_y * pan_y))
    return im.crop((left, top, left + W, top + H))


def scrim_left(im: Image.Image, width: int, strength: float) -> Image.Image:
    """Soft warm-dark gradient behind the left lettering band; hero stays untouched."""
    arr = np.array(im, dtype=np.float32)
    shade = np.array([16, 12, 10], dtype=np.float32)
    xs = np.arange(W, dtype=np.float32)
    alpha = np.clip(1.0 - xs / width, 0.0, 1.0) ** 1.35
    alpha = (alpha * strength).astype(np.float32)
    alpha[width:] = 0.0
    kernel = np.array([1, 4, 6, 4, 1], dtype=np.float32)
    kernel /= kernel.sum()
    alpha = np.convolve(alpha, kernel, mode="same")
    out = arr * (1.0 - alpha)[None, :, None] + shade * alpha[None, :, None]
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), "RGB")


def main() -> int:
    if not COMPOSE.exists():
        raise SystemExit(f"missing {COMPOSE}")
    c = load_compose()
    SELECTED.mkdir(parents=True, exist_ok=True)
    ASSETS.mkdir(parents=True, exist_ok=True)
    top_orn, bot_orn = c.extract_scroll_ornaments(c.ORNAMENT_REF)

    raw_a = ASSETS / "hos_008_thumb_A_raw_t4p20.png"
    raw_b = ASSETS / "hos_008_thumb_B_raw_t290p50.png"
    extract_frame(4.20, raw_a)
    extract_frame(290.50, raw_b)

    # Plate A: zoom 1.05, pan_x=0.0, pan_y=0.0 keeps Franklin's forehead + full key in frame and left band x<405 clear.
    plate_a_jpg = ASSETS / "hos_008_thumb_A_plate.jpg"
    plate_a = scrim_left(prepare_plate(raw_a, zoom=1.05, pan_x=0.0, pan_y=0.0), width=460, strength=0.42)
    plate_a.save(plate_a_jpg, "JPEG", quality=93)

    # Plate B: zoom 1.06, pan_x=0.0, pan_y=0.0 keeps the entire kite peak AND Franklin in frame while left band stays clear.
    plate_b_jpg = ASSETS / "hos_008_thumb_B_plate.jpg"
    plate_b = scrim_left(prepare_plate(raw_b, zoom=1.06, pan_x=0.0, pan_y=0.0), width=450, strength=0.44)
    plate_b.save(plate_b_jpg, "JPEG", quality=93)

    # Variant A: THE KEY / SPARKED (gold SPARKED)
    lines_a = [
        ("THE", "cream", 74, 0.88),
        ("KEY", "cream", 94, 0.88),
        ("SPARKED", "gold", 86, 0.84),
    ]
    hero_a = (420, 140, 1260, 710)
    explorer_a = (40, 560, 260, 710)
    im_a, meta_a = c.compose_variant(
        plate_a, lines_a, cx=208, top_y=54, line_gap=4,
        top_orn=top_orn, bot_orn=bot_orn,
        hero_box=hero_a, explorer_box=explorer_a,
    )
    out_a = SELECTED / "hos_008_thumb_A_the_key_sparked_v01.jpg"
    im_a.save(out_a, "JPEG", quality=93, optimize=True, subsampling=1)

    # Variant B: NO BOLT / STRUCK (gold STRUCK)
    lines_b = [
        ("NO", "cream", 76, 0.90),
        ("BOLT", "cream", 92, 0.88),
        ("STRUCK", "gold", 88, 0.84),
    ]
    hero_b = (395, 4, 1250, 710)
    explorer_b = (40, 560, 260, 710)
    im_b, meta_b = c.compose_variant(
        plate_b, lines_b, cx=202, top_y=54, line_gap=4,
        top_orn=top_orn, bot_orn=bot_orn,
        hero_box=hero_b, explorer_box=explorer_b,
    )
    out_b = SELECTED / "hos_008_thumb_B_no_bolt_struck_v01.jpg"
    im_b.save(out_b, "JPEG", quality=93, optimize=True, subsampling=1)

    for label, meta in (("A", meta_a), ("B", meta_b)):
        print(
            label,
            "box=", meta["letteringBox"],
            "clearOfHero=", meta["clearOfHero"],
            "clearOfBadge=", meta["clearOfBadge"],
        )
        if not (meta["clearOfHero"] and meta["clearOfBadge"]):
            raise SystemExit(f"Variant {label} failed clearance: {meta}")

    for path in (out_a, out_b):
        subprocess.check_call([
            sys.executable, str(TOOLS / "thumb_preview.py"), "long", str(path),
            "--out", str(SELECTED / f"{path.stem}_preview.jpg"),
        ])
        subprocess.check_call([
            sys.executable, str(TOOLS / "style_sheet.py"), "long", str(path),
            "--out", str(SELECTED / f"{path.stem}_style_sheet.jpg"),
        ])
    family = SELECTED / "hos_008_thumbs_AB_v01_style_sheet.jpg"
    subprocess.check_call([
        sys.executable, str(TOOLS / "style_sheet.py"), "long", str(out_a), str(out_b),
        "--out", str(family),
    ])

    # Remove raw PNGs from repo _assets_v01 (keep compact plate JPGs only)
    for raw in (raw_a, raw_b):
        raw.unlink(missing_ok=True)

    index = {
        "job": "J3500",
        "film": "008_Lightning-Franklin",
        "spend": "£0 cash, 0 Flow credits. No new generation. Plates are clean painted 3D frames from Ben-approved master v05 (d1ffb78d...841b).",
        "titleNotRepeated": [
            "Benjamin Franklin's Kite Experiment Explained",
            "Why Did Franklin Fly a Kite in a Storm?",
        ],
        "A": {
            "file": f"Selected/{out_a.name}",
            "words": "THE / KEY / SPARKED",
            "gold": "SPARKED",
            "sourceFrame": "hos_008_master_v05.mp4 @ t=4.20s (01_kite_open, no burned-in text)",
            "sha256": sha256(out_a),
            "plate": f"_assets_v01/{plate_a_jpg.name}",
            "plateSha256": sha256(plate_a_jpg),
            "meta": meta_a,
            "previews": [
                f"Selected/{out_a.stem}_preview.jpg",
                f"Selected/{out_a.stem}_style_sheet.jpg",
            ],
        },
        "B": {
            "file": f"Selected/{out_b.name}",
            "words": "NO / BOLT / STRUCK",
            "gold": "STRUCK",
            "sourceFrame": "hos_008_master_v05.mp4 @ t=290.50s (19_kite_climb, no burned-in text)",
            "sha256": sha256(out_b),
            "plate": f"_assets_v01/{plate_b_jpg.name}",
            "plateSha256": sha256(plate_b_jpg),
            "meta": meta_b,
            "previews": [
                f"Selected/{out_b.stem}_preview.jpg",
                f"Selected/{out_b.stem}_style_sheet.jpg",
            ],
        },
        "combinedStyleSheet": f"Selected/{family.name}",
    }
    (HERE / "THUMBS_INDEX_v01.json").write_text(json.dumps(index, indent=2) + "\n")
    print("DONE HOS 008 THUMBS A+B")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
