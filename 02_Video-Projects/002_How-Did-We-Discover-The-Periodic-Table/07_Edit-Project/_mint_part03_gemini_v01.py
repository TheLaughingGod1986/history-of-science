#!/usr/bin/env python3
"""Mint Part 03 real Veo motion via Gemini API.

CoS gate (from locked Part 02 v06 watch): no slideshow stills, no center stamps,
Animistry cartoon (not photoreal), one persistent set, Explorer once.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))
import orbit_gemini_veo as veo  # noqa: E402

PROJ = Path(__file__).resolve().parents[1]
PLATES = PROJ / "07_Edit-Project/parts/part-03_plates_v01.json"
RAW = PROJ / "04_Generated-Clips/part03/raw/v01_fast"
META = PROJ / "07_Edit-Project/part03_mint_v01_meta.json"
EXPLORER_LOCK = PROJ / "04_Generated-Clips/part01/refs/explorer_germs_part01_lock.jpg"
EXPLORER_START = PROJ / "04_Generated-Clips/part03/refs/v01_stills/05_explorer_ruler_start.jpg"
# Prefer Fast for continuous motion; lite only if Fast is exhausted.
MODEL = os.environ.get("ORBIT_VEO_MODEL", "veo-3.1-fast-generate-preview")
SET = (
    "ONE persistent 1860 Karlsruhe congress-hall / study-hall: warm honey oak panels, "
    "tall arched windows, soft volumetric daylight, blank cream pamphlets, blank cream cards. "
)
STYLE = (
    "Finished Animistry-class stylised 3D cartoon like Germs Part 01 PASS. "
    "NOT photoreal. NOT live-action. NOT a photographic AI still. "
    "Continuous real camera and object motion the whole clip. Silent. "
    "No Orbit orange robot. No dead-center full-screen text stamps. "
)
PHYSICS = (
    "Opaque ceramic / sealed metal only if vessels appear. ZERO clear liquid glass. "
    "ZERO bubbles in air. ZERO vessel fire. Candle wick OK. "
)
NEG = (
    "photoreal, live action, photographic still, Ken Burns only, freeze frame, "
    "Orbit orange robot, dead-center title card, full-screen chapter stamp, "
    "readable formulas, clear glass liquid, bubbles in air, vessel fire, twins, "
    "adult explorer redesign, hospital ward, modern conference, laptops"
)


def probe(path: Path) -> float:
    return float(
        subprocess.check_output(
            [
                "ffprobe", "-v", "error", "-show_entries", "format=duration",
                "-of", "default=nw=1:nk=1", str(path),
            ],
            text=True,
        ).strip()
    )


def ensure_explorer_start() -> Path | None:
    if EXPLORER_START.exists() and EXPLORER_START.stat().st_size > 40_000:
        return EXPLORER_START
    if not EXPLORER_LOCK.exists():
        return None
    # Lightweight composition still via ffmpeg overlay on a hall-colored bed
    EXPLORER_START.parent.mkdir(parents=True, exist_ok=True)
    bed = EXPLORER_START.with_name("_hall_bed.png")
    subprocess.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-f", "lavfi", "-i", "color=c=0xC4A574:s=1920x1080:d=1",
            "-frames:v", "1", str(bed),
        ],
        check=True,
    )
    subprocess.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(bed), "-i", str(EXPLORER_LOCK),
            "-filter_complex",
            "[1:v]scale=720:-1[ch];[0:v][ch]overlay=(W-w)/2:(H-h)/2+80",
            "-frames:v", "1", str(EXPLORER_START),
        ],
        check=True,
    )
    bed.unlink(missing_ok=True)
    return EXPLORER_START if EXPLORER_START.exists() else EXPLORER_LOCK


def generate_scenery(client, prompt: str, dest: Path, *, start: Path | None = None) -> dict:
    from google.genai import types

    full = f"{STYLE} {SET} {PHYSICS} {prompt}".strip()
    config = types.GenerateVideosConfig(
        number_of_videos=1,
        duration_seconds=8,
        aspect_ratio="16:9",
        resolution="720p",
        negative_prompt=NEG,
    )
    kwargs: dict = {"model": MODEL, "prompt": full, "config": config}
    if start and start.exists():
        kwargs["image"] = types.Image.from_file(location=str(start))
        print(f"  I2V start={start.name}", flush=True)
    else:
        print("  T2V scenery (no Orbit identity)", flush=True)
    t0 = time.time()
    print(f"  submit model={MODEL} → {dest.name}", flush=True)
    op = client.models.generate_videos(**kwargs)
    while not op.done:
        time.sleep(12)
        op = client.operations.get(op)
        print(f"  poll {dest.stem} … {int(time.time() - t0)}s", flush=True)
    if getattr(op, "error", None):
        raise RuntimeError(op.error)
    resp = getattr(op, "response", None) or getattr(op, "result", None)
    videos = getattr(resp, "generated_videos", None) if resp else None
    if not videos:
        raise RuntimeError(f"no videos: {resp!r}")
    video = videos[0]
    dest.parent.mkdir(parents=True, exist_ok=True)
    client.files.download(file=video.video)
    video.video.save(str(dest))
    veo.strip_audio(dest)
    return {"seconds": round(time.time() - t0, 1), "bytes": dest.stat().st_size, "model": MODEL}


def main() -> None:
    only = set(sys.argv[1:]) if len(sys.argv) > 1 else None
    plates = json.loads(PLATES.read_text())["plates"]
    # Ensure empty shell env vars do not block .env load
    for k in ("GEMINI_API_KEY", "GOOGLE_API_KEY"):
        if not os.environ.get(k):
            os.environ.pop(k, None)
    client = veo.make_client(PROJ / "07_Edit-Project/.env")
    meta: dict = {"model": MODEL, "engine": "gemini-api-veo", "plates": []}
    if META.exists():
        try:
            meta = json.loads(META.read_text())
        except Exception:
            pass
    by_id = {p["id"]: p for p in meta.get("plates", []) if "id" in p}
    explorer_start = ensure_explorer_start()

    for plate in plates:
        pid = plate["id"]
        if only and pid not in only and not any(pid.startswith(x) for x in only):
            continue
        dest = RAW / f"{pid}_v01.mp4"
        if dest.exists() and dest.stat().st_size > 400_000:
            try:
                d = probe(dest)
                if 5.5 <= d <= 14:
                    print(f"SKIP {pid} ({d:.2f}s)", flush=True)
                    by_id[pid] = {"id": pid, "status": "exists", "out": str(dest), "duration": d}
                    continue
            except Exception:
                pass
        start = explorer_start if plate.get("explorer") else None
        print(f"\n=== {pid} ===", flush=True)
        try:
            info = generate_scenery(client, plate["prompt"], dest, start=start)
            d = probe(dest)
            if d < 5.5:
                raise RuntimeError(f"short clip {d:.2f}s")
            row = {"id": pid, "status": "ok", "out": str(dest), "duration": d, **info}
            print(f"OK {pid} {d:.2f}s {dest.stat().st_size}b", flush=True)
        except Exception as e:
            row = {"id": pid, "status": "fail", "error": str(e)[:500]}
            print(f"FAIL {pid}: {e}", flush=True)
        by_id[pid] = row
        meta["plates"] = list(by_id.values())
        meta["updated"] = time.strftime("%Y-%m-%dT%H:%M:%S")
        META.write_text(json.dumps(meta, indent=2))

    ok = sum(1 for p in by_id.values() if p.get("status") in {"ok", "exists"})
    want = len(only) if only else len(plates)
    print(f"\nDONE ok={ok} want={want} meta={META}", flush=True)
    if ok < want:
        sys.exit(2)


if __name__ == "__main__":
    main()
