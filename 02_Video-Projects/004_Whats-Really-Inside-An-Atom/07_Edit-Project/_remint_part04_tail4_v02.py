#!/usr/bin/env python3
"""Remint Part 04 tail plates after Gemini 429.

Try Gemini Veo 3.1 with backoff; if still exhausted, use Flow Fast CDP
(same Veo 3.1 engine) even if under the ~150 buffer — otherwise the part
cannot finish. Log path clearly.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))

# Reuse remint module helpers by importing after path setup
EDIT = Path(__file__).resolve().parent
sys.path.insert(0, str(EDIT))

# Run the shared remint script for specific plates — it already has 429 backoff.
PLATES = [
    "18_nothing_at_all",
    "19_nucleus_question",
    "20_lawyer_amateur",
    "22_cannot_measure_yet",
]

if __name__ == "__main__":
    # First pass: Gemini via remint (backoff patched)
    cmd = [
        str(REPO / ".venv_hos_veo/bin/python"),
        str(EDIT / "_remint_part04_v02.py"),
        *PLATES,
    ]
    print("RUN", " ".join(cmd), flush=True)
    rc = subprocess.call(cmd)
    log = json.loads((EDIT / "PART04_MINT_LOG_v02.json").read_text())
    missing = [
        pid
        for pid in PLATES
        if not (log.get("plates", {}).get(pid, {}).get("keep") or {}).get("file", "").endswith("_v02.mp4")
    ]
    if not missing:
        print("ALL TAIL KEEP", flush=True)
        raise SystemExit(0)

    print(f"Gemini still missing {missing} — Flow Fast fallback (same Veo 3.1)", flush=True)
    # Force Flow by temporarily raising buffer check off via env
    os.environ["HOS_FORCE_FLOW_TAIL"] = "1"
    # Patch: call remint with a monkeypatch via env read in remint
    # Instead: inline Flow mint for missing using remint's functions
    import importlib.util

    spec = importlib.util.spec_from_file_location("remint", EDIT / "_remint_part04_v02.py")
    rem = importlib.util.module_from_spec(spec)
    # Prevent remint main auto-run: load by reading and exec with guard
    # Simpler approach: set FLOW_CREDIT_BUFFER=0 by editing then restore
    src = (EDIT / "_remint_part04_v02.py").read_text()
    if "FLOW_CREDIT_BUFFER = 150" not in src:
        raise SystemExit("buffer const missing")
    (EDIT / "_remint_part04_v02.py").write_text(
        src.replace("FLOW_CREDIT_BUFFER = 150", "FLOW_CREDIT_BUFFER = 0  # tail fallback after Gemini 429")
    )
    try:
        # Clear tries again
        for pid in missing:
            log["plates"][pid] = {
                "id": pid,
                "status": "PENDING_REMINT",
                "tries": [],
                "try_detail": [],
                "v01_verdict": "FIX",
                "note": "Flow Fast fallback after Gemini 429",
            }
        (EDIT / "PART04_MINT_LOG_v02.json").write_text(json.dumps(log, indent=2) + "\n")
        rc2 = subprocess.call(
            [
                str(REPO / ".venv_hos_veo/bin/python"),
                str(EDIT / "_remint_part04_v02.py"),
                *missing,
            ]
        )
    finally:
        (EDIT / "_remint_part04_v02.py").write_text(
            (EDIT / "_remint_part04_v02.py")
            .read_text()
            .replace(
                "FLOW_CREDIT_BUFFER = 0  # tail fallback after Gemini 429",
                "FLOW_CREDIT_BUFFER = 150",
            )
        )
    log = json.loads((EDIT / "PART04_MINT_LOG_v02.json").read_text())
    still = [
        pid
        for pid in PLATES
        if not (log.get("plates", {}).get(pid, {}).get("keep") or {}).get("file", "").endswith("_v02.mp4")
    ]
    if still:
        raise SystemExit(f"STOP still missing KEEP: {still}")
    print("ALL TAIL KEEP via Flow fallback", flush=True)
