#!/usr/bin/env python3
"""HOS 003 Part 05 Batch A — mint plates 02–11 (skip existing) on googlemail u/0 project."""
from __future__ import annotations

import importlib.util
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
EDIT = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))

import orbit_flow_veo_ui as flow  # noqa: E402
import orbit_gemini_veo as veo  # noqa: E402

_spec = importlib.util.spec_from_file_location("hos_mint04", EDIT / "_mint_part04_batch_a.py")
m = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(m)

ACCOUNT = "benoats@googlemail.com"
MODEL = "Veo 3.1 - Quality"
PROJECT = os.environ.get(
    "HOS_003_P05_FLOW_PROJECT",
    "https://flow.google.com/u/0/project/02ce23ba-3f6d-49ee-8177-67af2d9a1166",
)
CDP = os.environ.get("HOS_003_FLOW_CDP", "http://127.0.0.1:9222")
CLIP_DIR = (
    REPO
    / "02_Video-Projects"
    / "003_Invisible-Bones-X-Rays"
    / "04_Generated-Clips"
    / "part05"
)
QA_DIR = EDIT / "_qa_part05_batch_a"
BOARD = EDIT / "parts" / "part-05_plates_v01.json"

FACE_LOCK = (
    " Readable Animistry cartoon faces with eyes and nose when any person appears — "
    "HARD FAIL blank mannequin ovals. No DNA helix."
)


def load_plates() -> list[dict]:
    data = json.loads(BOARD.read_text(encoding="utf-8"))
    plates = data["plates"] if isinstance(data, dict) and "plates" in data else data
    # skip 01 — already landed
    return [p for p in plates if not str(p.get("id", "")).startswith("01_")]


def ensure_googlemail(page) -> None:
    aria = page.evaluate(
        """() => {
          const a = document.querySelector('a[aria-label*="Google Account"]');
          return a && a.getAttribute('aria-label');
        }"""
    ) or ""
    if "googlemail.com" not in aria.lower():
        raise SystemExit(f"STOP: wrong Flow account chip={aria!r} — need benoats@googlemail.com")
    print(f"  account chip ok: googlemail", flush=True)


