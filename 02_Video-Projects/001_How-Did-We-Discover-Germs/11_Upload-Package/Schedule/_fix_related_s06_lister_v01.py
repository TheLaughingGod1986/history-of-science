#!/usr/bin/env python3
"""Set Related `_C92tIJCk8A` on Lister Short clV6E10NLPw. HOS only. Do not touch CUu8k38iAMc."""
from __future__ import annotations

import importlib.util
import json
import re
import shutil
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from playwright.sync_api import sync_playwright

REPO = Path("/Users/benjaminoats/YouTube/History Of Science")
U004 = (
    REPO
    / "02_Video-Projects/004_Whats-Really-Inside-An-Atom/11_Upload-Package/Schedule"
    / "_upload_hos_004_shorts_v01.py"
)
SCHED = (
    REPO
    / "02_Video-Projects/001_How-Did-We-Discover-Germs/11_Upload-Package/Schedule"
)
EV = SCHED / "evidence_2026-09-30_s06_lister"
ART = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts"
AGENT = Path.home() / (
    "Library/Application Support/Cursor/AgentStores/"
    "cursor_agent_stores/bc-958ae0f3-be07-568f-a2ab-eb7f422d8839/files/artifacts"
)
LONDON = ZoneInfo("Europe/London")

VID = "clV6E10NLPw"
RELATED_ID = "_C92tIJCk8A"
RELATED_TITLE = "How Did We Discover Germs?"
BANNED = {"CUu8k38iAMc"}


def load_u():
    spec = importlib.util.spec_from_file_location("hos004_upload", U004)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


def shot(page, name: str) -> None:
    EV.mkdir(parents=True, exist_ok=True)
    p = EV / name
    page.screenshot(path=str(p), full_page=True)
    for d in (ART, AGENT):
        d.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, d / f"BEN_1445_{name}")


def related_chunk(page) -> str:
    t = page.inner_text("body")
    if "Related video" not in t:
        return ""
    return t.split("Related video", 1)[-1][:220]


def related_ok(chunk: str) -> bool:
    if not chunk:
        return False
    head = chunk[:80]
    if re.search(r"\bNone\b", head):
        return False
    return RELATED_TITLE in chunk or "Germs" in head


def list_cards(page, needle: str = "") -> list[dict]:
    return page.evaluate(
        """(needle) => {
          const hits=[];
          const walk=(r,d=0)=>{
            if(!r||d>55) return;
            const nodes = r.querySelectorAll
              ? r.querySelectorAll('ytcp-video-list-cell-video,ytcp-entity-card,ytcp-video-row,[role=option],a,div')
              : [];
            for (const el of nodes) {
              const tx=(el.innerText||'').replace(/\\s+/g,' ').trim();
              if (!tx || tx.length<8 || tx.length>280) continue;
              if (needle && !tx.toLowerCase().includes(needle.toLowerCase())
                  && !tx.includes(needle)) continue;
              const b=el.getBoundingClientRect();
              if (b.width>90 && b.height>36 && b.width<900 && b.y>40 && b.y<900)
                hits.push({
                  t: tx.slice(0,160),
                  tag: el.tagName,
                  w: Math.round(b.width),
                  h: Math.round(b.height),
                  x: Math.round(b.x+b.width/2),
                  y: Math.round(b.y+b.height/2),
                });
            }
            for (const el of (r.querySelectorAll ? r.querySelectorAll('*') : []))
              if (el.shadowRoot) walk(el.shadowRoot, d+1);
          };
          const dlg = document.querySelector('ytcp-video-pick-dialog') || document;
          walk(dlg);
          // dedupe by approx position
          const seen=new Set();
          const out=[];
          for (const h of hits.sort((a,b)=>a.h-b.h)) {
            const k=`${h.x>>3}_${h.y>>3}`;
            if (seen.has(k)) continue;
            seen.add(k);
            out.push(h);
          }
          return out.slice(0,40);
        }""",
        needle,
    )


