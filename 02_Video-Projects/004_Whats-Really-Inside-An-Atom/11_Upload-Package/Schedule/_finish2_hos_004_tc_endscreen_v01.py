#!/usr/bin/env python3
"""HOS 004 Studio finish pass 2: T&C + end screen → 002 + Subscribe.
CDP :9460 · HOS profile only. No .env. Never Orbit."""
from __future__ import annotations

import json
import re
import time
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
RELATED_TITLE = "How Did We Discover the Periodic Table?"

PROJ = Path(__file__).resolve().parents[2]
PKG = PROJ / "11_Upload-Package"
EV = PKG / "Schedule/evidence_2026-09-29_studio"
ART = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts"

THUMB_A = PROJ / "08_Thumbnail/Selected/hos_004_thumb_A_atom_live_v04.jpg"
THUMB_B = PROJ / "08_Thumbnail/Selected/hos_004_thumb_B_cut_gold_live_v04.jpg"
THUMB_C = PROJ / "08_Thumbnail/Selected/hos_004_thumb_C_hidden_number_live_v06.jpg"
PIN = (PKG / "Pinned-Comments/atom_long_pinned-comment_v01.txt").read_text().strip()


def log(msg: str) -> None:
    EV.mkdir(parents=True, exist_ok=True)
    line = f"{datetime.now().isoformat(timespec='seconds')} {msg}"
    print(line, flush=True)
    with (EV / "finish2.log").open("a") as f:
        f.write(line + "\n")


def dump(name: str, obj) -> None:
    EV.mkdir(parents=True, exist_ok=True)
    (EV / name).write_text(json.dumps(obj, indent=2) + "\n")
    try:
        ART.mkdir(parents=True, exist_ok=True)
        (ART / f"hos_004_{name}").write_text(json.dumps(obj, indent=2) + "\n")
    except Exception:
        pass


def shot(page, name: str) -> str:
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    dest = EV / name
    page.screenshot(path=str(dest), full_page=False)
    try:
        (ART / f"hos_004_{name}").write_bytes(dest.read_bytes())
    except Exception:
        pass
    return str(dest)


def snip(page, n: int = 3000) -> str:
    try:
        return page.inner_text("body")[:n]
    except Exception as e:
        return f"<err {e}>"


def dismiss(page) -> None:
    for name in ["Got it", "Dismiss", "Not now", "No thanks", "Skip", "Close"]:
        try:
            b = page.get_by_role("button", name=re.compile(rf"^{name}$", re.I))
            if b.count() and b.first.is_visible():
                b.first.click(timeout=1500)
                page.wait_for_timeout(400)
        except Exception:
            pass


def click_shadow_text(page, pattern: str, timeout_ms: int = 4000) -> str | None:
    """Click first visible element whose text matches pattern (incl. shadow)."""
    js = """(pattern) => {
      const re = new RegExp(pattern, 'i');
      const walk = (root, depth=0) => {
        if (!root || depth > 45) return null;
        const nodes = root.querySelectorAll
          ? root.querySelectorAll('button, a, [role="button"], tp-yt-paper-button, ytcp-button, span, div, yt-formatted-string')
          : [];
        for (const el of nodes) {
          const t = (el.innerText || el.textContent || '').trim().replace(/\\s+/g, ' ');
          if (!t || t.length > 120) continue;
          if (!re.test(t)) continue;
          const r = el.getBoundingClientRect();
          if (r.width < 2 || r.height < 2) continue;
          el.click();
          return t.slice(0, 80);
        }
        for (const el of (root.querySelectorAll ? root.querySelectorAll('*') : [])) {
          if (el.shadowRoot) {
            const hit = walk(el.shadowRoot, depth + 1);
            if (hit) return hit;
          }
        }
        return null;
      };
      return walk(document);
    }"""
    try:
        hit = page.evaluate(js, pattern)
        if hit:
            page.wait_for_timeout(600)
            return hit
    except Exception:
        pass
    # Playwright role fallback
    try:
        loc = page.get_by_role("button", name=re.compile(pattern, re.I))
        if loc.count():
            loc.first.click(timeout=timeout_ms)
            page.wait_for_timeout(600)
            return loc.first.inner_text()[:80]
    except Exception:
        pass
    try:
        loc = page.get_by_text(re.compile(pattern, re.I))
        if loc.count():
            loc.first.click(timeout=timeout_ms)
            page.wait_for_timeout(600)
            return loc.first.inner_text()[:80]
    except Exception:
        pass
    return None


