#!/usr/bin/env python3
"""J2652 (step 3/3): Render the v03f-r2 diagnostic rough with all 35 built £0 v03f free graphics.

- Preserves earlier v03f files (hos_013_timing_rough_J2652_v03f.mp4, ROUGH_MANIFEST_v03f.json, phone_contact_v03f_*.jpg) untouched.
- Uses all 35 hash-verified 1920x1080@50fps clips from code_graphics_v03f/CODE_GRAPHICS_v03f.json (0 free-graphic slates).
- Applies Chief ruling #6822305911 / #6822411223 on P2:11_island_split_vision (7.917s -> 8.00s setpts x1.0105, no freeze)
  and P3:02b_notebook_d_open (3.82-7.90s open-notebook window inside 7.917s take, no freeze).
- Keeps Pass-1 raw takes conspicuously watermarked 'TIMING ONLY - RAW TAKE - NOT KEEP' (never claiming KEEP; notes pending retakes).
- Keeps the 11 unminted Part 5/6 Quality beats as explicit slates (0 credits / £0 spent).
- Writes hos_013_timing_rough_J2652_v03f_r2.mp4 + 6 390px phone sheets + full ffmpeg decode check.
"""
from __future__ import annotations

import collections
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import textwrap
from PIL import Image, ImageDraw, ImageFont

EDIT = Path(__file__).resolve().parent
FILM = EDIT.parent
OUT = EDIT / "timing_rough_J2652"
SCRATCH = Path(os.environ.get("STUDIO_SCRATCH", "/private/tmp")) / "J2652-render-v03f-r2"
NAS = Path("/Volumes/data/studio-live/History Of Science/02_Video-Projects") / FILM.name
FONT = "/System/Library/Fonts/Supplemental/Arial.ttf"

PENDING_RETAKE_ROWS = {
    "P1:03a_unlabelled_birds",
    "P1:07_darwin_1837_desk",
    "P3:02a_malthus_lamplight",
}


@lru_cache(maxsize=None)
def sha(p: str | Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""):
            h.update(b)
    return h.hexdigest()


def run(args: list[str]) -> None:
    subprocess.run(args, check=True)


