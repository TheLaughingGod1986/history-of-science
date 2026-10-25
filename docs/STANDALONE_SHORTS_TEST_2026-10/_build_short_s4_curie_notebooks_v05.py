#!/usr/bin/env python3
"""HOS standalone S4 v05 (J0934, £0 local re-cut of vEg_tLIm0Co).

Frame 0 is the existing 003 Flow plate 02_wurzburg_lab_establishing_v03.mp4
(moving, about 3% black). No new TTS, Veo, Flow or Vertex. The uploaded v04
file is not touched.

VO is the recorded hos_sa_s4_curie_notebooks_vo_v01.wav. Sentence-1 gaps are
closed to 0.02 s so "still" lands by 1.5 s, and every later gap over 0.15 s
(including the 0.74 s breath after "radioactive." and the 0.46 s breath
before "polonium") is cut to 0.15 s of the same room tone.

    python3 _build_short_s4_curie_notebooks_v05.py
"""
from __future__ import annotations

import hashlib
import json
import math
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
SID, VER, JOB = "s4_curie_notebooks", "v05", "J0934"
AIR, YT = "2026-10-28", "vEg_tLIm0Co"
RAW_VO = HERE / "vo_v01/hos_sa_s4_curie_notebooks_vo_v01.wav"
STT = HERE / "vo_v01/stt/hos_sa_s4_curie_notebooks_vo_v01/stt_raw.json"
WORK = HERE / f"_work_{SID}_{VER}"
QA = HERE / "qa_shorts_v01" / f"hos_sa_{SID}_{VER}"
MUSIC = HERE / "05_Music"
W, H, FPS = 1080, 1920, 30
LOOP_S = 1.0
FIRST_CUT = 2.45
HOOK = "STILL **RADIOACTIVE**"
FONT = "/System/Library/Fonts/Supplemental/Didot.ttc"
CREAM, INK, YEL = (245, 232, 210, 255), (28, 26, 28, 255), (255, 214, 70, 255)
# (label, path under NAS_CLIPS, in-point). Frame 0 and the loop share the first plate.
PLATES = [
    ("lab", "02_wurzburg_lab_establishing_v03.mp4", 1.10),
    ("tube", "11_lab_hold_v01.mp4", 0.55),
    ("copy", "part04/06_labs_copy_tube_v03.mp4", 0.70),
    ("glow", "part02/05_glow_blooms_v02.mp4", 0.45),
    ("glass", "03_cathode_tube_hero_v02.mp4", 0.40),
    ("dark", "07_dark_on_purpose_v04.mp4", 0.50),
]


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


def lifted_vo(work: Path) -> tuple[Path, list[tuple[str, float, float]]]:
    """Squeeze sentence 1, cap later breaths at 0.15 s, keep the source room tone."""
    words = stt_words()
    pieces: list[tuple[float, float]] = []
    mapped: list[tuple[str, float, float]] = []
    pre = 0.08
    lead = max(0.0, words[0]["start"] - pre)
    pieces.append((lead, words[0]["start"]))
    cursor = words[0]["start"] - lead
    for i, w in enumerate(words):
        if i:
            prev = words[i - 1]
            raw = w["start"] - prev["end"]
            gap = 0.02 if i <= 5 else (0.15 if raw > 0.15 else raw)
            if raw <= gap + 0.004:
                pieces.append((prev["end"], w["start"]))
                cursor += raw
            else:
                pieces.append((prev["end"], prev["end"] + gap))
                cursor += gap
        dur = w["end"] - w["start"]
        mapped.append((w["text"], round(cursor, 3), round(cursor + dur, 3)))
        pieces.append((w["start"], w["end"]))
        cursor += dur
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
    return out, mapped


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


def band_mask() -> Path:
    """Feather the centre-band edges so the blur fill is not a hard split-panel seam."""
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


def seg(src: Path, dst: Path, start: float, dur: float) -> None:
    """16:9 plate, downscaled to the centre band, feathered onto a blurred fill. No Ken Burns."""
    if start + dur > probe(src) - 0.05:
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
       "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "16", "-r", str(FPS), str(dst))


