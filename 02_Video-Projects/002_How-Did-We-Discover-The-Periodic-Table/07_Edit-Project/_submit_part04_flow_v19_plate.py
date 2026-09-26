#!/usr/bin/env python3
"""Submit one Part04 v19 I2V create on live CDP; return project URL. No long wait."""
from __future__ import annotations
import argparse, json, os, sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))
import orbit_flow_veo_ui as flow

flow.FLOW_HOME = os.environ.get("ORBIT_FLOW_HOME", "https://flow.google.com/")
CDP = os.environ.get("ORBIT_FLOW_CDP", "http://127.0.0.1:9222")
STARTS = Path(__file__).resolve().parents[1] / "04_Generated-Clips/part04/refs/v19_start_frames"
MODEL = os.environ.get("ORBIT_FLOW_VEO_MODEL", "Veo 3.1 - Fast")

# Import prompts from mint module
sys.path.insert(0, str(Path(__file__).resolve().parent))
import importlib.util
spec = importlib.util.spec_from_file_location("mint", Path(__file__).resolve().parent / "_mint_part04_flow_v19.py")
mint = importlib.util.module_from_spec(spec)
# Avoid running mint main: load source and exec only constants/prompts
src = (Path(__file__).resolve().parent / "_mint_part04_flow_v19.py").read_text()
# crude extract PROMPTS dict via exec of prefix
ns = {}
exec(compile("\n".join(src.split("def sha256")[0].splitlines()), "mint_prefix", "exec"), ns)
PROMPTS = ns["PROMPTS"]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--plate", required=True)
    ap.add_argument("--out-json", type=Path, required=True)
    args = ap.parse_args()
    start = STARTS / f"{args.plate}_start_v19.jpg"
    if not start.exists():
        raise SystemExit(f"missing {start}")
    prompt = PROMPTS[args.plate]

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP)
        page = None
        for c in browser.contexts:
            for pg in c.pages:
                if "flow.google.com" in (pg.url or ""):
                    page = pg
                    break
            if page:
                break
        if page is None:
            page = browser.contexts[0].new_page()
        page.bring_to_front()
        # Always start from home to avoid stale project state
        page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=120000)
        time.sleep(2)
        try:
            page.get_by_role("button", name="Agree").click(timeout=2000)
        except Exception:
            pass

        # Monkeypatch wait: stop soon after submit by wrapping generate_clip timeout tiny
        # Better: call lower-level create once without waiting for media
        # Use generate_clip with timeout_s small AFTER submit by patching wait helper if needed.
        # Practical approach: call generate_clip with timeout_s=45 — it should submit then return gallery-pending.
        tmp = Path("/tmp") / f"hos_v19_{args.plate}_stub.mp4"
        if tmp.exists():
            tmp.unlink()
        info = {}
        try:
            info = flow.generate_clip(
                page,
                prompt,
                tmp,
                model=MODEL,
                start_frame=start,
                timeout_s=45,  # force early return after submit / early poll
                attempts=1,
                scenery_only=True,
            )
        except Exception as e:
            # Even on timeout, project URL may be pinned
            info = {
                "error": str(e),
                "project_url": getattr(page, "_orbit_flow_project_url", None) or (page.url or ""),
            }
            print(f"submit note: {e}", flush=True)

        project_url = (info.get("project_url") or info.get("url") or getattr(page, "_orbit_flow_project_url", None) or page.url or "")
        project_url = str(project_url).split("?")[0].rstrip("/")
        out = {
            "plate": args.plate,
            "project_url": project_url,
            "info": {k: v for k, v in info.items() if k != "path"},
            "start": str(start),
            "model": MODEL,
            "when": time.strftime("%Y-%m-%dT%H:%M:%S"),
        }
        args.out_json.parent.mkdir(parents=True, exist_ok=True)
        args.out_json.write_text(json.dumps(out, indent=2) + "\n")
        print(json.dumps(out, indent=2), flush=True)
        if "/project/" not in project_url:
            raise SystemExit("no project url after submit")


if __name__ == "__main__":
    main()
