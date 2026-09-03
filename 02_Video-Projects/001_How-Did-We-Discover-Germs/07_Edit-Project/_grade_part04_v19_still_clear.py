#!/usr/bin/env python3
"""Part 04 v19 — grade broth on living 04_still_clear_v17 only. No Flow.

Kill yellow/gold/tea/amber in the bulb so it reads distilled-water clear.
Keep swan-neck, one bottle, glass highlights, wood, lamp.
"""
from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
RAW = PROJ / "04_Generated-Clips/part04/raw/v01_fast_probe"
SRC = RAW / "04_still_clear_v17.mp4"
DEST = RAW / "04_still_clear_v19.mp4"
MASK = RAW / "_v19_broth_ellipse_mask.png"
QA = RAW / "_qa_04_still_clear_v19"
FPS = 24
STILL_FIRST = 2.0
STILL_MEAN = 1.4
# Soft ellipse over the liquid body only (not the table, not the lamp).
# Wide at the meniscus so the rim is not left as an amber ring.
CX, CY, RX, RY = 620, 528, 160, 66


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def ff(*args: str) -> None:
    r = subprocess.run(["ffmpeg", "-y", *args], capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-2000:], flush=True)
        raise SystemExit(f"ffmpeg failed: {args[:6]}")


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


def write_mask() -> None:
    # White ellipse, feathered, black elsewhere. 1280x720.
    expr = (
        f"if(lte(pow((X-{CX})/{RX},2)+pow((Y-{CY})/{RY},2),1),255,"
        f"if(lte(pow((X-{CX})/{RX},2)+pow((Y-{CY})/{RY},2),1.18),"
        f"clip(255*(1.18-sqrt(pow((X-{CX})/{RX},2)+pow((Y-{CY})/{RY},2)))/0.18,0,255),0))"
    )
    ff(
        "-f", "lavfi",
        "-i", "color=c=black:s=1280x720:d=0.04:r=24",
        "-vf", f"geq=lum='{expr}':cb=128:cr=128,format=gray",
        "-frames:v", "1",
        str(MASK),
    )


def grade() -> None:
    if not SRC.exists() or SRC.stat().st_size < 400_000:
        raise SystemExit(f"STOP: missing living plate {SRC}")
    write_mask()
    W, H = 1280, 720
    frame_n = W * H * 3
    rx2, ry2 = float(RX * RX), float(RY * RY)
    xs = range(max(0, CX - RX - 2), min(W, CX + RX + 3))
    ys = range(max(0, CY - RY - 2), min(H, CY + RY + 3))

    dec = subprocess.Popen(
        [
            "ffmpeg", "-v", "error", "-i", str(SRC),
            "-f", "rawvideo", "-pix_fmt", "rgb24", "pipe:1",
        ],
        stdout=subprocess.PIPE,
    )
    enc = subprocess.Popen(
        [
            "ffmpeg", "-y", "-v", "error",
            "-f", "rawvideo", "-pix_fmt", "rgb24",
            "-s", f"{W}x{H}", "-r", str(FPS), "-i", "pipe:0",
            "-an",
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-profile:v", "baseline", "-level", "3.1", "-bf", "0",
            "-preset", "fast", "-crf", "18",
            "-movflags", "+faststart",
            str(DEST),
        ],
        stdin=subprocess.PIPE,
    )
    assert dec.stdout is not None and enc.stdin is not None
    n = 0
    while True:
        buf = dec.stdout.read(frame_n)
        if not buf or len(buf) < frame_n:
            break
        px = bytearray(buf)
        for y in ys:
            row = y * W * 3
            dy = (y - CY) * (y - CY) / ry2
            for x in xs:
                d = (x - CX) * (x - CX) / rx2 + dy
                if d > 1.0:
                    continue
                i = row + x * 3
                r, g, b = px[i], px[i + 1], px[i + 2]
                if r + g + b > 600:
                    continue
                if r - b < 40:
                    continue
                lum = int(0.299 * r + 0.587 * g + 0.114 * b)
                amt = 1.0 if d <= 0.70 else (1.0 - d) / 0.30
                px[i] = int(r + (lum - r) * amt)
                px[i + 1] = int(g + (lum - g) * amt)
                px[i + 2] = int(b + (min(255, lum + 8) - b) * amt)
        enc.stdin.write(px)
        n += 1
    enc.stdin.close()
    dec.stdout.close()
    if dec.wait() != 0 or enc.wait() != 0:
        raise SystemExit("STOP: grade pipe failed")
    if n < 8:
        raise SystemExit(f"STOP: grade wrote {n} frames")
    print(f"  graded {n} frames", flush=True)


def qa() -> None:
    QA.mkdir(parents=True, exist_ok=True)
    for t, name in ((0.04, "t000"), (1.00, "t100"), (3.50, "t350"), (7.20, "t720")):
        ff(
            "-ss", f"{t:.2f}", "-i", str(DEST),
            "-frames:v", "1", "-q:v", "3", str(QA / f"{name}.jpg"),
        )
        ff(
            "-ss", f"{t:.2f}", "-i", str(DEST),
            "-frames:v", "1",
            "-vf", "crop=420:360:430:280",
            "-q:v", "3", str(QA / f"{name}_bulb.jpg"),
        )
    ff("-i", str(MASK), "-frames:v", "1", "-q:v", "3", str(QA / "mask.jpg"))


def main() -> None:
    print(f"GRADE src={SRC.name} dest={DEST.name} ellipse=({CX},{CY},{RX},{RY})", flush=True)
    grade()
    first, mean = motion_ok(DEST)
    print(f"  motion first={first:.2f} mean={mean:.2f} bytes={DEST.stat().st_size}", flush=True)
    if first < STILL_FIRST or mean < STILL_MEAN:
        DEST.unlink(missing_ok=True)
        raise SystemExit(
            f"STOP: grade froze the plate first={first:.2f} mean={mean:.2f}"
        )
    qa()
    print(f"SAVED {DEST}", flush=True)
    print(f"SHA256 {sha256(DEST)}", flush=True)
    print(f"QA {QA}", flush=True)


if __name__ == "__main__":
    main()