def tile_download(page, dest: Path) -> bool:
    """Open newest Generated video thumbnail and download 720p original."""
    for _ in range(3):
        page.keyboard.press("Escape")
        page.wait_for_timeout(120)
    flow.dismiss_banners(page)
    box = page.evaluate(
        """() => {
          const imgs = [...document.querySelectorAll('img')].filter(i =>
            /Generated video thumbnail/i.test(i.alt || '') || /\\/asb\\//.test(i.src || i.currentSrc || '')
          );
          if (!imgs.length) return null;
          const img = imgs[imgs.length - 1];
          img.scrollIntoView({block:'center'});
          const r = img.getBoundingClientRect();
          return {x:r.x+r.width/2, y:r.y+r.height/2};
        }"""
    )
    if not box:
        print("  tile_download: no thumbnail", flush=True)
        return False
    page.mouse.click(box["x"], box["y"])
    page.wait_for_timeout(1800)
    dls = page.evaluate(
        """() => [...document.querySelectorAll('button, a, [role=button]')].map(el => {
          const t = ((el.innerText||'') + ' ' + (el.getAttribute('aria-label')||'')).trim().replace(/\\n/g,' ');
          const r = el.getBoundingClientRect();
          return {t:t.slice(0,80), x:r.x+r.width/2, y:r.y+r.height/2,
                  visible: r.width>8 && r.height>8 && r.y>=0 && r.x>=0};
        }).filter(o => /download/i.test(o.t) && o.visible && !/batch/i.test(o.t))"""
    )
    for d in dls or []:
        try:
            print(f"  tile_download trying {d['t']!r}", flush=True)
            with page.expect_download(timeout=60_000) as di:
                page.mouse.click(d["x"], d["y"])
                page.wait_for_timeout(500)
                item = page.evaluate(
                    """() => {
                      const items = [...document.querySelectorAll(
                        '[role=menuitem], button, a, .mat-mdc-menu-item')];
                      for (const el of items) {
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
                    print(f"  menu → {item.get('t')!r}", flush=True)
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
                tmp = dest.with_suffix(".download.tmp")
                dl.save_as(str(tmp))
                raw = tmp.read_bytes()
                tmp.unlink(missing_ok=True)
            if raw and len(raw) > 150_000 and b"ftyp" in raw[:64]:
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(raw)
                print(f"  tile_download saved bytes={len(raw)}", flush=True)
                return True
        except Exception as e:
            print(f"  tile_download fail {type(e).__name__}: {e}", flush=True)
            try:
                page.keyboard.press("Escape")
            except Exception:
                pass
            page.wait_for_timeout(400)
    return False


def mint_one(page, plate: dict, timeout_s: int) -> dict:
    pid = plate["id"]
    dest = CLIP_DIR / f"{pid}_v01.mp4"
    if dest.exists() and dest.stat().st_size > 150_000:
        print(f"SKIP existing {dest}", flush=True)
        return {"plate": pid, "status": "skipped_existing", "path": str(dest)}

    prompt = m.bake_prompt((plate.get("prompt") or "").strip() + FACE_LOCK)
    if prompt.lstrip().lower().startswith("same dna soft background"):
        raise SystemExit("STOP: banned DNA opener")

    print(f"\n=== MINT {pid} Quality ===", flush=True)
    (QA_DIR / f"{pid}_SUBMITTED.json").write_text(
        json.dumps(
            {
                "plate": pid,
                "status": "about_to_submit",
                "model": MODEL,
                "account": ACCOUNT,
                "project": page.url,
                "ts": datetime.now(timezone.utc).isoformat(),
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    before_ids = flow.collect_media_ids(page)
    before_asb = set(flow.collect_gallery_asb_srcs(page))
    unpaid_retry = False
    try:
        meta = m.one_create(page, prompt, dest, timeout_s)
    except TimeoutError:
        print("  wait timeout — tile_download fallback", flush=True)
        meta = {"fallback": "tile_download"}
        if not (dest.exists() and dest.stat().st_size > 150_000):
            # try gallery harvest then tile download
            captured: list[bytes] = []
            hit = flow.harvest_agent_gallery_mp4(page, dest, captured, before_asb=before_asb)
            print(f"  gallery hit={hit}", flush=True)
            if not (dest.exists() and dest.stat().st_size > 150_000):
                ok = tile_download(page, dest)
                if not ok:
                    raise SystemExit(f"STOP: no land after timeout {pid}")
    except RuntimeError as e:
        if str(e) != "UNPAID_FAIL":
            raise
        unpaid_retry = True
        print("  UNPAID — ONE refresh retry…", flush=True)
        page.reload(wait_until="domcontentloaded", timeout=120_000)
        flow.settle_after_nav(page, wait_ms=2000)
        flow.dismiss_banners(page)
        m.abort_guards(page, "post-refresh")
        meta = m.one_create(page, prompt, dest, timeout_s)

    if not dest.exists() or dest.stat().st_size < 150_000:
        # one_create may have submitted but harvest_newest failed
        print("  dest missing — harvest fallbacks", flush=True)
        captured = []
        flow.harvest_agent_gallery_mp4(page, dest, captured, before_asb=before_asb)
        if not (dest.exists() and dest.stat().st_size > 150_000):
            if not tile_download(page, dest):
                raise SystemExit(f"STOP: dest missing/small {dest}")

    try:
        veo.strip_audio(dest)
    except Exception as e:
        print(f"  strip_audio warn: {e}", flush=True)
    dur = m.probe_dur(dest)
    if dur < 6.0 or dur > 12.0:
        raise SystemExit(f"STOP: unexpected duration {dur:.2f}s for {pid}")
    m.extract_qa_frames(dest, pid)
    report = {
        "plate": pid,
        "version": "v01",
        "path": str(dest),
        "bytes": dest.stat().st_size,
        "sha256": m.sha256_file(dest),
        "duration_s": dur,
        "model": MODEL,
        "selected_model": meta.get("selected_model") if isinstance(meta, dict) else None,
        "account": ACCOUNT,
        "project": page.url,
        "unpaid_refresh_retry": unpaid_retry,
        "assemble": "CLOSED",
        "explorer_allowed": bool(plate.get("explorer")),
        "ts": datetime.now(timezone.utc).isoformat(),
    }
    (QA_DIR / f"{pid}_v01_mint.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    (QA_DIR / f"{pid}_SUBMITTED.json").write_text(
        json.dumps({**report, "status": "landed"}, indent=2) + "\n", encoding="utf-8"
    )
    print("LANDED", json.dumps(report, indent=2), flush=True)
    return report


def main() -> None:
    m.CLIP_DIR = CLIP_DIR
    m.QA_DIR = QA_DIR
    m.MODEL = MODEL
    m.ACCOUNT = ACCOUNT
    CLIP_DIR.mkdir(parents=True, exist_ok=True)
    QA_DIR.mkdir(parents=True, exist_ok=True)
    plates = load_plates()
    only = os.environ.get("HOS_P05_ONLY", "").strip()
    if only:
        plates = [p for p in plates if p["id"] == only or p["id"].startswith(only)]
        if not plates:
            raise SystemExit(f"STOP: no plate match HOS_P05_ONLY={only!r}")

    timeout_s = int(os.environ.get("HOS_FLOW_TIMEOUT_S", "900"))
    from playwright.sync_api import sync_playwright

    print(f"cdp {CDP}", flush=True)
    print(f"project {PROJECT}", flush=True)
    print(f"plates {[p['id'] for p in plates]}", flush=True)

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        ctx = browser.contexts[0]
        page = None
        for pg in ctx.pages:
            if "flow.google.com" in (pg.url or ""):
                page = pg
                break
        if page is None:
            page = ctx.new_page()
        page.bring_to_front()
        page.goto(PROJECT, wait_until="domcontentloaded", timeout=120_000)
        flow.settle_after_nav(page, wait_ms=2000)
        flow.dismiss_banners(page)
        ensure_googlemail(page)
        # rename title if editable
        try:
            tb = page.get_by_role("textbox", name="Editable text")
            if tb.count():
                tb.first.click(timeout=3000)
                page.keyboard.press("Meta+A")
                page.keyboard.type("HOS 003 Part 05 Batch A", delay=8)
                page.keyboard.press("Enter")
                page.wait_for_timeout(400)
        except Exception as e:
            print(f"  rename warn: {e}", flush=True)

        results = []
        for plate in plates:
            ensure_googlemail(page)
            results.append(mint_one(page, plate, timeout_s))
            # brief settle between Creates
            page.wait_for_timeout(1500)
            try:
                page.keyboard.press("Escape")
            except Exception:
                pass

        summary = {
            "results": results,
            "assemble": "CLOSED",
            "ts": datetime.now(timezone.utc).isoformat(),
        }
        (QA_DIR / "BATCH_A_02_11_SUMMARY.json").write_text(
            json.dumps(summary, indent=2) + "\n", encoding="utf-8"
        )
        print("BATCH_DONE", json.dumps(summary, indent=2), flush=True)


if __name__ == "__main__":
    main()
