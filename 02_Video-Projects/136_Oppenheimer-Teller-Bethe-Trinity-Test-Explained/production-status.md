# Production status — 136 Trinity Test Explained: Could It Ignite the Sky?

| Field | Value |
|---|---|
| Slug | `136_Oppenheimer-Teller-Bethe-Trinity-Test-Explained` |
| Channel | `@HistoryOfScienceYT` only |
| Plan / Cluster | `hos-search-2027-01` Film 2 · Cluster 2 (Nuclear & Modern Physics) |
| Topic | **Rule-E GO (`96.3 / 100` · `9.63 / 10`, `J3502`, `2026-11-24`)** — `10/10` gates PASS |
| Package-first | `11_Upload-Package/PACKAGE_FIRST_SCORING_v01.md` & `LAUNCH_PLAN.md` (`J3507` + `J3675` `ADD-6`, `2026-11-25`): Primary Arm A `Trinity Test Explained: Could It Ignite the Sky?` (`48c`, `96/100`), Thumb A `AIR ON FIRE?` (`96/100`), Thumb B `MEASURED BY PAPER` (`93/100`), S01 `44c` & S02 `58c` (`0` collisions) |
| Pre-build vidIQ audit | `11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md` (updated for `v02` in `J3675`, `2026-11-25`) |
| Script review | **PASS — `93.4 / 100`** (`01_Script/trinity_test_explained_script_master_v02.md` — sole master in `01_Script/`, `1,260` words, `8.4` min, `4` chapter cards, `8/8` structure gates; awaits Chief lock) |
| Episode gate | **PASS** (default `npm run gate:episode` without `--script`, `9/9` checks `OK` — VO/Veo still held pending Chief lock & open WIP slot under Rule G) |
| Sources & Facts | `01_Script/SOURCES.md`, **`01_Script/FACT_NOTES_v02.md`** & **`01_Script/GEMINI_FACTS_CHECK_v02.md`** (`J3676` independent Gemini audit, `2026-11-25`: **0 blocking FLAGs**, `22 OK` / `1 non-blocking PARTIAL R04`; all 8 `J3552` `FLAG`s + `R20` polishes + `ADD-1`–`ADD-6` verified resolved; `LA-602` PDF pp. 1,2,3,10,12,15,16 visually verified; zero unverified new spoken claims; awaits `J3677` Chief lock; `£0.00` spent) |
| Shorts scripts | **`10_Shorts/SHORTS_SCRIPTS_v02.md`** (`J3675`, `2026-11-25`: programmatic counts **`S01 = 42w`** (`16.4–16.8 s` speech) & **`S02 = 42w`** (`16.4–16.8 s` speech), inside `16.0–19.0 s` house rule; `S02` `"in silence for the blast wave"` + `2.5m SHIFT ≈ 10KT` overlay + §2.6 edit ink; titles `S01` `44c` & `S02` `58c` `0` collisions) |
| VO | pending (Ben Orbit Narrator — starts only after script/facts lock & open WIP slot) |
| Picture | pending (Flow Veo 3.1, plate library — starts only after script & VO PASS) |
| Runtime target | 7–9 min, 5 parts (`8.4` min est. at 150 wpm) |
| Ben's watch target | Mon 14 Dec 2026 |
| Air | Thu 17 Dec 2026 18:00 London, normal publish (no Premiere; slides one week if not ready) |

---

## `v02` Corrections & Gate Evidence (`J3675`, `2026-11-25`, `£0.00` Spend)

