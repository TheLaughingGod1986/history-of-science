#!/usr/bin/env python3
"""HOS 006 Parts 04-05: Flow Veo 3.1 first takes via the Mini's CDP Chrome (:9222).

J0140, after the Chief's price pass J0139 (desk #180 comment 6133713891):
28 plates (P4:05-16, P5:01-23 minus reuse rows), ONE first take each, Flow only.
No Gemini API, no Vertex, no retakes. Floor 0: stop before a take the live
balance can't pay; never buy, top up or touch billing.

Text-to-video (the HOS 004 Part 05 path) came out near-photoreal on the P4:10
probe, so the Chief chose option 1 (desk #180 6134444292): with --stills each
plate first gets a Flow Image / Nano Banana 2 16:9 start still (0 credits,
_flow_still_v01.py), then Veo 3.1 image-to-video from it. Never Vertex. Media goes to the 006 media checkout
(HOS_006_MEDIA, default ~/YouTube/hos-006-trees/...), next to Parts 03-04.
Each Create writes one ai_spend flow line (orbit_flow_veo_ui._record_flow_spend).

    python3 _mint_flow_cdp_v01.py --list
    python3 _mint_flow_cdp_v01.py --part 04 --stills [--only 10_only_green] [--take 2] [--max N]
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

FILM = "006_Trees-Are-Made-Of-Air"
BOARD_DIR = Path(__file__).resolve().parent / "parts"
MEDIA = Path(
    os.environ.get(
        "HOS_006_MEDIA",
        str(Path.home() / "YouTube/hos-006-trees/02_Video-Projects" / FILM),
    )
)
CDP = os.environ.get("ORBIT_FLOW_CDP", "http://127.0.0.1:9222")
REQUIRED = "benoats@googlemail.com"
FORBIDDEN = "benoats86@gmail.com"
COST = {"Fast": 10, "Quality": 100}
FLOOR = 0

# J0139 PASS scope, board order.
PASSED = {
    "04": [
        "05_bubbles_macro", "06_collect_blaze", "08_explorer_shade", "10_only_green",
        "11_night_jars", "12_shutters_open", "13_sun_canopy", "14_leaf_glow",
        "15_leaf_turns_sun", "16_pores_question",
    ],
    "05": [
        "01_geneva_lake", "02_senebier_jars", "03_de_saussure", "04_fine_scales",
        "05_sums_add_up", "06_leaf_in", "07_sugar_oxygen", "08_sugar_wood",
        "11_trunk_pie", "14_built_from_sky", "15_food_glow", "16_cow_grass",
        "17_wind_air", "18_forest_sea", "19_dots_crowd", "20_explorer_willow",
        "22_pulled_down", "23_carbon_atom",
    ],
}

LOOK = (
    "History of Science locked look: premium Animistry-class 3D cartoon, finished "
    "materials, warm sunlit cinematic light, natural-history world of the 1600s-1800s. "
    "Not photoreal, not flat 2D. No logos, no captions, no signs, no UI. No Orbit "
    "orange robot. No DNA helix. Animals are always alive, lively and unhurt."
)
EXPLORER = (
    "Exactly ONE Explorer: young boy, messy brown hair, round thin gold glasses, "
    "teal long coat, tan vest, brown bow tie, satchel. Acts then leaves."
)
CREDIT_RE = re.compile(r"([\d,]{1,7})\s*(?:Google\s+Flow\s+)?credits", re.I)
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@(?:gmail|googlemail)\.com", re.I)
UNPAID_RE = re.compile(
    r"unpaid|payment (failed|error)|add a payment|update (your )?payment|"
    r"purchase failed|insufficient credits|not enough credits|"
    r"out of google flow credits|reached your credit",
    re.I,
)


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def duration(path: Path) -> float:
    out = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(path)], text=True)
    return float(out.strip())


def board(part: str) -> dict:
    return json.loads((BOARD_DIR / f"part-{part}_plates_v01.json").read_text())


def plates(part: str) -> list[dict]:
    by_id = {p["id"]: p for p in board(part)["plates"]}
    return [by_id[pid] for pid in PASSED[part]]


def paths(part: str) -> tuple[Path, Path, Path]:
    root = MEDIA / "04_Generated-Clips" / f"part{part}"
    return root / "raw/v01", root / "uat", MEDIA / "07_Edit-Project" / f"PART{part}_FLOW_MINT_LOG_v01.json"


def load_log(part: str) -> dict:
    _, _, log = paths(part)
    if log.exists():
        return json.loads(log.read_text())
    return {"film": FILM, "part": part, "job": "J0140", "pass": "J0139 desk #180 6133713891",
            "engine": "Flow Veo 3.1 text-to-video via CDP :9222", "takes": {}}


def save_log(part: str, data: dict) -> None:
    _, _, log = paths(part)
    data["updated"] = now()
    log.parent.mkdir(parents=True, exist_ok=True)
    log.write_text(json.dumps(data, indent=2) + "\n")


def body_text(page) -> str:
    try:
        return page.locator("body").inner_text(timeout=8000)[:16000]
    except Exception:
        return ""


def read_account(page) -> tuple[int | None, str | None]:
    def scan() -> tuple[int | None, set[str]]:
        text = body_text(page)
        try:
            text += "\n" + (page.evaluate(
                "() => [...document.querySelectorAll('[aria-label]')]"
                ".map(e => e.getAttribute('aria-label') || '').join('\\n')") or "")
        except Exception:
            pass
        hits = [int(m.group(1).replace(",", "")) for m in CREDIT_RE.finditer(text)]
        return (max(hits) if hits else None), {e.lower() for e in EMAIL_RE.findall(text)}

    credits, emails = scan()
    if credits is None or REQUIRED not in emails:
        for sel in ('[aria-label*="Account details" i]', '[aria-label*="Google Account" i]',
                    'button:has-text("ULTRA")', "text=ULTRA"):
            try:
                loc = page.locator(sel).first
                if loc.count():
                    loc.click(timeout=2500)
                    time.sleep(1.4)
                    break
            except Exception:
                continue
        c2, e2 = scan()
        credits = c2 if c2 is not None else credits
        emails |= e2
        try:
            page.keyboard.press("Escape")
        except Exception:
            pass
    account = REQUIRED if REQUIRED in emails else (sorted(emails)[0] if emails else None)
    return credits, account


def flow_page(browser, flow):
    ctx = browser.contexts[0]
    for pg in ctx.pages:
        if "flow.google.com" in (pg.url or "") and "/about" not in (pg.url or ""):
            pg.bring_to_front()
            return pg
    pg = ctx.new_page()
    pg.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
    time.sleep(3)
    flow.dismiss_banners(pg)
    return pg


def core_for(plate: dict) -> str:
    core = " ".join(plate["prompt"].split())
    if plate.get("explorer"):
        core = core.replace("No Explorer.", "") + " " + EXPLORER
    return core


def prompt_for(plate: dict, i2v: bool = False) -> str:
    lead = ("Animate the attached start frame; keep its exact cartoon look, objects and light."
            if i2v else "IMAGE-TO-VIDEO from text description (no attached still).")
    return (f"{lead} {LOOK} {core_for(plate)} "
            "Silent picture only. Continuous real camera and subject motion through the final frame.")


def contact_sheet(mp4: Path, out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", str(mp4), "-vf",
         "fps=6/8,scale=480:-2,tile=3x2", "-frames:v", "1", str(out)], check=True)


def freeze_events(mp4: Path) -> int:
    err = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", str(mp4), "-vf", "freezedetect=n=0.003:d=0.8",
         "-f", "null", "-"], capture_output=True, text=True, errors="replace").stderr
    return err.count("freeze_start")


def hover_fetch(page) -> bytes | None:
    """Clicking a tile opens no player; hovering a clip tile mounts a <video> whose src
    the signed-in browser session can fetch. The uploaded start still is a tile too,
    so hover every tile (top-left first) until one mounts a video."""
    try:
        boxes = [b for b in (i.bounding_box() for i in page.locator("img").all())
                 if b and b.get("width", 0) > 80]
        for box in sorted(boxes, key=lambda b: (round(b["y"]), b["x"])):
            page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            time.sleep(2)
            srcs = page.evaluate(
                "() => [...document.querySelectorAll('video')].map(v => v.currentSrc || v.src).filter(Boolean)")
            for src in srcs:
                r = page.context.request.get(src, timeout=120_000)
                body = r.body()
                if r.status == 200 and len(body) > 400_000 and b"ftyp" in body[:64]:
                    return body
            page.mouse.move(5, 5)
            time.sleep(0.5)
    except Exception as e:
        print(f"  hover fetch warn: {e}", flush=True)
    return None


def settled_credits(page, wait_s: int = 60) -> int | None:
    """Flow shows a Create's charge with a lag; wait for two equal reads 10 s apart."""
    last, _ = read_account(page)
    t0 = time.time()
    while time.time() - t0 < wait_s:
        time.sleep(10)
        cur, _ = read_account(page)
        if cur == last:
            return cur
        last = cur
    return last


