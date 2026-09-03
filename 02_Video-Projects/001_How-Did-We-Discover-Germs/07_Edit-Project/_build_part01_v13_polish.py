#!/usr/bin/env python3
"""Part 01 v13 polish — trim v12 VO tail. No remint. No new layers. No 0:08 recut."""
from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
SRC = PROJ / "09_Final-Export/hos_001_part01_rough_v12.mp4"
OUT = PROJ / "09_Final-Export/hos_001_part01_rough_v13.mp4"
# "shadow" residual through ~60.56; half-beat of air; hard stop. Frame-snap 24 fps.
CUT = 1460 / 24  # 60.833...s
ART = Path(
    "/Users/benjaminoats/Library/Application Support/Cursor/"
    "AgentStores/cursor_agent_stores/bc-eb2a62e0-1899-43b0-9cd2-0b96209c2bd0/"
    "files/artifacts"
)
ICLOUD = Path(
    "/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/HOS UAT"
)


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


def main() -> None:
    if not SRC.exists():
        raise SystemExit(f"missing {SRC}")
    # 12ms click-guard only — not a fade-out ending.
    af = f"afade=t=out:st={CUT - 0.012:.6f}:d=0.012"
    subprocess.run(
        [
            "ffmpeg", "-y",
            "-i", str(SRC),
            "-t", f"{CUT:.8f}",
            "-af", af,
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-profile:v", "baseline", "-level", "3.1", "-bf", "0",
            "-preset", "fast", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
            "-movflags", "+faststart", "-brand", "mp42",
            str(OUT),
        ],
        check=True,
    )
    print(f"CUT {CUT:.6f}", flush=True)
    print(f"SAVED {OUT}", flush=True)
    print(f"SIZE {OUT.stat().st_size}", flush=True)
    print(f"SHA256 {sha256(OUT)}", flush=True)
    print(f"DUR {probe_dur(OUT):.3f}", flush=True)
    ART.mkdir(parents=True, exist_ok=True)
    subprocess.run(["cp", "-f", str(OUT), str(ART / OUT.name)], check=True)
    if ICLOUD.parent.exists():
        ICLOUD.mkdir(parents=True, exist_ok=True)
        subprocess.run(["cp", "-f", str(OUT), str(ICLOUD / OUT.name)], check=False)
    print(f"ART {ART / OUT.name}", flush=True)
    print(f"ICLOUD {ICLOUD / OUT.name}", flush=True)


if __name__ == "__main__":
    main()
