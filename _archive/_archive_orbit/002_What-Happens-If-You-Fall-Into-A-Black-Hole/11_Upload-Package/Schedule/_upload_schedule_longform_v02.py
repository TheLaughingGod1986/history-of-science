#!/usr/bin/env python3
"""Upload Video 002 long-form to Orbit Studio as Private, then set schedule.

Channel: History of Science (TBD_CREATE_HISTORY_OF_SCIENCE_CHANNEL)
Schedule target: Thu 6 Aug 2026 19:00 UK
"""
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
VIDEO = ROOT / "09_Final-Export/blackhole_v04_UPLOAD_READY_MASTER.mp4"
THUMB = ROOT / "08_Thumbnail/blackhole_thumbnail_primary_A_falling-in_v01.png"
DESC = (ROOT / "11_Upload-Package/Descriptions/blackhole_long_description_v01.txt").read_text()
TAGS = (ROOT / "11_Upload-Package/Tags/blackhole_long_tags_v01.txt").read_text().strip()
PINNED = (
    ROOT / "11_Upload-Package/Pinned-Comments/blackhole_long_pinned-comment_v01.txt"
).read_text().strip()
TITLE = "What Happens If You Fall Into a Black Hole? History of Science"
CHANNEL = "TBD_CREATE_HISTORY_OF_SCIENCE_CHANNEL"
OUT = ROOT / "11_Upload-Package/Schedule/blackhole_longform_upload_result.json"
AUDIT = ROOT / "11_Upload-Package/Schedule/_studio_audit"
# Studio date picker: 6 Aug 2026 19:00
SCHEDULE = {"date_label": "6", "month_nav": "August", "year": "2026", "time": "19:00"}


def skip(page) -> None:
    try:
        page.get_by_role("link", name=re.compile(r"Skip", re.I)).click(timeout=1500)
    except Exception:
        pass


def dismiss(page) -> None:
    page.evaluate(
        "() => document.querySelectorAll('tp-yt-iron-overlay-backdrop').forEach(e => e.remove())"
    )
    for name in ("Dismiss", "Got it", "Not now", "Cancel"):
        try:
            b = page.get_by_role("button", name=name, exact=True)
            if b.count() and b.first.is_visible():
                b.first.click(force=True, timeout=700)
        except Exception:
            pass


def next_to_visibility(page) -> None:
    for _ in range(14):
        dismiss(page)
        dlg = page.locator("ytcp-uploads-dialog")
        text = dlg.inner_text() if dlg.count() else ""
        if "Save or publish" in text or (
            page.get_by_role("heading", name="Visibility", exact=True).count()
            and page.get_by_text("Private", exact=False).count()
        ):
            if "Public" in text and "Private" in text:
                return
        nxt = page.get_by_role("button", name="Next", exact=True)
        if nxt.count() and nxt.first.is_enabled():
            nxt.first.click(force=True)
            page.wait_for_timeout(1600)
        else:
            break


def extract_vid(page) -> str:
    body = page.locator("body").inner_text()
    for pat in (
        r"https://youtu\.be/([A-Za-z0-9_-]+)",
        r"youtube\.com/watch\?v=([A-Za-z0-9_-]+)",
        r"/video/([A-Za-z0-9_-]{6,})/",
    ):
        m = re.search(pat, body)
        if m and m.group(1) not in ("upload", "shorts"):
            return m.group(1)
    m = re.search(r"/video/([A-Za-z0-9_-]{6,})/", page.url)
    return m.group(1) if m else ""


