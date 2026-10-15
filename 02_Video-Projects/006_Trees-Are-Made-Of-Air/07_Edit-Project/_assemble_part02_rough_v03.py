#!/usr/bin/env python3
"""HOS 006 Part 02 rough v03 (J0290). Assembly only: no mint, no spend.

v02 failed picture_qa (five reuses) and polish_gate (desk-candle seam, freeze-pad).
Same plate lengths as v02 so the locked VO stays put. Reuse tails are their own
files, the way J0266 did Parts 03 and 04. Freeze-pads become moving KEEP tails
or a code graphic. The candle crop tracks above the desk lip.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

FPS = 24
W, H = 1920, 1080
FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
X264 = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-r", str(FPS), "-an"]

# Clips live in the part02 worktree (gitignored). Reports land in the HOS checkout.
MEDIA = Path("/Users/benjaminoats/YouTube/hos-006-trees/02_Video-Projects/006_Trees-Are-Made-Of-Air")
HERE = Path("/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project")
RAW = MEDIA / "04_Generated-Clips/part02/raw/v01"
TRIM = MEDIA / "04_Generated-Clips/part02/raw/v01_trim"
STRETCH = RAW / "stretches_v03"
VO = MEDIA / "02_Voiceover/part02_five_years_and_two_ounces_v02.mp3"

# v02 frame counts (24 fps). Row 22 grows to the end of the VO so nothing freezes.
V02_FRAMES = {
    "01_furnace_soil": 131,
    "02_balance_200": 140,
    "03_willow_shoot_scale": 103,
    "04_lid_rain": 153,
    "05_pure_water": 120,
    "06_garden_years": 190,
    "08_haul_tree": 115,
    "09_weights_169": 94,
    "10_fallen_leaves": 106,
    "11_furnace_again": 85,
    "12_pointer_short": 163,
    "13_tree_vs_pinch": 129,
    "14_why_grown": 106,
    "15_desk_candle": 131,
    "16_water_drawing": 123,
    "17_mostly_wrong": 128,
    "18_charcoal_hearth": 163,
    "19_ash_mound": 85,
    "20_shimmer_coals": 124,
    "21_gas_window": 159,
    "22_shimmer_willow": 143,
}
ORDER = list(V02_FRAMES)
LABELS = {
    "01_furnace_soil": "DRIED SOIL",
    "02_balance_200": "200 POUNDS OF SOIL",
    "03_willow_shoot_scale": "A 5-POUND WILLOW",
    "04_lid_rain": "WATER IN, DUST OUT",
    "06_garden_years": "FIVE YEARS",
    "09_weights_169": "169 POUNDS",
    "12_pointer_short": "SOIL LOST: ABOUT 2 OUNCES",
    "16_water_drawing": '"FROM WATER ALONE"',
    "19_ash_mound": "62 POUNDS → 1 POUND OF ASH",
    "21_gas_window": "GAS",
}


def run(cmd: list[str]) -> None:
    r = subprocess.run(cmd, stderr=subprocess.PIPE, text=True)
    if r.returncode != 0:
        raise SystemExit(f"ffmpeg failed ({r.returncode}): {' '.join(cmd[:8])}\n{r.stderr[-1500:]}")


def probe_dur(path: Path) -> float:
    out = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        text=True,
    )
    return float(out.strip())


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def encode_span(src: Path, start: float, frames: int, dest: Path, vf: str) -> None:
    """-ss after -i so a tail starts on the exact frame, not the previous keyframe."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    run(["ffmpeg", "-y", "-i", str(src), "-ss", f"{start:.3f}", "-frames:v", str(frames), "-vf", vf, *X264, str(dest)])


def concat(parts: list[Path], dest: Path) -> None:
    lst = dest.with_suffix(".txt")
    lst.write_text("".join(f"file '{p}'\n" for p in parts))
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(dest)])


