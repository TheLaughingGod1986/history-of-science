#!/usr/bin/env python3
"""Part 04 remint v16 via Gemini Veo I2V — LATE SHOTS SHARP.

Flow Ultra create may start, but gallery harvest is broken again (same as v13).
Gemini I2V fallback from sharp v16 start frames.

Remint ONLY: 10_family_before_weight, 11_publish_gaps, 11b_wait_and_hunt.
KEEP from v15: Explorer 06, 09, 09b CLEAN LIGHT.

Scores → CoS. Do not declare PASS. Do not ping Ben.
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
RAW = PROJ / "04_Generated-Clips/part04/raw/v16_fast"
META = PROJ / "07_Edit-Project/part04_mint_gemini_v16_meta.json"
STARTS = PROJ / "04_Generated-Clips/part04/refs/v16_start_frames"
ENV = Path(__file__).resolve().parent / ".env"
MODEL = os.environ.get("ORBIT_VEO_MODEL", "veo-3.1-generate-preview")
PARENT_SHA = "cd7a57b2979478a34ac7cc5fe5639aa156ae603b437674ccd724ab3fe994748c"

STYLE = (
    "Finished Animistry-class stylised 3D cartoon (NOT photoreal, NOT live-action). "
    "ONE continuous 1869 chemist desk: honey wood, soft warm desk-lamp glow, cream "
    "element cards with readable ink letters (H/C/O/N/Li — NEVER blank), leather books, "
    "lab vessels, indoor wood bookcase. Continuous real camera/object motion the whole "
    "clip. Silent. No Orbit robot. No Ken Burns still."
)
LAMP = (
    "CRITICAL CLEAN LIGHT: soft warm desk-lamp glow ONLY. ZERO flames, ZERO lava drip, "
    "ZERO molten orange leak, ZERO smoke, ZERO sparks. Empty Chairs glow = soft "
    "rectangular panel glow ONLY — never flames."
)
SHARP = (
    "CRITICAL LATE SHOTS SHARP: every frame finished and crisp. ZERO ghost doubles, "
    "ZERO motion-ghost trailing cards, ZERO double-exposure edges, ZERO unfinished "
    "left-half pixelation / blocky mush / jagged white cutouts. Prefer gentle slow "
    "motion so cards stay single-edged and readable."
)
CARDS = (
    "CRITICAL WRITTEN CARDS: every visible card face shows readable hand-ink "
    "H/C/O/N/Li marks with small numbers. NEVER blank cream tops."
)

PROMPTS = {
    "10_family_before_weight": (
        f"{STYLE} {LAMP} {SHARP} {CARDS} "
        "IMAGE-TO-VIDEO from the attached start frame. FAMILY FIRST beat: four sharp "
        "cream floating cards H/1, C/12, N/14, O/16 — each card SINGLE sharp edges only, "
        "NO ghost trail especially on the N card. Soft warm lamp + soft rectangular Empty "
        "Chairs panel glow. Gentle settle / tiny drift. No Explorer. Indoor wood/bookcase."
    ),
    "11_publish_gaps": (
        f"{STYLE} {LAMP} {SHARP} {CARDS} "
        "IMAGE-TO-VIDEO from the attached start frame. PUBLISH THE GAPS beat: sharp "
        "finished night desk with flat grid sheet, flasks, cards, magnifier. Every prop "
        "SINGLE sharp edges — never full-scene ghost doubles. Left half fully finished/"
        "sharp — never pixelated unfinished mush. Continuous subtle settle. No Explorer."
    ),
    "11b_wait_and_hunt": (
        f"{STYLE} {LAMP} {SHARP} {CARDS} "
        "IMAGE-TO-VIDEO from the attached start frame. Wait-and-hunt beat: published flat "
        "grid with empty holes, flasks, soft lamp. Whole frame finished and sharp — zero "
        "left-half pixel mush, zero ghost doubles. Continuous subtle hold/push. No Explorer."
    ),
}

DEFAULT_ONLY = tuple(PROMPTS.keys())


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


def mint_one(client, pid: str, dest: Path) -> dict:
    start = STARTS / f"{pid}_start_v16.jpg"
    if not start.exists() or start.stat().st_size < 20_000:
        raise SystemExit(f"missing start frame {start}")
    prompt = PROMPTS[pid] + "\n" + veo.CG_SILENT_AUDIO_BLOCK
    if dest.exists():
        dest.unlink()
    print(f"  I2V start={start.name} model={MODEL}", flush=True)
    t0 = time.time()
    meta = veo.generate_clip(
        client,
        prompt,
        dest,
        model=MODEL,
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
            "model": MODEL,
        }
    )
    return meta


def main() -> None:
    only = set(sys.argv[1:]) if len(sys.argv) > 1 else set(DEFAULT_ONLY)
    order = [pid for pid in DEFAULT_ONLY if pid in only]
    if not order:
        raise SystemExit(f"no plates matched {sorted(only)}")

    RAW.mkdir(parents=True, exist_ok=True)
    client = veo.make_client(ENV)

    meta: dict = {
        "engine": "gemini-api-veo",
        "model": MODEL,
        "parent_v15_sha": PARENT_SHA,
        "bible_main": "25bdefd",
        "reason": "Flow UI generate OK but gallery harvest broken; Gemini I2V fallback",
        "flow_account_target": "benoats@googlemail.com",
        "only": order,
        "plates": [],
    }
    if META.exists():
        try:
            prev = json.loads(META.read_text())
            meta["plates"] = prev.get("plates", [])
        except Exception:
            pass
    by_id = {p["id"]: p for p in meta.get("plates", []) if "id" in p}

    print(
        f"Gemini Veo remint v16 model={MODEL} only={order} parent={PARENT_SHA[:12]}…",
        flush=True,
    )
    for pid in order:
        dest = RAW / f"{pid}_v16.mp4"
        if dest.exists() and dest.stat().st_size >= 400_000:
            try:
                d = probe(dest)
                if 5.5 <= d <= 20:
                    print(f"SKIP {pid} ({d:.2f}s)", flush=True)
                    by_id[pid] = {
                        "id": pid,
                        "status": "exists",
                        "out": str(dest),
                        "duration": d,
                        "sha256": sha256(dest),
                    }
                    continue
            except Exception:
                pass
        print(f"\n=== {pid} ===", flush=True)
        try:
            info = mint_one(client, pid, dest)
            by_id[pid] = {"id": pid, "status": "ok", "out": str(dest), **info}
            print(
                f"OK {pid} {info['duration']:.2f}s {info['bytes']}b "
                f"sha={info['sha256'][:16]}… in {info['seconds']}s",
                flush=True,
            )
        except Exception as exc:
            by_id[pid] = {"id": pid, "status": "fail", "error": str(exc)[:600]}
            print(f"FAIL {pid}: {exc}", flush=True)
            if "429" in str(exc) or "RESOURCE_EXHAUSTED" in str(exc):
                lite = "veo-3.1-lite-generate-preview"
                print(f"  retry {pid} with {lite}", flush=True)
                try:
                    start = STARTS / f"{pid}_start_v16.jpg"
                    prompt = PROMPTS[pid] + "\n" + veo.CG_SILENT_AUDIO_BLOCK
                    if dest.exists():
                        dest.unlink()
                    t0 = time.time()
                    info = veo.generate_clip(
                        client,
                        prompt,
                        dest,
                        model=lite,
                        duration_seconds=8,
                        aspect_ratio="16:9",
                        resolution="720p",
                        orbit_ref=start,
                    )
                    dur = probe(dest)
                    info.update(
                        {
                            "seconds": round(time.time() - t0, 1),
                            "duration": dur,
                            "bytes": dest.stat().st_size,
                            "sha256": sha256(dest),
                            "start": str(start),
                            "model": lite,
                        }
                    )
                    by_id[pid] = {"id": pid, "status": "ok", "out": str(dest), **info}
                    print(
                        f"OK {pid} lite {info['duration']:.2f}s {info['bytes']}b",
                        flush=True,
                    )
                except Exception as exc2:
                    by_id[pid] = {"id": pid, "status": "fail", "error": str(exc2)[:600]}
                    print(f"FAIL {pid} lite: {exc2}", flush=True)
        meta["plates"] = list(by_id.values())
        meta["updated"] = time.strftime("%Y-%m-%dT%H:%M:%S")
        META.write_text(json.dumps(meta, indent=2) + "\n")

    ok = sum(
        1
        for p in by_id.values()
        if p.get("status") in {"ok", "exists"} and p["id"] in only
    )
    print(f"\nDONE ok={ok} want={len(order)} meta={META}", flush=True)
    if ok < len(order):
        sys.exit(2)


if __name__ == "__main__":
    main()
