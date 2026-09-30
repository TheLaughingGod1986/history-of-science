#!/usr/bin/env python3
"""Download newest gallery tiles via Download-media menu (NEW tab)."""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _mint_covers_live_v02_stills_cdp as mint  # noqa: E402

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))
import orbit_flow_veo_ui as flow  # noqa: E402


def main() -> int:
    from playwright.sync_api import sync_playwright
    from PIL import Image

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(mint.CDP)
        page = browser.contexts[0].new_page()
        try:
            page.goto(mint.PINNED, wait_until="domcontentloaded", timeout=120_000)
            page.wait_for_timeout(2500)
            flow.dismiss_banners(page)
            tiles = page.evaluate(
                """() => [...document.querySelectorAll('img')].map(i=>{
                  const r=i.getBoundingClientRect();
                  return {x:r.x+r.width/2,y:r.y+r.height/2,w:r.width,h:r.height,
                          portrait:r.height>r.width*1.05};
                }).filter(t=>t.w>70&&t.h>90&&t.y>100&&t.y<500)
                  .sort((a,b)=>a.y-b.y||a.x-b.x)"""
            )
            print("tiles", tiles)
            saved = 0
            for i, t in enumerate(tiles[:5]):
                if not t.get("portrait"):
                    continue
                page.keyboard.press("Escape")
                page.wait_for_timeout(200)
                page.mouse.click(t["x"], t["y"])
                page.wait_for_timeout(800)
                dest = mint.QA_DIR / f"salvage_menu_{i}.png"
                if mint._download_selected_media(page, dest):
                    im = Image.open(dest)
                    print("saved", dest.name, im.size)
                    saved += 1
                page.keyboard.press("Escape")
            print("saved_count", saved)
            return 0
        finally:
            page.close()


if __name__ == "__main__":
    raise SystemExit(main())
