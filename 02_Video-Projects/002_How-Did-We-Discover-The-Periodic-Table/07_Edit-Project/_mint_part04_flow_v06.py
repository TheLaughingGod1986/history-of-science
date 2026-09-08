#!/usr/bin/env python3
"""Part 04 Flow Veo 3.1 Fast remint v06 — 02b ONLY (scrub in-camera window roofs).

Showrunner PART04_V06_SCRUB_02B_WINDOW_ROOFS.md (parent v05 sha a7c9741c…):
  - REMINT: 02b_cards_sixty_three ONLY (~18–21 peaked roofs + chimneys through window)
  - KEEP: brown scrub cleared · late window · night-sky ~40 · Explorer teal · Empty Chairs
  - FULL Veo 3.1 Fast. Create dies OR gallery fail → STOP.
  - NEVER hard fills / brown panels / flat sky rectangles.
  - Prompt MUST lock window = night sky + moon + clouds + stars ONLY.
  - Still-check every second ~0–8; reject+retry if roofs readable (max 2 Creates).
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
RAW = PROJ / "04_Generated-Clips/part04/raw/v06_fast"
REJECTED = RAW / "_rejected"
QA_STILLS = PROJ / "07_Edit-Project/_qa_part04_v06_plate"
META = PROJ / "07_Edit-Project/part04_mint_flow_v06_meta.json"
HARVEST = Path(__file__).resolve().parent / "_harvest_newest_gallery_v01.py"
FORCE_DL = Path(__file__).resolve().parent / "_harvest_force_download_v01.py"
MODEL = os.environ.get("ORBIT_FLOW_VEO_MODEL", "Veo 3.1 - Fast")
PROFILE = Path(
    os.environ.get(
        "ORBIT_FLOW_PROFILE",
        str(Path.home() / ".playwright-hos-flow-profile"),
    )
)
MAX_CREATES = 2

STYLE = (
    "Animistry-class stylised 3D cartoon (NOT photoreal). "
    "ONE continuous 1869 chemist desk: honey wood, soft warm lamp, cream blank "
    "cards, leather books, lab vessels, night window. Continuous real "
    "camera/object motion the whole clip. Silent. No Orbit. No Ken Burns still. "
    "Opaque vessels preferred."
)

REJECT = (
    "HARD REJECT: peaked roofs; chimneys; town silhouette; skyline; buildings; "
    "houses; rooftops on the sill; model-town; village silhouette; dark building "
    "shapes through the window; unblended brown scrub panels; flat rectangular "
    "leather overlays; hard rectangular fills of any colour; flat blue sky boxes "
    "/ pasted sky rectangles cutting across desk or cards; Ken Burns only; "
    "Orbit robot; photoreal; layout reset away from desk DNA."
)

DESK_PROP_LOCK = (
    "Show a NATURAL stack of leather-bound books with PLAIN leather tops OR blank "
    "cream cards on them — continuous 3D books in the scene, NOT a flat brown "
    "panel. ZERO house silhouettes, ZERO peaked roofs, ZERO chimneys, ZERO brown "
    "scrub masks, ZERO glowing yellow house tokens."
)

# Sheet lock — must appear verbatim in spirit in the mint prompt.
WINDOW_LOCK = (
    "Through the REAL wooden window panes: deep night sky + full moon + soft "
    "clouds + faint stars ONLY. Window = night sky + moon + clouds + stars ONLY. "
    "NO buildings, NO houses, NO peaked roofs, NO chimneys, NO town silhouette, "
    "NO skyline, NO rooftops on the sill, NO model-town. Completely EMPTY of "
    "architecture — clear open night sky filling every pane down to the sill. "
    "Rendered IN-CAMERA through real window panes — NOT a pasted flat sky "
    "rectangle or hard fill."
)

PROMPT_02B = (
    "IMAGE-TO-VIDEO from the attached start frame. KEEP this EXACT 1869 chemist "
    "desk DNA (honey wood, soft lamp, cream blank card stacks, lab vessels, "
    "leather books with PLAIN tops). Cream blank cards keep settling / gentle "
    "shuffle across the honey wood — denser stack as if counting known elements. "
    "Continuous card motion. Soft lamp. "
    f"{DESK_PROP_LOCK} {WINDOW_LOCK} "
    "Silent. No people. No Explorer. "
    + REJECT + " " + STYLE
)

T2V_02B = (
    "ONE continuous natural 1869 chemist desk shot with NO overlays: honey wood "
    "desk, soft warm brass lamp glowing, dense neat stack of cream blank cards "
    "gently flipping and settling as if counting sixty-three known elements, "
    "stack of thick brown leather-bound books with PLAIN clean tops (no house "
    "props, no house silhouettes, no brown scrub panel), pink/teal/orange lab "
    "flasks, white mortar. "
    f"{WINDOW_LOCK} "
    "Continuous gentle card shuffle and subtle camera drift. Silent. No "
    "people. No hands. No Explorer. "
    + STYLE + " " + REJECT + " " + DESK_PROP_LOCK
)

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

DEFAULT_ONLY = ("02b_cards_sixty_three",)
ALLOWED_ONLY = set(DEFAULT_ONLY)


def dest_for(plate_id: str) -> Path:
    return RAW / f"{plate_id}_v06.mp4"


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
                "No Ken Burns. No Omni Flash substitute."
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
    for t in range(0, 9):
        out = dest_dir / f"{tag}_t{t}.jpg"
        subprocess.run(
            [
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-ss", str(t), "-i", str(clip), "-frames:v", "1", str(out),
            ],
            check=True,
        )
        outs.append(out)
    return outs


def roof_suspect_score(still: Path) -> dict:
    """Heuristic: dark silhouette band in lower window panes against blue sky.

    Window glass on 02b desk shots is typically upper-centre. Dark peaked roofs
    read as very dark pixels under blue night sky. This is a gate assist — agent
    still visually reviews stills before KEEP.
    """
    im = Image.open(still).convert("RGB")
    w, h = im.size
    # Upper-centre window glass (avoid desk / lamp / books)
    x0, x1 = int(w * 0.18), int(w * 0.72)
    y0, y1 = int(h * 0.02), int(h * 0.48)
    pix = im.load()
    dark = 0
    blueish = 0
    total = 0
    # Lower third of that window box = sill / roof zone
    y_sill0 = y0 + int((y1 - y0) * 0.55)
    for y in range(y_sill0, y1):
        for x in range(x0, x1, 2):
            r, g, b = pix[x, y]
            total += 1
            # wood muntins are warm brown — skip
            if r > 90 and g > 55 and b < 80 and (r - b) > 30:
                continue
            if r < 55 and g < 55 and b < 70:
                dark += 1
            elif b > r + 15 and b > g + 5 and b > 70:
                blueish += 1
    dark_frac = (dark / total) if total else 0.0
    # Peaked roofs leave a meaningful dark fraction in the sill band.
    suspect = dark_frac >= 0.085
    return {
        "still": str(still),
        "dark": dark,
        "blueish": blueish,
        "total": total,
        "dark_frac": round(dark_frac, 4),
        "suspect": suspect,
    }


def still_check_roofs(clip: Path, tag: str) -> dict:
    stills = extract_stills(clip, QA_STILLS, tag)
    scores = [roof_suspect_score(p) for p in stills]
    suspects = [s for s in scores if s["suspect"]]
    report = {
        "tag": tag,
        "clip": str(clip),
        "stills": [str(p) for p in stills],
        "scores": scores,
        "suspect_count": len(suspects),
        "roof_readable": len(suspects) >= 2,  # ≥2 seconds with dark sill band
    }
    (QA_STILLS / f"{tag}_roof_check.json").write_text(json.dumps(report, indent=2) + "\n")
    print(
        f"  still-check {tag}: suspect_frames={len(suspects)}/9 "
        f"roof_readable={report['roof_readable']} "
        f"dark_fracs={[s['dark_frac'] for s in scores]}",
        flush=True,
    )
    return report


def _truthy(name: str) -> bool:
    return os.environ.get(name, "").strip().lower() in {"1", "true", "yes", "on"}


def mint_one_create(page, tmp: Path) -> dict:
    """One Flow Create (attempts=1). Caller owns the max-2 retry loop."""
    info = flow.generate_clip(
        page,
        T2V_02B,
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
    # v06 default = T2V with sky-only window lock (avoid I2V stills that bake roofs).
    if not _truthy("HOS_FLOW_I2V_FIRST") and not _truthy("HOS_FLOW_T2V_ONLY"):
        os.environ["HOS_FLOW_T2V_ONLY"] = "1"
        print(
            "  v06 default: HOS_FLOW_T2V_ONLY=1 (sky-only window; no hard-fill)",
            flush=True,
        )

    argv = [a for a in sys.argv[1:] if not a.startswith("-")]
    if argv == ["--probe-auth"]:
        profile = flow.profile_path(PROFILE)
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            ctx, page, active = open_flow(p, profile=profile)
            print(f"PROBE_AUTH_OK account={active} home={flow.FLOW_HOME}", flush=True)
            safe_close(ctx)
        return

    only = set(argv) if argv else set(DEFAULT_ONLY)
    bad = only - ALLOWED_ONLY
    if bad:
        raise SystemExit(f"STOP: refuse remint via v06: {sorted(bad)}")

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
        "continuity": "scrub_02b_window_roofs_v06_veo_no_hard_fill",
        "parent_v05_sha": "a7c9741c32f9689c019d5c8695b36a8e8d2bbbebfb19b93ee53b6d584b8a43fc",
        "window_lock": (
            "night sky + moon + clouds + stars ONLY; "
            "NO buildings/houses/peaked roofs/chimneys/town silhouette/skyline"
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
                            print(f"  skip {dest.name} dur={dur:.2f} roofs_clear", flush=True)
                            by_id[pid] = {
                                "id": pid,
                                "status": by_id.get(pid, {}).get("status", "exists"),
                                "out": str(dest),
                                "duration": dur,
                                "roof_check": check,
                            }
                            continue
                        print(
                            f"  existing {dest.name} still has roofs — remint",
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
                for create_n in range(1, MAX_CREATES + 1):
                    print(
                        f"\n=== Fast T2V {pid} Create {create_n}/{MAX_CREATES} "
                        f"({i+1}/{len(plates)}) ===",
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
                        info = mint_one_create(page, tmp)
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
                                "No Ken Burns. No Omni Flash substitute."
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
                        rej = REJECTED / f"{pid}_v06_try{create_n}_roofs.mp4"
                        if rej.exists():
                            rej.unlink()
                        shutil.move(str(tmp), str(rej))
                        print(
                            f"  REJECT Create {create_n}: roofs readable → {rej.name} "
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
                        f"try={create_n} roofs_clear",
                        flush=True,
                    )
                    accepted = True
                    break

                if not accepted:
                    by_id[pid] = {
                        "id": pid,
                        "status": "fail_roofs_or_create",
                        "error": str(last_err)[:500] if last_err else "roofs after max Creates",
                        "tries": MAX_CREATES,
                    }
                    meta["plates"] = list(by_id.values())
                    META.write_text(json.dumps(meta, indent=2))
                    raise SystemExit(
                        f"STOP: {pid} still has roofs (or Create failed) after "
                        f"{MAX_CREATES} Creates. No hard-fill. Report to CoS."
                    )
        finally:
            safe_close(ctx)

    ok = sum(1 for p in by_id.values() if p.get("status") in {"ok", "exists"})
    want = len(plates)
    print(f"OK part 04 Flow mint v06 finished ok={ok} want={want}", flush=True)
    if ok < want:
        sys.exit(2)


if __name__ == "__main__":
    main()
