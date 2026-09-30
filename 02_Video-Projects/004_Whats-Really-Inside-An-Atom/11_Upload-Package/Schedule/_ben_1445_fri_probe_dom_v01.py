#!/usr/bin/env python3
"""Interactive DOM probe for Fri Studio dropdowns — dump structure."""
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


PROBE_JS = """(label) => {
  // find and click trigger
  let lab=null;
  const walk=(r,d=0)=>{
    if(!r||d>50||lab) return;
    for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
      const own=[...el.childNodes].filter(n=>n.nodeType===3).map(n=>n.textContent.trim()).join(' ').trim();
      const t=(el.innerText||'').trim();
      if (own===label || t===label) {
        const b=el.getBoundingClientRect();
        if (b.width>10&&b.height>8&&b.y>40&&b.y<1100) lab={el,x:b.x,y:b.y};
      }
    }
    for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
      if (el.shadowRoot) walk(el.shadowRoot,d+1);
  }; walk(document);
  if(!lab) return {error:'no_lab'};
  lab.el.scrollIntoView({block:'center'});
  let best=null, bestEl=null;
  const walk2=(r,d=0)=>{
    if(!r||d>50) return;
    for (const el of (r.querySelectorAll
      ? r.querySelectorAll('ytcp-dropdown-trigger,ytcp-text-dropdown-trigger,[role=combobox]')
      : [])) {
      const b=el.getBoundingClientRect();
      const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
      if (b.width<40||b.height<18) continue;
      if (Math.abs(b.y-lab.y)>140) continue;
      if (b.x < lab.x-20) continue;
      const score=Math.abs(b.y-lab.y)*4;
      if (!best||score<best.score) { best={t:t.slice(0,90),y:b.y,x:b.x,w:b.width,h:b.height,score}; bestEl=el; }
    }
    for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
      if (el.shadowRoot) walk2(el.shadowRoot,d+1);
  }; walk2(document);
  if (bestEl) bestEl.click();
  return {trig:best};
}"""


DUMP_JS = """() => {
  const report={visible_inputs:[], panels:[], optionish:[], text_hits:[]};
  const walk=(r,d=0,path='')=>{
    if(!r||d>60) return;
    for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
      const tag=el.tagName;
      const role=el.getAttribute('role')||'';
      const b=el.getBoundingClientRect();
      const style=r===document?null:null;
      const vis=b.width>0&&b.height>0&&b.y>-50&&b.y<1400;
      if (!vis) continue;
      if (tag==='INPUT' && el.type!=='hidden' && el.type!=='file') {
        report.visible_inputs.push({
          type:el.type, aria:(el.getAttribute('aria-label')||'').slice(0,80),
          ph:(el.getAttribute('placeholder')||'').slice(0,60),
          x:b.x,y:b.y,w:b.width,h:b.height, value:(el.value||'').slice(0,40)
        });
      }
      if (/listbox|menu|dropdown|DIALOG/i.test(tag+' '+role) || tag.includes('DROPDOWN') || tag.includes('LISTBOX') || tag.includes('MENU')) {
        if (b.height>30&&b.width>50)
          report.panels.push({tag,role,x:b.x,y:b.y,w:b.width,h:b.height,
            text:(el.innerText||'').replace(/\\s+/g,' ').trim().slice(0,200),
            childCount:el.children?el.children.length:0});
      }
      if (role==='option' || /PAPER-ITEM|MENU-ITEM/i.test(tag)) {
        report.optionish.push({tag,role,t:(el.innerText||'').replace(/\\s+/g,' ').trim().slice(0,80),
          x:b.x,y:b.y,w:b.width,h:b.height});
      }
      const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
      if (t && t.length<60 && /(United Kingdom|English \\(United|Ukrainian|United Arab|GCSE Chemistry|Concept overview|Secondary)/i.test(t)) {
        // leaf-ish
        const own=[...el.childNodes].filter(n=>n.nodeType===3).map(n=>n.textContent.trim()).join('');
        if (own || role==='option' || /ITEM|STRING/i.test(tag))
          report.text_hits.push({tag,role,t,own:own.slice(0,60),x:b.x,y:b.y,w:b.width,h:b.height});
      }
    }
    for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
      if (el.shadowRoot) walk(el.shadowRoot,d+1,path+'/'+el.tagName);
  }; walk(document);
  // dedupe text_hits
  const seen=new Set(); const uniq=[];
  for (const h of report.text_hits) {
    const k=h.t+'@'+Math.round(h.y);
    if (seen.has(k)) continue; seen.add(k); uniq.push(h);
  }
  report.text_hits=uniq.slice(0,60);
  report.optionish=report.optionish.slice(0,80);
  report.panels=report.panels.slice(0,20);
  return report;
}"""


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


