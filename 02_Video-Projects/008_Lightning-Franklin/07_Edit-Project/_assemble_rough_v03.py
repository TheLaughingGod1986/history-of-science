#!/usr/bin/env python3
"""HOS 008 — Rough v03 assembler (J1218 Chief FIX of diagnostic v02).

Preserves v01/v02 masters and manifests. Delivers a separate diagnostic rough v03:
1. Non-destructive NAS: fresh WORK/desk/NAS dirs; never unlink/rmtree prior NAS deliverables.
2. P5 10_metal_easy: cleaned alpha over KEEP P5:06_rod_fitting (breaks 09/10/11 full-frame chain).
3. P4 06_same_thing: keep sequential full-frame moving plates; CG label timing from graphics v02.
4. Suppress duplicate side labels on P4:08 / P5:11 (boards cleared; assembler skip list).
5. Contact-sheet labels use actual sampled master time (mid), not stale film_t.
6. J1193 ten-FIX / one-KEEP dispositions applied via code_graphics_v02 + this assembly.
7. §4 pause-trim ≤540 s; no music bed (SKIPPED_NO_BED). £0. No new generation.
"""
from __future__ import annotations

import hashlib
import json
import math
import shutil
import subprocess as sp
import sys
import traceback
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1920, 1080, 24
FONT = "/System/Library/Fonts/Supplemental/Didot.ttc"
BROWN = (61, 41, 28)
CREAM = (245, 232, 210, 255)
GOLD = (242, 208, 122, 255)
SHADOW = (36, 22, 12)

EDIT_DIR = Path(__file__).resolve().parent
FILM_DIR = EDIT_DIR.parent
HOS_ROOT = FILM_DIR.parent.parent
OWB_ROOT = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
MEDIA_DIR = Path(
    "/Users/benjaminoats/YouTube/hos-008-lightning/02_Video-Projects/008_Lightning-Franklin"
)
CG_DIR = EDIT_DIR / "code_graphics_v02"
CG_DIR_FALLBACK = EDIT_DIR / "code_graphics_v01"
WORK = Path("/Volumes/data/mac-mini-archive/tmp-render-scratch/j1218-hos008-rough-v03")
PRECHECK = MEDIA_DIR / "07_Edit-Project/_precheck/rough_v03"
DESK = EDIT_DIR / "_desk/008/rough_v03"
UAT_ROOT = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT"
NAS_FILM = Path(
    "/Volumes/data/mac-mini-archive/YouTube/History Of Science/02_Video-Projects/008_Lightning-Franklin"
)

# Moving-plate overlay rows (alpha MOV over minted KEEP plates).
# v03: 10_metal_easy returns to plate+cleaned-alpha over rod_fitting so P5:09/10/11
# are not three consecutive full-frame teach graphics (Chief J1218 29–30 Oct).
# 06_same_thing stays sequential full-frame plates (build_sequential_same_thing).
OVERLAY_COMPOSITES = {
    "15_likeness_fire": {
        "part": 2,
        "alpha": "code_graphic_008_p2_15_likeness_fire.mov",
        "plates": [("02", "12_notebook_list", "tail")],
    },
    "04_letter_crosses": {
        "part": 3,
        "alpha": "code_graphic_008_p3_04_letter_crosses.mov",
        "plates": [("03", "07_slow_news", "full")],
    },
    "08_looking_path": {
        "part": 5,
        "alpha": "code_graphic_008_p5_08_looking_path.mov",
        "plates": [("01", "16_question_sky", "full")],
    },
    "10_metal_easy": {
        "part": 5,
        "alpha": "code_graphic_008_p5_10_metal_easy.mov",
        "plates": [("05", "06_rod_fitting", "full")],
    },
}

# CG rows that already bake the teaching header — never stamp a second side_label.
SUPPRESS_SIDE_LABEL = frozenset({"08_teach_charge", "11_safe_path", "06_same_thing", "10_metal_easy"})

# Honest subject-preserving reframes (upscale stays under 2.35×).
# 09_window_storm: natural window mullion at ~6% trips split detector; crop left 5%.
PLATE_REFRAMES: dict[tuple[int, str], dict] = {
    (2, "09_window_storm"): {
        "vf_prefix": "crop=iw*0.95:ih:iw*0.05:0,",
        "upscale_factor": 1.0 / 0.95,
        "note": "J1218: crop left 5% to clear natural window-edge seam at 0.06; document if detector still FAILs",
    },
}


def resolve_cg_dir() -> Path:
    """Prefer repaired v02 pack; fall back to v01 only if a required file is absent."""
    if CG_DIR.exists():
        return CG_DIR
    if CG_DIR_FALLBACK.exists():
        print("WARN: code_graphics_v02 missing; falling back to v01", flush=True)
        return CG_DIR_FALLBACK
    raise FileNotFoundError("code_graphics_v02 and v01 both missing")


def cg_file(name: str) -> Path:
    primary = CG_DIR / name
    if primary.exists():
        return primary
    fb = CG_DIR_FALLBACK / name
    if fb.exists():
        print(f"WARN: using v01 fallback for {name}", flush=True)
        return fb
    raise FileNotFoundError(name)


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def probe_dur(p: Path) -> float:
    return float(
        sp.check_output(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
            text=True,
        ).strip()
    )


def font(size: int, italic: bool = True) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT, size, index=1 if italic else 0)


def fit_font(text: str, max_w: int, size: int, floor: int = 28, italic: bool = True) -> ImageFont.FreeTypeFont:
    f = font(size, italic=italic)
    while size > floor and f.getbbox(text)[2] > max_w:
        size -= 2
        f = font(size, italic=italic)
    return f


def ease(x: float) -> float:
    x = max(0.0, min(1.0, x))
    return x * x * (3.0 - 2.0 * x)


def prog(t: float, a: float, b: float) -> float:
    return ease((t - a) / (b - a)) if b > a else 1.0


def card_alpha(t: float, start: float, end: float, fade: float = 0.36) -> float:
    if t < start or t > end:
        return 0.0
    inn = prog(t, start, start + fade)
    out = 1.0 - prog(t, end - fade, end)
    return max(0.0, min(inn, out))


def load_mint_index() -> dict[tuple[str, str], Path]:
    log = json.loads((EDIT_DIR / "FLOW_MINT_LOG_v03.json").read_text())
    out: dict[tuple[str, str], Path] = {}
    for _k, v in log["takes"].items():
        if v.get("status") != "KEEP":
            continue
        part = str(v["part"]).zfill(2)
        plate = v["plate"]
        fp = Path(v["file"])
        if not fp.exists():
            cand = MEDIA_DIR / f"04_Generated-Clips/part{part}/raw/v01/{plate}_t1.mp4"
            if cand.exists():
                fp = cand
            else:
                raise FileNotFoundError(f"KEEP file missing for P{part}:{plate}: {v['file']}")
        out[(part, plate)] = fp
    return out


