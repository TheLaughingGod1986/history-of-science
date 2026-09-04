#!/usr/bin/env python3
"""Live Flow upload-control probe for Part 02 I2V."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))
import orbit_flow_veo_ui as flow  # noqa: E402

OUT = Path("/tmp/hos_flow_upload_probe")
OUT.mkdir(parents=True, exist_ok=True)
PINNED = os.environ.get(
    "HOS_FLOW_PROJECT_URL",
    "https://flow.google.com/u/1/project/30a34afb-8d9c-4eac-83ba-012d97f6b1b5",
)
PROFILE = Path(
    os.environ.get(
        "ORBIT_FLOW_PROFILE",
        str(Path.home() / ".playwright-hos-flow-profile"),
    )
)
STILL = (
    Path(__file__).resolve().parents[1]
    / "04_Generated-Clips/part02/refs/v04_stills/02_lavoisier_list_start.jpg"
)


def dump(page, label: str) -> None:
    rows = page.evaluate(
        """() => [...document.querySelectorAll('button,[role="button"],input,a,[role="tab"]')]
          .map(el => {
            const r = el.getBoundingClientRect();
            return {
              tag: el.tagName, type: el.getAttribute('type')||'',
              text: ((el.innerText||el.getAttribute('aria-label')||el.getAttribute('title')||'')
                .trim().replace(/\\s+/g,' ')).slice(0,160),
              aria: (el.getAttribute('aria-label')||'').slice(0,100),
              accept: el.getAttribute('accept')||'',
              x: Math.round(r.x), y: Math.round(r.y),
              w: Math.round(r.width), h: Math.round(r.height),
              vis: r.width>2 && r.height>2 && r.bottom>0 && r.top<innerHeight
            };
          }).filter(b => b.vis)
        """
    )
    (OUT / f"{label}.json").write_text(json.dumps(rows, indent=2))
    page.screenshot(path=str(OUT / f"{label}.png"), full_page=False)
    print(f"=== {label} ({len(rows)}) ===", flush=True)
    for b in rows:
        blob = f"{b['text']} {b['aria']} {b['accept']} {b['type']}".lower()
        if b["type"] == "file" or any(
            k in blob
            for k in (
                "upload", "add", "media", "frame", "ingredient",
                "image", "photo", "file", "create", "plus", "attach",
            )
        ):
            print(
                f"  [{b['tag']}] {b['text']!r} aria={b['aria']!r} "
                f"accept={b['accept']!r} @{b['x']},{b['y']} {b['w']}x{b['h']}",
                flush=True,
            )


def main() -> None:
    from playwright.sync_api import sync_playwright

    profile = flow.profile_path(PROFILE)
    print(f"profile={profile} still={STILL.exists()}", flush=True)
    with sync_playwright() as p:
        ctx, page = flow.launch_context(p, headed=True, profile=profile)
        flow.ensure_flow_account(page)
        page.goto(PINNED, wait_until="domcontentloaded", timeout=120_000)
        page.wait_for_timeout(2500)
        flow.dismiss_banners(page)
        dump(page, "01_project")

        flow._open_create_picker(page)
        page.wait_for_timeout(1000)
        dump(page, "02_create_picker")

        # Try Frames mode
        try:
            flow._set_video_aspect_and_outputs(
                page, frames_mode=True, ingredients_mode=False
            )
            page.wait_for_timeout(1000)
            dump(page, "03_frames_mode")
        except Exception as e:
            print(f"frames mode fail: {e}", flush=True)

        # Click anything that looks like a first-frame / upload dropzone
        clicked = page.evaluate(
            """() => {
              const out = [];
              for (const el of document.querySelectorAll('button,[role="button"],div,span')) {
                const t = ((el.innerText||'') + ' ' + (el.getAttribute('aria-label')||'')).trim();
                if (!/(frame|upload|image|photo|media|start|add)/i.test(t)) continue;
                if (t.length > 80) continue;
                const r = el.getBoundingClientRect();
                if (r.width < 10 || r.height < 10) continue;
                out.push({t: t.slice(0,80), x:r.x, y:r.y, w:r.width, h:r.height});
              }
              return out.slice(0, 40);
            }"""
        )
        print("frame-ish elements:", json.dumps(clicked, indent=2), flush=True)

        # Try file chooser from prompt + again after Frames
        for label in ("prompt_plus", "frames_plus"):
            try:
                with page.expect_file_chooser(timeout=5000) as fc:
                    flow._open_create_picker(page)
                print(f"{label}: chooser opened from create picker alone!", flush=True)
                fc.value.set_files(str(STILL))
                page.wait_for_timeout(3000)
                dump(page, f"04_{label}_after_upload")
                break
            except Exception as e:
                print(f"{label}: no chooser from create alone: {e}", flush=True)

        # Click dropzone-looking elements with file chooser
        for sel_text in (
            "Upload",
            "upload",
            "Add image",
            "Add media",
            "Frames",
            "Start frame",
            "First frame",
            "Image",
        ):
            loc = page.get_by_text(sel_text, exact=False)
            if loc.count() == 0:
                continue
            try:
                with page.expect_file_chooser(timeout=4000) as fc:
                    loc.first.click(timeout=2000, force=True)
                print(f"chooser via text {sel_text!r}", flush=True)
                fc.value.set_files(str(STILL))
                page.wait_for_timeout(4000)
                dump(page, f"05_after_{sel_text.replace(' ', '_')}")
                # check Add to Prompt
                add = page.locator('button:has-text("Add to Prompt")')
                print(f"Add to Prompt count={add.count()}", flush=True)
                break
            except Exception as e:
                print(f"text {sel_text!r} no chooser: {e}", flush=True)

        # Ingredients mode
        try:
            flow._set_video_aspect_and_outputs(
                page, frames_mode=False, ingredients_mode=True
            )
            page.wait_for_timeout(1000)
            dump(page, "06_ingredients_mode")
            with page.expect_file_chooser(timeout=5000) as fc:
                if not flow._click_uploadish_control(page):
                    flow._open_create_picker(page)
            fc.value.set_files(str(STILL))
            page.wait_for_timeout(4000)
            dump(page, "07_ingredients_uploaded")
            print(
                f"Add to Prompt count={page.locator('button:has-text(\"Add to Prompt\")').count()}",
                flush=True,
            )
            print(
                f"attachment_count={flow._prompt_attachment_count(page)}",
                flush=True,
            )
        except Exception as e:
            print(f"ingredients upload fail: {e}", flush=True)

        print(f"artifacts → {OUT}", flush=True)
        page.wait_for_timeout(2000)


if __name__ == "__main__":
    main()
