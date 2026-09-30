#!/usr/bin/env python3
"""Salvage gold-coin portrait gens already in Flow gallery (NEW tab)."""
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
            page.wait_for_timeout(2800)
            flow.dismiss_banners(page)
            page.screenshot(path=str(mint.QA_DIR / "salvage_coin_gallery.png"), full_page=False)
            tiles = page.evaluate(
                """() => [...document.querySelectorAll('img')].map((i,idx)=>{
                  const r=i.getBoundingClientRect();
                  return {idx,x:r.x+r.width/2,y:r.y+r.height/2,w:r.width,h:r.height,
                          x0:r.x,y0:r.y,portrait:r.height>r.width*1.05};
                }).filter(t=>t.w>70&&t.h>90&&t.y0>100&&t.y0<420)
                  .sort((a,b)=>a.y0-b.y0||a.x0-b.x0)"""
            )
            print("tiles", tiles)
            saved = []
            for i, t in enumerate(tiles):
                page.keyboard.press("Escape")
                page.wait_for_timeout(150)
                page.mouse.click(t["x"], t["y"])
                page.wait_for_timeout(900)
                # Prefer large preview clip
                dest = mint.QA_DIR / f"salvage_coin_{i}.png"
                ok = mint._screenshot_largest_new_portrait(page, dest, before_srcs=set())
                if not ok:
                    ok = mint._download_selected_media(page, dest)
                if ok and dest.exists():
                    im = Image.open(dest)
                    # Skip explorer sheet
                    if im.size == (1122, 1402):
                        print("skip explorer", dest.name)
                        continue
                    # Skip known style cover dims if identical to live covers? keep for QA
                    print("saved", dest.name, im.size)
                    saved.append({"path": str(dest), "size": list(im.size)})
                page.keyboard.press("Escape")
            print("saved", saved)
            # If we got a good coin scene, copy to s01 output
            out = mint.OUT_DIR / "s01_how_small_scene.png"
            for s in saved:
                im = Image.open(s["path"])
                # Heuristic: warm desk scene — not explorer sheet, tall, not tiny
                if im.size[1] > im.size[0] and im.size[0] >= 400:
                    # Rough color: goldish avg
                    small = im.resize((32, 32))
                    px = list(small.getdata())
                    avg = tuple(sum(c[i] for c in px) // len(px) for i in range(3))
                    print("avg", s["path"].split("/")[-1], avg)
                    # Prefer images with warm gold bias
                    if avg[0] > avg[2] + 5:
                        mint.normalize_to_png(Path(s["path"]), out)
                        print("PROMOTED s01", out, Image.open(out).size)
                        break
            return 0
        finally:
            page.close()


if __name__ == "__main__":
    raise SystemExit(main())
