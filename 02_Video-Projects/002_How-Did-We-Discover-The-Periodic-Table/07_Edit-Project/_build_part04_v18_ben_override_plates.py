#!/usr/bin/env python3
"""Build Part 04 v18 plates — single-exposure continuous motion (NO temporal-median).

Motion = brightness pulse + micro grain only.
NO crop-settle (v17 crop+sharpen rang as horizontal ghost doubles for Ben).
NO Image.composite of two full scene layers.
Verify ≥3 mid-plate frames for ghost before accept.
"""
from __future__ import annotations

import hashlib
import json
import math
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageChops, ImageEnhance, ImageFilter, ImageStat

PROJ = Path(__file__).resolve().parents[1]
STARTS = PROJ / "04_Generated-Clips/part04/refs/v18_start_frames"
RAW = PROJ / "04_Generated-Clips/part04/raw/v18_fast"
QA = PROJ / "07_Edit-Project/_qa_part04_v18_painted"
META = PROJ / "07_Edit-Project/part04_build_v18_painted_meta.json"
W, H = 1920, 1080
FPS = 24
DUR_S = 8.0
PLATES = [
    "06_explorer_leaves_gap",
    "10_family_before_weight",
    "11_publish_gaps",
    "11b_wait_and_hunt",
]


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


def ghost_peak(im: Image.Image) -> float:
    """Edge self-similarity at dx=4..14 — high peak ⇒ horizontal doubles."""
    e = im.convert("L").filter(ImageFilter.FIND_EDGES)
    w, h = e.size
    peaks = []
    for dx in range(4, 15):
        a = e.crop((0, 0, w - dx, h))
        b = e.crop((dx, 0, w, h))
        # similarity = inverse mean abs diff of edges
        d = ImageChops.difference(a, b)
        mean = ImageStat.Stat(d).mean[0]
        peaks.append(255.0 - mean)
    return max(peaks)


def animate_frame(base: Image.Image, i: int, n: int) -> Image.Image:
    """Opaque single-exposure — brightness only, never blend two scenes."""
    t = i / max(n - 1, 1)
    pulse = 1.0 + 0.010 * math.sin(t * math.pi * 2)
    frame = ImageEnhance.Brightness(base).enhance(pulse)
    # tiny grain (not a second exposure of props)
    if i % 2 == 0:
        grain = Image.effect_noise((W, H), 5).convert("L")
        grain_rgb = Image.merge("RGB", (grain, grain, grain))
        frame = Image.blend(frame, grain_rgb, 0.012)
    return frame


def build_plate(pid: str) -> dict:
    start = STARTS / f"{pid}_start_v18.jpg"
    if not start.exists():
        raise SystemExit(f"missing {start}")
    base = Image.open(start).convert("RGB").resize((W, H), Image.Resampling.LANCZOS)
    start_ghost = ghost_peak(base)
    if start_ghost > 252.5:
        print(f"WARN start ghost_peak={start_ghost:.2f} for {pid}", flush=True)
    dest = RAW / f"{pid}_v18.mp4"
    n = int(DUR_S * FPS)
    QA.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)
    sample_idxs = (12, 48, 96, 144, 180)
    sample_ghosts: list[float] = []

    with tempfile.TemporaryDirectory(prefix=f"hos_v18_{pid}_") as td:
        fout = Path(td) / "f"
        fout.mkdir()
        for i in range(n):
            fr = animate_frame(base, i, n)
            fr.save(fout / f"f_{i + 1:04d}.jpg", quality=94)
            if i in sample_idxs:
                fr.save(QA / f"{pid}_f{i:04d}.jpg", quality=92)
                g = ghost_peak(fr)
                sample_ghosts.append(g)
                print(f"  {pid} f{i:04d} ghost_peak={g:.2f}", flush=True)
        # self-FAIL if mid frames look as ghosty as Ben fail (~251.9)
        if any(g >= 251.6 for g in sample_ghosts):
            raise SystemExit(
                f"SELF-FAIL {pid}: mid-frame ghost_peak {sample_ghosts} ≥ 251.6 "
                "(Ben fail publish was ~251.9) — do not ship"
            )
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

    info = {
        "plate": pid,
        "path": str(dest),
        "sha256": sha256(dest),
        "bytes": dest.stat().st_size,
        "duration": probe(dest),
        "start_ghost_peak": start_ghost,
        "mid_ghost_peaks": sample_ghosts,
        "method": (
            "painted_single_exposure_v18 (brightness motion only; "
            "NO crop-settle; NO temporal-median; NO nested glow)"
        ),
    }
    print(json.dumps(info, indent=2), flush=True)
    return info


def main() -> None:
    summary = {"plates": [], "status": "running"}
    for pid in PLATES:
        summary["plates"].append(build_plate(pid))
        META.write_text(json.dumps(summary, indent=2) + "\n")
    summary["status"] = "done"
    META.write_text(json.dumps(summary, indent=2) + "\n")
    print("PAINTED BUILD OK", flush=True)


if __name__ == "__main__":
    main()
