#!/usr/bin/env python3
"""Ben 14:45 Studio fixes — ORDER 1 (Fri then Sun) + ORDER 2 (all four).

HOS only. One setting per save; re-read Audience + Visibility after each save.
Ignore vidIQ. Never add other-channel tags. Do not touch CUu8k38iAMc.
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
BANNED_IDS = {"CUu8k38iAMc"}
OTHER_CHANNEL_TAG_RE = re.compile(
    r"crash\s*course|vlogbrothers|hank\s*green|scishow|sci\s*show|"
    r"ted[- ]?ed|khan\s*academy|vsauce|veritasium|kurzgesagt|"
    r"freesciencelessons|mr\s*barnes|pbs\s*spacetime|minutephysics",
    re.I,
)

FRI_ID = "29bpGAI0wb8"
SUN_ID = "TbMMJSRKC3U"
LONG_ID = "GHZDsiH7L7A"
LISTER_ID = "clV6E10NLPw"
FRI_TITLE = "What happens if you keep cutting gold in half?"

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
SUN_FORBIDDEN = re.compile(r"gold|x-?ray|röntgen|roentgen|bertha|atom\b|dalton", re.I)

JOBS = [
    {
        "key": "fri",
        "id": FRI_ID,
        "title": FRI_TITLE,
        "tags": FRI_TAGS,
        "exam": "GCSE Chemistry",
        "order1": True,
    },
    {
        "key": "sun",
        "id": SUN_ID,
        "title": None,  # leave title
        "tags": SUN_TAGS,
        "exam": "GCSE Chemistry",
        "order1": True,
    },
    {
        "key": "long004",
        "id": LONG_ID,
        "title": None,
        "tags": None,  # strip other-channel only; keep topical
        "exam": "GCSE Chemistry",
        "order1": False,
    },
    {
        "key": "lister",
        "id": LISTER_ID,
        "title": None,
        "tags": None,
        "exam": "GCSE Biology",
        "order1": False,
    },
]


def load_u():
    spec = importlib.util.spec_from_file_location("hos004_upload", U004)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


def shot(page, name: str) -> Path:
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    p = EV / name
    page.screenshot(path=str(p), full_page=True)
    shutil.copy2(p, ART / f"BEN_1445fix_{name}")
    return p


def open_edit(page, u, vid: str) -> None:
    assert vid not in BANNED_IDS
    page.goto(
        f"https://studio.youtube.com/video/{vid}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3500)
    u.dismiss(page)
    assert not any(b in page.url for b in BANNED_IDS)


def show_more_all(page) -> int:
    n = 0
    for _ in range(6):
        clicked = page.evaluate(
            """() => {
              const walk=(r,d=0)=>{
                if(!r||d>45) return false;
                for (const el of (r.querySelectorAll
                  ? r.querySelectorAll('button,ytcp-button,[role=button]') : [])) {
                  if ((el.innerText||'').trim()==='Show more') {
                    const b=el.getBoundingClientRect();
                    if (b.width>20 && b.height>12) { el.click(); return true; }
                  }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                  if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
                return false;
              };
              return walk(document);
            }"""
        )
        if not clicked:
            break
        n += 1
        page.wait_for_timeout(500)
    return n


def scroll_find(page, pattern: str, max_wheels: int = 24) -> bool:
    for _ in range(max_wheels):
        found = page.evaluate(
            """(pat) => {
              const re=new RegExp(pat,'i');
              const walk=(r,d=0)=>{
                if(!r||d>45) return false;
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                  const t=(el.innerText||'').trim();
                  if (re.test(t) && t.length<80) {
                    el.scrollIntoView({block:'center'}); return true;
                  }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                  if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
                return false;
              };
              return walk(document);
            }""",
            pattern,
        )
        if found:
            page.wait_for_timeout(350)
            return True
        page.mouse.wheel(0, 700)
        page.wait_for_timeout(100)
    return False


def read_audience_vis(page, u) -> dict:
    return {
        "chip": u.visibility_chip(page),
        "audience": page.evaluate(
            """() => {
              const out=[];
              const walk=(r,d=0)=>{
                if(!r||d>50) return;
                for (const el of (r.querySelectorAll
                  ? r.querySelectorAll('[role=radio],tp-yt-paper-radio-button') : [])) {
                  const lab=(el.getAttribute('aria-label')||el.innerText||'')
                    .replace(/\\s+/g,' ').trim();
                  if (/Made for Kids/i.test(lab))
                    out.push({lab:lab.slice(0,60), checked:el.getAttribute('aria-checked')==='true'});
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                  if (el.shadowRoot) walk(el.shadowRoot,d+1);
              }; walk(document); return out;
            }"""
        ),
        "banner_not_kids": bool(
            re.search(
                r"set to not\s*['\"]?Made for Kids",
                page.inner_text("body"),
                re.I,
            )
        ),
    }


def save_and_reread(page, u, label: str) -> dict:
    s = u.page_save(page)
    page.wait_for_timeout(2200)
    av = read_audience_vis(page, u)
    return {"label": label, "save": s, **av}


def click_radio(page, pattern: str) -> dict | None:
    hit = page.evaluate(
        """(pat) => {
          const re=new RegExp(pat,'i');
          let hit=null;
          const walk=(r,d=0)=>{
            if(!r||d>50||hit) return;
            for (const el of (r.querySelectorAll
              ? r.querySelectorAll('[role=radio],tp-yt-paper-radio-button') : [])) {
              const lab=(el.getAttribute('aria-label')||el.innerText||'')
                .replace(/\\s+/g,' ').trim();
              if (!re.test(lab)) continue;
              const b=el.getBoundingClientRect();
              if (b.width>10 && b.height>10)
                hit={lab:lab.slice(0,90),x:b.x+b.width/2,y:b.y+b.height/2,
                     checked:el.getAttribute('aria-checked')==='true'};
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document); return hit;
        }""",
        pattern,
    )
    if hit:
        page.mouse.click(hit["x"], hit["y"])
        page.wait_for_timeout(500)
    return hit


def set_checkbox(page, pattern: str, want: bool) -> dict:
    return page.evaluate(
        """(args) => {
          const pat=args[0], want=args[1];
          const re=new RegExp(pat,'i');
          let found=null;
          const walk=(r,d=0)=>{
            if(!r||d>50||found) return;
            for (const el of (r.querySelectorAll
              ? r.querySelectorAll('[role=checkbox],tp-yt-paper-checkbox,input[type=checkbox]')
              : [])) {
              const lab=(el.getAttribute('aria-label')||el.innerText||
                (el.parentElement&&el.parentElement.innerText)||'')
                .replace(/\\s+/g,' ').trim();
              if (!re.test(lab)) continue;
              const on=el.getAttribute('aria-checked')==='true'||el.checked===true;
              found={lab:lab.slice(0,90), before:on};
              if (on !== want) el.click();
              found.after = el.getAttribute('aria-checked')==='true'||el.checked===true;
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document); return found||{lab:'missing'};
        }""",
        [pattern, want],
    )


def list_tag_chips(page) -> list[str]:
    return page.evaluate(
        """() => {
          const out=[];
          const walk=(r,d=0)=>{
            if(!r||d>50) return;
            for (const el of (r.querySelectorAll
              ? r.querySelectorAll('ytcp-chip,yt-chip-cloud-chip') : [])) {
              const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
              if (t && t.length<90 && t.toLowerCase()!=='tags') out.push(t);
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document);
          return [...new Set(out)];
        }"""
    )


def clear_all_tags(page) -> int:
    """Remove tag chips via remove buttons."""
    removed = 0
    for _ in range(40):
        hit = page.evaluate(
            """() => {
              const walk=(r,d=0)=>{
                if(!r||d>50) return null;
                for (const el of (r.querySelectorAll
                  ? r.querySelectorAll('ytcp-chip,yt-chip-cloud-chip') : [])) {
                  const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
                  if (!t || t.length>90) continue;
                  // find remove button inside chip
                  const btns=[...el.querySelectorAll('button,ytcp-icon-button,[role=button],yt-icon-button')];
                  const shadowBtns=[];
                  const sw=(n,dd=0)=>{
                    if(!n||dd>8) return;
                    for (const c of (n.querySelectorAll?n.querySelectorAll('*'):[])) {
                      if (c.tagName && /BUTTON|ICON/i.test(c.tagName)) shadowBtns.push(c);
                      if (c.shadowRoot) sw(c.shadowRoot,dd+1);
                    }
                  };
                  sw(el);
                  const candidates=btns.concat(shadowBtns);
                  for (const b of candidates) {
                    const a=(b.getAttribute('aria-label')||'')+(b.getAttribute('title')||'');
                    if (/remove|delete|clear/i.test(a) || true) {
                      const r=b.getBoundingClientRect();
                      if (r.width>8 && r.height>8)
                        return {x:r.x+r.width/2,y:r.y+r.height/2,t:t.slice(0,60)};
                    }
                  }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                  if (el.shadowRoot) { const h=walk(el.shadowRoot,d+1); if(h) return h; }
                return null;
              };
              return walk(document);
            }"""
        )
        if not hit:
            break
        page.mouse.click(hit["x"], hit["y"])
        page.wait_for_timeout(250)
        removed += 1
    return removed


def fill_tags(page, tags: list[str]) -> dict:
    joined = ", ".join(tags)
    ok = page.evaluate(
        """(tags) => {
          const boxes=[...document.querySelectorAll('input,textarea,[contenteditable=true]')];
          for (const b of boxes) {
            const aria=(b.getAttribute('aria-label')||'')+(b.getAttribute('placeholder')||'');
            const near=(b.closest('ytcp-form-input-container,ytcp-video-metadata-editor,ytcp-video-metadata-editor-advanced')?.innerText||'');
            if (/tag/i.test(aria+near) && !/hashtag/i.test(aria)) {
              b.focus();
              if (b.isContentEditable) {
                b.innerText='';
                b.dispatchEvent(new InputEvent('input',{bubbles:true}));
                b.innerText=tags;
                b.dispatchEvent(new InputEvent('input',{bubbles:true}));
              } else {
                const proto = b.tagName==='TEXTAREA'
                  ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype;
                Object.getOwnPropertyDescriptor(proto,'value').set.call(b, tags);
                b.dispatchEvent(new Event('input',{bubbles:true}));
              }
              return {ok:true, aria:aria.slice(0,60)};
            }
          }
          return {ok:false};
        }""",
        joined,
    )
    page.wait_for_timeout(600)
    # Press Enter to commit chips if needed
    try:
        page.keyboard.press("Enter")
        page.wait_for_timeout(400)
    except Exception:
        pass
    return ok


def set_title(page, title: str) -> dict:
    box = page.locator(
        "#textbox, ytcp-social-suggestions-textbox #textbox, [aria-label*='Title' i]"
    ).first
    info: dict = {}
    if box.count():
        box.click(force=True)
        page.keyboard.press("Meta+a")
        page.keyboard.type(title, delay=12)
        info["typed"] = True
    else:
        info["typed"] = False
    return info


def open_dropdown_near(page, label_pat: str) -> bool:
    return bool(
        page.evaluate(
            """(pat) => {
              const re=new RegExp(pat,'i');
              let labelY=null, labelX=null;
              const walk=(r,d=0)=>{
                if(!r||d>50) return;
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                  const t=(el.innerText||'').trim();
                  if (re.test(t) && t.length<60) {
                    const b=el.getBoundingClientRect();
                    if (b.width>20 && b.height>10 && b.y>80) {
                      labelY=b.y; labelX=b.x; return;
                    }
                  }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                  if (el.shadowRoot) walk(el.shadowRoot,d+1);
              };
              walk(document);
              if (labelY==null) return false;
              // click nearest dropdown/combobox to the right or just below
              let best=null;
              const walk2=(r,d=0)=>{
                if(!r||d>50) return;
                for (const el of (r.querySelectorAll
                  ? r.querySelectorAll('ytcp-dropdown-trigger,[role=combobox],tp-yt-paper-dropdown-menu,button,div')
                  : [])) {
                  const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
                  const b=el.getBoundingClientRect();
                  if (b.width<40 || b.height<18 || b.height>80) continue;
                  if (Math.abs(b.y-labelY)>90) continue;
                  if (b.x < labelX-20) continue;
                  const score=Math.abs(b.y-labelY)*2 + (b.x-labelX)*0.01;
                  if (!best || score<best.score)
                    best={x:b.x+Math.min(b.width*0.7,180), y:b.y+b.height/2, t:t.slice(0,50), score};
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                  if (el.shadowRoot) walk2(el.shadowRoot,d+1);
              };
              walk2(document);
              if (!best) return false;
              // click via returned coords — parent clicks
              const ev=new MouseEvent('click',{bubbles:true,clientX:best.x,clientY:best.y});
              document.elementFromPoint(best.x,best.y)?.dispatchEvent(ev);
              return best;
            }""",
            label_pat,
        )
    )


def pick_option(page, pattern: str) -> dict | None:
    hit = page.evaluate(
        """(pat) => {
          const re=new RegExp(pat,'i');
          let best=null;
          const walk=(r,d=0)=>{
            if(!r||d>50) return;
            for (const el of (r.querySelectorAll
              ? r.querySelectorAll('tp-yt-paper-item,[role=option],ytcp-ve,div,span,a')
              : [])) {
              const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
              if (!re.test(t) || t.length>100) continue;
              const b=el.getBoundingClientRect();
              if (b.width>40 && b.height>16 && b.height<70 && b.y>40)
                best={t:t.slice(0,80),x:b.x+b.width/2,y:b.y+b.height/2,w:b.width,h:b.height};
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document);
          return best;
        }""",
        pattern,
    )
    if hit:
        page.mouse.click(hit["x"], hit["y"])
        page.wait_for_timeout(700)
    return hit


def set_dropdown(page, label_pat: str, option_pat: str) -> dict:
    scroll_find(page, label_pat)
    page.wait_for_timeout(300)
    # Try click label's sibling dropdown via mouse on evaluate coords
    coords = page.evaluate(
        """(pat) => {
          const re=new RegExp(pat,'i');
          let label=null;
          const walk=(r,d=0)=>{
            if(!r||d>50||label) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim();
              if (re.test(t) && t.length<55) {
                const b=el.getBoundingClientRect();
                if (b.width>20 && b.height>12 && b.y>60) label={x:b.x,y:b.y,w:b.width,h:b.height,t:t.slice(0,40)};
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document);
          if (!label) return null;
          let best=null;
          const walk2=(r,d=0)=>{
            if(!r||d>50) return;
            for (const el of (r.querySelectorAll
              ? r.querySelectorAll('ytcp-dropdown-trigger,[role=combobox],tp-yt-paper-dropdown-menu,ytcp-text-dropdown-trigger,button,div')
              : [])) {
              const b=el.getBoundingClientRect();
              if (b.width<50 || b.height<18 || b.height>90) continue;
              if (Math.abs(b.y-label.y)>100) continue;
              if (b.x < label.x - 10) continue;
              const score=Math.abs(b.y-label.y)+ (b.x-label.x)*0.02;
              const t=(el.innerText||'').replace(/\\s+/g,' ').trim().slice(0,60);
              if (!best || score<best.score)
                best={x:b.x+Math.min(b.width*0.65,200),y:b.y+b.height/2,t,score};
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk2(el.shadowRoot,d+1);
          }; walk2(document);
          return {label, best};
        }""",
        label_pat,
    )
    info: dict = {"label": label_pat, "coords": coords}
    if coords and coords.get("best"):
        page.mouse.click(coords["best"]["x"], coords["best"]["y"])
        page.wait_for_timeout(900)
    else:
        open_dropdown_near(page, label_pat)
        page.wait_for_timeout(900)
    # Type into search if dropdown has filter (Exam field)
    try:
        page.keyboard.type(
            re.sub(r"[\^\\$]", "", option_pat).split("(")[0][:40], delay=20
        )
        page.wait_for_timeout(800)
    except Exception:
        pass
    opt = pick_option(page, option_pat)
    info["option"] = opt
    if not opt:
        # Escape and retry without typing
        try:
            page.keyboard.press("Escape")
        except Exception:
            pass
        page.wait_for_timeout(400)
        if coords and coords.get("best"):
            page.mouse.click(coords["best"]["x"], coords["best"]["y"])
            page.wait_for_timeout(800)
        opt = pick_option(page, option_pat)
        info["option_retry"] = opt
    try:
        page.keyboard.press("Escape")
    except Exception:
        pass
    page.wait_for_timeout(300)
    return info


def read_selects_snip(page) -> list[dict]:
    return page.evaluate(
        """() => {
          const out=[];
          const walk=(r,d=0)=>{
            if(!r||d>50) return;
            for (const el of (r.querySelectorAll
              ? r.querySelectorAll('ytcp-dropdown-trigger,[role=combobox],tp-yt-paper-dropdown-menu')
              : [])) {
              const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
              if (/language|Type|Level|Exam|Academic|Education/i.test(t) && t.length<120)
                out.push(t.slice(0,120));
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document);
          return [...new Set(out)].slice(0,30);
        }"""
    )


def live_shorts_check(page, u) -> dict:
    page.goto(
        f"https://studio.youtube.com/channel/{u.HOS}/videos/short",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(5000)
    u.dismiss(page)
    scraped = page.evaluate(
        """() => {
          const out=[];
          const walk=(r,d=0)=>{
            if(!r||d>45) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('ytcp-video-row,a'):[])) {
              const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
              if (t.length>12 && t.length<220) out.push(t.slice(0,200));
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document);
          return [...new Set(out)].slice(0,50);
        }"""
    )
    shot(page, "LIVE_SHORTS_titles.png")
    titles = [s for s in scraped if "cutting gold" in s.lower() or "how small can you cut gold" in s.lower() or "eighth" in s.lower() or "spray" in s.lower()]
    return {
        "fri_new_present": any("keep cutting gold in half" in s.lower() for s in scraped),
        "fri_old_present": any(
            re.search(r"how small can you cut gold\?", s, re.I) for s in scraped
        ),
        "duplicate_new_count": sum(
            1 for s in scraped if "keep cutting gold in half" in s.lower()
        ),
        "sample": titles[:15],
    }


def process_video(page, u, job: dict) -> dict:
    key = job["key"]
    vid = job["id"]
    out: dict = {
        "key": key,
        "id": vid,
        "steps": [],
        "started": datetime.now(LONDON).isoformat(timespec="seconds"),
    }
    open_edit(page, u, vid)
    show_more_all(page)
    out["before_av"] = read_audience_vis(page, u)
    out["before_tags"] = list_tag_chips(page)
    out["before_selects"] = read_selects_snip(page)
    shot(page, f"{key}_00_before.png")

    # --- ORDER 1 bits for Fri/Sun ---
    if job.get("order1"):
        # Title (Fri only if needed)
        if job.get("title"):
            body = page.inner_text("body")
            if job["title"] not in body:
                page.evaluate("window.scrollTo(0,0)")
                page.wait_for_timeout(300)
                out["title_set"] = set_title(page, job["title"])
                out["steps"].append(save_and_reread(page, u, "title"))
                shot(page, f"{key}_01_title.png")
            else:
                out["title_set"] = {"already": True}

        # Paid promotion No
        scroll_find(page, r"Paid promotion")
        hit = click_radio(page, r"No, my video doesn.?t include paid promotion")
        out["paid_click"] = hit
        if hit and not hit.get("checked"):
            out["steps"].append(save_and_reread(page, u, "paid_promotion_no"))
        else:
            # still save if we clicked, or note already
            if hit and hit.get("checked"):
                out["paid"] = "already_no"
            else:
                out["steps"].append(save_and_reread(page, u, "paid_promotion_no"))
        shot(page, f"{key}_02_paid.png")

        # Featured places — untick Allow automatic places
        scroll_find(page, r"Allow automatic places|Featured places")
        out["places"] = set_checkbox(page, r"Allow automatic places", False)
        out["steps"].append(save_and_reread(page, u, "automatic_places_off"))
        shot(page, f"{key}_03_places.png")

        # Tags replace
        scroll_find(page, r"^Tags$")
        removed = clear_all_tags(page)
        out["tags_removed"] = removed
        # Also remove any leftover via forbidden filter for Sun
        if key == "sun":
            # clear again if forbidden remain
            for _ in range(10):
                chips = list_tag_chips(page)
                bad = [c for c in chips if SUN_FORBIDDEN.search(c) or OTHER_CHANNEL_TAG_RE.search(c)]
                if not bad:
                    break
                clear_all_tags(page)
        fill = fill_tags(page, job["tags"])
        out["tags_fill"] = fill
        page.wait_for_timeout(800)
        # Ensure chips committed — type each tag with Enter
        for tag in job["tags"]:
            page.evaluate(
                """(tag) => {
                  const boxes=[...document.querySelectorAll('input,textarea')];
                  for (const b of boxes) {
                    const aria=(b.getAttribute('aria-label')||'')+(b.getAttribute('placeholder')||'');
                    if (/tag/i.test(aria)) {
                      b.focus();
                      const proto=b.tagName==='TEXTAREA'?HTMLTextAreaElement.prototype:HTMLInputElement.prototype;
                      Object.getOwnPropertyDescriptor(proto,'value').set.call(b, tag);
                      b.dispatchEvent(new Event('input',{bubbles:true}));
                      return true;
                    }
                  }
                  return false;
                }""",
                tag,
            )
            page.keyboard.press("Enter")
            page.wait_for_timeout(280)
        out["tags_after_fill"] = list_tag_chips(page)
        out["steps"].append(save_and_reread(page, u, "tags"))
        shot(page, f"{key}_04_tags.png")

    # --- ORDER 2: language + education + strip other-channel tags (all four) ---
    open_edit(page, u, vid)
    show_more_all(page)

    # Strip other-channel tags (and Sun forbidden if any remain)
    scroll_find(page, r"^Tags$")
    chips = list_tag_chips(page)
    strip = [c for c in chips if OTHER_CHANNEL_TAG_RE.search(c)]
    if key == "sun":
        strip += [c for c in chips if SUN_FORBIDDEN.search(c)]
    strip = list(dict.fromkeys(strip))
    out["other_channel_tags_found"] = strip
    if strip or (job.get("tags") is None and any(OTHER_CHANNEL_TAG_RE.search(c) for c in chips)):
        # remove matching chips only
        for _ in range(30):
            chips_now = list_tag_chips(page)
            target = next(
                (
                    c
                    for c in chips_now
                    if OTHER_CHANNEL_TAG_RE.search(c)
                    or (key == "sun" and SUN_FORBIDDEN.search(c))
                ),
                None,
            )
            if not target:
                break
            # click remove on that chip
            page.evaluate(
                """(want) => {
                  const walk=(r,d=0)=>{
                    if(!r||d>50) return null;
                    for (const el of (r.querySelectorAll?r.querySelectorAll('ytcp-chip,yt-chip-cloud-chip'):[])) {
                      const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
                      if (t!==want) continue;
                      const b=el.getBoundingClientRect();
                      // click right side (X)
                      return {x:b.x+b.width-12,y:b.y+b.height/2};
                    }
                    for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                      if (el.shadowRoot) { const h=walk(el.shadowRoot,d+1); if(h) return h; }
                    return null;
                  }; return walk(document);
                }""",
                target,
            )
            hit = page.evaluate(
                """(want) => {
                  const walk=(r,d=0)=>{
                    if(!r||d>50) return null;
                    for (const el of (r.querySelectorAll?r.querySelectorAll('ytcp-chip,yt-chip-cloud-chip'):[])) {
                      const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
                      if (t!==want) continue;
                      const b=el.getBoundingClientRect();
                      return {x:b.x+b.width-14,y:b.y+b.height/2,t};
                    }
                    for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                      if (el.shadowRoot) { const h=walk(el.shadowRoot,d+1); if(h) return h; }
                    return null;
                  }; return walk(document);
                }""",
                target,
            )
            if hit:
                page.mouse.click(hit["x"], hit["y"])
                page.wait_for_timeout(250)
        out["steps"].append(save_and_reread(page, u, "strip_other_channel_tags"))
        shot(page, f"{key}_05_tags_stripped.png")

    # Title and description language = English (United Kingdom)
    scroll_find(page, r"Title and description language")
    lang = set_dropdown(
        page, r"Title and description language", r"English \(United Kingdom\)"
    )
    out["title_desc_language"] = lang
    out["steps"].append(save_and_reread(page, u, "title_desc_language_en_uk"))
    shot(page, f"{key}_06_language.png")

    # Education fields
    scroll_find(page, r"^Education$|^Type$|Academic system")
    # Academic system United Kingdom
    acad = set_dropdown(page, r"Academic system", r"United Kingdom|^UK$")
    out["academic"] = acad
    out["steps"].append(save_and_reread(page, u, "academic_uk"))
    shot(page, f"{key}_07_academic.png")

    # Type = concept overview / explainer
    typ = set_dropdown(
        page,
        r"^Type$",
        r"concept overview|explainer|Concept overview",
    )
    if not typ.get("option") and not typ.get("option_retry"):
        typ = set_dropdown(page, r"^Type$", r"overview|Explainer|Concept")
    out["edu_type"] = typ
    out["steps"].append(save_and_reread(page, u, "edu_type"))
    shot(page, f"{key}_08_type.png")

    # Level = secondary
    lev = set_dropdown(page, r"^Level$", r"^Secondary$|secondary")
    out["edu_level"] = lev
    out["steps"].append(save_and_reread(page, u, "edu_level"))
    shot(page, f"{key}_09_level.png")

    # Exam
    exam = set_dropdown(page, r"Exam, course or standard", re.escape(job["exam"]))
    if not exam.get("option") and not exam.get("option_retry"):
        # try typing GCSE Chemistry / Biology more loosely
        exam = set_dropdown(page, r"Exam, course or standard", job["exam"].split()[-1])
        # last resort: open and type full
        scroll_find(page, r"Exam, course or standard")
        coords = page.evaluate(
            """() => {
              let label=null;
              const walk=(r,d=0)=>{
                if(!r||d>50||label) return;
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                  const t=(el.innerText||'').trim();
                  if (/Exam, course or standard/i.test(t) && t.length<40) {
                    const b=el.getBoundingClientRect();
                    if (b.y>60) label={x:b.x,y:b.y};
                  }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                  if (el.shadowRoot) walk(el.shadowRoot,d+1);
              }; walk(document);
              if(!label) return null;
              let best=null;
              const walk2=(r,d=0)=>{
                if(!r||d>50) return;
                for (const el of (r.querySelectorAll
                  ? r.querySelectorAll('input,ytcp-dropdown-trigger,[role=combobox],div') : [])) {
                  const b=el.getBoundingClientRect();
                  if (Math.abs(b.y-label.y)>80 || b.width<80) continue;
                  if (b.x<label.x-10) continue;
                  best={x:b.x+b.width/2,y:b.y+b.height/2};
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                  if (el.shadowRoot) walk2(el.shadowRoot,d+1);
              }; walk2(document); return best;
            }"""
        )
        if coords:
            page.mouse.click(coords["x"], coords["y"])
            page.wait_for_timeout(600)
            page.keyboard.type(job["exam"], delay=25)
            page.wait_for_timeout(1200)
            opt = pick_option(page, re.escape(job["exam"]))
            if not opt:
                opt = pick_option(page, r"GCSE")
            exam["typed_pick"] = opt
            try:
                page.keyboard.press("Enter")
            except Exception:
                pass
    out["edu_exam"] = exam
    out["steps"].append(save_and_reread(page, u, "edu_exam"))
    shot(page, f"{key}_10_exam.png")

    # Final proof
    open_edit(page, u, vid)
    show_more_all(page)
    for _ in range(12):
        page.mouse.wheel(0, 800)
        page.wait_for_timeout(80)
    out["final_tags"] = list_tag_chips(page)
    out["final_selects"] = read_selects_snip(page)
    out["final_av"] = read_audience_vis(page, u)
    body = page.inner_text("body")
    out["final"] = {
        "title_ok": (job.get("title") in body) if job.get("title") else None,
        "paid_no": bool(
            re.search(r"No, my video doesn.?t include paid promotion", body, re.I)
        ),
        "places_off": "Allow automatic places" in body,  # presence; check via checkbox
        "en_uk_title_desc": bool(
            re.search(r"Title and description language\s*English \(United Kingdom\)", body)
            or any("Title and description language English (United Kingdom)" in s for s in out["final_selects"])
        ),
        "video_lang_uk": any("Video language English (United Kingdom)" in s for s in out["final_selects"]),
        "exam_present": job["exam"] in body,
        "secondary": bool(re.search(r"Level\s*Secondary|Secondary", body)),
        "type_ok": bool(re.search(r"concept overview|explainer|Concept", body, re.I)),
        "academic_uk": bool(re.search(r"Academic system\s*United Kingdom", body)),
        "other_channel_tags_left": [
            c for c in out["final_tags"] if OTHER_CHANNEL_TAG_RE.search(c)
        ],
        "sun_forbidden_left": [
            c for c in out["final_tags"] if key == "sun" and SUN_FORBIDDEN.search(c)
        ],
    }
    out["places_checkbox"] = page.evaluate(
        """() => {
          const walk=(r,d=0)=>{
            if(!r||d>50) return null;
            for (const el of (r.querySelectorAll
              ? r.querySelectorAll('[role=checkbox],tp-yt-paper-checkbox') : [])) {
              const lab=(el.getAttribute('aria-label')||'').trim();
              if (/Allow automatic places/i.test(lab))
                return {checked:el.getAttribute('aria-checked')==='true'};
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) { const h=walk(el.shadowRoot,d+1); if(h) return h; }
            return null;
          }; return walk(document);
        }"""
    )
    # Paid radio state
    out["paid_radios"] = page.evaluate(
        """() => {
          const out=[];
          const walk=(r,d=0)=>{
            if(!r||d>50) return;
            for (const el of (r.querySelectorAll
              ? r.querySelectorAll('[role=radio],tp-yt-paper-radio-button') : [])) {
              const lab=(el.getAttribute('aria-label')||el.innerText||'').replace(/\\s+/g,' ').trim();
              if (/paid promotion/i.test(lab))
                out.push({lab:lab.slice(0,80), checked:el.getAttribute('aria-checked')==='true'});
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document); return out;
        }"""
    )
    shot(page, f"{key}_99_final.png")
    # scroll to education for shot
    scroll_find(page, r"Academic system|^Education$")
    shot(page, f"{key}_99_education.png")
    scroll_find(page, r"^Tags$")
    shot(page, f"{key}_99_tags.png")
    out["finished"] = datetime.now(LONDON).isoformat(timespec="seconds")
    out["ok"] = (
        out["final_av"].get("banner_not_kids")
        and not out["final"]["other_channel_tags_left"]
        and not out["final"]["sun_forbidden_left"]
    )
    (EV / f"{key}_RESULT.json").write_text(json.dumps(out, indent=2, default=str) + "\n")
    return out


def main() -> int:
    u = load_u()
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    result: dict = {
        "order": "Ben 14:45 ORDER1 Fri/Sun + ORDER2 lang/education all four",
        "started": datetime.now(LONDON).isoformat(timespec="seconds"),
        "channel": "@HistoryOfScienceYT",
        "do_not_touch": list(BANNED_IDS),
        "launch_day_15oct1805": "Fri Related → GHZDsiH7L7A",
        "videos": [],
    }
    u.ensure_chrome()
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(u.CDP)
        page = browser.contexts[0].new_page()
        page.set_viewport_size({"width": 1440, "height": 1100})
        # Ensure HOS via channel switcher (Related picker lesson)
        try:
            page.goto(
                "https://www.youtube.com/channel_switcher",
                wait_until="domcontentloaded",
                timeout=120000,
            )
            page.wait_for_timeout(2500)
            hit = page.evaluate(
                """() => {
                  const walk=(r,d=0)=>{
                    if(!r||d>45) return null;
                    for (const el of (r.querySelectorAll
                      ? r.querySelectorAll('ytd-account-item-renderer') : [])) {
                      const t=(el.innerText||'');
                      if (t.includes('History of Science')) {
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
        except Exception as e:
            result["switcher_err"] = f"{type(e).__name__}:{e}"
        hos = u.ensure_hos(page)
        result["hos"] = hos
        if not hos.get("ok"):
            (EV / "STUDIO_FIXES_RESULT.json").write_text(json.dumps(result, indent=2) + "\n")
            return 2

        print("==== live Shorts title check ====", flush=True)
        result["live_shorts"] = live_shorts_check(page, u)
        print(json.dumps(result["live_shorts"], indent=2), flush=True)

        for job in JOBS:
            print(f"==== {job['key']} {job['id']} ====", flush=True)
            try:
                item = process_video(page, u, job)
            except Exception as e:
                item = {
                    "key": job["key"],
                    "id": job["id"],
                    "ok": False,
                    "error": f"{type(e).__name__}:{e}",
                }
                page.screenshot(path=str(EV / f"{job['key']}_EXCEPTION.png"), full_page=True)
            result["videos"].append(item)
            print(
                json.dumps(
                    {
                        "key": item.get("key"),
                        "ok": item.get("ok"),
                        "final": item.get("final"),
                        "tags": item.get("final_tags"),
                        "selects": item.get("final_selects"),
                        "steps": [s.get("label") for s in item.get("steps") or []],
                    },
                    indent=2,
                    default=str,
                )[:2500],
                flush=True,
            )

        result["finished"] = datetime.now(LONDON).isoformat(timespec="seconds")
        result["ok"] = all(v.get("ok") for v in result["videos"])
        (EV / "STUDIO_FIXES_RESULT.json").write_text(
            json.dumps(result, indent=2, default=str) + "\n"
        )
        shutil.copy2(EV / "STUDIO_FIXES_RESULT.json", ART / "BEN_1445FIX_STUDIO_FIXES_RESULT.json")
        print(json.dumps(result, indent=2, default=str)[:8000])
        page.close()
        return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
