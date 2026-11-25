# Production status — 131 What Is the Theory of Relativity? (1919 Eclipse)

| Field | Value |
|---|---|
| Slug | `131_Einstein-Eddington-What-Is-The-Theory-Of-Relativity` |
| Channel | `@HistoryOfScienceYT` only |
| Topic | **Rule-E GO (`96.5 / 100` · `9.65 / 10` Opportunity Score, `J3351`, 2026-11-22)** — pre-cleared in `jobs/WIP.json` `next_hos` under **Rule G** (`4 / 4` active HOS slots full: `008`, `009`, `010`, `013`). See [`11_Upload-Package/TOPIC_GO_NO_GO_SHEET.md`](11_Upload-Package/TOPIC_GO_NO_GO_SHEET.md) and [`11_Upload-Package/TOPIC_OPPORTUNITY_SCORE.md`](11_Upload-Package/TOPIC_OPPORTUNITY_SCORE.md). |
| Neighbour gate | **PASS** (`7` raw / `5` strictly on-topic education videos `≥1M`, `TED-Ed/TED: yes`; `2` raw rows transparently excluded as logic puzzle / quantum entanglement) — `11_Upload-Package/evidence_2026-11-22_neighbours.json` |
| Public search check | **PASS** (`11` queries / `77` rows, `autocomplete = yes` on 3 core phrases + related `1919 solar eclipse einstein`, `0` exact and `0` near-exact title collisions across Titles A/B/C and Shorts S01/S02 after `J3351` replaced S02) — `11_Upload-Package/evidence_2026-11-22_public_search.json` |
| Pre-build vidIQ audit | Draft scaffolded & Rule-E verified (`11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md`, £0 spend; live per-title vidIQ scores pending WIP slot; all historical/scientific claims **UNVERIFIED**) |
| Script review | — / 90 (not started — waits on open HOS WIP slot under Rule G, `SOURCES.md` verbatim quotes, and `facts` lane) |
| Episode gate | not run |
| VO | pending (Ben Orbit Narrator — zero spend) |
| Picture | pending (Flow Veo 3.1, plate library — zero spend) |
| Runtime target | 7–9 min, 5 parts |
| Air | Proposal in `next_hos` — Thursday 18:00 UK, normal publish (no Premiere) |
| Shorts | 2 search-titled `16–19 s` Shorts planned (`Ben 19 Nov 2026` house rules: `S01` *How Did the 1919 Solar Eclipse Prove Einstein's Relativity?* `59c`, `S02` *How Does Einstein's Relativity Keep GPS Accurate?* `49c`), Related → this long |

## Topic Gate Evidence (`2026-11-22`, `J3348` + `J3351`)

### 1. Neighbour Gate (`neighbours.py "theory of relativity" "einstein relativity"`) — **PASS (`7` Raw / `5` Strictly On-Topic Education Videos `≥1M` Views, `TED-Ed/TED: yes`)**

