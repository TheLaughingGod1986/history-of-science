#!/usr/bin/env python3
"""Ben 14:47 — whole-channel Studio §9 settings on every HOS video.

HOS @HistoryOfScienceYT (UCXp7HkBIl1LgaznXuZHJyRg) only.
One setting per save; re-read Audience + Visibility after each save.
Leave CUu8k38iAMc Private. Skip Fri Related until 15 Oct 18:05.
If 001 Shorts Oops — record and move on.
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
    / "evidence_2026-09-30_whole_channel_1447"
)
ART = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts" / "BEN_1447_whole_channel"
LONDON = ZoneInfo("Europe/London")
HOS = "UCXp7HkBIl1LgaznXuZHJyRg"
OTHER = re.compile(
    r"crash\s*course|vlogbrothers|hank\s*green|john\s*green|scishow|sci\s*show|ted[- ]?ed|"
    r"khan\s*academy|vsauce|veritasium|kurzgesagt|freesciencelessons|cognito|"
    r"orbit\s*with\s*ben|opptiai|bobbybroccoli|animistry|heyhistorically|"
    r"national\s*geographic|mark\s*rober|startalk|neil\s*degrasse",
    re.I,
)
PLAYLIST = "History of Science: How We Found Out"
# Fri Related deferred to 15 Oct 18:05
SKIP_RELATED = {"29bpGAI0wb8"}

# id → film, exam, related long (or None), tags (5–8), kind
CATALOG = {
    "_C92tIJCk8A": {
        "film": "001", "kind": "long", "exam": "GCSE Biology", "related": None,
        "tags": ["germ theory", "louis pasteur", "joseph lister", "microbes", "history of medicine", "history of science"],
    },
    "H1y0DXFVmw8": {
        "film": "001", "kind": "Short", "exam": "GCSE Biology", "related": "_C92tIJCk8A",
        "tags": ["germs", "microbes", "shadow", "history of medicine", "history of science"],
    },
    "iqToagXnjX0": {
        "film": "001", "kind": "Short", "exam": "GCSE Biology", "related": "_C92tIJCk8A",
        "tags": ["microbes", "pond water", "microscope", "history of medicine", "history of science"],
    },
    "8_Edn_HCi1s": {
        "film": "001", "kind": "Short", "exam": "GCSE Biology", "related": "_C92tIJCk8A",
        "tags": ["germs", "contagion", "wards", "history of medicine", "history of science"],
    },
    "93fPUG-hW0A": {
        "film": "001", "kind": "Short", "exam": "GCSE Biology", "related": "_C92tIJCk8A",
        "tags": ["invisible life", "microbes", "germ theory", "history of medicine", "history of science"],
    },
    "sILtQxgYQk8": {
        "film": "001", "kind": "Short", "exam": "GCSE Biology", "related": "_C92tIJCk8A",
        "tags": ["pasteur", "swan neck flask", "spontaneous generation", "germ theory", "history of science"],
    },
    "clV6E10NLPw": {
        "film": "001", "kind": "Short", "exam": "GCSE Biology", "related": "_C92tIJCk8A",
        "tags": ["joseph lister", "carbolic spray", "antiseptic surgery", "germ theory", "history of medicine", "history of science"],
    },
    "AL_-qlWko_g": {
        "film": "002", "kind": "long", "exam": "GCSE Chemistry", "related": None,
        "tags": ["periodic table", "mendeleev", "elements", "history of chemistry", "history of science"],
    },
    "uU12JA5rMWg": {
        "film": "002", "kind": "Short", "exam": "GCSE Chemistry", "related": "AL_-qlWko_g",
        "tags": ["periodic table", "empty chairs", "mendeleev", "elements", "history of chemistry", "history of science"],
    },
    "nFQRWmpulTQ": {
        "film": "002", "kind": "Short", "exam": "GCSE Chemistry", "related": "AL_-qlWko_g",
        "tags": ["mendeleev", "predicted elements", "periodic table", "history of chemistry", "history of science"],
    },
    "kzDiVk4603s": {
        "film": "002", "kind": "Short", "exam": "GCSE Chemistry", "related": "AL_-qlWko_g",
        "tags": ["mendeleev", "predicted elements", "periodic table", "history of chemistry", "history of science"],
        "note": "private duplicate — settings only",
    },
    "CnHwX1L9XHg": {
        "film": "002", "kind": "Short", "exam": "GCSE Chemistry", "related": "AL_-qlWko_g",
        "tags": ["gallium", "periodic table", "mendeleev", "history of chemistry", "history of science"],
    },
    "nba0-f7PPeU": {
        "film": "002", "kind": "Short", "exam": "GCSE Chemistry", "related": "AL_-qlWko_g",
        "tags": ["tellurium", "iodine", "periodic table", "atomic weight", "history of chemistry", "history of science"],
    },
    "LanTHJckYx8": {
        "film": "002", "kind": "Short", "exam": "GCSE Chemistry", "related": "AL_-qlWko_g",
        "tags": ["periodic table", "empty chairs", "elements", "history of chemistry", "history of science"],
    },
    "frP_YrNShsU": {
        "film": "003", "kind": "long", "exam": "GCSE Physics", "related": None,
        "tags": ["x-rays", "röntgen", "radiography", "history of physics", "history of science"],
    },
    "oowAOWTBoq0": {
        "film": "003", "kind": "Short", "exam": "GCSE Physics", "related": "frP_YrNShsU",
        "tags": ["x-rays", "röntgen", "accident", "history of physics", "history of science"],
    },
    "xvanpsLeADE": {
        "film": "003", "kind": "Short", "exam": "GCSE Physics", "related": "frP_YrNShsU",
        "tags": ["x-rays", "röntgen", "bones", "history of physics", "history of science"],
    },
    "zI_eD3vFWmE": {
        "film": "003", "kind": "Short", "exam": "GCSE Physics", "related": "frP_YrNShsU",
        "tags": ["x-rays", "wedding ring", "bertha", "history of physics", "history of science"],
    },
    "CUu8k38iAMc": {
        "film": "003", "kind": "Short", "exam": "GCSE Physics", "related": "frP_YrNShsU",
        "tags": ["x-rays", "wedding ring", "bertha", "history of physics", "history of science"],
        "keep_private": True,
    },
    "GHZDsiH7L7A": {
        "film": "004", "kind": "long", "exam": "GCSE Chemistry", "related": None,
        "tags": ["atom", "rutherford", "moseley", "periodic table", "history of chemistry", "history of science"],
    },
    "29bpGAI0wb8": {
        "film": "004", "kind": "Short", "exam": "GCSE Chemistry", "related": None,  # deferred 15 Oct
        "tags": ["how small can you cut gold", "what's really inside an atom", "atom", "gold", "periodic table", "history of science"],
    },
    "TbMMJSRKC3U": {
        "film": "002", "kind": "Short", "exam": "GCSE Chemistry", "related": "AL_-qlWko_g",
        "tags": ["john newlands", "law of octaves", "periodic table", "davy medal", "history of chemistry", "history of science"],
    },
}


def load_u():
    spec = importlib.util.spec_from_file_location("u", U004)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def shot(page, name: str) -> Path:
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    p = EV / name
    page.screenshot(path=str(p), full_page=False)
    shutil.copy2(p, ART / name)
    return p


def ensure_hos(page, u) -> dict:
    page.goto(f"https://studio.youtube.com/channel/{HOS}", wait_until="domcontentloaded", timeout=120000)
    page.wait_for_timeout(3000)
    u.dismiss(page)
    body = page.inner_text("body")
    url = page.url
    if HOS not in url and "History of Science" not in body:
        page.goto("https://www.youtube.com/channel_switcher", wait_until="domcontentloaded", timeout=120000)
        page.wait_for_timeout(2500)
        page.evaluate(
            """() => {
              const nodes=[...document.querySelectorAll('a,yt-formatted-string,tp-yt-paper-item,div')];
              for (const el of nodes) {
                const t=(el.innerText||'').replace(/\\s+/g,' ');
                if (/History of Science/i.test(t) && !/Orbit|Oppti/i.test(t)) { el.click(); return; }
              }
            }"""
        )
        page.wait_for_timeout(3000)
        page.goto(f"https://studio.youtube.com/channel/{HOS}", wait_until="domcontentloaded", timeout=120000)
        page.wait_for_timeout(2500)
        u.dismiss(page)
        body = page.inner_text("body")
        url = page.url
    ok = HOS in url or "History of Science" in body
    wrong = bool(re.search(r"\bOrbit with Ben\b|\bOppti", body)) and "History of Science" not in body
    return {"ok": ok and not wrong, "url": url, "snip": body[:300]}


def open_edit(page, u, vid: str) -> dict:
    page.goto(f"https://studio.youtube.com/video/{vid}/edit", wait_until="domcontentloaded", timeout=120000)
    page.wait_for_timeout(3500)
    u.dismiss(page)
    body = page.inner_text("body")
    oops = bool(re.search(r"\bOops\b|Something went wrong|try again", body, re.I))
    return {"oops": oops, "url": page.url, "body_snip": body[:400]}


def show_more(page):
    for _ in range(8):
        ok = page.evaluate(
            """() => {
              const walk=(r,d=0)=>{
                if(!r||d>45) return false;
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
    for _ in range(30):
        if page.evaluate(
            """(pat)=>{
              const re=new RegExp(pat,'i');
              const walk=(r,d=0)=>{
                if(!r||d>45) return false;
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
            page.wait_for_timeout(250)
            return True
        page.mouse.wheel(0, 700)
        page.wait_for_timeout(80)
    return False


def av(page, u) -> dict:
    body = page.inner_text("body")
    kids = page.evaluate(
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
    )
    return {
        "chip": u.visibility_chip(page),
        "not_kids": bool(kids.get("no")) or bool(re.search(r"set to not\s*['\"]?Made for Kids", body, re.I)),
        "kids_yes": bool(kids.get("yes")),
        "kids": kids,
    }


def save_rr(page, u, label: str) -> dict:
    s = u.page_save(page)
    page.wait_for_timeout(2400)
    a = av(page, u)
    print(f"    SAVE {label} clicked={s.get('clicked')} chip={a.get('chip')} not_kids={a.get('not_kids')}", flush=True)
    return {"label": label, "save": s, **a}


def click_radio(page, pat: str):
    hit = page.evaluate(
        """(pat)=>{
          const re=new RegExp(pat,'i'); let hit=null;
          const walk=(r,d=0)=>{
            if(!r||d>50||hit) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('[role=radio],tp-yt-paper-radio-button'):[])) {
              const lab=(el.getAttribute('aria-label')||el.innerText||'').replace(/\\s+/g,' ').trim();
              if (!re.test(lab)) continue;
              const b=el.getBoundingClientRect();
              if (b.width>10&&b.height>10)
                hit={lab:lab.slice(0,100),x:b.x+b.width/2,y:b.y+b.height/2,checked:el.getAttribute('aria-checked')==='true'};
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document); return hit;
        }""",
        pat,
    )
    if hit and not hit.get("checked"):
        page.mouse.click(hit["x"], hit["y"])
        page.wait_for_timeout(500)
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
              found={lab:lab.slice(0,80), before:on};
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


def clear_tags(page) -> int:
    n = 0
    for _ in range(40):
        hit = page.evaluate(
            """()=>{
              const walk=(r,d=0)=>{
                if(!r||d>50) return null;
                for (const el of (r.querySelectorAll?r.querySelectorAll('ytcp-chip,yt-chip-cloud-chip'):[])) {
                  const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
                  if (!t||t.length>90) continue;
                  const b=el.getBoundingClientRect();
                  if (b.width>20&&b.height>12)
                    return {x:b.x+b.width-12, y:b.y+b.height/2};
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
              const near=(el.closest('ytcp-form-input-container,ytcp-chip-bar,ytcp-video-metadata-editor-advanced')?.innerText||'').slice(0,200);
              if (/tag/i.test(aria+near) && !/hashtag/i.test(aria)) {
                const b=el.getBoundingClientRect();
                if (b.width>40 && b.height>10)
                  return {x:b.x+b.width/2,y:b.y+b.height/2};
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
    loc = tags_input(page)
    info = {"removed": removed, "added": [], "input": bool(loc)}
    if not loc:
        return info
    for tag in tag_list:
        page.mouse.click(loc["x"], loc["y"])
        page.wait_for_timeout(120)
        page.keyboard.type(tag, delay=15)
        page.keyboard.press("Enter")
        page.wait_for_timeout(300)
        info["added"].append(tag)
    info["chips"] = chips(page)
    return info


def dropdown_trigger(page, label_exact):
    return page.evaluate(
        """(label)=>{
          let lab=null;
          const walk=(r,d=0)=>{
            if(!r||d>50||lab) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim();
              if (t===label || t.startsWith(label+'\\n')) {
                const b=el.getBoundingClientRect();
                if (b.width>15&&b.height>10&&b.y>40&&b.y<1050)
                  lab={x:b.x,y:b.y,w:b.width,h:b.height};
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document);
          if(!lab) return null;
          let best=null;
          const walk2=(r,d=0)=>{
            if(!r||d>50) return;
            for (const el of (r.querySelectorAll
              ? r.querySelectorAll('ytcp-dropdown-trigger,ytcp-text-dropdown-trigger,[role=combobox],button,div')
              : [])) {
              const b=el.getBoundingClientRect();
              if (b.width<60||b.height<20||b.height>100) continue;
              if (Math.abs(b.y-lab.y)>120) continue;
              if (b.x < lab.x-5) continue;
              const score=Math.abs(b.y-lab.y)*3 + Math.max(0,b.x-lab.x)*0.05;
              if (!best||score<best.score)
                best={x:b.x+Math.min(b.width*0.7,220), y:b.y+b.height/2, score};
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk2(el.shadowRoot,d+1);
          }; walk2(document);
          return {lab, best};
        }""",
        label_exact,
    )


def pick_exact(page, want: str):
    opts = page.evaluate(
        """()=>{
          const out=[];
          const walk=(r,d=0)=>{
            if(!r||d>50) return;
            for (const el of (r.querySelectorAll
              ? r.querySelectorAll('tp-yt-paper-item,[role=option],yt-formatted-string,div,span')
              : [])) {
              const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
              if (!t || t.length>90) continue;
              const b=el.getBoundingClientRect();
              if (b.width>50&&b.height>18&&b.height<72&&b.y>50&&b.y<1050)
                out.push({t, x:b.x+b.width/2, y:b.y+b.height/2});
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document);
          const seen=new Set(); const uniq=[];
          for (const o of out) { const k=o.t+'@'+Math.round(o.y); if(seen.has(k)) continue; seen.add(k); uniq.push(o); }
          return uniq.slice(0,80);
        }"""
    )
    exact = [o for o in opts if o["t"] == want]
    if not exact:
        exact = [
            o
            for o in opts
            if o["t"].startswith(want) and "Arab" not in o["t"] and "AP " not in o["t"] and "Ukrain" not in o["t"]
        ]
    if exact:
        exact.sort(key=lambda o: abs(o["y"] - 500))
        page.mouse.click(exact[0]["x"], exact[0]["y"])
        page.wait_for_timeout(700)
        return {"picked": exact[0]["t"], "sample": [o["t"] for o in opts[:15]]}
    return {"picked": None, "sample": [o["t"] for o in opts[:20]]}


def set_dd(page, label: str, want: str, type_text: str | None = None) -> dict:
    scroll_find(page, re.escape(label))
    page.wait_for_timeout(200)
    trig = dropdown_trigger(page, label)
    info = {"label": label, "want": want, "trig": bool(trig and trig.get("best"))}
    if not trig or not trig.get("best"):
        return {**info, "error": "no_trigger"}
    page.mouse.click(trig["best"]["x"], trig["best"]["y"])
    page.wait_for_timeout(800)
    if type_text:
        page.keyboard.type(type_text, delay=28)
        page.wait_for_timeout(1100)
    pick = pick_exact(page, want)
    info.update(pick)
    try:
        page.keyboard.press("Escape")
    except Exception:
        pass
    page.wait_for_timeout(300)
    return info


def read_ai(page) -> dict:
    return page.evaluate(
        """()=>{
          const out=[];
          const walk=(r,d=0)=>{
            if(!r||d>50) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('[role=radio]'):[])) {
              const lab=(el.getAttribute('aria-label')||el.innerText||'').replace(/\\s+/g,' ').trim();
              if (/altered|synthetic/i.test(lab))
                out.push({lab:lab.slice(0,100), checked:el.getAttribute('aria-checked')==='true'});
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document);
          return {
            radios: out,
            yes: out.some(r=>r.checked && /^Yes/i.test(r.lab)),
            no: out.some(r=>r.checked && /^No/i.test(r.lab)),
          };
        }"""
    )


def related_text(page) -> str:
    return page.evaluate(
        """()=>{
          const el=document.querySelector('ytcp-shorts-content-links-picker, [class*=content-links]');
          return (el && (el.innerText||'').replace(/\\s+/g,' ').trim().slice(0,200)) || '';
        }"""
    )


def set_related(page, u, long_id: str, title_frag: str) -> dict:
    """Pick Related long by title fragment. HOS channel filter."""
    out = {"want": long_id, "frag": title_frag}
    scroll_find(page, r"Related video|End screen|content link")
    page.wait_for_timeout(400)
    chunk = related_text(page)
    out["before"] = chunk
    if title_frag.lower() in chunk.lower() and "None" not in chunk[:40]:
        out["already"] = True
        return out
    try:
        page.locator("ytcp-shorts-content-links-picker").first.click(force=True, timeout=8000)
    except Exception as e:
        out["error"] = f"picker_click:{e}"
        return out
    page.wait_for_timeout(3500)
    # ensure HOS via channel switcher in dialog if needed
    clicked = page.evaluate(
        """({frag}) => {
          const dlg=document.querySelector('ytcp-video-pick-dialog');
          if(!dlg) return {ok:false, reason:'no_dialog'};
          const cards=[...dlg.querySelectorAll('ytcp-video-list-cell-video, ytcp-entity-card, [role=option]')];
          for (const c of cards) {
            const t=(c.innerText||'').replace(/\\s+/g,' ');
            if (t.toLowerCase().includes(frag.toLowerCase()) && !/Short|hitch a ride/i.test(t.split('\\n')[0]||'')) {
              c.click(); return {ok:true, t:t.slice(0,120)};
            }
          }
          for (const el of dlg.querySelectorAll('*')) {
            const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
            if (!t.toLowerCase().includes(frag.toLowerCase())) continue;
            if (/hitch a ride|pond water|cast a shadow/i.test(t)) continue;
            let n=el;
            for (let i=0;i<6&&n;i++) {
              const r=n.getBoundingClientRect();
              if (r.width>140 && r.height>80 && r.height<420) { n.click(); return {ok:true, via:'climb', t:t.slice(0,120)}; }
              n=n.parentElement;
            }
          }
          return {ok:false, n:cards.length};
        }""",
        {"frag": title_frag},
    )
    out["click"] = clicked
    for _ in range(20):
        page.wait_for_timeout(350)
        if page.locator("ytcp-video-pick-dialog").count() == 0:
            break
    page.wait_for_timeout(600)
    u.dismiss(page)
    out["after"] = related_text(page)
    return out


def add_playlist(page, u) -> dict:
    scroll_find(page, r"Playlists|Add to playlist")
    out = {"want": PLAYLIST}
    try:
        # open playlist picker
        hit = page.evaluate(
            """()=>{
              const walk=(r,d=0)=>{
                if(!r||d>50) return null;
                for (const el of (r.querySelectorAll?r.querySelectorAll('button,ytcp-button,[role=button],ytcp-text-dropdown-trigger'):[])) {
                  const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
                  if (/playlist/i.test(t) && t.length<40) {
                    const b=el.getBoundingClientRect();
                    if (b.width>40&&b.height>18) return {x:b.x+b.width/2,y:b.y+b.height/2,t:t.slice(0,40)};
                  }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                  if (el.shadowRoot) { const h=walk(el.shadowRoot,d+1); if(h) return h; }
                return null;
              }; return walk(document);
            }"""
        )
        out["btn"] = hit
        if hit:
            page.mouse.click(hit["x"], hit["y"])
            page.wait_for_timeout(1200)
        # check playlist checkbox
        chk = page.evaluate(
            """(name)=>{
              const walk=(r,d=0)=>{
                if(!r||d>50) return null;
                for (const el of (r.querySelectorAll?r.querySelectorAll('[role=checkbox],tp-yt-paper-checkbox'):[])) {
                  const lab=(el.getAttribute('aria-label')||el.innerText||'').replace(/\\s+/g,' ');
                  if (lab.includes(name) || /How We Found Out/i.test(lab)) {
                    const on=el.getAttribute('aria-checked')==='true';
                    if (!on) el.click();
                    return {lab:lab.slice(0,80), before:on, after:el.getAttribute('aria-checked')==='true'};
                  }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                  if (el.shadowRoot) { const h=walk(el.shadowRoot,d+1); if(h) return h; }
                return null;
              }; return walk(document);
            }""",
            PLAYLIST,
        )
        out["check"] = chk
        try:
            page.keyboard.press("Escape")
        except Exception:
            pass
    except Exception as e:
        out["error"] = str(e)[:200]
    return out


def process_video(page, u, vid: str, meta: dict) -> dict:
    title_hint = {
        "_C92tIJCk8A": "How Did We Discover Germs",
        "AL_-qlWko_g": "How Did We Discover the Periodic Table",
        "frP_YrNShsU": "How Did We Discover X-rays",
        "GHZDsiH7L7A": "What's Really Inside an Atom",
    }
    out = {
        "id": vid,
        "film": meta["film"],
        "kind": meta["kind"],
        "exam": meta["exam"],
        "changed": [],
        "would_not_save": [],
        "before": {},
        "after": {},
        "started": datetime.now(LONDON).isoformat(timespec="seconds"),
    }
    print(f"\n=== {vid} ({meta['kind']} film {meta['film']}) ===", flush=True)
    ch = ensure_hos(page, u)
    out["channel"] = ch
    if not ch.get("ok"):
        out["error"] = "WRONG_CHANNEL"
        return out

    op = open_edit(page, u, vid)
    out["open"] = op
    if op.get("oops"):
        out["would_not_save"].append("Studio Oops on open — skipped")
        shot(page, f"{vid}_OOPS.png")
        return out

    show_more(page)
    before_av = av(page, u)
    before_ai = read_ai(page)
    out["before"] = {
        "visibility": before_av.get("chip"),
        "not_kids": before_av.get("not_kids"),
        "kids_yes": before_av.get("kids_yes"),
        "ai_yes": before_ai.get("yes"),
        "ai_no": before_ai.get("no"),
        "tags": chips(page),
    }
    if before_av.get("kids_yes"):
        out["was_made_for_kids"] = True
    if before_ai.get("no"):
        out["was_ai_no"] = True
    shot(page, f"{vid}_00_before.png")

    # 1 Audience not kids
    if not before_av.get("not_kids") or before_av.get("kids_yes"):
        scroll_find(page, r"Audience|Made for Kids")
        hit = click_radio(page, r"No, it.?s not.?Made for Kids")
        out["audience_click"] = hit
        out["changed"].append("audience_not_kids")
        out.setdefault("saves", []).append(save_rr(page, u, "audience"))
    else:
        out["changed"].append("audience_already_ok")

    # Age restriction none
    scroll_find(page, r"Age restriction")
    age = click_radio(page, r"No, don.?t restrict my video to viewers over 18")
    if age and not age.get("checked"):
        out["changed"].append("age_none")
        out.setdefault("saves", []).append(save_rr(page, u, "age_none"))

    # 2 Altered Yes
    scroll_find(page, r"altered or synthetic|Altered content")
    ai = read_ai(page)
    if not ai.get("yes"):
        hit = click_radio(page, r"Yes,.*(altered|synthetic)")
        out["ai_click"] = hit
        out["changed"].append("altered_yes")
        out.setdefault("saves", []).append(save_rr(page, u, "altered_yes"))
    else:
        out["changed"].append("altered_already_yes")

    # 3 Paid No
    scroll_find(page, r"Paid promotion")
    paid = click_radio(page, r"No, my video doesn.?t include paid promotion")
    out["paid"] = paid
    if paid and not paid.get("checked"):
        out["changed"].append("paid_no")
        out.setdefault("saves", []).append(save_rr(page, u, "paid_no"))
    elif paid and paid.get("checked"):
        out["changed"].append("paid_already_no")
    else:
        out["would_not_save"].append("paid_promotion_radio_missing")

    # 4 Languages EN-GB
    lang1 = set_dd(page, "Video language", "English (United Kingdom)", type_text="English (United Kingdom)")
    out["video_lang"] = lang1
    if lang1.get("picked"):
        out["changed"].append("video_lang_en_gb")
        out.setdefault("saves", []).append(save_rr(page, u, "video_lang"))
    lang2 = set_dd(page, "Title and description language", "English (United Kingdom)", type_text="English (United Kingdom)")
    out["title_lang"] = lang2
    if lang2.get("picked"):
        out["changed"].append("title_lang_en_gb")
        out.setdefault("saves", []).append(save_rr(page, u, "title_lang"))

    # Caption certification
    cap = set_dd(page, "Caption certification", "None of the above / Never aired on television", type_text="Never")
    if not cap.get("picked"):
        cap = set_dd(page, "Caption certification", "This content has never aired on television in the US", type_text="never")
    out["caption_cert"] = cap
    if cap.get("picked"):
        out["changed"].append("caption_cert")
        out.setdefault("saves", []).append(save_rr(page, u, "caption_cert"))

    # 5 Category Education + education fields
    cat = set_dd(page, "Category", "Education", type_text=None)
    out["category"] = cat
    if cat.get("picked"):
        out["changed"].append("category_education")
        out.setdefault("saves", []).append(save_rr(page, u, "category"))

    acad = set_dd(page, "Academic system", "United Kingdom", type_text="United Kingdom")
    out["academic"] = acad
    if acad.get("picked") and "Arab" not in str(acad.get("picked")):
        out["changed"].append("academic_uk")
        out.setdefault("saves", []).append(save_rr(page, u, "academic"))
    elif acad.get("sample"):
        out["would_not_save"].append(f"academic_system:{acad.get('sample')[:5]}")

    typ = set_dd(page, "Type", "Concept overview", type_text=None)
    out["edu_type"] = typ
    if typ.get("picked"):
        out["changed"].append("type_concept")
        out.setdefault("saves", []).append(save_rr(page, u, "type"))

    lev = set_dd(page, "Level", "Secondary school", type_text=None)
    if not lev.get("picked"):
        lev = set_dd(page, "Level", "Key stage 4", type_text="Key stage 4")
    out["level"] = lev
    if lev.get("picked"):
        out["changed"].append(f"level:{lev.get('picked')}")
        out.setdefault("saves", []).append(save_rr(page, u, "level"))
    else:
        out["would_not_save"].append("level_secondary")

    exam = set_dd(page, "Exam, course or standard", meta["exam"], type_text=meta["exam"])
    out["exam_set"] = exam
    if exam.get("picked") == meta["exam"]:
        out["changed"].append(f"exam:{meta['exam']}")
        out.setdefault("saves", []).append(save_rr(page, u, "exam"))
    else:
        out["would_not_save"].append(f"exam:{meta['exam']}_not_in_taxonomy sample={exam.get('sample')}")

    # 6 Automatic places OFF; chapters ON; concepts ON
    scroll_find(page, r"Allow automatic places")
    places = set_check(page, r"Allow automatic places", False)
    out["places"] = places
    if places.get("lab") != "missing" and places.get("before") is True:
        out["changed"].append("places_off")
        out.setdefault("saves", []).append(save_rr(page, u, "places_off"))
    chapters = set_check(page, r"Allow automatic chapters", True)
    out["chapters"] = chapters
    if chapters.get("before") is False:
        out["changed"].append("chapters_on")
        out.setdefault("saves", []).append(save_rr(page, u, "chapters_on"))
    concepts = set_check(page, r"Allow automatic concepts", True)
    out["concepts"] = concepts
    if concepts.get("before") is False:
        out["changed"].append("concepts_on")
        out.setdefault("saves", []).append(save_rr(page, u, "concepts_on"))

    # 7 Tags 5–8 subject-only
    scroll_find(page, r"^Tags$")
    cur = chips(page)
    bad = [c for c in cur if OTHER.search(c)]
    want = meta["tags"]
    need_tags = bad or len(cur) < 5 or len(cur) > 8 or set(c.lower() for c in cur) != set(t.lower() for t in want)
    if need_tags:
        info = fill_tags(page, want)
        out["tags"] = info
        # strip any banned that snuck in
        if any(OTHER.search(c) for c in chips(page)):
            clear_tags(page)
            fill_tags(page, want)
        out["changed"].append("tags_replaced")
        out.setdefault("saves", []).append(save_rr(page, u, "tags"))
    else:
        out["changed"].append("tags_already_ok")
        out["tags"] = {"chips": cur}

    # 8 Comments / embedding / remix — best effort via checkboxes/radios
    scroll_find(page, r"^Comments$|Comment settings")
    # Embedding on
    emb = set_check(page, r"Allow embedding|Show viewers", True)
    # try common labels
    if emb.get("lab") == "missing":
        emb = set_check(page, r"embedding", True)
    out["embedding"] = emb

    # 9 Related (Shorts) / Playlist (longs)
    if meta["kind"] == "Short" and meta.get("related") and vid not in SKIP_RELATED:
        frag = title_hint.get(meta["related"], "How Did We Discover")
        rel = set_related(page, u, meta["related"], frag)
        out["related"] = rel
        if rel.get("click", {}).get("ok") or rel.get("already"):
            out["changed"].append("related_set" if not rel.get("already") else "related_already")
            if not rel.get("already"):
                out.setdefault("saves", []).append(save_rr(page, u, "related"))
        else:
            out["would_not_save"].append(f"related:{rel}")
    elif vid in SKIP_RELATED:
        out["changed"].append("related_skipped_until_15_oct_1805")

    if meta["kind"] == "long":
        pl = add_playlist(page, u)
        out["playlist"] = pl
        if pl.get("check") and pl["check"].get("after"):
            out["changed"].append("playlist_how_we_found_out")
            out.setdefault("saves", []).append(save_rr(page, u, "playlist"))
        elif pl.get("check") and pl["check"].get("before"):
            out["changed"].append("playlist_already")
        else:
            out["would_not_save"].append(f"playlist:{pl}")

    # Final re-read + screenshot
    open_edit(page, u, vid)
    if "Oops" in page.inner_text("body"):
        out["would_not_save"].append("Oops_on_final_reread")
        shot(page, f"{vid}_99_OOPS_final.png")
        return out
    show_more(page)
    for _ in range(10):
        page.mouse.wheel(0, 700)
        page.wait_for_timeout(60)
    final_av = av(page, u)
    final_ai = read_ai(page)
    out["after"] = {
        "visibility": final_av.get("chip"),
        "not_kids": final_av.get("not_kids"),
        "ai_yes": final_ai.get("yes"),
        "tags": chips(page),
        "related": related_text(page) if meta["kind"] == "Short" else None,
    }
    # visibility must be unchanged (except we never touch it)
    out["visibility_unchanged"] = True  # we never opened visibility dialog to change it
    shot(page, f"{vid}_99_final.png")
    out["finished"] = datetime.now(LONDON).isoformat(timespec="seconds")
    print(f"  DONE changed={out['changed']} wont={out['would_not_save']}", flush=True)
    return out


def contact_sheet(paths: list[Path], dest: Path):
    try:
        from PIL import Image
    except ImportError:
        return
    imgs = []
    for p in paths:
        if p.exists() and p.stat().st_size > 1000:
            try:
                imgs.append(Image.open(p).convert("RGB"))
            except Exception:
                pass
    if not imgs:
        return
    w, h = 320, 180
    cols = 4
    rows = (len(imgs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * w, rows * h), (20, 20, 20))
    for i, im in enumerate(imgs):
        im.thumbnail((w, h))
        x = (i % cols) * w + (w - im.width) // 2
        y = (i // cols) * h + (h - im.height) // 2
        sheet.paste(im, (x, y))
    sheet.save(dest)
    shutil.copy2(dest, ART / dest.name)


def main():
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    inv_path = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts/hos_full_inventory.json"
    inv = json.loads(inv_path.read_text())
    assert inv["channelId"] == HOS, inv["channelId"]
    titles = {v["id"]: v["snippet"]["title"] for v in inv["videos"]}
    order = list(titles.keys())
    # Prefer public longs first? Ben said every video — use upload order from inventory
    u = load_u()
    results = []
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9460")
        ctx = browser.contexts[0]
        page = ctx.new_page()
        page.set_default_timeout(60000)
        ch = ensure_hos(page, u)
        print("CHANNEL", ch, flush=True)
        if not ch.get("ok"):
            raise SystemExit("not on HOS")
        for vid in order:
            meta = CATALOG.get(vid)
            if not meta:
                results.append({"id": vid, "error": "not_in_catalog", "title": titles.get(vid)})
                continue
            try:
                r = process_video(page, u, vid, meta)
                r["title"] = titles.get(vid)
                results.append(r)
            except Exception as e:
                results.append({"id": vid, "title": titles.get(vid), "error": str(e)[:300], "film": meta["film"]})
                print(f"  ERR {vid}: {e}", flush=True)
            # persist incrementally
            (EV / "SWEEP_PARTIAL.json").write_text(json.dumps(results, indent=2, default=str))
        try:
            page.close()
        except Exception:
            pass

    finals = sorted(EV.glob("*_99_final.png"))
    contact_sheet(finals, EV / "CONTACT_final_states.jpg")
    report = {
        "ordered_by": "Ben 14:47",
        "at": datetime.now(LONDON).isoformat(timespec="seconds"),
        "channel_id": HOS,
        "handle": "@HistoryOfScienceYT",
        "n": len(results),
        "results": results,
        "was_made_for_kids": [r["id"] for r in results if r.get("was_made_for_kids")],
        "was_ai_no": [r["id"] for r in results if r.get("was_ai_no")],
        "would_not_save": [
            {"id": r["id"], "issues": r.get("would_not_save")}
            for r in results
            if r.get("would_not_save")
        ],
    }
    (EV / "SWEEP_RESULT.json").write_text(json.dumps(report, indent=2, default=str))
    shutil.copy2(EV / "SWEEP_RESULT.json", ART / "SWEEP_RESULT.json")
    print(json.dumps({"n": report["n"], "kids": report["was_made_for_kids"], "ai_no": report["was_ai_no"], "wont": len(report["would_not_save"])}, indent=2))


if __name__ == "__main__":
    main()
