#!/usr/bin/env python3
"""HOS 002 back-catalogue Short (Tue 3 Nov): the one Lavoisier plate on Vertex AI Veo 3.1 Quality.

Claude's approval, desk PR #180 comment 5950150517: one Vertex Quality mint of an 8 s plate, at most
2 takes, inside the £0-floor rule, logged. Same Vertex pattern as 005 (`_mint_vertex_v02.py`):
project gen-lang-client-0538779324 ("History of Science"), us-central1, ADC as benoats@googlemail.com.
Never an Orbit project. Tokens are never printed. Media stays out of git (written to the main checkout).

  still                  start frame (Vertex gemini-2.5-flash-image, 002 Part 01 look refs)
  mint [--still <jpg>]   one Quality take (refused after 2)
  verdict <take> KEEP|FAIL "why"
  total

Python: ~/.venvs/hos-vertex/bin/python
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
MEDIA = Path("/Users/benjaminoats/YouTube/History Of Science")
FILM = MEDIA / "02_Video-Projects/002_How-Did-We-Discover-The-Periodic-Table"
CLIPS = FILM / "04_Generated-Clips/shorts_backcat"
REFS = CLIPS / "refs"
STILLS = CLIPS / "stills"
RAW = CLIPS / "raw"
UAT = CLIPS / "uat"
LOG = HERE / "BACKCAT_LAVOISIER_MINT_LOG_v01.json"
PLATE = "lavoisier_list"

PROJECT = "gen-lang-client-0538779324"
LOCATION = "us-central1"
ACCOUNT = "benoats@googlemail.com"
MODEL = "veo-3.1-generate-001"
IMAGE_MODEL = "gemini-2.5-flash-image"
CLIP_S, RESOLUTION, MAX_TAKES = 8, "1080p", 2
USD_PER_S, USD_PER_STILL, GBP_PER_USD = 0.20, 0.039, 0.80
# Free Trial projection after 005 (`_mint_vertex_v02.py --part 5 total`, 2 Oct 2026 11:40 UK).
CREDIT_BEFORE_GBP, FLOOR_GBP = 57.03, 0.0
STYLE_REFS = (REFS / "style_02_workshop_jars_4s.jpg", REFS / "style_10_rock_not_fire_3s.jpg")

STYLE = ("History of Science locked look: premium Animistry-class 3D cartoon, finished materials, "
         "soft cinematic daylight, 18th-century Paris laboratory. Not photoreal, not flat 2D. "
         "No logos, no captions, no signs, no UI, no readable text or letters anywhere. "
         "No Orbit orange robot. No DNA helix. No boy explorer character.")
SUBJECT = ("Antoine Lavoisier in 1780s Paris: a slim man in his forties with a kind, focused, readable "
           "face, a powdered grey wig with side curls tied back, a dark blue-black coat and a white "
           "cravat. He stands at a long wooden laboratory bench with glass retorts, flasks and a large "
           "polished brass balance with two pans. He writes a list with a quill on a sheet of paper; "
           "the page is soft, angled away from the camera, so no writing can be read. Calm daylight "
           "from a tall window on the left; NO flame, no candles, no lamps, no fire, no glow.")
ACTION = ("He writes steadily down the page with the quill, pauses, looks up at the brass balance as its "
          "pans settle level, gives a small satisfied nod, then dips the quill and writes the next line. "
          "Slow continuous camera dolly from the side towards him.")
VEO_TAIL = ("Silent picture only. Continuous real camera and subject motion through the final frame. "
            "HARD REJECT: photoreal, Ken Burns or still push, freeze frame, slow motion, readable or "
            "garbled text, extra people, flame, Orbit orange robot, DNA helix.")


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def rel(p: Path) -> str:
    return str(p.relative_to(MEDIA)) if p.is_relative_to(MEDIA) else str(p)


def load() -> dict:
    if LOG.exists():
        return json.loads(LOG.read_text())
    return {"film": FILM.name, "plate": PLATE, "use": "Short Tue 3 Nov 2026 (four elements), Lavoisier beat",
            "authority": "Claude, desk PR #180 comment 5950150517 (one Vertex Quality mint, at most 2 takes)",
            "path": "vertex", "vertex_project": PROJECT, "vertex_location": LOCATION, "account": ACCOUNT,
            "model": MODEL, "image_model": IMAGE_MODEL,
            "pricing_usd": {"veo_quality_per_s_video_only_1080p": USD_PER_S, "still": USD_PER_STILL},
            "credit_before_gbp": CREDIT_BEFORE_GBP, "floor_gbp": FLOOR_GBP,
            "stills": [], "takes": [], "keep": None, "cost_usd_total": 0.0}


def save(log: dict) -> None:
    log["cost_usd_total"] = round(sum(t.get("cost_usd", 0) for t in log["takes"])
                                  + sum(s.get("cost_usd", 0) for s in log["stills"]), 3)
    log["projected_credit_after_gbp"] = round(CREDIT_BEFORE_GBP - log["cost_usd_total"] * GBP_PER_USD, 2)
    log["updated"] = now()
    LOG.write_text(json.dumps(log, indent=2, ensure_ascii=False) + "\n")


def guard(log: dict, usd: float) -> None:
    left = CREDIT_BEFORE_GBP - (log["cost_usd_total"] + usd) * GBP_PER_USD
    if left < FLOOR_GBP:
        raise SystemExit(f"STOP: projected credit £{left:.2f} would fall below £{FLOOR_GBP:.0f}")


def client():
    import google.auth
    from google import genai
    creds, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
    if not creds:
        raise SystemExit("STOP: no ADC")
    return genai.Client(vertexai=True, project=PROJECT, location=LOCATION)


def img_part(p: Path):
    from google.genai import types
    return types.Part.from_bytes(data=p.read_bytes(), mime_type="image/jpeg")


def cmd_still(a) -> None:
    from google.genai import types
    log = load()
    guard(log, USD_PER_STILL)
    STILLS.mkdir(parents=True, exist_ok=True)
    n = len(log["stills"]) + 1
    dest = STILLS / f"{PLATE}_v{n:02d}.jpg"
    parts, lead = [], ""
    for k, ref in enumerate(STYLE_REFS, 1):
        parts.append(img_part(ref))
        lead += (f"Image {k} is this film's locked look (passed by Ben): match its 3D cartoon material, "
                 "finish and soft daylight. Do NOT copy its objects or any text. ")
    prompt = (f"{lead}Finished 3D cartoon still, the FIRST frame of a moving shot, subject mid-action and "
              f"readable, no motion blur. {SUBJECT} {a.extra or ''} {STYLE}")
    parts.append(prompt)
    print(f"STILL {PLATE} v{n:02d} model={IMAGE_MODEL} path=vertex project={PROJECT}", flush=True)
    c = client()
    r = c.models.generate_content(
        model=IMAGE_MODEL, contents=parts,
        config=types.GenerateContentConfig(response_modalities=["IMAGE"],
                                           image_config=types.ImageConfig(aspect_ratio="16:9")))
    data = next((p.inline_data.data for c in r.candidates or [] for p in (c.content.parts if c.content else [])
                 if p.inline_data and p.inline_data.data), None)
    if not data:
        raise SystemExit("STOP: no image")
    tmp = dest.with_suffix(".bin")
    tmp.write_bytes(data)
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(tmp), "-vf",
                    "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080", "-frames:v", "1",
                    "-q:v", "2", str(dest)], check=True)
    tmp.unlink()
    log["stills"].append({"v": n, "file": rel(dest), "sha256": sha256(dest), "model": IMAGE_MODEL,
                          "style_refs": [rel(r) for r in STYLE_REFS], "prompt": prompt,
                          "cost_usd": USD_PER_STILL, "at": now()})
    save(log)
    print(f"SAVED {dest}")


def cmd_mint(a) -> None:
    from google.genai import types
    log = load()
    if len(log["takes"]) >= MAX_TAKES:
        raise SystemExit(f"STOP: {MAX_TAKES} takes already (Claude's cap)")
    guard(log, CLIP_S * USD_PER_S)
    still = Path(a.still) if a.still else MEDIA / log["stills"][-1]["file"]
    take = len(log["takes"]) + 1
    RAW.mkdir(parents=True, exist_ok=True)
    dest = RAW / f"{PLATE}_t{take}.mp4"
    prompt = f"{STYLE} {SUBJECT} {ACTION} {a.extra or ''} No Explorer. {VEO_TAIL}"
    print(f"=== MINT {PLATE} take={take} Quality model={MODEL} path=vertex project={PROJECT} res={RESOLUTION} ===",
          flush=True)
    c = client()
    t0 = time.time()
    op = c.models.generate_videos(
        model=MODEL,
        source=types.GenerateVideosSource(prompt=prompt, image=types.Image.from_file(location=str(still))),
        config=types.GenerateVideosConfig(number_of_videos=1, duration_seconds=CLIP_S, aspect_ratio="16:9",
                                          resolution=RESOLUTION, generate_audio=False))
    entry = {"take": take, "model": MODEL, "quality": "Quality", "seconds": CLIP_S, "resolution": RESOLUTION,
             "generate_audio": False, "prompt": prompt, "start_frame": rel(still),
             "start_frame_sha256": sha256(still), "op_name": op.name, "submitted_at": now(),
             "cost_usd": round(CLIP_S * USD_PER_S, 3), "status": "SUBMITTED"}
    log["takes"].append(entry)
    save(log)
    while not op.done:
        time.sleep(12)
        op = c.operations.get(op)
        print(f"  poll … {int(time.time() - t0)}s", flush=True)
    if getattr(op, "error", None):
        entry.update(status="ERROR", why=str(op.error)[:500], cost_usd=0.0)
        save(log)
        raise SystemExit(f"STOP: Vertex error {str(op.error)[:400]}")
    vids = op.response.generated_videos if op.response else None
    if not vids:
        entry.update(status="FILTERED", why=str(getattr(op.response, "rai_media_filtered_reasons", None))[:500],
                     cost_usd=0.0)
        save(log)
        raise SystemExit("STOP: no video (filtered)")
    src = dest.with_suffix(".src.mp4")
    v = vids[0].video
    if getattr(v, "video_bytes", None):
        src.write_bytes(v.video_bytes)
    else:
        v.save(str(src))
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(src), "-map", "0:v:0",
                    "-c", "copy", "-an", str(dest)], check=True)
    src.unlink()
    UAT.mkdir(parents=True, exist_ok=True)
    sheet = UAT / f"{PLATE}_t{take}_sheet.jpg"
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(dest), "-vf",
                    "fps=9/8,scale=640:-2,tile=3x3:padding=6:color=black", "-frames:v", "1", "-q:v", "3",
                    str(sheet)], check=True)
    err = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(dest), "-vf", "freezedetect=n=0.003:d=0.8",
                          "-f", "null", "-"], capture_output=True, text=True).stderr
    entry.update(status="PENDING_UAT", file=rel(dest), sha256=sha256(dest), uat_sheet=rel(sheet),
                 freeze_events_0p8s=err.count("freeze_start"), api_s=round(time.time() - t0, 1), at=now())
    save(log)
    print(json.dumps({"file": rel(dest), "sheet": rel(sheet), "freeze": entry["freeze_events_0p8s"]}))
    print(f"running total ${log['cost_usd_total']:.2f} · projected credit £{log['projected_credit_after_gbp']:.2f}")


def cmd_verdict(a) -> None:
    log = load()
    t = next(t for t in log["takes"] if t["take"] == a.take)
    t.update(status=a.status, why=a.why, uat_at=now())
    if a.status == "KEEP":
        log["keep"] = {"take": a.take, "file": t["file"], "sha256": t["sha256"], "model": MODEL, "path": "vertex"}
    save(log)
    print(f"{a.status} {PLATE} t{a.take}: {a.why}")


def cmd_total(_a) -> None:
    log = load()
    print(f"{PLATE}: stills={len(log['stills'])} takes={len(log['takes'])} keep={bool(log['keep'])} "
          f"cost ${log['cost_usd_total']:.2f} · projected credit £{log.get('projected_credit_after_gbp', CREDIT_BEFORE_GBP)}")


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("still"); s.add_argument("--extra")
    m = sub.add_parser("mint"); m.add_argument("--still"); m.add_argument("--extra")
    v = sub.add_parser("verdict"); v.add_argument("take", type=int)
    v.add_argument("status", choices=["KEEP", "FAIL"]); v.add_argument("why")
    sub.add_parser("total")
    a = ap.parse_args()
    {"still": cmd_still, "mint": cmd_mint, "verdict": cmd_verdict, "total": cmd_total}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
