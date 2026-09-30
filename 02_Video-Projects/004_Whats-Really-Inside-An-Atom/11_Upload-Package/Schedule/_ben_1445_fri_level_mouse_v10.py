#!/usr/bin/env python3
"""Fri Level Key stage 4 via mouse coordinate click so Save enables; report GCSE missing."""
from __future__ import annotations

import importlib.util
import json
import shutil
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

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
ART = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts"
LONDON = ZoneInfo("Europe/London")
VID = "29bpGAI0wb8"
FRI_TAGS = [
    "how small can you cut gold",
    "what's really inside an atom",
    "atom",
    "gold",
    "periodic table",
    "history of science",
]


def load_u():
    spec = importlib.util.spec_from_file_location("u", U004)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def shot(page, name):
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    p = EV / name
    page.screenshot(path=str(p), full_page=False)
    shutil.copy2(p, ART / f"BEN_1445FIX_{name}")
    return str(p)


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


def selects(page):
    return page.evaluate(
        """()=>{
          const out=[];
          const walk=(r,d=0)=>{
            if(!r||d>50) return;
            for (const el of (r.querySelectorAll
              ? r.querySelectorAll('ytcp-dropdown-trigger,ytcp-text-dropdown-trigger,[role=combobox]')
              : [])) {
              const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
              if (/language|Type|Level|Exam|Academic|Education/i.test(t) && t.length<160)
                out.push(t.slice(0,160));
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document); return [...new Set(out)];
        }"""
    )


def chips(page):
    return page.evaluate(
        """()=>{
          const out=[];
          const walk=(r,d=0)=>{
            if(!r||d>50) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('ytcp-chip,yt-chip-cloud-chip'):[])) {
              const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
              if (t && t.length<90) out.push(t);
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document); return [...new Set(out)];
        }"""
    )


def paid_places(page):
    return page.evaluate(
        """()=>{
          const paid=[]; const state={places:null};
          const walk=(r,d=0)=>{
            if(!r||d>50) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('tp-yt-paper-radio-button,[role=radio]'):[])) {
              const lab=(el.getAttribute('aria-label')||el.innerText||'').replace(/\\s+/g,' ').trim();
              if (/paid promotion/i.test(lab))
                paid.push({lab:lab.slice(0,100), checked:el.getAttribute('aria-checked')==='true'});
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('[role=checkbox],tp-yt-paper-checkbox'):[])) {
              const lab=(el.getAttribute('aria-label')||'');
              if (/Allow automatic places/i.test(lab))
                state.places={lab, checked:el.getAttribute('aria-checked')==='true'};
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document); return {paid, places:state.places};
        }"""
    )


def scroll_label(page, label):
    page.evaluate(
        """(label)=>{
          const walk=(r,d=0)=>{
            if(!r||d>50) return false;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if ((el.innerText||'').trim()===label) { el.scrollIntoView({block:'center'}); return true; }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
            return false;
          }; return walk(document);
        }""",
        label,
    )
    page.wait_for_timeout(400)


def open_value(page, label, value):
    scroll_label(page, label)
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
              if (!best||score<best.score) { best={t,y:b.y}; bestEl=el; }
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


def visible_options(page):
    return page.evaluate(
        """()=>{
          const out=[]; const seen=new Set();
          const walk=(r,d=0)=>{
            if(!r||d>55) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('tp-yt-paper-item,[role=option]'):[])) {
              const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
              if (!t||seen.has(t)) continue;
              const b=el.getBoundingClientRect();
              // only fully visible-ish
              if (b.width<30||b.height<14||b.y<60||b.y>820) continue;
              seen.add(t);
              out.push({t, x:b.x+b.width/2, y:b.y+b.height/2, top:b.y, h:b.height});
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document);
          out.sort((a,b)=>a.top-b.top);
          return out;
        }"""
    )


def find_listbox(page):
    return page.evaluate(
        """()=>{
          let best=null;
          const walk=(r,d=0)=>{
            if(!r||d>55) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('[role=listbox],tp-yt-paper-listbox'):[])) {
              const b=el.getBoundingClientRect();
              if (b.height>60&&b.width>80) best={x:b.x+b.width/2,y:b.y+100,h:b.height,w:b.width};
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('tp-yt-paper-item'):[])) {
              let p=el.parentElement;
              for (let i=0;i<8&&p;i++) {
                if (p.scrollHeight>p.clientHeight+40) {
                  const b=p.getBoundingClientRect();
                  if (b.height>60) best={x:b.x+b.width/2,y:b.y+100,h:b.height,w:b.width,scroll:true};
                  break;
                }
                p=p.parentElement;
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document); return best;
        }"""
    )


