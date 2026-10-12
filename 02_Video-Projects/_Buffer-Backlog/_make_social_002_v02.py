#!/usr/bin/env python3
"""HOS 002 social v02: hard-cut on last VO frame. No silent tail. No freeze. Keep film-title text. Zero CTA."""
from __future__ import annotations
import hashlib, json, subprocess, tempfile, wave
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
P002 = ROOT / "002_How-Did-We-Discover-The-Periodic-Table" / "10_Shorts"
OUT = ROOT / "_Buffer-Backlog" / "social_masters_v01"
ICLOUD = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT/Buffer-Backlog/social_masters_v01"
STILLS = OUT / "stills"

JOBS = [
    ("hos_002_s01_empty_chairs_punch_v01.mp4", "hos_002_s01_empty_chairs_punch_social_v02.mp4"),
    ("hos_002_s02_predict_metal_punch_v01.mp4", "hos_002_s02_predict_metal_punch_social_v02.mp4"),
    ("hos_002_s03_gallium_punch_v01.mp4", "hos_002_s03_gallium_punch_social_v02.mp4"),
    ("hos_002_s04_tellurium_punch_v01.mp4", "hos_002_s04_tellurium_punch_social_v02.mp4"),
    ("hos_002_s05_other_table_punch_v01.mp4", "hos_002_s05_other_table_punch_social_v02.mp4"),
]

def probe(p: Path) -> float:
    return float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)], text=True
    ).strip())

def sha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def last_vo_s(src: Path, thr: float = -40.0) -> float:
    wav = Path(tempfile.mkdtemp(prefix="vo_")) / "a.wav"
    subprocess.run(
        ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(src),
         "-ac", "1", "-ar", "16000", str(wav)],
        check=True,
    )
    with wave.open(str(wav), "rb") as w:
        sr = w.getframerate()
        data = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64)
    win = int(0.05 * sr)
    last = 0.0
    for i in range(0, max(0, len(data) - win), win):
        rms = float(np.sqrt((data[i : i + win] ** 2).mean()) + 1e-9)
        db = 20 * np.log10(rms / 32768)
        if db > thr:
            last = (i + win) / sr
    wav.unlink()
    wav.parent.rmdir()
    return last

def band_white(jpg: Path) -> float:
    im = np.array(Image.open(jpg).convert("L"))
    h, w = im.shape
    band = im[h - 300 : h - 40, int(w * 0.12) : int(w * 0.88)]
    return float((band > 200).mean())

def make(src: Path, dest: Path) -> dict:
    total = probe(src)
    vo = last_vo_s(src)
    # End on last VO frame; tiny pad so last syllable isn't clipped (≤1 frame @24fps)
    cut = min(total - 0.02, vo + 0.04)
    # Safety: never extend into known CTA window (builder last ~4s) if VO detect is late
    cta_default = max(total - 4.0, 14.0)
    if cut > cta_default:
        cut = cta_default
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        dest.unlink()
    subprocess.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(src),
            "-t", f"{cut:.3f}",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "18", "-r", "24",
            "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart",
            str(dest),
        ],
        check=True,
    )
    STILLS.mkdir(parents=True, exist_ok=True)
    stem = dest.stem
    d = probe(dest)
    for name, ss in (("mid", d * 0.4), ("near_end", max(0, d - 0.6)), ("last", max(0, d - 0.08))):
        sp = STILLS / f"{stem}_{name}.jpg"
        subprocess.run(
            ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
             "-ss", f"{ss:.3f}", "-i", str(dest), "-frames:v", "1", "-q:v", "3", str(sp)],
            check=True,
        )
    end_w = band_white(STILLS / f"{stem}_last.jpg")
    return {
        "src": src.name,
        "social": dest.name,
        "sha256": sha(dest),
        "duration_s": round(d, 3),
        "src_duration_s": round(total, 3),
        "vo_end_s": round(vo, 3),
        "cut_at_s": round(cut, 3),
        "freeze_s": 0.0,
        "mode": "hard_cut_at_last_vo",
        "end_band_white": round(end_w, 4),
        "method": "hard cut at last VO frame (+40ms); no freeze; no silent tail; keep film-title text; strip CTA by ending before it",
    }

def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    ICLOUD.mkdir(parents=True, exist_ok=True)
    rows = []
    for src_name, out_name in JOBS:
        src = P002 / src_name
        dest = OUT / out_name
        print(f"MAKE {out_name} …", flush=True)
        row = make(src, dest)
        (ICLOUD / out_name).write_bytes(dest.read_bytes())
        print(
            f"  sha {row['sha256'][:16]}… dur={row['duration_s']} vo={row['vo_end_s']} "
            f"cut={row['cut_at_s']} endW={row['end_band_white']}",
            flush=True,
        )
        if row["end_band_white"] > 0.05:
            print("  WARN end band still hot — check stills", flush=True)
        rows.append(row)
    # merge into manifest
    man = OUT / "SOCIAL_MASTERS_v01.json"
    meta = json.loads(man.read_text()) if man.exists() else {"ver": "social_v01", "shorts": []}
    meta["ver"] = "social_v01+002_v02"
    meta["002_v02"] = rows
    meta["parked"] = ["hos_001_s01 (broken punch audio)", "hos_001_s05 (holds+silence+CTA in punch_v01; remake from beds)"]
    # replace any 002 entries with v02 note
    meta["shorts"] = [s for s in meta.get("shorts", []) if not str(s.get("social", "")).startswith("hos_002_")]
    meta["shorts"].extend(rows)
    meta["n"] = len(meta["shorts"])
    man.write_text(json.dumps(meta, indent=2) + "\n")
    (ICLOUD / "SOCIAL_MASTERS_v01.json").write_text(json.dumps(meta, indent=2) + "\n")
    ic_stills = ICLOUD / "stills"
    ic_stills.mkdir(parents=True, exist_ok=True)
    for p in STILLS.glob("hos_002_*_social_v02_*.jpg"):
        (ic_stills / p.name).write_bytes(p.read_bytes())
    print("DONE", len(rows), flush=True)

if __name__ == "__main__":
    main()
