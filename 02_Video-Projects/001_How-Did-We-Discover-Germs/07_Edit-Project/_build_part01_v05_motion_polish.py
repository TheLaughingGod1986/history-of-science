#!/usr/bin/env python3
"""Part 01 v05 — polish stills into continuous video (Veo still quota-blocked).

Ben UAT: v04 stillbridges felt jumpy/frozen. This build:
  - multi-angle still CHAINS per beat (A→B→C) with long in-beat dissolves
  - continuous Ken Burns (different pan/zoom per segment — never a hold)
  - longer between-beat xfades
  - subtle lamp-flicker brightness so frames feel alive
  - keep real motion corridor + doctor-hands plates
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
RAW = PROJ / "04_Generated-Clips" / "part01" / "raw" / "v05"
REFS = PROJ / "04_Generated-Clips" / "part01" / "refs"
VO = PROJ / "02_Voiceover" / "part01_invisible_enemy_v01.mp3"
OUT = PROJ / "09_Final-Export" / "hos_001_part01_rough_v05.mp4"
META = PROJ / "07_Edit-Project" / "part01_gen_meta_v05.json"
ART = Path("/opt/cursor/artifacts")
LEGACY_RAW = PROJ / "04_Generated-Clips" / "part01" / "raw"

FPS = 24
# Longer in-beat segments + soft dissolves kill the slideshow feel.
# Sized so chained beats ≈ full Part 01 VO (~84s).
SEG_S = 4.5
IN_XFADE = 1.0
BEAT_XFADE = 1.1


def ff(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(["ffmpeg", "-y", *args], check=check, capture_output=True)


def still_to_motion(src: Path, dest: Path, *, seg_s: float, mode: int) -> None:
    """Continuous camera move — never a frozen hold."""
    frames = int(seg_s * FPS)
    # Alternate push / drift / rise so chained angles don't feel identical
    if mode % 3 == 0:
        z = "min(1.0+0.0015*on,1.18)"
        x = "iw/2-(iw/zoom/2)"
        y = "ih/2-(ih/zoom/2)-on*0.15"
    elif mode % 3 == 1:
        z = "min(1.04+0.0012*on,1.16)"
        x = "iw/2-(iw/zoom/2)+on*0.35"
        y = "ih/2-(ih/zoom/2)"
    else:
        z = "max(1.16-0.0012*on,1.02)"
        x = "iw/2-(iw/zoom/2)-on*0.25"
        y = "ih/2-(ih/zoom/2)+on*0.1"

    # Cover-crop to 16:9, continuous zoompan, subtle lamp flicker
    vf = (
        "scale=1600:900:force_original_aspect_ratio=increase,"
        "crop=1600:900,"
        f"zoompan=z='{z}':x='{x}':y='{y}':d={frames}:s=1280x720:fps={FPS},"
        "eq=brightness='0.012*sin(2*PI*t*1.4)':saturation=1.05,"
        "format=yuv420p"
    )
    ff(
        "-loop", "1", "-i", str(src),
        "-vf", vf, "-t", f"{seg_s:.3f}", "-an",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-pix_fmt", "yuv420p", str(dest),
    )


def motion_trim(src: Path, dest: Path, dur: float) -> None:
    vf = (
        f"trim=0:{dur:.3f},setpts=PTS-STARTPTS,"
        "scale=1280:720:force_original_aspect_ratio=decrease,"
        f"pad=1280:720:(ow-iw)/2:(oh-ih)/2,fps={FPS},"
        "eq=brightness='0.008*sin(2*PI*t*1.2)',format=yuv420p"
    )
    ff(
        "-i", str(src), "-vf", vf, "-an",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18", str(dest),
    )


def xfade_chain(clips: list[Path], dest: Path, xfade: float) -> float:
    """Soft-dissolve a list of equal-ish clips into one continuous beat."""
    n = len(clips)
    if n == 1:
        dest.write_bytes(clips[0].read_bytes())
        # probe duration
        p = subprocess.run(
            [
                "ffprobe", "-v", "error", "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1", str(dest),
            ],
            capture_output=True, text=True, check=True,
        )
        return float(p.stdout.strip())

    # Normalize each to exact SEG_S first via trim
    normed: list[Path] = []
    for i, c in enumerate(clips):
        npath = dest.parent / f"_norm_{dest.stem}_{i}.mp4"
        ff(
            "-i", str(c),
            "-vf", f"trim=0:{SEG_S:.3f},setpts=PTS-STARTPTS,fps={FPS},format=yuv420p",
            "-an", "-c:v", "libx264", "-preset", "fast", "-crf", "18", str(npath),
        )
        normed.append(npath)

    inputs: list[str] = []
    for c in normed:
        inputs += ["-i", str(c)]
    parts = [f"[{i}:v]format=yuv420p[v{i}]" for i in range(n)]
    vprev = "v0"
    offset = SEG_S - xfade
    for i in range(1, n):
        out = f"vx{i}"
        parts.append(
            f"[{vprev}][v{i}]xfade=transition=fade:duration={xfade:.3f}:offset={offset:.3f}[{out}]"
        )
        vprev = out
        offset += SEG_S - xfade
    dur = n * SEG_S - (n - 1) * xfade
    fc = ";".join(parts)
    ff(
        *inputs, "-filter_complex", fc, "-map", f"[{vprev}]",
        "-an", "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-t", f"{dur:.3f}", str(dest),
    )
    for p in normed:
        p.unlink(missing_ok=True)
    return dur


def assemble_beats(beats: list[Path], vo: Path, out: Path, xfade: float) -> float:
    n = len(beats)
    # Probe durations
    durs: list[float] = []
    for b in beats:
        p = subprocess.run(
            [
                "ffprobe", "-v", "error", "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1", str(b),
            ],
            capture_output=True, text=True, check=True,
        )
        durs.append(float(p.stdout.strip()))

    inputs: list[str] = []
    for b in beats:
        inputs += ["-i", str(b)]
    inputs += ["-i", str(vo)]

    parts = [f"[{i}:v]fps={FPS},format=yuv420p[v{i}]" for i in range(n)]
    vprev = "v0"
    offset = durs[0] - xfade
    for i in range(1, n):
        outl = f"vx{i}"
        parts.append(
            f"[{vprev}][v{i}]xfade=transition=fade:duration={xfade:.3f}:offset={offset:.3f}[{outl}]"
        )
        vprev = outl
        offset += durs[i] - xfade
    pic_dur = sum(durs) - (n - 1) * xfade
    afilter = (
        f"[{n}:a]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo,"
        f"atrim=0:{pic_dur:.3f},apad=whole_dur={pic_dur:.3f},"
        f"afade=t=in:st=0:d=0.4,afade=t=out:st={max(0, pic_dur-0.8):.3f}:d=0.8[a]"
    )
    fc = ";".join(parts) + ";" + afilter
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg", "-y", *inputs, "-filter_complex", fc,
            "-map", f"[{vprev}]", "-map", "[a]",
            "-c:v", "libx264", "-preset", "fast", "-crf", "17",
            "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart", str(out),
        ],
        check=True,
    )
    return pic_dur


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)

    # Beat plan: chains of stills OR real motion files
    plan: list[tuple[str, list[Path] | Path]] = [
        (
            "01_ward_open",
            [
                REFS / "ward_open_a_v05.jpg",
                REFS / "ward_open_b_v05.jpg",
                REFS / "ward_open_c_v05.jpg",
            ],
        ),
        ("02_corridor", LEGACY_RAW / "02_clean_corridor_v01.mp4"),
        (
            "03_patients",
            [REFS / "patients_a_v05.jpg", REFS / "patients_b_v05.jpg"],
        ),
        (
            "04_explorer",
            [
                REFS / "explorer_a_v05.jpg",
                REFS / "explorer_b_v05.jpg",
                REFS / "explorer_c_v05.jpg",
            ],
        ),
        ("05_instruments", LEGACY_RAW / "05_doctor_hands_instruments_v01.mp4"),
        (
            "06_fever",
            [REFS / "fever_a_v05.jpg", REFS / "fever_b_v05.jpg"],
        ),
        (
            "07_micro_hint",
            [REFS / "micro_hint_a_v05.jpg", REFS / "micro_hint_b_v05.jpg"],
        ),
        (
            "08_hands",
            [REFS / "hands_a_v05.jpg", REFS / "hands_b_v05.jpg"],
        ),
        (
            "09_micro_close",
            [REFS / "micro_close_a_v05.jpg", REFS / "micro_close_b_v05.jpg"],
        ),
        (
            "10_ward_hold",
            [REFS / "ward_hold_a_v05.jpg", REFS / "ward_hold_b_v05.jpg"],
        ),
    ]

    beat_paths: list[Path] = []
    mode = 0
    for bid, src in plan:
        beat_out = RAW / f"{bid}_beat.mp4"
        if isinstance(src, Path):
            # Real motion plate — keep longer so it carries the minute
            print(f"motion beat {bid}", flush=True)
            motion_trim(src, beat_out, dur=9.5)
        else:
            segs: list[Path] = []
            for i, still in enumerate(src):
                if not still.exists():
                    raise SystemExit(f"missing {still}")
                seg = RAW / f"{bid}_seg{i}.mp4"
                print(f"motionize {still.name} → {seg.name}", flush=True)
                still_to_motion(still, seg, seg_s=SEG_S, mode=mode)
                mode += 1
                segs.append(seg)
            print(f"chain {bid} ({len(segs)} segs)", flush=True)
            xfade_chain(segs, beat_out, IN_XFADE)
        beat_paths.append(beat_out)

    print("assemble master…", flush=True)
    pic_dur = assemble_beats(beat_paths, VO, OUT, BEAT_XFADE)
    print(f"SAVED {OUT} ({OUT.stat().st_size} bytes) ~{pic_dur:.1f}s", flush=True)

    ART.mkdir(parents=True, exist_ok=True)
    subprocess.run(["cp", "-f", str(OUT), str(ART / OUT.name)], check=False)

    meta = {
        "out": str(OUT),
        "mode": "motion_chain_v05",
        "note": (
            "Veo quota still blocked. Multi-angle still chains + continuous Ken Burns + "
            "long dissolves + lamp flicker; corridor/hands remain true motion."
        ),
        "seg_s": SEG_S,
        "in_xfade": IN_XFADE,
        "beat_xfade": BEAT_XFADE,
        "pic_dur": pic_dur,
        "beats": [b.name for b in beat_paths],
    }
    META.write_text(json.dumps(meta, indent=2))
    print(json.dumps(meta, indent=2))


if __name__ == "__main__":
    main()
