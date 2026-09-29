#!/usr/bin/env python3
"""HOS 004 Studio phone-UAT fix (29 Sep 18:51).

Ben (Studio app): auto thumb, no Altered label, date shows 30 Sep.
Fix via CDP :9460 / HOS Chrome profile — no .env / no API / never Orbit.

1. Upload custom thumbnail A v04 on Details
2. Test & Compare: Title and thumbnail · 3 pairs (A/C/B thumbs + 3 titles)
3. Altered content = YES (made with AI / synthetic)
4. Visibility schedule = Thu 15 Oct 2026 18:00 Europe/London (17:00Z), NOT Premiere, NOT 30 Sep
5. End screen: Specific video 002 (AL_-qlWko_g) + Subscribe
6. Pin comment if Studio allows (else record defer-to-launch)
Screenshot Visibility panel. No Shorts upload.
"""
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
RELATED_002 = "AL_-qlWko_g"
RELATED_TITLE = "How Did We Discover the Periodic Table?"
TITLES = [
    "What's Really Inside an Atom?",
    "Why Is the Periodic Table in This Order?",
    "How Small Can You Cut Gold?",
]
SCHED_DAY = "15"
SCHED_MONTH = "Oct"
SCHED_DATE_LABEL = "15 October 2026"
SCHED_TIME = "18:00"
PROJ = Path(__file__).resolve().parents[2]
PKG = PROJ / "11_Upload-Package"
EV = PKG / "Schedule/evidence_2026-09-29_studio"
ART = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts/hos004_studio_phone_uat"
THUMB_A = PROJ / "08_Thumbnail/Selected/hos_004_thumb_A_atom_live_v04.jpg"
THUMB_B = PROJ / "08_Thumbnail/Selected/hos_004_thumb_B_cut_gold_live_v04.jpg"
THUMB_C = PROJ / "08_Thumbnail/Selected/hos_004_thumb_C_hidden_number_live_v06.jpg"
THUMBS = [THUMB_A, THUMB_C, THUMB_B]  # slots 1/2/3 per PACKAGE_MANIFEST
PIN_TXT = PKG / "Pinned-Comments/atom_long_pinned-comment_v01.txt"


def log(m: str) -> None:
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    line = f"{datetime.now().isoformat(timespec='seconds')} {m}"
    print(line, flush=True)
    with (EV / "phone_uat_fix.log").open("a") as f:
        f.write(line + "\n")


def dump(n, o):
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    (EV / n).write_text(json.dumps(o, indent=2) + "\n")
    (ART / n).write_text(json.dumps(o, indent=2) + "\n")


def shot(page, n):
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    p = EV / n
    page.screenshot(path=str(p), full_page=False)
    try:
        (ART / n).write_bytes(p.read_bytes())
    except Exception:
        pass
    return str(p)


def snip(page, n=6000):
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
            f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload",
        ],
        stdout=open("/tmp/hos_chrome_phone_uat.log", "ab"),
        stderr=subprocess.STDOUT,
    )
    for _ in range(60):
        if chrome_up():
            return
        time.sleep(0.5)
    raise SystemExit("cdp fail")


def dismiss(page):
    for name in [
        "OK, got it",
        "Got it",
        "Dismiss",
        "Close",
        "Cancel",
        "Not now",
        "No thanks",
        "Skip",
    ]:
        try:
            b = page.get_by_role("button", name=re.compile(rf"^{re.escape(name)}$", re.I))
            if b.count() and b.first.is_visible(timeout=350):
                b.first.click(timeout=700)
        except Exception:
            pass
    try:
        page.keyboard.press("Escape")
    except Exception:
        pass


