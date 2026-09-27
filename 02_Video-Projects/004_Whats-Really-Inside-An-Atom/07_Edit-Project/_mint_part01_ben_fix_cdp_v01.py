#!/usr/bin/env python3
"""HOS 004 Part 01 — Flow remint of Ben's 3 FAIL scenes (4 plates).

Ben UAT 27 Sep 16:00 UK on rough v03:
  Image 1 → 12_1913_targets (Quality — glow in tube, no laser-to-head)
  Image 2 → 09_uncuttable_blur (Fast — no character / no Explorer)
  Image 3 → 01_coin_halves + 15_knife_coin_return (Fast — successive halvings spine)

Flow Ultra CDP :9222 as benoats@googlemail.com only.
scenery_only (new framing — do NOT reuse bad start frames).
Max 2 tries/plate; try 2 changes framing. Strip Veo audio. No Gemini.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
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
PLATES_JSON = PROJ / "07_Edit-Project/parts/part-01_plates_v02.json"
RAW = PROJ / "04_Generated-Clips/part01/raw/v01"
QA = PROJ / "07_Edit-Project/_qa_part01_ben_fix_v01"
LOG = PROJ / "07_Edit-Project/PART01_MINT_LOG_v01.json"

# Order: coin open → blur → xray glow → coin return
REFIX = [
    "01_coin_halves",
    "09_uncuttable_blur",
    "12_1913_targets",
    "15_knife_coin_return",
]
QUALITY_IDS = {"12_1913_targets"}

FRAMING_TRY2 = {
    "01_coin_halves": (
        " FRAMING CHANGE try2: extreme close-up top-down on the coin face; "
        "knife enters from top; three hard cut beats with a punch-in after each "
        "halving; no wide classroom; no wall diagrams."
    ),
    "09_uncuttable_blur": (
        " FRAMING CHANGE try2: ECU through magnifying glass only — soft empty "
        "blur fills frame; no lab floor walk; no wall tiles at all; no figure."
    ),
    "12_1913_targets": (
        " FRAMING CHANGE try2: medium shot of tube + targets only; physicist "
        "stands beside apparatus looking at targets, never in the beam path; "
        "camera dolly along glowing targets; zero floor signage."
    ),
    "15_knife_coin_return": (
        " FRAMING CHANGE try2: tight bench hero of knife across nested coin "
        "halves; slow settle; no scientist OC; no giant table."
    ),
}

STYLE = (
    "History of Science locked look: premium Animistry-class 3D cartoon, warm "
    "cinematic light, period science world. Not photoreal. Not live-action. "
    "Silent picture. No Orbit orange robot. No Explorer. Continuous motion the "
    "whole clip — never a still push or Ken Burns. Readable faces and letters "
    "when the beat needs them."
)

CREDIT_RE = re.compile(r"([\d,]{1,7})\s*(?:Google\s+Flow\s+)?credits", re.I)
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


def model_for(plate_id: str) -> str:
    return "Veo 3.1 - Quality" if plate_id in QUALITY_IDS else "Veo 3.1 - Fast"


def quality_or_fast(plate_id: str) -> str:
    return "Quality" if plate_id in QUALITY_IDS else "Fast"


def load_log() -> dict:
    if LOG.exists():
        return json.loads(LOG.read_text())
    return {"film": "004_Whats-Really-Inside-An-Atom", "part": "01", "plates": {}}


def save_log(log: dict) -> None:
    log["updated_at"] = now()
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
    if any(x in low for x in ("passkey", "verifying it's you", "verifying it’s you")):
        shot = QA / "gate_passkey.png"
        page.screenshot(path=str(shot), full_page=False)
        raise SystemExit(f"STOP passkey: {shot}")
    if "accounts.google.com" in (page.url or "") or "/about" in (page.url or ""):
        shot = QA / "gate_signed_out.png"
        page.screenshot(path=str(shot), full_page=False)
        raise SystemExit(f"STOP signed out: {page.url} {shot}")
    credits, active = read_credits(page)
    shot = QA / "gate_auth_ok.png"
    open_account_menu(page)
    page.screenshot(path=str(shot), full_page=False)
    try:
        page.keyboard.press("Escape")
    except Exception:
        pass
    if active not in {REQUIRED.lower(), "benoats@gmail.com"}:
        raise SystemExit(f"STOP wrong account: {active} shot={shot}")
    if credits is None or credits < 500:
        raise SystemExit(f"STOP low/zero credits={credits} shot={shot}")
    print(f"GATE PASS account={active} credits={credits}", flush=True)
    return {"account": active, "credits": credits, "shot": str(shot), "url": page.url}


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
    if mp4.stat().st_size < 400_000:
        return "FAIL", f"tiny file {mp4.stat().st_size}"
    return "KEEP", f"motion_ok scene_hits={hits} dur={dur:.2f}s"


def get_flow_page(ctx):
    for pg in ctx.pages:
        u = pg.url or ""
        if "flow.google.com" in u and "/about" not in u:
            return pg
    page = ctx.new_page()
    page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
    time.sleep(3)
    return page


def harvest_project_mp4(page, project_url: str, dest: Path, *, wait_s: int = 520) -> str:
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
    while time.time() - t0 < wait_s:
        thumbs = flow.collect_gallery_asb_srcs(page)
        new = [s for s in thumbs if s not in before]
        print(
            f"  harvest poll thumbs={len(thumbs)} new={len(new)} "
            f"captured={len(captured)} elapsed={time.time()-t0:.0f}s",
            flush=True,
        )
        pick_src = new[-1] if new else (thumbs[-1] if thumbs and time.time() - t0 > 45 else None)
        if pick_src:
            try:
                page.locator(f'img[src="{pick_src}"]').first.click(timeout=8000)
            except Exception:
                try:
                    page.locator('img[src*="/asb/"]').last.click(timeout=8000)
                except Exception:
                    time.sleep(6)
                    continue
            time.sleep(2.5)
            for label in (r"Download media", r"^Download$", r"download"):
                try:
                    page.get_by_role("button", name=re.compile(label, re.I)).first.click(timeout=2000)
                    time.sleep(2)
                    break
                except Exception:
                    continue
            for _ in range(20):
                if captured:
                    break
                time.sleep(1)
            if captured:
                dest.write_bytes(max(captured, key=len))
                return f"net:{dest.stat().st_size}"
            mid = flow.harvest_agent_gallery_mp4(page, dest, captured, before_asb=before)
            if mid and dest.exists() and dest.stat().st_size > 400_000:
                return mid
        time.sleep(8)
        try:
            page.reload(wait_until="domcontentloaded", timeout=60_000)
            time.sleep(2)
            flow.dismiss_banners(page)
        except Exception:
            pass
    raise RuntimeError(f"harvest timeout {wait_s}s project={project_url}")


def ensure_try_lists(plate_log: dict) -> None:
    if not isinstance(plate_log.get("try_detail"), list):
        plate_log["try_detail"] = []
    if not isinstance(plate_log.get("tries"), list):
        plate_log["tries"] = []


def archive_old_keep(pid: str) -> Path | None:
    old = RAW / f"{pid}_v01.mp4"
    if not old.exists():
        return None
    rej = RAW / "_rejected"
    rej.mkdir(parents=True, exist_ok=True)
    dest = rej / f"{pid}_v01_pre_ben_fix_{int(time.time())}.mp4"
    shutil.move(str(old), str(dest))
    print(f"  archived old KEEP → {dest.name}", flush=True)
    return dest


def mint_one(page, plate: dict, try_n: int, credits_before: int | None) -> dict:
    pid = plate["id"]
    model = model_for(pid)
    dest = RAW / f"{pid}_benfix_t{try_n}.mp4"
    if dest.exists():
        dest.unlink()

    prompt = f"{STYLE} {plate['prompt']}"
    if try_n >= 2:
        prompt += FRAMING_TRY2.get(pid, " FRAMING CHANGE try2: new camera angle, tighter subject.")

    print(
        f"\n=== REMINT {pid} try={try_n} {quality_or_fast(pid)} model={model} "
        f"credits_before={credits_before} scenery_only ===",
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
        timeout_s=180,
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
            raise RuntimeError(f"no project URL for harvest ({project_url!r})")
        print(f"  gallery harvest via {project_url}", flush=True)
        harvest_project_mp4(page, project_url, dest, wait_s=520)

    if not dest.exists() or dest.stat().st_size < 400_000:
        raise RuntimeError(f"no mp4 after harvest: {dest}")

    veo.strip_audio(dest)
    status, note = auto_qa(dest)
    credits_after, _ = read_credits(page)
    used = None
    if credits_before is not None and credits_after is not None:
        used = max(0, credits_before - credits_after)

    return {
        "id": pid,
        "try": try_n,
        "model": model,
        "quality_or_fast": quality_or_fast(pid),
        "ben_fix": True,
        "scenery_only": True,
        "out": str(dest),
        "file": str(dest.relative_to(REPO)),
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
        "engine": "flow-ui Veo 3.1 scenery_only (CDP) ben-fix",
        "image_map": {
            "01_coin_halves": "Image 3 coin/knife open",
            "15_knife_coin_return": "Image 3 coin spine return",
            "09_uncuttable_blur": "Image 2 little man / fake tiles",
            "12_1913_targets": "Image 1 beam-to-head / ATOMOS",
        }.get(pid),
    }


def promote_keep(log: dict, pid: str, try_n: int, entry: dict) -> Path:
    archive_old_keep(pid)
    src = RAW / f"{pid}_benfix_t{try_n}.mp4"
    dest = RAW / f"{pid}_v01.mp4"
    if dest.exists():
        dest.unlink()
    shutil.move(str(src), str(dest))
    entry["out"] = str(dest)
    entry["file"] = str(dest.relative_to(REPO))
    entry["sha256"] = sha256_file(dest)
    entry["status"] = "KEEP"
    plate = log["plates"].setdefault(pid, {"tries": [], "try_detail": []})
    ensure_try_lists(plate)
    plate["status"] = "KEEP"
    plate["ben_fix_2026_09_27"] = True
    plate["keep"] = {
        "file": dest.name,
        "sha256": entry["sha256"],
        "try": try_n,
        "model": entry["model"],
        "quality_or_fast": entry["quality_or_fast"],
        "engine": "flow-cdp-ben-fix",
        "credits_used": entry.get("credits_used"),
        "credits_remaining": entry.get("credits_remaining"),
    }
    plate["model_keep"] = entry["model"]
    plate["quality_or_fast"] = entry["quality_or_fast"]
    plate["file"] = str(dest.relative_to(REPO))
    plate["sha256"] = entry["sha256"]
    plate["duration_s"] = entry["duration_s"]
    plate["bytes"] = entry["bytes"]
    save_log(log)
    return dest


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    QA.mkdir(parents=True, exist_ok=True)
    board = json.loads(PLATES_JSON.read_text())
    by_id = {p["id"]: p for p in board["plates"]}
    todo = [by_id[i] for i in REFIX]

    log = load_log()
    log["status"] = "FLOW_CDP_BEN_FIX_IN_PROGRESS"
    log["ben_fix_2026_09_27"] = {
        "mapping": {
            "Image_1_beam_ATOMOS": "12_1913_targets @ 52.748s",
            "Image_2_helmet_fake_tiles": "09_uncuttable_blur @ 36.091s",
            "Image_3_coin_knife_ATOM": "01_coin_halves @ 0.000s (+ 15_knife_coin_return @ 63.853s spine)",
        },
        "plates": REFIX,
    }
    log["engine_used"] = "flow-ui Veo 3.1 scenery_only via Mini CDP :9222"
    log["flow_ultra"] = {
        "account": REQUIRED,
        "profile": "~/.hos-chrome-flow-benoats-googlemail-cdp",
        "cdp": CDP,
    }
    save_log(log)

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
        log["ben_fix_2026_09_27"]["credits_before"] = gate["credits"]
        log["credits_before_ben_fix"] = gate["credits"]
        save_log(log)

        credits_cursor = gate["credits"]
        results = []
        for plate in todo:
            pid = plate["id"]
            plate_log = log["plates"].setdefault(pid, {"tries": [], "try_detail": []})
            ensure_try_lists(plate_log)
            kept = False
            for try_n in (1, 2):
                # refresh credits before each try (avoid daily-50 chip)
                try:
                    flow.recover_flow_home(page)
                except Exception:
                    pass
                credits_cursor, _ = read_credits(page)
                try:
                    entry = mint_one(page, plate, try_n, credits_cursor)
                except SystemExit:
                    raise
                except Exception as e:
                    entry = {
                        "id": pid,
                        "try": try_n,
                        "model": model_for(pid),
                        "quality_or_fast": quality_or_fast(pid),
                        "status": "FAIL",
                        "note": f"exception {type(e).__name__}: {e}"[:400],
                        "credits_before": credits_cursor,
                        "credits_used": None,
                        "credits_remaining": credits_cursor,
                        "at": now(),
                        "engine": "flow-ui Veo 3.1 scenery_only (CDP) ben-fix",
                    }
                    print(f"  FAIL exception: {e}", flush=True)

                plate_log["try_detail"].append(entry)
                plate_log["tries"].append(entry)
                save_log(log)

                if entry.get("credits_remaining") is not None:
                    credits_cursor = entry["credits_remaining"]

                if entry["status"] == "KEEP":
                    promote_keep(log, pid, try_n, entry)
                    results.append({"id": pid, "status": "KEEP", "try": try_n, **{k: entry.get(k) for k in ("sha256", "quality_or_fast", "credits_used", "credits_remaining")}})
                    kept = True
                    break

                # archive fail try file
                fail_path = Path(entry.get("out") or RAW / f"{pid}_benfix_t{try_n}.mp4")
                if fail_path.exists():
                    rej = RAW / "_rejected"
                    rej.mkdir(parents=True, exist_ok=True)
                    fail_path.rename(rej / f"{fail_path.stem}_FAIL_{int(time.time())}.mp4")

            if not kept:
                plate_log["status"] = "FAIL"
                save_log(log)
                results.append({"id": pid, "status": "FAIL"})
                print(f"FAIL {pid} after 2 tries", flush=True)

        credits_after, _ = read_credits(page)
        log["status"] = "FLOW_CDP_BEN_FIX_DONE"
        log["ben_fix_2026_09_27"]["credits_after"] = credits_after
        log["ben_fix_2026_09_27"]["credits_spent"] = (
            None
            if gate["credits"] is None or credits_after is None
            else max(0, gate["credits"] - credits_after)
        )
        log["ben_fix_2026_09_27"]["results"] = results
        log["credits_after_ben_fix"] = credits_after
        save_log(log)
        print("\n=== BEN FIX DONE ===", flush=True)
        print(json.dumps(log["ben_fix_2026_09_27"], indent=2), flush=True)


if __name__ == "__main__":
    main()
