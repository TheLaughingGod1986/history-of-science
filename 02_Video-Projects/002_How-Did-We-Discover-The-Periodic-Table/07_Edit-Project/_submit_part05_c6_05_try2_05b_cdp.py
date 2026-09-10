#!/usr/bin/env python3
"""Part 05 cycle v01_c6 — remint 05 scandium (ONE card) + 05b germanium overhead.

05 try1 FAIL: three cards stacked in one slot + full-word Scandium.
try2: same SIDE DNA once — ONE card, sparse Sc only.

05b: OVERHEAD second gap fills. Distinct from SIDE drop.

Max 2 starts. Auth Mini CDP Ultra. Paint banned. T2V Quality.
No Explorer. No desk fire-trenches. Silver not lava.
"""
from __future__ import annotations

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
QA_DIR = PROJ / "07_Edit-Project/_qa_part05_v01_flow"
START_COUNTER = QA_DIR / "start_counter.json"
MODEL = os.environ.get("ORBIT_FLOW_VEO_MODEL") or "Veo 3.1 - Quality"
REQUIRED_EMAIL = "benoats@googlemail.com"
MAX_STARTS = 2
CYCLE = "v01_c6_05_try2_05b"
PLATE_LIBRARY = "4b8ed25"

BANNED_STILL = (
    "HARD FORBIDDEN COMPOSITION (P04 Ben reject): do NOT show a wide honey-wood desk "
    "with a full moon in the LEFT window, purple/green flasks, white mortar, stacked "
    "papers, three blank cards on the desk, desk-lamp on the RIGHT, clay pots, and a "
    "faint empty chair back. That exact still-life is BANNED for the full 8 seconds. "
)

CLEAN = (
    "CLEAN LIGHT (HARD for full 8s): THERE IS NO PRACTICAL TABLE LAMP — "
    "zero shade, zero bulb, zero shade-cup, zero brass desk lamp. "
    "Daytime window bounce ONLY. "
    "ZERO lava, ZERO molten bead, ZERO orange melt, ZERO fire, ZERO flame, ZERO sparks. "
    "ZERO fire-pits cut into wood. ZERO glowing trenches in a desk. "
    "No Explorer. No Orbit. No twins. No model-town / yellow house-blocks. No paint. "
    "No flasks. No mortar. No HUD paragraphs. No full element names spelled out. "
    "Continuous real Veo motion the WHOLE 8 seconds — never freeze, never Ken Burns still. "
    f"Silent. Plate-library lock {PLATE_LIBRARY}. Animistry-class stylised 3D cartoon. "
    + BANNED_STILL
)

PROMPT_05 = (
    "TEXT-TO-VIDEO. Plate 05_scandium_fills try2 — Scandium. ONE CARD ONLY. "
    "VO beat: scandium takes a seat. "
    "ONE continuous 8s take. SIDE three-quarter of a cream-card WALL CHART on honey wood. "
    "EXACTLY ONE cream card drops ONCE into ONE glowing vacant card-space, then rests. "
    "FORBIDDEN: a second card, a third card, stacking, looping drops, cards piling up. "
    "Sparse mark on the card: only the two letters Sc — never the word Scandium. "
    "Empty seat = a blank card-sized cell on the wall, solid wood behind. "
    "NOT a hole, NOT a trench, NOT a fire-pit. No person. No lamp. "
    "Continuous single drop + settle. Distinct from the Ga MACRO fill. "
    + CLEAN
)

PROMPT_05B = (
    "TEXT-TO-VIDEO. Plate 05b_germanium_verdict try1 — Germanium. "
    "VO beat: germanium, the verdict. "
    "ONE continuous 8s take. STRICT OVERHEAD looking down on a cream-card GRID. "
    "A SECOND glowing vacant cell fills as ONE cream card seats from above; vacant glow settles like a verdict. "
    "Sparse mark Ge only — never the word Germanium. "
    "NOT a side-angle wall. NOT a side drop. Camera is TOP-DOWN. "
    "Empty cell = blank card space, solid wood behind, never a fire-pit. "
    "Exactly one card seats. Continuous. No person. No lamp. "
    + CLEAN
)

