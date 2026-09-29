#!/usr/bin/env python3
"""HOS 004 Studio finish pass 3: restore thumb A · real A/B dialog · end screen 002.
CDP :9460 · HOS profile only. No .env. Never Orbit."""
from __future__ import annotations

import json
import re
import subprocess
import time
import urllib.request
from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright

PORT = 9460
CDP = f"http://127.0.0.1:{PORT}"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PROFILE = str(Path.home() / ".hos-chrome-youtube-studio")
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
    with (EV / "finish3.log").open("a") as f:
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


def chrome_up() -> bool:
    try:
        with urllib.request.urlopen(f"{CDP}/json/version", timeout=2) as r:
            return r.status == 200
    except Exception:
        return False


def ensure_chrome() -> None:
    if chrome_up():
        log("cdp already up")
        return
    Path(PROFILE).mkdir(parents=True, exist_ok=True)
    for name in ("SingletonLock", "SingletonSocket", "SingletonCookie"):
        p = Path(PROFILE) / name
        try:
            p.unlink()
        except FileNotFoundError:
            pass
    log_path = "/tmp/hos_chrome_9460_004_finish3.log"
    subprocess.Popen(
        [
            CHROME,
            f"--remote-debugging-port={PORT}",
            "--remote-allow-origins=*",
            f"--user-data-dir={PROFILE}",
            "--profile-directory=Default",
            "--no-first-run",
            "--no-default-browser-check",
            f"https://studio.youtube.com/channel/{CHANNEL}",
        ],
        stdout=open(log_path, "ab"),
        stderr=subprocess.STDOUT,
    )
    for _ in range(50):
        if chrome_up():
            log("cdp started")
            return
        time.sleep(0.5)
    raise SystemExit("CDP :9460 failed to start")


def dismiss(page) -> None:
    for name in ["Got it", "Dismiss", "Not now", "No thanks", "Skip", "Close"]:
        try:
            b = page.get_by_role("button", name=re.compile(rf"^{name}$", re.I))
            if b.count() and b.first.is_visible():
                b.first.click(timeout=1200)
                page.wait_for_timeout(300)
        except Exception:
            pass
    # Escape open Create menu
    try:
        page.keyboard.press("Escape")
        page.wait_for_timeout(200)
    except Exception:
        pass


def click_exact_ab_testing(page) -> str | None:
    """Click the A/B Testing control under the title — not Create, not Thumbnail label."""
    # Prefer Playwright get_by_role near title
    for role in ("button", "link"):
        try:
            loc = page.get_by_role(role, name=re.compile(r"^A/B Testing$", re.I))
            if loc.count():
                loc.first.click(timeout=5000)
                page.wait_for_timeout(1500)
                return f"role:{role}"
        except Exception:
            pass
    # Shadow walk — only short exact match
    try:
        hit = page.evaluate(
            """() => {
              const walk = (root, depth=0) => {
                if (!root || depth > 45) return null;
                const nodes = root.querySelectorAll
                  ? root.querySelectorAll('button, a, [role="button"], ytcp-button, tp-yt-paper-button')
                  : [];
                for (const el of nodes) {
                  const t = (el.innerText || el.textContent || '').trim().replace(/\\s+/g, ' ');
                  if (t !== 'A/B Testing' && t !== 'Test & Compare' && t !== 'Test and compare') continue;
                  const r = el.getBoundingClientRect();
                  if (r.width < 10 || r.height < 10) continue;
                  // Prefer left column (not top Create)
                  if (r.y < 80) continue;
                  el.click();
                  return t + '@' + Math.round(r.x) + ',' + Math.round(r.y);
                }
                for (const el of (root.querySelectorAll ? root.querySelectorAll('*') : [])) {
                  if (el.shadowRoot) {
                    const h = walk(el.shadowRoot, depth + 1);
                    if (h) return h;
                  }
                }
                return null;
              };
              return walk(document);
            }"""
        )
        if hit:
            page.wait_for_timeout(1500)
            return hit
    except Exception:
        pass
    return None


