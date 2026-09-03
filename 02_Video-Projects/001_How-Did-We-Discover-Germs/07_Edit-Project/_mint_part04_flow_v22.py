#!/usr/bin/env python3
"""Part 04 v22 — 08_passengers Fast T2V only.

Official FAIL: 08_passengers_v21 is not the locked Pasteur world
(other flask shapes + cartoon germ sprites). Hero bottle was correct.
Edit-first: no unused living is ONE Pasteur + motes, no second bottle.
KEEP 01–07, 09–12. Do not overwrite v21 dests.
If Create dies: STOP. One remint only if still-push.
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
RAW = PROJ / "04_Generated-Clips/part04/raw/v01_fast_probe"
META = PROJ / "07_Edit-Project/part04_gen_meta_v22.json"
T2V_ID = "08_passengers"
T2V_DEST = RAW / "08_passengers_v22.mp4"
PROMPT = (
    "Premium Animistry 3D cartoon. Close on ONE Pasteur swan-neck flask on a bare wooden "
    "bench. The neck IS the S-curve question-mark — glass rises from the onion bulb and "
    "bends over like a swan. NOT a straight chimney. NOT a boiling flask. Round bulb "
    "FLAT on the wood, grey-clear water inside. Bare wood wall behind — NO shelves, "
    "NO other glass, NO bottles, NO conical flasks, NO stands, NO lamp chimney as a "
    "second flask. One sunbeam with only fine pollen dust, tiny soft specks. Air is "
    "otherwise empty. ZERO germs, ZERO sprites, ZERO spiked blobs, ZERO smoke loops, "
    "ZERO microbes. Camera already easing in the first second. Continuous 8s. "
    "NO Explorer. NO Orbit. Silent. No text. Do NOT freeze. Do NOT invent extra glass."
)
KEEP_SHA = {
    "07_bloom_cloud": (
        RAW / "07_bloom_cloud_v13.mp4",
        "fd5d4f7470386ae1bf2eba745cd2d695c402c549cd6fc061edd885fdb34d3604",
    ),
    "04_still_clear": (RAW / "04_still_clear_v21.mp4", None),
    "10_an_address": (RAW / "10_an_address_v21.mp4", None),
    "11_result_returns": (RAW / "11_result_returns_v03.mp4", None),
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


def mint_t2v(page, dest: Path) -> dict:
    print(
        f"  T2V exact prompt ({len(PROMPT)} chars) start_frame=None scenery_only=True",
        flush=True,
    )
    info = flow.generate_clip(
        page,
        PROMPT,
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
    RAW.mkdir(parents=True, exist_ok=True)
    for slug, (path, want) in KEEP_SHA.items():
        if not veo.already_done(path, min_bytes=400_000):
            raise SystemExit(f"STOP: keep-plate missing {slug} {path}")
        got = sha256(path)
        if want and got != want:
            raise SystemExit(f"STOP: KEEP hash mismatch {slug} got={got}")
        print(f"KEEP {slug} {path.name} sha256={got}", flush=True)
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
            dest = T2V_DEST
            print(f"\n=== Fast T2V {T2V_ID} ===", flush=True)
            remint_used = False
            while True:
                try:
                    info = mint_t2v(page, dest)
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
    print("OK part 04 v22 T2V mint finished", flush=True)


if __name__ == "__main__":
    main()
