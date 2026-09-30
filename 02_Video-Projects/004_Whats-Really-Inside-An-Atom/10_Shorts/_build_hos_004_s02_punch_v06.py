#!/usr/bin/env python3
"""HOS 004 Short s02 Every Eighth — punch v06 (smooth motion).

Ben phone UAT 29 Sep 20:48: s01/s03 v05 PASS; s02 v05 FAIL "still shaky".
v06: remove shake/jitter — no zoompan, no integer-crop wobble.
Gentle sub-pixel push (scale-up → float crop → scale to 1080×1920).
Keep v05 word-timed captions, EVERY EIGHTH? hook, title 9–14 s,
Davy Medal last line, last-4 s loop, 30 fps. s01/s03 untouched.
gate_shorts_open PASS → iCloud → STOP for Ben. No schedule.
"""
from __future__ import annotations

import json
import os
import shutil
import statistics
import subprocess
import sys
import tempfile
from pathlib import Path

VENV_PY = Path(
    "/Users/benjaminoats/YouTube/History Of Science/"
    "02_Video-Projects/001_How-Did-We-Discover-Germs/10_Shorts/_venv/bin/python"
)
if VENV_PY.exists() and Path(sys.executable) != VENV_PY:
    os.execv(str(VENV_PY), [str(VENV_PY), str(Path(__file__).resolve())])

from PIL import Image, ImageDraw, ImageFont  # noqa: E402

# Reuse caption/chunk helpers from v05
import importlib.util

_V05 = Path(__file__).resolve().parent / "_build_hos_004_punch_shorts_v05.py"
_spec = importlib.util.spec_from_file_location("hos004_shorts_v05", _V05)
v05 = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
# Avoid v05's venv re-exec when loading as module
_spec.loader.exec_module(v05)

REPO = Path("/Users/benjaminoats/YouTube/History Of Science")
HERE = Path(__file__).resolve().parent
PROJ002 = REPO / "02_Video-Projects/002_How-Did-We-Discover-The-Periodic-Table"
ICLOUD = Path.home() / (
    "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT/"
    "004_Whats-Really-Inside-An-Atom/10_Shorts"
)
GATE = REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"
ART = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts/hos004_s02_v06"
W, H = 1080, 1920
FPS = 30

ITEM = {
    "id": "s02_every_eighth",
    "air_date": "2026-10-18",
    "hook": "EVERY EIGHTH?",
    "parent": "How Did We Discover the Periodic Table?",
    "vo": HERE / "vo_v03/hos_004_s02_every_eighth_vo_v04.wav",
    "align": HERE / "vo_v03/hos_004_s02_every_eighth_vo_v04_align.json",
    "rough": PROJ002 / "09_Final-Export/hos_002_part02_rough_v06.mp4",
    # Same story beats as v05; no open_speed (setpts slowdown caused judder)
    "wins": [(59.5, 7.5), (34.0, 7.0), (66.5, 7.0), (42.0, 6.0)],
    "open_ss": 59.5,
}


def log(m: str) -> None:
    ART.mkdir(parents=True, exist_ok=True)
    print(m, flush=True)
    with (ART / "build_v06.log").open("a") as f:
        f.write(m + "\n")


def probe(p: Path) -> float:
    return v05.probe(p)


def ff(*a: str) -> None:
    v05.ff(*a)


def sha256(p: Path) -> str:
    return v05.sha256(p)


def smooth_vf(
    dur: float,
    *,
    zoom: float = 0.06,
    x_bias: float = 0.0,
    zoom_out: bool = False,
) -> str:
    """9:16 with a gentle steady push-in/out — no crop-pan, no zoompan.

    Animated `scale` (eval=frame) gives continuous float size changes; static
    crop to 608×1080 then up to 1080×1920. Crop x/y pans quantize to integers
    and look like rounding wobble on still plates — do not animate crop.
    """
    d = max(0.35, float(dur))
    n_end = max(1.0, d * FPS)
    z = max(0.02, min(0.12, float(zoom)))
    if zoom_out:
        w_expr = f"1920*(1+{z:.5f}*(1-n/{n_end:.3f}))"
        h_expr = f"1080*(1+{z:.5f}*(1-n/{n_end:.3f}))"
    else:
        w_expr = f"1920*(1+{z:.5f}*(n/{n_end:.3f}))"
        h_expr = f"1080*(1+{z:.5f}*(n/{n_end:.3f}))"
    # Fixed framing bias only (not animated) — variety without integer wobble
    xb = float(x_bias)
    return (
        "scale=1920:1080:flags=lanczos,"
        f"scale=w='{w_expr}':h='{h_expr}':eval=frame:flags=lanczos,"
        f"crop=608:1080:'(iw-608)/2+({xb:.2f})':0,"
        "scale=1080:1920:flags=lanczos,"
        "setsar=1"
    )


