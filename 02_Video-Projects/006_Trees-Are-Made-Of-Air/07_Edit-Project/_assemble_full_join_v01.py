#!/usr/bin/env python3
"""HOS 006 full_join_v01: stream-copy the five QA-passed part roughs.

No re-encode, so each part's passed picture is unchanged. The voice is
already in each rough. There is no 05_Music bed (credit hold until 30 Oct;
a new bed needs the Chief's OK), so this join does not lay one.

Parts (sha prefixes checked by the caller):
  01 v01  69974f305a34
  02 v03  7ef9c117b295   (J0290)
  03 v03  1067c0661b8e   (J0266)
  04 v02  e639e9bbe2b6   (J0266)
  05 v01  b3ca1afb9cd9
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

MEDIA = Path(
    "/Users/benjaminoats/YouTube/hos-006-trees/02_Video-Projects"
    "/006_Trees-Are-Made-Of-Air/07_Edit-Project/_precheck"
)
OUT = Path("/private/tmp/j0312-join")
DESK = Path(__file__).resolve().parent / "_desk" / "006" / "full_join_v01"

PARTS = [
    {
        "part": 1,
        "mp4": MEDIA / "part01_rough_v01/hos_006_part01_rough_v01.mp4",
        "cuts": MEDIA / "part01_rough_v01/cuts_part01_rough_v01.json",
        "pool": MEDIA / "part01_rough_v01/pool_part01_rough_v01.json",
        "sha12": "69974f305a34",
    },
    {
        "part": 2,
        "mp4": MEDIA / "part02_rough_v03/hos_006_part02_rough_v03.mp4",
        "cuts": Path("/tmp/p2cuts.json"),
        "pool": Path("/tmp/p2pool.json"),
        "sha12": "7ef9c117b295",
    },
    {
        "part": 3,
        "mp4": MEDIA / "part03_rough_v03/hos_006_part03_rough_v03.mp4",
        "cuts": MEDIA / "part03_rough_v03/cuts_part03_rough_v03.json",
        "pool": MEDIA / "part03_rough_v03/pool_part03_rough_v03.json",
        "sha12": "1067c0661b8e",
    },
    {
        "part": 4,
        "mp4": MEDIA / "part04_rough_v02/hos_006_part04_rough_v02.mp4",
        "cuts": MEDIA / "part04_rough_v02/cuts_part04_rough_v02.json",
        "pool": MEDIA / "part04_rough_v02/pool_part04_rough_v02.json",
        "sha12": "e639e9bbe2b6",
    },
    {
        "part": 5,
        "mp4": MEDIA / "part05_rough_v01/hos_006_part05_rough_v01.mp4",
        "cuts": MEDIA / "part05_rough_v01/cuts_part05_rough_v01.json",
        "pool": MEDIA / "part05_rough_v01/pool_part05_rough_v01.json",
        "sha12": "b3ca1afb9cd9",
    },
]


def sha256(path: Path) -> str:
    out = subprocess.check_output(["shasum", "-a", "256", str(path)], text=True)
    return out.split()[0]


def duration(path: Path) -> float:
    out = subprocess.check_output(
        [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "csv=p=0", str(path),
        ],
        text=True,
    )
    return float(out.strip())


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    DESK.mkdir(parents=True, exist_ok=True)
    cuts_out = []
    pool_out = []
    meta_parts = []
    offset = 0.0
    lines = []
    for spec in PARTS:
        digest = sha256(spec["mp4"])
        if not digest.startswith(spec["sha12"]):
            raise SystemExit(f"part {spec['part']} sha {digest[:12]} != {spec['sha12']}")
        dur = duration(spec["mp4"])
        cuts = json.loads(spec["cuts"].read_text())
        pool = json.loads(spec["pool"].read_text())
        if not isinstance(pool, list):
            raise SystemExit(f"part {spec['part']} pool is not a list")
        for c in cuts:
            row = dict(c)
            row["part"] = spec["part"]
            row["timeline_in"] = c["timeline_in"] + offset
            row["timeline_out"] = c["timeline_out"] + offset
            if "film_t" in row:
                row["film_t"] = c["film_t"] + offset
            cuts_out.append(row)
        for e in pool:
            item = dict(e)
            item["part"] = spec["part"]
            pool_out.append(item)
        lines.append(f"file '{spec['mp4']}'")
        meta_parts.append({
            "part": spec["part"],
            "file": str(spec["mp4"]),
            "sha256": digest,
            "duration_s": dur,
            "offset_s": offset,
            "cuts": len(cuts),
        })
        offset += dur

    list_path = OUT / "concat.txt"
    list_path.write_text("\n".join(lines) + "\n")
    joined = OUT / "hos_006_full_join_v01.mp4"
    subprocess.check_call(
        [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(list_path),
            "-c", "copy", "-movflags", "+faststart", str(joined),
        ]
    )
    joined_dur = duration(joined)
    joined_sha = sha256(joined)
    (DESK / "cuts_full_join_v01.json").write_text(json.dumps(cuts_out, indent=2) + "\n")
    (DESK / "pool_full_join_v01.json").write_text(json.dumps(pool_out, indent=2) + "\n")
    meta = {
        "file": str(joined),
        "sha256": joined_sha,
        "duration_s": joined_dur,
        "parts_sum_s": offset,
        "cuts": len(cuts_out),
        "bed": None,
        "bed_note": "No 05_Music bed exists. Credit hold until 30 Oct: no new bed without the Chief's OK. VO is the audio already in each passed rough.",
        "parts": meta_parts,
    }
    (DESK / "JOIN_META_v01.json").write_text(json.dumps(meta, indent=2) + "\n")
    (OUT / "JOIN_META_v01.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps({k: meta[k] for k in ("sha256", "duration_s", "parts_sum_s", "cuts")}, indent=2))


if __name__ == "__main__":
    main()
