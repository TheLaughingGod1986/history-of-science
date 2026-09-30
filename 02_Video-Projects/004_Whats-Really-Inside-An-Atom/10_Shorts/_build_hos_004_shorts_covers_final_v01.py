#!/usr/bin/env python3
"""HOS 004 Shorts final covers — painted live-002 house look (§4).

Still from each passed cut (not frame 0) + cream/gold stacked hook type.
Feed-safe centre stack · no KEEP/LOCKED labels · preview sheet · iCloud copy.
"""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
OUT = HERE / "covers_final"
STILLS = OUT / "stills"
ICLOUD = Path.home() / (
    "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT/"
    "004_Whats-Really-Inside-An-Atom/10_Shorts"
)
ART = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts/hos004_shorts_covers_final"
W, H = 1080, 1920
FONT = Path("/System/Library/Fonts/Supplemental/Georgia Bold.ttf")
FONT_REG = Path("/System/Library/Fonts/Supplemental/Georgia.ttf")
CREAM = (245, 232, 198)
GOLD = (232, 186, 72)
INK = (28, 18, 8)
TEAL = (120, 170, 168)

JOBS = [
    {
        "id": "s01",
        "hook_lines": ["HOW", "SMALL?"],
        "still": STILLS / "clean_s01_0.8.jpg",
        "out": OUT / "hos_004_s01_how_small_cover_final.jpg",
        "accent": GOLD,
    },
    {
        "id": "s02",
        "hook_lines": ["EVERY", "EIGHTH?"],
        "still": STILLS / "clean_s02p_9.0.jpg",
        "out": OUT / "hos_004_s02_every_eighth_cover_final.jpg",
        "accent": GOLD,
    },
    {
        "id": "s03",
        "hook_lines": ["HER", "RING"],
        "still": STILLS / "s03scan_10.jpg",
        "out": OUT / "hos_004_s03_her_ring_cover_final.jpg",
        "accent": GOLD,
    },
]


def fit_still(path: Path) -> Image.Image:
    im = Image.open(path).convert("RGB")
    im = ImageOps.fit(im, (W, H), Image.Resampling.LANCZOS)
    # Slight grade toward live warm look
    im = ImageEnhance.Color(im).enhance(1.06)
    im = ImageEnhance.Contrast(im).enhance(1.04)
    # Soft vignette so type pops
    vig = Image.new("L", (W, H), 0)
    vd = ImageDraw.Draw(vig)
    for y in range(H):
        # darker toward top/bottom edges a little
        t = min(y / (H * 0.22), (H - 1 - y) / (H * 0.18), 1.0)
        vd.line([(0, y), (W, y)], fill=int(255 * (0.72 + 0.28 * t)))
    dark = ImageEnhance.Brightness(im).enhance(0.78)
    im = Image.composite(im, dark, vig)
    return im


def measure(lines: list[str], size: int) -> tuple[ImageFont.FreeTypeFont, list[int], list[int]]:
    font = ImageFont.truetype(str(FONT), size)
    widths = [int(font.getlength(l)) for l in lines]
    heights = [font.getbbox(l)[3] - font.getbbox(l)[1] for l in lines]
    return font, widths, heights


def pick_size(lines: list[str], target_w: int = int(W * 0.72)) -> int:
    # Grow until stack spans ~60–75% width
    lo, hi = 72, 220
    best = 120
    while lo <= hi:
        mid = (lo + hi) // 2
        _, widths, _ = measure(lines, mid)
        mw = max(widths)
        if mw < target_w:
            best = mid
            lo = mid + 1
        else:
            hi = mid - 1
    return best


