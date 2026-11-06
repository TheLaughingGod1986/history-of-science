#!/usr/bin/env python3
"""J2169 rebuild: HOS 006 Short B v02 and Short C v03. GBP0. No upload.

J2258 FIX on the v01/v02 masters. Existing plates and locked takes only.
Output is 1080x1920. The v01 files in Short_B/ and Short_C/ are left in place.
"""
import hashlib, json, math, subprocess, sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OWB = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
HOS = Path("/Users/benjaminoats/YouTube/History Of Science")
FILM = HOS / "02_Video-Projects/006_Trees-Are-Made-Of-Air"
OUT = Path("/Users/benjaminoats/_desk/renders/J2169")
NORM = OUT / "norm_1920"
INSERTS = FILM / "04_Generated-Clips/j2213_shorts_inserts"
NAS = Path("/Volumes/data/mac-mini-archive/hos-worktrees/2026-10-22/hos-006-trees/02_Video-Projects/006_Trees-Are-Made-Of-Air/04_Generated-Clips")
BED = FILM / "05_Music/trees006_score_bed_v01.mp3"
VO_B = Path("/Users/benjaminoats/_desk/006/shorts_vo_20261004/vo/t2_mint_fixed_vo_v03b.mp3")
VO_C = Path("/Users/benjaminoats/_desk/006/shorts_vo_20261004/vo/t3_bubbles_sunlight_vo_v01.mp3")
ALIGN_B = FILM / "10_Shorts/vo_20261004/t2_mint_fixed_vo_v03b_align.json"
ALIGN_C = FILM / "10_Shorts/vo_20261004/t3_bubbles_sunlight_vo_v01_align.json"
W, H, FPS = 1080, 1920, 24
FONT_PATH = "/System/Library/Fonts/Supplemental/Didot.ttc"
CREAM = (245, 232, 210, 255)
YELLOW = (246, 196, 69, 255)
INK = (20, 16, 14, 255)
# Didot Bold at 220px is an 8.2% cap on a 1920-tall frame, and each word fits
# the 1080 width. "REPAIRED" and "THE LIGHT" as single lines are wider than 1080
# at that cap, so the hook is one word per line.
HOOK_SIZE = 220
sys.path.insert(0, str(OWB / "scripts"))

CROP_720 = [656, 0, 608, 1080]  # 1280x720 plate after lanczos scale to 1920x1080
CROP_POT = [638, 0, 608, 1080]  # full-height window on the jar, was the tighter 460x818 crop


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit((r.stderr or r.stdout or f"fail {cmd[0]}")[-2500:])
    return r


def probe_dur(p):
    return float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
        text=True).strip())


def probe_frames(p):
    return int(subprocess.check_output(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames",
         "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", str(p)],
        text=True).strip())


def probe_wh(p):
    w, h = subprocess.check_output(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
         "-of", "csv=p=0", str(p)], text=True).strip().split(",")
    return int(w), int(h)


def span(name, inn, dur):
    start = int(math.ceil(inn * FPS - 1e-9))
    if name == "S01":
        n = int(math.ceil(dur * FPS - 1e-9))
    else:
        n = max(1, int(round(dur * FPS)))
    return start, n


def words_from_align(path, vo_hash):
    data = json.loads(path.read_text())
    if data.get("words"):
        words = [{"word": w["word"], "start": w["start"], "end": w["end"]} for w in data["words"]]
    else:
        words, buf, a, b = [], "", None, None
        chars = data["characters"]
        starts = data["character_start_times_seconds"]
        ends = data["character_end_times_seconds"]
        for ch, st, en in zip(chars, starts, ends):
            if str(ch).isspace():
                if buf:
                    words.append({"word": buf, "start": a, "end": b})
                    buf, a = "", None
            else:
                if a is None:
                    a = st
                buf += ch
                b = en
        if buf:
            words.append({"word": buf, "start": a, "end": b})
    return {"vo_sha256": vo_hash, "words": words,
            "note": "Word ends taken from the locked alignment. No spoken line was rewritten."}


