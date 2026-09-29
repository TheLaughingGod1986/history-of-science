#!/usr/bin/env python3
"""HOS 004 FINISH Studio (Ben 29 Sep 20:00 finish order).

CHANNEL: @HistoryOfScienceYT UCXp7HkBIl1LgaznXuZHJyRg only.
Video: GHZDsiH7L7A — do NOT re-upload / Replace / delete / publish-now / Premiere.

1. Visibility: confirm 15 Oct 2026 18:00 UK, Premiere OFF, title, thumb A → screenshot → leave alone
2. Test & Compare: Title+thumb×3 if offered, else Thumbnail only A/B/C
3. Captions / end screen (002+Subscribe) / pin / description
4. Audience: after each save confirm not made for kids
"""
from __future__ import annotations

import json
import re
import shutil
import urllib.request
from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright

PORT = 9460
VIDEO_ID = "GHZDsiH7L7A"
CHANNEL = "UCXp7HkBIl1LgaznXuZHJyRg"
RELATED_002 = "AL_-qlWko_g"
RELATED_TITLE = "How Did We Discover the Periodic Table"
PROJ = Path(__file__).resolve().parents[2]
PKG = PROJ / "11_Upload-Package"
EV = PKG / "Schedule/evidence_2026-09-29_studio"
ART = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts/hos004_studio_phone_uat"
THUMB_A = PROJ / "08_Thumbnail/Selected/hos_004_thumb_A_atom_live_v04.jpg"
THUMB_B = PROJ / "08_Thumbnail/Selected/hos_004_thumb_B_cut_gold_live_v04.jpg"
THUMB_C = PROJ / "08_Thumbnail/Selected/hos_004_thumb_C_hidden_number_live_v06.jpg"
CAPTIONS = PKG / "Captions/hos_004_full_v02.en.srt"
DESC = PKG / "Descriptions/atom_long_description_v01.txt"
CHAPTERS = PKG / "Chapters/atom_long_chapters_v01.txt"
PIN = PKG / "Pinned-Comments/atom_long_pinned-comment_v01.txt"
TITLE_MAIN = "What's Really Inside an Atom?"
TITLES = [
    "What's Really Inside an Atom?",
    "Why Is the Periodic Table in This Order?",
    "How Small Can You Cut Gold?",
]
THUMBS = [THUMB_A, THUMB_C, THUMB_B]  # A · C v06 · B v04


def log(m: str) -> None:
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    line = f"{datetime.now().isoformat(timespec='seconds')} {m}"
    print(line, flush=True)
    with (EV / "finish_v01.log").open("a") as f:
        f.write(line + "\n")


def dump(n: str, o) -> None:
    text = json.dumps(o, indent=2) + "\n"
    (EV / n).write_text(text)
    (ART / n).write_text(text)


def shot(page, n: str) -> Path:
    p = EV / n
    page.screenshot(path=str(p), full_page=False)
    (ART / n).write_bytes(p.read_bytes())
    return p


def dismiss(page) -> None:
    for _ in range(3):
        page.keyboard.press("Escape")
        page.wait_for_timeout(100)
        try:
            page.get_by_role(
                "button",
                name=re.compile(r"^(OK, got it|Got it|Close|Dismiss|Not now)$", re.I),
            ).first.click(timeout=300)
        except Exception:
            pass


def click_text(page, pattern: str, y_min: int = 40, max_len: int = 80) -> str | None:
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


def save_details(page) -> bool:
    try:
        btn = page.get_by_role("button", name=re.compile(r"^Save$", re.I))
        if btn.count() and btn.first.is_enabled():
            btn.first.click(force=True, timeout=8000)
            page.wait_for_timeout(4500)
            return True
    except Exception:
        pass
    return bool(click_text(page, r"^Save$", y_min=0, max_len=10))


def goto_edit(page) -> None:
    page.goto(
        f"https://studio.youtube.com/video/{VIDEO_ID}/edit",
        wait_until="domcontentloaded",
        timeout=90000,
    )
    page.wait_for_timeout(5000)
    dismiss(page)


def channel_check(page) -> dict:
    page.goto(
        f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload",
        wait_until="domcontentloaded",
        timeout=90000,
    )
    page.wait_for_timeout(4000)
    dismiss(page)
    shot(page, "finish_v01_00_channel.png")
    t = page.inner_text("body")
    ok = (
        ("History of Science" in t or "HistoryOfScience" in t)
        and "Orbit With Ben" not in t
        and "OpptiAI" not in t
    )
    return {
        "ok": ok,
        "has_orbit": "Orbit With Ben" in t,
        "has_oppti": "OpptiAI" in t,
        "snip": t[:400],
    }


