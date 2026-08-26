#!/usr/bin/env python3
"""Part 02 interim rough while Flow download is hung."""
from __future__ import annotations

import json
import math
import subprocess
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter

PROJ = Path(__file__).resolve().parents[1]
REFS = PROJ / "04_Generated-Clips" / "part02" / "refs"
RAW = PROJ / "04_Generated-Clips" / "part02" / "raw" / "v01_interim"
ASSETS = PROJ / "04_Generated-Clips" / "part01" / "refs" / "v08_micro_assets"
VO = PROJ / "02_Voiceover" / "part02_seeing_tiny_world_v01.mp3"
OUT = PROJ / "09_Final-Export" / "hos_001_part02_rough_v01.mp4"
ART = Path("/opt/cursor/artifacts")
TMP = PROJ / "07_Edit-Project" / "_tmp_p02_interim"
PLATES = json.loads((PROJ / "07_Edit-Project" / "parts" / "part-02_plates_v01.json").read_text())[
    "plates"
]
MICROBE_IDS = {
    "04_plunge_into_drop",
    "05_microbial_city",
    "07_tiny_world_hold",
    "09_faceless_swarm_detail",
}
FPS = 24
N = 192
CLIP_USE = 8.0
XFADE = 0.4


def load_micro(path: Path) -> Image.Image:
    im = Image.open(path).convert("RGBA")
    px = im.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if r < 28 and g < 28 and b < 28:
                px[x, y] = (r, g, b, 0)
            elif r < 45 and g < 45 and b < 45:
                px[x, y] = (r, g, b, int(a * 0.35))
    bb = im.getbbox()
    return im.crop(bb) if bb else im


def zoompan_cmd(still: Path, dest: Path) -> list[str]:
    return [
        "ffmpeg",
        "-y",
        "-loop",
        "1",
        "-i",
        str(still),
        "-vf",
        "scale=1500:844:force_original_aspect_ratio=increase,crop=1500:844,"
        "zoompan=z='min(1+0.002*on\\,1.14)':x='iw/2-(iw/zoom/2)+30*sin(on/35)':"
        "y='ih/2-(ih/zoom/2)+18*cos(on/42)':d=192:s=1280x720:fps=24,format=yuv420p",
        "-t",
        "8",
        "-c:v",
        "libx264",
        "-preset",
        "fast",
        "-crf",
        "17",
        "-an",
        str(dest),
    ]


def make_clip(still: Path, dest: Path, *, with_germs: bool, micros: dict) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    cmd = zoompan_cmd(still, dest)
    if not with_germs:
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"  ok {dest.name}", flush=True)
        return
    work = TMP / dest.stem
    work.mkdir(parents=True, exist_ok=True)
    bed = work / "bed.mp4"
    subprocess.run(zoompan_cmd(still, bed), check=True, capture_output=True)
    for p in work.glob("f_*.png"):
        p.unlink()
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(bed), "-vf", f"fps={FPS}", str(work / "f_%04d.png")],
        check=True,
        capture_output=True,
    )
    frames = sorted(work.glob("f_*.png"))[:N]
    placements = [
        {"name": "sphere_teal", "x0": 0.35, "y0": 0.4, "amp_x": 0.08, "amp_y": 0.07, "scale": 0.1, "speed": 1.0, "phase": 0.2, "rot_speed": -12},
        {"name": "rod_teal", "x0": 0.55, "y0": 0.5, "amp_x": 0.07, "amp_y": 0.09, "scale": 0.12, "speed": 0.9, "phase": 1.1, "rot_speed": 14, "rot0": -15},
        {"name": "spiral", "x0": 0.65, "y0": 0.32, "amp_x": 0.06, "amp_y": 0.08, "scale": 0.09, "speed": 1.2, "phase": 2.0, "rot_speed": 18},
        {"name": "sphere_amber", "x0": 0.28, "y0": 0.58, "amp_x": 0.07, "amp_y": 0.05, "scale": 0.07, "speed": 1.1, "phase": 0.7, "rot_speed": 10},
        {"name": "sphere_teal", "x0": 0.72, "y0": 0.55, "amp_x": 0.05, "amp_y": 0.07, "scale": 0.06, "speed": 1.3, "phase": 1.8, "rot_speed": -14},
    ]
    outd = work / "c"
    outd.mkdir(exist_ok=True)
    for i, fp in enumerate(frames):
        t = i / FPS
        base = Image.open(fp).convert("RGBA")
        W, H = base.size
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        for p in placements:
            m = micros[p["name"]]
            sc = p["scale"] * (1 + 0.05 * math.sin(t * p["speed"] + p["phase"]))
            mw = max(22, int(W * sc))
            mh = int(m.height * (mw / m.width))
            mm = m.resize((mw, mh), Image.Resampling.LANCZOS)
            mm = mm.rotate(
                p.get("rot0", 0) + t * p.get("rot_speed", 0),
                expand=True,
                resample=Image.Resampling.BICUBIC,
            )
            a = ImageEnhance.Brightness(mm.split()[-1]).enhance(0.86)
            mm.putalpha(a)
            x = int(W * (p["x0"] + p["amp_x"] * math.sin(t * p["speed"] + p["phase"])) - mm.width / 2)
            y = int(H * (p["y0"] + p["amp_y"] * math.cos(t * p["speed"] * 0.9 + p["phase"])) - mm.height / 2)
            layer.alpha_composite(mm, (x, y))
        Image.alpha_composite(base, layer.filter(ImageFilter.GaussianBlur(0.4))).convert("RGB").save(
            outd / f"c_{i+1:04d}.png"
        )
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-framerate",
            str(FPS),
            "-i",
            str(outd / "c_%04d.png"),
            "-c:v",
            "libx264",
            "-preset",
            "fast",
            "-crf",
            "17",
            "-pix_fmt",
            "yuv420p",
            "-an",
            str(dest),
        ],
        check=True,
        capture_output=True,
    )
    print(f"  germ ok {dest.name} ({dest.stat().st_size})", flush=True)


