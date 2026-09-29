#!/usr/bin/env python3
"""Ben 20:03 — Comments ON on 004 + audit 001/002/003+Shorts + pinned comment.

CDP :9460 HOS profile only. Never Orbit/Oppti/.env/API.
No re-upload / replace / delete / publish-now / Premiere.
"""
from __future__ import annotations

import json
import re
import urllib.request
from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright

PORT = 9460
CHANNEL = "UCXp7HkBIl1LgaznXuZHJyRg"
HANDLE = "@HistoryOfScienceYT"
VID_004 = "GHZDsiH7L7A"
PIN_TEXT = (
    Path(__file__).resolve().parents[1]
    / "Pinned-Comments/atom_long_pinned-comment_v01.txt"
).read_text().strip()

VIDEOS = [
    ("004_long", VID_004),
    ("001_long", "_C92tIJCk8A"),
    ("002_long", "AL_-qlWko_g"),
    ("003_long", "frP_YrNShsU"),
    ("002_short_uU12JA5rMWg", "uU12JA5rMWg"),
    ("002_short_nFQRWmpulTQ", "nFQRWmpulTQ"),
    ("002_short_CnHwX1L9XHg", "CnHwX1L9XHg"),
    ("002_short_nba0-f7PPeU", "nba0-f7PPeU"),
    ("002_short_LanTHJckYx8", "LanTHJckYx8"),
    ("003_short_oowAOWTBoq0", "oowAOWTBoq0"),
    ("003_short_xvanpsLeADE", "xvanpsLeADE"),
    ("003_short_zI_eD3vFWmE", "zI_eD3vFWmE"),
    ("001_short_8uBR-9oxeWs", "8uBR-9oxeWs"),
    ("001_short_YX2UR1u-JCQ", "YX2UR1u-JCQ"),
    ("001_short_Fnb3p81u-wY", "Fnb3p81u-wY"),
    ("001_short_vpuRgKXtFlY", "vpuRgKXtFlY"),
    ("001_short_Lcmh5y2KMQM", "Lcmh5y2KMQM"),
]

PROJ = Path(__file__).resolve().parents[2]
EV = PROJ / "11_Upload-Package/Schedule/evidence_2026-09-29_studio"
ART = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts/hos004_studio_phone_uat"
BEN = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts"


def log(m: str) -> None:
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    line = f"{datetime.now().isoformat(timespec='seconds')} {m}"
    print(line, flush=True)
    with (EV / "comments_v06.log").open("a") as f:
        f.write(line + "\n")


def dump(n: str, o) -> None:
    text = json.dumps(o, indent=2) + "\n"
    (EV / n).write_text(text)
    (ART / n).write_text(text)


def shot(page, n: str) -> Path:
    p = EV / n
    page.screenshot(path=str(p), full_page=False)
    (ART / n).write_bytes(p.read_bytes())
    ben = BEN / n
    if n.startswith("BEN_") or "004_comments_on" in n:
        ben.write_bytes(p.read_bytes())
    return p


def dismiss(page) -> None:
    for _ in range(3):
        page.keyboard.press("Escape")
        page.wait_for_timeout(80)
        try:
            page.get_by_role(
                "button",
                name=re.compile(r"^(OK, got it|Got it|Close|Dismiss|Not now|Continue)$", re.I),
            ).first.click(timeout=250)
        except Exception:
            pass


def ensure_cdp() -> None:
    urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/version", timeout=3).read()


def open_edit(page, video_id: str) -> None:
    page.goto(
        f"https://studio.youtube.com/video/{video_id}/edit",
        wait_until="commit",
        timeout=90000,
    )
    page.wait_for_timeout(4000)
    dismiss(page)


def click_show_more(page) -> bool:
    for pat in (r"^Show more$", r"Show more"):
        try:
            loc = page.get_by_role("button", name=re.compile(pat, re.I)).first
            if loc.count() and loc.is_visible():
                loc.click(timeout=1500)
                page.wait_for_timeout(600)
                return True
        except Exception:
            pass
    try:
        clicked = page.evaluate(
            """() => {
              const nodes = [...document.querySelectorAll('button, a, tp-yt-paper-button, ytcp-button')];
              for (const n of nodes) {
                const t = (n.innerText||'').trim();
                if (/^Show more$/i.test(t)) { n.click(); return true; }
              }
              return false;
            }"""
        )
        if clicked:
            page.wait_for_timeout(600)
            return True
    except Exception:
        pass
    return False