def audience_state(page) -> dict:
    for _ in range(20):
        t = page.inner_text("body")
        if re.search(r"Audience|Made for Kids", t, re.I):
            break
        page.mouse.wheel(0, 500)
        page.wait_for_timeout(100)
    return page.evaluate(
        """() => {
          let audY=null;
          const find=(r,d=0)=>{
            if(!r||d>55)return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim();
              if (/^Audience$/i.test(t) || /Made for Kids/i.test(t) && t.length<40) {
                const rect=el.getBoundingClientRect();
                if (rect.y>80) { audY=rect.y; el.scrollIntoView({block:'center'}); }
              }
              if (el.shadowRoot) find(el.shadowRoot,d+1);
            }
          }; find(document);
          const radios=[];
          const walk=(r,d=0)=>{
            if(!r||d>55)return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('[role=radio],input[type=radio]'):[])) {
              const rect=el.getBoundingClientRect();
              if (audY!=null && (rect.y<audY-20 || rect.y>audY+600)) continue;
              const t=((el.getAttribute('aria-label')||'')+' '+(el.innerText||'')+
                ' '+((el.closest&&el.closest('tp-yt-paper-radio-button,ytcp-radio,label')||{}).innerText||'')
              ).trim().slice(0,120);
              if (!/Kids|kids|Audience/i.test(t) && audY==null) continue;
              radios.push({
                t, checked: el.getAttribute('aria-checked')==='true' || el.checked===true, y:rect.y
              });
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
            }
          }; walk(document);
          const body=(document.body&&document.body.innerText)||'';
          const set_to_not=/set to not Made for Kids|not 'Made for Kids'|not Made for Kids/i.test(body);
          const set_to_yes=/set to Made for Kids/i.test(body) && !set_to_not;
          const no_checked=radios.some(r=>/No,.*not/i.test(r.t)&&r.checked);
          const yes_checked=radios.some(r=>/Yes,.*Made for Kids/i.test(r.t)&&r.checked);
          return {
            audY, radios, set_to_not, set_to_yes,
            no_checked, yes_checked,
            ok_not_kids: no_checked || (set_to_not && !yes_checked),
            made_for_kids: yes_checked || set_to_yes
          };
        }"""
    )


def premiere_state(page) -> dict:
    return page.evaluate(
        """() => {
          const out={found:false, checked:null, labels:[]};
          const walk=(r,d=0)=>{
            if(!r||d>55)return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('tp-yt-paper-checkbox,ytcp-checkbox-lit,paper-checkbox,input,[role=checkbox],*'):[])) {
              const t=((el.innerText||'')+' '+(el.getAttribute('aria-label')||'')).trim();
              if (!/Set as (?:instant )?Premiere/i.test(t)) continue;
              const rect=el.getBoundingClientRect();
              if (rect.width<8 || rect.y<80) continue;
              out.found=true;
              out.labels.push(t.slice(0,60));
              const tag=(el.tagName||'').toLowerCase();
              const role=el.getAttribute('role')||'';
              if ((tag==='input'&&el.type==='checkbox')||role==='checkbox'||role==='switch'
                  || /checkbox/i.test(tag)) {
                const ac=el.getAttribute('aria-checked');
                if (ac!=null) out.checked = ac==='true';
                else if (typeof el.checked==='boolean') out.checked = el.checked;
                else out.checked = el.hasAttribute('checked');
                out.near=t.slice(0,120);
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
            }
          }; walk(document);
          return out;
        }"""
    )


def open_visibility(page) -> dict:
    info = {}
    # Prefer pencil "edit video visibility status"
    pencil = page.evaluate(
        """() => {
          const cands=[];
          const walk=(r,d=0)=>{
            if(!r||d>55)return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('button,ytcp-icon-button,[role=button],*'):[])) {
              const aria=(el.getAttribute('aria-label')||'');
              if (!/edit video visibility|visibility status|Edit visibility/i.test(aria)
                  && !/^edit$/i.test((el.innerText||'').trim())) continue;
              if (!/visibility/i.test(aria) && !/visibility/i.test((el.innerText||'')+((el.parentElement&&el.parentElement.innerText)||''))) {
                if (!/edit video visibility/i.test(aria)) continue;
              }
              const rect=el.getBoundingClientRect();
              if (rect.width<6||rect.y<80) continue;
              cands.push({x:rect.x+rect.width/2,y:rect.y+rect.height/2,aria:aria.slice(0,80)});
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
            }
          }; walk(document);
          return cands[0]||null;
        }"""
    )
    info["pencil"] = pencil
    if pencil:
        page.mouse.click(pencil["x"], pencil["y"])
        page.wait_for_timeout(1800)
    else:
        box = page.evaluate(
            """() => {
              const cands=[];
              const walk=(r,d=0)=>{
                if(!r||d>55)return;
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                  const t=(el.innerText||'').trim();
                  if (t==='Scheduled' || t==='Visibility' || t==='Schedule') {
                    const rect=el.getBoundingClientRect();
                    if (rect.x>700 && rect.y>150 && rect.width>20)
                      cands.push({x:rect.x+Math.min(40,rect.width/2),y:rect.y+rect.height/2,t});
                  }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                  if (el.shadowRoot) walk(el.shadowRoot,d+1);
                }
              }; walk(document);
              cands.sort((a,b)=>(a.t==='Scheduled'?0:1)-(b.t==='Scheduled'?0:1));
              return cands[0]||null;
            }"""
        )
        info["rail"] = box
        if box:
            page.mouse.click(box["x"], box["y"])
            page.wait_for_timeout(1500)
    return info


