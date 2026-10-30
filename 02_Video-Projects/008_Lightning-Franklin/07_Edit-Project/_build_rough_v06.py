#!/usr/bin/env python3
"""J1257: HOS 008 rough v06.

code_graphics_v05 seeded from v04 (every row byte-identical except P3:04).
P3:04 is one compact inset map inside the clear left sky of 07_slow_news.
Rough v06 is rough v04 (e00bb897) with four byte-identical v05 FIX assets
plus the new P3:04, spliced by frame count. Base audio stays one track
(no per-segment AAC). Then one pause trim >=0.5s at a PAUSE_TRIM_v03 point.

£0. No music bed. Never overwrite v02–v05.
"""
from __future__ import annotations

import hashlib
import json
import math
import shutil
import subprocess as sp
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1920, 1080, 24
FONT = "/System/Library/Fonts/Supplemental/Didot.ttc"
CREAM = (244, 228, 195, 255)
GOLD = (211, 167, 88, 255)
LAND = (120, 88, 55)  # drawn at ~62% alpha; coverage is measured separately
INSET = (60, 60, 540, 420)  # Chief h07: clear left sky
ROW_FRAMES = 90  # 3.75s at 24fps, the v04 cut window
ROUTE_START, ROUTE_END = 1.90, 2.70
V04_SHA = "e00bb897a05c5a53843db9c7e7e62669194ced6f28f986daed6a142da54d7d5e"

WORK = Path("/Volumes/data/mac-mini-archive/tmp-render-scratch/j1257-hos008-rough-v06")
CG_V04 = Path(
    "/private/tmp/j1248-hos008-cg-v04-wt/02_Video-Projects/008_Lightning-Franklin"
    "/07_Edit-Project/code_graphics_v04"
)
CG_V05 = WORK / "code_graphics_v05"
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
PLATE = MEDIA / "04_Generated-Clips/part03/raw/v01/07_slow_news_t1.mp4"
OWB_ROOT = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
EDIT_SRC = Path(
    "/private/tmp/j1248-hos008-cg-v04-wt/02_Video-Projects/008_Lightning-Franklin/07_Edit-Project"
)

# Passed v05 FIX rows. P3:04 is rebuilt. Hashes must match cuts_rough_v05.json.
PASSED = {
    "15_likeness_fire": "overlay_15_likeness_fire.mp4",
    "03_rod_cloud": "cg_03_rod_cloud.mp4",
    "06_same_thing": "overlay_06_same_thing.mp4",
    "10_metal_easy": "overlay_10_metal_easy.mp4",
}

# Chamfered continents. Measured coverage of the inset is ~60% and every
# vertex stays inside x60-540, y60-420. Gap between them is the ocean.
WEST_BOX = (70, 146, 286, 408)   # Philadelphia
EAST_BOX = (346, 146, 528, 404)  # Paris
LABEL_PHIL = (168, 104)
LABEL_PARIS = (440, 104)


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def run(cmd: list[str]) -> None:
    print("+", " ".join(cmd[:8]), "...", flush=True)
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


def ease(t, a, b):
    if b <= a:
        return 1.0
    p = max(0.0, min(1.0, (t - a) / (b - a)))
    return p * p * (3 - 2 * p)


def box_center(box):
    return ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2)


def raster_fill() -> float:
    mask = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(mask)
    d.rounded_rectangle(WEST_BOX, radius=26, fill=255)
    d.rounded_rectangle(EAST_BOX, radius=26, fill=255)
    crop = mask.crop(INSET)
    area = (INSET[2] - INSET[0]) * (INSET[3] - INSET[1])
    return sum(1 for p in crop.get_flattened_data() if p) / area


def inside_inset(pts, pad=2) -> bool:
    x0, y0, x1, y1 = INSET
    return all(x0 + pad <= x <= x1 - pad and y0 + pad <= y <= y1 - pad for x, y in pts)


def point_on(route, q):
    steps = len(route) - 1
    j = q * steps
    k = min(int(j), steps - 1)
    u = j - k
    x = route[k][0] * (1 - u) + route[k + 1][0] * u
    y = route[k][1] * (1 - u) + route[k + 1][1] * u
    return x, y


def stroke_text(d, xy, label, font, alpha, stroke_w=3):
    fill = (*CREAM[:3], round(255 * alpha))
    sc = (36, 22, 12, round(230 * alpha))
    d.text(xy, label, font=font, fill=fill, anchor="mm", stroke_width=stroke_w, stroke_fill=sc)


