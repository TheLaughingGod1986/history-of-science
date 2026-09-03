#!/usr/bin/env python3
"""Part 02 v12 — restore the actual v08 53–61 residual (the plunge).

v09 / v10 / v11 stay FAIL. No remint. No Part 01 / Part 03.
Whoosh = v08[53–61] minus VO. Not plate. Not ticks. Not a synth pad.
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
V11 = PROJ / "09_Final-Export/hos_001_part02_rough_v11.mp4"
V11_SHA = "be4368169ba308d02f5c2ef1276a5b68ee28e1c167b69226eb31ce32f7321cbb"
OUT = PROJ / "09_Final-Export/hos_001_part02_rough_v12.mp4"
SWIFT = Path(__file__).resolve().parent / "_render_part01_side_label.swift"
LABEL_DIR = PROJ / "06_Sound-Effects/v08_part02_labels"
FX08 = PROJ / "06_Sound-Effects/v08_part02_fx"
FX12 = PROJ / "06_Sound-Effects/v12_part02_fx"
VO = FX08 / "_vo_from_v07.wav"
WOOD = FX08 / "wood_bench_v08.wav"
GLASS = FX08 / "glass_slide_v08.wav"
CLOTH = FX08 / "cloth_wipe_v08.wav"
BEAD = FX08 / "water_bead_v08.wav"
DIVE = FX12 / "v08_dive_residual_53_61.wav"
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


def decode_wav(src: Path, dest: Path) -> None:
    ff("-i", str(src), "-vn", "-ac", "2", "-ar", "48000", str(dest))


def slice_wav(src: Path, dest: Path, ss: float, t: float) -> None:
    # -ss after -i is sample-accurate on wav.
    ff("-i", str(src), "-ss", f"{ss:.6f}", "-t", f"{t:.6f}", str(dest))


def extract_v08_residual() -> None:
    """v08[53–61] minus VO, sample-accurate. That is the plunge UAT heard."""
    FX12.mkdir(parents=True, exist_ok=True)
    full_v08 = FX12 / "_v08_full.wav"
    tmp_v08 = FX12 / "_v08_53_61.wav"
    tmp_vo = FX12 / "_vo_53_61.wav"
    decode_wav(V08, full_v08)
    slice_wav(full_v08, tmp_v08, 53.0, 8.0)
    slice_wav(VO, tmp_vo, 53.0, 8.0)
    ff(
        "-i", str(tmp_v08), "-i", str(tmp_vo),
        "-filter_complex",
        "[1]volume=-1[inv];[0][inv]amix=inputs=2:duration=first:normalize=0,"
        "afade=t=in:d=0.08,afade=t=out:st=7.76:d=0.24",
        str(DIVE),
    )
    mx, mn = vol(DIVE, 0, 8)
    print(f"DIVE_STEM residual max={mx:.1f} mean={mn:.1f}", flush=True)
    if mn > -34 or mx > -20:
        raise SystemExit(
            f"STOP: dive stem is not the v08 residual (max={mx:.1f} mean={mn:.1f}). "
            "VO did not cancel. Not shipping."
        )


def residual_wav(mix: Path, vo: Path, dest: Path, ss: float, t: float) -> None:
    tmp_full = dest.with_name(dest.stem + "_full.wav")
    tmp_m = dest.with_name(dest.stem + "_m.wav")
    tmp_v = dest.with_name(dest.stem + "_v.wav")
    decode_wav(mix, tmp_full)
    slice_wav(tmp_full, tmp_m, ss, t)
    slice_wav(vo, tmp_v, ss, t)
    ff(
        "-i", str(tmp_m), "-i", str(tmp_v),
        "-filter_complex",
        "[1]volume=-1[inv];[0][inv]amix=inputs=2:duration=first:normalize=0",
        str(dest),
    )


def prove_dive(out: Path) -> None:
    tmp = Path("/tmp/p02_v12_prove")
    tmp.mkdir(parents=True, exist_ok=True)
    r08 = tmp / "v08_res.wav"
    r11 = tmp / "v11_res.wav"
    r12 = tmp / "v12_res.wav"
    residual_wav(V08, VO, r08, 53.0, 8.0)
    residual_wav(V11, VO, r11, 53.0, 8.0)
    residual_wav(out, VO, r12, 53.0, 8.0)
    m08, n08 = vol(r08, 0, 8)
    m11, n11 = vol(r11, 0, 8)
    m12, n12 = vol(r12, 0, 8)
    print(f"PROVE no_tx 53-61 v08 max={m08:.1f} mean={n08:.1f}", flush=True)
    print(f"PROVE no_tx 53-61 v11 max={m11:.1f} mean={n11:.1f}", flush=True)
    print(f"PROVE no_tx 53-61 v12 max={m12:.1f} mean={n12:.1f}", flush=True)
    dmax = abs(m12 - m08)
    dmean = abs(n12 - n08)
    print(f"PROVE delta vs v08 max={dmax:.1f} mean={dmean:.1f}", flush=True)
    # v12 must look like v08, not like v11 (v11 mean is ~7 dB quieter).
    if dmean > 3.0 or dmax > 4.0:
        raise SystemExit(
            f"STOP: 53-61 no_tx does not match v08 "
            f"(mean Δ{dmean:.1f} max Δ{dmax:.1f}). Not shipping."
        )
    if abs(n12 - n11) < 2.0 and abs(n08 - n11) > 4.0:
        raise SystemExit("STOP: 53-61 no_tx still looks like v11. Not shipping.")
    print("PROVE PASS: 53-61 no_tx matches v08", flush=True)


def main() -> None:
    if sha256(PIC) != PIC_SHA:
        raise SystemExit("v07 picture sha mismatch — abort")
    if sha256(V08) != V08_SHA:
        raise SystemExit("v08 sha mismatch — abort")
    if sha256(V11) != V11_SHA:
        raise SystemExit("v11 fail hash changed — abort (leave v11 FAIL)")
    needed = [VO, WOOD, GLASS, CLOTH, BEAD, BED]
    missing = [str(p) for p in needed if not p.exists()]
    if missing:
        raise SystemExit("missing " + ", ".join(missing))
    dur = probe_dur(PIC)
    extract_v08_residual()
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
    # v09 ducked bed except 53.08–60.88 (replaced by v08 residual).
    # Keep v11 gap hits. Scope glass/water/cloth slid to 47.75–48.20 (after the line).
    parts.append(f"[{last}]format=yuv420p,setsar=1[v]")
    parts.append(
        f"[{vo_i}:a]aformat=sample_fmts=fltp:channel_layouts=stereo,asplit=2[vo][sc];"
        f"[{bed_i}:a]atrim=0:{dur:.6f},asetpts=PTS-STARTPTS,volume=0.09[bed0];"
        f"[bed0][sc]sidechaincompress=threshold=0.016:ratio=7:attack=18:"
        f"release=380:makeup=1.05[bedd];"
        f"[bedd]volume='if(between(t,53.08,60.88),0,1)':eval=frame[bed];"
        f"[{wood_i}:a]asplit=2[w0][w1];"
        f"[w0]adelay=3280|3280,volume=0.14,afade=t=in:d=0.012[wood_open];"
        f"[w1]adelay=75220|75220,volume=0.13,afade=t=in:d=0.012[wood_end];"
        f"[{glass_i}:a]asplit=2[g0][g1];"
        f"[g0]adelay=6200|6200,volume=0.08,afade=t=in:d=0.012[glass_pond];"
        f"[g1]adelay=47750|47750,volume=0.16,afade=t=in:d=0.012[glass_lab];"
        f"[{cloth_i}:a]asplit=2[c0][c1];"
        f"[c0]adelay=47820|47820,volume=0.20,afade=t=in:d=0.012[cloth_lab];"
        f"[c1]adelay=75620|75620,volume=0.16,afade=t=in:d=0.012[cloth_end];"
        f"[{bead_i}:a]asplit=2[b0][b1];"
        f"[b0]adelay=8950|8950,volume=0.14,afade=t=in:d=0.012[bead_pond];"
        f"[b1]adelay=48150|48150,volume=0.16,afade=t=in:d=0.012[bead_scope];"
        f"[{dive_i}:a]adelay=53000|53000,volume=1.0[dive];"
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
    prove_dive(OUT)
    ART.mkdir(parents=True, exist_ok=True)
    subprocess.run(["cp", "-f", str(OUT), str(ART / OUT.name)], check=True)
    if ICLOUD.parent.exists():
        ICLOUD.mkdir(parents=True, exist_ok=True)
        subprocess.run(["cp", "-f", str(OUT), str(ICLOUD / OUT.name)], check=False)


if __name__ == "__main__":
    main()
