#!/usr/bin/env python3
"""Part 04 Flow Veo 3.1 Fast partial remint v02 — scrub model-town window.

Showrunner PART04_V02_SCRUB_MODEL_TOWN_WINDOW.md (parent v01 sha 543fd388…):
  - REMINT: 05_columns_families (REQUIRED ~40–45s) + 06_explorer_leaves_gap
    if window still shows houses (spot: t7 glow)
  - Window exterior: night sky + moon/stars ONLY (no model-town / yellow windows)
  - KEEP: Explorer teal trenchcoat, VO/labels, desk DNA, PLATE_ORDER
  - Prefer I2V from scrubbed stills. Veo Fast. Create dies → STOP (no Ken Burns).
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

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))

import orbit_flow_veo_ui as flow  # noqa: E402
import orbit_gemini_veo as veo  # noqa: E402

flow.FLOW_HOME = os.environ.get("ORBIT_FLOW_HOME", "https://flow.google.com/u/1/")

PROJ = Path(__file__).resolve().parents[1]
PLATES_JSON = PROJ / "07_Edit-Project/parts/part-04_plates_v01.json"
RAW = PROJ / "04_Generated-Clips/part04/raw/v02_fast"
META = PROJ / "07_Edit-Project/part04_mint_flow_v02_meta.json"
HARVEST = Path(__file__).resolve().parent / "_harvest_newest_gallery_v01.py"
FORCE_DL = Path(__file__).resolve().parent / "_harvest_force_download_v01.py"
STILLS = PROJ / "04_Generated-Clips/part04/refs/v02_stills"
MODEL = os.environ.get("ORBIT_FLOW_VEO_MODEL", "Veo 3.1 - Fast")
PROFILE = Path(
    os.environ.get(
        "ORBIT_FLOW_PROFILE",
        str(Path.home() / ".playwright-hos-flow-profile"),
    )
)

STYLE = (
    "Animistry-class stylised 3D cartoon (NOT photoreal). "
    "Same 1869 chemist desk DNA as the attached frame: honey wood desk, soft warm "
    "lamp, cream blank cards. Continuous real camera/object motion. Silent. "
    "No Orbit. No Ken Burns still. Opaque vessels preferred."
)

REJECT = (
    "HARD REJECT: model-town; miniature houses outside the window; glowing yellow "
    "rectangular house windows; toy house-blocks; outdoor town sprawl; floor "
    "diorama as hero; Ken Burns only; Orbit robot; photoreal; layout reset away "
    "from desk DNA."
)

WINDOW_LOCK = (
    "Through the lab window: deep night sky with moon and faint stars ONLY. "
    "NO houses. NO glowing yellow windows outside. NO miniature town. "
    "NO toy building blocks on the exterior ledge."
)

PROMPT_05 = (
    "IMAGE-TO-VIDEO from the attached start frame. KEEP this EXACT 1869 chemist "
    "desk DNA (honey wood, soft lamp, cream card stacks, lab vessels). "
    "Cards continue dropping into vertical family columns — cousins grouping. "
    f"{WINDOW_LOCK} "
    "Continuous drop + settle motion. Silent. No people. No Explorer. "
    + REJECT + " " + STYLE
)

PROMPT_06 = (
    "IMAGE-TO-VIDEO from the attached start frame. KEEP this EXACT 1869 desk DNA "
    "and the ONE Explorer boy — messy wavy brown hair, gold wire-rim glasses, "
    "teal trenchcoat overcoat house lock (NOT academic blazer). "
    "He pins one cream card into a column, leaves a glowing vacant seat/gap, "
    "steps back. Continuous acting + gentle camera. "
    f"{WINDOW_LOCK} "
    "Silent. HARD REJECT: twins, off-model Explorer, model-town, Orbit robot. "
    + REJECT + " " + STYLE
)

T2V_05 = (
    "ONE persistent 1869 chemist desk: honey wood, soft warm lamp, cream blank "
    "cards in family columns, lab vessels. Continuous card drop into columns. "
    f"{WINDOW_LOCK} Silent. No people. " + STYLE + " " + REJECT
)

T2V_06 = (
    "ONE persistent 1869 chemist desk DNA. Exactly ONE Explorer boy (messy wavy "
    "brown hair, gold glasses, teal trenchcoat). He leaves a glowing vacant seat "
    "in the card columns and steps back. Continuous acting. "
    f"{WINDOW_LOCK} Silent. " + STYLE + " " + REJECT
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

DEFAULT_ONLY = ("05_columns_families", "06_explorer_leaves_gap")
ALLOWED_ONLY = set(DEFAULT_ONLY)

START_FRAMES = {
    "05_primary": STILLS / "05_columns_scrub_i2v.jpg",
    "05_alt": STILLS / "05_columns_scrub_alt.jpg",
    "05_rough": STILLS / "05_columns_scrub_from_rough.jpg",
    "06_primary": STILLS / "06_explorer_scrub_i2v.jpg",
    "06_alt": STILLS / "06_explorer_scrub_alt.jpg",
}


def dest_for(plate_id: str) -> Path:
    return RAW / f"{plate_id}_v02.mp4"


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


def resolve_start_frame(pid: str) -> Path:
    if pid == "05_columns_families":
        keys = ["05_primary", "05_alt", "05_rough"]
    elif pid == "06_explorer_leaves_gap":
        keys = ["06_primary", "06_alt"]
    else:
        raise SystemExit(f"STOP: unexpected plate {pid}")
    for key in keys:
        path = START_FRAMES[key]
        if path.exists() and path.stat().st_size > 20_000:
            print(f"  I2V start_frame={path}", flush=True)
            return path
    raise SystemExit(f"STOP: no usable I2V start frame for {pid}")


def prompt_for(pid: str) -> str:
    if pid == "05_columns_families":
        return PROMPT_05
    if pid == "06_explorer_leaves_gap":
        return PROMPT_06
    raise SystemExit(f"STOP: unexpected plate {pid}")


def t2v_prompt(pid: str) -> str:
    if pid == "05_columns_families":
        return T2V_05
    if pid == "06_explorer_leaves_gap":
        return T2V_06
    raise SystemExit(f"STOP: unexpected plate {pid}")


def alt_starts_for(pid: str, start: Path) -> list[Path]:
    if pid == "05_columns_families":
        keys = ["05_alt", "05_rough", "05_primary"]
    else:
        keys = ["06_alt", "06_primary"]
    out: list[Path] = []
    for key in keys:
        path = START_FRAMES[key]
        if path.exists() and path.resolve() != start.resolve():
            out.append(path)
    return out


def _truthy(name: str) -> bool:
    return os.environ.get(name, "").strip().lower() in {"1", "true", "yes", "on"}


def main() -> None:
    if _truthy("HOS_FLOW_SKIP_I2V"):
        print(
            "  WARN: unsetting HOS_FLOW_SKIP_I2V — v02 prefers scrubbed I2V",
            flush=True,
        )
        os.environ.pop("HOS_FLOW_SKIP_I2V", None)

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
        raise SystemExit(f"STOP: refuse remint via v02: {sorted(bad)}")

    plates = json.loads(PLATES_JSON.read_text())["plates"]
    order = [pid for pid in DEFAULT_ONLY if pid in only]
    plates = [p for p in plates if p["id"] in only]
    plates.sort(key=lambda p: order.index(p["id"]))
    if not plates:
        raise SystemExit(f"STOP: no plates matched only={sorted(only)}")

    RAW.mkdir(parents=True, exist_ok=True)
    meta: dict = {
        "engine": "flow-ui",
        "model": MODEL,
        "flow_home": flow.FLOW_HOME,
        "raw": str(RAW),
        "continuity": "scrub_model_town_window_v02",
        "parent_v01_sha": "543fd388f1bc1f1502d1eb45faf28e494658ec2ccc4749cce76bc5167b7a6a03",
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
        f"partial remint only={order}",
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
                start = resolve_start_frame(pid)
                force = _truthy("HOS_FLOW_FORCE_REMINT")
                if veo.already_done(dest, min_bytes=400_000) and not force:
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
                elif dest.exists() and force:
                    print(f"  force remint — removing {dest.name}", flush=True)
                    dest.unlink(missing_ok=True)

                prompt = prompt_for(pid)
                force_t2v = _truthy("HOS_FLOW_T2V_ONLY")
                kind = "T2V" if force_t2v else "I2V"
                print(
                    f"\n=== Fast {kind} {pid} ({i+1}/{len(plates)}) ===",
                    flush=True,
                )
                if not force_t2v:
                    print(f"  start_frame={start}", flush=True)

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

                if force_t2v:
                    try:
                        info = flow.generate_clip(
                            page,
                            t2v_prompt(pid),
                            tmp,
                            model=MODEL,
                            start_frame=None,
                            scenery_only=True,
                            reuse_project=False,
                            attempts=2,
                            timeout_s=180,
                        )
                    except Exception as e:
                        i2v_err = e
                        info = None
                else:
                    try:
                        info = flow.generate_clip(
                            page,
                            prompt,
                            tmp,
                            model=MODEL,
                            start_frame=start,
                            scenery_only=False,
                            reuse_project=False,
                            attempts=2,
                            timeout_s=180,
                        )
                    except Exception as e:
                        i2v_err = e
                        info = None

                    # Retry alt scrubbed stills before T2V
                    if info is None:
                        for alt in alt_starts_for(pid, start):
                            print(f"  I2V retry alt start={alt}", flush=True)
                            safe_close(ctx)
                            ctx, page, active = open_flow(p, profile=profile)
                            try:
                                info = flow.generate_clip(
                                    page,
                                    prompt_for(pid),
                                    tmp,
                                    model=MODEL,
                                    start_frame=alt,
                                    scenery_only=False,
                                    reuse_project=False,
                                    attempts=2,
                                    timeout_s=180,
                                )
                                info["alt_start_frame"] = str(alt)
                                break
                            except Exception as e2:
                                i2v_err = e2
                                info = None

                    if info is None:
                        print(
                            f"  I2V failed ({i2v_err}); falling back to desk-DNA T2V Fast "
                            "(no Ken Burns)",
                            flush=True,
                        )
                        safe_close(ctx)
                        ctx, page, active = open_flow(p, profile=profile)
                        try:
                            info = flow.generate_clip(
                                page,
                                t2v_prompt(pid),
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
                    "start_frame": str(start) if not force_t2v else None,
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
    want = len(plates)
    print(f"OK part 04 Flow mint v02 finished ok={ok} want={want}", flush=True)
    if ok < want:
        sys.exit(2)


if __name__ == "__main__":
    main()
