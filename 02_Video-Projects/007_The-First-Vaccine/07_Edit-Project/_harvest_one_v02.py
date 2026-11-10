#!/usr/bin/env python3
"""Download one already-paid Flow clip. Does not click Create."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "04_Audio/tools"))
from playwright.sync_api import sync_playwright
import orbit_flow_veo_ui as flow

URL = "https://flow.google.com/project/9547a920-fe2c-4b49-886f-fd7cdb1fdc2b"
DEST = Path.home() / (
    "YouTube/hos-007-vaccine/02_Video-Projects/007_The-First-Vaccine"
    "/04_Generated-Clips/part01/raw/v01/01_cow_meadow_t1.mp4"
)


def main() -> int:
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp("http://127.0.0.1:9222")
        page = None
        for pg in browser.contexts[0].pages:
            if "flow.google.com" in (pg.url or ""):
                page = pg
                page.bring_to_front()
                break
        if page is None:
            raise SystemExit("no flow page")
        page.goto(URL, wait_until="domcontentloaded", timeout=120_000)
        page.wait_for_timeout(4000)
        captured: list[bytes] = []
        for i in range(12):
            hit = flow.harvest_agent_gallery_mp4(page, DEST, captured)
            size = DEST.stat().st_size if DEST.exists() else 0
            print(f"try {i} hit={hit} bytes={size}", flush=True)
            if size >= 400_000:
                print("HARVESTED", DEST, size, flush=True)
                return 0
            page.wait_for_timeout(10000)
    print("HARVEST FAILED", flush=True)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
