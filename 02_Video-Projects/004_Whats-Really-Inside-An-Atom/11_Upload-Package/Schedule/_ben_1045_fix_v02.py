#!/usr/bin/env python3
"""Ben 10:45 FIX v02 — stay on video edit pages; privatize Tue; confirm Fri/Sun.

Channel check: visit HOS dashboard once, then never navigate back mid-edit.
CDP :9460 · @HistoryOfScienceYT only. Never delete/publish/premiere/replace.
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

PORT = 9460
HOS = "UCXp7HkBIl1LgaznXuZHJyRg"
HANDLE = "@HistoryOfScienceYT"
LONDON = ZoneInfo("Europe/London")

PROJ = Path(
    "/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/"
    "004_Whats-Really-Inside-An-Atom"
)
SCHED = PROJ / "11_Upload-Package/Schedule"
EV = SCHED / "evidence_2026-09-30_shorts"
ART = Path(
    "/Users/benjaminoats/Library/Application Support/Cursor/AgentStores/"
    "cursor_agent_stores/bc-958ae0f3-be07-568f-a2ab-eb7f422d8839/files/artifacts"
)

TUE = "CUu8k38iAMc"
FRI = {
    "slot": "s01",
    "id": "29bpGAI0wb8",
    "title": "How small can you cut gold?",
    "related_id": "GHZDsiH7L7A",
    "related_title": "What's Really Inside an Atom?",
    "day": "16",
    "may_defer": True,
}
SUN = {
    "slot": "s02",
    "id": "TbMMJSRKC3U",
    "title": "He said every eighth element repeats",
    "related_id": "AL_-qlWko_g",
    "related_title": "How Did We Discover the Periodic Table?",
    "day": "18",
    "may_defer": False,
}

_SPEC = importlib.util.spec_from_file_location(
    "hos004_shorts", SCHED / "_upload_hos_004_shorts_v01.py"
)
up = importlib.util.module_from_spec(_SPEC)
assert _SPEC.loader
_SPEC.loader.exec_module(up)

_SPEC2 = importlib.util.spec_from_file_location(
    "cos2102", SCHED / "_cos_checkin_2102_growth_fix_v01.py"
)
cos = importlib.util.module_from_spec(_SPEC2)
assert _SPEC2.loader
_SPEC2.loader.exec_module(cos)


def log(msg: str) -> None:
    EV.mkdir(parents=True, exist_ok=True)
    line = f"{datetime.now(LONDON).isoformat(timespec='seconds')} {msg}"
    print(line, flush=True)
    with open(EV / "ben_1045_v02.log", "a") as f:
        f.write(line + "\n")


def dump(name: str, obj) -> None:
    (EV / name).write_text(json.dumps(obj, indent=2, default=str) + "\n")


def shot(page, name: str, art: str | None = None) -> Path:
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    p = EV / name
    page.screenshot(path=str(p), full_page=False)
    if art:
        shutil.copy2(p, ART / art)
    return p


def channel_gate(page) -> dict:
    """One-time HOS gate. Do not call again while on a video edit page."""
    page.goto(
        f"https://studio.youtube.com/channel/{HOS}",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3000)
    up.dismiss(page)
    body = page.inner_text("body")[:3000]
    url = page.url
    if any(x in url for x in ("accountchooser", "signin", "ServiceLogin")):
        raise SystemExit(f"LOGIN_REQUIRED {url}")
    if "History of Science" not in body and HOS not in url:
        raise SystemExit(f"WRONG_CHANNEL {url} {body[:200]!r}")
    if re.search(r"\bOrbit With Ben\b", body) and "History of Science" not in body:
        raise SystemExit("WRONG_CHANNEL Orbit")
    out = {"ok": True, "url": url, "snip": body[:300]}
    log(f"CHANNEL_GATE {out}")
    return out


def open_edit(page, vid: str) -> str:
    page.goto(
        f"https://studio.youtube.com/video/{vid}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(4000)
    up.dismiss(page)
    url = page.url or ""
    if f"/video/{vid}/" not in url:
        raise SystemExit(f"ABORT: expected edit {vid}, got {url}")
    # Soft channel confirm via page chrome (sidebar channel name)
    body = page.inner_text("body")[:2000]
    if re.search(r"\bOrbit With Ben\b", body) and "History of Science" not in body:
        raise SystemExit("ABORT: Orbit chrome on edit page")
    log(f"OPEN_EDIT {vid} url={url}")
    return url


def title_from_edit(page) -> str:
    return (
        page.evaluate(
            """() => {
          const walk = (r, d = 0) => {
            if (!r || d > 50) return null;
            for (const el of (r.querySelectorAll
              ? r.querySelectorAll('input,textarea,#textbox,[contenteditable=true]')
              : [])) {
              const al = (el.getAttribute('aria-label') || '').toLowerCase();
              const v = (el.value || el.innerText || '').trim();
              if (!v || v.length < 3) continue;
              if (al.includes('title') || el.id === 'textbox') return v.slice(0, 200);
            }
            for (const el of (r.querySelectorAll ? r.querySelectorAll('*') : []))
              if (el.shadowRoot) {
                const x = walk(el.shadowRoot, d + 1);
                if (x) return x;
              }
            return null;
          };
          return walk(document);
        }"""
        )
        or ""
    )


def wait_for_chip(page, tries: int = 8) -> str:
    for i in range(tries):
        chip = up.visibility_chip(page)
        if chip:
            return chip
        page.wait_for_timeout(800)
        # Sometimes need a tiny scroll to hydrate
        if i == 2:
            page.mouse.wheel(0, 200)
        if i == 4:
            page.keyboard.press("Home")
    return up.visibility_chip(page) or ""


def click_vis_edit(page) -> str:
    """Open visibility editor — icon button or Visibility chip."""
    if up.open_vis(page):
        page.wait_for_timeout(1200)
        return "icon"
    hit = page.evaluate(
        """() => {
          let hit = null;
          const walk = (r, d = 0) => {
            if (!r || d > 55 || hit) return;
            for (const el of (r.querySelectorAll ? r.querySelectorAll('*') : [])) {
              const t = (el.innerText || '').replace(/\\s+/g, ' ').trim();
              if (/^Visibility\\s+(Private|Public|Unlisted|Scheduled)/i.test(t)
                  && t.length < 160) {
                el.click(); hit = t.slice(0, 120); return;
              }
            }
            for (const el of (r.querySelectorAll ? r.querySelectorAll('*') : []))
              if (el.shadowRoot) walk(el.shadowRoot, d + 1);
          };
          walk(document);
          return hit;
        }"""
    )
    page.wait_for_timeout(1200)
    return hit or ""


def click_private_radio(page) -> str:
    # Prefer role
    try:
        r = page.get_by_role("radio", name=re.compile(r"^Private$", re.I))
        if r.count():
            r.first.click(force=True, timeout=4000)
            page.wait_for_timeout(700)
            return "role:Private"
    except Exception as e:
        log(f"role Private fail {e}")
    hit = page.evaluate(
        """() => {
          let hit = null;
          const walk = (r, d = 0) => {
            if (!r || d > 55 || hit) return;
            for (const el of (r.querySelectorAll
              ? r.querySelectorAll('tp-yt-paper-radio-button,[role=radio],input[type=radio]')
              : [])) {
              const al = (el.getAttribute('aria-label') || '').trim();
              const t = ((el.innerText || '') + ' ' + al).replace(/\\s+/g, ' ').trim();
              const first = t.split('\\n')[0].trim();
              if (/^Private$/i.test(first) || /^Private$/i.test(al)
                  || /^Private\\b/i.test(t) && t.length < 40) {
                // Reject Scheduled/Public/Unlisted
                if (/Public|Unlisted|Schedule/i.test(first)) continue;
                el.scrollIntoView({block:'center'});
                el.click();
                hit = t.slice(0, 80);
                return;
              }
            }
            for (const el of (r.querySelectorAll ? r.querySelectorAll('*') : []))
              if (el.shadowRoot) walk(el.shadowRoot, d + 1);
          };
          walk(document);
          return hit;
        }"""
    )
    page.wait_for_timeout(700)
    return hit or ""


def save_vis_dialog(page) -> dict:
    info = {}
    # Dialog Save / Done — NEVER Schedule / Publish / Delete / Premiere
    clicked = page.evaluate(
        """() => {
          const bad = /delete|publish|premiere|replace|^schedule$/i;
          let hit = null;
          const tryClick = (label) => {
            const walk = (r, d = 0) => {
              if (!r || d > 55 || hit) return;
              for (const el of (r.querySelectorAll
                ? r.querySelectorAll('button,ytcp-button,[role=button]') : [])) {
                const t = (el.innerText || el.getAttribute('aria-label') || '')
                  .trim().replace(/\\s+/g, ' ');
                if (!t || bad.test(t)) continue;
                if (t.toLowerCase() !== label.toLowerCase()) continue;
                const dis = el.disabled || el.getAttribute('aria-disabled') === 'true';
                if (dis) continue;
                el.click(); hit = t; return;
              }
              for (const el of (r.querySelectorAll ? r.querySelectorAll('*') : []))
                if (el.shadowRoot) walk(el.shadowRoot, d + 1);
            };
            walk(document);
          };
          tryClick('Save');
          if (!hit) tryClick('Done');
          if (!hit) tryClick('Update');
          return hit;
        }"""
    )
    info["dialog"] = clicked
    page.wait_for_timeout(1500)
    # Confirm only safe names
    for name in ["Update", "Save", "Confirm", "Yes", "OK", "Done"]:
        try:
            b = page.get_by_role("button", name=re.compile(rf"^{re.escape(name)}$", re.I))
            if b.count() and b.first.is_visible():
                lab = (b.first.inner_text() or "").strip()
                if re.search(r"publish|schedule|delete|premiere|replace", lab, re.I):
                    continue
                b.first.click(force=True, timeout=1500)
                info["confirm"] = name
                page.wait_for_timeout(900)
        except Exception:
            pass
    # Top Save if dirty
    ps = up.page_save(page)
    info["page_save"] = ps
    page.wait_for_timeout(2000)
    return info


def is_private_chip(chip: str) -> bool:
    if not chip:
        return False
    if re.search(r"Scheduled|Public|Unlisted", chip, re.I):
        return False
    return bool(re.search(r"Private", chip, re.I))


def privatize_tue(page) -> dict:
    open_edit(page, TUE)
    title = title_from_edit(page)
    chip0 = wait_for_chip(page)
    out = {"title": title, "chip_before": chip0, "url": page.url}
    log(f"TUE before chip={chip0!r} title={title!r}")
    shot(page, "BEN_1045_tue_before_visibility.png")

    via = click_vis_edit(page)
    out["open_via"] = via
    shot(page, "BEN_1045_tue_vis_dialog.png")
    # Dump dialog radios for debug
    radios = page.evaluate(
        """() => {
          const out = [];
          const walk = (r, d = 0) => {
            if (!r || d > 55) return;
            for (const el of (r.querySelectorAll
              ? r.querySelectorAll('tp-yt-paper-radio-button,[role=radio]') : [])) {
              const t = ((el.innerText||'')+' '+(el.getAttribute('aria-label')||''))
                .replace(/\\s+/g,' ').trim().slice(0,100);
              const checked = el.getAttribute('aria-checked')==='true' || el.checked===true;
              if (t) out.push({t, checked});
            }
            for (const el of (r.querySelectorAll ? r.querySelectorAll('*') : []))
              if (el.shadowRoot) walk(el.shadowRoot, d + 1);
          };
          walk(document);
          return out.slice(0, 30);
        }"""
    )
    out["dialog_radios"] = radios
    log(f"TUE dialog radios={radios}")

    radio = click_private_radio(page)
    out["radio"] = radio
    page.wait_for_timeout(600)
    shot(page, "BEN_1045_tue_private_selected.png")

    # Assert Private checked before save
    checked = page.evaluate(
        """() => {
          let priv=null, sched=null, pub=null, unl=null;
          const walk = (r, d = 0) => {
            if (!r || d > 55) return;
            for (const el of (r.querySelectorAll
              ? r.querySelectorAll('tp-yt-paper-radio-button,[role=radio]') : [])) {
              const t = ((el.innerText||'')+' '+(el.getAttribute('aria-label')||''))
                .replace(/\\s+/g,' ').trim();
              const checked = el.getAttribute('aria-checked')==='true' || el.checked===true;
              if (/^Private\\b/i.test(t) && t.length < 40) priv = checked;
              if (/^Schedule\\b|^Scheduled\\b/i.test(t)) sched = checked;
              if (/^Public\\b/i.test(t) && t.length < 40) pub = checked;
              if (/^Unlisted\\b/i.test(t)) unl = checked;
            }
            for (const el of (r.querySelectorAll ? r.querySelectorAll('*') : []))
              if (el.shadowRoot) walk(el.shadowRoot, d + 1);
          };
          walk(document);
          return {priv, sched, pub, unl};
        }"""
    )
    out["checked_before_save"] = checked
    log(f"TUE checked={checked}")
    if checked.get("priv") is not True:
        # Retry click Private via get_by_text
        try:
            page.get_by_text(re.compile(r"^Private$"), exact=True).first.click(timeout=3000)
            page.wait_for_timeout(700)
            out["retry_text_click"] = True
        except Exception as e:
            out["retry_text_click_err"] = str(e)

    save = save_vis_dialog(page)
    out["save"] = save
    log(f"TUE save={save}")

    # Reload and confirm
    open_edit(page, TUE)
    chip1 = wait_for_chip(page)
    out["chip_after"] = chip1
    out["private_ok"] = is_private_chip(chip1)
    shot(page, "BEN_1045_tue_after_visibility.png", art="BEN_1045_tue_private.png")
    shutil.copy2(EV / "BEN_1045_tue_after_visibility.png", ART / "BEN_1045_tue_private.png")
    log(f"TUE after chip={chip1!r} private_ok={out['private_ok']}")

    # Audience + Altered
    for _ in range(16):
        page.mouse.wheel(0, 900)
        page.wait_for_timeout(100)
    cos.show_more(page)
    page.wait_for_timeout(600)
    aud = cos.read_audience(page)
    ai = cos.read_ai_altered(page)
    if not aud.get("radios"):
        page.keyboard.press("Home")
        page.wait_for_timeout(300)
        for _ in range(25):
            page.keyboard.press("PageDown")
            page.wait_for_timeout(70)
        cos.show_more(page)
        aud = cos.read_audience(page)
        ai = cos.read_ai_altered(page)
    out["audience"] = aud
    out["altered"] = ai
    out["audience_not_kids"] = bool(aud.get("ok_not_kids")) and not aud.get("fail_kids")
    out["altered_yes"] = bool(ai.get("yes")) or any(
        isinstance(r, dict) and r.get("checked") and re.search(r"^Yes", str(r.get("label", "")), re.I)
        for r in (ai.get("radios") or [])
    )
    page.keyboard.press("Home")
    page.wait_for_timeout(400)
    shot(page, "BEN_1045_tue_final.png", art="BEN_1045_tue_private.png")
    shutil.copy2(EV / "BEN_1045_tue_final.png", ART / "BEN_1045_tue_private.png")
    # Final chip again at top
    chip2 = wait_for_chip(page)
    out["chip_final"] = chip2
    out["private_ok"] = is_private_chip(chip2)
    return out


def read_related(page) -> dict:
    body = page.inner_text("body")
    idx = body.lower().find("related video")
    window = body[idx : idx + 500] if idx >= 0 else ""
    line_m = re.search(r"Related video[^\n]{0,240}", body, re.I)
    line = line_m.group(0).strip() if line_m else ""
    out = {"line": line, "window": window.replace("\n", " ")[:350], "set": False, "title": None, "id_hint": None}
    pairs = [
        ("GHZDsiH7L7A", "What's Really Inside an Atom?"),
        ("AL_-qlWko_g", "How Did We Discover the Periodic Table?"),
        ("frP_YrNShsU", "How Did We Discover X-rays?"),
        ("_C92tIJCk8A", "How Did We Discover Germs?"),
    ]
    blob = window + " " + line
    for tid, ttitle in pairs:
        if tid in blob or ttitle in blob:
            out["set"] = True
            out["title"] = ttitle
            out["id_hint"] = tid
            break
    if not out["set"] and line and not re.search(r"None|Add (a )?related", line, re.I):
        out["set"] = True
    return out


def confirm_job(page, job: dict) -> dict:
    open_edit(page, job["id"])
    title = title_from_edit(page)
    chip = wait_for_chip(page)
    out = {
        "slot": job["slot"],
        "id": job["id"],
        "title": title,
        "visibility_chip": chip,
        "url": page.url,
    }
    body_top = page.inner_text("body")
    date_ok = bool(
        re.search(rf"\b{job['day']}\s+(Oct|October)\b", chip + " " + body_top, re.I)
        or re.search(rf"\b(Oct|October)\s+{job['day']}\b", chip + " " + body_top, re.I)
    )
    time_ok = bool(re.search(r"11:30|11\.30", chip + " " + body_top))
    scheduled_ok = "Scheduled" in chip and date_ok and time_ok
    out["date_ok"] = date_ok
    out["time_ok"] = time_ok
    out["scheduled_ok"] = scheduled_ok

    # Scroll for settings
    for _ in range(16):
        page.mouse.wheel(0, 900)
        page.wait_for_timeout(100)
    cos.show_more(page)
    aud = cos.read_audience(page)
    ai = cos.read_ai_altered(page)
    if not aud.get("radios"):
        for _ in range(20):
            page.keyboard.press("PageDown")
            page.wait_for_timeout(70)
        cos.show_more(page)
        aud = cos.read_audience(page)
        ai = cos.read_ai_altered(page)
    related = read_related(page)

    page.keyboard.press("Home")
    page.wait_for_timeout(500)
    # One more scroll to get visibility + title in shot, then a mid scroll for related
    shot(page, f"BEN_1045_{job['slot']}_confirm.png", art=f"BEN_1045_{job['slot']}_confirm.png")
    shutil.copy2(
        EV / f"BEN_1045_{job['slot']}_confirm.png",
        ART / f"BEN_1045_{job['slot']}_confirm.png",
    )
    # Also take a related-focused shot into evidence
    for _ in range(12):
        page.mouse.wheel(0, 1000)
        page.wait_for_timeout(80)
    shot(page, f"BEN_1045_{job['slot']}_confirm_related.png")

    if related.get("id_hint") == job["related_id"] or related.get("title") == job["related_title"]:
        related_status = "set"
    elif job.get("may_defer"):
        related_status = "deferred_or_unset"
    elif related.get("set"):
        related_status = f"other:{related.get('title') or related.get('line')[:80]}"
    else:
        related_status = "unset"

    altered_yes = bool(ai.get("yes")) or any(
        isinstance(r, dict) and r.get("checked") and re.search(r"Yes", str(r.get("label", "")), re.I)
        for r in (ai.get("radios") or [])
    )

    out.update(
        {
            "audience": aud,
            "audience_not_kids": bool(aud.get("ok_not_kids")) and not aud.get("fail_kids"),
            "altered": ai,
            "altered_yes": altered_yes,
            "related": related,
            "related_status": related_status,
            "ok": scheduled_ok
            and bool(aud.get("ok_not_kids"))
            and not aud.get("fail_kids"),
        }
    )
    log(
        f"{job['slot']} chip={chip!r} scheduled_ok={scheduled_ok} "
        f"aud_ok={out['audience_not_kids']} altered={altered_yes} related={related_status}"
    )
    return out


def fix_shorts_list_titles() -> list[dict]:
    raw = json.loads((EV / "LIVE_SHORTS_LIST.json").read_text())
    shorts = raw.get("shorts") or []
    fixed = []
    for s in shorts:
        item = dict(s)
        rt = item.get("row_text") or ""
        # Extract title: after duration "0:XX " then title repeated
        m = re.match(r"0:\d{2}\s+(.+?)(?:\s+\1\s+|\s+—|\s+Public|\s+Scheduled|\s+Private)", rt)
        if m:
            item["title"] = m.group(1).strip()
        else:
            # Fallback: known titles from description start
            for known in [
                "The first X-ray showed a wedding ring",
                "He said every eighth element repeats",
                "How small can you cut gold?",
                "How did Röntgen see bones without cutting",
                "How X-rays Were Discovered by Accident",
                "What other table has empty chairs?",
                "Why tellurium sat before iodine",
                "Gallium sat where the table said",
                "He predicted a metal before it was found",
                "The periodic table's empty chairs",
                "A flask that proved germs come from outside",
                "Invisible life is still everywhere",
                "Germs hitch a ride on you",
                "Microbes in a drop of pond water",
                "Germs don't cast a shadow",
            ]:
                if known in rt:
                    item["title"] = known
                    break
        # Visibility/date refine from row_text
        if "Scheduled" in rt:
            item["visibility"] = "Scheduled"
            dm = re.search(r"Scheduled\s+(\d{1,2}\s+\w+\s+\d{4})", rt)
            if dm:
                item["date"] = dm.group(1)
        elif "Private" in rt and "Scheduled" not in rt:
            item["visibility"] = "Private"
        elif "Public" in rt:
            item["visibility"] = "Public"
            dm = re.search(r"Public\s+(\d{1,2}\s+\w+\s+\d{4})", rt)
            if dm:
                item["date"] = dm.group(1)
        fixed.append(item)

    # Re-scrape list after privatize to refresh Tue visibility
    return fixed


def rescrape_shorts(page) -> list[dict]:
    page.goto(
        f"https://studio.youtube.com/channel/{HOS}/videos/short",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(4000)
    up.dismiss(page)
    for _ in range(20):
        page.mouse.wheel(0, 1600)
        page.wait_for_timeout(200)
    page.keyboard.press("Home")
    page.wait_for_timeout(600)
    shot(page, "LIVE_SHORTS_CONTENT.png", art="BEN_1045_live_shorts_list.png")
    shutil.copy2(EV / "LIVE_SHORTS_CONTENT.png", ART / "BEN_1045_live_shorts_list.png")

    rows = page.evaluate(
        """() => {
          const out = [];
          const seen = new Set();
          const walk = (r, d = 0) => {
            if (!r || d > 60) return;
            for (const a of (r.querySelectorAll
              ? r.querySelectorAll('a[href*="/video/"]') : [])) {
              const href = a.getAttribute('href') || '';
              const m = href.match(/\\/video\\/([A-Za-z0-9_-]{11})/);
              if (!m) continue;
              const id = m[1];
              if (seen.has(id)) continue;
              let el = a, text = '';
              for (let i = 0; i < 10 && el; i++) {
                const t = (el.innerText || '').replace(/\\s+/g, ' ').trim();
                if (t.length > text.length && t.length < 900) text = t;
                el = el.parentElement;
              }
              seen.add(id);
              let visibility = null;
              if (/\\bPrivate\\b/i.test(text) && !/\\bScheduled\\b/i.test(text)) visibility = 'Private';
              else if (/\\bScheduled\\b/i.test(text)) visibility = 'Scheduled';
              else if (/\\bUnlisted\\b/i.test(text)) visibility = 'Unlisted';
              else if (/\\bDraft\\b/i.test(text)) visibility = 'Draft';
              else if (/\\bPublic\\b/i.test(text)) visibility = 'Public';
              let date = null;
              let dm = text.match(/Scheduled\\s+(\\d{1,2}\\s+\\w+\\s+\\d{4}(?:\\s*[·,]?\\s*\\d{1,2}:\\d{2})?)/i);
              if (dm) date = dm[1];
              else {
                dm = text.match(/Public\\s+(\\d{1,2}\\s+\\w+\\s+\\d{4})/i);
                if (dm) date = dm[1];
                else {
                  dm = text.match(/Private\\s+(\\d{1,2}\\s+\\w+\\s+\\d{4})/i);
                  if (dm) date = dm[1];
                }
              }
              let title = null;
              const tm = text.match(/^0:\\d{2}\\s+(.+?)\\s+\\1\\s+/);
              if (tm) title = tm[1].trim();
              out.push({id, title, visibility, date, row_text: text.slice(0, 320), href});
            }
            for (const el of (r.querySelectorAll ? r.querySelectorAll('*') : []))
              if (el.shadowRoot) walk(el.shadowRoot, d + 1);
          };
          walk(document);
          return out;
        }"""
    )
    # Title fallbacks
    for item in rows:
        if item.get("title"):
            continue
        rt = item.get("row_text") or ""
        for known in [
            "The first X-ray showed a wedding ring",
            "He said every eighth element repeats",
            "How small can you cut gold?",
            "How did Röntgen see bones without cutting",
            "How X-rays Were Discovered by Accident",
            "What other table has empty chairs?",
            "Why tellurium sat before iodine",
            "Gallium sat where the table said",
            "He predicted a metal before it was found",
            "The periodic table's empty chairs",
            "A flask that proved germs come from outside",
            "Invisible life is still everywhere",
            "Germs hitch a ride on you",
            "Microbes in a drop of pond water",
            "Germs don't cast a shadow",
        ]:
            if known.lower() in rt.lower():
                item["title"] = known
                break
    return rows


def write_list(shorts: list[dict]) -> None:
    dump(
        "LIVE_SHORTS_LIST.json",
        {
            "ok": True,
            "channel": HANDLE,
            "channelId": HOS,
            "scraped_at": datetime.now(LONDON).isoformat(timespec="seconds"),
            "count": len(shorts),
            "shorts": shorts,
        },
    )
    lines = [
        "# Live HOS Shorts list",
        "",
        f"Channel: `{HANDLE}` (`{HOS}`)",
        f"Scraped: {datetime.now(LONDON).isoformat(timespec='seconds')}",
        f"Count: {len(shorts)}",
        "",
        "| # | Title | Video ID | Visibility | Date |",
        "|---|-------|----------|------------|------|",
    ]
    for i, s in enumerate(shorts, 1):
        title = (s.get("title") or "").replace("|", "\\|")
        lines.append(
            f"| {i} | {title} | `{s.get('id')}` | {s.get('visibility') or ''} | {s.get('date') or ''} |"
        )
    lines.append("")
    (EV / "LIVE_SHORTS_LIST.md").write_text("\n".join(lines) + "\n")


def main() -> None:
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    result = {"channel": HANDLE, "channelId": HOS, "started": datetime.now(LONDON).isoformat(timespec="seconds")}
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
        ctx = browser.contexts[0] if browser.contexts else browser.new_context()
        page = None
        for pg in ctx.pages:
            if "studio.youtube.com" in (pg.url or ""):
                page = pg
                break
        if page is None:
            page = ctx.new_page()

        channel_gate(page)

        log("=== PRIVATIZE TUE ===")
        tue = privatize_tue(page)
        result["tue_private"] = tue
        dump("BEN_1045_TUE_PRIVATE.json", tue)

        log("=== CONFIRM FRI ===")
        fri = confirm_job(page, FRI)
        result["fri"] = fri
        dump("BEN_1045_FRI_CONFIRM.json", fri)

        log("=== CONFIRM SUN ===")
        sun = confirm_job(page, SUN)
        result["sun"] = sun
        dump("BEN_1045_SUN_CONFIRM.json", sun)

        log("=== RESCRAPE SHORTS ===")
        shorts = rescrape_shorts(page)
        write_list(shorts)
        result["shorts_count"] = len(shorts)
        result["shorts"] = [
            {
                "id": s.get("id"),
                "title": s.get("title"),
                "visibility": s.get("visibility"),
                "date": s.get("date"),
            }
            for s in shorts
        ]

        result["ended"] = datetime.now(LONDON).isoformat(timespec="seconds")
        result["ok"] = bool(tue.get("private_ok")) and bool(fri.get("ok")) and bool(sun.get("ok"))
        dump("BEN_1045_RESULT.json", result)
        log(f"DONE ok={result['ok']} tue={tue.get('private_ok')} fri={fri.get('ok')} sun={sun.get('ok')}")
        print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
