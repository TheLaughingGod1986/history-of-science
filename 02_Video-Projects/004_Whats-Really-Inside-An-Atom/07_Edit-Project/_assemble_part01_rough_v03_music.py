#!/usr/bin/env python3
"""Part 01 rough v03 — TEMP music bed under locked v04 VO + v02 picture.

No Flow. Picture from hos_004_part01_rough_v02.mp4 (silent plates).
VO from hos_004_part01_vo_v04.wav at native level (unchanged).
TEMP bed: hos004-part01-temp_score_bed_v01.mp3 at ~-20 dB vs VO,
sidechain-ducked under speech, fade-out at part end.
Final bed is made at full-film assembly — this mix is UAT only.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EDIT = Path(__file__).resolve().parent
PIC = ROOT / "09_Final-Export" / "hos_004_part01_rough_v02.mp4"
VO = ROOT / "02_Voiceover" / "05_Master" / "hos_004_part01_vo_v04.wav"
MUSIC = ROOT / "05_Music" / "hos004-part01-temp_score_bed_v01.mp3"
OUT_LOCAL = ROOT / "09_Final-Export" / "hos_004_part01_rough_v03.mp4"
ICLOUD = Path.home() / (
    "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT/"
    "004_Whats-Really-Inside-An-Atom/09_Final-Export/hos_004_part01_rough_v03.mp4"
)
META = EDIT / "part01_rough_v03_land_meta.json"

# Bed ~-20 dB relative to VO (volume=0.1), then sidechain duck under speech.
BED_REL_DB = -20.0
BED_VOLUME = 10 ** (BED_REL_DB / 20.0)  # 0.1
FADE_OUT_S = 2.5
SIDECHAIN = "threshold=0.018:ratio=8:attack=20:release=500:level_sc=1"


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def probe_dur(path: Path) -> float:
    out = subprocess.check_output(
        [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=nw=1:nk=1",
            str(path),
        ],
        text=True,
    ).strip()
    return float(out)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    for p in (PIC, VO, MUSIC):
        if not p.exists():
            raise SystemExit(f"missing: {p}")

    vo_dur = probe_dur(VO)
    pic_dur = probe_dur(PIC)
    music_dur = probe_dur(MUSIC)
    if abs(pic_dur - vo_dur) > 0.05:
        raise SystemExit(f"v02 pic {pic_dur:.3f}s vs VO {vo_dur:.3f}s mismatch")
    if music_dur < vo_dur:
        raise SystemExit(f"music {music_dur:.3f}s shorter than VO {vo_dur:.3f}s")

    master_dur = vo_dur
    fade_start = max(0.0, master_dur - FADE_OUT_S)

    # 0=picture (video only) 1=VO 2=music
    # VO path untouched (no volume filter). Music: -20 dB, fade out, sidechain duck.
    graph = (
        f"[0:v]trim=0:{master_dur:.6f},setpts=PTS-STARTPTS,"
        "scale=1920:1080:force_original_aspect_ratio=decrease,"
        "pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps=30,format=yuv420p[v];"
        f"[1:a]atrim=0:{master_dur:.6f},asetpts=PTS-STARTPTS,"
        "aformat=sample_rates=48000:channel_layouts=stereo,asplit=2[vo][vo_sc];"
        f"[2:a]atrim=0:{master_dur:.6f},asetpts=PTS-STARTPTS,"
        f"volume={BED_VOLUME:.6f},"
        f"afade=t=out:st={fade_start:.6f}:d={FADE_OUT_S:.6f},"
        "aformat=sample_rates=48000:channel_layouts=stereo[music];"
        f"[music][vo_sc]sidechaincompress={SIDECHAIN}[ducked];"
        "[vo][ducked]amix=inputs=2:weights=1 1:normalize=0,"
        "alimiter=limit=0.8912509:level=false[a]"  # ~-1 dBTP
    )

    OUT_LOCAL.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="hos004_p01_v03_") as td:
        tmp = Path(td) / "rough_v03.mp4"
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(PIC),
            "-i", str(VO),
            "-i", str(MUSIC),
            "-filter_complex", graph,
            "-map", "[v]", "-map", "[a]",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
            "-pix_fmt", "yuv420p",
            "-r", "30",
            "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "192k",
            "-t", f"{master_dur:.6f}",
            "-movflags", "+faststart",
            str(tmp),
        ])
        shutil.copy2(tmp, OUT_LOCAL)

    ICLOUD.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(OUT_LOCAL, ICLOUD)

    # Also export VO-only and ducked-bed-only stems for level measurement
    stem_dir = EDIT / "_part01_rough_v03_work"
    stem_dir.mkdir(parents=True, exist_ok=True)
    vo_stem = stem_dir / "vo_only.wav"
    bed_stem = stem_dir / "bed_ducked_only.wav"
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(VO),
        "-af", f"atrim=0:{master_dur:.6f},asetpts=PTS-STARTPTS,"
               "aformat=sample_rates=48000:channel_layouts=stereo",
        str(vo_stem),
    ])
    bed_graph = (
        f"[0:a]atrim=0:{master_dur:.6f},asetpts=PTS-STARTPTS,"
        "aformat=sample_rates=48000:channel_layouts=stereo[vo_sc];"
        f"[1:a]atrim=0:{master_dur:.6f},asetpts=PTS-STARTPTS,"
        f"volume={BED_VOLUME:.6f},"
        f"afade=t=out:st={fade_start:.6f}:d={FADE_OUT_S:.6f},"
        "aformat=sample_rates=48000:channel_layouts=stereo[music];"
        f"[music][vo_sc]sidechaincompress={SIDECHAIN}[ducked]"
    )
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(VO), "-i", str(MUSIC),
        "-filter_complex", bed_graph,
        "-map", "[ducked]",
        str(bed_stem),
    ])

    digest = sha256(OUT_LOCAL)
    meta = {
        "temp": True,
        "note": "TEMP UAT bed only — final bed at full-film assembly",
        "out": str(OUT_LOCAL),
        "icloud": str(ICLOUD),
        "sha256": digest,
        "icloud_sha256": sha256(ICLOUD),
        "duration_s": probe_dur(OUT_LOCAL),
        "fps": 30,
        "size": "1920x1080",
        "picture_source": str(PIC),
        "vo": str(VO),
        "vo_duration_s": vo_dur,
        "vo_level": "unchanged (no volume filter on VO)",
        "music": {
            "path": str(MUSIC),
            "sha256": sha256(MUSIC),
            "generator": "04_Audio/tools/generate_music_bed.py --generate (ElevenLabs music_v2)",
            "prompt": (
                "warm curious documentary underscore, soft strings, light piano, "
                "gentle wonder, no vocals, leaves room for voice"
            ),
            "length_s": music_dur,
            "length_ms_requested": 75000,
            "bed_relative_db_vs_vo": BED_REL_DB,
            "bed_volume_linear": BED_VOLUME,
            "sidechain": SIDECHAIN,
            "fade_out_s": FADE_OUT_S,
            "fade_out_start_s": fade_start,
            "plates_audio": "silent (no Veo audio)",
        },
        "kept_v01_v02": True,
    }
    META.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(f"SAVED {OUT_LOCAL}")
    print(f"ICLOUD {ICLOUD}")
    print(f"sha256 {digest}")
    print(f"duration {meta['duration_s']:.3f}s")
    print(f"META {META}")


if __name__ == "__main__":
    main()
