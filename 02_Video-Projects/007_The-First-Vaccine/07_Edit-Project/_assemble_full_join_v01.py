#!/usr/bin/env python3
"""HOS 007 — Full Join v01 assembler for Parts 01–05 (J0827).

Joins the 5 passed part roughs (with the two £0 J0827 repeat-shot fixes folded into Part 01 and Part 05)
into `hos_007_full_join_v01.mp4` on the locked VO, with the HOS house teaching cards as laid.
Runs freezedetect, polish_gate.py, picture_qa.py, and 0.5-second sweep checks on the fixed cuts.
£0 spend, no new mints, no music bed, no upload.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess as sp
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1920, 1080, 24
FONT = "/System/Library/Fonts/Supplemental/Didot.ttc"

EDIT_DIR = Path(__file__).resolve().parent
FILM_DIR = EDIT_DIR.parent
HOS_ROOT = FILM_DIR.parent.parent
OWB_ROOT = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
MEDIA_DIR = Path("/Users/benjaminoats/YouTube/hos-007-vaccine/02_Video-Projects/007_The-First-Vaccine")
PRECHECK_ROOT = MEDIA_DIR / "07_Edit-Project/_precheck"
OUT_DIR = PRECHECK_ROOT / "full_join_v01"
DESK_DIR = EDIT_DIR / "_desk/007/full_join_v01"
UAT_ROOT = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT"


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def probe_dur(p: Path) -> float:
    return float(
        sp.check_output(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
            text=True,
        ).strip()
    )


def probe_frames(p: Path) -> int:
    return int(
        sp.check_output(
            [
                "ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0",
                "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", str(p),
            ],
            text=True,
        ).strip()
    )


def contact_sheet(video: Path, cuts: list[dict], out_dir: Path, path: Path) -> None:
    cols, tw, th = 6, 320, 180
    rows = (len(cuts) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw, rows * (th + 26)), (28, 22, 18))
    d = ImageDraw.Draw(sheet)
    f = ImageFont.truetype(FONT, 15, index=0)
    for i, c in enumerate(cuts):
        mid = (c["timeline_in"] + c["timeline_out"]) / 2.0
        jpg = out_dir / f"_fcs_{i:03d}.jpg"
        sp.run(
            ["ffmpeg", "-y", "-v", "error", "-ss", f"{mid:.3f}", "-i", str(video), "-frames:v", "1", "-vf", f"scale={tw}:{th}", str(jpg)],
            check=True,
        )
        x, y = (i % cols) * tw, (i // cols) * (th + 26)
        sheet.paste(Image.open(jpg), (x, y))
        t = c["timeline_in"]
        d.text((x + 5, y + th + 4), f"#{i+1:02d} P{c['part']}:{c['row'][:16]} {int(t // 60)}:{t % 60:05.2f}", font=f, fill=(240, 232, 215))
        jpg.unlink(missing_ok=True)
    sheet.save(path, quality=88)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    DESK_DIR.mkdir(parents=True, exist_ok=True)

    summary = json.loads((EDIT_DIR / "_desk/007/PART_ROUGHS_v01_SUMMARY.json").read_text())
    expected_shas = {r["part"]: r["sha256"] for r in summary}

    cuts_out = []
    pool_out = []
    seen_pool = set()
    meta_parts = []
    concat_lines = []
    offset_s = 0.0
    total_frames = 0

    for pno in range(1, 6):
        pstr = f"{pno:02d}"
        slug = f"part{pstr}_rough_v01"
        mp4 = PRECHECK_ROOT / slug / f"hos_007_{slug}.mp4"
        cuts_path = EDIT_DIR / "_desk/007" / slug / f"cuts_{slug}.json"
        pool_path = EDIT_DIR / "_desk/007" / slug / f"pool_{slug}.json"
        rmeta_path = EDIT_DIR / "_desk/007" / slug / f"ROUGH_META_part{pstr}_v01.json"

        digest = sha256_file(mp4)
        assert digest == expected_shas[pno], f"Part {pstr} sha mismatch: {digest} != {expected_shas[pno]}"
        rmeta = json.loads(rmeta_path.read_text())
        dur = float(rmeta["picture_s"])
        frames = int(rmeta["frames"])

        cuts = json.loads(cuts_path.read_text())
        pool = json.loads(pool_path.read_text())

        for c in cuts:
            row = dict(c)
            row["part"] = pno
            row["cut_no"] = len(cuts_out) + 1
            row["part_timeline_in"] = c["timeline_in"]
            row["part_timeline_out"] = c["timeline_out"]
            row["timeline_in"] = round(c["timeline_in"] + offset_s, 4)
            row["timeline_out"] = round(c["timeline_out"] + offset_s, 4)
            row["film_t"] = round(c["timeline_in"] + offset_s, 2)
            cuts_out.append(row)

        for e in pool:
            if e["file"] not in seen_pool:
                seen_pool.add(e["file"])
                pool_out.append(dict(e))

        concat_lines.append(f"file '{mp4}'")
        meta_parts.append({
            "part": pno,
            "slug": slug,
            "file": str(mp4),
            "sha256": digest,
            "duration_s": dur,
            "frames": frames,
            "offset_s": round(offset_s, 4),
            "cuts": len(cuts),
        })
        offset_s += dur
        total_frames += frames

    concat_txt = OUT_DIR / "concat.txt"
    concat_txt.write_text("\n".join(concat_lines) + "\n")
    joined_mp4 = OUT_DIR / "hos_007_full_join_v01.mp4"
    sp.run(
        [
            "ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
            "-i", str(concat_txt), "-c", "copy", "-movflags", "+faststart", str(joined_mp4),
        ],
        check=True,
    )

    joined_dur = round(probe_dur(joined_mp4), 3)
    joined_frames = probe_frames(joined_mp4)
    joined_sha = sha256_file(joined_mp4)

    # Freezedetect across full join
    fd = sp.run(
        ["ffmpeg", "-i", str(joined_mp4), "-vf", "freezedetect=n=-60dB:d=0.8", "-map", "0:v", "-f", "null", "-"],
        stderr=sp.PIPE, text=True,
    ).stderr
    freeze = [l.split("] ", 1)[1] for l in fd.splitlines() if "freezedetect" in l and "lavfi.freezedetect" in l]
    freeze_path = DESK_DIR / "full_join_v01_freezedetect.log"
    freeze_path.write_text("\n".join(freeze) + ("\n" if freeze else ""))

    cuts_json_path = DESK_DIR / "cuts_full_join_v01.json"
    pool_json_path = DESK_DIR / "pool_full_join_v01.json"
    cuts_json_path.write_text(json.dumps(cuts_out, indent=2) + "\n")
    pool_json_path.write_text(json.dumps(pool_out, indent=2) + "\n")

    # Reviewed-ok for board v02 reuse_of 8-second Veo plates across the full join (Chief PASS J0820:
    # "Every reuse is the board's reuse_of") + 11_mother_window Georgian window mullion
    rev_ok = {
        "11_mother_window_t1.mp4": {
            "kinds": ["split panel"],
            "note": "Georgian cottage window mullion in 3D cartoon plate 11_mother_window_t1.mp4 (Chief KEEP J0352), not a split-panel seam.",
        },
        "01_cow_meadow_t1.mp4": {
            "kinds": ["reuse"],
            "note": "Board v02 reuse_of P1:01_cow_meadow on P4:08c_cow_again (4.60-7.89 s) and P5:02_cow_again (0.84-7.88 s); Chief PASS J0820.",
        },
        "02_doctor_case_t1.mp4": {
            "kinds": ["reuse"],
            "note": "Board v02 reuse_of P1:02_doctor_case on P1:09c_case_again, reframed in J0827 Fix 2 to tight 1.88x crop on silver lancet in crimson velvet (1.20-5.53 s); Chief PASS J0820 / J0827.",
        },
        "03_globe_lights_t1.mp4": {
            "kinds": ["reuse"],
            "note": "Board v02 reuse_of P5:03_globe_lights (0.00-3.50 s) on P1:03b_globe_tease (3.80-7.92 s, 0.00 s overlap); Chief PASS J0820.",
        },
        "03_phipps_stool_t1.mp4": {
            "kinds": ["reuse"],
            "note": "Board v02 reuse_of P3:03_phipps_stool (0.00-4.42 s) on P3:09b_phipps_again (4.68-7.89 s, 0.00 s overlap); Chief PASS J0820.",
        },
        "03_table_three_t1.mp4": {
            "kinds": ["reuse"],
            "note": "Board v02 reuse_of P1:03_table_three on P5:11_table_three_again (2.18-7.89 s); Chief PASS J0820.",
        },
        "04_health_workers_t1.mp4": {
            "kinds": ["reuse"],
            "note": "J0827 Fix 1a: P5:06c_assembly_again (7:35.13-7:39.25) uses strictly unused back half (3.833-7.958 s, 0.00 s overlap with P5:04_health_workers 0.000-3.833 s) at 1.18x framing; Chief J0827 brief.",
        },
        "05_kit_opens_t1.mp4": {
            "kinds": ["reuse"],
            "note": "Board v02 reuse_of P5:05_kit_opens on P5:07b_kit_again (2.68-7.89 s); Chief PASS J0820.",
        },
        "05_quill_writes_t1.mp4": {
            "kinds": ["reuse"],
            "note": "Board v02 reuse_of P3:05_quill_writes on P4:01_page_turns (2.00-4.88 s) and P4:07b_quill_again (4.14-7.90 s); Chief PASS J0820.",
        },
        "06_assembly_1980_t1.mp4": {
            "kinds": ["reuse"],
            "note": "Board v02 reuse_of P5:06_assembly_1980: J0827 Fix 1b trims to tail 5.083-8.000 s (2.917 s) on P5:06d_assembly_front_row (7:39.25-7:42.17) with 1.38x push-in crop on clapping front row; Chief J0827 brief.",
        },
        "06_jesty_family_t1.mp4": {
            "kinds": ["reuse"],
            "note": "Board v02 reuse_of P2:06_jesty_family on P4:07_jesty_again (1.14-7.89 s); Chief PASS J0820.",
        },
        "07_playing_garden_t1.mp4": {
            "kinds": ["reuse"],
            "note": "Board v02 reuse_of P3:07_playing_garden (0.00-5.54 s) on P4:09b_boy_well (4.68-7.89 s); Chief PASS J0820.",
        },
        "09_churchyard_t1.mp4": {
            "kinds": ["reuse"],
            "note": "Board v02 reuse_of P1:09_churchyard (0.00-3.71 s) on P5:06b_churchyard_again (3.74-7.91 s, 0.00 s overlap); Chief PASS J0820.",
        },
        "12_farm_gate_t1.mp4": {
            "kinds": ["reuse"],
            "note": "Board v02 reuse_of P1:12_farm_gate (0.00-4.38 s) on P2:05b_gate_again (4.84-7.92 s, 0.00 s overlap); Chief PASS J0820.",
        },
        "13_casebook_t1.mp4": {
            "kinds": ["reuse"],
            "note": "Board v02 reuse_of P2:13_casebook on P3:09_casebook_open (1.10-6.77 s) and P4:07c_cases_again (2.22-7.89 s); Chief PASS J0820.",
        },
    }
    rev_ok_path = DESK_DIR / "reviewed_ok_full_join_v01.json"
    rev_ok_path.write_text(json.dumps(rev_ok, indent=2) + "\n")

    # Contact sheet of all 93 cuts
    sheet_path = DESK_DIR / "hos_007_full_join_v01_contact_sheet.jpg"
    contact_sheet(joined_mp4, cuts_out, OUT_DIR, sheet_path)

    # 540p UAT proxy
    proxy_path = OUT_DIR / "hos_007_full_join_v01_uat_proxy.mp4"
    sp.run(
        [
            "ffmpeg", "-y", "-v", "error", "-i", str(joined_mp4), "-vf", "scale=960:540",
            "-c:v", "libx264", "-preset", "fast", "-crf", "26",
            "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(proxy_path),
        ],
        check=True,
    )

    if UAT_ROOT.exists():
        uat_dest = UAT_ROOT / "007_full_join_v01"
        uat_dest.mkdir(parents=True, exist_ok=True)
        for f in (joined_mp4, proxy_path, sheet_path):
            shutil.copy2(f, uat_dest / f.name)

    # Run polish_gate.py and picture_qa.py on the full join
    pg_json = DESK_DIR / "polish_gate.json"
    pg_res = sp.run(
        [
            sys.executable, str(OWB_ROOT / "scripts/polish_gate.py"),
            str(joined_mp4), "--cuts", str(cuts_json_path), "--out", str(pg_json),
            "--reviewed-ok", str(rev_ok_path),
        ],
        capture_output=True, text=True,
    )
    (DESK_DIR / "polish_gate.txt").write_text(pg_res.stdout)

    pqa_res = sp.run(
        [
            sys.executable, str(OWB_ROOT / "scripts/picture_qa.py"),
            str(joined_mp4), "--cuts", str(cuts_json_path), "--pool", str(pool_json_path),
            "--out-dir", str(DESK_DIR), "--reviewed-ok", str(rev_ok_path),
        ],
        capture_output=True, text=True,
    )
    (DESK_DIR / "picture_qa.txt").write_text(pqa_res.stdout)

    # 0.5-second sweep across the fixed cuts (P1:09c_case_again, P5:06c_assembly_again, P5:06d_assembly_front_row)
    sys.path.insert(0, str(OWB_ROOT / "scripts"))
    import polish_gate as pg_mod

    sweep_results = {}
    for c in cuts_out:
        if c["row"] in ("09c_case_again", "06c_assembly_again", "06d_assembly_front_row"):
            t_in = float(c["timeline_in"])
            t_out = float(c["timeline_out"])
            samples = []
            t = t_in + 0.25
            while t < t_out - 0.10:
                g = pg_mod.frame_gray(joined_mp4, t)
                samples.append({
                    "film_t_s": round(t, 2),
                    "mean_luma": round(float(g.mean()), 2),
                    "luma_std": round(float(g.std()), 2),
                    "edge_density": round(float(pg_mod.edge_density(g)), 4),
                    "coarse_std": round(float(pg_mod.box_blur(g, 5).std()), 2),
                    "seams": pg_mod.seams(g),
                })
                t += 0.50
            sweep_results[f"P{c['part']}:{c['row']}"] = samples

    meta = {
        "film": "007_The-First-Vaccine",
        "kind": "full_join_v01",
        "job": "J0827",
        "authority": "Chief PASS J0820 (Claude, acting Chief, 22 Oct 2026) + J0827 2 £0 repeat-shot fixes",
        "applied_by": "gemini",
        "no_new_mints": True,
        "spend": "£0 (assembly + 2 £0 repeat-shot fixes only)",
        "file": str(joined_mp4),
        "sha256": joined_sha,
        "size_mb": round(joined_mp4.stat().st_size / 1e6, 2),
        "proxy_file": str(proxy_path),
        "proxy_sha256": sha256_file(proxy_path),
        "duration_s": joined_dur,
        "parts_sum_s": round(offset_s, 3),
        "frames": joined_frames,
        "cuts": len(cuts_out),
        "bed": None,
        "bed_note": "No 05_Music bed (ElevenLabs credit hold until 30 Oct; no new bed without Chief OK). Locked VO in each passed part rough.",
        "freeze_events": freeze,
        "polish_gate_rc": pg_res.returncode,
        "polish_gate_stdout": pg_res.stdout.strip(),
        "picture_qa_rc": pqa_res.returncode,
        "picture_qa_stdout": pqa_res.stdout.strip(),
        "fixed_cuts_0p5s_sweep": sweep_results,
        "parts": meta_parts,
    }
    (DESK_DIR / "JOIN_META_v01.json").write_text(json.dumps(meta, indent=2) + "\n")
    (OUT_DIR / "JOIN_META_v01.json").write_text(json.dumps(meta, indent=2) + "\n")
    (DESK_DIR / "SHA256.txt").write_text(f"{joined_sha}  hos_007_full_join_v01.mp4\n")

    print(json.dumps({
        "sha256": joined_sha,
        "duration_s": joined_dur,
        "frames": joined_frames,
        "cuts": len(cuts_out),
        "freeze_events": len(freeze),
        "polish_gate_rc": pg_res.returncode,
        "picture_qa_rc": pqa_res.returncode,
    }, indent=2))
    if pg_res.returncode != 0 or pqa_res.returncode != 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
