#!/usr/bin/env python3
"""HOS 003 Part 02 — mint ONLY 11_detector_hold in Batch B Flow project.

Pinned project (do not New project, do not remint KEEP plates):
  https://flow.google.com/u/1/project/95929b6f-ae75-40be-af91-05699c481557

Account: benoats@googlemail.com. Do not switch accounts.
Veo 3.1 Quality · 8s · 16:9 · scenery-only (no Explorer, no helix, no Orbit).

Unusual-activity: STOP, quote dialog, no charge-loop (no retry / resubmit).
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
    "https://flow.google.com/u/1/project/95929b6f-ae75-40be-af91-05699c481557"
)
ACCOUNT = "benoats@googlemail.com"
MODEL = "Veo 3.1 - Quality"
CLIP_DIR = (
    REPO
    / "02_Video-Projects"
    / "003_Invisible-Bones-X-Rays"
    / "04_Generated-Clips"
    / "part02"
)
DEST = CLIP_DIR / "11_detector_hold_v01.mp4"
KEEP = (
    "02_tube_covered_v01.mp4",
    "04_should_stay_dark_v01.mp4",
    "05_glow_blooms_v02.mp4",
    "06_passes_soft_things_v03.mp4",
    "07_names_it_x_v01.mp4",
    "08_locks_the_door_v01.mp4",
    "09_test_book_v01.mp4",
    "10_test_hand_metal_v01.mp4",
)
PROMPT = (
    "Animistry premium 3D cartoon. Dark 1895 Würzburg physics lab. "
    "Hold on a FLAT soft-glowing fluorescent cardboard screen "
    "(paper-thin sheet standing upright — NOT a TV, NOT a CRT monitor, "
    "NOT a glass bezel) as detector/proof; covered cathode tube nearby; "
    "ominous soft green glow holds; continuous subtle camera drift. "
    "Silent. No Explorer. No DNA helix. No Orbit. No people."
)
# Marketing Flow footer says "protected by reCAPTCHA" — that is NOT a block.
UNUSUAL_RE = re.compile(
    r"unusual activity|suspicious activity|verify it.?s you|"
    r"confirm you.?re not a robot|automated quer|"
    r"too many (requests|attempts)|try again later|unusual traffic|"
    r"couldn.?t verify|(?<!re)captcha|are you a robot",
    re.I,
)
FOREIGN_ACCOUNT_RE = re.compile(
    r"[A-Za-z0-9._%+\-]+@(?:gmail|googlemail)\.com"
)
# HOS default env profile is benoats86@gmail.com. This mint stays on
# benoats@googlemail.com — the account already in Batch B. Do not switch.
PROFILE = Path(
    os.environ.get(
        "HOS_003_FLOW_PROFILE",
        str(Path.home() / ".playwright-owb-flow-benoats-googlemail"),
    )
)
QA_DIR = Path(__file__).resolve().parent / "_qa_part02_plate11"


class UnusualActivity(RuntimeError):
    pass


def keep_fingerprints() -> dict[str, dict]:
    out: dict[str, dict] = {}
    for name in KEEP:
        p = CLIP_DIR / name
        if not p.exists():
            raise SystemExit(f"STOP: KEEP missing {p}")
        out[name] = {"size": p.stat().st_size, "mtime": p.stat().st_mtime}
    return out


def assert_keeps(before: dict[str, dict]) -> None:
    for name, meta in before.items():
        p = CLIP_DIR / name
        now = p.stat()
        if now.st_size != meta["size"] or now.st_mtime != meta["mtime"]:
            raise SystemExit(f"STOP: KEEP mutated {name}")


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


def quote_dialog(text: str) -> str:
    m = UNUSUAL_RE.search(text)
    if not m:
        return text[:800].replace("\n", " | ")
    i = max(0, m.start() - 180)
    j = min(len(text), m.end() + 420)
    return text[i:j].replace("\n", " | ")


def abort_if_unusual(page, stage: str, shot: Path) -> None:
    text = page_text(page)
    if not UNUSUAL_RE.search(text):
        return
    shot.parent.mkdir(parents=True, exist_ok=True)
    try:
        page.screenshot(path=str(shot), full_page=False)
    except Exception:
        pass
    raise UnusualActivity(
        f"UNUSUAL ACTIVITY at {stage}. STOP. No charge-loop.\n"
        f"url={page.url}\n"
        f"dialog={quote_dialog(text)!r}\n"
        f"shot={shot}"
    )


def assert_account_slot(page) -> str:
    url = page.url or ""
    if "/u/1/" not in url:
        raise SystemExit(f"STOP: not Flow /u/1/ slot ({url}). Do not switch accounts.")
    text = page_text(page, 20000)
    emails = sorted(set(FOREIGN_ACCOUNT_RE.findall(text)))
    foreign = [e for e in emails if e.lower() != ACCOUNT.lower()]
    if foreign:
        raise SystemExit(
            f"STOP: foreign Google account visible {foreign}. "
            f"Want {ACCOUNT}. Do not switch."
        )
    return url


def dump_probe(page, dest_dir: Path) -> dict:
    dest_dir.mkdir(parents=True, exist_ok=True)
    shot = dest_dir / "flow_probe_batch_b.png"
    html = dest_dir / "flow_probe_batch_b.html"
    page.screenshot(path=str(shot), full_page=False)
    html.write_text(page.content(), encoding="utf-8")
    summary = {
        "url": page.url,
        "logged_in": flow.looks_logged_in(page),
        "editor_usable": flow.editor_usable(page),
        "account_wanted": ACCOUNT,
        "project": PROJECT_URL,
        "screenshot": str(shot),
        "html": str(html),
        "body_head": page_text(page, 1500),
        "ts": datetime.now(timezone.utc).isoformat(),
    }
    (dest_dir / "flow_probe_batch_b.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    return summary


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


def wait_one_create(page, dest: Path, before_ids: set[str], timeout_s: int) -> str:
    """Wait for the single Create. Never retry / resubmit / regenerate."""
    t0 = time.time()
    last = ""
    while time.time() - t0 < timeout_s:
        abort_if_unusual(
            page, f"wait {int(time.time() - t0)}s", QA_DIR / "unusual_wait.png"
        )
        body = page_text(page, 4000).lower()
        if "generation quota for today" in body or "reached your generation quota" in body:
            raise SystemExit("STOP: Flow daily generation quota reached")
        if re.search(r"\bfailed\b", body):
            raise SystemExit(
                "STOP: Flow failed banner. No retry / no charge-loop.\n"
                f"dialog={quote_dialog(page_text(page))!r}"
            )
        hit = harvest_newest(page, dest, before_ids)
        if hit:
            return hit
        elapsed = int(time.time() - t0)
        status = "…"
        for k in ("generating", "thinking", "queue", "high demand", "creating", "working"):
            if k in body:
                status = k
                break
        pct = re.search(r"\b(\d{1,3})\s*%", body)
        if pct:
            status = f"{status} {pct.group(0)}"
        line = f"  wait {elapsed}s status={status}"
        if line != last:
            print(line, flush=True)
            last = line
        page.wait_for_timeout(4000)
    raise TimeoutError(f"Flow video not ready after {timeout_s}s (no retry)")


def extract_qa_frames(mp4: Path) -> list[Path]:
    QA_DIR.mkdir(parents=True, exist_ok=True)
    dur = probe_dur(mp4)
    stamps = {
        "start": 0.4,
        "mid": max(0.5, dur / 2.0),
        "end": max(0.5, dur - 0.6),
    }
    out: list[Path] = []
    for name, t in stamps.items():
        dest = QA_DIR / f"11_detector_hold_{name}.jpg"
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
        out.append(dest)
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--probe-only", action="store_true")
    ap.add_argument("--timeout", type=int, default=900)
    args = ap.parse_args()

    if DEST.exists():
        raise SystemExit(f"STOP: dest already exists {DEST} — will not overwrite")
    before = keep_fingerprints()
    flow.FLOW_HOME = "https://flow.google.com/u/1/"
    QA_DIR.mkdir(parents=True, exist_ok=True)

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        ctx, page = flow.launch_context(p, headed=True, profile=PROFILE)
        try:
            print(f"profile={PROFILE}", flush=True)
            print(f"account lock={ACCOUNT} (do not switch)", flush=True)
            print(f"goto {PROJECT_URL}", flush=True)
            page.goto(PROJECT_URL, wait_until="domcontentloaded", timeout=120_000)
            flow.settle_after_nav(page, wait_ms=2000)
            flow.dismiss_banners(page)
            if "95929b6f-ae75-40be-af91-05699c481557" not in (page.url or ""):
                print(f"  bounced to {page.url} — re-entering Batch B", flush=True)
                page.goto(PROJECT_URL, wait_until="domcontentloaded", timeout=120_000)
                flow.settle_after_nav(page, wait_ms=2000)
                flow.dismiss_banners(page)
            abort_if_unusual(page, "after-goto", QA_DIR / "unusual_goto.png")
            if not flow.looks_logged_in(page):
                raise SystemExit(
                    f"STOP: not logged into Google Flow as {ACCOUNT}. "
                    "Do not switch accounts."
                )
            url = assert_account_slot(page)
            if "95929b6f-ae75-40be-af91-05699c481557" not in url:
                raise SystemExit(f"STOP: left Batch B project ({url})")
            flow.ensure_agent_session(page)
            summary = dump_probe(page, QA_DIR)
            print(json.dumps({k: summary[k] for k in (
                "url", "logged_in", "editor_usable", "screenshot"
            )}, indent=2), flush=True)
            if args.probe_only:
                print("PROBE ONLY — no Create.", flush=True)
                return

            abort_if_unusual(page, "pre-settings", QA_DIR / "unusual_pre.png")
            flow.configure_veo_settings(
                page, model=MODEL, frames_mode=False, ingredients_mode=False
            )
            abort_if_unusual(page, "post-settings", QA_DIR / "unusual_settings.png")
            selected = flow.read_selected_video_model(page) or ""
            print(f"  selected model={selected!r}", flush=True)
            if selected and "Quality" not in selected:
                print("  WARN selected model missing Quality label — continuing if lock said Quality", flush=True)

            before_ids = flow.collect_media_ids(page)
            flow.ensure_agent_session(page)
            print("  setting scenery-only prompt…", flush=True)
            flow.set_prompt(page, flow.flow_prompt(PROMPT, scenery_only=True))
            abort_if_unusual(page, "pre-create", QA_DIR / "unusual_precreate.png")
            print("  submitting ONE Create…", flush=True)
            flow.submit_create(page)
            flow.settle_after_nav(page, wait_ms=1200)
            abort_if_unusual(page, "post-create", QA_DIR / "unusual_postcreate.png")
            try:
                flow.confirm_generation_spend(page, timeout_s=8.0)
            except Exception as e:
                print(f"  confirm spend: {e}", flush=True)
            abort_if_unusual(page, "post-confirm", QA_DIR / "unusual_postconfirm.png")

            media = wait_one_create(page, DEST, before_ids, args.timeout)
            print(f"  media={media}", flush=True)
        except UnusualActivity as e:
            print(str(e), flush=True)
            raise SystemExit(2)
        finally:
            try:
                ctx.close()
            except Exception:
                pass

    assert_keeps(before)
    if not DEST.exists() or DEST.stat().st_size < 150_000:
        raise SystemExit(f"STOP: dest missing/small {DEST}")
    raw = DEST.read_bytes()[:64]
    if b"ftyp" not in raw:
        raise SystemExit(f"STOP: not an mp4 {raw!r}")
    veo.strip_audio(DEST)
    dur = probe_dur(DEST)
    if dur < 6.0 or dur > 12.0:
        raise SystemExit(f"STOP: unexpected duration {dur:.2f}s")
    frames = extract_qa_frames(DEST)
    report = {
        "plate": "11_detector_hold",
        "path": str(DEST),
        "bytes": DEST.stat().st_size,
        "sha256": sha256_file(DEST),
        "duration_s": round(dur, 3),
        "model": MODEL,
        "project": PROJECT_URL,
        "account": ACCOUNT,
        "scenery_only": True,
        "frames": [str(p) for p in frames],
        "keeps_untouched": True,
        "ts": datetime.now(timezone.utc).isoformat(),
    }
    (QA_DIR / "11_detector_hold_mint.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    print(json.dumps(report, indent=2), flush=True)
    print(f"SAVED {DEST}", flush=True)


if __name__ == "__main__":
    main()
