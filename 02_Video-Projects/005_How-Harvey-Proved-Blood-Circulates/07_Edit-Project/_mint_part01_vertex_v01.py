#!/usr/bin/env python3
"""HOS 005 Part 01 on Vertex AI Veo 3.1 (Ben's OK for 005, 1 Oct 2026).

Project gen-lang-client-0538779324 ("History of Science"), us-central1, ADC as
benoats@googlemail.com. Never an Orbit project. Tokens are never printed.

  still   <plate> [--seed <jpg>] [--extra "…"]       start frame (Vertex gemini-2.5-flash-image)
  mint    <plate> [--still <jpg>] [--framing f] [--extra "…"]   one Veo take, audio stripped, UAT sheet
  resume  <plate> <take>                            finish a submitted take from its op_name
  verdict <plate> <take> KEEP|FAIL "why"            plate UAT result
  total                                              running cost

Quality plates → veo-3.1-generate-001, Fast → veo-3.1-fast-generate-001, 1080p,
8 s, generate_audio=False (video-only SKU), audio stream removed after download.
Python: ~/.venvs/hos-vertex/bin/python. Media stays out of git.
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

PROJ = Path(__file__).resolve().parents[1]
REPO = PROJ.parents[1]
EDIT = PROJ / "07_Edit-Project"
BOARD = EDIT / "parts/part-01_plates_v02.json"
LOG = EDIT / "PART01_MINT_LOG_v01.json"
STILLS = PROJ / "04_Generated-Clips/part01/refs/v02_vertex_stills"
RAW = PROJ / "04_Generated-Clips/part01/raw/v01"
UAT = PROJ / "04_Generated-Clips/part01/uat"

PROJECT = "gen-lang-client-0538779324"
LOCATION = "us-central1"
ACCOUNT = "benoats@googlemail.com"
MODELS = {"Quality": "veo-3.1-generate-001", "Fast": "veo-3.1-fast-generate-001"}
IMAGE_MODEL = "gemini-2.5-flash-image"
CLIP_S = 8
RESOLUTION = "1080p"
# Vertex list prices, video-only 1080p (Sept 2026 pricing page); image ≈ $0.039.
USD_PER_S = {"Quality": 0.20, "Fast": 0.10}
USD_PER_STILL = 0.039

STYLE_REF = REPO / "02_Video-Projects/001_How-Did-We-Discover-Germs/04_Generated-Clips/part01/refs/v08_stills/10_ward_clean.jpg"
LIVE_THUMB = REPO / "00_Brand/Channel-Setup/style/long/004_whats_really_inside_an_atom_A.jpg"
EXPLORER_REF = REPO / "01_Character/05_Generation-References/hos-explorer-reference-v01.jpg"
STYLE = (
    "History of Science locked look: premium Animistry-class 3D cartoon, finished "
    "materials, warm cinematic light, 17th-century world. Not photoreal, not flat 2D. "
    "No logos, no captions, no signs, no UI. No Orbit orange robot. No DNA helix. "
    "Wonder, not gore: no wounds, no blood on skin, no cut flesh, no animal organs."
)
CANDLE_LINE = "Warm candlelight falls from out of frame; no candle, flame, lantern or lamp in shot."
DAYLIGHT_LINE = ("Soft warm daylight from a window out of frame. There are no candles, candlesticks, "
                 "lamps or lanterns anywhere in the room.")
VEO_TAIL = (
    "Silent picture only. Continuous real camera and subject motion through the final frame. "
    "HARD REJECT: photoreal, Ken Burns or still push, freeze frame, slow motion, Orbit orange "
    "robot, DNA helix, lava drip, gore, garbled text."
)


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def rel(p: Path) -> str:
    return str(p.relative_to(REPO)) if p.is_relative_to(REPO) else str(p)


def probe_dur(p: Path) -> float:
    return float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(p)], text=True).strip())


def board() -> dict:
    return json.loads(BOARD.read_text())


def plate(pid: str) -> dict:
    for p in board()["plates"]:
        if p["id"] == pid:
            return p
    raise SystemExit(f"STOP: unknown plate {pid}")


def load_log() -> dict:
    if LOG.exists():
        return json.loads(LOG.read_text())
    return {
        "film": "005_How-Harvey-Proved-Blood-Circulates",
        "part": "01",
        "board": rel(BOARD),
        "path": "vertex",
        "vertex_project": PROJECT,
        "vertex_location": LOCATION,
        "account": ACCOUNT,
        "authority": "Ben, 1 Oct 2026 (chat with Claude): Vertex for 005; desk PR #180 comment 5942235177",
        "models": MODELS,
        "image_model": IMAGE_MODEL,
        "pricing_usd": {"veo_per_s_video_only_1080p": USD_PER_S, "still": USD_PER_STILL,
                        "source": "Vertex AI generative pricing page, video-only rows, Sept 2026"},
        "credit_check": None,
        "takes": [],
        "stills": [],
        "plates": {},
        "cost_usd_total": 0.0,
    }


def save_log(log: dict) -> None:
    log["cost_usd_total"] = round(
        sum(t.get("cost_usd", 0) for t in log["takes"]) + sum(s.get("cost_usd", 0) for s in log["stills"]), 3)
    log["updated"] = now()
    LOG.write_text(json.dumps(log, indent=2, ensure_ascii=False) + "\n")


def update_log(fn) -> dict:
    """Read-modify-write under a lock: parallel takes must not drop each other's entries."""
    import fcntl
    with (EDIT / ".part01_mint_log.lock").open("w") as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        log = load_log()
        fn(log)
        save_log(log)
        return log