def synth_bed(path: Path, dur: float, sr: int = 48000) -> None:
    """Glass-and-air pad. Distinct from the flask pulse and the heart-sum pad."""
    n = int(sr * dur)
    freqs = [98.00, 146.83, 196.00, 246.94, 392.00]
    amps = [0.28, 0.20, 0.14, 0.10, 0.06]
    frames = bytearray()
    for i in range(n):
        t = i / sr
        pulse = 0.86 + 0.14 * math.sin(2 * math.pi * (68 / 60) * t)
        env = min(1.0, t / 0.45) * min(1.0, max(0.0, (dur - t) / 0.4))
        l = r = 0.0
        for k, (f, a) in enumerate(zip(freqs, amps)):
            l += math.sin(2 * math.pi * f * t + 0.4 * k) * a
            r += math.sin(2 * math.pi * (f * 1.003) * t + 0.7 * k) * a
        g = env * pulse * 0.18
        frames += struct.pack("<hh", int(max(-1, min(1, l * g)) * 32767),
                              int(max(-1, min(1, r * g)) * 32767))
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(bytes(frames))


def place_sfx(total: float) -> Path:
    kit = HERE / "06_Sound-Effects" / "kit_v01"
    whoosh = kit / "sfx_hos_whoosh_soft_v01.wav"
    if not whoosh.exists():
        subprocess.run([sys.executable, str(OWB / "scripts/sfx_kit.py"), "make",
                        "--out-dir", str(kit), "--house", "hos"], check=True)
    dst = WORK / "sfx_stem.wav"
    ff("-f", "lavfi", "-t", f"{total:.3f}", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
       "-i", str(whoosh), "-filter_complex",
       "[1:a]volume=-16dB,afade=t=out:st=0.7:d=0.2[w];"
       "[0:a][w]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.5[a]",
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


def sound(vo: Path, total: float) -> dict:
    bed = MUSIC / f"hos_sa_{SID}_{VER}_bed.wav"
    synth_bed(bed, total + 0.3)
    plan = {
        "prompt": ("Quiet glass-and-air pad under a spoken radium fact, even, no chase. "
                   "Pace: 64-74 BPM. NOT the 001 flask pulse, NOT the 005 heart-sum pad, "
                   "NOT any Orbit With Ben bed, NOT a drum loop, NOT a trailer sting."),
        "film": "standalone-s4", "short": f"{SID}_{VER}", "job": JOB,
        "source": "own synthesis in _build_short_s4_curie_notebooks_v05.py, 0 credits",
    }
    bed.with_name(bed.stem + "_plan.json").write_text(json.dumps(plan, indent=2) + "\n")
    sfx = place_sfx(total)
    QA.mkdir(parents=True, exist_ok=True)
    bed_db, sfx_db = -8.0, -8.0
    audio = WORK / "audio.wav"
    level = {}
    for _ in range(5):
        mix(vo, bed, sfx, total, audio, bed_db, sfx_db)
        vo_stem, bed_stem, sfx_stem = WORK / "stem_vo.wav", WORK / "stem_bed.wav", WORK / "stem_sfx.wav"
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
    return {"audio": audio, "bed": bed, "level": level}


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
            differ = abs(r - r2) + abs(g - g2) + abs(bl - b2) > 80
            if differ and (cream or ink):
                mpix[x, y] = 255
    mask = mask.filter(ImageFilter.MaxFilter(5))
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


def body_plan(vo_s: float) -> list[dict]:
    n_body = len(PLATES)
    rest = vo_s - FIRST_CUT
    each = rest / (n_body - 1)
    if each > 3.5:
        raise SystemExit(f"hold {each:.2f}s over 3.5 (vo {vo_s:.2f})")
    if FIRST_CUT > 2.65:
        raise SystemExit(f"first cut {FIRST_CUT}")
    rows = []
    t = 0.0
    holds = [FIRST_CUT] + [each] * (n_body - 1)
    for (label, rel, ins), hold in zip(PLATES, holds):
        t1 = vo_s if label == PLATES[-1][0] else t + hold
        rows.append({"t0": round(t, 3), "t1": round(t1, 3), "rel": rel, "in_s": ins,
                     "label": label, "hold_s": round(t1 - t, 3)})
        t = t1
    rows.append({"t0": round(vo_s, 3), "t1": round(vo_s + LOOP_S, 3), "rel": PLATES[0][1],
                 "in_s": PLATES[0][2], "label": "loop", "hold_s": LOOP_S})
    return rows


def run_qa(mp4: Path, plan: list[dict]) -> dict:
    cuts, pool, seen = [], [], set()
    for k, row in enumerate(plan, 1):
        base = Path(row["rel"]).name
        src_id = f"loop_end_{base}" if row["label"] == "loop" else base
        cuts.append({"row": f"s{k:02d}_{row['label']}", "timeline_in": row["t0"], "timeline_out": row["t1"],
                     "source": src_id, "upscale": 0.84, "video": True,
                     "framing": {"offset": row["in_s"]}})
        if src_id not in seen:
            seen.add(src_id)
            pool.append({"file_id": src_id, "title": f"Flow Veo plate {base}"})
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
    return {"polish_gate": {"exit": r_pg.returncode, "tail": (r_pg.stdout + r_pg.stderr).strip().splitlines()[-6:]},
            "picture_qa": {"exit": r_pq.returncode, "tail": (r_pq.stdout + r_pq.stderr).strip().splitlines()[-8:]}}


def sheet_2fps(mp4: Path) -> Path:
    out = QA / f"{mp4.stem}_2fps_sheet.jpg"
    ff("-i", str(mp4), "-vf", "fps=2,scale=180:-2,tile=8x6", "-q:v", "4", str(out))
    return out


def copy_out(mp4: Path, phone: Path, sheet: Path) -> list[str]:
    uat = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT/standalone_s4_curie_v05"
    nas = Path("/Volumes/data/mac-mini-archive/YouTube/History Of Science/"
               "docs/STANDALONE_SHORTS_TEST_2026-10/s4_curie_notebooks_v05")
    copied = []
    for folder in (uat, nas):
        folder.mkdir(parents=True, exist_ok=True)
        for src in (mp4, phone, sheet):
            shutil.copy2(src, folder / src.name)
            copied.append(str(folder / src.name))
    return copied


def build() -> dict:
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    QA.mkdir(parents=True, exist_ok=True)
    for _, rel, _ in PLATES:
        if not (NAS_CLIPS / rel).exists():
            raise SystemExit(f"missing plate {NAS_CLIPS / rel}")
    vo, words = lifted_vo(WORK)
    spoken = " ".join(w for w, _, _ in words)
    (WORK / "spoken.txt").write_text(spoken + "\n")
    vo_s = probe(vo)
    total = round(vo_s + LOOP_S, 3)
    if not 18.0 <= total <= 24.05:
        raise SystemExit(f"duration {total}s outside 18–24 (vo {vo_s:.2f})")
    still_t = next(s for w, s, e in words if w.lower().startswith("still"))
    note_t = next(s for w, s, e in words if w.lower().startswith("notebook"))
    if words[0][1] > 0.15:
        raise SystemExit(f"first word at {words[0][1]}")
    if still_t > 1.50 or note_t > 1.50:
        raise SystemExit(f"claim late: notebooks {note_t} still {still_t}")
    plan = body_plan(vo_s)
    segs = []
    for k, row in enumerate(plan):
        src = NAS_CLIPS / row["rel"]
        out = WORK / f"seg_{k:02d}.mp4"
        seg(src, out, row["in_s"], row["hold_s"])
        segs.append(out)
    (WORK / "pic.txt").write_text("".join(f"file '{s.name}'\n" for s in segs))
    pic = WORK / "picture.mp4"
    ff("-f", "concat", "-safe", "0", "-i", "pic.txt", "-c:v", "libx264", "-pix_fmt", "yuv420p",
       "-preset", "fast", "-crf", "16", "-r", str(FPS), "-t", f"{total:.3f}", str(pic), cwd=WORK)
    ff("-i", str(pic), "-frames:v", "1", str(WORK / "frame0_pic.png"))

    snd = sound(vo, total)
    norm = WORK / "audio_norm.wav"
    ff("-i", str(snd["audio"]), "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-c:a", "pcm_s16le", str(norm))

    chunks = chunk_words(words)
    overlays = []
    hook_png = WORK / "cap_hook.png"
    hook_meta = render_hook(hook_png)
    overlays.append((hook_png, 0.0, 2.0))
    for i, c in enumerate(chunks):
        png = WORK / f"cap_{i:03d}.png"
        render_cap(png, c["text"])
        overlays.append((png, c["t0"], min(c["t1"], total - 0.05)))

    inputs = ["-i", str(pic), "-i", str(norm)]
    for png, *_ in overlays:
        inputs += ["-loop", "1", "-i", str(png)]
    fc, last = [], "[0:v]"
    for i, (_, t0, t1) in enumerate(overlays, 2):
        fc.append(f"{last}[{i}:v]overlay=0:0:enable='between(t,{t0:.3f},{t1:.3f})'[v{i}]")
        last = f"[v{i}]"
    mp4 = HERE / "shorts_v01" / f"hos_sa_{SID}_{VER}.mp4"
    ff(*inputs, "-filter_complex", ";".join(fc), "-map", last, "-map", "1:a",
       "-c:v", "libx264", "-pix_fmt", "yuv420p", "-profile:v", "high", "-preset", "medium", "-crf", "18",
       "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
       "-t", f"{total:.3f}", "-movflags", "+faststart", str(mp4))
    stamped = WORK / "stamped.mp4"
    nframes = int(round(total * FPS))
    ff("-i", str(mp4), "-loop", "1", "-i", str(WORK / "frame0_pic.png"), "-filter_complex",
       f"[1:v]scale={W}:{H},fps={FPS},format=yuv420p[f];"
       f"[0:v][f]overlay=enable='gte(n,{nframes - 2})'[v]",
       "-map", "[v]", "-map", "0:a", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "16",
       "-r", str(FPS), "-c:a", "copy", "-t", f"{total:.3f}", "-movflags", "+faststart", str(stamped))
    stamped.replace(mp4)

    diff = loop_diff(mp4)
    lufs, peak = integrated_lufs(mp4), true_peak(mp4)
    half_t = next(s for w, s, e in words if w.lower().startswith("half"))
    holds = [r["hold_s"] for r in plan if r["label"] != "loop"]
    brief = {
        "frame0_source": "003/04_Generated-Clips/02_wurzburg_lab_establishing_v03.mp4",
        "frame0_zoom": "none — moving Flow plate, in 1.10s, centre-band, no Ken Burns",
        "first_word_s": words[0][1],
        "surprise_s": {"notebooks": note_t, "still": still_t},
        "first_cut_s": plan[1]["t0"],
        "last_word_to_loop_s": round(total - words[-1][2], 3),
        "meta_promise": False,
        "runtime_s": round(probe(mp4), 3),
        "longest_hold_s": max(holds),
        "payoff_phrase": "lose half its strength",
        "payoff_s": half_t,
        "payoff_frac": round(half_t / total, 3),
        "loop_sentence": "Radium takes 1,600 years to lose half its strength. Marie Curie's notebooks are still radioactive.",
        "loop_diff": diff,
        "lufs": lufs,
        "true_peak_dbfs": peak,
        "frame0_black": black_frac(mp4, 0.2),
        "no_cta": True,
        "no_new_spend": True,
    }
    meta = {
        "id": SID, "version": VER, "job": JOB, "youtube_id": YT,
        "title": "Are Marie Curie's Notebooks Still Radioactive?",
        "air_date": AIR, "spoken": spoken, "script": spoken,
        "words": [{"word": w, "start": s, "end": e} for w, s, e in words],
        "word_count": len(words), "vo_s": round(vo_s, 3), "last_word_end_s": words[-1][2],
        "plan": plan, "hook": HOOK.replace("**", ""), "hook_layer": hook_meta,
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
        "file": mp4.name, "sha256": sha256(mp4), "duration_s": brief["runtime_s"],
        "spoken": spoken, "brief": brief, "gate_exit": gate.returncode,
        "gate_verdict": gate_json.get("verdict"), "gate_fails": gate_json.get("fails"),
        "gate_warns": gate_json.get("warns"), "qa": qa,
        "music_exit": music.returncode, "music_tail": (music.stdout + music.stderr).strip().splitlines()[-6:],
        "sfx": snd["level"], "copies": copies,
    }
    (QA / f"build_{SID}_{VER}.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({k: summary[k] for k in ("file", "duration_s", "gate_verdict", "gate_fails", "gate_warns",
                                              "qa", "music_exit", "music_tail", "sfx", "brief")}, indent=2))
    return summary


def main() -> None:
    rec = build()
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
    if rec["brief"]["loop_diff"] > 15:
        bad.append(f"loop_diff {rec['brief']['loop_diff']}")
    if rec["brief"]["frame0_black"] > 0.30:
        bad.append(f"black {rec['brief']['frame0_black']}")
    if rec["brief"]["payoff_frac"] < 0.70:
        bad.append(f"payoff {rec['brief']['payoff_frac']}")
    if bad:
        raise SystemExit("NOT PASS: " + ", ".join(bad))
    print("PASS", rec["file"], rec["duration_s"], "s")


if __name__ == "__main__":
    main()
