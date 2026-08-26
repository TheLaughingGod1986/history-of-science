#!/usr/bin/env python3
"""Part 01 v04 interim rough — ward-first stillbridges when Veo quota is exhausted.

Ben UAT 26 Aug 2026: human ward + sick patients first; Explorer walks past beds;
germs late + sparse + faceless. True motion plates resume via
`_build_part01_rough_v01.py` when Gemini Veo quota recovers.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
RAW = PROJ / "04_Generated-Clips" / "part01" / "raw"
REFS = PROJ / "04_Generated-Clips" / "part01" / "refs"
VO = PROJ / "02_Voiceover" / "part01_invisible_enemy_v01.mp3"
OUT = PROJ / "09_Final-Export" / "hos_001_part01_rough_v04.mp4"
META = PROJ / "07_Edit-Project" / "part01_gen_meta_v04.json"
ART = Path("/opt/cursor/artifacts")

CLIP_USE = 7.2
XFADE = 0.4
FPS = 24
FRAMES = int(CLIP_USE * FPS)

PLAN = [
    ("01_ward_open_patients", REFS / "ward_two_patients_v04.jpg"),
    ("02_clean_corridor", RAW / "02_clean_corridor_v01.mp4"),
    ("03_two_ill_patients", REFS / "two_ill_patients_close_v04.jpg"),
    ("04_explorer_walks_past_beds", REFS / "explorer_walks_past_beds_v04.jpg"),
    ("05_doctor_hands_instruments", RAW / "05_doctor_hands_instruments_v01.mp4"),
    ("06_fever_patient", REFS / "fever_patient_v04.jpg"),
    ("07_sparse_microbes_hint", REFS / "sparse_microbes_hint_v04.jpg"),
    ("08_hands_between_patients", REFS / "hands_between_patients_v04.jpg"),
    ("09_sparse_microbes_close", REFS / "sparse_microbes_close_v04.jpg"),
    ("10_ward_hold_patients", REFS / "ward_hold_patients_v04.jpg"),
]


def stillbridge(src: Path, dest: Path) -> None:
    vf = (
        "scale=1280:720:force_original_aspect_ratio=increase,"
        "crop=1280:720,"
        f"zoompan=z='min(zoom+0.0008,1.12)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
        f"d={FRAMES}:s=1280x720:fps={FPS},format=yuv420p"
    )
    subprocess.run(
        [
            "ffmpeg", "-y", "-loop", "1", "-i", str(src),
            "-vf", vf, "-t", str(CLIP_USE), "-an",
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-pix_fmt", "yuv420p", str(dest),
        ],
        check=True,
        capture_output=True,
    )


def motion_trim(src: Path, dest: Path) -> None:
    vf = (
        f"trim=0:{CLIP_USE},setpts=PTS-STARTPTS,"
        "scale=1280:720:force_original_aspect_ratio=decrease,"
        f"pad=1280:720:(ow-iw)/2:(oh-ih)/2,fps={FPS},format=yuv420p"
    )
    subprocess.run(
        [
            "ffmpeg", "-y", "-i", str(src),
            "-vf", vf, "-an",
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            str(dest),
        ],
        check=True,
        capture_output=True,
    )


def assemble(clips: list[Path]) -> float:
    n = len(clips)
    inputs: list[str] = []
    for c in clips:
        inputs += ["-i", str(c)]
    inputs += ["-i", str(VO)]

    parts = [f"[{i}:v]format=yuv420p[v{i}]" for i in range(n)]
    vprev = "v0"
    offset = CLIP_USE - XFADE
    for i in range(1, n):
        out = f"vx{i}"
        parts.append(
            f"[{vprev}][v{i}]xfade=transition=fade:duration={XFADE}:offset={offset:.3f}[{out}]"
        )
        vprev = out
        offset += CLIP_USE - XFADE
    pic_dur = n * CLIP_USE - (n - 1) * XFADE
    afilter = (
        f"[{n}:a]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo,"
        f"atrim=0:{pic_dur:.3f},apad=whole_dur={pic_dur:.3f}[a]"
    )
    fc = ";".join(parts) + ";" + afilter
    OUT.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg", "-y", *inputs, "-filter_complex", fc,
            "-map", f"[{vprev}]", "-map", "[a]",
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k", "-shortest",
            "-movflags", "+faststart", str(OUT),
        ],
        check=True,
    )
    return pic_dur


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    clips: list[Path] = []
    for pid, src in PLAN:
        if not src.exists():
            raise SystemExit(f"Missing source for {pid}: {src}")
        dest = RAW / f"{pid}_v04.mp4"
        if src.suffix.lower() in {".jpg", ".jpeg", ".png"}:
            print(f"stillbridge {pid}", flush=True)
            stillbridge(src, dest)
        else:
            print(f"motion {pid}", flush=True)
            motion_trim(src, dest)
        clips.append(dest)

    pic_dur = assemble(clips)
    print(f"SAVED {OUT} ({OUT.stat().st_size} bytes) ~{pic_dur:.1f}s", flush=True)
    ART.mkdir(parents=True, exist_ok=True)
    if OUT.exists():
        subprocess.run(["cp", "-f", str(OUT), str(ART / OUT.name)], check=False)
    meta = {
        "out": str(OUT),
        "mode": "still_interim_v04",
        "note": (
            "Veo quota blocked; ward-first stillbridges + corridor/hands motion "
            "for Ben UAT of patients + Explorer past beds"
        ),
        "plates": [p[0] for p in PLAN],
        "pic_dur": pic_dur,
    }
    META.write_text(json.dumps(meta, indent=2))
    print(json.dumps(meta, indent=2))


if __name__ == "__main__":
    main()
