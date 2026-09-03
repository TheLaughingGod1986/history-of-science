#!/usr/bin/env python3
"""Part 04 v13 — living 0:02 swan-neck into 07. Edit only. No Flow.

Source is 01_question_mark_flask_v06 (the open living take). Native 1×.
If shorter than CLIP_USE, loop at 1× — never freeze-pad, never Ken Burns.
Also write 08_passengers_v13 from unused living 01_v01 to kill the sunbeam
germ storm at ~0:50.
"""
from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
RAW = PROJ / "04_Generated-Clips/part04/raw/v01_fast_probe"
LIVE = RAW / "01_question_mark_flask_v06.mp4"
CLEAN = RAW / "01_question_mark_flask_v01.mp4"
DEST07 = RAW / "07_bloom_cloud_v13.mp4"
DEST08 = RAW / "08_passengers_v13.mp4"
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
    mean = sum(diffs) / len(diffs)
    return first, mean


def write_living(src: Path, dest: Path) -> None:
    if not src.exists():
        raise SystemExit(f"STOP: missing living take {src}")
    src_dur = probe_dur(src)
    if src_dur < 1.50:
        raise SystemExit(f"STOP: living take too short {src} {src_dur:.2f}s")
    # 1× only. Loop the moving clip if shorter than the plate.
    usable = min(src_dur, 7.90)
    loops = 1
    while loops * usable < CLIP_USE + 0.05:
        loops += 1
    if loops == 1:
        filt = (
            f"[0:v]trim=0:{CLIP_USE:.2f},setpts=PTS-STARTPTS,"
            "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,"
            f"fps={FPS},format=yuv420p,setsar=1[v]"
        )
        inputs = ["-i", str(src)]
    else:
        parts = []
        for i in range(loops):
            parts.append(
                f"[{i}:v]trim=0:{usable:.2f},setpts=PTS-STARTPTS,"
                "scale=1280:720:force_original_aspect_ratio=increase,"
                f"crop=1280:720,fps={FPS},format=yuv420p[s{i}]"
            )
        concat_in = "".join(f"[s{i}]" for i in range(loops))
        parts.append(
            f"{concat_in}concat=n={loops}:v=1:a=0,"
            f"trim=0:{CLIP_USE:.2f},setpts=PTS-STARTPTS,setsar=1[v]"
        )
        filt = ";".join(parts)
        inputs = []
        for _ in range(loops):
            inputs += ["-i", str(src)]
    subprocess.run(
        [
            "ffmpeg", "-y", *inputs,
            "-filter_complex", filt,
            "-map", "[v]", "-an",
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-profile:v", "baseline", "-level", "3.1", "-bf", "0",
            "-preset", "fast", "-crf", "18",
            "-movflags", "+faststart",
            str(dest),
        ],
        check=True,
        capture_output=True,
    )
    first, mean = motion_ok(dest)
    print(
        f"  {dest.name} first={first:.2f} mean={mean:.2f} "
        f"src={src.name} loops={loops}",
        flush=True,
    )
    if first < STILL_FIRST or mean < STILL_MEAN:
        dest.unlink(missing_ok=True)
        raise SystemExit(
            f"STOP: {dest.name} is still/Ken Burns "
            f"first={first:.2f} mean={mean:.2f}. Do not mint a new flask."
        )


def qa(dest: Path) -> None:
    qa_dir = RAW / f"_qa_{dest.stem}"
    qa_dir.mkdir(parents=True, exist_ok=True)
    for t, name in ((0.04, "t000"), (1.00, "t100"), (4.00, "t400"), (7.20, "t720")):
        subprocess.run(
            [
                "ffmpeg", "-y", "-ss", f"{t:.2f}", "-i", str(dest),
                "-frames:v", "1", "-q:v", "3", str(qa_dir / f"{name}.jpg"),
            ],
            check=True,
            capture_output=True,
        )


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    write_living(LIVE, DEST07)
    qa(DEST07)
    print(f"SAVED {DEST07}", flush=True)
    print(f"SHA256 {sha256(DEST07)}", flush=True)
    print(f"BYTES {DEST07.stat().st_size}", flush=True)
    if CLEAN.exists():
        write_living(CLEAN, DEST08)
        qa(DEST08)
        print(f"SAVED {DEST08} (no sunbeam storm)", flush=True)
        print(f"SHA256 {sha256(DEST08)}", flush=True)
    else:
        print("STOP: no clean unused take for 08 — left 08 as-is", flush=True)


if __name__ == "__main__":
    main()