def dump(name: str, data: object) -> None:
    (OUT / name).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def main() -> None:
    assert not (OUT / "ROUGH_MANIFEST_v03f_r2.json").exists(), "v03f_r2 already exists; refusing overwrite"
    if SCRATCH.exists():
        shutil.rmtree(SCRATCH)
    SCRATCH.mkdir(parents=True, exist_ok=True)

    plan = json.loads((EDIT / "PICTURE_PLAN_v03f.json").read_text())
    vo = NAS / "02_Voiceover/hos_013_vo_v03a.wav"
    assert sha(vo) == plan["vo_sha256"], "VO WAV hash mismatch"

    cg_manifest = json.loads((EDIT / "code_graphics_v03f/CODE_GRAPHICS_v03f.json").read_text())
    cg_by_row = {rec["id"]: rec for rec in cg_manifest["rendered_clips"]}
    assert len(cg_by_row) == 35, f"Expected 35 v03f free clips, got {len(cg_by_row)}"

    raw_assets: dict[str, dict] = {}
    for r in plan["rows"]:
        if r["source_kind"] not in ("new_mint_quality", "existing_plate_reuse"):
            continue
        key = "P1:01_study_beaks" if r["source_kind"] == "existing_plate_reuse" else r["source_row_v02"]
        part, rid = key.split(":")
        raw = NAS / "04_Generated-Clips/archive_v01_pass1" / f"P{int(part[1:]):02d}_{rid}_t1.mp4"
        receipt = Path(str(raw) + ".sha256.json")
        if raw.exists() and receipt.exists():
            expected = json.loads(receipt.read_text())["sha256"]
            assert sha(raw) == expected, f"Archive receipt mismatch: {raw.name}"
            dur_av = float(subprocess.check_output([
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
            assert cg_path.exists() and sha(cg_path) == cg_rec["sha256_mp4"], f"CG hash mismatch: {cg_path}"
            run([
                "ffmpeg", "-v", "error", "-y", "-i", str(cg_path),
                "-vf", "scale=960:540:flags=lanczos,setsar=1,fps=50",
                "-frames:v", str(round(duration * 50)),
                "-an", "-c:v", "libx264", "-preset", "ultrafast", "-crf", "23", "-pix_fmt", "yuv420p",
                "-threads", "2", str(target),
            ])
            record = {
                "row": row_key,
                "start_s": r["t_s"],
                "end_s": r["t_end_s"],
                "status": "v03f_free_render",
                "source": str(cg_path),
                "source_offset_s": 0.0,
                "source_sha256": cg_rec["sha256_mp4"],
                "crop": None,
                "reason": "Built £0 v03f 1920x1080@50fps render (exact beat duration and word-anchored cues)",
            }
        elif r["source_row_v02"] in raw_assets:
            ra = raw_assets[r["source_row_v02"]]
            source = ra["source"]
            avail = ra["available_s"]
            offset = float(r["source_window_s"][0])
            retime_factor = None

            if r["source_row_v02"] == "P2:11_island_split_vision":
                # Chief ruling #6822305911 & #6822411223: retime 7.917s -> 8.00s (x1.0105), no freeze
                retime_factor = round(8.00 / avail, 6)
            elif r["source_row_v02"] == "P3:02b_notebook_d_open":
                # Chief ruling #6822305911 & #6822411223: end at 7.90s open-notebook window inside 7.917s take
                offset = round(7.90 - duration, 2)

            is_detail = ("_beat2" in r["id"] or r["id"].endswith("_detail"))
            crop = "crop=trunc(iw*0.88/2)*2:trunc(ih*0.88/2)*2," if is_detail else ""
            if retime_factor is not None:
                vf = f"setpts={retime_factor:.6f}*PTS,trim=start={offset:.3f}:duration={duration:.3f},setpts=PTS-STARTPTS,{crop}scale=960:540:flags=lanczos,setsar=1,fps=50"
                args = ["-i", source, "-i", str(watermark)]
            else:
                assert offset + duration <= avail + 0.002, f"Source too short on {row_key}: {offset}+{duration} > {avail}"
                vf = f"{crop}scale=960:540:flags=lanczos,setsar=1,fps=50"
                args = ["-ss", str(offset), "-i", source, "-i", str(watermark)]

            run([
                "ffmpeg", "-v", "error", "-y", *args,
                "-filter_complex", f"[0:v]{vf}[base];[base][1:v]overlay=0:0",
                "-frames:v", str(round(duration * 50)),
                "-an", "-c:v", "libx264", "-preset", "ultrafast", "-crf", "26", "-pix_fmt", "yuv420p",
                "-threads", "2", str(target),
            ])
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
            run([
                "ffmpeg", "-v", "error", "-y", "-loop", "1", "-framerate", "50", "-i", str(slate),
                "-vf", "setsar=1,fps=50", "-frames:v", str(round(duration * 50)),
                "-an", "-c:v", "libx264", "-preset", "ultrafast", "-crf", "27", "-pix_fmt", "yuv420p",
                "-threads", "2", str(target),
            ])
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

        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{duration / 2:.3f}", "-i", str(target), "-frames:v", "1", str(frame)])
        return i, frame, record

    print(f"Rendering {len(plan['rows'])} v03f-r2 beats across 4 threads...", flush=True)
    results = []
    with ThreadPoolExecutor(max_workers=4) as ex:
        for res in ex.map(render_beat, list(enumerate(plan["rows"]))):
            results.append(res)
            if (res[0] + 1) % 20 == 0 or res[0] + 1 == len(plan["rows"]):
                print(f"  [{res[0]+1:03d}/{len(plan['rows'])}] {res[2]['row']} -> {res[2]['status']}", flush=True)

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
    events = []
    for c in plan["overlay_cues"]:
        if c["status"] != "ANCHORED":
            continue
        label = c["overlay"].get("line_1", c["overlay"].get("label", ""))
        events.append(f"Dialogue: 0,{stamp(c['display_start_s'])},{stamp(c['display_end_s'])},Default,,0,0,0,,PLANNED CUE: {label}")
    ass.write_text(header + "\n".join(events) + "\n")

    master = SCRATCH / "hos_013_timing_rough_J2652_v03f_r2.mp4"
    run([
        "ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(concat),
        "-i", str(vo), "-i", str(ass),
        "-map", "0:v", "-map", "1:a", "-map", "2:s",
        "-c:v", "copy", "-c:s", "mov_text",
        "-threads", "2", "-c:a", "aac", "-b:a", "192k", "-af", "apad", "-t", "515",
        "-movflags", "+faststart", str(master),
    ])

    # Full video + audio decode verification
    run(["ffmpeg", "-v", "error", "-i", str(master), "-f", "null", "-"])

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
        dest_git = OUT / f"phone_contact_v03f_r2_{page + 1:02d}.jpg"
        im.save(dest_git, quality=90)
        sheet_paths.append(dest_git)

    destdir = NAS / "07_Edit-Project/timing_rough_J2652"
    destdir.mkdir(parents=True, exist_ok=True)
    copies = []
    for src in [master, *sheet_paths]:
        dest = destdir / src.name
        assert not dest.exists(), f"Refusing overwrite on NAS: {dest}"
        shutil.copy2(src, dest)
        assert sha(src) == sha(dest)
        copies.append({"path": str(dest), "sha256": sha(dest)})

    counts = collections.Counter(r["status"] for r in inventory)
    dump("asset_inventory_v03f_r2.json", inventory)
    dump("ROUGH_MANIFEST_v03f_r2.json", {
        "files": copies,
        "vo_sha256": sha(vo),
        "plan_sha256": sha(EDIT / "PICTURE_PLAN_v03f.json"),
        "code_graphics_v03f_sha256": sha(EDIT / "code_graphics_v03f/CODE_GRAPHICS_v03f.json"),
        "duration_s": 515,
        "fps": 50,
        "credits_spent": 0,
        "gbp_spent": 0,
        "approved": False,
        "status_counts": dict(counts),
        "slates": counts["diagnostic_slate"],
        "limitations": (
            "All 35 £0 code-graphic/archive beats use finished v03f 1920x1080@50fps renders. "
            "58 beats use receipt-verified Pass-1 takes marked NOT KEEP (including Chief #6822411223 "
            "P2:11 x1.0105 retime and P3:02b 3.82-7.90s window; rows P1:03a, P1:07, P3:02a still await Pass-1 retakes). "
            "11 beats (P5:08a through P6:08b) remain explicit slates awaiting J2529 Pass-1 Part 5/6 generation. "
            "No music/SFX; no audio or moving-video perception claimed."
        ),
    })
    shutil.rmtree(SCRATCH, ignore_errors=True)
    print(f"V03F_R2 COMPLETE: {dict(counts)} — NAS COPY & FULL DECODE VERIFIED", flush=True)


if __name__ == "__main__":
    main()