def draw_map(t: float, route, phil, paris) -> Image.Image:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    land_a = ease(t, 0.25, 0.75)
    if land_a > 0:
        a = round(158 * land_a)  # 158/255 ≈ 62% opacity
        d.rounded_rectangle(WEST_BOX, radius=26, fill=(*LAND, a), outline=(*GOLD[:3], round(255 * land_a)), width=3)
        d.rounded_rectangle(EAST_BOX, radius=26, fill=(*LAND, a), outline=(*GOLD[:3], round(255 * land_a)), width=3)
    # Inset frame, wholly inside the sky box.
    x0, y0, x1, y1 = INSET
    frame_a = round(220 * land_a)
    if frame_a:
        d.rounded_rectangle((x0 + 6, y0 + 6, x1 - 6, y1 - 6), radius=16,
                            outline=(*GOLD[:3], frame_a), width=3)
        lab = ImageFont.truetype(FONT, 22, index=1)
    if t >= 0.55:
        la = ease(t, 0.55, 0.90) * (1 - ease(t, 3.35, 3.65))
        stroke_text(d, LABEL_PHIL, "PHILADELPHIA", lab, la, 2)
        stroke_text(d, LABEL_PARIS, "PARIS", lab, la, 2)
        d.ellipse((phil[0] - 7, phil[1] - 7, phil[0] + 7, phil[1] + 7), outline=(*GOLD[:3], round(255 * la)), width=4)
        if t >= 2.20:
            d.ellipse((paris[0] - 7, paris[1] - 7, paris[0] + 7, paris[1] + 7), outline=(*GOLD[:3], round(255 * la)), width=4)
    drawn = ease(t, ROUTE_START, ROUTE_END)
    if drawn > 0:
        for i in range(48):
            q = i / 47
            if q <= drawn:
                x, y = point_on(route, q)
                d.ellipse((x - 4, y - 4, x + 4, y + 4), fill=(*GOLD[:3], 235))
    # Title may stay: house label, top centre, outside the inset.
    title_a = ease(t, 0.50, 0.85) * (1 - ease(t, 3.40, 3.70))
    if title_a > 0:
        tf = ImageFont.truetype(FONT, 58, index=1)
        stroke_text(d, (W / 2, 150), "PHILADELPHIA TO PARIS", tf, title_a, 5)
    return im


def seed_v05() -> None:
    if CG_V05.exists():
        print(f"seed exists {CG_V05}", flush=True)
        return
    print(f"seeding {CG_V05} from v04", flush=True)
    shutil.copytree(CG_V04, CG_V05)


def render_p304(route, phil, paris) -> None:
    mp4 = CG_V05 / "code_graphic_008_p3_04_letter_crosses.mp4"
    mov = CG_V05 / "code_graphic_008_p3_04_letter_crosses.mov"
    jpg = CG_V05 / "code_graphic_008_p3_04_letter_crosses.jpg"
    for p in (mp4, mov, jpg):
        p.unlink(missing_ok=True)
    still = draw_map(2.85, route, phil, paris)
    Image.alpha_composite(Image.new("RGBA", (W, H), (40, 32, 24, 255)), still).convert("RGB").save(jpg, quality=90)
    paper = Image.new("RGBA", (W, H), (40, 32, 24, 255))

    def writer(path: Path, alpha: bool):
        cmd = [
            "ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgba",
            "-s", f"{W}x{H}", "-r", str(FPS), "-i", "pipe:0", "-an",
        ]
        if alpha:
            cmd += ["-c:v", "prores_ks", "-profile:v", "4", "-pix_fmt", "yuva444p10le"]
        else:
            cmd += ["-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-pix_fmt", "yuv420p"]
        cmd += ["-frames:v", str(ROW_FRAMES), str(path)]
        return sp.Popen(cmd, stdin=sp.PIPE)

    proc = writer(mp4, False)
    aproc = writer(mov, True)
    for n in range(ROW_FRAMES):
        layer = draw_map(n / FPS, route, phil, paris)
        aproc.stdin.write(layer.tobytes())
        proc.stdin.write(Image.alpha_composite(paper, layer).tobytes())
    for p in (proc, aproc):
        p.stdin.close()
        if p.wait() != 0:
            raise RuntimeError("ffmpeg graphic writer failed")
    print(f"rendered P3:04 {mp4.name} {mov.name}", flush=True)


