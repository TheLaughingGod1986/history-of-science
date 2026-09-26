#!/usr/bin/env python3
"""HOS 003 Part 05 — mint ONLY 01_chapter_new_seeing via Mini Flow CDP (HOS one_create path)."""
from __future__ import annotations

import importlib.util
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
EDIT = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))

import orbit_flow_veo_ui as flow  # noqa: E402
import orbit_gemini_veo as veo  # noqa: E402

# Load proven HOS mint helpers from Part 04 Batch A script
_spec = importlib.util.spec_from_file_location(
    "hos_mint04", EDIT / "_mint_part04_batch_a.py"
)
m = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(m)

ACCOUNT = "benoats@googlemail.com"
MODEL = "Veo 3.1 - Quality"
PROJECT = os.environ.get(
    "HOS_003_P05_FLOW_PROJECT",
    "https://flow.google.com/u/0/project/02ce23ba-3f6d-49ee-8177-67af2d9a1166",
)
CDP = os.environ.get("HOS_003_FLOW_CDP", "http://127.0.0.1:9222")
CLIP_DIR = (
    REPO
    / "02_Video-Projects"
    / "003_Invisible-Bones-X-Rays"
    / "04_Generated-Clips"
    / "part05"
)
QA_DIR = EDIT / "_qa_part05_batch_a"

PLATE = "01_chapter_new_seeing"
PROMPT = (
    "Animistry 3D. MUTE-TEST: soft settle from Würzburg lab glow into teach space "
    "must read as chapter open for A New Kind of Seeing (sound OFF). Continuous. Silent. "
    "No Explorer. HARD REJECT: Orbit, slogan bumper. HARD FAIL — no DNA helix / double helix / "
    "spiral DNA prop / Periodic DNA desk (incl. glowing yellow helix in palm or behind Explorer); "
    "never open Create with `Same DNA soft background`; prefer `Same Würzburg lab`. "
    "Readable Animistry cartoon faces with eyes and nose when any person appears — "
    "HARD FAIL blank mannequin ovals. No DNA helix."
)
MUTE = "Soft settle lab→teach = chapter open (sound OFF)"


def main() -> None:
    if PROMPT.lstrip().lower().startswith("same dna soft background"):
        raise SystemExit("STOP: banned DNA soft background opener")

    # Retarget Part-04 helpers to Part-05 dirs/model
    m.CLIP_DIR = CLIP_DIR
    m.QA_DIR = QA_DIR
    m.MODEL = MODEL
    m.ACCOUNT = ACCOUNT
    CLIP_DIR.mkdir(parents=True, exist_ok=True)
    QA_DIR.mkdir(parents=True, exist_ok=True)
    dest = CLIP_DIR / f"{PLATE}_v01.mp4"
    if dest.exists() and dest.stat().st_size > 150_000:
        print(f"ALREADY {dest} sha={m.sha256_file(dest)}", flush=True)
        return

    from playwright.sync_api import sync_playwright

    print(f"cdp attach {CDP}", flush=True)
    print(f"project {PROJECT}", flush=True)
    print(f"model {MODEL} account {ACCOUNT}", flush=True)

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        ctx = browser.contexts[0]
        page = None
        for pg in ctx.pages:
            if "flow.google.com" in (pg.url or "") and "/project/" in (pg.url or ""):
                page = pg
                break
        if page is None:
            for pg in ctx.pages:
                if "flow.google.com" in (pg.url or ""):
                    page = pg
                    break
        if page is None:
            page = ctx.new_page()
        page.bring_to_front()
        if "/project/" not in (page.url or ""):
            page.goto(PROJECT, wait_until="domcontentloaded", timeout=120_000)
            flow.settle_after_nav(page, wait_ms=2000)
        else:
            flow.settle_after_nav(page, wait_ms=800)
        flow.dismiss_banners(page)
        try:
            tb = page.get_by_role("textbox", name="Editable text")
            if tb.count():
                tb.first.click(timeout=3000)
                page.keyboard.press("Meta+A")
                page.keyboard.type("HOS 003 Part 05 Batch A", delay=8)
                page.keyboard.press("Enter")
                page.wait_for_timeout(500)
        except Exception as e:
            print(f"  rename warn: {e}", flush=True)
        print(f"url={page.url}", flush=True)
        print(
            f"logged_in={flow.looks_logged_in(page)} editor={flow.editor_usable(page)}",
            flush=True,
        )
        if not flow.looks_logged_in(page):
            raise SystemExit("STOP: Flow not logged in — need benoats@googlemail.com ULTRA")

        (QA_DIR / "01_SUBMITTED.json").write_text(
            json.dumps(
                {
                    "plate": PLATE,
                    "status": "about_to_submit",
                    "model": MODEL,
                    "account": ACCOUNT,
                    "project": page.url,
                    "ts": datetime.now(timezone.utc).isoformat(),
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        print("SUBMITTING Create for 01_chapter_new_seeing…", flush=True)
        baked = m.bake_prompt(PROMPT)
        unpaid_retry = False
        try:
            meta = m.one_create(page, baked, dest, int(os.environ.get("HOS_FLOW_TIMEOUT_S", "900")))
        except RuntimeError as e:
            if str(e) != "UNPAID_FAIL":
                raise
            unpaid_retry = True
            print("  UNPAID — ONE refresh retry…", flush=True)
            page.reload(wait_until="domcontentloaded", timeout=120_000)
            flow.settle_after_nav(page, wait_ms=2000)
            flow.dismiss_banners(page)
            m.abort_guards(page, "post-refresh")
            meta = m.one_create(page, baked, dest, int(os.environ.get("HOS_FLOW_TIMEOUT_S", "900")))

        # Mark submitted mid-flight file already written; update
        (QA_DIR / "01_SUBMITTED.json").write_text(
            json.dumps(
                {
                    "plate": PLATE,
                    "status": "submitted_running_or_landed",
                    "model": MODEL,
                    "account": ACCOUNT,
                    "project": page.url,
                    "unpaid_retry": unpaid_retry,
                    "ts": datetime.now(timezone.utc).isoformat(),
                },
                indent=2,
            ),
            encoding="utf-8",
        )

        if not dest.exists() or dest.stat().st_size < 150_000:
            raise SystemExit(f"STOP: dest missing/small {dest}")
        try:
            veo.strip_audio(dest)
        except Exception as e:
            print(f"  strip_audio warn: {e}", flush=True)
        dur = m.probe_dur(dest)
        if dur < 6.0 or dur > 12.0:
            raise SystemExit(f"STOP: unexpected duration {dur:.2f}s")
        m.extract_qa_frames(dest, PLATE)
        # extract_qa_frames names *_v01_* under QA_DIR using plate id — Part04 helper uses plate arg
        report = {
            "plate": PLATE,
            "version": "v01",
            "path": str(dest),
            "bytes": dest.stat().st_size,
            "sha256": m.sha256_file(dest),
            "duration_s": dur,
            "model": MODEL,
            "selected_model": meta.get("selected_model") if isinstance(meta, dict) else None,
            "mute_note": MUTE,
            "account": ACCOUNT,
            "project": page.url,
            "unpaid_refresh_retry": unpaid_retry,
            "assemble": "CLOSED",
            "ts": datetime.now(timezone.utc).isoformat(),
        }
        (QA_DIR / f"{PLATE}_v01_mint.json").write_text(
            json.dumps(report, indent=2), encoding="utf-8"
        )
        print("LANDED", json.dumps(report, indent=2), flush=True)


if __name__ == "__main__":
    main()