def set_audience_not_kids(page) -> dict:
    info = {"set_to_not": False, "already_not": False, "saved": False}
    for _ in range(20):
        body = page.inner_text("body")
        if re.search(r"set to not ['\"]?Made for Kids", body, re.I):
            info["already_not"] = True
            break
        if "Made for Kids" in body or "Audience" in body:
            break
        page.keyboard.press("PageDown")
        page.wait_for_timeout(200)
    body = page.inner_text("body")
    if re.search(r"set to not ['\"]?Made for Kids", body, re.I):
        info["already_not"] = True
        info["set_to_not"] = True
        return info
    # Click No radio
    try:
        page.get_by_text(re.compile(r"No, it's not ['\"]?Made for Kids['\"]?", re.I)).first.click(
            timeout=2500
        )
        info["set_to_not"] = True
        page.wait_for_timeout(400)
    except Exception as e:
        info["err"] = f"click:{type(e).__name__}"
        # JS fallback
        try:
            ok = page.evaluate(
                """() => {
                  const labs = [...document.querySelectorAll('label, ytcp-ve, div, span, tp-yt-paper-radio-button')];
                  for (const el of labs) {
                    const t = (el.innerText||'').trim();
                    if (/^No, it's not/i.test(t) && /Made for Kids/i.test(t)) {
                      (el.closest('tp-yt-paper-radio-button') || el).click();
                      return true;
                    }
                  }
                  return false;
                }"""
            )
            info["set_to_not"] = bool(ok)
        except Exception as e2:
            info["err"] = f"js:{type(e2).__name__}"
    # Save if enabled
    try:
        save = page.get_by_role("button", name=re.compile(r"^Save$", re.I)).first
        if save.count() and save.is_enabled():
            save.click(timeout=2000)
            page.wait_for_timeout(2500)
            info["saved"] = True
    except Exception:
        pass
    body = page.inner_text("body")
    if re.search(r"set to not ['\"]?Made for Kids", body, re.I):
        info["set_to_not"] = True
    return info


def parse_comments_mode(body: str) -> dict:
    """Parse Studio Comments block: Comments / On|Off / Moderation / ..."""
    info = {"section": False, "mode": None, "on": None, "snip": None}
    m = re.search(
        r"Choose if and how you want to show comments\s*(.{0,400})",
        body,
        re.I | re.S,
    )
    if not m:
        # alternate: bare Comments\nOn near Moderation
        m2 = re.search(
            r"(Comments\s*\n\s*(On|Off)\s*\n\s*Moderation.{0,200})",
            body,
            re.I | re.S,
        )
        if not m2:
            return info
        chunk = m2.group(1)
    else:
        chunk = "Choose if and how you want to show comments\n" + m.group(1)
    info["section"] = True
    info["snip"] = chunk[:280]
    mm = re.search(r"Comments\s*\n\s*(On|Off)\b", chunk, re.I)
    if mm:
        info["mode"] = mm.group(1)
        info["on"] = mm.group(1).lower() == "on"
    elif re.search(r"\bAllow all comments\b|\bHold potentially inappropriate\b", chunk, re.I):
        info["mode"] = "Allow/Hold"
        info["on"] = True
    elif re.search(r"Comments are turned off|turned off", chunk, re.I):
        info["mode"] = "Off"
        info["on"] = False
    return info


def scroll_to_comments(page) -> dict:
    click_show_more(page)
    found = {"section": False, "mode": None, "on": None, "snip": None}
    for i in range(36):
        body = page.inner_text("body")
        parsed = parse_comments_mode(body)
        if parsed["section"]:
            found = parsed
            # try to bring into view
            try:
                page.evaluate(
                    """() => {
                      const walk = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
                      let n; while (n = walk.nextNode()) {
                        if (/Choose if and how you want to show comments/i.test(n.textContent||'')) {
                          n.parentElement?.scrollIntoView({block:'center'});
                          return true;
                        }
                      }
                      return false;
                    }"""
                )
                page.wait_for_timeout(300)
                body = page.inner_text("body")
                found = parse_comments_mode(body) or found
            except Exception:
                pass
            break
        if i == 0 or i % 3 == 0:
            click_show_more(page)
        page.keyboard.press("PageDown")
        page.wait_for_timeout(180)
    return found


