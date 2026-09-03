#!/usr/bin/env python3
"""Motion gate for v20 aisle takes. Fail still / still+zoom / freeze tail."""
from __future__ import annotations

import argparse
import shutil
import subprocess
import tempfile
from pathlib import Path


def frames(mp4: Path, dest: Path) -> list[Path]:
    dest.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg", "-y", "-i", str(mp4),
            "-vf", "fps=8,scale=320:180,format=gray",
            str(dest / "%03d.png"),
        ],
        check=True,
        capture_output=True,
    )
    return sorted(dest.glob("*.png"))


def load(p: Path) -> bytes:
    return subprocess.check_output(
        [
            "ffmpeg", "-v", "error", "-i", str(p),
            "-f", "rawvideo", "-pix_fmt", "gray", "pipe:1",
        ]
    )


def mean_abs(a: bytes, b: bytes) -> float:
    n = min(len(a), len(b))
    if n == 0:
        return 0.0
    s = 0
    for i in range(n):
        s += abs(a[i] - b[i])
    return s / n


def mean(xs: list[float]) -> float:
    return sum(xs) / len(xs) if xs else 0.0


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("mp4", type=Path)
    args = ap.parse_args()
    if not args.mp4.exists():
        raise SystemExit(f"missing {args.mp4}")
    tmp = Path(tempfile.mkdtemp(prefix="hos_aisle_qa_"))
    try:
        pngs = frames(args.mp4, tmp)
        if len(pngs) < 8:
            raise SystemExit(f"too few frames {len(pngs)}")
        arr = [load(p) for p in pngs]
        diffs = [mean_abs(arr[i], arr[i + 1]) for i in range(len(arr) - 1)]
        first = diffs[:8]
        last = diffs[-8:]
        mid = diffs[8:-8] if len(diffs) > 16 else diffs
        print(f"FRAMES {len(pngs)}", flush=True)
        print(f"FIRST1S mean={mean(first):.2f} min={min(first):.2f}", flush=True)
        print(f"MID mean={mean(mid):.2f} min={min(mid):.2f}", flush=True)
        print(f"LAST1S mean={mean(last):.2f} min={min(last):.2f}", flush=True)
        if mean(first) < 1.4:
            raise SystemExit("FAIL still-or-zoom in first second")
        if mean(last) < 1.0:
            raise SystemExit("FAIL freeze tail")
        if diffs.count(0) >= 3:
            raise SystemExit("FAIL hard freeze frames")
        print("MOTION_GATE pass (still inspect walk vs zoom)", flush=True)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