def paint_type(canvas: Image.Image, lines: list[str], accent: tuple[int, int, int]) -> None:
    size = pick_size(lines)
    font, widths, heights = measure(lines, size)
    gap = int(size * 0.12)
    stack_h = sum(heights) + gap * (len(lines) - 1)
    # Vertical centre (survives 16:9 crop)
    y0 = (H - stack_h) // 2 - int(H * 0.02)
    draw = ImageDraw.Draw(canvas)

    # Soft dark plate behind type for readability (not a brown lower-third)
    pad_x = int(W * 0.08)
    pad_y = int(size * 0.35)
    plate = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pd = ImageDraw.Draw(plate)
    pd.rounded_rectangle(
        [
            pad_x,
            y0 - pad_y,
            W - pad_x,
            y0 + stack_h + pad_y + int(size * 0.35),
        ],
        radius=36,
        fill=(12, 8, 4, 110),
    )
    canvas.paste(Image.alpha_composite(canvas.convert("RGBA"), plate).convert("RGB"))

    draw = ImageDraw.Draw(canvas)
    y = y0
    for i, line in enumerate(lines):
        tw = widths[i]
        th = heights[i]
        x = (W - tw) // 2
        fill = CREAM if i == 0 else accent
        # Deep ink outline (painted edge)
        for dx in range(-5, 6):
            for dy in range(-5, 6):
                if dx * dx + dy * dy > 28:
                    continue
                draw.text((x + dx, y + dy), line, font=font, fill=INK)
        # Warm under-glow
        for dx, dy in ((0, 4), (0, 6), (2, 5), (-2, 5)):
            draw.text((x + dx, y + dy), line, font=font, fill=(90, 55, 10))
        draw.text((x, y), line, font=font, fill=fill)
        y += th + gap

    # Small gold flourish under last line (live-002 cue)
    fy = y + int(size * 0.05)
    cx = W // 2
    draw.arc([cx - 70, fy - 8, cx + 70, fy + 28], 200, 340, fill=accent, width=4)
    draw.ellipse([cx - 5, fy + 6, cx + 5, fy + 16], fill=accent)


def save_jpg(im: Image.Image, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    q = 90
    im.save(dest, "JPEG", quality=q, optimize=True, subsampling=1)
    while dest.stat().st_size > 1_900_000 and q > 72:
        q -= 4
        im.save(dest, "JPEG", quality=q, optimize=True, subsampling=1)


def preview_sheet(paths: list[Path], out: Path) -> None:
    tool = REPO / "00_Brand/Channel-Setup/tools/thumb_preview.py"
    subprocess.run(
        ["python3", str(tool), "short", *[str(p) for p in paths], "--out", str(out)],
        check=True,
    )


def contact_sheet(paths: list[Path], out: Path) -> None:
    """Full-size side-by-side for Ben screenshot (no KEEP labels)."""
    tiles = []
    for p in paths:
        im = Image.open(p).convert("RGB")
        im = im.resize((360, 640), Image.Resampling.LANCZOS)
        tiles.append(im)
    gap = 16
    sheet = Image.new(
        "RGB",
        (gap + len(tiles) * (360 + gap), 640 + 2 * gap),
        (245, 240, 230),
    )
    x = gap
    for t in tiles:
        sheet.paste(t, (x, gap))
        x += 360 + gap
    save_jpg(sheet, out)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    ICLOUD.mkdir(parents=True, exist_ok=True)
    outs = []
    for job in JOBS:
        assert job["still"].exists(), job["still"]
        canvas = fit_still(job["still"])
        paint_type(canvas, job["hook_lines"], job["accent"])
        # Mild sharpen
        canvas = canvas.filter(ImageFilter.UnsharpMask(radius=1.2, percent=110, threshold=2))
        save_jpg(canvas, job["out"])
        outs.append(job["out"])
        print(f"WROTE {job['out'].name}  {job['out'].stat().st_size}  from {job['still'].name}")

    sheet = OUT / "hos_004_shorts_covers_final_preview_sheet.jpg"
    preview_sheet(outs, sheet)
    contact = OUT / "hos_004_shorts_covers_final_contact.jpg"
    contact_sheet(outs, contact)
    print(f"WROTE {sheet.name}")
    print(f"WROTE {contact.name}")

    # Copy to iCloud + artifacts (no KEEP/LOCKED names)
    for p in outs + [sheet, contact]:
        shutil.copy2(p, ICLOUD / p.name)
        shutil.copy2(p, ART / p.name)
        print(f"ICLOUD+ART {p.name}")


if __name__ == "__main__":
    main()
