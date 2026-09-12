#!/usr/bin/env python3
"""HOS 002 Part 05 rough v02 — BED-ONLY remaster.

Parent KEEP picture: hos_002_part05_rough_v01.mp4 (sha locked below).
No Flow / plate / Explorer remint. Video stream copied bit-identical from v01.
Audio: same VO + workshop bed extended through full 147.310s (incl. end card).
"""
from __future__ import annotations

import hashlib
import shutil
import subprocess
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
PARENT = PROJ / "09_Final-Export/hos_002_part05_rough_v01.mp4"
PARENT_SHA = "8dcb06b596318a7283210928fbb0e78f6f89c7db5d200b8edeefbaa9b5522ec4"
VO = PROJ / "02_Voiceover/part05_the_guests_arrive_v01.wav"
BED_SRC = PROJ / "05_Music/hos_002_part01_curious_workshop_v02_norm.wav"
BED_LOOP130 = PROJ / "05_Music/hos_002_part01_curious_workshop_v02_loop130_norm.wav"
BED_LOOP150 = PROJ / "05_Music/hos_002_part01_curious_workshop_v02_loop150_norm.wav"
OUT = PROJ / "09_Final-Export/hos_002_part05_rough_v02.mp4"
ICLOUD = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT"
WATCH = PROJ / "07_Edit-Project/WATCH_part05_v02.txt"

# Match v01 mix
BED_VOL = 0.38
END_CARD_S = 3.5
XFADE_JOIN = 0.35
TARGET_DUR = 147.310
BODY_S = 84.0  # usable workshop body before silence tail in source
ACROSS_S = 2.0
BED_FADE_OUT = 1.6


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


def build_loop150() -> Path:
    """Extend curious workshop bed to ≥150s via soft-crossfaded usable body."""
    if BED_LOOP150.exists() and probe(BED_LOOP150) >= 148.0:
        print(f"reuse {BED_LOOP150.name} dur={probe(BED_LOOP150):.3f}", flush=True)
        return BED_LOOP150

    if not BED_SRC.exists():
        raise SystemExit(f"missing bed source {BED_SRC}")

    tmp = PROJ / "05_Music/_tmp_p05_bed_body84.wav"
    mid = PROJ / "05_Music/_tmp_p05_bed_mid.wav"

    # Usable body only (source dies ~85s)
    run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(BED_SRC),
            "-af", f"atrim=0:{BODY_S:.3f},asetpts=PTS-STARTPTS",
            "-c:a", "pcm_s16le", str(tmp),
        ]
    )

    # Soft-crossfade body onto itself → ~166s, then trim/normalize to 150s
    # Prefer extending existing loop130 when present (same seam language as P04).
    if BED_LOOP130.exists():
        run(
            [
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-i", str(BED_LOOP130), "-i", str(tmp),
                "-filter_complex",
                f"[0:a][1:a]acrossfade=d={ACROSS_S:.3f}:c1=tri:c2=tri,"
                f"atrim=0:150.000,asetpts=PTS-STARTPTS,"
                f"afade=t=out:st={150.0 - BED_FADE_OUT:.3f}:d={BED_FADE_OUT:.3f},"
                "loudnorm=I=-18:TP=-1.5:LRA=11[a]",
                "-map", "[a]", "-c:a", "pcm_s16le", str(BED_LOOP150),
            ]
        )
    else:
        run(
            [
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-i", str(tmp), "-i", str(tmp),
                "-filter_complex",
                f"[0:a][1:a]acrossfade=d={ACROSS_S:.3f}:c1=tri:c2=tri,"
                f"atrim=0:150.000,asetpts=PTS-STARTPTS,"
                f"afade=t=out:st={150.0 - BED_FADE_OUT:.3f}:d={BED_FADE_OUT:.3f},"
                "loudnorm=I=-18:TP=-1.5:LRA=11[a]",
                "-map", "[a]", "-c:a", "pcm_s16le", str(BED_LOOP150),
            ]
        )

    for p in (tmp, mid):
        if p.exists():
            p.unlink()

    dur = probe(BED_LOOP150)
    if dur < 148.0:
        raise SystemExit(f"loop150 too short: {dur:.3f}s")
    print(f"built {BED_LOOP150.name} dur={dur:.3f}", flush=True)
    return BED_LOOP150


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
    bed = build_loop150()

    vo_dur = probe(VO)
    total = vo_dur + END_CARD_S - XFADE_JOIN
    if abs(total - TARGET_DUR) > 0.05:
        raise SystemExit(f"computed total {total:.3f} != target {TARGET_DUR}")

    # Bed-only remux: copy video bitstream; rebuild VO+bed mix (same levels as v01).
    fade_st = max(0.0, total - BED_FADE_OUT)
    fc = (
        f"[1:a]aformat=sample_rates=48000:channel_layouts=stereo,"
        f"atrim=0:{vo_dur:.3f},asetpts=PTS-STARTPTS,"
        f"apad=pad_dur={END_CARD_S:.3f}[vo];"
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
        "WATCH THIS FILE ONLY (Part 05 rough v02 — BED-ONLY remaster):\n"
        f"  {OUT.name}\n\n"
        "Picture = KEEP v01 (video bitstream copy). No Flow / plate / Explorer remint.\n"
        f"parent_sha={PARENT_SHA}\n"
        f"sha256={digest}\n"
        f"bytes={out_bytes}\n"
        f"duration={out_dur:.3f}\n"
        f"bed={bed.name} (≥148s) BED_VOL={BED_VOL}\n"
        "UAT gate: bed continuous through last ~20s / end card; VO clear.\n"
        "Scores → CoS. Do not ping Ben unless CoS asks for watch.\n"
        "P04 stays LOCKED — do not touch.\n"
    )
    WATCH.write_text(watch)

    ICLOUD.mkdir(parents=True, exist_ok=True)
    dest = ICLOUD / OUT.name
    shutil.copy2(OUT, dest)
    # Identical bytes to iCloud copy
    if sha256(dest) != digest or dest.stat().st_size != out_bytes:
        raise SystemExit("iCloud copy byte mismatch")
    (ICLOUD / "WATCH_part05_v02.txt").write_text(watch)

    print(f"LANDED {OUT}", flush=True)
    print(f"sha256={digest}", flush=True)
    print(f"bytes={out_bytes}", flush=True)
    print(f"duration={out_dur:.3f}", flush=True)
    print(f"ICLOUD {dest}", flush=True)


if __name__ == "__main__":
    main()