def uncheck_premiere_if_needed(page) -> dict:
    before = premiere_state(page)
    info = {"before": before}
    if before.get("checked") is True:
        click_text(page, r"Set as (?:instant )?Premiere", y_min=100, max_len=50)
        page.wait_for_timeout(600)
        info["clicked"] = True
    info["after"] = premiere_state(page)
    return info


def probe_visibility(page) -> dict:
    vt = page.inner_text("body")
    prem = premiere_state(page)
    return {
        "has_15": bool(re.search(r"15\s*(Oct|October)\s*2026", vt, re.I)),
        "has_1800": bool(re.search(r"18:00", vt)),
        "has_30": bool(re.search(r"30\s*(Sept|Sep|September)\s*2026", vt, re.I)),
        "premiere_checkbox": prem,
        "premiere_off": prem.get("checked") is False,
        "title_main": TITLE_MAIN in vt,
        "snip": vt[:1400],
    }


def upload_file_near(page, label_re: str, path: Path) -> dict:
    info = {"file": path.name}
    ups = page.evaluate(
        """(labelRe) => {
          const re=new RegExp(labelRe,'i');
          const out=[];
          const walk=(r,d=0)=>{
            if(!r||d>55)return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim();
              if (!re.test(t) || t.length>40) continue;
              const rect=el.getBoundingClientRect();
              if (rect.y>80 && rect.width>20)
                out.push({x:rect.x+rect.width/2,y:rect.y+rect.height/2,t});
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
            }
          }; walk(document); return out;
        }""",
        label_re,
    )
    info["ups"] = ups[:6]
    for u in ups[:4]:
        try:
            with page.expect_file_chooser(timeout=7000) as fc:
                page.mouse.click(u["x"], u["y"])
            fc.value.set_files(str(path))
            info["via"] = f"chooser:{u['t']}"
            info["ok"] = True
            page.wait_for_timeout(3500)
            return info
        except Exception as e:
            info.setdefault("errs", []).append(str(e)[:80])
            dismiss(page)
    loc = page.locator('input[type="file"]')
    for i in range(loc.count()):
        try:
            loc.nth(i).set_input_files(str(path))
            info["via"] = f"input[{i}]"
            info["ok"] = True
            page.wait_for_timeout(3500)
            return info
        except Exception:
            continue
    info["ok"] = False
    return info


def upload_thumb_a(page) -> dict:
    for _ in range(14):
        page.mouse.wheel(0, 350)
        page.wait_for_timeout(80)
        if re.search(r"thumbnail|Upload file", page.inner_text("body"), re.I):
            break
    info = upload_file_near(page, r"^(Upload|Upload file|Upload thumbnail)$", THUMB_A)
    info["saved"] = save_details(page)
    for _ in range(6):
        t = page.inner_text("body")
        if "trouble saving" in t.lower() or "retrying" in t.lower():
            try:
                page.get_by_text("Retry", exact=True).first.click(timeout=800)
            except Exception:
                pass
            page.wait_for_timeout(3500)
        else:
            break
    return info


