#!/usr/bin/env python3
"""J0835 £0 HOS-specific score and mix; adapted envelope method from J0823."""
from __future__ import annotations

import hashlib
import json
import math
import re
import subprocess as sp
import sys
import wave
from pathlib import Path

import numpy as np

REPO = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
EP = Path("/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/006_Trees-Are-Made-Of-Air")
VO_DIR = EP / "02_Voiceover"
MUSIC_DIR = EP / "05_Music"
SFX_DIR = EP / "06_Sound-Effects"
KIT_DIR = SFX_DIR / "kit_v01"
EDIT_DIR = EP / "07_Edit-Project"
OV_PACK = EDIT_DIR / "teaching_overlays_v01_pack"
WORK = EP / "07_Edit-Project/master_v01"

VO_SRC = EDIT_DIR / "full_join_v02_teach/hos_006_full_join_v03_teach.mp4"
WORDS_JSON = VO_DIR / "words.json"
OV_JSON = OV_PACK / "overlays_v01.json"

SR = 48000
LAST_WORD = 514.260
HOLD = 2.000
FADE = 1.000
TOTAL = 507.833333  # matches 6-part rough total (517.26s)
BPM = 66.0  # 0.800s per beat (exact 16 x 50ms hops -> 75.0 BPM)

CHAPTER_CARDS = [(61.666667,"Five Years and Two Ounces","explain"),(178.666667,"The Air That Mint Repaired","awe"),(273.5,"Bubbles in the Sunlight","explain"),(365.416667,"Carbon From the Sky","awe")]
WHOOSH_PASSES=[]
RUMBLES=[]
CODE_TICKS=[]

GAIN_DB = {"tick": -1.5, "whoosh_card": -8.0, "whoosh_pass": -9.0, "rumble": -3.5}


def read_wav(p: Path) -> np.ndarray:
    with wave.open(str(p)) as w:
        assert w.getframerate() == SR and w.getsampwidth() == 2
        a = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(np.float32) / 32768.0
        return a.reshape(-1, w.getnchannels())


