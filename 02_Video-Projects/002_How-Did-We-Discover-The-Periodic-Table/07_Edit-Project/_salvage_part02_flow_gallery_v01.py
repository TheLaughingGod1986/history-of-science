#!/usr/bin/env python3
"""Salvage already-rendered Flow gallery videos into Part 02 raw slots.

Does NOT spend new Ultra credits. Downloads playable gallery mp4s from the
open HOS Flow project into unused plate filenames (duration-gated).
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))
import orbit_flow_veo_ui as flow  # noqa: E402

PROJ = Path(__file__).resolve().parents[1]
PLATES = PROJ / "07_Edit-Project/parts/part-02_plates_v01.json"
RAW = PROJ / "04_Generated-Clips/part02/raw/v01_fast"
OUT_DIR = PROJ / "04_Generated-Clips/part02/raw/_salvage_gallery_v01"
PROFILE = Path(
    os.environ.get(
        "ORBIT_FLOW_PROFILE",
        str(Path.home() / ".playwright-hos-flow-profile"),
    )
)


def probe(path: Path) -> float:
    return float(
        subprocess.check_output(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=nw=1:nk=1",
                str(path),
            ],
            text=True,
        ).strip()
    )


def main() -> None:
    plates = json.loads(PLATES.read_text())["plates"]
    RAW.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    profile = flow.profile_path(PROFILE)
    print(f"salvage gallery profile={profile}", flush=True)

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        headed = os.environ.get("ORBIT_FLOW_HEADED", "1") not in {"0", "false", "False"}
        ctx, page = flow.launch_context(p, headed=headed, profile=profile)
        try:
            page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
            page.wait_for_timeout(2000)
            flow.dismiss_banners(page)
            flow.ensure_project(page)
            flow.dismiss_banners(page)
            flow.click_visible(page, "Videos") or flow.click_visible(page, "All")
            page.wait_for_timeout(1500)
            body = ""
            try:
                body = page.locator("body").inner_text(timeout=5000)[:2500]
            except Exception:
                pass
            low = body.lower()
            if "usage limit" in low or "credit limit" in low:
                print("WARN: Flow still shows usage/credit limit on page", flush=True)
            ids = sorted(flow.collect_media_ids(page))
            print(f"media ids found: {len(ids)}", flush=True)
            saved: list[Path] = []
            for i, mid in enumerate(ids, 1):
                dest = OUT_DIR / f"gallery_{i:02d}.mp4"
                if dest.exists() and dest.stat().st_size > 200_000:
                    print(f"  skip existing {dest.name}", flush=True)
                    saved.append(dest)
                    continue
                try:
                    n = flow.download_media(page, mid, dest)
                    print(f"  downloaded {dest.name} bytes={n}", flush=True)
                    if n > 150_000:
                        saved.append(dest)
                    else:
                        dest.unlink(missing_ok=True)
                except Exception as e:  # noqa: BLE001
                    print(f"  skip {mid[:48]}… {e}", flush=True)

            usable: list[tuple[Path, float]] = []
            for path in saved:
                try:
                    d = probe(path)
                except Exception:
                    continue
                if 5.0 <= d <= 40.0 and path.stat().st_size > 150_000:
                    usable.append((path, d))
            print(f"usable salvaged: {len(usable)}", flush=True)

            filled = 0
            for plate, (src, d) in zip(plates, usable):
                dest = RAW / f"{plate['id']}_v01.mp4"
                if dest.exists() and dest.stat().st_size > 400_000:
                    print(f"  plate {plate['id']} already filled", flush=True)
                    continue
                dest.write_bytes(src.read_bytes())
                print(f"  mapped {src.name} → {dest.name} dur={d:.2f}", flush=True)
                filled += 1
            print(f"OK salvage mapped={filled}/{len(plates)}", flush=True)
            shot = OUT_DIR / "gallery_salvage_stall.png"
            try:
                page.screenshot(path=str(shot), full_page=False, timeout=10_000)
                print(f"screenshot {shot}", flush=True)
            except Exception as e:  # noqa: BLE001
                print(f"screenshot skipped: {e}", flush=True)
        finally:
            ctx.close()


if __name__ == "__main__":
    main()
