#!/usr/bin/env python3
"""Part 05 remint — failed plates only. Fast 3.1. No Omni / Quality / Lite.

KEEP: 04_explorer_scrubs, 06_soap_hands, 07_a_map.
REMINT: 01, 02, 03, 05, 08.
If Create dies: STOP. Do not remint 01–04 of the film.
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
RAW = PROJ / "04_Generated-Clips/part05/raw/v01_fast_probe"
META = PROJ / "07_Edit-Project/part05_gen_meta_v01b.json"
MODEL = "Veo 3.1 - Fast"
PROFILE = Path(
    os.environ.get(
        "ORBIT_FLOW_PROFILE",
        str(Path.home() / ".playwright-hos-flow-profile"),
    )
)
STILL_MEAN = 1.4
STILL_FIRST = 2.0
LOCK = (
    "Premium Animistry 3D cartoon, History of Science Part 01 v08 / v21. "
    "Warm oil-lamp gold, 1860s Glasgow surgical theatre. Silent picture. "
    "Continuous camera motion the whole 8 seconds. No freeze. No Ken Burns. "
    "ZERO cartoon germ sprites. ZERO smiling microbes. ZERO eyes on germs. "
    "ZERO purple or pink blob creatures. ZERO matching-coat twins. "
    "ZERO top hats. ZERO bowler hats. ZERO metal instrument trays. "
    "ZERO modern hospital. ZERO fluorescent lights. ZERO Orbit robot. "
    "ZERO Explorer. ZERO readable text. NOT photoreal."
)

PLATES = [
    {
        "id": "01_old_theatre",
        "prompt": (
            LOCK
            + " Wide 1860s operating theatre ALREADY IN MOTION in the first frame. "
            "ONE surgeon only, dark frock, hatless, at a wooden table. "
            "If anyone else is in frame they wear DIFFERENT clothes — shirtsleeves "
            "or a waistcoat — never a matching pair. Wooden benches, oil lamps, "
            "stained linen, cloth. The room is bloody and busy. Camera already "
            "drifting. No flask. No hats. No sprites."
        ),
    },
    {
        "id": "02_spray_scrub",
        "prompt": (
            LOCK
            + " Medium: carbolic spray mist already crossing a wooden operating table. "
            "Period hands scrub tools and linen. Steam and droplet mist only — "
            "no living germ creatures in the water or air. ONE hatless person. "
            "Wooden table, tools on cloth. Empty benches behind — no audience, "
            "no gallery, no hats. Camera drifts through the mist."
        ),
    },
    {
        "id": "03_protocol",
        "prompt": (
            LOCK
            + " Medium: ONE NEW 1860s British surgeon washing as craft. He is Joseph "
            "Lister: mid-40s, receding grey-brown hair, mutton-chop sideburns, "
            "NO mustache, NOT Semmelweis, NOT the VECTOR mustache doctor. "
            "Dark frock, no hat. Stone basin, soap, cloth. Empty theatre behind "
            "him — no seated gallery. Camera orbits slowly. Clear water only. "
            "No sprites in the basin."
        ),
    },
    {
        "id": "05_theatre_wins",
        "prompt": (
            LOCK
            + " Wide living 1860s wooden theatre after the protocol works. Patients "
            "rest in wooden beds, fever receding. Nurses in blue dresses and white "
            "aprons move between beds. Warm oil lamps and brass globes only — "
            "never modern circular LED surgical lights. NO giant germs, NO "
            "microbe close-up, NO purple blobs in the air. The room itself is "
            "the hero. Camera slowly trucks through the ward. No hats."
        ),
    },
    {
        "id": "08_last_light",
        "prompt": (
            LOCK
            + " Hold on clean 1860s theatre light. Empty wooden operating table, "
            "warm oil lamps, quiet room after the win. NO flask, NO bottle, "
            "NO glassware on the table, NO microbes, NO hats, NO people. "
            "Camera slowly pushes into the lamp glow."
        ),
    },
]


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
    tmp = Path(tempfile.mkdtemp(prefix="hos_p05b_m_"))
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
    return RAW / f"{plate_id}_v01b.mp4"


def archive_old(plate_id: str) -> None:
    old = RAW / f"{plate_id}_v01.mp4"
    if not old.exists():
        return
    reject = RAW / f"_rejected_{plate_id}_v01.mp4"
    if reject.exists():
        return
    old.rename(reject)
    print(f"  archived {reject.name}", flush=True)


def still_fail(info: dict) -> bool:
    return info["motion_mean"] < STILL_MEAN or info["first_second_motion"] < STILL_FIRST


def mint_one(page, plate: dict, dest: Path) -> dict:
    print(f"  T2V {plate['id']}", flush=True)
    info = flow.generate_clip(
        page,
        plate["prompt"],
        dest,
        model=MODEL,
        start_frame=None,
        scenery_only=True,
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
    info["i2v"] = False
    print(
        f"  motion_mean={mv:.2f} first_second={first:.2f} bytes={dest.stat().st_size}",
        flush=True,
    )
    extract_frames(dest)
    return info


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    for plate in PLATES:
        archive_old(plate["id"])
    missing = [p for p in PLATES if not veo.already_done(dest_for(p["id"]), min_bytes=400_000)]
    meta: dict = {"engine": "flow-ui", "model": MODEL, "plates": []}
    if META.exists():
        try:
            meta = json.loads(META.read_text())
        except Exception:
            pass
    meta["model"] = MODEL
    meta["raw"] = str(RAW)
    if not missing:
        print("all v01b Fast clips present — no Flow", flush=True)
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
            for i, plate in enumerate(PLATES):
                dest = dest_for(plate["id"])
                if veo.already_done(dest, min_bytes=400_000):
                    print(f"  skip {dest.name}", flush=True)
                    continue
                print(
                    f"\n=== Fast remint {plate['id']} ({i+1}/{len(PLATES)}) ===",
                    flush=True,
                )
                remint_used = False
                while True:
                    try:
                        info = mint_one(page, plate, dest)
                    except Exception as e:
                        print(f"STOP: Flow failed on {plate['id']}: {e}", flush=True)
                        META.write_text(json.dumps(meta, indent=2))
                        raise SystemExit(
                            "STOP: Create died. Do not loop. "
                            f"Last plate={plate['id']}"
                        ) from e
                    if still_fail(info):
                        reject = dest.with_name(f"_rejected_still_{dest.name}")
                        dest.rename(reject)
                        print(f"  archived {reject.name}", flush=True)
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
    print("OK part 05 v01b remint finished", flush=True)


if __name__ == "__main__":
    main()
