#!/usr/bin/env python3
"""Part 04 v22 — 08 passengers from later window of dust take. No Flow.

Source: 03_dust_in_the_curve_v01 (8.0s). Plate 03 already used 0.00–7.50.
Later window: 0.50–8.00. Do not loop. Do not mint.
"""
from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
RAW = PROJ / "04_Generated-Clips/part04/raw/v01_fast_probe"
SRC = RAW / "03_dust_in_the_curve_v01.mp4"
DEST = RAW / "08_passengers_v22.mp4"
PARENT = PROJ / "09_Final-Export/hos_001_part04_rough_v21.mp4"
PARENT_SHA = "b9d162f180a6b20ce69bec9ba26957dc5c495da01616ac6403b62f4d0bf76eee"
START = 0.50
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
    if not PARENT.exists() or sha256(PARENT) != PARENT_SHA:
        raise SystemExit("STOP: parent v21 missing or hash mismatch")
    if not SRC.exists() or SRC.stat().st_size < 400_000:
        raise SystemExit(f"STOP: missing dust take {SRC}")
    src_dur = probe_dur(SRC)
    if START + CLIP_USE > src_dur + 0.02:
        raise SystemExit(
            f"STOP: dust take {src_dur:.3f}s cannot cover window "
            f"{START:.2f}+{CLIP_USE:.2f}. No file."
        )
    dest_tmp = DEST.with_name(DEST.stem + ".part.mp4")
    dest_tmp.unlink(missing_ok=True)
    filt = (
        f"[0:v]trim={START:.2f}:{START + CLIP_USE:.2f},setpts=PTS-STARTPTS,"
        "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,"
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
        raise SystemExit(
            f"STOP: ffmpeg {r.returncode}\n{r.stderr[-2000:] if r.stderr else ''}"
        )
    first, mean = motion_ok(dest_tmp)
    print(
        f"  {DEST.name} src={SRC.name} start={START:.2f} "
        f"first={first:.2f} mean={mean:.2f}",
        flush=True,
    )
    if first < STILL_FIRST or mean < STILL_MEAN:
        dest_tmp.unlink(missing_ok=True)
        raise SystemExit(
            f"STOP: dust window is still/Ken Burns first={first:.2f} mean={mean:.2f}"
        )
    dest_tmp.replace(DEST)
    qa = RAW / f"_qa_{DEST.stem}"
    qa.mkdir(parents=True, exist_ok=True)
    for t, name in ((0.04, "t000"), (1.00, "t100"), (3.50, "t350"), (7.20, "t720")):
        subprocess.run(
            [
                "ffmpeg", "-y", "-ss", f"{t:.2f}", "-i", str(DEST),
                "-frames:v", "1", "-q:v", "3", str(qa / f"{name}.jpg"),
            ],
            check=True,
            capture_output=True,
        )
    print(f"SAVED {DEST} sha256={sha256(DEST)}", flush=True)


if __name__ == "__main__":
    main()
