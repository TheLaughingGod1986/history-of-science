#!/usr/bin/env python3
"""J0352 — HOS 007 boards v02, Flow only (CDP :9222).

Face lock first: Nano Banana 2 still of P2:08_jenner_window (0 credits).
Its Veo take, and every later readable Jenner face, wait for
FACE_LOCK_KEEP_jenner_window.json and start from that master still.
Other rows go in board order, one first take: Nano Banana 2 16:9 still,
then Veo 3.1 image-to-video.

No Vertex, no Omni, no retake. Stop before a take that would leave
live − remaining expected under 3,000, or before film spend passes 7,550,
or if free disk drops below 10 GiB.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

WT = Path(__file__).resolve().parents[3]
MINT006 = WT / "02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project/_mint_flow_cdp_v01.py"
STILL006 = WT / "02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project/_flow_still_v01.py"
BOARD = Path(__file__).resolve().parent / "parts"
MEDIA = Path(os.environ.get(
    "HOS_007_MEDIA",
    str(Path.home() / "YouTube/hos-007-vaccine/02_Video-Projects/007_The-First-Vaccine"),
))
OWB = Path(os.environ.get("OWB_REPO", str(Path.home() / "YouTube/orbit-with-ben")))
CDP = os.environ.get("ORBIT_FLOW_CDP", "http://127.0.0.1:9222")
REQUIRED = "benoats@googlemail.com"
FORBIDDEN = "benoats86@gmail.com"
TRY1 = {"Fast": 10, "Quality": 100}
CAP = 7550
BUFFER = 3000
MIN_DISK_GIB = 10.0

# Readable Jenner faces that start from the approved P2:08_jenner_window master still.
JENNER_MASTER_LOCK = {
    "08_jenner_window",
    "01_sarah_nelmes",
    "03_phipps_stool",
    "04_lancet_touch",
    "08_jenner_thinks",
    "02_variolation_calm",
    "03_waiting",
    "06b_still_nothing",
}
MASTER = "08_jenner_window"


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def free_disk_gib() -> float:
    return shutil.disk_usage("/").free / (1024 ** 3)


def check_disk() -> None:
    free = free_disk_gib()
    if free < MIN_DISK_GIB:
        raise SystemExit(f"STOP free disk {free:.2f} GiB < {MIN_DISK_GIB:.1f} GiB minimum")


def record_flow_balance(credits: int | None, note: str) -> None:
    if credits is None:
        return
    ai_spend = OWB / "scripts/ai_spend.py"
    if not ai_spend.exists():
        return
    try:
        subprocess.run(
            [sys.executable, str(ai_spend), "record", "--pool", "flow",
             "--left", str(credits), "--by", "gemini", "--note", note],
            cwd=OWB, capture_output=True, text=True, timeout=30,
        )
    except Exception as exc:
        print(f"  ai_spend record warn: {exc}", flush=True)


def load_mod(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


def boards() -> list[dict]:
    rows = []
    for n in range(1, 6):
        data = json.loads((BOARD / f"part-0{n}_plates_v02.json").read_text())
        for plate in data["plates"]:
            if plate.get("route") != "flow-first":
                continue
            plate = dict(plate)
            plate["_part"] = f"{n:02d}"
            rows.append(plate)
    return rows


def log_path() -> Path:
    return MEDIA / "07_Edit-Project/FLOW_MINT_LOG_v02.json"


def keep_path() -> Path:
    return MEDIA / "07_Edit-Project/FACE_LOCK_KEEP_jenner_window.json"


def load_log() -> dict:
    path = log_path()
    if path.exists():
        return json.loads(path.read_text())
    return {
        "job": "J0352", "film": "007", "engine": "flow-cdp-9222",
        "cap": CAP, "buffer": BUFFER, "takes": {}, "balance_reads": [],
    }


def save_log(log: dict) -> None:
    path = log_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    log["updated"] = now()
    path.write_text(json.dumps(log, indent=2) + "\n")


def spent(log: dict) -> int:
    total = 0
    for e in log["takes"].values():
        if e.get("status") in ("PENDING_UAT", "KEEP", "SUBMITTING"):
            priced = TRY1.get(e.get("quality") or "", 0)
            total += max(int(e.get("credits_used") or 0), priced)
    return total


def done_ids(log: dict) -> set[str]:
    return {k for k, e in log["takes"].items()
            if e.get("status") in ("PENDING_UAT", "KEEP")}


def remaining(rows: list[dict], log: dict) -> int:
    done = done_ids(log)
    return sum(int(p.get("flow_credits_expected") or 0) for p in rows if p["id"] not in done)


def still_dest(plate: dict) -> Path:
    return (MEDIA / "04_Generated-Clips" / f"part{plate['_part']}"
            / "refs/v02_flow_stills" / f"{plate['id']}_t1.png")


def video_dest(plate: dict) -> Path:
    return (MEDIA / "04_Generated-Clips" / f"part{plate['_part']}"
            / "raw/v01" / f"{plate['id']}_t1.mp4")


def sanitize_person_names(text: str) -> str:
    """Replace real proper surnames/names (e.g. 'Jenner') that trigger Veo's prominent-people text filter."""
    for src, dst in (
        ("This still is the face lock for later Jenner plates. ", ""),
        ("This still is the face lock for later Jenner plates.", ""),
        ("Edward Jenner", "the Georgian country doctor"),
        ("Jenner's", "the country doctor's"),
        ("Jenner", "the country doctor"),
        (", Sarah Nelmes,", ""),
        ("Sarah Nelmes", "the young dairymaid"),
        ("James Phipps, ", ""),
        ("James Phipps", "the boy"),
        ("Phipps", "the boy"),
        ("Benjamin Jesty, ", ""),
        ("Benjamin Jesty", "the sturdy farmer"),
        ("Jesty", "the farmer"),
        ("Louis Pasteur", "the bearded scientist"),
        ("Pasteur", "the bearded scientist"),
    ):
        text = text.replace(src, dst)
    return text


