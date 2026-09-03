#!/usr/bin/env python3
"""Part 04 v17 official — edit-only. No Flow. No T2V.

KEEP 07_bloom_cloud_v13 (0:43–0:49 living v06 1× hero).
KEEP 02 / 03 / 08 / 10 / 11 / 12.

09 (1:01 end desk): living v06 at 1×, opposite side, scientist-arm.
True S-curve. No twins. No magnifier. Not a tighter hero CU.

Other flask plates: different take or unused window at 1×.
No ping-pong. No nested glass. Loop not crawl.
"""
from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
RAW = PROJ / "04_Generated-Clips/part04/raw/v01_fast_probe"
LIVE01 = RAW / "01_question_mark_flask_v01.mp4"
LIVE03 = RAW / "01_question_mark_flask_v03.mp4"
LIVE06 = RAW / "01_question_mark_flask_v06.mp4"
EXPLORER = RAW / "06_explorer_watches_v01.mp4"
CLEAR01 = RAW / "04_still_clear_v01.mp4"
HOLD07 = RAW / "07_bloom_cloud_v13.mp4"
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


def qa(dest: Path) -> None:
    qa_dir = RAW / f"_qa_{dest.stem}"
    qa_dir.mkdir(parents=True, exist_ok=True)
    for t, name in ((0.04, "t000"), (1.00, "t100"), (3.50, "t350"), (7.20, "t720")):
        ff(
            "-ss", f"{t:.2f}", "-i", str(dest),
            "-frames:v", "1", "-q:v", "3", str(qa_dir / f"{name}.jpg"),
        )


def write_1x(
    src: Path,
    dest: Path,
    start: float = 0.0,
    hflip: bool = False,
) -> None:
    if not src.exists():
        raise SystemExit(f"STOP: missing {src}")
    src_dur = probe_dur(src)
    if src_dur < 1.50:
        raise SystemExit(f"STOP: {src.name} too short {src_dur:.2f}")
    usable = min(src_dur - start, src_dur)
    if usable < 1.50:
        raise SystemExit(f"STOP: {src.name} window too short start={start}")
    loops = 1
    while loops * usable < CLIP_USE + 0.05:
        loops += 1
    flip = "hflip," if hflip else ""
    if start + CLIP_USE <= src_dur + 0.02 and loops == 1:
        filt = (
            f"[0:v]trim={start:.2f}:{start + CLIP_USE:.2f},setpts=PTS-STARTPTS,"
            f"{flip}scale=1280:720:force_original_aspect_ratio=increase,"
            f"crop=1280:720,fps={FPS},format=yuv420p,setsar=1[v]"
        )
        inputs = ["-i", str(src)]
    else:
        # 1× forward loop — not reverse ping-pong, not crawl.
        parts = []
        for i in range(loops):
            parts.append(
                f"[{i}:v]trim={start:.2f}:{start + usable:.2f},setpts=PTS-STARTPTS,"
                f"{flip}scale=1280:720:force_original_aspect_ratio=increase,"
                f"crop=1280:720,fps={FPS},format=yuv420p[s{i}]"
            )
        concat = "".join(f"[s{i}]" for i in range(loops))
        parts.append(
            f"{concat}concat=n={loops}:v=1:a=0,"
            f"trim=0:{CLIP_USE:.2f},setpts=PTS-STARTPTS,setsar=1[v]"
        )
        filt = ";".join(parts)
        inputs = []
        for _ in range(loops):
            inputs += ["-i", str(src)]
    ff(
        *inputs,
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
        f"  {dest.name} src={src.name} start={start:.2f} flip={hflip} "
        f"loops={loops} first={first:.2f} mean={mean:.2f}",
        flush=True,
    )
    if first < STILL_FIRST or mean < STILL_MEAN:
        dest.unlink(missing_ok=True)
        raise SystemExit(
            f"STOP: {dest.name} is still/Ken Burns first={first:.2f} mean={mean:.2f}"
        )
    qa(dest)
    print(f"SHA256 {sha256(dest)}", flush=True)


def main() -> None:
    if not HOLD07.exists():
        raise SystemExit("STOP: missing 07_bloom_cloud_v13 KEEP")
    print(f"KEEP {HOLD07.name} sha256={sha256(HOLD07)}", flush=True)
    jobs = [
        (LIVE03, RAW / "01_question_mark_flask_v17.mp4", 0.00, False),
        (CLEAR01, RAW / "04_still_clear_v17.mp4", 0.00, False),
        (LIVE01, RAW / "05_tip_the_trap_v17.mp4", 0.50, False),
        (EXPLORER, RAW / "06_explorer_watches_v17.mp4", 0.00, False),
        (LIVE06, RAW / "09_sceptics_watch_v17.mp4", 0.50, True),
    ]
    for src, dest, start, flip in jobs:
        write_1x(src, dest, start, flip)
        print(f"SAVED {dest}", flush=True)


if __name__ == "__main__":
    main()
