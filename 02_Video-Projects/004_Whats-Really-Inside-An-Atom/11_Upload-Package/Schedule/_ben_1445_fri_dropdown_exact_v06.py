#!/usr/bin/env python3
"""Fri 29bpGAI0wb8 Studio fixes v06 — scrollTop list harvest + exact click.

Academic system: Studio has England/Scotland/Wales (no 'United Kingdom').
Use England for UK (NOT United Arab Emirates). Language exact EN-GB.
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
# Studio academic list has no "United Kingdom" — England is the UK system for GCSE.
ACADEMIC_WANT = "England"
PROBE: dict = {}


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
    EV.mkdir(parents=True, exist_ok=True)
    path = EV / "DROPDOWN_PROBE.json"
    path.write_text(json.dumps(PROBE, indent=2, default=str))
    shutil.copy2(path, ART / "BEN_1445FIX_DROPDOWN_PROBE.json")


def open_edit(page, u):
    page.goto(
        f"https://studio.youtube.com/video/{VID}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3500)
    u.dismiss(page)
    assert VID in page.url and "CUu8k38iAMc" not in page.url


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


def scroll_find(page, pat: str) -> bool:
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
        "kids_no_checked": page.evaluate(
            """() => {
              let no=false, yes=false;
              const walk=(r,d=0)=>{
                if(!r||d>50) return;
                for (const el of (r.querySelectorAll?r.querySelectorAll('[role=radio],tp-yt-paper-radio-button'):[])) {
                  const lab=(el.getAttribute('aria-label')||el.innerText||'');
                  const on=el.getAttribute('aria-checked')==='true';
                  if (/No, it.?s not.?Made for Kids/i.test(lab) && on) no=true;
                  if (/Yes, it.?s Made for Kids/i.test(lab) && on) yes=true;
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                  if (el.shadowRoot) walk(el.shadowRoot,d+1);
              }; walk(document); return {no, yes};
            }"""
        ),
    }


def save_rr(page, u, label):
    s = u.page_save(page)
    page.wait_for_timeout(2800)
    a = av(page, u)
    print(
        f"  SAVE {label} clicked={s.get('clicked')} chip={a.get('chip')} not_kids={a.get('not_kids')}",
        flush=True,
    )
    return {"label": label, "save": s, **a}


def click_radio_by_text(page, exact: str):
    return page.evaluate(
        """(want)=>{
          let hit=null;
          const walk=(r,d=0)=>{
            if(!r||d>55||hit) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('tp-yt-paper-radio-button,[role=radio]'):[])) {
              const lab=(el.getAttribute('aria-label')||el.innerText||'').replace(/\\s+/g,' ').trim();
              if (lab !== want) continue;
              el.scrollIntoView({block:'center'});
              el.click();
              hit={lab, checked:el.getAttribute('aria-checked')==='true'};
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document);
          const walk2=(r,d=0)=>{
            if(!r||d>55||!hit) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('tp-yt-paper-radio-button,[role=radio]'):[])) {
              const lab=(el.getAttribute('aria-label')||el.innerText||'').replace(/\\s+/g,' ').trim();
              if (lab===want) hit.checked=el.getAttribute('aria-checked')==='true';
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk2(el.shadowRoot,d+1);
          }; walk2(document);
          return hit;
        }""",
        exact,
    )


def set_check(page, pat, want):
    return page.evaluate(
        """(args)=>{
          const re=new RegExp(args[0],'i'), want=args[1];
          let found=null;
          const walk=(r,d=0)=>{
            if(!r||d>50||found) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('[role=checkbox],tp-yt-paper-checkbox'):[])) {
              const lab=(el.getAttribute('aria-label')||'').trim();
              if (!re.test(lab)) continue;
              el.scrollIntoView({block:'center'});
              const on=el.getAttribute('aria-checked')==='true';
              found={lab, before:on};
              if (on!==want) el.click();
              found.after=el.getAttribute('aria-checked')==='true';
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document); return found||{lab:'missing'};
        }""",
        [pat, want],
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


def clear_tags(page):
    n = 0
    for _ in range(80):
        hit = page.evaluate(
            """()=>{
              const walk=(r,d=0)=>{
                if(!r||d>50) return null;
                for (const el of (r.querySelectorAll?r.querySelectorAll('ytcp-chip,yt-chip-cloud-chip'):[])) {
                  const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
                  if (!t||t.length>120) continue;
                  let btn=null;
                  const findBtn=(node,dd=0)=>{
                    if(!node||dd>5||btn) return;
                    if (node.querySelector)
                      btn=node.querySelector('#delete-button,[icon=\"close\"],ytcp-icon-button,button');
                    if (!btn && node.shadowRoot) findBtn(node.shadowRoot, dd+1);
                  };
                  findBtn(el);
                  if (btn) { btn.click(); return {t:t.slice(0,50), via:'btn'}; }
                  const b=el.getBoundingClientRect();
                  if (b.width>20) return {x:b.x+b.width-8,y:b.y+b.height/2,t:t.slice(0,50),via:'coord'};
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                  if (el.shadowRoot) { const h=walk(el.shadowRoot,d+1); if(h) return h; }
                return null;
              }; return walk(document);
            }"""
        )
        if not hit:
            break
        if hit.get("via") == "coord":
            page.mouse.click(hit["x"], hit["y"])
        page.wait_for_timeout(150)
        n += 1
    return n


def fill_tags(page, tag_list):
    scroll_find(page, r"^Tags$")
    removed = clear_tags(page)
    info = {"removed": removed, "added": []}
    focused = page.evaluate(
        """()=>{
          const walk=(r,d=0)=>{
            if(!r||d>50) return null;
            for (const el of (r.querySelectorAll?r.querySelectorAll('input'):[])) {
              if (el.type!=='text') continue;
              const aria=(el.getAttribute('aria-label')||'');
              if (!/^Tags|Add tag/i.test(aria)) continue;
              el.scrollIntoView({block:'center'}); el.focus(); el.click();
              return {aria};
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) { const h=walk(el.shadowRoot,d+1); if(h) return h; }
            return null;
          }; return walk(document);
        }"""
    )
    info["input"] = focused
    if not focused:
        return info
    for tag in tag_list:
        page.evaluate(
            """()=>{
              const walk=(r,d=0)=>{
                if(!r||d>50) return false;
                for (const el of (r.querySelectorAll?r.querySelectorAll('input'):[])) {
                  const aria=(el.getAttribute('aria-label')||'');
                  if (/^Tags|Add tag/i.test(aria)) { el.focus(); el.click(); return true; }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                  if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
                return false;
              }; return walk(document);
            }"""
        )
        page.wait_for_timeout(80)
        page.keyboard.type(tag, delay=20)
        page.keyboard.press("Enter")
        page.wait_for_timeout(350)
        info["added"].append(tag)
    info["chips"] = chips(page)
    return info


def open_by_value(page, label: str, value: str):
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
              if (!best||score<best.score) { best={t,y:b.y,x:b.x,score}; bestEl=el; }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk2(el.shadowRoot,d+1);
          }; walk2(document);
          if(!bestEl) {
            // click combobox trigger containing label
            const walk3=(r,d=0)=>{
              if(!r||d>50) return;
              for (const el of (r.querySelectorAll?r.querySelectorAll('ytcp-dropdown-trigger,ytcp-text-dropdown-trigger,[role=combobox]'):[])) {
                const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
                if (!t.includes(label)) continue;
                const b=el.getBoundingClientRect();
                if (Math.abs(b.y-lab.y)>140) continue;
                bestEl=el; best={t:t.slice(0,90),y:b.y,via:'trig'};
              }
              for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                if (el.shadowRoot) walk3(el.shadowRoot,d+1);
            }; walk3(document);
          }
          if(!bestEl) return {error:'no_value', lab:{x:lab.x,y:lab.y}};
          bestEl.click();
          return {ok:true, clicked:best};
        }""",
        [label, value],
    )


def find_and_click_exact(page, want: str):
    """Scroll listbox via scrollTop until exact option exists, then click it. Dump all seen."""
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
          if (!box) return {error:'no_listbox', seen:[]};

          const seen=[]; const seenSet=new Set();
          const noteVisible=()=>{
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
                el.scrollIntoView({block:'nearest'});
                const b=el.getBoundingClientRect();
                el.click();
                hit={t,y:b.y,x:b.x,w:b.width,h:b.height};
              }
              for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                if (el.shadowRoot) walk(el.shadowRoot,d+1);
            }; walk(document); return hit;
          };

          box.scrollTop = 0;
          noteVisible();
          let hit=clickWant();
          if (hit) return {picked:hit, seen, via:'top'};
          for (let i=0;i<90;i++) {
            const before=box.scrollTop;
            box.scrollTop = before + Math.max(100, Math.floor(box.clientHeight*0.65));
            noteVisible();
            hit=clickWant();
            if (hit) return {picked:hit, seen, via:'scroll'+i, scrollTop:box.scrollTop};
            if (box.scrollTop===before) break;
          }
          box.scrollTop = box.scrollHeight;
          noteVisible();
          hit=clickWant();
          return {picked:hit, seen, via: hit?'bottom':'miss'};
        }""",
        want,
    )


def set_dd(page, label: str, want: str, open_value: str):
    opened = open_by_value(page, label, open_value)
    page.wait_for_timeout(1100)
    if (opened or {}).get("error"):
        opened = open_by_value(page, label, open_value)
        page.wait_for_timeout(1100)
    pick = find_and_click_exact(page, want)
    # probe dump with y coords
    PROBE[label] = {
        "want": want,
        "opened": opened,
        "picked": pick.get("picked"),
        "via": pick.get("via"),
        "options": [{"t": o["t"], "y": o.get("y")} for o in (pick.get("seen") or [])],
    }
    dump_probe()
    page.wait_for_timeout(600)
    # DO NOT Escape immediately — selection may need a beat; soft dismiss only if still open
    page.wait_for_timeout(300)
    return {"label": label, "want": want, "opened": opened, "pick": pick}


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


def trigger_value(page, label: str) -> str:
    for s in selects(page):
        if s.startswith(label):
            return s[len(label) :].strip()
    return ""


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


def set_exam(page, want: str, type_text: str):
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
    page.mouse.click(loc["x"], loc["y"], click_count=3)
    page.keyboard.press("Backspace")
    page.wait_for_timeout(200)
    page.keyboard.type(type_text, delay=40)
    page.wait_for_timeout(2000)
    pick = find_and_click_exact(page, want)
    info["pick"] = pick
    PROBE["Exam, course or standard"] = {
        "want": want,
        "typed": type_text,
        "picked": pick.get("picked"),
        "options": [{"t": o["t"], "y": o.get("y")} for o in (pick.get("seen") or [])],
    }
    dump_probe()
    if not pick.get("picked"):
        page.mouse.click(loc["x"], loc["y"], click_count=3)
        page.keyboard.press("Backspace")
        page.keyboard.type("GCSE", delay=40)
        page.wait_for_timeout(2000)
        pick2 = find_and_click_exact(page, want)
        info["pick2"] = pick2
        PROBE["Exam, course or standard __retry"] = {
            "want": want,
            "options": [{"t": o["t"], "y": o.get("y")} for o in (pick2.get("seen") or [])],
            "picked": pick2.get("picked"),
        }
        dump_probe()
    page.wait_for_timeout(400)
    return info


def main():
    global PROBE
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    PROBE = {
        "video": VID,
        "started": datetime.now(LONDON).isoformat(timespec="seconds"),
        "note": "Academic system Studio list has England/Scotland/Wales — not United Kingdom. Using England for UK.",
    }
    u = load_u()
    result = {
        "video": VID,
        "channel": "@HistoryOfScienceYT",
        "started": datetime.now(LONDON).isoformat(timespec="seconds"),
        "academic_note": "Studio has no 'United Kingdom' academic system; selected England (UK) not UAE.",
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
            result["before_tags"] = chips(page)
            result["before_av"] = av(page, u)
            shot(page, "fri_manual_00_before.png")

            # Paid
            scroll_find(page, r"Paid promotion")
            result["paid"] = click_radio_by_text(
                page, "No, my video doesn't include paid promotion"
            )
            result["steps"].append(save_rr(page, u, "paid_no"))
            shot(page, "fri_manual_paid.png")

            # Places
            scroll_find(page, r"Allow automatic places")
            result["places"] = set_check(page, r"Allow automatic places", False)
            result["steps"].append(save_rr(page, u, "places_off"))
            shot(page, "fri_manual_places.png")

            # Tags
            clear_tags(page)
            tags = fill_tags(page, FRI_TAGS)
            if set(chips(page)) != set(FRI_TAGS):
                clear_tags(page)
                tags = fill_tags(page, FRI_TAGS)
            result["tags"] = tags
            result["steps"].append(save_rr(page, u, "tags"))
            shot(page, "fri_manual_tags.png")

            # Language EN-GB
            lang_cur = trigger_value(page, "Title and description language") or "Ukrainian"
            lang = set_dd(
                page,
                "Title and description language",
                "English (United Kingdom)",
                lang_cur,
            )
            result["lang"] = lang
            result["steps"].append(save_rr(page, u, "lang_en_uk"))
            shot(page, "fri_manual_lang.png")
            if "English (United Kingdom)" not in " | ".join(selects(page)):
                lang2 = set_dd(
                    page,
                    "Title and description language",
                    "English (United Kingdom)",
                    trigger_value(page, "Title and description language") or lang_cur,
                )
                result["lang_retry"] = lang2
                result["steps"].append(save_rr(page, u, "lang_retry"))
                shot(page, "fri_manual_lang_retry.png")

            # Academic England (UK) — NOT UAE
            acad_cur = trigger_value(page, "Academic system") or "United Arab Emirates"
            acad = set_dd(page, "Academic system", ACADEMIC_WANT, acad_cur)
            result["academic"] = acad
            result["steps"].append(save_rr(page, u, "academic_england"))
            shot(page, "fri_manual_academic.png")

            # Type
            typ_cur = trigger_value(page, "Type") or "None"
            typ = set_dd(page, "Type", "Concept overview", typ_cur if typ_cur else "None")
            result["type"] = typ
            result["steps"].append(save_rr(page, u, "type_concept"))
            shot(page, "fri_manual_type.png")

            # Level
            lev_cur = trigger_value(page, "Level") or "None"
            lev = set_dd(page, "Level", "Secondary school", lev_cur)
            result["level"] = lev
            result["steps"].append(save_rr(page, u, "level_secondary"))
            shot(page, "fri_manual_level.png")
            # verify mid
            if "Secondary" not in " | ".join(selects(page)):
                lev2 = set_dd(page, "Level", "Secondary school", "None")
                result["level_retry"] = lev2
                result["steps"].append(save_rr(page, u, "level_retry"))
                shot(page, "fri_manual_level_retry.png")

            # Exam GCSE
            exam = set_exam(page, "GCSE Chemistry", "GCSE Chemistry")
            result["exam"] = exam
            result["steps"].append(save_rr(page, u, "exam_gcse"))
            shot(page, "fri_manual_exam.png")

            # Final
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
            scroll_find(page, r"Academic system")
            shot(page, "fri_manual_99_education.png")

            fs = " | ".join(result["final_selects"])
            ft = result["final_tags"]
            paid_ok = any(
                "doesn't include paid" in (p.get("lab") or "").lower() and p.get("checked")
                for p in result.get("final_paid") or []
            )
            places_ok = (result.get("final_places") or {}).get("checked") is False
            result["final"] = {
                "lang_uk": "Title and description language English (United Kingdom)" in fs,
                "lang_ukrainian_bad": "Ukrainian" in fs,
                "academic_england_uk": "Academic system England" in fs,
                "academic_uae_bad": "United Arab Emirates" in fs,
                "academic_note": "Studio list has England not 'United Kingdom'",
                "type_concept": "Concept overview" in fs,
                "level_secondary": "Secondary school" in fs
                or bool(re.search(r"Level Secondary\b", fs)),
                "exam_gcse": "GCSE Chemistry" in fs,
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
                    f["level_secondary"],
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
