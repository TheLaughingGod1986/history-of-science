#!/usr/bin/env python3
"""Dump FULL Academic / Language option lists via scrollTop; try UK aliases."""
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


def open_value(page, label, value):
    return page.evaluate(
        """(args)=>{
          const label=args[0], want=args[1];
          let lab=null;
          const walk=(r,d=0)=>{
            if(!r||d>50||lab) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const own=[...el.childNodes].filter(n=>n.nodeType===3).map(n=>n.textContent.trim()).join(' ').trim();
              if (own!==label && (el.innerText||'').trim()!==label) continue;
              const b=el.getBoundingClientRect();
              if (b.width>8&&b.height>8&&b.y>40&&b.y<1050) lab={el,x:b.x,y:b.y};
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document);
          if(!lab) return {error:'no_lab'};
          lab.el.scrollIntoView({block:'center'});
          let bestEl=null, best=null;
          const walk2=(r,d=0)=>{
            if(!r||d>50) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('span,yt-formatted-string,div'):[])) {
              const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
              if (t!==want && !t.includes(want)) continue;
              if (t.length>90) continue;
              const b=el.getBoundingClientRect();
              if (b.width<15||b.height<10||b.height>50) continue;
              if (b.y<lab.y-5||b.y>lab.y+130) continue;
              if (b.x<lab.x-40) continue;
              const score=Math.abs(b.y-(lab.y+22));
              if (!best||score<best.score) { best={t,y:b.y,score}; bestEl=el; }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk2(el.shadowRoot,d+1);
          }; walk2(document);
          if(!bestEl) return {error:'no_value'};
          bestEl.click();
          return {ok:true, clicked:best};
        }""",
        [label, value],
    )


