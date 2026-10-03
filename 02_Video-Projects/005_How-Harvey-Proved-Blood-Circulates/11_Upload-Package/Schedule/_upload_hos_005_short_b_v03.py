#!/usr/bin/env python3
"""Upload HOS 005 Short B v03 — Claude KEEP title. Related deferred to 29 Oct 18:05 → wwcjcFfC-5M."""
from __future__ import annotations

import importlib.util
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
BLOOD = HERE.parents[1]
ART = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts/DESK_2026-10-03_005_v02_upload"
EV = HERE / "evidence_2026-10-03_short_b"
LONDON = ZoneInfo("Europe/London")

_spec = importlib.util.spec_from_file_location("nov", HERE / "_upload_hos_nov_four_shorts_v01.py")
nov = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(nov)

# Defer Related — do not set to old 0If…; 18:05 jobs will point at NEW long
nov.wizard_related = lambda page, related_title, related_id: "deferred_to_29oct1805_new_long"
nov.set_related = lambda page, new_id, related_id, related_title: "deferred_to_29oct1805_new_long"

JOB = {
    "slot": "005b",
    "title": "One Tight Band Proved Your Blood Goes Round",
    "file": BLOOD / "10_Shorts/hos_005_s02_the_tied_arm_v03.mp4",
    "thumb": BLOOD / "10_Shorts/covers_v02/hos_005_s02_the_tied_arm_cover_v02.jpg",
    "cover": BLOOD / "10_Shorts/covers_v02/hos_005_s02_the_tied_arm_cover_v02.jpg",
    "desc": HERE / "hos_005_s02_description_v01.txt",
    "related_id": "wwcjcFfC-5M",  # placeholder for desc replace only; Related setter stubbed
    "related_title": "The Tied Arm That Proved Your Blood Circulates",
    "day": 8,
    "month_re": r"Nov|November",
    "date_typed": "8 November 2026",
    "time": "11:30",
    "label": "Sunday 8 Nov 2026 11:30 Europe/London",
    "air_date": "2026-11-08",
}


def main():
    ART.mkdir(parents=True, exist_ok=True)
    EV.mkdir(parents=True, exist_ok=True)
    assert JOB["file"].exists()
    assert JOB["cover"].exists()
    nov.ensure_chrome()
    out = {
        "at": datetime.now(LONDON).isoformat(timespec="seconds"),
        "job": {k: str(v) if isinstance(v, Path) else v for k, v in JOB.items()},
        "note": "Related deferred to 29 Oct 18:05 → wwcjcFfC-5M; not set now",
    }
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(nov.CDP, timeout=60000)
        page = browser.contexts[0].pages[0] if browser.contexts[0].pages else browser.contexts[0].new_page()
        page.set_default_timeout(180000)
        # Soft HOS check — avoid ensure_hos navigate ERR_ABORT on sticky Studio tabs
        body0 = page.inner_text("body") if page.url else ""
        if "History of Science" not in body0 or "Orbit" in body0 and "History of Science" not in body0:
            page.goto("https://studio.youtube.com/channel/UCXp7HkBIl1LgaznXuZHJyRg", wait_until="domcontentloaded", timeout=120000)
            page.wait_for_timeout(3500)
            body0 = page.inner_text("body")
        hos = {"ok": "History of Science" in body0, "url": page.url, "soft": True}
        out["hos"] = hos
        if not hos["ok"]:
            raise SystemExit(f"not HOS: {hos}")
        res = nov.upload_one(page, JOB)
        out["upload"] = res
        vid = (
            (res or {}).get("video_id")
            or (res or {}).get("id")
            or (res or {}).get("new_id")
            or (res or {}).get("udvid")
        )
        out["SHORT_B_ID"] = vid
        (EV / "SHORT_B_UPLOAD_RESULT.json").write_text(json.dumps(out, indent=2, default=str) + "\n")
        (ART / "SHORT_B_UPLOAD_RESULT.json").write_text(json.dumps(out, indent=2, default=str) + "\n")
        print(json.dumps(out, indent=2, default=str)[:5000])
        print("SHORT_B_ID", vid)
        if not vid:
            raise SystemExit("no short id returned")


if __name__ == "__main__":
    main()
