#!/usr/bin/env python3
"""Ben 22:26 recovery after T&C rearm trouble-saving / CDP drop.

1) Reload edit; end any staged 2-slot title test.
2) Confirm/restore main thumb A (one upload + one Save; if trouble wait 150s retry once).
3) Content list screenshot confirm A.
4) Audience not-kids + Altered YES.
5) Re-arm T&C via Thumbnail-only A/B/C (Title+thumb kept creating 2-slot scramble).
   One Save. If trouble — wait 150s, retry Thumbnail-only once, stop.
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
    with (EV / "recover_2226.log").open("a") as f:
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


def end_two_slot(page) -> dict:
    out = {"had": False, "ended": False, "actions": []}
    body = page.inner_text("body")
    titles = [t for t in cos.TITLES if t in body]
    out["titles"] = titles
    out["had"] = len(titles) == 2 or bool(
        re.search(r"A/B testing titles|title test has been set up", body, re.I)
    )
    shot(page, "RECOVER_2226_01_before.png")
    if not out["had"]:
        out["note"] = "no two-slot / staged title test visible"
        return out
    try:
        page.get_by_role("button", name=re.compile(r"^A/B Testing$", re.I)).first.click(
            timeout=2500
        )
        out["actions"].append("open_ab")
        page.wait_for_timeout(1200)
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
        page.wait_for_timeout(1200)
        out["actions"].append("open_ab_deep")
    shot(page, "RECOVER_2226_02_ab.png")
    body = page.inner_text("body")
    if re.search(r"current test will be deleted|Run a new test", body, re.I):
        try:
            page.get_by_role("button", name=re.compile(r"^Continue$", re.I)).first.click(
                timeout=2000
            )
            out["actions"].append("continue_delete")
            page.wait_for_timeout(2000)
        except Exception as e:
            out["actions"].append({"continue_err": type(e).__name__})
        for pat in (r"^Cancel$", r"^Close$", r"^Discard$"):
            try:
                page.get_by_role("button", name=re.compile(pat, re.I)).first.click(timeout=1200)
                out["actions"].append(f"cancel_{pat}")
                page.wait_for_timeout(600)
                break
            except Exception:
                pass
        page.keyboard.press("Escape")
        out["ended"] = True
    else:
        for pat in (r"^Remove test$", r"^End test$", r"^Delete test$", r"^Cancel$"):
            try:
                page.get_by_role("button", name=re.compile(pat, re.I)).first.click(timeout=1000)
                out["actions"].append(f"click_{pat}")
                out["ended"] = True
                page.wait_for_timeout(800)
                break
            except Exception:
                continue
        page.keyboard.press("Escape")
    # Undo leftover unsaved staged test if Save still active
    try:
        page.get_by_role("button", name=re.compile(r"^Undo changes$", re.I)).first.click(
            timeout=1000
        )
        out["actions"].append("undo")
        page.wait_for_timeout(800)
    except Exception:
        pass
    open_edit(page)
    body = page.inner_text("body")
    out["titles_after"] = [t for t in cos.TITLES if t in body]
    out["still_two"] = len(out["titles_after"]) == 2
    shot(page, "RECOVER_2226_03_after_clear.png")
    log(f"end_two_slot ended={out['ended']} still_two={out['still_two']} acts={out['actions']}")
    return out


def upload_a(page) -> dict:
    out = {"uploaded": False}
    assert THUMB_A.exists()
    for _ in range(18):
        if re.search(r"Thumbnail|Upload file|Custom thumbnail", page.inner_text("body"), re.I):
            break
        page.keyboard.press("PageDown")
        page.wait_for_timeout(100)
    loc = page.locator('input[type="file"]')
    n = loc.count()
    out["n"] = n
    for i in range(n):
        accept = loc.nth(i).get_attribute("accept") or ""
        if re.search(r"image", accept, re.I) or n == 1:
            loc.nth(i).set_input_files(str(THUMB_A))
            out["uploaded"] = True
            out["via"] = i
            break
    page.wait_for_timeout(2000)
    shot(page, "RECOVER_2226_04_after_upload.png")
    if not out["uploaded"]:
        return out
    out["saved_click"] = cos.save_named(page)
    page.wait_for_timeout(800)
    out["save"] = wait_saved(page, 25000)
    shot(page, "RECOVER_2226_05_after_save.png")
    log(f"upload_a save={out['save']}")
    return out


def content_confirm(page, tag: str) -> dict:
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
    shot(page, f"RECOVER_2226_{tag}_content.png")
    body = page.inner_text("body")
    return {
        "has_title": "What's Really Inside an Atom" in body,
        "mentions_hidden_number": bool(re.search(r"HIDDEN NUMBER", body)),
    }


def arm_thumbnail_only(page) -> dict:
    out = {"mode": "Thumbnail only", "actions": []}
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
    if re.search(r"current test will be deleted|Run a new test", body, re.I):
        try:
            page.get_by_role("button", name=re.compile(r"^Continue$", re.I)).first.click(
                timeout=1500
            )
            out["actions"].append("continue_replace")
            page.wait_for_timeout(1500)
        except Exception:
            pass
    shot(page, "RECOVER_2226_10_tc_dialog.png")
    if re.search(r"Ineligible|not eligible", body, re.I):
        out["blocked"] = True
        page.keyboard.press("Escape")
        return out
    # Click Thumbnail only
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
    shot(page, "RECOVER_2226_11_thumb_only.png")
    files = [str(THUMB_A), str(THUMB_C), str(THUMB_B)]
    loc = page.locator('input[type="file"]')
    n = loc.count()
    out["inputs"] = n
    for i in range(min(n, 3)):
        try:
            loc.nth(i).set_input_files(files[i])
            out["actions"].append(f"up_{i}")
            page.wait_for_timeout(800)
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
    shot(page, "RECOVER_2226_12_after_set.png")
    out["saved_click"] = cos.save_named(page)
    page.wait_for_timeout(800)
    out["save"] = wait_saved(page, 25000)
    shot(page, "RECOVER_2226_13_after_save.png")
    return out


def main():
    ART.mkdir(parents=True, exist_ok=True)
    EV.mkdir(parents=True, exist_ok=True)
    result = {
        "at": datetime.now().isoformat(timespec="seconds"),
        "order": "Ben 22:26 recover thumb A + Thumbnail-only T&C",
        "videoId": VID,
    }
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
        # Prefer a live page; create one if needed
        ctx = browser.contexts[0]
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        cos.channel_ok(page)
        open_edit(page)

        result["clear_tc"] = end_two_slot(page)

        # Ensure thumb A
        result["upload_a"] = upload_a(page)
        if result["upload_a"].get("save", {}).get("trouble") or (
            result["upload_a"].get("uploaded") and not result["upload_a"].get("save", {}).get("ok")
        ):
            log("trouble saving thumb — wait 150s then retry once")
            result["thumb_retry_wait_s"] = 150
            page.wait_for_timeout(150_000)
            open_edit(page)
            result["upload_a_retry"] = upload_a(page)

        result["content"] = content_confirm(page, "08")
        open_edit(page)
        result["audience"] = cos.ensure_not_kids(page, context="recover_after_thumb")
        cos.show_more(page)
        for _ in range(25):
            if re.search(r"AI wasn|AI was used", page.inner_text("body"), re.I):
                break
            page.keyboard.press("PageDown")
            page.wait_for_timeout(80)
        result["altered"] = cos.read_ai_altered(page)
        shot(page, "RECOVER_2226_09_audience_altered.png")

        # Thumbnail-only rearm
        result["tc_thumb_only"] = arm_thumbnail_only(page)
        if result["tc_thumb_only"].get("save", {}).get("trouble"):
            log("T&C Thumbnail-only trouble saving — wait 150s retry once")
            result["tc_retry_wait_s"] = 150
            page.wait_for_timeout(150_000)
            open_edit(page)
            # clear any staged mess first
            result["clear_before_tc_retry"] = end_two_slot(page)
            result["tc_thumb_only_retry"] = arm_thumbnail_only(page)

        # Final confirms
        result["content_final"] = content_confirm(page, "14")
        open_edit(page)
        # If T&C messed thumb, restore A once more (no second loop)
        body = page.inner_text("body")
        staged = bool(re.search(r"title test has been set up|A/B testing titles", body, re.I))
        result["tc_final"] = cos.read_tc_state(page)
        result["audience_final"] = cos.ensure_not_kids(page, context="recover_final")
        cos.show_more(page)
        for _ in range(20):
            if re.search(r"AI wasn|AI was used", page.inner_text("body"), re.I):
                break
            page.keyboard.press("PageDown")
            page.wait_for_timeout(80)
        result["altered_final"] = cos.read_ai_altered(page)
        shot(page, "RECOVER_2226_15_final.png")

        # If content still wrong after all, one last A restore (Ben: retry once total for trouble)
        result["summary"] = {
            "tc_cleared": result["clear_tc"].get("ended") or not result["clear_tc"].get("had"),
            "still_two_slot": result["tc_final"].get("two_slot_title_test"),
            "thumb_uploaded": (result.get("upload_a_retry") or result["upload_a"]).get("uploaded"),
            "thumb_saved": (result.get("upload_a_retry") or result["upload_a"]).get("save", {}).get(
                "ok"
            ),
            "content_has_title": result["content_final"].get("has_title"),
            "audience_not_kids": result["audience_final"].get("ok_not_kids"),
            "altered_yes": result["altered_final"].get("yes") is True,
            "tc_mode": "Thumbnail only",
            "tc_blocked": result["tc_thumb_only"].get("blocked"),
            "tc_saved": (
                result.get("tc_thumb_only_retry") or result["tc_thumb_only"]
            ).get("save", {}).get("ok"),
            "tc_trouble": (
                result.get("tc_thumb_only_retry") or result["tc_thumb_only"]
            ).get("save", {}).get("trouble"),
            "staged_title_test": staged,
        }
        dump("RECOVER_2226_RESULT.json", result)
        log(f"SUMMARY {result['summary']}")
        return result


if __name__ == "__main__":
    main()
