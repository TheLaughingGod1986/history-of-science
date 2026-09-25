#!/usr/bin/env python3
"""Gemini Veo I2V fallback for Part 03 v06 plate 03_method_pamphlet.

Uses Ben FAIL marked desk still as start frame (props lock).
Prefer Flow Ultra first; this path only when Flow I2V attach is broken.
No Ken Burns. No Omni.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))

import orbit_gemini_veo as veo  # noqa: E402

PROJ = Path(__file__).resolve().parents[1]
STILL = PROJ / "04_Generated-Clips/part03/refs/v06_stills/03_FAIL_desk_marked_i2v.jpg"
OUT = PROJ / "04_Generated-Clips/part03/raw/v06_fast/03_method_pamphlet_v06.mp4"
META = Path(__file__).resolve().parent / "part03_mint_gemini_v06_meta.json"
ENV = Path(__file__).resolve().parent / ".env"

PROMPT = (
    "IMAGE-TO-VIDEO from the attached start frame. KEEP this EXACT Karlsruhe "
    "congress-hall DNA (honey oak panels, arched windows, wooden desks/benches). "
    "Continuous soft camera settle on the desk. PROPS LOCK: keep the sparse "
    "phone-readable dark-ink marks already on the upright cream sheet — H 1, "
    "O 16, C 12 — and the soft N 14 on the top of the stack. MOST sheets stay "
    "completely BLANK. Do NOT invent equations, tables, walls of text, or new "
    "numbers. Do NOT morph H 1 into H 16. Continuous motion. Silent. No people. "
    "No Explorer. No Orbit. Animistry-class stylised 3D cartoon (NOT photoreal). "
    "HARD REJECT: blank papers; chicken-scratch; formula walls; room swap; "
    "green theatre chairs redesign; Ken Burns still."
)


def main() -> None:
    if not STILL.exists():
        raise SystemExit(f"missing start frame {STILL}")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    if OUT.exists():
        OUT.unlink()
    model = os.environ.get(
        "ORBIT_VEO_MODEL",
        "veo-3.1-lite-generate-preview",
    )
    print(f"Gemini I2V model={model} start={STILL.name} → {OUT.name}", flush=True)
    client = veo.make_client(ENV)
    prompt = PROMPT + "\n" + veo.CG_SILENT_AUDIO_BLOCK
    try:
        meta = veo.generate_clip(
            client,
            prompt,
            OUT,
            model=model,
            orbit_ref=STILL,
            duration_seconds=8,
            aspect_ratio="16:9",
            resolution="720p",
        )
    except Exception as e:
        err = str(e)
        print(f"Gemini FAIL: {err[:500]}", flush=True)
        META.write_text(json.dumps({"status": "fail", "error": err[:800]}, indent=2))
        # Retry standard preview if lite exhausted
        if "429" in err or "RESOURCE_EXHAUSTED" in err:
            alt = "veo-3.1-generate-preview"
            print(f"retry model={alt}", flush=True)
            try:
                meta = veo.generate_clip(
                    client,
                    prompt,
                    OUT,
                    model=alt,
                    orbit_ref=STILL,
                    duration_seconds=8,
                )
            except Exception as e2:
                META.write_text(
                    json.dumps({"status": "fail", "error": str(e2)[:800]}, indent=2)
                )
                raise SystemExit(f"STOP: Gemini exhausted ({e2})") from e2
        else:
            raise SystemExit(f"STOP: Gemini failed ({e})") from e
    meta["status"] = "ok"
    meta["start_frame"] = str(STILL)
    meta["out"] = str(OUT)
    META.write_text(json.dumps(meta, indent=2))
    print(json.dumps(meta, indent=2), flush=True)
    print(f"SAVED {OUT} bytes={OUT.stat().st_size}", flush=True)


if __name__ == "__main__":
    main()
