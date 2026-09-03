#!/usr/bin/env python3
"""Part 01 start-frame stills — Gemini Flash Image. No Pillow."""
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
PLATES_JSON = PROJ / "07_Edit-Project/parts/part-01_plates_v01.json"
REFS = PROJ / "04_Generated-Clips/part01/refs/v01_stills"
EXPLORER = REPO / "01_Character/01_Master-References/hos-explorer-character-sheet-v01.jpg"
STYLE_REF = GERMS / "04_Generated-Clips/part01/refs/v08_stills/10_ward_clean.jpg"
MODEL = "gemini-2.5-flash-image"
API = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    f"{MODEL}:generateContent"
)
STYLE = (
    "Match History of Science Part 01 locked look: Premium Animistry-class 3D cartoon, "
    "warm cinematic light, period science world. NOT photoreal. NOT live-action. "
    "NOT a modern lab. Silent still. No readable text, no logos, no UI. "
    "No Orbit orange robot. No cute atom faces."
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


def gen_still(key: str, plate: dict, dest: Path) -> None:
    if dest.exists() and dest.stat().st_size > 80_000:
        print(f"  skip {dest.name}", flush=True)
        return
    prompt = f"{plate['still_prompt']} {STYLE}"
    parts: list[dict] = []
    if STYLE_REF.exists():
        mime, b64 = b64_file(STYLE_REF)
        parts.append({"inline_data": {"mime_type": mime, "data": b64}})
        prompt = (
            "Image 1 is the locked History of Science 3D cartoon style — match "
            "that material and light, but this scene is a period chemistry workshop "
            "or hall, not a hospital ward. " + prompt
        )
        img_n = 2
    else:
        img_n = 1
    if plate.get("explorer") and EXPLORER.exists():
        mime, b64 = b64_file(EXPLORER)
        parts.append({"inline_data": {"mime_type": mime, "data": b64}})
        prompt = (
            f"Image {img_n} is the Explorer identity lock — match him exactly "
            "(messy brown hair, round gold glasses, teal coat, tan vest, "
            "brown bow tie, boy). Exactly one Explorer. " + prompt
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
        raise SystemExit(f"still HTTP {e.code}: {e.read()[:400]!r}") from e
    for cand in payload.get("candidates") or []:
        for part in (cand.get("content") or {}).get("parts") or []:
            inline = part.get("inlineData") or part.get("inline_data")
            if inline and inline.get("data"):
                save_image(base64.b64decode(inline["data"]), dest)
                print(f"  saved {dest.name} ({dest.stat().st_size})", flush=True)
                return
    raise RuntimeError(f"no still for {plate['id']}: {json.dumps(payload)[:400]}")


def main() -> None:
    for k in ("GEMINI_API_KEY", "GOOGLE_API_KEY"):
        if not os.environ.get(k):
            os.environ.pop(k, None)
    load_dotenv(GERMS / "07_Edit-Project" / ".env")
    key = resolve_api_key(GERMS / "07_Edit-Project" / ".env")
    plates = json.loads(PLATES_JSON.read_text())["plates"]
    REFS.mkdir(parents=True, exist_ok=True)
    for plate in plates:
        dest = REFS / f"{plate['id']}_v01.jpg"
        gen_still(key, plate, dest)
        if not dest.exists() or dest.stat().st_size < 80_000:
            raise SystemExit(f"missing/small {dest}")


if __name__ == "__main__":
    main()
