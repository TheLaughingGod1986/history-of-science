#!/usr/bin/env python3
"""LEGACY — JWST Omni variant regen via ElevenLabs Image & Video.

DO NOT USE FOR NEW WORK. Use Gemini Veo:
  python3 04_Audio/tools/orbit_gemini_veo.py
  or 07_Edit-Project/_generate_veo_gemini_api_v01.py

VO stays on ElevenLabs TTS (separate from this CG path).

Was: p1–p4 unique takes for 1× motion coverage when Omni inventory was thin.
"""
from __future__ import annotations

import importlib.util
import json
import sys
import time
from pathlib import Path

ROOT = Path(
    "/Users/ben/code/Orbit-YouTube/02_Video-Projects/"
    "004_JWST-Discoveries-That-Change-Everything"
)
EDIT = ROOT / "07_Edit-Project"
GEN = EDIT / "_generate_omni_v01.py"
RAW = ROOT / "04_Generated-Clips/01_Raw"
LOG = ROOT / "03_Animation-Prompts/03_Generation-Logs/jwst_omni_variants_v02.jsonl"
PLAN = EDIT / "MOTION_COVERAGE_REGEN_v02.md"

VARIANT_PASSES = ("p1", "p2", "p3", "p4")
CONCURRENCY = 1  # serial submit — concurrent mode burned slots with "no new generation"
ANTI_EIFFEL_PASS = (
    " START ON ORBIT IN SPACE ONLY — never open on paper, parchment, architectural "
    "blueprints, lattice iron towers, or the Eiffel Tower. No Paris landmarks. "
    "No Explore-gallery schematic overlays. Orbit must be visible in frame 1."
)

ANGLE = {
    "p1": (
        " Camera: gentle push-in, three-quarter view on Orbit's left. "
        "Continuous hover and eye emotion; scenery keeps changing — "
        "no static plate, no repeating tiled galaxies."
        + ANTI_EIFFEL_PASS
    ),
    "p2": (
        " Camera: slow lateral drift right, slightly wider establishing frame. "
        "Orbit reacts with cream-eye emotion; full body motion throughout. "
        "No freeze, no identical copy-paste background elements."
        + ANTI_EIFFEL_PASS
    ),
    "p3": (
        " Camera: soft arc around Orbit, warm rim light, parallax depth. "
        "Continuous motion through the final frame — avoid end-frame collapse "
        "into empty tiled stars."
        + ANTI_EIFFEL_PASS
    ),
    "p4": (
        " Camera: intimate close-up then ease out to medium. "
        "Antenna and underside glow stay readable; rich distinct scenery. "
        "Hold quality through the last second — no morph into blueprint/lattice."
        + ANTI_EIFFEL_PASS
    ),
}


def load_gen():
    spec = importlib.util.spec_from_file_location("omni_v01", GEN)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def variant_dest(scene: str, beat: str, slug: str, pass_id: str) -> Path:
    return RAW / f"scene-{scene}" / f"{pass_id}_{beat}_{slug}_gemini-omni-flash_v02_raw.mp4"


def build_queue(mod):
    queue = []
    for scene, beat, slug, prompt in mod.load_beats():
        for pass_id in VARIANT_PASSES:
            dest = variant_dest(scene, beat, slug, pass_id)
            body = (prompt.rstrip() + ANGLE[pass_id]).strip()
            queue.append((scene, beat, slug, pass_id, body, dest))
    return queue


def write_plan(queue, have_p0: int) -> None:
    need = len(queue)
    total = have_p0 + need
    PLAN.write_text(
        f"""# JWST motion-coverage regen v02

## Problem
- VO ~16.4 min; only **{have_p0}** unique Omni clips (~8s).
- Slow-mo → laggy. Long still-pan fills → stuck/static.
- Correct fix: **more unique 1× motion clips**.

## Target
- Generate **{need}** new variants (`p1`–`p4` × 24 beats).
- Total ≈ **{total}** unique 8s clips (~{total * 6:.0f}s usable after ~2.5s tail trim).
- Rebuild master at **1× only**; still-pan only for **≤4s** leftovers.
- Rebuild Shorts; replace YouTube uploads.

## Guards
- Clear start/end image refs every take (no Eiffel Explore blueprint).
- Prompt lock: FORBIDDEN Eiffel Tower / parchment blueprints / Paris landmarks.
- Orbit Headshot + Gemini Omni Flash 8s.
- Post-download QA: reject parchment first-frame (paper≥0.45 & orange≈0); quarantine + retry.
- Speed: pipeline concurrency={CONCURRENCY} overlapping server gens.

## Status
- Queue written: {time.strftime("%Y-%m-%d %H:%M")}
- Log: `{LOG.relative_to(ROOT)}`
"""
    )


def known_ids(mod, token: str) -> set[str]:
    return {
        g["id"]
        for g in (mod.api_get("/v1/content/generations?per_page=40", token).get("generations") or [])
        if g.get("id")
    }


