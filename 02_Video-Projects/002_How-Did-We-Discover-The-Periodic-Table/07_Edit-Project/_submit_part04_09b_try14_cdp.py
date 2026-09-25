#!/usr/bin/env python3
"""Dedicated 09b_risk_hold try14 submit on live Mini CDP.

Reopen CLEAN LIGHT after try13 STOP (bookshelf invents brass shade-cup).
NEW framing DNA (try8–13 BANNED): Empty Chairs seat-hero + daylight window,
ZEROLAMP — window/moon/off-world bounce ONLY. No practical lamp/shade/bulb/shade-cup.

Model: Veo 3.1 - Quality REQUIRED (Ben LOCK / main 3bc0414). Fast banned. Seedance banned.
Paint banned. No assemble. Max 2 Quality starts this NEW DNA then STOP_TO_COS.

Auth: Mini CDP benoats@googlemail.com ULTRA. STOP on passkey.
Plate-library 4b8ed25. Main lock 3bc0414.
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
START = REF / "09b_risk_hold_start_v20.jpg"
LOCK_A = REF / "09b_risk_hold_start_v20_try14_seathero_daywin_zerolamp.jpg"
LOCK_B = REF / "09b_risk_hold_start_v20_try14B_seathero_daywin_tight_zerolamp.jpg"
BANNED = [
    REF / "09b_risk_hold_start_v20_try8_KEEP_cf182dc.jpg",
    REF / "09b_risk_hold_start_v20_try11_zerolamp_moonwin.jpg",
    REF / "09b_risk_hold_start_v20_try12_rightcam_bookshelfL.jpg",
    REF / "09b_risk_hold_start_v20_try12B_rightcam_tq.jpg",
    REF / "09b_risk_hold_start_v20_try13_bookshelf_zerofixture_outworld.jpg",
    REF / "09b_risk_hold_start_v20_try13B_bookshelf_zerofixture_outworld_tq.jpg",
]
QA_DIR = PROJ / "07_Edit-Project/_qa_part04_v20_plates_try14_09b"
START_COUNTER = QA_DIR / "start_counter.json"
MODEL = os.environ.get("ORBIT_FLOW_VEO_MODEL") or "Veo 3.1 - Quality"
REQUIRED_EMAIL = "benoats@googlemail.com"
MAX_STARTS = 2
OUT_A = PROJ / "07_Edit-Project/_qa_part04_v20_flow/submit_09b_risk_hold_try14.json"
OUT_B = PROJ / "07_Edit-Project/_qa_part04_v20_flow/submit_09b_risk_hold_try14B.json"
PLATE_LIBRARY = "4b8ed25"
MAIN_LOCK = "3bc0414"

PROMPT = (
    "IMAGE-TO-VIDEO of the attached start frame. Animate THIS exact beat only. "
    "Plate 09b_risk_hold try14 — A BET / Empty Chairs HOLD (soft vacant seat after 09_risk_bet; "
    "Veo 3.1 Quality REQUIRED; NEW framing DNA — NOT try8–13). "
    "Finished cinematic stylised 3D laboratory hall (Animistry-class polish). "
    "NOT flat unfinished vlog vector. NOT 2D cutouts. NOT paint. NOT Ken Burns. "
    "Hero: EMPTY ornate wooden chairs in a row — Soft Empty Chairs seat glow ONLY "
    "(warm soft non-fire glow on vacant seats). Lab shelves with blue glassware behind. "
    "Tall arched DAYLIGHT WINDOW on the RIGHT with soft god-rays / window spill. "
    "CARDLESS (HARD): ZERO unfinished flat H/C/O/N element cards, letter tiles, HUD chips. "
    "Blank papers OK if any. No Explorer. No Orbit robot. No model-town / yellow house-blocks. "
    "CLEAN LIGHT / ZEROLAMP (HARD for full 8s): daylight WINDOW + soft OFF-WORLD bounce ONLY. "
    "THERE IS NO PRACTICAL TABLE LAMP IN FRAME — zero gooseneck, zero lampshade, zero bulb, "
    "zero shade-cup (open or closed), zero brass desk lamp, zero wall sconce, zero candle fixture, "
    "zero chandelier, zero torchiere, zero underside bulb look-in. "
    "Do NOT invent any lamp/fixture mid-clip on ANY edge (esp. LEFT + TOP — Quality invent zones). "
    "Warm fill may exist BEHIND CAMERA / OUT OF WORLD — never a visible fixture. "
    "Soft Empty Chairs seat glow is NOT a lamp and must NOT become fire, flame, lava, or molten bead. "
    "ACTION: gentle continuous Empty Chairs hold — soft seat glow breathes; dust motes drift in "
    "window light; glassware catches dull window bounce; LOCKED TRIPOD — no pan/zoom/tilt that "
    "reveals a lamp zone off left or top. "
    "HOUSE HARD FAIL forever (t0–t8): open shade-cup, practical lamp invent, underside bulb, "
    "lava drip, molten bead, chair fire, leather flames, unfinished flat H/C/O/N, "
    "model-town / yellow house-blocks, double-exposure / ghost doubles, Explorer, paint. "
    "Continuous real Veo motion. Silent. Paint banned. Seedance banned. Fast banned. "
    f"Plate-library lock {PLATE_LIBRARY}. Main lock {MAIN_LOCK}. "
    "NEW try14 DNA: seat-hero + daylight window + zerolamp — NOT moon-desk try8–12, "
    "NOT bookshelf try13 invent tree."
)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bump_start_counter(which: str, dna: str) -> int:
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
                "plate": "09b_risk_hold",
                "try": 14,
                "which": which,
                "starts": n,
                "max_starts": MAX_STARTS,
                "dna": dna,
                "model": MODEL,
                "when": time.strftime("%Y-%m-%dT%H:%M:%S"),
            },
            indent=2,
        )
        + "\n"
    )
    if n > MAX_STARTS:
        raise SystemExit(
            f"STOP_TO_COS: try14 DNA already used {n - 1}/{MAX_STARTS} Quality starts — do not mint further"
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
    which = (os.environ.get("HOS_09B_TRY14_START") or "A").upper().strip()
    if which == "B":
        lock = LOCK_B
        out_path = OUT_B
        dna_tag = (
            "try14B NEW KEEP seat-hero daywin tight: Empty Chairs vacant ornate seats + "
            "daylight window RIGHT; lamp zones OFF-FRAME left+top; CLEAN=window/off-world ONLY; "
            "ZEROLAMP; CARDLESS; soft Empty Chairs glow OK (not fire); finished 3D; LOCKED TRIPOD; "
            f"plate-library {PLATE_LIBRARY}; main {MAIN_LOCK}; NOT try8–13 moon-desk/bookshelf; "
            "paint banned; Seedance banned; Fast banned; Quality REQUIRED"
        )
    else:
        which = "A"
        lock = LOCK_A
        out_path = OUT_A
        dna_tag = (
            "try14A NEW KEEP seat-hero daywin: Empty Chairs vacant ornate seats + "
            "daylight window RIGHT; ZEROLAMP window/off-world bounce ONLY; CARDLESS; "
            "soft Empty Chairs glow OK (not fire); finished 3D; LOCKED TRIPOD; "
            f"plate-library {PLATE_LIBRARY}; main {MAIN_LOCK}; NOT try8–13 moon-desk/bookshelf; "
            "paint banned; Seedance banned; Fast banned; Quality REQUIRED"
        )

    if not lock.exists():
        raise SystemExit(f"ABORT: missing try14 start {lock}")
    if sha(START) != sha(lock):
        START.write_bytes(lock.read_bytes())
        print(f"synced ACTIVE start <- {lock.name}", flush=True)
    if sha(START) != sha(lock):
        raise SystemExit("ABORT: active start != chosen try14 lock")

    s = sha(START)
    for banned in BANNED:
        if banned.exists() and s == sha(banned):
            raise SystemExit(f"ABORT: active start collides with banned DNA {banned.name}")

    for need in (
        "ZEROLAMP",
        "NO PRACTICAL TABLE LAMP",
        "shade-cup",
        "WINDOW",
        "OFF-WORLD",
        "molten bead",
        "CARDLESS",
        "H/C/O/N",
        PLATE_LIBRARY,
        MAIN_LOCK,
        "LOCKED TRIPOD",
        "Empty Chairs",
        "Seedance",
        "try14",
        "Quality",
    ):
        if need.lower() not in PROMPT.lower():
            raise SystemExit(f"ABORT: prompt missing {need}")

    if "Quality" not in MODEL:
        raise SystemExit("ABORT: locked brief requires Veo 3.1 Quality for 09b try14 (CLEAN LIGHT)")
    if "Seedance" in MODEL or "seedance" in MODEL.lower():
        raise SystemExit("ABORT: Seedance banned")

    start_n = bump_start_counter(which, dna_tag)

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

        tmp = Path(f"/tmp/hos_v20_09b_try14{which}_stub.mp4")
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
            "plate": "09b_risk_hold",
            "try": f"14{which}" if which != "A" else 14,
            "start_n": start_n,
            "max_starts": MAX_STARTS,
            "project_url": project_url,
            "info": {k: v for k, v in info.items() if k != "path"},
            "start": str(START),
            "start_sha256": s,
            "start_lock": str(lock),
            "start_dna": dna_tag,
            "family": "NEW_KEEP_try14_seathero_daywin_zerolamp_empty_chairs",
            "plate_library_lock_sha": PLATE_LIBRARY,
            "main_lock_sha": MAIN_LOCK,
            "model": MODEL,
            "model_rationale": (
                "Quality REQUIRED — CLEAN LIGHT / lamp invent class "
                "(locked Showrunner brief PART04_NEXT_PLATE_09B_QUALITY_REOPEN.md; Ben LOCK main 3bc0414)"
            ),
            "seedance": "banned",
            "fast": "banned",
            "when": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "auth": auth,
            "paint": "banned",
            "assemble": False,
            "parent_keeps": {"06": "KEEP", "11": "97d0c419…", "11b": "5602762e…"},
            "banned_dna": "try8–13 moon-desk / bookshelf lamp invent",
            "out_of_scope": [
                "06_explorer_leaves_gap",
                "11_publish_gaps",
                "11b_wait_and_hunt",
                "assemble",
            ],
            "stop_rule": (
                "Max 2 Quality starts this NEW DNA; invent lamp/molten/fire → SELF_REJECT; "
                "both fail → STOP_TO_COS"
            ),
            "brief_lock": "PART04_NEXT_PLATE_09B_QUALITY_REOPEN.md",
        }
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(out, indent=2) + "\n")
        print(json.dumps(out, indent=2), flush=True)
        if "/project/" not in project_url:
            raise SystemExit("no project url after submit")


if __name__ == "__main__":
    main()