def ensure_hos(page) -> dict:
    page.goto(
        f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3500)
    dismiss(page)
    body = snip(page, 2500)
    url = page.url
    ok = (
        CHANNEL in url
        and ("History of Science" in body or HANDLE in body)
        and "Sign in" not in body
        and "orbit" not in body.lower()
    )
    # Reject wrong channel
    if re.search(r"@OrbitWithBen|orbit with ben", body, re.I):
        ok = False
    return {
        "ok": ok,
        "url": url,
        "snip": body[:400],
        "handle": HANDLE if ok else "UNKNOWN",
    }


def verify_schedule(page) -> dict:
    page.goto(
        f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3500)
    dismiss(page)
    shot(page, "200_content_verify.png")
    body = snip(page, 4000)
    # Hover visibility for tooltip
    try:
        page.locator("text=Scheduled").first.hover(timeout=4000)
        page.wait_for_timeout(800)
        shot(page, "201_schedule_tooltip.png")
    except Exception:
        pass
    tip = snip(page, 4000)
    return {
        "has15": bool(re.search(r"15\s*(Oct|October)\s*2026", body + tip, re.I)),
        "has1800": bool(re.search(r"18:00", body + tip)),
        "scheduled": bool(re.search(r"Scheduled", body, re.I)),
        "private_until": bool(
            re.search(r"private.*scheduled|scheduled to become public", tip, re.I)
        ),
        "premiere": bool(re.search(r"Premiere", body + tip))
        and not bool(re.search(r"Set as Premiere", tip)),
        "body_snip": body[:800],
        "tip_snip": tip[:800],
    }


