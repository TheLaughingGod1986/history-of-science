#!/usr/bin/env python3
"""Re-read Fri education fields + harvest full exam list under England/KS4."""
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


def chips(page):
    return page.evaluate(
        """()=>{
          const out=[];
          const walk=(r,d=0)=>{
            if(!r||d>50) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('ytcp-chip,yt-chip-cloud-chip'):[])) {
              const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
              if (t && t.length<90) out.push(t);
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document); return [...new Set(out)];
        }"""
    )


def paid_places(page):
    return page.evaluate(
        """()=>{
          const paid=[];
          const state={places:null};
          const walk=(r,d=0)=>{
            if(!r||d>50) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('tp-yt-paper-radio-button,[role=radio]'):[])) {
              const lab=(el.getAttribute('aria-label')||el.innerText||'').replace(/\\s+/g,' ').trim();
              if (/paid promotion/i.test(lab))
                paid.push({lab:lab.slice(0,100), checked:el.getAttribute('aria-checked')==='true'});
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('[role=checkbox],tp-yt-paper-checkbox'):[])) {
              const lab=(el.getAttribute('aria-label')||'');
              if (/Allow automatic places/i.test(lab))
                state.places={lab, checked:el.getAttribute('aria-checked')==='true'};
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document); return {paid, places:state.places};
        }"""
    )


def open_value(page, label, value):
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


