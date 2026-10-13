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
        0.5 s crossfades between shots, VO at -15 LUFS, the 004 bed 14 LU under it,
        limiter at -1 dBTP; writes the mp4, VO and bed stems, cuts.json (polish_gate
        format) and segment_report.json. Refuses a segment whose timeline graphic is
        missing unless --draft.

Inputs and trim points: COMPILATION_ASSEMBLY_INVENTORY_v01.md. Masters are read
only; nothing on the NAS is written.

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
SCRATCH = Path("/private/tmp/hos_comp_v01")
VO_DIR = HOS / "docs/STANDALONE_SHORTS_TEST_2026-10/vo_compilation_v01"
GRAPHICS_DIR = HOS / "docs/STANDALONE_SHORTS_TEST_2026-10/graphics_v01"

TARGET_I, TARGET_TP, TARGET_LRA = -14.0, -1.0, 11.0
TRIM_FADE = 0.25  # audio fade on a trimmed tail; the cut sits in a measured VO pause

# Order by proof year (Chief, J0173). keep_to = None keeps the whole master.
FILMS = [
    {"film": "005", "card": "The Hidden Circle", "keep_to": 489.20,
     "master": Path.home() / "YouTube/hos-005-blood/02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/09_Final-Export/hos_005_master_v01.mp4",
     "inv_len": 526.53},
    {"film": "006", "card": "Built From Air", "keep_to": None, "master": None, "inv_len": 500.0,
     "missing": "006 master not finished (picture ETA 25 Oct); trim point TBD"},
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
     "master": HOS / "02_Video-Projects/004_Whats-Really-Inside-An-Atom/09_Final-Export/hos_004_full_v02.mp4",
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
VO_I, BED_I = -15.0, -29.0  # bed sits 14 LU under the VO; sfx_kit level wants >= 10
BED = HOS / "02_Video-Projects/004_Whats-Really-Inside-An-Atom/05_Music/hos004-full_score_bed_v01.mp3"
BED_IN = {"intro": 0.0, "bridge1": 60.0, "bridge2": 90.0, "bridge3": 120.0, "bridge4": 150.0,
          "bridge5": 180.0, "closing": 220.0}  # distinct stretches of the 390.8 s bed
SEGMENT_SHOTS = {
    # 003 uses the italic look plus lower-third captions; both windows checked on a 1 s sheet:
    # dark screen 95.2-101.8 s (CARDBOARD from 103 s), lit screen 145.2-149.4 s (card at 151 s).
    # 002 EMPTY CHAIR cuts off between 230.0 and 230.2 s; the scan samples at 0.5 s, so edges keep 0.3 s.
    "bridge4": [("002", 230.3, 235.0), ("003", 95.2, 101.8), ("003", 145.2, 149.4)],
}


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
    graphic = None
    if name in TIMELINE_ROWS:
        graphic = GRAPHICS_DIR / f"{TIMELINE_ROWS[name]}.mov"
        if not graphic.exists():
            if not args.draft:
                print(f"{name}: {graphic.name} missing (J0204); rerun with --draft for a picture-only test")
                return 2
            graphic = None
    L = seg_len(name)
    need = L + SHOT_XFADE * (len(shots) - 1)
    have = sum(b - a for _, a, b in shots)
    if have + 1e-3 < need:
        print(f"{name}: shots cover {have:.2f} s, need {need:.2f} s")
        return 2
    out_dir = scratch / "segments" / name
    out_dir.mkdir(parents=True, exist_ok=True)

    cmd = ["ffmpeg", "-hide_banner", "-y"]
    for film, a, b in shots:
        cmd += ["-ss", f"{a:.3f}", "-t", f"{b - a:.3f}", "-i", str(scratch / f"film_{film}_norm.mp4")]
    vo = VO_DIR / f"hos_comp_{name}_vo_v01.wav"
    cmd += ["-i", str(vo), "-ss", f"{BED_IN[name]:.3f}", "-t", f"{L + 1:.3f}", "-i", str(BED)]
    n = len(shots)
    fc, prev, t = [], "[0:v]", 0.0
    for i in range(1, n):
        t += (shots[i - 1][2] - shots[i - 1][1]) - SHOT_XFADE
        fc.append(f"{prev}[{i}:v]xfade=transition=fade:duration={SHOT_XFADE}:offset={t:.3f}[x{i}]")
        prev = f"[x{i}]"
    fc.append(f"{prev}trim=duration={L:.3f},setpts=PTS-STARTPTS,format=yuv420p[vout]")
    fc.append(f"[{n}:a]aresample=48000,aformat=channel_layouts=stereo,"
              f"loudnorm=I={VO_I}:TP=-2:LRA=11,adelay={int(VO_LEAD * 1000)}:all=1,"
              f"apad,atrim=duration={L:.3f},asplit=2[vo][vostem]")
    fc.append(f"[{n + 1}:a]aresample=48000,aformat=channel_layouts=stereo,loudnorm=I={BED_I}:TP=-6:LRA=11,"
              f"atrim=duration={L:.3f},afade=t=in:d=1.5,afade=t=out:st={L - 1.5:.3f}:d=1.5,asplit=2[bed][bedstem]")
    fc.append("[vo][bed]amix=inputs=2:normalize=0,alimiter=limit=0.89:level=false[mix]")
    mp4 = out_dir / f"hos_comp_{name}_v01{'_draft' if args.draft else ''}.mp4"
    cmd += ["-filter_complex", ";".join(fc),
            "-map", "[vout]", "-map", "[mix]", "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-r", "30",
            "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-movflags", "+faststart", str(mp4),
            "-map", "[vostem]", "-c:a", "pcm_s24le", str(out_dir / f"{name}_vo_stem.wav"),
            "-map", "[bedstem]", "-c:a", "pcm_s24le", str(out_dir / f"{name}_bed_stem.wav")]
    r = run(cmd)
    if r.returncode != 0:
        print(r.stderr[-2000:])
        return 1
    cuts, t = [], 0.0
    for i, (film, a, b) in enumerate(shots):
        d = b - a
        cuts.append({"row": f"{name}_{i + 1:02d}", "timeline_in": round(t, 3),
                     "timeline_out": round(min(t + d, L), 3), "source": f"film_{film}_norm.mp4@{a:.2f}",
                     "framing": {"offset": a, "fit": "full 16:9 from the film's passed master"}})
        t += d - SHOT_XFADE
    (out_dir / "cuts.json").write_text(json.dumps(cuts, indent=1))
    rec = {"segment": name, "length": round(L, 3), "draft": bool(args.draft), "mp4": str(mp4),
           "graphic": str(graphic) if graphic else (TIMELINE_ROWS.get(name, "") + " missing" if name in TIMELINE_ROWS else None),
           "shots": shots, "vo": str(vo), "bed": str(BED), "bed_in": BED_IN[name],
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
