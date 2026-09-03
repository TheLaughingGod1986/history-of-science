#!/usr/bin/env python3
"""Part 04 v23 — crop leftover second-flask rim from dust take. No Flow.

03 THE CURVE ~0:14–0:21 and 08 passengers ~0:50–0:56 share 03_dust_in_the_curve_v01.
Rim sits lower-left until ~5.5s; 8.0s take cannot start late enough for 7.50s clean.
Crop left rim off. Different start + crop so 03 and 08 are not the same bytes.
"""
from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
RAW = PROJ / "04_Generated-Clips/part04/raw/v01_fast_probe"
SRC = RAW / "03_dust_in_the_curve_v01.mp4"
PARENT = PROJ / "09_Final-Export/hos_001_part04_rough_v22.mp4"
PARENT_SHA = "e462e16ce266fa5081ffa96a53547c6ed6251bd463d8d1c5df30f34af7ee7a25"
CLIP_USE = 7.50
FPS = 24
STILL_FIRST = 2.0
STILL_MEAN = 1.4
# 03: early window, lighter crop. 08: later window, tighter crop (0:54 framing).
JOBS = [
    (RAW / "03_dust_in_the_curve_v23.mp4", 0.00, 160),
    (RAW / "08_passengers_v23.mp4", 0.50, 200),
]


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


def splice(dest: Path, start: float, crop_l: int) -> None:
    dest_tmp = dest.with_name(dest.stem + ".part.mp4")
    dest_tmp.unlink(missing_ok=True)
    w = 1280 - crop_l
    filt = (
        f"[0:v]trim={start:.2f}:{start + CLIP_USE:.2f},setpts=PTS-STARTPTS,"
        f"crop={w}:720:{crop_l}:0,scale=1280:720,"
        f"fps={FPS},format=yuv420p,setsar=1[v]"
    )
    r = subprocess.run(
        [
            "ffmpeg", "-y", "-i", str(SRC),
            "-filter_complex", filt,
            "-map", "[v]", "-an",
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-profile:v", "baseline", "-level", "3.1", "-bf", "0",
            "-preset", "fast", "-crf", "18",
            "-movflags", "+faststart",
            str(dest_tmp),
        ],
        capture_output=True,
        text=True,
    )
    if r.returncode != 0:
        dest_tmp.unlink(missing_ok=True)
        raise SystemExit(
            f"STOP: ffmpeg {r.returncode}\n{r.stderr[-2000:] if r.stderr else ''}"
        )
    first, mean = motion_ok(dest_tmp)
    print(
        f"  {dest.name} start={start:.2f} crop_l={crop_l} "
        f"first={first:.2f} mean={mean:.2f}",
        flush=True,
    )
    if first < STILL_FIRST or mean < STILL_MEAN:
        dest_tmp.unlink(missing_ok=True)
        raise SystemExit(
            f"STOP: {dest.name} still/Ken Burns first={first:.2f} mean={mean:.2f}"
        )
    dest_tmp.replace(dest)
    qa = RAW / f"_qa_{dest.stem}"
    qa.mkdir(parents=True, exist_ok=True)
    for t, name in ((0.04, "t000"), (1.80, "t180"), (3.50, "t350"), (7.20, "t720")):
        subprocess.run(
            [
                "ffmpeg", "-y", "-ss", f"{t:.2f}", "-i", str(dest),
                "-frames:v", "1", "-q:v", "3", str(qa / f"{name}.jpg"),
            ],
            check=True,
            capture_output=True,
        )
        subprocess.run(
            [
                "ffmpeg", "-y", "-i", str(qa / f"{name}.jpg"),
                "-vf", "crop=200:240:0:480", "-q:v", "3",
                str(qa / f"{name}_bl.jpg"),
            ],
            check=True,
            capture_output=True,
        )
    print(f"SAVED {dest} sha256={sha256(dest)}", flush=True)


def main() -> None:
    if not PARENT.exists() or sha256(PARENT) != PARENT_SHA:
        raise SystemExit("STOP: parent v22 missing or hash mismatch")
    if not SRC.exists() or SRC.stat().st_size < 400_000:
        raise SystemExit(f"STOP: missing dust take {SRC}")
    src_dur = probe_dur(SRC)
    for dest, start, crop_l in JOBS:
        if start + CLIP_USE > src_dur + 0.02:
            raise SystemExit(
                f"STOP: dust take {src_dur:.3f}s cannot cover "
                f"{start:.2f}+{CLIP_USE:.2f}. No file."
            )
        splice(dest, start, crop_l)
    a, b = JOBS[0][0], JOBS[1][0]
    if sha256(a) == sha256(b):
        raise SystemExit("STOP: 03 and 08 recuts are identical bytes")


if __name__ == "__main__":
    main()
