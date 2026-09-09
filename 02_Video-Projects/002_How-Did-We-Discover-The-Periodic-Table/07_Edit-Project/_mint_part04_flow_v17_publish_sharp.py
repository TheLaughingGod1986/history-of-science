#!/usr/bin/env python3
"""Part 04 Flow remint v17 — PUBLISH THE GAPS sharp (11 / 11b only).

Parent KEEP: hos_002_part04_rough_v16.mp4
  sha256 7e083fc440879209bbc69459fbaf21dc29dbfc1f77b370ec92ee931bec82cb3c

Remint ONLY: 11_publish_gaps, 11b_wait_and_hunt
KEEP: 10_family_before_weight, Explorer 06, 09/09b CLEAN LIGHT, written cards ~40

Do NOT restore ghosty v01 DNA. Fresh I2V from painted sharp v17 starts.
Flow: benoats@googlemail.com on /u/1/. Scores → CoS. No PASS. No Ben ping.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

from PIL import Image, ImageFilter
from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))
import orbit_flow_veo_ui as flow  # noqa: E402
import orbit_gemini_veo as veo  # noqa: E402

flow.FLOW_HOME = os.environ.get("ORBIT_FLOW_HOME", "https://flow.google.com/u/1/")

PROJ = Path(__file__).resolve().parents[1]
RAW = PROJ / "04_Generated-Clips/part04/raw/v17_fast"
REJECTED = RAW / "_rejected"
QA = PROJ / "07_Edit-Project/_qa_part04_v17_flow"
META = PROJ / "07_Edit-Project/part04_mint_flow_v17_meta.json"
HARVEST = Path(__file__).resolve().parent / "_harvest_newest_gallery_v01.py"
FORCE_DL = Path(__file__).resolve().parent / "_harvest_force_download_v04.py"
EDIT_DL = Path(__file__).resolve().parent / "_harvest_part04_v11_edit_download.py"
STARTS = PROJ / "04_Generated-Clips/part04/refs/v17_start_frames"

MODEL = os.environ.get("ORBIT_FLOW_VEO_MODEL", "Veo 3.1 - Fast")
PROFILE = Path(os.environ.get("ORBIT_FLOW_PROFILE", str(Path.home() / ".playwright-hos-flow-profile")))
REQUIRED_FLOW_EMAIL = "benoats@googlemail.com"
ALLOWED_FLOW_EMAILS = {REQUIRED_FLOW_EMAIL, "benoats@gmail.com"}
FORBIDDEN_FLOW_EMAIL = "benoats86@gmail.com"
MAX_CREATES = int(os.environ.get("HOS_V17_MAX_CREATES", "3"))
HARVEST_WAIT_S = int(os.environ.get("HOS_FLOW_HARVEST_WAIT_S", "420"))

PARENT_V16 = PROJ / "09_Final-Export/hos_002_part04_rough_v16.mp4"
PARENT_V16_SHA = "7e083fc440879209bbc69459fbaf21dc29dbfc1f77b370ec92ee931bec82cb3c"

STYLE = (
    "Animistry-class stylised 3D cartoon (NOT photoreal). "
    "ONE continuous 1869 chemist desk at night: honey wood desktop, soft warm lamp, "
    "flat parchment grid sheet, coloured flasks, magnifier, cream cards. "
    "Continuous real camera/object motion the whole clip. Silent. No Orbit. No Ken Burns still."
)

CLEAN_LIGHT_LOCK = (
    "CLEAN LIGHT LOCK: soft warm desk-lamp glow ONLY — clean air under the bulb. "
    "HARD REJECT: lava drip, molten orange leak, sparks, smoke, candle flame, open fire. "
    "Empty-Chairs = soft rectangular panel glow ONLY — never flames."
)

SHARP_LOCK = (
    "LATE SHOTS SHARP LOCK (HARD): every frame finished and crisp SINGLE EXPOSURE. "
    "ZERO ghost doubles, ZERO double-exposure edges, ZERO motion-ghost trailing props, "
    "ZERO unfinished left-half pixelation / blocky mush. "
    "ONE solid lamp, ONE solid flask set, ONE solid grid — never blended layers. "
    "Prefer gentle slow settle over fast spins that smear."
)

REJECT = (
    "HARD REJECT: ghost doubles; double-exposure; unfinished left-half pixel mush; "
    "lava/molten lamp leak; chair-top flame; smoke; photoreal; Orbit; twins; hat."
)

PROMPTS = {
    "11_publish_gaps": (
        "Image-to-video from the attached start frame. Same 1869 night desk DNA. "
        "PUBLISH THE GAPS beat: sharp finished desk with flat grid sheet, flasks, cards, "
        "magnifier. Every prop SINGLE sharp edges — never full-scene ghost doubles. "
        "Left half fully finished/sharp — never pixelated unfinished mush. "
        f"{CLEAN_LIGHT_LOCK} {SHARP_LOCK} "
        "No Explorer. Continuous subtle settle / tiny camera drift. Silent. "
        + REJECT + " " + STYLE
    ),
    "11b_wait_and_hunt": (
        "Image-to-video from the attached start frame. Same 1869 night desk DNA. "
        "Wait-and-hunt beat: published flat grid with empty circular holes, flasks, soft lamp. "
        "Whole frame finished and sharp — zero left-half pixel mush, zero ghost doubles. "
        f"{CLEAN_LIGHT_LOCK} {SHARP_LOCK} "
        "No Explorer. Continuous subtle hold/push-in. Silent. "
        + REJECT + " " + STYLE
    ),
}

START_FILES = {
    "11_publish_gaps": STARTS / "11_publish_gaps_start_v17.jpg",
    "11b_wait_and_hunt": STARTS / "11b_wait_and_hunt_start_v17.jpg",
}


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


def lava_suspect(still: Path) -> dict:
    im = Image.open(still).convert("RGB")
    w, h = im.size
    px = im.load()
    hot = 0
    n = 0
    for y in range(int(h * 0.10), int(h * 0.65), 2):
        for x in range(int(w * 0.02), int(w * 0.45), 2):
            n += 1
            r, g, b = px[x, y]
            if r >= 200 and g >= 90 and b <= 90 and (r - b) >= 110:
                hot += 1
            elif r >= 230 and g >= 140 and b <= 110 and (r - b) >= 100:
                hot += 1
    pct = 100.0 * hot / max(n, 1)
    return {"still": str(still), "lava_pct": round(pct, 3), "reject": pct >= 1.2}


def blur_suspect(still: Path) -> dict:
    im = Image.open(still).convert("L")
    w, h = im.size
    right = im.crop((int(w * 0.55), int(h * 0.25), int(w * 0.95), int(h * 0.85)))
    edges = right.filter(ImageFilter.FIND_EDGES)
    stats = list(edges.getdata())
    mean = sum(stats) / max(len(stats), 1)
    return {"still": str(still), "edge_mean": round(mean, 2), "reject": mean < 6.5}


def left_mush_suspect(still: Path) -> dict:
    im = Image.open(still).convert("RGB")
    w, h = im.size
    px = im.load()
    mush = 0
    n = 0
    for y in range(int(h * 0.08), int(h * 0.85), 2):
        for x in range(0, int(w * 0.28), 2):
            n += 1
            r, g, b = px[x, y]
            if r > 235 and g > 235 and b > 230:
                mush += 1
            elif abs(r - g) > 80 and abs(r - b) > 80 and max(r, g, b) > 190:
                mush += 1
    pct = 100.0 * mush / max(n, 1)
    return {"still": str(still), "mush_pct": round(pct, 3), "reject": pct >= 4.5}


def ghost_suspect(still: Path) -> dict:
    im = Image.open(still).convert("L")
    w, h = im.size
    band = im.crop((int(w * 0.15), int(h * 0.35), int(w * 0.85), int(h * 0.75)))
    bw, bh = band.size
    shift = 6
    a = band.crop((0, 0, bw - shift, bh))
    b = band.crop((shift, 0, bw, bh))
    pa, pb = list(a.getdata()), list(b.getdata())
    diffs = [abs(pa[i] - pb[i]) for i in range(len(pa))]
    mean = sum(diffs) / max(len(diffs), 1)
    return {"still": str(still), "shift_mean": round(mean, 2), "reject": mean >= 42.0}


def qa_clip(clip: Path, tag: str) -> dict:
    qdir = QA / tag
    qdir.mkdir(parents=True, exist_ok=True)
    stills = []
    for i, t in enumerate([0.4, 1.5, 3.0, 4.5, 6.0, 7.4]):
        sp = qdir / f"t{i}.jpg"
        subprocess.run(
            [
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-ss", f"{t}", "-i", str(clip), "-frames:v", "1", str(sp),
            ],
            check=True,
        )
        stills.append(sp)
    lava = [lava_suspect(s) for s in stills]
    blur = [blur_suspect(s) for s in stills]
    mush = [left_mush_suspect(s) for s in stills]
    ghost = [ghost_suspect(s) for s in stills]
    report = {
        "tag": tag,
        "clip": str(clip),
        "lava_rejects": sum(1 for x in lava if x["reject"]),
        "blur_rejects": sum(1 for x in blur if x["reject"]),
        "mush_rejects": sum(1 for x in mush if x["reject"]),
        "ghost_rejects": sum(1 for x in ghost if x["reject"]),
        "lava": lava,
        "blur": blur,
        "mush": mush,
        "ghost": ghost,
    }
    report["reject"] = (
        report["lava_rejects"] >= 2
        or report["blur_rejects"] >= 3
        or report["mush_rejects"] >= 2
        or report["ghost_rejects"] >= 3
    )
    (qdir / "qa.json").write_text(json.dumps(report, indent=2) + "\n")
    print(
        f"  QA {tag}: lava={report['lava_rejects']} blur={report['blur_rejects']} "
        f"mush={report['mush_rejects']} ghost={report['ghost_rejects']} "
        f"reject={report['reject']}",
        flush=True,
    )
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
    raise SystemExit(f"BLOCKED_AUTH: account chooser open but {REQUIRED_FLOW_EMAIL} not listed.")


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


def accept_mp4(path: Path) -> bool:
    if not path.exists() or path.stat().st_size < 400_000:
        return False
    raw = path.read_bytes()[:64]
    if raw[:3] == b"\xff\xd8\xff" or b"ftyp" not in raw:
        return False
    try:
        veo.strip_audio(path)
    except Exception:
        pass
    return True


def run_harvest(dest: Path, project_url: str, before_thumbs: int = -1) -> bool:
    project_url = (project_url or "").split("?")[0].rstrip("/")
    env = dict(os.environ)
    env["ORBIT_FLOW_HOME"] = flow.FLOW_HOME
    env["ORBIT_FLOW_PROFILE"] = str(PROFILE)
    env["HOS_FLOW_HARVEST_WAIT_S"] = str(HARVEST_WAIT_S)
    cmd = [
        sys.executable, "-u", str(HARVEST),
        "--project", project_url,
        "--out", str(dest),
        "--wait-s", str(HARVEST_WAIT_S),
        "--before-thumbs", str(before_thumbs),
    ]
    print(f"  harvest: {' '.join(cmd)}", flush=True)
    try:
        subprocess.check_call(cmd, env=env)
    except Exception as e:
        print(f"  harvest failed: {e}", flush=True)
        return accept_mp4(dest)
    return accept_mp4(dest)


def run_force_download(dest: Path, project_url: str) -> bool:
    project_url = (project_url or "").split("?")[0].rstrip("/")
    env = dict(os.environ)
    env["ORBIT_FLOW_HOME"] = flow.FLOW_HOME
    env["ORBIT_FLOW_PROFILE"] = str(PROFILE)
    cmd = [sys.executable, "-u", str(FORCE_DL), "--project", project_url, "--dest", str(dest)]
    print(f"  force-dl: {' '.join(cmd)}", flush=True)
    try:
        subprocess.check_call(cmd, env=env)
    except Exception as e:
        print(f"  force-dl failed: {e}", flush=True)
        return accept_mp4(dest)
    return accept_mp4(dest)


def run_edit_download(dest: Path, project_url: str) -> bool:
    project_url = (project_url or "").split("?")[0].rstrip("/")
    env = dict(os.environ)
    env["ORBIT_FLOW_HOME"] = flow.FLOW_HOME
    env["ORBIT_FLOW_PROFILE"] = str(PROFILE)
    cmd = [
        sys.executable, "-u", str(EDIT_DL),
        "--project", project_url,
        "--edit", "",
        "--dest", str(dest),
    ]
    print(f"  edit-dl: {' '.join(cmd)}", flush=True)
    try:
        subprocess.check_call(cmd, env=env)
    except Exception as e:
        print(f"  edit-dl failed: {e}", flush=True)
        return accept_mp4(dest)
    return accept_mp4(dest)


def count_thumbs(page) -> int:
    try:
        return len(flow.collect_gallery_asb_srcs(page))
    except Exception:
        return -1


def mint_plate(page, ctx, pid: str, meta: dict):
    start = START_FILES[pid]
    if not start.exists():
        raise SystemExit(f"missing start {start}")
    dest = RAW / f"{pid}_v17.mp4"
    prompt = PROMPTS[pid]
    for create_n in range(1, MAX_CREATES + 1):
        print(f"\n=== v17 I2V {pid} Create {create_n}/{MAX_CREATES} ===", flush=True)
        tmp = dest.with_suffix(f".try{create_n}.tmp.mp4")
        tmp.unlink(missing_ok=True)
        before = count_thumbs(page)
        try:
            info = flow.generate_clip(
                page,
                prompt,
                tmp,
                model=MODEL,
                start_frame=start,
                scenery_only=False,
                reuse_project=False,
                attempts=1,
                timeout_s=900,
            )
        except Exception as e:
            print(f"  create failed: {e}", flush=True)
            meta.setdefault("tries", {}).setdefault(pid, []).append(
                {"create": create_n, "status": "fail", "error": str(e)[:500]}
            )
            META.write_text(json.dumps(meta, indent=2) + "\n")
            err = str(e).lower()
            if "credit" in err or "quota" in err or "limit" in err or "exhausted" in err:
                meta["credit_blocker"] = str(e)[:800]
                META.write_text(json.dumps(meta, indent=2) + "\n")
                return "credit_block", None
            try:
                _ = page.url
            except Exception:
                safe_close(ctx)
                return "reopen", None
            continue

        project_url = info.get("project_url") or info.get("url") or (page.url or "")
        project_url = project_url.split("?")[0].rstrip("/")
        meta.setdefault("projects", {})[f"{pid}_try{create_n}"] = project_url
        META.write_text(json.dumps(meta, indent=2) + "\n")

        got = accept_mp4(tmp)
        if not got and (
            info.get("needs_gallery_harvest")
            or (not tmp.exists() or tmp.stat().st_size < 400_000)
        ):
            print(f"  careful harvest from {project_url} (before_thumbs={before})", flush=True)
            safe_close(ctx)
            # wait for gallery mp4 — poll harvest → force → edit download
            if run_harvest(tmp, project_url, before_thumbs=max(before, 0)):
                got = True
            elif run_force_download(tmp, project_url):
                got = True
            elif run_edit_download(tmp, project_url):
                got = True
            return "reopen", None if not got else ("ok_pending", tmp, pid, create_n)

        if not got:
            print("  empty download", flush=True)
            continue

        report = qa_clip(tmp, f"{pid}_try{create_n}")
        meta.setdefault("tries", {}).setdefault(pid, []).append(
            {"create": create_n, "status": "qa", "reject": report["reject"], "qa": report,
             "project_url": project_url}
        )
        META.write_text(json.dumps(meta, indent=2) + "\n")
        if report["reject"]:
            REJECTED.mkdir(parents=True, exist_ok=True)
            bad = REJECTED / f"{pid}_v17_try{create_n}_reject.mp4"
            shutil.move(str(tmp), str(bad))
            print(f"  REJECT → {bad.name}", flush=True)
            continue
        shutil.move(str(tmp), str(dest))
        print(f"  ACCEPT {dest.name} sha={sha256(dest)[:16]}…", flush=True)
        return "ok", dest
    return "exhausted", None


def finalize_pending(tmp: Path, pid: str, create_n: int, meta: dict):
    dest = RAW / f"{pid}_v17.mp4"
    if not accept_mp4(tmp):
        return False
    report = qa_clip(tmp, f"{pid}_try{create_n}")
    meta.setdefault("tries", {}).setdefault(pid, []).append(
        {"create": create_n, "status": "qa_after_harvest", "reject": report["reject"], "qa": report}
    )
    META.write_text(json.dumps(meta, indent=2) + "\n")
    if report["reject"]:
        REJECTED.mkdir(parents=True, exist_ok=True)
        bad = REJECTED / f"{pid}_v17_try{create_n}_reject.mp4"
        shutil.move(str(tmp), str(bad))
        print(f"  REJECT → {bad.name}", flush=True)
        return False
    shutil.move(str(tmp), str(dest))
    print(f"  ACCEPT {dest.name} sha={sha256(dest)[:16]}…", flush=True)
    meta["accepted"][pid] = {
        "path": str(dest),
        "sha256": sha256(dest),
        "bytes": dest.stat().st_size,
    }
    META.write_text(json.dumps(meta, indent=2) + "\n")
    return True


def main() -> None:
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--plates",
        nargs="*",
        default=["11_publish_gaps", "11b_wait_and_hunt"],
    )
    args = ap.parse_args()

    RAW.mkdir(parents=True, exist_ok=True)
    REJECTED.mkdir(parents=True, exist_ok=True)
    QA.mkdir(parents=True, exist_ok=True)

    if not PARENT_V16.exists():
        raise SystemExit(f"missing parent v16 {PARENT_V16}")
    got = sha256(PARENT_V16)
    if got != PARENT_V16_SHA:
        raise SystemExit(f"STOP: v16 sha mismatch want {PARENT_V16_SHA} got {got}")
    print(f"parent v16 sha OK {got}", flush=True)

    for pid in args.plates:
        if not START_FILES[pid].exists():
            raise SystemExit(f"missing start frame {START_FILES[pid]} — run prep first")

    meta = {
        "parent_v16_sha256": PARENT_V16_SHA,
        "bible_main": "25bdefd",
        "flow_account": REQUIRED_FLOW_EMAIL,
        "model": MODEL,
        "plates": args.plates,
        "tries": {},
        "accepted": {},
        "projects": {},
        "status": "running",
        "method": "fresh Flow Veo I2V from painted sharp starts — NOT v01 restore",
    }
    META.write_text(json.dumps(meta, indent=2) + "\n")

    with sync_playwright() as p:
        ctx, page, active = open_flow(p)
        meta["active_account"] = active
        META.write_text(json.dumps(meta, indent=2) + "\n")
        try:
            for pid in args.plates:
                dest = RAW / f"{pid}_v17.mp4"
                if dest.exists() and dest.stat().st_size >= 400_000 and os.environ.get("HOS_V17_SKIP_EXISTING") == "1":
                    print(f"SKIP existing {dest.name}", flush=True)
                    meta["accepted"][pid] = {
                        "path": str(dest),
                        "sha256": sha256(dest),
                        "bytes": dest.stat().st_size,
                        "skipped_existing": True,
                    }
                    META.write_text(json.dumps(meta, indent=2) + "\n")
                    continue
                while True:
                    status, payload = mint_plate(page, ctx, pid, meta)
                    if status == "reopen":
                        # payload may be pending harvest result tuple
                        if isinstance(payload, tuple) and payload and payload[0] == "ok_pending":
                            _, tmp, ppid, create_n = payload
                            if finalize_pending(tmp, ppid, create_n, meta):
                                break
                        ctx, page, active = open_flow(p)
                        meta["active_account"] = active
                        dest = RAW / f"{pid}_v17.mp4"
                        if dest.exists() and dest.stat().st_size >= 400_000:
                            meta["accepted"][pid] = {
                                "path": str(dest),
                                "sha256": sha256(dest),
                                "bytes": dest.stat().st_size,
                            }
                            META.write_text(json.dumps(meta, indent=2) + "\n")
                            break
                        # retry harvest on last project if still empty
                        last_proj = None
                        for k, v in meta.get("projects", {}).items():
                            if k.startswith(pid):
                                last_proj = v
                        if last_proj:
                            tmp = dest.with_suffix(".harvest_retry.tmp.mp4")
                            if (
                                run_harvest(tmp, last_proj)
                                or run_force_download(tmp, last_proj)
                                or run_edit_download(tmp, last_proj)
                            ):
                                if finalize_pending(tmp, pid, 99, meta):
                                    break
                        # continue create attempts on reopened session
                        continue
                    if status == "credit_block":
                        print("CREDIT BLOCKER — stop mint", flush=True)
                        meta["status"] = "credit_blocked"
                        META.write_text(json.dumps(meta, indent=2) + "\n")
                        return
                    if status == "ok" and payload is not None:
                        meta["accepted"][pid] = {
                            "path": str(payload),
                            "sha256": sha256(payload),
                            "bytes": payload.stat().st_size,
                        }
                        META.write_text(json.dumps(meta, indent=2) + "\n")
                    else:
                        print(f"  GIVE UP {pid}", flush=True)
                    break
        finally:
            safe_close(ctx)

    meta["status"] = "done"
    META.write_text(json.dumps(meta, indent=2) + "\n")
    print("MINT DONE", json.dumps(meta.get("accepted", {}), indent=2), flush=True)
    missing = [p for p in args.plates if p not in meta.get("accepted", {})]
    if missing:
        print(f"MISSING plates: {missing}", flush=True)
        raise SystemExit(3)


if __name__ == "__main__":
    main()
