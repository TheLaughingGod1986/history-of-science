#!/usr/bin/env python3
"""HOS 004 finish pass 4: complete Title+thumbnail T&C 3 pairs + bind end screen to 002.
CDP :9460 · HOS profile only. No .env."""
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
HANDLE = "@HistoryOfScienceYT"
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
    with (EV / "finish4.log").open("a") as f:
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
        with urllib.request.urlopen(f"{CDP}/json/version", timeout=2) as r:
            return r.status == 200
    except Exception:
        return False


def ensure_chrome() -> None:
    if chrome_up():
        log("cdp already up")
        return
    Path(PROFILE).mkdir(parents=True, exist_ok=True)
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
        stdout=open("/tmp/hos_chrome_9460_004_finish4.log", "ab"),
        stderr=subprocess.STDOUT,
    )
    for _ in range(50):
        if chrome_up():
            log("cdp started")
            return
        time.sleep(0.5)
    raise SystemExit("CDP :9460 failed to start")


def dismiss(page) -> None:
    for name in [
        "Got it",
        "OK, got it",
        "Dismiss",
        "Not now",
        "No thanks",
        "Skip",
        "Close",
        "Cancel",
    ]:
        try:
            b = page.get_by_role("button", name=re.compile(rf"^{re.escape(name)}$", re.I))
            if b.count() and b.first.is_visible():
                b.first.click(timeout=1200)
                page.wait_for_timeout(250)
        except Exception:
            pass
    # Feedback dialogs
    try:
        page.keyboard.press("Escape")
        page.wait_for_timeout(200)
        page.keyboard.press("Escape")
    except Exception:
        pass


def click_text(page, pattern: str, y_min: int = 0) -> str | None:
    try:
        hit = page.evaluate(
            """([pattern, yMin]) => {
              const re = new RegExp(pattern, 'i');
              const walk = (root, depth=0) => {
                if (!root || depth > 50) return null;
                const nodes = root.querySelectorAll
                  ? root.querySelectorAll('button, a, [role="button"], [role="radio"], [role="option"], ytcp-button, tp-yt-paper-button, span, div, yt-formatted-string')
                  : [];
                for (const el of nodes) {
                  const t = (el.innerText || el.textContent || '').trim().replace(/\\s+/g, ' ');
                  if (!t || t.length > 100) continue;
                  if (!re.test(t)) continue;
                  const r = el.getBoundingClientRect();
                  if (r.width < 4 || r.height < 4 || r.y < yMin) continue;
                  el.click();
                  return t.slice(0, 90) + '@' + Math.round(r.x) + ',' + Math.round(r.y);
                }
                for (const el of (root.querySelectorAll ? root.querySelectorAll('*') : [])) {
                  if (el.shadowRoot) {
                    const h = walk(el.shadowRoot, depth + 1);
                    if (h) return h;
                  }
                }
                return null;
              };
              return walk(document);
            }""",
            [pattern, y_min],
        )
        if hit:
            page.wait_for_timeout(700)
            return hit
    except Exception:
        pass
    try:
        loc = page.get_by_role("button", name=re.compile(pattern, re.I))
        if loc.count():
            loc.first.click(timeout=4000)
            page.wait_for_timeout(700)
            return "role:" + pattern
    except Exception:
        pass
    return None


