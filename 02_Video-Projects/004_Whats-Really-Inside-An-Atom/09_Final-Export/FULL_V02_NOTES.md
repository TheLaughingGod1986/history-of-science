# HOS 004 full_v02 — two-section music (UAT)

**Cut:** `hos_004_full_v02.mp4`  
**sha256:** `ed870939f476d326197cdaf1403ce7064850d4286ff63aa81bc5a7584761e98e`  
**Duration:** 524.700 s · **A/V Δ:** 0.000000 s  
**Status:** UAT for Ben music listen. Do **not** label KEEP. No upload.

Picture locked from `hos_004_full_join_v03.mp4` (Ben PASS 29 Sep, sha `f88cb9d47e910425519a40a6af7649626c47afbcdddf1f0f3293564c59f65244`).  
VO v04 masters untouched.

## Music (no loop)

| Section | File | Window |
|---|---|---|
| 1 | `hos004-full_score_bed_v01.mp3` | 0:00 → Part 05 chapter card (355.478 s = 5:55.48) |
| 2 | `hos004-full-sect2_score_bed_v01.mp3` | card → cream end (504.694 s) |
| Join | acrossfade **1.5 s** under the Part 05 chapter card | — |

Gap level **−20 dB**. Extra ~3 dB duck under speech (`threshold=0.012:ratio=12:attack=20:release=500:level_sc=1`).  
`amix=inputs=2:weights=1 1:normalize=0`. Fade across cream · silent under 20 s hold.

Builder: `07_Edit-Project/_mix_hos_004_full_v02_music.py`

## vo_check paste (29 Sep 2026)

```
FAIL  full_v02.wav  8:44.70  mean -23.6 dB  peak -3.8 dB  147 wpm
   first minute: title_question 8.68s  promise 11.36s  stakes 17.98s
   FAIL  replace at ~6:07.50: script 'a living' / heard 'the living'
   FAIL  replace at ~7:40.30: script 'a weight' / heard 'of weight'
   FAIL  insert at ~8:06.14: script 'the next story' / heard 'the next story you'
```

Mean on 0:00–8:20.69 (`-t 500.69`): **−23.4 dB** mean / **−3.8 dB** max.  
A/V delta: **0.000 s**.

Expected 6:07 + 6:31 only — **6:31 did not flag** this run. **5:34 did not flag** on full. **7:40 did flag** → window compare: full_v02 and plain Part 05 v04 VO hear the same (“kind of…”); not a mix fault. Plain Part 04 still flags `van den`→`van der` at local ~1:33.
