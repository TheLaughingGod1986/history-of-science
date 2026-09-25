#!/usr/bin/env python3
"""Part 03 Flow Veo 3.1 Fast partial remint v09 — plate 10_city_plan_lots ONLY.

Showrunner PART03_V09_SCRUB_CITY_PLAN_HOUSE_BLOCKS.md (parent v08 sha 487dc2b8…):
  - REMINT ONLY: 10_city_plan_lots (~67–75s · Ben clock ~68–69)
  - Picture: flat postcard plan (grid INK only, no 3D) OR papers only on desk
  - HARD REJECT: glowing yellow house-blocks, 3D/black house icons, map pins,
    model-town sprawl, central-table diorama
  - KEEP locked from v08: 08_property_waves, EMPTY CHAIR, 03 swirl, 05 Explorer,
    Karlsruhe blank, VO / PLATE_ORDER
  - Prefer I2V. Veo Fast. Create dies → STOP (no Ken Burns).
  - Auth: benoats@googlemail.com on /u/1/. No P01/P02 remint. No P04.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))

import orbit_flow_veo_ui as flow  # noqa: E402
import orbit_gemini_veo as veo  # noqa: E402

flow.FLOW_HOME = os.environ.get("ORBIT_FLOW_HOME", "https://flow.google.com/u/1/")

PROJ = Path(__file__).resolve().parents[1]
PLATES_JSON = PROJ / "07_Edit-Project/parts/part-03_plates_v01.json"
RAW = PROJ / "04_Generated-Clips/part03/raw/v09_fast"
META = PROJ / "07_Edit-Project/part03_mint_flow_v09_meta.json"
HARVEST = Path(__file__).resolve().parent / "_harvest_newest_gallery_v01.py"
STILLS = PROJ / "04_Generated-Clips/part03/refs/v09_stills"
MODEL = os.environ.get("ORBIT_FLOW_VEO_MODEL", "Veo 3.1 - Fast")
PROFILE = Path(
    os.environ.get(
        "ORBIT_FLOW_PROFILE",
        str(Path.home() / ".playwright-hos-flow-profile"),
    )
)

STYLE = (
    "Animistry-class stylised 3D cartoon (NOT photoreal). "
    "Same Karlsruhe congress-hall DNA as plate-01 (honey oak panels, arched "
    "windows, wooden benches, cream pamphlets). Continuous real camera "
    "drift + prop motion. Silent. No Orbit. No Ken Burns still. No people / "
    "no Explorer on this plate."
)

REJECT = (
    "HARD REJECT: glowing yellow house-blocks; 3D house icons; black house "
    "silhouettes standing on the board; map pins; teardrop location pins as "
    "3D toys; miniature buildings; Lego-like blocks; model-town sprawl on desk "
    "or floor; central-table town diorama; any raised 3D markers on the plan; "
    "layout reset; courtroom redesign that dumps Karlsruhe hall DNA; Orbit; "
    "Ken Burns only; photoreal."
)

# Option 1 — flat ink postcard (preferred; VO-literal "city plan")
V09_PROMPT_10_FLAT = (
    "IMAGE-TO-VIDEO from the attached start frame. KEEP this EXACT Karlsruhe "
    "congress-hall DNA from the still (honey oak panels, arched windows, wooden "
    "benches/pews, cream pamphlets — do NOT redesign the room). "
    "HERO on an EXISTING hall desk/bench ONLY: a TINY palm-sized FLAT postcard "
    "city-plan of matter — completely 2D sheet. Printed street GRID as thin INK "
    "lines only. Vacant lots as FLAT ink/paint washes only (soft non-object glow "
    "on a wash mark OK if it never reads as a building). "
    "NO house shapes. NO pins. NO 3D icons. NO glowing house-blocks. "
    "Continuous gentle camera drift toward the flat postcard; hall stays in frame. "
    "Silent. No readable street names. No people. No Explorer. No Orbit. "
    + REJECT
)

# Option 2 — papers only (fallback start / T2V alt)
V09_PROMPT_10_PAPERS = (
    "IMAGE-TO-VIDEO from the attached start frame. KEEP this EXACT Karlsruhe "
    "congress-hall DNA (honey oak, arched windows, wooden benches). "
    "On an EXISTING hall desk ONLY: a tidy stack of blank cream pamphlets/papers. "
    "NO city-plan board. NO house icons. NO map pins. NO model-town. "
    "Meaning of 'city plan for matter' stays on VO — picture is papers on the desk. "
    "Continuous soft camera drift. Silent. No people. No Explorer. No Orbit. "
    + REJECT
)

REQUIRED_FLOW_EMAIL = "benoats@googlemail.com"
ALLOWED_FLOW_EMAILS = {REQUIRED_FLOW_EMAIL, "benoats@gmail.com"}
FORBIDDEN_FLOW_EMAIL = "benoats86@gmail.com"

CREATE_DIE_MARKERS = (
    "out of google flow credits",
    "reached your credit or daily limit",
    "you're out of google flow credits",
    "create failed",
    "generation failed",
    "could not create",
    "not been charged",
)

DEFAULT_ONLY = ("10_city_plan_lots",)
ALLOWED_ONLY = set(DEFAULT_ONLY)

START_FRAMES = {
    # Prefer desk-scrubbed FAIL frames (real Karlsruhe desk DNA, houses painted out)
    "10_desk_papers": STILLS / "10_desk_scrub_papers_i2v.jpg",
    "10_desk_flat": STILLS / "10_desk_scrub_flat_i2v.jpg",
    "10_desk_flat_rough": STILLS / "10_desk_scrub_flat_from_rough.jpg",
    "10_desk_flat_benfail": STILLS / "10_desk_scrub_flat_benfail.jpg",
    # Hall-compose alts (no FAIL DNA)
    "10_flat": STILLS / "10_flat_ink_grid_i2v.jpg",
    "10_flat_alt": STILLS / "10_flat_ink_grid_alt.jpg",
    "10_papers": STILLS / "10_papers_only_i2v.jpg",
    "10_papers_alt": STILLS / "10_papers_only_alt.jpg",
    "10_hall_fallback": STILLS / "10_hall_dna_fallback.jpg",
}


def dest_for(plate_id: str) -> Path:
    return RAW / f"{plate_id}_v09.mp4"


def pick_google_account(page) -> None:
    url = page.url or ""
    if "accounts.google.com" not in url:
        return
    for needle in (REQUIRED_FLOW_EMAIL, "benoats@gmail.com"):
        loc = page.get_by_text(needle, exact=False)
        if loc.count():
            print(f"  account chooser → {needle}", flush=True)
            loc.first.click(timeout=8000)
            page.wait_for_timeout(7000)
            return
    raise SystemExit(
        f"BLOCKED_AUTH: account chooser open but {REQUIRED_FLOW_EMAIL} not listed. "
        "Ben must sign Mini Flow himself (never paste passwords)."
    )


def require_flow_account(page) -> str:
    try:
        labels = page.eval_on_selector_all(
            "button, a, [role=button]",
            "els => els.map(e => (e.getAttribute('aria-label') || e.innerText || '').trim())"
            ".filter(Boolean)",
        )
    except Exception as exc:
        raise SystemExit(
            f"BLOCKED_AUTH: could not read Flow account chrome ({exc})."
        ) from exc
    blob = "\n".join(labels)
    emails = {
        e.lower()
        for e in re.findall(r"[A-Za-z0-9._%+-]+@(?:gmail|googlemail)\.com", blob, flags=re.I)
    }
    active = None
    m = re.search(
        r"Google Account:[^\n\(]*\(([^)]+@(?:gmail|googlemail)\.com)\)",
        blob,
        re.I,
    )
    if m:
        active = m.group(1).lower()
    elif FORBIDDEN_FLOW_EMAIL in emails:
        active = FORBIDDEN_FLOW_EMAIL
    elif emails & ALLOWED_FLOW_EMAILS:
        active = sorted(emails & ALLOWED_FLOW_EMAILS)[0]
    elif emails:
        active = sorted(emails)[0]

    print(f"  Flow account probe emails={sorted(emails)} active={active}", flush=True)
    print(f"  page.url={page.url}", flush=True)
    if not active:
        raise SystemExit("BLOCKED_AUTH: signed-in Google email not visible on Flow.")
    if active == FORBIDDEN_FLOW_EMAIL or "benoats86" in active:
        raise SystemExit(
            f"BLOCKED_AUTH: Mini Flow is signed in as {active}. "
            f"Need exactly {REQUIRED_FLOW_EMAIL} on /u/1/. No mint."
        )
    if active not in ALLOWED_FLOW_EMAILS:
        raise SystemExit(
            f"BLOCKED_AUTH: unexpected Flow account {active}. Need {REQUIRED_FLOW_EMAIL}."
        )
    return active


def probe_credits(page) -> str:
    try:
        body = (page.inner_text("body") or "")
    except Exception as exc:
        return f"credits_probe_error:{exc}"
    low = body.lower()
    for marker in CREATE_DIE_MARKERS:
        if marker in low:
            raise SystemExit(
                f"STOP BLOCKED: Create/credits death visible BEFORE mint ({marker}). "
                "No Ken Burns. No Omni Flash substitute."
            )
    hits = []
    for pat in (
        r"\d[\d,]*\+?\s*credits?",
        r"credits?\s*[:=]?\s*\d[\d,]*",
        r"ultra",
        r"daily limit",
    ):
        for m in re.finditer(pat, body, flags=re.I):
            hits.append(m.group(0).strip()[:80])
            if len(hits) >= 8:
                break
        if len(hits) >= 8:
            break
    blob = " | ".join(dict.fromkeys(hits)) if hits else "no-credit-string-visible"
    print(f"  credits probe: {blob}", flush=True)
    return blob


def looks_like_create_death(exc: BaseException, page) -> str | None:
    msg = str(exc).lower()
    for marker in CREATE_DIE_MARKERS:
        if marker in msg:
            return marker
    try:
        body = (page.inner_text("body") or "").lower()
    except Exception:
        body = ""
    for marker in CREATE_DIE_MARKERS:
        if marker in body:
            return marker
    return None


def safe_close(ctx) -> None:
    if ctx is None:
        return
    try:
        ctx.close()
    except Exception:
        pass


def open_flow(p, *, profile: Path):
    last_err = "not started"
    for attempt in range(1, 4):
        ctx, page = flow.launch_context(p, headed=True, profile=profile)
        try:
            page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
            page.wait_for_timeout(3500)
            pick_google_account(page)
            flow.dismiss_banners(page)
            page.wait_for_timeout(1500)
            flow.dismiss_banners(page)
            if not flow.looks_logged_in(page):
                flow.settle_after_nav(page, wait_ms=2000)
                flow.dismiss_banners(page)
                page.wait_for_timeout(2000)
                if not flow.looks_logged_in(page):
                    page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
                    page.wait_for_timeout(3500)
                    pick_google_account(page)
                    flow.dismiss_banners(page)
                    page.wait_for_timeout(1500)
            if not flow.looks_logged_in(page):
                try:
                    active_probe = require_flow_account(page)
                    print(
                        f"  looks_logged_in=False but account chrome OK ({active_probe}) "
                        f"attempt={attempt}",
                        flush=True,
                    )
                    credits = probe_credits(page)
                    print(
                        f"  AUTH OK minting as {active_probe} via {flow.FLOW_HOME} "
                        f"credits={credits}",
                        flush=True,
                    )
                    return ctx, page, active_probe
                except SystemExit as exc:
                    last_err = str(exc)
                    safe_close(ctx)
                    print(f"  open_flow retry {attempt}/3: {last_err}", flush=True)
                    time.sleep(2)
                    continue
            active = require_flow_account(page)
            credits = probe_credits(page)
            print(
                f"  AUTH OK minting as {active} via {flow.FLOW_HOME} credits={credits}",
                flush=True,
            )
            return ctx, page, active
        except SystemExit:
            safe_close(ctx)
            raise
        except Exception as exc:
            last_err = str(exc)
            safe_close(ctx)
            print(f"  open_flow exception retry {attempt}/3: {last_err}", flush=True)
            time.sleep(2)
    raise SystemExit(
        f"BLOCKED_AUTH: Flow not logged in after retries ({last_err}). "
        "Do not Ken-Burns. Ben must sign Mini as benoats@googlemail.com on /u/1/."
    )


def run_harvest(dest: Path, project_url: str, *, before_thumbs: int = -1) -> None:
    project_url = (project_url or "").split("?")[0].rstrip("/")
    if "flow.google.com" not in project_url or "/project/" not in project_url:
        raise SystemExit(
            f"STOP: refuse harvest — not a Flow project URL: {project_url!r}"
        )
    settle = int(os.environ.get("HOS_FLOW_HARVEST_SETTLE_S", "90"))
    wait_s = int(os.environ.get("HOS_FLOW_HARVEST_WAIT_S", "360"))
    print(f"  settle {settle}s then harvest wait_s={wait_s}", flush=True)
    time.sleep(settle)
    env = dict(os.environ)
    env["ORBIT_FLOW_HOME"] = flow.FLOW_HOME
    env["ORBIT_FLOW_PROFILE"] = str(PROFILE)
    env.pop("HOS_FLOW_SKIP_I2V", None)
    cmd = [
        sys.executable, "-u", str(HARVEST),
        "--out", str(dest),
        "--project", project_url,
        "--wait-s", str(wait_s),
        "--before-thumbs", str(before_thumbs),
    ]
    print(f"  spawn harvest: {' '.join(cmd)}", flush=True)
    subprocess.check_call(cmd, env=env)


def probe_dur(path: Path) -> float:
    return float(
        subprocess.check_output(
            [
                "ffprobe", "-v", "error", "-show_entries", "format=duration",
                "-of", "default=nw=1:nk=1", str(path),
            ],
            text=True,
        ).strip()
    )


def resolve_start_frame(pid: str) -> Path:
    if pid != "10_city_plan_lots":
        raise SystemExit(f"STOP: unexpected plate {pid}")
    preferred = [
        START_FRAMES["10_desk_papers"],
        START_FRAMES["10_desk_flat"],
        START_FRAMES["10_desk_flat_rough"],
        START_FRAMES["10_desk_flat_benfail"],
        START_FRAMES["10_flat"],
        START_FRAMES["10_flat_alt"],
        START_FRAMES["10_papers"],
        START_FRAMES["10_papers_alt"],
        START_FRAMES["10_hall_fallback"],
    ]
    for path in preferred:
        if path.exists() and path.stat().st_size > 20_000:
            print(f"  I2V start_frame={path}", flush=True)
            return path
    raise SystemExit(f"STOP: no usable I2V start frame for {pid}")


def prompt_for(start: Path) -> str:
    name = start.name.lower()
    if "papers" in name:
        return f"{V09_PROMPT_10_PAPERS} {STYLE}"
    return f"{V09_PROMPT_10_FLAT} {STYLE}"


def t2v_prompt(*, papers: bool = False) -> str:
    if papers:
        return (
            "Inside the SAME Karlsruhe congress hall DNA: warm honey oak panels, "
            "tall arched windows, wooden benches. On one existing desk ONLY a tidy "
            "stack of blank cream pamphlets/papers. NO city-plan board. NO house "
            "icons. NO map pins. NO glowing yellow house-blocks. NO model-town. "
            "Continuous soft camera drift. Silent. No people. No Orbit. "
            + STYLE + " " + REJECT
        )
    return (
        "Inside the SAME Karlsruhe congress hall DNA: warm honey oak panels, "
        "tall arched windows, wooden benches, cream pamphlets. On one existing "
        "desk ONLY a tiny palm-sized completely FLAT postcard city-plan — street "
        "grid as thin INK lines only, vacant lots as flat ink washes only. "
        "NO house shapes. NO 3D icons. NO map pins. NO glowing yellow house-blocks. "
        "Camera gently drifts toward the flat postcard. Continuous motion. Silent. "
        "No people. No Orbit. "
        + STYLE + " " + REJECT
    )


def alt_starts_for(start: Path) -> list[Path]:
    keys = [
        "10_desk_flat",
        "10_desk_flat_rough",
        "10_flat",
        "10_flat_alt",
        "10_papers",
        "10_papers_alt",
        "10_hall_fallback",
        "10_desk_papers",
    ]
    out: list[Path] = []
    for key in keys:
        path = START_FRAMES[key]
        if path.exists() and path.resolve() != start.resolve():
            out.append(path)
    return out


def _truthy(name: str) -> bool:
    return os.environ.get(name, "").strip().lower() in {"1", "true", "yes", "on"}


def main() -> None:
    if _truthy("HOS_FLOW_SKIP_I2V"):
        print(
            "  WARN: unsetting HOS_FLOW_SKIP_I2V — v09 prefers flat-ink I2V",
            flush=True,
        )
        os.environ.pop("HOS_FLOW_SKIP_I2V", None)

    if _truthy("HOS_FLOW_T2V_ONLY") and _truthy("HOS_FLOW_I2V_ONLY"):
        print(
            "  WARN: HOS_FLOW_T2V_ONLY wins — unsetting HOS_FLOW_I2V_ONLY",
            flush=True,
        )
        os.environ.pop("HOS_FLOW_I2V_ONLY", None)

    print(
        f"  env T2V_ONLY={os.environ.get('HOS_FLOW_T2V_ONLY')!r} "
        f"I2V_ONLY={os.environ.get('HOS_FLOW_I2V_ONLY')!r} "
        f"FORCE_REMINT={os.environ.get('HOS_FLOW_FORCE_REMINT')!r}",
        flush=True,
    )

    argv = [a for a in sys.argv[1:] if not a.startswith("-")]
    only = set(argv) if argv else set(DEFAULT_ONLY)
    bad = only - ALLOWED_ONLY
    if bad:
        raise SystemExit(f"STOP: refuse remint via v09: {sorted(bad)}")
    if not only:
        raise SystemExit("STOP: empty only set")

    plates = json.loads(PLATES_JSON.read_text())["plates"]
    order = [pid for pid in DEFAULT_ONLY if pid in only]
    for pid in sorted(only):
        if pid not in order:
            order.append(pid)
    plates = [p for p in plates if p["id"] in only]
    plates.sort(key=lambda p: order.index(p["id"]))
    if not plates:
        raise SystemExit(f"STOP: no plates matched only={sorted(only)}")

    RAW.mkdir(parents=True, exist_ok=True)
    meta: dict = {
        "engine": "flow-ui",
        "model": MODEL,
        "flow_home": flow.FLOW_HOME,
        "raw": str(RAW),
        "continuity": "scrub_city_plan_house_blocks_v09",
        "parent_v08_sha_prefix": "487dc2b8",
        "only": sorted(only),
        "keep_08_property_waves_v08": True,
        "keep_empty_chair_v04": True,
        "keep_explorer_v05": True,
        "keep_03_method_pamphlet_v07": True,
        "plates": [],
    }
    if META.exists():
        try:
            meta = json.loads(META.read_text())
            meta["only"] = sorted(only)
        except Exception:
            pass
    by_id = {p["id"]: p for p in meta.get("plates", []) if "id" in p}

    profile = flow.profile_path(PROFILE)
    print(
        f"Flow profile={profile} home={flow.FLOW_HOME} model={MODEL} "
        f"partial remint only={order} I2V preferred (flat ink / papers)",
        flush=True,
    )

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        ctx, page, active = open_flow(p, profile=profile)
        meta["flow_account"] = active
        meta["flow_home"] = flow.FLOW_HOME
        try:
            for i, plate in enumerate(plates):
                pid = plate["id"]
                dest = dest_for(pid)
                start = resolve_start_frame(pid)
                force = _truthy("HOS_FLOW_FORCE_REMINT")
                if veo.already_done(dest, min_bytes=400_000) and not force:
                    try:
                        dur = probe_dur(dest)
                    except Exception:
                        dur = 0.0
                    if 5.0 <= dur <= 40.0:
                        print(f"  skip {dest.name} dur={dur:.2f}", flush=True)
                        by_id[pid] = {
                            "id": pid,
                            "status": by_id.get(pid, {}).get("status", "exists"),
                            "out": str(dest),
                            "duration": dur,
                        }
                        continue
                    print(f"  re-mint bad existing {dest.name} dur={dur:.2f}", flush=True)
                    dest.unlink(missing_ok=True)
                elif dest.exists() and force:
                    print(f"  force remint — removing {dest.name}", flush=True)
                    dest.unlink(missing_ok=True)

                prompt = prompt_for(start)
                kind = "I2V"
                force_t2v = _truthy("HOS_FLOW_T2V_ONLY")
                print(
                    f"\n=== Fast {'T2V' if force_t2v else kind} {pid} "
                    f"({i+1}/{len(plates)}) force_t2v={force_t2v} ===",
                    flush=True,
                )
                if not force_t2v:
                    print(f"  start_frame={start}", flush=True)
                else:
                    print("  start_frame: (none — T2V scenery Fast)", flush=True)

                try:
                    _ = page.url
                except Exception:
                    print("  page dead — relaunching", flush=True)
                    safe_close(ctx)
                    ctx, page, active = open_flow(p, profile=profile)

                tmp = dest.with_suffix(".tmp.mp4")
                tmp.unlink(missing_ok=True)
                info = None
                i2v_err: Exception | None = None
                if force_t2v:
                    print(
                        "  HOS_FLOW_T2V_ONLY — scenery T2V Fast (no Ken Burns)",
                        flush=True,
                    )
                    try:
                        info = flow.generate_clip(
                            page,
                            t2v_prompt(papers=False),
                            tmp,
                            model=MODEL,
                            start_frame=None,
                            scenery_only=True,
                            reuse_project=False,
                            attempts=2,
                            timeout_s=240,
                        )
                        kind = "T2V_forced"
                    except Exception as e:
                        i2v_err = e
                        info = None
                else:
                    try:
                        info = flow.generate_clip(
                            page,
                            prompt,
                            tmp,
                            model=MODEL,
                            start_frame=start,
                            scenery_only=False,
                            reuse_project=False,
                            attempts=1,
                            timeout_s=240,
                        )
                    except Exception as e:
                        i2v_err = e
                        info = None

                if info is None and start is not None and not force_t2v:
                    elow = str(i2v_err or "").lower()
                    attach_fail = any(
                        x in elow
                        for x in (
                            "add to prompt",
                            "did not attach",
                            "upload",
                            "facebook",
                            "start frame",
                        )
                    )
                    if attach_fail or i2v_err is not None:
                        for alt in alt_starts_for(start):
                            if info is not None:
                                break
                            print(
                                f"  I2V attach failed ({i2v_err}); retry alt still {alt.name}",
                                flush=True,
                            )
                            safe_close(ctx)
                            ctx, page, active = open_flow(p, profile=profile)
                            try:
                                info = flow.generate_clip(
                                    page,
                                    prompt_for(alt),
                                    tmp,
                                    model=MODEL,
                                    start_frame=alt,
                                    scenery_only=True,
                                    reuse_project=False,
                                    attempts=2,
                                    timeout_s=180,
                                )
                                start = alt
                                kind = f"I2V_alt_{alt.stem}"
                            except Exception as e_alt:
                                i2v_err = e_alt
                                info = None
                        if info is None:
                            if _truthy("HOS_FLOW_I2V_ONLY"):
                                raise SystemExit(
                                    f"STOP: I2V-only mode — refuse T2V fallback after "
                                    f"attach failure ({i2v_err})"
                                ) from i2v_err
                            print(
                                f"  I2V preferred failed ({i2v_err}); "
                                "falling back to scenery T2V Fast (no Ken Burns)",
                                flush=True,
                            )
                            safe_close(ctx)
                            ctx, page, active = open_flow(p, profile=profile)
                            try:
                                info = flow.generate_clip(
                                    page,
                                    t2v_prompt(papers=False),
                                    tmp,
                                    model=MODEL,
                                    start_frame=None,
                                    scenery_only=True,
                                    reuse_project=False,
                                    attempts=2,
                                    timeout_s=180,
                                )
                                info["i2v_fallback_t2v"] = True
                                info["i2v_error"] = str(i2v_err)[:300]
                                kind = "T2V_fallback"
                            except Exception as e2:
                                i2v_err = e2
                                info = None

                if info is None:
                    e = i2v_err or RuntimeError("unknown Flow failure")
                    death = looks_like_create_death(e, page)
                    by_id[pid] = {
                        "id": pid,
                        "status": "fail",
                        "error": str(e)[:500],
                        "create_death": death,
                    }
                    meta["plates"] = list(by_id.values())
                    META.write_text(json.dumps(meta, indent=2))
                    if death:
                        raise SystemExit(
                            f"STOP BLOCKED: Create died on {pid} ({death}). "
                            "No Ken Burns. No Omni Flash substitute."
                        ) from e
                    raise SystemExit(f"STOP: Flow failed on {pid}: {e}") from e

                if info.get("needs_gallery_harvest"):
                    candidates = [
                        info.get("project_url") or "",
                        info.get("url") or "",
                        page.url or "",
                    ]
                    project_url = ""
                    for cand in candidates:
                        cand = (cand or "").split("?")[0].rstrip("/")
                        if "flow.google.com" in cand and "/project/" not in cand:
                            continue
                        if "flow.google.com" in cand and "/project/" in cand:
                            project_url = cand
                            break
                    if not project_url:
                        raise SystemExit(
                            f"STOP: no Flow project URL for harvest on {pid}; "
                            f"candidates={candidates!r}"
                        )
                    print(
                        f"  closing mint browser for harvest… project={project_url}",
                        flush=True,
                    )
                    safe_close(ctx)
                    ctx = None
                    page = None
                    run_harvest(tmp, project_url, before_thumbs=-1)
                    ctx, page, active = open_flow(p, profile=profile)
                    info["media_id"] = (
                        f"gallery-harvest:{tmp.stat().st_size if tmp.exists() else 0}"
                    )
                    info["bytes"] = tmp.stat().st_size if tmp.exists() else 0

                if not tmp.exists() or tmp.stat().st_size < 400_000:
                    raise SystemExit(f"STOP: download missing/small {tmp}")
                veo.strip_audio(tmp)
                try:
                    dur = probe_dur(tmp)
                except Exception as e:
                    raise SystemExit(f"STOP: unreadable download {tmp}: {e}") from e
                if dur < 5.0 or dur > 40.0:
                    badp = RAW / f"{pid}_bad_dur_{dur:.1f}.mp4"
                    shutil.move(str(tmp), str(badp))
                    raise SystemExit(f"STOP: bad duration {badp} dur={dur:.2f}")
                if dest.exists():
                    dest.unlink()
                shutil.move(str(tmp), str(dest))
                by_id[pid] = {
                    "id": pid,
                    "status": "ok",
                    "out": str(dest),
                    "duration": dur,
                    "kind": kind,
                    "start_frame": str(start),
                    **{k: v for k, v in info.items() if k != "needs_gallery_harvest"},
                }
                meta["plates"] = list(by_id.values())
                META.write_text(json.dumps(meta, indent=2))
                print(
                    f"  SAVED {dest.name} bytes={dest.stat().st_size} dur={dur:.2f}",
                    flush=True,
                )
        finally:
            safe_close(ctx)

    ok = sum(
        1
        for p in by_id.values()
        if p.get("status") in {"ok", "exists"} and p["id"] in only
    )
    want = len(only)
    print(f"OK part 03 Flow mint v09 finished ok={ok} want={want}", flush=True)
    if ok < want:
        sys.exit(2)


if __name__ == "__main__":
    main()