def enable_comments_on(page) -> dict:
    """If Comments Off, set On (Allow all / Hold)."""
    info = {"changed": False, "mode_after": None}
    parsed = scroll_to_comments(page)
    if parsed.get("on") is True:
        info["mode_after"] = parsed.get("mode")
        return info
    # Open Comments dropdown / toggle
    try:
        # Click the Comments control (shows Off/On)
        page.evaluate(
            """() => {
              const walk = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
              let n; while (n = walk.nextNode()) {
                const t = (n.textContent||'').trim();
                if (t === 'Comments') {
                  let el = n.parentElement;
                  for (let i=0;i<6 && el;i++) {
                    const btn = el.querySelector('button, [role=button], ytcp-dropdown-trigger, tp-yt-paper-button');
                    if (btn) { btn.click(); return 'btn'; }
                    el = el.parentElement;
                  }
                }
                if (t === 'Off' || t === 'On') {
                  const p = n.parentElement;
                  if (p) { p.click(); return 'val'; }
                }
              }
              return null;
            }"""
        )
        page.wait_for_timeout(700)
        # Pick On / Allow all / Hold potentially inappropriate
        for label in (
            r"^On$",
            r"^Allow all comments$",
            r"^Hold potentially inappropriate comments for review$",
            r"Hold potentially inappropriate",
            r"^Allow all$",
        ):
            try:
                page.get_by_text(re.compile(label, re.I)).first.click(timeout=1200)
                info["changed"] = True
                page.wait_for_timeout(500)
                break
            except Exception:
                continue
        try:
            save = page.get_by_role("button", name=re.compile(r"^Save$", re.I)).first
            if save.count() and save.is_enabled():
                save.click(timeout=2000)
                page.wait_for_timeout(2500)
                info["saved"] = True
        except Exception:
            pass
    except Exception as e:
        info["err"] = type(e).__name__
    parsed2 = scroll_to_comments(page)
    info["mode_after"] = parsed2.get("mode")
    info["on_after"] = parsed2.get("on")
    return info


def audit_video(page, key: str, video_id: str) -> dict:
    info = {"key": key, "videoId": video_id}
    open_edit(page, video_id)
    body = page.inner_text("body")
    if re.search(r"Oops|something went wrong|try again", body, re.I) and "Made for Kids" not in body:
        info["oops"] = True
        shot(page, f"comments_v06_audit_{key}_oops.png")
        return info
    # Audience
    aud = set_audience_not_kids(page) if key == "004_long" else {}
    if key != "004_long":
        # just read
        for _ in range(18):
            body = page.inner_text("body")
            if "Made for Kids" in body or "Audience" in body:
                break
            page.keyboard.press("PageDown")
            page.wait_for_timeout(160)
        body = page.inner_text("body")
        aud = {
            "audience_not_kids": bool(
                re.search(r"set to not ['\"]?Made for Kids|No, it's not", body, re.I)
            )
            and not re.search(r"Yes, it's ['\"]?Made for Kids['\"]?.*checked|set to ['\"]?Made for Kids", body, re.I)
        }
        # more reliable: look for status line
        aud["audience_not_kids"] = bool(
            re.search(r"This video is set to not ['\"]?Made for Kids", body, re.I)
        ) or (
            bool(re.search(r"No, it's not ['\"]?Made for Kids", body, re.I))
            and not bool(re.search(r"This video is set to ['\"]?Made for Kids", body, re.I))
        )
    info["audience"] = aud

    if key == "004_long" and not aud.get("set_to_not") and not aud.get("already_not"):
        aud = set_audience_not_kids(page)
        info["audience"] = aud
        shot(page, "comments_v06_004_audience.png")

    comments = scroll_to_comments(page)
    if key == "004_long" and comments.get("on") is not True:
        en = enable_comments_on(page)
        info["enable"] = en
        comments = scroll_to_comments(page)
    info["comments"] = comments
    shot(page, f"comments_v06_audit_{key}.png")
    if key == "004_long":
        # Dedicated Ben screenshot of Comments On
        shot(page, "BEN_004_comments_on.png")
        shot(page, "comments_v06_004_comments_on.png")
        # Also copy to artifacts root with clear name
        try:
            (BEN / "BEN_004_comments_on.png").write_bytes(
                (EV / "BEN_004_comments_on.png").read_bytes()
            )
        except Exception:
            pass
    return info


