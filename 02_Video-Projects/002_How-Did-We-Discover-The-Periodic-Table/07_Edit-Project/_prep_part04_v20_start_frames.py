#!/usr/bin/env python3
"""Prep Part 04 v20 Flow start frames — Ben UAT FAIL on parent v19 (5 stills).

Parent FAIL: hos_002_part04_rough_v19.mp4
  sha256 69d48f6e5fac419df5c23c17df5d0ef628cb4e8d533ba085bb3c8a173016bcdf

Ben stills (v19):
  1. 0:48 Explorer back — unfinished scalp holes / lamp banding / garbled cards → 06
  2. A PREDICTION — light bulbs dripping lava/fire → 08 / 08b
  3. 1:44 unfinished / pasted cards / blown lamp → 09b (and 09)
  4. FAMILY FIRST floating H/C/N/O flat 2D → 10
  5. overhead grid/flasks unfinished 2D → 11 / 11b

Start-frame hygiene ONLY (3D Flow DNA + lava/scalp/label heals).
NO paint on finished gallery mp4s. Do not I2V from the failed flat/lava stills.
"""
from __future__ import annotations

import json
import math
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

PROJ = Path(__file__).resolve().parents[1]
OUT = PROJ / "04_Generated-Clips/part04/refs/v20_start_frames"
QA = PROJ / "07_Edit-Project/_qa_part04_v20_prep"
META = OUT / "compose_meta.json"
PARENT_V19_SHA = "69d48f6e5fac419df5c23c17df5d0ef628cb4e8d533ba085bb3c8a173016bcdf"
W, H = 1920, 1080

RAW = PROJ / "04_Generated-Clips/part04/raw"
DNA = {
    "06": PROJ / "04_Generated-Clips/part04/refs/v10_start_frames/06_explorer_leaves_gap_start_v10.jpg",
    "08": RAW / "v12_fast/08_prediction_navigation_v12.mp4",
    "08b": RAW / "v12_fast/08b_navigation_walk_v12.mp4",
    "09": RAW / "v12_fast/08_prediction_navigation_v12.mp4",
    "09b": RAW / "v15_fast/11_publish_gaps_v15.mp4",
    "10": RAW / "v13_fast/05_columns_families_v13.mp4",
    "11": RAW / "v15_fast/11_publish_gaps_v15.mp4",
    "11b": RAW / "v15_fast/11b_wait_and_hunt_v15.mp4",
}
DNA_T = {
    "08": 1.0,
    "08b": 2.5,
    "09": 1.0,
    "09b": 1.2,
    "10": 2.5,
    "11": 1.2,
    "11b": 3.0,
}

REMINT = [
    "06_explorer_leaves_gap",
    "08_prediction_navigation",
    "08b_navigation_walk",
    "09_risk_bet",
    "09b_risk_hold",
    "10_family_before_weight",
    "11_publish_gaps",
    "11b_wait_and_hunt",
]


def _font(size: int):
    for path in (
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Supplemental/Georgia Bold.ttf",
        "/Library/Fonts/Arial Bold.ttf",
    ):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def extract_frame(src: Path, t: float, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    subprocess.check_call(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-ss", f"{t:.2f}", "-i", str(src), "-frames:v", "1", "-q:v", "2", str(dest),
        ]
    )
    return dest


def fit_cover(src: Path) -> Image.Image:
    im = Image.open(src).convert("RGB")
    sw, sh = im.size
    scale = max(W / sw, H / sh)
    nw, nh = int(sw * scale), int(sh * scale)
    im = im.resize((nw, nh), Image.Resampling.LANCZOS)
    left = (nw - W) // 2
    top = (nh - H) // 2
    return im.crop((left, top, left + W, top + H))


def is_drip_pixel(r: int, g: int, b: int) -> bool:
    """Hanging lava/fire goo — saturated orange against dark, not warm wood."""
    return r > 215 and g > 70 and g < 190 and b < 55 and (r - b) > 165