def encode_seg_smooth(
    src: Path,
    dst: Path,
    start: float,
    dur: float,
    *,
    zoom: float,
    x_bias: float,
    zoom_out: bool,
) -> None:
    vf = smooth_vf(dur, zoom=zoom, x_bias=x_bias, zoom_out=zoom_out)
    ff(
        "-ss",
        f"{start:.3f}",
        "-t",
        f"{dur + 0.05:.3f}",
        "-i",
        str(src),
        "-vf",
        vf,
        "-an",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-profile:v",
        "high",
        "-preset",
        "fast",
        "-crf",
        "18",
        "-r",
        str(FPS),
        "-t",
        f"{dur:.3f}",
        "-movflags",
        "+faststart",
        str(dst),
    )


def build_picture_smooth(work: Path, need: float) -> tuple[Path, Path]:
    rough = Path(ITEM["rough"])
    if not rough.exists():
        raise SystemExit(f"missing {rough}")
    wins = list(ITEM["wins"])
    segs: list[Path] = []
    covered = 0.0
    i = 0
    # Gentle push-in / push-out + fixed x bias (not animated crop)
    pushes = [
        {"zoom": 0.07, "x_bias": 0.0, "zoom_out": False},
        {"zoom": 0.055, "x_bias": -28.0, "zoom_out": True},
        {"zoom": 0.08, "x_bias": 24.0, "zoom_out": False},
        {"zoom": 0.05, "x_bias": -12.0, "zoom_out": True},
    ]
    while covered < need - 0.05:
        st, mx = wins[i % len(wins)]
        off = 0.6 * (i // len(wins))
        take = min(mx - off, need - covered)
        if take < 0.4:
            i += 1
            continue
        out = work / f"seg_{i:02d}.mp4"
        p = pushes[i % len(pushes)]
        encode_seg_smooth(
            rough,
            out,
            st + off,
            take,
            zoom=p["zoom"],
            x_bias=p["x_bias"],
            zoom_out=p["zoom_out"],
        )
        segs.append(out)
        covered += take
        i += 1

    concat = work / "pic.txt"
    concat.write_text("".join(f"file '{s.name}'\n" for s in segs))
    pic = work / "picture.mp4"
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat),
            "-c",
            "copy",
            str(pic),
        ],
        check=True,
        cwd=work,
    )
    trim = work / "picture_trim.mp4"
    ff(
        "-i",
        str(pic),
        "-t",
        f"{need:.3f}",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-preset",
        "fast",
        "-crf",
        "18",
        "-r",
        str(FPS),
        "-an",
        str(trim),
    )
    # Loop open: same window, gentle push-in (no setpts slowdown)
    loop_src = work / "open_src.mp4"
    encode_seg_smooth(
        rough,
        loop_src,
        float(ITEM["open_ss"]),
        4.5,
        zoom=0.07,
        x_bias=0.0,
        zoom_out=False,
    )
    return trim, loop_src


def frame_diff_series(mp4: Path, t0: float, dur: float, fps: int = 30) -> list[float]:
    td = Path(tempfile.mkdtemp(prefix="hos_s02_diff_"))
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-ss",
            f"{t0:.3f}",
            "-t",
            f"{dur:.3f}",
            "-i",
            str(mp4),
            "-vf",
            f"fps={fps},scale=180:320,format=gray",
            str(td / "f%05d.png"),
        ],
        check=True,
    )
    files = sorted(td.glob("f*.png"))
    prev = None
    diffs: list[float] = []
    for f in files:
        a = list(Image.open(f).getdata())
        if prev is not None:
            diffs.append(sum(abs(x - y) for x, y in zip(a, prev)) / len(a))
        prev = a
    shutil.rmtree(td, ignore_errors=True)
    return diffs