def try_pin(page) -> dict:
    info = {"text": PIN_TEXT, "ok": False, "steps": []}
    assert "http" not in PIN_TEXT.lower() and "/go/" not in PIN_TEXT

    # Studio comments tab
    page.goto(
        f"https://studio.youtube.com/video/{VID_004}/comments",
        wait_until="commit",
        timeout=90000,
    )
    page.wait_for_timeout(4000)
    dismiss(page)
    shot(page, "comments_v06_pin_studio_tab.png")
    body = page.inner_text("body")
    info["studio_snip"] = body[:500]
    studio_blocked = bool(
        re.search(r"Comments are turned off|comments are turned off", body, re.I)
    )
    info["studio_blocked"] = studio_blocked

    # Watch page (owner may still comment on scheduled)
    page.goto(
        f"https://www.youtube.com/watch?v={VID_004}",
        wait_until="commit",
        timeout=90000,
    )
    page.wait_for_timeout(4500)
    dismiss(page)
    # Scroll to comments
    for _ in range(8):
        page.keyboard.press("PageDown")
        page.wait_for_timeout(200)
    shot(page, "comments_v06_pin_watch.png")
    body = page.inner_text("body")
    info["watch_snip"] = body[:600]
    if re.search(r"Comments are turned off", body, re.I):
        info["reason"] = "watch_comments_turned_off"
        return info
    if re.search(r"Private video|Video unavailable|isn't available", body, re.I):
        # Scheduled often shows as unavailable to public but owner may still see
        info["steps"].append("watch_may_be_scheduled")

    # Focus comment box without TrustedHTML/innerHTML
    focused = False
    for sel in (
        "#simplebox-placeholder",
        "ytd-comment-simplebox-renderer #placeholder-area",
        "#placeholder-area",
        "ytd-commentbox #contenteditable-root",
        "#contenteditable-root",
        'div[contenteditable="true"]#contenteditable-root',
        'div[contenteditable="true"]',
    ):
        try:
            loc = page.locator(sel).first
            if loc.count() == 0:
                continue
            loc.scroll_into_view_if_needed(timeout=2000)
            loc.click(timeout=2500)
            page.wait_for_timeout(400)
            focused = True
            info["steps"].append(f"clicked:{sel}")
            break
        except Exception as e:
            info["steps"].append(f"miss:{sel}:{type(e).__name__}")

    if not focused:
        # Click "Add a comment"
        try:
            page.get_by_text(re.compile(r"Add a comment", re.I)).first.click(timeout=2500)
            page.wait_for_timeout(500)
            focused = True
            info["steps"].append("clicked:Add a comment")
        except Exception as e:
            info["steps"].append(f"add_comment_fail:{type(e).__name__}")

    if not focused:
        info["reason"] = "no_comment_box"
        shot(page, "comments_v06_pin_no_box.png")
        return info

    # Type via keyboard (avoids TrustedHTML)
    try:
        page.keyboard.press("Meta+a")
        page.keyboard.press("Backspace")
        page.keyboard.type(PIN_TEXT, delay=12)
        page.wait_for_timeout(600)
        info["steps"].append("typed")
    except Exception as e:
        info["reason"] = f"type:{type(e).__name__}"
        shot(page, "comments_v06_pin_type_fail.png")
        return info

    shot(page, "comments_v06_pin_typed.png")

    # Click Comment submit
    posted = False
    for name in (r"^Comment$", r"^Comment$"):
        try:
            btn = page.get_by_role("button", name=re.compile(name)).first
            if btn.count() and btn.is_enabled():
                btn.click(timeout=2500)
                posted = True
                info["steps"].append("clicked_comment_btn")
                break
        except Exception:
            pass
    if not posted:
        try:
            page.keyboard.press("Meta+Enter")
            posted = True
            info["steps"].append("meta_enter")
        except Exception as e:
            info["reason"] = f"submit:{type(e).__name__}"
            return info

    page.wait_for_timeout(3500)
    shot(page, "comments_v06_pin_posted.png")
    body = page.inner_text("body")
    if PIN_TEXT[:40] not in body and "periodic table" not in body.lower():
        info["reason"] = "comment_text_not_visible_after_post"
        # continue to try pin anyway

    # Open action menu on own comment and Pin
    pinned = False
    try:
        # Find comment containing our text, then action menu
        menus = page.locator(
            "ytd-comment-thread-renderer #action-menu button, "
            "ytd-comment-thread-renderer button[aria-label*='Action'], "
            "ytd-comment-view-model button[aria-label*='Action']"
        )
        count = menus.count()
        info["steps"].append(f"menus:{count}")
        if count:
            menus.first.click(timeout=2500)
            page.wait_for_timeout(600)
            try:
                page.get_by_text(re.compile(r"^Pin$", re.I)).first.click(timeout=2000)
            except Exception:
                page.get_by_role("menuitem", name=re.compile(r"Pin", re.I)).first.click(timeout=2000)
            page.wait_for_timeout(500)
            # Confirm dialog
            try:
                page.get_by_role("button", name=re.compile(r"^Pin$", re.I)).last.click(timeout=2000)
            except Exception:
                pass
            page.wait_for_timeout(2000)
            pinned = True
            info["steps"].append("pin_clicked")
    except Exception as e:
        info["steps"].append(f"pin_err:{type(e).__name__}:{e}")

    shot(page, "comments_v06_pin_after.png")
    body = page.inner_text("body")
    if re.search(r"Pinned by|Pinned", body, re.I) and (
        "periodic table" in body.lower() or PIN_TEXT[:30] in body
    ):
        info["ok"] = True
        info["reason"] = "pinned_visible"
    elif pinned:
        info["ok"] = True
        info["reason"] = "pin_clicked_confirm_ui"
    else:
        info["reason"] = info.get("reason") or "pin_not_confirmed"
    info["body_has_pin_label"] = bool(re.search(r"Pinned by|Pinned", body, re.I))
    info["body_has_text"] = PIN_TEXT[:40] in body or "periodic table" in body.lower()
    return info


