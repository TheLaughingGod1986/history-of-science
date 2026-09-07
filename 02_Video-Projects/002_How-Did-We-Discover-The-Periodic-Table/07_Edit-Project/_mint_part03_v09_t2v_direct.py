#!/usr/bin/env python3
"""Direct T2V remint for Part 03 v09 plate 10 — lock Video + Veo Fast explicitly.

Bypasses flaky configure_veo_settings when Flow Image/Video are role=radio and
session is polluted by Nano Banana image projects.
"""
from __future__ import annotations

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
DEST = PROJ / "04_Generated-Clips/part03/raw/v09_fast/10_city_plan_lots_v09.mp4"
HARVEST = Path(__file__).resolve().parent / "_harvest_newest_gallery_v01.py"
PROFILE = Path(
    os.environ.get(
        "ORBIT_FLOW_PROFILE",
        str(Path.home() / ".playwright-hos-flow-profile"),
    )
)
MODEL = "Veo 3.1 - Fast"

PROMPT = (
    "Inside the SAME Karlsruhe congress hall DNA: warm honey oak panels, "
    "tall arched windows, wooden benches. On one EXISTING hall desk ONLY a "
    "tidy stack of blank cream pamphlets and papers. NO city-plan board. "
    "NO postcard map. NO house shapes. NO 3D icons. NO map pins. "
    "NO glowing yellow house-blocks. NO black house silhouettes. "
    "NO miniature buildings. NO model-town sprawl. NO central-table diorama. "
    "Camera gently drifts across the papers on the desk; hall stays in frame. "
    "Continuous soft motion. Silent. No people. No Explorer. No Orbit. "
    "Animistry-class stylised 3D cartoon (NOT photoreal)."
)


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


def lock_video_veo(page) -> None:
    flow.dismiss_banners(page)
    # Open settings pill (Video · … or Nano Banana)
    box = page.evaluate(
        """() => {
          for (const b of document.querySelectorAll('button')) {
            const t = (b.innerText || '');
            if (/Nano Banana|Video ·|Omni|Veo 3|crop_16_9/.test(t)) {
              const r = b.getBoundingClientRect();
              if (r.width > 40 && r.height > 16)
                return {x:r.x+r.width/2, y:r.y+r.height/2, t:t.trim().slice(0,80)};
            }
          }
          return null;
        }"""
    )
    if not box:
        raise SystemExit("STOP: settings pill not found")
    print(f"  pill={box['t']!r}", flush=True)
    page.mouse.click(box["x"], box["y"])
    page.wait_for_timeout(1000)

    # Click Video radio
    video = page.evaluate(
        """() => {
          for (const b of document.querySelectorAll('button,[role=radio],[role=tab]')) {
            const t = (b.innerText || '').replace(/\\n/g,' ').trim();
            if (!/\\bVideo\\b/i.test(t) || /Video ·/.test(t)) continue;
            const r = b.getBoundingClientRect();
            if (r.width > 40 && r.height > 16)
              return {x:r.x+r.width/2, y:r.y+r.height/2, t:t.slice(0,40)};
          }
          return null;
        }"""
    )
    if video:
        print(f"  click Video radio {video}", flush=True)
        page.mouse.click(video["x"], video["y"])
        page.wait_for_timeout(900)

    # Open model dropdown (Omni / Veo)
    dd = page.evaluate(
        """() => {
          for (const b of document.querySelectorAll('button')) {
            const t = (b.innerText || '').replace(/\\n/g,' ');
            if (!/arrow_drop_down/.test(t)) continue;
            if (!/Omni|Veo 3|Flash/i.test(t)) continue;
            const r = b.getBoundingClientRect();
            if (r.width > 60 && r.height > 16)
              return {x:r.x+r.width/2, y:r.y+r.height/2, t:t.trim().slice(0,60)};
          }
          return null;
        }"""
    )
    if not dd:
        raise SystemExit("STOP: model dropdown not found")
    print(f"  dropdown={dd['t']!r}", flush=True)
    if MODEL not in dd["t"]:
        page.mouse.click(dd["x"], dd["y"])
        page.wait_for_timeout(800)
        clicked = page.evaluate(
            """(model) => {
              const needle = String(model||'').toLowerCase();
              for (const el of document.querySelectorAll('[role=menuitem],button')) {
                const t = (el.innerText||'').trim().replace(/\\n/g,' ');
                if (t.length < 80 && t.toLowerCase().includes(needle)) {
                  const r = el.getBoundingClientRect();
                  if (r.width>20 && r.height>12) {
                    el.click();
                    return t;
                  }
                }
              }
              return null;
            }""",
            MODEL,
        )
        if not clicked:
            raise SystemExit(f"STOP: could not pick {MODEL}")
        print(f"  selected {clicked!r}", flush=True)
        page.wait_for_timeout(500)
    else:
        print(f"  already on {MODEL}", flush=True)

    # Prefer 16:9 x1 if visible
    for kind in ("crop_16_9", "x1"):
        page.evaluate(
            """(kind) => {
              for (const b of document.querySelectorAll('button')) {
                const t=(b.innerText||'');
                if (kind==='crop_16_9' && !/crop_16_9|16:9/.test(t)) continue;
                if (kind==='x1' && t.trim()!=='x1') continue;
                const r=b.getBoundingClientRect();
                if (r.width>8 && r.height>8) { b.click(); return true; }
              }
              return false;
            }""",
            kind,
        )
    page.keyboard.press("Escape")
    page.wait_for_timeout(600)
    print("  Video+Veo lock done", flush=True)