def client():
    import google.auth
    from google import genai
    creds, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
    if not creds:
        raise SystemExit("STOP: no ADC (gcloud auth application-default login as benoats@googlemail.com)")
    return genai.Client(vertexai=True, project=PROJECT, location=LOCATION)


def img_part(p: Path):
    from google.genai import types
    mime = "image/png" if p.suffix.lower() == ".png" else "image/jpeg"
    return types.Part.from_bytes(data=p.read_bytes(), mime_type=mime)


def to_1080(src_bytes: bytes, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(".bin")
    tmp.write_bytes(src_bytes)
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(tmp),
                    "-vf", "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080",
                    "-frames:v", "1", "-q:v", "2", str(dest)], check=True)
    tmp.unlink(missing_ok=True)


def still_prompt(pl: dict, extra: str) -> str:
    p = pl.get("still_prompt") or pl["prompt"]
    for drop in ("Silent.", "Continuous motion through the final frame.", "Premium Animistry-class 3D cartoon."):
        p = p.replace(drop, "")
    tail = "" if pl.get("explorer") else " No boy explorer character in this image."
    return ("Finished 3D cartoon still: the FIRST frame of this moving shot, key subject "
            f"mid-action and readable, no motion blur. {p.strip()} {extra} {STYLE}{tail}").strip()


def cmd_still(a) -> None:
    from google.genai import types
    pl = plate(a.plate)
    STILLS.mkdir(parents=True, exist_ok=True)
    n = 1
    while (STILLS / f"{a.plate}_v{n:02d}.jpg").exists():
        n += 1
    dest = STILLS / f"{a.plate}_v{n:02d}.jpg"
    dest.touch()
    parts, lead, k = [], "", 0
    for ref, what in ((STYLE_REF, "the locked channel style"), (LIVE_THUMB, "the live channel look")):
        if ref.exists():
            parts.append(img_part(ref)); k += 1
            lead += (f"Image {k} shows {what} only: match its 3D cartoon material, finish and warm "
                     "light. Do NOT copy its room, people, objects or any text. ")
    if a.seed:
        seed = Path(a.seed)
        parts.append(img_part(seed)); k += 1
        lead += (f"Image {k} is the previous shot in the same set: keep its set, palette, props "
                 "and character design consistent. ")
    if pl.get("explorer") and EXPLORER_REF.exists():
        parts.append(img_part(EXPLORER_REF)); k += 1
        lead += f"Image {k} is the Explorer character sheet: match him exactly, exactly one Explorer. "
    parts.append(lead + still_prompt(pl, a.extra or ""))
    c = client()
    print(f"STILL {a.plate} v{n:02d} model={IMAGE_MODEL} path=vertex project={PROJECT}", flush=True)
    r = c.models.generate_content(
        model=IMAGE_MODEL, contents=parts,
        config=types.GenerateContentConfig(response_modalities=["IMAGE"],
                                           image_config=types.ImageConfig(aspect_ratio="16:9")))
    data = None
    for cand in r.candidates or []:
        for part in (cand.content.parts if cand.content else []) or []:
            if part.inline_data and part.inline_data.data:
                data = part.inline_data.data
    if not data:
        raise SystemExit(f"STOP: no image for {a.plate}")
    to_1080(data, dest)
    rec = {"plate": a.plate, "v": n, "file": rel(dest), "sha256": sha256(dest),
           "model": IMAGE_MODEL, "seed": a.seed and rel(Path(a.seed)),
           "extra": a.extra, "cost_usd": USD_PER_STILL, "at": now()}
    update_log(lambda log: log["stills"].append(rec))
    print(f"SAVED {dest}")


