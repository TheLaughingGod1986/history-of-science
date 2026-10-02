#!/usr/bin/env python3
"""Land the 004 back-catalogue cover v02 (desk PR #180 comment 5950838060).

Picture only: scene `hos_004_backcat_scene_v02a.jpg` (from `_repaint_backcat_004_scene_v02.py`), the v01 lettering
asset, layout and stacking unchanged (`_land_backcat_covers_v01.py`). Then thumb_preview.py short, and
style_sheet.py short with the 002 cover v01 beside it. Nothing to Studio.
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("land_v01", HERE / "_land_backcat_covers_v01.py")
v01 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v01)

OUT = HERE / "covers_backcat_v02"


def main() -> int:
    OUT.mkdir(exist_ok=True)
    cover = dict(v01.COVERS["004_gold_foil"])
    assets = cover["dir"] / "_assets"
    (OUT / "_assets").mkdir(exist_ok=True)
    for name in ("hos_004_backcat_scene_v02a.jpg", cover["letters"]):
        (OUT / "_assets" / name).write_bytes((assets / name).read_bytes())
    cover.update(dir=OUT, name="hos_004_backcat_gold_foil_cover_v02.jpg", scene="hos_004_backcat_scene_v02a.jpg")
    m = v01.build(v01.load_005(), "004_gold_foil", cover)
    other = v01.ROOT / json.loads((v01.COVERS["002_four_elements"]["dir"] / "COVERS_INDEX_BACKCAT_v01.json")
                                  .read_text())["covers"]["002_four_elements"]["file"]
    sheet = OUT / "hos_backcat_nov_covers_v02_style_sheet.jpg"
    subprocess.run([sys.executable, str(v01.TOOLS / "style_sheet.py"), "short", str(v01.ROOT / m["file"]), str(other),
                    "--out", str(sheet)], check=True)
    index = {"version": "covers_backcat_v02", "task": "PR #180 comment 5950838060",
             "change": "004 scene repainted: shell rebounding out, foil intact with a small dent, no tear or paper; "
                       "lettering, layout and Explorer unchanged",
             "covers": {"004_gold_foil": m, "002_four_elements": {"file": str(other.relative_to(v01.ROOT)),
                                                                  "unchanged": "covers_backcat_v01"}},
             "style_sheet": str(sheet.relative_to(v01.ROOT))}
    (OUT / "COVERS_INDEX_BACKCAT_v02.json").write_text(json.dumps(index, indent=2) + "\n")
    print("  style sheet", index["style_sheet"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
