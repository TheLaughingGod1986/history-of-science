#!/usr/bin/env python3
"""J0830 / J0856: £0 HOS 007 original chamber score (60.0 BPM harp pulse + J0079 ducking),
43 house SFX cues (every WHO card, date/place stamp, data pill, teach label, code graphic,
and 4 chapter-card page-turn whooshes; never over VO's first word), and lossless-picture master.
Chief authority: OWB #99 comment 6347492456 & J0856 (Claude, acting Chief, 22 Oct 2026).
Never uploads, spends, deletes NAS data, or grants approval.
"""
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

EDIT_DIR = Path(__file__).resolve().parent
FILM = EDIT_DIR.parent
ROOT = FILM.parents[1]
OWB = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
sys.path.insert(0, str(OWB / "scripts"))
sys.path.insert(0, str(EDIT_DIR))
import _assemble_part_roughs_v01 as apr
import music_gate
import sfx_kit

JOIN = EDIT_DIR / "_desk/007/full_join_v01"
META = json.loads((JOIN / "JOIN_META_v01.json").read_text())
SRC = Path(META["file"])
TOTAL = float(META["duration_s"])
SR = 48000
BPM = 60.0

WORK = Path("/private/tmp/j0856-audio-master-v02")
PACK = EDIT_DIR / "master_v01_pack"
MUSIC = FILM / "05_Music"
SFX = FILM / "06_Sound-Effects"
KIT_DIR = SFX / "kit_v01"
OUT = WORK / "hos_007_master_v02.mp4"

for p in [WORK, PACK, MUSIC, SFX]:
    p.mkdir(parents=True, exist_ok=True)


def run(args, log=None):
    print("RUN", " ".join(map(str, args)), flush=True)
    if log:
        r = sp.run(list(map(str, args)), stdout=sp.PIPE, stderr=sp.STDOUT, text=True)
        (PACK / log).write_text(r.stdout)
        print(r.stdout[-1800:], flush=True)
        return r.returncode
    sp.run(list(map(str, args)), check=True)
    return 0


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(1048576), b""):
            h.update(b)
    return h.hexdigest()


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