def harvest(page):
    return page.evaluate(
        """()=>{
          let box=null;
          const find=(r,d=0)=>{
            if(!r||d>55||box) return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('[role=listbox],tp-yt-paper-listbox'):[])) {
              const b=el.getBoundingClientRect();
              if (b.height>40&&b.width>80) box=el;
            }
            if (!box) {
              for (const el of (r.querySelectorAll?r.querySelectorAll('tp-yt-paper-item,[role=option]'):[])) {
                let p=el.parentElement;
                for (let i=0;i<10&&p;i++) {
                  if (p.scrollHeight>p.clientHeight+40) { box=p; break; }
                  p=p.parentElement;
                }
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) find(el.shadowRoot,d+1);
          }; find(document);
          const all=[]; const seen=new Set();
          const note=()=>{
            const walk=(r,d=0)=>{
              if(!r||d>40) return;
              for (const el of (r.querySelectorAll?r.querySelectorAll('tp-yt-paper-item,[role=option]'):[])) {
                const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
                if (!t||seen.has(t)) continue;
                const b=el.getBoundingClientRect();
                if (b.width<30||b.height<10) continue;
                seen.add(t); all.push({t,y:b.y});
              }
              for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                if (el.shadowRoot) walk(el.shadowRoot,d+1);
            }; walk(document);
          };
          if (!box) { note(); return {n:all.length, options:all, error:'no_box'}; }
          box.scrollTop=0; note();
          for (let i=0;i<100;i++) {
            const before=box.scrollTop;
            box.scrollTop=before+Math.max(100, Math.floor(box.clientHeight*0.7));
            note();
            if (box.scrollTop===before) break;
          }
          box.scrollTop=box.scrollHeight; note();
          return {n:all.length, options:all};
        }"""
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
              const b=el.getBoundingClientRect();
              hit={t,y:b.y,x:b.x};
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
          }; walk(document); return hit;
        }""",
        want,
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
            # scroll to education
            for _ in range(12):
                page.mouse.wheel(0, 700)
                page.wait_for_timeout(80)
            page.wait_for_timeout(500)
            out["selects"] = selects(page)
            out["tags"] = chips(page)
            # scroll paid
            for _ in range(8):
                page.mouse.wheel(0, 700)
                page.wait_for_timeout(60)
            out.update(paid_places(page))
            page.screenshot(path=str(EV / "fri_manual_99_reread.png"))
            shutil.copy2(EV / "fri_manual_99_reread.png", ART / "BEN_1445FIX_fri_manual_99_reread.png")

            # Ensure Level Key stage 4 again if None
            page.evaluate(
                """()=>{
                  const walk=(r,d=0)=>{
                    if(!r||d>50) return false;
                    for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                      if ((el.innerText||'').trim()==='Level') { el.scrollIntoView({block:'center'}); return true; }
                    }
                    for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                      if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
                    return false;
                  }; return walk(document);
                }"""
            )
            page.wait_for_timeout(400)
            sel = " | ".join(out["selects"])
            if "Key stage 4" not in sel:
                open_value(page, "Level", "None")
                page.wait_for_timeout(1000)
                # harvest levels
                out["level_options"] = harvest(page)
                hit = click_exact(page, "Key stage 4")
                out["level_pick"] = hit
                page.wait_for_timeout(500)
                u.page_save(page)
                page.wait_for_timeout(2500)
                page.screenshot(path=str(EV / "fri_manual_level.png"))
                shutil.copy2(EV / "fri_manual_level.png", ART / "BEN_1445FIX_fri_manual_level.png")

            # Exam harvest: click input, clear, don't type — scroll all
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
            page.wait_for_timeout(800)
            # clear any filter without Meta+a (selects page)
            page.keyboard.press("Control+a")
            page.keyboard.press("Backspace")
            page.wait_for_timeout(500)
            # click again to open
            page.evaluate(
                """()=>{
                  const walk=(r,d=0)=>{
                    if(!r||d>50) return false;
                    for (const el of (r.querySelectorAll?r.querySelectorAll('input'):[])) {
                      const aria=(el.getAttribute('aria-label')||'');
                      if (/Exam, course or standard/i.test(aria)) { el.click(); return true; }
                    }
                    for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                      if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
                    return false;
                  }; return walk(document);
                }"""
            )
            page.wait_for_timeout(1000)
            out["exam_all"] = harvest(page)
            page.screenshot(path=str(EV / "fri_probe_exam_full.png"))
            opts = [o["t"] for o in (out["exam_all"].get("options") or [])]
            out["exam_gcse_like"] = [t for t in opts if "GCSE" in t.upper() or "Chemistry" in t]
            # pick GCSE Chemistry if present
            want = "GCSE Chemistry"
            if want in opts:
                # scroll to and click
                # re-harvest with click
                hit = None
                # use scrollTop find from harvest's box again via find_and_click style
                hit = page.evaluate(
                    """(want)=>{
                      let box=null;
                      const find=(r,d=0)=>{
                        if(!r||d>55||box) return;
                        for (const el of (r.querySelectorAll?r.querySelectorAll('[role=listbox],tp-yt-paper-listbox'):[])) {
                          const b=el.getBoundingClientRect();
                          if (b.height>40&&b.width>80) box=el;
                        }
                        for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                          if (el.shadowRoot) find(el.shadowRoot,d+1);
                      }; find(document);
                      const clickWant=()=>{
                        let hit=null;
                        const walk=(r,d=0)=>{
                          if(!r||d>40||hit) return;
                          for (const el of (r.querySelectorAll?r.querySelectorAll('tp-yt-paper-item,[role=option]'):[])) {
                            const t=(el.innerText||'').replace(/\\s+/g,' ').trim();
                            if (t!==want) continue;
                            el.scrollIntoView({block:'nearest'}); el.click();
                            hit={t,y:el.getBoundingClientRect().y};
                          }
                          for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                            if (el.shadowRoot) walk(el.shadowRoot,d+1);
                        }; walk(document); return hit;
                      };
                      if (!box) return clickWant();
                      box.scrollTop=0;
                      let hit=clickWant();
                      if (hit) return hit;
                      for (let i=0;i<120;i++) {
                        const before=box.scrollTop;
                        box.scrollTop=before+120;
                        hit=clickWant();
                        if (hit) return hit;
                        if (box.scrollTop===before) break;
                      }
                      return null;
                    }""",
                    want,
                )
                out["exam_pick"] = hit
                if hit:
                    page.wait_for_timeout(500)
                    u.page_save(page)
                    page.wait_for_timeout(2500)
                    page.screenshot(path=str(EV / "fri_manual_exam.png"))
                    shutil.copy2(EV / "fri_manual_exam.png", ART / "BEN_1445FIX_fri_manual_exam.png")

            # final reread
            page.reload(wait_until="domcontentloaded")
            page.wait_for_timeout(4000)
            u.dismiss(page)
            show_more(page)
            for _ in range(14):
                page.mouse.wheel(0, 700)
                page.wait_for_timeout(60)
            out["final_selects"] = selects(page)
            out["final_tags"] = chips(page)
            out["final_pp"] = paid_places(page)
            page.screenshot(path=str(EV / "fri_manual_99_final.png"))
            shutil.copy2(EV / "fri_manual_99_final.png", ART / "BEN_1445FIX_fri_manual_99_final.png")
            # education closeup
            page.evaluate(
                """()=>{
                  const walk=(r,d=0)=>{
                    if(!r||d>50) return false;
                    for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                      if ((el.innerText||'').trim()==='Academic system') {
                        el.scrollIntoView({block:'center'}); return true;
                      }
                    }
                    for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                      if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
                    return false;
                  }; return walk(document);
                }"""
            )
            page.wait_for_timeout(400)
            page.screenshot(path=str(EV / "fri_manual_99_education.png"))
            shutil.copy2(
                EV / "fri_manual_99_education.png",
                ART / "BEN_1445FIX_fri_manual_99_education.png",
            )

            path = EV / "DROPDOWN_PROBE.json"
            old = {}
            if path.exists():
                try:
                    old = json.loads(path.read_text())
                except Exception:
                    pass
            old["v08_reread"] = {
                "selects": out.get("selects"),
                "final_selects": out.get("final_selects"),
                "exam_n": (out.get("exam_all") or {}).get("n"),
                "exam_gcse_like": out.get("exam_gcse_like"),
                "exam_pick": out.get("exam_pick"),
                "level_pick": out.get("level_pick"),
                "tags": out.get("final_tags") or out.get("tags"),
                "paid_places": out.get("final_pp") or {"paid": out.get("paid"), "places": out.get("places")},
            }
            # also store full exam list texts
            old["Exam full list"] = {
                "want": "GCSE Chemistry",
                "options": (out.get("exam_all") or {}).get("options") or [],
            }
            path.write_text(json.dumps(old, indent=2, default=str))
            shutil.copy2(path, ART / "BEN_1445FIX_DROPDOWN_PROBE.json")

            summary = {
                "selects_before_fix": out.get("selects"),
                "final_selects": out.get("final_selects"),
                "exam_n": (out.get("exam_all") or {}).get("n"),
                "exam_gcse_like": out.get("exam_gcse_like"),
                "exam_pick": out.get("exam_pick"),
                "level_pick": out.get("level_pick"),
                "tags": out.get("final_tags"),
                "paid_places": out.get("final_pp"),
            }
            (EV / "FRI_MANUAL_RESULT.json").write_text(json.dumps(summary, indent=2, default=str))
            shutil.copy2(EV / "FRI_MANUAL_RESULT.json", ART / "BEN_1445FIX_FRI_MANUAL_RESULT.json")
            print(json.dumps(summary, indent=2, default=str)[:4000])
        finally:
            page.close()


if __name__ == "__main__":
    main()