def open_related_picker(page, u) -> dict:
    info: dict = {"open": False}
    for _ in range(18):
        page.mouse.wheel(0, 1400)
        page.wait_for_timeout(120)
    # Prefer dedicated Shorts related widget
    try:
        w = page.locator("ytcp-shorts-content-links-picker").first
        if w.count():
            w.scroll_into_view_if_needed(timeout=4000)
            w.click(force=True, timeout=5000)
            info["via"] = "shorts-content-links-picker"
            info["open"] = True
    except Exception as e:
        info["widget_err"] = f"{type(e).__name__}:{e}"
    if not info.get("open"):
        clicked = u.click_shadow_text(
            page, r"Add (a )?related video|Select video|Add video|^None$"
        )
        info["via"] = clicked or "shadow_fail"
        info["open"] = bool(clicked)
    if not info.get("open"):
        # Click Related video label / None chip
        hit = page.evaluate(
            """() => {
              const walk=(r,d=0)=>{
                if(!r||d>50) return null;
                for (const el of (r.querySelectorAll
                  ? r.querySelectorAll('ytcp-button,button,[role=button],div,span,ytcp-icon-button')
                  : [])) {
                  const t=(el.innerText||'').trim();
                  const a=el.getAttribute('aria-label')||'';
                  if (/related video/i.test(a) || t==='None' || t==='Add' || t==='Add video'
                      || /^Related video$/i.test(t)) {
                    const b=el.getBoundingClientRect();
                    if (b.width>20 && b.height>16 && b.y>200)
                      return {x:b.x+b.width/2,y:b.y+b.height/2,t:(t||a).slice(0,60)};
                  }
                }
                for (const el of (r.querySelectorAll ? r.querySelectorAll('*') : [])) {
                  if (el.shadowRoot) {
                    const h=walk(el.shadowRoot,d+1);
                    if (h) return h;
                  }
                }
                return null;
              };
              return walk(document);
            }"""
        )
        if hit:
            page.mouse.click(hit["x"], hit["y"])
            info["via"] = f"mouse:{hit['t']}"
            info["open"] = True
    page.wait_for_timeout(2500)
    try:
        page.locator("ytcp-video-pick-dialog").first.wait_for(state="visible", timeout=15000)
        info["dialog"] = True
    except Exception:
        info["dialog"] = False
    return info


def fill_search(page, query: str) -> str:
    # Prefer #search-yours host / inner input inside dialog
    selectors = [
        "ytcp-video-pick-dialog #search-yours input",
        "ytcp-video-pick-dialog input#search-yours",
        "ytcp-video-pick-dialog #search-yours",
        "ytcp-video-pick-dialog tp-yt-paper-input input",
        "ytcp-video-pick-dialog input[type='text']",
        "#search-yours input",
        "#search-yours",
    ]
    for sel in selectors:
        loc = page.locator(sel).first
        try:
            if not loc.count():
                continue
            loc.click(force=True, timeout=2500)
            page.keyboard.press("Meta+a")
            page.keyboard.press("Backspace")
            page.wait_for_timeout(200)
            page.keyboard.type(query, delay=25)
            page.wait_for_timeout(2800)
            return f"typed:{sel}"
        except Exception:
            continue
    # JS fill fallback
    ok = page.evaluate(
        """(q) => {
          const dlg=document.querySelector('ytcp-video-pick-dialog');
          if(!dlg) return 'no_dlg';
          const walk=(r,d=0)=>{
            if(!r||d>40) return null;
            for (const el of (r.querySelectorAll?r.querySelectorAll('input'):[])) {
              const t=(el.getAttribute('aria-label')||'')+(el.id||'')+(el.placeholder||'');
              if (/search/i.test(t) || el.id==='search-yours' || el.type==='text') {
                el.focus(); el.value=''; el.dispatchEvent(new Event('input',{bubbles:true}));
                el.value=q; el.dispatchEvent(new Event('input',{bubbles:true}));
                return el.id||el.placeholder||'input';
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) { const h=walk(el.shadowRoot,d+1); if(h) return h; }
            return null;
          };
          return walk(dlg)||'no_input';
        }""",
        query,
    )
    page.wait_for_timeout(2800)
    return f"js:{ok}"


def dismiss_dialog(page) -> None:
    try:
        page.keyboard.press("Escape")
        page.wait_for_timeout(600)
    except Exception:
        pass
    try:
        page.locator("ytcp-video-pick-dialog #close-button, ytcp-video-pick-dialog [aria-label='Close']").first.click(
            force=True, timeout=1500
        )
    except Exception:
        pass


def click_tabs(page) -> list[str]:
    """Click Your videos / Search YouTube / Playlist tabs if present."""
    found = page.evaluate(
        """() => {
          const out=[];
          const walk=(r,d=0)=>{
            if(!r||d>45) return;
            for (const el of (r.querySelectorAll
              ? r.querySelectorAll('[role=tab],tp-yt-paper-tab,button,div') : [])) {
              const t=(el.innerText||'').trim();
              if (/^(Your videos|Search YouTube|Playlists|Playlist)$/i.test(t)) {
                const b=el.getBoundingClientRect();
                if (b.width>40 && b.height>18 && b.y>60 && b.y<400)
                  out.push({t,x:b.x+b.width/2,y:b.y+b.height/2});
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
          };
          const dlg=document.querySelector('ytcp-video-pick-dialog')||document;
          walk(dlg);
          return out;
        }"""
    )
    clicked = []
    for h in found or []:
        try:
            page.mouse.click(h["x"], h["y"])
            page.wait_for_timeout(1200)
            clicked.append(h["t"])
        except Exception:
            pass
    return clicked


