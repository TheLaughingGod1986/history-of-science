#!/usr/bin/env python3
"""HOS 004 Part 01 rough — assemble KEEP plates on VO v04.

1920x1080 · 30 fps · xfade 0.35 · bed ~-20 dB if present.
No freeze-pad. Trim VO to picture if needed (≤1s). Copy to iCloud UAT.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
REPO = Path(__file__).resolve().parents[3]
PLATES = PROJ / "07_Edit-Project/parts/part-01_plates_v02.json"
LOG = PROJ / "07_Edit-Project/PART01_MINT_LOG_v01.json"
RAW = PROJ / "04_Generated-Clips/part01/raw/v01"
VO = PROJ / "02_Voiceover/05_Master/hos_004_part01_vo_v04.wav"
OUT = PROJ / "09_Final-Export/hos_004_part01_rough_v01.mp4"
META = PROJ / "07_Edit-Project/part01_rough_v01_land_meta.json"
WORK = PROJ / "07_Edit-Project/_part01_rough_v01_work"
ICLOUD = (
    Path.home()
    / "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT"
    / "004_Whats-Really-Inside-An-Atom"
    / "09_Final-Export"
    / "hos_004_part01_rough_v01.mp4"
)
# Reuse Germs ominous bed quietly if present; else VO only.
BED_CANDIDATES = [
    REPO
    / "02_Video-Projects/001_How-Did-We-Discover-Germs/05_Music/hos_001_part01_ominous_ward_v14_norm.wav",
]
XFADE = 0.35
CLIP_USE = 7.9
BED_VOL = 0.10  # ~-20 dB vs unity
FPS = 30
W, H = 1920, 1080


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
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=nw=1:nk=1", str(path),
            ],
            text=True,
        ).strip()
    )


def main() -> None:
    board = json.loads(PLATES.read_text())
    log = json.loads(LOG.read_text()) if LOG.exists() else {"plates": {}}
    plates = board["plates"]
    WORK.mkdir(parents=True, exist_ok=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    ICLOUD.parent.mkdir(parents=True, exist_ok=True)

    clips: list[Path] = []
    missing = []
    for pl in plates:
        pid = pl["id"]
        keep = log.get("plates", {}).get(pid, {}).get("keep")
        path = RAW / (keep["file"] if keep else f"{pid}_v01.mp4")
        if not path.exists() or path.stat().st_size < 400_000:
            missing.append(pid)
            continue
        clips.append(path)
    if missing:
        raise SystemExit(f"STOP missing KEEP plates: {missing}")
    if len(clips) != len(plates):
        raise SystemExit(f"STOP clip count {len(clips)} != plates {len(plates)}")

    # Normalize each clip: scale/pad to 1920x1080 30fps, trim to CLIP_USE, strip audio
    normed: list[Path] = []
    for i, src in enumerate(clips):
        dest = WORK / f"n{i:02d}_{src.stem}.mp4"
        dur = min(CLIP_USE, probe(src))
        subprocess.check_call(
            [
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-i", str(src),
                "-t", f"{dur:.3f}",
                "-vf",
                f"scale={W}:{H}:force_original_aspect_ratio=decrease,"
                f"pad={W}:{H}:(ow-iw)/2:(oh-ih)/2,fps={FPS},format=yuv420p",
                "-an",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                str(dest),
            ]
        )
        normed.append(dest)

    # xfade chain
    if len(normed) == 1:
        picture = normed[0]
    else:
        # Build filter_complex xfade
        inputs = []
        for p in normed:
            inputs.extend(["-i", str(p)])
        n = len(normed)
        durs = [probe(p) for p in normed]
        filters = []
        # offset accumulates
        offset = durs[0] - XFADE
        filters.append(
            f"[0:v][1:v]xfade=transition=fade:duration={XFADE}:offset={offset:.3f}[v1]"
        )
        last = "[v1]"
        for i in range(2, n):
            offset = offset + durs[i - 1] - XFADE
            out = f"[v{i}]"
            filters.append(
                f"{last}[{i}:v]xfade=transition=fade:duration={XFADE}:offset={offset:.3f}{out}"
            )
            last = out
        picture = WORK / "picture_xfade.mp4"
        cmd = [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            *inputs,
            "-filter_complex", ";".join(filters),
            "-map", last,
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
            "-an", str(picture),
        ]
        subprocess.check_call(cmd)

    pic_dur = probe(picture)
    vo_dur = probe(VO)
    # Prefer picture coverage; trim VO to picture if VO longer by ≤1s, else fail if picture short
    if pic_dur + 1.0 < vo_dur:
        raise SystemExit(
            f"STOP picture short: pic={pic_dur:.2f}s vo={vo_dur:.2f}s — mint more plates, no freeze-pad"
        )
    use_vo_t = min(vo_dur, pic_dur)
    use_pic_t = min(pic_dur, vo_dur + 0.05)

    bed = next((b for b in BED_CANDIDATES if b.exists()), None)
    if bed:
        # VO + quiet bed under
        af = (
            f"[1:a]atrim=0:{use_vo_t:.3f},asetpts=PTS-STARTPTS,volume=1.0[vo];"
            f"[2:a]atrim=0:{use_vo_t:.3f},asetpts=PTS-STARTPTS,volume={BED_VOL}[bed];"
            f"[vo][bed]amix=inputs=2:duration=first:dropout_transition=0[a]"
        )
        subprocess.check_call(
            [
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-i", str(picture), "-t", f"{use_pic_t:.3f}",
                "-i", str(VO),
                "-i", str(bed),
                "-filter_complex", af,
                "-map", "0:v", "-map", "[a]",
                "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                "-c:a", "aac", "-b:a", "192k",
                "-r", str(FPS), "-s", f"{W}x{H}",
                "-movflags", "+faststart",
                str(OUT),
            ]
        )
    else:
        subprocess.check_call(
            [
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-i", str(picture), "-t", f"{use_pic_t:.3f}",
                "-i", str(VO),
                "-filter_complex",
                f"[1:a]atrim=0:{use_vo_t:.3f},asetpts=PTS-STARTPTS[a]",
                "-map", "0:v", "-map", "[a]",
                "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                "-c:a", "aac", "-b:a", "192k",
                "-r", str(FPS), "-s", f"{W}x{H}",
                "-shortest",
                "-movflags", "+faststart",
                str(OUT),
            ]
        )

    out_dur = probe(OUT)
    out_sha = sha256(OUT)
    # Copy to iCloud
    subprocess.check_call(["cp", "-f", str(OUT), str(ICLOUD)])
    icloud_sha = sha256(ICLOUD)

    plate_meta = []
    for pl, clip in zip(plates, clips):
        plog = log.get("plates", {}).get(pl["id"], {})
        tries = plog.get("tries")
        td = plog.get("try_detail")
        if isinstance(tries, list):
            n_tries = len(tries)
        elif isinstance(tries, int):
            n_tries = tries
        elif isinstance(td, list):
            n_tries = len(td)
        else:
            n_tries = 0
        keep = plog.get("keep") or {}
        plate_meta.append({
            "id": pl["id"],
            "file": clip.name,
            "sha256": sha256(clip),
            "duration_s": round(probe(clip), 3),
            "model": keep.get("model") or plog.get("model_keep"),
            "engine": keep.get("engine") or plog.get("engine"),
            "quality_or_fast": keep.get("quality_or_fast") or plog.get("quality_or_fast"),
            "tries": n_tries,
        })

    meta = {
        "out": str(OUT),
        "sha256": out_sha,
        "duration_s": round(out_dur, 3),
        "vo": str(VO),
        "vo_sha256": sha256(VO),
        "vo_duration_s": round(vo_dur, 3),
        "picture_duration_s": round(pic_dur, 3),
        "bed": str(bed) if bed else None,
        "bed_vol": BED_VOL if bed else None,
        "xfade_s": XFADE,
        "clip_use_s": CLIP_USE,
        "fps": FPS,
        "size": f"{W}x{H}",
        "icloud": str(ICLOUD),
        "icloud_sha256": icloud_sha,
        "plates": plate_meta,
        "engine_note": log.get("engine"),
        "flow_block": log.get("flow_block"),
    }
    META.write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta, indent=2))
    print(f"SAVED {OUT} ({out_dur:.2f}s) → iCloud {ICLOUD}")


if __name__ == "__main__":
    main()
