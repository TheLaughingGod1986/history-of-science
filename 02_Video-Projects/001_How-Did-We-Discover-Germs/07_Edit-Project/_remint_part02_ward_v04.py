#!/usr/bin/env python3
"""Remint Part 02 plate 08_ward_vs_lens as v04, splice 0:53–1:01 of v01.

v01–v03 FAIL UAT: still-push / Ken Burns on a frozen Victorian ward.
Do NOT splice 08_ward_vs_lens_v02 or v03. Camera must stay locked; nurses/steam/cloth move.

Hypothesis: Flow Ingredients + wrapper “continuous camera motion” invents a zoom
on a locked still. v04 uses a tightened start still, Frames I2V, locked-camera prompt.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "04_Audio" / "tools"))

import orbit_flow_veo_ui as flow  # noqa: E402
from orbit_gemini_veo import already_done, strip_audio  # noqa: E402

PROJ = Path(__file__).resolve().parents[1]
REFS = PROJ / "04_Generated-Clips" / "part02" / "refs"
RAW = PROJ / "04_Generated-Clips" / "part02" / "raw" / "v04_flow"
SRC_STILL = REFS / "08_ward_vs_lens_v03.jpg"
STILL = REFS / "08_ward_vs_lens_v04.jpg"
CLIP = RAW / "08_ward_vs_lens_v04.mp4"
QA = RAW / "qa"
META = PROJ / "07_Edit-Project" / "part02_ward_v04_meta.json"
ROUGH_V01 = PROJ / "09_Final-Export" / "hos_001_part02_rough_v01.mp4"
OUT = PROJ / "09_Final-Export" / "hos_001_part02_rough_v04.mp4"
PROFILE = Path.home() / ".playwright-hos-flow-profile"
MODEL = "Veo 3.1 - Lite"

# IMAGE-TO-VIDEO prefix skips flow_prompt's “continuous camera motion” wrapper.
PROMPT = (
    "IMAGE-TO-VIDEO of the attached start frame. "
    "CAMERA LOCKED on a tripod: no zoom, no push-in, no pull-back, no pan, "
    "no tilt, no Ken Burns, no dolly. Framing identical first frame to last. "
    "REAL ACTING the whole clip: the large mid-stride nurse walks forward down "
    "the aisle carrying her tray, legs striding, apron and skirt cloth swaying; "
    "steam and dust rise in the sunbeams; quilted blankets shift; sparse faceless "
    "3D cartoon germs (teal rods, spiked spheres) drift. Far nurse turns at a bed. "
    "Premium 3D cartoon Victorian ward. No Explorer, no orange robot, no 2D neon, "
    "no modern hospital, no text. Silent picture only."
)

SPLICE_START = 53.0
SPLICE_DUR = 8.0
FPS = 24


def run(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=True, **kw)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def crop_still() -> None:
    """Tighten 16:9 from top-left so the walking nurse reads larger, head intact."""
    if not SRC_STILL.exists():
        raise SystemExit(f"missing start still {SRC_STILL}")
    STILL.parent.mkdir(parents=True, exist_ok=True)
    # 1920x1080 → 1728x972 (90%) origin 0,0 then back to 1920x1080.
    run(
        [
            "ffmpeg", "-y", "-i", str(SRC_STILL),
            "-vf", "crop=1728:972:0:0,scale=1920:1080",
            "-q:v", "2",
            str(STILL),
        ],
        capture_output=True,
    )
    print(f"  still {STILL} {STILL.stat().st_size} bytes", flush=True)


def extract_qa(clip: Path, dest_dir: Path, tag: str) -> dict[str, Path]:
    dest_dir.mkdir(parents=True, exist_ok=True)
    frames = {}
    for t in (0.2, 4.0, 7.5):
        p = dest_dir / f"{tag}_{t:.1f}s.png"
        run(
            [
                "ffmpeg", "-y", "-ss", f"{t:.1f}", "-i", str(clip),
                "-frames:v", "1", str(p),
            ],
            capture_output=True,
        )
        frames[t] = p
    return frames


def rgb_bytes(path: Path, w: int = 320, h: int = 180) -> bytes:
    r = subprocess.run(
        [
            "ffmpeg", "-y", "-i", str(path),
            "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}",
            "pipe:1",
        ],
        capture_output=True,
        check=True,
    )
    return r.stdout


def mae(a: bytes, b: bytes) -> float:
    n = min(len(a), len(b))
    if n == 0:
        return 999.0
    return sum(abs(a[i] - b[i]) for i in range(n)) / n


def zoomed_first_vs_last(first: Path, last: Path, scale: float) -> float:
    """MAE of last frame vs a Ken-Burns crop of the first frame."""
    tmp = first.with_name(first.stem + f"_z{int(scale * 100)}.png")
    # Zoom toward center (classic still-push).
    run(
        [
            "ffmpeg", "-y", "-i", str(first),
            "-vf", f"scale=iw*{scale}:ih*{scale},crop=iw/{scale}:ih/{scale}",
            str(tmp),
        ],
        capture_output=True,
    )
    try:
        return mae(rgb_bytes(tmp), rgb_bytes(last))
    finally:
        tmp.unlink(missing_ok=True)


def judge_motion(clip: Path, tag: str) -> dict:
    """Reject still+camera-move. Local acting with a locked camera passes."""
    frames = extract_qa(clip, QA, tag)
    first, mid, last = frames[0.2], frames[4.0], frames[7.5]
    a, b, c = rgb_bytes(first), rgb_bytes(mid), rgb_bytes(last)
    mae_first_last = mae(a, c)
    mae_first_mid = mae(a, b)
    zoom_scores = {s: zoomed_first_vs_last(first, last, s) for s in (1.08, 1.16, 1.24)}
    best_zoom = min(zoom_scores, key=zoom_scores.get)
    # If a zoomed first-frame matches last better than 1.0x, Flow invented a push.
    ken_burns = zoom_scores[best_zoom] + 1.5 < mae_first_last
    # Tiny global change = freeze (nurses/steam/cloth not acting).
    frozen = mae_first_last < 8.0 and mae_first_mid < 6.0
    reject = ken_burns or frozen
    verdict = {
        "tag": tag,
        "bytes": clip.stat().st_size,
        "mae_first_last": round(mae_first_last, 2),
        "mae_first_mid": round(mae_first_mid, 2),
        "zoom_mae": {str(k): round(v, 2) for k, v in zoom_scores.items()},
        "best_zoom": best_zoom,
        "ken_burns": ken_burns,
        "frozen": frozen,
        "reject": reject,
        "qa": {str(k): str(v) for k, v in frames.items()},
    }
    print(json.dumps(verdict, indent=2), flush=True)
    return verdict


def mint(page, dest: Path) -> dict:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        dest.unlink()
    print(f"=== Flow Lite Frames I2V → {dest.name} ===", flush=True)
    info = flow.generate_clip(
        page,
        PROMPT,
        dest,
        model=MODEL,
        start_frame=STILL,
        timeout_s=900,
        reuse_project=False,
        scenery_only=False,
        attempts=2,
        frames_i2v=True,
    )
    strip_audio(dest)
    if not already_done(dest, min_bytes=400_000):
        raise RuntimeError(f"download too small: {dest} ({dest.stat().st_size if dest.exists() else 0})")
    print(f"  saved {dest} {dest.stat().st_size} {info.get('seconds')}s", flush=True)
    return info


def splice() -> None:
    if not ROUGH_V01.exists():
        raise SystemExit(f"missing {ROUGH_V01}")
    if not already_done(CLIP, min_bytes=400_000):
        raise SystemExit(f"missing clip {CLIP}")
    end = SPLICE_START + SPLICE_DUR
    fc = (
        f"[0:v]trim=0:{SPLICE_START:.3f},setpts=PTS-STARTPTS[v0];"
        f"[1:v]trim=0:{SPLICE_DUR:.3f},setpts=PTS-STARTPTS,"
        f"scale=1280:720:force_original_aspect_ratio=decrease,"
        f"pad=1280:720:(ow-iw)/2:(oh-ih)/2,fps={FPS},format=yuv420p[v1];"
        f"[0:v]trim=start={end:.3f},setpts=PTS-STARTPTS[v2];"
        f"[v0][v1][v2]concat=n=3:v=1:a=0,format=yuv420p[vout]"
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    run(
        [
            "ffmpeg", "-y",
            "-i", str(ROUGH_V01),
            "-i", str(CLIP),
            "-filter_complex", fc,
            "-map", "[vout]", "-map", "0:a",
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-profile:v", "baseline", "-level", "3.1", "-bf", "0",
            "-preset", "fast", "-crf", "18",
            "-c:a", "copy",
            "-movflags", "+faststart", "-brand", "mp42",
            str(OUT),
        ]
    )


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    crop_still()
    meta: dict = {
        "engine": "flow-ui",
        "model": MODEL,
        "frames_i2v": True,
        "prompt": PROMPT,
        "still": str(STILL),
        "src_still": str(SRC_STILL),
        "hypothesis": "Ingredients + camera-motion wrapper invented Ken Burns; Frames + locked prompt",
        "takes": [],
    }

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        ctx, page = flow.launch_context(p, headed=False, profile=flow.profile_path(PROFILE))
        try:
            take = 1
            dest = CLIP
            info = mint(page, dest)
            qa = judge_motion(dest, "take1")
            meta["takes"].append({"take": take, **info, "qa": qa})
            if qa["reject"]:
                print("TAKE 1 REJECT — remint once", flush=True)
                rejected = RAW / "_rejected_08_ward_vs_lens_v04_take1.mp4"
                dest.replace(rejected)
                take = 2
                info = mint(page, dest)
                qa = judge_motion(dest, "take2")
                meta["takes"].append({"take": take, **info, "qa": qa})
                if qa["reject"]:
                    meta["status"] = "FAIL_STILL_PUSH"
                    META.write_text(json.dumps(meta, indent=2))
                    print("FAIL still-push again after remint. STOP. No splice.", flush=True)
                    raise SystemExit(2)
        finally:
            ctx.close()

    splice()
    digest = sha256(OUT)
    meta["status"] = "SPLICED_STOP_FOR_UAT"
    meta["out"] = str(OUT)
    meta["out_bytes"] = OUT.stat().st_size
    meta["sha256"] = digest
    META.write_text(json.dumps(meta, indent=2))
    print(f"SAVED {OUT}", flush=True)
    print(f"size={OUT.stat().st_size} sha256={digest}", flush=True)
    print("STOP. Do not declare PASS. Do not start Parts 03–05.", flush=True)


if __name__ == "__main__":
    main()
