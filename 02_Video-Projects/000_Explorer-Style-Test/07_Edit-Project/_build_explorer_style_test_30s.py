#!/usr/bin/env python3
"""History of Science — ~30s Explorer style test (Gemini Veo).

Story-first 3D cartoon library beat + sparse Explorer (2 of 4 plates).
Requires: GEMINI_API_KEY. Optional: ELEVENLABS_API_KEY for British VO bed.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
import urllib.request
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
from orbit_voice import (  # noqa: E402
    CG_SILENT_AUDIO_BLOCK,
    MODEL_ID,
    VOICE_ID,
    VOICE_SETTINGS,
)

PROJ = Path(__file__).resolve().parents[1]
RAW = PROJ / "04_Generated-Clips" / "raw"
OUT = PROJ / "09_Final-Export" / "hos_explorer_style_test_30s_v01.mp4"
VO_PATH = PROJ / "02_Voiceover" / "style_test_vo_v01.mp3"
REF = REPO / "01_Character" / "05_Generation-References" / "hos-explorer-reference-v01.jpg"
META_PATH = PROJ / "07_Edit-Project" / "style_test_gen_meta_v01.json"

CLIP_USE_S = 7.2  # usable seconds per ~8s Veo plate
XFADE = 0.4

EXPLORER_LOCK = (
    "CRITICAL CHARACTER IDENTITY — match the attached reference exactly: "
    "young boy Explorer, messy wavy brown hair, round thin gold wire-rim glasses, "
    "teal-blue long overcoat with gold atom lapel pin, tan waistcoat, white shirt, "
    "dark brown floppy bow tie, brown trousers rolled at cuffs, cream socks, "
    "sturdy brown lace-up boots, brown leather satchel with brass compass, "
    "rolled parchment map in coat pocket. Premium 3D cartoon feature-animation "
    "polish, soft cinematic light, stylised materials — NOT photoreal, NOT flat 2D cel."
)

NEGATIVE = (
    "Orbit orange robot, floating robot, black visor mascot, Eiffel Tower, Paris, "
    "photoreal live action, horror, gore, readable UI chrome, watermark, logo overlay, "
    "dialogue, speech, talking, narrator, lip sync, twin characters, clone, "
    "duplicate boy, second explorer"
)

STYLE = (
    "Premium 3D cartoon animated film style, upbeat warm scholarly palette, "
    "rich teal and brown, golden dust motes, shallow depth of field, continuous "
    "camera motion through the final frame. " + CG_SILENT_AUDIO_BLOCK
)

VO_TEXT = (
    "In an old library of discoveries, every shelf holds a question someone once "
    "dared to ask. Our Explorer dusts a forgotten volume, reads a line — and the "
    "idea lights up. Science isn't a straight road. It's curiosity, walking the "
    "stacks, one book at a time."
)

PLATES = [
    {
        "id": "01_library_establish",
        "explorer": False,
        "prompt": (
            f"{STYLE} Wide shot of a grand dusty old library interior, towering "
            "wooden shelves of antique books, warm afternoon light shafts through "
            "tall windows, golden dust in the air, empty aisle inviting the viewer "
            "in. No people. Continuous slow push down the aisle. Story plate only."
        ),
    },
    {
        "id": "02_explorer_dusts_book",
        "explorer": True,
        "prompt": (
            f"{STYLE} {EXPLORER_LOCK} Medium shot: the Explorer walks through the "
            "dusty library aisle, stops at a shelf, carefully pulls out a thick dusty "
            "blue book, gently blows dust off the cover, opens it with curious eyes. "
            "Satchel and compass readable. Continuous motion, single character only."
        ),
    },
    {
        "id": "03_idea_pages",
        "explorer": False,
        "prompt": (
            f"{STYLE} Close cinematic shot of open antique book pages in the library "
            "light; handwritten diagrams and a soft glowing gold stylised atom "
            "diagram rises from the page like a discovery spark. No people. Magical "
            "but scientific wonder. Continuous subtle camera drift."
        ),
    },
    {
        "id": "04_explorer_eureka",
        "explorer": True,
        "prompt": (
            f"{STYLE} {EXPLORER_LOCK} The Explorer looks up thoughtful with finger on "
            "chin, then brightens into a eureka smile, pointing upward as a glowing "
            "gold atom symbol sparkles above his finger; he then steps aside toward "
            "frame edge as the library shelves reclaim the frame. Single character."
        ),
    },
]


def resolve_keys() -> None:
    for p in (
        REPO / "04_Audio" / "tools" / ".env",
        PROJ / "07_Edit-Project" / ".env",
        REPO / ".env",
    ):
        load_dotenv(p)


def gen_plate(client, plate: dict, dest: Path, model: str) -> dict:
    from google.genai import types

    if already_done(dest):
        print(f"  skip existing {dest.name}", flush=True)
        return {"skipped": True, "bytes": dest.stat().st_size}

    img = types.Image.from_file(str(REF)) if plate["explorer"] else None
    config_kwargs = dict(
        number_of_videos=1,
        duration_seconds=8,
        aspect_ratio="16:9",
        resolution="720p",
        negative_prompt=NEGATIVE,
        enhance_prompt=True,
        generate_audio=False,
    )
    if img is not None:
        config_kwargs["reference_images"] = [
            types.VideoGenerationReferenceImage(
                image=img,
                reference_type=types.VideoGenerationReferenceType.ASSET,
            )
        ]
    config = types.GenerateVideosConfig(**config_kwargs)

    print(f"  submit {plate['id']} explorer={plate['explorer']}", flush=True)
    t0 = time.time()
    kwargs = dict(model=model, prompt=plate["prompt"], config=config)
    if img is not None:
        kwargs["image"] = img
    operation = client.models.generate_videos(**kwargs)
    while not operation.done:
        time.sleep(12)
        operation = client.operations.get(operation)
        print(f"  poll {plate['id']} … {int(time.time() - t0)}s", flush=True)
    if operation.error:
        raise RuntimeError(operation.error)
    response = operation.response
    if not response or not response.generated_videos:
        raise RuntimeError(f"no video for {plate['id']}")
    video = response.generated_videos[0]
    dest.parent.mkdir(parents=True, exist_ok=True)
    client.files.download(file=video.video)
    video.video.save(str(dest))
    strip_audio(dest)
    return {"seconds": round(time.time() - t0, 1), "bytes": dest.stat().st_size}


def maybe_vo() -> Path | None:
    token = os.environ.get("ELEVENLABS_API_KEY") or os.environ.get("ELEVEN_API_KEY")
    if not token:
        print("No ELEVENLABS_API_KEY — assembling picture-only.", flush=True)
        return None
    VO_PATH.parent.mkdir(parents=True, exist_ok=True)
    if VO_PATH.exists() and VO_PATH.stat().st_size > 10_000:
        print(f"VO exists {VO_PATH}", flush=True)
        return VO_PATH
    payload = {
        "text": VO_TEXT,
        "model_id": MODEL_ID,
        "voice_settings": VOICE_SETTINGS,
    }
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}",
        data=json.dumps(payload).encode(),
        headers={
            "xi-api-key": token,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=180) as r:
        VO_PATH.write_bytes(r.read())
    print(f"VO saved {VO_PATH} ({VO_PATH.stat().st_size} bytes)", flush=True)
    return VO_PATH


def assemble(clips: list[Path], vo: Path | None) -> None:
    """xfade picture chain; optional VO under (trim/pad to picture length)."""
    n = len(clips)
    if n < 2:
        raise SystemExit("need ≥2 clips")
    inputs: list[str] = []
    for c in clips:
        inputs += ["-i", str(c)]
    if vo:
        inputs += ["-i", str(vo)]

    # trim each to CLIP_USE_S then xfade
    parts = []
    for i in range(n):
        parts.append(
            f"[{i}:v]trim=0:{CLIP_USE_S},setpts=PTS-STARTPTS,scale=1280:720:force_original_aspect_ratio=decrease,"
            f"pad=1280:720:(ow-iw)/2:(oh-ih)/2,fps=24,format=yuv420p[v{i}]"
        )
    vprev = "v0"
    offset = CLIP_USE_S - XFADE
    for i in range(1, n):
        out = f"vx{i}"
        parts.append(
            f"[{vprev}][v{i}]xfade=transition=fade:duration={XFADE}:offset={offset:.3f}[{out}]"
        )
        vprev = out
        offset += CLIP_USE_S - XFADE

    pic_dur = n * CLIP_USE_S - (n - 1) * XFADE
    filter_complex = ";".join(parts)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["ffmpeg", "-y", *inputs, "-filter_complex", filter_complex]
    if vo:
        # map picture + VO (atrim/apad to picture length)
        afilter = (
            f"[{n}:a]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo,"
            f"atrim=0:{pic_dur:.3f},apad=whole_dur={pic_dur:.3f}[a]"
        )
        cmd[-1] = filter_complex + ";" + afilter
        cmd += [
            "-map",
            f"[{vprev}]",
            "-map",
            "[a]",
            "-c:v",
            "libx264",
            "-preset",
            "fast",
            "-crf",
            "18",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-shortest",
            "-movflags",
            "+faststart",
            str(OUT),
        ]
    else:
        cmd += [
            "-map",
            f"[{vprev}]",
            "-an",
            "-c:v",
            "libx264",
            "-preset",
            "fast",
            "-crf",
            "18",
            "-movflags",
            "+faststart",
            str(OUT),
        ]
    print("ffmpeg assemble…", flush=True)
    subprocess.run(cmd, check=True)
    print(f"SAVED {OUT} ({OUT.stat().st_size} bytes) ~{pic_dur:.1f}s", flush=True)


def main() -> None:
    resolve_keys()
    if not (os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")):
        raise SystemExit(
            "Missing GEMINI_API_KEY. Add it to the cloud environment secrets, then re-run."
        )
    if not REF.exists():
        raise SystemExit(f"Missing Explorer ref: {REF}")

    model = os.environ.get("ORBIT_VEO_MODEL", DEFAULT_MODEL)
    client = make_client()
    meta = {"model": model, "plates": []}
    paths: list[Path] = []
    RAW.mkdir(parents=True, exist_ok=True)

    for plate in PLATES:
        dest = RAW / f"{plate['id']}_v01.mp4"
        info = gen_plate(client, plate, dest, model)
        meta["plates"].append({"id": plate["id"], **info, "path": str(dest)})
        paths.append(dest)

    vo = maybe_vo()
    assemble(paths, vo)
    meta["out"] = str(OUT)
    meta["vo"] = str(vo) if vo else None
    META_PATH.write_text(json.dumps(meta, indent=2))
    print(json.dumps(meta, indent=2))


if __name__ == "__main__":
    main()