def do_test_and_compare(page) -> dict:
    info = {
        "wanted": [
            {"title": TITLES[0], "thumb": THUMB_A.name},
            {"title": TITLES[1], "thumb": THUMB_C.name},
            {"title": TITLES[2], "thumb": THUMB_B.name},
        ]
    }
    goto_edit(page)
    # Scroll / open A/B
    for _ in range(10):
        page.mouse.wheel(0, 400)
        page.wait_for_timeout(80)
    shot(page, "finish_v01_20_ab_before.png")
    opened = click_text(page, r"^A/B Testing$|^Test and compare$|^Test & compare$", y_min=80, max_len=30)
    info["open_click"] = opened
    page.wait_for_timeout(2500)
    dismiss(page)
    body = page.inner_text("body")
    info["ineligible"] = bool(re.search(r"Ineligible", body, re.I))
    info["has_title_and_thumb"] = bool(re.search(r"Title and thumbnail", body, re.I))
    info["has_thumbnail_only"] = bool(re.search(r"Thumbnail only", body, re.I))
    shot(page, "finish_v01_21_ab_dialog.png")

    if info["ineligible"] and not info["has_title_and_thumb"] and not info["has_thumbnail_only"]:
        info["option_offered"] = "none_ineligible"
        info["ok"] = False
        info["note"] = "A/B Ineligible on scheduled/private — cannot arm T&C until eligible"
        page.keyboard.press("Escape")
        return info

    if info["has_title_and_thumb"]:
        info["option_offered"] = "Title and thumbnail"
        click_text(page, r"^Title and thumbnail$", y_min=60, max_len=40)
        page.wait_for_timeout(1000)
        shot(page, "finish_v01_22_title_thumb_mode.png")
        # Fill 3 pairs carefully — title then thumb
        for i, (title, thumb) in enumerate(zip(TITLES, THUMBS)):
            # Find title inputs / slots
            filled = page.evaluate(
                """({idx,title}) => {
                  const inputs=[];
                  const walk=(r,d=0)=>{
                    if(!r||d>55)return;
                    for (const inp of (r.querySelectorAll?r.querySelectorAll('input,textarea,#textbox'):[])) {
                      const rect=inp.getBoundingClientRect();
                      if (rect.y<80||rect.width<80||rect.height<20) continue;
                      const aria=((inp.getAttribute('aria-label')||'')+(inp.placeholder||'')).toLowerCase();
                      if (/title|variant|option/.test(aria) || inp.getAttribute('contenteditable')==='true'
                          || (inp.tagName==='DIV' && inp.id==='textbox')) {
                        inputs.push({y:rect.y,x:rect.x,w:rect.width,h:rect.height,aria});
                      }
                    }
                    for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                      if (el.shadowRoot) walk(el.shadowRoot,d+1);
                    }
                  }; walk(document);
                  inputs.sort((a,b)=>a.y-b.y||a.x-b.x);
                  if (!inputs[idx]) return {ok:false,n:inputs.length};
                  return {ok:true,n:inputs.length,y:inputs[idx].y,x:inputs[idx].x+20};
                }""",
                {"idx": i, "title": title},
            )
            info[f"title_slot_{i}"] = filled
            if filled and filled.get("ok"):
                page.mouse.click(filled["x"], filled["y"])
                page.wait_for_timeout(200)
                page.keyboard.press("Meta+a")
                page.keyboard.type(title, delay=12)
                page.wait_for_timeout(300)
            # Upload thumb for slot
            ups = page.evaluate(
                """(idx) => {
                  const outs=[];
                  const walk=(r,d=0)=>{
                    if(!r||d>55)return;
                    for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                      const t=(el.innerText||'').trim();
                      if (t!=='Upload' && t!=='Upload file' && t!=='Add thumbnail') continue;
                      const rect=el.getBoundingClientRect();
                      if (rect.y>100 && rect.width>20)
                        outs.push({x:rect.x+rect.width/2,y:rect.y+rect.height/2,t});
                    }
                    for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                      if (el.shadowRoot) walk(el.shadowRoot,d+1);
                    }
                  }; walk(document);
                  outs.sort((a,b)=>a.y-b.y||a.x-b.x);
                  return outs[idx]||outs[0]||null;
                }""",
                i,
            )
            info[f"thumb_slot_{i}"] = ups
            if ups:
                try:
                    with page.expect_file_chooser(timeout=7000) as fc:
                        page.mouse.click(ups["x"], ups["y"])
                    fc.value.set_files(str(thumb))
                    page.wait_for_timeout(2500)
                except Exception as e:
                    info[f"thumb_err_{i}"] = str(e)[:80]
            shot(page, f"finish_v01_23_pair_{i}.png")
        # Set test
        click_text(page, r"^Set test$|^Start test$|^Save$", y_min=40, max_len=20)
        page.wait_for_timeout(3000)
        shot(page, "finish_v01_24_ab_after_save.png")
    elif info["has_thumbnail_only"]:
        info["option_offered"] = "Thumbnail only"
        click_text(page, r"^Thumbnail only$", y_min=60, max_len=30)
        page.wait_for_timeout(1000)
        shot(page, "finish_v01_22_thumb_only_mode.png")
        for i, thumb in enumerate([THUMB_A, THUMB_B, THUMB_C]):
            ups = page.evaluate(
                """(idx) => {
                  const outs=[];
                  const walk=(r,d=0)=>{
                    if(!r||d>55)return;
                    for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                      const t=(el.innerText||'').trim();
                      if (t!=='Upload' && t!=='Upload file' && t!=='Add thumbnail') continue;
                      const rect=el.getBoundingClientRect();
                      if (rect.y>100 && rect.width>20)
                        outs.push({x:rect.x+rect.width/2,y:rect.y+rect.height/2,t});
                    }
                    for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                      if (el.shadowRoot) walk(el.shadowRoot,d+1);
                    }
                  }; walk(document);
                  outs.sort((a,b)=>a.y-b.y||a.x-b.x);
                  return outs[idx]||null;
                }""",
                i,
            )
            if ups:
                try:
                    with page.expect_file_chooser(timeout=7000) as fc:
                        page.mouse.click(ups["x"], ups["y"])
                    fc.value.set_files(str(thumb))
                    page.wait_for_timeout(2500)
                    info[f"thumb_only_{i}"] = thumb.name
                except Exception as e:
                    info[f"thumb_only_err_{i}"] = str(e)[:80]
            shot(page, f"finish_v01_23_thumb_only_{i}.png")
        click_text(page, r"^Set test$|^Start test$|^Save$", y_min=40, max_len=20)
        page.wait_for_timeout(3000)
        shot(page, "finish_v01_24_ab_after_save.png")
    else:
        info["option_offered"] = "unknown"
        info["ok"] = False
        page.keyboard.press("Escape")
        return info

    page.keyboard.press("Escape")
    page.wait_for_timeout(800)
    # Verify main title + thumb A still
    goto_edit(page)
    shot(page, "finish_v01_25_after_ab_details.png")
    t = page.inner_text("body")
    info["title_unchanged"] = TITLE_MAIN in t
    info["dom_hidden_number"] = bool(re.search(r"HIDDEN NUMBER|THE HIDDEN", t, re.I))
    info["ok"] = True
    return info