def do_ab_test(page) -> dict:
    info: dict = {
        "wanted": "Title and thumbnail",
        "pairs": [
            {"title": TITLE, "thumb": THUMB_A.name},
            {"title": TITLE_2, "thumb": THUMB_C.name},
            {"title": TITLE_3, "thumb": THUMB_B.name},
        ],
    }
    page.goto(
        f"https://studio.youtube.com/video/{VIDEO_ID}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(4000)
    dismiss(page)
    shot(page, "210_edit.png")
    body0 = snip(page, 2000)
    info["edit_snip"] = body0[:600]
    if "Oops" in body0 or "something went wrong" in body0.lower():
        # retry once
        page.reload(wait_until="domcontentloaded")
        page.wait_for_timeout(4000)
        dismiss(page)
        shot(page, "210b_edit_retry.png")

    # Open A/B Testing
    hit = click_shadow_text(page, r"A/B Testing|Test & Compare|Test and compare|A/B Test")
    info["open"] = hit
    page.wait_for_timeout(2500)
    shot(page, "211_ab_open.png")
    body = snip(page, 5000)
    info["ui_snip"] = body[:1800]

    offers = []
    for label in [
        "Title and thumbnail",
        "Titles and thumbnails",
        "Thumbnail",
        "Title",
        "Thumbnail only",
        "Title only",
    ]:
        if re.search(re.escape(label), body, re.I):
            offers.append(label)
    info["offers"] = offers

    # Prefer combined; else set what Studio allows
    chosen = None
    for label in [
        "Title and thumbnail",
        "Titles and thumbnails",
        "Thumbnail",
        "Title",
    ]:
        if click_shadow_text(page, rf"^{re.escape(label)}$"):
            chosen = label
            break
        # also try without anchors
        if label.lower() in body.lower() and click_shadow_text(page, re.escape(label)):
            chosen = label
            break
    info["chosen"] = chosen
    page.wait_for_timeout(2500)
    shot(page, "212_ab_type.png")
    body2 = snip(page, 4000)
    info["after_type_snip"] = body2[:1200]

    if not chosen:
        info["ok"] = False
        info["reason"] = "could_not_select_test_type"
        return info

    # Upload thumbs for thumbnail or title+thumbnail tests
    thumb_uploads = []
    if re.search(r"thumbnail", chosen, re.I):
        # Ensure variant 1 = A (often already set as current)
        # Fill file inputs for remaining variants with C then B
        for thumb in (THUMB_A, THUMB_C, THUMB_B):
            try:
                loc = page.locator('input[type="file"]')
                n = loc.count()
                for i in range(n):
                    acc = (loc.nth(i).get_attribute("accept") or "").lower()
                    if "image" in acc or "jpeg" in acc or "jpg" in acc or not acc:
                        try:
                            # only set empty / last unused
                            loc.nth(i).set_input_files(str(thumb))
                            thumb_uploads.append({"i": i, "file": thumb.name})
                            page.wait_for_timeout(1500)
                            break
                        except Exception as e:
                            thumb_uploads.append(
                                {"i": i, "file": thumb.name, "err": type(e).__name__}
                            )
            except Exception as e:
                thumb_uploads.append({"file": thumb.name, "err": type(e).__name__})
        info["thumb_uploads"] = thumb_uploads

    # Fill titles for title or title+thumbnail
    titles_filled = []
    if re.search(r"title", chosen, re.I):
        for title in (TITLE, TITLE_2, TITLE_3):
            try:
                filled = page.evaluate(
                    """(title) => {
                      const walk=(r,d=0)=>{
                        if(!r||d>45) return false;
                        const inputs = r.querySelectorAll
                          ? r.querySelectorAll('input, textarea, [contenteditable="true"]')
                          : [];
                        for (const inp of inputs) {
                          const aria=((inp.getAttribute('aria-label')||'')
                            +(inp.placeholder||'')+(inp.getAttribute('label')||'')).toLowerCase();
                          const isTitle = /title/.test(aria) || inp.getAttribute('maxlength')==='100';
                          if (!isTitle) continue;
                          const val = (inp.value !== undefined ? inp.value : (inp.innerText||'')).trim();
                          if (val) continue;
                          if (inp.isContentEditable) {
                            inp.focus(); inp.innerText = title;
                            inp.dispatchEvent(new Event('input',{bubbles:true}));
                            return true;
                          }
                          inp.focus();
                          inp.value = title;
                          inp.dispatchEvent(new Event('input',{bubbles:true}));
                          inp.dispatchEvent(new Event('change',{bubbles:true}));
                          return true;
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
                titles_filled.append({"title": title, "filled": bool(filled)})
                page.wait_for_timeout(500)
            except Exception as e:
                titles_filled.append({"title": title, "err": type(e).__name__})
        info["titles_filled"] = titles_filled

    shot(page, "213_ab_filled.png")

    # Start test
    start = None
    for pat in [r"^Start$", r"^Start test$", r"^Create$", r"^Save$", r"^Done$", r"^Next$"]:
        start = click_shadow_text(page, pat)
        if start:
            break
    info["start"] = start
    page.wait_for_timeout(3000)
    shot(page, "214_ab_after_start.png")
    info["after"] = snip(page, 1500)
    info["running"] = bool(
        re.search(r"A/B test running|test running|Test running", info["after"], re.I)
    )
    info["ok"] = True
    info["note"] = (
        f"Studio offered {offers}; selected {chosen}. "
        "Set what the UI allowed without guessing beyond that."
    )
    return info


def do_end_screen(page) -> dict:
    info: dict = {"related": RELATED_002, "relatedTitle": RELATED_TITLE, "subscribe": True}
    page.goto(
        f"https://studio.youtube.com/video/{VIDEO_ID}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3500)
    dismiss(page)
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
    shot(page, "220_endscreen_open.png")
    body = snip(page, 3000)
    info["open_snip"] = body[:800]

    # If existing "Most recent upload" — click it to edit / change video
    # Prefer template "1 video, 1 subscribe" only if empty
    has_elements = bool(
        re.search(r"Subscribe:|Most recent|Video element|AL_-qlWko_g|Periodic Table", body, re.I)
    )
    info["has_elements"] = has_elements

    if not has_elements:
        # Use template
        click_shadow_text(page, r"1 video,? 1 subscribe")
        page.wait_for_timeout(1500)
        shot(page, "221_template.png")

    # Click the video element to change from Most recent → specific 002
    changed = False
    for pat in [
        r"Most recent upload",
        r"^Video$",
        r"Video element",
        r"Change$",
        r"Edit$",
    ]:
        if click_shadow_text(page, pat):
            page.wait_for_timeout(1200)
            break

    # Look for "Specific video" / "Video from channel" radio
    for pat in [
        r"Specific video",
        r"Choose a video",
        r"Video from your channel",
        r"Select a video",
    ]:
        if click_shadow_text(page, pat):
            page.wait_for_timeout(1000)
            info["mode"] = pat
            break

    # Search box for 002
    try:
        # Prefer filling any search/textbox in dialog
        filled = page.evaluate(
            """(q) => {
              const walk=(r,d=0)=>{
                if(!r||d>45) return false;
                const inputs = r.querySelectorAll
                  ? r.querySelectorAll('input, textarea')
                  : [];
                for (const inp of inputs) {
                  const aria=((inp.getAttribute('aria-label')||'')
                    +(inp.placeholder||'')+(inp.type||'')).toLowerCase();
                  if (/search|video|url|id/.test(aria) || inp.type==='search' || inp.type==='text') {
                    inp.focus();
                    inp.value = q;
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
            RELATED_TITLE,
        )
        info["search_filled"] = bool(filled)
        if filled:
            page.keyboard.press("Enter")
            page.wait_for_timeout(2000)
    except Exception as e:
        info["search_err"] = type(e).__name__

    # Click result
    if click_shadow_text(page, r"Periodic Table|AL_-qlWko_g|How Did We Discover"):
        changed = True
        page.wait_for_timeout(1200)
    info["changed_to_002"] = changed
    shot(page, "222_endscreen_picked.png")

    # Ensure Subscribe exists
    body3 = snip(page, 3000)
    if not re.search(r"Subscribe", body3, re.I):
        click_shadow_text(page, r"^\+?\s*Element$|^Add element$")
        page.wait_for_timeout(800)
        click_shadow_text(page, r"^Subscribe$")
        page.wait_for_timeout(800)

    shot(page, "223_endscreen_before_save.png")
    save = click_shadow_text(page, r"^Save$")
    info["save"] = save
    page.wait_for_timeout(2500)
    # confirm dialog if any
    click_shadow_text(page, r"^Save$|^Confirm$|^OK$")
    page.wait_for_timeout(1500)
    shot(page, "224_endscreen_saved.png")
    after = snip(page, 2500)
    info["after_snip"] = after[:1000]
    info["has_002"] = bool(
        re.search(r"AL_-qlWko_g|Periodic Table|How Did We Discover the Periodic", after, re.I)
    )
    info["has_subscribe"] = bool(re.search(r"Subscribe", after, re.I))
    info["still_most_recent"] = bool(re.search(r"Most recent upload", after, re.I))
    info["ok"] = bool(info.get("save") and (info["has_002"] or not info["still_most_recent"]))
    if info["still_most_recent"] and not info["has_002"]:
        info["ok"] = False
        info["note"] = (
            "End screen still Most recent upload — could not bind AL_-qlWko_g in UI; "
            "Subscribe present. Manual bind of 002 needed."
        )
    return info


def try_pin(page) -> dict:
    info: dict = {"text": PIN[:120]}
    page.goto(
        f"https://www.youtube.com/watch?v={VIDEO_ID}",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3500)
    shot(page, "230_watch.png")
    body = snip(page, 2000)
    if re.search(r"private|unavailable|scheduled|premiere", body, re.I):
        info["ok"] = False
        info["reason"] = "watch_page_not_commentable_while_scheduled_or_private"
        info["note"] = "Pin on launch day (15 Oct 2026) — Studio blocks comments on scheduled private."
        return info
    # Studio comments
    page.goto(
        f"https://studio.youtube.com/video/{VIDEO_ID}/comments",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3000)
    shot(page, "231_comments.png")
    info["ok"] = False
    info["note"] = "Pin deferred to launch day."
    return info


def main() -> int:
    EV.mkdir(parents=True, exist_ok=True)
    (EV / "finish2.log").write_text("")
    result: dict = {
        "ok": False,
        "videoId": VIDEO_ID,
        "channel": HANDLE,
        "channelId": CHANNEL,
        "at": datetime.now().isoformat(timespec="seconds"),
    }
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        ctx = browser.contexts[0]
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        try:
            hos = ensure_hos(page)
            result["channelCheck"] = hos
            shot(page, "205_channel.png")
            if not hos.get("ok"):
                dump("FINISH2_RESULT.json", result)
                log(f"STOP channel check failed: {hos}")
                return 2

            result["schedule"] = verify_schedule(page)
            log(f"schedule={result['schedule']}")

            result["abTest"] = do_ab_test(page)
            log(f"abTest chosen={result['abTest'].get('chosen')} offers={result['abTest'].get('offers')}")

            result["endScreen"] = do_end_screen(page)
            log(f"endScreen={ {k:result['endScreen'].get(k) for k in ('ok','has_002','has_subscribe','still_most_recent','save')} }")

            result["pin"] = try_pin(page)
            log(f"pin={result['pin']}")

            # Final schedule proof
            result["scheduleFinal"] = verify_schedule(page)
            shot(page, "240_final_content.png")

            result["ok"] = bool(
                result["channelCheck"].get("ok")
                and result["scheduleFinal"].get("has15")
                and result["scheduleFinal"].get("scheduled")
            )
            dump("FINISH2_RESULT.json", result)
            log(f"DONE ok={result['ok']}")
            return 0 if result["ok"] else 1
        except Exception as e:
            result["error"] = f"{type(e).__name__}: {e}"
            dump("FINISH2_RESULT.json", result)
            log(f"ERROR {result['error']}")
            return 3


if __name__ == "__main__":
    raise SystemExit(main())
