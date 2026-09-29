#!/usr/bin/env python3
"""HOS 004 full_v03 — two-section music bed (no loop) on locked picture.

Sect2 v02 regen: no choir, no voices, no vocal pads, no humming (plain VO has no extra "you" at 8:06).

UAT only. Do not label KEEP. Do not upload.

- Picture: hos_004_full_join_v03.mp4 (Ben PASS)
- VO: locked v04 part masters at v03 starts (untouched level)
- Bed section 1: hos004-full_score_bed_v01.mp3 from 0:00 → Part 05 chapter card
- Bed section 2: hos004-full-sect2_score_bed_v02.mp3 from card → cream end
- ~1.5 s crossfade under the Part 05 chapter card (card05 @ 5:55.48)
- Gap level −20 dB; extra ~3 dB duck under speech via sidechain
- amix normalize=0; fade across cream; silent under 20 s hold
- No stream_loop anywhere
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TOOLS = ROOT / "04_Audio/tools"
sys.path.insert(0, str(TOOLS))
from orbit_cfr_delivery import remaster_cfr  # noqa: E402

PROJ = Path(__file__).resolve().parents[1]
EXP = PROJ / "09_Final-Export"
EDIT = PROJ / "07_Edit-Project"
MUSIC = PROJ / "05_Music"
VO_DIR = PROJ / "02_Voiceover/05_Master"
ICLOUD_DIR = (
    Path.home()
    / "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT"
    / "004_Whats-Really-Inside-An-Atom"
    / "09_Final-Export"
)

SRC_PIC = EXP / "hos_004_full_join_v03.mp4"
SRC_SHA = "f88cb9d47e910425519a40a6af7649626c47afbcdddf1f0f3293564c59f65244"
OUT = EXP / "hos_004_full_v03.mp4"
META = EDIT / "full_v03_land_meta.json"
WATCH = EDIT / "WATCH_full_v03.txt"
NOTES = EXP / "FULL_V03_NOTES.md"

BED_SECT1 = MUSIC / "hos004-full_score_bed_v01.mp3"
BED_SECT2 = MUSIC / "hos004-full-sect2_score_bed_v02.mp3"

# From full_join_v03_land_meta.json
PART_STARTS = {
    "01": 0.0,
    "02": 70.533333,
    "03": 162.411166,
    "04": 246.844499,
    "05": 356.577832,
}
CARD05 = 355.477832  # Part 05 chapter card — Ben 5:55.48
XFADE = 1.50
CREAM_AT = 500.693770
CREAM_DUR = 4.0
HOLD_DUR = 20.0
TOTAL = 524.7

BED_REL_DB = -20.0
BED_VOLUME = 10 ** (BED_REL_DB / 20.0)
# Gap stays −20 dB; under speech duck an extra ~3 dB vs ungated bed
# (lower threshold + higher ratio than v01's 0.018/8)
SIDECHAIN = "threshold=0.012:ratio=12:attack=20:release=500:level_sc=1"

VO_FILES = {
    "01": VO_DIR / "hos_004_part01_vo_v04.wav",
    "02": VO_DIR / "hos_004_part02_vo_v04.wav",
    "03": VO_DIR / "hos_004_part03_vo_v04.wav",
    "04": VO_DIR / "hos_004_part04_vo_v04.wav",
    "05": VO_DIR / "hos_004_part05_vo_v04.wav",
}


def ff(*args: str) -> None:
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *args], check=True)


def probe_dur(path: Path) -> float:
    out = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        text=True,
    ).strip()
    return float(out)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    if not SRC_PIC.exists():
        raise SystemExit(f"STOP: missing picture {SRC_PIC}")
    got = sha256(SRC_PIC)
    if got != SRC_SHA:
        raise SystemExit(f"STOP: v03 sha mismatch\n  want {SRC_SHA}\n  got  {got}")
    for p in VO_FILES.values():
        if not p.exists():
            raise SystemExit(f"STOP: missing VO {p}")
    if not BED_SECT1.exists():
        raise SystemExit(f"STOP: missing section-1 bed {BED_SECT1}")
    if not BED_SECT2.exists():
        raise SystemExit(f"STOP: missing section-2 bed {BED_SECT2}")

    s1_dur = probe_dur(BED_SECT1)
    s2_dur = probe_dur(BED_SECT2)
    print(f"BED1 {BED_SECT1.name} {s1_dur:.3f}s", flush=True)
    print(f"BED2 {BED_SECT2.name} {s2_dur:.3f}s", flush=True)

    # Section 1 must cover through the crossfade without looping
    sect1_need = CARD05 + XFADE
    if s1_dur + 0.05 < sect1_need:
        raise SystemExit(
            f"STOP: section-1 bed too short for card05+xfade "
            f"({s1_dur:.3f}s < {sect1_need:.3f}s) — do not loop"
        )
    cream_end = CREAM_AT + CREAM_DUR
    sect2_need = cream_end - CARD05  # from card start through cream end
    if s2_dur + 0.05 < sect2_need:
        raise SystemExit(
            f"STOP: section-2 bed too short "
            f"({s2_dur:.3f}s < {sect2_need:.3f}s needed) — do not loop"
        )

    work = Path(tempfile.mkdtemp(prefix="hos_004_full_v03_"))
    print(f"WORK {work}", flush=True)

    # --- Full-timeline VO (silence under cards / cream / hold) ---
    inputs: list[str] = []
    filters: list[str] = []
    labels: list[str] = []
    for i, (pid, start) in enumerate(PART_STARTS.items()):
        inputs += ["-i", str(VO_FILES[pid])]
        ms = int(round(start * 1000))
        lab = f"vo{pid}"
        filters.append(
            f"[{i}:a]aformat=sample_rates=48000:channel_layouts=stereo,"
            f"adelay={ms}|{ms},apad=whole_dur={TOTAL:.6f}[{lab}]"
        )
        labels.append(f"[{lab}]")
    n = len(labels)
    filters.append(
        f"{''.join(labels)}amix=inputs={n}:duration=first:dropout_transition=0:normalize=0,"
        f"atrim=0:{TOTAL:.6f},asetpts=PTS-STARTPTS[vo]"
    )
    vo_wav = work / "vo_timeline.wav"
    ff(*inputs, "-filter_complex", ";".join(filters), "-map", "[vo]", str(vo_wav))
    print(f"  VO timeline {probe_dur(vo_wav):.3f}s", flush=True)

    # --- Two-section bed, acrossfade under card05, fade across cream, silence under hold ---
    # No stream_loop. Sect1 plays 0 → CARD05+XFADE with fade-out in last XFADE.
    # Sect2 is delayed to CARD05, fade-in XFADE, covers through cream_end.
    bed_joined = work / "bed_two_section.wav"
    ms_card = int(round(CARD05 * 1000))
    fade_st = CREAM_AT
    fade_d = CREAM_DUR
    bed_fc = (
        f"[0:a]aformat=sample_rates=48000:channel_layouts=stereo,"
        f"atrim=0:{sect1_need:.6f},asetpts=PTS-STARTPTS,"
        f"afade=t=out:st={CARD05:.6f}:d={XFADE:.6f}[s1];"
        f"[1:a]aformat=sample_rates=48000:channel_layouts=stereo,"
        f"atrim=0:{sect2_need:.6f},asetpts=PTS-STARTPTS,"
        f"afade=t=in:st=0:d={XFADE:.6f},"
        f"adelay={ms_card}|{ms_card}[s2];"
        f"[s1][s2]amix=inputs=2:weights=1 1:normalize=0:duration=longest:dropout_transition=0,"
        f"atrim=0:{cream_end:.6f},asetpts=PTS-STARTPTS,"
        f"volume={BED_VOLUME:.8f},"
        f"afade=t=out:st={fade_st:.6f}:d={fade_d:.6f},"
        f"apad=whole_dur={TOTAL:.6f},atrim=0:{TOTAL:.6f},asetpts=PTS-STARTPTS[bed]"
    )
    ff(
        "-i", str(BED_SECT1),
        "-i", str(BED_SECT2),
        "-filter_complex", bed_fc,
        "-map", "[bed]",
        str(bed_joined),
    )
    print(
        f"  BED two-section card05={CARD05:.3f} xfade={XFADE:.2f}s "
        f"active→{cream_end:.3f}s (no loop)",
        flush=True,
    )

    # --- Mix VO + ducked bed ---
    mixed = work / "mix.wav"
    fc = (
        f"[0:a]aformat=sample_rates=48000:channel_layouts=stereo,asplit=2[vo_sc][vo_mix];"
        f"[1:a]aformat=sample_rates=48000:channel_layouts=stereo[bed];"
        f"[bed][vo_sc]sidechaincompress={SIDECHAIN}[ducked];"
        f"[vo_mix][ducked]amix=inputs=2:weights=1 1:normalize=0:duration=first:dropout_transition=0,"
        f"alimiter=limit=0.8912509:level=false,atrim=0:{TOTAL:.6f},asetpts=PTS-STARTPTS[a]"
    )
    ff("-i", str(vo_wav), "-i", str(bed_joined), "-filter_complex", fc, "-map", "[a]", str(mixed))
    print(f"  MIX {probe_dur(mixed):.3f}s", flush=True)

    # --- Mux picture + mix ---
    pre_cfr = work / "full_v03_pre_cfr.mp4"
    ff(
        "-i", str(SRC_PIC), "-i", str(mixed),
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-ac", "2",
        "-shortest",
        "-movflags", "+faststart",
        str(pre_cfr),
    )

    streams = json.loads(
        subprocess.check_output(
            [
                "ffprobe", "-v", "error",
                "-show_entries", "stream=codec_type,duration",
                "-of", "json", str(pre_cfr),
            ],
            text=True,
        )
    )
    v_dur = a_dur = None
    for s in streams["streams"]:
        if s["codec_type"] == "video":
            v_dur = float(s.get("duration") or 0)
        if s["codec_type"] == "audio":
            a_dur = float(s.get("duration") or 0)
    assert v_dur and a_dur
    delta = a_dur - v_dur
    print(f"PRE_SYNC v={v_dur:.6f} a={a_dur:.6f} delta={delta:.6f}", flush=True)
    synced = work / "full_v03_synced.mp4"
    if abs(delta) <= 0.033:
        synced = pre_cfr
    elif delta > 0:
        ff(
            "-i", str(pre_cfr),
            "-filter_complex", f"[0:a]atrim=0:{v_dur:.6f},asetpts=PTS-STARTPTS[a]",
            "-map", "0:v", "-map", "[a]",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "320k", "-ar", "48000",
            "-movflags", "+faststart",
            str(synced),
        )
    else:
        pad = -delta
        ff(
            "-i", str(pre_cfr),
            "-filter_complex", f"[0:a]apad=pad_dur={pad:.6f}[a]",
            "-map", "0:v", "-map", "[a]",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "320k", "-ar", "48000",
            "-t", f"{v_dur:.6f}",
            "-movflags", "+faststart",
            str(synced),
        )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    tmp_out = work / "full_v03_cfr.mp4"
    info = remaster_cfr(synced, tmp_out, fps=None, copy_audio=True)
    print(f"CFR {info}", flush=True)
    subprocess.run(["cp", "-f", str(tmp_out), str(OUT)], check=True)

    digest = sha256(OUT)
    dur = probe_dur(OUT)
    size = OUT.stat().st_size
    print(f"SAVED {OUT}", flush=True)
    print(f"SHA256 {digest}", flush=True)
    print(f"DUR {dur:.3f}", flush=True)

    streams = json.loads(
        subprocess.check_output(
            [
                "ffprobe", "-v", "error",
                "-show_entries", "stream=codec_type,duration",
                "-of", "json", str(OUT),
            ],
            text=True,
        )
    )
    v_dur = a_dur = None
    for s in streams["streams"]:
        if s["codec_type"] == "video":
            v_dur = float(s.get("duration") or 0)
        if s["codec_type"] == "audio":
            a_dur = float(s.get("duration") or 0)
    sync_delta = (a_dur or 0) - (v_dur or 0)
    print(f"SYNC_DELTA {sync_delta:.6f}", flush=True)

    ICLOUD_DIR.mkdir(parents=True, exist_ok=True)
    dest = ICLOUD_DIR / OUT.name
    tmp = ICLOUD_DIR / f"{OUT.name}.copying"
    subprocess.run(["cp", "-f", str(OUT), str(tmp)], check=True)
    tmp.replace(dest)
    print(f"ICLOUD {dest} sha={digest}", flush=True)

    meta = {
        "file": OUT.name,
        "sha256": digest,
        "duration": dur,
        "bytes": size,
        "sync_delta_a_minus_v": sync_delta,
        "picture_source": SRC_PIC.name,
        "picture_sha256": SRC_SHA,
        "bed_section_1": BED_SECT1.name,
        "bed_section_1_sha256": sha256(BED_SECT1),
        "bed_section_2": BED_SECT2.name,
        "bed_section_2_sha256": sha256(BED_SECT2),
        "bed_join_at": CARD05,
        "bed_xfade_s": XFADE,
        "bed_loop": False,
        "bed_rel_db": BED_REL_DB,
        "sidechain": SIDECHAIN,
        "sidechain_note": "extra ~3 dB duck under speech vs ungated −20 dB gap level",
        "amix": "inputs=2:weights=1 1:normalize=0",
        "cream_at": CREAM_AT,
        "cream_fade_s": CREAM_DUR,
        "hold_silent_s": HOLD_DUR,
        "part_starts": PART_STARTS,
        "vo": {k: v.name for k, v in VO_FILES.items()},
        "status": "UAT_MUSIC_FOR_BEN",
        "keep_locked_label": False,
        "upload": False,
    }
    META.write_text(json.dumps(meta, indent=2) + "\n")

    watch = (
        "WATCH THIS FILE (HOS 004 full_v03 — two-section bed, no loop):\n"
        f"  {OUT.name}\n"
        f"  sha256: {digest}\n"
        f"  duration: {dur:.3f}s · A/V Δ {sync_delta:.6f}s\n"
        f"  picture: {SRC_PIC.name} (Ben PASS v03)\n"
        f"  bed: {BED_SECT1.name} → card05 {CARD05:.2f}s xfade {XFADE:.1f}s → "
        f"{BED_SECT2.name} → cream fade (NO LOOP)\n"
        f"  gap −20 dB · extra ~3 dB duck under speech · amix normalize=0\n\n"
        "Listen to the music join at the Part 05 chapter card. Do NOT mark KEEP.\n"
        "No upload. Also pick thumbnail A/B/C.\n"
    )
    WATCH.write_text(watch)
    wtmp = ICLOUD_DIR / "WATCH_full_v03.txt.copying"
    wtmp.write_text(watch)
    wtmp.replace(ICLOUD_DIR / "WATCH_full_v03.txt")

    NOTES.write_text(
        f"""# HOS 004 full_v03 — two-section music (UAT)

**Cut:** `{OUT.name}`  
**sha256:** `{digest}`  
**Duration:** {dur:.3f} s · **A/V Δ:** {sync_delta:.6f} s  
**Status:** UAT for Ben music listen. Do **not** label KEEP. No upload.

Picture locked from `hos_004_full_join_v03.mp4` (Ben PASS 29 Sep, sha `{SRC_SHA}`).  
VO v04 masters untouched.

## Music (no loop)

| Section | File | Window |
|---|---|---|
| 1 | `{BED_SECT1.name}` | 0:00 → Part 05 chapter card ({CARD05:.3f} s = 5:55.48) |
| 2 | `{BED_SECT2.name}` | card → cream end ({cream_end:.3f} s) |
| Join | acrossfade **{XFADE:.1f} s** under the Part 05 chapter card | — |

Gap level **−20 dB**. Extra ~3 dB duck under speech (`{SIDECHAIN}`).  
`amix=inputs=2:weights=1 1:normalize=0`. Fade across cream · silent under 20 s hold.

Builder: `07_Edit-Project/_mix_hos_004_full_v03_music.py`
"""
    )
    print("DONE_BUILD", flush=True)


if __name__ == "__main__":
    main()
