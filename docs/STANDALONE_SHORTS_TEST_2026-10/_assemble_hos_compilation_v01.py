#!/usr/bin/env python3
"""HOS compilation film assembler v01 (J0175).

Stages:
  prep  normalise and trim each finished master into render scratch:
        1920x1080, 30 fps (fps=30, frame duplication only), yuv420p, AAC 48 kHz
        stereo, two-pass loudnorm to -14 LUFS / -1 dBTP. Writes prep_report.json.
  plan  write the cut plan (segment order, film-time starts, chapters list draft)
        from prep_report.json where present, else the inventory lengths. Missing
        inputs (006 master, J0204 graphics, intro/bridge plates) are listed, not faked.

Inputs and trim points: COMPILATION_ASSEMBLY_INVENTORY_v01.md. Masters are read
only; nothing on the NAS is written.

  python3 _assemble_hos_compilation_v01.py prep [--only 005,001] [--scratch DIR]
  python3 _assemble_hos_compilation_v01.py plan [--scratch DIR] [--out FILE]
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
    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
