#!/usr/bin/env python3
"""Assemble HOS 002 Part 01 rough v04."""
from pathlib import Path
import runpy

PROJ = Path(__file__).resolve().parent.parent
OUT = PROJ / "09_Final-Export/hos_002_part01_rough_v04.mp4"
# Reuse v03 logic with v04 output path
import json, subprocess
PLATES_JSON = PROJ / "07_Edit-Project/parts/part-01_plates_v01.json"
RAW = PROJ / "04_Generated-Clips/part01/raw/v01_fast"
VO = PROJ / "02_Voiceover/part01_zoo_of_stuff_v02.wav"
CLIP_USE, XFADE = 8.0, 0.4

def probe_dur(path):
    return float(subprocess.check_output(
        ["ffprobe","-v","error","-show_entries","format=duration","-of","default=nw=1:nk=1",str(path)], text=True).strip())

plates = json.loads(PLATES_JSON.read_text())["plates"]
clips = [RAW / f"{p['id']}_v01.mp4" for p in plates]
for mp4 in clips:
    if not mp4.exists() or mp4.stat().st_size < 400_000:
        raise SystemExit(f"missing/small {mp4}")
vo_dur = probe_dur(VO)
pic_dur = len(clips) * CLIP_USE - (len(clips) - 1) * XFADE
if pic_dur + 0.05 < vo_dur:
    raise SystemExit(f"STOP picture {pic_dur:.2f}s < VO {vo_dur:.2f}s")
OUT.parent.mkdir(parents=True, exist_ok=True)
inputs = [x for c in clips for x in ("-i", str(c))] + ["-i", str(VO)]
parts = [f"[{i}:v]trim=0:{CLIP_USE},setpts=PTS-STARTPTS,scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps=24,format=yuv420p[v{i}]" for i in range(len(clips))]
vprev, offset = "v0", CLIP_USE - XFADE
for i in range(1, len(clips)):
    parts.append(f"[{vprev}][v{i}]xfade=transition=fade:duration={XFADE}:offset={offset:.3f}[vx{i}]")
    vprev, offset = f"vx{i}", offset + CLIP_USE - XFADE
n = len(clips)
parts += [f"[{n}:a]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo,atrim=0:{vo_dur:.3f},apad=whole_dur={vo_dur:.3f}[a]", f"[{vprev}]trim=0:{vo_dur:.3f},setpts=PTS-STARTPTS[vout]"]
subprocess.run(["ffmpeg","-y",*inputs,"-filter_complex",";".join(parts),"-map","[vout]","-map","[a]","-c:v","libx264","-preset","fast","-crf","18","-c:a","aac","-b:a","192k","-shortest","-movflags","+faststart",str(OUT)], check=True)
print(f"SAVED {OUT} dur≈{probe_dur(OUT):.2f}s bytes={OUT.stat().st_size}")
ICLOUD = Path("/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/HOS UAT")
if ICLOUD.parent.exists():
    ICLOUD.mkdir(parents=True, exist_ok=True)
    dest = ICLOUD / OUT.name
    subprocess.run(["cp", "-f", str(OUT), str(dest)], check=False)
    print(f"ICLOUD {dest}", flush=True)
