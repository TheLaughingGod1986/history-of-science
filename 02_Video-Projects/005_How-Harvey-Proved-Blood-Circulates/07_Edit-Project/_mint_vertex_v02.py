#!/usr/bin/env python3
"""HOS 005 Parts 02–05 on Vertex AI Veo 3.1 (Ben's OK for 005, 1 Oct 2026). Part 01's tool, per part.

Project gen-lang-client-0538779324 ("History of Science"), us-central1, ADC as
benoats@googlemail.com. Never an Orbit project. Tokens are never printed.

  --part N still   <plate> [--seed <jpg>] [--extra "…"]   start frame (Vertex gemini-2.5-flash-image)
  --part N mint    <plate> [--still <jpg>] [--framing f] [--extra "…"] [--replace 'a=>b']
  --part N auto    <plate> [--seed <jpg>] [--still-extra "…"] [--extra "…"]   still (if none) then mint
  --part N resume  <plate> <take>                        finish a submitted take from its op_name
  --part N verdict <plate> <take> KEEP|FAIL "why"        plate UAT result
  --part N total                                         part cost; film cost and projected credit

Quality plates → veo-3.1-generate-001, Fast → veo-3.1-fast-generate-001, 1080p,
8 s, generate_audio=False (video-only SKU), audio stream removed after download.
Start frames attach the Part 01 Harvey reference on `harvey_ref` plates and the Explorer
sheet + generation reference on Explorer plates. Every spend is refused if the projected
Free Trial credit would fall below the floor (£20 for 005 since 2 Oct 2026) (see `projected_gbp`).
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
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))
from ai_spend_hook import film_of, spend as ai_spend  # noqa: E402
EDIT = PROJ / "07_Edit-Project"
PART = "02"
BOARD = LOG = STILLS = RAW = UAT = LOCK = Path()


def set_part(n: str) -> None:
    global PART, BOARD, LOG, STILLS, RAW, UAT, LOCK
    PART = f"{int(n):02d}"
    BOARD = EDIT / f"parts/part-{PART}_plates_v02.json"
    LOG = EDIT / f"PART{PART}_MINT_LOG_v01.json"
    STILLS = PROJ / f"04_Generated-Clips/part{PART}/refs/v02_vertex_stills"
    RAW = PROJ / f"04_Generated-Clips/part{PART}/raw/v01"
    UAT = PROJ / f"04_Generated-Clips/part{PART}/uat"
    LOCK = EDIT / f".part{PART}_mint_log.lock"


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
EXPLORER_SHEET = REPO / "01_Character/01_Master-References/hos-explorer-character-sheet-v01.jpg"
HARVEY_REF = PROJ / "04_Generated-Clips/refs/harvey_ref_v01.jpg"
STYLE_REFS_005 = (PROJ / "04_Generated-Clips/part01/refs/v02_vertex_stills/09_heart_clock_v02.jpg",
                   PROJ / "04_Generated-Clips/part01/refs/v02_vertex_stills/03_band_tightens_v02.jpg")
CREDIT_LOG = EDIT / "VERTEX_CREDIT_LOG_v01.json"
# Free Trial on the console before any 005 Vertex spend (1 Oct 23:05 UK, Part 01 section).
CREDIT_BASE_GBP = 209.53
GBP_PER_USD = 0.80  # conservative; list prices are in USD, the credit is in GBP
FLOOR_GBP = 20.0  # Ben via desk PR #180 (comment 5944398833), 2 Oct 2026: £60 → £20 for 005
STYLE = (
    "History of Science locked look: premium Animistry-class 3D cartoon, finished "
    "materials, warm cinematic light, 17th-century world. Not photoreal, not flat 2D. "
    "No logos, no captions, no signs, no UI. No Orbit orange robot. No DNA helix. "
    "Wonder, not gore: no wounds, no blood on skin, no cut flesh, no animal organs."
)
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


def film_spend_usd() -> float:
    total = 0.0
    for f in sorted(EDIT.glob("PART0*_MINT_LOG_v01.json")):
        total += float(json.loads(f.read_text()).get("cost_usd_total", 0.0))
    return total


def projected_gbp(extra_usd: float = 0.0) -> float:
    """Free Trial left after everything 005 has spent: the lower of (base − all logged spend) and
    the latest console reading (which lags by hours, and the billing account is shared)."""
    est = CREDIT_BASE_GBP - (film_spend_usd() + extra_usd) * GBP_PER_USD
    if CREDIT_LOG.exists():
        rs = json.loads(CREDIT_LOG.read_text()).get("readings", [])
        if rs:
            est = min(est, float(rs[-1]["free_trial_remaining_gbp"]) - extra_usd * GBP_PER_USD)
    return est


def guard(cost_usd: float) -> None:
    left = projected_gbp(cost_usd)
    if left < FLOOR_GBP:
        raise SystemExit(f"STOP: projected Free Trial £{left:.2f} after this ${cost_usd:.2f} would fall "
                         f"below the £{FLOOR_GBP:.0f} floor. Report to the desk.")


def load_log() -> dict:
    if LOG.exists():
        return json.loads(LOG.read_text())
    return {
        "film": "005_How-Harvey-Proved-Blood-Circulates",
        "part": PART,
        "board": rel(BOARD),
        "path": "vertex",
        "vertex_project": PROJECT,
        "vertex_location": LOCATION,
        "account": ACCOUNT,
        "authority": ("Ben, 1 Oct 2026 (chat with Claude): Vertex for 005; Part 01 OK'd by Ben 1 Oct; "
                      "Parts 02–05 desk PR #180 comment 5942662028"),
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
    with LOCK.open("w") as lk:
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


def with_retry(fn, what: str, tries: int = 8):
    """Vertex answers 429 RESOURCE_EXHAUSTED under parallel load: back off and try again."""
    for i in range(tries):
        try:
            return fn()
        except Exception as e:  # noqa: BLE001
            if "429" not in str(e) and "RESOURCE_EXHAUSTED" not in str(e) or i == tries - 1:
                raise
            wait = min(20 * (i + 1), 120)
            print(f"  429 on {what}; retry in {wait}s", flush=True)
            time.sleep(wait)


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
    if pl["quality"] == "Fast":
        tail += (" ABSOLUTELY NO candles, candlesticks, oil lamps, table lamps, lanterns, fireplaces "
                 "or any flame anywhere in the image; the only light is daylight from a window.")
    return ("Finished 3D cartoon still: the FIRST frame of this moving shot, key subject "
            f"mid-action and readable, no motion blur. {p.strip()} {extra} {STYLE}{tail}").strip()


def cmd_still(a) -> None:
    from google.genai import types
    pl = plate(a.plate)
    guard(USD_PER_STILL)
    STILLS.mkdir(parents=True, exist_ok=True)
    n = 1
    while (STILLS / f"{a.plate}_v{n:02d}.jpg").exists():
        n += 1
    dest = STILLS / f"{a.plate}_v{n:02d}.jpg"
    dest.touch()
    parts, lead, k = [], "", 0
    # The 001 ward and the 004 thumb pull in their rooms and lit lamps; Part 01's passed frames
    # are this film's look.
    style = tuple(Path(r) for r in getattr(a, "style_ref", None) or ()) or STYLE_REFS_005
    refs = tuple((r, "this film's locked look (passed by Ben)") for r in style)
    for ref, what in refs:
        if ref.exists():
            parts.append(img_part(ref)); k += 1
            lead += (f"Image {k} shows {what} only: match its 3D cartoon material, finish and warm "
                     "light. Do NOT copy its room, people, objects or any text. ")
    if a.seed:
        seed = Path(a.seed)
        parts.append(img_part(seed)); k += 1
        lead += (f"Image {k} is the previous shot in the same set: keep its set, palette, props "
                 "and character design consistent. ")
    if pl.get("harvey_ref") and HARVEY_REF.exists():
        parts.append(img_part(HARVEY_REF)); k += 1
        lead += (f"Image {k} is William Harvey from an earlier shot of this film: keep exactly the same "
                 "man, readable face, olive skin, black hair to the collar, small pointed black beard "
                 "and moustache, black physician's gown with a white collar (older or younger only if "
                 "the shot says so). Ignore the lantern and the street behind him. ")
    if pl.get("explorer"):
        for ref, what in ((EXPLORER_SHEET, "the Explorer character sheet"),
                          (EXPLORER_REF, "the Explorer generation reference")):
            if ref.exists():
                parts.append(img_part(ref)); k += 1
                lead += (f"Image {k} is {what}: match him exactly (round thin gold glasses, teal long "
                         "coat, tan waistcoat, brown bow tie, full messy brown hair), rendered in this "
                         "film's 3D cartoon finish, exactly one Explorer. ")
    parts.append(lead + still_prompt(pl, a.extra or ""))
    c = client()
    print(f"STILL {a.plate} v{n:02d} model={IMAGE_MODEL} path=vertex project={PROJECT}", flush=True)
    try:
        r = with_retry(lambda: c.models.generate_content(
            model=IMAGE_MODEL, contents=parts,
            config=types.GenerateContentConfig(response_modalities=["IMAGE"],
                                               image_config=types.ImageConfig(aspect_ratio="16:9"))),
            f"still {a.plate}")
    except BaseException:
        dest.unlink(missing_ok=True)
        raise
    data = None
    for cand in r.candidates or []:
        for part in (cand.content.parts if cand.content else []) or []:
            if part.inline_data and part.inline_data.data:
                data = part.inline_data.data
    if not data:
        dest.unlink(missing_ok=True)
        raise SystemExit(f"STOP: no image for {a.plate}")
    to_1080(data, dest)
    rec = {"plate": a.plate, "v": n, "file": rel(dest), "sha256": sha256(dest),
           "model": IMAGE_MODEL, "seed": a.seed and rel(Path(a.seed)),
           "style_refs": [rel(r) for r, _ in refs],
           "extra": a.extra, "cost_usd": USD_PER_STILL, "at": now()}
    update_log(lambda log: log["stills"].append(rec))
    ai_spend("vertex", round(USD_PER_STILL * GBP_PER_USD, 3), film_of(PROJ),
             f"P{PART}:{a.plate} start still v{n:02d} ({IMAGE_MODEL})")
    print(f"SAVED {dest}")
    return dest


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
    q = getattr(a, "quality", None) or pl["quality"]
    model = MODELS[q]
    guard(CLIP_S * USD_PER_S[q])
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
    try:
        op = with_retry(lambda: c.models.generate_videos(
            model=model,
            source=types.GenerateVideosSource(prompt=prompt, image=types.Image.from_file(location=str(still))),
            config=types.GenerateVideosConfig(number_of_videos=1, duration_seconds=CLIP_S,
                                              aspect_ratio="16:9", resolution=RESOLUTION,
                                              generate_audio=False),
        ), f"mint {a.plate}")
    except BaseException:
        dest.unlink(missing_ok=True)
        raise
    entry = {
        "plate": a.plate, "take": take, "model": model, "quality": q, "path": "vertex",
        "seconds": CLIP_S, "resolution": RESOLUTION, "generate_audio": False,
        "framing": a.framing, "extra": a.extra, "light_fix": bool(pl.get("light_fix")), "replace": a.replace,
        "prompt": prompt,
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
    t = next(t for t in log["takes"] if t["plate"] == pid and t["take"] == take)
    ai_spend("vertex", round(float(t.get("cost_usd", 0)) * GBP_PER_USD, 2), film_of(PROJ),
             f"P{PART}:{pid} take {take} {t.get('quality')} ({t.get('model')}, {t.get('seconds')} s)")
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
    lost = sum(t.get("cost_usd", 0) for t in log["takes"] if t.get("status") == "LOST")
    print(f"part {PART}: takes={len(log['takes'])} stills={len(log['stills'])} keep={keeps}/{n} "
          f"cost_usd=${log['cost_usd_total']:.2f} (lost ${lost:.2f})")
    print(f"film 005 Vertex spend ${film_spend_usd():.2f} · projected Free Trial "
          f"£{projected_gbp():.2f} (floor £{FLOOR_GBP:.0f}, £/$ {GBP_PER_USD})")


def cmd_auto(a) -> None:
    log = load_log()
    if a.still:
        pass
    elif not [s for s in log["stills"] if s["plate"] == a.plate]:
        a.still = str(cmd_still(argparse.Namespace(plate=a.plate, seed=a.seed, extra=a.still_extra)))
    cmd_mint(a)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--part", required=True)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("still"); s.add_argument("plate"); s.add_argument("--seed"); s.add_argument("--extra")
    s.add_argument("--style-ref", action="append",
                   help="look reference replacing STYLE_REFS_005 (repeatable; e.g. drop a ref whose props would leak)")
    for name in ("mint", "auto"):
        m = sub.add_parser(name); m.add_argument("plate"); m.add_argument("--still")
        m.add_argument("--framing", default="try1"); m.add_argument("--extra")
        m.add_argument("--quality", choices=sorted(MODELS),
                       help="engine override for this take (logged), e.g. a plate reframed as a glowing cutaway")
        m.add_argument("--replace", action="append", help="'old=>new' edit of the board prompt for this take (logged)")
        if name == "auto":
            m.add_argument("--seed"); m.add_argument("--still-extra")
    v = sub.add_parser("verdict"); v.add_argument("plate"); v.add_argument("take", type=int)
    v.add_argument("status", choices=["KEEP", "FAIL"]); v.add_argument("why")
    r = sub.add_parser("resume"); r.add_argument("plate"); r.add_argument("take", type=int)
    sub.add_parser("total")
    a = ap.parse_args()
    set_part(a.part)
    {"still": cmd_still, "mint": cmd_mint, "auto": cmd_auto, "verdict": cmd_verdict,
     "resume": cmd_resume, "total": cmd_total}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