def main() -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    result: dict = {
        "ok": False,
        "title": TITLE,
        "source": str(VIDEO),
        "schedule_target": "2026-08-06T19:00:00+01:00",
        "channel": CHANNEL,
    }
    if not VIDEO.exists():
        raise SystemExit(f"Missing video: {VIDEO}")

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            PROFILE,
            headless=False,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"],
            viewport={"width": 1440, "height": 900},
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()

        # Feature check
        page.goto(
            f"https://studio.youtube.com/channel/{CHANNEL}/editing/features",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(3000)
        skip(page)
        feat = page.locator("body").inner_text()
        result["features_snippet"] = feat[:1200]
        page.screenshot(path=str(AUDIT / "00_features.png"))
        if "Intermediate features" in feat and "Enabled" in feat:
            result["intermediate"] = "likely_enabled"
        elif "Eligible" in feat:
            result["intermediate"] = "eligible_not_enabled"
        else:
            result["intermediate"] = "unknown"

        page.goto(
            f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload?d=ud",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(2500)
        skip(page)
        dismiss(page)

        uploaded = False
        inputs = page.locator('input[type="file"]')
        if inputs.count():
            try:
                inputs.first.set_input_files(str(VIDEO))
                uploaded = True
            except Exception as e:
                result["file_input_err"] = str(e)[:160]
        if not uploaded:
            try:
                page.get_by_role("button", name="Select files").click(force=True)
                page.wait_for_timeout(500)
            except Exception:
                page.get_by_role("button", name="Create").click(force=True)
                page.wait_for_timeout(800)
            with page.expect_file_chooser(timeout=30000) as fc:
                page.get_by_role("button", name="Select files").click(force=True)
            fc.value.set_files(str(VIDEO))

        # Wait for title field OR error about length
        try:
            title_box = page.get_by_role(
                "textbox", name=re.compile(r"title that describes", re.I)
            )
            title_box.wait_for(timeout=300000)
        except Exception:
            body = page.locator("body").inner_text()
            page.screenshot(path=str(AUDIT / "01_upload_fail.png"))
            result["error"] = "title_box_timeout"
            result["body_snip"] = body[:2000]
            if "too long" in body.lower() or "15 minutes" in body.lower():
                result["blocker"] = "video_too_long_needs_intermediate_features"
            OUT.write_text(json.dumps(result, indent=2) + "\n")
            print(json.dumps(result, indent=2))
            ctx.close()
            return

        page.wait_for_timeout(2000)
        title_box.fill(TITLE)
        desc = page.get_by_role(
            "textbox", name=re.compile(r"tell viewers about your video", re.I)
        )
        desc.click(force=True)
        desc.fill(DESC)

        try:
            page.get_by_text("No, it's not 'Made for Kids'", exact=False).click(force=True)
        except Exception:
            pass
        try:
            page.get_by_role("radio", name=re.compile(r"Yes, AI was used", re.I)).click(
                force=True, timeout=3000
            )
        except Exception:
            pass

        try:
            page.get_by_role("button", name="Show more").click(force=True, timeout=2500)
            page.wait_for_timeout(400)
            page.get_by_role("textbox", name="Tags").fill(TAGS)
            page.keyboard.press("Enter")
            result["tags"] = True
        except Exception as e:
            result["tags_err"] = str(e)[:160]

        try:
            thumbs = page.locator('input[type="file"][accept*="image"]')
            if thumbs.count() == 0:
                page.get_by_text("Upload thumbnail", exact=False).first.click(force=True)
                page.wait_for_timeout(400)
                thumbs = page.locator('input[type="file"]')
            if thumbs.count() and THUMB.exists():
                thumbs.last.set_input_files(str(THUMB))
                page.wait_for_timeout(2000)
                result["thumb_a"] = True
        except Exception as e:
            result["thumb_err"] = str(e)[:200]

        try:
            page.get_by_text("Add a first comment", exact=False).first.click(
                force=True, timeout=2000
            )
            page.wait_for_timeout(300)
            page.keyboard.type(PINNED)
            result["first_comment"] = True
        except Exception:
            pass

        page.screenshot(path=str(AUDIT / "02_details.png"))
        next_to_visibility(page)
        page.screenshot(path=str(AUDIT / "03_visibility.png"))

        # Schedule radio
        try:
            page.get_by_text("Schedule", exact=True).first.click(force=True, timeout=4000)
            page.wait_for_timeout(800)
            # Date/time fields vary; fill visible time box if present
            time_box = page.get_by_label(re.compile(r"time", re.I))
            if time_box.count():
                time_box.first.fill(SCHEDULE["time"])
            result["schedule_ui"] = True
        except Exception as e:
            result["schedule_ui_err"] = str(e)[:200]
            # fallback Private save
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

        # Save / Schedule done
        for label in ("Schedule", "Save", "Done"):
            try:
                btn = page.get_by_role("button", name=label, exact=True)
                if btn.count() and btn.last.is_enabled():
                    btn.last.click(force=True)
                    result["finalize"] = label
                    break
            except Exception:
                pass
        page.wait_for_timeout(10000)
        page.screenshot(path=str(AUDIT / "04_after_save.png"))

        # Detect processing abandoned
        body = page.locator("body").inner_text()
        if "too long" in body.lower() or "Processing abandoned" in body:
            result["blocker"] = "video_too_long_or_processing_abandoned"
            result["body_snip"] = body[:1500]

        vid = extract_vid(page)
        result["video_id"] = vid
        result["url"] = f"https://youtu.be/{vid}" if vid else ""
        result["ok"] = bool(vid) and "blocker" not in result
        OUT.write_text(json.dumps(result, indent=2) + "\n")
        print(json.dumps(result, indent=2))
        ctx.close()


if __name__ == "__main__":
    main()
