#!/usr/bin/env python3
"""Probe how Image/Nano Banana attaches style refs on CDP :9222 (NEW tab)."""
from __future__ import annotations

import json
import os
import re
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))
import orbit_flow_veo_ui as flow  # noqa: E402

CDP = "http://127.0.0.1:9222"
PINNED = "https://flow.google.com/project/30a34afb-8d9c-4eac-83ba-012d97f6b1b5"
REF = (
    REPO
    / "01_Character/05_Generation-References/hos-explorer-reference-v01.jpg"
)
OUT = Path(__file__).resolve().parent / "covers_live_v02" / "stills" / "_qa_mint"


def main() -> int:
    from playwright.sync_api import sync_playwright

    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        ctx = browser.contexts[0]
        page = ctx.new_page()
        try:
            page.goto(PINNED, wait_until="domcontentloaded", timeout=120_000)
            page.wait_for_timeout(2500)
            flow.dismiss_banners(page)
            # lock Image 9:16
            flow._open_prompt_settings_pill(page)
            page.wait_for_timeout(700)
            page.evaluate(
                """() => {
                  for (const b of document.querySelectorAll('button[role=radio]')) {
                    const t=((b.innerText||'')+' '+(b.getAttribute('aria-label')||'')).trim();
                    if (/\\bimage\\b/i.test(t) && !/video/i.test(t)) b.click();
                  }
                }"""
            )
            page.wait_for_timeout(400)
            page.evaluate(
                """() => {
                  for (const b of document.querySelectorAll('button[role=radio]')) {
                    const t=((b.innerText||'')+' '+(b.getAttribute('aria-label')||'')).trim();
                    if (/crop_9_16|\\b9:16\\b/.test(t)) b.click();
                  }
                }"""
            )
            page.keyboard.press("Escape")
            page.wait_for_timeout(500)

            # Dump prompt-bar buttons
            dump = page.evaluate(
                """() => [...document.querySelectorAll('button,[role=button]')].map(b=>{
                  const t=(b.innerText||b.getAttribute('aria-label')||'').trim().replace(/\\n/g,' ');
                  const r=b.getBoundingClientRect();
                  if (!t || t.length>100 || r.width<8) return null;
                  if (r.y < 500) return null; // prompt bar area-ish
                  return {t:t.slice(0,100), x:Math.round(r.x), y:Math.round(r.y), w:Math.round(r.w||r.width), h:Math.round(r.height)};
                }).filter(Boolean).slice(0,80)"""
            )
            (OUT / "probe_prompt_buttons.json").write_text(json.dumps(dump, indent=2))
            page.screenshot(path=str(OUT / "probe_image_prompt_bar.png"), full_page=False)

            # Try + / add / create picker
            flow._open_create_picker(page)
            page.wait_for_timeout(800)
            page.screenshot(path=str(OUT / "probe_create_picker.png"), full_page=False)
            picker = page.evaluate(
                """() => [...document.querySelectorAll('button,[role=tab],input')].map(b=>{
                  const t=((b.innerText||'')+' '+(b.getAttribute('aria-label')||'')+' '+(b.getAttribute('type')||'')).trim().replace(/\\n/g,' ');
                  if (!t || t.length>120) return null;
                  if (!/upload|add|ingredient|media|image|file|create|asset|library|device|prompt|start|frame/i.test(t)) return null;
                  const r=b.getBoundingClientRect();
                  return {t:t.slice(0,120), tag:b.tagName, y:Math.round(r.y), w:Math.round(r.width)};
                }).filter(Boolean).slice(0,60)"""
            )
            (OUT / "probe_picker_buttons.json").write_text(json.dumps(picker, indent=2))
            print("PROMPT_BAR", json.dumps(dump[:30], indent=2))
            print("PICKER", json.dumps(picker, indent=2))

            # Try upload explorer via file input if present
            fi = page.locator('input[type="file"]')
            print("file_inputs", fi.count())
            if fi.count():
                fi.last.set_input_files(str(REF))
                page.wait_for_timeout(3000)
                page.screenshot(path=str(OUT / "probe_after_file_input.png"), full_page=False)
                # consent
                agree = page.get_by_role("button", name=re.compile(r"^(I agree|Agree)$", re.I))
                if agree.count():
                    agree.last.click(force=True)
                    page.wait_for_timeout(1500)
                page.screenshot(path=str(OUT / "probe_after_upload.png"), full_page=False)
                att = flow._prompt_attachment_count(page)
                print("attachments_after_file_input", att)
                body = page.locator("body").inner_text(timeout=5000)[:2000]
                print("BODY_SNIP", body[:800].replace("\n", " | "))
            return 0
        finally:
            page.close()


if __name__ == "__main__":
    raise SystemExit(main())
