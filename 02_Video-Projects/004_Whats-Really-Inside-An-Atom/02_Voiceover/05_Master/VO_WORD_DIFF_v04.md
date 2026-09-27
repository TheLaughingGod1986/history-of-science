# VO word-diff v04 vs atom_script_master_v02.md

**Transcriber:** ElevenLabs Scribe (`04_Audio/tools/transcribe_vo.py`) — same as earlier v04 STT.
**Normalisation:** `vo_check.py` rules (drop number-words/digits; alias Thomson/centre/etc.).
**Why:** `vo_check` skipped the word check (no `faster-whisper`). atempo 1.03 should not drop words — confirm.

**Part 05 note:** Scribe heard *bones in **the** living hand*; script is *bones in **a** living hand*. Locked VO matches the script (confirmed earlier). Not a dropped word from atempo.

**Verdict:** PASS for atempo word integrity — Parts 01–04 exact; Part 05 / listen show one Scribe article (*a*→*the* living hand). No content words missing.

## Part 01 — PASS
- audio: `hos_004_part01_vo_v04.wav`
- STT: `_stt_v04/hos-004-part01-vo-v04_transcript.txt`
- script_words=177 · heard_words=177
- no material diffs

## Part 02 — PASS
- audio: `hos_004_part02_vo_v04.wav`
- STT: `_stt_v04/hos-004-part02-vo-v04_transcript.txt`
- script_words=230 · heard_words=230
- no material diffs

## Part 03 — PASS
- audio: `hos_004_part03_vo_v04.wav`
- STT: `_stt_v04/hos-004-part03-vo-v04_transcript.txt`
- script_words=196 · heard_words=196
- no material diffs

## Part 04 — PASS
- audio: `hos_004_part04_vo_v04.wav`
- STT: `_stt_v04/hos-004-part04-vo-v04_transcript.txt`
- script_words=270 · heard_words=270
- no material diffs

## Part 05 — DIFFS×1
- audio: `hos_004_part05_vo_v04.wav`
- STT: `_stt_v04/hos-004-part05-vo-v04_transcript.txt`
- script_words=349 · heard_words=349
- `replace` script=`a` · heard=`the`

## Full listen — DIFFS×1
- audio: `hos_004_vo_all_parts_listen_v04.wav`
- script_words=1222 · heard_words=1221
- `replace` script=`a` · heard=`the`

