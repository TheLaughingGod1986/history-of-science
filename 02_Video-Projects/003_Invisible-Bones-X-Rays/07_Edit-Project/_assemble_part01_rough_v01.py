#!/usr/bin/env python3
"""HOS 003 Part 01 rough v01 — KEEP plates + VO draft + ominous bed + open stamp."""
from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

PROJ = Path(__file__).resolve().parents[1]
CLIPS = PROJ / "04_Generated-Clips"
VO = PROJ / "02_Voiceover/05_Master/hos_003_part01_vo_v02_draft.wav"
BED = Path(
    "/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/"
    "001_How-Did-We-Discover-Germs/05_Music/hos_001_part01_ominous_ward_v14_norm.wav"
)
OUT = PROJ / "09_Final-Export/hos_003_part01_rough_v01.mp4"
ICLOUD = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT" / "hos_003_part01_rough_v01.mp4"
WORK = PROJ / "07_Edit-Project/_part01_v01_work"
XFADE = 0.35
CLIP_USE = 8.0
BED_VOL = 0.34
FPS = 24

PLATES = [
    "01_skeleton_without_knife_open_v01.mp4",
    "02_wurzburg_lab_establishing_v03.mp4",
    "03_cathode_tube_hero_v02.mp4",
    "04_electricity_inside_tube_v03.mp4",
    "05_rays_stop_at_glass_v05.mp4",
    "06_explorer_peek_flare_v01.mp4",
    "07_dark_on_purpose_v04.mp4",
    "08_rontgen_late_ots_v01.mp4",
    "09_why_chase_invisible_v01.mp4",
    "10_accident_coming_v01.mp4",
    "11_lab_hold_v01.mp4",
]


def probe(path: Path) -> float:
    return float(
        subprocess.check_output(
            [
                "ffprobe", "-v", "error", "-show_entries", "format=duration",
                "-of", "default=nw=1:nk=1", str(path),
            ],
            text=True,
        ).strip()
    )


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def render_open_stamp(dest: Path) -> None:
    w, h = 1920, 1080
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    text = "A dark lab, 1895"
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Didot.ttc", 54)
    except OSError:
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia.ttf", 48)
        except OSError:
            font = ImageFont.load_default()
    bb = d.textbbox((0, 0), text, font=font)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    # upper-left dark negative space
    x, y = 96, 120
    pad = 18
    d.rounded_rectangle(
        (x - pad, y - pad, x + tw + pad, y + th + pad),
        radius=14,
        fill=(12, 10, 8, 170),
    )
    d.text((x, y), text, fill=(236, 228, 214, 245), font=font)
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.save(dest)


def main() -> None:
    for name in PLATES:
        p = CLIPS / name
        if not p.exists() or p.stat().st_size < 100_000:
            raise SystemExit(f"missing plate {p}")
    if not VO.exists():
        raise SystemExit(f"missing VO {VO}")
    if not BED.exists():
        raise SystemExit(f"missing bed {BED}")

    WORK.mkdir(parents=True, exist_ok=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)

    n = len(PLATES)
    pic_dur = n * CLIP_USE - (n - 1) * XFADE
    stamp = WORK / "open_stamp.png"
    render_open_stamp(stamp)

    # Normalize each plate to 1920x1080 24fps, clip_use, no audio
    normed = []
    for i, name in enumerate(PLATES):
        src = CLIPS / name
        dst = WORK / f"n{i:02d}.mp4"
        subprocess.run(
            [
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-i", str(src),
                "-t", f"{CLIP_USE:.3f}",
                "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,"
                       "pad=1920:1080:(ow-iw)/2:(oh-ih)/2,"
                       f"fps={FPS},format=yuv420p,setsar=1",
                "-an",
                "-c:v", "libx264", "-preset", "fast", "-crf", "18",
                str(dst),
            ],
            check=True,
        )
        normed.append(dst)

    # xfade chain
    inputs = []
    for p in normed:
        inputs += ["-i", str(p)]
    parts = []
    cur = "[0:v]"
    for i in range(1, n):
        offset = i * CLIP_USE - i * XFADE
        out = f"[v{i}]" if i < n - 1 else "[vout]"
        parts.append(
            f"{cur}[{i}:v]xfade=transition=fade:duration={XFADE}:offset={offset:.3f}{out}"
        )
        cur = out
    # open stamp overlay 1.5–5.0s
    t_in, hold = 1.5, 3.5
    fade = 0.45
    parts.append(
        f"[vout]format=rgba[base];"
        f"[{n}:v]format=rgba,"
        f"fade=t=in:st=0:d={fade}:alpha=1,"
        f"fade=t=out:st={hold - fade:.3f}:d={fade}:alpha=1,"
        f"setpts=PTS+{t_in}/TB[st];"
        f"[base][st]overlay=0:0:eof_action=pass,format=yuv420p,setsar=1[v]"
    )
    # audio: VO + looped bed, cut to pic_dur
    # inputs: plates 0..n-1, stamp n, VO n+1, bed n+2
    vo_i = n + 1
    bed_i = n + 2
    parts.append(
        f"[{vo_i}:a]atrim=0:{pic_dur:.3f},asetpts=PTS-STARTPTS,aformat=sample_rates=48000:channel_layouts=stereo[vo];"
        f"[{bed_i}:a]aloop=loop=-1:size=2e9,atrim=0:{pic_dur:.3f},asetpts=PTS-STARTPTS,"
        f"volume={BED_VOL},aformat=sample_rates=48000:channel_layouts=stereo[bed];"
        f"[vo][bed]amix=inputs=2:duration=first:dropout_transition=0[a]"
    )
    fc = ";".join(parts)

    cmd = [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        *inputs,
        "-loop", "1", "-t", f"{hold:.3f}", "-i", str(stamp),
        "-i", str(VO),
        "-i", str(BED),
        "-filter_complex", fc,
        "-map", "[v]", "-map", "[a]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-pix_fmt", "yuv420p", "-r", str(FPS),
        "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart",
        "-t", f"{pic_dur:.3f}",
        str(OUT),
    ]
    subprocess.run(cmd, check=True)

    digest = sha256(OUT)
    ICLOUD.parent.mkdir(parents=True, exist_ok=True)
    ICLOUD.write_bytes(OUT.read_bytes())

    print(f"LANDED {OUT}", flush=True)
    print(f"BYTES {OUT.stat().st_size}", flush=True)
    print(f"SHA256 {digest}", flush=True)
    print(f"DUR {probe(OUT):.3f} (target pic {pic_dur:.3f})", flush=True)
    print(f"ICLOUD {ICLOUD} bytes={ICLOUD.stat().st_size}", flush=True)
    print(f"VO_TRIM note: VO ~{probe(VO):.1f}s vs picture {pic_dur:.1f}s — ~20s overhang cut for v01", flush=True)
    print(f"BED {BED.name} vol={BED_VOL}", flush=True)
    print("PLATES " + " | ".join(PLATES), flush=True)


if __name__ == "__main__":
    main()