def write_wav_dithered(x: np.ndarray, dst: Path) -> None:
    pcm = (np.clip(x, -1.0, 1.0) * 32767.0).astype("<i2")
    zmask = (pcm[:, 0] == 0) & (pcm[:, 1] == 0)
    if zmask.any():
        idx = np.arange(zmask.sum())
        pcm[zmask, 0] = np.where(idx % 2 == 0, 1, -1)
        pcm[zmask, 1] = np.where(idx % 2 == 0, -1, 1)
    with wave.open(str(dst), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for blk in iter(lambda: fh.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def midi_hz(m: float) -> float:
    return 440.0 * (2.0 ** ((m - 69.0) / 12.0))


def synthesize_raw_score(total_s: float) -> np.ndarray:
    """Original G-major/D-major warm viol-like harmonics and soft harp, 66 BPM.
    Independent melody/harmony from OWB 029; chapter energy crossfades over 3 s.
    """
    n=int(round(total_s*SR)); out=np.zeros((n,2),np.float32)
    chords=[(43,50,55,59),(40,47,52,55),(48,55,60,64),(38,45,50,54),(43,50,59,62),(45,52,57,61)]
    def explain(t):
        value=0.0
        for at,_,mood in CHAPTER_CARDS:
            goal=1.0 if mood=='explain' else 0.0
            if t>=at+3: value=goal
            elif t>=at: return value+(goal-value)*(t-at)/3
        return value
    for b in range(int(math.ceil(total_s/12))):
        a=b*12; z=min(total_s,a+15); i=int(a*SR); j=int(z*SR)
        t=np.arange(j-i,dtype=np.float32)/SR
        env=np.minimum(t/3,1)*np.minimum((z-a-t)/3,1)
        for v,m in enumerate(chords[b%len(chords)]):
            f=midi_hz(m); tone=(np.sin(2*np.pi*f*t)+.12*np.sin(4*np.pi*f*t)+.035*np.sin(6*np.pi*f*t))*.10/(1+v*.3)
            out[i:j,0]+=tone*env*(.65+.04*v)
            out[i:j,1]+=tone*env*(.77-.04*v)
    beat=60/BPM
    for k in range(int(total_s/beat)):
        at=k*beat; i=int(at*SR); j=min(n,i+int(.85*SR));t=np.arange(j-i,dtype=np.float32)/SR
        chord=chords[int(at//12)%len(chords)];f=midi_hz(chord[[0,1,3,2,1,2][k%6]]+12)
        amp=.018+.06*explain(at)
        tone=amp*np.minimum(t/.015,1)*np.exp(-t/.25)*(np.sin(2*np.pi*f*t)+.16*np.sin(4*np.pi*f*t))
        out[i:j,0]+=tone*.7;out[i:j,1]+=tone*.6
    t=np.arange(n,dtype=np.float32)/SR
    out*= (np.minimum(t/1.5,1)*np.minimum((total_s-t)/FADE,1))[:,None]
    out*=10**(-14/20)/max(float(abs(out).max()),1e-9)
    return out


def main() -> int:
    sys.path.insert(0, str(REPO / "scripts"))
    import music_gate
    import sfx_kit

    WORK.mkdir(parents=True, exist_ok=True)
    MUSIC_DIR.mkdir(parents=True, exist_ok=True)
    SFX_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Prepare normalized VO stem (517.26s, -14 LUFS)
    vo_wav = WORK / "stem_vo_v01.wav"
    af_vo = f"apad=whole_dur={TOTAL:.3f},loudnorm=I=-14:TP=-1.5:LRA=11,afade=t=out:st={TOTAL-1.0:.3f}:d=1.0"
    sp.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(VO_SRC), "-af", af_vo, "-ar", str(SR), "-ac", "2", str(vo_wav),
        ],
        check=True,
    )
    write_wav_dithered(read_wav(vo_wav), vo_wav)
    vo_m, vo_i = sfx_kit.ebur128(vo_wav)
    vo_m_arr = np.array(vo_m)
    speaking = (vo_m_arr > sfx_kit.SILENT) & (vo_m_arr >= vo_i - sfx_kit.SPEAKING_WITHIN)
    print(f"VO stem ready: integrated {vo_i:.1f} LUFS, {len(vo_m)} 100ms steps")

    # 2. Synthesize raw score bed and apply J0079 envelope ducking under VO
    raw_bed = synthesize_raw_score(TOTAL) * (10.0 ** (-6.0 / 20.0))
    T = np.arange(len(raw_bed)) / SR
    grid = np.arange(len(vo_m)) * 0.1
    duck = np.zeros_like(grid)
    k_smooth = int(0.4 * SR)

    bed_wav = WORK / "trees006_score_bed_v01.wav"
    write_wav_dithered(raw_bed, bed_wav)
    for _ in range(10):
        bm, bi = sfx_kit.ebur128(bed_wav)
        n = min(len(vo_m), len(bm))
        bm_arr = np.array(bm[:n])
        d = vo_m_arr[:n] - bm_arr
        shortfall = np.where(speaking[:n], np.clip(11.6 - d, 0.0, None), 0.0)
        pause_over = np.where(~speaking[:n], np.clip(bm_arr - (vo_i - 12.0), 0.0, None), 0.0)
        need = np.maximum(shortfall, pause_over)
        if not (d[speaking[:n]] < 10.3).any():
            break
        held = np.array([need[max(0, i - 4) : min(n, i + 5)].max() for i in range(n)])
        duck[:n] = np.minimum(duck[:n] + held, 18.0)
        env_db = np.interp(T, grid, np.convolve(duck, np.ones(5)/5, mode="same"), left=0.0, right=0.0)
        write_wav_dithered(raw_bed * (10.0 ** (-env_db / 20.0))[:, None], bed_wav)

    bed_mp3 = MUSIC_DIR / "trees006_score_bed_v01.mp3"
    sp.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(bed_wav), "-c:a", "libmp3lame", "-b:a", "192k", str(bed_mp3),
        ],
        check=True,
    )
    bm_final, bi_final = sfx_kit.ebur128(bed_mp3)
    print(f"Bed MP3 ready: {bed_mp3.name}, integrated {bi_final:.1f} LUFS")

    prompt_txt = "Warm period chamber score for HOS 006 The Willow Tree That Was Made of Air. Original G major / E minor / C / D harmony, soft viol-like harmonic drones in wonder (0-61.67,178.67-273.5,365.42-end), gentle harp at 66 BPM in experiment/explain (61.67-178.67,273.5-365.42), 3 s mood crossfades at chapter cards. Pace: 60-72 BPM. NOT Betelgeuse, jupiter-music, saturn-rings, sun-brighter, venus, light-speed, mars-robot, nearest-star, earth-spin, or any earlier HOS bed. No modern synth pulse, drums or arpeggio above 75 BPM."
    plan_data = {
        "film": "006_Trees-Are-Made-Of-Air",
        "bed": bed_mp3.name,
        "duration_s": TOTAL,
        "source": "own synthesis (_build_trees006_audio_v01.py), £0 spend, no ElevenLabs credit",
        "prompt": prompt_txt,
        "chapters": [{"start_s":0,"mood":"awe"}]+[{"start_s":t,"title":title,"mood":mood} for t,title,mood in CHAPTER_CARDS],
        "integrated_lufs": round(bi_final, 2),
        "sha256": sha256_file(bed_mp3),
    }
    (MUSIC_DIR / "trees006_score_bed_v01_plan.json").write_text(json.dumps(plan_data, indent=2) + "\n")
    (MUSIC_DIR / "BED_BRIEF_v01.md").write_text("# HOS 006 own synthesized score (J0835, £0)\n\n"+prompt_txt+"\n\nChief authorization: J0835 history, Claude acting Chief 22 Oct 17:52Z. Fit awaits Chief listening review.\n")

    # 3. Synthesize house SFX kit and build 029 SFX stem
    sfx_kit.make(KIT_DIR, "hos", 11)
    whoosh_wav = read_wav(KIT_DIR / "sfx_hos_whoosh_soft_v01.wav")
    whoosh_len = len(whoosh_wav) / SR
    tick_wav = read_wav(KIT_DIR / "sfx_hos_tick_ink_v01.wav")
    rumble_wav = read_wav(KIT_DIR / "sfx_hos_rumble_low_v01.wav")

    ov_labels = json.loads((EDIT_DIR / "full_join_v02_teach/LAY_TIMES_v02.json").read_text())["rows"]
    cues = []
    for o in ov_labels:
        if o["kind"] != "chapter":
            cues.append(("tick", round(float(o["start"]), 3), f"teach overlay: {o['id']}"))
    for t_c, why in CODE_TICKS:
        cues.append(("tick", round(t_c, 3), f"code graphic: {why}"))
    for t_c, title, _ in CHAPTER_CARDS:
        cues.append(("whoosh_card", round(t_c - 0.15, 3), f"chapter card: {title}"))
    for t_c, why in WHOOSH_PASSES:
        cues.append(("whoosh_pass", round(t_c - 0.5 * whoosh_len, 3), why))
    for t_c, why in RUMBLES:
        cues.append(("rumble", round(t_c, 3), why))
    cues.sort(key=lambda c: c[1])

    kit_samples = {
        "tick": tick_wav,
        "whoosh_card": whoosh_wav,
        "whoosh_pass": whoosh_wav,
        "rumble": rumble_wav,
    }
    sfx_mix = np.zeros((int(round(TOTAL * SR)), 2), dtype=np.float32)
    for k, t_c, _ in cues:
        s = kit_samples[k] * (10.0 ** (GAIN_DB[k] / 20.0))
        i = int(round(t_c * SR))
        n = min(len(s), len(sfx_mix) - i)
        if i >= 0 and n > 0:
            sfx_mix[i : i + n] += s[:n]

    sfx_out = SFX_DIR / "stem_sfx_v01.wav"
    write_wav_dithered(sfx_mix, sfx_out)
    # Duck any 100ms window where SFX approaches VO speech or pause limits
    for _ in range(6):
        sm, si = sfx_kit.ebur128(sfx_out)
        n = min(len(vo_m), len(sm))
        sm_arr = np.array(sm[:n])
        sp_breach = np.where(speaking[:n] & (sm_arr > sfx_kit.SILENT), np.clip(11.5 - (vo_m_arr[:n] - sm_arr), 0.0, None), 0.0)
        gap_breach = np.where((~speaking[:n]) & (sm_arr > sfx_kit.SILENT), np.clip(sm_arr - (vo_i - 7.5), 0.0, None), 0.0)
        need = np.maximum(sp_breach, gap_breach)
        if not (need > 0.05).any():
            break
        held = np.array([need[max(0, i - 2) : min(n, i + 3)].max() for i in range(n)])
        env_db = np.interp(T, grid[:n], held, left=0.0, right=0.0)
        sfx_mix = sfx_mix * (10.0 ** (-env_db / 20.0))[:, None]
        write_wav_dithered(sfx_mix, sfx_out)

    (SFX_DIR / "sfx_cues_v01.json").write_text(
        json.dumps(
            {
                "film": "006_Trees-Are-Made-Of-Air",
                "cut_seconds": TOTAL,
                "kit": "kit_v01 (own synthesis via scripts/sfx_kit.py)",
                "gain_db": GAIN_DB,
                "cues": [{"kind": k, "start": t_c, "why": why} for k, t_c, why in cues],
                "spend": "none",
            },
            indent=2,
        )
        + "\n"
    )

    # 4. Run sfx_kit.py level and music_gate.py
    sfx_lv_json = SFX_DIR / "sfx_level_v01.json"
    r_sfx = sp.run(
        [
            sys.executable, str(REPO / "scripts/sfx_kit.py"), "level",
            "--vo", str(vo_wav), "--sfx", str(sfx_out), "--bed", str(bed_mp3),
            "--minutes", f"{TOTAL / 60.0:.2f}", "--out", str(sfx_lv_json),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    print(r_sfx.stdout.strip())

    mg_json = MUSIC_DIR / "music_gate_bed_v01.json"
    r_mg = sp.run(
        [
            sys.executable, str(REPO / "scripts/music_gate.py"),
            str(EP), "--bed", str(bed_mp3), "--out", str(mg_json),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    print(r_mg.stdout.strip())

    # 5. Mix VO + bed + SFX to -14.0 LUFS / <= -1.0 dBTP (two-pass linear loudnorm)
    mix_fc = "[0:a][1:a][2:a]amix=inputs=3:normalize=0:duration=first"
    first_err = sp.run(
        [
            "ffmpeg", "-hide_banner", "-i", str(vo_wav), "-i", str(bed_mp3), "-i", str(sfx_out),
            "-filter_complex", mix_fc + ",loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json[a]",
            "-map", "[a]", "-f", "null", "-",
        ],
        capture_output=True,
        text=True,
        check=True,
    ).stderr
    st = json.loads(re.findall(r'\{[^{}]*"input_i"[^{}]*\}', first_err, re.S)[-1])
    norm = (
        f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={st['input_i']}:measured_TP={st['input_tp']}:"
        f"measured_LRA={st['input_lra']}:measured_thresh={st['input_thresh']}:offset={st['target_offset']}:linear=true"
    )
    master_m4a = WORK / "audio_master_v01.m4a"
    sp.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(vo_wav), "-i", str(bed_mp3), "-i", str(sfx_out),
            "-filter_complex", mix_fc + "," + norm + "[a]",
            "-map", "[a]", "-ar", str(SR), "-c:a", "aac", "-b:a", "256k", str(master_m4a),
        ],
        check=True,
    )
    ll = sp.run(
        ["ffmpeg", "-hide_banner", "-i", str(master_m4a), "-af", "ebur128=peak=true", "-f", "null", "-"],
        capture_output=True,
        text=True,
        check=True,
    ).stderr
    mix_lufs = float(re.findall(r"I:\s*([-\d.]+) LUFS", ll)[-1])
    mix_tp = float(re.findall(r"Peak:\s*([-\d.]+) dBFS", ll)[-1])
    print(f"Master audio mix ready: {master_m4a} -> {mix_lufs:.1f} LUFS, {mix_tp:.1f} dBTP")
    return 0


if __name__ == "__main__":
    sys.exit(main())
