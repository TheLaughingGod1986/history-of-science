#!/usr/bin/env python3
"""Force live_v02 illustrated covers onto HOS 002 Scheduled listings.

Studio only. No remint. Never Public. @HistoryOfScienceYT CDP :9460.
Always ctx.new_page() — never reuse Facebook / Google One / Cloud Billing tabs.
"""
from __future__ import annotations

from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
CDP = "http://127.0.0.1:9460"
CHANNEL = "UCXp7HkBIl1LgaznXuZHJyRg"
EV = Path(__file__).resolve().parent / "evidence_2026-09-11_thumbs_live_v02"

JOBS = [
    {
        "slot": "s01",
        "id": "uU12JA5rMWg",
        "file": ROOT / "08_Thumbnail/Shorts/hos_002_s01_empty_chairs_cover_live_v02.jpg",
    },
    {
        "slot": "s02",
        "id": "nFQRWmpulTQ",
        "file": ROOT / "08_Thumbnail/Shorts/hos_002_s02_predict_metal_cover_live_v02.jpg",
    },
    {
        "slot": "s03",
        "id": "CnHwX1L9XHg",
        "file": ROOT / "08_Thumbnail/Shorts/hos_002_s03_gallium_cover_live_v02.jpg",
    },
    {
        "slot": "s04",
        "id": "nba0-f7PPeU",
        "file": ROOT / "08_Thumbnail/Shorts/hos_002_s04_tellurium_cover_live_v02.jpg",
    },
    {
        "slot": "s05",
        "id": "LanTHJckYx8",
        "file": ROOT / "08_Thumbnail/Shorts/hos_002_s05_other_table_cover_live_v02.jpg",
    },
    {
        "slot": "long",
        "id": "AL_-qlWko_g",
        "file": ROOT / "08_Thumbnail/Selected/hos_002_thumb_A_gallium_live_v02.jpg",
    },
]


def pick_image_input(page):
    for inp in page.locator("input[type=file]").all():
        acc = (inp.get_attribute("accept") or "").lower()
        if "video/" in acc and "image" not in acc:
            continue
        if inp.is_visible() or "image" in acc or acc in ("", "*/*"):
            return inp
    return None


def force_one(page, job: dict) -> str:
    thumb = job["file"]
    if not thumb.is_file():
        return f"{job['slot']} missing {thumb.name}"
    page.goto(
        f"https://studio.youtube.com/video/{job['id']}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(5000)
    if "studio.youtube.com" not in page.url:
        return f"{job['slot']} wrong url {page.url}"
    page.keyboard.press("Escape")
    page.wait_for_timeout(800)
    upload = page.get_by_text("Upload file", exact=True)
    if upload.count() and upload.first.is_visible():
        with page.expect_file_chooser(timeout=15000) as fc:
            upload.first.click(timeout=8000)
        chooser = fc.value
        acc = ""
        try:
            acc = (chooser.element.get_attribute("accept") or "").lower()
        except Exception:
            acc = ""
        if "video/" in acc and "image" not in acc:
            return f"{job['slot']} file chooser is video-only"
        chooser.set_files(str(thumb))
    else:
        for sel in ['ytcp-button#select-button', 'ytcp-button:has-text("Upload file")']:
            loc = page.locator(sel).first
            if loc.count() and loc.is_visible():
                loc.click(timeout=8000)
                break
        page.wait_for_timeout(1500)
        file_inp = pick_image_input(page)
        if file_inp is None:
            return f"{job['slot']} no image input"
        file_inp.set_input_files(str(thumb))
    page.wait_for_timeout(5000)
    if "studio.youtube.com" not in page.url:
        return f"{job['slot']} left Studio before save {page.url}"
    save = page.locator("#save").first
    if not (save.count() and save.is_visible()):
        return f"{job['slot']} save missing"
    if save.get_attribute("disabled") is not None:
        page.wait_for_timeout(8000)
    if save.get_attribute("disabled") is not None:
        return f"{job['slot']} save still disabled"
    save.click(timeout=8000)
    page.wait_for_timeout(8000)
    if "studio.youtube.com" not in page.url:
        return f"{job['slot']} left Studio after save {page.url}"
    EV.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(EV / f"{job['slot']}_edit.jpg"), full_page=False)
    return f"{job['slot']} saved {thumb.name}"


def shot_lists(page) -> None:
    EV.mkdir(parents=True, exist_ok=True)
    page.set_viewport_size({"width": 1440, "height": 1600})
    shorts = f"https://studio.youtube.com/channel/{CHANNEL}/videos/short"
    page.goto(shorts, wait_until="domcontentloaded", timeout=120000)
    page.wait_for_timeout(6000)
    if "studio.youtube.com" not in page.url:
        raise SystemExit("shorts list left Studio " + page.url)
    page.screenshot(path=str(EV / "studio_shorts_list.jpg"), full_page=False)
    videos = f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload"
    page.goto(videos, wait_until="domcontentloaded", timeout=120000)
    page.wait_for_timeout(6000)
    if "studio.youtube.com" not in page.url:
        raise SystemExit("videos list left Studio " + page.url)
    page.screenshot(path=str(EV / "studio_videos_list.jpg"), full_page=False)


def main() -> None:
    import sys

    wanted = {a for a in sys.argv[1:] if not a.startswith("-")}
    jobs = [j for j in JOBS if not wanted or j["slot"] in wanted]
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        ctx = browser.contexts[0]
        page = ctx.new_page()
        try:
            for job in jobs:
                print(force_one(page, job), flush=True)
            shot_lists(page)
            print("lists", EV)
        finally:
            page.close()


if __name__ == "__main__":
    main()
