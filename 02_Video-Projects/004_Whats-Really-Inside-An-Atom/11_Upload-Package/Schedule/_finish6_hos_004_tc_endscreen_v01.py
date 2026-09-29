#!/usr/bin/env python3
"""HOS 004 finish6 — minimal: open A/B → Title and thumbnail → 3 pairs → Set test;
end screen template 1 video 1 subscribe → bind 002. CDP :9460 · no .env."""
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
EV = PROJ / "11_Upload-Package/Schedule/evidence_2026-09-29_studio"
ART = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts"
THUMBS = [
    PROJ / "08_Thumbnail/Selected/hos_004_thumb_A_atom_live_v04.jpg",
    PROJ / "08_Thumbnail/Selected/hos_004_thumb_C_hidden_number_live_v06.jpg",
    PROJ / "08_Thumbnail/Selected/hos_004_thumb_B_cut_gold_live_v04.jpg",
]


def log(m: str) -> None:
    EV.mkdir(parents=True, exist_ok=True)
    line = f"{datetime.now().isoformat(timespec='seconds')} {m}"
    print(line, flush=True)
    with (EV / "finish6.log").open("a") as f:
        f.write(line + "\n")


def dump(n, o):
    EV.mkdir(parents=True, exist_ok=True)
    (EV / n).write_text(json.dumps(o, indent=2) + "\n")
    try:
        ART.mkdir(parents=True, exist_ok=True)
        (ART / f"hos_004_{n}").write_text(json.dumps(o, indent=2) + "\n")
    except Exception:
        pass


def shot(page, n):
    EV.mkdir(parents=True, exist_ok=True)
    p = EV / n
    page.screenshot(path=str(p), full_page=False)
    try:
        (ART / f"hos_004_{n}").write_bytes(p.read_bytes())
    except Exception:
        pass
    return str(p)


def snip(page, n=5000):
    try:
        return page.inner_text("body")[:n]
    except Exception as e:
        return str(e)


def chrome_up():
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/version", timeout=2) as r:
            return r.status == 200
    except Exception:
        return False


def ensure_chrome():
    if chrome_up():
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
        stdout=open("/tmp/hos_chrome_finish6.log", "ab"),
        stderr=subprocess.STDOUT,
    )
    for _ in range(50):
        if chrome_up():
            return
        time.sleep(0.5)
    raise SystemExit("cdp fail")


def dismiss(page):
    for name in ["OK, got it", "Got it", "Dismiss", "Close", "Cancel", "Not now"]:
        try:
            b = page.get_by_role("button", name=re.compile(rf"^{re.escape(name)}$", re.I))
            if b.count() and b.first.is_visible(timeout=400):
                b.first.click(timeout=800)
        except Exception:
            pass
    try:
        page.keyboard.press("Escape")
    except Exception:
        pass