def inpaint_lava(im: Image.Image) -> Image.Image:
    """Replace small hanging lava drips only. Do not eat the lamp cone."""
    rgb = im.convert("RGB")
    w, h = rgb.size
    px = rgb.load()
    marked = []
    for y in range(int(h * 0.05), int(h * 0.72)):
        for x in range(w):
            r, g, b = px[x, y]
            if not is_drip_pixel(r, g, b):
                continue
            dark_n = 0
            for dx, dy in ((-4, 0), (4, 0), (0, -4), (0, 6), (-3, 5), (3, 5)):
                sx, sy = x + dx, y + dy
                if 0 <= sx < w and 0 <= sy < h:
                    sr, sg, sb = px[sx, sy]
                    if max(sr, sg, sb) < 70:
                        dark_n += 1
            if dark_n >= 2:
                marked.append((x, y))
    if len(marked) > 8000:
        print(f"  lava skip (too many candidates={len(marked)})", flush=True)
        return rgb
    healed = 0
    for x, y in marked:
        samples = []
        for rad in (6, 10, 16):
            for ang in range(0, 360, 45):
                sx = int(x + rad * math.cos(math.radians(ang)))
                sy = int(y + rad * math.sin(math.radians(ang)))
                if 0 <= sx < w and 0 <= sy < h:
                    sr, sg, sb = px[sx, sy]
                    if not is_drip_pixel(sr, sg, sb) and max(sr, sg, sb) > 40:
                        samples.append((sr, sg, sb))
            if len(samples) >= 4:
                break
        if samples:
            n = len(samples)
            px[x, y] = (
                sum(s[0] for s in samples) // n,
                sum(s[1] for s in samples) // n,
                sum(s[2] for s in samples) // n,
            )
            healed += 1
    print(f"  lava drip pixels healed={healed}", flush=True)
    return rgb


def heal_scalp_pits(im: Image.Image) -> Image.Image:
    """Fill compact dark circular pits on the crown only (hair-surrounded blobs)."""
    rgb = im.convert("RGB")
    w, h = rgb.size
    px = rgb.load()
    x0, x1 = int(w * 0.38), int(w * 0.62)
    y0, y1 = int(h * 0.16), int(h * 0.45)

    def is_hair(r: int, g: int, b: int) -> bool:
        return r > 90 and r >= g and (r - b) > 18 and g > 45 and max(r, g, b) > 95

    def is_pit(r: int, g: int, b: int) -> bool:
        mx = max(r, g, b)
        return mx < 108 and r < 125 and abs(r - g) < 42 and not is_hair(r, g, b)

    visited = set()
    filled = 0
    blobs = 0
    for y in range(y0, y1):
        for x in range(x0, x1):
            if (x, y) in visited:
                continue
            r, g, b = px[x, y]
            if not is_pit(r, g, b):
                continue
            stack = [(x, y)]
            visited.add((x, y))
            cells: list[tuple[int, int]] = []
            while stack:
                cx, cy = stack.pop()
                cells.append((cx, cy))
                for dx, dy in (
                    (1, 0), (-1, 0), (0, 1), (0, -1),
                    (1, 1), (-1, -1), (1, -1), (-1, 1),
                ):
                    nx, ny = cx + dx, cy + dy
                    if nx < x0 or nx >= x1 or ny < y0 or ny >= y1 or (nx, ny) in visited:
                        continue
                    nr, ng, nb = px[nx, ny]
                    if is_pit(nr, ng, nb):
                        visited.add((nx, ny))
                        stack.append((nx, ny))
            if not (8 <= len(cells) <= 1200):
                continue
            samples = []
            for cx, cy in cells:
                for rad in (8, 14, 22):
                    for ang in range(0, 360, 30):
                        sx = int(cx + rad * math.cos(math.radians(ang)))
                        sy = int(cy + rad * math.sin(math.radians(ang)))
                        if x0 <= sx < x1 and y0 <= sy < y1:
                            sr, sg, sb = px[sx, sy]
                            if is_hair(sr, sg, sb):
                                samples.append((sr, sg, sb))
            if len(samples) < 10:
                continue
            n = len(samples)
            fill = (
                sum(s[0] for s in samples) // n,
                sum(s[1] for s in samples) // n,
                sum(s[2] for s in samples) // n,
            )
            blobs += 1
            extra: list[tuple[int, int]] = []
            for cx, cy in cells:
                px[cx, cy] = fill
                filled += 1
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = cx + dx, cy + dy
                    if x0 <= nx < x1 and y0 <= ny < y1:
                        nr, ng, nb = px[nx, ny]
                        if is_pit(nr, ng, nb) or max(nr, ng, nb) < 88:
                            extra.append((nx, ny))
            for nx, ny in extra:
                px[nx, ny] = fill
                filled += 1
    print(f"  scalp blob-fill pixels={filled} blobs={blobs}", flush=True)
    return rgb


