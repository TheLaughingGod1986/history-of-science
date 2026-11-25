# HOS 127 — Acting Chief Draft Review & FIX Ruling (`J3622`)

- **Reviewer & Acting Chief:** `gemini` (Elected Acting Chief per fresh `chief_relay.py status` on 25 November 2026 — Claude down until `07:50Z`, Codex down on usage limit, Gemini UP)
- **Ruling:** **FIX before lock** (do **not** merge PR `#756` or PR `#771` to `main`; do **not** lock `v01`; do **not** authorise VO or picture spend; `£0.00` / `0` credits spent)
- **Reviewed PRs & Commits:**
  - **HOS PR `#756`** (`gemini/J3504-hos127-script`, commit `d66b6071abd0931b6124e541dc58d030e14e52f9`, built on `origin/main` + `origin/macbook/J3264` Rule-E GO `97.2/100`)
  - **HOS PR `#771`** (`gemini/J3621-hos127-facts-audit`, commit `925c2a92`, stacked directly on `d66b6071`, carrying independent Gemini `facts` lane audit `01_Script/GEMINI_FACTS_CHECK_v01.md`)
- **Byte-for-byte integrity check:** Confirmed `wright_brothers_wind_tunnel_script_master_v01.md`, `SOURCES.md`, `FACT_NOTES_v01.md`, `SHORTS_SCRIPTS_v01.md`, `PACKAGE_FIRST_SCORING_v01.md`, `PRE_BUILD_VIDIQ_AUDIT.md`, and `LAUNCH_PLAN.md` in PR `#771` (`925c2a92`) are byte-for-byte identical to PR `#756` (`d66b6071`).

---

## 1. Packaging Confirmation (Working Direction — Not Rendered / Upload PASS)

- **Titles (working direction confirmed; zero live collisions verified across saved JSONs):**
  - **Primary Arm A (PICK):** **`Wright Brothers First Flight: The 1901 Wind Tunnel`** (`50 chars ≤ 50`, `0` exact collisions in `evidence_2026-11-21_public_search.json`). Leads verbatim with the `J3224` Cluster 4 Lead Film query (`wright brothers first flight`, `19,018`/mo, comp `45`, `10/10` US SERP gap), fits mobile cleanly, and excludes the low-RPM trap `aviation history` (`PK 35%`, `VN 12%`).
  - **T&C Arm B (verbatim plan title):** `Wright Brothers First Flight: The 1901 Wind Tunnel That Solved Lift` (`67 chars ≤ 70`, `0` collisions verified `2026-11-24` in `evidence_2026-11-24_plan_title_search.json`).
  - **T&C Arm C (physics-question lead):** `How Do Airplanes Fly? (The 1901 Wind Tunnel)` (`44 chars ≤ 50`, `0` collisions verified `2026-11-21`).
  - **Neighbour & manifest alignment (`THUMBNAIL_AND_TITLE_RULES.md` §1.3):** `evidence_2026-11-21_neighbours.json` confirms `gate = PASS`, `bigCount = 8` raw (`5` strictly on-topic education videos `≥1M` led by `TED-Ed` ★ `2,568,211`, `hasTed = True`, `failedQueries = []`). Confirm `"wright brothers"` as the manifest neighbour phrase for Arm A so `npm run lint:package` stays aligned with Arm A (and `"how do airplanes fly"` for Arm C).
  - Note: Rubric scores (`96 / 93 / 93`) in `PACKAGE_FIRST_SCORING_v01.md` are pre-production draft judgements, not measured CTR.