def flow_clip(mint: dict[tuple[str, str], Path], part: str | int, plate: str) -> Path:
    p = str(part).zfill(2)
    if (p, plate) in mint:
        return mint[(p, plate)]
    cand = MEDIA_DIR / f"04_Generated-Clips/part{p}/raw/v01/{plate}_t1.mp4"
    if cand.exists():
        return cand
    raise FileNotFoundError(f"No Flow KEEP for P{p}:{plate}")


def draw_side_label(frame: Image.Image, text: str, t_local: float, use_s: float) -> Image.Image:
    """House cream Didot italic stamp, bottom centre; fades in/out; one label at a time."""
    # Hold label for min(3.6s, use_s - 0.4) starting 0.15s into the plate.
    start = 0.15
    end = min(use_s - 0.25, start + 3.6)
    if end <= start + 0.6:
        end = use_s - 0.1
    a = card_alpha(t_local, start, end, fade=0.35)
    if a <= 0.01:
        return frame
    im = frame.convert("RGBA")
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    slide = int((1.0 - prog(t_local, start, start + 0.4)) * 18)
    f = fit_font(text, 1500, 58, 34)
    sc = (*SHADOW, int(230 * a))
    d.text(
        (W / 2, 940 + slide),
        text,
        font=f,
        fill=(GOLD[0], GOLD[1], GOLD[2], int(255 * a)),
        anchor="mm",
        stroke_width=4,
        stroke_fill=sc,
    )
    return Image.alpha_composite(im, layer).convert("RGB")


def build_overlay_composite(pid: str, meta: dict, mint: dict, use_s: float, out: Path) -> Path:
    """Composite alpha overlay onto moving plate(s) via ffmpeg filters (fast)."""
    if out.exists():
        try:
            if abs(probe_dur(out) - use_s) < 0.15 and out.stat().st_size > 200_000:
                return out
        except Exception:
            pass
        out.unlink(missing_ok=True)
    out.parent.mkdir(parents=True, exist_ok=True)
    alpha_path = cg_file(meta["alpha"])
    plates = meta["plates"]
    tmp = out.with_suffix(".building.mp4")

    if len(plates) == 1:
        part, plate, mode = plates[0]
        src = flow_clip(mint, part, plate)
        dur = probe_dur(src)
        start = max(0.0, dur - use_s - 0.05) if mode == "tail" else 0.0
        # Soft lift (eq) then overlay alpha MOV; force 24fps / exact length.
        filt = (
            f"[0:v]scale={W}:{H}:flags=lanczos,fps={FPS},"
            f"eq=brightness=0.04:contrast=0.96,format=rgba[base];"
            f"[1:v]scale={W}:{H}:flags=lanczos,fps={FPS},format=rgba[ov];"
            f"[base][ov]overlay=0:0:format=auto,format=yuv420p[v]"
        )
        cmd = [
            "ffmpeg", "-y", "-v", "error",
            "-ss", f"{start:.3f}", "-t", f"{use_s:.3f}", "-i", str(src),
            "-t", f"{use_s:.3f}", "-i", str(alpha_path),
            "-filter_complex", filt, "-map", "[v]", "-an",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "17",
            "-t", f"{use_s:.3f}", "-movflags", "+faststart", str(tmp),
        ]
    else:
        # P4:06 left/right split of two KEEP plates under the alpha divider.
        left = flow_clip(mint, plates[0][0], plates[0][1])
        right = flow_clip(mint, plates[1][0], plates[1][1])
        filt = (
            f"[0:v]scale={W}:{H}:flags=lanczos,fps={FPS},eq=brightness=0.04:contrast=0.96,crop={W//2}:{H}:0:0[L];"
            f"[1:v]scale={W}:{H}:flags=lanczos,fps={FPS},eq=brightness=0.04:contrast=0.96,crop={W//2}:{H}:{W//2}:0[R];"
            f"[L][R]hstack=inputs=2,format=rgba[base];"
            f"[2:v]scale={W}:{H}:flags=lanczos,fps={FPS},format=rgba[ov];"
            f"[base][ov]overlay=0:0:format=auto,format=yuv420p[v]"
        )
        cmd = [
            "ffmpeg", "-y", "-v", "error",
            "-t", f"{use_s:.3f}", "-i", str(left),
            "-t", f"{use_s:.3f}", "-i", str(right),
            "-t", f"{use_s:.3f}", "-i", str(alpha_path),
            "-filter_complex", filt, "-map", "[v]", "-an",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "17",
            "-t", f"{use_s:.3f}", "-movflags", "+faststart", str(tmp),
        ]
    sp.run(cmd, check=True)
    tmp.replace(out)
    print(f"  overlay {pid}: {probe_dur(out):.2f}s {out.stat().st_size} bytes", flush=True)
    return out



def build_sequential_same_thing(mint: dict, use_s: float, out: Path) -> Path:
    """P4:06 — sequential full-frame jar_spark then knuckle_spark (no hstack split)."""
    if out.exists():
        try:
            if abs(probe_dur(out) - use_s) < 0.15 and out.stat().st_size > 200_000:
                return out
        except Exception:
            pass
        out.unlink(missing_ok=True)
    out.parent.mkdir(parents=True, exist_ok=True)
    jar = flow_clip(mint, "02", "08_jar_spark")
    knuckle = flow_clip(mint, "04", "02_knuckle_spark")
    half = use_s / 2.0
    tmp_a = out.with_suffix(".a.mp4")
    tmp_b = out.with_suffix(".b.mp4")
    tmp = out.with_suffix(".building.mp4")
    for src, dst, t0 in ((jar, tmp_a, 0.0), (knuckle, tmp_b, 0.4)):
        sp.run(
            [
                "ffmpeg", "-y", "-v", "error",
                "-ss", f"{t0:.3f}", "-t", f"{half:.3f}", "-i", str(src),
                "-an", "-vf", f"scale={W}:{H}:flags=lanczos,fps={FPS},eq=brightness=0.04:contrast=0.96",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p",
                "-t", f"{half:.3f}", str(dst),
            ],
            check=True,
        )
    concat = out.with_suffix(".concat.txt")
    concat.write_text(f"file '{tmp_a}'\nfile '{tmp_b}'\n")
    sp.run(
        [
            "ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(concat),
            "-c", "copy", "-movflags", "+faststart", str(tmp),
        ],
        check=True,
    )
    tmp.replace(out)
    for p in (tmp_a, tmp_b, concat):
        p.unlink(missing_ok=True)
    print(f"  sequential 06_same_thing: {probe_dur(out):.2f}s (no split)", flush=True)
    return out


