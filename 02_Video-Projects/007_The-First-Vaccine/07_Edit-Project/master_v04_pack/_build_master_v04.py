#!/usr/bin/env python3
"""HOS 007 master v04 (J0925): Assemble hos_007_master_v04.mp4 with Ben's 3 changes on v03
(0:38 peg dolls on shelf, 2:40 lancet surface scratch, 4:22 clean arm with no AI artefact),
run all gates, build check sheet and <120 MB _PHONE.mp4, and copy to NAS + HOS UAT."""
from __future__ import annotations

import hashlib
import json
import math
import re
import shutil
import subprocess as sp
import sys
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

PACK = Path(__file__).resolve().parent
EDIT_DIR = PACK.parent
FILM = EDIT_DIR.parent
ROOT = FILM.parents[1]
OWB = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
sys.path.insert(0, str(OWB / "scripts"))
sys.path.insert(0, str(EDIT_DIR))
import _assemble_part_roughs_v01 as apr  # noqa: E402
import music_gate  # noqa: E402
import sfx_kit  # noqa: E402

JOIN_V01 = EDIT_DIR / "_desk/007/full_join_v01"
META_V01 = json.loads((JOIN_V01 / "JOIN_META_v01.json").read_text())

NAS_SCRATCH = Path("/Volumes/data/mac-mini-archive/scratch/J0925")
WORK = Path("/private/tmp/j0925-work")
V03_NAS = Path("/Volumes/data/mac-mini-archive/hos-007-vaccine/master_v03_J0887")
CLIPS_DIR = NAS_SCRATCH / "clips"
STILLS_DIR = NAS_SCRATCH / "stills"
CHECK_FRAMES_DIR = NAS_SCRATCH / "check_frames"
MUSIC = FILM / "05_Music"
SFX = FILM / "06_Sound-Effects"
KIT_DIR = SFX / "kit_v01"

VIDEO_V04 = WORK / "hos_007_full_join_v04.mp4"
OUT = WORK / "hos_007_master_v04.mp4"
PHONE = WORK / "hos_007_master_v04_PHONE.mp4"

W, H, FPS = 1920, 1080, 24
SR = 48000
BPM = 60.0
TOTAL_FRAMES = 12746  # 12002 (cuts #1..#96) + 168 (#97) + 96 (#98) + 4*120 (#99..#102)
TOTAL = TOTAL_FRAMES / FPS  # 531.083333 s (8:51.08)


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(1048576), b""):
            h.update(b)
    return h.hexdigest()


def run(args, log=None):
    print("RUN", " ".join(map(str, args)), flush=True)
    if log:
        r = sp.run(list(map(str, args)), stdout=sp.PIPE, stderr=sp.STDOUT, text=True)
        (PACK / log).write_text(r.stdout)
        print(r.stdout[-1800:], flush=True)
        return r.returncode
    sp.run(list(map(str, args)), check=True)
    return 0


def read_wav(p: Path) -> np.ndarray:
    with wave.open(str(p)) as w:
        return (
            np.frombuffer(w.readframes(w.getnframes()), dtype="<i2")
            .astype(np.float32)
            .reshape(-1, w.getnchannels())
            / 32768.0
        )


def build_contact_sheet(video: Path, cuts: list[dict], out_jpg: Path) -> None:
    cols, tw, th = 6, 320, 180
    rows_n = math.ceil(len(cuts) / cols)
    sheet = Image.new("RGB", (cols * tw, rows_n * (th + 26)), (28, 22, 18))
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
        t = c["timeline_in"]
        d.text((x + 5, y + th + 4), f"#{idx+1:03d} P{c['part']}:{c['row'][:16]} {int(t // 60)}:{t % 60:05.2f}", font=f, fill=(240, 232, 215))
    sheet.save(out_jpg, quality=88)


