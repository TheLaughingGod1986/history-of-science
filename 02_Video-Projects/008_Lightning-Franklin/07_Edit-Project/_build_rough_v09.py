#!/usr/bin/env python3
"""J1267: HOS 008 rough v09.

Same frame-exact splice as rough v08 (from v04 e00bb897), except P5:10 is
source frames 109-150 (42 frames) and the 29 freed frames become a lead-in
on the head of 11_safe_path. £0. New folders only.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import shutil
import subprocess as sp
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1920, 1080, 24
FONT = "/System/Library/Fonts/Supplemental/Didot.ttc"
CREAM = (244, 228, 195, 255)
GOLD = (211, 167, 88, 255)
V04_SHA = "e00bb897a05c5a53843db9c7e7e62669194ced6f28f986daed6a142da54d7d5e"
ALPHA_LOCKED = "bb821f402a2d1ca5a1536a6592e572b8a4d1653d6573ca733c2ae853db4c8056"
PLATE_FRAME0 = 109
METAL_N = 42
LEAD_N = 29
# On-screen safe-path body in v04/v08 is 157 frames. The asset file is 168.
# 29 + 157 = 186 fills 461.047-468.796s and keeps 12923 frames.
# 29 + 168 = 197 would run 11 frames into the next row.
SAFE_BODY_N = 157
SAFE_N = LEAD_N + SAFE_BODY_N

WORK = Path("/private/tmp/j1267-hos008-rough-v09")
CG_SRC = Path(
    "/Volumes/data/mac-mini-archive/mini-tmp-scratch/2026-10-30/j1248-hos008-cg-v04-wt"
    "/02_Video-Projects/008_Lightning-Franklin/07_Edit-Project/_build_code_graphics_v04.py"
)
LOCKED_ALPHA = Path(
    "/Volumes/data/mac-mini-archive/tmp-render-scratch/j1257-hos008-rough-v06"
    "/code_graphics_v05/code_graphic_008_p5_10_metal_easy.mov"
)
SAFE_ASSET = Path(
    "/Volumes/data/mac-mini-archive/tmp-render-scratch/j1218-hos008-rough-v03"
    "/special_assets/cg_11_safe_path.mp4"
)
V08_MASTER = Path(
    "/Users/benjaminoats/YouTube/hos-008-lightning/02_Video-Projects"
    "/008_Lightning-Franklin/07_Edit-Project/_precheck/rough_v08/hos_008_rough_v08.mp4"
)
PART_WAV = Path(
    "/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects"
    "/008_Lightning-Franklin/02_Voiceover/hos_008_part05_the_rod_on_every_roof_v01b.wav"
)
STT = Path(
    "/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects"
    "/008_Lightning-Franklin/02_Voiceover/stt"
    "/hos_008_part05_the_rod_on_every_roof_v01b/stt_raw.json"
)
OWB_ROOT = Path("/Users/benjaminoats/YouTube/orbit-with-ben")


def load_v08():
    p = Path("/Volumes/data/mac-mini-archive/tmp-render-scratch/j1263-hos008-rough-v08/build_v08.py")
    spec = importlib.util.spec_from_file_location("build_v08", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.WORK = WORK
    return mod


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def run(cmd: list[str]) -> None:
    print(" ", " ".join(cmd[:10]), "...", flush=True)
    sp.run(cmd, check=True)


def ease(t, a, b):
    if b <= a:
        return 1.0 if t >= a else 0.0
    p = max(0.0, min(1.0, (t - a) / (b - a)))
    return p * p * (3 - 2 * p)


def stroke_text(d, xy, label, font, alpha, stroke_w=7):
    fill = (*CREAM[:3], round(255 * alpha))
    sc = (36, 22, 12, round(230 * alpha))
    d.text(xy, label, font=font, fill=fill, anchor="mm", stroke_width=stroke_w, stroke_fill=sc)


def paper():
    rng = np.random.default_rng(8329)
    y, x = np.mgrid[:H, :W]
    v = np.clip(((x - W / 2) / (W / 2)) ** 2 + ((y - H / 2) / (H / 2)) ** 2, 0, 1.4)
    a = np.zeros((H, W, 3))
    noise = rng.normal(0, 1.2, (H, W))
    for c, base in enumerate((136, 100, 66)):
        a[:, :, c] = base - 42 * v + noise
    return Image.fromarray(np.uint8(np.clip(a, 0, 255))).convert("RGBA")


def draw_path(draw, pts, p, color, width):
    if p <= 0:
        return
    lengths = [math.dist(a, b) for a, b in zip(pts, pts[1:])]
    left = sum(lengths) * min(p, 1)
    for a, b, L in zip(pts, pts[1:], lengths):
        if left <= 0:
            break
        q = min(1, left / max(L, 0.001))
        draw.line([a, (a[0] + q * (b[0] - a[0]), a[1] + q * (b[1] - a[1]))], fill=color, width=width)
        left -= L


def metal_alpha(t: float) -> Image.Image:
    """Same geometry as bb821f40, retimed to a 1.75s / 42-frame row."""
    im = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(im)
    callout = ease(t, 0.0, 0.125)  # fully on by 0.125s, so by 0.15s
    draw_path(d, [(1180, 280), (1180, 920)], callout, GOLD, 12)
    for yy in range(320, 900, 64):
        if callout <= 0:
            break
        r, g, b, _a = CREAM
        col = (r, g, b, round(255 * callout))
        d.ellipse((1156, yy - 12, 1204, yy + 12), outline=col, width=4)
    # Trace starts at 0.30s and reaches the rod foot (y=920) by 1.50s (<=1.55).
    if t >= 0.30:
        draw_path(d, [(1180, 280), (1180, 920)], ease(t, 0.30, 1.50), CREAM, 5)
        if 0.40 <= t <= 1.75:
            pts = [(1180, 280), (1180, 600), (1180, 920)]
            for i in range(16):
                q = (i / 16 + (t - 0.40) * 0.23) % 1
                j = q * (len(pts) - 1)
                k = min(int(j), len(pts) - 2)
                u = j - k
                x = pts[k][0] * (1 - u) + pts[k + 1][0] * u
                y = pts[k][1] * (1 - u) + pts[k + 1][1] * u
                d.ellipse((x - 5, y - 5, x + 5, y + 5), outline=GOLD, width=4)
    # Full alpha by 0.48s (<=0.50) and held to the row end. No fade-out.
    alpha = 1.0 if t >= 0.48 else ease(t, 0.12, 0.48)
    font = ImageFont.truetype(FONT, 72, index=1)
    stroke_text(d, (W / 2, 150), "METAL CONDUCTS", font, alpha, stroke_w=7)
    return im


def render_alpha() -> Path:
    out_dir = WORK / "code_graphics_v06"
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / "code_graphic_008_p5_10_metal_easy.mov"
    if sha256_file(LOCKED_ALPHA) != ALPHA_LOCKED:
        raise RuntimeError("locked alpha bb821f40 moved; refusing")
    raw = sp.Popen(
        [
            "ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgba",
            "-s", f"{W}x{H}", "-r", str(FPS), "-i", "pipe:0", "-an",
            "-c:v", "prores_ks", "-profile:v", "4", "-pix_fmt", "yuva444p10le",
            str(dest),
        ],
        stdin=sp.PIPE,
    )
    assert raw.stdin is not None
    for i in range(METAL_N):
        raw.stdin.write(metal_alpha(i / FPS).tobytes())
    raw.stdin.close()
    if raw.wait() != 0:
        raise RuntimeError("alpha encode failed")
    print(f"alpha {dest} sha={sha256_file(dest)[:12]}", flush=True)
    return dest


def render_leadin() -> Path:
    """Opening state of the card: period paper, SAFE PATH DOWN fading in. No footage."""
    bg = paper()
    font = ImageFont.truetype(FONT, 66, index=1)
    dest = WORK / "code_graphics_v06" / "leadin_11_safe_path.mp4"
    raw = sp.Popen(
        [
            "ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
            "-s", f"{W}x{H}", "-r", str(FPS), "-i", "pipe:0", "-an",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p",
            "-frames:v", str(LEAD_N), str(dest),
        ],
        stdin=sp.PIPE,
    )
    assert raw.stdin is not None
    for i in range(LEAD_N):
        t = i / FPS
        # Full by the last lead-in frame (1.167s). Fade across the 29 frames.
        alpha = ease(t, 0.04, (LEAD_N - 1) / FPS)
        layer = Image.new("RGBA", (W, H))
        d = ImageDraw.Draw(layer)
        stroke_text(d, (W / 2, 150), "SAFE PATH DOWN", font, alpha, stroke_w=6)
        frame = Image.alpha_composite(bg, layer).convert("RGB")
        raw.stdin.write(frame.tobytes())
    raw.stdin.close()
    if raw.wait() != 0:
        raise RuntimeError("lead-in encode failed")
    return dest


def build_safe(leadin: Path) -> Path:
    dest = WORK / "code_graphics_v06" / "cg_11_safe_path.mp4"
    # 29-frame lead-in + the 157 frames that actually play in the v08 row.
    run([
        "ffmpeg", "-y", "-v", "error",
        "-i", str(leadin), "-i", str(SAFE_ASSET),
        "-filter_complex",
        f"[1:v]trim=end_frame={SAFE_BODY_N},setpts=PTS-STARTPTS[tail];"
        f"[0:v][tail]concat=n=2:v=1:a=0[v]",
        "-map", "[v]", "-an",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p",
        "-frames:v", str(SAFE_N), str(dest),
    ])
    return dest


def build_metal(v08, alpha: Path) -> Path:
    asset = WORK / "special_assets" / "overlay_10_metal_easy.mp4"
    asset.parent.mkdir(parents=True, exist_ok=True)
    use_s = METAL_N / FPS
    off = PLATE_FRAME0 / FPS
    filt = (
        f"[0:v]scale={W}:{H}:flags=lanczos,fps={FPS},"
        f"eq=brightness=0.04:contrast=0.96,format=rgba[base];"
        f"[1:v]scale={W}:{H}:flags=lanczos,fps={FPS},format=rgba[ov];"
        f"[base][ov]overlay=0:0:format=auto,format=yuv420p[v]"
    )
    tmp = asset.with_suffix(".building.mp4")
    run([
        "ffmpeg", "-y", "-v", "error",
        "-ss", f"{off:.6f}", "-t", f"{use_s:.3f}", "-i", str(v08.PLATE),
        "-t", f"{use_s:.3f}", "-i", str(alpha),
        "-filter_complex", filt, "-map", "[v]", "-an",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p",
        "-frames:v", str(METAL_N), str(tmp),
    ])
    tmp.replace(asset)
    info = v08.stream_durations(asset)
    if info["nb_frames"] != METAL_N:
        raise RuntimeError(f"metal frames {info['nb_frames']} != {METAL_N}")
    if sha256_file(LOCKED_ALPHA) != ALPHA_LOCKED:
        raise RuntimeError("locked alpha changed during composite")
    note = {
        "plate": str(v08.PLATE),
        "source_frames": "109-150 inclusive",
        "plate_in_point_s": off,
        "frames": METAL_N,
        "alpha": str(alpha),
        "alpha_sha256": sha256_file(alpha),
        "locked_alpha_left_untouched": str(LOCKED_ALPHA),
        "locked_alpha_sha256": ALPHA_LOCKED,
        "new_composite_sha256": sha256_file(asset),
        "timing": {
            "callout_on_by_s": 0.125,
            "trace_start_s": 0.30,
            "trace_reaches_foot_s": 1.50,
            "label_full_from_s": 0.48,
            "label_fade_out": False,
        },
    }
    (WORK / "PLATE_INPOINT.json").write_text(json.dumps(note, indent=2) + "\n")
    print(f"metal frames={METAL_N} sha={note['new_composite_sha256'][:12]}", flush=True)
    return asset


def row_check(v08, metal: Path) -> dict:
    use_s = METAL_N / FPS
    off = PLATE_FRAME0 / FPS
    samples = []
    ev = WORK / "row_probe"
    ev.mkdir(parents=True, exist_ok=True)
    sys.path.insert(0, str(OWB_ROOT / "scripts"))
    import polish_gate as pg

    worst = 0.0
    for pct in (10, 25, 50, 75, 90):
        t_row = use_s * pct / 100
        t_plate = off + t_row
        v08.grab(metal, t_row, ev / f"p{pct}.jpg")
        meas = v08.tip_offset(v08.plate_gray(t_plate))
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
            f"({meas['offset_pct_of_width']:+.2f}%)",
            flush=True,
        )
    limit = 0.01 * W
    align_ok = worst <= limit + 0.05
    seam_ok = all(not s["vertical_seams"] for s in samples)
    report = {
        "plate_in_point_s": off,
        "source_frame": PLATE_FRAME0,
        "source_frame_end_inclusive": 150,
        "window_frames": METAL_N,
        "aim_pct": 1.0,
        "align_ok": align_ok,
        "seam_ok": seam_ok,
        "worst_abs_px": worst,
        "limit_px": limit,
        "samples": samples,
    }
    (WORK / "ROD_TRACE.json").write_text(json.dumps(report, indent=2) + "\n")
    if not (align_ok and seam_ok):
        print("ROW ALIGN FAIL", report["worst_abs_px"], flush=True)
        raise SystemExit(2)
    print("ROW ALIGN PASS", flush=True)
    return report


def splice(v08, metal: Path, safe: Path) -> Path:
    if sha256_file(v08.V04_MP4) != V04_SHA:
        raise RuntimeError("v04 master sha mismatch")
    pts = v08.video_packets(v08.V04_MP4)
    print(f"v04 video packets {len(pts)}", flush=True)
    cuts = json.loads(v08.V04_CUTS.read_text())
    by = {c["row"]: c for c in cuts}
    v05 = {c["row"]: c for c in json.loads(v08.V05_CUTS.read_text())}
    v06 = {c["row"]: c for c in json.loads(v08.V06_CUTS.read_text())}
    repl = dict(v08.PASSED)
    repl["04_letter_crosses"] = v08.V06_P304
    repl["10_metal_easy"] = metal
    repl["11_safe_path"] = safe
    if sha256_file(v08.V06_P304) != v06["04_letter_crosses"]["source_sha256"]:
        raise RuntimeError("P3:04 inset is not the locked v06 asset")
    for row, path in v08.PASSED.items():
        digest = sha256_file(path)
        if digest != v05[row]["source_sha256"]:
            raise RuntimeError(f"{row} sha drifted")
    mf0, mf1 = v08.row_frame_range(pts, by["10_metal_easy"])
    sf0, sf1 = v08.row_frame_range(pts, by["11_safe_path"])
    if mf1 - mf0 != 71 or sf1 - sf0 != SAFE_BODY_N or mf1 != sf0:
        raise RuntimeError(f"unexpected windows metal {mf0}-{mf1} safe {sf0}-{sf1}")
    ranges = {}
    for row, path in repl.items():
        if row == "10_metal_easy":
            f0, f1 = mf0, mf0 + METAL_N
        elif row == "11_safe_path":
            f0, f1 = mf0 + METAL_N, sf1
        else:
            f0, f1 = v08.row_frame_range(pts, by[row])
        have = v08.stream_durations(path)["nb_frames"]
        need = f1 - f0
        print(f"  row {row} frames {f0}-{f1} need={need} asset={have}", flush=True)
        if have != need:
            raise RuntimeError(f"{row} asset frames {have} != window {need}")
        ranges[row] = (f0, f1, path)
    ordered = sorted(ranges.values(), key=lambda r: r[0])
    for (a0, a1, _), (b0, b1, _) in zip(ordered, ordered[1:]):
        if a1 > b0:
            raise RuntimeError(f"overlapping replacements {a0}-{a1} and {b0}-{b1}")
    joins = v08.map_pause_joins(json.loads(v08.V04_PAUSE.read_text()))
    spans = v08.parse_silence(v08.SILENCE_LOG)
    chosen = v08.choose_pause(pts, spans, joins, [(a, b) for a, b, _ in ordered], cuts)
    (WORK / "PAUSE_TRIM_APPLIED.json").write_text(json.dumps({
        "source": "PAUSE_TRIM_v03.json joins, after 0:30, trim contains a shot boundary",
        "choice": chosen,
        "vo": "pause only; trim sits inside silencedetect, clear of the hook and the FIX rows",
        "moved_from": "v06 trim 9.167-9.708s inside the kite plate",
    }, indent=2) + "\n")
    inputs = ["-i", str(v08.V04_MP4)]
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
    swapped = WORK / "hos_008_rough_v09_swapped.mp4"
    run([
        "ffmpeg", "-y", "-v", "error", *inputs,
        "-filter_complex", graph,
        "-map", last, "-map", "0:a:0",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "copy",
        "-movflags", "+faststart", str(swapped),
    ])
    out = v08.apply_pause_trim(swapped, chosen)
    # apply_pause_trim writes hos_008_rough_v08.mp4 because that name is inside v08.
    baked = WORK / "hos_008_rough_v08.mp4"
    final = WORK / "hos_008_rough_v09.mp4"
    if baked.exists():
        baked.replace(final)
    elif not final.exists():
        raise RuntimeError("pause trim did not write a master")
    info = v08.stream_durations(final)
    (WORK / "DURATION.json").write_text(json.dumps(info, indent=2) + "\n")
    print("DURATIONS", json.dumps(info), flush=True)
    if info.get("nb_frames") != 12923:
        raise RuntimeError(f"frame count {info.get('nb_frames')} != 12923")
    frame = 1 / FPS
    problems = []
    if abs(info["format"] - 539.626) > 0.05:
        problems.append(f"format {info['format']:.4f}")
    if abs(info["video"] - 539.500) > 0.05:
        problems.append(f"video {info['video']:.4f}")
    if info.get("av_end_offset", 9) > frame + 0.001:
        problems.append(f"A/V {info['av_end_offset']:.4f}")
    if problems:
        raise RuntimeError("; ".join(problems))
    t0, t1 = chosen["trim_start"], chosen["trim_end"]
    new_cuts = []
    for c in cuts:
        c = dict(c)
        nin, nout = v08.remap_cut_time(float(c["timeline_in"]), float(c["timeline_out"]), t0, t1)
        if c["row"] == "10_metal_easy":
            nout = nin + METAL_N / FPS
        elif c["row"] == "11_safe_path":
            # starts where metal now ends; end stays
            metal_in = v08.remap_cut_time(
                float(by["10_metal_easy"]["timeline_in"]),
                float(by["10_metal_easy"]["timeline_out"]), t0, t1,
            )[0]
            nin = metal_in + METAL_N / FPS
        c["timeline_in"] = round(nin, 4)
        c["timeline_out"] = round(nout, 4)
        new_cuts.append(c)
    for c in new_cuts:
        if c["row"] in repl:
            path = repl[c["row"]]
            c["source"] = path.name
            c["source_path"] = str(path)
            c["source_sha256"] = sha256_file(path)
            if c["row"] == "10_metal_easy":
                c["framing"] = {"offset": PLATE_FRAME0 / FPS, "source_frames": "109-150"}
                c["disposition"] = "J1267 v09 plate frames 109-150 (42) retimed alpha v06"
            elif c["row"] == "11_safe_path":
                c["disposition"] = (
                    f"J1267 v09 {LEAD_N}-frame SAFE PATH DOWN lead-in + {SAFE_BODY_N} existing frames"
                )
            else:
                c["disposition"] = f"J1267 v09 frame-exact lock ({path.name})"
    (WORK / "cuts_rough_v09.json").write_text(json.dumps(new_cuts, indent=2) + "\n")
    note = json.loads((WORK / "PAUSE_TRIM_APPLIED.json").read_text())
    note["choice"] = chosen
    (WORK / "PAUSE_TRIM_APPLIED.json").write_text(json.dumps(note, indent=2) + "\n")
    return final


def grab(master: Path, t: float, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    start = max(0.0, t - 1.0)
    rel = t - start
    run([
        "ffmpeg", "-y", "-v", "error",
        "-ss", f"{start:.3f}", "-i", str(master),
        "-vf", f"trim=start={rel:.3f}:duration=0.05,setpts=PTS-STARTPTS",
        "-frames:v", "1", "-q:v", "2", str(dest),
    ])


def vo_report(master: Path) -> dict:
    """Map part-05 word times onto v08/v09 by correlating the part wav with the master."""
    words = [w for w in json.loads(STT.read_text())["words"] if w.get("type") == "word"]
    film = WORK / "_vo_film.raw"
    part = WORK / "_vo_part.raw"
    run(["ffmpeg", "-y", "-v", "error", "-ss", "440", "-t", "40", "-i", str(master),
         "-ac", "1", "-ar", "8000", "-f", "s16le", str(film)])
    run(["ffmpeg", "-y", "-v", "error", "-ss", "40", "-t", "30", "-i", str(PART_WAV),
         "-ac", "1", "-ar", "8000", "-f", "s16le", str(part)])
    fa = np.fromfile(film, dtype=np.int16).astype(np.float32)
    pa = np.fromfile(part, dtype=np.int16).astype(np.float32)
    fa -= fa.mean()
    pa -= pa.mean()
    # Correlate a 4s slice of the part (48-52s, which is 8s into the 40s extract) against the film.
    sl = pa[8 * 8000:12 * 8000]
    sl /= max(np.linalg.norm(sl), 1)
    step = 80
    best_i, best = 0, -1e9
    for i in range(0, len(fa) - len(sl), step):
        seg = fa[i:i + len(sl)]
        score = float(np.dot(seg, sl) / max(np.linalg.norm(seg), 1))
        if score > best:
            best, best_i = score, i
    # part time 48s lands at film 440 + best_i/8000
    part_t = 48.0
    film_t = 440.0 + best_i / 8000
    offset = film_t - part_t  # film = part + offset
    spans = [(459.30, 461.05), (461.05, 462.26)]
    report = {"offset_film_minus_part_s": round(offset, 3), "correlation": round(best, 3), "spans": []}
    for a, b in spans:
        hit = [
            {"text": w["text"], "part_s": round(w["start"], 3), "film_s": round(w["start"] + offset, 3)}
            for w in words
            if w["end"] > (a - offset) and w["start"] < (b - offset)
        ]
        report["spans"].append({"film": [a, b], "words": hit})
        print(f"VO {a:.2f}-{b:.2f}: {' '.join(h['text'] for h in hit)}", flush=True)
    (WORK / "VO_WORDS.json").write_text(json.dumps(report, indent=2) + "\n")
    return report


def frame_diff(v09: Path) -> dict:
    """Mean abs at the brief's sample times, v09 vs v08."""
    times = [462.3, 464.0, 466.0, 468.7]
    out = []
    worst = 0.0
    for t in times:
        a = WORK / f"_d09_{t}.raw"
        b = WORK / f"_d08_{t}.raw"
        for src, dest in ((v09, a), (V08_MASTER, b)):
            start = t - 1.0
            sp.run([
                "ffmpeg", "-y", "-v", "error", "-ss", f"{start:.3f}", "-i", str(src),
                "-vf", "trim=start=1.0:duration=0.05,setpts=PTS-STARTPTS",
                "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", str(dest),
            ], check=True)
        fa = np.fromfile(a, dtype=np.uint8).astype(np.int16)
        fb = np.fromfile(b, dtype=np.uint8).astype(np.int16)
        if fa.size != fb.size or fa.size == 0:
            mean = 999.0
        else:
            mean = float(np.abs(fa - fb).mean())
        worst = max(worst, mean)
        out.append({"t": t, "mean_abs": round(mean, 3)})
        print(f"  diff t={t} mean_abs={mean:.3f}", flush=True)
        a.unlink(missing_ok=True)
        b.unlink(missing_ok=True)
    report = {"samples": out, "worst": round(worst, 3), "limit": 1.0, "pass": worst <= 1.0}
    (WORK / "FRAME_DIFF.json").write_text(json.dumps(report, indent=2) + "\n")
    return report


