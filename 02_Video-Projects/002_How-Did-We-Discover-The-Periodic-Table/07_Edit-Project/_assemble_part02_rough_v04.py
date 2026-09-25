#!/usr/bin/env python3
"""Assemble HOS 002 Part 02 rough v04 — jar-free finished Flow stills + cards.

Ben is still watching v03 (flaming jars + unfinished Pillow). This cut:
  - keeps chapter + triad card clips
  - builds ALL scenery from jar-free Flow Image stills (Ken Burns)
  - NEVER uses flaming-jar Flow video or unfinished Pillow desks
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
PLATES_JSON = PROJ / "07_Edit-Project/parts/part-02_plates_v04.json"
RAW = PROJ / "04_Generated-Clips/part02/raw/v01_fast"
STILLS = PROJ / "04_Generated-Clips/part02/refs/v04_flow_stills"
KB_DIR = PROJ / "04_Generated-Clips/part02/raw/v04_kenburns"
VO = PROJ / "02_Voiceover/part02_first_patterns_v01.wav"
BED = PROJ / "05_Music/hos_002_part01_curious_workshop_v02_norm.wav"
OUT = PROJ / "09_Final-Export/hos_002_part02_rough_v04.mp4"
ICLOUD = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT"
CLIP_USE = 8.0
XFADE = 0.4
BED_VOL = 0.42

# Plate id → Flow still filename (jar-free QA'd writing-study stills)
SCENERY_STILLS = {
    "02_lavoisier_list": "02_lavoisier_list_start.jpg",
    "03_not_a_map": "03_not_a_map_start.jpg",
    "05_explorer_triad_break": "05_explorer_triad_break_start.jpg",
    "06_rhymes_run_out": "06_rhymes_run_out_start.jpg",
    "07_newlands_octave": "07_newlands_octave_start.jpg",
    "08_piano_gag_fail": "08_piano_gag_fail_start.jpg",
    "09_almost_right": "09_almost_right_start.jpg",
    "10_ruler_crooked": "10_ruler_crooked_start.jpg",
    "11_shared_stick": "11_shared_stick_start.jpg",
}


def probe_dur(path: Path) -> float:
    return float(
        subprocess.check_output(
            [
                "ffprobe", "-v", "error", "-show_entries", "format=duration",
                "-of", "default=nw=1:nk=1", str(path),
            ],
            text=True,
        ).strip()
    )


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def ken_burns(still: Path, dest: Path, seconds: float = CLIP_USE) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    frames = max(int(seconds * 24), 24)
    vf = (
        f"scale=1920:1080:force_original_aspect_ratio=increase,"
        f"crop=1920:1080,"
        f"zoompan=z='min(1.08,1+0.08*on/{frames})':"
        f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1920x1080:fps=24,"
        f"trim=0:{seconds},setpts=PTS-STARTPTS,format=yuv420p"
    )
    subprocess.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-loop", "1", "-i", str(still),
            "-vf", vf, "-t", f"{seconds:.3f}",
            "-c:v", "libx264", "-preset", "medium", "-crf", "18",
            "-pix_fmt", "yuv420p", "-an", str(dest),
        ],
        check=True,
    )


def resolve_clip(plate: dict) -> Path:
    pid = plate["id"]
    kind = plate.get("kind", "")
    if kind in {"chapter_card", "teach_card"}:
        mp4 = RAW / f"{pid}_v01.mp4"
        if not mp4.exists() or mp4.stat().st_size < 400_000:
            raise SystemExit(f"missing card clip: {mp4}")
        return mp4
    if kind != "scenery":
        raise SystemExit(f"unknown plate kind {kind} for {pid}")
    stem = SCENERY_STILLS.get(pid)
    if not stem:
        raise SystemExit(f"no still mapping for scenery plate {pid}")
    still = STILLS / stem
    if not still.exists() or still.stat().st_size < 50_000:
        raise SystemExit(f"missing/weak Flow still: {still}")
    dest = KB_DIR / f"{pid}_kb_v04.mp4"
    if not dest.exists() or dest.stat().st_mtime < still.stat().st_mtime:
        print(f"  Ken Burns {pid} ← {still.name}", flush=True)
        ken_burns(still, dest)
    return dest


def main() -> None:
    plates = json.loads(PLATES_JSON.read_text())["plates"]
    clips: list[Path] = []
    for plate in plates:
        clip = resolve_clip(plate)
        d = probe_dur(clip)
        if d < 5.5:
            raise SystemExit(f"STOP short clip {clip} d={d}")
        clips.append(clip)
        print(f"  {plate['id']}: {clip.name} {clip.stat().st_size}b {d:.2f}s", flush=True)

    if not VO.exists():
        raise SystemExit(f"missing VO {VO}")
    if not BED.exists():
        raise SystemExit(f"missing bed {BED}")
    vo_dur = probe_dur(VO)
    pic_dur = len(clips) * CLIP_USE - (len(clips) - 1) * XFADE
    print(f"picture≈{pic_dur:.2f}s VO={vo_dur:.2f}s", flush=True)
    if pic_dur + 0.05 < vo_dur:
        raise SystemExit(f"picture {pic_dur:.2f} < VO {vo_dur:.2f}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    inputs: list[str] = []
    for c in clips:
        inputs += ["-i", str(c)]
    n = len(clips)
    inputs += ["-i", str(VO), "-i", str(BED)]
    parts: list[str] = []
    for i in range(n):
        parts.append(
            f"[{i}:v]trim=0:{CLIP_USE},setpts=PTS-STARTPTS,"
            f"scale=1920:1080:force_original_aspect_ratio=decrease,"
            f"pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps=24,format=yuv420p[v{i}]"
        )
    vlabel = "[v0]"
    for i in range(1, n):
        out = f"[vx{i}]"
        parts.append(
            f"{vlabel}[v{i}]xfade=transition=fade:duration={XFADE}:offset="
            f"{(CLIP_USE - XFADE) * i:.3f}{out}"
        )
        vlabel = out
    parts.append(
        f"[{n}:a]aformat=sample_rates=48000:channel_layouts=stereo,"
        f"atrim=0:{vo_dur:.3f},asetpts=PTS-STARTPTS[vo]"
    )
    parts.append(
        f"[{n+1}:a]aformat=sample_rates=48000:channel_layouts=stereo,"
        f"atrim=0:{vo_dur:.3f},volume={BED_VOL}[bed]"
    )
    parts.append("[vo][bed]amix=inputs=2:duration=first:dropout_transition=0[a]")
    fc = ";".join(parts)
    subprocess.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            *inputs,
            "-filter_complex", fc,
            "-map", vlabel, "-map", "[a]",
            "-c:v", "libx264", "-preset", "medium", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart", "-t", f"{vo_dur:.3f}",
            str(OUT),
        ],
        check=True,
    )
    digest = sha256(OUT)
    print(
        f"SAVED {OUT} bytes={OUT.stat().st_size} dur≈{probe_dur(OUT):.2f}s sha256={digest}",
        flush=True,
    )
    ICLOUD.mkdir(parents=True, exist_ok=True)
    dest = ICLOUD / OUT.name
    subprocess.run(["cp", "-f", str(OUT), str(dest)], check=True)
    for stale in ICLOUD.glob("WATCH_part02*.txt"):
        stale.unlink(missing_ok=True)
    watch = ICLOUD / "WATCH_part02_v04.txt"
    watch.write_text(
        "WATCH THIS FILE ONLY (v04 — replaces v03):\n"
        f"  {OUT.name}\n\n"
        "What changed vs v03:\n"
        "- Removed unfinished Pillow desks\n"
        "- Removed Flow clips with jars/pots on fire\n"
        "- Scenery = finished jar-free Flow stills (Ken Burns) + chapter/triad cards\n"
        "- Candle wick OK; jars/pots never on fire\n\n"
        "Part 01 is PASS. Reject with stills from THIS v04 file only.\n"
        "Do NOT start Part 03 until Ben PASSes this cut.\n"
        f"sha256={digest}\n"
    )
    print(f"ICLOUD {dest}", flush=True)
    print(f"WATCH {watch}", flush=True)


if __name__ == "__main__":
    main()
