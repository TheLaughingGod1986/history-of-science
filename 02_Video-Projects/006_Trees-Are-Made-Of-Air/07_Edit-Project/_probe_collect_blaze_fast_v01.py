#!/usr/bin/env python3
"""J0140: Acting-Chief ruling (14 Oct 20:50Z) item 1 for P4:06 (06_collect_blaze).

1. Try harvest_spent("04") first (0 credits) with the top-row harvest fix.
2. Only if 06_collect_blaze#t2 is still missing from the Flow project, mint
   exactly one Fast take (06_collect_blaze#t3, fresh Nano Banana start still +
   Veo 3.1 Fast i2v, ~10 credits) and log the spend via ai_spend.py.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import _mint_flow_cdp_v01 as mint

PLATE = "06_collect_blaze"
TAKE = 3


def selected_plates(part: str) -> list[dict]:
    plate = next(p for p in mint.board(part)["plates"] if p["id"] == PLATE).copy()
    plate["quality"] = "Fast"
    return [plate]


def main() -> None:
    os.environ["OWB_AGENT"] = "gemini"
    log = mint.load_log("04")
    t2 = log.get("takes", {}).get(f"{PLATE}#t2", {})
    if not str(t2.get("harvest_retry", "")).startswith("2026-10-14"):
        print("=== Step 1: harvest check on P4:06 t2 (0 credits) ===", flush=True)
        mint.harvest_spent("04", wait_s=15)
        log = mint.load_log("04")
        t2 = log.get("takes", {}).get(f"{PLATE}#t2", {})
    else:
        print(f"=== Step 1: P4:06 t2 already verified absent ({t2.get('harvest_retry')}) ===", flush=True)
    if t2.get("file") and Path(t2["file"]).exists():
        print(f"Harvested {PLATE}#t2 -> {t2['file']}, skipping Fast re-mint.", flush=True)
        return

    key = f"{PLATE}#t{TAKE}"
    prior = log.get("takes", {}).get(key)
    unsubmitted = (
        prior
        and (prior.get("credits_used") or 0) == 0
        and not prior.get("project_url")
        and "style refs not attached" in prior.get("why", "")
    )
    if prior and not unsubmitted:
        raise SystemExit(f"STOP: {key} attempt already recorded; no automatic retry")

    print(f"=== Step 2: {PLATE}#t2 absent in Flow project; minting 1 Fast take ({key}) ===", flush=True)
    mint.plates = selected_plates
    rc = mint.mint("04", {PLATE}, 1, stills=True, take=TAKE)
    log = mint.load_log("04")
    entry = log.get("takes", {}).get(key, {})
    entry["chief_authorization"] = (
        "Acting-Chief ruling J0140 (Claude, 14 Oct 20:50Z) item 1: "
        "P4:06 t2 not in Flow project -> one Fast take"
    )
    log["takes"][key] = entry
    mint.save_log("04", log)

    used = entry.get("credits_used") or 0
    after = entry.get("credits_after")
    ai_spend = Path.home() / "YouTube/orbit-with-ben/scripts/ai_spend.py"
    if used > 0 and after is not None:
        subprocess.run(
            [
                sys.executable,
                str(ai_spend),
                "spend",
                "--pool",
                "flow",
                "--amount",
                str(used),
                "--left",
                str(after),
                "--film",
                "hos-006",
                "--item",
                f"P4:{key}",
                "--by",
                "gemini",
                "--note",
                "J0140 P4:06 t3 Fast i2v after t2 missing in Flow project",
            ],
            check=True,
        )
    elif after is not None:
        subprocess.run(
            [
                sys.executable,
                str(ai_spend),
                "record",
                "--pool",
                "flow",
                "--left",
                str(after),
                "--by",
                "gemini",
                "--note",
                f"J0140 P4:06 {key} balance read",
            ],
            check=True,
        )
    raise SystemExit(rc)


if __name__ == "__main__":
    main()
