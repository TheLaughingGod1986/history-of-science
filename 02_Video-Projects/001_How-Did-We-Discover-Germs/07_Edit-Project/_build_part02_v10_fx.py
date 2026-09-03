#!/usr/bin/env python3
"""Part 02 v10 — restore v08 lab FX. Keep v09 picture/titles/ducked bed/VO.

v09 FAIL: FX faded into silence. Do not remint. Do not invent new hits.
"""
from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
PIC = PROJ / "09_Final-Export/hos_001_part02_rough_v07.mp4"
PIC_SHA = "914406d09b0da92a97432af9f32b88917b837b4e258173ee3f31cd9a1bfb9970"
V08 = PROJ / "09_Final-Export/hos_001_part02_rough_v08.mp4"
V08_SHA = "5e04283a79915b0f2a628038d053deb6755d0b96a45e825c9503e2ebf47c50dd"
OUT = PROJ / "09_Final-Export/hos_001_part02_rough_v10.mp4"
SWIFT = Path(__file__).resolve().parent / "_render_part01_side_label.swift"
LABEL_DIR = PROJ / "06_Sound-Effects/v08_part02_labels"
FX08 = PROJ / "06_Sound-Effects/v08_part02_fx"
VO = FX08 / "_vo_from_v07.wav"
WOOD = FX08 / "wood_bench_v08.wav"
GLASS = FX08 / "glass_slide_v08.wav"
CLOTH = FX08 / "cloth_wipe_v08.wav"
BEAD = FX08 / "water_bead_v08.wav"
BED = PROJ / "05_Music/hos_001_part02_ominous_ward_v09_norm.wav"
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
    if sha256(V08) != V08_SHA:
        raise SystemExit("v08 sha mismatch — abort")
    needed = [VO, WOOD, GLASS, CLOTH, BEAD, BED]
    missing = [str(p) for p in needed if not p.exists()]
    if missing:
        raise SystemExit("missing stems " + ", ".join(missing))
    dur = probe_dur(PIC)
    bin_path = Path("/tmp/render_part01_side_label")
    subprocess.run(["swiftc", "-O", "-o", str(bin_path), str(SWIFT)], check=True)

    inputs: list[str] = ["-i", str(PIC)]
    parts: list[str] = []
    last = "0:v"
    for i, (slug, text, t_in, t_out, side) in enumerate(CARDS):
        t_out = min(t_out, dur - 0.02)
        hold = t_out - t_in
        fade = min(FADE, hold / 3)
        png = LABEL_DIR / f"{slug}.png"
        subprocess.run([str(bin_path), text, str(png), side], check=True)
        print(f"CARD {text} {t_in:.2f}-{t_out:.2f} {side}", flush=True)
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

    n_lab = len(CARDS)
    vo_i, bed_i = n_lab + 1, n_lab + 2
    wood_i, glass_i, cloth_i, bead_i = n_lab + 3, n_lab + 4, n_lab + 5, n_lab + 6
    inputs += [
        "-i", str(VO),
        "-i", str(BED),
        "-i", str(WOOD),
        "-i", str(GLASS),
        "-i", str(CLOTH),
        "-i", str(BEAD),
    ]
    # v09 bed duck (PASS). Exact v08 stems + delay map. No new hits.
    # Mix ~2.2× v08 so hits read on a phone under the quieter ducked bed.
    # 12ms fade-in so joins do not scratch. Picture joins untouched.
    parts.append(f"[{last}]format=yuv420p,setsar=1[v]")
    parts.append(
        f"[{vo_i}:a]aformat=sample_fmts=fltp:channel_layouts=stereo,asplit=2[vo][sc];"
        f"[{bed_i}:a]atrim=0:{dur:.6f},asetpts=PTS-STARTPTS,volume=0.09[bed0];"
        f"[bed0][sc]sidechaincompress=threshold=0.016:ratio=7:attack=18:"
        f"release=380:makeup=1.05[bed];"
        f"[{wood_i}:a]asplit=3[w0][w1][w2];"
        f"[w0]adelay=1150|1150,volume=0.18,afade=t=in:d=0.012[wood_open];"
        f"[w1]adelay=43500|43500,volume=0.18,afade=t=in:d=0.012[wood_lab];"
        f"[w2]adelay=74980|74980,volume=0.16,afade=t=in:d=0.012[wood_end];"
        f"[{glass_i}:a]asplit=3[g0][g1][g2];"
        f"[g0]adelay=6200|6200,volume=0.16,afade=t=in:d=0.012[glass_pond];"
        f"[g1]adelay=44200|44200,volume=0.14,afade=t=in:d=0.012[glass_exp];"
        f"[g2]adelay=53200|53200,volume=0.16,afade=t=in:d=0.012[glass_drop];"
        f"[{cloth_i}:a]asplit=2[c0][c1];"
        f"[c0]adelay=45000|45000,volume=0.20,afade=t=in:d=0.012[cloth_lab];"
        f"[c1]adelay=75150|75150,volume=0.18,afade=t=in:d=0.012[cloth_end];"
        f"[{bead_i}:a]asplit=2[b0][b1];"
        f"[b0]adelay=7500|7500,volume=0.18,afade=t=in:d=0.012[bead_pond];"
        f"[b1]adelay=53800|53800,volume=0.18,afade=t=in:d=0.012[bead_drop];"
        f"[vo][bed][wood_open][wood_lab][wood_end]"
        f"[glass_pond][glass_exp][glass_drop]"
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


if __name__ == "__main__":
    main()
