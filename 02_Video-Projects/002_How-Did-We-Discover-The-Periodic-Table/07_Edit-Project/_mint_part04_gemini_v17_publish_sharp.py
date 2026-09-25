#!/usr/bin/env python3
"""Part 04 remint v17 via Gemini Veo I2V — PUBLISH THE GAPS sharp (11 / 11b).

Fallback when Flow gallery harvest fails. Fresh starts from painted sharp v17 DNA.
Do NOT restore ghosty v01. If 429 RESOURCE_EXHAUSTED — stop and report blocker.

Remint ONLY: 11_publish_gaps, 11b_wait_and_hunt.
KEEP: 10, Explorer 06, 09/09b.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))
import orbit_gemini_veo as veo  # noqa: E402

PROJ = Path(__file__).resolve().parents[1]
RAW = PROJ / "04_Generated-Clips/part04/raw/v17_fast"
META = PROJ / "07_Edit-Project/part04_mint_gemini_v17_meta.json"
STARTS = PROJ / "04_Generated-Clips/part04/refs/v17_start_frames"
ENV = Path(__file__).resolve().parent / ".env"
MODEL = os.environ.get("ORBIT_VEO_MODEL", "veo-3.1-generate-preview")
ALT_MODELS = [
    MODEL,
    "veo-3.1-lite-generate-preview",
    "veo-3.1-fast-generate-preview",
]
PARENT_SHA = "7e083fc440879209bbc69459fbaf21dc29dbfc1f77b370ec92ee931bec82cb3c"

STYLE = (
    "Finished Animistry-class stylised 3D cartoon (NOT photoreal). "
    "ONE continuous 1869 chemist night desk: honey wood, soft warm desk-lamp glow, "
    "flat parchment grid, coloured flasks, magnifier, cream cards, indoor bookcase. "
    "Continuous real camera/object motion. Silent. No Orbit. No Ken Burns still."
)
LAMP = (
    "CRITICAL CLEAN LIGHT: soft warm desk-lamp glow ONLY. ZERO flames, ZERO lava drip, "
    "ZERO molten orange leak, ZERO smoke. Empty Chairs glow = soft rectangular panel ONLY."
)
SHARP = (
    "CRITICAL LATE SHOTS SHARP: every frame finished crisp SINGLE EXPOSURE. "
    "ZERO ghost doubles, ZERO double-exposure edges, ZERO unfinished left-half pixel mush. "
    "ONE solid lamp, ONE solid flask set, ONE solid grid."
)

PROMPTS = {
    "11_publish_gaps": (
        f"{STYLE} {LAMP} {SHARP} "
        "IMAGE-TO-VIDEO from the attached start frame. PUBLISH THE GAPS beat: sharp "
        "finished night desk with flat grid sheet, flasks, cards, magnifier. Every prop "
        "SINGLE sharp edges — never full-scene ghost doubles. Continuous subtle settle."
    ),
    "11b_wait_and_hunt": (
        f"{STYLE} {LAMP} {SHARP} "
        "IMAGE-TO-VIDEO from the attached start frame. Wait-and-hunt beat: published flat "
        "grid with empty holes, flasks, soft lamp. Whole frame finished and sharp — zero "
        "ghost doubles. Continuous subtle hold/push."
    ),
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def probe(path: Path) -> float:
    return float(
        subprocess.check_output(
            [
                "ffprobe", "-v", "error", "-show_entries", "format=duration",
                "-of", "default=nw=1:nk=1", str(path),
            ],
            text=True,
        ).strip()
    )


def mint_one(client, pid: str, dest: Path, model: str) -> dict:
    start = STARTS / f"{pid}_start_v17.jpg"
    if not start.exists() or start.stat().st_size < 20_000:
        raise SystemExit(f"missing start frame {start}")
    prompt = PROMPTS[pid] + "\n" + veo.CG_SILENT_AUDIO_BLOCK
    if dest.exists():
        dest.unlink()
    print(f"  I2V start={start.name} model={model}", flush=True)
    t0 = time.time()
    meta = veo.generate_clip(
        client,
        prompt,
        dest,
        model=model,
        duration_seconds=8,
        aspect_ratio="16:9",
        resolution="720p",
        orbit_ref=start,
    )
    dur = probe(dest)
    if dur < 5.5 or dur > 20:
        raise RuntimeError(f"bad duration {dur}")
    meta.update(
        {
            "seconds": round(time.time() - t0, 1),
            "duration": dur,
            "bytes": dest.stat().st_size,
            "sha256": sha256(dest),
            "start": str(start),
            "model": model,
        }
    )
    return meta


def main() -> None:
    only = set(sys.argv[1:]) if len(sys.argv) > 1 else set(PROMPTS)
    order = [pid for pid in PROMPTS if pid in only]
    if not order:
        raise SystemExit(f"no plates matched {sorted(only)}")

    RAW.mkdir(parents=True, exist_ok=True)
    client = veo.make_client(ENV)
    meta: dict = {
        "engine": "gemini-api-veo",
        "models_tried": [],
        "parent_v16_sha": PARENT_SHA,
        "bible_main": "25bdefd",
        "reason": "Flow harvest fallback — fresh sharp I2V, not v01 restore",
        "only": order,
        "plates": [],
        "status": "running",
        "updated": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }
    META.write_text(json.dumps(meta, indent=2) + "\n")

    for pid in order:
        dest = RAW / f"{pid}_v17.mp4"
        ok = False
        last_err = ""
        for model in ALT_MODELS:
            if model in meta["models_tried"]:
                pass
            else:
                meta["models_tried"].append(model)
            try:
                print(f"  submit model={model} → {dest.name}", flush=True)
                info = mint_one(client, pid, dest, model)
                meta["plates"].append({"id": pid, "status": "ok", **info})
                META.write_text(json.dumps(meta, indent=2) + "\n")
                ok = True
                break
            except Exception as e:
                last_err = str(e)
                print(f"  FAIL {model}: {last_err[:400]}", flush=True)
                meta["plates"].append(
                    {"id": pid, "status": "fail", "model": model, "error": last_err[:800]}
                )
                META.write_text(json.dumps(meta, indent=2) + "\n")
                if "429" in last_err or "RESOURCE_EXHAUSTED" in last_err or "depleted" in last_err.lower():
                    # try next alternate once; if all fail, credit block
                    continue
                # non-credit error — still try next model once
                continue
        if not ok:
            meta["status"] = "credit_or_api_blocked"
            meta["blocker"] = last_err[:800]
            META.write_text(json.dumps(meta, indent=2) + "\n")
            print(f"BLOCKER {pid}: {last_err[:400]}", flush=True)
            raise SystemExit(4)

    meta["status"] = "done"
    meta["updated"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    META.write_text(json.dumps(meta, indent=2) + "\n")
    print("GEMINI MINT DONE", flush=True)


if __name__ == "__main__":
    main()
