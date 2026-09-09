#!/usr/bin/env python3
"""Build Part 04 v15 remint plates from painted CLEAN stills + light motion.

09b: near-static painted CLEAN LIGHT master (no lava) + grain flicker
06: motion base + crown/lamp paint lock on upper head/lamp
10/11/11b: temporal median deghost + cream lamp scrub
"""
from __future__ import annotations

import hashlib
import json
import math
import random
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter

PROJ = Path(__file__).resolve().parents[1]
RAW_OUT = PROJ / "04_Generated-Clips/part04/raw/v15_fast"
QA = PROJ / "07_Edit-Project/_qa_part04_v15_hard"
STARTS = PROJ / "04_Generated-Clips/part04/refs/v15_start_frames"
PAINT_09B = STARTS / "09b_risk_hold_start_v15_painted_clean.jpg"
PAINT_06 = STARTS / "06_explorer_leaves_gap_start_v15_painted.jpg"
SHEET = STARTS / "character_sheet.jpg"
if not SHEET.exists():
    SHEET = PROJ / "04_Generated-Clips/part04/refs/v11_dna/character_sheet.jpg"

SOURCES = {
    "06_explorer_leaves_gap": PROJ
    / "04_Generated-Clips/part04/raw/v11_fast/06_explorer_leaves_gap_v11.mp4",
    "09b_risk_hold": PROJ / "04_Generated-Clips/part04/raw/v14_fast/09b_risk_hold_v14.mp4",
    "10_family_before_weight": PROJ
    / "04_Generated-Clips/part04/raw/v12_fast/10_family_before_weight_v12.mp4",
    "11_publish_gaps": PROJ / "04_Generated-Clips/part04/raw/v01_fast/11_publish_gaps_v01.mp4",
    "11b_wait_and_hunt": PROJ
    / "04_Generated-Clips/part04/raw/v01_fast/11b_wait_and_hunt_v01.mp4",
}
W, H = 1920, 1080
FPS = 24
DUR_S = 8.0


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def is_lava(r: int, g: int, b: int) -> bool:
    if r < 170:
        return False
    if r >= 190 and g >= 70 and b <= 115 and (r - b) >= 85:
        return True
    if r >= 205 and g >= 130 and b <= 145 and (r - b) >= 70 and (r + g) > 350:
        return True
    return False


def cream_scrub(im: Image.Image) -> Image.Image:
    rgb = im.convert("RGB")
    w, h = rgb.size
    px = rgb.load()
    cream = (246, 232, 205)
    for y in range(int(h * 0.08), int(h * 0.68)):
        for x in range(0, int(w * 0.48)):
            r, g, b = px[x, y]
            if y < int(h * 0.28) and x < int(w * 0.22) and r > 245 and g > 235 and b > 200:
                continue
            if is_lava(r, g, b) or (r > 205 and g > 145 and b < 145 and (r - b) > 75):
                t = 0.78
                px[x, y] = (
                    int((1 - t) * r + t * cream[0]),
                    int((1 - t) * g + t * cream[1]),
                    int((1 - t) * b + t * cream[2]),
                )
    return rgb


def soft_panel(im: Image.Image) -> Image.Image:
    rgba = im.convert("RGBA")
    w, h = rgba.size
    ov = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    x0, y0, x1, y1 = int(w * 0.42), int(h * 0.27), int(w * 0.58), int(h * 0.46)
    for pad, a in ((16, 35), (6, 60), (0, 82)):
        d.rounded_rectangle(
            (x0 - pad, y0 - pad, x1 + pad, y1 + pad),
            radius=12,
            fill=(255, 244, 220, a),
        )
    ov = ov.filter(ImageFilter.GaussianBlur(1.5))
    return Image.alpha_composite(rgba, ov).convert("RGB")