def evidence(v08, master: Path) -> None:
    ev = WORK / "composite_evidence_v09"
    ev.mkdir(parents=True, exist_ok=True)
    cuts = json.loads((WORK / "cuts_rough_v09.json").read_text())
    by = {c["row"]: c for c in cuts}
    metal = by["10_metal_easy"]
    tin, tout = float(metal["timeline_in"]), float(metal["timeline_out"])
    for pct, name in ((10, "p10"), (25, "p25"), (50, "p50"), (75, "p75"), (90, "p90")):
        grab(master, tin + (tout - tin) * pct / 100, ev / f"p510_{name}.jpg")
    safe = by["11_safe_path"]
    for t in (461.05, 461.5, 462.0, 462.26, 462.3):
        grab(master, t, ev / f"safe_{t:.2f}.jpg".replace(".", "p", 1) if False else ev / f"safe_{str(t).replace('.', '_')}.jpg")
    grab(V08_MASTER, 462.3, ev / "v08_at_462_3.jpg")
    for t in (461.00, 461.09):
        grab(master, t, ev / f"join_{str(t).replace('.', '_')}.jpg")
    # 24fps strip of the 42 plate frames, cropped to the workman and the rod.
    crop = "crop=900:860:520:140"
    start = max(0.0, tin - 1.0)
    rel = tin - start
    span = METAL_N / FPS
    run([
        "ffmpeg", "-y", "-v", "error",
        "-ss", f"{start:.3f}", "-i", str(master),
        "-vf", f"trim=start={rel:.3f}:duration={span:.3f},setpts=PTS-STARTPTS,{crop},fps={FPS}",
        "-frames:v", str(METAL_N), "-an",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
        str(ev / "p510_workman_42f_24fps.mp4"),
    ])
    run([
        "ffmpeg", "-y", "-v", "error",
        "-ss", f"{start:.3f}", "-i", str(master),
        "-vf", f"trim=start={rel:.3f}:duration={span:.3f},setpts=PTS-STARTPTS,{crop},fps={FPS},scale=240:-1,tile=7x6",
        "-frames:v", "1", str(ev / "p510_workman_contact.jpg"),
    ])
    print(f"evidence {ev}", flush=True)


