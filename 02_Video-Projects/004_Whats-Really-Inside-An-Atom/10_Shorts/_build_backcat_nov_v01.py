#!/usr/bin/env python3
"""HOS back-catalogue Shorts for the week of 29 Oct: Sun 1 Nov → 004 (gold foil), Tue 3 Nov → 002 (four elements).

Claude's approval with fixes, desk PR #180 comment 5950150517. Scripts: each film's
`10_Shorts/SHORTS_SCRIPTS_BACKCAT_v02.md` (word for word). The 005 Shorts v02 pipeline
(`005_…/10_Shorts/_build_shorts_v02.py`): Ben Orbit Narrator at settings_for_part(1), the long's
VO finish step 1 (no atempo), KEEP plates cut to the words, the frame-0 hook at rules §3.3
(9% cap, one word per line, centred), word captions, the promoted long's exact title at 9–14 s,
a loop back to the opening picture with the CTA. Then caption-change check, gate_shorts_open,
vo_check, freezedetect, frame-0/title stills and the iCloud phone copy.

Media is read from and written to the main checkout (never git); this script and the index are the record.

    python3 _build_backcat_nov_v01.py vo <short> [--take a]
    python3 _build_backcat_nov_v01.py finish <short> --take a
    python3 _build_backcat_nov_v01.py build [<short> …] [--no-icloud]

short ∈ 004_gold_foil, 002_four_elements
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
MEDIA = Path("/Users/benjaminoats/YouTube/History Of Science")
VENV_PY = MEDIA / "02_Video-Projects/001_How-Did-We-Discover-Germs/10_Shorts/_venv/bin/python"
VO_PY = Path.home() / ".venvs/hos-vo/bin/python"
GATES = {"main": REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py",
         "pr189_library": Path("/Users/benjaminoats/YouTube/hos-gate-lib/00_Brand/Channel-Setup/tools/gate_shorts_open.py")}
VO_CHECK = REPO / "00_Brand/Channel-Setup/tools/vo_check.py"
GERMS_ENV = MEDIA / "02_Video-Projects/001_How-Did-We-Discover-Germs/07_Edit-Project/.env"
ICLOUD_ROOT = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT"
FONT = "/System/Library/Fonts/Supplemental/Didot.ttc"
CTA_FONT = "/System/Library/Fonts/Supplemental/Times New Roman.ttf"
W, H, FPS = 1080, 1920, 30
CREAM, INK, YEL = (245, 232, 210, 255), (28, 26, 28, 255), (255, 214, 70, 255)
TITLE_IN, TITLE_OUT = 9.0, 14.0
LOOP_MIN_S = 2.0          # the opening picture returns for this long after the last word
LOOP_FLOOR_S = 1.5
MAX_TOTAL_S = 26.95
CHUNK_MAX_S, CHUNK_MAX_WORDS, CHUNK_MIN_S = 1.55, 5, 0.45
HOOK_CAP = 0.09           # hook cap height, fraction of H (rules §3.3: 8–10%)
HOOK_CAP_MIN = 0.08
HOOK_PITCH = 1.32
HOOK_FALLBACK = "/System/Library/Fonts/Supplemental/Bodoni 72.ttc"
HOOK_SQUEEZE_MIN = 0.90
UI_TOP = 0.75
VER = "v01"

P004 = MEDIA / "02_Video-Projects/004_Whats-Really-Inside-An-Atom"
P002 = MEDIA / "02_Video-Projects/002_How-Did-We-Discover-The-Periodic-Table"
A004 = P004 / "04_Generated-Clips/part04/raw/v01"
A002 = P002 / "04_Generated-Clips/part01/raw/v01_fast"
LAV = P002 / "04_Generated-Clips/shorts_backcat/raw/lavoisier_list_t1.mp4"   # KEEP head only: candle from ~3.0 s

# beats: (word index the plate lands on, plate, in-point s, crop x on 1920×1080, sha256 prefix[, max out-point s]).
# The last beat is the loop: the opening picture returns after the last word, for LOOP_MIN_S (less, down to
# LOOP_FLOOR_S, only when that is what keeps the Short under 27 s).
SHORTS = {
    "004_gold_foil": {
        "film": P004, "repo_film": REPO / "02_Video-Projects/004_Whats-Really-Inside-An-Atom",
        "slug": "hos_004_backcat_gold_foil", "air_date": "2026-11-01",
        "title": "What's Really Inside an Atom?", "promotes": "GHZDsiH7L7A",
        "short_title": "Why Gold Foil Bounced Rutherford's Particles Back",
        "hook": "IT CAME **BACK**",
        "bed": P004 / "05_Music/hos004-part04-temp_score_bed_v01.mp3",
        "icloud": "004_Whats-Really-Inside-An-Atom/10_Shorts",
        "beats": [(0, A004 / "12_shell_comes_back_v02.mp4", 1.5, 560, "3764483d"),
                  (7, A004 / "03_fire_at_gold_v01.mp4", 0.5, 640, "d64e1b33"),        # In nineteen-oh-nine…
                  (19, A004 / "09_almost_all_pass_v02.mp4", 3.0, 520, "c73023c9"),    # Almost all went straight through.
                  (24, A004 / "07_green_flash_count_v02.mp4", 0.1, 656, "3c388ef1", 3.5),  # About one in eight thousand…
                  (31, A004 / "11_shell_tissue_v02.mp4", 1.2, 900, "78ee7164"),       # Rutherford said…
                  (49, A004 / "13_mass_packed_v02.mp4", 2.55, 656, "a770491d"),        # An atom's mass…
                  ("loop", A004 / "12_shell_comes_back_v02.mp4", 1.5, 560, "3764483d")]},
    "002_four_elements": {
        "film": P002, "repo_film": REPO / "02_Video-Projects/002_How-Did-We-Discover-The-Periodic-Table",
        "slug": "hos_002_backcat_four_elements", "air_date": "2026-11-03",
        "title": "How Did We Discover the Periodic Table?", "promotes": "AL_-qlWko_g",
        "short_title": "The Four Elements Were Wrong",
        "hook": "NOT **ELEMENTS**",
        "bed": P002 / "05_Music/hos_002_part01_curious_workshop_v02_norm.wav",
        "icloud": "002_How-Did-We-Discover-The-Periodic-Table/10_Shorts",
        "beats": [(0, A002 / "03_four_elements_crumble_v01.mp4", 1.1, 656, "57618639"),
                  (7, A002 / "04_iron_salt_flame_air_v01.mp4", 0.3, 250, "a0bc722b"),   # For two thousand years…
                  (19, A002 / "10_rock_not_fire_v01.mp4", 0.3, 300, "053c5999"),        # But heat a rock…
                  (29, A002 / "02_workshop_jars_v01.mp4", 0.5, 760, "52689953"),        # Air is a mixture…
                  (36, LAV, 0.1, 430, None, 2.85),                                      # Antoine Lavoisier threw out the four,
                  (42, A002 / "08_labelled_zoo_v01.mp4", 1.0, 700, "d6c31fae"),         # and listed only what couldn't…
                  (50, A002 / "07_shelf_names_grow_v01.mp4", 0.5, 656, "9817941e"),     # His list had thirty-three.
                  ("loop", A002 / "03_four_elements_crumble_v01.mp4", 1.1, 656, "57618639")]},
}


def reexec_venv() -> None:
    if VENV_PY.exists() and Path(sys.executable) != VENV_PY:
        os.execv(str(VENV_PY), [str(VENV_PY), str(Path(__file__).resolve()), *sys.argv[1:]])


def ff(*a: str, cwd: Path | None = None) -> None:
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *a], check=True, cwd=cwd)


def probe(p: Path) -> float:
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", str(p)], text=True))


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def volstats(p: Path) -> tuple[float, float]:
    err = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(p), "-af", "volumedetect", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    return (float(re.search(r"mean_volume: (-?[\d.]+)", err).group(1)),
            float(re.search(r"max_volume: (-?[\d.]+)", err).group(1)))


def vo_dir(item: dict) -> Path:
    return item["film"] / "10_Shorts/vo_backcat_v01"


def script_text(item: dict) -> str:
    md = (item["repo_film"] / "10_Shorts/SHORTS_SCRIPTS_BACKCAT_v02.md").read_text(encoding="utf-8")
    m = re.search(r"\*\*Script \((\d+) words\):\*\*\s*\n\s*\n(.+?)\n\s*\n", md, flags=re.S)
    if not m:
        raise SystemExit("no Script paragraph")
    text = " ".join(m.group(2).split())
    if len(text.split()) != int(m.group(1)):
        raise SystemExit(f"{len(text.split())} words, script says {m.group(1)}")
    return text


# ── VO ────────────────────────────────────────────────────────────────────────────────────────────

def cmd_vo(sid: str, take: str) -> None:
    item = SHORTS[sid]
    sys.path.insert(0, str(REPO / "04_Audio" / "tools"))
    from el_auth import load_token
    from el_client import request
    from orbit_gemini_veo import load_dotenv
    from orbit_voice import MODEL_ID, VOICE_ID, settings_for_part
    if GERMS_ENV.exists():
        load_dotenv(GERMS_ENV)
    token, mode = load_token(prefer_api_key=True)
    vs = settings_for_part(1)
    print(f"auth={mode} voice={VOICE_ID} model={MODEL_ID} speed={vs['speed']}", flush=True)
    out = vo_dir(item)
    out.mkdir(parents=True, exist_ok=True)
    text = script_text(item)
    (out / f"{sid}.txt").write_text(text + "\n", encoding="utf-8")
    stem = f"{item['slug']}_vo_v01{take}"
    mp3, wav, align = out / f"{stem}.mp3", out / f"{stem}.wav", out / f"{stem}_align.json"
    code, body, _ = request("POST", f"/v1/text-to-speech/{VOICE_ID}/with-timestamps", token, mode,
                            data={"text": text, "model_id": MODEL_ID, "voice_settings": vs},
                            query="output_format=mp3_44100_128", accept="application/json", timeout=300)
    if code != 200:
        raise SystemExit(f"TTS failed {code}: {body[:300]!r}")
    payload = json.loads(body.decode())
    mp3.write_bytes(base64.b64decode(payload["audio_base64"]))
    align.write_text(json.dumps(payload.get("alignment") or payload.get("normalized_alignment") or {}, indent=1))
    ff("-i", str(mp3), "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", str(wav))
    mean, peak = volstats(wav)
    meta_p = out / "VO_BACKCAT_v01.json"
    meta = json.loads(meta_p.read_text()) if meta_p.exists() else {
        "voice": "Ben Orbit Narrator", "voice_id": VOICE_ID, "model_id": MODEL_ID, "voice_settings": vs, "takes": []}
    meta["takes"].append({"id": sid, "take": take, "words": len(text.split()), "mp3": mp3.name,
                          "mp3_sha256": sha256(mp3), "duration_s": round(probe(wav), 3), "mean_db": mean,
                          "peak_db": peak})
    meta_p.write_text(json.dumps(meta, indent=2) + "\n")
    print(f"SAVED {stem} {probe(wav):.2f}s mean {mean} peak {peak}")


def cmd_splice(sid: str, head: str, tail: str, at_word: int) -> None:
    """Take `head` up to word `at_word`, then take `tail` from that word on, cut in the pause between the two
    sentences (both takes say the same script; nothing is re-timed). Writes take `<head><tail>`."""
    item = SHORTS[sid]
    d_ = vo_dir(item)
    stem = f"{item['slug']}_vo_v01"
    al_h = json.loads((d_ / f"{stem}{head}_align.json").read_text())
    al_t = json.loads((d_ / f"{stem}{tail}_align.json").read_text())
    if al_h["characters"] != al_t["characters"]:
        raise SystemExit("the two takes' texts differ")
    chars = al_h["characters"]
    k, n_words, prev_space = 0, 0, True
    for k, ch in enumerate(chars):
        if not ch.isspace() and prev_space:
            if n_words == at_word:
                break
            n_words += 1
        prev_space = ch.isspace()
    last = max(i for i in range(k) if not chars[i].isspace())

    def cut(al: dict) -> float:
        return (al["character_end_times_seconds"][last] + al["character_start_times_seconds"][k]) / 2

    c_h, c_t = cut(al_h), cut(al_t)
    out = d_ / f"{stem}{head}{tail}.wav"
    ff("-i", str(d_ / f"{stem}{head}.wav"), "-i", str(d_ / f"{stem}{tail}.wav"), "-filter_complex",
       f"[0:a]atrim=0:{c_h:.4f},asetpts=PTS-STARTPTS,afade=t=out:st={c_h - 0.02:.4f}:d=0.02[a];"
       f"[1:a]atrim={c_t:.4f},asetpts=PTS-STARTPTS,afade=t=in:d=0.02[b];[a][b]concat=n=2:v=0:a=1[o]",
       "-map", "[o]", "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", str(out))
    shift = c_h - c_t
    al = {"characters": chars,
          "character_start_times_seconds": al_h["character_start_times_seconds"][:k]
          + [round(t + shift, 4) for t in al_t["character_start_times_seconds"][k:]],
          "character_end_times_seconds": al_h["character_end_times_seconds"][:k]
          + [round(t + shift, 4) for t in al_t["character_end_times_seconds"][k:]]}
    (d_ / f"{stem}{head}{tail}_align.json").write_text(json.dumps(al, indent=1))
    rec = {"id": sid, "take": head + tail, "head_take": head, "tail_take": tail, "at_word": at_word,
           "cut_head_s": round(c_h, 3), "cut_tail_s": round(c_t, 3), "duration_s": round(probe(out), 3),
           "sha256": sha256(out)}
    (d_ / f"VO_BACKCAT_SPLICE_{sid}.json").write_text(json.dumps(rec, indent=2) + "\n")
    print(f"SPLICED {sid} take {head} [0–{c_h:.2f}] + take {tail} [{c_t:.2f}–] → {rec['duration_s']} s")


MAX_PAUSE, LEAD, TAIL, PEAK = 0.6, 0.05, 0.25, -2.0


def silences(wav: Path, d: float) -> list[tuple[float, float]]:
    err = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(wav), "-af",
                          "silencedetect=n=-45dB:d=0.05", "-f", "null", "-"], capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r"silence_start: (-?[\d.]+)", err)]
    en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
    if len(en) < len(st):
        en.append(d)
    return [(max(0.0, a), b) for a, b in zip(st, en)]


def cmd_finish(sid: str, take: str) -> None:
    """The long's VO finish step 1: lead 0.05 s, pauses > 0.6 s → 0.6 s, tail 0.25 s, peak −2 dB. No atempo."""
    item = SHORTS[sid]
    d_ = vo_dir(item)
    src = d_ / f"{item['slug']}_vo_v01{take}.wav"
    al = json.loads((d_ / f"{item['slug']}_vo_v01{take}_align.json").read_text())
    d = probe(src)
    keep, cur = [], 0.0
    for a, b in silences(src, d):
        if a <= 0.01:
            cur = max(0.0, b - LEAD)
            continue
        if b >= d - 0.01:
            keep.append((cur, min(d, a + TAIL)))
            cur = d
            break
        if b - a > MAX_PAUSE:
            keep.append((cur, a + MAX_PAUSE / 2))
            cur = b - MAX_PAUSE / 2
    if cur < d:
        keep.append((cur, d))

    def remap(t: float) -> float:
        out = 0.0
        for a, b in keep:
            if t <= a:
                return out
            if t <= b:
                return out + (t - a)
            out += b - a
        return out

    gain = PEAK - volstats(src)[1]
    parts = "".join(f"[0:a]atrim={a:.4f}:{b:.4f},asetpts=PTS-STARTPTS[s{i}];" for i, (a, b) in enumerate(keep))
    fc = parts + "".join(f"[s{i}]" for i in range(len(keep))) + f"concat=n={len(keep)}:v=0:a=1,volume={gain:.3f}dB[a]"
    out = d_ / f"{item['slug']}_vo_v01_fin.wav"
    ff("-i", str(src), "-filter_complex", fc, "-map", "[a]", "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", str(out))
    al2 = dict(al)
    al2["character_start_times_seconds"] = [round(remap(t), 4) for t in al["character_start_times_seconds"]]
    al2["character_end_times_seconds"] = [round(remap(t), 4) for t in al["character_end_times_seconds"]]
    (d_ / f"{item['slug']}_vo_v01_fin_align.json").write_text(json.dumps(al2, indent=1))
    rec = {"id": sid, "take": take, "source": src.name, "source_s": round(d, 3), "finished": out.name,
           "finished_s": round(probe(out), 3), "gain_db": round(gain, 2), "peak_db": volstats(out)[1],
           "sha256": sha256(out), "rule": "pauses > 0.6 s → 0.6 s, lead 0.05 s, tail 0.25 s, peak −2 dB, no atempo"}
    (d_ / f"VO_BACKCAT_FINISH_{sid}.json").write_text(json.dumps(rec, indent=2) + "\n")
    print(f"FIN {sid} take {take}: {rec['source_s']} → {rec['finished_s']} s, peak {rec['peak_db']}")


