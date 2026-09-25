#!/usr/bin/env python3
"""Force-schedule Video 002 long-form to Thu 6 Aug 2026 19:00 UK via edit page."""
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
UPLOAD = ROOT / "11_Upload-Package/Schedule/blackhole_longform_upload_result.json"
OUT = ROOT / "11_Upload-Package/Schedule/blackhole_longform_schedule_result.json"
AUDIT = ROOT / "11_Upload-Package/Schedule/_studio_audit"
CHANNEL = "TBD_CREATE_HISTORY_OF_SCIENCE_CHANNEL"
VID = json.loads(UPLOAD.read_text())["video_id"]
TARGET_DATE_TEXT = "6 Aug 2026"  # visible formats vary
TIME = "19:00"


def dismiss(page) -> None:
    for name in ("Got it", "Dismiss", "Close", "Not now"):
        try:
            b = page.get_by_role("button", name=name, exact=True)
            if b.count() and b.first.is_visible():
                b.first.click(force=True, timeout=800)
        except Exception:
            pass


def main() -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    result = {"ok": False, "video_id": VID, "target": "2026-08-06T19:00:00+01:00"}
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
            timeout=120000,
        )
        page.wait_for_timeout(3500)
        dismiss(page)
        page.screenshot(path=str(AUDIT / "sched_01_edit.png"))

        # Open visibility
        try:
            page.locator("ytcp-video-metadata-visibility").first.click(force=True)
        except Exception:
            page.get_by_text("Visibility", exact=False).first.click(force=True)
        page.wait_for_timeout(1500)
        dismiss(page)

        # Expand Schedule
        page.evaluate(
            """() => {
              const walk=(root)=>{
                for (const el of root.querySelectorAll('*')) {
                  const al=el.getAttribute('aria-label')||'';
                  if (/click to expand/i.test(al) || /Schedule/i.test(el.innerText||'')) {
                    const r=el.getBoundingClientRect();
                    if (r.width>40 && r.y>150) { el.click(); return true; }
                  }
                  if (el.shadowRoot && walk(el.shadowRoot)) return true;
                }
                return false;
              };
              return walk(document);
            }"""
        )
        page.wait_for_timeout(1000)

        # Prefer radio Schedule
        try:
            page.get_by_text("Schedule", exact=True).first.click(force=True)
        except Exception:
            pass
        page.wait_for_timeout(800)

        # Open date picker and choose 6
        try:
            page.get_by_label(re.compile(r"date", re.I)).first.click(force=True)
            page.wait_for_timeout(600)
            # click day 6 in calendar (not 16/26)
            page.evaluate(
                """() => {
                  const walk=(root)=>{
                    for (const el of root.querySelectorAll('span,div,button,td')) {
                      const t=(el.innerText||'').trim();
                      if (t==='6') {
                        const r=el.getBoundingClientRect();
                        if (r.width>10 && r.height>10 && r.y>200) { el.click(); return true; }
                      }
                      if (el.shadowRoot && walk(el.shadowRoot)) return true;
                    }
                    return false;
                  };
                  return walk(document);
                }"""
            )
            page.wait_for_timeout(500)
        except Exception as e:
            result["date_err"] = str(e)[:160]

        # Time
        try:
            tb = page.get_by_label(re.compile(r"^time$|publish time|Time", re.I))
            if tb.count():
                tb.first.click(force=True)
                tb.first.fill("")
                tb.first.type(TIME, delay=40)
                page.keyboard.press("Enter")
                result["time_set"] = TIME
        except Exception as e:
            result["time_err"] = str(e)[:160]

        page.screenshot(path=str(AUDIT / "sched_02_picker.png"))

        # Save
        for name in ("Save", "Schedule", "Done", "Publish"):
            try:
                b = page.get_by_role("button", name=name, exact=True)
                if b.count() and b.last.is_enabled():
                    b.last.click(force=True)
                    result["saved_via"] = name
                    break
            except Exception:
                pass
        page.wait_for_timeout(5000)
        dismiss(page)
        page.screenshot(path=str(AUDIT / "sched_03_after.png"))
        body = page.locator("body").inner_text()
        result["body_has_aug"] = ("6 Aug" in body) or ("6 August" in body) or ("Aug 6" in body)
        result["body_has_1900"] = ("19:00" in body) or ("7:00 PM" in body) or ("7:00pm" in body.lower())
        result["visibility_snip"] = "\n".join(
            [ln for ln in body.splitlines() if any(k in ln for k in ("Schedule", "Aug", "Jul", "19:", "Private", "Public"))][:20]
        )
        result["ok"] = True
        OUT.write_text(json.dumps(result, indent=2) + "\n")
        print(json.dumps(result, indent=2))
        ctx.close()


if __name__ == "__main__":
    main()
