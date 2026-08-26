#!/usr/bin/env python3
"""Part 01 v08 — v01 cartoon baseline, fewer germ floats, faceless microbes.

Ben UAT (26 Aug 2026):
- Keep v01 Animistry cartoon style (not v03–v07 redesigns)
- Too many germ-floating scenes → reduce
- Last ~5s still smiling → faceless deadly only

Method:
- Story stills = Gemini-edited germ-free frames from v01 plates
- Germ stills = clean ward + composited isolated FACELESS microbe assets
- Veo lite I2V with hard no-face lock on germ plates
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))

from orbit_gemini_veo import (  # noqa: E402
    DEFAULT_MODEL,
    already_done,
    load_dotenv,
    make_client,
    strip_audio,
)

PROJ = Path(__file__).resolve().parents[1]
STILLS = PROJ / "04_Generated-Clips" / "part01" / "refs" / "v08_stills"
RAW = PROJ / "04_Generated-Clips" / "part01" / "raw" / "v08_faceless"
VO = PROJ / "02_Voiceover" / "part01_invisible_enemy_v01.mp3"
OUT = PROJ / "09_Final-Export" / "hos_001_part01_rough_v08.mp4"
META = PROJ / "07_Edit-Project" / "part01_gen_meta_v08.json"
ART = Path("/opt/cursor/artifacts")

CLIP_USE = 8.0
XFADE = 0.40
FPS = 24

STYLE = (
    "Premium 3D cartoon Animistry style matching the start frame exactly. "
    "Victorian period hospital. Silent picture only. Continuous gentle motion. "
    "NO photoreal. NO modern hospital. NO text. NO logos."
)

NO_GERMS = (
    "NO floating germs, microbes, orbs, sparkles, or particle swarms. Empty air."
)

FACELESS = (
    "If microbes are visible in the start frame, KEEP them exactly faceless: "
    "glassy spiked spheres / rods / spirals only. "
    "NO eyes, NO mouths, NO smiles, NO winks, NO cute faces, NOT mascots. "
    "Do NOT add new facial features. Do NOT increase microbe count. Sparse deadly pathogens."
)

PLATES = [
    (
        "01_corridor",
        STILLS / "02_corridor_clean.jpg",
        f"Animate this clean Victorian hospital corridor. Slow dolly forward toward the "
        f"window. Soft lamp flicker. {NO_GERMS} {STYLE}",
    ),
    (
        "02_curtains",
        STILLS / "03_curtains_clean.jpg",
        f"Animate this Victorian ward aisle with beds and curtains. Gentle camera drift "
        f"forward. Soft lamp flicker, quiet empty air. {NO_GERMS} {STYLE}",
    ),
    (
        "03_explorer",
        STILLS / "04_explorer_clean.jpg",
        f"Animate the Explorer boy peeking through the doorway into the ward. Subtle "
        f"breathing and slight lean forward. Keep character identity. {NO_GERMS} {STYLE}",
    ),
    (
        "04_instruments",
        STILLS / "05_instruments_clean.jpg",
        f"Animate Victorian doctor hands near instruments under warm lamp light. Subtle "
        f"camera orbit, soft metal reflections. {NO_GERMS} {STYLE}",
    ),
    (
        "05_fever",
        STILLS / "06_fever_clean.jpg",
        f"Animate the feverish bedside. Slow push-in, soft lamp flicker, subtle breathing. "
        f"{NO_GERMS} {STYLE}",
    ),
    (
        "06_breath_ward",
        STILLS / "08_breath_clean.jpg",
        f"Animate this Victorian ward atmosphere. Gentle camera drift, soft chandelier "
        f"glow. {NO_GERMS} {STYLE}",
    ),
    (
        "07_hands",
        STILLS / "09_hands_clean.jpg",
        f"Animate doctor hands in the ward. Subtle motion toward the bedside. Soft "
        f"bokeh background. {NO_GERMS} {STYLE}",
    ),
    (
        "08_ward_calm",
        STILLS / "03_curtains_clean.jpg",
        f"Animate this Victorian ward. Slow lateral drift along the beds and curtains. "
        f"Soft lamp flicker. {NO_GERMS} {STYLE}",
    ),
    (
        "09_sparse_faceless",
        STILLS / "05_instruments_sparse_faceless.jpg",
        f"Animate this frame. Soft camera drift. Only a few microbes drift slowly like "
        f"dangerous dust on instruments. {FACELESS} {STYLE}",
    ),
    (
        "10_end_faceless",
        STILLS / "10_ward_end_faceless.jpg",
        f"Animate this Victorian ward wide shot for the closing hold. Slow gentle pull-back. "
        f"Sparse deadly microbes drift in the aisle air. {FACELESS} "
        f"Highest intensity is the faceless pathogen presence — never cute. {STYLE}",
    ),
]


def resolve_keys() -> None:
    for p in (
        REPO / "04_Audio" / "tools" / ".env",
        PROJ / "07_Edit-Project" / ".env",
    ):
        load_dotenv(p)


def gen_i2v(client, model: str, still: Path, prompt: str, dest: Path) -> dict:
    from google.genai import types

    if already_done(dest, min_bytes=400_000):
        print(f"  skip {dest.name}", flush=True)
        return {"skipped": True, "bytes": dest.stat().st_size}

    img = types.Image.from_file(location=str(still))
    config = types.GenerateVideosConfig(
        number_of_videos=1,
        duration_seconds=8,
        aspect_ratio="16:9",
        resolution="720p",
    )
    last_err: Exception | None = None
    for attempt in range(1, 4):
        try:
            print(f"  submit {dest.stem} attempt={attempt} model={model}", flush=True)
            t0 = time.time()
            op = client.models.generate_videos(
                model=model, prompt=prompt, image=img, config=config
            )
            while not op.done:
                time.sleep(12)
                op = client.operations.get(op)
                print(f"  poll {dest.stem} {int(time.time() - t0)}s", flush=True)
            if op.error:
                raise RuntimeError(op.error)
            if not op.response or not op.response.generated_videos:
                raise RuntimeError("no video")
            video = op.response.generated_videos[0]
            dest.parent.mkdir(parents=True, exist_ok=True)
            client.files.download(file=video.video)
            video.video.save(str(dest))
            strip_audio(dest)
            return {"seconds": round(time.time() - t0, 1), "bytes": dest.stat().st_size}
        except Exception as e:
            last_err = e
            print(f"  FAIL {dest.stem}: {e}", flush=True)
            s = str(e)
            sleep_s = 60 * attempt if ("429" in s or "RESOURCE_EXHAUSTED" in s) else 15 * attempt
            time.sleep(sleep_s)
    raise RuntimeError(f"{dest.stem} failed: {last_err}")


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
    resolve_keys()
    model = os.environ.get("ORBIT_VEO_MODEL", DEFAULT_MODEL)
    print(f"Using model: {model}", flush=True)
    client = make_client()
    RAW.mkdir(parents=True, exist_ok=True)
    meta = {
        "model": model,
        "mode": "v08_v01_style_fewer_germs_faceless",
        "notes": [
            "Keep v01 cartoon baseline",
            "Drop dense germ-float open + macro cloud",
            "Only late sparse + end hold use composited FACELESS microbes",
        ],
        "plates": [],
    }
    paths: list[Path] = []

    for pid, still, prompt in PLATES:
        if not still.exists():
            raise SystemExit(f"missing still {still}")
        dest = RAW / f"{pid}_v08.mp4"
        info = gen_i2v(client, model, still, prompt, dest)
        meta["plates"].append({"id": pid, "still": str(still), **info, "path": str(dest)})
        paths.append(dest)

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
            "-movflags", "+faststart", str(ART / "hos_001_part01_rough_v08_demo.mp4"),
        ],
        check=False,
        capture_output=True,
    )
    print(json.dumps(meta, indent=2))
    print(f"SAVED {OUT} ~{pic_dur:.1f}s", flush=True)


if __name__ == "__main__":
    main()
