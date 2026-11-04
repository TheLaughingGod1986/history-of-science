#!/usr/bin/env python3
"""J1267 h20: HOS 008 rough v11.

The J1273 alpha (sha 53454827) is copied once into code_graphics_v07 and
sha-checked. render_alpha() is not called. v06 and bb821f40 are not touched.

The picture change is the same v08 GOP (keyframe 459.291667 to 463.166667,
93 frames): 42-frame J1273 composite, then a 51-frame SAFE PATH DOWN lead-in
(29-frame fade, 22-frame hold at the opening state). No v08 plate frames sit
in that GOP. From the 463.166667s keyframe the tail is stream-copied.

New rough_v11 folders only. Never write v02-v10. No UAT copy. GBP0.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import subprocess as sp
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1920, 1080, 24
FONT = "/System/Library/Fonts/Supplemental/Didot.ttc"
CREAM = (244, 228, 195, 255)
V08 = Path(
    "/Users/benjaminoats/YouTube/hos-008-lightning/02_Video-Projects"
    "/008_Lightning-Franklin/07_Edit-Project/_precheck/rough_v08/hos_008_rough_v08.mp4"
)
ALPHA_SRC = Path(
    "/Users/benjaminoats/_desk/j1273-candidate-v08/code_graphic_008_p5_10_metal_easy_v08.mov"
)
COMP_SRC = Path("/Users/benjaminoats/_desk/j1273-candidate-v08/composite_v08.mp4")
OFFSETS = Path("/Users/benjaminoats/_desk/j1273-candidate-v08/OFFSETS.json")
ALPHA_SHA = "53454827126be943dc4b11b51c52a32e9131637094dc4ca869a57e2165a68312"
COMP_SHA = "f8453cc78529871ef12a5ce4b1ad84a55f1d3d3759b98d180507b4c09d400ca9"
PART_WAV = Path(
    "/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects"
    "/008_Lightning-Franklin/02_Voiceover/hos_008_part05_the_rod_on_every_roof_v01b.wav"
)
STT = Path(
    "/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects"
    "/008_Lightning-Franklin/02_Voiceover/stt"
    "/hos_008_part05_the_rod_on_every_roof_v01b/stt_raw.json"
)
V09_CUTS = Path("/private/tmp/j1267-hos008-rough-v09/cuts_rough_v09.json")
V09_POOL = Path("/private/tmp/j1267-hos008-rough-v09/pool_rough_v09.json")
V09_PAUSE = Path("/private/tmp/j1267-hos008-rough-v09/PAUSE_TRIM_APPLIED.json")
BUILD_V08 = Path(
    "/Volumes/data/mac-mini-archive/tmp-render-scratch/j1263-hos008-rough-v08/build_v08.py"
)
OWB_ROOT = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
WORK = Path("/private/tmp/j1267-hos008-rough-v11")
HEAD_N, PLATE_N, FADE_N, HOLD_N = 10996, 42, 29, 22
LEAD_N = FADE_N + HOLD_N
KEEP_N = 0
TAIL_N = 1834
GOP_N = PLATE_N + LEAD_N
GOP_START = 459.291667  # v08 keyframe, film time of plate frame 0
TAIL_START = 463.166667  # next v08 keyframe
ROW0 = 10996  # packet index of the plate's first frame
BODY_N = 135  # v08 card frames from the 463.167s keyframe to 468.796s
PLATE_FLASH_0 = 11067  # v10 frames that still showed the old plate
PLATE_FLASH_1 = 11088

PRECHECK = Path(
    "/Users/benjaminoats/YouTube/hos-008-lightning/02_Video-Projects"
    "/008_Lightning-Franklin/07_Edit-Project/_precheck/rough_v11"
)
NAS = Path(
    "/Volumes/data/mac-mini-archive/YouTube/History Of Science/02_Video-Projects"
    "/008_Lightning-Franklin/07_Edit-Project/_desk/008/rough_v11"
)


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def run(cmd: list[str]) -> None:
    print(" ", " ".join(cmd[:12]), "...", flush=True)
    sp.run(cmd, check=True)


def copy_verified(source: Path, target: Path) -> None:
    """Copy only. Conflicting destinations are never overwritten."""
    if source.is_dir():
        target.mkdir(parents=True, exist_ok=True)
        for item in sorted(source.iterdir()):
            if item.name.startswith("._"):
                continue
            copy_verified(item, target / item.name)
        return
    if target.exists():
        if not target.is_file() or sha256_file(source) != sha256_file(target):
            raise FileExistsError(f"Conflicting delivery: {target}")
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    with source.open("rb") as src, target.open("xb") as dst:
        shutil.copyfileobj(src, dst)
    if sha256_file(source) != sha256_file(target):
        raise RuntimeError(f"Delivery hash mismatch: {target}")


def ease(t, a, b):
    if b <= a:
        return 1.0 if t >= a else 0.0
    p = max(0.0, min(1.0, (t - a) / (b - a)))
    return p * p * (3 - 2 * p)


def install_alpha() -> Path:
    if sha256_file(ALPHA_SRC) != ALPHA_SHA:
        raise RuntimeError("J1273 alpha sha is not 53454827")
    if sha256_file(COMP_SRC) != COMP_SHA:
        raise RuntimeError("J1273 composite sha is not f8453cc7")
    dest = WORK / "code_graphics_v07" / "code_graphic_008_p5_10_metal_easy.mov"
    dest.parent.mkdir(parents=True, exist_ok=True)
    copy_verified(ALPHA_SRC, dest)
    if sha256_file(dest) != ALPHA_SHA:
        raise RuntimeError("v07 alpha sha changed during copy")
    if (WORK / "code_graphics_v06").exists():
        raise RuntimeError("refusing to keep a v06 alpha folder in the v11 work dir")
    print(f"alpha v07 {dest} sha={ALPHA_SHA[:12]}", flush=True)
    return dest


def render_leadin() -> Path:
    dest = WORK / "code_graphics_v07" / "leadin_11_safe_path.mp4"
    if dest.exists() and dest.stat().st_size > 1000:
        return dest
    bg_rng = np.random.default_rng(8329)
    y, x = np.mgrid[:H, :W]
    v = np.clip(((x - W / 2) / (W / 2)) ** 2 + ((y - H / 2) / (H / 2)) ** 2, 0, 1.4)
    noise = bg_rng.normal(0, 1.2, (H, W))
    a = np.zeros((H, W, 3))
    for c, base in enumerate((136, 100, 66)):
        a[:, :, c] = base - 42 * v + noise
    bg = Image.fromarray(np.uint8(np.clip(a, 0, 255))).convert("RGBA")
    font = ImageFont.truetype(FONT, 66, index=1)
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
        alpha = ease(t, 0.04, (FADE_N - 1) / FPS)
        layer = Image.new("RGBA", (W, H))
        d = ImageDraw.Draw(layer)
        fill = (*CREAM[:3], round(255 * alpha))
        sc = (36, 22, 12, round(230 * alpha))
        d.text((W / 2, 150), "SAFE PATH DOWN", font=font, fill=fill, anchor="mm",
               stroke_width=6, stroke_fill=sc)
        frame = Image.alpha_composite(bg, layer).convert("RGB")
        raw.stdin.write(frame.tobytes())
    raw.stdin.close()
    if raw.wait() != 0:
        raise RuntimeError("lead-in encode failed")
    return dest


def split_v08() -> tuple[Path, Path, Path]:
    seg = WORK / "_seg"
    seg.mkdir(parents=True, exist_ok=True)
    head, gop, tail = seg / "head.mp4", seg / "gop.mp4", seg / "tail.mp4"
    if not (head.exists() and gop.exists() and tail.exists()):
        run([
            "ffmpeg", "-y", "-v", "error", "-i", str(V08), "-an", "-c", "copy",
            "-f", "segment", "-segment_frames", f"{HEAD_N},{HEAD_N + GOP_N}",
            "-reset_timestamps", "1", str(seg / "part%02d.mp4"),
        ])
        (seg / "part00.mp4").replace(head)
        (seg / "part01.mp4").replace(gop)
        (seg / "part02.mp4").replace(tail)
    for path, n in ((head, HEAD_N), (gop, GOP_N), (tail, TAIL_N)):
        got = packet_count(path)
        if got != n:
            raise RuntimeError(f"{path.name} packets {got} != {n}")
    return head, gop, tail


def packet_count(path: Path) -> int:
    raw = sp.check_output(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_packets",
         "-show_entries", "stream=nb_read_packets", "-of", "csv=p=0", str(path)],
        text=True,
    )
    return int(raw.strip())


def encode_x264(src_filter_cmd: list[str], dest: Path, frames: int) -> None:
    """One closed-GOP encode. crf 8 keeps the plate within 1.0 of the composite."""
    if dest.exists():
        dest.unlink()
    run([
        *src_filter_cmd,
        "-frames:v", str(frames), "-an",
        "-c:v", "libx264", "-preset", "veryfast", "-profile:v", "high", "-level", "4.0",
        "-pix_fmt", "yuv420p", "-r", "24", "-video_track_timescale", "12288",
        "-x264-params", f"keyint={frames}:min-keyint={frames}:scenecut=0:open-gop=0",
        "-crf", "8", str(dest),
    ])
    got = packet_count(dest)
    if got != frames:
        raise RuntimeError(f"{dest.name} packets {got} != {frames}")


def build_middle(leadin: Path) -> tuple[Path, Path]:
    plate = WORK / "_seg" / "plate.mp4"
    rest = WORK / "_seg" / "rest.mp4"
    if not plate.exists():
        encode_x264(
            ["ffmpeg", "-y", "-v", "error", "-i", str(COMP_SRC)],
            plate, PLATE_N,
        )
    if not rest.exists():
        encode_x264(
            ["ffmpeg", "-y", "-v", "error", "-i", str(leadin)],
            rest, LEAD_N,
        )
    return plate, rest


def splice(head: Path, plate: Path, rest: Path, tail: Path) -> Path:
    final = WORK / "hos_008_rough_v11.mp4"
    if final.exists() and packet_count(final) == 12923:
        print("splice already complete", flush=True)
        return final
    lst = WORK / "_seg" / "concat.txt"
    lines = []
    for p in (head, plate, rest, tail):
        lines.append(f"file '{p}'")
    lst.write_text("\n".join(lines) + "\n")
    video = WORK / "_seg" / "video.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(video)])
    if packet_count(video) != 12923:
        raise RuntimeError(f"concat packets {packet_count(video)} != 12923")
    # v08's video track starts at 0.125s. The concat starts at 0. Shift once.
    run([
        "ffmpeg", "-y", "-v", "error", "-itsoffset", "0.125", "-i", str(video), "-i", str(V08),
        "-map", "0:v:0", "-map", "1:a:0", "-c", "copy", "-movflags", "+faststart",
        str(final),
    ])
    if packet_count(final) != 12923:
        raise RuntimeError(f"mux packets {packet_count(final)} != 12923")
    return final


def probe_durations(path: Path) -> dict:
    d = json.loads(sp.check_output(
        ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)],
        text=True,
    ))
    out = {"format": float(d["format"]["duration"]), "nb_packets": packet_count(path)}
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


def packets(path: Path) -> list[float]:
    raw = sp.check_output(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "packet=pts_time", "-of", "csv=p=0", str(path)],
        text=True,
    )
    return sorted(float(line) for line in raw.splitlines() if line.strip())


def decode_rgb(path: Path, frame_index: int) -> np.ndarray:
    """Decode one frame by index. Seek to the GOP keyframe when it is the tail."""
    if frame_index >= ROW0 + PLATE_N + LEAD_N + KEEP_N:
        ss = TAIL_START
        n = frame_index - (ROW0 + PLATE_N + LEAD_N + KEEP_N)
        cmd = [
            "ffmpeg", "-v", "error", "-ss", f"{ss:.6f}", "-i", str(path),
            "-vf", f"select=eq(n\\,{n})", "-frames:v", "1",
            "-f", "rawvideo", "-pix_fmt", "rgb24", "pipe:1",
        ]
    elif frame_index >= ROW0:
        ss = GOP_START
        n = frame_index - ROW0
        cmd = [
            "ffmpeg", "-v", "error", "-ss", f"{ss:.6f}", "-i", str(path),
            "-vf", f"select=eq(n\\,{n})", "-frames:v", "1",
            "-f", "rawvideo", "-pix_fmt", "rgb24", "pipe:1",
        ]
    else:
        cmd = [
            "ffmpeg", "-v", "error", "-i", str(path),
            "-vf", f"select=eq(n\\,{frame_index})", "-frames:v", "1",
            "-f", "rawvideo", "-pix_fmt", "rgb24", "pipe:1",
        ]
    raw = sp.check_output(cmd)
    arr = np.frombuffer(raw, dtype=np.uint8)
    if arr.size != W * H * 3:
        raise RuntimeError(f"frame {frame_index} of {path.name} is {arr.size} bytes")
    return arr


def mean_abs(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.abs(a.astype(np.int16) - b.astype(np.int16)).mean())


def nearest_index(pts: list[float], t: float) -> tuple[int, float]:
    i = min(range(len(pts)), key=lambda k: abs(pts[k] - t))
    return i, pts[i]


def composite_match(master: Path) -> dict:
    samples = []
    worst = 0.0
    for n in (0, 5, 11, 21, 32, 38, 41):
        a = decode_rgb(master, ROW0 + n)
        b = decode_rgb(COMP_SRC, n)
        m = mean_abs(a, b)
        worst = max(worst, m)
        samples.append({
            "row_frame": n,
            "master_frame_index": ROW0 + n,
            "plate_source_frame": 109 + n,
            "mean_abs": round(m, 3),
        })
        print(f"  composite frame {n} mean_abs={m:.3f}", flush=True)
    report = {
        "composite_sha256": COMP_SHA,
        "alpha_sha256": ALPHA_SHA,
        "limit": 1.0,
        "worst": round(worst, 3),
        "pass": worst <= 1.0,
        "samples": samples,
    }
    (WORK / "COMPOSITE_MATCH.json").write_text(json.dumps(report, indent=2) + "\n")
    return report


def frame_diff(master: Path) -> dict:
    v11_pts = packets(master)
    v08_pts = packets(V08)
    samples = []
    worst = 0.0
    for t in (463.2, 464.0, 466.0, 468.7):
        i11, p11 = nearest_index(v11_pts, t)
        i08, p08 = nearest_index(v08_pts, t)
        a = decode_rgb(master, i11)
        b = decode_rgb(V08, i08)
        m = mean_abs(a, b)
        worst = max(worst, m)
        samples.append({
            "t": t,
            "mean_abs": round(m, 3),
            "v11_frame_index": i11,
            "v11_pts": round(p11, 6),
            "v08_frame_index": i08,
            "v08_pts": round(p08, 6),
            "same_index": i11 == i08,
        })
        print(f"  diff t={t} idx {i11}/{i08} mean_abs={m:.3f}", flush=True)
    report = {
        "samples": samples,
        "worst": round(worst, 3),
        "limit": 1.0,
        "pass": worst <= 1.0,
        "body_frames": BODY_N,
        "note": (
            "Body samples are on the tail keyframe GOP, stream-copied from v08. "
            "The card body is 135 frames, from 463.167s. A miss is a source "
            "frame shift when the indexes differ, and a re-encode when they match."
        ),
    }
    (WORK / "FRAME_DIFF.json").write_text(json.dumps(report, indent=2) + "\n")
    return report


def plate_gone(master: Path) -> dict:
    """Frames 11067-11088 must no longer be the v08 metal plate."""
    samples = []
    worst_low = 1e9
    for i in range(PLATE_FLASH_0, PLATE_FLASH_1 + 1):
        m = mean_abs(decode_rgb(master, i), decode_rgb(V08, i))
        worst_low = min(worst_low, m)
        samples.append({"frame": i, "mean_abs": round(m, 3)})
        print(f"  plate-gone {i} mean_abs={m:.3f}", flush=True)
    report = {
        "frames": [PLATE_FLASH_0, PLATE_FLASH_1],
        "min_mean_abs": round(worst_low, 3),
        "need_above": 1.0,
        "pass": worst_low > 1.0,
        "samples": samples,
    }
    (WORK / "PLATE_GONE.json").write_text(json.dumps(report, indent=2) + "\n")
    return report


def join_check(master: Path) -> dict:
    last_i = ROW0 + GOP_N - 1
    card_i = ROW0 + GOP_N
    last = decode_rgb(master, last_i)
    card = decode_rgb(master, card_i)
    m = mean_abs(last, card)
    ev = WORK / "composite_evidence_v11"
    ev.mkdir(parents=True, exist_ok=True)
    Image.fromarray(last.reshape(H, W, 3)).save(ev / "join_last_leadin.jpg", quality=90)
    Image.fromarray(card.reshape(H, W, 3)).save(ev / "join_first_card.jpg", quality=90)
    report = {
        "last_leadin_frame": last_i,
        "first_card_frame": card_i,
        "first_card_time_s": TAIL_START,
        "mean_abs": round(m, 3),
        "limit": 1.0,
        "pass": m <= 1.0,
        "note": (
            "h20: report this number with both frames when the opening-state "
            "hold does not match the card's first stream-copied frame."
        ),
    }
    (WORK / "JOIN.json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"  join {last_i}->{card_i} mean_abs={m:.3f}", flush=True)
    return report


def audio_match(master: Path) -> dict:
    def stream_md5(path: Path) -> str:
        raw = sp.check_output(
            ["ffmpeg", "-v", "error", "-i", str(path), "-map", "0:a:0", "-f", "streamhash", "-hash", "md5", "-"],
            text=True,
        )
        return raw.strip()
    a = stream_md5(master)
    b = stream_md5(V08)
    report = {"v11": a, "v08": b, "pass": a == b and bool(a)}
    (WORK / "AUDIO_MATCH.json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"  audio match {report['pass']}", flush=True)
    return report


def tip_check(master: Path) -> dict:
    spec = importlib.util.spec_from_file_location("build_v08", BUILD_V08)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    offsets = json.loads(OFFSETS.read_text())
    samples = []
    worst = 0.0
    for row in offsets["samples"]:
        n = int(row["row_frame"])
        rgb = decode_rgb(master, ROW0 + n)
        gray = np.array(Image.fromarray(rgb.reshape(H, W, 3)).convert("L"), dtype="float32")
        trace_x = float(row["tip"]["trace_x"])
        meas = mod.tip_offset(gray, trace_x)
        if meas is None:
            raise RuntimeError(f"tip not found at row frame {n}")
        worst = max(worst, abs(meas["offset_px"]))
        samples.append({
            "pct": row["pct"],
            "row_frame": n,
            "master_frame_index": ROW0 + n,
            "j1273_offset_px": row["tip"]["offset_px"],
            **meas,
        })
        print(f"  tip p{row['pct']} {meas['offset_px']:+.1f}px", flush=True)
    limit = 19.2
    report = {
        "limit_px": limit,
        "worst_abs_px": round(worst, 1),
        "pass": worst <= limit,
        "samples": samples,
        "alpha_sha256": ALPHA_SHA,
    }
    (WORK / "ROD_TRACE.json").write_text(json.dumps(report, indent=2) + "\n")
    return report


def vo_report(master: Path) -> dict:
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
    sl = pa[8 * 8000:12 * 8000]
    sl /= max(np.linalg.norm(sl), 1)
    best_i, best = 0, -1e9
    for i in range(0, len(fa) - len(sl), 80):
        seg = fa[i:i + len(sl)]
        score = float(np.dot(seg, sl) / max(np.linalg.norm(seg), 1))
        if score > best:
            best, best_i = score, i
    offset = 440.0 + best_i / 8000 - 48.0
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


def grab(master: Path, t: float, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    start = max(0.0, t - 1.0)
    rel = t - start
    run([
        "ffmpeg", "-y", "-v", "error", "-ss", f"{start:.3f}", "-i", str(master),
        "-vf", f"trim=start={rel:.3f}:duration=0.05,setpts=PTS-STARTPTS",
        "-frames:v", "1", "-q:v", "2", str(dest),
    ])


def evidence(master: Path) -> None:
    ev = WORK / "composite_evidence_v11"
    ev.mkdir(parents=True, exist_ok=True)
    tin = GOP_START
    for pct, name in ((10, "p10"), (25, "p25"), (50, "p50"), (75, "p75"), (90, "p90")):
        grab(master, tin + (PLATE_N / FPS) * pct / 100, ev / f"p510_{name}.jpg")
    for t in (461.05, 461.5, 462.0, 462.26, 462.3, 463.2):
        grab(master, t, ev / f"safe_{str(t).replace('.', '_')}.jpg")
    grab(V08, 463.2, ev / "v08_at_463_2.jpg")
    for t in (461.00, 461.09):
        grab(master, t, ev / f"join_{str(t).replace('.', '_')}.jpg")
    crop = "crop=900:860:520:140"
    run([
        "ffmpeg", "-y", "-v", "error", "-ss", f"{GOP_START:.6f}", "-i", str(master),
        "-vf", f"trim=end_frame={PLATE_N},setpts=PTS-STARTPTS,{crop},fps={FPS}",
        "-frames:v", str(PLATE_N), "-an",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
        str(ev / "p510_workman_42f_24fps.mp4"),
    ])
    run([
        "ffmpeg", "-y", "-v", "error", "-ss", f"{GOP_START:.6f}", "-i", str(master),
        "-vf", f"trim=end_frame={PLATE_N},setpts=PTS-STARTPTS,{crop},fps={FPS},scale=240:-1,tile=7x6",
        "-frames:v", "1", str(ev / "p510_workman_contact.jpg"),
    ])
    # The 22 frames v10 still showed as the old plate (indexes 11067-11088).
    run([
        "ffmpeg", "-y", "-v", "error", "-ss", f"{GOP_START:.6f}", "-i", str(master),
        "-vf", f"trim=start_frame={PLATE_N + FADE_N}:end_frame={GOP_N},setpts=PTS-STARTPTS,scale=320:-1,tile=6x4",
        "-frames:v", "1", str(ev / "leadin_hold_11067_11088.jpg"),
    ])


def write_cuts(plate: Path, leadin: Path) -> None:
    cuts = json.loads(V09_CUTS.read_text())
    for c in cuts:
        if c["row"] == "10_metal_easy":
            c["source"] = "composite_v08.mp4"
            c["source_path"] = str(COMP_SRC)
            c["source_sha256"] = COMP_SHA
            c["disposition"] = "J1267 v11 plate frames 109-150, J1273 alpha 53454827, no render_alpha"
            c["framing"] = {"offset": 109 / FPS, "source_frames": "109-150"}
        elif c["row"] == "11_safe_path":
            c["source"] = leadin.name
            c["source_path"] = str(leadin)
            c["source_sha256"] = sha256_file(leadin)
            c["disposition"] = (
                "J1267 v11 51-frame SAFE PATH DOWN lead-in (29 fade + 22 hold), "
                "then 135 v08 card frames stream-copied from 463.167s"
            )
    (WORK / "cuts_rough_v11.json").write_text(json.dumps(cuts, indent=2) + "\n")
    copy_verified(V09_POOL, WORK / "pool_rough_v11.json")
    pause = json.loads(V09_PAUSE.read_text())
    pause["inherited"] = "v08 bitstream already contains this pause trim; v11 does not re-trim"
    (WORK / "PAUSE_TRIM_APPLIED.json").write_text(json.dumps(pause, indent=2) + "\n")
    note = {
        "plate": "06_rod_fitting_t1 frames 109-150 via J1273 composite f8453cc7",
        "alpha": str(WORK / "code_graphics_v07" / "code_graphic_008_p5_10_metal_easy.mov"),
        "alpha_sha256": ALPHA_SHA,
        "composite_sha256": COMP_SHA,
        "render_alpha_called": False,
        "plate_encode": str(plate),
        "plate_encode_sha256": sha256_file(plate),
        "row_start_s": GOP_START,
        "frames": PLATE_N,
        "master_frame_index_0": ROW0,
    }
    (WORK / "PLATE_INPOINT.json").write_text(json.dumps(note, indent=2) + "\n")


def gates(master: Path) -> dict:
    cuts = WORK / "cuts_rough_v11.json"
    pool = WORK / "pool_rough_v11.json"
    polish_json = WORK / "polish_gate_rough_v11.json"
    polish = sp.run(
        [sys.executable, str(OWB_ROOT / "scripts/polish_gate.py"), str(master),
         "--cuts", str(cuts), "--out", str(polish_json)],
        capture_output=True, text=True,
    )
    (WORK / "polish_gate_rough_v11.txt").write_text(polish.stdout + polish.stderr)
    print((polish.stdout or "")[-500:], flush=True)
    pq = WORK / "picture_qa_rough_v11"
    picture = sp.run(
        [sys.executable, str(OWB_ROOT / "scripts/picture_qa.py"), str(master),
         "--cuts", str(cuts), "--pool", str(pool), "--out-dir", str(pq)],
        capture_output=True, text=True,
    )
    (WORK / "picture_qa_rough_v11.txt").write_text(picture.stdout + picture.stderr)
    print((picture.stdout or "")[-500:], flush=True)
    note = {"status": "SKIPPED_NO_BED", "reason": "No new bed. Job brief.", "version": "rough_v11"}
    (WORK / "music_gate_rough_v11.json").write_text(json.dumps(note, indent=2) + "\n")
    (WORK / "music_gate_rough_v11.txt").write_text("SKIPPED_NO_BED\n")
    return {"polish_rc": polish.returncode, "picture_rc": picture.returncode}


def check_note(info, comp, diff, tip, gates_rc, gone, join, audio) -> None:
    text = f"""# J1267 rough v11

