#!/usr/bin/env python3
"""Submit one Part 05 Flow cycle (max 2 T2V Quality starts).

Usage:
  python3 _submit_part05_flow_cycle.py --jobs cycle.json

Jobs JSON:
  {"cycle": "v01_c7_...", "jobs": [{plate, try, which, prompt, note, out?}]}
"""
from __future__ import annotations

import argparse
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
PLATE_LIBRARY = "4b8ed25"

CLEAN = (
    "CLEAN LIGHT (HARD for full 8s): THERE IS NO PRACTICAL TABLE LAMP — "
    "zero shade, zero bulb, zero shade-cup, zero brass desk lamp. "
    "Daytime window bounce ONLY. "
    "ZERO lava, ZERO molten bead, ZERO orange melt, ZERO fire, ZERO flame, ZERO sparks. "
    "ZERO fire-pits cut into wood. ZERO glowing trenches in a desk. "
    "ZERO orange or amber light under a card or in a hole. "
    "Vacant glow is cool white or pale gold rim only. "
    "No Explorer. No Orbit. No twins. No model-town / yellow house-blocks. No paint. "
    "No flasks. No mortar. No HUD paragraphs. No full element names spelled out. "
    "Continuous real Veo motion the WHOLE 8 seconds — never freeze, never Ken Burns still. "
    "Silent. Plate-library lock 4b8ed25. Animistry-class stylised 3D cartoon. "
    "HARD FORBIDDEN COMPOSITION (P04 Ben reject): do NOT show a wide honey-wood desk "
    "with a full moon in the LEFT window, purple/green flasks, white mortar, stacked "
    "papers, three blank cards on the desk, desk-lamp on the RIGHT, clay pots, and a "
    "faint empty chair back. That exact still-life is BANNED for the full 8 seconds. "
)


def bump_start_counter(cycle: str, plate: str) -> int:
    QA_DIR.mkdir(parents=True, exist_ok=True)
    n = 0
    if START_COUNTER.exists():
        try:
            prev = json.loads(START_COUNTER.read_text())
            if prev.get("cycle") == cycle:
                n = int(prev.get("starts", 0))
        except Exception:
            n = 0
    n += 1
    START_COUNTER.write_text(
        json.dumps(
            {
                "cycle": cycle,
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
    print(f"start_counter={n}/{MAX_STARTS} plate={plate} cycle={cycle}", flush=True)
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


def submit_one(page, cycle: str, job: dict) -> dict:
    prompt = job["prompt"]
    if not prompt.rstrip().endswith(CLEAN[-80:]):
        prompt = prompt.rstrip() + " " + CLEAN
        job["prompt"] = prompt
    for need in ("TEXT-TO-VIDEO", "8s", "lava", "Ken Burns", "4b8ed25"):
        if need.lower() not in prompt.lower():
            raise SystemExit(f"ABORT: prompt missing {need}")
    start_n = bump_start_counter(cycle, job["plate"])
    tmp = Path(f"/tmp/hos_p05_{job['plate']}_{job['try']}_stub.mp4")
    if tmp.exists():
        tmp.unlink()
    info: dict = {}
    try:
        info = flow.generate_clip(
            page,
            prompt,
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
    out_path = Path(job["out"]) if not isinstance(job.get("out"), Path) else job["out"]
    if not str(out_path).startswith("/"):
        out_path = QA_DIR / job["out"]
    payload = {
        "plate": job["plate"],
        "try": job["try"],
        "which": job["which"],
        "start_n": start_n,
        "max_starts": MAX_STARTS,
        "cycle": cycle,
        "project_url": project_url,
        "info": {k: v for k, v in info.items() if k != "path"},
        "start_frame": None,
        "mode": "T2V",
        "model": MODEL,
        "when": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "paint": "banned",
        "assemble": False,
        "note": job.get("note", ""),
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2), flush=True)
    if "/project/" not in project_url:
        raise SystemExit(f"no project url after submit ({job['plate']})")
    return payload


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=Path, required=True)
    args = ap.parse_args()
    spec = json.loads(args.jobs.read_text())
    cycle = spec["cycle"]
    jobs = spec["jobs"]
    if not (1 <= len(jobs) <= MAX_STARTS):
        raise SystemExit(f"need 1–{MAX_STARTS} jobs, got {len(jobs)}")
    for job in jobs:
        job.setdefault("out", f"submit_{job['plate']}_{job['try']}.json")
        if "4b8ed25" not in job["prompt"]:
            job["prompt"] = job["prompt"].rstrip() + f" Plate-library lock {PLATE_LIBRARY}."
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
        print(f"auth={auth} cycle={cycle}", flush=True)
        urls = []
        for job in jobs:
            try:
                page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=180000)
                time.sleep(2)
            except Exception:
                pass
            urls.append(submit_one(page, cycle, job).get("project_url"))
            time.sleep(2)
        print(json.dumps({"submitted": urls, "cycle": cycle}, indent=2), flush=True)


if __name__ == "__main__":
    main()
