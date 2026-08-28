#!/usr/bin/env python3
"""Final cinematic polish: fewer cards and genuinely animated, frequent Orbit."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path("/Users/ben/code/Orbit-YouTube/02_Video-Projects/001_Will-We-Ever-Meet-Aliens")
EDIT = ROOT / "07_Edit-Project"
BASE_SCRIPT = EDIT / "_build_v23_interactive_orbit.py"
BED = EDIT / "_render_cache_v25/picture_bed_cinematic_fresh.mp4"
MIX = EDIT / "_mix_work_v24/final_mix_hook-first.wav"
RIG = Path("/Users/ben/code/Orbit-YouTube/01_Orbit-Character/06_Animation-Exports/Overlay-Rig-v03")
OUT = ROOT / "09_Final-Export/aliens_broadcast_v25_FINAL_POLISH.mp4"
OUT_PIC = ROOT / "09_Final-Export/aliens_broadcast_v25_FINAL_POLISH_pic.mp4"
PROOF = ROOT / "09_Final-Export/aliens_v25_PROOF_final-polish_120s.mp4"
PROOF_PIC = ROOT / "09_Final-Export/_v25_proof_picture.mp4"
MANIFEST = EDIT / "ORBIT_PERFORMANCES_v25.json"
PRIOR_MANIFEST = EDIT / "ORBIT_PERFORMANCES_v24.json"


ADDITIONAL_EVENTS = [
    {"section": "01_cold-open",     "start": 15.000,  "end": 22.000,  "pattern": "watch",   "purpose": "stay present through the opening promise"},
    {"section": "03_exoplanets",    "start": 78.200,  "end": 85.500,  "pattern": "present", "purpose": "guide the habitable-world transition"},
    {"section": "03_exoplanets",    "start": 105.000, "end": 112.000, "pattern": "think",   "purpose": "consider the Drake uncertainty"},
    {"section": "04_fermi-paradox", "start": 196.800, "end": 204.000, "pattern": "react",   "purpose": "register the missing evidence"},
    {"section": "05_great-filter",  "start": 227.200, "end": 236.000, "pattern": "present", "purpose": "follow the evolutionary barrier"},
    {"section": "05_great-filter",  "start": 266.900, "end": 274.000, "pattern": "watch",   "purpose": "stay with the early-universe possibility"},
    {"section": "06_explanations",  "start": 304.000, "end": 312.000, "pattern": "think",   "purpose": "consider interstellar distance"},
    {"section": "06_explanations",  "start": 368.300, "end": 375.500, "pattern": "react",   "purpose": "react after the Wow signal"},
    {"section": "07_detection",     "start": 448.800, "end": 455.000, "pattern": "present", "purpose": "guide the Solar System search"},
    {"section": "08_first-contact", "start": 520.500, "end": 528.000, "pattern": "watch",   "purpose": "stay with the honest answer"},
    {"section": "08_first-contact", "start": 548.200, "end": 555.000, "pattern": "think",   "purpose": "reflect before the conclusion"},
    {"section": "09_conclusion",    "start": 577.200, "end": 586.000, "pattern": "present", "purpose": "guide the final perspective"},
]


def load_base():
    spec = importlib.util.spec_from_file_location("orbit_v23", BASE_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def animated_expand(event: dict) -> list[dict]:
    """Choreograph real performance changes inside every appearance."""
    start, end = float(event["start"]), float(event["end"])
    duration = end - start
    pattern = event["pattern"]
    action = {
        "watch": "thinking-left",
        "present": "present-left",
        "think": "thinking-left",
        "react": "amazed",
        "wave": "wave-camera",
    }[pattern]

    if duration < 4.2:
        poses = [action]
    elif pattern == "wave":
        poses = ["neutral-left", "wave-camera"]
    else:
        poses = ["neutral-left", action, "neutral-left"]

    blend = 0.40
    unit = duration / len(poses)
    segments = []
    for index, pose in enumerate(poses):
        segment_start = start + index * unit
        segment_end = start + (index + 1) * unit
        if index:
            segment_start -= blend
        if index < len(poses) - 1:
            segment_end += blend
        segments.append({
            "start": segment_start,
            "end": segment_end,
            "pose": pose,
            "section": event["section"],
            "purpose": event["purpose"],
            "event_start": start,
            "event_end": end,
        })
    return segments


def configure(module) -> None:
    prior_events = json.loads(PRIOR_MANIFEST.read_text())["events"]
    # Keep Orbit clear of the retained "WE DON'T KNOW" information card.
    # The v24 performance originally crossed the card at 516.418–520.418.
    prior_events = [
        {
            **event,
            "start": 510.300,
            "end": 516.000,
        }
        if abs(float(event["start"]) - 513.000) < 0.100
        else event
        for event in prior_events
    ]
    module.BED = BED
    module.MIX = MIX
    module.RIG = RIG
    module.LOOPS = {
        pose: RIG / f"loops/orbit_{pose}_animated-blink_6s_v01.mov"
        for pose in ("neutral-left", "present-left", "thinking-left", "amazed", "wave-camera")
    }
    module.OUT = OUT
    module.OUT_PIC = OUT_PIC
    module.PROOF = PROOF
    module.PROOF_PIC = PROOF_PIC
    module.MANIFEST = MANIFEST
    module.POSE_BLEND = 0.40
    module.EVENTS = sorted(prior_events + ADDITIONAL_EVENTS, key=lambda item: item["start"])
    module.expand_event = animated_expand


def update_manifest() -> None:
    data = json.loads(MANIFEST.read_text())
    data.update({
        "version": 25,
        "rule": "cinematic card reduction with frequent blink-and-gesture Orbit performances",
        "animation_upgrade": {
            "genuine_blinks_per_six_second_loop": 2,
            "pose_changes_within_appearances": True,
            "fixed_lower_right_stage": True,
        },
        "information_cards_original": 53,
        "information_cards_retained": 6,
        "information_cards_replaced": 47,
        "chapter_cards_retained": 8,
        "brand_hold_seconds": 2.0,
        "source_version_preserved": 24,
        "output": str(OUT),
    })
    MANIFEST.write_text(json.dumps(data, indent=2))


def main(mode: str) -> None:
    module = load_base()
    configure(module)
    module.main(mode)
    update_manifest()


if __name__ == "__main__":
    import sys
    main(sys.argv[1] if len(sys.argv) > 1 else "proof")
