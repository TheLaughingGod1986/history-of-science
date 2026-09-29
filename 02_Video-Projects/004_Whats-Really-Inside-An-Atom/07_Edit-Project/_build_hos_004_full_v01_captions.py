#!/usr/bin/env python3
"""HOS 004 captions — script-locked SRT timed to VO v04 via faster-whisper.

Uses LOCKED script spoken words (atom_script_master_v02.md), never the
transcriber's substitutions. Word timings come from whisper on each part VO,
offset by full_v01 / v03 part start times. No cues during cream or hold.
"""
from __future__ import annotations

import json
import re
import subprocess
import unicodedata
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
SCRIPT = PROJ / "01_Script/atom_script_master_v02.md"
VO_DIR = PROJ / "02_Voiceover/05_Master"
OUT_SRT = PROJ / "11_Upload-Package/Captions/hos_004_full_v01.en.srt"
META = PROJ / "11_Upload-Package/Captions/hos_004_full_v01_captions_meta.json"

PART_STARTS = {
    1: 0.0,
    2: 70.533333,
    3: 162.411166,
    4: 246.844499,
    5: 356.577832,
}
CREAM_AT = 500.693770
MAX_CHARS = 42
MAX_LINES = 2

# Force script spellings when aligning
FORCE = {
    "rock": "wrong",  # never
    "sought": "sort",
    "the living": None,  # handled via word list
    "runtgen": "Röntgen",
    "rontgen": "Röntgen",
    "mosley": "Moseley",
    "jj": "J.J.",
    "j.j.": "J.J.",
    "thompson": "Thomson",
    "vandenbroek": "van den Broek",
}

VO_FILES = {
    1: VO_DIR / "hos_004_part01_vo_v04.wav",
    2: VO_DIR / "hos_004_part02_vo_v04.wav",
    3: VO_DIR / "hos_004_part03_vo_v04.wav",
    4: VO_DIR / "hos_004_part04_vo_v04.wav",
    5: VO_DIR / "hos_004_part05_vo_v04.wav",
}


def script_parts(path: Path) -> dict[int, list[str]]:
    text = path.read_text(encoding="utf-8")
    chunks = re.split(r"^## PART (\d+).*$", text, flags=re.M)
    # chunks: [preamble, "01", body, "02", body, ...]
    out: dict[int, list[str]] = {}
    for i in range(1, len(chunks), 2):
        num = int(chunks[i])
        body = chunks[i + 1]
        lines = []
        for line in body.splitlines():
            s = line.strip()
            if not s:
                continue
            if s.startswith("#") or s.startswith("[") or s.startswith("<!--"):
                continue
            lines.append(s)
        out[num] = lines
    return out


def tokenize_script(lines: list[str]) -> list[str]:
    """Keep punctuation-aware tokens for display; also return plain for align."""
    words: list[str] = []
    for line in lines:
        line = line.replace("**", "").replace("__", "").replace("`", "")
        # Keep apostrophes and hyphens inside words; split on spaces
        for w in line.split():
            words.append(w)
    return words


def norm_key(w: str) -> str:
    w = unicodedata.normalize("NFKD", w).encode("ascii", "ignore").decode()
    w = w.lower().replace("'", "'")
    w = re.sub(r"[^a-z0-9']+", "", w)
    return w


def whisper_words(path: Path) -> list[tuple[float, float, str]]:
    from faster_whisper import WhisperModel

    model = WhisperModel("small.en", device="cpu", compute_type="int8")
    segs, _ = model.transcribe(str(path), word_timestamps=True)
    out: list[tuple[float, float, str]] = []
    for s in segs:
        for w in s.words:
            tok = w.word.strip()
            if not tok:
                continue
            out.append((float(w.start), float(w.end), tok))
    return out


def align(script_words: list[str], whispered: list[tuple[float, float, str]]) -> list[tuple[float, float, str]]:
    """Map script words onto whisper timings (greedy)."""
    # Expand multi-token script items already split by space
    sw = script_words
    ww = whispered
    aligned: list[tuple[float, float, str]] = []
    wi = 0
    for s_word in sw:
        sk = norm_key(s_word)
        if not sk:
            # punctuation-only — attach to previous timing if any
            if aligned:
                t0, t1, _ = aligned[-1]
                aligned.append((t0, t1, s_word))
            continue
        # Advance whisper until keys match or run out
        found = None
        search_to = min(len(ww), wi + 8)
        for j in range(wi, search_to):
            wk = norm_key(ww[j][2])
            # alias fixes
            if wk in {"rock"} and sk == "wrong":
                found = j
                break
            if wk in {"sought"} and sk == "sort":
                found = j
                break
            if wk in {"runtgen", "rontgen"} and sk in {"rontgen", "röntgen", "roentgen"}:
                found = j
                break
            if wk in {"mosley"} and sk == "moseley":
                found = j
                break
            if wk in {"thompson"} and sk == "thomson":
                found = j
                break
            if wk == sk or wk.rstrip("s") == sk or sk.rstrip("s") == wk:
                found = j
                break
            # number words / digits skip on whisper side
            if wk.isdigit():
                continue
        if found is None:
            # interpolate from neighbours
            if aligned and wi < len(ww):
                t0 = aligned[-1][1]
                t1 = ww[wi][0] if wi < len(ww) else t0 + 0.25
            elif wi < len(ww):
                t0, t1 = ww[wi][0], ww[wi][1]
            else:
                t0 = aligned[-1][1] if aligned else 0.0
                t1 = t0 + 0.25
            aligned.append((t0, max(t1, t0 + 0.12), s_word))
        else:
            t0, t1, _ = ww[found]
            aligned.append((t0, t1, s_word))
            wi = found + 1
    return aligned


