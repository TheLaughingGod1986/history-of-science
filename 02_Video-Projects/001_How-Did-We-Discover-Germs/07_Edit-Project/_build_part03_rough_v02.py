#!/usr/bin/env python3
"""Part 03 v10 rough — Bad Air vs Living Seeds.

Chapter after moving picture: A childbirth ward, 1840s (left / Didot).
Drier bed. No cough. No metal tray. Flask SFX only on plate 10.
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
PLATES_JSON = PROJ / "07_Edit-Project/parts/part-03_plates_v02.json"
RAW = PROJ / "04_Generated-Clips/part03/raw/v02_fast_probe"
VO = PROJ / "02_Voiceover/part03_childbirth_ward_v01.wav"
ALIGN = PROJ / "02_Voiceover/part03_childbirth_ward_v01_align.json"
SWIFT = PROJ / "07_Edit-Project/_render_part01_side_label.swift"
LABEL_DIR = PROJ / "06_Sound-Effects/v02_part03_labels"
FX_DIR = PROJ / "06_Sound-Effects/v02_part03_fx"
MUSIC = PROJ / "05_Music"
BED_SRC = MUSIC / "hos_001_part01_ominous_ward_v12.wav"
BED = MUSIC / "hos_001_part03_dry_ward_v01.wav"
P01_SFX = PROJ / "06_Sound-Effects/v12"
OUT = PROJ / "09_Final-Export/hos_001_part03_rough_v10.mp4"
ICLOUD = Path(
    "/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/HOS UAT"
)
CLIP_USE = 7.50
XFADE = 0.40
FPS = 24
FADE = 14 / 24
HOLD = 4.20
CHAPTER = ("chapter", "A childbirth ward, 1840s", 1.50, 5.00, "left")
CLIP_VERS = ("v10", "v09", "v05", "v04", "v03", "v02")
NEEDLES = [
    ("living_seeds", "LIVING SEEDS", "living seeds", "right"),
    ("hitchhiker", "HITCHHIKER", "hitchhiker", "right"),
    ("semmelweis", "SEMMELWEIS", "semmelweis", "right"),
    ("handwashing", "HANDWASHING", "handwashing", "right"),
    ("the_vector", "THE VECTOR", "you are the vector", "right"),
    ("a_flask", "A FLASK", "flask", "right"),
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


def make_dry_bed() -> None:
    """Shift colour off the P01 funeral pad — drier, tighter, under VO."""
    if not BED_SRC.exists():
        raise SystemExit(f"missing bed source {BED_SRC}")
    ff(
        "-i", str(BED_SRC),
        "-af",
        "highpass=f=160,lowpass=f=2200,acompressor=threshold=-22dB:ratio=3:"
        "attack=20:release=180,loudnorm=I=-24:LRA=7:TP=-3,"
        "afade=t=in:d=1.2",
        "-ar", "48000", "-ac", "2", str(BED),
    )


def synth_fx() -> dict[str, Path]:
    FX_DIR.mkdir(parents=True, exist_ok=True)
    wood = FX_DIR / "wood_v01.wav"
    cloth = FX_DIR / "cloth_v01.wav"
    glass = FX_DIR / "glass_v01.wav"
    flask = FX_DIR / "flask_v01.wav"
    ff(
        "-f", "lavfi",
        "-i",
        "aevalsrc=0.60*sin(2*PI*88*t)*exp(-12*t)+0.20*sin(2*PI*140*t)*exp(-16*t)"
        ":d=0.38:s=48000",
        "-af", "lowpass=f=380,volume=0.48", "-ac", "2", str(wood),
    )
    ff(
        "-f", "lavfi", "-i", "anoisesrc=color=brown:duration=0.70:sample_rate=48000",
        "-af",
        "highpass=f=260,lowpass=f=2100,tremolo=f=13:d=0.5,volume=0.38,"
        "afade=t=in:d=0.04,afade=t=out:st=0.38:d=0.32",
        "-ac", "2", str(cloth),
    )
    ff(
        "-f", "lavfi",
        "-i",
        "aevalsrc=0.38*sin(2*PI*1240*t)*exp(-16*t)+0.16*sin(2*PI*1860*t)*exp(-22*t)"
        ":d=0.32:s=48000",
        "-af", "highpass=f=700,lowpass=f=3200,volume=0.32", "-ac", "2", str(glass),
    )
    ff(
        "-f", "lavfi",
        "-i",
        "aevalsrc=0.28*sin(2*PI*740*t)*exp(-9*t)+0.14*sin(2*PI*1480*t)*exp(-14*t)"
        ":d=0.55:s=48000",
        "-af", "highpass=f=400,lowpass=f=2600,aecho=0.6:0.5:18:0.25,volume=0.36",
        "-ac", "2", str(flask),
    )
    return {"wood": wood, "cloth": cloth, "glass": glass, "flask": flask}


def main() -> None:
    plates = json.loads(PLATES_JSON.read_text())["plates"]
    clips = []
    for p in plates:
        chosen = None
        for ver in CLIP_VERS:
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
    pic_dur = n * CLIP_USE - (n - 1) * XFADE
    cut = min(pic_dur, vo_dur + 0.80)
    align = json.loads(ALIGN.read_text()) if ALIGN.exists() else {}

    LABEL_DIR.mkdir(parents=True, exist_ok=True)
    bin_path = Path("/tmp/render_part01_side_label")
    subprocess.run(["swiftc", "-O", "-o", str(bin_path), str(SWIFT)], check=True)

    spoken: list[tuple[str, str, float, str]] = []
    for slug, text, needle, side in NEEDLES:
        t_in = phrase_time(align, needle)
        spoken.append((slug, text, t_in, side))
    spoken.sort(key=lambda x: x[2])
    cards: list[tuple[str, str, float, float, str]] = [CHAPTER]
    print(
        f"CARD {CHAPTER[1]} {CHAPTER[2]:.2f}-{CHAPTER[3]:.2f} {CHAPTER[4]}",
        flush=True,
    )
    for i, (slug, text, t_in, side) in enumerate(spoken):
        nxt = spoken[i + 1][2] if i + 1 < len(spoken) else cut
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
            f"[{i}:v]trim=0:{CLIP_USE},setpts=PTS-STARTPTS,"
            f"scale=1280:720:force_original_aspect_ratio=decrease,"
            f"pad=1280:720:(ow-iw)/2:(oh-ih)/2,fps={FPS},format=yuv420p[v{i}]"
        )
    vprev = "v0"
    offset = CLIP_USE - XFADE
    for i in range(1, n):
        out = f"vx{i}"
        parts.append(
            f"[{vprev}][v{i}]xfade=transition=fade:duration={XFADE}:offset={offset:.3f}[{out}]"
        )
        vprev = out
        offset += CLIP_USE - XFADE
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

    make_dry_bed()
    fx = synth_fx()
    walla = P01_SFX / "walla_ward_v12.wav"
    room = P01_SFX / "room_ward_v12.wav"
    vo_i = len(pngs) + 1
    bed_i = vo_i + 1
    walla_i = bed_i + 1
    room_i = walla_i + 1
    wood_i = room_i + 1
    cloth_i = wood_i + 1
    glass_i = cloth_i + 1
    flask_i = glass_i + 1
    overlay_in += [
        "-i", str(VO),
        "-i", str(BED),
        "-i", str(walla),
        "-i", str(room),
        "-i", str(fx["wood"]),
        "-i", str(fx["cloth"]),
        "-i", str(fx["glass"]),
        "-i", str(fx["flask"]),
    ]
    flask_at = phrase_time(align, "flask")
    flask_ms = int(round(flask_at * 1000))
    # No cough. No metal. Flask only when VO says flask (plate 10).
    ov_parts.append(
        f"[{vo_i}:a]aformat=sample_fmts=fltp:channel_layouts=stereo,"
        f"apad=whole_dur={cut:.6f},atrim=0:{cut:.6f},asplit=2[vo][sc];"
        f"[{bed_i}:a]atrim=0:{cut:.6f},asetpts=PTS-STARTPTS,volume=0.11[bed];"
        f"[{walla_i}:a]atrim=0:{cut:.6f},volume=0.06[walla_raw];"
        f"[walla_raw][sc]sidechaincompress=threshold=0.025:ratio=10:attack=12:"
        f"release=220:makeup=1.2[walla];"
        f"[{room_i}:a]atrim=0:{cut:.6f},volume=0.04[room];"
        f"[{wood_i}:a]asplit=3[w0][w1][w2];"
        f"[w0]adelay=2100|2100,volume=0.08[wood1];"
        f"[w1]adelay=22500|22500,volume=0.08[wood2];"
        f"[w2]adelay=52000|52000,volume=0.07[wood3];"
        f"[{cloth_i}:a]asplit=3[k0][k1][k2];"
        f"[k0]adelay=8500|8500,volume=0.09[cloth1];"
        f"[k1]adelay=30000|30000,volume=0.09[cloth2];"
        f"[k2]adelay=45500|45500,volume=0.08[cloth3];"
        f"[{glass_i}:a]asplit=2[g0][g1];"
        f"[g0]adelay=6200|6200,volume=0.06[glass1];"
        f"[g1]adelay=34800|34800,volume=0.06[glass2];"
        f"[{flask_i}:a]adelay={flask_ms}|{flask_ms},volume=0.08[flask];"
        f"[vo][bed][walla][room][wood1][wood2][wood3]"
        f"[cloth1][cloth2][cloth3][glass1][glass2][flask]"
        f"amix=inputs=13:duration=first:dropout_transition=0:normalize=0,"
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
        dest = ICLOUD / OUT.name
        subprocess.run(["cp", "-f", str(OUT), str(dest)], check=False)
        print(f"ICLOUD {dest}", flush=True)


if __name__ == "__main__":
    main()
