#!/usr/bin/env python3
"""HOS 006: Part 03 rough v02 (with P3:06 dropped in) + Part 04 rough v01 + Part 05 rough v01 (J0140).

No spend. VO-first assembly matching _assemble_part03_rough_v01.py:
- Every plate sits at its board time (parts/part-0N_plates_v01.json, t_s from vo_film_start_s)
  for its board use_s, hard cuts, 24 fps 1080p, VO padded with silence to part_end_film_s.
- Media stays out of git: cuts and proxies go to HOS_006_MEDIA/07_Edit-Project/_precheck/<part_rough>/
  and iCloud HOS UAT; metadata, cut lists, freeze logs, contact sheets and picture_qa reports go to
  07_Edit-Project/_desk/006/<part_rough>/ for the PR.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
MEDIA = Path(
    os.environ.get(
        "HOS_006_MEDIA",
        str(Path.home() / "YouTube/hos-006-trees/02_Video-Projects/006_Trees-Are-Made-Of-Air"),
    )
)
HOS_MAIN = Path.home() / "YouTube/History Of Science"
OWB_MAIN = Path.home() / "YouTube/orbit-with-ben"
UAT_ROOT = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT"
FPS = 24
W, H = 1920, 1080
X264 = ["-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-r", str(FPS)]
FONT = "/System/Library/Fonts/Supplemental/Georgia Italic.ttf"


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def probe_dur(p: Path) -> float:
    return float(
        subprocess.check_output(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)]
        )
        .decode()
        .strip()
    )


def contact_sheet(video: Path, cuts: list[dict], out_dir: Path, path: Path) -> None:
    cols, tw, th = 6, 320, 180
    rows = (len(cuts) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw, rows * (th + 28)), (20, 20, 20))
    d = ImageDraw.Draw(sheet)
    f = ImageFont.truetype(FONT, 18)
    for i, c in enumerate(cuts):
        mid = (c["timeline_in"] + c["timeline_out"]) / 2
        jpg = out_dir / f"_sheet_{i:02d}.jpg"
        run(["ffmpeg", "-y", "-ss", f"{mid:.3f}", "-i", str(video), "-frames:v", "1", "-vf", f"scale={tw}:{th}", str(jpg)])
        x, y = (i % cols) * tw, (i // cols) * (th + 28)
        sheet.paste(Image.open(jpg), (x, y))
        t = c["film_t"]
        d.text((x + 6, y + th + 4), f"{c['row']}  {int(t // 60)}:{t % 60:05.2f}", font=f, fill=(235, 235, 235))
        jpg.unlink()
    sheet.save(path, quality=88)


def part03_specs() -> dict[str, dict]:
    p3 = MEDIA / "04_Generated-Clips/part03/raw/v01"
    specs = {}
    for pid in [
        "01_soil_to_sky", "02_hales_branch", "03_water_level", "04_leaf_mist", "05_guess",
        "07_priestley", "08_candles_out", "09_injured_air", "10_mint_jar", "11_candle_tall",
        "12_mouse_mint", "13_fires_breath", "14_trees_breathe", "15_quill_vegetable",
        "17_notebook_tick", "18_dark_window",
    ]:
        specs[pid] = {
            "src": p3 / f"{pid}_t1.mp4",
            "start": 0.0,
            "vf": f"scale={W}:{H},fps={FPS}",
            "upscale": 1.0,
            "disp": "KEEP t1 (Chief, desk #180 6102934743)",
        }
    specs["06_leeds_brewery"] = {
        "src": p3 / "06_leeds_brewery_nofire_crop_v01.mp4",
        "start": 0.0,
        "vf": f"scale={W}:{H},fps={FPS}",
        "upscale": 1.33,
        "disp": "J0160 Vertex t1 top-cropped 1.33x to exclude vat fireboxes (Chief #180 6131279209 / 6133444306)",
    }
    specs["16_repair_reuse"] = {
        "src": p3 / "14_trees_breathe_t1.mp4",
        "start": 3.0,
        "vf": f"scale={W}:{H},fps={FPS}",
        "upscale": 1.0,
        "disp": "REUSE window 3.00-6.84 s of 14_trees_breathe (board reuse_of P3:14_trees_breathe)",
    }
    return specs


def part04_specs() -> dict[str, dict]:
    p3 = MEDIA / "04_Generated-Clips/part03/raw/v01"
    p4 = MEDIA / "04_Generated-Clips/part04/raw/v01"
    return {
        "01_villa": {
            "src": p4 / "01_villa_t1.mp4", "start": 0.0,
            "vf": f"scale={W}:{H},fps={FPS}", "upscale": 1.0,
            "disp": "KEEP Vertex t1 (Chief, desk #180 6131279209)",
        },
        "02_ingenhousz_jars": {
            "src": p4 / "02_ingenhousz_jars_t1.mp4", "start": 0.0,
            "vf": f"scale=2112:1188,crop=1920:1080:96:108,fps={FPS}", "upscale": 1.10,
            "disp": "KEEP Vertex t1, top ceiling light cropped out per Chief note (#180 6131279209)",
        },
        "03_plunge_leaf": {
            "src": p4 / "03_plunge_leaf_t1.mp4", "start": 0.0,
            "vf": f"scale={W}:{H},fps={FPS}", "upscale": 1.0,
            "disp": "KEEP Vertex t1 (Chief, desk #180 6131279209)",
        },
        "04_sunny_window": {
            "src": p4 / "04_sunny_window_t1.mp4", "start": 0.0,
            "vf": f"scale={W}:{H},fps={FPS}", "upscale": 1.0,
            "disp": "KEEP Vertex t1 (Chief, desk #180 6131279209)",
        },
        "05_bubbles_macro": {
            "src": p4 / "05_bubbles_macro_t1.mp4", "start": 0.0,
            "vf": f"scale={W}:{H},fps={FPS}", "upscale": 1.5,
            "disp": "KEEP Flow t1 (Chief, desk #180 6137551906)",
        },
        "06_collect_blaze": {
            "src": p4 / "06_collect_blaze_t3.mp4", "start": 0.0,
            "vf": f"scale=2048:1152,crop=1920:1080:64:0,fps={FPS}", "upscale": 1.60,
            "disp": "Flow Fast t3, bottom 6% trimmed to exclude frame-edge seam (Acting-Chief ruling 14 Oct 20:50Z item 1; PENDING_UAT on review/j0140)",
        },
        "07_priestley_callback": {
            "src": p3 / "11_candle_tall_t1.mp4", "start": 0.0,
            "vf": f"scale={W}:{H},fps={FPS}", "upscale": 1.0,
            "disp": "REUSE window 0.00-6.90 s of P3:11_candle_tall (board reuse_of)",
        },
        "08_explorer_shade": {
            "src": p4 / "08_explorer_shade_t2.mp4", "start": 0.0,
            "vf": f"scale={W}:{H},fps={FPS}", "upscale": 1.5,
            "disp": "Flow Quality t2 (Chief ruling #180 6137551906; PENDING_UAT on review/j0140)",
        },
        "09_bubbles_again": {
            "src": p4 / "05_bubbles_macro_t1.mp4", "start": 4.2,
            "vf": f"scale={W}:{H},fps={FPS}", "upscale": 1.5,
            "disp": "REUSE window 4.20-7.62 s of P4:05_bubbles_macro (board reuse_of)",
        },
        "10_only_green": {
            "src": p4 / "10_only_green_t2.mp4", "start": 0.0,
            "vf": f"scale={W}:{H},fps={FPS}", "upscale": 1.5,
            "disp": "KEEP Flow t2 (Chief, desk #180 6136917197)",
        },
        "11_night_jars": {
            "src": p4 / "11_night_jars_t1.mp4", "start": 0.0,
            "vf": f"scale={W}:{H},fps={FPS}", "upscale": 1.5,
            "disp": "KEEP Flow t1 (Chief, desk #180 6137551906)",
        },
        "12_shutters_open": {
            "src": p4 / "12_shutters_open_t1.mp4", "start": 0.0,
            "vf": f"scale={W}:{H},fps={FPS}", "upscale": 1.5,
            "disp": "KEEP Flow t1 (Chief, desk #180 6137551906)",
        },
        "13_sun_canopy": {
            "src": p4 / "13_sun_canopy_t1.mp4", "start": 0.0,
            "vf": f"scale={W}:{H},fps={FPS}", "upscale": 1.5,
            "disp": "Flow t1 (J0140 batch 2; PENDING_UAT on review/j0140)",
        },
        "14_leaf_glow": {
            "src": p4 / "14_leaf_glow_t1.mp4", "start": 0.0,
            "vf": f"scale={W}:{H},fps={FPS}", "upscale": 1.5,
            "disp": "Flow t1 (J0140 batch 2; PENDING_UAT on review/j0140)",
        },
        "15_leaf_turns_sun": {
            "src": p4 / "15_leaf_turns_sun_t1.mp4", "start": 0.0,
            "vf": f"scale={W}:{H},fps={FPS}", "upscale": 1.5,
            "disp": "Flow t1 (J0140 batch 2; PENDING_UAT on review/j0140)",
        },
        "16_pores_question": {
            "src": p4 / "16_pores_question_t1.mp4", "start": 0.0,
            "vf": f"scale={W}:{H},fps={FPS}", "upscale": 1.5,
            "disp": "Flow t1 (J0140 batch 2; PENDING_UAT on review/j0140)",
        },
    }


def part05_specs() -> dict[str, dict]:
    p1 = MEDIA / "04_Generated-Clips/part01/raw/v01"
    p2 = MEDIA / "04_Generated-Clips/part02/raw/v01"
    p5 = MEDIA / "04_Generated-Clips/part05/raw/v01"
    atom = HOS_MAIN / "02_Video-Projects/004_Whats-Really-Inside-An-Atom/04_Generated-Clips/part01/raw/v01/11_gold_foil_bounce_v01.mp4"
    return {
        "01_geneva_lake": {
            "src": p5 / "01_geneva_lake_t1.mp4", "start": 0.0,
            "vf": f"scale={W}:{H},fps={FPS}", "upscale": 1.5,
            "disp": "KEEP Flow t1 (Chief, desk #180 6140142639)",
        },
        "02_senebier_jars": {
            "src": p5 / "02_senebier_jars_cover_v01.mp4", "start": 0.0,
            "vf": f"scale={W}:{H},fps={FPS}", "upscale": 1.5,
            "disp": "COVER fallback: P4:04_sunny_window_t1 (1.50-5.25s) + P4:05_bubbles_macro_t1 (3.75-7.46s) per Chief #180 6140112141 / 14 Oct",
        },
        "03_de_saussure": {
            "src": p5 / "11_trunk_pie_t1.mp4", "start": 0.0,
            "vf": f"scale={W}:{H},fps={FPS}", "upscale": 1.5,
            "disp": "KEEP reassigned from P5:11_trunk_pie_t1 (Chief, desk #180 6140142639)",
        },
        "04_fine_scales": {
            "src": p5 / "04_fine_scales_t1.mp4", "start": 0.0,
            "vf": f"scale={W}:{H},fps={FPS}", "upscale": 1.5,
            "disp": "KEEP Flow t1 (Chief, desk #180 6140142639)",
        },
        "05_sums_add_up": {
            "src": p5 / "05_sums_add_up_t1.mp4", "start": 5.0,
            "vf": f"scale={W}:{H},fps={FPS}", "upscale": 1.5,
            "disp": "KEEP Flow t1 trimmed to last ~3 s ledger/quill tail (5.00-7.93 s, Chief #180 6140142639)",
        },
        "06_leaf_in": {
            "src": p5 / "06_leaf_in_t1.mp4", "start": 0.0,
            "vf": f"scale={W}:{H},fps={FPS}", "upscale": 1.5,
            "disp": "KEEP Flow t1 (Chief, desk #180 6140142639)",
        },
        "07_sugar_oxygen": {
            "src": p5 / "07_sugar_oxygen_t1.mp4", "start": 0.0,
            "vf": f"scale={W}:{H},fps={FPS}", "upscale": 1.5,
            "disp": "KEEP Flow t1 (Chief, desk #180 6140142639)",
        },
        "08_sugar_wood": {
            "src": p5 / "08_sugar_wood_t1.mp4", "start": 0.0,
            "vf": f"scale={W}:{H},fps={FPS}", "upscale": 1.5,
            "disp": "KEEP Flow t1 (Chief, desk #180 6140142639)",
        },
        "09_helmont_willow": {
            "src": p2 / "06_garden_years_t2.mp4", "start": 4.0,
            "vf": f"scale={W}:{H},fps={FPS}", "upscale": 1.0,
            "disp": "REUSE window 4.00-7.42 s of P2:06_garden_years_t2 (board reuse_of)",
        },
        "10_air_threads": {
            "src": p1 / "01_willow_air_t1.mp4", "start": 0.5,
            "vf": f"scale={W}:{H},fps={FPS}", "upscale": 1.0,
            "disp": "REUSE window 0.50-7.50 s of P1:01_willow_air_t1 (board reuse_of)",
        },
        "11_trunk_pie": {
            "src": p5 / "11_trunk_pie_cg_v01.mp4", "start": 0.0,
            "vf": f"scale={W}:{H},fps={FPS}", "upscale": 1.0,
            "disp": "Code graphic v01 (0 credits, Animistry cream/wood wedges per Chief #180 6140142639)",
        },
        "12_scales_barely": {
            "src": p2 / "12_pointer_short_t1.mp4", "start": 1.0,
            "vf": f"scale={W}:{H},fps={FPS}", "upscale": 1.0,
            "disp": "REUSE window 1.00-6.52 s of P2:12_pointer_short_t1 (board reuse_of)",
        },
        "13_water_in_tree": {
            "src": p2 / "05_pure_water_t1.mp4", "start": 0.0,
            "vf": f"scale={W}:{H},fps={FPS}", "upscale": 1.0,
            "disp": "REUSE window 0.00-5.08 s of P2:05_pure_water_t1 (board reuse_of)",
        },
        "14_built_from_sky": {
            "src": p5 / "14_built_from_sky_t1.mp4", "start": 0.0,
            "vf": f"scale={W}:{H},fps={FPS}", "upscale": 1.5,
            "disp": "KEEP Flow t1 (Chief, desk #180 6140142639)",
        },
        "15_food_glow": {
            "src": p5 / "15_food_glow_t1.mp4", "start": 0.0,
            "vf": f"scale={W}:{H},fps={FPS}", "upscale": 1.5,
            "disp": "KEEP Flow t1 (Chief, desk #180 6140142639)",
        },
        "16_cow_grass": {
            "src": p5 / "16_cow_grass_t1.mp4", "start": 0.0,
            "vf": f"scale={W}:{H},fps={FPS}", "upscale": 1.5,
            "disp": "KEEP Flow t1 (Chief, desk #180 6140142639)",
        },
        "17_wind_air": {
            "src": p5 / "17_wind_air_t1.mp4", "start": 0.0,
            "vf": f"scale={W}:{H},fps={FPS}", "upscale": 1.5,
            "disp": "KEEP Flow t1 (Chief, desk #180 6140142639)",
        },
        "18_forest_sea": {
            "src": p5 / "18_forest_sea_t1.mp4", "start": 0.0,
            "vf": f"scale={W}:{H},fps={FPS}", "upscale": 1.5,
            "disp": "KEEP Flow t1 full version (Chief, desk #180 6140142639)",
        },
        "19_dots_crowd": {
            "src": p5 / "19_dots_crowd_cg_v01.mp4", "start": 0.0,
            "vf": f"scale={W}:{H},fps={FPS}", "upscale": 1.0,
            "disp": "Code graphic v01 (0 credits, 10,000 dots with 4 gold per Chief #180 6140142639)",
        },
        "20_explorer_willow": {
            "src": p5 / "20_explorer_willow_t1.mp4", "start": 0.0,
            "vf": f"scale={W}:{H},fps={FPS}", "upscale": 1.5,
            "disp": "KEEP Flow t1 (Explorer UAT passed by Chief, desk #180 6140142639)",
        },
        "21_three_objects": {
            "src": p1 / "03_pot_jar_leaf_t1.mp4", "start": 2.3,
            "vf": f"scale={W}:{H},fps={FPS}", "upscale": 1.0,
            "disp": "REUSE window 2.30-7.42 s of P1:03_pot_jar_leaf_t1 (board reuse_of)",
        },
        "22_pulled_down": {
            "src": p5 / "22_pulled_down_t1.mp4", "start": 0.0,
            "vf": f"scale={W}:{H},fps={FPS}", "upscale": 1.5,
            "disp": "KEEP Flow t1 (Chief, desk #180 6140142639)",
        },
        "23_carbon_atom": {
            "src": p5 / "23_carbon_atom_t1.mp4", "start": 0.0,
            "vf": f"scale={W}:{H},fps={FPS}", "upscale": 1.5,
            "disp": "KEEP Flow t1 (Chief, desk #180 6140142639)",
        },
        "24_gold_foil": {
            "src": atom, "start": 0.0,
            "vf": f"scale={W}:{H},fps={FPS}", "upscale": 1.0,
            "disp": "REUSE window 0.00-6.44 s of HOS 004 KEEP 11_gold_foil_bounce_v01.mp4 (board reuse_of)",
        },
    }


def assemble_part(part_num: int, ver: str, specs: dict[str, dict], reviewed_ok: list[str] | None = None) -> dict:
    pstr = f"{part_num:02d}"
    board_path = HERE / "parts" / f"part-{pstr}_plates_v01.json"
    board = json.loads(board_path.read_text())
    vo = MEDIA / board["vo_file"]
    assert sha(vo) == board["vo_sha256"], f"Part {pstr} VO sha mismatch"

    slug = f"part{pstr}_rough_{ver}"
    name = f"hos_006_{slug}"
    out_dir = MEDIA / "07_Edit-Project" / "_precheck" / slug
    desk_dir = HERE / "_desk" / "006" / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    seg_dir = out_dir / "segs"
    seg_dir.mkdir(exist_ok=True)

    t0, end = board["vo_film_start_s"], board["part_end_film_s"]
    plates = board["plates"]
    cuts, segs = [], []

    for k, p in enumerate(plates):
        nxt = plates[k + 1]["t_s"] if k + 1 < len(plates) else end
        f_in, f_out = round((p["t_s"] - t0) * FPS), round((nxt - t0) * FPS)
        n = f_out - f_in
        seg = seg_dir / f"seg_{k:02d}_{p['id']}.mp4"
        sp = specs[p["id"]]
        src = sp["src"]
        start = float(sp["start"])
        assert start + n / FPS <= probe_dur(src) + 1e-3, f"Part {pstr} {p['id']}: window runs past clip"
        run(["ffmpeg", "-y", "-ss", f"{start:.3f}", "-i", str(src), "-an", "-vf", sp["vf"], "-frames:v", str(n), *X264, str(seg)])
        row = {
            "row": p["id"],
            "film_t": p["t_s"],
            "timeline_in": f_in / FPS,
            "timeline_out": f_out / FPS,
            "frames": n,
            "upscale": sp["upscale"],
            "side_label": p.get("side_label"),
            "source": src.name,
            "source_path": str(src),
            "source_sha256": sha(src),
            "framing": {"offset": start},
            "disposition": sp["disp"],
        }
        segs.append(seg)
        cuts.append(row)

    concat = out_dir / "concat.txt"
    concat.write_text("".join(f"file '{s}'\n" for s in segs))
    pic = out_dir / "picture_only.mp4"
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat), "-c", "copy", str(pic)])
    total = round((end - t0) * FPS) / FPS
    cut = out_dir / f"{name}.mp4"
    run([
        "ffmpeg", "-y", "-i", str(pic), "-i", str(vo), "-map", "0:v", "-map", "1:a",
        "-c:v", "copy", "-af", "apad", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-t", f"{total:.3f}", "-movflags", "+faststart", str(cut),
    ])

    fd = subprocess.run(
        ["ffmpeg", "-i", str(cut), "-vf", "freezedetect=n=-60dB:d=0.8", "-map", "0:v", "-f", "null", "-"],
        stderr=subprocess.PIPE, text=True,
    ).stderr
    freeze = [l.split("] ", 1)[1] for l in fd.splitlines() if "freezedetect" in l and "lavfi.freezedetect" in l]
    freeze_path = out_dir / "freezedetect.log"
    freeze_path.write_text("\n".join(freeze) + ("\n" if freeze else ""))

    cuts_path = out_dir / f"cuts_{slug}.json"
    cuts_path.write_text(json.dumps(cuts, indent=1) + "\n")
    pool = [{"file": c["source"], "title": "Veo 3.1 clip, Chief KEEP"} for c in cuts]
    pool_path = out_dir / f"pool_{slug}.json"
    pool_path.write_text(json.dumps(pool, indent=1) + "\n")

    sheet = out_dir / f"{name}_contact_sheet.jpg"
    contact_sheet(cut, cuts, out_dir, sheet)
    proxy = out_dir / f"{name}_uat_proxy.mp4"
    run([
        "ffmpeg", "-y", "-i", str(cut), "-vf", "scale=960:540", "-c:v", "libx264",
        "-preset", "medium", "-crf", "26", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(proxy),
    ])

    meta = {
        "film": board["film"],
        "part": part_num,
        "kind": f"rough_{ver}",
        "job": "J0140",
        "authority": "Chief J0139/J0140 rulings (#180 6133713891, 6137551906, 6140112141, 6140142639, 14 Oct 20:50Z)",
        "applied_by": "gemini",
        "no_new_mints": True,
        "spend": "none (assembly only)",
        "assemble_method": "VO-first: board t_s/use_s per plate, hard cuts, 24 fps 1080p, VO padded to part end",
        "board": f"02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project/parts/part-{pstr}_plates_v01.json",
        "vo_file": board["vo_file"],
        "vo_sha256": board["vo_sha256"],
        "vo_duration_s": round(probe_dur(vo), 3),
        "rough_duration_s": round(probe_dur(cut), 3),
        "picture_s": total,
        "rough_path": str(cut),
        "sha256": sha(cut),
        "size_mb": round(cut.stat().st_size / 1e6, 2),
        "proxy_path": str(proxy),
        "proxy_sha256": sha(proxy),
        "contact_sheet": str(sheet),
        "not_in_rough": [
            "side labels / WHO cards / chapter card (edit overlays, added at fine cut)",
            "music bed and house SFX",
            "xfades (board 0.35 s)",
        ],
        "freeze_events": freeze,
        "segments": cuts,
    }
    meta_name = f"ROUGH_META_part{pstr}_{ver}.json"
    (out_dir / meta_name).write_text(json.dumps(meta, indent=1) + "\n")

    desk_dir.mkdir(parents=True, exist_ok=True)
    for fname in (meta_name, cuts_path.name, pool_path.name, "freezedetect.log", sheet.name):
        dst = desk_dir / (fname if fname != "freezedetect.log" else f"{slug}_freezedetect.log")
        shutil.copy2(out_dir / fname, dst)

    # Run picture_qa.py into desk_dir
    pqa_cmd = [
        sys.executable,
        str(OWB_MAIN / "scripts/picture_qa.py"),
        str(cut),
        "--cuts", str(cuts_path),
        "--pool", str(pool_path),
        "--out-dir", str(desk_dir),
    ]
    pqa_res = subprocess.run(pqa_cmd, capture_output=True, text=True)
    meta["picture_qa_rc"] = pqa_res.returncode
    meta["picture_qa_stdout"] = pqa_res.stdout.strip()
    (out_dir / meta_name).write_text(json.dumps(meta, indent=1) + "\n")
    shutil.copy2(out_dir / meta_name, desk_dir / meta_name)

    if UAT_ROOT.exists():
        uat_dest = UAT_ROOT / f"006_{slug}"
        uat_dest.mkdir(parents=True, exist_ok=True)
        for f in (cut, proxy, sheet):
            shutil.copy2(f, uat_dest / f.name)

    return {
        "slug": slug,
        "rough_duration_s": meta["rough_duration_s"],
        "vo_duration_s": meta["vo_duration_s"],
        "sha256": meta["sha256"][:12],
        "freeze_events": len(freeze),
        "picture_qa_rc": pqa_res.returncode,
    }


def main() -> None:
    print("Assembling Part 03 rough v02 (with P3:06 dropped in) ...", flush=True)
    r3 = assemble_part(3, "v02", part03_specs())
    print("  ->", json.dumps(r3), flush=True)

    print("Assembling Part 04 rough v01 ...", flush=True)
    r4 = assemble_part(4, "v01", part04_specs())
    print("  ->", json.dumps(r4), flush=True)

    print("Assembling Part 05 rough v01 ...", flush=True)
    r5 = assemble_part(5, "v01", part05_specs())
    print("  ->", json.dumps(r5), flush=True)


if __name__ == "__main__":
    main()