def try_pick(page, queries: list[str]) -> dict:
    out: dict = {"attempts": []}
    # Wait for default grid
    for i in range(12):
        cards = list_cards(page)
        dlg_t = ""
        try:
            dlg_t = page.locator("ytcp-video-pick-dialog").inner_text()[:500]
        except Exception:
            pass
        if cards:
            out["grid_wait"] = i
            out["grid_n"] = len(cards)
            out["grid_sample"] = [c["t"][:80] for c in cards[:8]]
            break
        # scroll inside dialog
        page.evaluate(
            """() => {
              const dlg=document.querySelector('ytcp-video-pick-dialog');
              if(!dlg) return;
              const walk=(r,d=0)=>{
                if(!r||d>40) return;
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                  if (el.scrollHeight > el.clientHeight + 40) el.scrollTop += 400;
                  if (el.shadowRoot) walk(el.shadowRoot,d+1);
                }
              };
              walk(dlg);
            }"""
        )
        page.wait_for_timeout(900)
    else:
        out["grid_wait"] = "empty"
        out["dlg_empty_snip"] = dlg_t[:300] if dlg_t else ""

    # Try tabs
    out["tabs"] = click_tabs(page)

    for q in queries:
        att: dict = {"q": q}
        att["fill"] = fill_search(page, q)
        page.wait_for_timeout(1500)
        cards = list_cards(page, "")
        germs = [c for c in cards if "Germs" in c["t"] or RELATED_ID in c["t"] or "Discover Germs" in c["t"]]
        # Prefer landscape / long duration cards
        prefer = [
            c
            for c in germs
            if re.search(r"\b[1-9]:\d{2}\b|\b1[0-9]:\d{2}\b", c["t"]) or "How Did We Discover Germs" in c["t"]
        ] or germs
        att["cards_n"] = len(cards)
        att["germs_n"] = len(germs)
        att["sample"] = [c["t"][:90] for c in (prefer or cards)[:6]]
        try:
            att["dlg"] = page.locator("ytcp-video-pick-dialog").inner_text()[:350]
        except Exception:
            att["dlg"] = ""
        if prefer:
            # Avoid huge empty-state art: prefer mid-size cards
            prefer.sort(key=lambda c: abs(c["h"] - 72) + abs(c["w"] - 320))
            c = prefer[0]
            # Guard: empty-state art is often very tall/wide decorative
            if c["h"] > 220 and c["w"] > 400 and "How Did We Discover Germs" not in c["t"]:
                att["skip_empty_art"] = c
            else:
                page.mouse.click(c["x"], c["y"])
                page.wait_for_timeout(1200)
                att["clicked"] = c
                out["attempts"].append(att)
                out["picked"] = c["t"]
                return out
        out["attempts"].append(att)
    return out


def page_save(page, u) -> dict:
    return u.page_save(page)


