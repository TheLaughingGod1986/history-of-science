#!/usr/bin/env python3
"""J1267 h21: HOS 008 rough v12.

One title source: the SAFE PATH DOWN pixels already on the v08 card at full
opacity (frame 11114, 464.208 s). That is the card's own title, not a new
drawing. The 51-frame lead-in fades that title onto the card's opening field.
The card's first GOP (157 frames, 463.167-469.708 s) is re-encoded once, with
that same title box pasted until 464.375 s so the 462.25-464.4 s check stays
at full. From 469.708 s the tail is stream-copied.

New rough_v12 folders only. Never write v02-v11. No UAT. GBP0.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import subprocess as sp
import sys
import traceback
from pathlib import Path

import numpy as np
from PIL import Image

W, H, FPS = 1920, 1080, 24
TX0, TX1, TY0, TY1 = 640, 1280, 115, 182
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
V11_HEAD = Path("/private/tmp/j1267-hos008-rough-v11/_seg/head.mp4")
V11_TAIL = Path("/private/tmp/j1267-hos008-rough-v11/_seg/tail.mp4")
V11_CUTS = Path("/private/tmp/j1267-hos008-rough-v11/cuts_rough_v11.json")
V11_POOL = Path("/private/tmp/j1267-hos008-rough-v11/pool_rough_v11.json")
V11_PAUSE = Path("/private/tmp/j1267-hos008-rough-v11/PAUSE_TRIM_APPLIED.json")
BUILD_V08 = Path(
    "/Volumes/data/mac-mini-archive/tmp-render-scratch/j1263-hos008-rough-v08/build_v08.py"
)
OWB_ROOT = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
WORK = Path("/Volumes/data/mac-mini-archive/tmp-render-scratch/j1267-hos008-rough-v12")
WT = Path("/Volumes/data/mac-mini-archive/tmp-render-scratch/j1267-pr385-v12-wt")
REPO = Path("/Users/benjaminoats/YouTube/History Of Science")

HEAD_N, PLATE_N, FADE_N, HOLD_N, CARD_N = 10996, 42, 29, 22, 157
LEAD_N = FADE_N + HOLD_N
MID_N = PLATE_N + LEAD_N + CARD_N  # 250
TAIL_N = 12923 - HEAD_N - MID_N  # 1677
ROW0 = 10996
GOP_START = 459.291667
CARD_START = 463.166667
TAIL_START = 469.708333
# Card-relative frame whose title box is the full v08 title (pts 464.208333).
REF_CARD = 25
# Last card frame still inside the 464.4 s check (pts 464.375).
PASTE_LAST = 29
FRAME_BYTES = W * H * 3

PRECHECK = Path(
    "/Users/benjaminoats/YouTube/hos-008-lightning/02_Video-Projects"
    "/008_Lightning-Franklin/07_Edit-Project/_precheck/rough_v12"
)
NAS = Path(
    "/Volumes/data/mac-mini-archive/YouTube/History Of Science/02_Video-Projects"
    "/008_Lightning-Franklin/07_Edit-Project/_desk/008/rough_v12"
)


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def run(cmd: list[str]) -> None:
    print(" ", " ".join(cmd[:14]), "...", flush=True)
    sp.run(cmd, check=True)


def git(args: list[str]) -> None:
    run(["git", "-c", f"safe.directory={WT}", "-c", f"safe.directory={REPO}", *args])


def copy_verified(source: Path, target: Path) -> None:
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


def ease(i: int) -> float:
    if FADE_N <= 1:
        return 1.0
    p = max(0.0, min(1.0, i / (FADE_N - 1)))
    return p * p * (3 - 2 * p)


def packet_count(path: Path) -> int:
    raw = sp.check_output(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_packets",
         "-show_entries", "stream=nb_read_packets", "-of", "csv=p=0", str(path)],
        text=True,
    )
    return int(raw.strip())


def install_alpha() -> None:
    if sha256_file(ALPHA_SRC) != ALPHA_SHA:
        raise RuntimeError("J1273 alpha sha is not 53454827")
    if sha256_file(COMP_SRC) != COMP_SHA:
        raise RuntimeError("J1273 composite sha is not f8453cc7")
    dest = WORK / "code_graphics_v07" / "code_graphic_008_p5_10_metal_easy.mov"
    dest.parent.mkdir(parents=True, exist_ok=True)
    copy_verified(ALPHA_SRC, dest)
    print(f"alpha v07 sha={ALPHA_SHA[:12]}", flush=True)


def split_tail() -> tuple[Path, Path]:
    seg = WORK / "_seg"
    seg.mkdir(parents=True, exist_ok=True)
    head, tail = seg / "head.mp4", seg / "tail.mp4"
    if not head.exists():
        copy_verified(V11_HEAD, head)
    if packet_count(head) != HEAD_N:
        raise RuntimeError("v11 head is not 10996 packets")
    if not tail.exists():
        run([
            "ffmpeg", "-y", "-v", "error", "-i", str(V11_TAIL), "-an", "-c", "copy",
            "-f", "segment", "-segment_frames", str(CARD_N), "-reset_timestamps", "1",
            str(seg / "tailpart%02d.mp4"),
        ])
        (seg / "tailpart01.mp4").replace(tail)
        (seg / "tailpart00.mp4").unlink(missing_ok=True)
    if packet_count(tail) != TAIL_N:
        raise RuntimeError(f"tail packets {packet_count(tail)} != {TAIL_N}")
    return head, tail


def load_card() -> np.ndarray:
    raw_path = WORK / "_seg" / "card.raw"
    need = CARD_N * FRAME_BYTES
    if not raw_path.exists() or raw_path.stat().st_size != need:
        run([
            "ffmpeg", "-y", "-v", "error", "-ss", f"{CARD_START:.6f}", "-i", str(V08),
            "-frames:v", str(CARD_N), "-f", "rawvideo", "-pix_fmt", "rgb24", str(raw_path),
        ])
    if raw_path.stat().st_size != need:
        raise RuntimeError(f"card.raw {raw_path.stat().st_size} != {need}")
    return np.memmap(raw_path, dtype=np.uint8, mode="r", shape=(CARD_N, H, W, 3))


def encode_raw(frames: int, dest: Path, write) -> None:
    if dest.exists():
        dest.unlink()
    proc = sp.Popen(
        [
            "ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
            "-s", f"{W}x{H}", "-r", str(FPS), "-i", "pipe:0",
            "-frames:v", str(frames), "-an",
            "-c:v", "libx264", "-preset", "veryfast", "-profile:v", "high", "-level", "4.0",
            "-pix_fmt", "yuv420p", "-r", "24", "-video_track_timescale", "12288",
            "-x264-params", f"keyint={frames}:min-keyint={frames}:scenecut=0:open-gop=0",
            "-crf", "8", str(dest),
        ],
        stdin=sp.PIPE,
    )
    assert proc.stdin is not None
    write(proc.stdin)
    proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError(f"encode failed: {dest.name}")
    got = packet_count(dest)
    if got != frames:
        raise RuntimeError(f"{dest.name} packets {got} != {frames}")


def build_middle(card: np.ndarray) -> tuple[Path, Path]:
    seg = WORK / "_seg"
    plate = seg / "plate.mp4"
    body = seg / "body.mp4"
    if not plate.exists():
        encode_raw(PLATE_N, plate, lambda stdin: _write_plate(stdin))
    if packet_count(plate) != PLATE_N:
        raise RuntimeError("plate packet count")
    ref = np.array(card[REF_CARD, TY0:TY1, TX0:TX1])
    base_box = np.array(card[0, TY0:TY1, TX0:TX1])
    opening = np.array(card[0])

    def write_body(stdin) -> None:
        for i in range(LEAD_N):
            frame = opening.copy()
            alpha = 1.0 if i >= FADE_N else ease(i)
            box = (base_box.astype(np.float32) * (1 - alpha) + ref.astype(np.float32) * alpha)
            frame[TY0:TY1, TX0:TX1] = np.clip(box, 0, 255).astype(np.uint8)
            stdin.write(frame.tobytes())
        for i in range(CARD_N):
            frame = np.array(card[i])
            if i <= PASTE_LAST:
                frame[TY0:TY1, TX0:TX1] = ref
            stdin.write(frame.tobytes())

    if not body.exists():
        encode_raw(LEAD_N + CARD_N, body, write_body)
    if packet_count(body) != LEAD_N + CARD_N:
        raise RuntimeError("body packet count")
    # The title layer we used, saved so the evidence shows the one source.
    Image.fromarray(ref).save(WORK / "code_graphics_v07" / "safe_path_title_box.png")
    return plate, body


def _write_plate(stdin) -> None:
    raw = sp.check_output(
        ["ffmpeg", "-v", "error", "-i", str(COMP_SRC), "-frames:v", str(PLATE_N),
         "-f", "rawvideo", "-pix_fmt", "rgb24", "pipe:1"]
    )
    if len(raw) != PLATE_N * FRAME_BYTES:
        raise RuntimeError(f"composite decode {len(raw)}")
    stdin.write(raw)


def splice(head: Path, plate: Path, body: Path, tail: Path) -> Path:
    final = WORK / "hos_008_rough_v12.mp4"
    if final.exists() and packet_count(final) == 12923:
        print("splice already complete", flush=True)
        return final
    lst = WORK / "_seg" / "concat.txt"
    lst.write_text("".join(f"file '{p}'\n" for p in (head, plate, body, tail)))
    video = WORK / "_seg" / "video.mp4"
    if video.exists():
        video.unlink()
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(video)])
    if packet_count(video) != 12923:
        raise RuntimeError(f"concat packets {packet_count(video)} != 12923")
    run([
        "ffmpeg", "-y", "-v", "error", "-itsoffset", "0.125", "-i", str(video), "-i", str(V08),
        "-map", "0:v:0", "-map", "1:a:0", "-c", "copy", "-movflags", "+faststart", str(final),
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


def decode_range(path: Path, ss: float, start_frame: int, count: int) -> np.ndarray:
    raw = sp.check_output(
        ["ffmpeg", "-v", "error", "-ss", f"{ss:.6f}", "-i", str(path),
         "-vf", f"trim=start_frame={start_frame}:end_frame={start_frame + count},setpts=PTS-STARTPTS",
         "-frames:v", str(count), "-f", "rawvideo", "-pix_fmt", "rgb24", "pipe:1"]
    )
    if len(raw) != count * FRAME_BYTES:
        raise RuntimeError(f"decode {path.name} @{ss}+{start_frame} got {len(raw)}")
    return np.frombuffer(raw, dtype=np.uint8).reshape(count, H, W, 3)


def decode_one(path: Path, ss: float, n: int) -> np.ndarray:
    return decode_range(path, ss, n, 1)[0]


def mean_abs(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.abs(a.astype(np.int16) - b.astype(np.int16)).mean())


def title_box(frame: np.ndarray) -> np.ndarray:
    return frame[TY0:TY1, TX0:TX1]


def title_check(master: Path) -> dict:
    """462.25-464.4 s is master frames 11067-11118, 71-122 into the 459.292 GOP."""
    ref = title_box(decode_one(V08, CARD_START, REF_CARD))
    frames = decode_range(master, GOP_START, 71, 52)
    samples = []
    worst = 0.0
    below = []
    crops = []
    for i, frame in enumerate(frames):
        idx = 11067 + i
        m = mean_abs(title_box(frame), ref)
        worst = max(worst, m)
        samples.append({"frame": idx, "mean_abs": round(m, 3)})
        if m > 1.0:
            below.append(idx)
        if i % 4 == 0:
            crops.append(Image.fromarray(title_box(frame)))
    ev = WORK / "composite_evidence_v12"
    ev.mkdir(parents=True, exist_ok=True)
    if crops:
        tile_w, tile_h = crops[0].size
        cols = 7
        rows = (len(crops) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * tile_w, rows * tile_h), (40, 28, 18))
        for i, im in enumerate(crops):
            sheet.paste(im, ((i % cols) * tile_w, (i // cols) * tile_h))
        sheet.save(ev / "title_box_strip_462_25_464_4.jpg", quality=90)
    Image.fromarray(ref).save(ev / "v08_title_box_464_2.jpg", quality=90)
    Image.fromarray(title_box(frames[0])).save(ev / "v12_title_box_462_25.jpg", quality=90)
    Image.fromarray(title_box(frames[-1])).save(ev / "v12_title_box_464_375.jpg", quality=90)
    report = {
        "window_s": [462.25, 464.4],
        "frames": [11067, 11118],
        "reference": "v08 frame 11114 title box (464.208 s)",
        "box": [TX0, TY0, TX1, TY1],
        "worst": round(worst, 3),
        "limit": 1.0,
        "pass": worst <= 1.0 and not below,
        "over_limit": below,
        "samples": samples,
    }
    (WORK / "TITLE_BOX.json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"  title box worst {worst:.3f} over {below[:8]}", flush=True)
    return report


def composite_match(master: Path) -> dict:
    plate = decode_range(master, GOP_START, 0, PLATE_N)
    comp = decode_range(COMP_SRC, 0.0, 0, PLATE_N)
    samples = []
    worst = 0.0
    for n in (0, 5, 11, 21, 32, 38, 41):
        m = mean_abs(plate[n], comp[n])
        worst = max(worst, m)
        samples.append({"row_frame": n, "master_frame_index": ROW0 + n, "mean_abs": round(m, 3)})
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
    """Re-encoded body, then the stream-copied tail."""
    samples = []
    worst = 0.0
    # Offsets into the 459.292 GOP (250 frames) and one into the tail.
    wanted = [
        (464.2, 118, False),
        (466.0, 161, False),
        (468.7, 226, False),
        (469.6, 247, False),
        (469.708, 0, True),
    ]
    for t, n, on_tail in wanted:
        if on_tail:
            a = decode_one(master, TAIL_START, n)
            b = decode_one(V08, TAIL_START, n)
            idx = ROW0 + MID_N + n
        else:
            a = decode_one(master, GOP_START, n)
            b = decode_one(V08, GOP_START, n)
            idx = ROW0 + n
        m = mean_abs(a, b)
        if not on_tail:
            worst = max(worst, m)
        samples.append({
            "t": t, "mean_abs": round(m, 3), "frame_index": idx,
            "stream_copy": on_tail, "same_picture": True,
        })
        print(f"  diff t={t} idx {idx} mean_abs={m:.3f} copy={on_tail}", flush=True)
    body = [s for s in samples if not s["stream_copy"]]
    tail = [s for s in samples if s["stream_copy"]]
    report = {
        "samples": samples,
        "body_worst": round(worst, 3),
        "limit": 1.0,
        "pass": worst <= 1.0 and all(s["mean_abs"] == 0.0 for s in tail),
        "note": "Body is the re-encoded card GOP. From 469.708 s the packets are stream-copied, so the tail sample is 0.",
    }
    (WORK / "FRAME_DIFF.json").write_text(json.dumps(report, indent=2) + "\n")
    return report


def plate_gone(master: Path) -> dict:
    v12 = decode_range(master, GOP_START, 71, HOLD_N)
    v08 = decode_range(V08, GOP_START, 71, HOLD_N)
    samples = []
    worst_low = 1e9
    for i in range(HOLD_N):
        m = mean_abs(v12[i], v08[i])
        worst_low = min(worst_low, m)
        samples.append({"frame": 11067 + i, "mean_abs": round(m, 3)})
    report = {
        "frames": [11067, 11088],
        "min_mean_abs": round(worst_low, 3),
        "need_above": 1.0,
        "pass": worst_low > 1.0,
        "samples": samples,
    }
    (WORK / "PLATE_GONE.json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"  plate-gone min {worst_low:.3f}", flush=True)
    return report


def join_check(master: Path) -> dict:
    pair = decode_range(master, GOP_START, 92, 2)  # frames 11088 and 11089
    m = mean_abs(pair[0], pair[1])
    ev = WORK / "composite_evidence_v12"
    ev.mkdir(parents=True, exist_ok=True)
    Image.fromarray(pair[0]).save(ev / "join_last_leadin.jpg", quality=90)
    Image.fromarray(pair[1]).save(ev / "join_first_card.jpg", quality=90)
    report = {
        "last_leadin_frame": 11088,
        "first_card_frame": 11089,
        "first_card_time_s": CARD_START,
        "mean_abs": round(m, 3),
        "limit": 1.0,
        "pass": m <= 1.0,
    }
    (WORK / "JOIN.json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"  join mean_abs={m:.3f}", flush=True)
    return report


def audio_match(master: Path) -> dict:
    def stream_md5(path: Path) -> str:
        raw = sp.check_output(
            ["ffmpeg", "-v", "error", "-i", str(path), "-map", "0:a:0",
             "-f", "streamhash", "-hash", "md5", "-"],
            text=True,
        )
        return raw.strip()
    a, b = stream_md5(master), stream_md5(V08)
    report = {"v12": a, "v08": b, "pass": a == b and bool(a)}
    (WORK / "AUDIO_MATCH.json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"  audio match {report['pass']}", flush=True)
    return report


def tip_check(master: Path) -> dict:
    spec = importlib.util.spec_from_file_location("build_v08", BUILD_V08)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    offsets = json.loads(OFFSETS.read_text())
    plate = decode_range(master, GOP_START, 0, PLATE_N)
    samples = []
    worst = 0.0
    for row in offsets["samples"]:
        n = int(row["row_frame"])
        gray = np.array(Image.fromarray(plate[n]).convert("L"), dtype="float32")
        trace_x = float(row["tip"]["trace_x"])
        meas = mod.tip_offset(gray, trace_x)
        if meas is None:
            raise RuntimeError(f"tip not found at row frame {n}")
        worst = max(worst, abs(meas["offset_px"]))
        samples.append({"pct": row["pct"], "row_frame": n, "j1273_offset_px": row["tip"]["offset_px"], **meas})
        print(f"  tip p{row['pct']} {meas['offset_px']:+.1f}px", flush=True)
    report = {
        "limit_px": 19.2,
        "worst_abs_px": round(worst, 1),
        "pass": worst <= 19.2,
        "samples": samples,
        "alpha_sha256": ALPHA_SHA,
    }
    (WORK / "ROD_TRACE.json").write_text(json.dumps(report, indent=2) + "\n")
    return report


def write_meta(plate: Path, body: Path) -> None:
    cuts = json.loads(V11_CUTS.read_text())
    for c in cuts:
        if c["row"] == "10_metal_easy":
            c["source"] = "composite_v08.mp4"
            c["source_path"] = str(COMP_SRC)
            c["source_sha256"] = COMP_SHA
            c["disposition"] = "J1267 v12 plate frames 109-150, J1273 alpha 53454827, no render_alpha"
        elif c["row"] == "11_safe_path":
            c["source"] = body.name
            c["source_path"] = str(body)
            c["source_sha256"] = sha256_file(body)
            c["disposition"] = (
                "J1267 v12 51-frame lead-in of the card's own SAFE PATH DOWN title, "
                "then 157 re-encoded card frames with that title held to 464.375s"
            )
    (WORK / "cuts_rough_v12.json").write_text(json.dumps(cuts, indent=2) + "\n")
    copy_verified(V11_POOL, WORK / "pool_rough_v12.json")
    pause = json.loads(V11_PAUSE.read_text())
    pause["inherited"] = "v08 bitstream already contains this pause trim; v12 does not re-trim"
    (WORK / "PAUSE_TRIM_APPLIED.json").write_text(json.dumps(pause, indent=2) + "\n")
    note = {
        "plate": "06_rod_fitting_t1 frames 109-150 via J1273 composite f8453cc7",
        "alpha_sha256": ALPHA_SHA,
        "composite_sha256": COMP_SHA,
        "render_alpha_called": False,
        "title_source": "v08 frame 11114 title box, the card's own full SAFE PATH DOWN",
        "title_box": [TX0, TY0, TX1, TY1],
        "paste_through_s": 464.375,
        "plate_encode_sha256": sha256_file(plate),
    }
    (WORK / "PLATE_INPOINT.json").write_text(json.dumps(note, indent=2) + "\n")


def gates(master: Path) -> dict:
    cuts = WORK / "cuts_rough_v12.json"
    pool = WORK / "pool_rough_v12.json"
    polish_json = WORK / "polish_gate_rough_v12.json"
    polish = sp.run(
        [sys.executable, str(OWB_ROOT / "scripts/polish_gate.py"), str(master),
         "--cuts", str(cuts), "--out", str(polish_json)],
        capture_output=True, text=True,
    )
    (WORK / "polish_gate_rough_v12.txt").write_text(polish.stdout + polish.stderr)
    print((polish.stdout or polish.stderr)[-400:], flush=True)
    pq = WORK / "picture_qa_rough_v12"
    picture = sp.run(
        [sys.executable, str(OWB_ROOT / "scripts/picture_qa.py"), str(master),
         "--cuts", str(cuts), "--pool", str(pool), "--out-dir", str(pq)],
        capture_output=True, text=True,
    )
    (WORK / "picture_qa_rough_v12.txt").write_text(picture.stdout + picture.stderr)
    print((picture.stdout or picture.stderr)[-400:], flush=True)
    note = {"status": "SKIPPED_NO_BED", "reason": "No new bed. Job brief.", "version": "rough_v12"}
    (WORK / "music_gate_rough_v12.json").write_text(json.dumps(note, indent=2) + "\n")
    (WORK / "music_gate_rough_v12.txt").write_text("SKIPPED_NO_BED\n")
    return {"polish_rc": polish.returncode, "picture_rc": picture.returncode}


def evidence_stills(master: Path) -> None:
    ev = WORK / "composite_evidence_v12"
    ev.mkdir(parents=True, exist_ok=True)
    for pct, name in ((10, "p10"), (25, "p25"), (50, "p50"), (75, "p75"), (90, "p90")):
        t = GOP_START + (PLATE_N / FPS) * pct / 100
        run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.3f}", "-i", str(master),
             "-frames:v", "1", "-q:v", "2", str(ev / f"p510_{name}.jpg")])
    run([
        "ffmpeg", "-y", "-v", "error", "-ss", f"{GOP_START:.6f}", "-i", str(master),
        "-vf", "trim=end_frame=42,setpts=PTS-STARTPTS,crop=900:860:520:140,fps=24,scale=240:-1,tile=7x6",
        "-frames:v", "1", str(ev / "p510_workman_contact.jpg"),
    ])


def write_notes(info, comp, diff, tip, gates_rc, gone, join, audio, title) -> None:
    text = f"""# J1267 rough v12

