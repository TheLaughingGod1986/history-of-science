#!/usr/bin/env python3
"""Mint Part 02 plate 08 ward v04 via Gemini Veo API only (no Flow).

Locked camera · real acting (nurses / steam / cloth) · 3D cartoon · faceless.
Explorer OFF. No Orbit. No neon overlay. No Ken Burns substitute.

Exits:
  0 — minted mp4
  2 — missing API key
  3 — no credits / 429 RESOURCE_EXHAUSTED
  4 — other Veo failure
"""
from __future__ import annotations

import json
import os
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
STILL = PROJ / "04_Generated-Clips/part02/refs/08_ward_vs_lens_v04.jpg"
OUT = PROJ / "04_Generated-Clips/part02/raw/v04_api/08_ward_vs_lens_v04.mp4"
META = PROJ / "07_Edit-Project/part02_ward_v04_mint_meta.json"
ART = Path("/opt/cursor/artifacts")

PROMPT = (
    "IMAGE-TO-VIDEO from this exact start frame. Premium Animistry-class 3D cartoon. "
    "CAMERA 100% LOCKED — tripod lock. No push-in, no zoom, no dolly, no pan, no orbit, "
    "no Ken Burns, no reframing, no parallax that replaces acting. "
    "Animate ONLY subjects in the frame: Victorian nurses walk mid-stride down the ward "
    "aisle (legs and arms moving, apron cloth sways), steam/haze drifts through sunbeams, "
    "bed quilts and curtain cloth gently move, sparse faceless 3D germs "
    "(rods/spheres/spirals ONLY — no faces, no eyes, no mouths, no smiles) slowly drift. "
    "Brass microscope stays as a physical object in frame. Continuous real subject motion "
    "the whole 8 seconds. Silent picture. "
    "FORBIDDEN: camera push/zoom/orbit/pan; 2D neon overlay; HUD circles; Explorer child; "
    "Orbit orange robot; Omni Flash; Nano Banana; modern hospital; readable text; "
    "photoreal live-action; still-hold with only a slow zoom."
)


def resolve_keys() -> None:
    for p in (
        REPO / "04_Audio" / "tools" / ".env",
        PROJ / "07_Edit-Project" / ".env",
    ):
        load_dotenv(p)


def is_no_credit(err: BaseException) -> bool:
    s = str(err)
    return (
        "429" in s
        or "RESOURCE_EXHAUSTED" in s
        or "quota" in s.lower()
        or "insufficient" in s.lower()
        or "billing" in s.lower()
    )


def gen_i2v(client, model: str) -> dict:
    from google.genai import types

    if already_done(OUT, min_bytes=400_000):
        print(f"skip existing {OUT} ({OUT.stat().st_size})", flush=True)
        return {"skipped": True, "bytes": OUT.stat().st_size, "model": model}

    img = types.Image.from_file(location=str(STILL))
    # lite preview rejects negative_prompt (400)
    config = types.GenerateVideosConfig(
        number_of_videos=1,
        duration_seconds=8,
        aspect_ratio="16:9",
        resolution="720p",
    )
    print(f"submit model={model} still={STILL.name} → {OUT.name}", flush=True)
    t0 = time.time()
    op = client.models.generate_videos(
        model=model, prompt=PROMPT, image=img, config=config
    )
    while not op.done:
        time.sleep(12)
        op = client.operations.get(op)
        print(f"poll {int(time.time() - t0)}s", flush=True)
    if op.error:
        raise RuntimeError(op.error)
    if not op.response or not op.response.generated_videos:
        raise RuntimeError("Veo returned no videos")
    video = op.response.generated_videos[0]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    client.files.download(file=video.video)
    video.video.save(str(OUT))
    strip_audio(OUT)
    if not already_done(OUT, min_bytes=400_000):
        raise RuntimeError(f"download too small: {OUT}")
    return {
        "seconds": round(time.time() - t0, 1),
        "bytes": OUT.stat().st_size,
        "model": model,
        "engine": "gemini-api-veo",
        "still": str(STILL),
        "path": str(OUT),
    }


def main() -> None:
    if not STILL.exists():
        raise SystemExit(f"missing still {STILL}")
    resolve_keys()
    if not (os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")):
        print("STOP: GEMINI_API_KEY / GOOGLE_API_KEY missing — cannot mint.", flush=True)
        print("Do not fake Ken Burns. Do not use Flow on this VM.", flush=True)
        raise SystemExit(2)

    model = os.environ.get("ORBIT_VEO_MODEL", DEFAULT_MODEL)
    print(f"model={model}", flush=True)
    try:
        client = make_client()
        info = gen_i2v(client, model)
    except SystemExit:
        raise
    except Exception as e:
        print(f"Veo failure: {e}", flush=True)
        if is_no_credit(e):
            print(
                "STOP: Veo API no credits / RESOURCE_EXHAUSTED — do not Ken Burns.",
                flush=True,
            )
            raise SystemExit(3)
        raise SystemExit(4) from e

    META.write_text(json.dumps(info, indent=2) + "\n", encoding="utf-8")
    ART.mkdir(parents=True, exist_ok=True)
    art = ART / OUT.name
    art.write_bytes(OUT.read_bytes())
    print(json.dumps(info, indent=2), flush=True)
    print(f"SAVED {OUT}", flush=True)
    print(f"SAVED {art}", flush=True)


if __name__ == "__main__":
    main()