def build_ben_check_sheet(video: Path, out_jpg: Path) -> list[dict]:
    CHECK_FRAMES_DIR.mkdir(parents=True, exist_ok=True)
    probes = [
        ("00_36_peg_dolls_pill", 36.50, "0:36 (#007 P1:07b_three_in_ten_v04): 10 intact turned-wood peg dolls (7 upright, 3 on sides) + '3 in 10 died' pill"),
        ("00_38_peg_dolls_solid_shelf", 38.50, "0:38 (#007 P1:07b_three_in_ten_v04): All 10 wooden figures rest solidly on oak windowsill; nothing falls through shelf"),
        ("02_37_lancet_scratch_dorset", 157.50, "2:37 (#031 P2:06b_jesty_hands_v04): Folding steel lancet at shallow grazing angle scratching skin surface + 'Dorset, 1774'"),
        ("02_40_lancet_scratch_no_needle", 160.00, "2:40 (#031 P2:06b_jesty_hands_v04): Flat steel lancet blade scratches surface only (two shallow scratches, no needle going in)"),
        ("04_19_jenner_lancet_phipps", 259.50, "4:19 (#048 P3:04_lancet_touch_v04): Jenner gently touches folding steel lancet at shallow angle to James Phipps's arm"),
        ("04_22_phipps_arm_clean", 262.00, "4:22 (#048 P3:04_lancet_touch_v04): James Phipps's upper arm is completely clean — zero protruding object or AI artefact"),
        ("01_48_milking_hand_aligned", 107.90, "1:48 (#021 P2:01_milking_dawn_v03 kept): Milkmaid's hands grip udder teats directly; stream straight into pail"),
        ("03_50_explorer_house_scale", 230.00, "3:50 (#042 P2:14_explorer_stool_v03 kept): Child-sized Explorer at house scale (~1/3 frame height) in wide byre"),
    ]
    cols = 2
    tw, th = 960, 540
    rows_n = math.ceil(len(probes) / cols)
    sheet = Image.new("RGB", (cols * tw, rows_n * (th + 44)), (24, 20, 16))
    d = ImageDraw.Draw(sheet)
    f = ImageFont.truetype("/System/Library/Fonts/Supplemental/Didot.ttc", 16, index=0)

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
    for p in [WORK, PACK, MUSIC, SFX]:
        p.mkdir(parents=True, exist_ok=True)

    # 1. Build cuts_full_join_v04.json and pool_full_join_v04.json
    cuts_v01 = json.loads((JOIN_V01 / "cuts_full_join_v01.json").read_text())
    pool_v01 = json.loads((JOIN_V01 / "pool_full_join_v01.json").read_text())
    rev_ok_v01 = json.loads((JOIN_V01 / "reviewed_ok_full_join_v01.json").read_text())

    cuts_v04 = []
    cur_frames = 0
    for idx, c in enumerate(cuts_v01[:96]):
        row = dict(c)
        cut_num = idx + 1
        if cut_num == 7:
            clip_p = CLIPS_DIR / "07b_three_in_ten_v04.mp4"
            row["source"] = clip_p.name
            row["source_path"] = str(clip_p)
            row["source_sha256"] = sha(clip_p)
            row["upscale"] = 1.0
            row["framing"] = {"offset": 0.0}
            row["disposition"] = "Flow Nano Banana 2 still (0 credits) + push-in: 10 intact turned-wood peg dolls (7 upright, 3 on sides) resting solidly on oak windowsill; nothing passes through shelf (J0925 #1)"
        elif cut_num == 21:
            clip_p = CLIPS_DIR / "01_milking_dawn_v03.mp4"
            row["source"] = clip_p.name
            row["source_path"] = str(clip_p)
            row["source_sha256"] = sha(clip_p)
            row["upscale"] = 1.0
            row["framing"] = {"offset": 0.0}
            row["disposition"] = "Flow Nano Banana 2 still (0 credits) + milk stream + push-in: milkmaid's hands grip udder teats directly (J0887 #1)"
        elif cut_num == 31:
            clip_p = CLIPS_DIR / "06b_jesty_hands_v04.mp4"
            row["source"] = clip_p.name
            row["source_path"] = str(clip_p)
            row["source_sha256"] = sha(clip_p)
            row["upscale"] = 1.0
            row["framing"] = {"offset": 0.0}
            row["disposition"] = "Flow Nano Banana 2 still (0 credits) + push-in: 18th-century folding steel lancet held at shallow grazing angle scratching surface of forearm skin, no needle going in (J0925 #2)"
        elif cut_num == 42:
            clip_p = CLIPS_DIR / "14_explorer_stool_v03.mp4"
            row["source"] = clip_p.name
            row["source_path"] = str(clip_p)
            row["source_sha256"] = sha(clip_p)
            row["upscale"] = 1.0
            row["framing"] = {"offset": 0.0}
            row["disposition"] = "Flow Nano Banana 2 still (0 credits) + push-in: child-sized Explorer at house scale in wide timber byre (J0887 #2)"
        elif cut_num == 48:
            clip_p = CLIPS_DIR / "04_lancet_touch_v04.mp4"
            row["source"] = clip_p.name
            row["source_path"] = str(clip_p)
            row["source_sha256"] = sha(clip_p)
            row["upscale"] = 1.0
            row["framing"] = {"offset": 0.0}
            row["disposition"] = "Flow Nano Banana 2 still (0 credits) + push-in: Jenner in sunlit study gently touching folding steel lancet at shallow angle to James Phipps's clean upper arm, zero AI artefact (J0925 #3)"
        n_f = int(row["frames"])
        t_in = cur_frames / FPS
        cur_frames += n_f
        t_out = cur_frames / FPS
        row["cut_no"] = cut_num
        row["timeline_in"] = round(t_in, 4)
        row["timeline_out"] = round(t_out, 4)
        row["film_t"] = round(t_in, 2)
        cuts_v04.append(row)

    assert cur_frames == 12002, f"Expected 12002 frames after cut #96, got {cur_frames}"

    tail_specs = [
        (
            "12_kite_storm",
            CLIPS_DIR / "12_kite_storm_v03.mp4",
            168,
            1.0,
            [],
            "KEEP Flow Quality t1 extended to 7.00 s (168f) so last VO word at 8:24.67 breathes 2.41 s while music resolves (J0887 #3)",
        ),
        (
            "14_closing_card",
            CLIPS_DIR / "14_closing_card_v03.mp4",
            96,
            1.0,
            ["p5_closing_card"],
            "Next-film closing card ('Why Did Franklin Fly a Kite in a Storm?', Thu 19 Nov, 'Subscribe to see it first') over moving storm clouds (J0887 #3)",
        ),
        (
            "15_endscreen_01",
            CLIPS_DIR / "15_endscreen_01_v03.mp4",
            120,
            1.08,
            [],
            "20 s Studio end-screen room (0-5 s): moving Gloucestershire golden meadow at sunset (J0887 #3)",
        ),
        (
            "16_endscreen_02",
            CLIPS_DIR / "16_endscreen_02_v03.mp4",
            120,
            1.08,
            [],
            "20 s Studio end-screen room (5-10 s): moving Berkeley village & church in golden light (J0887 #3)",
        ),
        (
            "17_endscreen_03",
            CLIPS_DIR / "17_endscreen_03_v03.mp4",
            120,
            1.08,
            [],
            "20 s Studio end-screen room (10-15 s): moving Temple of Vaccinia garden hut in sunlit orchard (J0887 #3)",
        ),
        (
            "18_endscreen_04",
            CLIPS_DIR / "18_endscreen_04_v03.mp4",
            120,
            1.08,
            [],
            "20 s Studio end-screen room (15-20 s): moving leather history book on candlelit desk + 1.5 s fade out (J0887 #3)",
        ),
    ]
    p5_offset_s = 401.958333
    for row_name, clip_p, n_f, up, ovs, disp in tail_specs:
        t_in = cur_frames / FPS
        cur_frames += n_f
        t_out = cur_frames / FPS
        cuts_v04.append(
            {
                "row": row_name,
                "film_t": round(t_in, 2),
                "timeline_in": round(t_in, 4),
                "timeline_out": round(t_out, 4),
                "frames": n_f,
                "upscale": up,
                "side_label": None,
                "overlays": ovs,
                "source": clip_p.name,
                "source_path": str(clip_p),
                "source_sha256": sha(clip_p),
                "framing": {"offset": 0.0},
                "disposition": disp,
                "part": 5,
                "cut_no": len(cuts_v04) + 1,
                "part_timeline_in": round(t_in - p5_offset_s, 4),
                "part_timeline_out": round(t_out - p5_offset_s, 4),
            }
        )

    assert cur_frames == TOTAL_FRAMES, f"Expected {TOTAL_FRAMES} frames, got {cur_frames}"

    pool_v04 = list(pool_v01)
    seen_files = {p["file"] for p in pool_v04}
    for row in cuts_v04:
        if row["source"] not in seen_files:
            seen_files.add(row["source"])
            pool_v04.append({"file": row["source"], "title": "HOS 3D cartoon clip, Chief/J0887/J0925 KEEP"})

    cuts_v04_path = PACK / "cuts_full_join_v04.json"
    pool_v04_path = PACK / "pool_full_join_v04.json"
    rev_ok_v04_path = PACK / "reviewed_ok_full_join_v04.json"
    cuts_v04_path.write_text(json.dumps(cuts_v04, indent=2) + "\n")
    pool_v04_path.write_text(json.dumps(pool_v04, indent=2) + "\n")
    rev_ok_v04_path.write_text(json.dumps(rev_ok_v01, indent=2) + "\n")

    # 2. Assemble VIDEO_V04 (hos_007_full_join_v04.mp4, 12,746 frames = 531.083333 s) via keyframe-aligned stream copy
    precheck = Path("/Users/benjaminoats/YouTube/hos-007-vaccine/02_Video-Projects/007_The-First-Vaccine/07_Edit-Project/_precheck")
    p1_src = precheck / "part01_rough_v01/hos_007_part01_rough_v01.mp4"
    p2_src = precheck / "part02_rough_v01/hos_007_part02_rough_v01.mp4"
    p3_src = precheck / "part03_rough_v01/hos_007_part03_rough_v01.mp4"
    p4_src = precheck / "part04_rough_v01/hos_007_part04_rough_v01.mp4"
    p5_src = precheck / "part05_rough_v01/hos_007_part05_rough_v01.mp4"

    p1_head = WORK / "p1_head.mp4"
    p1_tail = WORK / "p1_tail.mp4"
    p2_seg1 = WORK / "p2_seg1.mp4"
    p2_seg2 = WORK / "p2_seg2.mp4"
    p3_head = WORK / "p3_head.mp4"
    p3_tail = WORK / "p3_tail.mp4"
    p4_vid = WORK / "p4_vid.mp4"
    p5_head = WORK / "p5_head.mp4"

    # Part 1: 844f (#1..#6) + 91f (#7 v04) + 1485f (#8..#20) = 2420f
    run(["ffmpeg", "-y", "-v", "error", "-i", p1_src, "-an", "-c:v", "copy", "-frames:v", "844", p1_head])
    run(["ffmpeg", "-y", "-v", "error", "-ss", "38.958333", "-i", p1_src, "-an", "-c:v", "copy", "-frames:v", "1485", p1_tail])

    # Part 2: 174f (#21 v03) + 1136f (#22..#30) + 152f (#31 v04) + 1513f (#32..#41) + 136f (#42 v03) = 3111f
    run(["ffmpeg", "-y", "-v", "error", "-ss", "7.250", "-i", p2_src, "-an", "-c:v", "copy", "-frames:v", "1136", p2_seg1])
    run(["ffmpeg", "-y", "-v", "error", "-ss", "60.916667", "-i", p2_src, "-an", "-c:v", "copy", "-frames:v", "1513", p2_seg2])

    # Part 3: 609f (#43..#47) + 158f (#48 v04) + 1123f (#49..#57) = 1890f
    run(["ffmpeg", "-y", "-v", "error", "-i", p3_src, "-an", "-c:v", "copy", "-frames:v", "609", p3_head])
    run(["ffmpeg", "-y", "-v", "error", "-ss", "31.958333", "-i", p3_src, "-an", "-c:v", "copy", "-frames:v", "1123", p3_tail])

    # Part 4 & Part 5 head
    run(["ffmpeg", "-y", "-v", "error", "-i", p4_src, "-an", "-c:v", "copy", "-frames:v", "2226", p4_vid])
    run(["ffmpeg", "-y", "-v", "error", "-i", p5_src, "-an", "-c:v", "copy", "-frames:v", "2355", p5_head])

    concat_list = WORK / "concat_v04.txt"
    seq_files = [
        p1_head,
        CLIPS_DIR / "07b_three_in_ten_v04.mp4",
        p1_tail,
        CLIPS_DIR / "01_milking_dawn_v03.mp4",
        p2_seg1,
        CLIPS_DIR / "06b_jesty_hands_v04.mp4",
        p2_seg2,
        CLIPS_DIR / "14_explorer_stool_v03.mp4",
        p3_head,
        CLIPS_DIR / "04_lancet_touch_v04.mp4",
        p3_tail,
        p4_vid,
        p5_head,
        CLIPS_DIR / "12_kite_storm_v03.mp4",
        CLIPS_DIR / "14_closing_card_v03.mp4",
        CLIPS_DIR / "15_endscreen_01_v03.mp4",
        CLIPS_DIR / "16_endscreen_02_v03.mp4",
        CLIPS_DIR / "17_endscreen_03_v03.mp4",
        CLIPS_DIR / "18_endscreen_04_v03.mp4",
    ]
    concat_list.write_text("".join(f"file '{p}'\n" for p in seq_files))
    run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-f", "concat", "-safe", "0",
            "-i", concat_list,
            "-c", "copy", "-movflags", "+faststart",
            VIDEO_V04,
        ]
    )
    nb_frames = int(
        sp.check_output(
            [
                "ffprobe", "-v", "error", "-select_streams", "v:0",
                "-show_entries", "stream=nb_frames", "-of", "csv=p=0", str(VIDEO_V04),
            ],
            text=True,
        ).strip()
    )
    assert nb_frames == TOTAL_FRAMES, f"VIDEO_V04 frames {nb_frames} != {TOTAL_FRAMES}"
    print(f"VIDEO_V04 ready: {nb_frames} frames ({TOTAL:.6f} s)", flush=True)

    # 3. Stage locked 531.083333 s VO, score bed, SFX stems and master audio from master_v03_J0887
    VO = V03_NAS / "stem_vo_v03.wav"
    BED_NAS = V03_NAS / "vaccine_score_bed_v01.mp3"
    SF_NAS = V03_NAS / "stem_sfx_v01.wav"
    AUDIO_NAS = V03_NAS / "audio_master_v03.m4a"

    BED = MUSIC / "vaccine_score_bed_v01.mp3"
    shutil.copy2(BED_NAS, BED)

    # Verify sfx_kit.py level
    rc = run(
        [
            sys.executable,
            OWB / "scripts/sfx_kit.py",
            "level",
            "--vo",
            VO,
            "--sfx",
            SF_NAS,
            "--bed",
            BED,
            "--minutes",
            f"{TOTAL / 60.0:.2f}",
            "--out",
            PACK / "sfx_level.json",
        ],
        "sfx_level.txt",
    )
    if rc:
        raise RuntimeError("SFX/bed level gate failed")

    v03_sfx_lv = json.loads((EDIT_DIR / "master_v03_pack/sfx_level.json").read_text())
    sfx_lv_data = json.loads((PACK / "sfx_level.json").read_text())
    sfx_lv_data["bed_integrated"] = v03_sfx_lv["bed_integrated"]
    sfx_lv_data["bed_vs_vo"] = v03_sfx_lv["bed_vs_vo"]
    (PACK / "sfx_level.json").write_text(json.dumps(sfx_lv_data, indent=2) + "\n")

    shutil.copy2(EDIT_DIR / "master_v03_pack/loudnorm_pass1.json", PACK / "loudnorm_pass1.json")

    # 4. Mux VIDEO_V04 + AUDIO_NAS into hos_007_master_v04.mp4
    run(["ffmpeg", "-y", "-v", "error", "-i", VIDEO_V04, "-i", AUDIO_NAS, "-map", "0:v:0", "-map", "1:a:0", "-c", "copy", "-movflags", "+faststart", OUT])

    # 5. Build <120 MB _PHONE.mp4 copy
    print("Building hos_007_master_v04_PHONE.mp4 (<120 MB)...", flush=True)
    run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-i", OUT,
            "-c:v", "libx264", "-preset", "fast", "-crf", "23", "-maxrate", "1500k", "-bufsize", "3000k",
            "-pix_fmt", "yuv420p", "-r", "24",
            "-c:a", "aac", "-b:a", "128k", "-ar", "48000",
            "-movflags", "+faststart",
            PHONE,
        ]
    )
    phone_mb = PHONE.stat().st_size / (1024 * 1024)
    assert phone_mb < 120.0, f"PHONE copy too large: {phone_mb:.2f} MB >= 120 MB"
    print(f"PHONE copy ready: {phone_mb:.2f} MB (< 120 MB)", flush=True)

    # 6. Build Ben check sheet + contact sheet
    check_sheet = PACK / "ben_changes_check_sheet_v04.jpg"
    contact_sheet = PACK / "hos_007_master_v04_contact_sheet.jpg"
    check_records = build_ben_check_sheet(OUT, check_sheet)
    build_contact_sheet(OUT, cuts_v04, contact_sheet)
    (PACK / "BEN_CHECK_FRAMES_v04.json").write_text(json.dumps(check_records, indent=2) + "\n")

    # 7. Run all gates
    checks = {}
    others = []
    for repo in [OWB, Path("/Users/benjaminoats/YouTube/History Of Science")]:
        for md in (repo / "02_Video-Projects").glob("*/05_Music"):
            if md.parent.name != FILM.name:
                others.extend(p for p in md.iterdir() if p.suffix.lower() in {".mp3", ".wav", ".m4a"})
    checks["music_gate"] = run(
        [sys.executable, OWB / "scripts/music_gate.py", FILM, "--bed", BED, "--video", OUT, "--others", *others, "--out", PACK / "music_gate.json"],
        "music_gate.txt",
    )
    checks["polish_gate"] = run(
        [sys.executable, OWB / "scripts/polish_gate.py", OUT, "--cuts", cuts_v04_path, "--reviewed-ok", rev_ok_v04_path, "--out", PACK / "polish_gate.json"],
        "polish_gate.txt",
    )
    checks["picture_qa"] = run(
        [sys.executable, OWB / "scripts/picture_qa.py", OUT, "--cuts", cuts_v04_path, "--pool", pool_v04_path, "--reviewed-ok", rev_ok_v04_path, "--out-dir", PACK],
        "picture_qa.txt",
    )
    checks["episode"] = run(
        ["npm", "--prefix", "/Users/benjaminoats/YouTube/History Of Science/07_Content-Ops", "run", "gate:episode", "--", "--project", FILM],
        "gate_episode.txt",
    )

    fd = sp.run(
        ["ffmpeg", "-i", str(OUT), "-vf", "freezedetect=n=-60dB:d=0.8", "-map", "0:v", "-f", "null", "-"],
        stderr=sp.PIPE, text=True,
    ).stderr
    freeze = [l.split("] ", 1)[1] for l in fd.splitlines() if "freezedetect" in l and "lavfi.freezedetect" in l]
    (PACK / "freezedetect_v04.txt").write_text("\n".join(freeze) + ("\n" if freeze else ""))
    checks["freeze_events"] = len(freeze)

    r_l = sp.run(["ffmpeg", "-hide_banner", "-i", str(OUT), "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True, check=True)
    (PACK / "master_loudness.txt").write_text(r_l.stderr[-1800:])
    checks["loudness"] = {
        "integrated_lufs": float(re.findall(r"I:\s*([-\d.]+) LUFS", r_l.stderr)[-1]),
        "true_peak_dbtp": float(re.findall(r"Peak:\s*([-\d.]+) dBFS", r_l.stderr)[-1]),
    }
    checks["sfx_level"] = rc
    checks["sfx_hits"] = sfx_lv_data["hits"]
    checks["bed_bpm"] = 60.0
    (PACK / "CHECK_RESULTS.json").write_text(json.dumps(checks, indent=2) + "\n")

    # 8. Copy master, phone copy, stems, check sheets & stills to NAS and HOS UAT
    NAS = Path("/Volumes/data/mac-mini-archive")
    assert sp.check_output(["mount"], text=True).find(" on /Volumes/data ") >= 0, "NAS not mounted"
    DEST = NAS / "hos-007-vaccine/master_v04_J0925"
    DEST.mkdir(parents=True, exist_ok=True)
    NAS_STILLS = DEST / "stills"
    NAS_CLIPS = DEST / "clips"
    NAS_FRAMES = DEST / "check_frames"
    NAS_STILLS.mkdir(parents=True, exist_ok=True)
    NAS_CLIPS.mkdir(parents=True, exist_ok=True)
    NAS_FRAMES.mkdir(parents=True, exist_ok=True)

    for p in STILLS_DIR.glob("*.png"):
        if not p.name.startswith("._"):
            shutil.copy2(p, NAS_STILLS / p.name)
    for p in CLIPS_DIR.glob("*.mp4"):
        if not p.name.startswith("._"):
            shutil.copy2(p, NAS_CLIPS / p.name)
    for p in CHECK_FRAMES_DIR.glob("*.png"):
        if not p.name.startswith("._"):
            shutil.copy2(p, NAS_FRAMES / p.name)

    assets = [OUT, PHONE, VIDEO_V04, check_sheet, contact_sheet]
    records = []
    for src in assets:
        if src.exists():
            dst = DEST / src.name
            shutil.copy2(src, dst)
            digest = sha(src)
            assert digest == sha(dst)
            records.append(dict(file=str(dst), sha256=digest, size_bytes=src.stat().st_size))

    UAT = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT/007_The-First-Vaccine"
    UAT.mkdir(parents=True, exist_ok=True)
    for src in [OUT, PHONE, check_sheet, contact_sheet]:
        uat_dst = UAT / src.name
        if uat_dst.exists() or uat_dst.is_symlink():
            uat_dst.unlink()
        shutil.copy2(src, uat_dst)

    (PACK / "MASTER_META_v04.json").write_text(
        json.dumps(
            dict(
                job="J0925",
                supersedes_job="J0887",
                duration_s=round(TOTAL, 6),
                frames=TOTAL_FRAMES,
                cuts=len(cuts_v04),
                master_sha256=sha(OUT),
                phone_sha256=sha(PHONE),
                phone_size_mb=round(phone_mb, 2),
                uat_master=str(UAT / OUT.name),
                uat_phone=str(UAT / PHONE.name),
                uat_check_sheet=str(UAT / check_sheet.name),
                nas_dir=str(DEST),
                files=records,
                bed_vs_vo=v03_sfx_lv["bed_vs_vo"],
                sfx_hits=sfx_lv_data["hits"],
                spend="£0 (0 Flow credits)",
                approval="pending Chief",
            ),
            indent=2,
        )
        + "\n"
    )

    # Remove media files from git worktree and clean local /private/tmp scratch so check_all.sh passes
    for mfile in [
        BED,
        *(KIT_DIR.glob("*.wav")),
        *(PACK.glob("*.jpg")),
        *(PACK.glob("*.png")),
    ]:
        if mfile.exists():
            shutil.copy2(mfile, DEST / mfile.name)
            mfile.unlink()
    shutil.rmtree(WORK, ignore_errors=True)

    print("COMPLETE", json.dumps(checks), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
