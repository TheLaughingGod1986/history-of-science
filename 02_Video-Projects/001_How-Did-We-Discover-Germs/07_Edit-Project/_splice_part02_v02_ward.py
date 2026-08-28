#!/usr/bin/env python3
"""Replace only 0:53–1:01 of Part 02 v01 with plate 08 I2V. Audio from v01."""
from __future__ import annotations

import subprocess
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
SRC = Path("/opt/cursor/artifacts/hos_001_part02_rough_v01.mp4")
PLATE = PROJ / "04_Generated-Clips/part02/raw/v01_flow/08_ward_vs_lens_v02.mp4"
OUT = PROJ / "09_Final-Export/hos_001_part02_rough_v02.mp4"
ART = Path("/opt/cursor/artifacts")
T0 = 53.0
T1 = 61.0


def encode_phone(src: Path, dest: Path, w: int, h: int, level: str, crf: str) -> None:
    subprocess.run(
        [
            "ffmpeg", "-y", "-i", str(src),
            "-vf", f"scale={w}:{h}:flags=lanczos,format=yuv420p",
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-profile:v", "baseline", "-level", level, "-bf", "0", "-crf", crf,
            "-c:a", "aac", "-profile:a", "aac_low", "-b:a", "160k", "-ac", "2", "-ar", "44100",
            "-movflags", "+faststart", "-brand", "mp42", str(dest),
        ],
        check=True,
    )


def main() -> None:
    if not SRC.exists():
        raise SystemExit(f"missing source {SRC}")
    if not PLATE.exists():
        raise SystemExit(f"missing plate {PLATE}")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fc = (
        f"[1:v]trim=0:8,setpts=PTS-STARTPTS,scale=1280:720:force_original_aspect_ratio=decrease,"
        f"pad=1280:720:(ow-iw)/2:(oh-ih)/2,fps=24,format=yuv420p,setsar=1[new];"
        f"[0:v]trim=0:{T0},setpts=PTS-STARTPTS,fps=24,format=yuv420p,setsar=1[pre];"
        f"[0:v]trim=start={T1},setpts=PTS-STARTPTS,fps=24,format=yuv420p,setsar=1[post];"
        f"[pre][new][post]concat=n=3:v=1:a=0[v]"
    )
    subprocess.run(
        [
            "ffmpeg", "-y", "-i", str(SRC), "-i", str(PLATE),
            "-filter_complex", fc,
            "-map", "[v]", "-map", "0:a",
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-profile:v", "baseline", "-level", "3.1", "-bf", "0",
            "-preset", "fast", "-crf", "18",
            "-c:a", "copy",
            "-movflags", "+faststart", "-brand", "mp42", str(OUT),
        ],
        check=True,
    )
    ART.mkdir(parents=True, exist_ok=True)
    subprocess.run(["cp", "-f", str(OUT), str(ART / OUT.name)], check=True)
    phone = ART / "hos_001_part02_rough_v02_PHONE_480.mp4"
    encode_phone(OUT, phone, 854, 480, "3.0", "20")
    print(f"SAVED {OUT}", flush=True)
    print(f"SAVED {ART / OUT.name}", flush=True)
    print(f"SAVED {phone}", flush=True)


if __name__ == "__main__":
    main()
