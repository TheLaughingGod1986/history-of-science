#!/usr/bin/env python3
"""Part 04 remint v13 via Gemini Veo I2V — CLEAN LIGHT + WRITTEN CARDS.

Flow Ultra generates but gallery harvest is broken. Gemini I2V fallback from
composed v13 start frames.

Remint ONLY: 04_sort_atomic_weight, 05_columns_families, 09_risk_bet, 09b_risk_hold.
KEEP: 06 cleared; 05b/07/08/08b/10 v12; 02b; 07b; P01–P03.
Scores → CoS. Do not declare PASS. Do not ping Ben.
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
import orbit_gemini_veo as veo  # noqa: E402

PROJ = Path(__file__).resolve().parents[1]
RAW = PROJ / "04_Generated-Clips/part04/raw/v13_fast"
META = PROJ / "07_Edit-Project/part04_mint_gemini_v13_meta.json"
STARTS = PROJ / "04_Generated-Clips/part04/refs/v13_start_frames"
ENV = Path(__file__).resolve().parent / ".env"
MODEL = os.environ.get("ORBIT_VEO_MODEL", "veo-3.1-fast-generate-preview")
PARENT_SHA = "175c40a948a24899507266d3f4bccf39f9f51a2906441cae4557bcbd312fe6c2"

STYLE = (
    "Finished Animistry-class stylised 3D cartoon (NOT photoreal, NOT live-action). "
    "ONE continuous 1869 chemist desk: honey wood, soft warm desk-lamp glow, cream "
    "element cards with readable ink letters (H/C/O/N/Li — NEVER blank), leather books, "
    "lab vessels, indoor wood bookcase. Continuous real camera/object motion the whole "
    "clip. Silent. No Orbit robot. No Ken Burns still."
)
LAMP = (
    "CRITICAL CLEAN LIGHT: soft warm desk-lamp glow ONLY. ZERO flames, ZERO white fire "
    "cluster in any chair seat, ZERO leather chair on fire, ZERO smoke wisps from lamp, "
    "ZERO sparks under bulb, ZERO candle. Empty Chairs glow = soft rectangular backrest "
    "glow / vacant-seat light ONLY — never flames."
)
CARDS = (
    "CRITICAL WRITTEN CARDS: every visible card face AND every stack TOP shows readable "
    "hand-ink H/C/O/N/Li/Be marks with small numbers. Stack edges look like paper layers "
    "with marks on tops. Foreground hero cards MUST be written. NEVER blank cream tops."
)

PROMPTS = {
    "04_sort_atomic_weight": (
        f"{STYLE} {LAMP} {CARDS} "
        "IMAGE-TO-VIDEO from the attached start frame. Written cream element cards slide "
        "and sort by atomic weight across the honey wood. Every stack top stays readable. "
        "Soft warm lamp only — no fire, no smoke. Continuous sort motion. Indoor wood/bookcase."
    ),
    "05_columns_families": (
        f"{STYLE} {LAMP} {CARDS} "
        "IMAGE-TO-VIDEO from the attached start frame. Written cream element cards settle "
        "into family columns. Every stack top and flat card stays readable (H/C/O/N/Li). "
        "Soft warm lamp only — no fire, no smoke. Continuous settle motion. Indoor wood/bookcase."
    ),
    "09_risk_bet": (
        f"{STYLE} {LAMP} {CARDS} "
        "IMAGE-TO-VIDEO from the attached start frame. Soft rectangular Empty Chairs "
        "backrest glow on the vacant chair — NEVER white flames in the seat, NEVER smoke "
        "from lamp. Foreground hero cream cards show readable H/C/O/N/Li. Continuous subtle "
        "camera drift. Indoor wood/bookcase."
    ),
    "09b_risk_hold": (
        f"{STYLE} {LAMP} {CARDS} "
        "IMAGE-TO-VIDEO from the attached start frame. Soft rectangular Empty Chairs "
        "backrest glow holds — NEVER white seat fire, NEVER lamp smoke. Written cream cards "
        "stay readable on every face and stack top. Continuous subtle hold. Indoor wood/bookcase."
    ),
}

DEFAULT_ONLY = tuple(PROMPTS.keys())


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
    start = STARTS / f"{pid}_start_v13.jpg"
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
        "parent_v12_sha": PARENT_SHA,
        "reason": "Flow UI generate OK but gallery harvest broken; Gemini I2V fallback",
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
        f"Gemini Veo remint v13 model={MODEL} only={order} parent={PARENT_SHA[:12]}…",
        flush=True,
    )
    for pid in order:
        dest = RAW / f"{pid}_v13.mp4"
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
                    }
                    continue
            except Exception:
                pass
        print(f"\n=== {pid} ===", flush=True)
        try:
            info = mint_one(client, pid, dest)
            by_id[pid] = {"id": pid, "status": "ok", "out": str(dest), **info}
            print(
                f"OK {pid} {info['duration']:.2f}s {info['bytes']}b in {info['seconds']}s",
                flush=True,
            )
        except Exception as exc:
            by_id[pid] = {"id": pid, "status": "fail", "error": str(exc)[:600]}
            print(f"FAIL {pid}: {exc}", flush=True)
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