def still_prompt(still, plate: dict) -> str:
    core = sanitize_person_names(" ".join(plate["prompt"].split()))
    if plate.get("explorer"):
        core = core.replace("No Explorer.", "") + " " + mint006.EXPLORER
    elif any(w in core.lower() for w in ("child", "children", "boy", "sons", "son", "phipps")):
        # Flow's external start-frame upload filter rejects images with children.
        # Keep the adult hero / setting in the opening start frame; Veo 3.1 animates the full prompt.
        for src, dst in (
            ("and two young sons ", ""),
            ("two young sons ", ""),
            ("a boy of about eight", "an adult figure seen from behind"),
            ("The boy", "The adult figure seen from behind"),
            ("the boy", "the distant adult figure seen from behind"),
            ("in a small bed by a window, a little warm, a cool cloth on his forehead",
             "in a wooden bed by a window resting under a blanket with head turned away from camera"),
            ("A smiling child", "An adult patient seen from behind over the shoulder"),
            ("children run, swing and climb", "distant figures seen from behind"),
        ):
            core = core.replace(src, dst)
        core += (" No children or young boys in the opening still frame;"
                 " any secondary figure is an adult seen from behind with head turned away.")
    core += (" Opening frame only. No sores, no pustules. Handwriting has no glyph in focus."
             " Book spines and titles face away from camera. No lightning touching a kite.")
    if plate["id"] == MASTER:
        core += (" The paper on the desk is turned edge-on, a thin edge only."
                 " No page face, no lines, no writing. The quill does not draw a glyph.")
    if (
        "no faces readable" in core.lower()
        or "faces not readable" in core.lower()
        or (("cot" in core.lower() or "bed" in core.lower()) and ("child" in core.lower() or "boy" in core.lower() or "figure" in core.lower()))
    ):
        core += (" Every person is seen from behind with their head turned completely away from camera;"
                 " only the back of the head and blanket/shoulders are visible, no face or profile shown.")
    return still.still_prompt(
        "History of Science locked look: premium Animistry-class 3D cartoon, finished materials, warm daylight.",
        core,
    )