def harvest(page, flow, project_url: str, dest: Path, wait_s: int = 360) -> None:
    """Play the new gallery clip and save the mp4 from the network (HOS 004 path)."""
    captured: list[bytes] = []

    def on_resp(resp) -> None:
        try:
            u = (resp.url or "").lower()
            ct = (resp.headers.get("content-type") or "").lower()
            if resp.status == 200 and ("flow-content.google/video" in u or "googlevideo.com" in u
                                       or "videoplayback" in u or "video/mp4" in ct):
                body = resp.body()
                if body and len(body) > 400_000 and b"ftyp" in body[:64]:
                    captured.append(body)
        except Exception:
            pass

    page.on("response", on_resp)
    try:
        page.goto(project_url, wait_until="domcontentloaded", timeout=120_000)
        time.sleep(3)
        flow.dismiss_banners(page)
        t0 = time.time()
        while time.time() - t0 < wait_s and not captured:
            thumbs = flow.collect_gallery_asb_srcs(page)
            print(f"  harvest poll thumbs={len(thumbs)} elapsed={time.time() - t0:.0f}s", flush=True)
            if thumbs:
                body = hover_fetch(page)
                if body:
                    captured.append(body)
                    break
                try:
                    page.locator(f'img[src="{thumbs[-1]}"]').first.click(timeout=8000)
                    time.sleep(1.5)
                    for _ in range(3):
                        if captured:
                            break
                        try:
                            page.locator("video").first.click(timeout=2000)
                        except Exception:
                            pass
                        time.sleep(2.5)
                except Exception as e:
                    print(f"  thumb click warn: {e}", flush=True)
            if captured:
                break
            time.sleep(8)
            try:
                page.reload(wait_until="domcontentloaded", timeout=60_000)
                time.sleep(2)
            except Exception:
                pass
    finally:
        page.remove_listener("response", on_resp)
    if not captured:
        raise RuntimeError(f"harvest timeout {wait_s}s project={project_url}")
    dest.write_bytes(max(captured, key=len))


