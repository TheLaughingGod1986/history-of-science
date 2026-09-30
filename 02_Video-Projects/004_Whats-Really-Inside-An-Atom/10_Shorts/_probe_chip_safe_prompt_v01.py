#!/usr/bin/env python3
"""Attach then chip-safe prompt insert — verify chips survive. No generate."""
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
            for ref in mint.STYLE_REFS:
                mint.attach_style_ref_image_mode(page, ref)
            chips1 = mint.ingredient_chip_count(page)
            print("after_attach", chips1)
            box = flow.editor_box(page)
            page.mouse.click(box["x"] + min(box["w"] - 40, 200), box["y"] + max(8, box["h"] / 2))
            page.wait_for_timeout(120)
            page.keyboard.insert_text(mint.STILLS["s02"]["try1"][:400])
            page.wait_for_timeout(300)
            chips2 = mint.ingredient_chip_count(page)
            got = flow._editor_prompt_text(page) or ""
            print("after_prompt chips", chips2, "len", len(got), "pill", mint.pill_text(page))
            page.screenshot(path=str(mint.QA_DIR / "probe_chip_safe.png"), full_page=False)
            return 0 if chips2 >= 2 and len(got) > 40 else 2
        finally:
            page.close()


if __name__ == "__main__":
    raise SystemExit(main())
