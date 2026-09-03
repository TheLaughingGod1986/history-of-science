#!/usr/bin/env python3
"""Part 05 v02 rough — Clean Hands, Clean Cuts. UAT remint 04/05/06.

Chapter after moving picture. Labels follow spoken nouns. Ward-family bed, lift at soap.
Do not remint 01–04. Not LOCKED.
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
PLATES_JSON = PROJ / "07_Edit-Project/parts/part-05_plates_v01.json"
RAW = PROJ / "04_Generated-Clips/part05/raw/v01_fast_probe"
VO = PROJ / "02_Voiceover/part05_clean_hands_v01.wav"
ALIGN = PROJ / "02_Voiceover/part05_clean_hands_v01_align.json"
SWIFT = PROJ / "07_Edit-Project/_render_part01_side_label.swift"
LABEL_DIR = PROJ / "06_Sound-Effects/v01_part05_labels"
FX_DIR = PROJ / "06_Sound-Effects/v01_part05_fx"
MUSIC = PROJ / "05_Music"
BED_SRC = MUSIC / "hos_001_part01_ominous_ward_v14_norm.wav"
BED = MUSIC / "hos_001_part05_theatre_bed_v01.wav"
OUT = PROJ / "09_Final-Export/hos_001_part05_rough_v02.mp4"
LOCK04 = PROJ / "09_Final-Export/hos_001_part04_rough_v23.mp4"
LOCK04_SHA = "afe44645ddcfbc649baca52a7720e083d48125d5fd6ca32606b3fb2c951fe763"
ICLOUD = Path(
    "/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/HOS UAT"
)
CLIP_LOCK = {
    "01_old_theatre": "01_old_theatre_v01b.mp4",
    "02_spray_scrub": "02_spray_scrub_v01c.mp4",
    "03_protocol": "03_protocol_v01b.mp4",
    "04_explorer_scrubs": "04_explorer_scrubs_v02d.mp4",
    "05_theatre_wins": "05_theatre_wins_v02.mp4",
    "06_soap_hands": "06_soap_hands_v02d.mp4",
    "07_a_map": "07_a_map_v01.mp4",
    "08_last_light": "08_last_light_v01d.mp4",
}
# VO 45.680s. 8 plates must all land before cut.
CLIP_USE = 6.20
XFADE = 0.40
FPS = 24
FADE = 14 / 24
HOLD = 4.20
CHAPTER = ("chapter", "A surgical theatre", 1.50, 5.00, "left")
# LISTER before chapter so cards stay one at a time. Rest snap to VO.
LABELS = [
    ("lister", "LISTER", 0.20, "right"),
    ("spray", "SPRAY", 8.13, "right"),
    ("protocol", "PROTOCOL", 20.84, "right"),
    ("soap", "SOAP", 31.06, "right"),
    ("a_map", "A MAP", 34.70, "right"),
    ("invisible", "INVISIBLE", 44.35, "right"),
]
SOAP_LIFT = 31.056


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


def make_theatre_bed() -> None:
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
    cloth = FX_DIR / "cloth_v01.wav"
    water = FX_DIR / "water_v01.wav"
    spray = FX_DIR / "spray_v01.wav"
    wood = FX_DIR / "wood_v01.wav"
    ff(
        "-f", "lavfi", "-i", "anoisesrc=color=brown:duration=0.70:sample_rate=48000",
        "-af",
        "highpass=f=260,lowpass=f=2100,tremolo=f=13:d=0.5,volume=0.38,"
        "afade=t=in:d=0.04,afade=t=out:st=0.38:d=0.32",
        "-ac", "2", str(cloth),
    )
    ff(
        "-f", "lavfi", "-i", "anoisesrc=color=white:duration=1.20:sample_rate=48000",
        "-af",
        "highpass=f=400,lowpass=f=2200,tremolo=f=18:d=0.45,volume=0.22,"
        "afade=t=in:d=0.08,afade=t=out:st=0.80:d=0.40",
        "-ac", "2", str(water),
    )
    ff(
        "-f", "lavfi", "-i", "anoisesrc=color=pink:duration=2.40:sample_rate=48000",
        "-af",
        "highpass=f=500,lowpass=f=2800,tremolo=f=22:d=0.55,volume=0.16,"
        "afade=t=in:d=0.12,afade=t=out:st=1.80:d=0.50",
        "-ac", "2", str(spray),
    )
    ff(
        "-f", "lavfi", "-i", "anoisesrc=color=brown:duration=0.45:sample_rate=48000",
        "-af",
        "highpass=f=80,lowpass=f=700,tremolo=f=7:d=0.35,volume=0.28,"
        "afade=t=in:d=0.02,afade=t=out:st=0.28:d=0.16",
        "-ac", "2", str(wood),
    )
    return {"cloth": cloth, "water": water, "spray": spray, "wood": wood}


def main() -> None:
    if not LOCK04.exists() or sha256(LOCK04) != LOCK04_SHA:
        raise SystemExit("STOP: Part 04 v23 missing or hash mismatch — do not remint")
    plates = json.loads(PLATES_JSON.read_text())["plates"]
    clips = []
    for p in plates:
        name = CLIP_LOCK.get(p["id"])
        if not name:
            raise SystemExit(f"STOP: no v02 lock for {p['id']}")
        cand = RAW / name
        clips.append(cand)
        print(f"  {p['id']:28s} {cand.name}", flush=True)
    missing = [str(c) for c in clips if not veo.already_done(c, min_bytes=400_000)]
    if missing:
        raise SystemExit("missing Fast plates: " + ", ".join(missing))
    if not VO.exists():
        raise SystemExit(f"missing VO {VO}")
    vo_dur = probe_dur(VO)
    n = len(clips)
    uses = [CLIP_USE] * n
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
        if slug == "lister":
            t_out = min(1.40, CHAPTER[2] - 0.10)
        else:
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

    make_theatre_bed()
    fx = synth_fx()
    vo_i = len(pngs) + 1
    bed_i = vo_i + 1
    spray_i = bed_i + 1
    water_i = spray_i + 1
    cloth_i = water_i + 1
    wood_i = cloth_i + 1
    overlay_in += [
        "-i", str(VO),
        "-i", str(BED),
        "-i", str(fx["spray"]),
        "-i", str(fx["water"]),
        "-i", str(fx["cloth"]),
        "-i", str(fx["wood"]),
    ]
    spray_at = phrase_time(align, "spray")
    soap_at = phrase_time(align, "soap meets")
    spray_ms = int(round(spray_at * 1000))
    soap_ms = int(round(soap_at * 1000))
    lift = SOAP_LIFT
    ov_parts.append(
        f"[{vo_i}:a]aformat=sample_fmts=fltp:channel_layouts=stereo,"
        f"apad=whole_dur={cut:.6f},atrim=0:{cut:.6f}[vo];"
        f"[{bed_i}:a]atrim=0:{cut:.6f},asetpts=PTS-STARTPTS,"
        f"volume='if(lt(t\\,{lift:.3f})\\,0.12\\,0.20)'[bed];"
        f"[{spray_i}:a]adelay={spray_ms}|{spray_ms},volume=0.10,atrim=0:{cut:.6f}[spray];"
        f"[{water_i}:a]adelay={soap_ms}|{soap_ms},volume=0.09,atrim=0:{cut:.6f}[water];"
        f"[{cloth_i}:a]asplit=2[k0][k1];"
        f"[k0]adelay=9000|9000,volume=0.07[cloth1];"
        f"[k1]adelay={soap_ms}|{soap_ms},volume=0.07[cloth2];"
        f"[{wood_i}:a]asplit=2[w0][w1];"
        f"[w0]adelay=18000|18000,volume=0.06[wood1];"
        f"[w1]adelay=40000|40000,volume=0.06[wood2];"
        f"[vo][bed][spray][water][cloth1][cloth2][wood1][wood2]"
        f"amix=inputs=8:duration=first:dropout_transition=0:normalize=0,"
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
