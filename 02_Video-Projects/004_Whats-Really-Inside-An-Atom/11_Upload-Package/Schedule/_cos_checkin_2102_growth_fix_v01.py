#!/usr/bin/env python3
"""CoS check-in 21:02 — live re-verify/fix of Ben 20:03 growth order.

Rules from CoS:
1. Altered/AI use = NO (overrides earlier Yes).
2. Never broad 'first Yes' — target by aria-label/name; one control per save;
   re-read Audience = not Made for Kids after EVERY save.
3. T&C = 3 ordered pairs, else Thumbnail-only A/B/C with main title.
   Do not leave a 2-slot title test running.
Then end screen Specific 002, rest gaps, records. Shorts s02 v06 already built.
"""
from __future__ import annotations

import json
import re
import shutil
from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright

PORT = 9460
CHANNEL = "UCXp7HkBIl1LgaznXuZHJyRg"
VID = "GHZDsiH7L7A"
VID_002 = "AL_-qlWko_g"
PROJ = Path(__file__).resolve().parents[2]
PKG = PROJ / "11_Upload-Package"
EV = PKG / "Schedule/evidence_2026-09-29_studio"
ART = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts/hos004_cos_2102"
BEN = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts"

THUMB_A = (PROJ / "08_Thumbnail/Selected/hos_004_thumb_A_atom_live_v04.jpg").resolve()
THUMB_B = (PROJ / "08_Thumbnail/Selected/hos_004_thumb_B_cut_gold_live_v04.jpg").resolve()
THUMB_C = (PROJ / "08_Thumbnail/Selected/hos_004_thumb_C_hidden_number_live_v06.jpg").resolve()

TITLES = [
    "What's Really Inside an Atom?",
    "Why Is the Periodic Table in This Order?",
    "How Small Can You Cut Gold?",
]
MAIN_TITLE = TITLES[0]


def log(m: str) -> None:
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    line = f"{datetime.now().isoformat(timespec='seconds')} {m}"
    print(line, flush=True)
    with (EV / "cos_2102.log").open("a") as f:
        f.write(line + "\n")


def dump(n: str, o) -> None:
    t = json.dumps(o, indent=2) + "\n"
    (EV / n).write_text(t)
    (ART / n).write_text(t)


def shot(page, n: str, *, ben: bool = True) -> Path:
    p = EV / n
    page.screenshot(path=str(p), full_page=False)
    (ART / n).write_bytes(p.read_bytes())
    if ben:
        (BEN / n).write_bytes(p.read_bytes())
    return p


def dismiss(page) -> None:
    for name in (r"^(OK, got it|Got it|Dismiss|Not now)$",):
        try:
            page.get_by_role("button", name=re.compile(name, re.I)).first.click(timeout=250)
        except Exception:
            pass


def channel_ok(page) -> None:
    page.goto(
        f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload",
        wait_until="commit",
        timeout=90000,
    )
    page.wait_for_timeout(2500)
    body = page.inner_text("body")
    if "History of Science" not in body and CHANNEL not in page.url:
        raise SystemExit("ABORT: not on HOS Studio channel")
    # Hard refuse Orbit
    if re.search(r"Orbit With Ben|@OrbitWithBen", body):
        raise SystemExit("ABORT: Orbit channel detected")


def open_edit(page) -> None:
    page.goto(
        f"https://studio.youtube.com/video/{VID}/edit",
        wait_until="commit",
        timeout=90000,
    )
    page.wait_for_timeout(3500)
    dismiss(page)


