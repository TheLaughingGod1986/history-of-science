#!/usr/bin/env python3
"""Take 2 on the HOS Animate page: lock Veo 3.1 Fast, never Nano Banana."""
from __future__ import annotations

import os
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))

import orbit_flow_veo_ui as flow  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

PROJ = Path(__file__).resolve().parents[1]
STILL = PROJ / "04_Generated-Clips/part01/refs/v20_aisle/aisle_t1_last.jpg"
OUT = PROJ / "04_Generated-Clips/part01/raw/v20_aisle/aisle_walk_t2.mp4"
MODEL = "Veo 3.1 - Fast"
PROFILE = Path(
    os.environ.get(
        "ORBIT_FLOW_PROFILE",
        str(Path.home() / ".playwright-hos-flow-profile"),
    )
)
PROMPT = (
    "IMAGE-TO-VIDEO of the attached start frame. Continue the SAME slow walk down "
    "this SAME Victorian death-ward aisle, SAME direction toward the far window. "
    "Camera keeps TRANSLATING forward from frame 1 — not a locked still, not a zoom, "
    "not Ken Burns. Faceless 3D rods and spiked spheres keep drifting in 3D space, "
    "sparse, not cute, not a neon overlay. No Explorer, no Orbit, no text, no modern "
    "hospital. Silent. Continuous 8 seconds through the last frame."
)


def lock_veo_on_animate_page(page) -> str:
    """On still→Animate sheet: pick Veo 3.1 Fast. Do not Escape away."""
    t0 = time.time()
    selected = ""
    pills: list[str] = []
    while time.time() - t0 < 25:
        flow.dismiss_banners(page)
        selected = flow.read_selected_video_model(page) or ""
        pills = page.evaluate(
            """() => [...document.querySelectorAll('button')]
              .map(b => (b.innerText || '').trim().replace(/\\n/g,' '))
              .filter(t => /Veo|Banana|Omni|Fast|Quality|Lite/i.test(t))
              .slice(0, 20)"""
        )
        print(f"  model wait selected={selected!r} pills={pills}", flush=True)
        if any("Veo" in t or "Banana" in t for t in pills) or selected:
            break
        page.wait_for_timeout(1000)
    if "Veo 3.1 - Fast" in selected or any("Veo 3.1 - Fast" in t for t in (pills or [])):
        print("  already Fast", flush=True)
        return selected or MODEL
    clicked = page.evaluate(
        """() => {
          for (const b of document.querySelectorAll('button')) {
            const t = (b.innerText || '').trim().replace(/\\n/g, ' ');
            if (/Nano Banana|Veo 3|Omni Flash/i.test(t)) {
              b.click();
              return t.slice(0, 60);
            }
          }
          return null;
        }"""
    )
    print(f"  opened model pill {clicked!r}", flush=True)
    page.wait_for_timeout(600)
    item = page.get_by_role("menuitem", name="Veo 3.1 - Fast")
    if item.count():
        item.last.click(timeout=5000)
    else:
        page.locator('[role="menuitem"]:has-text("Veo 3.1 - Fast")').last.click(
            timeout=5000
        )
    page.wait_for_timeout(800)
    selected = flow.read_selected_video_model(page) or ""
    pills = page.evaluate(
        """() => [...document.querySelectorAll('button')]
          .map(b => (b.innerText || '').trim().replace(/\\n/g,' '))
          .filter(t => /Veo|Banana|Omni|Fast|Quality|Lite/i.test(t))
          .slice(0, 20)"""
    )
    print(f"  after pick selected={selected!r} pills={pills}", flush=True)
    blob = selected + " " + " ".join(pills or [])
    if "Lite" in blob and "Fast" not in blob:
        raise SystemExit(f"refusing Lite: {blob}")
    if "Banana" in blob and "Veo 3.1 - Fast" not in blob:
        raise SystemExit(f"refusing Banana: {blob}")
    if "Veo 3.1 - Fast" not in blob and "Veo 3" not in selected:
        raise SystemExit(f"Veo Fast not locked: {blob}")
    print(f"  animate-page model: {blob}", flush=True)
    return blob


def click_arrow_create(page) -> bool:
    return bool(
        page.evaluate(
            """() => {
              const ranked = [];
              for (const b of document.querySelectorAll('button')) {
                const t = (b.innerText || '').trim().replace(/\\n/g, ' ');
                if (!/arrow_forward/i.test(t) || !/Create/i.test(t)) continue;
                if (/add_2|error|cancel/i.test(t)) continue;
                if (b.disabled || b.getAttribute('aria-disabled') === 'true') continue;
                const r = b.getBoundingClientRect();
                if (r.width < 8 || r.height < 8) continue;
                ranked.push(b);
              }
              if (!ranked.length) return false;
              ranked[ranked.length - 1].click();
              return true;
            }"""
        )
    )


def main() -> None:
    if not STILL.exists():
        raise SystemExit(f"missing {STILL}")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    with sync_playwright() as p:
        ctx, page = flow.launch_context(
            p, headed=False, profile=flow.profile_path(PROFILE)
        )
        try:
            page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
            page.wait_for_timeout(2000)
            flow.dismiss_banners(page)
            if not flow.looks_logged_in(page):
                raise SystemExit("Flow not logged in.")
            url = flow.ensure_project(page)
            print(f"  flow: {url}", flush=True)
            flow.ensure_agent_session(page)
            before = flow.collect_media_ids(page)
            flow.configure_veo_settings(
                page, model=MODEL, frames_mode=False, ingredients_mode=True
            )
            if not flow.attach_image_to_prompt(page, STILL):
                raise SystemExit("attach failed")
            if not flow.try_context_animate(page):
                raise SystemExit("Animate failed")
            page.wait_for_timeout(1200)
            # Stay on the Animate sheet. Do not Escape / re-open settings.
            lock_veo_on_animate_page(page)
            flow.set_prompt(page, PROMPT)
            selected = flow.read_selected_video_model(page) or ""
            print(f"  model at submit: {selected!r}", flush=True)
            if "Banana" in selected or "Omni" in selected:
                raise SystemExit(f"abort Banana/Omni at submit: {selected}")
            if not click_arrow_create(page):
                raise SystemExit("arrow_forward Create not on Animate page")
            print("  clicked arrow_forward Create", flush=True)
            flow.confirm_generation_spend(page)
            flow.wait_and_download(
                page, OUT, before_ids=before, timeout_s=900, min_elapsed_s=20
            )
        finally:
            ctx.close()
    if not OUT.exists() or OUT.stat().st_size < 400_000:
        raise SystemExit(f"download missing/small {OUT}")
    print(f"SAVED {OUT} bytes={OUT.stat().st_size} secs={time.time()-t0:.1f}", flush=True)


if __name__ == "__main__":
    main()
