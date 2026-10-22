#!/usr/bin/env python3
"""HOS 006: Assemble hos_006_full_join_v02_base.mp4 + cuts_full_join_v02.json + pool_full_join_v02.json.

Applies the Part 02 drift fix (#18 extended from 190 frames / 7.916667 s to 321 frames / 13.375000 s by appending
06_garden_years_t1.mp4 0.00-5.458333 s; #33 shortened from 260 frames / 10.833333 s back to 129 frames / 5.375000 s;
#19..#32 shifted by +131 frames / +5.458333 s to match VO_RETIME_v02.json), plus the 4 low-detail
replacements (#14, #24, #33, #62), #20 bottom-crop, and Part 05 labelled code graphics (#78, #86).
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
from pathlib import Path

FILM = "006_Trees-Are-Made-Of-Air"
REPO = Path("/Users/benjaminoats/YouTube/History Of Science")
PROJ = REPO / "02_Video-Projects" / FILM
MEDIA = Path(
    os.environ.get(
        "HOS_006_MEDIA",
        str(Path.home() / "YouTube/hos-006-trees/02_Video-Projects" / FILM),
    )
)
V01_DIR = PROJ / "07_Edit-Project/_desk/006/full_join_v01"
V01_TEACH_DIR = PROJ / "07_Edit-Project/full_join_v01_teach"
V02_DIR = Path(__file__).resolve().parent
FPS = 24


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> None:
    V02_DIR.mkdir(parents=True, exist_ok=True)
    cuts_v01 = json.loads((V01_DIR / "cuts_full_join_v01.json").read_text())
    pool_v01 = json.loads((V01_DIR / "pool_full_join_v01.json").read_text())

    p2_raw = MEDIA / "04_Generated-Clips/part02/raw/v01"
    p4_raw = MEDIA / "04_Generated-Clips/part04/raw/v01"
    p5_raw = MEDIA / "04_Generated-Clips/part05/raw/v01"

    cuts_v02 = []
    cur_frames = 0

    for idx, c in enumerate(cuts_v01):
        row = dict(c)
        cut_num = idx + 1

        if cut_num == 14:
            # #14 P2 02_balance_200: 02_balance_200_t1 top-cropped + house DATA counter
            sp = p2_raw / "02_balance_200_house_v02.mp4"
            row["source"] = sp.name
            row["source_path"] = str(sp)
            row["source_sha256"] = sha256_file(sp)
            row["frames"] = 140
            row["upscale"] = 1.32
            row["framing"] = {"offset": 0.0}
            row["disposition"] = "KEEP 02_balance_200_t1 top-cropped 1920x816 + HOS house DATA counter (J0809)"
        elif cut_num == 18:
            # #18 P2 06_garden_years: t2 (190f) + t1 (131f) = 321 frames (13.375 s)
            sp = p2_raw / "06_garden_years_joined_v02.mp4"
            row["source"] = sp.name
            row["source_path"] = str(sp)
            row["source_sha256"] = sha256_file(sp)
            row["frames"] = 321
            row["upscale"] = 1.0
            row["framing"] = {"offset": 0.0}
            row["disposition"] = "KEEP 06_garden_years_t2 (0-7.92s) + 06_garden_years_t1 (0-5.46s) = 13.375s (J0809)"
        elif cut_num == 20:
            # #20 P2 09_weights_169: top-cropped 1920x788 (1.37x upscale)
            sp = p2_raw / "09_weights_169_crop_v02.mp4"
            row["source"] = sp.name
            row["source_path"] = str(sp)
            row["source_sha256"] = sha256_file(sp)
            row["frames"] = 94
            row["upscale"] = 1.37
            row["framing"] = {"offset": 0.0}
            row["disposition"] = "KEEP 09_weights_169_t1 top-cropped 1920x788 to hide Veo numerals (J0809)"
        elif cut_num == 24:
            # #24 P2 13_tree_vs_pinch: cropped 1628:916:146:120 (1.18x upscale) + bare-table trim
            sp = p2_raw / "13_tree_vs_pinch_trim_v02.mp4"
            row["source"] = sp.name
            row["source_path"] = str(sp)
            row["source_sha256"] = sha256_file(sp)
            row["frames"] = 129
            row["upscale"] = 1.18
            row["framing"] = {"offset": 0.0}
            row["disposition"] = "KEEP 13_tree_vs_pinch_t1 cropped 1628x916 + bare-table trim (J0809)"
        elif cut_num == 33:
            # #33 P2 22_shimmer_willow: shortened from 260f (10.833s) back to 129f (5.375s), all willow (2.625-8.000s)
            sp = p2_raw / "22_shimmer_willow_v02.mp4"
            row["source"] = sp.name
            row["source_path"] = str(sp)
            row["source_sha256"] = sha256_file(sp)
            row["frames"] = 129
            row["upscale"] = 1.0
            row["framing"] = {"offset": 0.0}
            row["disposition"] = "KEEP 22_shimmer_willow_t1 (2.625-8.000s = 129f, all willow, no 15_desk_candle repeat) (J0826)"
        elif cut_num == 62:
            # #62 P4 11_night_jars: 11_night_jars_t1 (4.30-8.00s at 0.635x = 140f) + 18_dark_window_t1 (4.00-6.00s = 48f) = 188f
            sp = p4_raw / "11_night_jars_v02.mp4"
            row["source"] = sp.name
            row["source_path"] = str(sp)
            row["source_sha256"] = sha256_file(sp)
            row["frames"] = 188
            row["upscale"] = 1.0
            row["framing"] = {"offset": 0.0}
            row["disposition"] = "KEEP 11_night_jars_t1 (4.30-8.00s at 0.635x = 140f, frame-blended) + 18_dark_window_t1 (4.00-6.00s = 48f, unused by #51) (J0829)"
        elif cut_num in (78, 86):
            sp = Path(row["source_path"])
            row["source_sha256"] = sha256_file(sp)
        elif cut_num == 91:
            row["frames"] = int(row["frames"]) + 1  # match 12188 frames (507.833333 s) of master VO

        n_frames = int(row["frames"])
        t_in = cur_frames / FPS
        cur_frames += n_frames
        t_out = cur_frames / FPS
        row["film_t"] = round(t_in, 3)
        row["timeline_in"] = t_in
        row["timeline_out"] = t_out
        cuts_v02.append(row)

    assert cur_frames == 12188, f"Expected 12188 frames (507.833333 s), got {cur_frames}"

    # Update pool_v02 to match cuts_v02 sources
    pool_map = {(p["file"], p["part"]): dict(p) for p in pool_v01}
    for row in cuts_v02:
        key = (row["source"], row["part"])
        if key not in pool_map:
            pool_map[key] = {
                "file": row["source"],
                "title": "Veo 3.1 clip, Chief KEEP",
                "part": row["part"],
            }
    pool_v02 = list(pool_map.values())

    (V02_DIR / "cuts_full_join_v02.json").write_text(json.dumps(cuts_v02, indent=2) + "\n")
    (V02_DIR / "pool_full_join_v02.json").write_text(json.dumps(pool_v02, indent=2) + "\n")
    print(f"Wrote cuts_full_join_v02.json ({len(cuts_v02)} cuts, {cur_frames} frames = {cur_frames/FPS:.6f} s)")

    # Print Part 02 #18..#33 start/end times to verify exact match with REVIEW_v01 §2
    for idx in range(17, 33):
        row = cuts_v02[idx]
        cn = idx + 1
        s = row["timeline_in"]
        e = row["timeline_out"]
        print(
            f"  #{cn:02d} {row['row']:24s} {int(s//60)}:{s%60:05.2f}-{int(e//60)}:{e%60:05.2f} "
            f"({s:.2f}-{e:.2f}s, frames={row['frames']}) -> {row['source']}"
        )

    tmp = Path("/private/tmp/hos006_join_v02")
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir(parents=True, exist_ok=True)

    seg_files = []
    for idx, row in enumerate(cuts_v02):
        clip_path = Path(row["source_path"])
        if not clip_path.exists():
            raise FileNotFoundError(f"Cut #{idx+1} missing source_path: {clip_path}")
        n_frames = int(row["frames"])
        in_s = float(row.get("framing", {}).get("offset", 0.0))
        seg_out = tmp / f"seg_{idx:03d}.mp4"
        cut_num = idx + 1
        if cut_num == 53:
            vf = "fps=24,scale=2112:1188:flags=lanczos,crop=1920:1080:96:108,setsar=1,format=yuv420p"
        elif cut_num == 57:
            vf = "fps=24,scale=2048:1152:flags=lanczos,crop=1920:1080:64:0,setsar=1,format=yuv420p"
        else:
            vf = "fps=24,scale=1920:1080:flags=lanczos,setsar=1,format=yuv420p"
        cmd = [
            "ffmpeg", "-y", "-v", "error",
        ]
        if in_s > 0.001:
            cmd += ["-ss", f"{in_s:.6f}"]
        cmd += [
            "-i", str(clip_path),
            "-frames:v", str(n_frames),
            "-vf", vf,
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
            "-r", "24", "-an", str(seg_out),
        ]
        subprocess.run(cmd, check=True)
        seg_files.append(seg_out)

    concat_list = tmp / "concat.txt"
    concat_list.write_text("".join(f"file '{p}'\n" for p in seg_files))

    video_only = tmp / "video_only.mp4"
    subprocess.run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-f", "concat", "-safe", "0",
            "-i", str(concat_list),
            "-c", "copy", str(video_only),
        ],
        check=True,
    )

    v01_teach_mp4 = V01_TEACH_DIR / "hos_006_full_join_v01_teach.mp4"
    base_v02_mp4 = tmp / "hos_006_full_join_v02_base.mp4"
    subprocess.run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-i", str(video_only),
            "-i", str(v01_teach_mp4),
            "-map", "0:v:0", "-map", "1:a:0",
            "-c:v", "copy", "-c:a", "copy",
            str(base_v02_mp4),
        ],
        check=True,
    )

    nb = subprocess.check_output(
        [
            "ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0",
            "-show_entries", "stream=nb_read_frames,duration", "-of", "csv=p=0", str(base_v02_mp4),
        ],
        text=True,
    ).strip()
    print(f"Built base join {base_v02_mp4}: duration,frames = {nb}", flush=True)

    for p in seg_files:
        p.unlink(missing_ok=True)
    video_only.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
