# J2170 — HOS 008 Short C (`How Does a Lightning Rod Work?`): Paper Hook Resolution, `J1881`/`J2163` Plate Inventory, and Conditional 2 Dec Slot Disposition

- **Job**: `J2170` (`HOS 008 Short C: resolve blocked hook on paper for conditional 2 Dec slot`)
- **Parent Plan**: `J2023` (`Chief: fill Short gaps (HOS none after 17 Nov and 9-12 Nov; OWB 24-29 Nov) from finished or nearly finished Shorts`)
- **Film / Stage**: `HOS:008` (`02_Video-Projects/008_Lightning-Franklin`) · `edit`
- **Author / Worker**: `gemini` (`gemini-4-argon-high`)
- **Date**: `2026-11-05`
- **Spend & Production Lock**: **`£0` / `0` credits**. No voiceover recorded, no Flow/Vertex generation, no media modified, no upload, no scheduling, no privacy/retitle or Buffer writes. Locked files `10_Shorts/SHORTS_SCRIPTS_v02.md`, `10_Shorts/SHORTS_PICTURE_PLAN_v02.json`, and `10_Shorts/vo_v02/*` remain untouched (`status: "blocked_hook_and_missing_plates"` preserved).

---

## 1. Executive Summary & Slot Disposition (`2 Dec 2026 11:30Z`)

1. **Existing Audio Cannot Meet the `<= 2.85 s` Hook Gate (`J1004` Confirmed + Long Part 05 Audited)**:
   - In `10_Shorts/vo_v02/hos_008_short_C_v02.mp3` (`sha256: ba8ffec9c234c68961e5d7e3811d8104feb7d5485ab9d567c10ff91604803d08`), Sentence 1 (`w[00..12]`, 13 words: *"That thin metal rod on top of tall buildings was Benjamin Franklin's idea."*) spans `0.080–4.840 s` (**`4.840 s > 2.85 s`**). Pure speech across all 13 words is **`3.720 s` at `1.00x`**, which is **`3.509 s > 2.85 s`** even at the studio cap `atempo = 1.06x` with zero onset and zero inter-word gaps.
   - The unapproved `e1bbcfb9` proposal to excise 5 mid-sentence words (`w[04..08]`, *"on top of tall buildings"*, `1.580–3.060 s`) both violates the `AGENTS.md` Never list (*"Never change a word of the signed-off script in VO (regenerate the sentence instead)"*) and fails arithmetic (`4.840 - 1.600 = 3.240 s > 2.85 s` at `1.00x`).
   - Auditing the locked Long Part 05 VO (`02_Voiceover/hos_008_part05_the_rod_on_every_roof_v01b.mp3`, `sha256: e5e86140d0b7e5598eb8eeca39d0f260c2dcc9b698b36c119a8c51283c990c38`) confirms no contiguous `22–27 s` lightning-rod mechanism passage opens with a `<= 2.85 s` Sentence 1 naming both the subject (`lightning rod`) and a surprise claim (`LEARNINGS.md` Rules 2 & 8).
   - Therefore, the conditional **Wednesday 2 December 2026 11:30Z** slot (Ben watch by **29 November 2026**) is **explicitly NOT achievable on existing audio alone**, and remains **HELD / EMPTY** until (a) Chief/Claude approve the concise 1-sentence opening pickup below under valid credit scope, (b) `Short_C` `v03` is assembled at `£0` and passes all gates + Ben's final watch, and (c) HOS `008` Long (*Why Did Franklin Fly a Kite in a Storm?*, currently in `J1881`/`J2163` six-note correction scope) is public on YouTube.

2. **Duplicate Public/Scheduled Ideas & `Short_A` (`J0912`) Separation**:
   - **Channel Snapshot (`05_Analytics/hos/snapshots/2026-11-04.json`, 62 videos) & `SHORTS_LOG.md` Audit**: Zero public or scheduled HOS Shorts cover lightning, Benjamin Franklin, kites, or lightning rods.
   - **`008 Short_A` (`J0912`, conditional target 24 Nov / watch 20 Nov) Separation**: `Short_A` (*Did Lightning Hit Franklin's Kite?* / *Franklin's Kite Experiment: Was It Hit by Lightning?*) covers the June 1752 kite-and-key charge experiment using `P1:01_kite_open`, `P3:19_kite_climb`, `P3:13_key_ribbon`, `P3:25_fibres_rise`, `P4:02_knuckle_spark`, `P4:08_teach_charge`, and `P4:10_richmann_rod`. `Short_C` (*How Does a Lightning Rod Work?*) covers the rooftop lightning rod's low-resistance ground path and shares **zero** plates, VO words, or claims with `Short_A`.