def composite_p304() -> Path:
    out = WORK / "special_assets" / "overlay_04_letter_crosses.mp4"
    out.parent.mkdir(parents=True, exist_ok=True)
    alpha = CG_V05 / "code_graphic_008_p3_04_letter_crosses.mov"
    use_s = ROW_FRAMES / FPS
    tmp = out.with_suffix(".building.mp4")
    filt = (
        f"[0:v]scale={W}:{H}:flags=lanczos,fps={FPS},eq=brightness=0.04:contrast=0.96,format=rgba[base];"
        f"[1:v]scale={W}:{H}:flags=lanczos,fps={FPS},format=rgba[ov];"
        f"[base][ov]overlay=0:0:format=auto,format=yuv420p[v]"
    )
    run([
        "ffmpeg", "-y", "-v", "error",
        "-t", f"{use_s:.3f}", "-i", str(PLATE),
        "-t", f"{use_s:.3f}", "-i", str(alpha),
        "-filter_complex", filt, "-map", "[v]", "-an",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "17",
        "-frames:v", str(ROW_FRAMES), "-r", str(FPS),
        str(tmp),
    ])
    tmp.replace(out)
    info = stream_durations(out)
    if info.get("nb_frames") != ROW_FRAMES:
        raise RuntimeError(f"P3:04 composite frames {info.get('nb_frames')} != {ROW_FRAMES}")
    print(f"composite {out} frames={info['nb_frames']} dur={info['video']:.3f}", flush=True)
    return out


def check_strip(comp: Path) -> dict:
    """10 frames across the row. Map ink must stay inside the inset and off the ship."""
    strip = WORK / "strip"
    if strip.exists():
        shutil.rmtree(strip)
    strip.mkdir()
    plate_dir = strip / "plate"
    comp_dir = strip / "comp"
    plate_dir.mkdir()
    comp_dir.mkdir()
    use_s = ROW_FRAMES / FPS
    run(["ffmpeg", "-y", "-v", "error", "-t", f"{use_s:.3f}", "-i", str(PLATE),
         "-vf", f"scale={W}:{H}:flags=lanczos,fps={FPS},eq=brightness=0.04:contrast=0.96",
         "-frames:v", str(ROW_FRAMES), str(plate_dir / "p_%03d.png")])
    run(["ffmpeg", "-y", "-v", "error", "-i", str(comp),
         "-frames:v", str(ROW_FRAMES), str(comp_dir / "c_%03d.png")])
    # 10 frames evenly across the row (1-indexed pngs).
    idxs = [max(1, min(ROW_FRAMES, round((i + 0.5) * ROW_FRAMES / 10))) for i in range(10)]
    x0, y0, x1, y1 = INSET
    worst = []
    for n, idx in enumerate(idxs, start=1):
        plate = Image.open(plate_dir / f"p_{idx:03d}.png").convert("RGB")
        frame = Image.open(comp_dir / f"c_{idx:03d}.png").convert("RGB")
        frame.save(strip / f"row_f{n:02d}_t{(idx-1)/FPS:.2f}.jpg", quality=90)
        pp, fp = plate.load(), frame.load()
        outside = ship = 0
        # Sample every 2px. Title band is the allowed exception (top centre).
        for y in range(0, H, 2):
            for x in range(0, W, 2):
                pr, pg, pb = pp[x, y]
                fr, fg, fb = fp[x, y]
                if abs(pr - fr) + abs(pg - fg) + abs(pb - fb) < 36:
                    continue
                in_box = x0 <= x <= x1 and y0 <= y <= y1
                # House title "PHILADELPHIA TO PARIS" at y=150, size 58. Allowed to stay.
                in_title = 560 <= x <= 1380 and 90 <= y <= 210
                if not in_box and not in_title:
                    outside += 1
                if in_box:
                    luma = 0.2126 * pr + 0.7152 * pg + 0.0722 * pb
                    if luma < 110:
                        ship += 1
        worst.append({"frame": n, "src": idx, "t": round((idx - 1) / FPS, 3),
                      "outside_ink": outside, "ship_ink": ship})
        print(f"  strip f{n} t={(idx-1)/FPS:.2f}s outside={outside} ship={ship}", flush=True)
    # Land coverage on the finished alpha still (route complete).
    ratio = raster_fill()
    report = {"fill_ratio": round(ratio, 4), "frames": worst,
              "fill_ok": 0.55 <= ratio <= 0.65,
              "strip_ok": all(r["outside_ink"] == 0 and r["ship_ink"] == 0 for r in worst)}
    (strip / "STRIP_CHECK.json").write_text(json.dumps(report, indent=2) + "\n")
    if not report["fill_ok"] or not report["strip_ok"]:
        raise RuntimeError(f"P3:04 strip/fill failed: {report}")
    print(f"strip PASS fill={ratio:.3f}", flush=True)
    return report


