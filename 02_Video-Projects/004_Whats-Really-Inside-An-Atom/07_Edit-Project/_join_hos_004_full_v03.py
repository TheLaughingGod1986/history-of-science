#!/usr/bin/env python3
"""HOS 004 full join v03 — restore mix level (29 Sep 2026).

UAT only. Do not label KEEP/LOCKED. Do not upload.

Same picture/cards/seams/end as v02. Only fix: amix normalize=0 (v02 halved VO+bed).

- KEEP chapter cards (~1.5 s) at start of Parts 02–05 — real titles, never placeholder.
- TEMP music bed stays PER PART (acrossfade beds at joins; no one continuous bed).
- NO J-cut. Picture xfade 0.40 s.
- VO: butt joins by default (no VO acrossfade) so words are not smeared at seams;
  beds still acrossfade. If vo_check later needs a change, flip SEAM_VO_MODE.
- P01: strip bridge text plate (17_ledger_bridge); extend prior plate.
- P05: keep picture+VO through last word; cream AFTER last word (4 s, bed fades),
  then 20 s quiet cream Studio hold.
- A/V: force |audio−video| ≤ 0.033 s.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
import time
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

PROJ = Path(__file__).resolve().parents[1]
EXP = PROJ / "09_Final-Export"
EDIT = PROJ / "07_Edit-Project"
MUSIC = PROJ / "05_Music"
VO_DIR = PROJ / "02_Voiceover/05_Master"
CREAM_PNG = PROJ / "04_Generated-Clips/part05/refs/hos_end_card_v01.png"
P27_RAW = PROJ / "04_Generated-Clips/part05/raw/v01/27_next_story_rays_v01.mp4"
CARD_DIR = EDIT / "chapter_cards_v02"
ICLOUD_DIR = (
    Path.home()
    / "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT"
    / "004_Whats-Really-Inside-An-Atom"
    / "09_Final-Export"
)
OUT = EXP / "hos_004_full_join_v03.mp4"
NOTES = EXP / "FULL_JOIN_V03_NOTES.md"
META = EDIT / "full_join_v03_land_meta.json"
WATCH = EDIT / "WATCH_full_join_v03.txt"
VO_CHECK_OUT = EDIT / "FULL_JOIN_V03_VO_CHECK.txt"

XFADE = 0.40
CARD_HOLD = 1.50
CREAM_AFTER_VO = 4.00
END_HOLD = 20.00
P01_BRIDGE_CUT = 68.48
P05_CREAM_WAS = 140.50
BED_REL_DB = -20.0
BED_VOLUME = 10 ** (BED_REL_DB / 20.0)
SIDECHAIN = "threshold=0.018:ratio=8:attack=20:release=500:level_sc=1"
BED_XFADE = 0.40

# Per-seam VO mode: "butt" (default) or "acrossfade"
SEAM_VO_MODE = {
    "01→02": "butt",
    "02→03": "butt",
    "03→04": "butt",
    "04→05": "butt",
}

PARENTS = [
    {
        "id": "01",
        "name": "hos_004_part01_rough_v05.mp4",
        "sha": "71d7c70798c77ce2ecb02c37ad043fd98117a2209a84899236337fee8b952add",
        "vo": "hos_004_part01_vo_v04.wav",
        "bed": "hos004-part01-temp_score_bed_v01.mp3",
        "card": None,
    },
    {
        "id": "02",
        "name": "hos_004_part02_rough_v01.mp4",
        "sha": "620ce51250028495a588f25967dddfaa9c6136dc4172c7b0ce1ee609f103f1d2",
        "vo": "hos_004_part02_vo_v04.wav",
        "bed": "hos004-part02-temp_score_bed_v01.mp3",
        "card": {
            "part": "PART 02",
            "date": "1808",
            "title": "The Table That Broke Its Own Rule",
        },
    },
    {
        "id": "03",
        "name": "hos_004_part03_rough_v01.mp4",
        "sha": "d62e0ed096ead8ec52666ca07476f973aeaae7635b70a16faaac45f14ec518e0",
        "vo": "hos_004_part03_vo_v04.wav",
        "bed": "hos004-part03-temp_score_bed_v01.mp3",
        "card": {
            "part": "PART 03",
            "date": "1897",
            "title": "The Crumb Inside the Atom",
        },
    },
    {
        "id": "04",
        "name": "hos_004_part04_rough_v02.mp4",
        "sha": "157feaef7bd21236aeafc3e953fe461fe2ee95896bb868d57357c9c1c2c1e1f5",
        "vo": "hos_004_part04_vo_v04.wav",
        "bed": "hos004-part04-temp_score_bed_v01.mp3",
        "card": {
            "part": "PART 04",
            "date": "1909",
            "title": "The Shell That Bounced Back",
        },
    },
    {
        "id": "05",
        "name": "hos_004_part05_rough_v03.mp4",
        "sha": "b391bff0dbe8a8ae0130adef4f7f3d7b79aca2cb34a934d9cf42d76e1d03363f",
        "vo": "hos_004_part05_vo_v04.wav",
        "bed": "hos004-part05-temp_score_bed_v01.mp3",
        "card": {
            "part": "PART 05",
            "date": "1913",
            "title": "Counting With X-rays",
        },
    },
]

ENC = [
    "-c:v", "libx264", "-pix_fmt", "yuv420p",
    "-profile:v", "high", "-level", "4.1",
    "-preset", "fast", "-crf", "18", "-r", "30",
    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
    "-movflags", "+faststart",
]

W, H = 1920, 1080


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
    subprocess.run(
        ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *args],
        check=True,
    )


def fmt_tc(seconds: float) -> str:
    s = max(0.0, seconds)
    m = int(s // 60)
    rem = s - 60 * m
    return f"{m}:{rem:05.2f}"


def speech_last(wav: Path, thresh_db: float = -38.0) -> float:
    import struct
    import wave

    with wave.open(str(wav), "rb") as w:
        sr = w.getframerate()
        ch = w.getnchannels()
        raw = w.readframes(w.getnframes())
    samples = struct.unpack("<" + "h" * (len(raw) // 2), raw)
    mono = (
        [(samples[i] + samples[i + 1]) / 2 for i in range(0, len(samples), 2)]
        if ch == 2
        else list(samples)
    )
    thresh = (10 ** (thresh_db / 20.0)) * 32768.0
    last = len(mono) - 1 - next(
        (i for i, s in enumerate(reversed(mono)) if abs(s) > thresh), 0
    )
    return last / sr


def font(size: int, bold: bool = False, italic: bool = False) -> ImageFont.FreeTypeFont:
    candidates = []
    if bold and italic:
        candidates += [
            "/System/Library/Fonts/Supplemental/Georgia Bold Italic.ttf",
            "/System/Library/Fonts/Supplemental/Times New Roman Bold Italic.ttf",
        ]
    elif bold:
        candidates += [
            "/System/Library/Fonts/Supplemental/Georgia Bold.ttf",
            "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf",
        ]
    elif italic:
        candidates += [
            "/System/Library/Fonts/Supplemental/Georgia Italic.ttf",
            "/System/Library/Fonts/Supplemental/Times New Roman Italic.ttf",
        ]
    else:
        candidates += [
            "/System/Library/Fonts/Supplemental/Georgia.ttf",
            "/System/Library/Fonts/Supplemental/Times New Roman.ttf",
        ]
    for p in candidates:
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            continue
    return ImageFont.load_default()


def render_chapter_cards() -> dict[str, Path]:
    """Parchment chapter cards — real titles only."""
    CARD_DIR.mkdir(parents=True, exist_ok=True)
    stripe_a, stripe_b = (28, 20, 16), (36, 24, 18)
    plaque, ink, rule, muted = (234, 220, 196), (48, 32, 20), (92, 64, 40), (96, 68, 44)
    out: dict[str, Path] = {}
    for item in PARENTS:
        card = item.get("card")
        if not card:
            continue
        im = Image.new("RGB", (W, H), stripe_a)
        d = ImageDraw.Draw(im)
        for y in range(0, H, 28):
            if (y // 28) % 2 == 0:
                d.rectangle((0, y, W, y + 14), fill=stripe_b)
        x0, y0, x1, y1 = 220, 240, 1700, 840
        d.rounded_rectangle((x0 - 8, y0 - 8, x1 + 8, y1 + 8), radius=6, outline=rule, width=3)
        d.rounded_rectangle((x0, y0, x1, y1), radius=4, fill=plaque)
        d.rounded_rectangle((x0 + 18, y0 + 18, x1 - 18, y1 - 18), radius=2, outline=ink, width=3)

        def center(text: str, y: int, fnt, fill) -> None:
            bb = d.textbbox((0, 0), text, font=fnt)
            tw = bb[2] - bb[0]
            d.text(((W - tw) / 2, y), text, font=fnt, fill=fill)

        center(card["part"], 320, font(34), muted)
        cx, cy = W / 2, 390
        d.line((cx - 200, cy, cx - 16, cy), fill=rule, width=2)
        d.ellipse((cx - 5, cy - 5, cx + 5, cy + 5), fill=ink)
        d.line((cx + 16, cy, cx + 200, cy), fill=rule, width=2)
        center(card["date"], 420, font(110, bold=True), ink)
        # Title may wrap
        title = card["title"]
        f_title = font(40, italic=True)
        bb = d.textbbox((0, 0), title, font=f_title)
        if bb[2] - bb[0] > 1200:
            # two-line wrap at middle word
            words = title.split()
            mid = len(words) // 2
            line1, line2 = " ".join(words[:mid]), " ".join(words[mid:])
            center(line1, 560, f_title, muted)
            center(line2, 620, f_title, muted)
        else:
            center(title, 580, f_title, muted)

        png = CARD_DIR / f"chapter_{item['id']}.png"
        im.save(png, "PNG")
        out[item["id"]] = png
        print(f"CARD {item['id']} {card['title']}", flush=True)
    return out


def encode_silent_video(src: Path, dest: Path, dur: float | None = None) -> None:
    args = [
        "-i", str(src),
        "-an",
        "-vf", f"fps=30,scale={W}:{H}:flags=lanczos,format=yuv420p,setsar=1",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-r", "30",
    ]
    if dur is not None:
        args += ["-t", f"{dur:.6f}"]
    args.append(str(dest))
    ff(*args)


def main() -> None:
    if not CREAM_PNG.exists():
        raise SystemExit(f"STOP: missing cream {CREAM_PNG}")
    if not P27_RAW.exists():
        raise SystemExit(f"STOP: missing {P27_RAW}")

    print("HASH CHECK", flush=True)
    for item in PARENTS:
        exp = EXP / item["name"]
        if not exp.exists():
            raise SystemExit(f"STOP: missing {exp}")
        got = sha256(exp)
        if got != item["sha"]:
            raise SystemExit(f"STOP: hash mismatch {item['name']}")
        print(f"  OK {item['id']} {probe_dur(exp):.3f}s", flush=True)

    card_pngs = render_chapter_cards()
    work = Path(tempfile.mkdtemp(prefix="hos_004_join_v03_"))
    print(f"WORK {work}", flush=True)

    # --- Prepare each part: silent picture (fixed) + VO wav + bed wav ---
    parts_prep: list[dict] = []
    for item in PARENTS:
        src = EXP / item["name"]
        vo_src = VO_DIR / item["vo"]
        bed_src = MUSIC / item["bed"]
        vo_dur = probe_dur(vo_src)
        last = speech_last(vo_src)
        # Keep through last word + tiny tail
        keep_s = min(vo_dur, last + 0.08)

        raw_vid = work / f"p{item['id']}_raw.mp4"
        encode_silent_video(src, raw_vid)

        if item["id"] == "01":
            # Cut bridge text plate; extend last good frame to keep_s
            cut = min(P01_BRIDGE_CUT, probe_dur(raw_vid))
            nobridge = work / "p01_nobridge.mp4"
            ff(
                "-i", str(raw_vid), "-t", f"{cut:.6f}",
                "-c:v", "libx264", "-preset", "fast", "-crf", "18",
                "-pix_fmt", "yuv420p", "-r", "30", str(nobridge),
            )
            vid = work / "p01_vid.mp4"
            ff(
                "-i", str(nobridge),
                "-vf", f"tpad=stop_mode=clone:stop_duration={max(0.05, keep_s - cut + 0.05):.6f}",
                "-t", f"{keep_s:.6f}",
                "-c:v", "libx264", "-preset", "fast", "-crf", "18",
                "-pix_fmt", "yuv420p", "-r", "30", str(vid),
            )
            print(f"  P01 bridge-cut @{cut:.3f} → {keep_s:.3f}s", flush=True)
        elif item["id"] == "05":
            # Keep story through last word: replace cream window with plate 27 hold
            pre = work / "p05_pre.mp4"
            ff(
                "-i", str(raw_vid), "-t", f"{P05_CREAM_WAS:.6f}",
                "-c:v", "libx264", "-preset", "fast", "-crf", "18",
                "-pix_fmt", "yuv420p", "-r", "30", str(pre),
            )
            need = max(0.1, keep_s - P05_CREAM_WAS)
            ext = work / "p05_ext.mp4"
            ff(
                "-i", str(P27_RAW),
                "-vf", (
                    f"fps=30,scale={W}:{H}:flags=lanczos,format=yuv420p,setsar=1,"
                    f"tpad=stop_mode=clone:stop_duration={need + 0.5:.6f}"
                ),
                "-t", f"{need:.6f}",
                "-an",
                "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-r", "30",
                str(ext),
            )
            vid = work / "p05_vid.mp4"
            ff(
                "-i", str(pre), "-i", str(ext),
                "-filter_complex", "[0:v][1:v]concat=n=2:v=1:a=0[v]",
                "-map", "[v]",
                "-t", f"{keep_s:.6f}",
                "-c:v", "libx264", "-preset", "fast", "-crf", "18",
                "-pix_fmt", "yuv420p", "-r", "30", str(vid),
            )
            print(f"  P05 cream-out from {P05_CREAM_WAS:.2f}; story→{keep_s:.3f}s", flush=True)
        else:
            vid = work / f"p{item['id']}_vid.mp4"
            encode_silent_video(raw_vid, vid, keep_s)

        vo = work / f"p{item['id']}_vo.wav"
        ff("-i", str(vo_src), "-t", f"{keep_s:.6f}", "-ar", "48000", "-ac", "2", str(vo))
        bed = work / f"p{item['id']}_bed.wav"
        ff("-i", str(bed_src), "-t", f"{keep_s + CARD_HOLD + 2:.6f}", "-ar", "48000", "-ac", "2", str(bed))

        parts_prep.append(
            {
                "id": item["id"],
                "vid": vid,
                "vo": vo,
                "bed": bed,
                "keep_s": keep_s,
                "card": item.get("card"),
                "card_png": card_pngs.get(item["id"]),
            }
        )
        print(f"  PREP {item['id']} {keep_s:.3f}s", flush=True)

    # --- Build timeline segments (video + optional VO + bed) ---
    # Order: p01, card02, p02, card03, p03, card04, p04, card05, p05, cream4, hold20
    segs: list[dict] = []

    def add_part(p: dict) -> None:
        # Mix part bed ducked under VO → stereo wav; pair with video
        mixed = work / f"mix_{p['id']}.wav"
        fc = (
            f"[1:a]aformat=sample_rates=48000:channel_layouts=stereo,asplit=2[vo_sc][vo_mix];"
            f"[2:a]aformat=sample_rates=48000:channel_layouts=stereo,"
            f"volume={BED_VOLUME:.8f},atrim=0:{p['keep_s']:.6f},asetpts=PTS-STARTPTS[bed];"
            f"[bed][vo_sc]sidechaincompress={SIDECHAIN}[ducked];"
            f"[vo_mix][ducked]amix=inputs=2:weights=1 1:normalize=0:duration=first:dropout_transition=0,"
            f"alimiter=limit=0.8912509:level=false[a]"
        )
        ff(
            "-i", str(p["vid"]), "-i", str(p["vo"]), "-i", str(p["bed"]),
            "-filter_complex", fc,
            "-map", "0:v", "-map", "[a]",
            "-t", f"{p['keep_s']:.6f}",
            *ENC,
            str(work / f"seg_p{p['id']}.mp4"),
        )
        # Also keep separate VO/bed for optional butt rebuild — store mixed seg
        segs.append(
            {
                "label": f"p{p['id']}",
                "path": work / f"seg_p{p['id']}.mp4",
                "kind": "part",
                "part_id": p["id"],
                "dur": p["keep_s"],
                "vo_path": p["vo"],
                "bed_path": p["bed"],
                "vid_path": p["vid"],
            }
        )

    def add_card(p: dict) -> None:
        png = p["card_png"]
        assert png is not None
        # Card video + bed from this part (continuing into the part)
        card_mp4 = work / f"seg_card{p['id']}.mp4"
        bed_trim = work / f"cardbed_{p['id']}.wav"
        ff(
            "-i", str(p["bed"]),
            "-t", f"{CARD_HOLD:.6f}",
            "-af", f"volume={BED_VOLUME:.8f}",
            "-ar", "48000", "-ac", "2",
            str(bed_trim),
        )
        ff(
            "-loop", "1", "-i", str(png),
            "-i", str(bed_trim),
            "-vf", f"fps=30,scale={W}:{H}:flags=lanczos,format=yuv420p,setsar=1",
            "-t", f"{CARD_HOLD:.6f}",
            "-shortest",
            *ENC,
            str(card_mp4),
        )
        segs.append(
            {
                "label": f"card{p['id']}",
                "path": card_mp4,
                "kind": "card",
                "part_id": p["id"],
                "dur": CARD_HOLD,
                "title": p["card"]["title"],
            }
        )

    # p01 first (no card)
    add_part(parts_prep[0])
    for p in parts_prep[1:]:
        add_card(p)
        add_part(p)

    # Cream 4s after last word: bed fade from P05 bed, then quiet
    p05 = parts_prep[-1]
    cream4 = work / "seg_cream4.mp4"
    # bed slice starting near end of P05 for fade continuity
    bed_tail = work / "p05_bed_tail.wav"
    bed_full_dur = probe_dur(p05["bed"])
    start = max(0.0, min(p05["keep_s"] - 0.5, bed_full_dur - CREAM_AFTER_VO - 0.1))
    ff(
        "-ss", f"{start:.6f}", "-i", str(p05["bed"]),
        "-t", f"{CREAM_AFTER_VO:.6f}",
        "-af", f"volume={BED_VOLUME:.8f},afade=t=out:st=0:d={CREAM_AFTER_VO:.6f}",
        "-ar", "48000", "-ac", "2",
        str(bed_tail),
    )
    ff(
        "-loop", "1", "-i", str(CREAM_PNG),
        "-i", str(bed_tail),
        "-vf", f"fps=30,scale={W}:{H}:flags=lanczos,format=yuv420p,setsar=1",
        "-t", f"{CREAM_AFTER_VO:.6f}",
        "-shortest",
        *ENC,
        str(cream4),
    )
    segs.append({"label": "cream4", "path": cream4, "kind": "cream", "dur": CREAM_AFTER_VO})

    hold20 = work / "seg_hold20.mp4"
    ff(
        "-loop", "1", "-i", str(CREAM_PNG),
        "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
        "-vf", f"fps=30,scale={W}:{H}:flags=lanczos,format=yuv420p,setsar=1",
        "-t", f"{END_HOLD:.6f}",
        "-shortest",
        *ENC,
        str(hold20),
    )
    segs.append({"label": "hold20", "path": hold20, "kind": "hold", "dur": END_HOLD})

    # Probe actual seg durs
    for s in segs:
        s["dur"] = probe_dur(s["path"])
        print(f"  SEG {s['label']} {s['dur']:.3f}s", flush=True)

    # --- Soft xfade chain (picture + acrossfade audio) for all but hard-concat hold20 after cream ---
    # Cream→hold is same picture: hard concat after the xfade chain of earlier segs.
    story_segs = segs[:-1]  # through cream4
    hold_seg = segs[-1]

    n = len(story_segs)
    vchain: list[str] = []
    achain: list[str] = []
    running = 0.0
    join_offsets: list[tuple[str, str, float]] = []
    for i in range(n - 1):
        running += story_segs[i]["dur"]
        off = running - (i + 1) * XFADE
        join_offsets.append((story_segs[i]["label"], story_segs[i + 1]["label"], off))
        vin = "[0:v]" if i == 0 else f"[vx{i}]"
        ain = "[0:a]" if i == 0 else f"[ax{i}]"
        vout = "vstory" if i == n - 2 else f"vx{i+1}"
        aout = "astory" if i == n - 2 else f"ax{i+1}"
        vchain.append(
            f"{vin}[{i+1}:v]xfade=transition=fade:duration={XFADE:.3f}:offset={off:.6f}[{vout}]"
        )
        achain.append(
            f"{ain}[{i+1}:a]acrossfade=d={XFADE:.3f}:c1=tri:c2=tri[{aout}]"
        )
        print(f"  JOIN {story_segs[i]['label']}→{story_segs[i+1]['label']} @{off:.3f}", flush=True)

    story = work / "story.mp4"
    args: list[str] = []
    for s in story_segs:
        args += ["-i", str(s["path"])]
    ff(
        *args,
        "-filter_complex", ";".join(vchain + achain),
        "-map", "[vstory]", "-map", "[astory]",
        *ENC,
        str(story),
    )

    # Hard concat quiet hold
    final_tmp = work / "full_v03.mp4"
    ff(
        "-i", str(story), "-i", str(hold_seg["path"]),
        "-filter_complex",
        "[0:v][1:v]concat=n=2:v=1:a=0[v];"
        "[0:a][1:a]concat=n=2:v=0:a=1[a]",
        "-map", "[v]", "-map", "[a]",
        *ENC,
        str(final_tmp),
    )

    # --- A/V sync pad/trim to ≤ 0.033 s ---
    streams = json.loads(
        subprocess.check_output(
            [
                "ffprobe", "-v", "error",
                "-show_entries", "stream=codec_type,duration",
                "-of", "json", str(final_tmp),
            ],
            text=True,
        )
    )
    v_dur = a_dur = None
    for s in streams["streams"]:
        if s["codec_type"] == "video":
            v_dur = float(s.get("duration") or 0)
        if s["codec_type"] == "audio":
            a_dur = float(s.get("duration") or 0)
    assert v_dur and a_dur
    delta = a_dur - v_dur
    print(f"PRE_SYNC v={v_dur:.6f} a={a_dur:.6f} delta={delta:.6f}", flush=True)
    synced = work / "full_v03_sync.mp4"
    if abs(delta) <= 0.033:
        subprocess.run(["cp", "-f", str(final_tmp), str(synced)], check=True)
    elif delta > 0:
        # trim audio to video
        ff(
            "-i", str(final_tmp),
            "-filter_complex",
            f"[0:v]setpts=PTS-STARTPTS[v];[0:a]atrim=0:{v_dur:.6f},asetpts=PTS-STARTPTS[a]",
            "-map", "[v]", "-map", "[a]",
            "-t", f"{v_dur:.6f}",
            *ENC,
            str(synced),
        )
    else:
        # pad audio with silence
        pad = -delta
        ff(
            "-i", str(final_tmp),
            "-filter_complex",
            f"[0:v]setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration={pad:.6f}[v];"
            f"[0:a]apad=pad_dur={pad:.6f}[a]",
            "-map", "[v]", "-map", "[a]",
            "-t", f"{a_dur + pad:.6f}",
            *ENC,
            str(synced),
        )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["cp", "-f", str(synced), str(OUT)], check=True)

    # Final probe
    streams = json.loads(
        subprocess.check_output(
            [
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration:stream=codec_type,duration",
                "-of", "json", str(OUT),
            ],
            text=True,
        )
    )
    v_dur = a_dur = None
    for s in streams["streams"]:
        if s["codec_type"] == "video":
            v_dur = float(s.get("duration") or 0)
        if s["codec_type"] == "audio":
            a_dur = float(s.get("duration") or 0)
    dur = float(streams["format"]["duration"])
    delta = (a_dur or 0) - (v_dur or 0)
    digest = sha256(OUT)
    size = OUT.stat().st_size
    print(f"SAVED {OUT}", flush=True)
    print(f"SHA256 {digest}", flush=True)
    print(f"DUR {dur:.3f}", flush=True)
    print(f"SYNC_DELTA {delta:.6f}", flush=True)

    # Timeline bookkeeping
    # Segment starts after xfades
    starts: dict[str, float] = {}
    t = 0.0
    xfade_count = 0
    for i, s in enumerate(story_segs):
        starts[s["label"]] = t
        t += s["dur"]
        if i < len(story_segs) - 1:
            t -= XFADE
            xfade_count += 1
    hold_in = t  # after cream4, before hard concat... actually story already includes cream4
    # story duration:
    story_dur = probe_dur(story)
    hold_in = story_dur
    film_out = dur

    part_vo_seams = []
    for a, b, off in join_offsets:
        if a.startswith("p") and b.startswith("card"):
            part_vo_seams.append((f"{a}→{b}", off, "part→card"))
        elif a.startswith("card") and b.startswith("p"):
            part_vo_seams.append((f"{a}→{b}", off, "card→part"))
        elif a.startswith("p") and b.startswith("p"):
            part_vo_seams.append((f"{a}→{b}", off, "part→part"))

    # Card times + part picture times
    card_times = {k: starts[k] for k in starts if k.startswith("card")}
    part_times = {k: starts[k] for k in starts if k.startswith("p")}

    for lab, st in sorted(starts.items(), key=lambda x: x[1]):
        print(f"  START {lab} {st:.3f} ({fmt_tc(st)})", flush=True)

    # Extract audio for vo_check
    audio_wav = work / "full_v03_audio.wav"
    ff("-i", str(OUT), "-vn", "-ar", "48000", "-ac", "1", str(audio_wav))

    # iCloud
    ICLOUD_DIR.mkdir(parents=True, exist_ok=True)
    dest = ICLOUD_DIR / OUT.name
    for attempt in range(1, 5):
        try:
            tmp = ICLOUD_DIR / f"{OUT.name}.copying"
            subprocess.run(["cp", "-f", str(OUT), str(tmp)], check=True)
            tmp.replace(dest)
            break
        except OSError:
            if attempt == 4:
                raise
            time.sleep(2 * attempt)
    for attempt in range(1, 6):
        try:
            icloud_sha = sha256(dest)
            break
        except OSError:
            time.sleep(2 * attempt)
            icloud_sha = None
    print(f"ICLOUD {dest} sha={icloud_sha}", flush=True)

    meta = {
        "file": OUT.name,
        "sha256": digest,
        "duration": dur,
        "bytes": size,
        "xfade": XFADE,
        "card_hold": CARD_HOLD,
        "cream_after_vo": CREAM_AFTER_VO,
        "end_hold_s": END_HOLD,
        "p01_bridge_cut": P01_BRIDGE_CUT,
        "p05_cream_removed_from": P05_CREAM_WAS,
        "starts": starts,
        "card_times": card_times,
        "part_times": part_times,
        "join_offsets": [
            {"a": a, "b": b, "offset": off} for a, b, off in join_offsets
        ],
        "hold_in": hold_in,
        "video_duration": v_dur,
        "audio_duration": a_dur,
        "sync_delta_a_minus_v": delta,
        "seam_vo_mode": SEAM_VO_MODE,
        "status": "UAT_FOR_BEN",
        "keep_locked_label": False,
        "upload": False,
        "parents": PARENTS,
        "audio_wav_for_vo_check": str(audio_wav),
    }
    META.write_text(json.dumps(meta, indent=2) + "\n")
    (work / "META_PATH.txt").write_text(str(META) + "\n" + str(audio_wav) + "\n")

    watch = (
        "WATCH THIS FILE (HOS 004 full join v03 — mix restore):\n"
        f"  {OUT.name}\n"
        f"  iCloud: HOS UAT/004_Whats-Really-Inside-An-Atom/09_Final-Export/{OUT.name}\n\n"
        f"sha256={digest}\n"
        f"duration={dur:.3f}\n"
        f"sync_delta={delta:.6f}\n"
        "Chapter cards kept (real titles). Per-part TEMP beds. No J-cut.\n"
        "Cream AFTER last VO word (4s) then 20s Studio hold.\n"
        "Do NOT label KEEP/LOCKED. STOP for Ben — watch whole film continuous.\n"
    )
    WATCH.write_text(watch)
    (ICLOUD_DIR / WATCH.name).write_text(watch)

    print(f"AUDIO_FOR_VO_CHECK {audio_wav}", flush=True)
    print("DONE_BUILD", flush=True)


if __name__ == "__main__":
    main()
