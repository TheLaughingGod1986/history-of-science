#!/usr/bin/env python3
"""Part 01 v12 — mix + one text card on v10 picture. No remint. No join recut."""
from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
PIC = PROJ / "09_Final-Export/hos_001_part01_rough_v10.mp4"
VO_SRC = PROJ / "09_Final-Export/hos_001_part01_rough_v09.mp4"
OUT = PROJ / "09_Final-Export/hos_001_part01_rough_v12.mp4"
MUSIC = PROJ / "05_Music"
SFX = PROJ / "06_Sound-Effects/v12"
MID = MUSIC / "hos_001_part01_ominous_ward_v12.mid"
BED = MUSIC / "hos_001_part01_ominous_ward_v12.wav"
SF2 = MUSIC / "TimGM6mb.sf2"
CARD_SWIFT = Path(__file__).resolve().parent / "_render_living_cloud_card.swift"
CARD = PROJ / "06_Sound-Effects/v12/a_living_cloud_card.png"
# Snap: living-cloud phrase after "Why does order fail" / "because…"; out before fight.
TEXT_IN = 51.15
TEXT_OUT = 54.85
ART = Path(
    "/Users/benjaminoats/Library/Application Support/Cursor/"
    "AgentStores/cursor_agent_stores/bc-eb2a62e0-1899-43b0-9cd2-0b96209c2bd0/"
    "files/artifacts"
)
ICLOUD = Path(
    "/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/HOS UAT"
)
KILL = [
    MUSIC / "hos_001_part01_curious_pad_v10.wav",
    MUSIC / "hos_001_part01_warm_dls_pad_v11.wav",
    MUSIC / "hos_001_part01_warm_dls_pad_v11_norm.wav",
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


def say_aiff(voice: str, rate: int, text: str, dest: Path) -> None:
    subprocess.run(
        ["say", "-v", voice, "-r", str(rate), "-o", str(dest), text],
        check=True,
        capture_output=True,
    )


def main() -> None:
    if not PIC.exists() or not VO_SRC.exists():
        raise SystemExit("missing v10 picture or v09 VO")
    if not MID.exists() or not SF2.exists():
        raise SystemExit("compose MIDI + TimGM6mb.sf2 first")
    SFX.mkdir(parents=True, exist_ok=True)
    for dead in KILL:
        if dead.exists():
            dead.unlink()

    # Original cue → wav (FluidSynth + GM strings/cello/piano)
    subprocess.run(
        [
            "fluidsynth", "-ni", "-l",
            "-r", "48000",
            "-g", "0.7",
            "-F", str(BED),
            str(SF2),
            str(MID),
        ],
        check=True,
        capture_output=True,
    )
    bed_n = MUSIC / "hos_001_part01_ominous_ward_v12_norm.wav"
    ff(
        "-i", str(BED),
        "-af", "loudnorm=I=-21:LRA=9:TP=-3,afade=t=in:d=1.5,afade=t=out:st=73.2:d=2.0",
        "-ar", "48000", "-ac", "2", str(bed_n),
    )

    # Walla: original period mutter, low and distant (not English under the VO).
    w1 = SFX / "_walla_anna.aiff"
    w2 = SFX / "_walla_albert.aiff"
    w3 = SFX / "_walla_amelie.aiff"
    say_aiff("Anna", 95, "Die Betten die Lampen die Runde am Morgen die Tücher", w1)
    say_aiff("Albert", 80, "The basin the cloth the morning round the quiet ward", w2)
    say_aiff("Amélie", 90, "Les draps les lampes le corridor le silence des lits", w3)
    walla = SFX / "walla_ward_v12.wav"
    ff(
        "-stream_loop", "-1", "-i", str(w1),
        "-stream_loop", "-1", "-i", str(w2),
        "-stream_loop", "-1", "-i", str(w3),
        "-filter_complex",
        "[0:a][1:a][2:a]amix=inputs=3:duration=longest:normalize=0,"
        "lowpass=f=920,highpass=f=120,aecho=0.5:0.6:40:0.25,volume=0.55",
        "-t", "80", "-ar", "48000", "-ac", "2", str(walla),
    )

    # Room: distant steps + sheet rustle, always on.
    room = SFX / "room_ward_v12.wav"
    ff(
        "-f", "lavfi", "-i", "anoisesrc=color=brown:duration=80:sample_rate=48000",
        "-f", "lavfi",
        "-i",
        "aevalsrc=0.35*sin(2*PI*78*t)*max(0\\,sin(2*PI*t/1.7))*exp(-8*mod(t\\,1.7))"
        ":d=80:s=48000",
        "-filter_complex",
        "[0]highpass=f=200,lowpass=f=1600,volume=0.07[sheets];"
        "[1]lowpass=f=280,volume=0.12[steps];"
        "[sheets][steps]amix=inputs=2:duration=longest:normalize=0",
        "-ar", "48000", "-ac", "2", str(room),
    )

    cough = SFX / "cough_v12.wav"
    ff(
        "-f", "lavfi",
        "-i",
        "aevalsrc=0.55*sin(2*PI*210*t)*exp(-9*t)+0.35*sin(2*PI*140*t)*exp(-12*t)"
        ":d=0.45:s=48000",
        "-f", "lavfi", "-i", "anoisesrc=color=white:duration=0.18:sample_rate=48000",
        "-filter_complex",
        "[1]highpass=f=800,lowpass=f=4200,volume=0.35,adelay=40|40[n];"
        "[0][n]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.4",
        "-ac", "2", str(cough),
    )

    cloth = SFX / "cloth_v12.wav"
    wood = SFX / "wood_v12.wav"
    glass = SFX / "glass_lamp_v12.wav"
    ff(
        "-f", "lavfi", "-i", "anoisesrc=color=brown:duration=0.65:sample_rate=48000",
        "-af",
        "highpass=f=260,lowpass=f=2100,tremolo=f=13:d=0.5,volume=0.4,"
        "afade=t=in:d=0.04,afade=t=out:st=0.35:d=0.3",
        "-ac", "2", str(cloth),
    )
    ff(
        "-f", "lavfi",
        "-i",
        "aevalsrc=0.65*sin(2*PI*88*t)*exp(-12*t)+0.22*sin(2*PI*140*t)*exp(-16*t)"
        ":d=0.38:s=48000",
        "-af", "lowpass=f=380,volume=0.5",
        "-ac", "2", str(wood),
    )
    ff(
        "-f", "lavfi",
        "-i",
        "aevalsrc=0.4*sin(2*PI*1240*t)*exp(-16*t)+0.18*sin(2*PI*1860*t)*exp(-22*t)"
        ":d=0.35:s=48000",
        "-af", "highpass=f=700,lowpass=f=3200,volume=0.35",
        "-ac", "2", str(glass),
    )

    pic_dur = probe_dur(PIC)
    vo = SFX / "_vo_from_v09.wav"
    ff("-i", str(VO_SRC), "-t", f"{pic_dur:.6f}", "-vn", "-ac", "2", "-ar", "48000", str(vo))

    CARD.parent.mkdir(parents=True, exist_ok=True)
    card_bin = Path("/tmp/render_living_cloud_card")
    subprocess.run(["swiftc", "-O", "-o", str(card_bin), str(CARD_SWIFT)], check=True)
    subprocess.run([str(card_bin), str(CARD)], check=True)

    hold = TEXT_OUT - TEXT_IN
    fade = 8 / 24
    fc = (
        f"[9:v]trim=duration={hold:.3f},setpts=PTS-STARTPTS,format=rgba,"
        f"fade=t=in:st=0:d={fade:.3f}:alpha=1,"
        f"fade=t=out:st={hold - fade:.3f}:d={fade:.3f}:alpha=1,"
        f"setpts=PTS+{TEXT_IN:.3f}/TB[card];"
        f"[0:v][card]overlay=0:0:eof_action=pass,format=yuv420p,setsar=1[v];"
        f"[1:a]aformat=sample_fmts=fltp:channel_layouts=stereo,asplit=2[vo][sc];"
        f"[2:a]atrim=0:{pic_dur:.6f},asetpts=PTS-STARTPTS,volume=0.14[bed];"
        f"[3:a]atrim=0:{pic_dur:.6f},volume=0.09[walla_raw];"
        f"[walla_raw][sc]sidechaincompress=threshold=0.025:ratio=10:attack=12:"
        f"release=220:makeup=1.4[walla];"
        f"[4:a]atrim=0:{pic_dur:.6f},volume=0.06[room];"
        f"[5:a]asplit=3[cg1][cg2][cg3];"
        f"[cg1]adelay=12800|12800,volume=0.10[c1];"
        f"[cg2]adelay=38550|38550,volume=0.09[c2];"
        f"[cg3]adelay=47150|47150,volume=0.09[c3];"
        f"[6:a]adelay=1050|1050,volume=0.10[grab_cloth];"
        f"[7:a]adelay=6350|6350,volume=0.09[grab_wood];"
        f"[8:a]adelay=2100|2100,volume=0.07[grab_glass];"
        f"[vo][bed][walla][room][c1][c2][c3][grab_cloth][grab_wood][grab_glass]"
        f"amix=inputs=10:duration=first:dropout_transition=0:normalize=0[a]"
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg", "-y",
            "-i", str(PIC),
            "-i", str(vo),
            "-i", str(bed_n),
            "-i", str(walla),
            "-i", str(room),
            "-i", str(cough),
            "-i", str(cloth),
            "-i", str(wood),
            "-i", str(glass),
            "-loop", "1", "-t", f"{hold:.3f}", "-i", str(CARD),
            "-filter_complex", fc,
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
    print(f"TEXT {TEXT_IN:.2f}-{TEXT_OUT:.2f}", flush=True)
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
