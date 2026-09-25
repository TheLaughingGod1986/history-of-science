#!/usr/bin/env python3
"""Harvest existing Flow flask-grid mp4s for Part 04 plate 07. NO Create."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))

import orbit_flow_veo_ui as flow  # noqa: E402
import orbit_gemini_veo as veo  # noqa: E402

PROJ = Path(__file__).resolve().parents[1]
RAW = PROJ / "04_Generated-Clips/part04/raw/v01_fast_probe"
META = PROJ / "07_Edit-Project/part04_harvest07_meta_v01.json"
SKIP_PROJECT = "6edb3fca-da13-423f-bfd9-08e5b40be51f"  # Part 03 plate 06 mint
PREFER_PROJECT = "99d47c3d-90ff-4167-b56c-5c00a4d0a9e7"  # 17:27 flask grid
MAX_PROJECTS = 4
MAX_TILES = 16
STILL_MEAN = 1.4
STILL_FIRST = 2.0
PROFILE = Path(
    os.environ.get(
        "ORBIT_FLOW_PROFILE",
        str(Path.home() / ".playwright-hos-flow-profile"),
    )
)


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def mean_abs(a: bytes, b: bytes) -> float:
    n = min(len(a), len(b))
    if n == 0:
        return 0.0
    return sum(abs(a[i] - b[i]) for i in range(n)) / n


def gray_at(mp4: Path, t: float, w: int = 320, h: int = 180) -> bytes:
    return subprocess.check_output(
        [
            "ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(mp4),
            "-frames:v", "1", "-vf", f"scale={w}:{h},format=gray",
            "-f", "rawvideo", "-pix_fmt", "gray", "pipe:1",
        ]
    )


def motion_mean(mp4: Path) -> float:
    tmp = Path(tempfile.mkdtemp(prefix="hos_p04_h_"))
    try:
        subprocess.run(
            [
                "ffmpeg", "-y", "-i", str(mp4),
                "-vf", "fps=8,scale=320:180,format=gray",
                str(tmp / "%03d.png"),
            ],
            check=True,
            capture_output=True,
        )
        pngs = sorted(tmp.glob("*.png"))
        arr = [
            subprocess.check_output(
                [
                    "ffmpeg", "-v", "error", "-i", str(p),
                    "-f", "rawvideo", "-pix_fmt", "gray", "pipe:1",
                ]
            )
            for p in pngs
        ]
        diffs = [mean_abs(arr[i], arr[i + 1]) for i in range(len(arr) - 1)]
        return sum(diffs) / len(diffs) if diffs else 0.0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def first_second_motion(mp4: Path) -> float:
    return mean_abs(gray_at(mp4, 0.04), gray_at(mp4, 1.00))


def extract_frames(mp4: Path, dest_dir: Path) -> None:
    dest_dir.mkdir(parents=True, exist_ok=True)
    for t, name in ((0.04, "t000"), (1.00, "t100"), (4.00, "t400"), (7.20, "t720")):
        subprocess.run(
            [
                "ffmpeg", "-y", "-ss", f"{t:.2f}", "-i", str(mp4),
                "-frames:v", "1", "-q:v", "3", str(dest_dir / f"{name}.jpg"),
            ],
            check=True,
            capture_output=True,
        )


def score(mp4: Path) -> dict:
    mv = motion_mean(mp4)
    first = first_second_motion(mp4)
    extract_frames(mp4, RAW / f"_qa_{mp4.stem}")
    return {
        "path": str(mp4),
        "bytes": mp4.stat().st_size,
        "sha256": sha256(mp4),
        "motion_mean": round(mv, 2),
        "first_second_motion": round(first, 2),
        "moves": mv >= STILL_MEAN and first >= STILL_FIRST,
    }


def project_hrefs(page) -> list[str]:
    return page.evaluate(
        """() => {
          const seen = new Set();
          const out = [];
          for (const a of document.querySelectorAll('a[href*="/project/"]')) {
            const href = a.href;
            if (!href || seen.has(href)) continue;
            seen.add(href);
            out.push(href);
          }
          return out;
        }"""
    ) or []


def click_tile(page, index: int) -> bool:
    return bool(
        page.evaluate(
            """(i) => {
              const cards = [...document.querySelectorAll(
                '[role="button"], button, a, img, video, [data-testid]'
              )].filter(el => {
                const r = el.getBoundingClientRect();
                if (r.width < 120 || r.height < 80) return false;
                if (r.y < 80 || r.bottom > window.innerHeight - 40) return false;
                const t = (el.innerText || '').trim();
                if (/new project|create|add to prompt|upload/i.test(t)) return false;
                return true;
              });
              const el = cards[i];
              if (!el) return false;
              el.click();
              return true;
            }""",
            index,
        )
    )


def download_ids(page, dest_dir: Path, seen: set[str], harvested: list[dict]) -> None:
    ids = list(flow.collect_media_ids(page))
    for mid in ids:
        if mid in seen:
            continue
        dest = dest_dir / f"_harvest_07_{mid[:8]}.mp4"
        if dest.exists() and dest.stat().st_size > 400_000:
            seen.add(mid)
            continue
        try:
            n = flow.download_media(page, mid, dest)
        except Exception as e:
            print(f"  skip mid={mid[:8]} {e}", flush=True)
            continue
        if dest.exists() and dest.stat().st_size >= 400_000:
            seen.add(mid)
            print(f"  downloaded {dest.name} bytes={n}", flush=True)
            harvested.append({"media_id": mid, **score(dest)})
        elif dest.exists():
            dest.unlink(missing_ok=True)


def harvest_project(page, url: str, seen: set[str], harvested: list[dict]) -> None:
    print(f"\n=== harvest project {url} ===", flush=True)
    page.goto(url, wait_until="domcontentloaded", timeout=120_000)
    flow.settle_after_nav(page, wait_ms=1800)
    flow.dismiss_banners(page)
    download_ids(page, RAW, seen, harvested)
    for i in range(MAX_TILES):
        if not click_tile(page, i):
            break
        page.wait_for_timeout(1600)
        download_ids(page, RAW, seen, harvested)
        vsrc = page.evaluate(
            """() => {
              const vs = [...document.querySelectorAll('video')]
                .map(v => v.currentSrc || v.src)
                .filter(Boolean);
              return vs.length ? vs[vs.length - 1] : null;
            }"""
        )
        if vsrc and vsrc.startswith("http"):
            dest = RAW / f"_harvest_07_tile{i:02d}.mp4"
            if dest.exists() and dest.stat().st_size > 400_000:
                continue
            try:
                n = flow.download_media(page, vsrc, dest)
                if dest.exists() and dest.stat().st_size >= 400_000:
                    print(f"  tile src {dest.name} bytes={n}", flush=True)
                    harvested.append({"tile": i, "src": vsrc, **score(dest)})
                elif dest.exists():
                    dest.unlink(missing_ok=True)
            except Exception as e:
                print(f"  tile src fail {e}", flush=True)


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    profile = flow.profile_path(PROFILE)
    print(f"HARVEST ONLY — no Create. profile={profile} raw={RAW}", flush=True)
    from playwright.sync_api import sync_playwright

    harvested: list[dict] = []
    seen: set[str] = set()
    with sync_playwright() as p:
        ctx, page = flow.launch_context(p, headed=True, profile=profile)
        try:
            page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
            page.wait_for_timeout(3500)
            flow.dismiss_banners(page)
            page.wait_for_timeout(800)
            if not flow.looks_logged_in(page):
                raise SystemExit("STOP: Flow not logged in. Do not Create.")
            hrefs = [h for h in project_hrefs(page) if SKIP_PROJECT not in h]
            hrefs.sort(key=lambda h: (PREFER_PROJECT not in h, h))
            print(f"projects={len(hrefs)}", flush=True)
            for href in hrefs[:MAX_PROJECTS]:
                print(f"  {href}", flush=True)
            prefer = [h for h in hrefs if PREFER_PROJECT in h]
            rest = [h for h in hrefs if PREFER_PROJECT not in h]
            ordered = prefer + rest
            if not ordered:
                raise SystemExit("STOP: no Flow projects to harvest. Do not Create yet.")
            for href in ordered[:MAX_PROJECTS]:
                harvest_project(page, href, seen, harvested)
                if any(h.get("moves") for h in harvested):
                    print("moving take found — stop visiting more projects", flush=True)
                    break
        finally:
            ctx.close()

    moving = [h for h in harvested if h.get("moves")]
    META.write_text(json.dumps({"harvested": harvested, "moving": moving}, indent=2))
    print(f"\nHARVESTED {len(harvested)}  MOVING {len(moving)}", flush=True)
    for h in harvested:
        print(
            f"  {Path(h['path']).name} mean={h['motion_mean']} "
            f"first={h['first_second_motion']} moves={h['moves']}",
            flush=True,
        )
    if not harvested:
        raise SystemExit("STOP: harvested zero mp4s from Flow grid.")


if __name__ == "__main__":
    main()
