#!/usr/bin/env python3
"""Ben 22:26 follow-up — re-arm T&C after thumb A, with explicit Save.

Prior rearm opened Title-only by default and never Saved (discarded on reload).
This pass: open A/B Testing → force Title and thumbnail (else Thumbnail only) →
fill 3 pairs → Set test → Save details → confirm Content list still shows A.
If Title+thumb leaves a 2-slot scramble, cancel and fall back to Thumbnail only.
Then re-check Audience not-kids + Altered YES.
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

TITLES = [
    "What's Really Inside an Atom?",
    "Why Is the Periodic Table in This Order?",
    "How Small Can You Cut Gold?",
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
    with (EV / "tc_rearm_2226.log").open("a") as f:
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
    page.wait_for_timeout(3500)
    cos.dismiss(page)


def wait_changes_saved(page, timeout_ms: int = 20000) -> bool:
    deadline = time.time() + timeout_ms / 1000
    while time.time() < deadline:
        body = page.inner_text("body")
        if re.search(r"Changes saved|All changes saved|Saved", body, re.I):
            return True
        if re.search(r"trouble saving|problem saving|couldn.?t save|try again", body, re.I):
            return False
        page.wait_for_timeout(400)
    body = page.inner_text("body")
    return bool(re.search(r"Changes saved|All changes saved|Saved", body, re.I))


def content_shows_a(page) -> dict:
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
    shot(page, "TC_REARM_2226_content.png")
    # Crop/row heuristic: C has HIDDEN NUMBER text in alt/surrounding; A has atom wording
    body = page.inner_text("body")
    return {
        "has_title": "What's Really Inside an Atom" in body,
        "mentions_hidden_number": bool(re.search(r"HIDDEN NUMBER|Hidden Number", body)),
    }


def open_ab_dialog(page) -> dict:
    out = {"actions": []}
    try:
        page.get_by_role(
            "button", name=re.compile(r"^A/B Testing$|Test & Compare|Add test", re.I)
        ).first.click(timeout=2500)
        out["actions"].append("opened_role")
    except Exception:
        hit = page.evaluate(
            """() => {
              let hit=null;
              const walk=(r,d=0)=>{
                if(!r||d>55||hit) return;
                for (const el of (r.querySelectorAll
                  ? r.querySelectorAll('button,[role=button],a,ytcp-button') : [])) {
                  const t=(el.innerText||el.getAttribute('aria-label')||'').trim();
                  if (!/^(A\\/B Testing|Test & Compare|Add test|Get started)$/i.test(t)
                      && !/^A\\/B Testing$/i.test(t)) continue;
                  if (/Edit title/i.test(t)) continue;
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
        out["actions"].append({"opened_deep": hit})
    page.wait_for_timeout(1500)
    body = page.inner_text("body")
    # If "Run a new test? Your current test will be deleted" — Cancel (we already cleared)
    if re.search(r"current test will be deleted|Run a new test", body, re.I):
        try:
            page.get_by_role("button", name=re.compile(r"^Continue$", re.I)).first.click(
                timeout=1500
            )
            out["actions"].append("continue_replace")
            page.wait_for_timeout(1500)
        except Exception:
            pass
    shot(page, "TC_REARM_2226_01_dialog.png")
    out["body_snip"] = page.inner_text("body")[:1200]
    out["ineligible"] = bool(re.search(r"Ineligible|not eligible", out["body_snip"], re.I))
    return out


def click_mode(page, label: str) -> bool:
    """Click Title and thumbnail / Thumbnail only / Title only inside dialog."""
    # Prefer exact button/toggle text
    for role in ("button", "radio", "tab"):
        try:
            page.get_by_role(role, name=re.compile(rf"^{re.escape(label)}$", re.I)).first.click(
                timeout=1200
            )
            return True
        except Exception:
            continue
    # Deep click by exact innerText
    hit = page.evaluate(
        """(label) => {
          let hit=null;
          const walk=(r,d=0)=>{
            if(!r||d>55||hit) return;
            for (const el of (r.querySelectorAll
              ? r.querySelectorAll('button,[role=button],[role=radio],[role=tab],ytcp-button,div,span')
              : [])) {
              const t=(el.innerText||'').trim();
              if (t !== label) continue;
              const rect=el.getBoundingClientRect();
              if (rect.width<5||rect.height<5||rect.y<40) continue;
              el.click(); hit=t; return;
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if(el.shadowRoot) walk(el.shadowRoot,d+1);
          };
          walk(document); return hit;
        }""",
        label,
    )
    return bool(hit)


def fill_titles(page) -> int:
    return page.evaluate(
        """(titles) => {
          const boxes=[];
          const walk=(r,d=0)=>{
            if(!r||d>55) return;
            for (const el of (r.querySelectorAll
              ? r.querySelectorAll('input,textarea,[contenteditable=true]') : [])) {
              const a=(el.getAttribute('aria-label')||el.getAttribute('placeholder')||'');
              if (/title/i.test(a) || el.getAttribute('maxlength')==='100') boxes.push(el);
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if(el.shadowRoot) walk(el.shadowRoot,d+1);
          };
          walk(document);
          for (let i=0;i<Math.min(boxes.length,titles.length);i++){
            const b=boxes[i];
            if (b.isContentEditable) {
              b.focus(); b.textContent=titles[i];
              b.dispatchEvent(new Event('input',{bubbles:true}));
            } else {
              const proto=b.tagName==='TEXTAREA'
                ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype;
              Object.getOwnPropertyDescriptor(proto,'value').set.call(b,titles[i]);
              b.dispatchEvent(new Event('input',{bubbles:true}));
            }
          }
          return boxes.length;
        }""",
        TITLES,
    )


def upload_three(page) -> dict:
    out = {"uploaded": []}
    files = [str(THUMB_A), str(THUMB_C), str(THUMB_B)]
    loc = page.locator('input[type="file"]')
    n = loc.count()
    out["n"] = n
    for i in range(min(n, 3)):
        try:
            loc.nth(i).set_input_files(files[i])
            out["uploaded"].append(i)
            page.wait_for_timeout(800)
        except Exception as e:
            out.setdefault("errs", []).append({"i": i, "err": type(e).__name__})
    return out


def set_test_and_save(page) -> dict:
    out = {"set": False, "saved": False, "changes_saved": False}
    for name in (r"^Set test$", r"^Done$", r"^Create$", r"^Publish test$", r"^Save$"):
        try:
            btn = page.get_by_role("button", name=re.compile(name, re.I)).first
            # Skip disabled
            disabled = btn.get_attribute("aria-disabled") or btn.get_attribute("disabled")
            if disabled in ("true", "disabled", ""):
                # empty disabled attr can mean present; check class/enabled via evaluate
                en = btn.evaluate("el => !(el.disabled || el.getAttribute('aria-disabled')==='true')")
                if not en:
                    continue
            btn.click(timeout=1500)
            out["set"] = True
            out["set_via"] = name
            page.wait_for_timeout(1500)
            break
        except Exception:
            continue
    shot(page, "TC_REARM_2226_02_after_set.png")
    # Details-page Save (toast said test starts once you save)
    out["saved"] = cos.save_named(page)
    page.wait_for_timeout(800)
    out["changes_saved"] = wait_changes_saved(page, 25000)
    body = page.inner_text("body")
    out["trouble"] = bool(
        re.search(r"trouble saving|problem saving|couldn.?t save|try again", body, re.I)
    )
    shot(page, "TC_REARM_2226_03_after_save.png")
    return out


def arm_mode(page, mode: str) -> dict:
    """mode: 'Title and thumbnail' or 'Thumbnail only'."""
    out = {"mode": mode, "actions": []}
    opened = open_ab_dialog(page)
    out["open"] = opened
    if opened.get("ineligible"):
        out["blocked"] = True
        try:
            page.get_by_role("button", name=re.compile(r"^Cancel$", re.I)).first.click(timeout=1000)
        except Exception:
            page.keyboard.press("Escape")
        return out

    if not click_mode(page, mode):
        out["mode_click"] = False
        out["note"] = f"could not click mode {mode}"
        page.keyboard.press("Escape")
        return out
    out["mode_click"] = True
    page.wait_for_timeout(1000)
    shot(page, f"TC_REARM_2226_mode_{mode.replace(' ', '_')}.png")

    up = upload_three(page)
    out["upload"] = up
    if mode == "Title and thumbnail":
        n = fill_titles(page)
        out["titles_filled"] = n
        # Also try filling empty "Add title 2/3" via keyboard if needed
        page.wait_for_timeout(400)

    ss = set_test_and_save(page)
    out["set_save"] = ss
    open_edit(page)
    out["after_state"] = cos.read_tc_state(page)
    shot(page, "TC_REARM_2226_04_reload.png")
    return out


def restore_thumb_a_if_needed(page, confirm: dict) -> dict:
    """If Content no longer looks like A / edit shows HIDDEN NUMBER, re-upload A once."""
    out = {"needed": False, "restored": False}
    open_edit(page)
    shot(page, "TC_REARM_2226_05_thumb_check.png")
    # Visual: right-rail / custom thumb area — check page for HIDDEN NUMBER in preview alt
    # Heuristic from screenshot text won't catch image; use content list confirm flag
    # Re-open content was already done; if mentions_hidden_number or we detect C in edit:
    prev = page.evaluate(
        """() => {
          const imgs=[...document.querySelectorAll('img')];
          for (const img of imgs) {
            const alt=(img.getAttribute('alt')||'');
            const src=img.currentSrc||img.src||'';
            const rect=img.getBoundingClientRect();
            if (rect.width<80||rect.height<45) continue;
            if (/HIDDEN NUMBER/i.test(alt)) return {alt, src:src.slice(0,160), kind:'C'};
          }
          return null;
        }"""
    )
    body = page.inner_text("body")
    # If custom thumbnail section still Ineligible / or we previously saw C after bad rearm
    # Safer: always verify by re-checking content list was A; only restore if confirm failed
    if confirm.get("mentions_hidden_number") or (prev and prev.get("kind") == "C"):
        out["needed"] = True
        loc = page.locator('input[type="file"]')
        n = loc.count()
        for i in range(n):
            accept = loc.nth(i).get_attribute("accept") or ""
            if re.search(r"image", accept, re.I) or n == 1:
                loc.nth(i).set_input_files(str(THUMB_A))
                break
        page.wait_for_timeout(1500)
        cos.save_named(page)
        out["restored"] = wait_changes_saved(page, 25000)
        shot(page, "TC_REARM_2226_06_thumb_restored.png")
    out["prev"] = prev
    return out


def main():
    ART.mkdir(parents=True, exist_ok=True)
    EV.mkdir(parents=True, exist_ok=True)
    result = {
        "at": datetime.now().isoformat(timespec="seconds"),
        "order": "Ben 22:26 re-arm T&C with Save; keep main thumb A",
        "videoId": VID,
    }
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
        page = browser.contexts[0].pages[0]
        cos.channel_ok(page)
        open_edit(page)
        result["before"] = cos.read_tc_state(page)
        shot(page, "TC_REARM_2226_00_before.png")

        # Prefer Title and thumbnail ×3
        arm = arm_mode(page, "Title and thumbnail")
        result["arm_title_thumb"] = arm

        # If blocked, 2-slot scramble, or mode click failed → Thumbnail only
        after = arm.get("after_state") or {}
        need_fallback = (
            arm.get("blocked")
            or arm.get("mode_click") is False
            or after.get("two_slot_title_test")
            or not (arm.get("set_save") or {}).get("set")
        )
        if need_fallback and not arm.get("blocked"):
            log(f"falling back to Thumbnail only; after={ {k:after.get(k) for k in after if k!='snip'} }")
            # If a bad pending test is staged, cancel via Undo if Save not yet done
            try:
                page.get_by_role("button", name=re.compile(r"^Undo changes$", re.I)).first.click(
                    timeout=1000
                )
                page.wait_for_timeout(800)
            except Exception:
                pass
            open_edit(page)
            # If 2-slot already saved, try end it first
            if after.get("two_slot_title_test"):
                body = page.inner_text("body")
                if re.search(r"A/B testing titles", body, re.I):
                    page.get_by_role("button", name=re.compile(r"^A/B Testing$", re.I)).first.click(
                        timeout=2000
                    )
                    page.wait_for_timeout(1000)
                    body2 = page.inner_text("body")
                    if re.search(r"current test will be deleted|Run a new test", body2, re.I):
                        try:
                            page.get_by_role(
                                "button", name=re.compile(r"^Continue$", re.I)
                            ).first.click(timeout=1500)
                            page.wait_for_timeout(1200)
                            # Cancel new wizard — we'll open Thumbnail only next
                            for pat in (r"^Cancel$", r"^Close$"):
                                try:
                                    page.get_by_role(
                                        "button", name=re.compile(pat, re.I)
                                    ).first.click(timeout=1000)
                                    break
                                except Exception:
                                    pass
                            page.keyboard.press("Escape")
                        except Exception:
                            pass
                    open_edit(page)

            arm2 = arm_mode(page, "Thumbnail only")
            result["arm_thumbnail_only"] = arm2
            result["mode_used"] = "Thumbnail only"
        else:
            result["mode_used"] = arm.get("mode") if not arm.get("blocked") else "blocked"

        # Confirm Content list A
        result["content"] = content_shows_a(page)
        result["thumb_restore"] = restore_thumb_a_if_needed(page, result["content"])
        # Re-confirm content after optional restore
        if result["thumb_restore"].get("restored"):
            result["content_after_restore"] = content_shows_a(page)

        # Audience + Altered
        open_edit(page)
        result["audience"] = cos.ensure_not_kids(page, context="after_tc_rearm_save")
        cos.show_more(page)
        for _ in range(25):
            if re.search(r"AI wasn|AI was used|Altered", page.inner_text("body"), re.I):
                break
            page.keyboard.press("PageDown")
            page.wait_for_timeout(80)
        result["altered"] = cos.read_ai_altered(page)
        result["tc_final"] = cos.read_tc_state(page)
        shot(page, "TC_REARM_2226_07_final.png")

        result["summary"] = {
            "mode_used": result.get("mode_used"),
            "content_has_title": result["content"].get("has_title"),
            "content_hidden_number_text": result["content"].get("mentions_hidden_number"),
            "thumb_restore_needed": result["thumb_restore"].get("needed"),
            "audience_not_kids": result["audience"].get("ok_not_kids"),
            "altered_yes": result["altered"].get("yes") is True,
            "tc_two_slot": result["tc_final"].get("two_slot_title_test"),
            "tc_ineligible": result["tc_final"].get("ineligible"),
            "titles": result["tc_final"].get("titles_present"),
        }
        dump("TC_REARM_2226_RESULT.json", result)
        log(f"SUMMARY {result['summary']}")
        return result


if __name__ == "__main__":
    main()
