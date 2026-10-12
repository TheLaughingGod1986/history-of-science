#!/usr/bin/env python3
"""HOS 006 Flow Fast fair-test (2026-10-04): Vertex control vs Flow Veo 3.1 - Fast.

Mints three Part 01 plates over CDP :9222 as benoats@googlemail.com, ignoring board
quality (Quality-boarded plates are allowed — Flow model is always Veo 3.1 - Fast).
Does NOT use Vertex. Does NOT use Lite / Lower Priority.

  ~/.venvs/hos-vertex/bin/python 07_Edit-Project/_flow_fair_test_20261004.py
  ~/.venvs/hos-vertex/bin/python 07_Edit-Project/_flow_fair_test_20261004.py sheets
"""
from __future__ import annotations

import fcntl
import importlib.util
import json
import re
import subprocess
import sys
import time
from pathlib import Path

EDIT = Path(__file__).resolve().parent
PROJ = EDIT.parent
REPO = PROJ.parents[1]
sys.path.insert(0, str(REPO / "04_Audio/tools"))
import orbit_flow_veo_ui as flow  # noqa: E402
import orbit_gemini_veo as veo  # noqa: E402

_spec = importlib.util.spec_from_file_location("mint006", EDIT / "_mint_vertex_v01.py")
m = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(m)

_spec4 = importlib.util.spec_from_file_location(
    "flow004",
    REPO / "02_Video-Projects/004_Whats-Really-Inside-An-Atom/07_Edit-Project/_mint_part05_flow_cdp_v01.py",
)
f4 = importlib.util.module_from_spec(_spec4)
_spec4.loader.exec_module(f4)

CDP = "http://127.0.0.1:9222"
ACCOUNT = "benoats@googlemail.com"
MODEL = "Veo 3.1 - Fast"
MAX_SPEND = 10
LOG = EDIT / "FLOW_FAIR_TEST_20261004.json"
LOCK = EDIT / ".flow_fair_test_20261004.lock"
QA = EDIT / "_evidence"
OUT = PROJ / "04_Generated-Clips/flow_vs_vertex_fair_test_20261004"
STILLS = PROJ / "04_Generated-Clips/part01/refs/v01_vertex_stills"
VERTEX_RAW = PROJ / "04_Generated-Clips/part01/raw/v01"

# Fair-test set: still + Vertex control path (no board-quality gate).
PLATES = [
    {
        "id": "01_willow_air",
        "still": STILLS / "01_willow_air_v02.jpg",
        "vertex": VERTEX_RAW / "01_willow_air_t1.mp4",
    },
    {
        "id": "06_aristotle",
        "still": STILLS / "06_aristotle_v01.jpg",
        "vertex": VERTEX_RAW / "06_aristotle_t1.mp4",
    },
    {
        "id": "07_roots_mouths",
        "still": STILLS / "07_roots_mouths_v03.jpg",
        "vertex": VERTEX_RAW / "07_roots_mouths_t1.mp4",
    },
]


def update(fn) -> dict:
    with LOCK.open("w") as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        log = json.loads(LOG.read_text()) if LOG.exists() else {
            "film": "006_Trees-Are-Made-Of-Air",
            "task": "Flow Fast fair-test 2026-10-04 (Vertex left vs Flow Fast right)",
            "model": MODEL,
            "account": ACCOUNT,
            "max_spend_credits": MAX_SPEND,
            "takes": [],
        }
        fn(log)
        log["updated"] = m.now()
        LOG.write_text(json.dumps(log, indent=2, ensure_ascii=False) + "\n")
        return log


def credits(page, tag: str) -> dict:
    QA.mkdir(exist_ok=True)
    f4.open_account_menu(page)
    time.sleep(1.0)
    text = f4.page_text(page)
    shot = QA / f"flow_credits_fair_{tag}.png"
    page.screenshot(path=str(shot))
    try:
        page.keyboard.press("Escape")
    except Exception:
        pass
    hits = [int(x.replace(",", "")) for x in re.findall(
        r"([\d,]{1,7})\s*(?:Google\s+Flow\s+|AI\s+)?credits", text, re.I)]
    acct = ACCOUNT if ACCOUNT in text.lower() else None
    return {"hits": hits, "account_seen": acct, "screenshot": shot.name, "at": m.now()}


