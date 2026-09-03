#!/usr/bin/env python3
"""Take 2: same I2V path as take 1, plus Enter submit if arrow_forward is gone."""
from __future__ import annotations

import json
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


def dump(page, tag: str) -> None:
    info = page.evaluate(
        """() => {
          const btns = [];
          for (const b of document.querySelectorAll('button,[role="button"]')) {
            const t = (b.innerText || b.getAttribute('aria-label') || '')
              .trim().replace(/\\n/g, ' ');
            if (!t) continue;
            const r = b.getBoundingClientRect();
            btns.push({
              t: t.slice(0, 70),
              dis: !!(b.disabled || b.getAttribute('aria-disabled') === 'true'),
              x: Math.round(r.x), y: Math.round(r.y),
              w: Math.round(r.width), h: Math.round(r.height),
            });
          }
          return { url: location.href, btns: btns.slice(0, 90) };
        }"""
    )
    print(f"  DUMP {tag} {json.dumps(info)[:2400]}", flush=True)


def force_submit(page) -> bool:
    """arrow_forward, then prompt-bar Create, then keyboard."""
    try:
        flow.submit_create(page)
        return True
    except Exception as e:
        print(f"  submit_create miss: {e}", flush=True)
    clicked = page.evaluate(
        """() => {
          const ranked = [];
          for (const b of document.querySelectorAll('button')) {
            const t = (b.innerText || '').trim().replace(/\\n/g, ' ');
            const r = b.getBoundingClientRect();
            if (r.width < 8 || r.height < 8) continue;
            if (b.disabled || b.getAttribute('aria-disabled') === 'true') continue;
            if (/arrow_forward/i.test(t)) ranked.push({b, n: 3, t});
            else if (/^Create$/i.test(t) && r.y > 500) ranked.push({b, n: 2, t});
            else if (/add_2\\s*Create/i.test(t) && r.y > 500 && r.width < 160)
              ranked.push({b, n: 1, t});
          }
          ranked.sort((a,c) => c.n - a.n);
          if (!ranked.length) return null;
          ranked[0].b.click();
          return ranked[0].t.slice(0, 40);
        }"""
    )
    if clicked:
        print(f"  force clicked {clicked!r}", flush=True)
        page.wait_for_timeout(800)
        return True
    print("  keyboard Meta+Enter / Enter", flush=True)
    page.keyboard.press("Meta+Enter")
    page.wait_for_timeout(400)
    page.keyboard.press("Enter")
    page.wait_for_timeout(800)
    return True


def main() -> None:
    if not STILL.exists():
        raise SystemExit(f"missing {STILL}")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    print("cooldown 20s then fresh project", flush=True)
    time.sleep(20)
    t0 = time.time()
    with sync_playwright() as p:
        ctx, page = flow.launch_context(
            p, headed=False, profile=flow.profile_path(PROFILE)
        )
        try:
            page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
            page.wait_for_timeout(2000)
            flow.dismiss_banners(page)
            # Prefer dismissing consent without looping Agree if No thanks exists.
            try:
                page.get_by_role("button", name="No thanks").first.click(timeout=1500)
            except Exception:
                pass
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
            if flow.try_context_animate(page):
                flow.configure_veo_settings(
                    page, model=MODEL, frames_mode=False, ingredients_mode=True
                )
            flow.set_prompt(page, PROMPT)
            if flow._prompt_attachment_count(page) < 1:
                flow.attach_image_to_prompt(page, STILL)
                flow.set_prompt(page, PROMPT)
            dump(page, "pre-submit")
            force_submit(page)
            flow.confirm_generation_spend(page)
            flow.wait_and_download(
                page, OUT, before_ids=before, timeout_s=1200, min_elapsed_s=20
            )
        finally:
            ctx.close()
    if not OUT.exists() or OUT.stat().st_size < 400_000:
        raise SystemExit(f"download missing/small {OUT}")
    print(f"SAVED {OUT} bytes={OUT.stat().st_size} secs={time.time()-t0:.1f}", flush=True)


if __name__ == "__main__":
    main()