def main() -> None:
    DEST.parent.mkdir(parents=True, exist_ok=True)
    DEST.unlink(missing_ok=True)
    tmp = DEST.with_suffix(".tmp.mp4")
    tmp.unlink(missing_ok=True)

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        ctx, page = flow.launch_context(
            p, headed=True, profile=flow.profile_path(PROFILE)
        )
        try:
            page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
            page.wait_for_timeout(3500)
            flow.dismiss_banners(page)
            if "flow.google.com" not in (page.url or ""):
                print(f"  WARN not on Flow ({page.url}) — re-goto", flush=True)
                page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
                page.wait_for_timeout(4000)
                flow.dismiss_banners(page)
            if "flow.google.com" not in (page.url or ""):
                raise SystemExit(f"STOP: not on Flow after goto: {page.url}")
            # Prefer a brand-new project so we are not stuck in Image mode
            for label in ("New project", "Create project"):
                loc = page.get_by_role("button", name=re.compile(label, re.I))
                if loc.count() and loc.first.is_visible():
                    print(f"  {label}", flush=True)
                    loc.first.click()
                    page.wait_for_timeout(3500)
                    break
            flow.dismiss_banners(page)
            if "flow.google.com" not in (page.url or "") or "/project/" not in (page.url or ""):
                # Fallback: open a known blank-ish path
                print(f"  WARN unexpected url after New project: {page.url}", flush=True)
                page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
                page.wait_for_timeout(3000)
                flow.dismiss_banners(page)
                loc = page.get_by_role("button", name=re.compile("New project", re.I))
                if loc.count():
                    loc.first.click()
                    page.wait_for_timeout(3500)
            if "flow.google.com" not in (page.url or ""):
                raise SystemExit(f"STOP: left Flow: {page.url}")
            print(f"  project url={page.url}", flush=True)
            lock_video_veo(page)

            flow.set_prompt(page, PROMPT)
            print("  submitting Create…", flush=True)
            flow.submit_create(page)
            page.wait_for_timeout(1500)
            try:
                flow.confirm_generation_spend(page)
            except Exception as e:
                print(f"  confirm spend: {e}", flush=True)

            # Wait a bit then harvest
            project_url = (page.url or "").split("?")[0].rstrip("/")
            if "/project/" not in project_url:
                raise SystemExit(f"STOP: no project url {project_url}")
            print(f"  closing for harvest {project_url}", flush=True)
            try:
                ctx.close()
            except Exception:
                pass
            ctx = None

            settle = int(os.environ.get("HOS_FLOW_HARVEST_SETTLE_S", "90"))
            wait_s = int(os.environ.get("HOS_FLOW_HARVEST_WAIT_S", "480"))
            print(f"  settle {settle}s harvest wait_s={wait_s}", flush=True)
            time.sleep(settle)
            env = dict(os.environ)
            env["ORBIT_FLOW_HOME"] = flow.FLOW_HOME
            env["ORBIT_FLOW_PROFILE"] = str(PROFILE)
            cmd = [
                sys.executable, "-u", str(HARVEST),
                "--out", str(tmp),
                "--project", project_url,
                "--wait-s", str(wait_s),
                "--before-thumbs", "-1",
            ]
            print("  spawn", " ".join(cmd), flush=True)
            try:
                subprocess.check_call(cmd, env=env)
            except subprocess.CalledProcessError:
                print("  harvest script failed — trying force download", flush=True)
                force = Path(__file__).resolve().parent / "_harvest_part03_v09_force_download.py"
                subprocess.check_call(
                    [
                        sys.executable, "-u", str(force),
                        project_url, "--dest", str(DEST),
                    ],
                    env=env,
                )
                if DEST.exists() and DEST.stat().st_size > 400_000:
                    print(f"OK force {DEST} bytes={DEST.stat().st_size}", flush=True)
                    return
                raise SystemExit("STOP: force download also failed")

            if not tmp.exists() or tmp.stat().st_size < 400_000:
                raise SystemExit(f"STOP: download missing/small {tmp}")
            raw = tmp.read_bytes()
            if raw[:3] == b"\xff\xd8\xff" or b"ftyp" not in raw[:64]:
                raise SystemExit(f"STOP: not an mp4 ({raw[:16]!r})")
            veo.strip_audio(tmp)
            dur = probe_dur(tmp)
            if dur < 5.0 or dur > 40.0:
                raise SystemExit(f"STOP: bad dur {dur}")
            shutil.move(str(tmp), str(DEST))
            print(
                f"SAVED {DEST} bytes={DEST.stat().st_size} dur={dur:.2f} "
                f"project={project_url}",
                flush=True,
            )
        finally:
            if ctx is not None:
                try:
                    ctx.close()
                except Exception:
                    pass


if __name__ == "__main__":
    main()
