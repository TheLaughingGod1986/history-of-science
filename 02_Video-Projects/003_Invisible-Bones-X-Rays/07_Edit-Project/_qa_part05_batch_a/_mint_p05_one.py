#!/usr/bin/env python3
"""Mint one Part05 plate: Quality Create + wait + marker-based download."""
from __future__ import annotations
import importlib.util, json, re, sys, time
from datetime import datetime, timezone
from pathlib import Path

REPO = Path("/Users/benjaminoats/YouTube/History Of Science")
EDIT = REPO / "02_Video-Projects/003_Invisible-Bones-X-Rays/07_Edit-Project"
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))
import orbit_flow_veo_ui as flow
import orbit_gemini_veo as veo

spec = importlib.util.spec_from_file_location("m", EDIT / "_mint_part04_batch_a.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

QA = EDIT / "_qa_part05_batch_a"
CLIP_DIR = REPO / "02_Video-Projects/003_Invisible-Bones-X-Rays/04_Generated-Clips/part05"
PROJECT = "https://flow.google.com/u/0/project/02ce23ba-3f6d-49ee-8177-67af2d9a1166"
FACE = " Readable Animistry cartoon faces with eyes and nose when any person appears — HARD FAIL blank mannequin ovals. No DNA helix."
CDP = "http://127.0.0.1:9222"

# Unique text markers to find the finished tile
MARKERS = {
    "04_soft_vs_bone": r"Layered cartoon body|soft tissue translucent",
    "05_detector_then_now": r"glowing cardboard then a simple modern sensor|A DETECTOR",
    "06_explorer_diagram": r"Explorer \(younger boy|messy wavy brown hair",
    "07_why_groundbreaking": r"closed scalpel tray stays closed",
    "08_dentist_hospital_payoff": r"hospital/dentist silhouette|YOUR WORLD",
    "09_bigger_question": r"faint question-mark glow|still blind to",
    "10_cardboard_glow_hold": r"return to faint cardboard fluorescence",
    "11_soft_return": r"soft fade energy on last glow|end of part",
}


def ensure_gallery(page):
    if "/project/02ce23ba" not in (page.url or "") or "/edit/" in (page.url or ""):
        page.goto(PROJECT, wait_until="domcontentloaded", timeout=120_000)
        page.wait_for_timeout(2000)


def submit(page, prompt: str) -> None:
    ensure_gallery(page)
    aria = page.evaluate(
        """() => { const a=document.querySelector('a[aria-label*="Google Account"]');
           return a && a.getAttribute('aria-label'); }"""
    )
    if not aria or "googlemail" not in aria.lower():
        raise SystemExit(f"STOP wrong account {aria}")
    try:
        flow.configure_veo_settings(
            page, model="Veo 3.1 - Quality", frames_mode=False, ingredients_mode=False
        )
    except Exception as e:
        print(f"  settings warn {e}", flush=True)
    page.keyboard.press("Escape")
    page.wait_for_timeout(300)
    m.set_prompt_manual(page, prompt)
    page.wait_for_timeout(400)
    btn = page.evaluate(
        """() => {
          for (const el of document.querySelectorAll('button,[role=button]')) {
            const aria = el.getAttribute('aria-label') || '';
            if (/Start generation/i.test(aria) && !el.disabled) {
              el.scrollIntoView({block:'center'});
              const r = el.getBoundingClientRect();
              return {x:r.x+r.width/2,y:r.y+r.height/2};
            }
          }
          return null;
        }"""
    )
    if not btn:
        raise SystemExit("STOP no Start generation")
    page.mouse.click(btn["x"], btn["y"])
    try:
        flow.confirm_generation_spend(page, timeout_s=8)
    except Exception:
        pass
    page.wait_for_timeout(3000)
    print("  submitted Create", flush=True)


def wait_done(page, marker: str, timeout_s: int = 700) -> None:
    t0 = time.time()
    last = ""
    while time.time() - t0 < timeout_s:
        ensure_gallery(page)
        body = page.locator("body").inner_text(timeout=5000)
        pcts = [int(x) for x in re.findall(r"(\d{1,3})%", body)]
        active = [x for x in pcts if x < 100]
        has = bool(re.search(marker, body, re.I))
        line = f"  wait {int(time.time()-t0)}s pct={pcts[-3:] if pcts else None} active={active} has={has}"
        if line != last:
            print(line, flush=True)
            last = line
        if has and not active:
            print("  READY", flush=True)
            return
        page.wait_for_timeout(10000)
    print("  wait timeout — try download anyway", flush=True)


def download_by_marker(page, dest: Path, marker: str) -> None:
    ensure_gallery(page)
    hit = page.evaluate(
        """(marker) => {
          const re = new RegExp(marker, 'i');
          const imgs = [...document.querySelectorAll('img')].filter(i => /\\/asb\\//.test(i.src||''));
          for (const img of imgs) {
            let p = img.parentElement;
            for (let k=0;k<10 && p;k++) {
              if (re.test(p.innerText||'')) {
                const r = img.getBoundingClientRect();
                return {x:r.x+r.width/2,y:r.y+r.height/2};
              }
              p = p.parentElement;
            }
          }
          return null;
        }""",
        marker,
    )
    if not hit:
        raise SystemExit(f"STOP no tile for marker {marker}")
    page.mouse.click(hit["x"], hit["y"])
    page.wait_for_timeout(2000)
    dls = page.evaluate(
        """() => [...document.querySelectorAll('button,[role=button]')].map(el => {
          const t=((el.innerText||'')+' '+(el.getAttribute('aria-label')||'')).trim().replace(/\\n/g,' ');
          const r=el.getBoundingClientRect();
          return {t:t.slice(0,60),x:r.x+r.width/2,y:r.y+r.height/2,
                  visible:r.width>8&&r.height>8&&r.y>=0&&r.y<120};
        }).filter(o => /download/i.test(o.t) && o.visible && !/batch/i.test(o.t))"""
    )
    raw = None
    for d in dls or []:
        try:
            with page.expect_download(timeout=120_000) as di:
                page.mouse.click(d["x"], d["y"])
                page.wait_for_timeout(600)
                item = page.evaluate(
                    """() => {
                      for (const el of document.querySelectorAll('[role=menuitem],button,a,.mat-mdc-menu-item')) {
                        const t=((el.innerText||'')+' '+(el.getAttribute('aria-label')||'')).trim();
                        if (/720p|original|mp4/i.test(t) && !/image|png|batch/i.test(t)) {
                          const r=el.getBoundingClientRect();
                          if (r.width>20) return {x:r.x+r.width/2,y:r.y+r.height/2};
                        }
                      }
                      return null;
                    }"""
                )
                if item:
                    page.mouse.click(item["x"], item["y"])
            dl = di.value
            try:
                src = dl.path()
                if src:
                    raw = Path(src).read_bytes()
            except Exception:
                pass
            if raw is None:
                tmp = dest.with_suffix(".tmp")
                dl.save_as(str(tmp))
                raw = tmp.read_bytes()
                tmp.unlink(missing_ok=True)
            if raw and len(raw) > 150_000 and b"ftyp" in raw[:64]:
                break
            raw = None
        except Exception as e:
            print(f"  dl fail {e}", flush=True)
            page.keyboard.press("Escape")
    if not raw:
        raise SystemExit("STOP download failed")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(raw)


def mint_plate(page, plate: dict) -> dict:
    pid = plate["id"]
    dest = CLIP_DIR / f"{pid}_v01.mp4"
    if dest.exists() and dest.stat().st_size > 150_000:
        print(f"SKIP {pid}", flush=True)
        return {"plate": pid, "status": "skipped"}
    marker = MARKERS[pid]
    prompt = m.bake_prompt(plate["prompt"].strip() + FACE)
    print(f"\n=== {pid} ===", flush=True)
    submit(page, prompt)
    wait_done(page, marker)
    download_by_marker(page, dest, marker)
    try:
        veo.strip_audio(dest)
    except Exception as e:
        print(f"  strip {e}", flush=True)
    dur = m.probe_dur(dest)
    if dur < 6 or dur > 12:
        raise SystemExit(f"STOP dur {dur} for {pid}")
    m.extract_qa_frames(dest, pid)
    report = {
        "plate": pid,
        "version": "v01",
        "path": str(dest),
        "bytes": dest.stat().st_size,
        "sha256": m.sha256_file(dest),
        "duration_s": dur,
        "model": "Veo 3.1 - Quality",
        "account": "benoats@googlemail.com",
        "project": PROJECT,
        "assemble": "CLOSED",
        "ts": datetime.now(timezone.utc).isoformat(),
    }
    (QA / f"{pid}_v01_mint.json").write_text(json.dumps(report, indent=2) + "\n")
    print("LANDED", json.dumps(report, indent=2), flush=True)
    return report


def main() -> None:
    board = json.loads((EDIT / "parts/part-05_plates_v01.json").read_text())
    want = sys.argv[1:] or [f"{i:02d}" for i in range(4, 12)]
    plates = []
    for p in board["plates"]:
        if any(p["id"].startswith(w) or w in p["id"] for w in want):
            if p["id"] in MARKERS:
                plates.append(p)
    if not plates:
        raise SystemExit(f"no plates for {want}")
    from playwright.sync_api import sync_playwright

    CLIP_DIR.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        page = next(pg for pg in browser.contexts[0].pages if "flow.google.com" in (pg.url or ""))
        page.bring_to_front()
        results = []
        for plate in plates:
            results.append(mint_plate(page, plate))
            page.keyboard.press("Escape")
            page.wait_for_timeout(1000)
        (QA / "BATCH_04_11_SUMMARY.json").write_text(
            json.dumps({"results": results, "ts": datetime.now(timezone.utc).isoformat()}, indent=2)
            + "\n"
        )
        print("BATCH_DONE", flush=True)


if __name__ == "__main__":
    main()