# ── Picture ───────────────────────────────────────────────────────────────────────────────────────

def words_from_align(path: Path) -> list[tuple[str, float, float]]:
    d = json.loads(path.read_text())
    words, cur, t0, t1 = [], "", 0.0, 0.0
    for ch, a, b in zip(d["characters"], d["character_start_times_seconds"], d["character_end_times_seconds"]):
        if ch.isspace():
            if cur:
                words.append((cur, t0, t1))
            cur = ""
        else:
            if not cur:
                t0 = a
            cur, t1 = cur + ch, b
    if cur:
        words.append((cur, t0, t1))
    return words


def chunk_words(words: list[tuple[str, float, float]]) -> list[dict]:
    chunks, i, n = [], 0, len(words)
    while i < n:
        t0 = words[i][1]
        parts, t_end, j = [words[i][0]], words[i][2], i + 1
        while j < n:
            wj, sj, ej = words[j]
            if parts[-1][-1:] in ".?!":
                break
            if parts[-1][-1:] in ",;:" and len(parts) >= 2 and sj - t0 >= CHUNK_MIN_S:
                break
            if len(parts) >= CHUNK_MAX_WORDS and sj - t0 >= CHUNK_MIN_S:
                break
            if ej - t0 >= CHUNK_MAX_S and len(parts) >= 2:
                break
            parts.append(wj)
            t_end = ej
            j += 1
        t1 = words[j][1] if j < n else t_end + 0.25
        chunks.append({"text": " ".join(parts), "t0": round(t0, 3), "t1": round(t1, 3), "n_words": len(parts)})
        i = j
    return chunks


