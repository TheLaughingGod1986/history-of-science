#!/usr/bin/env python3
"""Build HOS 008 en-GB captions (SRT) aligned to locked master v05 (J3500).

Canonical sentence text comes from 01_Script/lightning_script_master_v01.md
via 07_Edit-Project/VO_RETIME_v01.json (British spelling, exact spoken words).
Word timestamps come from faster-whisper small.en alignment directly on
hos_008_master_v05.mp4 (d1ffb78d...841b, 539.626 s), preserving the pause trims
baked into master v03/v04/v05. Long sentences split into <=2-line, <=42-char
cues by character share; no cue crosses a chapter boundary or runs past the end.
"""
from __future__ import annotations

import difflib
import hashlib
import json
import re
import textwrap
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
RETIME = PROJ / "07_Edit-Project/VO_RETIME_v01.json"
ASR_WORDS = Path("/tmp/hos008_v05_words.json")
OUT_SRT = PROJ / "11_Upload-Package/Captions/hos_008_master_v05.en.srt"
OUT_META = PROJ / "11_Upload-Package/Captions/hos_008_master_v05_captions_meta.json"
OUT_CHAPTERS = PROJ / "11_Upload-Package/Chapters/lightning_long_chapters_v05.txt"

MASTER_PATH = "/Volumes/data/studio-live/History Of Science/02_Video-Projects/008_Lightning-Franklin/07_Edit-Project/_precheck/master_v05/hos_008_master_v05.mp4"
MASTER_SHA = "d1ffb78dfc3d77519b5f37dfbddeec2f7802fa2d79e58b4524be31551a67841b"
MASTER_DUR = 539.626
CHAPTER_STARTS_S = [100.251, 187.952, 319.004, 408.964]
MAX_CHARS = 42
MAX_LINES = 2
MIN_CUE_S = 0.8

NUM_MAP = {
    "seventeen": ["17"], "fifty": ["50"], "two": ["2"], "forties": ["40s"],
    "forty": ["40"], "nine": ["9"], "twelve": ["12"], "five": ["5"],
    "twenty": ["20"], "one": ["1"], "hundred": ["100"], "thousand": ["1000"],
    "eighteenth": ["18th"],
}


def norm_tokens(text: str) -> list[str]:
    clean = re.sub(r"['’]", "", text.lower())
    return re.findall(r"[a-z0-9]+", clean)


