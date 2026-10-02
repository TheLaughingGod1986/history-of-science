## 005: Ben's pass recorded, master copied, Shorts A–C v01 built (all checks PASS), package prep PASS. Nothing public

### 1. Ben's pass and the master

- Recorded in `production-status.md`: **Ben passed full join v01 (sha `84476e06…`, 8:46.5), 2 Oct 2026; listen-pass at 5:06/5:35 = clean; 8:20 curl = no trim.**
- Master: `09_Final-Export/hos_005_master_v01.mp4`. It is a byte copy of the join, not a re-encode: sha256 `84476e06c13e2a010974bc0937a7044374f637065edcf819c5ab5157165192f7` (same as the join), 526.533 s.

### 2. Shorts A–C v01

All three are built from KEEP plates only. **No new mints and no spend.** Every beat had a usable KEEP.

| Short | File (`10_Shorts/`) | Length | sha256 | Air (gate date) |
|---|---|---|---|---|
| A, the sum | `hos_005_s01_the_sum_v01.mp4` | 24.07 s | `732bca40629e9854800c6a7e8f400a6cde821a1183a7fe0803c7c83bca16d97b` | Fri 30 Oct |
| B, the tied arm | `hos_005_s02_the_tied_arm_v01.mp4` | 25.83 s | `e2eacb0c6d3e8b5828c69dc534860ce4e3d17544fed457f30c59ae3a144e0baf` | Sun 1 Nov |
| C, never saw | `hos_005_s03_never_saw_v01.mp4` | 24.83 s | `5839c4dd1e93dd0d11ae9c2c1191559662845b0c8d07731b2058365a25becbc4` | Tue 3 Nov |

Phone copies: iCloud `HOS UAT/005_How-Harvey-Proved-Blood-Circulates/10_Shorts/`. Builder: `10_Shorts/_build_shorts_v01.py`. Record: `10_Shorts/SHORTS_INDEX_v01.json`, which holds the per-Short plan (plate, in-point, crop, the word each cut lands on).

**VO.** The Shorts scripts differ from the long, so the lines are new takes with Ben Orbit Narrator (`kDch6ACCIpqgQ0NsU9kk`, `eleven_v3`, `settings_for_part(1)`, speed 1.04). The text is each Short's "Script" paragraph, word for word (`10_Shorts/_generate_shorts_vo_v01.py`).
- A and B use take a.
- C uses take b. Take a read slowly (130 wpm, 26.8 s) and peaked at −0.9 dB. Take b came in at 142 wpm and passed.
- Finish (`_finish_shorts_vo_v01.py`) is the long's step 1 only: pauses over 0.6 s cut to 0.6 s, lead-in trimmed, peak set to −2 dB. **No `atempo`.** The word timings were remapped through the same cuts, so the captions stay on the words.

**Picture.**
- Static 9:16 crops, with one fixed offset per plate. There is no animated crop, because 004 s02 v05 failed Ben's phone watch on crop wobble.
- Each cut lands on its sentence. The last 4.0 s is the opening plate, so each Short loops.
- Each Short has a hook caption on frame 0 with the yellow hook word (MORE THAN YOU **HAVE** / ONE TIGHT **BAND** / HE NEVER **SAW** THIS), plus word-timed captions.
- The exact title *The Tied Arm That Proved Your Blood Circulates* is on screen at 9.0–14.0 s over a soft top shade.
- The bed is the part's TEMP bed at VO mean −20 dB.
- The Explorer is in none of the three Shorts.

**Changes from the script tables, for your check:**
- **A, 5–14 s.** Part 03's "2 oz" page (06) doesn't survive a 9:16 crop: the page holds still while the quill is out of frame (freezedetect 1.3 s). So:
  - 07's finished list "2 oz / 1/8 / 1000" (correct, checked by hand) carries "two ounces… an eighth" in a 900 px window over a blurred fill, so all three numbers stay readable.
  - Then 03/04 (squeeze ripple down the arm) runs under "of that goes out. In half an hour".
  - Then 01/09 (a fingertip counting beats by the clock) runs under "it beats more than a thousand times".
- **B, 20–26 s.** "Look at your hand. That blood is heading home now." plays over the loop: the band plate, a hand with its veins swelling blue. This replaces the separate back-of-hand plate, which would have left only 0.5 s before the loop.
- **B opening.** The in-point is 0.8 s with crop x 640. The first cut gave a motion warning (8.5 < 10); this one measures 19.2.