def rewrite_sums() -> None:
    for junk in CG_V05.glob("._*"):
        junk.unlink(missing_ok=True)
    files = sorted(
        p for p in CG_V05.iterdir()
        if p.is_file() and not p.name.startswith("._")
        and p.name not in {"SHA256SUMS.txt", "MEDIA_SHA256SUMS.txt"}
    )
    (CG_V05 / "SHA256SUMS.txt").write_text("".join(f"{sha256_file(p)}  {p.name}\n" for p in files))
    media = [p for p in files if p.suffix.lower() in {".mp4", ".mov"}]
    (CG_V05 / "MEDIA_SHA256SUMS.txt").write_text("".join(f"{sha256_file(p)}  {p.name}\n" for p in media))
    # Manifest: keep every other row, mark P3:04 as the v05 rebuild.
    man_path = CG_V05 / "MANIFEST.json"
    rows = json.loads(man_path.read_text())
    for row in rows:
        if row.get("row") == "P3:04_letter_crosses":
            row["fix"] = "J1257_v05_inset"
            row["use_s"] = ROW_FRAMES / FPS
            row["encoded_s"] = ROW_FRAMES / FPS
            row["note"] = (
                "Compact inset wholly inside left sky x60-540 y60-420. "
                "Philadelphia west, Paris east, dotted route 1.90-2.70s. Illustrative."
            )
    man_path.write_text(json.dumps(rows, indent=2) + "\n")
    # Checksums of non-P3:04 media must match the v04 files on disk.
    changed = []
    for p in media:
        src = CG_V04 / p.name
        if "p3_04_letter_crosses" in p.name:
            continue
        if not src.exists() or sha256_file(src) != sha256_file(p):
            changed.append(p.name)
    if changed:
        raise RuntimeError(f"non-P3:04 media changed: {changed}")
    print("MEDIA_SHA256SUMS regenerated; other rows byte-identical", flush=True)


def assert_passed_assets() -> dict[str, Path]:
    cuts = json.loads(V05_CUTS.read_text())
    by = {c["row"]: c for c in cuts}
    out = {}
    for row, name in PASSED.items():
        path = V05_ASSETS / name
        digest = sha256_file(path)
        want = by[row]["source_sha256"]
        if digest != want:
            raise RuntimeError(f"{row} sha {digest} != cuts {want}")
        info = stream_durations(path)
        print(f"  lock {row} {digest[:12]} frames={info['nb_frames']}", flush=True)
        out[row] = path
    return out


def video_packets(path: Path) -> list[float]:
    raw = sp.check_output(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "packet=pts_time", "-of", "csv=p=0", str(path)],
        text=True,
    )
    # Packet pts are B-frame ordered. Presentation order is sorted pts.
    # 23 gaps of 2/24s are missing timestamps in the v04 encode, not a second rate.
    return sorted(float(line) for line in raw.splitlines() if line.strip())


def frame_index(pts: list[float], t: float) -> int:
    """First frame whose pts is at or after t, clamped. Exact boundary uses nearest."""
    # binary search
    lo, hi = 0, len(pts) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if pts[mid] < t - (0.5 / FPS):
            lo = mid + 1
        else:
            hi = mid
    return lo


def map_pause_joins(pause: dict) -> list[float]:
    """Output time where each removed pause was joined (v04 timeline)."""
    cuts = pause["cuts"]
    joins = []
    removed = 0.0
    for c in cuts:
        joins.append(c["from"] - removed)
        removed += c["to"] - c["from"]
    return joins


def silencedetect(path: Path) -> list[tuple[float, float]]:
    log = WORK / "silence.txt"
    sp.run(
        ["ffmpeg", "-v", "info", "-i", str(path),
         "-af", "silencedetect=noise=-35dB:d=0.50", "-f", "null", "-"],
        stderr=log.open("w"), stdout=sp.DEVNULL, check=False,
    )
    starts, spans = [], []
    for line in log.read_text(errors="replace").splitlines():
        if "silence_start:" in line:
            starts.append(float(line.split("silence_start:")[1].strip()))
        elif "silence_end:" in line and "silence_duration:" in line:
            end = float(line.split("silence_end:")[1].split("|")[0].strip())
            dur = float(line.split("silence_duration:")[1].strip())
            if starts:
                spans.append((starts.pop(0), end, dur))
    return [(a, b) for a, b, _d in spans]