def uat_sheet(mp4: Path, out: Path) -> None:
    """Start/middle/end + 1 fps strip as one sheet (for the desk; UAT itself is on playback)."""
    out.parent.mkdir(parents=True, exist_ok=True)
    dur = probe_dur(mp4)
    fps = 9 / dur
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(mp4),
                    "-vf", f"fps={fps:.5f},scale=640:-2,tile=3x3:padding=6:color=black",
                    "-frames:v", "1", "-q:v", "3", str(out)], check=True)


def motion_stats(mp4: Path) -> dict:
    err = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(mp4), "-vf",
                          "freezedetect=n=0.003:d=0.8", "-f", "null", "-"],
                         capture_output=True, text=True, errors="replace").stderr
    freezes = err.count("freeze_start")
    return {"freeze_events_0p8s": freezes}


def cmd_mint(a) -> None:
    from google.genai import types
    pl = plate(a.plate)
    q = pl["quality"]
    model = MODELS[q]
    log = load_log()
    if a.still:
        still = Path(a.still)
    else:
        mine = [s for s in log["stills"] if s["plate"] == a.plate]
        if not mine:
            raise SystemExit(f"STOP: no start frame for {a.plate} (run still first)")
        still = REPO / mine[-1]["file"]
    RAW.mkdir(parents=True, exist_ok=True)
    take = 1
    while (RAW / f"{a.plate}_t{take}.mp4").exists() or any(
            t["plate"] == a.plate and t["take"] == take for t in log["takes"]):
        take += 1
    dest = RAW / f"{a.plate}_t{take}.mp4"
    dest.touch()
    body = pl["prompt"]
    if a.daylight:
        body = body.replace(CANDLE_LINE, DAYLIGHT_LINE)
    for rep in a.replace or []:
        old, new = rep.split("=>", 1)
        if old not in body:
            raise SystemExit(f"STOP: --replace text not in the board prompt: {old!r}")
        body = body.replace(old, new)
    prompt = f"{STYLE} {body} {a.extra or ''}"
    prompt += (" Exactly ONE Explorer: young boy, messy brown hair, round thin gold glasses, teal "
               "long coat, tan waistcoat, brown bow tie, satchel." if pl.get("explorer") else " No Explorer.")
    prompt = f"{prompt} {VEO_TAIL}"
    print(f"=== MINT {a.plate} take={take} {q} model={model} path=vertex project={PROJECT} "
          f"location={LOCATION} res={RESOLUTION} framing={a.framing} ===", flush=True)
    c = client()
    t0 = time.time()
    op = c.models.generate_videos(
        model=model,
        source=types.GenerateVideosSource(prompt=prompt, image=types.Image.from_file(location=str(still))),
        config=types.GenerateVideosConfig(number_of_videos=1, duration_seconds=CLIP_S,
                                          aspect_ratio="16:9", resolution=RESOLUTION,
                                          generate_audio=False),
    )
    entry = {
        "plate": a.plate, "take": take, "model": model, "quality": q, "path": "vertex",
        "seconds": CLIP_S, "resolution": RESOLUTION, "generate_audio": False,
        "framing": a.framing, "extra": a.extra, "daylight": a.daylight, "replace": a.replace,
        "start_frame": rel(still), "start_frame_sha256": sha256(still),
        "op_name": op.name, "submitted_at": now(),
        "cost_usd": round(CLIP_S * USD_PER_S[q], 3),
        "status": "SUBMITTED", "why": None, "at": now(),
    }
    update_log(lambda log: log["takes"].append(entry))
    finish(c, op, a.plate, take, t0)


