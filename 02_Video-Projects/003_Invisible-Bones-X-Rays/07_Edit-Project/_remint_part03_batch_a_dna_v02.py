#!/usr/bin/env python3
"""HOS 003 Part 03 Batch A — remint 8 DNA-helix HARD FAIL plates → v02.

KEEP untouched: 01_chapter_bones, 03_soft_fades, 07_explorer_hand_beam.
Assemble stays CLOSED. Flow project pinned. Veo 3.1 Quality. ULTRA googlemail.

Unpaid/payment fail on Create: ONE refresh + one Create retry only (no charge-loop).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))

import orbit_flow_veo_ui as flow  # noqa: E402
import orbit_gemini_veo as veo  # noqa: E402

PROJECT_URL = (
    "https://flow.google.com/project/537a3344-5ba3-46c3-b727-4e166601d9d0"
)
ACCOUNT = "benoats@googlemail.com"
MODEL = "Veo 3.1 - Quality"
CLIP_DIR = (
    REPO
    / "02_Video-Projects"
    / "003_Invisible-Bones-X-Rays"
    / "04_Generated-Clips"
    / "part03"
)
QA_DIR = (
    REPO
    / "02_Video-Projects"
    / "003_Invisible-Bones-X-Rays"
    / "07_Edit-Project"
    / "_qa_part03_batch_a"
)
PROMPTS_PATH = QA_DIR / "REMINT_PROMPTS_v02.json"
INDEX_PATH = QA_DIR / "BATCH_A_REMINT_LAND_INDEX.json"

KEEP = {
    "01_chapter_bones_v01.mp4": "ebb64736279d6455d062e740d154d272ead839662eca7865ef4eb0e0a61aafc6",
    "03_soft_fades_v01.mp4": "5278f40d88f7c65949c773dbdf31633d94200d8badd67a6fe77a712a1e275b1a",
    "07_explorer_hand_beam_v01.mp4": "2c938277d3f743fe459ae5bd935adb5dd1bdad80538951a56b08a76e0599617a",
}
# Index is source of truth for KEEP shas (user handoff had a 1-char typo on 01).
KEEP_FROM_INDEX = True

REMINT_ORDER = [
    "02_hand_enters_path",
    "04_bones_hold",
    "05_ring_darker",
    "06_living_skeleton_read",
    "08_medicine_question",
    "09_wonder",
    "10_caution_burn",
    "11_hold_beam",
]

MUTE_NOTES = {
    "02_hand_enters_path": "Mute: faceless hand enters green-violet beam path; clean lab; no helix.",
    "04_bones_hold": "Mute: bones hold clearer than soft tissue on clean palm; no helix.",
    "05_ring_darker": "Mute: denser/darker ring on bone silhouette; no helix.",
    "06_living_skeleton_read": "Mute: living skeleton read / NO KNIFE; clean desk; no helix.",
    "08_medicine_question": "Mute: cardboard/CRT + empty beam read medicine question; no helix.",
    "09_wonder": "Mute: wonder bone silhouette clear; no helix.",
    "10_caution_burn": "Mute: caution/burn intensity + soft heat shimmer; no helix.",
    "11_hold_beam": "Mute: beam + cardboard hold readable (not neon-only); no helix.",
}

UNPAID_RE = re.compile(
    r"unpaid|payment (failed|error)|couldn.?t (charge|process)|billing|"
    r"add a payment|update (your )?payment|purchase failed|transaction failed",
    re.I,
)
SIGNED_OUT_RE = re.compile(
    r"you.?re not signed in|session ended because there was no activity|"
    r"try signing in again|sign in to continue",
    re.I,
)
UNUSUAL_RE = re.compile(
    r"unusual activity|suspicious activity|verify it.?s you|"
    r"confirm you.?re not a robot|automated quer|"
    r"too many (requests|attempts)|try again later|unusual traffic|"
    r"couldn.?t verify|(?<!re)captcha|are you a robot",
    re.I,
)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def probe_dur(path: Path) -> float:
    return float(
        subprocess.check_output(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=nw=1:nk=1",
                str(path),
            ],
            text=True,
        ).strip()
    )


def page_text(page, n: int = 12000) -> str:
    try:
        return page.locator("body").inner_text(timeout=8000)[:n]
    except Exception:
        return ""


def keep_shas() -> dict[str, str]:
    out: dict[str, str] = {}
    land = QA_DIR / "BATCH_A_LAND_INDEX.json"
    if KEEP_FROM_INDEX and land.exists():
        data = json.loads(land.read_text())
        for p in data.get("plates", []):
            if p["id"] in ("01_chapter_bones", "03_soft_fades", "07_explorer_hand_beam"):
                out[Path(p["path"]).name] = p["sha256"]
    for name, fallback in KEEP.items():
        out.setdefault(name, fallback)
    return out


def assert_keeps(before: dict[str, str]) -> None:
    for name, want in before.items():
        p = CLIP_DIR / name
        if not p.exists():
            raise SystemExit(f"STOP: KEEP missing {p}")
        got = sha256_file(p)
        if got != want:
            raise SystemExit(f"STOP: KEEP mutated {name}\n want {want}\n got  {got}")


def extract_qa_frames(mp4: Path, plate: str) -> None:
    QA_DIR.mkdir(parents=True, exist_ok=True)
    dur = probe_dur(mp4)
    stamps = {
        "start": 0.4,
        "mid": max(0.5, dur / 2.0),
        "end": max(0.5, dur - 0.6),
    }
    for name, t in stamps.items():
        dest = QA_DIR / f"{plate}_v02_{name}.jpg"
        subprocess.check_call(
            [
                "ffmpeg",
                "-y",
                "-ss",
                f"{t:.2f}",
                "-i",
                str(mp4),
                "-frames:v",
                "1",
                "-q:v",
                "3",
                str(dest),
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )


def abort_guards(page, stage: str) -> None:
    text = page_text(page)
    if UNUSUAL_RE.search(text) and not (
        re.search(r"protected by recaptcha", text, re.I)
        and not re.search(r"unusual activity|suspicious activity|verify it.?s you", text, re.I)
    ):
        shot = QA_DIR / f"unusual_{stage}.png"
        try:
            page.screenshot(path=str(shot), full_page=False)
        except Exception:
            pass
        raise SystemExit(f"STOP unusual activity at {stage}: {shot}")
    if SIGNED_OUT_RE.search(text) or "accounts.google.com" in (page.url or ""):
        raise SystemExit(f"STOP signed out at {stage}: {page.url}")


def unpaid_visible(page) -> bool:
    return bool(UNPAID_RE.search(page_text(page, 8000)))


def harvest_newest(page, dest: Path, before_ids: set[str]) -> str | None:
    ids = flow.collect_media_ids(page)
    new_ids = [i for i in ids if i not in before_ids] or list(ids)
    for mid in reversed(new_ids):
        url = flow.absolute_media_url(mid)
        try:
            head = page.request.get(url, timeout=60_000)
            body = head.body()
            if len(body) > 150_000 and body[:64].find(b"ftyp") >= 0:
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(body)
                print(f"  harvested mid={mid[:48]}… bytes={len(body)}", flush=True)
                return mid
        except Exception as e:
            print(f"  harvest mid err {type(e).__name__}: {e}", flush=True)
    vsrc = page.evaluate(
        """() => {
          const vs = [...document.querySelectorAll('video')]
            .map(v => v.currentSrc || v.src)
            .filter(Boolean);
          return vs.length ? vs[vs.length - 1] : null;
        }"""
    )
    if vsrc and vsrc.startswith("http") and flow.is_flow_video_url(vsrc):
        head = page.request.get(vsrc, timeout=60_000)
        body = head.body()
        if len(body) > 150_000 and body[:64].find(b"ftyp") >= 0:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(body)
            print(f"  harvested video src bytes={len(body)}", flush=True)
            return vsrc
    return None


def wait_create(page, dest: Path, before_ids: set[str], timeout_s: int) -> str:
    t0 = time.time()
    last = ""
    while time.time() - t0 < timeout_s:
        abort_guards(page, f"wait-{int(time.time()-t0)}")
        body = page_text(page, 4000).lower()
        if "generation quota for today" in body or "reached your generation quota" in body:
            raise SystemExit("STOP: Flow daily generation quota")
        if unpaid_visible(page):
            raise RuntimeError("UNPAID_FAIL")
        if re.search(r"\bfailed\b", body) and re.search(r"generat|create|video", body):
            # unpaid often surfaces as failed — distinguish
            if unpaid_visible(page):
                raise RuntimeError("UNPAID_FAIL")
            raise SystemExit("STOP: Flow failed banner (no unpaid match)")
        hit = harvest_newest(page, dest, before_ids)
        if hit:
            return hit
        elapsed = int(time.time() - t0)
        status = "…"
        for k in ("generating", "thinking", "queue", "high demand", "creating", "working"):
            if k in body:
                status = k
                break
        line = f"  wait {elapsed}s status={status}"
        if line != last:
            print(line, flush=True)
            last = line
        page.wait_for_timeout(4000)
    raise TimeoutError(f"Flow video not ready after {timeout_s}s")


def one_create(page, prompt: str, dest: Path, timeout_s: int) -> dict:
    abort_guards(page, "pre-settings")
    flow.configure_veo_settings(
        page, model=MODEL, frames_mode=False, ingredients_mode=False
    )
    abort_guards(page, "post-settings")
    selected = flow.read_selected_video_model(page) or ""
    print(f"  selected model={selected!r}", flush=True)
    before_ids = flow.collect_media_ids(page)
    flow.ensure_agent_session(page)
    flow.set_prompt(page, flow.flow_prompt(prompt, scenery_only=True))
    abort_guards(page, "pre-create")
    print("  submitting ONE Create…", flush=True)
    flow.submit_create(page)
    flow.settle_after_nav(page, wait_ms=1200)
    abort_guards(page, "post-create")
    try:
        flow.confirm_generation_spend(page, timeout_s=8.0)
    except Exception as e:
        print(f"  confirm spend: {e}", flush=True)
    # Early unpaid check
    page.wait_for_timeout(2500)
    if unpaid_visible(page):
        raise RuntimeError("UNPAID_FAIL")
    media = wait_create(page, dest, before_ids, timeout_s)
    return {"media": media, "selected_model": selected}


def remint_plate(page, plate: str, prompt: str, timeout_s: int) -> dict:
    dest = CLIP_DIR / f"{plate}_v02.mp4"
    if dest.exists():
        raise SystemExit(f"STOP: dest already exists {dest}")
    unpaid_retry = False
    try:
        meta = one_create(page, prompt, dest, timeout_s)
    except RuntimeError as e:
        if str(e) != "UNPAID_FAIL":
            raise
        unpaid_retry = True
        print("  UNPAID/payment fail — ONE refresh retry only…", flush=True)
        page.reload(wait_until="domcontentloaded", timeout=120_000)
        flow.settle_after_nav(page, wait_ms=2000)
        flow.dismiss_banners(page)
        abort_guards(page, "post-refresh")
        if "537a3344-5ba3-46c3-b727-4e166601d9d0" not in (page.url or ""):
            page.goto(PROJECT_URL, wait_until="domcontentloaded", timeout=120_000)
            flow.settle_after_nav(page, wait_ms=2000)
        try:
            meta = one_create(page, prompt, dest, timeout_s)
        except RuntimeError as e2:
            if str(e2) == "UNPAID_FAIL":
                raise SystemExit(
                    "STOP: unpaid fail after one refresh retry — no charge-loop"
                )
            raise
    if not dest.exists() or dest.stat().st_size < 150_000:
        raise SystemExit(f"STOP: dest missing/small {dest}")
    veo.strip_audio(dest)
    dur = probe_dur(dest)
    if dur < 6.0 or dur > 12.0:
        raise SystemExit(f"STOP: unexpected duration {dur:.2f}s")
    extract_qa_frames(dest, plate)
    report = {
        "plate": plate,
        "version": "v02",
        "path": str(dest),
        "bytes": dest.stat().st_size,
        "sha256": sha256_file(dest),
        "duration_s": dur,
        "model": MODEL,
        "selected_model": meta.get("selected_model"),
        "unpaid_refresh_retry": unpaid_retry,
        "mute_note": MUTE_NOTES[plate],
        "project": PROJECT_URL,
        "account": ACCOUNT,
        "assemble": "CLOSED",
        "ts": datetime.now(timezone.utc).isoformat(),
    }
    (QA_DIR / f"{plate}_v02_mint.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    print(json.dumps(report, indent=2), flush=True)
    return report


def write_index(reports: list[dict]) -> None:
    idx = {
        "film": "003_Invisible-Bones-X-Rays",
        "part": 3,
        "batch": "A_REMINT_DNA",
        "account": ACCOUNT,
        "model": MODEL,
        "project": PROJECT_URL,
        "assemble": "CLOSED",
        "keep_untouched": [
            "01_chapter_bones_v01.mp4",
            "03_soft_fades_v01.mp4",
            "07_explorer_hand_beam_v01.mp4",
        ],
        "plates_reminted": len(reports),
        "plates": [
            {
                "id": r["plate"],
                "version": r["version"],
                "path": r["path"],
                "sha256": r["sha256"],
                "bytes": r["bytes"],
                "duration_s": r["duration_s"],
                "mute_note": r["mute_note"],
                "unpaid_refresh_retry": r.get("unpaid_refresh_retry", False),
            }
            for r in reports
        ],
        "ts": datetime.now(timezone.utc).isoformat(),
    }
    INDEX_PATH.write_text(json.dumps(idx, indent=2), encoding="utf-8")
    print(f"INDEX → {INDEX_PATH}", flush=True)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--cdp", default=os.environ.get("HOS_003_FLOW_CDP", ""))
    ap.add_argument("--timeout", type=int, default=900)
    ap.add_argument("--only", nargs="*", default=None)
    ap.add_argument("--probe-only", action="store_true")
    args = ap.parse_args()

    prompts = json.loads(PROMPTS_PATH.read_text())["plates"]
    plates = args.only or REMINT_ORDER
    for p in plates:
        if p not in prompts:
            raise SystemExit(f"STOP: unknown plate {p}")
        if p in ("01_chapter_bones", "03_soft_fades", "07_explorer_hand_beam"):
            raise SystemExit(f"STOP: refuse KEEP remint {p}")

    before = keep_shas()
    assert_keeps(before)
    QA_DIR.mkdir(parents=True, exist_ok=True)
    CLIP_DIR.mkdir(parents=True, exist_ok=True)

    from playwright.sync_api import sync_playwright

    reports: list[dict] = []
    with sync_playwright() as p:
        if not args.cdp:
            raise SystemExit(
                "STOP: require --cdp http://127.0.0.1:PORT attached to "
                "benoats@googlemail.com ULTRA Flow session"
            )
        print(f"cdp attach {args.cdp}", flush=True)
        browser = p.chromium.connect_over_cdp(args.cdp)
        ctx = browser.contexts[0]
        page = None
        for pg in ctx.pages:
            if "537a3344-5ba3-46c3-b727-4e166601d9d0" in (pg.url or ""):
                page = pg
                break
        if page is None:
            page = ctx.new_page()
            page.goto(PROJECT_URL, wait_until="domcontentloaded", timeout=120_000)
            flow.settle_after_nav(page, wait_ms=2000)
        else:
            page.bring_to_front()
            flow.settle_after_nav(page, wait_ms=1000)
        flow.dismiss_banners(page)
        abort_guards(page, "goto")
        print(f"url={page.url}", flush=True)
        print(f"logged_in={flow.looks_logged_in(page)} editor={flow.editor_usable(page)}", flush=True)
        if args.probe_only:
            page.screenshot(path=str(QA_DIR / "remint_probe.png"), full_page=False)
            print("PROBE ONLY", flush=True)
            return
        for plate in plates:
            print(f"\n=== REMINT {plate} → v02 ===", flush=True)
            assert_keeps(before)
            rep = remint_plate(page, plate, prompts[plate], args.timeout)
            reports.append(rep)
            assert_keeps(before)
            # persist partial index
            write_index(reports)

    assert_keeps(before)
    write_index(reports)
    print("DONE remints", len(reports), "assemble CLOSED", flush=True)


if __name__ == "__main__":
    main()
