#!/usr/bin/env python3
"""CoS 21:02 — finish end screen: Specific 002 + Subscribe. Named selectors; audience after save."""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
import importlib.util

from playwright.sync_api import sync_playwright

PORT = 9460
VID = "GHZDsiH7L7A"
VID_002 = "AL_-qlWko_g"
PROJ = Path(__file__).resolve().parents[2]
EV = PROJ / "11_Upload-Package/Schedule/evidence_2026-09-29_studio"
ART = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts/hos004_cos_2102"

_SPEC = importlib.util.spec_from_file_location(
    "cos2102", Path(__file__).resolve().parent / "_cos_checkin_2102_growth_fix_v01.py"
)
cos = importlib.util.module_from_spec(_SPEC)
assert _SPEC.loader
_SPEC.loader.exec_module(cos)


def log(m):
    cos.log("ES2 " + m)


def main():
    ART.mkdir(parents=True, exist_ok=True)
    out = {"at": datetime.now().isoformat(timespec="seconds"), "actions": []}
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
        ctx = browser.contexts[0]
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        cos.channel_ok(page)
        cos.open_edit(page)
        out["audience_0"] = cos.ensure_not_kids(page, context="es2_start")

        # Dismiss leftover Choose-specific-video modal if open
        for _ in range(2):
            try:
                page.get_by_role("button", name=re.compile(r"^Close$|^Cancel$", re.I)).first.click(
                    timeout=800
                )
                page.wait_for_timeout(300)
            except Exception:
                pass
            page.keyboard.press("Escape")
            page.wait_for_timeout(200)

        # Open End screen from Details right rail
        for _ in range(25):
            if re.search(r"End screen", page.inner_text("body"), re.I):
                break
            page.keyboard.press("PageDown")
            page.wait_for_timeout(80)
        page.evaluate(
            """() => {
              const walk=(r,d=0)=>{
                if(!r||d>55) return;
                for (const el of (r.querySelectorAll
                  ? r.querySelectorAll('a,button,[role=button],ytcp-button') : [])) {
                  const t=(el.innerText||el.getAttribute('aria-label')||'').trim();
                  if (t!=='End screen') continue;
                  const rect=el.getBoundingClientRect();
                  if (rect.y>200 && rect.width>5) { el.click(); return true; }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                  if(el.shadowRoot) walk(el.shadowRoot,d+1);
              };
              walk(document);
            }"""
        )
        page.wait_for_timeout(4000)
        cos.dismiss(page)
        cos.shot(page, "COS2102ES_01_open.png")
        body = page.inner_text("body")
        if re.search(r"Oops, something went wrong", body, re.I):
            out["oops"] = True
            cos.dump("COS_CHECKIN_2102_ENDSCREEN_V02.json", out)
            raise SystemExit("End screen Oops")

        # If already on element picker / canvas
        # Click ADD ELEMENT → Video if needed
        if not re.search(r"Specific video|Choose specific|Element type|Subscribe", body, re.I):
            for pat in (r"ADD ELEMENT|Add element", r"IMPORT FROM VIDEO|Import from video"):
                try:
                    page.get_by_role("button", name=re.compile(pat, re.I)).first.click(timeout=1500)
                    out["actions"].append(pat)
                    page.wait_for_timeout(1000)
                    break
                except Exception:
                    pass
            try:
                page.get_by_role("button", name=re.compile(r"^Video$", re.I)).first.click(
                    timeout=1500
                )
                out["actions"].append("Video")
                page.wait_for_timeout(1000)
            except Exception:
                page.evaluate(
                    """() => {
                      const walk=(r,d=0)=>{
                        if(!r||d>55) return;
                        for (const el of (r.querySelectorAll
                          ? r.querySelectorAll('button,[role=button]') : [])) {
                          if ((el.innerText||'').trim()==='Video') { el.click(); return; }
                        }
                        for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                          if(el.shadowRoot) walk(el.shadowRoot,d+1);
                      };
                      walk(document);
                    }"""
                )
                out["actions"].append("Video_deep")
                page.wait_for_timeout(1000)

        # Specific video radio / tab
        page.evaluate(
            """() => {
              const walk=(r,d=0)=>{
                if(!r||d>55) return;
                for (const el of (r.querySelectorAll
                  ? r.querySelectorAll('[role=radio],button,[role=tab],div,span') : [])) {
                  const t=(el.innerText||el.getAttribute('aria-label')||'').trim();
                  if (/^Specific video$/i.test(t) || t==='Specific video') {
                    el.click(); return t;
                  }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                  if(el.shadowRoot) walk(el.shadowRoot,d+1);
              };
              walk(document);
            }"""
        )
        out["actions"].append("specific")
        page.wait_for_timeout(1000)
        cos.shot(page, "COS2102ES_02_specific.png")

        # Focus search in modal and type 002 id + title keywords
        # Clear and type into visible search box
        filled = page.evaluate(
            """(q) => {
              let hit=null;
              const walk=(r,d=0)=>{
                if(!r||d>55||hit) return;
                for (const el of (r.querySelectorAll
                  ? r.querySelectorAll('input[type=text],input[type=search],input:not([type]),textarea')
                  : [])) {
                  const a=(el.getAttribute('aria-label')||el.getAttribute('placeholder')||'');
                  const rect=el.getBoundingClientRect();
                  if (rect.width<40||rect.height<10) continue;
                  if (/search|video|url/i.test(a) || rect.y>80) {
                    el.focus();
                    const proto=HTMLInputElement.prototype;
                    Object.getOwnPropertyDescriptor(proto,'value').set.call(el, q);
                    el.dispatchEvent(new Event('input',{bubbles:true}));
                    el.dispatchEvent(new Event('change',{bubbles:true}));
                    hit=a||'input';
                    return;
                  }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                  if(el.shadowRoot) walk(el.shadowRoot,d+1);
              };
              walk(document); return hit;
            }""",
            VID_002,
        )
        out["filled"] = filled
        page.wait_for_timeout(400)
        # Also keyboard type in case focus works better
        try:
            page.keyboard.press("Meta+a")
            page.keyboard.type(VID_002, delay=30)
        except Exception:
            pass
        page.wait_for_timeout(2000)
        cos.shot(page, "COS2102ES_03_search.png")

        # Click result row for Periodic Table / 002
        picked = page.evaluate(
            """() => {
              let hit=null;
              const walk=(r,d=0)=>{
                if(!r||d>55||hit) return;
                for (const el of (r.querySelectorAll
                  ? r.querySelectorAll('ytcp-video-row,ytcp-entity-card,a,div,button,tp-yt-paper-item')
                  : [])) {
                  const t=(el.innerText||'').trim().replace(/\\s+/g,' ');
                  if (!t || t.length>160) continue;
                  if (!/Periodic Table|AL_-qlWko_g|How Did We Discover the Periodic/i.test(t))
                    continue;
                  const rect=el.getBoundingClientRect();
                  if (rect.width<40||rect.height<20||rect.y<100) continue;
                  el.click(); hit=t.slice(0,100); return;
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                  if(el.shadowRoot) walk(el.shadowRoot,d+1);
              };
              walk(document); return hit;
            }"""
        )
        out["picked"] = picked
        log(f"picked={picked!r}")
        page.wait_for_timeout(1200)
        cos.shot(page, "COS2102ES_04_picked.png")

        # If search by id failed, try title search
        if not picked:
            try:
                page.keyboard.press("Meta+a")
                page.keyboard.type("How Did We Discover the Periodic Table", delay=20)
                page.wait_for_timeout(2000)
                picked = page.evaluate(
                    """() => {
                      let hit=null;
                      const walk=(r,d=0)=>{
                        if(!r||d>55||hit) return;
                        for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                          const t=(el.innerText||'').trim().replace(/\\s+/g,' ');
                          if (/How Did We Discover the Periodic Table/i.test(t) && t.length<120) {
                            const rect=el.getBoundingClientRect();
                            if (rect.width>40&&rect.height>20&&rect.y>120) {
                              el.click(); hit=t.slice(0,100); return;
                            }
                          }
                        }
                        for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                          if(el.shadowRoot) walk(el.shadowRoot,d+1);
                      };
                      walk(document); return hit;
                    }"""
                )
                out["picked_title"] = picked
                page.wait_for_timeout(1000)
                cos.shot(page, "COS2102ES_04b_picked_title.png")
            except Exception as e:
                out["title_search_err"] = type(e).__name__

        # Add Subscribe element if not present
        body = page.inner_text("body")
        if not re.search(r"Subscribe", body, re.I) or True:
            # Always try add Subscribe (Studio allows both)
            try:
                page.get_by_role("button", name=re.compile(r"ADD ELEMENT|Add element", re.I)).first.click(
                    timeout=1200
                )
                page.wait_for_timeout(600)
            except Exception:
                pass
            try:
                page.get_by_role("button", name=re.compile(r"^Subscribe$", re.I)).first.click(
                    timeout=1500
                )
                out["actions"].append("Subscribe")
            except Exception:
                page.evaluate(
                    """() => {
                      const walk=(r,d=0)=>{
                        if(!r||d>55) return;
                        for (const el of (r.querySelectorAll
                          ? r.querySelectorAll('button,[role=button]') : [])) {
                          if ((el.innerText||'').trim()==='Subscribe') { el.click(); return; }
                        }
                        for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                          if(el.shadowRoot) walk(el.shadowRoot,d+1);
                      };
                      walk(document);
                    }"""
                )
                out["actions"].append("Subscribe_deep")
            page.wait_for_timeout(800)

        cos.shot(page, "COS2102ES_05_before_save.png")
        out["saved"] = cos.save_named(page)
        page.wait_for_timeout(3000)
        body = page.inner_text("body")
        out["processing_error"] = bool(
            re.search(r"problem in processing|couldn.?t be saved|NaN", body, re.I)
        )
        out["oops"] = bool(re.search(r"Oops, something went wrong", body, re.I))
        # Proof: look for element list mentioning Periodic / Subscribe on endscreen UI
        out["proof_snip"] = body[:1500]
        out["has_periodic_in_ui"] = bool(
            re.search(r"How Did We Discover the Periodic|AL_-qlWko_g", body)
        )
        out["has_subscribe_word"] = bool(re.search(r"Subscribe", body))
        cos.shot(page, "COS2102ES_06_after_save.png")

        # Close back to details; audience check
        for _ in range(2):
            page.keyboard.press("Escape")
            page.wait_for_timeout(200)
        cos.open_edit(page)
        out["audience_final"] = cos.ensure_not_kids(page, context="es2_final")
        cos.show_more(page)
        for _ in range(20):
            if re.search(r"AI wasn|AI was used", page.inner_text("body"), re.I):
                break
            page.keyboard.press("PageDown")
            page.wait_for_timeout(80)
        out["altered_final"] = cos.read_ai_altered(page)
        out["ok"] = bool(out.get("saved")) and not out.get("processing_error") and not out.get("oops")
        cos.dump("COS_CHECKIN_2102_ENDSCREEN_V02.json", out)
        log(f"ok={out['ok']} picked={out.get('picked') or out.get('picked_title')} saved={out.get('saved')} err={out.get('processing_error')}")
        return out


if __name__ == "__main__":
    main()