def submit_one(mod, page, prompt: str, token: str) -> str:
    """Fire one Omni generate; return generation id (not waited to complete)."""
    left = mod.credits_left(page)
    if left == "0":
        print("concurrent 0 left — waiting 35s", flush=True)
        time.sleep(35)
    # Always land on Video composer before prompt (anti Lip-sync + anti-Eiffel Explore refs)
    mod.click_video_tab(page)
    if mod.on_lip_sync(page) or "Omni" not in (mod.read_model_chip(page) or ""):
        mod.force_video_composer(page)
        mod.setup_composer(page)
    mod.clear_image_refs(page)
    before = known_ids(mod, token)
    mod.set_prompt(page, prompt)
    page.wait_for_timeout(350)
    mod.clear_image_refs(page)
    mod.click_video_tab(page)
    if "Omni" not in (mod.read_model_chip(page) or ""):
        mod.force_omni(page)
        mod.set_duration_8s(page)
    if mod.on_lip_sync(page):
        print("  WARN Lip sync tab — forcing Video composer", flush=True)
        mod.force_video_composer(page)
        mod.setup_composer(page)
        mod.set_prompt(page, prompt)
        page.wait_for_timeout(300)
        mod.clear_image_refs(page)
    if mod.on_lip_sync(page):
        raise RuntimeError("stuck on Lip sync before Generate")
    # Final scrub — Explore often rebinds start-frame after prompt paste.
    # Do NOT attach Orbit start-frame here: uploading an image ref often leaves
    # Generate stuck Loading/disabled. Prefer clear refs + post-download trim salvage.
    mod.clear_image_refs(page)
    mod.click_video_tab(page)
    if not mod.click_generate(page):
        raise RuntimeError("no generate button")
    page.wait_for_timeout(3500)
    if mod.on_lip_sync(page):
        # Generation may still have fired — check for new id before failing
        try:
            gid, _ = mod.wait_seen(token, before, timeout_s=40)
            mod.force_video_composer(page)
            return gid
        except Exception:
            raise RuntimeError("Generate landed on Lip sync") from None
    try:
        gid, _ = mod.wait_seen(token, before, timeout_s=210)
    except TimeoutError as e:
        # UI often goes stale after long runs — hard refresh once
        print("  no new gen — reloading Image/Video…", flush=True)
        page.goto(
            "https://elevenlabs.io/app/image-video?modality=video",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(3500)
        mod.setup_composer(page)
        mod.clear_image_refs(page)
        # One more poll after reload — gen may have landed server-side
        try:
            gid, _ = mod.wait_seen(token, before, timeout_s=45)
            print(f"  recovered after reload: {gid}", flush=True)
            return gid
        except TimeoutError:
            raise RuntimeError("no new generation (reloaded)") from e
    # Leave UI on Video so the next submit is fast
    try:
        mod.click_video_tab(page)
        if mod.on_lip_sync(page):
            mod.force_video_composer(page)
        mod.clear_image_refs(page)
    except Exception:
        pass
    return gid


def finalize_job(mod, job: dict) -> bool:
    """Download + Eiffel QA. True if kept."""
    g = job["g"]
    dest: Path = job["dest"]
    dest.parent.mkdir(parents=True, exist_ok=True)
    if g.get("model_id") and "omni" not in str(g.get("model_id")).lower():
        print("WARN wrong model", g.get("model_id"), flush=True)
    mod.download(g, dest)
    if not mod.already_done(dest):
        raise RuntimeError(f"download too small: {dest.stat().st_size}")
    mod.strip_native_audio(dest)
    eiffel = mod.reject_eiffel_startframe(dest)
    if eiffel:
        raise RuntimeError(f"Eiffel QA reject: {eiffel}")
    rec = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "pass": job["pass_id"],
        "scene": job["scene"],
        "beat": job["beat"],
        "slug": job["slug"],
        "generation_id": g["id"],
        "model_id": g.get("model_id"),
        "file": str(dest),
        "bytes": dest.stat().st_size,
        "attempt": job["attempt"],
        "eiffel_qa": "pass",
    }
    with LOG.open("a") as f:
        f.write(json.dumps(rec) + "\n")
    print(f"SAVED {dest.name} ({dest.stat().st_size}) eiffel_qa=pass", flush=True)
    return True


def poll_inflight(mod, token: str, inflight: list[dict]) -> list[dict]:
    """Complete any finished jobs; return list of items that need resubmit."""
    retry: list[dict] = []
    still: list[dict] = []
    for job in inflight:
        g = mod.api_get(f"/v1/content/generations/{job['gid']}", token)
        st = g.get("status")
        print(f"  poll {job['gid']} {st} ({job['pass_id']} {job['scene']}{job['beat']})", flush=True)
        if st == "completed":
            job["g"] = g
            try:
                finalize_job(mod, job)
            except Exception as e:
                print(f"  finalize failed: {e}", flush=True)
                job["attempt"] += 1
                if job["attempt"] <= 4:
                    retry.append(job)
                else:
                    print(f"FAIL {job['pass_id']} scene-{job['scene']} {job['beat']}", flush=True)
        elif st in ("failed", "error"):
            print(f"  gen failed: {g.get('error_message') or st}", flush=True)
            job["attempt"] += 1
            if job["attempt"] <= 4:
                retry.append(job)
            else:
                print(f"FAIL {job['pass_id']} scene-{job['scene']} {job['beat']}", flush=True)
        else:
            still.append(job)
    inflight[:] = still
    return retry


