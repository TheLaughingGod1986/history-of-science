#!/usr/bin/env python3
"""HOS 006 master v05 (J0886): Assemble hos_006_master_v05.mp4 from v04 + 7 replacement clips, run all gates, build check sheet and <120 MB _PHONE.mp4."""
from __future__ import annotations

import hashlib
import json
import math
import shutil
import subprocess as sp
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OWB = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
ROOT = Path("/Users/benjaminoats/YouTube/History Of Science")
EP = ROOT / "02_Video-Projects/006_Trees-Are-Made-Of-Air"
MUSIC_DIR = EP / "05_Music"
SFX_DIR = EP / "06_Sound-Effects"
EDIT_DIR = EP / "07_Edit-Project"
V04 = EDIT_DIR / "master_v04"
WORK = EDIT_DIR / "master_v05"
CLIPS_V05 = WORK / "clips"
CHECK_FRAMES_DIR = WORK / "check_frames"

VIDEO_V04 = V04 / "hos_006_full_join_v04_teach.mp4"
VIDEO_V05 = WORK / "hos_006_full_join_v05_teach.mp4"
MASTER_V05 = WORK / "hos_006_master_v05.mp4"
PHONE_V05 = WORK / "hos_006_master_v05_PHONE.mp4"

FPS = 24
TOTAL = 12764 / 24.0  # 531.833333 s


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for blk in iter(lambda: fh.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def run_logged(args: list, name: str, cwd: Path | None = None) -> str:
    r = sp.run([str(x) for x in args], stdout=sp.PIPE, stderr=sp.STDOUT, text=True, cwd=cwd)
    (WORK / name).write_text(r.stdout)
    print(r.stdout[-1500:], flush=True)
    if r.returncode != 0:
        raise RuntimeError(f"{name} failed with exit code {r.returncode}")
    return r.stdout


def build_contact_sheet(video: Path, cuts: list[dict], out_jpg: Path) -> None:
    cols = 6
    tw, th = 320, 180
    rows_n = math.ceil(len(cuts) / cols)
    sheet = Image.new("RGB", (cols * tw, rows_n * (th + 26)), (24, 20, 16))
    d = ImageDraw.Draw(sheet)
    f = ImageFont.truetype("/System/Library/Fonts/Supplemental/Didot.ttc", 14, index=0)

    for idx, c in enumerate(cuts):
        mid = (c["timeline_in"] + c["timeline_out"]) / 2.0
        raw = sp.run(
            [
                "ffmpeg", "-v", "error", "-ss", f"{mid:.3f}", "-i", str(video),
                "-frames:v", "1", "-vf", f"scale={tw}:{th}",
                "-f", "rawvideo", "-pix_fmt", "rgb24", "-",
            ],
            capture_output=True,
            check=True,
        ).stdout
        im = Image.frombytes("RGB", (tw, th), raw)
        x = (idx % cols) * tw
        y = (idx // cols) * (th + 26)
        sheet.paste(im, (x, y))
        mm = int(mid // 60)
        ss = mid % 60
        label = f"#{idx+1:02d} {mm}:{ss:04.1f} {c['row'][:22]}"
        d.text((x + 6, y + th + 5), label, font=f, fill=(245, 232, 210))

    sheet.save(out_jpg, quality=88)


def build_ben_check_sheet(video: Path, out_jpg: Path) -> list[dict]:
    CHECK_FRAMES_DIR.mkdir(parents=True, exist_ok=True)
    probes = [
        ("00_07_scales_tree", 6.50, "0:07 (#02 02_balance_trunk_v05): Whole willow tree (roots, trunk, canopy) sitting ON left scale pan"),
        ("01_26_tree_in_pot", 86.00, "1:26 (#17 05_pure_water_v05): Willow growing out of pot through perforated lid + van Helmont"),
        ("04_28_priestley_body", 268.00, "4:28 (#50 17_notebook_tick_v05): Joseph Priestley full upper body & arm connected to quill hand"),
        ("04_54_sunny_window_bubbles", 294.00, "4:54 (#55 04_sunny_window_v05, v03 check): Bubbles strictly underwater inside the 5 jars"),
        ("05_17_explorer_jar_bubbles", 317.00, "5:17 (#59a 08_explorer_shade_v05, v03 check): Bubbles strictly underwater inside corked jar"),
        ("05_21_explorer_carries_jar", 321.00, "5:21 (#59b 08_explorer_shade_v05, v03 check): Explorer carries corked jar into shade, 0 air bubbles"),
        ("05_29_only_green_bubbles", 329.00, "5:29 (#61 10_only_green_v05): Bubbles strictly underwater on green leaf in right jar, 0 air bubbles"),
        ("07_16_callback_tree_in_pot", 436.00, "7:16 (#80 13_water_in_tree_v05 callback): Closer framing of willow growing out of pot"),
    ]
    cols = 2
    tw, th = 960, 540
    rows_n = math.ceil(len(probes) / cols)
    sheet = Image.new("RGB", (cols * tw, rows_n * (th + 44)), (24, 20, 16))
    d = ImageDraw.Draw(sheet)
    f = ImageFont.truetype("/System/Library/Fonts/Supplemental/Didot.ttc", 20, index=0)

    records = []
    for idx, (slug, ts, caption) in enumerate(probes):
        png_p = CHECK_FRAMES_DIR / f"{slug}.png"
        sp.run(
            [
                "ffmpeg", "-y", "-v", "error",
                "-ss", f"{ts:.3f}", "-i", str(video),
                "-frames:v", "1", str(png_p),
            ],
            check=True,
        )
        im = Image.open(png_p).convert("RGB").resize((tw, th), Image.Resampling.LANCZOS)
        x = (idx % cols) * tw
        y = (idx // cols) * (th + 44)
        sheet.paste(im, (x, y))
        d.text((x + 12, y + th + 10), caption, font=f, fill=(245, 232, 210))
        records.append({"slug": slug, "timestamp_s": ts, "file": str(png_p), "caption": caption})

    sheet.save(out_jpg, quality=92)
    return records


def main() -> int:
    WORK.mkdir(parents=True, exist_ok=True)

    # 1. Build cuts_full_join_v05.json and pool_full_join_v05.json from v04
    cuts_v04 = json.loads((V04 / "cuts_full_join_v04.json").read_text())
    pool_v04 = json.loads((V04 / "pool_full_join_v04.json").read_text())

    v05_replacements = {
        2: ("02_balance_trunk_v05.mp4", 74, 1.0, "Flow Nano Banana 2 still + push-in: whole willow tree with roots sitting ON left brass scale pan (J0886 #1)"),
        17: ("05_pure_water_v05.mp4", 120, 1.0, "Flow Nano Banana 2 still + water stream: willow growing out of terracotta pot through perforated lid (J0886 #2)"),
        50: ("17_notebook_tick_v05.mp4", 101, 1.0, "Flow Nano Banana 2 still + push-in: Joseph Priestley full upper body & arm holding quill over notebook (J0886 #3)"),
        55: ("04_sunny_window_v05.mp4", 109, 1.0, "5 jars on sunny windowsill, n_motes=0, underwater bubbles strictly below meniscus (J0886 #4 / v03 4:54)"),
        59: ("08_explorer_shade_v05.mp4", 173, 1.0, "08_explorer_shade_t1 still with underwater-only bubbles + 8f xfade into Explorer carrying jar (J0886 #4 / v03 5:21)"),
        61: ("10_only_green_v05.mp4", 110, 1.0, "Flow Nano Banana 2 still + underwater bubbles strictly inside right green-leaf jar, 0 air bubbles (J0886 #4)"),
        80: ("13_water_in_tree_v05.mp4", 122, 1.0, "Distinct closer framing of willow growing out of terracotta pot for Part 5 callback (J0886 #2)"),
    }

    cuts_v05 = []
    overlay_jobs = []
    for idx, c in enumerate(cuts_v04):
        row = dict(c)
        cut_num = idx + 1
        if cut_num in v05_replacements:
            fname, n_f, up, disp = v05_replacements[cut_num]
            clip_p = CLIPS_V05 / fname
            assert int(row["frames"]) == n_f, f"Cut #{cut_num} frame mismatch: {row['frames']} != {n_f}"
            sf = int(round(row["timeline_in"] * FPS))
            ef = int(round(row["timeline_out"] * FPS))
            assert ef - sf == n_f
            row["source"] = fname
            row["source_path"] = str(clip_p)
            row["source_sha256"] = sha256_file(clip_p)
            row["upscale"] = up
            row["framing"] = {"offset": 0.0}
            row["disposition"] = disp
            overlay_jobs.append((cut_num, clip_p, sf, ef))
        cuts_v05.append(row)

    pool_map = {(p["file"], p["part"]): dict(p) for p in pool_v04}
    for row in cuts_v05:
        key = (row["source"], row["part"])
        if key not in pool_map:
            pool_map[key] = {
                "file": row["source"],
                "title": "HOS 3D cartoon clip, Chief/J0886 KEEP",
                "part": row["part"],
            }
    pool_v05 = list(pool_map.values())

    (WORK / "cuts_full_join_v05.json").write_text(json.dumps(cuts_v05, indent=2) + "\n")
    (WORK / "pool_full_join_v05.json").write_text(json.dumps(pool_v05, indent=2) + "\n")
    shutil.copy2(V04 / "picture_qa_reviewed_ok_v04.json", WORK / "picture_qa_reviewed_ok_v05.json")
    shutil.copy2(V04 / "LAY_TIMES_v04.json", WORK / "LAY_TIMES_v05.json")
    shutil.copy2(V04 / "TEACH_OVERLAYS_RENDER_v04.json", WORK / "TEACH_OVERLAYS_RENDER_v05.json")
    shutil.copy2(V04 / "teach_laid_sheet_v04.jpg", WORK / "teach_laid_sheet_v05.jpg")

    # 2. Composite the 7 replacement cuts directly over hos_006_full_join_v04_teach.mp4
    cmd = ["ffmpeg", "-y", "-v", "error", "-i", str(VIDEO_V04)]
    for _, clip_p, _, _ in overlay_jobs:
        cmd += ["-i", str(clip_p)]

    parts = ["[0:v]format=yuv420p[v0]"]
    for i, (cut_num, _, sf, ef) in enumerate(overlay_jobs):
        start_s = sf / FPS
        parts.append(f"[{i + 1}:v]fps=24,scale=1920:1080:flags=lanczos,setpts=PTS-STARTPTS+{start_s:.6f}/TB,format=yuv420p[r{i}]")
        parts.append(
            f"[v{i}][r{i}]overlay=x=0:y=0:eof_action=pass:repeatlast=0:shortest=0:"
            f"enable='between(n,{sf},{ef - 1})'[v{i + 1}]"
        )
    last = f"v{len(overlay_jobs)}"
    cmd += [
        "-filter_complex", ";".join(parts),
        "-map", f"[{last}]",
        "-an",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "17",
        "-pix_fmt", "yuv420p", "-r", "24",
        "-movflags", "+faststart",
        str(VIDEO_V05),
    ]
    print(f"Building {VIDEO_V05.name} with {len(overlay_jobs)} replacement cuts ...", flush=True)
    sp.run(cmd, check=True)

    # 3. Copy verified v04 audio stems and mux hos_006_master_v05.mp4
    vo_wav = WORK / "stem_vo_v05.wav"
    bed_mp3 = MUSIC_DIR / "trees006_score_bed_v01.mp3"
    sfx_out = SFX_DIR / "stem_sfx_v01.wav"
    master_m4a = WORK / "audio_master_v05.m4a"
    shutil.copy2(V04 / "stem_vo_v04.wav", vo_wav)
    shutil.copy2(V04 / "audio_master_v04.m4a", master_m4a)

    run_logged(
        [
            "ffmpeg", "-y", "-v", "error",
            "-i", VIDEO_V05, "-i", master_m4a,
            "-map", "0:v:0", "-map", "1:a:0",
            "-c", "copy", "-movflags", "+faststart", MASTER_V05,
        ],
        "mux_v05.txt",
    )
    for p, name in [(VIDEO_V05, "source_video_sha256.txt"), (MASTER_V05, "master_video_sha256.txt")]:
        run_logged(["ffmpeg", "-v", "error", "-i", p, "-map", "0:v:0", "-c", "copy", "-f", "hash", "-hash", "sha256", "-"], name)
    assert (WORK / "source_video_sha256.txt").read_text() == (WORK / "master_video_sha256.txt").read_text()

    # 4. Build full-size check frames + Ben check sheet + contact sheet
    check_records = build_ben_check_sheet(MASTER_V05, WORK / "hos_006_master_v05_ben_check_sheet.jpg")
    (WORK / "BEN_CHECK_FRAMES_v05.json").write_text(json.dumps(check_records, indent=2) + "\n")
    build_contact_sheet(MASTER_V05, cuts_v05, WORK / "hos_006_master_v05_contact_sheet.jpg")

    # 5. Run all gates (sfx_kit.py level, music_gate.py, picture_qa.py, polish_gate.py, gate:episode, ebur128)
    run_logged(
        [
            sys.executable, OWB / "scripts/sfx_kit.py", "level",
            "--vo", vo_wav, "--sfx", sfx_out, "--bed", bed_mp3,
            "--minutes", f"{TOTAL / 60.0:.2f}", "--out", SFX_DIR / "sfx_level_v01.json",
        ],
        "sfx_level_v05.txt",
    )

    other_beds = [
        p
        for root in (ROOT, OWB)
        for p in root.glob("02_Video-Projects/*/05_Music/*")
        if p.suffix.lower() in (".mp3", ".wav", ".m4a") and p.parent.parent != EP
    ]
    run_logged(
        [
            sys.executable, OWB / "scripts/music_gate.py", EP,
            "--bed", bed_mp3, "--video", MASTER_V05,
            "--out", WORK / "music_gate.json",
            "--others", *other_beds,
        ],
        "music_gate_v05.txt",
    )
    (MUSIC_DIR / "music_gate_bed_v01.json").write_text((WORK / "music_gate.json").read_text())

    run_logged(
        [
            sys.executable, OWB / "scripts/picture_qa.py", MASTER_V05,
            "--cuts", WORK / "cuts_full_join_v05.json",
            "--pool", WORK / "pool_full_join_v05.json",
            "--out-dir", WORK,
            "--reviewed-ok", WORK / "picture_qa_reviewed_ok_v05.json",
        ],
        "picture_qa_v05.txt",
    )
    run_logged(
        [
            sys.executable, OWB / "scripts/polish_gate.py", MASTER_V05,
            "--cuts", WORK / "cuts_full_join_v05.json",
            "--out", WORK / "polish_gate.json",
            "--reviewed-ok", WORK / "picture_qa_reviewed_ok_v05.json",
        ],
        "polish_gate_v05.txt",
    )
    run_logged(["npm", "run", "gate:episode", "--", "--project", EP], "episode_gate_v05.txt", ROOT / "07_Content-Ops")
    run_logged(["ffmpeg", "-hide_banner", "-i", MASTER_V05, "-af", "ebur128=peak=true", "-f", "null", "-"], "master_loudness_v05.txt")

    # 6. Build <120 MB _PHONE.mp4 copy
    sp.run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-i", str(MASTER_V05),
            "-c:v", "libx264", "-preset", "fast", "-crf", "23", "-maxrate", "1500k", "-bufsize", "3000k",
            "-pix_fmt", "yuv420p", "-r", "24",
            "-c:a", "copy", "-movflags", "+faststart",
            str(PHONE_V05),
        ],
        check=True,
    )
    phone_mb = PHONE_V05.stat().st_size / (1024 * 1024)
    print(f"Built {PHONE_V05.name}: {phone_mb:.2f} MB (< 120 MB)", flush=True)
    assert phone_mb < 120.0, f"PHONE copy too large: {phone_mb:.2f} MB"

    manifest = {
        str(p.relative_to(EP)): sha256_file(p)
        for p in [
            MASTER_V05,
            PHONE_V05,
            vo_wav,
            bed_mp3,
            sfx_out,
            WORK / "hos_006_master_v05_ben_check_sheet.jpg",
            WORK / "hos_006_master_v05_contact_sheet.jpg",
        ]
    }
    (WORK / "SHA256_v05.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print("ALL MASTER V05 GATES COMPLETED SUCCESSFULLY", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
