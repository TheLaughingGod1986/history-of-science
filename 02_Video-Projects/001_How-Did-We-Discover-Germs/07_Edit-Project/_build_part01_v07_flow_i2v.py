#!/usr/bin/env python3
"""History of Science Episode 001 — Part 01 Flow Veo I2V (primary CG path).

Uses Google Flow Ultra (same pipe as Orbit With Ben), not Gemini API Fast.
Animates locked v05 stills → real motion plates → assemble rough v07.

Requires one-time Flow login:
  ORBIT_FLOW_PROFILE=... python3 04_Audio/tools/orbit_flow_veo_ui.py --login
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
TOOLS = REPO / "04_Audio" / "tools"
sys.path.insert(0, str(TOOLS))

import orbit_flow_veo_ui as flow  # noqa: E402
import orbit_gemini_veo as veo  # noqa: E402

PROJ = Path(__file__).resolve().parents[1]
REFS = PROJ / "04_Generated-Clips" / "part01" / "refs"
RAW = PROJ / "04_Generated-Clips" / "part01" / "raw" / "v07_flow"
VO = PROJ / "02_Voiceover" / "part01_invisible_enemy_v01.mp3"
OUT = PROJ / "09_Final-Export" / "hos_001_part01_rough_v07.mp4"
META = PROJ / "07_Edit-Project" / "part01_gen_meta_v07.json"
ART = Path("/opt/cursor/artifacts")
# Prefer dedicated HOS Flow profile; fall back to Orbit Flow profile.
DEFAULT_PROFILE = Path(
    os.environ.get(
        "ORBIT_FLOW_PROFILE",
        str(Path.home() / ".playwright-hos-flow-profile"),
    )
)

CLIP_USE = 7.5
XFADE = 0.55
FPS = 24
MODEL = os.environ.get("ORBIT_FLOW_VEO_MODEL", "Veo 3.1 - Quality")

PLATES = [
    (
        "01_ward_open",
        REFS / "ward_open_a_v05.jpg",
        "Continuous slow camera push down the Victorian ward aisle past two sick "
        "patients in beds. Subtle breathing, soft lamp flicker. NO germs.",
    ),
    (
        "02_corridor",
        REFS / "corridor_a_v05.jpg",
        "Continuous slow dolly forward down the clean hospital corridor toward the "
        "window. Soft lamp flicker. Empty aisle. NO germs, NO floating orbs.",
    ),
    (
        "03_patients",
        REFS / "patients_a_v05.jpg",
        "Gentle camera drift closer on two ill patients in beds. Subtle breathing, "
        "soft lamp flicker. NO germs.",
    ),
    (
        "04_explorer",
        REFS / "explorer_b_v05.jpg",
        "The Explorer boy walks slowly past the hospital beds with quiet concern. "
        "Continuous walking motion. Sick patients stay in beds. NO germs.",
    ),
    (
        "05_instruments",
        REFS / "hands_a_v05.jpg",
        "Subtle camera orbit of Victorian doctor hands and instruments under warm "
        "lamp light. Soft metal reflections. NO germ swarm.",
    ),
    (
        "06_fever",
        REFS / "fever_a_v05.jpg",
        "Slow push-in on the feverish patient in bed. Subtle breathing, soft lamp "
        "flicker. NO germs.",
    ),
    (
        "07_micro_hint",
        REFS / "micro_hint_a_v05.jpg",
        "Sparse faceless translucent bacteria drift slowly like dangerous dust. "
        "Continuous gentle drift. NO faces, NO smiles, NOT cute.",
    ),
    (
        "08_hands",
        REFS / "hands_b_v05.jpg",
        "Doctor hands move from one sick bedside toward another. Continuous tracking. "
        "NO microbe swarm.",
    ),
    (
        "09_micro_close",
        REFS / "micro_close_a_v05.jpg",
        "A few faceless glassy bacteria tumble slowly in soft light. Continuous motion. "
        "NO faces, NO smiles.",
    ),
    (
        "10_ward_hold",
        REFS / "ward_hold_a_v05.jpg",
        "Slow pull-back on the Victorian ward. Soft lamp flicker, quiet patients in "
        "beds. NO germ swarm.",
    ),
]


def assemble(clips: list[Path]) -> float:
    n = len(clips)
    inputs: list[str] = []
    for c in clips:
        inputs += ["-i", str(c)]
    inputs += ["-i", str(VO)]
    parts = []
    for i in range(n):
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
    pic_dur = n * CLIP_USE - (n - 1) * XFADE
    afilter = (
        f"[{n}:a]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo,"
        f"atrim=0:{pic_dur:.3f},apad=whole_dur={pic_dur:.3f}[a]"
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg", "-y", *inputs,
            "-filter_complex", ";".join(parts) + ";" + afilter,
            "-map", f"[{vprev}]", "-map", "[a]",
            "-c:v", "libx264", "-preset", "fast", "-crf", "17",
            "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart", str(OUT),
        ],
        check=True,
    )
    return pic_dur


def main() -> None:
    profile = flow.profile_path(DEFAULT_PROFILE)
    print(f"Flow profile: {profile}", flush=True)
    print(f"Flow model: {MODEL}", flush=True)
    RAW.mkdir(parents=True, exist_ok=True)

    from playwright.sync_api import sync_playwright

    meta = {"engine": "flow-ui", "model": MODEL, "profile": str(profile), "plates": []}
    paths: list[Path] = []

    with sync_playwright() as p:
        ctx, page = flow.launch_context(p, headed=False, profile=profile)
        try:
            for i, (pid, still, prompt) in enumerate(PLATES):
                if not still.exists():
                    raise SystemExit(f"missing still {still}")
                dest = RAW / f"{pid}_v07.mp4"
                if veo.already_done(dest):
                    print(f"  skip {dest.name}", flush=True)
                    meta["plates"].append({"id": pid, "skipped": True, "path": str(dest)})
                    paths.append(dest)
                    continue
                print(f"\n=== Flow I2V {pid} ({i+1}/{len(PLATES)}) ===", flush=True)
                info = flow.generate_clip(
                    page,
                    prompt,
                    dest,
                    model=MODEL,
                    start_frame=still,
                    timeout_s=900,
                    reuse_project=(i > 0),
                    attempts=2,
                )
                meta["plates"].append({"id": pid, **info, "path": str(dest)})
                paths.append(dest)
        finally:
            ctx.close()

    pic_dur = assemble(paths)
    meta["out"] = str(OUT)
    meta["pic_dur"] = pic_dur
    META.write_text(json.dumps(meta, indent=2))
    ART.mkdir(parents=True, exist_ok=True)
    subprocess.run(["cp", "-f", str(OUT), str(ART / OUT.name)], check=False)
    subprocess.run(
        [
            "ffmpeg", "-y", "-i", str(OUT), "-vf", "scale=960:540",
            "-c:v", "libx264", "-crf", "28", "-c:a", "aac", "-b:a", "96k",
            "-movflags", "+faststart", str(ART / "hos_001_part01_rough_v07_demo.mp4"),
        ],
        check=False,
        capture_output=True,
    )
    print(json.dumps(meta, indent=2))
    print(f"SAVED {OUT} ~{pic_dur:.1f}s", flush=True)


if __name__ == "__main__":
    main()
