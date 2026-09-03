#!/usr/bin/env python3
"""Part 05 Flow Veo 3.1 Fast. I2V if Add to Prompt works; else T2V.

Do not remint 01–04. If Create dies: STOP. No Omni / Quality / Lite.
"""
from __future__ import annotations

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
PLATES_JSON = PROJ / "07_Edit-Project/parts/part-05_plates_v01.json"
REFS = PROJ / "04_Generated-Clips/part05/refs"
RAW = PROJ / "04_Generated-Clips/part05/raw/v01_fast_probe"
META = PROJ / "07_Edit-Project/part05_gen_meta_v01.json"
EXPLORER = REFS / "explorer_sheet.jpg"
MODEL = "Veo 3.1 - Fast"
PROFILE = Path(
    os.environ.get(
        "ORBIT_FLOW_PROFILE",
        str(Path.home() / ".playwright-hos-flow-profile"),
    )
)
STILL_MEAN = 1.4
STILL_FIRST = 2.0
FACELESS = (
    "Keep microbes FACELESS if present: rods/spheres/spirals only. "
    "NO eyes NO mouths NO smiles. Continuous motion whole clip — never freeze. "
    "Premium 3D cartoon. Silent. NOT photoreal. NOT modern hospital. "
    "No Orbit robot. No readable text."
)


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
    tmp = Path(tempfile.mkdtemp(prefix="hos_p05_m_"))
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


def extract_frames(mp4: Path) -> None:
    dest_dir = RAW / f"_qa_{mp4.stem}"
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


def dest_for(plate_id: str) -> Path:
    return RAW / f"{plate_id}_v01.mp4"


def archive_reject(dest: Path, tag: str) -> None:
    if not dest.exists():
        return
    reject = dest.with_name(f"_rejected_{tag}_{dest.name}")
    dest.rename(reject)
    print(f"  archived {reject.name}", flush=True)


def still_fail(info: dict) -> bool:
    return info["motion_mean"] < STILL_MEAN or info["first_second_motion"] < STILL_FIRST


def mint_one(page, plate: dict, dest: Path, *, i2v: bool) -> dict:
    prompt = f"{plate['prompt']} {FACELESS}"
    start = EXPLORER if i2v and plate.get("explorer") and EXPLORER.exists() else None
    print(
        f"  {'I2V' if start else 'T2V'} {plate['id']} start_frame={start}",
        flush=True,
    )
    info = flow.generate_clip(
        page,
        prompt,
        dest,
        model=MODEL,
        start_frame=start,
        scenery_only=start is None,
        reuse_project=False,
        attempts=1,
        timeout_s=700,
    )
    veo.strip_audio(dest)
    if not dest.exists() or dest.stat().st_size < 400_000:
        raise SystemExit(f"STOP: download missing/small {dest}")
    mv = motion_mean(dest)
    first = first_second_motion(dest)
    info["motion_mean"] = round(mv, 2)
    info["first_second_motion"] = round(first, 2)
    info["path"] = str(dest)
    info["i2v"] = bool(start)
    print(
        f"  motion_mean={mv:.2f} first_second={first:.2f} bytes={dest.stat().st_size}",
        flush=True,
    )
    extract_frames(dest)
    return info


def main() -> None:
    plates = json.loads(PLATES_JSON.read_text())["plates"]
    RAW.mkdir(parents=True, exist_ok=True)
    missing = [p for p in plates if not veo.already_done(dest_for(p["id"]), min_bytes=400_000)]
    meta: dict = {"engine": "flow-ui", "model": MODEL, "plates": []}
    if META.exists():
        try:
            meta = json.loads(META.read_text())
        except Exception:
            pass
    meta["model"] = MODEL
    meta["raw"] = str(RAW)
    if not missing:
        print("all Fast clips present — no Flow", flush=True)
        META.write_text(json.dumps(meta, indent=2))
        return

    profile = flow.profile_path(PROFILE)
    print(
        f"Flow profile={profile} model={MODEL} missing={len(missing)}",
        flush=True,
    )
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        ctx, page = flow.launch_context(p, headed=True, profile=profile)
        try:
            page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
            page.wait_for_timeout(2000)
            flow.dismiss_banners(page)
            if not flow.looks_logged_in(page):
                raise SystemExit("STOP: Flow not logged in. Do not loop.")
            for i, plate in enumerate(plates):
                dest = dest_for(plate["id"])
                if veo.already_done(dest, min_bytes=400_000):
                    print(f"  skip {dest.name}", flush=True)
                    continue
                want_i2v = bool(plate.get("i2v") and plate.get("explorer"))
                print(
                    f"\n=== Fast {plate['id']} ({i+1}/{len(plates)}) ===",
                    flush=True,
                )
                remint_used = False
                used_i2v = want_i2v
                while True:
                    try:
                        info = mint_one(page, plate, dest, i2v=used_i2v)
                    except Exception as e:
                        err = str(e)
                        if used_i2v and (
                            "Add to Prompt" in err or "start-frame" in err.lower()
                        ):
                            print(
                                f"  I2V failed ({e}) — falling back to Fast T2V",
                                flush=True,
                            )
                            used_i2v = False
                            continue
                        print(f"STOP: Flow failed on {plate['id']}: {e}", flush=True)
                        META.write_text(json.dumps(meta, indent=2))
                        raise SystemExit(
                            "STOP: Create died. Do not loop. "
                            f"Last plate={plate['id']}"
                        ) from e
                    if still_fail(info):
                        archive_reject(dest, "still")
                        if remint_used:
                            META.write_text(json.dumps(meta, indent=2))
                            raise SystemExit(
                                f"STOP: still-push on {plate['id']} after one remint. "
                                "Do not loop."
                            )
                        remint_used = True
                        print("  QA motion reject — one remint only", flush=True)
                        continue
                    break
                meta.setdefault("plates", []).append({"id": plate["id"], **info})
                META.write_text(json.dumps(meta, indent=2))
        finally:
            ctx.close()
    print("OK part 05 Fast mint finished", flush=True)


if __name__ == "__main__":
    main()
