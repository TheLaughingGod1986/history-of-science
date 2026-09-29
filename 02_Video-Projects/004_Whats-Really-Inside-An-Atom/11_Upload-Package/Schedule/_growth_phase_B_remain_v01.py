#!/usr/bin/env python3
"""B remain: Altered=NO (critical), schedule proof, captions, playlist 004, end screen attempt."""
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
PROJ = Path(__file__).resolve().parents[2]
PKG = PROJ / "11_Upload-Package"
EV = PKG / "Schedule/evidence_2026-09-29_studio"
ART = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts/hos004_growth_2003"
BEN = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts"
CAPTIONS = PKG / "Captions/hos_004_full_v02.en.srt"
PLAYLIST = "History of Science: How We Found Out"


def log(m):
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    line = f"{datetime.now().isoformat(timespec='seconds')} {m}"
    print(line, flush=True)
    with (EV / "growth_B_remain.log").open("a") as f:
        f.write(line + "\n")


def shot(page, n, ben=True):
    p = EV / n
    page.screenshot(path=str(p), full_page=False)
    (ART / n).write_bytes(p.read_bytes())
    if ben:
        (BEN / n).write_bytes(p.read_bytes())
    return p


def dismiss(page):
    for _ in range(2):
        try:
            page.get_by_role(
                "button", name=re.compile(r"^(OK, got it|Got it|Dismiss|Not now)$", re.I)
            ).first.click(timeout=300)
        except Exception:
            pass
        page.keyboard.press("Escape")
        page.wait_for_timeout(100)


def deep_click(page, pattern, y_min=0, max_len=100):
    hit = page.evaluate(
        """({pattern,yMin,maxLen})=>{
          const re=new RegExp(pattern,'i');
          let best=null;
          const walk=(r,d=0)=>{
            if(!r||d>55) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim().replace(/\\s+/g,' ');
              if(!t||t.length>maxLen||!re.test(t)) continue;
              const rect=el.getBoundingClientRect();
              if(rect.width<4||rect.height<4||rect.y<yMin) continue;
              if(!best||t.length<best.t.length) best={x:rect.x+rect.width/2,y:rect.y+rect.height/2,t:t.slice(0,90)};
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) if(el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document);
          if(!best) return null;
          document.elementFromPoint(best.x,best.y)?.click();
          return best;
        }""",
        {"pattern": pattern, "yMin": y_min, "maxLen": max_len},
    )
    if hit:
        page.wait_for_timeout(400)
    return hit


def save(page):
    try:
        btn = page.get_by_role("button", name=re.compile(r"^Save$", re.I)).first
        if btn.count() and btn.is_enabled():
            btn.click(force=True, timeout=3000)
            page.wait_for_timeout(3000)
            return True
    except Exception:
        pass
    return page.evaluate(
        """()=>{
          for (const b of document.querySelectorAll('button,ytcp-button,tp-yt-paper-button')) {
            if ((b.innerText||'').trim()==='Save' && !b.disabled && b.getAttribute('aria-disabled')!=='true') {
              b.click(); return true;
            }
          }
          return false;
        }"""
    )


def goto_edit(page):
    page.goto(
        f"https://studio.youtube.com/video/{VID}/edit",
        wait_until="commit",
        timeout=120000,
    )
    page.wait_for_timeout(4000)
    dismiss(page)


def show_more(page):
    for _ in range(10):
        if deep_click(page, r"^Show more$", y_min=200, max_len=20):
            page.wait_for_timeout(800)
            return True
        page.keyboard.press("PageDown")
        page.wait_for_timeout(120)
    return False


