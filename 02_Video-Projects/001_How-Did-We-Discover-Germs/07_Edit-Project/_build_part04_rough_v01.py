#!/usr/bin/env python3
"""Part 04 v13 rough — Proof in a Flask.

Prefer v13 living 0:02 splice on 07 (and 08 if present). Do not overwrite v12.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))
import orbit_gemini_veo as veo  # noqa: E402

PROJ = Path(__file__).resolve().parents[1]
PLATES_JSON = PROJ / "07_Edit-Project/parts/part-04_plates_v01.json"
RAW = PROJ / "04_Generated-Clips/part04/raw/v01_fast_probe"
VO = PROJ / "02_Voiceover/part04_proof_in_a_flask_v01.wav"
ALIGN = PROJ / "02_Voiceover/part04_proof_in_a_flask_v01_align.json"
SWIFT = PROJ / "07_Edit-Project/_render_part01_side_label.swift"
LABEL_DIR = PROJ / "06_Sound-Effects/v01_part04_labels"
FX_DIR = PROJ / "06_Sound-Effects/v01_part04_fx"
MUSIC = PROJ / "05_Music"
BED_SRC = MUSIC / "hos_001_part01_ominous_ward_v14_norm.wav"
BED = MUSIC / "hos_001_part04_lab_bed_v06.wav"
OUT = PROJ / "09_Final-Export/hos_001_part04_rough_v14.mp4"
ICLOUD = Path(
    "/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/HOS UAT"
)
CLIP_USE = 7.50
# v04 start is already-tipped + dry. If Veo invents a pour again, trim here.
CLIP_USE_BY_ID: dict[str, float] = {}
XFADE = 0.40
FPS = 24
FADE = 14 / 24
HOLD = 4.20
CHAPTER = ("chapter", "A swan-neck flask", 1.50, 5.00, "left")
# Locked times — one at a time, off before the next. No PASTEUR.
LABELS = [
    ("swan_neck", "SWAN NECK", 9.17, "right"),
    ("the_curve", "THE CURVE", 14.56, "right"),
    ("still_clear", "STILL CLEAR", 24.15, "right"),
    ("passengers", "PASSENGERS", 39.26, "right"),
    ("an_address", "AN ADDRESS", 77.22, "right"),
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


def ff(*args: str) -> None:
    subprocess.run(["ffmpeg", "-y", *args], check=True, capture_output=True)


def phrase_time(align: dict, needle: str) -> float:
    chars = align.get("characters") or []
    starts = align.get("character_start_times_seconds") or []
    blob = "".join(chars).lower()
    idx = blob.find(needle.lower())
    if idx < 0:
        raise SystemExit(f"needle missing in VO align: {needle}")
    return float(starts[idx])


def make_lab_bed() -> None:
    if not BED_SRC.exists():
        raise SystemExit(f"missing bed source {BED_SRC}")
    ff(
        "-i", str(BED_SRC),
        "-af",
        "highpass=f=90,lowpass=f=1800,acompressor=threshold=-20dB:ratio=3.5:"
        "attack=16:release=140,loudnorm=I=-23:LRA=6:TP=-3,"
        "afade=t=in:d=0.8",
        "-ar", "48000", "-ac", "2", str(BED),
    )


def synth_fx() -> dict[str, Path]:
    FX_DIR.mkdir(parents=True, exist_ok=True)
    glass = FX_DIR / "glass_v01.wav"
    boil = FX_DIR / "boil_v01.wav"
    cloth = FX_DIR / "cloth_v01.wav"
    wood = FX_DIR / "wood_v06.wav"
    ff(
        "-f", "lavfi",
        "-i",
        "aevalsrc=0.55*sin(2*PI*920*t)*exp(-18*t)+0.22*sin(2*PI*1840*t)*exp(-22*t)"
        ":d=0.32:s=48000",
        "-af", "highpass=f=400,lowpass=f=2600,aecho=0.6:0.5:18:0.25,volume=0.36",
        "-ac", "2", str(glass),
    )
    ff(
        "-f", "lavfi", "-i", "anoisesrc=color=pink:duration=8.0:sample_rate=48000",
        "-af",
        "highpass=f=200,lowpass=f=900,tremolo=f=8:d=0.4,volume=0.22,"
        "afade=t=in:d=0.4,afade=t=out:st=7.2:d=0.8",
        "-ac", "2", str(boil),
    )
    ff(
        "-f", "lavfi", "-i", "anoisesrc=color=brown:duration=0.70:sample_rate=48000",
        "-af",
        "highpass=f=260,lowpass=f=2100,tremolo=f=13:d=0.5,volume=0.38,"
        "afade=t=in:d=0.04,afade=t=out:st=0.38:d=0.32",
        "-ac", "2", str(cloth),
    )
    ff(
        "-f", "lavfi", "-i", "anoisesrc=color=brown:duration=0.45:sample_rate=48000",
        "-af",
        "highpass=f=80,lowpass=f=700,tremolo=f=7:d=0.35,volume=0.28,"
        "afade=t=in:d=0.02,afade=t=out:st=0.28:d=0.16",
        "-ac", "2", str(wood),
    )
    return {"glass": glass, "boil": boil, "cloth": cloth, "wood": wood}


def main() -> None:
    plates = json.loads(PLATES_JSON.read_text())["plates"]
    clips = []
    for p in plates:
        chosen = None
        for ver in ("v14", "v13", "v12", "v11", "v10", "v09", "v08", "v07", "v06", "v05", "v04", "v03", "v02"):
            cand = RAW / f"{p['id']}_{ver}.mp4"
            if veo.already_done(cand, min_bytes=400_000):
                chosen = cand
                break
        clips.append(chosen or RAW / f"{p['id']}_v01.mp4")
    missing = [str(c) for c in clips if not veo.already_done(c, min_bytes=400_000)]
    if missing:
        raise SystemExit("missing Fast plates: " + ", ".join(missing))
    if not VO.exists():
        raise SystemExit(f"missing VO {VO}")
    vo_dur = probe_dur(VO)
    n = len(clips)
    uses = [CLIP_USE_BY_ID.get(p["id"], CLIP_USE) for p in plates]
    pic_dur = sum(uses) - (n - 1) * XFADE
    cut = min(pic_dur, vo_dur + 0.80)
    if vo_dur - cut > 1.05:
        raise SystemExit(f"VO {vo_dur:.3f} exceeds picture {cut:.3f} by more than 1s")
    align = json.loads(ALIGN.read_text()) if ALIGN.exists() else {}

    LABEL_DIR.mkdir(parents=True, exist_ok=True)
    bin_path = Path("/tmp/render_part01_side_label")
    subprocess.run(["swiftc", "-O", "-o", str(bin_path), str(SWIFT)], check=True)

    cards: list[tuple[str, str, float, float, str]] = [CHAPTER]
    print(
        f"CARD {CHAPTER[1]} {CHAPTER[2]:.2f}-{CHAPTER[3]:.2f} {CHAPTER[4]}",
        flush=True,
    )
    for i, (slug, text, t_in, side) in enumerate(LABELS):
        nxt = LABELS[i + 1][2] if i + 1 < len(LABELS) else cut
        t_out = min(t_in + HOLD, nxt - 0.20, cut - 0.02)
        if t_out <= t_in + 0.80:
            t_out = min(t_in + max(1.20, nxt - t_in - 0.15), cut - 0.02)
        cards.append((slug, text, t_in, t_out, side))
        print(f"CARD {text} {t_in:.2f}-{t_out:.2f} {side}", flush=True)

    pic = FX_DIR / "_picture_xfade.mp4"
    FX_DIR.mkdir(parents=True, exist_ok=True)
    inputs: list[str] = []
    parts: list[str] = []
    for i, c in enumerate(clips):
        inputs += ["-i", str(c)]
        parts.append(
            f"[{i}:v]trim=0:{uses[i]:.3f},setpts=PTS-STARTPTS,"
            f"scale=1280:720:force_original_aspect_ratio=decrease,"
            f"pad=1280:720:(ow-iw)/2:(oh-ih)/2,fps={FPS},format=yuv420p[v{i}]"
        )
    vprev = "v0"
    offset = uses[0] - XFADE
    for i in range(1, n):
        out = f"vx{i}"
        parts.append(
            f"[{vprev}][v{i}]xfade=transition=fade:duration={XFADE}:offset={offset:.3f}[{out}]"
        )
        vprev = out
        offset += uses[i] - XFADE
    parts.append(f"[{vprev}]trim=0:{cut:.6f},setpts=PTS-STARTPTS,format=yuv420p,setsar=1[vout]")
    ff(
        *inputs,
        "-filter_complex", ";".join(parts),
        "-map", "[vout]",
        "-an",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-profile:v", "baseline", "-level", "3.1", "-bf", "0",
        "-preset", "fast", "-crf", "18",
        "-movflags", "+faststart", str(pic),
    )

    overlay_in: list[str] = ["-i", str(pic)]
    ov_parts: list[str] = []
    last = "0:v"
    pngs: list[tuple[Path, float, float]] = []
    for slug, text, t_in, t_out, side in cards:
        png = LABEL_DIR / f"{slug}.png"
        subprocess.run([str(bin_path), text, str(png), side], check=True)
        pngs.append((png, t_in, t_out))
    for i, (png, t_in, t_out) in enumerate(pngs):
        hold = t_out - t_in
        fade = min(FADE, hold / 3)
        overlay_in += ["-loop", "1", "-t", f"{hold:.4f}", "-i", str(png)]
        ov_parts.append(
            f"[{i+1}:v]format=rgba,"
            f"fade=t=in:st=0:d={fade:.3f}:alpha=1,"
            f"fade=t=out:st={hold - fade:.3f}:d={fade:.3f}:alpha=1,"
            f"setpts=PTS+{t_in:.3f}/TB[l{i}]"
        )
        nxt = f"v{i}"
        ov_parts.append(f"[{last}][l{i}]overlay=0:0:eof_action=pass[{nxt}]")
        last = nxt
    ov_parts.append(f"[{last}]format=yuv420p,setsar=1[v]")

    make_lab_bed()
    fx = synth_fx()
    vo_i = len(pngs) + 1
    bed_i = vo_i + 1
    boil_i = bed_i + 1
    glass_i = boil_i + 1
    cloth_i = glass_i + 1
    wood_i = cloth_i + 1
    overlay_in += [
        "-i", str(VO),
        "-i", str(BED),
        "-i", str(fx["boil"]),
        "-i", str(fx["glass"]),
        "-i", str(fx["cloth"]),
        "-i", str(fx["wood"]),
    ]
    boil_at = phrase_time(align, "boil broth")
    boil_ms = int(round(boil_at * 1000))
    ov_parts.append(
        f"[{vo_i}:a]aformat=sample_fmts=fltp:channel_layouts=stereo,"
        f"apad=whole_dur={cut:.6f},atrim=0:{cut:.6f}[vo];"
        f"[{bed_i}:a]atrim=0:{cut:.6f},asetpts=PTS-STARTPTS,volume=0.13[bed];"
        f"[{boil_i}:a]adelay={boil_ms}|{boil_ms},volume=0.10,atrim=0:{cut:.6f}[boil];"
        f"[{glass_i}:a]asplit=2[g0][g1];"
        f"[g0]adelay=1800|1800,volume=0.07[glass1];"
        f"[g1]adelay=22000|22000,volume=0.07[glass2];"
        f"[{cloth_i}:a]asplit=2[k0][k1];"
        f"[k0]adelay=9000|9000,volume=0.07[cloth1];"
        f"[k1]adelay=36000|36000,volume=0.07[cloth2];"
        f"[{wood_i}:a]asplit=2[w0][w1];"
        f"[w0]adelay=28000|28000,volume=0.06[wood1];"
        f"[w1]adelay=56000|56000,volume=0.06[wood2];"
        f"[vo][bed][boil][glass1][glass2][cloth1][cloth2][wood1][wood2]"
        f"amix=inputs=9:duration=first:dropout_transition=0:normalize=0,"
        f"afade=t=out:st={cut - 0.012:.6f}:d=0.012[a]"
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg", "-y", *overlay_in,
            "-filter_complex", ";".join(ov_parts),
            "-map", "[v]", "-map", "[a]",
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-profile:v", "baseline", "-level", "3.1", "-bf", "0",
            "-preset", "fast", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
            "-movflags", "+faststart", "-brand", "mp42",
            str(OUT),
        ],
        check=True,
    )
    print(f"SAVED {OUT}", flush=True)
    print(f"SIZE {OUT.stat().st_size}", flush=True)
    print(f"SHA256 {sha256(OUT)}", flush=True)
    print(f"DUR {probe_dur(OUT):.3f}", flush=True)
    print(f"VO {vo_dur:.3f} PIC_PLAN {pic_dur:.3f} CUT {cut:.3f}", flush=True)
    if ICLOUD.parent.exists():
        ICLOUD.mkdir(parents=True, exist_ok=True)
        subprocess.run(["cp", "-f", str(OUT), str(ICLOUD / OUT.name)], check=False)
        print(f"ICLOUD {ICLOUD / OUT.name}", flush=True)


if __name__ == "__main__":
    main()
