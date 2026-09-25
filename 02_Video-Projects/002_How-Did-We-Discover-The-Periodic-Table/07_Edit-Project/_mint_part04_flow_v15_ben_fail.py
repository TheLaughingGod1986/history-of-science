#!/usr/bin/env python3
"""Part 04 Flow remint v15 — Ben FAIL (Explorer hair + CLEAN LIGHT + sharp late desks).

Parent FAIL: hos_002_part04_rough_v14.mp4
  sha256 fa62ab22d0f7cbd4f208e5200c9b8b471c23595237b4d7d2dd18e6f47dabad4f

Remint plates: 06_explorer_leaves_gap, 10_family_before_weight,
               11_publish_gaps, 11b_wait_and_hunt
(09b uses lamplock composite unless --also-09b)

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

from PIL import Image, ImageDraw, ImageFilter
from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))
import orbit_flow_veo_ui as flow  # noqa: E402

flow.FLOW_HOME = os.environ.get("ORBIT_FLOW_HOME", "https://flow.google.com/u/1/")

PROJ = Path(__file__).resolve().parents[1]
RAW = PROJ / "04_Generated-Clips/part04/raw/v15_fast"
REJECTED = RAW / "_rejected"
QA = PROJ / "07_Edit-Project/_qa_part04_v15_flow"
META = PROJ / "07_Edit-Project/part04_mint_flow_v15_meta.json"
HARVEST = Path(__file__).resolve().parent / "_harvest_newest_gallery_v01.py"
FORCE_DL = Path(__file__).resolve().parent / "_harvest_force_download_v01.py"
STARTS = PROJ / "04_Generated-Clips/part04/refs/v15_start_frames"

MODEL = os.environ.get("ORBIT_FLOW_VEO_MODEL", "Veo 3.1 - Fast")
PROFILE = Path(os.environ.get("ORBIT_FLOW_PROFILE", str(Path.home() / ".playwright-hos-flow-profile")))
REQUIRED_FLOW_EMAIL = "benoats@googlemail.com"
ALLOWED_FLOW_EMAILS = {REQUIRED_FLOW_EMAIL, "benoats@gmail.com"}
FORBIDDEN_FLOW_EMAIL = "benoats86@gmail.com"
MAX_CREATES = int(os.environ.get("HOS_V15_MAX_CREATES", "3"))

PARENT_V14 = PROJ / "09_Final-Export/hos_002_part04_rough_v14.mp4"
PARENT_V14_SHA = "fa62ab22d0f7cbd4f208e5200c9b8b471c23595237b4d7d2dd18e6f47dabad4f"

STYLE = (
    "Animistry-class stylised 3D cartoon (NOT photoreal). "
    "ONE continuous 1869 chemist desk: honey wood desktop, soft warm lamp, cream "
    "element cards with readable ink letters/symbols (H/C/O/N/Li — NEVER blank), "
    "leather books. Continuous real camera/object motion the whole clip. Silent. "
    "No Orbit. No Ken Burns still."
)

HAIR_LOCK = (
    "EXPLORER HAIR LOCK (match History of Science character sheet EXACTLY): FULL dense "
    "finished messy wavy chestnut-brown crown covering the ENTIRE top of the head — "
    "thick tufts readable from behind and three-quarter back. ZERO unfinished mid-scalp "
    "hole, ZERO bald patch, ZERO tonsure, ZERO monk ring, ZERO shiny bare scalp, ZERO "
    "flat untextured crown crater. Hair must look finished and sculpted like the sheet."
)

CLEAN_LIGHT_LOCK = (
    "CLEAN LIGHT LOCK: soft warm desk-lamp glow ONLY — clean air under the bulb. "
    "HARD REJECT: lava drip, molten orange leak under lamp, orange fire drip onto chair "
    "or desk, sparks, smoke, candle flame, any open fire. Empty-Chairs = soft rectangular "
    "panel glow on chair back ONLY — never flames."
)

SHARP_LOCK = (
    "SHARP FINISHED DESK LOCK: crisp readable props, books, flasks, cards. "
    "HARD REJECT: heavy motion blur, ghost doubles, unfinished mush, smeared right-side books."
)

WRITTEN_CARDS = (
    "WRITTEN CARDS LOCK: every visible element card shows readable hand-ink H/C/O/N/Li "
    "with small numbers. HARD REJECT blank cream cards."
)

KEEP = (
    "KEEP: round gold/wire glasses, fair warm-tan skin, dark teal coat, bare head (no hat), "
    "indoor wood bookcase study."
)

REJECT = (
    "HARD REJECT: unfinished/bald crown; lava/molten lamp leak; chair-top flame; smoke; "
    "heavy blur/ghost doubles; blank cards; photoreal; Orbit; twins; hat; exterior sky."
)

PROMPTS = {
    "06_explorer_leaves_gap": (
        "Image-to-video from the attached start frame. Same 1869 chemist desk DNA. "
        "Exactly ONE Explorer boy from behind / three-quarter BACK — profile/back garnish. "
        f"{HAIR_LOCK} Round gold glasses readable at temple. Dark teal coat. Fair warm-tan skin. "
        "He places or leaves a WRITTEN cream element card, leaving a glowing vacant gap. "
        f"{CLEAN_LIGHT_LOCK} {WRITTEN_CARDS} {SHARP_LOCK} {KEEP} "
        "Continuous subtle motion. Fully indoor wood/bookcase. Silent. "
        + REJECT + " " + STYLE
    ),
    "10_family_before_weight": (
        "Image-to-video from the attached start frame. Same 1869 desk DNA. "
        "WRITTEN cream family cards settle / float gently over honey wood. Empty chair with "
        "soft rectangular panel glow ONLY. "
        f"{CLEAN_LIGHT_LOCK} {WRITTEN_CARDS} {SHARP_LOCK} "
        "No Explorer. Continuous subtle motion. Indoor wood/bookcase. Silent. "
        + REJECT + " " + STYLE
    ),
    "11_publish_gaps": (
        "Image-to-video from the attached start frame. Same 1869 night desk DNA. "
        "Publish-the-gaps beat: sharp finished desk with grid board, flasks, cards. "
        f"{CLEAN_LIGHT_LOCK} {SHARP_LOCK} {WRITTEN_CARDS} "
        "No Explorer. Continuous subtle motion. Sharp props — never mushy ghost doubles. Silent. "
        + REJECT + " " + STYLE
    ),
    "11b_wait_and_hunt": (
        "Image-to-video from the attached start frame. Same 1869 night desk DNA. "
        "Wait-and-hunt beat: sharp finished desk, calm hold, readable cards/tools. "
        f"{CLEAN_LIGHT_LOCK} {SHARP_LOCK} {WRITTEN_CARDS} "
        "No Explorer. Continuous subtle motion. Silent. "
        + REJECT + " " + STYLE
    ),
    "09b_risk_hold": (
        "Image-to-video from the attached start frame. Same 1869 desk DNA. "
        "Empty wooden chair with soft rectangular backrest PANEL glow ONLY. "
        f"{CLEAN_LIGHT_LOCK} {WRITTEN_CARDS} {SHARP_LOCK} "
        "No Explorer. Continuous subtle hold. Indoor wood/bookcase. Silent. "
        + REJECT + " " + STYLE
    ),
}

START_FILES = {
    "06_explorer_leaves_gap": STARTS / "06_explorer_leaves_gap_start_v15.jpg",
    "10_family_before_weight": STARTS / "10_family_before_weight_start_v15.jpg",
    "11_publish_gaps": STARTS / "11_publish_gaps_start_v15.jpg",
    "11b_wait_and_hunt": STARTS / "11b_wait_and_hunt_start_v15.jpg",
    "09b_risk_hold": STARTS / "09b_risk_hold_start_v15_lamplock.jpg",
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


def hair_hole_suspect(still: Path) -> dict:
    im = Image.open(still).convert("RGB")
    w, h = im.size
    px = im.load()
    # Upper mid head band
    dark = 0
    hair = 0
    for y in range(int(h * 0.22), int(h * 0.40), 2):
        for x in range(int(w * 0.42), int(w * 0.62), 2):
            r, g, b = px[x, y]
            lum = (r + g + b) / 3
            if lum < 45 and r < 60:
                dark += 1
            if 55 < r < 170 and 30 < g < 120 and (r - b) > 18:
                hair += 1
    ratio = dark / max(hair, 1)
    return {
        "still": str(still),
        "dark": dark,
        "hair": hair,
        "dark_to_hair": round(ratio, 3),
        "reject": dark >= 80 and ratio >= 0.35,
    }


def blur_suspect(still: Path) -> dict:
    im = Image.open(still).convert("L")
    w, h = im.size
    right = im.crop((int(w * 0.55), int(h * 0.25), int(w * 0.95), int(h * 0.85)))
    # Laplacian-ish via emboss residual
    edges = right.filter(ImageFilter.FIND_EDGES)
    stats = list(edges.getdata())
    mean = sum(stats) / max(len(stats), 1)
    return {"still": str(still), "edge_mean": round(mean, 2), "reject": mean < 6.5}


def qa_clip(clip: Path, tag: str, *, check_hair: bool) -> dict:
    qdir = QA / tag
    qdir.mkdir(parents=True, exist_ok=True)
    stills = []
    for i, t in enumerate([0.4, 1.5, 3.0, 4.5, 6.0, 7.4]):
        sp = qdir / f"t{i}.jpg"
        subprocess.run(
            ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-ss", f"{t}", "-i", str(clip), "-frames:v", "1", str(sp)],
            check=True,
        )
        stills.append(sp)
    lava = [lava_suspect(s) for s in stills]
    blur = [blur_suspect(s) for s in stills]
    hair = [hair_hole_suspect(s) for s in stills] if check_hair else []
    report = {
        "tag": tag,
        "clip": str(clip),
        "lava_rejects": sum(1 for x in lava if x["reject"]),
        "blur_rejects": sum(1 for x in blur if x["reject"]),
        "hair_rejects": sum(1 for x in hair if x["reject"]),
        "lava": lava,
        "blur": blur,
        "hair": hair,
    }
    report["reject"] = (
        report["lava_rejects"] >= 2
        or report["blur_rejects"] >= 3
        or (check_hair and report["hair_rejects"] >= 2)
    )
    (qdir / "qa.json").write_text(json.dumps(report, indent=2) + "\n")
    print(
        f"  QA {tag}: lava={report['lava_rejects']} blur={report['blur_rejects']} "
        f"hair={report['hair_rejects']} reject={report['reject']}",
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


def run_harvest(dest: Path, project_url: str) -> None:
    project_url = (project_url or "").split("?")[0].rstrip("/")
    env = dict(os.environ)
    env["ORBIT_FLOW_HOME"] = flow.FLOW_HOME
    env["ORBIT_FLOW_PROFILE"] = str(PROFILE)
    cmd = [sys.executable, "-u", str(HARVEST), "--project", project_url, "--out", str(dest)]
    print(f"  harvest: {' '.join(cmd)}", flush=True)
    subprocess.check_call(cmd, env=env)


def run_force_download(dest: Path, project_url: str) -> None:
    project_url = (project_url or "").split("?")[0].rstrip("/")
    env = dict(os.environ)
    env["ORBIT_FLOW_HOME"] = flow.FLOW_HOME
    env["ORBIT_FLOW_PROFILE"] = str(PROFILE)
    cmd = [sys.executable, "-u", str(FORCE_DL), "--project", project_url, "--dest", str(dest)]
    print(f"  force-dl: {' '.join(cmd)}", flush=True)
    subprocess.check_call(cmd, env=env)


def mint_plate(page, ctx, pid: str, meta: dict):
    start = START_FILES[pid]
    if not start.exists():
        raise SystemExit(f"missing start {start}")
    dest = RAW / f"{pid}_v15.mp4"
    prompt = PROMPTS[pid]
    check_hair = pid == "06_explorer_leaves_gap"
    for create_n in range(1, MAX_CREATES + 1):
        print(f"\n=== v15 I2V {pid} Create {create_n}/{MAX_CREATES} ===", flush=True)
        tmp = dest.with_suffix(f".try{create_n}.tmp.mp4")
        tmp.unlink(missing_ok=True)
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
            try:
                _ = page.url
            except Exception:
                safe_close(ctx)
                return "reopen", None
            continue

        if info.get("needs_gallery_harvest") or (
            (not tmp.exists() or tmp.stat().st_size < 400_000)
            and (info.get("project_url") or info.get("url"))
        ):
            project_url = info.get("project_url") or info.get("url") or (page.url or "")
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
            return "reopen", None

        if not tmp.exists() or tmp.stat().st_size < 400_000:
            print("  empty download", flush=True)
            continue

        report = qa_clip(tmp, f"{pid}_try{create_n}", check_hair=check_hair)
        meta.setdefault("tries", {}).setdefault(pid, []).append(
            {"create": create_n, "status": "qa", "reject": report["reject"], "qa": report}
        )
        META.write_text(json.dumps(meta, indent=2) + "\n")
        if report["reject"]:
            REJECTED.mkdir(parents=True, exist_ok=True)
            bad = REJECTED / f"{pid}_v15_try{create_n}_reject.mp4"
            shutil.move(str(tmp), str(bad))
            print(f"  REJECT → {bad.name}", flush=True)
            continue
        shutil.move(str(tmp), str(dest))
        print(f"  ACCEPT {dest.name} sha={sha256(dest)[:16]}…", flush=True)
        return "ok", dest
    return "exhausted", None


def main() -> None:
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--plates", nargs="*", default=[
        "06_explorer_leaves_gap",
        "10_family_before_weight",
        "11_publish_gaps",
        "11b_wait_and_hunt",
    ])
    args = ap.parse_args()

    RAW.mkdir(parents=True, exist_ok=True)
    REJECTED.mkdir(parents=True, exist_ok=True)
    QA.mkdir(parents=True, exist_ok=True)

    if not PARENT_V14.exists():
        raise SystemExit(f"missing parent v14 {PARENT_V14}")
    got = sha256(PARENT_V14)
    if got != PARENT_V14_SHA:
        raise SystemExit(f"STOP: v14 sha mismatch want {PARENT_V14_SHA} got {got}")
    print(f"parent v14 sha OK {got}", flush=True)

    meta = {
        "parent_v14_sha256": PARENT_V14_SHA,
        "flow_account": REQUIRED_FLOW_EMAIL,
        "model": MODEL,
        "plates": args.plates,
        "tries": {},
        "accepted": {},
        "status": "running",
    }
    META.write_text(json.dumps(meta, indent=2) + "\n")

    with sync_playwright() as p:
        ctx, page, active = open_flow(p)
        meta["active_account"] = active
        META.write_text(json.dumps(meta, indent=2) + "\n")
        try:
            for pid in args.plates:
                while True:
                    status, dest = mint_plate(page, ctx, pid, meta)
                    if status == "reopen":
                        ctx, page, active = open_flow(p)
                        meta["active_account"] = active
                        continue
                    if status == "ok" and dest is not None:
                        meta["accepted"][pid] = {
                            "path": str(dest),
                            "sha256": sha256(dest),
                            "bytes": dest.stat().st_size,
                        }
                        META.write_text(json.dumps(meta, indent=2) + "\n")
                    else:
                        print(f"  GIVE UP {pid} — keep scrub/composite fallback", flush=True)
                    break
        finally:
            safe_close(ctx)

    meta["status"] = "done"
    META.write_text(json.dumps(meta, indent=2) + "\n")
    print("MINT DONE", json.dumps(meta.get("accepted", {}), indent=2), flush=True)


if __name__ == "__main__":
    main()