def mint(part: str, only: set[str], max_n: int | None, stills: bool = False, take: int = 1) -> int:
    import orbit_flow_veo_ui as flow
    from playwright.sync_api import sync_playwright

    flow.FLOW_HOME = os.environ.get("ORBIT_FLOW_HOME", "https://flow.google.com/")
    raw, uat, _ = paths(part)
    raw.mkdir(parents=True, exist_ok=True)
    log = load_log(part)
    key = (lambda pid: pid) if take == 1 else (lambda pid: f"{pid}#t{take}")
    if stills:
        import _flow_still_v01 as still_tool
        log["engine"] = "Flow Image Nano Banana 2 16:9 still -> Veo 3.1 image-to-video via CDP :9222"
    def unspent_fail(e: dict) -> bool:
        if e.get("status") == "STOP" and not e.get("project_url"):
            return True
        return e.get("status") == "FAIL" and e.get("credits_after") == e.get("credits_before")

    todo = [p for p in plates(part) if (not only or p["id"] in only)
            and (key(p["id"]) not in log["takes"] or unspent_fail(log["takes"][key(p["id"])]))]
    if max_n:
        todo = todo[:max_n]
    print(f"Part {part}: {len(todo)} plates to mint -> {raw}", flush=True)

    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp(CDP)
        page = flow_page(browser, flow)
        credits, account = read_account(page)
        print(f"GATE account={account} credits={credits}", flush=True)
        if account != REQUIRED or FORBIDDEN in (account or ""):
            raise SystemExit(f"STOP wrong Flow account: {account}")
        if credits is None:
            raise SystemExit("STOP Flow credits unreadable")
        log.setdefault("balance_reads", []).append({"at": now(), "credits": credits, "when": "start"})
        save_log(part, log)

        for plate in todo:
            pid, q = plate["id"], plate["quality"]
            cost = COST[q]
            if credits - cost < FLOOR:
                print(f"STOP floor: {pid} needs {cost}, balance {credits}", flush=True)
                log["stopped"] = {"at": now(), "plate": pid, "credits": credits, "why": "floor 0"}
                save_log(part, log)
                return 3
            if UNPAID_RE.search(body_text(page)):
                raise SystemExit(f"STOP Flow billing/credit banner before {pid}")
            dest = raw / f"{pid}_t{take}.mp4"
            model = f"Veo 3.1 - {q}"
            print(f"\n=== {pid} {model} cost~{cost} balance={credits} ===", flush=True)
            entry = {"plate": pid, "take": take, "model": model, "quality": q,
                     "path": "flow-cdp-still-i2v" if stills else "flow-cdp",
                     "explorer": bool(plate.get("explorer")), "prompt": prompt_for(plate, stills),
                     "credits_before": credits, "submitted_at": now()}
            start = None
            try:
                try:
                    flow.recover_flow_home(page)
                except Exception:
                    pass
                if stills:
                    settled = settled_credits(page)
                    if settled is not None:
                        credits = entry["credits_before"] = settled
                    start = raw.parent.parent / "refs/v02_flow_stills" / f"{pid}_t{take}.png"
                    entry["still_prompt"] = still_tool.still_prompt(LOOK, core_for(plate))
                    if start.exists() and start.stat().st_size > 100_000:
                        print(f"  reuse still {start.name}", flush=True)
                        entry["still_reused"] = True
                    else:
                        still_tool.make_still(page, entry["still_prompt"], start)
                    entry["start_frame_sha256"] = still_tool.assert_unique_still(start, MEDIA / "04_Generated-Clips")
                    after_still, _ = read_account(page)
                    entry.update(start_frame=str(start), start_frame_sha256=sha256(start),
                                 style_ref_chips=getattr(still_tool.make_still, "refs_attached", None),
                                 credits_after_still=after_still)
                    if after_still is not None and after_still < credits:
                        entry.update(status="STOP", why=f"still cost {credits - after_still} credits (passed at 0)")
                        log["takes"][key(pid)] = entry
                        log["stopped"] = {"at": now(), "plate": pid, "why": entry["why"]}
                        save_log(part, log)
                        print(f"STOP {entry['why']}", flush=True)
                        return 5
                # The start-frame attach re-locks the model from this env (default Quality).
                os.environ["ORBIT_FLOW_VEO_MODEL"] = model
                info = flow.generate_clip(page, entry["prompt"], dest, model=model, timeout_s=600,
                                          start_frame=start, scenery_only=start is None, attempts=1,
                                          reuse_project=False) or {}
                entry["project_url"] = info.get("project_url") or info.get("url") or ""
                if not dest.exists() or dest.stat().st_size < 400_000:
                    if "/project/" not in entry["project_url"]:
                        raise RuntimeError(f"no mp4 and no project URL after Create: {entry['project_url']!r}")
                    print(f"  gallery harvest via {entry['project_url']}", flush=True)
                    harvest(page, flow, entry["project_url"], dest, wait_s=60)
                import orbit_gemini_veo as veo
                veo.strip_audio(dest)
                sheet = uat / f"{pid}_t{take}_sheet.jpg"
                contact_sheet(dest, sheet)
                entry.update(status="PENDING_UAT", file=str(dest), sha256=sha256(dest),
                             duration_s=round(duration(dest), 3), uat_sheet=str(sheet),
                             motion={"freeze_events_0p8s": freeze_events(dest)})
            except SystemExit:
                raise
            except Exception as e:
                entry.update(status="FAIL", why=f"{type(e).__name__}: {str(e)[:600]}")
                print(f"  FAIL {pid}: {entry['why']}", flush=True)
            after, _ = read_account(page)
            if after is not None:
                entry["credits_after"] = after
                entry["credits_used"] = max(0, credits - after)
                credits = after
            else:
                credits -= cost
            entry["at"] = now()
            log["takes"][key(pid)] = entry
            log.setdefault("balance_reads", []).append({"at": now(), "credits": credits, "after": pid})
            save_log(part, log)
            print(f"  -> {entry['status']} used={entry.get('credits_used')} balance={credits}", flush=True)
            if entry["status"] == "FAIL" and "credit" in entry.get("why", "").lower():
                return 4
            if (entry.get("credits_used") or 0) > cost:
                log["stopped"] = {"at": now(), "plate": pid, "credits": credits,
                                  "why": f"charged {entry['credits_used']} > priced {cost} (model drift?)"}
                save_log(part, log)
                print(f"STOP {log['stopped']['why']}", flush=True)
                return 6

    sheets = sorted(uat.glob("*_sheet.jpg"))
    print(f"DONE part {part}; sheets in {uat} ({len(sheets)})", flush=True)
    return 0


