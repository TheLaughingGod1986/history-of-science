# Production status — 137 Accidental Inventions: 5 Mistakes That Worked

| Field | Value |
|---|---|
| Slug | `137_Accidental-Inventions-That-Changed-The-World` |
| Channel | `@HistoryOfScienceYT` only |
| Plan / Cluster | `hos-search-2027-01` Film 3 · Cluster 3 (Accidental & World-Changing Inventions) |
| Topic | **Rule-E GO (`95.8 / 100` · `9.58 / 10`, `J3503`, `2026-11-24`)** — `10/10` gates PASS; Safety Glass (1903) locked over Microwave (zero overlap with `HOS:129`) |
| Package-first | `11_Upload-Package/PACKAGE_FIRST_SCORING_v01.md` & `LAUNCH_PLAN.md` (`J3513`, updated `J3685`): Primary Arm A `Accidental Inventions: 5 Mistakes That Worked` (`45c`, `0` collisions; manifest neighbour phrase `"inventions"` per §1.3), T&C Arm B (`69c`) & Arm C (`56c`), Draft Thumb Concepts A (`NEARLY TRASHED`, gold on `TRASHED`) & B (`WRONG RESISTOR`, gold on `WRONG`, §2.6 hand-verified; unrendered drafts until post-VO; 3rd T&C variant built post-VO per §2.9), S01 `48c` & S02 `54c` (`0` collisions) |
| Pre-build vidIQ audit | `11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md` (updated & signed off in `J3513`, `2026-11-24`) |
| Script review | **PASS — `91.8 / 100`** (`01_Script/accidental_inventions_script_master_v02.md`, `1,256` words, `8.4` min, `4` chapter cards, `8/8` structure gates; sole master script in `01_Script/`; resolves `FIX-1`–`FIX-9`; awaits independent `v02` `facts` re-verification + Chief lock) |
| Episode gate | **PASS** (default `npm run gate:episode` without `--script` resolves `accidental_inventions_script_master_v02.md`, all checks `OK` — VO/Veo still held pending `v02` `facts` re-verification, Chief lock & open WIP slot under Rule G) |
| Sources & Facts | `01_Script/SOURCES.md`, `01_Script/FACT_NOTES_v02.md` & prior v01 audit `01_Script/GEMINI_FACTS_CHECK_v01.md` (`J3564` PR `#769` + `J3565` PR `#770`): all 4 `J3564` FLAGs & 5 `J3565` fixes resolved in `v02` (`J3685`, `2026-11-25`) with dead `heartrhythm.com` URL replaced by `PMC3232561`, all 8 primary upgrades merged, 4 missing lifespan quotes + Harvard BioNumbers blink-duration quote added; awaits independent `v02` `facts` check |
| Shorts scripts | `10_Shorts/SHORTS_SCRIPTS_v02.md` (`S01` `42` spoken words / `17.2 s` Sat 26 Dec & `S02` `42` spoken words / `17.2 s` Fri 25 Dec, `150 wpm` per row, `≤4`-word synced Teach overlays, R7 end-title layout, 16–19 s Ben 19 Nov house rules; awaits `v02` `facts` check & Chief lock) |
| VO | pending (Ben Orbit Narrator — starts only after script/facts lock & open WIP slot) |
| Picture | pending (Flow Veo 3.1, plate library — starts only after script & VO PASS; Flow renews 12 Dec) |
| Runtime target | 7–9 min, 5 parts (`8.4` min est. at 150 wpm) |
| Ben's watch target | Mon 21 Dec 2026 |
| Air | Thu 24 Dec 2026 18:00 London, normal publish (no Premiere; slides one week if not ready) |
| Shorts | 16–19 s search-question Shorts (Fri 25 Dec & Sat 26 Dec promote this long, `0` collisions verified in `J3503`; Sun & Tue cluster/candidate rotation), Related → this long |

