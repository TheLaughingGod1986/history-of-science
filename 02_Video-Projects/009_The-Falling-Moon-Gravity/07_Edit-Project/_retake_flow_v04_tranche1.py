#!/usr/bin/env python3
"""Targeted UAT retakes for J1192 (HOS 009 boards v04 tranche 1)."""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import _mint_flow_v04_tranche1 as base

MEDIA = base.MEDIA

PARENT_STILL_REUSE = {
    "03_shot_slow": MEDIA / "04_Generated-Clips/part03/refs/v04_flow_stills/02_cannon_world_t1.png",
    "04_shot_faster": MEDIA / "04_Generated-Clips/part03/refs/v04_flow_stills/02_cannon_world_t1.png",
    "02_spray_paint_c1": MEDIA / "04_Generated-Clips/part04/refs/v04_flow_stills/02_spray_paint_t1.png",
    "02_spray_paint_c2": MEDIA / "04_Generated-Clips/part04/refs/v04_flow_stills/02_spray_paint_t1.png",
    "08_cup_and_planets_c1": MEDIA / "04_Generated-Clips/part05/refs/v04_flow_stills/08_cup_and_planets_t1.png",
}

REGEN_STILL_PROMPTS = {
    "05_iss_orbit": (
        "Premium Animistry-class 3D cartoon. A generic space station, a simple 3D cartoon silhouette "
        "with solar panels and cylindrical modules and no flags, logos or letters, gliding high in orbit "
        "above the curved blue Earth with white clouds against dark starry space. "
        "No Moon in frame, no drawn lines, no glowing rings or trails, no people."
    ),
    "06_iss_apple": (
        "Premium Animistry-class 3D cartoon. Inside a plain cylindrical space station cabin with handrails "
        "and warm side window light, two generic adult astronauts in plain white suits with gold visors down "
        "float upright side by side facing each other (both astronauts vertical with head at top and two legs "
        "at bottom, normal human anatomy, two arms and two legs each, single helmet on head), with a single "
        "green apple with a red flush floating in mid-air between them. No patches, no letters."
    ),
}

VIDEO_PROMPTS = {
    "03_shot_slow": (
        "Premium Animistry-class 3D cartoon. Same stylised small round Earth with the giant mountain and "
        "brass cannon on the peak from the attached start frame. The brass cannon fires a dark iron cannonball "
        "gently with a small puff of white smoke only (no flame, no spark, no glow). The ball curves down "
        "and lands near the foot of the mountain. Matte daylight only."
    ),
    "04_shot_faster": (
        "Premium Animistry-class 3D cartoon. Same stylised small round Earth with the giant mountain and "
        "brass cannon on the peak from the attached start frame. The brass cannon fires a single dark iron "
        "cannonball faster with a small puff of white smoke only (no flame, no spark, no glow). The ball curves "
        "further around the small globe before landing on the far slope. Matte daylight only."
    ),
    "02_spray_paint_c1": (
        "Premium Animistry-class 3D cartoon. From the side of the same pale plaster wall with the small dark "
        "paint spot and the wider pale patch four times as large, the hands holding the brass sprayers step "
        "back slightly in warm daylight. Hands and sleeves only; no face, head or profile ever enters the frame."
    ),
    "02_spray_paint_c2": (
        "Premium Animistry-class 3D cartoon. The camera tracks smoothly across the pale plaster wall in warm "
        "daylight from the small dark spot of paint to the wider pale patch four times as large beside it. "
        "Hands and sleeves at the edges only; no face or head ever enters the frame."
    ),
    "05_iss_orbit": (
        "Premium Animistry-class 3D cartoon. The generic space station silhouette with no flags, logos or "
        "letters glides smoothly forward and sideways along its curved orbital path high above the slowly "
        "rotating blue Earth. No Moon passes in front of Earth, no glowing lines."
    ),
    "06_iss_apple": (
        "Premium Animistry-class 3D cartoon. Inside the plain station cabin with handrails, the two upright "
        "astronauts in plain white suits with gold visors down drift gently in zero gravity while the green "
        "apple with a red flush floats and turns slowly between them. Both astronauts remain upright with "
        "normal human anatomy, one helmet each and two legs each."
    ),
    "08_cup_and_planets_c1": (
        "Premium Animistry-class 3D cartoon. On the wooden table beside the matte painted card of planets on "
        "ink curves around a painted Sun, the dry terracotta cup tips past the edge of the table and falls "
        "downward out of frame while the camera holds on the table edge and the painted solar system card in "
        "warm daylight. No liquid, no glow."
    ),
}

RETAKE_IDS = list(PARENT_STILL_REUSE.keys()) + list(REGEN_STILL_PROMPTS.keys())


def prep_retakes() -> None:
    log = base.load_log()
    all_rows = {p["id"]: p for p in base.boards()}
    for pid in RETAKE_IDS:
        plate = all_rows[pid]
        old = log["takes"].get(pid) or {}
        if old.get("status") == "REDO":
            continue
        prior = int(old.get("prior_credits_used") or 0) + int(old.get("credits_used") or base.TRY1[plate["quality"]])
        take_no = int(old.get("take") or 1) + 1
        s_dest = base.still_dest(plate)
        v_dest = base.video_dest(plate)
        for p_del in (s_dest.with_suffix(".armed.png"), v_dest):
            if p_del.exists():
                p_del.unlink()
        if pid in PARENT_STILL_REUSE:
            src = PARENT_STILL_REUSE[pid]
            if not src.exists():
                raise SystemExit(f"Missing parent still {src} for {pid}")
            s_dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, s_dest)
            print(f"Prepared {pid}: copied parent still {src.name} -> {s_dest.name} (take {take_no}, prior={prior})")
        else:
            if s_dest.exists():
                s_dest.unlink()
            print(f"Prepared {pid}: cleared still for fresh still+I2V (take {take_no}, prior={prior})")
        log["takes"][pid] = {
            "plate": pid,
            "part": plate["_part"],
            "tranche": 1,
            "take": take_no,
            "prior_credits_used": prior,
            "quality": plate["quality"],
            "status": "REDO",
        }
    base.save_log(log)


_orig_still_prompt = base.still_prompt
_orig_video_prompt = base.video_prompt


def _custom_still_prompt(still, plate: dict, extra_suffix: str = "") -> str:
    pid = plate["id"]
    if pid in REGEN_STILL_PROMPTS:
        p_copy = dict(plate)
        p_copy["prompt"] = REGEN_STILL_PROMPTS[pid]
        return _orig_still_prompt(still, p_copy, extra_suffix=extra_suffix)
    return _orig_still_prompt(still, plate, extra_suffix=extra_suffix)


def _custom_video_prompt(plate: dict, extra_suffix: str = "") -> str:
    pid = plate["id"]
    if pid in VIDEO_PROMPTS:
        p_copy = dict(plate)
        p_copy["prompt"] = VIDEO_PROMPTS[pid]
        return _orig_video_prompt(p_copy, extra_suffix=extra_suffix)
    return _orig_video_prompt(plate, extra_suffix=extra_suffix)


base.still_prompt = _custom_still_prompt
base.video_prompt = _custom_video_prompt


if __name__ == "__main__":
    prep_retakes()
    sys.argv = [sys.argv[0], "--until-part", "05"]
    raise SystemExit(base.main())
