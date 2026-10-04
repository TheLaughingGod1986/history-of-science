#!/usr/bin/env python3
"""Four frames of a take at 960 px in one 2x2 sheet, plus mean frame-to-frame motion (0-255 scale)
over the board window, so a near-still plate shows up as a number and not just a feeling.

  _uat_quad_v01.py <clip.mp4> <t1> <t2> <t3> <t4> [--use-s 4.28]
"""
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def motion(p: Path, use_s: float) -> float:
    err = subprocess.run(
        ["ffmpeg", "-hide_banner", "-t", f"{use_s}", "-i", str(p), "-vf",
         "scale=320:-2,tblend=all_mode=difference,signalstats,metadata=print:key=lavfi.signalstats.YAVG",
         "-f", "null", "-"], capture_output=True, text=True, errors="replace").stderr
    vals = [float(l.split("=")[-1]) for l in err.splitlines() if "lavfi.signalstats.YAVG" in l]
    return sum(vals) / len(vals) if vals else 0.0


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("clip")
    ap.add_argument("times", nargs=4, type=float)
    ap.add_argument("--use-s", type=float, default=8.0)
    a = ap.parse_args()
    p = Path(a.clip)
    out = p.parent.parent.parent / "uat" / f"{p.stem}_quad.jpg"
    args = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"]
    for t in a.times:
        args += ["-ss", f"{t}", "-i", str(p)]
    fc = ";".join(f"[{i}]scale=960:-2,format=yuvj420p,trim=end_frame=1[v{i}]" for i in range(4))
    fc += ";[v0][v1][v2][v3]xstack=inputs=4:layout=0_0|w0_0|0_h0|w0_h0"
    subprocess.run(args + ["-filter_complex", fc, "-frames:v", "1", "-q:v", "3", str(out)], check=True)
    print(f"{p.stem}: motion {motion(p, a.use_s):.2f} over 0-{a.use_s} s · {out}")


if __name__ == "__main__":
    main()
