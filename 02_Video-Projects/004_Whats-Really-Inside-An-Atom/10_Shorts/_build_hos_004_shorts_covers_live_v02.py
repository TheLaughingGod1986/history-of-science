#!/usr/bin/env python3
"""HOS 004 Short covers live-v02 — match live 002 Short covers.

Painted scene stills (Flow) + huge chunky cream/gold type across the TOP
with dark outline · ≥60% width · no see-through text box · Explorer OK on cover.
8-up sheet = 5 live 002 covers + 3 new. STOP for Ben — do not upload.
"""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
OUT = HERE / "covers_live_v02"
STILLS = OUT / "stills"
LIVE002 = REPO / (
    "02_Video-Projects/002_How-Did-We-Discover-The-Periodic-Table/"
    "08_Thumbnail/Shorts"
)
ICLOUD = Path.home() / (
    "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT/"
    "004_Whats-Really-Inside-An-Atom/10_Shorts"
)
ART = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts"
AGENT = Path.home() / (
    "Library/Application Support/Cursor/AgentStores/"
    "cursor_agent_stores/bc-958ae0f3-be07-568f-a2ab-eb7f422d8839/files/artifacts"
)
PREVIEW = REPO / "00_Brand/Channel-Setup/tools/thumb_preview.py"

W, H = 1080, 1920
FONT = Path("/System/Library/Fonts/Supplemental/Georgia Bold.ttf")
CREAM = (245, 232, 198)
GOLD = (232, 186, 72)
TEAL = (120, 190, 188)
INK = (28, 16, 8)
SHADOW = (12, 8, 4)

JOBS = [
    {
        "id": "s01",
        "lines": ["HOW", "SMALL?"],
        "colors": [CREAM, GOLD],
        "still": STILLS / "s01_how_small_scene.png",
        "out": OUT / "hos_004_s01_how_small_cover_live_v02.jpg",
    },
    {
        "id": "s02",
        "lines": ["EVERY", "EIGHTH?"],
        "colors": [CREAM, GOLD],
        "still": STILLS / "s02_every_eighth_scene.png",
        "out": OUT / "hos_004_s02_every_eighth_cover_live_v02.jpg",
    },
    {
        "id": "s03",
        "lines": ["THEY", "LAUGHED?"],
        "colors": [CREAM, GOLD],
        "still": STILLS / "s03_they_laughed_scene.png",
        "out": OUT / "hos_004_s03_they_laughed_cover_live_v02.jpg",
        "note": "provisional Tue hook for Idea A — STOP for Ben",
    },
]

LIVE_REFS = [
    LIVE002 / "hos_002_s01_empty_chairs_cover_live_v02.jpg",
    LIVE002 / "hos_002_s02_predict_metal_cover_live_v02.jpg",
    LIVE002 / "hos_002_s03_gallium_cover_live_v02.jpg",
    LIVE002 / "hos_002_s04_tellurium_cover_live_v02.jpg",
    LIVE002 / "hos_002_s05_other_table_cover_live_v02.jpg",
]


def font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT), size)


