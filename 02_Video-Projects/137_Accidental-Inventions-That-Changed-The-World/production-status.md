# Production status — 137 Accidental Inventions: 5 Mistakes That Worked

| Field | Value |
|---|---|
| Slug | `137_Accidental-Inventions-That-Changed-The-World` |
| Channel | `@HistoryOfScienceYT` only |
| Plan / Cluster | `hos-search-2027-01` Film 3 · Cluster 3 (Accidental & World-Changing Inventions) |
| Topic | **Rule-E GO (`95.8 / 100` · `9.58 / 10`, `J3503`, `2026-11-24`)** — `10/10` gates PASS; Safety Glass (1903) locked over Microwave (zero overlap with `HOS:129`) |
| Package-first | `11_Upload-Package/PACKAGE_FIRST_SCORING_v01.md` & `LAUNCH_PLAN.md` (`J3513`, `2026-11-24`): Primary Arm A `Accidental Inventions: 5 Mistakes That Worked` (`45c`, `96/100`), Thumb A `NEARLY TRASHED` (`96/100`), Thumb B `WRONG RESISTOR` (`93/100`), S01 `48c` & S02 `54c` (`0` collisions) |
| Pre-build vidIQ audit | `11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md` (updated & signed off for v01 draft in `J3513`, `2026-11-24`) |
| Script review | **PASS — `92.6 / 100`** (`01_Script/accidental_inventions_script_master_v01.md`, `1,225` words, `8.2` min, `4` chapter cards, `8/8` structure gates; awaits independent `facts` lane + Chief lock) |
| Episode gate | **PASS** (all checks `OK` — VO/Veo still held pending independent `facts` lane, Chief lock & open WIP slot under Rule G) |
| Sources & Facts | `01_Script/SOURCES.md` & `01_Script/FACT_NOTES_v01.md` (`24/24` rows verified with verbatim primary/institutional quotes & open URLs; all 6 `J3503` guardrails resolved; queued for independent `facts` lane `gemini-agy`) |
| Shorts scripts | `10_Shorts/SHORTS_SCRIPTS_v01.md` (`S01` `46w` Sat 26 Dec & `S02` `43w` Fri 25 Dec, 16–19 s Ben 19 Nov house rules; awaits Chief lock) |
| VO | pending (Ben Orbit Narrator — starts only after script/facts lock & open WIP slot) |
| Picture | pending (Flow Veo 3.1, plate library — starts only after script & VO PASS; Flow renews 12 Dec) |
| Runtime target | 7–9 min, 5 parts (`8.2` min est. at 150 wpm) |
| Ben's watch target | Mon 21 Dec 2026 |
| Air | Thu 24 Dec 2026 18:00 London, normal publish (no Premiere; slides one week if not ready) |
| Shorts | 16–19 s search-question Shorts (Fri 25 Dec & Sat 26 Dec promote this long, `0` collisions verified in `J3503`; Sun & Tue cluster/candidate rotation), Related → this long |

## Script & Episode Gate Evidence (`2026-11-24` · `J3513`)

### 1. `npm run review:script` — **PASS (`92.6 / 100`)**
```text
# accidental_inventions_script_master_v01.md

Decision: PASS · Score: 92.6 / 100
hook: 9.5 | curiosity: 8.7 | storytelling: 9.5 | scientificAccuracy: 10 | emotion: 9.6
escalation: 8.1 | retentionPotential: 9 | searchPotential: 9.1 | visualOpportunities: 9.5 | narrationFlow: 9.6
Words: 1225 · Est. min: 8.2 · Chapters: 4
Findings:
- [info] overall: Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- [info] overall: PASS 92.6/100 — proceed to VO after production checklist.
Pass threshold: 90
```

### 2. `npm run gate:episode` — **PASS**
```text
# Episode gate — 137_Accidental-Inventions-That-Changed-The-World
Decision: PASS — VO / Gemini Veo allowed (production still held pending independent facts lane, Chief lock & open WIP slot under Rule G)
project_dir: OK | prebuild_vidiq: OK | script_file: OK | script_review: OK (92.6/90)
explorer_acts: OK (2) | visual_must: OK (19) | teach: OK (5) | chapters: OK (4) | production_checklist: OK
```

### 3. Teach on Screen & Polish Pass Marker Counts (`accidental_inventions_script_master_v01.md`)
- `CHAPTER CARD:` `4` (Parts 02–05; Part 01 has no chapter card)
- `VISUAL MUST:` `19` · `TEACH:` `5` · `EXPLORER ACTS:` `2` (both outside first minute: Part 02 & Part 05)
- `DATA:` `5` · `SCALE:` `5` (`SCALE ≥ DATA`, incl. 0:28 early `10 kΩ → 1 MΩ` / `1.8 ms` resistor DATA+SCALE, Goodyear cure, Penicillin 12-year gap, Boise `>90%` curve, and Part 05 `1839–1974` timeline)
- `WHO:` `13` (Greatbatch, Chardack, Gage, Elmqvist, Senning, Goodyear, Bénédictus, Fleming, Florey, Chain, Heatley, Silver, Fry — every named person with year-accurate role)
- `WHEN:` `10` · `FACT:` `4` · `LABEL:` `18`

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
| 01 | `07_Edit-Project/parts/part-01_plates_v01.json` | — | script v01 drafted (`92.6/100` PASS, awaits lock) |
| 02 | | | script v01 drafted |
| 03 | | | script v01 drafted |
| 04 | | | script v01 drafted |
| 05 | | | script v01 drafted |

Keep this file current on `main`. A STOP (quota, auth, missing VO) is a line here, not an open branch.
