#!/usr/bin/env python3
"""Minimal: set Level Key stage 4, Save, reload verify; probe GCSE exam names."""
from __future__ import annotations

import importlib.util
import json
import shutil
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO = Path("/Users/benjaminoats/YouTube/History Of Science")
U004 = (
    REPO
    / "02_Video-Projects/004_Whats-Really-Inside-An-Atom/11_Upload-Package/Schedule"
    / "_upload_hos_004_shorts_v01.py"
)
EV = (
    REPO
    / "02_Video-Projects/004_Whats-Really-Inside-An-Atom/11_Upload-Package/Schedule"
    / "evidence_2026-09-30_studio_fixes"
)
ART = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts"
VID = "29bpGAI0wb8"


def load_u():
    spec = importlib.util.spec_from_file_location("u", U004)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def show_more(page):
    for _ in range(8):
        ok = page.evaluate(
            """() => {
              const walk=(r,d=0)=>{
                if(!r||d>50) return false;
                for (const el of (r.querySelectorAll?r.querySelectorAll('button,ytcp-button,[role=button]'):[])) {
                  if ((el.innerText||'').trim()==='Show more') { el.click(); return true; }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                  if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
                return false;
              }; return walk(document);
            }"""
        )
        if not ok:
            break
        page.wait_for_timeout(400)


def selects(page):
    return page.evaluate(
        """()=>{
          const out=[];
          const walk=(r,d=0)=>{
            if(!r||d>50) return;
            for (const el of (r.querySelectorAll
              ? r.querySelectorAll('ytcp-dropdown-trigger,ytcp-text-dropdown-trigger,[role=combobox]')
              : [])) {
              const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
              if (/language|Type|Level|Exam|Academic|Education/i.test(t) && t.length<160)
                out.push(t.slice(0,160));
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document); return [...new Set(out)];
        }"""
    )


def scroll_label(page, label):
    page.evaluate(
        """(label)=>{
          const walk=(r,d=0)=>{
            if(!r||d>50) return false;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if ((el.innerText||'').trim()===label) { el.scrollIntoView({block:'center'}); return true; }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
            return false;
          }; return walk(document);
        }""",
        label,
    )
    page.wait_for_timeout(400)


def open_value(page, label, value):
    scroll_label(page, label)
    return page.evaluate(
        """(args)=>{
          const label=args[0], want=args[1];
          let lab=null;
          const walk=(r,d=0)=>{
            if(!r||d>50||lab) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const own=[...el.childNodes].filter(n=>n.nodeType===3).map(n=>n.textContent.trim()).join(' ').trim();
              if (own!==label && (el.innerText||'').trim()!==label) continue;
              const b=el.getBoundingClientRect();
              if (b.width>8&&b.height>8&&b.y>40&&b.y<1050) lab={el,x:b.x,y:b.y};
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document);
          if(!lab) return {error:'no_lab'};
          lab.el.scrollIntoView({block:'center'});
          let bestEl=null, best=null;
          const walk2=(r,d=0)=>{
            if(!r||d>50) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('span,yt-formatted-string,div'):[])) {
              const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
              if (t!==want && !t.includes(want)) continue;
              if (t.length>90) continue;
              const b=el.getBoundingClientRect();
              if (b.width<15||b.height<10||b.height>50) continue;
              if (b.y<lab.y-5||b.y>lab.y+130) continue;
              if (b.x<lab.x-40) continue;
              const score=Math.abs(b.y-(lab.y+22));
              if (!best||score<best.score) { best={t,y:b.y}; bestEl=el; }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk2(el.shadowRoot,d+1);
          }; walk2(document);
          if(!bestEl) return {error:'no_value'};
          bestEl.click();
          return {ok:true, clicked:best};
        }""",
        [label, value],
    )