def do_captions(page) -> dict:
    info = {"file": CAPTIONS.name}
    page.goto(
        f"https://studio.youtube.com/video/{VIDEO_ID}/translations",
        wait_until="domcontentloaded",
        timeout=90000,
    )
    page.wait_for_timeout(4500)
    dismiss(page)
    shot(page, "finish_v01_30_captions_before.png")
    # Prefer ADD / Upload for English
    click_text(page, r"^ADD$|^Add$", y_min=100, max_len=10)
    page.wait_for_timeout(800)
    click_text(page, r"Upload file|Upload$", y_min=80, max_len=30)
    page.wait_for_timeout(600)
    up = upload_file_near(page, r"^(Upload|Upload file|Select files|Choose file)$", CAPTIONS)
    info["upload"] = up
    page.wait_for_timeout(2000)
    # Confirm English / Publish / Done
    for pat in [r"^Publish$", r"^Done$", r"^Save$", r"^Confirm$"]:
        if click_text(page, pat, y_min=40, max_len=20):
            info["confirm"] = pat
            page.wait_for_timeout(2500)
            break
    shot(page, "finish_v01_31_captions_after.png")
    body = page.inner_text("body")
    info["has_english"] = bool(re.search(r"English", body, re.I))
    info["published_or_draft"] = bool(re.search(r"Published|Draft|Complete|100%", body, re.I))
    info["ok"] = bool(up.get("ok") or info["has_english"])
    return info


def do_description(page) -> dict:
    info = {}
    goto_edit(page)
    desc_body = DESC.read_text().strip()
    chapters = CHAPTERS.read_text().strip()
    full = desc_body + "\n\n" + chapters + "\n"
    info["has_go_links"] = "/go/" in full
    # Find description box
    found = page.evaluate(
        """() => {
          const walk=(r,d=0)=>{
            if(!r||d>55)return null;
            for (const el of (r.querySelectorAll?r.querySelectorAll('#textbox,textarea,div[contenteditable=true]'):[])) {
              const aria=((el.getAttribute('aria-label')||'')+(el.getAttribute('aria-labelledby')||'')).toLowerCase();
              const rect=el.getBoundingClientRect();
              if (rect.y<100||rect.width<200||rect.height<40) continue;
              if (/description|tell viewers/i.test(aria) || rect.height>80) {
                el.scrollIntoView({block:'center'});
                return {y:rect.y,x:rect.x+20,h:rect.height,aria:aria.slice(0,60)};
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if (el.shadowRoot) { const x=walk(el.shadowRoot,d+1); if(x) return x; }
            }
            return null;
          }; return walk(document);
        }"""
    )
    info["box"] = found
    if found:
        page.mouse.click(found["x"], found["y"])
        page.wait_for_timeout(200)
        page.keyboard.press("Meta+a")
        page.keyboard.type(full, delay=2)
        page.wait_for_timeout(500)
        info["typed"] = True
    info["saved"] = save_details(page)
    shot(page, "finish_v01_32_description.png")
    t = page.inner_text("body")
    info["has_chapters"] = "How small can you cut gold?" in t or "0:00" in t
    info["ok"] = bool(info.get("typed") and not info["has_go_links"])
    return info


def find_modal_save(page) -> dict | None:
    return page.evaluate(
        """() => {
          let discard=null;
          const walkD=(r,d=0)=>{
            if(!r||d>55)return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim();
              if (t==='Discard changes' || t==='Discard') {
                const rect=el.getBoundingClientRect();
                if (rect.width>20 && rect.y<140) discard={x:rect.x,y:rect.y,w:rect.width,h:rect.height,t};
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if (el.shadowRoot) walkD(el.shadowRoot,d+1);
            }
          }; walkD(document);
          if (!discard) return null;
          let save=null;
          const walkS=(r,d=0)=>{
            if(!r||d>55)return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('button,ytcp-button,tp-yt-paper-button,*'):[])) {
              const t=(el.innerText||'').trim();
              if (t!=='Save' && t!=='SAVE') continue;
              const rect=el.getBoundingClientRect();
              if (Math.abs(rect.y - discard.y)>40) continue;
              if (rect.x < discard.x - 20) continue;
              const disabled = el.disabled || el.getAttribute('aria-disabled')==='true';
              save={x:rect.x+rect.width/2,y:rect.y+rect.height/2,w:rect.width,h:rect.height,disabled,t};
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if (el.shadowRoot) walkS(el.shadowRoot,d+1);
            }
          }; walkS(document);
          return {discard, save};
        }"""
    )


