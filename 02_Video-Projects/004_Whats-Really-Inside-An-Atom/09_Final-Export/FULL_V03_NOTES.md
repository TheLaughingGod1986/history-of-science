# HOS 004 full_v03 — two-section music (UAT · STOP listen)

**Cut:** `hos_004_full_v03.mp4`  
**sha256:** `503e228745d4cf87fe6f504522cbad99f6af0f9c8b038c1ed8c52da493428157`  
**Duration:** 524.700 s · **A/V Δ:** 0.000000 s  
**Status:** **UNUSED / PARKED.** Ben PASSed music on **full_v02** (sha `ed870939…`), not v03. Keep file aside; do not upload; do not regenerate. No KEEP label.

Picture locked from `hos_004_full_join_v03.mp4` (Ben PASS). VO v04 masters untouched.

## Why v03

Plain part-05 VO v04 ends **“That's the next story”** — no extra **“you”** (STT + faster-whisper).  
Sect2 bed v01 could bleed choir/vocal texture into the word check. Regenerated sect2 with an explicit ban on choir / voices / vocal pads / humming.

## Music (no loop)

| Section | File | Window |
|---|---|---|
| 1 | `hos004-full_score_bed_v01.mp3` | 0:00 → Part 05 chapter card (355.478 s = 5:55.48) |
| 2 | `hos004-full-sect2_score_bed_v02.mp3` | card → cream end (504.694 s) |
| Join | acrossfade **1.5 s** under the Part 05 chapter card | — |

Gap **−20 dB**. Extra ~3 dB duck under speech. `amix normalize=0`. Fade across cream · silent under hold.

Sect2 prompt adds: **no choir, no voices, no vocal pads, no humming**.

Builder: `07_Edit-Project/_mix_hos_004_full_v03_music.py`

## vo_check + levels (29 Sep 2026)

```
FAIL  full_v03.wav  8:44.70  mean -23.6 dB  peak -3.8 dB  147 wpm
   FAIL  replace at ~6:07.50: script 'a living' / heard 'the living'
   FAIL  replace at ~7:40.30: script 'a weight' / heard 'of weight'
   FAIL  insert at ~8:06.14: script 'the next story' / heard 'the next story you'
```

Film `−t 500.69`: mean **−23.4** / max **−3.8** dB.

**Listen note:** faster-whisper on the plain VO end and on full_v03 end both hear **“That's the next story”** with **no “you”**. The 8:06 vo_check insert is likely alignment noise — **Ben decides at 8:06**.
