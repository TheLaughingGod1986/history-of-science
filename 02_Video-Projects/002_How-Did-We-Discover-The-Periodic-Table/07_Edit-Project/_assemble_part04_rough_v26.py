#!/usr/bin/env python3
"""HOS 002 Part 04 rough v26 — BED-ONLY remaster.

Parent KEEP picture: hos_002_part04_rough_v25.mp4 (sha locked below).
No Flow / plate / Explorer remint. Video stream copied bit-identical from v25.
Audio: same VO + curious workshop bed continuous through full 127.760s
(FAMILY FIRST → end). Soft fade last ~1.6s OK.
"""
from __future__ import annotations

import hashlib
import shutil
import subprocess
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
PARENT = PROJ / "09_Final-Export/hos_002_part04_rough_v25.mp4"
PARENT_SHA = "e78027c0c58abe9284f7b85de693a08caabd3ad8ee45b64624eadd0329942bb1"
VO = PROJ / "02_Voiceover/part04_empty_chairs_v01.wav"
BED_SRC = PROJ / "05_Music/hos_002_part01_curious_workshop_v02_norm.wav"
BED_LOOP130 = PROJ / "05_Music/hos_002_part01_curious_workshop_v02_loop130_norm.wav"
OUT = PROJ / "09_Final-Export/hos_002_part04_rough_v26.mp4"
ICLOUD = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT"
WATCH = PROJ / "07_Edit-Project/WATCH_part04_v26.txt"

# Match v25 mix
BED_VOL = 0.38
TARGET_DUR = 127.760
BED_FADE_OUT = 1.6
BODY_S = 84.0  # usable workshop body before silence tail in source
ACROSS_S = 2.0


def probe(path: Path) -> float:
    return float(
        subprocess.check_output(
            [
                "ffprobe", "-v", "error", "-show_entries", "format=duration",
                "-of", "default=nw=1:nk=1", str(path),
            ],
            text=True,
        ).strip()
    )


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def ensure_bed(total: float) -> Path:
    """Return a workshop bed that covers full cut (≥ total + small pad)."""
    if BED_LOOP130.exists() and probe(BED_LOOP130) >= total + 0.5:
        print(f"reuse {BED_LOOP130.name} dur={probe(BED_LOOP130):.3f}", flush=True)
        return BED_LOOP130

    if not BED_SRC.exists():
        raise SystemExit(f"missing bed source {BED_SRC}")

    # Rebuild a soft-looped bed long enough for this cut (same language as P05).
    need = max(130.0, total + 2.0)
    out = PROJ / "05_Music/hos_002_part01_curious_workshop_v02_loop130_norm.wav"
    tmp = PROJ / "05_Music/_tmp_p04_bed_body84.wav"
    run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(BED_SRC),
            "-af", f"atrim=0:{BODY_S:.3f},asetpts=PTS-STARTPTS",
            "-c:a", "pcm_s16le", str(tmp),
        ]
    )
    run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(tmp), "-i", str(tmp),
            "-filter_complex",
            f"[0:a][1:a]acrossfade=d={ACROSS_S:.3f}:c1=tri:c2=tri,"
            f"atrim=0:{need:.3f},asetpts=PTS-STARTPTS,"
            f"afade=t=out:st={need - BED_FADE_OUT:.3f}:d={BED_FADE_OUT:.3f},"
            "loudnorm=I=-18:TP=-1.5:LRA=11[a]",
            "-map", "[a]", "-c:a", "pcm_s16le", str(out),
        ]
    )
    if tmp.exists():
        tmp.unlink()
    dur = probe(out)
    if dur < total + 0.5:
        raise SystemExit(f"bed too short: {dur:.3f}s need>={total + 0.5:.3f}")
    print(f"built {out.name} dur={dur:.3f}", flush=True)
    return out


def main() -> None:
    if not PARENT.exists():
        raise SystemExit(f"missing parent KEEP {PARENT}")
    got = sha256(PARENT)
    if got != PARENT_SHA:
        raise SystemExit(
            f"STOP: parent picture sha mismatch\n  want {PARENT_SHA}\n  got  {got}\n"
            "Do not remint picture — abort bed remaster."
        )
    parent_dur = probe(PARENT)
    if abs(parent_dur - TARGET_DUR) > 0.05:
        raise SystemExit(f"parent duration {parent_dur:.3f} != {TARGET_DUR}")

    if not VO.exists():
        raise SystemExit(f"missing VO {VO}")
    vo_dur = probe(VO)
    if abs(vo_dur - TARGET_DUR) > 0.05:
        raise SystemExit(f"VO duration {vo_dur:.3f} != {TARGET_DUR}")

    bed = ensure_bed(TARGET_DUR)
    total = TARGET_DUR

    # Bed-only remux: copy video bitstream; rebuild VO+bed mix (same levels as v25).
    fade_st = max(0.0, total - BED_FADE_OUT)
    fc = (
        f"[1:a]aformat=sample_rates=48000:channel_layouts=stereo,"
        f"atrim=0:{vo_dur:.3f},asetpts=PTS-STARTPTS[vo];"
        f"[2:a]aformat=sample_rates=48000:channel_layouts=stereo,"
        f"atrim=0:{total:.3f},asetpts=PTS-STARTPTS,"
        f"volume={BED_VOL},"
        f"afade=t=out:st={fade_st:.3f}:d={BED_FADE_OUT:.3f}[bed];"
        f"[vo][bed]amix=inputs=2:duration=first:dropout_transition=0[a]"
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(PARENT),
            "-i", str(VO),
            "-i", str(bed),
            "-filter_complex", fc,
            "-map", "0:v:0", "-map", "[a]",
            "-c:v", "copy",
            "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart",
            "-t", f"{total:.3f}",
            str(OUT),
        ]
    )

    digest = sha256(OUT)
    out_dur = probe(OUT)
    out_bytes = OUT.stat().st_size
    if abs(out_dur - TARGET_DUR) > 0.08:
        raise SystemExit(f"output duration {out_dur:.3f} != {TARGET_DUR}")

    watch = (
        "WATCH THIS FILE ONLY (Part 04 rough v26 — BED-ONLY remaster):\n"
        f"  {OUT.name}\n\n"
        "Picture = KEEP v25 (video bitstream copy). No Flow / plate / Explorer remint.\n"
        f"parent_sha={PARENT_SHA}\n"
        f"sha256={digest}\n"
        f"bytes={out_bytes}\n"
        f"duration={out_dur:.3f}\n"
        f"bed={bed.name} (≥{TARGET_DUR:.3f}s) BED_VOL={BED_VOL}\n"
        "UAT gate: bed continuous through last ~20s (FAMILY FIRST → end); VO clear.\n"
        "Scores → CoS. Do not ping Ben unless CoS asks for watch.\n"
        "P05 untouched. P01–P03 LOCKED.\n"
    )
    WATCH.write_text(watch)

    ICLOUD.mkdir(parents=True, exist_ok=True)
    dest = ICLOUD / OUT.name
    shutil.copy2(OUT, dest)
    if sha256(dest) != digest or dest.stat().st_size != out_bytes:
        raise SystemExit("iCloud copy byte mismatch")
    (ICLOUD / "WATCH_part04_v26.txt").write_text(watch)

    print(f"LANDED {OUT}", flush=True)
    print(f"sha256={digest}", flush=True)
    print(f"bytes={out_bytes}", flush=True)
    print(f"duration={out_dur:.3f}", flush=True)
    print(f"ICLOUD {dest}", flush=True)


if __name__ == "__main__":
    main()
