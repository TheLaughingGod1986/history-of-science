#!/usr/bin/env python3
"""HOS 004 — force main custom thumb A v04; cancel A/B if blocking."""
from __future__ import annotations

import json
import re
import urllib.request
from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright

PORT = 9460
VIDEO_ID = "GHZDsiH7L7A"
PROJ = Path(__file__).resolve().parents[2]
EV = PROJ / "11_Upload-Package/Schedule/evidence_2026-09-29_studio"
ART = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts/hos004_studio_phone_uat"
THUMB_A = PROJ / "08_Thumbnail/Selected/hos_004_thumb_A_atom_live_v04.jpg"


def log(m: str) -> None:
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    line = f"{datetime.now().isoformat(timespec='seconds')} {m}"
    print(line, flush=True)
    with (EV / "phone_uat_v25.log").open("a") as f:
        f.write(line + "\n")


def dump(n, o):
    t = json.dumps(o, indent=2) + "\n"
    (EV / n).write_text(t)
    (ART / n).write_text(t)


def shot(page, n):
    p = EV / n
    page.screenshot(path=str(p), full_page=False)
    (ART / n).write_bytes(p.read_bytes())
    return p


def dismiss(page):
    for _ in range(2):
        page.keyboard.press("Escape")
        page.wait_for_timeout(100)


def click_text(page, pattern, y_min=40, max_len=80):
    return page.evaluate(
        """({pattern,yMin,maxLen}) => {
          const re=new RegExp(pattern,'i');
          let best=null;
          const walk=(r,d=0)=>{
            if(!r||d>55)return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim();
              if (!t || t.length>maxLen) continue;
              if (!re.test(t)) continue;
              const rect=el.getBoundingClientRect();
              if (rect.y<yMin || rect.width<6 || rect.height<6) continue;
              const score=Math.abs(t.length - Math.min(pattern.length,40)) + rect.y/1000;
              if (!best || score<best.score) best={el,t,score};
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
            }
          };
          walk(document);
          if (!best) return null;
          best.el.scrollIntoView({block:'center'});
          best.el.click();
          return best.t;
        }""",
        {"pattern": pattern, "yMin": y_min, "maxLen": max_len},
    )


def goto_edit(page):
    page.goto(
        f"https://studio.youtube.com/video/{VIDEO_ID}/edit",
        wait_until="domcontentloaded",
        timeout=90000,
    )
    page.wait_for_timeout(5000)
    dismiss(page)


def main():
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    (EV / "phone_uat_v25.log").write_text("")
    urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/version", timeout=3)
    result = {"at": datetime.now().isoformat(timespec="seconds")}

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}", timeout=30000)
        page = browser.contexts[0].pages[0]
        page.set_default_timeout(45000)
        try:
            page.bring_to_front()
        except Exception:
            pass

        log("v25 open details")
        goto_edit(page)
        shot(page, "v25_01_before.png")

        # Try cancel/remove A/B test if UI offers it
        log("v25 try clear A/B")
        click_text(page, r"^A/B Testing$", y_min=80, max_len=20)
        page.wait_for_timeout(2500)
        shot(page, "v25_02_ab.png")
        body = page.inner_text("body")
        result["ab_body_has_ineligible"] = "Ineligible" in body
        for pat in [
            r"^Cancel test$",
            r"^End test$",
            r"^Remove test$",
            r"^Delete test$",
            r"^Discard$",
            r"^Clear$",
            r"^Turn off$",
        ]:
            hit = click_text(page, pat, y_min=40, max_len=30)
            if hit:
                result["ab_clear"] = hit
                page.wait_for_timeout(1500)
                # confirm
                click_text(page, r"^Confirm$|^Yes$|^Remove$|^OK$", y_min=40, max_len=20)
                page.wait_for_timeout(1500)
                break
        page.keyboard.press("Escape")
        page.wait_for_timeout(500)
        goto_edit(page)

        # Scroll to thumbnail
        for _ in range(14):
            page.mouse.wheel(0, 400)
            page.wait_for_timeout(100)
            if re.search(r"Set a thumbnail|Custom thumbnail|Thumbnail", page.inner_text("body"), re.I):
                break
        shot(page, "v25_03_thumb_section.png")

        # Enumerate candidate click targets for file chooser
        cands = page.evaluate(
            """() => {
              const out=[];
              const walk=(r,d=0)=>{
                if(!r||d>55)return;
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                  const t=(el.innerText||'').trim();
                  const aria=(el.getAttribute('aria-label')||'');
                  const rect=el.getBoundingClientRect();
                  if (rect.y<150 || rect.y>850 || rect.width<20 || rect.height<15) continue;
                  const blob=(t+' '+aria);
                  if (/upload|thumbnail|custom|change|replace|add image|browse/i.test(blob) && blob.length<60) {
                    out.push({t:t.slice(0,40),aria:aria.slice(0,40),x:rect.x+rect.width/2,y:rect.y+rect.height/2,w:rect.width,h:rect.height});
                  }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                  if (el.shadowRoot) walk(el.shadowRoot,d+1);
                }
              }; walk(document);
              // uniq by y roughly
              out.sort((a,b)=>a.y-b.y);
              const uniq=[];
              for (const c of out) {
                if (!uniq.length || Math.abs(uniq[uniq.length-1].y-c.y)>25 || Math.abs(uniq[uniq.length-1].x-c.x)>40)
                  uniq.push(c);
              }
              return uniq.slice(0,20);
            }"""
        )
        result["cands"] = cands
        log(f"v25 cands {len(cands)}")

        uploaded = False
        attempts = []
        for c in cands:
            try:
                with page.expect_file_chooser(timeout=5000) as fc:
                    page.mouse.click(c["x"], c["y"])
                fc.value.set_files(str(THUMB_A))
                attempts.append({"cand": c, "ok": True})
                uploaded = True
                page.wait_for_timeout(4500)
                shot(page, "v25_04_after_chooser.png")
                break
            except Exception as e:
                attempts.append({"cand": {k: c[k] for k in ("t", "aria", "x", "y")}, "err": str(e)[:80]})
                dismiss(page)

        if not uploaded:
            # Last resort: all image file inputs
            loc = page.locator('input[type="file"]')
            for i in range(loc.count()):
                try:
                    loc.nth(i).set_input_files(str(THUMB_A))
                    attempts.append({"input": i, "ok": True})
                    uploaded = True
                    page.wait_for_timeout(4500)
                    break
                except Exception as e:
                    attempts.append({"input": i, "err": str(e)[:80]})

        result["attempts"] = attempts
        result["uploaded"] = uploaded

        # Save
        try:
            btn = page.get_by_role("button", name=re.compile(r"^Save$", re.I))
            if btn.count() and btn.first.is_enabled():
                btn.first.click(force=True)
                result["saved"] = True
                page.wait_for_timeout(5000)
            else:
                result["saved"] = False
        except Exception as e:
            result["saved"] = str(e)[:80]

        shot(page, "v25_05_after_save.png")
        goto_edit(page)
        page.wait_for_timeout(3000)
        shot(page, "v25_06_reload.png")
        t = page.inner_text("body")
        result["still_hidden_number"] = bool(re.search(r"HIDDEN NUMBER|THE HIDDEN", t, re.I))
        # Crop player for visual
        shot(page, "v25_07_final.png")

    dump("PHONE_UAT_V25_THUMB.json", result)
    log("DONE " + json.dumps(result, default=str)[:1800])
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
