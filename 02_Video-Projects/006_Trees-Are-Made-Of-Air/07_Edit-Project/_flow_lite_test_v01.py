#!/usr/bin/env python3
"""HOS 006 Flow "Veo 3.1 - Lite [Lower Priority]" test (Claude desk task 5951520953, 2 Oct 2026).

  ~/.venvs/hos-vertex/bin/python 07_Edit-Project/_flow_lite_test_v01.py <part> <plate> [--still <jpg>]
  ~/.venvs/hos-vertex/bin/python 07_Edit-Project/_flow_lite_test_v01.py verdict <part> <plate> <take> KEEP|FAIL "why"
  ~/.venvs/hos-vertex/bin/python 07_Edit-Project/_flow_lite_test_v01.py --fast <part> <plate>   # a boarded Flow Fast row

--fast (first argument, before any subcommand) switches to "Veo 3.1 - Fast": files end
_flowfast_tN, takes go to FLOW_FAST_v01.json, and a take that spends more than 10 credits is a STOP.

Mints one plate on Flow Lite [Lower Priority] (0 credits) from the same start frame and the same
prompt as its Vertex Fast control (`_mint_vertex_v01.py --tag lite_test_control`). Runs on the
Mini's Flow Chrome over CDP :9222 as benoats@googlemail.com. Reads the Flow credit line before
and after; a take that spends a credit is a STOP. Media stays out of git.
"""
from __future__ import annotations

import fcntl
import importlib.util
import json
import re
import sys
import time
from pathlib import Path

EDIT = Path(__file__).resolve().parent
PROJ = EDIT.parent
REPO = PROJ.parents[1]
sys.path.insert(0, str(REPO / "04_Audio/tools"))
import orbit_flow_veo_ui as flow  # noqa: E402

_spec = importlib.util.spec_from_file_location("mint006", EDIT / "_mint_vertex_v01.py")
m = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(m)

_spec4 = importlib.util.spec_from_file_location(
    "flow004", REPO / "02_Video-Projects/004_Whats-Really-Inside-An-Atom/07_Edit-Project/_mint_part05_flow_cdp_v01.py")
f4 = importlib.util.module_from_spec(_spec4)
_spec4.loader.exec_module(f4)

CDP = "http://127.0.0.1:9222"
ACCOUNT = "benoats@googlemail.com"
MODEL = "Veo 3.1 - Lite [Lower Priority]"
LOG = EDIT / "LITE_TEST_v01.json"
LOCK = EDIT / ".lite_test.lock"
SUFFIX = "lite"
MAX_SPEND = 0
if sys.argv[1:2] == ["--fast"]:
    del sys.argv[1]
    MODEL, LOG, LOCK, SUFFIX, MAX_SPEND = ("Veo 3.1 - Fast", EDIT / "FLOW_FAST_v01.json",
                                           EDIT / ".flow_fast.lock", "flowfast", 10)
QA = EDIT / "_evidence"


def update(fn) -> dict:
    with LOCK.open("w") as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        log = json.loads(LOG.read_text()) if LOG.exists() else {
            "film": "006_Trees-Are-Made-Of-Air", "task": "Claude desk PR #180 comment 5951520953",
            "model": MODEL, "account": ACCOUNT, "takes": []}
        if SUFFIX == "lite":
            log.setdefault("control", "Vertex veo-3.1-fast-generate-001, same start frame and prompt")
        fn(log)
        log["updated"] = m.now()
        LOG.write_text(json.dumps(log, indent=2, ensure_ascii=False) + "\n")
        return log


def credits(page, tag: str) -> dict:
    QA.mkdir(exist_ok=True)
    f4.open_account_menu(page)
    time.sleep(1.0)
    text = f4.page_text(page)
    shot = QA / f"flow_credits_{SUFFIX}_{tag}.png"
    page.screenshot(path=str(shot))
    try:
        page.keyboard.press("Escape")
    except Exception:
        pass
    hits = [int(x.replace(",", "")) for x in re.findall(r"([\d,]{1,7})\s*(?:Google\s+Flow\s+|AI\s+)?credits", text, re.I)]
    acct = ACCOUNT if ACCOUNT in text.lower() else None
    return {"hits": hits, "account_seen": acct, "screenshot": shot.name, "at": m.now()}


def prompt_for(pl: dict) -> str:
    # Flow silently refuses to submit long prompts (the ~1,300-character Vertex wrapper sat in the
    # box for 9 minutes; the bare scene sentence submitted at once). Send the board's scene text only.
    body = pl["prompt"]
    for drop in ("Premium Animistry-class 3D cartoon.", "Daylight from out of frame; no candle, flame, lantern, lamp or fire in shot.",
                 "Silent.", "Continuous motion through the final frame.", "No Explorer."):
        body = body.replace(drop, "")
    return "IMAGE-TO-VIDEO of the attached start frame. " + " ".join(body.split()) + " No people. Silent."


