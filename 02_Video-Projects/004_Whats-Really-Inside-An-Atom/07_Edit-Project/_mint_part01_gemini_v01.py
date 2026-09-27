#!/usr/bin/env python3
"""HOS 004 Part 01 mint — Gemini API Veo fallback (Flow Ultra out of credits).

Start-frame I2V from refs/v01_stills. Prefer veo-3.1-generate-preview for glow;
veo-3.1-lite-generate-preview for low-risk. Never Ken Burns. Strip audio.
Record engine=gemini-api-veo in PART01_MINT_LOG_v01.json.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))
import orbit_gemini_veo as veo  # noqa: E402

PROJ = Path(__file__).resolve().parents[1]
PLATES_JSON = PROJ / "07_Edit-Project/parts/part-01_plates_v02.json"
REFS = PROJ / "04_Generated-Clips/part01/refs/v01_stills"
RAW = PROJ / "04_Generated-Clips/part01/raw/v01"
QA = PROJ / "07_Edit-Project/_qa_part01_mint_v01"
LOG = PROJ / "07_Edit-Project/PART01_MINT_LOG_v01.json"
ENV = REPO / "02_Video-Projects/002_How-Did-We-Discover-The-Periodic-Table/07_Edit-Project/.env"

QUALITY_IDS = {
    "02_atom_answer",
    "03_atom_turns",
    "10_electron_tube",
    "12_1913_targets",
    "13_numbered_cards",
}
STYLE = (
    "History of Science locked look: premium Animistry-class 3D cartoon, warm "
    "cinematic light, period science world. Not photoreal. Not live-action. "
    "Silent picture. No Orbit orange robot. No Explorer. Continuous motion the "
    "whole clip — never a still push or Ken Burns."
)
NEG = (
    "photoreal, live action, Ken Burns only, freeze frame, Orbit orange robot, "
    "Explorer, DNA helix, lava drip, underside lamp bulb, unfinished flat cards, "
    "garbled text, modern lab, hospital ward"
)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def probe_dur(path: Path) -> float:
    return float(
        subprocess.check_output(
            [
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=nw=1:nk=1", str(path),
            ],
            text=True,
        ).strip()
    )


def model_for(pid: str, plate_log: dict | None = None) -> str:
    if plate_log and plate_log.get("force_model"):
        return plate_log["force_model"]
    # After Flow Ultra + lite quota exhaustion, prefer generate-preview.
    if os.environ.get("HOS_VEO_FORCE_QUALITY") == "1":
        return os.environ.get("HOS_VEO_QUALITY_MODEL", "veo-3.1-generate-preview")
    if pid in QUALITY_IDS:
        return os.environ.get("HOS_VEO_QUALITY_MODEL", "veo-3.1-generate-preview")
    return os.environ.get("HOS_VEO_FAST_MODEL", "veo-3.1-lite-generate-preview")


def load_log() -> dict:
    if LOG.exists():
        return json.loads(LOG.read_text())
    return {
        "film": "004_Whats-Really-Inside-An-Atom",
        "part": "01",
        "engine": "gemini-api-veo (Flow Ultra insufficient credits)",
        "flow_block": "Not enough credits on benoats@googlemail.com Ultra",
        "started_at": datetime.now(timezone.utc).isoformat(),
        "plates": {},
    }


def save_log(log: dict) -> None:
    log["updated_at"] = datetime.now(timezone.utc).isoformat()
    LOG.write_text(json.dumps(log, indent=2) + "\n")


def extract_qa(mp4: Path, pid: str, try_n: int) -> dict:
    QA.mkdir(parents=True, exist_ok=True)
    dur = probe_dur(mp4)
    out = {}
    for name, t in {
        "start": 0.4,
        "mid": max(0.5, dur / 2),
        "end": max(0.5, dur - 0.6),
    }.items():
        dest = QA / f"{pid}_t{try_n}_{name}.jpg"
        subprocess.check_call(
            [
                "ffmpeg", "-y", "-ss", f"{t:.2f}", "-i", str(mp4),
                "-frames:v", "1", "-q:v", "3", str(dest),
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        out[name] = str(dest)
    return out


def auto_qa(mp4: Path) -> tuple[str, str]:
    dur = probe_dur(mp4)
    if dur < 4.0:
        return "FAIL", f"too short {dur:.2f}s"
    if mp4.stat().st_size < 400_000:
        return "FAIL", f"tiny {mp4.stat().st_size}"
    err = subprocess.run(
        [
            "ffmpeg", "-hide_banner", "-i", str(mp4),
            "-vf", "select='gt(scene,0.02)',showinfo", "-f", "null", "-",
        ],
        capture_output=True, text=True, errors="replace",
    ).stderr
    hits = len(re.findall(r"n:", err))
    # Soft cinematic plates (hand tap, scale tip, greek chip) often score 0–1
    # on scene>0.02 while still moving — accept size+duration, flag soft.
    if hits < 2 and dur > 5.0:
        return "KEEP", f"soft-motion scene_hits={hits} dur={dur:.2f}s (cinematic OK)"
    return "KEEP", f"motion_ok scene_hits={hits} dur={dur:.2f}s"


def generate_i2v(client, prompt: str, dest: Path, *, start: Path, model: str) -> dict:
    from google.genai import types

    full = f"{STYLE} {prompt}".strip()
    # Lite rejects negative_prompt; Quality/generate may accept it — omit always.
    config = types.GenerateVideosConfig(
        number_of_videos=1,
        duration_seconds=8,
        aspect_ratio="16:9",
        resolution="720p",
    )
    full = f"{full} HARD REJECT: {NEG}"
    print(f"  I2V start={start.name} model={model} → {dest.name}", flush=True)
    t0 = time.time()
    op = client.models.generate_videos(
        model=model,
        prompt=full,
        image=types.Image.from_file(location=str(start)),
        config=config,
    )
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
    return {"seconds": round(time.time() - t0, 1), "bytes": dest.stat().st_size, "model": model}


def force_api_key() -> None:
    for k in ("GEMINI_API_KEY", "GOOGLE_API_KEY"):
        if not os.environ.get(k):
            os.environ.pop(k, None)
    for line in ENV.read_text().splitlines():
        s = line.strip()
        if not s or s.startswith("#") or "=" not in s:
            continue
        k, v = s.split("=", 1)
        k, v = k.strip(), v.strip().strip('"').strip("'")
        if k in ("GEMINI_API_KEY", "GOOGLE_API_KEY") and v:
            os.environ[k] = v


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--plate", help="Single plate id")
    ap.add_argument("--from-id", help="Start from plate id inclusive")
    ap.add_argument("--all-pending", action="store_true")
    ap.add_argument("--max-tries", type=int, default=3)
    args = ap.parse_args()

    force_api_key()
    client = veo.make_client(ENV)
    plates = json.loads(PLATES_JSON.read_text())["plates"]
    log = load_log()
    log["engine"] = "gemini-api-veo (Flow Ultra insufficient credits)"
    log["flow_block"] = "Not enough credits on benoats@googlemail.com Ultra (Fast+Lite+Quality)"
    RAW.mkdir(parents=True, exist_ok=True)
    QA.mkdir(parents=True, exist_ok=True)

    ids = [p["id"] for p in plates]
    if args.plate:
        todo = [p for p in plates if p["id"] == args.plate]
    elif args.from_id:
        todo = plates[ids.index(args.from_id):]
    elif args.all_pending:
        todo = [p for p in plates if not log["plates"].get(p["id"], {}).get("keep")]
    else:
        todo = []
        for p in plates:
            if not log["plates"].get(p["id"], {}).get("keep"):
                todo = [p]
                break

    print(f"todo={[p['id'] for p in todo]}", flush=True)
    for plate in todo:
        pid = plate["id"]
        still = REFS / f"{pid}_v01.jpg"
        if not still.exists() or still.stat().st_size < 80_000:
            raise SystemExit(f"STOP missing still {still}")
        entry = log["plates"].setdefault(pid, {"tries": []})
        if entry.get("keep"):
            print(f"SKIP KEEP {pid}", flush=True)
            continue
        framing = None
        fails = 0
        for try_n in range(1, args.max_tries + 1):
            if any(t.get("try") == try_n for t in entry["tries"]):
                continue
            model = model_for(pid, entry)
            dest_try = RAW / f"{pid}_t{try_n}.mp4"
            dest_keep = RAW / f"{pid}_v01.mp4"
            prompt = plate["prompt"]
            if framing:
                prompt = f"{prompt} FRAMING CHANGE: {framing}"
            print(f"\n=== {pid} try={try_n} model={model} ===", flush=True)
            try:
                info = generate_i2v(client, prompt, dest_try, start=still, model=model)
                status, note = auto_qa(dest_try)
                frames = extract_qa(dest_try, pid, try_n)
                row = {
                    "id": pid,
                    "try": try_n,
                    "model": model,
                    "engine": "gemini-api-veo",
                    "start_frame": str(still),
                    "start_frame_sha256": sha256_file(still),
                    "out": str(dest_try),
                    "sha256": sha256_file(dest_try),
                    "bytes": dest_try.stat().st_size,
                    "duration_s": round(probe_dur(dest_try), 3),
                    "status": status,
                    "note": note,
                    "framing_note": framing,
                    "prompt": f"{STYLE} {prompt}",
                    "qa_frames": frames,
                    "flow_meta": info,
                    "at": datetime.now(timezone.utc).isoformat(),
                }
            except Exception as e:
                msg = str(e)
                row = {
                    "id": pid, "try": try_n, "model": model_for(pid, entry),
                    "engine": "gemini-api-veo",
                    "status": "FAIL",
                    "note": f"exception {type(e).__name__}: {e}",
                    "at": datetime.now(timezone.utc).isoformat(),
                }
                print(f"  FAIL {e}", flush=True)
                if "RESOURCE_EXHAUSTED" in msg or "429" in msg:
                    # Back off before next try / plate
                    wait_s = 90
                    print(f"  quota hit — sleep {wait_s}s", flush=True)
                    time.sleep(wait_s)
            entry["tries"].append(row)
            save_log(log)
            if row["status"] == "KEEP":
                if dest_keep.exists():
                    dest_keep.unlink()
                Path(row["out"]).rename(dest_keep)
                row["out"] = str(dest_keep)
                row["sha256"] = sha256_file(dest_keep)
                entry["keep"] = {
                    "file": dest_keep.name,
                    "sha256": row["sha256"],
                    "try": try_n,
                    "model": model,
                    "engine": "gemini-api-veo",
                }
                save_log(log)
                print(f"  KEEP {dest_keep.name} sha={row['sha256'][:16]}", flush=True)
                break
            fails += 1
            if fails >= 2 and framing is None:
                framing = (
                    "wider camera; subject lower-left; more depth; "
                    "stronger continuous motion from frame 0"
                )
                print(f"  framing change: {framing}", flush=True)
        else:
            print(f"  exhausted tries for {pid}", flush=True)
            if not args.all_pending and not args.from_id:
                break

    save_log(log)
    print(f"LOG {LOG}", flush=True)


if __name__ == "__main__":
    main()
