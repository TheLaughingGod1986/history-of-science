#!/usr/bin/env python3
"""HOS standalone story Shorts S1–S4 v01 (J0171): 9:16 from the Chief-KEEP still plates, VO, one bed, house SFX.

Chief rulings (HOS #180 6131411243, 6131594106): plates as kept (S1 runs 01–04 and loops to 01; S2 03–05 are the
v02 retakes; S3-05 is the v03 last take), one HOS standalone-Shorts bed under all four, pause-trim S1/S4 VO only.
v02 (Chief AMEND after watch, HOS #180 6132241581): S3 opens and ends on the handle-off plate (the handle never
returns); S4's archive plate is the no-hands v02 retake. S1/S2 stay v01.
SCRIPTS_v02: no 9–14 s long-title card and no "watch the full film" end card (the Shorts stand alone).
Each still moves with a smooth push (zoompan on a 4× upscale, so no wobble); frame 0 opens on a faster push with a
whoosh so the picture visibly changes by 1 s. Word captions all the way through (UK spelling), hook caption 0–2.6 s.

    python3 docs/STANDALONE_SHORTS_TEST_2026-10/_assemble_standalone_shorts_v01.py [--only s1 …]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
PL = HERE / "plates_v01"
VO = HERE / "vo_v01"
OUT = HERE / "shorts_v01"
WORK = HERE / "_work_shorts_v01"
BED = HERE / "music_v01/hos-standalone-shorts_score_bed_v01.mp3"
SFX = HERE / "sfx_kit_v01"
GATE = REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"
FONT = "/System/Library/Fonts/Supplemental/Didot.ttc"
W, H, FPS = 1080, 1920, 30
CREAM, INK, YEL = (245, 232, 210, 255), (28, 26, 28, 255), (255, 214, 70, 255)
TAIL_S, LOOP_S = 0.6, 2.6
PAUSE_CAP = 0.40
CHUNK_MAX_S, CHUNK_MAX_WORDS, CHUNK_MIN_S = 1.55, 4, 0.45
HOOK_CAP, HOOK_PITCH, UI_TOP = 0.09, 1.32, 0.75
HOOK_CAP_4LINE, HOOK_TOP_MIN = 0.08, 0.03
UK = [(re.compile(r"\b([Cc])olor"), r"\1olour"), (re.compile(r"\b([Mm])old"), r"\1ould")]

# S5–S8 (Chief, HOS #180 22:33Z/22:34Z/22:54Z): S5 drops 04 and lands "But the noise" on 02 again with a tighter
# push on the dial; S6-04 pushes in slowly on the mould so the clear ring fills the frame; S7-03 is the no-spend
# crop_no_flame (≥1.5× top-anchored, so the frame ends by 67% height, above the flame at ~72%); S8 runs 01–04.
# A beat's optional third item is its move: z (start, end), c (centre x, y as fractions), top (anchor at y=0).
DIAL_TIGHT = {"z": (1.60, 1.75), "c": (0.52, 0.60)}
RING_PUSH = {"z": (1.05, 1.35), "c": (0.505, 0.555)}
CROP_NO_FLAME = {"z": (1.50, 1.56), "c": (0.53, 0.0), "top": True}
COLUMN_TIGHT = {"z": (1.45, 1.60), "c": (0.545, 0.30)}

# beats: (word index the plate lands on, plate file[, move]). The "loop" beat starts LOOP_S before the end.
SHORTS = [
    {"id": "s1_herschel_infrared", "air_date": "2026-10-19", "hook": "HOTTER IN THE **DARK**",
     "vo": "hos_sa_s1_herschel_infrared_vo_v01", "trim": True,
     "beats": [(0, "s1/01_beyond_red_v01.jpg"), (10, "s1/02_prism_window_v01.jpg"),
               (17, "s1/03_thermometers_colours_v01.jpg"), (28, "s1/04_past_the_red_v01.jpg"),
               ("loop", "s1/01_beyond_red_v01.jpg")]},
    {"id": "s2_brand_phosphorus", "air_date": "2026-10-21", "hook": "BOILING URINE FOR **GOLD**",
     "vo": "hos_sa_s2_brand_phosphorus_vo_v02", "trim": False,
     "beats": [(0, "s2/01_glowing_flask_v01.jpg"), (9, "s2/02_hamburg_lab_v01.jpg"),
               (20, "s2/03_black_sludge_v02.jpg"), (28, "s2/04_no_gold_v02.jpg"),
               (30, "s2/05_first_glow_v02.jpg"), ("loop", "s2/01_glowing_flask_v01.jpg")]},
    {"id": "s3_snow_pump", "air_date": "2026-10-26", "hook": "THE KILLER **PUMP**",
     "vo": "hos_sa_s3_snow_pump_vo_v02", "trim": False,
     "ver": "v02", "beats": [(0, "s3/05_handle_off_v03.jpg"), (10, "s3/02_soho_1854_v01.jpg"),
               (23, "s3/03_snow_tracking_v01.jpg"), (31, "s3/04_map_bars_v01.jpg"),
               (39, "s3/05_handle_off_v03.jpg")]},
    {"id": "s4_curie_notebooks", "air_date": "2026-10-28", "hook": "STILL **RADIOACTIVE**",
     "vo": "hos_sa_s4_curie_notebooks_vo_v01", "trim": True, "ver": "v02",
     "beats": [(0, "s4/01_lead_box_v01.jpg"), (6, "s4/02_shed_lab_v01.jpg"), (18, "s4/03_glowing_vials_v01.jpg"),
               (23, "s4/04_bare_hands_v01.jpg"), (32, "s4/05_paris_archive_v02.jpg"),
               ("loop", "s4/01_lead_box_v01.jpg")]},
    {"id": "s5_penzias_pigeons", "air_date": "2026-11-02", "hook": "BLAMED THE **PIGEONS**",
     "vo": "hos_sa_s5_penzias_pigeons_vo_v01", "trim": True, "whoosh_db": -18.0,
     "beats": [(0, "s5/01_pigeons_horn_v01.jpg"), (12, "s5/02_receiver_needle_v01.jpg"),
               (26, "s5/03_nests_inside_v01.jpg"), (32, "s5/02_receiver_needle_v01.jpg", DIAL_TIGHT),
               (38, "s5/05_every_direction_v01.jpg"), ("loop", "s5/01_pigeons_horn_v01.jpg")]},
    {"id": "s6_fleming_mould", "air_date": "2026-11-04", "hook": "SAVED BY **MOULD**",
     "vo": "hos_sa_s6_fleming_mould_vo_v01", "trim": True, "bed_trim_db": -2.0,
     "beats": [(0, "s6/01_mouldy_dish_v01.jpg"), (8, "s6/02_back_from_holiday_v01.jpg"),
               (19, "s6/03_fuzzy_mould_v01.jpg"), (26, "s6/04_clear_ring_v01.jpg", RING_PUSH),
               (39, "s6/05_medicine_bottles_v01.jpg"), ("loop", "s6/01_mouldy_dish_v01.jpg")]},
    {"id": "s7_priestley_mint", "air_date": "2026-11-09", "hook": "MINT FIXED THE **AIR**",
     "vo": "hos_sa_s7_priestley_mint_vo_v01", "trim": True,
     "beats": [(0, "s7/01_candle_jar_v01.jpg"), (12, "s7/02_priestley_jar_v01.jpg"),
               (27, "s7/03_mint_sprig_v01.jpg", CROP_NO_FLAME), (38, "s7/04_candle_bright_v01.jpg"),
               ("loop", "s7/01_candle_jar_v01.jpg")]},
    {"id": "s8_hales_blood", "air_date": "2026-11-11", "hook": "BLOOD **EIGHT FEET** UP",
     "vo": "hos_sa_s8_hales_blood_vo_v01", "trim": True, "open_z": 1.55,
     "beats": [(0, "s8/01_tall_tube_v01.jpg"), (10, "s8/02_hales_sketch_v01.jpg"),
               (22, "s8/03_calm_mare_v01.jpg"), (31, "s8/04_taller_than_man_v01.jpg"),
               (38, "s8/04_taller_than_man_v01.jpg", COLUMN_TIGHT), ("loop", "s8/01_tall_tube_v01.jpg")]},
]


def ff(*a: str) -> None:
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *a], check=True)


def probe(p: Path) -> float:
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", str(p)], text=True))


def mean_db(p: Path) -> float:
    err = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(p), "-af", "volumedetect", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    return float(re.search(r"mean_volume: (-?[\d.]+)", err).group(1))


def uk(text: str) -> str:
    for pat, rep in UK:
        text = pat.sub(rep, text)
    return text


def stt_words(stem: str) -> list[list]:
    d = json.loads((VO / "stt" / stem / "stt_raw.json").read_text())
    return [[uk(w["text"]), w["start"], w["end"]] for w in d["words"] if w["type"] == "word"]


def pause_trim(src: Path, words: list[list], dst: Path) -> tuple[list[list], float]:
    """Cap every gap between words at PAUSE_CAP s; shift the word times to match."""
    keep, t, shift = [], 0.0, 0.0
    for k in range(len(words) - 1):
        gap = words[k + 1][1] - words[k][2]
        if gap > PAUSE_CAP:
            cut0 = words[k][2] + PAUSE_CAP / 2
            cut1 = words[k + 1][1] - PAUSE_CAP / 2
            keep.append((t, cut0))
            t = cut1
    keep.append((t, probe(src)))
    out = []
    for w in words:
        removed = sum(max(0.0, min(w[1], keep[i + 1][0]) - keep[i][1]) for i in range(len(keep) - 1))
        out.append([w[0], round(w[1] - removed, 3), round(w[2] - removed, 3)])
    parts = "".join(f"[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.01,"
                    f"afade=t=out:st={max(0.0, b - a - 0.01):.3f}:d=0.01[p{i}];" for i, (a, b) in enumerate(keep))
    ff("-i", str(src), "-filter_complex",
       parts + "".join(f"[p{i}]" for i in range(len(keep))) + f"concat=n={len(keep)}:v=0:a=1[a]",
       "-map", "[a]", "-c:a", "pcm_s16le", str(dst))
    return out, round(probe(src) - probe(dst), 3)


def chunk_words(words: list[list]) -> list[dict]:
    chunks, i, n = [], 0, len(words)
    while i < n:
        t0 = words[i][1]
        parts, t_end, j = [words[i][0]], words[i][2], i + 1
        while j < n:
            wj, sj, ej = words[j]
            if parts[-1][-1:] in ".?!:":
                break
            if parts[-1][-1:] in ",;" and len(parts) >= 2 and sj - t0 >= CHUNK_MIN_S:
                break
            if len(parts) >= CHUNK_MAX_WORDS and sj - t0 >= CHUNK_MIN_S:
                break
            if ej - t0 >= CHUNK_MAX_S and len(parts) >= 2:
                break
            parts.append(wj)
            t_end = ej
            j += 1
        t1 = words[j][1] if j < n else t_end + 0.3
        chunks.append({"text": " ".join(parts), "t0": round(t0, 3), "t1": round(t1, 3)})
        i = j
    return chunks


def render(path: Path, text: str, size: int, y: int) -> None:
    font = ImageFont.truetype(FONT, size, index=2)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    lines, cur = [], []
    for tok in text.split():
        if cur and font.getlength(" ".join(cur + [tok])) > W - 120:
            lines.append(cur)
            cur = [tok]
        else:
            cur.append(tok)
    lines.append(cur)
    asc, desc = font.getmetrics()
    lh = asc + desc + int(size * 0.1)
    cy = H - y - lh * len(lines)
    for line in lines:
        s = " ".join(line)
        draw.text(((W - font.getlength(s)) / 2, cy), s, font=font, fill=CREAM, stroke_width=4, stroke_fill=INK)
        cy += lh
    img.save(path)


def hook_layout(tokens: list[tuple], cap_target: float) -> tuple:
    size = 100
    while True:
        font = ImageFont.truetype(FONT, size, index=2)
        cap = -font.getbbox("H", anchor="ls")[1]
        if cap >= cap_target * H:
            break
        size += 1
    while max(font.getlength(t) for t, _ in tokens) > W - 100:
        size -= 2
        font = ImageFont.truetype(FONT, size, index=2)
        cap = -font.getbbox("H", anchor="ls")[1]
    lines: list[list] = []
    for tok in tokens:
        if lines and font.getlength(" ".join(t for t, _ in lines[-1] + [tok])) <= W - 100:
            lines[-1].append(tok)
        else:
            lines.append([tok])
    return size, font, cap, lines


def render_hook(path: Path, text: str) -> dict:
    tokens = [(w.strip("*"), w.startswith("**")) for w in text.split()]
    size, font, cap, lines = hook_layout(tokens, HOOK_CAP)
    if len(lines) >= 4:
        # A four-line block at 9% runs off the top edge (S7/S8 v01 frame 0); 8% is the house floor (rule 3.3).
        size, font, cap, lines = hook_layout(tokens, HOOK_CAP_4LINE)
    pitch = round(cap * HOOK_PITCH)
    block = pitch * (len(lines) - 1) + cap
    top = max(int(H * HOOK_TOP_MIN), int(H * 0.19) - block // 2)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    space = font.getlength(" ")
    for k, line in enumerate(lines):
        x = (W - font.getlength(" ".join(t for t, _ in line))) / 2
        for t, hot in line:
            draw.text((x, top + cap + k * pitch), t, font=font, anchor="ls", fill=YEL if hot else CREAM,
                      stroke_width=7, stroke_fill=INK)
            x += font.getlength(t) + space
    img.save(path)
    return {"font_size": size, "cap_pct": round(100 * cap / H, 2), "lines": len(lines),
            "block_pct": [round(100 * top / H, 1), round(100 * (top + block) / H, 1)]}


def seg(src: Path, dst: Path, dur: float, k: int, first: bool, move: dict | None = None,
        open_z: float = 1.40) -> None:
    """Smooth push on a still: zoompan over a 4× upscale (sub-pixel steps, no wobble)."""
    n = max(2, round(dur * FPS))
    x, y = "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"
    if move:
        z0, z1 = move["z"]
        z = f"{z0}+{z1 - z0:.4f}*on/{n}"
        cx, cy = move.get("c", (0.5, 0.5))
        x = f"max(0,min(iw-iw/zoom,{cx}*iw-iw/zoom/2))"
        y = "0" if move.get("top") else f"max(0,min(ih-ih/zoom,{cy}*ih-ih/zoom/2))"
    elif first:
        z = f"{open_z:.2f}-{open_z - 1.10:.2f}*min(on/{FPS * 1.0:.0f},1)-0.06*max(0,on-{FPS})/{n}"
    elif k % 2:
        z = f"1.0+0.07*on/{n}"
    else:
        z = f"1.07-0.07*on/{n}"
    vf = (f"scale={W * 4}:{H * 4}:flags=lanczos,zoompan=z='{z}':x='{x}':y='{y}'"
          f":d={n}:s={W}x{H}:fps={FPS},setsar=1,format=yuv420p")
    ff("-loop", "1", "-i", str(src), "-vf", vf, "-frames:v", str(n), "-c:v", "libx264", "-preset", "fast",
       "-crf", "17", "-r", str(FPS), str(dst))


def build(item: dict) -> dict:
    sid, ver = item["id"], item.get("ver", "v01")
    work = WORK / (sid if ver == "v01" else f"{sid}_{ver}")
    work.mkdir(parents=True, exist_ok=True)
    raw = VO / f"{item['vo']}.wav"
    words = stt_words(item["vo"])
    vo, trimmed = raw, 0.0
    if item["trim"]:
        vo = work / "vo_trim.wav"
        words, trimmed = pause_trim(raw, words, vo)
    total = round(words[-1][2] + TAIL_S, 3)
    if total > probe(vo) + TAIL_S + 0.05 or total >= 40:
        raise SystemExit(f"{sid}: bad length {total}")

    cuts = []
    for w, rel, *mv in item["beats"]:
        t = 0.0 if w == 0 else (total - LOOP_S if w == "loop" else max(0.0, words[w][1] - 0.12))
        cuts.append((round(t, 3), PL / rel, w, mv[0] if mv else None))
    plan, segs = [], []
    for k, (t, src, w, move) in enumerate(cuts):
        end = cuts[k + 1][0] if k + 1 < len(cuts) else total
        if end - t < 1.0:
            raise SystemExit(f"{sid}: beat {k} only {end - t:.2f} s")
        out = work / f"seg_{k:02d}.mp4"
        seg(src, out, end - t, k, k == 0, move, item.get("open_z", 1.40))
        segs.append(out)
        plan.append({"t0": t, "t1": round(end, 3), "plate": src.relative_to(HERE).as_posix(),
                     "lands_on": w if w in (0, "loop") else words[w][0], **({"move": move} if move else {})})
    (work / "pic.txt").write_text("".join(f"file '{s.name}'\n" for s in segs))
    pic = work / "picture.mp4"
    ff("-f", "concat", "-safe", "0", "-i", str(work / "pic.txt"), "-c:v", "libx264", "-pix_fmt", "yuv420p",
       "-preset", "fast", "-crf", "17", "-r", str(FPS), "-t", f"{total:.3f}", str(pic))

    bed_gain = (mean_db(vo) - 18.0) - mean_db(BED) + item.get("bed_trim_db", 0.0)
    whoosh_db = item.get("whoosh_db", -14.0)
    cut_times = [c[0] for c in cuts[1:]]
    sfx_in = ["-i", str(SFX / "sfx_hos_whoosh_soft_v01.wav")] + sum(
        (["-i", str(SFX / "sfx_hos_tick_ink_v01.wav")] for _ in cut_times), [])
    sfx_fc = f"[2:a]aformat=sample_rates=48000:channel_layouts=stereo,volume={whoosh_db:.1f}dB[s0];"
    for i, t in enumerate(cut_times, 1):
        ms = int(t * 1000)
        sfx_fc += (f"[{2 + i}:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=-24dB,"
                   f"adelay={ms}|{ms}[s{i}];")
    sfx_fc += "".join(f"[s{i}]" for i in range(len(cut_times) + 1)) + \
        f"amix=inputs={len(cut_times) + 1}:normalize=0:duration=longest,apad=whole_dur={total:.3f}[sfx];"
    audio = work / "audio.wav"
    ff("-i", str(vo), "-stream_loop", "-1", "-i", str(BED), *sfx_in, "-filter_complex",
       f"[0:a]aformat=sample_rates=48000:channel_layouts=stereo,apad=whole_dur={total:.3f}[v];"
       f"[1:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{total:.3f},asetpts=PTS-STARTPTS,"
       f"volume={bed_gain:.2f}dB,afade=t=in:d=0.05,afade=t=out:st={total - 0.25:.3f}:d=0.25[b];" + sfx_fc +
       "[v][b][sfx]amix=inputs=3:normalize=0:duration=first,"
       "loudnorm=I=-14:TP=-1.5:LRA=11[a]",
       "-map", "[a]", "-t", f"{total:.3f}", "-ar", "48000", "-c:a", "pcm_s16le", str(audio))

    chunks = chunk_words(words)
    overlays = []
    hook_png = work / "cap_hook.png"
    hook_meta = render_hook(hook_png, item["hook"])
    overlays.append((hook_png, 0.0, 2.6, "hook", item["hook"].replace("**", "")))
    for i, c in enumerate(chunks):
        png = work / f"cap_{i:03d}.png"
        render(png, c["text"], 82, 500)
        overlays.append((png, c["t0"], min(c["t1"], total - 0.05), "vo", c["text"]))
    inputs = ["-i", str(pic), "-i", str(audio)]
    for png, *_ in overlays:
        inputs += ["-loop", "1", "-i", str(png)]
    fc, last = [], "[0:v]"
    for i, (_, t0, t1, *_r) in enumerate(overlays, 2):
        fc.append(f"{last}[{i}:v]overlay=0:0:enable='between(t,{t0:.3f},{t1:.3f})'[v{i}]")
        last = f"[v{i}]"
    OUT.mkdir(exist_ok=True)
    mp4 = OUT / f"hos_sa_{sid}_{ver}.mp4"
    ff(*inputs, "-filter_complex", ";".join(fc), "-map", last, "-map", "1:a", "-c:v", "libx264",
       "-pix_fmt", "yuv420p", "-profile:v", "high", "-preset", "medium", "-crf", "18", "-r", str(FPS),
       "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", "-t", f"{total:.3f}", "-movflags", "+faststart",
       str(mp4))
    for tag, t in (("frame0", 0.0), ("t1s", 1.0), ("mid", total / 2), ("end", total - 0.1)):
        ff("-ss", f"{t:.3f}", "-i", str(mp4), "-frames:v", "1", "-q:v", "3", str(work / f"{tag}.jpg"))
    timeline = [{"role": r, "text": t, "t0": round(a, 3), "t1": round(b, 3)} for _, a, b, r, t in overlays]
    (work / "timeline.json").write_text(json.dumps({"plan": plan, "overlays": timeline}, indent=2) + "\n")
    return {"id": sid, "ver": ver, "work": work.relative_to(HERE).as_posix(), "air_date": item["air_date"], "file": mp4.relative_to(REPO).as_posix(),
            "sha256": hashlib.sha256(mp4.read_bytes()).hexdigest(), "duration_s": round(probe(mp4), 3),
            "vo": raw.name, "pause_trim_s": trimmed, "bed": BED.name, "bed_gain_db": round(bed_gain, 2),
            "hook": item["hook"].replace("**", ""), "hook_layer": hook_meta, "plan": plan,
            "captions": len(chunks),
            "sfx": {"whoosh_frame0": True, "whoosh_db": whoosh_db, "ticks_on_cuts": len(cut_times)}}


def sheet(recs: list[dict], name: str | None = None) -> Path:
    tags = ("frame0", "t1s", "mid", "end")
    tw, th = 216, 384
    img = Image.new("RGB", (tw * len(tags), th * len(recs)), (20, 20, 20))
    for r, rec in enumerate(recs):
        for c, tag in enumerate(tags):
            im = Image.open(HERE / rec.get("work", f"_work_shorts_v01/{rec['id']}") / f"{tag}.jpg").resize((tw, th))
            img.paste(im, (c * tw, r * th))
    p = OUT / (name or f"contact_sheet_{max(r.get('ver', 'v01') for r in recs)}.jpg")
    img.save(p, quality=88)
    return p


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*")
    ns = ap.parse_args()
    idx_p = HERE / "SHORTS_INDEX_v01.json"
    index = json.loads(idx_p.read_text()) if idx_p.exists() else {"job": "J0171", "shorts": {}}
    recs = []
    for item in SHORTS:
        if ns.only and not any(item["id"].startswith(o) for o in ns.only):
            continue
        rec = build(item)
        r = subprocess.run([sys.executable, str(GATE), "check", str(REPO / rec["file"]), "--air-date",
                            item["air_date"]], capture_output=True, text=True)
        rec["gate"] = {"exit": r.returncode, "output": (r.stdout + r.stderr).strip()[-1500:]}
        index["shorts"][item["id"]] = rec
        recs.append(rec)
        print(f"BUILT {item['id']} {rec['duration_s']} s trim {rec['pause_trim_s']} gate exit {r.returncode}")
        print(rec["gate"]["output"])
    if recs and ns.only:
        tag = "-".join(r["id"].split("_")[0] for r in recs)
        index.setdefault("contact_sheets", {})[tag] = sheet(
            recs, f"contact_sheet_{tag}_{max(r['ver'] for r in recs)}.jpg").relative_to(REPO).as_posix()
    elif recs:
        index["contact_sheet"] = sheet([index["shorts"][i["id"]] for i in SHORTS if i["id"] in index["shorts"]]
                                       ).relative_to(REPO).as_posix()
    idx_p.write_text(json.dumps(index, indent=2) + "\n")


if __name__ == "__main__":
    main()
