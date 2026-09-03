#!/usr/bin/env python3
"""Part 05 — remint 05 and 08 only. Do not touch 03. Do not remint 01–04 of the film.

08 I2V from t72 crop (right flask cut). Add to Prompt fallback = Fast T2V.
If Create dies on 05 or 08: STOP. Do not assemble without 03.
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
REFS = PROJ / "04_Generated-Clips/part05/refs"
T72 = REFS / "t72_pasteur_lock.jpg"
T72_ONE = REFS / "t72_pasteur_lock_one_flask.jpg"
META = PROJ / "07_Edit-Project/part05_gen_meta_v01e.json"
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
    "ZERO purple or pink blob creatures. ZERO floating orbs. ZERO germ-macro. "
    "ZERO matching-coat twins. ZERO top hats. ZERO metal trays. "
    "ZERO modern hospital. ZERO Orbit robot. ZERO Explorer. "
    "ZERO readable text. NOT photoreal."
)

PLATES = [
    {
        "id": "05_theatre_wins",
        "out": "05_theatre_wins_v01c.mp4",
        "i2v": False,
        "prompt": (
            LOCK
            + " Wide living 1860s wooden hospital ward. The ROOM is the picture. "
            "Patients rest in wooden beds, fever receding. Nurses in blue dresses "
            "and white aprons walk the aisle. Warm oil lamps and brass globes only. "
            "Empty air — no microbes, no purple shapes, no floating blobs, "
            "no educational germ overlay of any kind. Camera slowly trucks down "
            "the aisle. No hats."
        ),
    },
    {
        "id": "08_last_light",
        "out": "08_last_light_v01d.mp4",
        "i2v": True,
        "start": T72_ONE,
        "prompt": (
            LOCK
            + " IMAGE-TO-VIDEO from the locked classic Pasteur still (t72 crop: "
            "one flask only). Keep THAT exact S-curve swan-neck, round-bottom on "
            "wood, clear broth with NOTHING floating in it. Camera slowly pulls "
            "BACK so the flask becomes SMALL garnish in a clean 1860s theatre — "
            "not hero-scale. Empty wood on the right. ZERO second flask. "
            "ZERO straight-neck bottle. ZERO other glass on the table. "
            "ZERO people. Lamp flicker only. Continuous motion."
        ),
        "t2v_fallback": (
            LOCK
            + " Clean 1860s theatre. Empty wooden table. ONE tiny classic Pasteur "
            "flask SMALL in the far corner as garnish: S-curve swan-neck only, "
            "round-bottom on wood, clear broth. ZERO second flask. ZERO other "
            "glass. ZERO sprites. ZERO people. Camera slowly pushes into lamp glow."
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
    tmp = Path(tempfile.mkdtemp(prefix="hos_p05e_m_"))
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


def still_fail(info: dict) -> bool:
    return info["motion_mean"] < STILL_MEAN or info["first_second_motion"] < STILL_FIRST


def mint_one(page, plate: dict, dest: Path, *, i2v: bool) -> dict:
    start = plate.get("start") if i2v else None
    if start and not Path(start).exists():
        start = T72 if T72.exists() and i2v else None
    prompt = plate["prompt"] if start else plate.get("t2v_fallback", plate["prompt"])
    print(f"  {'I2V' if start else 'T2V'} {plate['id']} start={start}", flush=True)
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
    RAW.mkdir(parents=True, exist_ok=True)
    if not T72_ONE.exists():
        raise SystemExit(f"STOP: missing cropped Pasteur lock {T72_ONE}")
    meta: dict = {"engine": "flow-ui", "model": MODEL, "plates": []}
    if META.exists():
        try:
            meta = json.loads(META.read_text())
        except Exception:
            pass
    meta["model"] = MODEL
    meta["raw"] = str(RAW)
    meta["t72_start"] = str(T72_ONE)

    profile = flow.profile_path(PROFILE)
    print(f"Flow profile={profile} model={MODEL} order=05 then 08. No 03.", flush=True)
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        ctx, page = flow.launch_context(p, headed=True, profile=profile)
        try:
            page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
            page.wait_for_timeout(2000)
            flow.dismiss_banners(page)
            if not flow.looks_logged_in(page):
                raise SystemExit("STOP: Flow not logged in. Do not loop.")
            for plate in PLATES:
                dest = RAW / plate["out"]
                if veo.already_done(dest, min_bytes=400_000):
                    print(f"  skip {dest.name}", flush=True)
                    continue
                print(f"\n=== Fast {plate['id']} → {plate['out']} ===", flush=True)
                remint_used = False
                used_i2v = bool(plate.get("i2v"))
                while True:
                    try:
                        info = mint_one(page, plate, dest, i2v=used_i2v)
                    except Exception as e:
                        err = str(e)
                        if used_i2v and (
                            "Add to Prompt" in err
                            or "start-frame" in err.lower()
                            or "Start-frame" in err
                            or "chip missing" in err
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
                            f"STOP: Create died. Do not loop. Last plate={plate['id']}"
                        ) from e
                    if still_fail(info):
                        reject = dest.with_name(f"_rejected_still_{dest.name}")
                        dest.rename(reject)
                        print(f"  archived {reject.name}", flush=True)
                        if remint_used:
                            META.write_text(json.dumps(meta, indent=2))
                            raise SystemExit(
                                f"STOP: still-push on {plate['id']} after one remint."
                            )
                        remint_used = True
                        print("  QA motion reject — one remint only", flush=True)
                        continue
                    break
                meta.setdefault("plates", []).append({"id": plate["id"], **info})
                META.write_text(json.dumps(meta, indent=2))
        finally:
            ctx.close()
    print("OK part 05 v01e 05+08 mint finished", flush=True)


if __name__ == "__main__":
    main()
