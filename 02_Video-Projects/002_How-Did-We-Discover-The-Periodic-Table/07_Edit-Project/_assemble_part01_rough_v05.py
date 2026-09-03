#!/usr/bin/env python3
"""Assemble HOS 002 Part 01 rough v05."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).resolve().parent / "_assemble_part01_rough_v04.py"))
# v04 builder writes v04; copy to v05
PROJ = Path(__file__).resolve().parents[1]
src = PROJ / "09_Final-Export/hos_002_part01_rough_v04.mp4"
dst = PROJ / "09_Final-Export/hos_002_part01_rough_v05.mp4"
if src.exists():
    import shutil
    shutil.copy2(src, dst)
    print(f"COPIED → {dst.name}", flush=True)
