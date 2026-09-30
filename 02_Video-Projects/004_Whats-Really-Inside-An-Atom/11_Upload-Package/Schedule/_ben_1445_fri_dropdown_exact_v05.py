#!/usr/bin/env python3
"""Fri 29bpGAI0wb8 Studio fixes v05 — open by value-click, scroll listbox, exact pick.

Never Meta+a / never type into Tags while picking dropdowns.
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
    print(f"  SAVE {label} clicked={s.get('clicked')} chip={a.get('chip')} not_kids={a.get('not_kids')}", flush=True)
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
                  // try close button in light/shadow
                  let btn=null;
                  const findBtn=(node,dd=0)=>{
                    if(!node||dd>5||btn) return;
                    if (node.querySelector) {
                      btn=node.querySelector('#delete-button, #remove-icon, [icon=\"close\"], ytcp-icon-button, button');
                    }
                    if (!btn && node.shadowRoot) findBtn(node.shadowRoot, dd+1);
                    if (node.children) for (const c of node.children) findBtn(c, dd+1);
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
        page.wait_for_timeout(160)
        n += 1
    return n


def fill_tags(page, tag_list):
    scroll_find(page, r"^Tags$")
    removed = clear_tags(page)
    info = {"removed": removed, "added": []}
    # Focus tags input via element.click in evaluate
    focused = page.evaluate(
        """()=>{
          const walk=(r,d=0)=>{
            if(!r||d>50) return null;
            for (const el of (r.querySelectorAll?r.querySelectorAll('input'):[])) {
              if (el.type!=='text') continue;
              const aria=(el.getAttribute('aria-label')||'');
              if (!/^Tags/i.test(aria) && aria!=='Add tag' && !/Add tag/i.test(aria)) continue;
              el.scrollIntoView({block:'center'});
              el.focus(); el.click();
              const b=el.getBoundingClientRect();
              return {aria, x:b.x, y:b.y};
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
                if(!r||d>50) return null;
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
        page.wait_for_timeout(100)
        page.keyboard.type(tag, delay=22)
        page.keyboard.press("Enter")
        page.wait_for_timeout(400)
        info["added"].append(tag)
    info["chips"] = chips(page)
    return info


def open_by_value(page, label: str, current_value_substr: str):
    """Scroll to label, click the value text under it to open the list."""
    scroll_find(page, "^" + re.escape(label) + "$")
    page.wait_for_timeout(300)
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
              if (b.width>8&&b.height>8&&b.y>40&&b.y<1050)
                lab={el,x:b.x,y:b.y,w:b.width,h:b.height};
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document);
          if(!lab) return {error:'no_lab'};
          lab.el.scrollIntoView({block:'center'});
          let best=null, bestEl=null;
          const walk2=(r,d=0)=>{
            if(!r||d>50) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
              if (!t || t.length>100) continue;
              if (want && !t.includes(want) && t!==want) continue;
              // Prefer leaf: own text matches
              const own=[...el.childNodes].filter(n=>n.nodeType===3).map(n=>n.textContent.trim()).join(' ').trim();
              if (want && own && !own.includes(want) && t!==want) {
                // still allow if element is paper-item-body etc
                if (!/SPAN|YT-FORMATTED|DIV/i.test(el.tagName)) continue;
              }
              const b=el.getBoundingClientRect();
              if (b.width<15||b.height<10||b.height>60) continue;
              if (b.y < lab.y-5 || b.y > lab.y+130) continue;
              if (b.x < lab.x-40) continue;
              const score=Math.abs(b.y-(lab.y+22))*2 + (own===want||t===want?0:10) + t.length*0.02;
              if (!best||score<best.score) { best={t:t.slice(0,90),y:b.y,x:b.x,w:b.width,h:b.height,score,tag:el.tagName}; bestEl=el; }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk2(el.shadowRoot,d+1);
          }; walk2(document);
          if (!bestEl) return {error:'no_value', lab:{x:lab.x,y:lab.y}};
          bestEl.scrollIntoView({block:'center'});
          bestEl.click();
          return {ok:true, clicked:best};
        }""",
        [label, current_value_substr],
    )


def list_options(page):
    return page.evaluate(
        """()=>{
          const out=[]; const seen=new Set();
          const walk=(r,d=0)=>{
            if(!r||d>55) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('tp-yt-paper-item,[role=option]'):[])) {
              const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
              if (!t||t.length>120) continue;
              const b=el.getBoundingClientRect();
              if (b.width<30||b.height<10||b.height>90) continue;
              if (b.y<-40||b.y>1200) continue;
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


def find_listbox_scroll(page):
    """Return center of the tallest visible listbox-like scroller."""
    return page.evaluate(
        """()=>{
          let best=null;
          const walk=(r,d=0)=>{
            if(!r||d>55) return;
            for (const el of (r.querySelectorAll
              ? r.querySelectorAll('[role=listbox],tp-yt-paper-listbox,iron-dropdown,tp-yt-iron-dropdown')
              : [])) {
              const b=el.getBoundingClientRect();
              if (b.height<80||b.width<80) continue;
              if (b.y>1000||b.bottom<0) continue;
              if (!best||b.height>best.h) best={x:b.x+b.width/2,y:b.y+Math.min(b.height/2,200),h:b.height,w:b.width,tag:el.tagName};
            }
            // also large scrollable divs with many paper-items
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if (!el.shadowRoot) continue;
              // skip
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document);
          return best;
        }"""
    )


def click_exact_in_list(page, want: str):
    return page.evaluate(
        """(want)=>{
          let hit=null;
          const walk=(r,d=0)=>{
            if(!r||d>55||hit) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('tp-yt-paper-item,[role=option]'):[])) {
              const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
              if (t !== want) continue;
              el.scrollIntoView({block:'nearest'});
              const b=el.getBoundingClientRect();
              el.click();
              hit={t,y:b.y,x:b.x,w:b.width,h:b.height};
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document); return hit;
        }""",
        want,
    )


def pick_by_scroll(page, want: str, max_wheels: int = 40, direction: int = 1):
    """Scroll open listbox until exact option visible, then click. direction 1=down, -1=up."""
    seen_all = []
    seen_set = set()
    for i in range(max_wheels):
        opts = list_options(page)
        for o in opts:
            if o["t"] not in seen_set:
                seen_set.add(o["t"])
                seen_all.append({"t": o["t"], "y": o["y"]})
        if any(o["t"] == want for o in opts):
            hit = click_exact_in_list(page, want)
            return {"picked": hit, "wheels": i, "seen": seen_all}
        box = find_listbox_scroll(page)
        if box:
            page.mouse.move(box["x"], box["y"])
            page.mouse.wheel(0, 220 * direction)
        else:
            # fallback: wheel near first option
            if opts:
                page.mouse.move(opts[0]["x"] + 40, opts[0]["y"] + 40)
                page.mouse.wheel(0, 220 * direction)
            else:
                break
        page.wait_for_timeout(180)
    return {"picked": None, "wheels": max_wheels, "seen": seen_all}


def set_dd_scroll(
    page,
    label: str,
    want: str,
    open_value: str,
    prefer_up: bool = False,
):
    """Open dropdown by clicking current value, scroll to exact want, click."""
    opened = open_by_value(page, label, open_value)
    page.wait_for_timeout(1200)
    opts0 = list_options(page)
    PROBE[label + " __open"] = {
        "want": want,
        "opened": opened,
        "options": [{"t": o["t"], "y": o["y"]} for o in opts0],
    }
    dump_probe()

    if not opts0:
        # retry click
        opened = open_by_value(page, label, open_value)
        page.wait_for_timeout(1400)
        opts0 = list_options(page)
        PROBE[label + " __open2"] = {
            "want": want,
            "opened": opened,
            "options": [{"t": o["t"], "y": o["y"]} for o in opts0],
        }
        dump_probe()

    # Try exact click if already visible
    if any(o["t"] == want for o in opts0):
        hit = click_exact_in_list(page, want)
        page.wait_for_timeout(500)
        try:
            page.keyboard.press("Escape")
        except Exception:
            pass
        return {"label": label, "want": want, "opened": opened, "picked": hit, "path": "visible"}

    # Scroll preferred direction first
    directions = [-1, 1] if prefer_up else [1, -1]
    result = {"label": label, "want": want, "opened": opened}
    for d in directions:
        pick = pick_by_scroll(page, want, max_wheels=45, direction=d)
        result[f"scroll_{d}"] = {
            "picked": pick.get("picked"),
            "wheels": pick.get("wheels"),
            "seen_n": len(pick.get("seen") or []),
            "seen_sample": [x["t"] for x in (pick.get("seen") or [])[:30]],
        }
        PROBE[label] = {
            "want": want,
            "opened": opened,
            "seen": pick.get("seen") or [],
        }
        dump_probe()
        if pick.get("picked"):
            result["picked"] = pick["picked"]
            page.wait_for_timeout(500)
            try:
                page.keyboard.press("Escape")
            except Exception:
                pass
            return result
    try:
        page.keyboard.press("Escape")
    except Exception:
        pass
    result["picked"] = None
    return result


def current_select_value(page, label: str) -> str:
    sels = selects(page)
    for s in sels:
        if s.startswith(label):
            return s[len(label) :].strip()
    # fallback body scan near label
    return ""


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


def set_exam_search(page, want: str, type_text: str):
    """Exam field is a real search input."""
    scroll_find(page, r"Exam, course or standard")
    page.wait_for_timeout(300)
    # click the exam input specifically
    loc = page.evaluate(
        """()=>{
          const walk=(r,d=0)=>{
            if(!r||d>50) return null;
            for (const el of (r.querySelectorAll?r.querySelectorAll('input'):[])) {
              const aria=(el.getAttribute('aria-label')||'');
              if (!/Exam, course or standard/i.test(aria)) continue;
              el.scrollIntoView({block:'center'});
              el.click(); el.focus();
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
        return {**info, "error": "no_exam_input"}
    page.mouse.click(loc["x"], loc["y"], click_count=3)
    page.keyboard.press("Backspace")
    page.wait_for_timeout(200)
    page.keyboard.type(type_text, delay=45)
    page.wait_for_timeout(1800)
    opts = list_options(page)
    info["options"] = [{"t": o["t"], "y": o["y"]} for o in opts]
    PROBE["Exam, course or standard"] = info
    dump_probe()
    if any(o["t"] == want for o in opts):
        hit = click_exact_in_list(page, want)
        info["picked"] = hit
    else:
        # try shorter
        page.mouse.click(loc["x"], loc["y"], click_count=3)
        page.keyboard.press("Backspace")
        page.keyboard.type("GCSE", delay=45)
        page.wait_for_timeout(1800)
        opts = list_options(page)
        info["options2"] = [{"t": o["t"], "y": o["y"]} for o in opts]
        PROBE["Exam, course or standard __retry"] = {
            "want": want,
            "options": info["options2"],
        }
        dump_probe()
        if any(o["t"] == want for o in opts):
            info["picked"] = click_exact_in_list(page, want)
        else:
            info["picked"] = None
    try:
        page.keyboard.press("Escape")
    except Exception:
        pass
    return info


def main():
    global PROBE
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
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
            result["paid"] = click_radio_by_text(
                page, "No, my video doesn't include paid promotion"
            )
            result["steps"].append(save_rr(page, u, "paid_no"))
            shot(page, "fri_manual_paid.png")

            # 2 Places
            scroll_find(page, r"Allow automatic places")
            result["places"] = set_check(page, r"Allow automatic places", False)
            result["steps"].append(save_rr(page, u, "places_off"))
            shot(page, "fri_manual_places.png")

            # 3 Tags — clear corruption then set exact
            scroll_find(page, r"^Tags$")
            clear_tags(page)
            tags = fill_tags(page, FRI_TAGS)
            have = set(chips(page))
            if not set(FRI_TAGS).issubset(have) or len(have) != len(FRI_TAGS):
                clear_tags(page)
                tags = fill_tags(page, FRI_TAGS)
            result["tags"] = tags
            result["steps"].append(save_rr(page, u, "tags"))
            shot(page, "fri_manual_tags.png")

            # 4 Language — open Ukrainian value, scroll UP toward English
            lang_open = "Ukrainian"
            for s in result["before_selects"]:
                if "Title and description language" in s:
                    lang_open = s.replace("Title and description language", "").strip() or lang_open
            lang = set_dd_scroll(
                page,
                "Title and description language",
                "English (United Kingdom)",
                open_value=lang_open,
                prefer_up=True,
            )
            result["lang"] = lang
            result["steps"].append(save_rr(page, u, "lang_en_uk"))
            shot(page, "fri_manual_lang.png")

            # 5 Academic — open UAE, scroll to United Kingdom (near United*)
            acad_open = "United Arab Emirates"
            for s in selects(page):
                if s.startswith("Academic system"):
                    acad_open = s.replace("Academic system", "").strip() or acad_open
            acad = set_dd_scroll(
                page,
                "Academic system",
                "United Kingdom",
                open_value=acad_open,
                prefer_up=False,  # UAE region — UK nearby; try both dirs inside
            )
            result["academic"] = acad
            result["steps"].append(save_rr(page, u, "academic_uk"))
            shot(page, "fri_manual_academic.png")

            # 6 Type — open None
            typ = set_dd_scroll(
                page, "Type", "Concept overview", open_value="None", prefer_up=False
            )
            if not typ.get("picked"):
                # try open with empty / Select
                typ = set_dd_scroll(
                    page, "Type", "Concept overview", open_value="Type", prefer_up=False
                )
            result["type"] = typ
            result["steps"].append(save_rr(page, u, "type_concept"))
            shot(page, "fri_manual_type.png")

            # 7 Level
            lev = set_dd_scroll(
                page,
                "Level",
                "Secondary school",
                open_value="None",
                prefer_up=False,
            )
            result["level"] = lev
            result["steps"].append(save_rr(page, u, "level_secondary"))
            shot(page, "fri_manual_level.png")

            # 8 Exam search (after UK academic)
            exam = set_exam_search(page, "GCSE Chemistry", "GCSE Chemistry")
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
                "academic_uk": "Academic system United Kingdom" in fs,
                "academic_uae_bad": "United Arab Emirates" in fs,
                "type_concept": "Concept overview" in fs,
                "level_secondary": ("Secondary school" in fs)
                or bool(re.search(r"Level Secondary\\b", fs)),
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
            # fix escaped regex
            result["final"]["level_secondary"] = ("Secondary school" in fs) or bool(
                re.search(r"Level Secondary\b", fs)
            )
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
