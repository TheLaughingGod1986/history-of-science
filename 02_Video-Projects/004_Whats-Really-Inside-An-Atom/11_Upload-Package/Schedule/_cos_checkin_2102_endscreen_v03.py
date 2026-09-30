#!/usr/bin/env python3
"""CoS 21:02 end screen v03 — finish6 path: template 1 video+subscribe → Specific 002."""
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
TITLE_002 = "How Did We Discover the Periodic Table?"
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
    cos.log("ES3 " + m)


def find_click(page, pattern: str, y_min: int = 0, max_len: int = 100):
    hit = page.evaluate(
        """({pattern,yMin,maxLen})=>{
          const re=new RegExp(pattern,'i');
          let best=null;
          const walk=(r,d=0)=>{
            if(!r||d>55) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim().replace(/\\s+/g,' ');
              if(!t||t.length>maxLen||!re.test(t)) continue;
              const rect=el.getBoundingClientRect();
              if(rect.width<4||rect.height<4||rect.y<yMin) continue;
              // Prefer shorter exact-ish matches
              const score=t.length + Math.abs(rect.y);
              if(!best||score<best.score) best={x:rect.x+rect.width/2,y:rect.y+rect.height/2,t:t.slice(0,90),score};
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if(el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document);
          if(!best) return null;
          document.elementFromPoint(best.x,best.y)?.click();
          return best;
        }""",
        {"pattern": pattern, "yMin": y_min, "maxLen": max_len},
    )
    if hit:
        page.wait_for_timeout(500)
    return hit


