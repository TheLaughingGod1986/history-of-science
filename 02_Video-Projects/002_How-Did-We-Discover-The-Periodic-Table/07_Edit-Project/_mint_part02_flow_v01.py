#!/usr/bin/env python3
"""Mint HOS 002 Part 02 Flow Veo 3.1 Fast plates.

Applies PART01_LESSONS physics lock. Explorer once on 05 (T2V identity lock).
Duration guard rejects contamination outside ~6–12s.
"""
from __future__ import annotations

import json
import traceback
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))
import orbit_flow_veo_ui as flow  # noqa: E402
import orbit_gemini_veo as veo  # noqa: E402

PROJ = Path(__file__).resolve().parents[1]
PLATES_JSON = PROJ / "07_Edit-Project/parts/part-02_plates_v01.json"
RAW = PROJ / "04_Generated-Clips/part02/raw/v01_fast"
REJECT = PROJ / "04_Generated-Clips/part02/_rejected_mint_v01"
META = PROJ / "07_Edit-Project/part02_mint_v01_meta.json"
MODEL = "Veo 3.1 - Fast"
PROFILE = Path(
    os.environ.get("ORBIT_FLOW_PROFILE", str(Path.home() / ".playwright-hos-flow-profile"))
)
STYLE = (
    "History of Science locked look: premium Animistry-class 3D cartoon like Germs "
    "Part 01 and Periodic Table Part 01 PASS — warm wood period workshop, cinematic light. "
    "Not photoreal. Not live-action. Not a modern lab. Silent picture. "
    "No readable text, logos, or UI. No Orbit orange robot. Continuous motion the whole clip. "
)
PHYSICS = (
    "Prefer OPAQUE ceramic jars / sealed metal canisters / solid cylinders. "
    "ZERO clear glass flasks with liquid. ZERO bubbles floating in air. "
    "ZERO floating glassware. Objects sit IN or ON contact surfaces. "
    "Heat shimmer colourless only — no flames unless asked. "
)


def probe_dur(path: Path) -> float:
    return float(
        subprocess.check_output(
            [
                "ffprobe", "-v", "error", "-show_entries", "format=duration",
                "-of", "default=nw=1:nk=1", str(path),
            ],
            text=True,
        ).strip()
    )


def main() -> None:
    data = json.loads(PLATES_JSON.read_text())
    plates = data["plates"]
    RAW.mkdir(parents=True, exist_ok=True)
    REJECT.mkdir(parents=True, exist_ok=True)
    meta: dict = {"engine": "flow-ui", "model": MODEL, "mode": "part02-mint-v01", "plates": []}
    if META.exists():
        try:
            meta = json.loads(META.read_text())
        except Exception:
            pass
    profile = flow.profile_path(PROFILE)
    print(f"Flow Part 02 mint profile={profile} plates={len(plates)}", flush=True)

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        headed = os.environ.get("ORBIT_FLOW_HEADED", "1") not in {"0", "false", "False"}
        print(f"headed={headed}", flush=True)
        ctx, page = flow.launch_context(p, headed=headed, profile=profile)
        try:
            page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
            page.wait_for_timeout(2000)
            flow.dismiss_banners(page)
            if not flow.looks_logged_in(page):
                print(f"WARN looks_logged_in=False url={page.url}", flush=True)
                try:
                    body = page.locator("body").inner_text(timeout=5000)[:1500].lower()
                except Exception:
                    body = ""
                if "new project" not in body and "flow.google.com" not in (page.url or "").lower():
                    raise SystemExit("STOP: Flow not logged in.")
                print("  continuing — Flow UI reachable", flush=True)

            for i, plate in enumerate(plates):
                pid = plate["id"]
                dest = RAW / f"{pid}_v01.mp4"
                if veo.already_done(dest, min_bytes=800_000):
                    try:
                        d = probe_dur(dest)
                    except Exception:
                        d = 0.0
                    if 5.5 <= d <= 12.0:
                        print(f"  skip {dest.name} dur={d:.2f}", flush=True)
                        continue
                    bad = REJECT / f"{pid}_bad_existing.mp4"
                    if bad.exists():
                        bad.unlink()
                    shutil.move(str(dest), str(bad))
                    print(f"  archived bad existing {bad.name}", flush=True)

                prompt = f"{STYLE} {PHYSICS} {plate['prompt']}"
                # Always scenery_only=True — False attaches the Orbit robot ref (wrong channel).
                # Explorer identity is locked in the prompt text (Germs Part 01 younger boy).
                scenery = True
                print(
                    f"\n=== {i+1}/{len(plates)} T2V {pid} explorer={bool(plate.get('explorer'))} ===",
                    flush=True,
                )
                ok = False
                last_err: Exception | None = None
                for attempt in range(1, 4):
                    tmp = RAW / f"{pid}_v01_tmp.mp4"
                    if tmp.exists():
                        tmp.unlink()
                    try:
                        info = flow.generate_clip(
                            page,
                            prompt,
                            tmp,
                            model=MODEL,
                            reuse_project=False,
                            attempts=1,
                            timeout_s=420,
                            start_frame=None,
                            scenery_only=scenery,
                        )
                        veo.strip_audio(tmp)
                        dur = probe_dur(tmp)
                        size = tmp.stat().st_size
                        print(f"  attempt{attempt} dur={dur:.2f}s bytes={size}", flush=True)
                        if size < 800_000 or dur < 5.5 or dur > 12.0:
                            bad = REJECT / f"{pid}_contam_attempt{attempt}.mp4"
                            if bad.exists():
                                bad.unlink()
                            shutil.move(str(tmp), str(bad))
                            print("  REJECT duration/size", flush=True)
                            continue
                        if dest.exists():
                            dest.unlink()
                        shutil.move(str(tmp), str(dest))
                        meta.setdefault("plates", []).append(
                            {"id": pid, "mode": "t2v", "duration": dur, "bytes": size, **info}
                        )
                        META.write_text(json.dumps(meta, indent=2) + "\n")
                        print(f"  SAVED {dest.name}", flush=True)
                        ok = True
                        break
                    except Exception as e:  # noqa: BLE001
                        last_err = e
                        print(f"  error: {e}", flush=True)
                if not ok:
                    META.write_text(json.dumps(meta, indent=2) + "\n")
                    raise SystemExit(f"STOP: failed {pid}: {last_err}")
        finally:
            ctx.close()
    print("OK Part 02 mint finished", flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        raise