def read_audience(page) -> dict:
    """Read Made-for-Kids by aria-label ONLY — never parent text (pollutes Yes+No)."""
    state = page.evaluate(
        """() => {
          const out = {yes_checked:null, no_checked:null, banner:null, radios:[]};
          const walk=(r,d=0)=>{
            if(!r||d>60) return;
            for (const el of (r.querySelectorAll
              ? r.querySelectorAll('[role=radio],input[type=radio],tp-yt-paper-radio-button')
              : [])) {
              // Prefer aria-label; fall back to OWN text only (not parent)
              const al=(el.getAttribute('aria-label')||'').trim();
              let own=(el.innerText||'').trim().replace(/\\s+/g,' ');
              // paper-radio often has empty own text — use first child formatted string
              if (!own) {
                const fs=el.querySelector && el.querySelector('yt-formatted-string, .label, span');
                if (fs) own=(fs.innerText||'').trim().replace(/\\s+/g,' ');
              }
              const label = al || own;
              if (!label || label.length>200) continue;
              if (/AI\\b|altered|synthetic/i.test(label)) continue;
              const checked = el.getAttribute('aria-checked')==='true' || el.checked===true;
              // Strict: Yes kids vs No kids — mutually exclusive patterns
              const kidsNo = /^No,\\s*it'?s\\s*not\\s*['\"]?Made for Kids/i.test(label)
                || /^No,\\s*set this channel as not\\s*Made for Kids/i.test(label);
              const kidsYes = !kidsNo && (
                /^Yes,\\s*it'?s\\s*Made for Kids/i.test(label)
                || /^Yes,\\s*set this channel as Made for Kids/i.test(label)
              );
              if (!kidsYes && !kidsNo) continue;
              out.radios.push({
                label: label.slice(0,120), checked, kidsYes, kidsNo, via: al ? 'aria' : 'own'
              });
              if (kidsYes) out.yes_checked = checked;
              if (kidsNo) out.no_checked = checked;
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
          };
          walk(document);
          const body=(document.body&&document.body.innerText)||'';
          out.banner = /This video is set to not\\s*['\"]?Made for Kids/i.test(body)
            || /set to not\\s*['\"]?Made for Kids/i.test(body);
          return out;
        }"""
    )
    # ok if No is checked, or banner says not-kids and Yes is not checked
    no_c = state.get("no_checked")
    yes_c = state.get("yes_checked")
    state["ok_not_kids"] = (no_c is True) or (bool(state.get("banner")) and yes_c is not True)
    state["fail_kids"] = yes_c is True and no_c is not True
    return state