def gates(v08, master: Path) -> dict:
    cuts = WORK / "cuts_rough_v09.json"
    pool = WORK / "pool_rough_v09.json"
    shutil.copy2(v08.V04_POOL, pool)
    polish_json = WORK / "polish_gate_rough_v09.json"
    polish = sp.run(
        [sys.executable, str(OWB_ROOT / "scripts/polish_gate.py"), str(master),
         "--cuts", str(cuts), "--out", str(polish_json)],
        capture_output=True, text=True,
    )
    (WORK / "polish_gate_rough_v09.txt").write_text(polish.stdout + polish.stderr)
    print((polish.stdout or "")[-600:], flush=True)
    pq = WORK / "picture_qa_rough_v09"
    picture = sp.run(
        [sys.executable, str(OWB_ROOT / "scripts/picture_qa.py"), str(master),
         "--cuts", str(cuts), "--pool", str(pool), "--out-dir", str(pq)],
        capture_output=True, text=True,
    )
    (WORK / "picture_qa_rough_v09.txt").write_text(picture.stdout + picture.stderr)
    print((picture.stdout or "")[-600:], flush=True)
    note = {"status": "SKIPPED_NO_BED", "reason": "No new bed. Job brief.", "version": "rough_v09"}
    (WORK / "music_gate_rough_v09.json").write_text(json.dumps(note, indent=2) + "\n")
    (WORK / "music_gate_rough_v09.txt").write_text("SKIPPED_NO_BED\n")
    return {"polish_rc": polish.returncode, "picture_rc": picture.returncode}


