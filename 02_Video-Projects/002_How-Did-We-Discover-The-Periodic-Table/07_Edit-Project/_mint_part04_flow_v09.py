#!/usr/bin/env python3
"""Part 04 Flow Veo 3.1 Fast remint v09 — Explorer HAT-FREE + colour DNA lock.

CoS/Ben override 8 Sep: v08 FAIL = teal pith helmet AND colour DNA drift
(darkened skin / off-house coat). Remint ONLY 06_explorer_leaves_gap.

KEEP: v08/v07 timeline everything else; 02b/05/09/09b; P01–P03 untouched.
Flow: benoats@googlemail.com on /u/1/. Max 2 Creates. Create dies → STOP.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

from PIL import Image

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))

import orbit_flow_veo_ui as flow  # noqa: E402
import orbit_gemini_veo as veo  # noqa: E402

flow.FLOW_HOME = os.environ.get("ORBIT_FLOW_HOME", "https://flow.google.com/u/1/")

PROJ = Path(__file__).resolve().parents[1]
PLATES_JSON = PROJ / "07_Edit-Project/parts/part-04_plates_v01.json"
RAW = PROJ / "04_Generated-Clips/part04/raw/v09_fast"
REJECTED = RAW / "_rejected"
QA_STILLS = PROJ / "07_Edit-Project/_qa_part04_v09_plate"
META = PROJ / "07_Edit-Project/part04_mint_flow_v09_meta.json"
HARVEST = Path(__file__).resolve().parent / "_harvest_newest_gallery_v01.py"
FORCE_DL = Path(__file__).resolve().parent / "_harvest_force_download_v01.py"
MODEL = os.environ.get("ORBIT_FLOW_VEO_MODEL", "Veo 3.1 - Fast")
PROFILE = Path(
    os.environ.get(
        "ORBIT_FLOW_PROFILE",
        str(Path.home() / ".playwright-hos-flow-profile"),
    )
)
MAX_CREATES = int(os.environ.get("HOS_V09_MAX_CREATES", "2"))
CREATE_OFFSET = int(os.environ.get("HOS_V09_CREATE_OFFSET", "0"))

START_FRAME_06 = PROJ / (
    "04_Generated-Clips/part04/refs/v09_start_frames/06_explorer_leaves_gap_start_v09.jpg"
)
# Prefer hat-free on-colour start (NOT v08 FAIL video stills)
START_FRAME_PREF = PROJ / (
    "04_Generated-Clips/part04/refs/v09_start_frames/_ref_v08_start_hatfree.jpg"
)
DNA_GERMS = PROJ / "04_Generated-Clips/part04/refs/v09_dna/germs_lock.jpg"
DNA_P03 = PROJ / "04_Generated-Clips/part04/refs/v09_dna/p03_keep.jpg"
DNA_SHEET = PROJ / "04_Generated-Clips/part04/refs/v09_dna/character_sheet.jpg"

PARENT_V08 = PROJ / "09_Final-Export/hos_002_part04_rough_v08.mp4"
PARENT_V08_SHA = "8cafb379af976897d6cee46484439b1ecbda56f8a42760327a96d1744d614a83"

STYLE = (
    "Animistry-class stylised 3D cartoon (NOT photoreal). "
    "ONE continuous 1869 chemist desk: honey wood desktop, soft warm lamp, cream "
    "blank cards, leather books, lab vessels. Continuous real camera/object motion "
    "the whole clip. Silent. No Orbit. No Ken Burns still. Opaque vessels preferred."
)

COLOUR_DNA_LOCK = (
    "EXPLORER COLOUR DNA LOCK (match History of Science character sheet + Germs lock "
    "+ Part 03 keep EXACTLY — same boy, not a recolour cousin): "
    "Skin = light–medium warm tan / fair boy skin (NOT darkened, NOT deep brown, "
    "NOT grey-brown drift). "
    "Hair = FULL thick messy wavy chestnut-brown covering the ENTIRE crown — young boy "
    "with a complete head of hair like the character sheet (tufts on top visible). "
    "NO bald spot, NO tonsure, NO monk ring, NO male-pattern baldness, NO shiny bare "
    "scalp on top when seen from behind or above. BARE HEAD (no hat) with FULL hair. "
    "Glasses = round gold or thin dark wire-rim. "
    "Coat = house DARK TEAL / blue-green trenchcoat (same hue as sheet/Germs/P03 — "
    "NOT bright cyan, NOT mint, NOT olive, NOT navy). "
    "Underlayers = tan/mustard vest, white shirt, brown tie/cravat. "
    "Same young-boy face proportions as the locked sheet — NOT an older/bald man."
)

HAT_LOCK = (
    "CRITICAL EVERY FRAME: NO HAT. NO helmet. NO pith helmet. NO safari hat. NO cap. "
    "NO hood. NO beanie. NO dome. NO brim. NO head covering of ANY colour (teal, tan, "
    "beige, brown, cream). The Explorer's head stays BARE for the ENTIRE 8 seconds — "
    "FULL messy wavy chestnut-brown hair covering the crown from start to end, "
    "including when he turns, steps back, or is seen from behind. Never grow or spawn "
    "a hat mid-clip. Never strip the crown bald mid-clip. "
    "HARD REJECT any dome/brim/helmet OR bald-crown/tonsure appearing even for one frame."
)

REJECT = (
    "HARD REJECT: ANY hat/helmet/pith/cap/hood; bald crown / tonsure / ring-hair only; "
    "older bald Explorer; darkened/deep-brown skin drift; "
    "bright cyan or mint or olive coat; off-model Explorer cousin; "
    "any window showing exterior; flat navy/blue rectangular sky overlays; pasted sky boxes; "
    "hard fills of any colour; brown scrub panels; heal panels; unblended coloured "
    "rectangles covering half the frame; peaked roofs; gables; chimneys; town "
    "silhouette; skyline; horizon band with buildings; model-town; village; "
    "glowing yellow house windows outdoors; dark triangular roof shapes in lower "
    "window panes; Ken Burns only; Orbit robot; photoreal; layout reset away from "
    "desk DNA; Explorer face-hero close-up; Explorer filling the frame; twins; "
    "academic blazer instead of teal trenchcoat; teaching/presenting-to-camera pose."
)

DESK_PROP_LOCK = (
    "Leather-bound books stay with PLAIN leather tops OR blank cream cards — "
    "continuous 3D books, NOT a flat brown panel. ZERO house silhouettes on props."
)

WINDOW_LOCK = (
    "NO WINDOW in frame. Behind the desk is a solid warm wooden panelled wall "
    "and/or filled bookcase only — fully indoor night study lit by the desk lamp. "
    "ZERO exterior view, ZERO sky, ZERO moon-through-glass, ZERO glass panes "
    "showing outdoors, ZERO flat navy/blue sky rectangles, ZERO pasted sky boxes, "
    "ZERO hard fills, ZERO heal panels, ZERO rooftops, ZERO chimneys, ZERO town "
    "silhouette, ZERO skyline. The background wall stays continuous wood/books."
)

EXPLORER_GARNISH_LOCK = (
    "HOUSE SCALE LOCK (match History of Science P01/P03 keep stills): Explorer is a "
    "TINY toy-scale teal GARNISH in the wide desk scene — a small figurine on the "
    "desktop, about the height of a short stack of cream cards. He MUST occupy under "
    "~20% of frame height and under ~15% of frame width. Wide shot of the desk; "
    "Explorer is a small accent, NEVER a medium portrait. Prefer PROFILE or "
    "OVER-THE-SHOULDER from behind/side. HARD REJECT face-to-camera, teaching pose, "
    "waist-up hero framing, close-up face, or Explorer filling the middle of the frame."
)

PROMPTS = {
    "06_explorer_leaves_gap": (
        "Image-to-video from the attached start frame (identity lock). Keep the SAME "
        "toy-scale garnish composition: exactly ONE Explorer boy matching the locked "
        "History of Science DNA. "
        f"{HAT_LOCK} {COLOUR_DNA_LOCK} "
        "He stays a small teal figurine on the honey-wood chemist desk. Beat: he pins "
        "one cream card into a vertical card column, leaves a glowing vacant seat/gap "
        "in the column, then steps back. Continuous acting + gentle camera drift the "
        "whole clip — no Ken Burns still. Fully indoor wood panelled wall / filled "
        "bookcase behind the desk. "
        f"{EXPLORER_GARNISH_LOCK} {WINDOW_LOCK} {DESK_PROP_LOCK} "
        "Silent. HARD REJECT: hat, bald crown/tonsure, darkened skin, wrong coat hue, "
        "face-hero, giant Explorer, twins, window, exterior sky, navy sky boxes, roofs, "
        "model-town. "
        + REJECT + " " + STYLE
    ),
}

REQUIRED_FLOW_EMAIL = "benoats@googlemail.com"
ALLOWED_FLOW_EMAILS = {REQUIRED_FLOW_EMAIL, "benoats@gmail.com"}
FORBIDDEN_FLOW_EMAIL = "benoats86@gmail.com"

CREATE_DIE_MARKERS = (
    "out of google flow credits",
    "reached your credit or daily limit",
    "you're out of google flow credits",
    "create failed",
    "generation failed",
    "could not create",
    "not been charged",
)

DEFAULT_ONLY = ("06_explorer_leaves_gap",)
ALLOWED_ONLY = set(DEFAULT_ONLY)


def dest_for(plate_id: str) -> Path:
    return RAW / f"{plate_id}_v09.mp4"


def resolve_start_frame() -> Path:
    """Hat-free on-colour start. Prefer dedicated hatfree ref; never FAIL hat stills."""
    for cand in (START_FRAME_PREF, START_FRAME_06):
        if cand.exists() and cand.stat().st_size > 20_000:
            return cand
    raise SystemExit(
        f"STOP: missing hat-free start frame ({START_FRAME_PREF} or {START_FRAME_06})"
    )


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
        f"BLOCKED_AUTH: account chooser open but {REQUIRED_FLOW_EMAIL} not listed. "
        "Ben must sign Mini Flow himself (never paste passwords)."
    )


def require_flow_account(page) -> str:
    try:
        labels = page.eval_on_selector_all(
            "button, a, [role=button]",
            "els => els.map(e => (e.getAttribute('aria-label') || e.innerText || '').trim())"
            ".filter(Boolean)",
        )
    except Exception as exc:
        raise SystemExit(
            f"BLOCKED_AUTH: could not read Flow account chrome ({exc})."
        ) from exc
    blob = "\n".join(labels)
    emails = {
        e.lower()
        for e in re.findall(r"[A-Za-z0-9._%+-]+@(?:gmail|googlemail)\.com", blob, flags=re.I)
    }
    active = None
    m = re.search(
        r"Google Account:[^\n\(]*\(([^)]+@(?:gmail|googlemail)\.com)\)",
        blob,
        re.I,
    )
    if m:
        active = m.group(1).lower()
    elif FORBIDDEN_FLOW_EMAIL in emails:
        active = FORBIDDEN_FLOW_EMAIL
    elif emails & ALLOWED_FLOW_EMAILS:
        active = sorted(emails & ALLOWED_FLOW_EMAILS)[0]
    elif emails:
        active = sorted(emails)[0]

    print(f"  Flow account probe emails={sorted(emails)} active={active}", flush=True)
    print(f"  page.url={page.url}", flush=True)
    if not active:
        raise SystemExit("BLOCKED_AUTH: signed-in Google email not visible on Flow.")
    if active == FORBIDDEN_FLOW_EMAIL or "benoats86" in active:
        raise SystemExit(
            f"BLOCKED_AUTH: Mini Flow is signed in as {active}. "
            f"Need exactly {REQUIRED_FLOW_EMAIL} on /u/1/. No mint."
        )
    if active not in ALLOWED_FLOW_EMAILS:
        raise SystemExit(
            f"BLOCKED_AUTH: unexpected Flow account {active}. Need {REQUIRED_FLOW_EMAIL}."
        )
    return active


def probe_credits(page) -> str:
    try:
        body = (page.inner_text("body") or "")
    except Exception as exc:
        return f"credits_probe_error:{exc}"
    low = body.lower()
    for marker in CREATE_DIE_MARKERS:
        if marker in low:
            raise SystemExit(
                f"STOP BLOCKED: Create/credits death visible BEFORE mint ({marker}). "
                "No Ken Burns. No hard fills. No Omni Flash substitute."
            )
    hits = []
    for pat in (
        r"\d[\d,]*\+?\s*credits?",
        r"credits?\s*[:=]?\s*\d[\d,]*",
        r"ultra",
        r"daily limit",
    ):
        for m in re.finditer(pat, body, flags=re.I):
            hits.append(m.group(0).strip()[:80])
            if len(hits) >= 8:
                break
        if len(hits) >= 8:
            break
    blob = " | ".join(dict.fromkeys(hits)) if hits else "no-credit-string-visible"
    print(f"  credits probe: {blob}", flush=True)
    return blob


def looks_like_create_death(exc: BaseException, page) -> str | None:
    msg = str(exc).lower()
    for marker in CREATE_DIE_MARKERS:
        if marker in msg:
            return marker
    try:
        body = (page.inner_text("body") or "").lower()
    except Exception:
        body = ""
    for marker in CREATE_DIE_MARKERS:
        if marker in body:
            return marker
    return None


def safe_close(ctx) -> None:
    if ctx is None:
        return
    try:
        ctx.close()
    except Exception:
        pass


def open_flow(p, *, profile: Path):
    last_err = "not started"
    for attempt in range(1, 4):
        ctx, page = flow.launch_context(p, headed=True, profile=profile)
        try:
            page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
            page.wait_for_timeout(3500)
            pick_google_account(page)
            flow.dismiss_banners(page)
            page.wait_for_timeout(1500)
            flow.dismiss_banners(page)
            if not flow.looks_logged_in(page):
                flow.settle_after_nav(page, wait_ms=2000)
                flow.dismiss_banners(page)
                page.wait_for_timeout(2000)
                if not flow.looks_logged_in(page):
                    page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
                    page.wait_for_timeout(3500)
                    pick_google_account(page)
                    flow.dismiss_banners(page)
                    page.wait_for_timeout(1500)
            if not flow.looks_logged_in(page):
                try:
                    active_probe = require_flow_account(page)
                    print(
                        f"  looks_logged_in=False but account chrome OK ({active_probe}) "
                        f"attempt={attempt}",
                        flush=True,
                    )
                    credits = probe_credits(page)
                    print(
                        f"  AUTH OK minting as {active_probe} via {flow.FLOW_HOME} "
                        f"credits={credits}",
                        flush=True,
                    )
                    return ctx, page, active_probe
                except SystemExit as exc:
                    last_err = str(exc)
                    safe_close(ctx)
                    print(f"  open_flow retry {attempt}/3: {last_err}", flush=True)
                    time.sleep(2)
                    continue
            active = require_flow_account(page)
            credits = probe_credits(page)
            print(
                f"  AUTH OK minting as {active} via {flow.FLOW_HOME} credits={credits}",
                flush=True,
            )
            return ctx, page, active
        except SystemExit:
            safe_close(ctx)
            raise
        except Exception as exc:
            last_err = str(exc)
            safe_close(ctx)
            print(f"  open_flow exception retry {attempt}/3: {last_err}", flush=True)
            time.sleep(2)
    raise SystemExit(
        f"BLOCKED_AUTH: Flow not logged in after retries ({last_err}). "
        "Do not Ken-Burns. Ben must sign Mini as benoats@googlemail.com on /u/1/."
    )


def run_force_download(dest: Path, project_url: str) -> None:
    project_url = (project_url or "").split("?")[0].rstrip("/")
    env = dict(os.environ)
    env["ORBIT_FLOW_HOME"] = flow.FLOW_HOME
    env["ORBIT_FLOW_PROFILE"] = str(PROFILE)
    cmd = [
        sys.executable, "-u", str(FORCE_DL),
        "--project", project_url,
        "--dest", str(dest),
    ]
    print(f"  spawn force-download: {' '.join(cmd)}", flush=True)
    subprocess.check_call(cmd, env=env)


def run_harvest(dest: Path, project_url: str, *, before_thumbs: int = -1) -> None:
    project_url = (project_url or "").split("?")[0].rstrip("/")
    if "flow.google.com" not in project_url or "/project/" not in project_url:
        raise SystemExit(
            f"STOP: refuse harvest — not a Flow project URL: {project_url!r}"
        )
    settle = int(os.environ.get("HOS_FLOW_HARVEST_SETTLE_S", "55"))
    wait_s = int(os.environ.get("HOS_FLOW_HARVEST_WAIT_S", "200"))
    print(f"  settle {settle}s then harvest wait_s={wait_s}", flush=True)
    time.sleep(settle)
    env = dict(os.environ)
    env["ORBIT_FLOW_HOME"] = flow.FLOW_HOME
    env["ORBIT_FLOW_PROFILE"] = str(PROFILE)
    cmd = [
        sys.executable, "-u", str(HARVEST),
        "--out", str(dest),
        "--project", project_url,
        "--wait-s", str(wait_s),
        "--before-thumbs", str(before_thumbs),
    ]
    print(f"  spawn harvest: {' '.join(cmd)}", flush=True)
    try:
        subprocess.check_call(cmd, env=env)
    except subprocess.CalledProcessError as exc:
        print(
            f"  gallery harvest failed ({exc.returncode}); "
            "falling back to Download-media force path",
            flush=True,
        )
        run_force_download(dest, project_url)


def probe_dur(path: Path) -> float:
    return float(
        subprocess.check_output(
            [
                "ffprobe", "-v", "error", "-show_entries", "format=duration",
                "-of", "default=nw=1:nk=1", str(path),
            ],
            text=True,
        ).strip()
    )


def extract_stills(clip: Path, dest_dir: Path, tag: str) -> list[Path]:
    dest_dir.mkdir(parents=True, exist_ok=True)
    outs: list[Path] = []
    dur = probe_dur(clip)
    times = [float(t) for t in range(0, 9)]
    times = [min(t, max(0.0, dur - 0.08)) for t in times]
    seen: set[float] = set()
    uniq: list[float] = []
    for t in times:
        key = round(t, 2)
        if key in seen:
            continue
        seen.add(key)
        uniq.append(t)
    for i, t in enumerate(uniq):
        out = dest_dir / f"{tag}_t{i}.jpg"
        subprocess.run(
            [
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-ss", f"{t:.3f}", "-i", str(clip),
                "-frames:v", "1", "-q:v", "2", str(out),
            ],
            check=True,
        )
        outs.append(out)
    return outs


def hard_fill_or_roof_suspect_score(still: Path) -> dict:
    im = Image.open(still).convert("RGB")
    w, h = im.size
    pix = im.load()
    x0, x1 = int(w * 0.05), int(w * 0.98)
    y0, y1 = 0, int(h * 0.58)
    navy_flat = 0
    warm_window = 0
    dark_sil = 0
    total = 0
    navy_lums: list[float] = []
    for y in range(y0, y1, 2):
        for x in range(x0, x1, 2):
            r, g, b = pix[x, y]
            total += 1
            if r > 95 and g > 60 and b < 95 and (r - b) > 28:
                continue
            lum = (r + g + b) / 3.0
            if b > 70 and b > r + 22 and b > g + 15 and r < 95 and g < 100 and 40 < lum < 130:
                navy_flat += 1
                navy_lums.append(lum)
            if r > 160 and g > 110 and b < 90 and (r - b) > 70:
                warm_window += 1
            if lum < 55 and r < 70 and g < 70 and b < 90:
                dark_sil += 1
    navy_frac = (navy_flat / total) if total else 0.0
    warm_frac = (warm_window / total) if total else 0.0
    dark_frac = (dark_sil / total) if total else 0.0
    navy_var = 0.0
    if len(navy_lums) >= 40:
        mean = sum(navy_lums) / len(navy_lums)
        navy_var = sum((v - mean) ** 2 for v in navy_lums) / len(navy_lums)
    box = im.crop((int(w * 0.18), int(h * 0.02), int(w * 0.92), int(h * 0.48)))
    bp = list(box.getdata())
    bn = len(bp) or 1
    box_navy = [
        px for px in bp
        if px[2] > 70 and px[2] > px[0] + 22 and px[2] > px[1] + 15 and px[0] < 95 and px[1] < 100
    ]
    box_navy_frac = len(box_navy) / bn
    if box_navy:
        bm = sum(sum(px) / 3.0 for px in box_navy) / len(box_navy)
        box_var = sum((sum(px) / 3.0 - bm) ** 2 for px in box_navy) / len(box_navy)
    else:
        box_var = 999.0
    hard_fill = (box_navy_frac >= 0.42 and box_var < 180.0) or (
        navy_frac >= 0.28 and navy_var < 120.0
    )
    roof_town = (warm_frac >= 0.0025) or (dark_frac >= 0.16 and navy_frac >= 0.035)
    suspect = hard_fill or roof_town
    return {
        "still": str(still),
        "navy_frac": round(navy_frac, 4),
        "warm_frac": round(warm_frac, 4),
        "dark_frac": round(dark_frac, 4),
        "navy_var": round(navy_var, 2),
        "box_navy_frac": round(box_navy_frac, 4),
        "box_var": round(box_var, 2),
        "hard_fill": hard_fill,
        "roof_town": roof_town,
        "suspect": suspect,
    }


def _teal_mask_pts(im: Image.Image) -> tuple[list[int], list[int]]:
    w, h = im.size
    px = im.load()
    xs, ys = [], []
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            r, g, b = px[x, y]
            # house dark teal / blue-green trenchcoat
            if 15 < r < 120 and 60 < g < 190 and 70 < b < 200 and b > r + 8 and g > r:
                xs.append(x)
                ys.append(y)
    return xs, ys


def explorer_face_hero_suspect(still: Path) -> dict:
    im = Image.open(still).convert("RGB")
    w, h = im.size
    xs, ys = _teal_mask_pts(im)
    if len(xs) < 40:
        return {
            "still": str(still), "teal_px": len(xs), "h_frac": 0.0,
            "face_hero": False, "reason": "little_teal",
        }
    bw = max(xs) - min(xs)
    bh = max(ys) - min(ys)
    h_frac = bh / float(h)
    w_frac = bw / float(w)
    face_hero = h_frac >= 0.42 or (h_frac >= 0.34 and w_frac >= 0.28 and len(xs) > 1800)
    return {
        "still": str(still),
        "teal_px": len(xs),
        "h_frac": round(h_frac, 3),
        "w_frac": round(w_frac, 3),
        "face_hero": face_hero,
        "reason": "tall_teal_cluster" if face_hero else "ok",
    }


def explorer_hat_suspect(still: Path) -> dict:
    """Reject teal/beige pith helmet dome above hair on the Explorer cluster."""
    im = Image.open(still).convert("RGB")
    w, h = im.size
    px = im.load()
    xs, ys = _teal_mask_pts(im)
    if len(xs) < 30:
        return {
            "still": str(still), "hat": False, "reason": "little_teal",
            "hat_px": 0, "teal_px": len(xs),
        }
    x0, x1 = min(xs), max(xs)
    y0, y1 = min(ys), max(ys)
    # Band just above teal coat cluster (where a pith brim/dome would sit)
    band_y0 = max(0, y0 - int(0.12 * h))
    band_y1 = max(band_y0 + 2, y0 + int(0.08 * (y1 - y0 + 1)))
    hat_px = 0
    hair_px = 0
    total = 0
    for y in range(band_y0, band_y1, 1):
        for x in range(x0, x1 + 1, 1):
            r, g, b = px[x, y]
            total += 1
            # teal/olive dome (hat) — saturated cool-green above head
            if 20 < r < 140 and 70 < g < 200 and 60 < b < 190 and (g > r + 15) and (b > r):
                hat_px += 1
            # chestnut hair (good)
            if 40 < r < 140 and 25 < g < 100 and 15 < b < 80 and r > g + 8 and r > b + 15:
                hair_px += 1
    hat_frac = hat_px / float(total or 1)
    # Strong teal mass above coat + little hair → pith helmet tell
    hat = hat_frac >= 0.12 and hat_px >= 80 and hair_px < hat_px * 0.55
    return {
        "still": str(still),
        "hat": hat,
        "hat_px": hat_px,
        "hair_px": hair_px,
        "hat_frac": round(hat_frac, 4),
        "teal_px": len(xs),
        "reason": "teal_dome_above_head" if hat else "ok",
    }


def explorer_colour_suspect(still: Path) -> dict:
    """Reject darkened skin and bright-cyan/mint coat drift vs house DNA."""
    im = Image.open(still).convert("RGB")
    w, h = im.size
    px = im.load()
    xs, ys = _teal_mask_pts(im)
    if len(xs) < 30:
        return {
            "still": str(still), "colour_bad": False, "reason": "little_teal",
            "skin_mean": None, "coat_hue_ok": None,
        }
    x0, x1 = min(xs), max(xs)
    y0, y1 = min(ys), max(ys)
    # Face/skin band: upper third of teal bbox, exclude strong teal
    face_y0 = y0
    face_y1 = y0 + max(4, int(0.35 * (y1 - y0 + 1)))
    skins: list[tuple[int, int, int]] = []
    coat_samples: list[tuple[int, int, int]] = []
    for y in range(face_y0, face_y1, 1):
        for x in range(x0, x1 + 1, 2):
            r, g, b = px[x, y]
            # skip teal coat / dark glasses
            if b > r + 8 and g > r and 60 < g < 200:
                continue
            lum = (r + g + b) / 3.0
            # warm fair skin candidate
            if 70 < lum < 220 and r > 90 and g > 60 and b > 40 and r >= g - 5 and r > b + 5:
                skins.append((r, g, b))
    for y in range(y0, y1 + 1, 2):
        for x in range(x0, x1 + 1, 2):
            r, g, b = px[x, y]
            if 15 < r < 120 and 60 < g < 190 and 70 < b < 200 and b > r + 8 and g > r:
                coat_samples.append((r, g, b))
    skin_mean = None
    skin_dark = False
    if skins:
        sr = sum(p[0] for p in skins) / len(skins)
        sg = sum(p[1] for p in skins) / len(skins)
        sb = sum(p[2] for p in skins) / len(skins)
        skin_mean = [round(sr, 1), round(sg, 1), round(sb, 1)]
        # v08 FAIL deep-brown drift: low luminance brown face
        skin_dark = (sr + sg + sb) / 3.0 < 95 or (sr < 110 and sg < 85 and sb < 70)
    # Coat hue: house dark teal has g≈b band, not bright cyan (b>>g) or mint (g>>b+30)
    coat_hue_ok = True
    cyan_mint = False
    if coat_samples:
        cr = sum(p[0] for p in coat_samples) / len(coat_samples)
        cg = sum(p[1] for p in coat_samples) / len(coat_samples)
        cb = sum(p[2] for p in coat_samples) / len(coat_samples)
        # bright cyan: high blue vs green; mint: green much higher than blue
        if cb > cg + 35 and cb > 140:
            cyan_mint = True
            coat_hue_ok = False
        if cg > cb + 40 and cg > 150:
            cyan_mint = True
            coat_hue_ok = False
        # olive drift: green high, blue low
        if cg > 120 and cb < 90 and cr < 100:
            coat_hue_ok = False
        _ = (cr, cg, cb)
    colour_bad = skin_dark or (not coat_hue_ok)
    reason = "ok"
    if skin_dark and cyan_mint:
        reason = "dark_skin+cyan_mint_coat"
    elif skin_dark:
        reason = "dark_skin_drift"
    elif not coat_hue_ok:
        reason = "coat_hue_drift"
    return {
        "still": str(still),
        "colour_bad": colour_bad,
        "skin_mean": skin_mean,
        "skin_samples": len(skins),
        "skin_dark": skin_dark,
        "coat_hue_ok": coat_hue_ok,
        "coat_samples": len(coat_samples),
        "reason": reason,
    }


def still_check_garnish(clip: Path, tag: str) -> dict:
    stills = extract_stills(clip, QA_STILLS, tag)
    scores = [explorer_face_hero_suspect(p) for p in stills]
    heroes = [s for s in scores if s["face_hero"]]
    report = {
        "tag": tag,
        "clip": str(clip),
        "stills": [str(p) for p in stills],
        "scores": scores,
        "face_hero_count": len(heroes),
        "face_hero": len(heroes) >= 2,
        "max_h_frac": max((s["h_frac"] for s in scores), default=0.0),
    }
    (QA_STILLS / f"{tag}_garnish_check.json").write_text(json.dumps(report, indent=2) + "\n")
    print(
        f"  garnish-check {tag}: face_hero_frames={len(heroes)}/9 "
        f"max_h_frac={report['max_h_frac']} reject={report['face_hero']}",
        flush=True,
    )
    return report


def still_check_hat_colour(clip: Path, tag: str) -> dict:
    stills = extract_stills(clip, QA_STILLS, tag)
    hats = [explorer_hat_suspect(p) for p in stills]
    colours = [explorer_colour_suspect(p) for p in stills]
    hat_hits = [s for s in hats if s["hat"]]
    colour_hits = [s for s in colours if s["colour_bad"]]
    report = {
        "tag": tag,
        "clip": str(clip),
        "stills": [str(p) for p in stills],
        "hat_scores": hats,
        "colour_scores": colours,
        "hat_count": len(hat_hits),
        "colour_bad_count": len(colour_hits),
        "hat_reject": len(hat_hits) >= 2,
        "colour_reject": len(colour_hits) >= 2,
        "reject": len(hat_hits) >= 2 or len(colour_hits) >= 2,
    }
    (QA_STILLS / f"{tag}_hat_colour_check.json").write_text(
        json.dumps(report, indent=2) + "\n"
    )
    print(
        f"  hat/colour-check {tag}: hat_frames={len(hat_hits)}/9 "
        f"colour_bad={len(colour_hits)}/9 reject={report['reject']}",
        flush=True,
    )
    return report


def still_check_roofs(clip: Path, tag: str) -> dict:
    stills = extract_stills(clip, QA_STILLS, tag)
    scores = [hard_fill_or_roof_suspect_score(p) for p in stills]
    suspects = [s for s in scores if s["suspect"]]
    hard_fills = [s for s in scores if s.get("hard_fill")]
    roofs = [s for s in scores if s.get("roof_town")]
    report = {
        "tag": tag,
        "clip": str(clip),
        "stills": [str(p) for p in stills],
        "scores": scores,
        "suspect_count": len(suspects),
        "hard_fill_count": len(hard_fills),
        "roof_count": len(roofs),
        "roof_readable": len(suspects) >= 2,
        "hard_fill_or_roof": len(suspects) >= 2,
        "window_or_roof_readable": len(suspects) >= 2,
    }
    (QA_STILLS / f"{tag}_sky_check.json").write_text(json.dumps(report, indent=2) + "\n")
    print(
        f"  still-check {tag}: suspect={len(suspects)}/9 "
        f"hard_fill={len(hard_fills)} roof={len(roofs)} "
        f"reject={report['hard_fill_or_roof']}",
        flush=True,
    )
    return report


def _truthy(name: str) -> bool:
    return os.environ.get(name, "").strip().lower() in {"1", "true", "yes", "on"}


def mint_one_create(page, prompt: str, tmp: Path, start_frame: Path | None = None) -> dict:
    info = flow.generate_clip(
        page,
        prompt,
        tmp,
        model=MODEL,
        start_frame=start_frame,
        scenery_only=(start_frame is None),
        reuse_project=False,
        attempts=1,
        timeout_s=180,
    )
    return info


def main() -> None:
    # v09 default = I2V from hat-free on-colour start (identity lock).
    # Fallback T2V only if HOS_FLOW_T2V_ONLY=1.
    if not _truthy("HOS_FLOW_T2V_ONLY") and not _truthy("HOS_FLOW_I2V_FIRST"):
        os.environ["HOS_FLOW_I2V_FIRST"] = "1"
        print("  v09 default: I2V hat-free colour DNA start", flush=True)

    raw_argv = sys.argv[1:]
    if "--probe-auth" in raw_argv:
        profile = flow.profile_path(PROFILE)
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            ctx, page, active = open_flow(p, profile=profile)
            print(f"PROBE_AUTH_OK account={active} home={flow.FLOW_HOME}", flush=True)
            safe_close(ctx)
        return

    argv = [a for a in raw_argv if not a.startswith("-")]
    only = set(argv) if argv else set(DEFAULT_ONLY)
    bad = only - ALLOWED_ONLY
    if bad:
        raise SystemExit(f"STOP: refuse remint via v09: {sorted(bad)}")

    plates = json.loads(PLATES_JSON.read_text())["plates"]
    order = [pid for pid in DEFAULT_ONLY if pid in only]
    plates = [p for p in plates if p["id"] in only]
    plates.sort(key=lambda p: order.index(p["id"]))
    if not plates:
        raise SystemExit(f"STOP: no plates matched only={sorted(only)}")

    start06 = resolve_start_frame()
    # Promote preferred start to canonical v09 path for trail
    START_FRAME_06.parent.mkdir(parents=True, exist_ok=True)
    if start06.resolve() != START_FRAME_06.resolve():
        shutil.copy2(start06, START_FRAME_06)
        print(f"  promoted start → {START_FRAME_06.name}", flush=True)

    RAW.mkdir(parents=True, exist_ok=True)
    REJECTED.mkdir(parents=True, exist_ok=True)
    QA_STILLS.mkdir(parents=True, exist_ok=True)
    meta: dict = {
        "engine": "flow-ui",
        "model": MODEL,
        "flow_home": flow.FLOW_HOME,
        "raw": str(RAW),
        "continuity": "v09_explorer_hatfree_colour_dna",
        "parent_v08_sha": PARENT_V08_SHA,
        "start_frame_06": str(START_FRAME_06),
        "dna_refs": [str(DNA_SHEET), str(DNA_GERMS), str(DNA_P03)],
        "locks": ["NO_HAT", "fair_warm_skin", "dark_teal_coat", "toy_scale_garnish"],
        "max_creates": MAX_CREATES,
        "only": sorted(only),
        "plates": [],
        "tries": [],
    }
    if META.exists():
        try:
            prev = json.loads(META.read_text())
            meta["tries"] = prev.get("tries", [])
            meta["plates"] = prev.get("plates", [])
            meta["only"] = sorted(only)
        except Exception:
            pass
    by_id = {p["id"]: p for p in meta.get("plates", []) if "id" in p}

    profile = flow.profile_path(PROFILE)
    print(
        f"Flow profile={profile} home={flow.FLOW_HOME} model={MODEL} "
        f"partial remint only={order} max_creates={MAX_CREATES}",
        flush=True,
    )
    print(f"  start_frame={START_FRAME_06}", flush=True)
    print(f"  HAT_LOCK + COLOUR_DNA_LOCK armed", flush=True)

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        ctx, page, active = open_flow(p, profile=profile)
        meta["flow_account"] = active
        meta["flow_home"] = flow.FLOW_HOME
        try:
            for i, plate in enumerate(plates):
                pid = plate["id"]
                dest = dest_for(pid)
                force = _truthy("HOS_FLOW_FORCE_REMINT")
                if veo.already_done(dest, min_bytes=400_000) and not force:
                    try:
                        dur = probe_dur(dest)
                    except Exception:
                        dur = 0.0
                    if 5.0 <= dur <= 40.0:
                        check = still_check_roofs(dest, f"{pid}_existing")
                        gcheck = still_check_garnish(dest, f"{pid}_existing")
                        hcheck = still_check_hat_colour(dest, f"{pid}_existing")
                        if (
                            not check["roof_readable"]
                            and not gcheck.get("face_hero")
                            and not hcheck.get("reject")
                        ):
                            print(
                                f"  skip {dest.name} dur={dur:.2f} "
                                "sky_clear hatfree colour_ok",
                                flush=True,
                            )
                            by_id[pid] = {
                                "id": pid,
                                "status": by_id.get(pid, {}).get("status", "exists"),
                                "out": str(dest),
                                "duration": dur,
                                "roof_check": check,
                                "hat_colour_check": hcheck,
                            }
                            continue
                        print(
                            f"  existing {dest.name} fails hat/colour/roof — remint",
                            flush=True,
                        )
                        dest.unlink(missing_ok=True)
                    else:
                        print(f"  re-mint bad existing {dest.name} dur={dur:.2f}", flush=True)
                        dest.unlink(missing_ok=True)
                elif dest.exists() and force:
                    print(f"  force remint — removing {dest.name}", flush=True)
                    dest.unlink(missing_ok=True)

                accepted = False
                last_err: Exception | None = None
                submitted = 0
                attempt_n = 0
                while submitted < max(1, MAX_CREATES - CREATE_OFFSET) and attempt_n < 8:
                    attempt_n += 1
                    create_n = CREATE_OFFSET + submitted + 1
                    print(
                        f"\n=== Fast I2V {pid} Create {create_n}/{MAX_CREATES} "
                        f"(submitted={submitted} attempt={attempt_n}) ({i+1}/{len(plates)}) ===",
                        flush=True,
                    )
                    try:
                        _ = page.url
                    except Exception:
                        print("  page dead — relaunching", flush=True)
                        safe_close(ctx)
                        ctx, page, active = open_flow(p, profile=profile)

                    tmp = dest.with_suffix(f".try{create_n}.tmp.mp4")
                    tmp.unlink(missing_ok=True)
                    info = None
                    use_i2v = _truthy("HOS_FLOW_I2V_FIRST") and not _truthy(
                        "HOS_FLOW_T2V_ONLY"
                    )
                    try:
                        start = START_FRAME_06 if (pid == "06_explorer_leaves_gap" and use_i2v) else None
                        if start is not None and not start.exists():
                            raise SystemExit(f"STOP: missing start frame {start}")
                        if start is not None:
                            print(f"  start-frame I2V: {start}", flush=True)
                        else:
                            print("  mode: T2V (HOS_FLOW_T2V_ONLY) — colour+hat in prompt", flush=True)
                        info = mint_one_create(page, PROMPTS[pid], tmp, start_frame=start)
                    except Exception as e:
                        last_err = e
                        import traceback
                        print(f"  Create pre-submit exception:\n{traceback.format_exc()}", flush=True)
                        death = looks_like_create_death(e, page)
                        meta.setdefault("tries", []).append(
                            {
                                "id": pid,
                                "create": create_n,
                                "status": "fail_pre_submit",
                                "error": str(e)[:500],
                                "create_death": death,
                            }
                        )
                        META.write_text(json.dumps(meta, indent=2))
                        if death:
                            raise SystemExit(
                                f"STOP BLOCKED: Create died on {pid} ({death}). "
                                "No Ken Burns. No hard fills. No Omni Flash substitute."
                            ) from e
                        # I2V attach flake → one T2V retry without burning if never submitted
                        if use_i2v and attempt_n == 1:
                            print("  I2V pre-submit flake — will retry; if persists try T2V", flush=True)
                        print(
                            f"  Create pre-submit failed (does not burn budget): {e}",
                            flush=True,
                        )
                        continue
                    submitted += 1

                    if info.get("needs_gallery_harvest"):
                        candidates = [
                            info.get("project_url") or "",
                            info.get("url") or "",
                            page.url or "",
                        ]
                        project_url = ""
                        for cand in candidates:
                            cand = (cand or "").split("?")[0].rstrip("/")
                            if "flow.google.com" in cand and "/project/" in cand:
                                project_url = cand
                                break
                        if not project_url:
                            raise SystemExit(
                                f"STOP: no Flow project URL for harvest on {pid}; "
                                f"candidates={candidates!r}"
                            )
                        print(
                            f"  closing mint browser for harvest… project={project_url}",
                            flush=True,
                        )
                        safe_close(ctx)
                        ctx = None
                        page = None
                        run_harvest(tmp, project_url, before_thumbs=-1)
                        ctx, page, active = open_flow(p, profile=profile)
                        info["media_id"] = (
                            f"gallery-harvest:{tmp.stat().st_size if tmp.exists() else 0}"
                        )
                        info["bytes"] = tmp.stat().st_size if tmp.exists() else 0

                    if not tmp.exists() or tmp.stat().st_size < 400_000:
                        print(f"  Create {create_n}: download missing/small {tmp}", flush=True)
                        continue
                    veo.strip_audio(tmp)
                    try:
                        dur = probe_dur(tmp)
                    except Exception as e:
                        print(f"  Create {create_n}: unreadable {tmp}: {e}", flush=True)
                        continue
                    if dur < 5.0 or dur > 40.0:
                        bad = REJECTED / f"{pid}_bad_dur_{dur:.1f}_try{create_n}.mp4"
                        shutil.move(str(tmp), str(bad))
                        print(f"  Create {create_n}: bad duration → {bad}", flush=True)
                        continue

                    tag = f"{pid}_try{create_n}"
                    check = still_check_roofs(tmp, tag)
                    gcheck = still_check_garnish(tmp, tag)
                    hcheck = still_check_hat_colour(tmp, tag)
                    try_rec = {
                        "id": pid,
                        "create": create_n,
                        "status": "ok_pending_qa",
                        "out_tmp": str(tmp),
                        "duration": dur,
                        "bytes": tmp.stat().st_size,
                        "roof_check": {
                            "suspect_count": check["suspect_count"],
                            "roof_readable": check["roof_readable"],
                        },
                        "hat_colour": {
                            "hat_count": hcheck["hat_count"],
                            "colour_bad_count": hcheck["colour_bad_count"],
                            "reject": hcheck["reject"],
                        },
                        "face_hero": gcheck.get("face_hero"),
                        **{k: v for k, v in info.items() if k != "needs_gallery_harvest"},
                    }
                    meta.setdefault("tries", []).append(try_rec)
                    META.write_text(json.dumps(meta, indent=2))

                    reject_reasons = []
                    if check["roof_readable"]:
                        reject_reasons.append("hardfill_or_roof")
                    if gcheck.get("face_hero"):
                        reject_reasons.append("face_hero")
                    if hcheck.get("hat_reject"):
                        reject_reasons.append("hat")
                    if hcheck.get("colour_reject"):
                        reject_reasons.append("colour_dna")

                    if reject_reasons:
                        rej = REJECTED / f"{pid}_v09_try{create_n}_{'+'.join(reject_reasons)}.mp4"
                        if rej.exists():
                            rej.unlink()
                        shutil.move(str(tmp), str(rej))
                        print(
                            f"  REJECT Create {create_n}: {reject_reasons} → {rej.name}",
                            flush=True,
                        )
                        continue

                    if dest.exists():
                        dest.unlink()
                    shutil.move(str(tmp), str(dest))
                    by_id[pid] = {
                        "id": pid,
                        "status": "ok",
                        "out": str(dest),
                        "duration": dur,
                        "kind": "I2V" if use_i2v else "T2V",
                        "create_try": create_n,
                        "roof_check": check,
                        "hat_colour_check": hcheck,
                        **{k: v for k, v in info.items() if k != "needs_gallery_harvest"},
                    }
                    meta["plates"] = list(by_id.values())
                    meta["accepted_try"] = create_n
                    META.write_text(json.dumps(meta, indent=2))
                    print(
                        f"  SAVED {dest.name} bytes={dest.stat().st_size} dur={dur:.2f} "
                        f"try={create_n} hatfree_colour_ok",
                        flush=True,
                    )
                    accepted = True
                    break

                if not accepted:
                    by_id[pid] = {
                        "id": pid,
                        "status": "fail_qa_or_create",
                        "error": str(last_err)[:500] if last_err else "hat/colour/roof after max Creates",
                        "tries": MAX_CREATES,
                        "submitted_creates": submitted,
                    }
                    meta["plates"] = list(by_id.values())
                    meta.setdefault("failed_plates", []).append(pid)
                    META.write_text(json.dumps(meta, indent=2))
                    print(
                        f"FAIL: {pid} after {submitted} submitted Creates "
                        f"(max {MAX_CREATES}). No land. Report to CoS.",
                        flush=True,
                    )
                    continue
        finally:
            safe_close(ctx)

    ok = sum(1 for p in by_id.values() if p.get("status") in {"ok", "exists"})
    want = len(plates)
    print(f"OK part 04 Flow mint v09 finished ok={ok} want={want}", flush=True)
    if ok < want:
        sys.exit(2)


if __name__ == "__main__":
    main()
