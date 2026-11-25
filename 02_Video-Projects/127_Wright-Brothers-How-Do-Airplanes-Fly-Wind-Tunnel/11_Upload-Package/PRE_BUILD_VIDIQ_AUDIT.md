# Pre-Build vidIQ & Public-Search Audit — `HOS:127` (`Wright Brothers First Flight: The 1901 Wind Tunnel`)

**Hard gate:** Run **before** locking script, VO, prompts, or picture gen for any new long.  
**Status (`J3688`, `2026-11-25`):** Rule-E topic go/no-go review **GO (`97.2 / 100` · `9.72 / 10`, `J3264`, `2026-11-21`)**; accelerated into the December `hos-search-2027-01` 4-film test cohort as **Cluster 4 Lead Film 4 (target Thu 31 Dec 2026, 18:00 London)** (`J3495` / PR `#1239`). Independent Gemini `facts` audit (`J3621`, `01_Script/GEMINI_FACTS_CHECK_v01.md`, PR `#771`) and Acting Chief `J3622` FIX ruling resolved in **`v02`** (`J3688`, `2026-11-25`): `wright_brothers_wind_tunnel_script_master_v02.md`, `SOURCES.md`, `FACT_NOTES_v02.md`, `SHORTS_SCRIPTS_v02.md`, `PACKAGE_FIRST_SCORING_v01.md`, `LAUNCH_PLAN.md`, and this audit (`£0.00`). Per-title vidIQ app numeric scores remain pending when `HOS:127` enters active WIP under Rule G. **Awaits Chief `v02` review & lock before any VO or picture spend.**

---

## Episode

