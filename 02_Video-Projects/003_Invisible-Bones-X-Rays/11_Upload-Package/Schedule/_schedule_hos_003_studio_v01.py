#!/usr/bin/env python3
"""HOS 003 Studio schedule driver.

1) Long Premiere Thu 24 Sep 2026 18:00 Europe/London
2) Shorts Fri/Sat/Sun 11:30 London with Related ▶ Premiere

Channel: @HistoryOfScienceYT only. Never Orbit / Oppti. Zero /go/.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

PY = "/tmp/hos-studio-pw-venv/bin/python"
SCHED = Path(__file__).resolve().parent
PREMIERE = SCHED / "_upload_hos_003_premiere_v01.py"
SHORTS = SCHED / "_upload_hos_003_shorts_v01.py"
EV_LONG = SCHED / "evidence_2026-09-23_premiere"
EV_SHORTS = SCHED / "evidence_2026-09-23_shorts"


def run(script: Path, extra: list[str] | None = None) -> int:
    cmd = [PY, str(script)] + (extra or [])
    print("RUN", " ".join(cmd), flush=True)
    return subprocess.call(cmd)


def read_parent() -> str | None:
    for p in (
        EV_LONG / "RESULT.json",
        SCHED / "PACKAGE_UPLOAD_RESULT_2026-09-23_premiere.json",
    ):
        if not p.exists():
            continue
        try:
            data = json.loads(p.read_text())
        except Exception:
            continue
        vid = data.get("id") or data.get("videoId") or data.get("platformPostId")
        if vid and data.get("ok"):
            return vid
    return None


def main() -> int:
    extra = sys.argv[1:]
    if extra and extra[0] in ("--shorts-only",):
        parent = extra[1] if len(extra) > 1 else read_parent()
        if not parent:
            print("no premiere videoId — pass --shorts-only VIDEO_ID", flush=True)
            return 2
        return run(SHORTS, ["--parent", parent])
    rc = run(PREMIERE, extra)
    if rc != 0:
        print(f"premiere failed rc={rc}", flush=True)
        return rc
    parent = read_parent()
    if not parent:
        print("premiere reported ok but no videoId in RESULT.json", flush=True)
        return 2
    print(f"PARENT {parent}", flush=True)
    return run(SHORTS, ["--parent", parent])


if __name__ == "__main__":
    raise SystemExit(main())