def harvest_all(page, max_steps=80):
    """Scroll listbox via scrollTop and collect every unique option text with y."""
    return page.evaluate(
        """(maxSteps)=>{
          // find scrollable listbox
          let box=null;
          const find=(r,d=0)=>{
            if(!r||d>55||box) return;
            for (const el of (r.querySelectorAll
              ? r.querySelectorAll('[role=listbox],tp-yt-paper-listbox')
              : [])) {
              const b=el.getBoundingClientRect();
              if (b.height>60&&b.width>80) box=el;
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) find(el.shadowRoot,d+1);
          }; find(document);
          // fallback: scrollable parent of a paper-item
          if (!box) {
            const find2=(r,d=0)=>{
              if(!r||d>55||box) return;
              for (const el of (r.querySelectorAll?r.querySelectorAll('tp-yt-paper-item,[role=option]'):[])) {
                const b=el.getBoundingClientRect();
                if (b.width<40||b.height<10) continue;
                let p=el.parentElement;
                for (let i=0;i<8&&p;i++) {
                  if (p.scrollHeight > p.clientHeight+40) { box=p; break; }
                  p=p.parentElement;
                }
              }
              for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                if (el.shadowRoot) find2(el.shadowRoot,d+1);
            }; find2(document);
          }
          if (!box) return {error:'no_listbox', options:[]};

          const read=()=>{
            const out=[]; const seen=new Set();
            const walk=(r,d=0)=>{
              if(!r||d>40) return;
              for (const el of (r.querySelectorAll?r.querySelectorAll('tp-yt-paper-item,[role=option]'):[])) {
                const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
                if (!t||t.length>120) continue;
                const b=el.getBoundingClientRect();
                if (b.width<30||b.height<10) continue;
                const k=t;
                if (seen.has(k)) continue; // unique by text across scroll
                // only add if reasonably in/near box
                out.push({t,y:b.y}); seen.add(k);
              }
              for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                if (el.shadowRoot) walk(el.shadowRoot,d+1);
            }; walk(document);
            // actually we want ALL unique ever seen — handled outside
            return out;
          };

          const all=[]; const seen=new Set();
          const note=()=>{
            for (const o of read()) {
              if (seen.has(o.t)) continue;
              seen.add(o.t); all.push(o.t);
            }
          };
          // start at top
          box.scrollTop = 0;
          note();
          for (let i=0;i<maxSteps;i++) {
            const before=box.scrollTop;
            box.scrollTop = before + Math.max(120, Math.floor(box.clientHeight*0.7));
            if (box.scrollTop===before) break;
            note();
          }
          // also try scroll to bottom
          box.scrollTop = box.scrollHeight;
          note();
          return {
            tag: box.tagName,
            scrollHeight: box.scrollHeight,
            clientHeight: box.clientHeight,
            n: all.length,
            options: all.map((t,i)=>({t,i}))
          };
        }""",
        max_steps,
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

            # Academic full dump
            page.evaluate(
                """()=>{
                  const walk=(r,d=0)=>{
                    if(!r||d>50) return false;
                    for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                      if ((el.innerText||'').trim()==='Academic system') {
                        el.scrollIntoView({block:'center'}); return true;
                      }
                    }
                    for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                      if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
                    return false;
                  }; return walk(document);
                }"""
            )
            page.wait_for_timeout(500)
            out["academic_open"] = open_value(page, "Academic system", "United Arab Emirates")
            page.wait_for_timeout(1200)
            out["academic_all"] = harvest_all(page)
            page.screenshot(path=str(EV / "dbg_academic_full.png"))
            # search for UK-like
            opts = [o["t"] for o in (out["academic_all"].get("options") or [])]
            out["academic_uk_like"] = [
                t
                for t in opts
                if any(
                    x in t.lower()
                    for x in [
                        "kingdom",
                        "britain",
                        "england",
                        "scotland",
                        "wales",
                        "uk",
                        "united k",
                    ]
                )
            ]
            page.keyboard.press("Escape")
            page.wait_for_timeout(400)

            # Language full dump
            page.evaluate(
                """()=>{
                  const walk=(r,d=0)=>{
                    if(!r||d>50) return false;
                    for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                      if ((el.innerText||'').trim()==='Title and description language') {
                        el.scrollIntoView({block:'center'}); return true;
                      }
                    }
                    for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                      if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
                    return false;
                  }; return walk(document);
                }"""
            )
            page.wait_for_timeout(500)
            # read current value from trigger
            cur = page.evaluate(
                """()=>{
                  const walk=(r,d=0)=>{
                    if(!r||d>50) return null;
                    for (const el of (r.querySelectorAll?r.querySelectorAll('ytcp-dropdown-trigger,ytcp-text-dropdown-trigger,[role=combobox]'):[])) {
                      const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
                      if (/Title and description language/i.test(t)) return t;
                    }
                    for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                      if (el.shadowRoot) { const h=walk(el.shadowRoot,d+1); if(h) return h; }
                    return null;
                  }; return walk(document);
                }"""
            )
            out["lang_trigger"] = cur
            val = "Ukrainian"
            if cur and "language" in cur.lower():
                val = cur.split("language")[-1].strip() or val
            out["lang_open"] = open_value(page, "Title and description language", val)
            page.wait_for_timeout(1200)
            # if failed, try clicking trigger itself
            if (out["lang_open"] or {}).get("error"):
                page.evaluate(
                    """()=>{
                      const walk=(r,d=0)=>{
                        if(!r||d>50) return false;
                        for (const el of (r.querySelectorAll?r.querySelectorAll('ytcp-dropdown-trigger,ytcp-text-dropdown-trigger,[role=combobox]'):[])) {
                          const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
                          if (/Title and description language/i.test(t)) { el.click(); return true; }
                        }
                        for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                          if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
                        return false;
                      }; return walk(document);
                    }"""
                )
                page.wait_for_timeout(1200)
            out["lang_all"] = harvest_all(page)
            page.screenshot(path=str(EV / "dbg_lang_full.png"))
            lopts = [o["t"] for o in (out["lang_all"].get("options") or [])]
            out["lang_en_like"] = [
                t
                for t in lopts
                if "english" in t.lower() or "united kingdom" in t.lower()
            ]
            page.keyboard.press("Escape")

            path = EV / "DROPDOWN_PROBE.json"
            path.write_text(json.dumps(out, indent=2))
            print("academic n", out["academic_all"].get("n"), "uk_like", out["academic_uk_like"])
            print("lang n", out["lang_all"].get("n"), "en_like", out["lang_en_like"][:20])
            print("lang_open", out["lang_open"], "trigger", out["lang_trigger"])
            # print countries containing United
            print(
                "academic United*",
                [t for t in opts if t.startswith("United") or "Kingdom" in t],
            )
        finally:
            page.close()


if __name__ == "__main__":
    main()
