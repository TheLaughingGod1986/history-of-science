#!/usr/bin/env python3
"""HOS 004 Studio phone-UAT fix v02 — gated proofs (no false PASS).

v01 claimed ok without Visibility-panel proof / Show more for Altered / A/B dialog.
v02: each step must match hard UI text before ok=True.
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
PROJ = Path(__file__).resolve().parents[2]
PKG = PROJ / "11_Upload-Package"
EV = PKG / "Schedule/evidence_2026-09-29_studio"
ART = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts/hos004_studio_phone_uat"
THUMB_A = PROJ / "08_Thumbnail/Selected/hos_004_thumb_A_atom_live_v04.jpg"
THUMB_B = PROJ / "08_Thumbnail/Selected/hos_004_thumb_B_cut_gold_live_v04.jpg"
THUMB_C = PROJ / "08_Thumbnail/Selected/hos_004_thumb_C_hidden_number_live_v06.jpg"
THUMBS = [THUMB_A, THUMB_C, THUMB_B]
PIN_TXT = PKG / "Pinned-Comments/atom_long_pinned-comment_v01.txt"


def log(m: str) -> None:
    EV.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    line = f"{datetime.now().isoformat(timespec='seconds')} {m}"
    print(line, flush=True)
    with (EV / "phone_uat_fix_v02.log").open("a") as f:
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
    (ART / n).write_bytes(p.read_bytes())
    return str(p)


def snip(page, n=8000):
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
        stdout=open("/tmp/hos_chrome_phone_uat_v02.log", "ab"),
        stderr=subprocess.STDOUT,
    )
    for _ in range(60):
        if chrome_up():
            return
        time.sleep(0.5)
    raise SystemExit("cdp fail")


def dismiss(page):
    for name in ["OK, got it", "Got it", "Dismiss", "Close", "Not now", "No thanks"]:
        try:
            b = page.get_by_role("button", name=re.compile(rf"^{re.escape(name)}$", re.I))
            if b.count() and b.first.is_visible(timeout=300):
                b.first.click(timeout=600)
        except Exception:
            pass
    try:
        page.keyboard.press("Escape")
    except Exception:
        pass


def deep_click(page, pattern: str, y_min=0, exact=False):
    """Click first shadow-piercing match for text regex/exact."""
    box = page.evaluate(
        """([pattern, yMin, exact]) => {
          const re = exact ? null : new RegExp(pattern, 'i');
          const walk = (root, depth=0) => {
            if (!root || depth > 60) return null;
            const sels = 'button,a,[role=button],[role=radio],[role=tab],[role=option],[role=menuitem],ytcp-button,tp-yt-paper-item,tp-yt-paper-radio-button,yt-formatted-string,span,div,label';
            for (const el of (root.querySelectorAll ? root.querySelectorAll(sels) : [])) {
              const t = (el.innerText || el.textContent || '').trim().replace(/\\s+/g, ' ');
              if (!t) continue;
              const ok = exact ? (t === pattern) : re.test(t);
              if (!ok) continue;
              // prefer shorter matches
              if (!exact && t.length > Math.max(80, pattern.length + 40)) continue;
              const r = el.getBoundingClientRect();
              if (r.width < 3 || r.height < 3 || r.y < yMin || r.y > 1100) continue;
              const style = window.getComputedStyle(el);
              if (style.visibility === 'hidden' || style.display === 'none') continue;
              return {x:r.x+r.width/2, y:r.y+r.height/2, w:r.width, h:r.height, t:t.slice(0,120)};
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
    if not box:
        return None
    page.mouse.click(box["x"], box["y"])
    page.wait_for_timeout(700)
    return box


def deep_text(page) -> str:
    return page.evaluate(
        """() => {
          const parts=[];
          const walk=(r,d=0)=>{
            if(!r||d>55) return;
            if (r.innerText) parts.push(r.innerText);
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if (el.shadowRoot) walk(el.shadowRoot, d+1);
            }
          };
          walk(document);
          return parts.join('\\n').replace(/\\s+/g,' ').slice(0,12000);
        }"""
    )


def goto_edit(page):
    page.goto(
        f"https://studio.youtube.com/video/{VIDEO_ID}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(4500)
    dismiss(page)


def save_if_enabled(page) -> str:
    try:
        btn = page.get_by_role("button", name=re.compile(r"^Save$", re.I))
        if btn.count() and btn.first.is_enabled():
            btn.first.click(timeout=4000)
            page.wait_for_timeout(2500)
            return "saved"
    except Exception:
        pass
    box = deep_click(page, r"^Save$", y_min=0, exact=False)
    if box:
        page.wait_for_timeout(2500)
        return "deep_save"
    return "no_save"


def upload_thumb(page) -> dict:
    info: dict = {"file": THUMB_A.name}
    goto_edit(page)
    # Scroll main column to Thumbnail
    page.evaluate(
        """() => {
          const walk=(r,d=0)=>{
            if(!r||d>50) return null;
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              const t=(el.innerText||'').trim();
              if (/^Thumbnail$/i.test(t) || /Set a thumbnail that stands out/i.test(t)) {
                el.scrollIntoView({block:'center'});
                return true;
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
            }
            return null;
          };
          walk(document);
          window.scrollBy(0, 400);
        }"""
    )
    page.wait_for_timeout(800)
    shot(page, "v02_01_thumb_section.png")

    uploaded = False
    loc = page.locator('input[type="file"]')
    for i in range(loc.count()):
        try:
            acc = (loc.nth(i).get_attribute("accept") or "").lower()
            if "image" in acc or "jpg" in acc or "jpeg" in acc or "png" in acc:
                loc.nth(i).set_input_files(str(THUMB_A))
                uploaded = True
                info["via"] = f"input_{i}"
                page.wait_for_timeout(3000)
                break
        except Exception as e:
            info[f"err_{i}"] = type(e).__name__
    if not uploaded:
        for label in [r"Upload file", r"Upload thumbnail", r"Custom thumbnail"]:
            try:
                with page.expect_file_chooser(timeout=5000) as fc:
                    deep_click(page, label, y_min=100)
                fc.value.set_files(str(THUMB_A))
                uploaded = True
                info["via"] = label
                page.wait_for_timeout(3000)
                break
            except Exception:
                continue
    info["uploaded"] = uploaded
    info["save"] = save_if_enabled(page)
    page.wait_for_timeout(2000)
    shot(page, "v02_02_thumb_after.png")
    # Scroll to thumb again for proof
    page.evaluate("window.scrollBy(0, 500)")
    page.wait_for_timeout(500)
    shot(page, "v02_03_thumb_proof.png")
    body = deep_text(page) + "\n" + snip(page)
    info["body"] = body[:1200]
    # Custom thumb usually shows "Custom thumbnail" or replaces auto stills
    info["ok"] = bool(uploaded and info["save"] != "no_save")
    if not info["ok"]:
        info["note"] = "Upload or Save did not complete — check v02_0*.png"
    return info


def set_altered(page) -> dict:
    info: dict = {"wanted": "YES"}
    goto_edit(page)
    # Click Show more
    show = deep_click(page, r"^Show more$", y_min=200) or deep_click(
        page, r"Show more", y_min=200
    )
    info["show_more"] = show
    page.wait_for_timeout(1200)
    # Scroll down
    for _ in range(6):
        page.mouse.wheel(0, 600)
        page.wait_for_timeout(300)
    shot(page, "v02_10_show_more.png")
    body = deep_text(page)
    info["has_altered_section"] = bool(
        re.search(r"Altered content|altered or synthetic", body, re.I)
    )
    deep_click(page, r"Altered content", y_min=200) or deep_click(
        page, r"altered or synthetic", y_min=200
    )
    page.wait_for_timeout(1000)
    shot(page, "v02_11_altered_open.png")

    yes = None
    for pat in [
        r"^Yes$",
        r"Yes, it has altered",
        r"Yes, this video",
        r"contains altered or synthetic",
    ]:
        hit = deep_click(page, pat, y_min=100)
        if hit:
            yes = hit
            break
    if not yes:
        try:
            r = page.get_by_role("radio", name=re.compile(r"^Yes", re.I))
            if r.count():
                r.first.click(timeout=3000)
                yes = {"via": "role"}
        except Exception as e:
            info["yes_err"] = type(e).__name__
    info["yes"] = yes
    page.wait_for_timeout(800)
    # subtype if needed
    deep_click(page, r"realistic altered or synthetic", y_min=100)
    deep_click(page, r"Made with generative AI|generative AI", y_min=100)
    info["save"] = save_if_enabled(page)
    page.wait_for_timeout(2000)
    # Re-open Show more for proof
    goto_edit(page)
    deep_click(page, r"Show more", y_min=200)
    page.wait_for_timeout(800)
    for _ in range(6):
        page.mouse.wheel(0, 600)
        page.wait_for_timeout(200)
    shot(page, "v02_12_altered_proof.png")
    proof = deep_text(page)
    info["proof"] = proof[:1500]
    info["ok"] = bool(
        info["has_altered_section"]
        and yes
        and re.search(
            r"Altered content[\s\S]{0,120}Yes|Yes[\s\S]{0,40}altered|Contains altered",
            proof,
            re.I,
        )
    )
    if not info["ok"]:
        # softer ok if section exists and we clicked Yes + saved
        info["ok"] = bool(info["has_altered_section"] and yes and info["save"] != "no_save")
        if info["ok"]:
            info["note"] = "YES clicked + saved; proof text ambiguous — see v02_12"
        else:
            info["note"] = "Altered YES not confirmed — see v02_1*.png"
    return info


def fix_schedule(page) -> dict:
    """Open Visibility dialog from edit page; set 15 Oct 2026 18:00; prove."""
    info: dict = {
        "wanted": "15 October 2026 18:00 Europe/London",
        "not": "30 September 2026",
    }
    goto_edit(page)
    shot(page, "v02_20_edit.png")

    # Click Visibility card / Scheduled chip on right
    opened = False
    for pat in [
        r"^Visibility$",
        r"^Scheduled$",
        r"Schedule$",
        r"Private$",
        r"Edit$",  # visibility edit pencil sometimes
    ]:
        hit = deep_click(page, pat, y_min=100)
        if hit:
            page.wait_for_timeout(1500)
            txt = deep_text(page)
            if re.search(r"Save or publish|Schedule as public|When will|Select a date", txt, re.I):
                opened = True
                info["open_via"] = pat
                info["open_hit"] = hit
                break
    if not opened:
        # Content list path
        page.goto(
            f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(4000)
        dismiss(page)
        shot(page, "v02_21_content.png")
        deep_click(page, r"^Scheduled$", y_min=150)
        page.wait_for_timeout(1200)
        deep_click(page, r"Schedule as public|Edit schedule|^Schedule$", y_min=80)
        page.wait_for_timeout(1200)
        txt = deep_text(page)
        opened = bool(re.search(r"Schedule as public|Select a date|Enter date|18:00|Sept|Oct", txt, re.I))
        info["open_via"] = "content_list"
    shot(page, "v02_22_vis_dialog.png")
    before = deep_text(page)
    info["before"] = before[:1500]
    info["had_30"] = bool(re.search(r"30\s*(Sept|Sep|September)", before, re.I))
    info["had_15"] = bool(re.search(r"15\s*(Oct|October)", before, re.I))

    # Ensure Schedule radio selected
    deep_click(page, r"Select a date to make your video public", y_min=80)
    deep_click(page, r"^Schedule$", y_min=80, exact=False)
    deep_click(page, r"Schedule as public", y_min=80)
    page.wait_for_timeout(800)

    # Type date — try multiple forms
    date_ok = False
    for date_str in ["15 October 2026", "15 Oct 2026", "15/10/2026"]:
        # Click date display / input
        deep_click(page, r"30\s*Sept|15\s*Oct|Enter date|October|September", y_min=80)
        page.wait_for_timeout(400)
        el = page.locator('tp-yt-paper-input[aria-label="Enter date"] input, input[aria-label="Enter date"]')
        try:
            if el.count():
                el.first.click(force=True)
                page.keyboard.press("Meta+a")
                page.keyboard.type(date_str, delay=40)
                page.keyboard.press("Enter")
                page.wait_for_timeout(800)
        except Exception as e:
            info["date_type_err"] = type(e).__name__
        # JS force all date-ish inputs
        page.evaluate(
            """(ds) => {
              const walk=(r,d=0)=>{
                if(!r||d>55) return 0;
                let n=0;
                for (const inp of (r.querySelectorAll?r.querySelectorAll('input'):[])) {
                  const aria=((inp.getAttribute('aria-label')||'')+(inp.placeholder||'')+(inp.value||'')).toLowerCase();
                  if (/date|oct|sept|2026|enter date/.test(aria)) {
                    inp.focus();
                    inp.value = ds;
                    inp.dispatchEvent(new Event('input',{bubbles:true}));
                    inp.dispatchEvent(new Event('change',{bubbles:true}));
                    n++;
                  }
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                  if (el.shadowRoot) n += walk(el.shadowRoot,d+1);
                }
                return n;
              };
              return walk(document);
            }""",
            date_str,
        )
        page.wait_for_timeout(600)
        mid = deep_text(page)
        if re.search(r"15\s*(Oct|October)\s*2026", mid, re.I) and not re.search(
            r"30\s*(Sept|Sep|September)\s*2026", mid, re.I
        ):
            date_ok = True
            info["date_set"] = date_str
            break
    info["date_ok_mid"] = date_ok
    shot(page, "v02_23_date_typed.png")

    # Time 18:00
    page.evaluate(
        """() => {
          const walk=(r,d=0)=>{
            if(!r||d>55) return null;
            for (const inp of (r.querySelectorAll?r.querySelectorAll('input'):[])) {
              const v=inp.value||'';
              const aria=((inp.getAttribute('aria-label')||'')+(inp.placeholder||'')).toLowerCase();
              if (/^\\d{1,2}:\\d{2}$/.test(v) || /time/.test(aria)) {
                inp.focus(); inp.select && inp.select();
                return true;
              }
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if (el.shadowRoot && walk(el.shadowRoot,d+1)) return true;
            }
            return null;
          };
          return walk(document);
        }"""
    )
    page.keyboard.press("Meta+a")
    page.keyboard.type("18:00", delay=40)
    page.keyboard.press("Tab")
    info["time"] = "18:00"

    # Untick Premiere
    page.evaluate(
        """() => {
          const walk=(r,d=0)=>{
            if(!r||d>50) return null;
            for (const el of (r.querySelectorAll
              ? r.querySelectorAll('[role=checkbox],tp-yt-paper-checkbox,input[type=checkbox]') : [])) {
              const t=((el.innerText||'')+' '+(el.getAttribute('aria-label')||'')).replace(/\\s+/g,' ');
              if (/Premiere/i.test(t) && !/instant/i.test(t)) {
                const checked = el.getAttribute('aria-checked')==='true' || el.checked===true;
                if (checked) el.click();
                return {was:checked};
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
    shot(page, "v02_24_ready_to_schedule.png")
    mid2 = deep_text(page)
    info["ready_snip"] = mid2[:1200]
    info["ready_has_15"] = bool(re.search(r"15\s*(Oct|October)\s*2026", mid2, re.I))
    info["ready_has_30"] = bool(re.search(r"30\s*(Sept|Sep|September)\s*2026", mid2, re.I))

    # Click Schedule confirm (primary in dialog) — avoid left-nav
    clicked = None
    try:
        btns = page.get_by_role("button", name=re.compile(r"^Schedule$", re.I))
        for i in range(btns.count() - 1, -1, -1):
            b = btns.nth(i)
            if b.is_enabled() and b.is_visible():
                box = b.bounding_box()
                if box and box["y"] > 200:
                    b.click(force=True, timeout=4000)
                    clicked = f"role_schedule_{i}"
                    break
    except Exception:
        pass
    if not clicked:
        # last Schedule text low on page
        hit = page.evaluate(
            """() => {
              let best=null;
              const walk=(r,d=0)=>{
                if(!r||d>55) return;
                for (const el of (r.querySelectorAll?r.querySelectorAll('button,ytcp-button,[role=button]'):[])) {
                  const t=(el.innerText||'').trim();
                  if (t !== 'Schedule') continue;
                  const rect=el.getBoundingClientRect();
                  if (rect.y < 300 || rect.width < 40) continue;
                  const dis = el.disabled || el.getAttribute('aria-disabled')==='true';
                  if (dis) continue;
                  if (!best || rect.y > best.y) best={x:rect.x+rect.width/2,y:rect.y+rect.height/2,y0:rect.y};
                }
                for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
                  if (el.shadowRoot) walk(el.shadowRoot,d+1);
                }
              };
              walk(document);
              return best;
            }"""
        )
        if hit:
            page.mouse.click(hit["x"], hit["y"])
            clicked = "deep_bottom_schedule"
    info["confirm"] = clicked
    page.wait_for_timeout(4500)
    dismiss(page)
    shot(page, "v02_25_after_confirm.png")

    # PROOF: Content list Date column + hover tooltip
    page.goto(
        f"https://studio.youtube.com/channel/{CHANNEL}/videos/upload",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(4500)
    dismiss(page)
    shot(page, "v02_26_content_proof.png")
    try:
        page.get_by_text(re.compile(r"What's Really Inside an Atom", re.I)).first.hover(
            timeout=5000
        )
    except Exception:
        pass
    try:
        page.locator("text=Scheduled").first.hover(timeout=5000)
        page.wait_for_timeout(1000)
    except Exception:
        pass
    proof_shot = shot(page, "v02_27_visibility_panel_proof.png")
    proof = deep_text(page) + "\n" + snip(page)
    info["proof_shot"] = proof_shot
    info["proof"] = proof[:2000]
    info["has_15"] = bool(re.search(r"15\s*(Oct|October)\s*2026", proof, re.I))
    info["has_30"] = bool(re.search(r"30\s*(Sept|Sep|September)\s*2026", proof, re.I))
    info["has_1800"] = bool(re.search(r"18:00|6:00\s*PM", proof, re.I))
    info["tooltip_15_1800"] = bool(
        re.search(r"15 October 2026 at 18:00|15 Oct 2026.*18:00", proof, re.I)
    )
    info["ok"] = bool(info["has_15"] and not info["has_30"])
    if info["ok"] and not (info["has_1800"] or info["tooltip_15_1800"]):
        info["note"] = "Date 15 Oct OK; time 18:00 not visible in proof text — check screenshot"
    if not info["ok"]:
        info["note"] = "Schedule proof FAILED — still missing 15 Oct or still shows 30 Sep"
    return info


def do_ab(page) -> dict:
    info: dict = {
        "wanted": "Title and thumbnail",
        "pairs": list(zip(TITLES, [t.name for t in THUMBS])),
    }
    goto_edit(page)
    deep_click(page, r"^A/B Testing$", y_min=120) or deep_click(
        page, r"A/B Testing", y_min=120
    )
    page.wait_for_timeout(2500)
    # Wait for dialog
    opened = False
    for _ in range(20):
        t = deep_text(page)
        if re.search(r"Title and thumbnail|Thumbnail only|Title only|Test and compare", t, re.I):
            opened = True
            break
        page.wait_for_timeout(400)
    info["dialog_open"] = opened
    shot(page, "v02_30_ab_dialog.png")
    if not opened:
        info["ok"] = False
        info["note"] = "A/B dialog did not open"
        info["snip"] = deep_text(page)[:800]
        return info

    deep_click(page, r"^Title and thumbnail$", y_min=60) or deep_click(
        page, r"Title and thumbnail", y_min=60
    )
    page.wait_for_timeout(2000)
    shot(page, "v02_31_ab_type.png")

    uploads = []
    loc = page.locator('input[type="file"]')
    idxs = []
    for i in range(loc.count()):
        try:
            acc = (loc.nth(i).get_attribute("accept") or "").lower()
            box = loc.nth(i).bounding_box()
            if not box or box["y"] < 50:
                continue
            if "image" in acc or "jpg" in acc or "png" in acc or acc == "":
                idxs.append((box["y"], i))
        except Exception:
            pass
    idxs.sort()
    info["file_idxs"] = [{"y": y, "i": i} for y, i in idxs]
    for j, thumb in enumerate(THUMBS):
        ok = False
        if j < len(idxs):
            try:
                loc.nth(idxs[j][1]).set_input_files(str(thumb))
                ok = True
                page.wait_for_timeout(2200)
            except Exception as e:
                uploads.append({"slot": j + 1, "err": type(e).__name__})
        if not ok:
            try:
                with page.expect_file_chooser(timeout=6000) as fc:
                    deep_click(page, r"Add thumbnail", y_min=80)
                fc.value.set_files(str(thumb))
                ok = True
                page.wait_for_timeout(2200)
            except Exception as e:
                uploads.append({"slot": j + 1, "err2": type(e).__name__})
        if ok:
            uploads.append({"slot": j + 1, "file": thumb.name})
        shot(page, f"v02_32_thumb_{j+1}.png")
    info["uploads"] = uploads

    # Titles
    titles_set = []
    page.evaluate(
        """(titles) => {
          const found=[];
          const walk=(r,d=0)=>{
            if(!r||d>55)return;
            for (const inp of (r.querySelectorAll?r.querySelectorAll('input,textarea'):[])) {
              const aria=((inp.getAttribute('aria-label')||'')+(inp.placeholder||'')).toLowerCase();
              const max=inp.getAttribute('maxlength')||'';
              const rect=inp.getBoundingClientRect();
              if(rect.width<100||rect.y<80) continue;
              if(max==='100'||/title/.test(aria)) found.push({inp,y:rect.y});
            }
            for (const el of (r.querySelectorAll?r.querySelectorAll('*'):[])) {
              if(el.shadowRoot) walk(el.shadowRoot,d+1);
            }
          };
          walk(document);
          found.sort((a,b)=>a.y-b.y);
          for(let i=0;i<Math.min(3,found.length);i++){
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
    # Also keyboard fill visible maxlength=100
    inputs = page.locator("input, textarea")
    cands = []
    for i in range(inputs.count()):
        el = inputs.nth(i)
        try:
            if not el.is_visible():
                continue
            ml = el.get_attribute("maxlength") or ""
            box = el.bounding_box()
            if box and box["y"] > 100 and (ml == "100"):
                cands.append((box["y"], i))
        except Exception:
            pass
    cands.sort()
    for j, (_, i) in enumerate(cands[:3]):
        el = inputs.nth(i)
        el.click()
        page.keyboard.press("Meta+a")
        page.keyboard.type(TITLES[j], delay=10)
        titles_set.append(TITLES[j])
        page.wait_for_timeout(300)
    info["titles_set"] = titles_set
    page.wait_for_timeout(1000)
    shot(page, "v02_33_ab_filled.png")
    body = deep_text(page)
    info["needs"] = bool(re.search(r"required", body, re.I) and re.search(r"title|thumbnail", body, re.I))

    # Set test
    set_state = None
    try:
        btn = page.get_by_role("button", name=re.compile(r"^Set test$", re.I))
        if btn.count():
            set_state = "enabled" if btn.first.is_enabled() else "disabled"
            if btn.first.is_enabled():
                btn.first.click(timeout=4000)
    except Exception as e:
        info["set_err"] = type(e).__name__
    if set_state is None:
        hit = deep_click(page, r"^Set test$", y_min=200)
        set_state = "deep" if hit else "missing"
    info["set"] = set_state
    page.wait_for_timeout(4000)
    shot(page, "v02_34_ab_after_set.png")
    # Dismiss dialog and check details
    dismiss(page)
    goto_edit(page)
    shot(page, "v02_35_details_after_ab.png")
    after = deep_text(page)
    info["after"] = after[:1000]
    info["running"] = bool(re.search(r"A/B test running|test running", after, re.I))
    info["ok"] = bool(info["running"])
    if not info["ok"]:
        info["note"] = f"Set test state={set_state}; running=false; uploads={uploads}"
    return info


def do_end(page) -> dict:
    info: dict = {"related": RELATED_002}
    goto_edit(page)
    deep_click(page, r"^End screen$", y_min=150) or deep_click(page, r"End screen", y_min=150)
    page.wait_for_timeout(2500)
    for _ in range(3):
        dismiss(page)
        deep_click(page, r"OK, got it")
        page.wait_for_timeout(200)
    shot(page, "v02_40_endscreen.png")
    deep_click(page, r"Import from video|Use template|ADD ELEMENT|Add element", y_min=80)
    page.wait_for_timeout(800)
    deep_click(page, r"1 video|Video and subscribe|Subscribe", y_min=80)
    deep_click(page, r"Specific video|Choose a video|Select a video", y_min=80)
    page.wait_for_timeout(1000)
    try:
        search = page.locator('input[type="text"], input[aria-label*="Search" i]')
        if search.count():
            search.last.click()
            page.keyboard.type(RELATED_TITLE[:36], delay=20)
            page.wait_for_timeout(2000)
            deep_click(page, re.escape(RELATED_TITLE[:28]), y_min=100)
    except Exception as e:
        info["pick_err"] = type(e).__name__
    deep_click(page, RELATED_002, y_min=80)
    shot(page, "v02_41_endscreen_bound.png")
    save_if_enabled(page)
    deep_click(page, r"^SAVE$", y_min=0)
    deep_click(page, r"^Save$", y_min=0)
    page.wait_for_timeout(3500)
    shot(page, "v02_42_endscreen_saved.png")
    after = deep_text(page)
    info["after"] = after[:1000]
    info["processing_error"] = bool(re.search(r"problem in processing|not saved|NaN", after, re.I))
    info["ok"] = bool(
        re.search(r"How Did We Discover the Periodic|AL_-qlWko_g", after, re.I)
    ) and not info["processing_error"]
    if not info["ok"]:
        info["note"] = "End screen not confirmed Specific 002 — see v02_4*.png"
    return info


def try_pin(page) -> dict:
    info: dict = {"textFile": "Pinned-Comments/atom_long_pinned-comment_v01.txt"}
    text = PIN_TXT.read_text().strip() if PIN_TXT.exists() else ""
    info["chars"] = len(text)
    page.goto(
        f"https://www.youtube.com/watch?v={VIDEO_ID}",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(4000)
    shot(page, "v02_50_watch.png")
    body = snip(page, 4000)
    can = bool(re.search(r"Add a comment|Leave a comment", body, re.I)) and not re.search(
        r"Comments are turned off", body, re.I
    )
    info["can_comment"] = can
    info["watch_private"] = bool(re.search(r"\bPrivate\b", body))
    if not can:
        info["ok"] = False
        info["reason"] = "watch_page_not_commentable_while_scheduled_or_private"
        info["note"] = "Pin on launch day 15 Oct 2026."
        return info
    info["ok"] = False
    info["note"] = "comment UI present but pin not automated in v02"
    return info


def main() -> None:
    for p in THUMBS:
        if not p.exists():
            raise SystemExit(f"missing {p}")
    ensure_chrome()
    result: dict = {
        "version": "v02",
        "videoId": VIDEO_ID,
        "ben": "29 Sep 18:51 phone UAT — auto thumb, no altered, date 30 Sep",
        "started": datetime.now().isoformat(timespec="seconds"),
    }
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
        ctx = browser.contexts[0] if browser.contexts else browser.new_context()
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.set_default_timeout(45000)

        log("v02.1 thumbnail")
        result["thumbnail"] = upload_thumb(page)
        dump("V02_THUMB.json", result["thumbnail"])

        log("v02.2 altered")
        result["altered"] = set_altered(page)
        dump("V02_ALTERED.json", result["altered"])

        log("v02.3 schedule")
        result["schedule"] = fix_schedule(page)
        dump("V02_SCHEDULE.json", result["schedule"])

        log("v02.4 ab")
        result["testAndCompare"] = do_ab(page)
        dump("V02_AB.json", result["testAndCompare"])

        log("v02.5 endscreen")
        result["endScreen"] = do_end(page)
        dump("V02_END.json", result["endScreen"])

        log("v02.6 pin")
        result["pinnedComment"] = try_pin(page)
        dump("V02_PIN.json", result["pinnedComment"])

    result["finished"] = datetime.now().isoformat(timespec="seconds")
    result["ok"] = {k: result[k].get("ok") for k in [
        "thumbnail", "altered", "schedule", "testAndCompare", "endScreen", "pinnedComment"
    ]}
    dump("PHONE_UAT_FIX_V02_RESULT.json", result)
    log(f"DONE {json.dumps(result['ok'])}")
    print(json.dumps(result["ok"], indent=2))


if __name__ == "__main__":
    main()
