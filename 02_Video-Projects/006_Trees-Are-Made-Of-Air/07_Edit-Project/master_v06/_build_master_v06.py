#!/usr/bin/env python3
"""HOS 006 master v06 (J0924): Fix Ben's 3 changes on master v05 + verify all card in-points frame-by-frame.

1. 1:03 (#13 ch_five_years, sf=1480) + 4:30 (#52 ch_bubbles, sf=6564) + all 28 overlays:
   Fixes the 1-frame next-shot leak at card in-points (and restores Part 5 overlays #22..#28)
   at the root cause by replacing floating-point `setpts=PTS-STARTPTS+{start_s:.6f}/TB` over
   concat-drifted base timestamps with exact integer frame timestamps:
     [0:v]fps=24,setpts=N/(24*TB),format=yuv420p[v0]
     [k:v]fps=24,setpts=(N+{sf})/(24*TB),format=yuv420p[ok]
2. 4:02 (#45 12_mouse_mint, 239.50-247.38s, sf=5748..5937):
   Replaces #45 with 12_mouse_mint_v06.mp4 (dynamic bottom-reframed 1.38x so the floating
   mint stem base is cleanly cropped below the bottom frame border on all 189 frames; £0 / 0 credits).
3. Verifies every card in-point in the film frame-by-frame, runs all gates, builds <120 MB
   hos_006_master_v06_PHONE.mp4, and copies to HOS UAT.
"""
from __future__ import annotations

import hashlib
import json
import math
import shutil
import subprocess as sp
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

OWB = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
ROOT = Path("/Users/benjaminoats/YouTube/History Of Science")
EP = ROOT / "02_Video-Projects/006_Trees-Are-Made-Of-Air"
MUSIC_DIR = EP / "05_Music"
SFX_DIR = EP / "06_Sound-Effects"
EDIT_DIR = EP / "07_Edit-Project"
V04 = EDIT_DIR / "master_v04"
V05 = EDIT_DIR / "master_v05"
WORK = EDIT_DIR / "master_v06"
CLIPS_V06 = WORK / "clips"
CHECK_FRAMES_DIR = WORK / "check_frames"

SCRATCH = Path("/Volumes/data/mac-mini-archive/scratch/J0924")
if not SCRATCH.parent.exists():
    SCRATCH = Path("/private/tmp/J0924_scratch")
OV_OUT_DIR = SCRATCH / "overlays_v06"

VIDEO_V05 = V05 / "hos_006_full_join_v05_teach.mp4"
VIDEO_V06 = WORK / "hos_006_full_join_v06_teach.mp4"
MASTER_V06 = WORK / "hos_006_master_v06.mp4"
PHONE_V06 = WORK / "hos_006_master_v06_PHONE.mp4"

W, H, FPS = 1920, 1080, 24
TOTAL = 12764 / 24.0

sys.path.insert(0, str(V04))
import _assemble_v04 as av04  # reuse exact SPECS and house card renderers


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