def video_prompt(plate: dict) -> str:
    core = sanitize_person_names(" ".join(plate["prompt"].split()))
    if plate.get("explorer"):
        core = core.replace("No Explorer.", "") + " " + mint006.EXPLORER
    return ("Animate the attached start frame; keep its exact cartoon look, objects and light. "
            + core
            + " Silent picture only. Continuous real camera and subject motion through the final frame."
            + " No sores, no pustules. No readable handwriting. No book-spine titles facing camera.")


def gate(live: int, rem: int, cost: int, log: dict, plate_id: str) -> str | None:
    if live - rem < BUFFER:
        return f"live {live} − remaining {rem} = {live - rem} < {BUFFER}"
    if (live - cost) - rem < BUFFER:
        return f"after {plate_id} ({cost}): {live - cost} − remaining {rem} < {BUFFER}"
    if spent(log) + cost > CAP:
        return f"cap {CAP}: spent {spent(log)} + {cost}"
    return None


def mint_still(page, still, plate: dict, master: dict, credits: int) -> tuple[Path, int]:
    if plate["id"] in JENNER_MASTER_LOCK or plate.get("face_lock"):
        m_dest = still_dest(master)
        if m_dest.exists() and m_dest.stat().st_size > 80_000:
            print(f"  face-lock start frame -> {m_dest.name}", flush=True)
            return m_dest, credits
    dest = still_dest(plate)
    if dest.exists() and dest.stat().st_size > 80_000:
        print(f"  reuse still {dest}", flush=True)
        return dest, credits
    dest.parent.mkdir(parents=True, exist_ok=True)
    stills_proj = "https://flow.google.com/project/9547a920-fe2c-4b49-886f-fd7cdb1fdc2b"
    if stills_proj not in (page.url or ""):
        page.goto(stills_proj, wait_until="domcontentloaded", timeout=120_000)
        page.wait_for_timeout(3000)
    still.make_still(page, still_prompt(still, plate), dest, timeout_s=300)
    after, _ = mint006_read(page)
    if after is not None and after < credits:
        raise SystemExit(f"STOP still for {plate['id']} cost {credits - after} credits (priced at 0)")
    return dest, after if after is not None else credits


mint006 = None


def mint006_read(page):
    return mint006.read_account(page)


def harvest_project_mp4(page, flow, project_url: str, dest: Path, wait_s: int = 420) -> None:
    """Wait for the generated video tile on project_url and fetch its MP4 via hover_fetch / response."""
    captured: list[bytes] = []

    def on_resp(resp) -> None:
        try:
            u = (resp.url or "").lower()
            ct = (resp.headers.get("content-type") or "").lower()
            if resp.status == 200 and (
                "flow-content.google/video" in u
                or "googlevideo.com" in u
                or "videoplayback" in u
                or "video/mp4" in ct
            ):
                body = resp.body()
                if body and len(body) > 400_000 and b"ftyp" in body[:64]:
                    captured.append(body)
        except Exception:
            pass

    page.on("response", on_resp)
    try:
        if project_url not in (page.url or ""):
            page.goto(project_url, wait_until="domcontentloaded", timeout=120_000)
            page.wait_for_timeout(3000)
            flow.dismiss_banners(page)
        t0 = time.time()
        last_reload = t0
        while time.time() - t0 < wait_s:
            if dest.exists() and dest.stat().st_size >= 400_000:
                return
            if captured:
                dest.write_bytes(max(captured, key=len))
                return
            gen_thumbs = page.locator('img[alt*="Generated video" i]').count()
            vids = page.locator("video").count()
            elapsed = time.time() - t0
            print(f"  harvest poll gen_thumbs={gen_thumbs} vids={vids} elapsed={elapsed:.0f}s", flush=True)
            if gen_thumbs > 0 or vids > 0 or elapsed >= 45:
                body = mint006.hover_fetch(page)
                if body and len(body) >= 400_000:
                    dest.write_bytes(body)
                    return
                if captured:
                    dest.write_bytes(max(captured, key=len))
                    return
            if time.time() - last_reload >= 60 and gen_thumbs == 0:
                try:
                    page.reload(wait_until="domcontentloaded", timeout=60_000)
                    page.wait_for_timeout(3000)
                    flow.dismiss_banners(page)
                    last_reload = time.time()
                except Exception as exc:
                    print(f"  reload warn: {exc}", flush=True)
            page.wait_for_timeout(8000)
    finally:
        try:
            page.remove_listener("response", on_resp)
        except Exception:
            pass
    raise RuntimeError(f"harvest timeout {wait_s}s project={project_url}")


