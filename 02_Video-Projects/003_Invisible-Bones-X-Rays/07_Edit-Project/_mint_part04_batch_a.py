#!/usr/bin/env python3
"""HOS 003 Part 04 Batch A — mint all 11 plates → v01.

Ben mint-green. Assemble CLOSED. No remint of P01–P03.
Flow: benoats@googlemail.com ULTRA via Mini CDP.
Veo 3.1 Quality / CLEAN LIGHT.
HARD: no DNA helix; never open Create with \"Same DNA soft background\";
prefer \"Same Würzburg lab\".
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

ACCOUNT = "benoats@googlemail.com"
MODEL = "Veo 3.1 - Quality"
DEFAULT_PROJECT = (
    "https://flow.google.com/u/1/project/2ed989c7-688d-46cc-91f3-1ffc65526fc1"
)
CLIP_DIR = (
    REPO
    / "02_Video-Projects"
    / "003_Invisible-Bones-X-Rays"
    / "04_Generated-Clips"
    / "part04"
)
QA_DIR = (
    REPO
    / "02_Video-Projects"
    / "003_Invisible-Bones-X-Rays"
    / "07_Edit-Project"
    / "_qa_part04_batch_a"
)
PLATES_PATH = (
    REPO
    / "02_Video-Projects"
    / "003_Invisible-Bones-X-Rays"
    / "07_Edit-Project"
    / "parts"
    / "part-04_plates_v01.json"
)
INDEX_PATH = QA_DIR / "BATCH_A_LAND_INDEX.json"

# Parent KEEP fingerprints — never touch these trees.
# sha from live Mini land of 01_chapter_bones_v01 (BATCH_A_LAND_INDEX / file).
PARENT_KEEPS = {
    REPO
    / "02_Video-Projects"
    / "003_Invisible-Bones-X-Rays"
    / "04_Generated-Clips"
    / "part03"
    / "01_chapter_bones_v01.mp4": "ebb64736279d6455d062e740d154d272ead839662eca7865ef4eb0e0a61a6926",
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
BANNED_OPENER = "Same DNA soft background"


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


def assert_parents() -> None:
    for path, want in PARENT_KEEPS.items():
        if not path.exists():
            raise SystemExit(f"STOP: parent KEEP missing {path}")
        got = sha256_file(path)
        if got != want:
            raise SystemExit(
                f"STOP: parent KEEP mutated {path.name}\n want {want}\n got  {got}"
            )


def extract_qa_frames(mp4: Path, plate: str) -> None:
    QA_DIR.mkdir(parents=True, exist_ok=True)
    dur = probe_dur(mp4)
    stamps = {
        "start": 0.4,
        "mid": max(0.5, dur / 2.0),
        "end": max(0.5, dur - 0.6),
    }
    for name, t in stamps.items():
        dest = QA_DIR / f"{plate}_v01_{name}.jpg"
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
        and not re.search(
            r"unusual activity|suspicious activity|verify it.?s you", text, re.I
        )
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


def bake_prompt(raw: str) -> str:
    """Ensure CLEAN LIGHT + helix lock; never start with banned opener."""
    p = (raw or "").strip()
    if p.lower().startswith(BANNED_OPENER.lower()):
        raise SystemExit(f"STOP: banned Create opener in prompt: {BANNED_OPENER!r}")
    if BANNED_OPENER.lower() in p.lower() and "never" not in p.lower():
        # Reject accidental affirmative use of the banned phrase as an opener chain.
        pass
    extras: list[str] = []
    if "CLEAN LIGHT" not in p.upper():
        extras.append("Quality CLEAN LIGHT.")
    if "Same Würzburg lab" not in p and "Same Wuerzburg lab" not in p:
        # Do not force-prefix; prefer continuity wording inside when chaining.
        pass
    if extras:
        p = f"{p} {' '.join(extras)}"
    # Absolute never: open Create with banned phrase
    if p.lstrip().lower().startswith("same dna soft background"):
        raise SystemExit("STOP: would open Create with banned DNA soft background")
    return p


def set_prompt_manual(page, prompt: str) -> int:
    """Part-03 style: click visible contenteditable + insert_text (viewport-safe)."""
    target = page.evaluate(
        """() => {
          for (const el of document.querySelectorAll('[contenteditable=\"true\"]')) {
            const r = el.getBoundingClientRect();
            const style = getComputedStyle(el);
            if (r.width > 20 && r.height > 8 && style.visibility !== 'hidden'
                && style.display !== 'none') {
              return {x: r.x + r.width/2, y: r.y + Math.min(r.height/2, 12)};
            }
          }
          return null;
        }"""
    )
    if not target:
        raise RuntimeError("no contenteditable prompt target")
    page.mouse.click(target["x"], target["y"])
    page.wait_for_timeout(200)
    page.keyboard.press("Meta+A")
    page.keyboard.press("Backspace")
    page.keyboard.press("Control+A")
    page.keyboard.press("Backspace")
    page.wait_for_timeout(80)
    page.keyboard.insert_text(prompt)
    page.wait_for_timeout(400)
    typed = page.evaluate(
        """() => {
          for (const el of document.querySelectorAll('[contenteditable=\"true\"]')) {
            const r = el.getBoundingClientRect();
            if (r.width > 20 && r.height > 8) return (el.innerText || '').length;
          }
          return 0;
        }"""
    )
    if int(typed or 0) < min(40, max(20, len(prompt) // 10)):
        raise RuntimeError(f"prompt not armed typedLen={typed}")
    return int(typed)


def click_create(page) -> dict:
    # Close settings / overlays that hide Start generation.
    try:
        page.keyboard.press("Escape")
    except Exception:
        pass
    page.wait_for_timeout(400)
    flow.dismiss_banners(page)

    create_state = page.evaluate(
        """() => {
          const hits = [];
          for (const b of document.querySelectorAll('button')) {
            const t = (b.innerText || '').trim().replace(/\\n/g, ' ');
            const aria = b.getAttribute('aria-label') || '';
            const isArrow = /arrow_forward/i.test(t) || /arrow_forward/i.test(aria);
            const isCreate = /^Create$/i.test(t) || /Start generation/i.test(aria);
            if (!isArrow && !isCreate) continue;
            const disabled = b.disabled || b.getAttribute('aria-disabled') === 'true';
            const r = b.getBoundingClientRect();
            if (r.width < 4 || r.height < 4) continue;
            hits.push({
              disabled, t: t.slice(0,40), aria: aria.slice(0,40),
              x: r.x + r.width/2, y: r.y + r.height/2, arrow: isArrow
            });
          }
          return hits;
        }"""
    )
    send = next((h for h in create_state if h.get("arrow") and not h["disabled"]), None)
    if send is None:
        send = next((h for h in create_state if not h["disabled"]), None)
    if send is None:
        try:
            flow.submit_create(page)
            return {
                "send": {"via": "flow.submit_create"},
                "confirm": None,
                "create_state": create_state,
            }
        except Exception as e:
            page.screenshot(path=str(QA_DIR / "create_disabled.png"), full_page=False)
            raise RuntimeError(f"create-disabled {create_state} fallback={e}") from e
    page.mouse.click(send["x"], send["y"])
    page.wait_for_timeout(1200)
    confirm = page.evaluate(
        """() => {
          for (const b of document.querySelectorAll('button')) {
            const t = (b.innerText || '').trim().replace(/\\n/g, ' ');
            if (/^(Confirm|Continue|Generate|OK|Got it)$/i.test(t)
                || /confirm.*credit/i.test(t)) {
              b.click(); return t;
            }
          }
          return null;
        }"""
    )
    try:
        flow.confirm_generation_spend(page, timeout_s=6.0)
    except Exception:
        pass
    return {"send": send, "confirm": confirm, "create_state": create_state}


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
    try:
        flow.configure_veo_settings(
            page, model=MODEL, frames_mode=False, ingredients_mode=False
        )
    except Exception as e:
        print(f"  configure_veo_settings warn: {e}", flush=True)
    abort_guards(page, "post-settings")
    selected = flow.read_selected_video_model(page) or ""
    print(f"  selected model={selected!r}", flush=True)
    before_ids = flow.collect_media_ids(page)
    typed = set_prompt_manual(page, prompt)
    print(f"  prompt chars={typed}", flush=True)
    # Guard: never submit if banned opener is the start of what's in the box
    box_head = page.evaluate(
        """() => {
          for (const el of document.querySelectorAll('[contenteditable=\"true\"]')) {
            const r = el.getBoundingClientRect();
            if (r.width > 20 && r.height > 8)
              return (el.innerText || '').trim().slice(0, 40);
          }
          return '';
        }"""
    )
    if str(box_head).lower().startswith("same dna soft background"):
        raise SystemExit("STOP: editor starts with banned DNA soft background")
    abort_guards(page, "pre-create")
    print("  submitting ONE Create…", flush=True)
    click_create(page)
    flow.settle_after_nav(page, wait_ms=1200)
    abort_guards(page, "post-create")
    try:
        flow.confirm_generation_spend(page, timeout_s=8.0)
    except Exception as e:
        print(f"  confirm spend: {e}", flush=True)
    page.wait_for_timeout(2500)
    if unpaid_visible(page):
        raise RuntimeError("UNPAID_FAIL")
    media = wait_create(page, dest, before_ids, timeout_s)
    return {"media": media, "selected_model": selected}


def mint_plate(
    page, plate: str, prompt: str, mute_note: str, project_url: str, timeout_s: int
) -> dict:
    dest = CLIP_DIR / f"{plate}_v01.mp4"
    if dest.exists():
        print(f"  SKIP existing {dest}", flush=True)
        return {
            "plate": plate,
            "version": "v01",
            "path": str(dest),
            "bytes": dest.stat().st_size,
            "sha256": sha256_file(dest),
            "duration_s": probe_dur(dest),
            "model": MODEL,
            "mute_note": mute_note,
            "project": project_url,
            "account": ACCOUNT,
            "skipped_existing": True,
            "assemble": "CLOSED",
            "ts": datetime.now(timezone.utc).isoformat(),
        }
    unpaid_retry = False
    baked = bake_prompt(prompt)
    try:
        meta = one_create(page, baked, dest, timeout_s)
    except RuntimeError as e:
        if str(e) != "UNPAID_FAIL":
            raise
        unpaid_retry = True
        print("  UNPAID/payment fail — ONE refresh retry only…", flush=True)
        page.reload(wait_until="domcontentloaded", timeout=120_000)
        flow.settle_after_nav(page, wait_ms=2000)
        flow.dismiss_banners(page)
        abort_guards(page, "post-refresh")
        if "2ed989c7-688d-46cc-91f3-1ffc65526fc1" not in (page.url or ""):
            page.goto(project_url, wait_until="domcontentloaded", timeout=120_000)
            flow.settle_after_nav(page, wait_ms=2000)
        try:
            meta = one_create(page, baked, dest, timeout_s)
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
        "version": "v01",
        "path": str(dest),
        "bytes": dest.stat().st_size,
        "sha256": sha256_file(dest),
        "duration_s": dur,
        "model": MODEL,
        "selected_model": meta.get("selected_model"),
        "unpaid_refresh_retry": unpaid_retry,
        "mute_note": mute_note,
        "project": project_url,
        "account": ACCOUNT,
        "assemble": "CLOSED",
        "ts": datetime.now(timezone.utc).isoformat(),
    }
    (QA_DIR / f"{plate}_v01_mint.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    print(json.dumps(report, indent=2), flush=True)
    return report


def write_index(reports: list[dict], project_url: str) -> None:
    idx = {
        "film": "003_Invisible-Bones-X-Rays",
        "part": 4,
        "batch": "A",
        "title": "Bertha's Ring",
        "account": ACCOUNT,
        "model": MODEL,
        "quality": "Veo 3.1 Quality / CLEAN LIGHT",
        "project": project_url,
        "assemble": "CLOSED until all Batch A lands + plate-first UAT PASS",
        "parents": "P01+P02+P03 KEEP/LOCK — untouched",
        "explorer": "NONE",
        "helix_lock": "HOS_HOUSE_NO_DNA_HELIX_LOCK.md",
        "plates_landed": len(reports),
        "plates": [
            {
                "plate": r["plate"],
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


def load_board() -> tuple[list[str], dict[str, dict]]:
    data = json.loads(PLATES_PATH.read_text(encoding="utf-8"))
    if not data.get("mint"):
        raise SystemExit("STOP: part-04_plates_v01.json mint is not true")
    by_id = {p["id"]: p for p in data["plates"]}
    order = data.get("batch_a_order") or [p["id"] for p in data["plates"]]
    return order, by_id


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--cdp", default=os.environ.get("HOS_003_FLOW_CDP", "http://127.0.0.1:9222"))
    ap.add_argument("--project", default=os.environ.get("HOS_003_P04_FLOW_PROJECT", DEFAULT_PROJECT))
    ap.add_argument("--timeout", type=int, default=900)
    ap.add_argument("--only", nargs="*", default=None)
    ap.add_argument("--probe-only", action="store_true")
    args = ap.parse_args()

    order, by_id = load_board()
    plates = args.only or order
    for p in plates:
        if p not in by_id:
            raise SystemExit(f"STOP: unknown plate {p}")

    assert_parents()
    QA_DIR.mkdir(parents=True, exist_ok=True)
    CLIP_DIR.mkdir(parents=True, exist_ok=True)

    # Resume partial index if present
    reports: list[dict] = []
    done_ids: set[str] = set()
    if INDEX_PATH.exists():
        prev = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
        for row in prev.get("plates", []):
            pid = row.get("plate")
            path = Path(row.get("path", ""))
            if pid and path.exists() and path.stat().st_size > 150_000:
                reports.append(
                    {
                        "plate": pid,
                        "version": "v01",
                        "path": str(path),
                        "bytes": path.stat().st_size,
                        "sha256": row.get("sha256") or sha256_file(path),
                        "duration_s": row.get("duration_s") or probe_dur(path),
                        "mute_note": row.get("mute_note") or by_id[pid].get("mute_test", ""),
                        "unpaid_refresh_retry": row.get("unpaid_refresh_retry", False),
                        "project": args.project,
                        "account": ACCOUNT,
                        "assemble": "CLOSED",
                        "resumed": True,
                    }
                )
                done_ids.add(pid)

    from playwright.sync_api import sync_playwright

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
            if "2ed989c7-688d-46cc-91f3-1ffc65526fc1" in (pg.url or ""):
                page = pg
                break
        if page is None:
            for pg in ctx.pages:
                if "flow.google.com" in (pg.url or ""):
                    page = pg
                    break
        if page is None:
            page = ctx.new_page()
        page.bring_to_front()
        if "2ed989c7-688d-46cc-91f3-1ffc65526fc1" not in (page.url or ""):
            page.goto(args.project, wait_until="domcontentloaded", timeout=120_000)
            flow.settle_after_nav(page, wait_ms=2000)
        else:
            flow.settle_after_nav(page, wait_ms=1000)
        flow.dismiss_banners(page)
        abort_guards(page, "goto")
        # Rename project once
        try:
            tb = page.get_by_role("textbox", name="Editable text")
            if tb.count():
                tb.first.click(timeout=3000)
                page.keyboard.press("Meta+A")
                page.keyboard.type("HOS 003 Part 04 Batch A", delay=8)
                page.keyboard.press("Enter")
                page.wait_for_timeout(600)
        except Exception as e:
            print(f"  rename warn: {e}", flush=True)
        print(f"url={page.url}", flush=True)
        print(
            f"logged_in={flow.looks_logged_in(page)} editor={flow.editor_usable(page)}",
            flush=True,
        )
        if args.probe_only:
            page.screenshot(path=str(QA_DIR / "mint_probe.png"), full_page=False)
            print("PROBE ONLY", flush=True)
            return

        for plate in plates:
            if plate in done_ids and (CLIP_DIR / f"{plate}_v01.mp4").exists():
                print(f"\n=== SKIP {plate} (already in index) ===", flush=True)
                continue
            print(f"\n=== MINT {plate} → v01 ===", flush=True)
            assert_parents()
            spec = by_id[plate]
            rep = mint_plate(
                page,
                plate,
                spec["prompt"],
                spec.get("mute_test") or "",
                args.project,
                args.timeout,
            )
            # replace if resumed placeholder
            reports = [r for r in reports if r["plate"] != plate]
            reports.append(rep)
            done_ids.add(plate)
            assert_parents()
            write_index(reports, args.project)

    assert_parents()
    # order reports by board order
    order_map = {pid: i for i, pid in enumerate(order)}
    reports.sort(key=lambda r: order_map.get(r["plate"], 999))
    write_index(reports, args.project)
    print("DONE mints", len(reports), "assemble CLOSED", flush=True)
    if len(reports) < len(order) and not args.only:
        missing = [p for p in order if p not in {r["plate"] for r in reports}]
        raise SystemExit(f"STOP: incomplete Batch A missing {missing}")


if __name__ == "__main__":
    main()