def chunk_words(words):
    """House chunks: 2-5 words, break on a sentence end. From the 007 Short builder."""
    chunks, i, n = [], 0, len(words)
    max_s, max_n, min_s = 1.55, 5, 0.45
    while i < n:
        t0 = words[i]["start"]
        parts, t_end, j = [words[i]["word"]], words[i]["end"], i + 1
        while j < n:
            wj, sj, ej = words[j]["word"], words[j]["start"], words[j]["end"]
            if parts[-1][-1:] in ".?!":
                break
            if parts[-1][-1:] in ",;:" and sj - t0 >= min_s and (len(parts) >= 2 or wj[:1].isupper()):
                break
            if len(parts) >= max_n and sj - t0 >= min_s:
                break
            if ej - t0 >= max_s and len(parts) >= 2:
                break
            parts.append(wj)
            t_end = ej
            j += 1
        t1 = words[j]["start"] if j < n else t_end + 0.25
        chunks.append({"text": " ".join(parts), "t0": t0, "t1": max(t0 + 0.18, t1), "n": len(parts)})
        i = j
    return chunks


def prenorm(src: Path) -> Path:
    """Scale a 1280x720 plate to 1920x1080 so a 608-wide crop stays under 2.35x."""
    dest = NORM / (src.stem + "_1920.mp4")
    if dest.exists() and probe_wh(dest) == (1920, 1080) and probe_frames(dest) == probe_frames(src):
        return dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-an",
         "-vf", "scale=1920:1080:flags=lanczos,setsar=1",
         "-c:v", "libx264", "-bf", "0", "-crf", "16", "-preset", "veryfast", "-pix_fmt", "yuv420p",
         str(dest)])
    if probe_wh(dest) != (1920, 1080) or probe_frames(dest) != probe_frames(src):
        sys.exit(f"prenorm frame count changed {src.name}")
    return dest


