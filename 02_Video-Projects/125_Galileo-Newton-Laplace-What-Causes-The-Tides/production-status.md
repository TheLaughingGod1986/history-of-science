# Production status — 125 What Causes the Tides? (Galileo Got It Wrong)

| Field | Value |
|---|---|
| Slug | `125_Galileo-Newton-Laplace-What-Causes-The-Tides` |
| Channel | `@HistoryOfScienceYT` only |
| Topic | **Rule-E GO (`95.9 / 100`, `J3214`, 20 Nov 2026)** — pre-cleared in `jobs/WIP.json` `next_hos` under Rule G (waits for an active HOS WIP slot; all 4/4 active HOS slots full) |
| Neighbour gate | **PASS** (`2026-11-20`, `neighbours.py`: `6` education `≥1M` [`4` strictly on tides], `hasTed = true`, `TED-Ed` on-topic `605k`) |
| Public search & collisions | **PASS** (`2026-11-20`, `public_search.py`: `10` queries, `80` results; `0` exact title collisions across Titles A/B/C and disambiguated Shorts S01/S02) |
| Pre-build vidIQ audit | `11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md` drafted from `public_search.py` (vidIQ login scores pending when entering active WIP) |
| Facts / `SOURCES.md` | **NOT STARTED — ALL CLAIMS UNVERIFIED** (primary sources identified as sourceable; verbatim quotes + `facts` lane verification required before script lock) |
| Script review | pending (`— / 90`; template `01_Script/episode_script_draft_v01.md` untouched) |
| Episode gate | not run |
| VO | pending (Ben Orbit Narrator; `£0.00` spent) |
| Picture | pending (Flow Veo 3.1, plate library; `£0.00` spent) |
| Runtime target | 8.5–9 min, 5 parts |
| Air | Unscheduled (`next_hos` backlog; Thu 18:00 UK normal publish, no Premiere once active) |
| Shorts | 2 search-titled Shorts (`16–19 s` under 19 Nov 2026 Shorts house rules): S01 *Why Does the Moon Make Two Tides a Day?* (`39c`), S02 *What Did Galileo Get Wrong About the Tides?* (`43c`) |

## Rule-E Audit Evidence (`J3214`, 20 Nov 2026)

- `neighbours.py` output (`11_Upload-Package/evidence_2026-11-20_neighbours.json`):
  - `TED-Ed/TED neighbour: yes`
  - `Big neighbours (≥ 1,000,000 views): 6 (need 3)` (`4` strictly on tides: PBS Space Time `2.13M`, CrashCourse `2.01M`, minutephysics `1.79M`, minutephysics `1.05M`; plus `TED-Ed` `mpRJhhbKLFc` `605k` on tides)
  - `Neighbour gate (≥ 3 education videos with 1,000,000+ views): PASS`
- `public_search.py` output (`11_Upload-Package/evidence_2026-11-20_public_search.json`): `10` queries, `80` results, `4/4` core search phrases autocomplete `yes`, `0` exact title collisions on approved titles.
- Script-stage guardrails recorded in `TOPIC.md` §2.5 & `11_Upload-Package/TOPIC_GO_NO_GO_SHEET.md`:
  1. Never claim tides occur "twice a day, everywhere" (diurnal coasts exist).
  2. Explain Newton's tidal force via differential horizontal (tractive) convergence rather than vertical lifting or centrifugal fling, then pivot to Laplace's forced ocean-basin wave equations.
  3. Label William Thomson as **Sir William Thomson** in 1872 scenes (Baron Kelvin title dates from 1892).
  4. Keep Short S01 disambiguated as *Why Does the Moon Make Two Tides a Day?* (avoiding collision with TED-Ed `mpRJhhbKLFc`).

## Parts

| Part | Plate board | Latest cut | Status |
|---|---|---|---|
| 01 | `07_Edit-Project/parts/part-01_plates_v01.json` (template) | — | todo |
| 02 | — | — | todo |
| 03 | — | — | todo |
| 04 | — | — | todo |
| 05 | — | — | todo |

Keep this file current on `main`. A STOP (quota, auth, missing VO) is a line here, not an open branch.