def open_ab(page) -> dict:
    info: dict = {}
    page.goto(
        f"https://studio.youtube.com/video/{VIDEO_ID}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(4000)
    dismiss(page)
    shot(page, "400_edit.png")
    # Exact A/B Testing under title
    hit = page.evaluate(
        """() => {
          const walk = (root, depth=0) => {
            if (!root || depth > 50) return null;
            for (const el of (root.querySelectorAll
              ? root.querySelectorAll('button, a, [role="button"], ytcp-button')
              : [])) {
              const t = (el.innerText || el.textContent || '').trim().replace(/\\s+/g, ' ');
              if (t !== 'A/B Testing' && t !== 'Test & Compare') continue;
              const r = el.getBoundingClientRect();
              if (r.y < 100 || r.width < 10) continue;
              el.click();
              return t + '@' + Math.round(r.x) + ',' + Math.round(r.y);
            }
            for (const el of (root.querySelectorAll ? root.querySelectorAll('*') : [])) {
              if (el.shadowRoot) {
                const h = walk(el.shadowRoot, depth + 1);
                if (h) return h;
              }
            }
            return null;
          };
          return walk(document);
        }"""
    )
    info["open"] = hit
    page.wait_for_timeout(2500)
    dismiss(page)
    shot(page, "401_ab_open.png")
    body = snip(page, 5000)
    info["snip"] = body[:1200]
    # If already mid-setup, continue; else pick Title and thumbnail
    if re.search(r"Title and thumbnail|What do you want to test|Choose what", body, re.I):
        if click_text(page, r"^Title and thumbnail$"):
            info["chosen"] = "Title and thumbnail"
            page.wait_for_timeout(2000)
    if re.search(r"Set test|Third title|Add thumbnail|variant", body, re.I) or re.search(
        r"Title and thumbnail", body, re.I
    ):
        info["dialog"] = True
    shot(page, "402_ab_ready.png")
    return info


def fill_ab_pairs(page) -> dict:
    info: dict = {"pairs": []}
    # Collect image file inputs + title inputs inside dialog
    meta = page.evaluate(
        """() => {
          const files = [];
          const titles = [];
          const walk = (root, depth=0) => {
            if (!root || depth > 50) return;
            for (const inp of (root.querySelectorAll ? root.querySelectorAll('input[type=file]') : [])) {
              const acc = (inp.accept || '').toLowerCase();
              const r = inp.getBoundingClientRect();
              files.push({acc, y: r.y, w: r.width, h: r.height});
            }
            for (const inp of (root.querySelectorAll
              ? root.querySelectorAll('input, textarea, [contenteditable=true]')
              : [])) {
              const aria = ((inp.getAttribute('aria-label')||'')
                +(inp.placeholder||'')+(inp.getAttribute('label')||'')).toLowerCase();
              const max = inp.getAttribute('maxlength') || '';
              const r = inp.getBoundingClientRect();
              if (r.width < 40 || r.y < 80) continue;
              if (/title/.test(aria) || max === '100') {
                const val = inp.value !== undefined ? inp.value : (inp.innerText||'');
                titles.push({aria: aria.slice(0,60), max, y: r.y, val: (val||'').slice(0,80)});
              }
            }
            for (const el of (root.querySelectorAll ? root.querySelectorAll('*') : [])) {
              if (el.shadowRoot) walk(el.shadowRoot, depth + 1);
            }
          };
          walk(document);
          files.sort((a,b)=>a.y-b.y);
          titles.sort((a,b)=>a.y-b.y);
          return {files, titles};
        }"""
    )
    info["meta"] = meta

    # Set files by y-order
    try:
        loc = page.locator('input[type="file"]')
        image_idxs = []
        for i in range(loc.count()):
            acc = (loc.nth(i).get_attribute("accept") or "").lower()
            # include empty accept (Studio sometimes omits)
            if "image" in acc or "jpeg" in acc or "jpg" in acc or acc == "" or "png" in acc:
                box = loc.nth(i).bounding_box()
                if box and box["y"] > 60:
                    image_idxs.append((box["y"], i))
        image_idxs.sort()
        info["image_idxs"] = [{"y": y, "i": i} for y, i in image_idxs]
        for j, thumb in enumerate(THUMBS):
            if j >= len(image_idxs):
                break
            _, i = image_idxs[j]
            loc.nth(i).set_input_files(str(thumb))
            info["pairs"].append({"slot": j + 1, "thumb": thumb.name, "input": i})
            page.wait_for_timeout(1800)
            shot(page, f"403_thumb_slot{j+1}.png")
    except Exception as e:
        info["file_err"] = f"{type(e).__name__}: {e}"

    # Overwrite title fields top-to-bottom with our 3 titles
    titles_set = page.evaluate(
        """(titles) => {
          const inputs = [];
          const walk = (root, depth=0) => {
            if (!root || depth > 50) return;
            for (const inp of (root.querySelectorAll
              ? root.querySelectorAll('input, textarea, [contenteditable=true]')
              : [])) {
              const aria = ((inp.getAttribute('aria-label')||'')
                +(inp.placeholder||'')+(inp.getAttribute('label')||'')).toLowerCase();
              const max = inp.getAttribute('maxlength') || '';
              const r = inp.getBoundingClientRect();
              if (r.width < 80 || r.y < 80) continue;
              if (/title/.test(aria) || max === '100') {
                inputs.push({el: inp, y: r.y});
              }
            }
            for (const el of (root.querySelectorAll ? root.querySelectorAll('*') : [])) {
              if (el.shadowRoot) walk(el.shadowRoot, depth + 1);
            }
          };
          walk(document);
          inputs.sort((a,b)=>a.y-b.y);
          const out = [];
          for (let i=0; i<Math.min(titles.length, inputs.length); i++) {
            const inp = inputs[i].el;
            const title = titles[i];
            inp.focus();
            if (inp.isContentEditable) {
              inp.innerText = title;
            } else {
              inp.value = title;
            }
            inp.dispatchEvent(new Event('input', {bubbles:true}));
            inp.dispatchEvent(new Event('change', {bubbles:true}));
            out.push({y: inputs[i].y, title});
          }
          return out;
        }""",
        TITLES,
    )
    info["titles_set"] = titles_set
    # Also type via Playwright into each title box for reliability
    try:
        boxes = page.get_by_role("textbox")
        title_boxes = []
        for i in range(boxes.count()):
            try:
                aria = (boxes.nth(i).get_attribute("aria-label") or "").lower()
                ph = (boxes.nth(i).get_attribute("placeholder") or "").lower()
                ml = boxes.nth(i).get_attribute("maxlength") or ""
                if "title" in aria or "title" in ph or ml == "100":
                    box = boxes.nth(i).bounding_box()
                    if box and box["y"] > 80:
                        title_boxes.append((box["y"], i))
            except Exception:
                pass
        title_boxes.sort()
        for j, (_, i) in enumerate(title_boxes[:3]):
            boxes.nth(i).click(timeout=3000)
            boxes.nth(i).fill(TITLES[j])
            page.wait_for_timeout(400)
        info["pw_titles"] = [{"i": i, "title": TITLES[j]} for j, (_, i) in enumerate(title_boxes[:3])]
    except Exception as e:
        info["pw_titles_err"] = type(e).__name__

    page.wait_for_timeout(1500)
    shot(page, "404_ab_filled.png")
    body = snip(page, 3000)
    info["filled_snip"] = body[:1000]
    info["needs_third"] = bool(re.search(r"Third title and thumbnail are required", body, re.I))

    # Click Add thumbnail on empty slot if present
    if info["needs_third"] or re.search(r"Add thumbnail", body, re.I):
        click_text(page, r"^Add thumbnail$")
        page.wait_for_timeout(1000)
        # set last file input to B
        try:
            loc = page.locator('input[type="file"]')
            for i in range(loc.count() - 1, -1, -1):
                acc = (loc.nth(i).get_attribute("accept") or "").lower()
                if "image" in acc or "jpeg" in acc or acc == "":
                    loc.nth(i).set_input_files(str(THUMBS[2]))
                    info["add_thumbnail_b"] = True
                    page.wait_for_timeout(1800)
                    break
        except Exception as e:
            info["add_thumb_err"] = type(e).__name__
        # ensure title 3
        try:
            page.evaluate(
                """(title) => {
                  const walk=(r,d=0)=>{
                    if(!r||d>50) return false;
                    for (const inp of (r.querySelectorAll?r.querySelectorAll('input,textarea'):[])) {
                      const aria=((inp.getAttribute('aria-label')||'')+(inp.placeholder||'')).toLowerCase();
                      const max=inp.getAttribute('maxlength')||'';
                      if (!(/title/.test(aria) || max==='100')) continue;
                      if (!(inp.value||'').trim()) {
                        inp.focus(); inp.value=title;
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
                TITLES[2],
            )
        except Exception:
            pass
        page.wait_for_timeout(1000)
        shot(page, "405_ab_third.png")

    body2 = snip(page, 2500)
    info["before_set_snip"] = body2[:800]
    # Set test
    set_hit = click_text(page, r"^Set test$") or click_text(page, r"^Start test$") or click_text(
        page, r"^Save$"
    )
    info["set"] = set_hit
    page.wait_for_timeout(3500)
    dismiss(page)
    shot(page, "406_ab_after_set.png")
    after = snip(page, 2500)
    info["after"] = after[:1000]
    info["running"] = bool(re.search(r"A/B test running|test running", after, re.I))
    info["still_required"] = bool(
        re.search(r"Third title and thumbnail are required", after, re.I)
    )
    info["ok"] = bool(info["running"] or (info.get("set") and not info["still_required"]))
    return info


def fix_end_screen(page) -> dict:
    info: dict = {"related": RELATED_002}
    page.goto(
        f"https://studio.youtube.com/video/{VIDEO_ID}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3000)
    dismiss(page)
    # Open end screen
    opened = click_text(page, r"^End screen$", y_min=100)
    if not opened:
        page.goto(
            f"https://studio.youtube.com/video/{VIDEO_ID}/editor",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(3000)
        opened = click_text(page, r"End screen", y_min=80)
    info["open"] = opened
    page.wait_for_timeout(2500)
    dismiss(page)
    shot(page, "410_endscreen.png")

    # Dismiss feedback overlays aggressively
    for _ in range(3):
        dismiss(page)
        click_text(page, r"^OK, got it$")
        page.keyboard.press("Escape")
        page.wait_for_timeout(300)

    body = snip(page, 3000)
    info["open_snip"] = body[:700]

    # Click the video element (Best for viewer / Most recent)
    for pat in [
        r"Best for viewer",
        r"Most recent upload",
        r"Video: Best",
        r"Video: Most",
        r"^Video$",
    ]:
        if click_text(page, pat):
            info["clicked"] = pat
            page.wait_for_timeout(1200)
            break

    shot(page, "411_video_el.png")

    # Specific video
    for pat in [r"Specific video", r"Choose a specific video", r"Select a specific video"]:
        if click_text(page, pat):
            info["mode"] = pat
            page.wait_for_timeout(1000)
            break

    # Paste video id into search / URL field
    try:
        filled = page.evaluate(
            """(q) => {
              const candidates = [];
              const walk=(r,d=0)=>{
                if(!r||d>50) return;
                for (const inp of (r.querySelectorAll?r.querySelectorAll('input,textarea'):[])) {
                  const aria=((inp.getAttribute('aria-label')||'')
                    +(inp.placeholder||'')+(inp.type||'')).toLowerCase();
                  const rect=inp.getBoundingClientRect();
                  if (rect.width < 40 || rect.y < 60) continue;
                  if (/search|video|url|paste|id/.test(aria) || inp.type==='search' || inp.type==='text' || inp.type==='url') {
                    candidates.push({inp, y: rect.y, aria});
                  }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                  if (el.shadowRoot) walk(el.shadowRoot,d+1);
                }
              };
              walk(document);
              candidates.sort((a,b)=>a.y-b.y);
              if (!candidates.length) return null;
              const inp = candidates[0].inp;
              inp.focus();
              inp.value = q;
              inp.dispatchEvent(new Event('input',{bubbles:true}));
              return {aria: candidates[0].aria, y: candidates[0].y};
            }""",
            RELATED_002,
        )
        info["fill"] = filled
        page.keyboard.press("Enter")
        page.wait_for_timeout(2200)
    except Exception as e:
        info["fill_err"] = type(e).__name__

    # Also try title search if id didn't work
    if not click_text(page, r"Periodic Table|How Did We Discover the Periodic"):
        try:
            page.evaluate(
                """(q) => {
                  const walk=(r,d=0)=>{
                    if(!r||d>50) return false;
                    for (const inp of (r.querySelectorAll?r.querySelectorAll('input,textarea'):[])) {
                      const rect=inp.getBoundingClientRect();
                      if (rect.width < 60) continue;
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
            click_text(page, r"Periodic Table|How Did We Discover")
        except Exception:
            pass

    info["picked"] = bool(
        re.search(r"Periodic Table|AL_-qlWko_g", snip(page, 2500), re.I)
    )
    shot(page, "412_picked.png")

    # Ensure Subscribe present
    body2 = snip(page, 2500)
    if not re.search(r"Subscribe", body2, re.I):
        click_text(page, r"^\+?\s*Element$|Add element")
        page.wait_for_timeout(600)
        click_text(page, r"^Subscribe$")
        page.wait_for_timeout(800)

    shot(page, "413_before_save.png")
    save = click_text(page, r"^Save$")
    if not save:
        try:
            page.get_by_role("button", name=re.compile(r"^Save$", re.I)).first.click(timeout=4000)
            save = "Save"
        except Exception:
            pass
    info["save"] = save
    page.wait_for_timeout(2500)
    click_text(page, r"^Save$|^Confirm$")
    page.wait_for_timeout(1500)
    dismiss(page)
    shot(page, "414_endscreen_saved.png")
    after = snip(page, 3000)
    info["after"] = after[:900]
    info["has_002"] = bool(
        re.search(r"AL_-qlWko_g|Periodic Table|How Did We Discover the Periodic", after, re.I)
    )
    info["has_subscribe"] = bool(re.search(r"Subscribe", after, re.I))
    info["best_for_viewer"] = bool(re.search(r"Best for viewer", after, re.I))
    info["most_recent"] = bool(re.search(r"Most recent upload", after, re.I))
    info["ok"] = bool(info.get("save") and info["has_subscribe"] and info["has_002"])
    if not info["has_002"]:
        info["note"] = (
            "Could not confirm Specific video AL_-qlWko_g after save. "
            f"best_for_viewer={info['best_for_viewer']} most_recent={info['most_recent']}"
        )
    return info


def verify_schedule(page) -> dict:
    page.goto(
        f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3500)
    dismiss(page)
    shot(page, "420_content.png")
    body = snip(page, 4000)
    tip = ""
    try:
        # Prefer visibility cell near atom title
        page.locator("ytcp-video-row").filter(
            has_text=re.compile(r"What's Really Inside an Atom", re.I)
        ).locator("text=Scheduled").first.hover(timeout=6000)
        page.wait_for_timeout(1200)
        tip = snip(page, 4000)
        shot(page, "421_schedule_tooltip.png")
    except Exception:
        try:
            page.get_by_text(re.compile(r"^Scheduled$", re.I)).first.hover(timeout=5000)
            page.wait_for_timeout(1200)
            tip = snip(page, 4000)
            shot(page, "421_schedule_tooltip.png")
        except Exception as e:
            tip = f"<hover {type(e).__name__}>"
    text = body + "\n" + tip
    return {
        "has15": bool(re.search(r"15\s*(Oct|October)\s*2026", text, re.I)),
        "has1800": bool(re.search(r"18:00", text)),
        "scheduled": bool(re.search(r"Scheduled", body, re.I)),
        "tooltip": bool(
            re.search(r"15 October 2026 at 18:00|15 Oct 2026", tip, re.I)
        ),
        "body_snip": body[:600],
        "tip_snip": tip[:600],
    }


def ensure_hos(page) -> dict:
    page.goto(
        f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3000)
    dismiss(page)
    body = snip(page, 2000)
    ok = CHANNEL in page.url and "History of Science" in body and "Sign in" not in body
    return {"ok": ok, "url": page.url, "snip": body[:300]}


def main() -> int:
    EV.mkdir(parents=True, exist_ok=True)
    (EV / "finish4.log").write_text("")
    ensure_chrome()
    result: dict = {
        "ok": False,
        "videoId": VIDEO_ID,
        "channel": HANDLE,
        "at": datetime.now().isoformat(timespec="seconds"),
    }
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        ctx = browser.contexts[0]
        page = ctx.pages[0] if ctx.pages else ctx.new_page()

        def _dlg(d):
            try:
                log(f"dialog {d.type}: {d.message[:100]}")
                d.accept()
            except Exception:
                pass

        page.on("dialog", _dlg)
        try:
            hos = ensure_hos(page)
            result["channelCheck"] = hos
            if not hos.get("ok"):
                dump("FINISH4_RESULT.json", result)
                return 2

            result["abOpen"] = open_ab(page)
            log(f"abOpen={result['abOpen'].get('open')} chosen={result['abOpen'].get('chosen')}")
            result["abTest"] = fill_ab_pairs(page)
            log(
                f"abTest ok={result['abTest'].get('ok')} running={result['abTest'].get('running')} "
                f"set={result['abTest'].get('set')} still={result['abTest'].get('still_required')}"
            )

            result["endScreen"] = fix_end_screen(page)
            log(
                f"endScreen ok={result['endScreen'].get('ok')} 002={result['endScreen'].get('has_002')} "
                f"sub={result['endScreen'].get('has_subscribe')} bfv={result['endScreen'].get('best_for_viewer')}"
            )

            result["schedule"] = verify_schedule(page)
            shot(page, "430_final.png")
            result["ok"] = bool(
                result["channelCheck"].get("ok")
                and result["schedule"].get("has15")
                and result["schedule"].get("scheduled")
            )
            result["pin"] = {
                "ok": False,
                "reason": "watch_page_not_commentable_while_scheduled_or_private",
                "note": "Pin on launch day 15 Oct 2026.",
                "text": (PKG / "Pinned-Comments/atom_long_pinned-comment_v01.txt")
                .read_text()
                .strip()[:140],
            }
            dump("FINISH4_RESULT.json", result)
            log(f"DONE ok={result['ok']}")
            return 0 if result["ok"] else 1
        except Exception as e:
            result["error"] = f"{type(e).__name__}: {e}"
            dump("FINISH4_RESULT.json", result)
            log(f"ERROR {result['error']}")
            try:
                shot(page, "499_error.png")
            except Exception:
                pass
            return 3


if __name__ == "__main__":
    raise SystemExit(main())