def prompt_for(pl: dict) -> str:
    # Flow refuses the long Vertex house wrapper; send short board scene only.
    body = pl["prompt"]
    for drop in (
        "Premium Animistry-class 3D cartoon.",
        "Daylight from out of frame; no candle, flame, lantern, lamp or fire in shot.",
        "Silent.",
        "Continuous motion through the final frame.",
        "No Explorer.",
    ):
        body = body.replace(drop, "")
    return "IMAGE-TO-VIDEO of the attached start frame. " + " ".join(body.split()) + " No people. Silent."


def probe_wh(mp4: Path) -> tuple[int, int]:
    out = subprocess.check_output(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height", "-of", "csv=p=0:s=x", str(mp4)],
        text=True,
    ).strip()
    w, h = out.split("x")
    return int(w), int(h)


def credit_delta(before: dict, after: dict) -> int | None:
    if before.get("hits") and after.get("hits"):
        return min(before["hits"]) - min(after["hits"])
    return None


def mint_one(pid: str, still: Path, vertex: Path) -> dict:
    from playwright.sync_api import sync_playwright

    m.set_part("01")
    pl = m.plate(pid)
    if not still.exists():
        raise SystemExit(f"STOP: missing still {still}")
    if not vertex.exists():
        raise SystemExit(f"STOP: missing Vertex control {vertex}")

    OUT.mkdir(parents=True, exist_ok=True)
    dest = OUT / f"{pid}_flow_fast_t1.mp4"
    if dest.exists() and dest.stat().st_size > 400_000:
        print(f"=== SKIP {pid}: already have {dest.name} ({dest.stat().st_size} B) ===", flush=True)
        log = json.loads(LOG.read_text()) if LOG.exists() else {"takes": []}
        for t in log.get("takes", []):
            if t.get("plate") == pid and t.get("take") == 1:
                return t
        # re-register from existing file
        dur = m.probe_dur(dest)
        sheet = OUT / f"{pid}_flow_fast_t1_sheet.jpg"
        if not sheet.exists():
            m.uat_sheet(dest, sheet)
        w, h = probe_wh(dest)
        entry = {
            "part": "01", "plate": pid, "take": 1, "model": MODEL, "path": "flow-cdp",
            "prompt": prompt_for(pl), "start_frame": m.rel(still),
            "start_frame_sha256": m.sha256(still),
            "vertex_control": m.rel(vertex), "vertex_sha256": m.sha256(vertex),
            "file": m.rel(dest), "sha256": m.sha256(dest), "duration_s": round(dur, 3),
            "resolution": f"{w}x{h}", "uat_sheet": m.rel(sheet),
            "motion": m.motion_stats(dest), "status": "EXISTS_REUSED", "at": m.now(),
        }
        update(lambda log: log["takes"].append(entry))
        return entry

    prompt = prompt_for(pl)
    print(f"=== FAIR Fast {pid} model={MODEL} still={m.rel(still)} board_q={pl.get('quality')} ===", flush=True)
    print(f"  prompt ({len(prompt)} chars): {prompt[:180]}…", flush=True)
    t0 = time.time()
    before = after = {"hits": [], "account_seen": None, "screenshot": None, "at": m.now()}
    proj = ""
    with sync_playwright() as p:
        br = p.chromium.connect_over_cdp(CDP)
        ctx = br.contexts[0]
        page = ctx.new_page()
        try:
            page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
            time.sleep(4)
            flow.dismiss_banners(page)
            before = credits(page, f"{pid}_t1_before")
            print(f"  credits before {before['hits']} account={before['account_seen']}", flush=True)
            info = flow.generate_clip(
                page, prompt, dest, model=MODEL, start_frame=still,
                timeout_s=900, attempts=2,
            )
            proj = (info or {}).get("project_url") or (info or {}).get("url") or ""
            if (info or {}).get("needs_gallery_harvest") or not dest.exists() or dest.stat().st_size < 400_000:
                print(f"  gallery harvest via {proj}", flush=True)
                f4.harvest_project_mp4(page, proj, dest, wait_s=600)
            if dest.exists():
                veo.strip_audio(dest)
            after = credits(page, f"{pid}_t1_after")
            print(f"  credits after {after['hits']}", flush=True)
            # reread if after hits empty (known flaky account menu)
            if not after.get("hits"):
                time.sleep(2)
                after = credits(page, f"{pid}_t1_after_reread")
                print(f"  credits after reread {after['hits']}", flush=True)
        finally:
            page.close()

    if not dest.exists() or dest.stat().st_size < 400_000:
        raise SystemExit(f"STOP: mint failed for {pid}, missing/small dest {dest}")

    dur = m.probe_dur(dest)
    sheet = OUT / f"{pid}_flow_fast_t1_sheet.jpg"
    m.uat_sheet(dest, sheet)
    w, h = probe_wh(dest)
    spent = credit_delta(before, after)
    entry = {
        "part": "01", "plate": pid, "take": 1, "model": MODEL, "path": "flow-cdp",
        "board_quality": pl.get("quality"),
        "prompt": prompt, "start_frame": m.rel(still),
        "start_frame_sha256": m.sha256(still),
        "vertex_control": m.rel(vertex), "vertex_sha256": m.sha256(vertex),
        "file": m.rel(dest), "sha256": m.sha256(dest), "duration_s": round(dur, 3),
        "resolution": f"{w}x{h}", "uat_sheet": m.rel(sheet),
        "motion": m.motion_stats(dest), "project_url": proj,
        "flow_credits_before": before, "flow_credits_after": after,
        "credit_delta": spent,
        "seconds": round(time.time() - t0, 1), "status": "PENDING_UAT", "at": m.now(),
    }
    update(lambda log: log["takes"].append(entry))
    print(json.dumps({
        k: entry[k] for k in (
            "file", "sha256", "duration_s", "resolution", "credit_delta", "uat_sheet",
        )
    }), flush=True)
    if spent is not None and spent > MAX_SPEND:
        raise SystemExit(
            f"STOP: {pid} spent {spent} credits (> {MAX_SPEND}); "
            f"{before['hits']} → {after['hits']}"
        )
    return entry