def wrap_cues(words: list[tuple[float, float, str]]) -> list[tuple[float, float, str]]:
    """Pack into ≤2 lines × ≤42 chars cues."""
    cues: list[tuple[float, float, str]] = []
    i = 0
    n = len(words)
    while i < n:
        t0 = words[i][0]
        lines: list[str] = []
        cur = ""
        t1 = words[i][1]
        line_count = 0
        while i < n and line_count < MAX_LINES:
            w = words[i][2]
            trial = (cur + " " + w).strip() if cur else w
            if len(trial) <= MAX_CHARS:
                cur = trial
                t1 = words[i][1]
                i += 1
            else:
                if cur:
                    lines.append(cur)
                    line_count += 1
                    cur = ""
                    if line_count >= MAX_LINES:
                        break
                else:
                    # single word longer than max — hard take
                    lines.append(w[:MAX_CHARS])
                    t1 = words[i][1]
                    i += 1
                    line_count += 1
                    cur = ""
                    break
        if cur and line_count < MAX_LINES:
            lines.append(cur)
        if not lines:
            break
        text = "\n".join(lines)
        # Minimum on-screen duration
        if t1 - t0 < 0.7:
            t1 = t0 + 0.7
        cues.append((t0, t1, text))
    # Fix overlaps
    for j in range(1, len(cues)):
        if cues[j][0] < cues[j - 1][1]:
            # shrink previous
            prev = cues[j - 1]
            cues[j - 1] = (prev[0], max(prev[0] + 0.4, cues[j][0] - 0.02), prev[2])
    return cues


def ts(sec: float) -> str:
    if sec < 0:
        sec = 0
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    ms = int(round((sec - int(sec)) * 1000))
    if ms == 1000:
        s += 1
        ms = 0
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def main() -> None:
    parts = script_parts(SCRIPT)
    all_cues: list[tuple[float, float, str]] = []
    per_part = {}

    for pid in sorted(PART_STARTS):
        vo = VO_FILES[pid]
        if not vo.exists():
            raise SystemExit(f"missing {vo}")
        print(f"PART {pid} whisper {vo.name}…", flush=True)
        whispered = whisper_words(vo)
        sw = tokenize_script(parts[pid])
        aligned = align(sw, whispered)
        offset = PART_STARTS[pid]
        shifted = [(a + offset, b + offset, w) for a, b, w in aligned]
        cues = wrap_cues(shifted)
        # Drop anything at/after cream
        cues = [(a, min(b, CREAM_AT - 0.05), t) for a, b, t in cues if a < CREAM_AT - 0.15]
        cues = [(a, b, t) for a, b, t in cues if b > a]
        all_cues.extend(cues)
        per_part[pid] = {"script_words": len(sw), "whisper_words": len(whispered), "cues": len(cues)}
        print(f"  script={len(sw)} whisper={len(whispered)} cues={len(cues)}", flush=True)

    # Enforce known spellings in cue text
    fixes = [
        (re.compile(r"\brock\b", re.I), "wrong"),
        (re.compile(r"\bsought\b", re.I), "sort"),
        (re.compile(r"\bthe living hand\b", re.I), "a living hand"),
        (re.compile(r"\bRuntgen\b"), "Röntgen"),
        (re.compile(r"\bRontgen\b"), "Röntgen"),
        (re.compile(r"\bMosley\b"), "Moseley"),
        (re.compile(r"\bJJ Thomson\b"), "J.J. Thomson"),
        (re.compile(r"\bJ J Thomson\b"), "J.J. Thomson"),
        (re.compile(r"\bThompson\b"), "Thomson"),
        (re.compile(r"\bVandenbroek\b", re.I), "van den Broek"),
    ]
    fixed: list[tuple[float, float, str]] = []
    for a, b, t in all_cues:
        for rx, rep in fixes:
            t = rx.sub(rep, t)
        fixed.append((a, b, t))

    OUT_SRT.parent.mkdir(parents=True, exist_ok=True)
    lines = []
    for i, (a, b, t) in enumerate(fixed, 1):
        lines.append(str(i))
        lines.append(f"{ts(a)} --> {ts(b)}")
        lines.append(t)
        lines.append("")
    OUT_SRT.write_text("\n".join(lines), encoding="utf-8")

    meta = {
        "file": OUT_SRT.name,
        "script": SCRIPT.name,
        "cream_cutoff_s": CREAM_AT,
        "max_chars": MAX_CHARS,
        "max_lines": MAX_LINES,
        "part_starts": PART_STARTS,
        "per_part": per_part,
        "cue_count": len(fixed),
        "source": "script-locked + faster-whisper timings on VO v04",
    }
    META.write_text(json.dumps(meta, indent=2) + "\n")
    print(f"WROTE {OUT_SRT} cues={len(fixed)}", flush=True)


if __name__ == "__main__":
    main()