Chief h20. Built from rough v08 by replacing one GOP. J1273 alpha {ALPHA_SHA[:12]} copied into code_graphics_v07. render_alpha() was not called. GBP0. No UAT copy.

## Durations
format {info.get('format')} video {info.get('video')} start {info.get('video_start')} frames {info.get('nb_packets')} A/V end offset {info.get('av_end_offset')}

## Composite vs f8453cc7
worst mean abs {comp['worst']} limit 1.0 pass {comp['pass']}

## Frame diff vs v08 at 463.2/464/466/468.7
worst {diff['worst']} limit 1.0 pass {diff['pass']}
indexes: {[(s['t'], s['v11_frame_index'], s['v08_frame_index']) for s in diff['samples']]}

## Old plate gone (frames 11067-11088)
min mean abs {gone['min_mean_abs']} need above 1.0 pass {gone['pass']}

## Join last lead-in vs first card at 463.167s
mean abs {join['mean_abs']} limit 1.0 pass {join['pass']}
frames {join['last_leadin_frame']} -> {join['first_card_frame']}

## Tip
worst {tip['worst_abs_px']} px limit 19.2 pass {tip['pass']}

## Audio
streamhash match {audio['pass']}

## Gates
polish_rc {gates_rc['polish_rc']} picture_rc {gates_rc['picture_rc']}