Chief h21. One title: the card's own SAFE PATH DOWN pixels from v08 frame 11114 (464.208 s), pasted onto the opening field. Not a separately drawn title. Alpha {ALPHA_SHA[:12]} copied into code_graphics_v07. render_alpha() was not called. GBP0. No UAT copy.

## Durations
format {info.get('format')} video {info.get('video')} start {info.get('video_start')} frames {info.get('nb_packets')} A/V end offset {info.get('av_end_offset')}

## Title box vs v08 at 464.208 s, frames 11067-11118
worst {title['worst']} limit 1.0 pass {title['pass']} over {title['over_limit'][:12]}

## Join 11088 vs 11089
mean abs {join['mean_abs']} limit 1.0 pass {join['pass']}

## Body vs v08 at 464.2/466/468.7/469.6, and stream copy at 469.708
body worst {diff['body_worst']} limit 1.0 pass {diff['pass']}

## Old plate gone (frames 11067-11088)
min mean abs {gone['min_mean_abs']} need above 1.0 pass {gone['pass']}

## Composite vs f8453cc7
worst {comp['worst']} limit 1.0 pass {comp['pass']}

## Tip
worst {tip['worst_abs_px']} px limit 19.2 pass {tip['pass']}

## Audio
streamhash match {audio['pass']}

