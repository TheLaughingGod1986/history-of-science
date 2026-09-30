#!/usr/bin/env python3
"""Ben 21:49 CHANGE OF ORDER — Altered/synthetic content = YES on all HOS videos.

Overrides Ben 20:03 'No' and CoS 21:02 'set to No'.
Reason: AI-generated visuals + AI clone of Ben's voice.

Rules:
- Target AI/Altered YES by aria-label or own text ONLY (never Made-for-Kids Yes).
- One setting per save.
- Re-check Audience = not Made for Kids after EVERY save.
- CDP :9460 · @HistoryOfScienceYT only.
"""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
import importlib.util

from playwright.sync_api import sync_playwright

PORT = 9460
CHANNEL = "UCXp7HkBIl1LgaznXuZHJyRg"
PROJ = Path(__file__).resolve().parents[2]
EV = PROJ / "11_Upload-Package/Schedule/evidence_2026-09-29_studio"
ART = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts/hos004_altered_yes_2149"
BEN = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts"

VIDS = [
    ("004_long", "GHZDsiH7L7A"),
    ("001_long", "_C92tIJCk8A"),
    ("002_long", "AL_-qlWko_g"),
    ("003_long", "frP_YrNShsU"),
    ("001_short_8uBR", "8uBR-9oxeWs"),
    ("001_short_YX2U", "YX2UR1u-JCQ"),
    ("001_short_Fnb3", "Fnb3p81u-wY"),
    ("001_short_vpuR", "vpuRgKXtFlY"),
    ("001_short_Lcmh", "Lcmh5y2KMQM"),
    ("002_short_uU12", "uU12JA5rMWg"),
    ("002_short_nFQR", "nFQRWmpulTQ"),
    ("002_short_CnHw", "CnHwX1L9XHg"),
    ("002_short_nba0", "nba0-f7PPeU"),
    ("002_short_LanT", "LanTHJckYx8"),
    ("003_short_oowA", "oowAOWTBoq0"),
    ("003_short_xvan", "xvanpsLeADE"),
    ("003_short_zI_e", "zI_eD3vFWmE"),
]

_SPEC = importlib.util.spec_from_file_location(
    "cos2102", Path(__file__).resolve().parent / "_cos_checkin_2102_growth_fix_v01.py"
)
cos = importlib.util.module_from_spec(_SPEC)
assert _SPEC.loader
_SPEC.loader.exec_module(cos)


def log(m: str) -> None:
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    line = f"{datetime.now().isoformat(timespec='seconds')} {m}"
    print(line, flush=True)
    with (EV / "altered_yes_2149.log").open("a") as f:
        f.write(line + "\n")


def shot(page, n: str) -> Path:
    p = EV / n
    page.screenshot(path=str(p), full_page=False)
    (ART / n).write_bytes(p.read_bytes())
    (BEN / n).write_bytes(p.read_bytes())
    return p


def open_vid(page, vid: str) -> bool:
    page.goto(
        f"https://studio.youtube.com/video/{vid}/edit",
        wait_until="commit",
        timeout=90000,
    )
    page.wait_for_timeout(3500)
    cos.dismiss(page)
    body = page.inner_text("body")
    if re.search(r"Oops, something went wrong", body, re.I):
        return False
    return True


def show_more(page) -> None:
    cos.show_more(page)
    for _ in range(30):
        body = page.inner_text("body")
        if re.search(
            r"Altered content|AI wasn.?t used|AI was used|altered or synthetic|AI use",
            body,
            re.I,
        ):
            break
        page.keyboard.press("PageDown")
        page.wait_for_timeout(100)


def read_ai(page) -> dict:
    return cos.read_ai_altered(page)


def click_ai_yes(page) -> dict | None:
    """Click ONLY 'Yes, AI was used' / altered-synthetic Yes — never kids or paid promo."""
    return page.evaluate(
        """() => {
          let hit=null;
          const walk=(r,d=0)=>{
            if(!r||d>60||hit) return;
            for (const el of (r.querySelectorAll
              ? r.querySelectorAll('[role=radio],input[type=radio],tp-yt-paper-radio-button')
              : [])) {
              const al=(el.getAttribute('aria-label')||'').trim();
              let own=(el.innerText||'').trim().replace(/\\s+/g,' ');
              if (!own) {
                const fs=el.querySelector && el.querySelector('yt-formatted-string, .label, span');
                if (fs) own=(fs.innerText||'').trim().replace(/\\s+/g,' ');
              }
              const label = (al || own).slice(0,160);
              if (!label) continue;
              // HARD REJECT: kids, paid promotion, anything else
              if (/Made for Kids|paid promotion|includes paid/i.test(label)) continue;
              // STRICT ACCEPT only AI-use / altered-synthetic Yes lines
              const isAiYes = /^Yes,?\\s*AI was used\\b/i.test(label)
                || /^Yes,?\\s*it (has|does have) altered or synthetic content\\b/i.test(label)
                || /^Yes,?\\s*this video has altered or synthetic content\\b/i.test(label);
              if (!isAiYes) continue;
              el.scrollIntoView({block:'center'});
              el.click();
              hit={label: label, via: al ? 'aria' : 'own'};
              return;
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if(el.shadowRoot) walk(el.shadowRoot,d+1);
          };
          walk(document);
          return hit;
        }"""
    )


