#!/usr/bin/env python3
"""Join LOCKED Parts 01–05. Hard cuts. Cream end card. No remint. Not LOCKED."""
from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
REPO = Path(__file__).resolve().parents[3]
EXP = PROJ / "09_Final-Export"
ICLOUD = Path(
    "/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/HOS UAT"
)
ALIGN = PROJ / "02_Voiceover/part05_clean_hands_v01_align.json"
SWIFT = PROJ / "07_Edit-Project/_render_hos_end_card.swift"
OUT = EXP / "hos_001_germs_full_v01.mp4"
HOLD = 0.50
CARD = 3.50
LOCK = [
    {
        "id": "01",
        "name": "hos_001_part01_rough_v21.mp4",
        "sha": None,
    },
    {
        "id": "02",
        "name": "hos_001_part02_rough_v12.mp4",
        "sha": None,
    },
    {
        "id": "03",
        "name": "hos_001_part03_rough_v14.mp4",
        "sha": "a007e1330e85556ab8912f5b5a57f6bb8a69f2ba4ebdce44cb20e4071d9a8428",
    },
    {
        "id": "04",
        "name": "hos_001_part04_rough_v23.mp4",
        "sha": "afe44645ddcfbc649baca52a7720e083d48125d5fd6ca32606b3fb2c951fe763",
    },
    {
        "id": "05",
        "name": "hos_001_part05_rough_v03.mp4",
        "sha": "7aec17d498f65aaa3312f0d8f04e4411fa5debeff5eb646b5effa61d3f54e194",
    },
]


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def probe(p: Path, *entries: str) -> str:
    r = subprocess.run(
        [
            "ffprobe", "-v", "error", "-show_entries", *entries,
            "-of", "default=noprint_wrappers=1:nokey=1", str(p),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return r.stdout.strip()


def probe_dur(p: Path) -> float:
    return float(probe(p, "format=duration"))


def last_phoneme() -> float:
    a = json.loads(ALIGN.read_text())
    chars = a["characters"]
    ends = a["character_end_times_seconds"]
    for i in range(len(chars) - 1, -1, -1):
        if chars[i].strip():
            return float(ends[i])
    raise SystemExit("STOP: no last phoneme in Part 05 align")


def ff(*args: str) -> None:
    subprocess.run(["ffmpeg", "-y", *args], check=True)


def main() -> None:
    paths: list[Path] = []
    durs: list[float] = []
    print("HASH CHECK", flush=True)
    for item in LOCK:
        exp = EXP / item["name"]
        cloud = ICLOUD / item["name"]
        if not exp.exists():
            raise SystemExit(f"STOP: missing {exp}")
        got = sha256(exp)
        if item["sha"] and got != item["sha"]:
            raise SystemExit(f"STOP: hash mismatch {item['name']} {got}")
        if cloud.exists():
            cgot = sha256(cloud)
            if cgot != got:
                raise SystemExit(f"STOP: iCloud hash differs {item['name']}")
        print(f"  OK {item['id']} {got} {exp.stat().st_size}", flush=True)
        paths.append(exp)
        durs.append(probe_dur(exp))
    last = last_phoneme()
    p05_use = last + HOLD
    if p05_use > durs[-1] + 0.02:
        raise SystemExit(f"STOP: last+hold {p05_use:.3f} > part05 {durs[-1]:.3f}")
    print(f"P05 last_phoneme={last:.3f} hold={HOLD:.2f} use={p05_use:.3f}", flush=True)

    splices = []
    acc = 0.0
    uses = durs[:-1] + [p05_use]
    for i, u in enumerate(uses[:-1]):
        acc += u
        splices.append(acc)
        print(f"  SPLICE {i + 1} {acc:.3f}", flush=True)

    work = Path(tempfile.mkdtemp(prefix="hos_join_v01_"))
    png = work / "end_card.png"
    card = work / "end_card.mp4"
    p05t = work / "p05_trim.mp4"
    lst = work / "concat.txt"
    bin_path = Path("/tmp/render_hos_end_card")
    subprocess.run(["swiftc", "-O", "-o", str(bin_path), str(SWIFT)], check=True)
    subprocess.run([str(bin_path), str(png)], check=True)

    ff(
        "-loop", "1", "-i", str(png),
        "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
        "-filter_complex",
        "[0:v]fps=24,format=yuv420p,"
        "fade=t=in:st=0:d=0.25,"
        f"fade=t=out:st={CARD - 0.70:.3f}:d=0.70:c=black,setsar=1[v]",
        "-map", "[v]", "-map", "1:a",
        "-t", f"{CARD:.3f}",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-profile:v", "baseline", "-level", "3.1", "-bf", "0",
        "-preset", "fast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
        "-movflags", "+faststart", "-brand", "mp42",
        str(card),
    )
    ff(
        "-i", str(paths[-1]),
        "-t", f"{p05_use:.6f}",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-profile:v", "baseline", "-level", "3.1", "-bf", "0",
        "-preset", "fast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
        "-movflags", "+faststart", "-brand", "mp42",
        str(p05t),
    )

    lines = []
    for p in paths[:-1]:
        lines.append(f"file '{p}'")
    lines.append(f"file '{p05t}'")
    lines.append(f"file '{card}'")
    lst.write_text("\n".join(lines) + "\n")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    ff(
        "-f", "concat", "-safe", "0", "-i", str(lst),
        "-c", "copy",
        "-movflags", "+faststart", "-brand", "mp42",
        str(OUT),
    )
    print(f"SAVED {OUT}", flush=True)
    print(f"SIZE {OUT.stat().st_size}", flush=True)
    print(f"SHA256 {sha256(OUT)}", flush=True)
    print(f"DUR {probe_dur(OUT):.3f}", flush=True)
    print("SPLICES " + " ".join(f"{s:.3f}" for s in splices), flush=True)
    print(f"CARD_IN {sum(uses):.3f}", flush=True)
    if ICLOUD.parent.exists():
        ICLOUD.mkdir(parents=True, exist_ok=True)
        subprocess.run(["cp", "-f", str(OUT), str(ICLOUD / OUT.name)], check=False)
        print(f"ICLOUD {ICLOUD / OUT.name}", flush=True)


if __name__ == "__main__":
    main()
