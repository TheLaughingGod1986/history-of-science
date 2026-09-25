#!/usr/bin/env python3
"""Prep Part 04 v15 I2V start frames — Ben FAIL remint (hair + CLEAN LIGHT + sharp late).

Parent FAIL: hos_002_part04_rough_v14.mp4
  sha256 fa62ab22d0f7cbd4f208e5200c9b8b471c23595237b4d7d2dd18e6f47dabad4f
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

PROJ = Path(__file__).resolve().parents[1]
OUT = PROJ / "04_Generated-Clips/part04/refs/v15_start_frames"
QA = PROJ / "07_Edit-Project/_qa_part04_v15_prep"
META = OUT / "compose_meta.json"

SHEET = PROJ / "04_Generated-Clips/part04/refs/v11_dna/character_sheet.jpg"
SHEET_CROWN = PROJ / "04_Generated-Clips/part04/refs/v09_start_frames/_sheet_head_crown.png"
START_06 = PROJ / "04_Generated-Clips/part04/refs/v11_start_frames/06_explorer_leaves_gap_start_v11.jpg"
OK_ABET = PROJ / "07_Edit-Project/_qa_part04_v14_refs/ok_abet_98.jpg"
OK_GLOW = PROJ / "07_Edit-Project/_qa_part04_v14_refs/ok_glow_102.jpg"
CLEAN_09B = PROJ / "04_Generated-Clips/part04/refs/v14_start_frames/09b_risk_hold_start_v14_clean_glow.jpg"
RAW_06 = PROJ / "04_Generated-Clips/part04/raw/v11_fast/06_explorer_leaves_gap_v11.mp4"
RAW_10 = PROJ / "04_Generated-Clips/part04/raw/v12_fast/10_family_before_weight_v12.mp4"
RAW_11 = PROJ / "04_Generated-Clips/part04/raw/v01_fast/11_publish_gaps_v01.mp4"
RAW_11B = PROJ / "04_Generated-Clips/part04/raw/v01_fast/11b_wait_and_hunt_v01.mp4"
CUT_V14 = PROJ / "09_Final-Export/hos_002_part04_rough_v14.mp4"


def extract(clip: Path, t: float, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-ss", f"{t:.3f}", "-i", str(clip),
            "-frames:v", "1", "-q:v", "2", str(dest),
        ],
        check=True,
    )


def scrub_lava(im: Image.Image) -> Image.Image:
    rgb = im.convert("RGB")
    w, h = rgb.size
    px = rgb.load()
    wood = rgb.crop((int(w * 0.40), int(h * 0.55), int(w * 0.62), int(h * 0.78)))
    wood = wood.resize((w, h), Image.Resampling.BILINEAR).filter(
        ImageFilter.GaussianBlur(8)
    )
    wp = wood.load()
    out = rgb.copy()
    op = out.load()
    for y in range(int(h * 0.08), int(h * 0.72)):
        for x in range(int(w * 0.02), int(w * 0.55)):
            r, g, b = px[x, y]
            lava = (
                r >= 200 and g >= 90 and b <= 90 and (r - b) >= 110 and (r - g) <= 90
            ) or (
                r >= 230 and g >= 140 and b <= 110 and (r - b) >= 100
            )
            in_bulb = y < int(h * 0.28) and x < int(w * 0.22) and r > 240 and g > 220
            if lava and not in_bulb:
                wr, wg, wb = wp[x, y]
                op[x, y] = (
                    int(0.25 * r + 0.75 * wr),
                    int(0.30 * g + 0.70 * wg),
                    int(0.35 * b + 0.65 * max(wb, 40)),
                )
    return out


def soft_panel_glow(im: Image.Image) -> Image.Image:
    rgb = im.convert("RGBA")
    w, h = rgb.size
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    x0, y0 = int(w * 0.42), int(h * 0.28)
    x1, y1 = int(w * 0.58), int(h * 0.48)
    for pad, alpha in ((18, 35), (10, 70), (0, 110)):
        d.rounded_rectangle(
            (x0 - pad, y0 - pad, x1 + pad, y1 + pad),
            radius=10 + pad // 3,
            outline=(255, 230, 170, alpha),
            width=3,
        )
    d.rounded_rectangle(
        (x0, y0, x1, y1),
        radius=8,
        fill=(255, 236, 180, 55),
        outline=(255, 240, 200, 160),
        width=2,
    )
    return Image.alpha_composite(rgb, overlay).convert("RGB")


def fill_explorer_crown(im: Image.Image) -> Image.Image:
    rgb = im.convert("RGBA")
    w, h = rgb.size
    if SHEET_CROWN.exists():
        crown = Image.open(SHEET_CROWN).convert("RGBA")
    else:
        sheet_im = Image.open(SHEET).convert("RGBA")
        sw, sh = sheet_im.size
        crown = sheet_im.crop(
            (int(sw * 0.08), int(sh * 0.02), int(sw * 0.30), int(sh * 0.18))
        )
    tw = int(w * 0.085)
    th = int(h * 0.075)
    crown_r = crown.resize((tw, th), Image.Resampling.LANCZOS)
    mask = Image.new("L", (tw, th), 0)
    md = ImageDraw.Draw(mask)
    md.ellipse((2, 2, tw - 3, th - 3), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(3))
    crown_r.putalpha(mask)
    x = int(w * 0.48) - tw // 2
    y = int(h * 0.30) - th // 2
    out = rgb.copy()
    out.alpha_composite(crown_r, (x, y))
    crown2 = crown_r.resize((int(tw * 0.92), int(th * 0.85)), Image.Resampling.LANCZOS)
    out.alpha_composite(crown2, (x + 4, y + 2))
    return out.convert("RGB")


def sharpen_mild(im: Image.Image) -> Image.Image:
    return ImageEnhance.Sharpness(im.convert("RGB")).enhance(1.35)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QA.mkdir(parents=True, exist_ok=True)
    meta: dict = {
        "plates": {},
        "parent_v14_sha": "fa62ab22d0f7cbd4f208e5200c9b8b471c23595237b4d7d2dd18e6f47dabad4f",
    }

    src06 = OUT / "_src_06.jpg"
    if START_06.exists():
        Image.open(START_06).convert("RGB").save(src06, quality=95)
    else:
        extract(RAW_06, 2.0, src06)
    im06 = scrub_lava(Image.open(src06))
    im06 = fill_explorer_crown(im06)
    im06 = sharpen_mild(im06)
    out06 = OUT / "06_explorer_leaves_gap_start_v15.jpg"
    im06.save(out06, quality=95)
    im06.save(QA / "start_06_crown_v15.jpg", quality=92)
    meta["plates"]["06_explorer_leaves_gap"] = str(out06)

    base09 = CLEAN_09B if CLEAN_09B.exists() else (OK_ABET if OK_ABET.exists() else OK_GLOW)
    im09 = scrub_lava(Image.open(base09))
    im09 = soft_panel_glow(im09)
    im09 = sharpen_mild(im09)
    out09 = OUT / "09b_risk_hold_start_v15.jpg"
    im09.save(out09, quality=95)
    im09.save(QA / "start_09b_clean_v15.jpg", quality=92)
    meta["plates"]["09b_risk_hold"] = str(out09)

    src10 = OUT / "_src_10.jpg"
    extract(RAW_10, 2.5, src10)
    im10 = scrub_lava(Image.open(src10))
    im10 = soft_panel_glow(im10)
    im10 = sharpen_mild(im10)
    out10 = OUT / "10_family_before_weight_start_v15.jpg"
    im10.save(out10, quality=95)
    meta["plates"]["10_family_before_weight"] = str(out10)

    src11 = OUT / "_src_11.jpg"
    extract(RAW_11, 1.5, src11)
    im11 = scrub_lava(Image.open(src11))
    im11 = sharpen_mild(im11)
    out11 = OUT / "11_publish_gaps_start_v15.jpg"
    im11.save(out11, quality=95)
    meta["plates"]["11_publish_gaps"] = str(out11)

    src11b = OUT / "_src_11b.jpg"
    extract(RAW_11B, 1.5, src11b)
    im11b = scrub_lava(Image.open(src11b))
    im11b = sharpen_mild(im11b)
    out11b = OUT / "11b_wait_and_hunt_start_v15.jpg"
    im11b.save(out11b, quality=95)
    meta["plates"]["11b_wait_and_hunt"] = str(out11b)

    if CUT_V14.exists():
        for t, name in ((47, "cut_t47"), (51, "cut_t51"), (105, "cut_t105"), (120, "cut_t120")):
            extract(CUT_V14, float(t), QA / f"{name}_parent.jpg")

    META.write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta, indent=2), flush=True)
    print("PREP OK", flush=True)


if __name__ == "__main__":
    main()