def click_exact(page, want):
    return page.evaluate(
        """(want)=>{
          let hit=null;
          const walk=(r,d=0)=>{
            if(!r||d>55||hit) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('tp-yt-paper-item,[role=option]'):[])) {
              const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
              if (t!==want) continue;
              el.scrollIntoView({block:'nearest'}); el.click();
              hit={t,y:el.getBoundingClientRect().y};
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document); return hit;
        }""",
        want,
    )


def list_opts(page):
    return page.evaluate(
        """()=>{
          const out=[]; const seen=new Set();
          const walk=(r,d=0)=>{
            if(!r||d>55) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('tp-yt-paper-item,[role=option]'):[])) {
              const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
              if (!t||seen.has(t)) continue;
              const b=el.getBoundingClientRect();
              if (b.width<30||b.height<10||b.y<-20||b.y>1200) continue;
              seen.add(t); out.push({t,y:b.y});
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document); return out;
        }"""
    )


def main():
    u = load_u()
    out = {}
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9460")
        page = browser.contexts[0].new_page()
        page.set_viewport_size({"width": 1400, "height": 900})
        try:
            page.goto(
                f"https://studio.youtube.com/video/{VID}/edit",
                wait_until="domcontentloaded",
                timeout=120000,
            )
            page.wait_for_timeout(4000)
            u.dismiss(page)
            show_more(page)
            out["before"] = selects(page)

            # Set Level KS4 only
            cur = "None"
            for s in out["before"]:
                if s.startswith("Level"):
                    cur = s.replace("Level", "").strip() or cur
            opened = open_value(page, "Level", cur)
            page.wait_for_timeout(1100)
            # scroll list if needed
            opts = list_opts(page)
            if not any(o["t"] == "Key stage 4" for o in opts):
                # wheel
                for _ in range(15):
                    page.mouse.wheel(0, 200)
                    page.wait_for_timeout(120)
                    opts = list_opts(page)
                    if any(o["t"] == "Key stage 4" for o in opts):
                        break
            hit = click_exact(page, "Key stage 4")
            out["level_open"] = opened
            out["level_pick"] = hit
            out["level_opts_sample"] = [o["t"] for o in opts[:40]]
            page.wait_for_timeout(800)
            out["selects_after_pick"] = selects(page)
            page.screenshot(path=str(EV / "fri_manual_level_after_pick.png"))
            save = u.page_save(page)
            out["level_save"] = save
            page.wait_for_timeout(3000)
            out["selects_after_save"] = selects(page)
            page.screenshot(path=str(EV / "fri_manual_level.png"))
            shutil.copy2(EV / "fri_manual_level.png", ART / "BEN_1445FIX_fri_manual_level.png")

            # Hard reload verify
            page.goto(
                f"https://studio.youtube.com/video/{VID}/edit",
                wait_until="domcontentloaded",
                timeout=120000,
            )
            page.wait_for_timeout(4500)
            u.dismiss(page)
            show_more(page)
            for _ in range(14):
                page.mouse.wheel(0, 650)
                page.wait_for_timeout(50)
            out["selects_after_reload"] = selects(page)
            page.screenshot(path=str(EV / "fri_manual_level_after_reload.png"))
            shutil.copy2(
                EV / "fri_manual_level_after_reload.png",
                ART / "BEN_1445FIX_fri_manual_level_after_reload.png",
            )

            # Exam probes
            scroll_label(page, "Exam, course or standard")
            exam_trials = {}
            for q in ["GCSE Chemistry", "GCSE", "AQA", "OCR", "Edexcel", "Chemistry"]:
                page.evaluate(
                    """()=>{
                      const walk=(r,d=0)=>{
                        if(!r||d>50) return false;
                        for (const el of (r.querySelectorAll?r.querySelectorAll('input'):[])) {
                          const aria=(el.getAttribute('aria-label')||'');
                          if (/Exam, course or standard/i.test(aria)) {
                            el.scrollIntoView({block:'center'}); el.click(); el.focus(); return true;
                          }
                        }
                        for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                          if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
                        return false;
                      }; return walk(document);
                    }"""
                )
                page.wait_for_timeout(300)
                page.mouse.click(620, 530, click_count=3)
                page.keyboard.press("Backspace")
                page.wait_for_timeout(200)
                page.keyboard.type(q, delay=45)
                page.wait_for_timeout(1800)
                opts = list_opts(page)
                exam_trials[q] = [{"t": o["t"], "y": o["y"]} for o in opts]
                page.keyboard.press("Escape")
                page.wait_for_timeout(300)
            out["exam_trials"] = exam_trials
            # If GCSE Chemistry exact exists, pick+save
            if any(o["t"] == "GCSE Chemistry" for o in exam_trials.get("GCSE Chemistry") or []):
                page.evaluate(
                    """()=>{
                      const walk=(r,d=0)=>{
                        if(!r||d>50) return false;
                        for (const el of (r.querySelectorAll?r.querySelectorAll('input'):[])) {
                          const aria=(el.getAttribute('aria-label')||'');
                          if (/Exam, course or standard/i.test(aria)) { el.click(); el.focus(); return true; }
                        }
                        for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                          if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
                        return false;
                      }; return walk(document);
                    }"""
                )
                page.mouse.click(620, 530, click_count=3)
                page.keyboard.press("Backspace")
                page.keyboard.type("GCSE Chemistry", delay=45)
                page.wait_for_timeout(1800)
                out["exam_pick"] = click_exact(page, "GCSE Chemistry")
                page.wait_for_timeout(500)
                out["exam_save"] = u.page_save(page)
                page.wait_for_timeout(2500)
                page.screenshot(path=str(EV / "fri_manual_exam.png"))
                shutil.copy2(EV / "fri_manual_exam.png", ART / "BEN_1445FIX_fri_manual_exam.png")

            # Final
            page.goto(
                f"https://studio.youtube.com/video/{VID}/edit",
                wait_until="domcontentloaded",
                timeout=120000,
            )
            page.wait_for_timeout(4000)
            u.dismiss(page)
            show_more(page)
            for _ in range(14):
                page.mouse.wheel(0, 650)
                page.wait_for_timeout(50)
            out["final_selects"] = selects(page)
            page.screenshot(path=str(EV / "fri_manual_99_final.png"))
            shutil.copy2(EV / "fri_manual_99_final.png", ART / "BEN_1445FIX_fri_manual_99_final.png")
            scroll_label(page, "Academic system")
            page.screenshot(path=str(EV / "fri_manual_99_education.png"))
            shutil.copy2(
                EV / "fri_manual_99_education.png",
                ART / "BEN_1445FIX_fri_manual_99_education.png",
            )

            # Update probe
            probe_path = EV / "DROPDOWN_PROBE.json"
            old = {}
            if probe_path.exists():
                try:
                    old = json.loads(probe_path.read_text())
                except Exception:
                    pass
            old["v09_level_exam"] = out
            for q, opts in exam_trials.items():
                old[f"Exam probe typed={q}"] = {"want": "GCSE Chemistry", "options": opts}
            probe_path.write_text(json.dumps(old, indent=2, default=str))
            shutil.copy2(probe_path, ART / "BEN_1445FIX_DROPDOWN_PROBE.json")

            (EV / "FRI_MANUAL_RESULT.json").write_text(json.dumps(out, indent=2, default=str))
            shutil.copy2(EV / "FRI_MANUAL_RESULT.json", ART / "BEN_1445FIX_FRI_MANUAL_RESULT.json")
            print(json.dumps({
                "before": out["before"],
                "after_pick": out["selects_after_pick"],
                "after_save": out["selects_after_save"],
                "after_reload": out["selects_after_reload"],
                "final": out["final_selects"],
                "level_pick": out["level_pick"],
                "level_save": out["level_save"],
                "exam_trial_keys": {k: [o["t"] for o in v[:12]] for k,v in exam_trials.items()},
            }, indent=2))
        finally:
            page.close()


if __name__ == "__main__":
    main()