def click_in_dialog(page, pattern: str) -> str | None:
    """Click matching text inside any open dialog/modal."""
    try:
        # Prefer dialogs
        for sel in (
            "tp-yt-paper-dialog",
            "ytcp-dialog",
            "[role='dialog']",
            "ytcp-uploads-dialog",
        ):
            dlg = page.locator(sel)
            if not dlg.count():
                continue
            btn = dlg.get_by_role("button", name=re.compile(pattern, re.I))
            if btn.count():
                btn.first.click(timeout=4000)
                page.wait_for_timeout(800)
                return f"dlg:{pattern}"
            txt = dlg.get_by_text(re.compile(pattern, re.I))
            if txt.count():
                txt.first.click(timeout=4000)
                page.wait_for_timeout(800)
                return f"dlgtext:{pattern}"
    except Exception:
        pass
    try:
        hit = page.evaluate(
            """(pattern) => {
              const re = new RegExp(pattern, 'i');
              const walk = (root, depth=0) => {
                if (!root || depth > 45) return null;
                const nodes = root.querySelectorAll
                  ? root.querySelectorAll('button, a, [role="button"], [role="radio"], [role="option"], ytcp-button, span, div')
                  : [];
                for (const el of nodes) {
                  const t = (el.innerText || el.textContent || '').trim().replace(/\\s+/g, ' ');
                  if (!t || t.length > 80) continue;
                  if (!re.test(t)) continue;
                  const r = el.getBoundingClientRect();
                  if (r.width < 4 || r.height < 4) continue;
                  el.click();
                  return t.slice(0, 80);
                }
                for (const el of (root.querySelectorAll ? root.querySelectorAll('*') : [])) {
                  if (el.shadowRoot) {
                    const h = walk(el.shadowRoot, depth + 1);
                    if (h) return h;
                  }
                }
                return null;
              };
              return walk(document);
            }""",
            pattern,
        )
        if hit:
            page.wait_for_timeout(800)
            return hit
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
        and not re.search(r"@OrbitWithBen|orbit with ben", body, re.I)
    )
    return {"ok": ok, "url": url, "snip": body[:400]}


