#!/usr/bin/env python3
"""Join HOS 004 passed Parts 01–05 → hos_004_full_join_v01.

Soft xfade+acrossfade (0.40s) between parts. P05 already carries the ~4s
cream-on-brown house end card; append a 20s cream hold for the Studio end
screen. No remint. No script text changes. Do not label KEEP/LOCKED.

Parents (hash-checked):
  01 v05 · 02 v01 · 03 v01 · 04 v02 · 05 v03
VO: locked v04 (already baked into each rough).
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
EXP = PROJ / "09_Final-Export"
EDIT = PROJ / "07_Edit-Project"
ICLOUD_DIR = (
    Path.home()
    / "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT"
    / "004_Whats-Really-Inside-An-Atom"
    / "09_Final-Export"
)
CREAM_PNG = PROJ / "04_Generated-Clips/part05/refs/hos_end_card_v01.png"
OUT = EXP / "hos_004_full_join_v01.mp4"
NOTES = EXP / "FULL_JOIN_V01_NOTES.md"
META = EDIT / "full_join_v01_land_meta.json"
WATCH = EDIT / "WATCH_full_join_v01.txt"

# Cream card already baked into P05 from board t_s 140.5
P05_CREAM_IN = 140.5
END_HOLD = 20.0
XFADE = 0.40

PARENTS = [
    {
        "id": "01",
        "name": "hos_004_part01_rough_v05.mp4",
        "sha": "71d7c70798c77ce2ecb02c37ad043fd98117a2209a84899236337fee8b952add",
        "chapter": "Cold open",
    },
    {
        "id": "02",
        "name": "hos_004_part02_rough_v01.mp4",
        "sha": "620ce51250028495a588f25967dddfaa9c6136dc4172c7b0ce1ee609f103f1d2",
        "chapter": "The Table That Broke Its Own Rule",
    },
    {
        "id": "03",
        "name": "hos_004_part03_rough_v01.mp4",
        "sha": "d62e0ed096ead8ec52666ca07476f973aeaae7635b70a16faaac45f14ec518e0",
        "chapter": "The Crumb Inside the Atom",
    },
    {
        "id": "04",
        "name": "hos_004_part04_rough_v02.mp4",
        "sha": "157feaef7bd21236aeafc3e953fe461fe2ee95896bb868d57357c9c1c2c1e1f5",
        "chapter": "The Shell That Bounced Back",
    },
    {
        "id": "05",
        "name": "hos_004_part05_rough_v03.mp4",
        "sha": "b391bff0dbe8a8ae0130adef4f7f3d7b79aca2cb34a934d9cf42d76e1d03363f",
        "chapter": "Counting With X-rays",
    },
]

ENC = [
    "-c:v", "libx264", "-pix_fmt", "yuv420p",
    "-profile:v", "high", "-level", "4.1",
    "-preset", "fast", "-crf", "18", "-r", "30",
    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
    "-movflags", "+faststart",
]


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def probe_dur(p: Path) -> float:
    r = subprocess.run(
        [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(p),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(r.stdout.strip())


def probe_streams(p: Path) -> dict:
    r = subprocess.run(
        [
            "ffprobe", "-v", "error",
            "-show_entries", "stream=codec_type,duration,width,height,r_frame_rate",
            "-of", "json", str(p),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(r.stdout)


def ff(*args: str) -> None:
    subprocess.run(
        ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *args],
        check=True,
    )


def fmt_tc(seconds: float) -> str:
    s = max(0.0, seconds)
    m = int(s // 60)
    rem = s - 60 * m
    return f"{m}:{rem:05.2f}"


def encode_part(src: Path, dest: Path, dur: float) -> None:
    ff(
        "-i", str(src),
        "-vf", "fps=30,scale=1920:1080:flags=lanczos,format=yuv420p,setsar=1",
        "-af", "aformat=sample_rates=48000:channel_layouts=stereo",
        "-t", f"{dur:.6f}",
        *ENC,
        str(dest),
    )


def encode_cream_hold(png: Path, dest: Path, hold: float) -> None:
    ff(
        "-loop", "1", "-i", str(png),
        "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
        "-vf", "fps=30,scale=1920:1080:flags=lanczos,format=yuv420p,setsar=1",
        "-t", f"{hold:.6f}",
        "-shortest",
        *ENC,
        str(dest),
    )


def main() -> None:
    if not CREAM_PNG.exists():
        raise SystemExit(f"STOP: missing cream card {CREAM_PNG}")

    paths: list[Path] = []
    durs: list[float] = []
    print("HASH CHECK", flush=True)
    for item in PARENTS:
        exp = EXP / item["name"]
        if not exp.exists():
            raise SystemExit(f"STOP: missing {exp}")
        got = sha256(exp)
        if got != item["sha"]:
            raise SystemExit(f"STOP: hash mismatch {item['name']}\n  want {item['sha']}\n  got  {got}")
        dur = probe_dur(exp)
        print(f"  OK {item['id']} {dur:.3f}s {got}", flush=True)
        paths.append(exp)
        durs.append(dur)

    work = Path(tempfile.mkdtemp(prefix="hos_004_join_v01_"))
    print(f"WORK {work}", flush=True)

    segs: list[Path] = []
    seg_durs: list[float] = []
    labels: list[str] = []

    for item, src, dur in zip(PARENTS, paths, durs):
        dest = work / f"p{item['id']}.mp4"
        print(f"ENCODE {item['id']}", flush=True)
        encode_part(src, dest, dur)
        segs.append(dest)
        seg_durs.append(probe_dur(dest))
        labels.append(f"p{item['id']}")

    cream = work / "cream_hold_20s.mp4"
    print(f"CREAM HOLD {END_HOLD:.1f}s", flush=True)
    encode_cream_hold(CREAM_PNG, cream, END_HOLD)
    segs.append(cream)
    seg_durs.append(probe_dur(cream))
    labels.append("cream_hold_20s")

    n = len(segs)
    # Soft joins between story parts only; hard-concat cream hold after P05
    # (identical cream → cream; avoids a fake dissolve on the end card).
    story_n = 5
    vchain: list[str] = []
    achain: list[str] = []
    running = 0.0
    for i in range(story_n - 1):
        running += seg_durs[i]
        off = running - (i + 1) * XFADE
        vin = "[0:v]" if i == 0 else f"[vx{i}]"
        ain = "[0:a]" if i == 0 else f"[ax{i}]"
        vout = f"vx{i+1}"
        aout = f"ax{i+1}"
        vchain.append(
            f"{vin}[{i+1}:v]xfade=transition=fade:duration={XFADE:.3f}:offset={off:.6f}[{vout}]"
        )
        achain.append(
            f"{ain}[{i+1}:a]acrossfade=d={XFADE:.3f}:c1=tri:c2=tri[{aout}]"
        )
        print(f"  JOIN {labels[i]} → {labels[i+1]}  offset={off:.3f}", flush=True)

    # concat story chain + cream hold
    fc = (
        ";".join(vchain + achain)
        + f";[vx{story_n-1}][{story_n}:v]concat=n=2:v=1:a=0[vout];"
        + f"[ax{story_n-1}][{story_n}:a]concat=n=2:v=0:a=1[aout]"
    )
    args: list[str] = []
    for p in segs:
        args += ["-i", str(p)]
    print("XFADE + CREAM HOLD", flush=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    tmp = work / "full_join_v01.mp4"
    ff(
        *args,
        "-filter_complex", fc,
        "-map", "[vout]", "-map", "[aout]",
        *ENC,
        str(tmp),
    )
    subprocess.run(["cp", "-f", str(tmp), str(OUT)], check=True)

    digest = sha256(OUT)
    dur = probe_dur(OUT)
    size = OUT.stat().st_size
    streams = probe_streams(OUT)
    v_dur = a_dur = None
    for s in streams.get("streams", []):
        if s.get("codec_type") == "video":
            v_dur = float(s.get("duration") or 0) or None
        if s.get("codec_type") == "audio":
            a_dur = float(s.get("duration") or 0) or None

    # Seam / chapter starts (story only)
    starts: dict[str, float] = {}
    t = 0.0
    for item, src_dur in zip(PARENTS, durs):
        starts[item["id"]] = t
        t += src_dur - XFADE
    # last part start already set; story_end is after P05 without trailing xfade subtract on last
    story_end = starts["05"] + durs[4]
    cream_in_abs = starts["05"] + P05_CREAM_IN
    end_hold_in = story_end  # hard concat after P05
    film_out = story_end + END_HOLD

    seams = {
        "01→02": starts["02"],
        "02→03": starts["03"],
        "03→04": starts["04"],
        "04→05": starts["05"],
    }

    sync_delta = None
    if v_dur is not None and a_dur is not None:
        sync_delta = a_dur - v_dur

    print(f"SAVED {OUT}", flush=True)
    print(f"SIZE {size}", flush=True)
    print(f"SHA256 {digest}", flush=True)
    print(f"DUR {dur:.3f}", flush=True)
    print(f"V_DUR {v_dur} A_DUR {a_dur} SYNC_DELTA {sync_delta}", flush=True)
    for k, v in seams.items():
        print(f"SEAM {k} {v:.3f} ({fmt_tc(v)})", flush=True)
    print(f"CREAM_IN {cream_in_abs:.3f} ({fmt_tc(cream_in_abs)})", flush=True)
    print(f"END_HOLD_IN {end_hold_in:.3f} ({fmt_tc(end_hold_in)})", flush=True)
    print(f"FILM_OUT {film_out:.3f} ({fmt_tc(film_out)})", flush=True)

    watch = (
        "WATCH THIS FILE (HOS 004 full join v01 — soft joins + cream + 20s Studio hold):\n"
        f"  {OUT.name}\n"
        f"  iCloud: HOS UAT/004_Whats-Really-Inside-An-Atom/09_Final-Export/{OUT.name}\n\n"
        f"sha256={digest}\n"
        f"duration={dur:.3f}\n"
        f"bytes={size}\n"
        f"seams: 01→02 {fmt_tc(seams['01→02'])} · 02→03 {fmt_tc(seams['02→03'])} · "
        f"03→04 {fmt_tc(seams['03→04'])} · 04→05 {fmt_tc(seams['04→05'])}\n"
        f"cream card in P05 @ {fmt_tc(cream_in_abs)} · 20s Studio hold from {fmt_tc(end_hold_in)}\n"
        "Parents passed (not reminted). VO v04. Do NOT label KEEP/LOCKED. STOP for Ben.\n"
    )
    WATCH.write_text(watch)

    lines = [
        "# HOS 004 full join v01 — soft joins + cream + 20s Studio end hold",
        "",
        f"**Cut:** `{OUT.name}`",
        f"**sha256:** `{digest}`",
        f"**Duration:** {dur:.3f} s · **Size:** {size} B",
        "**Status:** UAT for Ben. Do **not** label KEEP/LOCKED. Do **not** upload.",
        "",
        "xfade+acrossfade 0.40s at every part join. P05 owns the house cream card (~4s from 140.5).",
        "After P05, hard-concat 20s cream hold for YouTube Studio end screens.",
        "No remint. Locked v04 VO baked into each parent rough.",
        "",
        "**Parents (hash-checked):**",
        "",
        "| Part | File | sha256 | duration |",
        "|---|---|---|---:|",
    ]
    for item, d in zip(PARENTS, durs):
        lines.append(f"| {item['id']} | `{item['name']}` | `{item['sha']}` | {d:.3f} |")
    lines += [
        "",
        "| Beat | Time (s) | TC |",
        "|---|---:|---|",
        f"| P01 start (cold open) | {starts['01']:.3f} | {fmt_tc(starts['01'])} |",
        f"| Seam 01→02 | {seams['01→02']:.3f} | {fmt_tc(seams['01→02'])} |",
        f"| Seam 02→03 | {seams['02→03']:.3f} | {fmt_tc(seams['02→03'])} |",
        f"| Seam 03→04 | {seams['03→04']:.3f} | {fmt_tc(seams['03→04'])} |",
        f"| Seam 04→05 | {seams['04→05']:.3f} | {fmt_tc(seams['04→05'])} |",
        f"| Cream card (in P05) | {cream_in_abs:.3f} | {fmt_tc(cream_in_abs)} |",
        f"| 20s Studio end hold in | {end_hold_in:.3f} | {fmt_tc(end_hold_in)} |",
        f"| Film out | {dur:.3f} | {fmt_tc(dur)} |",
        "",
        f"A/V sync delta (audio−video): `{sync_delta}`",
        "",
        "Builder: `07_Edit-Project/_join_hos_004_full_v01.py`",
        "",
    ]
    NOTES.write_text("\n".join(lines) + "\n")

    meta = {
        "file": OUT.name,
        "sha256": digest,
        "duration": dur,
        "bytes": size,
        "xfade": XFADE,
        "end_hold_s": END_HOLD,
        "p05_cream_in_part_local": P05_CREAM_IN,
        "starts": starts,
        "seams": seams,
        "cream_in_abs": cream_in_abs,
        "end_hold_in": end_hold_in,
        "video_duration": v_dur,
        "audio_duration": a_dur,
        "sync_delta_a_minus_v": sync_delta,
        "parents": [
            {**item, "duration": d}
            for item, d in zip(PARENTS, durs)
        ],
        "status": "UAT_FOR_BEN",
        "keep_locked_label": False,
        "upload": False,
        "air_target": "Thu 15 Oct 2026 18:00 Europe/London",
    }
    META.write_text(json.dumps(meta, indent=2) + "\n")

    ICLOUD_DIR.mkdir(parents=True, exist_ok=True)
    dest = ICLOUD_DIR / OUT.name
    # retry copy on EDEADLK
    for attempt in range(1, 5):
        try:
            subprocess.run(["cp", "-f", str(OUT), str(dest)], check=True)
            break
        except subprocess.CalledProcessError:
            if attempt == 4:
                raise
            import time
            time.sleep(2 * attempt)
    icloud_sha = sha256(dest)
    print(f"ICLOUD {dest}", flush=True)
    print(f"ICLOUD_SHA {icloud_sha}", flush=True)
    if icloud_sha != digest:
        raise SystemExit(f"STOP: iCloud sha mismatch {icloud_sha}")
    (ICLOUD_DIR / NOTES.name).write_text(NOTES.read_text())
    (ICLOUD_DIR / WATCH.name).write_text(watch)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
