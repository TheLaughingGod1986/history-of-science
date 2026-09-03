#!/usr/bin/env python3
"""Open @OrbitWithBen Studio via existing Chrome CDP :9222.

Probe login, list scheduled Content, try owner-download of Europa + Neutron Star.
Does not kill the Threads tab already on this Chrome.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

CDP = "http://127.0.0.1:9222"
CHANNEL = "UC_esArsDKd3GJvOkeO0DUog"
AUDIT = Path(
    "/Users/benjaminoats/YouTube/History Of Science/00_Brand/Channel-Setup/audits/"
    "studio_schedule_fill_2026-09-01"
)
OUT_JSON = AUDIT / "probe.json"

DOWNLOADS = {
    "NbW5G1BpPY0": Path(
        "/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/"
        "006_Could-Life-Exist-Under-The-Ice-Of-Europa/09_Final-Export/"
        "europa_v02_STUDIO_OWNER.mp4"
    ),
    "Yk1tLh23rko": Path(
        "/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/"
        "007_What-Happens-To-Your-Body-Near-A-Neutron-Star/09_Final-Export/"
        "neutron_star_STUDIO_OWNER.mp4"
    ),
}


def shot(page, name: str) -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(AUDIT / f"{name}.png"), full_page=False)


def dismiss(page) -> None:
    for name in ("Got it", "Dismiss", "Close", "Not now", "No thanks", "I understand"):
        try:
            b = page.get_by_role("button", name=name, exact=True)
            if b.count() and b.first.is_visible():
                b.first.click(force=True, timeout=800)
        except Exception:
            pass


def try_download(page, video_id: str, dest: Path) -> dict:
    dest.parent.mkdir(parents=True, exist_ok=True)
    page.goto(
        f"https://studio.youtube.com/video/{video_id}/edit",
        wait_until="domcontentloaded",
        timeout=120_000,
    )
    page.wait_for_timeout(4000)
    dismiss(page)
    shot(page, f"edit_{video_id}")
    rec = {"id": video_id, "url": page.url, "download": None}
    if "accounts.google.com" in page.url or "signin" in page.url.lower():
        rec["error"] = "signin"
        return rec
    # Prefer explicit Download controls.
    for name in ("Download", "Download video", "Download file"):
        loc = page.get_by_role("button", name=re.compile(name, re.I))
        if loc.count():
            try:
                with page.expect_download(timeout=600_000) as dl:
                    loc.first.click(force=True)
                downloaded = dl.value
                downloaded.save_as(str(dest))
                rec["download"] = str(dest)
                rec["bytes"] = dest.stat().st_size
                return rec
            except Exception as e:
                rec["click_error"] = f"{name}: {e}"
    # Overflow / more-actions menus
    for sel in (
        'button[aria-label*="More"]',
        'button[aria-label*="Actions"]',
        "ytcp-button#overflow-button",
    ):
        try:
            loc = page.locator(sel)
            if loc.count():
                loc.first.click(force=True, timeout=1500)
                page.wait_for_timeout(600)
        except Exception:
            pass
    body = page.locator("body").inner_text()[:4000]
    rec["has_download_word"] = "Download" in body
    rec["body_head"] = body[:800]
    return rec


def main() -> int:
    AUDIT.mkdir(parents=True, exist_ok=True)
    result: dict = {"ok": False, "downloads": []}
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        ctx = browser.contexts[0] if browser.contexts else None
        if ctx is None:
            result["error"] = "no_cdp_context"
            OUT_JSON.write_text(json.dumps(result, indent=2))
            print(json.dumps(result, indent=2))
            return 2
        page = ctx.new_page()
        page.set_viewport_size({"width": 1440, "height": 900})
        page.goto(
            f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload",
            wait_until="domcontentloaded",
            timeout=120_000,
        )
        page.wait_for_timeout(5000)
        dismiss(page)
        result["studio_url"] = page.url
        shot(page, "studio_content")
        if "accounts.google.com" in page.url:
            result["error"] = "signin_wall"
            OUT_JSON.write_text(json.dumps(result, indent=2))
            print(json.dumps(result, indent=2))
            return 3
        body = page.locator("body").inner_text()
        result["body_head"] = body[:1500]
        result["mentions"] = {
            "europa": "Europa" in body or "Ice" in body,
            "neutron": "Neutron" in body,
            "recycling": "Recycling" in body,
        }
        # Scheduled filter if present
        try:
            page.get_by_text("Scheduled", exact=False).first.click(timeout=3000)
            page.wait_for_timeout(2500)
            shot(page, "studio_scheduled")
            result["scheduled_body"] = page.locator("body").inner_text()[:2000]
        except Exception as e:
            result["scheduled_click"] = str(e)

        for vid, dest in DOWNLOADS.items():
            rec = try_download(page, vid, dest)
            result["downloads"].append(rec)
            print("download", rec, flush=True)

        result["ok"] = True
        # leave the Studio tab open for the next pass
        OUT_JSON.write_text(json.dumps(result, indent=2))
        print(json.dumps({k: result[k] for k in result if k != "body_head"}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