def crown_lock(im: Image.Image, sheet: Image.Image) -> Image.Image:
    rgb = cream_scrub(im).convert("RGBA")
    w, h = rgb.size
    sw, sh = sheet.size
    hair = sheet.crop((int(sw * 0.13), int(sh * 0.015), int(sw * 0.27), int(sh * 0.12)))
    hw, hh = int(w * 0.12), int(h * 0.11)
    hair = hair.resize((hw, hh), Image.Resampling.LANCZOS)
    hair = ImageEnhance.Color(hair).enhance(1.05)
    hair = ImageEnhance.Brightness(hair).enhance(1.04)
    mask = Image.new("L", (hw, hh), 0)
    ImageDraw.Draw(mask).ellipse((3, 3, hw - 4, hh - 4), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(5))
    hair.putalpha(mask)
    x = int(w * 0.505) - hw // 2
    y = int(h * 0.248)
    out = rgb.copy()
    out.alpha_composite(hair, (x, y))
    # second denser tuft pass with chestnut ellipses matching sheet
    tuft = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(tuft)
    rng = random.Random(3)
    colors = [(130, 78, 45), (110, 64, 36), (150, 92, 55), (95, 55, 30), (140, 85, 50)]
    cx, cy = int(w * 0.505), int(h * 0.295)
    for _ in range(260):
        ang = rng.uniform(0, 2 * math.pi)
        rad = rng.uniform(0, 1) ** 0.5
        xx = cx + int(math.cos(ang) * hw * 0.42 * rad)
        yy = cy + int(math.sin(ang) * hh * 0.38 * rad)
        col = colors[rng.randrange(len(colors))]
        r0 = rng.randint(2, 5)
        d.ellipse((xx - r0, yy - r0, xx + r0, yy + r0), fill=(*col, 210))
    tmask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(tmask).ellipse(
        (cx - hw // 2, cy - hh // 2, cx + hw // 2, cy + hh // 2), fill=255
    )
    tmask = tmask.filter(ImageFilter.GaussianBlur(4))
    tuft.putalpha(Image.composite(tuft.split()[-1], Image.new("L", (w, h), 0), tmask))
    out = Image.alpha_composite(out, tuft)
    return out.convert("RGB")


def encode_frames(frames_dir: Path, audio_src: Path, dest: Path) -> None:
    tmp = dest.with_suffix(".tmp.mp4")
    subprocess.check_call(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-framerate", str(FPS), "-i", str(frames_dir / "f_%04d.jpg"),
            "-i", str(audio_src),
            "-map", "0:v", "-map", "1:a?",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "17",
            "-preset", "medium", "-c:a", "aac", "-b:a", "192k",
            "-shortest", str(tmp),
        ]
    )
    shutil.move(str(tmp), str(dest))


def build_09b() -> dict:
    assert PAINT_09B.exists(), PAINT_09B
    clean = soft_panel(cream_scrub(Image.open(PAINT_09B))).resize((W, H), Image.Resampling.LANCZOS)
    n = int(DUR_S * FPS)
    with tempfile.TemporaryDirectory(prefix="hos_v15_09b_") as td:
        fout = Path(td) / "out"
        fout.mkdir()
        for i in range(n):
            frame = clean.copy()
            # tiny lamp flicker
            if i % 5 == 0:
                frame = frame.point(lambda p: min(255, int(p * 1.008)))
            elif i % 5 == 2:
                frame = frame.point(lambda p: max(0, int(p * 0.995)))
            # film grain
            grain = Image.effect_noise((W, H), 8).convert("L")
            g_rgb = Image.merge("RGB", (grain, grain, grain))
            frame = Image.blend(frame, g_rgb, 0.035)
            frame.save(fout / f"f_{i+1:04d}.jpg", quality=95)
        dest = RAW_OUT / "09b_risk_hold_v15.mp4"
        RAW_OUT.mkdir(parents=True, exist_ok=True)
        encode_frames(fout, SOURCES["09b_risk_hold"], dest)
    return {"plate": "09b_risk_hold", "out": str(dest), "sha256": sha256(dest), "method": "painted_clean_static"}


def build_06() -> dict:
    src = SOURCES["06_explorer_leaves_gap"]
    sheet = Image.open(SHEET).convert("RGBA")
    with tempfile.TemporaryDirectory(prefix="hos_v15_06_") as td:
        tdir = Path(td)
        fin, fout = tdir / "in", tdir / "out"
        fin.mkdir(); fout.mkdir()
        subprocess.check_call(
            [
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-i", str(src), "-vf", f"fps={FPS},scale={W}:{H}:flags=lanczos",
                str(fin / "f_%04d.jpg"),
            ]
        )
        frames = sorted(fin.glob("f_*.jpg"))
        # head/lamp lock mask
        mask = Image.new("L", (W, H), 0)
        d = ImageDraw.Draw(mask)
        d.ellipse((int(W * 0.43), int(H * 0.20), int(W * 0.60), int(H * 0.40)), fill=255)
        d.rectangle((0, 0, int(W * 0.30), int(H * 0.55)), fill=255)
        mask = mask.filter(ImageFilter.GaussianBlur(18))
        painted = crown_lock(Image.open(PAINT_06 if PAINT_06.exists() else frames[0]), sheet)
        painted = cream_scrub(painted)
        for i, fp in enumerate(frames):
            motion = Image.open(fp).convert("RGB")
            locked = crown_lock(motion, sheet)
            locked = cream_scrub(locked)
            # prefer painted crown/lamp DNA
            frame = Image.composite(painted, locked, mask)
            # keep lower body motion
            body_mask = Image.new("L", (W, H), 255)
            ImageDraw.Draw(body_mask).ellipse(
                (int(W * 0.43), int(H * 0.20), int(W * 0.60), int(H * 0.40)), fill=0
            )
            ImageDraw.Draw(body_mask).rectangle((0, 0, int(W * 0.30), int(H * 0.55)), fill=0)
            body_mask = body_mask.filter(ImageFilter.GaussianBlur(14))
            frame = Image.composite(locked, motion, ImageChops.invert(body_mask))
            # re-apply crown/lamp lock on top
            frame = Image.composite(painted, frame, mask)
            frame = cream_scrub(frame)
            frame.save(fout / fp.name, quality=95)
            if i % 40 == 0:
                print(f"  06 frame {i}/{len(frames)}", flush=True)
        dest = RAW_OUT / "06_explorer_leaves_gap_v15.mp4"
        encode_frames(fout, src, dest)
    return {"plate": "06_explorer_leaves_gap", "out": str(dest), "sha256": sha256(dest), "method": "crown_lamp_lock"}


