#!/usr/bin/env python3
"""Resume harvest of in-flight P05 plate 01 — do NOT re-Create."""
from __future__ import annotations
import importlib.util, json, sys, time, re
from datetime import datetime, timezone
from pathlib import Path

REPO = Path("/Users/benjaminoats/YouTube/History Of Science")
EDIT = REPO / "02_Video-Projects/003_Invisible-Bones-X-Rays/07_Edit-Project"
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))
import orbit_flow_veo_ui as flow
import orbit_gemini_veo as veo

spec = importlib.util.spec_from_file_location("hos_mint04", EDIT / "_mint_part04_batch_a.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

QA = EDIT / "_qa_part05_batch_a"
CLIP_DIR = REPO / "02_Video-Projects/003_Invisible-Bones-X-Rays/04_Generated-Clips/part05"
CLIP_DIR.mkdir(parents=True, exist_ok=True)
m.CLIP_DIR = CLIP_DIR
m.QA_DIR = QA
m.MODEL = "Veo 3.1 - Quality"
m.ACCOUNT = "benoats@googlemail.com"
PROJECT = "https://flow.google.com/u/0/project/02ce23ba-3f6d-49ee-8177-67af2d9a1166"
DEST = CLIP_DIR / "01_chapter_new_seeing_v01.mp4"
PLATE = "01_chapter_new_seeing"
CDP = "http://127.0.0.1:9222"

from playwright.sync_api import sync_playwright

def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        ctx = browser.contexts[0]
        page = next(pg for pg in ctx.pages if "flow.google.com" in (pg.url or ""))
        page.bring_to_front()
        page.goto(PROJECT, wait_until="domcontentloaded", timeout=120_000)
        flow.settle_after_nav(page, wait_ms=1500)
        flow.dismiss_banners(page)
        print(f"resume {page.url}", flush=True)
        # Confirm still googlemail
        aria = page.evaluate("""() => {
          const a = document.querySelector('a[aria-label*="Google Account"]');
          return a && a.getAttribute('aria-label');
        }""")
        print(f"chip {aria}", flush=True)
        if not aria or "googlemail" not in aria.lower():
            raise SystemExit(f"STOP: wrong account {aria}")

        before = set()  # harvest any ready media
        t0 = time.time()
        last = ""
        while time.time() - t0 < 900:
            flow.dismiss_banners(page)
            body = page.locator("body").inner_text(timeout=8000)
            pcts = [int(x) for x in re.findall(r"(\d{1,3})%", body)]
            line = f"wait {int(time.time()-t0)}s pct={pcts[-5:] if pcts else None}"
            if line != last:
                print(line, flush=True)
                last = line
            page.screenshot(path=str(QA / "01_RESUME_progress.png"), full_page=False)
            hit = m.harvest_newest(page, DEST, before)
            if hit and DEST.exists() and DEST.stat().st_size > 150_000:
                print(f"harvested via {hit}", flush=True)
                break
            if re.search(r"\bfailed\b", body, re.I) and re.search(r"generat|create|video", body, re.I):
                raise SystemExit("STOP: Flow failed banner during resume")
            page.wait_for_timeout(5000)
        else:
            raise SystemExit("STOP: resume timeout no harvest")

        try:
            veo.strip_audio(DEST)
        except Exception as e:
            print(f"strip warn {e}", flush=True)
        dur = m.probe_dur(DEST)
        if dur < 6.0 or dur > 12.0:
            raise SystemExit(f"STOP: unexpected duration {dur}")
        m.extract_qa_frames(DEST, PLATE)
        report = {
            "plate": PLATE,
            "version": "v01",
            "path": str(DEST),
            "bytes": DEST.stat().st_size,
            "sha256": m.sha256_file(DEST),
            "duration_s": dur,
            "model": "Veo 3.1 - Quality",
            "account": "benoats@googlemail.com",
            "project": page.url,
            "assemble": "CLOSED",
            "resume_harvest": True,
            "ts": datetime.now(timezone.utc).isoformat(),
        }
        (QA / f"{PLATE}_v01_mint.json").write_text(json.dumps(report, indent=2) + "\n")
        (QA / "01_SUBMITTED.json").write_text(
            json.dumps({**report, "status": "landed"}, indent=2) + "\n"
        )
        print("LANDED", json.dumps(report, indent=2), flush=True)

if __name__ == "__main__":
    main()
