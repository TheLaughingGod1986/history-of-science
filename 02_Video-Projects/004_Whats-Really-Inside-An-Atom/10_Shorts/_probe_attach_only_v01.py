#!/usr/bin/env python3
"""Attach three style refs in Image 9:16 — no generate. NEW tab only."""
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

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(mint.CDP)
        page = browser.contexts[0].new_page()
        try:
            page.goto(mint.PINNED, wait_until="domcontentloaded", timeout=120_000)
            page.wait_for_timeout(2200)
            flow.dismiss_banners(page)
            mint.select_image_9x16(page)
            mint.clear_prompt_attachments(page)
            n = 0
            for ref in mint.STYLE_REFS:
                ok = mint.attach_style_ref_image_mode(page, ref)
                print("OK" if ok else "FAIL", ref.name, "chips", mint.ingredient_chip_count(page))
                n += int(ok)
                mint.select_image_9x16(page)
            page.screenshot(
                path=str(mint.QA_DIR / "probe_three_refs_attached.png"), full_page=False
            )
            print("TOTAL", n, "chips", mint.ingredient_chip_count(page), "pill", mint.pill_text(page))
            return 0 if n >= 2 else 2
        finally:
            page.close()


if __name__ == "__main__":
    raise SystemExit(main())
