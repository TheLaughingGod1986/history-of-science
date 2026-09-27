#!/usr/bin/env python3
"""HOS 004 Part 02 — Flow Veo 3.1 mint via Mini CDP Chrome.

Ben 27 Sep 17:11 UK: Part 01 v05 PASS → mint Part 02 only.
Account: benoats@googlemail.com on :9222. No Gemini API for picture.
Quality only when plate.quality == Quality (glow). Fast otherwise.
Max 2 tries/plate; try2 uses prompt_try2 (framing change). Strip Veo audio.
One plate at a time until first KEEP, then continue the board (same CDP session).
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
PLATES_JSON = PROJ / "07_Edit-Project/parts/part-02_plates_v02.json"
REFS = PROJ / "04_Generated-Clips/part02/refs/v01_stills"
RAW = PROJ / "04_Generated-Clips/part02/raw/v01"
QA = PROJ / "07_Edit-Project/_qa_part02_mint_v01"
LOG = PROJ / "07_Edit-Project/PART02_MINT_LOG_v01.json"
EXPLORER_REF = (
    REPO / "01_Character/05_Generation-References/hos-explorer-reference-v01.jpg"
)

STYLE = (
    "History of Science locked look: premium Animistry-class 3D cartoon, warm "
    "cinematic light, period science world. Not photoreal. Not live-action. "
    "Silent picture. No Orbit orange robot. Continuous motion the whole clip — "
    "never a still push or Ken Burns. Readable faces when shown. Real element "
    "symbols only — never garbled tiles, never ATOMOS, never SEE labels."
)

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


def load_log() -> dict:
    if LOG.exists():
        return json.loads(LOG.read_text())
    return {
        "film": "004_Whats-Really-Inside-An-Atom",
        "part": "02",
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
    if any(x in low for x in ("passkey", "verifying it's you", "verifying it’s you", "use your passkey")):
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
            return pg
    page = ctx.new_page()
    page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
    time.sleep(3)
    return page


def harvest_project_mp4(page, project_url: str, dest: Path, *, wait_s: int = 480) -> str:
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
    print(f"  harvest start thumbs={len(before)}", flush=True)
    while time.time() - t0 < wait_s:
        thumbs = flow.collect_gallery_asb_srcs(page)
        new = [s for s in thumbs if s not in before]
        print(
            f"  harvest poll thumbs={len(thumbs)} new={len(new)} "
            f"captured={len(captured)} elapsed={time.time()-t0:.0f}s",
            flush=True,
        )
        pick_src = (new[-1] if new else (thumbs[-1] if thumbs and time.time() - t0 > 45 else None))
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
            time.sleep(2.5)
            for label in (r"Download media", r"^Download$", r"download"):
                try:
                    page.get_by_role("button", name=re.compile(label, re.I)).first.click(timeout=2000)
                    time.sleep(2)
                    break
                except Exception:
                    continue
            try:
                page.locator("video").first.click(timeout=1500)
                time.sleep(2)
            except Exception:
                pass
            for _ in range(20):
                if captured:
                    break
                time.sleep(1)
            if captured:
                dest.write_bytes(max(captured, key=len))
                print(f"  harvest saved {dest.name} bytes={dest.stat().st_size}", flush=True)
                return f"net:{dest.stat().st_size}"
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
    raise RuntimeError(f"harvest timeout {wait_s}s project={project_url}")


def ensure_try_lists(plate_log: dict) -> None:
    if not isinstance(plate_log.get("try_detail"), list):
        plate_log["try_detail"] = []
    if not isinstance(plate_log.get("tries"), list):
        plate_log["tries"] = []


def plate_prompt(plate: dict, try_n: int) -> str:
    if try_n >= 2 and plate.get("prompt_try2"):
        return plate["prompt_try2"]
    return plate["prompt"]


def mint_one(page, plate: dict, try_n: int, credits_before: int | None) -> dict:
    pid = plate["id"]
    model = model_for(plate)
    still = REFS / f"{pid}_v01.jpg"
    if not still.exists() or still.stat().st_size < 80_000:
        raise SystemExit(f"STOP: missing start frame {still}")

    dest = RAW / f"{pid}_t{try_n}.mp4"
    if dest.exists():
        dest.unlink()

    prompt = f"{STYLE} {plate_prompt(plate, try_n)}"
    if plate.get("explorer"):
        prompt += (
            " Exactly ONE Explorer matching the attached start frame "
            "(teal coat, round gold glasses). No twins."
        )
    else:
        prompt += " No Explorer in frame."

    print(
        f"\n=== MINT {pid} try={try_n} {quality_or_fast(plate)} model={model} "
        f"credits_before={credits_before} framing={'try2' if try_n >= 2 else 'try1'} ===",
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
        start_frame=still,
        scenery_only=False,
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
        harvest_project_mp4(page, project_url, dest, wait_s=520)

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
        "engine": "flow-ui Veo 3.1 start-frame I2V (CDP)",
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
        "engine": "flow-cdp",
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
    only = set(sys.argv[1:])  # optional plate ids
    RAW.mkdir(parents=True, exist_ok=True)
    QA.mkdir(parents=True, exist_ok=True)
    board = json.loads(PLATES_JSON.read_text())
    if not board.get("mint"):
        raise SystemExit("STOP: part-02 board mint:false")
    plates = board["plates"]
    if only:
        plates = [p for p in plates if p["id"] in only]
        if not plates:
            raise SystemExit(f"no plates matched {only}")

    missing_stills = [
        p["id"] for p in plates
        if not (REFS / f"{p['id']}_v01.jpg").exists()
        or (REFS / f"{p['id']}_v01.jpg").stat().st_size < 80_000
    ]
    if missing_stills:
        raise SystemExit(f"STOP missing stills: {missing_stills}")

    log = load_log()
    log["status"] = "FLOW_CDP_MINT_IN_PROGRESS"
    log["vo_status"] = "KEEP (v04)"
    log["engine_used"] = "flow-ui Veo 3.1 start-frame I2V via Mini CDP :9222"
    log["board"] = str(PLATES_JSON.relative_to(REPO))
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
        log["flow_ultra"]["credits_before"] = gate["credits"]
        log["flow_ultra"]["account_confirmed"] = gate["account"]
        log["flow_ultra"]["gate_shot"] = gate["shot"]
        log["credits_before_mint"] = gate["credits"]
        save_log(log)

        credits_cursor = gate["credits"]
        first_keep_seen = any(
            (log.get("plates", {}).get(p["id"], {}).get("status") == "KEEP")
            for p in board["plates"]
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
                # orphan file — treat as keep seed
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
                    bal, _ = read_credits(page)
                    if bal is not None:
                        credits_before = bal
                        credits_cursor = bal
                    entry = mint_one(page, plate, try_n, credits_before)
                except SystemExit:
                    raise
                except Exception as e:
                    bal, _ = read_credits(page)
                    entry = {
                        "id": pid,
                        "try": try_n,
                        "model": model_for(plate),
                        "quality_or_fast": quality_or_fast(plate),
                        "framing": "try2_alt" if try_n >= 2 else "try1",
                        "status": "FAIL",
                        "note": f"exception {type(e).__name__}: {e}",
                        "credits_before": credits_before,
                        "credits_used": None,
                        "credits_remaining": bal,
                        "at": now(),
                        "engine": "flow-ui Veo 3.1 start-frame I2V (CDP)",
                    }
                    print(f"  FAIL exception: {e}", flush=True)
                    if "Insufficient credits" in str(e) or "Not enough credits" in str(e):
                        ensure_try_lists(plate_log)
                        plate_log["try_detail"].append(entry)
                        plate_log["tries"].append(entry)
                        plate_log["status"] = "FAIL"
                        save_log(log)
                        raise SystemExit("STOP: Flow Ultra out of credits")

                ensure_try_lists(plate_log)
                plate_log["try_detail"].append(entry)
                plate_log["tries"].append(entry)
                if entry.get("credits_remaining") is not None:
                    credits_cursor = entry["credits_remaining"]
                save_log(log)
                print(
                    f"  → {entry['status']} {entry.get('note')} "
                    f"used={entry.get('credits_used')} rem={entry.get('credits_remaining')} "
                    f"sha={(entry.get('sha256') or '')[:12]}",
                    flush=True,
                )
                if entry["status"] == "KEEP":
                    promote_keep(log, pid, try_n, entry)
                    print(f"  KEEP {pid} → {pid}_v01.mp4", flush=True)
                    kept = True
                    first_keep_seen = True
                    break
                out_path = entry.get("out")
                if out_path and Path(out_path).exists():
                    archive_reject(Path(out_path), "auto_fail")
                note = entry.get("note") or ""
                if "Insufficient credits" in note or "Not enough credits" in note:
                    plate_log["status"] = "FAIL"
                    save_log(log)
                    raise SystemExit("STOP: Flow Ultra insufficient credits")

            if not kept:
                plate_log["status"] = "FAIL"
                plate_log["fail_reason"] = "exhausted 2 tries without KEEP — framing already changed on try2"
                save_log(log)
                print(f"  FAIL {pid} after 2 tries — leaving gap", flush=True)

        final_bal, _ = read_credits(page)
        log["credits_after_mint"] = final_bal
        log["flow_ultra"]["credits_after"] = final_bal
        before = log.get("credits_before_mint")
        if before is not None and final_bal is not None:
            log["credits_spent_total"] = max(0, before - final_bal)
        keep_n = sum(
            1
            for p in board["plates"]
            if log.get("plates", {}).get(p["id"], {}).get("status") == "KEEP"
            or log.get("plates", {}).get(p["id"], {}).get("keep")
        )
        fail_n = len(board["plates"]) - keep_n
        log["status"] = "FLOW_CDP_MINT_DONE" if fail_n == 0 else "FLOW_CDP_MINT_PARTIAL"
        log["summary"] = {
            "keep": keep_n,
            "fail_or_missing": fail_n,
            "total_board_plates": len(board["plates"]),
        }
        save_log(log)
        print(
            f"DONE before={before} after={final_bal} spent={log.get('credits_spent_total')} "
            f"keep={keep_n} fail={fail_n}",
            flush=True,
        )
        print(f"LOG {LOG}", flush=True)
        if fail_n:
            raise SystemExit(f"STOP: {fail_n} plates without KEEP")


if __name__ == "__main__":
    main()