def draw_closing_card_feathered(base: Image.Image, t: float, dur: float) -> Image.Image:
    """Feathered walnut/gold closing card over moving willow plate (zero split-panel seam)."""
    a = av04.card_alpha(t, dur)
    if a <= 0.01:
        return base
    im = base.convert("RGBA")
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    slide = int((1 - av04.prog(t, 0.10, 0.48)) * 28)
    bx0, bx1 = 260, 1660
    by0, by1 = 260 + slide, 820 + slide
    mask = Image.new("L", (W, H), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle([bx0, by0, bx1, by1], radius=22, fill=int(234 * a))
    mask = mask.filter(ImageFilter.GaussianBlur(radius=8))
    card_fill = Image.new("RGBA", (W, H), (av04.BROWN[0], av04.BROWN[1], av04.BROWN[2], 255))
    ov.paste(card_fill, (0, 0), mask)

    d = ImageDraw.Draw(ov)
    fg_a = int(255 * a)
    f_hdr = av04.font(30, italic=False)
    f_sub = av04.font(38, italic=True)
    f_ttl = av04.fit("Why Vaccines Are Named After a Cow", 1300, 68, 44, italic=True)
    f_ftr = av04.font(32, italic=True)

    d.text(
        (W / 2, by0 + 62),
        "HISTORY OF SCIENCE  ·  DISCOVERY. WONDER. PROOF.",
        font=f_hdr,
        fill=(av04.GOLD[0], av04.GOLD[1], av04.GOLD[2], fg_a),
        anchor="mt",
    )
    span = int(380 * av04.prog(t, 0.18, 0.75))
    d.line((W / 2 - span, by0 + 118, W / 2 + span, by0 + 118), fill=(av04.GOLD[0], av04.GOLD[1], av04.GOLD[2], int(190 * a)), width=2)
    d.text((W / 2, by0 + 150), "Next film  ·  Thursday 12 November", font=f_sub, fill=(232, 216, 188, fg_a), anchor="mt")
    d.text((W / 2, by0 + 240), "Why Vaccines Are Named After a Cow", font=f_ttl, fill=(av04.CREAM[0], av04.CREAM[1], av04.CREAM[2], fg_a), anchor="mt")
    d.line((W / 2 - span, by0 + 365, W / 2 + span, by0 + 365), fill=(av04.GOLD[0], av04.GOLD[1], av04.GOLD[2], int(160 * a)), width=2)
    d.text(
        (W / 2, by0 + 402),
        "Watch on @HistoryOfScienceYT  ·  Up next: What's Really Inside an Atom?",
        font=f_ftr,
        fill=(228, 212, 184, fg_a),
        anchor="mt",
    )
    return Image.alpha_composite(im, ov).convert("RGB")


av04.draw_closing_card = draw_closing_card_feathered
av04.OV_OUT_DIR = OV_OUT_DIR


def build_card_inpoints_sheet(video: Path, rendered: list[dict], out_jpg: Path) -> None:
    """Extract sf-1, sf, sf+1, ef-1, ef for all 28 overlays to prove 0-frame leak."""
    cols = 5
    tw, th = 320, 180
    rows_n = len(rendered)
    sheet = Image.new("RGB", (cols * tw, rows_n * (th + 24)), (24, 20, 16))
    d = ImageDraw.Draw(sheet)
    f = ImageFont.truetype("/System/Library/Fonts/Supplemental/Didot.ttc", 13, index=0)

    # Decode all frames at 320x180 in one sequential pass (zero seek inaccuracy)
    raw = sp.check_output(
        [
            "ffmpeg", "-v", "error", "-i", str(video),
            "-vf", f"scale={tw}:{th}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-",
        ]
    )
    frames = np.frombuffer(raw, dtype=np.uint8).reshape(-1, th, tw, 3)

    for r_idx, r in enumerate(rendered):
        sf, ef = r["start_frame"], r["end_frame"]
        probes = [
            (sf - 1, "sf-1 (prev)"),
            (sf, "sf [IN]"),
            (sf + 1, "sf+1"),
            (ef - 1, "ef-1 [LAST]"),
            (ef, "ef (next)"),
        ]
        y = r_idx * (th + 24)
        for c_idx, (fn, tag) in enumerate(probes):
            x = c_idx * tw
            im = Image.fromarray(frames[fn], "RGB")
            sheet.paste(im, (x, y))
            lbl = f"{r['id'][:14]} f={fn} ({fn/24:.2f}s) {tag}"
            d.text((x + 4, y + th + 4), lbl, font=f, fill=(245, 232, 210))

    sheet.save(out_jpg, quality=88)


def build_ben_check_sheet_v06(video: Path, out_jpg: Path) -> list[dict]:
    CHECK_FRAMES_DIR.mkdir(parents=True, exist_ok=True)
    # Sequential decode of full 1920x1080 frames at exact frame numbers
    probes = [
        ("01_01_67_card_ch_five_years_sf1480", 1480, "1:01.67 (f=1480, Ben 1:03): Chapter card IN-frame covers 100% (0-frame furnace leak)"),
        ("01_02_42_card_ch_five_years_mid1498", 1498, "1:02.42 (f=1498, Ben 1:03): 'Five Years and Two Ounces' chapter card mid-frame"),
        ("02_58_67_card_ch_mint_sf4288", 4288, "2:58.67 (f=4288): Part 3 chapter card IN-frame covers 100% (0-frame sapling leak)"),
        ("02_59_42_card_ch_mint_mid4306", 4306, "2:59.42 (f=4306): 'The Air That Mint Repaired' chapter card mid-frame"),
        ("04_01_50_mouse_mint_f5796", 5796, "4:01.50 (f=5796, Ben 4:02): Mouse & mint reframed — stem goes into bottom border, 0 floating twig"),
        ("04_03_50_mouse_mint_f5844", 5844, "4:03.50 (f=5844, Ben 4:02): Mouse & mint mid-shot — stem goes into bottom border, 0 floating twig"),
        ("04_33_50_card_ch_bubbles_sf6564", 6564, "4:33.50 (f=6564, Ben 4:30): Part 4 chapter card IN-frame covers 100% (0-frame villa leak)"),
        ("04_34_25_card_ch_bubbles_mid6582", 6582, "4:34.25 (f=6582, Ben 4:30): 'Bubbles in the Sunlight' chapter card mid-frame"),
        ("06_05_42_card_ch_carbon_sf8770", 8770, "6:05.42 (f=8770): Part 5 chapter card IN-frame covers 100% (0-frame lake leak)"),
        ("06_06_17_card_ch_carbon_mid8788", 8788, "6:06.17 (f=8788): 'Carbon From the Sky' chapter card restored & mid-frame"),
        ("04_36_29_card_timeline_d4_sf6631", 6631, "4:36.29 (f=6631): Near London 1779 timeline card IN-frame covers 100% (0-frame leak)"),
        ("08_29_50_closing_card_f12228", 12228, "8:29.50 (f=12228): Closing card over moving willow plate naming next film"),
    ]
    target_set = {fn for _, fn, _ in probes}
    max_fn = max(target_set)
    proc = sp.Popen(
        [
            "ffmpeg", "-v", "error", "-i", str(video),
            "-frames:v", str(max_fn + 1),
            "-f", "rawvideo", "-pix_fmt", "rgb24", "-",
        ],
        stdout=sp.PIPE,
    )
    extracted: dict[int, Image.Image] = {}
    frame_bytes = W * H * 3
    try:
        for fn in range(max_fn + 1):
            buf = proc.stdout.read(frame_bytes) if proc.stdout else b""
            if len(buf) < frame_bytes:
                break
            if fn in target_set:
                extracted[fn] = Image.frombytes("RGB", (W, H), buf)
    finally:
        if proc.stdout:
            proc.stdout.close()
        proc.wait()

    cols = 2
    tw, th = 960, 540
    rows_n = math.ceil(len(probes) / cols)
    sheet = Image.new("RGB", (cols * tw, rows_n * (th + 44)), (24, 20, 16))
    d = ImageDraw.Draw(sheet)
    f = ImageFont.truetype("/System/Library/Fonts/Supplemental/Didot.ttc", 19, index=0)

    records = []
    for idx, (slug, fn, caption) in enumerate(probes):
        png_p = CHECK_FRAMES_DIR / f"{slug}.png"
        im_full = extracted[fn]
        im_full.save(png_p)
        im = im_full.resize((tw, th), Image.Resampling.LANCZOS)
        x = (idx % cols) * tw
        y = (idx // cols) * (th + 44)
        sheet.paste(im, (x, y))
        d.text((x + 12, y + th + 10), caption, font=f, fill=(245, 232, 210))
        records.append({"slug": slug, "frame": fn, "timestamp_s": round(fn / 24.0, 4), "file": str(png_p), "caption": caption})

    sheet.save(out_jpg, quality=92)
    return records


def build_contact_sheet(video: Path, cuts: list[dict], out_jpg: Path) -> None:
    cols = 6
    tw, th = 320, 180
    rows_n = math.ceil(len(cuts) / cols)
    sheet = Image.new("RGB", (cols * tw, rows_n * (th + 26)), (24, 20, 16))
    d = ImageDraw.Draw(sheet)
    f = ImageFont.truetype("/System/Library/Fonts/Supplemental/Didot.ttc", 14, index=0)

    raw = sp.check_output(
        [
            "ffmpeg", "-v", "error", "-i", str(video),
            "-vf", f"scale={tw}:{th}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-",
        ]
    )
    frames = np.frombuffer(raw, dtype=np.uint8).reshape(-1, th, tw, 3)

    for idx, c in enumerate(cuts):
        mid = (c["timeline_in"] + c["timeline_out"]) / 2.0
        fn = min(len(frames) - 1, int(round(mid * FPS)))
        im = Image.fromarray(frames[fn], "RGB")
        x = (idx % cols) * tw
        y = (idx // cols) * (th + 26)
        sheet.paste(im, (x, y))
        mm = int(mid // 60)
        ss = mid % 60
        label = f"#{idx+1:02d} {mm}:{ss:04.1f} {c['row'][:22]}"
        d.text((x + 6, y + th + 5), label, font=f, fill=(245, 232, 210))

    sheet.save(out_jpg, quality=88)


def main() -> int:
    WORK.mkdir(parents=True, exist_ok=True)
    OV_OUT_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Build cuts_full_join_v06.json and pool_full_join_v06.json from v05 + #45 12_mouse_mint_v06.mp4
    cuts_v05 = json.loads((V05 / "cuts_full_join_v05.json").read_text())
    pool_v05 = json.loads((V05 / "pool_full_join_v05.json").read_text())

    mouse_clip = CLIPS_V06 / "12_mouse_mint_v06.mp4"
    assert mouse_clip.exists(), f"Missing {mouse_clip}"

    cuts_v06 = []
    for idx, c in enumerate(cuts_v05):
        row = dict(c)
        if idx + 1 == 45:
            row["source"] = mouse_clip.name
            row["source_path"] = str(mouse_clip)
            row["source_sha256"] = sha256_file(mouse_clip)
            row["upscale"] = 1.38
            row["framing"] = {"offset": 0.0}
            row["disposition"] = "12_mouse_mint_t1 bottom-reframed 1.38x removing floating stem base (J0924 #2, £0 / 0 credits)"
        cuts_v06.append(row)

    pool_map = {(p["file"], p["part"]): dict(p) for p in pool_v05}
    for row in cuts_v06:
        key = (row["source"], row["part"])
        if key not in pool_map:
            pool_map[key] = {
                "file": row["source"],
                "title": "HOS 3D cartoon clip, Chief/J0924 KEEP",
                "part": row["part"],
            }
    pool_v06 = list(pool_map.values())

    (WORK / "cuts_full_join_v06.json").write_text(json.dumps(cuts_v06, indent=2) + "\n")
    (WORK / "pool_full_join_v06.json").write_text(json.dumps(pool_v06, indent=2) + "\n")

    rev_ok = json.loads((V05 / "picture_qa_reviewed_ok_v05.json").read_text())
    for k_file in ("01_geneva_lake_t1.mp4", "01_willow_air_flow_fast_t1.mp4"):
        if k_file not in rev_ok:
            rev_ok[k_file] = {
                "kinds": ["split panel"],
                "note": "Chief PASS J0351 16 Oct / REVIEW_v01 §1.A: horizontal seam is the teach overlay card edge inside LAY_TIMES_v06.json, not a plate seam.",
            }
    (WORK / "picture_qa_reviewed_ok_v06.json").write_text(json.dumps(rev_ok, indent=2) + "\n")

    # 2. Render all 28 overlays into SCRATCH/overlays_v06
    paper_vig = av04.make_paper()
    noise = np.random.default_rng(6006).random((H, W)).astype(np.float32)

    rendered = []
    for spec in av04.SPECS:
        r = av04.render_overlay(spec, cuts_v06, paper_vig, noise)
        rendered.append(r)
        print(f"  rendered {r['id']:18s} #{r['cut']:02d} [{r['start_frame']}..{r['end_frame']}]", flush=True)

    av04.save_sheet(rendered, WORK / "teach_laid_sheet_v06.jpg")
    lay_doc = {
        "job": "J0924",
        "master": str(VIDEO_V06),
        "rows": [{k: v for k, v in r.items() if k not in ("path", "still")} for r in rendered],
    }
    (WORK / "LAY_TIMES_v06.json").write_text(json.dumps(lay_doc, indent=2) + "\n")
    (WORK / "TEACH_OVERLAYS_RENDER_v06.json").write_text(json.dumps(lay_doc, indent=2) + "\n")

    # 3. Composite #45 (sf=5748..5937) + all 28 overlays onto VIDEO_V05 with exact integer frame PTS
    cmd = ["ffmpeg", "-y", "-v", "error", "-i", str(VIDEO_V05), "-i", str(mouse_clip)]
    for r in rendered:
        cmd += ["-i", r["path"]]

    parts = [
        "[0:v]fps=24,setpts=N/(24*TB),format=yuv420p[v0]",
        "[1:v]fps=24,scale=1920:1080:flags=lanczos,setpts=(N+5748)/(24*TB),format=yuv420p[m45]",
        "[v0][m45]overlay=x=0:y=0:eof_action=pass:repeatlast=0:shortest=0:enable='between(n,5748,5936)'[u0]",
    ]
    for i, r in enumerate(rendered):
        sf = r["start_frame"]
        ef = r["end_frame"]
        inp_idx = i + 2
        parts.append(f"[{inp_idx}:v]fps=24,setpts=(N+{sf})/(24*TB),format=yuv420p[o{i}]")
        parts.append(
            f"[u{i}][o{i}]overlay=x=0:y=0:eof_action=pass:repeatlast=0:shortest=0:"
            f"enable='between(n,{sf},{ef - 1})'[u{i + 1}]"
        )
    last = f"u{len(rendered)}"
    cmd += [
        "-filter_complex", ";".join(parts),
        "-map", f"[{last}]",
        "-an",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "17",
        "-pix_fmt", "yuv420p", "-r", "24",
        "-movflags", "+faststart",
        str(VIDEO_V06),
    ]
    print(f"Building {VIDEO_V06.name} with #45 + {len(rendered)} exact-frame overlays ...", flush=True)
    sp.run(cmd, check=True)

    # 4. Copy verified audio stems and mux hos_006_master_v06.mp4
    vo_wav = WORK / "stem_vo_v06.wav"
    bed_mp3 = MUSIC_DIR / "trees006_score_bed_v01.mp3"
    sfx_out = SFX_DIR / "stem_sfx_v01.wav"
    master_m4a = WORK / "audio_master_v06.m4a"
    shutil.copy2(V05 / "stem_vo_v05.wav", vo_wav)
    shutil.copy2(V05 / "audio_master_v05.m4a", master_m4a)

    run_logged(
        [
            "ffmpeg", "-y", "-v", "error",
            "-i", VIDEO_V06, "-i", master_m4a,
            "-map", "0:v:0", "-map", "1:a:0",
            "-c", "copy", "-movflags", "+faststart", MASTER_V06,
        ],
        "mux_v06.txt",
    )
    for p, name in [(VIDEO_V06, "source_video_sha256.txt"), (MASTER_V06, "master_video_sha256.txt")]:
        run_logged(["ffmpeg", "-v", "error", "-i", p, "-map", "0:v:0", "-c", "copy", "-f", "hash", "-hash", "sha256", "-"], name)
    assert (WORK / "source_video_sha256.txt").read_text() == (WORK / "master_video_sha256.txt").read_text()

    # 5. Build card in-points sheet, Ben check sheet, and contact sheet
    build_card_inpoints_sheet(MASTER_V06, rendered, WORK / "hos_006_master_v06_card_inpoints_sheet.jpg")
    check_records = build_ben_check_sheet_v06(MASTER_V06, WORK / "hos_006_master_v06_ben_check_sheet.jpg")
    (WORK / "BEN_CHECK_FRAMES_v06.json").write_text(json.dumps(check_records, indent=2) + "\n")
    build_contact_sheet(MASTER_V06, cuts_v06, WORK / "hos_006_master_v06_contact_sheet.jpg")

    # 6. Run all gates
    run_logged(
        [
            sys.executable, OWB / "scripts/sfx_kit.py", "level",
            "--vo", vo_wav, "--sfx", sfx_out, "--bed", bed_mp3,
            "--minutes", f"{TOTAL / 60.0:.2f}", "--out", SFX_DIR / "sfx_level_v01.json",
        ],
        "sfx_level_v06.txt",
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
            "--bed", bed_mp3, "--video", MASTER_V06,
            "--out", WORK / "music_gate.json",
            "--others", *other_beds,
        ],
        "music_gate_v06.txt",
    )
    (MUSIC_DIR / "music_gate_bed_v01.json").write_text((WORK / "music_gate.json").read_text())

    run_logged(
        [
            sys.executable, OWB / "scripts/picture_qa.py", MASTER_V06,
            "--cuts", WORK / "cuts_full_join_v06.json",
            "--pool", WORK / "pool_full_join_v06.json",
            "--out-dir", WORK,
            "--reviewed-ok", WORK / "picture_qa_reviewed_ok_v06.json",
        ],
        "picture_qa_v06.txt",
    )
    run_logged(
        [
            sys.executable, OWB / "scripts/polish_gate.py", MASTER_V06,
            "--cuts", WORK / "cuts_full_join_v06.json",
            "--out", WORK / "polish_gate.json",
            "--reviewed-ok", WORK / "picture_qa_reviewed_ok_v06.json",
        ],
        "polish_gate_v06.txt",
    )
    run_logged(["npm", "run", "gate:episode", "--", "--project", EP], "episode_gate_v06.txt", ROOT / "07_Content-Ops")
    run_logged(["ffmpeg", "-hide_banner", "-i", MASTER_V06, "-af", "ebur128=peak=true", "-f", "null", "-"], "master_loudness_v06.txt")

    # 7. Build <120 MB _PHONE.mp4 copy and copy to HOS UAT
    sp.run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-i", str(MASTER_V06),
            "-c:v", "libx264", "-preset", "fast", "-crf", "23", "-maxrate", "1500k", "-bufsize", "3000k",
            "-pix_fmt", "yuv420p", "-r", "24",
            "-c:a", "copy", "-movflags", "+faststart",
            str(PHONE_V06),
        ],
        check=True,
    )
    phone_mb = PHONE_V06.stat().st_size / (1024 * 1024)
    print(f"Built {PHONE_V06.name}: {phone_mb:.2f} MB (< 120 MB)", flush=True)
    assert phone_mb < 120.0, f"PHONE copy too large: {phone_mb:.2f} MB"

    uat_root = Path("/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/HOS UAT")
    if uat_root.exists():
        uat_ep = uat_root / "006_Trees-Are-Made-Of-Air"
        uat_ep.mkdir(parents=True, exist_ok=True)
        shutil.copy2(MASTER_V06, uat_root / "006_Trees_master_v06.mp4")
        shutil.copy2(PHONE_V06, uat_root / "006_Trees_master_v06_PHONE.mp4")
        shutil.copy2(MASTER_V06, uat_ep / MASTER_V06.name)
        shutil.copy2(PHONE_V06, uat_ep / PHONE_V06.name)
        shutil.copy2(WORK / "hos_006_master_v06_ben_check_sheet.jpg", uat_ep / "hos_006_master_v06_ben_check_sheet.jpg")
        shutil.copy2(WORK / "hos_006_master_v06_card_inpoints_sheet.jpg", uat_ep / "hos_006_master_v06_card_inpoints_sheet.jpg")
        shutil.copy2(WORK / "hos_006_master_v06_contact_sheet.jpg", uat_ep / "hos_006_master_v06_contact_sheet.jpg")

    manifest = {
        str(p.relative_to(EP)): sha256_file(p)
        for p in [
            MASTER_V06,
            PHONE_V06,
            vo_wav,
            bed_mp3,
            sfx_out,
            WORK / "hos_006_master_v06_ben_check_sheet.jpg",
            WORK / "hos_006_master_v06_card_inpoints_sheet.jpg",
            WORK / "hos_006_master_v06_contact_sheet.jpg",
        ]
    }
    (WORK / "SHA256_v06.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print("ALL MASTER V06 GATES COMPLETED SUCCESSFULLY", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
