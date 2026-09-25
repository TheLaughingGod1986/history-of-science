#!/usr/bin/env python3
"""Join LOCKED HOS 002 Parts 01–05 → full v01. Concat only. No remint.

Hard cuts. No branded intro. Part 05 already carries the house cream-on-brown
end card — do not add a second card. P02 is yuvj444p and P05 is yuv444p, so
every parent is re-encoded to 1920x1080 yuv420p High before concat.

Not LOCKED. Scores → CoS. Do not declare Ben PASS. Do not upload.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
EXP = PROJ / "09_Final-Export"
ICLOUD = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT"
OUT = EXP / "hos_002_periodic_table_full_v01.mp4"
NOTES = EXP / "FULL_V01_JOIN_NOTES.md"
WATCH = PROJ / "07_Edit-Project/WATCH_full_v01.txt"

LOCK = [
    {
        "id": "01",
        "name": "hos_002_part01_rough_v14.mp4",
        "sha": "d903cf7ca1789dcfc1a3703b9215564b3a0d306d0ea1dbf7c2a974888fa92781",
    },
    {
        "id": "02",
        "name": "hos_002_part02_rough_v06.mp4",
        "sha": "799086795d62f159930bd00db638ea2de0e02a299d8c9d50c8eed3d482e89529",
    },
    {
        "id": "03",
        "name": "hos_002_part03_rough_v09.mp4",
        "sha": "30060612a00d628998008c9946b8e25319b56f3b9e5613b537c5d2be989bbe4e",
    },
    {
        "id": "04",
        "name": "hos_002_part04_rough_v25.mp4",
        "sha": "e78027c0c58abe9284f7b85de693a08caabd3ad8ee45b64624eadd0329942bb1",
    },
    {
        "id": "05",
        "name": "hos_002_part05_rough_v01.mp4",
        "sha": "8dcb06b596318a7283210928fbb0e78f6f89c7db5d200b8edeefbaa9b5522ec4",
    },
]

# P05 VO 144.160s; card xfade starts 0.35s before VO end.
P05_VO = 144.160
P05_CARD_XFADE = 0.35
P05_CARD_HOLD = 3.5

ENC = [
    "-c:v", "libx264", "-pix_fmt", "yuv420p",
    "-profile:v", "high", "-level", "4.1",
    "-preset", "fast", "-crf", "18", "-r", "24",
    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
    "-movflags", "+faststart",
]


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def probe_dur(p: Path) -> float:
    r = subprocess.run(
        [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(p),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(r.stdout.strip())


def ff(*args: str) -> None:
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *args], check=True)


def main() -> None:
    paths: list[Path] = []
    durs: list[float] = []
    print("HASH CHECK", flush=True)
    for item in LOCK:
        exp = EXP / item["name"]
        if not exp.exists():
            raise SystemExit(f"STOP: missing {exp}")
        got = sha256(exp)
        if got != item["sha"]:
            raise SystemExit(f"STOP: hash mismatch {item['name']} {got}")
        dur = probe_dur(exp)
        print(f"  OK {item['id']} {dur:.3f}s {exp.stat().st_size} {got}", flush=True)
        paths.append(exp)
        durs.append(dur)

    work = Path(tempfile.mkdtemp(prefix="hos_002_join_v01_"))
    print(f"WORK {work}", flush=True)
    segs: list[Path] = []
    for item, src, dur in zip(LOCK, paths, durs):
        dest = work / f"p{item['id']}.mp4"
        print(f"ENCODE {item['id']}", flush=True)
        ff(
            "-i", str(src),
            "-vf", "fps=24,scale=1920:1080:flags=lanczos,format=yuv420p,setsar=1",
            "-t", f"{dur:.6f}",
            *ENC,
            str(dest),
        )
        segs.append(dest)

    lst = work / "concat.txt"
    lst.write_text("".join(f"file '{p}'\n" for p in segs))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    ff(
        "-f", "concat", "-safe", "0", "-i", str(lst),
        "-c", "copy", "-movflags", "+faststart",
        str(OUT),
    )

    splice = [0.0]
    for d in durs:
        splice.append(splice[-1] + d)
    card_in = splice[4] + P05_VO - P05_CARD_XFADE
    card_land = card_in + P05_CARD_XFADE
    digest = sha256(OUT)
    dur = probe_dur(OUT)
    size = OUT.stat().st_size
    print(f"SAVED {OUT}", flush=True)
    print(f"SIZE {size}", flush=True)
    print(f"SHA256 {digest}", flush=True)
    print(f"DUR {dur:.3f}", flush=True)
    for i in range(5):
        print(f"SPLICE_{i+1}{i+2 if i < 4 else '_OUT'} {splice[i]:.3f}", flush=True)
    print(f"CARD_IN {card_in:.3f}", flush=True)
    print(f"CARD_LAND {card_land:.3f}", flush=True)

    watch = (
        "WATCH THIS FILE ONLY (HOS 002 full v01 — How Did We Discover the Periodic Table?):\n"
        f"  {OUT.name}\n"
        f"  iCloud: HOS UAT/{OUT.name}\n\n"
        f"sha256={digest}\n"
        f"duration={dur:.3f}\n"
        f"bytes={size}\n"
        "Hard concat of locked Parts 01–05. No branded intro. One house card (from P05).\n"
        "Not LOCKED. Scores → CoS. Do NOT declare PASS. No Ben ping. Do not upload.\n"
    )
    WATCH.write_text(watch)
    notes = f"""# HOS 002 full v01 — join notes (UAT pack, not ship lock)

