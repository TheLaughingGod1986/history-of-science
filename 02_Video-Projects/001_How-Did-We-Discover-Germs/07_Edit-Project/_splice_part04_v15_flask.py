#!/usr/bin/env python3
"""Part 04 v15 — edit-only flask splice. No Flow. No T2V.

KEEP 07_bloom_cloud_v13 (0:43–0:49 living v06).
KEEP Explorer teal garnish from remint A (06_v14 people).
REPLACE remaining broken flasks with 01_question_mark_flask_v06 at 1×.
"""
from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
RAW = PROJ / "04_Generated-Clips/part04/raw/v01_fast_probe"
LIVE = RAW / "01_question_mark_flask_v06.mp4"
EXPLORER = RAW / "06_explorer_watches_v14.mp4"
DEST04 = RAW / "04_still_clear_v15.mp4"
DEST05 = RAW / "05_tip_the_trap_v15.mp4"
DEST06 = RAW / "06_explorer_watches_v15.mp4"
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
    mean = sum(diffs) / len(diffs)
    return first, mean


def encode(filt: str, inputs: list[str], dest: Path) -> None:
    ff(
        *inputs,
        "-filter_complex", filt,
        "-map", "[v]",
        "-an",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-profile:v", "baseline", "-level", "3.1", "-bf", "0",
        "-preset", "fast", "-crf", "18",
        "-movflags", "+faststart",
        str(dest),
    )


def qa(dest: Path) -> None:
    qa_dir = RAW / f"_qa_{dest.stem}"
    qa_dir.mkdir(parents=True, exist_ok=True)
    for t, name in ((0.04, "t000"), (1.00, "t100"), (3.50, "t350"), (7.20, "t720")):
        ff(
            "-ss", f"{t:.2f}", "-i", str(dest),
            "-frames:v", "1", "-q:v", "3", str(qa_dir / f"{name}.jpg"),
        )


def write_living_window(dest: Path, start: float, ping_pong: bool = False) -> None:
    src_dur = probe_dur(LIVE)
    if src_dur < 7.40:
        raise SystemExit(f"STOP: living take too short {LIVE} {src_dur:.2f}s")
    if ping_pong:
        filt = (
            f"[0:v]trim=0:{src_dur:.2f},setpts=PTS-STARTPTS,"
            "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,"
            f"fps={FPS},format=yuv420p,split=2[fwd][tmp];"
            "[tmp]reverse[rev];"
            "[rev][fwd]concat=n=2:v=1:a=0,"
            f"trim=0:{CLIP_USE:.2f},setpts=PTS-STARTPTS,setsar=1[v]"
        )
        inputs = ["-i", str(LIVE)]
    else:
        filt = (
            f"[0:v]trim={start:.2f}:{start + CLIP_USE:.2f},setpts=PTS-STARTPTS,"
            "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,"
            f"fps={FPS},format=yuv420p,setsar=1[v]"
        )
        inputs = ["-i", str(LIVE)]
    encode(filt, inputs, dest)
    first, mean = motion_ok(dest)
    print(f"  {dest.name} first={first:.2f} mean={mean:.2f}", flush=True)
    if first < STILL_FIRST or mean < STILL_MEAN:
        dest.unlink(missing_ok=True)
        raise SystemExit(
            f"STOP: {dest.name} is still/Ken Burns first={first:.2f} mean={mean:.2f}"
        )
    qa(dest)


