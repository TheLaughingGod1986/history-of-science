#!/usr/bin/env python3
"""Dedicated 11_publish_gaps try8 submit on live Mini CDP.

Parent: 06_explorer_leaves_gap try3 UAT PASS
  sha df9bb44fb123e1a737976517be0dc809470f1828f1dba0dc8f1178f59721978c
09b parked. Paint banned. No assemble. No 11b/09b/06 this run.

try8 DNA: cropL40 zerolamp moonwin — practical lamp OFF FRAME.
CLEAN LIGHT = window/moon/off-world bounce ONLY.
Flask liquids dull/matte translucent — never self-emissive / desk-lighting invent.
Cardless / no unfinished flat H/C/O/N. Soft gap glow OK if not inventing as lamp.

Auth: Mini CDP benoats@googlemail.com ULTRA. STOP on passkey.
Max 2 starts this run then STOP_TO_COS.
Plate-library 4b8ed25.
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
START = REF / "11_publish_gaps_start_v20.jpg"
LOCK = REF / "11_publish_gaps_start_v20_try8_zerolamp_moonwin.jpg"
LAMP_DNA = REF / "11_publish_gaps_start_v20_pre_try8.jpg"
OUT = PROJ / "07_Edit-Project/_qa_part04_v20_flow/submit_11_publish_gaps_try8.json"
QA_DIR = PROJ / "07_Edit-Project/_qa_part04_v20_plates_try8_11"
START_COUNTER = QA_DIR / "start_counter.json"
MODEL = os.environ.get("ORBIT_FLOW_VEO_MODEL") or "Veo 3.1 - Fast"
REQUIRED_EMAIL = "benoats@googlemail.com"
MAX_STARTS = 2

PROMPT = (
    "IMAGE-TO-VIDEO of the attached start frame. Animate THIS exact beat only. "
    "Plate 11_publish_gaps try8 — PUBLISH THE GAPS. "
    "Finished cinematic stylised 3D chemist desk (Animistry-class). "
    "NOT flat unfinished vlog vector. NOT 2D cutouts. "
    "Hero: published parchment/grid board with CLEAR circular holes / empty seats on the honey wood desk, "
    "paper stack / loose papers, magnifier OK, flasks along the window. "
    "Soft gap glow on empty circular holes OK as a thin warm band ONLY if it does NOT invent as a lamp. "
    "CLEAN LIGHT (HARD for full 8s): moonlight through the WINDOW + window spill + soft OFF-WORLD bounce ONLY. "
    "THERE IS NO PRACTICAL TABLE LAMP IN FRAME — zero gooseneck, zero lampshade, zero bulb, "
    "zero shade-cup (open or closed), zero brass desk lamp, zero wall sconce, zero candle fixture. "
    "Do NOT invent any lamp/fixture mid-clip on any edge. "
    "Warm fill may exist BEHIND CAMERA / OUT OF WORLD — never a visible fixture. "
    "FLASK / GLASSWARE LIQUIDS (HARD for full 8s): every flask and bottle liquid stays DULL / MATTE / TRANSLUCENT — "
    "pale amber, pink, or green inert reagent only. "
    "NEVER self-emissive, NEVER molten, NEVER lava-core, NEVER neon fill, NEVER intensifying glow, "
    "NEVER desk-lighting invent from flask liquid mid→late. "
    "Flask glass may catch soft window bounce as a dull highlight only — liquid itself does not light the desk. "
    "CARDLESS / NO unfinished flat H/C/O/N element cards that fail house. "
    "Blank paper stacks OK for the publish beat; do NOT write letters, element symbols, captions, or UI. "
    "HOUSE HARD FAIL forever (t0–t8): open shade-cup, practical lamp invent, flask molten/desk-glow invent, "
    "lava drip, molten bead, chair fire, unfinished flat H/C/O/N, model-town / yellow house-blocks, "
    "double-exposure / horizontal ghost smear, Explorer, Orbit robot. "
    "LOCKED TRIPOD CAMERA — do NOT widen, zoom out, or pan to reveal a lamp off-frame. "
    "Continuous real Veo motion. Silent. Paint banned. "
    "Plate-library lock 4b8ed25. Same 1869 night study DNA — moon in window, bookshelf OK."
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
                "plate": "11_publish_gaps",
                "try": 8,
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
    if LAMP_DNA.exists() and sha(START) == sha(LAMP_DNA):
        raise SystemExit("ABORT: active start still lamp DNA (pre_try8)")
    if sha(START) != sha(LOCK):
        START.write_bytes(LOCK.read_bytes())
        print(f"synced ACTIVE start <- {LOCK.name}", flush=True)
    if sha(START) != sha(LOCK):
        raise SystemExit("ABORT: active start != try8 zerolamp lock")

    for need in (
        "NO PRACTICAL TABLE LAMP",
        "shade-cup",
        "WINDOW",
        "OFF-WORLD",
        "molten bead",
        "DULL / MATTE",
        "desk-lighting invent",
        "CARDLESS",
        "H/C/O/N",
        "4b8ed25",
        "LOCKED TRIPOD",
        "PUBLISH THE GAPS",
        "circular holes",
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

        tmp = Path("/tmp/hos_v20_11_try8_stub.mp4")
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
            "plate": "11_publish_gaps",
            "try": 8,
            "start_n": start_n,
            "max_starts": MAX_STARTS,
            "project_url": project_url,
            "info": {k: v for k, v in info.items() if k != "path"},
            "start": str(START),
            "start_sha256": sha(START),
            "start_dna": (
                "try8 zerolamp moonwin: cropL40 of v20 publish desk — practical lamp OFF FRAME; "
                "cool left grade; CLEAN=window/moon/off-world bounce ONLY; "
                "dull/matte flasks; cardless/no unfinished H/C/O/N; soft gap glow OK; "
                "plate-library 4b8ed25; paint banned"
            ),
            "plate_library_lock_sha": "4b8ed25",
            "model": MODEL,
            "when": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "auth": auth,
            "paint": "banned",
            "assemble": False,
            "parent_06": {
                "verdict": "UAT_PASS",
                "sha256": "df9bb44fb123e1a737976517be0dc809470f1828f1dba0dc8f1178f59721978c",
            },
            "parked": ["09b_risk_hold"],
            "out_of_scope": ["11b_wait_and_hunt", "09b_risk_hold", "06_explorer_leaves_gap", "assemble"],
        }
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(out, indent=2) + "\n")
        print(json.dumps(out, indent=2), flush=True)
        if "/project/" not in project_url:
            raise SystemExit("no project url after submit")


if __name__ == "__main__":
    main()
