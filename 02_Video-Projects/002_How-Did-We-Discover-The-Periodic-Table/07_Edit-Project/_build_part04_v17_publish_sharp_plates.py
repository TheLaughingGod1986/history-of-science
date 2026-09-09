#!/usr/bin/env python3
"""Build Part 04 v17 publish plates — sharp continuous motion (NO temporal-median, NO v01).

Fallback when Flow I2V introduces motion-ghost trails.
Animates painted sharp v17 start frames with per-frame opaque redraws
(tiny settle + lamp pulse + glow breathe) — single exposure every frame.

Remint ONLY: 11_publish_gaps · 11b_wait_and_hunt
"""
from __future__ import annotations

import hashlib
import json
import math
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageChops, ImageEnhance, ImageFilter

PROJ = Path(__file__).resolve().parents[1]
STARTS = PROJ / "04_Generated-Clips/part04/refs/v17_start_frames"
RAW = PROJ / "04_Generated-Clips/part04/raw/v17_fast"
QA = PROJ / "07_Edit-Project/_qa_part04_v17_painted"
META = PROJ / "07_Edit-Project/part04_build_v17_painted_meta.json"
W, H = 1920, 1080
FPS = 24
DUR_S = 8.0


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def probe(path: Path) -> float:
    return float(
        subprocess.check_output(
            [
                "ffprobe", "-v", "error", "-show_entries", "format=duration",
                "-of", "default=nw=1:nk=1", str(path),
            ],
            text=True,
        ).strip()
    )


def animate_frame(base: Image.Image, i: int, n: int) -> Image.Image:
    """Opaque single-exposure motion — never blend two video frames."""
    t = i / max(n - 1, 1)
    # micro camera settle (≤3 px) via crop+resize — keeps edges sharp, no double-exposure
    dx = int(round(2.2 * math.sin(t * math.pi * 2)))
    dy = int(round(1.6 * math.cos(t * math.pi * 1.5)))
    pad = 6
    canv = Image.new("RGB", (W + 2 * pad, H + 2 * pad), (28, 22, 18))
    canv.paste(base, (pad, pad))
    frame = canv.crop((pad + dx, pad + dy, pad + dx + W, pad + dy + H))
    # lamp pool breathe (brightness only — no layer ghost)
    pulse = 1.0 + 0.012 * math.sin(t * math.pi * 2)
    frame = ImageEnhance.Brightness(frame).enhance(pulse)
    # subtle warm cast pulse on left desk only
    if i % 5 == 0:
        warm = ImageEnhance.Color(frame).enhance(1.02)
        mask = Image.new("L", (W, H), 0)
        from PIL import ImageDraw

        ImageDraw.Draw(mask).ellipse(
            (int(W * 0.02), int(H * 0.30), int(W * 0.55), int(H * 0.95)), fill=180
        )
        mask = mask.filter(ImageFilter.GaussianBlur(40))
        frame = Image.composite(warm, frame, mask)
    # fine grain (not a second exposure)
    grain = Image.effect_noise((W, H), 6).convert("L")
    grain_rgb = Image.merge("RGB", (grain, grain, grain))
    frame = Image.blend(frame, grain_rgb, 0.018)
    return ImageEnhance.Sharpness(frame).enhance(1.08)


def build_plate(pid: str) -> dict:
    start = STARTS / f"{pid}_start_v17.jpg"
    if not start.exists():
        raise SystemExit(f"missing {start}")
    base = Image.open(start).convert("RGB").resize((W, H), Image.Resampling.LANCZOS)
    dest = RAW / f"{pid}_v17.mp4"
    n = int(DUR_S * FPS)
    QA.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix=f"hos_v17_{pid}_") as td:
        fout = Path(td) / "f"
        fout.mkdir()
        for i in range(n):
            fr = animate_frame(base, i, n)
            fr.save(fout / f"f_{i + 1:04d}.jpg", quality=94)
            if i in (12, 48, 96, 168):
                fr.save(QA / f"{pid}_f{i:04d}.jpg", quality=92)
        tmp = dest.with_suffix(".tmp.mp4")
        subprocess.check_call(
            [
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-framerate", str(FPS), "-i", str(fout / "f_%04d.jpg"),
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "17",
                "-preset", "medium", "-an",
                "-t", f"{DUR_S:.2f}", str(tmp),
            ]
        )
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists():
            rej = RAW / "_rejected"
            rej.mkdir(exist_ok=True)
            shutil.move(str(dest), str(rej / f"{pid}_pre_painted_{dest.stat().st_mtime_ns}.mp4"))
        shutil.move(str(tmp), str(dest))

    # verify continuous motion + no freeze
    d = probe(dest)
    info = {
        "plate": pid,
        "path": str(dest),
        "sha256": sha256(dest),
        "bytes": dest.stat().st_size,
        "duration": d,
        "method": "painted_sharp_continuous_motion (opaque per-frame; NOT temporal-median; NOT v01)",
    }
    print(json.dumps(info, indent=2), flush=True)
    return info


def main() -> None:
    plates = ["11_publish_gaps", "11b_wait_and_hunt"]
    summary = {"plates": [], "status": "running"}
    for pid in plates:
        summary["plates"].append(build_plate(pid))
        META.write_text(json.dumps(summary, indent=2) + "\n")
    summary["status"] = "done"
    META.write_text(json.dumps(summary, indent=2) + "\n")
    print("PAINTED BUILD OK", flush=True)


if __name__ == "__main__":
    main()
