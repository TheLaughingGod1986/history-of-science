#!/usr/bin/env python3
"""Auth+credits gate for Part 03 v06 — STOP before mint if wrong account."""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))
import orbit_flow_veo_ui as flow  # noqa: E402

flow.FLOW_HOME = os.environ.get("ORBIT_FLOW_HOME", "https://flow.google.com/u/1/")
REQUIRED = "benoats@googlemail.com"
ALLOWED = {REQUIRED, "benoats@gmail.com"}
FORBIDDEN = "benoats86@gmail.com"
OUT = Path(__file__).resolve().parent / "logs" / "flow_auth_probe_part03_v06.json"
PROFILE = Path(
    os.environ.get(
        "ORBIT_FLOW_PROFILE",
        str(Path.home() / ".playwright-hos-flow-profile"),
    )
)
DIE = (
    "out of google flow credits",
    "reached your credit or daily limit",
    "you're out of google flow credits",
)


def main() -> None:
    from playwright.sync_api import sync_playwright

    profile = flow.profile_path(PROFILE)
    result = {"ok": False, "flow_home": flow.FLOW_HOME, "profile": str(profile)}
    with sync_playwright() as p:
        ctx, page = flow.launch_context(p, headed=True, profile=profile)
        try:
            page.goto(flow.FLOW_HOME, wait_until="domcontentloaded", timeout=120_000)
            page.wait_for_timeout(4000)
            if "accounts.google.com" in (page.url or ""):
                for needle in (REQUIRED, "benoats@gmail.com"):
                    loc = page.get_by_text(needle, exact=False)
                    if loc.count():
                        loc.first.click(timeout=8000)
                        page.wait_for_timeout(7000)
                        break
            flow.dismiss_banners(page)
            page.wait_for_timeout(1500)
            if not flow.looks_logged_in(page):
                result["error"] = "BLOCKED_AUTH: not logged in"
                OUT.parent.mkdir(parents=True, exist_ok=True)
                OUT.write_text(json.dumps(result, indent=2))
                raise SystemExit(result["error"])
            labels = page.eval_on_selector_all(
                "button, a, [role=button]",
                "els => els.map(e => (e.getAttribute('aria-label') || e.innerText || '').trim())"
                ".filter(Boolean)",
            )
            blob = "\n".join(labels)
            emails = {
                e.lower()
                for e in re.findall(
                    r"[A-Za-z0-9._%+-]+@(?:gmail|googlemail)\.com", blob, flags=re.I
                )
            }
            active = None
            m = re.search(
                r"Google Account:[^\n\(]*\(([^)]+@(?:gmail|googlemail)\.com)\)",
                blob,
                re.I,
            )
            if m:
                active = m.group(1).lower()
            elif emails & ALLOWED:
                active = sorted(emails & ALLOWED)[0]
            elif emails:
                active = sorted(emails)[0]
            result["emails"] = sorted(emails)
            result["active"] = active
            result["url"] = page.url
            body = (page.inner_text("body") or "")
            low = body.lower()
            for marker in DIE:
                if marker in low:
                    result["error"] = f"STOP BLOCKED: {marker}"
                    OUT.parent.mkdir(parents=True, exist_ok=True)
                    OUT.write_text(json.dumps(result, indent=2))
                    raise SystemExit(result["error"])
            hits = []
            for pat in (r"\d[\d,]*\+?\s*credits?", r"ultra", r"daily limit"):
                for mm in re.finditer(pat, body, flags=re.I):
                    hits.append(mm.group(0).strip()[:80])
            result["credits_probe"] = hits[:8]
            if not active or active not in ALLOWED or "benoats86" in (active or ""):
                result["error"] = f"BLOCKED_AUTH: active={active} need={REQUIRED}"
                OUT.parent.mkdir(parents=True, exist_ok=True)
                OUT.write_text(json.dumps(result, indent=2))
                raise SystemExit(result["error"])
            result["ok"] = True
            OUT.parent.mkdir(parents=True, exist_ok=True)
            OUT.write_text(json.dumps(result, indent=2))
            print(json.dumps(result, indent=2), flush=True)
            print(f"AUTH_OK {active} credits={hits[:4]}", flush=True)
        finally:
            try:
                ctx.close()
            except Exception:
                pass


if __name__ == "__main__":
    main()