def densify_crown(im: Image.Image) -> Image.Image:
    rgb = im.convert("RGB")
    px = rgb.load()
    w, h = rgb.size
    x0, x1 = int(w * 0.28), int(w * 0.72)
    y0, y1 = int(h * 0.08), int(h * 0.48)
    for y in range(y0, y1):
        for x in range(x0, x1):
            r, g, b = px[x, y]
            if 45 < r < 160 and 25 < g < 120 and b < 100 and (r - b) > 12:
                px[x, y] = (
                    min(255, int(r * 1.05)),
                    min(255, int(g * 1.03)),
                    min(255, int(b * 1.02)),
                )
    return rgb


def smooth_lamp_glow(im: Image.Image) -> Image.Image:
    rgb = im.convert("RGB")
    warm = rgb.copy()
    px = warm.load()
    w, h = warm.size
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            if r > 150 and g > 100 and b < 140 and (r - b) > 40:
                continue
            px[x, y] = (0, 0, 0)
    soft = warm.filter(ImageFilter.GaussianBlur(10))
    bp = rgb.load()
    sp = soft.load()
    for y in range(h):
        for x in range(w):
            sr, sg, sb = sp[x, y]
            if sr + sg + sb < 40:
                continue
            r, g, b = bp[x, y]
            bp[x, y] = (
                int(0.78 * r + 0.22 * sr),
                int(0.78 * g + 0.22 * sg),
                int(0.82 * b + 0.18 * sb),
            )
    return rgb


def cover_corner_label(im: Image.Image) -> Image.Image:
    """Cover baked EMPTY SEATS overlay by tiling a neighbouring bookshelf patch."""
    rgb = im.convert("RGB")
    src = rgb.crop((int(W * 0.48), 16, int(W * 0.67), 16 + 148))
    dest_x = int(W * 0.68)
    while dest_x < W - 8:
        rgb.paste(src, (dest_x, 6))
        dest_x += src.size[0]
    return rgb


def cover_ghost_panel(im: Image.Image) -> Image.Image:
    """No-op — slab-paste created a ghost inset rectangle on v20 try."""
    return im.convert("RGB")


