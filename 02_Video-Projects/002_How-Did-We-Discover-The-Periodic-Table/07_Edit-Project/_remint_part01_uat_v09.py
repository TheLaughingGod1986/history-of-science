#!/usr/bin/env python3
"""UAT v09 — remint residual fails: Explorer 05 opaque jar, 10 no-flames, 11/12 opaque.

Duration guard rejects Flow contamination outside ~6–12s.
"""
from __future__ import annotations

import json
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
PLATES_JSON = PROJ / "07_Edit-Project/parts/part-01_plates_v01.json"
RAW = PROJ / "04_Generated-Clips/part01/raw/v01_fast"
REJECT = PROJ / "04_Generated-Clips/part01/_rejected_uat_v09"
META = PROJ / "07_Edit-Project/part01_remint_uat_v09_meta.json"
START_05 = PROJ / "04_Generated-Clips/part01/refs/v01_stills/05_explorer_ore_gas_start_v09.jpg"
MODEL = "Veo 3.1 - Fast"
PROFILE = Path(
    os.environ.get("ORBIT_FLOW_PROFILE", str(Path.home() / ".playwright-hos-flow-profile"))
)
STYLE = (
    "History of Science locked look: premium Animistry-class 3D cartoon like Germs "
    "Part 01 — warm wood workshop, cinematic light. Not photoreal. Silent. "
    "No readable text. No Orbit. No modern news. No food. Continuous motion."
)
PHYSICS = (
    "Prefer OPAQUE jars / metal canisters / solid cylinders. "
    "Avoid clear liquid air pockets. Nothing floats above stands or pans. "
    "NO flames under rocks unless VO asks — heat shimmer only."
)
# (plate_id, mode) — i2v uses START_05; t2v is scenery_only
JOBS = (
    ("05_explorer_ore_gas", "i2v"),
    ("10_rock_not_fire", "t2v"),
    ("11_chemists_more_names", "t2v"),
    ("12_workshop_hold", "t2v"),
)


def probe_dur(path: Path) -> float:
    out = subprocess.check_output(
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
    return float(out)


def archive_after_success(pid: str, new_path: Path) -> None:
    prev = RAW / f"{pid}_v01.mp4"
    if prev.exists() and prev.resolve() != new_path.resolve():
        REJECT.mkdir(parents=True, exist_ok=True)
        dest = REJECT / f"{pid}_v01.mp4"
        if dest.exists():
            dest.unlink()
        shutil.move(str(prev), str(dest))
        print(f"  archived previous {dest.name}", flush=True)
    if new_path.resolve() != prev.resolve():
        if prev.exists():
            prev.unlink()
        shutil.move(str(new_path), str(prev))


def main() -> None:
    if not START_05.exists():
        raise SystemExit(f"STOP: missing start frame {START_05}")
    plates = {p["id"]: p for p in json.loads(PLATES_JSON.read_text())["plates"]}
    RAW.mkdir(parents=True, exist_ok=True)
    meta: dict = {"engine": "flow-ui", "model": MODEL, "mode": "uat-v09", "plates": []}
    profile = flow.profile_path(PROFILE)
    print(f"Flow UAT v09 profile={profile}", flush=True)

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        ctx, page = flow.launch_context(p, headed=True, profile=profile)
        try:
            page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
            page.wait_for_timeout(2000)
            flow.dismiss_banners(page)
            if not flow.looks_logged_in(page):
                raise SystemExit("STOP: Flow not logged in.")

            for pid, mode in JOBS:
                prompt = f"{STYLE} {PHYSICS} {plates[pid]['prompt']}"
                print(f"\n=== {mode.upper()} {pid} ===", flush=True)
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
                            start_frame=START_05 if mode == "i2v" else None,
                            scenery_only=(mode == "t2v"),
                        )
                        veo.strip_audio(tmp)
                        dur = probe_dur(tmp)
                        size = tmp.stat().st_size
                        print(f"  attempt {attempt}: dur={dur:.2f}s bytes={size}", flush=True)
                        if size < 800_000 or dur < 5.5 or dur > 12.0:
                            print("  REJECT contamination/size/duration — retry", flush=True)
                            REJECT.mkdir(parents=True, exist_ok=True)
                            bad = REJECT / f"{pid}_contam_attempt{attempt}.mp4"
                            if bad.exists():
                                bad.unlink()
                            shutil.move(str(tmp), str(bad))
                            continue
                        archive_after_success(pid, tmp)
                        dest = RAW / f"{pid}_v01.mp4"
                        meta["plates"].append(
                            {
                                "id": pid,
                                "mode": mode,
                                "duration": dur,
                                **info,
                            }
                        )
                        META.write_text(json.dumps(meta, indent=2) + "\n")
                        print(f"  SAVED {dest.name} bytes={dest.stat().st_size}", flush=True)
                        ok = True
                        break
                    except Exception as e:  # noqa: BLE001
                        last_err = e
                        print(f"  attempt {attempt} error: {e}", flush=True)
                if not ok:
                    raise SystemExit(f"STOP: failed {pid}: {last_err}")
        finally:
            ctx.close()
    print("OK UAT v09 remint finished", flush=True)


if __name__ == "__main__":
    main()