def choose_pause(pts: list[float], spans, joins, row_ranges) -> dict:
    """Trim 13 frames (0.5417s) from the silence nearest a PAUSE_TRIM join, outside FIX rows."""
    trim_frames = 13
    trim_s = trim_frames / FPS
    best = None
    for a, b in spans:
        dur = b - a
        if dur < trim_s + 0.08:
            continue
        mid = (a + b) / 2
        # keep 1 frame of silence each side
        start = mid - trim_s / 2
        end = start + trim_s
        if start < a + 0.04 or end > b - 0.04:
            start = a + (dur - trim_s) / 2
            end = start + trim_s
        f0 = frame_index(pts, start)
        f1 = f0 + trim_frames
        if f1 > len(pts):
            continue
        # pause frames must not land inside a swapped row
        if any(not (f1 <= r0 or f0 >= r1) for r0, r1 in row_ranges):
            continue
        dist = min(abs(mid - j) for j in joins)
        cand = {"silence": [a, b], "trim_start": start, "trim_end": end,
                "frame0": f0, "frame1": f1, "trim_s": trim_s, "join_dist": dist}
        if best is None or dist < best["join_dist"]:
            best = cand
    if best is None:
        raise RuntimeError("no PAUSE_TRIM-adjacent silence long enough to trim")
    if best["join_dist"] > 2.5:
        raise RuntimeError(f"nearest pause join is {best['join_dist']:.2f}s from a silence; refusing")
    print(f"pause trim frames {best['frame0']}-{best['frame1']} "
          f"t {best['trim_start']:.3f}-{best['trim_end']:.3f} join_dist={best['join_dist']:.3f}", flush=True)
    return best


def row_frame_range(pts: list[float], cut: dict) -> tuple[int, int]:
    f0 = frame_index(pts, float(cut["timeline_in"]))
    f1 = frame_index(pts, float(cut["timeline_out"]))
    return f0, f1


