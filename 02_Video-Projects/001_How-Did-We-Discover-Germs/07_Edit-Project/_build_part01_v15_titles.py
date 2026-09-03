#!/usr/bin/env python3
"""Part 01 v15 — titles only. v10 picture (no center stamp) + v14 audio."""
from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
PIC = PROJ / "09_Final-Export/hos_001_part01_rough_v10.mp4"
AUD = PROJ / "09_Final-Export/hos_001_part01_rough_v14.mp4"
FALLBACK = PROJ / "09_Final-Export/hos_001_part01_rough_v12.mp4"
OUT = PROJ / "09_Final-Export/hos_001_part01_rough_v15.mp4"
SWIFT = Path(__file__).resolve().parent / "_render_part01_side_label.swift"
LABEL_DIR = PROJ / "06_Sound-Effects/v15_labels"
ART = Path(
    "/Users/benjaminoats/Library/Application Support/Cursor/"
    "AgentStores/cursor_agent_stores/bc-eb2a62e0-1899-43b0-9cd2-0b96209c2bd0/"
    "files/artifacts"
)
ICLOUD = Path(
    "/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/HOS UAT"
)
FADE = 14 / 24  # soft fade on/off — not a snap
# Same five cards and in-times. Hold ~4.2s, off before the next.
LABELS = [
    ("invisible_life", "INVISIBLE LIFE", 15.06, 19.26),
    ("septic", "SEPTIC", 26.48, 30.68),
    ("germs", "GERMS", 38.70, 42.90),
    ("fever", "FEVER", 59.28, 63.48),
    ("living_cloud", "LIVING CLOUD", 67.02, 71.22),
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
    src_pic = PIC if PIC.exists() else None
    src_aud = AUD if AUD.exists() else FALLBACK
    if src_pic is None:
        raise SystemExit("missing v10 picture (needed to retire center stamp)")
    if not src_aud.exists():
        raise SystemExit("missing v14/v12 audio source")
    LABEL_DIR.mkdir(parents=True, exist_ok=True)
    bin_path = Path("/tmp/render_part01_side_label")
    subprocess.run(["swiftc", "-O", "-o", str(bin_path), str(SWIFT)], check=True)

    pngs: list[tuple[Path, float, float]] = []
    for slug, text, t_in, t_out in LABELS:
        png = LABEL_DIR / f"{slug}.png"
        subprocess.run([str(bin_path), text, str(png)], check=True)
        pngs.append((png, t_in, t_out))
        print(f"LABEL {text} {t_in:.2f}-{t_out:.2f}", flush=True)

    inputs: list[str] = ["-i", str(src_pic), "-i", str(src_aud)]
    parts: list[str] = []
    last = "0:v"
    for i, (png, t_in, t_out) in enumerate(pngs):
        hold = t_out - t_in
        fade = min(FADE, hold / 3)
        idx = i + 2
        inputs += ["-loop", "1", "-t", f"{hold:.4f}", "-i", str(png)]
        parts.append(
            f"[{idx}:v]format=rgba,"
            f"fade=t=in:st=0:d={fade:.3f}:alpha=1,"
            f"fade=t=out:st={hold - fade:.3f}:d={fade:.3f}:alpha=1,"
            f"setpts=PTS+{t_in:.3f}/TB[l{i}]"
        )
        nxt = f"v{i}"
        parts.append(
            f"[{last}][l{i}]overlay=0:0:eof_action=pass[{nxt}]"
        )
        last = nxt
    parts.append(f"[{last}]format=yuv420p,setsar=1[v]")
    fc = ";".join(parts)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg", "-y", *inputs,
            "-filter_complex", fc,
            "-map", "[v]", "-map", "1:a",
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
    ART.mkdir(parents=True, exist_ok=True)
    subprocess.run(["cp", "-f", str(OUT), str(ART / OUT.name)], check=True)
    if ICLOUD.parent.exists():
        ICLOUD.mkdir(parents=True, exist_ok=True)
        subprocess.run(["cp", "-f", str(OUT), str(ICLOUD / OUT.name)], check=False)


if __name__ == "__main__":
    main()