def deliver(master: Path, gates_rc: dict, diff: dict) -> None:
    info = json.loads((WORK / "DURATION.json").read_text())
    summary = {
        "version": "rough_v09",
        "job": "J1267",
        "source_master": str(V08_MASTER.parent / "hos_008_rough_v04.mp4"),
        "built_from": "rough v04 e00bb897, same splice as v08",
        "master_sha256": sha256_file(master),
        "durations": info,
        "gates": gates_rc,
        "frame_diff": diff,
        "plate_in_point": json.loads((WORK / "PLATE_INPOINT.json").read_text()),
        "pause": json.loads((WORK / "PAUSE_TRIM_APPLIED.json").read_text()),
        "safe_path_frames": {
            "lead_in": LEAD_N,
            "body_from_existing_asset": SAFE_BODY_N,
            "asset_file_frames": 168,
            "row_frames": SAFE_N,
            "note": (
                "The v08 row holds 157 frames of the 168-frame asset. "
                "29+157=186 keeps the row end and the 12923-frame total. "
                "29+168=197 would cover 11 frames of the next row."
            ),
        },
        "note": "Parked for Chief: graphics + composite. No finished-film PASS. No music bed.",
    }
    if (WORK / "ROD_TRACE.json").exists():
        summary["rod_trace"] = json.loads((WORK / "ROD_TRACE.json").read_text())
    if (WORK / "VO_WORDS.json").exists():
        summary["vo_words"] = json.loads((WORK / "VO_WORDS.json").read_text())
    (WORK / "ROUGH_V09_SUMMARY.json").write_text(json.dumps(summary, indent=2) + "\n")
    names = [
        "hos_008_rough_v09.mp4", "cuts_rough_v09.json", "pool_rough_v09.json",
        "polish_gate_rough_v09.json", "polish_gate_rough_v09.txt",
        "picture_qa_rough_v09.txt", "music_gate_rough_v09.json", "music_gate_rough_v09.txt",
        "ROUGH_V09_SUMMARY.json", "DURATION.json", "PAUSE_TRIM_APPLIED.json",
        "PLATE_INPOINT.json", "ROD_TRACE.json", "VO_WORDS.json", "FRAME_DIFF.json",
    ]
    media = Path(
        "/Users/benjaminoats/YouTube/hos-008-lightning/02_Video-Projects"
        "/008_Lightning-Franklin/07_Edit-Project/_precheck/rough_v09"
    )
    dests = [
        media,
        Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT/HOS-008_Lightning-Franklin_rough_v09",
        Path("/Volumes/data/mac-mini-archive/YouTube/History Of Science/02_Video-Projects/008_Lightning-Franklin/07_Edit-Project/_desk/008/rough_v09"),
    ]
    for dest in dests:
        if dest.name in {f"rough_v0{n}" for n in range(2, 9)}:
            raise RuntimeError(dest)
        dest.mkdir(parents=True, exist_ok=True)
        for name in names:
            src = WORK / name
            if src.exists():
                shutil.copy2(src, dest / name)
        for folder in ("composite_evidence_v09", "picture_qa_rough_v09", "code_graphics_v06"):
            src = WORK / folder
            if not src.exists():
                continue
            target = dest / folder
            if target.exists():
                shutil.rmtree(target)
            shutil.copytree(src, target)
        sums = []
        for p in sorted(dest.rglob("*")):
            if p.is_file() and not p.name.startswith("._") and "picture_qa_rough_v09" not in p.parts:
                rel = p.relative_to(dest)
                sums.append(f"{sha256_file(p)}  {rel}\n")
        (dest / "MEDIA_SHA256SUMS.txt").write_text("".join(sums))
        print(f"delivered {dest}", flush=True)


