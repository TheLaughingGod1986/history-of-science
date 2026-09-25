#!/usr/bin/env python3
"""Part 04 Flow remint v14 — ONLY 09b_risk_hold CLEAN GLOW (chair-top flame UAT FAIL).

Parent FAIL: hos_002_part04_rough_v13.mp4
  sha256 27828f216c289d36aaeae7311c545cdf0fb829381ff110c528cc40008710cd6a
Single blocker @ ~105s under FAMILY FIRST side-label = chair-top flame.
Timeline: plate09b = 98.15–106.05; plate 10 floating-cards starts ~105.7.
Fail still matches 09b (not plate 10). Remint 09b only; KEEP all other v13 plates.

Empty Chairs glow = soft rectangular backrest panel ONLY — ZERO chair-top flame /
fire wisp / white seat fire / lamp smoke.
Flow: benoats@googlemail.com on /u/1/. Scores → CoS. No PASS. No Ben ping.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))

import orbit_flow_veo_ui as flow  # noqa: E402

flow.FLOW_HOME = os.environ.get("ORBIT_FLOW_HOME", "https://flow.google.com/u/1/")

PROJ = Path(__file__).resolve().parents[1]
RAW = PROJ / "04_Generated-Clips/part04/raw/v14_fast"
REJECTED = RAW / "_rejected"
QA = PROJ / "07_Edit-Project/_qa_part04_v14_plate"
META = PROJ / "07_Edit-Project/part04_mint_flow_v14_meta.json"
HARVEST = Path(__file__).resolve().parent / "_harvest_newest_gallery_v01.py"
FORCE_DL = Path(__file__).resolve().parent / "_harvest_force_download_v01.py"

PID = "09b_risk_hold"
START = (
    PROJ
    / "04_Generated-Clips/part04/refs/v14_start_frames/09b_risk_hold_start_v14_clean_glow.jpg"
)
MODEL = os.environ.get("ORBIT_FLOW_VEO_MODEL", "Veo 3.1 - Fast")
PROFILE = Path(
    os.environ.get(
        "ORBIT_FLOW_PROFILE",
        str(Path.home() / ".playwright-hos-flow-profile"),
    )
)
REQUIRED_FLOW_EMAIL = "benoats@googlemail.com"
ALLOWED_FLOW_EMAILS = {REQUIRED_FLOW_EMAIL, "benoats@gmail.com"}
FORBIDDEN_FLOW_EMAIL = "benoats86@gmail.com"
MAX_CREATES = int(os.environ.get("HOS_V14_MAX_CREATES", "4"))

PARENT_V13 = PROJ / "09_Final-Export/hos_002_part04_rough_v13.mp4"
PARENT_V13_SHA = "27828f216c289d36aaeae7311c545cdf0fb829381ff110c528cc40008710cd6a"

STYLE = (
    "Animistry-class stylised 3D cartoon (NOT photoreal). "
    "ONE continuous 1869 chemist desk: honey wood desktop, soft warm lamp, cream "
    "element cards with readable ink letters/symbols (H/C/O/N/Li — NEVER blank), "
    "leather books. Continuous real camera/object motion the whole clip. Silent. "
    "No Orbit. No Ken Burns still."
)

LAMP_CLEAN_LOCK = (
    "LAMP CLEAN LOCK: soft warm desk-lamp glow ONLY. HARD REJECT: lamp spitting fire, "
    "sparks under the bulb, candle flames, smoke wisps from lamp or chair, any vapor "
    "trail near the lamp head. ZERO open flames anywhere."
)

EMPTY_CHAIRS_GLOW_LOCK = (
    "EMPTY CHAIRS GLOW LOCK (match cleared A BET ~98s / ok_abet_98): soft rectangular "
    "backrest PANEL glow ONLY — a gentle warm softbox rectangle on the empty chair's "
    "inner backrest panel. Chair top rail stays plain dark wood — ZERO flame, ZERO fire "
    "wisp, ZERO orange/yellow fire tongue on the chair top, ZERO white seat fire, ZERO "
    "ember tips. Soft panel edge light is OK; fire shapes are FORBIDDEN."
)

WRITTEN_CARDS_LOCK = (
    "WRITTEN CARDS LOCK: every visible element card shows readable hand-ink H/C/O/N/Li "
    "(etc.) with small numbers. HARD REJECT blank cream cards."
)

WINDOW_LOCK = (
    "NO WINDOW / NO blue sky fills / NO roofs outdoors. Indoor wood panel + bookcase only."
)

REJECT = (
    "HARD REJECT: any flame, fire wisp, orange/yellow fire on chair top, white seat fire, "
    "burning leather, candle, torch, lamp smoke, vapor wisps, flat blue sky fills, roofs, "
    "blank cards, photoreal, Orbit robot, people, Explorer."
)

PROMPT = (
    "Image-to-video from the attached start frame. Same 1869 chemist desk DNA. "
    "Quiet hold on an EMPTY wooden chair with soft rectangular backrest PANEL glow ONLY "
    "(match ok_abet_98 clean glow — NEVER flames on the chair top). "
    "WRITTEN cream element cards stay readable on the desk (H/C/O/N/Li). "
    "Soft warm desk-lamp glow ONLY — crystal-clear air, ZERO smoke. "
    "Continuous subtle camera settle. Fully indoor wood/bookcase. "
    f"{EMPTY_CHAIRS_GLOW_LOCK} {LAMP_CLEAN_LOCK} {WRITTEN_CARDS_LOCK} {WINDOW_LOCK} "
    "Silent. No people. No Explorer. "
    + REJECT
    + " "
    + STYLE
)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def safe_close(ctx) -> None:
    try:
        if ctx is not None:
            ctx.close()
    except Exception:
        pass


def extract_stills(clip: Path, dest_dir: Path, tag: str) -> list[Path]:
    dest_dir.mkdir(parents=True, exist_ok=True)
    out: list[Path] = []
    for i, t in enumerate([0.3, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 7.6]):
        p = dest_dir / f"{tag}_t{i}.jpg"
        subprocess.run(
            [
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-ss", f"{t:.2f}", "-i", str(clip),
                "-frames:v", "1", "-q:v", "2", str(p),
            ],
            check=True,
        )
        out.append(p)
    return out


def chair_top_flame_suspect(still: Path) -> dict:
    im = Image.open(still).convert("RGB")
    w, h = im.size
    pix = im.load()
    x0, x1 = int(w * 0.40), int(w * 0.60)
    y0, y1 = int(h * 0.12), int(h * 0.28)
    hot = 0
    n = 0
    for y in range(y0, y1, 2):
        for x in range(x0, x1, 2):
            n += 1
            r, g, b = pix[x, y]
            if r >= 200 and g >= 110 and b <= 115 and (r - b) >= 95:
                hot += 1
            elif r >= 230 and g >= 170 and b <= 140 and (r - b) >= 80:
                hot += 1
    hot_pct = 100.0 * hot / max(n, 1)

    px0, px1 = int(w * 0.42), int(w * 0.58)
    py0, py1 = int(h * 0.30), int(h * 0.52)
    panel_hot = 0
    pn = 0
    for y in range(py0, py1, 2):
        for x in range(px0, px1, 2):
            pn += 1
            r, g, b = pix[x, y]
            if r >= 245 and g >= 230 and b <= 150 and (r - b) >= 100:
                panel_hot += 1
    panel_hot_pct = 100.0 * panel_hot / max(pn, 1)

    smoke = 0
    sn = 0
    for y in range(int(h * 0.05), int(h * 0.45), 2):
        for x in range(int(w * 0.12), int(w * 0.50), 2):
            sn += 1
            r, g, b = pix[x, y]
            avg = (r + g + b) / 3.0
            sat = max(r, g, b) - min(r, g, b)
            if 145 <= avg <= 235 and sat <= 28:
                smoke += 1
    smoke_pct = 100.0 * smoke / max(sn, 1)
    fire = hot_pct >= 0.85 or panel_hot_pct >= 2.0
    return {
        "still": str(still),
        "chair_top_hot_pct": round(hot_pct, 3),
        "panel_hot_pct": round(panel_hot_pct, 3),
        "smoke_pct": round(smoke_pct, 3),
        "fire": fire,
        "smoke": smoke_pct >= 2.8,
        "reject": bool(fire or smoke_pct >= 2.8),
    }


def qa_clip(clip: Path, tag: str) -> dict:
    stills = extract_stills(clip, QA, tag)
    scores = [chair_top_flame_suspect(p) for p in stills]
    bad = [s for s in scores if s["reject"]]
    report = {
        "tag": tag,
        "clip": str(clip),
        "scores": scores,
        "bad_frame_count": len(bad),
        "reject": len(bad) >= 2,
        "stills": [str(p) for p in stills],
    }
    (QA / f"{tag}_flame_check.json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"  flame-check {tag}: bad={len(bad)}/9 reject={report['reject']}", flush=True)
    return report


def pick_google_account(page) -> None:
    url = page.url or ""
    if "accounts.google.com" not in url:
        return
    for needle in (REQUIRED_FLOW_EMAIL, "benoats@gmail.com"):
        loc = page.get_by_text(needle, exact=False)
        if loc.count():
            print(f"  account chooser → {needle}", flush=True)
            loc.first.click(timeout=8000)
            page.wait_for_timeout(7000)
            return
    raise SystemExit(
        f"BLOCKED_AUTH: account chooser open but {REQUIRED_FLOW_EMAIL} not listed."
    )


def require_flow_account(page) -> str:
    try:
        labels = page.eval_on_selector_all(
            "button, a, [role=button]",
            "els => els.map(e => (e.innerText||e.textContent||'').trim()).filter(Boolean)",
        )
    except Exception:
        labels = []
    blob = " | ".join(labels[:120]).lower()
    if "benoats86" in blob:
        raise SystemExit(f"BLOCKED_AUTH: forbidden account {FORBIDDEN_FLOW_EMAIL}")
    for email in ALLOWED_FLOW_EMAILS:
        if email.lower() in blob:
            return email
    return REQUIRED_FLOW_EMAIL


def open_flow(p):
    last_err = "not started"
    for attempt in range(1, 4):
        ctx, page = flow.launch_context(p, headed=True, profile=PROFILE)
        try:
            page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
            page.wait_for_timeout(3500)
            pick_google_account(page)
            flow.dismiss_banners(page)
            page.wait_for_timeout(1500)
            active = require_flow_account(page)
            print(f"  AUTH OK minting as {active} via {flow.FLOW_HOME}", flush=True)
            return ctx, page, active
        except SystemExit:
            safe_close(ctx)
            raise
        except Exception as exc:
            last_err = str(exc)
            safe_close(ctx)
            print(f"  open_flow retry {attempt}/3: {last_err}", flush=True)
            time.sleep(2)
    raise SystemExit(f"BLOCKED_AUTH: Flow not logged in ({last_err})")


def run_harvest(dest: Path, project_url: str) -> None:
    project_url = (project_url or "").split("?")[0].rstrip("/")
    env = dict(os.environ)
    env["ORBIT_FLOW_HOME"] = flow.FLOW_HOME
    env["ORBIT_FLOW_PROFILE"] = str(PROFILE)
    cmd = [
        sys.executable, "-u", str(HARVEST),
        "--project", project_url, "--out", str(dest),
    ]
    print(f"  harvest: {' '.join(cmd)}", flush=True)
    subprocess.check_call(cmd, env=env)


def run_force_download(dest: Path, project_url: str) -> None:
    project_url = (project_url or "").split("?")[0].rstrip("/")
    env = dict(os.environ)
    env["ORBIT_FLOW_HOME"] = flow.FLOW_HOME
    env["ORBIT_FLOW_PROFILE"] = str(PROFILE)
    cmd = [
        sys.executable, "-u", str(FORCE_DL),
        "--project", project_url, "--dest", str(dest),
    ]
    print(f"  force-dl: {' '.join(cmd)}", flush=True)
    subprocess.check_call(cmd, env=env)


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    REJECTED.mkdir(parents=True, exist_ok=True)
    QA.mkdir(parents=True, exist_ok=True)

    if not PARENT_V13.exists():
        raise SystemExit(f"missing parent v13 {PARENT_V13}")
    got = sha256(PARENT_V13)
    if got != PARENT_V13_SHA:
        raise SystemExit(f"STOP: v13 sha mismatch want {PARENT_V13_SHA} got {got}")
    print(f"parent v13 sha OK {got}", flush=True)

    if not START.exists() or START.stat().st_size < 20_000:
        raise SystemExit(f"STOP: missing clean start {START}")
    start_check = chair_top_flame_suspect(START)
    (QA / "start_09b_v14_flame_check.json").write_text(
        json.dumps(start_check, indent=2) + "\n"
    )
    if start_check["reject"]:
        raise SystemExit(f"STOP: start frame still flame-hot: {start_check}")
    print(
        f"start OK {START.name} top_hot={start_check['chair_top_hot_pct']}",
        flush=True,
    )

    dest = RAW / f"{PID}_v14.mp4"
    meta: dict = {
        "parent_v13_sha256": PARENT_V13_SHA,
        "plate": PID,
        "uat_named_plate": "10_family_before_weight",
        "timeline_note": (
            "UAT fail ~105s under FAMILY FIRST label is plate09b window "
            "98.15–106.05; plate 10 floating-cards starts ~105.7"
        ),
        "start_frame": str(START),
        "flow_account": REQUIRED_FLOW_EMAIL,
        "prompt": PROMPT,
        "tries": [],
        "status": "running",
    }
    META.write_text(json.dumps(meta, indent=2) + "\n")

    with sync_playwright() as p:
        ctx, page, active = open_flow(p)
        meta["active_account"] = active
        META.write_text(json.dumps(meta, indent=2) + "\n")
        accepted = False
        try:
            for create_n in range(1, MAX_CREATES + 1):
                print(
                    f"\n=== v14 I2V {PID} Create {create_n}/{MAX_CREATES} ===",
                    flush=True,
                )
                tmp = dest.with_suffix(f".try{create_n}.tmp.mp4")
                tmp.unlink(missing_ok=True)
                try:
                    info = flow.generate_clip(
                        page,
                        PROMPT,
                        tmp,
                        model=MODEL,
                        start_frame=START,
                        scenery_only=False,
                        reuse_project=False,
                        attempts=1,
                        timeout_s=900,
                    )
                except Exception as e:
                    print(f"  create failed: {e}", flush=True)
                    meta["tries"].append(
                        {"create": create_n, "status": "fail", "error": str(e)[:500]}
                    )
                    META.write_text(json.dumps(meta, indent=2) + "\n")
                    try:
                        _ = page.url
                    except Exception:
                        safe_close(ctx)
                        ctx, page, active = open_flow(p)
                    continue

                if info.get("needs_gallery_harvest") or (
                    (not tmp.exists() or tmp.stat().st_size < 400_000)
                    and (info.get("project_url") or info.get("url"))
                ):
                    project_url = (
                        info.get("project_url")
                        or info.get("url")
                        or (page.url or "")
                    )
                    project_url = project_url.split("?")[0].rstrip("/")
                    print(f"  harvest from {project_url}", flush=True)
                    safe_close(ctx)
                    try:
                        run_harvest(tmp, project_url)
                    except Exception as harvest_err:
                        print(f"  harvest failed: {harvest_err}", flush=True)
                        try:
                            run_force_download(tmp, project_url)
                        except Exception as force_err:
                            print(f"  force-dl failed: {force_err}", flush=True)
                    ctx, page, active = open_flow(p)

                if not tmp.exists() or tmp.stat().st_size < 400_000:
                    print("  no usable clip bytes", flush=True)
                    meta["tries"].append(
                        {
                            "create": create_n,
                            "status": "empty",
                            "info": str(info)[:500],
                        }
                    )
                    META.write_text(json.dumps(meta, indent=2) + "\n")
                    continue

                tag = f"{PID}_try{create_n}"
                report = qa_clip(tmp, tag)
                meta["tries"].append(
                    {
                        "create": create_n,
                        "status": "reject" if report["reject"] else "accept",
                        "bytes": tmp.stat().st_size,
                        "sha256": sha256(tmp),
                        "qa": {
                            "bad_frame_count": report["bad_frame_count"],
                            "reject": report["reject"],
                        },
                    }
                )
                META.write_text(json.dumps(meta, indent=2) + "\n")
                if report["reject"]:
                    rej = REJECTED / f"{PID}_v14_try{create_n}_flame.mp4"
                    shutil.move(str(tmp), str(rej))
                    print(f"  REJECT → {rej.name}", flush=True)
                    continue

                shutil.move(str(tmp), str(dest))
                meta["status"] = "accepted"
                meta["out"] = str(dest)
                meta["sha256"] = sha256(dest)
                META.write_text(json.dumps(meta, indent=2) + "\n")
                print(f"ACCEPTED {dest} sha={meta['sha256']}", flush=True)
                accepted = True
                break
        finally:
            safe_close(ctx)

    if not accepted:
        meta["status"] = "failed"
        META.write_text(json.dumps(meta, indent=2) + "\n")
        raise SystemExit("STOP: no accepted clean-glow 09b take")


if __name__ == "__main__":
    main()
