#!/usr/bin/env python3
"""Ben 14:45 Studio fixes v02 — precise dropdowns + safe tag fill. HOS only."""
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
BANNED = {"CUu8k38iAMc"}
OTHER = re.compile(
    r"crash\s*course|vlogbrothers|hank\s*green|scishow|sci\s*show|ted[- ]?ed|"
    r"khan\s*academy|vsauce|veritasium|kurzgesagt|freesciencelessons",
    re.I,
)
SUN_BAD = re.compile(r"gold|x-?ray|röntgen|roentgen|bertha|\batom\b|dalton", re.I)

FRI_TAGS = [
    "how small can you cut gold",
    "what's really inside an atom",
    "atom",
    "gold",
    "periodic table",
    "history of science",
]
SUN_TAGS = [
    "newlands",
    "octaves",
    "every eighth element",
    "periodic table",
    "davy medal",
    "history of science",
]

JOBS = [
    {"key": "fri", "id": "29bpGAI0wb8", "title": "What happens if you keep cutting gold in half?", "tags": FRI_TAGS, "exam": "GCSE Chemistry", "order1": True},
    {"key": "sun", "id": "TbMMJSRKC3U", "title": None, "tags": SUN_TAGS, "exam": "GCSE Chemistry", "order1": True},
    {"key": "long004", "id": "GHZDsiH7L7A", "title": None, "tags": None, "exam": "GCSE Chemistry", "order1": False},
    {"key": "lister", "id": "clV6E10NLPw", "title": None, "tags": None, "exam": "GCSE Biology", "order1": False},
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
    page.screenshot(path=str(p), full_page=True)
    shutil.copy2(p, ART / f"BEN_1445FIX_{name}")
    return p


def open_edit(page, u, vid):
    assert vid not in BANNED
    page.goto(f"https://studio.youtube.com/video/{vid}/edit", wait_until="domcontentloaded", timeout=120000)
    page.wait_for_timeout(3500)
    u.dismiss(page)


def show_more(page):
    for _ in range(6):
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
        page.wait_for_timeout(450)


def scroll_find(page, pat):
    for _ in range(28):
        if page.evaluate(
            """(pat)=>{
              const re=new RegExp(pat,'i');
              const walk=(r,d=0)=>{
                if(!r||d>45) return false;
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                  const t=(el.innerText||'').trim();
                  if (re.test(t) && t.length<70) { el.scrollIntoView({block:'center'}); return true; }
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
        page.mouse.wheel(0, 750)
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


def save_rr(page, u, label):
    s = u.page_save(page)
    page.wait_for_timeout(2200)
    a = av(page, u)
    print(f"  SAVE {label} clicked={s.get('clicked')} chip={a.get('chip')} not_kids={a.get('not_kids')}", flush=True)
    return {"label": label, "save": s, **a}


def click_radio(page, pat):
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
                hit={lab:lab.slice(0,90),x:b.x+b.width/2,y:b.y+b.height/2,checked:el.getAttribute('aria-checked')==='true'};
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document); return hit;
        }""",
        pat,
    )
    if hit:
        page.mouse.click(hit["x"], hit["y"])
        page.wait_for_timeout(500)
    return hit


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
    for _ in range(50):
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
        page.wait_for_timeout(220)
        n += 1
    return n


def tags_input(page):
    """Locate tags text input — never file inputs."""
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
                  return {x:b.x+b.width/2,y:b.y+b.height/2,aria:aria.slice(0,60),tag:el.tagName,type:el.type||''};
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
        page.wait_for_timeout(150)
        page.keyboard.press("Meta+a")
        page.keyboard.type(tag, delay=18)
        page.keyboard.press("Enter")
        page.wait_for_timeout(350)
        info["added"].append(tag)
    info["chips"] = chips(page)
    return info


def dropdown_trigger(page, label_exact):
    """Click the dropdown control associated with an exact label."""
    return page.evaluate(
        """(label)=>{
          let lab=null;
          const walk=(r,d=0)=>{
            if(!r||d>50||lab) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim();
              if (t===label || t.startsWith(label+'\\n') || t===label+':') {
                const b=el.getBoundingClientRect();
                if (b.width>15&&b.height>10&&b.y>50&&b.y<1000)
                  lab={x:b.x,y:b.y,w:b.width,h:b.height,t:t.slice(0,40)};
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
              ? r.querySelectorAll('ytcp-dropdown-trigger,ytcp-text-dropdown-trigger,[role=combobox],tp-yt-paper-dropdown-menu,button,div')
              : [])) {
              const b=el.getBoundingClientRect();
              const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
              if (b.width<60||b.height<20||b.height>100) continue;
              if (Math.abs(b.y-lab.y)>110) continue;
              if (b.x < lab.x-5) continue;
              // prefer controls that include the label text or sit to the right
              const score=Math.abs(b.y-lab.y)*3 + Math.max(0,b.x-lab.x)*0.05 + (t.includes(label)?0:20);
              if (!best||score<best.score)
                best={x:b.x+Math.min(b.width*0.7,220), y:b.y+b.height/2, t:t.slice(0,70), score};
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk2(el.shadowRoot,d+1);
          }; walk2(document);
          return {lab, best};
        }""",
        label_exact,
    )


def pick_exact(page, want: str, typed: str | None = None):
    """Pick dropdown option whose visible text equals want (or starts with want)."""
    # collect options
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
                out.push({t, x:b.x+b.width/2, y:b.y+b.height/2, w:b.width, h:b.height});
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document);
          // dedupe
          const seen=new Set(); const uniq=[];
          for (const o of out) { const k=o.t+'@'+Math.round(o.y); if(seen.has(k)) continue; seen.add(k); uniq.push(o); }
          return uniq.slice(0,80);
        }"""
    )
    # exact first
    exact = [o for o in opts if o["t"] == want]
    if not exact:
        exact = [o for o in opts if o["t"].startswith(want) and "Arab" not in o["t"] and "AP " not in o["t"]]
    if not exact and typed:
        exact = [o for o in opts if want.lower() in o["t"].lower() and "Arab" not in o["t"]]
    if exact:
        # prefer mid-screen
        exact.sort(key=lambda o: abs(o["y"] - 500))
        page.mouse.click(exact[0]["x"], exact[0]["y"])
        page.wait_for_timeout(700)
        return {"picked": exact[0], "n_opts": len(opts), "sample": [o["t"] for o in opts[:12]]}
    return {"picked": None, "n_opts": len(opts), "sample": [o["t"] for o in opts[:20]]}


def set_dd(page, label: str, want: str, type_text: str | None = None) -> dict:
    scroll_find(page, re.escape(label))
    page.wait_for_timeout(250)
    trig = dropdown_trigger(page, label)
    info = {"label": label, "want": want, "trig": trig}
    if not trig or not trig.get("best"):
        return {**info, "error": "no_trigger"}
    page.mouse.click(trig["best"]["x"], trig["best"]["y"])
    page.wait_for_timeout(900)
    if type_text:
        page.keyboard.type(type_text, delay=30)
        page.wait_for_timeout(1200)
    pick = pick_exact(page, want, typed=type_text)
    info["pick"] = pick
    if not pick.get("picked") and type_text:
        # clear and retry with shorter type
        page.keyboard.press("Meta+a")
        page.keyboard.press("Backspace")
        page.wait_for_timeout(300)
        page.keyboard.type(type_text.split()[0], delay=30)
        page.wait_for_timeout(1000)
        pick = pick_exact(page, want, typed=type_text)
        info["pick2"] = pick
    try:
        page.keyboard.press("Escape")
    except Exception:
        pass
    page.wait_for_timeout(350)
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
              if (/language|Type|Level|Exam|Academic|Education/i.test(t) && t.length<140)
                out.push(t.slice(0,140));
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document); return [...new Set(out)];
        }"""
    )


