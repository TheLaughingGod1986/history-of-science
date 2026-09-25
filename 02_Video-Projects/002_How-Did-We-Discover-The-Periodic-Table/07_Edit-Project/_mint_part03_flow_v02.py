#!/usr/bin/env python3
"""Part 03 Flow Veo 3.1 Fast remint v02 — hall continuity lock.

HARD LOCK (UAT FAIL fix):
  - plate 01 hall DNA on EVERY scenery plate
  - Prefer I2V from plate-01 frames / same-room stills
  - Forbidden: blackboard, chandelier, fresco, model-town sets
  - KEEP plate 01 if already clean (copy into v02_fast)
  - Explorer once on plate 05 only
  - STOP if Create dies — no Ken Burns fallback
  - Do not remint/overwrite Part 01 v14 or Part 02 v06

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

# Critical: Ben's credited Ultra session is multi-login slot /u/1/
flow.FLOW_HOME = os.environ.get("ORBIT_FLOW_HOME", "https://flow.google.com/u/1/")

PROJ = Path(__file__).resolve().parents[1]
PLATES_JSON = PROJ / "07_Edit-Project/parts/part-03_plates_v01.json"
RAW = PROJ / "04_Generated-Clips/part03/raw/v02_fast"
RAW_V01 = PROJ / "04_Generated-Clips/part03/raw/v01_fast"
META = PROJ / "07_Edit-Project/part03_mint_flow_v02_meta.json"
HARVEST = Path(__file__).resolve().parent / "_harvest_newest_gallery_v01.py"
STILLS = PROJ / "04_Generated-Clips/part03/refs/v02_stills"
EXPLORER_LOCK = PROJ / "04_Generated-Clips/part01/refs/explorer_germs_part01_lock.jpg"
MODEL = os.environ.get("ORBIT_FLOW_VEO_MODEL", "Veo 3.1 - Fast")
PROFILE = Path(
    os.environ.get(
        "ORBIT_FLOW_PROFILE",
        str(Path.home() / ".playwright-hos-flow-profile"),
    )
)

# Short style prefix — I2V attached frame carries hall DNA; keep typed prompt lean.
STYLE = (
    "Animistry-class stylised 3D cartoon (NOT photoreal). "
    "Same Karlsruhe congress-hall DNA as the attached frame. "
    "Continuous real camera/object motion. Silent. No readable text. "
    "No Orbit. No Ken Burns still. No blackboard/chandelier/fresco/model-town swap."
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

START_FRAMES = {
    "hall_dna_t1": STILLS / "01_hall_dna_t1.jpg",
    "hall_dna_t4": STILLS / "01_hall_dna_t4.jpg",
    "hall_dna_t65": STILLS / "01_hall_dna_t65.jpg",
    "explorer_on_hall": STILLS / "05_explorer_on_hall_start.jpg",
}


def dest_for(plate_id: str) -> Path:
    return RAW / f"{plate_id}_v02.mp4"


def ensure_hall_stills() -> None:
    STILLS.mkdir(parents=True, exist_ok=True)
    src01 = RAW_V01 / "01_hall_open_side_label_v01.mp4"
    if not src01.exists():
        raise SystemExit(f"STOP: missing plate-01 DNA source {src01}")
    needed = {
        "01_hall_dna_t1.jpg": 1.0,
        "01_hall_dna_t4.jpg": 4.0,
        "01_hall_dna_t65.jpg": 6.5,
    }
    for name, ss in needed.items():
        dest = STILLS / name
        if dest.exists() and dest.stat().st_size > 10_000:
            continue
        subprocess.run(
            [
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-ss", str(ss), "-i", str(src01), "-frames:v", "1", str(dest),
            ],
            check=True,
        )
    explorer = STILLS / "05_explorer_on_hall_start.jpg"
    if not (explorer.exists() and explorer.stat().st_size > 10_000):
        if not EXPLORER_LOCK.exists():
            raise SystemExit(f"STOP: missing explorer lock {EXPLORER_LOCK}")
        bed = STILLS / "01_hall_dna_t4.jpg"
        subprocess.run(
            [
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-i", str(bed), "-i", str(EXPLORER_LOCK),
                "-filter_complex",
                "[1:v]scale=640:-1[ch];[0:v][ch]overlay=(W-w)/2:(H-h)/2+120",
                "-frames:v", "1", str(explorer),
            ],
            check=True,
        )


def keep_plate01_if_clean() -> Path | None:
    """Copy clean v01 plate 01 into v02_fast (DNA keeper)."""
    dest = dest_for("01_hall_open_side_label")
    if veo.already_done(dest, min_bytes=400_000):
        return dest
    src = RAW_V01 / "01_hall_open_side_label_v01.mp4"
    if not src.exists() or src.stat().st_size < 400_000:
        return None
    try:
        dur = probe_dur(src)
    except Exception:
        return None
    if not (5.0 <= dur <= 40.0):
        return None
    RAW.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    print(f"  KEEP plate01 DNA → {dest.name} bytes={dest.stat().st_size} dur={dur:.2f}", flush=True)
    return dest


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
    """Best-effort credit/limit probe before mint. Return status blob."""
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
    # Surface any credit-looking chrome for the log
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
                # Mid-picker residue after failed I2V can fool the probe —
                # hard reload once before declaring BLOCKED_AUTH.
                if not flow.looks_logged_in(page):
                    page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
                    page.wait_for_timeout(3500)
                    pick_google_account(page)
                    flow.dismiss_banners(page)
                    page.wait_for_timeout(1500)
            if not flow.looks_logged_in(page):
                # Last resort: if account chrome still shows required email, accept it.
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
        raise SystemExit(f"STOP: missing start frame key={key} path={path}")
    return path


def main() -> None:
    only = set(sys.argv[1:]) if len(sys.argv) > 1 else None
    plates = json.loads(PLATES_JSON.read_text())["plates"]
    ensure_hall_stills()
    RAW.mkdir(parents=True, exist_ok=True)
    meta: dict = {
        "engine": "flow-ui",
        "model": MODEL,
        "flow_home": flow.FLOW_HOME,
        "raw": str(RAW),
        "continuity": "plate01_hall_dna_i2v",
        "plates": [],
    }
    if META.exists():
        try:
            meta = json.loads(META.read_text())
        except Exception:
            pass
    by_id = {p["id"]: p for p in meta.get("plates", []) if "id" in p}

    # KEEP plate 01 DNA before opening Flow when possible
    if not only or "01_hall_open_side_label" in only or any(
        "01_hall_open_side_label".startswith(x) for x in (only or [])
    ):
        kept = keep_plate01_if_clean()
        if kept is not None:
            by_id["01_hall_open_side_label"] = {
                "id": "01_hall_open_side_label",
                "status": "kept_v01_dna",
                "out": str(kept),
                "duration": probe_dur(kept),
            }
            meta["plates"] = list(by_id.values())
            META.write_text(json.dumps(meta, indent=2))

    profile = flow.profile_path(PROFILE)
    print(
        f"Flow profile={profile} home={flow.FLOW_HOME} model={MODEL} plates={len(plates)}",
        flush=True,
    )

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        # Confirm email+credits BEFORE mint
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
                            "status": by_id.get(pid, {}).get("status", "exists"),
                            "out": str(dest),
                            "duration": dur,
                        }
                        continue
                    print(f"  re-mint bad existing {dest.name} dur={dur:.2f}", flush=True)
                    dest.unlink(missing_ok=True)

                # Plate 01 KEEP path — do not remint if clean
                if plate.get("keep_if_clean") and keep_plate01_if_clean() is not None:
                    by_id[pid] = {
                        "id": pid,
                        "status": "kept_v01_dna",
                        "out": str(dest_for(pid)),
                        "duration": probe_dur(dest_for(pid)),
                    }
                    meta["plates"] = list(by_id.values())
                    META.write_text(json.dumps(meta, indent=2))
                    continue

                # I2V Add-to-Prompt is flaky on Mini (Facebook poison / never enables).
                # Prefer I2V when available; HOS_FLOW_SKIP_I2V=1 jumps straight to
                # hall-DNA T2V Fast (still real Veo motion — never Ken Burns).
                skip_i2v = os.environ.get("HOS_FLOW_SKIP_I2V", "").strip() in {
                    "1", "true", "yes",
                }
                start = None if skip_i2v else start_frame_for(plate)
                kind = "I2V" if start else ("T2V_skip_i2v" if skip_i2v else "T2V")
                # Prefer short prompt for I2V (frame carries DNA); keep STYLE lean.
                if start:
                    prompt = plate["prompt"]
                    if "IMAGE-TO-VIDEO" not in prompt:
                        prompt = f"IMAGE-TO-VIDEO from attached start frame. {prompt}"
                    prompt = f"{prompt} {STYLE}"
                else:
                    # Hall DNA must live in the typed prompt when no start frame.
                    prompt = (
                        "SAME Karlsruhe congress hall DNA as plate 01 — warm honey oak panels, "
                        "tall arched windows with volumetric daylight, rows of wooden benches, "
                        "blank cream pamphlets. Camera moves only; do NOT reset furniture layout; "
                        "do NOT invent a new room. FORBIDDEN: blackboard classroom, chandelier ballroom, "
                        "fresco gallery, separate model-town set, Part 01 workshop. "
                        f"{STYLE} {plate['prompt']}"
                    )
                    if plate.get("explorer"):
                        prompt = (
                            "Exactly ONE Explorer boy (Germs younger-boy lock) inside the SAME "
                            "Karlsruhe congress hall DNA. " + prompt
                        )

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

                # Prefer I2V; if Add-to-Prompt / Facebook media poison / attach fails,
                # fall back once to T2V with HARD hall-DNA prompt (NO Ken Burns).
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
                        if plate.get("explorer"):
                            t2v_prompt = (
                                "Exactly ONE Explorer boy (Germs younger-boy lock: messy wavy brown hair, "
                                "gold wire-rim glasses, teal-blue overcoat, tan waistcoat, floppy brown bow, "
                                "satchel with brass compass) inside the SAME Karlsruhe congress hall DNA: "
                                "warm honey oak panels, tall arched windows, wooden benches, blank cream pamphlets, "
                                "glowing blank wooden mass-line on the floor. Continuous acting + camera drift. "
                                "Opaque props only. Silent. No clear liquid glass. No blackboard. No chandelier. "
                                "No fresco. No model-town. No Orbit. No Ken Burns still. "
                                f"{plate['prompt']}"
                            )
                        else:
                            t2v_prompt = (
                                "SAME Karlsruhe congress hall DNA as plate 01 — warm honey oak panels, "
                                "tall arched windows with volumetric daylight, rows of wooden benches, "
                                "blank cream pamphlets. Camera moves only; do NOT reset furniture layout; "
                                "do NOT invent a new room. FORBIDDEN: blackboard classroom, chandelier ballroom, "
                                "fresco gallery, separate model-town set, Part 01 workshop. "
                                "Continuous real Veo camera/object motion the whole clip. Silent. "
                                "No readable text. No Orbit. No Ken Burns. "
                                f"{plate['prompt']}"
                            )
                        # Strip I2V preface so Flow treats this as scenery T2V.
                        t2v_prompt = t2v_prompt.replace(
                            "IMAGE-TO-VIDEO from attached start frame. ", ""
                        ).replace(
                            "IMAGE-TO-VIDEO from attached Karlsruhe hall start frame. ", ""
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

    ok = sum(1 for p in by_id.values() if p.get("status") in {"ok", "exists", "kept_v01_dna"})
    want = len(only) if only else len(plates)
    print(f"OK part 03 Flow mint v02 finished ok={ok} want={want}", flush=True)
    if ok < want:
        sys.exit(2)


if __name__ == "__main__":
    main()
