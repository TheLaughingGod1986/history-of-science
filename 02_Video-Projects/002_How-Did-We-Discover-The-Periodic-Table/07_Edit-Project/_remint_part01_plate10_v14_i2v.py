#!/usr/bin/env python3
"""ONE-SHOT remint Part 01 plate 10 → v14 via Flow Veo I2V (Lite OK).

UAT FAIL v13:
  - blue RECTANGULAR scrub/mask around ore (~69–76s)
  - clear flask beside scale (regression)
KEEP: colourless shimmer only (no orange/fire/embers) · motion MAD ·
      Animistry side labels · ore IN brass pan · no flask beside scale.

HARD RULE: if Flow credits empty / generation cannot run → exit BLOCKED.
Do NOT fall back to a local scrub/mask that can leave a visible blue rect.
"""
from __future__ import annotations

import json
import os
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))
import orbit_flow_veo_ui as flow  # noqa: E402
import orbit_gemini_veo as veo  # noqa: E402

PROJ = Path(__file__).resolve().parents[1]
RAW = PROJ / "04_Generated-Clips/part01/raw/v01_fast"
REJECT = PROJ / "04_Generated-Clips/part01/_rejected_uat_v14_plate10"
START = PROJ / "07_Edit-Project/_qa_v14_plate10_prep/p10_start_v14_clean.jpg"
DEST = RAW / "10_rock_not_fire_v01.mp4"
META = PROJ / "07_Edit-Project/part01_remint_plate10_v14_meta.json"
MODEL = os.environ.get("ORBIT_FLOW_VEO_MODEL", "Veo 3.1 - Lite")
PROFILE = Path(
    os.environ.get(
        "ORBIT_FLOW_PROFILE",
        str(Path.home() / ".playwright-hos-flow-profile"),
    )
)

SCENE = (
    "History of Science locked look: premium Animistry-class 3D cartoon workshop, "
    "warm cinematic light. Not photoreal. Silent. No readable text. No Orbit robot. "
    "Continuous gentle camera drift the whole clip — never a still freeze, never Ken Burns. "
    "ONE continuous wide shot. "
    "LEFT: dark rough ore chunk on a COLD metal grate. ONLY a subtle colourless heat shimmer / "
    "air refraction haze rises through the grate — NO orange, NO red, NO yellow glow, NO embers, "
    "NO coals, NO flames, NO fire, NO burning, NO fire plumes, NO orange wisps. Under the grate: "
    "dark cool metal shadow with colourless shimmer only. "
    "Do NOT add any blue overlay, blue rectangle, blue mask, desaturation box, scrub patch, "
    "or processing artifact around the ore or grate — full natural warm workshop colour everywhere. "
    "RIGHT: classic brass balance scale. LEFT hanging pan holds heavy dark ore sitting FLAT "
    "INSIDE the pan metal — ore on the pan floor, pan clearly depressed, chains taut. RIGHT pan empty. "
    "Table around the scale EMPTY of glassware — ZERO clear glass flasks beside the scale, "
    "ZERO bottles on the table near the scale base. "
    "Background shelves: prefer OPAQUE ceramic jars and sealed metal canisters; minimise clear glass. "
    "HARD REJECT: blue rectangular mask/scrub around ore, orange/red fire or ember glow under the grate, "
    "clear flask beside the scale, floating ore, hanging pots, split-screen, text, Orbit, Ken Burns still-push."
)

I2V_PROMPT = (
    "IMAGE-TO-VIDEO of the attached start frame. Keep THIS exact workshop composition, "
    "but REMOVE any clear flask beside the scale and REPLACE any orange under-grate glow with "
    "colourless shimmer only. Preserve ore IN left brass pan. "
    + SCENE
)

T2V_PROMPT = (
    "TEXT-TO-VIDEO scenery only (no character reference). "
    + SCENE
)


def _credit_blocked(text: str) -> str | None:
    low = (text or "").lower()
    needles = [
        # Exact Flow banner from v13 remint fail log:
        "you're out of google flow credits",
        "out of google flow credits",
        "you can wait until they refresh, or upgrade to get more",
        "you can wait until they refresh or upgrade",
        "reached its current generation limit",
        "reached its current quota for video",
        "account has reached its current generation limit",
        "account has reached its current quota for video",
        "need more ai credits",
        "daily limit for this model",
        "upgrade to get more",
    ]
    for n in needles:
        if n in low:
            return n
    return None


def _body(page) -> str:
    try:
        return page.locator("body").inner_text(timeout=4000)[:7000]
    except Exception:
        return ""


def _blocked_exit(meta: dict, msg: str, payload: dict) -> None:
    meta["blocked"] = payload
    META.write_text(json.dumps(meta, indent=2) + "\n")
    print(msg, flush=True)
    raise SystemExit(msg)


