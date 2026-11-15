#!/usr/bin/env python3
"""J2230 Vaccine Shorts v01. Locked voice only. No new generation, no upload.

Variolation: part01 v03 [67.66, 92.16], four inter-sentence pauses tightened to 0.30 s.
Eradication: Option A from part05 v01b. Drop the defective "have killed" sentence.
Picture: top cover-crop of the locked public master (raw plates are not on the checkout).
The crop stays in the top 720 px so the long's lower-third cards are left out.
"""
from __future__ import annotations

import hashlib
import json
import math
import re
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

REPO = Path(__file__).resolve().parents[3]
FILM = REPO / "02_Video-Projects/007_The-First-Vaccine"
RETIME = FILM / "07_Edit-Project/VO_RETIME_v01.json"
VO_DIR = Path("/Volumes/data/mac-mini-archive/2026-11-05/YouTube/History Of Science/02_Video-Projects/007_The-First-Vaccine/02_Voiceover")
MASTER = Path("/Volumes/data/mac-mini-archive/hos-007-vaccine/master_v04_J0925/hos_007_master_v04.mp4")
BED = Path("/Volumes/data/mac-mini-archive/hos-007-vaccine/master_v04_J0925/vaccine_score_bed_v01.mp3")
OUT = Path("/Users/benjaminoats/_desk/renders/J2230/vaccine_v05")
PART5_OFFSET = 409.59

W, H, FPS = 1080, 1920, 30
CROP_W, CROP_H, CROP_X, CROP_Y = 405, 720, (1920 - 405) // 2, 0
FONT = "/System/Library/Fonts/Supplemental/Didot.ttc"
CREAM, INK, YEL = (245, 232, 210, 255), (16, 14, 12, 255), (255, 224, 0, 255)
WHITE = (255, 255, 255, 255)
PARENT = "How Was the First Vaccine Made? (And Why It's Named After a Cow)"

SOURCES = {
    "variolation": ("part01_the_speckled_monster_v03.mp3", "3881da7b96b4efaadde58287c4151b31c1dd39d337af4fd5dae0c6925ab5fb83", 1, 0.0),
    "eradication": ("part05_the_word_that_saved_millions_v01b.mp3", "18b725326c0b40e6bba2250be9f25a2581366a2ff76a2121fa889191f727557f", 5, PART5_OFFSET),
}
MASTER_SHA = "c7f62adbb241bf3fbfaa3a17929f05768eedcf89044cb2cc5ebd2971c163e810"

# (source start, source end) on the part file, then a breath of this many seconds
# taken from the next piece's picture. The last breath is the loop tail (silence).
PLANS = {
    "variolation": {
        "title": "What Is Variolation?",
        "hook": "SMALLPOX **SORE**",
        "card": ("CALLED VARIOLATION", "the old treatment"),
        "card_word": "variolation",
        "air": "2026-11-28",
        "bed_at": 67.66,
        # The doctor-and-child plate at 67.7 s is too still (frame diff about 1.2).
        # Open on the lancet push at 63.50 s (full-height cover so the point stays
        # in frame) for 1.80 s, then cut to the child as the line reaches the sore.
        "open_pic": (63.50, 1.80),
        "open_crop": (608, 1080, 656, 0),
        # The named 79.60–80.96 pause has the word "but" at 80.06. Keep that word
        # and only shorten the silence on either side of it.
        "pieces": [
            (67.66, 73.35, 0.30),
            (74.10, 77.45, 0.30),
            # variolation runs 79.12-80.06 and but runs 80.06-80.96. The v04
            # windows ended at 79.70 and 80.35, so both words were cut off.
            (78.28, 80.96, 0.0),
            (80.96, 85.20, 0.30),
            (86.26, 92.16, 0.55),
        ],
        "expect": (
            "Doctors took a little matter from a smallpox sore and scratched it into a healthy person's arm. "
            "It usually gave a milder illness, and lifelong protection. It was called variolation. "
            "But some people died from it, and they could pass full smallpox on to others. "
            "So people faced a terrible choice. Risk the treatment, or wait for the monster to come."
        ),
    },
    "eradication": {
        "title": "How Was Smallpox Eradicated?",
        "hook": "SMALLPOX **GONE**",
        "card": ("8 MAY 1980", "declared gone"),
        "card_word": "1980",
        "air": "2026-11-29",
        "bed_at": 444.75,
        # Include the cut at 443.75 s so the graveyard open is already moving.
        "pic_lead": {0: 1.20},
        "pieces": [
            (35.16, 36.45, 0.45),
            (37.42, 40.72, 0.55),
            (25.36, 34.50, 0.55),
            (70.06, 75.70, 1.15),
        ],
        "expect": (
            "On the eighth of May, nineteen eighty, the world's health leaders declared that smallpox was gone. "
            "Health workers travelled to every country where smallpox still lived, vaccinating everyone around each new case, "
            "until there was nowhere left for it to go. "
            "And because no one alive today needs a vaccine against smallpox, most of us have never seen it at all."
        ),
    },
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def ff(*args: str, cwd: Path | None = None) -> None:
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *args], check=True, cwd=cwd)