def harvest_spent(part: str, wait_s: int = 120) -> int:
    """0 credits: download paid takes whose harvest timed out, from their project_url."""
    import orbit_flow_veo_ui as flow
    import orbit_gemini_veo as veo
    from playwright.sync_api import sync_playwright

    raw, uat, _ = paths(part)
    log = load_log(part)
    todo = {k: e for k, e in log["takes"].items()
            if e.get("status") == "FAIL" and "/project/" in (e.get("project_url") or "")
            and "harvest timeout" in (e.get("why") or "")}
    print(f"Part {part}: {len(todo)} paid takes to harvest", flush=True)
    missed = 0
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp(CDP)
        page = flow_page(browser, flow)
        before, account = read_account(page)
        if account != REQUIRED:
            raise SystemExit(f"STOP wrong Flow account: {account}")
        for k, e in todo.items():
            dest = Path(e.get("file") or raw / f"{e['plate']}_t{e['take']}.mp4")
            print(f"\n=== harvest {k} {e['project_url']} ===", flush=True)
            try:
                harvest(page, flow, e["project_url"], dest, wait_s=wait_s)
                veo.strip_audio(dest)
                sheet = uat / f"{e['plate']}_t{e['take']}_sheet.jpg"
                contact_sheet(dest, sheet)
                e.update(status="PENDING_UAT", file=str(dest), sha256=sha256(dest),
                         duration_s=round(duration(dest), 3), uat_sheet=str(sheet),
                         motion={"freeze_events_0p8s": freeze_events(dest)},
                         harvested_at=now(), harvest="harvest-only pass, 0 credits")
                print(f"  OK {dest.name} {e['duration_s']}s", flush=True)
            except Exception as ex:
                missed += 1
                e["harvest_retry"] = f"{now()} {type(ex).__name__}: {str(ex)[:200]}"
                print(f"  MISS {k}: {ex}", flush=True)
            save_log(part, log)
        after, _ = read_account(page)
        log.setdefault("balance_reads", []).append(
            {"at": now(), "credits": after, "when": f"harvest-only (before {before})"})
        save_log(part, log)
        if before is not None and after is not None and after < before:
            print(f"WARN credits moved during harvest: {before} -> {after}", flush=True)
    print(f"DONE harvest part {part}: {len(todo) - missed} ok, {missed} missed", flush=True)
    return 1 if missed else 0


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--part", choices=sorted(PASSED))
    ap.add_argument("--only", nargs="*", default=[])
    ap.add_argument("--max", type=int)
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--stills", action="store_true", help="Flow Nano Banana 2 start still, then i2v")
    ap.add_argument("--take", type=int, default=1)
    ap.add_argument("--harvest", action="store_true",
                    help="0 credits: download paid takes whose harvest timed out")
    ap.add_argument("--wait", type=int, default=120, help="harvest wait per take, seconds")
    a = ap.parse_args()
    if a.list:
        total = 0
        for part in sorted(PASSED):
            for p in plates(part):
                total += COST[p["quality"]]
                print(f"P{part}:{p['id']:<22} {p['quality']:<8} {COST[p['quality']]:>4}  run {total}")
        print(f"{sum(len(v) for v in PASSED.values())} plates, {total} credits")
        return
    if not a.part:
        ap.error("--part is required")
    if a.harvest:
        sys.exit(harvest_spent(a.part, a.wait))
    sys.exit(mint(a.part, set(a.only), a.max, a.stills, a.take))


if __name__ == "__main__":
    main()
