## 005 full join v01 built (8:46.5). One check needs a decision: `vo_check` on the whole film prints FAIL on two transcriber misses of "Fabricius"

The full join is built and on the phone. Every part is in, with chapter cards, the end card and the 20 s end-screen hold. **It is not ready to call done.** `vo_check` on the whole film prints FAIL, so I am not asking for Ben's sign-off on my own. Details are under `vo_check` below. My read is that the transcriber is wrong, not the voice. If you agree after a listen, it goes to Ben for the moving-picture sign-off.

**File on the Mini:** `/Users/benjaminoats/YouTube/hos-005-blood/02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/09_Final-Export/hos_005_full_join_v01.mp4`
- sha256 `84476e06c13e2a010974bc0937a7044374f637065edcf819c5ab5157165192f7`, 526.533 s (8:46.5), 1920×1080 30 fps CFR, AAC stereo 48 kHz.
- Phone copy: iCloud `HOS UAT/005_How-Harvey-Proved-Blood-Circulates/09_Final-Export/hos_005_full_join_v01.mp4`.
- Built by `07_Edit-Project/_join_full_v01.py`. Record: `07_Edit-Project/full_join_v01_meta.json`.

### What's in it

| Part | Picture | Film start | Card in |
|---|---|---|---|
| 01 | Ben's passed rough v01 (`7661b6cf…`), unchanged | 0:00.00 | — |
| 02 | rough v02's plates and labels | 0:59.53 | 0:57.62 *PART 02 · c. AD 170 · The Liver That Made Blood* |
| 03 | rough v02's (with the 03/07 remint) | 2:39.61 | 2:37.71 *PART 03 · 1616 · The Sum That Broke the Old Idea* |
| 04 | rough v01's | 4:18.31 | 4:16.41 *PART 04 · 1628 · The Tied Arm* |
| 05 | rough v01's | 6:27.05 | 6:25.15 *PART 05 · 1661 · The Vessels He Never Saw* |
| End | cream card *History of Science · DISCOVERY. WONDER. PROOF.* (004's card) | 8:22.52 | 4 s, then the 20 s quiet hold for the Studio end screen (8:26.5–8:46.5) |

- **Timing** follows `VO_RETIME_v01.json`. Each card cross-fades in (0.35 s) 0.6 s after the last word. It holds to 0.1 s before the next part's first word, then fades out over 0.25 s. No card lands on a word. The card times match the retime to within 0.02 s.
- **Music** is each part's TEMP bed at the rough's level (−20 dB under VO). It carries on under the card and cross-fades (0.4 s) into the next part's bed. It fades out over the end card. The 20 s end-screen hold is quiet, as on 004 v03.
- **Picture:** the parts' own plates, labels and hard cuts, with no fade to black between parts. Under each card, the last plate holds its final frame only while the card is fully opaque.
- **Card dates, for your check:** c. AD 170 (Galen, the script's label). 1616 (Harvey's first College lectures, "London, sixteen-sixteen" in Part 01). 1628 (*De Motu Cordis*, where the tied-arm proof was published). 1661 (Malpighi, the script's label). 1616 and 1628 are my choice. Swap them for place names if you'd rather.

### Checks

freezedetect (n 0.003, d 0.8): 5 events, all inside the chapter-card and end-card holds, none in the story:
```
57.97–59.43 · 158.10–159.53 · 256.77–258.23 · 385.50–386.97 · 503.03–526.50
```

`vo_check.py` on the full join (hos-vo venv, word check on):
```
FAIL  hos_005_full_join_v01.mp4  8:46.53  mean -21.8 dB  peak -2.1 dB  143 wpm
   first minute: title_question 49.6s  promise 15.94s
   FAIL  replace at ~5:06.28: script 'valve the flaps fabricius found harvey presses' / heard 'valve the flaps vibrisius found harvey presses' — listen, then regenerate that sentence alone if real
   FAIL  replace at ~5:35.24: script 'towards the heart fabricius thought they slowed' / heard 'towards the heart vibrisius thought they slowed' — listen, then regenerate that sentence alone if real
   warn  silence 22.42s at 8:24.09 (part join?)
   warn  pace 143 wpm (< 145); expect a long film — see STUDIO_PLAYBOOK.md §4 speed
   warn  replace at ~2:07.42: script 'old professor called fabricius fabricius had found something' / heard 'old professor called fabrizius fabrizius had found something' — sounds alike (likely the transcriber); listen
   warn  replace at ~2:20.20: script 'vein need doors fabricius thought they slowed' / heard 'vein need doors fabrizius thought they slowed' — sounds alike (likely the transcriber); listen
   warn  replace at ~7:34.38: script 'wraps a cuff round your arm think' / heard 'wraps a cuff around your arm think' — sounds alike (likely the transcriber); listen
```

**Why I think the two FAILs are the transcriber, not the voice:**
- Both are the word "Fabricius" in Part 04, from the locked VO v01 take Ben OK'd. Not a word was changed.
- Run on Part 04 alone, the same audio hears "fabriceus". That counts as "sounds alike", so it's a warning, and the part PASSes.
- To show the join didn't change the audio, I cut Part 04's window out of the join (4:18.30, 128.24 s) and ran the check again:
  ```
  PASS  join_p04_window.mp4  2:08.27  mean -22.0 dB  peak -2.2 dB  153 wpm
     warn  replace at ~0:52.36: … heard 'valve the flaps fabriceus found harvey presses' — sounds alike (likely the transcriber); listen
     warn  replace at ~1:22.60: … heard 'towards the heart fabriceus thought they slowed' — sounds alike (likely the transcriber); listen
  ```
  So on a 2-minute window the transcriber hears "fabriceus". On the 8:46 whole it drifts to "vibrisius".

I have not edited, skipped or swapped the check.

**The other warnings:**
- The 22.4 s silence is the end-screen hold, as on 004.
- 143 wpm is the whole film including cards and the hold. Each part is 149–153 wpm.

**Two ways forward. Your call, or Ben's:**
1. Listen at 5:06 and 5:35. If "Fabricius" is clean, record a listen-pass on the two lines (Ben's call) and send the join to Ben.
2. If it isn't clean, I regenerate those two sentences alone with Ben Orbit Narrator (no other change) and rebuild Part 04 and the join.

A fix to how `vo_check` transcribes long files (for example, per part) would go in its own PR, with Ben's OK.

### Spend

None for the join. Film total on Vertex: $190.63. Projected Free Trial £57.03 (floor £20); the console reads £110.07, status Available.

Stills: the Part 02 card · the last line (the pond drop) · the end card.
