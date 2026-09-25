#!/usr/bin/env python3
"""Dedicated 09b_risk_hold try13 submit on live Mini CDP.

NEW KEEP FAMILY (CoS): v07 bookshelf + empty tufted leather chair + CARDLESS +
warm CLEAN fill from OFF-LEFT / out of world (desk-lamp fixture cropped out of start).
NOT try8–12 moon-desk crop/flip invent tree. NOT v01 cardless empty-chair moon starts.

Bible 8ddbf99 — never soft-pass molten bead / shade-cup invent.
Paint banned. No assemble. Max 2 starts. If both invent ANY fixture → STOP_TO_COS.
Auth: Mini CDP googlemail ULTRA. STOP on passkey.
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
LOCK_A = REF / "09b_risk_hold_start_v20_try13_bookshelf_zerofixture_outworld.jpg"
LOCK_B = REF / "09b_risk_hold_start_v20_try13B_bookshelf_zerofixture_outworld_tq.jpg"
TRY8 = REF / "09b_risk_hold_start_v20_try8_KEEP_cf182dc.jpg"
TRY11 = REF / "09b_risk_hold_start_v20_try11_zerolamp_moonwin.jpg"
TRY12 = REF / "09b_risk_hold_start_v20_try12_rightcam_bookshelfL.jpg"
TRY12B = REF / "09b_risk_hold_start_v20_try12B_rightcam_tq.jpg"
OUT_A = PROJ / "07_Edit-Project/_qa_part04_v20_flow/submit_09b_risk_hold_try13.json"
OUT_B = PROJ / "07_Edit-Project/_qa_part04_v20_flow/submit_09b_risk_hold_try13B.json"
MODEL = os.environ.get("ORBIT_FLOW_VEO_MODEL") or "Veo 3.1 - Fast"
REQUIRED_EMAIL = "benoats@googlemail.com"

PROMPT = (
    "IMAGE-TO-VIDEO of the attached start frame. Animate THIS exact empty-chair night study. "
    "NEW KEEP FAMILY try13: finished cinematic stylised 3D — honey wood desk, EMPTY tufted leather "
    "chair, floor-to-ceiling BOOKSHELVES behind, soft Empty Chairs panel glow OK. "
    "CARDLESS desk (HARD): books, mortar, ceramic vessels, blank paper slips only — "
    "ZERO flat H/C/O/N element cards, letter tiles, HUD chips, unfinished flat overlays. "
    "CLEAN LIGHT (HARD): warm CLEAN directional fill arrives from OFF-LEFT / OUT OF WORLD ONLY. "
    "THERE IS NO DESK LAMP AND NO LIGHTING FIXTURE OF ANY KIND IN FRAME — "
    "zero gooseneck, zero lampshade, zero bulb, zero shade cup, zero wall sconce, zero candle holder, "
    "zero chandelier, zero torchiere, zero fixture that can be invented on left OR right. "
    "Do NOT invent any lamp/fixture mid-clip on any edge. Do NOT tip a shade cup into view. "
    "LOCKED TRIPOD CAMERA. Silent. LOCKED FRAMING for all 8s — identical crop to the start frame: "
    "do NOT widen, do NOT zoom out, do NOT pan left/right, do NOT reveal anything off any edge. "
    "HOUSE HARD FAIL IF BROKEN for the FULL 8 seconds "
    "(try9 UAT HARD FAIL bible 8ddbf99 — NEVER soft-pass molten bead under shade cup; "
    "try10–12 SELF_REJECT: Veo invented lamp fixtures mid-clip from empty-chair starts — "
    "try13 DNA = NEW bookshelf leather-chair family with fixture already cropped out): "
    "HARD BAN forever (t0 through t8): inventing any lighting fixture, desk lamp, gooseneck, "
    "lampshade, bulb, shade cup, looking into shade, wall sconce, lava drip, molten teardrop, "
    "molten bead, glowing droplet, fire spit, sparks, embers, lava, molten leak, dripping bulb goo, "
    "fire, flame, flames, spark, ember, burning chair rim, candle flicker, firework particles, "
    "glowing coal, lamp-beam sparks, floating embers, visible bulb underside, open shade cup, "
    "mid-crown unfinished hair, unfinished flat cards, paint, double-exposure. "
    "Soft Empty Chairs glow OK. No Explorer. No Orbit. No paint. Finished 3D only. "
    "NOT try8–12 moon-desk DNA. NOT v01 cardless moon empty-chair invent tree."
)


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


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
            'img[alt*="Google Account"]',
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
    which = (os.environ.get("HOS_09B_TRY13_START") or "A").upper().strip()
    if which == "B":
        want = LOCK_B
        out_path = OUT_B
        dna_tag = (
            "try13B NEW KEEP bookshelf leather-chair tq: v07 L50 crop — ZERO fixture in frame; "
            "CLEAN=warm OFF-LEFT out-of-world fill ONLY; CARDLESS; Soft Empty Chairs OK; "
            "finished 3D; LOCKED FRAMING; bible 8ddbf99; plate-library 4b8ed25; "
            "NOT try8–12 moon-desk invent tree; paint banned"
        )
    else:
        which = "A"
        want = LOCK_A
        out_path = OUT_A
        dna_tag = (
            "try13A NEW KEEP bookshelf leather-chair: v07 L38 crop — ZERO fixture in frame; "
            "CLEAN=warm OFF-LEFT out-of-world fill ONLY; CARDLESS empty tufted leather chair + bookshelves; "
            "Soft Empty Chairs OK; finished 3D; LOCKED FRAMING; bible 8ddbf99; plate-library 4b8ed25; "
            "NOT try8–12 moon-desk invent tree; NOT v01 moon empty-chair invent starts; paint banned"
        )

    if not want.exists():
        raise SystemExit(f"ABORT: missing try13 start {want}")
    if sha(START) != sha(want):
        START.write_bytes(want.read_bytes())
        print(f"synced ACTIVE start <- {want.name}", flush=True)

    s = sha(START)
    for banned, label in (
        (TRY8, "try8 KEEP moon-desk"),
        (TRY11, "try11 zerolamp moon"),
        (TRY12, "try12 rightcam moon-desk flip"),
        (TRY12B, "try12B rightcam moon-desk flip"),
    ):
        if banned.exists() and s == sha(banned):
            raise SystemExit(f"ABORT: active start is banned {label}")
    if s != sha(want):
        raise SystemExit("ABORT: active start != chosen try13 lock")

    for need in (
        "molten bead",
        "shade cup",
        "CARDLESS",
        "8ddbf99",
        "OUT OF WORLD",
        "NO DESK LAMP",
        "fixture",
        "gooseneck",
        "try13",
        "LOCKED FRAMING",
        "BOOKSHELVES",
        "Empty Chairs",
    ):
        if need.lower() not in PROMPT.lower():
            raise SystemExit(f"ABORT: prompt missing {need}")

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

        tmp = Path(f"/tmp/hos_v20_09b_try13{which}_stub.mp4")
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
            "plate": "09b_risk_hold",
            "try": f"13{which}",
            "project_url": project_url,
            "info": {k: v for k, v in info.items() if k != "path"},
            "start": str(START),
            "start_sha256": s,
            "start_dna": dna_tag,
            "plate_library_lock_sha": "4b8ed25",
            "bible": "8ddbf99",
            "model": MODEL,
            "when": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "auth": auth,
            "parent_try9_uat": "FORMAL HARD FAIL molten bead — bible 8ddbf99",
            "parent_try10_12": "SELF_REJECT — lamp fixture invent mid-clip on moon-desk DNA",
            "family": "NEW_KEEP_v07_bookshelf_empty_leather_chair_zerofixture_outworld",
            "paint": "banned",
            "assemble": False,
            "max_starts": 2,
            "stop_rule": "If A and B both invent ANY fixture → STOP_TO_COS",
        }
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(out, indent=2) + "\n")
        print(json.dumps(out, indent=2), flush=True)
        if "/project/" not in project_url:
            raise SystemExit("no project url after submit")


if __name__ == "__main__":
    main()
