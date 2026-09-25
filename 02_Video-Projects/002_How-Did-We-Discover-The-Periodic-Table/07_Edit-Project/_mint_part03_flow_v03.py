#!/usr/bin/env python3
"""Part 03 Flow Veo 3.1 Fast partial remint v03 — plates 09 (±10) only.

Showrunner v03 sheet:
  - REMINT only 09_empty_chair_claim (±10_city_plan_lots if model-town)
  - KEEP rest of v02 timeline
  - Prefer I2V from plate-01 / KEEP chair frames
  - No model-town sprawl; postcard-scale plan on existing hall desk only
  - STOP if Create dies — no Ken Burns
  - Do not remint/overwrite Part 01 v14 or Part 02 v06
  - Do not remint plate 05 Explorer

Auth lock: mint ONLY via https://flow.google.com/u/1/ as
benoats@googlemail.com. Refuse benoats86@gmail.com. Confirm email+credits
BEFORE mint; STOP BLOCKED_AUTH if wrong account.
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

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))

import orbit_flow_veo_ui as flow  # noqa: E402
import orbit_gemini_veo as veo  # noqa: E402

flow.FLOW_HOME = os.environ.get("ORBIT_FLOW_HOME", "https://flow.google.com/u/1/")

PROJ = Path(__file__).resolve().parents[1]
PLATES_JSON = PROJ / "07_Edit-Project/parts/part-03_plates_v01.json"
RAW = PROJ / "04_Generated-Clips/part03/raw/v03_fast"
RAW_V02 = PROJ / "04_Generated-Clips/part03/raw/v02_fast"
META = PROJ / "07_Edit-Project/part03_mint_flow_v03_meta.json"
HARVEST = Path(__file__).resolve().parent / "_harvest_newest_gallery_v01.py"
STILLS = PROJ / "04_Generated-Clips/part03/refs/v03_stills"
STILLS_V02 = PROJ / "04_Generated-Clips/part03/refs/v02_stills"
MODEL = os.environ.get("ORBIT_FLOW_VEO_MODEL", "Veo 3.1 - Fast")
PROFILE = Path(
    os.environ.get(
        "ORBIT_FLOW_PROFILE",
        str(Path.home() / ".playwright-hos-flow-profile"),
    )
)

STYLE = (
    "Animistry-class stylised 3D cartoon (NOT photoreal). "
    "Same Karlsruhe congress-hall DNA as the attached plate-01 frame. "
    "Continuous real camera/object motion. Silent. No readable text. "
    "No Orbit. No Ken Burns still. No blackboard/chandelier/fresco/model-town sprawl."
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

DEFAULT_ONLY = ("09_empty_chair_claim", "10_city_plan_lots")

START_FRAMES = {
    "empty_chair_i2v": STILLS / "09_empty_chair_i2v_start.jpg",
    "postcard_plan_i2v": STILLS / "10_postcard_plan_i2v_start.jpg",
    "hall_dna_t1": STILLS_V02 / "01_hall_dna_t1.jpg",
    "hall_dna_t4": STILLS_V02 / "01_hall_dna_t4.jpg",
    "hall_dna_t65": STILLS_V02 / "01_hall_dna_t65.jpg",
    "09_hall_dna_fallback": STILLS / "09_hall_dna_fallback.jpg",
    "10_hall_dna_fallback": STILLS / "10_hall_dna_fallback.jpg",
}


def dest_for(plate_id: str) -> Path:
    return RAW / f"{plate_id}_v03.mp4"


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
    subprocess.check_call(cmd, env=env)


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


def start_frame_for(plate: dict) -> Path | None:
    if not plate.get("i2v", False):
        return None
    key = plate.get("start_frame_key") or "hall_dna_t4"
    path = START_FRAMES.get(key)
    if path is None or not path.exists():
        # Prefer plate-01 DNA fallbacks for v03 remint plates
        fallback = START_FRAMES.get(
            "09_hall_dna_fallback" if plate["id"].startswith("09_") else "10_hall_dna_fallback"
        )
        if fallback and fallback.exists():
            print(f"  start_frame missing key={key}; using fallback {fallback.name}", flush=True)
            return fallback
        raise SystemExit(f"STOP: missing start frame key={key} path={path}")
    return path


def hall_dna_t2v_prompt(plate: dict) -> str:
    base = (
        "SAME Karlsruhe congress hall DNA as plate 01 — warm honey oak panels, "
        "tall arched windows with volumetric daylight, rows of wooden benches, "
        "blank cream pamphlets, clear central aisle. Camera moves only; do NOT reset "
        "furniture layout; do NOT invent a new room. FORBIDDEN: blackboard classroom, "
        "chandelier ballroom, fresco gallery, wooden model-town sprawl / floor town, "
        "Part 01 workshop. Continuous real Veo camera/object motion the whole clip. "
        "Silent. No readable text. No Orbit. No Ken Burns. "
    )
    prompt = plate["prompt"]
    for pref in (
        "IMAGE-TO-VIDEO from attached start frame. ",
        "IMAGE-TO-VIDEO from attached Karlsruhe hall start frame. ",
    ):
        prompt = prompt.replace(pref, "")
    return base + prompt


def main() -> None:
    argv = [a for a in sys.argv[1:] if not a.startswith("-")]
    only = set(argv) if argv else set(DEFAULT_ONLY)
    # Hard refuse reminting Explorer / locked keepers via this partial script
    forbidden = {
        "01_hall_open_side_label",
        "05_explorer_ruler",
    }
    bad = only & forbidden
    if bad:
        raise SystemExit(f"STOP: refuse remint of locked plates via v03: {sorted(bad)}")

    plates = json.loads(PLATES_JSON.read_text())["plates"]
    plates = [p for p in plates if p["id"] in only or any(p["id"].startswith(x) for x in only)]
    if not plates:
        raise SystemExit(f"STOP: no plates matched only={sorted(only)}")

    for key, path in START_FRAMES.items():
        if key in {"empty_chair_i2v", "postcard_plan_i2v"} and not path.exists():
            raise SystemExit(f"STOP: missing v03 I2V still {path}")

    RAW.mkdir(parents=True, exist_ok=True)
    meta: dict = {
        "engine": "flow-ui",
        "model": MODEL,
        "flow_home": flow.FLOW_HOME,
        "raw": str(RAW),
        "continuity": "plate01_hall_dna_i2v_partial_v03",
        "source_keep_v02": str(RAW_V02),
        "only": sorted(only),
        "plates": [],
    }
    if META.exists():
        try:
            meta = json.loads(META.read_text())
            meta["only"] = sorted(only)
        except Exception:
            pass
    by_id = {p["id"]: p for p in meta.get("plates", []) if "id" in p}

    profile = flow.profile_path(PROFILE)
    print(
        f"Flow profile={profile} home={flow.FLOW_HOME} model={MODEL} "
        f"partial remint only={sorted(only)}",
        flush=True,
    )

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        ctx, page, active = open_flow(p, profile=profile)
        meta["flow_account"] = active
        meta["flow_home"] = flow.FLOW_HOME
        try:
            for i, plate in enumerate(plates):
                pid = plate["id"]
                dest = dest_for(pid)
                if veo.already_done(dest, min_bytes=400_000):
                    try:
                        dur = probe_dur(dest)
                    except Exception:
                        dur = 0.0
                    if 5.0 <= dur <= 40.0:
                        print(f"  skip {dest.name} dur={dur:.2f}", flush=True)
                        by_id[pid] = {
                            "id": pid,
                            "status": by_id.get(pid, {}).get("status", "exists"),
                            "out": str(dest),
                            "duration": dur,
                        }
                        continue
                    print(f"  re-mint bad existing {dest.name} dur={dur:.2f}", flush=True)
                    dest.unlink(missing_ok=True)

                skip_i2v = os.environ.get("HOS_FLOW_SKIP_I2V", "").strip() in {
                    "1", "true", "yes",
                }
                start = None if skip_i2v else start_frame_for(plate)
                kind = "I2V" if start else ("T2V_skip_i2v" if skip_i2v else "T2V")
                if start:
                    prompt = plate["prompt"]
                    if "IMAGE-TO-VIDEO" not in prompt:
                        prompt = f"IMAGE-TO-VIDEO from attached start frame. {prompt}"
                    prompt = f"{prompt} {STYLE}"
                else:
                    prompt = hall_dna_t2v_prompt(plate)

                print(f"\n=== Fast {kind} {pid} ({i+1}/{len(plates)}) ===", flush=True)
                if start:
                    print(f"  start_frame={start}", flush=True)
                elif skip_i2v:
                    print(
                        "  HOS_FLOW_SKIP_I2V=1 — hall-DNA T2V Fast (no Ken Burns)",
                        flush=True,
                    )

                try:
                    _ = page.url
                except Exception:
                    print("  page dead — relaunching", flush=True)
                    safe_close(ctx)
                    ctx, page, active = open_flow(p, profile=profile)

                tmp = dest.with_suffix(".tmp.mp4")
                tmp.unlink(missing_ok=True)
                info = None
                i2v_err: Exception | None = None
                try:
                    info = flow.generate_clip(
                        page,
                        prompt,
                        tmp,
                        model=MODEL,
                        start_frame=start,
                        scenery_only=(start is None),
                        reuse_project=False,
                        attempts=2,
                        timeout_s=180,
                    )
                except Exception as e:
                    i2v_err = e
                    info = None

                if info is None and start is not None:
                    elow = str(i2v_err or "").lower()
                    attach_fail = any(
                        x in elow
                        for x in (
                            "add to prompt",
                            "did not attach",
                            "upload",
                            "facebook",
                            "start frame",
                        )
                    )
                    if attach_fail or i2v_err is not None:
                        print(
                            f"  I2V preferred failed ({i2v_err}); "
                            "falling back to hall-DNA T2V Fast (no Ken Burns)",
                            flush=True,
                        )
                        safe_close(ctx)
                        ctx, page, active = open_flow(p, profile=profile)
                        t2v_prompt = hall_dna_t2v_prompt(plate)
                        try:
                            info = flow.generate_clip(
                                page,
                                t2v_prompt,
                                tmp,
                                model=MODEL,
                                start_frame=None,
                                scenery_only=True,
                                reuse_project=False,
                                attempts=2,
                                timeout_s=180,
                            )
                            info["i2v_fallback_t2v"] = True
                            info["i2v_error"] = str(i2v_err)[:300]
                            kind = "T2V_fallback"
                        except Exception as e2:
                            i2v_err = e2
                            info = None

                if info is None:
                    e = i2v_err or RuntimeError("unknown Flow failure")
                    death = looks_like_create_death(e, page)
                    by_id[pid] = {
                        "id": pid,
                        "status": "fail",
                        "error": str(e)[:500],
                        "create_death": death,
                    }
                    meta["plates"] = list(by_id.values())
                    META.write_text(json.dumps(meta, indent=2))
                    if death:
                        raise SystemExit(
                            f"STOP BLOCKED: Create died on {pid} ({death}). "
                            "No Ken Burns. No Omni Flash substitute."
                        ) from e
                    raise SystemExit(f"STOP: Flow failed on {pid}: {e}") from e

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
                    raise SystemExit(f"STOP: download missing/small {tmp}")
                veo.strip_audio(tmp)
                try:
                    dur = probe_dur(tmp)
                except Exception as e:
                    raise SystemExit(f"STOP: unreadable download {tmp}: {e}") from e
                if dur < 5.0 or dur > 40.0:
                    bad = RAW / f"{pid}_bad_dur_{dur:.1f}.mp4"
                    shutil.move(str(tmp), str(bad))
                    raise SystemExit(f"STOP: bad duration {bad} dur={dur:.2f}")
                if dest.exists():
                    dest.unlink()
                shutil.move(str(tmp), str(dest))
                by_id[pid] = {
                    "id": pid,
                    "status": "ok",
                    "out": str(dest),
                    "duration": dur,
                    "kind": kind,
                    "start_frame": str(start) if start else None,
                    **{k: v for k, v in info.items() if k != "needs_gallery_harvest"},
                }
                meta["plates"] = list(by_id.values())
                META.write_text(json.dumps(meta, indent=2))
                print(
                    f"  SAVED {dest.name} bytes={dest.stat().st_size} dur={dur:.2f}",
                    flush=True,
                )
        finally:
            safe_close(ctx)

    ok = sum(1 for p in by_id.values() if p.get("status") in {"ok", "exists"} and p["id"] in only)
    want = len(only)
    print(f"OK part 03 Flow mint v03 finished ok={ok} want={want}", flush=True)
    if ok < want:
        sys.exit(2)


if __name__ == "__main__":
    main()
