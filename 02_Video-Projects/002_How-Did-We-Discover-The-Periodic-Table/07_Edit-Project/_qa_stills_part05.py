#!/usr/bin/env python3
"""Extract t=0.3 / 4.0 / 7.5 stills + sha for a Part 05 clip."""
from __future__ import annotations
import argparse, hashlib, subprocess
from pathlib import Path

ARTS = Path("/Users/benjaminoats/.local/share/cursor-mac-mini-hos-worker/artifacts")
QA = Path(__file__).resolve().parent / "_qa_part05_v01_flow"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", type=Path, required=True)
    ap.add_argument("--qa-name", required=True)
    ap.add_argument("--art-prefix", required=True)
    args = ap.parse_args()
    src = args.src
    qa = QA / args.qa_name
    qa.mkdir(parents=True, exist_ok=True)
    ARTS.mkdir(parents=True, exist_ok=True)
    dur = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration,size",
         "-of", "default=nw=1", str(src)],
        text=True,
    )
    digest = sha256(src)
    print(dur.strip())
    print("sha256", digest)
    print("bytes", src.stat().st_size)
    for t, name in [(0.3, "t00"), (4.0, "t04"), (7.5, "t07")]:
        dst = qa / f"{name}.jpg"
        subprocess.check_call(
            ["ffmpeg", "-y", "-ss", str(t), "-i", str(src), "-frames:v", "1", "-q:v", "2", str(dst)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        (ARTS / f"{args.art_prefix}_{name}.jpg").write_bytes(dst.read_bytes())
        print(dst.name, dst.stat().st_size)


if __name__ == "__main__":
    main()
