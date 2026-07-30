#!/usr/bin/env python3
"""Apply the approved v25 Orbit performance to the narration-aligned v26 bed."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


ROOT = Path("/Users/ben/code/Orbit-YouTube/02_Video-Projects/001_Will-We-Ever-Meet-Aliens")
EDIT = ROOT / "07_Edit-Project"
V25_PATH = EDIT / "_build_v25_final_polish.py"
BED = EDIT / "_render_cache_v26/picture_bed_semantic_v26.mp4"
OUT = ROOT / "09_Final-Export/aliens_broadcast_v26_NARRATION_ALIGNED.mp4"
OUT_PIC = ROOT / "09_Final-Export/aliens_broadcast_v26_NARRATION_ALIGNED_pic.mp4"
PROOF = ROOT / "09_Final-Export/aliens_v26_PROOF_narration-aligned_120s.mp4"
PROOF_PIC = ROOT / "09_Final-Export/_v26_proof_picture.mp4"
MANIFEST = EDIT / "ORBIT_PERFORMANCES_v26.json"


def load_v25():
    spec = importlib.util.spec_from_file_location("orbit_v25_final", V25_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


def main(mode: str) -> None:
    v25 = load_v25()
    compositor = v25.load_base()
    v25.configure(compositor)
    compositor.BED = BED
    compositor.OUT = OUT
    compositor.OUT_PIC = OUT_PIC
    compositor.PROOF = PROOF
    compositor.PROOF_PIC = PROOF_PIC
    compositor.MANIFEST = MANIFEST
    compositor.main(mode)

    data = json.loads(MANIFEST.read_text())
    data.update({
        "version": 26,
        "rule": "approved Orbit performance over sentence-level narration-aligned footage",
        "picture_bed": str(BED),
        "semantic_alignment_report": str(EDIT / "NARRATION_VISUAL_ALIGNMENT_v26.json"),
        "source_version_preserved": 25,
        "output": str(OUT),
    })
    MANIFEST.write_text(json.dumps(data, indent=2))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "proof")
