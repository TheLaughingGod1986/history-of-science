#!/usr/bin/env python3
"""HOS 004 finish5: complete Title+thumbnail T&C + end screen Video=002 + Subscribe.
Uses Playwright file choosers + dialog waits. CDP :9460 · HOS only · no .env."""
from __future__ import annotations

import json
import re
import subprocess
import time
import urllib.request
from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright

PORT = 9460
CDP = f"http://127.0.0.1:{PORT}"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PROFILE = str(Path.home() / ".hos-chrome-youtube-studio")
CHANNEL = "UCXp7HkBIl1LgaznXuZHJyRg"
VIDEO_ID = "GHZDsiH7L7A"
TITLES = [
    "What's Really Inside an Atom?",
    "Why Is the Periodic Table in This Order?",
    "How Small Can You Cut Gold?",
]
RELATED_002 = "AL_-qlWko_g"
RELATED_TITLE = "How Did We Discover the Periodic Table?"

PROJ = Path(__file__).resolve().parents[2]
PKG = PROJ / "11_Upload-Package"
EV = PKG / "Schedule/evidence_2026-09-29_studio"
ART = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts"
THUMBS = [
    PROJ / "08_Thumbnail/Selected/hos_004_thumb_A_atom_live_v04.jpg",
    PROJ / "08_Thumbnail/Selected/hos_004_thumb_C_hidden_number_live_v06.jpg",
    PROJ / "08_Thumbnail/Selected/hos_004_thumb_B_cut_gold_live_v04.jpg",
]


def log(msg: str) -> None:
    EV.mkdir(parents=True, exist_ok=True)
    line = f"{datetime.now().isoformat(timespec='seconds')} {msg}"
    print(line, flush=True)
    with (EV / "finish5.log").open("a") as f:
        f.write(line + "\n")


def dump(name: str, obj) -> None:
    EV.mkdir(parents=True, exist_ok=True)
    (EV / name).write_text(json.dumps(obj, indent=2) + "\n")
    try:
        ART.mkdir(parents=True, exist_ok=True)
        (ART / f"hos_004_{name}").write_text(json.dumps(obj, indent=2) + "\n")
    except Exception:
        pass


def shot(page, name: str) -> str:
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    dest = EV / name
    page.screenshot(path=str(dest), full_page=False)
    try:
        (ART / f"hos_004_{name}").write_bytes(dest.read_bytes())
    except Exception:
        pass
    return str(dest)


def snip(page, n: int = 4000) -> str:
    try:
        return page.inner_text("body")[:n]
    except Exception as e:
        return f"<err {e}>"


def chrome_up() -> bool:
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/version", timeout=2) as r:
            return r.status == 200
    except Exception:
        return False


def ensure_chrome() -> None:
    if chrome_up():
        log("cdp up")
        return
    for name in ("SingletonLock", "SingletonSocket", "SingletonCookie"):
        try:
            (Path(PROFILE) / name).unlink()
        except FileNotFoundError:
            pass
    subprocess.Popen(
        [
            CHROME,
            f"--remote-debugging-port={PORT}",
            "--remote-allow-origins=*",
            f"--user-data-dir={PROFILE}",
            "--profile-directory=Default",
            "--no-first-run",
            "--no-default-browser-check",
            f"https://studio.youtube.com/channel/{CHANNEL}",
        ],
        stdout=open("/tmp/hos_chrome_9460_finish5.log", "ab"),
        stderr=subprocess.STDOUT,
    )
    for _ in range(50):
        if chrome_up():
            log("cdp started")
            return
        time.sleep(0.5)
    raise SystemExit("CDP fail")


def dismiss(page) -> None:
    for name in ["OK, got it", "Got it", "Dismiss", "Not now", "No thanks", "Close", "Cancel"]:
        try:
            b = page.get_by_role("button", name=re.compile(rf"^{re.escape(name)}$", re.I))
            if b.count() and b.first.is_visible(timeout=500):
                b.first.click(timeout=1000)
                page.wait_for_timeout(200)
        except Exception:
            pass
    try:
        page.keyboard.press("Escape")
    except Exception:
        pass