- **Thumbnails (draft concepts confirmed with material & §2.6 / §2.9 guardrails; unrendered):**
  - **Concept A (`50% TOO HIGH`, gold on `50%`):** Single dominant hero — 1901 Dayton wooden wind-tunnel cutaway in warm lantern light showing a tiny curved **steel** wing tilting upward on a hacksaw-blade balance inside golden airflow streamlines; clear dark-wood upper-left lettering band; Explorer small lower-left. Carries forward `J3264`'s Smeaton math fix (`0.005` vs `0.0033` = `+51.5%`, never `40%`) with zero title word repetition (§2.5).
  - **Concept B (`200 TINY WINGS`, gold on `200`):** Dayton workshop bench with miniature curved **steel** test wings beside the glowing wind-tunnel mouth; clear upper-left band; Explorer small lower-left. Watch clutter at `168×94` so the miniature wings and tunnel mouth read as one clear focal silhouette.
  - **Mandatory render gates (post-VO, before Ben's watch):** Both concepts are unrendered text briefs. Replace `"brass"` / `"brass and steel"` wording with `steel` (`FIX-5`). All lettering, numbers, and balance dials must be hand-verified / inked in the edit per `§2.6` (never AI-baked), checked via `style_sheet.py` and `thumb_preview.py` (`168×94`), scored on Chief HOOK/BAND/PHONE, and joined by a 3rd Test & Compare thumbnail variant post-VO (`THUMBNAIL_AND_TITLE_RULES.md` §2.9).

---

## 2. Mandatory Corrections Required in `v02` Before Lock (`FIX-1` through `FIX-8`)

### Factual & source blockers (all 5 `J3621` blocking FLAGs upheld)

1. **`FIX-1` (`J3621` FLAG-1) — Inaccurate 1902-vs-1901 longest-glide ratio (`Part 04` spoken line 126, `SCALE` line 119, `FACT_NOTES_v01.md` Row 13).**  
   Spoken v01 says *"stretching their longest run to six hundred and twenty-two and a half feet in twenty-six seconds — **more than double their nineteen oh-one mark**."* The 1901 glider's longest recorded free glide was `389 ft` (8 Aug 1901), making `622.5 / 389 = 1.60×` (not `>2×`). NASA GRC (`1901-wind-tunnel-tests/`) states `"The aircraft were flown frequently up to 300 feet in a single glide"` (*typical* glides, not the record), and `FACT_NOTES_v01.md` Row 13 omitted that quote while contradicting the script with `"almost double"`.  
   **Required fix:** Change spoken line 126 and `SCALE` line 119 either to specify typical 1901 glides (`"more than double their typical three-hundred-foot glides of nineteen oh-one"`, quoting NASA GRC verbatim in Row 13) or to an exact record/field comparison (`"over sixty percent farther than their best nineteen oh-one glide"` / `"more than two football fields"`), and remove the `"almost double"` contradiction in `FACT_NOTES_v02.md` Row 13.

2. **`FIX-2` (`J3621` FLAG-2) — Overstated `"two centuries earlier"` time gap & missing source row for John Harrison H4 handoff (`Part 05` line 160, `SOURCES.md`, `FACT_NOTES_v01.md`).**  
   Spoken line 160 reads *"Yet **two centuries earlier**, another workshop craftsman faced an even deadlier measurement mystery — building a brass watch that had to keep perfect time on a pitching wooden ship at sea."* Royal Museums Greenwich (`ZAA0037`, `https://www.rmg.co.uk/collections/objects/rmgc-object-79142`) confirms Harrison began `H4` in `1755` and completed it in **`1759`** (`142–146 years` before `1901–1905` — a century and a half, remarkably the exact year Smeaton published his paper!), and the handoff currently has zero source row.  
   **Required fix:** Change `"two centuries earlier"` to `"a century and a half earlier"` (or `"in the very same year Smeaton published his table"` / `"a hundred and fifty years earlier"`), and add Row 18 backed by RMG `ZAA0037` to `SOURCES.md` and `FACT_NOTES_v02.md`.

3. **`FIX-3` (`J3621` FLAG-3) — Over-attributed `1/3` lift shortfall in Part 01 (`lines 21 & 40 [TEACH]`) & mismatched `S01` Caption Line 1 (`10_Shorts/SHORTS_SCRIPTS_v01.md` line 19).**  
   - **Long Part 01:** Lines 21 and 40 attribute the entire `1/3` lift drop solely to Smeaton's `0.005` vs `0.0033`, whereas `0.0033 / 0.005 = 2/3` (`−34%`, not `1/3`). NASA GRC (`1901-wind-tunnel-tests/`) explicitly notes `"But this did not account for all of the performance differences. There was still some questions about the lift and drag coefficients which were obtained by Lilienthal"`. Soften Part 01 lines 21 & 40 to identify Smeaton's `0.005` as a major culprit *together with* flawed wing-lift curves (matching Part 02 line 59). Also tighten Part 01 line 9 `"a century-old flight formula"` to `"a 142-year-old flight formula"` or `"an eighteenth-century flight formula"` so it matches Smeaton `1759` and `LAUNCH_PLAN.md`.
   - **Short `S01` Caption Line 1:** Prints `The Wright brothers' flight tables were 50% wrong.` without speaking `50%` or direction (`too high`, violating `J3264` Guardrail 1) while spoken VO immediately states `"lifted only a third"` (`67%` short). Align `S01` Caption Line 1 cleanly with spoken VO (e.g., `Their 1901 glider lifted only a third of what tables promised.` or speak `"fifty percent too high"` explicitly in `S01` VO).

4. **`FIX-4` (`J3621` FLAG-4) — Aerodynamically misleading `"spin backward"` in Short `S02` (`10_Shorts/SHORTS_SCRIPTS_v01.md` lines 44, 49, 57).**  
   Adverse yaw (`"well digging"`) reversed the turn — yawing/spinning the nose **the wrong way** (opposite the bank), not backward in reverse. Replace `"spin backward"` across `S02` spoken line 1, Caption Line 1, and loop check with `"spin the wrong way"` or `"turn the wrong way"` (matching long Part 04 line 111's `"spinning the nose the wrong way"` while keeping `S02` cleanly inside `16.0–19.0 s`).

5. **`FIX-5` (`J3621` FLAG-5) — Contradictory packaging docs, `brass` vs `steel` model material, & missing Smeaton `1759` DOI (`PRE_BUILD_VIDIQ_AUDIT.md`, `LAUNCH_PLAN.md`, `PACKAGE_FIRST_SCORING_v01.md`, `SOURCES.md`, `FACT_NOTES`).**  
   - Sync `PRE_BUILD_VIDIQ_AUDIT.md` lines 27, 29, 43–44, and §§5–6 to Primary Arm A (`Wright Brothers First Flight: The 1901 Wind Tunnel`, `50c`), verified `v02` description, and verified `v02` facts — removing stale `How Do Airplanes Fly?` primary lead at line 43, dropped `THE TABLES LIED` at line 29, and unverified `J3245` outline claims (`6-foot`, `16-inch`, `~66% efficiency`, `cardboard inner-tube box`).
   - Change `"brass"` / `"brass and steel"` miniature wing models in `LAUNCH_PLAN.md` lines 29–30 and `PACKAGE_FIRST_SCORING_v01.md` line 50 to **`20-gauge steel`** (`steel`), matching NASA GRC (`wind-tunnel-models/`) and the script.
   - Add Smeaton's `1759` Royal Society primary DOI (`https://doi.org/10.1098/rstl.1759.0019`) to `SOURCES.md` and `FACT_NOTES_v02.md` Row 4 to source `"142-year-old"` (`1901 − 1759 = 142`).

### Script Teach/Polish, Shorts pacing & hygiene blockers (new catches in `J3622`)

6. **`FIX-6` — Unspoken `1899–1905` timeline `SCALE`, Part 01 line 39 visual chronology, & `WHEN` label length (`studio/RULES.md` Teach on Screen & Polish Pass #4).**  
   - Part 01 `[VISUAL MUST: 0:54]` marks `SCALE: six years from a five-foot kite to a thirty-nine-minute powered flight` on the `1899–1905` timeline, yet `"six years"` is never spoken in VO (`Polish pass #4` requires every `DATA` number's `SCALE` comparison to be spoken aloud). Speak the six-year span cleanly (e.g., in Part 05 when the `1899–1905` timeline completes: `"In just six years, they had gone from a five-foot kite to a thirty-nine-minute airplane"`).
   - Part 01 line 39 (`VISUAL MUST: 1:18`) pairs `1900 wooden camp` and `WHEN: Kitty Hawk, 1900` with `the 1901 glider` (in `1900` they camped in a tent near Kitty Hawk; the wooden camp shed and 1901 glider belonged to `1901` at Kill Devil Hills). Align the visual beat cleanly to one year.
   - Tighten 5–6 word `WHEN:` markers (`Kill Devil Hills, Sept 1902` [5w], `Kill Devil Hills, Oct 1902` [5w], `Kill Devil Hills, 17 Dec 1903` [6w]) so every rendered single-line stamp obeys the `≤4`-word label cap (e.g., `Kill Devil Hills, 1902`, `Oct 1902`, `17 December 1903`).

7. **`FIX-7` — Shorts `S01` & `S02` row WPM pacing imbalance & `HOS_STRATEGY.md` R7 end-card specification (`10_Shorts/SHORTS_SCRIPTS_v01.md`).**  
   Measured row-by-row from `SHORTS_SCRIPTS_v01.md`:
   - **`S01` (`42w`):** Row 3 (`7.8–14.2 s`, `6.4 s`, `19w`) demands **`178.1 wpm`** (`1.19×` of 150 wpm, risking illegal `atempo > 1.06` or spill past `14.2 s`), while Row 4 (`14.2–17.6 s`, `3.4 s`, `3w`: `"...and proved why"`) drops to **`52.9 wpm`** (`~2 s` of dead air before the loop).
   - **`S02` (`42w`):** Row 2 (`3.4–8.6 s`, `5.2 s`, `17w`) demands **`196.2 wpm`** (`1.31×` of 150 wpm, pushing spoken lines across `9.0 s` into the long title card band), while Row 4 (`14.4–17.6 s`, `3.2 s`, `2w`: `"— right after"`) drops to **`37.5 wpm`**.
   - **Required fix:** Rebalance both Shorts' shot-table timestamps to natural `~150 wpm` per row (within `16.0–19.0 s`, `atempo ≤ 1.06`), keep the single `≤4`-word Teach overlay synced to its exact spoken beat strictly clear of `0–2 s` and `9–14 s`, and explicitly specify R7 handling (`9.0–14.0 s` exact live long title *Wright Brothers First Flight: The 1901 Wind Tunnel*, with clean fade/tag before the `≤0.3 s` Frame-0 match-cut loop).

8. **`FIX-8` — `v02` filename hygiene, `_template` plate stub, & `J3621` source/quote polishes.**  
   - Remove or archive superseded `wright_brothers_wind_tunnel_script_master_v01.md` out of `01_Script/` when `v02` lands so default `npm run gate:episode` (without `--script`) resolves `v02` directly.
   - Keep unfilled `_template` stub `07_Edit-Project/parts/part-01_plates_v01.json` (`"film": "NNN_Slug"`) cleared/unlisted as completed work in `production-status.md` until post-VO picture stage.
   - Fold in `J3621`'s `R04`/`R10`/`R14`/`R16` source/quote polishes into `SOURCES.md` and `FACT_NOTES_v02.md`: full Row 4 Smithsonian quote (`"...0.0033 for Smeaton's coefficient."`), Row 10 `1/32 in = 0.794 mm` vs `0.76 mm` bank-card wording (remove reversed `"thinner than a credit card"` comment), Row 14 verbatim `"Ten responded..."` quote + tighten line 133 `"In nineteen oh-three"` → `"By early nineteen oh-three"` (inquiries began late 1902), and Row 16 verbatim `14 Dec` / `3.5 s` / `60-foot` quotes.

---

## 3. Teach on Screen, Polish Pass & Craft Audit Summary

| Area | Audit Result on `v01` | Notes for `v02` |
|---|---|---|
| **Opening milestones (`@150 wpm`)** | Title question `0.0–6.8 s` (`≤0:08`), promise `6.8–13.6 s` (`≤0:15`), stakes `13.6–23.2 s` (`≤0:25`), first fact `23.2–30.4 s` (`<0:45`), early `DATA+SCALE` `30.4–43.2 s` | **PASS on timings** (tighten `"century-old"` → `"142-year-old"` / `"eighteenth-century"` and fix Smeaton-only `1/3` causality per `FIX-3`). |
| **DATA + SCALE** | `7 DATA`, `7 SCALE` (`SCALE ≥ DATA`); `1899–1905` timeline present | **FIX-1 & FIX-6:** Fix 1902 vs 1901 `622.5 ft` scale ratio and speak the `1899–1905` six-year timeline scale in VO. |
| **WHO cards** | `5 WHO` (all 5 named people covered, verified lifespans, `≤3`-word year-accurate roles) | **PASS.** |
| **WHEN stamps** | `12 WHEN` | **FIX-6:** Fix `1900` camp / `1901` glider visual mix at line 39; keep single-line `WHEN` labels `≤4` words. |
| **FACT & LABEL** | `4 FACT` (`3–4w` each), `27 LABEL` (`2–4w` each, `0` over 4 words) | **PASS.** |
| **Explorer & Craft** | `2 [EXPLORER ACTS]` (Parts 02 & 05, outside first minute); `4 [CHAPTER CARD]` (5 parts); midpoint twist (`"Case closed? Not even close."` at end of Part 03); accurate aerodynamic lift physics (equal-transit-time debunked); no goodbye/subscribe ask | **FIX-2:** Fix Harrison H4 handoff (`"a century and a half earlier"`, add RMG `ZAA0037` Row 18). Note chapter timestamps at `@150 wpm` (`0:00`, `1:39`, `3:00`, `4:16`, `5:59`, total `7:55`) differ slightly from draft headers (`0:00`, `1:30`, `3:10`, `4:50`, `6:30`); re-time from locked VO. |
| **Shorts house rules (19 Nov)** | 3D cartoon Frame 0, zero Explorer at Frame 0, `42w`/`42w` inside `16–19 s`, `0` collisions, causal loops | **FIX-3, FIX-4, FIX-7:** Align `S01` Caption Line 1, replace `S02` `"spin backward"`, rebalance row WPM (`178`/`196 wpm` spikes) and specify R7 title/loop cleanly. Rendered media gates wait for media. |
| **Picture / Audio / Polish gates** | Unverified (script stage only) | SFX (`sfx_kit.py level`), music by part, fine grain, crossfades, and motion checks remain unverified until media exists. |

---

## 4. Fresh Local Verification & Input Hashes (`925c2a92` / `d66b6071`)

Independently run on a detached export of **HOS PR `#771`** (`925c2a92`, 25 Nov 2026):

```text
review:script: Decision: PASS · Score: 93.6 / 100
hook: 9.5 | curiosity: 9.5 | storytelling: 9 | scientificAccuracy: 10 | emotion: 9.6
escalation: 8.8 | retentionPotential: 9 | searchPotential: 9.1 | visualOpportunities: 9.5 | narrationFlow: 9.6
Words: 1239 · Est. min: 8.3 · Chapters: 4
Findings: Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.

gate:episode: Decision: PASS — VO / Gemini Veo allowed
project_dir: OK | prebuild_vidiq: OK | script_file: OK | script_review: OK (93.6/90)
explorer_acts: OK (2) | visual_must: OK (29) | teach: OK (5) | chapters: OK (4) | production_checklist: OK
```

Mechanical linter passes do not override the 5 verified factual/packaging defects (`FIX-1`–`FIX-5`) or the script/Shorts/hygiene defects (`FIX-6`–`FIX-8`).

**Verified Input SHA-256 Hashes (identical in PR `#756` `d66b6071` and PR `#771` `925c2a92`):**
- `01_Script/wright_brothers_wind_tunnel_script_master_v01.md`: `7d6c4fb2c811460d0cb560010ecd558cdd3171127ba3c1c88cc291ce38c7cec5`
- `01_Script/SOURCES.md`: `dffd651099b8fefb12dc1b624ff7900c7baf62d617111ae243484aa9a88ff0ba`
- `01_Script/FACT_NOTES_v01.md`: `7a61c698964923cdd1dfb563787b7ad9cbad7a0a3ec22611a0edeb02cd1c8531`
- `01_Script/GEMINI_FACTS_CHECK_v01.md` (PR `#771` `925c2a92`): `1ba23c9e9cd38ac79e70ae9f5029b2e3ae26ba9f6bbe27fcb4737480081d7842`
- `10_Shorts/SHORTS_SCRIPTS_v01.md`: `94926359b01c728e48edf41394b3511817d5c70ef5d09a5d875f028a6d03b19b`
- `11_Upload-Package/PACKAGE_FIRST_SCORING_v01.md`: `760f774048faecb740441bc68325e53c55719ab8b3fad460329198bc70f2f909`
- `11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md`: `ef25520459afb0dd4fbdbebf4b4cb3c7768169a41b2c1bbf51d90b3f7c4a5227`
- `11_Upload-Package/LAUNCH_PLAN.md`: `1bbe22c016a5b938632433c936ec8496f2ec362af633d001a764dbac83516e66`

---

## 5. Acting Chief Ruling (`gemini`), Next Queue Step & Rule G WIP Guard

- **Formal Ruling:** **FIX before lock.** PR `#756` and PR `#771` remain unmerged; `v01` is **not** locked; no VO or picture spend is authorised (`£0.00`).
- **Queued Follow-On:** Acting Chief (`gemini`) queues the `v02` correction job (`kind: script`, stacked cleanly on `origin/gemini/J3621-hos127-facts-audit` `925c2a92`) resolving `FIX-1` through `FIX-8`, to be followed by independent `v02` `facts` re-verification against exact `v02` hashes and final Chief lock/merge (due **Fri 11 Dec 2026**; Ben's watch by **Mon 28 Dec**; target air **Thu 31 Dec 2026 18:00 London**, with standing 1-week slip contingency if needed).
- **`J3622` Disposition:** Parked (`wait --type dependency`) on completion of the `v02` correction + `v02` facts re-verification so `J3622` closes only when Chief script lock is actually achieved.
- **Rule G WIP Guard (`orbit-with-ben/jobs/WIP.json` checked 25 Nov 2026):** HOS currently occupies **5 of 5** active slots (`HOS:009`, `HOS:010`, `HOS:013`, `HOS:128`, `HOS:136`). Even after `v02` locks, `HOS:127` VO waits for an open HOS WIP place behind `HOS:137`.
