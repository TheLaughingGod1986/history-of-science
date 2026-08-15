#!/usr/bin/env python3
"""Replace the *file* on existing YouTube videos. Same id. Same views.

YouTube Studio → video → Replace keeps:
  video id, URL, views, watch time, likes, comments, publish date.

It does NOT create a new video. Do not use `_replace_shorts_v02_youtube.py`
for this job — that script uploads a new id and deletes the old one, which
resets counters and can look like a brand-new upload to the algorithm.

Requires the logged-in Chrome profile:
  /Users/ben/code/youtube/.playwright-youtube-profile

Usage:
  python3 00_Brand/Channel-Setup/audits/_replace_media_in_place.py --dry-run
  python3 00_Brand/Channel-Setup/audits/_replace_media_in_place.py
  python3 00_Brand/Channel-Setup/audits/_replace_media_in_place.py --only 1HuV8o3gOss
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
PROFILE = "/Users/ben/code/youtube/.playwright-youtube-profile"
AUDIT = Path(__file__).resolve().parent / "playback_lag_in_place_replace"
CHANNEL = "UC_esArsDKd3GJvOkeO0DUog"
LONG_IDS = {"Mo93x0fxB1Q", "n7CbJrOCnU0", "b8-X_FyJnHM"}


def extract_long_id(data: dict) -> str:
    for key in ("long_id", "related_to_long"):
        if data.get(key):
            return str(data[key])
    for key in ("long_url", "long_placeholder"):
        m = re.search(r"youtu\.be/([A-Za-z0-9_-]{11})", data.get(key) or "")
        if m:
            return m.group(1)
    return ""



def dismiss(page) -> None:
    for name in ("Got it", "Dismiss", "Not now", "Close"):
        try:
            b = page.get_by_role("button", name=name, exact=True)
            if b.count() and b.first.is_visible():
                b.first.click(force=True, timeout=600)
        except Exception:
            pass


def collect_jobs(root: Path) -> list[dict]:
    jobs: list[dict] = []
    for index_path in sorted((root / "02_Video-Projects").glob("*/10_Shorts/SHORTS_UPLOAD_INDEX.json")):
        project_root = index_path.parents[1]
        data = json.loads(index_path.read_text())
        long_id = extract_long_id(data)
        long_file = None
        final_dir = project_root / "09_Final-Export"
        if final_dir.is_dir():
            masters = sorted(
                p
                for p in final_dir.glob("*UPLOAD_READY*.mp4")
                if "_cfr_fixed" not in p.name and not p.name.startswith("_")
            )
            if masters:
                long_file = masters[-1]
        if long_id:
            jobs.append(
                {
                    "kind": "longform",
                    "project": project_root.name,
                    "video_id": long_id,
                    "title": data.get("long_title") or (long_file.name if long_file else ""),
                    "file": str(long_file) if long_file else "",
                }
            )
        for item in data.get("shorts") or []:
            vid = item.get("youtube_video_id") or item.get("video_id")
            rel = item.get("file")
            if not vid or not rel:
                continue
            path = project_root / rel
            if not path.exists():
                # Prefer a remastered sibling if the index still points at the old name
                alt = path.with_name(path.stem + "_cfr_fixed" + path.suffix)
                path = alt if alt.exists() else path
            jobs.append(
                {
                    "kind": "short",
                    "project": project_root.name,
                    "video_id": vid,
                    "title": item.get("title") or "",
                    "file": str(path),
                    "index": str(index_path),
                }
            )
    return jobs


def click_replace_control(page) -> str:
    """Open Studio's Replace flow. Fail if it is not available — never upload new."""
    found = page.evaluate(
        """() => {
          const hit = (el) => {
            const t = ((el.innerText || '') + ' ' + (el.getAttribute('aria-label') || '')).replace(/\\s+/g, ' ').trim();
            if (/^replace( video| file)?$/i.test(t) || /replace video file/i.test(t)) {
              const r = el.getBoundingClientRect();
              if (r.width > 8 && r.height > 8) { el.click(); return t; }
            }
            return null;
          };
          const walk = (root) => {
            for (const el of root.querySelectorAll('button,ytcp-button,[role=button],ytcp-icon-button,a,span,div')) {
              const t = hit(el);
              if (t) return t;
            }
            for (const el of root.querySelectorAll('*')) {
              if (el.shadowRoot) {
                const t = walk(el.shadowRoot);
                if (t) return t;
              }
            }
            return null;
          };
          return walk(document);
        }"""
    )
    if found:
        return f"direct:{found}"
    # Overflow / options menu, then Replace
    page.evaluate(
        """() => {
          const walk = (root) => {
            for (const el of root.querySelectorAll('button,ytcp-icon-button,[role=button]')) {
              const al = (el.getAttribute('aria-label') || '').toLowerCase();
              if (al.includes('options') || al.includes('more actions') || al.includes('more options')) {
                const r = el.getBoundingClientRect();
                if (r.width > 8) { el.click(); return al; }
              }
            }
            for (const el of root.querySelectorAll('*')) {
              if (el.shadowRoot) {
                const x = walk(el.shadowRoot);
                if (x) return x;
              }
            }
            return null;
          };
          return walk(document);
        }"""
    )
    page.wait_for_timeout(600)
    found = page.evaluate(
        """() => {
          const walk = (root) => {
            for (const el of root.querySelectorAll('tp-yt-paper-item,[role=menuitem],yt-formatted-string,span,div')) {
              const t = (el.innerText || '').trim();
              if (/^Replace$/i.test(t) || /^Replace video$/i.test(t) || /^Replace file$/i.test(t)) {
                const r = el.getBoundingClientRect();
                if (r.width > 20) { el.click(); return t; }
              }
            }
            for (const el of root.querySelectorAll('*')) {
              if (el.shadowRoot) {
                const x = walk(el.shadowRoot);
                if (x) return x;
              }
            }
            return null;
          };
          return walk(document);
        }"""
    )
    if not found:
        raise RuntimeError(
            "Studio Replace control not found. Aborting rather than creating a new video "
            "(new uploads reset view count)."
        )
    return f"menu:{found}"


