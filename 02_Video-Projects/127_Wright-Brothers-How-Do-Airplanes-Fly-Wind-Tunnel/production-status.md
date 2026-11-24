# Production status — 127 How Do Airplanes Fly? (The 1901 Wind Tunnel)

| Field | Value |
|---|---|
| Slug | `127_Wright-Brothers-How-Do-Airplanes-Fly-Wind-Tunnel` |
| Channel | `@HistoryOfScienceYT` only |
| Topic | **Rule-E GO (`97.2 / 100`, `J3264`, `2026-11-21`)** — pre-cleared in `jobs/WIP.json` `next_hos` under **Rule G** (waits for an active HOS WIP slot; all `4 / 4` active HOS slots full: `008`, `009`, `010`, `013`). Directly implements **Cluster 4 Lead Film (Thu 28 Jan 2027)** of Ben's approved `hos-search-2027-01` plan (`J3224`, locked `2026-11-20` in `orbit-with-ben` `2803f878c`). |
| Working Title (A) | *How Do Airplanes Fly? (The 1901 Wind Tunnel)* (`44 chars ≤ 50`, `0` exact collisions; `Rules 1, 15, 23, 26`) |
| Title B (T&C) | *Wright Brothers First Flight: The 1901 Wind Tunnel* (`50 chars ≤ 50`, `0` exact collisions; exact `J3224` Lead Film 4 query `"wright brothers first flight"`) |
| Title C (Backup) | *How Did the Wright Brothers Solve Flight? (1901)* (`48 chars ≤ 50`, `0` exact collisions; `Rules 1, 15, 23`) |
| Neighbour gate | **PASS (`2026-11-21`)** — `8` raw / `6` aviation / **`5` strictly on-topic** education videos `≥1M` views (`TED-Ed/TED: yes`, led by `TED-Ed` ★ `2.57M` `p4VHMsIuPmk`, `minutephysics` `2.48M` `Gg0TXNXgz-w`, `SciShow Kids` `1.75M` `VLpSxHwfU04`, `Veritasium` `1.66M` `aFO4PBolwFg`, `Simple History` `1.41M` `YDlk4Ky_ahs`, plus broader aviation `TED-Ed` ★ `2.52M` `hd8tYiLSmn0`, `Real Engineering` `384,056` `WCPapu78SNM`, and `SciShow` `293,525` `9S7H8TlkBC4`) |
| Public search & collisions | **PASS (`2026-11-21`)** — `11_Upload-Package/evidence_2026-11-21_public_search.json` (`9` queries, `64` search rows; `"how do airplanes fly"` `10`, `"wright brothers first flight"` `10`, `"wright brothers wind tunnel"` `1`, `"how does an airplane wing work"` `3` autocomplete `yes`; `9` distinct `≥1M` strictly on-topic videos across `neighbours.json` + `public_search.json`; `0` exact title collisions across Titles A/B/C and Shorts S01/S02) |
| Pre-build vidIQ audit | `11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md` completed (`J3224` vidIQ demand + signed-out `public_search.py` & `neighbours.py`; per-title vidIQ login scores pending active WIP) |
| Facts / `SOURCES.md` | **NOT STARTED — ALL CLAIMS UNVERIFIED** (primary sources identified as sourceable; verbatim quotes + `facts` lane verification required before any script lock, VO, or picture spend) |
| Script review | pending (`— / 90`; template `01_Script/episode_script_draft_v01.md` untouched) |
| Episode gate | not run |
| VO | pending (Ben Orbit Narrator; `£0.00` spent) |
| Picture | pending (Flow Veo 3.1, plate library; `£0.00` spent) |
| Runtime target | 7–9 min, 5 parts |
| Air | Unscheduled (`next_hos` backlog; target Thu 28 Jan 2027 Cluster 4 Lead Film once active — Thu 18:00 UK normal publish, no Premiere) |
| Shorts | 2 search-titled Shorts (`16–19 s` under 19 Nov 2026 Shorts house rules): S01 *Why Did the Wright Brothers Build a Wind Tunnel?* (`48c`, `0` collisions), S02 *How Did the Wright Brothers Steer the First Plane?* (`50c`, `0` collisions) — unverified concepts only |

## Rule-E Audit Evidence (`J3264`, `2026-11-21`)

- `neighbours.py` output (`11_Upload-Package/evidence_2026-11-21_neighbours.json`):
  ```text
  Words the top neighbours share: wright brothers, how do, do airplanes, airplanes fly, the wright
  TED-Ed/TED neighbour: yes
  Big neighbours (≥ 1,000,000 views): 8 (need 3)
  Neighbour gate (≥ 3 education videos with 1,000,000+ views): PASS
  Raw pull: 02_Video-Projects/127_Wright-Brothers-How-Do-Airplanes-Fly-Wind-Tunnel/11_Upload-Package/evidence_2026-11-21_neighbours.json
  ```
  *(Transparent filter: excluding `2` airplane-keyword false positives `dzrwnwOx0fw` riddle `7.65M` & `iKYHf22qVdM` airplane mode `4.21M`, and noting broader aviation `hd8tYiLSmn0` `2.52M`, leaves **`5` strictly on-topic `≥1M` education videos**, with `TED-Ed` ★ `#1` at `2,568,211` views.)*
- `public_search.py` output (`11_Upload-Package/evidence_2026-11-21_public_search.json`): `9` queries, `64` search rows, `4/4` core search phrases autocomplete `yes`, `0` exact title collisions across all 5 candidate titles.
- Script-stage guardrails recorded in [`TOPIC.md`](TOPIC.md) §4.5 & [`11_Upload-Package/TOPIC_GO_NO_GO_SHEET.md`](11_Upload-Package/TOPIC_GO_NO_GO_SHEET.md):
  1. Fix Smeaton coefficient percentage contradiction (`0.005` is ~50% higher than `0.0033`, not 40% — Thumb C updated to `50% TOO HIGH`, verify exact values in `SOURCES.md`).
  2. Never use the debunked "equal transit time" lift myth; explain lift via pressure difference + downward airflow deflection and empirical wind-tunnel lift-to-drag measurements.
  3. Expand the 4-act sketch into HOS's standard 5-part (`7–9 min`) structure.
  4. Distinguish **Kill Devil Hills** (flight site) from **Kitty Hawk** (post office/telegraph), lock one verbatim despair quote in `SOURCES.md`, and keep every `WHO` card role accurate for 1901–1903.
  5. Test Title A (`44c`, `"how do airplanes fly"`) vs Title B (`50c`, `"wright brothers first flight"`, `J3224` Lead Film 4 exact query) in the active-WIP packaging panel and YouTube Test & Compare.

## Parts

| Part | Plate board | Latest cut | Status |
|---|---|---|---|
| 01 | `07_Edit-Project/parts/part-01_plates_v01.json` (template) | — | todo |
| 02 | — | — | todo |
| 03 | — | — | todo |
| 04 | — | — | todo |
| 05 | — | — | todo |

Keep this file current on `main`. A STOP (quota, auth, missing VO) is a line here, not an open branch.
