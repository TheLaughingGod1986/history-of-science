# Topic Brief — `132_Zachariasen-Zanotto-Pilkington-Why-Is-Glass-Transparent` (`HOS:132` — Rule-E GO `95.1/100` in `next_hos`)

> **RULE G & RULE-E STATUS (`J3408` / `J3409`, `2026-11-23`):**
> - **Rule-E verdict (`J3409`, `gemini` / `review` lane):** **GO (`95.1 / 100` · `9.51 / 10` Opportunity Score, `10 / 10` Rule-E gates PASS)** — pre-cleared in `jobs/WIP.json` `next_hos` under Rule G (`4/4` active HOS slots full: `HOS:008`, `HOS:009`, `HOS:010`, `HOS:013`). Nothing starts in production (`status.json` stages remain `todo`; merges remain Chief's). Review sheets: `11_Upload-Package/TOPIC_GO_NO_GO_SHEET.md` and `11_Upload-Package/TOPIC_OPPORTUNITY_SCORE.md`.
> - **Proposed 2027 Search Plan Note (`J3224`):** Complements Ben's proposed `hos-search-2027-01` search plan (`needsBen`, waiting for Ben's lock on the studio board — no HOS rule, cadence, or backlog policy changes until Ben approves).
> - **Strict Unverified Claims Guard (`facts` Lane Required Before Script Lock):** All historical and scientific claims in this brief are **UNVERIFIED** working notes. When an active HOS WIP slot opens, every claim, date, number, `DATA+SCALE`, `WHO`, `WHEN`, and `FACT` marker must be backed by verbatim primary-source quotes in `SOURCES.md` and verified through the `facts` lane (`gemini-agy`) before any script is locked, VO is recorded, or picture credit is spent.

---

## 1. HOS Data Comparison (`2026-11-23` Snapshot + `studio_ctr.json` + `channel_daily.json`)

- **Data sources read:**
  - `05_Analytics/hos/snapshots/2026-11-23.json` (`takenAt: 2026-11-23T06:40:34.195Z`, `43` public videos = `7` longs + `36` Shorts, `4,477` total views, `6` subscribers; `+565` views in last 24 h, `+928` in last 7 d, `+2,524` views and `+3` subs in last 30 d)
  - `05_Analytics/hos/studio_ctr.json` (`readAt: 2026-11-23T07:11:17.265966+00:00`, lifetime Studio impressions, CTR, average view %, and Shorts stayed-to-watch %)
  - `05_Analytics/hos/channel_daily.json` (`through: 2026-11-21`, `87` daily rows) and `05_Analytics/hos/REPORT.md`
  - `05_Analytics/LEARNINGS.md` (rules 1–41) and `05_Analytics/hos/search_research/2026-11-20.md` (`J3224`)
- **Elapsed-day denominator (`age_days`):** `max((date(2026, 11, 23) - date.fromisoformat(publishedAt[:10])).days, 1)` (`views/day = public_views / age_days`).
- **Low-sample statistical caveat (`Rule 1`):** Five public HOS longs have `5–15` lifetime views (`17–74` impressions), and bottom-tier Shorts have `4–30` views. Patterns inferred from low-N rows are treated explicitly as hypotheses, not settled laws.

### 1a. All `7` Public HOS Longs — Ranked by Views/Day Since Publish (`2026-11-23`)

