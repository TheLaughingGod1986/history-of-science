#!/usr/bin/env python3
"""J2652 (step 3/3 polish): Non-destructively patch P3:09a and P5:02b_wide portrait spillover into v03f-r3.

- Leaves all existing code_graphics_v03f/* and timing_rough_J2652/*v03f_r2* files and SHA-256s untouched.
- Renders ONLY the 2 updated free clips (P3:09a_essay_1844_sealed, P5:02b_joint_papers_lectern_wide) to *_v03f_r3_*.mp4/.jpg.
- Re-assembles the 35-clip QA reel (code_graphics_013_reel_v03f_r3.mp4) and CONTACT_SHEET_v03f_r3_390px.jpg,
  and re-runs polish_gate.py and picture_qa.py.
- Builds hos_013_timing_rough_J2652_v03f_r3.mp4 + phone_contact_v03f_r3_01..06.jpg + ROUGH_MANIFEST_v03f_r3.json
  + asset_inventory_v03f_r3.json, with full ffmpeg decode check and NAS SHA-256 verification.
"""
from __future__ import annotations

import collections
from concurrent.futures import ThreadPoolExecutor
import json
import math
import os
from pathlib import Path
import shutil
import subprocess as sp
import textwrap

import numpy as np
from PIL import Image, ImageDraw, ImageFont

import _build_code_graphics_v03f as cg

EDIT = Path(__file__).resolve().parent
FILM = EDIT.parent
OUT = EDIT / "timing_rough_J2652"
GIT_CG = EDIT / "code_graphics_v03f"
NAS_FILM = Path("/Volumes/data/studio-live/History Of Science/02_Video-Projects") / FILM.name
NAS_CG = NAS_FILM / "07_Edit-Project/code_graphics_v03f"
NAS_ROUGH = NAS_FILM / "07_Edit-Project/timing_rough_J2652"
OWB_ROOT = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
SCRATCH = Path(os.environ.get("STUDIO_SCRATCH", "/private/tmp")) / "J2652-render-v03f-r3"
FONT = "/System/Library/Fonts/Supplemental/Arial.ttf"

PATCH_IDS = {"P3:09a_essay_1844_sealed", "P5:02b_joint_papers_lectern_wide"}
PENDING_RETAKE_ROWS = {
    "P1:03a_unlabelled_birds",
    "P1:07_darwin_1837_desk",
    "P3:02a_malthus_lamplight",
}


def render_patched_clip(idx: int, row: dict, row_cues: list[dict]) -> dict:
    assert cg._G_BASE is not None
    pnum = int(row["part"])
    rid = row["id"]
    dur = round(float(row["t_end_s"]) - float(row["t_s"]), 2)
    n_frames = max(15, int(round(dur * cg.FPS)))
    hero_idx = n_frames // 2

    cg_name = f"code_graphic_013_v03f_r3_p{pnum}_{rid}.mp4"
    still_name = f"code_graphic_013_v03f_r3_p{pnum}_{rid}.jpg"
    mp4_path = NAS_CG / cg_name
    still_path = NAS_CG / still_name
    assert not mp4_path.exists(), f"Refusing overwrite on NAS: {mp4_path}"

    cmd = [
        "ffmpeg", "-y", "-v", "error",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{cg.W}x{cg.H}", "-r", str(cg.FPS),
        "-i", "-",
        "-an", "-c:v", "libx264", "-preset", "ultrafast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-threads", "2", str(mp4_path),
    ]
    enc = sp.Popen(cmd, stdin=sp.PIPE)
    min_mean = 999.0
    min_p95 = 999.0
    min_std = 999.0
    try:
        for f_idx in range(n_frames):
            t = f_idx / cg.FPS
            shift_x = int(8 * math.sin(2 * math.pi * (t / max(dur, 1.5)) + idx * 0.37))
            frame_arr = np.roll(cg._G_BASE, shift_x, axis=1).copy()
            im = Image.fromarray(frame_arr, "RGB")
            d = ImageDraw.Draw(im)
            cg.render_row_frame(im, d, row, t, dur, row_cues, cg._G_SCANS, cg._G_PORTRAITS)
            if f_idx in (0, hero_idx, n_frames - 1):
                gray = np.asarray(im.convert("L"), dtype=np.float32)
                min_mean = min(min_mean, float(gray.mean()))
                min_p95 = min(min_p95, float(np.percentile(gray, 95)))
                min_std = min(min_std, float(gray.std()))
            if f_idx == hero_idx:
                im.save(still_path, quality=92)
            assert enc.stdin is not None
            enc.stdin.write(im.tobytes())
    finally:
        if enc.stdin:
            enc.stdin.close()
        if enc.wait() != 0:
            raise RuntimeError(f"ffmpeg failed on {cg_name}")

    return {
        "idx": idx,
        "id": f"P{pnum}:{rid}",
        "source_row_v02": row["source_row_v02"],
        "source_kind": row["source_kind"],
        "file": cg_name,
        "nas_path": str(mp4_path),
        "still": still_name,
        "t_s": row["t_s"],
        "t_end_s": row["t_end_s"],
        "use_s": dur,
        "encoded_frames": n_frames,
        "encoded_s": round(n_frames / cg.FPS, 2),
        "fps": cg.FPS,
        "min_sample_mean_luma": round(min_mean, 2),
        "min_sample_p95": round(min_p95, 2),
        "min_sample_std": round(min_std, 2),
        "near_black": "PASS" if (min_mean >= 28.0 and min_p95 >= 50.0) else "FAIL",
        "sha256_mp4": cg.digest(mp4_path),
        "sha256_still": cg.digest(still_path),
        "spend": "£0",
    }


