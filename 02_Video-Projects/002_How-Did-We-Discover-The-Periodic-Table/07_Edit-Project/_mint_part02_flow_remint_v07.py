#!/usr/bin/env python3
"""Mint HOS 002 Part 02 remint v07 — all scenery plates as real Flow Veo Fast.

No Ken Burns. No Gemini prepaid (dry). Explorer once on plate 05.
Hard rejects: vessel fire, desk-toy miniature piano.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))

import orbit_flow_veo_ui as flow  # noqa: E402
import orbit_gemini_veo as veo  # noqa: E402

PROJ = Path(__file__).resolve().parents[1]
PLATES_JSON = PROJ / "07_Edit-Project/parts/part-02_plates_v04.json"
RAW = PROJ / "04_Generated-Clips/part02/raw/v07_fast"
META = PROJ / "07_Edit-Project/part02_remint_flow_v07_meta.json"
MODEL = "Veo 3.1 - Fast"
PROFILE = Path(
    os.environ.get(
        "ORBIT_FLOW_PROFILE",
        str(Path.home() / ".playwright-hos-flow-profile"),
    )
)
STYLE = (
    "History of Science locked look: premium Animistry-class 3D cartoon, warm "
    "cinematic light, scholar writing-study world. Not photoreal. Not live-action. "
    "Silent picture. No readable text, logos, or UI. No Orbit orange robot. "
    "Continuous real camera and object motion the whole clip. Never a still with "
    "Ken Burns. Never desk-toy miniature piano. Never jars or pots on fire."
)

# Chapter + teach cards also reminted as motion world plates (no center stamps).
CHAPTER_PROMPT = (
    "Premium Animistry-class 3D cartoon: warm oak scholar writing desk under soft "
    "window light. A neat stack of blank cream specimen cards slowly fans open. "
    "Continuous gentle camera drift. Silent. No readable text. No fire. No jars. "
    "No Orbit. No people."
)
TEACH_PROMPT = (
    "Premium Animistry-class 3D cartoon writing study: three blank cream cousin-cards "
    "glow softly in a row on oak, then a fourth blank card slides in and breaks the "
    "tidy rhyme. Continuous motion. Silent. No readable text. No fire. No jars. No Orbit."
)


def dest_for(pid: str) -> Path:
    return RAW / f"{pid}_v07.mp4"


def prompt_for(plate: dict) -> str:
    kind = plate.get("kind")
    if kind == "chapter_card" or plate["id"] == "01_chapter_card":
        return f"{STYLE} {CHAPTER_PROMPT}"
    if kind == "teach_card" or plate["id"] == "04_triad_cards":
        return f"{STYLE} {TEACH_PROMPT}"
    return f"{STYLE} {plate['prompt']}"


def main() -> None:
    only = set(sys.argv[1:]) if len(sys.argv) > 1 else None
    plates = json.loads(PLATES_JSON.read_text())["plates"]
    RAW.mkdir(parents=True, exist_ok=True)
    meta: dict = {"engine": "flow-ui", "model": MODEL, "raw": str(RAW), "plates": []}
    if META.exists():
        try:
            meta = json.loads(META.read_text())
        except Exception:
            pass
    by_id = {p["id"]: p for p in meta.get("plates", []) if "id" in p}
    profile = flow.profile_path(PROFILE)
    print(f"Flow remint Part02 profile={profile} model={MODEL}", flush=True)

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        ctx, page = flow.launch_context(p, headed=True, profile=profile)
        try:
            page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
            page.wait_for_timeout(2500)
            flow.dismiss_banners(page)
            if not flow.looks_logged_in(page):
                raise SystemExit(
                    "STOP: Flow not logged in. Do not Ken-Burns. "
                    "Re-auth: python3 04_Audio/tools/orbit_flow_veo_ui.py --login"
                )
            for i, plate in enumerate(plates):
                pid = plate["id"]
                if only and pid not in only:
                    continue
                dest = dest_for(pid)
                if veo.already_done(dest, min_bytes=400_000):
                    print(f"  skip {dest.name}", flush=True)
                    by_id[pid] = {"id": pid, "status": "exists", "out": str(dest)}
                    continue
                prompt = prompt_for(plate)
                print(f"\n=== Fast T2V {pid} ({i+1}/{len(plates)}) ===", flush=True)
                try:
                    info = flow.generate_clip(
                        page,
                        prompt,
                        dest,
                        model=MODEL,
                        start_frame=None,
                        scenery_only=True,
                        reuse_project=False,
                        attempts=2,
                        timeout_s=700,
                    )
                except Exception as e:
                    by_id[pid] = {"id": pid, "status": "fail", "error": str(e)[:500]}
                    meta["plates"] = list(by_id.values())
                    META.write_text(json.dumps(meta, indent=2))
                    raise SystemExit(f"STOP: Flow failed on {pid}: {e}") from e
                veo.strip_audio(dest)
                if not dest.exists() or dest.stat().st_size < 400_000:
                    raise SystemExit(f"STOP: download missing/small {dest}")
                by_id[pid] = {"id": pid, "status": "ok", "out": str(dest), **info}
                meta["plates"] = list(by_id.values())
                META.write_text(json.dumps(meta, indent=2))
                print(f"  SAVED {dest.name} bytes={dest.stat().st_size}", flush=True)
        finally:
            ctx.close()
    print("OK part 02 remint mint finished", flush=True)


if __name__ == "__main__":
    main()
