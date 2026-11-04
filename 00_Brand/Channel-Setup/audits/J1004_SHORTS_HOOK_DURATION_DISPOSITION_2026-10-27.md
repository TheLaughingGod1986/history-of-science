# J1004 — HOS J0967 Follow-Up: Paper Disposition of Remaining Shorts Hook & Duration Proposals and 008–010 Media Dependency Map

- **Task**: `J1004` (`HOS J0967 follow-up: resolve remaining hook and duration proposals on paper, preserve production holds`)
- **Author / Reviewer**: `gemini` (`gemini-argon`)
- **Date**: `2026-10-27`
- **Linked Films**: `HOS:006`, `HOS:007`, `HOS:008`, `HOS:009`, `HOS:010`
- **Preceding Rulings & Commits Audited**:
  - HOS Desk PR `#180` rulings: [`6425168160`](https://github.com/TheLaughingGod1986/history-of-science/pull/180#issuecomment-6425168160) (`FIX`), [`6426967421`](https://github.com/TheLaughingGod1986/history-of-science/pull/180#issuecomment-6426967421) (`FIX`), [`6428936303`](https://github.com/TheLaughingGod1986/history-of-science/pull/180#issuecomment-6428936303) (`PASS — plans-only scope of J0967`)
  - HOS Commits: `9e23d71a`, `c91a3633`, `3ecc2575`, `e1bbcfb9` (`00_Brand/Channel-Setup/tools/hos_build_rule_v02.py`)
- **Production Hold Guarantee**: This is a **no-spend (`£0`), paper-only disposition review**. No voiceover, plate, render, NAS file, or YouTube state is modified; `J0862`, `J0863`, and all credit/date/Ben holds remain closed; all `BUILD_RULE_v02.json`, `SHORTS_PICTURE_PLAN_v02.json`, and `BUILD_RULE_S5_S8_v02.json` statuses (`blocked_*`, `unbuilt`, `planned`) and retired assemblers remain untouched.

---

## 1. Governing Channel Rules & Scope

1. **Hook Window Lock (`<= 2.85 s`)**: Every HOS Short's opening spoken hook must complete a self-contained claim or question at **`<= 2.85 s`** (`00_Brand/Channel-Setup/tools/hos_build_rule_v02.py` `HOOK_MAX_END_S = 2.85`).
2. **Total Duration Lock (`22.00–27.00 s`)**: Every HOS Short must run **`22.00–27.00 s`** total (`vo_duration_s + 1.00 s` tail hold for seamless loop back to frame 0; `gate_shorts_open.py` and `AGENTS.md`).
3. **Voiceover Integrity & `atempo` Cap (`<= 1.06x`)**:
   - HOS `AGENTS.md` Never list: **"Never change a word of the signed-off script in VO (regenerate the sentence instead); never apply `atempo` above `1.06`."**
   - `J1004` brief: *"`atempo <= 1.06`; no new VO, no approved-wording changes. Proposals in `e1bbcfb9` remain unapproved, including quantitative feasibility claims: calculate from timing data, do not copy their prose as proof. Preserve both `one minute` and `one second` in the Moon comparison. If no lawful edit fits, explicitly recommend retaining the block or retiring that candidate, with reason; do not fabricate a workable cut. Do not approve milkmaid wording or any other scientific claim without the source/claims process."*
4. **Two-Short Selection Lock (`Test B`, `007` Onward)**:
   - Under `SHORTS_LOG.md` (`Test B`, 26 Oct 2026) and `J1004`, each film from `007` onward ships **2 Shorts** (`1` search-titled + `1` curiosity-gap, or `2` search-titled for `007`). Superseded or reserve inventory (`006 s07/s08`, `007 Short_B/Short_C`) must **not** be promoted into extra releases.
   - Standalone `S7` (`s7_priestley_mint`) remains `planned` only; `S5`, `S6`, and `S8` remain `unbuilt`.

---

## 2. Executive Summary & Master Disposition Table

| Candidate | Current v02 Status | Signed-Off Opening Hook (`w[0..k]`) | Existing Audio Hook End (`1.00x` / current) | Pure Speech Sum (`1.00x` -> `1.06x` cap) | Lawful Edit (`0` words changed, `atempo <= 1.06`) Fits `<= 2.85 s` & `22–27 s`? | Audit of `e1bbcfb9` Unapproved Proposal | Disposition Recommendation for Chief |
|---|---|---|---|---|---|---|---|
| **`006 Short_A`** (`t1_willow_air_vo_v02`) | `blocked_duration_under_22s` | *"A tree is built from thin air."* (`w[00..06]`, 7 words) | **`2.160 s <= 2.85 s`** (PASS) | `1.709 s` (`1.00x`) / `1.612 s` (`1.06x`) | **NO** — Hook passes (`2.160 s`), but after trimming forbidden spoken title (`w[53..60]`, `20.180–22.640 s`), VO is `19.920 s` and total with `1.00 s` tail is **`20.920 s` (`< 22.00 s` by `1.080 s`)**. | Correctly identified that `20.920 s < 22.00 s` has no lawful existing-audio fix. | **RETAIN `blocked_duration_under_22s` (or RETIRE `Short_A`)**: `006 Short_B` (`24.20 s`) and `006 Short_C` (`25.16 s`) already pass all paper gates as `006`'s 2 planned Shorts. Only revive `Short_A` if a 1-sentence VO pickup is approved after the 30 Oct ElevenLabs reset. |
| **`006 s04_photosynthesis`** (Part 05 lift) | `blocked_unfinished_hook` | *"A leaf takes in carbon dioxide through tiny pores."* (`w[00..08]`, 9 words) | `3.255 s` (at `1.02x`); `3.320 s` (raw `1.00x`) | `2.777 s` (`1.00x`) / `2.620 s` (`1.06x`) | **MARGINAL / NOT RECOMMENDED** — Even at `1.06x` cap (`2.620 s` speech), fitting `<= 2.850 s` leaves only `0.230 s` across 8 word boundaries (`0.0287 s/gap`), clipping consonant transitions. | `e1bbcfb9` proposed excising `w[06..08]` (*"through tiny pores"*, `1.873–3.255 s`) to end on *"dioxide"* at `1.843 s`. **REJECT**: alters signed-off lifted wording, deletes the stomata mechanism, and ends on non-final mid-sentence prosody. | **RETAIN `blocked_unfinished_hook` & RETIRE `s04_photosynthesis` from active release**: `006` already has 2 clean dedicated Shorts (`Short_B`, `Short_C`). Do not splice mid-sentence VO lifts. |
| **`006 s05_charcoal_gas`** (Part 02 lift) | `blocked_unfinished_hook` | *"Van Helmont also burned sixty-two pounds of charcoal and found just one pound of ash left behind."* (`w[00..16]`, 17 words) | `7.223 s` (at `1.03x`); `7.440 s` (raw `1.00x`) | `6.293 s` (`1.00x`) / `5.937 s` (`1.06x`) | **NO** — Pure speech at `1.06x` is `5.937 s` (`> 2.85 s` by `3.087 s`). Even first clause `w[00..07]` (*"...charcoal"*) is `3.961 s` (`3.509 s` speech) and incomplete. | `e1bbcfb9` proposed excising `w[00..02]` (*"Van Helmont also"*, `0.000–1.698 s`) + gap trim to end on *"charcoal"* at `2.16 s`. **REJECT**: leaves headless fragment *"burned sixty-two pounds of charcoal"* with no subject and no 1-lb-ash payoff. | **RETAIN `blocked_unfinished_hook` & RETIRE `s05_charcoal_gas`**: mid-paragraph long-form narration with anaphoric *"also"* cannot form a `<= 2.85 s` standalone hook without new VO. |
| **`006 s06_ingenhousz_oxygen`** (Part 04 lift) | `blocked_unfinished_hook` | *"Tiny silver bubbles appear on the green leaf and rise to the top."* (`w[00..12]`, 13 words) | `4.594 s` (at `1.05x`); `4.824 s` (raw `1.00x`) | `3.958 s` (`1.00x`) / `3.734 s` (`1.06x`) | **NO** — Full sentence pure speech at `1.06x` is `3.734 s > 2.85 s`. First clause `w[00..07]` (*"...green leaf"*) is `3.070 s` at `1.05x` and drops 5 signed-off words. | `e1bbcfb9` proposed excising `w[08..12]` (*"and rise to the top."*, `3.070–4.594 s`) + `-0.27 s` gap trim to end on *"leaf"* at `2.80 s`. **REJECT**: alters signed-off sentence, leaves mid-sentence cadence on *"leaf"*, and duplicates `006 Short_C`. | **RETAIN `blocked_unfinished_hook` & RETIRE `s06_ingenhousz_oxygen`**: redundant duplicate of `006 Short_C` (*"Leaves only make oxygen in the light."*, `25.16 s`, status `planned`, hook ends at `2.560 s <= 2.85 s`). |
| **`007 Short_B`** (`hos_007_short_B_v02`) | `blocked_unfinished_hook` | *"The first vaccine began with milkmaids, who never caught smallpox."* (`w[00..09]`, 10 words) | `4.600 s` (raw `1.00x`) | `3.480 s` (`1.00x`) / `3.283 s` (`1.06x`) | **NO** — Pure speech of the 10-word sentence at `1.06x` is `3.283 s > 2.85 s` even with zero gaps. | `e1bbcfb9` proposed excising `w[00..04]` (*"The first vaccine began with"*) and `w[06]` (*"who"*) to say *"milkmaids never caught smallpox."* at `1.88 s`. **REJECT**: violates no-wording-change rule, turns a qualified folklore/rumour clause into an unqualified absolute claim without source/claims sign-off, and exceeds `007`'s 2-Short Test B cap. | **RETAIN `blocked_unfinished_hook` & RETIRE/SHELVE `007 Short_B`**: `007` already has its 2 Test B Shorts built, approved, and scheduled on YouTube (`-I_GHK-GcFs` Fri 13 Nov, `4WUs0beKn0A` Tue 17 Nov). Do not promote `Short_B` or `Short_C`. |
| **`008 Short_C`** (`hos_008_short_C_v02`) | `blocked_hook_and_missing_plates` | *"That thin metal rod on top of tall buildings was Benjamin Franklin's idea."* (`w[00..12]`, 13 words) | `4.840 s` (raw `1.00x`) | `3.720 s` (`1.00x`) / `3.509 s` (`1.06x`) | **NO** — Pure speech of all 13 words at `1.06x` is `3.509 s > 2.85 s` even with zero gaps. | `e1bbcfb9` proposed excising `w[04..08]` (*"on top of tall buildings"*, `1.580–3.060 s`) and claimed it ends at `2.84 s` at `1.00x`. **REJECT (math error + wording change)**: removing `1.58–1.60 s` from `4.840 s` actually leaves **`3.240–3.260 s` at `1.00x` (`> 2.85 s`)**, and deleting 5 words violates the signed-off script lock. | **RETAIN `blocked_hook_and_missing_plates`**: `008 Short_C` is already held on missing `008` Flow Veo plates (`J0863` after 12 Nov). Require a 1-sentence script/VO pickup after the 30 Oct ElevenLabs reset so the hook finishes `<= 2.85 s` without splicing words. |
| **`009 Short_B`** (`hos_009_short_B_v02`) | `blocked_hook_and_missing_plates` | *"In one minute, the Moon falls about as far as an apple falls in one second."* (`w[00..15]`, 16 words) | `4.580 s` (raw `1.00x`); `4.270 s` (with `-0.310 s` comma trim) | `3.181 s` (`1.00x`) / `3.001 s` (`1.06x`) | **NO** — Pure speech of the 16 words at `1.06x` with zero gaps is **`3.001 s > 2.85 s`**, and both *"In one minute"* and *"in one second"* must be preserved for Newton's $60^2$ comparison. | `e1bbcfb9` correctly marked `009 Short_B` unresolvable via existing audio after ruling `6426967421` barred dropping *"In one minute"*. | **RETAIN `blocked_hook_and_missing_plates`**: cannot be solved on existing audio (`hos_009_short_B_v02`). Address via `J0862` (`009 + 010` Shorts VO after 30 Oct reset) if Chief & Claude shorten the sentence on paper, while `009` plates remain gated on `J0863` + tranche 2. |
| **`010 Short_A`** (`hos_010_short_A_v02`) | `blocked_hook_and_missing_plates` | *"This thin line of clay marks the end of the dinosaurs."* (`w[00..10]`, 11 words) | `3.280 s` (raw `1.00x`) | `2.620 s` (`1.00x`) / `2.472 s` (`1.06x`) | **YES (via pause trim + `1.06x` on S1, `0` words changed)** — Trimming `-0.080 s` lead-in (`0.000–0.080 s`) and `-0.180 s` across the 6 gaps `>= 0.060 s` (leaving `>= 0.040 s` at every word boundary) + `atempo = 1.06x` on S1 finishes *"dinosaurs."* at **`2.849 s <= 2.85 s`**, with `vo_duration_s = 22.289 s` and `total_duration_s = 23.289 s` (`22–27 s` PASS). | `e1bbcfb9` claimed `-0.48 s` gap trim at `1.00x` (`2.80 s`) or excising *"of clay"* (`w[03..04]`). **REJECT `e1bbcfb9` variants**: `-0.48 s` at `1.00x` strips `73%` of all `0.660 s` onset/inter-word gaps (`~0.016 s/gap`), and dropping *"of clay"* violates the signed-off script lock and breaks the promoted long title callback. | **RETAIN `blocked_hook_and_missing_plates` now (due to unminted `010` Flow plates); APPROVE Option A1 (`0` words changed: `-0.260 s` onset/pause trim + `1.06x` on S1 -> `2.849 s` hook end, `23.289 s` total) OR re-record in `J0862`** when `010` plates are ready. |

### Non-Conflict / Superseded / Standalone Inventory Status Confirmation

| Item | Current v02 Status | Hook End & Total Duration | J1004 Disposition |
|---|---|---|---|
| **`006 Short_B`** (`t2_two_ounces_vo_v03b`) | `planned` | Hook `w[00..07]` *"Two hundred pounds of soil lost two ounces."* ends at **`2.490 s <= 2.85 s`**; VO `23.20 s`, total **`24.20 s`** | Keep `planned` (1 of 2 active `006` Shorts; all 8 NAS plates verified). |
| **`006 Short_C`** (`t3_bubbles_sunlight_vo_v01`) | `planned` | Hook `w[00..06]` *"Leaves only make oxygen in the light."* ends at **`2.560 s <= 2.85 s`**; VO `24.16 s`, total **`25.16 s`** | Keep `planned` (2 of 2 active `006` Shorts; all 8 NAS plates verified). |
| **`006 s07_priestley_mint` & `s08_willow_pot`** | `superseded_inventory` | Superseded by standalone `S7` (`s7_priestley_mint`) and `006 Short_A/B/C` | **Do not revive** (`J1004` lock). |
| **`007 s04_smallpox_test` (`-I_GHK-GcFs`) & `s05_vacca_jesty` (`4WUs0beKn0A`)** | Scheduled on YouTube (Private `publishAt` 13 Nov & 17 Nov 2026) | `24.48 s` and `25.12 s` (`gate_shorts_open.py` PASS) | **Active 2-Short selection for `007`** (`SHORTS_RELEASE.json`). Preserve; do not add extra `007` releases. |
| **`007 Short_C`** (`hos_007_short_C_v02`) | `planned` (in `BUILD_RULE_v02.json`, shelved in `SHORTS_LOG.md`) | Hook `w[00..05]` *"Every vaccine is named after cows."* ends at **`2.220 s <= 2.85 s`**; VO `22.88 s`, total **`23.88 s`** | **Keep shelved in reserve** (`SHORTS_LOG.md` line 55): `007` already has its 2 scheduled Test B Shorts (`-I_GHK-GcFs`, `4WUs0beKn0A`), and `s05_vacca_jesty` already covers the *vacca* / Jesty story. |
| **`008 Short_A`** (`hos_008_short_A_v02`) | `blocked_missing_plates` | Hook `w[00..06]` *"Franklin's kite was never hit by lightning."* ends at **`2.480 s <= 2.85 s`**; VO `22.24 s`, total **`23.24 s`** | Hook & duration **PASS** on paper; keep `blocked_missing_plates` until `008` Flow plates mint (`J0863`). |
| **`009 Short_A`** (`hos_009_short_A_v02`) | `blocked_missing_plates` | Hook `w[00..06]` *"The Moon is falling towards the Earth."* ends at **`2.020 s <= 2.85 s`**; VO `22.34 s`, total **`23.34 s`** | Hook & duration **PASS** on paper; keep `blocked_missing_plates` until `009` Flow plates mint (`J0863` + tranche 2). |
| **`010 Short_C`** (`hos_010_short_C_v02`) | `blocked_missing_plates` | Hook `w[00..06]` *"Every bird is a living dinosaur."* ends at **`2.560 s <= 2.85 s`**; VO `22.40 s`, total **`23.40 s`** | Hook & duration **PASS** on paper; keep `blocked_missing_plates` until `010` Flow plates mint. |
| **Standalone `S7`** (`s7_priestley_mint`) | `planned` | Hook `w[00..09]` *"A candle in a closed jar goes out in seconds."* ends at **`2.800 s <= 2.85 s`**; VO `22.22 s`, total **`23.22 s`** | Keep `planned` only (`BUILD_RULE_S5_S8_v02.json`); do not render without Chief build instruction. |
| **Standalone `S5`, `S6`, `S8`** | `unbuilt` | Missing subject plates in `001..006` (`S6`, `S8`) and hook `2.960 s > 2.85 s` (`S5`) | Keep `unbuilt` (`BUILD_RULE_S5_S8_v02.json`). |

---

## 3. Candidate-by-Candidate Timing & Rule Disposition

### 3.1 `006 Short_A` (`t1_willow_air_vo_v02` — *"Where Do Trees Come From?"*)

- **Locked Script & Source Reference**:
  - Script: `02_Video-Projects/006_Trees-Are-Made-Of-Air/10_Shorts/SHORTS_SCRIPTS_v01.md` (lines 20–36, `Short A — The five-year pot (T1)`).
  - Fact Notes: `02_Video-Projects/006_Trees-Are-Made-Of-Air/01_Script/FACT_NOTES_v01.md` (lines 7, 11–18: Jan Baptist van Helmont, *Ortus Medicinae*, 1648, p. 109: 200 lb dried soil, 5 lb willow -> 169 lb 3 oz, soil lost 2 oz).
  - Audio & Alignment: `/Volumes/data/mac-mini-archive/hos-worktrees/2026-10-22/hos-006-trees/02_Video-Projects/006_Trees-Are-Made-Of-Air/10_Shorts/vo_test/t1_willow_air_vo_v02.mp3` (`t1_willow_air_vo_v02_align.json`).
- **Complete Signed-Off Spoken Text (53 words, `w[00..52]`, `0.000–19.920 s`)**:
  > *"A tree is built from thin air. One man spent five years proving the soil wasn't feeding it. He planted a willow in two hundred pounds of dried soil and gave it only water. Five years later the tree weighed a hundred and sixty-nine pounds, and the soil had lost just two ounces."*
- **Existing-Audio Word Ranges for Opening Hook (`w[00..06]`, 7 words)**:

| Word Index | Spoken Word | `start_s` | `end_s` | `dur_s` | `gap_after_s` |
|---|---|---:|---:|---:|---:|
| `w[00]` | `A` | `0.000` | `0.080` | `0.080` | `0.112` |
| `w[01]` | `tree` | `0.192` | `0.640` | `0.448` | `0.107` |
| `w[02]` | `is` | `0.747` | `0.960` | `0.213` | `0.040` |
| `w[03]` | `built` | `1.000` | `1.200` | `0.200` | `0.032` |
| `w[04]` | `from` | `1.232` | `1.360` | `0.128` | `0.080` |
| `w[05]` | `thin` | `1.440` | `1.760` | `0.320` | `0.080` |
| `w[06]` | `air.` | `1.840` | `2.160` | `0.320` | `0.200` |

- **Timing & Duration Calculation**:
  - **Computed Hook End**: `w[06] "air."` finishes at **`2.160 s <= 2.85 s`** (`1.709 s` pure speech + `0.451 s` inter-word gaps). **PASS**.
  - **Full Duration Conflict**: The raw test recording (`22.640 s`) includes a spoken end-card title at `w[53..60]` (`20.180–22.640 s`: *"The Willow Tree That Was Made of Air."*). Under `SHORTS_SCRIPTS_v01.md` line 5 (*"The long's title is on screen only, never spoken: trim any spoken title from a take before the edit"*), trimming `20.180–22.640 s` leaves `w[00..52]` ending at `"ounces."` (`19.920 s`).
  - With the mandatory `1.000 s` loop tail hold (`loop_tail`), `total_duration_s = 19.920 + 1.000 = 20.920 s`, which is **`1.080 s` below the `22.00 s` HOS Shorts minimum** (`SHORT_MIN_TOTAL_S = 22.00`).
  - Stretching `19.920 s` VO to `21.000 s` would require `atempo = 19.920 / 21.000 = 0.9486x` (artificial slowdown) or `2.080 s` of dead tail silence, both of which violate HOS audio/pacing gates (`vo_check.py` / `gate_shorts_open.py`).
- **Disposition Recommendation**:
  - **Retain `blocked_duration_under_22s` (or retire `006 Short_A`)**. `006` already has two complete, compliant Shorts in `planned` state — **`006 Short_B` (`24.20 s`)** and **`006 Short_C` (`25.16 s`)** — which fulfill a 2-Short release without `Short_A`. If Chief ever wishes to ship `Short_A` as a 3rd `006` Short, it requires a 1-sentence script/VO pickup after the 30 Oct ElevenLabs credit reset (just as `006 Short_B` received in `v03b`).

---

### 3.2 `006 s04_photosynthesis` (Lifted from `02_Voiceover/part05_carbon_from_the_sky_v01_raw.mp3`)

- **Locked Script & Source Reference**:
  - Long Script Master: `02_Video-Projects/006_Trees-Are-Made-Of-Air/01_Script/trees_script_master_v02.md` (Part 05: *Carbon from the Sky*, lines 167–175).
  - Fact Notes: `02_Video-Projects/006_Trees-Are-Made-Of-Air/01_Script/FACT_NOTES_v01.md` (lines 46–48: de Saussure, *Recherches chimiques sur la végétation*, 1804; Taiz & Zeiger, *Plant Physiology*; USDA *Wood Handbook*: ~50% of dry wood is carbon).
  - Lift Spec: `02_Video-Projects/006_Trees-Are-Made-Of-Air/10_Shorts/SHORT_s04_photosynthesis_v01.json` (`vo_take_indices: [70..113, 125..142]`, 62 words, `atempo = 1.02`, `max_pause_s = 0.45`).
- **Complete Spoken Text in Lift (62 words)**:
  > *"A leaf takes in carbon dioxide through tiny pores. It draws up water through its roots. Then, with the energy of sunlight, it joins them together into sugar, and lets the spare oxygen go. That sugar becomes everything else: leaves, roots, bark and wood. About half of dry wood is carbon, and every bit of that carbon came out of the air."*
- **Existing-Audio Word Ranges for Opening Sentence (`w[00..08]`, 9 words, shown at `1.02x` lift timeline and `1.00x` raw duration)**:

| Word Index | Spoken Word | `start_s` (`1.02x`) | `end_s` (`1.02x`) | `dur_s` (`1.02x`) | `dur_s` (`1.00x` raw) | `gap_after_s` (`1.02x`) |
|---|---|---:|---:|---:|---:|---:|
| `w[00]` | `A` | `0.000` | `0.039` | `0.039` | `0.040` | `0.063` |
| `w[01]` | `leaf` | `0.102` | `0.353` | `0.251` | `0.256` | `0.066` |
| `w[02]` | `takes` | `0.419` | `0.745` | `0.326` | `0.333` | `0.052` |
| `w[03]` | `in` | `0.797` | `0.902` | `0.105` | `0.107` | `0.056` |
| `w[04]` | `carbon` | `0.958` | `1.294` | `0.336` | `0.343` | `0.069` |
| `w[05]` | `dioxide` | `1.363` | `1.843` | `0.480` | `0.490` | `0.030` |
| `w[06]` | `through` | `1.873` | `2.078` | `0.205` | `0.209` | `0.079` |
| `w[07]` | `tiny` | `2.157` | `2.471` | `0.314` | `0.320` | `0.117` |
| `w[08]` | `pores.` | `2.588` | `3.255` | `0.667` | `0.680` | `0.157` |

- **Timing & Feasibility Audit**:
  1. **Current (`1.02x`)**: `w[08] "pores."` ends at **`3.255 s > 2.85 s`** (`0.405 s` over gate); `vo_duration_s = 24.977 s`, `total_duration_s = 25.977 s`.
  2. **Audit of `e1bbcfb9` Unapproved Proposal**: `e1bbcfb9` proposed excising `w[06..08]` (*"through tiny pores"*, `1.873–3.255 s`) at `1.02x` so *"A leaf takes in carbon dioxide."* ends at `1.843 s <= 2.85 s` (`vo_duration_s = 23.595 s`, `total = 24.595 s`).
     - **Why this violates channel rules**: (a) It deletes 3 signed-off words from the locked sentence in VO (`AGENTS.md` Never list); (b) it deletes the anatomical mechanism (*"through tiny pores"* / stomata) that connects to the visual plate (`20_leaf_breathing_t1.mp4`); and (c) in the recording, `w[05] "dioxide"` (`1.363–1.843 s`, `gap_after = 0.030 s`) has non-final, mid-phrase intonation running directly into *"through"*.
  3. **Word-Preserving (`0` words changed) Calculation at `atempo <= 1.06`**:
     - Raw (`1.00x`) pure speech across `w[00..08]` is **`2.777 s`**. At the studio cap `atempo = 1.06x`, pure speech is `2.777 / 1.06 = 2.620 s`.
     - To finish `w[08] "pores."` at `<= 2.850 s`, total inter-word gaps across all 8 word transitions must be compressed from `0.543 s` (raw) to **`<= 0.230 s`** (`<= 0.0287 s` average per transition). Splicing 8 consecutive word transitions down to `~28 ms` clips stop/fricative onsets (`leaf->takes`, `carbon->dioxide`, `tiny->pores`).
- **Disposition Recommendation**:
  - **Retain `blocked_unfinished_hook` and retire `006 s04_photosynthesis` from active release**. `006` already has two clean, purpose-recorded Shorts (`006 Short_B` `24.20 s` and `006 Short_C` `25.16 s`) that pass every gate without word deletion or sub-30ms micro-gap surgery.

---

### 3.3 `006 s05_charcoal_gas` (Lifted from `02_Voiceover/part02_five_years_and_two_ounces_v01_raw.mp3`)

- **Locked Script & Source Reference**:
  - Long Script Master: `02_Video-Projects/006_Trees-Are-Made-Of-Air/01_Script/trees_script_master_v02.md` (Part 02: *Five Years and Two Ounces*, lines 79–85).
  - Fact Notes: `02_Video-Projects/006_Trees-Are-Made-Of-Air/01_Script/FACT_NOTES_v01.md` (lines 22–25: van Helmont, *Ortus Medicinae*, 1648, Complexionum atque mistionum elementalium figmentum §14, p. 106: 62 lb oak charcoal -> 1 lb ash, 61 lb *spiritus sylvester* / *gas*).
  - Lift Spec: `02_Video-Projects/006_Trees-Are-Made-Of-Air/10_Shorts/SHORT_s05_charcoal_gas_v01.json` (`vo_take_indices: [243..304]`, 62 words, `atempo = 1.03`, `max_pause_s = 0.45`).
- **Complete Spoken Text in Lift (62 words)**:
  > *"Van Helmont also burned sixty-two pounds of charcoal and found just one pound of ash left behind. The rest had vanished into the air, as a wild, invisible spirit. He gave it a new name: gas. We now know that gas was mostly carbon dioxide. He had discovered the very thing his tree was made of. He never put the two together."*
- **Existing-Audio Word Ranges for Opening Sentence (`w[00..16]`, 17 words, at `1.03x` lift timeline)**:

| Word Index | Spoken Word | `start_s` (`1.03x`) | `end_s` (`1.03x`) | `dur_s` (`1.03x`) | `gap_after_s` (`1.03x`) |
|---|---|---:|---:|---:|---:|
| `w[00]` | `Van` | `0.000` | `0.699` | `0.699` | `0.058` |
| `w[01]` | `Helmont` | `0.757` | `1.165` | `0.408` | `0.093` |
| `w[02]` | `also` | `1.258` | `1.631` | `0.373` | `0.067` |
| `w[03]` | `burned` | `1.698` | `2.097` | `0.399` | `0.065` |
| `w[04]` | `sixty-two` | `2.162` | `2.718` | `0.556` | `0.056` |
| `w[05]` | `pounds` | `2.774` | `3.107` | `0.333` | `0.026` |
| `w[06]` | `of` | `3.133` | `3.184` | `0.051` | `0.087` |
| `w[07]` | `charcoal` | `3.271` | `3.961` | `0.690` | `0.136` |
| `w[08]` | `and` | `4.097` | `4.505` | `0.408` | `0.039` |
| `w[09]` | `found` | `4.544` | `4.738` | `0.194` | `0.046` |
| `w[10]` | `just` | `4.784` | `4.971` | `0.187` | `0.078` |
| `w[11]` | `one` | `5.049` | `5.282` | `0.233` | `0.065` |
| `w[12]` | `pound` | `5.347` | `5.670` | `0.323` | `0.026` |
| `w[13]` | `of` | `5.696` | `5.748` | `0.052` | `0.135` |
| `w[14]` | `ash` | `5.883` | `6.291` | `0.408` | `0.047` |
| `w[15]` | `left` | `6.338` | `6.524` | `0.186` | `0.089` |
| `w[16]` | `behind.` | `6.613` | `7.223` | `0.610` | `0.175` |

- **Timing & Feasibility Audit**:
  1. **Current (`1.03x`)**: The 17-word opening sentence ends at **`7.223 s`** (`6.110 s` pure speech + `1.113 s` inter-word gaps); `vo_duration_s = 25.558 s`, `total_duration_s = 26.558 s`.
  2. **Word-Preserving (`0` words changed) Calculation at `atempo = 1.06x`**:
     - Raw (`1.00x`) pure speech across `w[00..16]` is **`6.293 s`**. At `1.06x`, pure speech alone is **`5.937 s > 2.85 s`**. Even the first half of the compound predicate (`w[00..07]`, *"Van Helmont also burned sixty-two pounds of charcoal"*) has `3.509 s` of pure speech at `1.03x` (`3.410 s` at `1.06x` > `2.85 s`) and omits the payoff (*"and found just one pound of ash left behind"*).
  3. **Audit of `e1bbcfb9` Unapproved Proposal**: `e1bbcfb9` proposed excising `w[00..02]` (*"Van Helmont also"*, `0.000–1.698 s`) and trimming `0.10 s` of gaps so `w[03..07]` (*"burned sixty-two pounds of charcoal"*) ends at `2.16 s <= 2.85 s`.
     - **Why this violates channel rules**: Deleting *"Van Helmont also"* produces a grammatically headless verb phrase (*"Burned sixty-two pounds of charcoal and found just one pound of ash left behind."*) with no grammatical subject, alters signed-off words in VO, and still fails to complete a claim by `2.85 s` because *"burned sixty-two pounds of charcoal"* without a subject or outcome is not a complete clause.
- **Disposition Recommendation**:
  - **No lawful edit fits. Retain `blocked_unfinished_hook` and retire `006 s05_charcoal_gas`**. This passage was written as mid-scene long-form narration (*"Van Helmont also..."*) and cannot function as a standalone Short open without a purpose-written script and VO take.

---

### 3.4 `006 s06_ingenhousz_oxygen` (Lifted from `02_Voiceover/part04_bubbles_in_the_sunlight_v01_raw.mp3`)

- **Locked Script & Source Reference**:
  - Long Script Master: `02_Video-Projects/006_Trees-Are-Made-Of-Air/01_Script/trees_script_master_v02.md` (Part 04: *Bubbles in the Sunlight*, lines 134–144).
  - Fact Notes: `02_Video-Projects/006_Trees-Are-Made-Of-Air/01_Script/FACT_NOTES_v01.md` (lines 35–42: Jan Ingenhousz, *Experiments upon Vegetables*, London, 1779).
  - Lift Spec: `02_Video-Projects/006_Trees-Are-Made-Of-Air/10_Shorts/SHORT_s06_ingenhousz_oxygen_v01.json` (`vo_take_indices: [50..81, 105..134]`, 62 words, `atempo = 1.05`, `max_pause_s = 0.45`).
- **Complete Spoken Text in Lift (62 words)**:
  > *"Tiny silver bubbles appear on the green leaf and rise to the top. He collected the bubbles and tested the gas. A candle flame burned brighter in it than in ordinary air. Move the jar into the shade, and the bubbles stop. Move it back into the sun, and they start again. Only the green parts made bubbles. Roots and flowers didn't."*
- **Existing-Audio Word Ranges for Opening Sentence (`w[00..12]`, 13 words, at `1.05x` lift timeline)**:

| Word Index | Spoken Word | `start_s` (`1.05x`) | `end_s` (`1.05x`) | `dur_s` (`1.05x`) | `gap_after_s` (`1.05x`) |
|---|---|---:|---:|---:|---:|
| `w[00]` | `Tiny` | `0.038` | `0.404` | `0.366` | `0.066` |
| `w[01]` | `silver` | `0.470` | `0.861` | `0.391` | `0.067` |
| `w[02]` | `bubbles` | `0.928` | `1.394` | `0.466` | `0.098` |
| `w[03]` | `appear` | `1.492` | `2.080` | `0.588` | `0.026` |
| `w[04]` | `on` | `2.106` | `2.156` | `0.050` | `0.019` |
| `w[05]` | `the` | `2.175` | `2.232` | `0.057` | `0.051` |
| `w[06]` | `green` | `2.283` | `2.537` | `0.254` | `0.107` |
| `w[07]` | `leaf` | `2.644` | `3.070` | `0.426` | `0.096` |
| `w[08]` | `and` | `3.166` | `3.451` | `0.285` | `0.092` |
| `w[09]` | `rise` | `3.543` | `3.909` | `0.366` | `0.050` |
| `w[10]` | `to` | `3.959` | `4.061` | `0.102` | `0.019` |
| `w[11]` | `the` | `4.080` | `4.137` | `0.057` | `0.095` |
| `w[12]` | `top.` | `4.232` | `4.594` | `0.362` | `0.299` |

- **Timing & Feasibility Audit**:
  1. **Current (`1.05x`)**: The 13-word opening sentence ends at **`4.594 s > 2.85 s`** (`3.770 s` pure speech + `0.786 s` inter-word gaps + `0.038 s` onset); `vo_duration_s = 24.756 s`, `total_duration_s = 25.756 s`.
  2. **Word-Preserving (`0` words changed) Calculation at `atempo = 1.06x`**:
     - Raw (`1.00x`) pure speech across `w[00..12]` is **`3.958 s`**. At `1.06x`, pure speech alone is **`3.734 s > 2.85 s`**. Thus the full sentence cannot fit `<= 2.85 s` without deleting words.
  3. **Audit of `e1bbcfb9` Unapproved Proposal**: `e1bbcfb9` proposed excising `w[08..12]` (*"and rise to the top."*, `3.070–4.594 s`) and trimming `0.270 s` of onset/inter-word gaps so `w[00..07]` (*"Tiny silver bubbles appear on the green leaf."*) ends at `2.800 s <= 2.85 s` (`vo_duration_s = 22.962 s`, `total = 23.962 s`).
     - **Why this violates channel rules**: (a) It deletes 5 signed-off words from the locked sentence in VO; (b) `w[07] "leaf"` has non-final prosody leading into *"and rise"*; (c) the second sentence immediately says *"He collected the bubbles"* with no antecedent for *"He"* (Jan Ingenhousz is never named in the 62-word lift!); and (d) **`006 Short_C` (`t3_bubbles_sunlight_vo_v01.mp3`, `25.16 s`, status `planned`, hook *"Leaves only make oxygen in the light."* ending at `2.560 s <= 2.85 s`) already covers this exact Ingenhousz underwater-leaf bubble experiment** with a dedicated, compliant recording that names Jan Ingenhousz.
- **Disposition Recommendation**:
  - **No lawful edit fits. Retain `blocked_unfinished_hook` and retire `006 s06_ingenhousz_oxygen` as redundant with `006 Short_C`**.

---

### 3.5 `007 Short_B` (`hos_007_short_B_v02` — *"How Were Vaccines Discovered?"*)

- **Locked Script & Source Reference**:
  - Shorts Script: `02_Video-Projects/007_The-First-Vaccine/10_Shorts/SHORTS_SCRIPTS_v02.md` (lines 21–43, `Short B — The milkmaid clue`).
  - Fact Notes: `02_Video-Projects/007_The-First-Vaccine/01_Script/FACT_NOTES_v01.md` (lines 21–22: Edward Jenner, *An Inquiry into the Causes and Effects of the Variolae Vaccinae*, 1798; Country folk belief in Gloucestershire).
  - Audio & Alignment: `02_Video-Projects/007_The-First-Vaccine/10_Shorts/vo_v02/hos_007_short_B_v02.mp3` (`hos_007_short_B_v02_stt.json`).
- **Complete Signed-Off Spoken Text (59 words, `w[00..58]`, `0.100–25.520 s`)**:
  > *"The first vaccine began with milkmaids, who never caught smallpox. They caught cowpox from the cows instead — a few sore spots and nothing more. And farmers swore that anyone who'd had it was safe from smallpox for life. One country doctor, Edward Jenner, took the rumour seriously and tested it. He was right — and it became the first vaccine."*
- **Existing-Audio Word Ranges for Opening Sentence (`w[00..09]`, 10 words, `1.00x`)**:

| Word Index | Spoken Word | `start_s` | `end_s` | `dur_s` | `gap_after_s` |
|---|---|---:|---:|---:|---:|
| `w[00]` | `The` | `0.100` | `0.240` | `0.140` | `0.080` |
| `w[01]` | `first` | `0.320` | `0.600` | `0.280` | `0.100` |
| `w[02]` | `vaccine` | `0.700` | `1.200` | `0.500` | `0.100` |
| `w[03]` | `began` | `1.300` | `1.560` | `0.260` | `0.040` |
| `w[04]` | `with` | `1.600` | `1.740` | `0.140` | `0.140` |
| `w[05]` | `milkmaids` | `1.880` | `2.720` | `0.840` | `0.360` |
| `w[06]` | `who` | `3.080` | `3.220` | `0.140` | `0.060` |
| `w[07]` | `never` | `3.280` | `3.520` | `0.240` | `0.060` |
| `w[08]` | `caught` | `3.580` | `3.780` | `0.200` | `0.080` |
| `w[09]` | `smallpox.` | `3.860` | `4.600` | `0.740` | `0.880` |

- **Timing & Feasibility Audit**:
  1. **Current (`1.00x`)**: The 10-word opening sentence spans `0.100–4.600 s` (**`4.600 s > 2.85 s`**); `vo_duration_s = 25.520 s`, `total_duration_s = 26.520 s`.
  2. **Word-Preserving (`0` words changed) Calculation at `atempo = 1.06x`**:
     - Pure speech across `w[00..09]` is **`3.480 s`** at `1.00x`. Even at `1.06x` with **zero** onset and **zero** inter-word gaps, pure speech is **`3.480 / 1.06 = 3.283 s > 2.85 s`**. And stopping at `w[05] "milkmaids"` (`2.720 s`) leaves *"The first vaccine began with milkmaids"* without the reason why milkmaids mattered (*"who never caught smallpox"*).
  3. **Audit of `e1bbcfb9` Unapproved Proposal**: `e1bbcfb9` proposed excising `w[00..04]` (*"The first vaccine began with"*, `0.100–1.740 s`) and `w[06]` (*"who"*, `3.080–3.220 s`) plus `-0.300 s` of comma pause so `w[05] + w[07..09]` (*"Milkmaids never caught smallpox."*) finishes at `1.880 s <= 2.85 s` (`vo_duration_s = 22.800 s`, `total = 23.800 s`).
     - **Why this violates channel rules**:
       - (a) **Wording & Scientific Claims Lock**: Deleting 6 of the 10 words in sentence 1 violates the no-approved-wording-change lock and converts a contextualized historical introduction (*"The first vaccine began with milkmaids, who never caught smallpox ... And farmers swore that anyone who'd had it was safe ... One country doctor, Edward Jenner, took the rumour seriously"*) into an unqualified standalone biological claim (*"Milkmaids never caught smallpox."*) at `0.00 s`. `SHORTS_SCRIPTS_v02.md` line 43 and `J1004` explicitly bar approving milkmaid wording or any new scientific claim phrasing without the full source/claims process.
       - (b) **Two-Short Selection Lock (`Test B`)**: Under `02_Video-Projects/007_The-First-Vaccine/10_Shorts/SHORTS_RELEASE.json` and `SHORTS_LOG.md` (lines 48–56), **`007` ALREADY has its 2 Test B Shorts built, approved, uploaded Private, and scheduled on YouTube**:
         1. `-I_GHK-GcFs` (`s04_smallpox_test` — *What Was the Edward Jenner Experiment?*, `24.48 s`, scheduled `2026-11-13T11:30:00Z`)
         2. `4WUs0beKn0A` (`s05_vacca_jesty` — *Why Is It Called a Vaccine?*, `25.12 s`, scheduled `2026-11-17T11:30:00Z`)
- **Disposition Recommendation**:
  - **Do not approve the `"Milkmaids never caught smallpox"` splice. Retain `blocked_unfinished_hook` and retire/shelve `007 Short_B` (alongside reserve `007 Short_C`)** so `007`'s locked 2-Short release (`-I_GHK-GcFs` and `4WUs0beKn0A`) is preserved without promoting extra inventory.

---

### 3.6 `008 Short_C` (`hos_008_short_C_v02` — *"How Does a Lightning Rod Work?"*)

- **Locked Script & Source Reference**:
  - Shorts Script: `02_Video-Projects/008_Lightning-Franklin/10_Shorts/SHORTS_SCRIPTS_v02.md` (lines 47–69, `Short C — How the pointed rod saves the building`).
  - Fact Notes: `02_Video-Projects/008_Lightning-Franklin/01_Script/FACT_NOTES_v01.md` (lines 25, 38–44: Benjamin Franklin, *Poor Richard's Almanack* 1753; National Weather Service *Lightning Myths*: lightning rods provide a low-resistance path to ground; tall towers struck `>20` times/year).
  - Audio & Alignment: `02_Video-Projects/008_Lightning-Franklin/10_Shorts/vo_v02/hos_008_short_C_v02.mp3` (`hos_008_short_C_v02_stt.json`).
- **Complete Signed-Off Spoken Text (62 words, `w[00..61]`, `0.080–24.480 s`)**:
  > *"That thin metal rod on top of tall buildings was Benjamin Franklin's idea. Lightning takes the easiest path to the ground. A wooden roof is a terrible path, so it bursts into flame. A metal rod is an easy one: the lightning runs down the rod, round the building and into the earth. Some towers are struck over twenty times a year."*
- **Existing-Audio Word Ranges for Opening Sentence (`w[00..12]`, 13 words, `1.00x`)**:

| Word Index | Spoken Word | `start_s` | `end_s` | `dur_s` | `gap_after_s` |
|---|---|---:|---:|---:|---:|
| `w[00]` | `That` | `0.080` | `0.240` | `0.160` | `0.140` |
| `w[01]` | `thin` | `0.380` | `0.660` | `0.280` | `0.100` |
| `w[02]` | `metal` | `0.760` | `1.020` | `0.260` | `0.120` |
| `w[03]` | `rod` | `1.140` | `1.480` | `0.340` | `0.100` |
| `w[04]` | `on` | `1.580` | `1.680` | `0.100` | `0.040` |
| `w[05]` | `top` | `1.720` | `1.880` | `0.160` | `0.040` |
| `w[06]` | `of` | `1.920` | `2.060` | `0.140` | `0.100` |
| `w[07]` | `tall` | `2.160` | `2.400` | `0.240` | `0.100` |
| `w[08]` | `buildings` | `2.500` | `3.060` | `0.560` | `0.100` |
| `w[09]` | `was` | `3.160` | `3.400` | `0.240` | `0.040` |
| `w[10]` | `Benjamin` | `3.440` | `3.840` | `0.400` | `0.080` |
| `w[11]` | `Franklin's` | `3.920` | `4.400` | `0.480` | `0.080` |
| `w[12]` | `idea.` | `4.480` | `4.840` | `0.360` | `0.880` |

- **Timing & Feasibility Audit**:
  1. **Current (`1.00x`)**: The 13-word opening sentence spans `0.080–4.840 s` (**`4.840 s > 2.85 s`**); `vo_duration_s = 24.480 s`, `total_duration_s = 25.480 s`.
  2. **Word-Preserving (`0` words changed) Calculation at `atempo = 1.06x`**:
     - Pure speech across all 13 words is **`3.720 s`** at `1.00x`. Even at `1.06x` with **zero** onset and **zero** inter-word gaps, pure speech is **`3.720 / 1.06 = 3.509 s > 2.85 s`**. No word-preserving edit on the existing recording can fit `<= 2.85 s`.
  3. **Audit of `e1bbcfb9` Unapproved Proposal (Exposing Arithmetic Error + Rule Conflict)**:
     - `e1bbcfb9` claimed: *"excise the prepositional modifier `on top of tall buildings` (`1.58–3.06 s`, removing `1.58 s` including adjacent pause) at `1.00x` so the opening sentence becomes `'That thin metal rod was Benjamin Franklin's idea.'` and completes at `2.84 s <= 2.85 s` (`vo_duration_s = 22.90 s`, `total_duration_s = 23.90 s`)."*
     - **Quantitative Proof of Error**:
       - `w[00..03]` (*"That thin metal rod"*) spans `0.080–1.480 s` (`1.400 s` span: `1.040 s` speech + `0.360 s` gaps).
       - `w[09..12]` (*"was Benjamin Franklin's idea."*) spans `3.160–4.840 s` (`1.680 s` span: `1.480 s` speech + `0.200 s` gaps).
       - Even if you remove the entire `1.600 s` window from `1.520 s` to `3.120 s` (leaving an `0.080 s` bridge between `"rod"` and `"was"`), at `1.00x` `"idea."` finishes at **`4.840 - 1.600 = 3.240 s > 2.85 s`** (or `4.840 - 1.580 = 3.260 s`), **NOT `2.84 s`**! Even if you zeroed out the `0.080 s` lead-in and every single inter-word gap in `w[00..03]` and `w[09..12]`, pure speech + `0.560 s` natural gaps is `3.080 s > 2.85 s` at `1.00x`. Reaching `<= 2.85 s` would require deleting those 5 signed-off words **plus** trimming `-0.240 s` of onset/inter-word gaps **plus** applying `atempo = 1.06x` (`(3.240 - 0.240) / 1.06 = 2.830 s`).
       - Furthermore, deleting 5 words (*"on top of tall buildings"*) from the signed-off script in VO violates the `AGENTS.md` Never list.
- **Disposition Recommendation**:
  - **Reject the `e1bbcfb9` splice (`3.240 s` at `1.00x`, unlawful 5-word deletion) and retain `blocked_hook_and_missing_plates`**. Because `008 Short_C` is already held on unminted `008` Flow Veo plates (`J0863`, after the 12 Nov Flow renewal), no emergency audio surgery is needed: after the 30 Oct ElevenLabs credit reset, Chief & Claude can either approve a 1-sentence script/VO pickup for `008 Short_C` (e.g., *"Benjamin Franklin invented the lightning rod."*, ~6 words / `~2.1 s`, followed by *"That thin metal rod on top of tall buildings gives lightning the easiest path to the ground..."*) or keep `008 Short_C` blocked until re-recorded.

---

### 3.7 `009 Short_B` (`hos_009_short_B_v02` — *"How Did Newton Prove Gravity?"*)

- **Locked Script & Source Reference**:
  - Shorts Script: `02_Video-Projects/009_The-Falling-Moon-Gravity/10_Shorts/SHORTS_SCRIPTS_v02.md` (lines 47–70, `Short B — The one-minute Moon test (inverse-square proof)`).
  - Fact Notes: `02_Video-Projects/009_The-Falling-Moon-Gravity/01_Script/FACT_NOTES_v01.md` (line 30: Isaac Newton, *Principia* Book III Proposition IV, 1687: Moon at 60 Earth radii falls $15\frac{1}{12}$ Paris feet in 1 minute, matching a body at Earth's surface falling $15\frac{1}{12}$ Paris feet in 1 second under $1/60^2 = 1/3600$).
  - Audio & Alignment: `02_Video-Projects/009_The-Falling-Moon-Gravity/10_Shorts/vo_v02/hos_009_short_B_v02.mp3` (`hos_009_short_B_v02_stt.json`).
- **Complete Signed-Off Spoken Text (59 words, `w[00..58]`, raw `0.080–23.440 s`, `23.130 s` after `-0.310 s` comma trim)**:
  > *"In one minute, the Moon falls about as far as an apple falls in one second. Isaac Newton worked out why. The Moon is sixty times further from the Earth's centre than we are — so the pull on it is sixty times sixty weaker. Three thousand six hundred times. And the numbers matched. One pull for apples and moons."*
- **Existing-Audio Word Ranges for Opening Sentence (`w[00..15]`, 16 words, raw `1.00x`)**:

| Word Index | Spoken Word | `start_s` (raw) | `end_s` (raw) | `dur_s` | `gap_after_s` (raw) |
|---|---|---:|---:|---:|---:|
| `w[00]` | `In` | `0.080` | `0.180` | `0.100` | `0.060` |
| `w[01]` | `one` | `0.240` | `0.380` | `0.140` | `0.060` |
| `w[02]` | `minute,` | `0.440` | `0.740` | `0.300` | `0.320` (`0.010` after `-0.310 s` trim) |
| `w[03]` | `the` | `1.060` | `1.160` | `0.100` | `0.060` |
| `w[04]` | `moon` | `1.220` | `1.440` | `0.220` | `0.100` |
| `w[05]` | `falls` | `1.540` | `1.760` | `0.220` | `0.060` |
| `w[06]` | `about` | `1.820` | `2.040` | `0.220` | `0.040` |
| `w[07]` | `as` | `2.080` | `2.200` | `0.120` | `0.040` |
| `w[08]` | `far` | `2.240` | `2.420` | `0.180` | `0.060` |
| `w[09]` | `as` | `2.480` | `2.560` | `0.080` | `0.040` |
| `w[10]` | `an` | `2.600` | `2.700` | `0.100` | `0.080` |
| `w[11]` | `apple` | `2.780` | `3.060` | `0.280` | `0.100` |
| `w[12]` | `falls` | `3.160` | `3.440` | `0.280` | `0.040` |
| `w[13]` | `in` | `3.480` | `3.620` | `0.140` | `0.060` |
| `w[14]` | `one` | `3.680` | `3.860` | `0.180` | `0.199` |
| `w[15]` | `second.` | `4.059` | `4.580` | `0.521` | `0.980` |

- **Timing & Feasibility Audit**:
  1. **Current (`1.00x`)**: Raw opening sentence ends at `4.580 s`; after the `-0.310 s` comma-pause trim (`0.740–1.060 s`), it ends at **`4.270 s > 2.85 s`** (`vo_duration_s = 23.130 s`, `total_duration_s = 24.130 s`).
  2. **Scientific & Meaning Lock (`6426967421` & `J1004`)**: Both time intervals — **`"In one minute"`** (for the Moon at $60 R_\oplus$, where $d \propto g t^2$ with $g_{\text{Moon}} = g_0 / 60^2$ and $t = 60\text{ s}$ yields the same fall distance as $g_0$ in $t = 1\text{ s}$) and **`"in one second"`** (for the apple) — are mathematically indispensable. Dropping either time interval makes the physical statement false (`6426967421`).
  3. **Word-Preserving (`0` words changed) Calculation at `atempo = 1.06x`**:
     - Pure speech across `w[00..15]` is **`3.181 s`** at `1.00x`. Even at the `1.06x` studio `atempo` cap with **zero** onset and **zero** inter-word gaps, pure speech alone is **`3.181 / 1.06 = 3.001 s > 2.85 s`** (and with minimal `0.040 s` natural word transitions across 15 gaps = `0.600 s`, it is `3.567 s > 2.85 s`).
- **Disposition Recommendation**:
  - **No lawful edit on the existing recording (`hos_009_short_B_v02`) can fit `<= 2.85 s` while preserving both `"one minute"` and `"one second"`. Retain `blocked_hook_and_missing_plates`**.
  - Note for Chief when `J0862` (`HOS 009 + 010: Shorts voiceover`, held on 30 Oct ElevenLabs credit reset) opens: if Chief & Claude wish `009 Short_B` to clear `<= 2.85 s` while preserving both intervals, the opening sentence must be tightened on paper before VO regeneration (e.g., *"The Moon falls in one minute what an apple falls in one second."* — 13 words instead of 16, or opening on the 7-word title question *"How did Newton test gravity on the Moon?"* followed immediately by *"In one minute, the Moon falls about as far as an apple falls in one second."*).

---

### 3.8 `010 Short_A` (`hos_010_short_A_v02` — *"What Killed the Dinosaurs?"*)

- **Locked Script & Source Reference**:
  - Shorts Script: `02_Video-Projects/010_Alvarez-Clay-Line-Dinosaurs/10_Shorts/SHORTS_SCRIPTS_v02.md` (lines 27–50, `Short A — The thin line of clay in Gubbio`).
  - Fact Notes: `02_Video-Projects/010_Alvarez-Clay-Line-Dinosaurs/01_Script/FACT_NOTES_v01.md` (lines 18, 22, 29: Alvarez, Alvarez, Asaro & Michel, *Science* 208, 1980, p. 1095–1108: ~1 cm Gubbio boundary clay layer, foraminifera turnover, iridium anomaly).
  - Audio & Alignment: `02_Video-Projects/010_Alvarez-Clay-Line-Dinosaurs/10_Shorts/vo_v02/hos_010_short_A_v02.mp3` (`hos_010_short_A_v02_stt.json`).
- **Complete Signed-Off Spoken Text (60 script words / 59 STT tokens, `w[00..58]`, `0.120–22.720 s`)**:
  > *"This thin line of clay marks the end of the dinosaurs. It's in a cliff in Italy, about a centimetre thick. Below it, the rock is full of tiny fossil shells. Above it, almost all of them are gone. In nineteen eighty, scientists found the clay was packed with a rare metal from space. Something huge had hit the Earth."*
- **Existing-Audio Word Ranges for Opening Sentence (`w[00..10]`, 11 words, `1.00x`)**:

| Word Index | Spoken Word | `start_s` | `end_s` | `dur_s` | `gap_after_s` (raw) | Lawful Trim on Gap (`Option A1`) | Kept Gap (`Option A1`, `1.00x`) |
|---|---|---:|---:|---:|---:|---:|---:|
| *(lead-in)* | *(silence before `This`)* | `0.000` | `0.120` | `0.000` | `0.120` | `-0.080 s` (`0.000–0.080`) | `0.040` |
| `w[00]` | `This` | `0.120` | `0.380` | `0.260` | `0.020` | `0.000 s` | `0.020` |
| `w[01]` | `thin` | `0.400` | `0.620` | `0.220` | `0.080` | `-0.040 s` (`0.640–0.680`) | `0.040` |
| `w[02]` | `line` | `0.700` | `0.920` | `0.220` | `0.040` | `0.000 s` | `0.040` |
| `w[03]` | `of` | `0.960` | `1.060` | `0.100` | `0.060` | `-0.020 s` (`1.080–1.100`) | `0.040` |
| `w[04]` | `clay` | `1.120` | `1.420` | `0.300` | `0.100` | `-0.060 s` (`1.440–1.500`) | `0.040` |
| `w[05]` | `marks` | `1.520` | `1.780` | `0.260` | `0.040` | `0.000 s` | `0.040` |
| `w[06]` | `the` | `1.820` | `1.960` | `0.140` | `0.060` | `-0.020 s` (`1.980–2.000`) | `0.040` |
| `w[07]` | `end` | `2.020` | `2.220` | `0.200` | `0.040` | `0.000 s` | `0.040` |
| `w[08]` | `of` | `2.260` | `2.340` | `0.080` | `0.020` | `0.000 s` | `0.020` |
| `w[09]` | `the` | `2.360` | `2.400` | `0.040` | `0.080` | `-0.040 s` (`2.420–2.460`) | `0.040` |
| `w[10]` | `dinosaurs.` | `2.480` | `3.280` | `0.800` | `0.520` | `0.000 s` | `0.520` |

- **Timing & Feasibility Audit**:
  1. **Current (`1.00x`)**: `w[10] "dinosaurs."` finishes at **`3.280 s > 2.85 s`** (`2.620 s` pure speech + `0.120 s` onset + `0.540 s` inter-word gaps); `vo_duration_s = 22.720 s`, `total_duration_s = 23.720 s`.
  2. **Audit of `e1bbcfb9` Unapproved Proposals**:
     - `e1bbcfb9` Variant 1 proposed trimming `-0.480 s` of onset and inter-word gaps at `1.00x` (`3.280 - 0.480 = 2.800 s`). **Why Variant 1 is defective**: total onset + inter-word gaps across `0.000–3.280 s` is only `0.120 + 0.540 = 0.660 s`. Removing `0.480 s` at `1.00x` strips `72.7%` of all word boundaries (`0.180 s` left across 11 transitions = `0.016 s` average gap), clipping consonant releases (`thin->line`, `clay->marks`, `end->of`).
     - `e1bbcfb9` Variant 2 proposed excising `w[03..04]` (*"of clay"*, `0.960–1.420 s`) so sentence 1 becomes *"This thin line marks the end of the dinosaurs."* **Why Variant 2 violates channel rules**: it deletes 2 signed-off words from the locked script in VO (`AGENTS.md` Never list) and removes the noun *"clay"* that sentence 5 (*"scientists found the clay was packed..."*) and the promoted long title (*"What Killed the Dinosaurs Was Hidden in a Line of Clay"*) depend on.
  3. **Lawful Word-Preserving Calculation (`Option A1` — `0` words changed, `atempo <= 1.06`)**:
     - **Proposed Spoken Opening (complete, verbatim signed-off sentence 1, `w[00..10]`)**:
       > *"This thin line of clay marks the end of the dinosaurs."*
     - **Exact Existing-Audio Pause Removals (`-0.260 s` total across 6 silence windows, keeping `>= 0.040 s` on every trimmed boundary)**:
       1. Lead-in silence: trim `0.000–0.080 s` (`-0.080 s`; `"This"` starts at `0.040 s`).
       2. Gap `w[01]->w[02]` (`thin -> line`, `0.620–0.700 s`): trim `0.640–0.680 s` (`-0.040 s`; `0.040 s` kept).
       3. Gap `w[03]->w[04]` (`of -> clay`, `1.060–1.120 s`): trim `1.080–1.100 s` (`-0.020 s`; `0.040 s` kept).
       4. Gap `w[04]->w[05]` (`clay -> marks`, `1.420–1.520 s`): trim `1.440–1.500 s` (`-0.060 s`; `0.040 s` kept).
       5. Gap `w[06]->w[07]` (`the -> end`, `1.960–2.020 s`): trim `1.980–2.000 s` (`-0.020 s`; `0.040 s` kept).
       6. Gap `w[09]->w[10]` (`the -> dinosaurs.`, `2.400–2.480 s`): trim `2.420–2.460 s` (`-0.040 s`; `0.040 s` kept).
     - After `-0.260 s` of pure pause/onset removal, the `1.00x` span of `0.000–3.280 s` is `3.020 s` (`2.620 s` speech + `0.040 s` onset + `0.360 s` natural inter-word gaps).
     - Applying **`atempo = 1.06x`** (`<= 1.06x` studio cap) to Sentence 1 (`0.000–3.280 s` raw):
       $$\text{Hook end} = \frac{3.020\text{ s}}{1.06} = \mathbf{2.849\text{ s} \le 2.850\text{ s}}\text{ (PASS)}$$
     - **Full Duration Check**:
       - Sentence 1 compresses by `3.280 - 2.849 = 0.431 s`.
       - Keeping `w[11..58]` (`3.280–22.720 s` raw, `19.440 s`) at `1.00x`:
         - `vo_duration_s = 22.720 - 0.431 = 22.289 s`
         - `total_duration_s` (with `1.000 s` loop tail) = **`23.289 s`** (well inside the **`22.00–27.00 s`** band; payoff *"Scientists found the clay was packed with a rare metal from space. Something huge had hit the Earth."* runs `14.57–22.29 s`, completely clear of the `9.0–14.0 s` promoted long title banner).
       - *(Even if `atempo = 1.053x` with `-0.280 s` pause trim were applied uniformly across the entire take, `vo_duration_s = (22.720 - 0.280) / 1.053 = 21.311 s` and `total_duration_s = 22.311 s >= 22.00 s`; applying `1.06x` to Sentence 1 only preserves `23.289 s` total duration and `1.00x` body cadence.)*
     - **Retained Meaning**: 100% of signed-off words (`w[00..58]`) are spoken in full with zero word deletions or rewrites.
- **Disposition Recommendation**:
  - **Keep `010 Short_A` in `blocked_hook_and_missing_plates` now** (as `010` Flow plates are unminted and all production states stay held).
  - **For Chief's decision**: Either **(Option A1)** approve the word-preserving `-0.260 s` onset/pause trim + `1.06x` sentence-1 edit (`2.849 s <= 2.85 s`, `23.289 s` total, `0` words changed) for assembly once `010` plates exist, **or (Option A2)** re-record `010 Short_A` Sentence 1 at a slightly brisker natural pace when `J0862` (`HOS 009 + 010: Shorts voiceover`) runs after the 30 Oct ElevenLabs reset.

---

## 4. Missing `008–010` Media Dependency & Producer Map

Across `008`, `009`, and `010`, `SHORTS_PICTURE_PLAN_v02.json` defines **6 Shorts (`54` rows total, including `6` `loop_tail` rows)**. All 54 rows currently show `plate_on_disk: false` in `SHORTS_PICTURE_PLAN_v02.json`. Auditing the actual disk files and queue jobs reveals two distinct categories:

1. **`12` of the `54` rows (`12` unique plates) are `£0` `code_graphic` plates that ALREADY EXIST on disk** in `02_Video-Projects/<Episode>/07_Edit-Project/code_graphics_v01/*.mp4` (produced by completed jobs `J0329`, `J0342`, `J0348`, and `J0383`), but `resolve_plate_path()` in `00_Brand/Channel-Setup/tools/hos_build_rule_v02.py` currently only searches `04_Generated-Clips/part0{N}/raw/v01/` and `07_Edit-Project/stills/`, not `07_Edit-Project/code_graphics_v01/`.
2. **`42` of the `54` rows (`32` unique plates) are unminted `flow_veo` plates** (`11` unique in `008`, `9` unique in `009`, `12` unique in `010`) that depend on downstream long-film Flow Veo plate minting (`0` extra Shorts credits, because all Shorts reuse long-film plates).

### 4.1 Film `008_Lightning-Franklin` (`Short_A` & `Short_C`)

- **Long Board Input Spec**: `02_Video-Projects/008_Lightning-Franklin/07_Edit-Project/PICTURE_PLAN_v03.json` (`parts/part-01..05_plates_v03.json`, `J0240` PASS; `5,605` Flow credits expected across Parts 01–05).
- **Row-by-Row Media & Producer Table**:

| Short | Row(s) | `source_long_plate` | Plate Type / Route | On Disk Now? | Exact Producing Job / Input | Concrete Planning Gap |
|---|---|---|---|---|---|---|
| `Short_A` | `S01`, `loop_tail` | `P1:01_kite_open` | `flow_veo` (Part 01) | **No** | Price pass: **`J0863`** (`blocked` on Flow credit renewal `2026-11-12T00:05:00Z`) | **Gap 1**: `J0863` is only the Chief price-pass review; no downstream `--kind video` Flow mint job for `008` Parts 01–05 or `008` Shorts assembly job is queued yet. |
| `Short_A` | `S02` | `P3:19_kite_climb` | `flow_veo` (Part 03) | **No** | Price pass: **`J0863`** (`check_at: 2026-11-12`) | Same as Gap 1 (needs `008` Flow mint execution job after `J0863`). |
| `Short_A` | `S03` | `P3:13_key_ribbon` | `flow_veo` (Part 03) | **No** | Price pass: **`J0863`** (`check_at: 2026-11-12`) | Same as Gap 1. |
| `Short_A` | `S04` | `P3:25_fibres_rise` | `flow_veo` (Part 03) | **No** | Price pass: **`J0863`** (`check_at: 2026-11-12`) | Same as Gap 1. |
| `Short_A` | `S05` | `P4:02_knuckle_spark` | `flow_veo` (Part 04) | **No** | Price pass: **`J0863`** (`check_at: 2026-11-12`) | Same as Gap 1. |
| `Short_A` | `S06` | `P4:08_teach_charge` | `code_graphic` (Part 04) | **YES** (`07_Edit-Project/code_graphics_v01/code_graphic_008_p4_08_teach_charge.mp4`) | Produced by **`J0329`** (`done`; awaiting Chief visual sign-off in `PIPELINE.json`) | **Tooling gap**: `hos_build_rule_v02.py` `resolve_plate_path()` does not check `07_Edit-Project/code_graphics_v01/`. |
| `Short_A` | `S07` | `P4:10_richmann_rod` | `flow_veo` (Part 04) | **No** | Price pass: **`J0863`** (`check_at: 2026-11-12`) | Same as Gap 1. |
| `Short_C` | `S01`, `loop_tail` | `P5:06_rod_fitting` | `flow_veo` (Part 05) | **No** | Price pass: **`J0863`** (`check_at: 2026-11-12`) | Same as Gap 1. |
| `Short_C` | `S02` | `P5:01_house_rod` | `flow_veo` (Part 05) | **No** | Price pass: **`J0863`** (`check_at: 2026-11-12`) | Same as Gap 1. |
| `Short_C` | `S03` | `P5:08_looking_path` | `code_graphic` (Part 05) | **YES** (`code_graphic_008_p5_08_looking_path.mp4`) | Produced by **`J0329`** (`done`) | Tooling gap in `resolve_plate_path()`. |
| `Short_C` | `S04` | `P5:09_wood_vs_metal` | `code_graphic` (Part 05) | **YES** (`code_graphic_008_p5_09_wood_vs_metal.mp4`) | Produced by **`J0329`** (`done`) | Tooling gap in `resolve_plate_path()`. |
| `Short_C` | `S05` | `P1:12_steeple_fire` | `flow_veo` (Part 01) | **No** | Price pass: **`J0863`** (`check_at: 2026-11-12`) | Same as Gap 1. |
| `Short_C` | `S06` | `P5:10_metal_easy` | `code_graphic` (Part 05) | **YES** (`code_graphic_008_p5_10_metal_easy.mp4`) | Produced by **`J0329`** (`done`) | Tooling gap in `resolve_plate_path()`. |
| `Short_C` | `S07` | `P5:11_safe_path` | `code_graphic` (Part 05) | **YES** (`code_graphic_008_p5_11_safe_path.mp4`) | Produced by **`J0329`** (`done`) | Tooling gap in `resolve_plate_path()`. |
| `Short_C` | `S08` | `P5:14_safe_towers` | `flow_veo` (Part 05) | **No** | Price pass: **`J0863`** (`check_at: 2026-11-12`) | Same as Gap 1. |
| `Short_C` | `S09` | `P5:19_skyline_strike` | `flow_veo` (Part 05) | **No** | Price pass: **`J0863`** (`check_at: 2026-11-12`) | Same as Gap 1. |

---

### 4.2 Film `009_The-Falling-Moon-Gravity` (`Short_A` & `Short_B`)

- **Long Board Input Spec**: `02_Video-Projects/009_The-Falling-Moon-Gravity/07_Edit-Project/PICTURE_PLAN_v05.json` (`PICTURE_PLAN_v04.json` in `PIPELINE.json`: `12,534` Flow credits expected across 5 parts, split into **Tranche 1 = `7,354` credits** after `~12 Nov 2026` renewal and **Tranche 2 = `5,180` credits** after `~12 Dec 2026` renewal).
- **Shorts Price Review Input**: `02_Video-Projects/009_The-Falling-Moon-Gravity/10_Shorts/SHORTS_PRICE_REVIEW_v01.md` (`J0385` / `J0365` PASS: `0` extra Shorts credits).
- **Voiceover Hold Note**: Queue job **`J0862`** (`HOS 009 + 010: Shorts voiceover (2 Shorts each) from the v02 Shorts scripts, vo_check, park for Chief`) is currently `blocked` on ElevenLabs credit reset (`2026-10-30T12:00:00Z`), even though `v02` takes from `J0159` already exist in `10_Shorts/vo_v02/`.
- **Row-by-Row Media & Producer Table**:

| Short | Row(s) | `source_long_plate` | Plate Type / Route | On Disk Now? | Exact Producing Job / Input | Concrete Planning Gap |
|---|---|---|---|---|---|---|
| `Short_A` | `S01`, `loop_tail` | `P1:01_moon_falling` | `flow_veo` (Part 01, Tranche 1) | **No** | Price pass: **`J0863`** (`blocked` until `2026-11-12T00:05:00Z`) | **Gap 2a**: No downstream `--kind video` Flow mint job is queued behind `J0863` for `009` Tranche 1 (Parts 01–03). |
| `Short_A` | `S02` | `P3:08_km_a_second` | `code_graphic` (Part 03) | **YES** (`07_Edit-Project/code_graphics_v01/code_graphic_009_p3_08_km_a_second.mp4`) | Produced by **`J0342` / `J0383`** (`done`) | Tooling gap in `resolve_plate_path()`. |
| `Short_A` | `S03` | `P3:07_ball_to_moon` | `flow_veo` (Part 03, Tranche 1) | **No** | Price pass: **`J0863`** (`check_at: 2026-11-12`) | Same as Gap 2a. |
| `Short_A` | `S04` | `P3:05_shot_orbit` | `flow_veo` (Part 03, Tranche 1) | **No** | Price pass: **`J0863`** (`check_at: 2026-11-12`) | Same as Gap 2a. |
| `Short_A` | `S05` | `P2:07_orchard_bench` | `flow_veo` (Part 02, Tranche 1) | **No** | Price pass: **`J0863`** (`check_at: 2026-11-12`) | Same as Gap 2a. |
| `Short_A` | `S06` | `P2:08_the_apple` | `flow_veo` (Part 02, Tranche 1) | **No** | Price pass: **`J0863`** (`check_at: 2026-11-12`) | Same as Gap 2a. |
| `Short_A` | `S07` | `P3:06_orbit_teach` | `code_graphic` (Part 03) | **YES** (`code_graphic_009_p3_06_orbit_teach.mp4`) | Produced by **`J0342` / `J0383`** (`done`) | Tooling gap in `resolve_plate_path()`. |
| `Short_A` | `S08` | `P5:09_orchard_dusk` | `flow_veo` (Part 05, **Tranche 2**) | **No** | Input spec: `PICTURE_PLAN_v05.json` Part 05 (`Tranche 2`, `5,180` credits) | **Gap 2b**: `J0863` covers only `009` Tranche 1 (`7,354` credits). **No queue job exists at all** for `009` Tranche 2 price pass or Flow mint (`~12 Dec 2026` renewal), which is required for `P5:09_orchard_dusk` in `Short_A`! |
| `Short_B` | `S01`, `loop_tail` | `P4:05_minute_second` | `flow_veo` (Part 04, **Tranche 2**) | **No** | Input spec: `PICTURE_PLAN_v05.json` Part 04 (`Tranche 2`) | Same as Gap 2b (no `009` Tranche 2 price-pass or mint job queued). |
| `Short_B` | `S02` | `P1:02_apple_and_moon` | `flow_veo` (Part 01, Tranche 1) | **No** | Price pass: **`J0863`** (`check_at: 2026-11-12`) | Same as Gap 2a. |
| `Short_B` | `S03`, `S07` | `P4:06_pretty_nearly` | `flow_veo` (Part 04, **Tranche 2**) | **No** | Input spec: `PICTURE_PLAN_v05.json` Part 04 (`Tranche 2`) | Same as Gap 2b. |
| `Short_B` | `S04` | `P4:03_sixty_earths` | `code_graphic` (Part 04) | **YES** (`code_graphic_009_p4_03_sixty_earths.mp4`) | Produced by **`J0342` / `J0383`** (`done`) | Tooling gap in `resolve_plate_path()`. |
| `Short_B` | `S05` | `P4:01_weaker_far` | `code_graphic` (Part 04) | **YES** (`code_graphic_009_p4_01_weaker_far.mp4`) | Produced by **`J0342` / `J0383`** (`done`) | Tooling gap in `resolve_plate_path()`. |
| `Short_B` | `S06` | `P4:04_dots_square` | `code_graphic` (Part 04) | **YES** (`code_graphic_009_p4_04_dots_square.mp4`) | Produced by **`J0342` / `J0383`** (`done`) | Tooling gap in `resolve_plate_path()`. |
| `Short_B` | `S08` | `P5:01_one_law` | `flow_veo` (Part 05, **Tranche 2**) | **No** | Input spec: `PICTURE_PLAN_v05.json` Part 05 (`Tranche 2`) | Same as Gap 2b. |

---

### 4.3 Film `010_Alvarez-Clay-Line-Dinosaurs` (`Short_A` & `Short_C`)

- **Long Board Input Spec**: `02_Video-Projects/010_Alvarez-Clay-Line-Dinosaurs/07_Edit-Project/PICTURE_PLAN_v03.json` (`J0334` + `J0348` PASS; `10,190` Flow credits expected across Parts 01–05).
- **Shorts Price Review Input**: `02_Video-Projects/010_Alvarez-Clay-Line-Dinosaurs/10_Shorts/SHORTS_PRICE_REVIEW_v01.md` (`J0386` / `J0365` PASS: `0` extra Shorts credits).
- **Row-by-Row Media & Producer Table**:

| Short | Row(s) | `source_long_plate` | Plate Type / Route | On Disk Now? | Exact Producing Job / Input | Concrete Planning Gap |
|---|---|---|---|---|---|---|
| `Short_A` | `S01`, `loop_tail` | `P1:01_clay_line` | `flow_veo` (Part 01) | **No** | Input spec: `010/07_Edit-Project/PICTURE_PLAN_v03.json` (`10,190` Flow credits) | **Gap 3**: Unlike `008` and `009` (which have `J0863`), **`010` has NO open or blocked queue job at all** for its Flow picture price pass, Flow Veo plate minting, or `010` Shorts assembly. |
| `Short_A` | `S02` | `P2:01_walter_hammer` | `flow_veo` (Part 02) | **No** | Input spec: `PICTURE_PLAN_v03.json` Part 02 | Same as Gap 3 (no `010` Flow price-pass or mint job in `jobs.json`). |
| `Short_A` | `S03` | `P1:08_hand_on_rock` | `flow_veo` (Part 01) | **No** | Input spec: `PICTURE_PLAN_v03.json` Part 01 | Same as Gap 3. |
| `Short_A` | `S04` | `P2:03_tiny_shells` | `flow_veo` (Part 02) | **No** | Input spec: `PICTURE_PLAN_v03.json` Part 02 | Same as Gap 3. |
| `Short_A` | `S05` | `P2:05_almost_none` | `flow_veo` (Part 02) | **No** | Input spec: `PICTURE_PLAN_v03.json` Part 02 | Same as Gap 3. |
| `Short_A` | `S06` | `P3:08_asaro_michel` | `flow_veo` (Part 03) | **No** | Input spec: `PICTURE_PLAN_v03.json` Part 03 | Same as Gap 3. |
| `Short_A` | `S07` | `P4:01_iridium_spike` | `code_graphic` (Part 04) | **YES** (`07_Edit-Project/code_graphics_v01/code_graphic_010_p4_01_iridium_spike.mp4`) | Produced by **`J0348` / `J0383`** (`done`) | Tooling gap in `resolve_plate_path()`. |
| `Short_A` | `S08` | `P4:06_dust_veil` | `flow_veo` (Part 04) | **No** | Input spec: `PICTURE_PLAN_v03.json` Part 04 | Same as Gap 3. |
| `Short_C` | `S01`, `S05`, `loop_tail` | `P5:09_robin` | `flow_veo` (Part 05) | **No** | Input spec: `PICTURE_PLAN_v03.json` Part 05 | Same as Gap 3. |
| `Short_C` | `S02` | `P4:06_dust_veil` | `flow_veo` (Part 04) | **No** | Input spec: `PICTURE_PLAN_v03.json` Part 04 | Same as Gap 3. |
| `Short_C` | `S03` | `P5:11_why_survive` | `code_graphic` (Part 05) | **YES** (`code_graphic_010_p5_11_why_survive.mp4`) | Produced by **`J0348` / `J0383`** (`done`) | Tooling gap in `resolve_plate_path()`. |
| `Short_C` | `S04` | `P5:08_all_at_once` | `flow_veo` (Part 05) | **No** | Input spec: `PICTURE_PLAN_v03.json` Part 05 | Same as Gap 3. |
| `Short_C` | `S06` | `P5:13_window_song` | `flow_veo` (Part 05) | **No** | Input spec: `PICTURE_PLAN_v03.json` Part 05 | Same as Gap 3. |
| `Short_C` | `S07` | `P5:10_explorer_robin` | `flow_veo` (Part 05) | **No** | Input spec: `PICTURE_PLAN_v03.json` Part 05 | Same as Gap 3. |
| `Short_C` | `S08` | `P5:12_clay_callback` | `flow_veo` (Part 05) | **No** | Input spec: `PICTURE_PLAN_v03.json` Part 05 | Same as Gap 3. |

---

## 5. Summary of Decisions Prepared for Elected Chief

1. **Retire / Keep Shelved (Do Not Revive or Splice)**:
   - `006 s04_photosynthesis`, `006 s05_charcoal_gas`, `006 s06_ingenhousz_oxygen` (and already-superseded `s07_priestley_mint`, `s08_willow_pot`): long-VO lifts whose opening sentences cannot clear `<= 2.85 s` without deleting signed-off words or clipping word transitions (`<29 ms`), and which are unnecessary because `006 Short_B` (`24.20 s`) and `006 Short_C` (`25.16 s`) already pass all paper gates as `006`'s 2 active Shorts.
   - `007 Short_B` (and reserve `007 Short_C`): `007` already has its 2 Test B Shorts built, approved, and scheduled on YouTube (`-I_GHK-GcFs` and `4WUs0beKn0A`); reject the `e1bbcfb9` `"milkmaids never caught smallpox"` word-deletion splice.
2. **Retain Explicit Holds (`blocked_*`) Pending Post-Reset VO Pickup & Long-Plate Minting**:
   - `006 Short_A` (`blocked_duration_under_22s`, `20.92 s`): keep blocked unless Chief orders a 1-sentence VO pickup after the 30 Oct ElevenLabs reset.
   - `008 Short_C` (`blocked_hook_and_missing_plates`): reject `e1bbcfb9`'s miscalculated `2.84 s` splice (actual `3.240 s` at `1.00x` + 5-word deletion); keep blocked alongside `008` plates (`J0863`) until a 1-sentence opening pickup is recorded after 30 Oct.
   - `009 Short_B` (`blocked_hook_and_missing_plates`): pure speech of the 16-word Moon/apple sentence is `3.001 s` at `1.06x` (`> 2.85 s`) and both `"In one minute"` and `"in one second"` are mandatory; keep blocked and tighten sentence 1 on paper before `J0862` records.
   - `010 Short_A` (`blocked_hook_and_missing_plates`): keep blocked on missing `010` Flow plates; when `010` plates are minted, Chief can choose either **Option A1** (word-preserving `-0.260 s` onset/pause trim + `1.06x` on Sentence 1 -> `2.849 s <= 2.85 s`, `23.289 s` total, `0` words changed) or **Option A2** (re-recording Sentence 1 in `J0862`).
3. **Preserve All Production Holds**:
   - `006 Short_B`, `006 Short_C`, and standalone `S7` stay `planned` only.
   - Standalone `S5`, `S6`, and `S8` stay `unbuilt`.
   - `008 Short_A`, `009 Short_A`, and `010 Short_C` stay `blocked_missing_plates`.
   - `J0862`, `J0863`, and all credit/date/Ben holds remain untouched.