def extract_frames(mp4: Path, tmp: Path, n: int = 4) -> list[Path]:
    tmp.mkdir(parents=True, exist_ok=True)
    dur = m.probe_dur(mp4)
    # sample at ~12.5%, 37.5%, 62.5%, 87.5% of duration
    fracs = [(i + 0.5) / n for i in range(n)]
    frames: list[Path] = []
    for i, f in enumerate(fracs):
        t = max(0.05, min(dur - 0.05, dur * f))
        out = tmp / f"f{i:02d}.jpg"
        subprocess.run(
            ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
             "-ss", f"{t:.3f}", "-i", str(mp4), "-frames:v", "1",
             "-vf", "scale=640:-2", "-q:v", "3", str(out)],
            check=True,
        )
        frames.append(out)
    return frames


def side_by_side(vertex: Path, flow_mp4: Path, out: Path, n: int = 4) -> Path:
    """Vertex left column, Flow right column — n frames each stacked then hstacked."""
    import tempfile
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="fair_sbs_") as td:
        td_p = Path(td)
        vframes = extract_frames(vertex, td_p / "v", n)
        fframes = extract_frames(flow_mp4, td_p / "f", n)
        # vertical stack each side
        vstack = td_p / "vertex_col.jpg"
        fstack = td_p / "flow_col.jpg"
        v_inputs = []
        for f in vframes:
            v_inputs += ["-i", str(f)]
        f_inputs = []
        for f in fframes:
            f_inputs += ["-i", str(f)]
        vfilt = "".join(f"[{i}:v]" for i in range(n)) + f"vstack=inputs={n}[v]"
        ffilt = "".join(f"[{i}:v]" for i in range(n)) + f"vstack=inputs={n}[v]"
        subprocess.run(
            ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *v_inputs,
             "-filter_complex", vfilt, "-map", "[v]", "-q:v", "3", str(vstack)],
            check=True,
        )
        subprocess.run(
            ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *f_inputs,
             "-filter_complex", ffilt, "-map", "[v]", "-q:v", "3", str(fstack)],
            check=True,
        )
        # label bars via drawtext if available; else plain hstack
        labelled_v = td_p / "vertex_labelled.jpg"
        labelled_f = td_p / "flow_labelled.jpg"
        # pad a 36px black bar on top with text via color+overlay (no drawtext dependency risk)
        # Use simple pad + hstack; labels baked as color sources is complex — use drawtext with fallback.
        try:
            subprocess.run(
                ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                 "-i", str(vstack),
                 "-vf", "pad=iw:ih+40:0:40:black,drawtext=text='VERTEX':x=12:y=10:fontsize=28:fontcolor=white",
                 "-q:v", "3", str(labelled_v)],
                check=True, capture_output=True,
            )
            subprocess.run(
                ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                 "-i", str(fstack),
                 "-vf", "pad=iw:ih+40:0:40:black,drawtext=text='FLOW Fast':x=12:y=10:fontsize=28:fontcolor=white",
                 "-q:v", "3", str(labelled_f)],
                check=True, capture_output=True,
            )
            left, right = labelled_v, labelled_f
        except subprocess.CalledProcessError:
            left, right = vstack, fstack
        subprocess.run(
            ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
             "-i", str(left), "-i", str(right),
             "-filter_complex", "[0:v][1:v]hstack=inputs=2[v]",
             "-map", "[v]", "-q:v", "3", str(out)],
            check=True,
        )
    return out


