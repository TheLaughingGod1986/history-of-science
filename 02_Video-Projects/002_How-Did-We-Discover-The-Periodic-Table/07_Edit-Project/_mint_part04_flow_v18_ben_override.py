#!/usr/bin/env python3
"""Part 04 Flow remint v18 — Ben OVERRIDE FAIL (06 / 10 / 11 / 11b).

Careful Flow Ultra on benoats@googlemail.com. Prefer Veo I2V from clean v18 starts.
If harvest empty/MAD ghosty or credits block — report blocker; do not ship ghost paint.

MAX 1 create per plate this run (careful credit use).
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

from PIL import Image, ImageChops, ImageFilter, ImageStat
from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))
import orbit_flow_veo_ui as flow  # noqa: E402

flow.FLOW_HOME = os.environ.get("ORBIT_FLOW_HOME", "https://flow.google.com/u/1/")

PROJ = Path(__file__).resolve().parents[1]
RAW = PROJ / "04_Generated-Clips/part04/raw/v18_fast"
REJECTED = RAW / "_rejected"
QA = PROJ / "07_Edit-Project/_qa_part04_v18_flow"
META = PROJ / "07_Edit-Project/part04_mint_flow_v18_meta.json"
STARTS = PROJ / "04_Generated-Clips/part04/refs/v18_start_frames"
HARVEST = Path(__file__).resolve().parent / "_harvest_newest_gallery_v01.py"
FORCE_DL = Path(__file__).resolve().parent / "_harvest_force_download_v04.py"
EDIT_DL = Path(__file__).resolve().parent / "_harvest_part04_v11_edit_download.py"

MODEL = os.environ.get("ORBIT_FLOW_VEO_MODEL", "Veo 3.1 - Fast")
PROFILE = Path(os.environ.get("ORBIT_FLOW_PROFILE", str(Path.home() / ".playwright-hos-flow-profile")))
REQUIRED_FLOW_EMAIL = "benoats@googlemail.com"
ALLOWED_FLOW_EMAILS = {REQUIRED_FLOW_EMAIL, "benoats@gmail.com"}
FORBIDDEN_FLOW_EMAIL = "benoats86@gmail.com"
MAX_CREATES = int(os.environ.get("HOS_V18_MAX_CREATES", "1"))
HARVEST_WAIT_S = int(os.environ.get("HOS_FLOW_HARVEST_WAIT_S", "360"))
PARENT_V17_SHA = "e4cc41d8cf050f6726e6b3d5cbbbff10285656c588f3a758b4a29e1ec1f998fd"

STYLE = (
    "Animistry-class stylised 3D cartoon (NOT photoreal). "
    "ONE continuous 1869 chemist desk at night: honey wood desktop, soft warm lamp, "
    "flat parchment grid sheet OR floating element cards, coloured flasks. "
    "Continuous gentle real camera/object motion. Silent. No Orbit. No Ken Burns still."
)
CLEAN = (
    "CLEAN LIGHT: soft warm desk-lamp glow ONLY — no lava, no blown jagged white, no stepped rings. "
    "Empty Chairs = ONE soft rectangular panel glow ONLY — never double edge."
)
SHARP = (
    "LATE SHOTS SHARP: every frame finished SINGLE EXPOSURE. "
    "ZERO horizontal ghost doubles, ZERO double-exposure edges, ZERO left-half mush. "
    "ONE solid lamp, ONE solid flask set / card set, ONE solid grid."
)
REJECT = (
    "HARD REJECT: ghost doubles; double-exposure; unfinished mush; lava lamp; "
    "face-cloud blot; black hole dots in hair; photoreal; Orbit; twins; hat."
)

PROMPTS = {
    "06_explorer_leaves_gap": (
        "Image-to-video from the attached start frame. Explorer garnish beat: "
        "ONE Explorer 3/4 BACK/profile at the desk — finished wavy brown crown, "
        "NO face-cloud blot, NO black hole dots in hair, gold glasses rim readable, "
        "clean written H/C/N/O cards, clean warm lamp. Continuous subtle settle. Silent. "
        + CLEAN + " " + SHARP + " " + REJECT + " " + STYLE
    ),
    "10_family_before_weight": (
        "Image-to-video from the attached start frame. FAMILY FIRST beat: "
        "sharp single-exposure H/C/N/O cards on desk, clean warm lamp, "
        "ONE soft Empty Chairs panel (no double edge). Continuous subtle settle. Silent. "
        + CLEAN + " " + SHARP + " " + REJECT + " " + STYLE
    ),
    "11_publish_gaps": (
        "Image-to-video from the attached start frame. PUBLISH THE GAPS beat: "
        "sharp finished desk with flat grid, flasks, cards, magnifier — "
        "ZERO horizontal ghost doubles. Continuous subtle settle. Silent. "
        + CLEAN + " " + SHARP + " " + REJECT + " " + STYLE
    ),
    "11b_wait_and_hunt": (
        "Image-to-video from the attached start frame. Wait-and-hunt beat: "
        "published flat grid with empty holes, flasks, soft lamp — "
        "ZERO ghost doubles. Continuous subtle hold/push-in. Silent. "
        + CLEAN + " " + SHARP + " " + REJECT + " " + STYLE
    ),
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


def extract(path: Path, t: float, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    subprocess.check_call(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-ss", f"{t:.2f}", "-i", str(path), "-frames:v", "1", "-q:v", "2", str(dest),
        ]
    )


def mad(a: Path, b: Path) -> float:
    ia = Image.open(a).convert("RGB").resize((480, 270))
    ib = Image.open(b).convert("RGB").resize((480, 270))
    d = ImageChops.difference(ia, ib)
    return ImageStat.Stat(d).mean[0]


def ghost_pair_frac(path: Path) -> float:
    e = Image.open(path).convert("L").filter(ImageFilter.FIND_EDGES)
    w, h = e.size
    crop = e.crop((0, int(h * 0.35), w, int(h * 0.75)))
    px = crop.load()
    cw, ch = crop.size
    strong = 40
    total = sum(1 for y in range(ch) for x in range(cw) if px[x, y] > strong)
    best = 0.0
    for dx in range(4, 12):
        hits = 0
        for y in range(ch):
            for x in range(cw - dx):
                if px[x, y] > strong and px[x + dx, y] > strong:
                    hits += 1
        best = max(best, hits / max(total, 1))
    return best


def qa_clip(path: Path, tag: str) -> dict:
    QA.mkdir(parents=True, exist_ok=True)
    frames = []
    fracs = []
    for t in (0.5, 3.0, 5.5, 7.0):
        dest = QA / f"{tag}_t{t}.jpg"
        extract(path, t, dest)
        frames.append(str(dest))
        fracs.append(ghost_pair_frac(dest))
    start = STARTS / f"{tag.split('_try')[0]}_start_v18.jpg"
    # MAD vs start — heavy Veo motion often trails ghosts
    mads = []
    if start.exists():
        for t in (0.5, 4.0):
            mid = QA / f"{tag}_mad_t{t}.jpg"
            extract(path, t, mid)
            mads.append(mad(start, mid))
    report = {
        "frames": frames,
        "ghost_pair_fracs": fracs,
        "ghost_peak": max(fracs) if fracs else None,
        "mads": mads,
        "mad_peak": max(mads) if mads else None,
        "reject": False,
        "reason": "",
    }
    # Ben fail publish ~0.60; keep below ~0.55 and MAD below ~12 (plate10 KEEP was ~4-5)
    if report["ghost_peak"] is not None and report["ghost_peak"] >= 0.55:
        report["reject"] = True
        report["reason"] = f"ghost_pair_frac {report['ghost_peak']:.3f} >= 0.55"
    if report["mad_peak"] is not None and report["mad_peak"] >= 14:
        report["reject"] = True
        report["reason"] = (report["reason"] + "; " if report["reason"] else "") + (
            f"mad_peak {report['mad_peak']:.1f} >= 14 (motion-ghost risk)"
        )
    return report


def accept_mp4(path: Path) -> bool:
    return path.exists() and path.stat().st_size >= 400_000


def run_harvest(tmp: Path, project_url: str, before_thumbs: int) -> bool:
    if not HARVEST.exists():
        return False
    env = os.environ.copy()
    env["ORBIT_FLOW_PROFILE"] = str(PROFILE)
    cmd = [
        sys.executable, str(HARVEST),
        "--project-url", project_url,
        "--out", str(tmp),
        "--before-thumbs", str(before_thumbs),
        "--wait-s", str(HARVEST_WAIT_S),
    ]
    print("  harvest:", " ".join(cmd[-8:]), flush=True)
    subprocess.run(cmd, env=env, check=False)
    return accept_mp4(tmp)


def run_force_download(tmp: Path, project_url: str) -> bool:
    if not FORCE_DL.exists():
        return False
    env = os.environ.copy()
    env["ORBIT_FLOW_PROFILE"] = str(PROFILE)
    cmd = [sys.executable, str(FORCE_DL), "--project-url", project_url, "--out", str(tmp)]
    print("  force-dl", flush=True)
    subprocess.run(cmd, env=env, check=False)
    return accept_mp4(tmp)


def run_edit_download(tmp: Path, project_url: str) -> bool:
    if not EDIT_DL.exists():
        return False
    env = os.environ.copy()
    env["ORBIT_FLOW_PROFILE"] = str(PROFILE)
    cmd = [sys.executable, str(EDIT_DL), "--project-url", project_url, "--out", str(tmp)]
    print("  edit-dl", flush=True)
    subprocess.run(cmd, env=env, check=False)
    return accept_mp4(tmp)


def assert_auth(page) -> None:
    html = page.content()
    if FORBIDDEN_FLOW_EMAIL in html:
        raise SystemExit(f"STOP: wrong Flow account {FORBIDDEN_FLOW_EMAIL}")
    ok = any(e in html for e in ALLOWED_FLOW_EMAILS)
    # soft: also check account menu text
    if not ok:
        print("  WARN: email not found in HTML; continuing if /u/1/ session looks live", flush=True)
    print(f"  AUTH minting via {page.url}", flush=True)


def mint_one(page, pid: str, meta: dict):
    start = STARTS / f"{pid}_start_v18.jpg"
    if not start.exists():
        raise SystemExit(f"missing {start}")
    dest = RAW / f"{pid}_v18.mp4"
    tmp = RAW / f"{pid}_v18.try.tmp.mp4"
    if tmp.exists():
        tmp.unlink()
    RAW.mkdir(parents=True, exist_ok=True)
    prompt = PROMPTS[pid]
    for create_n in range(1, MAX_CREATES + 1):
        print(f"\n=== v18 I2V {pid} Create {create_n}/{MAX_CREATES} ===", flush=True)
        print(f"  start-frame I2V: {start}", flush=True)
        before = 0
        try:
            before = page.locator("img").count()
        except Exception:
            pass
        try:
            info = flow.generate_clip(
                page,
                prompt,
                tmp,
                model=MODEL,
                start_frame=start,
                timeout_s=420,
                attempts=1,
                scenery_only=True,
            )
        except Exception as e:
            err = str(e)
            print(f"  create error: {e}", flush=True)
            meta.setdefault("errors", []).append({"plate": pid, "error": err})
            META.write_text(json.dumps(meta, indent=2) + "\n")
            if any(x in err.lower() for x in ("credit", "quota", "limit", "exhausted", "upgrade")):
                meta["credit_blocker"] = err
                META.write_text(json.dumps(meta, indent=2) + "\n")
                return "credit_block", None
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
            print(f"  careful harvest from {project_url}", flush=True)
            if run_harvest(tmp, project_url, before_thumbs=max(before, 0)):
                got = True
            elif run_force_download(tmp, project_url):
                got = True
            elif run_edit_download(tmp, project_url):
                got = True

        if not got:
            print("  empty download / harvest miss", flush=True)
            meta.setdefault("harvest_miss", []).append(pid)
            META.write_text(json.dumps(meta, indent=2) + "\n")
            continue

        report = qa_clip(tmp, f"{pid}_try{create_n}")
        meta.setdefault("tries", {}).setdefault(pid, []).append(
            {"create": create_n, "qa": report, "project_url": project_url}
        )
        META.write_text(json.dumps(meta, indent=2) + "\n")
        if report["reject"]:
            REJECTED.mkdir(parents=True, exist_ok=True)
            bad = REJECTED / f"{pid}_v18_try{create_n}_reject.mp4"
            shutil.move(str(tmp), str(bad))
            print(f"  REJECT {report['reason']} → {bad.name}", flush=True)
            continue
        shutil.move(str(tmp), str(dest))
        print(f"  ACCEPT {dest.name} sha={sha256(dest)[:16]}…", flush=True)
        meta.setdefault("accepted", {})[pid] = {
            "path": str(dest),
            "sha256": sha256(dest),
            "bytes": dest.stat().st_size,
            "qa": report,
        }
        META.write_text(json.dumps(meta, indent=2) + "\n")
        return "ok", dest
    return "exhausted", None


def main() -> None:
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--plates",
        nargs="*",
        default=["11_publish_gaps", "11b_wait_and_hunt", "10_family_before_weight", "06_explorer_leaves_gap"],
    )
    args = ap.parse_args()
    RAW.mkdir(parents=True, exist_ok=True)
    meta: dict = {
        "engine": "flow-veo-ui",
        "account": REQUIRED_FLOW_EMAIL,
        "parent_v17_sha": PARENT_V17_SHA,
        "bible_main": "25bdefd",
        "plates_requested": args.plates,
        "accepted": {},
        "status": "running",
        "updated": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }
    META.write_text(json.dumps(meta, indent=2) + "\n")

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE),
            headless=False,
            viewport={"width": 1400, "height": 900},
            accept_downloads=True,
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=120000)
        time.sleep(3)
        try:
            page.get_by_role("button", name="Agree").click(timeout=3000)
        except Exception:
            pass
        assert_auth(page)
        for pid in args.plates:
            status, _ = mint_one(page, pid, meta)
            if status == "credit_block":
                meta["status"] = "CREDIT_BLOCKER"
                META.write_text(json.dumps(meta, indent=2) + "\n")
                print("CREDIT BLOCKER — stop Flow creates", flush=True)
                break
        else:
            meta["status"] = "done" if meta.get("accepted") else "no_accepts"
        META.write_text(json.dumps(meta, indent=2) + "\n")
        safe_close(ctx)
    print(json.dumps(meta, indent=2), flush=True)


if __name__ == "__main__":
    main()
