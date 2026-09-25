#!/usr/bin/env python3
"""Dedicated 06_explorer_leaves_gap try3 submit on live Mini CDP.

UAT HARD FAIL try2 sha c12b17ae82943c844fa981500ad7e7647414435980e9079d67883d874c85eaf8:
conical flask invents intense molten/glow desk light mid→late.
CLEARED on try2: crown OTS, glasses N/A, lamp prop invent, flats, continuous motion, soft gap glow.
try3 DNA: keep OTS Explorer + gap. HARD: flask liquids stay dull/matte translucent —
NEVER self-emissive / molten / desk-lighting invent. No practical lamp/shade-cup.
CLEAN LIGHT = window/off-world bounce ONLY. Soft gap glow OK if not inventing as lamp.

Paint banned. No assemble. Plate-library 4b8ed25.
Auth: Mini CDP benoats@googlemail.com ULTRA. STOP on passkey.
Max 2 starts this run then STOP_TO_COS. No 11/11b/09b.
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
LOCK = REF / "06_explorer_leaves_gap_start_v20_try1_ots_nolamp_windowbounce.jpg"
OUT = PROJ / "07_Edit-Project/_qa_part04_v20_flow/submit_06_explorer_leaves_gap_try3.json"
QA_DIR = PROJ / "07_Edit-Project/_qa_part04_v20_plates_try3_06"
START_COUNTER = QA_DIR / "start_counter.json"
MODEL = os.environ.get("ORBIT_FLOW_VEO_MODEL") or "Veo 3.1 - Fast"
REQUIRED_EMAIL = "benoats@googlemail.com"
MAX_STARTS = 2

PROMPT = (
    "IMAGE-TO-VIDEO of the attached start frame. Animate THIS exact beat only. "
    "Plate 06_explorer_leaves_gap try3 — EMPTY SEATS garnish, SAME OTS DNA as try2 with HARD flask lock. "
    "ONE finished Explorer (teal trenchcoat house lock, full chestnut crown finished — "
    "ZERO mid-crown unfinished hair) as toy-scale garnish. "
    "LOCKED BACK / OTS / REAR THREE-QUARTER for the FULL 8 seconds — "
    "Explorer's FACE NEVER turns toward camera; we only see the back of the head and coat; "
    "do NOT spin, do NOT face-reveal, do NOT cut to front. "
    "1869 card-desk DNA: warm wood desk, cream written cards in stacks, bookcase behind OK. "
    "Action: Explorer pins a card with small hand motion, then takes a small step BACK/AWAY from desk "
    "leaving a soft glowing vacant seat / gap on the desk — soft warm gap glow only, "
    "NOT chair fire, NOT lava, NOT molten bead. Soft gap glow OK as a thin band in the card stack "
    "if it does NOT invent as a lamp. "
    "Sparse readable marks on a few cards OK; ZERO unfinished flat blank cards. "
    "CLEAN LIGHT (HARD for full 8s): daytime WINDOW spill and/or soft OFF-WORLD bounce ONLY. "
    "THERE IS NO PRACTICAL TABLE LAMP IN FRAME — zero gooseneck, zero lampshade, zero bulb, "
    "zero shade-cup (open or closed), zero brass desk lamp, zero wall sconce, zero candle fixture. "
    "Do NOT invent any lamp/fixture mid-clip on any edge. "
    "FLASK / GLASSWARE LIQUIDS (HARD for full 8s — try2 UAT HARD FAIL): "
    "every conical flask and bottle liquid stays DULL / MATTE / TRANSLUCENT — "
    "pale amber or tea-brown inert reagent only. "
    "NEVER self-emissive, NEVER molten, NEVER lava-core, NEVER neon fill, NEVER intensifying glow, "
    "NEVER desk-lighting invent from flask liquid mid→late. "
    "Flask glass may catch soft window bounce as a dull highlight only — liquid itself does not light the desk. "
    "HOUSE HARD FAIL forever (t0–t8): flask molten glow, flask desk light pool, lava drip, molten bead, "
    "chair fire, unfinished flat cards, mid-crown unfinished Explorer hair, open shade-cup, "
    "visible underside bulb, invented brass lamp, model-town / yellow house-blocks, twins, "
    "academic blazer Explorer, Orbit robot, face-turn toward camera, front-facing Explorer hero. "
    "Exactly ONE Explorer. Continuous real Veo motion. "
    "LOCKED TRIPOD CAMERA — do NOT widen, zoom out, or pan to reveal a lamp off-frame. "
    "Finished cinematic stylised 3D. Silent. Paint banned. "
    "Plate-library lock 4b8ed25. NOT ore/gas workshop room."
)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bump_start_counter() -> int:
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
                "try": 3,
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
            f"STOP_TO_COS: try3 already used {n - 1}/{MAX_STARTS} Flow starts — do not mint further"
        )
    print(f"start_counter={n}/{MAX_STARTS}", flush=True)
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


def main() -> None:
    if not LOCK.exists():
        raise SystemExit(f"ABORT: missing lock {LOCK}")
    if sha(START) != sha(LOCK):
        START.write_bytes(LOCK.read_bytes())
        print(f"synced ACTIVE start <- {LOCK.name}", flush=True)
    if sha(START) != sha(LOCK):
        raise SystemExit("ABORT: active start != nolamp lock")

    for need in (
        "NO PRACTICAL TABLE LAMP",
        "shade-cup",
        "WINDOW",
        "OFF-WORLD",
        "molten bead",
        "mid-crown",
        "1869",
        "LOCKED BACK",
        "NEVER turns",
        "4b8ed25",
        "LOCKED TRIPOD",
        "face-turn",
        "DULL / MATTE",
        "desk-lighting invent",
        "self-emissive",
        "FLASK",
    ):
        if need.lower() not in PROMPT.lower():
            raise SystemExit(f"ABORT: prompt missing {need}")

    start_n = bump_start_counter()

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

        tmp = Path("/tmp/hos_v20_06_try3_stub.mp4")
        if tmp.exists():
            tmp.unlink()
        info: dict = {}
        try:
            info = flow.generate_clip(
                page,
                PROMPT,
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
            print(f"submit note: {e}", flush=True)

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
            "try": 3,
            "start_n": start_n,
            "max_starts": MAX_STARTS,
            "project_url": project_url,
            "info": {k: v for k, v in info.items() if k != "path"},
            "start": str(START),
            "start_sha256": sha(START),
            "start_dna": (
                "try3 = try2 OTS/back nolamp lock + HARD dull/matte flask liquids "
                "(never self-emissive / molten / desk-lighting invent); "
                "CLEAN=window/off-world bounce ONLY; soft gap glow OK; plate-library 4b8ed25"
            ),
            "plate_library_lock_sha": "4b8ed25",
            "model": MODEL,
            "when": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "auth": auth,
            "paint": "banned",
            "assemble": False,
            "parent_try2": {
                "verdict": "UAT_HARD_FAIL",
                "sha256": "c12b17ae82943c844fa981500ad7e7647414435980e9079d67883d874c85eaf8",
                "blocker": "conical flask invents intense molten/glow desk light mid→late",
                "cleared": "crown OTS, glasses N/A, lamp prop invent, flats, continuous motion, soft gap glow OK",
            },
        }
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(out, indent=2) + "\n")
        print(json.dumps(out, indent=2), flush=True)
        if "/project/" not in project_url:
            raise SystemExit("no project url after submit")


if __name__ == "__main__":
    main()
