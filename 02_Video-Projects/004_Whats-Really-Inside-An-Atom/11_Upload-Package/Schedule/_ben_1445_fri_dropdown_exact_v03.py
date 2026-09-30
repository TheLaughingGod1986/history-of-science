#!/usr/bin/env python3
"""Fri 29bpGAI0wb8 Studio dropdown exact-match fix.

Connect Chrome CDP :9460. Stay on @HistoryOfScienceYT only.
Never open CUu8k38iAMc. One setting per Save. Exact option text only.
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
BANNED = {"CUu8k38iAMc"}
TITLE = "What happens if you keep cutting gold in half?"
FRI_TAGS = [
    "how small can you cut gold",
    "what's really inside an atom",
    "atom",
    "gold",
    "periodic table",
    "history of science",
]
PROBE_PATH = EV / "DROPDOWN_PROBE.json"


def load_u():
    spec = importlib.util.spec_from_file_location("u", U004)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def shot(page, name: str):
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    p = EV / name
    page.screenshot(path=str(p), full_page=False)
    shutil.copy2(p, ART / f"BEN_1445FIX_{name}")
    return str(p)


def open_edit(page, u):
    assert VID not in BANNED
    page.goto(
        f"https://studio.youtube.com/video/{VID}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3500)
    u.dismiss(page)
    # Channel sanity: never on Orbit / banned id
    url = page.url
    assert VID in url
    assert "CUu8k38iAMc" not in url


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
        page.wait_for_timeout(500)


def scroll_find(page, pat: str) -> bool:
    for _ in range(32):
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
            page.wait_for_timeout(350)
            return True
        page.mouse.wheel(0, 700)
        page.wait_for_timeout(100)
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
                for (const el of (r.querySelectorAll?r.querySelectorAll('[role=radio]'):[])) {
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


def save_rr(page, u, label: str):
    s = u.page_save(page)
    page.wait_for_timeout(2500)
    a = av(page, u)
    print(
        f"  SAVE {label} clicked={s.get('clicked')} chip={a.get('chip')} not_kids={a.get('not_kids')}",
        flush=True,
    )
    return {"label": label, "save": s, **a}


def click_radio_exact(page, exact_lab: str):
    hit = page.evaluate(
        """(want)=>{
          let hit=null;
          const walk=(r,d=0)=>{
            if(!r||d>50||hit) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('[role=radio],tp-yt-paper-radio-button'):[])) {
              const lab=(el.getAttribute('aria-label')||el.innerText||'').replace(/\\s+/g,' ').trim();
              if (lab !== want && !(lab.includes(want))) continue;
              // Prefer exact aria-label match
              const b=el.getBoundingClientRect();
              if (b.width>10&&b.height>10)
                hit={lab, x:b.x+b.width/2, y:b.y+b.height/2,
                     checked:el.getAttribute('aria-checked')==='true',
                     exact: lab===want};
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document); return hit;
        }""",
        exact_lab,
    )
    if hit:
        page.mouse.click(hit["x"], hit["y"])
        page.wait_for_timeout(600)
        # re-read checked
        hit2 = page.evaluate(
            """(want)=>{
              let hit=null;
              const walk=(r,d=0)=>{
                if(!r||d>50||hit) return;
                for (const el of (r.querySelectorAll?r.querySelectorAll('[role=radio],tp-yt-paper-radio-button'):[])) {
                  const lab=(el.getAttribute('aria-label')||el.innerText||'').replace(/\\s+/g,' ').trim();
                  if (!lab.includes(want.slice(0,20))) continue;
                  hit={lab, checked:el.getAttribute('aria-checked')==='true'};
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                  if (el.shadowRoot) walk(el.shadowRoot,d+1);
              }; walk(document); return hit;
            }""",
            exact_lab,
        )
        hit["after"] = hit2
    return hit


def set_check(page, pat: str, want: bool):
    return page.evaluate(
        """(args)=>{
          const re=new RegExp(args[0],'i'), want=args[1];
          let found=null;
          const walk=(r,d=0)=>{
            if(!r||d>50||found) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('[role=checkbox],tp-yt-paper-checkbox'):[])) {
              const lab=(el.getAttribute('aria-label')||'').trim();
              if (!re.test(lab)) continue;
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
                  const b=el.getBoundingClientRect();
                  if (b.width>20&&b.height>12)
                    return {x:b.x+b.width-12, y:b.y+b.height/2, t:t.slice(0,50)};
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                  if (el.shadowRoot) { const h=walk(el.shadowRoot,d+1); if(h) return h; }
                return null;
              }; return walk(document);
            }"""
        )
        if not hit:
            break
        page.mouse.click(hit["x"], hit["y"])
        page.wait_for_timeout(200)
        n += 1
    return n


def tags_input(page):
    return page.evaluate(
        """()=>{
          const walk=(r,d=0)=>{
            if(!r||d>50) return null;
            for (const el of (r.querySelectorAll?r.querySelectorAll('input,textarea'):[])) {
              if (el.type==='file' || el.type==='hidden' || el.type==='checkbox' || el.type==='radio') continue;
              const aria=(el.getAttribute('aria-label')||'')+(el.getAttribute('placeholder')||'');
              if (/tag/i.test(aria) && !/hashtag/i.test(aria)) {
                const b=el.getBoundingClientRect();
                if (b.width>40 && b.height>10)
                  return {x:b.x+b.width/2,y:b.y+b.height/2,aria:aria.slice(0,80)};
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) { const h=walk(el.shadowRoot,d+1); if(h) return h; }
            return null;
          }; return walk(document);
        }"""
    )


def fill_tags(page, tag_list):
    scroll_find(page, r"^Tags$")
    removed = clear_tags(page)
    info = {"removed": removed, "added": []}
    loc = tags_input(page)
    info["input"] = loc
    if not loc:
        return info
    for tag in tag_list:
        page.mouse.click(loc["x"], loc["y"])
        page.wait_for_timeout(120)
        page.keyboard.press("Meta+a")
        page.keyboard.type(tag, delay=20)
        page.keyboard.press("Enter")
        page.wait_for_timeout(400)
        info["added"].append(tag)
    info["chips"] = chips(page)
    return info


def finds_label(page, label: str):
    """Find exact label node and nearby dropdown trigger."""
    return page.evaluate(
        """(label)=>{
          let labs=[];
          const walk=(r,d=0)=>{
            if(!r||d>50) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              // leaf-ish label: own text equals label (ignore deep children text)
              const own=[...el.childNodes].filter(n=>n.nodeType===3).map(n=>n.textContent.trim()).join(' ').trim();
              const t=(el.innerText||'').trim();
              const match = (own===label) || (t===label);
              if (!match) continue;
              const b=el.getBoundingClientRect();
              if (b.width>10&&b.height>8&&b.y>40&&b.y<1100)
                labs.push({x:b.x,y:b.y,w:b.width,h:b.height,t:t.slice(0,60),own:own.slice(0,60),tag:el.tagName});
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document);
          // prefer smallest / most leaf-like
          labs.sort((a,b)=> (a.w*a.h)-(b.w*b.h));
          if (!labs.length) return null;
          const lab=labs[0];
          let best=null;
          const walk2=(r,d=0)=>{
            if(!r||d>50) return;
            const sels='ytcp-dropdown-trigger,ytcp-text-dropdown-trigger,[role=combobox],tp-yt-paper-dropdown-menu';
            for (const el of (r.querySelectorAll?r.querySelectorAll(sels+',button'):[])) {
              const b=el.getBoundingClientRect();
              const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
              if (b.width<40||b.height<18||b.height>120) continue;
              if (Math.abs(b.y-lab.y)>140) continue;
              if (b.x < lab.x-20) continue;
              // prefer elements whose text contains label or sits just below/right
              const dy=Math.abs(b.y-lab.y);
              const score = dy*4 + Math.max(0,b.x-lab.x)*0.02 + (t.includes(label)?0:15);
              if (!best||score<best.score)
                best={x:b.x+Math.min(b.width*0.55,180), y:b.y+b.height/2,
                      t:t.slice(0,90), score, w:b.width, h:b.height, bx:b.x, by:b.y};
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk2(el.shadowRoot,d+1);
          }; walk2(document);
          return {lab, best, n_labs:labs.length};
        }""",
        label,
    )


def dump_listbox_options(page):
    """Dump ONLY options inside open listbox/menu/dropdown panels."""
    return page.evaluate(
        """()=>{
          const out=[];
          const seen=new Set();
          const push=(el,src)=>{
            const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
            if (!t || t.length>120) return;
            const b=el.getBoundingClientRect();
            if (b.width<30||b.height<14||b.height>80) return;
            if (b.y<0||b.y>1400) return;
            const k=t+'@'+Math.round(b.y)+'@'+Math.round(b.x);
            if (seen.has(k)) return;
            seen.add(k);
            out.push({t, y:b.y, x:b.x, w:b.width, h:b.height, src,
                      aria:(el.getAttribute('aria-label')||'').slice(0,80),
                      role:el.getAttribute('role')||''});
          };
          // Prefer panels that look like open dropdowns
          const panels=[];
          const walkP=(r,d=0)=>{
            if(!r||d>55) return;
            for (const el of (r.querySelectorAll
              ? r.querySelectorAll('[role=listbox],tp-yt-paper-listbox,ytcp-text-menu,iron-dropdown,tp-yt-iron-dropdown,.ytcp-menu-popup,ytcp-ve')
              : [])) {
              const b=el.getBoundingClientRect();
              const style=getComputedStyle(el);
              if (b.height>40 && b.width>80 && style.visibility!=='hidden' && style.display!=='none')
                panels.push(el);
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walkP(el.shadowRoot,d+1);
          }; walkP(document);

          const collectFrom=(root,src)=>{
            const walk=(r,d=0)=>{
              if(!r||d>40) return;
              for (const el of (r.querySelectorAll
                ? r.querySelectorAll('tp-yt-paper-item,[role=option],ytcp-ve[role=option],yt-formatted-string')
                : [])) {
                // Prefer leaf option rows
                const role=el.getAttribute('role')||'';
                const tag=el.tagName.toLowerCase();
                if (tag==='yt-formatted-string' && role!=='option') {
                  // only if parent looks like paper-item
                  const p=el.parentElement;
                  if (!p || !/ITEM|OPTION|MENU/i.test(p.tagName+' '+(p.getAttribute('role')||'')))
                    continue;
                }
                push(el, src);
              }
              for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                if (el.shadowRoot) walk(el.shadowRoot,d+1);
            }; walk(root);
          };

          if (panels.length) {
            panels.forEach((p,i)=>collectFrom(p, 'panel'+i));
          }
          // Also scan role=option globally (sometimes outside panels we found)
          const walkG=(r,d=0)=>{
            if(!r||d>55) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('[role=option],tp-yt-paper-item'):[])) {
              push(el, 'global');
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walkG(el.shadowRoot,d+1);
          }; walkG(document);

          out.sort((a,b)=>a.y-b.y || a.x-b.x);
          return {n_panels:panels.length, options:out};
        }"""
    )


def find_search_input(page):
    """Find visible text input inside an open dropdown (searchable menus)."""
    return page.evaluate(
        """()=>{
          let hit=null;
          const walk=(r,d=0)=>{
            if(!r||d>55||hit) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('input'):[])) {
              if (el.type==='file'||el.type==='hidden'||el.type==='checkbox'||el.type==='radio') continue;
              const b=el.getBoundingClientRect();
              if (b.width<40||b.height<10||b.y<0||b.y>1200) continue;
              // Prefer inputs near top of viewport that appeared with dropdown
              const aria=(el.getAttribute('aria-label')||'')+(el.getAttribute('placeholder')||'');
              if (/search|filter|type|language|exam|system|country/i.test(aria) || b.y>80) {
                hit={x:b.x+b.width/2,y:b.y+b.height/2,aria:aria.slice(0,80),ph:(el.getAttribute('placeholder')||'').slice(0,60)};
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document); return hit;
        }"""
    )


def click_exact_option(page, want: str, forbid_substrings=None):
    """Click ONLY option whose innerText EXACTLY equals want."""
    forbid_substrings = forbid_substrings or []
    dump = dump_listbox_options(page)
    opts = dump.get("options") or []
    exact = [o for o in opts if o["t"] == want]
    # Reject forbidden
    exact = [
        o
        for o in exact
        if not any(f.lower() in o["t"].lower() for f in forbid_substrings if f.lower() not in want.lower())
    ]
    info = {
        "want": want,
        "n_opts": len(opts),
        "all_texts": [{"t": o["t"], "y": o["y"], "x": o["x"], "src": o.get("src")} for o in opts],
        "exact_matches": exact,
    }
    if not exact:
        return {**info, "picked": None, "dump": dump}
    # Prefer mid-panel option (dropdown list, not page chrome)
    exact.sort(key=lambda o: (0 if o.get("src", "").startswith("panel") else 1, abs(o["y"] - 420)))
    pick = exact[0]
    page.mouse.click(pick["x"] + pick["w"] / 2, pick["y"] + pick["h"] / 2)
    page.wait_for_timeout(800)
    return {**info, "picked": pick, "dump": dump}


def set_dd_exact(
    page,
    label: str,
    want: str,
    type_text: str | None = None,
    forbid=None,
    probe_bucket: dict | None = None,
):
    forbid = forbid or []
    scroll_find(page, re.escape(label))
    page.wait_for_timeout(300)
    trig = finds_label(page, label)
    info = {"label": label, "want": want, "trig": trig}
    if not trig or not trig.get("best"):
        info["error"] = "no_trigger"
        return info
    page.mouse.click(trig["best"]["x"], trig["best"]["y"])
    page.wait_for_timeout(1000)

    if type_text:
        si = find_search_input(page)
        info["search_input"] = si
        if si:
            page.mouse.click(si["x"], si["y"])
            page.wait_for_timeout(200)
            page.keyboard.press("Meta+a")
            page.keyboard.press("Backspace")
            page.wait_for_timeout(150)
            page.keyboard.type(type_text, delay=35)
            page.wait_for_timeout(1400)
        else:
            # type into focused dropdown
            page.keyboard.type(type_text, delay=35)
            page.wait_for_timeout(1400)

    # Dump probe BEFORE click
    dump = dump_listbox_options(page)
    if probe_bucket is not None:
        probe_bucket[label] = {
            "want": want,
            "typed": type_text,
            "trig": trig,
            "n_panels": dump.get("n_panels"),
            "options": [{"t": o["t"], "y": o["y"], "x": o["x"], "src": o.get("src")} for o in dump.get("options", [])],
        }
        PROBE_PATH.write_text(json.dumps(probe_bucket, indent=2))

    pick = click_exact_option(page, want, forbid_substrings=forbid)
    info["pick"] = {k: pick[k] for k in pick if k != "dump"}
    info["n_panels"] = dump.get("n_panels")

    if not pick.get("picked"):
        # Retry: clear type, type shorter distinctive string
        if type_text:
            page.keyboard.press("Meta+a")
            page.keyboard.press("Backspace")
            page.wait_for_timeout(200)
            # For UK language use more unique phrase
            alt = type_text
            if "United Kingdom" in want and "English" in want:
                alt = "English (United Kingdom)"
            elif want == "United Kingdom":
                # Type full exact — UAE also contains United but not "Kingdom" alone as full text
                alt = "United Kingdom"
            page.keyboard.type(alt, delay=40)
            page.wait_for_timeout(1500)
            dump2 = dump_listbox_options(page)
            if probe_bucket is not None:
                probe_bucket[label + " __retry"] = {
                    "want": want,
                    "typed": alt,
                    "n_panels": dump2.get("n_panels"),
                    "options": [
                        {"t": o["t"], "y": o["y"], "x": o["x"], "src": o.get("src")}
                        for o in dump2.get("options", [])
                    ],
                }
                PROBE_PATH.write_text(json.dumps(probe_bucket, indent=2))
            pick2 = click_exact_option(page, want, forbid_substrings=forbid)
            info["pick2"] = {k: pick2[k] for k in pick2 if k != "dump"}

    # Escape leftover open menus
    try:
        page.keyboard.press("Escape")
    except Exception:
        pass
    page.wait_for_timeout(400)
    return info


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
            for (const el of (r.querySelectorAll?r.querySelectorAll('[role=radio],tp-yt-paper-radio-button'):[])) {
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
    u = load_u()
    probe: dict = {"video": VID, "started": datetime.now(LONDON).isoformat(timespec="seconds")}
    result = {
        "video": VID,
        "channel": "@HistoryOfScienceYT",
        "started": datetime.now(LONDON).isoformat(timespec="seconds"),
        "steps": [],
    }

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9460")
        ctx = browser.contexts[0]
        page = ctx.new_page()
        page.set_viewport_size({"width": 1400, "height": 900})
        try:
            open_edit(page, u)
            show_more(page)
            result["before_selects"] = selects(page)
            result["before_tags"] = chips(page)
            result["before_av"] = av(page, u)
            shot(page, "fri_manual_00_before.png")

            # --- Paid promotion ---
            scroll_find(page, r"Paid promotion")
            paid = click_radio_exact(
                page, "No, my video doesn't include paid promotion"
            )
            result["paid"] = paid
            result["steps"].append(save_rr(page, u, "paid_no"))
            shot(page, "fri_manual_paid.png")

            # --- Places off ---
            scroll_find(page, r"Allow automatic places")
            places = set_check(page, r"Allow automatic places", False)
            result["places"] = places
            result["steps"].append(save_rr(page, u, "places_off"))
            shot(page, "fri_manual_places.png")

            # --- Tags ---
            tags = fill_tags(page, FRI_TAGS)
            # if incomplete, retry once
            have = set(chips(page))
            missing = [t for t in FRI_TAGS if t not in have]
            if missing:
                tags2 = fill_tags(page, FRI_TAGS)
                tags["retry"] = tags2
            result["tags"] = tags
            result["steps"].append(save_rr(page, u, "tags"))
            shot(page, "fri_manual_tags.png")

            # --- Language: English (United Kingdom) NOT Ukrainian ---
            lang = set_dd_exact(
                page,
                "Title and description language",
                "English (United Kingdom)",
                type_text="English (United Kingdom)",
                forbid=["Ukrainian", "United Arab"],
                probe_bucket=probe,
            )
            result["lang"] = lang
            result["steps"].append(save_rr(page, u, "lang_en_uk"))
            shot(page, "fri_manual_lang.png")
            sel = selects(page)
            if not any(
                "Title and description language English (United Kingdom)" in s for s in sel
            ):
                lang2 = set_dd_exact(
                    page,
                    "Title and description language",
                    "English (United Kingdom)",
                    type_text="United Kingdom)",
                    forbid=["Ukrainian"],
                    probe_bucket=probe,
                )
                result["lang_retry"] = lang2
                result["steps"].append(save_rr(page, u, "lang_en_uk_retry"))
                shot(page, "fri_manual_lang_retry.png")

            # --- Academic system: United Kingdom NOT UAE ---
            acad = set_dd_exact(
                page,
                "Academic system",
                "United Kingdom",
                type_text="United Kingdom",
                forbid=["United Arab Emirates", "Arab"],
                probe_bucket=probe,
            )
            result["academic"] = acad
            result["steps"].append(save_rr(page, u, "academic_uk"))
            shot(page, "fri_manual_academic.png")
            sel = selects(page)
            if any("United Arab Emirates" in s for s in sel) or not any(
                "Academic system United Kingdom" in s for s in sel
            ):
                # reopen and pick carefully — type "Kingdom" alone may help filter UAE
                acad2 = set_dd_exact(
                    page,
                    "Academic system",
                    "United Kingdom",
                    type_text="Kingdom",
                    forbid=["Arab", "Emirates"],
                    probe_bucket=probe,
                )
                result["academic_retry"] = acad2
                result["steps"].append(save_rr(page, u, "academic_uk_retry"))
                shot(page, "fri_manual_academic_retry.png")

            # --- Type ---
            typ = set_dd_exact(
                page,
                "Type",
                "Concept overview",
                type_text=None,
                probe_bucket=probe,
            )
            result["type"] = typ
            result["steps"].append(save_rr(page, u, "type_concept"))
            shot(page, "fri_manual_type.png")

            # --- Level ---
            lev = set_dd_exact(
                page,
                "Level",
                "Secondary school",
                type_text=None,
                probe_bucket=probe,
            )
            if not (lev.get("pick") or {}).get("picked"):
                lev = set_dd_exact(
                    page,
                    "Level",
                    "Secondary",
                    type_text="Secondary",
                    probe_bucket=probe,
                )
            result["level"] = lev
            result["steps"].append(save_rr(page, u, "level_secondary"))
            shot(page, "fri_manual_level.png")

            # --- Exam: GCSE Chemistry NOT AP Chemistry ---
            exam = set_dd_exact(
                page,
                "Exam, course or standard",
                "GCSE Chemistry",
                type_text="GCSE Chemistry",
                forbid=["AP Chemistry", "AP "],
                probe_bucket=probe,
            )
            result["exam"] = exam
            result["steps"].append(save_rr(page, u, "exam_gcse"))
            shot(page, "fri_manual_exam.png")
            body = page.inner_text("body")
            if "GCSE Chemistry" not in body or "AP Chemistry" in "".join(selects(page)):
                exam2 = set_dd_exact(
                    page,
                    "Exam, course or standard",
                    "GCSE Chemistry",
                    type_text="GCSE",
                    forbid=["AP "],
                    probe_bucket=probe,
                )
                result["exam_retry"] = exam2
                result["steps"].append(save_rr(page, u, "exam_gcse_retry"))
                shot(page, "fri_manual_exam_retry.png")

            # Final read
            open_edit(page, u)
            show_more(page)
            page.mouse.wheel(0, 2000)
            page.wait_for_timeout(800)
            result["final_selects"] = selects(page)
            result["final_tags"] = chips(page)
            result["final_av"] = av(page, u)
            result["final_paid"] = paid_state(page)
            scroll_find(page, r"Allow automatic places")
            result["final_places"] = set_check(page, r"Allow automatic places", False)
            # re-check without flipping if already false — set_check may have toggled; undo if needed
            # Actually set_check with want=False leaves it false; OK
            shot(page, "fri_manual_99_final.png")
            scroll_find(page, r"Education|Academic system|Title and description")
            shot(page, "fri_manual_99_education.png")

            fs = " | ".join(result["final_selects"])
            ft = result["final_tags"]
            paid_ok = any(
                "doesn't include paid" in (p.get("lab") or "").lower() and p.get("checked")
                for p in result.get("final_paid") or []
            )
            places_off = result.get("final_places", {}).get("after") is False or (
                result.get("final_places", {}).get("before") is False
                and result.get("final_places", {}).get("after") is False
            )
            # places: after should be False
            places_ok = result.get("final_places", {}).get("after") is False

            result["final"] = {
                "lang_uk": "Title and description language English (United Kingdom)" in fs,
                "lang_ukrainian_bad": "Ukrainian" in fs,
                "academic_uk": "Academic system United Kingdom" in fs,
                "academic_uae_bad": "United Arab Emirates" in fs,
                "type_concept": "Concept overview" in fs,
                "level_secondary": ("Secondary school" in fs) or ("Level Secondary" in fs),
                "exam_gcse": "GCSE Chemistry" in fs,
                "exam_ap_bad": "AP Chemistry" in fs,
                "tags": ft,
                "tags_ok": set(FRI_TAGS).issubset(set(ft)) and len(ft) == len(FRI_TAGS),
                "paid_no": paid_ok,
                "places_off": places_ok,
                "audience_not_kids": result["final_av"].get("not_kids"),
                "visibility_scheduled": "Scheduled" in str(result["final_av"].get("chip") or ""),
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
            PROBE_PATH.write_text(json.dumps(probe, indent=2))
            out_path = EV / "FRI_MANUAL_RESULT.json"
            out_path.write_text(json.dumps(result, indent=2))
            shutil.copy2(out_path, ART / "BEN_1445FIX_FRI_MANUAL_RESULT.json")
            shutil.copy2(PROBE_PATH, ART / "BEN_1445FIX_DROPDOWN_PROBE.json")
            print(json.dumps(result["final"], indent=2))
            print("OK=", result["ok"])
        finally:
            page.close()


if __name__ == "__main__":
    main()