def do_end_screen(page) -> dict:
    info = {"related": RELATED_002}
    goto_edit(page)
    click_text(page, r"^End screen$", y_min=200, max_len=20)
    page.wait_for_timeout(4000)
    for _ in range(3):
        dismiss(page)
        click_text(page, r"^OK, got it$", y_min=50, max_len=20)
    shot(page, "finish_v01_40_endscreen_open.png")

    # Template path: 1 video, 1 subscribe
    info["template"] = click_text(page, r"1 video, 1 subscribe", y_min=50, max_len=40)
    page.wait_for_timeout(2500)
    if not info["template"]:
        info["import"] = click_text(page, r"Import from video", y_min=50, max_len=40)
        page.wait_for_timeout(1500)

    # Bind Specific video 002
    click_text(page, r"Best for viewer|Most recent upload|Video:", y_min=80, max_len=60)
    page.wait_for_timeout(500)
    click_text(page, r"Specific video", y_min=60, max_len=40)
    page.wait_for_timeout(800)
    page.evaluate(
        """(q)=>{
          const walk=(r,d=0)=>{
            if(!r||d>55)return false;
            for (const inp of (r.querySelectorAll?r.querySelectorAll('input,textarea'):[])) {
              const aria=((inp.getAttribute('aria-label')||'')+(inp.placeholder||'')).toLowerCase();
              const rect=inp.getBoundingClientRect();
              if(rect.width<40||rect.y<50) continue;
              if(/search|video|url|paste/.test(aria)||inp.type==='search'||inp.type==='text'){
                inp.focus();
                const s=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;
                s.call(inp,q);
                inp.dispatchEvent(new Event('input',{bubbles:true}));
                return true;
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if(el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
            }
            return false;
          };
          return walk(document);
        }""",
        RELATED_002,
    )
    page.keyboard.type(RELATED_002, delay=15)
    page.keyboard.press("Enter")
    page.wait_for_timeout(2500)
    click_text(page, RELATED_TITLE, y_min=80, max_len=90)
    page.wait_for_timeout(1200)
    shot(page, "finish_v01_41_endscreen_bound.png")

    # Ensure last 20s — set times if NaN
    body = page.inner_text("body")
    info["nan_before"] = "NaN" in body
    if info["nan_before"] or not re.search(r"8:2[0-9]|8:4[0-5]", body):
        page.evaluate(
            """() => {
              const vals=['8:25','8:45'];
              let i=0;
              const walk=(r,d=0)=>{
                if(!r||d>55||i>=2)return;
                for (const inp of (r.querySelectorAll?r.querySelectorAll('input'):[])) {
                  const rect=inp.getBoundingClientRect();
                  if (rect.y<60||rect.width<30) continue;
                  const v=(inp.value||'');
                  const aria=(inp.getAttribute('aria-label')||'').toLowerCase();
                  if (/nan/i.test(v) || /time|start|end|from|to/.test(aria) || /^\\d/.test(v) || v==='') {
                    const s=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;
                    s.call(inp, vals[i++]);
                    inp.dispatchEvent(new Event('input',{bubbles:true}));
                    inp.dispatchEvent(new Event('change',{bubbles:true}));
                    if (i>=2) return;
                  }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                  if (el.shadowRoot) walk(el.shadowRoot,d+1);
                }
              }; walk(document);
            }"""
        )
        page.wait_for_timeout(600)

    pair = find_modal_save(page)
    info["modal_save"] = pair
    if pair and pair.get("save") and not pair["save"].get("disabled"):
        page.mouse.click(pair["save"]["x"], pair["save"]["y"])
        info["save"] = "modal"
        page.wait_for_timeout(5000)
    else:
        try:
            btn = page.get_by_role("button", name=re.compile(r"^Save$|^SAVE$", re.I))
            if btn.count() and btn.first.is_enabled():
                btn.first.click(force=True)
                info["save"] = "role"
                page.wait_for_timeout(5000)
            else:
                info["save"] = click_text(page, r"^SAVE$", y_min=0, max_len=10) or "disabled"
                page.wait_for_timeout(4000)
        except Exception as e:
            info["save"] = f"err:{e}"[:80]
    shot(page, "finish_v01_42_endscreen_saved.png")

    # Verify reopen
    goto_edit(page)
    click_text(page, r"^End screen$", y_min=200, max_len=20)
    page.wait_for_timeout(3500)
    for _ in range(2):
        dismiss(page)
        click_text(page, r"^OK, got it$", y_min=50, max_len=20)
    shot(page, "finish_v01_43_endscreen_verify.png")
    tracks = page.evaluate(
        """() => {
          const labels=[];
          const walk=(r,d=0)=>{
            if(!r||d>55)return;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim();
              if (/^Subscribe:/i.test(t) || /^Video:/i.test(t)) labels.push(t.slice(0,80));
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
            }
          }; walk(document);
          return [...new Set(labels)];
        }"""
    )
    info["tracks"] = tracks
    after = page.inner_text("body")
    info["nan"] = "NaN" in after
    info["error"] = bool(re.search(r"problem in processing|couldn't be saved", after, re.I))
    info["has_subscribe_track"] = any(re.search(r"^Subscribe:", t, re.I) for t in tracks)
    info["has_video_track"] = any(re.search(r"^Video:", t, re.I) for t in tracks)
    info["has_002"] = any(re.search(r"Periodic Table|AL_-qlWko_g", t, re.I) for t in tracks) or bool(
        re.search(r"Periodic Table|AL_-qlWko_g", after, re.I)
    )
    info["ok"] = bool(
        not info["error"]
        and not info["nan"]
        and info["has_subscribe_track"]
        and info["has_video_track"]
    )
    return info


