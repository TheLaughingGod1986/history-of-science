#!/usr/bin/env python3
"""Owner-download Europa premiere NbW5G1BpPY0 from YouTube Studio.

The 16:9 master is not on this Mac. yt-dlp cannot fetch a premiere.
Studio → that video → Download is the owner path.

Writes:
  orbit-with-ben/.../006_.../09_Final-Export/europa_v02_STUDIO_OWNER.mp4

Requires a Playwright profile actually logged into @OrbitWithBen Studio
(not the Flow-only ~/.playwright-hos-flow-profile).

  python3 00_Brand/Channel-Setup/audits/_studio_download_europa_v01.py
"""
from __future__ import annotations

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

EUROPA_ID = "NbW5G1BpPY0"
OUT = Path(
    "/Users/benjaminoats/YouTube/orbit-with-ben/02_Video-Projects/"
    "006_Could-Life-Exist-Under-The-Ice-Of-Europa/09_Final-Export/"
    "europa_v02_STUDIO_OWNER.mp4"
)
PROFILES = [
    Path.home() / ".playwright-youtube-profile",
    Path.home() / "code/youtube/.playwright-youtube-profile",
    Path.home() / ".playwright-hos-flow-profile",
]


def main() -> int:
    profile = next((p for p in PROFILES if p.exists()), None)
    if profile is None:
        print("No Playwright profile on disk. Log into Studio once, then retry.")
        return 2
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            str(profile), headless=False, accept_downloads=True
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.goto(
            f"https://studio.youtube.com/video/{EUROPA_ID}/edit",
            wait_until="domcontentloaded",
            timeout=120_000,
        )
        page.wait_for_timeout(4000)
        if "accounts.google.com" in page.url or "signin" in page.url.lower():
            print(f"Sign-in wall ({profile}). Need @OrbitWithBen Studio session.")
            ctx.close()
            return 3
        # Visibility / download controls live on the edit page.
        downloaded = None
        for name in ("Download", "Download video", "Download file"):
            loc = page.get_by_role("button", name=name)
            if loc.count():
                with page.expect_download(timeout=600_000) as dl:
                    loc.first.click()
                downloaded = dl.value
                break
        if downloaded is None:
            print("No Download control found. Open Studio as owner and use Download.")
            print("Current URL:", page.url)
            ctx.close()
            return 4
        downloaded.save_as(str(OUT))
        print("Wrote", OUT, "bytes", OUT.stat().st_size)
        ctx.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
