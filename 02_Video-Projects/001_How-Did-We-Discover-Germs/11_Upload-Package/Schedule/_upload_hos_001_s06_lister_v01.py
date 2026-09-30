#!/usr/bin/env python3
"""Upload HOS 001 S06 Lister carbolic spray Short — Ben 14:45 GO.

@HistoryOfScienceYT only. Schedule Tue 20 Oct 2026 11:30 Europe/London.
Private until then. No Premiere. Not kids. Altered YES. Related `_C92tIJCk8A`.
Cover live_v06. Do NOT touch CUu8k38iAMc or any other video.
"""
from __future__ import annotations

import importlib.util
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

REPO = Path("/Users/benjaminoats/YouTube/History Of Science")
U004 = (
    REPO
    / "02_Video-Projects/004_Whats-Really-Inside-An-Atom/11_Upload-Package/Schedule"
    / "_upload_hos_004_shorts_v01.py"
)
PROJ = REPO / "02_Video-Projects/001_How-Did-We-Discover-Germs"
SCHED = PROJ / "11_Upload-Package/Schedule"
EV = SCHED / "evidence_2026-09-30_s06_lister"
ART = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts"
AGENT = Path.home() / (
    "Library/Application Support/Cursor/AgentStores/"
    "cursor_agent_stores/bc-958ae0f3-be07-568f-a2ab-eb7f422d8839/files/artifacts"
)
LONDON = ZoneInfo("Europe/London")

JOB = {
    "slot": "s06",
    "title": "The spray that stopped surgery killing patients",
    "file": PROJ / "10_Shorts/hos_001_s06_carbolic_spray_punch_v01.mp4",
    "thumb": PROJ / "10_Shorts/covers_live_v01/hos_001_s06_carbolic_spray_cover_live_v06.jpg",
    "cover": PROJ / "10_Shorts/covers_live_v01/hos_001_s06_carbolic_spray_cover_live_v06.jpg",
    "desc": SCHED / "hos_001_s06_description_v01.txt",
    "related_id": "_C92tIJCk8A",
    "related_title": "How Did We Discover Germs?",
    "day": 20,
    "month_re": r"Oct|October",
    "date_typed": "20 October 2026",
    "time": "11:30",
    "label": "Tuesday 20 Oct 2026 11:30 Europe/London",
    "air_date": "2026-10-20",
}

# Never steal these as the new Short id
EXTRA_BANNED = {
    "CUu8k38iAMc",  # Tue duplicate Private — do not touch
    "29bpGAI0wb8",  # Fri scheduled
    "TbMMJSRKC3U",  # Sun scheduled
    "zI_eD3vFWmE",
    "xvanpsLeADE",
    "oowAOWTBoq0",
}


def load_uploader():
    spec = importlib.util.spec_from_file_location("hos004_upload", U004)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


def copy_artifacts(prefix: str = "BEN_1445") -> None:
    for d in (ART, AGENT):
        d.mkdir(parents=True, exist_ok=True)
    if not EV.exists():
        return
    for p in EV.glob("s06_*.png"):
        for d in (ART, AGENT):
            shutil.copy2(p, d / f"{prefix}_{p.name}")
    for name in ("RESULT.json", "run.log"):
        src = EV / name
        if src.exists():
            for d in (ART, AGENT):
                shutil.copy2(src, d / f"{prefix}_s06_{name}")


def main() -> int:
    for key in ("file", "thumb", "desc"):
        if not Path(JOB[key]).exists():
            raise SystemExit(f"missing {key}: {JOB[key]}")

    u = load_uploader()
    # Point evidence + tags at 001 schedule folder
    u.EV = EV
    u.SCHED = SCHED
    tags_path = SCHED / "hos_001_s06_tags_v01.txt"
    u.TAGS = tags_path.read_text().strip()
    EV.mkdir(parents=True, exist_ok=True)

    # Harden extract_new_id against Fri/Sun/Private duplicate
    _orig = u.extract_new_id

    def extract_safe(page, exclude: str = ""):
        vid = _orig(page, exclude=exclude or JOB["related_id"])
        if vid in EXTRA_BANNED:
            return None
        return vid

    u.extract_new_id = extract_safe

    result = {
        "ok": False,
        "channel": u.HANDLE,
        "channelId": u.HOS,
        "job": {
            "slot": JOB["slot"],
            "title": JOB["title"],
            "related_id": JOB["related_id"],
            "air": JOB["label"],
            "cover": str(JOB["cover"]),
        },
        "do_not_touch": ["CUu8k38iAMc"],
        "affiliate": "none",
        "madeForKids": False,
        "altered": "YES",
        "category": "Education",
        "comments": "ON",
        "remixing": "ON",
        "premiere": False,
        "started": datetime.now(LONDON).isoformat(timespec="seconds"),
        "shorts": [],
    }

    u.ensure_chrome()
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(u.CDP)
        ctx = browser.contexts[0]
        page = u.studio_page(ctx)
        page.bring_to_front()
        hos = u.ensure_hos(page)
        result["hos"] = hos
        page.screenshot(path=str(EV / "00_hos_boot.png"), full_page=True)
        if not hos.get("ok"):
            result["stopped"] = hos.get("reason") or "HOS_NOT_READY"
            (EV / "RESULT.json").write_text(json.dumps(result, indent=2, default=str) + "\n")
            copy_artifacts()
            print(json.dumps(result, indent=2, default=str)[:2000])
            return 2

        u.log(f"==== upload s06 {JOB['title']} related={JOB['related_id']} ====")
        if u.is_glue(page):
            result["stopped"] = "GLUE_BEFORE_UPLOAD"
            (EV / "RESULT.json").write_text(json.dumps(result, indent=2, default=str) + "\n")
            copy_artifacts()
            return 1

        try:
            item = u.upload_one(page, JOB)
        except Exception as e:
            item = {"slot": "s06", "ok": False, "error": f"{type(e).__name__}:{e}"}
            page.screenshot(path=str(EV / "s06_exception.png"), full_page=True)

        result["shorts"].append(item)
        result["finished"] = datetime.now(LONDON).isoformat(timespec="seconds")
        result["ok"] = bool(item.get("ok") and item.get("platformPostId"))
        result["platformPostId"] = item.get("platformPostId")
        result["platformUrl"] = item.get("platformUrl")
        (EV / "RESULT.json").write_text(json.dumps(result, indent=2, default=str) + "\n")
        copy_artifacts()
        print(json.dumps(result, indent=2, default=str)[:5000])
        return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
