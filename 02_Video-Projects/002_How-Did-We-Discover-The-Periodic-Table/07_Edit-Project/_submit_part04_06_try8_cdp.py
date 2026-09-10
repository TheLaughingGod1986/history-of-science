#!/usr/bin/env python3
"""Dedicated 06_explorer_leaves_gap try8 — on-model Explorer remint (Ben UAT).

Ben UAT on rough v22: Explorer inconsistent with Parts 01 / Germs / film lock;
music dies mid-cut (separate assemble fix). try3 KEEP was OTS toy-scale —
face/glasses N/A — that fails continuity with Germs + P01 + P03 keep DNA.

NEW DNA try8 (OTS toy-scale BANNED for this remint):
- On-model Explorer matching Germs lock / character sheet / P03 keep:
  messy chestnut hair, round gold glasses VISIBLE, teal trenchcoat, mustard vest,
  brown bow tie, satchel+compass when readable, human hands (not C-clamp/Playmobil).
- 1869 card-desk EMPTY SEATS beat (NOT ore/gas workshop, NOT lecture-hall ruler).
- Soft glowing vacant seat/gap OK; no lava / flask desk-light invent / practical lamp.

Paint banned. Max 2 Fast starts (A=p03 face DNA, B=germs standing DNA) then STOP.
Auth: Mini CDP benoats@googlemail.com ULTRA.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))
import orbit_flow_veo_ui as flow

flow.FLOW_HOME = os.environ.get("ORBIT_FLOW_HOME", "https://flow.google.com/")
CDP = os.environ.get("ORBIT_FLOW_CDP", "http://127.0.0.1:9222")
PROJ = Path(__file__).resolve().parents[1]
REF = PROJ / "04_Generated-Clips/part04/refs/v20_start_frames"
START = REF / "06_explorer_leaves_gap_start_v20.jpg"
LOCK_A = REF / "06_explorer_leaves_gap_start_v20_try8_onmodel_p03face.jpg"
LOCK_B = REF / "06_explorer_leaves_gap_start_v20_try8B_onmodel_germs.jpg"
QA_DIR = PROJ / "07_Edit-Project/_qa_part04_v20_plates_try8_06"
START_COUNTER = QA_DIR / "start_counter.json"
OUT_A = PROJ / "07_Edit-Project/_qa_part04_v20_flow/submit_06_explorer_leaves_gap_try8.json"
OUT_B = PROJ / "07_Edit-Project/_qa_part04_v20_flow/submit_06_explorer_leaves_gap_try8B.json"
MODEL = os.environ.get("ORBIT_FLOW_VEO_MODEL") or "Veo 3.1 - Fast"
REQUIRED_EMAIL = "benoats@googlemail.com"
MAX_STARTS = 2
PLATE_LIBRARY = "4b8ed25"

PROMPT_COMMON = (
    "IMAGE-TO-VIDEO of the attached start frame. Animate THIS exact beat only. "
    "Plate 06_explorer_leaves_gap try8 — EMPTY SEATS garnish with ON-MODEL Explorer "
    "(Ben UAT: match Germs Part 01 lock + character sheet + Part 03 keep — "
    "NOT the Playmobil/OTS toy cousin from try1–try7). "
    "ONE finished Explorer: messy wavy chestnut-brown hair covering the full crown, "
    "round gold wire-rim glasses CLEARLY VISIBLE on the face, large expressive eyes, "
    "dark teal trenchcoat, mustard/tan vest, brown bow tie, white shirt, "
    "brown leather satchel with brass compass when the angle allows, "
    "human articulated hands (fingers — NOT C-clamp mitts, NOT LEGO/Playmobil). "
    "Camera: three-quarter FRONT / slight profile so glasses + face stay readable "
    "for most of the 8s — garnish scale in a WIDE desk shot (Explorer under ~25% frame height). "
    "HARD REJECT: locked back/OTS with no face for the whole take; toy figurine proportions; "
    "bald crown; hat/helmet; academic blazer; Orbit robot; twins. "
    "SCENE LOCK (HARD): 1869 chemist CARD DESK — warm honey wood desktop, cream written cards "
    "in stacks, bookcase behind OK. Explorer pins one cream card, then takes a small step "
    "BACK leaving a soft glowing vacant seat / gap in the card row — soft warm gap glow only "
    "(NOT chair fire, NOT lava, NOT molten bead). "
    "HARD REJECT ore/gas workshop (no balance scale, no volcanic rock in hands, no blue crystal jar). "
    "HARD REJECT lecture-hall / shared-ruler floor glow / pews. "
    "CLEAN LIGHT: daytime WINDOW spill and/or soft OFF-WORLD bounce ONLY. "
    "THERE IS NO PRACTICAL TABLE LAMP — zero shade, zero bulb, zero shade-cup, zero brass desk lamp. "
    "FLASK liquids stay DULL / MATTE / translucent tea-amber — NEVER self-emissive / molten / "
    "desk-lighting invent. Sparse readable marks on a few cards OK; ZERO unfinished blank flats. "
    "Continuous real Veo motion. Locked tripod. Finished cinematic stylised 3D (Animistry-class). "
    f"Silent. Paint banned. Plate-library lock {PLATE_LIBRARY}. "
)

PROMPT_A = (
    PROMPT_COMMON
    + "Start DNA A: on-model face from Part 03 keep Explorer — RELOCATE into the 1869 card desk "
    "EMPTY SEATS beat above. Do NOT keep the lecture-hall floor ruler glow as the hero."
)
PROMPT_B = (
    PROMPT_COMMON
    + "Start DNA B: on-model Germs Part 01 Explorer standing lock — RELOCATE into the 1869 card desk "
    "EMPTY SEATS beat above. Do NOT keep the ward hallway / checkered floor."
)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bump_start_counter(which: str) -> int:
    QA_DIR.mkdir(parents=True, exist_ok=True)
    n = 0
    if START_COUNTER.exists():
        try:
            n = int(json.loads(START_COUNTER.read_text()).get("starts", 0))
        except Exception:
            n = 0
    n += 1
    START_COUNTER.write_text(
        json.dumps(
            {
                "plate": "06_explorer_leaves_gap",
                "try": 8,
                "which": which,
                "starts": n,
                "max_starts": MAX_STARTS,
                "when": time.strftime("%Y-%m-%dT%H:%M:%S"),
            },
            indent=2,
        )
        + "\n"
    )
    if n > MAX_STARTS:
        raise SystemExit(
            f"STOP_TO_COS: try8 already used {n - 1}/{MAX_STARTS} Flow starts — do not mint further"
        )
    print(f"start_counter={n}/{MAX_STARTS} which={which}", flush=True)
    return n


def assert_auth(page) -> dict:
    html = page.content()
    try:
        body = page.inner_text("body")
    except Exception:
        body = ""
    blob = (html + "\n" + body).lower()
    if any(
        x in blob
        for x in (
            "passkey",
            "verifying it's you",
            "verifying it’s you",
            "use your passkey",
        )
    ):
        raise SystemExit("STOP_TO_COS BLOCKED_AUTH: passkey wall")
    if REQUIRED_EMAIL.lower() not in blob and "googlemail.com" not in blob:
        print("WARN: email not visible in DOM yet; continuing if ULTRA present", flush=True)
    if "ultra" not in blob:
        for sel in (
            '[aria-label*="Account details"]',
            '[aria-label*="Google Account"]',
            "text=ULTRA",
        ):
            try:
                page.locator(sel).first.click(timeout=1200)
                time.sleep(1)
                blob = (page.content() + "\n" + page.inner_text("body")).lower()
                break
            except Exception:
                pass
    if "ultra" not in blob:
        raise SystemExit("STOP_TO_COS BLOCKED_AUTH: ULTRA badge missing")
    return {"ultra": True, "email_hint": REQUIRED_EMAIL.lower() in blob}


def submit_one(page, *, which: str, lock: Path, prompt: str, out_path: Path) -> dict:
    if not lock.exists():
        raise SystemExit(f"ABORT: missing lock {lock}")
    START.write_bytes(lock.read_bytes())
    if sha(START) != sha(lock):
        raise SystemExit(f"ABORT: active start != {lock.name}")

    for need in (
        "ON-MODEL",
        "glasses",
        "1869",
        "EMPTY SEATS",
        "Playmobil",
        "ore/gas",
        "shade-cup",
        "4b8ed25",
        "DULL / MATTE",
    ):
        if need.lower() not in prompt.lower():
            raise SystemExit(f"ABORT: prompt missing {need}")

    start_n = bump_start_counter(which)
    tmp = Path(f"/tmp/hos_v20_06_try8_{which}_stub.mp4")
    if tmp.exists():
        tmp.unlink()
    info: dict = {}
    try:
        info = flow.generate_clip(
            page,
            prompt,
            tmp,
            model=MODEL,
            start_frame=START,
            timeout_s=70,
            attempts=1,
            scenery_only=True,
        )
    except Exception as e:
        info = {
            "error": str(e),
            "project_url": getattr(page, "_orbit_flow_project_url", None) or (page.url or ""),
        }
        print(f"submit note ({which}): {e}", flush=True)

    project_url = (
        info.get("project_url")
        or info.get("url")
        or getattr(page, "_orbit_flow_project_url", None)
        or page.url
        or ""
    )
    project_url = str(project_url).split("?")[0].rstrip("/")
    out = {
        "plate": "06_explorer_leaves_gap",
        "try": 8,
        "which": which,
        "start_n": start_n,
        "max_starts": MAX_STARTS,
        "project_url": project_url,
        "info": {k: v for k, v in info.items() if k != "path"},
        "start": str(START),
        "start_lock": str(lock),
        "start_sha256": sha(lock),
        "start_dna": (
            "try8 on-model face-visible Explorer (Germs/P01/P03 DNA) at 1869 card desk; "
            "OTS toy-scale try1–7 BANNED; CLEAN window/off-world; plate-library 4b8ed25"
        ),
        "plate_library_lock_sha": PLATE_LIBRARY,
        "model": MODEL,
        "when": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "paint": "banned",
        "assemble": False,
        "parent_try3_reject_reason": (
            "Ben UAT: Explorer inconsistent with film lock / Germs / Part 01 "
            "(try3 OTS toy-scale, glasses N/A)"
        ),
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2), flush=True)
    if "/project/" not in project_url:
        raise SystemExit(f"no project url after submit ({which})")
    return out


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        ctx = browser.contexts[0]
        page = ctx.new_page()
        page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=180000)
        time.sleep(3)
        for name in ("Agree", "Got it", "Accept all"):
            try:
                page.get_by_role("button", name=name).first.click(timeout=1500)
            except Exception:
                pass
        auth = assert_auth(page)
        print(f"auth={auth}", flush=True)

        a = submit_one(page, which="A", lock=LOCK_A, prompt=PROMPT_A, out_path=OUT_A)
        time.sleep(2)
        # fresh page hop reduces Flow project reuse flake
        try:
            page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=180000)
            time.sleep(2)
        except Exception:
            pass
        b = submit_one(page, which="B", lock=LOCK_B, prompt=PROMPT_B, out_path=OUT_B)
        print(
            json.dumps(
                {
                    "submitted": [a.get("project_url"), b.get("project_url")],
                    "next": "harvest both → self-QA on-model glasses+card-desk → assemble v23",
                },
                indent=2,
            ),
            flush=True,
        )


if __name__ == "__main__":
    main()