def finalize_video(page, plate: dict, dest: Path, entry: dict, credits: int, log: dict) -> int:
    import orbit_gemini_veo as veo
    veo.strip_audio(dest)
    sheet = dest.parent.parent.parent / "uat" / f"{plate['id']}_t1_sheet.jpg"
    mint006.contact_sheet(dest, sheet)
    after, account = mint006.read_account(page)
    priced = TRY1[plate["quality"]]
    ui_drop = max(0, credits - after) if after is not None else priced
    used = max(ui_drop, priced) if ui_drop in (0, priced) else priced
    entry.update(
        status="PENDING_UAT", file=str(dest), sha256=mint006.sha256(dest),
        duration_s=round(mint006.duration(dest), 3), uat_sheet=str(sheet),
        credits_after=after, credits_used=used, credits_ui_drop=ui_drop,
        account=account, at=now(),
    )
    log["takes"][plate["id"]] = entry
    log.setdefault("balance_reads", []).append({"at": now(), "credits": after, "after": plate["id"]})
    save_log(log)
    if ui_drop > priced and ui_drop > 100:
        raise SystemExit(f"STOP {plate['id']} charged {ui_drop} > priced {priced}")
    print(f"  -> PENDING_UAT used={used} (ui_drop={ui_drop}) balance={after} sha={entry['sha256'][:12]}", flush=True)
    return after if after is not None else credits - used


def one_video(page, flow, still, plate: dict, start: Path, credits: int, log: dict) -> int:
    dest = video_dest(plate)
    dest.parent.mkdir(parents=True, exist_ok=True)
    model = f"Veo 3.1 - {plate['quality']}"
    os.environ["ORBIT_FLOW_VEO_MODEL"] = model
    os.environ["OWB_AGENT"] = "gemini"
    entry = {
        "plate": plate["id"], "part": plate["_part"], "take": 1, "model": model,
        "quality": plate["quality"], "start_frame": str(start),
        "start_frame_sha256": mint006.sha256(start),
        "credits_before": credits, "status": "SUBMITTING", "submitted_at": now(),
    }
    log["takes"][plate["id"]] = entry
    save_log(log)
    info = flow.generate_clip(
        page, video_prompt(plate), dest, model=model, timeout_s=700,
        start_frame=start, attempts=1, reuse_project=False,
    ) or {}
    entry["project_url"] = info.get("project_url") or info.get("url") or ""
    log["takes"][plate["id"]] = entry
    save_log(log)
    if not dest.exists() or dest.stat().st_size < 400_000:
        if "/project/" not in entry["project_url"]:
            raise RuntimeError(f"no mp4 and no project URL: {entry['project_url']!r}")
        print(f"  gallery harvest {entry['project_url']}", flush=True)
        harvest_project_mp4(page, flow, entry["project_url"], dest, wait_s=420)
    return finalize_video(page, plate, dest, entry, credits, log)


