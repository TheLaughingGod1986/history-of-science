#!/usr/bin/env python3
"""Assemble HOS 002 Part 01 rough v05 + copy to iCloud HOS UAT."""
from pathlib import Path
import runpy
import shutil
import subprocess

runpy.run_path(str(Path(__file__).resolve().parent / "_assemble_part01_rough_v04.py"))
PROJ = Path(__file__).resolve().parents[1]
src = PROJ / "09_Final-Export/hos_002_part01_rough_v04.mp4"
dst = PROJ / "09_Final-Export/hos_002_part01_rough_v05.mp4"
ICLOUD = Path("/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/HOS UAT")
if src.exists():
    shutil.copy2(src, dst)
    print(f"COPIED → {dst.name}", flush=True)
if dst.exists() and ICLOUD.parent.exists():
    ICLOUD.mkdir(parents=True, exist_ok=True)
    cloud = ICLOUD / dst.name
    subprocess.run(["cp", "-f", str(dst), str(cloud)], check=False)
    print(f"ICLOUD {cloud}", flush=True)