def prepare_rows():
    raw = subprocess.check_output(["git", "-C", str(HOS), "show", "1ab1092b:jobs/reviews/J2189/PROPOSED_MAPPINGS.json"])
    mapping = json.loads(raw)
    by = {(r["short"], r["row"]): r for r in mapping["rows"]}
    pot = NAS / "part01/raw/v01/03_pot_jar_leaf_t1.mp4"
    pot_sha = "b1aaba6dbb36659388751fe942c5a7b367d35a9e181c3599a5cf8f4e7b6c96cb"

    def insert(name, digest):
        src = INSERTS / name
        if probe_wh(src) != (1280, 720):
            sys.exit(f"{name} is not 1280x720")
        return prenorm(src), digest

    b_s02, b_s02_sha = insert("short_b_s02_t01.mp4", "6dcdb7b1f92bb1a57bcfe13f11211f508eb1b3d20c26ca7b70aebef737bf99ad")
    b_s06, b_s06_sha = insert("short_b_s06_t01.mp4", "81bece1156b715f3f1189072a600ad19b22cf8f90306f63e16ebcd7aa13d2261")
    c_s01, c_s01_sha = insert("short_c_s01_t01.mp4", "14f9ca4a020dbe9326aa674961d81d59c5937498299524c79e59d1aae1ba8f51")
    c_s06, c_s06_sha = insert("short_c_s06_t01.mp4", "79eb35f53a7282662e97631c7a7595d278969cda7809a80508cbb4dc9e2a12e5")
    c_s07, c_s07_sha = insert("short_c_s07_t01.mp4", "ecf4b465a5e4509d6fb8512851eee64fa4f3c946b8bc0fe4271f4e71c9f9a2d5")
    c_s08, c_s08_sha = insert("short_c_s08_t01.mp4", "224e571e74ca12ab56792a0a61e42d6becb0cc6b9af99e6fddbebaee299bd4ea")
    # The cuts point at the prenormed file. The original hash is checked before the scale.
    originals = {
        b_s02: (INSERTS / "short_b_s02_t01.mp4", b_s02_sha),
        b_s06: (INSERTS / "short_b_s06_t01.mp4", b_s06_sha),
        c_s01: (INSERTS / "short_c_s01_t01.mp4", c_s01_sha),
        c_s06: (INSERTS / "short_c_s06_t01.mp4", c_s06_sha),
        c_s07: (INSERTS / "short_c_s07_t01.mp4", c_s07_sha),
        c_s08: (INSERTS / "short_c_s08_t01.mp4", c_s08_sha),
    }
    for norm, (src, digest) in originals.items():
        got = sha(src)
        if got != digest:
            sys.exit(f"original hash {src.name}: {got}")
        print("prenorm", norm.name, sha(norm)[:12], "from", digest[:12])

    rows = {
        "B": [
            # Offset 0 fails the open gate (frame diff 1.05, motion 5.1). Frame 33 is the
            # earliest 608-wide in-point that still clears it once the centred hook is on.
            ("S01", pot, pot_sha, 33 / FPS, 2.24, CROP_POT, "Veo scene: jar, leaf and pot"),
            ("S02", b_s02, sha(b_s02), 0.0, 3.38, CROP_720, "Veo scene: candle in a sealed jar"),
            ("S03", NAS / "part03/raw/v01/09_injured_air_t1.mp4", "23cc12c39387d6795072dda135139e6a589b93ede341c2f9ce89af016099adf5", 0.0, 3.78, [656, 0, 608, 1080], "Veo scene: flame dying in a jar"),
            ("S04", NAS / "part03/raw/v01/10_mint_jar_t1.mp4", "309957a192218bc7d1ff66a896adce207e18331a3f66a1f4b7d7acef84e52adf", 0.0, 3.62, [780, 0, 608, 1080], "Veo scene: mint sprig slid into a jar"),
            ("S05", NAS / "part03/raw/v01/11_candle_tall_t1.mp4", "3fe88ccf83a1eb65bbf59ee8bf75b605f72e03dc7204c6b6cef84a6ffbd06d28", 0.0, 78 / FPS, [840, 0, 608, 1080], "Veo scene: tall candle burning"),
            ("S06", b_s06, sha(b_s06), 0.0, 3.16, CROP_720, "Veo scene: candle and mint in one jar"),
            ("S07", NAS / "part03/raw/v01/01_soil_to_sky_t1.mp4", by[("Short_B", "S07")]["source_sha256"], 0.0, 91 / FPS, [600, 0, 608, 1080], "Veo scene: green plant and open sky"),
            ("loop_tail", pot, pot_sha, 33 / FPS, 1.0, CROP_POT, "Veo scene: jar, leaf and pot"),
        ],
        "C": [
            ("S01", c_s01, sha(c_s01), 0.0, 2.56, CROP_720, "Veo scene: leaf bubbling in sunlight"),
            ("S02", NAS / "part04/raw/v01/01_villa_t1.mp4", by[("Short_C", "S02")]["source_sha256"], 0.0, 3.12, [144, 0, 608, 1080], "Veo scene: a villa in daylight"),
            ("S03", NAS / "part04/raw/v01/03_plunge_leaf_t1.mp4", by[("Short_C", "S03")]["source_sha256"], 0.0, 3.12, [656, 0, 608, 1080], "Veo scene: a leaf lowered into water"),
            ("S04", NAS / "part04/raw/v01/04_sunny_window_t1.mp4", by[("Short_C", "S04")]["source_sha256"], 0.0, 3.20, [656, 0, 608, 1080], "Veo scene: jars by a sunny window"),
            ("S05", pot, pot_sha, 0.0, 2.96, [1120, 0, 608, 1080], "Veo scene: jar, leaf and pot"),
            # 107/24 = 4.458s, 83 frames. The clip has 190 frames, so 84 would run off the end.
            ("S06", c_s06, sha(c_s06), 107 / FPS, 83 / FPS, CROP_720, "Veo scene: jar in shade, bubbles stopped"),
            ("S07", c_s07, sha(c_s07), 0.0, 2.80, CROP_720, "Veo scene: jar moved back into sun"),
            # One extra frame so the shorter shade shot does not pull the return over the last word.
            ("S08", c_s08, sha(c_s08), 0.0, 70 / FPS, CROP_720, "Veo scene: sunlit leaf and rising bubbles"),
            ("loop_tail", c_s01, sha(c_s01), 0.0, 1.0, CROP_720, "Veo scene: leaf bubbling in sunlight"),
        ],
    }
    return rows


def font(size):
    return ImageFont.truetype(FONT_PATH, size, index=2)


def text_size(draw, text, fnt):
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0], box[3] - box[1]