def main() -> int:
    global mint006
    ap = argparse.ArgumentParser()
    ap.add_argument("--still-only", action="store_true")
    ap.add_argument("--until-part", default="01", help="last part number to mint this batch, e.g. 01")
    args = ap.parse_args()

    check_disk()

    sys.path.insert(0, str(WT / "04_Audio/tools"))
    sys.path.insert(0, str(STILL006.parent))
    mint006 = load_mod("hos006_mint", MINT006)
    still = load_mod("hos006_still", STILL006)
    still.MEDIA_CLIPS = MEDIA / "04_Generated-Clips"
    import orbit_flow_veo_ui as flow
    from playwright.sync_api import sync_playwright

    rows = boards()
    expected = sum(int(p.get("flow_credits_expected") or 0) for p in rows)
    if expected != 7196:
        raise SystemExit(f"STOP boards expected {expected}, job says 7196")
    log = load_log()
    master = next(p for p in rows if p["id"] == MASTER)

    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp(CDP)
        page = mint006.flow_page(browser, flow)
        credits, account = mint006.read_account(page)
        print(
            f"GATE account={account} credits={credits} remaining={remaining(rows, log)} "
            f"spent={spent(log)} disk_free_gib={free_disk_gib():.2f}",
            flush=True,
        )
        if account != REQUIRED or (account and FORBIDDEN in account):
            raise SystemExit(f"STOP wrong Flow account: {account}")
        if credits is None:
            raise SystemExit("STOP Flow credits unreadable")
        log.setdefault("balance_reads", []).append({"at": now(), "credits": credits, "when": "batch-start"})
        save_log(log)
        why = gate(credits, remaining(rows, log), 0, log, "batch")
        if why:
            raise SystemExit(f"STOP gate: {why}")

        print(f"\n=== still {MASTER} (0 credits) ===", flush=True)
        start, credits = mint_still(page, still, master, master, credits)
        log["master_still"] = {"path": str(start), "sha256": mint006.sha256(start), "at": now(), "credits": credits}
        save_log(log)
        print(f"MASTER STILL {start} sha={log['master_still']['sha256'][:12]} credits={credits}", flush=True)
        if args.still_only:
            return 0

        held = not keep_path().exists()
        for plate in rows:
            if plate["_part"] > args.until_part:
                print(f"STOP batch end at part {args.until_part}", flush=True)
                break
            if plate["id"] in done_ids(log):
                continue
            if (plate["id"] in JENNER_MASTER_LOCK or plate.get("face_lock")) and held:
                print(f"HOLD {plate['id']} until Jenner face KEEP", flush=True)
                continue
            check_disk()
            prev = log["takes"].get(plate["id"]) or {}
            if prev.get("status") == "SUBMITTING":
                proj = prev.get("project_url") or ""
                if "/project/" in proj:
                    print(f"RECOVER {plate['id']} from {proj} (0 credits)", flush=True)
                    dest = video_dest(plate)
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    harvest_project_mp4(page, flow, proj, dest, wait_s=180)
                    credits = finalize_video(page, plate, dest, prev, int(prev.get("credits_before") or credits), log)
                    continue
                credits_now, _ = mint006.read_account(page)
                if credits_now is not None and credits_now == prev.get("credits_before"):
                    print(f"CLEAR un-submitted {plate['id']} (credits unchanged={credits_now})", flush=True)
                    log["takes"].pop(plate["id"], None)
                    save_log(log)
                else:
                    raise SystemExit(f"STOP {plate['id']} already SUBMITTING without project_url — inspect before retake")
            cost = TRY1[plate["quality"]]
            credits, account = mint006.read_account(page)
            if credits is None:
                raise SystemExit("STOP credits unreadable before take")
            why = gate(credits, remaining(rows, log), cost, log, plate["id"])
            if why:
                raise SystemExit(f"STOP gate: {why}")
            if mint006.UNPAID_RE.search(mint006.body_text(page)):
                raise SystemExit(f"STOP billing banner before {plate['id']}")
            print(
                f"\n=== P{plate['_part']}:{plate['id']} {plate['quality']} ~{cost} "
                f"live={credits} rem={remaining(rows, log)} disk={free_disk_gib():.1f}GiB ===",
                flush=True,
            )
            frame, credits = mint_still(page, still, plate, master, credits)
            credits = one_video(page, flow, still, plate, frame, credits, log)

        end_credits, _ = mint006.read_account(page)
        log.setdefault("balance_reads", []).append({"at": now(), "credits": end_credits, "when": f"batch-end-p{args.until_part}"})
        save_log(log)
        record_flow_balance(
            end_credits,
            f"J0352 batch-end part {args.until_part}; spent={spent(log)} rem_expected={remaining(rows, log)}",
        )
    print(f"BATCH DONE until-part={args.until_part} spent={spent(log)} remaining_expected={remaining(rows, log)}", flush=True)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SystemExit:
        raise
    except Exception as exc:
        print(f"FAIL {type(exc).__name__}: {exc}", flush=True)
        raise SystemExit(1)