def set_replace_file(page, path: Path) -> None:
    inputs = page.locator('input[type="file"]')
    if inputs.count():
        inputs.last.set_input_files(str(path))
        return
    with page.expect_file_chooser(timeout=20000) as fc:
        click_replace_control(page)
    fc.value.set_files(str(path))


def confirm_replace(page) -> str:
    for label in ("Replace video", "Replace", "Confirm", "Save", "Done"):
        try:
            btn = page.get_by_role("button", name=re.compile(rf"^{label}$", re.I))
            if btn.count() and btn.last.is_enabled():
                btn.last.click(force=True, timeout=2000)
                return label
        except Exception:
            continue
    return ""


def replace_one(page, job: dict) -> dict:
    vid = job["video_id"]
    path = Path(job["file"])
    row = {"video_id": vid, "file": str(path), "kind": job["kind"], "ok": False}
    if vid in LONG_IDS and job["kind"] != "longform":
        raise RuntimeError(f"refusing to treat long-form id {vid} as a Short")
    if not path.exists():
        row["error"] = f"missing file: {path}"
        return row
    page.goto(
        f"https://studio.youtube.com/video/{vid}/edit",
        wait_until="domcontentloaded",
        timeout=120000,
    )
    page.wait_for_timeout(2800)
    dismiss(page)
    row["opened"] = page.url
    row["replace_control"] = click_replace_control(page)
    page.wait_for_timeout(800)
    set_replace_file(page, path)
    page.wait_for_timeout(1500)
    row["confirm"] = confirm_replace(page)
    page.wait_for_timeout(8000)
    dismiss(page)
    still = re.search(r"/video/([A-Za-z0-9_-]{11})/", page.url)
    row["id_after"] = still.group(1) if still else ""
    row["ok"] = row["id_after"] == vid
    if not row["ok"]:
        row["error"] = (
            f"URL video id changed from {vid} to {row['id_after']!r} — "
            "this would be a new upload. Investigate before continuing."
        )
    AUDIT.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(AUDIT / f"replace_{vid}.png"))
    return row


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=REPO)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--only", action="append", default=[], help="Limit to these video ids")
    args = ap.parse_args()
    root = args.root.expanduser().resolve()
    jobs = collect_jobs(root)
    if args.only:
        allow = set(args.only)
        jobs = [j for j in jobs if j["video_id"] in allow]
    AUDIT.mkdir(parents=True, exist_ok=True)
    plan = {
        "ran_at": datetime.now(timezone.utc).isoformat(),
        "dry_run": args.dry_run,
        "channel": CHANNEL,
        "jobs": jobs,
        "rule": "Studio Replace only. Never videos.insert / new upload for lag fixes.",
    }
    (AUDIT / "plan.json").write_text(json.dumps(plan, indent=2) + "\n")
    print(f"{len(jobs)} in-place replacements planned → {AUDIT / 'plan.json'}")
    if args.dry_run:
        for job in jobs:
            print(f"  {job['kind']:9} {job['video_id']}  {job['file']}")
        return 0

    from playwright.sync_api import sync_playwright

    results: list[dict] = []
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            PROFILE,
            headless=False,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"],
            viewport={"width": 1440, "height": 900},
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        for job in jobs:
            print(f"Replace {job['video_id']} ← {Path(job['file']).name}", flush=True)
            try:
                row = replace_one(page, job)
            except Exception as exc:
                row = {**job, "ok": False, "error": str(exc)[:400]}
                page.screenshot(path=str(AUDIT / f"err_{job['video_id']}.png"))
                for _ in range(3):
                    page.keyboard.press("Escape")
                    page.wait_for_timeout(200)
                    dismiss(page)
            results.append(row)
            print(f"  → {'OK' if row.get('ok') else 'FAIL'} {row.get('error') or row.get('id_after')}", flush=True)
        ctx.close()

    out = AUDIT / "result.json"
    out.write_text(
        json.dumps(
            {
                "ran_at": datetime.now(timezone.utc).isoformat(),
                "ok": sum(1 for r in results if r.get("ok")),
                "results": results,
            },
            indent=2,
        )
        + "\n"
    )
    print(out)
    return 0 if all(r.get("ok") for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
