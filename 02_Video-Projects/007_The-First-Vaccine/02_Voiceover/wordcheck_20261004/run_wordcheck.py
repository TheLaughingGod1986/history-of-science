#!/usr/bin/env python3
"""007 VO word-check: faster-whisper vs extract .txt (Claude 5982287173)."""
from __future__ import annotations
import difflib, json, re, unicodedata, subprocess
from pathlib import Path

VO = Path("/Users/benjaminoats/_desk/007/vo_20261004/vo")
OUT = Path("/Users/benjaminoats/_desk/007/vo_20261004/wordcheck_20261004")

PARTS = [
    ("01", "the_speckled_monster"),
    ("02", "the_milkmaids_secret"),
    ("03", "a_pail_a_lancet_and_a_boy"),
    ("04", "the_test"),
    ("05", "the_word_that_saved_millions"),
]

# UK/US + common ASR near-misses that are NOT content skips
SPELL_OK = {
    ("rumour", "rumor"), ("rumor", "rumour"),
    ("neighbour", "neighbor"), ("neighbor", "neighbour"),
    ("neighbour's", "neighbor's"), ("neighbor's", "neighbour's"),
    ("neighbours", "neighbors"), ("neighbors", "neighbours"),
    ("honour", "honor"), ("honor", "honour"),
    ("travelled", "traveled"), ("traveled", "travelled"),
    ("recognise", "recognize"), ("recognize", "recognise"),
    ("milked", "milk"),  # tense ASR soft — still flag as changed but soft
    ("jenner", "jenna"), ("jenna", "jenner"),  # ASR proper-name
    ("jenner's", "jenna's"), ("jenna's", "jenner's"),
    ("berkeley", "barclay"), ("barclay", "berkeley"),
    ("berkeley", "barkley"), ("barkley", "berkeley"),
    ("variolae", "varioli"), ("varioli", "variolae"),
    ("vacca", "vaca"), ("vaca", "vacca"),
    ("cow's", "cows"), ("cows", "cow's"),
    ("milkmaids", "milkmaid"), ("milkmaid", "milkmaids"),
    ("she'd", "she"), ("she'd", "shehad"),
    ("he'd", "he"),
    ("chocked", "chalked"), ("chalked", "chocked"),
}

ALIASES = {"thompson": "thomson", "center": "centre", "st": "saint"}
NUMBER_WORDS = set(("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen "
                    "fifteen sixteen seventeen eighteen nineteen twenty thirty forty fifty sixty seventy eighty "
                    "ninety hundred thousand oh first second").split())
NUMBER_WORDS |= {w + "s" for w in ("hundred", "thousand")}
NUMBER_WORDS |= set(("third fourth fifth sixth seventh eighth ninth tenth eleventh twelfth thirteenth fourteenth "
                     "fifteenth sixteenth seventeenth eighteenth nineteenth twentieth thirtieth").split())
NUMERAL = re.compile(r"^\d+(st|nd|rd|th|s)?$")


def norm(text: str) -> list[str]:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = text.lower().replace("\u2019", "'").replace("**", "")
    words = re.sub(r"[^a-z0-9' -]+", " ", text).replace("-", " ").split()
    pieces = [p.strip("'") for w in words for p in ALIASES.get(w, w).split()]
    is_num = [bool(NUMERAL.match(p)) or p in NUMBER_WORDS for p in pieces]
    out = []
    for i, piece in enumerate(pieces):
        if not piece or is_num[i]:
            continue
        nxt = i + 1 < len(pieces) and is_num[i + 1]
        if piece in ("a", "an") and nxt:
            continue
        if piece == "and" and nxt and i > 0 and is_num[i - 1]:
            continue
        out.append(piece)
    return out


def soft_equal(a: str, b: str) -> bool:
    if a == b:
        return True
    if (a, b) in SPELL_OK:
        return True
    # contractions: she had / she'd
    if a.replace("'", "") == b.replace("'", ""):
        return True
    if difflib.SequenceMatcher(None, a, b).ratio() >= 0.85:
        return True
    return False


def load_audio_np(path: Path):
    """Decode via ffmpeg → float32 mono 16k (avoids PyAV metadata_errors)."""
    import numpy as np
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(path), "-f", "f32le", "-acodec", "pcm_f32le",
         "-ac", "1", "-ar", "16000", "-"],
        check=True, capture_output=True,
    ).stdout
    return np.frombuffer(raw, dtype=np.float32)


def transcribe(path: Path):
    from faster_whisper import WhisperModel
    model = WhisperModel("small.en", device="cpu", compute_type="int8")
    try:
        segs, info = model.transcribe(str(path), word_timestamps=True)
        words = []
        texts = []
        for s in segs:
            texts.append(s.text)
            for w in (s.words or []):
                words.append({"start": round(w.start, 2), "end": round(w.end, 2), "word": w.word.strip()})
        return " ".join(texts).strip(), words
    except TypeError as e:
        if "metadata_errors" not in str(e):
            raise
        audio = load_audio_np(path)
        segs, info = model.transcribe(audio, word_timestamps=True)
        words = []
        texts = []
        for s in segs:
            texts.append(s.text)
            for w in (s.words or []):
                words.append({"start": round(w.start, 2), "end": round(w.end, 2), "word": w.word.strip()})
        return " ".join(texts).strip(), words