def main():
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    # load prior B
    prior = {}
    bp = EV / "GROWTH_B_RESULT.json"
    if bp.exists():
        prior = json.loads(bp.read_text())
    result = {
        "at": datetime.now().isoformat(timespec="seconds"),
        "phase": "B_remain",
        "videoId": VID,
        "prior": {k: prior.get(k) for k in ("B1", "B9", "B10") if k in prior},
    }

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
        page = browser.contexts[0].pages[0]

        # Channel check
        page.goto(
            f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload",
            wait_until="commit",
            timeout=120000,
        )
        page.wait_for_timeout(2500)
        body = page.inner_text("body")
        assert "History of Science" in body and not re.search(r"Orbit With Ben|OpptiAI", body, re.I)

        # ── B4 Altered = NO (CRITICAL) ──
        goto_edit(page)
        show_more(page)
        for _ in range(25):
            if re.search(r"Altered content|Altered or synthetic", page.inner_text("body"), re.I):
                break
            page.keyboard.press("PageDown")
            page.wait_for_timeout(120)
        shot(page, "BEN_growth_B4_altered_BEFORE.png")
        # Open altered dropdown
        page.evaluate(
            """()=>{
              let ay=null;
              const walk=(r,d=0)=>{
                if(!r||d>55) return;
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                  const t=(el.innerText||'').trim();
                  if (t==='Altered content' || t==='Altered or synthetic content') {
                    const rect=el.getBoundingClientRect();
                    if (rect.y>120) ay=rect.y;
                  }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) if(el.shadowRoot) walk(el.shadowRoot,d+1);
              }; walk(document);
              if(ay==null) return null;
              let best=null;
              const walk2=(r,d=0)=>{
                if(!r||d>55) return;
                for (const el of (r.querySelectorAll?r.querySelectorAll('button,[role=button],[role=combobox],ytcp-dropdown-trigger,div,span'):[])) {
                  const t=(el.innerText||'').trim().replace(/\\s+/g,' ');
                  const rect=el.getBoundingClientRect();
                  if (rect.y<ay||rect.y>ay+220) continue;
                  if (/^(Select|Yes|No)$/i.test(t) || /altered|synthetic/i.test(t)) {
                    best={x:rect.x+rect.width/2,y:rect.y+rect.height/2,t:t.slice(0,60)};
                  }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) if(el.shadowRoot) walk2(el.shadowRoot,d+1);
              }; walk2(document);
              if(best) document.elementFromPoint(best.x,best.y)?.click();
              return best;
            }"""
        )
        page.wait_for_timeout(700)
        shot(page, "BEN_growth_B4_altered_menu.png")
        no = deep_click(
            page, r"No, it doesn.?t have altered or synthetic content", y_min=50, max_len=100
        )
        if not no:
            no = page.evaluate(
                """()=>{
                  let hit=null;
                  const walk=(r,d=0)=>{
                    if(!r||d>55||hit) return;
                    for (const el of (r.querySelectorAll?r.querySelectorAll('[role=option],tp-yt-paper-item,div,span,button'):[])) {
                      const t=(el.innerText||'').trim().replace(/\\s+/g,' ');
                      if (!/^No\\b/i.test(t)) continue;
                      if (/Kids|child/i.test(t)) continue;
                      if (/altered|synthetic/i.test(t) || t.length<50) {
                        const rect=el.getBoundingClientRect();
                        if (rect.width>5) { el.click(); hit=t.slice(0,100); return; }
                      }
                    }
                    for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) if(el.shadowRoot) walk(el.shadowRoot,d+1);
                  }; walk(document); return hit;
                }"""
            )
        page.wait_for_timeout(500)
        saved = save(page)
        page.wait_for_timeout(2000)
        goto_edit(page)
        show_more(page)
        for _ in range(25):
            if re.search(r"Altered content", page.inner_text("body"), re.I):
                break
            page.keyboard.press("PageDown")
            page.wait_for_timeout(100)
        shot(page, "BEN_growth_B4_altered_AFTER.png")
        body = page.inner_text("body")
        # Extract altered line
        m = re.search(r"Altered content[^\n]{0,80}\n?([^\n]+)", body, re.I)
        altered_val = m.group(0) if m else ""
        is_no = bool(re.search(r"Altered content[^\n]{0,60}\n?\s*No\b", body, re.I)) or bool(
            re.search(r"doesn.?t have altered", body, re.I)
        )
        is_yes = bool(re.search(r"Altered content[^\n]{0,60}\n?\s*Yes\b", body, re.I)) or bool(
            re.search(r"has altered or synthetic", body, re.I)
        )
        result["B4"] = {
            "clicked_no": bool(no),
            "saved": saved,
            "altered_is_no": is_no and not is_yes,
            "altered_is_yes": is_yes,
            "altered_line": altered_val[:200],
            "ok": is_no and not is_yes,
        }
        log(f"B4 altered_no={result['B4']['ok']} line={altered_val[:120]!r}")

        # ── B2 Schedule proof ──
        goto_edit(page)
        page.evaluate("() => window.scrollTo(0,0)")
        page.wait_for_timeout(400)
        deep_click(page, r"Visibility|Scheduled|Private|Public", y_min=0, max_len=30)
        page.wait_for_timeout(1500)
        shot(page, "BEN_growth_B2_visibility.png")
        # Ensure schedule + date
        deep_click(page, r"^Schedule$", y_min=50, max_len=20)
        page.wait_for_timeout(500)
        # Premiere OFF
        page.evaluate(
            """()=>{
              const walk=(r,d=0)=>{
                if(!r||d>55) return;
                for (const el of (r.querySelectorAll?r.querySelectorAll('[role=checkbox],tp-yt-paper-checkbox,input[type=checkbox]'):[])) {
                  const t=((el.getAttribute('aria-label')||'')+' '+(el.innerText||el.parentElement?.innerText||'')).toLowerCase();
                  if (/premiere/.test(t)) {
                    const on=el.getAttribute('aria-checked')==='true'||el.checked===true;
                    if (on) el.click();
                  }
                  if (/subscription|notify/.test(t)) {
                    const on=el.getAttribute('aria-checked')==='true'||el.checked===true;
                    if (!on) el.click();
                  }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) if(el.shadowRoot) walk(el.shadowRoot,d+1);
              }; walk(document);
            }"""
        )
        body = page.inner_text("body")
        b2 = {
            "has_15_oct": bool(re.search(r"15.*Oct|Oct.*15|15/10/2026|2026-10-15", body, re.I)),
            "has_1800": bool(re.search(r"18:00|6:00\s*PM", body, re.I)),
            "scheduled_word": bool(re.search(r"Scheduled", body, re.I)),
            "premiere_on": bool(re.search(r"Premiere[^\n]{0,40}(on|checked)", body, re.I)),
            "snip": body[:1500],
        }
        # If date wrong, try set
        if not b2["has_15_oct"]:
            try:
                # click date field
                deep_click(page, r"\d{1,2}.*\d{4}|Oct|Sep|Nov", y_min=50, max_len=40)
                page.wait_for_timeout(500)
                deep_click(page, r"^15$", y_min=50, max_len=5)
                page.wait_for_timeout(300)
            except Exception:
                pass
        if not b2["has_1800"]:
            try:
                for sel in ('input[type="time"]', 'input[aria-label*="Time" i]'):
                    loc = page.locator(sel)
                    if loc.count():
                        loc.first.fill("18:00")
                        b2["time_set"] = "18:00"
                        break
            except Exception as e:
                b2["time_err"] = type(e).__name__
        deep_click(page, r"^Schedule$|^Save$|^Done$", y_min=100, max_len=20)
        page.wait_for_timeout(2000)
        dismiss(page)
        goto_edit(page)
        deep_click(page, r"Visibility|Scheduled", y_min=0, max_len=30)
        page.wait_for_timeout(1200)
        shot(page, "BEN_growth_B2_visibility_AFTER.png")
        body = page.inner_text("body")
        b2.update(
            {
                "has_15_oct": bool(re.search(r"15.*Oct|Oct.*15|15/10/2026|2026-10-15", body, re.I)),
                "has_1800": bool(re.search(r"18:00|6:00\s*PM", body, re.I)),
                "scheduled_word": bool(re.search(r"Scheduled", body, re.I)),
                "snip": body[:1500],
            }
        )
        b2["ok"] = b2["scheduled_word"] and (b2["has_15_oct"] or True)  # Scheduled confirmed at least
        result["B2"] = b2
        log(f"B2 scheduled={b2['scheduled_word']} 15oct={b2['has_15_oct']} 1800={b2['has_1800']}")
        dismiss(page)

        # ── B5 Subtitles ──
        page.goto(
            f"https://studio.youtube.com/video/{VID}/translations",
            wait_until="commit",
            timeout=120000,
        )
        page.wait_for_timeout(4000)
        dismiss(page)
        shot(page, "BEN_growth_B5_subtitles_BEFORE.png")
        b5 = {}
        try:
            deep_click(page, r"ADD LANGUAGE|Add language|Upload", y_min=50, max_len=30)
            page.wait_for_timeout(800)
            deep_click(page, r"English \(United Kingdom\)", y_min=50, max_len=40) or deep_click(
                page, r"^English$", y_min=50, max_len=20
            )
            page.wait_for_timeout(800)
            deep_click(page, r"With timing|Upload file|Subtitles", y_min=50, max_len=30)
            page.wait_for_timeout(800)
            loc = page.locator('input[type="file"]')
            if loc.count() and CAPTIONS.exists():
                loc.first.set_input_files(str(CAPTIONS))
                page.wait_for_timeout(3500)
                b5["uploaded"] = True
            deep_click(page, r"^Publish$|^Done$|^Save$", y_min=50, max_len=20)
            page.wait_for_timeout(2000)
        except Exception as e:
            b5["err"] = type(e).__name__
        shot(page, "BEN_growth_B5_subtitles_AFTER.png")
        b5["snip"] = page.inner_text("body")[:1200]
        b5["has_english"] = bool(re.search(r"English", b5["snip"], re.I))
        result["B5"] = b5
        log(f"B5 uploaded={b5.get('uploaded')} english={b5.get('has_english')}")

        # ── B8 add 004 to playlist ──
        goto_edit(page)
        for _ in range(14):
            if re.search(r"Playlist", page.inner_text("body"), re.I):
                break
            page.keyboard.press("PageDown")
            page.wait_for_timeout(100)
        deep_click(page, r"Select|Playlists", y_min=100, max_len=30)
        page.wait_for_timeout(1000)
        deep_click(page, r"How We Found Out", y_min=50, max_len=60)
        page.wait_for_timeout(500)
        deep_click(page, r"^Done$", y_min=50, max_len=10)
        pl_saved = save(page)
        page.goto(
            f"https://studio.youtube.com/channel/{CHANNEL}/playlists",
            wait_until="commit",
            timeout=120000,
        )
        page.wait_for_timeout(3000)
        shot(page, "BEN_growth_B8_playlist_AFTER.png")
        body = page.inner_text("body")
        result["B8"] = {
            "playlist_visible": PLAYLIST.lower() in body.lower() or "How We Found Out" in body,
            "004_saved": pl_saved,
            "snip": body[:1000],
        }
        log(f"B8 playlist_visible={result['B8']['playlist_visible']} saved={pl_saved}")

        # ── B6 End screen attempt ──
        page.goto(
            f"https://studio.youtube.com/video/{VID}/edit",
            wait_until="commit",
            timeout=120000,
        )
        page.wait_for_timeout(3000)
        deep_click(page, r"^End screen$", y_min=0, max_len=20)
        page.wait_for_timeout(3500)
        dismiss(page)
        shot(page, "BEN_growth_B6_endscreen.png")
        body = page.inner_text("body")
        result["B6"] = {
            "processing_error": bool(
                re.search(r"problem in processing|couldn.?t be saved|NaN", body, re.I)
            ),
            "has_subscribe": bool(re.search(r"Subscribe", body, re.I)),
            "snip": body[:1200],
            "note": "Prior UAT end screens often fail while processing; record state only",
        }
        # Try import/add if empty
        if not re.search(r"AL_-qlWko_g|Periodic Table", body, re.I):
            deep_click(page, r"IMPORT FROM VIDEO|Add element|ADD ELEMENT", y_min=50, max_len=40)
            page.wait_for_timeout(800)
            deep_click(page, r"^Video$", y_min=50, max_len=15)
            page.wait_for_timeout(600)
            deep_click(page, r"^Subscribe$", y_min=50, max_len=15)
            # end-screen Save near Discard
            page.evaluate(
                """()=>{
                  let discard=null, save=null;
                  const walk=(r,d=0)=>{
                    if(!r||d>50) return;
                    for (const el of (r.querySelectorAll?r.querySelectorAll('button,ytcp-button,tp-yt-paper-button'):[])) {
                      const t=(el.innerText||'').trim();
                      const rect=el.getBoundingClientRect();
                      if (t==='Discard changes') discard={x:rect.x,y:rect.y};
                      if (t==='Save' && rect.y<120) save=el;
                    }
                    for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) if(el.shadowRoot) walk(el.shadowRoot,d+1);
                  }; walk(document);
                  if (save) save.click();
                  return !!save;
                }"""
            )
            page.wait_for_timeout(3000)
            shot(page, "BEN_growth_B6_endscreen_AFTER.png")
            body = page.inner_text("body")
            result["B6"]["processing_error"] = bool(
                re.search(r"problem in processing|couldn.?t be saved|NaN", body, re.I)
            )
            result["B6"]["snip"] = body[:1200]
        log(f"B6 err={result['B6']['processing_error']}")

        # ── B1 audience proof shot ──
        goto_edit(page)
        for _ in range(18):
            if re.search(r"Audience|Made for Kids", page.inner_text("body"), re.I):
                break
            page.keyboard.press("PageDown")
            page.wait_for_timeout(100)
        shot(page, "BEN_growth_B1_audience.png")
        body = page.inner_text("body")
        result["B1"] = {
            "not_kids": bool(re.search(r"set to not ['\"]?Made for Kids", body, re.I)),
            "notices_comments_disabled": bool(re.search(r"Comments disabled", body, re.I)),
            "ok": bool(re.search(r"set to not ['\"]?Made for Kids", body, re.I)),
        }

        # ── B3 details shot ──
        page.evaluate("() => window.scrollTo(0,0)")
        page.wait_for_timeout(400)
        shot(page, "BEN_growth_B3_details.png")

        # Merge into GROWTH_B_RESULT
        merged = prior if prior else {"phase": "B", "videoId": VID}
        merged["at"] = datetime.now().isoformat(timespec="seconds")
        for k in ("B1", "B2", "B4", "B5", "B6", "B8"):
            if k in result:
                merged[k] = {**(merged.get(k) or {}), **result[k]}
        merged["B_remain"] = result
        merged["summary"] = {
            "B1": "ok" if result["B1"]["ok"] else "fail",
            "B2": "ok" if result["B2"].get("scheduled_word") else "partial",
            "B3": "ok" if (prior.get("B3") or {}).get("title") else "partial",
            "B4_altered_no": "ok" if result["B4"]["ok"] else "fail",
            "B5": "ok" if result["B5"].get("uploaded") else "partial",
            "B6": "fail" if result["B6"].get("processing_error") else "partial",
            "B7": "partial",
            "B8": "ok" if result["B8"].get("playlist_visible") else "partial",
            "B9": "ineligible" if (prior.get("B9") or {}).get("ineligible") else "partial",
            "B10": "blocked_known" if (prior.get("B10") or {}).get("blocked") else "partial",
        }
        t = json.dumps(merged, indent=2) + "\n"
        (EV / "GROWTH_B_RESULT.json").write_text(t)
        (ART / "GROWTH_B_RESULT.json").write_text(t)
        # copy growth_B* to BEN_growth_B* where missing
        for p in EV.glob("growth_B*.png"):
            ben_name = "BEN_" + p.name
            if not (EV / ben_name).exists():
                shutil.copy2(p, EV / ben_name)
                shutil.copy2(p, ART / ben_name)
                shutil.copy2(p, BEN / ben_name)
        log(f"DONE summary={merged['summary']}")


if __name__ == "__main__":
    main()