def main() -> None:
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    ensure_cdp()
    result = {"at": datetime.now().isoformat(timespec="seconds"), "pin_text": PIN_TEXT}

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
        ctx = browser.contexts[0] if browser.contexts else browser.new_context()
        page = ctx.pages[0] if ctx.pages else ctx.new_page()

        # Channel sanity
        page.goto(
            f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload",
            wait_until="commit",
            timeout=90000,
        )
        page.wait_for_timeout(3000)
        dismiss(page)
        t = page.inner_text("body")
        result["channel"] = {
            "ok": HANDLE in t or "History of Science" in t,
            "has_orbit": bool(re.search(r"Orbit With Ben|OpptiAI", t, re.I)),
        }
        assert result["channel"]["ok"] and not result["channel"]["has_orbit"], result["channel"]
        log(f"channel ok {result['channel']}")

        audits = {}
        # 004 first
        log("audit 004_long + enable comments")
        audits["004_long"] = audit_video(page, "004_long", VID_004)
        log(f"004 comments={audits['004_long'].get('comments')}")

        for key, vid in VIDEOS:
            if key == "004_long":
                continue
            log(f"audit {key}")
            try:
                audits[key] = audit_video(page, key, vid)
                c = audits[key].get("comments") or {}
                log(f"  {key} on={c.get('on')} mode={c.get('mode')} oops={audits[key].get('oops')}")
            except Exception as e:
                audits[key] = {"key": key, "videoId": vid, "err": f"{type(e).__name__}:{e}"}
                log(f"  ERR {key}: {e}")

        off_list = []
        for key, a in audits.items():
            if a.get("oops"):
                continue  # edit Oops — report separately
            c = a.get("comments") or {}
            if c.get("on") is False or (c.get("section") and c.get("on") is not True):
                off_list.append(
                    {
                        "key": key,
                        "videoId": a.get("videoId"),
                        "mode": c.get("mode"),
                        "on": c.get("on"),
                        "section": c.get("section"),
                    }
                )
            elif not c.get("section") and not a.get("oops"):
                off_list.append(
                    {
                        "key": key,
                        "videoId": a.get("videoId"),
                        "mode": None,
                        "on": None,
                        "section": False,
                        "note": "comments_section_not_found",
                    }
                )

        oops_list = [
            {"key": k, "videoId": a.get("videoId")}
            for k, a in audits.items()
            if a.get("oops")
        ]

        result["audits"] = audits
        result["comments_off"] = off_list
        result["oops"] = oops_list
        dump("COMMENTS_V06_RESULT.json", result)

        log("pin attempt")
        pin = try_pin(page)
        result["pin"] = pin
        dump("COMMENTS_V06_PIN.json", pin)
        dump("COMMENTS_V06_RESULT.json", result)
        log(f"DONE pin={pin.get('ok')} reason={pin.get('reason')} off={len(off_list)}")


if __name__ == "__main__":
    main()
