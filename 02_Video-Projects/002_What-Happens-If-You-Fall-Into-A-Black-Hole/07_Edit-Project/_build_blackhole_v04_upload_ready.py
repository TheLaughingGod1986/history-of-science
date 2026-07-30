#!/usr/bin/env python3
"""Video 002 — v04 upload-ready mix: ambient/cinematic bed + sparse SFX.

Takes the locked v03 picture (brand sting + subscribe outro already baked)
and rebuilds the soundtrack:
  - soft cosmic music bed (ambient × cinematic), looped to full length
  - sidechain duck under VO
  - music pulled back on brand sting + subscribe/end-screen
  - brand chime, sparse chapter whooshes, outro shimmer

Exports:
  07_Edit-Project/01_Masters/blackhole_v04_upload_ready.mp4
  09_Final-Export/blackhole_v04_UPLOAD_READY_MASTER.mp4
"""
from __future__ import annotations

import json
import shutil
import subprocess
import time
from pathlib import Path

ROOT = Path(
    "/Users/ben/code/Orbit-YouTube/02_Video-Projects/"
    "002_What-Happens-If-You-Fall-Into-A-Black-Hole"
)
EDIT = ROOT / "07_Edit-Project"
FINAL = ROOT / "09_Final-Export"
SOURCE = EDIT / "01_Masters/blackhole_v03_vo-locked_proof.mp4"
TIMELINE_IN = EDIT / "blackhole_v03_timeline.json"
TIMELINE_OUT = EDIT / "blackhole_v04_timeline.json"
MASTER = EDIT / "01_Masters/blackhole_v04_upload_ready.mp4"
UPLOAD = FINAL / "blackhole_v04_UPLOAD_READY_MASTER.mp4"
WORK = EDIT / "_work_v04"

MUSIC_A = ROOT / "05_Music/blackhole_score_cinematic_v19.wav"
MUSIC_B = ROOT / "05_Music/blackhole_score_ambient_v16.wav"
CHIME = ROOT / "06_Sound-Effects/sfx_brand_chime_v11.wav"
WHOOSH = ROOT / "06_Sound-Effects/sfx_whoosh_v19.wav"
SHIMMER = ROOT / "06_Sound-Effects/sfx_shimmer_v19.wav"
BLIP = ROOT / "06_Sound-Effects/sfx_orbit_blip_v19.wav"

# Sparse whooshes on major act turns (not every scene)
CHAPTER_WHOOSH_SCENES = ("04", "06", "08", "09", "11", "15")


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def probe_dur(path: Path) -> float:
    out = subprocess.check_output(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        text=True,
    ).strip()
    return float(out)


def scene_starts(timeline: list[dict]) -> dict[str, float]:
    starts: dict[str, float] = {}
    for e in timeline:
        sc = e["scene"]
        if sc in ("outro",) or e.get("beat") in ("brand", "cta"):
            continue
        if sc not in starts:
            starts[sc] = float(e["start_s"])
    return starts


