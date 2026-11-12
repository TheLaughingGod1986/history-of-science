#!/usr/bin/env python3
"""Find label-free windows in a normalised compilation master (J0175).

The HOS masters burn their keyword labels into the top right. Two looks:
  box     002, 004, 005: dark brown box with a cream border (right edge x~1892, bottom y~158)
  italic  001, 003: white italic text with a dark outline, no box (y~100-200)
Every look also checks the lower third: a grey see-through panel at bottom left
(x~70-620, y~900-1000) with a cream italic caption and sub-line (003 "WHY COVER
THE TUBE" 90.5-94.9 s, "X FOR UNKNOWN" ~138 s, "PATTERN, NOT GHOST" ~142 s). The
panel isn't always dark (over cardboard it's mid-grey), so the test counts rows of
thin bright letter strokes: captions give 30-32 rows, clean frames 0, including a
pale arm on dark wood (005 290 s) and brass telescopes (004 231 s). The line is 12.
The scan samples at 0.5 s, so keep 0.3 s off each edge of a clean window.
The italic look misses small labels ("A surgical theatre" at 001 315-317 s), so
001 and 003 windows are also checked by eye on a 1 s contact sheet before they're picked.

  python3 _label_scan_v01.py <film_NNN_norm.mp4> --look box|italic [--start 30] [--dur 600] [--min 2.5]
"""
from __future__ import annotations

import argparse
import subprocess

import numpy as np


def frames(src: str, start: float, dur: float, w: int, h: int, x: int, y: int) -> np.ndarray:
    cmd = ["ffmpeg", "-v", "error", "-ss", str(start), "-t", str(dur), "-i", src,
           "-vf", f"fps=2,crop={w}:{h}:{x}:{y},format=gray", "-f", "rawvideo", "-"]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    n = len(raw) // (w * h)
    return np.frombuffer(raw, np.uint8)[: n * w * h].reshape(n, h, w).astype(int)


def is_label_box(f: np.ndarray) -> bool:
    border = f[40:110, 648:656].max(axis=1).mean() - f[40:110, 600:640].mean()
    bottom = f[114:122, 400:640].max(axis=0).mean() - f[100:108, 400:640].mean()
    return border > 60 and bottom > 40


def is_label_italic(f: np.ndarray) -> bool:
    dark = f < 110
    near = np.zeros_like(dark)
    for dx in range(-4, 5):
        near |= np.roll(dark, dx, axis=1)
    return int(((f > 232) & near).sum()) > 600


def is_lower_third(f: np.ndarray) -> bool:
    p = f[10:130, 10:640]
    strokes = (p - np.roll(p, 4, axis=1) > 45) & (p - np.roll(p, -4, axis=1) > 45) & (p > 140)
    strokes[:, :5] = strokes[:, -5:] = False
    return int((strokes.sum(axis=1) > 25).sum()) >= 12


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("--look", choices=["box", "italic"], required=True)
    ap.add_argument("--start", type=float, default=30.0)
    ap.add_argument("--dur", type=float, default=600.0)
    ap.add_argument("--min", type=float, default=2.5)
    a = ap.parse_args()
    if a.look == "box":
        fs, test = frames(a.src, a.start, a.dur, 680, 140, 1240, 40), is_label_box
    else:
        fs, test = frames(a.src, a.start, a.dur, 640, 120, 1280, 90), is_label_italic
    lows = frames(a.src, a.start, a.dur, 700, 140, 50, 880)
    runs, s = [], None
    for i, f in enumerate(fs):
        t = a.start + i / 2
        if not (test(f) or (i < len(lows) and is_lower_third(lows[i]))):
            s = t if s is None else s
        elif s is not None:
            runs.append((s, t - 0.5))
            s = None
    if s is not None:
        runs.append((s, a.start + (len(fs) - 1) / 2))
    for s0, s1 in runs:
        if s1 - s0 >= a.min:
            print(f"clean {s0:7.1f} - {s1:7.1f}  ({s1 - s0:.1f} s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
