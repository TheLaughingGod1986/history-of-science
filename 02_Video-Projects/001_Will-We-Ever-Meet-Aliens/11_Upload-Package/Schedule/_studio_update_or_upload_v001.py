#!/usr/bin/env python3
"""Check Orbit Studio for V001; update metadata if present, else upload+schedule.

Channel: History of Science (TBD_CREATE_HISTORY_OF_SCIENCE_CHANNEL)
Schedule: Thu 7 Aug 2026 19:00 UK
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from playwright.sync_api import sync_playwright

PROFILE = "/Users/ben/code/youtube/.playwright-youtube-profile"
ROOT = Path(
    "/Users/ben/code/Orbit-YouTube/02_Video-Projects/001_Will-We-Ever-Meet-Aliens"
)
PKG = ROOT / "11_Upload-Package"
VIDEO = ROOT / "09_Final-Export/aliens_BOLD_EXPLAINER_v17_FINAL_UPLOAD_READY_MASTER.mp4"
THUMB = (
    ROOT
    / "08_Thumbnail/GPT-Image-2-Tests/aliens_thumbnail-test-A_where-is-everybody_gpt-image-2_v01.png"
)
TITLE = (
    PKG / "Titles/aliens_long_title_v01.txt"
).read_text().strip()
DESC = (PKG / "Descriptions/aliens_long_description_v01.txt").read_text().strip()
TAGS = (PKG / "Tags/aliens_long_tags_v01.txt").read_text().strip()
PINNED = (PKG / "Pinned-Comments/aliens_long_pinned-comment_v01.txt").read_text().strip()
CHANNEL = "TBD_CREATE_HISTORY_OF_SCIENCE_CHANNEL"
OUT = PKG / "Schedule/aliens_v001_studio_update_result.json"
AUDIT = PKG / "Schedule/_studio_audit_v001"
SCHEDULE_TIME = "19:00"


def skip(page) -> None:
    try:
        page.get_by_role("link", name=re.compile(r"Skip", re.I)).click(timeout=1200)
    except Exception:
        pass


def dismiss(page) -> None:
    page.evaluate(
        "() => document.querySelectorAll('tp-yt-iron-overlay-backdrop').forEach(e => e.remove())"
    )
    for name in ("Dismiss", "Got it", "Not now", "Cancel", "Close"):
        try:
            b = page.get_by_role("button", name=name, exact=True)
            if b.count() and b.first.is_visible():
                b.first.click(force=True, timeout=700)
        except Exception:
            pass


def extract_vid(page) -> str | None:
    m = re.search(r"/video/([A-Za-z0-9_-]{11})/", page.url)
    if m:
        return m.group(1)
    try:
        html = page.content()
        m = re.search(r"/video/([A-Za-z0-9_-]{11})/", html)
        if m:
            return m.group(1)
    except Exception:
        pass
    return None


def next_to_visibility(page) -> None:
    for _ in range(14):
        dismiss(page)
        dlg = page.locator("ytcp-uploads-dialog")
        text = dlg.inner_text() if dlg.count() else ""
        if "Save or publish" in text or (
            "Visibility" in text and "Private" in text and "Public" in text
        ):
            return
        try:
            page.get_by_role("button", name="Next", exact=True).last.click(force=True)
        except Exception:
            try:
                page.get_by_role("button", name=re.compile(r"^Next$", re.I)).last.click(
                    force=True
                )
            except Exception:
                break
        page.wait_for_timeout(1200)


def fill_details(page, result: dict, *, in_upload_dialog: bool) -> None:
    title_box = page.get_by_role(
        "textbox", name=re.compile(r"title that describes|add a title", re.I)
    )
    if title_box.count() == 0:
        title_box = page.locator("#textbox").first
    title_box.first.click(force=True)
    page.keyboard.press("Meta+a")
    page.keyboard.press("Backspace")
    title_box.first.fill(TITLE)
    result["title_set"] = TITLE

    desc = page.get_by_role(
        "textbox", name=re.compile(r"tell viewers about your video", re.I)
    )
    if desc.count():
        desc.first.click(force=True)
        page.keyboard.press("Meta+a")
        page.keyboard.press("Backspace")
        desc.first.fill(DESC)
        result["desc_set"] = True

    try:
        page.get_by_text("No, it's not 'Made for Kids'", exact=False).click(force=True)
        result["made_for_kids"] = "no"
    except Exception:
        pass

    try:
        page.get_by_role("radio", name=re.compile(r"Yes, AI was used", re.I)).click(
            force=True, timeout=2500
        )
        result["ai_disclosure"] = True
    except Exception:
        pass

    # Tags
    for _ in range(5):
        page.mouse.wheel(0, 800)
        page.wait_for_timeout(200)
    try:
        page.get_by_text("Show more", exact=True).first.click(force=True, timeout=2500)
        page.wait_for_timeout(600)
    except Exception:
        pass
    try:
        tags_box = page.get_by_role("textbox", name=re.compile(r"^Tags$", re.I))
        if tags_box.count() == 0:
            tags_box = page.get_by_placeholder(re.compile(r"tag", re.I))
        tags_box.first.click(force=True)
        # clear existing chips roughly
        page.keyboard.press("Meta+a")
        page.keyboard.press("Backspace")
        tags_box.first.fill(TAGS)
        page.keyboard.press("Enter")
        result["tags_set"] = True
        result["tag_chars"] = len(TAGS)
    except Exception as e:
        result["tags_err"] = str(e)[:180]

    if THUMB.exists():
        try:
            thumbs = page.locator('input[type="file"][accept*="image"]')
            if thumbs.count() == 0:
                page.get_by_text("Upload thumbnail", exact=False).first.click(force=True)
                page.wait_for_timeout(400)
                thumbs = page.locator('input[type="file"]')
            if thumbs.count():
                thumbs.last.set_input_files(str(THUMB))
                page.wait_for_timeout(2000)
                result["thumb_set"] = True
        except Exception as e:
            result["thumb_err"] = str(e)[:180]

    if in_upload_dialog:
        try:
            page.get_by_text("Add a first comment", exact=False).first.click(
                force=True, timeout=2000
            )
            page.wait_for_timeout(300)
            page.keyboard.type(PINNED[:450])
            result["first_comment"] = True
        except Exception:
            pass


def save_edit(page, result: dict) -> None:
    for label in ("Save", "Publish", "Done"):
        try:
            btn = page.get_by_role("button", name=label, exact=True)
            if btn.count() and btn.last.is_enabled():
                btn.last.click(force=True)
                result["finalize"] = label
                page.wait_for_timeout(4000)
                return
        except Exception:
            pass
    # fallback: keyboard save
    page.keyboard.press("Meta+s")
    page.wait_for_timeout(3000)
    result["finalize"] = "meta_s_fallback"


def main() -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    result: dict = {
        "ok": False,
        "action": None,
        "title": TITLE,
        "channel": CHANNEL,
        "schedule_target": "2026-08-07T19:00:00+01:00",
        "source": str(VIDEO),
    }
    if not VIDEO.exists():
        raise SystemExit(f"Missing video: {VIDEO}")

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            PROFILE,
            headless=False,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"],
            viewport={"width": 1440, "height": 1000},
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()

        # Features
        page.goto(
            f"https://studio.youtube.com/channel/{CHANNEL}/editing/features",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(3500)
        skip(page)
        feat = page.locator("body").inner_text()
        result["features_snippet"] = feat[:1500]
        page.screenshot(path=str(AUDIT / "00_features.png"))
        low = feat.lower()
        if "intermediate features" in low and "enabled" in low and "eligible" not in low.split("intermediate features")[-1][:80]:
            result["intermediate"] = "enabled"
        elif "eligible" in low:
            result["intermediate"] = "eligible_not_enabled"
        else:
            # softer parse
            if re.search(r"Intermediate features\s*Enabled", feat, re.I):
                result["intermediate"] = "enabled"
            elif re.search(r"Intermediate features\s*Eligible", feat, re.I):
                result["intermediate"] = "eligible_not_enabled"
            else:
                result["intermediate"] = "unknown"

        # Content list search
        page.goto(
            f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(4000)
        skip(page)
        dismiss(page)
        page.screenshot(path=str(AUDIT / "01_content.png"))

        body = page.locator("body").inner_text()
        result["content_snip"] = body[:2500]
        candidates = []
        # Collect video links/titles mentioning aliens/fermi/alone
        for a in page.locator("a[href*='/video/']").all()[:80]:
            try:
                href = a.get_attribute("href") or ""
                txt = (a.inner_text() or "").strip()
                m = re.search(r"/video/([A-Za-z0-9_-]{11})", href)
                if not m:
                    continue
                blob = f"{txt} {href}".lower()
                if any(
                    k in blob
                    for k in (
                        "alien",
                        "fermi",
                        "alone",
                        "everybody",
                        "meet aliens",
                    )
                ):
                    candidates.append({"id": m.group(1), "text": txt[:120], "href": href})
            except Exception:
                pass
        # de-dupe
        seen = set()
        uniq = []
        for c in candidates:
            if c["id"] not in seen:
                seen.add(c["id"])
                uniq.append(c)
        result["candidates"] = uniq

        existing_id = uniq[0]["id"] if uniq else None

        if existing_id:
            result["action"] = "update_existing"
            result["video_id"] = existing_id
            page.goto(
                f"https://studio.youtube.com/video/{existing_id}/edit",
                wait_until="domcontentloaded",
                timeout=120000,
            )
            page.wait_for_timeout(4500)
            skip(page)
            dismiss(page)
            fill_details(page, result, in_upload_dialog=False)
            page.screenshot(path=str(AUDIT / "02_edit_filled.png"))
            save_edit(page, result)
            page.screenshot(path=str(AUDIT / "03_edit_saved.png"))
            result["url"] = f"https://youtu.be/{existing_id}"
            result["ok"] = True
        else:
            result["action"] = "upload_new"
            if result.get("intermediate") == "eligible_not_enabled":
                result["blocker"] = "intermediate_features_not_enabled"
                result["ok"] = False
                OUT.write_text(json.dumps(result, indent=2) + "\n")
                print(json.dumps(result, indent=2))
                ctx.close()
                return

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
                    pass
                with page.expect_file_chooser(timeout=30000) as fc:
                    page.get_by_role("button", name="Select files").click(force=True)
                fc.value.set_files(str(VIDEO))

            try:
                title_box = page.get_by_role(
                    "textbox", name=re.compile(r"title that describes", re.I)
                )
                title_box.wait_for(timeout=360000)
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
            fill_details(page, result, in_upload_dialog=True)
            page.screenshot(path=str(AUDIT / "02_upload_details.png"))
            next_to_visibility(page)
            page.screenshot(path=str(AUDIT / "03_visibility.png"))

            # Prefer Schedule
            try:
                page.get_by_text("Schedule", exact=True).first.click(force=True, timeout=4000)
                page.wait_for_timeout(1000)
                time_box = page.get_by_label(re.compile(r"time", re.I))
                if time_box.count():
                    time_box.first.fill(SCHEDULE_TIME)
                # Try set date 7 Aug if date button present
                try:
                    page.get_by_label(re.compile(r"date", re.I)).first.click(force=True)
                    page.wait_for_timeout(600)
                    # navigate month if needed
                    for _ in range(3):
                        hdr = page.locator("body").inner_text()
                        if "August" in hdr and "2026" in hdr:
                            break
                        try:
                            page.get_by_role("button", name=re.compile(r"next month", re.I)).click(
                                force=True, timeout=1000
                            )
                        except Exception:
                            break
                        page.wait_for_timeout(400)
                    page.get_by_role("button", name=re.compile(r"^7$", re.I)).first.click(
                        force=True, timeout=2000
                    )
                    result["schedule_date_clicked"] = "7"
                except Exception as e:
                    result["schedule_date_err"] = str(e)[:160]
                result["schedule_ui"] = True
            except Exception as e:
                result["schedule_ui_err"] = str(e)[:200]
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
                result["fallback_private"] = True

            for label in ("Schedule", "Save", "Done"):
                try:
                    btn = page.get_by_role("button", name=label, exact=True)
                    if btn.count() and btn.last.is_enabled():
                        btn.last.click(force=True)
                        result["finalize"] = label
                        break
                except Exception:
                    pass
            page.wait_for_timeout(12000)
            page.screenshot(path=str(AUDIT / "04_after_save.png"))
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
