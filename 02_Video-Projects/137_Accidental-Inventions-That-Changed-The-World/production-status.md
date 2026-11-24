# Production status — 137 Accidental Inventions: 5 Mistakes That Worked

| Field | Value |
|---|---|
| Slug | `137_Accidental-Inventions-That-Changed-The-World` |
| Channel | `@HistoryOfScienceYT` only |
| Plan / Cluster | `hos-search-2027-01` Film 3 · Cluster 3 (Accidental & World-Changing Inventions) |
| Topic | **GO (`95.8 / 100` · `9.58 / 10`, `J3503`, `2026-11-24`)** — `10 / 10` Rule-E & Rule-42 gates PASS after `J3503` fixes; Safety Glass (1903) locked over Microwave (zero overlap with `HOS:129`); script job **`J3513`** queued |
| Pre-build vidIQ audit | `11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md` · `TOPIC_GO_NO_GO_SHEET.md` · `TOPIC_OPPORTUNITY_SCORE.md` |
| Script review | — / 90 (`J3513` draft due Mon 30 Nov 18:00 London, lock Tue 8 Dec) |
| Episode gate | not run |
| VO | pending (Ben Orbit Narrator — starts only after script/facts lock & open WIP slot) |
| Picture | pending (Flow Veo 3.1, plate library — starts only after script & VO PASS; Flow renews 12 Dec) |
| Runtime target | 7–9 min, 5 parts |
| Ben's watch target | Mon 21 Dec 2026 |
| Air | Thu 24 Dec 2026 18:00 London, normal publish (no Premiere; slides one week if not ready) |
| Shorts | 16–19 s search-question Shorts (Fri & Sat promote this long, `0` collisions verified in `J3503`; Sun & Tue cluster/candidate rotation), Related → this long |

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
| 01 | `07_Edit-Project/parts/part-01_plates_v01.json` | — | — |
| 02 | | | |
| 03 | | | |
| 04 | | | |
| 05 | | | |

Keep this file current on `main`. A STOP (quota, auth, missing VO) is a line here, not an open branch.
