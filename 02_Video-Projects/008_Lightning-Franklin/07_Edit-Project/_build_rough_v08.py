#!/usr/bin/env python3
"""J1263: HOS 008 rough v08.

Frame-exact splice of rough v04 (e00bb897), same method as v08.
Locks, byte-identical with v08 except the P5:10 composite: P2:15, P3:03,
P4:06, P3:04, the P5:10 alpha mov bb821f40, and the pause trim
(frames 1539-1552, 64.333-64.875 s). Plate in-point is the first source
frame at or after 4.40 s whose 71-frame window ends by 7.60 s and whose
rod-top vs gold-trace offset stays within 1% of width at p10/p25/p50/p75/p90.
That frame is 109 (4.541667 s). £0. No music bed. Never overwrite v02-v08.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess as sp
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1920, 1080, 24
FONT = "/System/Library/Fonts/Supplemental/Didot.ttc"
V04_SHA = "e00bb897a05c5a53843db9c7e7e62669194ced6f28f986daed6a142da54d7d5e"
ALPHA_EXPECT = None  # filled after first hash; the file itself is never rewritten
PLATE_OFFSET = 109 / 24  # 4.541667 s, first passing source frame >= 4.40 s

# Big encodes stay on the local disk. A NAS write of the splice stalled in
# uninterruptible sleep on 30 Oct. Deliver still copies the finished master to the NAS.
WORK = Path("/private/tmp/j1263-hos008-rough-v08")
MEDIA = Path(
    "/Users/benjaminoats/YouTube/hos-008-lightning/02_Video-Projects/008_Lightning-Franklin"
)
V04_MP4 = MEDIA / "07_Edit-Project/_precheck/rough_v04/hos_008_rough_v04.mp4"
V04_CUTS = MEDIA / "07_Edit-Project/_precheck/rough_v04/cuts_rough_v04.json"
V04_POOL = MEDIA / "07_Edit-Project/_precheck/rough_v04/pool_rough_v04.json"
V04_PAUSE = MEDIA / "07_Edit-Project/_precheck/rough_v04/PAUSE_TRIM_v03.json"
V05_CUTS = MEDIA / "07_Edit-Project/_precheck/rough_v05/cuts_rough_v05.json"
V05_ASSETS = Path(
    "/Volumes/data/mac-mini-archive/tmp-render-scratch/j1248-hos008-rough-v05/special_assets"
)
V06_CUTS = MEDIA / "07_Edit-Project/_precheck/rough_v06/cuts_rough_v06.json"
V06_P304 = Path(
    "/Volumes/data/mac-mini-archive/tmp-render-scratch/j1257-hos008-rough-v06"
    "/special_assets/overlay_04_letter_crosses.mp4"
)
ALPHA = Path(
    "/private/tmp/j1248-hos008-cg-v04-wt/02_Video-Projects/008_Lightning-Franklin"
    "/07_Edit-Project/code_graphics_v04/code_graphic_008_p5_10_metal_easy.mov"
)
PLATE = MEDIA / "04_Generated-Clips/part05/raw/v01/06_rod_fitting_t1.mp4"
LOCKED_COMPOSITE = V05_ASSETS / "overlay_10_metal_easy.mp4"
OWB_ROOT = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
SILENCE_LOG = Path(
    "/Volumes/data/mac-mini-archive/tmp-render-scratch/j1257-hos008-rough-v06/silence.txt"
)

PASSED = {
    "15_likeness_fire": V05_ASSETS / "overlay_15_likeness_fire.mp4",
    "03_rod_cloud": V05_ASSETS / "cg_03_rod_cloud.mp4",
    "06_same_thing": V05_ASSETS / "overlay_06_same_thing.mp4",
}


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def run(cmd: list[str]) -> None:
    print(" ", " ".join(cmd[:8]), "...", flush=True)
    sp.run(cmd, check=True)


def probe_json(path: Path) -> dict:
    return json.loads(sp.check_output(
        ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)],
        text=True,
    ))


def stream_durations(path: Path) -> dict:
    d = probe_json(path)
    out = {"format": float(d["format"]["duration"])}
    ends = {}
    for s in d["streams"]:
        kind = s["codec_type"]
        dur = float(s["duration"])
        start = float(s.get("start_time") or 0)
        out[kind] = dur
        out[f"{kind}_start"] = start
        ends[kind] = start + dur
        if kind == "video":
            out["nb_frames"] = int(s.get("nb_frames") or 0)
            out["r_frame_rate"] = s.get("r_frame_rate")
    if "video" in ends and "audio" in ends:
        out["av_end_offset"] = abs(ends["audio"] - ends["video"])
    return out


def video_packets(path: Path) -> list[float]:
    raw = sp.check_output(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "packet=pts_time", "-of", "csv=p=0", str(path)],
        text=True,
    )
    return sorted(float(line) for line in raw.splitlines() if line.strip())


def frame_index(pts: list[float], t: float) -> int:
    lo, hi = 0, len(pts) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if pts[mid] < t - (0.5 / FPS):
            lo = mid + 1
        else:
            hi = mid
    return lo


def map_pause_joins(pause: dict) -> list[float]:
    joins = []
    removed = 0.0
    for c in pause["cuts"]:
        joins.append(c["from"] - removed)
        removed += c["to"] - c["from"]
    return joins


def parse_silence(path: Path) -> list[tuple[float, float]]:
    starts, spans = [], []
    for line in path.read_text(errors="replace").splitlines():
        if "silence_start:" in line:
            starts.append(float(line.split("silence_start:")[1].strip()))
        elif "silence_end:" in line and "silence_duration:" in line:
            end = float(line.split("silence_end:")[1].split("|")[0].strip())
            if starts:
                spans.append((starts.pop(0), end))
    return spans


def row_frame_range(pts: list[float], cut: dict) -> tuple[int, int]:
    return frame_index(pts, float(cut["timeline_in"])), frame_index(pts, float(cut["timeline_out"]))


def build_metal(need: int) -> Path:
    """Same alpha mov, plate in-point frame 109 (4.541667s). Exact frame count."""
    asset = WORK / "special_assets" / "overlay_10_metal_easy.mp4"
    asset.parent.mkdir(parents=True, exist_ok=True)
    use_s = need / FPS
    alpha_sha = sha256_file(ALPHA)
    if sha256_file(LOCKED_COMPOSITE) != "eaf7bf88d890423750d0952043cf3f8239efb1c7f0343da5e879096266615ad8":
        raise RuntimeError("locked composite eaf7bf88 moved; refusing to touch a changed file")
    # The locked composite stays where it is. This is a new file.
    filt = (
        f"[0:v]scale={W}:{H}:flags=lanczos,fps={FPS},"
        f"eq=brightness=0.04:contrast=0.96,format=rgba[base];"
        f"[1:v]scale={W}:{H}:flags=lanczos,fps={FPS},format=rgba[ov];"
        f"[base][ov]overlay=0:0:format=auto,format=yuv420p[v]"
    )
    tmp = asset.with_suffix(".building.mp4")
    run([
        "ffmpeg", "-y", "-v", "error",
        "-ss", f"{PLATE_OFFSET:.6f}", "-t", f"{use_s:.3f}", "-i", str(PLATE),
        "-t", f"{use_s:.3f}", "-i", str(ALPHA),
        "-filter_complex", filt, "-map", "[v]", "-an",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p",
        "-frames:v", str(need), str(tmp),
    ])
    tmp.replace(asset)
    info = stream_durations(asset)
    if info["nb_frames"] != need:
        raise RuntimeError(f"metal frames {info['nb_frames']} != {need}")
    if sha256_file(ALPHA) != alpha_sha:
        raise RuntimeError("alpha mov changed")
    note = {
        "plate": str(PLATE),
        "plate_in_point_s": PLATE_OFFSET,
        "why": (
            "Chief h11: smallest source frame at or after 4.40 s (frame 109, "
            f"{PLATE_OFFSET:.6f}s) whose 71-frame window ends by 7.60 s. "
            "Clears the hammer morph (plate 4.00-4.375 s) and the repeat of "
            "06_rod_fitting at 437.7-438.6 s. Rod-top vs gold trace stays within "
            "1% of width at p10/p25/p50/p75/p90. Alpha mov unchanged."
        ),
        "alpha": str(ALPHA),
        "alpha_sha256": alpha_sha,
        "locked_composite_left_untouched": str(LOCKED_COMPOSITE),
        "locked_composite_sha256": "eaf7bf88d890423750d0952043cf3f8239efb1c7f0343da5e879096266615ad8",
        "new_composite_sha256": sha256_file(asset),
        "frames": need,
    }
    (WORK / "PLATE_INPOINT.json").write_text(json.dumps(note, indent=2) + "\n")
    print(f"metal in-point +{PLATE_OFFSET:.6f}s frames={need} sha={note['new_composite_sha256'][:12]}", flush=True)
    return asset


def choose_pause(pts, spans, joins, row_ranges, cuts) -> dict:
    """13-frame pause after 0:30, inside a silence, containing a shot boundary, nearest a v03 join."""
    trim_frames = 13
    trim_s = trim_frames / FPS
    bounds = []
    for c in cuts:
        bounds.append((float(c["timeline_out"]), c["row"]))
    best = None
    for a, b in spans:
        if a < 30.0:
            continue
        if (b - a) < trim_s + 0.08:
            continue
        lo, hi = a + 0.04, b - 0.04
        if hi - lo < trim_s:
            continue
        starts = []
        for bound, _row in bounds:
            start = min(max(bound - trim_s / 2, lo), hi - trim_s)
            if start <= bound <= start + trim_s:
                starts.append(start)
        for start in starts:
            if start < 30.0:
                continue
            f0 = frame_index(pts, start)
            f1 = f0 + trim_frames
            if f1 >= len(pts):
                continue
            if not (a + 0.02 <= pts[f0] and pts[f1] <= b - 0.02):
                continue
            if any(not (f1 <= r0 or f0 >= r1) for r0, r1 in row_ranges):
                continue
            hit = [row for bound, row in bounds if pts[f0] <= bound <= pts[f1]]
            if not hit:
                continue
            mid = (pts[f0] + pts[f1]) / 2
            dist = min(abs(mid - j) for j in joins)
            cand = {
                "silence": [a, b],
                "trim_start": pts[f0],
                "trim_end": pts[f1],
                "frame0": f0,
                "frame1": f1,
                "trim_s": pts[f1] - pts[f0],
                "join_dist": dist,
                "boundary_rows": hit,
                "hook": "no trim before 0:30",
            }
            if best is None or dist < best["join_dist"]:
                best = cand
    if best is None:
        raise RuntimeError("no post-0:30 shot-boundary silence can take the pause")
    if best["join_dist"] > 2.5:
        raise RuntimeError(f"nearest pause join is {best['join_dist']:.2f}s away; refusing")
    if best["trim_start"] < 30.0:
        raise RuntimeError("trim landed in the hook")
    if best["frame0"] != 1539 or best["frame1"] != 1552:
        raise RuntimeError(
            f"pause drifted to frames {best['frame0']}-{best['frame1']}; v08 must keep v07's 1539-1552"
        )
    print(
        f"pause trim frames {best['frame0']}-{best['frame1']} "
        f"t {best['trim_start']:.3f}-{best['trim_end']:.3f} "
        f"join_dist={best['join_dist']:.3f} boundary={best['boundary_rows']}",
        flush=True,
    )
    return best


def apply_pause_trim(swapped: Path, chosen: dict) -> Path:
    pts = video_packets(swapped)
    f0, f1 = int(chosen["frame0"]), int(chosen["frame1"])
    span = pts[f1] - pts[f0]
    expect = (f1 - f0) / FPS
    if abs(span - expect) > 0.002:
        raise RuntimeError(f"pause frames {f0}-{f1} span {span:.6f}s, expected {expect:.6f}s")
    silence = chosen["silence"]
    if not (silence[0] + 0.02 <= pts[f0] and pts[f1] <= silence[1] - 0.02):
        raise RuntimeError(f"cut {pts[f0]:.3f}-{pts[f1]:.3f} is not inside silence {silence}")
    chosen["trim_start"] = pts[f0]
    chosen["trim_end"] = pts[f1]
    chosen["trim_s"] = span
    chosen["audio"] = (
        "splice audio stream-copied; this pause cut is one AAC encode of the joined track"
    )
    n_drop = f1 - f0
    vf = (
        f"select='not(between(n,{f0},{f1 - 1}))',"
        f"setpts='if(lt(N,{f0}),PTS,PTS-{n_drop}/{FPS}/TB)'"
    )
    af = (
        f"[0:a]atrim=end={pts[f0]:.6f},asetpts=PTS-STARTPTS[a1];"
        f"[0:a]atrim=start={pts[f1]:.6f},asetpts=PTS-STARTPTS[a2];"
        f"[a1][a2]concat=n=2:v=0:a=1[a]"
    )
    out = WORK / "hos_008_rough_v08.mp4"
    run([
        "ffmpeg", "-y", "-v", "error", "-i", str(swapped),
        "-filter_complex", f"[0:v]{vf}[v];{af}",
        "-map", "[v]", "-map", "[a]",
        "-fps_mode", "passthrough",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-movflags", "+faststart", str(out),
    ])
    return out


def remap_cut_time(tin: float, tout: float, t0: float, t1: float) -> tuple[float, float]:
    """Map a row across a removed span. A row that straddles the span is shortened on each side."""
    shift = t1 - t0
    if tout <= t0 + 1e-4:
        return tin, tout
    if tin >= t1 - 1e-4:
        return tin - shift, tout - shift
    new_in = tin if tin <= t0 else t0
    new_out = (tout - shift) if tout >= t1 else t0
    if new_out < new_in:
        raise RuntimeError(f"row collapsed {tin}-{tout} across {t0}-{t1}")
    return new_in, new_out


def splice(metal: Path) -> Path:
    if sha256_file(V04_MP4) != V04_SHA:
        raise RuntimeError("v04 master sha mismatch")
    pts = video_packets(V04_MP4)
    print(f"v04 video packets {len(pts)} first={pts[0]:.4f} last={pts[-1]:.4f}", flush=True)
    deltas = [round((b - a) * 24000) for a, b in zip(pts, pts[1:])]
    on_grid = sum(1 for d in deltas if d == 1000)
    if on_grid < len(deltas) * 0.99:
        raise RuntimeError(f"v04 timing is not 24fps: {on_grid}/{len(deltas)}")
    cuts = json.loads(V04_CUTS.read_text())
    by = {c["row"]: c for c in cuts}
    v05 = {c["row"]: c for c in json.loads(V05_CUTS.read_text())}
    v06 = {c["row"]: c for c in json.loads(V06_CUTS.read_text())}
    repl = dict(PASSED)
    repl["04_letter_crosses"] = V06_P304
    repl["10_metal_easy"] = metal
    if sha256_file(V06_P304) != v06["04_letter_crosses"]["source_sha256"]:
        raise RuntimeError("P3:04 inset is not the locked v06 asset")
    for row, path in PASSED.items():
        digest = sha256_file(path)
        if digest != v05[row]["source_sha256"]:
            raise RuntimeError(f"{row} sha {digest} != v05 {v05[row]['source_sha256']}")
    ranges = {}
    for row, path in repl.items():
        f0, f1 = row_frame_range(pts, by[row])
        have = stream_durations(path)["nb_frames"]
        need = f1 - f0
        print(f"  row {row} frames {f0}-{f1} need={need} asset={have}", flush=True)
        if have != need:
            raise RuntimeError(f"{row} asset frames {have} != window {need}")
        ranges[row] = (f0, f1, path)
    ordered = sorted(ranges.values(), key=lambda r: r[0])
    for (a0, a1, _), (b0, b1, _) in zip(ordered, ordered[1:]):
        if a1 > b0:
            raise RuntimeError(f"overlapping replacements {a0}-{a1} and {b0}-{b1}")
    joins = map_pause_joins(json.loads(V04_PAUSE.read_text()))
    spans = parse_silence(SILENCE_LOG)
    chosen = choose_pause(pts, spans, joins, [(a, b) for a, b, _ in ordered], cuts)
    (WORK / "PAUSE_TRIM_APPLIED.json").write_text(json.dumps({
        "source": "PAUSE_TRIM_v03.json joins, after 0:30, trim contains a shot boundary",
        "choice": chosen,
        "vo": "pause only; trim sits inside silencedetect, clear of the hook and the FIX rows",
        "moved_from": "v06 trim 9.167-9.708s inside the kite plate",
    }, indent=2) + "\n")

    inputs = ["-i", str(V04_MP4)]
    lines = []
    last = "[0:v]"
    for i, (f0, f1, src) in enumerate(ordered, start=1):
        inputs += ["-i", str(src)]
        start_pts = pts[f0]
        lines.append(f"[{i}:v]setpts=PTS-STARTPTS+{start_pts:.6f}/TB[o{i}]")
        lines.append(
            f"{last}[o{i}]overlay=eof_action=pass:repeatlast=0:"
            f"enable='between(n\\,{f0}\\,{f1 - 1})'[v{i}]"
        )
        last = f"[v{i}]"
    graph = ";".join(lines)
    (WORK / "splice_graph.txt").write_text(graph + "\n")
    swapped = WORK / "hos_008_rough_v08_swapped.mp4"
    run([
        "ffmpeg", "-y", "-v", "error", *inputs,
        "-filter_complex", graph,
        "-map", last, "-map", "0:a:0",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "copy",
        "-movflags", "+faststart", str(swapped),
    ])
    out = apply_pause_trim(swapped, chosen)
    info = stream_durations(out)
    (WORK / "DURATION.json").write_text(json.dumps(info, indent=2) + "\n")
    print("DURATIONS", json.dumps(info), flush=True)
    frame = 1 / FPS
    problems = []
    for key in ("format", "video", "audio"):
        if info[key] > 540.000:
            problems.append(f"{key} {info[key]:.4f} > 540")
    if info.get("av_end_offset", 9) > frame + 0.001:
        problems.append(f"A/V end offset {info['av_end_offset']:.4f} > {frame:.4f}")
    if problems:
        raise RuntimeError("; ".join(problems))

    t0, t1 = chosen["trim_start"], chosen["trim_end"]
    new_cuts = []
    for c in cuts:
        c = dict(c)
        nin, nout = remap_cut_time(float(c["timeline_in"]), float(c["timeline_out"]), t0, t1)
        c["timeline_in"] = round(nin, 4)
        c["timeline_out"] = round(nout, 4)
        new_cuts.append(c)
    for c in new_cuts:
        if c["row"] in repl:
            path = repl[c["row"]]
            c["source"] = path.name
            c["source_path"] = str(path)
            c["source_sha256"] = sha256_file(path)
            if c["row"] in PASSED and c["source_sha256"] != v05[c["row"]]["source_sha256"]:
                raise RuntimeError(f"sha drifted for {c['row']}")
            if c["row"] == "04_letter_crosses" and c["source_sha256"] != v06[c["row"]]["source_sha256"]:
                raise RuntimeError("P3:04 sha drifted")
            if c["row"] == "10_metal_easy":
                c["framing"] = {"offset": PLATE_OFFSET}
                c["disposition"] = f"J1263 v08 plate in-point +{PLATE_OFFSET:.6f}s frame 109 (alpha mov unchanged)"
            else:
                c["disposition"] = f"J1263 v08 frame-exact lock ({path.name})"
    (WORK / "cuts_rough_v08.json").write_text(json.dumps(new_cuts, indent=2) + "\n")
    # refresh the applied note with snapped times
    note = json.loads((WORK / "PAUSE_TRIM_APPLIED.json").read_text())
    note["choice"] = chosen
    (WORK / "PAUSE_TRIM_APPLIED.json").write_text(json.dumps(note, indent=2) + "\n")
    return out


def grab(master: Path, t: float, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.3f}", "-i", str(master),
         "-frames:v", "1", "-q:v", "2", str(dest)])


def evidence(master: Path) -> None:
    ev = WORK / "composite_evidence_v08"
    ev.mkdir(parents=True, exist_ok=True)
    cuts = json.loads((WORK / "cuts_rough_v08.json").read_text())
    by = {c["row"]: c for c in cuts}
    cc = by["10_metal_easy"]
    tin, tout = float(cc["timeline_in"]), float(cc["timeline_out"])
    for pct, name in ((10, "p10"), (25, "p25"), (50, "p50"), (75, "p75"), (90, "p90")):
        grab(master, tin + (tout - tin) * pct / 100, ev / f"p510_{name}.jpg")
    pause = json.loads((WORK / "PAUSE_TRIM_APPLIED.json").read_text())["choice"]
    join = pause["trim_start"]  # output time of the new join
    for label, dt in (("m0.50", -0.50), ("m0.25", -0.25), ("m0.04", -0.04),
                      ("p0.04", 0.04), ("p0.25", 0.25), ("p0.50", 0.50)):
        grab(master, max(0.0, join + dt), ev / f"pause_join_{label}.jpg")
    # Before: v04 around the same original span. After: v08 around the join.
    t0, t1 = pause["trim_start"], pause["trim_end"]
    run([
        "ffmpeg", "-y", "-v", "error",
        "-ss", f"{max(0.0, t0 - 0.5):.3f}", "-t", "1.6", "-i", str(V04_MP4),
        "-filter_complex", "showwavespic=s=1600x240:split_channels=1",
        "-frames:v", "1", str(ev / "wave_before.png"),
    ])
    run([
        "ffmpeg", "-y", "-v", "error",
        "-ss", f"{max(0.0, join - 0.5):.3f}", "-t", "1.0", "-i", str(master),
        "-filter_complex", "showwavespic=s=1600x240:split_channels=1",
        "-frames:v", "1", str(ev / "wave_after.png"),
    ])
    # silence numbers on the first 40s of the new master
    log = WORK / "silence_after_head.txt"
    sp.run(
        ["ffmpeg", "-v", "info", "-t", "40", "-i", str(master),
         "-af", "silencedetect=noise=-35dB:d=0.30", "-f", "null", "-"],
        stderr=log.open("w"), stdout=sp.DEVNULL, check=False,
    )
    kept = [ln for ln in log.read_text(errors="replace").splitlines() if "silence_" in ln]
    (ev / "SILENCE_NUMBERS.txt").write_text(
        "BEFORE v04 silence containing the trim:\n"
        f"  {pause['silence'][0]:.3f}-{pause['silence'][1]:.3f}s "
        f"dur={pause['silence'][1] - pause['silence'][0]:.3f}\n"
        f"TRIM removed {t0:.3f}-{t1:.3f}s ({t1 - t0:.3f}s), frames {pause['frame0']}-{pause['frame1']}\n"
        f"boundary rows: {pause['boundary_rows']}\n"
        f"join_dist to PAUSE_TRIM_v03 point: {pause['join_dist']:.3f}s\n"
        "AFTER, silences in the first 40s of v08:\n"
        + "\n".join(kept) + "\n"
    )
    print(f"evidence {ev}", flush=True)


def gates(master: Path) -> dict:
    cuts = WORK / "cuts_rough_v08.json"
    pool = WORK / "pool_rough_v08.json"
    shutil.copy2(V04_POOL, pool)
    polish_json = WORK / "polish_gate_rough_v08.json"
    polish = sp.run(
        [sys.executable, str(OWB_ROOT / "scripts/polish_gate.py"), str(master),
         "--cuts", str(cuts), "--out", str(polish_json)],
        capture_output=True, text=True,
    )
    (WORK / "polish_gate_rough_v08.txt").write_text(polish.stdout + polish.stderr)
    print(polish.stdout[-800:], flush=True)
    pq = WORK / "picture_qa_rough_v08"
    picture = sp.run(
        [sys.executable, str(OWB_ROOT / "scripts/picture_qa.py"), str(master),
         "--cuts", str(cuts), "--pool", str(pool), "--out-dir", str(pq)],
        capture_output=True, text=True,
    )
    (WORK / "picture_qa_rough_v08.txt").write_text(picture.stdout + picture.stderr)
    print(picture.stdout[-800:], flush=True)
    note = {"status": "SKIPPED_NO_BED", "reason": "No new bed. Job brief.", "version": "rough_v08"}
    (WORK / "music_gate_rough_v08.json").write_text(json.dumps(note, indent=2) + "\n")
    (WORK / "music_gate_rough_v08.txt").write_text("SKIPPED_NO_BED\n")
    return {"polish_rc": polish.returncode, "picture_rc": picture.returncode}


def deliver(master: Path, gates_rc: dict) -> None:
    info = json.loads((WORK / "DURATION.json").read_text())
    summary = {
        "version": "rough_v08",
        "job": "J1263",
        "source_master": str(V04_MP4),
        "source_sha256": sha256_file(V04_MP4),
        "master_sha256": sha256_file(master),
        "durations": info,
        "gates": gates_rc,
        "plate_in_point": json.loads((WORK / "PLATE_INPOINT.json").read_text()),
        "pause": json.loads((WORK / "PAUSE_TRIM_APPLIED.json").read_text()),
        "note": "Parked for Chief: graphics + composite. No finished-film PASS. No music bed.",
    }
    if (WORK / "ROD_TRACE.json").exists():
        summary["rod_trace"] = json.loads((WORK / "ROD_TRACE.json").read_text())
    (WORK / "ROUGH_V08_SUMMARY.json").write_text(json.dumps(summary, indent=2) + "\n")
    names = [
        "hos_008_rough_v08.mp4", "cuts_rough_v08.json", "pool_rough_v08.json",
        "polish_gate_rough_v08.json", "polish_gate_rough_v08.txt",
        "picture_qa_rough_v08.txt", "music_gate_rough_v08.json", "music_gate_rough_v08.txt",
        "ROUGH_V08_SUMMARY.json", "DURATION.json", "PAUSE_TRIM_APPLIED.json",
        "PLATE_INPOINT.json", "ROD_TRACE.json",
    ]
    dests = [
        MEDIA / "07_Edit-Project/_precheck/rough_v08",
        Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT/HOS-008_Lightning-Franklin_rough_v08",
        Path("/Volumes/data/mac-mini-archive/YouTube/History Of Science/02_Video-Projects/008_Lightning-Franklin/07_Edit-Project/_desk/008/rough_v08"),
    ]
    for dest in dests:
        if dest.name in {f"rough_v0{n}" for n in range(2, 8)}:
            raise RuntimeError(dest)
        dest.mkdir(parents=True, exist_ok=True)
        for name in names:
            src = WORK / name
            if src.exists():
                shutil.copy2(src, dest / name)
        for folder in ("composite_evidence_v08", "picture_qa_rough_v08"):
            src = WORK / folder
            if not src.exists():
                continue
            target = dest / folder
            if target.exists():
                shutil.rmtree(target)
            shutil.copytree(src, target)
        sums = []
        for p in sorted(dest.rglob("*")):
            if p.is_file() and not p.name.startswith("._") and "picture_qa_rough_v08" not in p.parts:
                rel = p.relative_to(dest)
                sums.append(f"{sha256_file(p)}  {rel}\n")
        (dest / "SHA256SUMS.txt").write_text("".join(sums))
        print(f"delivered {dest}", flush=True)


def tip_offset(gray, trace_x: float = 1180.5) -> dict | None:
    """Rod-tip x on a 1920x1080 graded plate. Calibrated on v07 p50 (~-33 px, Chief ~20 px at 1024)."""
    import numpy as np
    xs, ys = [], []
    for y in range(20, 320):
        row = gray[y, 1100:1260]
        i = int(np.argmin(row))
        x = 1100 + i
        left = float(gray[y, x - 22:x - 8].mean())
        right = float(gray[y, x + 8:x + 22].mean())
        if row[i] < 90 and (left + right) / 2 - float(row[i]) > 40:
            xs.append(x)
            ys.append(y)
            if len(xs) >= 12:
                break
    if len(xs) < 8:
        return None
    import numpy as np
    rod_x = float(np.median(xs))
    off = rod_x - trace_x
    return {
        "rod_x": rod_x,
        "trace_x": trace_x,
        "offset_px": round(off, 1),
        "offset_pct_of_width": round(100 * off / W, 2),
        "offset_px_at_1024": round(off * 1024 / W, 1),
        "tip_y": int(ys[0]),
    }


def plate_gray(t: float):
    import numpy as np
    raw = sp.check_output([
        "ffmpeg", "-v", "error", "-ss", f"{t:.6f}", "-i", str(PLATE), "-frames:v", "1",
        "-vf", f"scale={W}:{H}:flags=lanczos,eq=brightness=0.04:contrast=0.96,format=gray",
        "-f", "rawvideo", "-",
    ])
    import numpy as np
    return np.frombuffer(raw, np.uint8).reshape(H, W).astype("float32")


def row_check(metal: Path) -> dict:
    """Offsets, brick-corner seams and unmodified gates on the 71-frame row before the long splice."""
    import numpy as np
    sys.path.insert(0, str(OWB_ROOT / "scripts"))
    import polish_gate as pg

    use_s = 71 / FPS
    samples = []
    ev = WORK / "row_probe"
    ev.mkdir(parents=True, exist_ok=True)
    worst = 0.0
    for pct in (10, 25, 50, 75, 90):
        t_row = use_s * pct / 100
        t_plate = PLATE_OFFSET + t_row
        grab(metal, t_row, ev / f"p{pct}.jpg")
        meas = tip_offset(plate_gray(t_plate))
        frame = pg.frame_gray(metal, t_row)
        hits = pg.seams(frame)
        vertical = [h for h in hits if "vertical" in h.get("kind", "")]
        if meas is None:
            raise RuntimeError(f"p{pct}: rod tip not found")
        worst = max(worst, abs(meas["offset_px"]))
        samples.append({
            "pct": pct,
            "plate_s": round(t_plate, 4),
            "row_s": round(t_row, 4),
            **meas,
            "vertical_seams": vertical,
        })
        print(
            f"  p{pct} plate {t_plate:.3f}s off {meas['offset_px']:+.1f}px "
            f"({meas['offset_pct_of_width']:+.2f}%) seams={vertical or 'none'}",
            flush=True,
        )
    limit = 0.01 * W
    align_ok = worst <= limit + 0.05
    seam_ok = all(not s["vertical_seams"] for s in samples)
    cuts = [{
        "row": "10_metal_easy",
        "timeline_in": 0.0,
        "timeline_out": round(use_s, 4),
        "source": metal.name,
        "source_path": str(metal),
        "framing": {"offset": PLATE_OFFSET},
    }]
    cuts_path = WORK / "row_cuts.json"
    cuts_path.write_text(json.dumps(cuts, indent=2) + "\n")
    pool_path = WORK / "row_pool.json"
    pool_path.write_text(json.dumps([{
        "file": metal.name,
        "title": "v03 alpha over KEEP 06_rod_fitting",
    }], indent=2) + "\n")
    polish = sp.run(
        [sys.executable, str(OWB_ROOT / "scripts/polish_gate.py"), str(metal),
         "--cuts", str(cuts_path), "--out", str(WORK / "row_polish.json")],
        capture_output=True, text=True,
    )
    (WORK / "row_polish.txt").write_text(polish.stdout + polish.stderr)
    picture = sp.run(
        [sys.executable, str(OWB_ROOT / "scripts/picture_qa.py"), str(metal),
         "--cuts", str(cuts_path), "--pool", str(pool_path),
         "--out-dir", str(WORK / "row_picture_qa")],
        capture_output=True, text=True,
    )
    (WORK / "row_picture.txt").write_text(picture.stdout + picture.stderr)
    print(polish.stdout[-400:], picture.stdout[-400:], flush=True)
    report = {
        "plate_in_point_s": PLATE_OFFSET,
        "source_frame": 109,
        "window_end_s": PLATE_OFFSET + use_s,
        "aim_pct": 1.0,
        "align_ok": align_ok,
        "seam_ok": seam_ok,
        "polish_rc": polish.returncode,
        "picture_rc": picture.returncode,
        "samples": samples,
    }
    (WORK / "ROD_TRACE.json").write_text(json.dumps(report, indent=2) + "\n")
    if not (align_ok and seam_ok and polish.returncode == 0 and picture.returncode == 0):
        print("ROW CHECK FAIL", {k: report[k] for k in ("align_ok", "seam_ok", "polish_rc", "picture_rc")}, flush=True)
        raise SystemExit(2)
    print("ROW CHECK PASS", flush=True)
    return report


def commit_evidence() -> None:
    """Evidence only (no mp4) onto HOS PR #385. The shared checkout stays untouched."""
    repo = Path("/Users/benjaminoats/YouTube/History Of Science")
    wt = Path("/Volumes/data/mac-mini-archive/tmp-render-scratch/j1263-hos008-wt")
    if not (wt / ".git").exists():
        run(["git", "-C", str(repo), "worktree", "add", "--detach", str(wt),
             "origin/cursor/j1257-hos008-rough-v06"])
    run(["git", "-C", str(wt), "switch", "-C", "cursor/j1257-hos008-rough-v06"])
    edit = wt / "02_Video-Projects/008_Lightning-Franklin/07_Edit-Project"
    script_src = Path(__file__).resolve() if "__file__" in globals() else WORK / "build_v08.py"
    shutil.copy2(script_src, edit / "_build_rough_v08.py")
    desk = edit / "_desk/008/rough_v08"
    if desk.exists():
        shutil.rmtree(desk)
    desk.mkdir(parents=True)
    skip_suffix = {".mp4", ".mov", ".wav"}
    for p in WORK.rglob("*"):
        if not p.is_file() or p.name.startswith("._"):
            continue
        if p.suffix.lower() in skip_suffix:
            continue
        if "special_assets" in p.parts or p.name.endswith(".building.mp4"):
            continue
        rel = p.relative_to(WORK)
        dest = desk / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, dest)
    run(["git", "-C", str(wt), "add", "-f",
         "02_Video-Projects/008_Lightning-Franklin/07_Edit-Project/_build_rough_v08.py",
         "02_Video-Projects/008_Lightning-Franklin/07_Edit-Project/_desk/008/rough_v08"])
    status = sp.run(["git", "-C", str(wt), "diff", "--cached", "--quiet"])
    if status.returncode == 0:
        print("nothing to commit", flush=True)
        return
    run(["git", "-C", str(wt), "commit", "-m",
         "hos(008): J1263 rough v08 plate in-point frame 109 for Chief review"])
    run(["git", "-C", str(wt), "push", "origin", "HEAD:cursor/j1257-hos008-rough-v06"])
    sha = sp.check_output(["git", "-C", str(wt), "rev-parse", "--short", "HEAD"], text=True).strip()
    (WORK / "PR_COMMIT.txt").write_text(sha + "\n")
    print(f"pushed evidence {sha}", flush=True)


def main() -> int:
    WORK.mkdir(parents=True, exist_ok=True)
    cuts = json.loads(V04_CUTS.read_text())
    by = {c["row"]: c for c in cuts}
    pts = video_packets(V04_MP4)
    f0, f1 = row_frame_range(pts, by["10_metal_easy"])
    metal = build_metal(f1 - f0)
    row_check(metal)
    (WORK / "phase_row.done").write_text("pass\n")
    master = splice(metal)
    evidence(master)
    gates_rc = gates(master)
    deliver(master, gates_rc)
    try:
        commit_evidence()
    except Exception:
        import traceback
        traceback.print_exc()
        (WORK / "commit_error.txt").write_text(traceback.format_exc())
    (WORK / "phase_splice.done").write_text(json.dumps(gates_rc) + "\n")
    if gates_rc["polish_rc"] or gates_rc["picture_rc"]:
        print("GATES FAIL", gates_rc, flush=True)
        return 1
    print("ALL DONE", flush=True)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception:
        import traceback
        traceback.print_exc()
        raise
