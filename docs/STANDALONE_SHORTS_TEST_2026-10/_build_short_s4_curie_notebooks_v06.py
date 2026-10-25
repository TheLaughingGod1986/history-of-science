#!/usr/bin/env python3
"""HOS standalone S4 v06 (J0934, £0 local re-cut of vEg_tLIm0Co).

Chief ruling 25 Oct 10:45 London. v05 is left untouched.

- The takes / "1,600" join is not cut. v05 deleted the source from the end of
  "takes" to the STT start of "1,600", and small.en heard "600". This version
  plays that source straight through from before 20.38 s.
- Frame 0 stays the moving Wurzburg lab plate. Curie stills sit on the lines
  Chief named, each between moving plates. No frame-0 paste on the tail.
  The loop is that same plate ending on the frame before frame 0's in-point.
- Card: MARIE CURIE / Paris, 1898. Optional half-life card at the payoff.
- Holds <= 3.0 s. Master aimed at -14.0 LUFS, true peak <= -1.0 dBFS.

    python3 _build_short_s4_curie_notebooks_v06.py
    VO_ONLY=1 python3 _build_short_s4_curie_notebooks_v06.py
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import re
import shutil
import struct
import subprocess
import sys
import wave
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
OWB = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
NAS_CLIPS = Path("/Volumes/data/mac-mini-archive/YouTube/History Of Science/"
                 "02_Video-Projects/003_Invisible-Bones-X-Rays/04_Generated-Clips")
STILLS = HERE / "plates_v01/s4"
SID, VER, JOB = "s4_curie_notebooks", "v06", "J0934"
AIR, YT = "2026-10-28", "vEg_tLIm0Co"
RAW_VO = HERE / "vo_v01/hos_sa_s4_curie_notebooks_vo_v01.wav"
STT = HERE / "vo_v01/stt/hos_sa_s4_curie_notebooks_vo_v01/stt_raw.json"
WORK = HERE / f"_work_{SID}_{VER}"
QA = HERE / "qa_shorts_v01" / f"hos_sa_{SID}_{VER}"
MUSIC = HERE / "05_Music"
W, H, FPS = 1080, 1920, 30
LOOP_S = 1.0
# 5.72 s is a calm moment of the lab plate, so the frame before it
# sits within 5 luma of frame 0. The opening has to finish before the plate ends.
F0_IN = 5.72
FIRST_CUT_MAX = 2.47
PLATE_SAFE = 7.92
HOOK = "STILL **RADIOACTIVE**"
FONT = "/System/Library/Fonts/Supplemental/Didot.ttc"
CREAM, INK, YEL = (245, 232, 210, 255), (28, 26, 28, 255), (255, 214, 70, 255)
BAND_TOP, BAND_H = (H - 608) // 2, 608
# Chief: the sixteen-hundred speech is already in the source by 20.42 s.
SIXTEEN_SRC = 20.38
DB60 = -60.0
LEAD_S, TAIL_S = 0.020, 0.030

WURZ = "02_wurzburg_lab_establishing_v03.mp4"
GLOW = "part02/05_glow_blooms_v02.mp4"
BENCH = "08_rontgen_late_ots_v01.mp4"
DOOR_A = "part02/08_locks_the_door_v02.mp4"
DOOR_B = "part02/08_locks_the_door_v01.mp4"


def ff(*a: str, cwd: Path | None = None) -> None:
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *a], check=True, cwd=cwd)


def probe(p: Path) -> float:
    return float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)], text=True))


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def stt_words() -> list[dict]:
    d = json.loads(STT.read_text())
    return [w for w in d["words"] if w.get("type") == "word"]


def load_stereo() -> tuple[int, list[int]]:
    with wave.open(str(RAW_VO)) as w:
        sr = w.getframerate()
        ch = w.getnchannels()
        raw = w.readframes(w.getnframes())
    samples = list(memoryview(raw).cast("h"))
    if ch == 2:
        left = samples[0::2]
    else:
        left = samples
    return sr, left


SR, LEFT = load_stereo()


def rms_db(t: float) -> float:
    hop = SR // 100
    i0 = int(t * SR)
    if i0 < 0 or i0 + hop > len(LEFT):
        return -99.0
    acc = 0.0
    for i in range(i0, i0 + hop):
        v = LEFT[i] / 32768.0
        acc += v * v
    rms = math.sqrt(acc / hop)
    return -99.0 if rms <= 1e-9 else 20 * math.log10(rms)


def attack_in(a: float, b: float) -> tuple[float | None, float | None]:
    onset = offset = None
    t = round(max(0.0, a), 3)
    end = round(b, 3)
    while t < end - 0.009:
        if rms_db(t) > DB60:
            if onset is None:
                onset = t
            offset = round(t + 0.01, 3)
        t = round(t + 0.01, 3)
    return onset, offset


def sixteen_index(words: list[dict]) -> int:
    for i, w in enumerate(words):
        if "1600" in w["text"].replace(",", ""):
            return i
    raise SystemExit("no 1,600 word in the source STT")


def lifted_vo(work: Path) -> tuple[Path, list[tuple[str, float, float]], list[dict]]:
    """v05 gap squeeze, except takes and 1,600 play as one source span.

    v05 replaced the source between the STT end of "takes" and the STT start
    of "1,600" with 0.15 s of room. That span holds the start of "sixteen".
    """
    words = stt_words()
    idx = sixteen_index(words)
    pieces: list[tuple[float, float]] = []
    mapped: list[tuple[str, float, float]] = []
    log: list[dict] = []
    pre = 0.08
    lead = max(0.0, words[0]["start"] - pre)
    pieces.append((lead, words[0]["start"]))
    cursor = words[0]["start"] - lead

    for i, w in enumerate(words):
        if i == idx:
            pa, pb = pieces[-1]
            new_b = w["end"] + TAIL_S
            nxt = words[i + 1]["start"] if i + 1 < len(words) else new_b
            new_b = min(new_b, nxt - 0.012)
            if new_b <= pa + 0.05:
                raise SystemExit("merged sixteen span is empty")
            pieces[-1] = (pa, new_b)
            span_out0 = cursor - (pb - pa)
            cap0 = span_out0 + max(0.0, SIXTEEN_SRC + 0.04 - pa)
            if mapped and cap0 < mapped[-1][2] + 0.02:
                cap0 = mapped[-1][2] + 0.04
            cap1 = span_out0 + (w["end"] - pa)
            mapped.append((w["text"], round(cap0, 3), round(max(cap1, cap0 + 0.2), 3)))
            cursor += new_b - pb
            onset, offset = attack_in(pa, new_b)
            log.append({
                "word": w["text"], "merged_with_previous": True,
                "src": [round(pa, 3), round(new_b, 3)],
                "join_at_or_before": SIXTEEN_SRC,
                "onset_s": onset, "offset_s": offset,
                "cut_s": round(pa, 3), "end_s": round(new_b, 3),
                "lead_ms": None if onset is None else round((onset - pa) * 1000, 1),
                "tail_ms": None if offset is None else round((new_b - offset) * 1000, 1),
            })
            continue

        src_a, src_b = w["start"], w["end"]
        if i:
            prev_end = pieces[-1][1]
            full = w["start"] - prev_end
            # First six words stay tight so "still" lands by 1.5 s. A 20 ms
            # source lead on later words is taken out of the gap, not added on.
            lead = LEAD_S if (i > 5 and full > 0.08) else 0.0
            src_a = max(prev_end, w["start"] - lead)
            if i <= 4:
                # Gaps before "still". 0.02 left it at 1.52 s; 0.008 lands it by 1.50.
                gap = 0.008 if full > 0.008 else max(0.0, full)
            elif i == 5:
                gap = 0.02 if full > 0.02 else max(0.0, full)
            else:
                gap = 0.15 if full > 0.15 else max(0.0, full)
            room = max(0.0, gap - lead)
            if room > 0.004:
                pieces.append((prev_end, prev_end + room))
                cursor += room
        if i > 5 and i + 1 < len(words) and i + 1 != idx:
            nxt = words[i + 1]["start"]
            if nxt - w["end"] > 0.08:
                src_b = min(nxt - 0.02, w["end"] + TAIL_S)
        elif i + 1 == len(words):
            src_b = min(probe(RAW_VO) - 0.01, w["end"] + TAIL_S)
        cap_s = cursor + max(0.0, w["start"] - src_a)
        cap_e = cap_s + (w["end"] - w["start"])
        mapped.append((w["text"], round(cap_s, 3), round(cap_e, 3)))
        pieces.append((src_a, src_b))
        cursor += src_b - src_a
        onset, offset = attack_in(src_a, src_b)
        log.append({
            "word": w["text"], "src": [round(src_a, 3), round(src_b, 3)],
            "onset_s": onset, "offset_s": offset,
            "cut_s": round(src_a, 3), "end_s": round(src_b, 3),
            "lead_ms": None if onset is None else round((onset - src_a) * 1000, 1),
            "tail_ms": None if offset is None else round((src_b - offset) * 1000, 1),
            "opens_in_speech": rms_db(src_a) > DB60,
        })

    for n in range(1, len(pieces)):
        if pieces[n][0] + 0.002 < pieces[n - 1][1]:
            raise SystemExit(f"overlap at piece {n}: {pieces[n - 1]} -> {pieces[n]}")
    # The sixteen span must include source 20.38.
    sixteen = next(row for row in log if "1600" in row["word"].replace(",", ""))
    if not (sixteen["src"][0] <= SIXTEEN_SRC <= sixteen["src"][1]):
        raise SystemExit(f"sixteen span {sixteen['src']} misses {SIXTEEN_SRC}")

    fc = []
    for i, (a, b) in enumerate(pieces):
        d = max(0.012, b - a)
        fade = min(0.004, d / 4)
        fc.append(
            f"[0:a]atrim={a:.4f}:{a + d:.4f},asetpts=PTS-STARTPTS,"
            f"afade=t=in:d={fade:.4f},afade=t=out:st={d - fade:.4f}:d={fade:.4f}[p{i}]")
    fc.append("".join(f"[p{i}]" for i in range(len(pieces))) + f"concat=n={len(pieces)}:v=0:a=1[a]")
    out = work / f"hos_sa_{SID}_vo_{VER}.wav"
    ff("-i", str(RAW_VO), "-filter_complex", ";".join(fc), "-map", "[a]", "-c:a", "pcm_s16le", str(out))
    (work / "onset_log.json").write_text(json.dumps(log, indent=2) + "\n")
    return out, mapped, log


def chunk_words(words: list[tuple[str, float, float]]) -> list[dict]:
    chunks, i, n = [], 0, len(words)
    while i < n:
        t0 = words[i][1]
        parts, t_end, j = [words[i][0]], words[i][2], i + 1
        while j < n:
            wj, sj, ej = words[j]
            if parts[-1][-1:] in ".?!":
                break
            if ej - t0 >= 1.55 and len(parts) >= 2:
                break
            if len(parts) >= 5 and sj - t0 >= 0.45:
                break
            parts.append(wj)
            t_end = ej
            j += 1
        chunks.append({"text": " ".join(parts), "t0": round(t0, 3), "t1": round(t_end + 0.08, 3)})
        i = j
    for k in range(len(chunks) - 1):
        chunks[k]["t1"] = chunks[k + 1]["t0"]
    return chunks


def render_hook(path: Path) -> dict:
    tokens = [(w.strip("*"), w.startswith("**")) for w in HOOK.split()]
    size = 60
    font = ImageFont.truetype(FONT, size, index=2)
    while True:
        font = ImageFont.truetype(FONT, size, index=2)
        cap = -font.getbbox("H", anchor="ls")[1]
        if cap >= 0.086 * H:
            break
        size += 1
    while max(font.getlength(t) for t, _ in tokens) > W - 100 and size > 48:
        size -= 2
        font = ImageFont.truetype(FONT, size, index=2)
        cap = -font.getbbox("H", anchor="ls")[1]
    pitch = round(cap * 1.22)
    top = int(0.025 * H)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    for k, (t, hot) in enumerate(tokens):
        draw.text((W / 2, top + cap + k * pitch), t, font=font, anchor="ms",
                  fill=YEL if hot else CREAM, stroke_width=6, stroke_fill=INK)
    img.save(path)
    block = pitch * (len(tokens) - 1) + cap
    return {"font_size": size, "cap_pct": round(100 * cap / H, 2),
            "block_pct": [round(100 * top / H, 1), round(100 * (top + block) / H, 1)]}


def render_cap(path: Path, text: str) -> None:
    size = 64
    font = ImageFont.truetype(FONT, size, index=2)
    while font.getlength(text) > W - 80 and size > 36:
        size -= 2
        font = ImageFont.truetype(FONT, size, index=2)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    y = H - 280
    draw.text((W / 2, y), text, font=font, anchor="ms", fill=CREAM, stroke_width=4, stroke_fill=INK)
    img.save(path)


def render_card(path: Path, line1: str, line2: str) -> dict:
    """Lower-band card, same band as Galen v02 (y 656-1264)."""
    size1 = int(BAND_H * 0.11)
    size2 = int(BAND_H * 0.072)
    f1 = ImageFont.truetype(FONT, size1, index=2)
    f2 = ImageFont.truetype(FONT, size2, index=0)
    while f1.getlength(line1) > W - 160 and size1 > 42:
        size1 -= 2
        f1 = ImageFont.truetype(FONT, size1, index=2)
    while f2.getlength(line2) > W - 160 and size2 > 32:
        size2 -= 2
        f2 = ImageFont.truetype(FONT, size2, index=0)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shade)
    y2 = BAND_TOP + BAND_H - 36
    y1 = y2 - size2 - 16
    top = y1 - size1 - 28
    band_bottom = BAND_TOP + BAND_H
    for yy in range(max(0, top), min(H, band_bottom + 40)):
        rise = min(1.0, (yy - top) / 80)
        fall = 1.0 if yy < band_bottom - 40 else max(0.0, 1 - (yy - (band_bottom - 40)) / 80)
        a = int(110 * rise * fall)
        if a <= 0:
            continue
        sd.line([(48, yy), (W - 48, yy)], fill=(0, 0, 0, a))
    img = Image.alpha_composite(img, shade)
    d = ImageDraw.Draw(img)
    d.text((72, y1), line1, font=f1, anchor="ls", fill=YEL, stroke_width=4, stroke_fill=INK)
    d.text((72, y2), line2, font=f2, anchor="ls", fill=CREAM, stroke_width=3, stroke_fill=INK)
    img.save(path)
    return {"line1": line1, "line2": line2, "y": [int(top), int(y2)], "band": [BAND_TOP, band_bottom]}


def band_mask() -> Path:
    path = WORK / "band_mask.png"
    if path.exists():
        return path
    fh, feather = 608, 140
    img = Image.new("L", (W, fh), 255)
    px = img.load()
    for y in range(fh):
        if y < feather:
            a = int(255 * (y / feather) ** 1.6)
        elif y > fh - 1 - feather:
            a = int(255 * ((fh - 1 - y) / feather) ** 1.6)
        else:
            a = 255
        for x in range(W):
            px[x, y] = a
    img.save(path)
    return path


def seg_move(src: Path, dst: Path, start: float, dur: float) -> None:
    if start < 0:
        raise SystemExit(f"{src.name}: negative in-point {start}")
    if start + dur > probe(src) - 0.04:
        raise SystemExit(f"{src.name}: in {start} + {dur:.2f} runs past {probe(src):.2f}")
    mask = band_mask()
    vf = (f"trim=start={start:.4f}:duration={dur:.4f},setpts=PTS-STARTPTS,fps={FPS},split[a][b];"
          f"[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=26:2,"
          f"eq=brightness=-0.06[bg];"
          f"[b]scale={W}:608:flags=lanczos,format=rgba[fg];"
          f"[1:v]format=gray[m];"
          f"[fg][m]alphamerge[fg2];"
          f"[bg][fg2]overlay=(W-w)/2:(H-h)/2:shortest=1,setsar=1")
    ff("-i", str(src), "-loop", "1", "-i", str(mask), "-filter_complex", vf, "-an",
       "-t", f"{dur:.3f}", "-c:v", "libx264",
       "-pix_fmt", "yuv420p", "-color_range", "tv", "-colorspace", "bt709",
       "-preset", "fast", "-crf", "16", "-r", str(FPS), str(dst))


def seg_still(src: Path, dst: Path, dur: float, direction: int, scale: float = 1.08,
              y_frac: float = 0.40, x0: float | None = None, x1: float | None = None) -> None:
    """Slow linear pan on a 9:16 still. One direction, no reversal."""
    if x0 is None or x1 is None:
        x0, x1 = (0.12, 0.88) if direction > 0 else (0.88, 0.12)
    nw, nh = int(W * scale), int(H * scale)
    # JPEG stills otherwise tag yuvj (full range). Mixed with the limited-range
    # plates, the concat re-encode shifts the loop and the last frame no longer
    # matches frame 0.
    vf = (f"scale={nw}:{nh}:flags=lanczos,crop=1080:1920:"
          f"x='(iw-ow)*({x0:.3f}+({x1 - x0:.3f})*t/{dur:.4f})':y='(ih-oh)*{y_frac:.3f}',"
          f"fps={FPS},setsar=1,scale=in_range=pc:out_range=tv,format=yuv420p")
    ff("-loop", "1", "-i", str(src), "-vf", vf, "-an", "-t", f"{dur:.3f}",
       "-c:v", "libx264", "-pix_fmt", "yuv420p", "-color_range", "tv", "-colorspace", "bt709",
       "-preset", "fast", "-crf", "16", "-r", str(FPS), str(dst))


def word_at(words: list[tuple[str, float, float]], token: str, after: float = -1.0) -> float:
    tok = token.lower()
    for w, s, _e in words:
        if w.lower().strip(".,;:").startswith(tok) and s >= after:
            return s
    raise SystemExit(f"no word {token!r} after {after}")


def frames_between(t0: float, t1: float) -> tuple[int, float]:
    n = max(8, int(round((t1 - t0) * FPS)))
    return n, n / FPS


def body_plan(words: list[tuple[str, float, float]], vo_s: float) -> list[dict]:
    """Picture follows the line. Every hold is at most 3.0 s. Stills never touch."""
    in_t = word_at(words, "in")
    pol_t = word_at(words, "polonium")
    glowed_t = word_at(words, "glowed")
    handled_t = word_at(words, "handled")
    today_t = word_at(words, "today")
    takes_t = word_at(words, "takes")
    rows = []
    t = 0.0

    def add(t1: float, kind: str, rel: str, ins: float, label: str, direction: int = 1) -> None:
        nonlocal t
        t1 = min(vo_s if label != "loop" else t1, t1)
        n, dur = frames_between(t, t1)
        t1 = t + dur
        if dur > 3.001:
            raise SystemExit(f"{label} hold {dur:.2f}s ({t:.2f}-{t1:.2f})")
        if dur < 0.50:
            raise SystemExit(f"{label} hold {dur:.2f}s is under 0.50")
        rows.append({"t0": round(t, 3), "t1": round(t1, 3), "kind": kind, "rel": rel,
                     "in_s": ins, "label": label, "hold_s": round(dur, 3), "direction": direction})
        t = t1

    first = min(FIRST_CUT_MAX, PLATE_SAFE - F0_IN, max(2.05, in_t - 0.05))
    add(first, "move", WURZ, F0_IN, "lab")
    add(min(pol_t - 0.04, t + 2.90), "still", "02_shed_lab_v01.jpg", 0, "shed", 1)
    add(min(glowed_t + 0.02, t + 2.90), "move", GLOW, 0.45, "glow")
    add(min(handled_t - 0.62, t + 2.20), "still", "03_glowing_vials_v01.jpg", 0, "vials", -1)
    add(min(handled_t + 0.08, t + 1.05), "move", BENCH, 0.80, "bench")
    add(min(today_t - 0.08, t + 2.90), "still", "04_bare_hands_v01.jpg", 0, "hands", 1)
    add(min(today_t + 0.85, t + 1.10), "move", DOOR_A, 0.55, "door")
    # v02's shelves read as a split panel. v01 is the same archive and passes.
    add(min(takes_t - 0.70, t + 2.90), "still", "05_paris_archive_v01.jpg", 0, "paris", -1)
    # Bridge, then the lead box for at most 2.90 s, ending on the voice.
    lead_len = min(2.90, max(0.80, vo_s - t - 0.70))
    bridge_end = vo_s - lead_len
    if bridge_end < t + 0.55:
        bridge_end = t + 0.55
    add(bridge_end, "move", DOOR_B, 0.40, "latch")
    # Full frame shelves fail the split-panel check. This crop stays on the box.
    rows_lead_still = {"scale": 1.7, "y_frac": 0.47, "x0": 0.06, "x1": 0.22}
    add(vo_s, "still", "01_lead_box_v01.jpg", 0, "lead", 1)
    rows[-1]["still"] = rows_lead_still
    rows[-1]["upscale"] = 1.7
    if abs(t - vo_s) > 0.05:
        raise SystemExit(f"plan ends {t:.3f}, vo {vo_s:.3f}")
    n_loop = int(round(LOOP_S * FPS))
    loop_dur = n_loop / FPS
    loop_in = round(F0_IN - loop_dur, 4)
    if loop_in < 0.02:
        raise SystemExit(f"loop in-point {loop_in}")
    rows.append({"t0": round(vo_s, 3), "t1": round(vo_s + loop_dur, 3), "kind": "move",
                 "rel": WURZ, "in_s": loop_in, "label": "loop", "hold_s": round(loop_dur, 3),
                 "direction": 0})
    if rows[1]["t0"] > FIRST_CUT_MAX + 0.02:
        raise SystemExit(f"first cut {rows[1]['t0']}")
    for a, b in zip(rows, rows[1:]):
        if a["kind"] == "still" and b["kind"] == "still":
            raise SystemExit(f"still-to-still {a['label']} -> {b['label']}")
    return rows


def synth_bed(path: Path, dur: float, sr: int = 48000) -> None:
    """Low fifths at 61 BPM. Not the v05 glass pad (68 BPM, 98 Hz stack)."""
    n = int(sr * dur)
    freqs = [82.41, 123.47, 164.81, 246.94, 329.63]
    amps = [0.30, 0.18, 0.12, 0.08, 0.05]
    frames = bytearray()
    for i in range(n):
        t = i / sr
        pulse = 0.90 + 0.10 * math.sin(2 * math.pi * (61 / 60) * t)
        env = min(1.0, t / 0.55) * min(1.0, max(0.0, (dur - t) / 0.45))
        l = r = 0.0
        for k, (f, a) in enumerate(zip(freqs, amps)):
            l += math.sin(2 * math.pi * f * t + 0.3 * k) * a
            r += math.sin(2 * math.pi * (f * 1.002) * t + 0.55 * k) * a
        g = env * pulse * 0.16
        frames += struct.pack("<hh", int(max(-1, min(1, l * g)) * 32767),
                              int(max(-1, min(1, r * g)) * 32767))
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(bytes(frames))


def place_sfx(total: float, tick_at: float) -> Path:
    kit = HERE / "06_Sound-Effects" / "kit_v01"
    whoosh = kit / "sfx_hos_whoosh_soft_v01.wav"
    tick = kit / "sfx_hos_tick_ink_v01.wav"
    if not whoosh.exists() or not tick.exists():
        subprocess.run([sys.executable, str(OWB / "scripts/sfx_kit.py"), "make",
                        "--out-dir", str(kit), "--house", "hos"], check=True)
    dst = WORK / "sfx_stem.wav"
    delay = int(tick_at * 1000)
    ff("-f", "lavfi", "-t", f"{total:.3f}", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
       "-i", str(whoosh), "-i", str(tick), "-filter_complex",
       "[1:a]volume=-16dB,afade=t=out:st=0.7:d=0.2[w];"
       f"[2:a]volume=-10dB,adelay={delay}|{delay}[t];"
       "[0:a][w][t]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.5[a]",
       "-map", "[a]", "-c:a", "pcm_s16le", str(dst))
    return dst


def mix(vo: Path, bed: Path, sfx: Path, total: float, dst: Path, bed_db: float, sfx_db: float) -> None:
    ff("-i", str(vo), "-i", str(bed), "-i", str(sfx), "-filter_complex",
       f"[0:a]aformat=sample_rates=48000:channel_layouts=stereo,apad=whole_dur={total:.3f}[v];"
       f"[1:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{total:.3f},volume={bed_db:.2f}dB[b];"
       f"[2:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{total:.3f},volume={sfx_db:.2f}dB[s];"
       f"[v][b][s]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.9[a]",
       "-map", "[a]", "-t", f"{total:.3f}", "-c:a", "pcm_s16le", str(dst))


def integrated_lufs(p: Path) -> float:
    err = subprocess.run(["ffmpeg", "-nostats", "-hide_banner", "-i", str(p), "-af", "ebur128", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    lines = [ln for ln in err.splitlines() if "I:" in ln and "LUFS" in ln]
    return float(lines[-1].split("I:")[1].split("LUFS")[0].strip())


def true_peak(p: Path) -> float:
    err = subprocess.run(["ffmpeg", "-nostats", "-hide_banner", "-i", str(p),
                          "-af", "ebur128=peak=true", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    hits = [ln for ln in err.splitlines() if "Peak:" in ln]
    return float(hits[-1].split("Peak:")[1].split("dBFS")[0].strip())


def sound(vo: Path, total: float, tick_at: float) -> dict:
    bed = MUSIC / f"hos_sa_{SID}_{VER}_bed.wav"
    synth_bed(bed, total + 0.3)
    plan = {
        "prompt": ("Low open-fifth drone under a spoken radium fact, even, no chase. "
                   "Pace: 58-66 BPM. NOT the v05 Curie glass pad (68 BPM, 98 Hz stack), "
                   "NOT the 001 flask pulse, NOT the 005 heart-sum pad, "
                   "NOT any Orbit With Ben bed, NOT a drum loop, NOT a trailer sting."),
        "film": "standalone-s4", "short": f"{SID}_{VER}", "job": JOB,
        "source": "own synthesis in _build_short_s4_curie_notebooks_v06.py, 0 credits",
        "pace_bpm": "58-66",
    }
    bed.with_name(bed.stem + "_plan.json").write_text(json.dumps(plan, indent=2) + "\n")
    sfx = place_sfx(total, tick_at)
    QA.mkdir(parents=True, exist_ok=True)
    bed_db, sfx_db = -10.0, -10.0
    audio = WORK / "audio.wav"
    level = {}
    for _ in range(6):
        mix(vo, bed, sfx, total, audio, bed_db, sfx_db)
        vo_stem = WORK / "stem_vo.wav"
        bed_stem, sfx_stem = WORK / "stem_bed.wav", WORK / "stem_sfx.wav"
        ff("-i", str(vo), "-af", f"apad=whole_dur={total:.3f}", "-t", f"{total:.3f}", "-c:a", "pcm_s16le", str(vo_stem))
        ff("-i", str(bed), "-af", f"volume={bed_db:.2f}dB,atrim=0:{total:.3f}", "-c:a", "pcm_s16le", str(bed_stem))
        ff("-i", str(sfx), "-af", f"volume={sfx_db:.2f}dB,atrim=0:{total:.3f}", "-c:a", "pcm_s16le", str(sfx_stem))
        r = subprocess.run([sys.executable, str(OWB / "scripts/sfx_kit.py"), "level",
                            "--vo", str(vo_stem), "--sfx", str(sfx_stem), "--bed", str(bed_stem),
                            "--minutes", f"{total / 60:.3f}", "--out", str(QA / "sfx_level.json")],
                           capture_output=True, text=True)
        level = {"exit": r.returncode, "output": (r.stdout + r.stderr).strip(), "bed_db": bed_db, "sfx_db": sfx_db}
        if r.returncode == 0:
            break
        bed_db -= 3.0
        sfx_db -= 3.0
    norm = WORK / "audio_norm.wav"
    ff("-i", str(audio), "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-c:a", "pcm_s16le", str(norm))
    measured = integrated_lufs(norm)
    peak = true_peak(norm)
    gain = -14.0 - measured
    if peak + gain > -1.15:
        gain = -1.15 - peak
    nudged = WORK / "audio_nudge.wav"
    # Leave about 3 dB before 0 dBFS so the AAC encode stays at or under -1 dBTP.
    ff("-i", str(norm), "-af", f"volume={gain:.2f}dB,alimiter=limit=0.71:attack=5:release=40",
       "-c:a", "pcm_s16le", str(nudged))
    level["nudge_db"] = round(gain, 2)
    level["pre_nudge_lufs"] = measured
    return {"audio": nudged, "bed": bed, "level": level}


def loop_diff(mp4: Path) -> float:
    a, c = WORK / "diff_a.png", WORK / "diff_b.png"
    ff("-i", str(mp4), "-frames:v", "1", str(a))
    ff("-sseof", "-0.05", "-i", str(mp4), "-frames:v", "1", str(c))
    im_a = Image.open(a).convert("RGB")
    im_b = Image.open(c).convert("RGB").resize(im_a.size)
    pa, pb = im_a.load(), im_b.load()
    w, h = im_a.size
    mask = Image.new("L", (w, h), 0)
    mpix = mask.load()
    for y in range(h):
        for x in range(w):
            r, g, bl = pa[x, y]
            r2, g2, b2 = pb[x, y]
            cream = r > 200 and g > 185 and bl > 150 and abs(r - g) < 50
            ink = r < 40 and g < 40 and bl < 40
            yellow = r > 200 and g > 160 and bl < 140 and g > bl + 80
            differ = abs(r - r2) + abs(g - g2) + abs(bl - b2) > 80
            if differ and (cream or ink or yellow):
                mpix[x, y] = 255
    mask = mask.filter(ImageFilter.MaxFilter(7))
    mpix = mask.load()
    acc = n = 0
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            if mpix[x, y]:
                continue
            r, g, bl = pa[x, y]
            r2, g2, b2 = pb[x, y]
            la = 0.2126 * r + 0.7152 * g + 0.0722 * bl
            lb = 0.2126 * r2 + 0.7152 * g2 + 0.0722 * b2
            acc += abs(la - lb)
            n += 1
    return round(acc / max(1, n), 2)


def black_frac(mp4: Path, t: float) -> float:
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(mp4),
                                   "-frames:v", "1", "-vf", "scale=160:284", "-f", "rawvideo", "-pix_fmt", "gray", "-"])
    return round(sum(1 for p in raw if p < 18) / max(1, len(raw)), 3)


def norm_tokens(text: str) -> list[str]:
    """Numeral 1,600, '1 600' and 'sixteen hundred' are the same words."""
    t = text.lower().replace("’", "'").replace(",", " ")
    t = re.sub(r"\b(?:1\s*600|1600|sixteen\s+hundred)\b", " sixteen hundred ", t)
    return re.findall(r"[a-z']+", t)


def whisper_words(wav: Path) -> dict:
    py = Path.home() / ".venvs/hos-vo/bin/python"
    if not py.exists():
        raise SystemExit(f"no faster-whisper venv at {py}")
    code = (
        "import json,sys\n"
        "from faster_whisper import WhisperModel\n"
        "m=WhisperModel('small.en', device='cpu', compute_type='int8')\n"
        "segs,_=m.transcribe(sys.argv[1], language='en', word_timestamps=True, vad_filter=False)\n"
        "words=[]\n"
        "for s in segs:\n"
        "    for w in (s.words or []):\n"
        "        words.append({'word':w.word.strip(),'start':round(w.start,3),'end':round(w.end,3)})\n"
        "text=' '.join(w['word'] for w in words)\n"
        "print(json.dumps({'text':text,'words':words}))\n"
    )
    r = subprocess.run([str(py), "-c", code, str(wav)], capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"whisper failed: {r.stderr[-800:]}")
    return json.loads(r.stdout)


def asr_check(spoken: str, vo: Path) -> dict:
    stem = whisper_words(vo)
    want = norm_tokens(spoken)
    got = norm_tokens(stem["text"])
    notes = []
    if got != want:
        notes.append(f"stem {stem['text']!r}")
    heard = " ".join(norm_tokens(stem["text"]))
    if "sixteen hundred" not in heard:
        notes.append(f"sixteen hundred not heard: {stem['text']!r}")
    QA.mkdir(parents=True, exist_ok=True)
    payload = {"model": "small.en", "spoken": spoken, "stem": stem, "ok": not notes, "notes": notes}
    (QA / f"asr_{SID}_{VER}.json").write_text(json.dumps(payload, indent=2) + "\n")
    (QA / f"asr_{SID}_{VER}.txt").write_text(
        f"spoken: {spoken}\nstem: {stem['text']}\n" + ("\n".join(notes) if notes else "OK\n"))
    return payload


def run_qa(mp4: Path, plan: list[dict]) -> dict:
    cuts, pool, seen = [], [], set()
    for k, row in enumerate(plan, 1):
        base = Path(row["rel"]).name
        src_id = f"loop_span_{base}" if row["label"] == "loop" else base
        video = row["kind"] == "move"
        cuts.append({"row": f"s{k:02d}_{row['label']}", "timeline_in": row["t0"], "timeline_out": row["t1"],
                     "source": src_id, "upscale": row.get("upscale", 0.84 if video else 1.08), "video": video,
                     "framing": {"offset": row["in_s"]}})
        if src_id not in seen:
            seen.add(src_id)
            title = "Flow Veo plate" if video else "Flow house plate"
            pool.append({"file_id": src_id, "title": title})
    cuts_f = QA / f"cuts_{SID}_{VER}.json"
    pool_f = QA / f"pool_{SID}_{VER}.json"
    cuts_f.write_text(json.dumps(cuts, indent=2) + "\n")
    pool_f.write_text(json.dumps(pool, indent=2) + "\n")
    rel = lambda p: str(p.relative_to(REPO))  # noqa: E731
    r_pg = subprocess.run([sys.executable, str(OWB / "scripts/polish_gate.py"), rel(mp4),
                           "--cuts", rel(cuts_f), "--out", rel(QA / f"polish_gate_{SID}_{VER}.json")],
                          cwd=REPO, capture_output=True, text=True)
    (QA / f"polish_gate_{SID}_{VER}.txt").write_text((r_pg.stdout + r_pg.stderr).strip() + "\n")
    r_pq = subprocess.run([sys.executable, str(OWB / "scripts/picture_qa.py"), rel(mp4),
                           "--cuts", rel(cuts_f), "--pool", rel(pool_f),
                           "--out-dir", rel(QA / f"picture_qa_{SID}_{VER}")],
                          cwd=REPO, capture_output=True, text=True)
    (QA / f"picture_qa_{SID}_{VER}.txt").write_text((r_pq.stdout + r_pq.stderr).strip() + "\n")
    return {"polish_gate": {"exit": r_pg.returncode, "tail": (r_pg.stdout + r_pg.stderr).strip().splitlines()[-8:]},
            "picture_qa": {"exit": r_pq.returncode, "tail": (r_pq.stdout + r_pq.stderr).strip().splitlines()[-8:]}}


def sheet_2fps(mp4: Path) -> Path:
    out = QA / f"{mp4.stem}_2fps_sheet.jpg"
    ff("-i", str(mp4), "-vf", "fps=2,scale=180:-2,tile=8x8", "-q:v", "4", str(out))
    return out


def copy_out(mp4: Path, phone: Path, sheet: Path) -> list[str]:
    uat = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT/standalone_s4_curie_v06"
    nas = Path("/Volumes/data/mac-mini-archive/YouTube/History Of Science/"
               "docs/STANDALONE_SHORTS_TEST_2026-10/s4_curie_notebooks_v06")
    copied = []
    for folder in (uat, nas):
        folder.mkdir(parents=True, exist_ok=True)
        for src in (mp4, phone, sheet):
            shutil.copy2(src, folder / src.name)
            copied.append(str(folder / src.name))
    return copied


def plate_path(rel: str, kind: str) -> Path:
    p = (STILLS / rel) if kind == "still" else (NAS_CLIPS / rel)
    if not p.exists():
        raise SystemExit(f"missing plate {p}")
    return p


def build() -> dict:
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    QA.mkdir(parents=True, exist_ok=True)
    vo, words, onset_log = lifted_vo(WORK)
    spoken = " ".join(w for w, _, _ in words)
    (WORK / "spoken.txt").write_text(spoken + "\n")
    shutil.copy(WORK / "onset_log.json", QA / f"onset_{SID}_{VER}.json")
    vo_s = probe(vo)
    asr = asr_check(spoken, vo)
    if os.environ.get("VO_ONLY"):
        summary = {"vo_s": round(vo_s, 3), "spoken": spoken, "asr": asr, "onset": onset_log,
                   "words": [{"w": w, "s": s, "e": e} for w, s, e in words]}
        print(json.dumps({k: summary[k] for k in ("vo_s", "spoken", "asr", "words")}, indent=2))
        return summary
    if not asr["ok"]:
        raise SystemExit("ASR not word-for-word: " + "; ".join(asr["notes"]))

    total = round(vo_s + LOOP_S, 3)
    if not 18.0 <= total <= 24.05:
        raise SystemExit(f"duration {total}s outside 18-24 (vo {vo_s:.2f})")
    still_t = next(s for w, s, e in words if w.lower().startswith("still"))
    note_t = next(s for w, s, e in words if w.lower().startswith("notebook"))
    if words[0][1] > 0.15:
        raise SystemExit(f"first word at {words[0][1]}")
    if still_t > 1.50 or note_t > 1.50:
        raise SystemExit(f"claim late: notebooks {note_t} still {still_t}")
    plan = body_plan(words, vo_s)
    (WORK / "plan.json").write_text(json.dumps(plan, indent=2) + "\n")
    print("PLAN", json.dumps([{k: r[k] for k in ("t0", "t1", "label", "hold_s", "rel")} for r in plan]))

    segs = []
    for k, row in enumerate(plan):
        src = plate_path(row["rel"], row["kind"])
        out = WORK / f"seg_{k:02d}.mp4"
        if row["kind"] == "still":
            extra = row.get("still") or {}
            seg_still(src, out, row["hold_s"], row["direction"], **extra)
        else:
            seg_move(src, out, row["in_s"], row["hold_s"])
        segs.append(out)
    (WORK / "pic.txt").write_text("".join(f"file '{s.name}'\n" for s in segs))
    pic = WORK / "picture.mp4"
    ff("-f", "concat", "-safe", "0", "-i", "pic.txt", "-c:v", "libx264", "-pix_fmt", "yuv420p",
       "-preset", "fast", "-crf", "16", "-r", str(FPS), "-t", f"{total:.3f}", str(pic), cwd=WORK)

    who_in = plan[1]["t0"]
    who_out = min(who_in + 3.2, plan[2]["t1"])
    half_t = next(s for w, s, e in words if "1600" in w.replace(",", ""))
    half_out = min(half_t + 3.2, vo_s - 0.15)
    snd = sound(vo, total, who_in)
    chunks = chunk_words(words)
    overlays = []
    hook_png = WORK / "cap_hook.png"
    hook_meta = render_hook(hook_png)
    overlays.append((hook_png, 0.0, 2.0, False))
    who_png = WORK / "card_who.png"
    who_meta = render_card(who_png, "MARIE CURIE", "Paris, 1898")
    who_meta["in_s"] = round(who_in, 3)
    who_meta["out_s"] = round(who_out, 3)
    overlays.append((who_png, who_in, who_out, True))
    fact_png = WORK / "card_half.png"
    fact_meta = render_card(fact_png, "HALF-LIFE", "1,600 years")
    fact_meta["in_s"] = round(half_t, 3)
    fact_meta["out_s"] = round(half_out, 3)
    overlays.append((fact_png, half_t, half_out, True))
    for i, c in enumerate(chunks):
        png = WORK / f"cap_{i:03d}.png"
        render_cap(png, c["text"])
        overlays.append((png, c["t0"], min(c["t1"], total - 0.05), False))

    inputs = ["-i", str(pic), "-i", str(snd["audio"])]
    fc, last = [], "[0:v]"
    for i, (png, t0, t1, fade) in enumerate(overlays):
        inputs += ["-loop", "1", "-t", f"{total:.3f}", "-i", str(png)]
        src = f"[{i + 2}:v]"
        if fade:
            faded = f"[c{i}]"
            fc.append(f"{src}format=rgba,fade=t=in:st={t0:.3f}:d=0.35:alpha=1,"
                      f"fade=t=out:st={max(t0, t1 - 0.35):.3f}:d=0.35:alpha=1{faded}")
            src = faded
        fc.append(f"{last}{src}overlay=0:0:enable='between(t,{t0:.3f},{t1:.3f})'[v{i}]")
        last = f"[v{i}]"
    mp4 = HERE / "shorts_v01" / f"hos_sa_{SID}_{VER}.mp4"
    ff(*inputs, "-filter_complex", ";".join(fc), "-map", last, "-map", "1:a",
       "-c:v", "libx264", "-pix_fmt", "yuv420p", "-profile:v", "high", "-preset", "medium", "-crf", "18",
       "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
       "-t", f"{total:.3f}", "-movflags", "+faststart", str(mp4))
    peak_now = true_peak(mp4)
    if peak_now > -1.05:
        drop = min(-0.3, -1.25 - peak_now)
        quieter = WORK / "quieter.mp4"
        ff("-i", str(mp4), "-c:v", "copy", "-af", f"volume={drop:.2f}dB",
           "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
           "-movflags", "+faststart", str(quieter))
        quieter.replace(mp4)

    diff = loop_diff(mp4)
    lufs, peak = integrated_lufs(mp4), true_peak(mp4)
    half_word = next(s for w, s, e in words if w.lower().startswith("half"))
    holds = [r["hold_s"] for r in plan if r["label"] != "loop"]
    digest = sha256(mp4)
    brief = {
        "frame0_source": f"003/04_Generated-Clips/{WURZ}",
        "frame0_zoom": f"none — moving Flow plate, in {F0_IN:.2f}s, centre-band, no Ken Burns",
        "frame0_in_s": F0_IN,
        "loop_in_s": plan[-1]["in_s"],
        "loop_ends_on": "frame before frame 0 in-point; no frame-0 copy",
        "first_word_s": words[0][1],
        "surprise_s": {"notebooks": note_t, "still": still_t},
        "first_cut_s": plan[1]["t0"],
        "last_word_to_loop_s": round(total - words[-1][2], 3),
        "meta_promise": False,
        "runtime_s": round(probe(mp4), 3),
        "longest_hold_s": max(holds),
        "payoff_phrase": "lose half its strength",
        "payoff_s": half_word,
        "payoff_frac": round(half_word / total, 3),
        "loop_sentence": "Radium takes 1,600 years to lose half its strength. Marie Curie's notebooks are still radioactive.",
        "loop_diff": diff,
        "lufs": lufs,
        "true_peak_dbfs": peak,
        "frame0_black": black_frac(mp4, 0.2),
        "sha256": digest,
        "who_card": who_meta,
        "half_life_card": fact_meta,
        "no_cta": True,
        "no_new_spend": True,
        "no_frame0_stamp": True,
    }
    meta = {
        "id": SID, "version": VER, "job": JOB, "youtube_id": YT,
        "title": "Are Marie Curie's Notebooks Still Radioactive?",
        "air_date": AIR, "spoken": spoken, "script": spoken,
        "words": [{"word": w, "start": s, "end": e} for w, s, e in words],
        "word_count": len(words), "vo_s": round(vo_s, 3), "last_word_end_s": words[-1][2],
        "plan": plan, "hook": HOOK.replace("**", ""), "hook_layer": hook_meta,
        "onset": onset_log, "asr_ok": asr["ok"],
        "no_cta": True, "no_new_spend": True,
        "bed": snd["bed"].name, "sfx_level": snd["level"], **brief,
    }
    meta_path = HERE / "shorts_v01" / f"hos_sa_{SID}_{VER}_meta.json"
    meta_path.write_text(json.dumps(meta, indent=2) + "\n")

    gate = subprocess.run([sys.executable, str(REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"),
                           "check", str(mp4), "--air-date", AIR, "--id", YT,
                           "--script", str(WORK / "spoken.txt"), "--vo", str(vo),
                           "--meta", str(meta_path), "--json"],
                          capture_output=True, text=True)
    (QA / f"gate_{SID}_{VER}.txt").write_text((gate.stdout + gate.stderr).strip() + "\n")
    try:
        gate_json = json.loads(gate.stdout)
        if isinstance(gate_json, list):
            gate_json = gate_json[0]
    except json.JSONDecodeError:
        gate_json = {"verdict": "FAIL", "raw": (gate.stdout + gate.stderr)[-2000:]}
    (QA / f"gate_{SID}_{VER}.json").write_text(json.dumps(gate_json, indent=2) + "\n")

    qa = run_qa(mp4, plan)
    music = subprocess.run([sys.executable, str(OWB / "scripts/music_gate.py"), str(HERE),
                            "--bed", str(snd["bed"]), "--video", str(mp4),
                            "--out", str(QA / f"music_gate_{SID}_{VER}.json")],
                           capture_output=True, text=True)
    (QA / f"music_gate_{SID}_{VER}.txt").write_text((music.stdout + music.stderr).strip() + "\n")

    phone = HERE / "shorts_v01" / f"hos_sa_{SID}_{VER}_PHONE.mp4"
    ff("-i", str(mp4), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "26",
       "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(phone))
    sheet = sheet_2fps(mp4)
    copies = copy_out(mp4, phone, sheet)
    summary = {
        "file": mp4.name, "sha256": digest, "duration_s": brief["runtime_s"],
        "spoken": spoken, "brief": brief, "gate_exit": gate.returncode,
        "gate_verdict": gate_json.get("verdict"), "gate_fails": gate_json.get("fails"),
        "gate_warns": gate_json.get("warns"), "qa": qa, "asr": asr,
        "music_exit": music.returncode, "music_tail": (music.stdout + music.stderr).strip().splitlines()[-6:],
        "sfx": snd["level"], "copies": copies,
    }
    (QA / f"build_{SID}_{VER}.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({k: summary[k] for k in ("file", "duration_s", "gate_verdict", "gate_fails", "gate_warns",
                                              "qa", "music_exit", "music_tail", "sfx", "asr", "brief")}, indent=2))
    return summary


def main() -> None:
    rec = build()
    if os.environ.get("VO_ONLY"):
        if not rec["asr"]["ok"]:
            raise SystemExit("ASR NOT OK")
        print("VO OK", rec["vo_s"])
        return
    bad = []
    if rec["gate_verdict"] != "PASS":
        bad.append("gate")
    if rec["qa"]["polish_gate"]["exit"] != 0:
        bad.append("polish")
    if rec["qa"]["picture_qa"]["exit"] != 0:
        bad.append("picture")
    if rec["music_exit"] != 0:
        bad.append("music")
    if rec["sfx"]["exit"] != 0:
        bad.append("sfx")
    if not rec["asr"]["ok"]:
        bad.append("asr")
    if rec["brief"]["loop_diff"] > 5:
        bad.append(f"loop_diff {rec['brief']['loop_diff']}")
    if rec["brief"]["frame0_black"] > 0.30:
        bad.append(f"black {rec['brief']['frame0_black']}")
    if rec["brief"]["payoff_frac"] < 0.70:
        bad.append(f"payoff {rec['brief']['payoff_frac']}")
    if rec["brief"]["longest_hold_s"] > 3.01:
        bad.append(f"hold {rec['brief']['longest_hold_s']}")
    if not (-14.5 <= rec["brief"]["lufs"] <= -13.5):
        bad.append(f"lufs {rec['brief']['lufs']}")
    if rec["brief"]["true_peak_dbfs"] > -1.0:
        bad.append(f"tp {rec['brief']['true_peak_dbfs']}")
    if bad:
        raise SystemExit("NOT PASS: " + ", ".join(bad))
    print("PASS", rec["file"], rec["duration_s"], "s")


if __name__ == "__main__":
    main()
