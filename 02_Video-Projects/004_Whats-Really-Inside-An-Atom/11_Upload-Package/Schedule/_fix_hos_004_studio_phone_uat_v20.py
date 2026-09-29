#!/usr/bin/env python3
"""HOS 004 Studio phone-UAT v20 — post Chrome restart finish pass."""
from __future__ import annotations

import json
import re
import urllib.request
from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright

PORT = 9460
VIDEO_ID = "GHZDsiH7L7A"
CHANNEL = "UCXp7HkBIl1LgaznXuZHJyRg"
PROJ = Path(__file__).resolve().parents[2]
EV = PROJ / "11_Upload-Package/Schedule/evidence_2026-09-29_studio"
ART = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts/hos004_studio_phone_uat"
THUMBS = [
    PROJ / "08_Thumbnail/Selected/hos_004_thumb_A_atom_live_v04.jpg",
    PROJ / "08_Thumbnail/Selected/hos_004_thumb_C_hidden_number_live_v06.jpg",
    PROJ / "08_Thumbnail/Selected/hos_004_thumb_B_cut_gold_live_v04.jpg",
]
TITLES = [
    "What's Really Inside an Atom?",
    "Why Is the Periodic Table in This Order?",
    "How Small Can You Cut Gold?",
]


def log(m: str) -> None:
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    line = f"{datetime.now().isoformat(timespec='seconds')} {m}"
    print(line, flush=True)
    with (EV / "phone_uat_v20.log").open("a") as f:
        f.write(line + "\n")


def dump(n: str, o) -> None:
    text = json.dumps(o, indent=2) + "\n"
    (EV / n).write_text(text)
    (ART / n).write_text(text)


def shot(page, n: str) -> None:
    p = EV / n
    page.screenshot(path=str(p), full_page=False)
    (ART / n).write_bytes(p.read_bytes())


def dismiss(page) -> None:
    for _ in range(3):
        page.keyboard.press("Escape")
        page.wait_for_timeout(150)
        page.evaluate(
            """() => {
          const walk=(r,d=0)=>{
            if(!r||d>40)return false;
            for (const el of (r.querySelectorAll?r.querySelectorAll('button,ytcp-button'):[])) {
              const t=(el.innerText||'').trim();
              if (/^(Continue|Cancel|Close|Done|OK|Dismiss|Got it|OK, got it|Not now)$/i.test(t)) {
                el.click(); return t;
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
            }
            return false;
          };
          return walk(document);
        }"""
        )


def goto_edit(page) -> None:
    page.goto(
        f"https://studio.youtube.com/video/{VIDEO_ID}/edit",
        wait_until="domcontentloaded",
        timeout=90000,
    )
    page.wait_for_timeout(4500)
    dismiss(page)


def save(page) -> bool:
    try:
        btn = page.get_by_role("button", name=re.compile(r"^Save$", re.I))
        if btn.count() and btn.first.is_enabled():
            btn.first.click(force=True, timeout=8000)
            page.wait_for_timeout(4000)
            return True
    except Exception:
        pass
    return False