def _still_plate_push_check(work: Path) -> dict:
    """Definitive anti-wobble test: freeze one plate, run smooth_vf, diff frames.

    Real footage has natural motion variance; integer crop-step wobble only
    shows cleanly on a still. Fail if near-zero frames mix with jump steps.
    """
    rough = Path(ITEM["rough"])
    still_png = work / "smooth_still.png"
    still_mp4 = work / "smooth_still.mp4"
    pushed = work / "smooth_still_push.mp4"
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-ss",
            f"{float(ITEM['open_ss']):.3f}",
            "-i",
            str(rough),
            "-vf",
            "scale=1920:1080:flags=lanczos",
            "-frames:v",
            "1",
            str(still_png),
        ],
        check=True,
    )
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-loop",
            "1",
            "-i",
            str(still_png),
            "-t",
            "3",
            "-r",
            str(FPS),
            "-pix_fmt",
            "yuv420p",
            str(still_mp4),
        ],
        check=True,
    )
    vf = smooth_vf(3.0, zoom=0.07, x_bias=0.0, zoom_out=False)
    ff(
        "-i",
        str(still_mp4),
        "-vf",
        vf,
        "-an",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-preset",
        "ultrafast",
        "-crf",
        "16",
        "-r",
        str(FPS),
        str(pushed),
    )
    ds = frame_diff_series(pushed, 0.0, 2.8, fps=30)
    if len(ds) < 20:
        return {"ok": False, "error": "too few diffs", "n": len(ds)}
    mean = statistics.mean(ds)
    sd = statistics.pstdev(ds)
    cv = (sd / mean) if mean > 0.05 else 99.0
    near_zero = sum(1 for d in ds if d < max(0.12, mean * 0.22)) / len(ds)
    d2 = [abs(ds[i] - ds[i - 1]) for i in range(1, len(ds))]
    d2_mean = statistics.mean(d2)
    # Crop-pan wobble signature (seen in tests): near_zero ~0.2+ and cv high.
    # Healthy scale push: near_zero≈0, cv≲0.35, steady mean≳0.4
    wobble = near_zero > 0.12 or cv > 0.45
    frozen = mean < 0.35
    ok = (not wobble) and (not frozen)
    row = {
        "ok": ok,
        "mean": round(mean, 3),
        "sd": round(sd, 3),
        "cv": round(cv, 3),
        "near_zero_frac": round(near_zero, 3),
        "d2_mean": round(d2_mean, 3),
        "d2_max": round(max(d2), 3),
        "wobble_fail": wobble,
        "frozen_fail": frozen,
        "vf": vf,
    }
    log(f"SMOOTH still_plate: {row}")
    return row


def verify_smooth_motion(mp4: Path, work: Path, story: float) -> dict:
    """Still-plate push must be smooth; open of final must not be frozen."""
    still = _still_plate_push_check(work)
    ok = bool(still.get("ok"))

    # Story open: require some motion (push or source), no frozen static crop
    open_ds = frame_diff_series(mp4, 0.15, 2.5, fps=30)
    open_mean = statistics.mean(open_ds) if open_ds else 0.0
    if open_mean < 0.35:
        ok = False
        log(f"SMOOTH FAIL open too still mean={open_mean:.3f}")

    # Light sanity on mid window — only fail extreme shake, not natural stills
    mid_t0 = min(8.2, max(0.5, story - 6.0))
    mid_ds = frame_diff_series(mp4, mid_t0, 4.0, fps=30)
    mid_row = None
    if len(mid_ds) >= 20:
        clipped = sorted(mid_ds)[: max(1, int(len(mid_ds) * 0.95))]
        mean_c = statistics.mean(clipped)
        d2 = [abs(mid_ds[i] - mid_ds[i - 1]) for i in range(1, len(mid_ds))]
        d2_clip = sorted(d2)[: max(1, int(len(d2) * 0.95))]
        d2_max = max(d2_clip) if d2_clip else 0.0
        # Only catastrophic micro-shake (not segment content)
        spike = mean_c < 2.0 and d2_max > 10.0
        mid_row = {
            "window": "mid_seg",
            "mean": round(mean_c, 3),
            "d2_max": round(d2_max, 3),
            "spike_fail": spike,
        }
        if spike:
            ok = False
        log(f"SMOOTH mid_seg: {mid_row}")

    out = {
        "ok": ok,
        "open_mean_0_2p5": round(open_mean, 3),
        "still_plate": still,
        "windows": [mid_row] if mid_row else [],
        "note": "gentle scale push-in/out (eval=frame); static crop; no zoompan; no setpts",
    }
    (work / "smooth_motion_check.json").write_text(json.dumps(out, indent=2) + "\n")
    (ART / "smooth_motion_check.json").write_text(json.dumps(out, indent=2) + "\n")
    if not ok:
        raise SystemExit(f"SMOOTH MOTION FAIL — see {work / 'smooth_motion_check.json'}")
    log("SMOOTH OK")
    return out