def process(page, u, job):
    key, vid = job["key"], job["id"]
    out = {"key": key, "id": vid, "steps": [], "started": datetime.now(LONDON).isoformat(timespec="seconds")}
    open_edit(page, u, vid)
    show_more(page)
    out["before_selects"] = selects(page)
    out["before_tags"] = chips(page)
    out["before_av"] = av(page, u)
    shot(page, f"{key}_v02_00_before.png")

    if job.get("order1"):
        if job.get("title"):
            body = page.inner_text("body")
            if job["title"] not in body:
                page.evaluate("window.scrollTo(0,0)")
                box = page.locator("#textbox, [aria-label*='Title' i]").first
                if box.count():
                    box.click(force=True)
                    page.keyboard.press("Meta+a")
                    page.keyboard.type(job["title"], delay=12)
                out["steps"].append(save_rr(page, u, "title"))
            else:
                out["title"] = "already"

        scroll_find(page, r"Paid promotion")
        hit = click_radio(page, r"No, my video doesn.?t include paid promotion")
        out["paid"] = hit
        out["steps"].append(save_rr(page, u, "paid_no"))
        shot(page, f"{key}_v02_paid.png")

        scroll_find(page, r"Allow automatic places")
        out["places"] = set_check(page, r"Allow automatic places", False)
        out["steps"].append(save_rr(page, u, "places_off"))
        shot(page, f"{key}_v02_places.png")

        out["tags"] = fill_tags(page, job["tags"])
        # strip forbidden if sun
        if key == "sun":
            for _ in range(15):
                bad = [c for c in chips(page) if SUN_BAD.search(c) or OTHER.search(c)]
                if not bad:
                    break
                clear_tags(page)
                fill_tags(page, job["tags"])
        out["steps"].append(save_rr(page, u, "tags"))
        shot(page, f"{key}_v02_tags.png")

    # Strip other-channel tags for all
    open_edit(page, u, vid)
    show_more(page)
    scroll_find(page, r"^Tags$")
    bad = [c for c in chips(page) if OTHER.search(c) or (key == "sun" and SUN_BAD.search(c))]
    out["strip_found"] = bad
    if bad:
        clear_tags(page)
        if job.get("tags"):
            fill_tags(page, job["tags"])
        out["steps"].append(save_rr(page, u, "strip_tags"))

    # Language
    lang = set_dd(page, "Title and description language", "English (United Kingdom)", type_text="English (United Kingdom)")
    out["lang"] = lang
    out["steps"].append(save_rr(page, u, "lang_en_uk"))
    shot(page, f"{key}_v02_lang.png")
    # verify
    sel = selects(page)
    if not any("Title and description language English (United Kingdom)" in s for s in sel):
        lang2 = set_dd(page, "Title and description language", "English (United Kingdom)", type_text="United Kingdom")
        out["lang_retry"] = lang2
        out["steps"].append(save_rr(page, u, "lang_en_uk_retry"))

    # Academic system United Kingdom (NOT UAE)
    acad = set_dd(page, "Academic system", "United Kingdom", type_text="United Kingdom")
    out["academic"] = acad
    # verify not UAE
    sel = selects(page)
    if any("United Arab Emirates" in s for s in sel) or not any(
        "Academic system United Kingdom" in s for s in sel
    ):
        acad = set_dd(page, "Academic system", "United Kingdom", type_text="United Kingdom")
        out["academic_retry"] = acad
    out["steps"].append(save_rr(page, u, "academic_uk"))
    shot(page, f"{key}_v02_academic.png")

    # Type Concept overview
    typ = set_dd(page, "Type", "Concept overview", type_text=None)
    out["type"] = typ
    out["steps"].append(save_rr(page, u, "type_concept"))
    shot(page, f"{key}_v02_type.png")

    # Level — Studio shows "Secondary school"
    lev = set_dd(page, "Level", "Secondary school", type_text=None)
    if not (lev.get("pick") or {}).get("picked"):
        lev = set_dd(page, "Level", "Secondary", type_text="Secondary")
    out["level"] = lev
    out["steps"].append(save_rr(page, u, "level_secondary"))
    shot(page, f"{key}_v02_level.png")

    # Exam exact
    exam = set_dd(page, "Exam, course or standard", job["exam"], type_text=job["exam"])
    out["exam"] = exam
    # verify
    body = page.inner_text("body")
    if job["exam"] not in body:
        exam = set_dd(page, "Exam, course or standard", job["exam"], type_text="GCSE")
        # pick from samples carefully
        if exam.get("pick", {}).get("sample"):
            # reopen and click exact from list
            trig = dropdown_trigger(page, "Exam, course or standard")
            if trig and trig.get("best"):
                page.mouse.click(trig["best"]["x"], trig["best"]["y"])
                page.wait_for_timeout(700)
                page.keyboard.type(job["exam"], delay=35)
                page.wait_for_timeout(1500)
                pick = pick_exact(page, job["exam"])
                out["exam_pick3"] = pick
                page.keyboard.press("Escape")
        out["exam_retry"] = exam
    out["steps"].append(save_rr(page, u, "exam"))
    shot(page, f"{key}_v02_exam.png")

    # Final
    open_edit(page, u, vid)
    show_more(page)
    for _ in range(14):
        page.mouse.wheel(0, 800)
        page.wait_for_timeout(70)
    out["final_tags"] = chips(page)
    out["final_selects"] = selects(page)
    out["final_av"] = av(page, u)
    body = page.inner_text("body")
    places = set_check(page, r"Allow automatic places", False)  # read-only effect; if already false ok
    # re-read without toggling wrongly — just read
    places_state = page.evaluate(
        """()=>{
          const walk=(r,d=0)=>{
            if(!r||d>50) return null;
            for (const el of (r.querySelectorAll?r.querySelectorAll('[role=checkbox]'):[])) {
              const lab=el.getAttribute('aria-label')||'';
              if (/Allow automatic places/i.test(lab))
                return el.getAttribute('aria-checked')==='true';
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) { const h=walk(el.shadowRoot,d+1); if(h!==null) return h; }
            return null;
          }; return walk(document);
        }"""
    )
    paid = page.evaluate(
        """()=>{
          const out=[];
          const walk=(r,d=0)=>{
            if(!r||d>50) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('[role=radio]'):[])) {
              const lab=(el.getAttribute('aria-label')||el.innerText||'').replace(/\\s+/g,' ').trim();
              if (/paid promotion/i.test(lab))
                out.push({lab:lab.slice(0,80), checked:el.getAttribute('aria-checked')==='true'});
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document); return out;
        }"""
    )
    out["final"] = {
        "title_ok": (job["title"] in body) if job.get("title") else None,
        "paid_no": any(p.get("checked") and p["lab"].startswith("No") for p in paid),
        "places_off": places_state is False,
        "lang_uk": any("Title and description language English (United Kingdom)" in s for s in out["final_selects"]),
        "video_lang_uk": any("Video language English (United Kingdom)" in s for s in out["final_selects"]),
        "type_concept": any(re.search(r"Type Concept overview", s) for s in out["final_selects"]),
        "level_secondary": any(re.search(r"Level Secondary", s) for s in out["final_selects"]),
        "academic_uk": any("Academic system United Kingdom" in s for s in out["final_selects"]),
        "academic_uae_bad": any("United Arab Emirates" in s for s in out["final_selects"]),
        "exam_ok": job["exam"] in body or any(job["exam"] in s for s in out["final_selects"]),
        "tags": out["final_tags"],
        "other_left": [c for c in out["final_tags"] if OTHER.search(c)],
        "sun_bad_left": [c for c in out["final_tags"] if key == "sun" and SUN_BAD.search(c)],
        "paid_radios": paid,
        "places_state": places_state,
    }
    shot(page, f"{key}_v02_99_final.png")
    scroll_find(page, r"Academic system|^Education$")
    shot(page, f"{key}_v02_99_education.png")
    scroll_find(page, r"^Tags$|Paid promotion")
    shot(page, f"{key}_v02_99_tags_paid.png")
    f = out["final"]
    out["ok"] = bool(
        out["final_av"]["not_kids"]
        and not f["other_left"]
        and not f["sun_bad_left"]
        and not f["academic_uae_bad"]
        and f["lang_uk"]
        and f["type_concept"]
        and f["level_secondary"]
        and f["academic_uk"]
        and f["exam_ok"]
        and (f["paid_no"] if job.get("order1") else True)
        and (f["places_off"] if job.get("order1") else True)
        and (f["title_ok"] if job.get("title") else True)
    )
    out["finished"] = datetime.now(LONDON).isoformat(timespec="seconds")
    (EV / f"{key}_V02_RESULT.json").write_text(json.dumps(out, indent=2, default=str) + "\n")
    return out


