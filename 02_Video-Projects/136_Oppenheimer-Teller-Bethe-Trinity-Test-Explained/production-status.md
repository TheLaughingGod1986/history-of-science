# Production status — 136 Trinity Test Explained: Could It Ignite the Sky?

| Field | Value |
|---|---|
| Slug | `136_Oppenheimer-Teller-Bethe-Trinity-Test-Explained` |
| Channel | `@HistoryOfScienceYT` only |
| Plan / Cluster | `hos-search-2027-01` Film 2 · Cluster 2 (Nuclear & Modern Physics) |
| Topic | **Rule-E GO (`96.3 / 100` · `9.63 / 10`, `J3502`, `2026-11-24`)** — `10/10` gates PASS |
| Package-first | `11_Upload-Package/PACKAGE_FIRST_SCORING_v01.md` & `LAUNCH_PLAN.md` (`J3507`, `2026-11-24`): Primary Arm A `Trinity Test Explained: Could It Ignite the Sky?` (`48c`, `96/100`), Thumb A `AIR ON FIRE?` (`96/100`), Thumb B `MEASURED BY PAPER` (`93/100`), S01 `44c` & S02 `58c` (`0` collisions) |
| Pre-build vidIQ audit | `11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md` (updated & signed off for v01 draft in `J3507`, `2026-11-24`) |
| Script review | **PASS — `93.7 / 100`** (`01_Script/trinity_test_explained_script_master_v01.md`, `1,266` words, `8.4` min, `4` chapter cards, `8/8` structure gates; awaits independent `facts` lane + Chief lock) |
| Episode gate | **PASS** (all checks `OK` — VO/Veo still held pending Chief lock & open WIP slot under Rule G) |
| Sources & Facts | `01_Script/SOURCES.md`, `01_Script/FACT_NOTES_v01.md` & **`01_Script/GEMINI_FACTS_CHECK_v01.md`** (`J3552`, `2026-11-25`: **13 OK · 2 PARTIAL · 8 FLAG** across 23 items; 8 blocking FLAGs + primary upgrades incl. 22-page declassified `LA-602` PDF handed off to `J3553` for v02 revision before lock; `£0.00` spent) |
| Shorts scripts | `10_Shorts/SHORTS_SCRIPTS_v01.md` (`J3552` FLAG-5 & FLAG-7: actual counts `S01` `55w` / `S02` `65w` exceed 16–19 s house rule, and `S02` `"silent shockwave"` needs fix before lock; titles `S01` `44c` & `S02` `58c` confirmed `0` collisions) |
| VO | pending (Ben Orbit Narrator — starts only after script/facts lock & open WIP slot) |
| Picture | pending (Flow Veo 3.1, plate library — starts only after script & VO PASS) |
| Runtime target | 7–9 min, 5 parts (`8.4` min est. at 150 wpm) |
| Ben's watch target | Mon 14 Dec 2026 |
| Air | Thu 17 Dec 2026 18:00 London, normal publish (no Premiere; slides one week if not ready) |

---

## Independent Gemini Facts Audit (`J3552`, `2026-11-25`)

