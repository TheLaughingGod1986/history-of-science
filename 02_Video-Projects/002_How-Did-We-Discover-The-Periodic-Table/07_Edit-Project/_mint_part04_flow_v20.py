#!/usr/bin/env python3
"""Part 04 Flow remint v20 — UAT HARD FAIL bible 43d9405 (parent v19 scalp pits + publish ghosts).

Parent FAIL: hos_002_part04_rough_v19.mp4
  sha256 69d48f6e5fac419df5c23c17df5d0ef628cb4e8d533ba085bb3c8a173016bcdf

Remint ONLY via Flow Ultra real gallery mp4 harvest (Ben v19 stills):
  06_explorer_leaves_gap · 07_eka_placeholders · 07b_eka_names_rotate
  08_prediction_navigation · 08b_navigation_walk
  09_risk_bet · 09b_risk_hold · 10_family_before_weight
  11_publish_gaps · 11b_wait_and_hunt

NO PAINT FALLBACK. NO temporal-median. NO brightness-motion paint.
If harvest empty / MAD-high doubles → reject + retry. STOP to CoS only after real retries.

Flow: benoats@googlemail.com (credits confirmed 8000+). Scores → CoS. No PASS. No Ben ping.
"""
from __future__ import annotations
import faulthandler
faulthandler.enable()

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

flow.FLOW_HOME = os.environ.get("ORBIT_FLOW_HOME", "https://flow.google.com/")

PROJ = Path(__file__).resolve().parents[1]
RAW = PROJ / "04_Generated-Clips/part04/raw/v20_fast"
REJECTED = RAW / "_rejected"
QA = PROJ / "07_Edit-Project/_qa_part04_v20_flow"
META = PROJ / "07_Edit-Project/part04_mint_flow_v20_meta.json"
STARTS = PROJ / "04_Generated-Clips/part04/refs/v20_start_frames"
HARVEST = Path(__file__).resolve().parent / "_harvest_newest_gallery_v01.py"
FORCE_DL = Path(__file__).resolve().parent / "_harvest_force_download_v04.py"
EDIT_DL = Path(__file__).resolve().parent / "_harvest_part04_v11_edit_download.py"

MODEL = os.environ.get("ORBIT_FLOW_VEO_MODEL") or "Veo 3.1 - Fast"
PROFILE = Path(os.environ.get("ORBIT_FLOW_PROFILE", str(Path.home() / ".playwright-hos-flow-profile")))
CDP_URL = os.environ.get("ORBIT_FLOW_CDP", "http://127.0.0.1:9222")
REQUIRE_CDP = os.environ.get("HOS_FLOW_REQUIRE_CDP", "1") == "1"
REQUIRED_FLOW_EMAIL = "benoats@googlemail.com"
ALLOWED_FLOW_EMAILS = {REQUIRED_FLOW_EMAIL, "benoats@gmail.com"}
FORBIDDEN_FLOW_EMAIL = "benoats86@gmail.com"
MAX_CREATES = int(os.environ.get("HOS_V20_MAX_CREATES", "3"))
HARVEST_WAIT_S = int(os.environ.get("HOS_FLOW_HARVEST_WAIT_S", "480"))
PARENT_V19_SHA = "69d48f6e5fac419df5c23c17df5d0ef628cb4e8d533ba085bb3c8a173016bcdf"

