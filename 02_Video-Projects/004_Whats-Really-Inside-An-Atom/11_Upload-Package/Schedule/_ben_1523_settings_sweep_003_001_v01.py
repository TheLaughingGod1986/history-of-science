#!/usr/bin/env python3
"""Ben 15:23 settings sweep — 003 then 001 FIRST.

1) Finish Lister Related save in flight (clV6E10NLPw → _C92tIJCk8A).
2) BEFORE report+screenshots for 003 frP_YrNShsU then 001 _C92tIJCk8A
   (Audience, age restriction, visibility, Premiere, notices, Analytics Reach).
3) Apply playbook settings (not kids, no age restrict, Altered YES, comments ON).
4) Confirm Fri Short 29bpGAI0wb8 title = What happens if you keep cutting gold in half?
HOS only. Do not touch CUu8k38iAMc.
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
    / "evidence_2026-09-30_settings_sweep"
)
ART = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts"
LONDON = ZoneInfo("Europe/London")
HOS = "UCXp7HkBIl1LgaznXuZHJyRg"
BANNED = {"CUu8k38iAMc"}

VIDS = [
    {
        "key": "003",
        "id": "frP_YrNShsU",
        "title": "How Did We Discover X-rays?",
    },
    {
        "key": "001",
        "id": "_C92tIJCk8A",
        "title": "How Did We Discover Germs?",
    },
]
FRI_ID = "29bpGAI0wb8"
FRI_TITLE = "What happens if you keep cutting gold in half?"
LISTER = "clV6E10NLPw"
RELATED_LONG = "_C92tIJCk8A"
RELATED_TITLE = "How Did We Discover Germs?"


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
    shutil.copy2(p, ART / name)
    return p


def ensure_hos_session(page, u) -> dict:
    """Channel switcher → HOS, then Studio HOS (fixes Related picker Oppti deleg)."""
    out: dict = {}
    try:
        page.goto(
            "https://www.youtube.com/channel_switcher",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(3000)
        hit = page.evaluate(
            """() => {
              const walk=(r,d=0)=>{
                if(!r||d>45) return null;
                for (const el of (r.querySelectorAll
                  ? r.querySelectorAll('ytd-account-item-renderer') : [])) {
                  const t=(el.innerText||'');
                  if (t.includes('History of Science')) {
                    const b=el.getBoundingClientRect();
                    return {x:b.x+b.width/2,y:b.y+b.height/2,t:t.replace(/\\s+/g,' ').trim().slice(0,80)};
                  }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                  if (el.shadowRoot) { const h=walk(el.shadowRoot,d+1); if(h) return h; }
                return null;
              };
              return walk(document);
            }"""
        )
        out["switcher"] = hit
        if hit:
            page.mouse.click(hit["x"], hit["y"])
            page.wait_for_timeout(4000)
    except Exception as e:
        out["switcher_err"] = f"{type(e).__name__}:{e}"
    hos = u.ensure_hos(page)
    out["hos"] = hos
    return out


def related_chunk(page) -> str:
    t = page.inner_text("body")
    if "Related video" not in t:
        return ""
    return t.split("Related video", 1)[-1][:220]


def finish_lister_related(page, u) -> dict:
    out: dict = {"vid": LISTER}
    page.goto(
        f"https://studio.youtube.com/video/{LISTER}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3000)
    u.dismiss(page)
    if any(b in page.url for b in BANNED):
        return {"error": "banned"}
    chunk0 = related_chunk(page)
    out["before"] = chunk0
    if RELATED_TITLE in chunk0 and "hitch" not in chunk0[:80].lower() and "None" not in chunk0[:40]:
        out["ok"] = True
        out["status"] = "already"
        return out
    try:
        page.locator("ytcp-shorts-content-links-picker").first.scroll_into_view_if_needed()
        page.locator("ytcp-shorts-content-links-picker").first.click(force=True)
        page.wait_for_timeout(7000)
    except Exception as e:
        out["open_err"] = f"{type(e).__name__}:{e}"
        return out
    shot(page, "LISTER_related_picker.png")
    # Scroll to long title and click largest matching card under 180h
    picked = None
    for _ in range(20):
        cards = page.evaluate(
            """(title) => {
              const hits=[];
              const walk=(r,d=0)=>{
                if(!r||d>55) return;
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                  const tx=(el.innerText||'').replace(/\\s+/g,' ').trim();
                  if (tx !== title && !tx.startsWith(title)) continue;
                  if (/hitch|shadow|pond|flask/i.test(tx)) continue;
                  const b=el.getBoundingClientRect();
                  if (b.width>100 && b.height>50 && b.height<190 && b.y>120 && b.y<980)
                    hits.push({t:tx.slice(0,80),x:b.x+b.width/2,y:b.y+b.height/2,w:Math.round(b.width),h:Math.round(b.height)});
                  if (el.shadowRoot) walk(el.shadowRoot,d+1);
                }
              };
              walk(document.querySelector('ytcp-video-pick-dialog')||document);
              hits.sort((a,b)=> (b.w*b.h)-(a.w*a.h));
              return hits.slice(0,8);
            }""",
            RELATED_TITLE,
        )
        if cards:
            page.mouse.click(cards[0]["x"], cards[0]["y"])
            page.wait_for_timeout(1500)
            picked = cards[0]
            break
        page.evaluate(
            """() => {
              const dlg=document.querySelector('ytcp-video-pick-dialog');
              if(!dlg) return;
              const walk=(r,d=0)=>{
                if(!r||d>40) return;
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                  if (el.scrollHeight>el.clientHeight+40) el.scrollTop+=240;
                  if (el.shadowRoot) walk(el.shadowRoot,d+1);
                }
              }; walk(dlg);
            }"""
        )
        page.wait_for_timeout(350)
    out["picked"] = picked
    save = page.get_by_role("button", name=re.compile(r"^Save$", re.I))
    if save.count() and save.first.is_enabled():
        save.first.click()
        page.wait_for_timeout(2800)
        out["saved"] = True
    else:
        out["saved"] = False
        try:
            page.keyboard.press("Escape")
        except Exception:
            pass
        out["save2"] = u.page_save(page)
    page.goto(
        f"https://studio.youtube.com/video/{LISTER}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3000)
    chunk = related_chunk(page)
    out["after"] = chunk
    out["ok"] = (
        RELATED_TITLE in chunk
        and "hitch" not in chunk[:80].lower()
        and "None" not in chunk[:40]
    )
    shot(page, "LISTER_related_after.png")
    return out


def read_radios(page, patterns: list[str]) -> list[dict]:
    return page.evaluate(
        """(patterns) => {
          const out=[];
          const walk=(r,d=0)=>{
            if(!r||d>50) return;
            for (const el of (r.querySelectorAll
              ? r.querySelectorAll('[role=radio],tp-yt-paper-radio-button') : [])) {
              const lab=(el.getAttribute('aria-label')||el.innerText||'').replace(/\\s+/g,' ').trim();
              if (!lab) continue;
              if (!patterns.some(p => new RegExp(p,'i').test(lab))) continue;
              out.push({
                lab: lab.slice(0,80),
                aria: el.getAttribute('aria-checked'),
                checked: el.getAttribute('aria-checked')==='true' || el.hasAttribute('checked'),
              });
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
          };
          walk(document);
          return out;
        }""",
        patterns,
    )


def open_visibility(page, u) -> dict:
    info: dict = {}
    try:
        opened = u.open_vis(page)
        info["opened"] = opened
        page.wait_for_timeout(1200)
        try:
            info["snip"] = page.locator(
                "ytcp-video-visibility-select, tp-yt-paper-dialog, ytcp-uploads-dialog"
            ).first.inner_text()[:1200]
        except Exception:
            info["snip"] = page.inner_text("body")[:1200]
        info["premiere"] = bool(
            re.search(r"Set as Premiere|Premiere", info["snip"] or "", re.I)
        )
        info["premiere_on"] = bool(
            re.search(
                r"Set as Premiere[^\n]{0,80}(checked|on)|Premiere.*selected",
                info["snip"] or "",
                re.I,
            )
        )
        # Better: look for checked premiere checkbox
        prem = page.evaluate(
            """() => {
              const out=[];
              const walk=(r,d=0)=>{
                if(!r||d>45) return;
                for (const el of (r.querySelectorAll
                  ? r.querySelectorAll('[role=checkbox],tp-yt-paper-checkbox,input') : [])) {
                  const lab=(el.getAttribute('aria-label')||el.innerText||'').trim();
                  if (/Premiere/i.test(lab)) {
                    out.push({
                      lab:lab.slice(0,60),
                      aria:el.getAttribute('aria-checked'),
                      checked: el.getAttribute('aria-checked')==='true' || el.checked===true,
                    });
                  }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                  if (el.shadowRoot) walk(el.shadowRoot,d+1);
              }; walk(document); return out;
            }"""
        )
        info["premiere_boxes"] = prem
        info["visibility_public"] = bool(re.search(r"\bPublic\b", info["snip"] or ""))
        info["visibility_private"] = bool(re.search(r"\bPrivate\b", info["snip"] or ""))
        info["visibility_unlisted"] = bool(re.search(r"\bUnlisted\b", info["snip"] or ""))
        info["visibility_scheduled"] = bool(re.search(r"Schedule", info["snip"] or "", re.I))
    except Exception as e:
        info["err"] = f"{type(e).__name__}:{e}"
    return info


def close_dialogs(page) -> None:
    for _ in range(3):
        try:
            page.keyboard.press("Escape")
            page.wait_for_timeout(400)
        except Exception:
            pass


def audit_before(page, u, job: dict) -> dict:
    """BEFORE-only: no settings changes."""
    vid = job["id"]
    key = job["key"]
    out: dict = {
        "key": key,
        "id": vid,
        "titleWanted": job["title"],
        "phase": "BEFORE",
        "ts": datetime.now(LONDON).isoformat(timespec="seconds"),
    }
    page.goto(
        f"https://studio.youtube.com/video/{vid}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(4000)
    u.dismiss(page)
    if any(b in page.url for b in BANNED):
        out["error"] = "banned_url"
        return out
    body = page.inner_text("body")
    out["url"] = page.url
    out["title_ok"] = job["title"][:24].lower() in body.lower()
    out["chip"] = u.visibility_chip(page)
    # Notices / restrictions on Details
    notices = []
    for pat, label in (
        (r"Comments are turned off|Comments disabled", "comments_disabled"),
        (r"Notifications are turned off|Notifications disabled", "notifications_disabled"),
        (r"Limited features|some features.*unavailable", "limited_features"),
        (r"age.?restrict|Age-restricted|Age restricted", "age_restricted_notice"),
        (r"Made for Kids", "made_for_kids_mention"),
        (r"Copyright|Content ID|strike", "copyright_notice"),
        (r"processing error|Trouble saving|Something went wrong|Oops", "studio_error"),
        (r"Restricted mode|may not be suitable", "restricted_mode"),
    ):
        if re.search(pat, body, re.I):
            notices.append(label)
    out["notices"] = notices
    # Audience radios
    out["audience_radios"] = read_radios(
        page,
        [
            r"Made for Kids",
            r"not ['\"]?Made for Kids",
            r"set this channel as",
        ],
    )
    out["audience_banner_not_kids"] = bool(
        re.search(r"set to not\s*['\"]?Made for Kids", body, re.I)
    )
    kids_yes = any(
        r.get("checked") and re.search(r"^Yes", r.get("lab", ""), re.I)
        for r in out["audience_radios"]
    )
    kids_no = any(
        r.get("checked") and re.search(r"^No", r.get("lab", ""), re.I)
        for r in out["audience_radios"]
    )
    out["made_for_kids"] = True if kids_yes else (False if kids_no else None)
    # Age restriction section
    out["age_radios"] = read_radios(
        page,
        [r"age.?restrict", r"Yes, restrict", r"No, don't restrict", r"Don't restrict"],
    )
    # Scroll to age restriction if present
    page.evaluate(
        """() => {
          const walk=(r,d=0)=>{
            if(!r||d>45) return false;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim();
              if (/^Age restriction/i.test(t) && t.length<40) {
                el.scrollIntoView({block:'center'}); return true;
              }
              if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
            }
            return false;
          }; walk(document);
        }"""
    )
    page.wait_for_timeout(400)
    out["age_radios"] = read_radios(
        page,
        [r"age.?restrict", r"Yes, restrict", r"No, don't restrict", r"Don't restrict", r"restrict my video"],
    )
    age_yes = any(
        r.get("checked") and re.search(r"Yes", r.get("lab", ""), re.I)
        for r in out["age_radios"]
    )
    age_no = any(
        r.get("checked") and re.search(r"No", r.get("lab", ""), re.I)
        for r in out["age_radios"]
    )
    out["age_restricted"] = True if age_yes else (False if age_no else None)
    # AI
    out["ai_radios"] = read_radios(page, [r"AI was used", r"AI wasn't used"])
    # Premiere mention on details
    out["premiere_word_on_details"] = bool(re.search(r"Premiere[d]?", body[:3500]))
    # Visibility dialog
    page.evaluate("window.scrollTo(0,0)")
    page.wait_for_timeout(300)
    shot(page, f"{key}_BEFORE_details_top.png")
    # Audience region shot
    page.evaluate(
        """() => {
          const walk=(r,d=0)=>{
            if(!r||d>45) return false;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim();
              if (/^Audience$/i.test(t)) { el.scrollIntoView({block:'center'}); return true; }
              if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
            }
            return false;
          }; walk(document);
        }"""
    )
    page.wait_for_timeout(400)
    shot(page, f"{key}_BEFORE_audience.png")
    vis = open_visibility(page, u)
    out["visibility"] = vis
    shot(page, f"{key}_BEFORE_visibility.png")
    close_dialogs(page)
    # Analytics Reach → traffic sources
    page.goto(
        f"https://studio.youtube.com/video/{vid}/analytics/tab-reach/period-default",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(5000)
    u.dismiss(page)
    # Try clicking Traffic source if needed
    try:
        page.get_by_text(re.compile(r"^Traffic source$", re.I)).first.click(timeout=3000)
        page.wait_for_timeout(2500)
    except Exception:
        pass
    # Also try Reach tab
    try:
        page.get_by_role("tab", name=re.compile(r"Reach", re.I)).first.click(timeout=2000)
        page.wait_for_timeout(2000)
    except Exception:
        pass
    abody = page.inner_text("body")
    out["analytics_url"] = page.url
    out["analytics_snip"] = abody[:2500]
    # Extract traffic source-ish lines
    lines = [ln.strip() for ln in abody.splitlines() if ln.strip()]
    traffic = []
    capture = False
    for ln in lines:
        if re.search(r"Traffic source", ln, re.I):
            capture = True
        if capture:
            traffic.append(ln)
            if len(traffic) > 40:
                break
        if re.search(
            r"Browse features|YouTube search|Suggested|Shorts|External|Direct|Playlist|Channel pages|Notifications",
            ln,
            re.I,
        ):
            if ln not in traffic:
                traffic.append(ln)
    out["traffic_lines"] = traffic[:40]
    shot(page, f"{key}_BEFORE_analytics_reach.png")
    # Scroll for more traffic table
    for _ in range(4):
        page.mouse.wheel(0, 900)
        page.wait_for_timeout(200)
    shot(page, f"{key}_BEFORE_analytics_reach_scrolled.png")
    return out


def click_radio_by_label(page, pattern: str) -> str | None:
    return page.evaluate(
        """(pattern) => {
          const re=new RegExp(pattern,'i');
          let hit=null;
          const walk=(r,d=0)=>{
            if(!r||d>50||hit) return;
            for (const el of (r.querySelectorAll
              ? r.querySelectorAll('[role=radio],tp-yt-paper-radio-button') : [])) {
              const lab=(el.getAttribute('aria-label')||el.innerText||'').replace(/\\s+/g,' ').trim();
              if (!re.test(lab)) continue;
              const b=el.getBoundingClientRect();
              if (b.width>10 && b.height>10) { hit={lab:lab.slice(0,80),x:b.x+b.width/2,y:b.y+b.height/2}; }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
          };
          walk(document);
          return hit;
        }""",
        pattern,
    )


def apply_settings(page, u, job: dict) -> dict:
    """Apply playbook: not kids, no age restrict, Altered YES, comments ON. One control per save."""
    vid = job["id"]
    key = job["key"]
    out: dict = {
        "key": key,
        "id": vid,
        "phase": "APPLY",
        "steps": [],
        "ts": datetime.now(LONDON).isoformat(timespec="seconds"),
    }
    page.goto(
        f"https://studio.youtube.com/video/{vid}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3500)
    u.dismiss(page)

    def save_once(label: str) -> dict:
        s = u.page_save(page)
        page.wait_for_timeout(2000)
        # Re-read audience after every save
        aud = read_radios(page, [r"Made for Kids", r"not ['\"]?Made for Kids"])
        step = {"label": label, "save": s, "audience_after": aud}
        out["steps"].append(step)
        return step

    # 1) Audience not kids
    hit = click_radio_by_label(page, r"^No, it.?s not.?Made for Kids")
    if hit:
        page.mouse.click(hit["x"], hit["y"])
        page.wait_for_timeout(600)
        save_once("audience_not_kids")
        out["audience_click"] = hit
    else:
        out["audience_click"] = "already_or_missing"
        out["steps"].append({"label": "audience_skip", "radios": read_radios(page, [r"Made for Kids"])})

    # 2) Age restriction No
    page.evaluate(
        """() => {
          const walk=(r,d=0)=>{
            if(!r||d>45) return false;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim();
              if (/Age restriction/i.test(t) && t.length<60) {
                el.scrollIntoView({block:'center'}); return true;
              }
              if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
            }
            return false;
          }; walk(document);
        }"""
    )
    page.wait_for_timeout(500)
    hit = click_radio_by_label(
        page, r"No, don.?t restrict|Don't restrict my video|No.*restrict"
    )
    if hit:
        page.mouse.click(hit["x"], hit["y"])
        page.wait_for_timeout(600)
        save_once("age_not_restricted")
        out["age_click"] = hit
    else:
        out["age_click"] = "already_or_missing"

    # 3) Altered YES
    page.evaluate(
        """() => {
          const walk=(r,d=0)=>{
            if(!r||d>45) return false;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim();
              if (/Altered content|AI use|synthetic/i.test(t) && t.length<80) {
                el.scrollIntoView({block:'center'}); return true;
              }
              if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
            }
            return false;
          }; walk(document);
        }"""
    )
    page.wait_for_timeout(500)
    hit = click_radio_by_label(page, r"^Yes, AI was used$")
    if not hit:
        hit = click_radio_by_label(page, r"Yes, AI was used")
    if hit:
        page.mouse.click(hit["x"], hit["y"])
        page.wait_for_timeout(600)
        save_once("altered_yes")
        out["ai_click"] = hit
    else:
        out["ai_click"] = "already_or_missing"

    # 4) Comments ON if visible
    try:
        page.evaluate(
            """() => {
              const walk=(r,d=0)=>{
                if(!r||d>45) return false;
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                  const t=(el.innerText||'').trim();
                  if (/^Comments$/i.test(t) && t.length<20) {
                    el.scrollIntoView({block:'center'}); return true;
                  }
                  if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
                }
                return false;
              }; walk(document);
            }"""
        )
        page.wait_for_timeout(400)
        # Look for comments toggle / On
        clicked = page.evaluate(
            """() => {
              const walk=(r,d=0)=>{
                if(!r||d>45) return null;
                for (const el of (r.querySelectorAll
                  ? r.querySelectorAll('[role=radio],tp-yt-paper-radio-button,button') : [])) {
                  const lab=(el.getAttribute('aria-label')||el.innerText||'').trim();
                  if (/^On$/i.test(lab) || /Allow all comments/i.test(lab) || /Comments.*On/i.test(lab)) {
                    const b=el.getBoundingClientRect();
                    if (b.width>20 && b.height>16 && b.y>200)
                      return {lab:lab.slice(0,40),x:b.x+b.width/2,y:b.y+b.height/2};
                  }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                  if (el.shadowRoot) { const h=walk(el.shadowRoot,d+1); if(h) return h; }
                return null;
              }; return walk(document);
            }"""
        )
        if clicked:
            page.mouse.click(clicked["x"], clicked["y"])
            page.wait_for_timeout(500)
            save_once("comments_on")
            out["comments_click"] = clicked
        else:
            out["comments_click"] = "already_or_missing"
    except Exception as e:
        out["comments_err"] = f"{type(e).__name__}:{e}"

    # Final AFTER shots
    page.goto(
        f"https://studio.youtube.com/video/{vid}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3500)
    u.dismiss(page)
    body = page.inner_text("body")
    out["audience_final"] = read_radios(page, [r"Made for Kids"])
    out["ai_final"] = read_radios(page, [r"AI was used", r"AI wasn't used"])
    out["age_final"] = read_radios(page, [r"restrict"])
    out["chip"] = u.visibility_chip(page)
    out["banner_not_kids"] = bool(re.search(r"set to not\s*['\"]?Made for Kids", body, re.I))
    page.evaluate(
        """() => {
          const walk=(r,d=0)=>{
            if(!r||d>45) return false;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim();
              if (/^Audience$/i.test(t)) { el.scrollIntoView({block:'center'}); return true; }
              if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
            }
            return false;
          }; walk(document);
        }"""
    )
    page.wait_for_timeout(400)
    shot(page, f"{key}_AFTER_audience.png")
    vis = open_visibility(page, u)
    out["visibility_after"] = vis
    shot(page, f"{key}_AFTER_visibility.png")
    close_dialogs(page)
    out["ok"] = out.get("banner_not_kids") or any(
        r.get("checked") and re.search(r"^No", r.get("lab", ""), re.I)
        for r in out.get("audience_final") or []
    )
    return out


def fri_title_check_and_rename(page, u) -> dict:
    out: dict = {"id": FRI_ID, "wanted": FRI_TITLE}
    page.goto(
        f"https://studio.youtube.com/video/{FRI_ID}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3500)
    u.dismiss(page)
    body = page.inner_text("body")
    out["has_wanted"] = FRI_TITLE in body
    out["has_old"] = "How small can you cut gold?" in body
    shot(page, "FRI_title_BEFORE.png")
    if out["has_wanted"]:
        out["ok"] = True
        out["status"] = "already_renamed"
        return out
    # Rename title field
    try:
        # Prefer title textbox
        filled = page.evaluate(
            """(title) => {
              const walk=(r,d=0)=>{
                if(!r||d>50) return null;
                for (const el of (r.querySelectorAll
                  ? r.querySelectorAll('textarea,input,#textbox,[contenteditable=true]') : [])) {
                  const lab=(el.getAttribute('aria-label')||el.getAttribute('id')||'');
                  const near=(el.closest && (el.closest('ytcp-social-suggestions-textbox,ytcp-mention-textbox,ytcp-video-metadata-editor')||{}).tagName)||'';
                  const t=(el.value||el.innerText||'').trim();
                  if (/title/i.test(lab) || /TITLE/i.test(near) || (t && t.length<120 && /cut gold|cutting gold/i.test(t))) {
                    el.focus();
                    if (el.value !== undefined) { el.value=''; el.dispatchEvent(new Event('input',{bubbles:true})); el.value=title; el.dispatchEvent(new Event('input',{bubbles:true})); }
                    else { el.innerText=title; el.dispatchEvent(new InputEvent('input',{bubbles:true})); }
                    return {lab:lab.slice(0,40), near, old:t.slice(0,80)};
                  }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                  if (el.shadowRoot) { const h=walk(el.shadowRoot,d+1); if(h) return h; }
                return null;
              }; return walk(document);
            }""",
            FRI_TITLE,
        )
        out["fill_js"] = filled
        # Also try Playwright fill on title
        box = page.locator(
            "#textbox, ytcp-social-suggestions-textbox #textbox, [aria-label*='Title' i]"
        ).first
        if box.count():
            box.click(force=True)
            page.keyboard.press("Meta+a")
            page.keyboard.type(FRI_TITLE, delay=15)
            out["typed"] = True
        page.wait_for_timeout(800)
        save = u.page_save(page)
        out["save"] = save
        page.wait_for_timeout(2500)
    except Exception as e:
        out["err"] = f"{type(e).__name__}:{e}"
    page.goto(
        f"https://studio.youtube.com/video/{FRI_ID}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3000)
    body = page.inner_text("body")
    out["has_wanted_after"] = FRI_TITLE in body
    out["ok"] = out["has_wanted_after"]
    out["audience_after"] = read_radios(page, [r"Made for Kids"])
    shot(page, "FRI_title_AFTER.png")
    return out


def main() -> int:
    u = load_u()
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    result: dict = {
        "order": "Ben 15:23 — 003 then 001 FIRST; before-report then apply; Fri rename confirm",
        "started": datetime.now(LONDON).isoformat(timespec="seconds"),
        "channel": "@HistoryOfScienceYT",
        "do_not_touch": list(BANNED),
    }
    u.ensure_chrome()
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(u.CDP)
        ctx = browser.contexts[0]
        page = ctx.new_page()
        page.set_viewport_size({"width": 1440, "height": 1100})
        result["session"] = ensure_hos_session(page, u)
        if not result["session"].get("hos", {}).get("ok"):
            (EV / "SWEEP_RESULT.json").write_text(json.dumps(result, indent=2) + "\n")
            print(json.dumps(result, indent=2)[:2000])
            return 2

        # 1) Finish Lister Related
        print("==== finish Lister Related ====", flush=True)
        result["lister_related"] = finish_lister_related(page, u)
        print(json.dumps(result["lister_related"], indent=2)[:800], flush=True)

        # 2) BEFORE audits — 003 then 001
        befores = []
        for job in VIDS:
            print(f"==== BEFORE {job['key']} {job['id']} ====", flush=True)
            before = audit_before(page, u, job)
            befores.append(before)
            (EV / f"{job['key']}_BEFORE.json").write_text(
                json.dumps(before, indent=2, default=str) + "\n"
            )
            print(
                f"{job['key']} kids={before.get('made_for_kids')} age={before.get('age_restricted')} "
                f"chip={before.get('chip')} notices={before.get('notices')} "
                f"traffic={before.get('traffic_lines', [])[:8]}",
                flush=True,
            )
        result["before"] = befores
        (EV / "BEFORE_REPORT.json").write_text(
            json.dumps({"before": befores, "ts": result["started"]}, indent=2, default=str)
            + "\n"
        )
        shutil.copy2(EV / "BEFORE_REPORT.json", ART / "BEN_1523_BEFORE_REPORT.json")

        # 3) Apply settings — 003 then 001
        applies = []
        for job in VIDS:
            print(f"==== APPLY {job['key']} {job['id']} ====", flush=True)
            applied = apply_settings(page, u, job)
            applies.append(applied)
            (EV / f"{job['key']}_AFTER.json").write_text(
                json.dumps(applied, indent=2, default=str) + "\n"
            )
            print(json.dumps(applied, indent=2, default=str)[:1200], flush=True)
        result["apply"] = applies

        # 4) Fri rename confirm
        print("==== Fri title ====", flush=True)
        result["fri"] = fri_title_check_and_rename(page, u)
        print(json.dumps(result["fri"], indent=2, default=str)[:1000], flush=True)

        result["finished"] = datetime.now(LONDON).isoformat(timespec="seconds")
        result["ok"] = all(a.get("ok") for a in applies) and result["fri"].get("ok")
        (EV / "SWEEP_RESULT.json").write_text(
            json.dumps(result, indent=2, default=str) + "\n"
        )
        shutil.copy2(EV / "SWEEP_RESULT.json", ART / "BEN_1523_SWEEP_RESULT.json")
        # Copy key shots to artifacts with BEN_1523 prefix
        for p in EV.glob("*_BEFORE_*.png"):
            shutil.copy2(p, ART / f"BEN_1523_{p.name}")
        for p in EV.glob("*_AFTER_*.png"):
            shutil.copy2(p, ART / f"BEN_1523_{p.name}")
        for p in EV.glob("FRI_*.png"):
            shutil.copy2(p, ART / f"BEN_1523_{p.name}")
        print(json.dumps(result, indent=2, default=str)[:8000])
        page.close()
        return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
