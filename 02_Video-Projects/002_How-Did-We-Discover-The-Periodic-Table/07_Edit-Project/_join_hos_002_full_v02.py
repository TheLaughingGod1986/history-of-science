#!/usr/bin/env python3
"""Join LOCKED HOS 002 Parts 01–05 → full v02 with chapter cards + soft joins.

Does not remint 01–05. P01 cold-opens (no card at 0:00). P02 already opens on
its baked CHAPTER 2 parchment card. Insert matching cards before 03 / 04 / 05.
Every part join is paired xfade + acrossfade (0.40s). P05 still owns the house
end card — do not add a second out.

Not LOCKED. Scores → CoS. Do not declare Ben PASS. Do not upload.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
EXP = PROJ / "09_Final-Export"
ICLOUD = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT"
CARD_DIR = PROJ / "07_Edit-Project/chapter_cards_v01"
OUT = EXP / "hos_002_periodic_table_full_v02.mp4"
NOTES = EXP / "FULL_V02_JOIN_NOTES.md"
WATCH = PROJ / "07_Edit-Project/WATCH_full_v02.txt"
CHAP = PROJ / "11_Upload-Package/Chapters/periodic_table_long_chapters_v02.txt"
DESC = PROJ / "11_Upload-Package/Descriptions/periodic_table_long_description_v01.txt"

LOCK = [
    {
        "id": "01",
        "name": "hos_002_part01_rough_v14.mp4",
        "sha": "d903cf7ca1789dcfc1a3703b9215564b3a0d306d0ea1dbf7c2a974888fa92781",
        "chapter": "A zoo of names",
        "card": None,
    },
    {
        "id": "02",
        "name": "hos_002_part02_rough_v06.mp4",
        "sha": "799086795d62f159930bd00db638ea2de0e02a299d8c9d50c8eed3d482e89529",
        "chapter": "First patterns",
        "card": None,  # baked into the locked parent
    },
    {
        "id": "03",
        "name": "hos_002_part03_rough_v09.mp4",
        "sha": "30060612a00d628998008c9946b8e25319b56f3b9e5613b537c5d2be989bbe4e",
        "chapter": "A ruler for atoms",
        "card": "chapter_03.png",
    },
    {
        "id": "04",
        "name": "hos_002_part04_rough_v25.mp4",
        "sha": "e78027c0c58abe9284f7b85de693a08caabd3ad8ee45b64624eadd0329942bb1",
        "chapter": "Empty chairs",
        "card": "chapter_04.png",
    },
    {
        "id": "05",
        "name": "hos_002_part05_rough_v01.mp4",
        "sha": "8dcb06b596318a7283210928fbb0e78f6f89c7db5d200b8edeefbaa9b5522ec4",
        "chapter": "The guests arrive",
        "card": "chapter_05.png",
    },
]

XFADE = 0.40
CARD_HOLD = 3.00
P05_VO = 144.160
P05_CARD_XFADE = 0.35

ENC = [
    "-c:v", "libx264", "-pix_fmt", "yuv420p",
    "-profile:v", "high", "-level", "4.1",
    "-preset", "fast", "-crf", "18", "-r", "24",
    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
    "-movflags", "+faststart",
]


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def probe_dur(p: Path) -> float:
    r = subprocess.run(
        [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(p),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(r.stdout.strip())


def ff(*args: str) -> None:
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *args], check=True)


def fmt_tc(seconds: float) -> str:
    s = int(round(seconds))
    return f"{s // 60}:{s % 60:02d}"


def encode_part(src: Path, dest: Path, dur: float) -> None:
    ff(
        "-i", str(src),
        "-vf", "fps=24,scale=1920:1080:flags=lanczos,format=yuv420p,setsar=1",
        "-t", f"{dur:.6f}",
        *ENC,
        str(dest),
    )


def encode_card(png: Path, dest: Path) -> None:
    ff(
        "-loop", "1", "-i", str(png),
        "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
        "-vf", "fps=24,scale=1920:1080:flags=lanczos,format=yuv420p,setsar=1",
        "-t", f"{CARD_HOLD:.6f}",
        "-shortest",
        *ENC,
        str(dest),
    )


def main() -> None:
    paths: list[Path] = []
    durs: list[float] = []
    print("HASH CHECK", flush=True)
    for item in LOCK:
        exp = EXP / item["name"]
        if not exp.exists():
            raise SystemExit(f"STOP: missing {exp}")
        got = sha256(exp)
        if got != item["sha"]:
            raise SystemExit(f"STOP: hash mismatch {item['name']} {got}")
        dur = probe_dur(exp)
        print(f"  OK {item['id']} {dur:.3f}s {got}", flush=True)
        paths.append(exp)
        durs.append(dur)

    subprocess.run(
        ["python3", str(PROJ / "07_Edit-Project/_render_hos_002_chapter_cards_v01.py")],
        check=True,
    )
    for item in LOCK:
        if item["card"]:
            png = CARD_DIR / item["card"]
            if not png.exists():
                raise SystemExit(f"STOP: missing chapter card {png}")

    work = Path(tempfile.mkdtemp(prefix="hos_002_join_v02_"))
    print(f"WORK {work}", flush=True)

    segs: list[Path] = []
    seg_durs: list[float] = []
    labels: list[str] = []

    for item, src, dur in zip(LOCK, paths, durs):
        if item["card"]:
            cdest = work / f"card{item['id']}.mp4"
            print(f"CARD {item['id']}", flush=True)
            encode_card(CARD_DIR / item["card"], cdest)
            segs.append(cdest)
            seg_durs.append(probe_dur(cdest))
            labels.append(f"card{item['id']}")
        dest = work / f"p{item['id']}.mp4"
        print(f"ENCODE {item['id']}", flush=True)
        encode_part(src, dest, dur)
        segs.append(dest)
        seg_durs.append(probe_dur(dest))
        labels.append(f"p{item['id']}")

    n = len(segs)
    vchain: list[str] = []
    achain: list[str] = []
    running = 0.0
    for i in range(n - 1):
        running += seg_durs[i]
        off = running - (i + 1) * XFADE
        vin = "[0:v]" if i == 0 else f"[vx{i}]"
        ain = "[0:a]" if i == 0 else f"[ax{i}]"
        vout = "vout" if i == n - 2 else f"vx{i+1}"
        aout = "aout" if i == n - 2 else f"ax{i+1}"
        vchain.append(
            f"{vin}[{i+1}:v]xfade=transition=fade:duration={XFADE:.3f}:offset={off:.6f}[{vout}]"
        )
        achain.append(
            f"{ain}[{i+1}:a]acrossfade=d={XFADE:.3f}:c1=tri:c2=tri[{aout}]"
        )
        print(f"  JOIN {labels[i]} → {labels[i+1]}  offset={off:.3f}", flush=True)

    fc = ";".join(vchain + achain)
    args: list[str] = []
    for p in segs:
        args += ["-i", str(p)]
    print("XFADE CHAIN", flush=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    ff(
        *args,
        "-filter_complex", fc,
        "-map", "[vout]", "-map", "[aout]",
        *ENC,
        str(OUT),
    )

    digest = sha256(OUT)
    dur = probe_dur(OUT)
    size = OUT.stat().st_size

    # Chapter starts: P01 at 0. Each later segment starts after
    # previous_duration - xfade. Inserted cards ARE the chapter start for 03–05.
    starts: dict[str, float] = {}
    t = 0.0
    for item, src_dur in zip(LOCK, durs):
        if item["card"]:
            starts[item["id"]] = t
            t += CARD_HOLD - XFADE
            t += src_dur - XFADE
        else:
            starts[item["id"]] = t
            t += src_dur - XFADE

    p05_pic = starts["05"] + CARD_HOLD - XFADE
    card_in = p05_pic + P05_VO - P05_CARD_XFADE
    card_land = card_in + P05_CARD_XFADE

    print(f"SAVED {OUT}", flush=True)
    print(f"SIZE {size}", flush=True)
    print(f"SHA256 {digest}", flush=True)
    print(f"DUR {dur:.3f}", flush=True)
    for item in LOCK:
        print(f"CH_{item['id']} {starts[item['id']]:.3f}", flush=True)

    chap_txt = "".join(
        f"{fmt_tc(starts[item['id']])} {item['chapter']}\n" for item in LOCK
    )
    CHAP.write_text(chap_txt)

    # Refresh in-description chapter block if the v01 file still has the old clock.
    desc = DESC.read_text()
    old_block = (
        "0:00 A zoo of names\n"
        "1:26 First patterns\n"
        "2:50 A ruler for atoms\n"
        "4:19 Empty chairs\n"
        "6:27 The guests arrive\n"
    )
    if old_block in desc:
        DESC.write_text(desc.replace(old_block, chap_txt))
        print("DESC chapters refreshed", flush=True)

    watch = (
        "WATCH THIS FILE ONLY (HOS 002 full v02 — chapter cards + soft joins):\n"
        f"  {OUT.name}\n"
        f"  iCloud: HOS UAT/{OUT.name}\n\n"
        f"sha256={digest}\n"
        f"duration={dur:.3f}\n"
        f"bytes={size}\n"
        "P01 cold open. P02 baked CHAPTER 2 card. Inserted parchment cards before 03–05.\n"
        "xfade+acrossfade 0.40s at every join. One house end card (from P05).\n"
        "Not LOCKED. Scores → CoS. Do NOT declare PASS. No Ben ping. Do not upload.\n"
    )
    WATCH.write_text(watch)

    lines = [
        "# HOS 002 full v02 — chapter cards + soft joins (UAT, not ship lock)",
        "",
        f"**Cut:** `{OUT.name}`",
        f"**sha256:** `{digest}`",
        f"**Duration:** {dur:.3f} s · **Size:** {size} B",
        "**UAT:** CoS watch only. Do **not** declare Ben PASS. Do **not** upload.",
        "",
        "P01 stays a story cold open (house lock — no channel/title bumper at 0:00).",
        "P02 already opens on its locked CHAPTER 2 parchment card.",
        "Parts 03–05 get matching parchment cards stating what the section is about,",
        "then a 0.40s dissolve into the locked picture. Audio acrossfades with picture.",
        "",
        "**Parents LOCKED (hash-checked, not reminted):**",
        "",
        "| Part | File | sha256 | duration |",
        "|---|---|---|---:|",
    ]
    for item, d in zip(LOCK, durs):
        lines.append(f"| {item['id']} | `{item['name']}` | `{item['sha']}` | {d:.3f} |")
    lines += [
        "",
        "| Beat | Time |",
        "|---|---:|",
        f"| P01 start (cold open) | {starts['01']:.3f} |",
        f"| P02 start (baked CHAPTER 2 card) | {starts['02']:.3f} |",
        f"| Card 03 A ruler for atoms | {starts['03']:.3f} |",
        f"| Card 04 Empty chairs | {starts['04']:.3f} |",
        f"| Card 05 The guests arrive | {starts['05']:.3f} |",
        f"| End-card dissolve | {card_in:.3f} |",
        f"| End card on | {card_land:.3f} |",
        f"| Film out | {dur:.3f} |",
        "",
        "YouTube chapters: `11_Upload-Package/Chapters/periodic_table_long_chapters_v02.txt`",
        "",
        "Builder: `07_Edit-Project/_join_hos_002_full_v02.py`",
        "Cards: `07_Edit-Project/_render_hos_002_chapter_cards_v01.py`",
        "",
    ]
    NOTES.write_text("\n".join(lines))

    meta = {
        "file": OUT.name,
        "sha256": digest,
        "duration": dur,
        "bytes": size,
        "xfade": XFADE,
        "card_hold": CARD_HOLD,
        "starts": starts,
        "parents": [
            {**item, "duration": d}
            for item, d in zip(LOCK, durs)
        ],
        "card_in": card_in,
        "card_land": card_land,
        "status": "UAT",
        "locked": False,
        "upload": False,
    }
    (PROJ / "07_Edit-Project/part_full_v02_land_meta.json").write_text(
        json.dumps(meta, indent=2) + "\n"
    )

    ICLOUD.mkdir(parents=True, exist_ok=True)
    subprocess.run(["cp", "-f", str(OUT), str(ICLOUD / OUT.name)], check=True)
    check = ICLOUD / "002_CHECK/FULL"
    if check.parent.exists():
        check.mkdir(parents=True, exist_ok=True)
        subprocess.run(["cp", "-f", str(OUT), str(check / OUT.name)], check=True)
    (ICLOUD / WATCH.name).write_text(watch)
    (ICLOUD / NOTES.name).write_text(NOTES.read_text())
    print(f"ICLOUD {ICLOUD / OUT.name}", flush=True)


if __name__ == "__main__":
    main()
