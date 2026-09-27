#!/usr/bin/env python3
"""HOS 004 Part 01 rough v02 — cut each plate to board t_s windows on VO v04.

v01 bug: CLIP_USE=7.9 × 17 − xfade → 128.7s picture while VO is 69.81s
(audio ended; video kept going silent). v02 uses part-01_plates_v02.json
t_s windows so picture ends with VO (~70s). Hard cuts (no xfade pad).
No Veo audio. Keep v01. Copy to iCloud UAT.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
REPO = Path(__file__).resolve().parents[3]
PLATES = PROJ / "07_Edit-Project/parts/part-01_plates_v02.json"
LOG = PROJ / "07_Edit-Project/PART01_MINT_LOG_v01.json"
RAW = PROJ / "04_Generated-Clips/part01/raw/v01"
VO = PROJ / "02_Voiceover/05_Master/hos_004_part01_vo_v04.wav"
OUT = PROJ / "09_Final-Export/hos_004_part01_rough_v02.mp4"
META = PROJ / "07_Edit-Project/part01_rough_v02_land_meta.json"
WORK = PROJ / "07_Edit-Project/_part01_rough_v02_work"
NOTE = PROJ / "07_Edit-Project/PART01_ROUGH_V02_REASON.md"
ICLOUD = (
    Path.home()
    / "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT"
    / "004_Whats-Really-Inside-An-Atom"
    / "09_Final-Export"
    / "hos_004_part01_rough_v02.mp4"
)
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


def windows(plates: list[dict], vo_dur: float) -> list[tuple[float, float, float]]:
    """Return (t0, t1, dur) per plate from successive t_s → VO end."""
    starts = [float(p["t_s"]) for p in plates]
    out = []
    for i, t0 in enumerate(starts):
        t1 = starts[i + 1] if i + 1 < len(starts) else vo_dur
        dur = max(0.20, t1 - t0)
        out.append((t0, t1, dur))
    return out


def main() -> None:
    board = json.loads(PLATES.read_text())
    log = json.loads(LOG.read_text()) if LOG.exists() else {"plates": {}}
    plates = board["plates"]
    vo_dur = probe(VO)
    wins = windows(plates, vo_dur)
    assert abs(sum(w[2] for w in wins) - vo_dur) < 0.05, (
        f"window sum {sum(w[2] for w in wins)} != vo {vo_dur}"
    )

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

    # Trim each clip to its board window (from frame 0), scale to 1080p30, strip audio
    normed: list[Path] = []
    plate_meta = []
    for i, (src, pl, (t0, t1, dur)) in enumerate(zip(clips, plates, wins)):
        dest = WORK / f"n{i:02d}_{pl['id']}.mp4"
        src_dur = probe(src)
        use = min(dur, src_dur)
        # If window longer than clip (shouldn't for ~2–6s windows vs ~8s Veo), no freeze — fail
        if use + 0.05 < dur:
            raise SystemExit(
                f"STOP {pl['id']}: clip {src_dur:.2f}s shorter than window {dur:.2f}s — no freeze-pad"
            )
        subprocess.check_call(
            [
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-i", str(src),
                "-t", f"{dur:.6f}",
                "-vf",
                f"scale={W}:{H}:force_original_aspect_ratio=decrease,"
                f"pad={W}:{H}:(ow-iw)/2:(oh-ih)/2,fps={FPS},format=yuv420p,"
                f"setpts=PTS-STARTPTS",
                "-an",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                str(dest),
            ]
        )
        # Exact duration enforce (fps rounding)
        got = probe(dest)
        if abs(got - dur) > 0.08:
            # retime lightly with trim to exact
            exact = WORK / f"e{i:02d}_{pl['id']}.mp4"
            subprocess.check_call(
                [
                    "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                    "-i", str(dest),
                    "-t", f"{dur:.6f}",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                    "-an", str(exact),
                ]
            )
            dest = exact
        normed.append(dest)
        plate_meta.append({
            "id": pl["id"],
            "file": src.name,
            "sha256": sha256(src),
            "window_t0": round(t0, 3),
            "window_t1": round(t1, 3),
            "window_s": round(dur, 3),
            "used_s": round(probe(dest), 3),
            "vo_land": pl.get("vo_land"),
        })

    # Hard concat (no xfade) so sum(windows) == VO
    concat_list = WORK / "concat.txt"
    concat_list.write_text(
        "".join(f"file '{p.resolve()}'\n" for p in normed)
    )
    picture = WORK / "picture_concat.mp4"
    subprocess.check_call(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-f", "concat", "-safe", "0", "-i", str(concat_list),
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
            "-an", str(picture),
        ]
    )
    pic_dur = probe(picture)

    # Mux VO exactly — shortest so we don't pad video past VO or vice versa
    # Prefer matching both: trim to min
    use_t = min(pic_dur, vo_dur)
    if abs(pic_dur - vo_dur) > 0.15:
        raise SystemExit(
            f"STOP picture/vo mismatch: pic={pic_dur:.3f} vo={vo_dur:.3f}"
        )

    subprocess.check_call(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(picture), "-t", f"{use_t:.6f}",
            "-i", str(VO), "-t", f"{use_t:.6f}",
            "-filter_complex",
            f"[0:v]fps={FPS},format=yuv420p,setpts=PTS-STARTPTS[v];"
            f"[1:a]aformat=sample_rates=48000:channel_layouts=stereo,"
            f"asetpts=PTS-STARTPTS,volume=1.0[a]",
            "-map", "[v]", "-map", "[a]",
            "-c:v", "libx264", "-preset", "medium", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k",
            "-r", str(FPS), "-s", f"{W}x{H}",
            "-movflags", "+faststart",
            str(OUT),
        ]
    )

    out_dur = probe(OUT)
    out_sha = sha256(OUT)
    subprocess.check_call(["cp", "-f", str(OUT), str(ICLOUD)])
    icloud_sha = sha256(ICLOUD)

    # stream durations
    v_dur = float(
        subprocess.check_output(
            [
                "ffprobe", "-v", "error", "-select_streams", "v:0",
                "-show_entries", "stream=duration", "-of", "default=nw=1:nk=1",
                str(OUT),
            ],
            text=True,
        ).strip()
    )
    a_dur = float(
        subprocess.check_output(
            [
                "ffprobe", "-v", "error", "-select_streams", "a:0",
                "-show_entries", "stream=duration", "-of", "default=nw=1:nk=1",
                str(OUT),
            ],
            text=True,
        ).strip()
    )

    cold = [m for m in plate_meta if m["window_t0"] < 30.0]
    cold_long = [m for m in cold if m["window_s"] > 6.0]

    reason = (
        "v01 assembly error: `_assemble_part01_rough_v01.py` used hardcoded "
        "`CLIP_USE=7.9` per plate × 17 with 0.35s xfade → **128.7s** picture. "
        "VO v04 is **69.81s**; audio stream ended at VO while video kept playing "
        "(no black pad — full Veo clips). v02 cuts each plate to "
        "`part-01_plates_v02.json` `t_s` windows (hard concat, no freeze-pad) "
        "so A/V both ≈70s. v01 kept."
    )
    NOTE.write_text(
        "# Part 01 rough v02 — why\n\n"
        f"{reason}\n\n"
        f"- v01: `hos_004_part01_rough_v01.mp4` 128.7s (kept)\n"
        f"- v02: `{OUT.name}` {out_dur:.3f}s  v={v_dur:.3f}s a={a_dur:.3f}s\n"
        f"- sha256: `{out_sha}`\n"
        f"- iCloud: `{ICLOUD}`\n"
        f"- cold-open cuts >6s: {len(cold_long)} "
        f"({', '.join(m['id'] for m in cold_long) or 'none'})\n"
    )

    meta = {
        "out": str(OUT),
        "sha256": out_sha,
        "duration_s": round(out_dur, 3),
        "video_stream_s": round(v_dur, 3),
        "audio_stream_s": round(a_dur, 3),
        "vo": str(VO),
        "vo_duration_s": round(vo_dur, 3),
        "fps": FPS,
        "size": f"{W}x{H}",
        "icloud": str(ICLOUD),
        "icloud_sha256": icloud_sha,
        "kept_v01": True,
        "v01_bug": "7.9s×17−xfade=128.7s picture vs 69.81s VO",
        "reason": reason,
        "xfade": False,
        "plates": plate_meta,
        "cold_open_cuts_gt_6s": [m["id"] for m in cold_long],
        "gaps": [],
    }
    META.write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta, indent=2))
    print(f"SAVED {OUT} ({out_dur:.3f}s) → iCloud")


if __name__ == "__main__":
    main()
