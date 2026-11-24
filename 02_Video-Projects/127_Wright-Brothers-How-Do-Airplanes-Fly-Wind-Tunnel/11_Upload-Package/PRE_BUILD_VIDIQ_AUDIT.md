# Pre-Build vidIQ & Public-Search Audit — `HOS:127` (`Wright Brothers First Flight: The 1901 Wind Tunnel`)

**Hard gate:** Run **before** locking script, VO, prompts, or picture gen for any new long.  
**Status (`J3504`, `2026-11-24`):** Rule-E topic go/no-go review **GO (`97.2 / 100` · `9.72 / 10`, `J3264`, `2026-11-21`)**; accelerated into the December `hos-search-2027-01` 4-film test cohort as **Cluster 4 Lead Film 4 (target Thu 31 Dec 2026, 18:00 London)** (`J3495` / PR `#1239`). Package-first scoring (`PACKAGE_FIRST_SCORING_v01.md`), `wright_brothers_wind_tunnel_script_master_v01.md`, `SOURCES.md`, `FACT_NOTES_v01.md`, `SHORTS_SCRIPTS_v01.md`, and `LAUNCH_PLAN.md` drafted in `J3504` (`£0.00`). Per-title vidIQ app numeric scores remain pending when `HOS:127` enters active WIP under Rule G. **Awaits independent `facts` lane (`gemini-agy`) audit and Chief script/package lock before any VO or picture spend.**

---

## Episode

