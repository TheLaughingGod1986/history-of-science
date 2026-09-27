#!/usr/bin/env python3
"""HOS 004 Part 01 start-frame stills — Gemini Flash Image.

No Explorer. Style-matched to Germs Part 01 locked look.
Media stays out of git (04_Generated-Clips/).
"""
from __future__ import annotations

import base64
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))

from orbit_gemini_veo import load_dotenv, resolve_api_key  # noqa: E402

PROJ = Path(__file__).resolve().parents[1]
GERMS = REPO / "02_Video-Projects/001_How-Did-We-Discover-Germs"
PLATES_JSON = PROJ / "07_Edit-Project/parts/part-01_plates_v02.json"
REFS = PROJ / "04_Generated-Clips/part01/refs/v01_stills"
STYLE_REF = GERMS / "04_Generated-Clips/part01/refs/v08_stills/10_ward_clean.jpg"
# 002 has a live Gemini key; 001/003 placeholders are empty.
ENV_CANDIDATES = [
    REPO / "02_Video-Projects/002_How-Did-We-Discover-The-Periodic-Table/07_Edit-Project/.env",
    GERMS / "07_Edit-Project/.env",
    REPO / "02_Video-Projects/003_Invisible-Bones-X-Rays/07_Edit-Project/.env",
]
MODEL = "gemini-2.5-flash-image"
API = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    f"{MODEL}:generateContent"
)
STYLE = (
    "Match History of Science locked look: Premium Animistry-class 3D cartoon, "
    "warm cinematic light, period science world. NOT photoreal. NOT live-action. "
    "NOT a modern hospital. Silent still. Readable carved letters OK when the beat "
    "needs ATOMOS / element symbols. No logos, no UI chrome. No Orbit orange robot. "
    "No Explorer. No cute atom faces. Finished materials — not flat placeholders."
)


def b64_file(p: Path) -> tuple[str, str]:
    raw = p.read_bytes()
    mime = "image/jpeg" if p.suffix.lower() in {".jpg", ".jpeg"} else "image/png"
    return mime, base64.b64encode(raw).decode()


def save_image(data: bytes, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(".bin")
    tmp.write_bytes(data)
    subprocess.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(tmp), "-frames:v", "1", "-q:v", "2", str(dest),
        ],
        check=True,
    )
    tmp.unlink(missing_ok=True)


def still_prompt(plate: dict) -> str:
    if plate.get("still_prompt"):
        return plate["still_prompt"]
    # Derive a still from the motion prompt: drop continuous-motion verbs.
    p = plate["prompt"]
    for drop in (
        "Continuous chip.", "Continuous turn.", "Continuous resolve.",
        "Continuous slam + light chase.", "Continuous tap + wobble.",
        "Continuous tip.", "Continuous slip + blur.", "Continuous flight.",
        "Continuous stream + one bounce.", "Continuous glow chase.",
        "Continuous flip.", "Continuous pullback.", "Continuous settle.",
        "Continuous micro-move.", "Continuous page turn.",
        "Continuous cutting motion at frame 0.", "Continuous push + slip.",
    ):
        p = p.replace(drop, "")
    return (
        f"Finished 3D cartoon still for this beat (start frame for I2V). "
        f"Hold the key subject mid-action, readable, no freeze-blur. {p}"
    )


def gen_still(key: str, plate: dict, dest: Path) -> None:
    if dest.exists() and dest.stat().st_size > 80_000:
        print(f"  skip {dest.name}", flush=True)
        return
    prompt = f"{still_prompt(plate)} {STYLE}"
    parts: list[dict] = []
    if STYLE_REF.exists():
        mime, b64 = b64_file(STYLE_REF)
        parts.append({"inline_data": {"mime_type": mime, "data": b64}})
        prompt = (
            "Image 1 is the locked History of Science 3D cartoon style — match "
            "that material and light. This scene is NOT a hospital ward; it is "
            "the atom / periodic-table cold-open world in the prompt. " + prompt
        )
    parts.append({"text": prompt})
    body = json.dumps({
        "contents": [{"role": "user", "parts": parts}],
        "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]},
    }).encode()
    print(f"  still gen {plate['id']}", flush=True)
    req = urllib.request.Request(
        f"{API}?key={key}",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            payload = json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        raise SystemExit(f"still HTTP {e.code}: {e.read()[:500]!r}") from e
    for cand in payload.get("candidates") or []:
        for part in (cand.get("content") or {}).get("parts") or []:
            inline = part.get("inlineData") or part.get("inline_data")
            if inline and inline.get("data"):
                save_image(base64.b64decode(inline["data"]), dest)
                print(f"  saved {dest.name} ({dest.stat().st_size})", flush=True)
                return
    raise RuntimeError(f"no still for {plate['id']}: {json.dumps(payload)[:500]}")


def main() -> None:
    only = sys.argv[1:]  # optional plate ids
    key = None
    for env in ENV_CANDIDATES:
        if not env.exists():
            continue
        # Force-load even if empty placeholders already set in environ
        for line in env.read_text().splitlines():
            s = line.strip()
            if not s or s.startswith("#") or "=" not in s:
                continue
            k, v = s.split("=", 1)
            k, v = k.strip(), v.strip().strip('"').strip("'")
            if k in ("GEMINI_API_KEY", "GOOGLE_API_KEY") and v:
                os.environ[k] = v
        try:
            key = resolve_api_key(env)
            if key:
                print(f"key from {env}", flush=True)
                break
        except SystemExit:
            continue
    if not key:
        raise SystemExit("No non-empty GEMINI_API_KEY found")

    plates = json.loads(PLATES_JSON.read_text())["plates"]
    if only:
        plates = [p for p in plates if p["id"] in only]
        if not plates:
            raise SystemExit(f"no plates matched {only}")
    REFS.mkdir(parents=True, exist_ok=True)
    for plate in plates:
        dest = REFS / f"{plate['id']}_v01.jpg"
        gen_still(key, plate, dest)
        if not dest.exists() or dest.stat().st_size < 80_000:
            raise SystemExit(f"missing/small {dest}")


if __name__ == "__main__":
    main()
