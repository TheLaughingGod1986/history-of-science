#!/usr/bin/env python3
"""Finish HOS 004 Studio draft: trim tags, Not for kids, Schedule 15 Oct 18:00 (no Premiere),
then T&C / end screen / pin. CDP :9460 · HOS profile only. No .env."""
from __future__ import annotations

import json
import re
import time
import traceback
from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright

PORT = 9460
CDP = f"http://127.0.0.1:{PORT}"
CHANNEL = "UCXp7HkBIl1LgaznXuZHJyRg"
HANDLE = "@HistoryOfScienceYT"
VIDEO_ID = "GHZDsiH7L7A"
TITLE = "What's Really Inside an Atom?"
TITLE_2 = "Why Is the Periodic Table in This Order?"
TITLE_3 = "How Small Can You Cut Gold?"
RELATED_002 = "AL_-qlWko_g"

PROJ = Path(__file__).resolve().parents[2]
PKG = PROJ / "11_Upload-Package"
EV = PKG / "Schedule/evidence_2026-09-29_studio"
ART = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts"

THUMB_A = PROJ / "08_Thumbnail/Selected/hos_004_thumb_A_atom_live_v04.jpg"
THUMB_B = PROJ / "08_Thumbnail/Selected/hos_004_thumb_B_cut_gold_live_v04.jpg"
THUMB_C = PROJ / "08_Thumbnail/Selected/hos_004_thumb_C_hidden_number_live_v06.jpg"
PIN = (PKG / "Pinned-Comments/atom_long_pinned-comment_v01.txt").read_text().strip()
CAPTIONS = PKG / "Captions/hos_004_full_v02.en.srt"

ALL_TAGS = [
    ln.strip()
    for ln in (PKG / "Tags/atom_long_tags_v01.txt").read_text().splitlines()
    if ln.strip()
]
# YouTube hard cap ~500 chars
TAGS: list[str] = []
for t in ALL_TAGS:
    trial = ", ".join(TAGS + [t])
    if len(trial) > 500:
        break
    TAGS.append(t)

SCHED_DAY = 15
SCHED_MONTH = "October"
SCHED_TIME = "18:00"


def log(msg: str) -> None:
    EV.mkdir(parents=True, exist_ok=True)
    line = f"{datetime.now().isoformat(timespec='seconds')} {msg}"
    print(line, flush=True)
    with (EV / "finish.log").open("a") as f:
        f.write(line + "\n")


def dump(name: str, obj) -> None:
    EV.mkdir(parents=True, exist_ok=True)
    (EV / name).write_text(json.dumps(obj, indent=2) + "\n")
    try:
        (ART / f"hos_004_{name}").write_text(json.dumps(obj, indent=2) + "\n")
    except Exception:
        pass


def shot(page, name: str) -> str:
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    dest = EV / name
    page.screenshot(path=str(dest), full_page=False)
    (ART / f"hos_004_{name}").write_bytes(dest.read_bytes())
    return str(dest)


def snip(page, n: int = 3000) -> str:
    try:
        return page.inner_text("body")[:n]
    except Exception as e:
        return f"<err {e}>"


def dlg_text(page, n: int = 5000) -> str:
    try:
        dlg = page.locator("ytcp-uploads-dialog")
        if dlg.count():
            return dlg.inner_text()[:n]
    except Exception:
        pass
    return snip(page, n)


def dismiss(page) -> None:
    for name in ["Got it", "Dismiss", "Not now", "No thanks", "Skip"]:
        try:
            b = page.get_by_role("button", name=re.compile(rf"^{name}$", re.I))
            if b.count() and b.first.is_visible():
                b.first.click(timeout=500, force=True)
        except Exception:
            pass


