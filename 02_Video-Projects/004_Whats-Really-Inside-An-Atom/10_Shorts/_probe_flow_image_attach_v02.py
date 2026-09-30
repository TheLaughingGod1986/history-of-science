#!/usr/bin/env python3
"""Click Add-ingredients in Image mode and upload a style ref."""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))
import orbit_flow_veo_ui as flow  # noqa: E402

CDP = "http://127.0.0.1:9222"
PINNED = "https://flow.google.com/project/30a34afb-8d9c-4eac-83ba-012d97f6b1b5"
REF = REPO / "01_Character/05_Generation-References/hos-explorer-reference-v01.jpg"
OUT = Path(__file__).resolve().parent / "covers_live_v02" / "stills" / "_qa_mint"


def lock_916(page):
    flow._open_prompt_settings_pill(page)
    page.wait_for_timeout(600)
    page.evaluate(
        """() => {
          for (const b of document.querySelectorAll('button[role=radio]')) {
            const t=((b.innerText||'')+' '+(b.getAttribute('aria-label')||'')).trim();
            if (/\\bimage\\b/i.test(t) && !/video/i.test(t)) b.click();
          }
        }"""
    )
    page.wait_for_timeout(300)
    page.evaluate(
        """() => {
          for (const b of document.querySelectorAll('button[role=radio]')) {
            const t=((b.innerText||'')+' '+(b.getAttribute('aria-label')||'')).trim();
            if (/crop_9_16|\\b9:16\\b/.test(t)) b.click();
          }
        }"""
    )
    page.keyboard.press("Escape")
    page.wait_for_timeout(400)


def main() -> int:
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        page = browser.contexts[0].new_page()
        try:
            page.goto(PINNED, wait_until="domcontentloaded", timeout=120_000)
            page.wait_for_timeout(2200)
            flow.dismiss_banners(page)
            lock_916(page)

            # Click Add ingredients
            add = page.get_by_role(
                "button",
                name=re.compile(r"Add ingredients|add Add ingredients|ingredients", re.I),
            )
            print("add_role_count", add.count())
            if add.count() == 0:
                add = page.locator(
                    'button[aria-label*="ingredient" i], button:has-text("add")'
                ).last
            else:
                add = add.last
            add.click(force=True, timeout=5000)
            page.wait_for_timeout(900)
            page.screenshot(path=str(OUT / "probe_ingredients_menu.png"), full_page=False)
            menu = page.evaluate(
                """() => [...document.querySelectorAll('button,[role=menuitem],input,[role=option]')].map(b=>{
                  const t=((b.innerText||'')+' '+(b.getAttribute('aria-label')||'')+' '+(b.type||'')).trim().replace(/\\n/g,' ');
                  if (!t || t.length>140) return null;
                  const r=b.getBoundingClientRect();
                  if (r.width<6) return null;
                  return {t:t.slice(0,140), tag:b.tagName, y:Math.round(r.y), w:Math.round(r.width), type:b.type||''};
                }).filter(Boolean).slice(0,80)"""
            )
            (OUT / "probe_ingredients_menu.json").write_text(json.dumps(menu, indent=2))
            print(json.dumps(menu, indent=2)[:4000])

            # Prefer Upload
            up = page.get_by_role("button", name=re.compile(r"Upload", re.I))
            print("upload_btns", up.count())
            fi = page.locator('input[type=file]')
            print("file_inputs_after_add", fi.count())
            if up.count():
                try:
                    with page.expect_file_chooser(timeout=12000) as fc:
                        up.last.click(force=True)
                    fc.value.set_files(str(REF))
                    print("uploaded via chooser")
                except Exception as e:
                    print("chooser fail", e)
                    if fi.count():
                        fi.last.set_input_files(str(REF))
                        print("uploaded via hidden input")
            elif fi.count():
                fi.last.set_input_files(str(REF))
                print("uploaded via hidden input direct")
            else:
                # try Upload media text
                for lab in ("Upload media", "Upload", "From device"):
                    loc = page.locator(f'button:has-text("{lab}")')
                    if loc.count():
                        try:
                            with page.expect_file_chooser(timeout=10000) as fc:
                                loc.last.click(force=True)
                            fc.value.set_files(str(REF))
                            print("uploaded via", lab)
                            break
                        except Exception as e:
                            print(lab, e)

            page.wait_for_timeout(2500)
            for _ in range(5):
                agree = page.get_by_role("button", name=re.compile(r"^(I agree|Agree)$", re.I))
                if not agree.count():
                    break
                agree.last.click(force=True)
                page.wait_for_timeout(900)
            page.wait_for_timeout(2000)
            page.screenshot(path=str(OUT / "probe_after_ingredient_upload.png"), full_page=False)
            att = flow._prompt_attachment_count(page)
            print("attachments", att)
            # Try Add to Prompt
            addp = page.locator('button:has-text("Add to Prompt")')
            print("add_to_prompt", addp.count())
            if addp.count():
                st = page.evaluate(
                    """() => {
                      const b=[...document.querySelectorAll('button')].filter(x=>/Add to Prompt/i.test(x.innerText||''));
                      if (!b.length) return null;
                      const el=b[b.length-1];
                      return {dis:!!(el.disabled||el.getAttribute('aria-disabled')==='true'), t:(el.innerText||'').slice(0,40)};
                    }"""
                )
                print("add_to_prompt_state", st)
                if st and not st.get("dis"):
                    addp.last.click(force=True)
                    page.wait_for_timeout(1200)
                    print("attachments_after_add", flow._prompt_attachment_count(page))
            page.screenshot(path=str(OUT / "probe_final_attach.png"), full_page=False)
            return 0
        finally:
            page.close()


if __name__ == "__main__":
    raise SystemExit(main())