def probe(path: Path) -> float:
    return float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        text=True,
    ))


def mean_db(path: Path) -> float:
    err = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af", "volumedetect", "-f", "null", "-"],
        capture_output=True, text=True,
    ).stderr
    return float(re.search(r"mean_volume: (-?[\d.]+)", err).group(1))


def norm(text: str) -> str:
    return re.sub(r"[^a-z0-9']+", " ", text.lower()).strip()


def load_words(part: int) -> list[tuple[str, float, float]]:
    data = json.loads(RETIME.read_text())
    block = next(item for item in data["parts"] if item["part"] == part)
    raw = block["words"]
    words = []
    for i, (start, text) in enumerate(raw):
        end = raw[i + 1][0] if i + 1 < len(raw) else start + 0.35
        words.append((text, float(start), float(end)))
    return words


def words_in(words, start: float, end: float) -> list[tuple[str, float, float]]:
    return [(w, s, e) for w, s, e in words if start - 0.04 <= s < end - 0.01]


def check_sources() -> None:
    if sha256(MASTER) != MASTER_SHA:
        raise SystemExit("master hash mismatch; refusing to cut")
    for name, expected, _part, _off in SOURCES.values():
        got = sha256(VO_DIR / name)
        if got != expected:
            raise SystemExit(f"VO hash mismatch: {name} {got}")
    if not BED.exists():
        raise SystemExit(f"missing bed {BED}")


def render_text(path: Path, text: str, size: int, y: int, *, hook: bool = False) -> None:
    font = ImageFont.truetype(FONT, size, index=2)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    tokens = [(word.strip("*"), word.startswith("**")) for word in text.split()]
    lines, cur = [], []
    for tok in tokens:
        trial = " ".join(t for t, _ in cur + [tok])
        if cur and font.getlength(trial) > W - 80:
            lines.append(cur)
            cur = [tok]
        else:
            cur.append(tok)
    lines.append(cur)
    asc, desc = font.getmetrics()
    gap = int(size * (0.18 if hook else 0.12))
    lh = asc + desc
    cy = y
    space = font.getlength(" ")
    stroke = 10 if hook else 4
    for line in lines:
        x = (W - font.getlength(" ".join(t for t, _ in line))) / 2
        for t, hot in line:
            fill = YEL if hot else (WHITE if hook else CREAM)
            draw.text((x, cy), t, font=font, fill=fill, stroke_width=stroke, stroke_fill=INK)
            x += font.getlength(t) + space
        cy += lh + gap
    img.save(path)


def render_card(path: Path, line1: str, line2: str) -> None:
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    band_top = (H - 608) // 2
    band_bot = band_top + 608
    shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(shade)
    top, bot = band_bot - 280, band_bot + 40
    for yy in range(top, bot):
        edge = min(yy - top, bot - yy) / 80
        alpha = int(150 * max(0.0, min(1.0, edge)))
        draw.line([(0, yy), (W, yy)], fill=(0, 0, 0, alpha))
    img = Image.alpha_composite(img, shade)
    d = ImageDraw.Draw(img)
    f1 = ImageFont.truetype(FONT, 64, index=2)
    f2 = ImageFont.truetype(FONT, 40, index=0)
    d.text((72, band_bot - 150), line1, font=f1, fill=YEL, stroke_width=4, stroke_fill=INK)
    d.text((72, band_bot - 70), line2, font=f2, fill=CREAM, stroke_width=3, stroke_fill=INK)
    img.save(path)