def js_click(page, pattern: str, y_min: int = 0, exact: bool = False) -> str | None:
    try:
        return page.evaluate(
            """([pattern, yMin, exact]) => {
              const re = exact ? null : new RegExp(pattern, 'i');
              const walk = (root, depth=0) => {
                if (!root || depth > 55) return null;
                const sel = 'button, a, [role="button"], [role="radio"], [role="option"], ytcp-button, tp-yt-paper-button, span, div, yt-formatted-string, li';
                for (const el of (root.querySelectorAll ? root.querySelectorAll(sel) : [])) {
                  const t = (el.innerText || el.textContent || '').trim().replace(/\\s+/g, ' ');
                  if (!t || t.length > 120) continue;
                  const ok = exact ? (t === pattern) : re.test(t);
                  if (!ok) continue;
                  const r = el.getBoundingClientRect();
                  if (r.width < 3 || r.height < 3 || r.y < yMin) continue;
                  el.scrollIntoView({block:'center'});
                  el.click();
                  return t.slice(0,90)+'@'+Math.round(r.x)+','+Math.round(r.y);
                }
                for (const el of (root.querySelectorAll ? root.querySelectorAll('*') : [])) {
                  if (el.shadowRoot) {
                    const h = walk(el.shadowRoot, depth+1);
                    if (h) return h;
                  }
                }
                return null;
              };
              return walk(document);
            }""",
            [pattern, y_min, exact],
        )
    except Exception:
        return None


def wait_text(page, pattern: str, timeout_ms: int = 8000) -> bool:
    deadline = time.time() + timeout_ms / 1000
    while time.time() < deadline:
        if re.search(pattern, snip(page, 6000), re.I):
            return True
        page.wait_for_timeout(300)
    return False