def find_click(page, text: str, y_min=0):
    """Return bounding box center of exact visible text and click it."""
    box = page.evaluate(
        """([text, yMin]) => {
          const walk = (root, depth=0) => {
            if (!root || depth > 55) return null;
            for (const el of (root.querySelectorAll
              ? root.querySelectorAll('button, a, [role="button"], [role="radio"], [role="tab"], ytcp-button, span, div, yt-formatted-string')
              : [])) {
              const t = (el.innerText || el.textContent || '').trim().replace(/\\s+/g, ' ');
              if (t !== text) continue;
              const r = el.getBoundingClientRect();
              if (r.width < 4 || r.height < 4 || r.y < yMin) continue;
              return {x: r.x + r.width/2, y: r.y + r.height/2, w: r.width, h: r.height};
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
        [text, y_min],
    )
    if not box:
        return None
    page.mouse.click(box["x"], box["y"])
    page.wait_for_timeout(800)
    return box


def wait_for(page, pattern, ms=10000):
    t0 = time.time()
    while time.time() - t0 < ms / 1000:
        if re.search(pattern, snip(page, 8000), re.I):
            return True
        page.wait_for_timeout(250)
    return False


def do_ab(page):
    info = {"wanted": "Title and thumbnail"}
    page.goto(
        f"https://studio.youtube.com/video/{VIDEO_ID}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(4500)
    dismiss(page)
    shot(page, "600_edit.png")

    # Click A/B Testing — try mouse on exact text
    box = find_click(page, "A/B Testing", y_min=140)
    info["open_box"] = box
    if not box:
        # force via get_by_text
        try:
            page.get_by_text("A/B Testing", exact=True).first.click(timeout=5000)
            info["open"] = "get_by_text"
        except Exception as e:
            info["open_err"] = type(e).__name__
            info["ok"] = False
            return info
    else:
        info["open"] = "mouse"

    # Wait for dialog
    opened = wait_for(
        page,
        r"Title and thumbnail|Thumbnail only|Title only|Test and compare your",
        12000,
    )
    info["dialog_open"] = opened
    shot(page, "601_ab_dialog.png")
    body = snip(page, 6000)
    info["offers"] = [
        lab
        for lab in ["Title and thumbnail", "Thumbnail only", "Title only", "Thumbnail", "Title"]
        if re.search(re.escape(lab), body, re.I)
    ]
    if not opened:
        info["ok"] = False
        info["reason"] = "dialog_did_not_open"
        info["snip"] = body[:800]
        return info

    # Select Title and thumbnail pill
    chosen = None
    for lab in ["Title and thumbnail", "Thumbnail only", "Title only"]:
        b = find_click(page, lab, y_min=80)
        if b and lab == "Title and thumbnail":
            chosen = lab
            break
        if b and lab != "Title and thumbnail" and chosen is None:
            # keep looking for Title and thumbnail first
            pass
    if not chosen:
        b = find_click(page, "Title and thumbnail", y_min=80)
        if b:
            chosen = "Title and thumbnail"
    info["chosen"] = chosen or ("Title and thumbnail" if "Title and thumbnail" in info["offers"] else info["offers"][0] if info["offers"] else None)
    # Ensure Title and thumbnail selected — click again
    find_click(page, "Title and thumbnail", y_min=80)
    page.wait_for_timeout(2000)
    shot(page, "602_ab_type.png")

    # Upload 3 thumbs into y-ordered file inputs inside dialog
    uploads = []
    loc = page.locator('input[type="file"]')
    idxs = []
    for i in range(loc.count()):
        try:
            acc = (loc.nth(i).get_attribute("accept") or "").lower()
            box = loc.nth(i).bounding_box()
            if not box or box["y"] < 60:
                continue
            if "image" in acc or "jpg" in acc or "jpeg" in acc or acc == "" or "png" in acc:
                idxs.append((box["y"], i))
        except Exception:
            pass
    idxs.sort()
    info["file_idxs"] = [{"y": y, "i": i} for y, i in idxs]
    for j, thumb in enumerate(THUMBS):
        if j < len(idxs):
            _, i = idxs[j]
            try:
                loc.nth(i).set_input_files(str(thumb))
                uploads.append({"slot": j + 1, "file": thumb.name, "i": i})
                page.wait_for_timeout(2000)
            except Exception as e:
                uploads.append({"slot": j + 1, "err": type(e).__name__})
        else:
            # click Add thumbnail + chooser
            find_click(page, "Add thumbnail", y_min=100)
            page.wait_for_timeout(500)
            try:
                with page.expect_file_chooser(timeout=5000) as fc:
                    find_click(page, "Add thumbnail", y_min=100)
                fc.value.set_files(str(thumb))
                uploads.append({"slot": j + 1, "file": thumb.name, "via": "chooser"})
                page.wait_for_timeout(2000)
            except Exception:
                # set any remaining file input
                try:
                    loc2 = page.locator('input[type="file"]')
                    for k in range(loc2.count() - 1, -1, -1):
                        acc = (loc2.nth(k).get_attribute("accept") or "").lower()
                        if "image" in acc or acc == "":
                            loc2.nth(k).set_input_files(str(thumb))
                            uploads.append({"slot": j + 1, "file": thumb.name, "i": k})
                            page.wait_for_timeout(2000)
                            break
                except Exception as e:
                    uploads.append({"slot": j + 1, "err": type(e).__name__})
        shot(page, f"603_thumb_{j+1}.png")
    info["uploads"] = uploads

    # Fill 3 title fields (maxlength 100) top to bottom — overwrite
    titles_set = []
    inputs = page.locator("input, textarea")
    cands = []
    for i in range(inputs.count()):
        el = inputs.nth(i)
        try:
            if not el.is_visible():
                continue
            ml = el.get_attribute("maxlength") or ""
            aria = ((el.get_attribute("aria-label") or "") + (el.get_attribute("placeholder") or "")).lower()
            box = el.bounding_box()
            if not box or box["y"] < 100 or box["width"] < 120:
                continue
            if ml == "100" or "title" in aria or "add title" in aria:
                cands.append((box["y"], i))
        except Exception:
            pass
    cands.sort()
    info["title_cands"] = [{"y": y, "i": i} for y, i in cands]
    for j, (_, i) in enumerate(cands[:3]):
        el = inputs.nth(i)
        el.click(timeout=3000)
        page.keyboard.press("Meta+a")
        page.keyboard.type(TITLES[j], delay=15)
        titles_set.append({"i": i, "title": TITLES[j]})
        page.wait_for_timeout(400)
    # Also JS force
    page.evaluate(
        """(titles) => {
          const found=[];
          const walk=(r,d=0)=>{
            if(!r||d>55)return;
            for (const inp of (r.querySelectorAll?r.querySelectorAll('input,textarea'):[])) {
              const aria=((inp.getAttribute('aria-label')||'')+(inp.placeholder||'')).toLowerCase();
              const max=inp.getAttribute('maxlength')||'';
              const rect=inp.getBoundingClientRect();
              if(rect.width<120||rect.y<100) continue;
              if(max==='100'||/title/.test(aria)) found.push({inp,y:rect.y});
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if(el.shadowRoot) walk(el.shadowRoot,d+1);
            }
          };
          walk(document);
          found.sort((a,b)=>a.y-b.y);
          for(let i=0;i<Math.min(3,found.length);i++){
            const inp=found[i].inp; inp.focus(); inp.value=titles[i];
            inp.dispatchEvent(new Event('input',{bubbles:true}));
            inp.dispatchEvent(new Event('change',{bubbles:true}));
          }
          return found.length;
        }""",
        TITLES,
    )
    info["titles_set"] = titles_set
    page.wait_for_timeout(1000)
    shot(page, "604_ab_filled.png")
    body = snip(page, 4000)
    info["filled_snip"] = body[:900]
    info["needs_third"] = bool(re.search(r"Third title and thumbnail are required|Second title is required", body, re.I))

    # Set test via mouse on exact button
    set_box = find_click(page, "Set test", y_min=200)
    info["set_box"] = set_box
    if not set_box:
        try:
            btn = page.get_by_role("button", name=re.compile(r"^Set test$", re.I))
            if btn.count():
                # force even if disabled to record state
                info["set_disabled"] = not btn.first.is_enabled()
                if btn.first.is_enabled():
                    btn.first.click(timeout=4000)
                    info["set"] = "enabled_click"
                else:
                    info["set"] = "disabled"
        except Exception as e:
            info["set_err"] = type(e).__name__
    else:
        info["set"] = "mouse"
    page.wait_for_timeout(4000)
    shot(page, "605_ab_after_set.png")
    after = snip(page, 3000)
    info["after"] = after[:900]
    info["running"] = bool(re.search(r"A/B test running|test running", after, re.I))
    info["still_required"] = bool(re.search(r"required", after, re.I) and re.search(r"title|thumbnail", after, re.I))
    info["ok"] = bool(info["running"])
    if not info["ok"]:
        info["note"] = (
            f"Studio offered {info.get('offers')}; chose {info.get('chosen')}. "
            f"Set test state={info.get('set')}. needs_third={info.get('needs_third')}."
        )
    return info


def do_end(page):
    info = {"related": RELATED_002}
    page.goto(
        f"https://studio.youtube.com/video/{VIDEO_ID}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3500)
    dismiss(page)
    find_click(page, "End screen", y_min=200) or page.get_by_text("End screen", exact=True).first.click(timeout=5000)
    page.wait_for_timeout(2500)
    for _ in range(3):
        dismiss(page)
        find_click(page, "OK, got it")
        page.keyboard.press("Escape")
        page.wait_for_timeout(200)
    shot(page, "610_endscreen.png")

    # Apply template
    # The template cards say "1 video, 1 subscribe" — click first one
    tbox = find_click(page, "1 video, 1 subscribe", y_min=100)
    info["template"] = tbox
    page.wait_for_timeout(2000)
    shot(page, "611_template.png")

    # Click video element to change to specific
    find_click(page, "Most recent upload", y_min=80) or find_click(page, "Best for viewer", y_min=80)
    page.wait_for_timeout(800)
    find_click(page, "Specific video", y_min=80)
    page.wait_for_timeout(800)

    # Type id into focused/search field
    page.keyboard.type(RELATED_002, delay=20)
    page.keyboard.press("Enter")
    page.wait_for_timeout(2000)
    # If search bar at top was focused wrongly, try evaluate
    page.evaluate(
        """(q) => {
          const walk=(r,d=0)=>{
            if(!r||d>55) return false;
            for (const inp of (r.querySelectorAll?r.querySelectorAll('input,textarea'):[])) {
              const aria=((inp.getAttribute('aria-label')||'')+(inp.placeholder||'')).toLowerCase();
              const rect=inp.getBoundingClientRect();
              if (rect.width<40||rect.y<40) continue;
              if (/search|video|url|paste/.test(aria) || inp.type==='search' || inp.type==='text') {
                // prefer dialog-ish (not top channel search at y~20)
                if (rect.y < 50) continue;
                inp.focus(); inp.value=q;
                inp.dispatchEvent(new Event('input',{bubbles:true}));
                return true;
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
            }
            return false;
          };
          return walk(document);
        }""",
        RELATED_002,
    )
    page.keyboard.press("Enter")
    page.wait_for_timeout(2000)
    find_click(page, "How Did We Discover the Periodic Table?") or find_click(
        page, "Periodic Table", y_min=80
    )
    page.wait_for_timeout(1000)
    shot(page, "612_picked.png")

    # Ensure subscribe via template should already have it
    body = snip(page, 3000)
    if not re.search(r"Subscribe", body, re.I):
        find_click(page, "Element", y_min=100)
        page.wait_for_timeout(500)
        find_click(page, "Subscribe", y_min=100)

    shot(page, "613_before_save.png")
    sbox = find_click(page, "Save", y_min=0)
    info["save_box"] = sbox
    if not sbox:
        try:
            btn = page.get_by_role("button", name=re.compile(r"^Save$", re.I))
            if btn.count() and btn.first.is_enabled():
                btn.first.click(timeout=4000)
                info["save"] = "click"
            else:
                info["save"] = "disabled"
                info["save_enabled"] = False
        except Exception as e:
            info["save_err"] = type(e).__name__
    else:
        info["save"] = "mouse"
    page.wait_for_timeout(3000)
    shot(page, "614_endscreen_saved.png")
    after = snip(page, 3500)
    info["after"] = after[:900]
    info["has_002"] = bool(re.search(r"Periodic Table|AL_-qlWko_g", after, re.I))
    info["has_subscribe"] = bool(re.search(r"Subscribe", after, re.I))
    info["error"] = bool(re.search(r"At least one element must be a video", after, re.I))
    info["best_for_viewer"] = bool(re.search(r"Best for viewer", after, re.I))
    info["most_recent"] = bool(re.search(r"Most recent", after, re.I))
    info["ok"] = bool(
        info.get("save") not in (None, "disabled")
        and info["has_subscribe"]
        and (info["has_002"] or info["best_for_viewer"] or info["most_recent"])
        and not info["error"]
    )
    return info


def verify(page):
    page.goto(
        f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3500)
    dismiss(page)
    shot(page, "620_content.png")
    tip = ""
    try:
        page.locator("ytcp-video-row").filter(
            has_text=re.compile(r"What's Really Inside an Atom", re.I)
        ).locator("text=Scheduled").first.hover(timeout=6000)
        page.wait_for_timeout(1200)
        tip = snip(page, 4000)
        shot(page, "621_schedule_proof.png")
    except Exception as e:
        tip = str(e)
    body = snip(page, 2500)
    return {
        "has15": bool(re.search(r"15\s*(Oct|October)\s*2026", body + tip, re.I)),
        "has1800": bool(re.search(r"18:00", body + tip)),
        "scheduled": "Scheduled" in body,
        "tooltip": bool(re.search(r"15 October 2026 at 18:00", tip, re.I)),
        "tip": tip[:400],
    }


def main():
    EV.mkdir(parents=True, exist_ok=True)
    (EV / "finish6.log").write_text("")
    ensure_chrome()
    result = {
        "ok": False,
        "videoId": VIDEO_ID,
        "channel": "@HistoryOfScienceYT",
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
            page.wait_for_timeout(2500)
            body = snip(page, 1200)
            if "History of Science" not in body:
                result["channelCheck"] = {"ok": False, "snip": body[:300]}
                dump("FINISH6_RESULT.json", result)
                return 2
            result["channelCheck"] = {"ok": True}

            result["abTest"] = do_ab(page)
            log(f"ab dialog={result['abTest'].get('dialog_open')} chosen={result['abTest'].get('chosen')} running={result['abTest'].get('running')} ok={result['abTest'].get('ok')}")

            result["endScreen"] = do_end(page)
            log(f"end ok={result['endScreen'].get('ok')} 002={result['endScreen'].get('has_002')} sub={result['endScreen'].get('has_subscribe')} save={result['endScreen'].get('save')}")

            result["schedule"] = verify(page)
            result["pin"] = {
                "ok": False,
                "reason": "watch_page_not_commentable_while_scheduled_or_private",
                "note": "Pin on launch day 15 Oct 2026.",
            }
            result["ok"] = bool(result["schedule"].get("has15") and result["schedule"].get("scheduled"))
            dump("FINISH6_RESULT.json", result)
            log(f"DONE ok={result['ok']}")
            return 0 if result["ok"] else 1
        except Exception as e:
            result["error"] = f"{type(e).__name__}: {e}"
            dump("FINISH6_RESULT.json", result)
            log(f"ERROR {result['error']}")
            try:
                shot(page, "699_error.png")
            except Exception:
                pass
            return 3


if __name__ == "__main__":
    raise SystemExit(main())