def graphic(dest: Path, frames: int, kind: str) -> None:
    """Own code graphic. The panel stays inside 90% of the frame so it is not a seam.
    This ffmpeg build has no drawtext, so the frames are drawn with PIL."""
    from PIL import Image, ImageDraw, ImageFont

    dest.parent.mkdir(parents=True, exist_ok=True)
    font_n = ImageFont.truetype(FONT, 150 if kind == "pounds" else 110)
    font_l = ImageFont.truetype(FONT, 64)
    tmp = dest.parent / f"_gfx_{dest.stem}"
    tmp.mkdir(exist_ok=True)
    for i in range(frames):
        u = i / max(1, frames - 1)
        im = Image.new("RGB", (W, H), (36, 52, 72))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle((280, 220, 1640, 860), radius=28, fill=(232, 214, 184))
        if kind == "pounds":
            d.text((W / 2, 430), str(int(round(200 * u))), font=font_n, fill=(28, 32, 38), anchor="mm")
            d.text((W / 2, 610), "200 pounds", font=font_l, fill=(28, 32, 38), anchor="mm")
            bw = int(40 + 900 * u)
            d.rounded_rectangle((510, 720, 510 + bw, 776), radius=8, fill=(176, 92, 42))
        else:
            d.text((W / 2, 460), "made of air", font=font_n, fill=(28, 32, 38), anchor="mm")
            d.text((W / 2, 640), "the same gas", font=font_l, fill=(28, 32, 38), anchor="mm")
            bw = int(40 + 900 * u)
            d.rounded_rectangle((510, 740, 510 + bw, 796), radius=8, fill=(42, 92, 78))
        im.save(tmp / f"f{i:04d}.png", compress_level=1)
    run(["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(tmp / "f%04d.png"), "-frames:v", str(frames), *X264, str(dest)])
    for p in tmp.glob("*.png"):
        p.unlink()
    tmp.rmdir()


class Pool:
    """Unused KEEP tails, in frames. Each donor starts the frame after that clip's own plate."""

    def __init__(self) -> None:
        # (id, file, clip frames, frames already used on its own plate)
        spec = [
            ("weights", "09_weights_169_t1.mp4", 6 * FPS, 94),
            ("wrong", "17_mostly_wrong_t1.mp4", 6 * FPS, 128),
            ("coals", "20_shimmer_coals_t1.mp4", 6 * FPS, 124),
            ("shoot", "03_willow_shoot_scale_t1.mp4", 6 * FPS, 103),
            ("lid", "04_lid_rain_t1.mp4", 8 * FPS, 153),
            ("water", "05_pure_water_t1.mp4", 6 * FPS, 120),
            ("leaves", "10_fallen_leaves_t1.mp4", 6 * FPS, 106),
            ("pointer", "12_pointer_short_t1.mp4", 8 * FPS, 163),
            ("tree", "13_tree_vs_pinch_t1.mp4", 6 * FPS, 129),
            ("candle", "15_desk_candle_t1.mp4", 6 * FPS, 131),
            ("drawing", "16_water_drawing_t1.mp4", 6 * FPS, 123),
            ("charcoal", "18_charcoal_hearth_t1.mp4", 8 * FPS, 163),
            # ash KEEP stops at 4.0s (96 frames), before the flame
            ("ash", "19_ash_mound_t1.mp4", 4 * FPS, 85),
        ]
        self.donors = []
        for did, name, total, used in spec:
            src = RAW / name
            left = total - used
            if left <= 0:
                raise SystemExit(f"donor {did} has no tail")
            if probe_dur(src) + 0.05 < total / FPS:
                raise SystemExit(f"donor {did} clip is shorter than {total / FPS:.2f}s")
            self.donors.append({"id": did, "src": src, "start": used / FPS, "left": left})

    def frames_left(self) -> int:
        return sum(d["left"] for d in self.donors)

    def take(self, frames: int, prefer: list[str]) -> list[tuple[Path, float, int]]:
        need = frames
        got: list[tuple[Path, float, int]] = []
        order = sorted(self.donors, key=lambda d: (prefer.index(d["id"]) if d["id"] in prefer else 99, -d["left"]))
        for d in order:
            if need <= 0:
                break
            if d["left"] <= 0:
                continue
            n = min(d["left"], need)
            got.append((d["src"], d["start"], n))
            d["start"] += n / FPS
            d["left"] -= n
            need -= n
        if need:
            raise SystemExit(f"KEEP tails short by {need} frames")
        return got


def build_from_pieces(pieces: list[tuple[Path, float, int]], dest: Path, vf: str = f"scale={W}:{H},fps={FPS}") -> None:
    segs = []
    for i, (src, start, n) in enumerate(pieces):
        seg = dest.parent / f"_{dest.stem}_{i:02d}.mp4"
        encode_span(src, start, n, seg, vf)
        segs.append(seg)
    if len(segs) == 1:
        segs[0].replace(dest)
    else:
        concat(segs, dest)
        for s in segs:
            s.unlink(missing_ok=True)


def main() -> None:
    STRETCH.mkdir(parents=True, exist_ok=True)
    vo_dur = probe_dur(VO)
    total_frames = int(round(vo_dur * FPS))
    head = sum(V02_FRAMES[k] for k in ORDER if k != "22_shimmer_willow")
    row22 = total_frames - head
    if row22 < V02_FRAMES["22_shimmer_willow"]:
        raise SystemExit(f"row 22 would shrink ({row22} frames)")

    pool = Pool()
    plain = f"scale={W}:{H},fps={FPS}"

    # Row 11: furnace tail after row 01's 131 frames. Own file. Mild setpts fills 85 frames.
    furn_start = 131 / FPS
    furn_have = int((8.0 - furn_start) * FPS)  # 61
    furn_tail = STRETCH / "01_furnace_soil_t1_from5.458.mp4"
    raw_tail = STRETCH / "_furnace_tail_raw.mp4"
    encode_span(RAW / "01_furnace_soil_t1.mp4", furn_start, furn_have, raw_tail, plain)
    run(["ffmpeg", "-y", "-i", str(raw_tail),
         "-vf", f"setpts={V02_FRAMES['11_furnace_again']}/{furn_have}*PTS,fps={FPS}",
         "-frames:v", str(V02_FRAMES["11_furnace_again"]), *X264, str(furn_tail)])

    # Row 02: the stand-in cannot share the weights clip. Own graphic, full plate.
    g02 = STRETCH / "code_graphic_p2_02_pounds_v03.mp4"
    graphic(g02, V02_FRAMES["02_balance_200"], "pounds")

    # Row 14 cover: garden KEEP tails, not the 17 opening.
    cover14 = STRETCH / "14_why_grown_cover_v03.mp4"
    bits14 = pool.take(V02_FRAMES["14_why_grown"], ["shoot", "leaves", "lid", "tree"])
    build_from_pieces(bits14, cover14)

    # Row 21: coals tail first (the approved cover idea), then other KEEP tails. No hold.
    cover21 = STRETCH / "21_gas_window_cover_v03.mp4"
    bits21 = pool.take(V02_FRAMES["21_gas_window"], ["coals", "charcoal", "ash", "drawing", "pointer"])
    build_from_pieces(bits21, cover21)

    # Row 15: constant-size crop whose top tracks down with the desk lip.
    candle = STRETCH / "15_desk_candle_t1_above_desk_v03.mp4"
    candle_vf = "crop=1244:700:338:'47+36*t',scale=1920:1080:flags=lanczos,fps=24"
    encode_span(RAW / "15_desk_candle_t1.mp4", 0.0, V02_FRAMES["15_desk_candle"], candle, candle_vf)

    # Row 22: KEEP last third, then a code graphic, then whatever KEEP tails remain.
    willow_n = int(round((8.0 - 5.333) * FPS))  # 64
    willow = STRETCH / "_22_willow_keep.mp4"
    encode_span(RAW / "22_shimmer_willow_t1.mp4", 5.333, willow_n, willow, plain)
    left_frames = pool.frames_left()
    gfx_n = row22 - willow_n - left_frames
    if gfx_n < 24:
        raise SystemExit(f"row 22 graphic would be {gfx_n} frames; tails left {left_frames}")
    g22 = STRETCH / "code_graphic_p2_22_air_v03.mp4"
    graphic(g22, gfx_n, "air")
    tail_bits = pool.take(left_frames, [])
    tails = STRETCH / "_22_tails.mp4"
    build_from_pieces(tail_bits, tails)
    row22_file = STRETCH / "22_shimmer_willow_moving_v03.mp4"
    concat([willow, g22, tails], row22_file)

    specs = {
        "01_furnace_soil": (RAW / "01_furnace_soil_t1.mp4", 0.0, plain, 1.0, "KEEP"),
        "02_balance_200": (g02, 0.0, plain, 1.0, "CODE GRAPHIC stand-in (weights clip stays on row 09 only). J0290"),
        "03_willow_shoot_scale": (RAW / "03_willow_shoot_scale_t1.mp4", 0.0, plain, 1.0, "KEEP"),
        "04_lid_rain": (RAW / "04_lid_rain_t1.mp4", 0.0, plain, 1.0, "KEEP"),
        "05_pure_water": (RAW / "05_pure_water_t1.mp4", 0.0, plain, 1.0, "KEEP"),
        "06_garden_years": (RAW / "06_garden_years_t2.mp4", 0.0, plain, 1.0, "KEEP t2"),
        "08_haul_tree": (TRIM / "08_haul_tree_t1_trim_0to4p8.mp4", 0.0, plain, 1.0, "KEEP trim 0-4.80"),
        "09_weights_169": (RAW / "09_weights_169_t1.mp4", 0.0, plain, 1.0, "KEEP"),
        "10_fallen_leaves": (RAW / "10_fallen_leaves_t1.mp4", 0.0, plain, 1.0, "KEEP"),
        "11_furnace_again": (furn_tail, 0.0, plain, 1.0,
                             "REUSE non-overlapping tail 5.458-8.000s of 01_furnace_soil, own file, setpts to plate length (J0290)"),
        "12_pointer_short": (RAW / "12_pointer_short_t1.mp4", 0.0, plain, 1.0, "KEEP"),
        "13_tree_vs_pinch": (RAW / "13_tree_vs_pinch_t1.mp4", 0.0, plain, 1.0, "KEEP"),
        "14_why_grown": (cover14, 0.0, plain, 1.0,
                         "COVER from unused KEEP tails (not 17's opening). Own file (J0290)"),
        "15_desk_candle": (candle, 0.0, plain, round(1920 / 1244, 3),
                           "KEEP, crop tracks above the desk lip (1244x700, up 1.54). J0290"),
        "16_water_drawing": (RAW / "16_water_drawing_t1.mp4", 0.0, plain, 1.0, "KEEP"),
        "17_mostly_wrong": (RAW / "17_mostly_wrong_t1.mp4", 0.0, plain, 1.0, "KEEP"),
        "18_charcoal_hearth": (RAW / "18_charcoal_hearth_t1.mp4", 0.0, plain, 1.0, "KEEP"),
        "19_ash_mound": (RAW / "19_ash_mound_t1.mp4", 0.0, plain, 1.0, "KEEP trim before flame"),
        "20_shimmer_coals": (RAW / "20_shimmer_coals_t1.mp4", 0.0, plain, 1.0, "KEEP"),
        "21_gas_window": (cover21, 0.0, plain, 1.0,
                          "COVER coals tail then other KEEP tails. Own file, no freeze (J0290)"),
        "22_shimmer_willow": (row22_file, 0.0, plain, 1.0,
                              "KEEP last third, then code graphic, then KEEP tails, out to the VO. No freeze (J0290)"),
    }

    out_dir = MEDIA / "07_Edit-Project/_precheck/part02_rough_v03"
    seg_dir = out_dir / "segs"
    seg_dir.mkdir(parents=True, exist_ok=True)
    cuts, segs = [], []
    t = 0
    for pid in ORDER:
        n = row22 if pid == "22_shimmer_willow" else V02_FRAMES[pid]
        src, start, vf, up, disp = specs[pid]
        seg = seg_dir / f"seg_{pid}.mp4"
        # Prebuilt plates are already the right length and graded.
        if src.parent == STRETCH:
            if src != seg:
                run(["ffmpeg", "-y", "-i", str(src), "-c", "copy", str(seg)])
        else:
            encode_span(src, start, n, seg, vf)
        cuts.append({
            "row": pid,
            "film_t": round(t, 3),
            "timeline_in": t,
            "timeline_out": t + n / FPS,
            "frames": n,
            "upscale": up,
            "side_label": LABELS.get(pid),
            "source": src.name,
            "source_path": str(src),
            "framing": {"offset": 0.0},
            "disposition": disp,
        })
        segs.append(seg)
        t += n / FPS

    pic = out_dir / "picture_only.mp4"
    concat(segs, pic)
    cut = out_dir / "hos_006_part02_rough_v03.mp4"
    run(["ffmpeg", "-y", "-i", str(pic), "-i", str(VO), "-map", "0:v", "-map", "1:a",
         "-c:v", "copy", "-af", "apad", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
         "-t", f"{vo_dur:.3f}", "-movflags", "+faststart", str(cut)])

    fd = subprocess.run(
        ["ffmpeg", "-i", str(cut), "-vf", "freezedetect=n=-60dB:d=0.8", "-map", "0:v", "-f", "null", "-"],
        stderr=subprocess.PIPE, text=True,
    ).stderr
    freeze = [ln.split("] ", 1)[1] for ln in fd.splitlines() if "lavfi.freezedetect" in ln]

    desk = HERE / "_desk/006/part02_rough_v03"
    desk.mkdir(parents=True, exist_ok=True)
    cuts_path = desk / "cuts_part02_rough_v03.json"
    cuts_path.write_text(json.dumps(cuts, indent=1) + "\n")
    pool_path = desk / "pool_part02_rough_v03.json"
    pool_items = []
    for c in cuts:
        title = "our own clip or graphic" if "code_graphic" in c["source"] or c["source"].endswith("_v03.mp4") else "Veo 3.1 clip, Chief KEEP"
        pool_items.append({"file": c["source"], "title": title})
    pool_path.write_text(json.dumps(pool_items, indent=1) + "\n")
    (desk / "part02_rough_v03_freezedetect.json").write_text(json.dumps({
        "freeze_lines": freeze,
        "freeze_event_count": len([ln for ln in freeze if "freeze_start" in ln]),
    }, indent=1) + "\n")
    meta = {
        "film": "006_Trees-Are-Made-Of-Air",
        "part": 2,
        "kind": "rough_v03",
        "job": "J0290",
        "no_new_mints": True,
        "spend": "none",
        "vo_file": str(VO),
        "vo_duration_s": round(vo_dur, 3),
        "rough_path": str(cut),
        "rough_sha256": sha(cut),
        "picture_frames": total_frames,
        "row22_frames": row22,
        "gfx_frames": gfx_n,
        "willow_keep_frames": willow_n,
        "tail_frames": left_frames,
        "freeze_lines": freeze,
    }
    (desk / "ROUGH_META_part02_v03.json").write_text(json.dumps(meta, indent=1) + "\n")
    print(json.dumps(meta, indent=1))


if __name__ == "__main__":
    main()
