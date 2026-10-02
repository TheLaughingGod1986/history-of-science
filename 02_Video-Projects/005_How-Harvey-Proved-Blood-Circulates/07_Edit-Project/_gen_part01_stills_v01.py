#!/usr/bin/env python3
"""HOS 005 Part 01 start-frame stills (Gemini Flash Image), one per plate.

Start frames for Flow Veo 3.1 image-to-video, so the sums and Harvey's face can
be checked by hand before any Flow spend. Media stays out of git.

  python3 07_Edit-Project/_gen_part01_stills_v01.py [plate_id …]
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

PROJ = Path(__file__).resolve().parents[1]
REPO = PROJ.parents[1]
LIVE = Path("/Users/benjaminoats/YouTube/History Of Science")
PART = os.environ.get("HOS_PART", "01")
PLATES_JSON = PROJ / f"07_Edit-Project/parts/part-{PART}_plates_v02.json"
REFS = PROJ / f"04_Generated-Clips/part{PART}/refs/v01_stills"
STYLE_REF = REPO / "02_Video-Projects/001_How-Did-We-Discover-Germs/04_Generated-Clips/part01/refs/v08_stills/10_ward_clean.jpg"
EXPLORER_REF = REPO / "01_Character/05_Generation-References/hos-explorer-reference-v01.jpg"
ENV_CANDIDATES = [
    base / "02_Video-Projects/002_How-Did-We-Discover-The-Periodic-Table/07_Edit-Project/.env"
    for base in (REPO, LIVE)
]
MODEL = "gemini-2.5-flash-image"
API = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"
STYLE = (
    "Match the History of Science locked look: premium Animistry-class 3D cartoon, warm "
    "cinematic candlelight, 17th-century world. NOT photoreal. 16:9 frame. No logos, no UI, "
    "no captions, no signs. No Orbit orange robot. Finished materials, not flat placeholders. "
    "Wonder, not gore: no wounds, no blood on skin, no cut flesh, no animal organs."
)


def api_key() -> str:
    for env in ENV_CANDIDATES:
        if not env.exists():
            continue
        for line in env.read_text().splitlines():
            s = line.strip()
            if s.startswith(("GEMINI_API_KEY=", "GOOGLE_API_KEY=")):
                v = s.split("=", 1)[1].strip().strip('"').strip("'")
                if v:
                    return v
    raise SystemExit("STOP: no GEMINI_API_KEY in the Mini env files")


def b64_file(p: Path) -> tuple[str, str]:
    mime = "image/jpeg" if p.suffix.lower() in {".jpg", ".jpeg"} else "image/png"
    return mime, base64.b64encode(p.read_bytes()).decode()


def save_image(data: bytes, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(".bin")
    tmp.write_bytes(data)
    subprocess.run(
        ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(tmp),
         "-vf", "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080",
         "-frames:v", "1", "-q:v", "2", str(dest)],
        check=True,
    )
    tmp.unlink(missing_ok=True)


def still_prompt(plate: dict) -> str:
    p = plate.get("still_prompt") or plate["prompt"]
    for drop in ("Silent.", "Continuous motion through the final frame.", "Premium Animistry-class 3D cartoon."):
        p = p.replace(drop, "")
    return (
        "Finished 3D cartoon still, the first frame of this moving shot, key subject "
        f"mid-action and readable, no motion blur. {p.strip()}"
    )


def gen_still(key: str, plate: dict, dest: Path) -> None:
    parts: list[dict] = []
    lead = ""
    n = 0
    if STYLE_REF.exists():
        mime, b64 = b64_file(STYLE_REF)
        parts.append({"inline_data": {"mime_type": mime, "data": b64}})
        n += 1
        lead += (
            f"Image {n} shows the locked channel style only: match its 3D cartoon material, "
            "finish and warm light. Do NOT copy its room, people or objects. "
        )
    if plate.get("explorer") and EXPLORER_REF.exists():
        mime, b64 = b64_file(EXPLORER_REF)
        parts.append({"inline_data": {"mime_type": mime, "data": b64}})
        n += 1
        lead += f"Image {n} is the Explorer character sheet: match him exactly, exactly one Explorer. "
    tail = "" if plate.get("explorer") else " No boy explorer character in this image."
    parts.append({"text": f"{lead}{still_prompt(plate)} {STYLE}{tail}"})
    body = json.dumps({
        "contents": [{"role": "user", "parts": parts}],
        "generationConfig": {"responseModalities": ["TEXT", "IMAGE"], "imageConfig": {"aspectRatio": "16:9"}},
    }).encode()
    for attempt in range(1, 4):
        print(f"  still {plate['id']} try={attempt}", flush=True)
        req = urllib.request.Request(f"{API}?key={key}", data=body,
                                     headers={"Content-Type": "application/json"}, method="POST")
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
    raise RuntimeError(f"no still for {plate['id']}")


def main() -> None:
    only = set(sys.argv[1:])
    key = api_key()
    plates = json.loads(PLATES_JSON.read_text())["plates"]
    if only:
        plates = [p for p in plates if p["id"] in only]
    REFS.mkdir(parents=True, exist_ok=True)
    for plate in plates:
        dest = REFS / f"{plate['id']}_v01.jpg"
        if dest.exists() and dest.stat().st_size > 20_000 and not only:
            print(f"  skip {dest.name}", flush=True)
            continue
        gen_still(key, plate, dest)
    print(f"DONE → {REFS}", flush=True)


if __name__ == "__main__":
    main()
