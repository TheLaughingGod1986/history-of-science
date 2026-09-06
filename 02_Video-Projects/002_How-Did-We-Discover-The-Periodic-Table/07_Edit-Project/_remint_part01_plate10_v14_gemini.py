#!/usr/bin/env python3
"""Remint Part 01 plate 10 via Gemini Veo API (I2V).

UAT FAIL on v13: blue rectangular scrub/mask around ore (~69–76s).
Also must keep colourless shimmer under grate (no orange/fire/embers).

KEEP: ore IN brass pan · no flask beside scale · Animistry 3D cartoon · continuous motion.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))
import orbit_gemini_veo as veo  # noqa: E402

PROJ = Path(__file__).resolve().parents[1]
RAW = PROJ / "04_Generated-Clips/part01/raw/v01_fast"
DEST = RAW / "10_rock_not_fire_v01.mp4"
REJECT = PROJ / "04_Generated-Clips/part01/_rejected_uat_v14_plate10"
START = PROJ / "07_Edit-Project/_qa_v14_plate10_prep/p10_start_v14_norange.jpg"
META = PROJ / "07_Edit-Project/part01_remint_plate10_v14_meta.json"
ENV = PROJ / "07_Edit-Project/.env"

# Prefer Fast if prepaid allows; fall back to lite.
MODELS = [
    os.environ.get("ORBIT_VEO_MODEL", "").strip() or "veo-3.1-fast-generate-preview",
    "veo-3.1-lite-generate-preview",
    "veo-3.0-generate-001",
]

PROMPT = (
    "IMAGE-TO-VIDEO of the attached start frame. Keep THIS exact workshop composition and camera. "
    "History of Science locked look: premium Animistry-class 3D cartoon workshop, warm cinematic light. "
    "Not photoreal. Silent. No readable text. No Orbit robot. No Explorer. "
    "Continuous gentle camera drift the whole clip — never a still freeze, never Ken Burns still-push. "
    "ONE continuous wide shot. "
    "LEFT: dark rough ore chunk on a COLD metal grate. ONLY a subtle colourless heat shimmer / "
    "air refraction haze rises through the grate — NO orange, NO red, NO yellow glow, NO embers, "
    "NO coals, NO flames, NO fire, NO burning, NO fire plumes, NO orange wisps. Under the grate: "
    "dark cool metal shadow with colourless shimmer only. "
    "CRITICAL: NO blue rectangle, NO cyan scrub, NO selection mask, NO UI overlay, NO blue tint box, "
    "NO rectangular artifact around the ore or grate. Clean natural pixels only. "
    "RIGHT: classic brass balance scale. LEFT hanging pan holds heavy dark ore sitting FLAT "
    "INSIDE the pan metal — ore on the pan floor, pan clearly depressed, chains taut. RIGHT pan empty. "
    "Table around the scale EMPTY of glassware — ZERO clear glass flasks beside the scale. "
    "Background shelves: prefer OPAQUE ceramic jars and sealed metal canisters; minimise clear glass. "
    "HARD REJECT: blue/cyan mask or scrub around ore, orange/red fire or ember glow under the grate, "
    "clear flask beside the scale, floating ore, hanging pots, split-screen, text, Orbit, Ken Burns."
)

NEG = (
    "blue rectangle, cyan scrub, selection mask, UI overlay, blue tint box, rectangular artifact, "
    "orange fire, embers, coals, flames, glowing coals under grate, clear glass flask beside scale, "
    "Orbit robot, Explorer character, readable text, Ken Burns still zoom, freeze frame, photoreal"
)


def probe(path: Path) -> float:
    return float(
        subprocess.check_output(
            [
                "ffprobe", "-v", "error", "-show_entries", "format=duration",
                "-of", "default=nw=1:nk=1", str(path),
            ],
            text=True,
        ).strip()
    )


def generate(client, model: str, dest: Path) -> dict:
    from google.genai import types

    config = types.GenerateVideosConfig(
        number_of_videos=1,
        duration_seconds=8,
        aspect_ratio="16:9",
        resolution="720p",
        negative_prompt=NEG,
    )
    kwargs = {"model": model, "prompt": PROMPT, "config": config}
    if START.exists():
        kwargs["image"] = types.Image.from_file(location=str(START))
        print(f"  I2V start={START.name}", flush=True)
    else:
        print("  T2V (no start frame)", flush=True)
    t0 = time.time()
    print(f"  submit model={model} → {dest.name}", flush=True)
    op = client.models.generate_videos(**kwargs)
    while not op.done:
        time.sleep(12)
        op = client.operations.get(op)
        print(f"  poll … {int(time.time() - t0)}s", flush=True)
    if getattr(op, "error", None):
        raise RuntimeError(op.error)
    resp = getattr(op, "response", None) or getattr(op, "result", None)
    videos = getattr(resp, "generated_videos", None) if resp else None
    if not videos:
        raise RuntimeError(f"no videos: {resp!r}")
    video = videos[0]
    dest.parent.mkdir(parents=True, exist_ok=True)
    client.files.download(file=video.video)
    video.video.save(str(dest))
    veo.strip_audio(dest)
    return {"seconds": round(time.time() - t0, 1), "bytes": dest.stat().st_size, "model": model}


def main() -> None:
    if not START.exists():
        raise SystemExit(f"STOP: missing start {START}")
    REJECT.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)

    for k in ("GEMINI_API_KEY", "GOOGLE_API_KEY"):
        if not os.environ.get(k):
            os.environ.pop(k, None)
    client = veo.make_client(ENV)

    tmp = REJECT / "10_rock_not_fire_v14_gemini_new.mp4"
    if tmp.exists():
        tmp.unlink()

    last_err: Exception | None = None
    info: dict | None = None
    for model in MODELS:
        print(f"\n=== try {model} ===", flush=True)
        try:
            info = generate(client, model, tmp)
            last_err = None
            break
        except Exception as e:
            last_err = e
            print(f"FAIL {model}: {e}", flush=True)
            if tmp.exists():
                tmp.unlink()

    if last_err is not None or info is None or not tmp.exists():
        raise SystemExit(f"STOP: all Gemini models failed: {last_err}")

    d = probe(tmp)
    if d < 5.5 or tmp.stat().st_size < 400_000:
        raise SystemExit(f"STOP: bad clip d={d} bytes={tmp.stat().st_size}")

    if DEST.exists():
        prev = REJECT / "10_rock_not_fire_v01_prev_from_v13.mp4"
        if prev.exists():
            prev.unlink()
        shutil.move(str(DEST), str(prev))
        print(f"archived previous → {prev.name}", flush=True)
    shutil.move(str(tmp), str(DEST))

    meta = {
        "engine": "gemini-api-veo",
        "mode": "i2v-v14-plate10",
        "start": str(START),
        "out": str(DEST),
        "duration": d,
        **info,
        "updated": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }
    META.write_text(json.dumps(meta, indent=2) + "\n")
    print(f"SAVED {DEST} bytes={DEST.stat().st_size} dur={d:.2f}s", flush=True)
    print(f"META {META}", flush=True)
    print("OK plate10 v14 gemini remint finished", flush=True)


if __name__ == "__main__":
    main()