def scroll_find(page, pat):
    for _ in range(28):
        if page.evaluate(
            """(pat)=>{
              const re=new RegExp(pat,'i');
              const walk=(r,d=0)=>{
                if(!r||d>50) return false;
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                  const t=(el.innerText||'').trim();
                  if (re.test(t) && t.length<80) { el.scrollIntoView({block:'center'}); return true; }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                  if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
                return false;
              }; return walk(document);
            }""",
            pat,
        ):
            page.wait_for_timeout(300)
            return True
        page.mouse.wheel(0, 700)
        page.wait_for_timeout(80)
    return False


def probe_one(page, label, type_text=None):
    scroll_find(page, label.replace("(", "\\(").replace(")", "\\)"))
    page.wait_for_timeout(400)
    trig = page.evaluate(PROBE_JS, label)
    page.wait_for_timeout(1200)
    before = page.evaluate(DUMP_JS)
    typed = None
    if type_text:
        # click first visible input that looks like search in dropdown
        inputs = before.get("visible_inputs") or []
        # prefer newest / lower on page or with search aria
        cand = None
        for inp in inputs:
            aria = (inp.get("aria") or "") + (inp.get("ph") or "")
            if "tag" in aria.lower():
                continue
            if inp["y"] > 50 and inp["w"] > 80:
                cand = inp
                # keep looking for better
                if "search" in aria.lower() or "filter" in aria.lower() or not inp.get("value"):
                    cand = inp
                    break
        if cand:
            page.mouse.click(cand["x"] + cand["w"] / 2, cand["y"] + cand["h"] / 2)
            page.wait_for_timeout(200)
            page.keyboard.press("Meta+a")
            page.keyboard.type(type_text, delay=40)
            page.wait_for_timeout(1500)
            typed = cand
        else:
            page.keyboard.type(type_text, delay=40)
            page.wait_for_timeout(1500)
            typed = "keyboard_only"
    after = page.evaluate(DUMP_JS)
    page.keyboard.press("Escape")
    page.wait_for_timeout(400)
    return {"trig": trig, "typed_into": typed, "before_type": before, "after_type": after}


def probe_paid(page):
    scroll_find(page, "Paid promotion")
    page.wait_for_timeout(400)
    return page.evaluate(
        """() => {
          const out={radios:[], labels:[]};
          const walk=(r,d=0)=>{
            if(!r||d>50) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const lab=(el.getAttribute('aria-label')||'');
              const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
              const b=el.getBoundingClientRect();
              if (/paid promotion/i.test(lab) && b.width>5) {
                out.radios.push({tag:el.tagName, role:el.getAttribute('role'), lab:lab.slice(0,100),
                  checked:el.getAttribute('aria-checked'),
                  ariaDisabled:el.getAttribute('aria-disabled'),
                  x:b.x,y:b.y,w:b.width,h:b.height});
              }
              if (/paid promotion/i.test(t) && t.length<80 && b.width>5)
                out.labels.push({tag:el.tagName, t:t.slice(0,100), x:b.x,y:b.y,w:b.width,h:b.height});
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document); return out;
        }"""
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
            out["paid"] = probe_paid(page)
            page.screenshot(path=str(EV / "fri_probe_paid.png"))

            out["lang"] = probe_one(
                page, "Title and description language", "English (United Kingdom)"
            )
            page.screenshot(path=str(EV / "fri_probe_lang_open.png"))

            out["academic"] = probe_one(page, "Academic system", "United Kingdom")
            page.screenshot(path=str(EV / "fri_probe_academic_open.png"))

            out["type"] = probe_one(page, "Type", None)
            page.screenshot(path=str(EV / "fri_probe_type_open.png"))

            out["exam"] = probe_one(page, "Exam, course or standard", "GCSE Chemistry")
            page.screenshot(path=str(EV / "fri_probe_exam_open.png"))

            path = EV / "DROPDOWN_PROBE.json"
            path.write_text(json.dumps(out, indent=2, default=str))
            print("wrote", path)
            # quick summary
            for k in ["lang", "academic", "type", "exam"]:
                a = out[k].get("after_type") or out[k].get("before_type") or {}
                print(
                    k,
                    "panels",
                    len(a.get("panels") or []),
                    "optionish",
                    len(a.get("optionish") or []),
                    "text_hits",
                    [h["t"] for h in (a.get("text_hits") or [])[:12]],
                    "inputs",
                    len(a.get("visible_inputs") or []),
                )
            print("paid radios", out["paid"].get("radios"))
        finally:
            page.close()


if __name__ == "__main__":
    main()