def main(limit: int | None = None) -> None:
    from playwright.sync_api import sync_playwright

    mod = load_gen()
    queue = build_queue(mod)
    pending = [q for q in queue if not mod.already_done(q[5])]
    have_p0 = sum(
        1
        for scene, beat, slug, _ in mod.load_beats()
        if mod.already_done(mod.out_path(scene, beat, slug))
    )
    write_plan(queue, have_p0)
    print(f"plan → {PLAN}", flush=True)
    print(
        f"variants total {len(queue)} · pending {len(pending)} · have p0 {have_p0} · "
        f"concurrency={CONCURRENCY}",
        flush=True,
    )
    if limit is not None:
        pending = pending[:limit]
        print(f"this run limited to {len(pending)}", flush=True)
    if not pending:
        print("nothing to generate")
        return

    LOG.parent.mkdir(parents=True, exist_ok=True)
    mod.AUDIT.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            str(mod.PROFILE),
            headless=False,
            channel="chrome",
            viewport={"width": 1440, "height": 1000},
            args=["--disable-blink-features=AutomationControlled"],
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.goto(
            "https://elevenlabs.io/app/image-video?modality=video",
            wait_until="domcontentloaded",
            timeout=120000,
        )
        page.wait_for_timeout(3500)
        chip = mod.setup_composer(page)
        print("ready chip=", chip, "credits≈", mod.credits_left(page), flush=True)
        if "Omni" not in (chip or ""):
            print("FATAL: could not select Gemini Omni Flash", flush=True)
            ctx.close()
            raise SystemExit(2)

        inflight: list[dict] = []
        retry_q: list[tuple] = []
        consecutive_fail = 0
        i = 0
        items = list(pending)

        while i < len(items) or inflight or retry_q:
            token = mod.bearer(page)

            # Prefer retries, then new queue items
            while len(inflight) < CONCURRENCY and (retry_q or i < len(items)):
                if retry_q:
                    scene, beat, slug, pass_id, prompt, dest, attempt = retry_q.pop(0)
                else:
                    scene, beat, slug, pass_id, prompt, dest = items[i]
                    i += 1
                    attempt = 1
                if mod.already_done(dest):
                    continue
                print(
                    f"\n=== SUBMIT {pass_id} scene-{scene} {beat} {slug} · "
                    f"attempt={attempt} · credits≈{mod.credits_left(page)} · "
                    f"inflight={len(inflight)} ===",
                    flush=True,
                )
                try:
                    gid = submit_one(mod, page, prompt, token)
                    inflight.append(
                        {
                            "gid": gid,
                            "scene": scene,
                            "beat": beat,
                            "slug": slug,
                            "pass_id": pass_id,
                            "prompt": prompt,
                            "dest": dest,
                            "attempt": attempt,
                        }
                    )
                    consecutive_fail = 0
                    time.sleep(0.8)
                except Exception as e:
                    print(f"  submit failed: {e}", flush=True)
                    page.keyboard.press("Escape")
                    page.wait_for_timeout(400)
                    try:
                        mod.force_video_composer(page)
                        mod.setup_composer(page)
                    except Exception:
                        pass
                    if attempt < 4:
                        retry_q.append((scene, beat, slug, pass_id, prompt, dest, attempt + 1))
                    else:
                        consecutive_fail += 1
                        print(f"FAIL {pass_id} scene-{scene} {beat}", flush=True)
                        if consecutive_fail >= 3:
                            print("ABORT: 3 consecutive submit failures", flush=True)
                            ctx.close()
                            raise SystemExit(1)

            # Poll / harvest
            if inflight:
                token = mod.bearer(page)
                need_retry = poll_inflight(mod, token, inflight)
                for job in need_retry:
                    retry_q.append(
                        (
                            job["scene"],
                            job["beat"],
                            job["slug"],
                            job["pass_id"],
                            job["prompt"],
                            job["dest"],
                            job["attempt"],
                        )
                    )
                if inflight and len(inflight) >= CONCURRENCY:
                    time.sleep(2)
                elif inflight:
                    time.sleep(1.2)

        ctx.close()
    print("\nvariant batch complete", flush=True)


if __name__ == "__main__":
    lim = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else None
    try:
        main(lim)
    except SystemExit:
        raise
    except Exception:
        import traceback

        print("=== FATAL TRACEBACK ===", flush=True)
        traceback.print_exc()
        raise