| Field | Value |
|-------|-------|
| ID / slug | `127_Wright-Brothers-How-Do-Airplanes-Fly-Wind-Tunnel` |
| Working title | `Wright Brothers First Flight: The 1901 Wind Tunnel` (`50` chars, Arm A) · T&C Arm B: `Wright Brothers First Flight: The 1901 Wind Tunnel That Solved Lift` (`67` chars) · T&C Arm C: `How Do Airplanes Fly? (The 1901 Wind Tunnel)` (`44` chars) |
| Date pulled | `2026-11-21` (`J3245` / `J3264`) + `2026-11-24` (`J3504` plan-title collision check; `J3224` vidIQ `2026-11-20`) + `2026-11-25` (`J3621` / `J3688` v02 sync) |
| Credits used (approx) | `0` (`£0.00` across `J3245`, `J3264`, `J3504`, `J3621`, and `J3688`) |
| 2027 Search Plan slot | Cluster 4 Lead Film 4 (accelerated target **Thu 31 Dec 2026, 18:00 London**; Ben's watch Mon 28 Dec) — *Breakthrough & Lost Engineering* (`hos-search-2027-01`) |
| Brand guardrails | Wonder over fearbait · primary NASA/Smithsonian/NPS/Royal Society/RMG aerodynamics & archival history · HOS lane (a familiar thing, and the moment we found out) |

---

## 1. Success Targets (This Episode)

| Metric | Target |
|--------|--------|
| Title score | ≥ **90** (aim **95+**; per-title vidIQ login score pending active WIP) |
| Primary keyword overall | `wright brothers first flight` (`19,018`/mo, comp `45`, `10/10` US SERP gap, `10` GB autocomplete suggestions) + `how do airplanes fly` (`10` GB autocomplete suggestions; `9` distinct `≥1M` on-topic videos across `neighbours.json` + `public_search.json`) |
| Hook promise | How two bicycle mechanics exposed a 142-year-old flight formula fifty percent too high inside a homemade wooden wind tunnel — and cracked how wings lift and turn |
| Retention design | 5 cause-and-effect parts (`1901 glider 1/3 lift failure` → `horizontal third bicycle wheel & wooden wind tunnel` → `200 tiny 20-gauge steel wings & real lift physics` → `1902 "well digging" adverse yaw & linked movable rear rudder` → `Charlie Taylor's 12-hp aluminium engine, rotary-wing propellers, 17 Dec 1903 flights & 1905 payoff`) |
| Packaging | Thumb readable at `168×94`; clear left-band cream/gold serif lettering (`50% TOO HIGH` with steel airfoil / `200 TINY WINGS` with miniature 20-gauge steel wings; 3rd T&C variant built post-VO per `§2.9`; all text hand-verified per `§2.6`), warm 3D period palette, Explorer small lower-left |

---

## 2. Keyword Research (`J3224` vidIQ `2026-11-20` + Signed-Out GB `public_search.py` / `neighbours.py` `2026-11-21`)

| Keyword | Monthly Vol / Comp (`J3224`) | Autocomplete (GB `11-21`) | Top Competitors | Role (title / desc / tags / Shorts) | Keep? |
|---------|------------------------------|---------------------------|-----------------|-------------------------------------|-------|
| `wright brothers first flight` | `19,018`/mo · comp `45` · `10/10` US gap | **yes** (`10` suggestions) | `Sabin Civil Eng.` `4.46M`, `Naked Science` `1.58M`, `Simple History` `1.41M` | **primary** (Title Arm A + T&C Arm B + desc line 1 + tags) | **Keep** |
| `how do airplanes fly` | Evergreen high demand | **yes** (`10` suggestions) | `TED-Ed` `2.57M`, `minutephysics` `2.48M`, `SciShow Kids` `1.75M` | **primary / T&C Arm C** (Title Arm C + desc line 1 + tags) | **Keep** |
| `wright brothers wind tunnel` | Specific apparatus query | **yes** (`1` exact suggestion) | `Sabin Civil Eng.` `4.46M`, `MIT` `12.9k` | **secondary / Short S01** (desc + tags) | **Keep** |
| `how does an airplane wing work` | Evergreen physics query | **yes** (`3` suggestions) | `The Efficient Engineer` `2.11M`, `Math & Science` `2.04M`, `Veritasium` `1.66M` | **secondary** (desc + tags) | **Keep** |
| `aviation history` | `54,239`/mo · PK 35%, VN 12% | — | Non-Anglosphere top 3 | **Rejected in `J3224`** — do NOT use in title or tags | **Reject** |

**Decision:** Primary title lead = `Wright Brothers First Flight: The 1901 Wind Tunnel` (Arm A, `50c`, `0` collisions; manifest neighbour phrase `"wright brothers"`), with `Wright Brothers First Flight: The 1901 Wind Tunnel That Solved Lift` (Arm B, `67c`, verbatim plan title, `0` collisions) and `How Do Airplanes Fly? (The 1901 Wind Tunnel)` (Arm C, `44c`, physics lead, `0` collisions) as Test & Compare arms.  
**Verified description first line (`v02`, synced with `LAUNCH_PLAN.md` & `SOURCES.md`):** `Wright brothers first flight: how a 1901 bicycle-shop wind tunnel fixed a 142-year-old lift error and solved how airplanes fly.`

**Proposed subject-only tags (8 tags, zero channel names, zero `J3224`-rejected low-RPM keywords):**  
`wright brothers first flight, how do airplanes fly, wright brothers wind tunnel, how does an airplane wing work, 1901 wind tunnel experiment, smeaton coefficient lift, wing warping three axis control, history of engineering breakthroughs`

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
| **Short S01** | `Why Did the Wright Brothers Build a Wind Tunnel?` | `48` | `0` (`11-21`) | `16–19 s` positive search question (Sat 2 Jan 11:30 · `43w` ≈ `17.8 s` · Ben 19 Nov house rules · `SHORTS_SCRIPTS_v02.md`) | **Keep (Short 1)** |
| **Short S02** | `How Did the Wright Brothers Steer the First Plane?` | `50` | `0` (`11-21`) | `16–19 s` positive search question (Fri 1 Jan 11:30 · `44w` ≈ `18.0 s` · Ben 19 Nov house rules · `SHORTS_SCRIPTS_v02.md`) | **Keep (Short 2)** |

---

## 4. Outlier / Competitive Patterns (On-Brand Only)

| Outlier / pattern | Views | Steal (structure) | Do **not** copy |
|---|---|---|---|
| `Sabin Civil Engineering` *The Brilliant Engineering of FIRST FLIGHT !* (`LigpsX1KoQE`) | `4,461,586` | Engineering-problem framing (lift, control, propellers as linked puzzles) | Modern CAD/cutaway lecture visual style |
| `TED-Ed` *How do airplanes actually fly?* (`p4VHMsIuPmk`) & `Veritasium` *How Does A Wing Actually Work?* (`aFO4PBolwFg`) | `2.57M` / `1.66M` | Myth-busting lift accurately (pressure difference + downward deflection — zero equal-transit-time fallacy) | Purely modern physics whiteboard without the 1901 workshop discovery drama |
| `History Dude` (1.1K US → `51.9K`, `13×`) & `Acta Historia` (1.2K CA → `1.4K`, `12×`) (`J3224`) | `51.9K` / `1.4K` | Adult Anglosphere historical-engineering narrative framing | Long slow-paced slideshow pacing |

---

## 5. Incorporate Into the Build (Verified 5-Part Chapter Arc & Guardrails — Synced to `v02` & `SOURCES.md`)

**5-part chapter list (synced to `01_Script/wright_brothers_wind_tunnel_script_master_v02.md`, `7–9 min`):**
1. **Part 01 (0:00–1:30, no chapter card):** Proof-first cold open inside the roaring 1901 Dayton bicycle-shop wind tunnel (`0:00–0:05`) showing a tiny curved **20-gauge steel** wing tilting on a hacksaw-blade / bicycle-spoke balance (`0:05–0:15`); `1900` tent-camp glider stakes near Kitty Hawk (`0:14–0:23`); `1901` Kill Devil Hills glider producing only `1/3` of predicted lift due to flawed wing-lift curves together with John Smeaton's `1759` air-pressure coefficient `0.005` (`>50%` higher than `0.0033` / modern `0.00327`); May `1899` Smithsonian letter, `5-foot` wing-warping kite, Otto Lilienthal (`1896`), and the `1901` wooden camp shed test (`100 lb` airframe + `150 lb` pilot design vs barely lifting itself).
2. **Part 02 (1:30–3:10):** Autumn `1901` horizontal third bicycle wheel test (`>3×` greater angle than Lilienthal predicted; Explorer beat 1), followed by the open-return wooden wind tunnel belt-driven from the shop's small gas engine (`Oct 1901`), nearly a month perfecting flow-straightening vanes, and delicate lift and drag balances built from bicycle spokes and hacksaw blades.
3. **Part 03 (3:10–4:50):** Cutting, hammering, filing, and soldering `100–200` (up to `200`) miniature **`20-gauge` (`1/32` inch) steel** wings — as thin as a modern bank card (`0.794 mm` vs `0.76 mm`) — formally charting nearly `50`; explicitly debunking the equal-transit-time myth with accurate lift physics (faster upper airflow / pressure difference + downward airflow turning via NASA GRC); proving long, narrow, gently curved wings outperform thick deeply arched airfoils.
4. **Part 04 (4:50–6:30, Midpoint Twist):** "Case closed? Not even close." In September `1902` at Kill Devil Hills, accurate lift tables solve lift, yet warping the wings triggers violent adverse-yaw `"well digging"` turn reversals (spinning the nose the wrong way); wiring a movable single rear rudder to the pilot's wing-warping hip cradle alongside the front elevator yields the world's first coordinated three-axis aircraft (`700–1,000` glides, longest `622.5 ft` in `26 s` — more than double their typical `300-foot` glides of `1901`, plus Wilbur's `"knowledge and skill"` quote).
5. **Part 05 (6:30–8:30):** By early `1903`, `10` engine makers reply unable to meet spec; machinist **Charlie Taylor** builds a `12-hp` 4-cylinder cast-aluminium-crankcase engine in `6` weeks (`12 Feb 1903`, roughly two typical `6-hp` lawn-mower engines); `8.5-foot` laminated-spruce rotary-wing counter-rotating propellers driven by figure-eight bicycle chains; `14 Dec` coin toss and `3.5 s` stall off the `60-foot` rail (Explorer beat 2); **`17 December 1903` at `10:35 a.m.`** (`27 mph` headwind: Orville `12 s / 120 ft`, Wilbur 4th flight `59 s / 852 ft`); `5 Oct 1905` Huffman Prairie (`39 min / 24.5 mi / 30 circles`, speaking the 6-year `1899–1905` timeline `SCALE` aloud); hand-off to John Harrison's `1759` brass marine watch `H4` (`"a century and a half earlier — in the very same year Smeaton published his table"`, RMG `ZAA0037`).

---

## 6. Retention Plan (Whole-Video Watch — Synced to `v02`)

| Minute zone | Job | Picture / VO note |
|---|---|---|
| `0:00–0:05` | Answer image / curiosity spike | Roaring 1901 Dayton bicycle-shop wooden wind tunnel cutaway with golden airflow rushing past a tiny curved 20-gauge steel wing on a hacksaw-blade / bicycle-spoke balance (3D cartoon, moving); *"How did a wooden box in a bicycle shop solve the mystery of how airplanes actually fly?"* |
| `0:05–0:15` | Physical proof + promise | Close-up through the wind-tunnel viewing glass onto the balance pointer & ink ledger; *"By exposing an eighteenth-century flight formula fifty percent too high, then cracking how wings lift and turn."* |
| `~0:14–0:23` | Stakes | 1900 canvas tent camp & dunes near Kitty Hawk — why textbook equations left early gliders stranded or risking a fatal fall |
| `0:25–0:40` | First fact + early DATA+SCALE | `1901` glider `1/3` lift + Smeaton `1759` `0.005` vs `0.0033` (`>50%` too high, bridge steel-beam analogy) alongside flawed wing-lift curves (`SOURCES.md` verified) |
| `~4:50` | Midpoint twist | Good wings still spun the wrong way (`"well digging"` adverse yaw) → 1902 movable single rear rudder linked to wing-warping hip cradle |
| `~8:02–8:30` | Payoff + hand-off | `17 Dec 1903` flights (`12 s / 120 ft` → `59 s / 852 ft`) + `5 Oct 1905` (`39 min / 24.5 mi`, 6-year timeline `SCALE` spoken aloud) → John Harrison `1759` `H4` hand-off (no goodbye, no subscribe ask) |

---

## 7. Sign-Off (Block Production Until Checked)

- [x] **Keywords** verified (`wright brothers first flight` `19,018`/mo comp `45` `10/10` US gap, `the wright brothers` `+74.8%`, `how do airplanes fly`, `4/4` autocomplete `yes`, `5` strictly on-topic `≥1M` neighbours incl. `TED-Ed` ★ `#1`, low-RPM `aviation history` PK 35% rejected).
- [x] **Title** primary and Test & Compare variants scored (`PACKAGE_FIRST_SCORING_v01.md`, `0` exact collisions across Titles A/B/C and Shorts S01/S02; Primary Arm A `Wright Brothers First Flight: The 1901 Wind Tunnel`, `50c`, synced across all docs; `J3264` & `J3621` Smeaton `50% TOO HIGH`, 20-gauge steel models, accurate lift physics, and Kill Devil Hills guardrails locked).
- [x] **Script reviewer** (`npm run review:script` PASS `93.6/100`, `1,282` words, `8.5` min, `8/8` structure gates) and default `npm run gate:episode` (no `--script`, `9/9 OK`) PASS verified on `01_Script/wright_brothers_wind_tunnel_script_master_v02.md` with primary NASA/Smithsonian/NPS/Royal Society/RMG citations in `SOURCES.md` & `FACT_NOTES_v02.md` (`J3688` resolves all 8 `J3621`/`J3622` fixes; awaiting Chief lock before any VO or picture spend).

**Signed off by:** `macbook-2` (`J3688` v02 sync — awaits Chief `v02` review & lock before VO/picture spend; `£0.00` spent) · **Date:** `2026-11-25`

- **Rule-E topic review (`J3264`, `2026-11-21`):** **GO (`97.2 / 100` · `9.72 / 10`, `10/10` gates PASS)**
- **Package-first + script draft (`J3504`, `2026-11-24`):** **DRAFTED (`v01`)**
- **Independent `facts` audit (`J3621`, `2026-11-25`):** **AUDITED (`GEMINI_FACTS_CHECK_v01.md`, PR `#771` — 5 blocking FLAGs)**
- **Corrected `v02` package (`J3688`, `2026-11-25`):** **BUILT (all 8 `J3621`/`J3622` fixes applied; awaits Chief lock)**
- **Chief script lock due:** Fri 11 Dec 2026
- **Ben's watch by:** Mon 28 Dec 2026 · **Target air:** Thu 31 Dec 2026 18:00 London (slides one week if not ready)
