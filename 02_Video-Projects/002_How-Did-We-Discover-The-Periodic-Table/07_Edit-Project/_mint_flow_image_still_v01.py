#!/usr/bin/env python3
"""Mint one finished jar-free Flow IMAGE still (Nano Banana), save JPEG.

Intentional Image mode — stills only. Video remint stays on Veo I2V afterward.
"""
from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))
import orbit_flow_veo_ui as flow  # noqa: E402

PINNED = os.environ.get(
    "HOS_FLOW_PROJECT_URL",
    "https://flow.google.com/u/1/project/30a34afb-8d9c-4eac-83ba-012d97f6b1b5",
)
PROFILE = Path(
    os.environ.get(
        "ORBIT_FLOW_PROFILE",
        str(Path.home() / ".playwright-hos-flow-profile"),
    )
)

STILL_PROMPT = """Premium finished Animistry-class 3D cartoon still (Germs Part 01 PASS quality).
Scholar WRITING STUDY desk — warm oak, soft volumetric window light, rich wood grain,
polished finished render (NOT flat placeholders, NOT unfinished).
On the desk: a neat short row of blank cream specimen cards (paper only), leather notebooks,
quill, closed ink bottle with lid, one brass candlestick with a tiny natural candle-wick flame.
HARD LOCK: ZERO jars, pots, canisters, tins, flasks, bottles, vials, retorts, burners,
chemistry shelves, alchemy glassware, smoke, fire under vessels.
Not photoreal. Silent. No people. No Orbit. No readable text."""


def _select_image_tab(page) -> None:
    flow._open_prompt_settings_pill(page)
    page.wait_for_timeout(700)
    box = page.evaluate(
        """() => {
          for (const b of document.querySelectorAll('button[role=radio],button[role=tab],[role=radio]')) {
            const t = ((b.innerText||'')+' '+(b.getAttribute('aria-label')||'')).trim();
            if (/\\bImage\\b/i.test(t) && !/\\bVideo\\b/i.test(t)) {
              const r = b.getBoundingClientRect();
              if (r.width > 20 && r.height > 16)
                return {x:r.x+r.width/2,y:r.y+r.height/2,t};
            }
          }
          return null;
        }"""
    )
    if not box:
        raise RuntimeError("Image radio not found in settings popover")
    page.mouse.click(box["x"], box["y"])
    page.wait_for_timeout(900)
    try:
        page.keyboard.press("Escape")
    except Exception:
        pass
    page.wait_for_timeout(400)
    pill = flow._prompt_settings_pill_text(page)
    print(f"  image-mode pill={pill!r}", flush=True)
    if "Video" in pill and "Nano Banana" not in pill and "Banana" not in pill:
        raise RuntimeError(f"Failed to switch to Image mode: {pill!r}")


def _download_newest_image(page, dest: Path, timeout_s: float = 180) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    while time.time() - t0 < timeout_s:
        thumbs = page.locator("img").count()
        print(f"  image poll imgs={thumbs} elapsed={int(time.time()-t0)}s", flush=True)
        # Click newest large gallery tile
        hit = page.evaluate(
            """() => {
              const imgs=[...document.querySelectorAll('img')].map(i=>{
                const r=i.getBoundingClientRect();
                return {x:r.x+r.width/2,y:r.y+r.height/2,w:r.width,h:r.height,y0:r.y};
              }).filter(i=>i.w>120&&i.h>80&&i.y0>80);
              imgs.sort((a,b)=>b.y0-a.y0 || b.x-a.x);
              return imgs[0]||null;
            }"""
        )
        if hit:
            page.mouse.click(hit["x"], hit["y"])
            page.wait_for_timeout(1200)
            # Try download button
            for label in ("Download", "download", "Save"):
                btn = page.get_by_role("button", name=label)
                if btn.count():
                    try:
                        with page.expect_download(timeout=15000) as dl:
                            btn.first.click(timeout=3000)
                        d = dl.value
                        d.save_as(str(dest))
                        if dest.exists() and dest.stat().st_size > 20000:
                            return dest
                    except Exception as e:
                        print(f"  download via {label} failed: {e}", flush=True)
            # Fallback: grab currentSrc of large preview
            src = page.evaluate(
                """() => {
                  const imgs=[...document.querySelectorAll('img')].map(i=>{
                    const r=i.getBoundingClientRect();
                    return {src:i.currentSrc||i.src,w:r.width,h:r.height};
                  }).filter(i=>i.w>400&&i.h>220&&i.src);
                  imgs.sort((a,b)=>b.w*b.h-a.w*a.h);
                  return imgs[0]?.src||null;
                }"""
            )
            if src and src.startswith("http"):
                data = page.evaluate(
                    """async (url) => {
                      const r = await fetch(url); const b = await r.arrayBuffer();
                      const u = new Uint8Array(b); let s='';
                      for (let i=0;i<u.length;i++) s+=String.fromCharCode(u[i]);
                      return btoa(s);
                    }""",
                    src,
                )
                import base64

                dest.write_bytes(base64.b64decode(data))
                if dest.stat().st_size > 20000:
                    return dest
        page.wait_for_timeout(4000)
    raise RuntimeError(f"Timed out waiting for Flow image still → {dest}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--prompt", default=STILL_PROMPT)
    args = ap.parse_args()

    from playwright.sync_api import sync_playwright

    profile = flow.profile_path(PROFILE)
    print(f"IMAGE_STILL out={args.out} profile={profile}", flush=True)
    with sync_playwright() as p:
        ctx, page = flow.launch_context(p, headed=True, profile=profile)
        flow.ensure_flow_account(page)
        page.goto(PINNED, wait_until="domcontentloaded", timeout=120_000)
        page.wait_for_timeout(2500)
        flow.dismiss_banners(page)
        before = page.evaluate("() => document.querySelectorAll('img').length")
        _select_image_tab(page)
        flow.force_outputs_x1(page)
        flow.set_prompt(page, args.prompt)
        print("  submitting Image Create…", flush=True)
        flow.submit_create(page)
        flow.confirm_generation_spend(page)
        page.wait_for_timeout(8000)
        path = _download_newest_image(page, args.out)
        print(f"OK still bytes={path.stat().st_size} before_imgs={before}", flush=True)
        ctx.close()


if __name__ == "__main__":
    main()