def classify_diff(script_words, heard_words):
    missing = added = changed = soft = 0
    notes = []
    for op, a1, a2, b1, b2 in difflib.SequenceMatcher(None, script_words, heard_words, autojunk=False).get_opcodes():
        if op == "equal":
            continue
        sw = script_words[a1:a2]
        hw = heard_words[b1:b2]
        if op == "replace":
            # pair-wise soft
            if len(sw) == len(hw) and all(soft_equal(x, y) for x, y in zip(sw, hw)):
                soft += len(sw)
                notes.append({"op": "soft_replace", "script": " ".join(sw), "heard": " ".join(hw)})
            else:
                # count as changed; also track length delta as missing/added
                changed += max(len(sw), len(hw))
                if len(sw) > len(hw):
                    missing += len(sw) - len(hw)
                elif len(hw) > len(sw):
                    added += len(hw) - len(sw)
                notes.append({"op": "replace", "script": " ".join(script_words[max(0,a1-2):a2+2]),
                              "heard": " ".join(heard_words[max(0,b1-2):b2+2]),
                              "script_span": " ".join(sw), "heard_span": " ".join(hw)})
        elif op == "delete":
            missing += len(sw)
            notes.append({"op": "delete", "script": " ".join(script_words[max(0,a1-2):a2+2]),
                          "heard": " ".join(heard_words[max(0,b1-2):b2+2]),
                          "script_span": " ".join(sw)})
        elif op == "insert":
            added += len(hw)
            notes.append({"op": "insert", "script": " ".join(script_words[max(0,a1-2):a2+2]),
                          "heard": " ".join(heard_words[max(0,b1-2):b2+2]),
                          "heard_span": " ".join(hw)})
    # Claude: pass with no missing or added; small spelling diffs fine
    hard = missing + added
    # also treat non-soft replaces of same length as "changed" — Claude said missing/added;
    # real content change (a→the) is a changed word, count as fail if not soft
    hard_changed = sum(1 for n in notes if n["op"] == "replace")
    verdict = "PASS" if hard == 0 and hard_changed == 0 else "FAIL"
    return {
        "missing": missing,
        "added": added,
        "changed_ops": hard_changed,
        "soft_spelling": soft,
        "verdict": verdict,
        "notes": notes,
    }


def main():
    summary = []
    for num, slug in PARTS:
        mp3 = VO / f"part{num}_{slug}_v01.mp3"
        txt = VO / f"part{num}_{slug}.txt"
        extract = txt.read_text(encoding="utf-8")
        print(f"=== part{num} transcribing {mp3.name} ===", flush=True)
        transcript, words = transcribe(mp3)
        (OUT / f"part{num}_transcript.txt").write_text(transcript + "\n", encoding="utf-8")
        (OUT / f"part{num}_whisper_words.json").write_text(json.dumps(words, indent=2), encoding="utf-8")
        sw = norm(extract)
        hw = norm(transcript)
        diff = classify_diff(sw, hw)
        # also write unified-ish text diff of raw lowercased
        ud = list(difflib.unified_diff(
            extract.strip().splitlines(),
            [transcript],
            fromfile=f"extract_part{num}",
            tofile=f"whisper_part{num}",
            lineterm="",
        ))
        (OUT / f"part{num}_diff.json").write_text(json.dumps({
            "part": num,
            "slug": slug,
            "extract_words_norm": len(sw),
            "heard_words_norm": len(hw),
            "extract_raw_words": len(extract.split()),
            **{k: diff[k] for k in ("missing", "added", "changed_ops", "soft_spelling", "verdict")},
            "notes": diff["notes"],
            "script_norm_preview": " ".join(sw[:40]) + "...",
            "heard_norm_preview": " ".join(hw[:40]) + "...",
        }, indent=2), encoding="utf-8")
        (OUT / f"part{num}_unified.diff").write_text("\n".join(ud) + "\n", encoding="utf-8")
        row = {
            "part": num,
            "slug": slug,
            "extract_words": len(extract.split()),
            "norm_script": len(sw),
            "norm_heard": len(hw),
            **{k: diff[k] for k in ("missing", "added", "changed_ops", "soft_spelling", "verdict")},
            "hard_notes": [n for n in diff["notes"] if n["op"] != "soft_replace"],
            "soft_notes": [n for n in diff["notes"] if n["op"] == "soft_replace"],
        }
        summary.append(row)
        print(f"part{num}: verdict={row['verdict']} missing={row['missing']} added={row['added']} "
              f"changed_ops={row['changed_ops']} soft={row['soft_spelling']}", flush=True)
        for n in row["hard_notes"]:
            print(f"  HARD {n['op']}: script='{n.get('script_span', n.get('script'))}' heard='{n.get('heard_span', n.get('heard'))}'", flush=True)
    (OUT / "wordcheck_results.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