def main() -> None:
    assert not (OUT / "ROUGH_MANIFEST_v03f_r3.json").exists(), "v03f_r3 already exists; refusing overwrite"
    arch_items = json.loads((EDIT / "archive_pulls_v01/ARCHIVE_PULLS_RAW_v01.json").read_text())
    for item in arch_items:
        p = Path(item["nas_raw"])
        assert p.exists() and cg.digest(p) == item["sha256"], f"Raw archive mismatch: {p}"
    cg._init_worker(arch_items)

    plan = json.loads((EDIT / "PICTURE_PLAN_v03f.json").read_text())
    all_cues = [c for c in plan["overlay_cues"] if c.get("status") == "ANCHORED"]
    free_rows = [r for r in plan["rows"] if r["source_kind"] in ("code_graphic", "free_archive")]

    prev_cg = json.loads((GIT_CG / "CODE_GRAPHICS_v03f.json").read_text())
    rendered_rows = list(prev_cg["rendered_clips"])

    for idx, r in enumerate(free_rows):
        rk = f"P{r['part']}:{r['id']}"
        if rk in PATCH_IDS:
            ov = [
                c for c in all_cues
                if max(float(r["t_s"]), float(c["display_start_s"])) < min(float(r["t_end_s"]), float(c["display_end_s"]))
            ]
            rec = render_patched_clip(idx, r, ov)
            assert rec["near_black"] == "PASS", f"Near-black failed on {rk}"
            rendered_rows[idx] = rec
            print(f"Patched {rk} -> {rec['file']} ({rec['sha256_mp4'][:12]})", flush=True)
        else:
            existing = rendered_rows[idx]
            assert cg.digest(Path(existing["nas_path"])) == existing["sha256_mp4"], f"Existing clip hash mismatch: {rk}"

    # Build 390px contact sheet of all 35 r3 free clips
    cols, tw, th = 4, 390, 219
    rows_n = math.ceil(len(rendered_rows) / cols)
    sheet_im = Image.new("RGB", (cols * tw, rows_n * (th + 42)), (28, 34, 44))
    sd = ImageDraw.Draw(sheet_im)
    sfont = cg.fnt(18, italic=True)
    for i, rec in enumerate(rendered_rows):
        st = Image.open(NAS_CG / rec["still"]).resize((tw, th), Image.Resampling.LANCZOS)
        x, y = (i % cols) * tw, (i // cols) * (th + 42)
        sheet_im.paste(st, (x, y))
        sd.text((x + 6, y + th + 4), f"{rec['id'][:30]} ({rec['t_s']:.2f}-{rec['t_end_s']:.2f}s)", fill=cg.CREAM, font=sfont)
    sheet_path = GIT_CG / "CONTACT_SHEET_v03f_r3_390px.jpg"
    sheet_im.save(sheet_path, quality=90)
    shutil.copy2(sheet_path, NAS_CG / sheet_path.name)

    # Build r3 QA reel & run polish_gate + picture_qa
    cuts, pool = [], []
    cur_t = 0.0
    for rec in rendered_rows:
        dur = rec["encoded_s"]
        cuts.append({
            "row": rec["id"],
            "timeline_in": round(cur_t, 3),
            "timeline_out": round(cur_t + dur, 3),
            "source": rec["file"],
            "upscale": 1.0,
            "framing": {"offset": 0.0},
            "video": True,
        })
        pool.append({"file_id": rec["file"], "title": f"own code graphic {rec['id']}"})
        cur_t += dur

    concat_txt = NAS_CG / "concat_list_v03f_r3.txt"
    concat_txt.write_text("".join(f"file '{NAS_CG / rec['file']}'\n" for rec in rendered_rows))
    reel_mp4 = NAS_CG / "code_graphics_013_reel_v03f_r3.mp4"
    sp.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(concat_txt), "-c", "copy", str(reel_mp4)], check=True)

    (GIT_CG / "cuts_v03f_r3_cg.json").write_text(json.dumps(cuts, indent=2) + "\n")
    (GIT_CG / "pool_v03f_r3_cg.json").write_text(json.dumps(pool, indent=2) + "\n")

    pg_json = GIT_CG / "polish_gate_v03f_r3.json"
    pg_res = sp.run([
        "python3", str(OWB_ROOT / "scripts/polish_gate.py"),
        str(reel_mp4),
        "--cuts", str(GIT_CG / "cuts_v03f_r3_cg.json"),
        "--out", str(pg_json),
        "--no-jitter",
    ], capture_output=True, text=True, check=True)
    (GIT_CG / "polish_gate_v03f_r3.txt").write_text(pg_res.stdout)
    print(pg_res.stdout, end="")

    pqa_dir = GIT_CG / "picture_qa_v03f_r3"
    pqa_dir.mkdir(parents=True, exist_ok=True)
    pqa_res = sp.run([
        "python3", str(OWB_ROOT / "scripts/picture_qa.py"),
        str(reel_mp4),
        "--cuts", str(GIT_CG / "cuts_v03f_r3_cg.json"),
        "--pool", str(GIT_CG / "pool_v03f_r3_cg.json"),
        "--out-dir", str(pqa_dir),
        "--no-jitter",
    ], capture_output=True, text=True, check=True)
    (GIT_CG / "picture_qa_v03f_r3.txt").write_text(pqa_res.stdout)
    print(pqa_res.stdout, end="")

    cg_manifest = {
        "film": "013_Darwin-Wallace-Evolution",
        "version": "v03f_r3",
        "task": "J2652",
        "plan_sha256": cg.digest(EDIT / "PICTURE_PLAN_v03f.json"),
        "spend": "£0",
        "credits_spent": 0,
        "fps": cg.FPS,
        "resolution": f"{cg.W}x{cg.H}",
        "rendered_clips_count": len(rendered_rows),
        "reel_nas_path": str(reel_mp4),
        "reel_sha256": cg.digest(reel_mp4),
        "contact_sheet_390px": str(sheet_path.relative_to(EDIT)),
        "rendered_clips": rendered_rows,
    }
    (GIT_CG / "CODE_GRAPHICS_v03f_r3.json").write_text(json.dumps(cg_manifest, indent=2) + "\n")
    for fn in (
        "cuts_v03f_r3_cg.json",
        "pool_v03f_r3_cg.json",
        "CODE_GRAPHICS_v03f_r3.json",
        "polish_gate_v03f_r3.json",
        "polish_gate_v03f_r3.txt",
        "picture_qa_v03f_r3.txt",
    ):
        shutil.copy2(GIT_CG / fn, NAS_CG / fn)

    # Build complete v03f_r3 diagnostic rough
    if SCRATCH.exists():
        shutil.rmtree(SCRATCH)
    SCRATCH.mkdir(parents=True, exist_ok=True)

    vo = NAS_FILM / "02_Voiceover/hos_013_vo_v03a.wav"
    assert cg.digest(vo) == plan["vo_sha256"], "VO WAV hash mismatch"
    cg_by_row = {rec["id"]: rec for rec in rendered_rows}

    raw_assets: dict[str, dict] = {}
    for r in plan["rows"]:
        if r["source_kind"] not in ("new_mint_quality", "existing_plate_reuse"):
            continue
        key = "P1:01_study_beaks" if r["source_kind"] == "existing_plate_reuse" else r["source_row_v02"]
        part, rid = key.split(":")
        raw = NAS_FILM / "04_Generated-Clips/archive_v01_pass1" / f"P{int(part[1:]):02d}_{rid}_t1.mp4"
        receipt = Path(str(raw) + ".sha256.json")
        if raw.exists() and receipt.exists():
            expected = json.loads(receipt.read_text())["sha256"]
            assert cg.digest(raw) == expected, f"Archive receipt mismatch: {raw.name}"
            dur_av = float(sp.check_output([
                "ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(raw)
            ]))
            raw_assets[r["source_row_v02"]] = {
                "source": str(raw),
                "source_sha256": expected,
                "available_s": dur_av,
            }

    watermark = SCRATCH / "diagnostic_watermark.png"
    wi = Image.new("RGBA", (960, 540), (0, 0, 0, 0))
    wd = ImageDraw.Draw(wi)
    wd.rectangle((8, 502, 490, 534), fill=(0, 0, 0, 190))
    wd.text((12, 507), "TIMING ONLY - RAW TAKE - NOT KEEP", font=ImageFont.truetype(FONT, 18), fill=(255, 235, 0, 255))
    wi.save(watermark)

    def render_beat(item: tuple[int, dict]) -> tuple[int, Path, dict]:
        i, r = item
        row_key = f"P{r['part']}:{r['id']}"
        duration = round(r["t_end_s"] - r["t_s"], 2)
        target = SCRATCH / f"row_{i:03d}.mp4"
        frame = SCRATCH / f"frame_{i:03d}.jpg"

        if r["source_kind"] in ("code_graphic", "free_archive"):
            cg_rec = cg_by_row[row_key]
            cg_path = Path(cg_rec["nas_path"])
            sp.run([
                "ffmpeg", "-v", "error", "-y", "-i", str(cg_path),
                "-vf", "scale=960:540:flags=lanczos,setsar=1,fps=50",
                "-frames:v", str(round(duration * 50)),
                "-an", "-c:v", "libx264", "-preset", "ultrafast", "-crf", "23", "-pix_fmt", "yuv420p",
                "-threads", "2", str(target),
            ], check=True)
            record = {
                "row": row_key,
                "start_s": r["t_s"],
                "end_s": r["t_end_s"],
                "status": "v03f_free_render",
                "source": str(cg_path),
                "source_offset_s": 0.0,
                "source_sha256": cg_rec["sha256_mp4"],
                "crop": None,
                "reason": "Built £0 v03f-r3 1920x1080@50fps render (exact beat duration and word-anchored cues; zero portrait overlap)",
            }
        elif r["source_row_v02"] in raw_assets:
            ra = raw_assets[r["source_row_v02"]]
            source = ra["source"]
            avail = ra["available_s"]
            offset = float(r["source_window_s"][0])
            retime_factor = None
            if r["source_row_v02"] == "P2:11_island_split_vision":
                retime_factor = round(8.00 / avail, 6)
            elif r["source_row_v02"] == "P3:02b_notebook_d_open":
                offset = round(7.90 - duration, 2)
            is_detail = ("_beat2" in r["id"] or r["id"].endswith("_detail"))
            crop = "crop=trunc(iw*0.88/2)*2:trunc(ih*0.88/2)*2," if is_detail else ""
            if retime_factor is not None:
                vf = f"setpts={retime_factor:.6f}*PTS,trim=start={offset:.3f}:duration={duration:.3f},setpts=PTS-STARTPTS,{crop}scale=960:540:flags=lanczos,setsar=1,fps=50"
                args = ["-i", source, "-i", str(watermark)]
            else:
                assert offset + duration <= avail + 0.002
                vf = f"{crop}scale=960:540:flags=lanczos,setsar=1,fps=50"
                args = ["-ss", str(offset), "-i", source, "-i", str(watermark)]
            sp.run([
                "ffmpeg", "-v", "error", "-y", *args,
                "-filter_complex", f"[0:v]{vf}[base];[base][1:v]overlay=0:0",
                "-frames:v", str(round(duration * 50)),
                "-an", "-c:v", "libx264", "-preset", "ultrafast", "-crf", "26", "-pix_fmt", "yuv420p",
                "-threads", "2", str(target),
            ], check=True)
            note = "Raw first take only; NOT KEEP"
            if r["source_row_v02"] in PENDING_RETAKE_ROWS:
                note += " (pending Quality retake per Chief #6822411223)"
            elif retime_factor is not None:
                note += f" (retimed x{retime_factor:.4f} 7.917->8.00s per Chief #6822411223, no freeze)"
            elif r["source_row_v02"] == "P3:02b_notebook_d_open":
                note += f" (shifted in-point {offset:.2f}-7.90s per Chief #6822305911/#6822411223)"
            record = {
                "row": row_key,
                "start_s": r["t_s"],
                "end_s": r["t_end_s"],
                "status": "raw_pass1_take",
                "source": source,
                "source_offset_s": offset,
                "source_sha256": ra["source_sha256"],
                "retime_factor": retime_factor,
                "crop": "centred 88 percent diagnostic detail" if is_detail else None,
                "reason": note,
            }
        else:
            reason = "Unminted Quality row — awaits J2529 Pass-1 Part 5/6 generation (0 credits spent)"
            im = Image.new("RGB", (960, 540), "#293340")
            d = ImageDraw.Draw(im)
            lines = [
                "J2652 DIAGNOSTIC — UNMINTED PASS-1 ROW",
                row_key,
                f"{r['t_s']:.2f}–{r['t_end_s']:.2f} s ({duration:.2f} s)",
                reason,
                "",
                *textwrap.wrap(r["shot_description"], 64),
            ]
            d.multiline_text((28, 25), "\n".join(lines), font=ImageFont.truetype(FONT, 22), fill="white", spacing=7)
            slate = SCRATCH / f"row_{i:03d}.png"
            im.save(slate)
            sp.run([
                "ffmpeg", "-v", "error", "-y", "-loop", "1", "-framerate", "50", "-i", str(slate),
                "-vf", "setsar=1,fps=50", "-frames:v", str(round(duration * 50)),
                "-an", "-c:v", "libx264", "-preset", "ultrafast", "-crf", "27", "-pix_fmt", "yuv420p",
                "-threads", "2", str(target),
            ], check=True)
            record = {
                "row": row_key,
                "start_s": r["t_s"],
                "end_s": r["t_end_s"],
                "status": "diagnostic_slate",
                "source": None,
                "source_offset_s": None,
                "source_sha256": None,
                "crop": None,
                "reason": reason,
            }

        sp.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{duration / 2:.3f}", "-i", str(target), "-frames:v", "1", str(frame)], check=True)
        return i, frame, record

    results = []
    with ThreadPoolExecutor(max_workers=4) as ex:
        for res in ex.map(render_beat, list(enumerate(plan["rows"]))):
            results.append(res)
    results.sort(key=lambda x: x[0])
    inventory = [r[2] for r in results]
    sheets = [(r[1], r[2]) for r in results]

    concat = SCRATCH / "concat.txt"
    concat.write_text("".join(f"file 'row_{i:03d}.mp4'\n" for i in range(len(plan["rows"]))))

    ass = SCRATCH / "onsets.ass"

    def stamp(t: float) -> str:
        return f"{int(t // 3600)}:{int(t // 60) % 60:02d}:{t % 60:05.2f}"

    header = (
        "[Script Info]\nScriptType: v4.00+\nPlayResX: 960\nPlayResY: 540\n[V4+ Styles]\n"
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, "
        "Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, "
        "Alignment, MarginL, MarginR, MarginV, Encoding\n"
        "Style: Default,Arial,20,&H0000FFFF,&H0000FFFF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,3,2,0,8,20,20,12,1\n"
        "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
    )
    events = [
        f"Dialogue: 0,{stamp(c['display_start_s'])},{stamp(c['display_end_s'])},Default,,0,0,0,,PLANNED CUE: {c['overlay'].get('line_1', c['overlay'].get('label', ''))}"
        for c in plan["overlay_cues"] if c["status"] == "ANCHORED"
    ]
    ass.write_text(header + "\n".join(events) + "\n")

    master = SCRATCH / "hos_013_timing_rough_J2652_v03f_r3.mp4"
    sp.run([
        "ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(concat),
        "-i", str(vo), "-i", str(ass),
        "-map", "0:v", "-map", "1:a", "-map", "2:s",
        "-c:v", "copy", "-c:s", "mov_text",
        "-threads", "2", "-c:a", "aac", "-b:a", "192k", "-af", "apad", "-t", "515",
        "-movflags", "+faststart", str(master),
    ], check=True)
    sp.run(["ffmpeg", "-v", "error", "-i", str(master), "-f", "null", "-"], check=True)

    n_pages = math.ceil(len(sheets) / 20)
    sheet_paths = []
    for page in range(n_pages):
        im = Image.new("RGB", (390 * 4, 260 * 5), "#202733")
        d = ImageDraw.Draw(im)
        for k, (path, r) in enumerate(sheets[page * 20:(page + 1) * 20]):
            x = (k % 4) * 390
            y = (k // 4) * 260
            thumb = Image.open(path).resize((390, 219), Image.Resampling.LANCZOS)
            im.paste(thumb, (x, y))
            tag = "FREE" if r["status"] == "v03f_free_render" else ("RAW" if r["status"] == "raw_pass1_take" else "SLATE")
            d.text((x + 4, y + 221), f"{r['row']} [{tag}]\n{r['start_s']:.2f}–{r['end_s']:.2f}s", font=ImageFont.truetype(FONT, 12), fill="white")
        dest_git = OUT / f"phone_contact_v03f_r3_{page + 1:02d}.jpg"
        im.save(dest_git, quality=90)
        sheet_paths.append(dest_git)

    NAS_ROUGH.mkdir(parents=True, exist_ok=True)
    copies = []
    for src in [master, *sheet_paths]:
        dest = NAS_ROUGH / src.name
        assert not dest.exists(), f"Refusing overwrite on NAS: {dest}"
        shutil.copy2(src, dest)
        assert cg.digest(src) == cg.digest(dest)
        copies.append({"path": str(dest), "sha256": cg.digest(dest)})

    counts = collections.Counter(r["status"] for r in inventory)
    (OUT / "asset_inventory_v03f_r3.json").write_text(json.dumps(inventory, indent=2, ensure_ascii=False) + "\n")
    (OUT / "ROUGH_MANIFEST_v03f_r3.json").write_text(json.dumps({
        "files": copies,
        "vo_sha256": cg.digest(vo),
        "plan_sha256": cg.digest(EDIT / "PICTURE_PLAN_v03f.json"),
        "code_graphics_v03f_r3_sha256": cg.digest(GIT_CG / "CODE_GRAPHICS_v03f_r3.json"),
        "duration_s": 515,
        "fps": 50,
        "credits_spent": 0,
        "gbp_spent": 0,
        "approved": False,
        "status_counts": dict(counts),
        "slates": counts["diagnostic_slate"],
        "limitations": (
            "All 35 £0 code-graphic/archive beats use finished v03f-r3 1920x1080@50fps renders (with double-portrait "
            "overlap eliminated on P5:02b_wide and P3:09a). 58 beats use receipt-verified Pass-1 takes marked NOT KEEP "
            "(including Chief #6822411223 P2:11 x1.0105 retime and P3:02b 3.82-7.90s window; rows P1:03a, P1:07, P3:02a "
            "still await Pass-1 retakes). 11 beats (P5:08a through P6:08b) remain explicit slates awaiting J2529 Pass-1 "
            "Part 5/6 generation. No music/SFX; no audio or moving-video perception claimed."
        ),
    }, indent=2, ensure_ascii=False) + "\n")
    shutil.rmtree(SCRATCH, ignore_errors=True)
    print(f"V03F_R3 COMPLETE: {dict(counts)} — NAS COPY & FULL DECODE VERIFIED", flush=True)


if __name__ == "__main__":
    main()