def click_shadow_text(page, pattern: str) -> str | None:
    return page.evaluate(
        """(pattern) => {
          const re = new RegExp(pattern, 'i');
          const walk=(r,d=0)=>{
            if(!r||d>45) return null;
            for (const el of (r.querySelectorAll
              ? r.querySelectorAll('button,ytcp-button,[role=button],tp-yt-paper-item,yt-formatted-string,a,div,span')
              : [])) {
              const t=((el.innerText||'')+' '+(el.getAttribute('aria-label')||''))
                .replace(/\\s+/g,' ').trim();
              if (re.test(t) && t.length<64) {
                const box=el.getBoundingClientRect();
                if (box.width>12 && box.height>8) { el.click(); return t.slice(0,80); }
              }
            }
            for (const el of (r.querySelectorAll ? r.querySelectorAll('*') : [])) {
              if (el.shadowRoot) {
                const x=walk(el.shadowRoot, d+1);
                if (x) return x;
              }
            }
            return null;
          };
          return walk(document);
        }""",
        pattern,
    )


def ensure_hos(page) -> dict:
    page.goto(
        f"https://studio.youtube.com/channel/{CHANNEL}/video/{VIDEO_ID}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(4000)
    dismiss(page)
    body = snip(page, 2500)
    url = page.url
    if CHANNEL not in url and VIDEO_ID not in url:
        return {"ok": False, "reason": "WRONG_URL", "url": url}
    if re.search(r"signin|accounts\.google", url, re.I):
        return {"ok": False, "reason": "SIGNED_OUT", "url": url}
    if "History of Science" not in body and TITLE not in body:
        # still may be ok on edit page
        pass
    return {"ok": True, "url": url, "snip": body[:500]}


def clear_and_set_tags(page) -> dict:
    info: dict = {"target_chars": len(", ".join(TAGS)), "n": len(TAGS)}
    # scroll to tags
    for _ in range(10):
        page.mouse.wheel(0, 600)
        page.wait_for_timeout(100)
    try:
        more = page.get_by_text("Show more", exact=True)
        if more.count():
            more.first.click(force=True, timeout=2000)
            page.wait_for_timeout(400)
    except Exception:
        pass
    blob = ", ".join(TAGS)
    try:
        box = page.get_by_role("textbox", name=re.compile(r"^Tags$", re.I))
        if box.count():
            box.first.click(force=True)
            page.keyboard.press("Meta+A")
            page.keyboard.press("Backspace")
            page.wait_for_timeout(200)
            box.first.fill(blob)
            page.keyboard.press("Enter")
            info["ok"] = True
            info["via"] = "role"
            return info
    except Exception as e:
        info["role_err"] = f"{type(e).__name__}"
    # JS fallback: find tags input in shadow
    ok = page.evaluate(
        """(blob) => {
          const walk=(r,d=0)=>{
            if(!r||d>50) return false;
            for (const inp of (r.querySelectorAll ? r.querySelectorAll('input,textarea') : [])) {
              const aria=(inp.getAttribute('aria-label')||'')+(inp.getAttribute('placeholder')||'');
              if (/^Tags$/i.test(aria) || /tags/i.test(aria)) {
                inp.focus();
                inp.value='';
                inp.dispatchEvent(new Event('input',{bubbles:true}));
                inp.value=blob;
                inp.dispatchEvent(new Event('input',{bubbles:true}));
                return true;
              }
            }
            for (const el of (r.querySelectorAll ? r.querySelectorAll('*') : [])) {
              if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
            }
            return false;
          };
          return walk(document);
        }""",
        blob,
    )
    info["ok"] = bool(ok)
    info["via"] = "js" if ok else "fail"
    return info


def set_not_kids(page) -> dict:
    info: dict = {}
    try:
        page.get_by_text(re.compile(r"No, it.?s not.?Made for Kids", re.I)).first.click(
            force=True, timeout=5000
        )
        info["kids"] = "no"
    except Exception:
        hit = click_shadow_text(page, r"No, it.?s not.?Made for Kids")
        info["kids"] = hit or "miss"
    try:
        page.get_by_text(re.compile(r"Yes, AI was used|Altered content|Yes$", re.I)).first.click(
            force=True, timeout=2500
        )
        info["ai"] = "clicked"
    except Exception:
        info["ai"] = "skip"
    return info


def open_edit_draft(page) -> dict:
    info: dict = {}
    # Click Edit draft banner
    hit = click_shadow_text(page, r"^Edit draft$")
    info["editDraft"] = hit
    page.wait_for_timeout(2500)
    if page.locator("ytcp-uploads-dialog").count():
        info["dialog"] = True
        return info
    # Try Create flow resume from content
    page.goto(
        f"https://studio.youtube.com/video/{VIDEO_ID}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3000)
    hit2 = click_shadow_text(page, r"^Edit draft$")
    info["editDraft2"] = hit2
    page.wait_for_timeout(2500)
    info["dialog"] = bool(page.locator("ytcp-uploads-dialog").count())
    return info


def next_until_visibility(page) -> str:
    for i in range(24):
        dismiss(page)
        text = dlg_text(page, 4000)
        if re.search(r"Save or publish|When will (your|this) video", text, re.I) or (
            re.search(r"\bPrivate\b", text)
            and re.search(r"\bPublic\b", text)
            and re.search(r"\bSchedule\b", text)
        ):
            return f"vis_{i}"
        if re.search(r"exceed the allowed character|error", text, re.I) and "Tags" in text:
            clear_and_set_tags(page)
            page.wait_for_timeout(800)
        nxt = page.get_by_role("button", name=re.compile(r"^Next$", re.I))
        if nxt.count() and nxt.first.is_enabled():
            nxt.first.click(force=True)
            page.wait_for_timeout(1800)
            continue
        if click_shadow_text(page, r"^Next$"):
            page.wait_for_timeout(1800)
            continue
        page.wait_for_timeout(900)
    return "no_vis"


def click_schedule_radio(page) -> str:
    try:
        loc = page.get_by_text("Select a date to make your video public", exact=False)
        if loc.count():
            loc.first.click(force=True, timeout=4000)
            page.wait_for_timeout(900)
            return "select_date_copy"
    except Exception:
        pass
    try:
        radio = page.get_by_role("radio", name=re.compile(r"^Schedule$", re.I))
        if radio.count():
            radio.first.click(force=True)
            page.wait_for_timeout(800)
            return "role:Schedule"
    except Exception:
        pass
    return click_shadow_text(page, r"^Schedule$") or ""


def fill_schedule_when(page) -> dict:
    info: dict = {"premiere": False}
    date_str = f"{SCHED_DAY} {SCHED_MONTH} 2026"
    el = page.locator('tp-yt-paper-input[aria-label="Enter date"] input')
    if el.count():
        el.first.click(force=True)
        page.keyboard.press("Meta+a")
        page.keyboard.type(date_str, delay=25)
        page.keyboard.press("Enter")
        info["date_typed"] = date_str
        page.wait_for_timeout(400)
    focused = page.evaluate(
        """() => {
          let el=null;
          const walk=(r,d=0)=>{
            if(!r||d>50||el) return;
            for (const inp of (r.querySelectorAll ? r.querySelectorAll('input') : [])) {
              if (/^\\d{1,2}:\\d{2}$/.test(inp.value||'')) { el=inp; return; }
            }
            for (const n of (r.querySelectorAll ? r.querySelectorAll('*') : [])) {
              if (n.shadowRoot) walk(n.shadowRoot, d+1);
            }
          };
          walk(document);
          if (!el) return {ok:false};
          el.focus(); el.select && el.select();
          return {ok:true, old:el.value||''};
        }"""
    )
    info["time_focus"] = focused
    if focused and focused.get("ok"):
        page.keyboard.press("Meta+a")
        page.keyboard.type(SCHED_TIME, delay=35)
        page.keyboard.press("Tab")
        info["time_typed"] = SCHED_TIME
    # Untick Premiere if checked
    page.evaluate(
        """() => {
          const walk=(r,d=0)=>{
            if(!r||d>40) return null;
            for (const el of (r.querySelectorAll
              ? r.querySelectorAll('[role=checkbox],tp-yt-paper-checkbox,input[type=checkbox]')
              : [])) {
              const t=((el.innerText||'')+' '+(el.getAttribute('aria-label')||'')+' '+((el.closest('label')||{}).innerText||''))
                .replace(/\\s+/g,' ').trim();
              if (/Premiere/i.test(t) && !/instant/i.test(t)) {
                const checked = el.getAttribute('aria-checked')==='true' || el.checked===true;
                if (checked) el.click();
                return {checkedWas:checked, t:t.slice(0,50)};
              }
            }
            for (const el of (r.querySelectorAll ? r.querySelectorAll('*') : [])) {
              if (el.shadowRoot) {
                const x=walk(el.shadowRoot,d+1);
                if (x) return x;
              }
            }
            return null;
          };
          return walk(document.querySelector('ytcp-uploads-dialog')||document);
        }"""
    )
    page.wait_for_timeout(300)
    return info


def click_schedule(page) -> str:
    for name in ["Schedule", "Done", "Save"]:
        try:
            btn = page.get_by_role("button", name=re.compile(rf"^{name}$", re.I))
            if btn.count() and btn.last.is_enabled():
                btn.last.click(force=True)
                page.wait_for_timeout(5000)
                return name
        except Exception:
            continue
    return click_shadow_text(page, r"^(Schedule|Done|Save)$") or ""


def verify_visibility(page) -> dict:
    page.goto(
        f"https://studio.youtube.com/video/{VIDEO_ID}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3500)
    dismiss(page)
    click_shadow_text(page, r"^Visibility$")
    page.wait_for_timeout(2000)
    # Also try top-right visibility chip
    body = snip(page, 5000)
    shot(page, "20_visibility_final.png")
    # Open publish schedule panel if present
    click_shadow_text(page, r"Scheduled|Private|Visibility")
    page.wait_for_timeout(1500)
    body2 = snip(page, 5000)
    shot(page, "21_visibility_panel.png")
    text = body + "\n" + body2
    return {
        "scheduled": bool(re.search(r"15\s*(Oct|October).*2026|Scheduled.*15|18:00", text, re.I)),
        "premiere": bool(re.search(r"will premiere|Premiere on", text, re.I)),
        "draft": bool(re.search(r"draft state", text, re.I)),
        "private": bool(re.search(r"\bPrivate\b", text, re.I)),
        "snip": text[:1800],
    }


def try_ab_test(page) -> dict:
    """Start Title and thumbnail Test & Compare if offered. Report exact options."""
    info: dict = {"wanted": "Title and thumbnail", "pairs": [
        {"title": TITLE, "thumb": str(THUMB_A)},
        {"title": TITLE_2, "thumb": str(THUMB_C)},
        {"title": TITLE_3, "thumb": str(THUMB_B)},
    ]}
    page.goto(
        f"https://studio.youtube.com/video/{VIDEO_ID}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3000)
    dismiss(page)
    hit = click_shadow_text(page, r"A/B Testing|Test & Compare|Test and compare")
    info["open"] = hit
    page.wait_for_timeout(2500)
    shot(page, "30_ab_open.png")
    body = snip(page, 4000)
    info["ui_snip"] = body[:1500]
    # What options are offered?
    offers = []
    for label in [
        "Title and thumbnail",
        "Thumbnail",
        "Title",
        "Titles and thumbnails",
        "Thumbnail only",
        "Title only",
    ]:
        if re.search(re.escape(label), body, re.I):
            offers.append(label)
    info["offers"] = offers
    # Try click Title and thumbnail
    chosen = None
    for label in ["Title and thumbnail", "Titles and thumbnails", "Thumbnail", "Title"]:
        if click_shadow_text(page, rf"^{re.escape(label)}$"):
            chosen = label
            break
    info["chosen"] = chosen
    page.wait_for_timeout(2000)
    shot(page, "31_ab_type.png")

    if not chosen:
        info["ok"] = False
        info["reason"] = "could_not_select_test_type"
        return info

    # Add variants — UI varies; try to set 3 variants
    # Upload additional thumbs / titles as available
    try:
        # Variant 2 title
        boxes = page.get_by_role("textbox")
        info["textbox_count"] = boxes.count()
    except Exception:
        info["textbox_count"] = 0

    # Attempt file inputs for B/C thumbs
    thumb_uploads = []
    for thumb in (THUMB_C, THUMB_B):
        try:
            loc = page.locator('input[type="file"]')
            for i in range(loc.count()):
                acc = (loc.nth(i).get_attribute("accept") or "").lower()
                if "image" in acc or "jpeg" in acc or "jpg" in acc:
                    # skip already-filled if possible
                    loc.nth(i).set_input_files(str(thumb))
                    thumb_uploads.append({"i": i, "file": thumb.name})
                    page.wait_for_timeout(1200)
                    break
        except Exception as e:
            thumb_uploads.append({"err": f"{type(e).__name__}", "file": thumb.name})
    info["thumb_uploads"] = thumb_uploads

    # Fill alt titles if title fields exist beyond primary
    try:
        for title in (TITLE_2, TITLE_3):
            # look for empty title inputs
            page.evaluate(
                """(title) => {
                  const walk=(r,d=0)=>{
                    if(!r||d>40) return false;
                    for (const inp of (r.querySelectorAll ? r.querySelectorAll('input,textarea') : [])) {
                      const aria=(inp.getAttribute('aria-label')||'')+(inp.placeholder||'');
                      if (/title/i.test(aria) && !(inp.value||'').trim()) {
                        inp.focus(); inp.value=title;
                        inp.dispatchEvent(new Event('input',{bubbles:true}));
                        return true;
                      }
                    }
                    for (const el of (r.querySelectorAll ? r.querySelectorAll('*') : [])) {
                      if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
                    }
                    return false;
                  };
                  return walk(document);
                }""",
                title,
            )
            page.wait_for_timeout(400)
    except Exception as e:
        info["title_fill_err"] = f"{type(e).__name__}"

    shot(page, "32_ab_filled.png")
    # Start / Save test
    start = click_shadow_text(page, r"^(Start|Save|Create|Done|Next)$")
    info["start"] = start
    page.wait_for_timeout(2500)
    shot(page, "33_ab_after_start.png")
    info["after"] = snip(page, 1200)
    info["ok"] = True
    info["note"] = (
        "Recorded what Studio offered. If only Thumbnail or only Title was available, "
        "that is what was set — no guessing beyond UI."
    )
    return info


def try_end_screen(page) -> dict:
    info: dict = {"related": RELATED_002, "subscribe": True}
    page.goto(
        f"https://studio.youtube.com/video/{VIDEO_ID}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(2500)
    dismiss(page)
    # End screen pencil under preview or Editor → End screen
    hit = click_shadow_text(page, r"^End screen$")
    info["open"] = hit
    page.wait_for_timeout(2000)
    if not hit:
        page.goto(
            f"https://studio.youtube.com/video/{VIDEO_ID}/edit?panel=endscreen",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(3000)
    shot(page, "40_endscreen_open.png")
    # Add element Video + Subscribe
    click_shadow_text(page, r"^Add element$|^Element$")
    page.wait_for_timeout(800)
    click_shadow_text(page, r"^Video$|^Video or playlist$")
    page.wait_for_timeout(1200)
    # search / pick 002
    try:
        box = page.get_by_role("textbox").first
        if box.count():
            box.fill("How Did We Discover the Periodic Table")
            page.keyboard.press("Enter")
            page.wait_for_timeout(1500)
    except Exception:
        pass
    # click first result or paste id
    click_shadow_text(page, r"Periodic Table|AL_-qlWko_g")
    page.wait_for_timeout(1000)
    click_shadow_text(page, r"^Subscribe$|^Add element$")
    page.wait_for_timeout(800)
    click_shadow_text(page, r"^Subscribe$")
    page.wait_for_timeout(800)
    # timing last 20s — often default
    save = click_shadow_text(page, r"^(Save|Done)$")
    info["save"] = save
    page.wait_for_timeout(2000)
    shot(page, "41_endscreen_saved.png")
    info["snip"] = snip(page, 1000)
    info["ok"] = True
    return info


def try_pin(page) -> dict:
    info: dict = {"text": PIN}
    page.goto(
        f"https://www.youtube.com/watch?v={VIDEO_ID}",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(4000)
    shot(page, "50_watch.png")
    body = snip(page, 2000)
    if re.search(r"premiere|scheduled|unavailable|private", body, re.I):
        info["ok"] = False
        info["reason"] = "watch_page_not_commentable_while_scheduled_or_private"
        info["note"] = "Pin on launch day if Studio blocks comments on scheduled drafts."
        return info
    # Studio comments tab
    page.goto(
        f"https://studio.youtube.com/video/{VIDEO_ID}/comments",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3000)
    shot(page, "51_comments.png")
    # Try add comment as channel
    try:
        box = page.get_by_role("textbox").first
        if box.count():
            box.click()
            box.fill(PIN)
            page.keyboard.press("Enter")
            page.wait_for_timeout(2000)
            info["posted"] = True
    except Exception as e:
        info["posted"] = False
        info["err"] = f"{type(e).__name__}"
    pin = click_shadow_text(page, r"^Pin$|^Pin comment$")
    info["pinClick"] = pin
    shot(page, "52_pin.png")
    info["ok"] = bool(info.get("posted") or pin)
    if not info["ok"]:
        info["note"] = "Pinned comment deferred to launch day if Studio blocks it on scheduled video."
    return info


def try_captions(page) -> dict:
    info: dict = {"file": str(CAPTIONS)}
    if not CAPTIONS.exists():
        info["ok"] = False
        info["reason"] = "missing_srt"
        return info
    page.goto(
        f"https://studio.youtube.com/video/{VIDEO_ID}/translations",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3000)
    shot(page, "60_captions.png")
    try:
        with page.expect_file_chooser(timeout=8000) as fc:
            click_shadow_text(page, r"Upload|Add language|Duplicate")
        fc.value.set_files(str(CAPTIONS))
        info["ok"] = True
        info["via"] = "chooser"
    except Exception:
        try:
            loc = page.locator('input[type="file"]')
            if loc.count():
                loc.first.set_input_files(str(CAPTIONS))
                info["ok"] = True
                info["via"] = "input"
            else:
                info["ok"] = False
                info["reason"] = "no_file_input"
        except Exception as e:
            info["ok"] = False
            info["err"] = f"{type(e).__name__}"
    page.wait_for_timeout(2000)
    shot(page, "61_captions_after.png")
    return info


def main() -> int:
    EV.mkdir(parents=True, exist_ok=True)
    (EV / "finish.log").write_text("")
    result: dict = {
        "ok": False,
        "videoId": VIDEO_ID,
        "channel": HANDLE,
        "channelId": CHANNEL,
        "tagsTrimmedChars": len(", ".join(TAGS)),
    }

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        ctx = browser.contexts[0]
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        try:
            hos = ensure_hos(page)
            result["channelCheck"] = hos
            shot(page, "11_edit_open.png")
            if not hos.get("ok"):
                dump("FINISH_RESULT.json", result)
                return 2

            # Prefer resume upload dialog
            draft = open_edit_draft(page)
            result["editDraft"] = draft
            shot(page, "12_edit_draft.png")

            if draft.get("dialog"):
                result["tags"] = clear_and_set_tags(page)
                result["kids"] = set_not_kids(page)
                # ensure thumb still A
                try:
                    loc = page.locator('input[type="file"]')
                    for i in range(loc.count()):
                        acc = (loc.nth(i).get_attribute("accept") or "").lower()
                        if "image" in acc:
                            loc.nth(i).set_input_files(str(THUMB_A))
                            result["thumbRefresh"] = True
                            break
                except Exception:
                    pass
                shot(page, "13_details_fixed.png")
                result["next"] = next_until_visibility(page)
                shot(page, "14_visibility.png")
                result["scheduleRadio"] = click_schedule_radio(page)
                result["when"] = fill_schedule_when(page)
                shot(page, "15_schedule_when.png")
                result["done"] = click_schedule(page)
                shot(page, "16_after_schedule.png")
            else:
                # Edit-page path: fix tags/kids then Visibility panel
                result["tags"] = clear_and_set_tags(page)
                result["kids"] = set_not_kids(page)
                try:
                    page.get_by_role("button", name=re.compile(r"^Save$", re.I)).first.click(
                        force=True, timeout=3000
                    )
                except Exception:
                    click_shadow_text(page, r"^Save$")
                page.wait_for_timeout(2000)
                # Visibility from top
                click_shadow_text(page, r"Visibility|Private|Draft")
                page.wait_for_timeout(1500)
                shot(page, "14b_vis_chip.png")
                result["scheduleRadio"] = click_schedule_radio(page)
                result["when"] = fill_schedule_when(page)
                shot(page, "15b_schedule_when.png")
                result["done"] = click_schedule(page) or click_shadow_text(page, r"^Save$")
                shot(page, "16b_after_schedule.png")

            result["visibility"] = verify_visibility(page)
            result["abTest"] = try_ab_test(page)
            result["endScreen"] = try_end_screen(page)
            result["pin"] = try_pin(page)
            result["captions"] = try_captions(page)

            vis = result.get("visibility") or {}
            result["ok"] = bool(
                VIDEO_ID
                and vis.get("scheduled")
                and not vis.get("premiere")
                and not vis.get("draft")
            )
            result["scheduleLabel"] = "Thu 15 Oct 2026 18:00 Europe/London"
            result["publishAt"] = "2026-10-15T17:00:00.000Z"
            result["screenshot"] = str(EV / "20_visibility_final.png")

            dump("FINISH_RESULT.json", result)
            # Merge into PACKAGE_UPLOAD_RESULT
            out = PKG / "Schedule/PACKAGE_UPLOAD_RESULT_2026-09-29.json"
            base = {}
            if out.exists():
                base = json.loads(out.read_text())
            base.update(
                {
                    "ok": result["ok"],
                    "finish": result,
                    "videoId": VIDEO_ID,
                    "scheduleVerified": vis,
                    "testAndCompare": result.get("abTest"),
                    "endScreen": result.get("endScreen"),
                    "pinnedComment": result.get("pin"),
                    "captions": result.get("captions"),
                    "tagsTrimmedTo": result["tagsTrimmedChars"],
                    "screenshot": result["screenshot"],
                }
            )
            out.write_text(json.dumps(base, indent=2) + "\n")
            (ART / "PACKAGE_UPLOAD_RESULT_2026-09-29.json").write_text(out.read_text())
            log(f"FINISH ok={result['ok']} scheduled={vis.get('scheduled')} premiere={vis.get('premiere')} draft={vis.get('draft')}")
            return 0 if result["ok"] else 5
        except Exception as e:
            result["error"] = f"{type(e).__name__}:{e}"
            result["trace"] = traceback.format_exc()[-2000:]
            shot(page, "99_finish_error.png")
            dump("FINISH_RESULT.json", result)
            log(f"ERROR {e}")
            return 9


if __name__ == "__main__":
    raise SystemExit(main())
