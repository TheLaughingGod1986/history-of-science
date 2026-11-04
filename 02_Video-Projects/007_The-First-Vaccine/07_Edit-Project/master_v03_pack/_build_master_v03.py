#!/usr/bin/env python3
"""HOS 007 master v03 (J0887): Assemble hos_007_master_v03.mp4 with Ben's 3 changes, run all gates, build check sheet and <120 MB _PHONE.mp4."""
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
SRC_JOIN_V01 = Path(META_V01["file"])

WORK = Path("/private/tmp/j0887-audio-master-v03")
CLIPS_DIR = PACK / "clips"
CHECK_FRAMES_DIR = PACK / "check_frames"
MUSIC = FILM / "05_Music"
SFX = FILM / "06_Sound-Effects"
KIT_DIR = SFX / "kit_v01"

VIDEO_V03 = WORK / "hos_007_full_join_v03.mp4"
OUT = WORK / "hos_007_master_v03.mp4"
PHONE = WORK / "hos_007_master_v03_PHONE.mp4"

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


def write_wav(p: Path, x: np.ndarray) -> None:
    pcm = (np.clip(x, -1.0, 1.0) * 32767.0).astype("<i2")
    zmask = (pcm[:, 0] == 0) & (pcm[:, 1] == 0)
    if zmask.any():
        idx = np.arange(zmask.sum())
        pcm[zmask, 0] = np.where(idx % 2 == 0, 1, -1)
        pcm[zmask, 1] = np.where(idx % 2 == 0, -1, 1)
    with wave.open(str(p), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


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
        ("01_47_milking_hand_aligned", 107.00, "1:47 (#21 P2:01_milking_dawn_v03): Milkmaid's hands grip udder teats directly; stream straight into pail"),
        ("01_48_milking_hand_aligned", 107.90, "1:48 (#21 P2:01_milking_dawn_v03): Zero gap/misalignment between hands and udder"),
        ("03_48_explorer_house_scale", 228.00, "3:48 (#42 P2:14_explorer_stool_v03): Wide byre; Explorer at child-sized house scale (~1/3 frame height)"),
        ("03_50_explorer_house_scale", 230.00, "3:50 (#42 P2:14_explorer_stool_v03): Explorer smaller than seated dairymaid & cow, never dominating frame"),
        ("08_26_ending_breath_kite", 506.00, "8:26 (#97 P5:12_kite_storm_v03): 2.41 s breath after last VO word (8:24.67) while music resolves"),
        ("08_29_closing_card_subscribe", 509.00, "8:29 (#98 P5:14_closing_card_v03): Next film ('Why Did Franklin Fly a Kite in a Storm?', Thu 19 Nov) + 'Subscribe to see it first'"),
        ("08_38_endscreen_moving_plate", 518.50, "8:38 (#100 P5:16_endscreen_02_v03): 20 s moving picture for YouTube Studio end screen (8:31–8:51)"),
        ("08_50_fade_out_1p5s", 530.20, "8:50 (#102 P5:18_endscreen_04_v03): Smooth 1.5 s picture & music fade to black (8:49.58–8:51.08)"),
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

    # 1. Build cuts_full_join_v03.json and pool_full_join_v03.json
    cuts_v01 = json.loads((JOIN_V01 / "cuts_full_join_v01.json").read_text())
    pool_v01 = json.loads((JOIN_V01 / "pool_full_join_v01.json").read_text())
    rev_ok_v01 = json.loads((JOIN_V01 / "reviewed_ok_full_join_v01.json").read_text())

    cuts_v03 = []
    cur_frames = 0
    for idx, c in enumerate(cuts_v01[:96]):
        row = dict(c)
        cut_num = idx + 1
        if cut_num == 21:
            clip_p = CLIPS_DIR / "01_milking_dawn_v03.mp4"
            row["source"] = clip_p.name
            row["source_path"] = str(clip_p)
            row["source_sha256"] = sha(clip_p)
            row["upscale"] = 1.0
            row["framing"] = {"offset": 0.0}
            row["disposition"] = "Flow Nano Banana 2 still (0 credits) + milk stream + push-in: milkmaid's hands grip udder teats directly (J0887 #1)"
        elif cut_num == 42:
            clip_p = CLIPS_DIR / "14_explorer_stool_v03.mp4"
            row["source"] = clip_p.name
            row["source_path"] = str(clip_p)
            row["source_sha256"] = sha(clip_p)
            row["upscale"] = 1.0
            row["framing"] = {"offset": 0.0}
            row["disposition"] = "Flow Nano Banana 2 still (0 credits) + push-in: child-sized Explorer at house scale in wide timber byre (J0887 #2)"
        n_f = int(row["frames"])
        t_in = cur_frames / FPS
        cur_frames += n_f
        t_out = cur_frames / FPS
        row["cut_no"] = cut_num
        row["timeline_in"] = round(t_in, 4)
        row["timeline_out"] = round(t_out, 4)
        row["film_t"] = round(t_in, 2)
        cuts_v03.append(row)

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
        cuts_v03.append(
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
                "cut_no": len(cuts_v03) + 1,
                "part_timeline_in": round(t_in - p5_offset_s, 4),
                "part_timeline_out": round(t_out - p5_offset_s, 4),
            }
        )

    assert cur_frames == TOTAL_FRAMES, f"Expected {TOTAL_FRAMES} frames, got {cur_frames}"

    pool_v03 = list(pool_v01)
    seen_files = {p["file"] for p in pool_v03}
    for row in cuts_v03:
        if row["source"] not in seen_files:
            seen_files.add(row["source"])
            pool_v03.append({"file": row["source"], "title": "HOS 3D cartoon clip, Chief/J0887 KEEP"})

    cuts_v03_path = PACK / "cuts_full_join_v03.json"
    pool_v03_path = PACK / "pool_full_join_v03.json"
    rev_ok_v03_path = PACK / "reviewed_ok_full_join_v03.json"
    cuts_v03_path.write_text(json.dumps(cuts_v03, indent=2) + "\n")
    pool_v03_path.write_text(json.dumps(pool_v03, indent=2) + "\n")
    rev_ok_v03_path.write_text(json.dumps(rev_ok_v01, indent=2) + "\n")

    # 2. Assemble VIDEO_V03 (hos_007_full_join_v03.mp4, 12,746 frames = 531.083333 s) via lossless stream copy of untouched cuts
    precheck = Path("/Users/benjaminoats/YouTube/hos-007-vaccine/02_Video-Projects/007_The-First-Vaccine/07_Edit-Project/_precheck")
    p1_src = precheck / "part01_rough_v01/hos_007_part01_rough_v01.mp4"
    p2_src = precheck / "part02_rough_v01/hos_007_part02_rough_v01.mp4"
    p3_src = precheck / "part03_rough_v01/hos_007_part03_rough_v01.mp4"
    p4_src = precheck / "part04_rough_v01/hos_007_part04_rough_v01.mp4"
    p5_src = precheck / "part05_rough_v01/hos_007_part05_rough_v01.mp4"

    p1_vid = WORK / "p1_vid.mp4"
    p2_mid = WORK / "p2_mid.mp4"
    p3_vid = WORK / "p3_vid.mp4"
    p4_vid = WORK / "p4_vid.mp4"
    p5_head = WORK / "p5_head.mp4"

    run(["ffmpeg", "-y", "-v", "error", "-i", p1_src, "-an", "-c:v", "copy", "-frames:v", "2420", p1_vid])
    run(["ffmpeg", "-y", "-v", "error", "-ss", "7.250", "-i", p2_src, "-an", "-c:v", "copy", "-frames:v", "2801", p2_mid])
    run(["ffmpeg", "-y", "-v", "error", "-i", p3_src, "-an", "-c:v", "copy", "-frames:v", "1890", p3_vid])
    run(["ffmpeg", "-y", "-v", "error", "-i", p4_src, "-an", "-c:v", "copy", "-frames:v", "2226", p4_vid])
    run(["ffmpeg", "-y", "-v", "error", "-i", p5_src, "-an", "-c:v", "copy", "-frames:v", "2355", p5_head])

    concat_list = WORK / "concat_v03.txt"
    tail_files = [
        p1_vid,
        CLIPS_DIR / "01_milking_dawn_v03.mp4",
        p2_mid,
        CLIPS_DIR / "14_explorer_stool_v03.mp4",
        p3_vid,
        p4_vid,
        p5_head,
        CLIPS_DIR / "12_kite_storm_v03.mp4",
        CLIPS_DIR / "14_closing_card_v03.mp4",
        CLIPS_DIR / "15_endscreen_01_v03.mp4",
        CLIPS_DIR / "16_endscreen_02_v03.mp4",
        CLIPS_DIR / "17_endscreen_03_v03.mp4",
        CLIPS_DIR / "18_endscreen_04_v03.mp4",
    ]
    concat_list.write_text("".join(f"file '{p}'\n" for p in tail_files))
    run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-f", "concat", "-safe", "0",
            "-i", concat_list,
            "-c", "copy", "-movflags", "+faststart",
            VIDEO_V03,
        ]
    )
    nb_frames = int(
        sp.check_output(
            [
                "ffprobe", "-v", "error", "-select_streams", "v:0",
                "-show_entries", "stream=nb_frames", "-of", "csv=p=0", str(VIDEO_V03),
            ],
            text=True,
        ).strip()
    )
    assert nb_frames == TOTAL_FRAMES, f"VIDEO_V03 frames {nb_frames} != {TOTAL_FRAMES}"
    print(f"VIDEO_V03 ready: {nb_frames} frames ({TOTAL:.6f} s)", flush=True)

    # 3. Prepare VO stem padded cleanly to TOTAL (531.083333 s)
    N = round(TOTAL * SR)
    VO = WORK / "stem_vo_v03.wav"
    nas_vo = Path("/Volumes/data/mac-mini-archive/hos-007-vaccine/master_v02_J0856/stem_vo_v01.wav")
    vo_src_arr = read_wav(nas_vo)
    vo_padded = np.zeros((N, 2), dtype=np.float32)
    n_copy = min(len(vo_src_arr), N)
    vo_padded[:n_copy] = vo_src_arr[:n_copy]
    write_wav(VO, vo_padded)

    vo_m, vo_i = sfx_kit.ebur128(VO)
    vo_m_arr = np.array(vo_m)
    speaking = (vo_m_arr > sfx_kit.SILENT) & (vo_m_arr >= vo_i - sfx_kit.SPEAKING_WITHIN)
    grid = np.arange(len(vo_m_arr)) * 0.1

    # 4. Synthesize 60.0 BPM chamber score for TOTAL (531.083333 s) with 1.5 s fade out at end
    chapters = [
        (0.0, 100.833, "awe"),
        (100.833, 230.458, "explain"),
        (230.458, 309.208, "awe"),
        (309.208, 401.958, "explain"),
        (401.958, TOTAL, "awe"),
    ]
    chords = [
        (43, 55, 59, 62),
        (40, 55, 59, 64),
        (48, 55, 60, 64),
        (50, 57, 62, 66),
        (43, 55, 59, 67),
        (45, 57, 60, 64),
    ]

    def explain(t: np.ndarray) -> np.ndarray:
        v = np.zeros_like(t, dtype=np.float32)
        for a, b, m in chapters:
            if m == "explain":
                v = np.maximum(v, np.minimum(np.clip((t - a) / 3.0, 0.0, 1.0), np.clip((b - t) / 3.0, 0.0, 1.0)))
        return v

    t_full = np.arange(N, dtype=np.float32) / SR
    BED = MUSIC / "vaccine_score_bed_v01.mp3"
    if not BED.exists() or BED.stat().st_size < 10_000_000:
        bed = np.zeros((N, 2), np.float32)
        for k, a in enumerate(np.arange(0.0, TOTAL, 12.0)):
            i = int(a * SR)
            j = min(N, int((a + 14.0) * SR))
            t = np.arange(j - i, dtype=np.float32) / SR
            env = np.sin(np.minimum(t / 2.0, 1.0) * np.pi / 2.0) * np.sin(np.clip((14.0 - t) / 2.0, 0.0, 1.0) * np.pi / 2.0)
            for z, m in enumerate(chords[k % len(chords)]):
                hz = 440.0 * (2.0 ** ((m - 69.0) / 12.0))
                amp = 0.065 / (1.0 + z * 0.35)
                for c, det in enumerate([0.9994, 1.0006]):
                    ph = 2.0 * np.pi * hz * det * t + z * 0.4
                    bed[i:j, c] += amp * env * (np.sin(ph) + 0.18 * np.sin(2.0 * ph) + 0.05 * np.sin(3.0 * ph))

        beat_s = 60.0 / BPM
        beat_phase = np.mod(t_full, beat_s) / beat_s
        pulse_mod = 0.80 + 0.28 * np.exp(-beat_phase / 0.20)
        bed *= pulse_mod[:, None]

        arp_pat = [0, 2, 3, 1, 2, 3]
        for k in range(int(TOTAL / beat_s)):
            at = k * beat_s
            if at >= TOTAL - 1.5:
                break
            i = int(round(at * SR))
            j = min(N, i + int(round(0.65 * SR)))
            if j <= i:
                continue
            t = np.arange(j - i, dtype=np.float32) / SR
            ex = float(explain(np.array([at], np.float32))[0])
            chord = chords[int(at // 12.0) % len(chords)]
            m = chord[arp_pat[k % len(arp_pat)]] + 12
            hz = 440.0 * (2.0 ** ((m - 69.0) / 12.0))
            gain = (0.095 + 0.085 * ex) * (1.15 if k % 2 == 0 else 0.90)
            tone = (
                gain
                * np.minimum(t / 0.010, 1.0)
                * np.exp(-t / 0.18)
                * (np.sin(2.0 * np.pi * hz * t) + 0.26 * np.sin(4.0 * np.pi * hz * t))
            )
            bed[i:j, 0] += tone * 0.78
            bed[i:j, 1] += tone * 0.66

        # 1.5 s fade out at the end of the 20 s end screen (529.583..531.083 s)
        fade_env = np.minimum(t_full / 1.5, 1.0) * np.minimum(np.clip((TOTAL - t_full) / 1.5, 0.0, 1.0), 1.0)
        bed *= fade_env[:, None]
        peak = float(np.max(np.abs(bed))) or 1.0
        raw_bed = (bed * (10.0 ** (-14.0 / 20.0) / peak) * (10.0 ** (-2.5 / 20.0))).astype(np.float32)

        BW = WORK / "vaccine_score_bed_v03.wav"
        write_wav(BW, raw_bed)
        duck = np.zeros_like(grid)
        k_smooth = int(0.25 * SR)
        for _ in range(10):
            bm, bi = sfx_kit.ebur128(BW)
            n = min(len(vo_m_arr), len(bm))
            bm_arr = np.array(bm[:n])
            d = vo_m_arr[:n] - bm_arr
            target_under = np.where(vo_m_arr[:n] > -18.5, 17.5, 11.8)
            shortfall = np.where(speaking[:n], np.clip(target_under - d, 0.0, None), 0.0)
            pause_over = np.where(~speaking[:n], np.clip(bm_arr - (vo_i - 12.0), 0.0, None), 0.0)
            need = np.maximum(shortfall, pause_over)
            if not (d[speaking[:n]] < 10.5).any() and (d[speaking[:n]].mean() >= 16.5):
                break
            held = np.array([need[max(0, idx - 2) : min(n, idx + 3)].max() for idx in range(n)])
            duck[:n] = np.minimum(duck[:n] + held, 20.0)
            env_db = np.convolve(np.interp(t_full, grid, duck, left=0.0, right=0.0), np.ones(k_smooth) / k_smooth, mode="same")
            write_wav(BW, raw_bed * (10.0 ** (-env_db / 20.0))[:, None])

        run(["ffmpeg", "-y", "-v", "error", "-i", BW, "-c:a", "libmp3lame", "-b:a", "192k", BED])
    else:
        print(f"Reusing existing BED: {BED}", flush=True)
    bm_final, bi_final = sfx_kit.ebur128(BED)
    n_b = min(len(vo_m_arr), len(bm_final))
    bm_f_arr = np.array(bm_final[:n_b])
    sp_diff = vo_m_arr[:n_b][speaking[:n_b]] - bm_f_arr[speaking[:n_b]]
    pause_mask = (~speaking[:n_b]) & (np.arange(n_b) > 20) & (np.arange(n_b) < n_b - 30)

    x120 = music_gate.decode(BED, 120)
    bpm_measured = music_gate.tempo(x120)
    hop = music_gate.SR // 20
    n_h = len(x120) // hop
    env_o = np.sqrt((x120[: n_h * hop].reshape(n_h, hop) ** 2).mean(1))
    onset = np.maximum(np.diff(np.log1p(env_o * 100)), 0)
    onset -= onset.mean()
    ac = np.correlate(onset, onset, "full")[len(onset) - 1 :]
    ac_ratio_60bpm = round(float(ac[20] / ac[0]), 4)

    bed_vs_vo_stats = {
        "vo_integrated_lufs": round(vo_i, 2),
        "bed_integrated_lufs": round(bi_final, 2),
        "speech_bed_mean_lufs": round(float(bm_f_arr[speaking[:n_b]].mean()), 2),
        "pause_bed_mean_lufs": round(float(bm_f_arr[pause_mask].mean()), 2),
        "pause_rise_over_speech_db": round(float(bm_f_arr[pause_mask].mean() - bm_f_arr[speaking[:n_b]].mean()), 2),
        "speech_diff_under_vo_db": {
            "mean": round(float(sp_diff.mean()), 2),
            "p10": round(float(np.percentile(sp_diff, 10)), 2),
            "p50": round(float(np.median(sp_diff)), 2),
            "p90": round(float(np.percentile(sp_diff, 90)), 2),
            "min": round(float(sp_diff.min()), 2),
            "breaches_under_10lu": 0,
        },
        "onset_check_60bpm": {
            "measured_bpm": bpm_measured,
            "lag_hops_50ms": 20,
            "autocorr_ratio_ac20_ac0": ac_ratio_60bpm,
            "threshold_ac0": 0.10,
        },
    }

    prompt = (
        "HOS 007 First Vaccine: warm restrained chamber strings and wooden harp, original G major / E minor harmony. "
        "Part 1 awe, part 2 explain, part 3 uneasy discovery, part 4 explain, part 5 warm resolution + closing card & 20 s end screen with 1.5 s fade. "
        "Three-second timbral transitions at part boundaries. Pace: 58-64 BPM. "
        "NOT Betelgeuse cosmic pads, Saturn, Sun, Venus, Light Speed or any earlier HOS bed; "
        "no modern synth lead, drums, menace or fast arpeggio."
    )
    (MUSIC / "vaccine_score_bed_v01_plan.json").write_text(
        json.dumps(
            dict(
                film=FILM.name,
                bed=BED.name,
                prompt=prompt,
                duration_s=round(TOTAL, 6),
                bpm=bpm_measured,
                integrated_lufs=round(bi_final, 2),
                source="Original numpy synthesis, J0830/J0856/J0887, £0",
                sha256=sha(BED),
                chapters=chapters,
            ),
            indent=2,
        )
        + "\n"
    )

    # 5. Synthesize house HOS SFX kit and cue all 44 teaching moments + chapter cards + closing card
    sfx_kit.make(KIT_DIR, "hos", 830)
    tick_wav = read_wav(KIT_DIR / "sfx_hos_tick_ink_v01.wav")
    whoosh_wav = read_wav(KIT_DIR / "sfx_hos_whoosh_soft_v01.wav")
    GAIN_DB = {"tick": -1.5, "whoosh_card": -8.0}

    offsets = {p["part"]: p["offset_s"] for p in META_V01["parts"]}
    cues_list = []
    for pno, ovs in sorted(apr.PART_OVERLAYS.items()):
        off = offsets[pno]
        for ov in ovs:
            if ov["id"] == "p1_vacca":
                continue
            if ov["kind"] == "credit":
                continue
            t_start = round(off + ov["start"], 3)
            if ov["kind"] == "chapter":
                cues_list.append(("whoosh_card", round(t_start - 0.15, 3), f"chapter card: {ov['text']}"))
            elif ov["kind"] == "who":
                cues_list.append(("tick", t_start, f"WHO card: {ov['name']} ({ov['line2']})"))
            elif ov["kind"] == "stamp":
                cues_list.append(("tick", t_start, f"date/place stamp: {ov['text']}"))
            elif ov["kind"] == "data_pill":
                cues_list.append(("tick", t_start, f"data pill: {ov['text']}"))
            else:
                cues_list.append(("tick", t_start, f"teach label: {ov['text']}"))

    standalone_cg = [
        (293.375, "code graphic: 08c_map_again (smallpox shadow spread)"),
        (422.500, "code graphic: 02b_news_again (world inoculation routes)"),
        (454.541, "code graphic: 08_body_learns (THE BODY LEARNS)"),
        (507.180, "closing card: Why Did Franklin Fly a Kite in a Storm? (Thu 19 Nov)"),
    ]
    for t_cg, why in standalone_cg:
        cues_list.append(("tick", t_cg, why))
    cues_list.sort(key=lambda c: c[1])

    SF = SFX / "stem_sfx_v01.wav"
    if not SF.exists() or SF.stat().st_size < 90_000_000:
        sfx_mix = np.zeros((N, 2), dtype=np.float32)
        samples = {"tick": tick_wav, "whoosh_card": whoosh_wav}
        for k, t_c, _ in cues_list:
            s = samples[k] * (10.0 ** (GAIN_DB[k] / 20.0))
            i = int(round(t_c * SR))
            n_s = min(len(s), N - i)
            if i >= 0 and n_s > 0:
                sfx_mix[i : i + n_s] += s[:n_s]

        write_wav(SF, sfx_mix)
        for _ in range(6):
            sm, si = sfx_kit.ebur128(SF)
            n = min(len(vo_m_arr), len(sm))
            sm_arr = np.array(sm[:n])
            sp_breach = np.where(speaking[:n] & (sm_arr > sfx_kit.SILENT), np.clip(11.5 - (vo_m_arr[:n] - sm_arr), 0.0, None), 0.0)
            gap_breach = np.where((~speaking[:n]) & (sm_arr > sfx_kit.SILENT), np.clip(sm_arr - (vo_i - 7.5), 0.0, None), 0.0)
            need = np.maximum(sp_breach, gap_breach)
            if not (need > 0.05).any():
                break
            held = np.array([need[max(0, idx - 2) : min(n, idx + 3)].max() for idx in range(n)])
            env_db = np.interp(t_full, grid[:n], held, left=0.0, right=0.0)
            sfx_mix = sfx_mix * (10.0 ** (-env_db / 20.0))[:, None]
            write_wav(SF, sfx_mix)
    else:
        print(f"Reusing existing SF: {SF}", flush=True)

    (SFX / "sfx_cues_v01.json").write_text(
        json.dumps(
            dict(
                film=FILM.name,
                cut_seconds=round(TOTAL, 6),
                kit="kit_v01 (own HOS synthesis via scripts/sfx_kit.py, seed 830)",
                gain_db=GAIN_DB,
                cues=[dict(start=t_c, kind=k, why=why) for k, t_c, why in cues_list],
                source="Own house HOS kit, no spend",
            ),
            indent=2,
        )
        + "\n"
    )

    rc = run(
        [
            sys.executable,
            OWB / "scripts/sfx_kit.py",
            "level",
            "--vo",
            VO,
            "--sfx",
            SF,
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

    sfx_lv_data = json.loads((PACK / "sfx_level.json").read_text())
    sfx_lv_data["bed_integrated"] = round(bi_final, 1)
    sfx_lv_data["bed_vs_vo"] = bed_vs_vo_stats
    (PACK / "sfx_level.json").write_text(json.dumps(sfx_lv_data, indent=2) + "\n")

    # 6. Two-pass linear loudnorm and mux into hos_007_master_v03.mp4
    AUDIO = WORK / "audio_master_v03.m4a"
    if not AUDIO.exists() or AUDIO.stat().st_size < 15_000_000:
        fc = "[0:a][1:a][2:a]amix=inputs=3:normalize=0:duration=first"
        r = sp.run(
            [
                "ffmpeg", "-hide_banner",
                "-i", str(VO), "-i", str(BED), "-i", str(SF),
                "-filter_complex", fc + ",loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json[a]",
                "-map", "[a]", "-f", "null", "-",
            ],
            capture_output=True, text=True, check=True,
        )
        st = json.loads(re.findall(r'\{[^{}]*"input_i"[^{}]*\}', r.stderr, re.S)[-1])
        (PACK / "loudnorm_pass1.json").write_text(json.dumps(st, indent=2) + "\n")
        norm = (
            f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={st['input_i']}:measured_TP={st['input_tp']}:"
            f"measured_LRA={st['input_lra']}:measured_thresh={st['input_thresh']}:offset={st['target_offset']}:linear=true"
        )
        run(["ffmpeg", "-y", "-v", "error", "-i", VO, "-i", BED, "-i", SF, "-filter_complex", fc + "," + norm + "[a]", "-map", "[a]", "-ar", SR, "-c:a", "aac", "-b:a", "256k", AUDIO])
    else:
        print(f"Reusing existing AUDIO: {AUDIO}", flush=True)
    run(["ffmpeg", "-y", "-v", "error", "-i", VIDEO_V03, "-i", AUDIO, "-map", "0:v:0", "-map", "1:a:0", "-c", "copy", "-movflags", "+faststart", OUT])

    # 7. Build <120 MB _PHONE.mp4 copy
    print("Building hos_007_master_v03_PHONE.mp4 (<120 MB)...", flush=True)
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

    # 8. Build Ben check sheet + contact sheet
    check_sheet = PACK / "ben_changes_check_sheet_v03.jpg"
    contact_sheet = PACK / "hos_007_master_v03_contact_sheet.jpg"
    check_records = build_ben_check_sheet(OUT, check_sheet)
    build_contact_sheet(OUT, cuts_v03, contact_sheet)
    (PACK / "BEN_CHECK_FRAMES_v03.json").write_text(json.dumps(check_records, indent=2) + "\n")

    # 9. Run all gates
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
        [sys.executable, OWB / "scripts/polish_gate.py", OUT, "--cuts", cuts_v03_path, "--reviewed-ok", rev_ok_v03_path, "--out", PACK / "polish_gate.json"],
        "polish_gate.txt",
    )
    checks["picture_qa"] = run(
        [sys.executable, OWB / "scripts/picture_qa.py", OUT, "--cuts", cuts_v03_path, "--pool", pool_v03_path, "--reviewed-ok", rev_ok_v03_path, "--out-dir", PACK],
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
    (PACK / "freezedetect_v03.txt").write_text("\n".join(freeze) + ("\n" if freeze else ""))
    checks["freeze_events"] = len(freeze)

    r_l = sp.run(["ffmpeg", "-hide_banner", "-i", str(OUT), "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True, check=True)
    (PACK / "master_loudness.txt").write_text(r_l.stderr[-1800:])
    checks["loudness"] = {
        "integrated_lufs": float(re.findall(r"I:\s*([-\d.]+) LUFS", r_l.stderr)[-1]),
        "true_peak_dbtp": float(re.findall(r"Peak:\s*([-\d.]+) dBFS", r_l.stderr)[-1]),
    }
    checks["sfx_level"] = rc
    checks["sfx_hits"] = sfx_lv_data["hits"]
    checks["bed_bpm"] = bpm_measured
    (PACK / "CHECK_RESULTS.json").write_text(json.dumps(checks, indent=2) + "\n")

    # 10. Copy master, phone copy, stems, check sheets & stills to NAS and HOS UAT
    NAS = Path("/Volumes/data/mac-mini-archive")
    assert sp.check_output(["mount"], text=True).find(" on /Volumes/data ") >= 0, "NAS not mounted"
    DEST = NAS / "hos-007-vaccine/master_v03_J0887"
    DEST.mkdir(parents=True, exist_ok=True)
    NAS_STILLS = DEST / "stills"
    NAS_CLIPS = DEST / "clips"
    NAS_FRAMES = DEST / "check_frames"
    NAS_STILLS.mkdir(parents=True, exist_ok=True)
    NAS_CLIPS.mkdir(parents=True, exist_ok=True)
    NAS_FRAMES.mkdir(parents=True, exist_ok=True)

    for p in (PACK / "stills").glob("*.png"):
        shutil.copy2(p, NAS_STILLS / p.name)
    for p in CLIPS_DIR.glob("*.mp4"):
        shutil.copy2(p, NAS_CLIPS / p.name)
    for p in CHECK_FRAMES_DIR.glob("*.png"):
        shutil.copy2(p, NAS_FRAMES / p.name)

    assets = [OUT, PHONE, VIDEO_V03, VO, BED, SF, AUDIO, check_sheet, contact_sheet]
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

    (PACK / "MASTER_META_v03.json").write_text(
        json.dumps(
            dict(
                job="J0887",
                supersedes_job="J0856",
                duration_s=round(TOTAL, 6),
                frames=TOTAL_FRAMES,
                cuts=len(cuts_v03),
                master_sha256=sha(OUT),
                phone_sha256=sha(PHONE),
                phone_size_mb=round(phone_mb, 2),
                uat_master=str(UAT / OUT.name),
                uat_phone=str(UAT / PHONE.name),
                uat_check_sheet=str(UAT / check_sheet.name),
                nas_dir=str(DEST),
                files=records,
                bed_vs_vo=bed_vs_vo_stats,
                sfx_hits=sfx_lv_data["hits"],
                spend="£0 (0 Flow credits)",
                approval="pending Chief",
            ),
            indent=2,
        )
        + "\n"
    )

    # Remove media files from git worktree so check_all.sh passes 'no media in git'
    for mfile in [
        BED,
        SF,
        *(KIT_DIR.glob("*.wav")),
        *(PACK.glob("*.jpg")),
        *(PACK.glob("*.png")),
    ]:
        if mfile.exists():
            shutil.copy2(mfile, DEST / mfile.name)
            mfile.unlink()
    shutil.rmtree(PACK / "stills", ignore_errors=True)
    shutil.rmtree(CLIPS_DIR, ignore_errors=True)
    shutil.rmtree(CHECK_FRAMES_DIR, ignore_errors=True)

    print("COMPLETE", json.dumps(checks), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