def apply_pause_trim(swapped: Path, chosen: dict) -> Path:
    """Trim one pause. Video frame span and audio PTS span are the same length."""
    pts = video_packets(swapped)
    f0, f1 = int(chosen["frame0"]), int(chosen["frame1"])
    span = pts[f1] - pts[f0]
    expect = (f1 - f0) / FPS
    if abs(span - expect) > 0.002:
        raise RuntimeError(f"pause frames {f0}-{f1} span {span:.6f}s, expected {expect:.6f}s")
    silence = chosen.get("silence") or [0, 0]
    if not (silence[0] + 0.02 <= pts[f0] and pts[f1] <= silence[1] - 0.02):
        raise RuntimeError(
            f"cut {pts[f0]:.3f}-{pts[f1]:.3f} is not inside silence {silence}"
        )
    chosen["trim_start"] = pts[f0]
    chosen["trim_end"] = pts[f1]
    chosen["trim_s"] = span
    chosen["audio"] = (
        "splice audio stream-copied; this pause cut is one AAC encode of the joined track"
    )
    note = json.loads((WORK / "PAUSE_TRIM_APPLIED.json").read_text())
    note["choice"] = chosen
    (WORK / "PAUSE_TRIM_APPLIED.json").write_text(json.dumps(note, indent=2) + "\n")
    print(
        f"pause trim exact frames {f0}-{f1} pts {pts[f0]:.6f}-{pts[f1]:.6f} span={span:.6f}",
        flush=True,
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
    out = WORK / "hos_008_rough_v06.mp4"
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


def splice(new_p304: Path, passed: dict[str, Path], pause: dict, resume: bool = False) -> Path:
    pts = video_packets(V04_MP4)
    print(f"v04 video packets {len(pts)} first={pts[0]:.4f} last={pts[-1]:.4f}", flush=True)
    # CFR check
    deltas = [round((b - a) * 24000) for a, b in zip(pts, pts[1:])]
    on_grid = sum(1 for d in deltas if d == 1000)
    if on_grid < len(deltas) * 0.99:
        raise RuntimeError(f"v04 timing is not 24fps: {on_grid}/{len(deltas)} steps are 1/24")
    cuts = json.loads(V04_CUTS.read_text())
    by = {c["row"]: c for c in cuts}
    repl = {
        "15_likeness_fire": passed["15_likeness_fire"],
        "03_rod_cloud": passed["03_rod_cloud"],
        "04_letter_crosses": new_p304,
        "06_same_thing": passed["06_same_thing"],
        "10_metal_easy": passed["10_metal_easy"],
    }
    ranges = {}
    for row, path in repl.items():
        f0, f1 = row_frame_range(pts, by[row])
        info = stream_durations(path)
        have = int(info["nb_frames"])
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
    spans = silencedetect(V04_MP4)
    chosen = choose_pause(pts, spans, joins, [(a, b) for a, b, _ in ordered])
    (WORK / "PAUSE_TRIM_APPLIED.json").write_text(json.dumps({
        "source": "PAUSE_TRIM_v03.json joins, nearest remaining silence >=0.5s",
        "choice": chosen,
        "vo": "pause only; trim sits inside silencedetect, clear of FIX rows",
    }, indent=2) + "\n")

    # Build keep/replace segments in frame order, dropping the pause frames.
    events = []  # (start, end, path or None)
    cursor = 0
    nframes = len(pts)
    pf0, pf1 = chosen["frame0"], chosen["frame1"]
    pieces = [(a, b, p) for a, b, p in ordered]
    pieces.append((pf0, pf1, "DROP"))
    pieces.sort(key=lambda r: r[0])
    for a, b, src in pieces:
        if a > cursor:
            events.append((cursor, a, None))
        if src != "DROP":
            events.append((a, b, src))
        cursor = max(cursor, b)
    if cursor < nframes:
        events.append((cursor, nframes, None))

    # Pass 1: replace the five rows on the master video. Audio is stream-copied,
    # one continuous track, no per-segment AAC encode.
    inputs = ["-i", str(V04_MP4)]
    lines = []
    last = "[0:v]"
    for i, (f0, f1, _src) in enumerate(ordered, start=1):
        inputs += ["-i", str(_src)]
        start_pts = pts[f0]
        lines.append(f"[{i}:v]setpts=PTS-STARTPTS+{start_pts:.6f}/TB[o{i}]")
        lines.append(
            f"{last}[o{i}]overlay=eof_action=pass:repeatlast=0:"
            f"enable='between(n\\,{f0}\\,{f1 - 1})'[v{i}]"
        )
        last = f"[v{i}]"
    graph = ";".join(lines)
    (WORK / "splice_graph.txt").write_text(graph + "\n")
    swapped = WORK / "hos_008_rough_v06_swapped.mp4"
    if resume:
        got = stream_durations(swapped)
        if got.get("nb_frames") != nframes:
            raise RuntimeError(f"swapped frames {got.get('nb_frames')} != {nframes}")
        print(f"resume swapped frames={got['nb_frames']} audio={got['audio']:.3f}", flush=True)
    else:
        run([
            "ffmpeg", "-y", "-v", "error", *inputs,
            "-filter_complex", graph,
            "-map", last, "-map", "0:a:0",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
            "-c:a", "copy",
            "-movflags", "+faststart", str(swapped),
        ])
    # Pass 2: drop one pause by frame count. Later video PTS shift by that
    # exact span so v04's timestamp gaps stay and the end stays locked to the
    # audio. Audio is the same PTS span, encoded once (the splice itself was
    # a single audio copy, not a per-segment AAC re-encode).
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
    # Shift cut times for the removed pause so gates sample the new picture.
    shift = chosen["trim_s"]
    t_cut = chosen["trim_start"]
    new_cuts = []
    for c in cuts:
        c = dict(c)
        tin, tout = float(c["timeline_in"]), float(c["timeline_out"])
        if tout <= t_cut:
            pass
        elif tin >= t_cut + shift - 0.01:
            c["timeline_in"] = round(tin - shift, 4)
            c["timeline_out"] = round(tout - shift, 4)
        else:
            # pause landed inside this row: shorten it
            c["timeline_out"] = round(tout - shift, 4)
        new_cuts.append(c)
    v05 = {c["row"]: c for c in json.loads(V05_CUTS.read_text())}
    for c in new_cuts:
        if c["row"] in repl:
            path = repl[c["row"]]
            c["source"] = path.name
            c["source_path"] = str(path)
            c["source_sha256"] = sha256_file(path)
            if c["row"] in PASSED:
                if c["source_sha256"] != v05[c["row"]]["source_sha256"]:
                    raise RuntimeError(f"sha drifted for {c['row']}")
            c["disposition"] = f"J1257 v06 frame-exact ({path.name})"
    (WORK / "cuts_rough_v06.json").write_text(json.dumps(new_cuts, indent=2) + "\n")
    return out


def evidence(master: Path) -> None:
    ev = WORK / "composite_evidence_v06"
    ev.mkdir(parents=True, exist_ok=True)
    cuts = json.loads((WORK / "cuts_rough_v06.json").read_text())
    by = {c["row"]: c for c in cuts}

    def grab(t, dest):
        run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.3f}", "-i", str(master),
             "-frames:v", "1", "-q:v", "2", str(dest)])

    c = by["04_letter_crosses"]
    tin, tout = float(c["timeline_in"]), float(c["timeline_out"])
    for pct in (10, 25, 50, 75, 90):
        grab(tin + (tout - tin) * pct / 100, ev / f"p304_p{pct}.jpg")
    same = by["06_same_thing"]
    grab(float(same["timeline_in"]) + 5.14, ev / "p406_spoken_electricity.jpg")
    grab(float(same["timeline_in"]) + 6.64, ev / "p406_spoken_plus_1_5s.jpg")
    thumbs = []
    for row, name in [
        ("15_likeness_fire", "p215"),
        ("03_rod_cloud", "p303"),
        ("04_letter_crosses", "p304"),
        ("06_same_thing", "p406"),
        ("10_metal_easy", "p510"),
    ]:
        cc = by[row]
        t = (float(cc["timeline_in"]) + float(cc["timeline_out"])) / 2
        dest = ev / f"{name}_p50.jpg"
        grab(t, dest)
        thumbs.append((row, Image.open(dest).convert("RGB")))
    sheet = Image.new("RGB", (480, 310 * len(thumbs)), (45, 33, 23))
    d = ImageDraw.Draw(sheet)
    font = ImageFont.truetype(FONT, 22, index=1)
    for i, (label, img) in enumerate(thumbs):
        y = i * 310
        sheet.paste(img.resize((480, 270)), (0, y))
        d.text((12, y + 278), label, fill="white", font=font)
    sheet_path = ev / "CONTACT_SHEET_FIX5.jpg"
    sheet.save(sheet_path, quality=90)
    shutil.copy2(sheet_path, WORK / "CONTACT_SHEET_FIX5.jpg")
    print(f"evidence {ev}", flush=True)


