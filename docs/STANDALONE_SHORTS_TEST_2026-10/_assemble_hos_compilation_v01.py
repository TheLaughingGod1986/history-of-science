#!/usr/bin/env python3
"""HOS compilation film assembler v01 (J0175).

Stages:
  prep  normalise and trim each finished master into render scratch:
        1920x1080, 30 fps (fps=30, frame duplication only), yuv420p, AAC 48 kHz
        stereo, two-pass loudnorm to -14 LUFS / -1 dBTP. Writes prep_report.json.
  plan  write the cut plan (segment order, film-time starts, chapters list draft)
        from prep_report.json where present, else the inventory lengths. Missing
        inputs (006 master, J0204 graphics, intro/bridge plates) are listed, not faked.
  segment  render one VO segment (intro, bridge, closing) from its checked shots:
        0.5 s crossfades between shots, VO at -15 LUFS, the 004 bed 17 LU under it with narration sidechain ducking,
        limiter at -1 dBTP; writes the mp4, VO and bed stems, cuts.json (polish_gate
        format) and segment_report.json. Refuses a segment whose timeline graphic is
        missing unless --draft.

Inputs and trim points: COMPILATION_ASSEMBLY_INVENTORY_v01.md. Masters are read
only; new render scratch is written to the NAS (Chief, 14 Oct).

  python3 _assemble_hos_compilation_v01.py prep [--only 005,001] [--scratch DIR]
  python3 _assemble_hos_compilation_v01.py plan [--scratch DIR] [--out FILE]
  python3 _assemble_hos_compilation_v01.py segment bridge4 [--draft] [--scratch DIR]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
HOS = Path.home() / "YouTube" / "History Of Science"
NAS = Path("/Volumes/data/mac-mini-archive/YouTube/History Of Science/02_Video-Projects")
SCRATCH = Path("/Volumes/data/mac-mini-archive/mini-tmp-scratch/2026-10-15/hos_comp_j0175")
VO_DIR = HOS / "docs/STANDALONE_SHORTS_TEST_2026-10/vo_compilation_v01"
GRAPHICS_DIR = HOS / "docs/STANDALONE_SHORTS_TEST_2026-10/graphics_v01"

TARGET_I, TARGET_TP, TARGET_LRA = -14.0, -1.0, 11.0
TRIM_FADE = 0.25  # audio fade on a trimmed tail; the cut sits in a measured VO pause

# Order by proof year (Chief, J0173). keep_to = None keeps the whole master.
FILMS = [
    {"film": "005", "card": "The Hidden Circle", "keep_to": 489.20,
     "master": Path("/Volumes/data/mac-mini-archive/mini-tmp-scratch/2026-10-21/HOS-005/hos_005_master_v01.mp4"),
     "inv_len": 526.53},
    {"film": "006", "card": "Built From Air", "keep_to": None, "master": NAS / "006_Trees-Are-Made-Of-Air/09_Final-Export/master_v01/hos_006_master_v01.mp4", "inv_len": 508.0,
     "missing": "006 hand-off trim point still needs measurement before final assembly"},
    {"film": "001", "card": "The Invisible Enemy", "keep_to": None,
     "master": NAS / "001_How-Did-We-Discover-Germs/09_Final-Export/hos_001_germs_full_v02.mp4",
     "inv_len": 364.55},
    {"film": "002", "card": "The Empty Chairs", "keep_to": None,
     "master": NAS / "002_How-Did-We-Discover-The-Periodic-Table/09_Final-Export/hos_002_periodic_table_full_v02.mp4",
     "inv_len": 540.63},
    {"film": "003", "card": "A Light Through Skin", "keep_to": None,
     "master": NAS / "003_Invisible-Bones-X-Rays/09_Final-Export/hos_003_full_polish_v01.mp4",
     "inv_len": 425.71},
    {"film": "004", "card": "Inside the Atom", "keep_to": 491.40,
     "master": Path("/Volumes/data/mac-mini-archive/mini-tmp-scratch/2026-10-21/HOS-004/hos_004_full_v02.mp4"),
     "inv_len": 524.70},
]
# Segment that follows each film (the closing follows 004).
AFTER = {"005": "bridge1", "006": "bridge2", "001": "bridge3", "002": "bridge4", "003": "bridge5", "004": "closing"}
VO_LEN = {"intro": 51.68, "bridge1": 17.12, "bridge2": 17.04, "bridge3": 13.84,
          "bridge4": 13.44, "bridge5": 14.88, "closing": 30.24}
CARD_LEN = 3.0
BREATH = 0.6           # picture and bed past a VO segment's last word
END_CARD_HOLD = 3.5 + 2.5  # closing end card 3-4 s, then hold 2-3 s
TIMELINE_ROWS = {"bridge1": "code_graphic_comp_timeline_b1", "bridge3": "code_graphic_comp_timeline_b3",
                 "bridge5": "code_graphic_comp_timeline_b5", "closing": "code_graphic_comp_timeline_close"}

# Segment stage. Shots are (film, master in, master out) windows from the normalised masters,
# each checked frame by frame for burned-in labels (_label_scan_v01.py misses 003's italic
# labels from ~103 s: CARDBOARD, FLUORESCENT) and the lower-third captions (003 90.5-94.9 s
# WHY COVER THE TUBE). Only segments whose inputs all exist are listed.
VO_LEAD = 0.25
SHOT_XFADE = 0.5
VO_I, BED_I = -15.0, -32.0  # bed 17 LU under the VO integrated; at 14 LU, sfx_kit level found pockets inside 10 LU
BED = HOS / "02_Video-Projects/004_Whats-Really-Inside-An-Atom/05_Music/hos004-full_score_bed_v01.mp3"
BED_IN = {"intro": 0.0, "bridge1": 60.0, "bridge2": 90.0, "bridge3": 120.0, "bridge4": 150.0,
          "bridge5": 180.0, "closing": 220.0}  # distinct stretches of the 390.8 s bed
TICK = HOS / "docs/STANDALONE_SHORTS_TEST_2026-10/sfx_kit_v01/sfx_hos_tick_ink_v01.wav"
TICK_GAIN_DB = -14.0
GFX = "gfx"  # a shot ("gfx", 0, length) is the segment's J0204 timeline, played from its start
SEGMENT_SHOTS = {
    # 003 uses the italic look plus lower-third captions; both windows checked on a 1 s sheet:
    # dark screen 95.2-101.8 s (CARDBOARD from 103 s), lit screen 145.2-149.4 s (card at 151 s).
    # 002 EMPTY CHAIR cuts off between 230.0 and 230.2 s; the scan samples at 0.5 s, so edges keep 0.3 s.
    "bridge4": [("002", 230.3, 235.0), ("003", 95.2, 101.8), ("003", 145.2, 149.4)],
    # 001 330.7 s on is the Explorer in the empty theatre (kept out of new material, script v01),
    # so Bridge 3 opens on Lister at the basin (dissolve in ends 325.4 s). 002 candlelit cards hold
    # to ~130.9 s, then dissolve to the daylit desk (clean 131.5-138.4 s, piano from 138.5 s).
    # Each timeline is drawn over its blurred plate from background_offset (GRAPHICS_MANIFEST_v01),
    # so the sharp shot after it starts at offset + length - xfade: the dissolve reads as a focus pull.
    "bridge3": [("001", 325.5, 329.8), ("002", 117.0, 121.5), (GFX, 0.0, 4.0), ("002", 135.0, 138.4)],
    # 004: the 1909 date card sits at 246 s and the lab hall cuts in at 267 s; the framed foil
    # arrives ~263 s, on "a sheet of gold". 003's hand-at-screen shot dissolves in until 118.8 s.
    "bridge5": [("003", 118.9, 124.5), ("004", 240.3, 245.5), (GFX, 0.0, 4.0), ("004", 263.5, 266.7)],
    # Closing: one plate per spoken object, none reusing an intro or bridge window. The willow
    # ("a tree made of air", ~4-6 s) needs 006, so the arm holds over it until then. 005 "Deep
    # arteries" label ends 286 s; 002 1860 date card from 170 s; 003 SOFT TISSUE from ~168 s;
    # The beam runs on through the film's own cut (~257 s) to the two scientists for "by people who
    # refused to trust the obvious answer" (clean to 262.7 s). The timeline lands on "So what is still
    # invisible" (VO 25.75 s). Plate 25's dark hall (314.5-318.5 s) is near-black, and its atom in space
    # is the timeline's own blurred plate, so neither is cut in. The orb sits under the end card.
    "closing": [("004", 227.6, 230.9), ("005", 287.6, 291.3), ("001", 298.0, 300.6),
                ("002", 162.3, 165.6), ("003", 163.8, 167.6), ("004", 224.0, 227.3),
                ("004", 252.0, 261.7), (GFX, 0.0, 4.0), ("004", 214.6, 222.8)],
}


def gfx_manifest() -> dict:
    p = GRAPHICS_DIR / "GRAPHICS_MANIFEST_v01.json"
    return {Path(r["file"]).stem: r for r in json.loads(p.read_text())} if p.exists() else {}


def seg_len(name: str) -> float:
    tail = BREATH + (END_CARD_HOLD if name == "closing" else 0.0)
    return VO_LEAD + VO_LEN[name] + tail


def cmd_segment(args) -> int:
    scratch = Path(args.scratch)
    name = args.name
    shots = SEGMENT_SHOTS.get(name)
    if not shots:
        print(f"{name}: no checked shots yet (see COMPILATION_PLATES_v01.json missing rows)")
        return 2
    graphic, gfx_rec = None, None
    if name in TIMELINE_ROWS:
        row = TIMELINE_ROWS[name]
        graphic = GRAPHICS_DIR / f"{row}.mp4"
        gfx_rec = gfx_manifest().get(row)
        if not graphic.exists() or gfx_rec is None:
            if not args.draft:
                print(f"{name}: {graphic.name} missing (J0204); rerun with --draft for a picture-only test")
                return 2
            graphic, gfx_rec = None, None
            shots = [s for s in shots if s[0] != GFX]
        elif sha256(graphic) != gfx_rec["sha256"]:
            print(f"{name}: {graphic.name} sha256 differs from GRAPHICS_MANIFEST_v01 (not the passed render)")
            return 2
    L = seg_len(name)
    need = L + SHOT_XFADE * (len(shots) - 1)
    have = sum(b - a for _, a, b in shots)
    if have + 1e-3 < need:
        print(f"{name}: shots cover {have:.2f} s, need {need:.2f} s")
        return 2
    out_dir = scratch / "segments" / name
    if not out_dir.is_dir():
        out_dir.mkdir(parents=True, exist_ok=True)

    cmd = ["ffmpeg", "-hide_banner", "-y"]
    input_sources = []
    for film, a, b in shots:
        if film == GFX:
            input_sources.append(str(graphic))
            cmd += ["-i", str(graphic)]
        else:
            src = scratch / f"film_{film}_norm.mp4"
            if not src.exists():
                src = next(f["master"] for f in FILMS if f["film"] == film)
            input_sources.append(str(src))
            cmd += ["-ss", f"{a:.3f}", "-t", f"{b - a:.3f}", "-i", str(src)]
    vo = VO_DIR / f"hos_comp_{name}_vo_v01.wav"
    cmd += ["-i", str(vo), "-ss", f"{BED_IN[name]:.3f}", "-t", f"{L + 1:.3f}", "-i", str(BED), "-i", str(TICK)]
    n = len(shots)
    starts, t = [], 0.0
    for film, a, b in shots:
        starts.append(t)
        t += (b - a) - SHOT_XFADE
    ticks = []
    for (film, a, b), s in zip(shots, starts):
        if film == GFX:
            ticks += [round(s + c, 3) for c in gfx_rec["tick_ink_seconds"]]
    # Original masters are a safe fallback when macOS has purged old prep scratch.
    fc = [f"[{i}:v]scale=1920:1080,setsar=1,fps=30,settb=AVTB,setpts=PTS-STARTPTS[p{i}]" for i in range(n)]
    prev = "[p0]"
    if name == "bridge4":
        # The screen lights up at the final shot; one pen-tap marks that reveal.
        ticks = [round(starts[2] + SHOT_XFADE / 2, 3)]
    for i in range(1, n):
        fc.append(f"{prev}[p{i}]xfade=transition=fade:duration={SHOT_XFADE}:offset={starts[i]:.3f}[x{i}]")
        prev = f"[x{i}]"
    if name == "closing":
        start, end = L - END_CARD_HOLD, L - END_CARD_HOLD + 3.5
        from PIL import Image, ImageDraw, ImageFont
        card = Image.new("RGBA", (1920, 1080))
        # A feathered navy wash gives the cream type a stable contrast over the plate.
        pen = ImageDraw.Draw(card)
        for y in range(680, 1080):
            alpha = int(210 * min(1.0, (y - 680) / 120))
            pen.line((0, y, 1920, y), fill=(24, 34, 49, alpha))
        pen.line((700, 775, 1220, 775), fill=(213, 179, 113, 255), width=3)
        for text, size, y in [("History of Science", 92, 850), ("More discovery stories", 60, 950)]:
            font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Didot.ttc", size, index=1)
            pen.text((960, y), text, font=font, fill=(255,244,218,255), anchor="mm")
        overlay = out_dir / "code_graphic_comp_closing_end_card.png"
        card.save(overlay)
        cmd += ["-loop", "1", "-i", str(overlay)]
        fc.append(f"[{n+3}:v]format=rgba,fade=t=in:st={start}:d=0.5:alpha=1,fade=t=out:st={end-.5}:d=0.5:alpha=1[card]")
        # Chief 23 Oct: freeze the underlying composite for exactly the card's
        # 3.5 s window, then resume from that frame. The PNG and plate are both
        # stationary during the gate's still-row sample; no gate exception.
        fc.append(f"{prev}split=3[before][freeze][after]")
        fc.append(f"[before]trim=end={start:.3f},setpts=PTS-STARTPTS[precard]")
        fc.append(f"[freeze]trim=start={start:.3f},setpts=PTS-STARTPTS,trim=end_frame=1,tpad=stop_mode=clone:stop_duration=3.5,trim=duration=3.5[held]")
        fc.append(f"[after]trim=start={start:.3f},setpts=PTS-STARTPTS[postcode]")
        fc.append("[precard][held][postcode]concat=n=3:v=1:a=0[cardplate]")
        fc.append(f"[cardplate][card]overlay=shortest=1,trim=duration={L:.3f},setpts=PTS-STARTPTS,fade=t=out:st={L-1.5}:d=1.5,format=yuv420p[vout]")
    else:
        fc.append(f"{prev}trim=duration={L:.3f},setpts=PTS-STARTPTS,format=yuv420p[vout]")
    fc.append(f"[{n}:a]aresample=48000,aformat=channel_layouts=stereo,"
              f"loudnorm=I={VO_I}:TP=-2:LRA=11,adelay={int(VO_LEAD * 1000)}:all=1,"
              f"apad,atrim=duration={L:.3f},asplit=3[vo][vostem][duckvo]")
    fc.append(f"[{n + 1}:a]aresample=48000,aformat=channel_layouts=stereo,loudnorm=I={BED_I}:TP=-6:LRA=11,"
              f"atrim=duration={L:.3f},afade=t=in:d=1.5,afade=t=out:st={L - 1.5:.3f}:d=1.5[bedraw]")
    fc.append("[bedraw][duckvo]sidechaincompress=threshold=0.003:ratio=20:attack=5:release=300:"
              "knee=2.828:makeup=1:link=maximum:detection=rms,asplit=2[bed][bedstem]")
    tick_in = f"[{n + 2}:a]aresample=48000,aformat=channel_layouts=stereo,volume={TICK_GAIN_DB}dB"
    if ticks:
        fc.append(f"{tick_in},asplit={len(ticks)}" + "".join(f"[tk{i}]" for i in range(len(ticks))))
        for i, c in enumerate(ticks):
            fc.append(f"[tk{i}]adelay={int(c * 1000)}:all=1[td{i}]")
        fc.append("".join(f"[td{i}]" for i in range(len(ticks))) +
                  f"amix=inputs={len(ticks)}:normalize=0:duration=longest,apad=whole_dur={L:.3f},asplit=2[sfx][sfxstem]")
    else:
        fc.append(f"{tick_in},volume=0,apad=whole_dur={L:.3f},asplit=2[sfx][sfxstem]")
    fc.append("[vo][bed][sfx]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.89:level=false[mix]")
    mp4 = out_dir / f"hos_comp_{name}_v01{'_draft' if args.draft else ''}.mp4"
    # Every output carries -t: an apad branch that atrim fails to end once wrote a 16 GB stem.
    cap = ["-t", f"{L:.3f}"]
    cmd += ["-filter_complex", ";".join(fc),
            "-map", "[vout]", "-map", "[mix]", *cap, "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-r", "30",
            "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-movflags", "+faststart", str(mp4),
            "-map", "[vostem]", *cap, "-c:a", "pcm_s24le", str(out_dir / f"{name}_vo_stem.wav"),
            "-map", "[bedstem]", *cap, "-c:a", "pcm_s24le", str(out_dir / f"{name}_bed_stem.wav"),
            "-map", "[sfxstem]", *cap, "-c:a", "pcm_s24le", str(out_dir / f"{name}_sfx_stem.wav")]
    r = run(cmd)
    if r.returncode != 0:
        print(r.stderr[-2000:])
        return 1
    cuts = []
    for i, ((film, a, b), s) in enumerate(zip(shots, starts)):
        d = b - a
        if film == GFX:
            src, framing = graphic.name, {"offset": 0.0, "fit": "J0204 code graphic, own render (Chief PASS 13 Oct)"}
        else:
            src, framing = f"{input_sources[i]}@{a:.2f}", {"offset": a, "fit": "full 16:9 from the film's passed master"}
        cuts.append({"row": f"{name}_{i + 1:02d}", "timeline_in": round(s, 3),
                     "timeline_out": round(min(s + d, L), 3), "source": src, "framing": framing})
    if name == "closing":
        cuts.append({"row": "code_graphic_comp_closing_end_card", "timeline_in": round(L-6,3),
                     "timeline_out": round(L-2.5,3), "source": str(overlay),
                     "framing": {"fit": "own cream Didot card and navy wash; plate frozen for card 3.5 s, then resumes; 0.5 s alpha fades"}})
    (out_dir / "cuts.json").write_text(json.dumps(cuts, indent=1))
    rec = {"segment": name, "length": round(L, 3), "draft": bool(args.draft), "mp4": str(mp4),
           "closing_card": {"text": ["History of Science", "More discovery stories"], "start": L-6, "end": L-2.5, "animation": "0.5 s fade in/out; plate held 3.5 s during card, then resumes"} if name == "closing" else None,
           "graphic": str(graphic) if graphic else (TIMELINE_ROWS.get(name, "") + " missing" if name in TIMELINE_ROWS else None),
           "ticks": ticks, "tick": str(TICK), "tick_gain_db": TICK_GAIN_DB,
           "shots": shots, "vo": str(vo), "bed": str(BED), "bed_in": BED_IN[name],
           "bed_ducking": {"threshold": 0.003, "ratio": 20, "attack_ms": 5, "release_ms": 300},
           "loudness_mix": measure(mp4, None), "probe": probe(mp4)}
    (out_dir / "segment_report.json").write_text(json.dumps(rec, indent=1))
    lo = rec["loudness_mix"]
    print(f"{name}: {mp4} {L:.2f} s, mix I={lo['input_i']} TP={lo['input_tp']}")
    return 0


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True)


def probe(path: Path) -> dict:
    r = run(["ffprobe", "-v", "error", "-show_entries",
             "format=duration:stream=codec_type,width,height,r_frame_rate,sample_rate,channels",
             "-of", "json", str(path)])
    return json.loads(r.stdout or "{}")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 22), b""):
            h.update(chunk)
    return h.hexdigest()


def measure(path: Path, keep_to: float | None) -> dict:
    cmd = ["ffmpeg", "-hide_banner", "-nostats", "-i", str(path)]
    if keep_to:
        cmd += ["-t", f"{keep_to:.3f}"]
    cmd += ["-vn", "-af", f"loudnorm=I={TARGET_I}:TP={TARGET_TP}:LRA={TARGET_LRA}:print_format=json",
            "-f", "null", "-"]
    r = run(cmd)
    m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", r.stderr, re.S)
    if not m:
        raise RuntimeError(f"loudnorm measure failed for {path}: {r.stderr[-800:]}")
    return json.loads(m.group(0))


def prep_one(spec: dict, scratch: Path) -> dict:
    src: Path = spec["master"]
    out = scratch / f"film_{spec['film']}_norm.mp4"
    rec = {"film": spec["film"], "master": str(src), "keep_to": spec["keep_to"], "out": str(out)}
    rec["master_sha256"] = sha256(src)
    rec["master_probe"] = probe(src)
    m = measure(src, spec["keep_to"])
    rec["loudness_in"] = m
    af = (f"loudnorm=I={TARGET_I}:TP={TARGET_TP}:LRA={TARGET_LRA}"
          f":measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
          f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,"
          "aresample=48000,aformat=channel_layouts=stereo")
    if spec["keep_to"]:
        af += f",afade=t=out:st={spec['keep_to'] - TRIM_FADE:.3f}:d={TRIM_FADE}"
    vf = ("scale=1920:1080:flags=lanczos:force_original_aspect_ratio=decrease,"
          "pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30,format=yuv420p")
    cmd = ["ffmpeg", "-hide_banner", "-y", "-i", str(src)]
    if spec["keep_to"]:
        cmd += ["-t", f"{spec['keep_to']:.3f}"]
    cmd += ["-vf", vf, "-af", af, "-c:v", "libx264", "-preset", "medium", "-crf", "16",
            "-g", "60", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2",
            "-movflags", "+faststart", str(out)]
    t0 = time.time()
    r = run(cmd)
    if r.returncode != 0:
        raise RuntimeError(f"encode failed for {spec['film']}: {r.stderr[-1500:]}")
    rec["encode_s"] = round(time.time() - t0, 1)
    rec["out_probe"] = probe(out)
    rec["out_duration"] = float(rec["out_probe"]["format"]["duration"])
    rec["loudness_out"] = measure(out, None)
    return rec


def cmd_prep(args) -> int:
    scratch = Path(args.scratch)
    scratch.mkdir(parents=True, exist_ok=True)
    report_path = scratch / "prep_report.json"
    report = json.loads(report_path.read_text()) if report_path.exists() else {}
    only = set(args.only.split(",")) if args.only else None
    failed = 0
    for spec in FILMS:
        if only and spec["film"] not in only:
            continue
        if spec["master"] is None:
            print(f"{spec['film']}: skipped ({spec['missing']})", flush=True)
            continue
        print(f"{spec['film']}: prep start {time.strftime('%H:%M:%S')}", flush=True)
        try:
            rec = prep_one(spec, scratch)
        except Exception as e:  # keep going so one bad master doesn't stop the rest
            print(f"{spec['film']}: FAIL {e}", flush=True)
            failed += 1
            continue
        report[spec["film"]] = rec
        report_path.write_text(json.dumps(report, indent=1))
        lo = rec["loudness_out"]
        print(f"{spec['film']}: done {rec['out_duration']:.2f} s, {rec['encode_s']} s encode, "
              f"out I={lo['input_i']} TP={lo['input_tp']}", flush=True)
    return 1 if failed else 0


def fmt(t: float) -> str:
    t = int(round(t))
    return f"{t // 3600}:{t % 3600 // 60:02d}:{t % 60:02d}" if t >= 3600 else f"{t // 60}:{t % 60:02d}"


def cmd_plan(args) -> int:
    scratch = Path(args.scratch)
    rp = scratch / "prep_report.json"
    report = json.loads(rp.read_text()) if rp.exists() else {}
    segs, missing, t = [], [], 0.0

    def add(kind, name, length, src, source_of_length, **extra):
        nonlocal t
        segs.append({"start": round(t, 3), "start_hms": fmt(t), "kind": kind, "name": name,
                     "length": round(length, 3), "src": src, "length_from": source_of_length, **extra})
        t += length

    add("vo", "intro", VO_LEN["intro"] + BREATH, str(VO_DIR / "hos_comp_intro_vo_v01.wav"), "vo take + breath",
        picture="six plates (arm, willow, flask, cards, screen, foil) from the films' passed clips")
    missing.append("intro plates: pick one passed clip per object (willow needs 006)")
    chapters = [("0:00", "Six discoveries, one question")]
    for i, spec in enumerate(FILMS, 1):
        card_row = f"code_graphic_comp_card_{i:02d}"
        card_file = GRAPHICS_DIR / f"{card_row}.mp4"
        if not card_file.exists():
            missing.append(f"{card_row} ({spec['card']}): J0204")
        chapters.append((fmt(t), spec["card"]))
        add("card", card_row, CARD_LEN, str(card_file), "plan ~3 s", title=spec["card"])
        rec = report.get(spec["film"])
        if rec:
            length, src, how = rec["out_duration"], rec["out"], "prep_report"
        else:
            length, src = spec["keep_to"] or spec["inv_len"], spec["master"] and str(spec["master"])
            how = "estimate (006 ~8:20)" if spec["master"] is None else "inventory (not prepped yet)"
            if spec["master"] is None:
                missing.append(spec["missing"])
        add("film", spec["film"], length, src, how, keep_to=spec["keep_to"])
        nxt = AFTER[spec["film"]]
        extra = {}
        if nxt in TIMELINE_ROWS:
            row = TIMELINE_ROWS[nxt]
            extra["graphic"] = row
            if not (GRAPHICS_DIR / f"{row}.mp4").exists():
                missing.append(f"{row}: J0204")
        tail = BREATH + (END_CARD_HOLD if nxt == "closing" else 0.0)
        add("vo", nxt, VO_LEN[nxt] + tail, str(VO_DIR / f"hos_comp_{nxt}_vo_v01.wav"), "vo take + breath", **extra)
        if nxt != "closing":
            missing.append(f"{nxt} plates: pick from the neighbouring films' passed clips")
    plan = {"version": "v01", "job": "J0175", "generated": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "total_s": round(t, 2), "total_hms": fmt(t), "in_45_60": 2700 <= t <= 3600,
            "note": "Crossfades (0.5-1.5 s) overlap segments, so the final runtime is a few seconds under this sum.",
            "segments": segs, "chapters_draft": [f"{a} {b}" for a, b in chapters], "missing": missing}
    out = Path(args.out) if args.out else scratch / "cut_plan_v01.json"
    out.write_text(json.dumps(plan, indent=1))
    print(f"plan: {len(segs)} segments, total {plan['total_hms']} ({t:.1f} s), in 45-60: {plan['in_45_60']}")
    print("chapters draft:\n  " + "\n  ".join(plan["chapters_draft"]))
    print(f"missing ({len(missing)}):\n  " + "\n  ".join(missing))
    print(f"wrote {out}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("prep")
    p.add_argument("--only")
    p.add_argument("--scratch", default=str(SCRATCH))
    p.set_defaults(fn=cmd_prep)
    p = sub.add_parser("plan")
    p.add_argument("--scratch", default=str(SCRATCH))
    p.add_argument("--out")
    p.set_defaults(fn=cmd_plan)
    p = sub.add_parser("segment")
    p.add_argument("name", choices=sorted(VO_LEN))
    p.add_argument("--draft", action="store_true", help="render without a missing timeline graphic")
    p.add_argument("--scratch", default=str(SCRATCH))
    p.set_defaults(fn=cmd_segment)
    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