def open_altered_dropdown_if_needed(page) -> str | None:
    """Some Studio builds use a dropdown for Altered content instead of radios."""
    return page.evaluate(
        """() => {
          let ay=null;
          const walk=(r,d=0)=>{
            if(!r||d>55) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim();
              if (t==='Altered content' || t==='AI use'
                  || (/^Altered/i.test(t) && t.length<40)) {
                const rect=el.getBoundingClientRect();
                if (rect.y>100) ay=rect.y;
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if(el.shadowRoot) walk(el.shadowRoot,d+1);
          };
          walk(document);
          if (ay==null) return null;
          let opened=null;
          const walk2=(r,d=0)=>{
            if(!r||d>55||opened) return;
            for (const el of (r.querySelectorAll
              ? r.querySelectorAll('button,[role=button],[role=combobox],ytcp-dropdown-trigger')
              : [])) {
              const t=(el.innerText||el.getAttribute('aria-label')||'').trim();
              const rect=el.getBoundingClientRect();
              if (rect.y<ay||rect.y>ay+300) continue;
              if (/Yes|No|Select|altered|synthetic|AI/i.test(t) && t.length<80) {
                el.click(); opened=t.slice(0,60); return;
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if(el.shadowRoot) walk2(el.shadowRoot,d+1);
          };
          walk2(document);
          return opened;
        }"""
    )


def click_ai_yes_option(page) -> str | None:
    """Pick Yes option from open dropdown — AI/altered wording only."""
    return page.evaluate(
        """() => {
          let hit=null;
          const walk=(r,d=0)=>{
            if(!r||d>60||hit) return;
            for (const el of (r.querySelectorAll
              ? r.querySelectorAll('[role=option],tp-yt-paper-item,yt-formatted-string,div,span,button')
              : [])) {
              const t=(el.innerText||'').trim().replace(/\\s+/g,' ');
              if (!t || t.length>120) continue;
              if (/Made for Kids|paid promotion|includes paid/i.test(t)) continue;
              if (/^Yes,?\\s*AI was used\\b/i.test(t)
                  || /has altered or synthetic content/i.test(t)) {
                el.click(); hit=t.slice(0,140); return;
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if(el.shadowRoot) walk(el.shadowRoot,d+1);
          };
          walk(document); return hit;
        }"""
    )