def restore_thumb_a(page) -> dict:
    info: dict = {"file": THUMB_A.name}
    page.goto(
        f"https://studio.youtube.com/video/{VIDEO_ID}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(4000)
    dismiss(page)
    shot(page, "300_edit_before_thumb.png")
    try:
        loc = page.locator('input[type="file"]')
        set_ok = False
        for i in range(loc.count()):
            acc = (loc.nth(i).get_attribute("accept") or "").lower()
            if "image" in acc or "jpeg" in acc or "jpg" in acc or ".jpg" in acc:
                loc.nth(i).set_input_files(str(THUMB_A))
                set_ok = True
                info["via"] = f"input[{i}]"
                break
        if not set_ok and loc.count():
            loc.first.set_input_files(str(THUMB_A))
            info["via"] = "input[0]"
            set_ok = True
        info["set"] = set_ok
    except Exception as e:
        info["set"] = False
        info["err"] = f"{type(e).__name__}: {e}"
    page.wait_for_timeout(2500)
    # Save if needed
    try:
        save = page.get_by_role("button", name=re.compile(r"^Save$", re.I))
        if save.count() and save.first.is_enabled():
            save.first.click(timeout=4000)
            info["saved"] = True
            page.wait_for_timeout(2500)
    except Exception:
        info["saved"] = False
    dismiss(page)
    shot(page, "301_edit_after_thumb_a.png")
    return info


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
    shot(page, "310_edit.png")

    hit = click_exact_ab_testing(page)
    info["open"] = hit
    page.wait_for_timeout(2500)
    shot(page, "311_ab_dialog.png")
    body = snip(page, 6000)
    info["ui_snip"] = body[:2000]

    # Detect dialog presence
    dialog_open = bool(
        re.search(
            r"Title and thumbnail|What do you want to test|Test type|Choose what to test|Start test",
            body,
            re.I,
        )
    )
    info["dialog_open"] = dialog_open

    offers = []
    for label in [
        "Title and thumbnail",
        "Titles and thumbnails",
        "Thumbnail",
        "Title",
        "Thumbnail only",
        "Title only",
    ]:
        # Only count if in dialog-like context — check after open
        if dialog_open and re.search(re.escape(label), body, re.I):
            offers.append(label)
        elif not dialog_open:
            # Still record page-level labels but mark
            if re.search(rf"\b{re.escape(label)}\b", body):
                offers.append(f"page:{label}")
    info["offers"] = offers

    chosen = None
    for label in [
        "Title and thumbnail",
        "Titles and thumbnails",
        "Thumbnail",
        "Title",
    ]:
        if click_in_dialog(page, rf"^{re.escape(label)}$"):
            chosen = label
            break
    info["chosen"] = chosen
    page.wait_for_timeout(2000)
    shot(page, "312_ab_type.png")
    body2 = snip(page, 5000)
    info["after_type"] = body2[:1500]

    if not chosen:
        info["ok"] = False
        info["reason"] = "no_test_type_selected_dialog_may_not_have_opened"
        info["note"] = (
            "Could not open or select a Test & Compare type. "
            f"Raw offers seen: {offers}. Report to Ben — do not guess."
        )
        try:
            page.keyboard.press("Escape")
        except Exception:
            pass
        return info

    # Configure variants based on type
    thumb_uploads = []
    if re.search(r"thumbnail", chosen, re.I):
        # Upload A, C, B into successive image file inputs inside dialog
        thumbs = [THUMB_A, THUMB_C, THUMB_B]
        try:
            loc = page.locator('input[type="file"]')
            idxs = []
            for i in range(loc.count()):
                acc = (loc.nth(i).get_attribute("accept") or "").lower()
                if "image" in acc or "jpeg" in acc or "jpg" in acc or not acc:
                    idxs.append(i)
            info["file_input_idxs"] = idxs
            for j, thumb in enumerate(thumbs):
                if j >= len(idxs):
                    break
                try:
                    loc.nth(idxs[j]).set_input_files(str(thumb))
                    thumb_uploads.append({"i": idxs[j], "file": thumb.name})
                    page.wait_for_timeout(1500)
                except Exception as e:
                    thumb_uploads.append(
                        {"i": idxs[j], "file": thumb.name, "err": type(e).__name__}
                    )
        except Exception as e:
            thumb_uploads.append({"err": type(e).__name__})
        info["thumb_uploads"] = thumb_uploads

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
                page.wait_for_timeout(400)
            except Exception as e:
                titles_filled.append({"title": title, "err": type(e).__name__})
        info["titles_filled"] = titles_filled

    shot(page, "313_ab_filled.png")

    start = None
    for pat in [r"^Start$", r"^Start test$", r"^Create test$", r"^Save$", r"^Done$", r"^Next$"]:
        start = click_in_dialog(page, pat)
        if start:
            break
    info["start"] = start
    page.wait_for_timeout(3500)
    shot(page, "314_ab_after_start.png")
    after = snip(page, 2000)
    info["after"] = after[:1200]
    info["running"] = bool(re.search(r"A/B test running|test running", after, re.I))
    info["ok"] = True
    info["note"] = (
        f"Studio dialog offered {offers}; selected {chosen}. "
        "Combined Title+thumbnail only if listed; otherwise set what UI allows."
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

    # Open via left Editor or End screen link
    opened = False
    try:
        page.get_by_role("link", name=re.compile(r"^Editor$", re.I)).first.click(timeout=4000)
        page.wait_for_timeout(2000)
        opened = True
    except Exception:
        pass
    hit = click_in_dialog(page, r"^End screen$") or None
    if not hit:
        try:
            page.get_by_text(re.compile(r"^End screen$", re.I)).first.click(timeout=4000)
            hit = "End screen"
        except Exception:
            pass
    if not hit:
        page.goto(
            f"https://studio.youtube.com/video/{VIDEO_ID}/editor",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(3000)
        try:
            page.get_by_text(re.compile(r"End screen", re.I)).first.click(timeout=5000)
            hit = "End screen"
        except Exception:
            pass
    info["open"] = hit
    info["editor_nav"] = opened
    page.wait_for_timeout(2500)
    shot(page, "320_endscreen_open.png")
    body = snip(page, 3500)
    info["open_snip"] = body[:900]

    # If empty, apply 1 video 1 subscribe template
    if not re.search(r"Subscribe:|Most recent|Video:", body, re.I):
        click_in_dialog(page, r"1 video,? 1 subscribe")
        page.wait_for_timeout(1500)
        shot(page, "321_template.png")

    # Click Most recent upload / Video element to change
    for pat in [r"Most recent upload", r"Video: Most recent", r"^Video$"]:
        if click_in_dialog(page, pat):
            page.wait_for_timeout(1200)
            info["clicked_video_el"] = pat
            break

    # Specific video mode
    for pat in [
        r"Specific video",
        r"Choose a specific video",
        r"Select a video",
        r"Video from your channel",
    ]:
        if click_in_dialog(page, pat):
            info["mode"] = pat
            page.wait_for_timeout(1000)
            break

    # Type search
    try:
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
                  if (/search|video|url|paste/.test(aria) || inp.type==='search' || inp.type==='text' || inp.type==='url') {
                    const rct = inp.getBoundingClientRect();
                    if (rct.width < 20) continue;
                    inp.focus();
                    inp.value = '';
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
            RELATED_002,  # paste id first — most reliable
        )
        info["search_id"] = bool(filled)
        if filled:
            page.keyboard.press("Enter")
            page.wait_for_timeout(2000)
        else:
            # try title
            page.evaluate(
                """(q) => {
                  const walk=(r,d=0)=>{
                    if(!r||d>45) return false;
                    for (const inp of (r.querySelectorAll?r.querySelectorAll('input,textarea'):[])) {
                      const rct=inp.getBoundingClientRect();
                      if(rct.width<40) continue;
                      inp.focus(); inp.value=q;
                      inp.dispatchEvent(new Event('input',{bubbles:true}));
                      return true;
                    }
                    for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                      if(el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
                    }
                    return false;
                  };
                  return walk(document);
                }""",
                RELATED_TITLE,
            )
            page.keyboard.press("Enter")
            page.wait_for_timeout(2000)
            info["search_title"] = True
    except Exception as e:
        info["search_err"] = type(e).__name__

    if click_in_dialog(page, r"Periodic Table|AL_-qlWko_g|How Did We Discover"):
        info["picked_002"] = True
        page.wait_for_timeout(1200)
    else:
        info["picked_002"] = False

    shot(page, "322_endscreen_picked.png")

    # Ensure subscribe
    body3 = snip(page, 3000)
    if not re.search(r"Subscribe", body3, re.I):
        click_in_dialog(page, r"^\+?\s*Element$|Add element")
        page.wait_for_timeout(600)
        click_in_dialog(page, r"^Subscribe$")
        page.wait_for_timeout(800)

    shot(page, "323_endscreen_before_save.png")
    save = click_in_dialog(page, r"^Save$")
    if not save:
        try:
            page.get_by_role("button", name=re.compile(r"^Save$", re.I)).first.click(timeout=4000)
            save = "Save"
        except Exception:
            pass
    info["save"] = save
    page.wait_for_timeout(2500)
    click_in_dialog(page, r"^Save$|^Confirm$|^OK$")
    page.wait_for_timeout(1500)
    shot(page, "324_endscreen_saved.png")
    after = snip(page, 3000)
    info["after_snip"] = after[:1000]
    info["has_002"] = bool(
        re.search(r"AL_-qlWko_g|Periodic Table|How Did We Discover the Periodic", after, re.I)
    )
    info["has_subscribe"] = bool(re.search(r"Subscribe", after, re.I))
    info["still_most_recent"] = bool(re.search(r"Most recent upload", after, re.I))
    info["ok"] = bool(info.get("save") and info["has_subscribe"] and (info["has_002"] or info.get("picked_002")))
    if info["still_most_recent"] and not info["has_002"]:
        info["ok"] = False
        info["note"] = "Still Most recent upload after save — bind AL_-qlWko_g manually."
    return info


def try_pin(page) -> dict:
    info: dict = {"text": PIN[:140]}
    page.goto(
        f"https://www.youtube.com/watch?v={VIDEO_ID}",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3000)
    shot(page, "330_watch.png")
    body = snip(page, 2000)
    if re.search(r"private|unavailable|scheduled", body, re.I):
        info["ok"] = False
        info["reason"] = "watch_page_not_commentable_while_scheduled_or_private"
        info["note"] = "Pin on launch day 15 Oct 2026 — Studio blocks comments while private/scheduled."
        return info
    info["ok"] = False
    info["note"] = "Pin deferred to launch day."
    return info


def verify_schedule(page) -> dict:
    page.goto(
        f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3500)
    dismiss(page)
    shot(page, "340_content.png")
    body = snip(page, 4000)
    tip = ""
    try:
        # Hover the Scheduled chip on the atom row
        page.locator("text=Scheduled").first.hover(timeout=5000)
        page.wait_for_timeout(1000)
        tip = snip(page, 4000)
        shot(page, "341_schedule_tooltip.png")
    except Exception as e:
        tip = f"<hover err {type(e).__name__}>"
    text = body + "\n" + tip
    return {
        "has15": bool(re.search(r"15\s*(Oct|October)\s*2026", text, re.I)),
        "has1800": bool(re.search(r"18:00", text)),
        "scheduled": bool(re.search(r"Scheduled", body, re.I)),
        "tooltip_public": bool(
            re.search(r"scheduled to become public on 15 October 2026 at 18:00", tip, re.I)
        ),
        "premiere_flag_on_004": bool(
            re.search(r"Premiere", tip)
            and re.search(r"atom|GHZDsiH7L7A", tip, re.I)
        ),
        "body_snip": body[:700],
        "tip_snip": tip[:700],
    }


def main() -> int:
    EV.mkdir(parents=True, exist_ok=True)
    (EV / "finish3.log").write_text("")
    ensure_chrome()
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

        def _on_dialog(d):
            try:
                log(f"dialog: {d.type} {d.message[:120]}")
                d.accept()
            except Exception as e:
                log(f"dialog handle err: {e}")

        page.on("dialog", _on_dialog)
        try:
            hos = ensure_hos(page)
            result["channelCheck"] = hos
            shot(page, "305_channel.png")
            if not hos.get("ok"):
                dump("FINISH3_RESULT.json", result)
                return 2

            result["thumbA"] = restore_thumb_a(page)
            log(f"thumbA={result['thumbA']}")

            result["abTest"] = do_ab_test(page)
            log(
                f"abTest dialog={result['abTest'].get('dialog_open')} "
                f"chosen={result['abTest'].get('chosen')} offers={result['abTest'].get('offers')}"
            )

            result["endScreen"] = do_end_screen(page)
            log(
                f"endScreen ok={result['endScreen'].get('ok')} "
                f"002={result['endScreen'].get('has_002')} "
                f"sub={result['endScreen'].get('has_subscribe')} "
                f"mru={result['endScreen'].get('still_most_recent')}"
            )

            result["pin"] = try_pin(page)
            result["scheduleFinal"] = verify_schedule(page)
            shot(page, "350_final.png")

            result["ok"] = bool(
                result["channelCheck"].get("ok")
                and result["scheduleFinal"].get("has15")
                and result["scheduleFinal"].get("scheduled")
            )
            dump("FINISH3_RESULT.json", result)
            log(f"DONE ok={result['ok']}")
            return 0 if result["ok"] else 1
        except Exception as e:
            result["error"] = f"{type(e).__name__}: {e}"
            dump("FINISH3_RESULT.json", result)
            log(f"ERROR {result['error']}")
            try:
                shot(page, "399_error.png")
            except Exception:
                pass
            return 3


if __name__ == "__main__":
    raise SystemExit(main())
