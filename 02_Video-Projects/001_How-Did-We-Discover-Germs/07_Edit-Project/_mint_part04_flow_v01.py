#!/usr/bin/env python3
"""Part 04 Flow Veo 3.1 Fast I2V → raw/v01_fast_probe.

Remint 07_bloom_cloud v10 only. Keep 01–06, 08–12.
If Create/arrow_forward dies: STOP. Do not loop. No Quality/Lite/Omni.
Do not harvest. Do not reuse v09 harvest clip.
"""
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
PLATES_JSON = PROJ / "07_Edit-Project/parts/part-04_plates_v01.json"
REFS = PROJ / "04_Generated-Clips/part04/refs"
RAW = PROJ / "04_Generated-Clips/part04/raw/v01_fast_probe"
META = PROJ / "07_Edit-Project/part04_gen_meta_v01.json"
KEEP = {
    "01_question_mark_flask",
    "02_boil_broth",
    "03_dust_in_the_curve",
    "04_still_clear",
    "05_tip_the_trap",
    "06_explorer_watches",
    "08_passengers",
    "09_sceptics_watch",
    "10_an_address",
    "11_result_returns",
    "12_block_the_road",
}
STILL_VERS = ("v10", "v09", "v08", "v07", "v06", "v05", "v04", "v03", "v02")
ZERO_GERM_IDS = {
    "01_question_mark_flask",
    "02_boil_broth",
    "03_dust_in_the_curve",
    "04_still_clear",
    "06_explorer_watches",
    "09_sceptics_watch",
    "10_an_address",
    "11_result_returns",
    "12_block_the_road",
}
MODEL = "Veo 3.1 - Fast"
PROFILE = Path(
    os.environ.get(
        "ORBIT_FLOW_PROFILE",
        str(Path.home() / ".playwright-hos-flow-profile"),
    )
)
MOTION = (
    "SCENERY FIRST. The picture is already translating in the first second — "
    "not a hold then move, never freeze, never Ken Burns. "
    "Premium 3D cartoon matching start frame. Silent. NOT photoreal. "
    "NOT modern hospital. No Orbit robot. No readable text."
)
ZERO_GERM = (
    f"{MOTION} ZERO microbes. NO floating rods. NO spheres. NO germ overlay. "
    "NO living cloud. NO germ city. NO split-world. NO garnish germs at all."
)
GARNISH = (
    f"{MOTION} Germs garnish at most — tiny, faceless rods/spheres in the broth "
    "or on a shaft of light. NEVER a living cloud. NEVER germ-macro fill. "
    "NEVER a split-world. NO eyes NO mouths NO smiles."
)
STILL_MEAN = 1.4
STILL_FIRST = 2.0


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
    tmp = Path(tempfile.mkdtemp(prefix="hos_p04_m_"))
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


def archive_reject(dest: Path, tag: str) -> Path | None:
    if not dest.exists():
        return None
    reject = dest.with_name(f"_rejected_{tag}_{dest.name}")
    dest.rename(reject)
    print(f"  archived {reject.name}", flush=True)
    return reject


def still_for(plate_id: str) -> Path:
    for ver in STILL_VERS:
        p = REFS / f"{plate_id}_{ver}.jpg"
        if p.exists():
            return p
    return REFS / f"{plate_id}_v01.jpg"


def dest_for(plate_id: str) -> Path:
    still = still_for(plate_id)
    for ver in STILL_VERS:
        if still.name.endswith(f"_{ver}.jpg"):
            return RAW / f"{plate_id}_{ver}.mp4"
    return RAW / f"{plate_id}_v01.mp4"