def assemble(paths: list[Path]) -> float:
    n = len(paths)
    inputs: list[str] = []
    for c in paths:
        inputs += ["-i", str(c)]
    inputs += ["-i", str(VO)]
    parts = [
        f"[{i}:v]trim=0:{CLIP_USE},setpts=PTS-STARTPTS,"
        f"scale=1280:720:force_original_aspect_ratio=decrease,"
        f"pad=1280:720:(ow-iw)/2:(oh-ih)/2,fps={FPS},format=yuv420p[v{i}]"
        for i in range(n)
    ]
    vprev = "v0"
    offset = CLIP_USE - XFADE
    for i in range(1, n):
        out = f"vx{i}"
        parts.append(
            f"[{vprev}][v{i}]xfade=transition=fade:duration={XFADE}:offset={offset:.3f}[{out}]"
        )
        vprev = out
        offset += CLIP_USE - XFADE
    pic = n * CLIP_USE - (n - 1) * XFADE
    afilter = (
        f"[{n}:a]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo,"
        f"atrim=0:{pic:.3f},apad=whole_dur={pic:.3f}[a]"
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            *inputs,
            "-filter_complex",
            ";".join(parts) + ";" + afilter,
            "-map",
            f"[{vprev}]",
            "-map",
            "[a]",
            "-c:v",
            "libx264",
            "-preset",
            "fast",
            "-crf",
            "17",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-movflags",
            "+faststart",
            str(OUT),
        ],
        check=True,
        capture_output=True,
    )
    return pic


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    TMP.mkdir(parents=True, exist_ok=True)
    micros = {
        "sphere_teal": load_micro(ASSETS / "sphere_teal.png"),
        "sphere_amber": load_micro(ASSETS / "sphere_amber.png"),
        "spiral": load_micro(ASSETS / "spiral.png"),
    }
    rod = ASSETS / "rod_teal_v02.png"
    if not rod.exists():
        rod = ASSETS / "rod_teal.png"
    micros["rod_teal"] = load_micro(rod)

    paths: list[Path] = []
    for plate in PLATES:
        still = REFS / f"{plate['id']}_v01.jpg"
        dest = RAW / f"{plate['id']}_v01.mp4"
        print("clip", plate["id"], flush=True)
        make_clip(still, dest, with_germs=plate["id"] in MICROBE_IDS, micros=micros)
        paths.append(dest)

    pic = assemble(paths)
    ART.mkdir(parents=True, exist_ok=True)
    subprocess.run(["cp", "-f", str(OUT), str(ART / OUT.name)], check=True)
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(OUT),
            "-vf",
            "scale=960:540",
            "-c:v",
            "libx264",
            "-crf",
            "28",
            "-c:a",
            "aac",
            "-b:a",
            "96k",
            "-movflags",
            "+faststart",
            str(ART / "hos_001_part02_rough_v01_demo.mp4"),
        ],
        check=True,
        capture_output=True,
    )
    (ART / "hos_part02_INTERIM_NOTE.txt").write_text(
        "Part 02 rough v01 INTERIM: Flow Veo hung (only captured start-frame JPEG; "
        "no finished mp4 ids). This cut uses continuous camera motion + faceless "
        "drifting microbes on microbe beats. Replace with Flow/Veo I2V when Ultra "
        "download recovers. Style locked to Part 01 v08.\n"
    )
    print(f"SAVED {OUT} ~{pic:.1f}s", flush=True)


if __name__ == "__main__":
    main()
