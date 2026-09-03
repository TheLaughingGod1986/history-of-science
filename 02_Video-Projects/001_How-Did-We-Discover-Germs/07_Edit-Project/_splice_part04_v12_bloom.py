#!/usr/bin/env python3
"""Part 04 v12 — splice unused swan-neck take into 07_bloom_cloud.

No Flow. No T2V. Source is 01_question_mark_flask_v03 (same S-curve bottle
as the 0:02 keeper, unused in the assemble). Native 1× motion + a late
milky grade in the bulb only. No Ken Burns. No pill-germ overlay.
"""
from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
RAW = PROJ / "04_Generated-Clips/part04/raw/v01_fast_probe"
SRC = RAW / "01_question_mark_flask_v03.mp4"
DEST = RAW / "07_bloom_cloud_v12.mp4"
QA = RAW / "_qa_07_bloom_cloud_v12"
CLIP_USE = 7.50


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def ff(*args: str) -> None:
    subprocess.run(["ffmpeg", "-y", *args], check=True, capture_output=True)


def main() -> None:
    if not SRC.exists():
        raise SystemExit(f"STOP: missing splice source {SRC}")
    RAW.mkdir(parents=True, exist_ok=True)
    # Native 1×. No tracked disc (a fixed ellipse slides off the bulb).
    # Late global dulling so the amber reads muddier without swapping glass
    # or stamping pills from the v11 fail.
    ff(
        "-i", str(SRC),
        "-filter_complex",
        f"[0:v]trim=0:{CLIP_USE:.2f},setpts=PTS-STARTPTS,"
        "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,"
        "fps=24,format=yuv420p,"
        "eq=saturation=1.00:contrast=1.00,"
        "eq=saturation=0.86:contrast=0.96:brightness=-0.02:enable='gte(t,3.2)',"
        "eq=saturation=0.78:contrast=0.93:brightness=-0.035:enable='gte(t,5.4)',"
        "setsar=1[v]",
        "-map", "[v]",
        "-an",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-profile:v", "baseline", "-level", "3.1", "-bf", "0",
        "-preset", "fast", "-crf", "18",
        "-movflags", "+faststart",
        str(DEST),
    )
    QA.mkdir(parents=True, exist_ok=True)
    for t, name in ((0.04, "t000"), (1.00, "t100"), (4.00, "t400"), (7.20, "t720")):
        ff(
            "-ss", f"{t:.2f}", "-i", str(DEST),
            "-frames:v", "1", "-q:v", "3", str(QA / f"{name}.jpg"),
        )
    print(f"SAVED {DEST}", flush=True)
    print(f"SRC {SRC.name}", flush=True)
    print(f"SHA256 {sha256(DEST)}", flush=True)
    print(f"BYTES {DEST.stat().st_size}", flush=True)


if __name__ == "__main__":
    main()