def try_pin(page) -> dict:
    info = {"text": PIN.read_text().strip(), "ok": False}
    # Studio comments tab first
    page.goto(
        f"https://studio.youtube.com/video/{VIDEO_ID}/comments",
        wait_until="domcontentloaded",
        timeout=90000,
    )
    page.wait_for_timeout(4000)
    dismiss(page)
    shot(page, "finish_v01_50_comments.png")
    body = page.inner_text("body")
    if re.search(r"Comments are turned off|unavailable|Private|scheduled", body, re.I):
        info["reason"] = "comments_unavailable_while_private_scheduled"
        info["note"] = "Pin on launch day 15 Oct 2026 — package text ready, no links"
        return info
    # Try watch page
    page.goto(f"https://www.youtube.com/watch?v={VIDEO_ID}", wait_until="domcontentloaded", timeout=60000)
    page.wait_for_timeout(3500)
    shot(page, "finish_v01_51_watch.png")
    body = page.inner_text("body")
    if re.search(r"Private video|isn't available|Comments are turned off", body, re.I):
        info["reason"] = "watch_page_not_commentable_while_scheduled_or_private"
        info["note"] = "Pin on launch day 15 Oct 2026 — package text ready, no links"
        return info
    # Attempt comment box
    try:
        box = page.locator("#simplebox-placeholder, #contenteditable-root, ytd-commentbox #contenteditable-root").first
        if box.count():
            box.click(timeout=3000)
            page.keyboard.type(info["text"], delay=8)
            page.wait_for_timeout(500)
            click_text(page, r"^Comment$", y_min=100, max_len=20)
            page.wait_for_timeout(3000)
            # Pin
            click_text(page, r"^Pin$|Pin comment", y_min=100, max_len=30)
            page.wait_for_timeout(1500)
            info["ok"] = True
            info["reason"] = "posted_and_pin_attempted"
        else:
            info["reason"] = "no_comment_box"
    except Exception as e:
        info["reason"] = f"err:{type(e).__name__}"
    shot(page, "finish_v01_52_pin_after.png")
    return info