def gates(master: Path) -> dict:
    cuts = WORK / "cuts_rough_v06.json"
    pool = WORK / "pool_rough_v06.json"
    shutil.copy2(V04_POOL, pool)
    polish_json = WORK / "polish_gate_rough_v06.json"
    polish = sp.run(
        [sys.executable, str(OWB_ROOT / "scripts/polish_gate.py"), str(master),
         "--cuts", str(cuts), "--out", str(polish_json)],
        capture_output=True, text=True,
    )
    (WORK / "polish_gate_rough_v06.txt").write_text(polish.stdout + polish.stderr)
    print(polish.stdout[-600:], flush=True)
    pq = WORK / "picture_qa_rough_v06"
    picture = sp.run(
        [sys.executable, str(OWB_ROOT / "scripts/picture_qa.py"), str(master),
         "--cuts", str(cuts), "--pool", str(pool), "--out-dir", str(pq)],
        capture_output=True, text=True,
    )
    (WORK / "picture_qa_rough_v06.txt").write_text(picture.stdout + picture.stderr)
    print(picture.stdout[-600:], flush=True)
    note = {"status": "SKIPPED_NO_BED", "reason": "No new bed. Job brief.", "version": "rough_v06"}
    (WORK / "music_gate_rough_v06.json").write_text(json.dumps(note, indent=2) + "\n")
    (WORK / "music_gate_rough_v06.txt").write_text("SKIPPED_NO_BED\n")
    return {"polish_rc": polish.returncode, "picture_rc": picture.returncode}


