#!/usr/bin/env python3
"""HOS Buffer social masters: strip end CTA (+ use non-pill 002).

CoS guardrail (5 Oct): no long still at end. If CTA arrives after last VO,
hard-cut there. Freeze only if VO overlaps CTA, and only ≤1.0s.
002 from punch (no title pill). Full last VO line kept.
"""
from __future__ import annotations
import hashlib, json, subprocess, tempfile, wave
from pathlib import Path
from PIL import Image
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
P001 = ROOT / "001_How-Did-We-Discover-Germs" / "10_Shorts"
P002 = ROOT / "002_How-Did-We-Discover-The-Periodic-Table" / "10_Shorts"
OUT_DIR = ROOT / "_Buffer-Backlog" / "social_masters_v01"
ICLOUD = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT/Buffer-Backlog/social_masters_v01"
STILLS = OUT_DIR / "stills"
BAND_H = 300
MAX_FREEZE_S = 1.0

JOBS = [
    (P001 / "hos_001_s01_shadow_punch_v02.mp4", "hos_001_s01_shadow_punch_social_v01.mp4"),
    (P001 / "hos_001_s02_pond_punch_v02.mp4", "hos_001_s02_pond_punch_social_v01.mp4"),
    (P001 / "hos_001_s03_vector_punch_v02.mp4", "hos_001_s03_vector_punch_social_v01.mp4"),
    (P001 / "hos_001_s04_flask_punch_v02.mp4", "hos_001_s04_flask_punch_social_v01.mp4"),
    (P001 / "hos_001_s05_soap_punch_v03.mp4", "hos_001_s05_soap_punch_social_v01.mp4"),
    (P002 / "hos_002_s01_empty_chairs_punch_v01.mp4", "hos_002_s01_empty_chairs_punch_social_v01.mp4"),
    (P002 / "hos_002_s02_predict_metal_punch_v01.mp4", "hos_002_s02_predict_metal_punch_social_v01.mp4"),
    (P002 / "hos_002_s03_gallium_punch_v01.mp4", "hos_002_s03_gallium_punch_social_v01.mp4"),
    (P002 / "hos_002_s04_tellurium_punch_v01.mp4", "hos_002_s04_tellurium_punch_social_v01.mp4"),
    (P002 / "hos_002_s05_other_table_punch_v01.mp4", "hos_002_s05_other_table_punch_social_v01.mp4"),
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

def grab(src: Path, t: float, dest: Path) -> None:
    subprocess.run(
        ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
         "-ss", f"{t:.3f}", "-i", str(src), "-frames:v", "1", "-q:v", "2", str(dest)],
        check=True,
    )

def band_white(path: Path) -> float:
    im = np.array(Image.open(path).convert("L"))
    h, w = im.shape
    band = im[h - BAND_H : h - 40, int(w * 0.12) : int(w * 0.88)]
    return float((band > 200).mean())

def last_audio_s(src: Path) -> float:
    wav = Path(tempfile.mkdtemp(prefix="vo_")) / "a.wav"
    subprocess.run(
        ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(src),
         "-ac", "1", "-ar", "16000", str(wav)],
        check=True,
    )
    with wave.open(str(wav), "rb") as w:
        sr = w.getframerate()
        data = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64)
    win = int(0.25 * sr)
    last = 0.0
    for i in range(0, max(0, len(data) - win), win):
        rms = float(np.sqrt((data[i : i + win] ** 2).mean()) + 1e-9)
        db = 20 * np.log10(rms / 32768)
        if db > -45:
            last = (i + win) / sr
    wav.unlink()
    wav.parent.rmdir()
    return last