def mint(part: str, pid: str, still: str | None) -> None:
    from playwright.sync_api import sync_playwright

    m.set_part(part)
    pl = m.plate(pid)
    if pl.get("explorer") or pl["quality"] != "Fast":
        raise SystemExit(f"STOP: {pid} is not a no-face Fast plate")
    if still:
        sf = Path(still).resolve()
    else:
        mine = [s for s in m.load_log()["stills"] if s["plate"] == pid]
        if not mine:
            raise SystemExit(f"STOP: no start frame for {pid}")
        sf = REPO / mine[-1]["file"]
    m.RAW.mkdir(parents=True, exist_ok=True)
    take = 1
    while (m.RAW / f"{pid}_{SUFFIX}_t{take}.mp4").exists():
        take += 1
    dest = m.RAW / f"{pid}_{SUFFIX}_t{take}.mp4"
    prompt = prompt_for(pl)
    print(f"=== {SUFFIX.upper()} {pid} take={take} model={MODEL} still={m.rel(sf)} ===", flush=True)
    t0 = time.time()
    with sync_playwright() as p:
        br = p.chromium.connect_over_cdp(CDP)
        ctx = br.contexts[0]
        page = ctx.new_page()
        try:
            page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
            time.sleep(4)
            flow.dismiss_banners(page)
            before = credits(page, f"{pid}_t{take}_before")
            print(f"  credits before {before['hits']} account={before['account_seen']}", flush=True)
            info = flow.generate_clip(page, prompt, dest, model=MODEL, start_frame=sf,
                                      timeout_s=900, attempts=2)
            proj = (info or {}).get("project_url") or (info or {}).get("url") or ""
            if (info or {}).get("needs_gallery_harvest") or not dest.exists() or dest.stat().st_size < 400_000:
                print(f"  gallery harvest via {proj}", flush=True)
                f4.harvest_project_mp4(page, proj, dest, wait_s=600)
                f4.veo.strip_audio(dest)
            after = credits(page, f"{pid}_t{take}_after")
            print(f"  credits after {after['hits']}", flush=True)
        finally:
            page.close()
    dur = m.probe_dur(dest)
    sheet = m.UAT / f"{pid}_{SUFFIX}_t{take}_sheet.jpg"
    m.uat_sheet(dest, sheet)
    entry = {"part": m.PART, "plate": pid, "take": take, "model": MODEL, "path": "flow-cdp",
             "prompt": prompt, "start_frame": m.rel(sf), "start_frame_sha256": m.sha256(sf),
             "file": m.rel(dest), "sha256": m.sha256(dest), "duration_s": round(dur, 3),
             "uat_sheet": m.rel(sheet), "motion": m.motion_stats(dest), "project_url": proj,
             "flow_credits_before": before, "flow_credits_after": after,
             "seconds": round(time.time() - t0, 1), "status": "PENDING_UAT", "at": m.now()}
    update(lambda log: log["takes"].append(entry))
    print(json.dumps({k: entry[k] for k in ("file", "duration_s", "uat_sheet", "motion")}))
    if before["hits"] and after["hits"] and min(before["hits"]) - min(after["hits"]) > MAX_SPEND:
        raise SystemExit(f"STOP: Flow credits moved {before['hits']} → {after['hits']}")


def harvest(part: str, pid: str, project_url: str, prompt: str, still: str, downloaded: str) -> None:
    """Register a Lite take submitted by hand in a Flow project and downloaded from its tile."""
    import shutil
    from playwright.sync_api import sync_playwright

    m.set_part(part)
    sf = Path(still).resolve()
    take = 1
    while (m.RAW / f"{pid}_{SUFFIX}_t{take}.mp4").exists():
        take += 1
    dest = m.RAW / f"{pid}_{SUFFIX}_t{take}.mp4"
    t0 = time.time()
    shutil.copyfile(downloaded, dest)
    f4.veo.strip_audio(dest)
    with sync_playwright() as p:
        br = p.chromium.connect_over_cdp(CDP)
        page = br.contexts[0].new_page()
        try:
            page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
            time.sleep(4)
            after = credits(page, f"{pid}_t{take}_after")
        finally:
            page.close()
    dur = m.probe_dur(dest)
    sheet = m.UAT / f"{pid}_{SUFFIX}_t{take}_sheet.jpg"
    m.uat_sheet(dest, sheet)
    entry = {"part": m.PART, "plate": pid, "take": take, "model": MODEL, "path": "flow-cdp",
             "submitted": f"by hand in the Flow composer (settings panel showed {MODEL!r})",
             "prompt": prompt, "start_frame": m.rel(sf), "start_frame_sha256": m.sha256(sf),
             "file": m.rel(dest), "sha256": m.sha256(dest), "duration_s": round(dur, 3),
             "uat_sheet": m.rel(sheet), "motion": m.motion_stats(dest), "project_url": project_url,
             "flow_credits_after": after, "seconds": round(time.time() - t0, 1),
             "status": "PENDING_UAT", "at": m.now()}
    update(lambda log: log["takes"].append(entry))
    print(json.dumps({k: entry[k] for k in ("file", "duration_s", "uat_sheet", "motion")}))


def verdict(part: str, pid: str, take: int, status: str, why: str) -> None:
    def apply(log: dict) -> None:
        hit = [t for t in log["takes"] if t["part"] == f"{int(part):02d}" and t["plate"] == pid and t["take"] == take]
        if not hit:
            raise SystemExit("STOP: no such take")
        hit[0].update(status=status, why=why, uat_at=m.now())
    update(apply)
    print(f"{status} {pid} {SUFFIX} t{take}: {why}")


def main() -> None:
    a = sys.argv[1:]
    if a and a[0] == "verdict":
        verdict(a[1], a[2], int(a[3]), a[4], a[5])
        return
    if a and a[0] == "harvest":
        harvest(a[1], a[2], a[3], a[4], a[5], a[6])
        return
    still = None
    if "--still" in a:
        i = a.index("--still")
        still = a[i + 1]
        del a[i:i + 2]
    mint(a[0], a[1], still)


if __name__ == "__main__":
    main()