def main() -> None:
    t0 = time.time()
    missing = [p for p in (SOURCE, MUSIC_A, MUSIC_B, CHIME, WHOOSH, SHIMMER, BLIP) if not p.exists()]
    if missing:
        raise SystemExit("Missing:\n" + "\n".join(map(str, missing)))

    meta = json.loads(TIMELINE_IN.read_text())
    duration = probe_dur(SOURCE)
    brand_t = float(meta["brand_start_s"])
    outro_t = float(meta["outro_start_s"])
    starts = scene_starts(meta["timeline"])
    whoosh_times = [starts[s] for s in CHAPTER_WHOOSH_SCENES if s in starts]

    WORK.mkdir(parents=True, exist_ok=True)
    FINAL.mkdir(parents=True, exist_ok=True)
    mixed_wav = WORK / "mixed_soundtrack.wav"

    # Music stems are ~635s each; acrossfade blend is already >19 min.
    print(f"Mixing soundtrack for {duration:.1f}s…", flush=True)
    endscreen = float(meta.get("endscreen_hold_s", 8.0))
    vo = ROOT / meta["vo"]
    if not vo.exists():
        vo = ROOT / "02_Voiceover/05_Master/blackhole_voiceover_v04_ivc_kDch_master.wav"

    # Inputs: 0=picture, 1=musicA, 2=musicB, 3=VO, 4=chime, 5=whoosh, 6=shimmer, 7=blip
    filters = [
        "[1:a]loudnorm=I=-28:LRA=9:TP=-3,aformat=sample_rates=48000:channel_layouts=stereo[ma]",
        "[2:a]loudnorm=I=-28:LRA=9:TP=-3,aformat=sample_rates=48000:channel_layouts=stereo[mb]",
        "[ma][mb]acrossfade=d=5:c1=tri:c2=tri,"
        f"atrim=0:{duration:.3f},asetpts=PTS-STARTPTS[music_raw]",
        f"[music_raw]volume=enable='between(t\\,{brand_t:.3f}\\,{brand_t + 2.2:.3f})':volume=0.28,"
        f"volume=enable='gte(t\\,{outro_t:.3f})':volume=0.22[music_shaped]",
        f"[3:a]apad=pad_dur={endscreen:.3f},atrim=0:{duration:.3f},"
        "aformat=sample_rates=48000:channel_layouts=stereo,asetpts=PTS-STARTPTS[voice]",
        "[voice]asplit=2[voice_sc][voice_mix]",
        "[music_shaped][voice_sc]sidechaincompress="
        "threshold=0.020:ratio=7:attack=18:release=420[ducked_music]",
        f"[4:a]volume=0.42,adelay={int(brand_t * 1000)}|{int(brand_t * 1000)}[brand]",
    ]

    mix_labels = ["voice_mix", "ducked_music", "brand"]
    for i, cue in enumerate(whoosh_times):
        name = f"whoosh_{i}"
        delay = int(cue * 1000)
        filters.append(f"[5:a]volume=0.10,adelay={delay}|{delay}[{name}]")
        mix_labels.append(name)

    filters.append(
        f"[6:a]volume=0.16,adelay={int((outro_t + 0.25) * 1000)}|"
        f"{int((outro_t + 0.25) * 1000)}[outro_shimmer]"
    )
    mix_labels.append("outro_shimmer")

    for i, cue in enumerate((brand_t + 0.55, outro_t + 0.70)):
        name = f"blip_{i}"
        delay = int(cue * 1000)
        filters.append(f"[7:a]volume=0.16,adelay={delay}|{delay}[{name}]")
        mix_labels.append(name)

    weights = "1 0.58 " + " ".join("1" for _ in mix_labels[2:])
    filters.append(
        "".join(f"[{label}]" for label in mix_labels)
        + f"amix=inputs={len(mix_labels)}:weights='{weights}':normalize=0,"
        "volume=-0.5dB,alimiter=limit=0.88:level=false[out]"
    )

    run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(SOURCE),  # 0 — timing reference only
            "-i",
            str(MUSIC_A),
            "-i",
            str(MUSIC_B),
            "-i",
            str(vo),
            "-i",
            str(CHIME),
            "-i",
            str(WHOOSH),
            "-i",
            str(SHIMMER),
            "-i",
            str(BLIP),
            "-filter_complex",
            ";".join(filters),
            "-map",
            "[out]",
            "-t",
            f"{duration:.3f}",
            "-ar",
            "48000",
            "-ac",
            "2",
            str(mixed_wav),
        ]
    )
    print(f"  soundtrack {mixed_wav} ({probe_dur(mixed_wav):.1f}s)", flush=True)

    print("Muxing upload master…", flush=True)
    run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(SOURCE),
            "-i",
            str(mixed_wav),
            "-map",
            "0:v:0",
            "-map",
            "1:a:0",
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-shortest",
            "-movflags",
            "+faststart",
            str(MASTER),
        ]
    )
    shutil.copy2(MASTER, UPLOAD)

    master_dur = probe_dur(MASTER)
    out_meta = {
        **{k: meta[k] for k in meta if k != "timeline"},
        "version": "v04",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "source_picture": str(SOURCE.relative_to(ROOT)),
        "master": str(MASTER.relative_to(ROOT)),
        "upload_master": str(UPLOAD.relative_to(ROOT)),
        "master_duration_s": round(master_dur, 3),
        "audio": {
            "music_a": str(MUSIC_A.relative_to(ROOT)),
            "music_b": str(MUSIC_B.relative_to(ROOT)),
            "music_weight": 0.58,
            "sidechain": "threshold=0.020 ratio=7 attack=18 release=420",
            "brand_music_pull": 0.28,
            "outro_music_pull": 0.22,
            "whoosh_at_s": [round(t, 3) for t in whoosh_times],
        },
        "rules": list(meta.get("rules", []))
        + [
            "ambient+cinematic music bed with VO sidechain duck",
            "music pulled back on brand + outro",
            "sparse chapter whooshes + outro shimmer",
        ],
        "timeline": meta["timeline"],
    }
    TIMELINE_OUT.write_text(json.dumps(out_meta, indent=2) + "\n")

    print(f"\nUPLOAD MASTER {UPLOAD}", flush=True)
    print(f"  also {MASTER}", flush=True)
    print(f"  duration {master_dur/60:.2f} min ({master_dur:.1f}s)", flush=True)
    print(f"  elapsed {time.time()-t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