def temporal_median_frame(bufs: list[Image.Image]) -> Image.Image:
    # cheap median via blend stack (approx) — enough to kill ghost doubles
    acc = bufs[0].convert("RGB")
    for im in bufs[1:]:
        acc = Image.blend(acc, im.convert("RGB"), 0.5)
    # then unsharp
    return ImageEnhance.Sharpness(acc).enhance(1.6)


def build_late(pid: str) -> dict:
    src = SOURCES[pid]
    with tempfile.TemporaryDirectory(prefix=f"hos_v15_{pid}_") as td:
        tdir = Path(td)
        fin, fout = tdir / "in", tdir / "out"
        fin.mkdir(); fout.mkdir()
        subprocess.check_call(
            [
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-i", str(src), "-vf", f"fps={FPS},scale={W}:{H}:flags=lanczos",
                str(fin / "f_%04d.jpg"),
            ]
        )
        frames = sorted(fin.glob("f_*.jpg"))
        loaded = [Image.open(fp).convert("RGB") for fp in frames]
        for i, motion in enumerate(loaded):
            lo = max(0, i - 2)
            hi = min(len(loaded), i + 3)
            med = temporal_median_frame(loaded[lo:hi])
            # keep center sharp-ish, prefer median on right ghost zone
            mask = Image.new("L", (W, H), 0)
            ImageDraw.Draw(mask).rectangle([int(W * 0.50), 0, W, H], fill=255)
            mask = mask.filter(ImageFilter.GaussianBlur(16))
            frame = Image.composite(med, motion, mask)
            frame = cream_scrub(frame)
            if pid.startswith("10"):
                frame = soft_panel(frame)
            frame = ImageEnhance.Sharpness(frame).enhance(1.35)
            frame.save(fout / f"f_{i+1:04d}.jpg", quality=95)
            if i % 40 == 0:
                print(f"  {pid} frame {i}/{len(frames)}", flush=True)
        dest = RAW_OUT / f"{pid}_v15.mp4"
        encode_frames(fout, src, dest)
    return {"plate": pid, "out": str(dest), "sha256": sha256(dest), "method": "median_deghost_cream"}


def main() -> None:
    RAW_OUT.mkdir(parents=True, exist_ok=True)
    QA.mkdir(parents=True, exist_ok=True)
    # archive prior v15
    rejected = RAW_OUT / "_rejected"
    rejected.mkdir(exist_ok=True)
    for pid in SOURCES:
        old = RAW_OUT / f"{pid}_v15.mp4"
        if old.exists():
            shutil.move(str(old), str(rejected / f"{pid}_v15_pre_paint_{old.stat().st_mtime_ns}.mp4"))

    results = []
    print("=== 09b painted clean static ===", flush=True)
    results.append(build_09b())
    print("=== 06 crown/lamp lock ===", flush=True)
    results.append(build_06())
    for pid in ("10_family_before_weight", "11_publish_gaps", "11b_wait_and_hunt"):
        print(f"=== {pid} median deghost ===", flush=True)
        results.append(build_late(pid))

    # QA stills
    for r in results:
        pid = r["plate"]
        qdir = QA / pid
        qdir.mkdir(parents=True, exist_ok=True)
        dest = Path(r["out"])
        for t in (0.5, 2.0, 4.0, 6.0, 7.5):
            subprocess.check_call(
                [
                    "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                    "-ss", str(t), "-i", str(dest), "-frames:v", "1",
                    str(qdir / f"t{t:.1f}.jpg"),
                ]
            )
        r["bytes"] = dest.stat().st_size
        print(json.dumps(r), flush=True)

    summary = {"results": results, "status": "PAINTED_V15_PLATES — no PASS"}
    (QA / "paint_build_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print("PLATE BUILD OK", flush=True)


if __name__ == "__main__":
    main()
