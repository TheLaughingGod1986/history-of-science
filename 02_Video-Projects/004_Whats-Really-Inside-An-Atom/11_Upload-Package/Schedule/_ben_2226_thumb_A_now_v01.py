#!/usr/bin/env python3
"""Ben 22:26 TOP PRIORITY — set main thumbnail on GHZDsiH7L7A to A (atom v04).

If 2-slot T&C holds the thumb slot, stop/end that test first, then set A.
One targeted Thumbnail Upload file control → one Save → wait Changes saved →
reload → confirm Content list shows A. Retry once after 2–3 min if trouble saving.
Then re-check Audience not-kids + Altered YES. Re-arm T&C per Ben order after.
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
    with (EV / "thumb_A_2226.log").open("a") as f:
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


def end_ab_test_if_present(page) -> dict:
    """Stop/end the scrambled 2-slot title test if it holds the thumb slot."""
    out = {"actions": [], "had_two_slot": False, "ended": False}
    body = page.inner_text("body")
    titles = [t for t in TITLES if t in body]
    out["titles_present"] = titles
    out["had_two_slot"] = len(titles) == 2 and bool(
        re.search(r"A/B testing|Ineligible|Test & Compare", body, re.I)
    )
    shot(page, "THUMB_A_2226_01_before_tc.png")

    if not out["had_two_slot"] and not re.search(r"A/B testing titles", body, re.I):
        out["note"] = "no A/B testing titles block visible"
        return out

    # Open A/B Testing (not Edit title) — Cancel if "Run a new test?"
    clicked = page.evaluate(
        """() => {
          let hit=null;
          const walk=(r,d=0)=>{
            if(!r||d>55||hit) return;
            for (const el of (r.querySelectorAll
              ? r.querySelectorAll('button,[role=button],a,ytcp-button') : [])) {
              const t=(el.innerText||el.getAttribute('aria-label')||'').trim();
              if (!/A\\/B Testing|Test & Compare|Remove test|End test|Delete test|Stop test/i.test(t))
                continue;
              if (/Edit title/i.test(t)) continue;
              if (t.length>40) continue;
              const rect=el.getBoundingClientRect();
              if (rect.y<80||rect.width<5) continue;
              el.click(); hit=t; return;
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if(el.shadowRoot) walk(el.shadowRoot,d+1);
          };
          walk(document); return hit;
        }"""
    )
    out["actions"].append({"open_ab": clicked})
    page.wait_for_timeout(1200)
    shot(page, "THUMB_A_2226_02_ab_dialog.png")
    body = page.inner_text("body")

    # If "Run a new test? Your current test will be deleted" — Continue ONLY to clear,
    # then immediately cancel/close without creating a new test. Ben said stop/end the
    # scrambled test first. Prefer Remove/End/Delete if available; else Continue then Cancel.
    if re.search(r"current test will be deleted|Run a new test", body, re.I):
        # Prefer explicit end/remove controls in any open UI first
        removed = False
        for pat in (r"^Remove test$", r"^End test$", r"^Delete test$", r"^Stop test$"):
            try:
                page.get_by_role("button", name=re.compile(pat, re.I)).first.click(timeout=1000)
                out["actions"].append(f"clicked_{pat}")
                removed = True
                page.wait_for_timeout(1000)
                break
            except Exception:
                pass
        if not removed:
            # Continue deletes current test — then Cancel so we don't start a new one
            try:
                page.get_by_role("button", name=re.compile(r"^Continue$", re.I)).first.click(
                    timeout=2000
                )
                out["actions"].append("continue_delete_current_test")
                page.wait_for_timeout(2000)
                shot(page, "THUMB_A_2226_03_after_continue.png")
                # Cancel / close any new-test wizard without setting it
                for pat in (r"^Cancel$", r"^Close$", r"^Discard$", r"^Back$"):
                    try:
                        page.get_by_role("button", name=re.compile(pat, re.I)).first.click(
                            timeout=1200
                        )
                        out["actions"].append(f"cancel_new_{pat}")
                        page.wait_for_timeout(600)
                        break
                    except Exception:
                        pass
                page.keyboard.press("Escape")
                page.wait_for_timeout(400)
                removed = True
            except Exception as e:
                out["actions"].append({"continue_err": type(e).__name__})
                # Fallback: Cancel the dialog without deleting
                try:
                    page.get_by_role("button", name=re.compile(r"^Cancel$", re.I)).first.click(
                        timeout=1000
                    )
                    out["actions"].append("cancelled_without_delete")
                except Exception:
                    pass
        out["ended"] = removed
    else:
        # Look for Remove/End in panel
        for pat in (r"^Remove test$", r"^End test$", r"^Delete test$", r"^Stop test$", r"^Remove$"):
            try:
                page.get_by_role("button", name=re.compile(pat, re.I)).first.click(timeout=1000)
                out["actions"].append(f"clicked_{pat}")
                out["ended"] = True
                page.wait_for_timeout(1000)
                break
            except Exception:
                continue
        # Close leftover
        page.keyboard.press("Escape")
        page.wait_for_timeout(300)

    open_edit(page)
    body = page.inner_text("body")
    out["titles_after"] = [t for t in TITLES if t in body]
    out["still_two_slot"] = len(out["titles_after"]) == 2
    shot(page, "THUMB_A_2226_04_after_tc_clear.png")
    log(f"T&C clear ended={out['ended']} still_two={out['still_two_slot']} actions={out['actions']}")
    return out


def upload_thumb_a(page) -> dict:
    """Target Thumbnail Upload file by aria-label; set A; one Save."""
    out = {"file": str(THUMB_A), "uploaded": False, "saved": False}
    assert THUMB_A.exists(), f"missing {THUMB_A}"

    # Scroll to Thumbnail section
    for _ in range(20):
        if re.search(r"^Thumbnail$|Upload file|Custom thumbnail", page.inner_text("body"), re.I):
            break
        page.keyboard.press("PageDown")
        page.wait_for_timeout(120)
    shot(page, "THUMB_A_2226_05_thumb_section.png")

    # Prefer file input near Thumbnail with accept=image
    uploaded = page.evaluate(
        """() => {
          const infos=[];
          const walk=(r,d=0)=>{
            if(!r||d>55) return;
            for (const inp of (r.querySelectorAll
              ? r.querySelectorAll('input[type=file]') : [])) {
              const al=(inp.getAttribute('aria-label')||'');
              const acc=(inp.getAttribute('accept')||'');
              const name=(inp.getAttribute('name')||'');
              const rect=inp.getBoundingClientRect();
              infos.push({al,acc,name,y:Math.round(rect.y),w:rect.width,h:rect.height});
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if(el.shadowRoot) walk(el.shadowRoot,d+1);
          };
          walk(document);
          return infos;
        }"""
    )
    out["file_inputs"] = uploaded
    log(f"file_inputs={uploaded}")

    # Click "Upload file" near Thumbnail by aria-label / role
    try:
        page.get_by_role(
            "button", name=re.compile(r"Upload file|Upload thumbnail|Custom thumbnail", re.I)
        ).first.click(timeout=2000)
        out["clicked_upload_btn"] = True
        page.wait_for_timeout(600)
    except Exception:
        out["clicked_upload_btn"] = False
        # deep click Upload file near Thumbnail heading
        page.evaluate(
            """() => {
              let ty=null;
              const walk=(r,d=0)=>{
                if(!r||d>55) return;
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                  const t=(el.innerText||'').trim();
                  if (t==='Thumbnail') {
                    const rect=el.getBoundingClientRect();
                    if (rect.y>100) ty=rect.y;
                  }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                  if(el.shadowRoot) walk(el.shadowRoot,d+1);
              };
              walk(document);
              if (ty==null) return null;
              const walk2=(r,d=0)=>{
                if(!r||d>55) return;
                for (const el of (r.querySelectorAll
                  ? r.querySelectorAll('button,[role=button],ytcp-button,label') : [])) {
                  const t=(el.innerText||el.getAttribute('aria-label')||'').trim();
                  const rect=el.getBoundingClientRect();
                  if (rect.y<ty||rect.y>ty+400) continue;
                  if (/Upload file|Upload|Custom thumbnail/i.test(t) && t.length<40) {
                    el.click(); return t;
                  }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                  if(el.shadowRoot) walk2(el.shadowRoot,d+1);
              };
              return walk2(document);
            }"""
        )
        page.wait_for_timeout(600)

    # Set files on the best matching input (image accept, near thumb, or first image)
    set_ok = False
    loc = page.locator('input[type="file"]')
    n = loc.count()
    out["input_count"] = n
    # Prefer accept containing image
    for i in range(n):
        try:
            accept = loc.nth(i).get_attribute("accept") or ""
            al = loc.nth(i).get_attribute("aria-label") or ""
            if re.search(r"image|thumb", accept + " " + al, re.I) or n == 1:
                loc.nth(i).set_input_files(str(THUMB_A))
                out["uploaded_via"] = {"i": i, "accept": accept, "aria": al}
                set_ok = True
                break
        except Exception as e:
            out.setdefault("set_errs", []).append({"i": i, "err": type(e).__name__})
    if not set_ok and n:
        try:
            loc.first.set_input_files(str(THUMB_A))
            out["uploaded_via"] = {"i": 0, "fallback": True}
            set_ok = True
        except Exception as e:
            out["upload_err"] = type(e).__name__

    out["uploaded"] = set_ok
    page.wait_for_timeout(2000)
    shot(page, "THUMB_A_2226_06_after_upload.png")

    if not set_ok:
        return out

    # ONE Save
    out["saved_click"] = cos.save_named(page)
    page.wait_for_timeout(1000)
    out["changes_saved"] = wait_changes_saved(page, 25000)
    body = page.inner_text("body")
    out["trouble_saving"] = bool(
        re.search(r"trouble saving|problem saving|couldn.?t save|try again", body, re.I)
    )
    shot(page, "THUMB_A_2226_07_after_save.png")
    log(f"upload saved={out['saved_click']} changes_saved={out['changes_saved']} trouble={out['trouble_saving']}")
    return out


def content_list_shows_a(page) -> dict:
    """Reload Content list and judge if thumb looks like A (not C/HIDDEN NUMBER)."""
    out = {}
    page.goto(
        f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload",
        wait_until="commit",
        timeout=90000,
    )
    page.wait_for_timeout(4000)
    cos.dismiss(page)
    # Search for the video
    try:
        page.get_by_role("textbox", name=re.compile(r"Search", re.I)).first.fill(
            "What's Really Inside an Atom"
        )
        page.keyboard.press("Enter")
        page.wait_for_timeout(2500)
    except Exception:
        pass
    shot(page, "THUMB_A_2226_08_content_list.png")
    body = page.inner_text("body")
    out["has_title"] = "What's Really Inside an Atom" in body
    # Visual heuristic from page text around row — C often still labeled via alt?
    # Capture row screenshot area by evaluating img near the title
    info = page.evaluate(
        """() => {
          let hit=null;
          const walk=(r,d=0)=>{
            if(!r||d>55||hit) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('a,ytcp-video-row,div'):[])) {
              const t=(el.innerText||'').trim();
              if (!/What.?s Really Inside an Atom/i.test(t)) continue;
              if (t.length>300) continue;
              const img=el.querySelector('img');
              const src=img?(img.getAttribute('src')||img.currentSrc||''):'';
              const alt=img?(img.getAttribute('alt')||''):'';
              const rect=el.getBoundingClientRect();
              hit={src:src.slice(0,200), alt:alt.slice(0,80), y:Math.round(rect.y), t:t.slice(0,80)};
              return;
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if(el.shadowRoot) walk(el.shadowRoot,d+1);
          };
          walk(document); return hit;
        }"""
    )
    out["row"] = info
    # Also open edit preview thumb — check for HIDDEN NUMBER text in page (C marker)
    open_edit(page)
    page.wait_for_timeout(2000)
    shot(page, "THUMB_A_2226_09_edit_reload.png")
    # Right-rail preview: C has "THE HIDDEN NUMBER"; A has atom/cut visuals without that
    # Download preview img if possible
    prev = page.evaluate(
        """() => {
          const imgs=[...document.querySelectorAll('img')];
          let best=null;
          for (const img of imgs) {
            const src=img.currentSrc||img.src||'';
            const alt=(img.getAttribute('alt')||'');
            const rect=img.getBoundingClientRect();
            if (rect.width<80||rect.height<45) continue;
            // right rail preview often x>700
            if (rect.x>600 && rect.y>80 && rect.y<500) {
              best={src:src.slice(0,240), alt:alt.slice(0,80), w:Math.round(rect.width), h:Math.round(rect.height), x:Math.round(rect.x), y:Math.round(rect.y)};
              break;
            }
          }
          return best;
        }"""
    )
    out["edit_preview"] = prev
    body = page.inner_text("body")
    # Weak text signals
    out["page_mentions_hidden_number"] = bool(re.search(r"HIDDEN NUMBER|Hidden Number", body))
    out["ok_guess"] = None  # filled by caller after visual check
    return out


def rearm_tc(page) -> dict:
    """Re-arm T&C: prefer 3 title+thumb pairs; else Thumbnail-only A/B/C."""
    out = {"mode": None, "actions": []}
    open_edit(page)
    for _ in range(15):
        if re.search(r"Test & Compare|A/B testing|Ineligible", page.inner_text("body"), re.I):
            break
        page.keyboard.press("PageDown")
        page.wait_for_timeout(100)
    shot(page, "THUMB_A_2226_10_tc_rearm_before.png")
    try:
        page.get_by_role(
            "button", name=re.compile(r"Test & Compare|A/B Testing|Add test|Get started", re.I)
        ).first.click(timeout=2000)
        out["actions"].append("opened_tc")
        page.wait_for_timeout(1500)
    except Exception:
        page.evaluate(
            """() => {
              const walk=(r,d=0)=>{
                if(!r||d>55) return;
                for (const el of (r.querySelectorAll?r.querySelectorAll('button,[role=button],a'):[])) {
                  const t=(el.innerText||'').trim();
                  if (/Test & Compare|A\\/B Testing|Add test|Get started/i.test(t) && t.length<40) {
                    el.click(); return t;
                  }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                  if(el.shadowRoot) walk(el.shadowRoot,d+1);
              };
              walk(document);
            }"""
        )
        page.wait_for_timeout(1500)
        out["actions"].append("opened_tc_deep")

    body = page.inner_text("body")
    out["ineligible"] = bool(re.search(r"Ineligible|not eligible", body, re.I))
    shot(page, "THUMB_A_2226_11_tc_rearm_dialog.png")
    if out["ineligible"]:
        out["mode"] = "blocked_ineligible"
        out["note"] = "Still Ineligible while scheduled — cannot re-arm until public/eligible"
        # Cancel any replace dialog
        try:
            page.get_by_role("button", name=re.compile(r"^Cancel$", re.I)).first.click(timeout=1000)
        except Exception:
            pass
        page.keyboard.press("Escape")
        return out

    # Prefer Title and thumbnail
    chose = False
    for name in (r"Title and thumbnail", r"Titles and thumbnails", r"^Thumbnail$"):
        try:
            page.get_by_role("button", name=re.compile(name, re.I)).first.click(timeout=1500)
            out["mode"] = "Title and thumbnail" if "Title" in name else "Thumbnail only"
            chose = True
            out["actions"].append(f"chose_{name}")
            break
        except Exception:
            try:
                page.get_by_role("radio", name=re.compile(name, re.I)).first.click(timeout=1000)
                out["mode"] = "Title and thumbnail" if "Title" in name else "Thumbnail only"
                chose = True
                break
            except Exception:
                continue
    if not chose:
        out["mode"] = "could_not_select"
        return out

    page.wait_for_timeout(1000)
    files = [str(THUMB_A), str(THUMB_C), str(THUMB_B)]
    loc = page.locator('input[type="file"]')
    n = loc.count()
    out["file_inputs"] = n
    for i in range(min(n, 3)):
        try:
            loc.nth(i).set_input_files(files[i])
            out["actions"].append(f"uploaded_{i}")
            page.wait_for_timeout(700)
        except Exception as e:
            out["actions"].append(f"upload_err_{i}_{type(e).__name__}")

    if out["mode"] == "Title and thumbnail":
        page.evaluate(
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
                if (b.isContentEditable) { b.textContent=titles[i];
                  b.dispatchEvent(new Event('input',{bubbles:true})); }
                else {
                  const proto=b.tagName==='TEXTAREA'?HTMLTextAreaElement.prototype:HTMLInputElement.prototype;
                  Object.getOwnPropertyDescriptor(proto,'value').set.call(b,titles[i]);
                  b.dispatchEvent(new Event('input',{bubbles:true}));
                }
              }
              return boxes.length;
            }""",
            TITLES,
        )
        out["actions"].append("filled_titles")

    for name in (r"^Save$", r"^Done$", r"^Set test$", r"^Create$", r"^Publish test$"):
        try:
            page.get_by_role("button", name=re.compile(name, re.I)).first.click(timeout=1500)
            out["actions"].append(f"tc_{name}")
            page.wait_for_timeout(1500)
            break
        except Exception:
            pass
    shot(page, "THUMB_A_2226_12_tc_rearm_after.png")
    return out


def main():
    ART.mkdir(parents=True, exist_ok=True)
    EV.mkdir(parents=True, exist_ok=True)
    result = {
        "at": datetime.now().isoformat(timespec="seconds"),
        "order": "Ben 22:26 TOP PRIORITY thumb A on GHZDsiH7L7A",
        "videoId": VID,
        "thumb_a": str(THUMB_A),
    }
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
        page = browser.contexts[0].pages[0]
        cos.channel_ok(page)
        open_edit(page)

        # 1) End T&C if holding slot
        result["tc_clear"] = end_ab_test_if_present(page)

        # 2) Upload A
        result["upload"] = upload_thumb_a(page)

        # Retry once after 2–3 min if trouble saving
        if result["upload"].get("trouble_saving") or (
            result["upload"].get("uploaded") and not result["upload"].get("changes_saved")
        ):
            log("trouble saving — wait 150s then retry once")
            result["retry_wait_s"] = 150
            page.wait_for_timeout(150_000)
            open_edit(page)
            # don't re-scramble T&C; just upload again
            result["upload_retry"] = upload_thumb_a(page)

        # 3) Confirm content list / edit reload
        result["confirm"] = content_list_shows_a(page)

        # 4) Audience + Altered
        open_edit(page)
        result["audience"] = cos.ensure_not_kids(page, context="after_thumb_A")
        cos.show_more(page)
        for _ in range(25):
            if re.search(r"AI wasn|AI was used|Altered", page.inner_text("body"), re.I):
                break
            page.keyboard.press("PageDown")
            page.wait_for_timeout(80)
        result["altered"] = cos.read_ai_altered(page)
        shot(page, "THUMB_A_2226_13_audience_altered.png")

        # 5) Re-arm T&C
        result["tc_rearm"] = rearm_tc(page)
        open_edit(page)
        result["audience_final"] = cos.ensure_not_kids(page, context="after_tc_rearm")
        cos.show_more(page)
        for _ in range(20):
            if re.search(r"AI wasn|AI was used", page.inner_text("body"), re.I):
                break
            page.keyboard.press("PageDown")
            page.wait_for_timeout(80)
        result["altered_final"] = cos.read_ai_altered(page)
        shot(page, "THUMB_A_2226_14_final.png")

        result["summary"] = {
            "tc_ended": result["tc_clear"].get("ended"),
            "still_two_slot": result["tc_clear"].get("still_two_slot"),
            "uploaded": (result.get("upload_retry") or result["upload"]).get("uploaded"),
            "changes_saved": (result.get("upload_retry") or result["upload"]).get("changes_saved"),
            "trouble_saving": (result.get("upload_retry") or result["upload"]).get("trouble_saving"),
            "audience_not_kids": result["audience_final"].get("ok_not_kids"),
            "altered_yes": result["altered_final"].get("yes") is True,
            "tc_rearm_mode": result["tc_rearm"].get("mode"),
        }
        dump("THUMB_A_2226_RESULT.json", result)
        log(f"SUMMARY {result['summary']}")
        return result


if __name__ == "__main__":
    main()
