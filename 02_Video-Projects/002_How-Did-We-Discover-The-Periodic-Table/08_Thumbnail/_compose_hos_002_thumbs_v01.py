#!/usr/bin/env python3
"""Compose HOS 002 long ABC thumbs + Shorts covers from film frames.

Animistry house: one big 3D-cartoon scene + title painted into the picture.
Not a brown lower-third bar. No Orbit. Film frames only — no remint.

Long title (all ABC): HOW DID WE / DISCOVER THE / PERIODIC TABLE?
Shorts covers use the punch line for that slot.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
PROJ = HERE.parent
EXP = PROJ / "09_Final-Export"
SELECTED = HERE / "Selected"
SHORTS = HERE / "Shorts"
FRAMES = HERE / "_frames_v01"
ICLOUD = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT"
ICLOUD_THUMBS = ICLOUD / "002_thumbs"

CREAM = (245, 232, 210)
GOLD = (214, 162, 48)
INK = (42, 28, 18)
SHADOW = (24, 16, 12, 210)

DIDOT = "/System/Library/Fonts/Supplemental/Didot.ttc"
IMPACT = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"
TIMES = "/System/Library/Fonts/Supplemental/Times New Roman.ttf"

LONG_LINES = ["HOW DID WE", "DISCOVER THE", "PERIODIC TABLE?"]

# Local times on locked parts (do not wait for the full stitch).
LONG = [
    {
        "id": "A",
        "beat": "object — gallium in the Explorer's palm",
        "src_part": "hos_002_part05_rough_v01.mp4",
        "t": 24.5,
        "frame": FRAMES / "a_gallium_palm.jpg",
        "png": SELECTED / "hos_002_thumb_A_gallium_v01.png",
        "jpg": SELECTED / "hos_002_thumb_A_gallium_v01.jpg",
        "type_anchor": "left",
    },
    {
        "id": "B",
        "beat": "emotion — Explorer leaves a gap in the cards",
        "src_part": "hos_002_part04_rough_v25.mp4",
        "t": 48.8,
        "frame": FRAMES / "b_explorer_gap.jpg",
        "png": SELECTED / "hos_002_thumb_B_empty_seats_v01.png",
        "jpg": SELECTED / "hos_002_thumb_B_empty_seats_v01.jpg",
        "type_anchor": "left",
    },
    {
        "id": "C",
        "beat": "question — one empty seat still glowing",
        "src_part": "hos_002_part05_rough_v01.mp4",
        "t": 8.0,
        "frame": FRAMES / "a_gallium_early.jpg",
        "png": SELECTED / "hos_002_thumb_C_empty_slot_v01.png",
        "jpg": SELECTED / "hos_002_thumb_C_empty_slot_v01.jpg",
        "type_anchor": "left",
    },
]

SHORT_COVERS = [
    {
        "id": "s01_empty_chairs",
        "title": "The empty chairs were the cleverest part",
        "src_part": "hos_002_part04_rough_v25.mp4",
        "t": 47.2,
        "lines": ["THE EMPTY CHAIRS", "WERE THE POINT"],
    },
    {
        "id": "s02_predict_metal",
        "title": "He predicted a metal before anyone found it",
        "src_part": "hos_002_part04_rough_v25.mp4",
        "t": 72.0,
        "lines": ["HE PREDICTED", "A METAL"],
    },
    {
        "id": "s03_gallium",
        "title": "A drop of gallium that sat in the gap",
        "src_part": "hos_002_part05_rough_v01.mp4",
        "t": 24.5,
        "lines": ["A DROP OF", "GALLIUM"],
    },
    {
        "id": "s04_tellurium",
        "title": "Why tellurium and iodine sat wrong",
        "src_part": "hos_002_part04_rough_v25.mp4",
        "t": 108.0,
        "lines": ["TELLURIUM", "BEFORE IODINE"],
    },
    {
        "id": "s05_other_table",
        "title": "What other table are we staring at?",
        "src_part": "hos_002_part05_rough_v01.mp4",
        "t": 124.0,
        "lines": ["WHAT OTHER", "TABLE?"],
    },
]


def font(path: str, size: int, index: int = 0) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(path, size, index=index)
    except OSError:
        return ImageFont.truetype(TIMES, size)


def draw_stacked(
    im: Image.Image,
    lines: list[str],
    *,
    sizes: list[int],
    colors: list[tuple[int, int, int]],
    x: int,
    y: int,
    max_w: int,
) -> None:
    draw = ImageDraw.Draw(im)
    cy = y
    for line, size, color in zip(lines, sizes, colors):
        f = font(IMPACT, size)
        # shrink until it fits
        while f.getlength(line) > max_w and size > 28:
            size -= 2
            f = font(IMPACT, size)
        stroke = max(4, size // 14)
        draw.text(
            (x + 3, cy + 4),
            line,
            font=f,
            fill=SHADOW,
            stroke_width=stroke + 2,
            stroke_fill=SHADOW,
        )
        draw.text(
            (x, cy),
            line,
            font=f,
            fill=color,
            stroke_width=stroke,
            stroke_fill=INK,
        )
        cy += int(size * 1.08)


def cover_side_label(im: Image.Image) -> Image.Image:
    """Hide the brown HUD pill in the top-right of part roughs."""
    w, h = im.size
    # sample wood/scene just left of the pill
    crop = im.crop((int(w * 0.62), 8, int(w * 0.70), int(h * 0.14)))
    wash = crop.resize((int(w * 0.42), int(h * 0.16)), Image.Resampling.LANCZOS)
    wash = wash.filter(ImageFilter.GaussianBlur(8))
    out = im.copy()
    out.paste(wash, (int(w * 0.58), 0))
    return out


def compose_long(job: dict) -> None:
    src = Image.open(job["frame"]).convert("RGB")
    src = src.resize((1280, 720), Image.Resampling.LANCZOS)
    src = cover_side_label(src)
    # slight grade so type pops
    overlay = Image.new("RGB", src.size, (20, 12, 8))
    src = Image.blend(src, overlay, 0.12)
    draw_stacked(
        src,
        LONG_LINES,
        sizes=[46, 58, 52],
        colors=[CREAM, CREAM, GOLD],
        x=48,
        y=78,
        max_w=620,
    )
    job["png"].parent.mkdir(parents=True, exist_ok=True)
    src.save(job["png"])
    rgb = src.convert("RGB")
    q = 88
    rgb.save(job["jpg"], "JPEG", quality=q, optimize=True, subsampling=1)
    while job["jpg"].stat().st_size > 1_800_000 and q > 70:
        q -= 4
        rgb.save(job["jpg"], "JPEG", quality=q, optimize=True, subsampling=1)


def extract_frame(part: str, t: float, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    src = EXP / part
    subprocess.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-ss", f"{t:.3f}", "-i", str(src), "-frames:v", "1", str(dest),
        ],
        check=True,
    )


def compose_short(job: dict) -> None:
    frame = FRAMES / f"{job['id']}_cover.jpg"
    extract_frame(job["src_part"], job["t"], frame)
    src = Image.open(frame).convert("RGB")
    # 9:16 centre crop from 16:9
    w, h = src.size
    crop_w = int(h * 9 / 16)
    x0 = (w - crop_w) // 2
    src = src.crop((x0, 0, x0 + crop_w, h)).resize((1080, 1920), Image.Resampling.LANCZOS)
    src = cover_side_label(src)
    overlay = Image.new("RGB", src.size, (20, 12, 8))
    src = Image.blend(src, overlay, 0.16)
    draw_stacked(
        src,
        job["lines"],
        sizes=[72, 86],
        colors=[CREAM, GOLD],
        x=70,
        y=220,
        max_w=900,
    )
    png = SHORTS / f"hos_002_{job['id']}_cover_v01.png"
    jpg = SHORTS / f"hos_002_{job['id']}_cover_v01.jpg"
    SHORTS.mkdir(parents=True, exist_ok=True)
    src.save(png)
    src.convert("RGB").save(jpg, "JPEG", quality=86, optimize=True, subsampling=1)
    job["png"] = str(png.name)
    job["jpg"] = str(jpg.name)


def main() -> None:
    FRAMES.mkdir(parents=True, exist_ok=True)
    SELECTED.mkdir(parents=True, exist_ok=True)
    for job in LONG:
        if not job["frame"].exists():
            extract_frame(job["src_part"], job["t"], job["frame"])
        compose_long(job)
        print(f"LONG {job['id']} {job['jpg']}", flush=True)
    for job in SHORT_COVERS:
        compose_short(job)
        print(f"SHORT {job['id']}", flush=True)

    index = {
        "parentTitle": "How Did We Discover the Periodic Table?",
        "style": "Animistry painted-in type. Film-frame overlays are fallback. No Orbit. UAT.",
        "recommend": "A (gallium palm) as listing thumb; B emotion; C empty slot. Run Studio ABC after upload.",
        "long": [
            {
                "id": "A",
                "beat": "object — gallium in the Explorer's palm",
                "jpg": "hos_002_thumb_A_gallium_animistry_v01.jpg",
                "fallback": "hos_002_thumb_A_gallium_v01.jpg",
            },
            {
                "id": "B",
                "beat": "emotion — Explorer leaves a gap in the cards",
                "jpg": "hos_002_thumb_B_empty_seats_animistry_v01.jpg",
                "fallback": "hos_002_thumb_B_empty_seats_v01.jpg",
            },
            {
                "id": "C",
                "beat": "question — one empty seat still glowing",
                "jpg": "hos_002_thumb_C_empty_slot_animistry_v01.jpg",
                "fallback": "hos_002_thumb_C_empty_slot_v01.jpg",
            },
        ],
        "shorts": SHORT_COVERS,
        "upload": False,
        "vidiq": "Score before listing lock. Reject fearbait.",
    }
    (HERE / "THUMBS_INDEX_v01.json").write_text(json.dumps(index, indent=2) + "\n")
    ICLOUD_THUMBS.mkdir(parents=True, exist_ok=True)
    for job in LONG:
        for p in (job["png"], job["jpg"]):
            (ICLOUD_THUMBS / p.name).write_bytes(p.read_bytes())
    for job in SHORT_COVERS:
        for name in (job["png"], job["jpg"]):
            src = SHORTS / name
            (ICLOUD_THUMBS / name).write_bytes(src.read_bytes())
    print(f"ICLOUD {ICLOUD_THUMBS}", flush=True)


if __name__ == "__main__":
    main()