Resolved all 8 `J3552` blocking `FLAG`s, both `R20` polishes, and all 6 `J3553` editorial items (`ADD-1`–`ADD-6`) on a clean branch off PR `#764` (`4afb106f`):
- **FLAG-1 (`SOURCES.md`, `FACT_NOTES_v02.md` Row 7):** Removed bogus OSTI `4036390` (1964 R. M. Misra paper), WAF-blocked `sgp.fas.org`, and unbacked `OSTI/DOE` on `LA-602` in draft description `Sources:` line; cited verified 22-page Wayback scan of declassified `LA-602` (`14 August 1946`, declassified `2-2-73`) + DOE OpenNet `trinity_safety.htm` + LANL/OSTI `1836991` (Katz 2021).
- **FLAG-2 (Long Part 02 spoken & `SCALE:`):** Removed unsourced `"a thousand times faster"` cooling ratio; aligned with `LA-602`'s safety factor `>1` (`~1.6` minimum worst-case floor, `7.4` with inverse Compton in a 57 m sphere).
- **FLAG-3 (`FACT_NOTES_v02.md` Rows 3, 8, 9):** Row 3 upgraded to NASA Goddard Earth Fact Sheet verbatim quote (`"78.08% Nitrogen (N2), 20.95% Oxygen (O2)"`); Row 8 populated with verbatim `LA-602` PDF pp. 3, 10, 15–16 quotes; Row 9 stripped non-matching Wikipedia `Arthur_Compton`/`Hans_Bethe` links and added NobelPrize.org + CrossRef Bethe June 1976 DOI (`10.1080/00963402.1976.11455623`) + directly opened verbatim quotes from Stanford PH241 (`chung1`), Wikipedia `Manhattan_Project`, and AI Impacts.
- **FLAG-4 (Long Part 04 `VISUAL MUST` `5:10`/`5:26`):** Moved Kenneth Bainbridge's countdown station from `"ten miles away"` to **`S-10000` (South 10,000-yard control bunker, `~5.7 miles / 9.1 km` south of Ground Zero)** per DOE OpenNet `trinity.htm`; kept Base Camp (`~10 miles`) clearly pre-shot before `S-10000` countdown.
- **FLAG-5 (Short `S02`):** Replaced `"for the silent shockwave to arrive"` with `"in silence for the blast wave"`.
- **FLAG-6 (Long Part 03 spoken & `SCALE:`):** Fixed inverted light-speed analogy to verified physics (`c = 299,792,458 m/s ≈ 299.8 m/µs`: `"In one microsecond, light itself travels barely three hundred metres, about three football fields"`).
- **FLAG-7 (Shorts `S01` & `S02` in `10_Shorts/SHORTS_SCRIPTS_v02.md`):** Programmatically trimmed both to **`42` actual whitespace-separated spoken words** (`16.36 s` @ 154 wpm / `16.80 s` @ 150 wpm; `~17.2–17.6 s` with natural pauses, cleanly inside Ben's `16.0–19.0 s` house rule), preserving Frame 0 3D cartoon moving plate, concrete-fact line 1, single Teach overlay (`4.5–8.5 s`), `9–14 s` long title, seamless spoken/visual loop, and `0`-collision titles (`S01` `44c`, `S02` `58c`).
- **FLAG-8 (`FACT_NOTES_v02.md` Row 10):** Replaced spliced Wikipedia `Edward_Teller` quote with primary DOE OpenNet `hans-bethe.html` verbatim quote.
- **`R20` Polishes (Long Part 05):** Unified timeline span to **`1942–1946`** (`four years` July 1942 → August 1946 `LA-602`) and tightened Chicago Pile-1 handoff (`2 Dec 1942 → 16 Jul 1945` = `2 yr 7.5 mo`) to `"Nearly three years"`.
- **ADD-1 (`WHO:` cards):** Resolved Cloyd Marvin cleanly to `"Konopinski, Teller, and a colleague"` in spoken Part 02 (full `E. J. Konopinski, C. Marvin, E. Teller` authorship preserved in `SOURCES.md`/`FACT_NOTES_v02.md`); moved Arthur Compton's `WHO:` card to Part 01 first mention; ensured every named person gets a `WHO:` card at exact first spoken mention (`8/8`).
- **ADD-2 (`WHEN:` stamps):** Added `WHEN: 1959` (Part 02) and `WHEN: Los Alamos, 1943` (Part 03), aligned 1-to-1 with `FACT_NOTES_v02.md` (`7` total `WHEN:` stamps).
- **ADD-3 (One card/label at a time & interleaved `[VISUAL MUST]`):** Split all stacked multi-card `[VISUAL MUST]` blocks across Parts 01–05 and interleaved all `36` `[VISUAL MUST]` cues at their spoken beats (`0` stacked `WHO`/`WHEN`/`FACT`/`LABEL` cards).
- **ADD-4 (Part 01 first-minute milestones — verified programmatically at 150 & 154 wpm):**
  - Title question (L5, `13w`): `0.0–5.2 s` (`150 wpm`) / `0.0–5.1 s` (`154 wpm`) (`<=0:08`)
  - Proof & answer (L9, `+21w → 34w`): finishes **`13.6 s`** (`150 wpm`) / **`13.2 s`** (`154 wpm`) (`<=0:15`)
  - Crisp stakes (L13, `+21w → 55w`): finishes **`22.0 s`** (`150 wpm`) / **`21.4 s`** (`154 wpm`) (`<=0:24`)
  - Early `DATA+SCALE` (L17, `+18w → 73w`): **`22.0–29.2 s`** (`150 wpm`) / **`21.4–28.4 s`** (`154 wpm`) (`0:25–0:35`)
  - Berkeley July 1942 first real fact (L21, `+25w → 98w`): **`29.2–39.2 s`** (`150 wpm`) / **`28.4–38.2 s`** (`154 wpm`) (`<0:45`)
- **ADD-5 (`S02` overlay & §2.6):** Tightened `S02` overlay to `2.5m SHIFT ≈ 10KT` (`4` tokens `≤4` words) and marked `10,000 TONS TNT` cream-pad note as hand-verified edit ink (§2.6).
- **ADD-6 (Single master filename & `LAUNCH_PLAN.md`):** Removed `trinity_test_explained_script_master_v01.md` so only `trinity_test_explained_script_master_v02.md` sits in `01_Script/`; updated `LAUNCH_PLAN.md` so archive-image credit & production lines match final archive count at package lock.

### Exact `v02` Artifact SHA-256 Hashes
```text
85fb1286610264f5692a1e1dfe766fc0dfb90231016fd27f012dc079499047b2  02_Video-Projects/136_Oppenheimer-Teller-Bethe-Trinity-Test-Explained/01_Script/trinity_test_explained_script_master_v02.md
060acf45825759934812f8a12833f298c2d5de68a236e9a237d215961a69311a  02_Video-Projects/136_Oppenheimer-Teller-Bethe-Trinity-Test-Explained/01_Script/SOURCES.md
899156a368a5f22e554b3d267f073e3c69ff7eded609e2aa07f5db2e5c8126a6  02_Video-Projects/136_Oppenheimer-Teller-Bethe-Trinity-Test-Explained/01_Script/FACT_NOTES_v02.md
e1df5d81baffca83c559b78a2a87df97df0fe8be15fb8de96a761445906941fe  02_Video-Projects/136_Oppenheimer-Teller-Bethe-Trinity-Test-Explained/10_Shorts/SHORTS_SCRIPTS_v02.md
```

### 1. `npm run review:script` (`v02`) — **PASS (`93.4 / 100`)**
```text
# trinity_test_explained_script_master_v02.md

**Decision:** PASS · **Score:** 93.4 / 100

| Dimension | Score |
|---|---:|
| hook | 9.5 |
| curiosity | 9.5 |
| storytelling | 9.5 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 8.1 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1260 · Est. min: 8.4 · Chapters: 4

- [info] overall: Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- [info] overall: PASS 93.4/100 — proceed to VO after production checklist.
```

### 2. `npm run gate:episode` (default, no `--script`) — **PASS (`9/9` OK)**
```text
# Episode gate — 136_Oppenheimer-Teller-Bethe-Trinity-Test-Explained

**Decision:** PASS — VO / Gemini Veo allowed

| Check | Status | Detail |
|---|---|---|
| project_dir | OK | Project: /Users/ben/_desk/worker/slot2/history-of-science/02_Video-Projects/136_Oppenheimer-Teller-Bethe-Trinity-Test-Explained |
| prebuild_vidiq | OK | Pre-build vidIQ audit present and looks signed off. |
| script_file | OK | Script: 01_Script/trinity_test_explained_script_master_v02.md |
| script_review | OK | Script reviewer PASS 93.4/90 (need ≥90). |
| explorer_acts | OK | [EXPLORER ACTS] beats 2 (need ≥1). |
| visual_must | OK | [VISUAL MUST] count 36 (need ≥4). |
| teach | OK | [TEACH] count 5 (need ≥4). |
| chapters | OK | [CHAPTER CARD] count 4 (aim 4–6 film acts). |
| production_checklist | OK | Checklist present: 11_Upload-Package/PRODUCTION_CHECKLIST_V2.md |

Script score: 93.4/100 · PASS
```

### 3. `00_Brand/Channel-Setup/tools/check_all.sh 02_Video-Projects/136_Oppenheimer-Teller-Bethe-Trinity-Test-Explained` — **ALL CHECKS PASS**
```text
-- durable desk handoffs: PASS
-- email ratchet: PASS
-- no media: PASS
-- status board in sync: PASS (34 status files and BOARD.json are in order)
-- ElevenLabs guard tests: PASS
-- vo_check word tests: PASS
-- atempo check tests: PASS
-- voice speed (atempo <= 1.06): PASS
-- contract tests: PASS
-- package-lint: PASS
-- review:script trinity_test_explained_script_master_v02.md: PASS (93.4 / 100, 8/8 structure gates)
-- gate:episode: PASS (9/9 checks OK)

ALL CHECKS PASS
```

### 4. Teach on Screen & Polish Pass Marker Counts (`trinity_test_explained_script_master_v02.md`)
- `CHAPTER CARD:` `4` (Parts 02–05; Part 01 has no chapter card)
- `VISUAL MUST:` `36` (interleaved, `0` stacked cards) · `TEACH:` `5` · `EXPLORER ACTS:` `2` (both outside first minute: Part 02 & Part 04)
- `DATA:` `5` · `SCALE:` `5` (`SCALE ≥ DATA`, incl. 0:23–0:29 early nitrogen-air DATA+SCALE and Part 05 unified `1942–1946` timeline)
- `WHO:` `8` (Oppenheimer, Teller, Compton [Part 01], Bethe, Konopinski, Segrè, Bainbridge, Fermi — all at exact first spoken mention with primary-verified lifespans & year-accurate 1942–1945 roles)
- `WHEN:` `7` (`Berkeley, July 1942`, `1942–1943`, `1959`, `August 1946`, `Los Alamos, 1943`, `Los Alamos, April 1944`, `New Mexico, 16 July 1945`)
- `FACT:` `4` · `LABEL:` `16` (all `≤4` words)

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
| 01 | `07_Edit-Project/parts/part-01_plates_v01.json` | — | script v02 PASS (`93.4/100`, awaits Chief lock) |
| 02 | | | script v02 PASS |
| 03 | | | script v02 PASS |
| 04 | | | script v02 PASS |
| 05 | | | script v02 PASS |

Keep this file current on `main`. A STOP (quota, auth, missing VO) is a line here, not an open branch.
