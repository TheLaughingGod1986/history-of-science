#!/usr/bin/env python3
"""HOS 008 Short s04: Why Did Franklin Never Patent the Lightning Rod? (J3763, £0).

Test B search-titled Short cut from the locked HOS 008 long
('Benjamin Franklin's Kite Experiment Explained', YqCWYlv_LCY):
  - Existing locked VO only (Part 05 v01b 60.12-74.88 s, atempo 1.00, 0 credits)
  - Existing approved 3D cartoon Veo plates only (full-bleed 9:16 952x1692 @ 2.35x)
  - Ben 19 Nov 2026 Shorts house rules: 16.08 s (16-19 s band), 3D cartoon moving
    frame 0 (14_safe_towers_t1), concrete-fact hook caption on frame 0, seamless
    loop pre-roll ending on exact frame 0
  - WHO person card (Benjamin Franklin, 1706-1790 · Printer & inventor) in 16:9
    centre band clear of 0-2 s and 9-14 s title; captions throughout with soft
    translucent backing (Ben 5 Nov note)
  - Own 008 score bed slice (lightning008_score_bed_v02.mp3) + house SFX kit_v01
  - Runs sfx_kit.py level, polish_gate.py, picture_qa.py, music_gate.py, and
    gate_shorts_open.py check.

Usage:
    python3 _build_short_s04_no_patent_v01.py [--work-dir <dir>] [--out-dir <dir>] [--qa-dir <dir>]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
SHARED_HOS = Path("/Users/benjaminoats/YouTube/History Of Science")
SHARED_PROJ = SHARED_HOS / "02_Video-Projects/008_Lightning-Franklin"
NAS_PROJ = Path("/Volumes/data/studio-live/History Of Science/02_Video-Projects/008_Lightning-Franklin")
MEDIA = Path("/Users/benjaminoats/YouTube/hos-008-lightning/02_Video-Projects/008_Lightning-Franklin")
OWB = Path("/Users/benjaminoats/YouTube/orbit-with-ben")

VO_SRC = SHARED_PROJ / "02_Voiceover/hos_008_part05_the_rod_on_every_roof_v01b.mp3"
VO_SRC_SHA = "e5e86140d0b7e5598eb8eeca39d0f260c2dcc9b698b36c119a8c51283c990c38"
STT_SRC = SHARED_PROJ / "02_Voiceover/stt/hos_008_part05_the_rod_on_every_roof_v01b/stt_raw.json"
BED_SRC = SHARED_PROJ / "05_Music/lightning008_score_bed_v02.mp3"
BED_OFFSET_S = 320.0

VO_IN_S = 60.12
VO_OUT_S = 74.88
TOTAL = 16.08
LOOP_S = 1.20
FRAME0_IN = 1.20  # Beat 7 plays 0.00..1.20 s so final frame matches frame 0 at 1.20 s

SID = "s04_no_patent"
VER = "v01"
STEM = f"hos_008_{SID}_{VER}"

# 720p plates cannot fill 1080x1920 inside the 2.35x upscale limit (1920/720 = 2.67).
# Largest even 9:16 at 2.35x is 952x1692 (1280x720 -> 3008x1692 -> crop 952x1692).
W, H, FPS = 952, 1692, 30
UPSCALE = 2.35
BAND_H = W * 9 // 16  # 535 px
BAND_TOP = (H - BAND_H) // 2  # 578 px

CREAM = (245, 232, 210, 255)
INK = (24, 20, 20, 255)
YEL = (255, 214, 70, 255)
PANEL_BG = (24, 20, 18, 162)
FONT = "/System/Library/Fonts/Supplemental/Didot.ttc"

YT_TITLE = "Why Did Franklin Never Patent the Lightning Rod?"
YT_TITLE_ALT = "Who Invented the Lightning Rod? (And Gave It Away)"
LONG_TITLE = "Benjamin Franklin's Kite Experiment Explained"
LONG_VIDEO_ID = "YqCWYlv_LCY"

HOOK_LINES = [
    "Franklin **never**",
    "patented his",
    "lightning rod.",
]
HOOK_OUT = 2.36
CARD_IN, CARD_OUT, CARD_FADE = 2.45, 5.25, 0.35
TITLE_IN, TITLE_OUT = 9.00, 13.80

PLATES = {
    "safe_towers": MEDIA / "04_Generated-Clips/part05/raw/v01/14_safe_towers_t1.mp4",
    "no_patent": MEDIA / "04_Generated-Clips/part05/raw/v01/12_no_patent_t1.mp4",
    "rod_fitting": MEDIA / "04_Generated-Clips/part05/raw/v01/06_rod_fitting_t1.mp4",
    "rods_spread": MEDIA / "04_Generated-Clips/part05/j2241/13_rods_spread_j2241_t2.mp4",
    "roofs_golden": MEDIA / "04_Generated-Clips/part05/raw/v01/21_roofs_golden_t1.mp4",
    "rod_closeup": MEDIA / "04_Generated-Clips/part05/raw/v01/18_rod_closeup_t1.mp4",
}

# (t0, plate_key, source_in_s, crop_x)
# Every beat hold <= 2.96 s; first cut at 2.36 s (<= 3.0 s); WHO card stays 100% over Franklin (2.45-5.25 s);
# beat 7 loops 0.00->1.20 s into frame 0 at 1.20 s.
BEATS = [
    (0.00, "safe_towers", FRAME0_IN, 1028),
    (2.36, "no_patent", 1.40, 1450),
    (5.30, "rod_fitting", 0.50, 1028),
    (7.70, "rods_spread", 0.60, 1028),
    (10.60, "roofs_golden", 0.60, 1028),
    (13.56, "rod_closeup", 0.60, 1028),
    (14.88, "safe_towers", FRAME0_IN - LOOP_S, 1028),
]


def ff(*args: str, cwd: Path | None = None) -> None:
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *args], check=True, cwd=cwd)


def probe(path: Path) -> float:
    return float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        text=True,
    ).strip())


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_words() -> list[dict]:
    raw = json.loads(STT_SRC.read_text())["words"]
    out = []
    for w in raw:
        txt = (w.get("text") or "").strip()
        if not txt:
            continue
        s, e = float(w["start"]), float(w["end"])
        if s >= VO_IN_S - 0.02 and e <= VO_OUT_S + 0.02:
            out.append({
                "word": txt,
                "start": round(max(0.0, s - VO_IN_S), 3),
                "end": round(max(0.0, e - VO_IN_S), 3),
            })
    return out


def chunk_words(ws: list[dict]) -> list[dict]:
    """Group spoken words after 2.0 s into tight, readable phone captions."""
    hot_words = {"everyone", "churches,", "houses,", "masts,", "safer", "never", "patented"}
    chunks, i, n = [], 0, len(ws)
    while i < n:
        t0 = ws[i]["start"]
        parts, t_end, j = [ws[i]["word"]], ws[i]["end"], i + 1
        while j < n:
            wj, sj, ej = ws[j]["word"], ws[j]["start"], ws[j]["end"]
            if parts[-1][-1:] in ".?!":
                break
            if parts[-1][-1:] in ",;:" and sj - t0 >= 0.40 and len(parts) >= 2:
                break
            if len(parts) >= 5 and sj - t0 >= 0.40:
                break
            if ej - t0 >= 1.45 and len(parts) >= 2:
                break
            parts.append(wj)
            t_end = ej
            j += 1
        t1 = ws[j]["start"] if j < n else t_end + 0.22
        # Skip sentence-1 chunks already spoken under the 0.00-2.36 s frame-0 hook caption
        if t_end <= HOOK_OUT + 0.05:
            i = j
            continue
        t0_show = max(t0, HOOK_OUT)
        if t1 > t0_show + 0.12:
            styled = [f"**{p}**" if p.lower() in hot_words else p for p in parts]
            chunks.append({
                "text": " ".join(parts),
                "styled": " ".join(styled),
                "t0": round(t0_show, 3),
                "t1": round(min(t1, TOTAL - 0.10), 3),
            })
        i = j
    return chunks


def _draw_styled_lines(
    draw: ImageDraw.ImageDraw,
    lines: list[list[tuple[str, bool]]],
    font: ImageFont.FreeTypeFont,
    y_top: int,
    *,
    stroke: int = 4,
    pad_x: int = 28,
    pad_y: int = 16,
    radius: int = 18,
    bg: tuple[int, int, int, int] | None = PANEL_BG,
) -> tuple[int, int, int, int]:
    asc, desc = font.getmetrics()
    lh = asc + desc
    gap = int(font.size * 0.16)
    space = font.getlength(" ")
    widths = [font.getlength(" ".join(t for t, _ in line)) for line in lines]
    max_w = max(widths)
    block_h = lh * len(lines) + gap * (len(lines) - 1)
    x0 = int((W - max_w) / 2 - pad_x)
    y0 = int(y_top - pad_y)
    x1 = int((W + max_w) / 2 + pad_x)
    y1 = int(y_top + block_h + pad_y)
    if bg is not None:
        draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=bg)
    cy = y_top
    for line, lw in zip(lines, widths):
        x = (W - lw) / 2
        for tok, hot in line:
            draw.text(
                (x, cy), tok, font=font,
                fill=YEL if hot else CREAM,
                stroke_width=stroke, stroke_fill=INK,
            )
            x += font.getlength(tok) + space
        cy += lh + gap
    return (x0, y0, x1, y1)


def render_hook(path: Path) -> dict:
    """Frame-0 concrete-fact caption (Ben 19 Nov 2026 rule 4), no rectangular box (avoids split-panel seam)."""
    size = 104
    font = ImageFont.truetype(FONT, size, index=2)  # Didot Bold
    parsed_lines = [[(w.strip("*"), w.startswith("**")) for w in ln.split()] for ln in HOOK_LINES]
    while max(font.getlength(" ".join(t for t, _ in ln)) for ln in parsed_lines) > W - 96 and size > 64:
        size -= 2
        font = ImageFont.truetype(FONT, size, index=2)
    cap = -font.getbbox("H", anchor="ls")[1]
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Place inside 0.15..0.44 H (hook band checked by gate_shorts_open.py), no horizontal box edge
    y_top = int(H * 0.17)
    box = _draw_styled_lines(draw, parsed_lines, font, y_top, stroke=8, pad_x=0, pad_y=0, radius=0, bg=None)
    img.save(path)
    return {
        "lines": [ln.replace("**", "") for ln in HOOK_LINES],
        "font_size": size,
        "cap_px": cap,
        "cap_pct": round(100 * cap / H, 2),
        "box_pct_y": [round(100 * box[1] / H, 1), round(100 * box[3] / H, 1)],
    }


def render_caption(path: Path, styled_text: str) -> None:
    size = 58
    font = ImageFont.truetype(FONT, size, index=2)  # Didot Bold for crisp phone legibility
    tokens = [(w.strip("*"), w.startswith("**")) for w in styled_text.split()]
    lines, cur = [], []
    for tok in tokens:
        trial = " ".join(t for t, _ in cur + [tok])
        if cur and font.getlength(trial) > W - 128:
            lines.append(cur)
            cur = [tok]
        else:
            cur.append(tok)
    lines.append(cur)
    asc, desc = font.getmetrics()
    lh = asc + desc
    gap = int(size * 0.16)
    block_h = lh * len(lines) + gap * (len(lines) - 1)
    y_top = H - 330 - block_h  # safely above YouTube Shorts bottom UI
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    _draw_styled_lines(draw, lines, font, y_top, stroke=5, pad_x=28, pad_y=14, radius=18, bg=(20, 16, 14, 185))
    img.save(path)


def render_who_card(path: Path) -> dict:
    """WHO person card inside 16:9 centre band, clear of 0-2 s and 9-14 s title."""
    f_name = ImageFont.truetype(FONT, 62, index=2)  # Didot Bold
    f_role = ImageFont.truetype(FONT, 42, index=1)  # Didot Italic
    line1 = "Benjamin Franklin"
    years = "1706–1790"
    role = " · Printer & inventor"
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    w1 = f_name.getlength(line1)
    w2 = f_role.getlength(years + role)
    max_w = max(w1, w2)
    asc1, desc1 = f_name.getmetrics()
    asc2, desc2 = f_role.getmetrics()
    h1, h2 = asc1 + desc1, asc2 + desc2
    gap = 10
    total_h = h1 + gap + h2
    # Inside lower third of 16:9 centre band (BAND_TOP=578 .. BAND_TOP+BAND_H=1113)
    y_top = BAND_TOP + BAND_H - total_h - 32
    pad_x, pad_y = 32, 18
    x0 = int((W - max_w) / 2 - pad_x)
    y0 = int(y_top - pad_y)
    x1 = int((W + max_w) / 2 + pad_x)
    y1 = int(y_top + total_h + pad_y)
    draw.rounded_rectangle([x0, y0, x1, y1], radius=20, fill=(28, 22, 18, 175))
    draw.text(((W - w1) / 2, y_top), line1, font=f_name, fill=CREAM, stroke_width=4, stroke_fill=INK)
    x2 = (W - w2) / 2
    y2 = y_top + h1 + gap
    draw.text((x2, y2), years, font=f_role, fill=YEL, stroke_width=3, stroke_fill=INK)
    draw.text((x2 + f_role.getlength(years), y2), role, font=f_role, fill=CREAM, stroke_width=3, stroke_fill=INK)
    img.save(path)
    return {
        "kind": "WHO",
        "line1": line1,
        "line2": f"{years}{role}",
        "in_s": CARD_IN,
        "out_s": CARD_OUT,
        "fade_s": CARD_FADE,
        "box_y_px": [y0, y1],
        "band_y_px": [BAND_TOP, BAND_TOP + BAND_H],
    }


def render_long_title(path: Path) -> dict:
    """Exact live title of promoted long YqCWYlv_LCY at 9.0-13.8 s, upper safe band."""
    f_kicker = ImageFont.truetype(FONT, 30, index=1)
    size = 46
    f_title = ImageFont.truetype(FONT, size, index=2)
    tokens = [(w, w in ("Franklin's", "Kite")) for w in LONG_TITLE.split()]
    lines, cur = [], []
    for tok in tokens:
        trial = " ".join(t for t, _ in cur + [tok])
        if cur and f_title.getlength(trial) > W - 150:
            lines.append(cur)
            cur = [tok]
        else:
            cur.append(tok)
    lines.append(cur)
    asc_k, desc_k = f_kicker.getmetrics()
    kh = asc_k + desc_k
    asc_t, desc_t = f_title.getmetrics()
    th = asc_t + desc_t
    gap = 8
    block_h = kh + 8 + th * len(lines) + gap * (len(lines) - 1)
    kicker = "Full film"
    widths = [f_title.getlength(" ".join(t for t, _ in ln)) for ln in lines]
    max_w = max(max(widths), f_kicker.getlength(kicker))
    y_top = 210
    pad_x, pad_y = 28, 16
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    x0 = int((W - max_w) / 2 - pad_x)
    y0 = int(y_top - pad_y)
    x1 = int((W + max_w) / 2 + pad_x)
    y1 = int(y_top + block_h + pad_y)
    draw.rounded_rectangle([x0, y0, x1, y1], radius=18, fill=(24, 20, 18, 168))
    draw.text(((W - f_kicker.getlength(kicker)) / 2, y_top), kicker, font=f_kicker, fill=YEL, stroke_width=2, stroke_fill=INK)
    cy = y_top + kh + 8
    space = f_title.getlength(" ")
    for ln, lw in zip(lines, widths):
        x = (W - lw) / 2
        for tok, hot in ln:
            draw.text((x, cy), tok, font=f_title, fill=YEL if hot else CREAM, stroke_width=4, stroke_fill=INK)
            x += f_title.getlength(tok) + space
        cy += th + gap
    img.save(path)
    return {
        "title": LONG_TITLE,
        "video_id": LONG_VIDEO_ID,
        "in_s": TITLE_IN,
        "out_s": TITLE_OUT,
        "box_y_px": [y0, y1],
    }


def make_seg(src: Path, dst: Path, start: float, dur: float, crop_x: int) -> None:
    src_dur = probe(src)
    if start < 0 or start + dur > src_dur + 0.03:
        raise SystemExit(f"{src.name}: in {start} + {dur:.2f}s exceeds {src_dur:.2f}s")
    vf = f"scale=3008:1692:flags=lanczos,crop={W}:{H}:{crop_x}:0,setsar=1,fps={FPS}"
    ff(
        "-i", str(src), "-ss", f"{start:.3f}", "-t", f"{dur:.3f}",
        "-vf", vf, "-an",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "18",
        str(dst),
    )


def place_sfx(work: Path, total: float) -> Path:
    kit = SHARED_PROJ / "06_Sound-Effects/kit_v01"
    whoosh = kit / "sfx_hos_whoosh_soft_v01.wav"
    rumble = kit / "sfx_hos_rumble_low_v01.wav"
    tick = kit / "sfx_hos_tick_ink_v01.wav"
    dst = work / "sfx_raw.wav"
    d_card = int(CARD_IN * 1000)
    d_title = int(TITLE_IN * 1000)
    ff(
        "-f", "lavfi", "-t", f"{total:.3f}", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
        "-i", str(whoosh),
        "-i", str(rumble),
        "-i", str(tick),
        "-i", str(tick),
        "-filter_complex",
        "[1:a]volume=-15dB,afade=t=out:st=0.45:d=0.25[w];"
        "[2:a]atrim=0:1.6,volume=-18dB,afade=t=in:d=0.05,afade=t=out:st=1.0:d=0.6[r];"
        f"[3:a]volume=-10dB,adelay={d_card}|{d_card}[t1];"
        f"[4:a]volume=-11dB,adelay={d_title}|{d_title}[t2];"
        "[0:a][w][r][t1][t2]amix=inputs=5:normalize=0:duration=first,alimiter=limit=0.5[a]",
        "-map", "[a]", "-c:a", "pcm_s16le", str(dst),
    )
    return dst


def ebur128(path: Path) -> tuple[float, float]:
    err = subprocess.run(
        ["ffmpeg", "-nostats", "-hide_banner", "-i", str(path), "-af", "ebur128=peak=true", "-f", "null", "-"],
        capture_output=True, text=True, check=True,
    ).stderr
    i_lines = [ln for ln in err.splitlines() if ln.strip().startswith("I:") and "LUFS" in ln]
    p_lines = [ln for ln in err.splitlines() if ln.strip().startswith("Peak:") and "dBFS" in ln]
    if not i_lines or not p_lines:
        raise SystemExit(f"ebur128 failed on {path.name}")
    lufs = float(i_lines[-1].split("I:")[1].split("LUFS")[0].strip())
    peak = float(p_lines[-1].split("Peak:")[1].split("dBFS")[0].strip())
    return lufs, peak


def level_master(mp4: Path) -> dict:
    tmp = mp4.with_suffix(".leveled.mp4")
    target, tp = -12.0, -2.0
    lufs, peak = 0.0, 0.0
    for _ in range(4):
        ff(
            "-i", str(mp4), "-c:v", "copy",
            "-af", f"loudnorm=I={target:.1f}:TP={tp:.1f}:LRA=11",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
            "-movflags", "+faststart", str(tmp),
        )
        lufs, peak = ebur128(tmp)
        if -14.5 <= lufs <= -13.5 and peak <= -1.6:
            break
        target += (-14.0 - lufs)
        if peak > -1.6:
            tp -= 0.4
    if not (-14.5 <= lufs <= -13.5) or peak > -1.6:
        tmp.unlink(missing_ok=True)
        raise SystemExit(f"level landed at {lufs:.2f} LUFS / {peak:.2f} dBTP")
    tmp.replace(mp4)
    return {"lufs": round(lufs, 2), "true_peak_dbtp": round(peak, 2), "loudnorm_I": round(target, 2)}


def make_full_sheet(mp4: Path, out: Path) -> None:
    dur = probe(mp4)
    times = [0.0, 0.5, 1.5, 2.6, 3.8, 5.2, 6.8, 8.2, 9.6, 11.2, 12.6, 14.0, 15.0, round(dur - 0.06, 2)]
    tw, th = 190, 338
    cols = 7
    rows = (len(times) + cols - 1) // cols
    sheet = Image.new("RGB", (tw * cols, th * rows), (18, 18, 22))
    draw = ImageDraw.Draw(sheet)
    tmp = out.parent / "_sheet_tmp.jpg"
    for idx, t in enumerate(times):
        ff("-ss", f"{t:.2f}", "-i", str(mp4), "-frames:v", "1", "-vf", f"scale={tw}:{th}", str(tmp))
        r, c = divmod(idx, cols)
        sheet.paste(Image.open(tmp), (c * tw, r * th))
        draw.rectangle([c * tw + 2, r * th + 2, c * tw + 82, r * th + 22], fill=(0, 0, 0))
        draw.text((c * tw + 6, r * th + 5), f"t={t:.2f}s", fill=(255, 220, 80))
    tmp.unlink(missing_ok=True)
    sheet.save(out, quality=88)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--work-dir", type=Path, default=Path("/Volumes/data/mac-mini-archive/mini-tmp-scratch/J3763_work"))
    ap.add_argument("--out-dir", type=Path, default=NAS_PROJ / "10_Shorts/J3763")
    ap.add_argument("--qa-dir", type=Path, default=HERE / f"qa_{SID}_{VER}")
    ap.add_argument("--music-dir", type=Path, default=SHARED_PROJ / "05_Music")
    ap.add_argument("--air-date", default="2026-12-01")
    ns = ap.parse_args()

    work, out_dir, qa_dir = ns.work_dir, ns.out_dir, ns.qa_dir
    work.mkdir(parents=True, exist_ok=True)
    out_dir.mkdir(parents=True, exist_ok=True)
    qa_dir.mkdir(parents=True, exist_ok=True)

    if sha256(VO_SRC) != VO_SRC_SHA:
        raise SystemExit("locked Part 05 VO hash mismatch; refusing to continue")
    for k, p in PLATES.items():
        if not p.is_file():
            raise SystemExit(f"missing plate {k}: {p}")

    ws = load_words()
    if not ws:
        raise SystemExit("no STT words found in VO slice")
    spoken = " ".join(w["word"] for w in ws)
    (work / "spoken.txt").write_text(spoken + "\n")

    # 1. Extract untouched locked VO slice (atempo = 1.00)
    vo_wav = work / f"{STEM}_vo.wav"
    vo_dur = round(VO_OUT_S - VO_IN_S, 3)
    ff(
        "-ss", f"{VO_IN_S:.3f}", "-t", f"{vo_dur:.3f}", "-i", str(VO_SRC),
        "-af", f"aformat=sample_rates=48000:channel_layouts=stereo,afade=t=in:d=0.015,afade=t=out:st={vo_dur - 0.025:.3f}:d=0.025",
        "-c:a", "pcm_s16le", str(vo_wav),
    )

    # 2. Slice 008's own score bed (0 credits, distinct offset from Short C)
    bed_wav = out_dir / f"{STEM}_bed.wav"
    ff(
        "-ss", f"{BED_OFFSET_S:.3f}", "-t", f"{TOTAL + 0.5:.3f}", "-i", str(BED_SRC),
        "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(bed_wav),
    )
    bed_plan = {
        "created_at": "2026-11-26T00:55:00+00:00",
        "project": STEM,
        "generate": False,
        "audio_file": bed_wav.name,
        "source_take": "lightning008_score_bed_v02.mp3",
        "note": f"{TOTAL:.2f} s slice of HOS 008's own v02 score bed from {BED_OFFSET_S:.0f} s. No new ElevenLabs take. £0.",
        "prompt": (
            "HOS 008 Short s04 (no patent), a slice of the film's own lightning bed. Soft gut-string quartet, "
            "a quiet baroque pulse, and one wooden flute, under a spoken account of Franklin giving the lightning rod "
            "away without a patent. Leave room for a spoken voice. No vocals. Pace: 64-72 BPM. NOT the 007 vaccine "
            "wooden-harp bed, NOT the Trees of Air bed, NOT Orbit cosmic pads, Betelgeuse, Saturn, Sun, Venus, "
            "Light Speed, Mars or the nearest-star bed; no drums, no EDM, no cartoon sting, no menace drone."
        ),
    }
    bed_wav.with_name(f"{STEM}_bed_plan.json").write_text(json.dumps(bed_plan, indent=2) + "\n")
    # Also write plan next to 05_Music for music_gate.py
    ns.music_dir.mkdir(parents=True, exist_ok=True)
    music_bed_copy = ns.music_dir / f"{STEM}_bed.wav"
    ff("-i", str(bed_wav), "-c:a", "copy", str(music_bed_copy))
    (ns.music_dir / f"{STEM}_bed_plan.json").write_text(json.dumps(bed_plan, indent=2) + "\n")

    # 3. Cut full-bleed 9:16 video segments
    segs, plan = [], []
    for idx, (t0, key, inn, cx) in enumerate(BEATS):
        t1 = BEATS[idx + 1][0] if idx + 1 < len(BEATS) else TOTAL
        dur = round(t1 - t0, 3)
        if idx == 0 and t1 > 3.0:
            raise SystemExit(f"first cut {t1}s > 3.0s")
        if dur > 4.0:
            raise SystemExit(f"beat {idx} hold {dur}s > 4.0s")
        dst = work / f"seg_{idx:02d}.mp4"
        make_seg(PLATES[key], dst, inn, dur, cx)
        segs.append(dst)
        plan.append({
            "t0": t0, "t1": t1, "plate": PLATES[key].name,
            "plate_sha256": sha256(PLATES[key]),
            "in_s": inn, "crop_x": cx, "hold_s": dur,
            "lands_on": "loop" if idx == len(BEATS) - 1 else "plate",
            "upscale": UPSCALE,
        })
    (work / "pic.txt").write_text("".join(f"file '{s.name}'\n" for s in segs))
    pic = work / "picture.mp4"
    ff(
        "-f", "concat", "-safe", "0", "-i", "pic.txt",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "18",
        "-r", str(FPS), "-t", f"{TOTAL:.3f}", str(pic), cwd=work,
    )

    # 4. Audio mix + sfx_kit.py level gate
    sfx_raw = place_sfx(work, TOTAL)
    audio_mix = work / "audio_mix.wav"
    bed_db, sfx_db, sfx_level = -18.0, -14.0, {}
    for _ in range(6):
        ff(
            "-i", str(vo_wav), "-i", str(bed_wav), "-i", str(sfx_raw),
            "-filter_complex",
            f"[0:a]aformat=sample_rates=48000:channel_layouts=stereo,apad=whole_dur={TOTAL:.3f}[v];"
            f"[1:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{TOTAL:.3f},asetpts=PTS-STARTPTS,"
            f"volume={bed_db:.2f}dB,afade=t=in:d=0.05,afade=t=out:st={TOTAL - 0.25:.3f}:d=0.25[b];"
            f"[2:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{TOTAL:.3f},volume={sfx_db:.2f}dB[s];"
            "[v][b][s]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.89[a]",
            "-map", "[a]", "-t", f"{TOTAL:.3f}", "-c:a", "pcm_s16le", str(audio_mix),
        )
        stems = {}
        for name, src, extra in (
            ("vo", vo_wav, f"apad=whole_dur={TOTAL:.3f}"),
            ("bed", bed_wav, f"volume={bed_db:.2f}dB,atrim=0:{TOTAL:.3f}"),
            ("sfx", sfx_raw, f"volume={sfx_db:.2f}dB,atrim=0:{TOTAL:.3f}"),
        ):
            stems[name] = work / f"stem_{name}.wav"
            ff("-i", str(src), "-af", extra, "-t", f"{TOTAL:.3f}", "-c:a", "pcm_s16le", str(stems[name]))
        r = subprocess.run(
            [
                sys.executable, str(OWB / "scripts/sfx_kit.py"), "level",
                "--vo", str(stems["vo"]), "--sfx", str(stems["sfx"]), "--bed", str(stems["bed"]),
                "--minutes", f"{TOTAL / 60:.3f}",
            ],
            capture_output=True, text=True,
        )
        sfx_level = {"exit": r.returncode, "output": (r.stdout + r.stderr).strip(), "bed_db": bed_db, "sfx_db": sfx_db}
        if r.returncode == 0:
            break
        bed_db -= 3.0
        sfx_db -= 3.0
    if sfx_level["exit"] != 0:
        raise SystemExit(f"sfx_kit.py level failed: {sfx_level['output']}")

    # 5. Render overlays (hook caption, captions throughout, WHO card, exact live long title)
    chunks = chunk_words(ws)
    overlays = []
    hook_png = work / "cap_hook.png"
    hook_meta = render_hook(hook_png)
    overlays.append((hook_png, 0.00, HOOK_OUT, "hook", " ".join(hook_meta["lines"])))
    for i, c in enumerate(chunks):
        png = work / f"cap_{i:03d}.png"
        render_caption(png, c["styled"])
        overlays.append((png, c["t0"], c["t1"], "vo", c["text"]))
    title_png = work / "cap_title.png"
    title_meta = render_long_title(title_png)
    overlays.append((title_png, TITLE_IN, TITLE_OUT, "title", LONG_TITLE))
    card_png = work / "card_who.png"
    card_meta = render_who_card(card_png)

    # 6. Composite + encode + loudness level
    inputs = ["-i", str(pic), "-i", str(audio_mix)]
    for png, *_ in overlays:
        inputs += ["-loop", "1", "-i", str(png)]
    ci = 2 + len(overlays)
    inputs += ["-loop", "1", "-t", f"{TOTAL:.3f}", "-i", str(card_png)]
    fc, last = [], "[0:v]"
    fc.append(
        f"[{ci}:v]format=rgba,fade=t=in:st={CARD_IN:.3f}:d={CARD_FADE:.3f}:alpha=1,"
        f"fade=t=out:st={CARD_OUT - CARD_FADE:.3f}:d={CARD_FADE:.3f}:alpha=1[card]"
    )
    fc.append(f"{last}[card]overlay=0:0:enable='gte(t,{CARD_IN:.3f})*lt(t,{CARD_OUT:.3f})'[vc]")
    last = "[vc]"
    for i, (_, t0, t1, *_r) in enumerate(overlays, 2):
        fc.append(f"{last}[{i}:v]overlay=0:0:enable='gte(t,{t0:.3f})*lt(t,{t1:.3f})'[v{i}]")
        last = f"[v{i}]"

    mp4 = out_dir / f"{STEM}.mp4"
    ff(
        *inputs, "-filter_complex", ";".join(fc),
        "-map", last, "-map", "1:a",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-profile:v", "high",
        "-preset", "veryfast", "-crf", "18", "-r", str(FPS),
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
        "-t", f"{TOTAL:.3f}", "-movflags", "+faststart", str(mp4),
    )
    level = level_master(mp4)

    # Sidecar meta + words files beside master AND in repo 10_Shorts
    words_payload = {"words": ws}
    meta_payload = {
        "film": "008",
        "short_id": SID,
        "version": VER,
        "file": str(mp4),
        "sha256": sha256(mp4),
        "duration_s": round(probe(mp4), 3),
        "youtube_title_draft": YT_TITLE,
        "youtube_title_alt": YT_TITLE_ALT,
        "promotes": "008",
        "promotes_video_id": LONG_VIDEO_ID,
        "title_on_screen": LONG_TITLE,
        "spoken": spoken,
        "vo_source": f"02_Voiceover/{VO_SRC.name} ({VO_IN_S:.2f}-{VO_OUT_S:.2f} s, atempo 1.00)",
        "vo_src_sha256": VO_SRC_SHA,
        "words_count": len(ws),
        "first_word_s": ws[0]["start"],
        "last_word_end_s": ws[-1]["end"],
        "tail_gap_s": round(TOTAL - ws[-1]["end"], 3),
        "loop_sentence": "…and one by one, church towers became safer places to stand. Franklin never patented his lightning rod.",
        "hook": hook_meta,
        "card": card_meta,
        "title_overlay": title_meta,
        "captions": ws,
        "level": level,
        "sfx_level": sfx_level,
        "bed_source": f"05_Music/{BED_SRC.name} (offset {BED_OFFSET_S:.0f} s)",
        "plan": plan,
        "upscale": UPSCALE,
        "spend_gbp": 0,
        "spend_credits": 0,
    }
    (out_dir / f"{STEM}_words.json").write_text(json.dumps(words_payload, indent=2) + "\n")
    (out_dir / f"{STEM}_meta.json").write_text(json.dumps(meta_payload, indent=2) + "\n")

    # 7. Run all gates
    cuts, pool, seen = [], [], set()
    for k, row in enumerate(plan, 1):
        src_name = f"loop_{row['plate']}" if row["lands_on"] == "loop" else row["plate"]
        cuts.append({
            "row": f"s{k:02d}",
            "timeline_in": row["t0"],
            "timeline_out": row["t1"],
            "source": src_name,
            "upscale": row["upscale"],
            "video": True,
            "framing": {"offset": row["in_s"], "crop_x": row["crop_x"]},
        })
        if src_name not in seen:
            seen.add(src_name)
            pool.append({"file_id": src_name, "title": f"Approved HOS 008 3D cartoon plate {row['plate']}"})

    cuts_f, pool_f = qa_dir / "cuts.json", qa_dir / "pool.json"
    cuts_f.write_text(json.dumps(cuts, indent=2) + "\n")
    pool_f.write_text(json.dumps(pool, indent=2) + "\n")
    (qa_dir / "sfx.txt").write_text(sfx_level["output"] + "\n")

    gates_out = {"sfx": {"exit": sfx_level["exit"], "tail": sfx_level["output"][-1500:]}}
    gate_cmds = [
        ("polish", [sys.executable, str(OWB / "scripts/polish_gate.py"), str(mp4),
                    "--cuts", str(cuts_f), "--out", str(qa_dir / "polish_gate.json")]),
        ("picture", [sys.executable, str(OWB / "scripts/picture_qa.py"), str(mp4),
                     "--cuts", str(cuts_f), "--pool", str(pool_f), "--out-dir", str(qa_dir / "picture_qa")]),
        ("music", [sys.executable, str(OWB / "scripts/music_gate.py"), str(ns.music_dir.parent),
                   "--bed", str(music_bed_copy), "--video", str(mp4), "--out", str(qa_dir / "music_gate.json")]),
        ("open", [sys.executable, str(SHARED_HOS / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
                  "check", str(mp4), "--air-date", ns.air_date,
                  "--sheet-dir", str(qa_dir),
                  "--meta", str(out_dir / f"{STEM}_meta.json"),
                  "--script", str(work / "spoken.txt"),
                  "--vo", str(vo_wav)]),
    ]
    for name, cmd in gate_cmds:
        r = subprocess.run(cmd, capture_output=True, text=True)
        txt = (r.stdout + r.stderr).strip()
        (qa_dir / f"{name}.txt").write_text(txt + "\n")
        gates_out[name] = {"exit": r.returncode, "tail": txt[-1500:]}

    make_full_sheet(mp4, qa_dir / f"{STEM}_full_sheet.jpg")
    meta_payload["gates"] = gates_out
    (qa_dir / "BUILD.json").write_text(json.dumps(meta_payload, indent=2) + "\n")

    print(json.dumps({
        "file": str(mp4),
        "sha256": meta_payload["sha256"],
        "duration_s": meta_payload["duration_s"],
        "words_count": meta_payload["words_count"],
        "first_word_s": meta_payload["first_word_s"],
        "last_word_end_s": meta_payload["last_word_end_s"],
        "tail_gap_s": meta_payload["tail_gap_s"],
        "level": level,
        "gates": {k: v["exit"] for k, v in gates_out.items()},
    }, indent=2))
    for k, v in gates_out.items():
        print(f"\n=== GATE {k} (exit {v['exit']}) ===\n{v['tail']}")


if __name__ == "__main__":
    main()
