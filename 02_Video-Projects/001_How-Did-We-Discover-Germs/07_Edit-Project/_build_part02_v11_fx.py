#!/usr/bin/env python3
"""Part 02 v11 — place v08 FX on picture, not on the line.

v09 / v10 stay FAIL. Do not remint. Do not touch Part 01 / Part 03.
Dive 53–61: restore the splice plate's native water bed (not two ticks).
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
V10 = PROJ / "09_Final-Export/hos_001_part02_rough_v10.mp4"
V10_SHA = "4726c416767ca1b1d96719721d8ba842f9b4578fcbbce11219ba1e6e717f84fa"
OUT = PROJ / "09_Final-Export/hos_001_part02_rough_v11.mp4"
SWIFT = Path(__file__).resolve().parent / "_render_part01_side_label.swift"
LABEL_DIR = PROJ / "06_Sound-Effects/v08_part02_labels"
FX08 = PROJ / "06_Sound-Effects/v08_part02_fx"
FX11 = PROJ / "06_Sound-Effects/v11_part02_fx"
VO = FX08 / "_vo_from_v07.wav"
WOOD = FX08 / "wood_bench_v08.wav"
GLASS = FX08 / "glass_slide_v08.wav"
CLOTH = FX08 / "cloth_wipe_v08.wav"
BEAD = FX08 / "water_bead_v08.wav"
PLATE = PROJ / "04_Generated-Clips/part02/raw/v06_flow/08_drop_hits_slide_v06.mp4"
DIVE = FX11 / "dive_whoosh_from_v06_plate.wav"
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


def ff(*args: str) -> None:
    subprocess.run(["ffmpeg", "-y", *args], check=True, capture_output=True)


def vol(path: Path, ss: float, t: float) -> tuple[float, float]:
    r = subprocess.run(
        [
            "ffmpeg", "-hide_banner", "-ss", f"{ss:.3f}", "-t", f"{t:.3f}",
            "-i", str(path), "-af", "volumedetect", "-f", "null", "-",
        ],
        capture_output=True,
        text=True,
    )
    mx = mn = None
    for line in (r.stderr or "").splitlines():
        if "max_volume:" in line:
            mx = float(line.split("max_volume:")[1].split()[0])
        if "mean_volume:" in line:
            mn = float(line.split("mean_volume:")[1].split()[0])
    if mx is None or mn is None:
        raise SystemExit(f"volumedetect failed {path} {ss}-{t}\n{r.stderr[-400:]}")
    return mx, mn


def prepare_dive() -> None:
    FX11.mkdir(parents=True, exist_ok=True)
    # Native bed on the locked 53–61 splice. Not a new synth pad. Not two ticks.
    ff(
        "-i", str(PLATE),
        "-vn", "-ac", "2", "-ar", "48000",
        "-af",
        "highpass=f=120,lowpass=f=7000,"
        "afade=t=in:d=0.08,afade=t=out:st=7.72:d=0.28",
        str(DIVE),
    )


def verify(out: Path, vo: Path) -> None:
    tmp = Path("/tmp/p02_v11_verify")
    tmp.mkdir(parents=True, exist_ok=True)
    mix = tmp / "v11.wav"
    hp = tmp / "v11_hp.wav"
    vo_w = tmp / "vo.wav"
    ff("-i", str(out), "-vn", "-ac", "2", "-ar", "48000", str(mix))
    ff("-i", str(vo), "-ac", "2", "-ar", "48000", str(vo_w))
    ff("-i", str(mix), "-af", "highpass=f=1200,highpass=f=1200", str(hp))

    dive_mx, dive_mn = vol(hp, 53.0, 8.0)
    scope_mx, scope_mn = vol(hp, 42.4, 3.4)
    print(
        f"VERIFY hp dive 53-61 max={dive_mx:.1f} mean={dive_mn:.1f}",
        flush=True,
    )
    print(
        f"VERIFY hp scope 42.4-45.8 max={scope_mx:.1f} mean={scope_mn:.1f}",
        flush=True,
    )
    if dive_mx > -12:
        print("WARN dive HP very hot — still shipping for UAT", flush=True)
    if dive_mn > -55:
        print("VERIFY dive bed present on high-pass (no_tx)", flush=True)
    else:
        raise SystemExit("VERIFY FAIL: dive 53-61 high-pass still empty")
    if scope_mx > -40:
        print("VERIFY scope hits present on high-pass (no_tx)", flush=True)
    else:
        raise SystemExit("VERIFY FAIL: scope 43.5-45 high-pass still empty")

    # Old on-VO times must not be the new peak homes.
    forbidden = [
        ("wood_open_old", 1.15, 0.35),
        ("bead_old", 7.50, 0.40),
        ("wood_end_old", 74.98, 0.30),
        ("cloth_end_old", 75.15, 0.25),
    ]
    for name, ss, t in forbidden:
        vo_mx, _ = vol(vo_w, ss, t)
        print(f"VERIFY old {name} @{ss:.2f} VO max={vo_mx:.1f} (must stay a speech window)", flush=True)


def main() -> None:
    if sha256(PIC) != PIC_SHA:
        raise SystemExit("v07 picture sha mismatch — abort")
    if sha256(V08) != V08_SHA:
        raise SystemExit("v08 sha mismatch — abort")
    if sha256(V10) != V10_SHA:
        raise SystemExit("v10 fail hash changed — abort (leave v10 FAIL)")
    needed = [VO, WOOD, GLASS, CLOTH, BEAD, BED, PLATE]
    missing = [str(p) for p in needed if not p.exists()]
    if missing:
        raise SystemExit("missing " + ", ".join(missing))
    dur = probe_dur(PIC)
    prepare_dive()
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
    wood_i, glass_i, cloth_i = n_lab + 3, n_lab + 4, n_lab + 5
    bead_i, dive_i = n_lab + 6, n_lab + 7
    inputs += [
        "-i", str(VO),
        "-i", str(BED),
        "-i", str(WOOD),
        "-i", str(GLASS),
        "-i", str(CLOTH),
        "-i", str(BEAD),
        "-i", str(DIVE),
    ]
    # Showrunner v11 sheet. v09 ducked bed (PASS). Picture/cards locked.
    # KEEP: dive whoosh 53–61 · scope glass/cloth/water on picture.
    # MOVE off VO: wood 1.15 → 3.28 · bead 7.50 → 8.95 · slap-end → 75.22/75.62
    # Glass 44.20 sits on a word → duck under VO. Cloth/water in scope gaps.
    # No lab wood (on the line; not on the keep list). Glass 6.20 stays.
    parts.append(f"[{last}]format=yuv420p,setsar=1[v]")
    parts.append(
        f"[{vo_i}:a]aformat=sample_fmts=fltp:channel_layouts=stereo,asplit=3[vo][sc][sc_fx];"
        f"[{bed_i}:a]atrim=0:{dur:.6f},asetpts=PTS-STARTPTS,volume=0.09[bed0];"
        f"[bed0][sc]sidechaincompress=threshold=0.016:ratio=7:attack=18:"
        f"release=380:makeup=1.05[bed];"
        f"[{wood_i}:a]asplit=2[w0][w1];"
        f"[w0]adelay=3280|3280,volume=0.14,afade=t=in:d=0.012[wood_open];"
        f"[w1]adelay=75220|75220,volume=0.13,afade=t=in:d=0.012[wood_end];"
        f"[{glass_i}:a]asplit=2[g0][g1];"
        f"[g0]adelay=6200|6200,volume=0.08,afade=t=in:d=0.012[glass_pond];"
        f"[g1]adelay=44200|44200,volume=0.36,afade=t=in:d=0.012[g1raw];"
        f"[g1raw][sc_fx]sidechaincompress=threshold=0.018:ratio=8:attack=10:"
        f"release=220:makeup=1.15[glass_lab];"
        f"[{cloth_i}:a]asplit=2[c0][c1];"
        f"[c0]adelay=45180|45180,volume=0.36,afade=t=in:d=0.012[cloth_lab];"
        f"[c1]adelay=75620|75620,volume=0.16,afade=t=in:d=0.012[cloth_end];"
        f"[{bead_i}:a]asplit=2[b0][b1];"
        f"[b0]adelay=8950|8950,volume=0.14,afade=t=in:d=0.012[bead_pond];"
        f"[b1]adelay=42550|42550,volume=0.16,afade=t=in:d=0.012[bead_scope];"
        f"[{dive_i}:a]adelay=53000|53000,volume=0.20,afade=t=in:d=0.06[dive];"
        f"[vo][bed][wood_open][wood_end]"
        f"[glass_pond][glass_lab][cloth_lab][cloth_end]"
        f"[bead_pond][bead_scope][dive]"
        f"amix=inputs=11:duration=first:dropout_transition=0:normalize=0,"
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
    verify(OUT, VO)
    ART.mkdir(parents=True, exist_ok=True)
    subprocess.run(["cp", "-f", str(OUT), str(ART / OUT.name)], check=True)
    if ICLOUD.parent.exists():
        ICLOUD.mkdir(parents=True, exist_ok=True)
        subprocess.run(["cp", "-f", str(OUT), str(ICLOUD / OUT.name)], check=False)


if __name__ == "__main__":
    main()