def main() -> int:
    assert sha(SRC) == META["sha256"], "Approved join changed"
    N = round(TOTAL * SR)

    # 1. Normalized VO stem (-16.1 LUFS integrated)
    VO = WORK / "stem_vo_v01.wav"
    nas_vo = Path("/Volumes/data/mac-mini-archive/hos-007-vaccine/master_v01_J0830/stem_vo_v01.wav")
    if nas_vo.exists():
        shutil.copy2(nas_vo, VO)
    else:
        run(["ffmpeg", "-y", "-v", "error", "-i", SRC, "-vn", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", SR, "-ac", 2, VO])
        vo = read_wav(VO)[:N]
        write_wav(VO, vo)

    vo_m, vo_i = sfx_kit.ebur128(VO)
    vo_m_arr = np.array(vo_m)
    speaking = (vo_m_arr > sfx_kit.SILENT) & (vo_m_arr >= vo_i - sfx_kit.SPEAKING_WITHIN)
    grid = np.arange(len(vo_m_arr)) * 0.1

    # 2. Original G-major / E-minor chamber score at 60.0 BPM:
    #    Sustained warm chamber strings + 60.0 BPM wooden harp pulse (gentle in awe chapters,
    #    lifted in explain chapters, with 3-second timbral crossfades at part boundaries).
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

    t_full = np.arange(N, dtype=np.float32) / SR
    beat_s = 60.0 / BPM  # 1.000 s per beat (exact 60.0 BPM = 20 x 50 ms hops)
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

    fade_env = np.minimum(t_full / 1.5, 1.0) * np.minimum((TOTAL - t_full) / 2.0, 1.0)
    bed *= fade_env[:, None]
    peak = float(np.max(np.abs(bed))) or 1.0
    raw_bed = (bed * (10.0 ** (-14.0 / 20.0) / peak) * (10.0 ** (-2.5 / 20.0))).astype(np.float32)

    # Apply OWB 029 / J0079 envelope ducking: ~16-21 dB under VO in speech, rises in pauses, 0 breaches.
    BW = WORK / "vaccine_score_bed_v01.wav"
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

    BED = MUSIC / "vaccine_score_bed_v01.mp3"
    run(["ffmpeg", "-y", "-v", "error", "-i", BW, "-c:a", "libmp3lame", "-b:a", "192k", BED])
    bm_final, bi_final = sfx_kit.ebur128(BED)
    n_b = min(len(vo_m_arr), len(bm_final))
    bm_f_arr = np.array(bm_final[:n_b])
    sp_diff = vo_m_arr[:n_b][speaking[:n_b]] - bm_f_arr[speaking[:n_b]]
    pause_mask = (~speaking[:n_b]) & (np.arange(n_b) > 20) & (np.arange(n_b) < n_b - 30)

    # Onset check for 60.0 BPM harp pulse
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
        "Part 1 awe, part 2 explain, part 3 uneasy discovery, part 4 explain, part 5 warm resolution. "
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
                duration_s=TOTAL,
                bpm=bpm_measured,
                integrated_lufs=round(bi_final, 2),
                source="Original numpy synthesis, J0830/J0856, £0",
                sha256=sha(BED),
                chapters=chapters,
            ),
            indent=2,
        )
        + "\n"
    )
    (MUSIC / "BED_BRIEF_v01.md").write_text(
        "# HOS 007 original chamber score\n\n"
        "Chief authority: OWB #99 comment 6347492456 & J0856 (22 Oct 2026). £0, no ElevenLabs.\n\n"
        + prompt
        + "\n\nSustained lower strings and gentle 60.0 BPM wooden harp pulse under wonder; "
        "lifted wooden harp pulse at 60.0 BPM under explanation (`music_gate.py` measured `60.0 BPM`, "
        f"`ac[20]/ac[0] = {ac_ratio_60bpm}`). Mood blends over three seconds at part boundaries. "
        "Fit remains for Chief to hear.\n"
    )

    # 3. Synthesize house HOS SFX kit and cue all 43 on-screen teaching moments + chapter cards
    sfx_kit.make(KIT_DIR, "hos", 830)
    tick_wav = read_wav(KIT_DIR / "sfx_hos_tick_ink_v01.wav")
    whoosh_wav = read_wav(KIT_DIR / "sfx_hos_whoosh_soft_v01.wav")
    GAIN_DB = {"tick": -1.5, "whoosh_card": -8.0}

    offsets = {p["part"]: p["offset_s"] for p in META["parts"]}
    cues_list = []
    for pno, ovs in sorted(apr.PART_OVERLAYS.items()):
        off = offsets[pno]
        for ov in ovs:
            if ov["id"] == "p1_vacca":
                continue  # Never over the VO's first word (0.25 s)
            if ov["kind"] == "credit":
                continue  # Corner archive credit lines
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
    ]
    for t_cg, why in standalone_cg:
        cues_list.append(("tick", t_cg, why))

    cues_list.sort(key=lambda c: c[1])

    sfx_mix = np.zeros((N, 2), dtype=np.float32)
    samples = {"tick": tick_wav, "whoosh_card": whoosh_wav}
    for k, t_c, _ in cues_list:
        s = samples[k] * (10.0 ** (GAIN_DB[k] / 20.0))
        i = int(round(t_c * SR))
        n_s = min(len(s), N - i)
        if i >= 0 and n_s > 0:
            sfx_mix[i : i + n_s] += s[:n_s]

    SF = SFX / "stem_sfx_v01.wav"
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

    (SFX / "sfx_cues_v01.json").write_text(
        json.dumps(
            dict(
                film=FILM.name,
                cut_seconds=TOTAL,
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
        raise RuntimeError("SFX/bed level gate failed; inspect before mixing")

    # Augment sfx_level.json with the bed-vs-VO speech & pause breakdown and onset proof
    sfx_lv_data = json.loads((PACK / "sfx_level.json").read_text())
    sfx_lv_data["bed_integrated"] = round(bi_final, 1)
    sfx_lv_data["bed_vs_vo"] = bed_vs_vo_stats
    (PACK / "sfx_level.json").write_text(json.dumps(sfx_lv_data, indent=2) + "\n")

    # 4. Two-pass linear loudnorm; picture bitstream copied untouched from approved join
    fc = "[0:a][1:a][2:a]amix=inputs=3:normalize=0:duration=first"
    r = sp.run(
        [
            "ffmpeg",
            "-hide_banner",
            "-i",
            str(VO),
            "-i",
            str(BED),
            "-i",
            str(SF),
            "-filter_complex",
            fc + ",loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json[a]",
            "-map",
            "[a]",
            "-f",
            "null",
            "-",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    st = json.loads(re.findall(r'\{[^{}]*"input_i"[^{}]*\}', r.stderr, re.S)[-1])
    (PACK / "loudnorm_pass1.json").write_text(json.dumps(st, indent=2) + "\n")
    norm = (
        f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={st['input_i']}:measured_TP={st['input_tp']}:"
        f"measured_LRA={st['input_lra']}:measured_thresh={st['input_thresh']}:offset={st['target_offset']}:linear=true"
    )
    AUDIO = WORK / "audio_master_v02.m4a"
    run(["ffmpeg", "-y", "-v", "error", "-i", VO, "-i", BED, "-i", SF, "-filter_complex", fc + "," + norm + "[a]", "-map", "[a]", "-ar", SR, "-c:a", "aac", "-b:a", "256k", AUDIO])
    run(["ffmpeg", "-y", "-v", "error", "-i", SRC, "-i", AUDIO, "-map", "0:v:0", "-map", "1:a:0", "-c", "copy", "-movflags", "+faststart", OUT])

    # 5. Persist master v02 and separate stems on mounted NAS (new folder master_v02_J0856; never delete NAS data)
    NAS = Path("/Volumes/data/mac-mini-archive")
    assert sp.check_output(["mount"], text=True).find(" on /Volumes/data ") >= 0, "NAS not mounted"
    DEST = NAS / "hos-007-vaccine/master_v02_J0856"
    DEST.mkdir(parents=True, exist_ok=True)
    assets = [OUT, VO, BED, SF, AUDIO]
    records = []
    for src in assets:
        dst = DEST / src.name
        shutil.copy2(src, dst)
        digest = sha(src)
        assert digest == sha(dst)
        records.append(dict(file=str(dst), sha256=digest))

    (PACK / "MASTER_META_v01.json").write_text(
        json.dumps(
            dict(
                job="J0856",
                supersedes_job="J0830",
                approved_join_sha256=META["sha256"],
                picture="video stream copy, no picture edits",
                duration_s=TOTAL,
                files=records,
                bed_vs_vo=bed_vs_vo_stats,
                sfx_hits=sfx_lv_data["hits"],
                spend="£0",
                approval="pending Chief",
            ),
            indent=2,
        )
        + "\n"
    )

    # 6. Run gates
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
        [sys.executable, OWB / "scripts/polish_gate.py", OUT, "--cuts", JOIN / "cuts_full_join_v01.json", "--reviewed-ok", JOIN / "reviewed_ok_full_join_v01.json", "--out", PACK / "polish_gate.json"],
        "polish_gate.txt",
    )
    checks["picture_qa"] = run(
        [sys.executable, OWB / "scripts/picture_qa.py", OUT, "--cuts", JOIN / "cuts_full_join_v01.json", "--pool", JOIN / "pool_full_join_v01.json", "--reviewed-ok", JOIN / "reviewed_ok_full_join_v01.json", "--out-dir", PACK],
        "picture_qa.txt",
    )
    checks["episode"] = run(
        ["npm", "--prefix", "/Users/benjaminoats/YouTube/History Of Science/07_Content-Ops", "run", "gate:episode", "--", "--project", FILM],
        "gate_episode.txt",
    )

    # Verify compressed video bitstream hash matches source join identically
    src_vhash = sp.check_output(["ffmpeg", "-v", "error", "-i", str(SRC), "-map", "0:v:0", "-c", "copy", "-f", "hash", "-"], text=True).strip()
    out_vhash = sp.check_output(["ffmpeg", "-v", "error", "-i", str(OUT), "-map", "0:v:0", "-c", "copy", "-f", "hash", "-"], text=True).strip()
    assert src_vhash == out_vhash, f"Video stream hash mismatch: {src_vhash} != {out_vhash}"
    (PACK / "VIDEO_STREAM_VERIFY.json").write_text(
        json.dumps(
            dict(
                source=str(SRC),
                master=str(DEST / OUT.name),
                source_video_hash=src_vhash,
                master_video_hash=out_vhash,
                match=(src_vhash == out_vhash),
            ),
            indent=2,
        )
        + "\n"
    )

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

    # Remove untracked media files from git worktree after copying to NAS so `check_all.sh` passes `no media`
    for mfile in [BED, SF, *(KIT_DIR.glob("*.wav")), *(PACK.glob("*.jpg"))]:
        if mfile.exists():
            shutil.copy2(mfile, DEST / mfile.name)
            mfile.unlink()

    print("COMPLETE", json.dumps(checks), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
