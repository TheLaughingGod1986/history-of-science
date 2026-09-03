#!/usr/bin/env python3
"""Part 04 v19 — 04_still_clear Fast T2V only.

Edit-first found no living take with colorless water-clear broth.
KEEP 01–03, 05–12 from v18 (07 v13, 09 v17, 08 v18, 05 v17).
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
RAW = PROJ / "04_Generated-Clips/part04/raw/v01_fast_probe"
META = PROJ / "07_Edit-Project/part04_gen_meta_v01.json"
T2V_ID = "04_still_clear"
T2V_DEST = RAW / "04_still_clear_v19.mp4"
KEEP = {
    "01_question_mark_flask",
    "02_boil_broth",
    "03_dust_in_the_curve",
    "05_tip_the_trap",
    "06_explorer_watches",
    "07_bloom_cloud",
    "08_passengers",
    "09_sceptics_watch",
    "10_an_address",
    "11_result_returns",
    "12_block_the_road",
}
KEEP_SHA = {
    "07_bloom_cloud": (
        RAW / "07_bloom_cloud_v13.mp4",
        "fd5d4f7470386ae1bf2eba745cd2d695c402c549cd6fc061edd885fdb34d3604",
    ),
    "09_sceptics_watch": (
        RAW / "09_sceptics_watch_v17.mp4",
        "3c221c0a17da8e3c57098ab2c9910df9eb41bd783d9f631bb7b210c5825a6a3a",
    ),
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


def dest_for(plate_id: str) -> Path:
    if plate_id == T2V_ID:
        return T2V_DEST
    for ver in ("v18", "v17", "v16", "v15", "v14", "v13", "v12", "v11", "v10", "v09", "v08", "v07", "v06", "v05", "v04", "v03", "v02", "v01"):
        cand = RAW / f"{plate_id}_{ver}.mp4"
        if veo.already_done(cand, min_bytes=400_000):
            return cand
    return RAW / f"{plate_id}_v01.mp4"


def mint_t2v(page, plate: dict, dest: Path) -> dict:
    if plate["id"] != T2V_ID:
        raise SystemExit(f"STOP: refusing to mint {plate['id']} (only {T2V_ID} T2V)")
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
    plates = json.loads(PLATES_JSON.read_text())["plates"]
    RAW.mkdir(parents=True, exist_ok=True)
    for slug in sorted(KEEP):
        p = dest_for(slug)
        if not veo.already_done(p, min_bytes=400_000):
            raise SystemExit(f"STOP: keep-plate missing {slug}")
        print(f"KEEP {slug} {p.name} sha256={sha256(p)} — will not remint", flush=True)
    for slug, (path, want) in KEEP_SHA.items():
        got = sha256(path)
        if got != want:
            raise SystemExit(f"STOP: KEEP hash mismatch {slug} got={got} want={want}")
        print(f"KEEP HASH {slug} {path.name}", flush=True)
    if veo.already_done(T2V_DEST, min_bytes=400_000):
        print(f"already have {T2V_DEST.name} — no Flow", flush=True)
        return

    profile = flow.profile_path(PROFILE)
    print(f"Flow profile={profile} model={MODEL} raw={RAW}", flush=True)
    meta: dict = {"engine": "flow-ui", "model": MODEL, "plates": []}
    if META.exists():
        try:
            meta = json.loads(META.read_text())
        except Exception:
            pass
    meta["model"] = MODEL
    meta["raw"] = str(RAW)

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        ctx, page = flow.launch_context(p, headed=True, profile=profile)
        try:
            page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
            page.wait_for_timeout(2000)
            flow.dismiss_banners(page)
            if not flow.looks_logged_in(page):
                raise SystemExit("STOP: Flow not logged in. Do not loop.")
            plate = next(x for x in plates if x["id"] == T2V_ID)
            dest = T2V_DEST
            print(f"\n=== Fast T2V {T2V_ID} ===", flush=True)
            remint_used = False
            while True:
                try:
                    info = mint_t2v(page, plate, dest)
                except Exception as e:
                    print(f"STOP: Flow failed on {T2V_ID}: {e}", flush=True)
                    META.write_text(json.dumps(meta, indent=2))
                    raise SystemExit(
                        "STOP: Create/arrow_forward died. Do not loop. "
                        f"Last plate={T2V_ID}"
                    ) from e
                if still_fail(info):
                    archive_reject(dest, "still")
                    if remint_used:
                        META.write_text(json.dumps(meta, indent=2))
                        raise SystemExit(
                            f"STOP: still-push on {T2V_ID} after one remint. "
                            "Do not loop. QA frames extracted."
                        )
                    remint_used = True
                    print(
                        "  QA motion reject — one remint only (Create still alive)",
                        flush=True,
                    )
                    continue
                break
            meta.setdefault("plates", []).append({"id": T2V_ID, **info})
            META.write_text(json.dumps(meta, indent=2))
        finally:
            ctx.close()
    print("OK part 04 v19 T2V mint finished", flush=True)


if __name__ == "__main__":
    main()