def stroke_text(draw, xy, text, fnt, fill, stroke=3):
    x, y = xy
    for dx in range(-stroke, stroke + 1):
        for dy in range(-stroke, stroke + 1):
            if dx or dy:
                draw.text((x + dx, y + dy), text, font=fnt, fill=INK)
    draw.text((x, y), text, font=fnt, fill=fill)


def hook_plate(lines):
    """lines: list of (text, fill). Centred as a block. Cap stays in the 8-10% band."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    fnt = font(HOOK_SIZE)
    cap = text_size(draw, "H", fnt)[1]
    if not 0.08 * H <= cap <= 0.10 * H:
        sys.exit(f"hook cap {cap / H:.3f} outside 8-10%")
    gap = int(HOOK_SIZE * 0.16)
    metrics = [text_size(draw, text, fnt) for text, _ in lines]
    for w, _h in metrics:
        if w > W - 80:
            sys.exit(f"hook line wider than the frame: {w}")
    block = sum(h for _, h in metrics) + gap * (len(lines) - 1)
    y = (H - block) // 2
    for (text, fill), (w, h) in zip(lines, metrics):
        stroke_text(draw, ((W - w) / 2, y), text, fnt, fill, stroke=3)
        y += h + gap
    return im


def title_plate():
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    fnt = font(78)
    lines = ["The Willow Tree", "That Was Made of Air"]
    gap = 12
    metrics = [text_size(draw, line, fnt) for line in lines]
    y = 170
    for line, (w, h) in zip(lines, metrics):
        if w > W - 120:
            sys.exit(f"title wider than the frame: {line} {w}")
        stroke_text(draw, ((W - w) / 2, y), line, fnt, CREAM, stroke=3)
        y += h + gap
    return im


def wrap_lines(text, fnt, max_w):
    draw = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    words = text.split()
    lines, cur = [], []
    for word in words:
        trial = " ".join(cur + [word])
        if cur and text_size(draw, trial, fnt)[0] > max_w:
            lines.append(" ".join(cur))
            cur = [word]
        else:
            cur.append(word)
    if cur:
        lines.append(" ".join(cur))
    return lines


def caption_plate(text, fnt):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    lines = wrap_lines(text, fnt, W - 140)
    gap = 8
    metrics = [text_size(draw, line, fnt) for line in lines]
    block = sum(h for _, h in metrics) + gap * (len(lines) - 1)
    y = H - 340 - block
    for line, (w, h) in zip(lines, metrics):
        stroke_text(draw, ((W - w) / 2, y), line, fnt, CREAM, stroke=3)
        y += h + gap
    return im


def burn(picture, mix, chunks, hook, hook_end, loop_start, master):
    hook_im = hook_plate(hook)
    title_im = title_plate()
    cap_font = font(64)
    cache = {}
    blank = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    nframes = probe_frames(picture)

    def chunk_at(t):
        if t < hook_end or t >= loop_start:
            return None
        for c in chunks:
            if c["t0"] <= t < min(c["t1"], loop_start):
                return c["text"]
        return None

    cmd = ["ffmpeg", "-y", "-v", "error",
           "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "pipe:0",
           "-i", str(picture), "-i", str(mix),
           "-filter_complex", "[1:v][0:v]overlay=format=auto:shortest=1[v]",
           "-map", "[v]", "-map", "2:a",
           "-c:v", "libx264", "-bf", "0", "-crf", "18", "-preset", "veryfast", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "192k", str(master)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    shown = {"hook": 0, "title": 0, "cap": 0}
    try:
        for i in range(nframes):
            t = i / FPS
            frame = blank.copy()
            if t < hook_end:
                frame = Image.alpha_composite(frame, hook_im)
                shown["hook"] += 1
            else:
                text = chunk_at(t)
                if text:
                    if text not in cache:
                        cache[text] = caption_plate(text, cap_font)
                    frame = Image.alpha_composite(frame, cache[text])
                    shown["cap"] += 1
            if 9.0 <= t < 14.0:
                frame = Image.alpha_composite(frame, title_im)
                shown["title"] += 1
            proc.stdin.write(frame.tobytes())
    finally:
        proc.stdin.close()
        err = proc.stderr.read().decode()
        code = proc.wait()
    if code:
        sys.exit(err[-2000:] or f"caption overlay failed {code}")
    print("caption frames", shown, "chunk plates", len(cache))


def render_picture(label, rows, dest):
    cmd = ["ffmpeg", "-y", "-v", "error"]
    for row in rows:
        cmd += ["-i", str(row[1])]
    parts = []
    expect = 0
    for i, row in enumerate(rows):
        inn, dur, crop = row[3], row[4], row[5]
        x, y, w, h = crop
        sf, n = span(row[0], inn, dur)
        src_n = probe_frames(row[1])
        if sf + n > src_n:
            sys.exit(f"{label} {row[0]} needs frames {sf}:{sf + n} but source has {src_n}")
        expect += n
        parts.append(
            f"[{i}:v]trim=start_frame={sf}:end_frame={sf + n},setpts=PTS-STARTPTS,"
            f"crop={w}:{h}:{x}:{y},scale={W}:{H}:flags=lanczos,setsar=1,format=yuv420p[v{i}]"
        )
    concat = "".join(f"[v{i}]" for i in range(len(rows))) + f"concat=n={len(rows)}:v=1:a=0[v]"
    cmd += ["-filter_complex", ";".join(parts) + ";" + concat, "-map", "[v]",
            "-an", "-c:v", "libx264", "-bf", "0", "-crf", "16", "-preset", "veryfast",
            "-pix_fmt", "yuv420p", str(dest)]
    print("render", label, "frames", expect)
    run(cmd)
    got = probe_frames(dest)
    if got != expect:
        sys.exit(f"{label} picture frames {got} != {expect}")


def lufs(path):
    r = subprocess.run(["ffmpeg", "-nostats", "-hide_banner", "-i", str(path),
                        "-af", "ebur128=framelog=verbose", "-f", "null", "-"],
                       capture_output=True, text=True)
    import re
    m = re.findall(r"Integrated loudness:\s+I:\s+(-?[\d.]+) LUFS", r.stderr)
    if not m:
        sys.exit("no lufs " + path.name + r.stderr[-400:])
    return float(m[-1])


def build_audio(label, rows, vo, total, dest_dir):
    vo_wav = dest_dir / "vo.wav"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(vo),
         "-af", f"apad=whole_dur={total},loudnorm=I=-16:TP=-2.5:LRA=11",
         "-t", str(total), "-ar", "48000", "-ac", "2", str(vo_wav)])
    vo_i = lufs(vo_wav)
    bed_wav = dest_dir / "bed.wav"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(BED), "-t", str(total), "-ar", "48000", "-ac", "2", str(bed_wav)])
    bed_i = lufs(bed_wav)
    bed_out = dest_dir / "bed_level.wav"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(bed_wav), "-af", f"volume={vo_i - 16 - bed_i}dB", str(bed_out)])
    kit = dest_dir / "sfx_kit"
    run([sys.executable, str(OWB / "scripts/sfx_kit.py"), "make", "--out-dir", str(kit), "--house", "hos"])
    whoosh = kit / "sfx_hos_whoosh_soft_v01.wav"
    tick = kit / "sfx_hos_tick_ink_v01.wav"
    cuts = []
    t = 0.0
    for row in rows:
        if t > 0.2:
            cuts.append(t)
        t += row[4]
    delays = ["[1:a]adelay=0|0,volume=-6dB[w]"]
    mix_in = ["[w]"]
    cmd = ["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-t", str(total), "-i",
           "anullsrc=channel_layout=stereo:sample_rate=48000", "-i", str(whoosh)]
    for i, ct in enumerate(cuts):
        cmd += ["-i", str(tick)]
        ms = int(round(ct * 1000))
        delays.append(f"[{i + 2}:a]adelay={ms}|{ms},volume=-4dB[t{i}]")
        mix_in.append(f"[t{i}]")
    filt = ";".join(delays) + ";" + "".join(mix_in) + f"amix=inputs={len(mix_in)}:normalize=0:duration=first[a]"
    sfx = dest_dir / "sfx.wav"
    cmd += ["-filter_complex", filt, "-map", "[a]", "-t", str(total), "-ar", "48000", "-ac", "2", str(sfx)]
    run(cmd)
    sfx_i = lufs(sfx)
    sfx_out = dest_dir / "sfx_level.wav"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(sfx), "-af", f"volume={vo_i - 18 - sfx_i}dB", str(sfx_out)])
    mix = dest_dir / "mix.wav"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(vo_wav), "-i", str(bed_out), "-i", str(sfx_out),
         "-filter_complex", "[0:a][1:a][2:a]amix=inputs=3:normalize=0:duration=first,loudnorm=I=-14:TP=-2.0:LRA=11[a]",
         "-map", "[a]", "-ar", "48000", "-ac", "2", str(mix)])
    return vo_wav, sfx_out, bed_out, mix


def cuts_json(rows):
    out = []
    t_frames = 0
    for row in rows:
        name, path, digest, inn, dur, crop, title = row
        x, y, w, h = crop
        sf, n = span(name, inn, dur)
        item = {
            "row": name,
            "source": str(path.resolve()),
            "video": True,
            "spoken": "",
            "timeline_in": t_frames / FPS,
            "timeline_out": (t_frames + n) / FPS,
            "upscale": round(W / w, 6),
            "framing": {"offset": sf / FPS, "crop": [int(x), int(y), int(w), int(h)], "output": [W, H]},
            "title_hint": title,
        }
        if name == "loop_tail":
            item["role"] = "prescribed_terminal_loop"
        out.append(item)
        t_frames += n
    return out


def pool_json(rows):
    items, seen = [], set()
    for row in rows:
        stem = Path(row[1]).stem
        if stem in seen:
            continue
        seen.add(stem)
        items.append({"id": stem, "file": Path(row[1]).name, "title": row[6]})
    return items


def coverage(chunks, words, hook_end, loop_start):
    missing = []
    for w in words:
        if w["end"] <= hook_end or w["start"] >= loop_start:
            continue
        mid = (max(w["start"], hook_end) + min(w["end"], loop_start)) / 2
        if not any(c["t0"] <= mid < min(c["t1"], loop_start) for c in chunks):
            missing.append(w["word"])
    band = [w["word"] for w in words if 9.0 <= w["start"] < 14.0]
    band_missing = [w for w in band if w in missing]
    return missing, band, band_missing


def main():
    recipe = OUT / "RECIPE_v02.md"
    recipe.write_text("""# J2169 v02 assembly

