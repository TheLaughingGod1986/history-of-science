#!/usr/bin/env python3
"""HOS 004 full join v02 — seamless seams (Ben FAIL on v01).

Fixes vs v01:
  1) Strip the baked P01 bridge plate (17_ledger_bridge @ 68.48) that shows
     on-screen "BRIDGES TO PART 02 / CHAPTER CARD"; extend plate 16 instead.
  2) No chapter/bridge cards anywhere.
  3) Trim part A/V to speech; ~0.45 s VO gap between parts (in-part median).
  4) ONE continuous TEMP bed (acrossfade of part beds) + sidechain duck — no
     bed restart at seams.
  5) J-cut: next VO starts ~0.5 s before its picture; 0.5 s picture dissolve.
  6) Cream end card (from P05) then 20 s Studio hold.

No remint. No script text changes. Do not label KEEP/LOCKED.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
import time
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
EXP = PROJ / "09_Final-Export"
EDIT = PROJ / "07_Edit-Project"
MUSIC = PROJ / "05_Music"
VO_DIR = PROJ / "02_Voiceover/05_Master"
CREAM_PNG = PROJ / "04_Generated-Clips/part05/refs/hos_end_card_v01.png"
ICLOUD_DIR = (
    Path.home()
    / "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT"
    / "004_Whats-Really-Inside-An-Atom"
    / "09_Final-Export"
)
OUT = EXP / "hos_004_full_join_v02.mp4"
NOTES = EXP / "FULL_JOIN_V02_NOTES.md"
META = EDIT / "full_join_v02_land_meta.json"
WATCH = EDIT / "WATCH_full_join_v02.txt"

# Seam grammar
GAP = 0.45          # VO gap between parts (~in-part median)
J_LEAD = 0.50       # next VO before its picture
XFADE = 0.50        # picture dissolve
END_HOLD = 20.0
P01_BRIDGE_CUT = 68.48   # plate 17_ledger_bridge start — reject text card
P05_CREAM_IN = 140.5     # part-local (pre J-trim)

BED_REL_DB = -20.0
BED_VOLUME = 10 ** (BED_REL_DB / 20.0)
SIDECHAIN = "threshold=0.018:ratio=8:attack=20:release=500:level_sc=1"
BED_ACROSS = 2.0

PARENTS = [
    {
        "id": "01",
        "name": "hos_004_part01_rough_v05.mp4",
        "sha": "71d7c70798c77ce2ecb02c37ad043fd98117a2209a84899236337fee8b952add",
        "vo": "hos_004_part01_vo_v04.wav",
        "bed": "hos004-part01-temp_score_bed_v01.mp3",
        "bridge_cut": P01_BRIDGE_CUT,
    },
    {
        "id": "02",
        "name": "hos_004_part02_rough_v01.mp4",
        "sha": "620ce51250028495a588f25967dddfaa9c6136dc4172c7b0ce1ee609f103f1d2",
        "vo": "hos_004_part02_vo_v04.wav",
        "bed": "hos004-part02-temp_score_bed_v01.mp3",
        "bridge_cut": None,
    },
    {
        "id": "03",
        "name": "hos_004_part03_rough_v01.mp4",
        "sha": "d62e0ed096ead8ec52666ca07476f973aeaae7635b70a16faaac45f14ec518e0",
        "vo": "hos_004_part03_vo_v04.wav",
        "bed": "hos004-part03-temp_score_bed_v01.mp3",
        "bridge_cut": None,
    },
    {
        "id": "04",
        "name": "hos_004_part04_rough_v02.mp4",
        "sha": "157feaef7bd21236aeafc3e953fe461fe2ee95896bb868d57357c9c1c2c1e1f5",
        "vo": "hos_004_part04_vo_v04.wav",
        "bed": "hos004-part04-temp_score_bed_v01.mp3",
        "bridge_cut": None,
    },
    {
        "id": "05",
        "name": "hos_004_part05_rough_v03.mp4",
        "sha": "b391bff0dbe8a8ae0130adef4f7f3d7b79aca2cb34a934d9cf42d76e1d03363f",
        "vo": "hos_004_part05_vo_v04.wav",
        "bed": "hos004-part05-temp_score_bed_v01.mp3",
        "bridge_cut": None,
    },
]

ENC = [
    "-c:v", "libx264", "-pix_fmt", "yuv420p",
    "-profile:v", "high", "-level", "4.1",
    "-preset", "fast", "-crf", "18", "-r", "30",
    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
    "-movflags", "+faststart",
]


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def probe_dur(p: Path) -> float:
    r = subprocess.run(
        [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(p),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(r.stdout.strip())


def probe_streams(p: Path) -> dict:
    r = subprocess.run(
        [
            "ffprobe", "-v", "error",
            "-show_entries", "stream=codec_type,duration,width,height,r_frame_rate",
            "-of", "json", str(p),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(r.stdout)


def ff(*args: str) -> None:
    subprocess.run(
        ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *args],
        check=True,
    )


def fmt_tc(seconds: float) -> str:
    s = max(0.0, seconds)
    m = int(s // 60)
    rem = s - 60 * m
    return f"{m}:{rem:05.2f}"


def speech_bounds(wav: Path, thresh_db: float = -38.0) -> tuple[float, float, float]:
    """Return (first_speech, last_speech, file_dur) seconds."""
    import struct
    import wave

    with wave.open(str(wav), "rb") as w:
        sr = w.getframerate()
        ch = w.getnchannels()
        sw = w.getsampwidth()
        n = w.getnframes()
        raw = w.readframes(n)
    if sw != 2:
        raise SystemExit(f"STOP: expected 16-bit wav, got sw={sw} for {wav}")
    samples = struct.unpack("<" + "h" * (len(raw) // 2), raw)
    if ch == 2:
        mono = [(samples[i] + samples[i + 1]) / 2 for i in range(0, len(samples), 2)]
    else:
        mono = list(samples)
    thresh = (10 ** (thresh_db / 20.0)) * 32768.0
    first = next((i for i, s in enumerate(mono) if abs(s) > thresh), 0)
    last = len(mono) - 1 - next(
        (i for i, s in enumerate(reversed(mono)) if abs(s) > thresh), 0
    )
    dur = len(mono) / sr
    return first / sr, last / sr, dur


def main() -> None:
    if not CREAM_PNG.exists():
        raise SystemExit(f"STOP: missing cream {CREAM_PNG}")

    print("HASH CHECK", flush=True)
    for item in PARENTS:
        exp = EXP / item["name"]
        if not exp.exists():
            raise SystemExit(f"STOP: missing {exp}")
        got = sha256(exp)
        if got != item["sha"]:
            raise SystemExit(f"STOP: hash mismatch {item['name']}")
        print(f"  OK {item['id']} {probe_dur(exp):.3f}s", flush=True)

    work = Path(tempfile.mkdtemp(prefix="hos_004_join_v02_"))
    print(f"WORK {work}", flush=True)

    # --- Per-part VO trims (tight speech, tiny pad) ---
    vo_info: list[dict] = []
    for item in PARENTS:
        wav = VO_DIR / item["vo"]
        first, last, file_dur = speech_bounds(wav)
        # Keep a hair of lead-in; trim empty trail
        t0 = max(0.0, first - 0.04)
        t1 = min(file_dur, last + 0.06)
        out = work / f"vo_{item['id']}.wav"
        ff(
            "-i", str(wav),
            "-ss", f"{t0:.6f}", "-to", f"{t1:.6f}",
            "-ar", "48000", "-ac", "2",
            str(out),
        )
        vd = probe_dur(out)
        vo_info.append(
            {
                "id": item["id"],
                "path": out,
                "dur": vd,
                "src_t0": t0,
                "src_t1": t1,
                "file_dur": file_dur,
                "first": first,
                "last": last,
            }
        )
        print(
            f"  VO {item['id']} trim {t0:.3f}→{t1:.3f} ({vd:.3f}s) "
            f"speech {first:.3f}–{last:.3f}",
            flush=True,
        )

    # --- Per-part silent picture (strip baked VO+bed) ---
    vid_clips: list[Path] = []
    vid_meta: list[dict] = []
    for idx, item in enumerate(PARENTS):
        src = EXP / item["name"]
        vo_d = vo_info[idx]["dur"]
        raw = work / f"vid_{item['id']}_raw.mp4"
        # Normalize video-only; take full parent picture then reshape
        ff(
            "-i", str(src),
            "-an",
            "-vf", "fps=30,scale=1920:1080:flags=lanczos,format=yuv420p,setsar=1",
            "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-r", "30",
            "-movflags", "+faststart",
            str(raw),
        )
        parent_vd = probe_dur(raw)

        # P01: cut bridge text plate, extend prior plate
        if item["bridge_cut"] is not None:
            cut = min(item["bridge_cut"], parent_vd)
            trimmed = work / f"vid_{item['id']}_nobridge.mp4"
            ff(
                "-i", str(raw),
                "-t", f"{cut:.6f}",
                "-c:v", "libx264", "-preset", "fast", "-crf", "18",
                "-pix_fmt", "yuv420p", "-r", "30",
                str(trimmed),
            )
            # Extend to VO length (freeze last good frame of plate 16)
            base = work / f"vid_{item['id']}_base.mp4"
            ff(
                "-i", str(trimmed),
                "-vf", f"tpad=stop_mode=clone:stop_duration={max(0.0, vo_d - cut) + 0.05:.6f}",
                "-t", f"{vo_d:.6f}",
                "-c:v", "libx264", "-preset", "fast", "-crf", "18",
                "-pix_fmt", "yuv420p", "-r", "30",
                str(base),
            )
            print(
                f"  VID {item['id']} bridge-cut @{cut:.3f} → extend to {vo_d:.3f}s",
                flush=True,
            )
        else:
            # Match VO duration (trim or tiny pad)
            base = work / f"vid_{item['id']}_base.mp4"
            if parent_vd >= vo_d - 0.01:
                ff(
                    "-i", str(raw),
                    "-t", f"{vo_d:.6f}",
                    "-c:v", "libx264", "-preset", "fast", "-crf", "18",
                    "-pix_fmt", "yuv420p", "-r", "30",
                    str(base),
                )
            else:
                ff(
                    "-i", str(raw),
                    "-vf", f"tpad=stop_mode=clone:stop_duration={vo_d - parent_vd + 0.05:.6f}",
                    "-t", f"{vo_d:.6f}",
                    "-c:v", "libx264", "-preset", "fast", "-crf", "18",
                    "-pix_fmt", "yuv420p", "-r", "30",
                    str(base),
                )
            print(f"  VID {item['id']} base {vo_d:.3f}s", flush=True)

        # J-cut video handling:
        # parts 2–5: skip first J_LEAD of picture (heard under prior hold);
        #   then pad end by J_LEAD so length still equals VO.
        # parts 1–4: after that, extend by GAP+J_LEAD+XFADE for hold+dissolve.
        if idx == 0:
            content = base
            content_dur = vo_d
        else:
            trimmed = work / f"vid_{item['id']}_jtrim.mp4"
            # Drop first J_LEAD of picture; freeze-extend tail to keep VO length
            ff(
                "-ss", f"{J_LEAD:.6f}",
                "-i", str(base),
                "-vf", f"tpad=stop_mode=clone:stop_duration={J_LEAD + 0.05:.6f}",
                "-t", f"{vo_d:.6f}",
                "-c:v", "libx264", "-preset", "fast", "-crf", "18",
                "-pix_fmt", "yuv420p", "-r", "30",
                str(trimmed),
            )
            content = trimmed
            content_dur = vo_d
            print(f"  VID {item['id']} J-trim start {J_LEAD:.2f}s (sync lock)", flush=True)

        if idx < len(PARENTS) - 1:
            ext = GAP + J_LEAD + XFADE
            final = work / f"vid_{item['id']}_seg.mp4"
            ff(
                "-i", str(content),
                "-vf", f"tpad=stop_mode=clone:stop_duration={ext + 0.05:.6f}",
                "-t", f"{content_dur + ext:.6f}",
                "-c:v", "libx264", "-preset", "fast", "-crf", "18",
                "-pix_fmt", "yuv420p", "-r", "30",
                # silent audio placeholder so later filters are video-only
                "-an",
                str(final),
            )
            print(f"  VID {item['id']} +hold/xfade ext {ext:.2f}s → {content_dur + ext:.3f}s", flush=True)
        else:
            final = work / f"vid_{item['id']}_seg.mp4"
            ff(
                "-i", str(content),
                "-c:v", "libx264", "-preset", "fast", "-crf", "18",
                "-pix_fmt", "yuv420p", "-r", "30",
                "-an",
                str(final),
            )

        vid_clips.append(final)
        vid_meta.append(
            {
                "id": item["id"],
                "content_dur": content_dur,
                "seg_dur": probe_dur(final),
                "bridge_cut": item["bridge_cut"],
            }
        )

    # --- Picture xfade chain ---
    print("PICTURE XFADE", flush=True)
    n = len(vid_clips)
    vchain: list[str] = []
    running = 0.0
    seam_dissolve_start: list[float] = []
    for i in range(n - 1):
        running += vid_meta[i]["seg_dur"]
        off = running - (i + 1) * XFADE
        seam_dissolve_start.append(off)
        vin = "[0:v]" if i == 0 else f"[vx{i}]"
        vout = "vstory" if i == n - 2 else f"vx{i+1}"
        vchain.append(
            f"{vin}[{i+1}:v]xfade=transition=fade:duration={XFADE:.3f}:offset={off:.6f}[{vout}]"
        )
        print(f"  seam {i+1}→{i+2} dissolve@{off:.3f}", flush=True)

    story_vid = work / "story_vid.mp4"
    args: list[str] = []
    for p in vid_clips:
        args += ["-i", str(p)]
    ff(
        *args,
        "-filter_complex", ";".join(vchain),
        "-map", "[vstory]",
        "-an",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-pix_fmt", "yuv420p", "-r", "30",
        str(story_vid),
    )
    story_vd = probe_dur(story_vid)
    print(f"  story picture {story_vd:.3f}s", flush=True)

    # --- Continuous VO with gaps ---
    print("VO CONCAT", flush=True)
    vo_wav = work / "vo_continuous.wav"
    gap_wav = work / "gap.wav"
    ff(
        "-f", "lavfi", "-i", f"anullsrc=r=48000:cl=stereo",
        "-t", f"{GAP:.6f}",
        str(gap_wav),
    )
    concat_list = work / "vo_concat.txt"
    lines = []
    for i, info in enumerate(vo_info):
        lines.append(f"file '{info['path']}'")
        if i < len(vo_info) - 1:
            lines.append(f"file '{gap_wav}'")
    concat_list.write_text("\n".join(lines) + "\n")
    ff(
        "-f", "concat", "-safe", "0", "-i", str(concat_list),
        "-ar", "48000", "-ac", "2",
        str(vo_wav),
    )
    vo_total = probe_dur(vo_wav)
    print(f"  VO continuous {vo_total:.3f}s", flush=True)

    # VO start times on timeline
    vo_starts = []
    t = 0.0
    for i, info in enumerate(vo_info):
        vo_starts.append(t)
        t += info["dur"]
        if i < len(vo_info) - 1:
            t += GAP

    # Picture seam = dissolve start; part picture fully on at dissolve_start + XFADE
    # From construction: dissolve_start for seam i = vo_starts[i+1] + J_LEAD - XFADE? 
    # Verify against seam_dissolve_start
    print("  VO starts:", [f"{s:.3f}" for s in vo_starts], flush=True)
    print("  dissolve starts:", [f"{s:.3f}" for s in seam_dissolve_start], flush=True)

    # --- Continuous bed (acrossfade part beds, then pad/trim) ---
    print("BED CONTINUOUS", flush=True)
    bed_paths = [MUSIC / p["bed"] for p in PARENTS]
    for bp in bed_paths:
        if not bp.exists():
            raise SystemExit(f"STOP: missing bed {bp}")
    # Normalize each bed then acrossfade chain
    bed_norm: list[Path] = []
    for i, bp in enumerate(bed_paths):
        bn = work / f"bed_{i}.wav"
        ff("-i", str(bp), "-ar", "48000", "-ac", "2", str(bn))
        bed_norm.append(bn)
    # Chain acrossfade
    if len(bed_norm) == 1:
        bed_joined = bed_norm[0]
    else:
        cur = bed_norm[0]
        for i in range(1, len(bed_norm)):
            nxt = work / f"bed_acc_{i}.wav"
            d0 = probe_dur(cur)
            # acrossfade consumes BED_ACROSS from each end
            ff(
                "-i", str(cur), "-i", str(bed_norm[i]),
                "-filter_complex",
                f"[0:a][1:a]acrossfade=d={BED_ACROSS:.3f}:c1=tri:c2=tri[a]",
                "-map", "[a]",
                str(nxt),
            )
            cur = nxt
            print(f"  bed acrossfade +part{i+1} (prev {d0:.1f}s)", flush=True)
        bed_joined = cur
    bed_len = probe_dur(bed_joined)
    # Target: story picture + cream hold
    target_bed = story_vd + END_HOLD + 1.0
    bed_full = work / "bed_full.wav"
    if bed_len >= target_bed:
        ff("-i", str(bed_joined), "-t", f"{target_bed:.6f}", str(bed_full))
    else:
        # loop with acrossfade soft join
        loops_needed = int(target_bed / max(1.0, bed_len - BED_ACROSS)) + 2
        loop_list = work / "bed_loop.txt"
        loop_list.write_text(("file '%s'\n" % bed_joined) * loops_needed)
        bed_looped = work / "bed_looped.wav"
        ff(
            "-f", "concat", "-safe", "0", "-i", str(loop_list),
            "-t", f"{target_bed:.6f}",
            str(bed_looped),
        )
        # Soften obvious loop points by a light afade only at very start/end later
        bed_full = bed_looped
        print(f"  bed looped to {target_bed:.1f}s", flush=True)
    print(f"  bed ready {probe_dur(bed_full):.3f}s", flush=True)

    # --- Cream 20s hold ---
    cream = work / "cream_hold_20s.mp4"
    ff(
        "-loop", "1", "-i", str(CREAM_PNG),
        "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
        "-vf", "fps=30,scale=1920:1080:flags=lanczos,format=yuv420p,setsar=1",
        "-t", f"{END_HOLD:.6f}",
        "-shortest",
        *ENC,
        str(cream),
    )

    # Append cream hold to story picture (hard concat — identical cream)
    picture = work / "picture_full.mp4"
    ff(
        "-i", str(story_vid), "-i", str(cream),
        "-filter_complex", "[0:v][1:v]concat=n=2:v=1:a=0[v]",
        "-map", "[v]",
        "-an",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-pix_fmt", "yuv420p", "-r", "30",
        str(picture),
    )
    pic_dur = probe_dur(picture)
    print(f"PICTURE+CREAM {pic_dur:.3f}s", flush=True)

    # --- Final mix: picture + VO + ducked continuous bed ---
    print("FINAL MIX", flush=True)
    # Pad VO with silence to picture length (cream hold is silent VO)
    vo_pad = max(0.0, pic_dur - vo_total)
    final_tmp = work / "full_v02.mp4"
    fc = (
        f"[1:a]apad=pad_dur={vo_pad:.6f},atrim=0:{pic_dur:.6f},asetpts=PTS-STARTPTS,"
        f"aformat=sample_rates=48000:channel_layouts=stereo[vo];"
        f"[2:a]atrim=0:{pic_dur:.6f},asetpts=PTS-STARTPTS,"
        f"aformat=sample_rates=48000:channel_layouts=stereo,"
        f"volume={BED_VOLUME:.8f}[bed];"
        f"[bed][vo]sidechaincompress={SIDECHAIN}[ducked];"
        f"[vo][ducked]amix=inputs=2:duration=first:dropout_transition=0,"
        f"alimiter=limit=0.8912509:level=false[a];"
        f"[0:v]fps=30,format=yuv420p,setsar=1[v]"
    )
    ff(
        "-i", str(picture),
        "-i", str(vo_wav),
        "-i", str(bed_full),
        "-filter_complex", fc,
        "-map", "[v]", "-map", "[a]",
        "-t", f"{pic_dur:.6f}",
        *ENC,
        str(final_tmp),
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["cp", "-f", str(final_tmp), str(OUT)], check=True)

    digest = sha256(OUT)
    dur = probe_dur(OUT)
    size = OUT.stat().st_size
    streams = probe_streams(OUT)
    v_dur = a_dur = None
    for s in streams.get("streams", []):
        if s.get("codec_type") == "video":
            v_dur = float(s.get("duration") or 0) or None
        if s.get("codec_type") == "audio":
            a_dur = float(s.get("duration") or 0) or None
    sync_delta = (a_dur - v_dur) if (a_dur and v_dur) else None

    # Seam report
    # Part picture fully-on times:
    # P01 at 0
    # P0k fully on at seam_dissolve_start[k-2] + XFADE  (1-indexed: seam 01→02 is index 0)
    part_pic_in = {"01": 0.0}
    for i in range(1, 5):
        part_pic_in[f"0{i+1}"] = seam_dissolve_start[i - 1] + XFADE

    cream_in_abs = part_pic_in["05"] + max(0.0, P05_CREAM_IN - J_LEAD)
    # P05 video was J-trimmed by J_LEAD, so cream at part-local 140.5 appears at 140.5 - J_LEAD into P05 picture,
    # and P05 picture starts at part_pic_in['05']
    cream_in_abs = part_pic_in["05"] + (P05_CREAM_IN - J_LEAD)
    end_hold_in = story_vd  # cream hold concat after story
    # story_vd already includes P05 through its cream; end_hold is the extra 20s

    print(f"SAVED {OUT}", flush=True)
    print(f"SHA256 {digest}", flush=True)
    print(f"DUR {dur:.3f}", flush=True)
    print(f"SYNC_DELTA {sync_delta}", flush=True)
    for i in range(4):
        a = f"0{i+1}"
        b = f"0{i+2}"
        print(
            f"SEAM {a}→{b}  VO_next@{vo_starts[i+1]:.3f}  "
            f"dissolve@{seam_dissolve_start[i]:.3f}  "
            f"pic_full@{part_pic_in[b]:.3f}",
            flush=True,
        )
    print(f"CREAM_IN {cream_in_abs:.3f}", flush=True)
    print(f"END_HOLD_IN {end_hold_in:.3f}", flush=True)

    watch = (
        "WATCH THIS FILE (HOS 004 full join v02 — seamless seams):\n"
        f"  {OUT.name}\n"
        f"  iCloud: HOS UAT/004_Whats-Really-Inside-An-Atom/09_Final-Export/{OUT.name}\n\n"
        f"sha256={digest}\n"
        f"duration={dur:.3f}\n"
        f"bytes={size}\n"
        "P01 bridge text plate REMOVED. No chapter cards.\n"
        f"VO gap {GAP:.2f}s · J-lead {J_LEAD:.2f}s · picture xfade {XFADE:.2f}s · continuous TEMP bed.\n"
        "Do NOT label KEEP/LOCKED. STOP for Ben.\n"
    )
    WATCH.write_text(watch)

    lines = [
        "# HOS 004 full join v02 — seamless seams (UAT)",
        "",
        f"**Cut:** `{OUT.name}`",
        f"**sha256:** `{digest}`",
        f"**Duration:** {dur:.3f} s · **Size:** {size} B",
        "**Status:** UAT for Ben after v01 FAIL (abrupt seams + bridge text card). "
        "Do **not** label KEEP/LOCKED. Do **not** upload.",
        "",
        "## Fixes vs v01",
        "",
        "- Removed P01 `17_ledger_bridge` (on-screen “BRIDGES TO PART 02 / CHAPTER CARD”); extended plate 16.",
        "- No chapter / bridge cards.",
        f"- VO gaps ~{GAP:.2f}s between parts (match in-part line gaps).",
        "- One continuous TEMP bed (acrossfaded part beds) + sidechain duck — no bed restart at seams.",
        f"- J-cut: next VO leads picture by ~{J_LEAD:.2f}s; picture dissolve {XFADE:.2f}s.",
        "- Cream card then 20 s Studio end hold.",
        "",
        "## Parents (hash-checked, not reminted)",
        "",
        "| Part | File | sha256 |",
        "|---|---|---|",
    ]
    for item in PARENTS:
        lines.append(f"| {item['id']} | `{item['name']}` | `{item['sha']}` |")
    lines += [
        "",
        "## Seams",
        "",
        "| Seam | Next VO in | Dissolve in | Next picture full |",
        "|---|---:|---:|---:|",
    ]
    for i in range(4):
        a, b = f"0{i+1}", f"0{i+2}"
        lines.append(
            f"| {a}→{b} | {fmt_tc(vo_starts[i+1])} ({vo_starts[i+1]:.3f}) | "
            f"{fmt_tc(seam_dissolve_start[i])} ({seam_dissolve_start[i]:.3f}) | "
            f"{fmt_tc(part_pic_in[b])} ({part_pic_in[b]:.3f}) |"
        )
    lines += [
        "",
        f"| Cream card | {fmt_tc(cream_in_abs)} ({cream_in_abs:.3f}) |",
        f"| 20 s Studio hold | {fmt_tc(end_hold_in)} ({end_hold_in:.3f}) |",
        f"| Film out | {fmt_tc(dur)} ({dur:.3f}) |",
        "",
        f"A/V sync delta (audio−video): `{sync_delta}`",
        "",
        "Builder: `07_Edit-Project/_join_hos_004_full_v02.py`",
        "",
    ]
    NOTES.write_text("\n".join(lines) + "\n")

    meta = {
        "file": OUT.name,
        "sha256": digest,
        "duration": dur,
        "bytes": size,
        "gap": GAP,
        "j_lead": J_LEAD,
        "xfade": XFADE,
        "end_hold_s": END_HOLD,
        "p01_bridge_cut": P01_BRIDGE_CUT,
        "vo_starts": {f"0{i+1}": vo_starts[i] for i in range(5)},
        "dissolve_starts": {
            f"0{i+1}→0{i+2}": seam_dissolve_start[i] for i in range(4)
        },
        "part_picture_full": part_pic_in,
        "cream_in_abs": cream_in_abs,
        "end_hold_in": end_hold_in,
        "video_duration": v_dur,
        "audio_duration": a_dur,
        "sync_delta_a_minus_v": sync_delta,
        "parents": PARENTS,
        "status": "UAT_FOR_BEN",
        "keep_locked_label": False,
        "upload": False,
        "supersedes": "hos_004_full_join_v01.mp4",
        "ben_fail_v01": "abrupt seams + Bridges to Part 02 / Chapter Card text",
    }
    META.write_text(json.dumps(meta, indent=2) + "\n")

    # iCloud
    ICLOUD_DIR.mkdir(parents=True, exist_ok=True)
    dest = ICLOUD_DIR / OUT.name
    for attempt in range(1, 5):
        try:
            tmp_dest = ICLOUD_DIR / f"{OUT.name}.copying"
            subprocess.run(["cp", "-f", str(OUT), str(tmp_dest)], check=True)
            tmp_dest.replace(dest)
            break
        except OSError:
            if attempt == 4:
                raise
            time.sleep(2 * attempt)
    # verify
    for attempt in range(1, 6):
        try:
            icloud_sha = sha256(dest)
            break
        except OSError:
            time.sleep(2 * attempt)
    else:
        icloud_sha = None
    print(f"ICLOUD {dest}", flush=True)
    print(f"ICLOUD_SHA {icloud_sha}", flush=True)
    if icloud_sha and icloud_sha != digest:
        raise SystemExit("STOP: iCloud sha mismatch")
    (ICLOUD_DIR / NOTES.name).write_text(NOTES.read_text())
    (ICLOUD_DIR / WATCH.name).write_text(watch)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