def mint_one(page, plate: dict, dest: Path) -> dict:
    still = still_for(plate["id"])
    if not still.exists():
        raise SystemExit(f"STOP: missing still {still}")
    lock = ZERO_GERM if plate["id"] in ZERO_GERM_IDS else GARNISH
    prompt = f"{plate['prompt']} {lock}"
    info = flow.generate_clip(
        page,
        prompt,
        dest,
        model=MODEL,
        start_frame=still,
        timeout_s=700,
        reuse_project=False,
        scenery_only=False,
        attempts=1,
    )
    veo.strip_audio(dest)
    if not dest.exists() or dest.stat().st_size < 400_000:
        raise SystemExit(f"STOP: download missing/small {dest}")
    mv = motion_mean(dest)
    first = first_second_motion(dest)
    info["motion_mean"] = round(mv, 2)
    info["first_second_motion"] = round(first, 2)
    info["path"] = str(dest)
    print(
        f"  motion_mean={mv:.2f} first_second={first:.2f} bytes={dest.stat().st_size}",
        flush=True,
    )
    extract_frames(dest, RAW / f"_qa_{dest.stem}")
    return info


def still_fail(info: dict) -> bool:
    return (
        info["motion_mean"] < STILL_MEAN
        or info["first_second_motion"] < STILL_FIRST
    )


def main() -> None:
    plates = json.loads(PLATES_JSON.read_text())["plates"]
    RAW.mkdir(parents=True, exist_ok=True)
    for slug in sorted(KEEP):
        p = dest_for(slug)
        if not veo.already_done(p, min_bytes=400_000):
            raise SystemExit(f"STOP: keep-plate missing {p}")
        print(f"KEEP {slug} sha256={sha256(p)} — will not remint", flush=True)
    missing = [
        p for p in plates
        if p["id"] not in KEEP
        and not veo.already_done(dest_for(p["id"]), min_bytes=400_000)
    ]
    meta: dict = {"engine": "flow-ui", "model": MODEL, "plates": []}
    if META.exists():
        try:
            meta = json.loads(META.read_text())
        except Exception:
            pass
    meta["model"] = MODEL
    meta["raw"] = str(RAW)
    if not missing:
        print("nothing to mint — no Flow", flush=True)
        META.write_text(json.dumps(meta, indent=2))
        return

    profile = flow.profile_path(PROFILE)
    print(
        f"Flow profile={profile} model={MODEL} missing={len(missing)} raw={RAW}",
        flush=True,
    )
    from playwright.sync_api import sync_playwright

    failed: list[str] = []
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
                if plate["id"] in KEEP:
                    print(f"  skip keep {dest.name}", flush=True)
                    continue
                if veo.already_done(dest, min_bytes=400_000):
                    print(f"  skip {dest.name}", flush=True)
                    continue
                print(
                    f"\n=== Fast I2V {plate['id']} ({i+1}/{len(plates)}) ===",
                    flush=True,
                )
                try:
                    info = mint_one(page, plate, dest)
                except Exception as e:
                    print(f"STOP: Flow failed on {plate['id']}: {e}", flush=True)
                    META.write_text(json.dumps(meta, indent=2))
                    raise SystemExit(
                        "STOP: Create/arrow_forward died. Do not loop. "
                        f"Last plate={plate['id']}"
                    ) from e
                if still_fail(info):
                    archive_reject(dest, "still")
                    print(
                        f"  still-push on {plate['id']} — one remint only",
                        flush=True,
                    )
                    try:
                        info = mint_one(page, plate, dest)
                    except Exception as e:
                        print(f"STOP: remint Flow failed on {plate['id']}: {e}", flush=True)
                        META.write_text(json.dumps(meta, indent=2))
                        raise SystemExit(
                            "STOP: Create died on remint. Do not loop. "
                            f"Last plate={plate['id']}"
                        ) from e
                    if still_fail(info):
                        archive_reject(dest, "still2")
                        META.write_text(json.dumps(meta, indent=2))
                        raise SystemExit(
                            f"STOP: still-push on {plate['id']} after one remint. "
                            "Do not burn another Create. QA frames extracted."
                        )
                meta.setdefault("plates", []).append({"id": plate["id"], **info})
                META.write_text(json.dumps(meta, indent=2))
        finally:
            ctx.close()
    if failed:
        print("FAILED after one remint: " + ", ".join(failed), flush=True)
    print("OK part 04 mint finished", flush=True)


if __name__ == "__main__":
    main()