def finish(c, op, pid: str, take: int, t0: float) -> None:
    dest = RAW / f"{pid}_t{take}.mp4"
    while not op.done:
        time.sleep(12)
        op = c.operations.get(op)
        print(f"  poll {pid} … {int(time.time() - t0)}s", flush=True)

    def set_take(**kw):
        def apply(log: dict) -> None:
            for t in log["takes"]:
                if t["plate"] == pid and t["take"] == take:
                    t.update(kw)
        return update_log(apply)

    if getattr(op, "error", None):
        dest.unlink(missing_ok=True)
        set_take(status="ERROR", why=str(op.error)[:500], cost_usd=0.0, at=now())
        raise SystemExit(f"STOP: Vertex error {str(op.error)[:400]}")
    vids = op.response.generated_videos if op.response else None
    if not vids:
        filt = getattr(op.response, "rai_media_filtered_reasons", None) if op.response else None
        dest.unlink(missing_ok=True)
        set_take(status="FILTERED", why=str(filt)[:500], cost_usd=0.0, at=now())
        raise SystemExit(f"STOP: no video (filtered: {filt})")
    raw = dest.with_suffix(".src.mp4")
    v = vids[0].video
    if getattr(v, "video_bytes", None):
        raw.write_bytes(v.video_bytes)
    else:
        v.save(str(raw))
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(raw),
                    "-map", "0:v:0", "-c", "copy", "-an", str(dest)], check=True)
    raw.unlink(missing_ok=True)
    dur = probe_dur(dest)
    sheet = UAT / f"{pid}_t{take}_sheet.jpg"
    uat_sheet(dest, sheet)
    log = set_take(file=rel(dest), sha256=sha256(dest), duration_s=round(dur, 3),
                   uat_sheet=rel(sheet), motion=motion_stats(dest),
                   api_s=round(time.time() - t0, 1), status="PENDING_UAT", at=now())
    print(json.dumps({"file": rel(dest), "duration_s": round(dur, 3), "uat_sheet": rel(sheet)}))
    print(f"running total ${log['cost_usd_total']:.2f}")


def cmd_resume(a) -> None:
    from google.genai import types
    log = load_log()
    hit = [t for t in log["takes"] if t["plate"] == a.plate and t["take"] == a.take and t.get("op_name")]
    if not hit:
        raise SystemExit("STOP: no op_name recorded for that take")
    c = client()
    op = types.GenerateVideosOperation(name=hit[0]["op_name"])
    finish(c, c.operations.get(op), a.plate, a.take, time.time())


def cmd_verdict(a) -> None:
    def apply(log: dict) -> None:
        hit = [t for t in log["takes"] if t["plate"] == a.plate and t["take"] == a.take]
        if not hit:
            raise SystemExit("STOP: no such take")
        t = hit[0]
        t["status"], t["why"], t["uat_at"] = a.status, a.why, now()
        if a.status == "KEEP":
            log["plates"][a.plate] = {"keep": t["file"], "take": a.take, "sha256": t["sha256"],
                                      "model": t["model"], "path": "vertex"}
    update_log(apply)
    print(f"{a.status} {a.plate} t{a.take}: {a.why}")


def cmd_total(_a) -> None:
    log = load_log()
    keeps = len(log["plates"])
    n = len(board()["plates"])
    print(f"takes={len(log['takes'])} stills={len(log['stills'])} keep={keeps}/{n} "
          f"cost_usd=${log['cost_usd_total']:.2f}")


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("still"); s.add_argument("plate"); s.add_argument("--seed"); s.add_argument("--extra")
    m = sub.add_parser("mint"); m.add_argument("plate"); m.add_argument("--still")
    m.add_argument("--framing", default="try1"); m.add_argument("--extra")
    m.add_argument("--daylight", action="store_true", help="swap the board's candlelight line for daylight (Fast plates)")
    m.add_argument("--replace", action="append", help="'old=>new' edit of the board prompt for this take (logged)")
    v = sub.add_parser("verdict"); v.add_argument("plate"); v.add_argument("take", type=int)
    v.add_argument("status", choices=["KEEP", "FAIL"]); v.add_argument("why")
    r = sub.add_parser("resume"); r.add_argument("plate"); r.add_argument("take", type=int)
    sub.add_parser("total")
    a = ap.parse_args()
    {"still": cmd_still, "mint": cmd_mint, "verdict": cmd_verdict, "resume": cmd_resume,
     "total": cmd_total}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