**Cut:** `{OUT.name}`
**sha256:** `{digest}`
**Duration:** {dur:.3f} s · **Size:** {size} B
**UAT:** CoS watch only. Do **not** declare Ben PASS. Do **not** upload.

**Parents LOCKED (hash-checked, not reminted):**

| Part | File | sha256 | duration |
|---|---|---|---:|
| 01 | `{LOCK[0]['name']}` | `{LOCK[0]['sha']}` | {durs[0]:.3f} |
| 02 | `{LOCK[1]['name']}` | `{LOCK[1]['sha']}` | {durs[1]:.3f} |
| 03 | `{LOCK[2]['name']}` | `{LOCK[2]['sha']}` | {durs[2]:.3f} |
| 04 | `{LOCK[3]['name']}` | `{LOCK[3]['sha']}` | {durs[3]:.3f} |
| 05 | `{LOCK[4]['name']}` | `{LOCK[4]['sha']}` | {durs[4]:.3f} |

| Beat | Time |
|---|---:|
| P01 start | {splice[0]:.3f} |
| P02 start | {splice[1]:.3f} |
| P03 start | {splice[2]:.3f} |
| P04 start | {splice[3]:.3f} |
| P05 start | {splice[4]:.3f} |
| End-card dissolve | {card_in:.3f} |
| End card on | {card_land:.3f} |
| Film out | {dur:.3f} |

Hard cuts only. No freeze-pad. P05 already holds the cream-on-brown card
(`History of Science` / `DISCOVERY. WONDER. PROOF.`). Subscribe = Studio only.

Builder: `07_Edit-Project/_join_hos_002_full_v01.py`
"""
    NOTES.write_text(notes)

    meta = {
        "file": OUT.name,
        "sha256": digest,
        "duration": dur,
        "bytes": size,
        "parents": [
            {**item, "duration": d, "offset": splice[i]}
            for i, (item, d) in enumerate(zip(LOCK, durs))
        ],
        "card_in": card_in,
        "card_land": card_land,
        "status": "UAT",
        "locked": False,
        "upload": False,
    }
    (PROJ / "07_Edit-Project/part_full_v01_land_meta.json").write_text(
        json.dumps(meta, indent=2) + "\n"
    )

    ICLOUD.mkdir(parents=True, exist_ok=True)
    subprocess.run(["cp", "-f", str(OUT), str(ICLOUD / OUT.name)], check=True)
    (ICLOUD / WATCH.name).write_text(watch)
    (ICLOUD / NOTES.name).write_text(notes)
    print(f"ICLOUD {ICLOUD / OUT.name}", flush=True)


if __name__ == "__main__":
    main()