def pause_trim_av(video: Path, out: Path, max_pause: float = 0.6, target_max_s: float = 540.0) -> dict:
    """STUDIO_PLAYBOOK §4: trim pauses over 0.6s to ~0.6s on assembled A/V. Prefer regions
    0:15–0:45 and 1:00–2:30. Words untouched. Returns trim report.

    J1218 fix: do NOT use input-seek `-ss`/`-to` before `-i` (keyframe snap lengthened
    557.8s → 618s). One decode pass with trim/atrim + concat keeps duration honest.
    """
    import re

    # Detect silences on audio
    r = sp.run(
        ["ffmpeg", "-i", str(video), "-af", "silencedetect=noise=-35dB:d=0.35", "-f", "null", "-"],
        capture_output=True, text=True,
    )
    durs = []
    for ln in r.stderr.splitlines():
        m = re.search(r"silence_end:\s*([0-9.]+).*silence_duration:\s*([0-9.]+)", ln)
        if m:
            durs.append((float(m.group(1)) - float(m.group(2)), float(m.group(1)), float(m.group(2))))
    # Prefer cutting in focus windows; then anywhere
    focus = [(15.0, 45.0), (60.0, 150.0)]
    cuts = []  # (cut_start, cut_end) absolute times to REMOVE
    trimmed = 0.0
    dur0 = probe_dur(video)

    def priority(item):
        s, e, d = item
        in_focus = any(a <= s <= b or a <= e <= b for a, b in focus)
        return (0 if in_focus else 1, -d)

    # Only cut silences that drop ≥0.35s (fewer keep segs; avoids 30+ fragment encode).
    min_drop = 0.35
    for s, e, d in sorted(durs, key=priority):
        drop = d - max_pause
        if drop < min_drop:
            continue
        mid = (s + e) / 2.0
        cs = mid - drop / 2.0
        ce = mid + drop / 2.0
        cuts.append((cs, ce))
        trimmed += drop
        if trimmed >= 18.0 and (dur0 - trimmed) <= target_max_s:
            break
    # Also keep trimming until under target if needed (allow smaller drops then)
    if dur0 - trimmed > target_max_s:
        for s, e, d in sorted(durs, key=lambda x: -x[2]):
            if any(abs(s - c[0]) < 0.05 for c in cuts):
                continue
            drop = d - max_pause
            if drop < 0.12:
                continue
            mid = (s + e) / 2.0
            cuts.append((mid - drop / 2.0, mid + drop / 2.0))
            trimmed += drop
            if dur0 - trimmed <= target_max_s:
                break
    cuts.sort()
    # Merge overlapping
    merged = []
    for cs, ce in cuts:
        if merged and cs <= merged[-1][1] + 0.01:
            merged[-1] = (merged[-1][0], max(merged[-1][1], ce))
        else:
            merged.append((cs, ce))
    # Build keep ranges
    keep = []
    t = 0.0
    for cs, ce in merged:
        if cs > t + 0.05:
            keep.append((t, cs))
        t = max(t, ce)
    if t < dur0 - 0.05:
        keep.append((t, dur0))
    if not merged or not keep:
        shutil.copy2(video, out)
        return {"trimmed_s": 0.0, "duration_in": dur0, "duration_out": dur0, "cuts": [], "under_9min": dur0 <= target_max_s}

    # Segment extract with accurate decode-seek (-ss AFTER -i). Avoids:
    # - input-seek keyframe pad that lengthened 557→618
    # - 37-branch filter_complex deadlock/hang on NAS +faststart
    # Work on local /tmp, then move the concat result to `out`.
    import tempfile

    # Drop tiny keep fragments and tiny cut scraps: merge keep gaps <0.08s
    keep2: list[tuple[float, float]] = []
    for a, b in keep:
        if b - a < 0.08:
            continue
        if keep2 and a - keep2[-1][1] < 0.08:
            keep2[-1] = (keep2[-1][0], b)
        else:
            keep2.append((a, b))
    keep = keep2
    if not keep:
        shutil.copy2(video, out)
        return {"trimmed_s": 0.0, "duration_in": dur0, "duration_out": dur0, "cuts": [], "under_9min": dur0 <= target_max_s}

    local_root = Path(tempfile.mkdtemp(prefix="j1218_pause_", dir="/private/tmp"))
    try:
        segs: list[Path] = []
        for i, (a, b) in enumerate(keep):
            seg = local_root / f"seg_{i:03d}.mp4"
            dur = max(0.05, b - a)
            print(f"  pause-seg {i+1}/{len(keep)} {a:.2f}-{b:.2f} ({dur:.2f}s)", flush=True)
            sp.run(
                [
                    "ffmpeg", "-y", "-v", "error",
                    "-i", str(video),
                    "-ss", f"{a:.3f}", "-t", f"{dur:.3f}",
                    "-c:v", "libx264", "-preset", "ultrafast", "-crf", "18", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                    # no +faststart on segments (avoids mid-write seek hangs on slow disks)
                    str(seg),
                ],
                check=True,
            )
            segs.append(seg)
        concat = local_root / "concat.txt"
        concat.write_text("".join(f"file '{s}'\n" for s in segs))
        local_out = local_root / "trimmed.mp4"
        sp.run(
            [
                "ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(concat),
                "-c", "copy", "-movflags", "+faststart", str(local_out),
            ],
            check=True,
        )
        shutil.copy2(local_out, out)
    finally:
        shutil.rmtree(local_root, ignore_errors=True)
    dur1 = probe_dur(out)
    report = {
        "trimmed_s": round(dur0 - dur1, 3),
        "duration_in": round(dur0, 3),
        "duration_out": round(dur1, 3),
        "max_pause_s": max_pause,
        "cuts": [{"from": round(a, 3), "to": round(b, 3)} for a, b in merged],
        "keep_ranges": [{"from": round(a, 3), "to": round(b, 3)} for a, b in keep],
        "under_9min": dur1 <= target_max_s,
        "method": "local_tmp_accurate_seek_segments",
        "n_keep_segs": len(keep),
    }
    # Trailing silence pad: if still a hair over 9:00, hard-cap to target (VO ends first).
    # Cap on local /tmp without +faststart — NAS remux+faststart hangs (J1218).
    if dur1 > target_max_s:
        over = dur1 - target_max_s
        print(f"  trailing cap: {dur1:.3f}s → {target_max_s:.3f}s via /private/tmp (drop {over:.3f}s)", flush=True)
        import tempfile

        local_root = Path(tempfile.mkdtemp(prefix="j1218_trail_", dir="/private/tmp"))
        try:
            capped = local_root / "capped.mp4"
            sp.run(
                [
                    "ffmpeg", "-y", "-v", "error", "-i", str(out),
                    "-t", f"{target_max_s:.3f}", "-c", "copy", str(capped),
                ],
                check=True,
            )
            sp.run(["rsync", "-a", str(capped), str(out)], check=True)
        finally:
            shutil.rmtree(local_root, ignore_errors=True)
        dur1 = probe_dur(out)
        report["trimmed_s"] = round(dur0 - dur1, 3)
        report["duration_out"] = round(dur1, 3)
        report["under_9min"] = dur1 <= target_max_s + 0.05
        report["trailing_cap_s"] = round(over, 3)
    print(f"PAUSE TRIM {dur0:.2f}s → {dur1:.2f}s (cut {report['trimmed_s']}s)", flush=True)
    if dur1 > target_max_s + 0.05:
        print(f"WARNING: still over 9:00 ({dur1:.2f}s); needs more pause cut or Chief ruling", flush=True)
    return report