JOBS = [
    {
        "plate": "05_scandium_fills",
        "try": "2_v01",
        "which": "side_one_card_sc",
        "prompt": PROMPT_05,
        "out": QA_DIR / "submit_05_scandium_fills_try2.json",
        "note": "ONE Sc card drop; no stacking; no word Scandium",
    },
    {
        "plate": "05b_germanium_verdict",
        "try": "1_v01",
        "which": "overhead_ge_verdict",
        "prompt": PROMPT_05B,
        "out": QA_DIR / "submit_05b_germanium_verdict_try1.json",
        "note": "OVERHEAD Ge fill; distinct from SIDE scandium",
    },
]


def bump_start_counter(plate: str) -> int:
    QA_DIR.mkdir(parents=True, exist_ok=True)
    n = 0
    if START_COUNTER.exists():
        try:
            prev = json.loads(START_COUNTER.read_text())
            if prev.get("cycle") == CYCLE:
                n = int(prev.get("starts", 0))
        except Exception:
            n = 0
    n += 1
    START_COUNTER.write_text(
        json.dumps(
            {
                "cycle": CYCLE,
                "plate": plate,
                "starts": n,
                "max_starts": MAX_STARTS,
                "when": time.strftime("%Y-%m-%dT%H:%M:%S"),
            },
            indent=2,
        )
        + "\n"
    )
    if n > MAX_STARTS:
        raise SystemExit(f"STOP_TO_COS: already used {n - 1}/{MAX_STARTS} Flow starts")
    print(f"start_counter={n}/{MAX_STARTS} plate={plate} cycle={CYCLE}", flush=True)
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


def submit_one(page, job: dict) -> dict:
    for need in ("TEXT-TO-VIDEO", "8s", "lava", "Ken Burns", "4b8ed25"):
        if need.lower() not in job["prompt"].lower():
            raise SystemExit(f"ABORT: prompt missing {need}")
    start_n = bump_start_counter(job["plate"])
    tmp = Path(f"/tmp/hos_p05_{job['plate']}_{job['try']}_stub.mp4")
    if tmp.exists():
        tmp.unlink()
    info: dict = {}
    try:
        info = flow.generate_clip(
            page,
            job["prompt"],
            tmp,
            model=MODEL,
            timeout_s=70,
            attempts=1,
            scenery_only=True,
        )
    except Exception as e:
        info = {
            "error": str(e),
            "project_url": getattr(page, "_orbit_flow_project_url", None) or (page.url or ""),
        }
        print(f"submit note ({job['plate']}): {e}", flush=True)

    project_url = (
        info.get("project_url")
        or info.get("url")
        or getattr(page, "_orbit_flow_project_url", None)
        or page.url
        or ""
    )
    project_url = str(project_url).split("?")[0].rstrip("/")
    out = {
        "plate": job["plate"],
        "try": job["try"],
        "which": job["which"],
        "start_n": start_n,
        "max_starts": MAX_STARTS,
        "cycle": CYCLE,
        "project_url": project_url,
        "info": {k: v for k, v in info.items() if k != "path"},
        "start_frame": None,
        "mode": "T2V",
        "model": MODEL,
        "when": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "paint": "banned",
        "assemble": False,
        "note": job["note"],
    }
    job["out"].parent.mkdir(parents=True, exist_ok=True)
    job["out"].write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2), flush=True)
    if "/project/" not in project_url:
        raise SystemExit(f"no project url after submit ({job['plate']})")
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
        urls = []
        for job in JOBS:
            try:
                page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=180000)
                time.sleep(2)
            except Exception:
                pass
            urls.append(submit_one(page, job).get("project_url"))
            time.sleep(2)
        print(json.dumps({"submitted": urls, "next": "harvest 05 try2 + 05b → plate UAT"}, indent=2), flush=True)


if __name__ == "__main__":
    main()
