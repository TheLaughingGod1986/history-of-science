#!/usr/bin/env python3
"""Part 04 v18 — break the v01 desk-CU double. Edit-only. No Flow.

KEEP 07_bloom_cloud_v13 (0:43–0:49 living v06).
KEEP 09_sceptics_watch_v17 (1:01 opposite-side arm).
KEEP 05_tip_the_trap_v17 (t32 v01 window).

REPLACE 08_passengers (t54) — same v01 desk CU as t32.
New plate: unused living v03 at 1×, later window, no flip, no tighter crop.
"""
from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
RAW = PROJ / "04_Generated-Clips/part04/raw/v01_fast_probe"
LIVE03 = RAW / "01_question_mark_flask_v03.mp4"
HOLD07 = RAW / "07_bloom_cloud_v13.mp4"
HOLD09 = RAW / "09_sceptics_watch_v17.mp4"
HOLD05 = RAW / "05_tip_the_trap_v17.mp4"
DEST08 = RAW / "08_passengers_v18.mp4"
CLIP_USE = 7.50
FPS = 24
STILL_FIRST = 2.0
STILL_MEAN = 1.4


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def probe_dur(p: Path) -> float:
    r = subprocess.run(
        [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(p),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(r.stdout.strip())


def ff(*args: str) -> None:
    subprocess.run(["ffmpeg", "-y", *args], check=True, capture_output=True)


def gray(p: Path, t: float) -> bytes:
    return subprocess.check_output(
        [
            "ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(p),
            "-frames:v", "1", "-vf", "scale=320:180,format=gray",
            "-f", "rawvideo", "-pix_fmt", "gray", "pipe:1",
        ]
    )


def mad(a: bytes, b: bytes) -> float:
    n = min(len(a), len(b))
    if n == 0:
        return 0.0
    return sum(abs(a[i] - b[i]) for i in range(n)) / n


def motion_ok(p: Path) -> tuple[float, float]:
    first = mad(gray(p, 0.04), gray(p, 1.00))
    diffs = [
        mad(gray(p, t), gray(p, t + 0.50))
        for t in (0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0)
    ]
    return first, sum(diffs) / len(diffs)


def main() -> None:
    for p, tag in ((HOLD07, "07 KEEP"), (HOLD09, "09 KEEP"), (HOLD05, "05 t32 KEEP")):
        if not p.exists() or p.stat().st_size < 400_000:
            raise SystemExit(f"STOP: missing {tag} {p}")
        print(f"{tag} {p.name} sha256={sha256(p)}", flush=True)
    if not LIVE03.exists():
        raise SystemExit(f"STOP: missing living take {LIVE03}")
    src_dur = probe_dur(LIVE03)
    start = 0.50
    if start + CLIP_USE > src_dur + 0.02:
        raise SystemExit(
            f"STOP: v03 window {start:.2f}+{CLIP_USE:.2f} exceeds {src_dur:.2f}"
        )
    filt = (
        f"[0:v]trim={start:.2f}:{start + CLIP_USE:.2f},setpts=PTS-STARTPTS,"
        "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,"
        f"fps={FPS},format=yuv420p,setsar=1[v]"
    )
    ff(
        "-i", str(LIVE03),
        "-filter_complex", filt,
        "-map", "[v]", "-an",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-profile:v", "baseline", "-level", "3.1", "-bf", "0",
        "-preset", "fast", "-crf", "18",
        "-movflags", "+faststart",
        str(DEST08),
    )
    first, mean = motion_ok(DEST08)
    print(
        f"  {DEST08.name} src={LIVE03.name} start={start:.2f} "
        f"first={first:.2f} mean={mean:.2f}",
        flush=True,
    )
    if first < STILL_FIRST or mean < STILL_MEAN:
        DEST08.unlink(missing_ok=True)
        raise SystemExit(
            f"STOP: {DEST08.name} is still/Ken Burns first={first:.2f} mean={mean:.2f}"
        )
    qa = RAW / f"_qa_{DEST08.stem}"
    qa.mkdir(parents=True, exist_ok=True)
    for t, name in ((0.04, "t000"), (1.00, "t100"), (3.50, "t350"), (7.20, "t720")):
        ff(
            "-ss", f"{t:.2f}", "-i", str(DEST08),
            "-frames:v", "1", "-q:v", "3", str(qa / f"{name}.jpg"),
        )
    print(f"SAVED {DEST08}", flush=True)
    print(f"SHA256 {sha256(DEST08)}", flush=True)
    print("REPLACED t54 plate 08_passengers (v01 desk CU) with living v03 1×", flush=True)


if __name__ == "__main__":
    main()
