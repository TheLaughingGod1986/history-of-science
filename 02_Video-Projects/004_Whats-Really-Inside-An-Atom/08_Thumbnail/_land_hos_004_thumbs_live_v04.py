#!/usr/bin/env python3
"""Land HOS 004 thumbs v04 to the LIVE 001/002 Studio grammar.

Ben order 29 Sep 2026. Letters REASSIGNED:
  A = atom · B = coin · C = Te/I tiles
Ignore THUMBNAIL_AND_TITLE_RULES §2.4 heavy-sans/yellow for now.
Match LIVE_THUMB_LOCK.md / 002 README Hard rules + live 002 look.

Same route as `_land_hos_002_thumbs_live_v02.py`: generated PNGs → 1280×720 JPEG.
C tiles are blank in the painting; we overlay Te 52 / I 53 in painted type.
Nothing to Studio. No KEEP/LOCKED.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "_assets_v04"
SELECTED = HERE / "Selected"
PREVIEWS = HERE / "Previews"
DRAFTS = HERE / "Drafts"
WORKER_ASSETS = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts/assets"
WALK = Path(
    "/Users/benjaminoats/Library/Application Support/Cursor/AgentStores/"
    "cursor_agent_stores/bc-958ae0f3-be07-568f-a2ab-eb7f422d8839/files/artifacts"
)
ICLOUD = (
    Path.home()
    / "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT"
    / "004_Whats-Really-Inside-An-Atom/08_Thumbnail/Selected"
)
LIVE_002 = (
    Path(__file__).resolve().parents[2]
    / "002_How-Did-We-Discover-The-Periodic-Table/08_Thumbnail/Selected"
    / "hos_002_thumb_A_gallium_live_v02.jpg"
)
PREVIEW_TOOL = (
    Path(__file__).resolve().parents[3]
    / "00_Brand/Channel-Setup/tools/thumb_preview.py"
)

W, H = 1280, 720
CREAM = (245, 232, 200)
GOLD = (232, 178, 48)
INK = (28, 18, 10)
SHADOW = (12, 8, 4)

# Painted type (live 001/002) — Georgia Bold, not Arial Black
FONT_PATHS = [
    "/System/Library/Fonts/Supplemental/Georgia Bold.ttf",
    "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf",
    "/Library/Fonts/Arial Unicode.ttf",
]

LONG = [
    ("hos_004_thumb_A_atom_live_v04.png", "hos_004_thumb_A_atom_live_v04", False),
    ("hos_004_thumb_B_cut_gold_live_v04.png", "hos_004_thumb_B_cut_gold_live_v04", False),
    ("hos_004_thumb_C_hidden_number_live_v04.png", "hos_004_thumb_C_hidden_number_live_v04", True),
]

# Tile face boxes measured on the blank-face C painting (1280×720)
TE_FACE = (570, 146, 826, 518)
I_FACE = (930, 130, 1206, 542)
TE_Z, I_Z = 52, 53


def font(size: int) -> ImageFont.FreeTypeFont:
    for p in FONT_PATHS:
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            continue
    return ImageFont.load_default()


def resolve_src(name: str) -> Path:
    for base in (ASSETS, WORKER_ASSETS, WALK / "assets", WALK):
        p = base / name
        if p.exists():
            return p
    raise SystemExit(f"missing source PNG {name}")


def save_jpg(im: Image.Image, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    rgb = im.convert("RGB").resize((W, H), Image.Resampling.LANCZOS)
    q = 90
    rgb.save(dest, "JPEG", quality=q, optimize=True, subsampling=1)
    while dest.stat().st_size > 1_900_000 and q > 70:
        q -= 4
        rgb.save(dest, "JPEG", quality=q, optimize=True, subsampling=1)
    print(f"  {dest.name}  {dest.stat().st_size} B  q={q}", flush=True)
    return dest


def paint_word(
    draw: ImageDraw.ImageDraw,
    text: str,
    *,
    cx: int,
    cy: int,
    size: int,
    fill: tuple[int, int, int],
) -> None:
    """Cream/gold painted bevel lettering (live 001/002 feel)."""
    f = font(size)
    tw = f.getlength(text)
    x = int(cx - tw / 2)
    y = int(cy - size / 2)
    # soft shadow stack
    for dx, dy in ((4, 5), (2, 3)):
        draw.text((x + dx, y + dy), text, font=f, fill=SHADOW)
    # dark edge
    draw.text((x, y), text, font=f, fill=INK, stroke_width=max(3, size // 18), stroke_fill=INK)
    draw.text((x, y), text, font=f, fill=fill)


def overlay_tile_labels(im: Image.Image) -> Image.Image:
    """House-painted Te 52 / I 53 on blank tile faces. Never AI-baked."""
    assert TE_Z == 52 and I_Z == 53
    draw = ImageDraw.Draw(im)
    specs = [
        ("Te", TE_Z, TE_FACE, CREAM, CREAM),
        ("I", I_Z, I_FACE, GOLD, GOLD),
    ]
    for symbol, number, box, scol, ncol in specs:
        x0, y0, x1, y1 = box
        tw, th = x1 - x0, y1 - y0
        cx = (x0 + x1) // 2
        # number top
        n_size = max(42, th // 7)
        paint_word(draw, str(number), cx=cx, cy=y0 + th // 5, size=n_size, fill=ncol)
        # symbol centre
        s_size = max(96, th // 3)
        paint_word(draw, symbol, cx=cx, cy=y0 + int(th * 0.52), size=s_size, fill=scol)
    return im


def land_one(src_name: str, stem: str, overlay_c: bool) -> Path:
    src = resolve_src(src_name)
    ASSETS.mkdir(parents=True, exist_ok=True)
    if not (ASSETS / src_name).exists():
        (ASSETS / src_name).write_bytes(src.read_bytes())
    im = Image.open(src).convert("RGB")
    if overlay_c:
        im = overlay_tile_labels(im)
    png = SELECTED / f"{stem}.png"
    SELECTED.mkdir(parents=True, exist_ok=True)
    im.save(png, "PNG")
    jpg = save_jpg(im, SELECTED / f"{stem}.jpg")
    DRAFTS.mkdir(parents=True, exist_ok=True)
    (DRAFTS / jpg.name).write_bytes(jpg.read_bytes())
    return jpg


def family_sheet(paths: list[Path]) -> Path:
    """One row: live 002 A + 004 A/B/C so Ben can see the family."""
    refs = [LIVE_002] + paths
    tiles = []
    tw, th = 420, 236
    for p in refs:
        im = Image.open(p).convert("RGB").resize((tw, th), Image.Resampling.LANCZOS)
        tiles.append(im)
    gap = 16
    labels = ["002 LIVE A", "004 A atom", "004 B coin", "004 C Te/I"]
    label_h = 36
    sheet_w = gap + len(tiles) * (tw + gap)
    sheet_h = gap + label_h + th + gap
    sheet = Image.new("RGB", (sheet_w, sheet_h), (18, 14, 10))
    draw = ImageDraw.Draw(sheet)
    f = font(22)
    x = gap
    for im, lab in zip(tiles, labels):
        draw.text((x, gap + 4), lab, font=f, fill=CREAM)
        sheet.paste(im, (x, gap + label_h))
        x += tw + gap
    out = SELECTED / "hos_004_thumbs_v04_family_vs_002_live.jpg"
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, "JPEG", quality=92, optimize=True)
    print(f"  FAMILY {out.name}  {out.stat().st_size} B  {sheet.size}", flush=True)
    return out


def run_previews(paths: list[Path]) -> list[Path]:
    import subprocess
    import sys

    outs = []
    PREVIEWS.mkdir(parents=True, exist_ok=True)
    for p in paths:
        preview = SELECTED / f"{p.stem}_preview.jpg"
        subprocess.check_call(
            [sys.executable, str(PREVIEW_TOOL), "long", str(p), "--out", str(preview)],
        )
        (PREVIEWS / f"{p.stem.replace('_live_v04', '')}_preview_v04.jpg").write_bytes(preview.read_bytes())
        outs.append(preview)
    return outs


def write_index(paths: list[Path]) -> Path:
    pairs = [
        {
            "slot": 1,
            "role": "main",
            "title": "What's Really Inside an Atom?",
            "thumbId": "A",
            "hook": "WHAT'S REALLY INSIDE AN ATOM?",
            "jpg": f"Selected/{paths[0].name}",
            "preview": f"Selected/{paths[0].stem}_preview.jpg",
            "sha256": hashlib.sha256(paths[0].read_bytes()).hexdigest(),
            "bytes": paths[0].stat().st_size,
        },
        {
            "slot": 2,
            "role": "alt",
            "title": "Why Is the Periodic Table in This Order?",
            "thumbId": "C",
            "hook": "THE HIDDEN NUMBER",
            "jpg": f"Selected/{paths[2].name}",
            "preview": f"Selected/{paths[2].stem}_preview.jpg",
            "sha256": hashlib.sha256(paths[2].read_bytes()).hexdigest(),
            "bytes": paths[2].stat().st_size,
        },
        {
            "slot": 3,
            "role": "alt",
            "title": "How Small Can You Cut Gold?",
            "thumbId": "B",
            "hook": "CUT GOLD?",
            "jpg": f"Selected/{paths[1].name}",
            "preview": f"Selected/{paths[1].stem}_preview.jpg",
            "sha256": hashlib.sha256(paths[1].read_bytes()).hexdigest(),
            "bytes": paths[1].stat().st_size,
        },
    ]
    idx = {
        "parentTitle": "What's Really Inside an Atom?",
        "version": "v04",
        "status": "STOP for Ben pick. Proposed only. Nothing to Studio. No KEEP/LOCKED.",
        "note": (
            "Letters REASSIGNED vs v01–v03: A=atom, B=coin, C=Te/I. "
            "Live 001/002 Studio grammar (cream + gold punch painted type). "
            "Ignores THUMBNAIL_AND_TITLE_RULES §2.4 heavy-sans/yellow for now."
        ),
        "composer": "_land_hos_004_thumbs_live_v04.py",
        "styleLock": "002 LIVE_THUMB_LOCK.md + README Hard rules",
        "factLock": {"Te": 52, "I": 53, "note": "painted overlays on blank tiles only"},
        "testAndComparePairs": pairs,
        "upload": False,
        "studio": False,
        "icloud": "HOS UAT/004_Whats-Really-Inside-An-Atom/08_Thumbnail/Selected/",
        "familySheet": "Selected/hos_004_thumbs_v04_family_vs_002_live.jpg",
    }
    out = HERE / "THUMBS_INDEX_v04.json"
    out.write_text(json.dumps(idx, indent=2) + "\n")
    print(f"  INDEX {out.name}", flush=True)
    return out


def sync_icloud(paths: list[Path], extras: list[Path]) -> None:
    ICLOUD.mkdir(parents=True, exist_ok=True)
    for p in paths + extras:
        dest = ICLOUD / p.name
        dest.write_bytes(p.read_bytes())
        print(f"  iCloud ← {p.name}", flush=True)


def main() -> None:
    print("LONG v04", flush=True)
    paths = [land_one(src, stem, overlay) for src, stem, overlay in LONG]
    family = family_sheet(paths)
    previews = run_previews(paths)
    write_index(paths)
    # walkthrough copies
    WALK.mkdir(parents=True, exist_ok=True)
    for p in paths + previews + [family]:
        (WALK / p.name).write_bytes(p.read_bytes())
    sync_icloud(paths, previews + [family])
    print("DONE", [p.name for p in paths])
    print("FACT_LOCK Te=52 I=53 · live Studio grammar · STOP for Ben · no Studio")


if __name__ == "__main__":
    main()