def pick_level_ks4_mouse(page):
    """Open Level, scroll until Key stage 4 is visible, mouse.click center."""
    opened = open_value(page, "Level", "None")
    page.wait_for_timeout(1100)
    box = find_listbox(page)
    seen = []
    for i in range(40):
        opts = visible_options(page)
        for o in opts:
            if o["t"] not in [x["t"] for x in seen]:
                seen.append({"t": o["t"], "y": o["top"]})
        match = [o for o in opts if o["t"] == "Key stage 4"]
        if match:
            o = match[0]
            page.mouse.click(o["x"], o["y"])
            page.wait_for_timeout(900)
            return {
                "opened": opened,
                "picked": o,
                "via": f"mouse_visible_wheel{i}",
                "seen": seen,
            }
        if box:
            page.mouse.move(box["x"], box["y"])
            page.mouse.wheel(0, 180)
        else:
            page.mouse.wheel(0, 180)
        page.wait_for_timeout(200)
    # try scrollTop on box via JS then mouse click
    page.evaluate(
        """()=>{
          let box=null;
          const walk=(r,d=0)=>{
            if(!r||d>55||box) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('[role=listbox],tp-yt-paper-listbox'):[])) {
              const b=el.getBoundingClientRect();
              if (b.height>60) box=el;
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document);
          if (box) {
            // scroll until Key stage 4 in view
            for (let i=0;i<80;i++) {
              const items=[...box.querySelectorAll('tp-yt-paper-item,[role=option]')];
              // also shadow
              const all=[];
              const w=(r,d=0)=>{
                if(!r||d>20) return;
                for (const el of (r.querySelectorAll?r.querySelectorAll('tp-yt-paper-item,[role=option]'):[])) all.push(el);
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) if(el.shadowRoot) w(el.shadowRoot,d+1);
              }; w(box);
              const hit=all.find(el=>(el.innerText||'').replace(/\\s+/g,' ').trim()==='Key stage 4');
              if (hit) { hit.scrollIntoView({block:'center'}); return true; }
              const before=box.scrollTop; box.scrollTop=before+120;
              if (box.scrollTop===before) break;
            }
          }
          return false;
        }"""
    )
    page.wait_for_timeout(400)
    opts = visible_options(page)
    match = [o for o in opts if o["t"] == "Key stage 4"]
    if match:
        o = match[0]
        page.mouse.click(o["x"], o["y"])
        page.wait_for_timeout(900)
        return {"opened": opened, "picked": o, "via": "mouse_after_scrollTop", "seen": seen}
    return {"opened": opened, "picked": None, "via": "miss", "seen": seen}


def av(page, u):
    body = page.inner_text("body")
    import re
    return {
        "chip": u.visibility_chip(page),
        "not_kids": bool(re.search(r"set to not\s*['\"]?Made for Kids", body, re.I)),
    }