3. **Approved Existing Long Plates vs `J1881` / `J2163` Six-Note Corrections**:
   - All 6 `J1881` / `J2163` UAT notes on `master_v03` (`00:20` `P1:03_table_three`, `0:30` `P1:03b_town_safe -> P1:04_storm_mystery`, `1:49` `P2:02_salon_spark`, `2:20` `P2:07_foil_jar`, `3:31` `P3:04_letter_crosses`, `7:58` `P5:13_rods_spread`) are **100% disjoint** from `Short_C`'s plate pool. Defective `P5:13_rods_spread` (`13_rods_spread_t1.mp4`, `d9fa5f13...`, where rods kink/detach after `1.50 s` and ship masts are absent) is explicitly excluded.
   - All 8 moving Flow Veo plates for `Short_C` `v03` (`P5:19_skyline_strike`, `P5:01_house_rod`, `P5:07_giant_spark`, `P1:16_question_sky`, `P1:12_steeple_fire`, `P5:18_rod_closeup`, `P5:06_rod_fitting_c1`, `P5:14_safe_towers`) are minted (`J1191` KEEP), hash-verified on both local SSD and NAS (`10_Shorts/J2170/INPUT_INVENTORY.json`), and resolve `SHORTS_PICTURE_PLAN_v02.json`'s label collisions over the `9.0–14.0 s` promoted-long title banner.

---

## 2. Quantitative Proof Why Existing Audio Cannot Clear `<= 2.85 s` (`J1004` + Long Part 05)

### 2.1 Existing `hos_008_short_C_v02.mp3` Opening Sentence (`w[00..12]`, 13 words)

| Word Index | Token | `start_s` | `end_s` | `dur_s` | `gap_after_s` | Cumulative Speech (`1.00x`) | Cumulative Speech (`1.06x`) |
|---|---|---:|---:|---:|---:|---:|---:|
| *(lead-in)* | *(silence)* | `0.000` | `0.080` | `0.000` | `0.080` | `0.000` | `0.000` |
| `w[00]` | `That` | `0.080` | `0.240` | `0.160` | `0.140` | `0.160` | `0.151` |
| `w[01]` | `thin` | `0.380` | `0.660` | `0.280` | `0.100` | `0.440` | `0.415` |
| `w[02]` | `metal` | `0.760` | `1.020` | `0.260` | `0.120` | `0.700` | `0.660` |
| `w[03]` | `rod` | `1.140` | `1.480` | `0.340` | `0.100` | `1.040` | `0.981` |
| `w[04]` | `on` | `1.580` | `1.680` | `0.100` | `0.040` | `1.140` | `1.075` |
| `w[05]` | `top` | `1.720` | `1.880` | `0.160` | `0.040` | `1.300` | `1.226` |
| `w[06]` | `of` | `1.920` | `2.060` | `0.140` | `0.100` | `1.440` | `1.358` |
| `w[07]` | `tall` | `2.160` | `2.400` | `0.240` | `0.100` | `1.680` | `1.585` |
| `w[08]` | `buildings` | `2.500` | `3.060` | `0.560` | `0.100` | `2.240` | `2.113` |
| `w[09]` | `was` | `3.160` | `3.400` | `0.240` | `0.040` | `2.480` | `2.340` |
| `w[10]` | `Benjamin` | `3.440` | `3.840` | `0.400` | `0.080` | `2.880` | `2.717` |
| `w[11]` | `Franklin's` | `3.920` | `4.400` | `0.480` | `0.080` | `3.360` | `3.170` |
| `w[12]` | `idea.` | `4.480` | `4.840` | `0.360` | `0.880` | **`3.720`** | **`3.509`** |

- **Result**: Even with `0.000 s` lead-in, `0.000 s` inter-word gaps, and maximum allowed `atempo = 1.06x`, the 13 words require **`3.509 s > 2.85 s`** (`+0.659 s` over the gate).

