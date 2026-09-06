#!/usr/bin/env python3
"""Part 03 Flow Veo 3.1 Fast — all real motion plates. No Ken Burns.

Auth lock (2026-09-06): mint ONLY via https://flow.google.com/u/1/ as
benoats@googlemail.com (10k+ credits). Refuse benoats86@gmail.com.

Create UI often finishes at 100% with zero getMediaUrlRedirect ids. After
Create is running, generate_clip returns needs_gallery_harvest; this mint
closes Chromium, settles, harvests in a fresh process, then relaunches.

Do not remint Part 01/02. Do not ping Ben. STOP if Create dies.
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

# Critical: Ben's credited Ultra session is multi-login slot /u/1/
flow.FLOW_HOME = os.environ.get("ORBIT_FLOW_HOME", "https://flow.google.com/u/1/")

PROJ = Path(__file__).resolve().parents[1]
PLATES_JSON = PROJ / "07_Edit-Project/parts/part-03_plates_v01.json"
RAW = PROJ / "04_Generated-Clips/part03/raw/v01_fast"
META = PROJ / "07_Edit-Project/part03_mint_flow_v01_meta.json"
HARVEST = Path(__file__).resolve().parent / "_harvest_newest_gallery_v01.py"
EXPLORER_LOCK = PROJ / "04_Generated-Clips/part01/refs/explorer_germs_part01_lock.jpg"
EXPLORER_START = PROJ / "04_Generated-Clips/part03/refs/v01_stills/05_explorer_ruler_start.jpg"
MODEL = os.environ.get("ORBIT_FLOW_VEO_MODEL", "Veo 3.1 - Fast")
PROFILE = Path(
    os.environ.get(
        "ORBIT_FLOW_PROFILE",
        str(Path.home() / ".playwright-hos-flow-profile"),
    )
)
STYLE = (
    "History of Science locked look: premium Animistry-class 3D cartoon, warm "
    "cinematic light, 1860 Karlsruhe congress-hall continuity. Not photoreal. "
    "Not live-action. Silent picture. No readable text, logos, or UI. "
    "No Orbit orange robot. Continuous real camera and object motion the whole clip. "
    "Never a still photo with Ken Burns. Never a dead-center full-screen title stamp."
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


def dest_for(plate_id: str) -> Path:
    return RAW / f"{plate_id}_v01.mp4"


def ensure_explorer_start() -> Path | None:
    if EXPLORER_START.exists() and EXPLORER_START.stat().st_size > 20_000:
        return EXPLORER_START
    if not EXPLORER_LOCK.exists():
        print(f"WARN missing explorer lock {EXPLORER_LOCK}", flush=True)
        return None
    EXPLORER_START.parent.mkdir(parents=True, exist_ok=True)
    bed = EXPLORER_START.with_name("_hall_bed.png")
    subprocess.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-f", "lavfi", "-i", "color=c=0xC4A574:s=1920x1080:d=1",
            "-frames:v", "1", str(bed),
        ],
        check=True,
    )
    subprocess.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(bed), "-i", str(EXPLORER_LOCK),
            "-filter_complex",
            "[1:v]scale=720:-1[ch];[0:v][ch]overlay=(W-w)/2:(H-h)/2+80",
            "-frames:v", "1", str(EXPLORER_START),
        ],
        check=True,
    )
    bed.unlink(missing_ok=True)
    return EXPLORER_START if EXPLORER_START.exists() else EXPLORER_LOCK


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
    ctx, page = flow.launch_context(p, headed=True, profile=profile)
    page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
    page.wait_for_timeout(2500)
    pick_google_account(page)
    flow.dismiss_banners(page)
    if not flow.looks_logged_in(page):
        safe_close(ctx)
        raise SystemExit(
            "BLOCKED_AUTH: Flow not logged in. Do not Ken-Burns. "
            "Ben must sign Mini as benoats@googlemail.com on /u/1/."
        )
    active = require_flow_account(page)
    print(f"  AUTH OK minting as {active} via {flow.FLOW_HOME}", flush=True)
    return ctx, page, active


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


def main() -> None:
    only = set(sys.argv[1:]) if len(sys.argv) > 1 else None
    plates = json.loads(PLATES_JSON.read_text())["plates"]
    RAW.mkdir(parents=True, exist_ok=True)
    meta: dict = {
        "engine": "flow-ui",
        "model": MODEL,
        "flow_home": flow.FLOW_HOME,
        "raw": str(RAW),
        "plates": [],
    }
    if META.exists():
        try:
            meta = json.loads(META.read_text())
        except Exception:
            pass
    by_id = {p["id"]: p for p in meta.get("plates", []) if "id" in p}
    explorer_start = ensure_explorer_start()
    profile = flow.profile_path(PROFILE)
    print(
        f"Flow profile={profile} home={flow.FLOW_HOME} model={MODEL} plates={len(plates)}",
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
                if only and pid not in only and not any(pid.startswith(x) for x in only):
                    continue
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
                            "status": "exists",
                            "out": str(dest),
                            "duration": dur,
                        }
                        continue
                    print(f"  re-mint bad existing {dest.name} dur={dur:.2f}", flush=True)
                    dest.unlink(missing_ok=True)

                prompt = f"{STYLE} {plate['prompt']}"
                start = explorer_start if plate.get("explorer") else None
                kind = "I2V" if start else "T2V"
                print(f"\n=== Fast {kind} {pid} ({i+1}/{len(plates)}) ===", flush=True)

                # Ensure live page
                try:
                    _ = page.url
                except Exception:
                    print("  page dead — relaunching", flush=True)
                    safe_close(ctx)
                    ctx, page, active = open_flow(p, profile=profile)

                tmp = dest.with_suffix(".tmp.mp4")
                tmp.unlink(missing_ok=True)
                info = None
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
                    # Explorer I2V attach can fail when Create UI hides Add to Prompt.
                    # Fall back once to T2V with the same Explorer prompt (no Ken Burns).
                    if (
                        start is not None
                        and "add to prompt" in str(e).lower()
                    ):
                        print(
                            f"  I2V attach failed ({e}); falling back to Explorer T2V",
                            flush=True,
                        )
                        safe_close(ctx)
                        ctx, page, active = open_flow(p, profile=profile)
                        t2v_prompt = prompt.replace(
                            "IMAGE-TO-VIDEO from attached start frame. ",
                            "Exactly ONE Explorer boy in frame. ",
                        )
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
                        except Exception as e2:
                            e = e2
                            info = None
                    if info is None:
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
                    project_url = info.get("project_url") or (page.url or "")
                    project_url = project_url.split("?")[0].rstrip("/")
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

    ok = sum(1 for p in by_id.values() if p.get("status") in {"ok", "exists"})
    want = len(only) if only else len(plates)
    print(f"OK part 03 Flow mint finished ok={ok} want={want}", flush=True)
    if ok < want:
        sys.exit(2)


if __name__ == "__main__":
    main()
