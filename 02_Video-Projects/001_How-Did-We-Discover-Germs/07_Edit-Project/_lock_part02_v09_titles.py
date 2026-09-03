#!/usr/bin/env python3
"""Part 02 v09 — relock titles to showrunner sheet. Keep existing v09 mix."""
from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
PIC = PROJ / "09_Final-Export/hos_001_part02_rough_v07.mp4"
PIC_SHA = "914406d09b0da92a97432af9f32b88917b837b4e258173ee3f31cd9a1bfb9970"
AUD = PROJ / "09_Final-Export/hos_001_part02_rough_v09.mp4"
OUT = PROJ / "09_Final-Export/hos_001_part02_rough_v09.mp4"
TMP = PROJ / "06_Sound-Effects/v09_part02_fx/_v09_mix.wav"
SWIFT = Path(__file__).resolve().parent / "_render_part01_side_label.swift"
LABEL_DIR = PROJ / "06_Sound-Effects/v08_part02_labels"
ART = Path(
    "/Users/benjaminoats/Library/Application Support/Cursor/"
    "AgentStores/cursor_agent_stores/bc-eb2a62e0-1899-43b0-9cd2-0b96209c2bd0/"
    "files/artifacts"
)
ICLOUD = Path(
    "/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/HOS UAT"
)
FADE = 14 / 24
HOLD = 4.20
CARDS = [
    ("drop_pond_water", "A drop of pond water", 1.50, 5.00, "right"),
    ("pond_water", "POND WATER", 7.00, 7.00 + HOLD, "right"),
    ("cells", "CELLS", 12.84, 12.84 + HOLD, "right"),
    ("microbes", "MICROBES", 35.80, 35.80 + HOLD, "right"),
    ("microscope", "MICROSCOPE", 43.34, 43.34 + HOLD, "right"),
    ("slap", "SLAP", 74.98, 76.35, "left"),
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
    if sha256(PIC) != PIC_SHA:
        raise SystemExit("v07 picture sha mismatch — abort")
    if not AUD.exists():
        raise SystemExit("missing current v09 mix")
    dur = probe_dur(PIC)
    TMP.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg", "-y", "-i", str(AUD),
            "-vn", "-ac", "2", "-ar", "48000", str(TMP),
        ],
        check=True,
        capture_output=True,
    )
    bin_path = Path("/tmp/render_part01_side_label")
    subprocess.run(["swiftc", "-O", "-o", str(bin_path), str(SWIFT)], check=True)
    inputs: list[str] = ["-i", str(PIC), "-i", str(TMP)]
    parts: list[str] = []
    last = "0:v"
    for i, (slug, text, t_in, t_out, side) in enumerate(CARDS):
        t_out = min(t_out, dur - 0.02)
        hold = t_out - t_in
        fade = min(FADE, hold / 3)
        png = LABEL_DIR / f"{slug}.png"
        subprocess.run([str(bin_path), text, str(png), side], check=True)
        print(f"CARD {text} {t_in:.2f}-{t_out:.2f} {side}", flush=True)
        idx = i + 2
        inputs += ["-loop", "1", "-t", f"{hold:.4f}", "-i", str(png)]
        parts.append(
            f"[{idx}:v]format=rgba,"
            f"fade=t=in:st=0:d={fade:.3f}:alpha=1,"
            f"fade=t=out:st={hold - fade:.3f}:d={fade:.3f}:alpha=1,"
            f"setpts=PTS+{t_in:.3f}/TB[l{i}]"
        )
        nxt = f"v{i}"
        parts.append(f"[{last}][l{i}]overlay=0:0:eof_action=pass[{nxt}]")
        last = nxt
    parts.append(f"[{last}]format=yuv420p,setsar=1[v]")
    fc = ";".join(parts)
    dest = OUT.with_name("hos_001_part02_rough_v09_tmp.mp4")
    subprocess.run(
        [
            "ffmpeg", "-y", *inputs,
            "-filter_complex", fc,
            "-map", "[v]", "-map", "1:a",
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-profile:v", "baseline", "-level", "3.1", "-bf", "0",
            "-preset", "fast", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
            "-movflags", "+faststart", "-brand", "mp42",
            str(dest),
        ],
        check=True,
    )
    dest.replace(OUT)
    print(f"SAVED {OUT}", flush=True)
    print(f"SIZE {OUT.stat().st_size}", flush=True)
    print(f"SHA256 {sha256(OUT)}", flush=True)
    print(f"DUR {probe_dur(OUT):.3f}", flush=True)
    ART.mkdir(parents=True, exist_ok=True)
    subprocess.run(["cp", "-f", str(OUT), str(ART / OUT.name)], check=True)
    if ICLOUD.parent.exists():
        ICLOUD.mkdir(parents=True, exist_ok=True)
        subprocess.run(["cp", "-f", str(OUT), str(ICLOUD / OUT.name)], check=False)


if __name__ == "__main__":
    main()