### 2.2 Locked Long Part 05 VO (`hos_008_part05_the_rod_on_every_roof_v01b.mp3`) Audit

| Part 05 Word Range | Time (`s`) | Span (`1.00x`) | Pure Speech (`1.06x`) | Spoken Sentence | Why It Cannot Serve as a `£0` Unchanged-Audio Short C Open |
|---|---|---:|---:|---|---|
| `w[0..14]` | `0.100–5.520` | `5.420 s` | `3.736 s` | *"In September seventeen fifty-two, Franklin put an iron rod on top of his own house."* | `3.736 s > 2.85 s`; opens with chronological dateline (`LEARNINGS.md` Rule 2 FAIL). |
| `w[93..104]` | `35.740–39.780` | `4.040 s` | `2.774 s` | *"Lightning is a giant spark hotter than the surface of the sun."* | Omits subject `"lightning rod"` in Sentence 1 (`LEARNINGS.md` Rules 2 & 8 FAIL); `2.774 s` leaves `< 7 ms/gap` to fit `2.85 s`. |
| `w[105..113]` | `40.460–42.880` | `2.420 s` | `1.887 s` | *"It's looking for the easiest path to the ground."* | Starts with anaphoric pronoun `"It's"` (`LEARNINGS.md` Rule 2 FAIL). |
| `w[159..164]` | `60.180–62.440` | `2.260 s` | `1.736 s` | *"Franklin never patented his lightning rod."* | Continuation (`w[165..195]`) is about patents and ships' masts (`P5:13_rods_spread` missing asset), not how a lightning rod works; non-chronological backward splice into `w[93..158]` is unapproved. |

---

## 3. Concise Source-Checked Opening for Normal Script/Facts Lock (Paper Specification)

To preserve the existing locked `49`-word body of `hos_008_short_C_v02.wav` (`w[13..61]`, `5.720–24.400 s`, `sha256: 0a25b6dab1351e70fad717d96e066f0d6c1981bd2d17eba1b65db719acec0aa0`) while satisfying `<= 2.85 s` hook completion, `LEARNINGS.md` Rules 1, 2, 3, 6, 7, 8, and `FACT_NOTES_v01.md`, **only Sentence 1 (`w[00..12]`) requires a 1-sentence script/VO pickup**:

### 3.1 Proposed Sentence 1 Pickup Candidates (for Claude / Chief Script Lock)

| Candidate ID | Proposed Sentence 1 Text | Words | Chars | Syllables | Est. Duration (`speed=1.04`, `1.00x`) | `LEARNINGS.md` Rule 2 & Rule 8 Check |
|---|---|---:|---:|---:|---:|---|
| **`C-Open-1` (Recommended)** | **`That rooftop lightning rod was Franklin's idea.`** | **7** | **47** | **10** | **`~2.35–2.55 s <= 2.85 s`** | Names deictic Frame-0 visual (`"That rooftop lightning rod"`) by `~1.3 s` + surprise attribution (`"was Franklin's idea"`) by `~2.45 s <= 2.85 s`. Matches `SHORTS_SCRIPTS_v02.md` meaning 1:1. |
| **`C-Open-2` (6-Word Alternative)** | **`Benjamin Franklin invented the lightning rod.`** | **6** | **45** | **10** | **`~2.15–2.35 s <= 2.85 s`** | Names `"Benjamin Franklin"` + `"lightning rod"` in `~2.25 s <= 2.85 s` (`0.50–0.70 s` margin below `2.85 s`). |

### 3.2 Fact-Notes & Primary Source Verification (`01_Script/FACT_NOTES_v01.md`)

Every word in `C-Open-1` / `C-Open-2` and the unchanged `49`-word body `w[13..61]` is already sourced and verified in `01_Script/FACT_NOTES_v01.md` (`sha256: bab1bb388caed2c95fbf89fa3b9d3ecec27e95b3c46f82af32395edc0fbbaf0d`):

