# Production status — 137 Accidental Inventions: 5 Mistakes That Worked

| Field | Value |
|---|---|
| Slug | `137_Accidental-Inventions-That-Changed-The-World` |
| Channel | `@HistoryOfScienceYT` only |
| Plan / Cluster | `hos-search-2027-01` Film 3 · Cluster 3 (Accidental & World-Changing Inventions) |
| Topic | **Rule-E GO (`95.8 / 100` · `9.58 / 10`, `J3503`, `2026-11-24`)** — `10/10` gates PASS; Safety Glass (1903) locked over Microwave (zero overlap with `HOS:129`) |
| Package-first | `11_Upload-Package/PACKAGE_FIRST_SCORING_v01.md` & `LAUNCH_PLAN.md` (working direction confirmed in `J3687`, `2026-11-25`): Primary Arm A `Accidental Inventions: 5 Mistakes That Worked` (`45c`, `0` collisions; manifest neighbour phrase `"inventions"` per §1.3), T&C Arm B (`69c`) & Arm C (`56c`), Draft Thumb Concepts A (`NEARLY TRASHED`, gold on `TRASHED`) & B (`WRONG RESISTOR`, gold on `WRONG`, §2.6 hand-verified; unrendered drafts until post-VO; 3rd T&C variant built post-VO per §2.9), S01 `48c` & S02 `54c` (`0` collisions) |
| Pre-build vidIQ audit | `11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md` (updated & signed off in `J3513`, `2026-11-24`) |
| Script review | **LOCKED — PASS `91.8 / 100`** (`01_Script/accidental_inventions_script_master_v02.md`, sha256 `d2a359c4...`, `1,256` words, `8.4` min, `4` chapter cards, `8/8` structure gates; sole master script in `01_Script/`; Acting Chief `gemini` **KEEP & LOCK** in `J3687`, HOS PR `#775` merged `b4622600` superseding `#747`/`#754`/`#769`/`#772`, `J3565` closed `done`) |
| Episode gate | **PASS (`9/9 OK`)** (default `npm run gate:episode` without `--script` resolves `accidental_inventions_script_master_v02.md`, all checks `OK` — VO still held strictly under Rule G WIP until an open HOS slot clears) |
| Sources & Facts | **LOCKED (`J3687` KEEP, `2026-11-25`):** `01_Script/SOURCES.md` (`bc755590...`), `01_Script/FACT_NOTES_v02.md` (`7f502091...`) & `01_Script/GEMINI_FACTS_CHECK_v02.md` (`1fd7a797...`, `J3686`: **`18 OK · 10 PARTIAL · 0 FLAG`** across 28 items, `36/36` live URLs `HTTP 200`; `J3687` direct live HTTP quote verification `35/36` direct `HTTP 200` + `3M Post-it` search-grounded) |
| Shorts scripts | **LOCKED (`J3687` KEEP, `2026-11-25`):** `10_Shorts/SHORTS_SCRIPTS_v02.md` (`62ff7c99...`, `S01` `42` spoken words / `17.2 s` Sat 26 Dec & `S02` `42` spoken words / `17.2 s` Fri 25 Dec, `~150 wpm` per row, `≤4`-word synced Teach overlays clear of `0–2 s` & `9–14 s`, R7 end-title layout, 16–19 s Ben 19 Nov house rules) |
| VO | pending — held under Rule G WIP (`orbit-with-ben/jobs/WIP.json` currently `5/5` HOS active: `009`, `010`, `013`, `128`, `136`; queue Mac-mini Ben Orbit Narrator VO once an open HOS WIP slot clears) |
| Picture | pending (Flow Veo 3.1, plate library — starts only after Chief VO PASS; Flow renews 12 Dec) |
| Runtime target | 7–9 min, 5 parts (`8.4` min est. at 150 wpm) |
| Ben's watch target | Mon 21 Dec 2026 |
| Air | Thu 24 Dec 2026 18:00 London, normal publish (no Premiere; slides one week if not ready) |
| Shorts | 16–19 s search-question Shorts (Fri 25 Dec & Sat 26 Dec promote this long, `0` collisions verified in `J3503`; Sun & Tue cluster/candidate rotation), Related → this long |

## Acting Chief `KEEP` & Script Lock (`2026-11-25` · `J3687`)