def write_05() -> None:
    """Upright living swan-neck. 1×. Offset window so it is not a crawl of 01/07."""
    src_dur = probe_dur(LIVE)
    if src_dur < 7.40:
        raise SystemExit(f"STOP: living take too short {LIVE} {src_dur:.2f}s")
    # 1× from 0.50 so this is not the same 0–7.5 window as plate 01 / 07.
    start = 0.50
    usable = min(src_dur - start, CLIP_USE)
    loops_needed = CLIP_USE - usable
    if loops_needed <= 0.02:
        filt = (
            f"[0:v]trim={start:.2f}:{start + CLIP_USE:.2f},setpts=PTS-STARTPTS,"
            "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,"
            f"fps={FPS},format=yuv420p,setsar=1[v]"
        )
        inputs = ["-i", str(LIVE)]
    else:
        # 1× ping-pong of moving frames — never freeze, never Ken Burns.
        filt = (
            f"[0:v]trim={start:.2f}:{src_dur:.2f},setpts=PTS-STARTPTS,"
            "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,"
            f"fps={FPS},format=yuv420p,split=2[fwd][tmp];"
            "[tmp]reverse[rev];"
            "[fwd][rev]concat=n=2:v=1:a=0,"
            f"trim=0:{CLIP_USE:.2f},setpts=PTS-STARTPTS,setsar=1[v]"
        )
        inputs = ["-i", str(LIVE)]
    encode(filt, inputs, DEST05)
    first, mean = motion_ok(DEST05)
    print(f"  {DEST05.name} first={first:.2f} mean={mean:.2f}", flush=True)
    if first < STILL_FIRST or mean < STILL_MEAN:
        DEST05.unlink(missing_ok=True)
        raise SystemExit(
            f"STOP: {DEST05.name} is still/Ken Burns first={first:.2f} mean={mean:.2f}"
        )
    qa(DEST05)


def write_06() -> None:
    """Keep remint A Explorer. Stamp living v06 swan-neck over the straight neck."""
    if not EXPLORER.exists():
        raise SystemExit(f"STOP: missing Explorer remint A {EXPLORER}")
    mask = RAW / "_v15_flask_ellipse_mask.png"
    ff(
        "-f", "lavfi", "-i", "color=c=white:s=400x381:d=0.04",
        "-frames:v", "1",
        "-vf",
        "format=gray,"
        "geq=lum='255*max(0,min(1,(1-hypot((X-W/2)/(W*0.40),(Y-H/2)/(H*0.42)))*7))'",
        str(mask),
    )
    filt = (
        f"[0:v]trim=0:{CLIP_USE:.2f},setpts=PTS-STARTPTS,"
        "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,"
        f"fps={FPS},format=yuv420p[base];"
        f"[1:v]trim=0:{CLIP_USE:.2f},setpts=PTS-STARTPTS,"
        "crop=420:400:460:200,scale=400:381,format=rgb24[fl];"
        f"[2:v]format=gray,fps={FPS},trim=0:{CLIP_USE:.2f},setpts=PTS-STARTPTS[mask];"
        "[fl][mask]alphamerge[fla];"
        f"[base][fla]overlay=440:175:format=auto,format=yuv420p,setsar=1[v]"
    )
    encode(
        filt,
        [
            "-i", str(EXPLORER),
            "-i", str(LIVE),
            "-loop", "1", "-t", f"{CLIP_USE:.2f}", "-i", str(mask),
        ],
        DEST06,
    )
    first, mean = motion_ok(DEST06)
    print(f"  {DEST06.name} first={first:.2f} mean={mean:.2f}", flush=True)
    if first < STILL_FIRST or mean < STILL_MEAN:
        DEST06.unlink(missing_ok=True)
        raise SystemExit(
            f"STOP: {DEST06.name} is still/Ken Burns first={first:.2f} mean={mean:.2f}"
        )
    qa(DEST06)


def main() -> None:
    if not LIVE.exists():
        raise SystemExit(f"STOP: missing living take {LIVE}")
    RAW.mkdir(parents=True, exist_ok=True)
    write_living_window(DEST04, start=0.0, ping_pong=True)
    print(f"SAVED {DEST04}", flush=True)
    print(f"SHA256 {sha256(DEST04)}", flush=True)
    write_05()
    print(f"SAVED {DEST05}", flush=True)
    print(f"SHA256 {sha256(DEST05)}", flush=True)
    write_06()
    print(f"SAVED {DEST06}", flush=True)
    print(f"SHA256 {sha256(DEST06)}", flush=True)
    hold07 = RAW / "07_bloom_cloud_v13.mp4"
    if not hold07.exists():
        raise SystemExit("STOP: missing 07_bloom_cloud_v13 KEEP")
    print(f"KEEP {hold07.name} {sha256(hold07)}", flush=True)


if __name__ == "__main__":
    main()
