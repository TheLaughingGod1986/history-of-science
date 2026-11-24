# Topic Brief — `135_Carnot-Clausius-Boltzmann-What-Is-Entropy` (`HOS:135` · Backlog Proposal in `next_hos`, Awaiting Rule-E Review)

> **RULE G & UNVERIFIED CLAIMS STATUS (`J3458`, `2026-11-24`):**
> - **Backlog Status:** Added to `jobs/WIP.json` `next_hos` under **Rule G** (`active` has `4 / 4` HOS films full: `008`, `009`, `010`, `013`). Nothing is started in production (`status.json` stages are all `todo`; `£0.00` spent). Awaits its queued **Rule-E topic go/no-go review** (`kind:review`).
> - **Unverified Working Notes:** All historical, biographical, and scientific claims in this brief are **UNVERIFIED** working notes. Before any script is locked, VO is recorded, or picture credit is spent, every claim must be backed by verbatim primary-source quotes in `SOURCES.md` and verified through the `facts` lane (`gemini-agy`).

---

## 1. HOS Data Comparison (`2026-11-23` Snapshot + `studio_ctr.json` + `channel_daily.json` + `REPORT.md`)

- **Data sources read:**
  - `05_Analytics/hos/snapshots/2026-11-23.json` (`takenAt: 2026-11-23T06:40:34.195Z`, `43` public videos = `7` longs + `36` Shorts, `4,477` total views, `6` subscribers)
  - `05_Analytics/hos/studio_ctr.json` (`readAt: 2026-11-23T07:11:17.265966+00:00`, lifetime Studio impressions, CTR, average view %, and Shorts stayed-to-watch %)
  - `05_Analytics/hos/channel_daily.json` (`through: 2026-11-21`) and `05_Analytics/hos/REPORT.md`
  - `05_Analytics/LEARNINGS.md` (rules 1–41) and `05_Analytics/hos/search_research/2026-11-20.md` (`J3224`, `needsBen`)
- **Elapsed-day denominator (`age_days`):** `max((date(2026, 11, 23) - date.fromisoformat(publishedAt[:10])).days, 1)` (`views/day = views / age_days`).
- **Low-sample statistical caveat (`LEARNINGS.md` Rule 1):** Five public HOS longs have only `5–15` lifetime views (`17–74` impressions), and bottom-tier Shorts have `4–30` views. Patterns inferred from those small-N rows are treated explicitly as **hypotheses**, not settled laws.

### 1a. All `7` Public HOS Longs — Ranked by Views/Day Since Publish (`2026-11-23`)