def build_one(sid: str) -> dict:
    plan = PLANS[sid]
    work = OUT / sid
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    vo_name, _sha, part, offset = SOURCES[sid]
    src = VO_DIR / vo_name
    words = load_words(part)
    pieces = plan["pieces"]

    # Audio spans are the speech pieces. Breaths are silence. The last breath is the tail,
    # and its picture continues past the speech if the source has frames left.
    labels = []
    clock = 0.0
    mapped = []
    audio_fc = []
    seg_paths = []
    for i, (a, b, breath) in enumerate(pieces):
        dur = b - a
        taken = words_in(words, a, b)
        for w, s, e in taken:
            mapped.append((w, round(clock + (s - a), 3), round(clock + min(e, b) - a, 3)))
        labels.append({"kind": "speech", "src": [a, b], "out": [round(clock, 3), round(clock + dur, 3)]})
        audio_fc.append(
            f"[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,"
            f"afade=t=in:d=0.015,afade=t=out:st={max(0.02, dur - 0.02):.3f}:d=0.015,"
            f"aformat=sample_rates=48000:channel_layouts=stereo[s{i}]"
        )
        clock += dur
        if breath > 0:
            audio_fc.append(
                f"anullsrc=r=48000:cl=stereo,atrim=0:{breath:.3f},asetpts=PTS-STARTPTS[g{i}]"
            )
            labels.append({"kind": "breath", "s": breath, "out": [round(clock, 3), round(clock + breath, 3)]})
            clock += breath

    spoken_raw = " ".join(w for w, _, _ in mapped)
    spoken_norm = norm(spoken_raw).replace("8th", "eighth").replace("1980", "nineteen eighty")
    spoken_norm = spoken_norm.replace("traveled", "travelled").replace("onto", "on to")
    if norm(plan["expect"]) not in spoken_norm and spoken_norm != norm(plan["expect"]):
        # ASR writes "1980" and "onto" as one token. The locked sentence still has to be there.
        missing = [tok for tok in norm(plan["expect"]).split() if tok not in spoken_norm.split()]
        allowed = {"nineteen", "eighty", "on", "to"}
        missing = [tok for tok in missing if tok not in allowed]
        if missing:
            (work / "WORD_MISMATCH.txt").write_text(spoken_raw + "\nMISSING " + " ".join(missing) + "\n")
            raise SystemExit(f"{sid}: missing locked words: {' '.join(missing)}\n{spoken_raw}")

    order = []
    for i, (_a, _b, breath) in enumerate(pieces):
        order.append(f"[s{i}]")
        if breath > 0:
            order.append(f"[g{i}]")
    audio_fc.append("".join(order) + f"concat=n={len(order)}:v=0:a=1[a]")
    vo = work / "vo.wav"
    ff("-i", str(src), "-filter_complex", ";".join(audio_fc), "-map", "[a]", "-c:a", "pcm_s16le", str(vo))
    total = probe(vo)
    (work / "spoken.txt").write_text(spoken_raw + "\n")

    # Picture follows the same clock. Breaths play the next speech's opening frames
    # (or, for the tail, the frames just after the last word) so nothing freezes.
    vf = (
        f"crop={CROP_W}:{CROP_H}:{CROP_X}:{CROP_Y},"
        f"scale={W}:{H}:flags=lanczos,setsar=1,fps={FPS}"
    )
    def grab(dst: Path, start: float, dur: float, crop: tuple[int, int, int, int] | None = None) -> None:
        if crop:
            cw, ch, cx, cy = crop
            used = f"crop={cw}:{ch}:{cx}:{cy},scale={W}:{H}:flags=lanczos,setsar=1,fps={FPS}"
        else:
            used = vf
        ff("-ss", f"{start:.3f}", "-i", str(MASTER), "-t", f"{dur:.3f}",
           "-vf", used, "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast",
           "-crf", "18", "-r", str(FPS), str(dst))

    pic_list = work / "pic.txt"
    lines = []
    for i, (a, b, breath) in enumerate(pieces):
        dur = b - a
        lead = plan.get("pic_lead", {}).get(i, 0.0)
        open_pic = plan.get("open_pic") if i == 0 else None
        if open_pic:
            op_s, op_d = open_pic
            op_d = min(op_d, dur - 0.4)
            grab(work / "seg_00a.mp4", op_s, op_d, plan.get("open_crop"))
            grab(work / "seg_00b.mp4", a + offset, dur - op_d)
            lines.append("file 'seg_00a.mp4'\nfile 'seg_00b.mp4'\n")
        else:
            seg = work / f"seg_{i:02d}.mp4"
            grab(seg, a + offset - lead, dur)
            lines.append(f"file '{seg.name}'\n")
        if breath <= 0:
            continue
        hold = work / f"hold_{i:02d}.mp4"
        if i + 1 < len(pieces):
            na, _nb, _ = pieces[i + 1]
            src_s = na + offset
        else:
            src_s = b + offset
        ff("-ss", f"{src_s:.3f}", "-i", str(MASTER), "-t", f"{breath:.3f}",
           "-vf", vf, "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast",
           "-crf", "18", "-r", str(FPS), str(hold))
        lines.append(f"file '{hold.name}'\n")
    pic_list.write_text("".join(lines))
    pic = work / "picture.mp4"
    ff("-f", "concat", "-safe", "0", "-i", "pic.txt", "-c:v", "libx264", "-pix_fmt", "yuv420p",
       "-preset", "veryfast", "-crf", "18", "-r", str(FPS), "-t", f"{total:.3f}", str(pic), cwd=work)

    bed_gain = (mean_db(vo) - 20.0) - mean_db(BED)
    bed = work / "bed.wav"
    ff("-ss", f"{plan['bed_at']:.3f}", "-i", str(BED), "-t", f"{total:.3f}",
       "-af", f"aformat=sample_rates=48000:channel_layouts=stereo,volume={bed_gain:.2f}dB,"
              f"afade=t=in:d=0.05,afade=t=out:st={max(0.1, total - 0.2):.3f}:d=0.2",
       "-c:a", "pcm_s16le", str(bed))
    # One soft tick as the card arrives. No whoosh on the cut.
    sfx = work / "sfx.wav"
    card_at = next((s for w, s, _e in mapped if plan["card_word"] in norm(w)), 4.0)
    if 0.0 <= card_at < 2.0 or 9.0 <= card_at < 14.0:
        card_at = 15.2 if sid == "variolation" else 2.2
    card_out = min(total - 0.4, card_at + 3.4)
    ff("-f", "lavfi", "-i", f"anullsrc=r=48000:cl=stereo:d={total:.3f}",
       "-c:a", "pcm_s16le", str(work / "silence.wav"))
    tick = work / "tick.wav"
    ff("-f", "lavfi", "-i", "sine=frequency=880:duration=0.05:sample_rate=48000",
       "-af", "aformat=channel_layouts=stereo,volume=-12dB,afade=t=out:st=0.03:d=0.02",
       "-c:a", "pcm_s16le", str(tick))
    ff("-i", str(work / "silence.wav"), "-i", str(tick), "-filter_complex",
       f"[1:a]adelay={int(card_at * 1000)}|{int(card_at * 1000)}[t];"
       f"[0:a][t]amix=inputs=2:normalize=0:duration=first[a]",
       "-map", "[a]", "-c:a", "pcm_s16le", str(sfx))

    mix = work / "mix.wav"
    ff("-i", str(vo), "-i", str(bed), "-i", str(sfx), "-filter_complex",
       "[0:a][1:a][2:a]amix=inputs=3:normalize=0:duration=first[a]",
       "-map", "[a]", "-c:a", "pcm_s16le", str(mix))
    measured = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", str(mix),
         "-af", "loudnorm=I=-14:TP=-2.5:LRA=11:print_format=json", "-f", "null", "-"],
        capture_output=True, text=True,
    ).stderr
    blob = measured[measured.rfind("{"): measured.rfind("}") + 1]
    m = json.loads(blob)
    final_audio = work / "audio_norm.wav"
    ff("-i", str(mix), "-af",
       "loudnorm=I=-14:TP=-2.5:LRA=11:"
       f"measured_I={m['input_i']}:measured_LRA={m['input_lra']}:"
       f"measured_TP={m['input_tp']}:measured_thresh={m['input_thresh']}:"
       f"offset={m['target_offset']}:linear=true",
       "-c:a", "pcm_s16le", str(final_audio))

    hook = work / "hook.png"
    render_text(hook, plan["hook"], 168, int(0.12 * H), hook=True)
    title = work / "title.png"
    render_text(title, PARENT, 46, 430)
    card = work / "card.png"
    render_card(card, *plan["card"])
    caps = []
    # Group words into short lines of at most 5 words / 1.6 s.
    group: list[tuple[str, float, float]] = []
    groups = []
    for item in mapped:
        if not group:
            group = [item]
            continue
        span = item[2] - group[0][1]
        if len(group) >= 5 or span >= 1.6 or group[-1][0][-1:] in ".?!":
            groups.append(group)
            group = [item]
        else:
            group.append(item)
    if group:
        groups.append(group)
    for i, group in enumerate(groups):
        png = work / f"cap_{i:03d}.png"
        render_text(png, " ".join(w for w, _, _ in group), 48, H - 280)
        caps.append((png, group[0][1], group[-1][2]))

    inputs = ["-i", str(pic), "-i", str(final_audio), "-loop", "1", "-i", str(hook),
              "-loop", "1", "-i", str(title), "-loop", "1", "-i", str(card)]
    for png, _a, _b in caps:
        inputs += ["-loop", "1", "-i", str(png)]
    fc = [
        f"[2:v]format=rgba[h]",
        f"[0:v][h]overlay=0:0:enable='between(t,0,2)'[v1]",
        f"[3:v]format=rgba[ti]",
        f"[v1][ti]overlay=0:0:enable='between(t,9,14)'[v2]",
        f"[4:v]format=rgba,fade=t=in:st={card_at}:d=0.35:alpha=1,"
        f"fade=t=out:st={card_out - 0.35}:d=0.35:alpha=1[c]",
        f"[v2][c]overlay=0:0:enable='between(t,{card_at:.3f},{card_out:.3f})'[v3]",
    ]
    last = "[v3]"
    for i, (_png, a, b) in enumerate(caps):
        src_i = 5 + i
        nxt = f"[v{i + 4}]"
        fc.append(f"{last}[{src_i}:v]overlay=0:0:enable='between(t,{a:.3f},{b:.3f})'{nxt}")
        last = nxt
    ver = "v06" if sid == "eradication" else "v05"
    mp4 = OUT / f"hos_007_{sid}_{ver}.mp4"
    ff(*inputs, "-filter_complex", ";".join(fc), "-map", last, "-map", "1:a",
       "-c:v", "libx264", "-pix_fmt", "yuv420p", "-profile:v", "high", "-preset", "medium",
       "-crf", "18", "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
       "-t", f"{total:.3f}", "-movflags", "+faststart", str(mp4))
    duration = round(probe(mp4), 3)
    result = {
        "id": sid,
        "file": str(mp4),
        "sha256": sha256(mp4),
        "duration_s": duration,
        "words": len(mapped),
        "within_22_27": 22.0 <= duration <= 27.0,
        "youtube_title": plan["title"],
        "parent_title_on_screen": PARENT,
        "hook": plan["hook"].replace("**", ""),
        "card": plan["card"],
        "card_in_s": round(card_at, 3),
        "card_out_s": round(card_out, 3),
        "air_draft": plan["air"],
        "vo": str(src),
        "pieces": labels,
        "spoken": spoken_raw,
        "bed": str(BED),
        "bed_gain_db": round(bed_gain, 2),
        "picture": "top cover crop of locked master_v04; lower-third cards excluded",
        "spend": 0,
        "approval": "NONE",
    }
    (work / "BUILD.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in ("id", "duration_s", "words", "within_22_27", "sha256")}, indent=2))
    return result


def main() -> None:
    import sys
    OUT.mkdir(parents=True, exist_ok=True)
    check_sources()
    ids = sys.argv[1:] or ["variolation", "eradication"]
    results = [build_one(sid) for sid in ids]
    (OUT / "BUILD.json").write_text(json.dumps(results, indent=2) + "\n")


if __name__ == "__main__":
    main()
