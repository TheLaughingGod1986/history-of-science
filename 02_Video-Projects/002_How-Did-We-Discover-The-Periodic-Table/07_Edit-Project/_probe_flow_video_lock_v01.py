#!/usr/bin/env python3
"""Probe: open Flow project → lock Video/Veo via prompt pill → print pill text."""
from __future__ import annotations

import os
import sys
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
OUT = Path("/tmp/hos_flow_video_lock_probe")
OUT.mkdir(parents=True, exist_ok=True)


def main() -> None:
    from playwright.sync_api import sync_playwright

    print(f"profile={PROFILE} url={PINNED}", flush=True)
    with sync_playwright() as p:
        ctx, page = flow.launch_context(p, headed=True, profile=PROFILE)
        flow.ensure_flow_account(page)
        page.goto(PINNED, wait_until="domcontentloaded", timeout=120_000)
        page.wait_for_timeout(2500)
        flow.dismiss_banners(page)
        page.screenshot(path=str(OUT / "01_before.png"))
        before = flow._prompt_settings_pill_text(page)
        print(f"BEFORE pill={before!r}", flush=True)

        flow.configure_veo_settings(page, model="Veo 3.1 - Fast")
        page.wait_for_timeout(800)
        after = flow._prompt_settings_pill_text(page)
        print(f"AFTER pill={after!r}", flush=True)
        page.screenshot(path=str(OUT / "02_after_lock.png"))

        # Re-open pill and dump radios for evidence
        try:
            flow._open_prompt_settings_pill(page)
            page.wait_for_timeout(700)
            dump = page.evaluate(
                """() => [...document.querySelectorAll('button[role=radio],button[role=tab]')]
                  .map(b => ({
                    t: ((b.innerText||'')+'|'+(b.getAttribute('aria-label')||'')).trim().slice(0,80),
                    checked: b.getAttribute('aria-checked')||b.getAttribute('aria-selected')||'',
                  }))"""
            )
            print(f"RADIOS={dump!r}", flush=True)
            page.screenshot(path=str(OUT / "03_popover.png"))
        except Exception as e:
            print(f"popover dump failed: {e}", flush=True)

        ok = bool(after) and (
            ("Video" in after or "Veo" in after)
            and "Nano Banana" not in after
        )
        print(f"PASS={ok}", flush=True)
        ctx.close()
        raise SystemExit(0 if ok else 2)


if __name__ == "__main__":
    main()
