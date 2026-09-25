#!/usr/bin/env python3
"""10_family_before_weight try1 — BOARDTOP_DAY_NOFIXTURE DNA on live Mini CDP.

Parent: v21 FAMILY FIRST ~t108 lava drip under bulb.
Unlocked by: 05_columns_families try2B UAT KEEP sha 49437e7e…
KEEP hold: 06 / 09b / 11 / 11b / 05. No assemble this run.
Model: Veo 3.1 - Quality REQUIRED. Fast banned. Seedance banned.
DNA: BOARDTOP_DAY_NOFIXTURE — prefer try2B cards-only lesson; no room for practical lamp invent.

Auth: Mini CDP benoats@googlemail.com ULTRA. STOP on passkey.
Plate-library 4b8ed25. Max 2 Quality starts this DNA then STOP_TO_COS.
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
REF = PROJ / "04_Generated-Clips/part04/refs/v22_dna_try2_10"
PARENT_START = (
    PROJ
    / "04_Generated-Clips/part04/refs/v21_lava_remint_starts/10_family_before_weight_start_v21_from_v20_t04.jpg"
)
START = REF / "10_family_before_weight_start_v22_try1_active.jpg"
# Lead with try2B-style cards-only (05 KEEP lesson). B = even tighter stacks.
LOCK_A = REF / "10_family_before_weight_start_v22_try1_BOARDTOP_CARDS_ONLY.jpg"
LOCK_B = REF / "10_family_before_weight_start_v22_try1_BOARDTOP_STACKS_TIGHT.jpg"
QA_DIR = PROJ / "07_Edit-Project/_qa_part04_v22_plates_try1_10"
START_COUNTER = QA_DIR / "start_counter.json"
MODEL = os.environ.get("ORBIT_FLOW_VEO_MODEL") or "Veo 3.1 - Quality"
REQUIRED_EMAIL = "benoats@googlemail.com"
MAX_STARTS = 2
OUT_A = PROJ / "07_Edit-Project/_qa_part04_v22_flow/submit_10_family_before_weight_try1.json"
OUT_B = PROJ / "07_Edit-Project/_qa_part04_v22_flow/submit_10_family_before_weight_try1B.json"
PLATE_LIBRARY = "4b8ed25"
MAIN_LOCK = "3bc0414"
BRIEF_LOCK = "PART04_NEXT_PLATE_10_TRY1_BOARDTOP_DNA.md"
KEEP_05_SHA = "49437e7e4004c224b021409e15ebb50fb06b74737adfe2b6c0bc0a61bfae8caa"

PROMPT = (
    "IMAGE-TO-VIDEO of the attached start frame. Animate THIS exact beat only. "
    "Plate 10_family_before_weight try1 — FAMILY FIRST remint after v21 lava FAIL ~t108 "
    "(Veo 3.1 Quality REQUIRED; DNA family BOARDTOP_DAY_NOFIXTURE — same KEEP lessons as "
    "05_columns_families try2B; NOT side-desk practical lamp). "
    "Finished cinematic stylised 3D 1869 chemist BOARDTOP (Animistry-class polish). "
    "NOT flat unfinished vlog vector. NOT 2D cutouts. NOT paint. NOT Ken Burns. "
    "CAMERA (HARD): steep / boardtop — cream element CARDS fill the frame. "
    "Desk wood is a flat plane under the cards; daylight / flat sky bounce ONLY. "
    "NO deep room volume that can host a lamp niche, NO side-desk lamp pocket, "
    "NO gooseneck, NO brass desk lamp anywhere. "
    "Hero action: in ONE column, TWO cream WRITTEN element cards SWAP ORDER "
    "(family wins over messy weight — FAMILY FIRST beat). Sparse readable marks OK "
    "(F/Na/Mg/H/C/O/N). Paper-layer stack edges; continuous gentle swap/settle — "
    "LOCKED boardtop tripod. "
    "CLEAN LIGHT / DAYLIGHT ONLY (HARD for full 8s): soft DAYLIGHT / flat sky bounce ONLY. "
    "THERE IS NO PRACTICAL LAMP ANYWHERE — zero gooseneck, zero lampshade, zero shade-cup "
    "(open or closed), zero brass desk lamp, zero wall sconce, zero candle, zero chandelier, "
    "zero torchiere, zero underside bulb look-in, zero molten bead, zero lava drip. "
    "HARD composition: LEFT THIRD + UPPER FIFTH stay EMPTY OF FIXTURES for the whole clip "
    "(no brass, no shade, no stem walking in). Do NOT invent any lamp/fixture mid-clip. "
    "HOUSE HARD FAIL forever (t0–t8): lava drip, molten bead, liquid light drip, open shade-cup, "
    "underside bulb, practical lamp invent, unfinished blank flat cards, model-town, "
    "Explorer, paint, Ken Burns. "
    "ACTION: continuous gentle two-card swap in one family column; dust motes in daylight; "
    "LOCKED BOARDTOP — no pan/zoom/tilt that opens room volume for a lamp. "
    "Continuous real Veo motion. Silent. Paint banned. Seedance banned. Fast banned. "
    f"Plate-library lock {PLATE_LIBRARY}. Main lock {MAIN_LOCK}. "
    "NEW try1 DNA: BOARDTOP_DAY_NOFIXTURE join from 05 try2B KEEP — NOT v21 lamp-desk."
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
                "plate": "10_family_before_weight",
                "try": 1,
                "which": which,
                "starts": n,
                "max_starts": MAX_STARTS,
                "dna_family": "BOARDTOP_DAY_NOFIXTURE",
                "dna": dna,
                "model": MODEL,
                "parent_start": str(PARENT_START),
                "unlocked_by_05_try2B_sha": KEEP_05_SHA,
                "when": time.strftime("%Y-%m-%dT%H:%M:%S"),
            },
            indent=2,
        )
        + "\n"
    )
    if n > MAX_STARTS:
        raise SystemExit(
            f"STOP_TO_COS: try1 BOARDTOP DNA already used {n - 1}/{MAX_STARTS} Quality starts — do not mint further"
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
    which = (os.environ.get("HOS_10_TRY1_START") or "A").upper().strip()
    if which == "B":
        lock = LOCK_B
        out_path = OUT_B
        dna_tag = (
            "try1B BOARDTOP_DAY_NOFIXTURE stacks-tight: hanging F/Na/Mg + stacks fill frame; "
            "daylight bounce ONLY; no room volume for practical lamp; two cards swap in one column; "
            "LEFT THIRD + UPPER FIFTH fixture-empty; LOCKED BOARDTOP; "
            f"plate-library {PLATE_LIBRARY}; main {MAIN_LOCK}; NOT v21 lamp-desk; "
            "paint banned; Seedance banned; Fast banned; Quality REQUIRED"
        )
    else:
        which = "A"
        lock = LOCK_A
        out_path = OUT_A
        dna_tag = (
            "try1A BOARDTOP_DAY_NOFIXTURE cards-only (05 try2B KEEP lesson): cream cards fill frame; "
            "daylight bounce ONLY; no furniture-lamp volume; two cards swap order in one family column; "
            "LEFT THIRD + UPPER FIFTH fixture-empty; LOCKED BOARDTOP; "
            f"plate-library {PLATE_LIBRARY}; main {MAIN_LOCK}; NOT v21 lamp-desk; "
            "paint banned; Seedance banned; Fast banned; Quality REQUIRED"
        )

    if not lock.exists():
        raise SystemExit(f"ABORT: missing try1 start {lock}")
    START.write_bytes(lock.read_bytes())
    print(f"synced ACTIVE start <- {lock.name}", flush=True)
    if sha(START) != sha(lock):
        raise SystemExit("ABORT: active start != chosen try1 lock")

    for need in (
        "BOARDTOP",
        "DAYLIGHT",
        "NO PRACTICAL LAMP",
        "shade-cup",
        "LEFT THIRD",
        "UPPER FIFTH",
        "molten bead",
        "lava drip",
        "SWAP",
        "FAMILY",
        "readable",
        PLATE_LIBRARY,
        MAIN_LOCK,
        "LOCKED BOARDTOP",
        "Seedance",
        "Quality",
        "try2B",
    ):
        if need.lower() not in PROMPT.lower():
            raise SystemExit(f"ABORT: prompt missing {need}")

    if "Quality" not in MODEL:
        raise SystemExit("ABORT: locked brief requires Veo 3.1 Quality for 10 try1 (BOARDTOP)")
    if "Seedance" in MODEL or "seedance" in MODEL.lower():
        raise SystemExit("ABORT: Seedance banned")
    if "Fast" in MODEL and "Quality" not in MODEL:
        raise SystemExit("ABORT: Fast banned — Quality REQUIRED")

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

        tmp = Path(f"/tmp/hos_v22_10_try1{which}_stub.mp4")
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
            "plate": "10_family_before_weight",
            "try": f"1{which}" if which != "A" else 1,
            "start_n": start_n,
            "max_starts": MAX_STARTS,
            "dna_family": "BOARDTOP_DAY_NOFIXTURE",
            "project_url": project_url,
            "info": {k: v for k, v in info.items() if k != "path"},
            "start": str(START),
            "start_sha256": sha(START),
            "start_lock": str(lock),
            "parent_start": str(PARENT_START),
            "start_dna": dna_tag,
            "family": "BOARDTOP_DAY_NOFIXTURE_join_05_try2B",
            "plate_library_lock_sha": PLATE_LIBRARY,
            "main_lock_sha": MAIN_LOCK,
            "model": MODEL,
            "model_rationale": (
                "Quality REQUIRED — BOARDTOP_DAY_NOFIXTURE CLEAN LIGHT remint "
                f"(locked Showrunner brief {BRIEF_LOCK}; join 05 try2B KEEP {KEEP_05_SHA[:12]}…)"
            ),
            "seedance": "banned",
            "fast": "banned",
            "when": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "auth": auth,
            "paint": "banned",
            "assemble": False,
            "parent_keeps": {
                "05": f"KEEP {KEEP_05_SHA}",
                "06": "KEEP",
                "09b": "KEEP",
                "11": "KEEP",
                "11b": "KEEP",
            },
            "out_of_scope": [
                "05_columns_families",
                "06_explorer_leaves_gap",
                "09b_risk_hold",
                "11_publish_gaps",
                "11b_wait_and_hunt",
                "assemble",
            ],
            "stop_rule": (
                "Max 2 Quality starts this BOARDTOP_DAY_NOFIXTURE DNA; "
                "invent lamp/lava/molten bead → SELF_REJECT; both fail → STOP_TO_COS"
            ),
            "brief_lock": BRIEF_LOCK,
            "banned_dna": "v21 lamp-desk with underside bulb / lava drip",
        }
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(out, indent=2) + "\n")
        print(json.dumps(out, indent=2), flush=True)
        if "/project/" not in project_url:
            raise SystemExit("no project url after submit")


if __name__ == "__main__":
    main()
