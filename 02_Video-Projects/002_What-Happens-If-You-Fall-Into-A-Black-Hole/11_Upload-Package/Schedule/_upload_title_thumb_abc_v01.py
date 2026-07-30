#!/usr/bin/env python3
"""Enable Title and thumbnail Test & Compare on Video 002 long-form."""
from __future__ import annotations

import json
import re
from pathlib import Path

from playwright.sync_api import sync_playwright

PROFILE = "/Users/ben/code/youtube/.playwright-youtube-profile"
VID = "n7CbJrOCnU0"
ROOT = Path(
    "/Users/ben/code/Orbit-YouTube/02_Video-Projects/"
    "002_What-Happens-If-You-Fall-Into-A-Black-Hole"
)
AUDIT = ROOT / "11_Upload-Package/Schedule/_abc_upload"
OUT = ROOT / "11_Upload-Package/Schedule/blackhole_title_thumb_abc_result.json"
THUMB_DIR = ROOT / "08_Thumbnail/GPT-Image-2-Tests"

THUMBS = [
    THUMB_DIR / "blackhole_thumb_A_falling-in_gpt-image-2_v01.png",
    THUMB_DIR / "blackhole_thumb_B_spaghettified_gpt-image-2_v01.png",
    THUMB_DIR / "blackhole_thumb_C_point-of-no-return_gpt-image-2_v01.png",
]
TITLES = [
    "What Happens If You Fall Into a Black Hole? Orbit's Cosmic Journey",
    "Fall Into a Black Hole — Spaghettification Explained",
    "What Happens Past the Event Horizon? A Cosmic Journey",
]


def skip(page) -> None:
    try:
        page.get_by_role("link", name=re.compile(r"Skip", re.I)).click(timeout=1200)
    except Exception:
        pass


def main() -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    for p in THUMBS:
        assert p.exists(), p
    r: dict = {"id": VID, "ok": False, "mode": None, "titles": TITLES}

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            PROFILE,
            headless=False,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"],
            viewport={"width": 1440, "height": 900},
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.goto(
            f"https://studio.youtube.com/video/{VID}/edit",
            wait_until="domcontentloaded",
            timeout=120_000,
        )
        page.wait_for_timeout(4000)
        skip(page)

        ab = page.locator("#ab-test-button").get_by_role("button", name="A/B Testing")
        if ab.count():
            ab.first.click(force=True)
        else:
            page.get_by_role("button", name="A/B Testing", exact=True).first.click(force=True)
        page.wait_for_timeout(2000)

        dlg = page.get_by_role("dialog", name="A/B Testing")
        dlg.wait_for(state="visible", timeout=15000)
        r["dialog"] = True

        dlg.get_by_text("Title and thumbnail", exact=True).click(force=True)
        page.wait_for_timeout(1200)
        r["mode"] = "Title and thumbnail"
        page.screenshot(path=str(AUDIT / "upload_mode.png"))

        boxes = dlg.get_by_role("textbox")
        for i in range(min(3, boxes.count())):
            boxes.nth(i).click(force=True)
            page.keyboard.press("Meta+a")
            page.keyboard.press("Backspace")
            page.keyboard.type(TITLES[i], delay=2)
            r[f"title{i+1}"] = True

        filled = 0
        for slot, path in enumerate(THUMBS, 1):
            ok = False
            try:
                inputs = dlg.locator('input[type="file"]')
                if inputs.count() >= slot:
                    inputs.nth(slot - 1).set_input_files(str(path))
                    page.wait_for_timeout(2800)
                    ok = True
            except Exception as e:
                r[f"s{slot}_inp"] = str(e)[:120]
            if not ok:
                try:
                    btn = dlg.locator(f'button[aria-label="Upload thumbnail {slot}"]')
                    if btn.count():
                        with page.expect_file_chooser(timeout=12000) as fc:
                            btn.first.click(force=True)
                        fc.value.set_files(str(path))
                        page.wait_for_timeout(2800)
                        ok = True
                except Exception as e:
                    r[f"s{slot}_err"] = str(e)[:120]
            r[f"th{slot}"] = ok
            if ok:
                filled += 1
        r["filled"] = filled
        page.screenshot(path=str(AUDIT / "upload_slots.png"))

        setb = dlg.get_by_role("button", name=re.compile(r"^Set test$", re.I))
        for _ in range(10):
            if setb.count() and setb.first.is_enabled():
                break
            page.wait_for_timeout(400)
        if setb.count() and setb.first.is_enabled():
            setb.first.click(force=True)
            page.wait_for_timeout(3000)
            r["set_test"] = True
        else:
            r["set_test"] = False

        save = page.get_by_role("button", name="Save", exact=True)
        if save.count() and save.first.is_enabled():
            save.first.click(force=True)
            page.wait_for_timeout(3000)
            r["saved"] = True

        page.goto(
            f"https://studio.youtube.com/video/{VID}/edit",
            wait_until="domcontentloaded",
            timeout=120_000,
        )
        page.wait_for_timeout(3500)
        skip(page)
        body = page.locator("body").inner_text()
        r["verify_ab_titles"] = "A/B testing titles" in body
        r["verify_ineligible"] = "Ineligible" in body
        page.screenshot(path=str(AUDIT / "upload_verify.png"), full_page=True)

        r["ok"] = bool(r.get("set_test") and filled >= 2 and r.get("title1") and r.get("title2"))
        OUT.write_text(json.dumps(r, indent=2) + "\n")
        print(json.dumps(r, indent=2))
        ctx.close()
        raise SystemExit(0 if r["ok"] else 1)


if __name__ == "__main__":
    main()
