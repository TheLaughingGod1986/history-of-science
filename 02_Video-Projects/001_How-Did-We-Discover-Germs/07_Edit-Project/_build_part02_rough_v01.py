#!/usr/bin/env python3
"""Part 02 — Seeing the Tiny World. Match Part 01 v08 style lock.

1) Gemini stills → 2) Flow Veo I2V (primary) / API fallback → 3) assemble rough.
Stop for Ben UAT. Do not start Part 03.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from io import BytesIO
from pathlib import Path

from PIL import Image

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
PLATES_JSON = PROJ / "07_Edit-Project" / "parts" / "part-02_plates_v01.json"
REFS = PROJ / "04_Generated-Clips" / "part02" / "refs"
RAW = PROJ / "04_Generated-Clips" / "part02" / "raw" / "v01"
VO = PROJ / "02_Voiceover" / "part02_seeing_tiny_world_v01.mp3"
OUT = PROJ / "09_Final-Export" / "hos_001_part02_rough_v01.mp4"
META = PROJ / "07_Edit-Project" / "part02_gen_meta_v01.json"
ART = Path("/opt/cursor/artifacts")
EXPLORER = REPO / "01_Character" / "01_Master-References" / "hos-explorer-character-sheet-v01.jpg"

CLIP_USE = 8.0
XFADE = 0.40
FPS = 24

STYLE_LOCK = (
    "Match History of Science Part 01 locked look: Premium Animistry-class 3D cartoon, "
    "warm cinematic light, period science world. NOT photoreal. NOT live-action. "
    "NOT modern hospital. Silent picture only."
)
FACELESS = (
    "Any microbes must be FACELESS: rods / spiked spheres / spirals only. "
    "NO eyes, NO mouths, NO smiles, NO winks, NOT cute mascots."
)


def resolve_keys() -> None:
    for p in (REPO / "04_Audio" / "tools" / ".env", PROJ / "07_Edit-Project" / ".env"):
        load_dotenv(p)


def gen_still(client, plate: dict, dest: Path) -> None:
    from google.genai import types

    if dest.exists() and dest.stat().st_size > 80_000:
        print(f"  still skip {dest.name}", flush=True)
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    prompt = f"{plate['prompt']} {STYLE_LOCK} {FACELESS} Still image."
    parts = []
    if plate.get("explorer") and EXPLORER.exists():
        parts.append(types.Part.from_bytes(data=EXPLORER.read_bytes(), mime_type="image/jpeg"))
        prompt = (
            "Image 1 is the Explorer identity lock — match him exactly (teal coat, gold glasses, boy). "
            + prompt
        )
    parts.append(types.Part.from_text(text=prompt))
    print(f"  still gen {plate['id']}", flush=True)
    resp = client.models.generate_content(
        model="gemini-2.5-flash-image",
        contents=[types.Content(role="user", parts=parts)],
        config=types.GenerateContentConfig(response_modalities=["TEXT", "IMAGE"]),
    )
    for cand in resp.candidates or []:
        for part in cand.content.parts if cand.content else []:
            inline = getattr(part, "inline_data", None)
            if inline and inline.data:
                Image.open(BytesIO(inline.data)).convert("RGB").save(dest, quality=95)
                print(f"  saved {dest.name} ({dest.stat().st_size})", flush=True)
                return
    raise RuntimeError(f"no still for {plate['id']}")


def gen_i2v_api(client, model: str, still: Path, prompt: str, dest: Path) -> dict:
    from google.genai import types

    if already_done(dest, min_bytes=400_000):
        print(f"  i2v skip {dest.name}", flush=True)
        return {"skipped": True, "bytes": dest.stat().st_size}
    img = types.Image.from_file(location=str(still))
    config = types.GenerateVideosConfig(
        number_of_videos=1, duration_seconds=8, aspect_ratio="16:9", resolution="720p"
    )
    full = f"{prompt} {STYLE_LOCK} {FACELESS} Continuous motion the whole clip — never freeze."
    last_err = None
    for attempt in range(1, 3):
        try:
            print(f"  i2v {dest.stem} attempt={attempt} model={model}", flush=True)
            t0 = time.time()
            op = client.models.generate_videos(model=model, prompt=full, image=img, config=config)
            while not op.done:
                time.sleep(12)
                op = client.operations.get(op)
                print(f"  poll {dest.stem} {int(time.time()-t0)}s", flush=True)
            if op.error:
                raise RuntimeError(op.error)
            if not op.response or not op.response.generated_videos:
                raise RuntimeError("no video")
            video = op.response.generated_videos[0]
            dest.parent.mkdir(parents=True, exist_ok=True)
            client.files.download(file=video.video)
            video.video.save(str(dest))
            strip_audio(dest)
            return {"seconds": round(time.time() - t0, 1), "bytes": dest.stat().st_size, "engine": "api"}
        except Exception as e:
            last_err = e
            print(f"  FAIL {dest.stem}: {e}", flush=True)
            time.sleep(45 * attempt if "429" in str(e) else 12 * attempt)
    raise RuntimeError(f"{dest.stem} failed: {last_err}")


def still_motion_fallback(still: Path, dest: Path) -> dict:
    """REMOVED — Ben 2026-08-26: still-push is not animation. Never ship this."""
    raise RuntimeError(
        f"Refusing still-motion fallback for {still.name} → {dest.name}. "
        "Part 02 requires real Flow/API Veo I2V (see PART02_LESSONS.md)."
    )


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
            "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(OUT),
        ],
        check=True,
    )
    return pic_dur


def main() -> None:
    resolve_keys()
    plates = json.loads(PLATES_JSON.read_text())["plates"]
    client = make_client()
    model = os.environ.get("ORBIT_VEO_MODEL", DEFAULT_MODEL)
    REFS.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)

    meta = {"part": 2, "model": model, "style_lock": "v08_pass", "plates": []}
    paths: list[Path] = []

    for plate in plates:
        still = REFS / f"{plate['id']}_v01.jpg"
        dest = RAW / f"{plate['id']}_v01.mp4"
        gen_still(client, plate, still)
        try:
            info = gen_i2v_api(client, model, still, plate["prompt"], dest)
        except Exception as e:
            print(f"  API fail → still-motion fallback: {e}", flush=True)
            info = still_motion_fallback(still, dest)
        meta["plates"].append({"id": plate["id"], "still": str(still), **info, "path": str(dest)})
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
            "-movflags", "+faststart", str(ART / "hos_001_part02_rough_v01_demo.mp4"),
        ],
        check=False,
        capture_output=True,
    )
    print(json.dumps(meta, indent=2))
    print(f"SAVED {OUT} ~{pic_dur:.1f}s — STOP for Ben UAT", flush=True)


if __name__ == "__main__":
    main()
