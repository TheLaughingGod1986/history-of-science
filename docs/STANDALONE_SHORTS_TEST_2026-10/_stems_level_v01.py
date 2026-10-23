#!/usr/bin/env python3
"""HOS standalone Shorts S1–S4 (J0171): VO / bed / SFX stems and the Polish-pass SFX level check.

Rebuilds each Short's three stems from SHORTS_INDEX_v01.json (VO take, pause trim, bed gain) and the cut times in
its timeline.json, with the same gains and chains as the mix in _assemble_standalone_shorts_v01.py (before its
loudnorm, which moves all three together). Then runs the house check:
    sfx_kit.py level --vo <vo> --sfx <sfx> --bed <bed> --minutes <len>
Writes stems to _work_shorts_v01/<id>[_v02]/stems/ and SFX_LEVEL_v01.json next to this file. No spend.

    python3 docs/STANDALONE_SHORTS_TEST_2026-10/_stems_level_v01.py --sfx-kit <orbit-with-ben>/scripts/sfx_kit.py
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
VO = HERE / "vo_v01"
WORK = HERE / "_work_shorts_v01"
BED = HERE / "music_v01/hos-standalone-shorts_score_bed_v01.mp3"
SFX = HERE / "sfx_kit_v01"
COVERS = HERE / "covers_j0209_v01"
GATE = REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"
# S4 v02 failed the bed rule for 0.4 s on its last word (0:21.6), so the bed ducks 3 dB before "strength"
# (~21.1 s), keeping the Chief-KEEP v02 picture stream as is. v03's 0.3 s ramp sounded like a hard step
# (Chief, HOS #180 6133314609): the ramp must be at least 1.0 s on a smoothstep curve. (start s, ramp s, dB)
DUCK = {"s4_curie_notebooks": (19.8, 1.3, -3.0)}
DUCK_VER = "_v04"


def ff(*a: str) -> None:
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *a], check=True)


def stems(rec: dict, work: Path) -> dict[str, Path]:
    total = rec["duration_s"]
    vo = work / "vo_trim.wav" if rec["pause_trim_s"] else VO / rec["vo"]
    plan = json.loads((work / "timeline.json").read_text())["plan"]
    cut_times = [p["t0"] for k, p in enumerate(plan) if k and p["plate"] != plan[k - 1]["plate"]]
    out = work / "stems"
    out.mkdir(exist_ok=True)
    p = {"vo": out / "vo.wav", "bed": out / "bed.wav", "sfx": out / "sfx.wav"}
    fmt = "aformat=sample_rates=48000:channel_layouts=stereo"
    ff("-i", str(vo), "-af", f"{fmt},apad=whole_dur={total:.3f}", "-t", f"{total:.3f}", "-c:a", "pcm_s16le",
       str(p["vo"]))
    duck = ""
    if rec["id"] in DUCK:
        t0, ramp, db = DUCK[rec["id"]]
        x = f"clip((t-{t0})/{ramp},0,1)"
        duck = f",asetnsamples=n=240,volume='pow(10,{db}/20*{x}*{x}*(3-2*{x}))':eval=frame"
    ff("-stream_loop", "-1", "-i", str(BED), "-af",
       f"{fmt},atrim=0:{total:.3f},asetpts=PTS-STARTPTS,volume={rec['bed_gain_db']:.2f}dB{duck},afade=t=in:d=0.05,"
       f"afade=t=out:st={total - 0.25:.3f}:d=0.25", "-t", f"{total:.3f}", "-c:a", "pcm_s16le", str(p["bed"]))
    ins = ["-i", str(SFX / "sfx_hos_whoosh_soft_v01.wav")] + sum(
        (["-i", str(SFX / "sfx_hos_tick_ink_v01.wav")] for _ in cut_times), [])
    fc = f"[0:a]{fmt},volume={rec.get('sfx', {}).get('whoosh_db', -14.0):.1f}dB[s0];"
    for i, t in enumerate(cut_times, 1):
        ms = int(t * 1000)
        fc += f"[{i}:a]{fmt},volume=-24dB,adelay={ms}|{ms}[s{i}];"
    fc += "".join(f"[s{i}]" for i in range(len(cut_times) + 1)) + \
        f"amix=inputs={len(cut_times) + 1}:normalize=0:duration=longest,apad=whole_dur={total:.3f}[a]"
    ff(*ins, "-filter_complex", fc, "-map", "[a]", "-t", f"{total:.3f}", "-c:a", "pcm_s16le", str(p["sfx"]))
    return p


def remix(rec: dict, p: dict[str, Path], src: Path, dst: Path) -> None:
    """Same mix as the assembler (amix + loudnorm) from the stems; picture stream copied from src."""
    total = rec["duration_s"]
    audio = p["vo"].parent / "audio_remix.wav"
    ff("-i", str(p["vo"]), "-i", str(p["bed"]), "-i", str(p["sfx"]), "-filter_complex",
       "[0:a][1:a][2:a]amix=inputs=3:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=11[a]",
       "-map", "[a]", "-t", f"{total:.3f}", "-ar", "48000", "-c:a", "pcm_s16le", str(audio))
    ff("-i", str(src), "-i", str(audio), "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac",
       "-b:a", "192k", "-ar", "48000", "-ac", "2", "-t", f"{total:.3f}", "-movflags", "+faststart", str(dst))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sfx-kit", required=True)
    ap.add_argument("--only", nargs="*")
    ns = ap.parse_args()
    index = json.loads((HERE / "SHORTS_INDEX_v01.json").read_text())
    rep_p = HERE / "SFX_LEVEL_v01.json"
    report = json.loads(rep_p.read_text()) if ns.only and rep_p.exists() else {"job": "J0171",
                                                                               "check": "sfx_kit.py level", "shorts": {}}
    ok = True
    for sid, rec in index["shorts"].items():
        if ns.only and not any(sid.startswith(o) for o in ns.only):
            continue
        stem = Path(rec["file"]).stem
        work = WORK / (sid if stem.endswith("_v01") else sid + "_v02")
        p = stems(rec, work)
        if sid in DUCK and not stem.endswith(DUCK_VER):
            src = REPO / rec["file"]
            dst = src.with_name(stem.rsplit("_v", 1)[0] + DUCK_VER + ".mp4")
            remix(rec, p, src, dst)
            g = subprocess.run([sys.executable, str(GATE), "check", str(dst), "--air-date", rec["air_date"]],
                               capture_output=True, text=True)
            rec.update({"file": dst.relative_to(REPO).as_posix(),
                        "sha256": hashlib.sha256(dst.read_bytes()).hexdigest(),
                        "audio_from": src.name, "bed_duck": dict(zip(("t0", "ramp_s", "db"), DUCK[sid])),
                        "gate": {"exit": g.returncode, "output": (g.stdout + g.stderr).strip()[-1500:]}})
            print(f"{sid}: remixed {dst.name}, gate exit {g.returncode}")
            ok &= g.returncode == 0
        r = subprocess.run([sys.executable, ns.sfx_kit, "level", "--vo", str(p["vo"]), "--sfx", str(p["sfx"]),
                            "--bed", str(p["bed"]), "--minutes", f"{rec['duration_s'] / 60:.3f}"],
                           capture_output=True, text=True)
        cover = COVERS / f"hos_sa_{sid.split('_')[0]}_cover_v01.png"
        report["shorts"][sid] = {"file": rec["file"], "sha256": rec["sha256"], "air_date": rec["air_date"],
                                 "cover": cover.relative_to(REPO).as_posix() if cover.exists() else None,
                                 "stems": {k: v.relative_to(REPO).as_posix() for k, v in p.items()},
                                 "level_exit": r.returncode, "level_output": (r.stdout + r.stderr).strip()[-1500:]}
        ok &= r.returncode == 0 and cover.exists()
        print(f"{sid}: level exit {r.returncode} cover {'ok' if cover.exists() else 'MISSING'}")
        print(report["shorts"][sid]["level_output"])
    report["all_pass"] = all(r["level_exit"] == 0 and r["cover"] for r in report["shorts"].values())
    (HERE / "SHORTS_INDEX_v01.json").write_text(json.dumps(index, indent=2) + "\n")
    rep_p.write_text(json.dumps(report, indent=2) + "\n")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