def build_sheets() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for spec in PLATES:
        pid = spec["id"]
        flow_mp4 = OUT / f"{pid}_flow_fast_t1.mp4"
        vertex = spec["vertex"]
        if not flow_mp4.exists():
            print(f"SKIP sheet {pid}: missing Flow mp4", flush=True)
            continue
        if not vertex.exists():
            print(f"SKIP sheet {pid}: missing Vertex mp4", flush=True)
            continue
        out = OUT / f"{pid}_vertex_vs_flow_sheet.jpg"
        side_by_side(vertex, flow_mp4, out, n=4)
        sha = m.sha256(out)
        print(f"SHEET {out} sha256={sha}", flush=True)
        update(lambda log, pid=pid, out=out, sha=sha: (
            log.setdefault("sheets", []).append({
                "plate": pid,
                "file": m.rel(out),
                "sha256": sha,
                "at": m.now(),
            })
            if not any(s.get("plate") == pid and s.get("file") == m.rel(out) for s in log.get("sheets", []))
            else None
        ))


def ensure_cdp() -> None:
    import urllib.request
    try:
        with urllib.request.urlopen(CDP + "/json/version", timeout=3) as r:
            print(f"CDP ok: {json.loads(r.read())['Browser']}", flush=True)
            return
    except Exception as e:
        print(f"CDP down ({e}); restarting Chrome…", flush=True)
    subprocess.Popen([
        "open", "-na", "Google Chrome", "--args",
        "--remote-debugging-port=9222",
        "--remote-allow-origins=*",
        "--user-data-dir=/Users/benjaminoats/.hos-chrome-flow-benoats-googlemail-cdp",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-background-timer-throttling",
        "--disable-renderer-backgrounding",
        "https://flow.google.com/",
    ])
    for i in range(30):
        time.sleep(2)
        try:
            with urllib.request.urlopen(CDP + "/json/version", timeout=2) as r:
                print(f"CDP back: {json.loads(r.read())['Browser']}", flush=True)
                return
        except Exception:
            pass
    raise SystemExit("STOP: could not restart CDP Chrome on :9222")


def main() -> None:
    if sys.argv[1:] == ["sheets"]:
        build_sheets()
        return
    ensure_cdp()
    results = []
    for spec in PLATES:
        try:
            ensure_cdp()
            entry = mint_one(spec["id"], spec["still"], spec["vertex"])
            results.append(entry)
        except SystemExit as e:
            print(f"HALT: {e}", flush=True)
            # still try sheets for whatever we have
            break
        except Exception as e:
            print(f"FAIL {spec['id']}: {type(e).__name__}: {e}", flush=True)
            update(lambda log, pid=spec["id"], err=str(e): log["takes"].append({
                "part": "01", "plate": pid, "take": 1, "model": MODEL,
                "status": "FAIL", "error": err, "at": m.now(),
            }))
            break
    print("=== building side-by-side sheets ===", flush=True)
    build_sheets()
    print("=== done ===", flush=True)
    if LOG.exists():
        print(LOG.read_text(), flush=True)


if __name__ == "__main__":
    main()
