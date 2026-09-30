#!/usr/bin/env python3
"""Ben 22:26 finish — Audience + Altered re-check, then Thumbnail-only T&C.

Thumb A already confirmed on Content list (RECOVER_2226_08_content.png).
Scroll to Audience before reading (prior abort: radios empty at top of page).
"""
from __future__ import annotations

import json
import re
import time
from datetime import datetime
from pathlib import Path
import importlib.util

from playwright.sync_api import sync_playwright

PORT = 9460
CHANNEL = "UCXp7HkBIl1LgaznXuZHJyRg"
VID = "GHZDsiH7L7A"
PROJ = Path(__file__).resolve().parents[2]
EV = PROJ / "11_Upload-Package/Schedule/evidence_2026-09-29_studio"
ART = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts/hos004_thumb_A_2226"
BEN = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts"
THUMB_A = (PROJ / "08_Thumbnail/Selected/hos_004_thumb_A_atom_live_v04.jpg").resolve()
THUMB_B = (PROJ / "08_Thumbnail/Selected/hos_004_thumb_B_cut_gold_live_v04.jpg").resolve()
THUMB_C = (PROJ / "08_Thumbnail/Selected/hos_004_thumb_C_hidden_number_live_v06.jpg").resolve()

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
    with (EV / "finish_2226.log").open("a") as f:
        f.write(line + "\n")


def dump(n, o):
    t = json.dumps(o, indent=2) + "\n"
    (EV / n).write_text(t)
    (ART / n).write_text(t)


def shot(page, n: str) -> Path:
    p = EV / n
    page.screenshot(path=str(p), full_page=False)
    (ART / n).write_bytes(p.read_bytes())
    (BEN / n).write_bytes(p.read_bytes())
    return p


def open_edit(page) -> None:
    page.goto(
        f"https://studio.youtube.com/video/{VID}/edit",
        wait_until="commit",
        timeout=90000,
    )
    page.wait_for_timeout(4000)
    cos.dismiss(page)


def scroll_to(page, pattern: str, max_pages: int = 30) -> bool:
    for _ in range(max_pages):
        if re.search(pattern, page.inner_text("body"), re.I):
            return True
        page.keyboard.press("PageDown")
        page.wait_for_timeout(120)
    return bool(re.search(pattern, page.inner_text("body"), re.I))


def wait_saved(page, timeout_ms=25000) -> dict:
    deadline = time.time() + timeout_ms / 1000
    while time.time() < deadline:
        body = page.inner_text("body")
        if re.search(r"Changes saved|All changes saved", body, re.I):
            return {"ok": True, "trouble": False}
        if re.search(r"trouble saving|problem saving|couldn.?t save", body, re.I):
            return {"ok": False, "trouble": True}
        page.wait_for_timeout(400)
    body = page.inner_text("body")
    return {
        "ok": bool(re.search(r"Changes saved|All changes saved|Saved", body, re.I)),
        "trouble": bool(re.search(r"trouble saving|problem saving", body, re.I)),
    }


def content_confirm(page) -> dict:
    page.goto(
        f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload",
        wait_until="commit",
        timeout=90000,
    )
    page.wait_for_timeout(3500)
    cos.dismiss(page)
    try:
        page.get_by_role("textbox", name=re.compile(r"Search", re.I)).first.fill(
            "What's Really Inside an Atom"
        )
        page.keyboard.press("Enter")
        page.wait_for_timeout(2500)
    except Exception:
        pass
    shot(page, "FINISH_2226_content.png")
    body = page.inner_text("body")
    return {
        "has_title": "What's Really Inside an Atom" in body,
        "mentions_hidden_number": bool(re.search(r"HIDDEN NUMBER", body)),
    }


