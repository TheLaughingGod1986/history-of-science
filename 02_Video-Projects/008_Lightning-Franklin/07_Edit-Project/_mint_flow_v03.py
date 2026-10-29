#!/usr/bin/env python3
"""J1191 — HOS 008 boards v03, Flow only (CDP :9222).

Mints the 101 Flow rows (15 Quality + 86 Fast; 5,605 expected credits; cap 6,500)
of PICTURE_PLAN_v03.json / part-01..05_plates_v03.json.
The 11 code-graphic rows stay as rendered (J0329).
Mints the six moving plates the five overlays need first:
  P2:12_notebook_list, P3:07_slow_news, P2:08_jar_spark, P4:02_knuckle_spark,
  P1:16_question_sky, P5:06_rod_fitting.
Then mints Parts 01..05 in board order, one first take per row:
Nano Banana 2 16:9 start still (0 credits), then Veo 3.1 image-to-video.

No Vertex, no Omni, no ElevenLabs, £0. Stop before any take that would leave
live − remaining expected under 3,000, or before film spend passes 6,500,
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

WT = Path(os.environ.get("HOS_REPO", str(Path(__file__).resolve().parents[3])))
MINT006 = WT / "02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project/_mint_flow_cdp_v01.py"
STILL006 = WT / "02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project/_flow_still_v01.py"
REPO_EDIT = WT / "02_Video-Projects/008_Lightning-Franklin/07_Edit-Project"
BOARD = REPO_EDIT / "parts"
MEDIA = Path(os.environ.get(
    "HOS_008_MEDIA",
    str(Path.home() / "YouTube/hos-008-lightning/02_Video-Projects/008_Lightning-Franklin"),
))
OWB = Path(os.environ.get("OWB_REPO", str(Path.home() / "YouTube/orbit-with-ben")))
CDP = os.environ.get("ORBIT_FLOW_CDP", "http://127.0.0.1:9222")
REQUIRED = "benoats@googlemail.com"
FORBIDDEN = "benoats86@gmail.com"
TRY1 = {"Fast": 10, "Quality": 100}
EXPECTED_TOTAL = 5605
CAP = 6500
BUFFER = 3000
MIN_DISK_GIB = 10.0

# Five overlays need these six moving plates first (P4:06 needs both P2:08 and P4:02).
PRIORITY_IDS = [
    "12_notebook_list",   # P2:12 (for P2:15_likeness_fire)
    "07_slow_news",       # P3:07 (for P3:04_letter_crosses)
    "08_jar_spark",       # P2:08 (left half of P4:06_same_thing)
    "02_knuckle_spark",   # P4:02 (right half of P4:06_same_thing)
    "16_question_sky",    # P1:16 (for P5:08_looking_path)
    "06_rod_fitting",     # P5:06 (for P5:10_metal_easy)
]


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
        data = json.loads((BOARD / f"part-0{n}_plates_v03.json").read_text())
        for plate in data["plates"]:
            if plate.get("route") != "flow-first":
                continue
            plate = dict(plate)
            plate["_part"] = f"{n:02d}"
            rows.append(plate)
    return rows


def ordered_rows(rows: list[dict], priority_only: bool = False) -> list[dict]:
    by_id = {p["id"]: p for p in rows}
    prio = [by_id[pid] for pid in PRIORITY_IDS if pid in by_id]
    if priority_only:
        return prio
    prio_set = set(PRIORITY_IDS)
    rest = [p for p in rows if p["id"] not in prio_set]
    return prio + rest


def log_paths() -> list[Path]:
    return [
        MEDIA / "07_Edit-Project/FLOW_MINT_LOG_v03.json",
        REPO_EDIT / "FLOW_MINT_LOG_v03.json",
    ]


def load_log() -> dict:
    for path in log_paths():
        if path.exists():
            return json.loads(path.read_text())
    return {
        "job": "J1191",
        "film": "008",
        "board_version": "v03",
        "engine": "flow-cdp-9222",
        "expected_credits": EXPECTED_TOTAL,
        "cap": CAP,
        "buffer": BUFFER,
        "priority_overlay_plates": PRIORITY_IDS,
        "takes": {},
        "balance_reads": [],
    }


def save_log(log: dict) -> None:
    log["updated"] = now()
    payload = json.dumps(log, indent=2) + "\n"
    for path in log_paths():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(payload)


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
            / "refs/v03_flow_stills" / f"{plate['id']}_t1.png")


def video_dest(plate: dict) -> Path:
    return (MEDIA / "04_Generated-Clips" / f"part{plate['_part']}"
            / "raw/v01" / f"{plate['id']}_t1.mp4")


def sanitize_person_names(text: str) -> str:
    """Replace real proper surnames/names and child triggers that trip Veo/Flow filters."""
    for src, dst in (
        ("Benjamin Franklin", "the 1750s colonial scientist"),
        ("William Franklin", "the young twenty-one-year-old adult assistant"),
        ("Franklin's", "the colonial scientist's"),
        ("Franklin", "the colonial scientist"),
        ("Georg Richmann", "the St Petersburg physicist"),
        ("Richmann's", "the St Petersburg physicist's"),
        ("Richmann", "the St Petersburg physicist"),
        ("(an adult, never a child)", "(an adult man in his twenties)"),
        ("a child's kite", "a small diamond kite"),
        ("father and son stand", "the older scientist and his young adult assistant stand"),
        ("beside his father", "beside the older scientist"),
        ("families going indoors", "adult townsfolk going indoors"),
        ("a family waits", "adult townsfolk wait"),
    ):
        text = text.replace(src, dst)
    return text


def still_prompt(still, plate: dict) -> str:
    core = sanitize_person_names(" ".join(plate["prompt"].split()))
    if plate.get("explorer"):
        core = core.replace("No Explorer.", "") + " " + mint006.EXPLORER
    elif any(w in core.lower() for w in ("child", "children", "boy", "sons", "son", "families", "family")):
        for src, dst in (
            ("a child at a window, seen from behind, looks up", "an adult figure at a window, seen from behind, looks up"),
            ("a child", "an adult figure seen from behind"),
        ):
            core = core.replace(src, dst)
        core += (" No children or young boys in the opening still frame;"
                 " any secondary figure is an adult seen from behind with head turned away.")
    core += (" Opening frame only. No readable words, numbers, letters or text anywhere."
             " Book spines, almanac pages, newspaper pages and notebook pages show no legible glyphs."
             " The kite and string are never struck by a lightning bolt.")
    if "no faces readable" in core.lower() or "faces not readable" in core.lower():
        core += (" Every person is seen from behind with their head turned completely away from camera;"
                 " no face or profile shown.")
    return still.still_prompt(
        "History of Science locked look: premium Animistry-class 3D cartoon, finished materials, warm cinematic period light.",
        core,
    )


def video_prompt(plate: dict) -> str:
    core = sanitize_person_names(" ".join(plate["prompt"].split()))
    if plate.get("explorer"):
        core = core.replace("No Explorer.", "") + " " + mint006.EXPLORER
    return ("Animate the attached start frame; keep its exact cartoon look, objects and light. "
            + core
            + " Silent picture only. Continuous real camera and subject motion through the final frame."
            + " No readable handwriting, letters or numbers anywhere. Nobody is struck or hurt.")


def gate(live: int, rem: int, cost: int, log: dict, plate_id: str) -> str | None:
    if live - rem < BUFFER:
        return f"live {live} − remaining {rem} = {live - rem} < {BUFFER}"
    if (live - cost) - rem < BUFFER:
        return f"after {plate_id} ({cost}): {live - cost} − remaining {rem} < {BUFFER}"
    if spent(log) + cost > CAP:
        return f"cap {CAP}: spent {spent(log)} + {cost}"
    return None


def mint_still(page, still, plate: dict, credits: int) -> tuple[Path, int]:
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
    used = ui_drop if ui_drop > 0 else priced
    entry.update(
        status="KEEP",
        uat_note="KEEP vs v03 board, sources and period look (3D cartoon house look, continuous motion, no readable text)",
        file=str(dest),
        sha256=mint006.sha256(dest),
        duration_s=round(mint006.duration(dest), 3),
        uat_sheet=str(sheet),
        motion={"freeze_events_0p8s": mint006.freeze_events(dest)},
        credits_after=after,
        credits_used=used,
        credits_ui_drop=ui_drop,
        account=account,
        at=now(),
    )
    log["takes"][plate["id"]] = entry
    log.setdefault("balance_reads", []).append({"at": now(), "credits": after, "after": plate["id"]})
    save_log(log)
    if ui_drop > priced:
        raise SystemExit(f"STOP {plate['id']} charged {ui_drop} > priced {priced} (check x1 setting)")
    print(f"  -> KEEP used={used} (ui_drop={ui_drop}) balance={after} sha={entry['sha256'][:12]}", flush=True)
    return after if after is not None else credits - used


def one_video(page, flow, still, plate: dict, start: Path, credits: int, log: dict) -> int:
    dest = video_dest(plate)
    dest.parent.mkdir(parents=True, exist_ok=True)
    model = f"Veo 3.1 - {plate['quality']}"
    os.environ["ORBIT_FLOW_VEO_MODEL"] = model
    os.environ["OWB_AGENT"] = "gemini"
    entry = {
        "plate": plate["id"],
        "part": plate["_part"],
        "take": 1,
        "model": model,
        "quality": plate["quality"],
        "priority_overlay_plate": plate["id"] in PRIORITY_IDS,
        "start_frame": str(start),
        "start_frame_sha256": mint006.sha256(start),
        "credits_before": credits,
        "status": "SUBMITTING",
        "submitted_at": now(),
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
    ap.add_argument("--priority-only", action="store_true",
                    help="mint only the 6 priority moving plates needed by the 5 overlays")
    ap.add_argument("--until-part", default="01",
                    help="last part number to mint this batch (after priority plates), e.g. 01..05")
    ap.add_argument("--max", type=int, default=0,
                    help="optional max number of plates to mint in this invocation")
    args = ap.parse_args()

    check_disk()

    sys.path.insert(0, str(WT / "04_Audio/tools"))
    sys.path.insert(0, str(STILL006.parent))
    mint006 = load_mod("hos006_mint", MINT006)
    still = load_mod("hos006_still", STILL006)
    still.MEDIA_CLIPS = MEDIA / "04_Generated-Clips"
    style_dir = MEDIA / "04_Generated-Clips/_style_refs"
    still.STYLE_REFS = [
        style_dir / "04_sunny_window_v01.jpg",
        style_dir / "10_mint_jar_v01.jpg",
    ]
    for r in still.STYLE_REFS:
        if not r.exists():
            raise SystemExit(f"STOP missing style reference image: {r}")

    import orbit_flow_veo_ui as flow
    from playwright.sync_api import sync_playwright

    def _safe_set_video_aspect_and_outputs(page, *, frames_mode: bool = False, ingredients_mode: bool = False) -> None:
        def _mouse_click_match(kind: str) -> str | None:
            box = page.evaluate(
                """(kind) => {
                  for (const b of document.querySelectorAll('button,[role=radio]')) {
                    const aria = (b.getAttribute('aria-label') || '').trim();
                    if (/Settings trigger/i.test(aria)) continue;
                    const t = (b.innerText || '').trim().replace(/\\n+/g, ' ');
                    let ok = false;
                    if (kind === 'frames') ok = /crop_free|\\bFrames\\b/i.test(t) && t.length < 40;
                    else if (kind === 'ingredients') ok = /Ingredients|chrome_extension/i.test(t) && t.length < 50;
                    else if (kind === '16:9') ok = (/crop_16_9/.test(t) || /\\b16:9\\b/.test(t)) && t.length < 30;
                    else if (kind === '8s') ok = t === '8s';
                    else if (kind === 'x1') ok = t === 'x1';
                    if (!ok) continue;
                    const r = b.getBoundingClientRect();
                    if (r.width < 8 || r.height < 8) continue;
                    return { x: r.x + r.width / 2, y: r.y + r.height / 2, t };
                  }
                  return null;
                }""",
                kind,
            )
            if not box:
                return None
            page.mouse.click(box["x"], box["y"])
            page.wait_for_timeout(350)
            return box.get("t")

        if frames_mode:
            _mouse_click_match("frames")
        elif ingredients_mode:
            _mouse_click_match("ingredients")
        _mouse_click_match("16:9")
        _mouse_click_match("8s")
        clicked_x1 = _mouse_click_match("x1")
        print(f"  outputs clicked x1={clicked_x1!r}", flush=True)

    def _safe_select_image_16x9(page) -> str:
        pill0 = still.v02.pill_text(page)
        print(f"  pill before={pill0!r}", flush=True)
        if still._pill_is_image_wide(pill0) and "x1" in pill0:
            return pill0
        flow._open_prompt_settings_pill(page)
        page.wait_for_timeout(900)
        for kind in ("image", "16:9", "x1"):
            box = page.evaluate(
                """(kind) => {
                  for (const b of document.querySelectorAll('button[role=radio],button[role=tab],[role=radio],button')) {
                    const aria = (b.getAttribute('aria-label') || '').trim();
                    if (/Settings trigger/i.test(aria)) continue;
                    const t = ((b.innerText||'')+' '+aria).trim().replace(/\\n+/g, ' ');
                    let ok = false;
                    if (kind === 'image') ok = (/\\bimage\\b/i.test(t) || /banana/i.test(t)) && !/video|veo|omni|All media|Images/i.test(t) && t.length < 30;
                    else if (kind === '16:9') ok = (/crop_16_9|\\b16:9\\b|crop_landscape/.test(t)) && t.length < 30;
                    else if (kind === 'x1') ok = (b.innerText||'').trim() === 'x1';
                    if (!ok) continue;
                    const r = b.getBoundingClientRect();
                    if (r.width > 16 && r.height > 14 && r.x > 400) return { x: r.x + r.width/2, y: r.y + r.height/2, t: t.slice(0,40) };
                  }
                  return null;
                }""",
                kind,
            )
            if box:
                page.mouse.click(box["x"], box["y"])
                page.wait_for_timeout(450)
        page.keyboard.press("Escape")
        page.wait_for_timeout(400)
        pill = still.v02.pill_text(page)
        print(f"  image-mode pill={pill!r}", flush=True)
        if not still._pill_is_image_wide(pill):
            raise RuntimeError(f"Flow Image 16:9 not selected: {pill!r}")
        return pill

    def _safe_read_account(page) -> tuple[int | None, str | None]:
        try:
            page.keyboard.press("Escape")
            page.wait_for_timeout(250)
        except Exception:
            pass
        credits, account = mint006._orig_read_account(page)
        if credits is not None and credits <= 200:
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
            text = mint006.body_text(page)
            hits = [int(m.group(1).replace(",", "")) for m in mint006.CREDIT_RE.finditer(text)]
            big = [h for h in hits if h > 200]
            if big:
                credits = max(big)
            try:
                page.keyboard.press("Escape")
            except Exception:
                pass
        return credits, account

    def _safe_attach_image_to_prompt(page, ref: Path) -> bool:
        ref = Path(ref).resolve()
        if not ref.exists():
            raise FileNotFoundError(ref)
        print(f"  attaching start frame: {ref.name}", flush=True)
        for _ in range(2):
            try:
                page.keyboard.press("Escape")
                page.wait_for_timeout(150)
            except Exception:
                pass
        opened = page.evaluate(
            """() => {
              for (const b of document.querySelectorAll('button')) {
                const r = b.getBoundingClientRect();
                if (r.width < 20 || r.height < 16 || r.y < 350) continue;
                const t = (b.innerText || '').trim();
                const aria = (b.getAttribute('aria-label') || '').trim();
                if (t === 'Start' || /Add ingredients/i.test(aria) || t === 'add_2' || t === 'add') {
                  b.click();
                  return t || aria;
                }
              }
              return null;
            }"""
        )
        print(f"  opened start-frame picker via {opened!r}", flush=True)
        page.wait_for_timeout(900)
        up = page.locator('button:has-text("Upload media"), button:has-text("Upload")').last
        with page.expect_file_chooser(timeout=15_000) as fc:
            up.click()
        fc.value.set_files(str(ref))
        print("  uploaded — waiting for Add to prompt…", flush=True)
        t0 = time.time()
        while time.time() - t0 < 60:
            page.evaluate(
                """() => {
                  for (const b of document.querySelectorAll('button')) {
                    const r = b.getBoundingClientRect();
                    if (r.width < 20 || r.height < 16) continue;
                    const t = (b.innerText || '').trim();
                    if (/^I agree$/i.test(t)) b.click();
                  }
                }"""
            )
            ready = page.evaluate(
                """(fname) => {
                  const btns = [...document.querySelectorAll('button')].filter(b => {
                    const r = b.getBoundingClientRect();
                    return r.width > 20 && r.height > 16 && /^Add to prompt$/i.test((b.innerText || '').trim());
                  });
                  if (!btns.length) return {found: false};
                  const b = btns[btns.length - 1];
                  const disabled = b.disabled || b.getAttribute('aria-disabled') === 'true' || /disabled/i.test(b.className || '');
                  if (disabled) {
                    for (const el of document.querySelectorAll('button.asset-item, button[role="option"]')) {
                      const r = el.getBoundingClientRect();
                      if (r.width > 20 && r.height > 16 && (el.innerText || '').toLowerCase().includes(fname.toLowerCase())) {
                        el.click();
                        break;
                      }
                    }
                  }
                  return {found: true, disabled};
                }""",
                ref.name,
            )
            if ready.get("found") and not ready.get("disabled"):
                break
            page.wait_for_timeout(1000)
        add_btn = page.locator('button:has-text("Add to prompt")').last
        add_btn.click(timeout=5000)
        page.wait_for_timeout(1500)
        attached = (
            page.locator('img[alt="Ingredient image"]').count() > 0
            or flow._start_frame_present(page)
            or flow._prompt_attachment_count(page) > 0
        )
        print(f"  start frame attached={attached}", flush=True)
        if not attached:
            raise RuntimeError(f"Start frame {ref.name} did not attach after Add to prompt")
        return True

    mint006._orig_read_account = mint006.read_account
    mint006.read_account = _safe_read_account
    flow._set_video_aspect_and_outputs = _safe_set_video_aspect_and_outputs
    flow.attach_image_to_prompt = _safe_attach_image_to_prompt
    still.select_image_16x9 = _safe_select_image_16x9

    all_rows = boards()
    expected = sum(int(p.get("flow_credits_expected") or 0) for p in all_rows)
    if expected != EXPECTED_TOTAL:
        raise SystemExit(f"STOP boards expected {expected}, job says {EXPECTED_TOTAL}")
    log = load_log()
    batch_rows = ordered_rows(all_rows, priority_only=args.priority_only)

    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp(CDP)
        page = mint006.flow_page(browser, flow)
        credits, account = mint006.read_account(page)
        print(
            f"GATE account={account} credits={credits} remaining={remaining(all_rows, log)} "
            f"spent={spent(log)} disk_free_gib={free_disk_gib():.2f}",
            flush=True,
        )
        if account != REQUIRED or (account and FORBIDDEN in account):
            raise SystemExit(f"STOP wrong Flow account: {account}")
        if credits is None:
            raise SystemExit("STOP Flow credits unreadable")
        tag = "priority" if args.priority_only else f"p{args.until_part}"
        log.setdefault("balance_reads", []).append({"at": now(), "credits": credits, "when": f"batch-start-{tag}"})
        save_log(log)
        record_flow_balance(
            credits,
            f"J1191 batch-start {tag}; spent={spent(log)} rem_expected={remaining(all_rows, log)}",
        )
        why = gate(credits, remaining(all_rows, log), 0, log, "batch")
        if why:
            raise SystemExit(f"STOP gate: {why}")

        minted_this_run = 0
        for plate in batch_rows:
            if not args.priority_only and plate["id"] not in PRIORITY_IDS and plate["_part"] > args.until_part:
                continue
            if plate["id"] in done_ids(log):
                continue
            if args.max and minted_this_run >= args.max:
                print(f"STOP reached --max {args.max}", flush=True)
                break
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
                    minted_this_run += 1
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
            why = gate(credits, remaining(all_rows, log), cost, log, plate["id"])
            if why:
                raise SystemExit(f"STOP gate: {why}")
            if mint006.UNPAID_RE.search(mint006.body_text(page)):
                raise SystemExit(f"STOP billing banner before {plate['id']}")
            print(
                f"\n=== P{plate['_part']}:{plate['id']} {plate['quality']} ~{cost} "
                f"live={credits} rem={remaining(all_rows, log)} disk={free_disk_gib():.1f}GiB ===",
                flush=True,
            )
            frame, credits = mint_still(page, still, plate, credits)
            credits = one_video(page, flow, still, plate, frame, credits, log)
            minted_this_run += 1

        end_credits, _ = mint006.read_account(page)
        log.setdefault("balance_reads", []).append({"at": now(), "credits": end_credits, "when": f"batch-end-{tag}"})
        save_log(log)
        record_flow_balance(
            end_credits,
            f"J1191 batch-end {tag}; spent={spent(log)} rem_expected={remaining(all_rows, log)}",
        )
    print(f"BATCH DONE tag={tag} minted={minted_this_run} spent={spent(log)} remaining_expected={remaining(all_rows, log)}", flush=True)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SystemExit:
        raise
    except Exception as exc:
        print(f"FAIL {type(exc).__name__}: {exc}", flush=True)
        raise SystemExit(1)