def commit_evidence() -> None:
    repo = Path("/Users/benjaminoats/YouTube/History Of Science")
    wt = Path("/Volumes/data/mac-mini-archive/tmp-render-scratch/j1263-hos008-wt")
    if not (wt / ".git").exists():
        run(["git", "-C", str(repo), "worktree", "add", "--detach", str(wt),
             "origin/cursor/j1257-hos008-rough-v06"])
    run(["git", "-C", str(wt), "fetch", "origin", "cursor/j1257-hos008-rough-v06"])
    run(["git", "-C", str(wt), "switch", "-C", "cursor/j1257-hos008-rough-v06",
         "origin/cursor/j1257-hos008-rough-v06"])
    edit = wt / "02_Video-Projects/008_Lightning-Franklin/07_Edit-Project"
    shutil.copy2(Path(__file__).resolve(), edit / "_build_rough_v09.py")
    desk = edit / "_desk/008/rough_v09"
    if desk.exists():
        shutil.rmtree(desk)
    desk.mkdir(parents=True)
    skip_suffix = {".mp4", ".mov", ".wav", ".raw"}
    for p in WORK.rglob("*"):
        if not p.is_file() or p.name.startswith("._") or p.name.startswith("_vo") or p.name.startswith("_d"):
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
         "02_Video-Projects/008_Lightning-Franklin/07_Edit-Project/_build_rough_v09.py",
         "02_Video-Projects/008_Lightning-Franklin/07_Edit-Project/_desk/008/rough_v09"])
    status = sp.run(["git", "-C", str(wt), "diff", "--cached", "--quiet"])
    if status.returncode == 0:
        print("nothing to commit", flush=True)
        return
    run(["git", "-C", str(wt), "commit", "-m",
         "hos(008): J1267 rough v09 shorter P5:10 hold and safe-path lead-in for Chief review"])
    run(["git", "-C", str(wt), "push", "origin", "HEAD:cursor/j1257-hos008-rough-v06"])
    sha = sp.check_output(["git", "-C", str(wt), "rev-parse", "--short", "HEAD"], text=True).strip()
    (WORK / "PR_COMMIT.txt").write_text(sha + "\n")
    print(f"pushed evidence {sha}", flush=True)


def main() -> int:
    WORK.mkdir(parents=True, exist_ok=True)
    v08 = load_v08()
    alpha = render_alpha()
    lead = render_leadin()
    safe = build_safe(lead)
    metal = build_metal(v08, alpha)
    row_check(v08, metal)
    (WORK / "phase_row.done").write_text("pass\n")
    master = splice(v08, metal, safe)
    vo_report(master)
    diff = frame_diff(master)
    evidence(v08, master)
    gates_rc = gates(v08, master)
    deliver(master, gates_rc, diff)
    try:
        commit_evidence()
    except Exception:
        import traceback
        traceback.print_exc()
        (WORK / "commit_error.txt").write_text(traceback.format_exc())
    (WORK / "phase_splice.done").write_text(json.dumps({"gates": gates_rc, "diff": diff}) + "\n")
    ok = gates_rc["polish_rc"] == 0 and gates_rc["picture_rc"] == 0 and diff["pass"]
    print("RESULT", "PASS" if ok else "CHECK_FAIL", gates_rc, diff["worst"], flush=True)
    return 0 if ok else 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SystemExit:
        raise
    except Exception:
        import traceback
        traceback.print_exc()
        raise