- **Audit file:** `01_Script/GEMINI_FACTS_CHECK_v01.md` (audited PR `#753` commit `ebb55eea`; script & Shorts files left byte-for-byte unchanged; `£0.00` spent).
- **Tally (`23` items = `R01–R20` + `S01` + `S02` + `P01`):** **`13 OK · 2 PARTIAL · 8 FLAG`**.
- **8 Blocking `FLAG`s handed off to `J3553` (do not lock `v01` as-is):**
  1. **FLAG-1 (`SOURCES.md` & `FACT_NOTES_v01.md` Row 7):** Wrong OSTI URL `https://www.osti.gov/biblio/4036390` (actually an unrelated 1964 R. M. Misra paper); replaced in audit with verified 22-page Wayback scan of declassified `LA-602` (`14 August 1946`, declassified `2-2-73`).
  2. **FLAG-2 (Long Part 02 lines 40 & 51):** Unsourced `"a thousand times faster"` cooling ratio contradicts `LA-602`'s headline `~1.6` worst-case minimum safety factor (`7.4` with inverse Compton in 57 m sphere).
  3. **FLAG-3 (`FACT_NOTES_v01.md` Rows 8 & 9):** Missing verbatim quotes; Wikipedia `Arthur_Compton` & `Hans_Bethe` do not mention Pearl Buck or `"three chances in a million"` (upgraded with `LA-602` verbatim PDF quotes + CrossRef DOI `10.1080/00963402.1976.11455623` for Bethe June 1976).
  4. **FLAG-4 (Long Part 04 line 86 `VISUAL MUST: 5:03`):** Bainbridge's countdown bunker (`S-10000`) was `10,000 yards` (`~5.7 miles`) from Ground Zero, not `"ten miles away"` (Base Camp was ~10 miles).
  5. **FLAG-5 (Short `S02` lines 56 & 62):** `"silent shockwave"` misattaches silence to the shockwave (the *flash* was silent for 40 s; the blast wave arrived with a roar).
  6. **FLAG-6 (Long Part 03 lines 65 & 77):** Inverted speed-of-light math — light crosses a football field in `~0.33 µs`, so `1 µs` is `~3×` LONGER (and plural microseconds `~10–100×` longer), not `"shorter than light takes to cross a football field"`.
  7. **FLAG-7 (Shorts `S01` & `S02`):** Actual spoken word counts are **`55w`** (`S01`, `~21.4–23.5 s`) and **`65w`** (`S02`, `~25.3–27.5 s`) vs claimed `44w`/`46w`, exceeding the `16–19 s` house rule.
  8. **FLAG-8 (`FACT_NOTES_v01.md` Row 10):** Sentence splice without `[...]` in Wikipedia `Edward_Teller` mutates `"its head"` from Theoretical Division to Los Alamos Laboratory (upgraded to DOE OpenNet `hans-bethe.html` verbatim quote).
- **Primary upgrades verified:** Scanned 22-page `LA-602` PDF (`14 Aug 1946`), DOE OpenNet (`trinity.htm`, `trinity_safety.htm`, `edward-teller.html`, `hans-bethe.html`, `enrico-fermi.html`), LANL/OSTI `1836991` (Katz 2021) & `962810` (Teller), NASA Earth Fact Sheet (`78.08% N₂`), NobelPrize.org (Compton, Fermi, Segrè, Bethe), and CrossRef DOIs for Selby et al. 2021 (`10.1080/00295450.2021.1932176`) & Bethe 1976 (`10.1080/00963402.1976.11455623`).

---

## Script & Episode Gate Evidence (`J3507`, `2026-11-24`)

### 1. `npm run review:script` — **PASS (`93.7 / 100`)**
```text
# trinity_test_explained_script_master_v01.md

**Decision:** PASS · **Score:** 93.7 / 100

| Dimension | Score |
|---|---:|
| hook | 9.5 |
| curiosity | 9.5 |
| storytelling | 9.5 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 8.4 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1266 · Est. min: 8.4 · Chapters: 4

- [info] overall: Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- [info] overall: PASS 93.7/100 — proceed to VO after production checklist.
```

### 2. `npm run gate:episode` — **PASS**
```text
# Episode gate — 136_Oppenheimer-Teller-Bethe-Trinity-Test-Explained

**Decision:** PASS — VO / Gemini Veo allowed

| Check | Status | Detail |
|---|---|---|
| project_dir | OK | Project: .../136_Oppenheimer-Teller-Bethe-Trinity-Test-Explained |
| prebuild_vidiq | OK | Pre-build vidIQ audit present and looks signed off. |
| script_file | OK | Script: 01_Script/trinity_test_explained_script_master_v01.md |
| script_review | OK | Script reviewer PASS 93.7/90 (need ≥90). |
| explorer_acts | OK | [EXPLORER ACTS] beats 2 (need ≥1). |
| visual_must | OK | [VISUAL MUST] count 18 (need ≥4). |
| teach | OK | [TEACH] count 5 (need ≥4). |
| chapters | OK | [CHAPTER CARD] count 4 (aim 4–6 film acts). |
| production_checklist | OK | Checklist present: 11_Upload-Package/PRODUCTION_CHECKLIST_V2.md |

Script score: 93.7/100 · PASS
```