## Gates
polish_rc {gates_rc['polish_rc']} picture_rc {gates_rc['picture_rc']}

## Safe path
51-frame lead-in (29 fade + 22 hold) plus 157 re-encoded card frames. The full title is held through 464.375 s. From 469.708 s the packets are stream-copied. Total frames 12923.
"""
    (WORK / "CHECK_NOTE.md").write_text(text)
    body = {
        "version": "rough_v12",
        "job": "J1267",
        "ruling": "Chief h21",
        "master_sha256": sha256_file(WORK / "hos_008_rough_v12.mp4"),
        "alpha_sha256": ALPHA_SHA,
        "render_alpha_called": False,
        "title_source": "v08 frame 11114 title box",
        "durations": info,
        "title_box": {"worst": title["worst"], "pass": title["pass"]},
        "join": join,
        "frame_diff": {"body_worst": diff["body_worst"], "pass": diff["pass"]},
        "plate_gone": {"min_mean_abs": gone["min_mean_abs"], "pass": gone["pass"]},
        "composite_match": {"worst": comp["worst"], "pass": comp["pass"]},
        "tip": {"worst_abs_px": tip["worst_abs_px"], "pass": tip["pass"]},
        "audio_match": audio["pass"],
        "gates": gates_rc,
        "note": "Parked for Chief. No finished-film PASS. No UAT. No upload. GBP0.",
    }
    (WORK / "ROUGH_V12_SUMMARY.json").write_text(json.dumps(body, indent=2) + "\n")


def deliver(include_master: bool) -> None:
    names = [
        "cuts_rough_v12.json", "pool_rough_v12.json",
        "polish_gate_rough_v12.json", "polish_gate_rough_v12.txt",
        "picture_qa_rough_v12.txt", "music_gate_rough_v12.json", "music_gate_rough_v12.txt",
        "ROUGH_V12_SUMMARY.json", "DURATION.json", "PAUSE_TRIM_APPLIED.json",
        "PLATE_INPOINT.json", "ROD_TRACE.json", "FRAME_DIFF.json",
        "COMPOSITE_MATCH.json", "PLATE_GONE.json", "JOIN.json", "AUDIO_MATCH.json",
        "TITLE_BOX.json", "CHECK_NOTE.md",
    ]
    if include_master:
        names.insert(0, "hos_008_rough_v12.mp4")
    for dest_root in (PRECHECK, NAS):
        if dest_root.name in {f"rough_v{n:02d}" for n in range(2, 12)} or dest_root.name == "rough_v11":
            raise RuntimeError(dest_root)
        for name in names:
            src = WORK / name
            if src.exists():
                copy_verified(src, dest_root / name)
        for folder in ("composite_evidence_v12", "code_graphics_v07"):
            src = WORK / folder
            if src.exists():
                copy_verified(src, dest_root / folder)
        if include_master:
            pq = WORK / "picture_qa_rough_v12"
            if pq.exists():
                copy_verified(pq, dest_root / "picture_qa_rough_v12")
        sums = []
        for p in sorted(dest_root.rglob("*")):
            if p.is_file() and not p.name.startswith("._") and p.name != "MEDIA_SHA256SUMS.txt":
                if "picture_qa_rough_v12" in p.parts:
                    continue
                sums.append(f"{sha256_file(p)}  {p.relative_to(dest_root)}\n")
        manifest = WORK / "MEDIA_SHA256SUMS.txt"
        manifest.write_text("".join(sums))
        copy_verified(manifest, dest_root / "MEDIA_SHA256SUMS.txt")
        print(f"delivered {dest_root}", flush=True)


def commit_evidence() -> None:
    git(["-C", str(REPO), "fetch", "origin", "cursor/j1257-hos008-rough-v06"])
    if not WT.exists():
        git(["-C", str(REPO), "worktree", "add", "--detach", str(WT), "origin/cursor/j1257-hos008-rough-v06"])
    dirty = sp.check_output(
        ["git", "-c", f"safe.directory={WT}", "-C", str(WT), "status", "--porcelain"],
        text=True,
    )
    if dirty.strip():
        raise RuntimeError("Evidence commit requires a clean worktree:\n" + dirty[:500])
    edit = WT / "02_Video-Projects/008_Lightning-Franklin/07_Edit-Project"
    desk = edit / "_desk/008/rough_v12"
    if desk.exists():
        raise RuntimeError(f"refusing to write into existing {desk}")
    copy_verified(Path(__file__).resolve(), edit / "_build_rough_v12.py")
    skip_suffix = {".mp4", ".mov", ".wav", ".raw", ".png"}
    for p in WORK.rglob("*"):
        if not p.is_file() or p.name.startswith("._") or p.name.startswith("_"):
            continue
        if p.suffix.lower() in skip_suffix or "_seg" in p.parts or "__pycache__" in p.parts:
            continue
        if p.name.startswith("hos_008"):
            continue
        copy_verified(p, desk / p.relative_to(WORK))
    git(["-C", str(WT), "add", "-f",
         "02_Video-Projects/008_Lightning-Franklin/07_Edit-Project/_build_rough_v12.py",
         "02_Video-Projects/008_Lightning-Franklin/07_Edit-Project/_desk/008/rough_v12"])
    status = sp.run(
        ["git", "-c", f"safe.directory={WT}", "-C", str(WT), "diff", "--cached", "--quiet"]
    )
    if status.returncode == 0:
        print("nothing to commit", flush=True)
        return
    git(["-C", str(WT), "commit", "-m",
         "hos(008): J1267 rough v12 one safe-path title through the join, for Chief review"])
    git(["-C", str(WT), "push", "origin", "HEAD:cursor/j1257-hos008-rough-v06"])
    sha = sp.check_output(
        ["git", "-c", f"safe.directory={WT}", "-C", str(WT), "rev-parse", "--short", "HEAD"],
        text=True,
    ).strip()
    (WORK / "PR_COMMIT.txt").write_text(sha + "\n")
    print(f"pushed evidence {sha}", flush=True)


def main() -> int:
    WORK.mkdir(parents=True, exist_ok=True)
    install_alpha()
    head, tail = split_tail()
    card = load_card()
    plate, body = build_middle(card)
    del card
    master = splice(head, plate, body, tail)
    info = probe_durations(master)
    (WORK / "DURATION.json").write_text(json.dumps(info, indent=2) + "\n")
    print("DURATIONS", json.dumps(info), flush=True)
    if info["nb_packets"] != 12923:
        raise RuntimeError("frame count")
    if abs(info.get("video_start", 9) - 0.125) > 0.002:
        raise RuntimeError(f"video_start {info.get('video_start')}")
    comp = composite_match(master)
    title = title_check(master)
    diff = frame_diff(master)
    gone = plate_gone(master)
    join = join_check(master)
    tip = tip_check(master)
    audio = audio_match(master)
    write_meta(plate, body)
    evidence_stills(master)
    gates_rc = gates(master)
    write_notes(info, comp, diff, tip, gates_rc, gone, join, audio, title)
    ok = (
        title["pass"] and join["pass"] and diff["pass"] and gone["pass"]
        and comp["pass"] and tip["pass"] and audio["pass"]
        and gates_rc["polish_rc"] == 0 and gates_rc["picture_rc"] == 0
        and info["nb_packets"] == 12923
        and abs(info["format"] - 539.626) < 0.05
        and abs(info["video"] - 539.500) < 0.05
        and info.get("av_end_offset", 9) <= (1 / FPS) + 0.001
    )
    deliver(include_master=ok)
    try:
        commit_evidence()
    except Exception:
        traceback.print_exc()
        (WORK / "commit_error.txt").write_text(traceback.format_exc())
    (WORK / "phase_splice.done").write_text(json.dumps({
        "ok": ok,
        "title": title["worst"],
        "join": join["mean_abs"],
        "diff": diff["body_worst"],
        "gates": gates_rc,
    }) + "\n")
    print("RESULT", "PASS" if ok else "CHECK_FAIL", flush=True)
    return 0 if ok else 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SystemExit:
        raise
    except Exception:
        traceback.print_exc()
        raise
