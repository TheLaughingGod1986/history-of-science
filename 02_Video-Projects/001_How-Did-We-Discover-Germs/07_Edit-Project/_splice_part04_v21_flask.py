#!/usr/bin/env python3
"""Part 04 v21 — flask-identity splices. Edit-only. No Flow.

FAIL 04 STILL CLEAR ~0:25 flared glass foot → unused living
  04_still_clear_v03 (S-curve only, round-bottom on wood, grey-clear).
FAIL 10 lecture-arch ~1:05 two-neck retort → unused living
  10_an_address_v04 (classic Pasteur, lecture theater, same as t72 lock).

Do not overwrite v19/v20 dests. 08 hitchhikers has no unused locked Pasteur — T2V later.
KEEP 07 bloom v13. Nested/ghost HOLD. No twins. No top hats.
"""
from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
RAW = PROJ / "04_Generated-Clips/part04/raw/v01_fast_probe"
KEEP07 = RAW / "07_bloom_cloud_v13.mp4"
KEEP07_SHA = "fd5d4f7470386ae1bf2eba745cd2d695c402c549cd6fc061edd885fdb34d3604"
PARENT = PROJ / "09_Final-Export/hos_001_part04_rough_v20.mp4"
PARENT_SHA = "49942b3185275621d9e291bc0b453905f3de36576b7ed6c9f030a33bf24a5345"
JOBS = [
    (
        RAW / "04_still_clear_v03.mp4",
        RAW / "04_still_clear_v21.mp4",
        0.00,
        "STILL CLEAR round-bottom grey-clear",
    ),
    (
        RAW / "10_an_address_v04.mp4",
        RAW / "10_an_address_v21.mp4",
        0.00,
        "lecture-arch Pasteur",
    ),
]
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


def write_1x(src: Path, dest: Path, start: float) -> None:
    if dest.exists() and dest.name in {
        "04_still_clear_v19.mp4",
        "10_an_address_v20.mp4",
        "07_bloom_cloud_v13.mp4",
    }:
        raise SystemExit(f"STOP: refusing to overwrite {dest.name}")
    src_dur = probe_dur(src)
    if start + CLIP_USE > src_dur + 0.02:
        raise SystemExit(
            f"STOP: {src.name} window {start:.2f}+{CLIP_USE:.2f} exceeds {src_dur:.2f}"
        )
    filt = (
        f"[0:v]trim={start:.2f}:{start + CLIP_USE:.2f},setpts=PTS-STARTPTS,"
        "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,"
        f"fps={FPS},format=yuv420p,setsar=1[v]"
    )
    ff(
        "-i", str(src),
        "-filter_complex", filt,
        "-map", "[v]", "-an",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-profile:v", "baseline", "-level", "3.1", "-bf", "0",
        "-preset", "fast", "-crf", "18",
        "-movflags", "+faststart",
        str(dest),
    )
    first, mean = motion_ok(dest)
    print(
        f"  {dest.name} src={src.name} start={start:.2f} "
        f"first={first:.2f} mean={mean:.2f}",
        flush=True,
    )
    if first < STILL_FIRST or mean < STILL_MEAN:
        dest.unlink(missing_ok=True)
        raise SystemExit(
            f"STOP: {dest.name} is still/Ken Burns first={first:.2f} mean={mean:.2f}"
        )
    qa = RAW / f"_qa_{dest.stem}"
    qa.mkdir(parents=True, exist_ok=True)
    for t, name in ((0.04, "t000"), (1.00, "t100"), (3.50, "t350"), (7.20, "t720")):
        ff(
            "-ss", f"{t:.2f}", "-i", str(dest),
            "-frames:v", "1", "-q:v", "3", str(qa / f"{name}.jpg"),
        )
    print(f"SAVED {dest} sha256={sha256(dest)}", flush=True)


def main() -> None:
    if not PARENT.exists() or sha256(PARENT) != PARENT_SHA:
        raise SystemExit("STOP: parent v20 missing or hash mismatch")
    if not KEEP07.exists() or sha256(KEEP07) != KEEP07_SHA:
        raise SystemExit("STOP: bloom v13 missing or hash mismatch")
    print(f"PARENT v20 {PARENT_SHA}", flush=True)
    print(f"KEEP {KEEP07.name}", flush=True)
    for src, dest, start, tag in JOBS:
        if not src.exists() or src.stat().st_size < 400_000:
            raise SystemExit(f"STOP: missing unused living {src}")
        print(f"REPLACE {tag} {src.name} -> {dest.name}", flush=True)
        write_1x(src, dest, start)
    print("OK v21 flask splices — 08 still needs T2V", flush=True)


if __name__ == "__main__":
    main()