def paint_element_card(
    canvas: Image.Image,
    center: tuple[int, int],
    symbol: str,
    number: str,
    *,
    angle: float = 0.0,
    scale: float = 1.0,
) -> None:
    cw, ch = int(150 * scale), int(200 * scale)
    card = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    d = ImageDraw.Draw(card)
    d.rounded_rectangle((2, 2, cw - 3, ch - 3), radius=14, fill=(252, 248, 236, 255))
    d.rounded_rectangle((2, 2, cw - 3, ch - 3), radius=14, outline=(40, 32, 24, 240), width=3)
    f_sym = _font(max(40, int(72 * scale)))
    f_num = _font(max(24, int(40 * scale)))
    bb = d.textbbox((0, 0), symbol, font=f_sym)
    tw = bb[2] - bb[0]
    d.text(((cw - tw) / 2, ch * 0.18), symbol, fill=(24, 20, 16, 255), font=f_sym)
    bb2 = d.textbbox((0, 0), number, font=f_num)
    tw2 = bb2[2] - bb2[0]
    d.text(((cw - tw2) / 2, ch * 0.58), number, fill=(40, 34, 28, 255), font=f_num)
    if abs(angle) > 0.1:
        card = card.rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)
    cx, cy = center
    canvas.alpha_composite(card, (cx - card.size[0] // 2, cy - card.size[1] // 2))


def stamp_desk_cards(im: Image.Image, y_frac: float = 0.74) -> Image.Image:
    rgba = im.convert("RGBA")
    cover = Image.new("RGBA", rgba.size, (0, 0, 0, 0))
    cd = ImageDraw.Draw(cover)
    cd.rounded_rectangle(
        (int(W * 0.28), int(H * (y_frac - 0.16)), int(W * 0.80), int(H * (y_frac + 0.18))),
        radius=18,
        fill=(110, 78, 48, 210),
    )
    rgba = Image.alpha_composite(rgba, cover.filter(ImageFilter.GaussianBlur(0.8)))
    paint_element_card(rgba, (int(W * 0.36), int(H * y_frac)), "H", "1", angle=-6, scale=0.92)
    paint_element_card(rgba, (int(W * 0.48), int(H * y_frac - 0.01 * H)), "C", "12", angle=4, scale=0.95)
    paint_element_card(rgba, (int(W * 0.60), int(H * y_frac)), "N", "14", angle=-3, scale=0.95)
    paint_element_card(rgba, (int(W * 0.72), int(H * y_frac + 0.01 * H)), "O", "16", angle=7, scale=0.92)
    return rgba.convert("RGB")


def deghost_desk(im: Image.Image) -> Image.Image:
    rgb = im.convert("RGB")
    soft = rgb.filter(ImageFilter.GaussianBlur(0.7))
    sharp = ImageEnhance.Sharpness(rgb).enhance(1.12)
    return Image.blend(soft, sharp, 0.72)


def save_plate(im: Image.Image, pid: str) -> Path:
    dest = OUT / f"{pid}_start_v20.jpg"
    im = ImageEnhance.Sharpness(im).enhance(1.08)
    im.save(dest, quality=95)
    im.save(QA / f"start_{pid}.jpg", quality=92)
    print(f"wrote {dest.name}", flush=True)
    return dest


def prep_explorer() -> Path:
    src = DNA["06"]
    if not src.exists():
        raise SystemExit(f"missing explorer DNA {src}")
    im = fit_cover(src)
    im = cover_corner_label(im)
    im = heal_scalp_pits(im)
    im = densify_crown(im)
    return save_plate(im, "06_explorer_leaves_gap")


def prep_from_clip(
    pid: str,
    key: str,
    *,
    heal_lava: bool = False,
    stamp_cards: bool = False,
    y_frac: float = 0.78,
) -> Path:
    src = DNA[key]
    if not src.exists():
        raise SystemExit(f"missing DNA {src}")
    tmp = QA / f"_dna_{key}.jpg"
    if src.suffix.lower() in {".jpg", ".jpeg", ".png"}:
        im = fit_cover(src)
    else:
        extract_frame(src, DNA_T[key], tmp)
        im = fit_cover(tmp)
    if heal_lava:
        im = inpaint_lava(im)
    if stamp_cards:
        im = stamp_desk_cards(im, y_frac=y_frac)
    return save_plate(im, pid)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QA.mkdir(parents=True, exist_ok=True)
    meta = {
        "parent_v19_sha": PARENT_V19_SHA,
        "bible_main": "43d9405",
        "ben_fail_stills": {
            "01_explorer_t048": "06_explorer_leaves_gap",
            "02_prediction_lava": ["08_prediction_navigation", "08b_navigation_walk"],
            "03_t144_unfinished": ["09_risk_bet", "09b_risk_hold"],
            "04_family_first_2d": "10_family_before_weight",
            "05_publish_overhead_2d": ["11_publish_gaps", "11b_wait_and_hunt"],
        },
        "plates": {},
        "method": (
            "06=v10 3D back explorer + conservative scalp heal (no collage stamp); "
            "08/08b/09=v12 empty-chair 3D DNA + drip-only lava (NOT failed v19 still); "
            "09b/11/11b=v15 3D desk+moon (not flat overhead); "
            "10=v13 columns 3D desk DNA"
        ),
        "remint": REMINT,
        "keep_assemble": ["written cards ~40", "01-05/05b/07/07b locked"],
        "no_paint_on_mp4": True,
    }
    meta["plates"]["06_explorer_leaves_gap"] = str(prep_explorer())
    meta["plates"]["08_prediction_navigation"] = str(
        prep_from_clip("08_prediction_navigation", "08", heal_lava=True)
    )
    meta["plates"]["08b_navigation_walk"] = str(
        prep_from_clip("08b_navigation_walk", "08b", heal_lava=True)
    )
    meta["plates"]["09_risk_bet"] = str(
        prep_from_clip("09_risk_bet", "09", heal_lava=True)
    )
    meta["plates"]["09b_risk_hold"] = str(
        prep_from_clip("09b_risk_hold", "09b")
    )
    meta["plates"]["10_family_before_weight"] = str(
        prep_from_clip("10_family_before_weight", "10")
    )
    meta["plates"]["11_publish_gaps"] = str(
        prep_from_clip("11_publish_gaps", "11")
    )
    meta["plates"]["11b_wait_and_hunt"] = str(
        prep_from_clip("11b_wait_and_hunt", "11b")
    )
    META.write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta, indent=2), flush=True)
    print("PREP OK", flush=True)


if __name__ == "__main__":
    main()
