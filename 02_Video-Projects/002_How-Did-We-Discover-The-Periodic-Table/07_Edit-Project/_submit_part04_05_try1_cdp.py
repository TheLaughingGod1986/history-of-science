#!/usr/bin/env python3
"""Dedicated 05_columns_families try1 submit on live Mini CDP.

Parent rough v21 HARD FAIL: CLEAN LIGHT lava drip under bulb ~t38–43 PERIODIC TABLE.
KEEP hold: 06 / 09b / 11 / 11b — do not remint those.
Model: Veo 3.1 - Quality REQUIRED. Fast banned. Seedance banned.
DNA: ZEROLAMP — start crop has practical lamp OFF-FRAME; window/off-world bounce ONLY.
Readable written element cards OK. Continuous motion. Paint banned. No assemble. No plate 10.

Auth: Mini CDP benoats@googlemail.com ULTRA. STOP on passkey.
Plate-library 4b8ed25. Max 2 Quality starts then STOP_TO_COS.
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
REF = PROJ / "04_Generated-Clips/part04/refs/v21_lava_remint_starts"
PARENT_START = REF / "05_columns_families_start_v21_from_v13_t04.jpg"
START = REF / "05_columns_families_start_v21_active.jpg"
LOCK_A = REF / "05_columns_families_start_v21_try1_zerolamp_crop.jpg"
LOCK_B = REF / "05_columns_families_start_v21_try1B_zerolamp_tight.jpg"
QA_DIR = PROJ / "07_Edit-Project/_qa_part04_v22_plates_try1_05"
START_COUNTER = QA_DIR / "start_counter.json"
MODEL = os.environ.get("ORBIT_FLOW_VEO_MODEL") or "Veo 3.1 - Quality"
REQUIRED_EMAIL = "benoats@googlemail.com"
MAX_STARTS = 2
OUT_A = PROJ / "07_Edit-Project/_qa_part04_v22_flow/submit_05_columns_families_try1.json"
OUT_B = PROJ / "07_Edit-Project/_qa_part04_v22_flow/submit_05_columns_families_try1B.json"
PLATE_LIBRARY = "4b8ed25"
MAIN_LOCK = "3bc0414"

PROMPT = (
    "IMAGE-TO-VIDEO of the attached start frame. Animate THIS exact beat only. "
    "Plate 05_columns_families try1 — PERIODIC TABLE desks remint after v21 lava FAIL "
    "(Veo 3.1 Quality REQUIRED; NEW ZEROLAMP framing DNA — practical lamp OFF-FRAME). "
    "Finished cinematic stylised 3D 1869 chemist study desk (Animistry-class polish). "
    "NOT flat unfinished vlog vector. NOT 2D cutouts. NOT paint. NOT Ken Burns. "
    "Hero: cream WRITTEN element cards settle into family COLUMNS on a finished wooden desk — "
    "stack tops and upright cards show sparse readable marks (H/C/O/N/Li/Be/F/Na/Mg OK). "
    "Paper-layer stack edges; cards gently drop / settle into column seats. "
    "Bookshelf + flasks + mortar OK as desk props. No Explorer. No Orbit robot. No model-town. "
    "CLEAN LIGHT / ZEROLAMP (HARD for full 8s): soft WINDOW spill + OFF-WORLD warm bounce ONLY. "
    "THERE IS NO PRACTICAL TABLE LAMP IN FRAME — zero gooseneck, zero lampshade, zero bulb, "
    "zero shade-cup (open or closed), zero brass desk lamp, zero wall sconce, zero candle fixture, "
    "zero chandelier, zero torchiere, zero underside bulb look-in. "
    "Do NOT invent any lamp/fixture mid-clip on ANY edge (esp. LEFT + TOP — Quality invent zones). "
    "Warm fill may exist BEHIND CAMERA / OUT OF WORLD — never a visible fixture. "
    "HOUSE HARD FAIL forever (t0–t8): lava drip, molten bead, liquid light drip from any cup, "
    "open shade-cup, underside bulb, practical lamp invent, desk-lighting invent from flask, "
    "unfinished blank flat cards, model-town / yellow house-blocks, Explorer, paint. "
    "ACTION: continuous gentle settle — cards drift into family columns; dust motes in window light; "
    "LOCKED TRIPOD — no pan/zoom/tilt that reveals a lamp zone off left or top. "
    "Continuous real Veo motion. Silent. Paint banned. Seedance banned. Fast banned. "
    f"Plate-library lock {PLATE_LIBRARY}. Main lock {MAIN_LOCK}. "
    "NEW try1 DNA: card-column hero + zerolamp crop (fixture OFF-FRAME) — NOT v13/v21 lamp-desk."
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
                "plate": "05_columns_families",
                "try": 1,
                "which": which,
                "starts": n,
                "max_starts": MAX_STARTS,
                "dna": dna,
                "model": MODEL,
                "parent_start": str(PARENT_START),
                "when": time.strftime("%Y-%m-%dT%H:%M:%S"),
            },
            indent=2,
        )
        + "\n"
    )
    if n > MAX_STARTS:
        raise SystemExit(
            f"STOP_TO_COS: try1 DNA already used {n - 1}/{MAX_STARTS} Quality starts — do not mint further"
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
    which = (os.environ.get("HOS_05_TRY1_START") or "A").upper().strip()
    if which == "B":
        lock = LOCK_B
        out_path = OUT_B
        dna_tag = (
            "try1B NEW KEEP card-columns tight zerolamp: family card stacks settle; "
            "practical lamp OFF-FRAME; CLEAN=window/off-world ONLY; readable sparse marks OK; "
            "LOCKED TRIPOD; "
            f"plate-library {PLATE_LIBRARY}; main {MAIN_LOCK}; NOT v21 lamp-desk lava; "
            "paint banned; Seedance banned; Fast banned; Quality REQUIRED"
        )
    else:
        which = "A"
        lock = LOCK_A
        out_path = OUT_A
        dna_tag = (
            "try1A NEW KEEP card-columns zerolamp: cream cards drop into family columns; "
            "practical lamp OFF-FRAME; CLEAN=window/off-world bounce ONLY; readable sparse marks OK; "
            "LOCKED TRIPOD; "
            f"plate-library {PLATE_LIBRARY}; main {MAIN_LOCK}; NOT v21 lamp-desk lava; "
            "paint banned; Seedance banned; Fast banned; Quality REQUIRED"
        )

    if not lock.exists():
        raise SystemExit(f"ABORT: missing try1 start {lock}")
    START.write_bytes(lock.read_bytes())
    print(f"synced ACTIVE start <- {lock.name}", flush=True)
    if sha(START) != sha(lock):
        raise SystemExit("ABORT: active start != chosen try1 lock")

    for need in (
        "ZEROLAMP",
        "NO PRACTICAL TABLE LAMP",
        "shade-cup",
        "WINDOW",
        "OFF-WORLD",
        "molten bead",
        "lava drip",
        "family COLUMNS",
        "readable",
        PLATE_LIBRARY,
        MAIN_LOCK,
        "LOCKED TRIPOD",
        "Seedance",
        "Quality",
    ):
        if need.lower() not in PROMPT.lower():
            raise SystemExit(f"ABORT: prompt missing {need}")

    if "Quality" not in MODEL:
        raise SystemExit("ABORT: locked brief requires Veo 3.1 Quality for 05 (CLEAN LIGHT)")
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

        tmp = Path(f"/tmp/hos_v22_05_try1{which}_stub.mp4")
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
            "plate": "05_columns_families",
            "try": f"1{which}" if which != "A" else 1,
            "start_n": start_n,
            "max_starts": MAX_STARTS,
            "project_url": project_url,
            "info": {k: v for k, v in info.items() if k != "path"},
            "start": str(START),
            "start_sha256": sha(START),
            "start_lock": str(lock),
            "parent_start": str(PARENT_START),
            "start_dna": dna_tag,
            "family": "NEW_KEEP_try1_columns_zerolamp_nolava",
            "plate_library_lock_sha": PLATE_LIBRARY,
            "main_lock_sha": MAIN_LOCK,
            "model": MODEL,
            "model_rationale": (
                "Quality REQUIRED — CLEAN LIGHT / lava-desk remint class "
                "(locked Showrunner brief PART04_NEXT_PLATE_05_COLUMNS_NO_LAVA.md)"
            ),
            "seedance": "banned",
            "fast": "banned",
            "when": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "auth": auth,
            "paint": "banned",
            "assemble": False,
            "parent_keeps": {"06": "KEEP", "09b": "KEEP", "11": "KEEP", "11b": "KEEP"},
            "out_of_scope": [
                "10_family_before_weight",
                "06_explorer_leaves_gap",
                "09b_risk_hold",
                "11_publish_gaps",
                "11b_wait_and_hunt",
                "assemble",
            ],
            "stop_rule": (
                "Max 2 Quality starts this NEW DNA; invent lamp/lava/molten bead → SELF_REJECT; "
                "both fail → STOP_TO_COS"
            ),
            "brief_lock": "PART04_NEXT_PLATE_05_COLUMNS_NO_LAVA.md",
        }
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(out, indent=2) + "\n")
        print(json.dumps(out, indent=2), flush=True)
        if "/project/" not in project_url:
            raise SystemExit("no project url after submit")


if __name__ == "__main__":
    main()