def set_altered_yes(page, key: str, vid: str) -> dict:
    row = {"key": key, "videoId": vid, "ok": False}
    if not open_vid(page, vid):
        row["oops"] = True
        row["note"] = "Studio Oops on edit page"
        shot(page, f"ALTERED_YES_{key}_oops.png")
        log(f"{key} OOPS")
        return row

    # Baseline audience — must already be not kids; do not change kids here
    aud0 = cos.read_audience(page)
    row["audience_before"] = aud0
    if aud0.get("fail_kids"):
        # Fix kids first alone (Ben policy), then AI
        cos.ensure_not_kids(page, context=f"{key}_pre_ai")
        open_vid(page, vid)
        aud0 = cos.read_audience(page)
        row["audience_before"] = aud0

    show_more(page)
    before = read_ai(page)
    row["ai_before"] = before
    shot(page, f"ALTERED_YES_{key}_BEFORE.png")

    if before.get("yes") is True and before.get("no") is not True:
        row["already_yes"] = True
        row["ok"] = True
        row["clicked"] = None
        row["saved"] = False
        # Still re-check audience
        aud1 = cos.read_audience(page)
        row["audience_after"] = aud1
        row["ok"] = bool(aud1.get("ok_not_kids")) and not aud1.get("fail_kids")
        shot(page, f"ALTERED_YES_{key}_AFTER.png")
        log(f"{key} already YES audience_ok={row['ok']}")
        return row

    # Prefer Playwright get_by_role with exact AI Yes name (safest)
    clicked = None
    for name in (
        r"^Yes, AI was used$",
        r"^Yes, AI was used",
        r"Yes, it has altered or synthetic content",
        r"Yes, this video has altered or synthetic content",
    ):
        try:
            loc = page.get_by_role("radio", name=re.compile(name, re.I))
            if loc.count():
                loc.first.scroll_into_view_if_needed(timeout=2000)
                loc.first.click(timeout=2500)
                clicked = {"label": name, "via": "playwright_role"}
                break
        except Exception:
            continue
    if not clicked:
        clicked = click_ai_yes(page)
    row["clicked"] = clicked
    if not clicked:
        opened = open_altered_dropdown_if_needed(page)
        row["dropdown_opened"] = opened
        page.wait_for_timeout(600)
        shot(page, f"ALTERED_YES_{key}_menu.png")
        opt = click_ai_yes_option(page)
        row["clicked"] = {"label": opt, "via": "menu"} if opt else None
        clicked = row["clicked"]

    if not clicked:
        row["error"] = "could_not_find_AI_Yes_control"
        shot(page, f"ALTERED_YES_{key}_FAIL.png")
        log(f"{key} FAIL no AI Yes control")
        return row

    # Reject accidental paid-promo click
    lab = str((clicked or {}).get("label") or "")
    if re.search(r"paid promotion|includes paid|Made for Kids", lab, re.I):
        row["error"] = f"refused_wrong_yes:{lab[:80]}"
        log(f"{key} REFUSED wrong Yes: {lab[:80]}")
        return row

    page.wait_for_timeout(500)
    shot(page, f"ALTERED_YES_{key}_CLICKED.png")
    mid = read_ai(page)
    row["ai_mid_before_save"] = mid
    if mid.get("yes") is not True:
        # try once more with deep click
        clicked2 = click_ai_yes(page)
        row["clicked_retry"] = clicked2
        page.wait_for_timeout(400)
        mid = read_ai(page)
        row["ai_mid_before_save"] = mid
    if mid.get("yes") is not True:
        row["error"] = "AI_Yes_not_checked_before_save"
        shot(page, f"ALTERED_YES_{key}_FAIL.png")
        log(f"{key} FAIL AI Yes not checked before save mid={mid}")
        return row

    # ONE control → one save
    row["saved"] = cos.save_named(page)
    page.wait_for_timeout(2000)

    # Re-open and re-check Audience + AI
    open_vid(page, vid)
    aud1 = cos.read_audience(page)
    row["audience_after"] = aud1
    if aud1.get("fail_kids") or not aud1.get("ok_not_kids"):
        # CRITICAL: AI Yes click must never have flipped kids — fix kids alone
        log(f"{key} WARN audience not ok after AI save — fixing kids only")
        cos.ensure_not_kids(page, context=f"{key}_after_ai")
        open_vid(page, vid)
        aud1 = cos.read_audience(page)
        row["audience_after_fix"] = aud1

    show_more(page)
    after = read_ai(page)
    row["ai_after"] = after
    shot(page, f"ALTERED_YES_{key}_AFTER.png")
    row["ok"] = (
        after.get("yes") is True
        and after.get("no") is not True
        and aud1.get("ok_not_kids")
        and not aud1.get("fail_kids")
    )
    log(f"{key} ok={row['ok']} ai_yes={after.get('yes')} aud={aud1.get('ok_not_kids')} saved={row['saved']}")
    return row


def main() -> dict:
    ART.mkdir(parents=True, exist_ok=True)
    EV.mkdir(parents=True, exist_ok=True)
    result = {
        "at": datetime.now().isoformat(timespec="seconds"),
        "order": "Ben 21:49 CHANGE — Altered/synthetic = YES (overrides 20:03 No)",
        "reason": "AI-generated visuals and an AI clone of Ben's voice",
        "channel": "@HistoryOfScienceYT",
        "policy_from_now": "every upload: Altered/synthetic YES; Audience not Made for Kids after every save",
        "videos": [],
    }
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
        ctx = browser.contexts[0] if browser.contexts else browser.new_context()
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        cos.channel_ok(page)

        # 004 first (explicit in order)
        for key, vid in VIDS:
            try:
                row = set_altered_yes(page, key, vid)
            except Exception as e:
                row = {"key": key, "videoId": vid, "ok": False, "error": type(e).__name__, "msg": str(e)[:200]}
                log(f"{key} EXCEPTION {row['error']}: {row['msg']}")
            result["videos"].append(row)

    ok = [v for v in result["videos"] if v.get("ok")]
    oops = [v for v in result["videos"] if v.get("oops")]
    fail = [v for v in result["videos"] if not v.get("ok") and not v.get("oops")]
    result["summary"] = {
        "total": len(result["videos"]),
        "ok": len(ok),
        "oops": [v["key"] for v in oops],
        "fail": [{"key": v["key"], "error": v.get("error")} for v in fail],
        "ok_keys": [v["key"] for v in ok],
    }
    t = json.dumps(result, indent=2) + "\n"
    (EV / "ALTERED_YES_2149_RESULT.json").write_text(t)
    (ART / "ALTERED_YES_2149_RESULT.json").write_text(t)
    log(f"SUMMARY {result['summary']}")
    return result


if __name__ == "__main__":
    main()