def detect_cta_in(src: Path, total: float) -> float:
    default = max(total - 4.0, 14.0)
    tmp = Path(tempfile.mkdtemp(prefix="cta_det_"))
    samples = []
    t = max(0.0, total - 7.0)
    while t < total - 0.05:
        fp = tmp / f"{t:.2f}.jpg"
        grab(src, t, fp)
        samples.append((t, band_white(fp)))
        t += 0.25
    n = max(1, len(samples) // 3)
    base = float(np.median([w for _, w in samples[:n]]))
    thr = max(0.025, base + 0.02)
    onset = None
    if samples[-1][1] >= thr or (len(samples) > 1 and samples[-2][1] >= thr):
        i = len(samples) - 1
        while i >= 0 and samples[i][1] >= thr * 0.65:
            onset = samples[i][0]
            i -= 1
    cta_in = min(default, onset - 0.15) if onset is not None else default
    cta_in = max(8.0, min(cta_in, total - 0.5))
    for p in tmp.glob("*"):
        p.unlink()
    tmp.rmdir()
    return round(cta_in, 3)

def make_social(src: Path, dest: Path) -> dict:
    total = probe(src)
    cta_in = detect_cta_in(src, total)
    vo_end = last_audio_s(src)
    # Default CoS path: CTA after VO → hard cut at CTA (no freeze).
    freeze_s = 0.0
    freeze_at = None
    if vo_end <= cta_in + 0.12:
        cut_at = cta_in
        mode = "hard_cut_at_cta"
    else:
        # VO overlaps CTA: keep through VO end; freeze clean frame ≤1s over the overlap.
        overlap = vo_end - cta_in
        if overlap > MAX_FREEZE_S + 0.05:
            raise SystemExit(
                f"{src.name}: VO overlaps CTA by {overlap:.2f}s (> {MAX_FREEZE_S}s); need remake from raw"
            )
        cut_at = vo_end
        freeze_s = overlap
        freeze_at = max(0.5, cta_in - 0.12)
        # walk back if freeze frame already has CTA white
        tmp = Path(tempfile.mkdtemp(prefix="fr_"))
        for _ in range(10):
            fp = tmp / "f.jpg"
            grab(src, freeze_at, fp)
            if band_white(fp) < 0.03:
                break
            freeze_at = max(0.5, freeze_at - 0.25)
        for p in tmp.glob("*"):
            p.unlink()
        tmp.rmdir()
        mode = "short_freeze_then_cut"

    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        dest.unlink()

    if freeze_s <= 0.05:
        # Simple trim — video+audio to cut_at
        subprocess.run(
            [
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-i", str(src),
                "-t", f"{cut_at:.3f}",
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "18", "-r", "24",
                "-c:a", "aac", "-b:a", "192k",
                "-movflags", "+faststart",
                str(dest),
            ],
            check=True,
        )
    else:
        head = cta_in
        rem = freeze_s
        fc = (
            f"[0:v]trim=0:{head:.3f},setpts=PTS-STARTPTS[vhead];"
            f"[0:v]trim={freeze_at:.3f}:{freeze_at + 0.04:.3f},loop=loop=-1:size=1:start=0,"
            f"setpts=N/24/TB,trim=duration={rem:.3f},setpts=PTS-STARTPTS[vtail];"
            f"[vhead][vtail]concat=n=2:v=1:a=0[v];"
            f"[0:a]atrim=0:{cut_at:.3f},asetpts=PTS-STARTPTS[a]"
        )
        subprocess.run(
            [
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-i", str(src),
                "-filter_complex", fc,
                "-map", "[v]", "-map", "[a]",
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "18", "-r", "24",
                "-c:a", "aac", "-b:a", "192k",
                "-t", f"{cut_at:.3f}",
                "-movflags", "+faststart",
                str(dest),
            ],
            check=True,
        )

    STILLS.mkdir(parents=True, exist_ok=True)
    stem = dest.stem
    d = probe(dest)
    for name, ss in (("mid", d * 0.4), ("near_end", max(0, d - 0.8)), ("last", max(0, d - 0.15))):
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
        "cta_in_s": cta_in,
        "vo_end_s": round(vo_end, 3),
        "cut_at_s": round(cut_at, 3),
        "freeze_s": round(freeze_s, 3),
        "mode": mode,
        "end_band_white": round(end_w, 4),
        "method": "hard_cut_at_cta_or_short_freeze_le_1s; audio through last VO; 002 from punch (no pill)",
    }

def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ICLOUD.mkdir(parents=True, exist_ok=True)
    rows = []
    for src, name in JOBS:
        if not src.exists():
            raise SystemExit(f"missing {src}")
        dest = OUT_DIR / name
        print(f"MAKE {name} from {src.name} …", flush=True)
        row = make_social(src, dest)
        (ICLOUD / name).write_bytes(dest.read_bytes())
        print(
            f"  sha {row['sha256'][:16]}…  {row['duration_s']}s  mode={row['mode']} "
            f"cta={row['cta_in_s']} vo={row['vo_end_s']} freeze={row['freeze_s']} endW={row['end_band_white']}",
            flush=True,
        )
        rows.append(row)
    meta = {"ver": "social_v01", "n": len(rows), "shorts": rows}
    (OUT_DIR / "SOCIAL_MASTERS_v01.json").write_text(json.dumps(meta, indent=2) + "\n")
    (ICLOUD / "SOCIAL_MASTERS_v01.json").write_text(json.dumps(meta, indent=2) + "\n")
    ic_stills = ICLOUD / "stills"
    ic_stills.mkdir(parents=True, exist_ok=True)
    for p in STILLS.glob("*.jpg"):
        (ic_stills / p.name).write_bytes(p.read_bytes())
    print("DONE", len(rows), flush=True)

if __name__ == "__main__":
    main()
