#!/usr/bin/env python3
"""HOS 003 X-rays long thumb v04: repaint with Röntgen's 1895 hand radiograph as the hero.

Thumb audit 9 Oct item 8 (live `frP_YrNShsU`: the Explorer fills the right half, the X-ray tube is tiny,
47% near-black; HOS rules 2.2 and 2.3). Job J0100 (Claude). The new thumb is a Test & Compare variant
against the live one; nothing is swapped blind.

  paint [--n N]   Vertex gemini-2.5-flash-image plates -> _assets_v04/
  pick <plate>    copy a plate to Selected/ + 168x94 preview + family sheet vs the live look

Python: ~/.venvs/hos-vertex/bin/python for `paint`. Media stays out of git. Nothing to Studio.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))
from ai_spend_hook import spend as ai_spend  # noqa: E402

ASSETS = HERE / "_assets_v04"
SELECTED = HERE / "Selected"
LOG = HERE / "THUMB_XRAY_V04_LOG.json"
STEM = "hos_003_thumb_long_xrays_hand_v04"
PREVIEW_TOOL = REPO / "00_Brand/Channel-Setup/tools/thumb_preview.py"
STYLE_SHEET = REPO / "00_Brand/Channel-Setup/tools/style_sheet.py"

STYLE_REF = REPO / "00_Brand/Channel-Setup/style/long/002_how_did_we_discover_the_periodic_table.jpg"
LIVE_XRAY = ASSETS / "live_frP_YrNShsU.jpg"
RADIOGRAPH = ASSETS / "rontgen_anna_bertha_hand_1895.jpg"
EXPLORER_REF = REPO / "01_Character/05_Generation-References/hos-explorer-reference-v01.jpg"

PROJECT = "gen-lang-client-0538779324"
LOCATION = "us-central1"
IMAGE_MODEL = "gemini-2.5-flash-image"
USD_PER_STILL = 0.039
GBP_PER_USD = 0.80
MAX_PAINTS = 3

W, H = 1280, 720

PROMPT = (
    "Image 1 is the live History of Science long thumbnail: match its premium 3D cartoon painting, "
    "warm golden library light, bookshelves, green curtain, arched window, and its painted serif "
    "title lettering (cream words, one gold line) with small gold flourishes exactly, and its layout: "
    "title upper left, one giant hero object filling the right two thirds, the Explorer small lower left. "
    "Image 2 is the current X-rays thumbnail: same subject (Würzburg 1895), but do NOT copy its layout; "
    "its Explorer was far too big. Image 3 is Wilhelm Röntgen's real 1895 X-ray of his wife Anna Bertha's "
    "left hand: the hero must be this exact radiograph, same four fingers and thumb, same bones, the dark "
    "ring on the fourth finger, black-and-grey photographic plate. Image 4 is the Explorer: match him "
    "exactly (round thin gold glasses, teal long coat, tan waistcoat, brown bow tie, messy brown hair, "
    "satchel), exactly one Explorer.\n\n"
    "Paint a new 16:9 thumbnail in the same golden library, bright and warm, not dark. Hero object: "
    "the radiograph of Image 3 as a large glass photographic plate in a carved wooden frame, standing "
    "upright on a polished wooden desk, lit from behind by a soft warm-white glow so the bones and the "
    "ring read clearly; soft contact shadow on the desk, gold rim light on the frame. The plate fills "
    "the right two thirds of the frame, from about 36% to 92% of the width, top at about 8% of the "
    "height, bottom resting on the desk at about 84% of the height, fully in frame, upright, not tilted. "
    "The bones are the subject: large, sharp, unmistakably a human hand with a ring. No writing on the "
    "plate. Keep the bottom-right corner of the frame empty desk and shadow only (a duration badge sits "
    "there).\n\n"
    "Upper left: the painted title lettering in the same style as Image 1, three lines: 'HOW DID WE' small "
    "in cream, 'DISCOVER' larger in cream, and 'X-RAYS?' largest in gold, with small gold flourishes "
    "above and below. Spell it exactly HOW DID WE DISCOVER X-RAYS? No other text anywhere in the picture.\n\n"
    "Lower left: the Explorer small, about a third of the frame height, standing beside the desk, "
    "looking up at the glowing hand with wonder. He is a garnish, not the subject.\n\n"
    "HARD REJECT: any text other than the title, writing on the plate, a skeleton or a cartoon hand instead "
    "of the radiograph, more or fewer than five digits, flat shapes, split panels, photoreal people, a "
    "plain dark background, objects cut off by the frame edge, anything in the bottom-right corner, "
    "logos, an orange robot."
)


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load_log() -> dict:
    if LOG.exists():
        return json.loads(LOG.read_text())
    return {"film": "003_Invisible-Bones-X-Rays", "video": "frP_YrNShsU",
            "what": "long thumb v04 repaint (Test & Compare variant)",
            "authority": "thumb audit 9 Oct item 8; job J0100 (Claude)",
            "radiograph_source": "Wikimedia Commons, First_medical_X-ray_by_Wilhelm_Röntgen_of_his_wife_"
                                 "Anna_Bertha_Ludwig's_hand_-_18951222.gif (public domain)",
            "model": IMAGE_MODEL, "path": "vertex", "vertex_project": PROJECT,
            "prompt": PROMPT, "paints": [], "picked": []}


def save_log(log: dict) -> None:
    log["cost_usd_total"] = round(sum(p["cost_usd"] for p in log["paints"]), 3)
    LOG.write_text(json.dumps(log, indent=2, ensure_ascii=False) + "\n")


def paint(n: int) -> None:
    import google.auth
    from google import genai
    from google.genai import types

    log = load_log()
    if len(log["paints"]) + n > MAX_PAINTS:
        raise SystemExit(f"STOP: {len(log['paints'])} paints already; cap is {MAX_PAINTS}")
    creds, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
    if not creds:
        raise SystemExit("STOP: no ADC")
    c = genai.Client(vertexai=True, project=PROJECT, location=LOCATION)
    parts = [types.Part.from_bytes(data=p.read_bytes(), mime_type="image/jpeg")
             for p in (STYLE_REF, LIVE_XRAY, RADIOGRAPH, EXPLORER_REF)] + [PROMPT]
    ASSETS.mkdir(parents=True, exist_ok=True)
    for _ in range(n):
        k = len(log["paints"]) + 1
        dest = ASSETS / f"{STEM}_plate{k:02d}.jpg"
        print(f"PAINT {k} model={IMAGE_MODEL} path=vertex", flush=True)
        r = c.models.generate_content(
            model=IMAGE_MODEL, contents=parts,
            config=types.GenerateContentConfig(response_modalities=["IMAGE"],
                                               image_config=types.ImageConfig(aspect_ratio="16:9")))
        data = None
        for cand in r.candidates or []:
            for part in (cand.content.parts if cand.content else []) or []:
                if part.inline_data and part.inline_data.data:
                    data = part.inline_data.data
        log["paints"].append({"k": k, "file": dest.name if data else None,
                              "cost_usd": USD_PER_STILL, "at": now()})
        save_log(log)
        ai_spend("vertex", round(USD_PER_STILL * GBP_PER_USD, 3), "HOS:003",
                 f"X-rays thumb v04 plate {k:02d} ({IMAGE_MODEL}), J0100", by="cursor")
        if not data:
            print(f"  no image for paint {k}", flush=True)
            continue
        tmp = dest.with_suffix(".bin")
        tmp.write_bytes(data)
        subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(tmp),
                        "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}",
                        "-frames:v", "1", "-q:v", "2", str(dest)], check=True)
        tmp.unlink(missing_ok=True)
        print(f"SAVED {dest}", flush=True)


def pick(plate: Path) -> None:
    SELECTED.mkdir(parents=True, exist_ok=True)
    jpg = SELECTED / f"{STEM}.jpg"
    shutil.copyfile(plate, jpg)
    preview = SELECTED / f"{STEM}_preview.jpg"
    subprocess.run([sys.executable, str(PREVIEW_TOOL), "long", str(jpg), "--out", str(preview)], check=True)
    family = SELECTED / "hos_003_thumb_v04_family_vs_live.jpg"
    subprocess.run([sys.executable, str(STYLE_SHEET), "long", str(jpg), "--out", str(family)], check=False)
    log = load_log()
    log["picked"].append({"plate": plate.name, "out": jpg.name, "at": now()})
    save_log(log)
    print(f"SAVED {jpg}\nPREVIEW {preview}\nFAMILY {family}", flush=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("paint")
    p.add_argument("--n", type=int, default=2)
    q = sub.add_parser("pick")
    q.add_argument("plate", type=Path)
    a = ap.parse_args()
    if a.cmd == "paint":
        paint(a.n)
    else:
        pick(a.plate)


if __name__ == "__main__":
    main()