| Claim in `Short_C` (`v03` Paper Plan) | `FACT_NOTES_v01.md` Row & Primary Citation | Verification Status |
|---|---|---|
| *"That rooftop lightning rod was Franklin's idea."* / *"Benjamin Franklin invented the lightning rod."* | **Rows 25, 38, 39, 41, 42**: Benjamin Franklin, *"Opinions and Conjectures"* (1750), published in *Experiments and Observations on Electricity* (London, 1751); Sept 1752 pointed iron rod on his Market Street house (Franklin to Collinson, Sept 1753, Founders Online); *Poor Richard Improved* (1753, Founders Online). | **PASS** (zero new claims; matches signed-off `SHORTS_SCRIPTS_v02.md` line 67). |
| *"Lightning takes the easiest path to the ground. A wooden roof is a terrible path, so it bursts into flame."* | **Row 41**: *Poor Richard Improved* (1753, Founders Online) & standard NFPA 780 / atmospheric-electricity teaching paraphrase confirmed by Claude (4 Oct 2026, hard check #2). | **PASS** (unchanged `w[13..32]`). |
| *"A metal rod is an easy one. The lightning runs down the rod, round the building, and into the earth."* | **Row 41**: *Poor Richard Improved* (1753, Founders Online): iron rod extending `6–8 ft` above highest part of building, wire down the exterior wall, foot `3–4 ft` in moist earth. | **PASS** (unchanged `w[33..51]`). |
| *"Some towers are struck over twenty times a year."* + `DATA: 20+ STRIKES A YEAR` | **Row 44**: NOAA / National Weather Service, *Lightning Myths and Facts* (Empire State Building struck an average of `23` times per year; Uman `~20–25`/yr; confirmed by Claude hard check #4). | **PASS** (unchanged `w[52..61]`). |

### 3.3 Full Spoken Word Timings & Two Body Layouts Using Unchanged `w[13..61]` (`hos_008_short_C_v02.wav`)

In `10_Shorts/vo_v02/hos_008_short_C_v02.wav` (`sha256: 0a25b6dab1351e70fad717d96e066f0d6c1981bd2d17eba1b65db719acec0aa0`), sentences 2–6 (`w[13..61]`, `49` words) have clean inter-sentence silences (`0.60–0.90 s`), allowing two exact assembly layouts once the 1-sentence pickup (`~2.45 s`) is recorded:

#### Layout `C-v03a` — Original Script Order (`Pickup S1` + Unchanged Contiguous `w[13..61]`)
- **Spoken Script (`56` words with `C-Open-1` / `55` words with `C-Open-2`; `55–65` word lock PASS)**:
  > *"That rooftop lightning rod was Franklin's idea. Lightning takes the easiest path to the ground. A wooden roof is a terrible path, so it bursts into flame. A metal rod is an easy one. The lightning runs down the rod, round the building, and into the earth. Some towers are struck over twenty times a year."*
- **Exact Segment Map (`atempo = 1.00x`, zero internal edits to `w[13..61]`)**:
  1. `0.000–2.450 s`: Pickup Sentence 1 (`C-Open-1`, `~2.450 s <= 2.85 s`).
  2. `2.450–2.670 s`: Seam breath (`0.220 s < 0.25 s`, `LEARNINGS.md` Rule 7 PASS).
  3. `2.670–21.350 s`: Existing `hos_008_short_C_v02.wav` slice `5.720–24.400 s` (`w[13..61]`, `18.680 s` contiguous, unmodified).
  4. `21.350–22.350 s`: Loop tail (`1.000 s <= 1.00 s` HOS lock, returning to Frame-0 `P5:19_skyline_strike`).
- **Metrics**:
  - Hook completion: **`~2.450 s <= 2.85 s`** (`PASS`).
  - VO duration: **`21.350 s`**; Total duration: **`22.350 s`** (`22.00–27.00 s` `PASS`).
  - `9.0–14.0 s` promoted-long title banner: overlays *"A wooden roof is a terrible path, so it bursts into flame. A metal rod..."* (stakes/problem beat; zero early payoff resolution).
  - Final scale payoff (`w[52..61]`, *"Some towers are struck over twenty times a year."*, `DATA: 20+ STRIKES A YEAR`): starts at **`18.390 / 22.350 s = 82.3% >= 70%`** (`PASS`). *(Note: the mechanism sentence `w[40..51]` *"The lightning runs down the rod..."* starts at `13.470 / 22.350 s = 60.3%`; if Chief requires the mechanism sentence itself to start `>= 70%`, use Layout `C-v03b` below.)*

#### Layout `C-v03b` — Strict Rule-6 Mechanism-Payoff Order (`Pickup S1` + Whole-Sentence `w[52..61]` at `S02` + `w[13..51]`)
- **Spoken Script (`56` words, whole-sentence reorder only)**:
  > *"That rooftop lightning rod was Franklin's idea. Some towers are struck over twenty times a year. Lightning takes the easiest path to the ground. A wooden roof is a terrible path, so it bursts into flame. A metal rod is an easy one. The lightning runs down the rod, round the building, and into the earth."*
- **Exact Segment Map (`atempo = 1.00x`, cut only on `0.72–0.90 s` inter-sentence silences)**:
  1. `0.000–2.450 s`: Pickup Sentence 1 (`C-Open-1`, `~2.450 s <= 2.85 s`).
  2. `2.450–2.670 s`: Seam breath (`0.220 s < 0.25 s`).
  3. `2.670–5.630 s`: Existing `hos_008_short_C_v02.wav` slice `21.440–24.400 s` (`w[52..61]`: *"Some towers are struck over twenty times a year."*, `2.960 s`).
  4. `5.630–5.980 s`: Inter-sentence breath (`0.350 s`).
  5. `5.980–20.800 s`: Existing `hos_008_short_C_v02.wav` slice `5.720–20.540 s` (`w[13..51]`, `14.820 s` contiguous: *"Lightning takes the easiest path to the ground... and into the earth."*).
  6. `20.800–22.000 s` (or `21.800 s` with natural breaths): Loop tail (`1.000 s` after `0.200 s` final word decay = **`22.000–22.200 s` total**).
- **Metrics**:
  - Mechanism payoff (`w[40..51]`, *"The lightning runs down the rod, round the building, and into the earth."*) starts at **`16.780 / 22.050 s = 76.1% >= 70%`** (`LEARNINGS.md` Rule 6 strict start-of-answer `PASS`!).

---

## 4. Approved Existing Long Plates Inventory vs `J1881` / `J2163` Six-Note Corrections

### 4.1 Cross-Check Against All Six `J1881` / `J2163` UAT Notes on `master_v03` (`cf1561c2...`)

| Note # | Master Time | `J2163` Frame Envelope | Long Board Row & Clip | Issue in `J1881` / `J2163` | Used in `008 Short_C`? |
|---:|---|---|---|---|---|
| **1** | `00:20` | `427–544` (`17.917–22.833 s`) | `P1:03_table_three` (`03_table_three_t1.mp4`) | Unbacked gold text over sunlit table; needs sequential `<=4`-word house labels. | **NO (Disjoint)** |
| **2** | `0:30` | `744–839` (`31.167–35.167 s`) | `P1:03b_town_safe -> P1:04_storm_mystery` | 4-frame residual flash at pause-trim boundary. | **NO (Disjoint)** |
| **3** | `1:49` | `2506–2665` (`104.667–111.333 s`) | `P2:02_salon_spark` (`02_salon_spark_t1.mp4`) | Hair extruding out of glass tube (`1.5–6.5 s`); missing exact-match asset. | **NO (Disjoint)** |
| **4** | `2:20` | `3260–3343` (`136.125–139.625 s`) | `P2:07_foil_jar` (`07_foil_jar_t1.mp4`) | Silver foil peels/teleports & jar levitates in frames `92–175`. | **NO (Disjoint)** |
| **5** | `3:31` | `4977–5077` (`207.833–212.125 s`) | `P3:04_letter_crosses` (`overlay_04_letter_crosses.mp4`) | Unclear 2-box Atlantic inset & 9-frame splice flash; unsourced `3,600 MILES`. | **NO (Disjoint)** |
| **6** | `7:58` | `11358–11492` (`474.375–480.000 s`) | `P5:13_rods_spread` (`13_rods_spread_t1.mp4`) | Lightning rods kink, detach, and fall across sky after `1.50 s`; no ship mast. | **NO — Explicitly Excluded (`d9fa5f13...` never used)** |

### 4.2 Audit of `SHORTS_PICTURE_PLAN_v02.json` & Clean `v03` Moving-Plate Replacement Table

Auditing `10_Shorts/SHORTS_PICTURE_PLAN_v02.json` against `AGENTS.md` (*Teach on screen* Shorts rules) and `J1260`/`J1263`/`J1267`/`J1273` reveals two defects in the `v02` picture plan that are resolved at `£0` using already-minted (`J1191` KEEP) Part 05 and Part 01 moving Flow plates:
1. **Label Collisions & 1-Overlay Cap Violation in `v02`**: `v02` scheduled four pre-labelled long code graphics (`P5:08_looking_path` `"EASIEST PATH DOWN"`, `P5:09_wood_vs_metal` `"WOOD AND STONE RESIST"`, `P5:10_metal_easy` `"METAL CONDUCTS"`, `P5:11_safe_path` `"SAFE PATH DOWN"`) plus `teach_overlay` (`"20+ STRIKES A YEAR"`). In `v02`, `P5:09` (`7.58–10.18 s`) and `P5:10` (`13.06–15.80 s`) collide directly with the mandatory `9.0–14.0 s` promoted-long title banner (*Why Did Franklin Fly a Kite in a Storm?*) and violate the Shorts **at-most-one-overlay** and **one-label-at-a-time** rules (`AGENTS.md` line 114).
2. **`P5:06_rod_fitting` / `P5:10_metal_easy` Repeat & 42-Frame Limit (`J1267`/`J1273`)**: `v02` used `P5:06_rod_fitting` at `S01` (`0.0–2.4 s`), again as the background of `S06` (`P5:10_metal_easy`), and at `loop_tail`, while `J1273`'s tracked rod composite (`composite_v08.mp4`, `sha256: f8453cc7...`) is only `42` clean frames (`1.750 s`, `frames 109–150`) and remains parked for Chief due to workman hand/bracket occlusion.

#### Clean `Short_C` `v03` Moving-Plate Schedule (`£0`, 100% On Local SSD & NAS, `Layout C-v03a` Timings Shown)

| Row | Window (`s`) | Dur (`s`) | Approved Minted Plate (`FLOW_MINT_LOG_v03.json`) | Verified SHA-256 (`8.0 s` MP4 on SSD & NAS) | Visual Action & Overlay Compliance |
|---|---:|---:|---|---|---|
| **`S01`** | `0.00–2.45` | `2.45` | `P5:19_skyline_strike` (`19_skyline_strike_t1.mp4`, Veo 3.1 Quality) | `06caaeb6b7394ad590547b2f3f09db2dbe3a4a0354977591d36fb72769065026` | Matches `SHORTS_SCRIPTS_v02.md` line 52 Frame 0: modern tower at night already struck on top rod; bolt channels down rod by `1.0 s`. Hook caption: `FRANKLIN'S ROD` (yellow `ROD`). Spoken: *"That rooftop lightning rod was Franklin's idea."* |
| **`S02`** | `2.45–5.33` | `2.88` | `P5:01_house_rod` (`01_house_rod_t1.mp4`, Veo 3.1 Fast) | `3822f6f706eb9263e2ec0fd6f3f8cb4b46bdb848778622505d25af1ad52001a3` | Pointed iron rod rising above Franklin's Philadelphia brick roof under dark storm sky. Spoken: *"Lightning takes the easiest path to the ground."* |
| **`S03`** | `5.33–8.25` | `2.92` | `P5:07_giant_spark` (`07_giant_spark_t1.mp4`, Veo 3.1 Quality) | `8be031a332ec3ef63a3702a29f0df90230d7dec95ea27d0da83e90bd82c3c293` | Giant lightning bolt forks searching downward toward town rooftops (clean moving plate replacing pre-labelled `P5:08`). Spoken: *"A wooden roof is a"* |
| **`S04`** | `8.25–11.15` | `2.90` | `P1:12_steeple_fire` (`12_steeple_fire_t1.mp4`, Veo 3.1 Fast) | `421b96d9b6c6497bbae10abeaca56af50230c11fc2024988906429fbb0c6c453` | Wooden roof / church steeple struck and bursting into flame. **`9.0–14.0 s` promoted long title (`Why Did Franklin Fly a Kite in a Storm?`)** enters cleanly with zero competing label. Spoken: *"terrible path, so it bursts into flame."* |
| **`S05`** | `11.15–13.95` | `2.80` | `P5:18_rod_closeup` (`18_rod_closeup_t1.mp4`, Veo 3.1 Fast) | `9535c72f68606a9de5293739535dd9b826ca624daf73889fa2aba46b5b36ce15` | Sharp pointed iron rod gleaming in storm rain above roof peak (`9.0–14.0 s` promoted long title exits cleanly at `14.0 s`). Spoken: *"A metal rod is an easy one."* |
| **`S06`** | `13.95–16.75` | `2.80` | `P5:06_rod_fitting_c1` (`06_rod_fitting_c1_t1.mp4`, Veo 3.1 Fast) | `de605071ba81008eca11b7e10c17e9fcf88ac303f32d800c8fb745793d4f6908` | Iron conductor rod running down the exterior brick wall toward the ground (clean companion take, avoiding `06_rod_fitting_t1` hand/bracket occlusion). Spoken: *"The lightning runs down the rod, round"* |
| **`S07`** | `16.75–19.45` | `2.70` | `P5:06_rod_fitting` (`06_rod_fitting_t1.mp4`, clean window `4.50–7.20 s`) *or* `P5:11_safe_path` (`4.40–7.00 s` unlabelled tail) | `73c43fc2502c38dbbc8e65691402c6ee84e4937c429647f6270e2cc372fd38ad` / `e19a1164b08a9f62fac99e1bccdd6bb14f3ababbb5ce69a8d0656def42124be9` | Down-conductor path carrying charge harmlessly into the damp earth outside the building. Spoken: *"the building, and into the earth. Some"* |
| **`S08`** | `19.45–21.35` | `1.90` (`2.90` w/ tail) | `P5:14_safe_towers` (`14_safe_towers_t1.mp4`, Veo 3.1 Quality) | `0c7e98c2d89d2e4ef61271af00d71ae77d9e1e55b871b70bdc33ea79e81ffbdd` | Tall towers under lightning strikes staying calm and safe. Single Short teach overlay: **`DATA: 20+ STRIKES A YEAR`** (`18.5–21.2 s`, inside 16:9 centre band, clear of `0–2 s` and `9–14 s`). Spoken: *"towers are struck over twenty times a year."* |
| **`loop_tail`** | `21.35–22.35` | `1.00` | `P5:19_skyline_strike` (`19_skyline_strike_t1.mp4`, Frame-0 match) | `06caaeb6b7394ad590547b2f3f09db2dbe3a4a0354977591d36fb72769065026` | `1.00 s` seamless visual loop back to Frame-0 tower strike (`<= 1.00 s` HOS lock; no end card, no video ID, no spoken/visual CTA). |

---

## 5. Concrete Missing Input & Bounded Next Decision Queued

1. **Exact Missing Inputs Preventing Immediate `£0` Render**:
   - **Input 1 (Script Lock + 1-Sentence VO Pickup Scope)**: Chief/Claude approval of the 1-sentence replacement hook (`C-Open-1`: *"That rooftop lightning rod was Franklin's idea."* [7w, 47c] or `C-Open-2`: *"Benjamin Franklin invented the lightning rod."* [6w, 45c]), selection of `Layout C-v03a` vs `Layout C-v03b`, and credit authorization to record that single sentence (`~45–47` characters against `101,014` available ElevenLabs characters) via `vo_take.py` (`Ben Orbit Narrator`, `eleven_v3`, `speed=1.04`).
   - **Input 2 (`008` Long Public Prerequisite)**: HOS `008` Long (*Why Did Franklin Fly a Kite in a Storm?*) must complete `J1881` / `J2163` six-note corrections, pass Ben's final watch, and be **Public on YouTube** before any `008` Short (`Short_A` via `J0912` or `Short_C`) can air.
2. **Bounded Next Decision Job**:
   - Queued as **`J2175`** (`Chief: HOS 008 Short C 1-sentence hook approval and VO pickup scope for conditional 2 Dec slot`, `ref: J2170`, `film: 008`, `stage: edit`). Until `J2175` approves the 1-sentence pickup and `008` Long is public, `008 Short_C` remains held (`blocked_hook_and_missing_plates`) and the conditional **2 Dec 11:30Z** slot is reported **EMPTY / HELD**.