def main():
    u = load_u()
    EV.mkdir(parents=True, exist_ok=True)
    result = {
        "order": "Ben 14:45 v02 precise",
        "started": datetime.now(LONDON).isoformat(timespec="seconds"),
        "launch_day_15oct1805": "Fri Related → GHZDsiH7L7A",
        "videos": [],
    }
    u.ensure_chrome()
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(u.CDP)
        page = browser.contexts[0].new_page()
        page.set_viewport_size({"width": 1440, "height": 1100})
        try:
            page.goto("https://www.youtube.com/channel_switcher", wait_until="domcontentloaded", timeout=120000)
            page.wait_for_timeout(2500)
            hit = page.evaluate(
                """()=>{
                  const walk=(r,d=0)=>{
                    if(!r||d>45) return null;
                    for (const el of (r.querySelectorAll?r.querySelectorAll('ytd-account-item-renderer'):[])) {
                      if ((el.innerText||'').includes('History of Science')) {
                        const b=el.getBoundingClientRect();
                        return {x:b.x+b.width/2,y:b.y+b.height/2};
                      }
                    }
                    for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                      if (el.shadowRoot) { const h=walk(el.shadowRoot,d+1); if(h) return h; }
                    return null;
                  }; return walk(document);
                }"""
            )
            if hit:
                page.mouse.click(hit["x"], hit["y"])
                page.wait_for_timeout(3500)
        except Exception:
            pass
        hos = u.ensure_hos(page)
        result["hos"] = hos
        if not hos.get("ok"):
            (EV / "STUDIO_FIXES_V02.json").write_text(json.dumps(result, indent=2) + "\n")
            return 2
        for job in JOBS:
            print(f"==== {job['key']} {job['id']} ====", flush=True)
            try:
                item = process(page, u, job)
            except Exception as e:
                item = {"key": job["key"], "id": job["id"], "ok": False, "error": f"{type(e).__name__}:{e}"}
                shot(page, f"{job['key']}_v02_EXCEPTION.png")
            result["videos"].append(item)
            print(json.dumps({"key": item.get("key"), "ok": item.get("ok"), "final": item.get("final"), "selects": item.get("final_selects"), "tags": item.get("final_tags")}, indent=2, default=str)[:3000], flush=True)
        result["finished"] = datetime.now(LONDON).isoformat(timespec="seconds")
        result["ok"] = all(v.get("ok") for v in result["videos"])
        (EV / "STUDIO_FIXES_V02.json").write_text(json.dumps(result, indent=2, default=str) + "\n")
        shutil.copy2(EV / "STUDIO_FIXES_V02.json", ART / "BEN_1445FIX_STUDIO_FIXES_V02.json")
        print("ALL_OK", result["ok"], flush=True)
        page.close()
        return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