- **Ruling:** **`KEEP` & SCRIPT LOCKED** (`jobs/reviews/J3687/REVIEW.md`, elected Acting Chief `gemini` under `Claude -> Codex -> Gemini -> Grok`; `chief_relay.py status` = `Chief: Gemini`).
- **Merged PR:** HOS PR `#775` merged into `main` as **`b4622600888c536da1cc894344daca30a4eae4b2`** (auto-merging/superseding PRs `#747`, `#754`, `#769`, and `#772`); parent **`J3565`** closed `done`.
- **Locked `v02` SHA-256 Hashes:**
  - `01_Script/accidental_inventions_script_master_v02.md`: `d2a359c4cb30b707b9ac723693372c6faba1d65ca1d32d8241a2b9a3c25caecb`
  - `01_Script/SOURCES.md`: `bc755590b3f7df7894f03fc2a202f60b92641aac9bc657107771e65d8bfbdb0c`
  - `01_Script/FACT_NOTES_v02.md`: `7f5020911bbc8dd5e2f9c2911095c8fd7657ef8b029575fb071e1bcccc6df4b4`
  - `01_Script/GEMINI_FACTS_CHECK_v02.md`: `1fd7a797be0ae74292f9c00e753800c61d2fac40b1689dbb486827e60ddd01da`
  - `10_Shorts/SHORTS_SCRIPTS_v02.md`: `62ff7c99d88c0416f0b6a23191b8fb60e1915776c91fc67e2d5fb67163f0da94`
- **Rule G WIP Hold:** HOS currently occupies `5/5` active WIP slots (`HOS:009`, `HOS:010`, `HOS:013`, `HOS:128`, `HOS:136`). Long VO and Shorts `S01`/`S02` VO are held cleanly until an HOS WIP slot opens (`£0.00` spent; no upload/schedule). Picture and rendered thumbnails wait for Chief VO PASS.

## Script & Episode Gate Evidence (`2026-11-25` · `J3685` / `J3687` `v02`)

### 1. `npm run review:script` — **PASS (`91.8 / 100`)**
```text
# accidental_inventions_script_master_v02.md

Decision: PASS · Score: 91.8 / 100
hook: 9.5 | curiosity: 7.9 | storytelling: 9.5 | scientificAccuracy: 10 | emotion: 9.6
escalation: 8.1 | retentionPotential: 9 | searchPotential: 9.1 | visualOpportunities: 9.5 | narrationFlow: 9.6
Words: 1256 · Est. min: 8.4 · Chapters: 4
Findings:
- [info] overall: Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- [info] overall: PASS 91.8/100 — proceed to VO after production checklist.
Pass threshold: 90
```

### 2. `npm run gate:episode` (default, no `--script`) — **PASS**
```text
# Episode gate — 137_Accidental-Inventions-That-Changed-The-World
Decision: PASS — VO / Gemini Veo allowed (VO held strictly under Rule G WIP until an open HOS WIP slot clears)
project_dir: OK | prebuild_vidiq: OK | script_file: OK (01_Script/accidental_inventions_script_master_v02.md) | script_review: OK (91.8/90)
explorer_acts: OK (2) | visual_must: OK (19) | teach: OK (5) | chapters: OK (4) | production_checklist: OK
```

### 3. Teach on Screen & Polish Pass Marker Counts (`accidental_inventions_script_master_v02.md`)
- `CHAPTER CARD:` `4` (Parts 02–05; Part 01 has no chapter card)
- `VISUAL MUST:` `19` · `TEACH:` `5` · `EXPLORER ACTS:` `2` (both outside first minute: Part 02 & Part 05)
- `DATA:` `5` · `SCALE:` `5` (`SCALE ≥ DATA`, every `DATA` number & `SCALE` spoken in VO and sourced in `FACT_NOTES_v02.md`)
- `WHO:` `13` (all 13 named people covered with live-opened lifespan quotes & `≤4`-word year-accurate roles)
- `WHEN:` `10` · `FACT:` `4` (all `≤4` words: `100× larger resistor`, `Died $200,000 in debt`, `Used in gas masks`, `90% wanted to buy`) · `LABEL:` `18` (all `≤4` words)
- Part 01 opening milestones @ 150 wpm: title question `0:05.6` (`≤0:08`), promise `0:14.0` (`≤0:15`), stakes `0:21.2` (`≤0:25`), Greatbatch 1956 `100×` error `0:21.2–0:35.6` (inside `0:25–0:40`, well before `<0:45`).

