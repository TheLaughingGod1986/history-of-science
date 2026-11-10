#!/usr/bin/env python3
"""J0140: Chief-authorized fresh P5:02 still + exactly one Fast attempt.

Desk #180 6140112141, amended by 6140142639. Never retry this runner
after an attempt record exists; Chief decides the cover if Fast fails.
"""
import os
import subprocess
import sys

import _mint_flow_cdp_v01 as mint

PLATE = "02_senebier_jars"
TAKE = 3  # fresh filename; prior Quality failures remain recorded


def selected_plates(part):
    plate = next(p for p in mint.board(part)["plates"] if p["id"] == PLATE).copy()
    plate["quality"] = "Fast"
    plate["prompt"] = (
        "Premium Animistry-class 3D cartoon. Jean Senebier, a thin Genevan pastor "
        "of about forty, short dark hair, dark clerical coat with white neck bands, "
        "sits by two water jars containing green leaves in a bright period room. "
        "He gently squeezes one bellows, its tube feeding bubbles into one jar. "
        "The other jar stays still. One figure, one simple motion. Warm daylight; "
        "no glow, candle, flame, lamp, text or Explorer. Continuous motion."
    )
    return [plate]


def main():
    os.environ["OWB_AGENT"] = "codex"
    key = f"{PLATE}#t{TAKE}"
    prior = mint.load_log("05")["takes"].get(key)
    # A style-chip refusal before Create consumes neither still nor Fast attempt.
    unsubmitted = (prior and prior.get("credits_used") == 0
                   and not prior.get("project_url") and not prior.get("start_frame")
                   and "style refs not attached" in prior.get("why", ""))
    if prior and not unsubmitted:
        raise SystemExit("STOP: Fast attempt already recorded; no automatic retry")
    raw, _, _ = mint.paths("05")
    still = raw.parent.parent / "refs/v02_flow_stills" / f"{PLATE}_t{TAKE}.png"
    if still.exists():
        raise SystemExit("STOP: fresh still filename already exists; inspect before continuing")
    mint.plates = selected_plates
    rc = mint.mint("05", {PLATE}, 1, stills=True, take=TAKE)
    log = mint.load_log("05")
    entry = log["takes"].get(key, {})
    entry["chief_authorization"] = "HOS #180 6140112141 / 6140142639; one Fast attempt only"
    log["takes"][key] = entry
    mint.save_log("05", log)
    reads = log.get("balance_reads", [])
    if reads and reads[-1].get("credits") is not None:
        subprocess.run([
            sys.executable, str(mint.Path.home() / "YouTube/orbit-with-ben/scripts/ai_spend.py"),
            "record", "--pool", "flow", "--left", str(reads[-1]["credits"]),
            "--by", "codex", "--note", "J0140 P5:02 fresh still/Fast attempt settled reading",
        ], check=True)
    raise SystemExit(rc)


if __name__ == "__main__":
    main()
