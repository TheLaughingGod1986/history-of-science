#!/usr/bin/env python3
"""Ben 10:45 — Privatize Tue Short CUu8k38iAMc + scrape HOS Shorts + confirm Fri/Sun.

CDP :9460 · ~/.hos-chrome-youtube-studio · @HistoryOfScienceYT only.
Never Orbit. Never delete. Never publish-now. Never Premiere. Never Replace.
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

TUE_ID = "CUu8k38iAMc"
FRI = {
    "slot": "s01",
    "id": "29bpGAI0wb8",
    "title": "How small can you cut gold?",
    "expect_date": "16 Oct",
    "expect_time": "11:30",
    "related_id": "GHZDsiH7L7A",
    "related_title": "What's Really Inside an Atom?",
    "related_may_defer": True,
}
SUN = {
    "slot": "s02",
    "id": "TbMMJSRKC3U",
    "title": "He said every eighth element repeats",
    "expect_date": "18 Oct",
    "expect_time": "11:30",
    "related_id": "AL_-qlWko_g",
    "related_title": "How Did We Discover the Periodic Table?",
    "related_may_defer": False,
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
    with open(EV / "ben_1045.log", "a") as f:
        f.write(line + "\n")


def dump(name: str, obj) -> None:
    EV.mkdir(parents=True, exist_ok=True)
    (EV / name).write_text(json.dumps(obj, indent=2, default=str) + "\n")


def shot(page, name: str, also_art: str | None = None) -> Path:
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    p = EV / name
    page.screenshot(path=str(p), full_page=False)
    if also_art:
        shutil.copy2(p, ART / also_art)
    return p


def ensure_hos(page) -> dict:
    ch = up.ensure_hos(page)
    log(f"CHANNEL_CHECK ok={ch.get('ok')} url={ch.get('url')}")
    if not ch.get("ok"):
        raise SystemExit(f"ABORT: channel check failed: {ch}")
    body = page.inner_text("body")[:3000]
    if re.search(r"\bOrbit With Ben\b|\bOppti\b", body, re.I) and "History of Science" not in body:
        raise SystemExit("ABORT: wrong channel (Orbit/Oppti)")
    return ch


def open_edit(page, vid: str) -> None:
    ensure_hos(page)
    page.goto(
        f"https://studio.youtube.com/video/{vid}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3500)
    up.dismiss(page)
    if HOS not in (page.url or "") and "studio.youtube.com/video/" not in (page.url or ""):
        # Studio edit URLs often omit channel id; re-verify via body
        body = page.inner_text("body")[:2500]
        if "History of Science" not in body and HANDLE not in body:
            # Soft: still on edit page for our video
            if f"/video/{vid}/" not in (page.url or ""):
                raise SystemExit(f"ABORT: not on expected edit page: {page.url}")


def read_related(page) -> dict:
    body = page.inner_text("body")
    m = re.search(r"Related video[^\n]{0,240}", body, re.I)
    line = m.group(0).strip() if m else ""
    out = {"line": line, "set": False, "title": None, "id_hint": None}
    if not line or re.search(r"Related video\s*(None|Add)", line, re.I):
        # Also look for selected card titles nearby
        if "Related video" in body:
            # Pull a wider window
            idx = body.lower().find("related video")
            window = body[idx : idx + 400] if idx >= 0 else ""
            out["window"] = window.replace("\n", " ")[:300]
            for tid, ttitle in (
                ("GHZDsiH7L7A", "What's Really Inside an Atom?"),
                ("AL_-qlWko_g", "How Did We Discover the Periodic Table?"),
                ("frP_YrNShsU", "How Did We Discover X-rays?"),
                ("_C92tIJCk8A", "How Did We Discover Germs?"),
            ):
                if tid in window or ttitle in window:
                    out["set"] = True
                    out["title"] = ttitle
                    out["id_hint"] = tid
                    break
        return out
    out["set"] = "None" not in line and "Add" not in line[:40]
    for tid, ttitle in (
        ("GHZDsiH7L7A", "What's Really Inside an Atom?"),
        ("AL_-qlWko_g", "How Did We Discover the Periodic Table?"),
        ("frP_YrNShsU", "How Did We Discover X-rays?"),
        ("_C92tIJCk8A", "How Did We Discover Germs?"),
    ):
        if tid in line or ttitle in line or ttitle in body[body.lower().find("related video") : body.lower().find("related video") + 500]:
            out["title"] = ttitle
            out["id_hint"] = tid
            out["set"] = True
            break
    return out


def dialog_save(page) -> dict:
    """Save visibility dialog — prefer Save, never Schedule/Publish/Premiere/Delete."""
    info = {"clicked": None, "enabled_candidates": []}
    # First try dialog footer Save
    hit = page.evaluate(
        """() => {
          const forbidden = /delete|publish|premiere|replace|schedule(?!d)/i;
          let hit = null;
          const walk = (r, d = 0) => {
            if (!r || d > 55 || hit) return;
            for (const el of (r.querySelectorAll
              ? r.querySelectorAll('button,ytcp-button,[role=button]') : [])) {
              const t = (el.innerText || el.getAttribute('aria-label') || '')
                .trim().replace(/\\s+/g, ' ');
              if (!t || t.length > 40) continue;
              const dis = el.disabled || el.getAttribute('aria-disabled') === 'true';
              const rect = el.getBoundingClientRect();
              if (rect.width < 10 || rect.height < 10) continue;
              if (/^Save$/i.test(t) && !dis) {
                el.click(); hit = {label: t, y: rect.y}; return;
              }
              if (/^Done$/i.test(t) && !dis && rect.y > 200) {
                // keep as fallback only
              }
            }
            for (const el of (r.querySelectorAll ? r.querySelectorAll('*') : []))
              if (el.shadowRoot) walk(el.shadowRoot, d + 1);
          };
          walk(document);
          if (hit) return hit;
          // Fallback Done in dialog
          const walk2 = (r, d = 0) => {
            if (!r || d > 55 || hit) return;
            for (const el of (r.querySelectorAll
              ? r.querySelectorAll('button,ytcp-button,[role=button]') : [])) {
              const t = (el.innerText || '').trim();
              const dis = el.disabled || el.getAttribute('aria-disabled') === 'true';
              if (/^Done$/i.test(t) && !dis) { el.click(); hit = {label: t}; return; }
            }
            for (const el of (r.querySelectorAll ? r.querySelectorAll('*') : []))
              if (el.shadowRoot) walk2(el.shadowRoot, d + 1);
          };
          walk2(document);
          return hit;
        }"""
    )
    info["clicked"] = hit
    page.wait_for_timeout(1500)
    # Confirm dialogs that say Update / Save — never Publish / Schedule / Delete
    for name in ["Update", "Save", "Confirm", "Yes", "OK", "Done"]:
        if name.lower() in ("publish", "schedule", "delete", "premiere"):
            continue
        try:
            b = page.get_by_role("button", name=re.compile(rf"^{re.escape(name)}$", re.I))
            if b.count() and b.first.is_visible():
                label = b.first.inner_text().strip()
                if re.search(r"publish|schedule|delete|premiere|replace", label, re.I):
                    continue
                b.first.click(force=True, timeout=1500)
                info["confirm"] = name
                page.wait_for_timeout(900)
        except Exception:
            pass
    # Also page-level Save if still dirty
    page.wait_for_timeout(800)
    ps = up.page_save(page)
    info["page_save"] = ps
    return info


def set_private(page) -> dict:
    out = {"chip_before": up.visibility_chip(page)}
    shot(page, "BEN_1045_tue_before_visibility.png")
    if not up.open_vis(page):
        # Try clicking Visibility chip text
        page.evaluate(
            """() => {
              const walk = (r, d = 0) => {
                if (!r || d > 55) return false;
                for (const el of (r.querySelectorAll ? r.querySelectorAll('*') : [])) {
                  const t = (el.innerText || '').replace(/\\s+/g, ' ').trim();
                  if (/^Visibility\\s+(Private|Public|Unlisted|Scheduled)/i.test(t)
                      && t.length < 140) {
                    el.click(); return true;
                  }
                }
                for (const el of (r.querySelectorAll ? r.querySelectorAll('*') : []))
                  if (el.shadowRoot && walk(el.shadowRoot, d + 1)) return true;
                return false;
              };
              return walk(document);
            }"""
        )
        page.wait_for_timeout(1400)
    shot(page, "BEN_1045_tue_vis_dialog.png")
    # Click Private radio — NEVER Public/Unlisted/Scheduled
    hit = up.click_radio(page, "Private")
    out["radio"] = hit
    page.wait_for_timeout(800)
    # Ensure Scheduled is NOT selected: if schedule date picker still active, Private should clear it
    shot(page, "BEN_1045_tue_private_selected.png")
    save_info = dialog_save(page)
    out["save"] = save_info
    page.wait_for_timeout(2500)
    up.dismiss(page)
    # Reload edit to confirm
    page.reload(wait_until="domcontentloaded", timeout=120000)
    page.wait_for_timeout(3000)
    up.dismiss(page)
    out["chip_after"] = up.visibility_chip(page)
    shot(page, "BEN_1045_tue_after_visibility.png", also_art="BEN_1045_tue_private.png")
    # Also copy the after shot as the primary art name
    shutil.copy2(EV / "BEN_1045_tue_after_visibility.png", ART / "BEN_1045_tue_private.png")
    out["private_ok"] = bool(
        re.search(r"Visibility\\s+Private\\b", out.get("chip_after") or "", re.I)
        or re.search(r"\\bPrivate\\b", out.get("chip_after") or "", re.I)
    ) and not re.search(r"Scheduled|Public|Unlisted", out.get("chip_after") or "", re.I)
    # Fix private_ok logic — chip is like "Visibility Private"
    chip = out.get("chip_after") or ""
    out["private_ok"] = (
        re.search(r"Private", chip, re.I) is not None
        and re.search(r"Scheduled|Public|Unlisted", chip, re.I) is None
    )
    return out


def check_audience_altered(page) -> dict:
    # Scroll details for audience / AI
    for _ in range(12):
        page.mouse.wheel(0, 900)
        page.wait_for_timeout(120)
    cos.show_more(page)
    page.wait_for_timeout(500)
    aud = cos.read_audience(page)
    ai = cos.read_ai_altered(page)
    # If AI section not found, try settings-ish scroll back and show more again
    if not ai.get("yes") and not ai.get("no"):
        page.keyboard.press("Home")
        page.wait_for_timeout(400)
        for _ in range(20):
            page.keyboard.press("PageDown")
            page.wait_for_timeout(80)
        cos.show_more(page)
        ai = cos.read_ai_altered(page)
        aud = cos.read_audience(page)
    return {"audience": aud, "altered": ai}


def scrape_shorts_list(page) -> list[dict]:
    ensure_hos(page)
    page.goto(
        f"https://studio.youtube.com/channel/{HOS}/videos/short",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(4500)
    up.dismiss(page)
    # Scroll to load all rows
    for _ in range(25):
        page.mouse.wheel(0, 1600)
        page.wait_for_timeout(250)
    page.keyboard.press("Home")
    page.wait_for_timeout(800)
    shot(page, "LIVE_SHORTS_CONTENT.png", also_art="BEN_1045_live_shorts_list.png")
    shutil.copy2(EV / "LIVE_SHORTS_CONTENT.png", ART / "BEN_1045_live_shorts_list.png")

    rows = page.evaluate(
        """() => {
          const out = [];
          const seen = new Set();
          const walk = (r, d = 0) => {
            if (!r || d > 60) return;
            const anchors = r.querySelectorAll
              ? r.querySelectorAll('a[href*="/video/"], a[href*="udvid="], a[href*="shorts/"]')
              : [];
            for (const a of anchors) {
              const href = a.getAttribute('href') || '';
              let id = null;
              let m = href.match(/\\/video\\/([A-Za-z0-9_-]{11})/);
              if (m) id = m[1];
              if (!id) {
                m = href.match(/[?&]udvid=([A-Za-z0-9_-]{11})/);
                if (m) id = m[1];
              }
              if (!id) {
                m = href.match(/shorts\\/([A-Za-z0-9_-]{11})/);
                if (m) id = m[1];
              }
              if (!id || seen.has(id)) continue;
              // climb for row text
              let el = a;
              let text = '';
              for (let i = 0; i < 8 && el; i++) {
                const t = (el.innerText || '').replace(/\\s+/g, ' ').trim();
                if (t.length > text.length && t.length < 800) text = t;
                el = el.parentElement;
              }
              const title = (a.innerText || a.getAttribute('aria-label') || '')
                .replace(/\\s+/g, ' ').trim().slice(0, 200);
              let visibility = '';
              if (/\\bPrivate\\b/i.test(text)) visibility = 'Private';
              else if (/\\bUnlisted\\b/i.test(text)) visibility = 'Unlisted';
              else if (/\\bScheduled\\b/i.test(text)) visibility = 'Scheduled';
              else if (/\\bDraft\\b/i.test(text)) visibility = 'Draft';
              else if (/\\bPublic\\b/i.test(text)) visibility = 'Public';
              let date = '';
              const dm = text.match(
                /(?:Scheduled for|Published|Uploaded)?\\s*(?:on\\s*)?(\\d{1,2}\\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\\w*(?:\\s+\\d{4})?(?:\\s*[·,]?\\s*\\d{1,2}:\\d{2})?)/i
              );
              if (dm) date = dm[1].trim();
              else {
                const dm2 = text.match(
                  /((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\\w*\\s+\\d{1,2},?\\s+\\d{4}(?:\\s*[·,]?\\s*\\d{1,2}:\\d{2})?)/i
                );
                if (dm2) date = dm2[1].trim();
              }
              seen.add(id);
              out.push({
                id, title: title || null, visibility: visibility || null,
                date: date || null, row_text: text.slice(0, 280), href
              });
            }
            for (const el of (r.querySelectorAll ? r.querySelectorAll('*') : []))
              if (el.shadowRoot) walk(el.shadowRoot, d + 1);
          };
          walk(document);
          return out;
        }"""
    )

    # Enrich missing titles/visibility by clicking each row if needed
    enriched = []
    for row in rows:
        item = dict(row)
        if not item.get("title") or item["title"] in ("Edit video", "Edit", ""):
            # title often in aria-label of thumbnail
            pass
        enriched.append(item)

    # Second pass: parse body table lines as backup
    body = page.inner_text("body")
    # Also collect from ytcp-video-row if evaluate missed titles
    more = page.evaluate(
        """() => {
          const out = [];
          const walk = (r, d = 0) => {
            if (!r || d > 55) return;
            const rows = r.querySelectorAll
              ? r.querySelectorAll('ytcp-video-row, #video-title, ytcp-video-list-cell-video')
              : [];
            for (const row of rows) {
              const t = (row.innerText || '').replace(/\\s+/g, ' ').trim();
              if (t.length < 5) continue;
              out.push(t.slice(0, 400));
            }
            // also any element with data-video-id
            for (const el of (r.querySelectorAll ? r.querySelectorAll('[data-video-id]') : [])) {
              out.push({
                id: el.getAttribute('data-video-id'),
                text: (el.innerText || '').replace(/\\s+/g, ' ').trim().slice(0, 300)
              });
            }
            for (const el of (r.querySelectorAll ? r.querySelectorAll('*') : []))
              if (el.shadowRoot) walk(el.shadowRoot, d + 1);
          };
          walk(document);
          return out;
        }"""
    )
    return {"rows": enriched, "raw_row_texts": more[:80], "body_snip": body[:4000]}


def enrich_ids_by_click(page, rows: list[dict]) -> list[dict]:
    """If title is weak, open each edit briefly — but prefer list data.

    We already have ids from hrefs. Click each Shorts row link title area only if
    visibility/date missing — actually user asked to get id from URL when clicking.
    We'll navigate list and for each unique id already collected, fill gaps from edit
    page only when title empty.
    """
    out = []
    for r in rows:
        item = dict(r)
        if item.get("title") and item["title"] not in ("Edit video", "Edit") and item.get("visibility"):
            out.append(item)
            continue
        # Open edit lightly for missing fields
        try:
            page.goto(
                f"https://studio.youtube.com/video/{item['id']}/edit",
                wait_until="domcontentloaded",
                timeout=90000,
            )
            page.wait_for_timeout(2200)
            up.dismiss(page)
            # Title from input
            title = page.evaluate(
                """() => {
                  const walk = (r, d = 0) => {
                    if (!r || d > 50) return null;
                    for (const el of (r.querySelectorAll
                      ? r.querySelectorAll('input,textarea,#textbox') : [])) {
                      const al = (el.getAttribute('aria-label') || '').toLowerCase();
                      if (al.includes('title') || el.id === 'textbox') {
                        const v = el.value || el.innerText || '';
                        if (v && v.trim().length > 2) return v.trim().slice(0, 200);
                      }
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
            chip = up.visibility_chip(page)
            if title:
                item["title"] = title
            if chip:
                item["visibility_chip"] = chip
                if "Private" in chip and "Scheduled" not in chip:
                    item["visibility"] = "Private"
                elif "Scheduled" in chip:
                    item["visibility"] = "Scheduled"
                    m = re.search(r"Scheduled\\s+(.+)$", chip, re.I)
                    if m:
                        item["date"] = m.group(1).strip()
                elif "Unlisted" in chip:
                    item["visibility"] = "Unlisted"
                elif "Public" in chip:
                    item["visibility"] = "Public"
            item["enriched_from_edit"] = True
        except Exception as e:
            item["enrich_err"] = str(e)
        out.append(item)
    return out


def confirm_scheduled(page, job: dict) -> dict:
    open_edit(page, job["id"])
    ensure_hos(page)
    chip = up.visibility_chip(page)
    shot_name = f"BEN_1045_{job['slot']}_confirm.png"
    # Scroll for related / audience / altered
    for _ in range(14):
        page.mouse.wheel(0, 900)
        page.wait_for_timeout(100)
    cos.show_more(page)
    aud = cos.read_audience(page)
    ai = cos.read_ai_altered(page)
    page.keyboard.press("Home")
    page.wait_for_timeout(400)
    for _ in range(10):
        page.mouse.wheel(0, 1000)
        page.wait_for_timeout(100)
    related = read_related(page)
    # Screenshot showing visibility + as much settings as possible
    page.keyboard.press("Home")
    page.wait_for_timeout(500)
    shot(page, shot_name, also_art=shot_name)
    shutil.copy2(EV / shot_name, ART / shot_name)

    body = page.inner_text("body")
    date_pat = job["expect_date"].replace(" ", r"\s+")
    alt_pat = (
        r"16\s+October|16\s+Oct|October\s+16"
        if "16" in job["expect_date"]
        else r"18\s+October|18\s+Oct|October\s+18"
    )
    date_ok = bool(
        re.search(date_pat, chip + " " + body, re.I)
        or re.search(alt_pat, chip + " " + body, re.I)
    )
    time_ok = "11:30" in (chip + body) or "11.30" in (chip + body)
    scheduled_ok = "Scheduled" in chip and date_ok and time_ok

    related_status = "unset"
    if related.get("set") and related.get("id_hint") == job["related_id"]:
        related_status = "set"
    elif related.get("set") and related.get("title") == job["related_title"]:
        related_status = "set"
    elif job.get("related_may_defer") and (
        not related.get("set")
        or related.get("id_hint") != job["related_id"]
    ):
        # Check if 004 title appears
        if related.get("id_hint") == job["related_id"] or related.get("title") == job["related_title"]:
            related_status = "set"
        else:
            related_status = "deferred_or_unset"
    elif related.get("line"):
        related_status = f"other:{related.get('title') or related.get('line')[:80]}"

    altered_yes = bool(ai.get("yes")) or (
        isinstance(ai.get("radios"), list)
        and any(r.get("checked") and "Yes" in str(r.get("label", "")) for r in ai.get("radios", []))
    )

    return {
        "slot": job["slot"],
        "id": job["id"],
        "title_expected": job["title"],
        "visibility_chip": chip,
        "scheduled_ok": scheduled_ok,
        "date_ok": date_ok,
        "time_ok": time_ok,
        "audience": aud,
        "audience_not_kids": bool(aud.get("ok_not_kids")) and not aud.get("fail_kids"),
        "altered": ai,
        "altered_yes": altered_yes,
        "related": related,
        "related_status": related_status,
        "screenshot": shot_name,
        "ok": scheduled_ok
        and bool(aud.get("ok_not_kids"))
        and not aud.get("fail_kids"),
    }


def write_list_files(shorts: list[dict]) -> None:
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
    result = {
        "channel": HANDLE,
        "channelId": HOS,
        "started": datetime.now(LONDON).isoformat(timespec="seconds"),
    }
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

        # --- 1) Privatize Tue Short ---
        log("=== TASK 1: Privatize CUu8k38iAMc ===")
        open_edit(page, TUE_ID)
        ensure_hos(page)
        priv = set_private(page)
        post = check_audience_altered(page)
        priv["post_checks"] = post
        # Re-confirm chip after audience scroll
        page.keyboard.press("Home")
        page.wait_for_timeout(500)
        priv["chip_final"] = up.visibility_chip(page)
        chip = priv.get("chip_final") or priv.get("chip_after") or ""
        priv["private_ok"] = (
            re.search(r"Private", chip, re.I) is not None
            and re.search(r"Scheduled|Public|Unlisted", chip, re.I) is None
        )
        shot(page, "BEN_1045_tue_final.png", also_art="BEN_1045_tue_private.png")
        shutil.copy2(EV / "BEN_1045_tue_final.png", ART / "BEN_1045_tue_private.png")
        result["tue_private"] = priv
        dump("BEN_1045_TUE_PRIVATE.json", priv)
        log(f"TUE private_ok={priv['private_ok']} chip={chip!r}")

        # --- 2) Scrape Shorts list ---
        log("=== TASK 2: Scrape Shorts content list ===")
        ensure_hos(page)
        scraped = scrape_shorts_list(page)
        rows = scraped["rows"]
        log(f"scraped raw rows={len(rows)}")
        # Enrich any weak rows
        need = [r for r in rows if not r.get("title") or not r.get("visibility")]
        if need:
            log(f"enriching {len(need)} rows via edit pages")
            # Only enrich missing; keep already-good
            good = [r for r in rows if r.get("title") and r.get("visibility")]
            enriched = enrich_ids_by_click(page, need)
            # Dedupe by id
            by_id = {r["id"]: r for r in good + enriched}
            rows = list(by_id.values())
        else:
            # Still visit list once more for a clean screenshot after scroll-top
            page.goto(
                f"https://studio.youtube.com/channel/{HOS}/videos/short",
                wait_until="domcontentloaded",
                timeout=120000,
            )
            page.wait_for_timeout(3000)
            up.dismiss(page)
            shot(page, "LIVE_SHORTS_CONTENT.png", also_art="BEN_1045_live_shorts_list.png")
            shutil.copy2(EV / "LIVE_SHORTS_CONTENT.png", ART / "BEN_1045_live_shorts_list.png")

        # If titles still look like "Edit video", enrich all
        if any(
            not r.get("title") or r.get("title") in ("Edit video", "Edit") for r in rows
        ):
            rows = enrich_ids_by_click(page, rows)
            # Reshoot list
            page.goto(
                f"https://studio.youtube.com/channel/{HOS}/videos/short",
                wait_until="domcontentloaded",
                timeout=120000,
            )
            page.wait_for_timeout(3000)
            up.dismiss(page)
            shot(page, "LIVE_SHORTS_CONTENT.png", also_art="BEN_1045_live_shorts_list.png")
            shutil.copy2(EV / "LIVE_SHORTS_CONTENT.png", ART / "BEN_1045_live_shorts_list.png")

        write_list_files(rows)
        result["shorts_count"] = len(rows)
        result["shorts"] = rows
        dump("LIVE_SHORTS_SCRAPE_RAW.json", scraped)
        log(f"LIVE_SHORTS_LIST written count={len(rows)}")

        # --- 3) Confirm Fri / Sun ---
        log("=== TASK 3: Confirm Fri + Sun scheduled ===")
        fri = confirm_scheduled(page, FRI)
        sun = confirm_scheduled(page, SUN)
        result["fri"] = fri
        result["sun"] = sun
        dump("BEN_1045_FRI_CONFIRM.json", fri)
        dump("BEN_1045_SUN_CONFIRM.json", sun)
        log(f"FRI ok={fri.get('ok')} chip={fri.get('visibility_chip')!r} related={fri.get('related_status')}")
        log(f"SUN ok={sun.get('ok')} chip={sun.get('visibility_chip')!r} related={sun.get('related_status')}")

        result["ended"] = datetime.now(LONDON).isoformat(timespec="seconds")
        result["ok"] = bool(priv.get("private_ok")) and bool(fri.get("ok")) and bool(sun.get("ok"))
        dump("BEN_1045_RESULT.json", result)
        log(f"DONE ok={result['ok']}")
        print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
