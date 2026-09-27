#!/usr/bin/env python3
"""HOS 004 Part 03 start-frame stills — Gemini Flash Image.

No Explorer in Part 03. Never name Thomson/Mendeleev in still prompts — describe.
Style-matched to Germs / Part 01 locked look. Media stays out of git.
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

from orbit_gemini_veo import resolve_api_key  # noqa: E402

PROJ = Path(__file__).resolve().parents[1]
GERMS = REPO / "02_Video-Projects/001_How-Did-We-Discover-Germs"
PLATES_JSON = PROJ / "07_Edit-Project/parts/part-03_plates_v02.json"
REFS = PROJ / "04_Generated-Clips/part03/refs/v01_stills"
STYLE_REF = GERMS / "04_Generated-Clips/part01/refs/v08_stills/10_ward_clean.jpg"
EXPLORER_REF = (
    REPO / "01_Character/05_Generation-References/hos-explorer-reference-v01.jpg"
)
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
    "Silent still. No garbled dials or fake text. "
    "never garbled or fake tiles. No ATOMOS, no SEE labels, no logos, no UI chrome. "
    "No Orbit orange robot. Finished materials — not flat placeholders."
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
    p = plate["prompt"]
    for drop in (
        "Continuous place-on-balance motion.",
        "Continuous soft push along the row.",
        "Continuous line-up.",
        "Continuous settle.",
        "Continuous snap-combine.",
        "Continuous split/recombine.",
        "Continuous converge.",
        "Continuous write.",
        "Continuous sort.",
        "Continuous column form.",
        "Continuous leave-gap.",
        "Continuous print-then-fly.",
        "Continuous weigh compare.",
        "Continuous acting then leave.",
        "Continuous nudge-swap.",
        "Continuous confirm.",
        "Continuous soft glow pulse.",
        "Continuous soft push.",
        "Continuous place.",
        "Continuous camera drift.",
        "Continuous tip.",
        "Continuous sink.",
        "Continuous land.",
        "Continuous form.",
        "Continuous meet.",
        "Continuous slide.",
        "Continuous fizz.",
        "Continuous snap.",
        "Continuous push.",
        "Continuous arc.",
        "Continuous place-and-leave.",
        "Continuous wobble.",
        "Continuous fade.",
        "Continuous soft camera drift.",
        "Continuous lift.",
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
    img_n = 0
    if STYLE_REF.exists():
        mime, b64 = b64_file(STYLE_REF)
        parts.append({"inline_data": {"mime_type": mime, "data": b64}})
        img_n += 1
        prompt = (
            f"Image {img_n} is the locked History of Science 3D cartoon style — match "
            "that material and light. This scene is NOT a hospital ward; it is the "
            "Cambridge 1897 cathode-ray tube lab / 1904 plum-pudding atom story world. "
            + prompt
        )
    if plate.get("explorer") and EXPLORER_REF.exists():
        mime, b64 = b64_file(EXPLORER_REF)
        parts.append({"inline_data": {"mime_type": mime, "data": b64}})
        img_n += 1
        prompt = (
            f"Image {img_n} is the locked Explorer character sheet — match him exactly "
            "(teal coat, round gold glasses, messy brown hair, boy). Exactly ONE Explorer. "
            + prompt
        )
    elif not plate.get("explorer"):
        prompt += " No Explorer in this still."
    parts.append({"text": prompt})
    body = json.dumps({
        "contents": [{"role": "user", "parts": parts}],
        "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]},
    }).encode()
    last_payload = None
    for attempt in range(1, 4):
        print(f"  still gen {plate['id']} try={attempt}", flush=True)
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
        last_payload = payload
        for cand in payload.get("candidates") or []:
            for part in (cand.get("content") or {}).get("parts") or []:
                inline = part.get("inlineData") or part.get("inline_data")
                if inline and inline.get("data"):
                    save_image(base64.b64decode(inline["data"]), dest)
                    print(f"  saved {dest.name} ({dest.stat().st_size})", flush=True)
                    return
        print(f"  retry {plate['id']} (text-only response)", flush=True)
    raise RuntimeError(
        f"no still for {plate['id']}: {json.dumps(last_payload)[:500]}"
    )


def main() -> None:
    only = sys.argv[1:]
    key = None
    for env in ENV_CANDIDATES:
        if not env.exists():
            continue
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
        if dest.exists() and dest.stat().st_size >= 80_000 and not only:
            print(f"  skip existing {dest.name}", flush=True)
            continue
        gen_still(key, plate, dest)
        if not dest.exists() or dest.stat().st_size < 80_000:
            raise SystemExit(f"missing/small {dest}")
    print(f"DONE stills → {REFS}", flush=True)


if __name__ == "__main__":
    main()
