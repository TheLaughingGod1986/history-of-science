#!/usr/bin/env python3
"""Put live_v04 covers on Fri + Sun scheduled Shorts ONLY.

Ben 12:30 / CoS: cover only on 29bpGAI0wb8 + TbMMJSRKC3U.
No schedule, visibility, audience, AI, or Related changes.
HOS @HistoryOfScienceYT CDP :9460.
"""
from __future__ import annotations

import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright

# Reuse proven upload_thumb from Germs force-thumb script
import importlib.util

FORCE = Path(
    "/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/"
    "001_How-Did-We-Discover-Germs/11_Upload-Package/Schedule/"
    "_force_shorts_thumb_house_v01.py"
)
spec = importlib.util.spec_from_file_location("force_thumbs", FORCE)
mod = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(mod)
upload_thumb = mod.upload_thumb
click_save = mod.click_save
ensure_hos = mod.ensure_hos

CDP = "http://127.0.0.1:9460"
CHANNEL = "UCXp7HkBIl1LgaznXuZHJyRg"
EV = Path(
    "/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/"
    "004_Whats-Really-Inside-An-Atom/11_Upload-Package/Schedule/"
    "evidence_2026-09-30_shorts"
)
ART = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts"
AGENT = Path.home() / (
    "Library/Application Support/Cursor/AgentStores/"
    "cursor_agent_stores/bc-958ae0f3-be07-568f-a2ab-eb7f422d8839/files/artifacts"
)
COVERS = Path(
    "/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/"
    "004_Whats-Really-Inside-An-Atom/10_Shorts/covers_live_v04"
)

JOBS = [
    {
        "slot": "fri",
        "id": "29bpGAI0wb8",
        "title": "How small can you cut gold?",
        "cover": COVERS / "hos_004_s01_how_small_cover_live_v04.jpg",
    },
    {
        "slot": "sun",
        "id": "TbMMJSRKC3U",
        "title": "He said every eighth element repeats",
        "cover": COVERS / "hos_004_s02_every_eighth_cover_live_v04.jpg",
    },
]


def shot(page, name: str) -> Path:
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    AGENT.mkdir(parents=True, exist_ok=True)
    p = EV / name
    page.screenshot(path=str(p), full_page=False)
    for d in (ART, AGENT):
        dest = d / name.replace("COVER_", "BEN_1230_COVER_")
        dest.write_bytes(p.read_bytes())
    return p


def process_one(page, job: dict) -> dict:
    vid = job["id"]
    cover = job["cover"]
    if not cover.exists():
        return {"ok": False, "err": f"missing {cover}"}
    url = f"https://studio.youtube.com/channel/{CHANNEL}/video/{vid}/edit"
    page.goto(url, wait_until="domcontentloaded", timeout=90000)
    page.wait_for_timeout(3500)
    # Stay on Details — do not open Visibility / Audience tabs
    before = shot(page, f"COVER_{job['slot']}_{vid}_01_before.png")
    up = upload_thumb(page, cover)
    mid = shot(page, f"COVER_{job['slot']}_{vid}_02_after_upload.png")
    if not up.get("ok"):
        return {
            "ok": False,
            "id": vid,
            "slot": job["slot"],
            "upload": up,
            "before": str(before),
            "after_upload": str(mid),
        }
    page.wait_for_timeout(1500)
    saved = click_save(page)
    page.wait_for_timeout(3500)
    after = shot(page, f"COVER_{job['slot']}_{vid}_03_after_save.png")
    # Confirm we did not leave Details for Visibility
    body = page.inner_text("body")[:800]
    return {
        "ok": bool(up.get("ok")),
        "id": vid,
        "slot": job["slot"],
        "title": job["title"],
        "cover": str(cover),
        "upload": {"ok": up.get("ok"), "method": up.get("method")},
        "save": saved,
        "before": str(before),
        "after_upload": str(mid),
        "after_save": str(after),
        "url": url,
        "body_snip": body[:240],
    }


def main() -> int:
    EV.mkdir(parents=True, exist_ok=True)
    results = []
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        ctx = browser.contexts[0] if browser.contexts else browser.new_context()
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        ensure_hos(page)
        for job in JOBS:
            print(f"== {job['slot']} {job['id']} ==", flush=True)
            try:
                r = process_one(page, job)
            except Exception as e:
                r = {"ok": False, "id": job["id"], "slot": job["slot"], "err": f"{type(e).__name__}:{e}"}
            results.append(r)
            print(json.dumps({k: r.get(k) for k in ("ok", "slot", "id", "save", "upload")}, indent=2), flush=True)
            time.sleep(1.2)
    out = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "channel": CHANNEL,
        "note": "cover only — no schedule/visibility/audience/AI/Related changes",
        "results": results,
        "ok": all(r.get("ok") for r in results),
    }
    path = EV / "FRI_SUN_COVERS_LIVE_V04.json"
    path.write_text(json.dumps(out, indent=2) + "\n")
    ART.mkdir(parents=True, exist_ok=True)
    (ART / "BEN_1230_FRI_SUN_COVERS_LIVE_V04.json").write_text(json.dumps(out, indent=2) + "\n")
    print("WROTE", path, "ok=", out["ok"], flush=True)
    return 0 if out["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