def capture_settings(page, u) -> dict:
    """Scroll + screenshot schedule/audience/AI/Related/cover after save."""
    info: dict = {}
    page.goto(
        f"https://studio.youtube.com/video/{VID}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3500)
    u.dismiss(page)
    body = page.inner_text("body")
    info["title_ok"] = "The spray that stopped surgery killing patients" in body
    info["chip"] = u.visibility_chip(page) if hasattr(u, "visibility_chip") else ""
    # schedule from chip / visibility
    m = re.search(r"Scheduled for ([^\n]+)", body)
    info["scheduled_for"] = m.group(1).strip() if m else None
    info["schedule_ok"] = bool(
        info.get("scheduled_for")
        and "20" in (info["scheduled_for"] or "")
        and ("Oct" in (info["scheduled_for"] or "") or "October" in (info["scheduled_for"] or ""))
        and "11:30" in (info["scheduled_for"] or "")
    ) or ("Visibility Scheduled" in body and "20 Oct" in body)
    # Audience
    info["audience"] = u.read_audience(page) if hasattr(u, "read_audience") else {}
    # AI
    info["ai"] = u.read_ai(page) if hasattr(u, "read_ai") else {}
    chunk = related_chunk(page)
    info["related_chunk"] = chunk
    info["related_ok"] = related_ok(chunk)
    # Cover: scroll top + shot
    page.evaluate("window.scrollTo(0,0)")
    page.wait_for_timeout(400)
    shot(page, "s06_FINAL_cover_title.png")
    # Audience / AI region
    for _ in range(8):
        page.mouse.wheel(0, 900)
        page.wait_for_timeout(150)
    shot(page, "s06_FINAL_audience_ai.png")
    # Related region
    for _ in range(6):
        page.mouse.wheel(0, 900)
        page.wait_for_timeout(150)
    shot(page, "s06_FINAL_related.png")
    # Visibility chip area — open visibility dialog briefly for schedule proof
    try:
        if hasattr(u, "open_vis"):
            u.open_vis(page)
            page.wait_for_timeout(1200)
            shot(page, "s06_FINAL_schedule.png")
            page.keyboard.press("Escape")
            page.wait_for_timeout(500)
    except Exception as e:
        info["vis_err"] = f"{type(e).__name__}:{e}"
    # Full page
    shot(page, "s06_FINAL_edit_full.png")
    # Fallback reads if helpers missing
    if not info.get("audience"):
        info["audience_snip"] = "not Made for Kids" in body or "No, it's not" in body
    if not info.get("ai"):
        yes = "Yes, AI was used" in body
        info["ai_snip_yes"] = yes
    info["body_has_private"] = "Private" in body[:2500]
    info["premiere"] = bool(re.search(r"Premiere", body[:3000]))
    return info


def main() -> int:
    u = load_u()
    u.EV = EV
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    result: dict = {
        "vid": VID,
        "related_id": RELATED_ID,
        "related_title": RELATED_TITLE,
        "started": datetime.now(LONDON).isoformat(timespec="seconds"),
        "do_not_touch": list(BANNED),
        "list_calls": [],
    }

    u.ensure_chrome()
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(u.CDP)
        ctx = browser.contexts[0]
        page = u.studio_page(ctx)
        page.bring_to_front()
        hos = u.ensure_hos(page)
        result["hos"] = hos
        if not hos.get("ok"):
            (EV / "RELATED_FINAL.json").write_text(json.dumps(result, indent=2) + "\n")
            print(json.dumps(result, indent=2)[:2000])
            return 2

        # Capture list_creator_videos
        def on_response(resp):
            if "list_creator_videos" not in resp.url and "creator_videos" not in resp.url:
                return
            try:
                data = resp.json()
            except Exception:
                try:
                    data = {"raw": resp.text()[:2500]}
                except Exception:
                    data = {"raw": "unreadable"}
            text = json.dumps(data)
            ids = re.findall(r'"videoId"\s*:\s*"([A-Za-z0-9_-]{11})"', text)
            titles = re.findall(
                r'"title"\s*:\s*\{[^}]*"simpleText"\s*:\s*"([^"]+)"', text
            )
            if not titles:
                titles = re.findall(r'"simpleText"\s*:\s*"([^"]{8,120})"', text)[:40]
            entry = {
                "status": resp.status,
                "url": resp.url[:160],
                "ids": list(dict.fromkeys(ids))[:50],
                "titles": titles[:25],
                "has_germs_id": RELATED_ID in text,
                "has_germs_title": "Germs" in text,
                "len": len(text),
            }
            result["list_calls"].append(entry)
            print(
                f"LIST status={entry['status']} n={len(entry['ids'])} "
                f"has_germs={entry['has_germs_id']} titles={entry['titles'][:4]}",
                flush=True,
            )

        page.on("response", on_response)

        # Confirm we never navigate to banned id
        page.goto(
            f"https://studio.youtube.com/video/{VID}/edit",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(3500)
        u.dismiss(page)
        if any(b in page.url for b in BANNED):
            result["error"] = "navigated_to_banned"
            (EV / "RELATED_FINAL.json").write_text(json.dumps(result, indent=2) + "\n")
            return 3

        chunk0 = related_chunk(page)
        result["related0"] = chunk0
        shot(page, "s06_rel_retry_edit.png")
        if related_ok(chunk0):
            result["ok"] = True
            result["status"] = "already_set"
            result["settings"] = capture_settings(page, u)
            (EV / "RELATED_FINAL.json").write_text(json.dumps(result, indent=2, default=str) + "\n")
            print(json.dumps(result, indent=2, default=str)[:4000])
            return 0

        # Attempt 1: open picker, wait, search
        op = open_related_picker(page, u)
        result["open1"] = op
        shot(page, "s06_rel_retry_modal.png")
        page.wait_for_timeout(8000)  # let list API settle
        shot(page, "s06_rel_retry_waited.png")
        pick = try_pick(
            page,
            [
                RELATED_TITLE,
                "How Did We Discover Germs",
                "Discover Germs",
                "Germs",
                RELATED_ID,
                "How Did We",
            ],
        )
        result["pick1"] = pick
        shot(page, "s06_rel_retry_after_pick.png")

        if pick.get("picked"):
            save = page_save(page, u)
            result["save1"] = save
            page.wait_for_timeout(2000)
        else:
            # Attempt 2: Search YouTube tab + paste watch URL
            dismiss_dialog(page)
            page.wait_for_timeout(800)
            op2 = open_related_picker(page, u)
            result["open2"] = op2
            page.wait_for_timeout(5000)
            tabs = click_tabs(page)
            result["tabs2"] = tabs
            # Click Search YouTube explicitly
            page.evaluate(
                """() => {
                  const walk=(r,d=0)=>{
                    if(!r||d>45) return false;
                    for (const el of (r.querySelectorAll
                      ? r.querySelectorAll('[role=tab],tp-yt-paper-tab,button,div,span') : [])) {
                      const t=(el.innerText||'').trim();
                      if (/Search YouTube/i.test(t)) { el.click(); return true; }
                    }
                    for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[]))
                      if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
                    return false;
                  };
                  return walk(document.querySelector('ytcp-video-pick-dialog')||document);
                }"""
            )
            page.wait_for_timeout(1000)
            for q in [
                f"https://www.youtube.com/watch?v={RELATED_ID}",
                RELATED_ID,
                RELATED_TITLE,
            ]:
                fill_search(page, q)
                page.wait_for_timeout(2500)
                cards = list_cards(page)
                germs = [
                    c
                    for c in cards
                    if "Germs" in c["t"] or RELATED_ID in c["t"]
                ]
                if germs:
                    germs.sort(key=lambda c: abs(c["h"] - 72))
                    c = germs[0]
                    page.mouse.click(c["x"], c["y"])
                    result["pick2"] = c
                    page.wait_for_timeout(1000)
                    break
            shot(page, "s06_rel_retry_search_yt.png")
            save = page_save(page, u)
            result["save2"] = save

        # Verify Related after reload
        page.goto(
            f"https://studio.youtube.com/video/{VID}/edit",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(3500)
        u.dismiss(page)
        chunk = related_chunk(page)
        result["related_final_chunk"] = chunk
        result["ok"] = related_ok(chunk)
        result["status"] = "set" if result["ok"] else "still_none"

        # If still none but API had germs — one more grid scroll+click without search
        if not result["ok"] and any(c.get("has_germs_id") for c in result["list_calls"]):
            op3 = open_related_picker(page, u)
            result["open3"] = op3
            page.wait_for_timeout(10000)
            # Clear search
            fill_search(page, "")
            page.wait_for_timeout(2000)
            for _ in range(20):
                cards = list_cards(page, "Germs")
                if cards:
                    cards.sort(key=lambda c: abs(c["h"] - 72))
                    page.mouse.click(cards[0]["x"], cards[0]["y"])
                    result["pick3"] = cards[0]
                    page_save(page, u)
                    break
                page.evaluate(
                    """() => {
                      const dlg=document.querySelector('ytcp-video-pick-dialog');
                      if(!dlg) return;
                      const walk=(r,d=0)=>{
                        if(!r||d>40) return;
                        for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                          if (el.scrollHeight > el.clientHeight + 40) el.scrollTop += 500;
                          if (el.shadowRoot) walk(el.shadowRoot,d+1);
                        }
                      };
                      walk(dlg);
                    }"""
                )
                page.wait_for_timeout(700)
            page.goto(
                f"https://studio.youtube.com/video/{VID}/edit",
                wait_until="domcontentloaded",
                timeout=120000,
            )
            page.wait_for_timeout(3500)
            chunk = related_chunk(page)
            result["related_final_chunk"] = chunk
            result["ok"] = related_ok(chunk)
            result["status"] = "set" if result["ok"] else "still_none"

        result["settings"] = capture_settings(page, u)
        result["finished"] = datetime.now(LONDON).isoformat(timespec="seconds")
        # Never leave on banned video
        result["final_url"] = page.url
        result["touched_banned"] = any(b in page.url for b in BANNED)
        (EV / "RELATED_FINAL.json").write_text(
            json.dumps(result, indent=2, default=str) + "\n"
        )
        (EV / "LIST_CREATOR_VIDEOS.json").write_text(
            json.dumps(result["list_calls"], indent=2, default=str) + "\n"
        )
        print(json.dumps(result, indent=2, default=str)[:6000])
        return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
