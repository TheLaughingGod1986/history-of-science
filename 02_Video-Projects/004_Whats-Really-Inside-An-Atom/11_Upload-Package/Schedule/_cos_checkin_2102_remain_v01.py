#!/usr/bin/env python3
"""CoS 21:02 remain — clear 2-slot T&C if possible; end screen via Details (not /endscreen).

Named selectors only. Audience re-read after every save. Altered left as No.
"""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright

PORT = 9460
CHANNEL = "UCXp7HkBIl1LgaznXuZHJyRg"
VID = "GHZDsiH7L7A"
VID_002 = "AL_-qlWko_g"
PROJ = Path(__file__).resolve().parents[2]
EV = PROJ / "11_Upload-Package/Schedule/evidence_2026-09-29_studio"
ART = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts/hos004_cos_2102"
BEN = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts"

# Reuse safe helpers from main check-in script
import importlib.util

_SPEC = importlib.util.spec_from_file_location(
    "cos2102", Path(__file__).resolve().parent / "_cos_checkin_2102_growth_fix_v01.py"
)
cos = importlib.util.module_from_spec(_SPEC)
assert _SPEC.loader
_SPEC.loader.exec_module(cos)


def log(m: str) -> None:
    cos.log("REMAIN " + m)


def dump(n, o):
    cos.dump(n, o)


def shot(page, n, ben=True):
    return cos.shot(page, n, ben=ben)