def main() -> None:
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    (EV / "finish_v01.log").write_text("")
    urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/version", timeout=3)
    result = {
        "at": datetime.now().isoformat(timespec="seconds"),
        "videoId": VIDEO_ID,
        "channel": "@HistoryOfScienceYT",
        "channelId": CHANNEL,
        "order": "Ben FINISH 29 Sep 20:00",
    }

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}", timeout=30000)
        page = browser.contexts[0].pages[0] if browser.contexts[0].pages else browser.contexts[0].new_page()
        page.set_default_timeout(45000)
        try:
            page.bring_to_front()
        except Exception:
            pass

        log("FINISH 0 channel check")
        result["channelCheck"] = channel_check(page)
        if not result["channelCheck"]["ok"]:
            dump("FINISH_V01_RESULT.json", result)
            raise SystemExit("WRONG CHANNEL — STOP")

        log("FINISH 1 Visibility (fix if needed, then leave alone)")
        goto_edit(page)
        shot(page, "finish_v01_01_details.png")
        result["audience_before"] = audience_state(page)
        shot(page, "finish_v01_02_audience.png")
        result["visibility_open"] = open_visibility(page)
        page.wait_for_timeout(1000)
        result["premiere_fix"] = uncheck_premiere_if_needed(page)
        result["visibility"] = probe_visibility(page)
        shot(page, "finish_v01_10_visibility_panel.png")
        shutil.copy2(EV / "finish_v01_10_visibility_panel.png", EV / "FINISH_visibility_15oct_1800_premiere_off.png")
        shutil.copy2(EV / "finish_v01_10_visibility_panel.png", ART / "FINISH_visibility_15oct_1800_premiere_off.png")

        vis_ok = (
            result["visibility"]["has_15"]
            and result["visibility"]["has_1800"]
            and not result["visibility"]["has_30"]
            and result["visibility"]["premiere_off"]
        )
        result["visibility"]["ok"] = vis_ok
        if not vis_ok:
            # Only fix if broken — then leave alone
            if result["visibility"]["premiere_checkbox"].get("checked") is True:
                click_text(page, r"Set as (?:instant )?Premiere", y_min=100, max_len=50)
                page.wait_for_timeout(500)
            # Done/Save only if we had to change
            try:
                btn = page.get_by_role("button", name=re.compile(r"^Done$", re.I))
                if btn.count() and btn.first.is_enabled():
                    btn.first.click(force=True)
                    page.wait_for_timeout(1500)
            except Exception:
                pass
            save_details(page)
            goto_edit(page)
            open_visibility(page)
            page.wait_for_timeout(1000)
            result["visibility_after_fix"] = probe_visibility(page)
            shot(page, "finish_v01_11_visibility_after_fix.png")
            shutil.copy2(EV / "finish_v01_11_visibility_after_fix.png", EV / "FINISH_visibility_15oct_1800_premiere_off.png")
            shutil.copy2(EV / "finish_v01_11_visibility_after_fix.png", ART / "FINISH_visibility_15oct_1800_premiere_off.png")
            result["visibility"]["ok"] = (
                result["visibility_after_fix"]["has_15"]
                and result["visibility_after_fix"]["has_1800"]
                and result["visibility_after_fix"]["premiere_off"]
            )
        else:
            # Leave alone — close panel without Save churn
            page.keyboard.press("Escape")
            page.wait_for_timeout(400)

        if not result["visibility"].get("ok"):
            dump("FINISH_V01_RESULT.json", result)
            log("STOP — Visibility will not stick")
            print(json.dumps(result, indent=2))
            raise SystemExit("VISIBILITY_WONT_STICK")

        dump("FINISH_V01_VISIBILITY.json", result["visibility"])

        log("FINISH 1b thumb A + title check")
        page.keyboard.press("Escape")
        goto_edit(page)
        # Title check
        t = page.inner_text("body")
        result["title_ok"] = TITLE_MAIN in t
        result["thumb"] = upload_thumb_a(page)
        shot(page, "finish_v01_12_thumb_after.png")
        goto_edit(page)
        shot(page, "finish_v01_13_thumb_reload.png")
        t2 = page.inner_text("body")
        result["thumb"]["title_still"] = TITLE_MAIN in t2
        result["thumb"]["dom_hidden_number"] = bool(re.search(r"HIDDEN NUMBER|THE HIDDEN", t2, re.I))
        result["audience_after_thumb"] = audience_state(page)
        dump("FINISH_V01_THUMB.json", result["thumb"])

        log("FINISH 2 Test & Compare")
        result["testAndCompare"] = do_test_and_compare(page)
        dump("FINISH_V01_TC.json", result["testAndCompare"])
        # Copy T&C proof
        for cand in [
            "finish_v01_24_ab_after_save.png",
            "finish_v01_21_ab_dialog.png",
            "finish_v01_20_ab_before.png",
        ]:
            src = EV / cand
            if src.exists():
                shutil.copy2(src, EV / "FINISH_test_and_compare.png")
                shutil.copy2(src, ART / "FINISH_test_and_compare.png")
                break

        log("FINISH 3 description + chapters")
        result["description"] = do_description(page)
        result["audience_after_desc"] = audience_state(page)
        dump("FINISH_V01_DESC.json", result["description"])

        log("FINISH 3 captions")
        result["captions"] = do_captions(page)
        dump("FINISH_V01_CAPTIONS.json", result["captions"])

        log("FINISH 3 end screen (Audience already not-kids)")
        goto_edit(page)
        result["audience_before_endscreen"] = audience_state(page)
        if result["audience_before_endscreen"].get("made_for_kids"):
            result["endScreen"] = {"skipped": True, "reason": "made_for_kids"}
        else:
            result["endScreen"] = do_end_screen(page)
        dump("FINISH_V01_ENDSCREEN.json", result.get("endScreen"))

        log("FINISH 3 pinned comment")
        result["pinnedComment"] = try_pin(page)
        dump("FINISH_V01_PIN.json", result["pinnedComment"])

        # Final audience + visibility leave-alone re-check
        goto_edit(page)
        result["audience_final"] = audience_state(page)
        shot(page, "finish_v01_90_audience_final.png")
        open_visibility(page)
        page.wait_for_timeout(800)
        result["visibility_final"] = probe_visibility(page)
        shot(page, "finish_v01_91_visibility_final.png")
        page.keyboard.press("Escape")

    result["ok_visibility"] = bool(result.get("visibility", {}).get("ok"))
    result["ok_audience"] = bool(result.get("audience_final", {}).get("ok_not_kids"))
    dump("FINISH_V01_RESULT.json", result)
    log(
        "DONE "
        + json.dumps(
            {
                k: result.get(k)
                for k in (
                    "ok_visibility",
                    "ok_audience",
                    "visibility",
                    "thumb",
                    "testAndCompare",
                    "captions",
                    "endScreen",
                    "pinnedComment",
                )
            },
            default=str,
        )[:2500]
    )
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