### 3. Teach on Screen & Polish Pass Marker Counts (`trinity_test_explained_script_master_v01.md`)
- `CHAPTER CARD:` `4` (Parts 02–05; Part 01 has no chapter card)
- `VISUAL MUST:` `18` · `TEACH:` `5` · `EXPLORER ACTS:` `2` (both outside first minute: Part 02 & Part 04)
- `DATA:` `5` · `SCALE:` `5` (`SCALE ≥ DATA`, incl. 0:27 early nitrogen-air DATA+SCALE and Part 05 1942–1946 timeline)
- `WHO:` `8` (Oppenheimer, Teller, Compton, Bethe, Konopinski, Segrè, Bainbridge, Fermi — all year-accurate 1942–1945 roles)
- `WHEN:` `5` · `FACT:` `4` · `LABEL:` `17`

---

## Topic Gate Evidence (`2026-11-24` · Audited in `J3502`)

### 1. Search-Led Gate (`J3224`, `05_Analytics/hos/search_research/2026-11-20.md`) — **PASS**
- `trinity test`: `21,494`/mo, competition `38`, steady; parent `manhattan project`: `35,203`/mo (**US 18%, GB 9%**); US Education RPM proxy `$3.42` mid (`$2.05–$5.47`); low-RPM trap `nuclear bomb` (`IN 26%, BD 17%`) rejected.
- Signed-out US top-10 gap: **9/10** (`#1` 1:44 movie clip, `#2/#4/#5` raw clips, 7 old, 6 `<50k`).
- Small-channel outliers (`<50k`, `≥5×`): `Unifying Lens` (1.5K US → `1.7K`, `15×`), `Untold WWII` (84 US → `5.8K`, `172×`), Cluster 2 `Science Retold` (3.4K US → `61.9K` `13×` & `28.5K` `6.1×`), `Math Everywhere` (10.3K US → `36.5K` `10×`).

### 2. Neighbour Tie-Breaker (`neighbours.py`, `2026-11-24`) — **PASS**
```text
Words the top neighbours share: nuclear power, nuclear fusion, taylor wilson, the world
TED-Ed/TED neighbour: yes
Big neighbours (≥ 1,000,000 views): 8 (need 3)
Neighbour gate (≥ 3 education videos with 1,000,000+ views): PASS
Raw pull: 02_Video-Projects/136_Oppenheimer-Teller-Bethe-Trinity-Test-Explained/11_Upload-Package/evidence_2026-11-24_neighbours.json
```
Strictly relevant education neighbours verified in saved JSON (`5` strictly relevant `≥1M`, `2` `TED-Ed` ★ `≥1M`): `Veritasium` `19,956,652` (*The Man Who Gave us the Power To Destroy Ourselves (Oppenheimer)*), `TEDx Talks` ★ `9,215,188`, `Kurzgesagt` `8,226,886`, `TED-Ed` ★ `3,332,906` & `2,149,453`.

### 3. Public Search & Collision Check (`public_search.py`, `2026-11-24`, `11` Queries incl. S01 `44c`) — **PASS (`0` Collisions)**
- `4/4` core queries `autocomplete = yes`: `"trinity test"`, `"trinity test explained"`, `"manhattan project"`, `"enrico fermi"`.
- Exact title collisions across Long Titles A (`48c`), B (`68c`), C (`52c`) and Short Titles S01 (`44c` & backup `63c`), S02 (`58c`): **`0`**.
- Raw pulls: `11_Upload-Package/evidence_2026-11-24_public_search.json` and `11_Upload-Package/evidence_2026-11-24_s01_short_search.json`.

## Parts

| Part | Plate board | Latest cut | Status |
|---|---|---|---|
| 01 | `07_Edit-Project/parts/part-01_plates_v01.json` | — | script v01 drafted (`93.7/100` PASS, awaits lock) |
| 02 | | | script v01 drafted |
| 03 | | | script v01 drafted |
| 04 | | | script v01 drafted |
| 05 | | | script v01 drafted |

Keep this file current on `main`. A STOP (quota, auth, missing VO) is a line here, not an open branch.