def deliver(master: Path, gates_rc: dict) -> None:
    info = json.loads((WORK / "DURATION.json").read_text())
    summary = {
        "version": "rough_v06",
        "job": "J1257",
        "source_master": str(V04_MP4),
        "source_sha256": sha256_file(V04_MP4),
        "master_sha256": sha256_file(master),
        "durations": info,
        "gates": gates_rc,
        "pause": json.loads((WORK / "PAUSE_TRIM_APPLIED.json").read_text()),
        "note": "Parked for Chief: graphics + composite. No finished-film PASS. No music bed.",
    }
    (WORK / "ROUGH_V06_SUMMARY.json").write_text(json.dumps(summary, indent=2) + "\n")
    names = [
        "hos_008_rough_v06.mp4", "cuts_rough_v06.json", "pool_rough_v06.json",
        "polish_gate_rough_v06.json", "polish_gate_rough_v06.txt",
        "picture_qa_rough_v06.txt", "music_gate_rough_v06.json", "music_gate_rough_v06.txt",
        "ROUGH_V06_SUMMARY.json", "DURATION.json", "PAUSE_TRIM_APPLIED.json",
        "CONTACT_SHEET_FIX5.jpg",
    ]
    dests = [
        MEDIA / "07_Edit-Project/_precheck/rough_v06",
        Path("/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/HOS UAT/HOS-008_Lightning-Franklin_rough_v06"),
        Path("/Volumes/data/mac-mini-archive/YouTube/History Of Science/02_Video-Projects/008_Lightning-Franklin/07_Edit-Project/_desk/008/rough_v06"),
    ]
    # Refuse to touch v02-v05.
    for dest in dests:
        if dest.name in {"rough_v02", "rough_v03", "rough_v04", "rough_v05"}:
            raise RuntimeError(dest)
        dest.mkdir(parents=True, exist_ok=True)
        for name in names:
            src = WORK / name
            if src.exists():
                shutil.copy2(src, dest / name)
        ev = WORK / "composite_evidence_v06"
        target = dest / "composite_evidence_v06"
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(ev, target)
        pq = WORK / "picture_qa_rough_v06"
        if pq.exists():
            tq = dest / "picture_qa_rough_v06"
            if tq.exists():
                shutil.rmtree(tq)
            shutil.copytree(pq, tq)
        sums = []
        for p in sorted(dest.iterdir()):
            if p.is_file() and not p.name.startswith("._") and p.suffix != ".partial":
                sums.append(f"{sha256_file(p)}  {p.name}\n")
        (dest / "SHA256SUMS.txt").write_text("".join(sums))
        print(f"delivered {dest}", flush=True)
    # code graphics folder beside the film media checkout (not over v04).
    film_cg = MEDIA / "07_Edit-Project/code_graphics_v05"
    if film_cg.exists():
        shutil.rmtree(film_cg)
    shutil.copytree(CG_V05, film_cg)
    print("ALL DONE", flush=True)


def phase_graphics() -> None:
    if sha256_file(V04_MP4) != V04_SHA:
        raise RuntimeError("v04 master sha mismatch")
    seed_v05()
    ratio = raster_fill()
    phil, paris = box_center(WEST_BOX), box_center(EAST_BOX)
    route = [
        phil,
        ((phil[0] * 2 + paris[0]) / 3, (phil[1] + paris[1]) / 2 - 28),
        ((phil[0] + paris[0] * 2) / 3, (phil[1] + paris[1]) / 2 - 36),
        paris,
    ]
    print(f"fill={ratio:.3f} phil={tuple(round(v,1) for v in phil)} paris={tuple(round(v,1) for v in paris)}", flush=True)
    if not (0.55 <= ratio <= 0.65):
        raise RuntimeError(f"fill {ratio}")
    corners = []
    for box in (WEST_BOX, EAST_BOX):
        corners += [(box[0], box[1]), (box[2], box[1]), (box[2], box[3]), (box[0], box[3])]
    if not inside_inset(corners, pad=2) or not inside_inset(route, pad=2):
        raise RuntimeError(f"map left the inset route={route}")
    lab = ImageFont.truetype(FONT, 22, index=1)
    for text, xy in (("PHILADELPHIA", LABEL_PHIL), ("PARIS", LABEL_PARIS)):
        bbox = lab.getbbox(text)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        box = (xy[0] - w / 2 - 2, xy[1] - h / 2 - 2, xy[0] + w / 2 + 2, xy[1] + h / 2 + 2)
        x0, y0, x1, y1 = INSET
        if not (x0 <= box[0] and box[2] <= x1 and y0 <= box[1] and box[3] <= y1):
            raise RuntimeError(f"label {text} bbox {box} outside inset")
    render_p304(route, phil, paris)
    comp = composite_p304()
    check_strip(comp)
    rewrite_sums()
    (WORK / "phase_graphics.done").write_text("ok\n")


def phase_splice(resume: bool = False) -> None:
    rewrite_sums()
    passed = assert_passed_assets()
    comp = WORK / "special_assets" / "overlay_04_letter_crosses.mp4"
    pause = json.loads(V04_PAUSE.read_text())
    master = splice(comp, passed, pause, resume=resume)
    evidence(master)
    gates_rc = gates(master)
    deliver(master, gates_rc)
    (WORK / "phase_splice.done").write_text("ok\n")


def main() -> int:
    phase = sys.argv[1] if len(sys.argv) > 1 else "graphics"
    WORK.mkdir(parents=True, exist_ok=True)
    if phase == "graphics":
        phase_graphics()
    elif phase == "splice":
        phase_splice()
    elif phase == "trim":
        phase_splice(resume=True)
    elif phase == "all":
        phase_graphics()
        phase_splice()
    else:
        raise SystemExit(f"unknown phase {phase}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception:
        import traceback
        traceback.print_exc()
        raise SystemExit(1)
