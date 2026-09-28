#!/usr/bin/env python3
"""HOS 004 Part 04 — Flow Veo 3.1 mint via Mini CDP + Gemini API fallback.

Part 03 rough v01 PASS (Ben: fine) → mint Part 04.
Account: benoats@googlemail.com on :9222 (primary).
Quality only when plate.quality == Quality (glow). Fast otherwise.
Max 2 tries/plate; try2 uses prompt_try2 (framing change). Strip Veo audio.
One plate at a time until first KEEP, then continue the board.

NEW (Ben-approved): if Flow credits would drop below ~150 buffer after the next
plate (Fast~20 / Quality~100 estimate), switch remaining plates to the SAME
Veo 3.1 model via Gemini API key already in Mini env:
  Quality → veo-3.1-generate-preview
  Fast    → veo-3.1-lite-generate-preview
Never mix other models. Log path + spend per plate. Never print API keys.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))
import orbit_flow_veo_ui as flow  # noqa: E402
import orbit_gemini_veo as veo  # noqa: E402

flow.FLOW_HOME = os.environ.get("ORBIT_FLOW_HOME", "https://flow.google.com/")
CDP = os.environ.get("ORBIT_FLOW_CDP", "http://127.0.0.1:9222")
REQUIRED = "benoats@googlemail.com"
FORBIDDEN = "benoats86@gmail.com"

PROJ = Path(__file__).resolve().parents[1]
PLATES_JSON = PROJ / "07_Edit-Project/parts/part-04_plates_v02.json"
REFS = PROJ / "04_Generated-Clips/part04/refs/v01_stills"
RAW = PROJ / "04_Generated-Clips/part04/raw/v01"
QA = PROJ / "07_Edit-Project/_qa_part04_mint_v01"
LOG = PROJ / "07_Edit-Project/PART04_MINT_LOG_v01.json"
EXPLORER_REF = (
    REPO / "01_Character/05_Generation-References/hos-explorer-reference-v01.jpg"
)

STYLE = (
    "Premium Animistry-class 3D cartoon, warm cinematic light, period science world. "
    "Not photoreal. Silent. Continuous motion the whole clip. No Orbit robot. "
    "No readable fake text or garbled tiles."
)

# Flow credit buffer (Ben-approved). Keep ~150 spare before switching to Gemini API.
FLOW_CREDIT_BUFFER = 150
FLOW_COST_FAST_EST = 20
FLOW_COST_QUALITY_EST = 100
GEMINI_FAST_MODEL = os.environ.get("HOS_VEO_FAST_MODEL", "veo-3.1-lite-generate-preview")
GEMINI_QUALITY_MODEL = os.environ.get(
    "HOS_VEO_QUALITY_MODEL", "veo-3.1-generate-preview"
)
ENV_CANDIDATES = [
    REPO / "02_Video-Projects/002_How-Did-We-Discover-The-Periodic-Table/07_Edit-Project/.env",
    REPO / "02_Video-Projects/001_How-Did-We-Discover-Germs/07_Edit-Project/.env",
    REPO / "02_Video-Projects/003_Invisible-Bones-X-Rays/07_Edit-Project/.env",
    PROJ / "07_Edit-Project/.env",
]

CREDIT_RE = re.compile(
    r"([\d,]{1,7})\s*(?:Google\s+Flow\s+)?credits", re.I
)
UNPAID_RE = re.compile(
    r"unpaid|payment (failed|error)|couldn.?t (charge|process)|billing|"
    r"add a payment|update (your )?payment|purchase failed|transaction failed|"
    r"insufficient credits|not enough credits|out of google flow credits|"
    r"reached your credit",
    re.I,
)
SIGNED_OUT_RE = re.compile(
    r"you.?re not signed in|session ended because there was no activity|"
    r"try signing in again|sign in to continue",
    re.I,
)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def probe_dur(path: Path) -> float:
    return float(
        subprocess.check_output(
            [
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=nw=1:nk=1", str(path),
            ],
            text=True,
        ).strip()
    )


def model_for(plate: dict) -> str:
    q = (plate.get("quality") or "Fast").strip()
    if q.lower() == "quality":
        return "Veo 3.1 - Quality"
    return "Veo 3.1 - Fast"


def quality_or_fast(plate: dict) -> str:
    q = (plate.get("quality") or "Fast").strip()
    return "Quality" if q.lower() == "quality" else "Fast"


def estimate_flow_cost(plate: dict) -> int:
    return (
        FLOW_COST_QUALITY_EST
        if quality_or_fast(plate) == "Quality"
        else FLOW_COST_FAST_EST
    )


def gemini_model_for(plate: dict) -> str:
    return (
        GEMINI_QUALITY_MODEL
        if quality_or_fast(plate) == "Quality"
        else GEMINI_FAST_MODEL
    )


def flow_would_breach_buffer(credits: int | None, plate: dict) -> bool:
    """True when next Flow plate would leave us under the ~150 buffer."""
    if credits is None:
        return False
    return credits - estimate_flow_cost(plate) < FLOW_CREDIT_BUFFER


def load_gemini_client():
    """Load Gemini client from Mini env. Never print keys."""
    for env in ENV_CANDIDATES:
        if not env.exists():
            continue
        for line in env.read_text().splitlines():
            s = line.strip()
            if not s or s.startswith("#") or "=" not in s:
                continue
            k, v = s.split("=", 1)
            k, v = k.strip(), v.strip().strip('"').strip("'")
            if k in ("GEMINI_API_KEY", "GOOGLE_API_KEY") and v:
                os.environ[k] = v
        try:
            client = veo.make_client(env)
            print(f"Gemini client ready (key from {env.name})", flush=True)
            return client
        except SystemExit:
            continue
        except Exception as e:
            print(f"Gemini client skip {env.name}: {type(e).__name__}", flush=True)
            continue
    raise SystemExit("STOP: no Gemini API key in Mini env for Veo 3.1 fallback")


def load_log() -> dict:
    if LOG.exists():
        return json.loads(LOG.read_text())
    return {
        "film": "004_Whats-Really-Inside-An-Atom",
        "part": "04",
        "plates": {},
    }


def save_log(log: dict) -> None:
    log["updated_at"] = now()
    LOG.parent.mkdir(parents=True, exist_ok=True)
    LOG.write_text(json.dumps(log, indent=2) + "\n")


def page_text(page, n: int = 16000) -> str:
    try:
        return page.locator("body").inner_text(timeout=8000)[:n]
    except Exception:
        try:
            return page.inner_text("body")[:n]
        except Exception:
            return ""


def open_account_menu(page) -> None:
    for sel in (
        '[aria-label*="Account details" i]',
        '[aria-label*="Google Account" i]',
        'button:has-text("ULTRA")',
        "text=ULTRA",
    ):
        try:
            loc = page.locator(sel).first
            if loc.count() == 0:
                continue
            loc.click(timeout=2500)
            time.sleep(1.4)
            return
        except Exception:
            continue


def read_credits(page) -> tuple[int | None, str | None]:
    text = page_text(page)
    emails = set(re.findall(r"[A-Za-z0-9._%+-]+@(?:gmail|googlemail)\.com", text, flags=re.I))
    # Also scrape aria-labels (Google Account chip often only lives there)
    try:
        aria_emails = page.evaluate(
            """() => [...document.querySelectorAll('[aria-label]')]
              .map(e => e.getAttribute('aria-label') || '')
              .join('\\n')"""
        ) or ""
        emails |= set(
            re.findall(r"[A-Za-z0-9._%+-]+@(?:gmail|googlemail)\.com", aria_emails, flags=re.I)
        )
    except Exception:
        pass
    active = None
    if REQUIRED.lower() in {e.lower() for e in emails}:
        active = REQUIRED.lower()
    elif emails:
        active = sorted(emails)[0].lower()

    hits = [int(m.group(1).replace(",", "")) for m in CREDIT_RE.finditer(text)]
    credits = None
    if hits:
        near = [c for c in hits if 500 <= c <= 20000]
        credits = near[0] if near else max(hits)

    if credits is None or active is None:
        open_account_menu(page)
        text = page_text(page)
        emails = set(re.findall(r"[A-Za-z0-9._%+-]+@(?:gmail|googlemail)\.com", text, flags=re.I))
        try:
            aria_emails = page.evaluate(
                """() => [...document.querySelectorAll('[aria-label]')]
                  .map(e => e.getAttribute('aria-label') || '')
                  .join('\\n')"""
            ) or ""
            emails |= set(
                re.findall(
                    r"[A-Za-z0-9._%+-]+@(?:gmail|googlemail)\.com", aria_emails, flags=re.I
                )
            )
        except Exception:
            pass
        if REQUIRED.lower() in {e.lower() for e in emails}:
            active = REQUIRED.lower()
        elif emails and active is None:
            active = sorted(emails)[0].lower()
        hits = [int(m.group(1).replace(",", "")) for m in CREDIT_RE.finditer(text)]
        if hits:
            near = [c for c in hits if 500 <= c <= 20000]
            credits = near[0] if near else max(hits)
        try:
            page.keyboard.press("Escape")
            time.sleep(0.4)
        except Exception:
            pass
    return credits, active


def assert_gate(page) -> dict:
    QA.mkdir(parents=True, exist_ok=True)
    text = page_text(page)
    low = text.lower()
    if any(x in low for x in ("passkey", "verifying it's you", "verifying it’s you", "use your passkey")):
        shot = QA / "gate_passkey.png"
        page.screenshot(path=str(shot), full_page=False)
        raise SystemExit(f"STOP passkey: {shot}")
    if "accounts.google.com" in (page.url or "") or "/about" in (page.url or ""):
        shot = QA / "gate_signed_out.png"
        page.screenshot(path=str(shot), full_page=False)
        raise SystemExit(f"STOP signed out: {page.url} {shot}")
    open_account_menu(page)
    credits, active = read_credits(page)
    shot = QA / "gate_auth_ok.png"
    page.screenshot(path=str(shot), full_page=False)
    try:
        page.keyboard.press("Escape")
    except Exception:
        pass
    # Re-read once if menu race left us empty
    if active is None or credits is None:
        time.sleep(1.0)
        open_account_menu(page)
        credits, active = read_credits(page)
        page.screenshot(path=str(shot), full_page=False)
        try:
            page.keyboard.press("Escape")
        except Exception:
            pass
    if active not in {REQUIRED.lower(), "benoats@gmail.com"}:
        raise SystemExit(f"STOP wrong account: {active} shot={shot}")
    if FORBIDDEN.lower() in low and (active or "").find("86") >= 0:
        raise SystemExit(f"STOP forbidden account: {active}")
    if credits is None:
        raise SystemExit(f"STOP credits unreadable shot={shot}")
    if credits == 0 or credits < 100:
        raise SystemExit(f"STOP low/zero credits={credits} shot={shot}")
    info = {
        "account": active,
        "credits": credits,
        "ultra": "ultra" in low,
        "shot": str(shot),
        "url": page.url,
    }
    print(f"GATE PASS account={active} credits={credits}", flush=True)
    return info


def abort_guards(page, stage: str) -> None:
    text = page_text(page)
    if SIGNED_OUT_RE.search(text) or "accounts.google.com" in (page.url or ""):
        raise SystemExit(f"STOP signed out at {stage}: {page.url}")
    if UNPAID_RE.search(text):
        shot = QA / f"unpaid_{stage}.png"
        try:
            page.screenshot(path=str(shot), full_page=False)
        except Exception:
            pass
        raise SystemExit(f"STOP unpaid/credits at {stage}: {shot}")


def auto_qa(mp4: Path) -> tuple[str, str]:
    dur = probe_dur(mp4)
    if dur < 4.0:
        return "FAIL", f"too short {dur:.2f}s"
    err = subprocess.run(
        [
            "ffmpeg", "-hide_banner", "-i", str(mp4),
            "-vf", "select='gt(scene,0.02)',showinfo", "-f", "null", "-",
        ],
        capture_output=True, text=True, errors="replace",
    ).stderr
    hits = len(re.findall(r"n:", err))
    if hits < 2 and dur > 5.0:
        return "FAIL", f"near-still scene_hits={hits}"
    size = mp4.stat().st_size
    if size < 400_000:
        return "FAIL", f"tiny file {size}"
    return "KEEP", f"motion_ok scene_hits={hits} dur={dur:.2f}s"


def archive_reject(mp4: Path, reason: str) -> Path:
    rej = RAW / "_rejected"
    rej.mkdir(parents=True, exist_ok=True)
    dest = rej / f"{mp4.stem}_{reason}_{int(time.time())}{mp4.suffix}"
    if mp4.exists():
        mp4.rename(dest)
    return dest


def get_flow_page(ctx):
    for pg in ctx.pages:
        u = pg.url or ""
        if "flow.google.com" in u and "/about" not in u:
            try:
                _ = pg.url  # touch
                return pg
            except Exception:
                continue
    page = ctx.new_page()
    page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
    time.sleep(3)
    return page


def refresh_page(browser, page):
    """Return a live Flow page; open a new one if the tab died."""
    try:
        _ = page.url
        if "flow.google.com" in (page.url or ""):
            return page
    except Exception:
        pass
    ctx = browser.contexts[0]
    page = get_flow_page(ctx)
    page.bring_to_front()
    if "/about" in (page.url or "") or "flow.google.com" not in (page.url or ""):
        page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
        time.sleep(3)
    flow.dismiss_banners(page)
    return page


def harvest_project_mp4(page, project_url: str, dest: Path, *, wait_s: int = 360) -> str:
    """Wait for gallery video thumb, play it, save mp4 from network capture.

    Flow Download-button path is unreliable on this CDP profile (Sep 2026);
    playing the clip reliably fires flow-content.google/video / googlevideo.
    """
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        dest.unlink()

    captured: list[bytes] = []

    def on_resp(resp) -> None:
        try:
            if resp.status != 200:
                return
            u = (resp.url or "").lower()
            ct = (resp.headers.get("content-type") or "").lower()
            if not (
                "flow-content.google/video" in u
                or "googlevideo.com" in u
                or "videoplayback" in u
                or ("video/mp4" in ct)
            ):
                return
            body = resp.body()
            if body and len(body) > 400_000 and b"ftyp" in body[:64]:
                captured.append(body)
                print(f"  net mp4 {len(body)}", flush=True)
        except Exception:
            pass

    page.on("response", on_resp)
    page.goto(project_url, wait_until="domcontentloaded", timeout=120_000)
    time.sleep(3)
    flow.dismiss_banners(page)

    t0 = time.time()
    before = set(flow.collect_gallery_asb_srcs(page))
    print(f"  harvest start thumbs={len(before)}", flush=True)
    while time.time() - t0 < wait_s:
        if captured:
            dest.write_bytes(max(captured, key=len))
            print(f"  harvest saved {dest.name} bytes={dest.stat().st_size} via=net", flush=True)
            return f"net:{dest.stat().st_size}"

        thumbs = flow.collect_gallery_asb_srcs(page)
        new = [s for s in thumbs if s not in before]
        body = page_text(page, 8000)
        low = body.lower()
        print(
            f"  harvest poll thumbs={len(thumbs)} new={len(new)} "
            f"captured={len(captured)} elapsed={time.time()-t0:.0f}s",
            flush=True,
        )
        # Real fail with no media — don't burn the full timeout
        if ("failed" in low or "couldn't generate" in low or "could not generate" in low) and not thumbs and time.time() - t0 > 75:
            raise RuntimeError(f"Flow generation failed (no thumbs) project={project_url}")
        if not thumbs and time.time() - t0 > 180:
            raise RuntimeError(f"no gallery thumbs after 180s project={project_url}")

        pick_src = new[-1] if new else (thumbs[-1] if thumbs and time.time() - t0 > 25 else None)
        if pick_src:
            try:
                page.locator(f'img[src="{pick_src}"]').first.click(timeout=8000)
            except Exception:
                try:
                    page.locator('img[src*="/asb/"]').last.click(timeout=8000)
                except Exception as e:
                    print(f"  thumb click warn: {e}", flush=True)
                    time.sleep(6)
                    continue
            time.sleep(1.5)
            # Prefer play → network capture (Download button often no-ops)
            for _ in range(3):
                try:
                    page.locator("video").first.click(timeout=2000)
                    time.sleep(2.5)
                except Exception:
                    pass
                if captured:
                    break
                time.sleep(1.5)
            if captured:
                dest.write_bytes(max(captured, key=len))
                print(f"  harvest saved {dest.name} bytes={dest.stat().st_size} via=play-net", flush=True)
                return f"play-net:{dest.stat().st_size}"
            # Fallback: library helper
            mid = flow.harvest_agent_gallery_mp4(page, dest, captured, before_asb=before)
            if mid and dest.exists() and dest.stat().st_size > 400_000:
                return mid
            if captured:
                dest.write_bytes(max(captured, key=len))
                return f"net-fallback:{dest.stat().st_size}"
        time.sleep(8)
        try:
            page.reload(wait_until="domcontentloaded", timeout=60_000)
            time.sleep(2)
            flow.dismiss_banners(page)
        except Exception:
            pass
    if captured:
        dest.write_bytes(max(captured, key=len))
        return f"net-late:{dest.stat().st_size}"
    raise RuntimeError(f"harvest timeout {wait_s}s project={project_url}")


def ensure_try_lists(plate_log: dict) -> None:
    if not isinstance(plate_log.get("try_detail"), list):
        plate_log["try_detail"] = []
    if not isinstance(plate_log.get("tries"), list):
        plate_log["tries"] = []


def plate_prompt(plate: dict, try_n: int) -> str:
    raw = plate["prompt_try2"] if try_n >= 2 and plate.get("prompt_try2") else plate["prompt"]
    # Strip QA reject boilerplate — it makes Flow fail silently on long prompts.
    for drop in (
        "HARD REJECT: Orbit, unfinished face, garbled cards, ATOMOS.",
        "HARD REJECT: Orbit, garbled text.",
        "HARD REJECT: Orbit, DNA helix, garbled letters.",
        "HARD REJECT: Orbit, Explorer, garbled H/O tiles.",
        "HARD REJECT: Orbit, Explorer, lava drip.",
        "HARD REJECT: Orbit.",
        "HARD REJECT: Orbit, photoreal chemistry lab, Explorer.",
        "HARD REJECT: Orbit, photoreal lab glassware hero, Explorer.",
        "HARD REJECT: garbled letters, Orbit.",
        "HARD REJECT: Orbit, Explorer.",
        "HARD REJECT: Orbit, Explorer, garbled scale numbers as hero.",
        "HARD REJECT: Orbit, garbled cards, unfinished face.",
        "HARD REJECT: Orbit, Explorer, lamp lava.",
        "HARD REJECT: Orbit, garbled fake letters, unfinished flat cards.",
        "HARD REJECT: garbled tiles, Orbit.",
        "HARD REJECT: Orbit, Explorer, garbled cards.",
        "HARD REJECT: Orbit, garbled letters, fake symbols.",
        "HARD REJECT: garbled text.",
        "HARD REJECT: Orbit, Explorer, filling gaps with garbled letters.",
        "HARD REJECT: Orbit, Explorer, ATOMOS, SEE labels.",
        "HARD REJECT: Orbit, garbled postage.",
        "HARD REJECT: Orbit, garbled Te/I, Explorer this plate.",
        "HARD REJECT: twins, no glasses, Orbit, Explorer parked all minute, garbled cards.",
        "HARD REJECT: twins, no glasses, Orbit.",
        "HARD REJECT: Orbit, garbled cards.",
        "HARD REJECT: Orbit, Explorer, Ken Burns only, lamp lava drip.",
        "HARD REJECT: Orbit, lava drip.",
        "HARD REJECT: Orbit, Explorer, Ken Burns only, SEE labels.",
        "Silent. No Explorer. No text labels in plate.",
        "Silent. No Explorer.",
        "Silent. No Explorer yet.",
        "Attach Explorer reference.",
    ):
        raw = raw.replace(drop, "")
    return " ".join(raw.split())


def mint_one(page, plate: dict, try_n: int, credits_before: int | None) -> dict:
    pid = plate["id"]
    model = model_for(plate)
    still = REFS / f"{pid}_v01.jpg"
    if not still.exists() or still.stat().st_size < 20_000:
        raise SystemExit(f"STOP: missing start frame {still}")

    dest = RAW / f"{pid}_t{try_n}.mp4"
    if dest.exists():
        dest.unlink()

    # Bypass orbit_flow_veo_ui.flow_prompt scenery_only clause ("no characters") —
    # Part 04 needs physicists / Explorer. Prefix triggers plain-body return.
    core = f"{STYLE} {plate_prompt(plate, try_n)}"
    if plate.get("explorer"):
        core += (
            " Exactly ONE Explorer: young boy, messy brown hair, round thin gold "
            "glasses, teal long coat, tan vest, brown bow tie, satchel. Acts then leaves."
        )
    else:
        core += " No Explorer."
    prompt = (
        "IMAGE-TO-VIDEO from text description (no attached still). "
        f"{core} Silent picture only. Continuous motion through the final frame."
    )

    print(
        f"\n=== MINT {pid} try={try_n} {quality_or_fast(plate)} model={model} "
        f"credits_before={credits_before} framing={'try2' if try_n >= 2 else 'try1'} "
        f"scenery_only chars={len(prompt)} ===",
        flush=True,
    )
    abort_guards(page, f"pre-{pid}-t{try_n}")
    try:
        flow.recover_flow_home(page)
    except Exception:
        pass
    info = flow.generate_clip(
        page,
        prompt,
        dest,
        model=model,
        timeout_s=120,
        start_frame=None,
        scenery_only=True,
        attempts=2,
        reuse_project=False,
    )
    abort_guards(page, f"post-{pid}-t{try_n}")

    project_url = (info or {}).get("project_url") or (info or {}).get("url") or ""
    if (info or {}).get("needs_gallery_harvest") or not dest.exists() or dest.stat().st_size < 400_000:
        if not project_url or "/project/" not in project_url:
            project_url = getattr(page, "_orbit_flow_project_url", None) or page.url or ""
        if "/project/" not in project_url:
            raise RuntimeError(f"no project URL for harvest after Create ({project_url!r})")
        print(f"  gallery harvest via {project_url}", flush=True)
        harvest_project_mp4(page, project_url, dest, wait_s=360)

    if not dest.exists() or dest.stat().st_size < 400_000:
        raise RuntimeError(f"no mp4 after harvest: {dest}")

    veo.strip_audio(dest)

    status, note = auto_qa(dest)
    credits_after, _ = read_credits(page)
    used = None
    if credits_before is not None and credits_after is not None:
        used = max(0, credits_before - credits_after)

    entry = {
        "id": pid,
        "try": try_n,
        "model": model,
        "quality_or_fast": quality_or_fast(plate),
        "framing": "try2_alt" if try_n >= 2 else "try1",
        "explorer": bool(plate.get("explorer")),
        "start_frame": str(still.relative_to(REPO)) if still.is_relative_to(REPO) else str(still),
        "start_frame_sha256": sha256_file(still),
        "out": str(dest),
        "file": str(dest.relative_to(REPO)) if dest.is_relative_to(REPO) else str(dest),
        "sha256": sha256_file(dest),
        "bytes": dest.stat().st_size,
        "duration_s": round(probe_dur(dest), 3),
        "status": status,
        "note": note,
        "credits_before": credits_before,
        "credits_used": used,
        "credits_remaining": credits_after,
        "project_url": project_url,
        "at": now(),
        "engine": "flow-ui Veo 3.1 scenery_only (CDP)",
        "path": "flow-cdp",
        "scenery_only": True,
    }
    return entry


def mint_one_gemini(client, plate: dict, try_n: int, credits_before: int | None) -> dict:
    """Same Veo 3.1 model via Gemini API — I2V from plate still. Never print keys."""
    from google.genai import types

    pid = plate["id"]
    model = gemini_model_for(plate)
    still = REFS / f"{pid}_v01.jpg"
    if not still.exists() or still.stat().st_size < 20_000:
        raise SystemExit(f"STOP: missing start frame for Gemini I2V {still}")

    dest = RAW / f"{pid}_t{try_n}.mp4"
    if dest.exists():
        dest.unlink()

    core = f"{STYLE} {plate_prompt(plate, try_n)}"
    if plate.get("explorer"):
        core += (
            " Exactly ONE Explorer: young boy, messy brown hair, round thin gold "
            "glasses, teal long coat, tan vest, brown bow tie, satchel. Acts then leaves."
        )
    else:
        core += " No Explorer."
    prompt = (
        f"{core} Silent picture only. Continuous motion through the final frame. "
        "HARD REJECT: photoreal, Ken Burns only, freeze frame, Orbit orange robot, "
        "DNA helix, lava drip, war gore, garbled text."
    )

    print(
        f"\n=== MINT {pid} try={try_n} {quality_or_fast(plate)} model={model} "
        f"path=gemini-api credits_before={credits_before} "
        f"framing={'try2' if try_n >= 2 else 'try1'} ===",
        flush=True,
    )
    t0 = time.time()
    config = types.GenerateVideosConfig(
        number_of_videos=1,
        duration_seconds=8,
        aspect_ratio="16:9",
        resolution="720p",
    )
    op = client.models.generate_videos(
        model=model,
        prompt=prompt,
        image=types.Image.from_file(location=str(still)),
        config=config,
    )
    while not op.done:
        time.sleep(12)
        op = client.operations.get(op)
        print(f"  gemini poll {pid} … {int(time.time() - t0)}s", flush=True)
    if getattr(op, "error", None):
        raise RuntimeError(op.error)
    resp = getattr(op, "response", None) or getattr(op, "result", None)
    videos = getattr(resp, "generated_videos", None) if resp else None
    if not videos:
        raise RuntimeError(f"no videos: {resp!r}")
    video = videos[0]
    dest.parent.mkdir(parents=True, exist_ok=True)
    client.files.download(file=video.video)
    video.video.save(str(dest))
    veo.strip_audio(dest)

    if not dest.exists() or dest.stat().st_size < 400_000:
        raise RuntimeError(f"no mp4 after Gemini download: {dest}")

    status, note = auto_qa(dest)
    entry = {
        "id": pid,
        "try": try_n,
        "model": model,
        "quality_or_fast": quality_or_fast(plate),
        "framing": "try2_alt" if try_n >= 2 else "try1",
        "explorer": bool(plate.get("explorer")),
        "start_frame": str(still.relative_to(REPO)) if still.is_relative_to(REPO) else str(still),
        "start_frame_sha256": sha256_file(still),
        "out": str(dest),
        "file": str(dest.relative_to(REPO)) if dest.is_relative_to(REPO) else str(dest),
        "sha256": sha256_file(dest),
        "bytes": dest.stat().st_size,
        "duration_s": round(probe_dur(dest), 3),
        "status": status,
        "note": note,
        "credits_before": credits_before,
        "credits_used": None,
        "credits_remaining": credits_before,
        "flow_credits_spent": 0,
        "api_seconds": round(time.time() - t0, 1),
        "at": now(),
        "engine": f"gemini-api Veo 3.1 ({model})",
        "path": "gemini-api",
        "reason": "flow_credit_buffer",
    }
    return entry


def promote_keep(log: dict, pid: str, try_n: int, entry: dict) -> Path:
    src = RAW / f"{pid}_t{try_n}.mp4"
    dest = RAW / f"{pid}_v01.mp4"
    if dest.exists():
        dest.unlink()
    src.rename(dest)
    entry["out"] = str(dest)
    entry["file"] = str(dest.relative_to(REPO))
    entry["sha256"] = sha256_file(dest)
    entry["status"] = "KEEP"
    plate = log["plates"].setdefault(pid, {"tries": [], "try_detail": []})
    plate["status"] = "KEEP"
    plate["keep"] = {
        "file": dest.name,
        "sha256": entry["sha256"],
        "try": try_n,
        "model": entry["model"],
        "quality_or_fast": entry["quality_or_fast"],
        "engine": entry.get("engine", "flow-cdp"),
        "path": entry.get("path", "flow-cdp"),
        "credits_used": entry.get("credits_used"),
        "credits_remaining": entry.get("credits_remaining"),
    }
    plate["model_keep"] = entry["model"]
    plate["quality_or_fast"] = entry["quality_or_fast"]
    plate["path"] = entry.get("path", "flow-cdp")
    plate["file"] = str(dest.relative_to(REPO))
    plate["sha256"] = entry["sha256"]
    plate["duration_s"] = entry["duration_s"]
    plate["bytes"] = entry["bytes"]
    save_log(log)
    return dest


def main() -> None:
    only = set(sys.argv[1:])  # optional plate ids
    RAW.mkdir(parents=True, exist_ok=True)
    QA.mkdir(parents=True, exist_ok=True)
    board = json.loads(PLATES_JSON.read_text())
    if not board.get("mint"):
        raise SystemExit("STOP: part-04 board mint:false")
    plates = board["plates"]
    if only:
        plates = [p for p in plates if p["id"] in only]
        if not plates:
            raise SystemExit(f"no plates matched {only}")

    missing_stills = [
        p["id"] for p in plates
        if not (REFS / f"{p['id']}_v01.jpg").exists()
        or (REFS / f"{p['id']}_v01.jpg").stat().st_size < 20_000
    ]
    if missing_stills:
        raise SystemExit(f"STOP missing stills: {missing_stills}")

    log = load_log()
    log["status"] = "FLOW_CDP_MINT_IN_PROGRESS"
    log["vo_status"] = "KEEP (v04)"
    log["engine_used"] = "flow-ui Veo 3.1 scenery_only via Mini CDP :9222"
    log["credit_fallback"] = {
        "buffer": FLOW_CREDIT_BUFFER,
        "fast_est": FLOW_COST_FAST_EST,
        "quality_est": FLOW_COST_QUALITY_EST,
        "gemini_fast": GEMINI_FAST_MODEL,
        "gemini_quality": GEMINI_QUALITY_MODEL,
        "rule": "if flow_credits - next_cost < 150 → gemini-api same Veo 3.1",
    }
    log["board"] = str(PLATES_JSON.relative_to(REPO))
    log["flow_ultra"] = {
        "account": REQUIRED,
        "profile": "~/.hos-chrome-flow-benoats-googlemail-cdp",
        "cdp": CDP,
    }
    save_log(log)

    gemini_client = None
    use_gemini_rest = False

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        ctx = browser.contexts[0]
        page = get_flow_page(ctx)
        page.bring_to_front()
        if "/about" in (page.url or "") or "flow.google.com" not in (page.url or ""):
            page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
            time.sleep(3)
        flow.dismiss_banners(page)
        gate = assert_gate(page)
        log["flow_ultra"]["credits_before"] = gate["credits"]
        log["flow_ultra"]["account_confirmed"] = gate["account"]
        log["flow_ultra"]["gate_shot"] = gate["shot"]
        log["credits_before_mint"] = gate["credits"]
        save_log(log)

        credits_cursor = gate["credits"]
        first_keep_seen = any(
            (log.get("plates", {}).get(pl["id"], {}).get("status") == "KEEP")
            for pl in board["plates"]
        )

        for plate in plates:
            pid = plate["id"]
            existing = log.get("plates", {}).get(pid, {})
            keep = existing.get("keep")
            keep_path = RAW / (keep["file"] if keep else f"{pid}_v01.mp4")
            if keep and keep_path.exists() and keep_path.stat().st_size > 400_000:
                print(f"SKIP {pid} already KEEP {keep_path.name}", flush=True)
                first_keep_seen = True
                continue
            if keep_path.exists() and keep_path.stat().st_size > 400_000 and not keep:
                print(f"SKIP {pid} file present {keep_path.name}", flush=True)
                first_keep_seen = True
                continue

            if not first_keep_seen:
                print(f"SERIAL (await first KEEP) → {pid}", flush=True)
            else:
                print(f"BATCH continue → {pid}", flush=True)

            plate_log = log["plates"].setdefault(
                pid,
                {"id": pid, "tries": [], "try_detail": [], "status": "PENDING"},
            )
            ensure_try_lists(plate_log)
            plate_log["status"] = "PENDING"

            if not use_gemini_rest:
                bal_check = credits_cursor
                try:
                    bal, _ = read_credits(page)
                    if bal is not None:
                        bal_check = bal
                        credits_cursor = bal
                except Exception:
                    pass
                if flow_would_breach_buffer(bal_check, plate):
                    print(
                        f"  FLOW BUFFER: credits={bal_check} "
                        f"next_est={estimate_flow_cost(plate)} "
                        f"buffer={FLOW_CREDIT_BUFFER} → Gemini Veo 3.1 API",
                        flush=True,
                    )
                    use_gemini_rest = True
                    log["credit_fallback"]["switched_at_plate"] = pid
                    log["credit_fallback"]["credits_at_switch"] = bal_check
                    log["engine_used"] = (
                        "flow-ui Veo 3.1 CDP until buffer; then gemini-api Veo 3.1"
                    )
                    save_log(log)

            if use_gemini_rest and gemini_client is None:
                gemini_client = load_gemini_client()

            kept = False
            for try_n in range(1, 3):
                ensure_try_lists(plate_log)
                if any(
                    isinstance(t, dict) and t.get("try") == try_n and t.get("status") == "KEEP"
                    for t in plate_log.get("try_detail", [])
                ):
                    kept = True
                    break
                credits_before = credits_cursor
                try:
                    if use_gemini_rest:
                        entry = mint_one_gemini(
                            gemini_client, plate, try_n, credits_before
                        )
                    else:
                        bal, _ = read_credits(page)
                        if bal is not None:
                            credits_before = bal
                            credits_cursor = bal
                        if flow_would_breach_buffer(credits_before, plate):
                            print(
                                f"  FLOW BUFFER mid-plate → Gemini for {pid}",
                                flush=True,
                            )
                            use_gemini_rest = True
                            if gemini_client is None:
                                gemini_client = load_gemini_client()
                            entry = mint_one_gemini(
                                gemini_client, plate, try_n, credits_before
                            )
                        else:
                            entry = mint_one(page, plate, try_n, credits_before)
                except SystemExit:
                    raise
                except Exception as e:
                    bal = credits_cursor
                    if not use_gemini_rest:
                        try:
                            bal, _ = read_credits(page)
                        except Exception:
                            pass
                    entry = {
                        "id": pid,
                        "try": try_n,
                        "model": (
                            gemini_model_for(plate)
                            if use_gemini_rest
                            else model_for(plate)
                        ),
                        "quality_or_fast": quality_or_fast(plate),
                        "framing": "try2_alt" if try_n >= 2 else "try1",
                        "status": "FAIL",
                        "note": f"exception {type(e).__name__}: {e}",
                        "credits_before": credits_before,
                        "credits_used": None,
                        "credits_remaining": bal,
                        "at": now(),
                        "engine": (
                            f"gemini-api Veo 3.1 ({gemini_model_for(plate)})"
                            if use_gemini_rest
                            else "flow-ui Veo 3.1 scenery_only (CDP)"
                        ),
                        "path": "gemini-api" if use_gemini_rest else "flow-cdp",
                    }
                    print(f"  FAIL exception: {e}", flush=True)
                    if (
                        not use_gemini_rest
                        and (
                            "Insufficient credits" in str(e)
                            or "Not enough credits" in str(e)
                        )
                    ):
                        print("  Flow out of credits → switch to Gemini", flush=True)
                        use_gemini_rest = True
                        ensure_try_lists(plate_log)
                        plate_log["try_detail"].append(entry)
                        plate_log["tries"].append(entry)
                        save_log(log)
                        if gemini_client is None:
                            gemini_client = load_gemini_client()
                        # retry this try_n via Gemini
                        try:
                            entry = mint_one_gemini(
                                gemini_client, plate, try_n, credits_before
                            )
                        except Exception as e2:
                            entry = {
                                "id": pid,
                                "try": try_n,
                                "model": gemini_model_for(plate),
                                "quality_or_fast": quality_or_fast(plate),
                                "framing": "try2_alt" if try_n >= 2 else "try1",
                                "status": "FAIL",
                                "note": f"exception {type(e2).__name__}: {e2}",
                                "credits_before": credits_before,
                                "credits_used": None,
                                "credits_remaining": credits_before,
                                "at": now(),
                                "engine": f"gemini-api Veo 3.1 ({gemini_model_for(plate)})",
                                "path": "gemini-api",
                            }
                            print(f"  FAIL gemini exception: {e2}", flush=True)

                ensure_try_lists(plate_log)
                plate_log["try_detail"].append(entry)
                plate_log["tries"].append(entry)
                if (
                    entry.get("credits_remaining") is not None
                    and entry.get("path") == "flow-cdp"
                ):
                    credits_cursor = entry["credits_remaining"]
                save_log(log)
                print(
                    f"  → {entry['status']} path={entry.get('path')} {entry.get('note')} "
                    f"used={entry.get('credits_used')} rem={entry.get('credits_remaining')} "
                    f"sha={(entry.get('sha256') or '')[:12]}",
                    flush=True,
                )
                if entry["status"] == "KEEP":
                    promote_keep(log, pid, try_n, entry)
                    print(
                        f"  KEEP {pid} → {pid}_v01.mp4 path={entry.get('path')}",
                        flush=True,
                    )
                    kept = True
                    first_keep_seen = True
                    break
                out_path = entry.get("out")
                if out_path and Path(out_path).exists():
                    archive_reject(Path(out_path), "auto_fail")
                note = entry.get("note") or ""
                if (
                    not use_gemini_rest
                    and (
                        "Insufficient credits" in note
                        or "Not enough credits" in note
                    )
                ):
                    print("  Flow insufficient → Gemini for remaining", flush=True)
                    use_gemini_rest = True
                    if gemini_client is None:
                        gemini_client = load_gemini_client()

            if not kept:
                plate_log["status"] = "FAIL"
                plate_log["fail_reason"] = (
                    "exhausted 2 tries without KEEP — framing already changed on try2"
                )
                save_log(log)
                print(f"  FAIL {pid} after 2 tries — leaving gap", flush=True)

        final_bal = credits_cursor
        try:
            final_bal, _ = read_credits(page)
        except Exception:
            pass
        log["credits_after_mint"] = final_bal
        log["flow_ultra"]["credits_after"] = final_bal
        before = log.get("credits_before_mint")
        if before is not None and final_bal is not None:
            log["credits_spent_total"] = max(0, before - final_bal)
        keep_n = sum(
            1
            for pl in board["plates"]
            if log.get("plates", {}).get(pl["id"], {}).get("status") == "KEEP"
            or log.get("plates", {}).get(pl["id"], {}).get("keep")
        )
        fail_n = len(board["plates"]) - keep_n
        path_counts: dict[str, int] = {}
        for pl in board["plates"]:
            row = log.get("plates", {}).get(pl["id"], {})
            path = (row.get("keep") or {}).get("path") or row.get("path") or "?"
            if row.get("status") == "KEEP" or row.get("keep"):
                path_counts[path] = path_counts.get(path, 0) + 1
        log["path_counts"] = path_counts
        log["status"] = (
            "FLOW_CDP_MINT_DONE" if fail_n == 0 else "FLOW_CDP_MINT_PARTIAL"
        )
        log["summary"] = {
            "keep": keep_n,
            "fail_or_missing": fail_n,
            "total_board_plates": len(board["plates"]),
            "path_counts": path_counts,
        }
        save_log(log)
        print(
            f"DONE before={before} after={final_bal} spent={log.get('credits_spent_total')} "
            f"keep={keep_n} fail={fail_n} paths={path_counts}",
            flush=True,
        )
        print(f"LOG {LOG}", flush=True)
        if fail_n:
            raise SystemExit(f"STOP: {fail_n} plates without KEEP")


if __name__ == "__main__":
    main()
