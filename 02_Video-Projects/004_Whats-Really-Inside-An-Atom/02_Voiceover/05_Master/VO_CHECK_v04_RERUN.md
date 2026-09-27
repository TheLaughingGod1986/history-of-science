# vo_check v04 rerun — 27 Sep 2026

**Env:** `.venv-hos` · `faster-whisper 1.2.1` installed · PR **#141** on main (`45333fe`)  
**Command base:** `00_Brand/Channel-Setup/tools/vo_check.py`  
**Script:** `01_Script/atom_script_master_v02.md`  
**VO status:** **KEEP** (Ben listened at 3:38, 6:06 and 7:39, 27 Sep 2026; the three FAILs are the transcriber)

Every check below **ran** (word diff + loudness + pauses + pace). Nothing SKIPPED.

| File | Result | Word check | Loudness | Notes |
|---|---|---|---|---|
| `hos_004_part01_vo_v04.mp3` | **PASS** | ran · pass | ran · pass (−23.8 / −4.2) | 1:09.81 · 158 wpm · title_q 8.64s |
| `hos_004_part02_vo_v04.mp3` | **PASS** | ran · pass | ran · pass (−22.0 / −4.1) | 1:31.20 · 154 wpm |
| `hos_004_part03_vo_v04.mp3` | **PASS** | ran · pass | ran · pass (−23.4 / −4.1) | 1:23.73 · 148 wpm |
| `hos_004_part04_vo_v04.mp3` | **PASS** | ran · pass | ran · pass (−24.7 / −4.1) | 1:49.02 · 154 wpm |
| `hos_004_part05_vo_v04.mp3` | **FAIL** | ran · **fail** | ran · pass (−24.3 / −4.4) | see holds below |
| `hos_004_vo_all_parts_listen_v04.mp3` | **FAIL** | ran · **fail** | ran · pass (−23.6 / −4.1) | see holds below |

## Word-diff holds Ben is listening

| Film time | Script | Heard (faster-whisper) | Where flagged |
|---|---|---|---|
| **~3:38** | `…call them electrons **but** atoms have no…` | `…call them electrons **for** atoms have no…` | listen FAIL only (Part 03 alone PASS) |
| **~6:06** | `…the bones in **a** living hand…` | `…the bones in **the** living hand…` | Part 05 FAIL (~0:18.30) · listen FAIL |
| **~7:39** | `…gave each kind **a** weight…` | `…gave each kind **of** weight…` | Part 05 FAIL (~1:51.72) · listen FAIL |

Do **not** remint 7:39 unless Ben asks after listen (would be one sentence + Part 05 retime only).

## Verbatim — Part 05

```
FAIL  hos_004_part05_vo_v04.mp3  2:24.52  mean -24.3 dB  peak -4.4 dB  157 wpm
   FAIL  replace at ~0:18.30: script 'the bones in a living hand moseley' / heard 'the bones in the living hand moseley' — listen, then regenerate that sentence alone if real
   FAIL  replace at ~1:51.72: script 'gave each kind a weight thomson found' / heard 'gave each kind of weight thomson found' — listen, then regenerate that sentence alone if real
   warn  replace at ~0:16.06: script 'same invisible light rontgen used to see' / heard 'same invisible light runt gun used to see' — sounds alike (likely the transcriber); listen
   warn  replace at ~0:41.20: script 'in its nucleus van den broek's guess was right' / heard 'in its nucleus vanden brookes guess was right' — sounds alike (likely the transcriber); listen
```

## Verbatim — listen

```
FAIL  hos_004_vo_all_parts_listen_v04.mp3  8:19.69  mean -23.6 dB  peak -4.1 dB  154 wpm
   first minute: title_question 8.64s  promise 11.34s  stakes 17.74s
   FAIL  replace at ~3:38.50: script 'call them electrons but atoms have no' / heard 'call them electrons for atoms have no' — listen, then regenerate that sentence alone if real
   FAIL  replace at ~6:06.38: script 'the bones in a living hand moseley' / heard 'the bones in the living hand moseley' — listen, then regenerate that sentence alone if real
   FAIL  replace at ~7:39.70: script 'gave each kind a weight thomson found' / heard 'gave each kind of weight thomson found' — listen, then regenerate that sentence alone if real
   warn  re-checked 6:31.38: 'sort the table by that number tellurium is and iodine is cobalt is and nickel is' is present (the full-file transcription skipped it)
   warn  replace at ~2:38.42: script 'what is cambridge j j thomson is studying' / heard 'what is cambridge jj thomson is studying' — sounds alike (likely the transcriber); listen
   warn  replace at ~3:34.98: script 'thomson called them corpuscles today we call' / heard 'thomson called them core puzzles today we call' — sounds alike (likely the transcriber); listen
   warn  replace at ~6:03.60: script 'same invisible light rontgen used to see' / heard 'same invisible light runt gun used to see' — sounds alike (likely the transcriber); listen
```