def render(path: Path, text: str, size: int, y: int, *, anchor: str = "top", font_path: str = FONT,
           index: int = 0, fill=CREAM, stroke: int = 3) -> None:
    from PIL import Image, ImageDraw, ImageFont
    font = ImageFont.truetype(font_path, size, index=index)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    tokens = [(w.strip("*"), w.startswith("**")) for w in text.split()]
    lines, cur = [], []
    for tok in tokens:
        trial = " ".join(t for t, _ in cur + [tok])
        if cur and font.getlength(trial) > W - 96:
            lines.append(cur)
            cur = [tok]
        else:
            cur.append(tok)
    lines.append(cur)
    asc, desc = font.getmetrics()
    lh, gap = asc + desc, int(size * 0.12)
    block = lh * len(lines) + gap * (len(lines) - 1)
    cy = H - y - block if anchor == "bottom" else y
    space = font.getlength(" ")
    for line in lines:
        x = (W - font.getlength(" ".join(t for t, _ in line))) / 2
        for t, hot in line:
            draw.text((x, cy), t, font=font, fill=YEL if hot else fill, stroke_width=stroke, stroke_fill=INK)
            x += font.getlength(t) + space
        cy += lh + gap
    img.save(path)


def render_hook(path: Path, text: str) -> dict:
    """One word per line, cap height HOOK_CAP of H (down to HOOK_CAP_MIN if the widest word needs it), centred.
    Didot Bold like the 005 hooks; a word too wide for Didot even at HOOK_CAP_MIN (ELEMENTS) falls back to
    Bodoni 72 Bold at HOOK_CAP_MIN with at most HOOK_SQUEEZE_MIN horizontal squeeze."""
    from PIL import Image, ImageDraw, ImageFont
    tokens = [(w.strip("*"), w.startswith("**")) for w in text.split()]
    fit = W - 80

    def sized(face: str, idx: int, cap_t: float):
        size = 60
        while True:
            font = ImageFont.truetype(face, size, index=idx)
            if -font.getbbox("H", anchor="ls")[1] >= cap_t * H:
                return font, size, -font.getbbox("H", anchor="ls")[1]
            size += 1

    choice = None
    target = HOOK_CAP
    while target >= HOOK_CAP_MIN - 1e-9:
        font, size, cap = sized(FONT, 2, target)
        widest = max(font.getlength(t) for t, _ in tokens)
        if widest <= fit:
            choice = (FONT, font, size, cap, widest, 1.0)
            break
        target -= 0.0025
    if choice is None:
        font, size, cap = sized(HOOK_FALLBACK, 2, HOOK_CAP_MIN)
        widest = max(font.getlength(t) for t, _ in tokens)
        sx = min(1.0, fit / widest)
        if sx < HOOK_SQUEEZE_MIN:
            raise SystemExit(f"hook word {widest:.0f} px needs a {sx:.2f} squeeze even in the fallback face")
        choice = (HOOK_FALLBACK, font, size, cap, widest, sx)
    face, font, size, cap, widest, sx = choice
    pitch = round(cap * HOOK_PITCH)
    block = pitch * (len(tokens) - 1) + cap
    top = (H - block) // 2
    wide = Image.new("RGBA", (int(W / sx) + 2, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(wide)
    for k, (t, hot) in enumerate(tokens):
        draw.text((wide.width / 2, top + cap + k * pitch), t, font=font, anchor="ms", fill=YEL if hot else CREAM,
                  stroke_width=6, stroke_fill=INK)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sq = wide.resize((round(wide.width * sx), H), Image.LANCZOS) if sx < 1.0 else wide
    img.alpha_composite(sq, ((W - sq.width) // 2, 0))
    img.save(path)
    bottom = top + block
    if bottom > UI_TOP * H:
        raise SystemExit(f"hook block ends at {bottom / H:.1%}, inside the bottom UI")
    return {"font": Path(face).stem + " Bold", "font_size": size, "cap_px": cap, "cap_pct": round(100 * cap / H, 2),
            "h_squeeze": round(sx, 3), "lines": len(tokens),
            "block_pct": [round(100 * top / H, 1), round(100 * bottom / H, 1)],
            "widest_pct": round(100 * widest * sx / W, 1)}


def seg(src: Path, dst: Path, start: float, dur: float, x: int) -> None:
    if start + dur > probe(src) - 0.05:
        raise SystemExit(f"{src.name}: in {start} + {dur:.2f} s runs past the plate")
    vf = f"scale=1920:1080,crop=608:1080:{x}:0,scale={W}:{H}:flags=lanczos,setsar=1"
    ff("-ss", f"{start:.3f}", "-i", str(src), "-t", f"{dur:.3f}", "-filter_complex", vf, "-an", "-c:v", "libx264",
       "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "17", "-r", str(FPS), str(dst))


def build(sid: str) -> dict:
    from PIL import Image, ImageDraw
    item = SHORTS[sid]
    d_ = vo_dir(item)
    vo = d_ / f"{item['slug']}_vo_v01_fin.wav"
    words = words_from_align(d_ / f"{item['slug']}_vo_v01_fin_align.json")
    vo_s = probe(vo)
    last_end = min(words[-1][2], vo_s - TAIL)   # the finish leaves TAIL s of room tone after the last word
    loop_t = round(last_end + 0.12, 3)
    loop_s = min(LOOP_MIN_S, MAX_TOTAL_S - loop_t)
    if loop_s < LOOP_FLOOR_S:
        raise SystemExit(f"{sid}: only {loop_s:.2f} s left for the loop under 27 s; use a tighter take")
    total = round(max(vo_s, loop_t + loop_s), 3)
    if not 22.0 <= total <= 27.0:
        raise SystemExit(f"{sid}: {total} s outside 22–27 s")
    work = item["film"] / f"10_Shorts/_work_backcat_{VER}/{sid}"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)

    plates = []
    cuts = []
    for w, src, ins, x, pre, *lim in item["beats"]:
        digest = sha256(src)
        if pre and not digest.startswith(pre):
            raise SystemExit(f"{src.name}: sha {digest[:8]} is not the recorded KEEP {pre}")
        plates.append({"plate": src.relative_to(MEDIA).as_posix(), "sha256": digest})
        t = 0.0 if w == 0 else (loop_t if w == "loop" else max(0.0, words[w][1] - 0.15))
        cuts.append((round(t, 3), src, ins, x, w, lim[0] if lim else None))
    plan, segs = [], []
    for k, (t, src, ins, x, w, max_out) in enumerate(cuts):
        end = cuts[k + 1][0] if k + 1 < len(cuts) else total
        d = end - t
        if d < 1.2:
            raise SystemExit(f"{sid}: beat {k} only {d:.2f} s")
        if max_out is not None and ins + d > max_out:
            raise SystemExit(f"{sid}: beat {k} {src.name} would run to {ins + d:.2f} s, past its clean {max_out} s")
        out = work / f"seg_{k:02d}.mp4"
        seg(src, out, ins, d, x)
        segs.append(out)
        plan.append({"t0": t, "t1": round(end, 3), "plate": src.relative_to(MEDIA).as_posix(), "in_s": ins,
                     "out_s": round(ins + d, 3), "crop_x": x,
                     "lands_on": w if w in (0, "loop") else words[w][0]})
    (work / "pic.txt").write_text("".join(f"file '{s.name}'\n" for s in segs))
    pic = work / "picture.mp4"
    ff("-f", "concat", "-safe", "0", "-i", "pic.txt", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast",
       "-crf", "17", "-r", str(FPS), "-t", f"{total:.3f}", str(pic), cwd=work)

    bed_gain = (volstats(vo)[0] - 20.0) - volstats(item["bed"])[0]
    audio = work / "audio.wav"
    ff("-i", str(vo), "-stream_loop", "-1", "-i", str(item["bed"]), "-filter_complex",
       f"[0:a]aformat=sample_rates=48000:channel_layouts=stereo,apad=whole_dur={total:.3f}[v];"
       f"[1:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{total:.3f},asetpts=PTS-STARTPTS,"
       f"volume={bed_gain:.2f}dB,afade=t=in:d=0.05,afade=t=out:st={total - 0.2:.3f}:d=0.2[b];"
       f"[v][b]amix=inputs=2:normalize=0:duration=first[a]",
       "-map", "[a]", "-t", f"{total:.3f}", "-c:a", "pcm_s16le", str(audio))

    chunks = chunk_words(words)
    overlays = []
    hook_png = work / "cap_hook.png"
    hook_meta = render_hook(hook_png, item["hook"])
    overlays.append((hook_png, 0.0, 2.6, "hook", item["hook"].replace("**", "")))
    for i, c in enumerate(chunks):
        png = work / f"cap_{i:03d}.png"
        render(png, c["text"], 52, 330, anchor="bottom")
        overlays.append((png, c["t0"], min(c["t1"], total - 0.05), "vo", c["text"]))
    title_png = work / "cap_title.png"
    render(title_png, item["title"], 62, 250, index=2, stroke=4)
    shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for yy in range(560):
        ImageDraw.Draw(shade).line([(0, yy), (W, yy)], fill=(0, 0, 0, int(150 * (1 - yy / 560) ** 1.5)))
    Image.alpha_composite(shade, Image.open(title_png)).save(title_png)
    overlays.append((title_png, TITLE_IN, TITLE_OUT, "title", item["title"]))
    cta = work / "cap_cta.png"
    render(cta, "watch the full film →", 44, 250, anchor="bottom", font_path=CTA_FONT)
    overlays.append((cta, loop_t, total - 0.08, "cta", "watch the full film →"))

    inputs = ["-i", str(pic), "-i", str(audio)]
    for png, *_ in overlays:
        inputs += ["-loop", "1", "-i", str(png)]
    fc, last = [], "[0:v]"
    for i, (_, t0, t1, *_r) in enumerate(overlays, 2):
        fc.append(f"{last}[{i}:v]overlay=0:0:enable='between(t,{t0:.3f},{t1:.3f})'[v{i}]")
        last = f"[v{i}]"
    mp4 = item["film"] / f"10_Shorts/{item['slug']}_{VER}.mp4"
    ff(*inputs, "-filter_complex", ";".join(fc), "-map", last, "-map", "1:a", "-c:v", "libx264",
       "-pix_fmt", "yuv420p", "-profile:v", "high", "-preset", "medium", "-crf", "18", "-r", str(FPS),
       "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", "-t", f"{total:.3f}", "-movflags", "+faststart",
       str(mp4))
    timeline = [{"role": r, "text": t, "t0": round(a, 3), "t1": round(b, 3)} for _, a, b, r, t in overlays]
    (work / "timeline.json").write_text(json.dumps({"plan": plan, "overlays": timeline}, indent=2) + "\n")
    return {"id": sid, "air_date": item["air_date"], "short_title": item["short_title"],
            "promotes": item["promotes"], "file": mp4.relative_to(MEDIA).as_posix(), "sha256": sha256(mp4),
            "duration_s": round(probe(mp4), 3), "vo": vo.name, "vo_sha256": sha256(vo), "vo_s": round(vo_s, 3),
            "loop_from_s": loop_t, "loop_s": round(total - loop_t, 3), "bed": item["bed"].name, "bed_gain_db": round(bed_gain, 2),
            "hook": item["hook"].replace("**", ""), "hook_layer": hook_meta, "title_on_screen": item["title"],
            "plates": plates, "plan": plan, "captions": len(chunks), "work": work, "timeline": timeline}


def caption_check(work: Path, mp4: Path, timeline: list[dict]) -> dict:
    frames = work / "frames"
    frames.mkdir(parents=True, exist_ok=True)
    vo_rows = [r for r in timeline if r["role"] == "vo"]
    prev_text = prev_hash = None
    changes = matched = 0
    t, dur = 0.0, probe(mp4)
    while t < dur - 0.05:
        crop = frames / f"c{t:05.1f}.png"
        ff("-ss", f"{t:.3f}", "-i", str(mp4), "-frames:v", "1", "-vf", "crop=1000:320:40:1250", str(crop))
        text = next((r["text"] for r in vo_rows if r["t0"] <= t < r["t1"]), None)
        h = hashlib.md5(crop.read_bytes()).hexdigest()
        if prev_text is not None and text != prev_text:
            changes += 1
            matched += h != prev_hash
        prev_text, prev_hash = text, h
        t += 0.5
    ratio = matched / changes if changes else 0.0
    return {"ok": changes >= 7 and ratio >= 0.7, "changes": changes, "ratio": round(ratio, 2)}


def freeze(mp4: Path) -> list[str]:
    err = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(mp4), "-vf",
                          "freezedetect=n=0.003:d=0.8", "-map", "0:v", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    return re.findall(r"freeze_start: ([\d.]+)", err)


def run(cmd: list[str]) -> tuple[int, str]:
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.returncode, "\n".join(l for l in (r.stdout + r.stderr).splitlines() if "Warning" not in l and l.strip())


def cmd_build(only: list[str], icloud: bool) -> None:
    for sid in only or list(SHORTS):
        item = SHORTS[sid]
        rec = build(sid)
        work = rec.pop("work")
        mp4 = MEDIA / rec["file"]
        rec["caption_check"] = caption_check(work, mp4, rec.pop("timeline"))
        rec["gate"] = {}
        for name, gate in GATES.items():
            if gate.exists():
                code, out = run([sys.executable, str(gate), "check", str(mp4), "--air-date", item["air_date"]])
                rec["gate"][name] = {"exit": code, "output": out}
        code, out = run([str(VO_PY), str(VO_CHECK), str(mp4), "--script", str(vo_dir(item) / f"{sid}.txt")])
        rec["vo_check"] = {"exit": code, "output": out}
        rec["freezedetect_starts"] = freeze(mp4)
        for name, t in (("frame0", 0.0), ("title_frame", 11.5)):
            still = work / f"{mp4.stem}_{name}.jpg"
            ff("-ss", f"{t}", "-i", str(mp4), "-frames:v", "1", "-q:v", "2", str(still))
            rec[f"{name}_still"] = still.relative_to(MEDIA).as_posix()
        if icloud:
            dest = ICLOUD_ROOT / item["icloud"]
            dest.mkdir(parents=True, exist_ok=True)
            shutil.copy2(mp4, dest / mp4.name)
            rec["icloud"] = str(dest / mp4.name)
        idx_p = item["repo_film"] / "10_Shorts/SHORTS_INDEX_BACKCAT_v01.json"
        idx = json.loads(idx_p.read_text()) if idx_p.exists() else {
            "scripts": "SHORTS_SCRIPTS_BACKCAT_v02.md", "task": "PR #180 comment 5950150517",
            "builder": "02_Video-Projects/004_Whats-Really-Inside-An-Atom/10_Shorts/_build_backcat_nov_v01.py",
            "shorts": {}}
        idx["shorts"][sid] = rec
        idx_p.write_text(json.dumps(idx, indent=2) + "\n")
        print(f"BUILT {sid} {rec['duration_s']} s sha {rec['sha256'][:12]} captions {rec['caption_check']} "
              f"hook {rec['hook_layer']}")
        for name, g in rec["gate"].items():
            print(f"[gate {name}]\n{g['output']}")
        print(rec["vo_check"]["output"])
        print(f"freezedetect: {len(rec['freezedetect_starts'])} events {rec['freezedetect_starts']}")


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    v = sub.add_parser("vo"); v.add_argument("short", choices=list(SHORTS)); v.add_argument("--take", default="a")
    f = sub.add_parser("finish"); f.add_argument("short", choices=list(SHORTS)); f.add_argument("--take", required=True)
    b = sub.add_parser("build"); b.add_argument("short", nargs="*"); b.add_argument("--no-icloud", action="store_true")
    s = sub.add_parser("splice"); s.add_argument("short", choices=list(SHORTS))
    s.add_argument("--head", required=True); s.add_argument("--tail", required=True)
    s.add_argument("--at-word", type=int, required=True)
    a = ap.parse_args()
    if a.cmd == "vo":
        cmd_vo(a.short, a.take)
    elif a.cmd == "splice":
        cmd_splice(a.short, a.head, a.tail, a.at_word)
    elif a.cmd == "finish":
        cmd_finish(a.short, a.take)
    else:
        reexec_venv()
        cmd_build(a.short, not a.no_icloud)


if __name__ == "__main__":
    main()