def main():
    u = load_u()
    result = {
        "video": VID,
        "started": datetime.now(LONDON).isoformat(timespec="seconds"),
        "notes": {
            "academic": "Studio has England/Scotland/Wales — not 'United Kingdom'. Set England (not UAE).",
            "level": "Under England, options are Key stages. Target Key stage 4 (GCSE secondary years).",
            "exam": "GCSE Chemistry is NOT in YouTube Studio exam taxonomy (GCSE→CBSE false friend; Chemistry→AP Chemistry + Indian exams).",
        },
    }
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
            page.wait_for_timeout(4000)
            u.dismiss(page)
            show_more(page)
            result["before"] = selects(page)

            pick = pick_level_ks4_mouse(page)
            result["level_pick"] = pick
            # dump probe options
            probe = {}
            if (EV / "DROPDOWN_PROBE.json").exists():
                try:
                    probe = json.loads((EV / "DROPDOWN_PROBE.json").read_text())
                except Exception:
                    pass
            probe["Level"] = {
                "want": "Key stage 4",
                "picked": pick.get("picked"),
                "via": pick.get("via"),
                "options": pick.get("seen") or [],
            }
            result["selects_after_pick"] = selects(page)
            # Wait for Save to enable
            save_enabled = False
            for _ in range(10):
                s = page.evaluate(
                    """()=>{
                      const walk=(r,d=0)=>{
                        if(!r||d>50) return null;
                        for (const el of (r.querySelectorAll?r.querySelectorAll('button,ytcp-button'):[])) {
                          const t=(el.innerText||'').trim();
                          if (t==='Save' || t.startsWith('Save')) {
                            const dis=el.disabled || el.getAttribute('aria-disabled')==='true' || el.hasAttribute('disabled');
                            return {t, disabled:dis, aria:el.getAttribute('aria-disabled')};
                          }
                        }
                        for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                          if (el.shadowRoot) { const h=walk(el.shadowRoot,d+1); if(h) return h; }
                        return null;
                      }; return walk(document);
                    }"""
                )
                result.setdefault("save_poll", []).append(s)
                if s and not s.get("disabled"):
                    save_enabled = True
                    break
                page.wait_for_timeout(400)
            save = u.page_save(page)
            result["level_save"] = save
            result["save_enabled_poll"] = save_enabled
            page.wait_for_timeout(3000)
            result["selects_after_save"] = selects(page)
            shot(page, "fri_manual_level.png")

            # reload verify
            page.goto(
                f"https://studio.youtube.com/video/{VID}/edit",
                wait_until="domcontentloaded",
                timeout=120000,
            )
            page.wait_for_timeout(4500)
            u.dismiss(page)
            show_more(page)
            for _ in range(14):
                page.mouse.wheel(0, 650)
                page.wait_for_timeout(50)
            result["final_selects"] = selects(page)
            result["final_tags"] = chips(page)
            # paid/places: scroll further
            for _ in range(10):
                page.mouse.wheel(0, 700)
                page.wait_for_timeout(50)
            result["final_pp"] = paid_places(page)
            # scroll back for education shot
            for _ in range(20):
                page.mouse.wheel(0, -700)
                page.wait_for_timeout(40)
            scroll_label(page, "Academic system")
            shot(page, "fri_manual_99_education.png")
            shot(page, "fri_manual_99_final.png")

            # Also copy prior successful field screenshots if missing BEN prefix
            for name in [
                "fri_manual_paid.png",
                "fri_manual_places.png",
                "fri_manual_tags.png",
                "fri_manual_lang.png",
                "fri_manual_academic.png",
                "fri_manual_type.png",
            ]:
                src = EV / name
                if src.exists():
                    shutil.copy2(src, ART / f"BEN_1445FIX_{name}")

            fs = " | ".join(result["final_selects"])
            ft = result["final_tags"]
            pp = result.get("final_pp") or {}
            paid_ok = any(
                "doesn't include paid" in (p.get("lab") or "").lower() and p.get("checked")
                for p in pp.get("paid") or []
            )
            places_ok = (pp.get("places") or {}).get("checked") is False
            result["final"] = {
                "lang_uk": "Title and description language English (United Kingdom)" in fs,
                "lang_ukrainian_bad": "Ukrainian" in fs,
                "academic_england_uk": "Academic system England" in fs,
                "academic_uae_bad": "United Arab Emirates" in fs,
                "type_concept": "Concept overview" in fs,
                "level_ks4": "Key stage 4" in fs,
                "level_secondary_school": "Secondary school" in fs,
                "exam_gcse": "GCSE Chemistry" in fs,
                "exam_ap_bad": "AP Chemistry" in fs,
                "exam_unavailable": True,
                "exam_note": "GCSE Chemistry not present in Studio exam search taxonomy for this video",
                "tags": ft,
                "tags_ok": set(FRI_TAGS) == set(ft),
                "paid_no": paid_ok,
                "places_off": places_ok,
                "audience_not_kids": bool(av(page, u).get("not_kids")),
                "visibility_scheduled": "Scheduled" in str(av(page, u).get("chip") or ""),
                "selects": result["final_selects"],
            }
            f = result["final"]
            # OK if all settable targets pass; exam is catalog-blocked
            result["ok_settable"] = all(
                [
                    f["lang_uk"],
                    not f["lang_ukrainian_bad"],
                    f["academic_england_uk"],
                    not f["academic_uae_bad"],
                    f["type_concept"],
                    f["level_ks4"],
                    f["tags_ok"],
                    f["paid_no"],
                    f["places_off"],
                    f["audience_not_kids"],
                    f["visibility_scheduled"],
                ]
            )
            result["ok"] = result["ok_settable"] and f["exam_gcse"]
            result["finished"] = datetime.now(LONDON).isoformat(timespec="seconds")

            probe["v10"] = result
            (EV / "DROPDOWN_PROBE.json").write_text(json.dumps(probe, indent=2, default=str))
            shutil.copy2(EV / "DROPDOWN_PROBE.json", ART / "BEN_1445FIX_DROPDOWN_PROBE.json")
            (EV / "FRI_MANUAL_RESULT.json").write_text(json.dumps(result, indent=2, default=str))
            shutil.copy2(EV / "FRI_MANUAL_RESULT.json", ART / "BEN_1445FIX_FRI_MANUAL_RESULT.json")
            print(json.dumps(result["final"], indent=2, default=str))
            print("ok_settable=", result["ok_settable"], "ok=", result["ok"])
            print("level_save", result.get("level_save"), "after_pick", result.get("selects_after_pick"))
        finally:
            page.close()


if __name__ == "__main__":
    main()
