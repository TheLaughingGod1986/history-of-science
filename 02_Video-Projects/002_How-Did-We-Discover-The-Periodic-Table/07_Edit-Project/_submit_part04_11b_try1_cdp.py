#!/usr/bin/env python3
"""Dedicated 11b_wait_and_hunt try1 submit on live Mini CDP.

Parent: 11_publish_gaps try9 Fast UAT KEEP
  sha 97d0c419fdf7720f366140a9fb2b024a29580a2db51a434e7afb425a19f8cc72
Start: last frame of 11 KEEP (continuity join).
DNA: same board-top edge-off / zerolamp moon-window as 11 KEEP.
Model: Veo 3.1 - Quality REQUIRED (CLEAN LIGHT class per locked Showrunner brief).
Seedance banned. Paint banned. No assemble. No 09b. No remint 06/11.

Auth: Mini CDP benoats@googlemail.com ULTRA. STOP on passkey.
Plate-library 4b8ed25. Main lock 3bc0414.
Max 2 starts this DNA then STOP_TO_COS.
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
START = REF / "11b_wait_and_hunt_start_v20.jpg"
LOCK = REF / "11b_wait_and_hunt_start_v20_from_11_try9_KEEP_last.jpg"
QA_DIR = PROJ / "07_Edit-Project/_qa_part04_v20_plates_try1_11b"
START_COUNTER = QA_DIR / "start_counter.json"
# CLEAN LIGHT class — Quality REQUIRED (locked brief). Seedance banned.
MODEL = os.environ.get("ORBIT_FLOW_VEO_MODEL") or "Veo 3.1 - Quality"
REQUIRED_EMAIL = "benoats@googlemail.com"
MAX_STARTS = 2
OUT = PROJ / "07_Edit-Project/_qa_part04_v20_flow/submit_11b_wait_and_hunt_try1.json"
PARENT_11_SHA = "97d0c419fdf7720f366140a9fb2b024a29580a2db51a434e7afb425a19f8cc72"
PLATE_LIBRARY = "4b8ed25"
MAIN_LOCK = "3bc0414"

PROMPT = (
    "IMAGE-TO-VIDEO of the attached start frame. Animate THIS exact beat only. "
    "Plate 11b_wait_and_hunt try1 — WAIT AND HUNT (sibling after 11_publish_gaps KEEP; "
    "continuity join from 11 last frame; Veo 3.1 Quality; zerolamp DNA). "
    "Finished cinematic stylised 3D chemist desk (Animistry-class). "
    "NOT flat unfinished vlog vector. NOT 2D cutouts. "
    "Hero: TOP of published parchment/grid with CLEAR circular holes / empty seats, "
    "magnifier resting on the grid, paper scraps — the FRONT EDGE / printable band of the board "
    "is OUT OF FRAME (below the bottom of this crop). Do NOT invent or reveal that front lip. "
    "ACTION: gentle continuous WAIT AND HUNT push toward the empty holes after publish — "
    "slow intentional settle into the gaps; papers and magnifier may drift a hair toward holes. "
    "Soft gap glow on empty circular holes OK as a thin warm band ONLY if it does NOT invent as a lamp. "
    "TEXT / CAPTION LOCK (HARD for full 8s): ZERO printed words, ZERO letters, ZERO captions, ZERO UI, "
    "ZERO watermarks, ZERO logos, ZERO 'SECURITY', ZERO 'RESULT', ZERO 'SERIES', ZERO any readable text "
    "on grid, papers, flasks, or edges. Blank cream tiles only — no symbols. "
    "CLEAN LIGHT / ZEROLAMP (HARD for full 8s): moonlight / WINDOW spill + soft OFF-WORLD bounce ONLY. "
    "THERE IS NO PRACTICAL TABLE LAMP IN FRAME — zero gooseneck, zero lampshade, zero bulb, "
    "zero shade-cup (open or closed), zero brass desk lamp, zero wall sconce, zero candle fixture. "
    "Do NOT invent any lamp/fixture mid-clip on any edge (esp. LEFT desk — Quality invent zone). "
    "Warm fill may exist BEHIND CAMERA / OUT OF WORLD — never a visible fixture. "
    "FLASK / GLASSWARE LIQUIDS (HARD for full 8s): every flask and bottle liquid stays DULL / MATTE / TRANSLUCENT — "
    "pale amber, pink, or green inert reagent only. "
    "NEVER self-emissive, NEVER molten, NEVER lava-core, NEVER neon fill, NEVER intensifying glow, "
    "NEVER desk-lighting invent from flask liquid mid→late. "
    "Flask glass may catch soft window bounce as a dull highlight only — liquid itself does not light the desk. "
    "CARDLESS / NO unfinished flat H/C/O/N element cards — ALWAYS FAIL if flat H/C/O/N appear. "
    "HOUSE HARD FAIL forever (t0–t8): readable text invent, open shade-cup, practical lamp invent, "
    "flask molten/desk-glow invent, lava drip, molten bead, chair fire, unfinished flat H/C/O/N, "
    "model-town / yellow house-blocks, double-exposure / horizontal ghost smear, Explorer, Orbit robot, "
    "camera tip that re-reveals the off-frame front printable board edge or left lamp zone. "
    "LOCKED TRIPOD CAMERA — do NOT widen, zoom out, tilt down, or pan to reveal a lamp or the board front lip. "
    "Continuous real Veo motion. Silent. Paint banned. Seedance banned. "
    f"Plate-library lock {PLATE_LIBRARY}. Main lock {MAIN_LOCK}. "
    "Same 1869 night study DNA as 11 KEEP — moon/window bounce, bookshelf OK."
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
                "plate": "11b_wait_and_hunt",
                "try": 1,
                "starts": n,
                "max_starts": MAX_STARTS,
                "dna": "try1 from 11 KEEP last — boardtop edgeoff zerolamp",
                "parent_11_sha256": PARENT_11_SHA,
                "model": MODEL,
                "when": time.strftime("%Y-%m-%dT%H:%M:%S"),
            },
            indent=2,
        )
        + "\n"
    )
    if n > MAX_STARTS:
        raise SystemExit(
            f"STOP_TO_COS: try1 DNA already used {n - 1}/{MAX_STARTS} Flow starts — do not mint further"
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
            '[aria-label*="Account"]',
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
    return {
        "ultra": True,
        "email_hint": REQUIRED_EMAIL.lower() in blob or "googlemail.com" in blob,
    }


def main() -> None:
    if not LOCK.exists():
        raise SystemExit(f"ABORT: missing lock start {LOCK}")
    if sha(START) != sha(LOCK):
        START.write_bytes(LOCK.read_bytes())
        print(f"synced ACTIVE start <- {LOCK.name}", flush=True)
    if sha(START) != sha(LOCK):
        raise SystemExit("ABORT: active start != 11b from-11-KEEP lock")

    for need in (
        "ZEROLAMP",
        "NO PRACTICAL TABLE LAMP",
        "shade-cup",
        "WINDOW",
        "OFF-WORLD",
        "molten bead",
        "DULL / MATTE",
        "desk-lighting invent",
        "CARDLESS",
        "H/C/O/N",
        PLATE_LIBRARY,
        MAIN_LOCK,
        "LOCKED TRIPOD",
        "WAIT AND HUNT",
        "circular holes",
        "SECURITY",
        "RESULT",
        "self-emissive",
        "FLASK",
        "front lip",
        "Seedance",
    ):
        if need.lower() not in PROMPT.lower():
            raise SystemExit(f"ABORT: prompt missing {need}")

    if "Quality" not in MODEL:
        raise SystemExit("ABORT: locked brief requires Veo 3.1 Quality for 11b (CLEAN LIGHT class)")
    if "Seedance" in MODEL or "seedance" in MODEL.lower():
        raise SystemExit("ABORT: Seedance banned")

    start_n = bump_start_counter()

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        page = None
        for ctx in browser.contexts:
            for pg in ctx.pages:
                if "flow.google.com" in (pg.url or ""):
                    page = pg
                    break
            if page:
                break
        if page is None:
            page = browser.contexts[0].new_page()
        page.bring_to_front()
        page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=180000)
        time.sleep(3)
        for name in ("Agree", "Got it", "Accept all"):
            try:
                page.get_by_role("button", name=name).first.click(timeout=1500)
            except Exception:
                pass
        auth = assert_auth(page)

        tmp = Path("/tmp/hos_v20_11b_try1_stub.mp4")
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
                timeout_s=90,
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
            "plate": "11b_wait_and_hunt",
            "try": 1,
            "start_n": start_n,
            "max_starts": MAX_STARTS,
            "project_url": project_url,
            "info": {k: v for k, v in info.items() if k != "path"},
            "start": str(START),
            "start_sha256": sha(START),
            "start_dna": (
                "try1 from 11 KEEP last: boardtop edgeoff zerolamp continuity join — "
                "publish-grid front printable band OFF-FRAME; holes+magnifier hero; "
                "gentle hunt toward holes; CLEAN=window/moon/off-world bounce ONLY; "
                "dull/matte flasks; cardless/no unfinished H/C/O/N; soft gap glow OK; "
                f"plate-library {PLATE_LIBRARY}; main {MAIN_LOCK}; paint banned; Seedance banned"
            ),
            "plate_library_lock_sha": PLATE_LIBRARY,
            "main_lock_sha": MAIN_LOCK,
            "model": MODEL,
            "model_rationale": (
                "Quality REQUIRED — CLEAN LIGHT / lamp·flask·emissive invent class "
                "(locked Showrunner brief PART04_NEXT_PLATE_11B_WAIT_AND_HUNT.md)"
            ),
            "seedance": "banned",
            "when": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "auth": auth,
            "paint": "banned",
            "assemble": False,
            "parent_11": {
                "verdict": "UAT_KEEP",
                "sha256": PARENT_11_SHA,
                "model": "Veo 3.1 - Fast",
            },
            "parent_06": {
                "verdict": "UAT_PASS",
                "sha256": "df9bb44fb123e1a737976517be0dc809470f1828f1dba0dc8f1178f59721978c",
            },
            "parked": ["09b_risk_hold"],
            "out_of_scope": [
                "09b_risk_hold",
                "06_explorer_leaves_gap",
                "11_publish_gaps",
                "assemble",
            ],
        }
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(out, indent=2) + "\n")
        print(json.dumps(out, indent=2), flush=True)
        if "/project/" not in project_url:
            raise SystemExit("no project url after submit")


if __name__ == "__main__":
    main()
