#!/usr/bin/env python3
"""Part 04 Gemini Veo I2V remint v18 — Ben OVERRIDE FAIL plates.

Uses painted sharp v18 starts as I2V start frames (via orbit_ref=).
If 429 RESOURCE_EXHAUSTED — stop and report credit blocker.
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
RAW = PROJ / "04_Generated-Clips/part04/raw/v18_fast"
META = PROJ / "07_Edit-Project/part04_mint_gemini_v18_meta.json"
STARTS = PROJ / "04_Generated-Clips/part04/refs/v18_start_frames"
ENV = Path(__file__).resolve().parent / ".env"
MODEL = os.environ.get("ORBIT_VEO_MODEL", "veo-3.1-generate-preview")
ALT_MODELS = [
    MODEL,
    "veo-3.1-lite-generate-preview",
    "veo-3.1-fast-generate-preview",
]
PARENT_SHA = "e4cc41d8cf050f6726e6b3d5cbbbff10285656c588f3a758b4a29e1ec1f998fd"

STYLE = (
    "Finished Animistry-class stylised 3D cartoon (NOT photoreal). "
    "ONE continuous 1869 chemist night desk. Continuous real gentle camera motion. "
    "Silent. No Orbit. No Ken Burns still."
)
LOCK = (
    "CRITICAL: ZERO horizontal ghost doubles; ZERO double-exposure; "
    "ONE soft Empty Chairs panel (no double edge); clean warm lamp (no lava/jagged white); "
    "Explorer if present: finished wavy crown, NO face-cloud blot, NO black hole dots, gold glasses."
)

PROMPTS = {
    "06_explorer_leaves_gap": (
        f"{STYLE} {LOCK} IMAGE-TO-VIDEO from attached start. Explorer 3/4 back at desk, "
        "finished crown, clean written cards, clean lamp. Subtle settle."
    ),
    "10_family_before_weight": (
        f"{STYLE} {LOCK} IMAGE-TO-VIDEO from attached start. FAMILY FIRST: sharp H/C/N/O cards, "
        "clean lamp, one soft panel. Subtle settle."
    ),
    "11_publish_gaps": (
        f"{STYLE} {LOCK} IMAGE-TO-VIDEO from attached start. PUBLISH THE GAPS: sharp grid/flasks/"
        "lamp — zero ghost doubles. Subtle settle."
    ),
    "11b_wait_and_hunt": (
        f"{STYLE} {LOCK} IMAGE-TO-VIDEO from attached start. Wait-and-hunt: grid with holes, "
        "flasks, soft lamp — zero ghosts. Subtle hold."
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
    start = STARTS / f"{pid}_start_v18.jpg"
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
    # Prefer venv python if this interpreter lacks google.genai
    try:
        import google.genai  # noqa: F401
    except ImportError:
        raise SystemExit(
            "missing google.genai — run with /tmp/hos_v18_venv/bin/python "
            "and PYTHONPATH to 04_Audio/tools"
        )

    client = veo.make_client(ENV)
    meta: dict = {
        "engine": "gemini-api-veo",
        "models_tried": [],
        "parent_v17_sha": PARENT_SHA,
        "bible_main": "25bdefd",
        "only": order,
        "plates": [],
        "status": "running",
        "updated": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }
    META.write_text(json.dumps(meta, indent=2) + "\n")

    for pid in order:
        dest = RAW / f"{pid}_v18.GEMINI_TRY.mp4"
        ok = False
        last_err = ""
        for model in ALT_MODELS:
            meta["models_tried"] = list(dict.fromkeys(meta["models_tried"] + [model]))
            try:
                info = mint_one(client, pid, dest, model)
                meta["plates"].append({"plate": pid, **info})
                META.write_text(json.dumps(meta, indent=2) + "\n")
                print(json.dumps(info, indent=2), flush=True)
                ok = True
                break
            except Exception as e:
                last_err = str(e)
                print(f"  FAIL {model}: {e}", flush=True)
                meta.setdefault("errors", []).append({"plate": pid, "model": model, "error": last_err})
                META.write_text(json.dumps(meta, indent=2) + "\n")
                if "429" in last_err or "RESOURCE_EXHAUSTED" in last_err:
                    meta["credit_blocker"] = last_err
                    meta["status"] = "CREDIT_BLOCKER"
                    META.write_text(json.dumps(meta, indent=2) + "\n")
                    print("CREDIT BLOCKER — stop Gemini", flush=True)
                    return
        if not ok:
            print(f"  plate {pid} exhausted models: {last_err}", flush=True)

    meta["status"] = "done" if meta["plates"] else "no_accepts"
    META.write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta, indent=2), flush=True)


if __name__ == "__main__":
    main()
