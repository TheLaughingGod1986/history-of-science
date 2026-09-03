#!/usr/bin/env python3
"""Part 01 v16 — titles only. v15 picture/mix/titles + one house-open card."""
from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
SRC = PROJ / "09_Final-Export/hos_001_part01_rough_v15.mp4"
SRC_SHA = "f5ad3ff53e859c412af1881d8e8f497809a19978edeb392aa8fac303cf5b309e"
OUT = PROJ / "09_Final-Export/hos_001_part01_rough_v16.mp4"
SWIFT = Path(__file__).resolve().parent / "_render_part01_side_label.swift"
LABEL_DIR = PROJ / "06_Sound-Effects/v16_labels"
ART = Path(
    "/Users/benjaminoats/Library/Application Support/Cursor/"
    "AgentStores/cursor_agent_stores/bc-eb2a62e0-1899-43b0-9cd2-0b96209c2bd0/"
    "files/artifacts"
)
ICLOUD = Path(
    "/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/HOS UAT"
)
FADE = 14 / 24  # same 14-frame fade as v15
# Existing five stay baked on v15. Only the new open card is added.
OPEN = ("death_ward_1840s", "A death ward, 1840s", 1.50, 5.00)
KEPT = [
    ("INVISIBLE LIFE", 15.06, 19.26),
    ("SEPTIC", 26.48, 30.68),
    ("GERMS", 38.70, 42.90),
    ("FEVER", 59.28, 63.48),
    ("LIVING CLOUD", 67.02, 71.22),
]


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
        raise SystemExit(f"missing source {SRC}")
    got = sha256(SRC)
    if got != SRC_SHA:
        raise SystemExit(f"v15 sha mismatch: {got}")
    LABEL_DIR.mkdir(parents=True, exist_ok=True)
    bin_path = Path("/tmp/render_part01_side_label")
    subprocess.run(["swiftc", "-O", "-o", str(bin_path), str(SWIFT)], check=True)

    slug, text, t_in, t_out = OPEN
    png = LABEL_DIR / f"{slug}.png"
    # Dark negative space (upper-left) — open lamp occupies upper-right.
    subprocess.run([str(bin_path), text, str(png), "left"], check=True)
    hold = t_out - t_in
    fade = min(FADE, hold / 3)
    fc = (
        f"[1:v]format=rgba,"
        f"fade=t=in:st=0:d={fade:.3f}:alpha=1,"
        f"fade=t=out:st={hold - fade:.3f}:d={fade:.3f}:alpha=1,"
        f"setpts=PTS+{t_in:.3f}/TB[l0];"
        f"[0:v][l0]overlay=0:0:eof_action=pass,format=yuv420p,setsar=1[v]"
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg", "-y",
            "-i", str(SRC),
            "-loop", "1", "-t", f"{hold:.4f}", "-i", str(png),
            "-filter_complex", fc,
            "-map", "[v]", "-map", "0:a",
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-profile:v", "baseline", "-level", "3.1", "-bf", "0",
            "-preset", "fast", "-crf", "18",
            "-c:a", "copy",
            "-movflags", "+faststart", "-brand", "mp42",
            str(OUT),
        ],
        check=True,
    )
    print(f"SAVED {OUT}", flush=True)
    print(f"SIZE {OUT.stat().st_size}", flush=True)
    print(f"SHA256 {sha256(OUT)}", flush=True)
    print(f"DUR {probe_dur(OUT):.3f}", flush=True)
    print(f"OPEN {text} {t_in:.2f}-{t_out:.2f}", flush=True)
    for name, a, b in KEPT:
        print(f"KEEP {name} {a:.2f}-{b:.2f}", flush=True)
    ART.mkdir(parents=True, exist_ok=True)
    subprocess.run(["cp", "-f", str(OUT), str(ART / OUT.name)], check=True)
    if ICLOUD.parent.exists():
        ICLOUD.mkdir(parents=True, exist_ok=True)
        subprocess.run(["cp", "-f", str(OUT), str(ICLOUD / OUT.name)], check=False)


if __name__ == "__main__":
    main()