def main() -> None:
    if not START.exists():
        raise SystemExit(f"STOP: missing start frame {START}")
    RAW.mkdir(parents=True, exist_ok=True)
    REJECT.mkdir(parents=True, exist_ok=True)
    profile = flow.profile_path(PROFILE)
    print(f"Flow plate10 v14 model={MODEL} profile={profile}", flush=True)
    print(f"  start_frame={START}", flush=True)

    from playwright.sync_api import sync_playwright

    meta: dict = {
        "engine": "flow-ui",
        "model": MODEL,
        "mode": "i2v-v14-plate10",
        "start_frame": str(START),
        "plates": [],
        "blocked": None,
    }
    with sync_playwright() as p:
        ctx, page = flow.launch_context(p, headed=True, profile=profile)
        try:
            page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
            page.wait_for_timeout(3000)
            for _ in range(3):
                flow.dismiss_banners(page)
                page.wait_for_timeout(700)
            logged = False
            for attempt in range(1, 4):
                if flow.looks_logged_in(page):
                    logged = True
                    break
                print(f"  login check miss {attempt}/3 — retrying…", flush=True)
                page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
                page.wait_for_timeout(2500)
                flow.dismiss_banners(page)
            if not logged:
                raise SystemExit(
                    "STOP: Flow not logged in. "
                    "Re-auth: python3 04_Audio/tools/orbit_flow_veo_ui.py --login"
                )

            body0 = _body(page)
            hit0 = _credit_blocked(body0)
            if hit0:
                shot = REJECT / "flow_credits_blocked_home.png"
                page.screenshot(path=str(shot), full_page=True)
                _blocked_exit(
                    meta,
                    "BLOCKED: Google Flow credits empty / generation limit. "
                    f"UI match={hit0!r}. screenshot={shot}",
                    {"stage": "home", "match": hit0, "screenshot": str(shot)},
                )

            tmp = REJECT / "10_rock_not_fire_v14_new.mp4"
            if tmp.exists():
                tmp.unlink()

            info: dict
            print("\n=== I2V 10_rock_not_fire (v14 colourless · no blue mask · no flask) ===", flush=True)
            try:
                info = flow.generate_clip(
                    page,
                    I2V_PROMPT,
                    tmp,
                    model=MODEL,
                    start_frame=START,
                    scenery_only=False,
                    reuse_project=False,
                    attempts=2,
                    timeout_s=700,
                )
            except Exception as i2v_err:
                body = _body(page)
                shot = REJECT / "10_rock_not_fire_v14_i2v_fail.png"
                try:
                    page.screenshot(path=str(shot), full_page=True)
                except Exception:
                    pass
                hit = _credit_blocked(body) or _credit_blocked(str(i2v_err))
                print(f"  I2V failed: {i2v_err}", flush=True)
                if hit:
                    _blocked_exit(
                        meta,
                        "BLOCKED: Google Flow credits empty / I2V cannot run. "
                        f"UI match={hit!r}. err={i2v_err}. screenshot={shot}",
                        {
                            "stage": "i2v",
                            "match": hit,
                            "error": str(i2v_err),
                            "screenshot": str(shot),
                            "body_snip": body[:1500],
                        },
                    )

                # Credits may still exist; try real Flow T2V scenery (NOT local scrub).
                print("\n=== FALLBACK T2V scenery (real Flow only; no scrub) ===", flush=True)
                if tmp.exists():
                    tmp.unlink()
                try:
                    info = flow.generate_clip(
                        page,
                        T2V_PROMPT,
                        tmp,
                        model=MODEL,
                        start_frame=None,
                        scenery_only=True,
                        reuse_project=False,
                        attempts=2,
                        timeout_s=700,
                    )
                    info = {**info, "fallback": "t2v-scenery-after-i2v-fail"}
                except Exception as t2v_err:
                    body2 = _body(page)
                    shot2 = REJECT / "10_rock_not_fire_v14_t2v_fail.png"
                    try:
                        page.screenshot(path=str(shot2), full_page=True)
                    except Exception:
                        pass
                    hit2 = (
                        _credit_blocked(body2)
                        or _credit_blocked(str(t2v_err))
                        or _credit_blocked(body)
                    )
                    if hit2:
                        _blocked_exit(
                            meta,
                            "BLOCKED: Google Flow credits empty / generation cannot run. "
                            f"UI match={hit2!r}. i2v_err={i2v_err}. t2v_err={t2v_err}. "
                            f"screenshot={shot2}",
                            {
                                "stage": "t2v-after-i2v",
                                "match": hit2,
                                "i2v_error": str(i2v_err),
                                "t2v_error": str(t2v_err),
                                "screenshot": str(shot2),
                                "body_snip": body2[:1500],
                            },
                        )
                    _blocked_exit(
                        meta,
                        "BLOCKED: Flow Veo I2V/T2V failed (no local scrub fallback). "
                        f"i2v_err={i2v_err}. t2v_err={t2v_err}. screenshot={shot2}",
                        {
                            "stage": "t2v-after-i2v",
                            "match": None,
                            "i2v_error": str(i2v_err),
                            "t2v_error": str(t2v_err),
                            "screenshot": str(shot2),
                            "body_snip": body2[:1500],
                        },
                    )

            veo.strip_audio(tmp)
            if not tmp.exists() or tmp.stat().st_size < 400_000:
                raise SystemExit("STOP: plate10 download missing/small")
            if DEST.exists():
                prev = REJECT / "10_rock_not_fire_v01_prev_from_v13.mp4"
                if prev.exists():
                    prev.unlink()
                shutil.move(str(DEST), str(prev))
                print(f"  archived previous → {prev.name}", flush=True)
            shutil.move(str(tmp), str(DEST))
            meta["plates"].append(
                {
                    "id": "10_rock_not_fire",
                    "status": "ok",
                    "out": str(DEST),
                    "bytes": DEST.stat().st_size,
                    **info,
                }
            )
            META.write_text(json.dumps(meta, indent=2) + "\n")
            print(f"SAVED {DEST} bytes={DEST.stat().st_size}", flush=True)
            print(f"info={info}", flush=True)
        finally:
            ctx.close()
    print("OK plate10 v14 remint finished", flush=True)


if __name__ == "__main__":
    main()