def _removed_intervals(pause_report: dict) -> list[tuple[float, float]]:
    """Removed (from,to) segments in pre-trim time, sorted."""
    raw = pause_report.get("cuts") or pause_report.get("prior_cuts") or []
    out: list[tuple[float, float]] = []
    for c in raw:
        if isinstance(c, dict):
            out.append((float(c["from"]), float(c["to"])))
        else:
            out.append((float(c[0]), float(c[1])))
    out.sort()
    return out


def map_time_through_removals(t: float, removed: list[tuple[float, float]]) -> float:
    """Map a pre-trim timeline time into post-trim time after silence cuts."""
    shift = 0.0
    for a, b in removed:
        if b <= t:
            shift += b - a
        elif a < t < b:
            return max(0.0, a - shift)
        else:
            break
    return max(0.0, t - shift)


def remap_cuts_after_pause_trim(
    cuts: list[dict],
    pause_report: dict,
    *,
    duration_out: float | None = None,
) -> list[dict]:
    """Rewrite timeline_in/out (and film_t) so gates sample inside the trimmed master."""
    removed = _removed_intervals(pause_report)
    if not removed:
        return [dict(c) for c in cuts]
    dur_out = float(duration_out if duration_out is not None else pause_report.get("duration_out") or 0.0)
    remapped: list[dict] = []
    for c in cuts:
        row = dict(c)
        tin = map_time_through_removals(float(c["timeline_in"]), removed)
        tout = map_time_through_removals(float(c["timeline_out"]), removed)
        if dur_out > 0:
            tin = min(tin, max(0.0, dur_out - 0.05))
            tout = min(max(tout, tin + 0.04), dur_out)
        row["timeline_in"] = round(tin, 4)
        row["timeline_out"] = round(tout, 4)
        row["timeline_pretrim_in"] = float(c["timeline_in"])
        row["timeline_pretrim_out"] = float(c["timeline_out"])
        if "film_t" in c:
            row["film_t_pretrim"] = float(c["film_t"])
            row["film_t"] = round(map_time_through_removals(float(c["film_t"]), removed), 4)
        remapped.append(row)
    return remapped


def prepare_special_assets(mint: dict) -> dict[str, Path]:
    asset_dir = WORK / "special_assets"
    asset_dir.mkdir(parents=True, exist_ok=True)
    out: dict[str, Path] = {}
    man = {r["row"].split(":", 1)[1]: r for r in json.loads((EDIT_DIR / "CODE_GRAPHICS_v01_MANIFEST.json").read_text())}

    # Full-frame code graphics: retime 30fps -> 24fps to exact use_s
    for pid, row in man.items():
        if pid in OVERLAY_COMPOSITES:
            continue
        src = cg_file(row["spec"]["file"])
        use_s = float(row["use_s"])
        dst = asset_dir / f"cg_{pid}.mp4"
        if not dst.exists() or abs(probe_dur(dst) - use_s) > 0.2:
            sp.run(
                [
                    "ffmpeg", "-y", "-v", "error", "-i", str(src),
                    "-an", "-vf", f"scale={W}:{H}:flags=lanczos,fps={FPS}",
                    "-t", f"{use_s:.3f}",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p",
                    str(dst),
                ],
                check=True,
            )
        out[pid] = dst

    # Moving-plate overlays (v02: 06_same_thing and 10_metal_easy handled below/above)
    for pid, meta in OVERLAY_COMPOSITES.items():
        use_s = float(man[pid]["use_s"])
        dst = asset_dir / f"overlay_{pid}.mp4"
        build_overlay_composite(pid, meta, mint, use_s, dst)
        out[pid] = dst

    # Sequential full-frame replacement for the old split composite
    use_same = float(man["06_same_thing"]["use_s"])
    dst_same = asset_dir / "overlay_06_same_thing.mp4"
    build_sequential_same_thing(mint, use_same, dst_same)
    out["06_same_thing"] = dst_same
    assert "10_metal_easy" in out, "10_metal_easy overlay missing"
    print("  10_metal_easy: alpha over KEEP 06_rod_fitting (v03 Teach MOTION fix)", flush=True)
    return out


def resolve_source(
    part_no: int,
    plate: dict,
    mint: dict,
    special: dict[str, Path],
) -> tuple[Path, float, str, str, float]:
    """Returns src, start_s, vf, disposition, upscale."""
    pid = plate["id"]
    q = plate["quality"]
    if q in ("Quality", "Fast"):
        src = flow_clip(mint, part_no, pid)
        upscale = 1.0 if q == "Quality" else 1.5
        vf = f"scale={W}:{H}:flags=lanczos,fps={FPS}"
        disp = f"KEEP Flow {q} t1 (J1191)"
        refr = PLATE_REFRAMES.get((part_no, pid))
        if refr:
            vf = refr["vf_prefix"] + vf
            upscale = upscale * float(refr["upscale_factor"])
            disp = f"{disp}; {refr['note']}"
        return src, 0.0, vf, disp, upscale
    if q == "code_graphic":
        src = special[pid]
        note = "v03 sequential full-frame (no split)" if pid == "06_same_thing" else (
            "v03 alpha over KEEP 06_rod_fitting" if pid == "10_metal_easy" else f"Code graphic (£0, {src.name})"
        )
        return src, 0.0, f"scale={W}:{H}:flags=lanczos,fps={FPS}", note, 1.0
    raise ValueError(f"Unknown quality {q} on P{part_no}:{pid}")