## Safe path
51-frame lead-in (29 fade + 22 hold) plus 135 v08 card frames. 51+135=186. Total frames 12923.
Frames 11067-11088 are the lead-in hold, not the old plate. From the 463.166667s keyframe the packets are stream-copied from v08.
"""
    (WORK / "CHECK_NOTE.md").write_text(text)


def summary(master, info, comp, diff, tip, gates_rc, gone, join, audio) -> None:
    body = {
        "version": "rough_v11",
        "job": "J1267",
        "ruling": "Chief h20",
        "built_from": "rough v08 stream copy, one GOP replaced",
        "master_sha256": sha256_file(master),
        "alpha_sha256": ALPHA_SHA,
        "composite_sha256": COMP_SHA,
        "render_alpha_called": False,
        "durations": info,
        "composite_match": {"worst": comp["worst"], "pass": comp["pass"]},
        "frame_diff": {"worst": diff["worst"], "pass": diff["pass"], "samples": diff["samples"]},
        "plate_gone": {"min_mean_abs": gone["min_mean_abs"], "pass": gone["pass"]},
        "join": join,
        "tip": {"worst_abs_px": tip["worst_abs_px"], "pass": tip["pass"]},
        "audio_match": audio["pass"],
        "gates": gates_rc,
        "safe_path_frames": {
            "lead_in": LEAD_N,
            "fade": FADE_N,
            "hold": HOLD_N,
            "body_from_v08": BODY_N,
            "row_frames": LEAD_N + BODY_N,
        },
        "note": "Parked for Chief. No finished-film PASS. No UAT. No upload. GBP0.",
    }
    (WORK / "ROUGH_V11_SUMMARY.json").write_text(json.dumps(body, indent=2) + "\n")


def deliver(master: Path) -> None:
    names = [
        "hos_008_rough_v11.mp4", "cuts_rough_v11.json", "pool_rough_v11.json",
        "polish_gate_rough_v11.json", "polish_gate_rough_v11.txt",
        "picture_qa_rough_v11.txt", "music_gate_rough_v11.json", "music_gate_rough_v11.txt",
        "ROUGH_V11_SUMMARY.json", "DURATION.json", "PAUSE_TRIM_APPLIED.json",
        "PLATE_INPOINT.json", "ROD_TRACE.json", "VO_WORDS.json", "FRAME_DIFF.json",
        "COMPOSITE_MATCH.json", "PLATE_GONE.json", "JOIN.json", "AUDIO_MATCH.json",
        "CHECK_NOTE.md",
    ]
    forbidden = {f"rough_v0{n}" for n in range(2, 10)} | {"rough_v10"}
    for dest in (PRECHECK, NAS):
        if dest.name in forbidden:
            raise RuntimeError(dest)
        for name in names:
            src = WORK / name
            if src.exists():
                copy_verified(src, dest / name)
        for folder in ("composite_evidence_v11", "picture_qa_rough_v11", "code_graphics_v07"):
            src = WORK / folder
            if src.exists():
                copy_verified(src, dest / folder)
        sums = []
        for p in sorted(dest.rglob("*")):
            if p.is_file() and not p.name.startswith("._") and "picture_qa_rough_v11" not in p.parts and p.name != "MEDIA_SHA256SUMS.txt":
                sums.append(f"{sha256_file(p)}  {p.relative_to(dest)}\n")
        manifest = WORK / "MEDIA_SHA256SUMS.txt"
        manifest.write_text("".join(sums))
        copy_verified(manifest, dest / "MEDIA_SHA256SUMS.txt")
        print(f"delivered {dest}", flush=True)


def commit_evidence() -> None:
    repo = "/Users/benjaminoats/YouTube/History Of Science"
    run(["git", "-C", repo, "fetch", "origin", "cursor/j1257-hos008-rough-v06"])
    wt = Path("/Volumes/data/mac-mini-archive/tmp-render-scratch/j1267-pr385-v11-wt")
    if wt.exists():
        raise RuntimeError(f"worktree already exists: {wt}")
    run(["git", "-C", repo, "worktree", "add", "--detach", str(wt), "origin/cursor/j1257-hos008-rough-v06"])
    dirty = sp.check_output(["git", "-C", str(wt), "status", "--porcelain"], text=True)
    if dirty.strip():
        raise RuntimeError("Evidence commit requires a clean worktree")
    edit = wt / "02_Video-Projects/008_Lightning-Franklin/07_Edit-Project"
    desk = edit / "_desk/008/rough_v11"
    if desk.exists():
        raise RuntimeError(f"refusing to write into existing {desk}")
    copy_verified(Path(__file__).resolve(), edit / "_build_rough_v11.py")
    skip_suffix = {".mp4", ".mov", ".wav", ".raw", ".png"}
    for p in WORK.rglob("*"):
        if not p.is_file() or p.name.startswith("._") or p.name.startswith("_"):
            continue
        if p.suffix.lower() in skip_suffix or "_seg" in p.parts or "__pycache__" in p.parts:
            continue
        rel = p.relative_to(WORK)
        copy_verified(p, desk / rel)
    run(["git", "-C", str(wt), "add", "-f",
         "02_Video-Projects/008_Lightning-Franklin/07_Edit-Project/_build_rough_v11.py",
         "02_Video-Projects/008_Lightning-Franklin/07_Edit-Project/_desk/008/rough_v11"])
    status = sp.run(["git", "-C", str(wt), "diff", "--cached", "--quiet"])
    if status.returncode == 0:
        print("nothing to commit", flush=True)
        return
    run(["git", "-C", str(wt), "commit", "-m",
         "hos(008): J1267 rough v11 51-frame safe-path lead-in, old plate flash removed, for Chief review"])
    run(["git", "-C", str(wt), "push", "origin", "HEAD:cursor/j1257-hos008-rough-v06"])
    sha = sp.check_output(["git", "-C", str(wt), "rev-parse", "--short", "HEAD"], text=True).strip()
    (WORK / "PR_COMMIT.txt").write_text(sha + "\n")
    print(f"pushed evidence {sha}", flush=True)


def main() -> int:
    WORK.mkdir(parents=True, exist_ok=True)
    install_alpha()
    lead = render_leadin()
    head, _gop, tail = split_v08()
    plate, rest = build_middle(lead)
    master = splice(head, plate, rest, tail)
    info = probe_durations(master)
    (WORK / "DURATION.json").write_text(json.dumps(info, indent=2) + "\n")
    print("DURATIONS", json.dumps(info), flush=True)
    if info["nb_packets"] != 12923:
        raise RuntimeError("frame count")
    if abs(info.get("video_start", 9) - 0.125) > 0.002:
        raise RuntimeError(f"video_start {info.get('video_start')}")
    comp = composite_match(master)
    diff = frame_diff(master)
    gone = plate_gone(master)
    join = join_check(master)
    tip = tip_check(master)
    audio = audio_match(master)
    vo_report(master)
    write_cuts(plate, lead)
    evidence(master)
    gates_rc = gates(master)
    check_note(info, comp, diff, tip, gates_rc, gone, join, audio)
    summary(master, info, comp, diff, tip, gates_rc, gone, join, audio)
    ok = (
        comp["pass"] and diff["pass"] and tip["pass"] and gone["pass"] and audio["pass"]
        and gates_rc["polish_rc"] == 0 and gates_rc["picture_rc"] == 0
        and info["nb_packets"] == 12923
        and abs(info["format"] - 539.626) < 0.05
        and abs(info["video"] - 539.500) < 0.05
        and info.get("av_end_offset", 9) <= (1 / FPS) + 0.001
    )
    if ok:
        deliver(master)
        try:
            commit_evidence()
        except Exception:
            import traceback
            traceback.print_exc()
            (WORK / "commit_error.txt").write_text(traceback.format_exc())
    (WORK / "phase_splice.done").write_text(json.dumps({
        "ok": ok, "gates": gates_rc, "diff": diff["worst"], "comp": comp["worst"],
        "plate_gone": gone["min_mean_abs"], "join": join["mean_abs"], "join_pass": join["pass"],
    }) + "\n")
    print("RESULT", "PASS" if ok else "CHECK_FAIL", "join", join["mean_abs"], flush=True)
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