def main() -> None:
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    (EV / "phone_uat_v20.log").write_text("")
    urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/version", timeout=3)
    result = {"at": datetime.now().isoformat(timespec="seconds"), "videoId": VIDEO_ID}

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}", timeout=30000)
        page = browser.contexts[0].pages[0]
        page.set_default_timeout(45000)

        log("v20 details")
        goto_edit(page)
        shot(page, "v20_01_details.png")
        t = page.inner_text("body")
        result["title_ok"] = "What's Really Inside an Atom?" in t
        result["ineligible"] = "Ineligible" in t

        log("v20 thumb A")
        for _ in range(5):
            page.mouse.wheel(0, 300)
            page.wait_for_timeout(100)
        loc = page.locator('input[type="file"]')
        uploaded = False
        for i in range(loc.count()):
            acc = (loc.nth(i).get_attribute("accept") or "").lower()
            if "image" in acc or "jpg" in acc or "png" in acc or "jpeg" in acc:
                try:
                    loc.nth(i).set_input_files(str(THUMBS[0]))
                    uploaded = True
                    break
                except Exception:
                    continue
        page.wait_for_timeout(2000)
        save(page)
        shot(page, "v20_02_thumb.png")
        result["thumb_upload"] = uploaded

        log("v20 kids NO + AI YES")
        goto_edit(page)
        for _ in range(22):
            if re.search(r"AI use|Was AI used|Audience", page.inner_text("body"), re.I):
                break
            page.evaluate(
                """() => {
              const walk=(r,d=0)=>{
                if(!r||d>55)return false;
                for (const el of (r.querySelectorAll?r.querySelectorAll('button,ytcp-button,span,div'):[])) {
                  if ((el.innerText||'').trim()==='Show more') { el.click(); return true; }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                  if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
                }
                return false;
              }; return walk(document);
            }"""
            )
            page.mouse.wheel(0, 500)
            page.wait_for_timeout(140)
        page.evaluate(
            """() => {
          const walk=(r,d=0)=>{
            if(!r||d>55)return false;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim();
              if (/No, it's not.?Made for Kids/i.test(t) && t.length<80) { el.click(); return true; }
              if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
            }
            return false;
          }; return walk(document);
        }"""
        )
        page.evaluate(
            """() => {
          let aiY=null;
          const find=(r,d=0)=>{
            if(!r||d>55)return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim();
              if (/^AI use$/i.test(t)||/Was AI used/i.test(t)) {
                const rect=el.getBoundingClientRect(); if(rect.y>80) aiY=rect.y;
              }
              if (el.shadowRoot) find(el.shadowRoot,d+1);
            }
          }; find(document);
          const walk=(r,d=0)=>{
            if(!r||d>55)return false;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim(); const rect=el.getBoundingClientRect();
              if (/Yes, AI was used/i.test(t) && t.length<60) { el.click(); return 'exact'; }
              if (aiY!=null && /^Yes$/.test(t) && rect.y>aiY && rect.y<aiY+450) { el.click(); return 'yes'; }
              if (el.shadowRoot) { const x=walk(el.shadowRoot,d+1); if(x) return x; }
            }
            return false;
          }; return {hit:walk(document),aiY};
        }"""
        )
        save(page)
        goto_edit(page)
        for _ in range(22):
            if re.search(r"AI use|Audience", page.inner_text("body"), re.I):
                break
            page.evaluate(
                """() => {
              const walk=(r,d=0)=>{
                if(!r||d>55)return false;
                for (const el of (r.querySelectorAll?r.querySelectorAll('button,ytcp-button,span,div'):[])) {
                  if ((el.innerText||'').trim()==='Show more') { el.click(); return true; }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                  if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
                }
                return false;
              }; return walk(document);
            }"""
            )
            page.mouse.wheel(0, 500)
            page.wait_for_timeout(120)
        page.evaluate(
            """() => {
          const walk=(r,d=0)=>{
            if(!r||d>55)return false;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim();
              if (/^AI use$/i.test(t)||/^Audience$/i.test(t)) { el.scrollIntoView({block:'center'}); return t; }
              if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
            }
            return false;
          }; return walk(document);
        }"""
        )
        page.wait_for_timeout(400)
        shot(page, "v20_03_ai_kids.png")
        tb = page.inner_text("body")
        result["kids_no"] = bool(re.search(r"set to not 'Made for Kids'", tb, re.I))
        result["kids_yes_bad"] = bool(re.search(r"set to 'Made for Kids'", tb, re.I))
        result["ai_yes"] = bool(re.search(r"Yes, AI was used|AI use[\s\S]{0,500}Yes", tb, re.I))

        log("v20 A/B")
        goto_edit(page)
        page.evaluate(
            """() => {
          const cands=[];
          const walk=(r,d=0)=>{
            if(!r||d>55)return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('button,ytcp-button'):[])) {
              if ((el.innerText||'').trim()==='A/B Testing') {
                const rect=el.getBoundingClientRect();
                if (rect.width>20 && rect.width<200 && rect.y>100) cands.push(el);
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
            }
          }; walk(document); if(cands[0]) cands[0].click();
        }"""
        )
        page.wait_for_timeout(2800)
        try:
            page.get_by_text("Title and thumbnail", exact=True).first.click(timeout=4000, force=True)
        except Exception:
            page.evaluate(
                """() => {
              const walk=(r,d=0)=>{
                if(!r||d>55)return false;
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                  if ((el.innerText||'').trim()==='Title and thumbnail') { el.click(); return true; }
                  if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
                }
                return false;
              }; return walk(document);
            }"""
            )
        page.wait_for_timeout(2000)
        shot(page, "v20_10_ab.png")
        loc = page.locator('input[type="file"]')
        idxs = []
        for i in range(loc.count()):
            acc = (loc.nth(i).get_attribute("accept") or "").lower()
            if "image" in acc or "jpg" in acc or "png" in acc or "jpeg" in acc:
                idxs.append(i)
        uploads = []
        for j, thumb in enumerate(THUMBS):
            done = False
            adds = page.evaluate(
                """() => {
              const adds=[];
              const walk=(r,d=0)=>{
                if(!r||d>55)return;
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                  if ((el.innerText||'').trim()==='Add thumbnail') {
                    const rect=el.getBoundingClientRect();
                    if (rect.y>100 && rect.width>80 && rect.height>30)
                      adds.push({x:rect.x+rect.width/2,y:rect.y+rect.height/2,y0:rect.y});
                  }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                  if (el.shadowRoot) walk(el.shadowRoot,d+1);
                }
              }; walk(document); adds.sort((a,b)=>a.y0-b.y0);
              const uniq=[]; for(const a of adds){ if(!uniq.length||Math.abs(uniq[uniq.length-1].y0-a.y0)>40) uniq.push(a);} return uniq;
            }"""
            )
            if adds:
                try:
                    with page.expect_file_chooser(timeout=10000) as fc:
                        page.mouse.click(adds[0]["x"], adds[0]["y"])
                    fc.value.set_files(str(thumb))
                    uploads.append({"slot": j + 1, "via": "chooser", "file": thumb.name})
                    done = True
                    page.wait_for_timeout(2600)
                except Exception:
                    pass
            if not done and j < len(idxs):
                loc.nth(idxs[j]).set_input_files(str(thumb))
                uploads.append({"slot": j + 1, "via": "input", "file": thumb.name})
                done = True
                page.wait_for_timeout(2600)
            if not done:
                uploads.append({"slot": j + 1, "err": "fail"})
            shot(page, f"v20_11_slot{j+1}.png")
            log(f"  slot {uploads[-1]}")
        for i, label in enumerate(["Add title 1", "Add title 2", "Add title 3"]):
            box = page.evaluate(
                """(label)=>{
              let best=null;
              const walk=(r,d=0)=>{
                if(!r||d>55)return;
                for (const node of (r.querySelectorAll?r.querySelectorAll('[contenteditable=true]'):[])) {
                  if ((node.getAttribute('aria-label')||'')===label) {
                    const rect=node.getBoundingClientRect(); best={x:rect.x+80,y:rect.y+40};
                  }
                }
                for (const node of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                  if (node.shadowRoot) walk(node.shadowRoot,d+1);
                }
              }; walk(document); return best;
            }""",
                label,
            )
            if not box:
                continue
            page.mouse.click(box["x"], box["y"])
            page.keyboard.press("Meta+a")
            page.keyboard.press("Backspace")
            page.keyboard.type(TITLES[i], delay=12)
            page.wait_for_timeout(200)
        vals = page.evaluate(
            """() => {
          const out=[];
          const walk=(r,d=0)=>{
            if(!r||d>55)return;
            for (const node of (r.querySelectorAll?r.querySelectorAll('[contenteditable=true]'):[])) {
              const aria=node.getAttribute('aria-label')||'';
              if (/Add title/.test(aria)) out.push({aria,val:(node.textContent||'').trim()});
            }
            for (const node of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if (node.shadowRoot) walk(node.shadowRoot,d+1);
            }
          }; walk(document); return out;
        }"""
        )
        shot(page, "v20_12_filled.png")
        body = page.inner_text("body")
        ready = bool(re.search(r"Title and thumbnail test ready", body, re.I))
        set_state = "missing"
        btn = page.get_by_role("button", name=re.compile(r"^Set test$", re.I))
        if btn.count():
            set_state = "enabled" if btn.first.is_enabled() else "disabled"
            if btn.first.is_enabled():
                btn.first.click(force=True)
                set_state = "clicked"
        page.wait_for_timeout(3000)
        shot(page, "v20_13_after_set.png")
        banner = page.inner_text("body")
        info_banner = {
            "title_and_thumb": bool(re.search(r"title and thumbnail test has been set up", banner, re.I)),
            "title_only": bool(re.search(r"A title test has been set up", banner, re.I)),
            "save_or_publish": bool(re.search(r"Save or publish to start", banner, re.I)),
        }
        page.keyboard.press("Escape")
        page.wait_for_timeout(500)
        saved = save(page)
        shot(page, "v20_14_after_save.png")
        result["ab"] = {
            "uploads": uploads,
            "vals": vals,
            "ready": ready,
            "set": set_state,
            "banner": info_banner,
            "saved": saved,
        }

        log("v20 visibility")
        goto_edit(page)
        page.evaluate(
            """() => {
          const walk=(r,d=0)=>{
            if(!r||d>55)return false;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim();
              if (t==='Visibility' || /^Scheduled$/i.test(t)) { el.click(); return t; }
              if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
            }
            return false;
          }; return walk(document);
        }"""
        )
        page.wait_for_timeout(1000)
        page.evaluate(
            """() => {
          const walk=(r,d=0)=>{
            if(!r||d>55)return false;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim();
              if (/15 Oct 2026/.test(t) || t==='Schedule') {
                const rect=el.getBoundingClientRect();
                if (rect.y>100 && rect.width>20) { el.click(); return t; }
              }
              if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
            }
            return false;
          }; return walk(document);
        }"""
        )
        page.wait_for_timeout(1200)
        shot(page, "v20_20_visibility.png")
        vt = page.inner_text("body")
        result["schedule"] = {
            "has_15": bool(re.search(r"15\s*(Oct|October)\s*2026", vt, re.I)),
            "has_1800": bool(re.search(r"18:00", vt)),
            "has_30": bool(re.search(r"30\s*(Sept|Sep|September)\s*2026", vt, re.I)),
        }

        log("v20 content")
        page.goto(
            f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload",
            wait_until="domcontentloaded",
            timeout=90000,
        )
        page.wait_for_timeout(4000)
        shot(page, "v20_21_content.png")
        ct = page.inner_text("body")
        result["content_15"] = bool(re.search(r"15\s*(Oct|October)\s*2026", ct, re.I))
        result["content_30"] = bool(re.search(r"30\s*(Sept|Sep|September)\s*2026", ct, re.I))
        result["content_ab"] = bool(
            re.search(r"What's Really Inside an Atom\?[\s\S]{0,300}A/B test", ct, re.I)
        )

        log("v20 end screen")
        goto_edit(page)
        page.evaluate(
            """() => {
          const walk=(r,d=0)=>{
            if(!r||d>55)return false;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if ((el.innerText||'').trim()==='End screen') { el.click(); return true; }
              if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
            }
            return false;
          }; return walk(document);
        }"""
        )
        page.wait_for_timeout(3000)
        for _ in range(3):
            try:
                page.get_by_role("button", name=re.compile(r"OK, got it", re.I)).first.click(timeout=500)
            except Exception:
                pass
        page.evaluate(
            """() => {
          const walk=(r,d=0)=>{
            if(!r||d>55)return false;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if ((el.innerText||'').trim()==='1 video, 1 subscribe') { el.click(); return true; }
              if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
            }
            return false;
          }; return walk(document);
        }"""
        )
        page.wait_for_timeout(2000)
        page.evaluate(
            """() => {
          const walk=(r,d=0)=>{
            if(!r||d>55)return false;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim();
              if (t==='Best for viewer' || t==='Most recent upload' || /Video:\\s*Best for viewer/i.test(t)) {
                el.click(); return t;
              }
              if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
            }
            return false;
          }; return walk(document);
        }"""
        )
        page.wait_for_timeout(600)
        page.evaluate(
            """() => {
          const walk=(r,d=0)=>{
            if(!r||d>55)return false;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if ((el.innerText||'').trim()==='Specific video') { el.click(); return true; }
              if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
            }
            return false;
          }; return walk(document);
        }"""
        )
        page.wait_for_timeout(900)
        page.evaluate(
            """() => {
          const cands=[];
          const walk=(r,d=0)=>{
            if(!r||d>55)return;
            for (const inp of (r.querySelectorAll?r.querySelectorAll('input'):[])) {
              const rect=inp.getBoundingClientRect();
              if (rect.y>80 && rect.width>40) cands.push(inp);
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
            }
          }; walk(document);
          if (cands.length) { cands[cands.length-1].focus(); cands[cands.length-1].click(); }
        }"""
        )
        page.keyboard.press("Meta+a")
        page.keyboard.type("How Did We Discover the Periodic Table", delay=12)
        page.wait_for_timeout(2200)
        page.evaluate(
            """() => {
          const walk=(r,d=0)=>{
            if(!r||d>55)return false;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim();
              if (/How Did We Discover the Periodic Table/i.test(t) && t.length<90) { el.click(); return true; }
              if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
            }
            return false;
          }; return walk(document);
        }"""
        )
        page.wait_for_timeout(1000)
        shot(page, "v20_30_end.png")
        try:
            btn = page.get_by_role("button", name=re.compile(r"^SAVE$|^Save$", re.I))
            if btn.count() and btn.first.is_enabled():
                btn.first.click(force=True)
                page.wait_for_timeout(4000)
        except Exception:
            page.evaluate(
                """() => {
              const walk=(r,d=0)=>{
                if(!r||d>55)return false;
                for (const el of (r.querySelectorAll?r.querySelectorAll('button,ytcp-button'):[])) {
                  const t=(el.innerText||'').trim();
                  if (t==='SAVE'||t==='Save') { el.click(); return true; }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                  if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
                }
                return false;
              }; return walk(document);
            }"""
            )
            page.wait_for_timeout(4000)
        shot(page, "v20_31_end_saved.png")
        et = page.inner_text("body")
        result["end"] = {
            "has_002": bool(re.search(r"Periodic Table|AL_-qlWko_g", et, re.I)),
            "has_subscribe": bool(re.search(r"Subscribe", et, re.I)),
            "best_for_viewer": bool(re.search(r"Best for viewer", et, re.I)),
            "error": bool(re.search(r"problem in processing|couldn't be saved", et, re.I)),
        }
        result["pin"] = {
            "ok": False,
            "reason": "deferred_while_private_scheduled",
            "note": "Pin on launch 15 Oct 2026",
        }

    dump("PHONE_UAT_V20_RESULT.json", result)
    log(f"DONE {json.dumps({k: result.get(k) for k in ('kids_no','ai_yes','schedule','content_15','content_ab','ab','end')}, default=str)}")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