| Field | Value |
|-------|-------|
| ID / slug | `127_Wright-Brothers-How-Do-Airplanes-Fly-Wind-Tunnel` |
| Working title | `Wright Brothers First Flight: The 1901 Wind Tunnel` (`50` chars, Arm A) · T&C Arm B: `Wright Brothers First Flight: The 1901 Wind Tunnel That Solved Lift` (`67` chars) · T&C Arm C: `How Do Airplanes Fly? (The 1901 Wind Tunnel)` (`44` chars) |
| Date pulled | `2026-11-21` (`J3245` / `J3264`) + `2026-11-24` (`J3504` plan-title collision check; `J3224` vidIQ `2026-11-20`) |
| Credits used (approx) | `0` (`£0.00` in `J3245`, `J3264`, and `J3504`) |
| 2027 Search Plan slot | Cluster 4 Lead Film 4 (accelerated target **Thu 31 Dec 2026, 18:00 London**; Ben's watch Mon 28 Dec) — *Breakthrough & Lost Engineering* (`hos-search-2027-01`) |
| Brand guardrails | Wonder over fearbait · primary NASA/Smithsonian/NPS aerodynamics & archival history · HOS lane (a familiar thing, and the moment we found out) |

---

## 1. Success Targets (This Episode)

| Metric | Target |
|--------|--------|
| Title score | ≥ **90** (aim **95+**; per-title vidIQ login score pending active WIP) |
| Primary keyword overall | `how do airplanes fly` (`10` GB autocomplete suggestions) + `wright brothers first flight` (`19,018`/mo, comp `45`, `10/10` US SERP gap, `10` GB autocomplete suggestions; `9` distinct `≥1M` on-topic videos across `neighbours.json` + `public_search.json`) |
| Hook promise | How two bicycle mechanics proved a 142-year-old flight equation wrong inside a 6-foot homemade wind tunnel — and cracked lift and three-axis control before 1903 |
| Retention design | 5 cause-and-effect parts (`1901 glider failure & despair` → `bike-wheel test & wooden wind tunnel` → `Smeaton's 0.005 error & 200 tiny wings` → `1902 adverse yaw & wing-warping/rudder twist` → `propellers, Charlie Taylor engine & 17 Dec 1903 flights`) |
| Packaging | Thumb readable at `168×94`; clear left-band cream/gold serif lettering (`200 TINY WINGS` / `THE TABLES LIED` / `50% TOO HIGH`), warm 3D period palette, Explorer small lower-left |

---

## 2. Keyword Research (`J3224` vidIQ `2026-11-20` + Signed-Out GB `public_search.py` / `neighbours.py` `2026-11-21`)

| Keyword | Monthly Vol / Comp (`J3224`) | Autocomplete (GB `11-21`) | Top Competitors | Role (title / desc / tags / Shorts) | Keep? |
|---------|------------------------------|---------------------------|-----------------|-------------------------------------|-------|
| `how do airplanes fly` | Evergreen high demand | **yes** (`10` suggestions) | `TED-Ed` `2.57M`, `minutephysics` `2.48M`, `SciShow Kids` `1.75M` | **primary** (Title A + desc line 1 + tags) | **Keep** |
| `wright brothers first flight` | `19,018`/mo · comp `45` · `10/10` US gap | **yes** (`10` suggestions) | `Sabin Civil Eng.` `4.46M`, `Naked Science` `1.58M`, `Simple History` `1.41M` | **primary / T&C Arm 2** (Title B + desc + tags) | **Keep** |
| `wright brothers wind tunnel` | Specific apparatus query | **yes** (`1` exact suggestion) | `Sabin Civil Eng.` `4.46M`, `MIT` `12.9k` | **secondary / Short S01** (desc + tags) | **Keep** |
| `how does an airplane wing work` | Evergreen physics query | **yes** (`3` suggestions) | `The Efficient Engineer` `2.11M`, `Math & Science` `2.04M`, `Veritasium` `1.66M` | **secondary** (desc + tags) | **Keep** |
| `aviation history` | `54,239`/mo · PK 35%, VN 12% | — | Non-Anglosphere top 3 | **Rejected in `J3224`** — do NOT use in title or tags | **Reject** |

**Decision:** Primary title lead = `How Do Airplanes Fly? (The 1901 Wind Tunnel)` (Title A, `44c`) with `Wright Brothers First Flight: The 1901 Wind Tunnel` (Title B, `50c`) as T&C Arm 2 (re-evaluate A vs B in the active-WIP packaging panel).  
**Candidate description first 100 chars (unverified until `SOURCES.md`):** `How do airplanes fly? Inside the Wright brothers' 1901 wind tunnel that proved the flight tables wrong.`

**Proposed subject-only tags (8 tags, zero channel names, zero `J3224`-rejected low-RPM keywords):**  
`how do airplanes fly, wright brothers first flight, wright brothers wind tunnel, how does an airplane wing work, 1901 wind tunnel experiment, smeaton coefficient lift, wing warping three axis control, history of engineering breakthroughs`

---

## 2b. Neighbour Pass (Blocking · `STUDIO_PLAYBOOK.md` §2 Step 4, Retrieved `2026-11-21`)

Saved in [`evidence_2026-11-21_neighbours.json`](evidence_2026-11-21_neighbours.json) (`bigCount = 8` raw / `6` aviation `≥1M` / **`5` strictly on-topic lift & Wright-brothers education videos `≥1M`** after excluding `2` airplane-keyword false positives `dzrwnwOx0fw` & `iKYHf22qVdM` and noting broader aviation `hd8tYiLSmn0`; `hasTed = true`, `gate = PASS`) and [`evidence_2026-11-21_public_search.json`](evidence_2026-11-21_public_search.json) (`9` queries, `64` search rows, `0` exact title collisions):

| # | Views (`2026-11-21`) | Channel (internal) | id & URL | Title | Subject words we reuse |
|---:|------:|--------------------|----------|-------|------------------------|
| 1 | `4,461,586` | Sabin Civil Engineering (`public_search.py`) | [`LigpsX1KoQE`](https://youtu.be/LigpsX1KoQE) | *The Brilliant Engineering of FIRST FLIGHT !* | `first flight`, `wright brothers`, `lift`, `wing` |
| 2 | `2,568,211` | TED-Ed ★ (`neighbours.py`) | [`p4VHMsIuPmk`](https://youtu.be/p4VHMsIuPmk) | *How do airplanes actually fly? - Raymond Adkins* | `how do airplanes fly`, `lift`, `airfoil` |
| 3 | `2,481,276` | minutephysics (`neighbours.py`) | [`Gg0TXNXgz-w`](https://youtu.be/Gg0TXNXgz-w) | *How Do Airplanes Fly?* | `how do airplanes fly`, `wings`, `airflow` |
| 4 | `2,113,943` | The Efficient Engineer (`public_search.py`) | [`E3i_XHlVCeU`](https://youtu.be/E3i_XHlVCeU) | *Understanding Aerodynamic Lift* | `aerodynamic lift`, `airfoil`, `pressure` |
| 5 | `2,044,514` | Math and Science (`public_search.py`) | [`CT5oMBN5W5M`](https://youtu.be/CT5oMBN5W5M) | *How Airplane Wings REALLY Generate Lift* | `airplane wings`, `generate lift`, `airflow` |
| 6 | `1,754,830` | SciShow Kids (`neighbours.py`) | [`VLpSxHwfU04`](https://youtu.be/VLpSxHwfU04) | *How Airplanes Fly! \| Airplane Science* | `how airplanes fly`, `lift`, `thrust`, `drag` |
| 7 | `1,662,146` | Veritasium (`neighbours.py`) | [`aFO4PBolwFg`](https://youtu.be/aFO4PBolwFg) | *How Does A Wing Actually Work?* | `how does a wing work`, `lift`, `airflow` |
| 8 | `1,583,808` | Naked Science (`public_search.py`) | [`iSuDuCzszUg`](https://youtu.be/iSuDuCzszUg) | *Learning To Fly \| The World's First Airplane* | `first airplane`, `wright brothers`, `flight` |
| 9 | `1,410,350` | Simple History (`neighbours.py`) | [`YDlk4Ky_ahs`](https://youtu.be/YDlk4Ky_ahs) | *The Wright Brothers, First Successful Airplane (1903)* | `wright brothers`, `first flight`, `1903`, `Kitty Hawk` |
| 10 | `384,056` | Real Engineering (`neighbours.py`) | [`WCPapu78SNM`](https://youtu.be/WCPapu78SNM) | *Wright Brothers Didn't Invent Flight* | `wright brothers`, `control`, `wing warping` |
| 11 | `293,525` | SciShow (`neighbours.py`) | [`9S7H8TlkBC4`](https://youtu.be/9S7H8TlkBC4) | *How the Wright Brothers Changed Everything We Know About Flying* | `wright brothers`, `wind tunnel`, `flight` |

---

## 3. Title ABC & Shorts Titles (Collision-Checked `2026-11-21` & `2026-11-24` · Full Scoring in `PACKAGE_FIRST_SCORING_v01.md`)

**Growth System v2 + LEARNINGS Rule 15 & Rule 26:** search phrase first · `≤50` characters ideal (`≤70` max) · no series suffix · `0` exact collisions with live videos.

| | Title | Chars | Exact Collisions | Role & Notes | Keep? |
|---|-------|------:|-----------------:|--------------|-------|
| **A (Primary ≤50c · PICK)** | `Wright Brothers First Flight: The 1901 Wind Tunnel` | `50` | `0` (`11-21`) | Exact `J3224` Cluster 4 Lead Film query (`19.0k`/mo, comp `45`, `10/10` US gap) + `1901 Wind Tunnel` twist (`96/100` draft rubric) | **PICK (Primary Arm A)** |
| **B (T&C Arm B · Plan Title)** | `Wright Brothers First Flight: The 1901 Wind Tunnel That Solved Lift` | `67` | `0` (`11-24`) | Verbatim `hos-search-2027-01` plan title; `evidence_2026-11-24_plan_title_search.json` (`93/100` draft rubric) | **KEEP (T&C Arm B)** |
| **C (T&C Arm C · Physics Lead)** | `How Do Airplanes Fly? (The 1901 Wind Tunnel)` | `44` | `0` (`11-21`) | Exact evergreen autocomplete question `"how do airplanes fly"` + 1901 apparatus (`93/100` draft rubric) | **KEEP (T&C Arm C)** |
| **Reserve Backup** | `How Did the Wright Brothers Solve Flight? (1901)` | `48` | `0` (`11-21`) | Direct discovery question + 1901 date hook | Reserve backup |
| **Reject** | `Aerodynamic Lift Coefficients and Control Surfaces \| HOS` | `57` | — | Academic jargon + forbidden series suffix | **Reject** |
| **Short S01** | `Why Did the Wright Brothers Build a Wind Tunnel?` | `48` | `0` (`11-21`) | `16–19 s` positive search question (Sat 2 Jan 11:30 · 42 words · Ben 19 Nov house rules) | **Keep (Short 1)** |
| **Short S02** | `How Did the Wright Brothers Steer the First Plane?` | `50` | `0` (`11-21`) | `16–19 s` positive search question (Fri 1 Jan 11:30 · 42 words · Ben 19 Nov house rules) | **Keep (Short 2)** |

---

## 4. Outlier / Competitive Patterns (On-Brand Only)

| Outlier / pattern | Views | Steal (structure) | Do **not** copy |
|---|---|---|---|
| `Sabin Civil Engineering` *The Brilliant Engineering of FIRST FLIGHT !* (`LigpsX1KoQE`) | `4,461,586` | Engineering-problem framing (lift, control, propellers as linked puzzles) | Modern CAD/cutaway lecture visual style |
| `TED-Ed` *How do airplanes actually fly?* (`p4VHMsIuPmk`) & `Veritasium` *How Does A Wing Actually Work?* (`aFO4PBolwFg`) | `2.57M` / `1.66M` | Myth-busting lift accurately (pressure difference + downward deflection — zero equal-transit-time fallacy) | Purely modern physics whiteboard without the 1901 workshop discovery drama |
| `History Dude` (1.1K US → `51.9K`, `13×`) & `Acta Historia` (1.2K CA → `1.4K`, `12×`) (`J3224`) | `51.9K` / `1.4K` | Adult Anglosphere historical-engineering narrative framing | Long slow-paced slideshow pacing |

---

## 5. Incorporate Into the Build (5-Part Chapter Arc & Guardrails — UNVERIFIED)

**5-part chapter list (draft for script stage — expands `TOPIC.md` 4-act sketch to HOS's standard 5 parts, `7–9 min`):**
1. **Part 01 (0:00–1:30, no chapter card):** Proof-first cold open inside the roaring 1901 Dayton bicycle-shop wind tunnel (`0:00–0:05`) cutting to a tiny brass airfoil tilting on a hacksaw-blade balance (`0:05–0:15`); rewind to the summer 1901 Kill Devil Hills glider producing barely a third of predicted lift and Wilbur's despair quote (lock verbatim quote in `SOURCES.md`).
2. **Part 02 (1:30–3:15):** Suspecting Otto Lilienthal's lift tables and John Smeaton's 1759 air-pressure coefficient (`0.005`), Wilbur and Orville bolt a horizontal third bicycle wheel to the front of a bike, then build the 6-foot wooden wind tunnel (`16-inch` square) with honeycomb air-straightener and hacksaw-blade / bicycle-spoke lift and drift balances (`Oct–Dec 1901`).
3. **Part 03 (3:15–5:00):** Testing `200+` miniature wings (`~40–50` systematically graphed) exposes Smeaton's `0.005` as roughly **50% too high** vs `0.0033` (note exact denominator — never call it "40%"), explains lift accurately via pressure difference + downward airflow deflection (never equal-transit-time), and proves long, narrow, gently cambered wings beat thick curved ones.
4. **Part 04 (5:00–6:45, Midpoint Twist):** "Case closed? Wrong." Even with accurate lift tables, the 1902 glider at Kill Devil Hills hits **adverse yaw** — the rising wing drags more and spins the glider sideways. Wilbur's cardboard inner-tube box wing-warping + linking roll to a movable rear rudder alongside the front elevator creates three-axis control.
5. **Part 05 (6:45–8:45):** Treating propellers as rotating wings (`~66%` efficiency) + lightweight cast-aluminium engine built with machinist **Charlie Taylor** (`~12 hp`) → **17 December 1903** at Kill Devil Hills near Kitty Hawk (`12 s / 120 ft` to `59 s / 852 ft`) → hand-off to next Cluster 4 film.

---

## 6. Retention Plan (Whole-Video Watch)

| Minute zone | Job | Picture / VO note |
|---|---|---|
| `0:00–0:05` | Answer image / curiosity spike | 6-foot wooden wind tunnel roaring in 1901 Dayton bicycle shop, glowing airflow streamlines (3D cartoon, moving) |
| `0:05–0:15` | Physical proof + title question | Tiny curved brass wing tilting upward on hacksaw-blade / bicycle-spoke balance; *"How do airplanes actually fly — and why did two bicycle mechanics have to break a 142-year-old physics table to find out?"* |
| `~0:25` | Stakes | Why every engine-heavy flying machine crashed until someone measured lift accurately |
| `0:25–0:45` | First fact + early DATA+SCALE | `0.005` vs `0.0033` Smeaton error (~50% too high) / 200 tiny wings tested (`SOURCES.md` required) |
| `~5:00` | Midpoint twist | Good wings still spun out of control → 1902 adverse yaw & linked wing-warping + rudder |
| `~8:30` | Payoff + hand-off | 17 Dec 1903 Kill Devil Hills flights (`12 s` → `59 s`) → hand-off line (no goodbye, no subscribe ask) |

---

## 7. Sign-Off (Block Production Until Checked)

- [x] **Keywords** verified (`wright brothers first flight` `19,018`/mo comp `45` `10/10` US gap, `the wright brothers` `+74.8%`, `how do airplanes fly`, `4/4` autocomplete `yes`, `5` strictly on-topic `≥1M` neighbours incl. `TED-Ed` ★ `#1`, low-RPM `aviation history` PK 35% rejected).
- [x] **Title** primary and Test & Compare variants scored (`PACKAGE_FIRST_SCORING_v01.md`, `0` exact collisions across Titles A/B/C and Shorts S01/S02; `J3264` Smeaton `50% TOO HIGH`, accurate lift physics, and Kill Devil Hills guardrails locked).
- [x] **Script reviewer** (`npm run review:script` PASS `93.6/100`) and `npm run gate:episode` PASS verified on `01_Script/wright_brothers_wind_tunnel_script_master_v01.md` (drafted with primary NASA/Smithsonian/NPS quotes in `SOURCES.md` & `FACT_NOTES_v01.md`; pending independent `facts` lane audit and Chief lock before any VO or picture spend).

**Signed off by:** Gemini (`J3504` draft package & script — awaits independent `facts` lane & Chief lock before VO/picture spend; `£0.00` spent) · **Date:** `2026-11-24`

- **Rule-E topic review (`J3264`, `2026-11-21`):** **GO (`97.2 / 100` · `9.72 / 10`, `10/10` gates PASS)**
- **Package-first + script draft (`J3504`, `2026-11-24`):** **DRAFTED** (8 days ahead of Wed 2 Dec 18:00 London target)
- **Independent `facts` lane & Chief script lock due:** Fri 11 Dec 2026
- **Ben's watch by:** Mon 28 Dec 2026 · **Target air:** Thu 31 Dec 2026 18:00 London (slides one week if not ready)
