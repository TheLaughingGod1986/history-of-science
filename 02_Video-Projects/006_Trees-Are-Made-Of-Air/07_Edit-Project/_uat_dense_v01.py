#!/usr/bin/env python3
"""Dense UAT tile for a Veo take: N evenly spaced frames across the clip (6 per row, 480 px wide;
frame k sits at k·dur/N s — this ffmpeg has no drawtext),
plus ffprobe size/duration/audio and freezedetect at 0.5 s. Prints one table row per clip.

  _uat_dense_v01.py <clip.mp4> [<clip.mp4> …] [--frames 24] [--out-dir <dir>]
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def probe(p: Path) -> dict:
    j = json.loads(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,width,height:format=duration",
         "-of", "json", str(p)], text=True))
    v = next(s for s in j["streams"] if s["codec_type"] == "video")
    audio = sum(1 for s in j["streams"] if s["codec_type"] == "audio")
    return {"w": v["width"], "h": v["height"], "dur": float(j["format"]["duration"]), "audio": audio}


def freezes(p: Path) -> int:
    err = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(p), "-vf", "freezedetect=n=0.003:d=0.5",
                          "-f", "null", "-"], capture_output=True, text=True, errors="replace").stderr
    return err.count("freeze_start")


def tile(p: Path, out: Path, n: int, dur: float) -> None:
    fps = n / dur
    rows = (n + 5) // 6
    vf = f"fps={fps:.5f},scale=480:-2,tile=6x{rows}:padding=4:color=black"
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(p), "-vf", vf,
                    "-frames:v", "1", "-q:v", "3", str(out)], check=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("clips", nargs="+")
    ap.add_argument("--frames", type=int, default=24)
    ap.add_argument("--out-dir")
    a = ap.parse_args()
    for c in a.clips:
        p = Path(c)
        info = probe(p)
        out_dir = Path(a.out_dir) if a.out_dir else p.parent.parent.parent / "uat"
        out_dir.mkdir(parents=True, exist_ok=True)
        out = out_dir / f"{p.stem}_dense.jpg"
        tile(p, out, a.frames, info["dur"])
        print(f"| {p.stem} | {info['w']}x{info['h']} | {info['dur']:.2f} s | audio={info['audio']} | "
              f"freeze>0.5s={freezes(p)} | {out}")


if __name__ == "__main__":
    main()
