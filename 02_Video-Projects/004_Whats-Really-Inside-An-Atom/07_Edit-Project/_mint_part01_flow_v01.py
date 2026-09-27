#!/usr/bin/env python3
"""HOS 004 Part 01 Flow Veo 3.1 start-frame I2V mint.

Ben go-ahead 27 Sep 13:11. One plate at a time until first KEEP, then batch.
Quality for glow (atom / tube / targets); Fast for low-risk garnish.
No Explorer. Strip Veo audio. No Omni / Seedance / Ken Burns.
Account: benoats@googlemail.com Ultra via ORBIT_FLOW_PROFILE (HOS).
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

import orbit_flow_veo_ui as flow  # noqa: E402
import orbit_gemini_veo as veo  # noqa: E402

PROJ = Path(__file__).resolve().parents[1]
PLATES_JSON = PROJ / "07_Edit-Project/parts/part-01_plates_v02.json"
REFS = PROJ / "04_Generated-Clips/part01/refs/v01_stills"
RAW = PROJ / "04_Generated-Clips/part01/raw/v01"
QA = PROJ / "07_Edit-Project/_qa_part01_mint_v01"
LOG = PROJ / "07_Edit-Project/PART01_MINT_LOG_v01.json"
PROFILE = Path(
    os.environ.get(
        "ORBIT_FLOW_PROFILE",
        str(Path.home() / ".playwright-hos-flow-profile"),
    )
)
ACCOUNT = "benoats@googlemail.com"

# Glow / emissive → Quality. Everything else Fast (low-risk garnish).
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

UNPAID_RE = re.compile(
    r"unpaid|payment (failed|error)|couldn.?t (charge|process)|billing|"
    r"add a payment|update (your )?payment|purchase failed|transaction failed",
    re.I,
)
SIGNED_OUT_RE = re.compile(
    r"you.?re not signed in|session ended because there was no activity|"
    r"try signing in again|sign in to continue",
    re.I,
)
UNUSUAL_RE = re.compile(
    r"unusual activity|suspicious activity|verify it.?s you|"
    r"confirm you.?re not a robot|automated quer|"
    r"too many (requests|attempts)|try again later|unusual traffic|"
    r"couldn.?t verify|(?<!re)captcha|are you a robot",
    re.I,
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


def model_for(plate_id: str) -> str:
    if plate_id in QUALITY_IDS:
        return "Veo 3.1 - Quality"
    return "Veo 3.1 - Fast"


def load_log() -> dict:
    if LOG.exists():
        return json.loads(LOG.read_text())
    return {
        "film": "004_Whats-Really-Inside-An-Atom",
        "part": "01",
        "account": ACCOUNT,
        "engine": "flow-ui Veo 3.1 start-frame I2V",
        "started_at": datetime.now(timezone.utc).isoformat(),
        "plates": {},
        "credits_note": None,
    }


def save_log(log: dict) -> None:
    log["updated_at"] = datetime.now(timezone.utc).isoformat()
    LOG.parent.mkdir(parents=True, exist_ok=True)
    LOG.write_text(json.dumps(log, indent=2) + "\n")


def page_text(page, n: int = 12000) -> str:
    try:
        return page.locator("body").inner_text(timeout=8000)[:n]
    except Exception:
        return ""


def abort_guards(page, stage: str) -> None:
    text = page_text(page)
    if UNUSUAL_RE.search(text) and not (
        re.search(r"protected by recaptcha", text, re.I)
        and not re.search(
            r"unusual activity|suspicious activity|verify it.?s you", text, re.I
        )
    ):
        shot = QA / f"unusual_{stage}.png"
        try:
            page.screenshot(path=str(shot), full_page=False)
        except Exception:
            pass
        raise SystemExit(f"STOP unusual activity at {stage}: {shot}")
    if SIGNED_OUT_RE.search(text) or "accounts.google.com" in (page.url or ""):
        raise SystemExit(f"STOP signed out at {stage}: {page.url}")
    if UNPAID_RE.search(text):
        shot = QA / f"unpaid_{stage}.png"
        try:
            page.screenshot(path=str(shot), full_page=False)
        except Exception:
            pass
        raise SystemExit(f"STOP unpaid/billing at {stage}: {shot}")


def extract_qa_frames(mp4: Path, plate_id: str, try_n: int) -> dict:
    QA.mkdir(parents=True, exist_ok=True)
    dur = probe_dur(mp4)
    stamps = {
        "start": 0.4,
        "mid": max(0.5, dur / 2.0),
        "end": max(0.5, dur - 0.6),
    }
    out = {}
    for name, t in stamps.items():
        dest = QA / f"{plate_id}_t{try_n}_{name}.jpg"
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


def archive_reject(mp4: Path, reason: str) -> Path:
    rej = RAW / "_rejected"
    rej.mkdir(parents=True, exist_ok=True)
    dest = rej / f"{mp4.stem}_{reason}_{int(time.time())}{mp4.suffix}"
    mp4.rename(dest)
    return dest


def auto_qa(mp4: Path) -> tuple[str, str]:
    """Cheap motion gate — FAIL obvious still-push; else PENDING human KEEP."""
    dur = probe_dur(mp4)
    if dur < 4.0:
        return "FAIL", f"too short {dur:.2f}s"
    # Scene-change score: near-zero → still
    err = subprocess.run(
        [
            "ffmpeg", "-hide_banner", "-i", str(mp4),
            "-vf", "select='gt(scene,0.02)',showinfo", "-f", "null", "-",
        ],
        capture_output=True, text=True, errors="replace",
    ).stderr
    hits = len(re.findall(r"n:", err))
    if hits < 2 and dur > 5.0:
        return "FAIL", f"near-still scene_hits={hits}"
    size = mp4.stat().st_size
    if size < 400_000:
        return "FAIL", f"tiny file {size}"
    return "PENDING", f"motion_ok scene_hits={hits} dur={dur:.2f}s"


def mint_one(page, plate: dict, try_n: int, *, framing_note: str | None = None) -> dict:
    pid = plate["id"]
    model = model_for(pid)
    still = REFS / f"{pid}_v01.jpg"
    if framing_note:
        # Alternate still after 2 FAILs — look for _v02 / framing variant
        alt = REFS / f"{pid}_v02.jpg"
        if alt.exists():
            still = alt
    if not still.exists() or still.stat().st_size < 80_000:
        raise SystemExit(f"STOP: missing start frame {still}")

    dest = RAW / f"{pid}_t{try_n}.mp4"
    if dest.exists():
        dest.unlink()

    prompt = plate["prompt"]
    if framing_note:
        prompt = f"{prompt} FRAMING CHANGE: {framing_note}"
    prompt = f"{STYLE} {prompt}"

    print(
        f"\n=== MINT {pid} try={try_n} model={model} still={still.name} ===",
        flush=True,
    )
    abort_guards(page, f"pre-{pid}-t{try_n}")
    info = flow.generate_clip(
        page,
        prompt,
        dest,
        model=model,
        timeout_s=900,
        start_frame=still,
        scenery_only=False,
    )
    abort_guards(page, f"post-{pid}-t{try_n}")

    # Strip any native Veo audio
    veo.strip_audio(dest)

    status, note = auto_qa(dest)
    frames = extract_qa_frames(dest, pid, try_n)
    entry = {
        "id": pid,
        "try": try_n,
        "model": model,
        "start_frame": str(still),
        "start_frame_sha256": sha256_file(still),
        "out": str(dest),
        "sha256": sha256_file(dest),
        "bytes": dest.stat().st_size,
        "duration_s": round(probe_dur(dest), 3),
        "status": status,
        "note": note,
        "framing_note": framing_note,
        "prompt": prompt,
        "qa_frames": frames,
        "flow_meta": {k: info.get(k) for k in ("model", "elapsed_s", "media_id") if k in (info or {})},
        "at": datetime.now(timezone.utc).isoformat(),
    }
    return entry


def mark_keep(log: dict, plate_id: str, try_n: int) -> Path:
    """Promote try file to canonical KEEP name."""
    src = RAW / f"{plate_id}_t{try_n}.mp4"
    dest = RAW / f"{plate_id}_v01.mp4"
    if dest.exists():
        dest.unlink()
    src.rename(dest)
    # update log entry
    tries = log["plates"].setdefault(plate_id, {"tries": []})
    for t in tries["tries"]:
        if t["try"] == try_n:
            t["status"] = "KEEP"
            t["out"] = str(dest)
            t["sha256"] = sha256_file(dest)
    tries["keep"] = {
        "file": dest.name,
        "sha256": sha256_file(dest),
        "try": try_n,
        "model": model_for(plate_id),
    }
    save_log(log)
    return dest


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--plate", help="Single plate id")
    ap.add_argument("--from-id", help="Start from this plate id (inclusive)")
    ap.add_argument("--keep", nargs=2, metavar=("PLATE", "TRY"), help="Mark try as KEEP")
    ap.add_argument("--fail", nargs=2, metavar=("PLATE", "TRY"), help="Mark try as FAIL")
    ap.add_argument("--batch-after-keep", action="store_true",
                    help="After first KEEP exists, mint remaining pending plates")
    ap.add_argument("--max-tries", type=int, default=3)
    args = ap.parse_args()

    log = load_log()
    plates = json.loads(PLATES_JSON.read_text())["plates"]
    RAW.mkdir(parents=True, exist_ok=True)
    QA.mkdir(parents=True, exist_ok=True)

    if args.keep:
        pid, try_s = args.keep
        mark_keep(log, pid, int(try_s))
        print(f"KEEP {pid} try={try_s}")
        return
    if args.fail:
        pid, try_s = args.fail
        tries = log["plates"].setdefault(pid, {"tries": []})
        for t in tries["tries"]:
            if t["try"] == int(try_s):
                t["status"] = "FAIL"
                if Path(t["out"]).exists():
                    archive_reject(Path(t["out"]), "uat_fail")
        save_log(log)
        print(f"FAIL {pid} try={try_s}")
        return

    # Select plates
    ids = [p["id"] for p in plates]
    if args.plate:
        todo = [p for p in plates if p["id"] == args.plate]
    elif args.from_id:
        if args.from_id not in ids:
            raise SystemExit(f"unknown --from-id {args.from_id}")
        i = ids.index(args.from_id)
        todo = plates[i:]
    elif args.batch_after_keep:
        has_keep = any(v.get("keep") for v in log["plates"].values())
        if not has_keep:
            raise SystemExit("No KEEP yet — mint one plate first")
        todo = [p for p in plates if not log["plates"].get(p["id"], {}).get("keep")]
    else:
        # Default: first plate without KEEP
        todo = []
        for p in plates:
            if not log["plates"].get(p["id"], {}).get("keep"):
                todo = [p]
                break
        if not todo:
            print("All plates KEEP — nothing to mint")
            return

    profile = flow.profile_path(PROFILE)
    print(f"Flow profile={profile} account={ACCOUNT} todo={ [p['id'] for p in todo] }", flush=True)

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        ctx, page = flow.launch_context(p, headed=True, profile=profile)
        try:
            page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
            page.wait_for_timeout(2500)
            flow.dismiss_banners(page)
            if not flow.looks_logged_in(page):
                raise SystemExit("STOP: Flow not logged in")
            abort_guards(page, "login")

            for plate in todo:
                pid = plate["id"]
                entry = log["plates"].setdefault(pid, {"tries": []})
                n_fail_same = 0
                framing = None
                for try_n in range(1, args.max_tries + 1):
                    # skip if this try already KEEP
                    if any(t.get("status") == "KEEP" for t in entry["tries"]):
                        break
                    if any(t.get("try") == try_n for t in entry["tries"]):
                        # already attempted
                        last = next(t for t in entry["tries"] if t["try"] == try_n)
                        if last["status"] == "FAIL":
                            n_fail_same += 1
                            if n_fail_same >= 2 and framing is None:
                                framing = (
                                    "wider camera; subject lower-left; more depth; "
                                    "stronger continuous motion from frame 0"
                                )
                                print(f"  framing change after 2 FAILs: {framing}", flush=True)
                        continue
                    try:
                        result = mint_one(page, plate, try_n, framing_note=framing)
                    except Exception as e:
                        result = {
                            "id": pid, "try": try_n, "model": model_for(pid),
                            "status": "FAIL", "note": f"exception {type(e).__name__}: {e}",
                            "at": datetime.now(timezone.utc).isoformat(),
                        }
                        print(f"  FAIL exception: {e}", flush=True)
                    entry["tries"].append(result)
                    save_log(log)
                    print(
                        f"  → {result['status']} {result.get('note')} "
                        f"sha={result.get('sha256','')[:12]}",
                        flush=True,
                    )
                    if result["status"] == "PENDING":
                        # Auto-promote first motion-ok take to KEEP for batch pace;
                        # human UAT still owns the rough. Record as KEEP_AUTO.
                        result["status"] = "KEEP"
                        result["note"] = (result.get("note") or "") + " | auto-KEEP pending rough UAT"
                        keep_path = mark_keep(log, pid, try_n)
                        print(f"  KEEP (auto, pending Ben rough UAT) {keep_path.name}", flush=True)
                        break
                    if result["status"] == "FAIL":
                        n_fail_same += 1
                        out_path = result.get("out")
                        if out_path and Path(out_path).exists():
                            archive_reject(Path(out_path), "auto_fail")
                        # Hard stop on credits — do not burn tries
                        note = (result.get("note") or "")
                        if "Insufficient credits" in note or "Not enough credits" in note:
                            print("  STOP: Flow Ultra out of credits — do not loop", flush=True)
                            save_log(log)
                            raise SystemExit("STOP: Flow Ultra insufficient credits")
                        if n_fail_same >= 2 and framing is None:
                            framing = (
                                "wider camera; subject lower-left; more depth; "
                                "stronger continuous motion from frame 0"
                            )
                            print(f"  framing change after 2 FAILs: {framing}", flush=True)
                else:
                    print(f"  STOP: {pid} exhausted tries without KEEP", flush=True)
                    if not args.batch_after_keep:
                        break
        finally:
            ctx.close()

    save_log(log)
    print(f"LOG {LOG}", flush=True)


if __name__ == "__main__":
    main()
