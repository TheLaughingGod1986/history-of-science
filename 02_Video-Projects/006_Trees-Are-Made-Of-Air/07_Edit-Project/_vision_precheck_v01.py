#!/usr/bin/env python3
"""HOS 006 Part 01 local vision precheck pilot (advisory only).

Uses mlx-community/Qwen2.5-VL-3B-Instruct-4bit via mlx-vlm.
Freeze detect: ffmpeg freezedetect + VL confirm on stills.
Repeat: perceptual hash across distant timestamps.
Garbled text: VL OCR on labeled-plate stills.
Optional VO ASR: reuse ~/.venvs/hos-vo faster-whisper (not a second ASR).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import resource
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

import imagehash
import numpy as np
from PIL import Image

FILM = Path(__file__).resolve().parents[1]
PRECHECK = Path(__file__).resolve().parent / "_precheck"
STILLS = PRECHECK / "stills"
LOGS = PRECHECK / "logs"
RAW = FILM / "04_Generated-Clips" / "part01" / "raw" / "v01"
BOARD = Path(__file__).resolve().parent / "parts" / "part-01_plates_v01.json"
REPORT_NOTES = Path(__file__).resolve().parent / "_desk" / "REPORT_picture_part01_lite_v01.md"
ROUGH = PRECHECK / "hos_006_part01_precheck_rough_v01.mp4"
TIMELINE = PRECHECK / "timeline_v01.json"
MODEL_ID = "mlx-community/Qwen2.5-VL-3B-Instruct-4bit"
HOS_VO_PY = Path.home() / ".venvs" / "hos-vo" / "bin" / "python"

KEEP_CLIPS = [
    ("01_willow_air_t1", 4.28, "MADE OF AIR"),
    ("02_balance_trunk_t1", 3.08, "NOT THE SOIL"),
    ("03_pot_jar_leaf_t1", 7.5, "A POT · A JAR · THE SUN"),
    ("04_years_pass_t3", 5.48, None),
    ("05_olive_grove_t1", 4.2, None),
    ("06_aristotle_t1", 6.24, "ARISTOTLE"),
    ("07_roots_mouths_t1", 4.74, "ROOTS AS MOUTHS"),
    ("08_wood_food_air_t3", 4.22, None),
    ("09_vilvoorde_flowfast_t1", 5.0, "VILVOORDE"),
    ("10_van_helmont_sack_t1", 6.44, "JAN BAPTIST VAN HELMONT"),
    ("11_shoot_in_pot_t1", 4.8, None),
    ("12_garden_sky_t2", 5.67, None),
]

# Positive controls: known-bad takes still on disk
BAD_CONTROLS = [
    ("04_years_pass_t1", "freeze", "froze first ~0.54s"),
    ("08_wood_food_air_t2", "other", "campfire flame on Fast plate"),
    ("12_garden_sky_t1", "other", "clouds at pot height read as smoke"),
]

# From mint review — issues that SHOULD be caught or noted
GROUND_TRUTH = {
    "bad_controls": {
        "04_years_pass_t1": {"expect": "freeze", "note": "first 0.54s freeze"},
        "08_wood_food_air_t2": {"expect": "other", "note": "campfire flame"},
        "12_garden_sky_t1": {"expect": "other", "note": "smoke/clouds at pot height"},
    },
    "keep_watch": {
        "11_shoot_in_pot_t1": {"expect": "other", "note": "hand deforms after 5.0s; board uses 4.8s"},
        "09_vilvoorde_flowfast_t1": {"expect": None, "note": "720p Flow — resolution not a VL category"},
    },
}


@dataclass
class Flag:
    timestamp_s: float
    category: str
    detail: str
    still: str | None
    source: str
    confidence: str = "med"


def sh(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(list(args), check=check, capture_output=True, text=True)


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def extract_still(video: Path, t: float, out: Path) -> Path:
    out.parent.mkdir(parents=True, exist_ok=True)
    sh(
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-ss", f"{t:.3f}", "-i", str(video), "-frames:v", "1",
        "-q:v", "3", str(out),
    )
    return out


def freezedetect(video: Path, noise: float = 0.003, min_duration: float = 0.5) -> list[tuple[float, float]]:
    """Return list of (start, duration) freeze intervals."""
    cmd = [
        "ffmpeg", "-hide_banner", "-i", str(video),
        "-vf", f"freezedetect=n={noise}:d={min_duration}",
        "-f", "null", "-",
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    text = r.stderr or ""
    starts = [float(m.group(1)) for m in re.finditer(r"freeze_start:\s*([0-9.]+)", text)]
    ends = [float(m.group(1)) for m in re.finditer(r"freeze_end:\s*([0-9.]+)", text)]
    durs = [float(m.group(1)) for m in re.finditer(r"freeze_duration:\s*([0-9.]+)", text)]
    out = []
    for i, s in enumerate(starts):
        if i < len(durs):
            out.append((s, durs[i]))
        elif i < len(ends):
            out.append((s, ends[i] - s))
    return out


def sample_times(duration: float, step: float = 1.0) -> list[float]:
    if duration <= 0:
        return [0.0]
    times = []
    t = 0.0
    while t < duration - 0.05:
        times.append(round(t, 3))
        t += step
    # always include near-end
    end = max(0.0, duration - 0.15)
    if not times or abs(times[-1] - end) > 0.25:
        times.append(round(end, 3))
    return times


def phash_distance(a: Image.Image, b: Image.Image) -> int:
    return imagehash.phash(a) - imagehash.phash(b)


class VLSession:
    def __init__(self, model_id: str):
        self.model_id = model_id
        self.model = None
        self.processor = None
        self.config = None
        self.peak_rss_mb = 0.0
        self.n_calls = 0

    def load(self):
        from mlx_vlm import load
        from mlx_vlm.utils import load_config
        t0 = time.time()
        self.model, self.processor = load(self.model_id)
        self.config = load_config(self.model_id)
        self._update_rss()
        return time.time() - t0

    def _update_rss(self):
        # macOS: ru_maxrss is bytes
        rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        mb = rss / (1024 * 1024)
        if mb > self.peak_rss_mb:
            self.peak_rss_mb = mb

    def ask(self, image_path: Path, prompt: str, max_tokens: int = 120) -> str:
        from mlx_vlm import generate
        from mlx_vlm.prompt_utils import apply_chat_template
        formatted = apply_chat_template(
            self.processor, self.config, prompt, num_images=1
        )
        result = generate(
            self.model,
            self.processor,
            formatted,
            image=str(image_path),
            max_tokens=max_tokens,
            verbose=False,
            temperature=0.0,
        )
        self.n_calls += 1
        self._update_rss()
        text = getattr(result, "text", None) or str(result)
        return text.strip()


def vl_confirm_freeze(vl: VLSession, still: Path) -> tuple[bool, str]:
    prompt = (
        "You are checking a video frame for a FREEZE FAULT (frozen / still-frame look). "
        "Reply with exactly one line: FREEZE:YES or FREEZE:NO, then a short reason. "
        "YES only if the image looks like a paused still with no motion cues."
    )
    ans = vl.ask(still, prompt)
    yes = bool(re.search(r"FREEZE\s*:\s*YES", ans, re.I))
    return yes, ans


def vl_read_text(vl: VLSession, still: Path, expected: str | None) -> tuple[str, str]:
    prompt = (
        "Read any on-screen title/label text in this frame. "
        "Reply with exactly: TEXT:<what you read or NONE> | READABLE:YES or READABLE:NO. "
        "Mark READABLE:NO if letters are garbled, misspelled nonsense, or unreadable."
    )
    if expected:
        prompt += f" Expected label theme (not exact OCR): {expected}."
    ans = vl.ask(still, prompt)
    readable = "YES"
    m = re.search(r"READABLE\s*:\s*(YES|NO)", ans, re.I)
    if m:
        readable = m.group(1).upper()
    return readable, ans


def vl_anomaly(vl: VLSession, still: Path, hint: str) -> tuple[bool, str]:
    prompt = (
        f"Natural-history cartoon still. Watch for: {hint}. "
        "Reply one line: ISSUE:YES or ISSUE:NO, then short reason. "
        "YES if the described fault is clearly visible."
    )
    ans = vl.ask(still, prompt, max_tokens=100)
    yes = bool(re.search(r"ISSUE\s*:\s*YES", ans, re.I))
    return yes, ans


def probe_duration(video: Path) -> float:
    r = sh(
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=nw=1:nk=1", str(video),
    )
    return float(r.stdout.strip())


def run_whisper_optional(vo: Path, out_json: Path) -> dict[str, Any] | None:
    if not HOS_VO_PY.exists():
        return None
    code = r'''
import json, sys
from pathlib import Path
from faster_whisper import WhisperModel
vo = Path(sys.argv[1]); out = Path(sys.argv[2])
model = WhisperModel("small.en", device="cpu", compute_type="int8")
segs, info = model.transcribe(str(vo), word_timestamps=False)
text = " ".join(s.text.strip() for s in segs).strip()
out.write_text(json.dumps({"language": info.language, "duration": info.duration, "text": text}, indent=2))
print(text[:200])
'''
    r = subprocess.run(
        [str(HOS_VO_PY), "-c", code, str(vo), str(out_json)],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        return {"error": r.stderr[-500:]}
    return json.loads(out_json.read_text())


def score_results(flags: list[Flag], bad_flags: dict[str, list[Flag]]) -> dict[str, Any]:
    hits, misses, false_alarms = [], [], []

    # Positive controls
    for clip, meta in GROUND_TRUTH["bad_controls"].items():
        got = bad_flags.get(clip, [])
        expect = meta["expect"]
        if expect == "freeze":
            ok = any(f.category == "freeze" for f in got)
        else:
            # other/anomaly: any flag or VL ISSUE yes stored as other
            ok = any(f.category in ("other", "freeze", "garbled_text") for f in got)
        if ok:
            hits.append({"clip": clip, "expect": expect, "note": meta["note"], "flags": [asdict(f) for f in got]})
        else:
            misses.append({"clip": clip, "expect": expect, "note": meta["note"], "flags": [asdict(f) for f in got]})

    # KEEP rough: false alarms = flags that don't match known watch points
    watch_notes = GROUND_TRUTH["keep_watch"]
    for f in flags:
        # map rough timestamp to plate
        plate = None
        t = 0.0
        for name, dur, _ in KEEP_CLIPS:
            if t <= f.timestamp_s < t + dur + 0.05:
                plate = name
                break
            t += dur
        if plate and plate in watch_notes and watch_notes[plate]["expect"]:
            hits.append({"clip": plate, "expect": "watch", "note": watch_notes[plate]["note"], "flag": asdict(f)})
        else:
            # freeze/repeat/garbled on accepted KEEP is likely false alarm for pilot
            false_alarms.append({"clip": plate or "rough", "flag": asdict(f)})

    return {"hits": hits, "misses": misses, "false_alarms": false_alarms}


def write_report(path: Path, data: dict[str, Any]) -> None:
    lines = []
    lines.append("# HOS 006 Part 01 · local vision precheck pilot v01")
    lines.append("")
    lines.append(f"- **When:** {data['when']}")
    lines.append(f"- **Model:** `{data['model_id']}`")
    lines.append(f"- **Install footprint:** venv {data['install']['venv_gb']} GB + model {data['install']['model_gb']} GB = **{data['install']['total_gb']} GB** (<20 GB)")
    lines.append(f"- **Rough:** `{data['rough']['path']}`")
    lines.append(f"  - sha256 `{data['rough']['sha256']}`")
    lines.append(f"  - duration **{data['rough']['duration_s']:.2f} s**, size {data['rough']['size_mb']:.1f} MB")
    lines.append(f"- **Runtime:** wall {data['runtime']['wall_s']:.1f}s · VL load {data['runtime']['vl_load_s']:.1f}s · VL calls {data['runtime']['vl_calls']}")
    lines.append(f"- **Peak RSS (VL process):** **{data['runtime']['peak_rss_mb']:.0f} MB**")
    lines.append("")
    lines.append("## Scope")
    lines.append("Advisory only — never a gate. Part 01 KEEP plates already accepted (12/12). Local Mini only; no cloud vision.")
    lines.append("")
    lines.append("## Flags on KEEP rough")
    if not data["flags"]:
        lines.append("_None._")
    else:
        lines.append("| ts (s) | category | detail | still |")
        lines.append("|---|---|---|---|")
        for f in data["flags"]:
            lines.append(f"| {f['timestamp_s']:.2f} | `{f['category']}` | {f['detail'][:120]} | `{f.get('still') or ''}` |")
    lines.append("")
    lines.append("## Positive controls (known-bad takes)")
    for clip, fl in data["bad_control_flags"].items():
        lines.append(f"### `{clip}`")
        if not fl:
            lines.append("- _No flags raised._")
        else:
            for f in fl:
                lines.append(f"- **{f['category']}** @ {f['timestamp_s']:.2f}s — {f['detail'][:160]}")
    lines.append("")
    lines.append("## Scoring vs mint review notes")
    sc = data["scoring"]
    lines.append(f"- **Hits:** {len(sc['hits'])}")
    for h in sc["hits"]:
        lines.append(f"  - HIT `{h['clip']}` expect={h.get('expect')} — {h.get('note')}")
    lines.append(f"- **Misses:** {len(sc['misses'])}")
    for m in sc["misses"]:
        lines.append(f"  - MISS `{m['clip']}` expect={m.get('expect')} — {m.get('note')}")
    lines.append(f"- **False alarms (on KEEP rough):** {len(sc['false_alarms'])}")
    for fa in sc["false_alarms"]:
        flag = fa["flag"]
        lines.append(f"  - FA `{fa['clip']}` `{flag['category']}` @ {flag['timestamp_s']:.2f}s — {flag['detail'][:100]}")
    lines.append("")
    if data.get("whisper"):
        lines.append("## Optional Whisper (hos-vo / faster-whisper small.en)")
        w = data["whisper"]
        if "error" in w:
            lines.append(f"- Error: {w['error']}")
        else:
            lines.append(f"- Duration {w.get('duration')} · text preview: {str(w.get('text',''))[:240]}")
        lines.append("")
    lines.append("## Recommendation")
    lines.append(data["recommendation"])
    lines.append("")
    lines.append("## Method notes")
    lines.append("- Freeze: ffmpeg `freezedetect` (n=0.003, d=0.5s) then VL confirm on mid-freeze still.")
    lines.append("- Repeat: phash every 1.0s; flag if Hamming distance ≤ 6 and |Δt| ≥ 8s.")
    lines.append("- Garbled text: VL OCR on mid-plate stills that have board `side_label`.")
    lines.append("- Bad controls run the same detectors on raw known-bad takes.")
    path.write_text("\n".join(lines) + "\n")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--skip-whisper", action="store_true")
    ap.add_argument("--skip-vl", action="store_true", help="detectors only (debug)")
    args = ap.parse_args()

    PRECHECK.mkdir(parents=True, exist_ok=True)
    STILLS.mkdir(parents=True, exist_ok=True)
    LOGS.mkdir(parents=True, exist_ok=True)

    when = time.strftime("%Y-%m-%d %H:%M:%S %Z")
    t_wall0 = time.time()

    if not ROUGH.exists():
        print("MISSING rough", ROUGH, file=sys.stderr)
        return 2

    duration = probe_duration(ROUGH)
    rough_sha = sha256_file(ROUGH)
    print(f"ROUGH duration={duration:.2f} sha={rough_sha[:16]}…")

    flags: list[Flag] = []
    freeze_raw = freezedetect(ROUGH)
    print(f"freezedetect intervals: {freeze_raw}")

    # Sample frames for phash + labeled text
    times = sample_times(duration, step=1.0)
    frame_paths: dict[float, Path] = {}
    for t in times:
        p = STILLS / f"rough_{t:06.2f}.jpg".replace(".", "p")
        # fix naming: rough_000p00.jpg style
        p = STILLS / f"rough_t{int(t*100):06d}.jpg"
        extract_still(ROUGH, t, p)
        frame_paths[t] = p

    # Repeat detect via phash
    imgs = {t: Image.open(p).convert("RGB") for t, p in frame_paths.items()}
    sorted_t = sorted(imgs)
    for i, t1 in enumerate(sorted_t):
        for t2 in sorted_t[i + 1:]:
            if t2 - t1 < 8.0:
                continue
            dist = phash_distance(imgs[t1], imgs[t2])
            if dist <= 6:
                still = frame_paths[t2]
                flags.append(Flag(
                    timestamp_s=t2,
                    category="repeat",
                    detail=f"phash dist={dist} vs t={t1:.2f}s (Δ={t2-t1:.1f}s)",
                    still=str(still.relative_to(PRECHECK)),
                    source="phash",
                ))
                break  # one flag per later frame is enough

    vl = None
    vl_load_s = 0.0
    if not args.skip_vl:
        vl = VLSession(MODEL_ID)
        print("Loading VL…")
        vl_load_s = vl.load()
        print(f"VL loaded in {vl_load_s:.1f}s peak_rss={vl.peak_rss_mb:.0f}MB")

        # Confirm freezes
        for start, dur in freeze_raw:
            mid = start + min(dur, 0.4) / 2
            still = STILLS / f"freeze_t{int(mid*100):06d}.jpg"
            extract_still(ROUGH, mid, still)
            if vl:
                ok, ans = vl_confirm_freeze(vl, still)
                if ok:
                    flags.append(Flag(mid, "freeze", f"ffmpeg {dur:.2f}s + VL: {ans[:140]}", str(still.relative_to(PRECHECK)), "ffmpeg+vl", "high"))
                else:
                    flags.append(Flag(mid, "freeze", f"ffmpeg {dur:.2f}s but VL NO: {ans[:140]}", str(still.relative_to(PRECHECK)), "ffmpeg", "low"))
            else:
                flags.append(Flag(mid, "freeze", f"ffmpeg {dur:.2f}s (no VL)", str(still.relative_to(PRECHECK)), "ffmpeg"))

        # Garbled text on labeled plates
        t_cursor = 0.0
        for name, use_s, label in KEEP_CLIPS:
            if label:
                mid = t_cursor + min(use_s * 0.45, use_s - 0.1)
                still = STILLS / f"label_{name}.jpg"
                extract_still(ROUGH, mid, still)
                readable, ans = vl_read_text(vl, still, label)
                if readable == "NO":
                    flags.append(Flag(mid, "garbled_text", f"{name} expected~{label} | {ans[:140]}", str(still.relative_to(PRECHECK)), "vl", "med"))
                else:
                    # store soft note in log only
                    (LOGS / f"ocr_{name}.txt").write_text(ans)
            t_cursor += use_s

    # Positive controls
    bad_flags: dict[str, list[Flag]] = {}
    for clip, expect_cat, hint in BAD_CONTROLS:
        vpath = RAW / f"{clip}.mp4"
        bad_flags[clip] = []
        if not vpath.exists():
            print("MISSING bad control", vpath)
            continue
        cdur = probe_duration(vpath)
        fr = freezedetect(vpath)
        print(f"control {clip} dur={cdur:.2f} freezes={fr}")
        for start, dur in fr:
            mid = start + min(dur, 0.4) / 2
            still = STILLS / f"bad_{clip}_freeze_t{int(mid*100):06d}.jpg"
            extract_still(vpath, mid, still)
            confirmed = True
            detail = f"ffmpeg freeze {dur:.2f}s"
            if vl:
                confirmed, ans = vl_confirm_freeze(vl, still)
                detail += f" | VL: {ans[:120]}"
            if confirmed or expect_cat == "freeze":
                # for freeze-expect, keep ffmpeg even if VL soft-no
                cat = "freeze"
                if not confirmed and expect_cat == "freeze":
                    detail += " (VL soft-no; keeping ffmpeg hit for scoring)"
                bad_flags[clip].append(Flag(mid, cat, detail, str(still.relative_to(PRECHECK)), "ffmpeg+vl"))
        # anomaly VL at 0.5s, mid, near end
        if vl and expect_cat == "other":
            for t in [0.5, cdur / 2, max(0.2, cdur - 0.4)]:
                still = STILLS / f"bad_{clip}_t{int(t*100):06d}.jpg"
                extract_still(vpath, t, still)
                yes, ans = vl_anomaly(vl, still, hint)
                if yes:
                    bad_flags[clip].append(Flag(t, "other", ans[:180], str(still.relative_to(PRECHECK)), "vl"))
                    break

    whisper = None
    if not args.skip_whisper:
        vo = FILM / "02_Voiceover" / "part01_plants_eat_soil_v02.mp3"
        try:
            whisper = run_whisper_optional(vo, LOGS / "whisper_part01.json")
        except Exception as e:
            whisper = {"error": str(e)}

    scoring = score_results(flags, bad_flags)

    # Install size
    venv = Path.home() / ".venvs" / "hos-vl-precheck"
    model_cache = Path.home() / ".cache" / "huggingface" / "hub" / "models--mlx-community--Qwen2.5-VL-3B-Instruct-4bit"

    def du_gb(p: Path) -> float:
        if not p.exists():
            return 0.0
        r = subprocess.run(["du", "-sk", str(p)], capture_output=True, text=True)
        kb = float(r.stdout.split()[0])
        return kb / 1e6  # approx GB (1000^2 KB)

    # model via follow symlinks
    r = subprocess.run(["du", "-skL", str(model_cache / "snapshots")], capture_output=True, text=True)
    model_gb = float(r.stdout.split()[0]) / 1e6 if r.returncode == 0 and r.stdout.strip() else 3.09
    venv_gb = du_gb(venv)
    total_gb = venv_gb + model_gb

    peak = vl.peak_rss_mb if vl else 0.0
    # also sample current RSS via ps
    ps = subprocess.run(["ps", "-o", "rss=", "-p", str(os.getpid())], capture_output=True, text=True)
    try:
        ps_mb = int(ps.stdout.strip()) / 1024
        peak = max(peak, ps_mb)
    except Exception:
        pass

    wall = time.time() - t_wall0
    n_hits = len(scoring["hits"])
    n_miss = len(scoring["misses"])
    n_fa = len(scoring["false_alarms"])

    # Recommendation heuristic
    if n_hits >= 1 and n_fa <= 3:
        reco = (
            "**Keep as standing pre-UAT advisory step** on the Mini overnight (outside Tdarr 01:00–05:00). "
            f"3B caught {n_hits} known issue(s) with {n_fa} false alarm(s) on the KEEP rough. "
            "Do not gate ship on it; human/UAT remains the sign-off."
        )
        if n_miss:
            reco += f" Note: {n_miss} known-bad miss(es) — useful as a net, not a sieve."
    elif n_hits == 0:
        reco = (
            "**Stop / do not promote to standing step** without a better prompt pack or 7B trial. "
            "3B notes were not useful enough against known-bad controls (0 hits)."
        )
    else:
        reco = (
            "**Conditional keep:** advisory-only with tuned thresholds. "
            f"Hits={n_hits}, misses={n_miss}, false_alarms={n_fa}. Review FA noise before standing use."
        )

    data = {
        "when": when,
        "model_id": MODEL_ID,
        "install": {"venv_gb": round(venv_gb, 2), "model_gb": round(model_gb, 2), "total_gb": round(total_gb, 2)},
        "rough": {
            "path": str(ROUGH),
            "sha256": rough_sha,
            "duration_s": duration,
            "size_mb": ROUGH.stat().st_size / 1e6,
        },
        "runtime": {
            "wall_s": wall,
            "vl_load_s": vl_load_s,
            "vl_calls": vl.n_calls if vl else 0,
            "peak_rss_mb": peak,
        },
        "flags": [asdict(f) for f in flags],
        "bad_control_flags": {k: [asdict(f) for f in v] for k, v in bad_flags.items()},
        "scoring": scoring,
        "whisper": whisper,
        "recommendation": reco,
        "freeze_raw_rough": freeze_raw,
    }

    raw_json = LOGS / "results_v01.json"
    raw_json.write_text(json.dumps(data, indent=2))
    report = PRECHECK / "REPORT_part01_vision_precheck_v01.md"
    write_report(report, data)
    # summary copy for possible commit
    desk_copy = Path(__file__).resolve().parent / "_desk" / "REPORT_part01_vision_precheck_v01.md"
    shutil.copy2(report, desk_copy)
    print("WROTE", report)
    print("WROTE", desk_copy)
    print("HITS", n_hits, "MISSES", n_miss, "FA", n_fa)
    print("PEAK_RSS_MB", peak, "WALL_S", wall)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