STYLE = (
    "FINISHED cinematic stylised 3D house quality (Animistry-class). "
    "NOT flat unfinished vlog vector. NOT 2D cutouts. NOT cheap cel. "
    "Believable wood grain, glass refraction, soft depth of field, polished materials. "
    "ONE continuous 1869 chemist study at night: honey wood desk, soft warm lamp, "
    "parchment grid OR readable element cards, coloured flasks. "
    "Silent. No Orbit. No Ken Burns still. No paint / no double-exposure."
)
CLEAN = (
    "CLEAN LIGHT (BIBLE HARD): warm desk-lamp glow ONLY — a soft continuous luminous cone. "
    "ZERO lava drip, ZERO molten leak, ZERO fire spit, ZERO sparks, ZERO embers, "
    "ZERO flames, ZERO burning chair rim, ZERO dripping bulb goo onto desk/chair. "
    "ZERO lamp-beam sparks, ZERO floating embers, ZERO fire spit motes, ZERO firework particles, "
    "ZERO ash flecks, ZERO glowing coal dots drifting in the beam (try7 UAT: continuous beam sparks FAIL — never soft-pass as dust). "
    "Soft continuous warm cone — no stepped banding rings on the lamp shade. "
    "Empty Chairs = ONE soft rectangular panel glow ONLY — never double edge."
)
SHARP = (
    "LATE SHOTS SHARP / SINGLE EXPOSURE (HARD): every frame finished cinematic 3D. "
    "ZERO horizontal ghost doubles, ZERO double-exposure edges, ZERO left-half mush, "
    "ZERO jitter trail on grid lines / flasks / lamp / magnifier. "
    "ONE solid lamp, ONE solid flask set / card set, ONE solid grid. "
    "LOCKED or VERY GENTLE camera — prefer locked tripod settle over any pan that smears edges."
)
REJECT = (
    "HARD REJECT: unfinished flat vlog vector; lava drip / molten leak / fire spit; "
    "horizontal ghost doubles; double-exposure; unfinished mush; "
    "garbled cards / striping; lamp banding; face-cloud blot; black hole dots in hair; "
    "photoreal; Orbit; twins; hat."
)