### 4. `v02` Corrections Verified Resolved (`J3685` / `J3686` / `J3687`)
- **`FIX-1` (`FR 405,881`):** Part 03 line 85 speaks *"August nineteen oh-nine"* matching primary `FR405881A` (`1909-08-10`); `FR405881A` in `SOURCES.md` & `FACT_NOTES_v02.md`.
- **`FIX-2` (Chardack-Greatbatch 1960):** Part 01 spoken text & comparison card updated to `June 1960` (`Buffalo June 1960`) and `two years` survival per `PMC3232561` & VA (two-stage April lead / June pulse-generator procedure and Wikipedia `18 months` variance documented in `FACT_NOTES_v02.md`).
- **`FIX-3` (Dead URL, lifespans & 8 primary upgrades):** Dead `HTTP 521` `heartrhythm.com` removed everywhere and replaced with live `PMC3232561`; all 8 `J3564` primary/institutional upgrades merged; live-opened lifespan quotes added for Chardack (`1914–2006`), Gage (`1922–2024`), Elmqvist (`1906–1996`), and Senning (`1915–2000`); un-upheld v01 all-OK tally removed.
- **`FIX-4` (Microsphere chemistry):** `"low-tack"` replaced with `"low-adhesion, pressure-sensitive adhesive"` in Part 05, `SOURCES.md`, and `FACT_NOTES_v02.md` matching primary `US3691140A` & NIHF.
- **`FIX-5` (Part 01 opening & blink scale):** Part 01 agenda line trimmed so all opening milestones hit target (`≤0:15` promise, `≤0:25` stakes, `0:25–0:40` Greatbatch `100×` error); `"briefer than a camera flash"` replaced with *"less than two thousandths of a second, a tiny fraction of a blink"* backed by Harvard BioNumbers `BNID 100706` (`100–400 ms`) & `PMC4043155`.
- **`FIX-6` (Part 02 spoken `DATA`/`SCALE` & Part 05 alignment):** Goodyear's `270°F` (`132°C`, *"hotter than boiling water"*) cure spoken in Part 02 VO backed by primary `US3633A`; Long Part 05 and Short `S02` aligned on 3M's `ninety percent` (`nine out of every ten`); secondary-only `"aerospace"` removed.
- **`FIX-7` (`FACT:` cap):** Part 03 `FACT:` card tightened from 5 words to 4 words (`Used in gas masks`).
- **`FIX-8` (Shorts `v02`):** `10_Shorts/SHORTS_SCRIPTS_v02.md` rebalanced to `~150 wpm` per row (`42` spoken words → `17.2 s`, `atempo ≤ 1.06`), synced `≤4`-word Teach overlays (`1.8 MS PULSE` & `1974 CHOIR BOOKMARK`) clear of `0–2 s` and `9–14 s`, and R7 end-title layout preserving `≤0.3 s` Frame-0 match-cut loop.
- **`FIX-9` (Filename & stub hygiene):** `accidental_inventions_script_master_v01.md` removed so `accidental_inventions_script_master_v02.md` is the sole master in `01_Script/`; unfilled `_template` `part-01_plates_v01.json` cleared from completed plate-board status below.

### 5. Independent Gemini `v02` Facts & Exact-Quote Audit (`2026-11-25` · `J3686`)
- **Report:** `01_Script/GEMINI_FACTS_CHECK_v02.md` (audited PR `#772` commit `be99dffe`; all 4 `v02` script/source/Shorts files byte-for-byte unchanged, `£0.00` spent).
- **Tally (`28` audited items):** **`18 OK · 10 PARTIAL · 0 FLAG`** (`36/36` unique URLs independently fetched live `HTTP 200`, `0` dead URLs; `10 PARTIAL` items are solely labelled secondary Wikipedia dependencies or documented non-blocking historical nuances).
- **Chief lock (`J3687`):** Independently re-verified all 9 fixes, live quotes, opening timings, card caps, Shorts pacing, `review:script` `91.8`, default `gate:episode`, `check_all.sh`, and `7/7` CI green.

