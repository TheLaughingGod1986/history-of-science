#!/usr/bin/env python3
"""Part 04 v16 — plate 06 only. Edit-first. No Flow. No T2V.

People stamps from remint A nest leftover straight-neck glass or
read as stickers. Sheet fallback: living v06 is the only glass.

KEEP 07_bloom_cloud_v13 (0:43–0:49). KEEP v15 04/05 splices.
"""
from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
RAW = PROJ / "04_Generated-Clips/part04/raw/v01_fast_probe"
LIVE = RAW / "01_question_mark_flask_v06.mp4"
DEST06 = RAW / "06_explorer_watches_v16.mp4"
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
    if not LIVE.exists():
        raise SystemExit(f"STOP: missing living take {LIVE}")
    src_dur = probe_dur(LIVE)
    if src_dur < 7.40:
        raise SystemExit(f"STOP: living take too short {src_dur:.2f}s")
    # 1× from 1.80 then reverse the moving tail — not a crawl of 01/04/07.
    start = 1.80
    filt = (
        f"[0:v]trim={start:.2f}:{src_dur:.2f},setpts=PTS-STARTPTS,"
        "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,"
        f"fps={FPS},format=yuv420p,split=2[fwd][tmp];"
        "[tmp]reverse[rev];"
        "[fwd][rev]concat=n=2:v=1:a=0,"
        f"trim=0:{CLIP_USE:.2f},setpts=PTS-STARTPTS,setsar=1[v]"
    )
    ff(
        "-i", str(LIVE),
        "-filter_complex", filt,
        "-map", "[v]", "-an",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-profile:v", "baseline", "-level", "3.1", "-bf", "0",
        "-preset", "fast", "-crf", "18",
        "-movflags", "+faststart",
        str(DEST06),
    )
    first, mean = motion_ok(DEST06)
    print(f"  {DEST06.name} first={first:.2f} mean={mean:.2f}", flush=True)
    if first < STILL_FIRST or mean < STILL_MEAN:
        DEST06.unlink(missing_ok=True)
        raise SystemExit(
            f"STOP: {DEST06.name} is still/Ken Burns first={first:.2f} mean={mean:.2f}"
        )
    qa = RAW / f"_qa_{DEST06.stem}"
    qa.mkdir(parents=True, exist_ok=True)
    for t, name in ((0.04, "t000"), (1.00, "t100"), (3.50, "t350"), (7.20, "t720")):
        ff(
            "-ss", f"{t:.2f}", "-i", str(DEST06),
            "-frames:v", "1", "-q:v", "3", str(qa / f"{name}.jpg"),
        )
    hold07 = RAW / "07_bloom_cloud_v13.mp4"
    if not hold07.exists():
        raise SystemExit("STOP: missing 07_bloom_cloud_v13 KEEP")
    print(f"SAVED {DEST06}", flush=True)
    print(f"SHA256 {sha256(DEST06)}", flush=True)
    print(f"BYTES {DEST06.stat().st_size}", flush=True)
    print(f"KEEP {hold07.name} {sha256(hold07)}", flush=True)


if __name__ == "__main__":
    main()
