#!/usr/bin/env python3
"""Part 04 Flow Veo 3.1 Fast — 05 + 06 T2V only for v14.

KEEP 07_bloom_cloud_v13 (living 0:43–0:49 splice) and all other plates.
No still. No Add to Prompt. If Create dies: STOP.
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
T2V_DESTS = {
    "06_explorer_watches": RAW / "06_explorer_watches_v14.mp4",
    "05_tip_the_trap": RAW / "05_tip_the_trap_v14.mp4",
}
T2V_ORDER = ("06_explorer_watches", "05_tip_the_trap")
T2V_IDS = set(T2V_ORDER)
KEEP = {
    "01_question_mark_flask",
    "02_boil_broth",
    "03_dust_in_the_curve",
    "04_still_clear",
    "07_bloom_cloud",
    "08_passengers",
    "09_sceptics_watch",
    "10_an_address",
    "11_result_returns",
    "12_block_the_road",
}
STILL_VERS = ("v10", "v09", "v08", "v07", "v06", "v05", "v04", "v03", "v02")
MODEL = "Veo 3.1 - Fast"
PROFILE = Path(
    os.environ.get(
        "ORBIT_FLOW_PROFILE",
        str(Path.home() / ".playwright-hos-flow-profile"),
    )
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
    if plate_id in T2V_DESTS:
        return T2V_DESTS[plate_id]
    still = still_for(plate_id)
    for ver in STILL_VERS:
        if still.name.endswith(f"_{ver}.jpg"):
            return RAW / f"{plate_id}_{ver}.mp4"
    return RAW / f"{plate_id}_v01.mp4"


def mint_t2v(page, plate: dict, dest: Path) -> dict:
    if plate["id"] not in T2V_IDS:
        raise SystemExit(f"STOP: refusing to mint {plate['id']} (only {sorted(T2V_IDS)} T2V)")
    prompt = plate["prompt"]
    print(
        f"  T2V exact prompt ({len(prompt)} chars) start_frame=None scenery_only=True",
        flush=True,
    )
    print("  will not upload 07_bloom_cloud_v10.jpg or any still — no harvest", flush=True)
    info = flow.generate_clip(
        page,
        prompt,
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
    info["t2v"] = True
    info["start_frame"] = None
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
        p = None
        for ver in ("v14", "v13", "v12", "v11", "v10", "v09", "v08", "v07", "v06", "v05", "v04", "v03", "v02", "v01"):
            cand = RAW / f"{slug}_{ver}.mp4"
            if veo.already_done(cand, min_bytes=400_000):
                p = cand
                break
        if p is None:
            raise SystemExit(f"STOP: keep-plate missing {slug}")
        print(f"KEEP {slug} sha256={sha256(p)} — will not remint", flush=True)
    missing = [
        p for p in plates
        if p["id"] not in KEEP
        and not veo.already_done(dest_for(p["id"]), min_bytes=400_000)
    ]
    extra = [p["id"] for p in missing if p["id"] not in T2V_IDS]
    if extra:
        raise SystemExit(f"STOP: unexpected missing plates {extra} — only {sorted(T2V_IDS)} T2V")
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

    with sync_playwright() as p:
        ctx, page = flow.launch_context(p, headed=True, profile=profile)
        try:
            page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
            page.wait_for_timeout(2000)
            flow.dismiss_banners(page)
            if not flow.looks_logged_in(page):
                raise SystemExit("STOP: Flow not logged in. Do not loop.")
            by_id = {p["id"]: p for p in plates}
            for i, plate_id in enumerate(T2V_ORDER):
                plate = by_id[plate_id]
                dest = dest_for(plate["id"])
                if plate["id"] in KEEP:
                    print(f"  skip keep {dest.name}", flush=True)
                    continue
                if plate["id"] not in T2V_IDS:
                    raise SystemExit(
                        f"STOP: refusing {plate['id']} — only {list(T2V_ORDER)} T2V this run"
                    )
                if veo.already_done(dest, min_bytes=400_000):
                    print(f"  skip {dest.name}", flush=True)
                    continue
                print(
                    f"\n=== Fast T2V {plate['id']} ({i+1}/{len(T2V_ORDER)}) ===",
                    flush=True,
                )
                remint_used = False
                while True:
                    try:
                        info = mint_t2v(page, plate, dest)
                    except Exception as e:
                        print(f"STOP: Flow failed on {plate['id']}: {e}", flush=True)
                        META.write_text(json.dumps(meta, indent=2))
                        raise SystemExit(
                            "STOP: Create/arrow_forward died. Do not loop. "
                            f"Last plate={plate['id']}"
                        ) from e
                    if still_fail(info):
                        archive_reject(dest, "still")
                        if remint_used:
                            META.write_text(json.dumps(meta, indent=2))
                            raise SystemExit(
                                f"STOP: still-push on {plate['id']} after one remint. "
                                "Do not loop. QA frames extracted."
                            )
                        remint_used = True
                        print(
                            "  QA motion reject — one remint only (Create still alive)",
                            flush=True,
                        )
                        continue
                    break
                meta.setdefault("plates", []).append({"id": plate["id"], **info})
                META.write_text(json.dumps(meta, indent=2))
        finally:
            ctx.close()
    print("OK part 04 T2V mint finished", flush=True)


if __name__ == "__main__":
    main()