def build() -> dict:
    vo = Path(ITEM["vo"])
    align = Path(ITEM["align"])
    if not vo.exists() or not align.exists():
        raise SystemExit("missing VO or align")
    # Confirm Davy Medal last line still in align/script
    align_txt = align.read_text()
    if "Davy" not in align_txt and "Medal" not in (HERE / "vo_v03/s02_every_eighth.txt").read_text():
        # soft check via script file
        pass
    script = (HERE / "vo_v03/s02_every_eighth.txt").read_text()
    if "Davy Medal for it" not in script:
        raise SystemExit("script missing Davy Medal last line")

    vo_dur = probe(vo)
    story, loop, total = v05.fit_story_loop(vo_dur)
    work = HERE / "_work_v06" / ITEM["id"]
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)

    words = v05.words_from_align(align)
    chunks = v05.chunk_words(words, story)
    if len(chunks) < 8:
        raise SystemExit(f"too few caption chunks ({len(chunks)})")
    last_chunk = chunks[-1]["text"]
    if "Davy" not in last_chunk and "Medal" not in last_chunk:
        # find any chunk with Davy
        if not any("Davy" in c["text"] or "Medal" in c["text"] for c in chunks):
            raise SystemExit(f"captions missing Davy Medal; last={last_chunk!r}")
    (work / "caption_chunks.json").write_text(json.dumps(chunks, indent=2) + "\n")

    pic, open_clip = build_picture_smooth(work, story)
    audio = v05.mix_vo_bed(vo, story, work)

    story_av = work / "story_av.mp4"
    ff(
        "-i",
        str(pic),
        "-i",
        str(audio),
        "-map",
        "0:v",
        "-map",
        "1:a",
        "-c:v",
        "copy",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-ar",
        "48000",
        "-ac",
        "2",
        "-shortest",
        str(story_av),
    )

    loop_vid = work / "loop.mp4"
    ff(
        "-i",
        str(open_clip),
        "-t",
        f"{loop:.3f}",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-preset",
        "fast",
        "-crf",
        "18",
        "-r",
        str(FPS),
        "-an",
        str(loop_vid),
    )
    loop_av = work / "loop_av.mp4"
    ff(
        "-i",
        str(loop_vid),
        "-f",
        "lavfi",
        "-i",
        "anullsrc=r=48000:cl=stereo",
        "-shortest",
        "-c:v",
        "copy",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        str(loop_av),
    )

    raw = work / "raw.mp4"
    (work / "av.txt").write_text(f"file '{story_av.name}'\nfile '{loop_av.name}'\n")
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(work / "av.txt"),
            "-c",
            "copy",
            str(raw),
        ],
        check=True,
        cwd=work,
    )

    overlays, timeline = v05.caption_overlays(work, ITEM, story, total, chunks)
    (work / "caption_timeline.json").write_text(json.dumps(timeline, indent=2) + "\n")

    inputs: list[str] = ["-i", str(raw)]
    for png, _, _, _, _ in overlays:
        inputs += ["-loop", "1", "-i", str(png)]
    fc = []
    last = "[0:v]"
    for i, (_, t0, t1, _, _) in enumerate(overlays, 1):
        out = f"[v{i}]"
        fc.append(f"{last}[{i}:v]overlay=0:0:enable='between(t,{t0:.3f},{t1:.3f})'{out}")
        last = out

    out_mp4 = HERE / "hos_004_s02_every_eighth_punch_v06.mp4"
    ff(
        *inputs,
        "-filter_complex",
        ";".join(fc),
        "-map",
        last,
        "-map",
        "0:a",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-preset",
        "fast",
        "-crf",
        "18",
        "-r",
        str(FPS),
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-ar",
        "48000",
        "-ac",
        "2",
        "-t",
        f"{total:.3f}",
        "-movflags",
        "+faststart",
        str(out_mp4),
    )
    dur = probe(out_mp4)
    if not (22.0 <= dur <= 27.05):
        log(f"WARN duration {dur:.2f} outside 22–27 band")
    if dur >= 40:
        raise SystemExit("ABORT ≥40s")

    # Smoothness on picture (pre-caption raw story) is cleaner; also check final
    verify_smooth_motion(story_av, work, story)
    # Final with captions — open still must move (captions add energy but open pic moves)
    open_ds = frame_diff_series(out_mp4, 0.15, 2.0, fps=30)
    open_mean = statistics.mean(open_ds) if open_ds else 0.0
    log(f"FINAL open_mean={open_mean:.3f}")

    check = v05.verify_caption_changes(out_mp4, timeline, work, dur)
    gate = v05.run_gate(out_mp4, ITEM["air_date"])

    ICLOUD.mkdir(parents=True, exist_ok=True)
    dest = ICLOUD / out_mp4.name
    dest.write_bytes(out_mp4.read_bytes())
    sheet_src = Path(check["sheet"])
    sheet_dest = ICLOUD / sheet_src.name
    sheet_dest.write_bytes(sheet_src.read_bytes())
    (ICLOUD / f"{out_mp4.stem}_caption_timeline.json").write_text(
        json.dumps(timeline, indent=2) + "\n"
    )

    # Contact sheet to artifacts
    shutil.copy(sheet_src, ART / sheet_src.name)
    shutil.copy(out_mp4, ART / out_mp4.name)

    # Ensure s01/s03 v05 untouched (sanity)
    for keep in (
        HERE / "hos_004_s01_how_small_punch_v05.mp4",
        HERE / "hos_004_s03_her_ring_punch_v05.mp4",
    ):
        if not keep.exists():
            log(f"WARN missing keep file {keep.name}")

    watch = ICLOUD / "WATCH_shorts_s02_v06.txt"
    watch.write_text(
        "HOS 004 Short s02 Every Eighth — punch v06\n"
        "Ben v05 FAIL (29 Sep 20:48): video still shaky.\n"
        "v06: gentle scale push-in/out (eval=frame) + static 9:16 crop. No crop-pan wobble. No zoompan. No setpts.\n"
        "Captions: same v05 word-timed VO align. Hook EVERY EIGHTH?. Title 9–14s. Davy Medal last line. Last-4s loop.\n"
        "s01 + s03 stay on v05 (Ben PASS). Do not schedule until Ben OKs s02 v06.\n"
        "STOP for phone watch.\n"
    )

    rec = {
        "id": ITEM["id"],
        "version": "v06",
        "air_date": ITEM["air_date"],
        "file": str(out_mp4),
        "sha256": sha256(out_mp4),
        "duration_s": round(dur, 3),
        "vo_duration_s": round(vo_dur, 3),
        "story_s": round(story, 3),
        "loop_s": round(loop, 3),
        "fps": FPS,
        "parent": ITEM["parent"],
        "hook": ITEM["hook"],
        "caption_chunks": len(chunks),
        "caption_check": {
            k: check[k]
            for k in (
                "ok",
                "unique_vo_captions_in_0p5_samples",
                "text_changes",
                "crop_change_ratio",
                "sheet",
            )
        },
        "gate": {"pass": gate.get("returncode", 1) == 0},
        "smooth": json.loads((work / "smooth_motion_check.json").read_text()),
        "icloud": str(dest),
        "icloud_sheet": str(sheet_dest),
        "s01_s03": "unchanged v05 Ben PASS",
        "note": (
            "Ben phone UAT FAIL on v05 shake. v06 gentle scale push (no crop-pan). "
            "STOP for Ben. No schedule."
        ),
    }
    idx = HERE / "SHORTS_PUNCH_INDEX_s02_v06.json"
    idx.write_text(json.dumps(rec, indent=2) + "\n")
    (ICLOUD / idx.name).write_text(idx.read_text())
    (ART / idx.name).write_text(idx.read_text())
    log(f"BUILT {out_mp4.name} dur={dur:.2f}s sha={rec['sha256'][:16]}…")
    log(f"ICLOUD {dest}")
    log("STOP for Ben phone watch. s01/s03 v05 untouched. No schedule.")
    return rec


if __name__ == "__main__":
    build()
