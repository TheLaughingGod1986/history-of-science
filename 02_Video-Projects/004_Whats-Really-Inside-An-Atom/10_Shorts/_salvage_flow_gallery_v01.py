#!/usr/bin/env python3
"""Salvage newest portrait Flow Image gens from the project gallery (NEW tab)."""
from __future__ import annotations

import base64
import json
import re
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))
import orbit_flow_veo_ui as flow  # noqa: E402

CDP = "http://127.0.0.1:9222"
PINNED = "https://flow.google.com/project/30a34afb-8d9c-4eac-83ba-012d97f6b1b5"
OUT = Path(__file__).resolve().parent / "covers_live_v02" / "stills" / "_qa_mint"


def main() -> int:
    from playwright.sync_api import sync_playwright
    from PIL import Image

    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        page = browser.contexts[0].new_page()
        try:
            page.goto(PINNED, wait_until="domcontentloaded", timeout=120_000)
            page.wait_for_timeout(3000)
            flow.dismiss_banners(page)
            page.screenshot(path=str(OUT / "salvage_gallery.png"), full_page=False)
            # Wait if generating
            for i in range(40):
                body = page.locator("body").inner_text(timeout=5000)[:3000]
                if re.search(r"\b\d{1,3}%\b|in the queue|Generating", body, re.I):
                    print(f"still generating… {i*3}s")
                    page.wait_for_timeout(3000)
                    continue
                break
            page.screenshot(path=str(OUT / "salvage_gallery_done.png"), full_page=False)
            tiles = page.evaluate(
                """() => [...document.querySelectorAll('img')].map((i,idx)=>{
                  const r=i.getBoundingClientRect();
                  return {idx, w:Math.round(r.width), h:Math.round(r.height),
                          y:Math.round(r.y), x:Math.round(r.x),
                          src:(i.currentSrc||i.src||'').slice(0,180),
                          portrait: r.height > r.width * 1.1};
                }).filter(t=>t.w>80&&t.h>80&&t.y>80&&t.y<700)
                  .sort((a,b)=>a.y-b.y || a.x-b.x)"""
            )
            (OUT / "salvage_tiles.json").write_text(json.dumps(tiles, indent=2))
            print("tiles", json.dumps(tiles, indent=2)[:3000])
            # Download up to 3 newest portrait-ish gallery tiles (not the style refs which may be tall too)
            saved = []
            # Click each large tile from left (newest often leftmost)
            candidates = [t for t in tiles if t["w"] > 140 and t["h"] > 140]
            for n, t in enumerate(candidates[:6]):
                page.mouse.click(t["x"] + t["w"] / 2, t["y"] + t["h"] / 2)
                page.wait_for_timeout(900)
                dest = OUT / f"salvage_{n}.png"
                got = False
                for label in ("Download", "download", "Save"):
                    btn = page.get_by_role("button", name=re.compile(label, re.I))
                    if btn.count():
                        try:
                            with page.expect_download(timeout=15000) as dl:
                                btn.first.click(timeout=3000)
                            dl.value.save_as(str(dest))
                            if dest.exists() and dest.stat().st_size > 30000:
                                got = True
                                break
                        except Exception as e:
                            print("dl fail", e)
                if not got and t.get("src", "").startswith("http"):
                    data = page.evaluate(
                        """async (url) => {
                          const r=await fetch(url); const b=await r.arrayBuffer();
                          const u=new Uint8Array(b); let s='';
                          for (let i=0;i<u.length;i++) s+=String.fromCharCode(u[i]);
                          return btoa(s);
                        }""",
                        t["src"],
                    )
                    dest.write_bytes(base64.b64decode(data))
                    got = dest.stat().st_size > 20000
                if got:
                    im = Image.open(dest)
                    print(f"saved {dest.name} {im.size} portrait={im.size[1]>im.size[0]}")
                    saved.append({"path": str(dest), "size": im.size})
                page.keyboard.press("Escape")
                page.wait_for_timeout(300)
            (OUT / "salvage_saved.json").write_text(json.dumps(saved, indent=2))
            return 0
        finally:
            page.close()


if __name__ == "__main__":
    raise SystemExit(main())
