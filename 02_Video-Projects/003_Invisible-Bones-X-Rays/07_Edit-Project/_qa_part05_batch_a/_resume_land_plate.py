#!/usr/bin/env python3
"""Wait for Flow % to clear, then tile-download newest clip as PLATE_ID_v01.mp4."""
from __future__ import annotations
import importlib.util, json, os, re, sys, time
from datetime import datetime, timezone
from pathlib import Path

REPO = Path("/Users/benjaminoats/YouTube/History Of Science")
EDIT = REPO / "02_Video-Projects/003_Invisible-Bones-X-Rays/07_Edit-Project"
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))
import orbit_flow_veo_ui as flow
import orbit_gemini_veo as veo

spec = importlib.util.spec_from_file_location("hos_mint04", EDIT / "_mint_part04_batch_a.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

QA = EDIT / "_qa_part05_batch_a"
CLIP_DIR = REPO / "02_Video-Projects/003_Invisible-Bones-X-Rays/04_Generated-Clips/part05"
PROJECT = os.environ.get(
    "HOS_003_P05_FLOW_PROJECT",
    "https://flow.google.com/u/0/project/02ce23ba-3f6d-49ee-8177-67af2d9a1166",
)
PLATE = os.environ["HOS_P05_PLATE"]
DEST = CLIP_DIR / f"{PLATE}_v01.mp4"
CDP = "http://127.0.0.1:9222"


def tile_download(page, dest: Path) -> bool:
    for _ in range(3):
        page.keyboard.press("Escape")
        page.wait_for_timeout(120)
    flow.dismiss_banners(page)
    box = page.evaluate(
        """() => {
          const imgs = [...document.querySelectorAll('img')].filter(i =>
            /Generated video thumbnail/i.test(i.alt || '') || /\\/asb\\//.test(i.src || i.currentSrc || ''));
          if (!imgs.length) return null;
          const img = imgs[imgs.length - 1];
          img.scrollIntoView({block:'center'});
          const r = img.getBoundingClientRect();
          return {x:r.x+r.width/2, y:r.y+r.height/2, n:imgs.length};
        }"""
    )
    print(f"  thumbs click {box}", flush=True)
    if not box:
        return False
    page.mouse.click(box["x"], box["y"])
    page.wait_for_timeout(1800)
    dls = page.evaluate(
        """() => [...document.querySelectorAll('button,a,[role=button]')].map(el => {
          const t = ((el.innerText||'')+' '+(el.getAttribute('aria-label')||'')).trim().replace(/\\n/g,' ');
          const r = el.getBoundingClientRect();
          return {t:t.slice(0,80), x:r.x+r.width/2, y:r.y+r.height/2,
                  visible: r.width>8 && r.height>8 && r.y>=0};
        }).filter(o => /download/i.test(o.t) && o.visible && !/batch/i.test(o.t))"""
    )
    for d in dls or []:
        try:
            print(f"  try {d['t']!r}", flush=True)
            with page.expect_download(timeout=90_000) as di:
                page.mouse.click(d["x"], d["y"])
                page.wait_for_timeout(500)
                item = page.evaluate(
                    """() => {
                      for (const el of document.querySelectorAll('[role=menuitem],button,a,.mat-mdc-menu-item')) {
                        const t = ((el.innerText||'')+' '+(el.getAttribute('aria-label')||'')).trim();
                        if (/mp4|original|720|1080|video/i.test(t) && !/image|png|jpeg|batch/i.test(t)) {
                          const r = el.getBoundingClientRect();
                          if (r.width > 20) return {t:t.slice(0,60), x:r.x+r.width/2, y:r.y+r.height/2};
                        }
                      }
                      return null;
                    }"""
                )
                if item:
                    print(f"  menu {item.get('t')!r}", flush=True)
                    page.mouse.click(item["x"], item["y"])
            dl = di.value
            raw = None
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
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(raw)
                print(f"  saved bytes={len(raw)}", flush=True)
                return True
        except Exception as e:
            print(f"  fail {type(e).__name__}: {e}", flush=True)
            try:
                page.keyboard.press("Escape")
            except Exception:
                pass
            page.wait_for_timeout(300)
    return False


def main() -> None:
    from playwright.sync_api import sync_playwright

    CLIP_DIR.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        page = next(pg for pg in browser.contexts[0].pages if "flow.google.com" in (pg.url or ""))
        page.bring_to_front()
        page.goto(PROJECT.split("/edit/")[0], wait_until="domcontentloaded", timeout=120_000)
        flow.settle_after_nav(page, wait_ms=1500)
        flow.dismiss_banners(page)
        aria = page.evaluate(
            """() => { const a=document.querySelector('a[aria-label*="Google Account"]');
               return a && a.getAttribute('aria-label'); }"""
        )
        print(f"chip {aria}", flush=True)
        if not aria or "googlemail" not in aria.lower():
            raise SystemExit(f"STOP wrong account {aria}")

        t0 = time.time()
        last = ""
        ready_streak = 0
        while time.time() - t0 < 900:
            flow.dismiss_banners(page)
            body = page.locator("body").inner_text(timeout=8000)
            pcts = [int(x) for x in re.findall(r"(\d{1,3})%", body)]
            active = [x for x in pcts if x < 100]
            thumbs = page.evaluate(
                """() => [...document.querySelectorAll('img')].filter(i =>
                  /Generated video thumbnail/i.test(i.alt||'') || /\\/asb\\//.test(i.src||'')).length"""
            )
            line = f"wait {int(time.time()-t0)}s pct={pcts[-5:] if pcts else None} thumbs={thumbs} active={active}"
            if line != last:
                print(line, flush=True)
                last = line
            page.screenshot(path=str(QA / f"{PLATE}_RESUME_progress.png"), full_page=False)

            # Ready when we have at least as many thumbs as we expect and no active %
            # For plate 02 after 01: want thumbs>=2 and no active pct
            min_thumbs = int(os.environ.get("HOS_P05_MIN_THUMBS", "2"))
            if not active and thumbs >= min_thumbs:
                ready_streak += 1
            else:
                ready_streak = 0
            if ready_streak >= 2:
                print("ready — downloading", flush=True)
                if tile_download(page, DEST):
                    break
                ready_streak = 0
            page.wait_for_timeout(7000)
        else:
            print("timeout — final download attempt", flush=True)
            if not tile_download(page, DEST):
                raise SystemExit(f"STOP: no land {PLATE}")

        try:
            veo.strip_audio(DEST)
        except Exception as e:
            print(f"strip {e}", flush=True)
        dur = m.probe_dur(DEST)
        if dur < 6 or dur > 12:
            raise SystemExit(f"STOP duration {dur}")
        m.extract_qa_frames(DEST, PLATE)
        report = {
            "plate": PLATE,
            "version": "v01",
            "path": str(DEST),
            "bytes": DEST.stat().st_size,
            "sha256": m.sha256_file(DEST),
            "duration_s": dur,
            "model": "Veo 3.1 - Quality",
            "account": "benoats@googlemail.com",
            "project": page.url,
            "assemble": "CLOSED",
            "harvest": "tile_download_resume",
            "ts": datetime.now(timezone.utc).isoformat(),
        }
        (QA / f"{PLATE}_v01_mint.json").write_text(json.dumps(report, indent=2) + "\n")
        print("LANDED", json.dumps(report, indent=2), flush=True)


if __name__ == "__main__":
    main()
