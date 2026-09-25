#!/usr/bin/env python3
"""Part 04 v15 Ben-FAIL scrub compose — hair crown + CLEAN LIGHT + sharp late desks.

Applies frame-level fixes when Flow remints are pending / rejected:
  - 06: lock finished sheet crown onto mid-scalp; scrub lamp lava
  - 09b: lock lamp+chair upper to clean start; scrub lava; keep desk card motion
  - 10/11/11b: scrub lava; mild sharpen; light ghost damp on right edge

Outputs under raw/v15_fast/*.mp4
"""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

PROJ = Path(__file__).resolve().parents[1]
RAW_OUT = PROJ / "04_Generated-Clips/part04/raw/v15_fast"
QA = PROJ / "07_Edit-Project/_qa_part04_v15_scrub"
STARTS = PROJ / "04_Generated-Clips/part04/refs/v15_start_frames"
SHEET_CROWN = PROJ / "04_Generated-Clips/part04/refs/v09_start_frames/_sheet_head_crown.png"
SHEET = PROJ / "04_Generated-Clips/part04/refs/v11_dna/character_sheet.jpg"

SOURCES = {
    "06_explorer_leaves_gap": PROJ / "04_Generated-Clips/part04/raw/v11_fast/06_explorer_leaves_gap_v11.mp4",
    "09b_risk_hold": PROJ / "04_Generated-Clips/part04/raw/v14_fast/09b_risk_hold_v14.mp4",
    "10_family_before_weight": PROJ / "04_Generated-Clips/part04/raw/v12_fast/10_family_before_weight_v12.mp4",
    "11_publish_gaps": PROJ / "04_Generated-Clips/part04/raw/v01_fast/11_publish_gaps_v01.mp4",
    "11b_wait_and_hunt": PROJ / "04_Generated-Clips/part04/raw/v01_fast/11b_wait_and_hunt_v01.mp4",
}
START_MAP = {
    "06_explorer_leaves_gap": STARTS / "06_explorer_leaves_gap_start_v15.jpg",
    "09b_risk_hold": STARTS / "09b_risk_hold_start_v15.jpg",
    "10_family_before_weight": STARTS / "10_family_before_weight_start_v15.jpg",
    "11_publish_gaps": STARTS / "11_publish_gaps_start_v15.jpg",
    "11b_wait_and_hunt": STARTS / "11b_wait_and_hunt_start_v15.jpg",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def scrub_lava(im: Image.Image) -> Image.Image:
    rgb = im.convert("RGB")
    w, h = rgb.size
    px = rgb.load()
    wood = rgb.crop((int(w * 0.40), int(h * 0.55), int(w * 0.62), int(h * 0.78)))
    wood = wood.resize((w, h), Image.Resampling.BILINEAR).filter(ImageFilter.GaussianBlur(8))
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


def crown_overlay(base: Image.Image) -> Image.Image:
    rgb = base.convert("RGBA")
    w, h = rgb.size
    if SHEET_CROWN.exists():
        crown = Image.open(SHEET_CROWN).convert("RGBA")
    else:
        sheet_im = Image.open(SHEET).convert("RGBA")
        sw, sh = sheet_im.size
        crown = sheet_im.crop((int(sw * 0.08), int(sh * 0.02), int(sw * 0.30), int(sh * 0.18)))
    tw, th = int(w * 0.085), int(h * 0.075)
    crown_r = crown.resize((tw, th), Image.Resampling.LANCZOS)
    mask = Image.new("L", (tw, th), 0)
    ImageDraw.Draw(mask).ellipse((2, 2, tw - 3, th - 3), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(3))
    crown_r.putalpha(mask)
    x = int(w * 0.48) - tw // 2
    y = int(h * 0.30) - th // 2
    out = rgb.copy()
    out.alpha_composite(crown_r, (x, y))
    crown2 = crown_r.resize((int(tw * 0.92), int(th * 0.85)), Image.Resampling.LANCZOS)
    out.alpha_composite(crown2, (x + 4, y + 2))
    return out.convert("RGB")


def lamp_chair_mask(w: int, h: int) -> Image.Image:
    """255 = use clean start (lamp + chair upper); 0 = motion desk."""
    mask = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(mask)
    # Left lamp column
    d.rectangle([0, 0, int(w * 0.28), int(h * 0.62)], fill=255)
    # Upper chair / shelves
    d.rectangle([0, 0, w, int(h * 0.48)], fill=255)
    # Soft falloff into desk
    band = int(h * 0.16)
    y0 = int(h * 0.48)
    for i in range(band):
        a = int(255 * (1.0 - i / max(1, band - 1)))
        d.rectangle([0, y0 + i, w, y0 + i + 1], fill=max(mask.getpixel((w // 2, y0 + i)), a))
    return mask.filter(ImageFilter.GaussianBlur(18))


def sharpen(im: Image.Image, amount: float = 1.25) -> Image.Image:
    return ImageEnhance.Sharpness(im.convert("RGB")).enhance(amount)


def damp_right_ghost(im: Image.Image) -> Image.Image:
    """Mild local contrast restore on right third to fight mush/ghost."""
    rgb = im.convert("RGB")
    w, h = rgb.size
    right = rgb.crop((int(w * 0.55), 0, w, h))
    right = ImageEnhance.Sharpness(right).enhance(1.55)
    right = ImageEnhance.Contrast(right).enhance(1.08)
    out = rgb.copy()
    out.paste(right, (int(w * 0.55), 0))
    # Feather seam
    seam = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(seam)
    d.rectangle([int(w * 0.55), 0, w, h], fill=255)
    seam = seam.filter(ImageFilter.GaussianBlur(10))
    return Image.composite(out, rgb, seam)


def process_plate(pid: str) -> dict:
    src = SOURCES[pid]
    start = START_MAP[pid]
    if not src.exists():
        raise SystemExit(f"missing source {src}")
    if not start.exists():
        raise SystemExit(f"missing start {start}")
    dest = RAW_OUT / f"{pid}_v15.mp4"
    RAW_OUT.mkdir(parents=True, exist_ok=True)
    QA.mkdir(parents=True, exist_ok=True)
    clean = Image.open(start).convert("RGB").resize((1920, 1080), Image.Resampling.LANCZOS)

    with tempfile.TemporaryDirectory(prefix=f"hos_v15_{pid}_") as td:
        tdir = Path(td)
        fin = tdir / "in"
        fout = tdir / "out"
        fin.mkdir()
        fout.mkdir()
        subprocess.check_call(
            [
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-i", str(src),
                "-vf", "fps=24,scale=1920:1080:flags=lanczos",
                str(fin / "f_%04d.jpg"),
            ]
        )
        frames = sorted(fin.glob("f_*.jpg"))
        if not frames:
            raise SystemExit(f"no frames from {src}")
        mask = lamp_chair_mask(1920, 1080) if pid in {"09b_risk_hold", "10_family_before_weight"} else None
        for i, fp in enumerate(frames):
            motion = Image.open(fp).convert("RGB")
            if motion.size != (1920, 1080):
                motion = motion.resize((1920, 1080), Image.Resampling.LANCZOS)
            if mask is not None:
                # slight lamp flicker on clean lock
                if i % 5 == 0:
                    base = clean.point(lambda p: min(255, int(p * 1.006)))
                elif i % 5 == 2:
                    base = clean.point(lambda p: max(0, int(p * 0.996)))
                else:
                    base = clean
                frame = Image.composite(base, motion, mask)
            else:
                frame = motion
            frame = scrub_lava(frame)
            if pid == "06_explorer_leaves_gap":
                frame = crown_overlay(frame)
            if pid in {"11_publish_gaps", "11b_wait_and_hunt", "10_family_before_weight"}:
                frame = damp_right_ghost(frame)
                frame = sharpen(frame, 1.35)
            else:
                frame = sharpen(frame, 1.18)
            frame.save(fout / fp.name, quality=95)

        tmp = tdir / "out.mp4"
        subprocess.check_call(
            [
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-framerate", "24", "-i", str(fout / "f_%04d.jpg"),
                "-i", str(src),
                "-map", "0:v", "-map", "1:a?",
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
                "-preset", "medium", "-c:a", "aac", "-b:a", "192k",
                "-shortest", str(tmp),
            ]
        )
        shutil.copy2(tmp, dest)

    # QA stills
    qdir = QA / pid
    qdir.mkdir(parents=True, exist_ok=True)
    for t in (0.5, 2.0, 4.0, 6.0, 7.5):
        subprocess.check_call(
            [
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-ss", str(t), "-i", str(dest), "-frames:v", "1",
                str(qdir / f"t{t:.1f}.jpg"),
            ]
        )
    info = {
        "plate": pid,
        "src": str(src),
        "out": str(dest),
        "sha256": sha256(dest),
        "bytes": dest.stat().st_size,
    }
    (qdir / "meta.json").write_text(json.dumps(info, indent=2) + "\n")
    print(json.dumps(info), flush=True)
    return info


def main() -> None:
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*", default=list(SOURCES.keys()))
    args = ap.parse_args()
    results = []
    for pid in args.only:
        if pid not in SOURCES:
            raise SystemExit(f"unknown plate {pid}")
        print(f"=== scrub {pid} ===", flush=True)
        results.append(process_plate(pid))
    summary = {"results": results}
    (QA / "scrub_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print("SCRUB OK", flush=True)


if __name__ == "__main__":
    main()