def draw_top_stack(
    im: Image.Image,
    lines: list[str],
    colors: list[tuple[int, int, int]],
) -> dict:
    """Huge chunky type across the TOP — no text box. ≥60% width."""
    draw = ImageDraw.Draw(im)
    max_w = int(W * 0.92)
    target_min = int(W * 0.60)
    # Start large; shrink until widest line ≤ max_w, prefer ≥60% width
    size = 168
    while size > 56:
        f = font(size)
        widths = [int(f.getlength(l)) for l in lines]
        if max(widths) <= max_w:
            break
        size -= 2
    f = font(size)
    widths = [int(f.getlength(l)) for l in lines]
    # If still under 60%, bump size up until just under max_w
    while max(widths) < target_min and size < 200:
        size += 2
        f = font(size)
        widths = [int(f.getlength(l)) for l in lines]
        if max(widths) > max_w:
            size -= 2
            f = font(size)
            widths = [int(f.getlength(l)) for l in lines]
            break

    stroke = max(6, size // 12)
    line_gap = int(size * 1.02)
    total_h = line_gap * len(lines)
    # Top band — match live tellurium / gaps placement
    y0 = 110
    for i, (line, color) in enumerate(zip(lines, colors)):
        w = int(f.getlength(line))
        x = (W - w) // 2
        y = y0 + i * line_gap
        # soft shadow
        draw.text(
            (x + 4, y + 6),
            line,
            font=f,
            fill=SHADOW,
            stroke_width=stroke + 3,
            stroke_fill=SHADOW,
        )
        draw.text(
            (x, y),
            line,
            font=f,
            fill=color,
            stroke_width=stroke,
            stroke_fill=INK,
        )
    span = max(widths) / W
    return {"size": size, "span": round(span, 3), "widths": widths, "y0": y0}


def compose(job: dict) -> dict:
    im = Image.open(job["still"]).convert("RGB")
    im = ImageOps.fit(im, (W, H), Image.Resampling.LANCZOS)
    # Slight darken upper band so cream type pops (no box)
    top = im.crop((0, 0, W, int(H * 0.38)))
    top = ImageEnhance.Brightness(top).enhance(0.78)
    im.paste(top, (0, 0))
    meta = draw_top_stack(im, job["lines"], job["colors"])
    job["out"].parent.mkdir(parents=True, exist_ok=True)
    im.save(job["out"], "JPEG", quality=90, optimize=True, subsampling=1)
    png = job["out"].with_suffix(".png")
    im.save(png)
    meta["out"] = str(job["out"])
    meta["png"] = str(png)
    meta["id"] = job["id"]
    meta["lines"] = job["lines"]
    return meta


def eight_up(new_covers: list[Path]) -> Path:
    """5 live 002 + 3 new, side by side."""
    paths = list(LIVE_REFS) + new_covers
    assert len(paths) == 8, paths
    tiles = []
    tw, th = 270, 480
    for p in paths:
        im = Image.open(p).convert("RGB")
        im = ImageOps.fit(im, (tw, th), Image.Resampling.LANCZOS)
        tiles.append(im)
    gap = 10
    sheet = Image.new("RGB", (8 * tw + 9 * gap, th + 2 * gap), (245, 240, 230))
    x = gap
    for t in tiles:
        sheet.paste(t, (x, gap))
        x += tw + gap
    out = OUT / "hos_004_shorts_covers_live_v02_eight_up.jpg"
    sheet.save(out, "JPEG", quality=90)
    return out


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    metas = []
    new_paths = []
    for job in JOBS:
        if not job["still"].exists():
            raise SystemExit(f"missing still {job['still']}")
        m = compose(job)
        metas.append(m)
        new_paths.append(job["out"])
        print(f"{job['id']} span={m['span']} size={m['size']} → {job['out'].name}", flush=True)
        if m["span"] < 0.60:
            print(f"WARN {job['id']} span {m['span']} < 0.60", flush=True)

    eight = eight_up(new_paths)
    print("eight_up", eight, flush=True)

    # thumb_preview short on the 8
    preview = OUT / "hos_004_shorts_covers_live_v02_thumb_preview.jpg"
    cmd = [
        "python3",
        str(PREVIEW),
        "short",
        *[str(p) for p in LIVE_REFS],
        *[str(p) for p in new_paths],
        "--out",
        str(preview),
    ]
    subprocess.run(cmd, check=True)
    print("thumb_preview", preview, flush=True)

    # iCloud + artifacts
    ICLOUD.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    AGENT.mkdir(parents=True, exist_ok=True)
    copies = new_paths + [eight, preview]
    for p in copies:
        shutil.copy2(p, ICLOUD / p.name)
        shutil.copy2(p, ART / f"BEN_1045_{p.name}")
        shutil.copy2(p, AGENT / f"BEN_1045_{p.name}")
    # Friendly names
    shutil.copy2(eight, AGENT / "BEN_1045_covers_eight_up.jpg")
    shutil.copy2(preview, AGENT / "BEN_1045_covers_thumb_preview.jpg")
    shutil.copy2(eight, ART / "BEN_1045_covers_eight_up.jpg")
    shutil.copy2(preview, ART / "BEN_1045_covers_thumb_preview.jpg")

    import json

    (OUT / "COVERS_LIVE_V02.json").write_text(
        json.dumps(
            {
                "ok": all(m["span"] >= 0.60 for m in metas),
                "covers": metas,
                "eight_up": str(eight),
                "thumb_preview": str(preview),
                "icloud": str(ICLOUD),
                "stop": "STOP for Ben — do not upload covers until he OKs",
                "tue_hook": "THEY LAUGHED? (Idea A provisional)",
            },
            indent=2,
        )
        + "\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