## Script & Episode Gate Evidence (`2026-11-25` · `J3685` `v02`)

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
Decision: PASS — VO / Gemini Veo allowed (production still held pending v02 facts re-verification, Chief lock & open WIP slot under Rule G)
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

### 4. `v02` Corrections Applied (`2026-11-25` · `J3685`, resolving `J3564` PR `#769` & `J3565` PR `#770`)
- **`FIX-1` (`FR 405,881`):** Updated Part 03 line 85 to *"August nineteen oh-nine"* matching primary `FR405881A` (`1909-08-10`); added `FR405881A` to `SOURCES.md` & `FACT_NOTES_v02.md`.
- **`FIX-2` (Chardack-Greatbatch 1960):** Updated Part 01 spoken text & comparison card to `June 1960` (`Buffalo June 1960`) and `two years` survival per `PMC3232561` & VA (two-stage April lead / June pulse-generator procedure and Wikipedia `18 months` variance documented in `FACT_NOTES_v02.md`).
- **`FIX-3` (Dead URL, lifespans & 8 primary upgrades):** Replaced dead `HTTP 521` `heartrhythm.com` URL everywhere with live `PMC3232561`; merged all 8 `J3564` primary/institutional upgrades; added live-opened lifespan quotes for Chardack (`1914–2006`), Gage (`1922–2024`), Elmqvist (`1906–1996`), and Senning (`1915–2000`); removed the un-upheld v01 all-OK tally claim.
- **`FIX-4` (Microsphere chemistry):** Replaced `"low-tack"` with `"low-adhesion, pressure-sensitive adhesive"` in Part 05, `SOURCES.md`, and `FACT_NOTES_v02.md` matching primary `US3691140A` & NIHF.
- **`FIX-5` (Part 01 opening & blink scale):** Trimmed Part 01 agenda line so all opening milestones hit target (`≤0:15` promise, `≤0:25` stakes, `0:25–0:40` Greatbatch `100×` error); replaced `"briefer than a camera flash"` with *"less than two thousandths of a second, a tiny fraction of a blink"* backed by Harvard BioNumbers `BNID 100706` (`100–400 ms`) & `PMC4043155`.
- **`FIX-6` (Part 02 spoken `DATA`/`SCALE` & Part 05 alignment):** Spoke Goodyear's `270°F` (`132°C`, *"hotter than boiling water"*) cure in Part 02 VO backed by primary `US3633A`; aligned Long Part 05 and Short `S02` on 3M's `ninety percent` (`nine out of every ten`); removed secondary-only `"aerospace"`.
- **`FIX-7` (`FACT:` cap):** Tightened Part 03 `FACT:` card from 5 words to 4 words (`Used in gas masks`).
- **`FIX-8` (Shorts `v02`):** Created `10_Shorts/SHORTS_SCRIPTS_v02.md` pacing every row of `S01` and `S02` at `150 wpm` (`42` spoken words → `17.2 s`, `atempo ≤ 1.06`), syncing `≤4`-word Teach overlays (`1.8 MS PULSE` & `1974 CHOIR BOOKMARK`) to their spoken lines clear of `0–2 s` and `9–14 s`, and specifying R7 end-title layout without breaking the `≤0.3 s` Frame-0 match-cut loop.
- **`FIX-9` (Filename & stub hygiene):** Removed `accidental_inventions_script_master_v01.md` so `accidental_inventions_script_master_v02.md` is the sole master in `01_Script/`; cleared unfilled `_template` `part-01_plates_v01.json` from completed plate-board status below.

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
| 01 | — *(unfilled `_template` stub only; starts post-VO)* | — | script `v02` drafted (`91.8/100` PASS, awaits `v02` facts check & Chief lock) |
| 02 | — | — | script `v02` drafted |
| 03 | — | — | script `v02` drafted |
| 04 | — | — | script `v02` drafted |
| 05 | — | — | script `v02` drafted |

Keep this file current on `main`. A STOP (quota, auth, missing VO) is a line here, not an open branch.
