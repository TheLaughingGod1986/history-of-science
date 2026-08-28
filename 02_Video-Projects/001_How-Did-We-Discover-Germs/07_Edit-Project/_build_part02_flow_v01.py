#!/usr/bin/env python3
"""Part 02 Flow Veo I2V from locked stills — real motion (no still-zoom).

Requires Flow Ultra login profile (~/.playwright-hos-flow-profile).
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))

import orbit_flow_veo_ui as flow  # noqa: E402
import orbit_gemini_veo as veo  # noqa: E402

PROJ = Path(__file__).resolve().parents[1]
PLATES_JSON = PROJ / "07_Edit-Project" / "parts" / "part-02_plates_v01.json"
REFS = PROJ / "04_Generated-Clips" / "part02" / "refs"
RAW = PROJ / "04_Generated-Clips" / "part02" / "raw" / "v01_flow"
VO = PROJ / "02_Voiceover" / "part02_seeing_tiny_world_v01.mp3"
OUT = PROJ / "09_Final-Export" / "hos_001_part02_rough_v01.mp4"
META = PROJ / "07_Edit-Project" / "part02_gen_meta_v01.json"
ART = Path("/opt/cursor/artifacts")
DEFAULT_PROFILE = Path(
    os.environ.get("ORBIT_FLOW_PROFILE", str(Path.home() / ".playwright-hos-flow-profile"))
)
MODEL = os.environ.get("ORBIT_FLOW_VEO_MODEL", "Veo 3.1 - Fast")
CLIP_USE = 8.0
XFADE = 0.40
FPS = 24

FACELESS = (
    "Keep microbes FACELESS if present: rods/spheres/spirals only. "
    "NO eyes NO mouths NO smiles NO winks. Continuous motion whole clip — never freeze. "
    "Premium 3D cartoon matching start frame. Silent. NOT photoreal. NOT modern hospital. "
    "FORBIDDEN: photographic cameras, camcorders, film cameras, multi-lens gadgets."
)


def assemble(clips: list[Path]) -> float:
    n = len(clips)
    inputs: list[str] = []
    for c in clips:
        inputs += ["-i", str(c)]
    inputs += ["-i", str(VO)]
    parts = [
        f"[{i}:v]trim=0:{CLIP_USE},setpts=PTS-STARTPTS,"
        f"scale=1280:720:force_original_aspect_ratio=decrease,"
        f"pad=1280:720:(ow-iw)/2:(oh-ih)/2,fps={FPS},format=yuv420p[v{i}]"
        for i in range(n)
    ]
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
    # xfade can promote to yuv444p; browsers/QuickTime then refuse playback.
    parts.append(f"[{vprev}]format=yuv420p[vout]")
    afilter = (
        f"[{n}:a]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo,"
        f"atrim=0:{pic_dur:.3f},apad=whole_dur={pic_dur:.3f}[a]"
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg", "-y", *inputs,
            "-filter_complex", ";".join(parts) + ";" + afilter,
            "-map", "[vout]", "-map", "[a]",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-profile:v", "high",
            "-preset", "fast", "-crf", "17",
            "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(OUT),
        ],
        check=True,
    )
    return pic_dur


def clip_paths(plates: list[dict]) -> list[Path]:
    paths = []
    for plate in plates:
        dest = RAW / f"{plate['id']}_v01.mp4"
        if not veo.already_done(dest, min_bytes=400_000):
            raise FileNotFoundError(dest)
        paths.append(dest)
    return paths


def main() -> None:
    plates = json.loads(PLATES_JSON.read_text())["plates"]
    RAW.mkdir(parents=True, exist_ok=True)
    profile = flow.profile_path(DEFAULT_PROFILE)
    print(f"Flow profile={profile} model={MODEL}", flush=True)

    meta = {"engine": "flow-ui", "model": MODEL, "style_lock": "v08_pass", "plates": []}
    paths: list[Path] = []
    missing = [
        plate["id"]
        for plate in plates
        if not veo.already_done(RAW / f"{plate['id']}_v01.mp4", min_bytes=400_000)
    ]

    if not missing:
        print(f"  all {len(plates)} Flow clips present — assemble only (no Flow)", flush=True)
        paths = clip_paths(plates)
        meta["plates"] = [{"id": p.stem, "skipped": True, "path": str(p)} for p in paths]
    else:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            ctx, page = flow.launch_context(p, headed=False, profile=profile)
            try:
                for i, plate in enumerate(plates):
                    still = REFS / plate.get("start_still", f"{plate['id']}_v01.jpg")
                    dest = RAW / f"{plate['id']}_v01.mp4"
                    if not still.exists():
                        raise SystemExit(f"missing still {still}")
                    if veo.already_done(dest, min_bytes=400_000):
                        print(f"  skip {dest.name}", flush=True)
                        meta["plates"].append({"id": plate["id"], "skipped": True, "path": str(dest)})
                        paths.append(dest)
                        continue
                    prompt = f"{plate['prompt']} {FACELESS}"
                    print(f"\n=== Flow I2V {plate['id']} ({i+1}/{len(plates)}) ===", flush=True)
                    info = flow.generate_clip(
                        page,
                        prompt,
                        dest,
                        model=MODEL,
                        start_frame=still,
                        timeout_s=700,
                        reuse_project=False,
                        scenery_only=not plate.get("explorer", False),
                        attempts=2,
                    )
                    veo.strip_audio(dest)
                    meta["plates"].append({"id": plate["id"], **info, "path": str(dest)})
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
            "ffmpeg", "-y", "-i", str(OUT), "-vf", "scale=960:540,format=yuv420p",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-profile:v", "high", "-crf", "28",
            "-c:a", "aac", "-b:a", "96k",
            "-movflags", "+faststart", str(ART / "hos_001_part02_rough_v01_demo.mp4"),
        ],
        check=False,
        capture_output=True,
    )
    print(json.dumps(meta, indent=2))
    print(f"SAVED {OUT} ~{pic_dur:.1f}s — STOP for Ben UAT", flush=True)


if __name__ == "__main__":
    main()
