#!/usr/bin/env python3
"""Part 04 v04 stills — boil steam-from-tip + address single swan-neck.

Attaches the locked plate-01 flask as geometry. Gemini Flash Image via REST.
"""
from __future__ import annotations

import base64
import json
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))

from orbit_gemini_veo import load_dotenv, resolve_api_key  # noqa: E402

PROJ = Path(__file__).resolve().parents[1]
REFS = PROJ / "04_Generated-Clips/part04/refs"
FLASK_LOCK = REFS / "01_question_mark_flask_v03.jpg"
BOIL_SCENE = REFS / "02_boil_broth_v03.jpg"
ADDR_SCENE = REFS / "10_an_address_v02.jpg"
MODEL = "gemini-2.5-flash-image"
API = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    f"{MODEL}:generateContent"
)
STYLE = (
    "Premium Animistry-class 3D cartoon matching the attached flask photo. "
    "Warm 1860s laboratory. NOT photoreal. NOT live-action. NOT modern. "
    "Silent still. No readable text, no logos, no UI, no numbers."
)
FLASK_GEO = (
    "HARD LOCK flask geometry from Image 1: EXACTLY ONE neck. "
    "Onion-round bulb. The top of the bulb is CLOSED — it tapers into that "
    "single long thin S-curve question-mark swan neck. "
    "The ONLY opening is the far tip of the S-curve. "
    "NO second vertical chimney. NO open-top Florence flask. "
    "NO extra tube branching off the shoulder. NO pedestal foot."
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


def gen_still(key: str, dest: Path, refs: list[Path], prompt: str) -> None:
    parts: list[dict] = []
    for p in refs:
        mime, b64 = b64_file(p)
        parts.append({"inline_data": {"mime_type": mime, "data": b64}})
    parts.append({"text": prompt})
    body = json.dumps({
        "contents": [{"role": "user", "parts": parts}],
        "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]},
    }).encode()
    print(f"  still gen {dest.name}", flush=True)
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
    raise RuntimeError(f"no still for {dest.name}: {json.dumps(payload)[:400]}")


def main() -> None:
    load_dotenv(PROJ / "07_Edit-Project" / ".env")
    key = resolve_api_key(PROJ / "07_Edit-Project" / ".env")
    if not FLASK_LOCK.exists():
        raise SystemExit(f"missing flask lock {FLASK_LOCK}")
    jobs = [
        (
            REFS / "02_boil_broth_v04.jpg",
            [FLASK_LOCK, BOIL_SCENE],
            (
                "Image 1 is the LOCKED Pasteur swan-neck flask. Copy that "
                "exact glass geometry. Image 2 is the boil-lab scene to keep "
                "(tripod, flame, oil lamp, books, 1860s shelves). "
                f"{FLASK_GEO} {STYLE} "
                "The flask sits in a metal tripod over a small flame. "
                "Broth is boiling — bubbles stay INSIDE the liquid in the bulb. "
                "A thin white steam wisp is ALREADY leaving ONLY the OPEN TIP "
                "of the S-curve tube on the right. "
                "HARD LOCK: NO steam above the bulb. NO steam leaking through "
                "solid glass. Glass is sealed and airtight. Steam cannot pass "
                "through glass. The tube is intact. 16:9."
            ),
        ),
        (
            REFS / "10_an_address_v04.jpg",
            [FLASK_LOCK, ADDR_SCENE],
            (
                "Image 1 is the LOCKED Pasteur swan-neck flask. Copy that "
                "exact glass geometry. Image 2 is the doorway / theatre scene "
                "to keep (arched door, 1860s lab, theatre beyond). "
                f"{FLASK_GEO} {STYLE} "
                "The locked flask sits FLAT on the wooden bench in the "
                "foreground — onion bulb on wood, no foot. Doorway behind. "
                "Clear still broth. ZERO steam. ZERO germs. "
                "Do NOT invent a second neck. 16:9."
            ),
        ),
    ]
    for dest, refs, prompt in jobs:
        if dest.exists() and dest.stat().st_size > 80_000:
            print(f"  skip {dest.name}", flush=True)
            continue
        missing = [p for p in refs if not p.exists()]
        if missing:
            raise SystemExit(f"missing refs {missing}")
        gen_still(key, dest, refs, prompt)
        if dest.stat().st_size < 80_000:
            raise SystemExit(f"small still {dest}")


if __name__ == "__main__":
    main()
