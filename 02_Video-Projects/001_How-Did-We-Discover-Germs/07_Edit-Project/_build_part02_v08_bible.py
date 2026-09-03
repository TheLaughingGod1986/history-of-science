#!/usr/bin/env python3
"""Part 02 v08 — bible stack on locked v07 picture.

Titles + Part 01 death-ward bed + sparse period-lab FX.
No remint. No walla. No metal. No Part 03.
"""
from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
SRC = PROJ / "09_Final-Export/hos_001_part02_rough_v07.mp4"
SRC_SHA = "914406d09b0da92a97432af9f32b88917b837b4e258173ee3f31cd9a1bfb9970"
OUT = PROJ / "09_Final-Export/hos_001_part02_rough_v08.mp4"
SWIFT = Path(__file__).resolve().parent / "_render_part01_side_label.swift"
LABEL_DIR = PROJ / "06_Sound-Effects/v08_part02_labels"
FX_DIR = PROJ / "06_Sound-Effects/v08_part02_fx"
MUSIC = PROJ / "05_Music"
BED_RAW = MUSIC / "hos_001_part01_ominous_ward_v12.wav"
BED = MUSIC / "hos_001_part02_ominous_ward_v08_norm.wav"
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


def ff(*args: str) -> None:
    subprocess.run(["ffmpeg", "-y", *args], check=True, capture_output=True)


def synth_fx() -> dict[str, Path]:
    FX_DIR.mkdir(parents=True, exist_ok=True)
    glass = FX_DIR / "glass_slide_v08.wav"
    cloth = FX_DIR / "cloth_wipe_v08.wav"
    wood = FX_DIR / "wood_bench_v08.wav"
    bead = FX_DIR / "water_bead_v08.wav"
    # Thin slide tap — not a tray clink, not a flask pour.
    ff(
        "-f", "lavfi",
        "-i",
        "aevalsrc=0.38*sin(2*PI*1680*t)*exp(-18*t)+0.16*sin(2*PI*2520*t)*exp(-24*t)"
        ":d=0.32:s=48000",
        "-af", "highpass=f=900,lowpass=f=3800,volume=0.32",
        "-ac", "2", str(glass),
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
        "aevalsrc=0.60*sin(2*PI*88*t)*exp(-12*t)+0.20*sin(2*PI*140*t)*exp(-16*t)"
        ":d=0.38:s=48000",
        "-af", "lowpass=f=380,volume=0.48",
        "-ac", "2", str(wood),
    )
    # Soft liquid bead, not a splash gag.
    ff(
        "-f", "lavfi",
        "-i",
        "aevalsrc=0.28*sin(2*PI*620*t)*exp(-14*t)+0.16*sin(2*PI*380*t)*exp(-10*t)"
        ":d=0.42:s=48000",
        "-f", "lavfi", "-i", "anoisesrc=color=brown:duration=0.22:sample_rate=48000",
        "-filter_complex",
        "[1]highpass=f=400,lowpass=f=2400,volume=0.22,adelay=20|20[n];"
        "[0][n]amix=inputs=2:duration=first:normalize=0,"
        "lowpass=f=2800,afade=t=out:st=0.22:d=0.20,volume=0.40",
        "-ac", "2", str(bead),
    )
    return {"glass": glass, "cloth": cloth, "wood": wood, "bead": bead}


def main() -> None:
    if sha256(SRC) != SRC_SHA:
        raise SystemExit("v07 sha mismatch — abort")
    if not BED_RAW.exists():
        raise SystemExit(f"missing bed {BED_RAW}")
    dur = probe_dur(SRC)
    LABEL_DIR.mkdir(parents=True, exist_ok=True)
    bin_path = Path("/tmp/render_part01_side_label")
    subprocess.run(["swiftc", "-O", "-o", str(bin_path), str(SWIFT)], check=True)

    pngs: list[tuple[Path, float, float]] = []
    for slug, text, t_in, t_out, side in CARDS:
        t_out = min(t_out, dur - 0.02)
        if t_out <= t_in:
            raise SystemExit(f"bad window {text} {t_in}-{t_out}")
        png = LABEL_DIR / f"{slug}.png"
        subprocess.run([str(bin_path), text, str(png), side], check=True)
        pngs.append((png, t_in, t_out))
        print(f"CARD {text} {t_in:.2f}-{t_out:.2f} {side}", flush=True)

    fx = synth_fx()
    # Same loudnorm as Part 01 v14 → v21 bed, then under-VO 0.14.
    ff(
        "-i", str(BED_RAW),
        "-af", "loudnorm=I=-21:LRA=9:TP=-3,afade=t=in:d=1.5",
        "-ar", "48000", "-ac", "2", str(BED),
    )
    vo = FX_DIR / "_vo_from_v07.wav"
    ff("-i", str(SRC), "-t", f"{dur:.6f}", "-vn", "-ac", "2", "-ar", "48000", str(vo))

    inputs: list[str] = ["-i", str(SRC)]
    parts: list[str] = []
    last = "0:v"
    for i, (png, t_in, t_out) in enumerate(pngs):
        hold = t_out - t_in
        fade = min(FADE, hold / 3)
        idx = i + 1
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
    n_lab = len(pngs)
    vo_i = n_lab + 1
    bed_i = n_lab + 2
    wood_i = n_lab + 3
    glass_i = n_lab + 4
    cloth_i = n_lab + 5
    bead_i = n_lab + 6
    inputs += [
        "-i", str(vo),
        "-i", str(BED),
        "-i", str(fx["wood"]),
        "-i", str(fx["glass"]),
        "-i", str(fx["cloth"]),
        "-i", str(fx["bead"]),
    ]
    # Sparse, on picture. No walla. No metal. Flask only where flasks are on screen.
    parts.append(f"[{last}]format=yuv420p,setsar=1[v]")
    parts.append(
        f"[{vo_i}:a]aformat=sample_fmts=fltp:channel_layouts=stereo[vo];"
        f"[{bed_i}:a]atrim=0:{dur:.6f},asetpts=PTS-STARTPTS,volume=0.14[bed];"
        f"[{wood_i}:a]asplit=3[w0][w1][w2];"
        f"[w0]adelay=1150|1150,volume=0.08[wood_open];"
        f"[w1]adelay=43500|43500,volume=0.08[wood_lab];"
        f"[w2]adelay=74980|74980,volume=0.07[wood_end];"
        f"[{glass_i}:a]asplit=3[g0][g1][g2];"
        f"[g0]adelay=6200|6200,volume=0.07[glass_pond];"
        f"[g1]adelay=44200|44200,volume=0.06[glass_flask];"
        f"[g2]adelay=53200|53200,volume=0.07[glass_drop];"
        f"[{cloth_i}:a]asplit=2[c0][c1];"
        f"[c0]adelay=45000|45000,volume=0.09[cloth_lab];"
        f"[c1]adelay=75150|75150,volume=0.08[cloth_end];"
        f"[{bead_i}:a]asplit=2[b0][b1];"
        f"[b0]adelay=7500|7500,volume=0.08[bead_pond];"
        f"[b1]adelay=53800|53800,volume=0.08[bead_drop];"
        f"[vo][bed][wood_open][wood_lab][wood_end]"
        f"[glass_pond][glass_flask][glass_drop]"
        f"[cloth_lab][cloth_end][bead_pond][bead_drop]"
        f"amix=inputs=12:duration=first:dropout_transition=0:normalize=0,"
        f"afade=t=out:st={dur - 0.012:.6f}:d=0.012[a]"
    )
    fc = ";".join(parts)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg", "-y", *inputs,
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


if __name__ == "__main__":
    main()