def ts(s: float) -> str:
    ms = int(round(max(0.0, s) * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    sec, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{sec:02d},{ms:03d}"


def chunks(text: str) -> list[str]:
    lines = textwrap.wrap(text, MAX_CHARS)
    return [" ".join(lines[i:i + MAX_LINES]) for i in range(0, len(lines), MAX_LINES)]


def main() -> int:
    retime = json.loads(RETIME.read_text())
    asr = json.loads(ASR_WORDS.read_text())
    asr_words = asr["words"]
    asr_toks: list[str] = []
    asr_word_idx: list[int] = []
    for idx, w in enumerate(asr_words):
        for tok in norm_tokens(w["word"]):
            asr_toks.append(tok)
            asr_word_idx.append(idx)

    # Flatten script sentences and their tokens
    sentences: list[dict] = []
    script_toks: list[str] = []
    sent_spans: list[tuple[int, int]] = []
    for part in retime["parts"]:
        for s in part["sentences"]:
            t0 = len(script_toks)
            toks = norm_tokens(s["text"])
            script_toks.extend(toks)
            t1 = len(script_toks)
            sentences.append({"part": part["part"], "text": s["text"], "orig_dur": float(s["end_s"]) - float(s["start_s"])})
            sent_spans.append((t0, t1))

    # Align script tokens to ASR tokens via SequenceMatcher
    sm = difflib.SequenceMatcher(None, script_toks, asr_toks, autojunk=False)
    tok_to_asr: list[int | None] = [None] * len(script_toks)
    for block in sm.get_matching_blocks():
        for k in range(block.size):
            tok_to_asr[block.a + k] = asr_word_idx[block.b + k]

    matched_toks = sum(1 for x in tok_to_asr if x is not None)
    print(f"Token alignment: {matched_toks}/{len(script_toks)} ({100*matched_toks/len(script_toks):.1f}%)")

    windows: list[list] = []
    for idx, (s, (t0, t1)) in enumerate(zip(sentences, sent_spans)):
        mapped = [tok_to_asr[k] for k in range(t0, t1) if tok_to_asr[k] is not None]
        if mapped:
            first_k = next(k for k in range(t0, t1) if tok_to_asr[k] is not None)
            last_k = next(k for k in range(t1 - 1, t0 - 1, -1) if tok_to_asr[k] is not None)
            a = float(asr_words[tok_to_asr[first_k]]["start"])
            b = float(asr_words[tok_to_asr[last_k]]["end"])
            # Back-adjust slightly if leading/trailing number tokens (e.g. "seventeen fifty-two" vs "1752") missed
            if first_k > t0 and tok_to_asr[first_k] > 0:
                prev_end = float(asr_words[tok_to_asr[first_k] - 1]["end"])
                if a - prev_end < 0.9:
                    a = max(0.0, a - min(0.35 * (first_k - t0), a - prev_end))
            if last_k < t1 - 1 and tok_to_asr[last_k] + 1 < len(asr_words):
                next_start = float(asr_words[tok_to_asr[last_k] + 1]["start"])
                b = min(next_start - 0.04, b + 0.30 * (t1 - 1 - last_k))
            if b <= a + 0.2:
                b = a + max(0.8, s["orig_dur"])
        else:
            prev_end = windows[-1][1] if windows else 0.0
            a = prev_end + 0.15
            b = a + max(1.0, s["orig_dur"])
        windows.append([a, b, s["text"], s["part"]])

    # Enforce monotonic starts
    for i in range(1, len(windows)):
        if windows[i][0] < windows[i - 1][1]:
            mid = (windows[i - 1][1] + windows[i][0]) / 2.0
            windows[i - 1][1] = max(windows[i - 1][0] + 0.4, mid - 0.02)
            windows[i][0] = windows[i - 1][1] + 0.04
            if windows[i][1] <= windows[i][0] + 0.4:
                windows[i][1] = windows[i][0] + 0.8

    # Split long sentences into <=2-line cues
    cues: list[tuple[float, float, str]] = []
    for a, b, text, _part in windows:
        pieces = chunks(text)
        total = sum(len(p) for p in pieces) or 1
        t = a
        for p in pieces:
            d = (b - a) * len(p) / total
            cues.append((t, t + d, p))
            t += d

    fixed: list[tuple[float, float, str]] = []
    for i, (a, b, text) in enumerate(cues):
        nxt = cues[i + 1][0] if i + 1 < len(cues) else MASTER_DUR
        stop = min(nxt - 0.04, MASTER_DUR - 0.05)
        for c in CHAPTER_STARTS_S:
            if a < c < stop:
                stop = min(stop, c - 0.04)
        if stop - a >= MIN_CUE_S and b - a < MIN_CUE_S:
            b = a + MIN_CUE_S
        b = min(b, stop)
        if b <= a + 0.05:
            raise SystemExit(f"cue collapsed: {text!r} at {a:.2f} stop={stop:.2f}")
        for c in CHAPTER_STARTS_S:
            if a < c < b:
                raise SystemExit(f"cue crosses chapter {c}: {text!r} ({a:.2f}-{b:.2f})")
        fixed.append((a, b, text))

    lines = []
    for i, (a, b, text) in enumerate(fixed, 1):
        wrapped = "\n".join(textwrap.wrap(text, MAX_CHARS))
        lines.append(f"{i}\n{ts(a)} --> {ts(b)}\n{wrapped}\n")
    OUT_SRT.parent.mkdir(parents=True, exist_ok=True)
    OUT_SRT.write_text("\n".join(lines), encoding="utf-8")

    OUT_CHAPTERS.parent.mkdir(parents=True, exist_ok=True)
    OUT_CHAPTERS.write_text(
        "0:00 Fire from the sky\n"
        "1:40 The sparks in a jar\n"
        "3:08 A kite in the storm\n"
        "5:19 The spark from the key\n"
        "6:49 The rod on every roof\n",
        encoding="utf-8",
    )

    srt_sha = hashlib.sha256(OUT_SRT.read_bytes()).hexdigest()
    OUT_META.write_text(json.dumps({
        "srt": OUT_SRT.name,
        "sha256": srt_sha,
        "language": "en-GB",
        "master": MASTER_PATH,
        "master_sha256": MASTER_SHA,
        "audio_packet_sha256": "1a4b59543c66851f8853bacb4a902642ae7cb26653fa7cabecaf3dcf770f1f69",
        "audio_note": "Aligned directly to hos_008_master_v05.mp4 audio via faster-whisper small.en; canonical British English text from 01_Script/lightning_script_master_v01.md via VO_RETIME_v01.json",
        "source_text": "01_Script/lightning_script_master_v01.md via 07_Edit-Project/VO_RETIME_v01.json",
        "token_match_pct": round(100.0 * matched_toks / len(script_toks), 2),
        "cues": len(fixed),
        "first": ts(fixed[0][0]),
        "last_end": ts(fixed[-1][1]),
        "chapter_starts_s": CHAPTER_STARTS_S,
    }, indent=2) + "\n")
    print(f"PASS  {OUT_SRT.name}  cues={len(fixed)}  {ts(fixed[0][0])} -> {ts(fixed[-1][1])}  sha256={srt_sha}")
    # Print part-opening cues for verification
    for p_idx in (1, 2, 3, 4, 5):
        first_w = next(w for w in windows if w[3] == p_idx)
        print(f"  Part {p_idx}: {first_w[0]:.2f}s - {first_w[1]:.2f}s | {first_w[2][:65]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