| Rank | Video ID | Film | Title | Published (`age_days`) | Len | Views | Views/Day | Studio Impr | Studio CTR | Studio Avg View % | YTA 28d Views / Avg % |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| **1** | `AL_-qlWko_g` | `002` | *How Did We Discover the Periodic Table?* | `2026-09-17` (`67d`) | `541s` | **162** | **2.42/d** | **1,163** | 3.35% | 21.23% (`115s`) | `13v / 23.33%` |
| **2** | `GHZDsiH7L7A` | `004` | *What's Inside an Atom? Mostly Empty Space* | `2026-10-15` (`39d`) | `525s` | **35** | **0.90/d** | **840** | 1.43% | 23.54% (`124s`) | `9v / 54.97%` |
| **3** | `VbPubYd6Fbs` | `006` | *The Willow Tree That Was Made of Air* | `2026-11-05` (`18d`) | `532s` | **15** | **0.83/d** | 74 | 4.05% | **48.15%** (`256s`) | `15v / 48.15%` |
| **4** | `ETynHpIYLeY` | `007` | *How Was the First Vaccine Made? (And Why It's Named After a Cow)* | `2026-11-12` (`11d`) | `532s` | **7** | **0.64/d** | 44 | 4.55% | 19.29% (`103s`) | `7v / 19.29%` |
| **5** | `wwcjcFfC-5M` | `005` | *The Tied Arm That Proved Your Blood Circulates* | `2026-10-29` (`25d`) | `529s` | **7** | **0.28/d** | 17 | 17.65% | **6.73%** (`36s`) | `6v / 7.78%` |
| **6** | `_C92tIJCk8A` | `001` | *How Did We Discover Germs?* | `2026-09-03` (`81d`) | `365s` | **7** | **0.09/d** | 46 | 6.52% | 48.08% (`176s`) | `0v / —` |
| **7** | `frP_YrNShsU` | `003` | *How Did We Discover X-rays?* | `2026-09-24` (`60d`) | `426s` | **5** | **0.08/d** | 43 | 2.33% | 26.65% (`114s`) | `3v / 14.12%` |

- **3 Best HOS Longs & What They Share:**
  1. **`AL_-qlWko_g` (`002` *How Did We Discover the Periodic Table?*, `541s`)** — **`2.42/d`** (`162` views in `67d`), **`1,163` impressions** (`52.2%` of all `2,227` HOS long impressions), `3.35%` CTR, `21.23%` Studio avg view % (`70%` at `0:15`, `50%` at `0:30`).
  2. **`GHZDsiH7L7A` (`004` *What's Inside an Atom? Mostly Empty Space*, `525s`)** — **`0.90/d`** (`35` views in `39d`, `+1` sub), **`840` impressions** (`37.7%` of all HOS long impressions), `1.43%` CTR, `23.54%` Studio avg view % (`54.97%` in 28d YTA; `62%` at `0:15`, `45%` at `0:30`).
  3. **`VbPubYd6Fbs` (`006` *The Willow Tree That Was Made of Air*, `532s`)** — **`0.83/d`** (`15` views in `18d`), `74` impressions, `4.05%` CTR, channel-best **`48.15%` Studio & YTA avg view % (`256s`)** (low-N hypothesis).
  - **Shared pattern (Subject, Title Shape, Opening, Thumbnail Concept, Length):** `002` and `004` drive **`89.9%` (`2,003 / 2,227`) of all HOS long impressions** and **`82.8%` (`197 / 238`) of all HOS long views** because both open with plain, massive-demand search questions backed by multi-million `TED-Ed`/education neighbours (`LEARNINGS.md` Rules 1, 15, 26), run **`8.75–9.0 min` (`525–541s`)**, pair a single physical mystery object on the thumbnail with clear serif lettering (`Rules 11–12`), and deliver concrete physical facts in the first `15s` (`Rule 10`). Meanwhile `006` (`48.15%` avg viewed) shows a single unforgettable experimental paradox holds viewers once clicked.
- **3 Worst HOS Longs & What They Share (Small-N Hypotheses):**
  1. **`frP_YrNShsU` (`003` *How Did We Discover X-rays?*, `426s`)** — **`0.08/d`** (`5` views in `60d`), `43` impressions, `2.33%` CTR, `26.65%` avg view %.
  2. **`_C92tIJCk8A` (`001` *How Did We Discover Germs?*, `365s`)** — **`0.09/d`** (`7` views in `81d`), `46` impressions, `6.52%` CTR, `48.08%` avg view %.
  3. **`wwcjcFfC-5M` (`005` *The Tied Arm That Proved Your Blood Circulates*, `529s`)** — **`0.28/d`** (`7` views in `25d`), **`17` impressions**, `17.65%` CTR (tiny N), **`6.73%` Studio avg view % (`36s`)**.
  - **Shared pattern:** `005` used a literary statement title with no searchable phrase (`Rule 26` violation → `17` impressions), while `001` (`365s`) and `003` (`426s`) used generic *How Did We Discover…* survey labels and shorter `6–7 min` runtimes rather than a sharp search question + concrete mechanism twist (`Rules 10, 15, 23, 26`). (`007` vaccine at `44` impr / `7`v also faces health/vaccine distribution throttling per `Rule 36` and `J3224`.)

### 1b. All `36` Public HOS Shorts — Ranked by Views/Day Since Publish (`2026-11-23`)

| Rank | Video ID | Title | Published (`age_days`) | Len | Views | Views/Day | Stayed % | Studio Avg View % | Likes |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|
| **1** | `el30-mHiH-0` | *How Does the Heart Pump Blood?* *(early `20h`)* | `2026-11-22` (`1d`) | `26s` | **523** | **523.00/d** | 26.77% | 66.41% (`17s`) | 5 |
| **2** | `xzKoHg0E0_U` | *What Is Dalton's Atomic Theory?* | `2026-11-16` (`7d`) | `25s` | **239** | **34.14/d** | **53.13%** | 61.49% (`15s`) | 0 |
| **3** | `29bpGAI0wb8` | *What happens if you keep cutting gold in half?* | `2026-10-16` (`38d`) | `25s` | **1,229** | **32.34/d** | 40.78% | 44.14% (`11s`) | 12 |
| **4** | `Wvjd8g0CpzE` | *The Blood Vessels Finer Than a Hair* | `2026-11-15` (`8d`) | `26s` | **218** | **27.25/d** | 15.35% | 74.94% (`19s`) | 3 |
| **5** | `Bks_JLId1ew` | *How Do Plants Make Oxygen?* *(early `44h`)* | `2026-11-21` (`2d`) | `26s` | **50** | **25.00/d** | 48.57% | 96.53% (`25s`) | 0 |
| **6** | `PFj6172YU4Q` | *One Tight Band Proved Your Blood Goes Round* | `2026-11-08` (`15d`) | `27s` | **221** | **14.73/d** | 16.67% | 61.53% (`17s`) | 3 |
| **7** | `AMSriTQ-lcQ` | *Are Marie Curie's Notebooks Still Radioactive?* | `2026-10-28` (`26d`) | `22s` | **274** | **10.54/d** | 22.66% | 76.94% (`17s`) | 6 |
| **8** | `l8bxm9L3zl8` | *How Does a Blood Pressure Cuff Work?* | `2026-11-20` (`3d`) | `24s` | **29** | **9.67/d** | 38.46% | 60.99% (`15s`) | 0 |
| **9** | `OnJ8MFu0Mi0` | *How Did John Snow Stop Cholera?* | `2026-10-26` (`28d`) | `23s` | **231** | **8.25/d** | 29.60% | 65.66% (`15s`) | 8 |
| **10** | `pWySvZsneZg` | *Why Gold Foil Bounced Rutherford's Particles Back* | `2026-11-01` (`22d`) | `25s` | **137** | **6.23/d** | 37.23% | **112.43%** (`28s`) | 2 |
| **11** | `oKqmnJNGiHg` | *How Was Phosphorus Discovered?* | `2026-10-21` (`33d`) | `23s` | **194** | **5.88/d** | 42.03% | **88.35%** (`20s`) | 7 |
| **12** | `-3L6HzJ_d_4` | *What Is the Pasteur Swan Neck Flask Experiment?* | `2026-10-27` (`27d`) | `19s` | **140** | **5.19/d** | **78.95%** | **73.84%** (`14s`) | 1 |
| **13** | `cLKDiYP55J8` | *What Was the Edward Jenner Experiment?* | `2026-11-13` (`10d`) | `23s` | 47 | 4.70/d | 43.48% | 67.71% (`16s`) | 0 |
| **14** | `clV6E10NLPw` | *The spray that stopped surgery killing patients* | `2026-10-20` (`34d`) | `25s` | 155 | 4.56/d | 23.45% | 57.79% (`14s`) | 4 |
| **15** | `qOZgess30h0` | *Invisible life is still everywhere* | `2026-10-13` (`41d`) | `24s` | 169 | 4.12/d | 25.15% | 39.82% (`10s`) | 5 |
| **16** | `c2q7w0pgcn8` | *Who Discovered Infrared Light?* | `2026-10-19` (`35d`) | `23s` | 138 | 3.94/d | 43.52% | **105.30%** (`24s`) | 1 |
| **17** | `BW_CFAX-mxc` | *Is the Heart a Pump?* | `2026-10-31` (`23d`) | `22s` | 89 | 3.87/d | 32.91% | 81.69% (`18s`) | 1 |
| **18** | `Rl2uZ-KOTl8` | *Your Heart Pumps More Blood Than You Have* | `2026-10-30` (`24d`) | `25s` | 78 | 3.25/d | 26.58% | 53.64% (`13s`) | 4 |
| **19** | `xHnIi9GqOsM` | *Why Do Veins Have Valves?* | `2026-11-05` (`18d`) | `23s` | 42 | 2.33/d | 20.59% | 61.55% (`14s`) | 0 |
| **20** | `TbMMJSRKC3U` | *He said every eighth element repeats* | `2026-10-18` (`36d`) | `27s` | 63 | 1.75/d | 26.92% | 118.07% (`32s`) | 1 |
| **21** | `qW2OsD4mujc` | *The Four Elements Were Wrong* | `2026-11-03` (`20d`) | `24s` | 34 | 1.70/d | 57.69% | 192.62% (`46s`) | 0 |
| **22** | `LCZRHUyTiq0` | *What Are Cathode Rays?* | `2026-10-23` (`31d`) | `26s` | 49 | 1.58/d | 29.79% | 50.04% (`13s`) | 2 |
| **23** | `iqToagXnjX0` | *Microbes in a drop of pond water* | `2026-09-06` (`78d`) | `25s` | 113 | 1.45/d | 28.28% | 77.86% (`19s`) | 1 |
| **24** | `H1y0DXFVmw8` | *Germs don't cast a shadow* | `2026-09-06` (`78d`) | `25s` | 80 | 1.03/d | 19.75% | 59.46% (`15s`) | 1 |
| **25** | `ChbsigHD5_o` | *How Do Plants Clean the Air?* | `2026-11-18` (`5d`) | `25s` | 5 | 1.00/d | 100.00% | 36.12% (`9s`) | 0 |
| **26** | `xvanpsLeADE` | *How did Röntgen see bones without cutting* | `2026-09-26` (`58d`) | `25s` | 40 | 0.69/d | 23.33% | 50.33% (`13s`) | 0 |
| **27** | `xgx2lYHhYZM` | *Why Is It Called a Vaccine?* | `2026-11-17` (`6d`) | `25s` | 4 | 0.67/d | 100.00% | 62.41% (`16s`) | 0 |
| **28** | `oowAOWTBoq0` | *How X-rays Were Discovered by Accident* | `2026-09-25` (`59d`) | `25s` | 32 | 0.54/d | 47.62% | 331.08% (`83s`) | 1 |
| **29** | `nba0-f7PPeU` | *Why tellurium sat before iodine* | `2026-09-21` (`63d`) | `25s` | 34 | 0.54/d | 60.71% | 42.70% (`11s`) | 1 |
| **30** | `nFQRWmpulTQ` | *He predicted a metal before it was found* | `2026-09-19` (`65d`) | `25s` | 34 | 0.52/d | 66.67% | 55.91% (`14s`) | 0 |
| **31** | `8_Edn_HCi1s` | *Germs hitch a ride on you* | `2026-09-06` (`78d`) | `25s` | 38 | 0.49/d | 33.33% | 34.25% (`9s`) | 0 |
| **32** | `uU12JA5rMWg` | *The periodic table's empty chairs* | `2026-09-18` (`66d`) | `25s` | 30 | 0.45/d | 66.67% | 58.79% (`15s`) | 0 |
| **33** | `sILtQxgYQk8` | *A flask that proved germs come from outside* | `2026-09-06` (`78d`) | `25s` | 24 | 0.31/d | 41.67% | 36.70% (`9s`) | 0 |
| **34** | `CnHwX1L9XHg` | *Gallium sat where the table said* | `2026-09-20` (`64d`) | `26s` | 16 | 0.25/d | 30.43% | 33.45% (`9s`) | 0 |
| **35** | `zI_eD3vFWmE` | *The first X-ray showed a wedding ring* | `2026-09-27` (`57d`) | `25s` | 9 | 0.16/d | 50.00% | 64.00% (`16s`) | 0 |
| **36** | `LanTHJckYx8` | *What other table has empty chairs?* | `2026-09-22` (`62d`) | `26s` | 4 | 0.06/d | 33.33% | 23.08% (`6s`) | 0 |

- **3 Best Mature HOS Shorts & What They Share:**
  1. **`xzKoHg0E0_U` (*What Is Dalton's Atomic Theory?*, `25s`)** — **`34.14/d`** (`239` views in `7d`), **`53.13%` stayed (`WATCH`)**, `61.49%` avg view % (`15s`), driven by **`197` 28d YouTube search views** (`88.3%` of `223` YTA views; `Rule 41`).
  2. **`29bpGAI0wb8` (*What happens if you keep cutting gold in half?*, `25s`)** — **`32.34/d`** (**`1,229` public / `1,230` Studio views**, #1 lifetime HOS video, `12` likes), `40.78%` stayed, `44.14%` avg view % (`11s`).
  3. **`-3L6HzJ_d_4` (*What Is the Pasteur Swan Neck Flask Experiment?*, `19s`)** — **`5.19/d`** (`140` views in `27d`), channel-best **`78.95%` stayed (`PASS ≥60%`)** and **`73.84%` Studio / `74.98%` YTA avg view % (`PASS ≥70%`)**, **`129` 28d search views (`93.5%` of `138` YTA views)** — the ONLY mature `100+`-view HOS Short passing BOTH targets AND the channel's only `19s` cut (matching Ben's 19 Nov `16–19 s` house rule); reinforced by loop winners `pWySvZsneZg` (`112.43%` avg view %, `137`v, `+1` sub), `c2q7w0pgcn8` (`105.30%` avg view %, `43.52%` stayed, `138`v), `oKqmnJNGiHg` (`88.35%` avg view %, `42.03%` stayed, `194`v), and early burst `el30-mHiH-0` (`523`v in `20h`, `26.77%` stayed, `66.41%` avg).
  - **Shared pattern:** Direct positive search questions naming a specific **object, experiment, or physical paradox** win stayed-to-watch (`40.8–79.0%`) and compounding YouTube search, while tighter cuts (`19–23s`), `≤1.0s` loop tails, zero CTA, and payoff withheld past `70%` push average viewed to `74–112%` (`Rules 1, 2, 3, 6, 24, 27, 28, 32, 41`).
- **3 Worst Mature HOS Shorts & What They Share (Small-N Hypotheses):**
  1. **`LanTHJckYx8` (*What other table has empty chairs?*, `26s`)** — **`0.06/d`** (`4` views in `62d`), `33.33%` stayed, `23.08%` avg view % (`6s`).
  2. **`zI_eD3vFWmE` (*The first X-ray showed a wedding ring*, `25s`)** — **`0.16/d`** (`9` views in `57d`), `50.00%` stayed, `64.00%` avg view % (`16s`).
  3. **`CnHwX1L9XHg` (*Gallium sat where the table said*, `26s`)** — **`0.25/d`** (`16` views in `64d`), `30.43%` stayed, `33.45%` avg view % (`9s`) — alongside cold-feed statement flops `Wvjd8g0CpzE` (**`15.35%` stayed MISS** on `218`v) and `PFj6172YU4Q` (**`16.67%` stayed MISS** on `221`v) plus zero-feed stalls `xgx2lYHhYZM` (`4`v) and `ChbsigHD5_o` (`5`v).
  - **Shared pattern:** Cryptic riddles, declarative statements lacking a searchable subject, generic non-entity questions, and vaccine framing fail either stayed-to-watch (`15.4–16.7%`) or impressions (`Rules 1, 28, 32, 36, 41`).

---

## 2. Overlap & Non-Duplication Check (`2026-11-23`)

Checked against:
- All folders in `02_Video-Projects/` (`000`–`018`, `099`–`119` on `main`),
- All open HOS topic PRs `#659` (`120` Why Do We Cry, `121` Why Do Cats Purr), `#682` (`122` Why Do We Sneeze, `123` Why Does Hair Turn Grey), `#689` (`124` Why Is the Ocean Salty, `125` What Causes the Tides), `#706` (`126` What Is the Higgs Boson, `127` How Do Airplanes Fly), `#724` (`128` Why Do We Use AC Instead of DC, `129` How Was the Microwave Invented), `#726` (`130` How Does a Nuclear Reactor Work, `131` What Is the Theory of Relativity), and paired film `133` (Max Planck & Birth of Quantum Physics),
- All `011`–`095` folders in `00_Brand/Channel-Setup/ideas/`, `VIDEO_BACKLOG.json`, and `jobs/WIP.json` (`083` covers eyes/glasses optical refraction; `042` covers lasers and optical fibres; **none** cover why solid glass is transparent while sand is opaque, Zachariasen's 1932 random network, the 9 eV quantum band gap, Zanotto's 1998 debunking of the flowing cathedral-glass myth, or Alastair Pilkington's 1952–1959 float-glass breakthrough).
- **Result:** **Zero overlap.**

---

## 3. Packaging, Why It Should Work & Search/Neighbour Evidence (`Rule 26` + `neighbours.py` + `public_search.py`)

- **Title A (Primary Proposal, `LEARNINGS.md` Rules 1, 15, 23, 26 — `43 chars ≤ 50 chars`, `0` exact collisions):** `Why Is Glass Transparent? (The Quantum Gap)`
- **Title A1 (Story + Stakes Bracket Variant — `49 chars ≤ 50 chars`, `0` exact collisions):** `Why Is Glass Transparent? (Made From Opaque Sand)`
- **Title B (Test & Compare Arm 2, `Rule 23` — `52 chars ≤ 70 chars`, `0` exact collisions):** `Glass Isn't a Liquid (The Quantum Reason It's Clear)`
- **Title C (`Rule 26` Exact Phrase + Process — `56 chars ≤ 70 chars`, `0` exact collisions):** `Why Is Glass Transparent? (How Melting Sand Turns Clear)`
- **One-Line Hook:** Every window on Earth is made from opaque beach sand — yet melting it into a disordered atomic web opens a quantum energy gap so wide that visible light flies straight through a solid wall while sunburn UV rays bounce off.
- **Why It Should Work (Past Winners & `LEARNINGS.md` Rules):**
  - Mirrors our top two impression-driving HOS longs — **`002` Periodic Table (`AL_-qlWko_g`, `162` views, `2.42/d`, `1,163` impressions, `3.35%` CTR)** and **`004` Inside an Atom (`GHZDsiH7L7A`, `35` views, `0.90/d`, `840` impressions)** — by opening with an exact, universal everyday search question (`"why is glass transparent"`, `autocomplete = yes`) anchored directly beside **`TED-Ed`'s `5.03M`-view *Why is glass transparent?*** and **`Veritasium`'s `9.81M`-view *The Most Important Material Ever Made*** (`Rules 1, 15, 26`), while pairing it with a concrete physical-object paradox and myth-bust (opaque beach sand → clear solid window; medieval cathedral glass is NOT a slow liquid) like retention leader **`006` Willow Tree (`VbPubYd6Fbs`, `48.15%` Studio avg view %)** (`Rules 10, 23`).
  - Mirrors our top-performing HOS Shorts — **`29bpGAI0wb8` (*What happens if you keep cutting gold in half?*, `1,229` views, `32.34/d`)**, **`xzKoHg0E0_U` (*What Is Dalton's Atomic Theory?*, `34.14/d`, `53.13%` stayed, `197` search views)**, and **`-3L6HzJ_d_4` (*What Is the Pasteur Swan Neck Flask Experiment?*, `19s`, `78.95%` stayed PASS, `73.84%` avg view % PASS)** — by turning an everyday familiar object (`a windowpane`) into 16–19 s question-led, myth-busting visual experiments (`Rules 2, 3, 6, 24, 27, 28, 32, 41` + Ben's 19 Nov Shorts house rules).
- **3-Way Thumbnail Test & Compare Plan (`LEARNINGS.md` Rules 11, 12, 14 + `THUMBNAIL_AND_TITLE_RULES.md` §2.1–2.B; zero title-word repeats per §2.5 and zero AI-painted text on key art per §2.6):**
  - **Thumb A (Hero Object — Sand Grain to Window Beam):** Painted 3D house-style key art: a glowing sunbeam passes cleanly through a thick bevelled glass pane emerging from a mound of opaque golden beach sand on the right two-thirds (clean painted art with zero AI-made labels or numbers per §2.6); the Explorer small at lower left; cream/gold serif text on the clear left band: `LIGHT PASSES THROUGH` (`3 words`, gold on `PASSES`, zero overlap on hero, zero words repeated from Titles A, A1, B, or C). *(Tightened in `J3409` from `9 EV BARRIER` to remove mobile jargon and avoid conflating pure fused silica's `~9 eV` gap with soda-lime window glass's `~3.9–4.1 eV` UV cutoff.)*
  - **Thumb B (`Rule 14` Bright High-Contrast Variant — Sunlit Cathedral Window):** Bright sunlit medieval Gothic stained-glass window cross-section showing uneven glass thickness beside a cracked period brass hourglass (no painted numbers/text on the hourglass per §2.6); Explorer small at lower left; serif text on clear left band: `WINDOWS NEVER FLOW` (`3 words`, gold on `NEVER`, concrete named subject per §2.B.1, zero words repeated from Titles A, A1, B, or C). *(Tightened in `J3409` from `NOT A LIQUID` to eliminate cross-title §2.5 overlap with Title B.)*
  - **Thumb C (Molten Tin Float-Glass Ribbon):** Warm amber industrial furnace interior where a glowing river of molten glass floats dead-flat across a mirror-like bath of liquid silver tin; Explorer small at lower left; serif text on clear left band: `MOLTEN TIN` (`2 words`, gold on `MOLTEN`, zero words repeated from Titles A, A1, B, or C).
- **Signed-out YouTube Autocomplete (`2026-11-23`, `10` queries / `75` search rows in `11_Upload-Package/evidence_2026-11-23_public_search.json`):**
  - `"why is glass transparent"` → **`autocomplete = yes`** (`why is glass transparent`, `why is glass clear`)
  - `"is glass a liquid"` → **`autocomplete = yes`** (`is glass a liquid`, `is glass a liquid or a solid`)
  - `"why does light pass through glass"` → **`autocomplete = yes`** (`why does light pass through glass`)
  - `"how is float glass made"` → **`autocomplete = yes`** (`how is float glass made`, `how is plate glass made`, `how is sheet glass made`)
  - **Exact title collisions across all 4 long titles + 2 Short titles:** **`0` exact collisions.**
- **Rule 26(a) Two Ranking Videos (`≥10,000` views, saved `2026-11-23` in `evidence_2026-11-23_public_search.json`):**
  1. `TED-Ed` — [`VwRLIt6jgdM`](https://youtu.be/VwRLIt6jgdM) *Why is glass transparent? - Mark Miodownik* (**`5,032,342` views**)
  2. `Be Smart` — [`FnDP1sjKGfU`](https://youtu.be/FnDP1sjKGfU) *Glass is Solid… So Why Is It Clear?* (**`1,854,079` views**; plus `Veritasium` [`2oDXbFcHliM`](https://youtu.be/2oDXbFcHliM) **`9,814,172` views**, `Veritasium` [`c6wuh0NRG1s`](https://youtu.be/c6wuh0NRG1s) *Is Glass a Liquid?* **`5,789,606` views**, and `Sixty Symbols` [`Omr0JNyDBI0`](https://youtu.be/Omr0JNyDBI0) **`1,526,530` views**)
- **Neighbour Gate (`neighbours.py`):** **PASS (`4` raw / `4` education videos `≥1,000,000` views — `3` directly on glass/transparency + `1` adjacent amorphous metallic glass; `0` off-topic rows at `≥1M`, `TED-Ed/TED: yes`)** — saved in [`11_Upload-Package/evidence_2026-11-23_neighbours.json`](11_Upload-Package/evidence_2026-11-23_neighbours.json):
  1. `Veritasium` — [`2oDXbFcHliM`](https://youtu.be/2oDXbFcHliM) *The Most Important Material Ever Made* (**`9,814,162` views**)
  2. `TED-Ed` ★ — [`VwRLIt6jgdM`](https://youtu.be/VwRLIt6jgdM) *Why is glass transparent? - Mark Miodownik* (**`5,032,327` views**)
  3. `TED-Ed` ★ — [`oULkYytYPgs`](https://youtu.be/oULkYytYPgs) *What is metallic glass? - Ashwini Bharathula* (**`2,031,710` views** — adjacent amorphous glass structure)
  4. `Be Smart` — [`FnDP1sjKGfU`](https://youtu.be/FnDP1sjKGfU) *Glass is Solid… So Why Is It Clear?* (**`1,854,087` views**; plus `<1M` on-topic `The Science Asylum` [`wDu0KMdDD1I`](https://youtu.be/wDu0KMdDD1I) **`103,912` views**. Three `<1M` rows in `neighbours.json` are transparently excluded as off-topic/tangential: `TED-Ed` [`d5_h1VuwD6g`](https://youtu.be/d5_h1VuwD6g) *Rapid prototyping Google Glass* `466,294`, `Khan Academy` [`sv8-y7N0Ryw`](https://youtu.be/sv8-y7N0Ryw) *Refraction in a glass of water* `12,411`, and `TEDx Talks` [`dlrNp_Vgw7o`](https://youtu.be/dlrNp_Vgw7o) *The Alchemy of Glass* `1,471`.)

---

## 4. Candidate 4-Act Discovery Outline (All Claims UNVERIFIED Pending `SOURCES.md` & `facts` Lane)

- **Cold Open (0:00–0:45, Proof-First `0:05–0:15` Apparatus Window per `Rules 10 & 30`, UNVERIFIED):**
  - `0:00–0:05`: A handful of opaque golden beach sand (`silicon dioxide`) pours into a white-hot crucible, melts into glowing honey, and cools into a crystal-clear sheet of glass — and a beam of sunlight flies straight through the solid wall.
  - `0:05–0:15` (Apparatus / Physical Proof): Hard cut to a side-by-side optical bench: visible rainbow light beams (`~1.8–3.1 eV`) pass cleanly through ordinary soda-lime window glass while sunburn UVB ultraviolet light (`~3.9–4.4 eV`) stops dead at the pane (with pure fused silica's much wider `~9 eV` deep-UV band gap clearly distinguished from soda-lime window glass's `~3.9–4.1 eV` UV cutoff in Act II — never conflated). Zero *"In this film…"* agenda line.
  - `0:15–0:45`: Sand and window glass are built from the same silicon and oxygen atoms — yet one blocks every ray of sunlight and the other vanishes before your eyes. Solving why took Venetian glassmakers, atomic blueprints, quantum physics, a debunked cathedral myth, and a British engineer washing up at his kitchen sink.
- **Act I — From Venetian *Cristallo* to Zachariasen's 1932 Atomic Blueprint & Warren's X-Ray Proof (1450–1937, UNVERIFIED):** For centuries after **Angelo Barovier** (~1450, Murano, Venice) purified murky green glass into clear *cristallo* using purified plant ash and manganese oxide decolouriser and **George Ravenscroft** (1674, London) pioneered brilliant lead glass, craftsmen could make clear glass without knowing what made it transparent. Why does a pile of quartz sand scatter light white when melted quartz turns clear? In **October 1932**, Norwegian-American physicist **William Houlder Zachariasen** (*J. Am. Chem. Soc.* `54(10): 3841–3851`, *"The Atomic Arrangement in Glass"*) proposed the theoretical **continuous random network** model of $\text{SiO}_4$ tetrahedra — experimentally confirmed shortly afterward via X-ray diffraction by **B. E. Warren** (1933–1937) — showing glass has no microscopic crystal grain boundaries or air pockets to bounce light sideways (`DATA+SCALE`: wavelength of visible light `~400–700 nm` vs atomic spacing `~0.16 nm` — light waves glide over atomic spacing thousands of times smaller than themselves). *(Guardrail: do not misattribute Warren's experimental X-ray diffraction proof to Zachariasen's theoretical 1932 paper.)*
- **Act II — The Midpoint Twist: Why Isn't Glass Black? (Band Theory & the Quantum Energy Gap, UNVERIFIED):** *"Case closed? Wrong."* Obsidian volcanic glass and amorphous silicon have no crystal grain boundaries either — yet they are dark or opaque! Uniformity stops scattering, not absorption. Quantum solid-state band theory (pioneered for crystals by **Felix Bloch** 1928 and **Alan Herries Wilson** 1931, *Proc. R. Soc. A* `133: 458`, and grounded in glass by **short-range $\text{Si–O}$ chemical bonding**, not long-range crystal periodicity) delivered the real twist: electrons in glass can only occupy allowed energy bands separated by a forbidden **band gap**. In pure **fused silica ($\text{SiO}_2$)** glass, that gap is roughly **`~9 electron-volts (eV)`** (absorbing only deep/vacuum UV around `~138 nm`), whereas visible light photons carry only **`~1.8 to 3.1 eV`** (`DATA+SCALE` energy ladder). Because a visible photon lacks the energy to jump an electron across the gap, the glass refuses to absorb it — so visible light passes straight through! In **ordinary soda-lime window glass**, added soda/lime fluxes (creating non-bridging oxygens) and trace iron oxides lower the UV absorption edge to **`~3.9–4.1 eV` (`~300–320 nm`)** — which is why ordinary window glass blocks sunburn **UVB** (`280–315 nm`) while letting much **UVA** (`315–400 nm`) and all visible light through (whereas pure `9 eV` fused silica actually transmits UVB).
- **Act III — The Slow-Liquid Myth Busted: Edgar Dutra Zanotto's 1998 Calculation (1998–1999, UNVERIFIED):** Tour guides still point to thick bottoms on medieval stained-glass cathedral windows as proof that "glass is an ultra-slow liquid flowing downhill over centuries." In **May 1998**, Brazilian materials scientist **Edgar Dutra Zanotto** (*American Journal of Physics* `66(5): 392–395`, *"Do cathedral glasses flow?"*; refined with P. K. Gupta in 1999 to `~10^23` years for medieval soda-lime compositions vs `~10^32` years for $\text{GeO}_2$/reference calculations — verify exact paper values in `SOURCES.md`) calculated room-temperature relaxation times and showed that a stained-glass pane would take **vastly longer than the `13.8-billion-year` age of the universe** to sag measurably under gravity (`DATA+SCALE` timeline comparison). Medieval windows vary in thickness because hand-blown **cylinder (muff)** and spun **crown-glass** panes came out uneven from the furnace — indeed surveys find panes thicker at the top or sides as well as the bottom!
- **Act IV — Alastair Pilkington's 1952 Kitchen-Sink Epiphany (1952–1959, UNVERIFIED):** Even once science understood glass's quantum secret, making a truly flat, distortion-free windowpane required grinding and polishing away roughly a fifth of every cast plate at huge cost. In **October 1952**, British engineer **Alastair Pilkington** *(knighted 1970 — never "Sir" on 1952/1959 `WHO` cards)* in St Helens, England noticed a film of grease floating dead-flat on dishwater while washing dishes at home. Seven years and millions of pounds of molten-tin furnace trials later (**20 January 1959** announcement; verify exact £4M vs £7M development cost in `SOURCES.md`), Pilkington's **float glass process** — pouring `~1,000 °C` molten glass onto a mirror-flat bath of liquid tin — produced optically flat panes with zero grinding, transforming modern architecture, lenses, and screens worldwide.
- **Pre-sourced `Teach on screen` & `Polish pass` markers (all numbers UNVERIFIED pending `SOURCES.md`):** `DATA+SCALE` (5, incl. `1450 → 1998` timeline, `400–700 nm` vs `0.16 nm` atomic scale, `1.8–3.1 eV` visible vs `~3.9–4.1 eV` window-glass UV cutoff vs `~9 eV` pure silica gap ladder, Zanotto relaxation time vs `13.8B yr` universe age, `~1,000 °C` molten tin float bath), `WHO` (Angelo Barovier, William Houlder Zachariasen, B. E. Warren, Alan Herries Wilson, Edgar Dutra Zanotto, Alastair Pilkington — all year-accurate), `WHEN` (`~1450`, `1931`, `Oct 1932`, `Oct 1952`, `1959`, `May 1998`), `FACT` (4 sourced beats).

---

## 5. Two Candidate Search-Titled Shorts (`Ben 19 Nov 16–19 s Rules` + `Rules 32 & 41` — UNVERIFIED Concepts Only)

- **Short `S01`:** *Is Medieval Cathedral Glass Really a Slow Liquid?* (`49 chars`, `0` exact collisions; positive myth-bust search question backed by `"is glass a liquid"` `autocomplete = yes`)
  - **16–19 s Loop Concept (`Ben 19 Nov Rules`):**
    - **Frame 0 (`0.0 s`, premium 3D cartoon moving plate, zero Explorer, zero bars):** Warm golden sunlight streaming through a tall medieval cathedral window as the 3D cross-section glows thicker at the bottom edge. On-screen line-1 concrete fact caption: `Old windows never flowed` (yellow on `never`).
    - **Spoken hook (`≤1.5 s` titled noun + surprise, zero dateline, zero meta-promise):** *"Medieval cathedral glass is thicker at the bottom — and it has nothing to do with glass flowing like a liquid."*
    - **Single mid-Short `Teach on screen` overlay (`~9.5 s`, inside 16:9 band):** `LONGER THAN THE UNIVERSE`.
    - **Payoff (`≥70%` runtime, `~13.5 s / 18.0 s`):** Materials physicist Edgar Zanotto proved room-temperature glass would take longer than the age of the universe to sag — medieval glassmakers simply hand-blew and spun uneven panes (many thicker at the top or sides too) — looping cleanly back into *"Medieval cathedral glass is thicker at the bottom…"* (`<0.3 s` visual seam match, `0` CTA).
- **Short `S02`:** *Why Does Window Glass Block Sunburn UV Rays?* (`44 chars`, `0` exact collisions; positive everyday search question backed by `"why is glass transparent"` and `"why does light pass through glass"` `autocomplete = yes`)
  - **16–19 s Loop Concept (`Ben 19 Nov Rules`):**
    - **Frame 0 (`0.0 s`, premium 3D cartoon moving plate, zero Explorer, zero bars):** Bright 3D cutaway of a sunlit windowpane: golden visible light beams glide cleanly through the glass while sharp violet UVB waves stop dead in the pane. On-screen line-1 concrete fact caption: `Visible light skips the gap` (yellow on `skips`).
    - **Spoken hook (`≤1.5 s` titled noun + surprise, zero dateline, zero meta-promise):** *"Window glass lets bright sunlight right through — yet stops the UVB rays that cause sunburn."*
    - **Single mid-Short `Teach on screen` overlay (`~9.5 s`, inside 16:9 band):** `BLOCKS SUNBURN UVB` *(tightened in `J3409` from `9 EV QUANTUM GAP` so ordinary soda-lime window glass's `~3.9–4.1 eV` UVB cutoff is never conflated with pure fused silica's `~9 eV` deep-UV gap)*.
    - **Payoff (`≥70%` runtime, `~13.5 s / 18.0 s`):** Visible light photons carry too little energy to excite window glass's electrons, so they pass right through, while punchier UVB photons hit the glass's soda-lime UV cutoff and get absorbed — looping cleanly back into *"Window glass lets bright sunlight right through…"* (`<0.3 s` visual seam match, `0` CTA).