def find_click(page, text: str, y_min=0, exact=True):
    box = page.evaluate(
        """([text, yMin, exact]) => {
          const walk = (root, depth=0) => {
            if (!root || depth > 55) return null;
            const sels = 'button, a, [role="button"], [role="radio"], [role="tab"], [role="option"], ytcp-button, span, div, yt-formatted-string, tp-yt-paper-item, tp-yt-paper-radio-button';
            for (const el of (root.querySelectorAll ? root.querySelectorAll(sels) : [])) {
              const t = (el.innerText || el.textContent || '').trim().replace(/\\s+/g, ' ');
              const ok = exact ? (t === text) : t.includes(text);
              if (!ok) continue;
              const r = el.getBoundingClientRect();
              if (r.width < 4 || r.height < 4 || r.y < yMin) continue;
              return {x: r.x + r.width/2, y: r.y + r.height/2, w: r.width, h: r.height, t};
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
        [text, y_min, exact],
    )
    if not box:
        return None
    page.mouse.click(box["x"], box["y"])
    page.wait_for_timeout(700)
    return box


def wait_re(page, pattern, ms=12000):
    t0 = time.time()
    while time.time() - t0 < ms / 1000:
        if re.search(pattern, snip(page, 9000), re.I):
            return True
        page.wait_for_timeout(250)
    return False


def goto_edit(page):
    page.goto(
        f"https://studio.youtube.com/video/{VIDEO_ID}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(4000)
    dismiss(page)


def save_details(page) -> bool:
    for _ in range(3):
        box = find_click(page, "Save", y_min=0)
        if box:
            page.wait_for_timeout(2500)
            dismiss(page)
            return True
        try:
            btn = page.get_by_role("button", name=re.compile(r"^Save$", re.I))
            if btn.count() and btn.first.is_enabled():
                btn.first.click(timeout=4000)
                page.wait_for_timeout(2500)
                return True
        except Exception:
            pass
        page.wait_for_timeout(500)
    return False


def upload_custom_thumb(page) -> dict:
    info: dict = {"file": THUMB_A.name}
    goto_edit(page)
    shot(page, "uat_01_edit_before_thumb.png")
    body0 = snip(page, 3000)
    info["before_snip"] = body0[:400]

    # Prefer file input with image accept on details
    uploaded = False
    loc = page.locator('input[type="file"]')
    for i in range(loc.count()):
        try:
            acc = (loc.nth(i).get_attribute("accept") or "").lower()
            if "image" in acc or "jpg" in acc or "jpeg" in acc or "png" in acc:
                loc.nth(i).set_input_files(str(THUMB_A))
                uploaded = True
                info["via"] = f"input_{i}"
                page.wait_for_timeout(2500)
                break
        except Exception as e:
            info[f"input_{i}_err"] = type(e).__name__
    if not uploaded:
        for label in ["Upload file", "Upload thumbnail", "Custom thumbnail", "Edit"]:
            try:
                with page.expect_file_chooser(timeout=4000) as fc:
                    hit = find_click(page, label, y_min=80, exact=False)
                    if not hit:
                        page.get_by_text(re.compile(label, re.I)).first.click(timeout=2000)
                fc.value.set_files(str(THUMB_A))
                uploaded = True
                info["via"] = f"chooser:{label}"
                page.wait_for_timeout(2500)
                break
            except Exception:
                continue
    info["uploaded"] = uploaded
    shot(page, "uat_02_after_thumb_a.png")
    saved = save_details(page)
    info["saved"] = saved
    page.wait_for_timeout(2000)
    shot(page, "uat_03_thumb_saved.png")
    info["after_snip"] = snip(page, 2000)[:500]
    info["ok"] = uploaded
    return info


def set_altered_yes(page) -> dict:
    info: dict = {"wanted": "YES altered/synthetic / made with AI"}
    goto_edit(page)
    # Scroll toward bottom where Altered content lives
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(800)
    page.mouse.wheel(0, 2000)
    page.wait_for_timeout(800)
    shot(page, "uat_10_before_altered.png")
    body = snip(page, 8000)
    info["has_section"] = bool(re.search(r"Altered content|altered or synthetic|synthetic media", body, re.I))

    # Open the Altered content control
    opened = False
    for label in [
        "Altered content",
        "Does this video contain altered or synthetic content?",
        "Select an option",
        "Tell us if your video contains",
    ]:
        box = find_click(page, label, y_min=200, exact=False)
        if box:
            opened = True
            info["open"] = label
            break
    if not opened:
        # try role combobox near Altered
        try:
            page.get_by_text(re.compile(r"Altered content", re.I)).first.click(timeout=4000)
            opened = True
            info["open"] = "get_by_text"
        except Exception as e:
            info["open_err"] = type(e).__name__
    page.wait_for_timeout(1200)
    shot(page, "uat_11_altered_open.png")

    # Choose YES
    yes_hit = None
    for label in [
        "Yes",
        "Yes, it has altered or synthetic content",
        "Yes, this video has altered content",
        "Made with AI",
    ]:
        box = find_click(page, label, y_min=100, exact=True)
        if box:
            yes_hit = label
            break
        box = find_click(page, label, y_min=100, exact=False)
        if box:
            yes_hit = label
            break
    if not yes_hit:
        # radio by role
        try:
            r = page.get_by_role("radio", name=re.compile(r"^Yes", re.I))
            if r.count():
                r.first.click(timeout=3000)
                yes_hit = "role:Yes"
        except Exception as e:
            info["yes_err"] = type(e).__name__
    info["yes"] = yes_hit
    page.wait_for_timeout(1000)
    shot(page, "uat_12_altered_yes.png")

    # Some UIs ask for disclosure subtype — pick AI-generated if offered
    for label in [
        "Yes, it contains realistic altered or synthetic content",
        "Altered or synthetic content",
        "Made with generative AI",
        "Generated with AI",
    ]:
        find_click(page, label, y_min=100, exact=False)

    saved = save_details(page)
    info["saved"] = saved
    page.wait_for_timeout(2000)
    shot(page, "uat_13_altered_saved.png")
    after = snip(page, 6000)
    info["after_snip"] = after[:800]
    info["ok"] = bool(
        yes_hit
        and (
            re.search(r"\bYes\b", after, re.I)
            or re.search(r"altered or synthetic|Contains altered", after, re.I)
        )
    )
    if not info["ok"]:
        info["note"] = "Could not confirm Altered=YES in UI text after save — check screenshots."
    return info


def fix_schedule(page) -> dict:
    """Open Visibility / Content schedule popover; set 15 Oct 2026 18:00 UK; prove panel."""
    info: dict = {
        "wanted": "2026-10-15T17:00:00.000Z / Thu 15 Oct 2026 18:00 Europe/London",
        "not": "30 September 2026",
        "premiere": False,
    }
    # Prefer Content list Visibility chip (reliable in prior DATE_FIX)
    page.goto(
        f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(4500)
    dismiss(page)
    shot(page, "uat_20_content.png")

    # Hover / click Scheduled or Visibility on the atom row
    row_hit = page.evaluate(
        """() => {
          const walk=(root,d=0)=>{
            if(!root||d>50) return null;
            for (const el of (root.querySelectorAll?root.querySelectorAll('a,ytcp-video-row,tr,div'):[])) {
              const t=(el.innerText||'').replace(/\\s+/g,' ');
              if (!/What.?s Really Inside an Atom/i.test(t)) continue;
              if (t.length > 800) continue;
              const r=el.getBoundingClientRect();
              if (r.width<40||r.height<20) continue;
              return {x:r.x+r.width/2,y:r.y+Math.min(40,r.height/2), t:t.slice(0,180)};
            }
            for (const el of (root.querySelectorAll?root.querySelectorAll('*'):[])) {
              if (el.shadowRoot) { const h=walk(el.shadowRoot,d+1); if(h) return h; }
            }
            return null;
          };
          return walk(document);
        }"""
    )
    info["row"] = row_hit
    # Click "Scheduled" text near the video
    sched_box = find_click(page, "Scheduled", y_min=120)
    info["scheduled_chip"] = sched_box
    if not sched_box:
        # try Visibility column Private/Scheduled via row
        find_click(page, "Private", y_min=120)
    page.wait_for_timeout(1500)
    shot(page, "uat_21_vis_popover.png")

    # Expand Schedule / Edit schedule
    for label in [
        "Schedule",
        "Edit schedule",
        "Schedule as public",
        "Select a date to make your video public",
    ]:
        if find_click(page, label, y_min=80, exact=False):
            info["expand"] = label
            page.wait_for_timeout(1000)
            break
    shot(page, "uat_22_schedule_expanded.png")
    body = snip(page, 5000)
    info["panel_before"] = body[:900]
    info["had_30_sep"] = bool(re.search(r"30\s*(Sept|Sep|September).*2026|2026-09-30", body, re.I))
    info["had_15_oct"] = bool(re.search(r"15\s*(Oct|October).*2026", body, re.I))

    # Type date
    date_str = f"{SCHED_DAY} {SCHED_MONTH} 2026"
    typed = False
    for sel in [
        'tp-yt-paper-input[aria-label="Enter date"] input',
        'input[aria-label="Enter date"]',
        'input[placeholder*="date" i]',
    ]:
        el = page.locator(sel)
        if el.count():
            try:
                el.first.click(force=True)
                page.keyboard.press("Meta+a")
                page.keyboard.type(date_str, delay=30)
                page.keyboard.press("Enter")
                typed = True
                info["date_typed"] = date_str
                page.wait_for_timeout(600)
                break
            except Exception as e:
                info["date_err"] = type(e).__name__
    if not typed:
        # JS find date-looking input
        page.evaluate(
            """(dateStr) => {
              const walk=(r,d=0)=>{
                if(!r||d>55) return false;
                for (const inp of (r.querySelectorAll?r.querySelectorAll('input'):[])) {
                  const aria=((inp.getAttribute('aria-label')||'')+(inp.placeholder||'')).toLowerCase();
                  const v=(inp.value||'');
                  if (/date|oct|sept|2026/.test(aria+v) || /\\d{1,2}\\s*\\w+\\s*2026/.test(v)) {
                    inp.focus(); inp.value=dateStr;
                    inp.dispatchEvent(new Event('input',{bubbles:true}));
                    inp.dispatchEvent(new Event('change',{bubbles:true}));
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
            SCHED_DATE_LABEL if False else date_str,
        )
        # Prefer "15 October 2026" long form too
        page.keyboard.type("")  # noop keep typed
        info["date_js"] = True

    # Also try long form
    try:
        el = page.locator('tp-yt-paper-input[aria-label="Enter date"] input')
        if el.count():
            el.first.click(force=True)
            page.keyboard.press("Meta+a")
            page.keyboard.type(SCHED_DATE_LABEL, delay=25)
            page.keyboard.press("Enter")
            info["date_typed_long"] = SCHED_DATE_LABEL
            page.wait_for_timeout(500)
    except Exception:
        pass

    # Time 18:00
    page.evaluate(
        """(t) => {
          const walk=(r,d=0)=>{
            if(!r||d>55) return null;
            for (const inp of (r.querySelectorAll?r.querySelectorAll('input'):[])) {
              const v=inp.value||'';
              const aria=((inp.getAttribute('aria-label')||'')+(inp.placeholder||'')).toLowerCase();
              if (/^\\d{1,2}:\\d{2}$/.test(v) || /time/.test(aria)) {
                inp.focus(); inp.select && inp.select();
                inp.value=t;
                inp.dispatchEvent(new Event('input',{bubbles:true}));
                inp.dispatchEvent(new Event('change',{bubbles:true}));
                return {old:v, aria};
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if (el.shadowRoot) { const x=walk(el.shadowRoot,d+1); if(x) return x; }
            }
            return null;
          };
          return walk(document);
        }""",
        SCHED_TIME,
    )
    page.keyboard.press("Meta+a")
    page.keyboard.type(SCHED_TIME, delay=35)
    page.keyboard.press("Tab")
    info["time_typed"] = SCHED_TIME
    page.wait_for_timeout(400)

    # Untick Premiere
    page.evaluate(
        """() => {
          const walk=(r,d=0)=>{
            if(!r||d>45) return null;
            for (const el of (r.querySelectorAll
              ? r.querySelectorAll('[role=checkbox],tp-yt-paper-checkbox,input[type=checkbox]')
              : [])) {
              const t=((el.innerText||'')+' '+(el.getAttribute('aria-label')||'')).replace(/\\s+/g,' ');
              if (/Premiere/i.test(t) && !/instant/i.test(t)) {
                const checked = el.getAttribute('aria-checked')==='true' || el.checked===true;
                if (checked) el.click();
                return {was:checked, t:t.slice(0,60)};
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if (el.shadowRoot) { const x=walk(el.shadowRoot,d+1); if(x) return x; }
            }
            return null;
          };
          return walk(document);
        }"""
    )
    shot(page, "uat_23_date_time_set.png")

    # Confirm Schedule / Save
    clicked = None
    for name in ["Schedule", "Save", "Done"]:
        # Prefer bottom primary button — last match
        try:
            btn = page.get_by_role("button", name=re.compile(rf"^{name}$", re.I))
            if btn.count():
                # click last enabled
                for i in range(btn.count() - 1, -1, -1):
                    if btn.nth(i).is_enabled():
                        btn.nth(i).click(force=True, timeout=4000)
                        clicked = name
                        break
            if clicked:
                break
        except Exception:
            pass
        if find_click(page, name, y_min=200):
            clicked = name
            break
    info["confirm"] = clicked
    page.wait_for_timeout(4000)
    dismiss(page)
    shot(page, "uat_24_after_schedule_save.png")

    # Re-open Visibility panel for proof screenshot
    page.goto(
        f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(4000)
    dismiss(page)
    find_click(page, "Scheduled", y_min=120)
    page.wait_for_timeout(1500)
    # Also hover for tooltip
    try:
        page.get_by_text("Scheduled").first.hover(timeout=4000)
        page.wait_for_timeout(800)
    except Exception:
        pass
    proof = shot(page, "uat_25_visibility_panel_proof.png")
    body2 = snip(page, 6000)
    info["proof_shot"] = proof
    info["proof_snip"] = body2[:1200]
    info["has_15_oct"] = bool(re.search(r"15\s*(Oct|October).*2026", body2, re.I))
    info["has_30_sep"] = bool(re.search(r"30\s*(Sept|Sep|September).*2026", body2, re.I))
    info["has_1800"] = bool(re.search(r"18:00|6:00\s*PM|17:00", body2, re.I))
    info["premiere_on"] = bool(re.search(r"will premiere|Premiere on", body2, re.I))
    # Also open edit Visibility tab
    goto_edit(page)
    find_click(page, "Visibility", y_min=0)
    page.wait_for_timeout(1500)
    shot(page, "uat_26_edit_visibility.png")
    vis_body = snip(page, 4000)
    info["edit_vis_snip"] = vis_body[:800]
    if re.search(r"15\s*(Oct|October).*2026", vis_body, re.I):
        info["has_15_oct"] = True
    if re.search(r"30\s*(Sept|Sep|September).*2026", vis_body, re.I):
        info["has_30_sep"] = True
    info["ok"] = bool(info["has_15_oct"] and not info["has_30_sep"] and not info["premiere_on"])
    return info


def do_ab(page) -> dict:
    info: dict = {
        "wanted": "Title and thumbnail",
        "pairs": [
            {"title": TITLES[0], "thumb": THUMB_A.name},
            {"title": TITLES[1], "thumb": THUMB_C.name},
            {"title": TITLES[2], "thumb": THUMB_B.name},
        ],
    }
    goto_edit(page)
    shot(page, "uat_30_edit_ab.png")
    box = find_click(page, "A/B Testing", y_min=140)
    info["open_box"] = box
    if not box:
        try:
            page.get_by_text("A/B Testing", exact=True).first.click(timeout=5000)
            info["open"] = "get_by_text"
        except Exception as e:
            info["open_err"] = type(e).__name__
            info["ok"] = False
            return info
    else:
        info["open"] = "mouse"
    opened = wait_re(
        page,
        r"Title and thumbnail|Thumbnail only|Title only|Test and compare",
        12000,
    )
    info["dialog_open"] = opened
    shot(page, "uat_31_ab_dialog.png")
    body = snip(page, 6000)
    info["offers"] = [
        lab
        for lab in ["Title and thumbnail", "Thumbnail only", "Title only"]
        if re.search(re.escape(lab), body, re.I)
    ]
    find_click(page, "Title and thumbnail", y_min=80)
    page.wait_for_timeout(2000)
    shot(page, "uat_32_ab_type.png")

    # Upload thumbs into y-sorted image file inputs
    uploads = []
    loc = page.locator('input[type="file"]')
    idxs = []
    for i in range(loc.count()):
        try:
            acc = (loc.nth(i).get_attribute("accept") or "").lower()
            boxb = loc.nth(i).bounding_box()
            if not boxb or boxb["y"] < 60:
                continue
            if "image" in acc or "jpg" in acc or "jpeg" in acc or "png" in acc or acc == "":
                idxs.append((boxb["y"], i))
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
                page.wait_for_timeout(2200)
            except Exception as e:
                uploads.append({"slot": j + 1, "err": type(e).__name__})
        else:
            try:
                with page.expect_file_chooser(timeout=5000) as fc:
                    find_click(page, "Add thumbnail", y_min=100)
                fc.value.set_files(str(thumb))
                uploads.append({"slot": j + 1, "file": thumb.name, "via": "chooser"})
                page.wait_for_timeout(2200)
            except Exception as e:
                uploads.append({"slot": j + 1, "err": type(e).__name__})
        shot(page, f"uat_33_thumb_{j+1}.png")
    info["uploads"] = uploads

    # Title fields
    titles_set = []
    inputs = page.locator("input, textarea")
    cands = []
    for i in range(inputs.count()):
        el = inputs.nth(i)
        try:
            if not el.is_visible():
                continue
            ml = el.get_attribute("maxlength") or ""
            aria = (
                (el.get_attribute("aria-label") or "")
                + (el.get_attribute("placeholder") or "")
            ).lower()
            boxb = el.bounding_box()
            if not boxb or boxb["y"] < 100 or boxb["width"] < 120:
                continue
            if ml == "100" or "title" in aria or "add title" in aria:
                cands.append((boxb["y"], i))
        except Exception:
            pass
    cands.sort()
    info["title_cands"] = [{"y": y, "i": i} for y, i in cands]
    for j, (_, i) in enumerate(cands[:3]):
        el = inputs.nth(i)
        el.click(timeout=3000)
        page.keyboard.press("Meta+a")
        page.keyboard.type(TITLES[j], delay=12)
        titles_set.append({"i": i, "title": TITLES[j]})
        page.wait_for_timeout(350)
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
    shot(page, "uat_34_ab_filled.png")
    body = snip(page, 4000)
    info["needs_third"] = bool(
        re.search(r"Third title and thumbnail are required|Second title is required", body, re.I)
    )

    set_box = find_click(page, "Set test", y_min=200)
    info["set_box"] = set_box
    if not set_box:
        try:
            btn = page.get_by_role("button", name=re.compile(r"^Set test$", re.I))
            if btn.count():
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
    shot(page, "uat_35_ab_after_set.png")
    after = snip(page, 3000)
    info["after"] = after[:900]
    info["running"] = bool(re.search(r"A/B test running|test running", after, re.I))
    info["ok"] = bool(info["running"])
    if not info["ok"]:
        info["note"] = (
            f"offers={info.get('offers')} set={info.get('set')} "
            f"disabled={info.get('set_disabled')} needs_third={info.get('needs_third')}"
        )
    return info


def do_end_screen(page) -> dict:
    info: dict = {"related": RELATED_002, "relatedTitle": RELATED_TITLE}
    goto_edit(page)
    find_click(page, "End screen", y_min=200) or page.get_by_text(
        "End screen", exact=True
    ).first.click(timeout=5000)
    page.wait_for_timeout(2500)
    for _ in range(3):
        dismiss(page)
        find_click(page, "OK, got it")
        try:
            page.keyboard.press("Escape")
        except Exception:
            pass
        page.wait_for_timeout(200)
    shot(page, "uat_40_endscreen.png")

    # Import / template
    for label in ["Import from video", "Use template", "Template", "ADD ELEMENT", "Add element"]:
        find_click(page, label, y_min=80, exact=False)
        page.wait_for_timeout(600)

    # Prefer template with 1 video + subscribe if listed
    for label in [
        "1 video + 1 subscribe",
        "Video and subscribe",
        "One video and subscribe",
    ]:
        if find_click(page, label, y_min=80, exact=False):
            info["template"] = label
            page.wait_for_timeout(1500)
            break

    # Add Video element if missing
    if not re.search(r"Video|Subscribe", snip(page, 3000), re.I):
        find_click(page, "Element", y_min=80, exact=False)
        find_click(page, "Video", y_min=80)
        find_click(page, "Subscribe", y_min=80)

    shot(page, "uat_41_endscreen_elements.png")

    # Bind Specific video 002
    for label in ["Specific video", "Select a video", "Choose a video", "Most recent upload"]:
        if find_click(page, label, y_min=80, exact=False):
            info["picker"] = label
            page.wait_for_timeout(1200)
            break
    # Search for 002
    try:
        search = page.locator('input[type="text"], input[aria-label*="Search" i]')
        if search.count():
            search.last.click(timeout=2000)
            page.keyboard.press("Meta+a")
            page.keyboard.type(RELATED_TITLE[:40], delay=20)
            page.wait_for_timeout(2000)
            find_click(page, RELATED_TITLE, y_min=100, exact=False)
            info["picked_title"] = RELATED_TITLE
    except Exception as e:
        info["pick_err"] = type(e).__name__
    # Also try by id text
    find_click(page, RELATED_002, y_min=80, exact=False)
    page.wait_for_timeout(1000)

    # Ensure Subscribe present
    if not re.search(r"Subscribe", snip(page, 3000), re.I):
        find_click(page, "Subscribe", y_min=80)

    shot(page, "uat_42_endscreen_bound.png")
    # Save
    for name in ["SAVE", "Save"]:
        if find_click(page, name, y_min=0):
            info["save"] = name
            break
        try:
            btn = page.get_by_role("button", name=re.compile(rf"^{name}$", re.I))
            if btn.count() and btn.first.is_enabled():
                btn.first.click(timeout=4000)
                info["save"] = f"role:{name}"
                break
        except Exception:
            pass
    page.wait_for_timeout(4000)
    shot(page, "uat_43_endscreen_saved.png")
    after = snip(page, 4000)
    info["after"] = after[:900]
    info["has_processing_error"] = bool(
        re.search(r"problem in processing|recent edits were not saved|NaN", after, re.I)
    )
    info["ok"] = bool(
        re.search(re.escape(RELATED_TITLE[:20]), after, re.I)
        or re.search(RELATED_002, after)
    ) and not info["has_processing_error"]
    if not info["ok"]:
        info["note"] = "End screen bind may still be Most recent / processing — see screenshots."
    return info


def try_pin(page) -> dict:
    info: dict = {"textFile": str(PIN_TXT.relative_to(PKG)) if PIN_TXT.exists() else None}
    text = PIN_TXT.read_text().strip() if PIN_TXT.exists() else ""
    info["chars"] = len(text)
    # Watch page often blocks comments while private/scheduled
    page.goto(
        f"https://studio.youtube.com/video/{VIDEO_ID}/comments",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(3000)
    shot(page, "uat_50_comments.png")
    body = snip(page, 3000)
    info["studio_snip"] = body[:500]
    # Try watch page
    page.goto(
        f"https://www.youtube.com/watch?v={VIDEO_ID}",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(4000)
    shot(page, "uat_51_watch.png")
    wbody = snip(page, 3000)
    info["watch_snip"] = wbody[:500]
    can_comment = bool(
        re.search(r"Add a comment|Leave a comment", wbody, re.I)
    ) and not re.search(r"Comments are turned off|private video", wbody, re.I)
    info["can_comment"] = can_comment
    if not can_comment:
        info["ok"] = False
        info["reason"] = "watch_page_not_commentable_while_scheduled_or_private"
        info["note"] = "Pin on launch day 15 Oct 2026 — Studio blocks comments while private/scheduled."
        return info
    try:
        page.get_by_text(re.compile(r"Add a comment|Leave a comment", re.I)).first.click(
            timeout=5000
        )
        page.wait_for_timeout(800)
        page.keyboard.type(text, delay=5)
        page.wait_for_timeout(500)
        find_click(page, "Comment", y_min=200)
        page.wait_for_timeout(3000)
        # Pin via menu — best-effort
        find_click(page, "Action menu", y_min=200, exact=False)
        find_click(page, "Pin", y_min=100, exact=False)
        info["ok"] = True
    except Exception as e:
        info["ok"] = False
        info["err"] = type(e).__name__
    shot(page, "uat_52_pin_attempt.png")
    return info


def main() -> None:
    for p in THUMBS:
        if not p.exists():
            raise SystemExit(f"missing thumb {p}")
    ensure_chrome()
    result: dict = {
        "videoId": VIDEO_ID,
        "channel": "@HistoryOfScienceYT",
        "ben_phone_uat": "29 Sep 18:51 — auto thumb, no altered label, date 30 Sep in app",
        "started": datetime.now().isoformat(timespec="seconds"),
    }
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        ctx = browser.contexts[0] if browser.contexts else browser.new_context()
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.set_default_timeout(30000)

        log("1 thumb A v04")
        result["thumbnail"] = upload_custom_thumb(page)
        dump("UAT_THUMB_RESULT.json", result["thumbnail"])

        log("2 altered YES")
        result["altered"] = set_altered_yes(page)
        dump("UAT_ALTERED_RESULT.json", result["altered"])

        log("3 schedule 15 Oct 18:00")
        result["schedule"] = fix_schedule(page)
        dump("UAT_SCHEDULE_RESULT.json", result["schedule"])

        log("4 test & compare")
        result["testAndCompare"] = do_ab(page)
        dump("UAT_AB_RESULT.json", result["testAndCompare"])

        log("5 end screen")
        result["endScreen"] = do_end_screen(page)
        dump("UAT_ENDSCREEN_RESULT.json", result["endScreen"])

        log("6 pin")
        result["pinnedComment"] = try_pin(page)
        dump("UAT_PIN_RESULT.json", result["pinnedComment"])

    result["finished"] = datetime.now().isoformat(timespec="seconds")
    result["ok"] = {
        "thumbnail": result["thumbnail"].get("ok"),
        "altered": result["altered"].get("ok"),
        "schedule": result["schedule"].get("ok"),
        "testAndCompare": result["testAndCompare"].get("ok"),
        "endScreen": result["endScreen"].get("ok"),
        "pinnedComment": result["pinnedComment"].get("ok"),
    }
    dump("PHONE_UAT_FIX_RESULT.json", result)
    log(f"DONE {json.dumps(result['ok'])}")
    print(json.dumps(result["ok"], indent=2), flush=True)


if __name__ == "__main__":
    main()
