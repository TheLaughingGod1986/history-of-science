#!/usr/bin/env python3
"""Mint HOS 002 Part 02 Flow Veo 3.1 Fast plates.

Applies PART01_LESSONS physics lock. Explorer once on 05 (prompt identity).
Duration guard rejects contamination outside ~6–12s.

Crash isolation: one Playwright session per plate. When Agent UI returns
needs_gallery_harvest, end that session without ctx.close() mid-gen, settle,
then Download-harvest in a fresh process.
"""
from __future__ import annotations

import faulthandler
import signal

faulthandler.enable()
signal.signal(signal.SIGPIPE, signal.SIG_IGN)
signal.signal(signal.SIGHUP, signal.SIG_IGN)
signal.signal(signal.SIGTERM, signal.SIG_DFL)

import json
import os
import shutil
import subprocess
import sys
import time
import traceback
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
    os.environ.get(
        "ORBIT_FLOW_PROFILE",
        str(Path.home() / ".playwright-hos-flow-profile"),
    )
)
PINNED_DEFAULT = (
    "https://flow.google.com/u/1/project/30a34afb-8d9c-4eac-83ba-012d97f6b1b5"
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
HARVEST = Path(__file__).resolve().parent / "_harvest_newest_gallery_v01.py"


def probe_dur(path: Path) -> float:
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


def open_flow(p, *, headed: bool, profile: Path, pinned: str):
    ctx, page = flow.launch_context(p, headed=headed, profile=profile)
    flow.ensure_flow_account(page)
    page.goto(pinned, wait_until="domcontentloaded", timeout=120_000)
    page.wait_for_timeout(2000)
    flow.dismiss_banners(page)
    print(f"  mint project={page.url}", flush=True)
    if not flow.looks_logged_in(page):
        print(f"WARN looks_logged_in=False url={page.url}", flush=True)
        try:
            body = page.locator("body").inner_text(timeout=5000)[:1500].lower()
        except Exception:
            body = ""
        if "new project" not in body and "flow.google.com" not in (page.url or "").lower():
            try:
                ctx.close()
            except Exception:
                pass
            raise SystemExit("STOP: Flow not logged in.")
        print("  continuing — Flow UI reachable", flush=True)
    return ctx, page


def run_harvest(dest: Path, project_url: str) -> None:
    settle = int(os.environ.get("HOS_FLOW_HARVEST_SETTLE_S", "70"))
    wait_s = int(os.environ.get("HOS_FLOW_HARVEST_WAIT_S", "180"))
    print(f"  settle {settle}s then harvest wait_s={wait_s}", flush=True)
    # Sleep in small slices so a late Playwright SIGPIPE cannot kill a long sleep.
    end = time.time() + settle
    while time.time() < end:
        time.sleep(min(5.0, max(0.1, end - time.time())))
    env = dict(os.environ)
    env["HOS_FLOW_PROJECT_URL"] = project_url
    cmd = [
        sys.executable,
        "-u",
        str(HARVEST),
        "--out",
        str(dest),
        "--project",
        project_url,
        "--wait-s",
        str(wait_s),
    ]
    print(f"  spawn harvest: {' '.join(cmd)}", flush=True)
    # Detach from any leftover Playwright process group.
    proc = subprocess.Popen(
        cmd,
        env=env,
        start_new_session=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    assert proc.stdout is not None
    for line in proc.stdout:
        print(line, end="", flush=True)
    rc = proc.wait()
    if rc != 0:
        raise RuntimeError(f"harvest exited {rc}")


def mint_one_plate(
    *,
    prompt: str,
    dest: Path,
    headed: bool,
    profile: Path,
    pinned: str,
    reuse: bool,
) -> dict:
    from playwright.sync_api import sync_playwright

    tmp = dest.with_name(dest.stem + "_tmp.mp4")
    if tmp.exists():
        tmp.unlink()

    info: dict = {}
    with sync_playwright() as p:
        ctx, page = open_flow(p, headed=headed, profile=profile, pinned=pinned)
        try:
            info = flow.generate_clip(
                page,
                prompt,
                tmp,
                model=MODEL,
                reuse_project=reuse,
                attempts=1,
                timeout_s=420,
                start_frame=None,
                scenery_only=True,
            )
        finally:
            # Never ctx.close() mid-gen — that SIGPIPEs the mint process.
            if not info.get("needs_gallery_harvest"):
                try:
                    ctx.close()
                except Exception:
                    pass

    if info.get("needs_gallery_harvest"):
        project_url = info.get("project_url") or pinned
        print("  playwright session ended — settling for harvest…", flush=True)
        run_harvest(tmp, project_url)
        info["media_id"] = f"gallery-harvest:{tmp.stat().st_size if tmp.exists() else 0}"
        info["bytes"] = tmp.stat().st_size if tmp.exists() else 0

    return {"tmp": tmp, "info": info}


def main() -> None:
    data = json.loads(PLATES_JSON.read_text())
    plates = data["plates"]
    RAW.mkdir(parents=True, exist_ok=True)
    REJECT.mkdir(parents=True, exist_ok=True)
    meta: dict = {
        "engine": "flow-ui",
        "model": MODEL,
        "mode": "part02-mint-v01",
        "plates": [],
    }
    if META.exists():
        try:
            meta = json.loads(META.read_text())
        except Exception:
            pass

    profile = flow.profile_path(PROFILE)
    print(f"Flow Part 02 mint profile={profile} plates={len(plates)}", flush=True)
    os.environ.setdefault("ORBIT_FLOW_ACCOUNT", "benoats@googlemail.com")
    os.environ.setdefault("ORBIT_FLOW_FORCE_NEW_PROJECT", "0")
    os.environ.setdefault("ORBIT_FLOW_HOME", "https://flow.google.com/u/1/")
    if os.environ.get("HOS_FLOW_PROJECT_URL"):
        os.environ["ORBIT_FLOW_PROJECT_URL"] = os.environ["HOS_FLOW_PROJECT_URL"]

    pinned = (
        os.environ.get("HOS_FLOW_PROJECT_URL")
        or os.environ.get("ORBIT_FLOW_PROJECT_URL")
        or PINNED_DEFAULT
    )
    os.environ["ORBIT_FLOW_PROJECT_URL"] = pinned
    os.environ["HOS_FLOW_PROJECT_URL"] = pinned

    headed = os.environ.get("ORBIT_FLOW_HEADED", "1") not in {"0", "false", "False"}
    print(f"headed={headed}", flush=True)

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
        reuse = bool(
            os.environ.get("ORBIT_FLOW_REUSE_PROJECT", "1")
            not in {"0", "false", "False"}
        )
        print(
            f"\n=== {i + 1}/{len(plates)} T2V {pid} "
            f"explorer={bool(plate.get('explorer'))} reuse={reuse} ===",
            flush=True,
        )
        ok = False
        last_err: Exception | None = None
        for attempt in range(1, 4):
            try:
                result = mint_one_plate(
                    prompt=prompt,
                    dest=dest,
                    headed=headed,
                    profile=profile,
                    pinned=pinned,
                    reuse=reuse,
                )
                tmp: Path = result["tmp"]
                info: dict = result["info"]
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
                    {
                        "id": pid,
                        "mode": "t2v",
                        "duration": dur,
                        "bytes": size,
                        **{
                            k: v
                            for k, v in info.items()
                            if k != "needs_gallery_harvest"
                        },
                    }
                )
                META.write_text(json.dumps(meta, indent=2) + "\n")
                print(f"  SAVED {dest.name}", flush=True)
                ok = True
                break
            except Exception as e:  # noqa: BLE001
                last_err = e
                print(f"  error: {e}", flush=True)
                traceback.print_exc()
        if not ok:
            META.write_text(json.dumps(meta, indent=2) + "\n")
            raise SystemExit(f"STOP: failed {pid}: {last_err}")

    print("OK Part 02 mint finished", flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        raise