def ensure_not_kids(page, *, context: str) -> dict:
    """If kids Yes is checked, click aria-labelled No radio only, then save alone."""
    st = read_audience(page)
    log(f"AUDIENCE[{context}] before={st}")
    if st.get("fail_kids"):
        # Click ONLY radio whose aria-label / own text is the kids-No line
        clicked = page.evaluate(
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
                  const label = al || own;
                  if (!label) continue;
                  if (/AI\\b|altered|synthetic/i.test(label)) continue;
                  if (!/^No,\\s*it'?s\\s*not\\s*['\"]?Made for Kids/i.test(label)
                      && !/^No,\\s*set this channel as not\\s*Made for Kids/i.test(label))
                    continue;
                  // Never click if this looks like Yes
                  if (/^Yes\\b/i.test(label)) continue;
                  el.click();
                  hit={label: label.slice(0,120), via: al ? 'aria' : 'own'};
                  return;
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                  if(el.shadowRoot) walk(el.shadowRoot,d+1);
              };
              walk(document);
              return hit;
            }"""
        )
        log(f"AUDIENCE[{context}] clicked_not_kids={clicked!r}")
        if not clicked:
            raise SystemExit(f"ABORT: kids Yes checked but could not find named No radio ({context})")
        page.wait_for_timeout(400)
        # One control → one save
        save_named(page)
        page.wait_for_timeout(1500)
        open_edit(page)
        st = read_audience(page)
        log(f"AUDIENCE[{context}] after_save={st}")
    if st.get("fail_kids") or not st.get("ok_not_kids"):
        raise SystemExit(f"ABORT: Audience not confirmed not-kids after {context}: {st}")
    return st


def save_named(page) -> bool:
    """Click the top Save button by role/name only."""
    try:
        page.get_by_role("button", name=re.compile(r"^Save$", re.I)).first.click(timeout=2500)
        page.wait_for_timeout(1200)
        return True
    except Exception:
        hit = page.evaluate(
            """() => {
              let hit=null;
              const walk=(r,d=0)=>{
                if(!r||d>50||hit) return;
                for (const el of (r.querySelectorAll
                  ? r.querySelectorAll('button,[role=button],ytcp-button') : [])) {
                  const t=(el.innerText||el.getAttribute('aria-label')||'').trim();
                  if (t!=='Save' && t!=='SAVE') continue;
                  const rect=el.getBoundingClientRect();
                  if (rect.y>0 && rect.y<140 && rect.width>20) {
                    el.click(); hit=true; return;
                  }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                  if(el.shadowRoot) walk(el.shadowRoot,d+1);
              };
              walk(document); return hit;
            }"""
        )
        page.wait_for_timeout(1200)
        return bool(hit)


def show_more(page) -> None:
    page.evaluate(
        """() => {
          const walk=(r,d=0)=>{
            if(!r||d>55) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('button,[role=button],ytcp-button'):[])) {
              const t=(el.innerText||'').trim();
              if (/^Show more$/i.test(t)) { el.click(); return true; }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if(el.shadowRoot) walk(el.shadowRoot,d+1);
          };
          walk(document);
        }"""
    )
    page.wait_for_timeout(800)


def read_ai_altered(page) -> dict:
    """Read AI use / Altered radios by aria-label — never kids radios."""
    return page.evaluate(
        """() => {
          const out={radios:[], no:null, yes:null, section:null};
          const walk=(r,d=0)=>{
            if(!r||d>60) return;
            for (const el of (r.querySelectorAll
              ? r.querySelectorAll('[role=radio],input[type=radio],tp-yt-paper-radio-button')
              : [])) {
              const al=(el.getAttribute('aria-label')||'').trim();
              const t=((el.innerText||'')+(el.parentElement?.innerText||''))
                .trim().replace(/\\s+/g,' ');
              const label = al || t;
              if (!/AI\\b|altered|synthetic/i.test(label)) continue;
              if (/Made for Kids/i.test(label)) continue;
              const checked = el.getAttribute('aria-checked')==='true' || el.checked===true;
              const isNo = /No,?\\s*AI wasn'?t used/i.test(label)
                || /doesn'?t have altered or synthetic/i.test(label)
                || (/^No\\b/i.test(label) && /AI|altered|synthetic/i.test(label));
              const isYes = /Yes,?\\s*AI was used/i.test(label)
                || /has altered or synthetic/i.test(label)
                || (/^Yes\\b/i.test(label) && /AI|altered|synthetic/i.test(label));
              out.radios.push({label:label.slice(0,140), checked, isNo, isYes});
              if (isNo) out.no = checked;
              if (isYes) out.yes = checked;
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if(el.shadowRoot) walk(el.shadowRoot,d+1);
          };
          walk(document);
          const body=(document.body&&document.body.innerText)||'';
          if (/Altered content/i.test(body)) out.section='Altered content';
          if (/AI use|altered or synthetic|AI wasn'?t used|AI was used/i.test(body))
            out.section = out.section || 'AI use';
          return out;
        }"""
    )


def set_ai_no(page) -> dict:
    """Set AI/Altered to No via named control only; save alone; re-read audience."""
    show_more(page)
    for _ in range(30):
        body = page.inner_text("body")
        if re.search(r"Altered content|AI wasn.?t used|AI was used|synthetic", body, re.I):
            break
        page.keyboard.press("PageDown")
        page.wait_for_timeout(120)
    shot(page, "COS2102_B4_altered_BEFORE.png")
    before = read_ai_altered(page)
    log(f"AI before={before}")
    out = {"before": before, "clicked": None, "saved": False}

    if before.get("no") is True and before.get("yes") is not True:
        out["already_no"] = True
        shot(page, "COS2102_B4_altered_AFTER.png")
        out["after"] = before
        return out

    clicked = page.evaluate(
        """() => {
          let hit=null;
          const walk=(r,d=0)=>{
            if(!r||d>60||hit) return;
            for (const el of (r.querySelectorAll
              ? r.querySelectorAll('[role=radio],input[type=radio],tp-yt-paper-radio-button,button,[role=option]')
              : [])) {
              const al=(el.getAttribute('aria-label')||'').trim();
              const t=((el.innerText||'')+(el.parentElement?.innerText||''))
                .trim().replace(/\\s+/g,' ');
              const label = al || t;
              if (/Made for Kids/i.test(label)) continue;
              const isNo = /No,?\\s*AI wasn'?t used/i.test(label)
                || /No,\\s*it doesn'?t have altered or synthetic content/i.test(label);
              if (!isNo) continue;
              el.click();
              hit=label.slice(0,140);
              return;
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if(el.shadowRoot) walk(el.shadowRoot,d+1);
          };
          walk(document);
          return hit;
        }"""
    )
    out["clicked"] = clicked
    log(f"AI clicked_no={clicked!r}")
    if not clicked:
        # Try opening dropdown labelled Altered / AI use, then pick No option by name
        page.evaluate(
            """() => {
              let ay=null;
              const walk=(r,d=0)=>{
                if(!r||d>55) return;
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                  const t=(el.innerText||'').trim();
                  if (t==='Altered content' || t==='AI use' || /^Altered/i.test(t) && t.length<40) {
                    const rect=el.getBoundingClientRect();
                    if (rect.y>120) ay=rect.y;
                  }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                  if(el.shadowRoot) walk(el.shadowRoot,d+1);
              };
              walk(document);
              if (ay==null) return null;
              const walk2=(r,d=0)=>{
                if(!r||d>55) return;
                for (const el of (r.querySelectorAll
                  ? r.querySelectorAll('button,[role=button],[role=combobox],ytcp-dropdown-trigger')
                  : [])) {
                  const t=(el.innerText||el.getAttribute('aria-label')||'').trim();
                  const rect=el.getBoundingClientRect();
                  if (rect.y<ay||rect.y>ay+300) continue;
                  if (/Yes|No|Select|altered|synthetic|AI/i.test(t)) { el.click(); return t; }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                  if(el.shadowRoot) walk2(el.shadowRoot,d+1);
              };
              return walk2(document);
            }"""
        )
        page.wait_for_timeout(600)
        shot(page, "COS2102_B4_altered_menu.png")
        clicked = page.evaluate(
            """() => {
              let hit=null;
              const walk=(r,d=0)=>{
                if(!r||d>60||hit) return;
                for (const el of (r.querySelectorAll
                  ? r.querySelectorAll('[role=option],tp-yt-paper-item,yt-formatted-string,div,span,button')
                  : [])) {
                  const t=(el.innerText||'').trim().replace(/\\s+/g,' ');
                  if (!t || t.length>100) continue;
                  if (/Made for Kids/i.test(t)) continue;
                  if (/No,?\\s*AI wasn'?t used/i.test(t)
                      || /doesn'?t have altered or synthetic/i.test(t)) {
                    el.click(); hit=t.slice(0,140); return;
                  }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                  if(el.shadowRoot) walk(el.shadowRoot,d+1);
              };
              walk(document); return hit;
            }"""
        )
        out["clicked"] = clicked
        log(f"AI menu_clicked_no={clicked!r}")

    page.wait_for_timeout(400)
    # ONE control → save
    out["saved"] = save_named(page)
    page.wait_for_timeout(1800)
    open_edit(page)
    aud = ensure_not_kids(page, context="after_ai_save")
    out["audience_after"] = aud
    show_more(page)
    for _ in range(25):
        if re.search(r"Altered|AI wasn|AI was used|synthetic", page.inner_text("body"), re.I):
            break
        page.keyboard.press("PageDown")
        page.wait_for_timeout(100)
    after = read_ai_altered(page)
    out["after"] = after
    shot(page, "COS2102_B4_altered_AFTER.png")
    out["ok"] = after.get("no") is True and after.get("yes") is not True
    log(f"AI after ok={out['ok']} {after}")
    return out


def read_tc_state(page) -> dict:
    body = page.inner_text("body")
    titles_present = [t for t in TITLES if t in body]
    return {
        "ineligible": bool(re.search(r"Ineligible|not eligible", body, re.I)),
        "has_ab_testing": bool(re.search(r"A/B testing|Test & Compare|Test and compare", body, re.I)),
        "titles_present": titles_present,
        "title_count": len(titles_present),
        "two_slot_title_test": len(titles_present) == 2,
        "snip": body[:1800],
    }


def fix_tc(page) -> dict:
    """Prefer 3 title+thumb pairs; else Thumbnail-only A/B/C. Clear 2-slot title test."""
    open_edit(page)
    for _ in range(18):
        if re.search(r"Test & Compare|A/B testing|Ineligible", page.inner_text("body"), re.I):
            break
        page.keyboard.press("PageDown")
        page.wait_for_timeout(100)
    shot(page, "COS2102_B9_tc_BEFORE.png")
    before = read_tc_state(page)
    log(f"T&C before={ {k:before[k] for k in before if k!='snip'} }")
    out = {"before": before, "mode": None, "actions": []}

    # Open T&C UI if possible
    try:
        page.get_by_role(
            "button", name=re.compile(r"Test & Compare|Add test|Get started|A/B Testing", re.I)
        ).first.click(timeout=2000)
        out["actions"].append("opened_tc_button")
        page.wait_for_timeout(1500)
    except Exception:
        page.evaluate(
            """() => {
              const walk=(r,d=0)=>{
                if(!r||d>55) return;
                for (const el of (r.querySelectorAll?r.querySelectorAll('a,button,[role=button]'):[])) {
                  const t=(el.innerText||el.getAttribute('aria-label')||'').trim();
                  if (/Test & Compare|Add test|Get started|A\\/B Testing/i.test(t) && t.length<40) {
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
    shot(page, "COS2102_B9_tc_DIALOG.png")

    if out["ineligible"]:
        out["mode"] = "blocked_ineligible"
        out["note"] = (
            "Studio Ineligible while scheduled/private. Cannot arm 3 pairs or "
            "Thumbnail-only until eligible. Details still lists titles — do not "
            "start a new 2-slot title test. Re-arm after 15 Oct public."
        )
        # If a 2-slot title list is showing on Details, try to remove/cancel test
        if before.get("two_slot_title_test"):
            for pat in (
                r"Remove test|End test|Delete test|Cancel test|Stop test",
                r"Remove|Delete",
            ):
                try:
                    page.get_by_role("button", name=re.compile(pat, re.I)).first.click(timeout=1200)
                    out["actions"].append(f"clicked_{pat}")
                    page.wait_for_timeout(800)
                    break
                except Exception:
                    pass
        shot(page, "COS2102_B9_tc_AFTER.png")
        open_edit(page)
        ensure_not_kids(page, context="after_tc_ineligible")
        out["after"] = read_tc_state(page)
        return out

    # Eligible path: prefer Title and thumbnail ×3, else Thumbnail only
    chose_title = False
    try:
        page.get_by_role(
            "button", name=re.compile(r"Title and thumbnail|Title \\+ thumbnail", re.I)
        ).first.click(timeout=1500)
        chose_title = True
        out["mode"] = "Title and thumbnail"
        out["actions"].append("chose_title_and_thumbnail")
    except Exception:
        try:
            page.get_by_role("radio", name=re.compile(r"Title and thumbnail", re.I)).first.click(
                timeout=1200
            )
            chose_title = True
            out["mode"] = "Title and thumbnail"
        except Exception:
            pass

    if not chose_title:
        try:
            page.get_by_role("button", name=re.compile(r"^Thumbnail$", re.I)).first.click(
                timeout=1500
            )
            out["mode"] = "Thumbnail only"
            out["actions"].append("fell_back_thumbnail_only")
        except Exception:
            try:
                page.get_by_role("radio", name=re.compile(r"^Thumbnail$", re.I)).first.click(
                    timeout=1200
                )
                out["mode"] = "Thumbnail only"
                out["actions"].append("fell_back_thumbnail_only_radio")
            except Exception:
                out["mode"] = "could_not_select_mode"
                out["note"] = "Could not select T&C mode; left untouched"
                shot(page, "COS2102_B9_tc_AFTER.png")
                return out

    page.wait_for_timeout(1000)

    # Upload thumbs A/B/C into file inputs if present
    files = [str(THUMB_A), str(THUMB_C), str(THUMB_B)]  # ordered A, C, B per Ben pairs
    try:
        loc = page.locator('input[type="file"]')
        n = loc.count()
        out["file_inputs"] = n
        for i in range(min(n, 3)):
            loc.nth(i).set_input_files(files[i])
            page.wait_for_timeout(800)
            out["actions"].append(f"uploaded_slot_{i}")
    except Exception as e:
        out["upload_err"] = type(e).__name__

    if out["mode"] == "Title and thumbnail":
        # Fill three title fields if editable
        try:
            page.evaluate(
                """(titles) => {
                  const boxes=[];
                  const walk=(r,d=0)=>{
                    if(!r||d>55) return;
                    for (const el of (r.querySelectorAll
                      ? r.querySelectorAll('input,textarea,[contenteditable=true]') : [])) {
                      const a=(el.getAttribute('aria-label')||el.getAttribute('placeholder')||'');
                      if (/title/i.test(a) || (el.getAttribute('maxlength')==='100')) boxes.push(el);
                    }
                    for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                      if(el.shadowRoot) walk(el.shadowRoot,d+1);
                  };
                  walk(document);
                  for (let i=0;i<Math.min(boxes.length, titles.length);i++){
                    const b=boxes[i];
                    if (b.isContentEditable) { b.textContent=titles[i];
                      b.dispatchEvent(new Event('input',{bubbles:true})); }
                    else {
                      const proto = b.tagName==='TEXTAREA'
                        ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype;
                      Object.getOwnPropertyDescriptor(proto,'value').set.call(b, titles[i]);
                      b.dispatchEvent(new Event('input',{bubbles:true}));
                    }
                  }
                  return boxes.length;
                }""",
                TITLES,
            )
            out["actions"].append("filled_3_titles")
        except Exception as e:
            out["title_fill_err"] = type(e).__name__

    # Save / Done if available
    for name in (r"^Save$", r"^Done$", r"^Create$", r"^Publish test$"):
        try:
            page.get_by_role("button", name=re.compile(name, re.I)).first.click(timeout=1200)
            out["actions"].append(f"tc_{name}")
            page.wait_for_timeout(1200)
            break
        except Exception:
            pass

    shot(page, "COS2102_B9_tc_AFTER.png")
    dismiss(page)
    open_edit(page)
    ensure_not_kids(page, context="after_tc_save")
    out["after"] = read_tc_state(page)
    # Guard: must not leave exactly 2 titles if we could change anything
    if out["after"].get("two_slot_title_test") and out.get("mode") == "Title and thumbnail":
        out["warning"] = "still_two_slot_after_attempt — prefer Thumbnail-only next pass"
    return out


def fix_endscreen(page) -> dict:
    """Bind end screen Video → Specific 002 + Subscribe, last ~20s."""
    out = {"actions": [], "ok": False}
    page.goto(
        f"https://studio.youtube.com/video/{VID}/edit",
        wait_until="commit",
        timeout=90000,
    )
    page.wait_for_timeout(3000)
    dismiss(page)
    # Prefer dedicated endscreen URL
    page.goto(
        f"https://studio.youtube.com/video/{VID}/endscreen",
        wait_until="commit",
        timeout=90000,
    )
    page.wait_for_timeout(3500)
    dismiss(page)
    shot(page, "COS2102_B6_endscreen_BEFORE.png")
    body = page.inner_text("body")
    if re.search(r"Oops|something went wrong", body, re.I):
        out["oops"] = True
        out["note"] = "End screen page Oops — Studio blocked"
        shot(page, "COS2102_B6_endscreen_AFTER.png")
        return out

    # Clear existing elements if needed, then add Video + Subscribe
    for pat in (r"ADD ELEMENT|Add element", r"^IMPORT FROM VIDEO$|Import from video"):
        try:
            page.get_by_role("button", name=re.compile(pat, re.I)).first.click(timeout=1500)
            out["actions"].append(pat)
            page.wait_for_timeout(800)
            break
        except Exception:
            pass

    # Add Video element
    try:
        page.get_by_role("button", name=re.compile(r"^Video$", re.I)).first.click(timeout=1500)
        out["actions"].append("add_video")
        page.wait_for_timeout(1000)
    except Exception:
        page.evaluate(
            """() => {
              const walk=(r,d=0)=>{
                if(!r||d>55) return;
                for (const el of (r.querySelectorAll?r.querySelectorAll('button,[role=button]'):[])) {
                  const t=(el.innerText||'').trim();
                  if (t==='Video') { el.click(); return true; }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                  if(el.shadowRoot) walk(el.shadowRoot,d+1);
              };
              walk(document);
            }"""
        )
        page.wait_for_timeout(1000)

    # Specific video
    try:
        page.get_by_role(
            "radio", name=re.compile(r"Specific video|By video URL", re.I)
        ).first.click(timeout=1500)
        out["actions"].append("specific_radio")
    except Exception:
        page.evaluate(
            """() => {
              const walk=(r,d=0)=>{
                if(!r||d>55) return;
                for (const el of (r.querySelectorAll
                  ? r.querySelectorAll('[role=radio],button,div,span') : [])) {
                  const t=(el.innerText||el.getAttribute('aria-label')||'').trim();
                  if (/Specific video|Choose a video|By video/i.test(t) && t.length<40) {
                    el.click(); return t;
                  }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                  if(el.shadowRoot) walk(el.shadowRoot,d+1);
              };
              walk(document);
            }"""
        )
        out["actions"].append("specific_deep")
    page.wait_for_timeout(800)

    # Type 002 id into search/URL field
    filled = page.evaluate(
        """(vid) => {
          const walk=(r,d=0)=>{
            if(!r||d>55) return null;
            for (const el of (r.querySelectorAll
              ? r.querySelectorAll('input,textarea,[contenteditable=true]') : [])) {
              const a=(el.getAttribute('aria-label')||el.getAttribute('placeholder')||'');
              if (/search|video|url|paste/i.test(a) || el.type==='search' || el.type==='text') {
                if (el.isContentEditable) { el.textContent=vid;
                  el.dispatchEvent(new Event('input',{bubbles:true})); return a||'ce'; }
                const proto = HTMLInputElement.prototype;
                Object.getOwnPropertyDescriptor(proto,'value').set.call(el, vid);
                el.dispatchEvent(new Event('input',{bubbles:true}));
                return a||el.type||'input';
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if(el.shadowRoot) {
                const x=walk(el.shadowRoot,d+1); if(x) return x;
              }
          };
          return walk(document);
        }""",
        VID_002,
    )
    out["filled_field"] = filled
    page.wait_for_timeout(500)
    try:
        page.keyboard.type(VID_002, delay=25)
    except Exception:
        pass
    page.wait_for_timeout(1500)
    # Click result mentioning Periodic Table or id
    page.evaluate(
        """() => {
          const walk=(r,d=0)=>{
            if(!r||d>55) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim().replace(/\\s+/g,' ');
              if (/Periodic Table|AL_-qlWko_g|How Did We Discover the Periodic/i.test(t)
                  && t.length<120) {
                const rect=el.getBoundingClientRect();
                if (rect.width>20 && rect.height>10) { el.click(); return t.slice(0,80); }
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if(el.shadowRoot) walk(el.shadowRoot,d+1);
          };
          walk(document);
        }"""
    )
    out["actions"].append("picked_002")
    page.wait_for_timeout(800)

    # Subscribe element
    try:
        page.get_by_role("button", name=re.compile(r"^Subscribe$", re.I)).first.click(timeout=1500)
        out["actions"].append("add_subscribe")
    except Exception:
        page.evaluate(
            """() => {
              const walk=(r,d=0)=>{
                if(!r||d>55) return;
                for (const el of (r.querySelectorAll?r.querySelectorAll('button,[role=button]'):[])) {
                  const t=(el.innerText||'').trim();
                  if (t==='Subscribe') { el.click(); return true; }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                  if(el.shadowRoot) walk(el.shadowRoot,d+1);
              };
              walk(document);
            }"""
        )
        out["actions"].append("add_subscribe_deep")
    page.wait_for_timeout(600)

    out["saved"] = save_named(page)
    page.wait_for_timeout(2500)
    body = page.inner_text("body")
    out["processing_error"] = bool(
        re.search(r"problem in processing|couldn.?t be saved|NaN|Oops", body, re.I)
    )
    out["has_subscribe"] = bool(re.search(r"Subscribe", body, re.I))
    out["has_002"] = bool(
        re.search(r"Periodic Table|AL_-qlWko_g|How Did We Discover the Periodic", body, re.I)
    )
    out["ok"] = out.get("saved") and not out["processing_error"]
    shot(page, "COS2102_B6_endscreen_AFTER.png")
    # Re-open details and confirm audience untouched
    open_edit(page)
    out["audience_after"] = ensure_not_kids(page, context="after_endscreen")
    return out


def verify_visibility(page) -> dict:
    open_edit(page)
    # Open visibility
    try:
        page.get_by_role("button", name=re.compile(r"Visibility|Scheduled|Private|Public", re.I)).first.click(
            timeout=2000
        )
    except Exception:
        page.evaluate(
            """() => {
              const walk=(r,d=0)=>{
                if(!r||d>55) return;
                for (const el of (r.querySelectorAll?r.querySelectorAll('button,[role=button],a'):[])) {
                  const t=(el.innerText||'').trim();
                  if (/^Visibility$|^Scheduled$|Schedule/i.test(t) && t.length<40) {
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
    shot(page, "COS2102_B2_visibility.png")
    body = page.inner_text("body")
    premiere = page.evaluate(
        """() => {
          let checked=null;
          const walk=(r,d=0)=>{
            if(!r||d>55) return;
            for (const el of (r.querySelectorAll
              ? r.querySelectorAll('[role=checkbox],input[type=checkbox]') : [])) {
              const al=(el.getAttribute('aria-label')||'').toLowerCase();
              const t=((el.innerText||'')+(el.parentElement?.innerText||'')).toLowerCase();
              if (/premiere/.test(al+t)) {
                checked = el.getAttribute('aria-checked')==='true' || el.checked===true;
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if(el.shadowRoot) walk(el.shadowRoot,d+1);
          };
          walk(document); return checked;
        }"""
    )
    st = {
        "has_15_oct": bool(re.search(r"15\s*Oct|Oct(?:ober)?\s*15|15/10/2026|2026-10-15", body, re.I)),
        "has_1800": bool(re.search(r"18:00|6:00\s*PM|6:00\s*pm", body)),
        "scheduled": bool(re.search(r"Scheduled", body, re.I)),
        "premiere_checked": premiere,
        "snip": body[:1000],
    }
    dismiss(page)
    return st


def main() -> dict:
    ART.mkdir(parents=True, exist_ok=True)
    EV.mkdir(parents=True, exist_ok=True)
    result = {
        "at": datetime.now().isoformat(timespec="seconds"),
        "cos": "21:02 check-in",
        "order": "Ben 20:03 growth-settings (unchanged)",
        "videoId": VID,
    }
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
        ctx = browser.contexts[0] if browser.contexts else browser.new_context()
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        channel_ok(page)

        # 1) Audience baseline
        open_edit(page)
        result["audience_baseline"] = ensure_not_kids(page, context="baseline")
        shot(page, "COS2102_B1_audience.png")

        # 2) Altered/AI = NO
        result["altered"] = set_ai_no(page)

        # 3) Visibility proof (no change unless needed)
        result["visibility"] = verify_visibility(page)
        open_edit(page)
        result["audience_after_visibility"] = ensure_not_kids(page, context="after_visibility_read")

        # 4) T&C
        result["tc"] = fix_tc(page)

        # 5) End screen Specific 002
        result["endscreen"] = fix_endscreen(page)

        # Final audience + AI proof
        open_edit(page)
        result["audience_final"] = ensure_not_kids(page, context="final")
        show_more(page)
        for _ in range(25):
            if re.search(r"Altered|AI wasn|AI was used|synthetic", page.inner_text("body"), re.I):
                break
            page.keyboard.press("PageDown")
            page.wait_for_timeout(100)
        result["altered_final"] = read_ai_altered(page)
        shot(page, "COS2102_FINAL_details.png")
        result["tc_final"] = read_tc_state(page)

        result["summary"] = {
            "audience_not_kids": result["audience_final"].get("ok_not_kids"),
            "altered_no": result["altered_final"].get("no") is True
            and result["altered_final"].get("yes") is not True,
            "tc_mode": result["tc"].get("mode"),
            "tc_two_slot": result["tc_final"].get("two_slot_title_test"),
            "endscreen_ok": result["endscreen"].get("ok"),
            "endscreen_err": result["endscreen"].get("processing_error"),
            "visibility_scheduled": result["visibility"].get("scheduled"),
            "premiere_off": result["visibility"].get("premiere_checked") is not True,
        }
        dump("COS_CHECKIN_2102_RESULT.json", result)
        log(f"SUMMARY {result['summary']}")
        return result


if __name__ == "__main__":
    main()