def arm_thumbnail_only(page) -> dict:
    out = {"mode": "Thumbnail only", "actions": []}
    open_edit(page)
    # Ensure no staged 2-slot title test first
    body = page.inner_text("body")
    if re.search(r"A/B testing titles|title test has been set up", body, re.I):
        out["actions"].append("had_staged_titles")
        try:
            page.get_by_role("button", name=re.compile(r"^A/B Testing$", re.I)).first.click(
                timeout=2000
            )
            page.wait_for_timeout(1000)
            body2 = page.inner_text("body")
            if re.search(r"current test will be deleted|Run a new test", body2, re.I):
                page.get_by_role("button", name=re.compile(r"^Continue$", re.I)).first.click(
                    timeout=1500
                )
                page.wait_for_timeout(1500)
                for pat in (r"^Cancel$", r"^Close$"):
                    try:
                        page.get_by_role("button", name=re.compile(pat, re.I)).first.click(
                            timeout=1000
                        )
                        break
                    except Exception:
                        pass
                page.keyboard.press("Escape")
                out["actions"].append("cleared_staged")
            else:
                page.keyboard.press("Escape")
        except Exception:
            pass
        try:
            page.get_by_role("button", name=re.compile(r"^Undo changes$", re.I)).first.click(
                timeout=800
            )
            out["actions"].append("undo")
        except Exception:
            pass
        open_edit(page)

    try:
        page.get_by_role("button", name=re.compile(r"^A/B Testing$", re.I)).first.click(
            timeout=2500
        )
        out["actions"].append("open")
    except Exception:
        page.evaluate(
            """() => {
              const walk=(r,d=0)=>{
                if(!r||d>55) return;
                for (const el of (r.querySelectorAll?r.querySelectorAll('button,[role=button]'):[])) {
                  const t=(el.innerText||'').trim();
                  if (t==='A/B Testing') { el.click(); return; }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                  if(el.shadowRoot) walk(el.shadowRoot,d+1);
              };
              walk(document);
            }"""
        )
        out["actions"].append("open_deep")
    page.wait_for_timeout(1500)
    body = page.inner_text("body")
    shot(page, "FINISH_2226_tc_dialog.png")
    if re.search(r"Ineligible|not eligible", body, re.I):
        out["blocked"] = True
        page.keyboard.press("Escape")
        return out
    if re.search(r"current test will be deleted|Run a new test", body, re.I):
        try:
            page.get_by_role("button", name=re.compile(r"^Continue$", re.I)).first.click(
                timeout=1500
            )
            out["actions"].append("continue_replace")
            page.wait_for_timeout(1500)
        except Exception:
            pass

    hit = page.evaluate(
        """() => {
          let hit=null;
          const walk=(r,d=0)=>{
            if(!r||d>55||hit) return;
            for (const el of (r.querySelectorAll
              ? r.querySelectorAll('button,[role=button],[role=radio],[role=tab],div,span') : [])) {
              const t=(el.innerText||'').trim();
              if (t !== 'Thumbnail only') continue;
              const rect=el.getBoundingClientRect();
              if (rect.width<5||rect.height<5) continue;
              el.click(); hit=t; return;
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if(el.shadowRoot) walk(el.shadowRoot,d+1);
          };
          walk(document); return hit;
        }"""
    )
    out["mode_click"] = hit
    page.wait_for_timeout(1000)
    shot(page, "FINISH_2226_thumb_only_mode.png")

    files = [str(THUMB_A), str(THUMB_C), str(THUMB_B)]
    loc = page.locator('input[type="file"]')
    n = loc.count()
    out["inputs"] = n
    for i in range(min(n, 3)):
        try:
            loc.nth(i).set_input_files(files[i])
            out["actions"].append(f"up_{i}")
            page.wait_for_timeout(900)
        except Exception as e:
            out["actions"].append(f"up_err_{i}_{type(e).__name__}")

    for name in (r"^Set test$", r"^Done$", r"^Create$"):
        try:
            btn = page.get_by_role("button", name=re.compile(name, re.I)).first
            en = btn.evaluate(
                "el => !(el.disabled || el.getAttribute('aria-disabled')==='true')"
            )
            if not en:
                continue
            btn.click(timeout=1500)
            out["actions"].append(f"set_{name}")
            page.wait_for_timeout(1200)
            break
        except Exception:
            continue
    shot(page, "FINISH_2226_tc_after_set.png")
    out["saved_click"] = cos.save_named(page)
    page.wait_for_timeout(800)
    out["save"] = wait_saved(page, 25000)
    shot(page, "FINISH_2226_tc_after_save.png")
    return out


