#!/usr/bin/env python3
"""Part 01 v06 — real Veo I2V motion from locked v05 stills (lite model).

Uses veo-3.1-lite-generate-preview (Fast is 429 on its own quota bucket).
Ward-first narrative: patients → Explorer past beds → sparse microbes late.
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
RAW = PROJ / "04_Generated-Clips" / "part01" / "raw" / "v06"
REFS = PROJ / "04_Generated-Clips" / "part01" / "refs"
VO = PROJ / "02_Voiceover" / "part01_invisible_enemy_v01.mp3"
OUT = PROJ / "09_Final-Export" / "hos_001_part01_rough_v06.mp4"
META = PROJ / "07_Edit-Project" / "part01_gen_meta_v06.json"
ART = Path("/opt/cursor/artifacts")
REF_EXPLORER = REPO / "01_Character" / "05_Generation-References" / "hos-explorer-reference-v01.jpg"

CLIP_USE = 7.5
XFADE = 0.55
FPS = 24

# (id, start_still, prompt) — I2V from locked compositions
PLATES = [
    (
        "01_ward_open",
        REFS / "ward_open_a_v05.jpg",
        "Animate this exact Victorian hospital ward. Continuous slow camera push down "
        "the aisle past the two sick patients in beds. Subtle chest breathing on patients, "
        "soft oil-lamp flicker. Keep composition and characters. NO floating germs. "
        "Silent picture only. Premium 3D cartoon.",
    ),
    (
        "02_corridor",
        REFS / "corridor_a_v05.jpg",
        "Animate this clean Victorian hospital corridor. Continuous slow dolly forward "
        "toward the window. Soft lamp flicker. Empty aisle. NO germs, NO floating orbs. "
        "Silent. Premium 3D cartoon.",
    ),
    (
        "03_patients",
        REFS / "patients_a_v05.jpg",
        "Animate these two ill patients in beds. Gentle camera drift closer. Subtle "
        "breathing, soft lamp flicker. Keep faces and layout. NO germs. Silent. Premium 3D cartoon.",
    ),
    (
        "04_explorer",
        REFS / "explorer_b_v05.jpg",
        "Animate the Explorer boy walking slowly past the hospital beds with quiet concern. "
        "Continuous walking motion, satchel moves with him, soft lamp light. Keep character "
        "identity. Sick patients stay in beds. NO germs. Silent. Premium 3D cartoon.",
    ),
    (
        "05_instruments",
        REFS / "hands_a_v05.jpg",
        "Animate Victorian doctor hands and instruments under warm lamp light. Subtle "
        "camera orbit, soft reflections on metal. NO germ swarm. Silent. Premium 3D cartoon.",
    ),
    (
        "06_fever",
        REFS / "fever_a_v05.jpg",
        "Animate the feverish patient in bed. Slow push-in, subtle breathing, soft lamp "
        "flicker. NO germs. Silent. Premium 3D cartoon.",
    ),
    (
        "07_micro_hint",
        REFS / "micro_hint_a_v05.jpg",
        "Animate these sparse faceless translucent bacteria drifting slowly like dangerous "
        "dust. Continuous gentle drift and parallax. NO faces, NO smiles, NOT cute. Silent.",
    ),
    (
        "08_hands",
        REFS / "hands_b_v05.jpg",
        "Animate doctor hands moving from one sick bedside toward another. Continuous "
        "tracking. NO microbe swarm. Silent. Premium 3D cartoon.",
    ),
    (
        "09_micro_close",
        REFS / "micro_close_a_v05.jpg",
        "Animate a few faceless glassy bacteria tumbling slowly in soft light. Continuous "
        "motion. NO faces, NO smiles. Silent. Scientific 3D.",
    ),
    (
        "10_ward_hold",
        REFS / "ward_hold_a_v05.jpg",
        "Animate this Victorian ward wide shot. Slow pull-back, soft lamp flicker, quiet "
        "patients in beds. NO germ swarm. Silent. Premium 3D cartoon.",
    ),
]

NEGATIVE = (
    "smiling germs, cute faces on bacteria, anthropomorphic germs, freeze frame, "
    "slideshow, text, logos, watermark, dialogue, speech, twin Explorers"
)


def resolve_keys() -> None:
    for p in (
        REPO / "04_Audio" / "tools" / ".env",
        PROJ / "07_Edit-Project" / ".env",
    ):
        load_dotenv(p)


def gen_i2v(client, model: str, still: Path, prompt: str, dest: Path) -> dict:
    from google.genai import types

    if already_done(dest):
        print(f"  skip {dest.name}", flush=True)
        return {"skipped": True, "bytes": dest.stat().st_size}

    img = types.Image.from_file(location=str(still))
    config = types.GenerateVideosConfig(
        number_of_videos=1,
        duration_seconds=8,
        aspect_ratio="16:9",
        resolution="720p",
        negative_prompt=NEGATIVE,
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
    meta = {"model": model, "plates": [], "mode": "veo_i2v_v06"}
    paths: list[Path] = []

    for pid, still, prompt in PLATES:
        if not still.exists():
            raise SystemExit(f"missing still {still}")
        dest = RAW / f"{pid}_v06.mp4"
        info = gen_i2v(client, model, still, prompt, dest)
        meta["plates"].append({"id": pid, "still": str(still), **info, "path": str(dest)})
        paths.append(dest)

    pic_dur = assemble(paths)
    meta["out"] = str(OUT)
    meta["pic_dur"] = pic_dur
    META.write_text(json.dumps(meta, indent=2))
    ART.mkdir(parents=True, exist_ok=True)
    subprocess.run(["cp", "-f", str(OUT), str(ART / OUT.name)], check=False)
    # demo under 15MB
    subprocess.run(
        [
            "ffmpeg", "-y", "-i", str(OUT), "-vf", "scale=960:540",
            "-c:v", "libx264", "-crf", "28", "-c:a", "aac", "-b:a", "96k",
            "-movflags", "+faststart", str(ART / "hos_001_part01_rough_v06_demo.mp4"),
        ],
        check=False, capture_output=True,
    )
    print(json.dumps(meta, indent=2))
    print(f"SAVED {OUT} ~{pic_dur:.1f}s", flush=True)


if __name__ == "__main__":
    main()
