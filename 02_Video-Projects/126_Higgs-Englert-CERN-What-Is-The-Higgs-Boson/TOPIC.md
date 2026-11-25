# Topic Brief — `126_Higgs-Englert-CERN-What-Is-The-Higgs-Boson` (`HOS:126` · Rule-E GO in `next_hos`)

> **RULE-E GO & RULE G STATUS (`J3263`, `2026-11-21` — `96.1 / 100`):**
> - **Status:** Proposed in `J3245` and pre-cleared by `J3263` Rule-E topic go/no-go review (**GO**, `9.61 / 10` Opportunity Score; see [`11_Upload-Package/TOPIC_GO_NO_GO_SHEET.md`](11_Upload-Package/TOPIC_GO_NO_GO_SHEET.md) & [`11_Upload-Package/TOPIC_OPPORTUNITY_SCORE.md`](11_Upload-Package/TOPIC_OPPORTUNITY_SCORE.md)). Remains in `jobs/WIP.json` `next_hos` under **Rule G** (`active` has `4 / 4` HOS slots full: `008`, `009`, `010`, `013`). Nothing is started in production (`status.json` stages are all `todo`; `£0.00` spent).
> - **2027 Search Plan Alignment (`J3224`, currently `needsBen` in `studio/plan.json`):** `HOS:126` independently passes all currently in-force HOS topic gates (`neighbours.py`, `public_search.py`, `LEARNINGS.md` Rules 1, 15, 23, 26) and also aligns with **proposed** Cluster 2 (*Nuclear, Quantum & Modern Physics Breakthroughs*) from `05_Analytics/hos/search_research/2026-11-20.md` (`the god particle`: `19,705` est. monthly searches, comp `42`, `+89.8%` growth, `9/10` US SERP gap, verified sub-50k US breakouts `Science Retold` 3.4K → `61.9K` 13× & `Cosmo Explains` 37K → `239.7K` 65×; plan still waiting for Ben's OK under Rule 34 item 7).
> - **Awaits Active HOS Slot, `SOURCES.md` & `facts` Lane:** All historical and scientific claims in this brief are **UNVERIFIED** working notes. Before any script is locked, VO is recorded, or picture credit is spent, every claim must be backed by verbatim primary-source quotes in `SOURCES.md` and verified through the `facts` lane (`gemini-agy`).

---

## 1. HOS Data Comparison (`2026-11-20` Snapshot + `studio_ctr.json` + `channel_daily.json`)

- **Data sources read:**
  - `05_Analytics/hos/snapshots/2026-11-20.json` (`takenAt: 2026-11-20T06:40:34.014Z`, `40` public videos = `7` longs + `33` Shorts, `4,387` total views, `6` subscribers)
  - `05_Analytics/hos/studio_ctr.json` (`readAt: 2026-11-20T07:16:24.533881+00:00`, lifetime Studio impressions, CTR, average view %, and Shorts stayed-to-watch %)
  - `05_Analytics/hos/channel_daily.json` (`through: 2026-11-18`, `84` daily rows; peak days `2026-10-16` `1,173` views / `105` min, `2026-11-15` `223` views, `2026-11-08` `216` views, `2026-10-26` `207` views) and `05_Analytics/hos/REPORT.md`
  - `05_Analytics/LEARNINGS.md` (rules `1–22`, plus active HOS rules `23–38`) and `05_Analytics/hos/search_research/2026-11-20.md` (`J3224`)
- **Elapsed-day denominator (`age_days`):** `max((date(2026, 11, 20) - date.fromisoformat(publishedAt[:10])).days, 1)` (`views/day = views / age_days`).
- **Small-sample caveat (`Rule 1`):** Five of the seven public HOS longs have `5–14` lifetime views (`17–64` impressions), and bottom-tier Shorts have `3–24` views. Metrics on `<100`-view videos are descriptive hypotheses, not settled proof.

### 1a. All `7` Public HOS Longs — Ranked by Views/Day Since Publish (`2026-11-20`)

| Rank | Video ID | Film | Title | Published (`age_days`) | Length | Views (`11-20`) | Views / Day | Studio Impressions | Studio CTR | Studio Avg View % (Lifetime) | YTA Lifetime Avg View % |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **1** | `AL_-qlWko_g` | `002` | *How Did We Discover the Periodic Table?* | `2026-09-17` (`64d`) | `541s` | **162** | **2.53/d** | **1,139** | 3.4% | 21.0% (`114s`) | 21.23% |
| **2** | `GHZDsiH7L7A` | `004` | *What's Inside an Atom? Mostly Empty Space* | `2026-10-15` (`36d`) | `525s` | **35** | **0.97/d** | **840** | 1.4% | 23.0% (`128s`) | 23.54% |
| **3** | `VbPubYd6Fbs` | `006` | *The Willow Tree That Was Made of Air* | `2026-11-05` (`15d`) | `532s` | **14** | **0.93/d** | 64 | 4.7% | **48.12%** (`256s`) | **53.96%** |
| **4** | `ETynHpIYLeY` | `007` | *How Was the First Vaccine Made? (And Why It's Named After a Cow)* | `2026-11-12` (`8d`) | `532s` | **7** | **0.88/d** | 44 | 4.6% | 19.17% (`102s`) | 28.49% |
| **5** | `wwcjcFfC-5M` | `005` | *The Tied Arm That Proved Your Blood Circulates* | `2026-10-29` (`22d`) | `529s` | **6** | **0.27/d** | **17** | 17.6% | **7.75%** (`41s`) | **9.24%** |
| **6** | `_C92tIJCk8A` | `001` | *How Did We Discover Germs?* | `2026-09-03` (`78d`) | `365s` | **7** | **0.09/d** | 41 | 7.3% | 47.95% (`175s`) | 48.08% |
| **7** | `frP_YrNShsU` | `003` | *How Did We Discover X-rays?* | `2026-09-24` (`57d`) | `426s` | **5** | **0.09/d** | 40 | 2.5% | 26.53% (`113s`) | 26.65% |

- **3 Best HOS Longs & What They Share:**
  1. **`AL_-qlWko_g` (`002` *How Did We Discover the Periodic Table?*, `541s` / 9:01)** — **`2.53` views/day** (`162` views in `64d`), **`1,139` impressions** (`52.1%` of all HOS long impressions), `3.4%` CTR, `21.0%` Studio avg view % (`50%` at `0:30`).
  2. **`GHZDsiH7L7A` (`004` *What's Inside an Atom? Mostly Empty Space*, `525s` / 8:45)** — **`0.97` views/day** (`35` views in `36d`), **`840` impressions** (`38.4%` of all HOS long impressions), `1.4%` CTR, `23.0%` Studio avg view % (`45%` at `0:30`).
  3. **`VbPubYd6Fbs` (`006` *The Willow Tree That Was Made of Air*, `532s` / 8:52)** — **`0.93` views/day** (`14` views in `15d`, low-N), `64` impressions, `4.7%` CTR, channel-best **`48.12%` Studio / `53.96%` YTA avg view %**.
  - **Shared pattern:**
    - *Subject:* Iconic physics/chemistry discovery questions (`Periodic Table`, `Atom`) backed by massive TED-Ed/education neighbour pools (`002` and `004` capture **`90.6%` (`1,979 / 2,185`) of all HOS long impressions** and **`83.5%` (`197 / 236`) of all HOS long views**).
    - *Title shape:* Direct searchable question naming the core subject (`How Did We Discover the Periodic Table?`, `What's Inside an Atom? Mostly Empty Space`) — matching `LEARNINGS.md` Rules 1, 15 & 26.
    - *Opening:* Concrete physical paradox/object in the first 15 s (`Rule 10`; `006`'s willow-tree weight paradox holds `48–54%` avg view %; `002`/`004` hold `45–50%` at `0:30`, still leaving room to lift `0:30` via proof-first apparatus openings without agenda lines per `Rule 38`).
    - *Thumbnail concept:* Warm 3D painted hero object on the right (gallium/table, glowing atom, weighted willow) with small Explorer lower left and clear left-band cream/gold serif hook text (`Rules 12, 14`).
    - *Length:* **`8:45–9:01` (`525–541s`)** — every top-3 long sits in the 8.5–9 min band.
- **3 Worst HOS Longs & What They Share (Small-N Hypotheses):**
  1. **`frP_YrNShsU` (`003` *How Did We Discover X-rays?*, `426s` / 7:06)** — **`0.09` views/day** (`5` views in `57d`), `40` impressions, `2.5%` CTR, `26.53%` Studio avg view %.
  2. **`_C92tIJCk8A` (`001` *How Did We Discover Germs?*, `365s` / 6:05)** — **`0.09` views/day** (`7` views in `78d`), `41` impressions, `7.3%` CTR, `47.95%` Studio avg view %.
  3. **`wwcjcFfC-5M` (`005` *The Tied Arm That Proved Your Blood Circulates*, `529s` / 8:49)** — **`0.27` views/day** (`6` views in `22d`), **`17` impressions** (channel bottom), `17.6%` CTR (3 clicks / 17 impr), **`7.75%` Studio avg view % (`41s`)**.
  - **Shared pattern:** `005` used a literary statement title (`The Tied Arm...`) with no searchable phrase (`Rule 26` miss), getting only `17` impressions and `7.75%` retention; `001` (`365s`) and `003` (`426s`) were shorter early Premieres with generic survey titles (`How Did We Discover...`) and no concrete stakes/twist in the title (`Rules 11, 15, 23`). (Note: `007` *First Vaccine*, `44` impr / `7` views / `0.88/d`, also confirms `J3224`'s warning against health/vaccine topics due to zero Suggested distribution.)

### 1b. All `33` Public HOS Shorts — Ranked by Views/Day Since Publish (`2026-11-20`)

| Rank | Video ID | Title | Published (`age_days`) | Len | Views (`11-20`) | Views / Day | Studio Stayed % | Studio Avg View % | Likes |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|
| **1** | `xzKoHg0E0_U` | *What Is Dalton's Atomic Theory?* | `2026-11-16` (`4d`) | `25s` | **208** | **52.00/d** | **52.0%** | 60.0% (`15s`) | 0 |
| **2** | `Wvjd8g0CpzE` | *The Blood Vessels Finer Than a Hair* | `2026-11-15` (`5d`) | `26s` | **215** | **43.00/d** | 14.6% | **76.0%** (`19s`) | 3 |
| **3** | `29bpGAI0wb8` | *What happens if you keep cutting gold in half?* | `2026-10-16` (`35d`) | `25s` | **1,228** | **35.09/d** | 40.8% | 44.0% (`11s`) | 12 |
| **4** | `PFj6172YU4Q` | *One Tight Band Proved Your Blood Goes Round* | `2026-11-08` (`12d`) | `27s` | **221** | **18.42/d** | 16.7% | 61.0% (`16s`) | 3 |
| **5** | `AMSriTQ-lcQ` | *Are Marie Curie's Notebooks Still Radioactive?* | `2026-10-28` (`23d`) | `22s` | **274** | **11.91/d** | 22.7% | **76.0%** (`16s`) | 6 |
| **6** | `OnJ8MFu0Mi0` | *How Did John Snow Stop Cholera?* | `2026-10-26` (`25d`) | `23s` | **231** | **9.24/d** | 29.6% | 65.0% (`15s`) | 8 |
| **7** | `pWySvZsneZg` | *Why Gold Foil Bounced Rutherford's Particles Back* | `2026-11-01` (`19d`) | `25s` | **137** | **7.21/d** | 37.2% | **112.0%** (`28s`) | 2 |
| **8** | `oKqmnJNGiHg` | *How Was Phosphorus Discovered?* | `2026-10-21` (`30d`) | `23s` | **193** | **6.43/d** | 42.0% | **87.0%** (`20s`) | 7 |
| **9** | `cLKDiYP55J8` | *What Was the Edward Jenner Experiment?* | `2026-11-13` (`7d`) | `23s` | **43** | **6.14/d** | 40.9% | 64.0% (`14s`) | 0 |
| **10** | `-3L6HzJ_d_4` | *What Is the Pasteur Swan Neck Flask Experiment?* | `2026-10-27` (`24d`) | `19s` | **138** | **5.75/d** | **78.7%** | **74.0%** (`14s`) | 1 |
| **11** | `clV6E10NLPw` | *The spray that stopped surgery killing patients* | `2026-10-20` (`31d`) | `25s` | **155** | **5.00/d** | 23.4% | 57.0% (`14s`) | 4 |
| **12** | `BW_CFAX-mxc` | *Is the Heart a Pump?* | `2026-10-31` (`20d`) | `22s` | **89** | **4.45/d** | 32.9% | 81.0% (`17s`) | 1 |
| **13** | `qOZgess30h0` | *Invisible life is still everywhere* | `2026-10-13` (`38d`) | `24s` | **169** | **4.45/d** | 25.2% | 39.0% (`9s`) | 5 |
| **14** | `c2q7w0pgcn8` | *Who Discovered Infrared Light?* | `2026-10-19` (`32d`) | `23s` | **138** | **4.31/d** | **43.5%** | **105.0%** (`24s`) | 1 |
| **15** | `Rl2uZ-KOTl8` | *Your Heart Pumps More Blood Than You Have* | `2026-10-30` (`21d`) | `25s` | **78** | **3.71/d** | 26.6% | 53.0% (`13s`) | 4 |
| **16** | `xHnIi9GqOsM` | *Why Do Veins Have Valves?* | `2026-11-05` (`15d`) | `23s` | **42** | **2.80/d** | 20.6% | 60.87% (`14s`) | 0 |
| **17** | `qW2OsD4mujc` | *The Four Elements Were Wrong* | `2026-11-03` (`17d`) | `24s` | **34** | **2.00/d** | 57.7% | 192.0% (`46s`) | 0 |
| **18** | `TbMMJSRKC3U` | *He said every eighth element repeats* | `2026-10-18` (`33d`) | `27s` | **62** | **1.88/d** | 25.5% | 123.0% (`33s`) | 1 |
| **19** | `LCZRHUyTiq0` | *What Are Cathode Rays?* | `2026-10-23` (`28d`) | `26s` | **49** | **1.75/d** | 29.8% | 50.0% (`13s`) | 2 |
| **20** | `iqToagXnjX0` | *Microbes in a drop of pond water* | `2026-09-06` (`75d`) | `25s` | **113** | **1.51/d** | 28.3% | 77.0% (`19s`) | 1 |
| **21** | `ChbsigHD5_o` | *How Do Plants Clean the Air?* | `2026-11-18` (`2d`) | `25s` | **3** | **1.50/d** | — | 8.0% (`2s`) | 0 |
| **22** | `xgx2lYHhYZM` | *Why Is It Called a Vaccine?* | `2026-11-17` (`3d`) | `25s` | **4** | **1.33/d** | 100.0% | 60.0% (`15s`) | 0 |
| **23** | `H1y0DXFVmw8` | *Germs don't cast a shadow* | `2026-09-06` (`75d`) | `25s` | **80** | **1.07/d** | 19.8% | 59.0% (`14s`) | 1 |
| **24** | `xvanpsLeADE` | *How did Röntgen see bones without cutting* | `2026-09-26` (`55d`) | `25s` | **40** | **0.73/d** | 23.3% | 48.0% (`12s`) | 0 |
| **25** | `oowAOWTBoq0` | *How X-rays Were Discovered by Accident* | `2026-09-25` (`56d`) | `25s` | **32** | **0.57/d** | 47.6% | 331.0% (`82s`) | 1 |
| **26** | `nba0-f7PPeU` | *Why tellurium sat before iodine* | `2026-09-21` (`60d`) | `25s` | **34** | **0.57/d** | 60.7% | 42.0% (`10s`) | 1 |
| **27** | `nFQRWmpulTQ` | *He predicted a metal before it was found* | `2026-09-19` (`62d`) | `25s` | **34** | **0.55/d** | 66.7% | 55.0% (`13s`) | 0 |
| **28** | `8_Edn_HCi1s` | *Germs hitch a ride on you* | `2026-09-06` (`75d`) | `25s` | **36** | **0.48/d** | 32.3% | 36.0% (`9s`) | 0 |
| **29** | `uU12JA5rMWg` | *The periodic table's empty chairs* | `2026-09-18` (`63d`) | `25s` | **30** | **0.48/d** | 66.7% | 58.0% (`14s`) | 0 |
| **30** | `sILtQxgYQk8` | *A flask that proved germs come from outside* | `2026-09-06` (`75d`) | `25s` | **24** | **0.32/d** | 41.7% | 36.0% (`9s`) | 0 |
| **31** | `CnHwX1L9XHg` | *Gallium sat where the table said* | `2026-09-20` (`61d`) | `26s` | **16** | **0.26/d** | 30.4% | 30.77% (`8s`) | 0 |
| **32** | `zI_eD3vFWmE` | *The first X-ray showed a wedding ring* | `2026-09-27` (`54d`) | `25s` | **9** | **0.17/d** | 50.0% | 64.0% (`16s`) | 0 |
| **33** | `LanTHJckYx8` | *What other table has empty chairs?* | `2026-09-22` (`59d`) | `26s` | **4** | **0.07/d** | 33.3% | 23.08% (`6s`) | 0 |

- **3 Best HOS Shorts (Balancing Views/Day, Stayed % & Avg View % on `≥100`-View Mature Shorts) & What They Share:**
  1. **`29bpGAI0wb8` (*What happens if you keep cutting gold in half?*, `25s`)** — **`35.09` views/day** (`1,228` views in `35d`, #1 HOS video overall), `40.8%` stayed-to-watch, `44.0%` avg view %, `12` likes.
  2. **`-3L6HzJ_d_4` (*What Is the Pasteur Swan Neck Flask Experiment?*, `19s`)** — **`5.75` views/day** (`138` views in `24d`), channel-best **`78.7%` stayed-to-watch (PASS `≥60%`)** and **`74.0%` avg view % (PASS `≥70%`)** — the only mature `≥100`-view HOS Short to pass both targets (`19s` tight cut matching Ben's 19 Nov `16–19s` Shorts house lock!).
  3. **`xzKoHg0E0_U` (*What Is Dalton's Atomic Theory?*, `25s`)** & **`oKqmnJNGiHg` (*How Was Phosphorus Discovered?*, `23s`)** / **`c2q7w0pgcn8` (*Who Discovered Infrared Light?*, `23s`)** — `xzKoHg0E0_U` leads velocity at **`52.00/d`** (`208` views in `4d`, **`52.0%` stayed**, `60.0%` avg viewed, search-led), while `oKqmnJNGiHg` (`6.43/d`, `193`v, `42.0%` stayed, **`87.0%` PASS**), `pWySvZsneZg` (`7.21/d`, `137`v, `37.2%` stayed, **`112.0%` LOOP**), and `c2q7w0pgcn8` (`4.31/d`, `138`v, **`43.5%` stayed**, **`105.0%` LOOP**) prove that positive search questions + tight `<1.0s` loop tails drive both stayed-to-watch and rewatch loops. By contrast, high-feed statement Shorts `Wvjd8g0CpzE` (`43.0/d`, `14.6%` stayed MISS) and `PFj6172YU4Q` (`18.42/d`, `16.7%` stayed MISS) collapse on cold-feed stayed-to-watch.
  - **Shared pattern:** Direct positive search questions naming a concrete physics/chemistry object or experiment (`What Is...`, `What happens if...`, `How Was...`, `Who Discovered...`, `Why...`), moving hero object at frame 0, payoff held past `≥70%`, zero CTA, and tight **`16–19s` loop runtime** (Ben's 19 Nov Shorts house rules; `LEARNINGS.md` Rules 1, 2, 3, 6, 8, 24, 27, 28, 32).
- **3 Worst HOS Shorts & What They Share:**
  1. **`LanTHJckYx8` (*What other table has empty chairs?*, `26s`)** — **`0.07` views/day** (`4` views in `59d`), `33.3%` stayed, `23.08%` avg view %.
  2. **`zI_eD3vFWmE` (*The first X-ray showed a wedding ring*, `25s`)** — **`0.17` views/day** (`9` views in `54d`), `50.0%` stayed, `64.0%` avg view %.
  3. **`CnHwX1L9XHg` (*Gallium sat where the table said*, `26s`)** — **`0.26` views/day** (`16` views in `61d`), `30.4%` stayed, `30.77%` avg view %.
  - **Shared pattern:** Cryptic riddles (*empty chairs*) and flat past-tense statements (*Gallium sat...*, *The first X-ray showed...*) omit the searchable subject question, run `25–26s` with slow holds, and fail both search discovery and Shorts-feed retention (`Rules 1, 2, 3, 28, 32`).

---

## 2. Overlap & Non-Duplication Check (`2026-11-21`)

Checked across:
- All folders in `02_Video-Projects/` (`000`–`018`, `099`–`119` on `main`),
- Open HOS backlog PRs (`#682`–`#692` & OWB `#1033`/`#1051`/`#1059`): `120` *Why Do We Cry?*, `121` *Why Do Cats Purr?*, `122` *Why Do We Sneeze?*, `123` *Why Does Hair Turn Grey?*, `124` *Why Is the Ocean Salty?*, `125` *What Causes the Tides?*,
- All `011`–`095` ideas folders and `IDEAS_*.md` files under `00_Brand/Channel-Setup/ideas/`, `VIDEO_BACKLOG.json`, and `jobs/WIP.json` (`active` + `next_hos`).
- Note: `004_Whats-Really-Inside-An-Atom` covers Democritus, Dalton, Thomson (electrons), and Rutherford's 1909 gold-foil nucleus; `ideas/022_Meitner-Hahn-Nuclear-Fission` covers uranium fission (1938); `ideas/023_Becquerel-Curie-Radioactivity` covers radioactivity (1896–1898). **None** cover Peter Higgs / François Englert & Robert Brout / Guralnik–Hagen–Kibble (1964), electroweak symmetry breaking, CERN's Large Hadron Collider (4 July 2012), Leon Lederman's "God particle" naming twist, or why 99% of your body's mass comes from strong-force binding energy rather than the Higgs boson.
- **Result:** **Zero overlap.**

---

## 3. Packaging, Why It Should Work & Search/Neighbour Evidence (`Rule 26` + `J3224` + `neighbours.py` + `public_search.py`)

- **Title A (Primary Proposal, `LEARNINGS.md` Rules 1, 15, 23, 26 — `43 chars ≤ 50`, `0` exact collisions):** `What Is the Higgs Boson? (The 48-Year Hunt)`
- **Title B (Test & Compare Arm 2, `J3224` High-Growth Phrase `+89.8%` + `Rules 15, 23` — `46 chars ≤ 50`, `0` exact collisions):** `The God Particle: The 1964 Paper They Rejected`
- **Title C (`Rule 26` Exact Phrase + CERN Proof — `53 chars ≤ 70`, `0` exact collisions):** `What Is the Higgs Boson? (The 1964 Paper CERN Proved)`
- **One-Line Hook:** In 1964 a physics journal rejected Peter Higgs's paper as having "no obvious relevance to physics" — yet 48 years and a 27-kilometre superconducting collider later, CERN proved his invisible field existed, and revealed the twist that 99% of your body's mass does not even come from it.
- **Why It Should Work (Past Winners, `LEARNINGS.md` Rules & `J3224` Search Demand):**
  - Resembles HOS's #1 and #2 longs **`002` Periodic Table (`AL_-qlWko_g`, `162` views, `2.53/d`, `1,139` impressions, `3.4%` CTR)** and **`004` Inside an Atom (`GHZDsiH7L7A`, `35` views, `0.97/d`, `840` impressions)** — both foundational chemistry/physics search questions with huge education neighbour pools (`002` + `004` = `90.6%` of all HOS long impressions) — while adding a concrete historical stakes tail (`The 48-Year Hunt` / `The 1964 Paper They Rejected`) so CTR improves over `004`'s `1.4%` (`Rules 1, 11, 15, 23, 26`).
  - Matches our best physics/chemistry Shorts **`29bpGAI0wb8` (*What happens if you keep cutting gold in half?*, `1,228` views, `35.09/d`)**, **`xzKoHg0E0_U` (*What Is Dalton's Atomic Theory?*, `52.00/d`, `52.0%` stayed)**, **`pWySvZsneZg` (*Why Gold Foil Bounced Rutherford's Particles Back*, `112.0%` avg viewed LOOP)**, and **`-3L6HzJ_d_4` (`19s`, `78.7%` stayed PASS, `74.0%` avg viewed PASS)** (`Rules 1, 2, 3, 6, 8, 24, 27, 28, 32`).
  - Aligns with the proposed `2026-11-20` search plan (`J3224`, `05_Analytics/hos/search_research/2026-11-20.md` Cluster 2; currently `needsBen` in `studio/plan.json`, not yet approved by Ben): `the god particle` averages `19,705` searches/mo at comp `42` with **`+89.8%` growth** and a `9/10` US SERP gap, with sub-50k US science-history channels breaking out massively (`Science Retold` 3.4K US → `61.9K` 13×; `Cosmo Explains` 37K US → `239.7K` 65×), avoiding low-RPM exam traps and vaccine/health throttling.
  - Connects naturally via end screens & playlists to `004` *What's Inside an Atom?* (`Rule 20`).
- **3-Way Thumbnail Test & Compare Plan (`LEARNINGS.md` Rules 11, 12, 14 + `THUMBNAIL_AND_TITLE_RULES.md` §2.1–2.B):**
  - **Thumb A (Hero Object — Rejected 1964 Paper & Glowing Collider Burst):** Warm 3D painted key art: right two-thirds shows an aged 1964 physics manuscript stamped in wax beside a luminous golden particle-collision starburst inside the circular LHC detector chamber; Explorer small lower left; clear left-band cream/gold serif lettering: `REJECTED IN 1964` (`3 words`, gold on `1964`, zero overlap on hero, no other AI-made text; fixed in `J3263` from `48-YEAR HUNT` so cover text never repeats Title A per §2.5 — pair Title B with Thumb B or C instead).
  - **Thumb B (`Rule 14` Bright High-Contrast Variant — Glowing Invisible Field):** Bright sunlit/golden laboratory cutaway: a glowing marble interacting with a luminous amber-gold quantum field (showing inertia / resistance to acceleration, avoiding a viscous-drag misconception in VO) while a massless photon darts past unhindered; Explorer small lower left; clear left-band serif lettering: `WHY THINGS WEIGH` (`3 words`, gold on `WEIGH`, zero overlap).
  - **Thumb C (Myth-Reversal Variant — The 1% Mass Twist):** Warm 3D painted cutaway of a glowing proton on an antique brass balance scale with three fiery quarks and swirling gluon energy bands dominating the pan (`99%` visual weight vs a tiny glowing golden Higgs spark); Explorer small lower left; clear left-band serif lettering: `ONLY 1% MASS` (`3 words`, gold on `1%`, zero overlap).
- **Signed-out YouTube Autocomplete (`2026-11-21`, `public_search.py`):**
  - `"what is the higgs boson"` → **`autocomplete = yes`** (`6` suggestions)
  - `"the god particle"` → **`autocomplete = yes`** (`10` suggestions, incl. `the god particle explained`)
  - `"why is it called the god particle"` → **`autocomplete = yes`** (`2` suggestions, incl. `why is the higgs boson called the god particle`)
  - `"how does the higgs field work"` → **`related`** (`how does higgs field work`, `how does higgs boson work`)
  - **Exact title collisions:** `0` across all `3` long title options (`A`, `B`, `C`) and both Short titles (`S01`, `S02`).
- **Rule 26(a) Two Ranking Videos (`≥10,000` views, retrieved `2026-11-21`):**
  1. `Fermilab` — [`RIg1Vh7uPyw`](https://youtu.be/RIg1Vh7uPyw) *What is a Higgs Boson?* (**`3,503,595` views**)
  2. `TED-Ed` — [`IElHgJG5Fe4`](https://youtu.be/IElHgJG5Fe4) *The basics of the Higgs boson - Dave Barney and Steve Goldfarb* (**`2,380,303` views**; plus `Veritasium` [`Ztc6QPNUqls`](https://youtu.be/Ztc6QPNUqls) **`3,372,242` views**, `PBS Space Time` [`kixAljyfdqU`](https://youtu.be/kixAljyfdqU) **`2,718,704` views**, `minutephysics` [`9Uh5mTxRQcg`](https://youtu.be/9Uh5mTxRQcg) **`2,571,633` views**, `Arvin Ash` [`R7dsACYTTXE`](https://youtu.be/R7dsACYTTXE) **`1,740,629` views**, and `SEA` [`7oR0Pmd-WIk`](https://youtu.be/7oR0Pmd-WIk) **`574,640` views**)
- **Neighbour Gate (`neighbours.py "higgs boson" "higgs field" "higgs mechanism" --top 25 --phrase "higgs boson"`):** **PASS (`11` strictly on-topic education videos `≥1,000,000` views, `TED-Ed/TED: yes`, `0` off-topic rows)** — saved in [`11_Upload-Package/evidence_2026-11-21_neighbours.json`](11_Upload-Package/evidence_2026-11-21_neighbours.json):
  1. `Veritasium` — [`Ztc6QPNUqls`](https://youtu.be/Ztc6QPNUqls) *Your Mass is NOT From the Higgs Boson* (**`3,372,242` views**, Tier 2)
  2. `PBS Space Time` — [`kixAljyfdqU`](https://youtu.be/kixAljyfdqU) *The Higgs Mechanism Explained | Space Time | PBS Digital Studios* (**`2,718,704` views**, Tier 2)
  3. `minutephysics` — [`9Uh5mTxRQcg`](https://youtu.be/9Uh5mTxRQcg) *The Higgs Boson, Part I* (**`2,571,633` views**, Tier 2)
  4. `TED-Ed` ★ — [`IElHgJG5Fe4`](https://youtu.be/IElHgJG5Fe4) *The basics of the Higgs boson - Dave Barney and Steve Goldfarb* (**`2,380,303` views**, Tier 1)
  5. `PBS Space Time` — [`G0Q4UAiKacw`](https://youtu.be/G0Q4UAiKacw) *How the Higgs Mechanism Give Things Mass* (**`1,905,645` views**, Tier 2)
  6. `minutephysics` — [`ASRpIym_jFM`](https://youtu.be/ASRpIym_jFM) *The Higgs Boson, Part II: What is Mass?* (**`1,516,607` views**, Tier 2)
  7. `PBS Space Time` — [`GjkqedrTwZo`](https://youtu.be/GjkqedrTwZo) *The Crisis in Physics: Why the Higgs Boson Should NOT Exist!* (**`1,508,804` views**, Tier 2)
  8. `Veritasium` — [`649iUqrOKuE`](https://youtu.be/649iUqrOKuE) *What Now For The Higgs Boson?* (**`1,352,059` views**, Tier 2)
  9. `SciShow` — [`WUnDsNL_5nk`](https://youtu.be/WUnDsNL_5nk) *So what IS the Higgs boson?* (**`1,290,571` views**, Tier 2)
  10. `minutephysics` — [`6guXMfg88Z8`](https://youtu.be/6guXMfg88Z8) *Higgs Boson Part III: How to Discover a Particle* (**`1,135,744` views**, Tier 2)
  11. `TED-Ed` ★ — [`joTKd5j3mzk`](https://youtu.be/joTKd5j3mzk) *The Higgs Field, explained - Don Lincoln* (**`1,098,547` views**, Tier 1)

---

## 4. Candidate 4-Act Discovery Outline (All Claims UNVERIFIED Pending `SOURCES.md` & `facts` Lane)

- **Cold Open (0:00–0:45, UNVERIFIED):** Cut immediately to a glowing particle-collision starburst inside the 27-kilometre tunnel beneath Geneva (`0:00–0:05`), then the physical apparatus — the superconducting dipole magnets and ATLAS/CMS detector rings (`0:05–0:15`). Zero agenda line (`Rules 10, 38`). State the paradox: physicists spent 48 years and billions building the largest machine in history to catch a particle that vanishes in less than a sextillionth of a second — after the very paper predicting it was rejected in 1964.
- **Act I — The 1964 Mass Crisis & the Rejected Edinburgh Paper (1964, UNVERIFIED):** In the early 1960s, the equations of fundamental forces demanded that force-carrying particles be massless — which flatly contradicted the real world where electrons, W/Z bosons, and matter have mass. In summer **1964**, **François Englert & Robert Brout** in Brussels, **Peter Higgs** in Edinburgh, and **Gerald Guralnik, Carl Hagen & Tom Kibble** in London independently proposed an invisible all-space field that slows certain particles down. *Physics Letters* rejected Higgs's second paper as having *"no obvious relevance to physics"*; Higgs revised it with a new paragraph explicitly predicting a massive spin-0 boson and sent it to *Physical Review Letters* (published October **1964**).
- **Act II — "The Goddamn Particle" & Why It Took 48 Years (1964–1993, UNVERIFIED):** Why couldn't anyone see the field? You can't scoop up empty space — you have to slam protons together hard enough to ring the field like a bell and knock loose a single excitation (a Higgs boson). In **1993**, Nobel laureate **Leon Lederman** wanted to call his book *"The Goddamn Particle"* because it was so maddeningly expensive and elusive; his publisher shortened it to **"The God Particle"**, a nickname physicists famously disliked.
- **Act III — The 27-Kilometre Ring & the 4 July 2012 Five-Sigma Reveal (2008–2012, UNVERIFIED):** Beneath the Franco-Swiss border, **CERN** cooled the **27-kilometre Large Hadron Collider** to **1.9 kelvin** (colder than outer space) to smash proton beams at nearly light speed. On **4 July 2012**, **Fabiola Gianotti** (ATLAS) and **Joe Incandela** (CMS) stood before a packed auditorium — with 83-year-old Peter Higgs wiping away tears in the audience — and revealed a **125 GeV** bump passing the **5-sigma** (`1 in 3.5 million`) discovery threshold. Higgs and Englert shared the **2013 Nobel Prize in Physics**.
- **Act IV — Midpoint/Late Twist: Why 99% of Your Mass Isn't From the Higgs (UNVERIFIED):** Raise the popular headline ("the Higgs gives everything its mass") and flip it: the Higgs field gives fundamental particles like electrons and quarks their intrinsic mass, yet roughly **99% of the mass of every proton and neutron in your body** comes from the strong-force binding energy ($E = mc^2$) of quarks and gluons trapped inside them. *Why then does that 1% matter?* Without the Higgs giving electrons even their tiny mass, electrons would zip away at the speed of light, atoms could never hold together, and chemistry — and you — could not exist.
- **Primary-Source Verification Guardrails (Mandatory Before Script Lock):**
  1. **Englert & Brout (`31 Aug 1964`, *Phys. Rev. Lett.* `13:321–323`), Higgs (`19 Oct 1964`, *Phys. Rev. Lett.* `13:508–509`), Guralnik, Hagen & Kibble (`16 Nov 1964`, *Phys. Rev. Lett.* `13:585–587`):** Verify exact submission/publication dates, *Physics Letters* rejection wording from Peter Higgs's own recollections/Nobel lecture (`2013`), and exact wording of the spin-0 boson prediction.
  2. **Lederman & Teresi (`1993`, *The God Particle*):** Verify exact quote on *"The Goddamn Particle"* publisher edit.
  3. **CERN / ATLAS (*Phys. Lett. B* `716:1–29`, 2012) & CMS (*Phys. Lett. B* `716:30–61`, 2012):** Verify LHC circumference (`27 km`), magnet operating temperature (`1.9 K`), `4 July 2012` seminar announcement, measured mass (`~125 GeV`), `5-sigma` threshold, and decay lifetime (`~1.6 × 10^-22 s`).
  4. **Proton mass budget (Wilczek / lattice QCD / Fermilab):** Verify exact percentage (`~99%`) of nucleon mass arising from QCD binding energy vs Higgs quark masses.

---

## 5. Two Candidate Search-Titled Shorts (`16–19 s` Ben 19 Nov House Rules · `Rule 32` · UNVERIFIED Concepts Only)

- **Short `S01`:** *Why Is the Higgs Boson Called the God Particle?* (`47 chars`, `0` exact collisions, positive search question; matches exact YouTube autocomplete `"why is the higgs boson called the god particle"`)
  - **First-line answer hook (`0.0–1.5s`, `vo_onset_s ≤ 0.15s`, UNVERIFIED):** *"Physicists never named it the God particle — a book publisher censored the real name."* (Concrete fact on line 1, names the subject and surprise within `1.5 s`, zero meta-promise.)
  - **Frame-0, Runtime & Loop Plan (Ben 19 Nov Shorts house rules · `16–19 s` · `Rules 2, 3, 6, 24, 27, 32`):**
    - Frame 0 (`0.0s`, full-bleed `9:16` premium **3D cartoon** moving plate, `0%` Explorer, `0%` bars/stills): glowing golden particle-collision burst flashing inside the 3D cartoon LHC ring; frame-0 caption line 1 carries the concrete fact (`A PUBLISHER CENSORED THE NAME`, yellow on `CENSORED` — never a 2-word ALL CAPS label).
    - Target runtime: **`17.5 s`** (inside the `16.0–19.0 s` house band). Cut 1 `≤2.8s`, all holds `≤3.5s`. Single mid-Short `WHEN` overlay: `1993` (white Didot italic inside `16:9` centre band, clear of `0–2s` and `9–14s`).
    - Payoff start at `≥70%` (`~12.5s / 17.5s`): Leon Lederman wanted *"The Goddamn Particle"* because it stayed hidden for decades — his publisher cut four letters, which is why *(loops seamlessly into line 1: "Physicists never named it the God particle…")*. Crossfade `≤0.3s` back to frame 0, zero CTA.
- **Short `S02`:** *Does the Higgs Boson Give You Your Mass?* (`40 chars`, `0` exact collisions, positive search question; myth-bust opener)
  - **First-line answer hook (`0.0–1.5s`, `vo_onset_s ≤ 0.15s`, UNVERIFIED):** *"Ninety-nine percent of your body's mass does not come from the Higgs boson."* (Concrete myth-busting fact on line 1 within `1.5 s`, zero meta-promise.)
  - **Frame-0, Runtime & Loop Plan (Ben 19 Nov Shorts house rules · `16–19 s` · `Rules 2, 3, 6, 24, 27, 32`):**
    - Frame 0 (`0.0s`, full-bleed `9:16` premium **3D cartoon** moving plate, `0%` Explorer, `0%` bars/stills): glowing 3D proton trembling on a gleaming antique brass balance scale as quarks and golden energy bands swirl inside; frame-0 caption line 1 carries the concrete fact (`99% OF YOUR MASS ISN'T HIGGS`, yellow on `99%`).
    - Target runtime: **`18.0 s`** (`16.0–19.0 s` band). Cut 1 `≤2.8s`, all holds `≤3.5s`. Single mid-Short `DATA` scale overlay: `99% BINDING ENERGY` (white Didot italic, clear of `0–2s` and `9–14s`).
    - Payoff start at `≥70%` (`~13.0s / 18.0s`): almost all your weight is pure strong-force energy trapped inside protons, yet without the Higgs's tiny 1% on electrons, atoms could never form — even though *(loops seamlessly into line 1: "Ninety-nine percent of your body's mass…")*. Crossfade `≤0.3s` back to frame 0, zero CTA.