`gate_shorts_open.py check <mp4> --air-date …`:
```
PASS  hos_005_s01_the_sum_v01.mp4  dur=24.07s  audio=-21.2dB  motion=27.31  dhash=4b5307236a79723b
PASS  hos_005_s02_the_tied_arm_v01.mp4  dur=25.83s  audio=-21.6dB  motion=19.22  dhash=070f46033fa90e0e
PASS  hos_005_s03_never_saw_v01.mp4  dur=24.83s  audio=-21.7dB  motion=17.01  dhash=0f0f0d1f6e030f0f
```

`vo_check.py <mp4> --script 10_Shorts/vo_v01/<id>.txt` (on the finished Shorts, hos-vo venv, word check on):
```
PASS  hos_005_s01_the_sum_v01.mp4  0:24.07  mean -21.2 dB  peak -2.0 dB  157 wpm
   warn  replace at ~0:03.22: script 'have london doctor proved it with a' / heard 'have london doctor approved it with a' — sounds alike (likely the transcriber); listen
PASS  hos_005_s02_the_tied_arm_v01.mp4  0:25.83  mean -21.6 dB  peak -1.9 dB  146 wpm
   warn  replace at ~0:00.26: script 'band proved your blood goes' / heard 'band proves your blood goes' — sounds alike (likely the transcriber); listen
PASS  hos_005_s03_never_saw_v01.mp4  0:24.83  mean -21.7 dB  peak -2.0 dB  140 wpm
   warn  pace 140 wpm (< 145); expect a long film — see STUDIO_PLAYBOOK.md §4 speed
```

freezedetect (n 0.003, d 0.8): **0 events** on all three. The caption-change check (every 0.5 s) passed with 20, 20 and 19 changes, ratio 1.0.

**Listen items for Ben's phone watch:** "proved" at 0:03 in A and at 0:00 in B. If either really says "approved" or "proves", I regenerate that sentence alone.

**Schedule question.** You set Fri 30 Oct, Sun 1 Nov and Tue 3 Nov for A, B and C. `HOS_STRATEGY.md` says each Short in a week promotes a different film. `SHORTS_SCRIPTS_v01.md` also says B and C belong to later weeks unless Ben says otherwise. Three 005 Shorts in the 29 Oct week would break that rule. I gated them on those dates, but none is scheduled. Please confirm the dates with Ben, or give me B and C dates in later weeks.

### 3. Package prep (nothing uploaded or scheduled)

`neighbours.py "blood circulation" "william harvey" --phrase blood --phrase heart --manifest …`: **gate PASS**, 6 at 1M+, TED-Ed yes. One of the six, a TEDx talk on listening found by "william harvey ted", is noise; the manifest block keeps the five on-topic videos:

| # | Channel | Views | Title |
|---|---|---:|---|
| 1 | TED-Ed | 17,959,080 | How blood pressure works - Wilfred Manzano |
| 2 | Amoeba Sisters | 7,390,037 | Circulatory System and Pathway of Blood Through the Heart |
| 3 | TED-Ed | 6,734,275 | Why do blood types matter? - Natalie S. Hodge |
| 4 | TED-Ed | 4,459,222 | How the heart actually pumps blood - Edmond Hui |
| 5 | TED-Ed | 1,419,073 | What happens if you're injected with the wrong blood type? - Bill Schutt |

Evidence: `11_Upload-Package/evidence_2026-10-02_neighbours.json`.

**Description v02** (`Descriptions/blood_long_description_v02.txt`). The first two lines:
> Your heart pumps more blood in half an hour than your whole body holds. So where does it all go?
> For 1,400 years doctors taught that blood was made from food and used up, until William Harvey proved it circulates, with a sum and a band tied round an arm.

The chapters are re-timed from the master's cards: 0:00 The used-up blood · 0:57 The liver that made blood · 2:37 The sum that broke the old idea · 4:16 The tied arm · 6:25 The vessels he never saw. The sources are unchanged.

**Tags (7, unchanged):** blood circulation · heart · william harvey · circulatory system · capillaries · history of medicine · history of science.

**Manifest:** `video` = the master, `schedule` `2026-10-29T18:00:00.000Z`, private, not Made for Kids, altered content yes, no Premiere.

`npm run lint:package -- --film 005`:
```
PASS  02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/11_Upload-Package/PACKAGE_MANIFEST.json
   warn  [captions] no captionsFile (captions from the script)
```

**Still needed before upload, all for Ben to sign off:** the title (*The Tied Arm That Proved Your Blood Circulates*, B: *Why Doctors Thought Your Blood Was Used Up*), the **thumbnail** (not made yet; say if I should start it) and description v02.

### Spend

None. Vertex is unchanged at $190.63 for the film. The ElevenLabs Shorts VO is 5 takes, about 1,600 characters.

Image: the title frame (11.5 s) of A, B and C.