def main() -> dict:
    ART.mkdir(parents=True, exist_ok=True)
    result = {"at": datetime.now().isoformat(timespec="seconds"), "phase": "remain"}
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
        ctx = browser.contexts[0] if browser.contexts else browser.new_context()
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        cos.channel_ok(page)
        cos.open_edit(page)
        result["audience_0"] = cos.ensure_not_kids(page, context="remain_start")

        # ── Cancel any "Run a new test?" dialog left open ──
        try:
            page.get_by_role("button", name=re.compile(r"^Cancel$", re.I)).first.click(timeout=1500)
            log("cancelled Run a new test dialog")
            result["cancelled_new_test_dialog"] = True
            page.wait_for_timeout(600)
        except Exception:
            result["cancelled_new_test_dialog"] = False
        cos.dismiss(page)

        # ── Try to remove the existing 2-slot A/B title test ──
        tc = {"actions": []}
        shot(page, "COS2102R_tc_BEFORE.png")
        # Click A/B Testing button near titles (not Edit title)
        clicked_ab = page.evaluate(
            """() => {
              let hit=null;
              const walk=(r,d=0)=>{
                if(!r||d>55||hit) return;
                for (const el of (r.querySelectorAll
                  ? r.querySelectorAll('button,[role=button],a,ytcp-button') : [])) {
                  const t=(el.innerText||el.getAttribute('aria-label')||'').trim();
                  if (!/A\\/B Testing|Test & Compare|Remove test|End test|Delete test/i.test(t))
                    continue;
                  if (/Edit title/i.test(t)) continue;
                  if (t.length>40) continue;
                  const rect=el.getBoundingClientRect();
                  if (rect.y<80||rect.width<5) continue;
                  el.click(); hit=t; return;
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                  if(el.shadowRoot) walk(el.shadowRoot,d+1);
              };
              walk(document); return hit;
            }"""
        )
        tc["actions"].append({"clicked_ab": clicked_ab})
        page.wait_for_timeout(1200)
        shot(page, "COS2102R_tc_DIALOG.png")

        # If "Run a new test?" → Cancel (do not start another while Ineligible)
        body = page.inner_text("body")
        if re.search(r"current test will be deleted|Run a new test", body, re.I):
            try:
                page.get_by_role("button", name=re.compile(r"^Cancel$", re.I)).first.click(
                    timeout=1500
                )
                tc["actions"].append("cancelled_replace_dialog")
                page.wait_for_timeout(500)
            except Exception:
                pass

        # Look for Remove / End / Delete on any open panel
        for pat in (
            r"^Remove test$",
            r"^End test$",
            r"^Delete test$",
            r"^Stop test$",
            r"^Remove$",
            r"^Delete$",
        ):
            try:
                page.get_by_role("button", name=re.compile(pat, re.I)).first.click(timeout=1000)
                tc["actions"].append(f"clicked_{pat}")
                page.wait_for_timeout(1000)
                # Confirm if asked
                try:
                    page.get_by_role(
                        "button", name=re.compile(r"^Remove$|^Delete$|^Confirm$|^Yes$", re.I)
                    ).first.click(timeout=800)
                    tc["actions"].append("confirmed_remove")
                except Exception:
                    pass
                break
            except Exception:
                continue

        cos.dismiss(page)
        cos.open_edit(page)
        result["audience_after_tc"] = cos.ensure_not_kids(page, context="after_tc_remain")
        tc["after"] = cos.read_tc_state(page)
        shot(page, "COS2102R_tc_AFTER.png")
        # If still 2-slot + Ineligible: record blocker — cannot clear via UI while Ineligible
        if tc["after"].get("two_slot_title_test") and tc["after"].get("ineligible"):
            tc["blocker"] = (
                "Studio shows Ineligible A/B testing titles (2 slots: Atom + Periodic). "
                "No Remove/End control while Ineligible. Do NOT Continue 'Run a new test' "
                "(would scramble). Clear/re-arm after 15 Oct public: 3 pairs or Thumbnail-only."
            )
        result["tc"] = tc
        log(f"T&C after titles={tc['after'].get('titles_present')} ineligible={tc['after'].get('ineligible')}")

        # ── End screen via Details → End screen card (finish6 path), NOT /endscreen URL ──
        es = {"actions": []}
        cos.open_edit(page)
        # Scroll to End screen card in right rail / bottom
        for _ in range(20):
            if re.search(r"End screen", page.inner_text("body"), re.I):
                break
            page.keyboard.press("PageDown")
            page.wait_for_timeout(100)
        # Click End screen entry point
        hit = page.evaluate(
            """() => {
              let hit=null;
              const walk=(r,d=0)=>{
                if(!r||d>55||hit) return;
                for (const el of (r.querySelectorAll
                  ? r.querySelectorAll('a,button,[role=button],ytcp-button,div,span') : [])) {
                  const t=(el.innerText||el.getAttribute('aria-label')||'').trim();
                  if (t!=='End screen' && t!=='ADD' && !/^End screen$/i.test(t)) continue;
                  if (t.length>20) continue;
                  const rect=el.getBoundingClientRect();
                  if (rect.width<5||rect.height<5) continue;
                  // Prefer right-rail / lower area
                  if (rect.y<100) continue;
                  el.click(); hit={t, y:Math.round(rect.y)}; return;
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                  if(el.shadowRoot) walk(el.shadowRoot,d+1);
              };
              walk(document); return hit;
            }"""
        )
        es["actions"].append({"open": hit})
        page.wait_for_timeout(3500)
        cos.dismiss(page)
        shot(page, "COS2102R_endscreen_BEFORE.png")
        body = page.inner_text("body")
        es["oops"] = bool(re.search(r"Oops, something went wrong", body, re.I))
        es["url"] = page.url

        if es["oops"]:
            # Try Editor tab
            page.goto(
                f"https://studio.youtube.com/video/{VID}/editor",
                wait_until="commit",
                timeout=90000,
            )
            page.wait_for_timeout(4000)
            cos.dismiss(page)
            page.evaluate(
                """() => {
                  const walk=(r,d=0)=>{
                    if(!r||d>55) return;
                    for (const el of (r.querySelectorAll
                      ? r.querySelectorAll('a,button,[role=button],div,span') : [])) {
                      const t=(el.innerText||'').trim();
                      if (/^End screen$/i.test(t) && t.length<=20) { el.click(); return t; }
                    }
                    for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                      if(el.shadowRoot) walk(el.shadowRoot,d+1);
                  };
                  walk(document);
                }"""
            )
            page.wait_for_timeout(3500)
            shot(page, "COS2102R_endscreen_editor.png")
            body = page.inner_text("body")
            es["oops_editor"] = bool(re.search(r"Oops, something went wrong", body, re.I))
            es["actions"].append("tried_editor")

        if not re.search(r"Oops, something went wrong", page.inner_text("body"), re.I):
            # Import template or add elements
            for pat in (
                r"IMPORT FROM VIDEO|Import from video",
                r"ADD ELEMENT|Add element",
                r"^Template$",
            ):
                try:
                    page.get_by_role("button", name=re.compile(pat, re.I)).first.click(timeout=1500)
                    es["actions"].append(pat)
                    page.wait_for_timeout(1000)
                    break
                except Exception:
                    pass
            # Prefer template with 1 video + subscribe if offered
            page.evaluate(
                """() => {
                  const walk=(r,d=0)=>{
                    if(!r||d>55) return;
                    for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                      const t=(el.innerText||'').trim().replace(/\\s+/g,' ');
                      if (/1 video.*subscribe|Subscribe.*video|Video and subscribe/i.test(t)
                          && t.length<80) {
                        el.click(); return t.slice(0,80);
                      }
                    }
                    for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                      if(el.shadowRoot) walk(el.shadowRoot,d+1);
                  };
                  walk(document);
                }"""
            )
            page.wait_for_timeout(800)
            # Specific video → 002
            try:
                page.get_by_role(
                    "radio", name=re.compile(r"Specific video", re.I)
                ).first.click(timeout=1500)
                es["actions"].append("specific_radio")
            except Exception:
                page.evaluate(
                    """() => {
                      const walk=(r,d=0)=>{
                        if(!r||d>55) return;
                        for (const el of (r.querySelectorAll
                          ? r.querySelectorAll('[role=radio],button,div,span') : [])) {
                          const t=(el.innerText||el.getAttribute('aria-label')||'').trim();
                          if (/^Specific video$/i.test(t) || /Specific video/i.test(t) && t.length<30) {
                            el.click(); return t;
                          }
                        }
                        for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                          if(el.shadowRoot) walk(el.shadowRoot,d+1);
                      };
                      walk(document);
                    }"""
                )
                es["actions"].append("specific_deep")
            page.wait_for_timeout(600)
            try:
                page.keyboard.type(VID_002, delay=20)
            except Exception:
                pass
            page.wait_for_timeout(1500)
            page.evaluate(
                """() => {
                  const walk=(r,d=0)=>{
                    if(!r||d>55) return;
                    for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                      const t=(el.innerText||'').trim();
                      if (/Periodic Table|AL_-qlWko_g|How Did We Discover the Periodic/i.test(t)
                          && t.length<120) {
                        const rect=el.getBoundingClientRect();
                        if (rect.width>20) { el.click(); return t.slice(0,80); }
                      }
                    }
                    for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                      if(el.shadowRoot) walk(el.shadowRoot,d+1);
                  };
                  walk(document);
                }"""
            )
            es["actions"].append("picked_002")
            page.wait_for_timeout(800)
            # Subscribe
            try:
                page.get_by_role("button", name=re.compile(r"^Subscribe$", re.I)).first.click(
                    timeout=1500
                )
                es["actions"].append("subscribe")
            except Exception:
                page.evaluate(
                    """() => {
                      const walk=(r,d=0)=>{
                        if(!r||d>55) return;
                        for (const el of (r.querySelectorAll
                          ? r.querySelectorAll('button,[role=button]') : [])) {
                          const t=(el.innerText||'').trim();
                          if (t==='Subscribe') { el.click(); return true; }
                        }
                        for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                          if(el.shadowRoot) walk(el.shadowRoot,d+1);
                      };
                      walk(document);
                    }"""
                )
                es["actions"].append("subscribe_deep")
            es["saved"] = cos.save_named(page)
            page.wait_for_timeout(2500)
            body = page.inner_text("body")
            es["processing_error"] = bool(
                re.search(r"problem in processing|couldn.?t be saved|NaN|Oops", body, re.I)
            )
            es["has_002"] = bool(
                re.search(r"Periodic Table|AL_-qlWko_g|How Did We Discover the Periodic", body, re.I)
            )
            es["has_subscribe"] = bool(re.search(r"Subscribe", body, re.I))
            es["ok"] = bool(es.get("saved")) and not es.get("processing_error")
        else:
            es["ok"] = False
            es["blocker"] = (
                "Studio End screen surfaces Oops (dedicated URL + Details/Editor entry). "
                "Same processing block as prior UAT. Re-set Specific 002 + Subscribe after "
                "processing settles / on launch day 15 Oct."
            )

        shot(page, "COS2102R_endscreen_AFTER.png")
        cos.open_edit(page)
        result["audience_final"] = cos.ensure_not_kids(page, context="remain_final")
        cos.show_more(page)
        for _ in range(20):
            if re.search(r"AI wasn|AI was used|Altered", page.inner_text("body"), re.I):
                break
            page.keyboard.press("PageDown")
            page.wait_for_timeout(80)
        result["altered_final"] = cos.read_ai_altered(page)
        shot(page, "COS2102R_FINAL.png")
        result["endscreen"] = es
        result["summary"] = {
            "audience_not_kids": result["audience_final"].get("ok_not_kids"),
            "altered_no": result["altered_final"].get("no") is True,
            "tc_two_slot": tc["after"].get("two_slot_title_test"),
            "tc_ineligible": tc["after"].get("ineligible"),
            "tc_blocker": tc.get("blocker"),
            "endscreen_ok": es.get("ok"),
            "endscreen_blocker": es.get("blocker"),
        }
        dump("COS_CHECKIN_2102_REMAIN_RESULT.json", result)
        log(f"SUMMARY {result['summary']}")
        return result


if __name__ == "__main__":
    main()