Short B v02 uses locked take t2_mint_fixed_vo_v03b. Sentence 1 is "A sprig of mint repaired the air." This is not the soil take.

Short C v03 uses locked take t3_bubbles_sunlight_vo_v01.

Output is 1080x1920. The six 1280x720 Flow plates are scaled to 1920x1080 with lanczos first, then cropped 608x1080, so the upscale into the frame is 1.776. The v01 masters at 720x1280 are kept.

Short C's opening and return both start at source time 0. That plate is already moving. Short B's pot plate is an ease-in at time 0: the open gate measured frame diff 1.05 and motion 5.1, under the 1.50 fail and the 10 warn. Both B rows therefore start at frame 33 (1.375 s), the earliest 608-wide in-point that still clears the gate once the centred hook is on the picture. The checker samples the opening and the return at that shared in-point and one frame before the return ends, and fails if those frames differ from the source by more than 8. A dissolve on the last part of the return would change that last frame, so this cut does not add one.

Short B cuts: the candle row ends at 16.292s, before "bright". The mint-and-candle row ends at 19.458s, before "the". The sky row takes the extra frame so the film stays 24.250s.

Short C shade row starts at 4.458s of short_c_s06_t01 (frame 107) and uses the 83 frames that remain. The sunlit-leaf row is one frame longer so the return still starts after the last word.

