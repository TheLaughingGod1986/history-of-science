#!/usr/bin/env python3
"""Part 04 Flow Veo 3.1 Fast remint v07 — scrub hard navy sky fills.

Showrunner PART04_V07_SCRUB_HARD_SKY_FILLS.md (parent v06 sha 5aea09bd…):
  - REMINT: 05_columns_families, 06_explorer_leaves_gap, 09_risk_bet, 09b_risk_hold
  - KEEP: 02b desk-only (do NOT remint), Explorer teal on 06, Empty Chairs / VO / labels
  - FULL Veo 3.1 Fast — real window with night sky + moon IN-CAMERA
  - ZERO flat blue/navy boxes · ZERO town roofs/chimneys · ZERO hard fills / heal panels
  - Create dies → STOP. Max 2 Creates per plate.
  - Auth: benoats@googlemail.com on /u/1/. P01–P03 FROZEN.
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
RAW = PROJ / "04_Generated-Clips/part04/raw/v07_fast"
REJECTED = RAW / "_rejected"
QA_STILLS = PROJ / "07_Edit-Project/_qa_part04_v07_plate"
META = PROJ / "07_Edit-Project/part04_mint_flow_v07_meta.json"
HARVEST = Path(__file__).resolve().parent / "_harvest_newest_gallery_v01.py"
FORCE_DL = Path(__file__).resolve().parent / "_harvest_force_download_v01.py"
MODEL = os.environ.get("ORBIT_FLOW_VEO_MODEL", "Veo 3.1 - Fast")
PROFILE = Path(
    os.environ.get(
        "ORBIT_FLOW_PROFILE",
        str(Path.home() / ".playwright-hos-flow-profile"),
    )
)
MAX_CREATES = int(os.environ.get("HOS_V07_MAX_CREATES", "2"))
CREATE_OFFSET = int(os.environ.get("HOS_V07_CREATE_OFFSET", "0"))  # prior Creates already spent


STYLE = (
    "Animistry-class stylised 3D cartoon (NOT photoreal). "
    "ONE continuous 1869 chemist desk: honey wood desktop, soft warm lamp, cream "
    "blank cards, leather books, lab vessels. Continuous real camera/object motion "
    "the whole clip. Silent. No Orbit. No Ken Burns still. Opaque vessels preferred."
)

REJECT = (
    "HARD REJECT: flat navy/blue rectangular sky overlays; pasted sky boxes; "
    "hard fills of any colour; brown scrub panels; heal panels; unblended coloured "
    "rectangles covering half the frame; peaked roofs; chimneys; town silhouette; "
    "skyline; model-town; village; glowing yellow house windows outdoors; "
    "Ken Burns only; Orbit robot; photoreal; layout reset away from desk DNA."
)

DESK_PROP_LOCK = (
    "Leather-bound books stay with PLAIN leather tops OR blank cream cards — "
    "continuous 3D books, NOT a flat brown panel. ZERO house silhouettes on props."
)

WINDOW_LOCK = (
    "Lab window in frame must be a REAL wooden multi-pane window with true glass "
    "muntins. Through the panes: a CONTINUOUS deep night sky with ONE soft moon, "
    "soft clouds, and faint stars rendered IN-CAMERA as part of the 3D world — "
    "NOT a flat navy rectangle, NOT a pasted sky box, NOT a hard fill, NOT a heal "
    "panel. Exterior EMPTY of architecture — no rooftops, no chimneys, no "
    "model-town, no village silhouette, no glowing yellow street windows. "
    "Sky + moon + soft clouds + stars ONLY beyond the glass."
)

PROMPTS = {
    "05_columns_families": (
        "Text-to-video. ONE persistent 1869 chemist desk: honey wood, soft warm "
        "lamp, cream blank cards dropping into vertical family columns — cousins "
        "grouping. Continuous drop + settle motion. Behind the desk a real "
        "multi-pane night window with moon + soft clouds + stars in-camera. "
        f"{WINDOW_LOCK} {DESK_PROP_LOCK} "
        "Silent. No people. No Explorer. "
        + REJECT + " " + STYLE
    ),
    "06_explorer_leaves_gap": (
        "Text-to-video. ONE persistent 1869 chemist desk DNA. Exactly ONE Explorer "
        "boy — messy wavy brown hair, gold wire-rim glasses, TEAL trenchcoat "
        "overcoat (house lock, NOT academic blazer). He pins one cream card into "
        "a column, leaves a glowing vacant seat/gap, steps back. Continuous acting "
        "+ gentle camera. Behind him a real multi-pane night window with moon + "
        "soft clouds + stars in-camera. "
        f"{WINDOW_LOCK} {DESK_PROP_LOCK} "
        "Silent. HARD REJECT: twins, off-model Explorer, flat sky boxes. "
        + REJECT + " " + STYLE
    ),
    "09_risk_bet": (
        "Text-to-video. ONE persistent 1869 chemist desk with ONE glowing vacant "
        "wooden chair (Empty Chairs / A BET). Soft tension lighting. Continuous "
        "subtle camera drift + chair glow pulse. Real multi-pane night window "
        "behind with moon + soft clouds + stars in-camera. "
        f"{WINDOW_LOCK} {DESK_PROP_LOCK} "
        "Silent. No people. No Explorer. KEEP chair glow. "
        + REJECT + " " + STYLE
    ),
    "09b_risk_hold": (
        "Text-to-video. ONE persistent 1869 chemist desk; glowing vacant chair "
        "holds frame as hero. Continuous subtle hold / lamp warmth vs cooler night "
        "window. Real multi-pane night window with moon + soft clouds + stars "
        "in-camera. "
        f"{WINDOW_LOCK} {DESK_PROP_LOCK} "
        "Silent. No people. KEEP chair glow. "
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

DEFAULT_ONLY = ("05_columns_families", "06_explorer_leaves_gap", "09_risk_bet", "09b_risk_hold")
ALLOWED_ONLY = set(DEFAULT_ONLY)


def dest_for(plate_id: str) -> Path:
    return RAW / f"{plate_id}_v07.mp4"


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
    # Sheet: still-check every second ~0–8. Clamp last seek inside clip.
    times = [float(t) for t in range(0, 9)]
    times = [min(t, max(0.0, dur - 0.08)) for t in times]
    # de-dupe if clip shorter than 8s
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
    """Reject FLAT navy hard-fill rectangles and town-roof tells.

    Real in-camera night sky through a window is ALLOWED. Flat uniform navy
    boxes covering large upper regions are NOT. Gate assist only — agent still
    visually reviews stills before KEEP.
    """
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
    # Warm yellow outdoor windows OR a dark sill-band under cool sky (town tell)
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


def still_check_roofs(clip: Path, tag: str) -> dict:
    """Name kept for callers; now rejects window OR roof readable."""
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
        # ≥2 seconds with hard fill OR roof/town tell → reject
        "roof_readable": len(suspects) >= 2,
        "hard_fill_or_roof": len(suspects) >= 2,
        "window_or_roof_readable": len(suspects) >= 2,
    }
    (QA_STILLS / f"{tag}_sky_check.json").write_text(json.dumps(report, indent=2) + "\n")
    print(
        f"  still-check {tag}: suspect={len(suspects)}/9 "
        f"hard_fill={len(hard_fills)} roof={len(roofs)} "
        f"reject={report['hard_fill_or_roof']} "
        f"box_navy={[s.get('box_navy_frac') for s in scores]}",
        flush=True,
    )
    return report


def _truthy(name: str) -> bool:
    return os.environ.get(name, "").strip().lower() in {"1", "true", "yes", "on"}


def mint_one_create(page, prompt: str, tmp: Path) -> dict:
    """One Flow Create (attempts=1). Caller owns the max-2 retry loop."""
    info = flow.generate_clip(
        page,
        prompt,
        tmp,
        model=MODEL,
        start_frame=None,
        scenery_only=True,
        reuse_project=False,
        attempts=1,
        timeout_s=180,
    )
    return info


def main() -> None:
    # v07 window remint default = T2V (no I2V still that bakes a window).
    if not _truthy("HOS_FLOW_I2V_FIRST") and not _truthy("HOS_FLOW_T2V_ONLY"):
        os.environ["HOS_FLOW_T2V_ONLY"] = "1"
        print(
            "  v07 default: HOS_FLOW_T2V_ONLY=1 (real window in-camera; no hard-fill)",
            flush=True,
        )

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
        raise SystemExit(f"STOP: refuse remint via v07: {sorted(bad)}")

    plates = json.loads(PLATES_JSON.read_text())["plates"]
    order = [pid for pid in DEFAULT_ONLY if pid in only]
    plates = [p for p in plates if p["id"] in only]
    plates.sort(key=lambda p: order.index(p["id"]))
    if not plates:
        raise SystemExit(f"STOP: no plates matched only={sorted(only)}")

    RAW.mkdir(parents=True, exist_ok=True)
    REJECTED.mkdir(parents=True, exist_ok=True)
    QA_STILLS.mkdir(parents=True, exist_ok=True)
    meta: dict = {
        "engine": "flow-ui",
        "model": MODEL,
        "flow_home": flow.FLOW_HOME,
        "raw": str(RAW),
        "continuity": "v07_real_window_night_sky_moon_no_hard_fill",
        "parent_v06_sha": "5aea09bdc505beb4d887acdfcfc5c43b307ee0bb7c606bb287b4beeb56e5bbf2",
        "window_lock": (
            "real multi-pane window; night sky + moon + soft clouds + stars "
            "in-camera; NO flat navy boxes; NO town roofs/chimneys; NO hard fills"
        ),
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
    print(f"  WINDOW_LOCK head={WINDOW_LOCK[:120]}…", flush=True)

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
                        if not check["roof_readable"]:
                            print(f"  skip {dest.name} dur={dur:.2f} sky_clear_no_hard_fill", flush=True)
                            by_id[pid] = {
                                "id": pid,
                                "status": by_id.get(pid, {}).get("status", "exists"),
                                "out": str(dest),
                                "duration": dur,
                                "roof_check": check,
                            }
                            continue
                        print(
                            f"  existing {dest.name} still has hard-fill/roof — remint",
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
                # CREATE_OFFSET accounts for Creates already spent this scrub (e.g. try1 rejected).
                creates_this_run = max(1, MAX_CREATES - CREATE_OFFSET)
                for local_n in range(1, creates_this_run + 1):
                    create_n = CREATE_OFFSET + local_n
                    print(
                        f"\n=== Fast T2V {pid} Create {create_n}/{MAX_CREATES} "
                        f"(run {local_n}/{creates_this_run}) ({i+1}/{len(plates)}) ===",
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
                    try:
                        info = mint_one_create(page, PROMPTS[pid], tmp)
                    except Exception as e:
                        last_err = e
                        death = looks_like_create_death(e, page)
                        meta.setdefault("tries", []).append(
                            {
                                "id": pid,
                                "create": create_n,
                                "status": "fail",
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
                        print(f"  Create {create_n} failed: {e}", flush=True)
                        continue

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
                    try_rec = {
                        "id": pid,
                        "create": create_n,
                        "status": "ok_pending_roof" if check["roof_readable"] else "ok",
                        "out_tmp": str(tmp),
                        "duration": dur,
                        "bytes": tmp.stat().st_size,
                        "roof_check": {
                            "suspect_count": check["suspect_count"],
                            "roof_readable": check["roof_readable"],
                            "dark_fracs": [s["dark_frac"] for s in check["scores"]],
                        },
                        **{k: v for k, v in info.items() if k != "needs_gallery_harvest"},
                    }
                    meta.setdefault("tries", []).append(try_rec)
                    META.write_text(json.dumps(meta, indent=2))

                    if check["roof_readable"]:
                        rej = REJECTED / f"{pid}_v07_try{create_n}_hardfill_or_roof.mp4"
                        if rej.exists():
                            rej.unlink()
                        shutil.move(str(tmp), str(rej))
                        print(
                            f"  REJECT Create {create_n}: hard-fill/roof readable → {rej.name} "
                            f"(suspect_frames={check['suspect_count']})",
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
                        "kind": "T2V",
                        "create_try": create_n,
                        "roof_check": check,
                        **{k: v for k, v in info.items() if k != "needs_gallery_harvest"},
                    }
                    meta["plates"] = list(by_id.values())
                    meta["accepted_try"] = create_n
                    META.write_text(json.dumps(meta, indent=2))
                    print(
                        f"  SAVED {dest.name} bytes={dest.stat().st_size} dur={dur:.2f} "
                        f"try={create_n} sky_clear_no_hard_fill",
                        flush=True,
                    )
                    accepted = True
                    break

                if not accepted:
                    by_id[pid] = {
                        "id": pid,
                        "status": "fail_roofs_or_create",
                        "error": str(last_err)[:500] if last_err else "hard-fill/roof after max Creates",
                        "tries": MAX_CREATES,
                    }
                    meta["plates"] = list(by_id.values())
                    META.write_text(json.dumps(meta, indent=2))
                    raise SystemExit(
                        f"STOP: {pid} still has hard-fill/roof (window/roof or Create failed) after "
                        f"{MAX_CREATES} Creates. No hard-fill. Report to CoS."
                    )
        finally:
            safe_close(ctx)

    ok = sum(1 for p in by_id.values() if p.get("status") in {"ok", "exists"})
    want = len(plates)
    print(f"OK part 04 Flow mint v07 finished ok={ok} want={want}", flush=True)
    if ok < want:
        sys.exit(2)


if __name__ == "__main__":
    main()