def do_ab(page) -> dict:
    info: dict = {"wanted": "Title and thumbnail", "pairs_wanted": list(zip(TITLES, [t.name for t in THUMBS]))}
    page.goto(
        f"https://studio.youtube.com/video/{VIDEO_ID}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(4000)
    dismiss(page)
    shot(page, "500_edit.png")

    # Click A/B Testing under title (y>~150)
    hit = js_click(page, "A/B Testing", y_min=150, exact=True)
    if not hit:
        hit = js_click(page, r"^A/B Testing$", y_min=120)
    info["open"] = hit
    page.wait_for_timeout(2500)
    shot(page, "501_ab_open.png")
    body = snip(page, 6000)
    info["open_snip"] = body[:1500]

    offers = []
    for label in [
        "Title and thumbnail",
        "Titles and thumbnails",
        "Thumbnail",
        "Title",
        "Thumbnail only",
        "Title only",
    ]:
        if re.search(re.escape(label), body, re.I):
            offers.append(label)
    info["offers"] = offers

    # Choose type if picker showing
    chosen = None
    for label in ["Title and thumbnail", "Titles and thumbnails", "Thumbnail", "Title"]:
        if label in offers or re.search(re.escape(label), body, re.I):
            if js_click(page, label, y_min=100, exact=True) or js_click(page, rf"^{re.escape(label)}$", y_min=100):
                chosen = label
                page.wait_for_timeout(2000)
                break
    info["chosen"] = chosen
    shot(page, "502_ab_type.png")
    body = snip(page, 6000)

    # If we landed in setup UI without choosing, continue
    in_setup = bool(
        re.search(r"Set test|Add thumbnail|Third title|variant|Title and thumbnail", body, re.I)
    )
    info["in_setup"] = in_setup
    if not in_setup and not chosen:
        info["ok"] = False
        info["reason"] = "ab_dialog_did_not_open"
        return info
    if not chosen and in_setup:
        info["chosen"] = "Title and thumbnail (assumed — setup UI)"

    # Fill via file choosers: click each Add thumbnail / upload zone
    uploads = []
    for i, thumb in enumerate(THUMBS):
        # Try click Add thumbnail or empty thumb slot
        clicked = js_click(page, r"^Add thumbnail$", y_min=100)
        if not clicked:
            # click upload icon areas — try nth file input directly
            pass
        try:
            # Prefer set_input_files on all image inputs in y order each pass
            loc = page.locator('input[type="file"]')
            candidates = []
            for j in range(loc.count()):
                acc = (loc.nth(j).get_attribute("accept") or "").lower()
                box = loc.nth(j).bounding_box()
                if not box or box["y"] < 80:
                    continue
                if "image" in acc or "jpeg" in acc or "jpg" in acc or acc == "" or "png" in acc:
                    candidates.append((box["y"], j))
            candidates.sort()
            if i < len(candidates):
                _, j = candidates[i]
                loc.nth(j).set_input_files(str(thumb))
                uploads.append({"slot": i + 1, "file": thumb.name, "input": j})
                page.wait_for_timeout(2000)
            elif candidates:
                # set last
                _, j = candidates[-1]
                loc.nth(j).set_input_files(str(thumb))
                uploads.append({"slot": i + 1, "file": thumb.name, "input": j, "fallback": True})
                page.wait_for_timeout(2000)
            else:
                # file chooser path
                try:
                    with page.expect_file_chooser(timeout=4000) as fc:
                        js_click(page, r"Add thumbnail|Upload|Choose", y_min=100)
                    fc.value.set_files(str(thumb))
                    uploads.append({"slot": i + 1, "file": thumb.name, "via": "chooser"})
                    page.wait_for_timeout(2000)
                except Exception as e:
                    uploads.append({"slot": i + 1, "err": type(e).__name__})
        except Exception as e:
            uploads.append({"slot": i + 1, "err": f"{type(e).__name__}: {e}"})
        shot(page, f"503_thumb_{i+1}.png")
    info["uploads"] = uploads

    # Fill titles top-to-bottom — force overwrite
    titles_out = []
    try:
        # Find title inputs by maxlength 100 or aria
        boxes = []
        all_tb = page.locator("input, textarea")
        for j in range(all_tb.count()):
            el = all_tb.nth(j)
            try:
                if not el.is_visible():
                    continue
                aria = ((el.get_attribute("aria-label") or "") + (el.get_attribute("placeholder") or "")).lower()
                ml = el.get_attribute("maxlength") or ""
                box = el.bounding_box()
                if not box or box["y"] < 100 or box["width"] < 100:
                    continue
                if "title" in aria or ml == "100":
                    boxes.append((box["y"], j))
            except Exception:
                pass
        boxes.sort()
        for k, (_, j) in enumerate(boxes[:3]):
            el = all_tb.nth(j)
            el.click(timeout=3000)
            el.fill("")
            el.fill(TITLES[k])
            titles_out.append({"i": j, "title": TITLES[k]})
            page.wait_for_timeout(400)
    except Exception as e:
        info["title_err"] = f"{type(e).__name__}: {e}"
    info["titles"] = titles_out
    # JS overwrite empty or wrong
    page.evaluate(
        """(titles) => {
          const found = [];
          const walk=(r,d=0)=>{
            if(!r||d>55) return;
            for (const inp of (r.querySelectorAll?r.querySelectorAll('input,textarea'):[])) {
              const aria=((inp.getAttribute('aria-label')||'')+(inp.placeholder||'')).toLowerCase();
              const max=inp.getAttribute('maxlength')||'';
              const rect=inp.getBoundingClientRect();
              if (rect.width < 100 || rect.y < 100) continue;
              if (/title/.test(aria) || max==='100') found.push({inp, y: rect.y});
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
            }
          };
          walk(document);
          found.sort((a,b)=>a.y-b.y);
          for (let i=0;i<Math.min(3,found.length);i++){
            const inp=found[i].inp;
            inp.focus();
            inp.value=titles[i];
            inp.dispatchEvent(new Event('input',{bubbles:true}));
            inp.dispatchEvent(new Event('change',{bubbles:true}));
          }
          return found.length;
        }""",
        TITLES,
    )
    page.wait_for_timeout(1000)
    shot(page, "504_ab_filled.png")
    body = snip(page, 4000)
    info["filled_snip"] = body[:1200]
    info["needs_third"] = bool(re.search(r"Third title and thumbnail are required", body, re.I))

    # Set test
    set_hit = js_click(page, "Set test", y_min=100, exact=True)
    if not set_hit:
        set_hit = js_click(page, r"^Set test$", y_min=100)
    if not set_hit:
        set_hit = js_click(page, r"^Start test$", y_min=100)
    info["set"] = set_hit
    page.wait_for_timeout(4000)
    dismiss(page)
    shot(page, "505_ab_after_set.png")
    after = snip(page, 3000)
    info["after"] = after[:1000]
    info["running"] = bool(re.search(r"A/B test running|test running", after, re.I))
    info["still_required"] = bool(re.search(r"Third title and thumbnail are required", after, re.I))
    info["ok"] = bool(info["running"] or (set_hit and not info["still_required"] and not info["needs_third"]))
    if info["still_required"] or info["needs_third"]:
        info["ok"] = False
        info["note"] = "T&C incomplete — third pair still required; Set test not armed."
    return info


def do_end_screen(page) -> dict:
    info: dict = {"related": RELATED_002, "subscribe": True}
    page.goto(
        f"https://studio.youtube.com/video/{VIDEO_ID}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3000)
    dismiss(page)
    hit = js_click(page, "End screen", y_min=200, exact=True) or js_click(
        page, r"^End screen$", y_min=150
    )
    info["open"] = hit
    page.wait_for_timeout(2500)
    for _ in range(4):
        dismiss(page)
        js_click(page, "OK, got it", exact=True)
        page.keyboard.press("Escape")
        page.wait_for_timeout(200)
    shot(page, "510_endscreen_open.png")

    body = snip(page, 3000)
    # If video element missing, add it
    if not re.search(r"Video:|Best for viewer|Most recent|Periodic Table", body, re.I):
        js_click(page, r"^\+?\s*Element$|^Element$", y_min=100) or js_click(
            page, r"Add element", y_min=100
        )
        page.wait_for_timeout(800)
        js_click(page, r"^Video$", y_min=100, exact=True) or js_click(
            page, r"^Video or playlist$", y_min=100
        )
        page.wait_for_timeout(1200)
        info["added_video"] = True
        shot(page, "511_added_video.png")

    # Prefer specific video
    for pat in [
        "Specific video",
        "Choose a specific video",
        "Best for viewer",
        "Most recent upload",
        "Video: Best for viewer",
        "Video: Most recent upload",
    ]:
        if js_click(page, pat, y_min=80):
            info["clicked_el"] = pat
            page.wait_for_timeout(1000)
            break

    js_click(page, "Specific video", y_min=80, exact=True) or js_click(
        page, r"^Specific video$", y_min=80
    )
    page.wait_for_timeout(800)

    # Fill search with id
    filled = page.evaluate(
        """(q) => {
          const c=[];
          const walk=(r,d=0)=>{
            if(!r||d>55) return;
            for (const inp of (r.querySelectorAll?r.querySelectorAll('input,textarea'):[])) {
              const aria=((inp.getAttribute('aria-label')||'')+(inp.placeholder||'')+(inp.type||'')).toLowerCase();
              const rect=inp.getBoundingClientRect();
              if (rect.width<50 || rect.y<50) continue;
              if (/search|video|url|paste|id/.test(aria) || ['search','text','url'].includes(inp.type)) {
                c.push({inp,y:rect.y,aria});
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if (el.shadowRoot) walk(el.shadowRoot,d+1);
            }
          };
          walk(document);
          c.sort((a,b)=>a.y-b.y);
          if(!c.length) return null;
          const inp=c[0].inp; inp.focus(); inp.value=q;
          inp.dispatchEvent(new Event('input',{bubbles:true}));
          return {aria:c[0].aria,y:c[0].y};
        }""",
        RELATED_002,
    )
    info["fill"] = filled
    page.keyboard.press("Enter")
    page.wait_for_timeout(2200)
    if not js_click(page, r"Periodic Table|How Did We Discover the Periodic", y_min=80):
        # try title
        page.evaluate(
            """(q) => {
              const walk=(r,d=0)=>{
                if(!r||d>55) return false;
                for (const inp of (r.querySelectorAll?r.querySelectorAll('input,textarea'):[])) {
                  const rect=inp.getBoundingClientRect();
                  if (rect.width<60) continue;
                  inp.focus(); inp.value=q;
                  inp.dispatchEvent(new Event('input',{bubbles:true}));
                  return true;
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                  if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
                }
                return false;
              };
              return walk(document);
            }""",
            RELATED_TITLE,
        )
        page.keyboard.press("Enter")
        page.wait_for_timeout(2000)
        js_click(page, r"Periodic Table|How Did We Discover", y_min=80)
    page.wait_for_timeout(1000)
    shot(page, "512_video_picked.png")

    # Subscribe
    body2 = snip(page, 3000)
    if not re.search(r"Subscribe", body2, re.I):
        js_click(page, r"^\+?\s*Element$|Add element", y_min=100)
        page.wait_for_timeout(600)
        js_click(page, "Subscribe", y_min=100, exact=True)
        page.wait_for_timeout(800)
    shot(page, "513_before_save.png")

    save = js_click(page, "Save", y_min=0, exact=True)
    if not save:
        try:
            page.get_by_role("button", name=re.compile(r"^Save$", re.I)).first.click(timeout=4000)
            save = "Save"
        except Exception:
            pass
    info["save"] = save
    page.wait_for_timeout(2500)
    js_click(page, "Save", exact=True)
    page.wait_for_timeout(1500)
    shot(page, "514_endscreen_saved.png")
    after = snip(page, 3500)
    info["after"] = after[:1000]
    info["has_002"] = bool(
        re.search(r"AL_-qlWko_g|Periodic Table|How Did We Discover the Periodic", after, re.I)
    )
    info["has_subscribe"] = bool(re.search(r"Subscribe", after, re.I))
    info["error_need_video"] = bool(
        re.search(r"At least one element must be a video", after, re.I)
    )
    info["best_for_viewer"] = bool(re.search(r"Best for viewer", after, re.I))
    info["ok"] = bool(
        info.get("save")
        and info["has_subscribe"]
        and (info["has_002"] or info["best_for_viewer"])
        and not info["error_need_video"]
    )
    if info["best_for_viewer"] and not info["has_002"]:
        info["note"] = "Saved with Best for viewer + Subscribe (specific 002 not bound)."
    if info["error_need_video"]:
        info["ok"] = False
        info["note"] = "End screen Save blocked — needs a video/playlist element."
    return info


def verify_schedule(page) -> dict:
    page.goto(
        f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3500)
    dismiss(page)
    shot(page, "520_content.png")
    tip = ""
    try:
        page.locator("ytcp-video-row").filter(
            has_text=re.compile(r"What's Really Inside an Atom", re.I)
        ).locator("text=Scheduled").first.hover(timeout=6000)
        page.wait_for_timeout(1200)
        tip = snip(page, 4000)
        shot(page, "521_schedule_proof.png")
    except Exception as e:
        tip = f"<err {type(e).__name__}>"
        try:
            page.get_by_text("Scheduled").first.hover(timeout=4000)
            page.wait_for_timeout(1000)
            tip = snip(page, 4000)
            shot(page, "521_schedule_proof.png")
        except Exception:
            pass
    body = snip(page, 3000)
    text = body + tip
    return {
        "has15": bool(re.search(r"15\s*(Oct|October)\s*2026", text, re.I)),
        "has1800": bool(re.search(r"18:00", text)),
        "scheduled": bool(re.search(r"Scheduled", body, re.I)),
        "tooltip": bool(re.search(r"15 October 2026 at 18:00", tip, re.I)),
        "tip_snip": tip[:500],
    }


def main() -> int:
    EV.mkdir(parents=True, exist_ok=True)
    (EV / "finish5.log").write_text("")
    ensure_chrome()
    result: dict = {
        "ok": False,
        "videoId": VIDEO_ID,
        "channel": "@HistoryOfScienceYT",
        "channelId": CHANNEL,
        "at": datetime.now().isoformat(timespec="seconds"),
    }
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        ctx = browser.contexts[0]
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.on("dialog", lambda d: d.accept())
        try:
            page.goto(
                f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload",
                wait_until="domcontentloaded",
                timeout=120000,
            )
            page.wait_for_timeout(3000)
            body = snip(page, 1500)
            hos_ok = "History of Science" in body and CHANNEL in page.url
            result["channelCheck"] = {"ok": hos_ok, "url": page.url, "snip": body[:300]}
            if not hos_ok:
                dump("FINISH5_RESULT.json", result)
                return 2

            result["abTest"] = do_ab(page)
            log(
                f"ab offers={result['abTest'].get('offers')} chosen={result['abTest'].get('chosen')} "
                f"running={result['abTest'].get('running')} ok={result['abTest'].get('ok')}"
            )
            result["endScreen"] = do_end_screen(page)
            log(
                f"end ok={result['endScreen'].get('ok')} 002={result['endScreen'].get('has_002')} "
                f"sub={result['endScreen'].get('has_subscribe')} err={result['endScreen'].get('error_need_video')}"
            )
            result["schedule"] = verify_schedule(page)
            result["pin"] = {
                "ok": False,
                "reason": "watch_page_not_commentable_while_scheduled_or_private",
                "note": "Pin on launch day 15 Oct 2026 from manifest pinned comment.",
            }
            result["ok"] = bool(
                result["channelCheck"]["ok"]
                and result["schedule"].get("has15")
                and result["schedule"].get("scheduled")
            )
            dump("FINISH5_RESULT.json", result)
            log(f"DONE ok={result['ok']}")
            return 0 if result["ok"] else 1
        except Exception as e:
            result["error"] = f"{type(e).__name__}: {e}"
            dump("FINISH5_RESULT.json", result)
            log(f"ERROR {result['error']}")
            try:
                shot(page, "599_error.png")
            except Exception:
                pass
            return 3


if __name__ == "__main__":
    raise SystemExit(main())