| Rank | Video ID | Film | Title | Published (`age_days`) | Views (`2026-11-23`) | Views / Day | Studio Impressions (Lifetime) | Studio CTR (Lifetime) | Studio Avg View % (Lifetime) | YTA 28d Views (`through 11-21`) | YTA 28d Avg View % |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **1** | `AL_-qlWko_g` | `002` | *How Did We Discover the Periodic Table?* | `2026-09-17` (`67d`) | **162** | **2.42/d** | 1,163 | 3.35% | 21.23% (`115s / 541s`) | 13 | 23.33% |
| **2** | `GHZDsiH7L7A` | `004` | *What's Inside an Atom? Mostly Empty Space* | `2026-10-15` (`39d`) | **35** | **0.90/d** | 840 | 1.43% | 23.54% (`124s / 525s`) | 9 | 54.97% |
| **3** | `VbPubYd6Fbs` | `006` | *The Willow Tree That Was Made of Air* | `2026-11-05` (`18d`) | **15** | **0.83/d** | 74 | 4.05% | **48.15%** (`256s / 532s`) | 15 | 48.15% |
| **4** | `ETynHpIYLeY` | `007` | *How Was the First Vaccine Made? (And Why It's Named After a Cow)* | `2026-11-12` (`11d`) | **7** | **0.64/d** | 44 | 4.55% | 19.29% (`103s / 532s`) | 7 | 19.29% |
| **5** | `wwcjcFfC-5M` | `005` | *The Tied Arm That Proved Your Blood Circulates* | `2026-10-29` (`25d`) | **7** | **0.28/d** | 17 | **17.65%** | 6.73% (`36s / 529s`) | 6 | 7.78% |
| **6** | `_C92tIJCk8A` | `001` | *How Did We Discover Germs?* | `2026-09-03` (`81d`) | **7** | **0.09/d** | 46 | 6.52% | 48.08% (`176s / 365s`) | 0 | — |
| **7** | `frP_YrNShsU` | `003` | *How Did We Discover X-rays?* | `2026-09-24` (`60d`) | **5** | **0.08/d** | 43 | 2.33% | 26.65% (`114s / 426s`) | 3 | 14.12% |

- **3 Best HOS Longs & What They Share:**
  1. **`AL_-qlWko_g` (`002` *How Did We Discover the Periodic Table?*, `541s`):** **`2.42` views/day** (`162` views in `67d`), **`1,163` impressions** (`52.2%` of all HOS long impressions), `3.35%` CTR, `21.23%` Studio avg view % (`70%` at `0:15`, `50%` at `0:30`).
  2. **`GHZDsiH7L7A` (`004` *What's Inside an Atom? Mostly Empty Space*, `525s`):** **`0.90` views/day** (`35` views in `39d`), **`840` impressions** (`37.7%` of all HOS long impressions), `1.43%` CTR, `23.54%` Studio avg view % (`54.97%` in 28d YTA; `62%` at `0:15`, `45%` at `0:30`).
  3. **`VbPubYd6Fbs` (`006` *The Willow Tree That Was Made of Air*, `532s`):** **`0.83` views/day** (`15` views in `18d`), `74` impressions, `4.05%` CTR, channel-best **`48.15%` Studio avg view % (`256s / 532s`)** (small-N hypothesis at `15` views).
  - **Shared pattern (Subject, Title Shape, Opening, Thumbnail Concept, Length):** `002` and `004` generate **`89.9%` (`2,003 / 2,227`) of all HOS long impressions** and **`82.8%` (`197 / 238`) of all HOS long views** because they combine iconic physics/chemistry concepts with plain, high-volume search questions (`Periodic Table`, `What's Inside an Atom?`) backed by massive `TED-Ed` / `Veritasium` neighbour pools (`LEARNINGS.md` Rules 1, 15, 26), run **`8.75–9.0 min` (`525–541s`)**, and open with a concrete physical mystery (`Rule 10`). `006` (`48.15%` avg view %) demonstrates strong retention when one physical mystery carries the whole narrative.
- **3 Worst HOS Longs & What They Share (Hypotheses on Small N):**
  1. **`frP_YrNShsU` (`003` *How Did We Discover X-rays?*, `426s`):** **`0.08` views/day** (`5` views in `60d`), `43` impressions, `2.33%` CTR, `26.65%` Studio avg view %.
  2. **`_C92tIJCk8A` (`001` *How Did We Discover Germs?*, `365s`):** **`0.09` views/day** (`7` views in `81d`), `46` impressions, `6.52%` CTR, `48.08%` Studio avg view %.
  3. **`wwcjcFfC-5M` (`005` *The Tied Arm That Proved Your Blood Circulates*, `529s`):** **`0.28` views/day** (`7` views in `25d`), **`17` impressions**, `17.65%` CTR, **`6.73%` Studio avg view % (`36s / 529s`)** (alongside `007` Vaccine `44` impr / `7`v / `0%` Suggested).
  - **Shared pattern:** Literary statement titles without a search phrase (`005`, `17` impressions; `Rule 26`) and shorter `6–7 min` broad survey titles (`001`, `003`) miss both search demand and high-CTR stakes framing (`Rules 10, 15, 23, 26`).

### 1b. All `36` Public HOS Shorts — Ranked by Views/Day Since Publish (`2026-11-23`)

| Rank | Video ID | Title | Published (`age_days`) | Views (`2026-11-23`) | Views / Day | Studio Stayed % (Lifetime) | Studio Avg View % (Lifetime) | Likes |
|---:|---|---|---:|---:|---:|---:|---:|---:|
| **1** | `el30-mHiH-0` | *How Does the Heart Pump Blood?* | `2026-11-22` (`1d`, early 20h) | **523** | **523.00/d** | 26.77% | 66.41% (`17s / 26s`) | 5 |
| **2** | `xzKoHg0E0_U` | *What Is Dalton's Atomic Theory?* | `2026-11-16` (`7d`) | **239** | **34.14/d** | **53.13%** | 61.49% (`15s / 25s`) | 0 |
| **3** | `29bpGAI0wb8` | *What happens if you keep cutting gold in half?* | `2026-10-16` (`38d`) | **1,229** | **32.34/d** | 40.78% | 44.14% (`11s / 25s`) | 12 |
| **4** | `Wvjd8g0CpzE` | *The Blood Vessels Finer Than a Hair* | `2026-11-15` (`8d`) | **218** | **27.25/d** | 15.35% | 74.94% (`19s / 26s`) | 3 |
| **5** | `Bks_JLId1ew` | *How Do Plants Make Oxygen?* | `2026-11-21` (`2d`, early 44h) | **50** | **25.00/d** | 48.57% | 96.53% (`25s / 26s`) | 0 |
| **6** | `PFj6172YU4Q` | *One Tight Band Proved Your Blood Goes Round* | `2026-11-08` (`15d`) | **221** | **14.73/d** | 16.67% | 61.53% (`17s / 27s`) | 3 |
| **7** | `AMSriTQ-lcQ` | *Are Marie Curie's Notebooks Still Radioactive?* | `2026-10-28` (`26d`) | **274** | **10.54/d** | 22.66% | 76.94% (`17s / 22s`) | 6 |
| **8** | `l8bxm9L3zl8` | *How Does a Blood Pressure Cuff Work?* | `2026-11-20` (`3d`) | **29** | **9.67/d** | 38.46% | 60.99% (`15s / 24s`) | 0 |
| **9** | `OnJ8MFu0Mi0` | *How Did John Snow Stop Cholera?* | `2026-10-26` (`28d`) | **231** | **8.25/d** | 29.60% | 65.66% (`15s / 23s`) | 8 |
| **10** | `pWySvZsneZg` | *Why Gold Foil Bounced Rutherford's Particles Back* | `2026-11-01` (`22d`) | **137** | **6.23/d** | 37.23% | **112.43%** (`28s / 25s`) | 2 |
| **11** | `oKqmnJNGiHg` | *How Was Phosphorus Discovered?* | `2026-10-21` (`33d`) | **194** | **5.88/d** | 42.03% | 88.35% (`20s / 23s`) | 7 |
| **12** | `-3L6HzJ_d_4` | *What Is the Pasteur Swan Neck Flask Experiment?* | `2026-10-27` (`27d`) | **140** | **5.19/d** | **78.95%** | **73.84%** (`14s / 19s`) | 1 |
| **13** | `cLKDiYP55J8` | *What Was the Edward Jenner Experiment?* | `2026-11-13` (`10d`) | **47** | **4.70/d** | 43.48% | 67.71% (`16s / 23s`) | 0 |
| **14** | `clV6E10NLPw` | *The spray that stopped surgery killing patients* | `2026-10-20` (`34d`) | **155** | **4.56/d** | 23.45% | 57.79% (`14s / 25s`) | 4 |
| **15** | `qOZgess30h0` | *Invisible life is still everywhere* | `2026-10-13` (`41d`) | **169** | **4.12/d** | 25.15% | 39.82% (`10s / 24s`) | 5 |
| **16** | `c2q7w0pgcn8` | *Who Discovered Infrared Light?* | `2026-10-19` (`35d`) | **138** | **3.94/d** | 43.52% | **105.30%** (`24s / 23s`) | 1 |
| **17** | `BW_CFAX-mxc` | *Is the Heart a Pump?* | `2026-10-31` (`23d`) | **89** | **3.87/d** | 32.91% | 81.69% (`18s / 22s`) | 1 |
| **18** | `Rl2uZ-KOTl8` | *Your Heart Pumps More Blood Than You Have* | `2026-10-30` (`24d`) | **78** | **3.25/d** | 26.58% | 53.64% (`13s / 25s`) | 4 |
| **19** | `xHnIi9GqOsM` | *Why Do Veins Have Valves?* | `2026-11-05` (`18d`) | **42** | **2.33/d** | 20.59% | 61.55% (`14s / 23s`) | 0 |
| **20** | `TbMMJSRKC3U` | *He said every eighth element repeats* | `2026-10-18` (`36d`) | **63** | **1.75/d** | 26.92% | 118.07% (`32s / 27s`) | 1 |
| **21** | `qW2OsD4mujc` | *The Four Elements Were Wrong* | `2026-11-03` (`20d`) | **34** | **1.70/d** | 57.69% | 192.62% (`46s / 24s`) | 0 |
| **22** | `LCZRHUyTiq0` | *What Are Cathode Rays?* | `2026-10-23` (`31d`) | **49** | **1.58/d** | 29.79% | 50.04% (`13s / 26s`) | 2 |
| **23** | `iqToagXnjX0` | *Microbes in a drop of pond water* | `2026-09-06` (`78d`) | **113** | **1.45/d** | 28.28% | 77.86% (`19s / 25s`) | 1 |
| **24** | `H1y0DXFVmw8` | *Germs don't cast a shadow* | `2026-09-06` (`78d`) | **80** | **1.03/d** | 19.75% | 59.46% (`15s / 25s`) | 1 |
| **25** | `ChbsigHD5_o` | *How Do Plants Clean the Air?* | `2026-11-18` (`5d`) | **5** | **1.00/d** | 100.00% | 36.12% (`9s / 25s`) | 0 |
| **26** | `xvanpsLeADE` | *How did Röntgen see bones without cutting* | `2026-09-26` (`58d`) | **40** | **0.69/d** | 23.33% | 50.33% (`13s / 25s`) | 0 |
| **27** | `xgx2lYHhYZM` | *Why Is It Called a Vaccine?* | `2026-11-17` (`6d`) | **4** | **0.67/d** | 100.00% | 62.41% (`16s / 25s`) | 0 |
| **28** | `oowAOWTBoq0` | *How X-rays Were Discovered by Accident* | `2026-09-25` (`59d`) | **32** | **0.54/d** | 47.62% | 331.08% (`83s / 25s`) | 1 |
| **29** | `nba0-f7PPeU` | *Why tellurium sat before iodine* | `2026-09-21` (`63d`) | **34** | **0.54/d** | 60.71% | 42.70% (`11s / 25s`) | 1 |
| **30** | `nFQRWmpulTQ` | *He predicted a metal before it was found* | `2026-09-19` (`65d`) | **34** | **0.52/d** | 66.67% | 55.91% (`14s / 25s`) | 0 |
| **31** | `8_Edn_HCi1s` | *Germs hitch a ride on you* | `2026-09-06` (`78d`) | **38** | **0.49/d** | 33.33% | 34.25% (`9s / 25s`) | 0 |
| **32** | `uU12JA5rMWg` | *The periodic table's empty chairs* | `2026-09-18` (`66d`) | **30** | **0.45/d** | 66.67% | 58.79% (`15s / 25s`) | 0 |
| **33** | `sILtQxgYQk8` | *A flask that proved germs come from outside* | `2026-09-06` (`78d`) | **24** | **0.31/d** | 41.67% | 36.70% (`9s / 25s`) | 0 |
| **34** | `CnHwX1L9XHg` | *Gallium sat where the table said* | `2026-09-20` (`64d`) | **16** | **0.25/d** | 30.43% | 33.45% (`9s / 26s`) | 0 |
| **35** | `zI_eD3vFWmE` | *The first X-ray showed a wedding ring* | `2026-09-27` (`57d`) | **9** | **0.16/d** | 50.00% | 64.00% (`16s / 25s`) | 0 |
| **36** | `LanTHJckYx8` | *What other table has empty chairs?* | `2026-09-22` (`62d`) | **4** | **0.06/d** | 33.33% | 23.08% (`6s / 26s`) | 0 |

- **3 Best HOS Shorts & What They Share:**
  1. **`29bpGAI0wb8` (*What happens if you keep cutting gold in half?*, `25s`):** **`32.34` views/day** (`1,229` views in `38d`, #1 mature HOS Short), `40.78%` stayed-to-watch, `44.14%` avg view %, `12` likes (while early `20h` read `el30-mHiH-0` *How Does the Heart Pump Blood?* hit `523` views / `523.0/d`, `66.41%` avg view %, `26.77%` stayed).
  2. **`-3L6HzJ_d_4` (*What Is the Pasteur Swan Neck Flask Experiment?*, `19s`):** **`5.19` views/day** (`140` views in `27d`), channel-best **`78.95%` stayed-to-watch (PASS `≥60%`)** and **`73.84%` avg view % (PASS `≥70%`)**, `129` 28d search views — first mature `100+` view HOS Short passing both bars (`Rules 28, 32, 41` & Ben 19 Nov `16–19s` house rules).
  3. **`xzKoHg0E0_U` (*What Is Dalton's Atomic Theory?*, `25s`):** **`34.14` views/day** (`239` views in `7d`, `197` search), **`53.13%` stayed-to-watch (WATCH)** and `61.49%` avg view % — alongside mature loop/retention winners `pWySvZsneZg` (`112.43%` LOOP), `c2q7w0pgcn8` (`105.30%` LOOP), and `oKqmnJNGiHg` (`88.35%` PASS).
  - **Shared pattern:** Positive named-entity search questions (`What Is...`, `Why...`, `How Was...`) outperform statements on stayed-to-watch (`40.8–78.95%` vs `15.35–16.67%`; `Rules 1, 28, 32, 41`), while tight `16–19 s` / zero-CTA loop cuts drive `73.8–112.4%` avg view % (`Rules 3, 6, 24, 27`).
- **3 Worst HOS Shorts & What They Share (Hypotheses on Small N):**
  1. **`LanTHJckYx8` (*What other table has empty chairs?*, `26s`):** **`0.06` views/day** (`4`v in `62d`), `33.33%` stayed, `23.08%` avg view %.
  2. **`zI_eD3vFWmE` (*The first X-ray showed a wedding ring*, `25s`):** **`0.16` views/day** (`9`v in `57d`), `50.00%` stayed, `64.00%` avg view %.
  3. **`CnHwX1L9XHg` (*Gallium sat where the table said*, `26s`):** **`0.25` views/day** (`16`v in `64d`), `30.43%` stayed, `33.45%` avg view %.
  - **Shared pattern:** Cryptic riddles and past-tense statements omit the searchable named entity, failing both feed stayed-to-watch and YouTube search (`Rules 1, 28, 32, 41`).

---

## 2. Overlap & Non-Duplication Check (`2026-11-24`)

Checked against:
- All folders in `02_Video-Projects/` on `main` (`000`–`018`, `099`–`119`),
- All open topic PRs in `history-of-science` (`#659` `120–121`, `#682` `122–123`, `#689` `124–125`, `#706` `126–127`, `#724` `128–129`, `#726` `130–131`, `#733` `132–133`), plus paired `134` (*What Is Antimatter?*),
- All `011`–`095` ideas in `00_Brand/Channel-Setup/ideas/`, `VIDEO_BACKLOG.json`, and `jobs/WIP.json` (`active` and `next_hos`).
- **Explicit separation from `ideas/024_Rumford-Joule-Thermodynamics`:** Inspected `024_Rumford-Joule-Thermodynamics/opening_and_outline_v00.md` directly — `024` covers the **First Law of Thermodynamics / Conservation of Energy** (Count Rumford's 1798 Munich cannon boring & James Prescott Joule's 1845–1849 Manchester paddle wheel), mentioning Clausius only in a single closing paragraph. `024` does **not** cover Sadi Carnot's 1824 steam-engine ideal cycle, Rudolf Clausius's 1865 coining of *Entropie*, Ludwig Boltzmann's 1877 statistical atom-counting law (`S = k log W`, carved on his Vienna tombstone), or Jean Perrin's 1908 Brownian-motion vindication of atoms.
- **Result:** **Zero overlap.**

---

## 3. Packaging, Why It Should Work & Search/Neighbour Evidence (`Rule 26` + `neighbours.py` + `public_search.py`)

- **Proposed 2027 Search Plan Fit (`J3224`, `needsBen`):** Bridges **Cluster 2 (Modern Physics Breakthroughs)** and **Cluster 4 (Breakthrough Engineering / Steam Engines)** — directly backed in `public_search.py` by `Science Retold` (`21,064` views on *How Entropy Was Discovered*, one of `J3224`'s verified `<50k` US breakout channels) and `Abide By Reason` (`1.31M`), while avoiding health throttling and school-syllabus traps.
- **Title A (Primary Proposal, `LEARNINGS.md` Rules 1, 15, 23, 26 — `50 chars ≤ 50`, `0` exact collisions):** `What Is Entropy? (Boltzmann's Gravestone Equation)`
- **Title B (Test & Compare Arm 2, `Rules 15, 23, 26` — `59 chars ≤ 70`, `0` exact collisions):** `What Is Entropy? (The Engine That Proved Time Runs One Way)`
- **Title C (Story+Stakes, `Rule 23` — `56 chars ≤ 70`, `0` exact collisions):** `Why Time Only Runs Forward (The 1824 Steam Engine Twist)`
- **One-Line Hook:** Trying to figure out why British steam engines outperformed French ones in 1824 led scientists to the most misunderstood law in physics — and to a lonely Viennese physicist whose simple equation for why time only flows forward was carved into his tombstone after rivals drove him to despair.
- **Why It Should Work (Past Winners & `LEARNINGS.md` Rules):**
  - Directly matches the search-question + high-demand physics profile of **`002` Periodic Table (`AL_-qlWko_g`, `162` views, `2.42/d`, `1,163` impressions, `3.35%` CTR)** and **`004` Inside an Atom (`GHZDsiH7L7A`, `35` views, `0.90/d`, `840` impressions)** by opening with the exact massive-demand query **`What Is Entropy?`** (`50 chars ≤ 50`, where `Veritasium` has `31.70M` views and `TED-Ed` has `5.09M` views; `Rules 1, 15, 26`), while pairing it with a vivid human & physical twist (`Boltzmann's Gravestone Equation` + `Carnot's 1824 Steam Engine`) like retention leader **`006` Willow Tree (`VbPubYd6Fbs`, `48.15%` Studio avg view %)** (`Rules 10, 23, 30`).
  - Mirrors top HOS Shorts **`29bpGAI0wb8` (`1,229`v, `32.34/d`)**, **`xzKoHg0E0_U` (`239`v, `34.14/d`, `53.13%` stayed, `197` search)**, **`-3L6HzJ_d_4` (`140`v, `78.95%` stayed PASS, `73.84%` avg view % PASS)**, and **`pWySvZsneZg` (`137`v, `112.43%` LOOP)** via two `16–19 s` named-entity search-question Shorts (`Rules 2, 3, 6, 8, 24, 27, 28, 32, 39, 41` + Ben 19 Nov Shorts house rules).
- **3-Way Thumbnail Test & Compare Plan (`LEARNINGS.md` Rules 11, 12, 14 + `THUMBNAIL_AND_TITLE_RULES.md` §2.5–2.B):**
  - **Thumb A (Hero Object — The Marble Tombstone & Scattering Atoms):** Painted 3D house-style key art: on the right two-thirds, a warm candle-lit stone monument carved with `S = k log W` as glowing golden gas spheres burst outward from one corner of a glass box into chaotic motion; Explorer small at lower left (round gold glasses, teal coat); cream/gold serif text in the clear left band: `TIME'S ARROW` (`2 words`, gold on `ARROW`, never repeats the title, zero overlap on the hero).
  - **Thumb B (`Rule 14` Bright High-Contrast Variant — Unmixable Cream in Coffee):** Bright sunlit Viennese café tabletop cutaway: a clear glass mug of dark coffee as a swirling white cloud of milk expands irreversibly outward beside a cracked pocket watch with its gears freezing backward; Explorer small at lower left; serif text on the clear left band: `NO REVERSE` (`2 words`, gold on `REVERSE`).
  - **Thumb C (Carnot's 1824 Brass Steam Cylinder):** Painted 3D cutaway of a gleaming 1824 brass steam engine piston glowing ember-red at the boiler end and icy blue at the condenser end, with a golden heat waterfall leaking out as waste steam; Explorer small at lower left; serif text on the clear left band: `HEAT'S TAX` (`2 words`, gold on `TAX`).
- **Signed-out YouTube Autocomplete (`2026-11-24`, `10` queries / `72` search rows in [`11_Upload-Package/evidence_2026-11-24_public_search.json`](11_Upload-Package/evidence_2026-11-24_public_search.json)):**
  - `"what is entropy"` → **`autocomplete = yes`** (`10` suggestions; `0` exact collisions across all `5` proposed long/Short titles)
  - `"how was entropy discovered"` → **`autocomplete = yes`**
  - `"second law of thermodynamics"` → **`autocomplete = yes`** (`10` suggestions)
  - `"ludwig boltzmann entropy"` → **`autocomplete = yes`**
  - `"why does time only go forward"` → **`related: why does time only move forward`**
- **Rule 26(a) Two Ranking Videos (`≥10,000` views, retrieved `2026-11-24`):**
  1. `Veritasium` — [`DxL2HoqLbyA`](https://youtu.be/DxL2HoqLbyA) *The Most Misunderstood Concept in Physics* (**`31,701,440` views**)
  2. `Abide By Reason` — [`WI0ZLkxJ6Zk`](https://youtu.be/WI0ZLkxJ6Zk) *How Entropy Was Discovered* (**`1,307,580` views**; plus `TED-Ed` [`YM-uykVfq_E`](https://youtu.be/YM-uykVfq_E) **`5,090,744` views**, `BBC` **`4,290,796` views**, `Big Think and Sean Carroll` **`1,223,064` views**, `The Organic Chemistry Tutor` **`825,828` views**, `The Royal Institution` **`609,319` views**, `Physics Explained` **`504,409` views**, `Kathy Loves Physics` **`340,807` views**, and `Science Retold` **`21,064` views**)
- **Neighbour Gate (`neighbours.py "what is entropy" "entropy physics" "second law of thermodynamics" "boltzmann entropy" --top 25`):** **PASS (`7` raw / `6` strictly on-topic Entropy & Second Law education videos `≥1,000,000` views + `1` adjacent thermodynamics video `Khan Academy` *Enthalpy* `1.56M`, `TED-Ed/TED: yes`)** — saved in [`11_Upload-Package/evidence_2026-11-24_neighbours.json`](11_Upload-Package/evidence_2026-11-24_neighbours.json):
  1. `Veritasium` — [`DxL2HoqLbyA`](https://youtu.be/DxL2HoqLbyA) *The Most Misunderstood Concept in Physics* (**`31,701,405` views**, strictly on-topic)
  2. `TED-Ed` ★ — [`YM-uykVfq_E`](https://youtu.be/YM-uykVfq_E) *What is entropy? - Jeff Phillips* (**`5,090,744` views**, strictly on-topic)
  3. `CrashCourse` — [`4i1MUWJoI0U`](https://youtu.be/4i1MUWJoI0U) *Thermodynamics: Crash Course Physics #23* (**`2,050,142` views**, strictly on-topic)
  4. `CrashCourse` — [`ZsY4WcQOrfk`](https://youtu.be/ZsY4WcQOrfk) *Entropy: Embrace the Chaos! Crash Course Chemistry #20* (**`2,033,809` views**, strictly on-topic)
  5. `TED-Ed` ★ — [`OpohbXB_JZU`](https://youtu.be/OpohbXB_JZU) *The Boltzmann brain paradox - Fabio Pacucci* (**`1,399,583` views**, strictly on-topic)
  6. `PBS Space Time` — [`kfffy12uQ7g`](https://youtu.be/kfffy12uQ7g) *The Misunderstood Nature of Entropy* (**`1,268,850` views**, strictly on-topic)
  7. *(Adjacent thermodynamics row, transparently noted, not needed for PASS)* `Khan Academy` — [`fucyI7Ouj2c`](https://youtu.be/fucyI7Ouj2c) *Enthalpy | Thermodynamics | Chemistry | Khan Academy* (**`1,559,665` views**; plus strictly on-topic `The Science Asylum` [`ykUmibZHEZk`](https://youtu.be/ykUmibZHEZk) **`734,736` views**, `Khan Academy` [`xQ9D4Jz95-A`](https://youtu.be/xQ9D4Jz95-A) **`635,540` views**, `The Royal Institution` [`mGDJO2M7RBg`](https://youtu.be/mGDJO2M7RBg) *What is the Second Law of Thermodynamics?* **`609,319` views**, and `Khan Academy` [`PFcGiMLwjeY`](https://youtu.be/PFcGiMLwjeY) **`442,596` views**)

---

## 4. Candidate 4-Act Discovery Outline (All Claims UNVERIFIED Pending `SOURCES.md` & `facts` Lane)

- **Cold Open (0:00–0:45, Proof-First Apparatus Window per `Rules 10 & 30`, UNVERIFIED):**
  - `0:00–0:05`: A drop of white cream hits black coffee and swirls apart, a glass shatters on stone, and an 1824 brass steam engine leaks heat into cold air — none of which ever runs in reverse, even though Newton's laws of motion work identically backward and forward.
  - `0:05–0:15` (Apparatus / Physical Proof): Hard cut directly to **Sadi Carnot**'s 1824 ideal hot-to-cold piston diagram dissolving into **Ludwig Boltzmann**'s glass chamber of colliding gas spheres spreading from one corner across the entire room — showing visually that **entropy** is not a mysterious "disorder fluid", but the sheer mathematical probability of how many ways energy can spread out. Zero *"In this film..."* agenda line.
- **Act I — Sadi Carnot's 1824 Steam-Engine Waterfall (1824, UNVERIFIED):** After Napoleon's defeat, 28-year-old French military engineer **Nicolas Léonard Sadi Carnot** wonders why British coal-fired steam engines crush French industry. In his **June 1824** self-published booklet *Reflections on the Motive Power of Fire*, Carnot compares a steam engine to a waterwheel: just as water only turns a wheel by falling from high to low, heat can only do mechanical work by flowing from a **hot boiler** to a **cold condenser** — setting a hard universal ceiling on engine efficiency (`1 - T_cold / T_hot`) that no engineer can ever beat. Twist: Carnot got the law right even while believing heat was an indestructible fluid ("caloric")! He died of cholera at `36` in **1832** with almost all his papers burned.
- **Act II — Rudolf Clausius Names the One-Way Tax "Entropy" (1850–1865, UNVERIFIED):** In **1850**, German physicist **Rudolf Clausius** reconciles Carnot's efficiency limit with Joule's new proof that heat *is* energy, formulating the **Second Law of Thermodynamics** (heat never flows spontaneously from a colder body to a hotter one). In **1865** (*Annalen der Physik* `125:353–400`), Clausius coins the Greek-rooted word **Entropie** ("transformation") and summarizes the cosmos in two immortal lines: *"The energy of the universe is constant; the entropy of the universe tends to a maximum."*
- **Act III — Ludwig Boltzmann's Atom-Counting Revolution & Rival War (1877–1906, UNVERIFIED):** Why must entropy always climb? In **1877**, Austrian physicist **Ludwig Boltzmann** in Vienna connects thermodynamics to **atoms** and probability: there are astronomically more microscopic ways (`W`) for fast and slow molecules to share energy evenly across a room than to huddle in one hot corner. Entropy is simply proportional to the logarithm of those possible arrangements (`S = k log W`, later written in that exact notation by **Max Planck** in **1900**). Midpoint twist ("Case closed? Wrong."): powerful European philosophers and physicists led by **Ernst Mach** and **Wilhelm Ostwald** fiercely deny that atoms even exist, mocking Boltzmann's statistical proof until exhaustion and depression claim his life in **September 1906** in Duino, Italy.
- **Act IV — Jean Perrin's 1908 Vindication & the Vienna Gravestone (1908–1933, UNVERIFIED):** Just **two years** after Boltzmann's death, French physicist **Jean Perrin** (**1908–1909**, guided by Einstein's 1905 Brownian-motion math) tracks microscopic resin grains dancing in water and measures **Avogadro's number**, proving atoms are physically real and vindicating Boltzmann completely. When Vienna unveils Boltzmann's marble monument in the Central Cemetery (**1933**), they chisel his probability equation — **`S = k log W`** — directly above his bust: the law that explains why engines waste heat, why stars burn out, and why yesterday can never happen again.
- **Primary-Source Verification Guardrails (Mandatory Before Script Lock):**
  1. **Carnot (`June 1824`, *Réflexions sur la puissance motrice du feu*):** Verify exact age (`28`), publication year (`1824`), waterwheel analogy, and cholera death date (`24 August 1832`, age `36`).
  2. **Clausius (`1850`, *Ann. Phys.* `79:368–397`; `1865`, *Ann. Phys.* `125:353–400`):** Verify exact 1865 coining of *Entropie* and verbatim two-sentence summary.
  3. **Boltzmann (`1877`, *Wiener Berichte* `76:373–435`) & Planck (`1900`):** Verify exact statistical microstate derivation (`W`), clarify that Max Planck introduced the constant `k` and compact `S = k log W` notation in 1900, and verify Boltzmann's death date (`5 September 1906`) and Vienna Zentralfriedhof monument unveiling (`1933`).
  4. **Perrin (`1908–1909`, *Annales de Chimie et de Physique* `18:5–114`):** Verify exact Brownian-motion Avogadro verification and 1926 Nobel citation.

---

## 5. Two Candidate `16–19 s` Search-Titled Shorts (Ben 19 Nov 2026 Shorts House Rules + Rules 32 & 41 — UNVERIFIED)

- **Short `S01`:** *Why Is S = k log W Carved on Boltzmann's Tombstone?* (`51 chars`, `0` exact collisions, named-scientist + formula search question)
  - **First-line answer hook (`0.0–1.5s`, `vo_onset_s ≤ 0.15s`, zero calendar dateline, UNVERIFIED):** *"Ludwig Boltzmann's tombstone carries the equation that explains why time only flows forward — yet rivals mocked it until he died."*
  - **Frame-0, Caption, Overlay & `16–19 s` Loop Plan (`studio/RULES.md` Shorts house rules + Rules 2, 3, 6, 24, 27, 39, 41):** Frame 0 (`0.0s`, `mode: "cover"`, `0%` Explorer, `0%` bars): **premium 3D cartoon moving plate** (no archival photo/still) pushing across warm chiselled marble lettering `S = k log W` as glowing gas spheres burst outward behind it. Line-1 caption carries the concrete fact (`This gravestone equation proves why time moves one way`, yellow on `gravestone equation`). Single mid-Short `Teach on screen` overlay (`WHEN` stamp inside `16:9` centre band, clear of `0–2s` and `9–14s`): `VIENNA, 1877`. Target runtime **`17.5 s`** (`16.0–19.0 s` band); payoff start at `≥70%` (`~12.5 s`): `W` counts the hidden ways atoms can arrange themselves — and two years after Boltzmann's death, Brownian-motion experiments proved his atoms were real. Last line loops directly into sentence 1 (`≤0.3 s` visual frame-0 match, zero CTA).
- **Short `S02`:** *How Did Sadi Carnot Discover Entropy?* (`37 chars`, `0` exact collisions, named-scientist + concept search question)
  - **First-line answer hook (`0.0–1.5s`, `vo_onset_s ≤ 0.15s`, zero calendar dateline, UNVERIFIED):** *"The law of entropy was discovered by a 28-year-old engineer trying to beat British steam engines — using a totally wrong theory of heat."*
  - **Frame-0, Caption, Overlay & `16–19 s` Loop Plan (`studio/RULES.md` Shorts house rules + Rules 2, 3, 6, 24, 27, 39, 41):** Frame 0 (`0.0s`, `mode: "cover"`, `0%` Explorer, `0%` bars): **premium 3D cartoon moving plate** of a glowing brass 1824 steam-engine piston pumping between a fiery boiler and an icy condenser as shimmering heat escapes. Line-1 caption carries the concrete fact (`A steam engine revealed time's one-way heat tax`, yellow on `one-way heat tax`). Single mid-Short `Teach on screen` overlay (`WHEN` stamp inside `16:9` centre band): `PARIS, 1824`. Target runtime **`17.5 s`** (`16.0–19.0 s` band); payoff start at `≥70%` (`~12.6 s`): Sadi Carnot proved heat only does work by falling from hot to cold, setting an unbreakable efficiency limit that Rudolf Clausius later named entropy. Last line loops directly into sentence 1 (`≤0.3 s` visual frame-0 match, zero CTA).