def main():
    ART.mkdir(parents=True, exist_ok=True)
    out = {"at": datetime.now().isoformat(timespec="seconds"), "steps": []}
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
        page = browser.contexts[0].pages[0]
        cos.channel_ok(page)
        cos.open_edit(page)
        out["audience_0"] = cos.ensure_not_kids(page, context="es3_start")

        # Close any leftover dialogs
        for _ in range(3):
            page.keyboard.press("Escape")
            page.wait_for_timeout(150)

        # Open End screen from Details
        hit = find_click(page, r"^End screen$", y_min=200, max_len=20)
        out["steps"].append({"open": hit})
        page.wait_for_timeout(3000)
        for _ in range(2):
            cos.dismiss(page)
            find_click(page, r"^OK, got it$", y_min=0, max_len=20)
            page.wait_for_timeout(200)
        cos.shot(page, "COS2102ES3_01_open.png")
        body = page.inner_text("body")
        if re.search(r"Oops, something went wrong", body, re.I):
            out["oops"] = True
            cos.dump("COS_CHECKIN_2102_ENDSCREEN_V03.json", out)
            raise SystemExit("End screen Oops")

        # Template: 1 video, 1 subscribe
        t = find_click(page, r"1 video,\s*1 subscribe", y_min=80, max_len=40)
        out["steps"].append({"template": t})
        page.wait_for_timeout(2000)
        cos.shot(page, "COS2102ES3_02_template.png")

        # Switch video source to Specific
        find_click(page, r"Most recent upload|Best for viewer", y_min=80, max_len=40)
        page.wait_for_timeout(600)
        s = find_click(page, r"^Specific video$", y_min=80, max_len=30)
        out["steps"].append({"specific": s})
        page.wait_for_timeout(1000)
        cos.shot(page, "COS2102ES3_03_specific.png")

        # Fill dialog search — skip top channel search (y<50)
        filled = page.evaluate(
            """(q) => {
              let hit=null;
              const walk=(r,d=0)=>{
                if(!r||d>55||hit) return;
                for (const inp of (r.querySelectorAll
                  ? r.querySelectorAll('input,textarea') : [])) {
                  const aria=((inp.getAttribute('aria-label')||'')+(inp.placeholder||'')).toLowerCase();
                  const rect=inp.getBoundingClientRect();
                  if (rect.width<40||rect.y<50) continue; // skip top chrome search
                  if (/search|video|url|paste/.test(aria) || inp.type==='search' || inp.type==='text') {
                    inp.focus();
                    const proto = inp.tagName==='TEXTAREA'
                      ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype;
                    Object.getOwnPropertyDescriptor(proto,'value').set.call(inp, q);
                    inp.dispatchEvent(new Event('input',{bubbles:true}));
                    hit={aria:aria.slice(0,60), y:Math.round(rect.y)};
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
        out["steps"].append({"filled": filled})
        page.wait_for_timeout(300)
        if filled:
            page.keyboard.press("Enter")
        else:
            # focused keyboard fallback
            page.keyboard.type(VID_002, delay=25)
            page.keyboard.press("Enter")
        page.wait_for_timeout(2000)
        cos.shot(page, "COS2102ES3_04_search.png")

        # Pick 002 by exact title — avoid A/B titles on Details behind modal
        picked = page.evaluate(
            """(title) => {
              let hit=null;
              const walk=(r,d=0)=>{
                if(!r||d>55||hit) return;
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                  const t=(el.innerText||'').trim().replace(/\\s+/g,' ');
                  if (t!==title && !t.startsWith(title)) continue;
                  // Must be reasonably short (row title, not whole page)
                  if (t.length>title.length+40) continue;
                  const rect=el.getBoundingClientRect();
                  if (rect.width<40||rect.height<12||rect.y<100) continue;
                  el.click(); hit={t:t.slice(0,100), y:Math.round(rect.y)}; return;
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                  if(el.shadowRoot) walk(el.shadowRoot,d+1);
              };
              walk(document); return hit;
            }""",
            TITLE_002,
        )
        out["steps"].append({"picked": picked})
        if not picked:
            # try id visible in results
            picked = find_click(page, re.escape(VID_002), y_min=100, max_len=40)
            out["steps"].append({"picked_id": picked})
        page.wait_for_timeout(1200)
        cos.shot(page, "COS2102ES3_05_picked.png")

        # Subscribe should come from template; ensure present
        body = page.inner_text("body")
        if not re.search(r"Subscribe", body, re.I):
            find_click(page, r"^\+?\s*Element$|^Element$", y_min=80, max_len=20)
            page.wait_for_timeout(400)
            find_click(page, r"^Subscribe$", y_min=80, max_len=15)
            out["steps"].append("added_subscribe")

        cos.shot(page, "COS2102ES3_06_before_save.png")
        saved = False
        try:
            btn = page.get_by_role("button", name=re.compile(r"^Save$", re.I))
            if btn.count() and btn.first.is_enabled():
                btn.first.click(timeout=4000)
                saved = True
                out["steps"].append("save_enabled_click")
            else:
                out["steps"].append("save_disabled")
                # try Discard? no — click template video again
        except Exception as e:
            out["save_err"] = type(e).__name__
        if not saved:
            sbox = find_click(page, r"^Save$", y_min=0, max_len=10)
            out["steps"].append({"save_find": sbox})
            saved = bool(sbox)
        page.wait_for_timeout(3000)
        cos.shot(page, "COS2102ES3_07_after_save.png")
        after = page.inner_text("body")
        out["after_snip"] = after[:1200]
        out["processing_error"] = bool(
            re.search(r"problem in processing|couldn.?t be saved|NaN", after, re.I)
        )
        out["has_002_title"] = TITLE_002 in after or "Periodic Table" in after
        out["has_subscribe"] = bool(re.search(r"Subscribe", after, re.I))
        out["best_for_viewer"] = bool(re.search(r"Best for viewer", after, re.I))
        out["most_recent"] = bool(re.search(r"Most recent", after, re.I))
        out["specific_set"] = bool(picked) or bool(out.get("steps") and any(
            isinstance(s, dict) and s.get("picked_id") for s in out["steps"]
        ))
        out["saved"] = saved
        out["ok"] = (
            saved
            and not out["processing_error"]
            and out["has_subscribe"]
            and (out["has_002_title"] or out["best_for_viewer"] or out["most_recent"] or out["specific_set"])
        )

        # Close modal, verify audience + altered
        for _ in range(2):
            page.keyboard.press("Escape")
            page.wait_for_timeout(200)
        cos.open_edit(page)
        out["audience_final"] = cos.ensure_not_kids(page, context="es3_final")
        cos.show_more(page)
        for _ in range(20):
            if re.search(r"AI wasn|AI was used", page.inner_text("body"), re.I):
                break
            page.keyboard.press("PageDown")
            page.wait_for_timeout(80)
        out["altered_final"] = cos.read_ai_altered(page)
        cos.shot(page, "COS2102ES3_08_details.png")
        cos.dump("COS_CHECKIN_2102_ENDSCREEN_V03.json", out)
        log(f"ok={out['ok']} saved={saved} picked={picked} err={out['processing_error']}")
        return out


if __name__ == "__main__":
    main()
