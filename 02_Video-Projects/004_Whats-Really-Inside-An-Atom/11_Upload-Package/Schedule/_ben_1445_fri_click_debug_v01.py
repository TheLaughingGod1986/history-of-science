#!/usr/bin/env python3
"""Focused click-debug for Academic / Language / Type on Fri video."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO = Path("/Users/benjaminoats/YouTube/History Of Science")
U004 = (
    REPO
    / "02_Video-Projects/004_Whats-Really-Inside-An-Atom/11_Upload-Package/Schedule"
    / "_upload_hos_004_shorts_v01.py"
)
EV = (
    REPO
    / "02_Video-Projects/004_Whats-Really-Inside-An-Atom/11_Upload-Package/Schedule"
    / "evidence_2026-09-30_studio_fixes"
)
VID = "29bpGAI0wb8"


def load_u():
    spec = importlib.util.spec_from_file_location("u", U004)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def show_more(page):
    for _ in range(8):
        ok = page.evaluate(
            """() => {
              const walk=(r,d=0)=>{
                if(!r||d>50) return false;
                for (const el of (r.querySelectorAll?r.querySelectorAll('button,ytcp-button,[role=button]'):[])) {
                  if ((el.innerText||'').trim()==='Show more') { el.click(); return true; }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                  if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
                return false;
              }; return walk(document);
            }"""
        )
        if not ok:
            break
        page.wait_for_timeout(400)


def scroll_text(page, text):
    page.evaluate(
        """(text)=>{
          const walk=(r,d=0)=>{
            if(!r||d>50) return false;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim();
              if (t===text || t.startsWith(text)) { el.scrollIntoView({block:'center'}); return true; }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
            return false;
          }; return walk(document);
        }""",
        text,
    )
    page.wait_for_timeout(500)


def deep_dump(page):
    return page.evaluate(
        """()=>{
          const items=[];
          const triggers=[];
          const inputs=[];
          const walk=(r,d=0)=>{
            if(!r||d>55) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const tag=el.tagName;
              const role=el.getAttribute('role')||'';
              const b=el.getBoundingClientRect();
              if (!(b.width>0&&b.height>0&&b.y>-30&&b.y<1100)) continue;
              const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
              if (/DROPDOWN|FORM-SELECT|COMBOBOX|LANGUAGE|TEXT-DROPDOWN/i.test(tag) || role==='combobox' || role==='listbox') {
                triggers.push({tag,role,t:t.slice(0,120),x:b.x,y:b.y,w:b.width,h:b.height,
                  ariaExpanded:el.getAttribute('aria-expanded'),
                  open:el.hasAttribute('opened')||el.getAttribute('aria-expanded')==='true'});
              }
              if (role==='option' || /PAPER-ITEM/i.test(tag)) {
                items.push({tag,role,t:t.slice(0,100),y:b.y,x:b.x,h:b.height});
              }
              if (tag==='INPUT' && el.type!=='hidden' && el.type!=='file') {
                inputs.push({aria:(el.getAttribute('aria-label')||'').slice(0,80),
                  ph:(el.getAttribute('placeholder')||'').slice(0,60),
                  y:b.y,x:b.x,w:b.width,value:(el.value||'').slice(0,40)});
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document);
          return {triggers:triggers.slice(0,40), items:items.slice(0,60), inputs};
        }"""
    )


def click_value_near_label(page, label, value_substr):
    """Find label, then click element below it containing value_substr."""
    return page.evaluate(
        """(args)=>{
          const label=args[0], want=args[1];
          let lab=null;
          const walk=(r,d=0)=>{
            if(!r||d>50||lab) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const own=[...el.childNodes].filter(n=>n.nodeType===3).map(n=>n.textContent.trim()).join(' ').trim();
              if (own===label || (el.innerText||'').trim()===label) {
                const b=el.getBoundingClientRect();
                if (b.width>8&&b.height>8&&b.y>40&&b.y<1100) lab={x:b.x,y:b.y,w:b.width,h:b.height,el};
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document);
          if(!lab) return {error:'no_lab'};
          lab.el.scrollIntoView({block:'center'});
          // find value text near label
          let best=null, bestEl=null;
          const walk2=(r,d=0)=>{
            if(!r||d>50) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
              if (!t.includes(want)) continue;
              if (t.length>120) continue;
              const b=el.getBoundingClientRect();
              if (b.width<20||b.height<10) continue;
              if (b.y < lab.y-10 || b.y > lab.y+120) continue;
              if (b.x < lab.x-30) continue;
              const score=Math.abs(b.y-(lab.y+24))*2 + Math.abs(b.x-lab.x)*0.05 + t.length*0.01;
              if (!best||score<best.score) { best={t:t.slice(0,80),y:b.y,x:b.x,w:b.width,h:b.height,score}; bestEl=el; }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk2(el.shadowRoot,d+1);
          }; walk2(document);
          if (!bestEl) {
            // fallback: click dropdown trigger near label
            const walk3=(r,d=0)=>{
              if(!r||d>50) return;
              for (const el of (r.querySelectorAll?r.querySelectorAll('ytcp-dropdown-trigger,ytcp-text-dropdown-trigger,[role=combobox]'):[])) {
                const b=el.getBoundingClientRect();
                if (Math.abs(b.y-lab.y)>140) continue;
                if (b.x<lab.x-40) continue;
                bestEl=el; best={t:(el.innerText||'').slice(0,80),y:b.y,x:b.x,w:b.width,h:b.height,via:'trig'};
              }
              for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                if (el.shadowRoot) walk3(el.shadowRoot,d+1);
            }; walk3(document);
          }
          if (!bestEl) return {error:'no_value', lab:{x:lab.x,y:lab.y}};
          bestEl.scrollIntoView({block:'center'});
          const b=bestEl.getBoundingClientRect();
          // click center then chevron
          bestEl.click();
          return {clicked:best, box:{x:b.x,y:b.y,w:b.width,h:b.height}};
        }""",
        [label, value_substr],
    )


def main():
    u = load_u()
    out = {}
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9460")
        page = browser.contexts[0].new_page()
        page.set_viewport_size({"width": 1400, "height": 900})
        try:
            page.goto(
                f"https://studio.youtube.com/video/{VID}/edit",
                wait_until="domcontentloaded",
                timeout=120000,
            )
            page.wait_for_timeout(3500)
            u.dismiss(page)
            show_more(page)

            # --- Academic ---
            scroll_text(page, "Academic system")
            page.wait_for_timeout(600)
            page.screenshot(path=str(EV / "dbg_academic_before.png"))
            out["academic_before"] = deep_dump(page)
            click = click_value_near_label(page, "Academic system", "United Arab Emirates")
            out["academic_click"] = click
            page.wait_for_timeout(1500)
            page.screenshot(path=str(EV / "dbg_academic_after_click.png"))
            out["academic_after"] = deep_dump(page)
            # try typing United Kingdom into focused element
            page.keyboard.type("United Kingdom", delay=50)
            page.wait_for_timeout(1500)
            page.screenshot(path=str(EV / "dbg_academic_after_type.png"))
            out["academic_after_type"] = deep_dump(page)
            page.keyboard.press("Escape")
            page.wait_for_timeout(400)

            # --- Language ---
            for _ in range(10):
                page.mouse.wheel(0, -600)
                page.wait_for_timeout(80)
            scroll_text(page, "Title and description language")
            page.wait_for_timeout(600)
            page.screenshot(path=str(EV / "dbg_lang_before.png"))
            click = click_value_near_label(page, "Title and description language", "Ukrainian")
            out["lang_click"] = click
            page.wait_for_timeout(1500)
            page.screenshot(path=str(EV / "dbg_lang_after_click.png"))
            out["lang_after"] = deep_dump(page)
            page.keyboard.type("English (United Kingdom)", delay=45)
            page.wait_for_timeout(1500)
            page.screenshot(path=str(EV / "dbg_lang_after_type.png"))
            out["lang_after_type"] = deep_dump(page)
            page.keyboard.press("Escape")
            page.wait_for_timeout(400)

            # --- Type ---
            scroll_text(page, "Education")
            scroll_text(page, "Type")
            page.wait_for_timeout(600)
            page.screenshot(path=str(EV / "dbg_type_before.png"))
            click = click_value_near_label(page, "Type", "None")
            out["type_click"] = click
            page.wait_for_timeout(1500)
            page.screenshot(path=str(EV / "dbg_type_after_click.png"))
            out["type_after"] = deep_dump(page)
            page.keyboard.press("Escape")

            # --- Level (known working pattern) ---
            scroll_text(page, "Level")
            click = click_value_near_label(page, "Level", "None")
            out["level_click"] = click
            page.wait_for_timeout(1500)
            page.screenshot(path=str(EV / "dbg_level_after_click.png"))
            out["level_after"] = deep_dump(page)
            page.keyboard.press("Escape")

            path = EV / "DROPDOWN_PROBE.json"
            # compact: only item texts
            summary = {}
            for k in ["academic_after", "academic_after_type", "lang_after", "lang_after_type", "type_after", "level_after"]:
                d = out.get(k) or {}
                summary[k] = {
                    "n_items": len(d.get("items") or []),
                    "items": [i["t"] for i in (d.get("items") or [])[:40]],
                    "inputs": d.get("inputs"),
                    "open_triggers": [t for t in (d.get("triggers") or []) if t.get("open") or t.get("ariaExpanded") == "true"][:10],
                    "trigger_sample": (d.get("triggers") or [])[:8],
                }
            summary["clicks"] = {k: out.get(k) for k in ["academic_click", "lang_click", "type_click", "level_click"]}
            path.write_text(json.dumps(summary, indent=2))
            print(json.dumps({k: {"n": v["n_items"], "items": v["items"][:15], "inputs": v["inputs"]} for k, v in summary.items() if isinstance(v, dict) and "n_items" in v}, indent=2))
            print("clicks", json.dumps(summary["clicks"], indent=2))
        finally:
            page.close()


if __name__ == "__main__":
    main()
