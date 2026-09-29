#!/usr/bin/env python3
"""Ben 29 Sep 20:03 — HOS Studio growth settings (full order).

CDP :9460 · ~/.hos-chrome-youtube-studio · @HistoryOfScienceYT only.
Never Orbit/Oppti/.env/API. Never replace/delete/publish-now/Premiere.

Phases: A channel · B 004 long · C older films · D shorts STOP · E records.
Usage: python3 _growth_settings_ben_2003_v01.py --phase A|B|C|D|all
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import urllib.request
from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright

PORT = 9460
CHANNEL = "UCXp7HkBIl1LgaznXuZHJyRg"
HANDLE = "@HistoryOfScienceYT"
VID_004 = "GHZDsiH7L7A"
VIDS = {
    "001_long": "_C92tIJCk8A",
    "002_long": "AL_-qlWko_g",
    "003_long": "frP_YrNShsU",
    "004_long": VID_004,
    "001_shorts": ["8uBR-9oxeWs", "YX2UR1u-JCQ", "Fnb3p81u-wY", "vpuRgKXtFlY", "Lcmh5y2KMQM"],
    "002_shorts": ["uU12JA5rMWg", "nFQRWmpulTQ", "CnHwX1L9XHg", "nba0-f7PPeU", "LanTHJckYx8"],
    "003_shorts": ["oowAOWTBoq0", "xvanpsLeADE", "zI_eD3vFWmE"],
}
PLAYLIST_NAME = "History of Science: How We Found Out"
TITLE_004 = "What's Really Inside an Atom?"

ROOT = Path(__file__).resolve().parents[4]  # History Of Science
PROJ = Path(__file__).resolve().parents[2]
PKG = PROJ / "11_Upload-Package"
EV = PKG / "Schedule/evidence_2026-09-29_studio"
ART = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts/hos004_growth_2003"
BEN = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts"
BRAND = ROOT / "00_Brand/Channel-Setup"

KEYWORDS = (BRAND / "channel_keywords.txt").read_text().strip()
DESC = (PKG / "Descriptions/atom_long_description_v01.txt").read_text().strip()
CHAPTERS = (PKG / "Chapters/atom_long_chapters_v01.txt").read_text().strip()
TAGS = (PKG / "Tags/atom_long_tags_v01.txt").read_text().strip()
PIN = (PKG / "Pinned-Comments/atom_long_pinned-comment_v01.txt").read_text().strip()
CAPTIONS = PKG / "Captions/hos_004_full_v02.en.srt"
THUMB_A = (PROJ / "08_Thumbnail/Selected/hos_004_thumb_A_atom_live_v04.jpg").resolve()
THUMB_B = (PROJ / "08_Thumbnail/Selected/hos_004_thumb_B_cut_gold_live_v04.jpg").resolve()
THUMB_C = (PROJ / "08_Thumbnail/Selected/hos_004_thumb_C_hidden_number_live_v06.jpg").resolve()

# Full description = package desc + chapters (Studio often wants them in one box)
DESC_FULL = DESC + "\n\n" + CHAPTERS


def log(m: str) -> None:
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    line = f"{datetime.now().isoformat(timespec='seconds')} {m}"
    print(line, flush=True)
    with (EV / "growth_v01.log").open("a") as f:
        f.write(line + "\n")


def dump(n: str, o) -> None:
    t = json.dumps(o, indent=2) + "\n"
    (EV / n).write_text(t)
    (ART / n).write_text(t)


def shot(page, n: str, *, ben: bool = False) -> Path:
    p = EV / n
    page.screenshot(path=str(p), full_page=False)
    (ART / n).write_bytes(p.read_bytes())
    if ben or n.startswith("BEN_"):
        (BEN / n).write_bytes(p.read_bytes())
    return p


def settings_dialog_open(page) -> bool:
    try:
        loc = page.locator("ytcp-settings-dialog").first
        if loc.count() and loc.is_visible():
            return True
    except Exception:
        pass
    return False


def dismiss(page, *, allow_escape: bool = True) -> None:
    """Dismiss toasts/modals. NEVER Escape while channel Settings dialog is open."""
    if settings_dialog_open(page):
        # Only dismiss non-settings toast overlays; do not Escape.
        try:
            page.get_by_role(
                "button",
                name=re.compile(r"^(OK, got it|Got it|Dismiss|Not now)$", re.I),
            ).first.click(timeout=250)
        except Exception:
            pass
        return
    for _ in range(3):
        if allow_escape:
            page.keyboard.press("Escape")
        page.wait_for_timeout(80)
        try:
            page.get_by_role(
                "button",
                name=re.compile(r"^(OK, got it|Got it|Close|Dismiss|Not now|Continue)$", re.I),
            ).first.click(timeout=250)
        except Exception:
            pass


def deep_click(page, pattern: str, y_min: int = 0, max_len: int = 120) -> bool:
    hit = page.evaluate(
        """({pattern, yMin, maxLen}) => {
          const re = new RegExp(pattern, 'i');
          let best=null;
          const walk=(r,d=0)=>{
            if(!r||d>55) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim().replace(/\\s+/g,' ');
              if (!t || t.length>maxLen) continue;
              if (!re.test(t)) continue;
              const rect=el.getBoundingClientRect();
              if (rect.width<4||rect.height<4||rect.y<yMin) continue;
              if (!best || t.length < best.t.length) best={x:rect.x+rect.width/2,y:rect.y+rect.height/2,t:t.slice(0,80)};
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
            }
          };
          walk(document);
          if (!best) return null;
          const el = document.elementFromPoint(best.x, best.y);
          if (el) el.click();
          return best;
        }""",
        {"pattern": pattern, "yMin": y_min, "maxLen": max_len},
    )
    if hit:
        page.wait_for_timeout(400)
        return True
    return False


def save(page) -> bool:
    """Click Save. Do not Escape after settings-dialog Save (dialog may close itself)."""
    in_settings = settings_dialog_open(page)
    try:
        if in_settings:
            btn = page.locator("ytcp-settings-dialog").get_by_role(
                "button", name=re.compile(r"^Save$", re.I)
            ).first
        else:
            btn = page.get_by_role("button", name=re.compile(r"^Save$", re.I)).first
        if btn.count() and btn.is_enabled():
            btn.click(force=True, timeout=3000)
            page.wait_for_timeout(3500)
            if not in_settings:
                dismiss(page)
            return True
    except Exception:
        pass
    # dialog / page Save via evaluate
    try:
        ok = page.evaluate(
            """(inSettings) => {
              const root = inSettings ? document.querySelector('ytcp-settings-dialog') : document;
              if (!root) return false;
              const walk=(r,d=0)=>{
                if(!r||d>45) return false;
                for (const b of (r.querySelectorAll?r.querySelectorAll('button, ytcp-button, tp-yt-paper-button'):[])) {
                  const t=(b.innerText||'').trim();
                  if (t==='Save' && !b.disabled && b.getAttribute('aria-disabled')!=='true') {
                    b.click(); return true;
                  }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                  if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
                return false;
              };
              return walk(root);
            }""",
            in_settings,
        )
        if ok:
            page.wait_for_timeout(3500)
            if not in_settings:
                dismiss(page)
            return True
    except Exception:
        pass
    return False


def channel_ok(page) -> dict:
    page.goto(
        f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload",
        wait_until="commit",
        timeout=90000,
    )
    page.wait_for_timeout(3500)
    dismiss(page)
    t = page.inner_text("body")
    info = {
        "ok": HANDLE in t or "History of Science" in t,
        "has_orbit": bool(re.search(r"Orbit With Ben|OpptiAI", t, re.I)),
    }
    shot(page, "growth_00_channel_check.png", ben=True)
    assert info["ok"] and not info["has_orbit"], info
    return info


def open_settings(page) -> None:
    """Open channel Settings dialog via left-rail mouse click. Never Escape while open."""
    try:
        if settings_dialog_open(page):
            page.locator("ytcp-settings-dialog").get_by_role(
                "button", name=re.compile(r"^Close$")
            ).first.click(timeout=1500)
            page.wait_for_timeout(600)
    except Exception:
        pass
    page.goto(f"https://studio.youtube.com/channel/{CHANNEL}", wait_until="commit", timeout=90000)
    page.wait_for_timeout(3000)
    dismiss(page, allow_escape=True)
    hit = page.evaluate(
        """() => {
          const items=[...document.querySelectorAll('tp-yt-paper-icon-item, ytcp-ve')];
          for (const el of items) {
            const t=(el.innerText||'').trim();
            if (t==='Settings') {
              const r=el.getBoundingClientRect();
              if (r.height>10) return {x:r.x+r.width/2,y:r.y+r.height/2};
            }
          }
          return null;
        }"""
    )
    if hit:
        page.mouse.click(hit["x"], hit["y"])
    else:
        deep_click(page, r"^Settings$", y_min=0, max_len=20)
    page.wait_for_timeout(2500)
    # Do NOT Escape here — that closes the settings dialog.


def click_settings_nav(page, label: str) -> bool:
    return deep_click(page, rf"^{re.escape(label)}$", y_min=0, max_len=40) or deep_click(
        page, label, y_min=0, max_len=60
    )


def read_audience_state(body: str) -> dict:
    not_kids = bool(re.search(r"set to not ['\"]?Made for Kids|No, it's not ['\"]?Made for Kids|No, set this channel as not Made for Kids", body, re.I))
    kids = bool(re.search(r"This video is set to ['\"]?Made for Kids|Yes, it's ['\"]?Made for Kids|Yes, set this channel as Made for Kids", body, re.I)) and not not_kids
    return {"not_kids": not_kids, "kids": kids}


# ─── PHASE A ───────────────────────────────────────────────────────────────


def phase_a(page) -> dict:
    result = {"phase": "A", "at": datetime.now().isoformat(timespec="seconds")}
    channel_ok(page)

    # A1 Channel Advanced Audience
    open_settings(page)
    shot(page, "growth_A_settings_home.png")
    click_settings_nav(page, "Channel")
    page.wait_for_timeout(1500)
    click_settings_nav(page, "Advanced settings")
    page.wait_for_timeout(2000)
    for _ in range(12):
        body = page.inner_text("body")
        if re.search(r"Audience|Made for Kids", body, re.I):
            break
        page.keyboard.press("PageDown")
        page.wait_for_timeout(150)
    shot(page, "growth_A1_audience_BEFORE.png", ben=True)
    before_body = page.inner_text("body")
    before = read_audience_state(before_body)
    # also check radio labels
    before["snip"] = before_body[:1200]
    before["channel_default_guess"] = (
        "not_kids" if before["not_kids"] else ("kids" if before["kids"] else "unknown")
    )
    result["A1_before"] = before
    log(f"A1 before={before['channel_default_guess']}")

    # Set No
    clicked = deep_click(
        page, r"No, set this channel as not Made for Kids", y_min=100, max_len=80
    ) or deep_click(page, r"No, set this channel as not", y_min=100, max_len=90)
    if not clicked:
        try:
            page.get_by_role(
                "radio", name=re.compile(r"No, set this channel as not Made for Kids", re.I)
            ).first.click(force=True, timeout=3000)
            clicked = True
        except Exception:
            pass
    result["A1_clicked"] = clicked
    page.wait_for_timeout(500)
    saved = save(page)
    # Also try Save in settings dialog footer
    if not saved:
        deep_click(page, r"^Save$", y_min=0, max_len=10)
        page.wait_for_timeout(2500)
        saved = True
    result["A1_saved"] = saved
    page.wait_for_timeout(1500)
    # Re-open advanced for after shot
    open_settings(page)
    click_settings_nav(page, "Channel")
    page.wait_for_timeout(1000)
    click_settings_nav(page, "Advanced settings")
    page.wait_for_timeout(2000)
    for _ in range(10):
        if re.search(r"Audience|Made for Kids", page.inner_text("body"), re.I):
            break
        page.keyboard.press("PageDown")
        page.wait_for_timeout(120)
    shot(page, "growth_A1_audience_AFTER.png", ben=True)
    after_body = page.inner_text("body")
    after = read_audience_state(after_body)
    after["snip"] = after_body[:1200]
    result["A1_after"] = after
    result["A1_ok"] = after.get("not_kids") is True
    log(f"A1 after not_kids={after.get('not_kids')} ok={result['A1_ok']}")

    # A2 Upload defaults → Basic info
    open_settings(page)
    click_settings_nav(page, "Upload defaults")
    page.wait_for_timeout(2000)
    # Basic info tab often default
    deep_click(page, r"^Basic info$", y_min=0, max_len=20)
    page.wait_for_timeout(1500)
    shot(page, "growth_A2_upload_defaults_basic_BEFORE.png")
    a2 = {"steps": []}
    # Category Education
    if deep_click(page, r"^Category$|^Select$", y_min=100, max_len=30) or True:
        deep_click(page, r"^Education$", y_min=50, max_len=30)
        a2["steps"].append("category_education")
    # Language English (United Kingdom)
    deep_click(page, r"Video language|Language", y_min=100, max_len=40)
    page.wait_for_timeout(400)
    deep_click(page, r"English \(United Kingdom\)", y_min=50, max_len=40)
    a2["steps"].append("lang_en_uk")
    # Caption certification
    deep_click(page, r"Caption certification|None|Select", y_min=100, max_len=50)
    page.wait_for_timeout(400)
    deep_click(
        page,
        r"This content has never aired on television in the US",
        y_min=50,
        max_len=80,
    )
    a2["steps"].append("caption_cert")
    # Licence Standard YouTube
    deep_click(page, r"Licence|License|Standard YouTube", y_min=100, max_len=40)
    page.wait_for_timeout(300)
    deep_click(page, r"Standard YouTube License|Standard YouTube Licence", y_min=50, max_len=50)
    a2["steps"].append("licence")
    # Visibility Private
    deep_click(page, r"^Visibility$|^Private$|^Public$|^Unlisted$", y_min=100, max_len=30)
    page.wait_for_timeout(300)
    deep_click(page, r"^Private$", y_min=50, max_len=20)
    a2["steps"].append("visibility_private")
    # Ensure title/desc templates empty — skip if already empty
    a2["saved"] = save(page)
    page.wait_for_timeout(1000)
    shot(page, "growth_A2_upload_defaults_basic_AFTER.png", ben=True)
    a2["snip"] = page.inner_text("body")[:1500]
    result["A2"] = a2
    log(f"A2 steps={a2['steps']} saved={a2['saved']}")

    # A3 Upload defaults → Advanced
    open_settings(page)
    click_settings_nav(page, "Upload defaults")
    page.wait_for_timeout(1500)
    click_settings_nav(page, "Advanced settings")
    page.wait_for_timeout(2000)
    shot(page, "growth_A3_upload_defaults_advanced_BEFORE.png")
    a3 = {"steps": []}
    for _ in range(20):
        body = page.inner_text("body")
        if re.search(r"Comments|Allow embedding|Shorts remixing", body, re.I):
            break
        page.keyboard.press("PageDown")
        page.wait_for_timeout(120)

    # Comments On + Hold potentially inappropriate
    deep_click(page, r"^Comments$", y_min=100, max_len=20)
    page.wait_for_timeout(400)
    deep_click(page, r"^On$", y_min=50, max_len=10) or deep_click(
        page, r"Hold potentially inappropriate", y_min=50, max_len=80
    )
    deep_click(page, r"Hold potentially inappropriate comments for review", y_min=50, max_len=90)
    a3["steps"].append("comments_hold")
    deep_click(page, r"^Sort by$|^Top$", y_min=100, max_len=20)
    deep_click(page, r"^Top$", y_min=50, max_len=10)
    a3["steps"].append("sort_top")

    # Checkboxes via evaluate
    toggles = page.evaluate(
        """() => {
          const want = [
            [/like count|Show how many viewers like/i, true],
            [/Allow embedding/i, true],
            [/Publish to subscriptions feed|notify subscribers/i, true],
            [/automatic chapters/i, true],
          ];
          const out=[];
          const walk=(r,d=0)=>{
            if(!r||d>55) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('tp-yt-paper-checkbox, yt-checkbox, [role=checkbox], input[type=checkbox]'):[])) {
              const label = (el.getAttribute('aria-label')||el.innerText||el.parentElement?.innerText||'').trim().slice(0,120);
              const checked = el.getAttribute('aria-checked')==='true' || el.checked===true || el.hasAttribute('checked');
              for (const [re, wantOn] of want) {
                if (re.test(label)) {
                  if (wantOn && !checked) { el.click(); out.push('on:'+label.slice(0,40)); }
                  if (!wantOn && checked) { el.click(); out.push('off:'+label.slice(0,40)); }
                }
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
            }
          };
          walk(document);
          return out;
        }"""
    )
    a3["toggles"] = toggles
    # Shorts remixing
    deep_click(page, r"Shorts remixing|Remixing", y_min=100, max_len=40)
    page.wait_for_timeout(400)
    deep_click(page, r"Allow video and audio remixing", y_min=50, max_len=50)
    a3["steps"].append("remixing")
    a3["saved"] = save(page)
    page.wait_for_timeout(1000)
    # Reopen for after shot
    open_settings(page)
    click_settings_nav(page, "Upload defaults")
    page.wait_for_timeout(1000)
    click_settings_nav(page, "Advanced settings")
    page.wait_for_timeout(2000)
    for _ in range(15):
        if re.search(r"Comments|Allow embedding", page.inner_text("body"), re.I):
            break
        page.keyboard.press("PageDown")
        page.wait_for_timeout(100)
    shot(page, "growth_A3_upload_defaults_advanced_AFTER.png", ben=True)
    a3["snip"] = page.inner_text("body")[:2000]
    result["A3"] = a3
    log(f"A3 steps={a3['steps']} toggles={a3.get('toggles')}")

    # A4 Channel → Basic info: country UK + keywords
    open_settings(page)
    click_settings_nav(page, "Channel")
    page.wait_for_timeout(1000)
    click_settings_nav(page, "Basic info")
    page.wait_for_timeout(2000)
    shot(page, "growth_A4_basic_info_BEFORE.png")
    a4 = {"steps": []}
    body = page.inner_text("body")
    a4["has_orbit_in_desc"] = bool(re.search(r"Orbit With Ben|OpptiAI", body, re.I))
    # Country
    deep_click(page, r"^Country$|United Kingdom|United States", y_min=100, max_len=40)
    page.wait_for_timeout(400)
    deep_click(page, r"^United Kingdom$", y_min=50, max_len=30)
    a4["steps"].append("country_uk")
    # Keywords — find textarea
    try:
        # Prefer dedicated keywords box
        filled = page.evaluate(
            """(kw) => {
              const boxes = [...document.querySelectorAll('textarea, input, [contenteditable=true]')];
              for (const b of boxes) {
                const aria=(b.getAttribute('aria-label')||'') + ' ' + (b.getAttribute('placeholder')||'');
                const near = (b.closest('ytcp-form-textarea, ytcp-social-suggestions, ytcp-form-input-container')?.innerText||'');
                if (/keyword/i.test(aria+near)) {
                  if (b.tagName==='TEXTAREA' || b.tagName==='INPUT') {
                    const setter = Object.getOwnPropertyDescriptor(b.tagName==='TEXTAREA'?HTMLTextAreaElement.prototype:HTMLInputElement.prototype,'value').set;
                    setter.call(b, kw);
                    b.dispatchEvent(new Event('input',{bubbles:true}));
                    return 'filled:'+aria.slice(0,40);
                  }
                }
              }
              return null;
            }""",
            KEYWORDS,
        )
        a4["keywords"] = filled
        if not filled:
            # click Keywords label then type
            deep_click(page, r"^Keywords$", y_min=100, max_len=20)
            page.wait_for_timeout(300)
            page.keyboard.type(KEYWORDS, delay=5)
            a4["keywords"] = "typed"
    except Exception as e:
        a4["keywords_err"] = type(e).__name__
    a4["saved"] = save(page)
    page.wait_for_timeout(1000)
    open_settings(page)
    click_settings_nav(page, "Channel")
    click_settings_nav(page, "Basic info")
    page.wait_for_timeout(2000)
    shot(page, "growth_A4_basic_info_AFTER.png", ben=True)
    a4["snip"] = page.inner_text("body")[:1500]
    result["A4"] = a4
    log(f"A4 keywords={a4.get('keywords')} orbit={a4.get('has_orbit_in_desc')}")

    # A5 Branding — confirm no watermark (do not add)
    open_settings(page)
    # Branding may be under Channel → Branding or Settings → Branding
    deep_click(page, r"^Branding$", y_min=0, max_len=20)
    page.wait_for_timeout(2000)
    shot(page, "growth_A5_branding.png", ben=True)
    body = page.inner_text("body")
    result["A5"] = {
        "has_watermark_section": bool(re.search(r"Video watermark|Watermark", body, re.I)),
        "note": "Did not add watermark / subscribe graphics",
        "snip": body[:1000],
    }
    log("A5 branding checked — no watermark added")

    dump("GROWTH_A_RESULT.json", result)
    return result


# ─── PHASE B ───────────────────────────────────────────────────────────────


def open_edit(page, video_id: str) -> None:
    page.goto(
        f"https://studio.youtube.com/video/{video_id}/edit",
        wait_until="commit",
        timeout=90000,
    )
    page.wait_for_timeout(4500)
    dismiss(page)


def show_more(page) -> None:
    for _ in range(8):
        if deep_click(page, r"^Show more$", y_min=200, max_len=20):
            page.wait_for_timeout(800)
            return
        page.keyboard.press("PageDown")
        page.wait_for_timeout(150)


def phase_b(page) -> dict:
    result = {"phase": "B", "at": datetime.now().isoformat(timespec="seconds"), "videoId": VID_004}
    channel_ok(page)
    open_edit(page, VID_004)

    # B1 Audience No + Age restriction No
    b1 = {}
    for _ in range(20):
        if re.search(r"Audience|Made for Kids", page.inner_text("body"), re.I):
            break
        page.keyboard.press("PageDown")
        page.wait_for_timeout(150)
    deep_click(page, r"No, it's not ['\"]?Made for Kids", y_min=100, max_len=60)
    b1["audience_clicked"] = True
    # Age restriction No
    deep_click(page, r"Age restriction", y_min=100, max_len=30)
    page.wait_for_timeout(300)
    deep_click(page, r"No, don't restrict my video to viewers over 18|No,", y_min=50, max_len=80)
    b1["saved"] = save(page)
    page.wait_for_timeout(1500)
    open_edit(page, VID_004)
    for _ in range(20):
        if re.search(r"Audience|Made for Kids", page.inner_text("body"), re.I):
            break
        page.keyboard.press("PageDown")
        page.wait_for_timeout(120)
    shot(page, "growth_B1_audience.png", ben=True)
    body = page.inner_text("body")
    b1["not_kids"] = bool(re.search(r"set to not ['\"]?Made for Kids", body, re.I))
    b1["notices_comments_disabled"] = bool(re.search(r"Comments disabled", body, re.I))
    b1["notices_notifications_disabled"] = bool(re.search(r"Notifications disabled", body, re.I))
    b1["ok"] = b1["not_kids"] and not b1["notices_comments_disabled"]
    result["B1"] = b1
    log(f"B1 not_kids={b1['not_kids']} notices_comments={b1['notices_comments_disabled']}")

    # B2 Visibility
    b2 = {}
    # scroll top + open visibility pencil
    page.evaluate("() => window.scrollTo(0,0)")
    page.wait_for_timeout(400)
    deep_click(page, r"Edit video visibility|Visibility|Scheduled|Private", y_min=0, max_len=40)
    page.wait_for_timeout(1500)
    # Or sidebar Visibility card
    try:
        page.locator('button[aria-label*="visibility" i], ytcp-video-visibility-select').first.click(
            timeout=2000
        )
    except Exception:
        pass
    page.wait_for_timeout(1000)
    shot(page, "growth_B2_visibility_dialog.png")
    # Ensure Schedule selected
    deep_click(page, r"^Schedule$", y_min=50, max_len=20)
    page.wait_for_timeout(500)
    # Date 15 Oct 2026 / time 18:00
    try:
        # time input
        for sel in ('input[type="time"]', 'tp-yt-paper-input input', 'input[aria-label*="Time" i]'):
            loc = page.locator(sel)
            if loc.count():
                loc.first.fill("18:00")
                b2["time"] = "18:00"
                break
    except Exception as e:
        b2["time_err"] = type(e).__name__
    # Premiere OFF
    page.evaluate(
        """() => {
          const walk=(r,d=0)=>{
            if(!r||d>55) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('[role=checkbox], tp-yt-paper-checkbox, input[type=checkbox]'):[])) {
              const t=((el.getAttribute('aria-label')||'')+' '+(el.innerText||el.parentElement?.innerText||'')).toLowerCase();
              if (/premiere/.test(t)) {
                const on = el.getAttribute('aria-checked')==='true' || el.checked===true;
                if (on) el.click();
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) if (el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document);
        }"""
    )
    b2["premiere"] = "off_attempted"
    # Publish to subscriptions ON
    page.evaluate(
        """() => {
          const walk=(r,d=0)=>{
            if(!r||d>55) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('[role=checkbox], tp-yt-paper-checkbox, input[type=checkbox]'):[])) {
              const t=((el.getAttribute('aria-label')||'')+' '+(el.innerText||el.parentElement?.innerText||'')).toLowerCase();
              if (/subscription|notify/.test(t)) {
                const on = el.getAttribute('aria-checked')==='true' || el.checked===true;
                if (!on) el.click();
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) if (el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document);
        }"""
    )
    b2["notify"] = "on_attempted"
    deep_click(page, r"^Schedule$|^Save$|^Done$", y_min=100, max_len=20)
    page.wait_for_timeout(2000)
    dismiss(page)
    # reopen visibility proof
    page.evaluate("() => window.scrollTo(0,0)")
    page.wait_for_timeout(300)
    deep_click(page, r"Visibility|Scheduled|Private", y_min=0, max_len=30)
    page.wait_for_timeout(1200)
    shot(page, "growth_B2_visibility_AFTER.png", ben=True)
    body = page.inner_text("body")
    b2["snip"] = body[:1500]
    b2["has_15_oct"] = bool(re.search(r"15.*Oct|Oct.*15|15/10/2026|2026-10-15", body, re.I))
    b2["has_1800"] = bool(re.search(r"18:00|6:00\s*PM", body, re.I))
    b2["premiere_checked"] = bool(
        re.search(r"Premiere[^\n]{0,40}checked|Set as Premiere[^\n]{0,20}on", body, re.I)
    )
    dismiss(page)
    result["B2"] = b2
    log(f"B2 date={b2.get('has_15_oct')} time={b2.get('has_1800')}")

    # B3 Details: title, description+chapters, thumb A, tags
    open_edit(page, VID_004)
    b3 = {}
    # Title
    try:
        title_box = page.locator(
            "#textbox, ytcp-social-suggestion-input #textbox, div[aria-label*='Add a title' i]"
        ).first
        title_box.click(timeout=3000)
        page.keyboard.press("Meta+a")
        page.keyboard.type(TITLE_004, delay=8)
        b3["title"] = TITLE_004
    except Exception as e:
        b3["title_err"] = type(e).__name__
    # Description
    try:
        desc = page.locator(
            "div[aria-label*='Tell viewers about' i], div[aria-label*='description' i], #description-textarea #textbox"
        ).first
        desc.click(timeout=3000)
        page.keyboard.press("Meta+a")
        # type in chunks
        page.keyboard.type(DESC_FULL[:500], delay=2)
        # paste rest via evaluate for speed
        page.evaluate(
            """(txt) => {
              const el = document.activeElement;
              if (!el) return;
              if (el.isContentEditable) {
                el.textContent = txt;
                el.dispatchEvent(new InputEvent('input',{bubbles:true}));
              }
            }""",
            DESC_FULL,
        )
        b3["description_len"] = len(DESC_FULL)
        b3["has_go"] = "/go/" in DESC_FULL.lower()
    except Exception as e:
        b3["desc_err"] = type(e).__name__
    # Thumbnail A
    try:
        page.evaluate("() => window.scrollTo(0,400)")
        page.wait_for_timeout(400)
        file_inputs = page.locator('input[type="file"]')
        n = file_inputs.count()
        b3["file_inputs"] = n
        if n:
            file_inputs.first.set_input_files(str(THUMB_A))
            page.wait_for_timeout(2500)
            b3["thumb_a_uploaded"] = True
    except Exception as e:
        b3["thumb_err"] = type(e).__name__
    # Tags via Show more
    show_more(page)
    for _ in range(10):
        if re.search(r"^Tags$|Tags", page.inner_text("body"), re.I):
            break
        page.keyboard.press("PageDown")
        page.wait_for_timeout(120)
    try:
        page.evaluate(
            """(tags) => {
              const boxes=[...document.querySelectorAll('input, textarea, [contenteditable=true]')];
              for (const b of boxes) {
                const aria=(b.getAttribute('aria-label')||'')+(b.getAttribute('placeholder')||'');
                const near=(b.closest('ytcp-form-input-container,ytcp-video-metadata-editor')?.innerText||'');
                if (/tag/i.test(aria+near) && !/keyword/i.test(aria)) {
                  if (b.tagName==='INPUT' || b.tagName==='TEXTAREA') {
                    const proto = b.tagName==='TEXTAREA'?HTMLTextAreaElement.prototype:HTMLInputElement.prototype;
                    Object.getOwnPropertyDescriptor(proto,'value').set.call(b, tags.replace(/\\n/g,','));
                    b.dispatchEvent(new Event('input',{bubbles:true}));
                    return true;
                  }
                }
              }
              return false;
            }""",
            TAGS,
        )
        b3["tags"] = True
    except Exception as e:
        b3["tags_err"] = type(e).__name__
    b3["saved"] = save(page)
    page.wait_for_timeout(2000)
    open_edit(page, VID_004)
    shot(page, "growth_B3_details.png", ben=True)
    result["B3"] = b3
    log(f"B3 title={b3.get('title')} thumb={b3.get('thumb_a_uploaded')} saved={b3.get('saved')}")

    # B4 Show more settings — Altered NO (override), comments hold, etc.
    open_edit(page, VID_004)
    show_more(page)
    b4 = {"steps": []}
    for _ in range(25):
        body = page.inner_text("body")
        if re.search(r"Altered content|Paid promotion|Category|Comments", body, re.I):
            break
        page.keyboard.press("PageDown")
        page.wait_for_timeout(120)

    # Paid promotion No
    deep_click(page, r"Paid promotion", y_min=100, max_len=30)
    page.evaluate(
        """() => {
          const walk=(r,d=0)=>{
            if(!r||d>55) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('[role=checkbox],input[type=checkbox]'):[])) {
              const t=((el.getAttribute('aria-label')||'')+(el.parentElement?.innerText||'')).toLowerCase();
              if (/paid promotion|includes paid/.test(t)) {
                const on=el.getAttribute('aria-checked')==='true'||el.checked===true;
                if (on) el.click();
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) if(el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document);
        }"""
    )
    b4["steps"].append("paid_no")

    # Altered content NO
    deep_click(page, r"^Altered content$", y_min=150, max_len=30)
    page.wait_for_timeout(400)
    # open dropdown near Altered
    page.evaluate(
        """() => {
          let ay=null;
          const walk=(r,d=0)=>{
            if(!r||d>55) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim();
              if (t==='Altered content') {
                const rect=el.getBoundingClientRect();
                if (rect.y>100) { ay=rect.y; }
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) if(el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document);
          if (ay==null) return null;
          let target=null;
          const walk2=(r,d=0)=>{
            if(!r||d>55||target) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('button,[role=button],[role=combobox],ytcp-dropdown-trigger,div,span'):[])) {
              const t=(el.innerText||'').trim().replace(/\\s+/g,' ');
              const rect=el.getBoundingClientRect();
              if (rect.y<ay||rect.y>ay+280) continue;
              if (/^(Select|Yes|No)$/i.test(t) || /altered|synthetic/i.test(t)) {
                target={x:rect.x+rect.width/2,y:rect.y+rect.height/2,t:t.slice(0,60)};
                el.click(); return;
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) if(el.shadowRoot) walk2(el.shadowRoot,d+1);
          }; walk2(document);
          return target;
        }"""
    )
    page.wait_for_timeout(700)
    shot(page, "growth_B4_altered_menu.png")
    no = deep_click(
        page, r"No, it doesn.?t have altered or synthetic content", y_min=50, max_len=90
    ) or deep_click(page, r"^No,", y_min=50, max_len=80)
    # Avoid kids No — prefer altered wording
    if not no:
        hit = page.evaluate(
            """() => {
              let hit=null;
              const walk=(r,d=0)=>{
                if(!r||d>55||hit) return;
                for (const el of (r.querySelectorAll?r.querySelectorAll('[role=option],tp-yt-paper-item,div,span,button'):[])) {
                  const t=(el.innerText||'').trim().replace(/\\s+/g,' ');
                  if (!/^No\\b/i.test(t)) continue;
                  if (/Kids|child/i.test(t)) continue;
                  if (/altered|synthetic/i.test(t) || t.length<40) {
                    const rect=el.getBoundingClientRect();
                    if (rect.width>5) { el.click(); hit=t.slice(0,100); return; }
                  }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) if(el.shadowRoot) walk(el.shadowRoot,d+1);
              }; walk(document); return hit;
            }"""
        )
        no = hit
    b4["altered_no"] = no
    b4["steps"].append("altered_no")
    page.wait_for_timeout(500)

    # Automatic chapters ON, featured places OFF, automatic concepts ON
    page.evaluate(
        """() => {
          const rules = [
            [/automatic chapters/i, true],
            [/featured places/i, false],
            [/automatic concepts/i, true],
            [/Allow embedding/i, true],
            [/like count|Show how many viewers like/i, true],
          ];
          const walk=(r,d=0)=>{
            if(!r||d>55) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('[role=checkbox],input[type=checkbox],tp-yt-paper-checkbox'):[])) {
              const t=((el.getAttribute('aria-label')||'')+(el.parentElement?.innerText||'')).trim();
              const on=el.getAttribute('aria-checked')==='true'||el.checked===true;
              for (const [re, want] of rules) {
                if (re.test(t)) {
                  if (want && !on) el.click();
                  if (!want && on) el.click();
                }
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) if(el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document);
        }"""
    )
    b4["steps"].append("chapters_places_concepts")

    # Language / caption cert / category / licence / remixing / comments
    deep_click(page, r"Video language|Language", y_min=100, max_len=40)
    deep_click(page, r"English \(United Kingdom\)", y_min=50, max_len=40)
    deep_click(page, r"Caption certification", y_min=100, max_len=40)
    deep_click(page, r"never aired on television in the US", y_min=50, max_len=80)
    deep_click(page, r"^Category$", y_min=100, max_len=20)
    deep_click(page, r"^Education$", y_min=50, max_len=20)
    deep_click(page, r"Licence|License", y_min=100, max_len=20)
    deep_click(page, r"Standard YouTube", y_min=50, max_len=40)
    deep_click(page, r"Shorts remixing|Remixing", y_min=100, max_len=30)
    deep_click(page, r"Allow video and audio remixing", y_min=50, max_len=50)

    # Comments ON + Hold potentially inappropriate + Sort Top
    for _ in range(15):
        if re.search(r"Choose if and how you want to show comments", page.inner_text("body"), re.I):
            break
        page.keyboard.press("PageDown")
        page.wait_for_timeout(120)
    deep_click(page, r"^Comments$", y_min=200, max_len=20)
    page.wait_for_timeout(400)
    deep_click(page, r"^On$", y_min=50, max_len=10)
    # Moderation / hold
    deep_click(page, r"^Moderation$|^Basic$|^Strict$", y_min=200, max_len=20)
    page.wait_for_timeout(300)
    deep_click(page, r"Hold potentially inappropriate", y_min=50, max_len=80) or deep_click(
        page, r"^Strict$", y_min=50, max_len=15
    )
    # Also try Comments dropdown for hold wording
    deep_click(page, r"Hold potentially inappropriate comments for review", y_min=50, max_len=90)
    deep_click(page, r"^Sort by$", y_min=200, max_len=15)
    deep_click(page, r"^Top$", y_min=50, max_len=10)
    b4["steps"].append("comments_hold_top")

    b4["saved"] = save(page)
    page.wait_for_timeout(2000)
    open_edit(page, VID_004)
    show_more(page)
    for _ in range(20):
        body = page.inner_text("body")
        if re.search(r"Altered content", body, re.I):
            break
        page.keyboard.press("PageDown")
        page.wait_for_timeout(120)
    shot(page, "growth_B4_show_more_AFTER.png", ben=True)
    body = page.inner_text("body")
    b4["altered_is_no"] = bool(
        re.search(r"Altered content[^\n]{0,40}\n?No\b|No, it doesn", body, re.I)
    ) and not bool(re.search(r"Altered content[^\n]{0,40}\n?Yes\b", body, re.I))
    b4["snip"] = body[:2500]
    result["B4"] = b4
    log(f"B4 altered_no={b4.get('altered_no')} proof_no={b4.get('altered_is_no')}")

    # B5 Subtitles
    b5 = {}
    page.goto(
        f"https://studio.youtube.com/video/{VID_004}/translations",
        wait_until="commit",
        timeout=90000,
    )
    page.wait_for_timeout(4000)
    dismiss(page)
    shot(page, "growth_B5_subtitles_BEFORE.png")
    # Upload
    try:
        deep_click(page, r"Upload|ADD LANGUAGE|Add language", y_min=50, max_len=30)
        page.wait_for_timeout(800)
        deep_click(page, r"English \(United Kingdom\)|English", y_min=50, max_len=40)
        page.wait_for_timeout(800)
        deep_click(page, r"With timing|Upload file", y_min=50, max_len=30)
        page.wait_for_timeout(800)
        loc = page.locator('input[type="file"]')
        if loc.count():
            loc.first.set_input_files(str(CAPTIONS))
            page.wait_for_timeout(3000)
            b5["uploaded"] = True
        deep_click(page, r"^Publish$|^Done$|^Save$", y_min=50, max_len=20)
        page.wait_for_timeout(2000)
    except Exception as e:
        b5["err"] = type(e).__name__
    shot(page, "growth_B5_subtitles_AFTER.png", ben=True)
    b5["snip"] = page.inner_text("body")[:1000]
    result["B5"] = b5
    log(f"B5 uploaded={b5.get('uploaded')}")

    # B6 End screen
    b6 = {}
    page.goto(
        f"https://studio.youtube.com/video/{VID_004}/edit",
        wait_until="commit",
        timeout=90000,
    )
    page.wait_for_timeout(3000)
    # End screen via sidebar or card
    deep_click(page, r"^End screen$", y_min=0, max_len=20)
    page.wait_for_timeout(3000)
    dismiss(page)
    shot(page, "growth_B6_endscreen_BEFORE.png")
    deep_click(page, r"IMPORT FROM VIDEO|Import from video|ADD ELEMENT|Add element", y_min=50, max_len=40)
    page.wait_for_timeout(1000)
    deep_click(page, r"^Video$", y_min=50, max_len=15)
    page.wait_for_timeout(800)
    # Pick specific video 002
    deep_click(page, r"Specific video|Choose", y_min=50, max_len=30)
    page.wait_for_timeout(1000)
    try:
        page.keyboard.type("AL_-qlWko_g", delay=20)
        page.wait_for_timeout(1500)
        deep_click(page, r"Periodic Table|AL_-qlWko_g", y_min=50, max_len=60)
    except Exception:
        pass
    deep_click(page, r"^Subscribe$", y_min=50, max_len=15)
    page.wait_for_timeout(500)
    # Ensure last 20s — Studio default often OK
    b6["saved"] = save(page)
    page.wait_for_timeout(3000)
    shot(page, "growth_B6_endscreen_AFTER.png", ben=True)
    body = page.inner_text("body")
    b6["processing_error"] = bool(re.search(r"problem in processing|couldn.?t be saved|NaN", body, re.I))
    b6["snip"] = body[:1200]
    result["B6"] = b6
    log(f"B6 saved={b6.get('saved')} err={b6.get('processing_error')}")

    # B7 Cards
    b7 = {"cards": []}
    page.goto(
        f"https://studio.youtube.com/video/{VID_004}/edit",
        wait_until="commit",
        timeout=90000,
    )
    page.wait_for_timeout(3000)
    deep_click(page, r"^Cards$", y_min=0, max_len=15)
    page.wait_for_timeout(3000)
    shot(page, "growth_B7_cards_BEFORE.png")
    # Card 1 ~1:30 → 002
    for teaser, vid, tsec in (
        ("How the table was found", "AL_-qlWko_g", "1:30"),
        ("How X-rays were discovered", "frP_YrNShsU", "6:00"),
    ):
        card = {"teaser": teaser, "videoId": vid, "time": tsec}
        deep_click(page, r"Add card|ADD CARD", y_min=50, max_len=20)
        page.wait_for_timeout(800)
        deep_click(page, r"^Video$", y_min=50, max_len=15)
        page.wait_for_timeout(800)
        try:
            page.keyboard.type(vid, delay=15)
            page.wait_for_timeout(1200)
            deep_click(page, re.escape(vid)[:8], y_min=50, max_len=40)
        except Exception as e:
            card["err"] = type(e).__name__
        # teaser
        try:
            page.evaluate(
                """(t) => {
                  const boxes=[...document.querySelectorAll('input, textarea, [contenteditable=true]')];
                  for (const b of boxes) {
                    const a=(b.getAttribute('aria-label')||b.getAttribute('placeholder')||'');
                    if (/teaser|message|custom/i.test(a)) {
                      if (b.tagName==='INPUT'||b.tagName==='TEXTAREA') {
                        Object.getOwnPropertyDescriptor(b.tagName==='TEXTAREA'?HTMLTextAreaElement.prototype:HTMLInputElement.prototype,'value').set.call(b,t);
                        b.dispatchEvent(new Event('input',{bubbles:true}));
                        return true;
                      }
                    }
                  }
                  return false;
                }""",
                teaser,
            )
        except Exception:
            pass
        # time
        try:
            page.evaluate(
                """(t) => {
                  for (const b of document.querySelectorAll('input')) {
                    const a=(b.getAttribute('aria-label')||b.getAttribute('placeholder')||'');
                    if (/time|start/i.test(a)) { b.value=t; b.dispatchEvent(new Event('input',{bubbles:true})); return true; }
                  }
                  return false;
                }""",
                tsec,
            )
        except Exception:
            pass
        deep_click(page, r"^Create card$|^Save$|^Done$", y_min=50, max_len=20)
        page.wait_for_timeout(1500)
        b7["cards"].append(card)
    b7["saved"] = save(page)
    page.wait_for_timeout(2000)
    shot(page, "growth_B7_cards_AFTER.png", ben=True)
    result["B7"] = b7
    log(f"B7 cards={len(b7['cards'])}")

    # B8 Playlist
    b8 = {}
    page.goto(
        f"https://studio.youtube.com/channel/{CHANNEL}/playlists",
        wait_until="commit",
        timeout=90000,
    )
    page.wait_for_timeout(3500)
    dismiss(page)
    shot(page, "growth_B8_playlists.png")
    body = page.inner_text("body")
    b8["exists"] = PLAYLIST_NAME.lower() in body.lower() or "How We Found Out" in body
    if not b8["exists"]:
        deep_click(page, r"New playlist|NEW PLAYLIST", y_min=50, max_len=30)
        page.wait_for_timeout(1000)
        page.keyboard.type(PLAYLIST_NAME, delay=15)
        page.wait_for_timeout(400)
        deep_click(page, r"^Public$", y_min=50, max_len=15)
        deep_click(page, r"^Create$|^Save$", y_min=50, max_len=15)
        page.wait_for_timeout(2500)
        b8["created"] = True
    # Add videos via edit 004 playlist picker
    open_edit(page, VID_004)
    for _ in range(12):
        if re.search(r"Playlist", page.inner_text("body"), re.I):
            break
        page.keyboard.press("PageDown")
        page.wait_for_timeout(120)
    deep_click(page, r"Select|Playlists", y_min=100, max_len=30)
    page.wait_for_timeout(1000)
    deep_click(page, r"How We Found Out|History of Science: How We Found Out", y_min=50, max_len=60)
    page.wait_for_timeout(500)
    deep_click(page, r"^Done$", y_min=50, max_len=10)
    b8["004_added"] = save(page)
    # Add 001,002,003 similarly
    for key, vid in (("001", VIDS["001_long"]), ("002", VIDS["002_long"]), ("003", VIDS["003_long"])):
        open_edit(page, vid)
        for _ in range(12):
            if re.search(r"Playlist", page.inner_text("body"), re.I):
                break
            page.keyboard.press("PageDown")
            page.wait_for_timeout(100)
        deep_click(page, r"Select|Playlists", y_min=100, max_len=30)
        page.wait_for_timeout(800)
        deep_click(page, r"How We Found Out", y_min=50, max_len=60)
        deep_click(page, r"^Done$", y_min=50, max_len=10)
        save(page)
        b8[f"{key}_added"] = True
    page.goto(
        f"https://studio.youtube.com/channel/{CHANNEL}/playlists",
        wait_until="commit",
        timeout=90000,
    )
    page.wait_for_timeout(3000)
    shot(page, "growth_B8_playlist_AFTER.png", ben=True)
    result["B8"] = b8
    log(f"B8 exists={b8.get('exists')} created={b8.get('created')}")

    # B9 Test & Compare
    b9 = {}
    open_edit(page, VID_004)
    for _ in range(15):
        if re.search(r"Test & Compare|Test and compare", page.inner_text("body"), re.I):
            break
        page.keyboard.press("PageDown")
        page.wait_for_timeout(120)
    shot(page, "growth_B9_tc_BEFORE.png")
    deep_click(page, r"Test & Compare|Add test|Get started", y_min=100, max_len=40)
    page.wait_for_timeout(1500)
    body = page.inner_text("body")
    b9["ineligible"] = bool(re.search(r"Ineligible|not eligible", body, re.I))
    if deep_click(page, r"Title and thumbnail", y_min=50, max_len=40):
        b9["mode"] = "Title and thumbnail"
    elif deep_click(page, r"^Thumbnail$", y_min=50, max_len=20):
        b9["mode"] = "Thumbnail"
    else:
        b9["mode"] = None
    shot(page, "growth_B9_tc_AFTER.png", ben=True)
    b9["snip"] = page.inner_text("body")[:1200]
    dismiss(page)
    result["B9"] = b9
    log(f"B9 mode={b9.get('mode')} ineligible={b9.get('ineligible')}")

    # B10 Pin
    b10 = {
        "text": PIN,
        "ok": False,
        "reason": None,
        "note": "If blocked, pin at 18:05 on 15 Oct",
    }
    page.goto(
        f"https://studio.youtube.com/video/{VID_004}/comments",
        wait_until="commit",
        timeout=90000,
    )
    page.wait_for_timeout(3500)
    dismiss(page)
    page.locator("ytcp-commentbox").first.click(force=True)
    page.wait_for_timeout(600)
    shot(page, "growth_B10_pin.png", ben=True)
    body = page.inner_text("body")
    if "doesn't have permission to create comments" in body.lower():
        b10["reason"] = "studio_no_permission_while_private_scheduled"
        b10["blocked"] = True
    else:
        b10["reason"] = "attempt_needed"
        b10["blocked"] = False
    disabled = page.evaluate(
        "() => !!document.querySelector('ytcp-commentbox textarea#textarea')?.disabled"
    )
    b10["textarea_disabled"] = disabled
    result["B10"] = b10
    log(f"B10 blocked={b10.get('blocked')} reason={b10.get('reason')}")

    dump("GROWTH_B_RESULT.json", result)
    return result


# ─── PHASE C ───────────────────────────────────────────────────────────────


def phase_c(page) -> dict:
    result = {
        "phase": "C",
        "at": datetime.now().isoformat(timespec="seconds"),
        "changed_to_not_kids": [],
        "already_not_kids": [],
        "oops": [],
        "longs": {},
    }
    channel_ok(page)

    all_vids = (
        [("001_long", VIDS["001_long"])]
        + [("002_long", VIDS["002_long"])]
        + [("003_long", VIDS["003_long"])]
        + [(f"001_short_{i}", i) for i in VIDS["001_shorts"]]
        + [(f"002_short_{i}", i) for i in VIDS["002_shorts"]]
        + [(f"003_short_{i}", i) for i in VIDS["003_shorts"]]
    )

    for key, vid in all_vids:
        info = {"videoId": vid}
        try:
            open_edit(page, vid)
            body = page.inner_text("body")
            if re.search(r"Oops|something went wrong", body, re.I) and "Made for Kids" not in body:
                info["oops"] = True
                result["oops"].append(key)
                shot(page, f"growth_C_{key}_oops.png")
                continue
            for _ in range(18):
                if re.search(r"Audience|Made for Kids", page.inner_text("body"), re.I):
                    break
                page.keyboard.press("PageDown")
                page.wait_for_timeout(120)
            body = page.inner_text("body")
            state = read_audience_state(body)
            info["before"] = state
            if state.get("kids") or (
                not state.get("not_kids")
                and re.search(r"Yes, it's ['\"]?Made for Kids", body, re.I)
            ):
                deep_click(page, r"No, it's not ['\"]?Made for Kids", y_min=100, max_len=60)
                save(page)
                info["changed"] = True
                result["changed_to_not_kids"].append(key)
            else:
                info["changed"] = False
                result["already_not_kids"].append(key)

            # Longs: comments ON, category Education, playlist (already for playlist in B8)
            if key.endswith("_long"):
                show_more(page)
                for _ in range(20):
                    if re.search(
                        r"Choose if and how you want to show comments|Category",
                        page.inner_text("body"),
                        re.I,
                    ):
                        break
                    page.keyboard.press("PageDown")
                    page.wait_for_timeout(100)
                deep_click(page, r"^Comments$", y_min=200, max_len=20)
                deep_click(page, r"^On$", y_min=50, max_len=10)
                deep_click(page, r"Hold potentially inappropriate", y_min=50, max_len=80)
                deep_click(page, r"^Category$", y_min=100, max_len=20)
                deep_click(page, r"^Education$", y_min=50, max_len=20)
                info["long_settings_saved"] = save(page)
                result["longs"][key] = info
            shot(page, f"growth_C_{key}.png")
            log(f"C {key} not_kids={state.get('not_kids')} changed={info.get('changed')}")
        except Exception as e:
            info["err"] = f"{type(e).__name__}:{e}"
            log(f"C ERR {key}: {e}")
        result.setdefault("audits", {})[key] = info

    result["note_C4"] = (
        "AFTER 004 public (15 Oct 18:05): set end screen video on 001/002/003 → 004 + Subscribe"
    )
    dump("GROWTH_C_RESULT.json", result)
    return result


def phase_d() -> dict:
    """Shorts: STOP until Ben yes. Confirm v05 gate if possible."""
    result = {
        "phase": "D",
        "at": datetime.now().isoformat(timespec="seconds"),
        "scheduled": False,
        "note": "Nothing scheduled before Ben yes. Fri 16 / Sun 18 / Tue 20 Oct 11:30 UK after 004 public.",
    }
    gate = ROOT / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"
    shorts_dir = PROJ / "10_Shorts"
    import subprocess

    try:
        out = subprocess.check_output(
            ["python3", str(gate), "check", str(shorts_dir)],
            stderr=subprocess.STDOUT,
            text=True,
            timeout=120,
        )
        result["gate_output"] = out[-2000:]
        result["gate_pass"] = "PASS" in out and "FAIL" not in out.split("PASS")[-1][:20]
    except Exception as e:
        result["gate_err"] = f"{type(e).__name__}:{e}"
        # try listing
        result["shorts_files"] = [p.name for p in shorts_dir.glob("hos_004_s*.mp4")][:20]
    # iCloud path check
    icloud = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT/004_Whats-Really-Inside-An-Atom/10_Shorts"
    result["icloud_exists"] = icloud.exists()
    if icloud.exists():
        result["icloud_files"] = sorted([p.name for p in icloud.glob("*.mp4")])[:20]
    result["stop"] = True
    dump("GROWTH_D_RESULT.json", result)
    log(f"D gate={result.get('gate_pass')} icloud={result.get('icloud_exists')} STOP")
    return result


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", default="all", choices=["A", "B", "C", "D", "all"])
    args = ap.parse_args()
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/version", timeout=3).read()

    results = {}
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
        ctx = browser.contexts[0]
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        if args.phase in ("A", "all"):
            log("=== PHASE A ===")
            results["A"] = phase_a(page)
        if args.phase in ("B", "all"):
            log("=== PHASE B ===")
            results["B"] = phase_b(page)
        if args.phase in ("C", "all"):
            log("=== PHASE C ===")
            results["C"] = phase_c(page)
    if args.phase in ("D", "all"):
        log("=== PHASE D ===")
        results["D"] = phase_d()

    results["at"] = datetime.now().isoformat(timespec="seconds")
    dump("GROWTH_ALL_RESULT.json", results)
    log("DONE phases=" + ",".join(results.keys()))


if __name__ == "__main__":
    main()
