#!/usr/bin/env python3
"""Fri 29bpGAI0wb8 Studio fixes v04 — scroll-into-view, element.click, UK academic first.

Order: paid → places → tags → language → academic(UK) → type → level → exam(GCSE).
Exact option innerText only. Never open CUu8k38iAMc.
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
PROBE = {}


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
        page.wait_for_timeout(450)


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
            page.wait_for_timeout(400)
            return True
        page.mouse.wheel(0, 650)
        page.wait_for_timeout(90)
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
    print(f"  SAVE {label} clicked={s.get('clicked')} chip={a.get('chip')} not_kids={a.get('not_kids')}", flush=True)
    return {"label": label, "save": s, **a}


def click_radio_by_text(page, exact: str):
    """Scroll paper-radio into view and el.click() — works for off-screen radios."""
    return page.evaluate(
        """(want)=>{
          let hit=null;
          const walk=(r,d=0)=>{
            if(!r||d>55||hit) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('tp-yt-paper-radio-button,[role=radio]'):[])) {
              const lab=(el.getAttribute('aria-label')||el.innerText||'').replace(/\\s+/g,' ').trim();
              if (lab !== want) continue;
              el.scrollIntoView({block:'center'});
              const b=el.getBoundingClientRect();
              el.click();
              hit={lab, x:b.x, y:b.y, w:b.width, h:b.height,
                   checked_before:el.getAttribute('aria-checked'),
                   checked_after:el.getAttribute('aria-checked')};
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document);
          // re-read
          const walk2=(r,d=0)=>{
            if(!r||d>55) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('tp-yt-paper-radio-button,[role=radio]'):[])) {
              const lab=(el.getAttribute('aria-label')||el.innerText||'').replace(/\\s+/g,' ').trim();
              if (lab===want) hit.checked_final=el.getAttribute('aria-checked')==='true';
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
    for _ in range(60):
        hit = page.evaluate(
            """()=>{
              const walk=(r,d=0)=>{
                if(!r||d>50) return null;
                for (const el of (r.querySelectorAll?r.querySelectorAll('ytcp-chip,yt-chip-cloud-chip'):[])) {
                  const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
                  if (!t||t.length>90) continue;
                  const btn=el.querySelector('[icon=close],#delete-icon,ytcp-icon-button,button')
                    || el.shadowRoot?.querySelector('[icon=close],#delete-icon,ytcp-icon-button,button');
                  if (btn) { btn.click(); return {t:t.slice(0,40), via:'btn'}; }
                  const b=el.getBoundingClientRect();
                  if (b.width>20) return {x:b.x+b.width-10,y:b.y+b.height/2,t:t.slice(0,40),via:'coord'};
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
        page.wait_for_timeout(180)
        n += 1
    return n


def fill_tags(page, tag_list):
    scroll_find(page, r"^Tags$")
    removed = clear_tags(page)
    info = {"removed": removed, "added": []}
    # Find tags input by aria
    loc = page.evaluate(
        """()=>{
          const walk=(r,d=0)=>{
            if(!r||d>50) return null;
            for (const el of (r.querySelectorAll?r.querySelectorAll('input'):[])) {
              if (el.type!=='text') continue;
              const aria=(el.getAttribute('aria-label')||'');
              if (/^Tags/i.test(aria) || aria==='Add tag' || /Add tag/i.test(aria)) {
                el.scrollIntoView({block:'center'});
                const b=el.getBoundingClientRect();
                return {x:b.x+b.width/2,y:b.y+b.height/2,aria};
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) { const h=walk(el.shadowRoot,d+1); if(h) return h; }
            return null;
          }; return walk(document);
        }"""
    )
    info["input"] = loc
    if not loc:
        return info
    for tag in tag_list:
        page.mouse.click(loc["x"], loc["y"])
        page.wait_for_timeout(120)
        # do NOT Meta+a — it selects page text. Clear via Backspace on empty field focus
        page.keyboard.type(tag, delay=25)
        page.keyboard.press("Enter")
        page.wait_for_timeout(450)
        info["added"].append(tag)
    info["chips"] = chips(page)
    return info


def click_dropdown_trigger(page, label: str):
    """Click ytcp-dropdown-trigger associated with exact label; prefer chevron side."""
    return page.evaluate(
        """(label)=>{
          let labs=[];
          const walk=(r,d=0)=>{
            if(!r||d>50) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const own=[...el.childNodes].filter(n=>n.nodeType===3).map(n=>n.textContent.trim()).join(' ').trim();
              if (own!==label && (el.innerText||'').trim()!==label) continue;
              const b=el.getBoundingClientRect();
              if (b.width>8&&b.height>8&&b.y>40&&b.y<1100)
                labs.push({el, x:b.x,y:b.y,w:b.width,h:b.height});
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document);
          labs.sort((a,b)=>(a.w*a.h)-(b.w*b.h));
          if (!labs.length) return {error:'no_lab'};
          const lab=labs[0];
          lab.el.scrollIntoView({block:'center'});
          let best=null, bestEl=null;
          const walk2=(r,d=0)=>{
            if(!r||d>50) return;
            for (const el of (r.querySelectorAll
              ? r.querySelectorAll('ytcp-dropdown-trigger,ytcp-text-dropdown-trigger,[role=combobox],ytcp-form-select')
              : [])) {
              const b=el.getBoundingClientRect();
              const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
              if (b.width<40||b.height<18||b.height>130) continue;
              if (Math.abs(b.y-lab.y)>160) continue;
              if (b.x < lab.x-40) continue;
              // Prefer controls that INCLUDE the label text (label+value stacked)
              const hasLab = t.includes(label) || Math.abs(b.y-(lab.y+20))<40;
              if (!hasLab && Math.abs(b.y-lab.y)>50) continue;
              const score = Math.abs(b.y-lab.y)*3 + (t.includes(label)?0:25);
              if (!best||score<best.score) {
                best={t:t.slice(0,100), y:b.y, x:b.x, w:b.width, h:b.height, score};
                bestEl=el;
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk2(el.shadowRoot,d+1);
          }; walk2(document);
          if (!bestEl) return {error:'no_trig', lab:{x:lab.x,y:lab.y}};
          bestEl.scrollIntoView({block:'center'});
          // click right side (chevron)
          const b=bestEl.getBoundingClientRect();
          bestEl.click();
          return {ok:true, trig:best, click:{x:b.x+b.width-20, y:b.y+b.height/2}};
        }""",
        label,
    )


def list_options(page):
    """All visible paper-item / role=option with y coords."""
    return page.evaluate(
        """()=>{
          const out=[]; const seen=new Set();
          const walk=(r,d=0)=>{
            if(!r||d>55) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('tp-yt-paper-item,[role=option]'):[])) {
              const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
              if (!t||t.length>120) continue;
              const b=el.getBoundingClientRect();
              if (b.width<40||b.height<12||b.height>90) continue;
              if (b.y<-20||b.y>1200) continue;
              const k=t+'@'+Math.round(b.y);
              if (seen.has(k)) continue; seen.add(k);
              out.push({t, y:Math.round(b.y*10)/10, x:Math.round(b.x*10)/10, w:b.width, h:b.height});
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document);
          out.sort((a,b)=>a.y-b.y);
          return out;
        }"""
    )


def click_option_exact(page, want: str):
    """Click paper-item whose innerText === want exactly. Returns pick info."""
    return page.evaluate(
        """(want)=>{
          let hit=null;
          const walk=(r,d=0)=>{
            if(!r||d>55||hit) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('tp-yt-paper-item,[role=option]'):[])) {
              const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
              if (t !== want) continue;
              const b=el.getBoundingClientRect();
              if (b.width<40||b.height<12) continue;
              el.scrollIntoView({block:'nearest'});
              el.click();
              hit={t, y:b.y, x:b.x, w:b.width, h:b.height};
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document); return hit;
        }""",
        want,
    )


def type_into_open_search(page, text: str, prefer_aria: str | None = None):
    """Type into the search/filter input that belongs to the open dropdown — never Tags, never channel search."""
    loc = page.evaluate(
        """(prefer)=>{
          const cands=[];
          const walk=(r,d=0)=>{
            if(!r||d>55) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('input'):[])) {
              if (el.type!=='text' && el.type!=='search' && el.type) continue;
              if (el.type==='hidden'||el.type==='file') continue;
              const aria=(el.getAttribute('aria-label')||'');
              const ph=(el.getAttribute('placeholder')||'');
              const b=el.getBoundingClientRect();
              if (b.width<40||b.height<8||b.y<0||b.y>1000) continue;
              if (/tag|hashtag|location|Search across your channel/i.test(aria+ph)) continue;
              cands.push({aria, ph, x:b.x+b.width/2, y:b.y+b.height/2, w:b.width, h:b.height, value:el.value||''});
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document);
          if (prefer) {
            const m=cands.find(c=> (c.aria+c.ph).toLowerCase().includes(prefer.toLowerCase()));
            if (m) return m;
          }
          // Prefer inputs with Search placeholder or recently focused-looking (lower y in form area)
          cands.sort((a,b)=>{
            const as=/search/i.test(a.ph+a.aria)?0:1;
            const bs=/search/i.test(b.ph+b.aria)?0:1;
            return as-bs || a.y-b.y;
          });
          return cands[0]||null;
        }""",
        prefer_aria,
    )
    if not loc:
        # fallback: just type (dropdown may accept keystrokes)
        page.keyboard.type(text, delay=40)
        page.wait_for_timeout(1400)
        return {"via": "keyboard", "text": text}
    page.mouse.click(loc["x"], loc["y"])
    page.wait_for_timeout(200)
    # Clear with triple-click + delete, NOT Meta+a (selects page)
    page.mouse.click(loc["x"], loc["y"], click_count=3)
    page.keyboard.press("Backspace")
    page.wait_for_timeout(150)
    page.keyboard.type(text, delay=40)
    page.wait_for_timeout(1600)
    return {"via": "input", "loc": loc, "text": text}


def set_dd(page, label: str, want: str, type_text: str | None = None, alts=None):
    alts = alts or []
    scroll_find(page, re.escape(label.split(",")[0] if len(label) > 20 else label))
    # More reliable: scroll exact label
    scroll_find(page, "^" + re.escape(label) + "$")
    page.wait_for_timeout(350)
    trig = click_dropdown_trigger(page, label)
    page.wait_for_timeout(1100)
    typed = None
    if type_text:
        typed = type_into_open_search(page, type_text, prefer_aria=label)
        page.wait_for_timeout(800)
    opts = list_options(page)
    # Scroll list within dropdown if needed
    for _ in range(8):
        if any(o["t"] == want for o in opts):
            break
        # try wheel inside list
        if opts:
            page.mouse.move(opts[-1]["x"] + 40, opts[-1]["y"])
            page.mouse.wheel(0, 240)
            page.wait_for_timeout(250)
            opts = list_options(page)
        elif type_text:
            break
        else:
            page.mouse.wheel(0, 200)
            page.wait_for_timeout(250)
            opts = list_options(page)

    PROBE[label] = {
        "want": want,
        "typed": typed,
        "trig": trig,
        "options": [{"t": o["t"], "y": o["y"]} for o in opts],
    }
    dump_probe()

    targets = [want] + [a for a in alts if a != want]
    picked = None
    for t in targets:
        exact = [o for o in opts if o["t"] == t]
        if not exact:
            continue
        # Safety rejects
        if t == "United Kingdom":
            bad = [o for o in exact if "Arab" in o["t"]]
            if bad:
                continue
        if "Chemistry" in t and t.startswith("AP"):
            continue
        picked = click_option_exact(page, t)
        if picked:
            break

    if not picked and type_text:
        # retry with shorter type
        short = type_text.split("(")[0].strip() if "(" in type_text else type_text.split()[0]
        if want == "United Kingdom":
            short = "United Kingdom"  # don't use just United
        if want == "English (United Kingdom)":
            short = "English (United Kingdom)"
        if want == "GCSE Chemistry":
            short = "GCSE"
        typed2 = type_into_open_search(page, short, prefer_aria=label)
        page.wait_for_timeout(1200)
        opts = list_options(page)
        PROBE[label + " __retry"] = {
            "want": want,
            "typed": typed2,
            "options": [{"t": o["t"], "y": o["y"]} for o in opts],
        }
        dump_probe()
        if any(o["t"] == want for o in opts):
            picked = click_option_exact(page, want)

    page.wait_for_timeout(500)
    try:
        page.keyboard.press("Escape")
    except Exception:
        pass
    page.wait_for_timeout(300)
    return {"label": label, "want": want, "trig": trig, "typed": typed, "picked": picked, "n_opts": len(opts)}


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


def main():
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    global PROBE
    PROBE = {"video": VID, "started": datetime.now(LONDON).isoformat(timespec="seconds")}
    u = load_u()
    result = {
        "video": VID,
        "channel": "@HistoryOfScienceYT",
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
            result["before_tags"] = chips(page)
            result["before_av"] = av(page, u)
            shot(page, "fri_manual_00_before.png")

            # 1 Paid
            scroll_find(page, r"Paid promotion")
            page.wait_for_timeout(400)
            paid = click_radio_by_text(page, "No, my video doesn't include paid promotion")
            page.wait_for_timeout(400)
            # if still not checked, click again
            if not (paid or {}).get("checked_final"):
                paid2 = click_radio_by_text(page, "No, my video doesn't include paid promotion")
                paid = {"first": paid, "second": paid2}
            result["paid"] = paid
            result["steps"].append(save_rr(page, u, "paid_no"))
            shot(page, "fri_manual_paid.png")

            # 2 Places
            scroll_find(page, r"Allow automatic places")
            result["places"] = set_check(page, r"Allow automatic places", False)
            result["steps"].append(save_rr(page, u, "places_off"))
            shot(page, "fri_manual_places.png")

            # 3 Tags
            tags = fill_tags(page, FRI_TAGS)
            have = set(chips(page))
            if not set(FRI_TAGS).issubset(have):
                # clear and retry full set
                clear_tags(page)
                tags = fill_tags(page, FRI_TAGS)
            result["tags"] = tags
            result["steps"].append(save_rr(page, u, "tags"))
            shot(page, "fri_manual_tags.png")

            # 4 Language
            lang = set_dd(
                page,
                "Title and description language",
                "English (United Kingdom)",
                type_text="English (United Kingdom)",
            )
            result["lang"] = lang
            result["steps"].append(save_rr(page, u, "lang_en_uk"))
            shot(page, "fri_manual_lang.png")
            if "English (United Kingdom)" not in " | ".join(selects(page)):
                lang2 = set_dd(
                    page,
                    "Title and description language",
                    "English (United Kingdom)",
                    type_text="United Kingdom)",
                )
                result["lang_retry"] = lang2
                result["steps"].append(save_rr(page, u, "lang_retry"))
                shot(page, "fri_manual_lang_retry.png")

            # 5 Academic FIRST (unlocks GCSE)
            acad = set_dd(
                page,
                "Academic system",
                "United Kingdom",
                type_text="United Kingdom",
            )
            result["academic"] = acad
            result["steps"].append(save_rr(page, u, "academic_uk"))
            shot(page, "fri_manual_academic.png")
            if "Academic system United Kingdom" not in " | ".join(selects(page)):
                acad2 = set_dd(page, "Academic system", "United Kingdom", type_text="Kingdom")
                # filter options manually if Kingdom matches both
                result["academic_retry"] = acad2
                result["steps"].append(save_rr(page, u, "academic_retry"))
                shot(page, "fri_manual_academic_retry.png")

            # 6 Type
            typ = set_dd(page, "Type", "Concept overview", type_text=None)
            result["type"] = typ
            result["steps"].append(save_rr(page, u, "type_concept"))
            shot(page, "fri_manual_type.png")

            # 7 Level
            lev = set_dd(
                page,
                "Level",
                "Secondary school",
                type_text=None,
                alts=["Secondary"],
            )
            result["level"] = lev
            result["steps"].append(save_rr(page, u, "level_secondary"))
            shot(page, "fri_manual_level.png")

            # 8 Exam — after UK academic
            exam = set_dd(
                page,
                "Exam, course or standard",
                "GCSE Chemistry",
                type_text="GCSE Chemistry",
            )
            result["exam"] = exam
            result["steps"].append(save_rr(page, u, "exam_gcse"))
            shot(page, "fri_manual_exam.png")
            if "GCSE Chemistry" not in " | ".join(selects(page)):
                exam2 = set_dd(
                    page,
                    "Exam, course or standard",
                    "GCSE Chemistry",
                    type_text="GCSE",
                )
                result["exam_retry"] = exam2
                result["steps"].append(save_rr(page, u, "exam_retry"))
                shot(page, "fri_manual_exam_retry.png")

            # Final verify
            open_edit(page, u)
            show_more(page)
            page.wait_for_timeout(1000)
            result["final_selects"] = selects(page)
            result["final_tags"] = chips(page)
            result["final_av"] = av(page, u)
            scroll_find(page, r"Paid promotion")
            result["final_paid"] = paid_state(page)
            scroll_find(page, r"Allow automatic places")
            places = page.evaluate(
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
            result["final_places"] = places
            shot(page, "fri_manual_99_final.png")
            scroll_find(page, r"Academic system")
            shot(page, "fri_manual_99_education.png")

            fs = " | ".join(result["final_selects"])
            ft = result["final_tags"]
            paid_ok = any(
                "doesn't include paid" in (p.get("lab") or "").lower() and p.get("checked")
                for p in result.get("final_paid") or []
            )
            places_ok = places is not None and places.get("checked") is False
            result["final"] = {
                "lang_uk": "Title and description language English (United Kingdom)" in fs,
                "lang_ukrainian_bad": "Ukrainian" in fs,
                "academic_uk": "Academic system United Kingdom" in fs,
                "academic_uae_bad": "United Arab Emirates" in fs,
                "type_concept": "Concept overview" in fs,
                "level_secondary": ("Secondary school" in fs)
                or bool(re.search(r"Level Secondary\b", fs)),
                "exam_gcse": "GCSE Chemistry" in fs,
                "exam_ap_bad": "AP Chemistry" in fs,
                "tags": ft,
                "tags_ok": set(FRI_TAGS).issubset(set(ft))
                and len([t for t in ft if t in FRI_TAGS]) >= 6,
                "paid_no": paid_ok,
                "places_off": places_ok,
                "audience_not_kids": bool(result["final_av"].get("not_kids")),
                "visibility_scheduled": "Scheduled" in str(result["final_av"].get("chip") or ""),
                "selects": result["final_selects"],
            }
            f = result["final"]
            result["ok"] = all(
                [
                    f["lang_uk"],
                    not f["lang_ukrainian_bad"],
                    f["academic_uk"],
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
