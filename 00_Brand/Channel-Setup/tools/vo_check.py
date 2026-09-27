#!/usr/bin/env python3
"""VO check — run on every narration take before Ben listens (STUDIO_PLAYBOOK.md §4).

Written 27 Sep 2026 from the HOS 004 VO rounds. Checks one audio file (a part or the whole
film) against the locked master script:

  FAIL  a spoken word is missing or added (after number/spelling normalisation)
  FAIL  speech mean outside −19 to −28 dB, or peak above −1 dB
  FAIL  a silence longer than 1.5 s (part joins in a full listen file are reported, not failed)
  warn  pace under 145 words a minute (the v01 take ran ~140 wpm and 8:58 for 1,283 words)
  info  duration, pace, loudness, and the time of the first question, the promise and the stakes

Usage
  python3 vo_check.py <audio> --script <…/01_Script/<slug>_script_master_vNN.md> [--part 1] [--json]

--part N checks only that part's lines (Part 01 = everything before "## PART 02").
Without --part the whole script is used (for the all-parts listen file).

Needs ffmpeg/ffprobe. The word check needs `pip install faster-whisper` (downloads the
small.en model once); without it the word check is skipped and the report says so.
It cannot judge warmth or delivery: Ben still listens.
Exit code 0 = PASS, 1 = FAIL, 2 = tool error.
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

MEAN_MIN, MEAN_MAX = -28.0, -19.0
PEAK_MAX = -1.0
SILENCE_DB, SILENCE_FAIL_S = -45, 1.5
WPM_WARN = 145

# Words a transcriber writes differently from the script. Numbers are dropped from both
# sides before the diff (the script spells them out, the transcriber writes digits).
ALIASES = {"thompson": "thomson", "thompson's": "thomson's", "center": "centre", "st": "saint",
           "dimitri": "dmitri", "vandenbroek": "van den broek", "vandenbroek's": "van den broek's",
           "schoolteacher": "school teacher", "p": "pea", "dmitry": "dmitri"}
NUMBER_WORDS = set(("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen "
                    "fifteen sixteen seventeen eighteen nineteen twenty thirty forty fifty sixty seventy eighty "
                    "ninety hundred thousand oh").split())


def run(cmd: list[str]) -> str:
    return subprocess.run(cmd, check=True, capture_output=True, text=True, errors="replace").stderr


def probe_duration(path: Path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                         check=True, capture_output=True, text=True).stdout
    return float(out.strip())


def loudness(path: Path) -> tuple[float, float]:
    err = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af", "volumedetect", "-f", "null", "-"])
    mean = float(re.search(r"mean_volume: (-?[\d.]+)", err).group(1))
    peak = float(re.search(r"max_volume: (-?[\d.]+)", err).group(1))
    return mean, peak


def silences(path: Path) -> list[tuple[float, float]]:
    err = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af",
               f"silencedetect=n={SILENCE_DB}dB:d=1.0", "-f", "null", "-"])
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", err)]
    lens = [float(x) for x in re.findall(r"silence_duration: ([\d.]+)", err)]
    return list(zip(starts, lens))


def script_lines(script: Path, part: int | None) -> list[str]:
    text = script.read_text(encoding="utf-8")
    if part:
        chunks = re.split(r"^## PART \d+.*$", text, flags=re.M)
        # chunks[0] is the title block; chunk N is part N
        text = chunks[part] if part < len(chunks) else ""
    return [l for l in text.splitlines() if l.strip() and not re.match(r"\s*(#|\[|<!--)", l)]


def norm(text: str) -> list[str]:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()  # Röntgen -> Rontgen
    text = text.lower().replace("’", "'").replace("**", "")
    words = re.sub(r"[^a-z0-9' -]+", " ", text).replace("-", " ").split()
    out: list[str] = []
    for w in words:
        w = ALIASES.get(w, w)
        for piece in w.split():
            if piece.isdigit() or piece in NUMBER_WORDS or not piece:
                continue
            out.append(piece.strip("'"))
    return [w for w in out if w]


def transcribe(path: Path):
    try:
        from faster_whisper import WhisperModel  # type: ignore
    except ImportError:
        return None
    model = WhisperModel("small.en", device="cpu", compute_type="int8")
    segs, _ = model.transcribe(str(path), word_timestamps=True)
    return [(round(w.start, 2), w.word.strip()) for s in segs for w in s.words]


def first_time(words, phrase: str) -> float | None:
    p = norm(phrase)[:3]
    seq = [(t, norm(w)) for t, w in words]
    flat = [(t, x) for t, ws in seq for x in ws]
    for i in range(len(flat) - len(p) + 1):
        if [flat[i + j][1] for j in range(len(p))] == p:
            return flat[i][0]
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("audio", type=Path)
    ap.add_argument("--script", type=Path, required=True)
    ap.add_argument("--part", type=int, default=None)
    ap.add_argument("--json", action="store_true")
    ns = ap.parse_args()

    res: dict = {"file": str(ns.audio), "part": ns.part, "fails": [], "warns": []}
    dur = probe_duration(ns.audio)
    mean, peak = loudness(ns.audio)
    res.update(duration_s=round(dur, 2), duration=f"{int(dur // 60)}:{dur % 60:05.2f}", mean_db=mean, peak_db=peak)
    if not (MEAN_MIN <= mean <= MEAN_MAX):
        res["fails"].append(f"speech mean {mean} dB outside {MEAN_MIN} to {MEAN_MAX} dB")
    if peak > PEAK_MAX:
        res["fails"].append(f"peak {peak} dB above {PEAK_MAX} dB")
    long_gaps = [(round(s, 2), round(l, 2)) for s, l in silences(ns.audio)]
    res["pauses_over_1s"] = long_gaps
    for s, l in long_gaps:
        if l > SILENCE_FAIL_S:
            msg = f"silence {l}s at {int(s // 60)}:{s % 60:05.2f}"
            (res["warns"] if ns.part is None else res["fails"]).append(msg + (" (part join?)" if ns.part is None else ""))

    lines = script_lines(ns.script, ns.part)
    script_words = norm(" ".join(lines))
    words = transcribe(ns.audio)
    if words is None:
        res["warns"].append("word check skipped: pip install faster-whisper")
    else:
        heard = norm(" ".join(w for _, w in words))
        res["script_words"], res["heard_words"] = len(script_words), len(heard)
        spoken = len(re.findall(r"[A-Za-z0-9']+", " ".join(lines)))
        res["wpm"] = round(spoken / (dur / 60))
        if res["wpm"] < WPM_WARN:
            res["warns"].append(f"pace {res['wpm']} wpm (< {WPM_WARN}); expect a long film — see STUDIO_PLAYBOOK.md §4 speed")
        diffs = []
        for op, a1, a2, b1, b2 in difflib.SequenceMatcher(None, script_words, heard, autojunk=False).get_opcodes():
            if op == "equal":
                continue
            where = words[min(b1, len(words) - 1)][0] if words else 0
            a, b = "".join(script_words[a1:a2]), "".join(heard[b1:b2])
            alike = op == "replace" and difflib.SequenceMatcher(None, a, b).ratio() >= 0.7
            diffs.append({"at": f"{int(where // 60)}:{where % 60:05.2f}", "op": op, "sounds_alike": alike,
                          "script": " ".join(script_words[max(a1 - 3, 0):a2 + 3]),
                          "heard": " ".join(heard[max(b1 - 3, 0):b2 + 3])})
        res["word_diffs"] = diffs
        for d in diffs:
            msg = f"{d['op']} at ~{d['at']}: script '{d['script']}' / heard '{d['heard']}'"
            if d["sounds_alike"]:
                res["warns"].append(msg + " — sounds alike (likely the transcriber); listen")
            else:
                res["fails"].append(msg + " — listen, then regenerate that sentence alone if real")
        if ns.part in (None, 1):
            questions = [l for l in lines if "?" in l]
            marks = {}
            if questions:
                q = questions[1] if len(questions) > 1 else questions[0]
                marks["title_question"] = first_time(words, q.split("?")[0].split(".")[-1])
            by_end = next((l for l in lines if l.lower().startswith("by the end")), None)
            if by_end:
                marks["promise"] = first_time(words, by_end)
            because = next((l for l in lines if l.lower().startswith("because")), None)
            if because:
                marks["stakes"] = first_time(words, because)
            res["first_minute"] = marks

    res["verdict"] = "FAIL" if res["fails"] else "PASS"
    if ns.json:
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        print(f"{res['verdict']}  {ns.audio.name}  {res['duration']}  mean {mean} dB  peak {peak} dB"
              + (f"  {res.get('wpm')} wpm" if "wpm" in res else ""))
        if res.get("first_minute"):
            print("   first minute: " + "  ".join(f"{k} {v}s" for k, v in res["first_minute"].items()))
        for x in res["fails"]:
            print(f"   FAIL  {x}")
        for x in res["warns"]:
            print(f"   warn  {x}")
    return 1 if res["fails"] else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        sys.stderr.write(f"tool error: {exc}\n")
        raise SystemExit(2)
