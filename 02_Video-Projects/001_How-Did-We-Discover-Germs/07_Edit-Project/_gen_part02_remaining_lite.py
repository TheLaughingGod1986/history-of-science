#!/usr/bin/env python3
"""Generate remaining Part 02 plates via Flow Veo 3.1 Lite. Skip existing."""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))
import orbit_flow_veo_ui as flow  # noqa: E402
from orbit_gemini_veo import already_done, strip_audio  # noqa: E402
from playwright.sync_api import sync_playwright

PROJ = Path(__file__).resolve().parents[1]
PLATES = json.loads((PROJ / "07_Edit-Project" / "parts" / "part-02_plates_v01.json").read_text())["plates"]
REFS = PROJ / "04_Generated-Clips" / "part02" / "refs"
RAW = PROJ / "04_Generated-Clips" / "part02" / "raw" / "v01_flow"
FACELESS = (
    "Keep microbes FACELESS if present: rods/spheres/spirals only. "
    "NO eyes NO mouths NO smiles. Continuous motion whole clip — never freeze. "
    "Premium 3D cartoon matching start frame. Silent. NOT photoreal. NOT modern hospital. "
    "FORBIDDEN: photographic cameras, camcorders, film cameras, multi-lens gadgets, "
    "steampunk cameras, floating cameras inside the droplet."
)
MODEL = "Veo 3.1 - Lite"
LIMIT_RE = re.compile(
    r"generation limit|daily gen|you've reached|reached your (daily )?limit|"
    r"quota|try again tomorrow|limit for today|"
    r"Not enough Google Flow and AI credits|not enough .*credits",
    re.I,
)


def page_limit_text(page) -> str:
    try:
        return (page.inner_text("body", timeout=4000) or "")[:4000]
    except Exception:
        return ""


def is_daily_limit(err: BaseException, page) -> str | None:
    blob = f"{err}\n{page_limit_text(page)}"
    if LIMIT_RE.search(blob):
        m = LIMIT_RE.search(blob)
        # Prefer a tight window around the match.
        i = blob.lower().find(m.group(0).lower())
        snippet = blob[max(0, i - 80) : i + 240].replace("\n", " ")
        return snippet.strip()
    return None


def main() -> None:
    only = {x.strip() for x in os.environ.get("HOS_PLATE_ONLY", "04_plunge_into_drop").split(",") if x.strip()}
    RAW.mkdir(parents=True, exist_ok=True)
    for junk in RAW.glob("*.nosound.mp4"):
        if junk.stat().st_size < 400_000:
            junk.unlink(missing_ok=True)
    profile = flow.profile_path(Path.home() / ".playwright-hos-flow-profile")
    print(f"profile={profile} model={MODEL} only={sorted(only)}", flush=True)
    with sync_playwright() as p:
        ctx, page = flow.launch_context(p, headed=False, profile=profile)
        try:
            for i, plate in enumerate(PLATES, 1):
                if only and plate["id"] not in only:
                    continue
                still = REFS / plate.get("start_still", f"{plate['id']}_v01.jpg")
                dest = RAW / f"{plate['id']}_v01.mp4"
                if not still.exists():
                    raise SystemExit(f"missing still {still}")
                if already_done(dest, min_bytes=400_000):
                    print(f"  skip {dest.name} ({dest.stat().st_size})", flush=True)
                    continue
                prompt = f"{plate['prompt']} {FACELESS}"
                print(f"\n=== Lite I2V {plate['id']} ({i}/{len(PLATES)}) ===", flush=True)
                try:
                    info = flow.generate_clip(
                        page,
                        prompt,
                        dest,
                        model=MODEL,
                        start_frame=still,
                        timeout_s=900,
                        reuse_project=False,
                        scenery_only=not plate.get("explorer", False),
                        attempts=1,
                    )
                except Exception as e:
                    dump = Path("/tmp/hos_part02_plate10_flow_dump.txt")
                    body = page_limit_text(page)
                    dump.write_text(f"{e}\n\n--- body ---\n{body}\n", encoding="utf-8")
                    try:
                        page.screenshot(path="/tmp/hos_part02_plate10_flow.png", full_page=True)
                    except Exception:
                        pass
                    print(f"FAILED_AT {plate['id']}: {e}", flush=True)
                    print("--- UI body (truncated) ---", flush=True)
                    print(body[:2500], flush=True)
                    limit = is_daily_limit(e, page)
                    if limit:
                        print("DAILY_GEN_LIMIT — stop. Exact error / page snippet:", flush=True)
                        print(limit, flush=True)
                        raise SystemExit(2)
                    raise
                strip_audio(dest)
                print(f"  OK {dest.name} {dest.stat().st_size} {info.get('seconds')}s", flush=True)
        finally:
            ctx.close()
    print("DONE remaining Lite plates", flush=True)


if __name__ == "__main__":
    main()