The frame-0 hook is Didot Bold, one word per line, cap about 8.2% of the frame, centred. Cream on the setup words, yellow on the hook words. Spoken captions are Didot cream chunks of a few words, including through the 9-14s title. The title is The Willow Tree / That Was Made of Air.

No generation, no upload. Long id VbPubYd6Fbs is not a publish instruction. Standalone S7 stays planned and is not built. Short A, s04, s05, s06, s07 and s08 are not built.
""")
    print("preparing rows")
    rows_all = prepare_rows()
    vo_map = {
        "B": (VO_B, "0f1099262037b62ea2b2a003ce86e196458fa983e9ca97877afb5600e97c7479", ALIGN_B,
              [("MINT", CREAM), ("FIXED", CREAM), ("THE", YELLOW), ("AIR", YELLOW)], "v02"),
        "C": (VO_C, "5b5d84e560d51ed9ad6f9bf5588f458802620f48f008b9409c532f8a1ea4e269", ALIGN_C,
              [("ONLY", CREAM), ("IN", CREAM), ("THE", YELLOW), ("LIGHT", YELLOW)], "v03"),
    }
    only = [a.upper() for a in sys.argv[1:]] or ["B", "C"]
    for label, rows in rows_all.items():
        if label not in only:
            continue
        t = 0.0
        for row in rows:
            name, path, expect, inn, dur, crop, _title = row
            got = sha(path)
            if got != expect:
                sys.exit(f"hash mismatch {label} {name}: {got}")
            if probe_dur(path) + 1e-3 < inn + dur:
                sys.exit(f"too short {label} {name}: need {inn + dur:.3f} have {probe_dur(path):.3f}")
            x, y, w, h = crop
            sw, sh = probe_wh(path)
            if x < 0 or y < 0 or x + w > sw or y + h > sh or w != 608 or h != 1080:
                sys.exit(f"bad crop {label} {name} {crop} on {sw}x{sh}")
            if W / w > 2.35:
                sys.exit(f"upscale {label} {name}")
            t += dur
        print(label, "duration nominal", round(t, 3))
        vo, vo_hash, align, hook, version = vo_map[label]
        if sha(vo) != vo_hash:
            sys.exit(f"VO hash {label}")
        dest = OUT / f"Short_{label}_{version}"
        dest.mkdir(parents=True, exist_ok=True)
        words = words_from_align(align, vo_hash)
        (dest / "words.json").write_text(json.dumps(words, indent=2) + "\n")
        picture = dest / "picture.mp4"
        cuts = cuts_json(rows)
        (dest / "cuts.json").write_text(json.dumps(cuts, indent=2) + "\n")
        (dest / "pool.json").write_text(json.dumps(pool_json(rows), indent=2) + "\n")
        total = cuts[-1]["timeline_out"]
        loop_start = cuts[-1]["timeline_in"]
        hook_end = cuts[0]["timeline_out"]
        last = words["words"][-1]["end"]
        if last > loop_start + 1e-6:
            sys.exit(f"{label} last word {last} overlaps the return at {loop_start}")
        body = [w for w in words["words"] if w["start"] >= hook_end - 1e-6]
        chunks = chunk_words(body)
        for c in chunks:
            if c["n"] > 5:
                sys.exit(f"chunk too long {c}")
        missing, band, band_missing = coverage(chunks, words["words"], hook_end, loop_start)
        print(label, "hook_end", round(hook_end, 3), "loop", round(loop_start, 3),
              "chunks", len(chunks), "missing", missing, "band", band)
        if missing or band_missing:
            sys.exit(f"{label} caption gap {missing}")
        (dest / "chunks.json").write_text(json.dumps(chunks, indent=2) + "\n")
        contract = {
            "version": 1, "format": "short", "cut": len(cuts) - 1, "duration": total,
            "last_vo_word": last,
            "prescription": {"path": str(recipe.resolve()), "sha256": sha(recipe)},
            "words": {"path": str((dest / "words.json").resolve()), "sha256": sha(dest / "words.json")},
            "vo": {"path": str(vo.resolve()), "sha256": vo_hash},
            "source": {"path": str(Path(cuts[0]["source"]).resolve()), "sha256": sha(cuts[0]["source"])},
            "source_in": cuts[-1]["framing"]["offset"],
            "source_out": cuts[-1]["framing"]["offset"] + (cuts[-1]["timeline_out"] - cuts[-1]["timeline_in"]),
            "framing": {"crop": cuts[0]["framing"]["crop"], "output": [W, H]},
        }
        (dest / "contract.json").write_text(json.dumps(contract, indent=2) + "\n")
        from terminal_loop import validate
        pre = validate(cuts, contract)
        print(label, "preflight", pre["status"], pre["errors"])
        if pre["status"] != "source_preflight":
            sys.exit(f"{label} preflight failed")
        if not (picture.exists() and picture.stat().st_size > 1_000_000 and probe_frames(picture) == int(round(total * FPS))):
            render_picture(label, rows, picture)
        vo_wav = dest / "vo.wav"
        mix = dest / "mix.wav"
        if not (mix.exists() and vo_wav.exists() and abs(probe_dur(mix) - total) < 0.05):
            vo_wav, sfx_wav, bed_wav, mix = build_audio(label, rows, vo, total, dest)
        else:
            sfx_wav, bed_wav = dest / "sfx_level.wav", dest / "bed_level.wav"
        master = dest / f"hos006_short_{label.lower()}_{version}.mp4"
        if not (master.exists() and master.stat().st_size > 1_000_000 and probe_frames(master) == probe_frames(picture)):
            burn(picture, mix, chunks, hook, hook_end, loop_start, master)
        print("master", master.name, "dur", round(probe_dur(master), 3), "frames", probe_frames(master))
        for video, tag in ((picture, "picture"), (master, "master")):
            qa_dir = dest / f"picture_qa_{tag}"
            qa_dir.mkdir(exist_ok=True)
            r = subprocess.run([sys.executable, str(OWB / "scripts/picture_qa.py"), str(video),
                                "--cuts", str(dest / "cuts.json"), "--pool", str(dest / "pool.json"),
                                "--terminal-loop", str(dest / "contract.json"), "--out-dir", str(qa_dir)])
            print(label, tag, "picture_qa", r.returncode)
            if r.returncode:
                sys.exit(f"{label} {tag} picture_qa failed")
        r = subprocess.run([sys.executable, str(OWB / "scripts/polish_gate.py"), str(master),
                            "--cuts", str(dest / "cuts.json"), "--out", str(dest / "polish_gate.json")])
        print(label, "polish", r.returncode)
        if r.returncode:
            sys.exit(f"{label} polish failed")
        r = subprocess.run([sys.executable, str(OWB / "scripts/sfx_kit.py"), "level",
                            "--vo", str(vo_wav), "--sfx", str(sfx_wav), "--bed", str(bed_wav),
                            "--minutes", str(total / 60), "--out", str(dest / "sfx_level.json")])
        print(label, "sfx", r.returncode)
        if r.returncode:
            sys.exit(f"{label} sfx failed")
        r = subprocess.run([sys.executable, str(OWB / "scripts/music_gate.py"), str(FILM),
                            "--bed", str(BED), "--video", str(master), "--out", str(dest / "music_gate.json")])
        print(label, "music", r.returncode)
        if r.returncode:
            sys.exit(f"{label} music failed")
        gate = HOS / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"
        air = "2026-11-18" if label == "B" else "2026-11-21"
        script = dest / "spoken.txt"
        script.write_text(" ".join(w["word"] for w in words["words"]) + "\n")
        r = subprocess.run([sys.executable, str(gate), "check", str(master), "--air-date", air,
                            "--script", str(script), "--vo", str(vo), "--json"], cwd=str(HOS),
                           capture_output=True, text=True)
        (dest / "gate_shorts.json").write_text((r.stdout or "") + (r.stderr or ""))
        print(label, "gate", r.returncode)
        if r.returncode:
            print((r.stdout or "")[-1500:], (r.stderr or "")[-800:])
            sys.exit(f"{label} shorts gate failed")
        fz = subprocess.run(["ffmpeg", "-v", "info", "-i", str(master),
                             "-vf", "freezedetect=n=0.003:d=0.5", "-f", "null", "-"],
                            capture_output=True, text=True)
        freezes = [line for line in fz.stderr.splitlines() if "freeze" in line.lower()]
        (dest / "freezedetect.txt").write_text("\n".join(freezes) + "\n")
        print(label, "freezes", len(freezes))
        man = {
            "job": "J2169", "short": label, "version": version, "master": str(master),
            "sha256": sha(master), "picture": str(picture), "picture_sha256": sha(picture),
            "duration_s": probe_dur(master), "frames": probe_frames(master),
            "size": [W, H], "vo_sha256": vo_hash, "long": "VbPubYd6Fbs",
            "watched": False, "heard": False, "approved": False,
        }
        (dest / "MANIFEST.json").write_text(json.dumps(man, indent=2) + "\n")
        print(json.dumps(man, indent=2))


if __name__ == "__main__":
    main()
