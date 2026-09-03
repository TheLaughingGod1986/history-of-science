#!/usr/bin/env python3
"""Part 03 Flow Veo 3.1 Fast — 04 + 09 T2V only.

SHIP GATE: EVERY two-doctor shot = THE SAME two men as KEEP 0:48 07_mocked_v12
(mustache younger, grey 1840s beard older, matching dark frocks, finished
faces, same 1840s wood ward). No top-hat twins. No new hallway pair. No hats.

KEEP 01–03, 05–08, 10. Remint 04_autopsy_to_ward + 09_they_still_sneer to v14.
Fast T2V only. If Create/arrow_forward dies: STOP. No Omni / Quality / Lite.
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
PLATES_JSON = PROJ / "07_Edit-Project/parts/part-03_plates_v02.json"
RAW = PROJ / "04_Generated-Clips/part03/raw/v02_fast_probe"
META = PROJ / "07_Edit-Project/part03_gen_meta_v14.json"
LOCKED_01 = "01_hands_arrive"
LOCKED_01_SHA = "03740f749d43be0ce5977b08713adaaf9924ea098cea6aac8a5daf40fa8e522f"
LOCKED_07 = RAW / "07_mocked_v12.mp4"
LOCKED_07_SHA = "31df8834367e43098a5b4ab7e8c8742d64b5d95e515728ed8bb6de5a6122692d"
T2V_IDS = ("04_autopsy_to_ward", "09_they_still_sneer")
T2V_DEST = {pid: RAW / f"{pid}_v14.mp4" for pid in T2V_IDS}
KEEP = {
    "01_hands_arrive",
    "02_perfume_windows",
    "03_bedside_hands",
    "05_wash_works",
    "06_explorer_crosses",
    "07_mocked",
    "08_prestige_hands",
    "10_flask_in_the_room",
}
KEEP_CLIPS = {
    "01_hands_arrive": RAW / "01_hands_arrive_v01.mp4",
    "02_perfume_windows": RAW / "02_perfume_windows_v02.mp4",
    "03_bedside_hands": RAW / "03_bedside_hands_v04.mp4",
    "05_wash_works": RAW / "05_wash_works_v03.mp4",
    "06_explorer_crosses": RAW / "06_explorer_crosses_v09.mp4",
    "07_mocked": LOCKED_07,
    "08_prestige_hands": RAW / "08_prestige_hands_v01.mp4",
    "10_flask_in_the_room": RAW / "10_flask_in_the_room_v03.mp4",
}
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
    tmp = Path(tempfile.mkdtemp(prefix="hos_p03_m_"))
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


def mint_t2v(page, plate: dict, dest: Path) -> dict:
    if plate["id"] not in T2V_IDS:
        raise SystemExit(f"STOP: refusing to mint {plate['id']} (only {T2V_IDS})")
    prompt = plate["prompt"]
    print(
        f"  T2V exact prompt ({len(prompt)} chars) start_frame=None scenery_only=True",
        flush=True,
    )
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
    spec = json.loads(PLATES_JSON.read_text())
    plates = spec["plates"]
    for pid in T2V_IDS:
        plate = next(p for p in plates if p["id"] == pid)
        low = plate["prompt"].lower()
        if "top hat" in low and "no top hat" not in low and "not use a top hat" not in low:
            raise SystemExit(f"STOP: {pid} prompt missing no-top-hat lock")
        if "SHIP GATE" not in plate["prompt"]:
            raise SystemExit(f"STOP: {pid} prompt missing SHIP GATE")
    RAW.mkdir(parents=True, exist_ok=True)
    locked = RAW / f"{LOCKED_01}_v01.mp4"
    if not veo.already_done(locked, min_bytes=400_000):
        raise SystemExit(f"STOP: locked 01 missing {locked}")
    got = sha256(locked)
    if got != LOCKED_01_SHA:
        raise SystemExit(
            f"STOP: locked 01 hash mismatch got={got} want={LOCKED_01_SHA}"
        )
    print(f"LOCKED 01 sha256={got} — will not remint", flush=True)
    if not veo.already_done(LOCKED_07, min_bytes=400_000):
        raise SystemExit(f"STOP: locked 07 missing {LOCKED_07}")
    got7 = sha256(LOCKED_07)
    if got7 != LOCKED_07_SHA:
        raise SystemExit(
            f"STOP: locked 07 hash mismatch got={got7} want={LOCKED_07_SHA}"
        )
    print(f"LOCKED 07 VECTOR 0:48 sha256={got7} — will not remint", flush=True)
    print(
        "SHIP GATE: EVERY two-doctor shot = THE SAME two men as 0:48. "
        "No top-hat twins. No new hallway pair. Fast only.",
        flush=True,
    )
    for slug, p in KEEP_CLIPS.items():
        if slug == LOCKED_01:
            continue
        if not veo.already_done(p, min_bytes=400_000):
            raise SystemExit(f"STOP: keep-plate missing {p}")
        print(f"KEEP {slug} {p.name} sha256={sha256(p)} — will not remint", flush=True)

    missing = [
        p for p in plates
        if p["id"] in T2V_IDS
        and not veo.already_done(T2V_DEST[p["id"]], min_bytes=400_000)
    ]
    extra = [p["id"] for p in missing if p["id"] not in T2V_IDS]
    if extra:
        raise SystemExit(f"STOP: unexpected missing plates {extra}")
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
            for i, plate in enumerate(plates):
                if plate["id"] in KEEP:
                    print(f"  skip keep {plate['id']}", flush=True)
                    continue
                if plate["id"] not in T2V_IDS:
                    raise SystemExit(
                        f"STOP: refusing {plate['id']} — only {T2V_IDS} T2V this run"
                    )
                dest = T2V_DEST[plate["id"]]
                if veo.already_done(dest, min_bytes=400_000):
                    print(f"  skip {dest.name}", flush=True)
                    continue
                print(
                    f"\n=== Fast T2V {plate['id']} ({i+1}/{len(plates)}) ===",
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
    print("OK T2V mint finished", flush=True)


if __name__ == "__main__":
    main()
