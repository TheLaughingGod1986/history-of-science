#!/usr/bin/env python3
"""HOS 004 Part 04 rough v01 — board windows + v04 VO + TEMP bed (same treatment as Part 01).

Picture: part-04_plates_v02.json t_s windows (part-local).
Audio: hos_004_part04_vo_v04.wav + TEMP bed −20 dB sidechain duck + end fade.
1080p30. No Veo audio. Copy to iCloud HOS UAT.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
EDIT = Path(__file__).resolve().parent
PLATES = EDIT / "parts/part-04_plates_v02.json"
LOG = EDIT / "PART04_MINT_LOG_v01.json"
RAW = PROJ / "04_Generated-Clips/part04/raw/v01"
VO = PROJ / "02_Voiceover/05_Master/hos_004_part04_vo_v04.wav"
MUSIC = PROJ / "05_Music/hos004-part04-temp_score_bed_v01.mp3"
OUT = PROJ / "09_Final-Export/hos_004_part04_rough_v01.mp4"
META = EDIT / "part04_rough_v01_land_meta.json"
WORK = EDIT / "_part04_rough_v01_work"
ICLOUD = (
    Path.home()
    / "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT"
    / "004_Whats-Really-Inside-An-Atom"
    / "09_Final-Export"
    / "hos_004_part04_rough_v01.mp4"
)

FPS = 30
W, H = 1920, 1080
BED_REL_DB = -20.0
BED_VOLUME = 10 ** (BED_REL_DB / 20.0)
FADE_OUT_S = 2.5
SIDECHAIN = "threshold=0.018:ratio=8:attack=20:release=500:level_sc=1"


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


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def windows(plates: list[dict], vo_dur: float) -> list[tuple[float, float, float]]:
    starts = [float(p["t_s"]) for p in plates]
    out = []
    for i, t0 in enumerate(starts):
        t1 = starts[i + 1] if i + 1 < len(starts) else vo_dur
        out.append((t0, t1, max(0.20, t1 - t0)))
    return out


def main() -> None:
    board = json.loads(PLATES.read_text())
    log = json.loads(LOG.read_text()) if LOG.exists() else {"plates": {}}
    plates = board["plates"]
    vo_dur = probe(VO)
    if abs(vo_dur - 109.022) > 0.05:
        print(f"WARN VO dur {vo_dur:.3f} (expected ~109.022)", flush=True)
    if not MUSIC.exists():
        raise SystemExit(f"STOP missing TEMP bed {MUSIC}")
    music_dur = probe(MUSIC)
    wins = windows(plates, vo_dur)
    if abs(sum(w[2] for w in wins) - vo_dur) > 0.05:
        raise SystemExit(f"window sum mismatch {sum(w[2] for w in wins)} vs {vo_dur}")
    if music_dur < vo_dur:
        raise SystemExit(f"music {music_dur:.3f}s < VO {vo_dur:.3f}s")

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

    normed: list[Path] = []
    plate_meta = []
    for i, (pl, (t0, t1, win_s), src) in enumerate(zip(plates, wins, clips)):
        dest = WORK / f"n{i:02d}_{pl['id']}.mp4"
        frames = max(1, int(round(win_s * FPS)))
        used_s = frames / FPS
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(src),
            "-vf", (
                f"trim=duration={used_s:.6f},setpts=PTS-STARTPTS,"
                f"scale={W}:{H}:force_original_aspect_ratio=decrease,"
                f"pad={W}:{H}:(ow-iw)/2:(oh-ih)/2,fps={FPS},format=yuv420p"
            ),
            "-an",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
            "-r", str(FPS),
            "-t", f"{used_s:.6f}",
            str(dest),
        ])
        normed.append(dest)
        plate_meta.append({
            "id": pl["id"],
            "file": src.name,
            "sha256": sha256(src),
            "window_t0": t0,
            "window_t1": t1,
            "window_s": win_s,
            "used_s": used_s,
            "explorer": bool(pl.get("explorer")),
            "quality": pl.get("quality"),
            "vo_land": pl.get("vo_land"),
        })

    concat_list = WORK / "concat.txt"
    concat_list.write_text(
        "".join(f"file '{p.resolve()}'\n" for p in normed), encoding="utf-8"
    )
    picture = WORK / "picture_silent.mp4"
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-f", "concat", "-safe", "0", "-i", str(concat_list),
        "-c", "copy",
        str(picture),
    ])

    master_dur = vo_dur
    fade_start = max(0.0, master_dur - FADE_OUT_S)
    graph = (
        f"[0:v]trim=0:{master_dur:.6f},setpts=PTS-STARTPTS,"
        f"scale={W}:{H}:force_original_aspect_ratio=decrease,"
        f"pad={W}:{H}:(ow-iw)/2:(oh-ih)/2,fps={FPS},format=yuv420p[v];"
        f"[1:a]atrim=0:{master_dur:.6f},asetpts=PTS-STARTPTS,"
        "aformat=sample_rates=48000:channel_layouts=stereo,asplit=2[vo][vo_sc];"
        f"[2:a]atrim=0:{master_dur:.6f},asetpts=PTS-STARTPTS,"
        f"volume={BED_VOLUME:.6f},"
        f"afade=t=out:st={fade_start:.6f}:d={FADE_OUT_S:.6f},"
        "aformat=sample_rates=48000:channel_layouts=stereo[music];"
        f"[music][vo_sc]sidechaincompress={SIDECHAIN}[ducked];"
        "[vo][ducked]amix=inputs=2:weights=1 1:normalize=0,"
        "alimiter=limit=0.8912509:level=false[a]"
    )

    with tempfile.TemporaryDirectory(prefix="hos004_p04_v01_") as td:
        tmp = Path(td) / "rough_v01.mp4"
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(picture),
            "-i", str(VO),
            "-i", str(MUSIC),
            "-filter_complex", graph,
            "-map", "[v]", "-map", "[a]",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
            "-pix_fmt", "yuv420p",
            "-r", str(FPS),
            "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "192k",
            "-t", f"{master_dur:.6f}",
            "-movflags", "+faststart",
            str(tmp),
        ])
        shutil.copy2(tmp, OUT)
    shutil.copy2(OUT, ICLOUD)

    digest = sha256(OUT)
    meta = {
        "out": str(OUT),
        "icloud": str(ICLOUD),
        "sha256": digest,
        "icloud_sha256": sha256(ICLOUD),
        "duration_s": probe(OUT),
        "video_stream_note": "1080p30 silent plates + TEMP bed + v04 VO",
        "fps": FPS,
        "size": f"{W}x{H}",
        "vo": str(VO),
        "vo_duration_s": vo_dur,
        "vo_level": "unchanged",
        "music": {
            "temp": True,
            "path": str(MUSIC),
            "sha256": sha256(MUSIC),
            "bed_relative_db_vs_vo": BED_REL_DB,
            "sidechain": SIDECHAIN,
            "fade_out_s": FADE_OUT_S,
            "same_treatment_as_part01": True,
        },
        "part": "04",
        "parent_part03_pass": "hos_004_part03_rough_v01.mp4",
        "explorer_plate": "16_explorer_stadium_pea",
        "plates": plate_meta,
    }
    META.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(f"SAVED {OUT}")
    print(f"ICLOUD {ICLOUD}")
    print(f"sha256 {digest}")
    print(f"duration {meta['duration_s']:.3f}s")


if __name__ == "__main__":
    main()