---

## Topic Gate Evidence (`2026-11-24` · Audited in `J3503`)

### 1. Search-Led Gate (`J3224`, `05_Analytics/hos/search_research/2026-11-20.md`) — **PASS**
- `inventions that changed the world`: `35,881`/mo (**US 23%** = 8,280 US/mo), **10/10** US signed-out top-10 gap.
- `accidental discoveries`: `9,367`/mo, competition `39`, **+93.0% growth**, parent `amazing discoveries` `25.7k` (**AU 20% + US 20%**), **9/10** gap.
- `accidental inventions that changed the world`: `8,092`/mo, **+73.9% growth**, **10/10** gap; `inventions that shook the world`: `8,001`/mo, comp `32`, **+69.5%**.
- Small-channel outliers (`<50k`, `≥5×`): `Invention Flex` (6.2K US → `9.6K`, `8.3×`), `Industrial Case Files` (138 US → `4.7K`, `8.6×`), `Counter Facts Lab` (1.4K → `1.5K`, `22×`), `TheOriginLens` (246 → `1.6K`, `8×`).

### 2. Neighbour Tie-Breaker (`neighbours.py`, `2026-11-24`) — **PASS (`3` Strictly Relevant `≥1M` + `SciShow` `1.48M`)**
```text
Words the top neighbours share: the world, that changed, changed the
TED-Ed/TED neighbour: yes
Big neighbours (≥ 1,000,000 views): 4 (need 3)
Neighbour gate (≥ 3 education videos with 1,000,000+ views): PASS
Raw pull: 02_Video-Projects/137_Accidental-Inventions-That-Changed-The-World/11_Upload-Package/evidence_2026-11-24_neighbours.json
```
Strictly relevant `≥1M` education neighbours in `evidence_2026-11-24_neighbours.json` (`3` of `4` raw; `2` `TED-Ed` ★ `≥1M`): `Thoughty2` `1,594,081` (*10 Inventions That Changed the World*, `Zaez9eM8wTs`), `TED-Ed` ★ `1,486,538` (*The accident that changed the world*, `CNbnLgetqHs`), `TED-Ed` ★ `1,041,862` (*How inventions change history (for better and for worse)*, `0SMNYivhGsc`). Transparently excluded as off-topic in `J3503`: `TED-Ed` `RzkD_rTEBYs` (*How will AI change the world?*, `2,323,113`). Reinforced by `SciShow` `1,484,724` (*6 Incredible Discoveries Made on Accident*, `YYyfioO50fM`) in `evidence_2026-11-24_public_search.json`.

### 3. Public Search & Collision Check (`public_search.py`, `2026-11-24`, `13` queries after `J3503`) — **PASS (`0` Collisions on Updated Titles & Shorts)**
- `5/5` core phrases `autocomplete = yes`: `"accidental inventions that changed the world"`, `"accidental discoveries"`, `"inventions that changed the world"`, `"accidental inventions"`, `"inventions that shook the world"`.
- **Collision caught & fixed in `J3503`:** PR `#743`'s original Title A `5 Accidental Inventions That Changed the World` had 5 exact live collisions (incl. `Arun Surya Teja` `nLbBtuydgZo` 251,692 views) and was retired.
- Exact title collisions across updated Long Titles A (`45c`), B (`69c`), C (`56c`), alternate (`48c`), and Short Titles S01 (`61c` & `48c`) and S02 (`54c`): **`0`**.
- Raw pull: `02_Video-Projects/137_Accidental-Inventions-That-Changed-The-World/11_Upload-Package/evidence_2026-11-24_public_search.json`

## Parts

| Part | Plate board | Latest cut | Status |
|---|---|---|---|
| 01 | — *(unfilled `_template` stub only; starts post-VO)* | — | script `v02` **LOCKED** (`91.8/100` PASS, `J3687` KEEP; VO held on Rule G WIP) |
| 02 | — | — | script `v02` **LOCKED** |
| 03 | — | — | script `v02` **LOCKED** |
| 04 | — | — | script `v02` **LOCKED** |
| 05 | — | — | script `v02` **LOCKED** |

Keep this file current on `main`. A STOP (quota, auth, missing VO) is a line here, not an open branch.