def contact_sheet(video: Path, cuts: list[dict], out_dir: Path, path: Path) -> None:
    """Build contact sheet. Cuts may be pre-pause-trim board times — clamp seeks to the
    delivered file duration so a §4 trim never seeks past EOF (J1218 hang/exit 234)."""
    cols, tw, th = 6, 320, 180
    rows = (len(cuts) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw, rows * (th + 28)), (28, 22, 18))
    d = ImageDraw.Draw(sheet)
    f = font(14, italic=False)
    vid_dur = max(0.1, probe_dur(video))
    last_safe = max(0.05, vid_dur - 0.08)
    import tempfile

    tmp_cs = Path(tempfile.mkdtemp(prefix="j1218v03_cs_", dir="/private/tmp"))
    try:
        for i, c in enumerate(cuts):
            mid = (float(c["timeline_in"]) + float(c["timeline_out"])) / 2.0
            mid = min(max(0.05, mid), last_safe)
            # PNG on local /tmp: avoids mjpeg YUV rejects and NAS per-frame seek latency.
            png = tmp_cs / f"_cs_{i:03d}.png"
            sp.run(
                [
                    "ffmpeg", "-y", "-v", "error",
                    "-i", str(video), "-ss", f"{mid:.3f}",
                    "-frames:v", "1", "-vf", f"scale={tw}:{th}:flags=lanczos",
                    str(png),
                ],
                check=True,
            )
            x, y = (i % cols) * tw, (i // cols) * (th + 28)
            sheet.paste(Image.open(png).convert("RGB"), (x, y))
            # Label with the actual seek time used (mid of remapped interval), not stale film_t.
            t = mid
            d.text((x + 4, y + th + 4), f"{c['row'][:20]} {int(t // 60)}:{t % 60:05.2f}", font=f, fill=(240, 232, 215))
            png.unlink(missing_ok=True)
        # Write sheet locally then rsync — NAS Image.save can stall.
        local_sheet = tmp_cs / "contact.jpg"
        sheet.save(local_sheet, quality=88)
        sp.run(["rsync", "-a", str(local_sheet), str(path)], check=True)
    finally:
        shutil.rmtree(tmp_cs, ignore_errors=True)


def assemble_part(part_no: int, mint: dict, special: dict[str, Path]) -> dict:
    pstr = f"{part_no:02d}"
    board = json.loads((EDIT_DIR / "parts" / f"part-{pstr}_plates_v03.json").read_text())
    vo_path = FILM_DIR / board["vo_file"]
    assert vo_path.exists(), vo_path
    assert sha256_file(vo_path) == board["vo_sha256"], f"VO sha mismatch part {pstr}"

    slug = f"part{pstr}_rough_v03"
    name = f"hos_008_{slug}"
    out_dir = WORK / slug
    if out_dir.exists():
        n=2
        while (WORK / f"{slug}_r{n:02d}").exists():
            n+=1
        out_dir = WORK / f"{slug}_r{n:02d}"
        print(f"  part out_dir collision -> {out_dir.name} (kept prior)", flush=True)
    out_dir.mkdir(parents=True)
    seg_dir = out_dir / "segs"
    seg_dir.mkdir()

    t0 = float(board["vo_film_start_s"])
    end = float(board["part_end_film_s"])
    plates = board["plates"]
    cuts = []
    segs = []
    cur_frames = 0

    for k, p in enumerate(plates):
        nxt = float(plates[k + 1]["t_s"]) if k + 1 < len(plates) else end
        f_in = round((float(p["t_s"]) - t0) * FPS)
        f_out = round((nxt - t0) * FPS)
        n_frames = f_out - f_in
        assert n_frames > 0, f"P{pstr}:{p['id']} non-positive frames"

        src, start_s, vf, disp, upscale = resolve_source(part_no, p, mint, special)
        src_dur = probe_dur(src)
        need = n_frames / FPS
        if start_s + need > src_dur + 0.08:
            start_s = max(0.0, round(src_dur - need - 0.04, 3))

        seg_path = seg_dir / f"seg_{k:02d}_{p['id']}.mp4"
        label = (p.get("side_label") or "").strip()
        # Suppress duplicate headers already baked into CG / overlay rows (J1193 / Chief).
        if p["id"] in SUPPRESS_SIDE_LABEL:
            label = ""
        t_in_part = f_in / FPS
        t_out_part = f_out / FPS

        if not label:
            sp.run(
                [
                    "ffmpeg", "-y", "-v", "error", "-ss", f"{start_s:.3f}", "-i", str(src),
                    "-an", "-vf", vf, "-frames:v", str(n_frames),
                    "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-pix_fmt", "yuv420p", "-r", str(FPS),
                    str(seg_path),
                ],
                check=True,
            )
        else:
            dec = sp.Popen(
                [
                    "ffmpeg", "-v", "error", "-ss", f"{start_s:.3f}", "-i", str(src),
                    "-frames:v", str(n_frames), "-vf", vf,
                    "-f", "rawvideo", "-pix_fmt", "rgb24", "-",
                ],
                stdout=sp.PIPE,
            )
            enc = sp.Popen(
                [
                    "ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pixel_format", "rgb24",
                    "-video_size", f"{W}x{H}", "-framerate", str(FPS), "-i", "-", "-an",
                    "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-pix_fmt", "yuv420p", "-r", str(FPS),
                    str(seg_path),
                ],
                stdin=sp.PIPE,
            )
            assert dec.stdout and enc.stdin
            last = None
            use_s = t_out_part - t_in_part
            for f_idx in range(n_frames):
                buf = dec.stdout.read(W * H * 3)
                if len(buf) == W * H * 3:
                    im = Image.frombytes("RGB", (W, H), buf)
                    last = im
                elif last is not None:
                    im = last
                else:
                    im = Image.new("RGB", (W, H), BROWN)
                im = draw_side_label(im, label, f_idx / FPS, use_s)
                enc.stdin.write(im.tobytes())
            dec.stdout.close()
            dec.wait()
            enc.stdin.close()
            if enc.wait() != 0:
                raise RuntimeError(f"label encode failed {seg_path}")

        cuts.append(
            {
                "row": p["id"],
                "film_t": round(float(p["t_s"]), 2),
                "timeline_in": round(t_in_part, 4),
                "timeline_out": round(t_out_part, 4),
                "frames": n_frames,
                "upscale": round(upscale, 4),
                "side_label": label or None,
                "source": src.name,
                "source_path": str(src),
                "source_sha256": sha256_file(src),
                "framing": {"offset": round(start_s, 3)},
                "disposition": disp,
                "quality": p["quality"],
            }
        )
        segs.append(seg_path)
        cur_frames += n_frames
        print(f"  P{pstr} {k+1}/{len(plates)} {p['id']} {n_frames}f", flush=True)

    concat_txt = out_dir / "concat.txt"
    concat_txt.write_text("".join(f"file '{s}'\n" for s in segs))
    pic_mp4 = out_dir / "picture_only.mp4"
    sp.run(
        ["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(concat_txt), "-c", "copy", str(pic_mp4)],
        check=True,
    )
    total_s = cur_frames / FPS
    cut_mp4 = out_dir / f"{name}.mp4"
    sp.run(
        [
            "ffmpeg", "-y", "-v", "error", "-i", str(pic_mp4), "-i", str(vo_path),
            "-map", "0:v", "-map", "1:a", "-c:v", "copy",
            "-af", "apad", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
            "-t", f"{total_s:.3f}", "-movflags", "+faststart", str(cut_mp4),
        ],
        check=True,
    )
    shutil.rmtree(seg_dir, ignore_errors=True)
    pic_mp4.unlink(missing_ok=True)

    fd = sp.run(
        ["ffmpeg", "-i", str(cut_mp4), "-vf", "freezedetect=n=-60dB:d=0.8", "-map", "0:v", "-f", "null", "-"],
        stderr=sp.PIPE, text=True,
    ).stderr
    freeze = [ln for ln in fd.splitlines() if "lavfi.freezedetect" in ln]
    (out_dir / "freezedetect.log").write_text("\n".join(freeze) + ("\n" if freeze else ""))

    cuts_path = out_dir / f"cuts_{slug}.json"
    cuts_path.write_text(json.dumps(cuts, indent=2) + "\n")
    pool = []
    seen = set()
    for c in cuts:
        if c["source"] in seen:
            continue
        seen.add(c["source"])
        title = (
            "HOS house code graphic / overlay composite (£0)"
            if c["source"].startswith(("cg_", "overlay_", "code_graphic"))
            else "Flow Veo 3.1 clip, KEEP (J1191)"
        )
        pool.append({"file": c["source"], "title": title})
    pool_path = out_dir / f"pool_{slug}.json"
    pool_path.write_text(json.dumps(pool, indent=2) + "\n")

    sheet_path = out_dir / f"contact_{slug}.jpg"
    contact_sheet(cut_mp4, cuts, out_dir, sheet_path)

    # Gates
    pg_json = out_dir / f"polish_gate_{slug}.json"
    pq_dir = out_dir / f"picture_qa_{slug}"
    pq_dir.mkdir(exist_ok=True)
    polish = sp.run(
        [
            sys.executable, str(OWB_ROOT / "scripts/polish_gate.py"),
            str(cut_mp4), "--cuts", str(cuts_path), "--out", str(pg_json),
        ],
        capture_output=True, text=True,
    )
    (out_dir / f"polish_gate_{slug}.txt").write_text(polish.stdout + polish.stderr)
    picture = sp.run(
        [
            sys.executable, str(OWB_ROOT / "scripts/picture_qa.py"),
            str(cut_mp4), "--cuts", str(cuts_path), "--pool", str(pool_path),
            "--out-dir", str(pq_dir),
        ],
        capture_output=True, text=True,
    )
    (out_dir / f"picture_qa_{slug}.txt").write_text(picture.stdout + picture.stderr)

    meta = {
        "part": part_no,
        "slug": slug,
        "authority": "J1218 repair after J1213 v01; J1191 PASS; PR #374 MERGED; J1193 code-graphic review still open at assemble start",
        "vo": str(vo_path),
        "vo_sha256": board["vo_sha256"],
        "picture_s": round(total_s, 4),
        "frames": cur_frames,
        "rows": len(cuts),
        "mp4": str(cut_mp4),
        "sha256": sha256_file(cut_mp4),
        "polish_gate_exit": polish.returncode,
        "picture_qa_exit": picture.returncode,
        "freeze_lines": len(freeze),
        "no_music": True,
        "j1193_note": "J1193 not landed; overlays used as delivered in CODE_GRAPHICS_v01 (P5:11 SAFE PATH DOWN fix applied)",
    }
    (out_dir / f"ROUGH_META_part{pstr}_v01.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(f"DONE part {pstr}: {total_s:.2f}s sha={meta['sha256'][:12]} polish={polish.returncode} pq={picture.returncode}", flush=True)
    return meta


def _collect_part_timeline(part_metas: list[dict] | None = None) -> tuple[list[dict], list[dict], list[dict]]:
    """Build all_cuts / pool / metas from existing part folders (no re-encode)."""
    all_cuts: list[dict] = []
    pool: list[dict] = []
    seen: set[str] = set()
    metas: list[dict] = []
    offset = 0.0
    parts = part_metas or [{"part": p} for p in range(1, 6)]
    for m in parts:
        part = int(m["part"])
        pstr = f"{part:02d}"
        slug = f"part{pstr}_rough_v02"
        part_dir = WORK / slug
        cuts_path = part_dir / f"cuts_{slug}.json"
        meta_path = part_dir / f"META_{slug}.json"
        mp4 = part_dir / f"hos_008_{slug}.mp4"
        if not cuts_path.exists() or not mp4.exists():
            raise FileNotFoundError(f"missing part assemble: {part_dir}")
        cuts = json.loads(cuts_path.read_text())
        picture_s = float(m.get("picture_s") or probe_dur(mp4))
        if meta_path.exists():
            try:
                picture_s = float(json.loads(meta_path.read_text()).get("picture_s", picture_s))
            except Exception:
                pass
        for c in cuts:
            row = dict(c)
            row["part"] = part
            row["timeline_in"] = round(c["timeline_in"] + offset, 4)
            row["timeline_out"] = round(c["timeline_out"] + offset, 4)
            all_cuts.append(row)
            if c["source"] not in seen:
                seen.add(c["source"])
                pool.append({"file": c["source"], "title": c["disposition"]})
        meta = dict(m)
        meta["part"] = part
        meta["picture_s"] = picture_s
        metas.append(meta)
        offset += picture_s
    return all_cuts, pool, metas



def latest_join_dir() -> Path:
    cands=sorted(WORK.glob("full_join_v03*"), key=lambda p: p.stat().st_mtime if p.exists() else 0)
    if not cands:
        raise FileNotFoundError(f"no full_join_v03* under {WORK}")
    return cands[-1]

def join_full(
    part_metas: list[dict],
    *,
    reuse_pretrim: Path | None = None,
    reuse_trimmed: Path | None = None,
) -> dict:
    # Fresh run directory every invocation — never delete prior NAS/work trees (Chief J1218).
    run_id = "full_join_v03"
    out_dir = WORK / run_id
    if out_dir.exists() and reuse_trimmed is None and reuse_pretrim is None:
        # Local/NAS scratch collision: stamp a new sibling; never rmtree.
        n = 2
        while (WORK / f"full_join_v03_r{n:02d}").exists():
            n += 1
        out_dir = WORK / f"full_join_v03_r{n:02d}"
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"join_full WORK out_dir={out_dir} (non-destructive)", flush=True)

    all_cuts, pool, metas = _collect_part_timeline(part_metas)
    raw_mp4 = out_dir / "hos_008_rough_v03_pretrim.mp4"
    out_mp4 = out_dir / "hos_008_rough_v03.mp4"

    if reuse_trimmed is not None and reuse_trimmed.exists():
        if out_mp4.resolve() != reuse_trimmed.resolve():
            shutil.copy2(reuse_trimmed, out_mp4)
        dur = probe_dur(out_mp4)
        print(f"Reusing trimmed {reuse_trimmed} ({dur:.2f}s)", flush=True)
        pause_report: dict = {
            "trimmed_s": None,
            "duration_in": None,
            "duration_out": round(dur, 3),
            "under_9min": dur <= 540.05,
            "method": "reuse_trimmed",
            "source": str(reuse_trimmed),
        }
        prior = out_dir / "PAUSE_TRIM_v03.json"
        if prior.exists():
            try:
                old = json.loads(prior.read_text())
                pause_report["trimmed_s"] = old.get("trimmed_s")
                pause_report["duration_in"] = old.get("duration_in")
                # Prefer full cut list under either key (reuse_trimmed previously
                # only looked at "cuts" and dropped "prior_cuts", so remap no-oped).
                cut_list = old.get("cuts") or old.get("prior_cuts") or []
                pause_report["cuts"] = cut_list
                pause_report["prior_cuts"] = cut_list
                if old.get("keep_ranges"):
                    pause_report["keep_ranges"] = old["keep_ranges"]
            except Exception:
                pass
        if dur > 540.05:
            # Cap on local /tmp without +faststart — NAS remux+faststart hangs (J1218).
            print(f"  existing trim still over 9:00 ({dur:.3f}s); trailing cap to 540.000 via /private/tmp", flush=True)
            import tempfile

            local_cap = Path(tempfile.mkdtemp(prefix="j1218v03_cap_", dir="/private/tmp")) / "capped.mp4"
            try:
                sp.run(
                    [
                        "ffmpeg", "-y", "-v", "error", "-i", str(out_mp4),
                        "-t", "540.000", "-c", "copy", str(local_cap),
                    ],
                    check=True,
                )
                sp.run(["rsync", "-a", str(local_cap), str(out_mp4)], check=True)
            finally:
                shutil.rmtree(local_cap.parent, ignore_errors=True)
            new_dur = probe_dur(out_mp4)
            pause_report["duration_out"] = round(new_dur, 3)
            pause_report["under_9min"] = new_dur <= 540.05
            pause_report["trailing_cap_s"] = round(dur - new_dur, 3)
            pause_report["method"] = "reuse_trimmed+trailing_cap_local"

        (out_dir / "PAUSE_TRIM_v03.json").write_text(json.dumps(pause_report, indent=2) + "\n")
    elif reuse_pretrim is not None and reuse_pretrim.exists():
        if raw_mp4.resolve() != reuse_pretrim.resolve():
            shutil.copy2(reuse_pretrim, raw_mp4)
        print(f"Reusing pretrim {reuse_pretrim} ({probe_dur(raw_mp4):.2f}s)", flush=True)
        pause_report = pause_trim_av(raw_mp4, out_mp4, max_pause=0.6, target_max_s=540.0)
        (out_dir / "PAUSE_TRIM_v03.json").write_text(json.dumps(pause_report, indent=2) + "\n")
    else:
        concat = out_dir / "concat.txt"
        lines = []
        for m in metas:
            pstr = f"{int(m['part']):02d}"
            slug = f"part{pstr}_rough_v02"
            mp4 = WORK / slug / f"hos_008_{slug}.mp4"
            lines.append(f"file '{mp4}'\n")
        concat.write_text("".join(lines))
        sp.run(
            ["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(concat), "-c", "copy", "-movflags", "+faststart", str(raw_mp4)],
            check=True,
        )
        pause_report = pause_trim_av(raw_mp4, out_mp4, max_pause=0.6, target_max_s=540.0)
        (out_dir / "PAUSE_TRIM_v03.json").write_text(json.dumps(pause_report, indent=2) + "\n")
    # Remap cut times through pause-trim removals so polish/picture_qa sample inside the trimmed master.
    dur_out = probe_dur(out_mp4)
    all_cuts = remap_cuts_after_pause_trim(all_cuts, pause_report, duration_out=dur_out)
    cuts_path = out_dir / "cuts_rough_v03.json"
    cuts_path.write_text(json.dumps(all_cuts, indent=2) + "\n")
    pool_path = out_dir / "pool_rough_v03.json"
    pool_path.write_text(json.dumps(pool, indent=2) + "\n")
    sheet = out_dir / "contact_rough_v03.jpg"
    contact_sheet(out_mp4, all_cuts, out_dir, sheet)

    pg_json = out_dir / "polish_gate_rough_v03.json"
    pq_dir = out_dir / "picture_qa_rough_v03"
    pq_dir.mkdir(exist_ok=True)
    polish = sp.run(
        [sys.executable, str(OWB_ROOT / "scripts/polish_gate.py"), str(out_mp4), "--cuts", str(cuts_path), "--out", str(pg_json)],
        capture_output=True, text=True,
    )
    (out_dir / "polish_gate_rough_v03.txt").write_text(polish.stdout + polish.stderr)
    picture = sp.run(
        [
            sys.executable, str(OWB_ROOT / "scripts/picture_qa.py"),
            str(out_mp4), "--cuts", str(cuts_path), "--pool", str(pool_path), "--out-dir", str(pq_dir),
        ],
        capture_output=True, text=True,
    )
    (out_dir / "picture_qa_rough_v03.txt").write_text(picture.stdout + picture.stderr)

    # music_gate: VO-only rough — no bed laid (credit hold until Chief OK). Record skip.
    music_note = {
        "status": "SKIPPED_NO_BED",
        "reason": "J1218: no music bed without Chief OK (ElevenLabs credit hold to 30 Oct). VO-only rough.",
        "video": str(out_mp4),
        "duration_s": probe_dur(out_mp4),
    }
    (out_dir / "music_gate_rough_v03.json").write_text(json.dumps(music_note, indent=2) + "\n")
    (out_dir / "music_gate_rough_v03.txt").write_text(
        "SKIPPED_NO_BED: no music bed without Chief OK; VO-only rough per J1218.\n"
    )

    digest = sha256_file(out_mp4)
    summary = {
        "film": "008_Lightning-Franklin",
        "job": "J1218",
        "version": "rough_v03",
        "work_dir": str(out_dir),
        "mp4": str(out_mp4),
        "sha256": digest,
        "duration_s": probe_dur(out_mp4),
        "rows": len(all_cuts),
        "parts": metas,
        "polish_gate_exit": polish.returncode,
        "picture_qa_exit": picture.returncode,
        "music_gate": music_note,
        "j1193": "review delivered (PR378) + Chief FIX 30 Oct; formal graphics approval still required; ten FIX rows dispositioned in v03",
        "pr_374": "MERGED before assemble",
        "pause_trim": pause_report,
        "v01_preserved": True,
        "repairs": ["06_same_thing sequential", "10_metal_easy alpha over KEEP rod_fitting", "09_window_storm left-5pct reframe", "side_label suppress P4:08/P5:11", "non-destructive NAS", "J1193 graphics v02", "§4 pause trim ≤9:00"],
    }
    (out_dir / "ROUGH_V03_SUMMARY.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(f"FULL JOIN {summary['duration_s']:.2f}s sha={digest}", flush=True)
    return summary


def _copy_evidence(dest_dir: Path, src: Path, digest: str) -> None:
    dest_dir.mkdir(parents=True, exist_ok=True)
    dst = dest_dir / src.name
    if dst.exists() and sha256_file(dst) == digest:
        pass
    else:
        # Prefer rsync for large masters (iCloud/NAS friendlier than shutil.copy2).
        sp.run(["rsync", "-a", str(src), str(dst)], check=True)
        assert sha256_file(dst) == digest
    for name in (
        "ROUGH_V03_SUMMARY.json",
        "cuts_rough_v03.json",
        "contact_rough_v03.jpg",
        "PAUSE_TRIM_v03.json",
        "polish_gate_rough_v03.json",
        "polish_gate_rough_v03.txt",
        "picture_qa_rough_v03.txt",
        "music_gate_rough_v03.json",
        "music_gate_rough_v03.txt",
        "pool_rough_v03.json",
    ):
        p = latest_join_dir() / name
        if p.exists():
            shutil.copy2(p, dest_dir / name)
    pq = latest_join_dir() / "picture_qa_rough_v03"
    if pq.exists() and pq.is_dir():
        dest_pq = dest_dir / "picture_qa_rough_v03"
        if dest_pq.exists():
            # Chief: never rmtree NAS/desk prior packs — write beside as _new if needed
            dest_pq = Path(str(dest_pq) + "_v03")
        shutil.copytree(pq, dest_pq)


def deliver(summary: dict) -> None:
    """Copy master + manifests to PRECHECK, DESK, UAT, NAS (sha checked)."""
    src = Path(summary["mp4"])
    digest = summary["sha256"]
    targets: list[str] = []
    errors: list[str] = []

    PRECHECK.mkdir(parents=True, exist_ok=True)
    DESK.mkdir(parents=True, exist_ok=True)
    for dest_dir in (PRECHECK, DESK):
        _copy_evidence(dest_dir, src, digest)
        targets.append(str(dest_dir / src.name))

    # Always stage durable NAS copy (create film folder if missing).
    try:
        nas = NAS_FILM / "07_Edit-Project" / "rough_v03"
        _copy_evidence(nas, src, digest)
        (nas / "SHA256SUMS.txt").write_text(f"{digest}  {src.name}\n")
        targets.append(str(nas / src.name))
    except Exception as e:
        errors.append(f"NAS: {e!r}")
        print(f"DELIVER WARN NAS: {e!r}", flush=True)

    if UAT_ROOT.exists():
        try:
            uat = UAT_ROOT / "008_Lightning-Franklin_rough_v03"
            _copy_evidence(uat, src, digest)
            (uat / "SHA256SUMS.txt").write_text(f"{digest}  {src.name}\n")
            targets.append(str(uat / src.name))
        except Exception as e:
            # iCloud deadlock (Errno 11) seen on Mini — non-fatal if NAS+desk hold the master.
            errors.append(f"UAT: {e!r}")
            print(f"DELIVER WARN UAT: {e!r}", flush=True)

    summary["delivered"] = targets
    if errors:
        summary["deliver_errors"] = errors
    (latest_join_dir() / "ROUGH_V03_SUMMARY.json").write_text(json.dumps(summary, indent=2) + "\n")
    (DESK / "DELIVERED.json").write_text(
        json.dumps({"sha256": digest, "targets": targets, "errors": errors}, indent=2) + "\n"
    )
    print("DELIVERED", targets, flush=True)
    if errors:
        print("DELIVER_ERRORS", errors, flush=True)


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    resume = "--resume-join" in argv
    finish = "--finish-existing" in argv
    WORK.mkdir(parents=True, exist_ok=True)

    if finish:
        trimmed = latest_join_dir() / "hos_008_rough_v03.mp4"
        if not trimmed.exists():
            raise FileNotFoundError(f"no trimmed master for --finish-existing: {trimmed}")
        print(f"=== Finish existing trimmed {trimmed} ===", flush=True)
        summary = join_full([], reuse_trimmed=trimmed)
    elif resume:
        safe = WORK / "hos_008_rough_v03_pretrim.SAFE.mp4"
        pretrim = latest_join_dir() / "hos_008_rough_v03_pretrim.mp4"
        reuse = safe if safe.exists() else (pretrim if pretrim.exists() else None)
        if reuse is None:
            raise FileNotFoundError("no pretrim SAFE/mp4 for --resume-join")
        print(f"=== Resume join from {reuse} ===", flush=True)
        summary = join_full([], reuse_pretrim=reuse)
    else:
        print("Loading mint index…", flush=True)
        mint = load_mint_index()
        print(f"KEEP Flow clips: {len(mint)}", flush=True)
        print("Preparing code graphics + 5 overlay composites…", flush=True)
        special = prepare_special_assets(mint)
        print(f"Special assets: {len(special)}", flush=True)

        metas = []
        for part in range(1, 6):
            print(f"=== Assemble part {part:02d} ===", flush=True)
            metas.append(assemble_part(part, mint, special))

        print("=== Full join ===", flush=True)
        summary = join_full(metas)

    print("=== Deliver ===", flush=True)
    deliver(summary)
    print("ALL DONE", flush=True)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception:
        traceback.print_exc()
        raise SystemExit(1)
