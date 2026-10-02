#!/usr/bin/env python3
"""Repaint the 004 back-catalogue cover scene (desk PR #180 comment 5950838060).

v01 showed the brass shell tearing through the foil and paper, the opposite of GOLD / threw it / BACK.
v02: the same scene (frame, table, lab, Explorer) with the shell rebounding back out towards the viewer,
the gold foil intact with only a small dent, no tear, no paper. Gemini 2.5 Flash Image, the v01 scene as
the reference. Lettering is untouched; `_land_backcat_cover_004_v02.py` stacks it. Media stays out of git.
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))
from orbit_gemini_veo import resolve_api_key  # noqa: E402

ASSETS = HERE / "covers_backcat_v01" / "_assets"
SRC = ASSETS / "hos_004_backcat_scene_v01.jpg"
EXPLORER_REF = REPO / "01_Character/05_Generation-References/hos-explorer-reference-v01.jpg"
MAIN = Path("/Users/benjaminoats/YouTube/History Of Science")
ENV_CANDIDATES = [
    MAIN / "02_Video-Projects/002_How-Did-We-Discover-The-Periodic-Table/07_Edit-Project/.env",
    MAIN / "02_Video-Projects/001_How-Did-We-Discover-Germs/07_Edit-Project/.env",
    MAIN / "02_Video-Projects/003_Invisible-Bones-X-Rays/07_Edit-Project/.env",
]
MODEL = "gemini-2.5-flash-image"
VERTEX_PROJECT = "gen-lang-client-0538779324"
VERTEX_LOCATION = "us-central1"
USD_PER_IMAGE = 0.039
LOG = HERE / "covers_backcat_v02" / "REPAINT_LOG_v02.json"
API = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"

PROMPT = (
    "Image 1 is a finished History of Science cover scene. Image 2 is the Explorer character sheet. "
    "Repaint Image 1 keeping the same composition, camera, warm lab light, dark empty top half, ornate wooden "
    "frame, wooden table, blurred brass lab apparatus behind, and the Explorer exactly as he is (bottom left, "
    "teal coat, round gold glasses, messy brown hair, arms up in surprise, same size and pose). "
    "Change only the action inside the frame: a sheet of thin GOLD FOIL fills the frame, fully INTACT, smooth "
    "and bright, catching the warm light, with only one small shallow dent and a soft ripple ring where it was "
    "struck, in the centre. The same ornate brass shell is REBOUNDING BACK OUT of the foil towards the viewer: "
    "it is in front of the foil, a little apart from it, its pointed nose aimed out of the picture towards the "
    "camera and slightly down-left, clearly flying away from the foil, never touching or entering it. "
    "Curved motion streaks run from the dent outwards along the shell's path, pointing back towards the viewer. "
    "A few small golden sparks at the dent. "
    "NO tear, NO hole, NO ripped paper, NO paper or tissue anywhere, NO fragments or flying scraps. "
    "Premium 3D cartoon, warm cinematic light, NOT photoreal. No text, no letters, no logos. "
    "Exactly one Explorer. No orange robot. Tall 9:16 portrait, same framing as Image 1."
)


def b64(p: Path) -> dict:
    mime = "image/jpeg" if p.suffix.lower() in {".jpg", ".jpeg"} else "image/png"
    return {"inline_data": {"mime_type": mime, "data": base64.b64encode(p.read_bytes()).decode()}}


def api_key() -> str:
    for env in ENV_CANDIDATES:
        if not env.exists():
            continue
        for line in env.read_text().splitlines():
            s = line.strip()
            if s and not s.startswith("#") and "=" in s:
                k, v = s.split("=", 1)
                k, v = k.strip(), v.strip().strip('"').strip("'")
                if k in ("GEMINI_API_KEY", "GOOGLE_API_KEY") and v:
                    os.environ[k] = v
        try:
            key = resolve_api_key(env)
        except SystemExit:
            continue
        if key:
            return key
    raise SystemExit("No non-empty GEMINI_API_KEY found")


def gen_vertex(dest: Path) -> None:
    import google.auth
    from google import genai
    from google.genai import types
    creds, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
    if not creds:
        raise SystemExit("STOP: no ADC")
    c = genai.Client(vertexai=True, project=VERTEX_PROJECT, location=VERTEX_LOCATION)
    parts = [types.Part.from_bytes(data=SRC.read_bytes(), mime_type="image/jpeg"),
             types.Part.from_bytes(data=EXPLORER_REF.read_bytes(), mime_type="image/jpeg"), PROMPT]
    r = c.models.generate_content(
        model=MODEL, contents=parts,
        config=types.GenerateContentConfig(response_modalities=["IMAGE"],
                                           image_config=types.ImageConfig(aspect_ratio="9:16")))
    data = next((p.inline_data.data for cand in r.candidates or []
                 for p in (cand.content.parts if cand.content else []) if p.inline_data and p.inline_data.data), None)
    if not data:
        raise SystemExit("STOP: no image")
    tmp = dest.with_suffix(".bin")
    tmp.write_bytes(data)
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(tmp),
                    "-frames:v", "1", "-q:v", "2", str(dest)], check=True)
    tmp.unlink(missing_ok=True)
    log = json.loads(LOG.read_text()) if LOG.exists() else {
        "task": "desk PR #180 comment 5950838060", "path": "vertex", "project": VERTEX_PROJECT,
        "location": VERTEX_LOCATION, "model": MODEL, "src": SRC.name, "prompt": PROMPT, "takes": []}
    log["takes"].append({"file": dest.name, "sha256": hashlib.sha256(dest.read_bytes()).hexdigest(),
                         "cost_usd": USD_PER_IMAGE})
    log["cost_usd_total"] = round(sum(t["cost_usd"] for t in log["takes"]), 3)
    LOG.write_text(json.dumps(log, indent=2) + "\n")
    print(f"  saved {dest.name} (vertex {VERTEX_PROJECT})", flush=True)


def gen(key: str, dest: Path) -> None:
    body = json.dumps({
        "contents": [{"role": "user", "parts": [b64(SRC), b64(EXPLORER_REF), {"text": PROMPT}]}],
        "generationConfig": {"responseModalities": ["TEXT", "IMAGE"], "imageConfig": {"aspectRatio": "9:16"}},
    }).encode()
    for attempt in range(1, 4):
        req = urllib.request.Request(f"{API}?key={key}", data=body,
                                     headers={"Content-Type": "application/json"}, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                payload = json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            raise SystemExit(f"HTTP {e.code}: {e.read()[:400]!r}") from e
        for cand in payload.get("candidates") or []:
            for part in (cand.get("content") or {}).get("parts") or []:
                inline = part.get("inlineData") or part.get("inline_data")
                if inline and inline.get("data"):
                    tmp = dest.with_suffix(".bin")
                    tmp.write_bytes(base64.b64decode(inline["data"]))
                    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(tmp),
                                    "-frames:v", "1", "-q:v", "2", str(dest)], check=True)
                    tmp.unlink(missing_ok=True)
                    print(f"  saved {dest.name} (try {attempt})", flush=True)
                    return
        print(f"  try {attempt}: text-only response", flush=True)
    raise SystemExit("no image returned")


def main() -> int:
    tag = sys.argv[1] if len(sys.argv) > 1 else "a"
    dest = ASSETS / f"hos_004_backcat_scene_v02{tag}.jpg"
    if "--gemini-api" in sys.argv:
        gen(api_key(), dest)
    else:
        gen_vertex(dest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