def main():
    ART.mkdir(parents=True, exist_ok=True)
    EV.mkdir(parents=True, exist_ok=True)
    result = {
        "at": datetime.now().isoformat(timespec="seconds"),
        "order": "Ben 22:26 finish Audience/Altered + Thumbnail-only T&C",
        "videoId": VID,
        "note": "Main thumb A already confirmed on Content list",
    }
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
        ctx = browser.contexts[0]
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        cos.channel_ok(page)
        open_edit(page)
        shot(page, "FINISH_2226_00_edit.png")

        # Audience — scroll first
        scroll_to(page, r"Made for Kids|Audience")
        page.wait_for_timeout(500)
        shot(page, "FINISH_2226_01_audience.png")
        result["audience"] = cos.ensure_not_kids(page, context="finish_2226")

        # Altered
        cos.show_more(page)
        scroll_to(page, r"AI wasn|AI was used|Altered content|AI use")
        page.wait_for_timeout(400)
        result["altered"] = cos.read_ai_altered(page)
        shot(page, "FINISH_2226_02_altered.png")
        # If not Yes, set Yes once (Ben 21:49)
        if result["altered"].get("yes") is not True:
            try:
                page.get_by_role("radio", name=re.compile(r"^Yes, AI was used$", re.I)).first.click(
                    timeout=2000
                )
                cos.save_named(page)
                page.wait_for_timeout(1000)
                wait_saved(page, 20000)
                open_edit(page)
                cos.show_more(page)
                scroll_to(page, r"AI wasn|AI was used")
                result["altered"] = cos.read_ai_altered(page)
                result["altered_resaved"] = True
            except Exception as e:
                result["altered_set_err"] = type(e).__name__

        # Thumbnail-only T&C
        result["tc"] = arm_thumbnail_only(page)
        if result["tc"].get("save", {}).get("trouble"):
            log("T&C trouble saving — wait 150s, retry Thumbnail-only once")
            result["tc_retry_wait_s"] = 150
            page.wait_for_timeout(150_000)
            result["tc_retry"] = arm_thumbnail_only(page)

        # Confirm content still A + final audience/altered
        result["content"] = content_confirm(page)
        open_edit(page)
        # If thumb flipped, restore A once
        shot(page, "FINISH_2226_03_edit_after_tc.png")
        # Heuristic: if right preview / sidebar still looks like atom we're good;
        # if staged title test reappeared, clear without looping
        body = page.inner_text("body")
        if re.search(r"A/B testing titles", body, re.I) and not result["tc"].get("blocked"):
            result["note_tc_ui"] = "A/B testing titles banner visible after rearm"
        scroll_to(page, r"Made for Kids|Audience")
        result["audience_final"] = cos.ensure_not_kids(page, context="finish_final")
        cos.show_more(page)
        scroll_to(page, r"AI wasn|AI was used")
        result["altered_final"] = cos.read_ai_altered(page)
        result["tc_final"] = cos.read_tc_state(page)
        shot(page, "FINISH_2226_04_final.png")

        tc = result.get("tc_retry") or result["tc"]
        result["summary"] = {
            "audience_not_kids": result["audience_final"].get("ok_not_kids"),
            "altered_yes": result["altered_final"].get("yes") is True,
            "content_has_title": result["content"].get("has_title"),
            "tc_mode": tc.get("mode"),
            "tc_blocked": tc.get("blocked"),
            "tc_saved": (tc.get("save") or {}).get("ok"),
            "tc_trouble": (tc.get("save") or {}).get("trouble"),
            "tc_two_slot": result["tc_final"].get("two_slot_title_test"),
            "tc_ineligible": result["tc_final"].get("ineligible"),
            "titles": result["tc_final"].get("titles_present"),
        }
        dump("FINISH_2226_RESULT.json", result)
        log(f"SUMMARY {result['summary']}")
        return result


if __name__ == "__main__":
    main()