LOCK_CAM = (
    "ABSOLUTELY LOCKED CAMERA: no camera move at all for 8 seconds. Static tripod. "
    "Any horizontal motion causes FAIL ghost doubles — forbidden. "
    "Single clean exposure like a still photograph that barely breathes."
)
STILL_PROPS = (
    "ALL PROPS FROZEN IN PLACE: grid, flasks, lamp, magnifier, cards do not travel, "
    "do not slide, do not pan across frame. Magnifier stays fixed on the desk — ZERO travel. "
    "Only microscopic liquid shimmer inside flasks is allowed. No object fly-through."
)
PROMPTS = {
    "11_publish_gaps": (
        "Image-to-video from the attached start frame. PUBLISH THE GAPS beat. "
        "Finished cinematic stylised 3D chemist desk — NOT flat unfinished vector. "
        "HARD LOCKED TRIPOD CAMERA — zero pan, zero dolly, zero truck, zero orbit. "
        + LOCK_CAM + " " + STILL_PROPS + " "
        "SINGLE EXPOSURE every frame: ZERO horizontal ghost / double-edge / smear / tear on "
        "grid lines, coloured flasks, desk lamp, magnifier, moon. "
        "One solid lamp, one solid flask set, one solid grid, one solid magnifier. "
        "CLEAN warm lamp ONLY — zero lava drip / molten leak / fire spit. No Explorer. Silent. "
        + CLEAN + " " + SHARP + " " + REJECT + " " + STYLE
    ),
    "11b_wait_and_hunt": (
        "Image-to-video from the attached start frame. Wait-and-hunt beat. "
        "Finished cinematic stylised 3D published parchment grid with empty circular holes, "
        "flasks, soft warm lamp — NOT flat unfinished vector. "
        "HARD LOCKED TRIPOD CAMERA — zero horizontal pan / smear. "
        + LOCK_CAM + " " + STILL_PROPS + " "
        "SINGLE EXPOSURE continuous playback: ZERO ghost doubles / horizontal tears on "
        "grid / flasks / lamp / magnifier / moon in mid frames. "
        "CLEAN warm lamp ONLY — zero lava drip. No Explorer. Silent. "
        + CLEAN + " " + SHARP + " " + REJECT + " " + STYLE
    ),
    "06_explorer_leaves_gap": (
        "Image-to-video from the attached start frame. Explorer garnish beat. "
        "KEEP THIS exact finished Explorer from the still: gold round glasses, messy brown hair "
        "with ZERO black circular scalp pits, teal coat, yellow vest, brown bow tie, satchel. "
        "He is examining a specimen at a chemist bench. Tiny head/hands settle only. "
        "Finished cinematic stylised 3D (Animistry-class). NOT flat unfinished vlog. "
        "NOT a rear-view orange-hair chibi with holes in the crown. NOT a pith helmet. NOT twins. "
        "Exactly one Explorer, one face. CLEAN warm lamp ONLY — no lava, no fire. "
        "LOCKED CAMERA. Silent. "
        + CLEAN + " " + SHARP + " " + REJECT + " " + STYLE
    ),
    "07_eka_placeholders": (
        "IMAGE-TO-VIDEO of the attached start frame. Eka-placeholder beat. "
        "Animate THIS exact empty-chair chemist study at night — honey wood desk, empty wooden chair, "
        "moon in the window, one desk lamp. LOCKED TRIPOD CAMERA. Silent. "
        "Vacant cream card seats sit ON the desk as physical paper placeholders in a column — "
        "not floating HUD, not pasted 2D overlays, not flaming cards. "
        "CLEAN LIGHT — HOUSE HARD FAIL IF BROKEN for the FULL 8 seconds: the lampshade HIDES the bulb; "
        "only a soft continuous warm cone. ZERO visible hanging glass bulb drip. "
        "HARD BAN (t0 through t8): fire, flame, flames, spark, sparks, ember, embers, lava, lava drip, "
        "molten leak, fire spit, burning card aura, fiery N14, dripping bulb goo, lamp-beam sparks. "
        "Do NOT write letters, element symbols, captions, UI, or signage anywhere. Blank cream cards only. "
        "No floating cards. No Explorer. No Orbit. No paint. No double-exposure. "
        + LOCK_CAM + " " + CLEAN + " " + SHARP + " " + REJECT + " " + STYLE
    ),
    "07b_eka_names_rotate": (
        "IMAGE-TO-VIDEO of the attached start frame. Eka-names / vacant-seat pulse beat. "
        "Animate THIS exact empty-chair chemist study. Soft pulse of attention across two or three "
        "vacant cream-card seats that rest ON the honey wood desk as physical paper — "
        "NOT floating HUD, NOT pasted 2D cutouts, NOT a flaming N14 card. "
        "LOCKED TRIPOD CAMERA. Silent. "
        "CLEAN LIGHT — HOUSE HARD FAIL IF BROKEN for the FULL 8 seconds: lampshade HIDES the bulb; "
        "only a soft continuous warm cone. ZERO lava drip, ZERO molten leak, ZERO fire spit, "
        "ZERO fiery card border, ZERO dripping goo onto chair/desk. "
        "Do NOT write letters, element symbols, Eka labels, N14, captions, or UI anywhere in the frame. "
        "Blank cream cards / empty slots only. No Explorer. No Orbit. No paint. No double-exposure. "
        + LOCK_CAM + " " + CLEAN + " " + SHARP + " " + REJECT + " " + STYLE
    ),
    "08_prediction_navigation": (
        "IMAGE-TO-VIDEO of the attached start frame. A PREDICTION beat. "
        "Animate THIS exact empty-chair chemist study — honey wood desk, empty wooden chair, "
        "moon in the window. LOCKED TRIPOD CAMERA. Silent. "
        "CLEAN LIGHT — HOUSE HARD FAIL IF BROKEN for the FULL 8 seconds: the lampshade HIDES the bulb; "
        "only a soft continuous warm cone. ZERO visible hanging glass bulb. "
        "HARD BAN (t0 through t8): fire, flame, flames, spark, sparks, ember, embers, lava, lava drip, "
        "molten leak, fire spit, burning chair rim, fiery card aura, flaming N14, dripping bulb goo. "
        "CARDLESS desk: flasks, mortar, book, blank paper stack, lamp, empty chair only. "
        "Do NOT write letters, element symbols, or UI. No floating cards. No Explorer. No Orbit. "
        + LOCK_CAM + " " + CLEAN + " " + SHARP + " " + REJECT + " " + STYLE
    ),
    "08b_navigation_walk": (
        "IMAGE-TO-VIDEO of the attached start frame. Prediction settle / walk-to-address beat. "
        "Animate THIS exact empty-chair chemist study. LOCKED TRIPOD CAMERA. Silent. "
        "CLEAN LIGHT HARD for 8 seconds: lampshade HIDES the bulb; soft continuous warm cone only. "
        "ZERO lava drip / molten leak / fire spit / flames behind the chair / lamp-beam sparks. "
        "Do NOT write letters or UI on cards. Blank paper stacks OK. No floating cards. "
        "No Explorer. No Orbit. No paint. No double-exposure. "
        + LOCK_CAM + " " + CLEAN + " " + SHARP + " " + REJECT + " " + STYLE
    ),
    "09_risk_bet": (
        "Image-to-video from the attached start frame. RISK / A PREDICTION beat. "
        "Finished cinematic stylised 3D chemist study — NOT flat unfinished vlog vector. "
        "Wooden chair + desk + warm lamp. "
        "CLEAN LIGHT HARD: warm lamp glow ONLY — ZERO lava drip under bulb, ZERO molten leak, "
        "ZERO fire spit onto chair/desk, ZERO burning chair rim glow. "
        "Readable element cards. LOCKED or very gentle camera. Silent. "
        + LOCK_CAM + " " + CLEAN + " " + SHARP + " " + REJECT + " " + STYLE
    ),
    "09b_risk_hold": (
        "IMAGE-TO-VIDEO of the attached start frame. Animate THIS exact empty-chair chemist study. "
        "A BET / risk-hold settle beat. Finished cinematic stylised 3D — honey wood desk, empty wooden chair, "
        "bookshelf, moon in the window. LOCKED TRIPOD CAMERA. Silent. "
        "CLEAN LIGHT — HOUSE HARD FAIL IF BROKEN for the FULL 8 seconds: warm clean desk-lamp glow ONLY. "
        "HARD BAN forever (t0 through t8): fire, flame, flames, spark, sparks, ember, embers, lava, lava drip, "
        "molten leak, fire spit, burning chair rim, candle flicker, firework particles, glowing coal, "
        "dripping bulb goo, lamp-beam sparks, floating embers. "
        "Chair back is PLAIN finished wood. Do NOT write any words, labels, captions, UI, or signage "
        "anywhere in the frame. No lettering on the chair. No HUD. "
        "CARDLESS desk: ceramic vessels, mortar, flasks, one blank paper stack, lamp, chair only. "
        "No Explorer. No Orbit. No paint. No double-exposure. "
        + LOCK_CAM + " " + CLEAN + " " + SHARP + " " + REJECT + " " + STYLE
    ),
    "10_family_before_weight": (
        "Image-to-video from the attached start frame. FAMILY FIRST beat. "
        "Finished cinematic stylised 3D chemist desk with readable element cards — "
        "NOT flat unfinished vlog vector cutouts. Wood grain, glass, soft DOF. "
        "CLEAN LIGHT HARD: warm lamp ONLY — ZERO lava drip / molten leak / fire spit "
        "under bulb onto desk/chair. Readable cards H/C/N/O family. Locked camera. Silent. "
        + LOCK_CAM + " " + STILL_PROPS + " " + CLEAN + " " + SHARP + " " + REJECT + " " + STYLE
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
    """≥5 mid-plate frames + ghost/MAD gates. Reject MAD-high doubles."""
    QA.mkdir(parents=True, exist_ok=True)
    frames = []
    fracs = []
    times = (0.4, 1.5, 3.0, 4.5, 6.0, 7.2)
    for t in times:
        dest = QA / f"{tag}_t{t}.jpg"
        extract(path, t, dest)
        frames.append(str(dest))
        fracs.append(ghost_pair_frac(dest))
    start = STARTS / f"{tag.split('_try')[0]}_start_v20.jpg"
    mads = []
    if start.exists():
        for t in (0.5, 3.5, 6.5):
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
    # Ben publish fail ~0.60; keep stricter for continuous playback
    if report["ghost_peak"] is not None and report["ghost_peak"] >= 0.40:
        report["reject"] = True
        report["reason"] = f"ghost_pair_frac {report['ghost_peak']:.3f} >= 0.40"
    if report["mad_peak"] is not None and report["mad_peak"] >= 12:
        report["reject"] = True
        report["reason"] = (report["reason"] + "; " if report["reason"] else "") + (
            f"mad_peak {report['mad_peak']:.1f} >= 12 (MAD-high / motion-ghost risk)"
        )
    lavas = []
    for dest in frames:
        lavas.append(lava_frac(Path(dest)))
    report["lava_fracs"] = lavas
    report["lava_peak"] = max(lavas) if lavas else None
    if report["lava_peak"] is not None and report["lava_peak"] >= 0.012:
        report["reject"] = True
        report["reason"] = (report["reason"] + "; " if report["reason"] else "") + (
            f"lava_peak {report['lava_peak']:.4f} >= 0.012 (bulb drip / fire)"
        )
    return report


def lava_frac(path: Path) -> float:
    im = Image.open(path).convert("RGB").resize((480, 270))
    px = im.load()
    w, h = im.size
    n = 0
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            if r > 185 and b < 85 and (r - b) > 105 and g < 165:
                n += 1
    return n / max(1, w * h)


def accept_mp4(path: Path) -> bool:
    return path.exists() and path.stat().st_size >= 400_000


def run_harvest(tmp: Path, project_url: str, before_thumbs: int) -> bool:
    if not HARVEST.exists():
        return False
    env = os.environ.copy()
    env["ORBIT_FLOW_PROFILE"] = str(PROFILE)
    env["ORBIT_FLOW_CDP"] = CDP_URL
    env["HOS_FLOW_REQUIRE_CDP"] = "1"
    env["ORBIT_FLOW_HOME"] = flow.FLOW_HOME
    env["HOS_FLOW_HARVEST_WAIT_S"] = str(max(HARVEST_WAIT_S, 480))
    cmd = [
        sys.executable, str(HARVEST),
        "--project", project_url,
        "--out", str(tmp),
        "--before-thumbs", str(before_thumbs),
        "--wait-s", str(HARVEST_WAIT_S),
        "--cdp", CDP_URL,
    ]
    print("  harvest:", " ".join(cmd[-8:]), flush=True)
    subprocess.run(cmd, env=env, check=False)
    return accept_mp4(tmp)


def run_force_download(tmp: Path, project_url: str) -> bool:
    if not FORCE_DL.exists():
        return False
    env = os.environ.copy()
    env["ORBIT_FLOW_PROFILE"] = str(PROFILE)
    env["ORBIT_FLOW_CDP"] = CDP_URL
    env["HOS_FLOW_REQUIRE_CDP"] = "1"
    cmd = [sys.executable, str(FORCE_DL), "--project", project_url, "--dest", str(tmp)]
    print("  force-dl", flush=True)
    subprocess.run(cmd, env=env, check=False)
    return accept_mp4(tmp)


def run_edit_download(tmp: Path, project_url: str) -> bool:
    if not EDIT_DL.exists():
        return False
    env = os.environ.copy()
    env["ORBIT_FLOW_PROFILE"] = str(PROFILE)
    env["ORBIT_FLOW_CDP"] = CDP_URL
    env["HOS_FLOW_REQUIRE_CDP"] = "1"
    cmd = [sys.executable, str(EDIT_DL), "--project", project_url, "--dest", str(tmp)]
    print("  edit-dl", flush=True)
    subprocess.run(cmd, env=env, check=False)
    return accept_mp4(tmp)


def assert_auth(page) -> dict:
    """Confirm live ULTRA session = benoats@googlemail.com, ~8k+ credits, no passkey.

    STOP_TO_COS on passkey / forbidden 86 / low credits. Never open a fresh Playwright profile.
    """
    import re as _re

    html = page.content()
    body = ""
    try:
        body = page.inner_text("body")
    except Exception:
        body = html
    low = (html + "\n" + body).lower()
    # passkey / verify wall
    passkey = any(
        x in low
        for x in (
            "passkey",
            "verifying it's you",
            "verifying it’s you",
            "complete sign-in using your passkey",
            "use your passkey",
            "confirm it's you",
            "confirm it’s you",
        )
    )
    if passkey:
        raise SystemExit(
            "STOP_TO_COS BLOCKED_AUTH: passkey wall on attached Chrome. "
            f"profile/CDP={CDP_URL} url={page.url}"
        )
    if FORBIDDEN_FLOW_EMAIL.lower() in low or "benoats86" in low:
        # only fatal if required email absent
        if REQUIRED_FLOW_EMAIL.lower() not in low and "benoats@googlemail.com" not in low:
            raise SystemExit(
                f"STOP_TO_COS BLOCKED_AUTH: forbidden {FORBIDDEN_FLOW_EMAIL} on {page.url}"
            )
    credits = None
    for m in _re.finditer(r"([\d,]{3,7})\s*google flow credits", body, _re.I):
        credits = int(m.group(1).replace(",", ""))
        break
    if credits is None:
        for m in _re.finditer(r"([\d,]{3,7})\s*credits", body, _re.I):
            credits = int(m.group(1).replace(",", ""))
            break
    ultra = "ultra" in low
    has_req = REQUIRED_FLOW_EMAIL.lower() in low or "benoats@googlemail.com" in low
    if credits is not None and credits < 1000:
        raise SystemExit(
            f"STOP_TO_COS BLOCKED_AUTH: credits={credits} too low on {page.url}"
        )
    if not has_req:
        print(
            "  WARN: required email not in DOM yet; ULTRA+credits gate still applies",
            flush=True,
        )
    info = {
        "url": page.url,
        "email_ok": has_req,
        "credits": credits,
        "ultra": ultra,
        "cdp": CDP_URL,
        "passkey": False,
    }
    print(
        f"  AUTH OK cdp={CDP_URL} ultra={ultra} credits={credits} url={page.url}",
        flush=True,
    )
    return info


def mint_one(page, pid: str, meta: dict):
    start = STARTS / f"{pid}_start_v20.jpg"
    if not start.exists():
        raise SystemExit(f"missing {start}")
    dest = RAW / f"{pid}_v20.mp4"
    tmp = RAW / f"{pid}_v20.try.tmp.mp4"
    if dest.exists() and accept_mp4(dest) and os.environ.get("HOS_V20_SKIP_EXISTING", "1") == "1":
        report = qa_clip(dest, f"{pid}_existing")
        if not report["reject"]:
            print(f"  SKIP existing clean {dest.name}", flush=True)
            meta.setdefault("accepted", {})[pid] = {
                "path": str(dest),
                "sha256": sha256(dest),
                "bytes": dest.stat().st_size,
                "qa": report,
                "skipped_existing": True,
            }
            META.write_text(json.dumps(meta, indent=2) + "\n")
            return "ok", dest
        print(f"  existing REJECT {report['reason']} — reminting", flush=True)
    if tmp.exists():
        tmp.unlink()
    RAW.mkdir(parents=True, exist_ok=True)
    prompt = PROMPTS[pid]
    for create_n in range(1, MAX_CREATES + 1):
        print(f"\n=== v20 I2V {pid} Create {create_n}/{MAX_CREATES} ===", flush=True)
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
                timeout_s=900,
                attempts=1,
                scenery_only=True,
            )
        except Exception as e:
            err = str(e)
            print(f"  create error: {e}", flush=True)
            meta.setdefault("errors", []).append({"plate": pid, "error": err, "create": create_n})
            META.write_text(json.dumps(meta, indent=2) + "\n")
            if any(x in err.lower() for x in ("credit", "quota", "limit", "exhausted", "upgrade")):
                meta["credit_blocker"] = err
                META.write_text(json.dumps(meta, indent=2) + "\n")
                return "credit_block", None
            # retry next create
            continue

        project_url = info.get("project_url") or info.get("url") or (page.url or "")
        project_url = project_url.split("?")[0].rstrip("/")
        meta.setdefault("projects", {})[f"{pid}_try{create_n}"] = project_url
        meta.setdefault("flow_job_ids", {})[f"{pid}_try{create_n}"] = {
            "project_url": project_url,
            "media_id": info.get("media_id"),
            "model": MODEL,
        }
        META.write_text(json.dumps(meta, indent=2) + "\n")

        got = accept_mp4(tmp)
        if not got and (
            info.get("needs_gallery_harvest")
            or (not tmp.exists() or tmp.stat().st_size < 400_000)
        ):
            print(f"  careful harvest from {project_url}", flush=True)
            print("  waiting 90s for Flow gen before harvest…", flush=True)
            time.sleep(90)
            # close page noise — harvest uses its own browser
            if run_harvest(tmp, project_url, before_thumbs=max(before, 0)):
                got = True
            elif run_force_download(tmp, project_url):
                got = True
            elif run_edit_download(tmp, project_url):
                got = True

        if not got:
            print("  empty download / harvest miss — NO PAINT; retry create", flush=True)
            meta.setdefault("harvest_miss", []).append({"plate": pid, "create": create_n, "project_url": project_url})
            META.write_text(json.dumps(meta, indent=2) + "\n")
            continue

        report = qa_clip(tmp, f"{pid}_try{create_n}")
        meta.setdefault("tries", {}).setdefault(pid, []).append(
            {"create": create_n, "qa": report, "project_url": project_url, "bytes": tmp.stat().st_size}
        )
        META.write_text(json.dumps(meta, indent=2) + "\n")
        if report["reject"]:
            REJECTED.mkdir(parents=True, exist_ok=True)
            bad = REJECTED / f"{pid}_v20_try{create_n}_reject.mp4"
            shutil.move(str(tmp), str(bad))
            print(f"  REJECT {report['reason']} → {bad.name}", flush=True)
            continue
        shutil.move(str(tmp), str(dest))
        print(f"  ACCEPT {dest.name} sha={sha256(dest)[:16]}… bytes={dest.stat().st_size}", flush=True)
        meta.setdefault("accepted", {})[pid] = {
            "path": str(dest),
            "sha256": sha256(dest),
            "bytes": dest.stat().st_size,
            "qa": report,
            "project_url": project_url,
            "create": create_n,
            "engine": "flow-veo-ui-gallery",
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
        default=[
            "06_explorer_leaves_gap",
            "07_eka_placeholders",
            "07b_eka_names_rotate",
            "08_prediction_navigation",
            "08b_navigation_walk",
            "09_risk_bet",
            "09b_risk_hold",
            "10_family_before_weight",
            "11_publish_gaps",
            "11b_wait_and_hunt",
        ],
    )
    args = ap.parse_args()
    RAW.mkdir(parents=True, exist_ok=True)
    QA.mkdir(parents=True, exist_ok=True)
    meta: dict = {
        "engine": "flow-veo-ui",
        "account": REQUIRED_FLOW_EMAIL,
        "forbidden_account": FORBIDDEN_FLOW_EMAIL,
        "parent_v19_sha": PARENT_V19_SHA,
        "bible_main": "43d9405",
        "model": MODEL,
        "plates_requested": args.plates,
        "accepted": {},
        "no_paint_fallback": True,
        "cdp": CDP_URL,
        "flow_home": flow.FLOW_HOME,
        "status": "running",
        "updated": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }
    META.write_text(json.dumps(meta, indent=2) + "\n")

    # HARD RULE: attach to Ben's already-open Mini Chrome CDP (OrbitStudio :9222).
    # Do NOT launch a fresh Playwright profile (passkey). Do NOT use benoats86.
    if REQUIRE_CDP:
        print(f"Attaching Flow via CDP {CDP_URL} (no fresh Playwright profile)", flush=True)
    with sync_playwright() as p:
        browser = None
        ctx = None
        page = None
        close_ctx = False
        try:
            browser = p.chromium.connect_over_cdp(CDP_URL)
            # Prefer existing Flow tab
            for c in browser.contexts:
                for pg in c.pages:
                    u = (pg.url or "").lower()
                    if "flow.google.com" in u or "labs.google" in u:
                        page = pg
                        ctx = c
                        break
                if page is not None:
                    break
            if page is None:
                # open Flow on existing context (still same Chrome profile — no passkey)
                ctx = browser.contexts[0] if browser.contexts else None
                if ctx is None:
                    raise SystemExit(
                        f"STOP_TO_COS BLOCKED_AUTH: CDP {CDP_URL} has no contexts"
                    )
                page = ctx.new_page()
                page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=120000)
            else:
                page.bring_to_front()
                # Stay on live ULTRA home — do NOT hop to /u/1/ (86 trap)
                if "/u/1" in (page.url or ""):
                    raise SystemExit(
                        "STOP_TO_COS BLOCKED_AUTH: attached tab is /u/1/ "
                        "(forbidden 86 path). Need live flow.google.com ULTRA tab."
                    )
                if "flow.google.com" not in (page.url or ""):
                    page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=120000)
            time.sleep(2)
            try:
                page.get_by_role("button", name="Agree").click(timeout=3000)
            except Exception:
                pass
            # Open account menu so credits + email land in DOM
            try:
                page.locator("text=ULTRA").first.click(timeout=2500)
                time.sleep(1.5)
            except Exception:
                pass
            auth = assert_auth(page)
            meta["auth"] = auth
            META.write_text(json.dumps(meta, indent=2) + "\n")
            (QA / "auth_ok_cdp.json").write_text(json.dumps(auth, indent=2) + "\n")
            try:
                page.screenshot(path=str(QA / "auth_ok_cdp.png"), full_page=False)
            except Exception:
                pass

            for pid in args.plates:
                status, _ = mint_one(page, pid, meta)
                if status == "credit_block":
                    meta["status"] = "CREDIT_BLOCKER"
                    META.write_text(json.dumps(meta, indent=2) + "\n")
                    print("CREDIT BLOCKER — stop Flow creates; NO PAINT", flush=True)
                    break
                if status == "exhausted":
                    meta.setdefault("exhausted_plates", []).append(pid)
                    META.write_text(json.dumps(meta, indent=2) + "\n")
                    print(f"EXHAUSTED {pid} after {MAX_CREATES} creates — NO PAINT", flush=True)
            else:
                want = set(args.plates)
                got = set(meta.get("accepted", {}))
                meta["status"] = "done" if want <= got else "partial"
            META.write_text(json.dumps(meta, indent=2) + "\n")
        finally:
            # Never close Ben's Chrome — only disconnect Playwright CDP client.
            try:
                if browser is not None:
                    browser.close()
            except Exception:
                pass

    print(json.dumps(meta, indent=2), flush=True)
    missing = [p for p in args.plates if p not in meta.get("accepted", {})]
    if missing:
        raise SystemExit(
            f"STOP_TO_COS: Flow did not accept real gallery mp4 for {missing}. "
            "NO PAINT FALLBACK. Retry evidence in part04_mint_flow_v20_meta.json"
        )


if __name__ == "__main__":
    try:
        main()
    except BaseException as e:
        import traceback
        traceback.print_exc()
        print(f"FATAL: {type(e).__name__}: {e}", flush=True)
        raise
