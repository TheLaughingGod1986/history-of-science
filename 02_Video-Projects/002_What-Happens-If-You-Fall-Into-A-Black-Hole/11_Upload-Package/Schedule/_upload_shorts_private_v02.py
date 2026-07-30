#!/usr/bin/env python3
"""Upload Video 002 Shorts as Private drafts (schedule second pass)."""
from __future__ import annotations

import json
import re
from pathlib import Path

from playwright.sync_api import sync_playwright

PROFILE = "/Users/ben/code/youtube/.playwright-youtube-profile"
ROOT = Path(
    "/Users/ben/code/Orbit-YouTube/02_Video-Projects/"
    "002_What-Happens-If-You-Fall-Into-A-Black-Hole"
)
INDEX = json.loads((ROOT / "10_Shorts/SHORTS_UPLOAD_INDEX.json").read_text())
LONG_URL = "https://youtu.be/n7CbJrOCnU0"
CHANNEL = "UC_esArsDKd3GJvOkeO0DUog"
OUT = ROOT / "11_Upload-Package/Schedule/blackhole_shorts_upload_result.json"
AUDIT = ROOT / "11_Upload-Package/Schedule/_studio_audit_shorts"


def dismiss(page) -> None:
    for name in ("Got it", "Dismiss", "Close", "Not now"):
        try:
            b = page.get_by_role("button", name=name, exact=True)
            if b.count() and b.first.is_visible():
                b.first.click(force=True, timeout=600)
        except Exception:
            pass


def next_vis(page) -> None:
    for _ in range(12):
        dismiss(page)
        text = page.locator("ytcp-uploads-dialog").inner_text() if page.locator("ytcp-uploads-dialog").count() else ""
        if "Save or publish" in text or page.get_by_text("Private", exact=False).count():
            if "Public" in text:
                return
        nxt = page.get_by_role("button", name="Next", exact=True)
        if nxt.count() and nxt.first.is_enabled():
            nxt.first.click(force=True)
            page.wait_for_timeout(1200)
        else:
            break


def extract_vid(page) -> str:
    body = page.locator("body").inner_text()
    for pat in (r"https://youtu\.be/([A-Za-z0-9_-]+)", r"/video/([A-Za-z0-9_-]{6,})/"):
        m = re.search(pat, body)
        if m:
            return m.group(1)
    return ""


def upload_one(page, item: dict) -> dict:
    path = ROOT / item["file"]
    desc = item["description"].replace("{{LONG_VIDEO_URL}}", LONG_URL)
    page.goto(
        f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload?d=ud",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(2000)
    dismiss(page)
    inputs = page.locator('input[type="file"]')
    if inputs.count():
        inputs.first.set_input_files(str(path))
    else:
        with page.expect_file_chooser(timeout=20000) as fc:
            page.get_by_role("button", name="Select files").click(force=True)
        fc.value.set_files(str(path))

    title_box = page.get_by_role("textbox", name=re.compile(r"title that describes", re.I))
    title_box.wait_for(timeout=180000)
    title_box.fill(item["title"])
    desc_box = page.get_by_role("textbox", name=re.compile(r"tell viewers about your video", re.I))
    desc_box.click(force=True)
    desc_box.fill(desc)
    try:
        page.get_by_text("No, it's not 'Made for Kids'", exact=False).click(force=True)
    except Exception:
        pass
    try:
        page.get_by_role("radio", name=re.compile(r"Yes, AI was used", re.I)).click(
            force=True, timeout=2000
        )
    except Exception:
        pass
    next_vis(page)
    # Private
    page.evaluate(
        """() => {
          const walk=(r)=>{
            if(!r)return false;
            for(const el of (r.querySelectorAll?r.querySelectorAll('tp-yt-paper-radio-button,[role=radio]'):[])){
              const t=(el.innerText||'').toLowerCase();
              if(t.includes('private') && !t.includes('schedule')){ el.click(); return true; }
            }
            for(const el of (r.querySelectorAll?r.querySelectorAll('*'):[])){
              if(el.shadowRoot && walk(el.shadowRoot)) return true;
            }
            return false;
          };
          return walk(document.querySelector('ytcp-uploads-dialog')||document);
        }"""
    )
    page.wait_for_timeout(400)
    page.get_by_role("button", name="Save", exact=True).last.click(force=True)
    page.wait_for_timeout(7000)
    dismiss(page)
    vid = extract_vid(page)
    try:
        page.get_by_role("button", name="Close").click(force=True, timeout=2000)
    except Exception:
        pass
    return {
        "id": item["id"],
        "title": item["title"],
        "schedule_iso": item["schedule_iso"],
        "video_id": vid,
        "url": f"https://youtu.be/{vid}" if vid else "",
        "file": item["file"],
    }


def main() -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    results = []
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            PROFILE,
            headless=False,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"],
            viewport={"width": 1440, "height": 900},
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        for item in INDEX["shorts"]:
            print(f"Uploading Short {item['id']}…", flush=True)
            try:
                r = upload_one(page, item)
                results.append(r)
                print(f"  → {r.get('url') or r}", flush=True)
            except Exception as e:
                results.append({"id": item["id"], "error": str(e)[:300]})
                print(f"  ERR {e}", flush=True)
                page.screenshot(path=str(AUDIT / f"short_{item['id']}_err.png"))
        ctx.close()
    OUT.write_text(json.dumps({"long_url": LONG_URL, "shorts": results}, indent=2) + "\n")
    print(OUT)


if __name__ == "__main__":
    main()
