#!/usr/bin/env python3
"""Fri 29bpGAI0wb8 finish Level + Exam only (v07).

After Academic=England, Level list is UK key stages (no 'Secondary school').
Use Key stage 4 (GCSE years) as Secondary equivalent, then GCSE Chemistry.
"""
from __future__ import annotations

import importlib.util
import json
import re
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
PROBE: dict = {}

# Import helpers by loading v06 module pieces inline via exec of key funcs —
# keep this file self-contained for the remaining two fields.


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


def dump_probe():
    path = EV / "DROPDOWN_PROBE.json"
    # merge with existing
    old = {}
    if path.exists():
        try:
            old = json.loads(path.read_text())
        except Exception:
            old = {}
    old.update(PROBE)
    path.write_text(json.dumps(old, indent=2, default=str))
    shutil.copy2(path, ART / "BEN_1445FIX_DROPDOWN_PROBE.json")


def open_edit(page, u):
    page.goto(
        f"https://studio.youtube.com/video/{VID}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3500)
    u.dismiss(page)


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
    for _ in range(36):
        if page.evaluate(
            """(pat)=>{
              const re=new RegExp(pat,'i');
              const walk=(r,d=0)=>{
                if(!r||d>50) return false;
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                  const t=(el.innerText||'').trim();
                  if (re.test(t) && t.length<90) { el.scrollIntoView({block:'center'}); return true; }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                  if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
                return false;
              }; return walk(document);
            }""",
            pat,
        ):
            page.wait_for_timeout(350)
            return True
        page.mouse.wheel(0, 650)
        page.wait_for_timeout(80)
    return False


def av(page, u):
    body = page.inner_text("body")
    return {
        "chip": u.visibility_chip(page),
        "not_kids": bool(re.search(r"set to not\s*['\"]?Made for Kids", body, re.I)),
    }


def save_rr(page, u, label):
    s = u.page_save(page)
    page.wait_for_timeout(2800)
    a = av(page, u)
    print(f"  SAVE {label} clicked={s.get('clicked')} chip={a.get('chip')}", flush=True)
    return {"label": label, "save": s, **a}


def open_by_value(page, label, value):
    scroll_find(page, "^" + re.escape(label) + "$")
    page.wait_for_timeout(250)
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
              if (t!==want && !(want && t.includes(want))) continue;
              if (t.length>90) continue;
              const b=el.getBoundingClientRect();
              if (b.width<15||b.height<10||b.height>50) continue;
              if (b.y<lab.y-5||b.y>lab.y+130) continue;
              if (b.x<lab.x-40) continue;
              const score=Math.abs(b.y-(lab.y+22))+(t===want?0:5);
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


def find_and_click_exact(page, want):
    return page.evaluate(
        """(want)=>{
          let box=null;
          const findBox=(r,d=0)=>{
            if(!r||d>55||box) return;
            for (const el of (r.querySelectorAll
              ? r.querySelectorAll('[role=listbox],tp-yt-paper-listbox')
              : [])) {
              const b=el.getBoundingClientRect();
              if (b.height>60&&b.width>80) box=el;
            }
            if (!box) {
              for (const el of (r.querySelectorAll?r.querySelectorAll('tp-yt-paper-item,[role=option]'):[])) {
                let p=el.parentElement;
                for (let i=0;i<10&&p;i++) {
                  if (p.scrollHeight > p.clientHeight+40) { box=p; break; }
                  p=p.parentElement;
                }
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) findBox(el.shadowRoot,d+1);
          }; findBox(document);
          if (!box) {
            // still try click without scroll
            let hit=null;
            const walk=(r,d=0)=>{
              if(!r||d>40||hit) return;
              for (const el of (r.querySelectorAll?r.querySelectorAll('tp-yt-paper-item,[role=option]'):[])) {
                const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
                if (t!==want) continue;
                el.scrollIntoView({block:'nearest'}); el.click();
                const b=el.getBoundingClientRect();
                hit={t,y:b.y,x:b.x};
              }
              for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                if (el.shadowRoot) walk(el.shadowRoot,d+1);
            }; walk(document);
            return {picked:hit, seen:[], via: hit?'direct':'no_listbox'};
          }
          const seen=[]; const seenSet=new Set();
          const note=()=>{
            const walk=(r,d=0)=>{
              if(!r||d>40) return;
              for (const el of (r.querySelectorAll?r.querySelectorAll('tp-yt-paper-item,[role=option]'):[])) {
                const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
                if (!t||seenSet.has(t)) continue;
                const b=el.getBoundingClientRect();
                if (b.width<30||b.height<10) continue;
                seenSet.add(t); seen.push({t,y:b.y});
              }
              for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                if (el.shadowRoot) walk(el.shadowRoot,d+1);
            }; walk(document);
          };
          const clickWant=()=>{
            let hit=null;
            const walk=(r,d=0)=>{
              if(!r||d>40||hit) return;
              for (const el of (r.querySelectorAll?r.querySelectorAll('tp-yt-paper-item,[role=option]'):[])) {
                const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
                if (t!==want) continue;
                el.scrollIntoView({block:'nearest'}); el.click();
                const b=el.getBoundingClientRect();
                hit={t,y:b.y,x:b.x,w:b.width,h:b.height};
              }
              for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                if (el.shadowRoot) walk(el.shadowRoot,d+1);
            }; walk(document); return hit;
          };
          box.scrollTop=0; note();
          let hit=clickWant();
          if (hit) return {picked:hit, seen, via:'top'};
          for (let i=0;i<90;i++) {
            const before=box.scrollTop;
            box.scrollTop=before+Math.max(100, Math.floor(box.clientHeight*0.65));
            note(); hit=clickWant();
            if (hit) return {picked:hit, seen, via:'scroll'+i};
            if (box.scrollTop===before) break;
          }
          box.scrollTop=box.scrollHeight; note(); hit=clickWant();
          return {picked:hit, seen, via: hit?'bottom':'miss'};
        }""",
        want,
    )


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


def paid_state(page):
    return page.evaluate(
        """()=>{
          const out=[];
          const walk=(r,d=0)=>{
            if(!r||d>50) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('tp-yt-paper-radio-button,[role=radio]'):[])) {
              const lab=(el.getAttribute('aria-label')||el.innerText||'').replace(/\\s+/g,' ').trim();
              if (/paid promotion/i.test(lab))
                out.push({lab:lab.slice(0,100), checked:el.getAttribute('aria-checked')==='true'});
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document); return out;
        }"""
    )


def set_dd(page, label, want, open_value):
    opened = open_by_value(page, label, open_value)
    page.wait_for_timeout(1100)
    pick = find_and_click_exact(page, want)
    PROBE[label] = {
        "want": want,
        "opened": opened,
        "picked": pick.get("picked"),
        "via": pick.get("via"),
        "options": [{"t": o["t"], "y": o.get("y")} for o in (pick.get("seen") or [])],
    }
    dump_probe()
    page.wait_for_timeout(600)
    return {"label": label, "want": want, "opened": opened, "pick": pick}


def set_exam(page, want, type_text):
    scroll_find(page, r"Exam, course or standard")
    page.wait_for_timeout(300)
    loc = page.evaluate(
        """()=>{
          const walk=(r,d=0)=>{
            if(!r||d>50) return null;
            for (const el of (r.querySelectorAll?r.querySelectorAll('input'):[])) {
              const aria=(el.getAttribute('aria-label')||'');
              if (!/Exam, course or standard/i.test(aria)) continue;
              el.scrollIntoView({block:'center'}); el.click(); el.focus();
              const b=el.getBoundingClientRect();
              return {x:b.x+b.width/2,y:b.y+b.height/2,aria,ph:el.getAttribute('placeholder')||''};
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) { const h=walk(el.shadowRoot,d+1); if(h) return h; }
            return null;
          }; return walk(document);
        }"""
    )
    info = {"loc": loc, "want": want}
    if not loc:
        return {**info, "error": "no_input"}
    for attempt, text in enumerate([type_text, "GCSE Chemistry", "GCSE", "Chemistry"]):
        page.mouse.click(loc["x"], loc["y"], click_count=3)
        page.keyboard.press("Backspace")
        page.wait_for_timeout(200)
        page.keyboard.type(text, delay=40)
        page.wait_for_timeout(2200)
        # list options currently visible
        opts = page.evaluate(
            """()=>{
              const out=[]; const seen=new Set();
              const walk=(r,d=0)=>{
                if(!r||d>55) return;
                for (const el of (r.querySelectorAll?r.querySelectorAll('tp-yt-paper-item,[role=option]'):[])) {
                  const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
                  if (!t||seen.has(t)) continue;
                  const b=el.getBoundingClientRect();
                  if (b.width<30||b.height<10||b.y<0||b.y>1100) continue;
                  seen.add(t); out.push({t,y:b.y});
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                  if (el.shadowRoot) walk(el.shadowRoot,d+1);
              }; walk(document); return out;
            }"""
        )
        info[f"attempt_{attempt}"] = {"typed": text, "options": opts}
        PROBE[f"Exam attempt {attempt} typed={text}"] = {
            "want": want,
            "options": opts,
        }
        dump_probe()
        if any(o["t"] == want for o in opts):
            pick = find_and_click_exact(page, want)
            info["picked"] = pick
            PROBE["Exam, course or standard"] = {
                "want": want,
                "typed": text,
                "picked": pick.get("picked"),
                "options": opts,
            }
            dump_probe()
            page.wait_for_timeout(500)
            return info
        # also try fuzzy: any option that equals want after normalize
        exact = [o for o in opts if o["t"] == want]
        if exact:
            page.evaluate(
                """(want)=>{
                  const walk=(r,d=0)=>{
                    if(!r||d>55) return false;
                    for (const el of (r.querySelectorAll?r.querySelectorAll('tp-yt-paper-item,[role=option]'):[])) {
                      const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
                      if (t===want) { el.click(); return true; }
                    }
                    for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                      if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
                    return false;
                  }; return walk(document);
                }""",
                want,
            )
            info["picked"] = {"t": want, "via": "direct"}
            page.wait_for_timeout(500)
            return info
    info["picked"] = None
    return info


def main():
    global PROBE
    PROBE = {
        "v07": True,
        "started": datetime.now(LONDON).isoformat(timespec="seconds"),
        "note": "Level under England academic = Key stage 4 (GCSE secondary), not 'Secondary school'",
    }
    u = load_u()
    result = {
        "video": VID,
        "started": datetime.now(LONDON).isoformat(timespec="seconds"),
        "steps": [],
    }
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9460")
        page = browser.contexts[0].new_page()
        page.set_viewport_size({"width": 1400, "height": 900})
        try:
            open_edit(page, u)
            show_more(page)
            result["before_selects"] = selects(page)
            shot(page, "fri_manual_v07_00_before.png")

            # Level = Key stage 4 (GCSE secondary under England system)
            # Also accept Key stage 3 if KS4 fails
            lev = set_dd(page, "Level", "Key stage 4", "None")
            result["level"] = lev
            result["steps"].append(save_rr(page, u, "level_ks4"))
            shot(page, "fri_manual_level.png")
            if "Key stage 4" not in " | ".join(selects(page)):
                lev2 = set_dd(page, "Level", "Key stage 3", trigger_value := "None")
                # re-open current
                cur = "None"
                for s in selects(page):
                    if s.startswith("Level"):
                        cur = s.replace("Level", "").strip() or cur
                lev2 = set_dd(page, "Level", "Key stage 3", cur)
                result["level_ks3"] = lev2
                result["steps"].append(save_rr(page, u, "level_ks3"))
                shot(page, "fri_manual_level_retry.png")

            # Exam after level
            exam = set_exam(page, "GCSE Chemistry", "GCSE Chemistry")
            result["exam"] = exam
            result["steps"].append(save_rr(page, u, "exam_gcse"))
            shot(page, "fri_manual_exam.png")

            # If still missing, try opening exam without filter and scroll
            if "GCSE Chemistry" not in " | ".join(selects(page)) and "GCSE Chemistry" not in page.inner_text("body"):
                scroll_find(page, r"Exam, course or standard")
                # click into exam input, type GCSE slowly
                exam2 = set_exam(page, "GCSE Chemistry", "GCSE Chem")
                result["exam_retry"] = exam2
                result["steps"].append(save_rr(page, u, "exam_retry"))
                shot(page, "fri_manual_exam_retry.png")

            open_edit(page, u)
            show_more(page)
            result["final_selects"] = selects(page)
            result["final_tags"] = chips(page)
            result["final_av"] = av(page, u)
            scroll_find(page, r"Paid promotion")
            result["final_paid"] = paid_state(page)
            scroll_find(page, r"Allow automatic places")
            result["final_places"] = page.evaluate(
                """()=>{
                  let found=null;
                  const walk=(r,d=0)=>{
                    if(!r||d>50||found) return;
                    for (const el of (r.querySelectorAll?r.querySelectorAll('[role=checkbox],tp-yt-paper-checkbox'):[])) {
                      const lab=(el.getAttribute('aria-label')||'');
                      if (/Allow automatic places/i.test(lab))
                        found={lab, checked:el.getAttribute('aria-checked')==='true'};
                    }
                    for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                      if (el.shadowRoot) walk(el.shadowRoot,d+1);
                  }; walk(document); return found;
                }"""
            )
            shot(page, "fri_manual_99_final.png")
            scroll_find(page, r"Academic system|Level|Exam")
            shot(page, "fri_manual_99_education.png")

            fs = " | ".join(result["final_selects"])
            ft = result["final_tags"]
            paid_ok = any(
                "doesn't include paid" in (p.get("lab") or "").lower() and p.get("checked")
                for p in result.get("final_paid") or []
            )
            places_ok = (result.get("final_places") or {}).get("checked") is False
            level_ok = ("Key stage 4" in fs) or ("Key stage 3" in fs) or ("Secondary" in fs)
            result["final"] = {
                "lang_uk": "Title and description language English (United Kingdom)" in fs,
                "lang_ukrainian_bad": "Ukrainian" in fs,
                "academic_england_uk": "Academic system England" in fs,
                "academic_uae_bad": "United Arab Emirates" in fs,
                "type_concept": "Concept overview" in fs,
                "level_secondary_equiv": level_ok,
                "level_value": next((s for s in result["final_selects"] if s.startswith("Level")), None),
                "level_note": "Under England academic system, Studio shows Key stages not 'Secondary school'; used Key stage 4 (GCSE years)",
                "exam_gcse": "GCSE Chemistry" in fs or "GCSE Chemistry" in page.inner_text("body"),
                "exam_ap_bad": "AP Chemistry" in fs,
                "tags": ft,
                "tags_ok": set(FRI_TAGS) == set(ft),
                "paid_no": paid_ok,
                "places_off": places_ok,
                "audience_not_kids": bool(result["final_av"].get("not_kids")),
                "visibility_scheduled": "Scheduled"
                in str(result["final_av"].get("chip") or ""),
                "selects": result["final_selects"],
            }
            f = result["final"]
            result["ok"] = all(
                [
                    f["lang_uk"],
                    not f["lang_ukrainian_bad"],
                    f["academic_england_uk"],
                    not f["academic_uae_bad"],
                    f["type_concept"],
                    f["level_secondary_equiv"],
                    f["exam_gcse"],
                    not f["exam_ap_bad"],
                    f["tags_ok"],
                    f["paid_no"],
                    f["places_off"],
                    f["audience_not_kids"],
                    f["visibility_scheduled"],
                ]
            )
            result["finished"] = datetime.now(LONDON).isoformat(timespec="seconds")
            dump_probe()
            outp = EV / "FRI_MANUAL_RESULT.json"
            outp.write_text(json.dumps(result, indent=2, default=str))
            shutil.copy2(outp, ART / "BEN_1445FIX_FRI_MANUAL_RESULT.json")
            print(json.dumps(result["final"], indent=2, default=str))
            print("OK=", result["ok"])
        finally:
            page.close()


if __name__ == "__main__":
    main()