| # | Views (`2026-11-22`) | Channel | Video ID | Title | Relevance |
|---:|---:|---|---|---|---|
| 1 | `8,545,878` | Veritasium | [`eyZEqSPeMwg`](https://youtu.be/eyZEqSPeMwg) | *Relativity is so much weirder than we thought...* | Strictly on-topic |
| 2 | `5,919,102` | TED-Ed ★ | [`h8GqaAp3cGs`](https://youtu.be/h8GqaAp3cGs) | *Einstein's twin paradox explained - Amber Stuver* | Strictly on-topic |
| 3 | `2,733,278` | TED-Ed ★ | [`91XI7M9l3no`](https://youtu.be/91XI7M9l3no) | *Einstein's miracle year - Larry Lagerstrom* | Strictly on-topic |
| 4 | `1,855,197` | minutephysics | [`eNhJY-R3Gwg`](https://youtu.be/eNhJY-R3Gwg) | *General Relativity Explained in 7 Levels of Difficulty* | Strictly on-topic |
| 5 | `1,449,325` | CrashCourse | [`AInCqm5nCzw`](https://youtu.be/AInCqm5nCzw) | *Special Relativity: Crash Course Physics #42* | Strictly on-topic |
| 6 | `423,973` | TED-Ed ★ | [`gkTVlYDB21g`](https://youtu.be/gkTVlYDB21g) | *The physics behind Einstein's most famous equation* | On-topic `<1M` |
| 7 | `363,369` | Khan Academy | [`HIQ5hnm61LQ`](https://youtu.be/HIQ5hnm61LQ) | *Introduction to the Lorentz transformation \| Special relativity* | On-topic `<1M` |
| 8 | `310,265` | Khan Academy | [`3G_Q6AggQF8`](https://youtu.be/3G_Q6AggQF8) | *Michelson–Morley Experiment introduction \| Special relativity* | On-topic `<1M` |

*(Transparently excluded from the `7` raw `≥1M` count: `TED-Ed` `1rDVz_Fb6HQ` `13,415,539` "Einstein's Riddle" logic puzzle and `TED-Ed` `DbbWx2COU0E` `1,291,010` quantum entanglement.)*

```text
neighbours.py "theory of relativity" "einstein relativity"
Words the top neighbours share: einstein s
TED-Ed/TED neighbour: yes
Big neighbours (≥ 1,000,000 views): 7 (need 3; 5 strictly on-topic relativity)
Neighbour gate (≥ 3 education videos with 1,000,000+ views): PASS
Raw pull: 02_Video-Projects/131_Einstein-Eddington-What-Is-The-Theory-Of-Relativity/11_Upload-Package/evidence_2026-11-22_neighbours.json
```

### 2. Public Search & Autocomplete Gate (`public_search.py`, `11` Queries / `77` Rows) — **PASS (`0` Collisions)**

- `"what is the theory of relativity"` → **`autocomplete = yes`** (`10` suggestions; `Science ABC` `yuD34tEpRFw` `9,685,020`; `Arvin Ash` `tzQC3uYL67U` `7,384,849`; `SpaceRip` `g8ZO5XvHORI` `1,881,348`; `BBC News` `B6kreUskcpo` `822,972`)
- `"theory of relativity explained"` → **`autocomplete = yes`** (`10` suggestions)
- `"how did einstein prove relativity"` → **`autocomplete = yes`** (`1` suggestion; `Science ABC` `9,685,020`; `Arvin Ash` `7,384,849`; `minutephysics` `hW7DW9NIO9M` `6,268,836`; `StarTalk` `1BCkSYQ0NRQ` `3,512,623`; `minutephysics` `eNhJY-R3Gwg` `1,855,197`; `Beeyond Ideas` `-2X8alKLJq0` `1,647,646`)
- `"einstein 1919 solar eclipse"` → related (`1919 solar eclipse einstein`; `Vox` `HLxvq_M4218` `2,196,555`; `Seeker` `qgc9bDH4b-0` `263,635`; `OpenMind` `97Y5Oqzuqv8` `115,201`)
- `"why does gps need relativity"` → `minutephysics` `ky4RgRvVDoA` `998,921`; `FlightInsight` `C6012z6NmUU` `51,459`
- **Title collisions (`J3351` audited):** `0` exact and `0` near-exact collisions across Titles A (`48c`), B (`58c`), C (`63c`), Short S01 (`59c`), and replacement Short S02 (*How Does Einstein's Relativity Keep GPS Accurate?*, `49c`, replacing original S02 which near-collided with `tU2gJpkmEgs`).

## Parts

| Part | Plate board | Latest cut | Status |
|---|---|---|---|
| 01 | `07_Edit-Project/parts/part-01_plates_v01.json` | — | todo |
| 02 | | | todo |
| 03 | | | todo |
| 04 | | | todo |
| 05 | | | todo |

Keep this file current on `main`. A STOP (quota, auth, missing VO) is a line here, not an open branch.
