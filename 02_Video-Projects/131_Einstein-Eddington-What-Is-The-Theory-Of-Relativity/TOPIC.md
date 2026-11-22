# Topic Brief — `131_Einstein-Eddington-What-Is-The-Theory-Of-Relativity` (`HOS:131` — Queued for Rule-E Review in `next_hos`)

> **RULE-E & RULE G STATUS (`J3348`, `2026-11-22`):**
> - **Backlog placement (`jobs/WIP.json` `next_hos`):** Added under **Rule G** (`active` holds `4/4` HOS slots: `008`, `009`, `010`, `013`). Nothing starts in production (`status.json` stages are all `todo`) until Rule-E topic go/no-go review passes and an active HOS WIP slot opens.
> - **2027 Search Plan Alignment (`J3224` `hos-search-2027-01`, pending Ben's OK):** Fits **Cluster 2 (*Nuclear, Quantum & Modern Physics Breakthroughs*, Film #5)** — pairs directly with `009_The-Falling-Moon-Gravity` (Newton's gravity) as a natural end-screen sequel, and has zero overlap with `025_Young-Fresnel-Einstein-Light` (which covers wave-particle duality and the 1905 photoelectric effect, not relativity or the 1919 eclipse).
> - **Strict Unverified Claims Guard (`facts` Lane Required Before Script Lock):** All historical and scientific claims in this brief are **UNVERIFIED** working notes. When an active HOS WIP slot opens, every claim, date, and number must be backed by verbatim primary-source quotes in `SOURCES.md` and verified through the `facts` lane (`gemini-agy`) before any script is locked, VO is recorded, or picture credit is spent.

---

## 1. HOS Data Comparison (`2026-11-22` Snapshot + `studio_ctr.json` + `channel_daily.json`)

- **Data sources read:**
  - `05_Analytics/hos/snapshots/2026-11-22.json` (`takenAt: 2026-11-22T06:40:31.126Z`, `42` public videos = `7` longs + `35` Shorts, `4,422` total views, `6` subscribers)
  - `05_Analytics/hos/studio_ctr.json` (`readAt: 2026-11-22T07:12:32.334030+00:00`, lifetime Studio impressions, CTR, average view %, and Shorts stayed-to-watch %)
  - `05_Analytics/hos/channel_daily.json` (`through: 2026-11-20`, `86` daily rows, `4,450` settled views, `623` watch minutes, `+6` subs; last 7 days `13–19 Nov` = `529` views, `56` watch minutes) and `05_Analytics/hos/REPORT.md`
  - `05_Analytics/LEARNINGS.md` (rules `1–22` plus HOS rules `23–41`) and `05_Analytics/hos/search_research/2026-11-20.md` (`J3224`)
- **Elapsed-day denominator (`age_days`):** `max((date(2026, 11, 22) - date.fromisoformat(publishedAt[:10])).days, 1)` (`views/day = views / age_days`).
- **Low-sample statistical caveat (`Rule 1` / `RULING.md`):** Five public HOS longs have `5–15` lifetime views (`17–69` impressions), and newer/bottom Shorts have `4–49` views. Patterns inferred from small-N rows are treated explicitly as **hypotheses**, not settled laws.

### 1a. All `7` Public HOS Longs — Ranked by Views/Day Since Publish (`2026-11-22`)

| Rank | Video ID | Film | Title | Published (`age_days`) | Length | Views (`2026-11-22`) | Views / Day | Studio Impressions (Lifetime) | Studio CTR (Lifetime) | Studio Avg View % (Lifetime) | YTA 28d Views (`through 11-20`) | YTA 28d Avg View % |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **1** | `AL_-qlWko_g` | `002` | *How Did We Discover the Periodic Table?* | `2026-09-17` (`66d`) | `541s` | **162** | **2.45/d** | **1,163** | 3.4% | 21.2% (`115s`) | 13 | 23.33% |
| **2** | `GHZDsiH7L7A` | `004` | *What's Inside an Atom? Mostly Empty Space* | `2026-10-15` (`38d`) | `525s` | **35** | **0.92/d** | **840** | 1.4% | 23.5% (`124s`) | 9 | 54.97% |
| **3** | `VbPubYd6Fbs` | `006` | *The Willow Tree That Was Made of Air* | `2026-11-05` (`17d`) | `532s` | **15** | **0.88/d** | 69 | 4.3% | **48.1%** (`256s`) | 15 | 48.15% |
| **4** | `ETynHpIYLeY` | `007` | *How Was the First Vaccine Made? (And Why It's Named After a Cow)* | `2026-11-12` (`10d`) | `532s` | **7** | **0.70/d** | 43 | 4.7% | 19.3% (`103s`) | 7 | 19.29% |
| **5** | `wwcjcFfC-5M` | `005` | *The Tied Arm That Proved Your Blood Circulates* | `2026-10-29` (`24d`) | `529s` | **6** | **0.25/d** | **17** | 17.6% | **7.8%** (`41s`) | 6 | 7.78% |
| **6** | `_C92tIJCk8A` | `001` | *How Did We Discover Germs?* | `2026-09-03` (`80d`) | `365s` | **7** | **0.09/d** | 45 | 6.7% | 48.1% (`176s`) | 0 | — |
| **7** | `frP_YrNShsU` | `003` | *How Did We Discover X-rays?* | `2026-09-24` (`59d`) | `426s` | **5** | **0.08/d** | 43 | 2.3% | 26.6% (`114s`) | 3 | 14.12% |

- **3 Best HOS Longs & What They Share:**
  1. **`AL_-qlWko_g` (`002` *How Did We Discover the Periodic Table?*, `541s`)** — **`2.45` views/day** (`162` views in `66d`), **`1,163` impressions** (`52.4%` of all `2,220` HOS long impressions), `3.4%` CTR, `21.2%` Studio avg view % (`70%` at `0:15`, `50%` at `0:30`).
  2. **`GHZDsiH7L7A` (`004` *What's Inside an Atom? Mostly Empty Space*, `525s`)** — **`0.92` views/day** (`35` views in `38d`), **`840` impressions** (`37.8%` of all HOS long impressions), `1.4%` CTR, `23.5%` Studio avg view % (`54.97%` in 28d YTA; `62%` at `0:15`, `45%` at `0:30`).
  3. **`VbPubYd6Fbs` (`006` *The Willow Tree That Was Made of Air*, `532s`)** — **`0.88` views/day** (`15` views in `17d`, small-N hypothesis), `69` impressions, `4.3%` CTR, channel-best **`48.1%` Studio avg view % (`256s` = 4m 16s)** (`48.15%` 28d YTA).
  - **Shared pattern (Subject, Title Shape, Opening, Thumbnail Concept, Length):** `002` and `004` generate **`90.2%` (`2,003 / 2,220`) of all HOS long impressions** and **`83.1%` (`197 / 237`) of all HOS long views** because they target massive, universal science-curriculum search subjects (`Periodic Table`, `Inside an Atom`) with plain question titles backed by huge `TED-Ed` / education neighbour pools (`Rules 1, 15, 26`), run **`8.75–9.0 min` (`525–541s`)**, use one iconic painted 3D hero object on the right with cream-and-gold serif lettering, and open with a concrete physical puzzle (`Rule 10`). `006` confirms that a single tangible proof-experiment story holds viewers (`48.1%` avg view %) once clicked, while lacking a search-phrase title limited its impressions (`69`).
- **3 Worst HOS Longs & What They Share (Small-N Hypotheses):**
  1. **`frP_YrNShsU` (`003` *How Did We Discover X-rays?*, `426s`)** — **`0.08` views/day** (`5` views in `59d`), `43` impressions, `2.3%` CTR, `26.6%` Studio avg view %.
  2. **`_C92tIJCk8A` (`001` *How Did We Discover Germs?*, `365s`)** — **`0.09` views/day** (`7` views in `80d`), `45` impressions, `6.7%` CTR, `48.1%` Studio avg view %.
  3. **`wwcjcFfC-5M` (`005` *The Tied Arm That Proved Your Blood Circulates*, `529s`)** — **`0.25` views/day** (`6` views in `24d`), channel-low **`17` impressions**, `17.6%` CTR (tiny N), and channel-low **`7.8%` Studio avg view % (`41s`)**.
  - **Shared pattern:** `005` used a literary statement title with zero searchable query phrase (`Rule 26` miss), starving impressions to `17`; `001` (`365s`) and `003` (`426s`) premiered early on a near-zero-subscriber channel with shorter `6–7 min` runtimes and generic `How Did We Discover...` survey titles instead of a concrete search phrase + physical twist (`Rules 10, 15, 23, 26`).

### 1b. All `35` Public HOS Shorts — Ranked by Views/Day Since Publish (`2026-11-22`)

| Rank | Video ID | Title | Published (`age_days`) | Len | Views (`2026-11-22`) | Views / Day | Studio Views | Studio Stayed % | Studio Avg View % | Likes | 28d Search / Feed |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **1** | `xzKoHg0E0_U` | *What Is Dalton's Atomic Theory?* | `2026-11-16` (`6d`) | `25s` | **232** | **38.67/d** | 223 | **51.9%** | 61.0% (`15s`) | 0 | `182 / 26` |
| **2** | `29bpGAI0wb8` | *What happens if you keep cutting gold in half?* | `2026-10-16` (`37d`) | `25s` | **1,229** | **33.22/d** | 1,228 | 40.8% | 44.1% (`11s`) | 12 | `9 / 0` (d1 `1,111` feed) |
| **3** | `Wvjd8g0CpzE` | *The Blood Vessels Finer Than a Hair* | `2026-11-15` (`7d`) | `26s` | **217** | **31.00/d** | 215 | **14.6%** | **76.6%** (`20s`) | 3 | `15 / 199` |
| **4** | `Bks_JLId1ew` | *How Do Plants Make Oxygen?* | `2026-11-21` (`1d`) | `26s` | 21 | 21.00/d | — | — | — | 0 | early (`<48h`) |
| **5** | `PFj6172YU4Q` | *One Tight Band Proved Your Blood Goes Round* | `2026-11-08` (`14d`) | `27s` | 221 | 15.79/d | 221 | **16.7%** | 61.5% (`17s`) | 3 | `32 / 189` |
| **6** | `l8bxm9L3zl8` | *How Does a Blood Pressure Cuff Work?* | `2026-11-20` (`2d`) | `24s` | 27 | 13.50/d | 25 | 36.0% | 67.8% (`16s`) | 0 | early (`44h`) |
| **7** | `AMSriTQ-lcQ` | *Are Marie Curie's Notebooks Still Radioactive?* | `2026-10-28` (`25d`) | `22s` | 274 | 10.96/d | 274 | 22.7% | **76.9%** (`17s`) | 6 | `41 / 227` |
| **8** | `OnJ8MFu0Mi0` | *How Did John Snow Stop Cholera?* | `2026-10-26` (`27d`) | `23s` | 231 | 8.56/d | 231 | 29.6% | 65.7% (`15s`) | 8 | `27 / 202` |
| **9** | `pWySvZsneZg` | *Why Gold Foil Bounced Rutherford's Particles Back* | `2026-11-01` (`21d`) | `25s` | 137 | 6.52/d | 137 | 37.2% | **112.4%** (`28s`) | 2 | `82 / 53` |
| **10** | `oKqmnJNGiHg` | *How Was Phosphorus Discovered?* | `2026-10-21` (`32d`) | `23s` | 194 | 6.06/d | 193 | 42.0% | **88.3%** (`20s`) | 7 | `32 / 2` |
| **11** | `-3L6HzJ_d_4` | *What Is the Pasteur Swan Neck Flask Experiment?* | `2026-10-27` (`26d`) | `19s` | 139 | 5.35/d | 138 | **78.7%** | **75.0%** (`14s`) | 1 | `129 / 9` |
| **12** | `cLKDiYP55J8` | *What Was the Edward Jenner Experiment?* | `2026-11-13` (`9d`) | `23s` | 47 | 5.22/d | 46 | 43.5% | 67.7% (`16s`) | 0 | `40 / 3` |
| **13** | `clV6E10NLPw` | *The spray that stopped surgery killing patients* | `2026-10-20` (`33d`) | `25s` | 155 | 4.70/d | 155 | 23.4% | 57.8% (`14s`) | 4 | `5 / 0` |
| **14** | `qOZgess30h0` | *Invisible life is still everywhere* | `2026-10-13` (`40d`) | `24s` | 169 | 4.22/d | 169 | 25.1% | 39.8% (`10s`) | 5 | `1 / 0` |
| **15** | `c2q7w0pgcn8` | *Who Discovered Infrared Light?* | `2026-10-19` (`34d`) | `23s` | 138 | 4.06/d | 138 | 43.5% | **105.3%** (`24s`) | 1 | `8 / 1` |
| **16** | `BW_CFAX-mxc` | *Is the Heart a Pump?* | `2026-10-31` (`22d`) | `22s` | 89 | 4.05/d | 89 | 32.9% | 81.7% (`18s`) | 1 | `25 / 64` |
| **17** | `Rl2uZ-KOTl8` | *Your Heart Pumps More Blood Than You Have* | `2026-10-30` (`23d`) | `25s` | 78 | 3.39/d | 78 | 26.6% | 53.6% (`13s`) | 4 | `12 / 64` |
| **18** | `xHnIi9GqOsM` | *Why Do Veins Have Valves?* | `2026-11-05` (`17d`) | `23s` | 42 | 2.47/d | 42 | 20.6% | 61.5% (`14s`) | 0 | `16 / 26` |
| **19** | `qW2OsD4mujc` | *The Four Elements Were Wrong* | `2026-11-03` (`19d`) | `24s` | 34 | 1.79/d | 34 | 57.7% | 192.6% (`46s`) | 0 | `31 / 3` |
| **20** | `TbMMJSRKC3U` | *He said every eighth element repeats* | `2026-10-18` (`35d`) | `27s` | 62 | 1.77/d | 62 | 25.5% | 123.3% (`33s`) | 1 | `5 / 0` |
| **21** | `LCZRHUyTiq0` | *What Are Cathode Rays?* | `2026-10-23` (`30d`) | `26s` | 49 | 1.63/d | 49 | 29.8% | 50.0% (`13s`) | 2 | `10 / 2` |
| **22** | `iqToagXnjX0` | *Microbes in a drop of pond water* | `2026-09-06` (`77d`) | `25s` | 113 | 1.47/d | 113 | 28.3% | 77.9% (`19s`) | 1 | `3 / 0` |
| **23** | `ChbsigHD5_o` | *How Do Plants Clean the Air?* | `2026-11-18` (`4d`) | `25s` | 5 | 1.25/d | 3 | — | 11.3% (`3s`) | 0 | `1 / 0` |
| **24** | `H1y0DXFVmw8` | *Germs don't cast a shadow* | `2026-09-06` (`77d`) | `25s` | 80 | 1.04/d | 80 | 19.8% | 59.5% (`15s`) | 1 | `1 / 0` |
| **25** | `xgx2lYHhYZM` | *Why Is It Called a Vaccine?* | `2026-11-17` (`5d`) | `25s` | 4 | 0.80/d | 4 | 100.0% | 62.4% (`16s`) | 0 | `3 / 0` |
| **26** | `xvanpsLeADE` | *How did Röntgen see bones without cutting* | `2026-09-26` (`57d`) | `25s` | 40 | 0.70/d | 40 | 23.3% | 50.3% (`13s`) | 0 | `1 / 0` |
| **27** | `oowAOWTBoq0` | *How X-rays Were Discovered by Accident* | `2026-09-25` (`58d`) | `25s` | 32 | 0.55/d | 32 | 47.6% | 331.1% (`83s`) | 1 | `5 / 0` |
| **28** | `nba0-f7PPeU` | *Why tellurium sat before iodine* | `2026-09-21` (`62d`) | `25s` | 34 | 0.55/d | 34 | 60.7% | 42.7% (`11s`) | 1 | `3 / 0` |
| **29** | `nFQRWmpulTQ` | *He predicted a metal before it was found* | `2026-09-19` (`64d`) | `25s` | 34 | 0.53/d | 34 | 66.7% | 55.9% (`14s`) | 0 | `0 / 0` |
| **30** | `8_Edn_HCi1s` | *Germs hitch a ride on you* | `2026-09-06` (`77d`) | `25s` | 38 | 0.49/d | 38 | 34.4% | 34.2% (`9s`) | 0 | `6 / 0` |
| **31** | `uU12JA5rMWg` | *The periodic table's empty chairs* | `2026-09-18` (`65d`) | `25s` | 30 | 0.46/d | 30 | 66.7% | 58.8% (`15s`) | 0 | `0 / 0` |
| **32** | `sILtQxgYQk8` | *A flask that proved germs come from outside* | `2026-09-06` (`77d`) | `25s` | 24 | 0.31/d | 24 | 41.7% | 36.7% (`9s`) | 0 | `0 / 0` |
| **33** | `CnHwX1L9XHg` | *Gallium sat where the table said* | `2026-09-20` (`63d`) | `26s` | 16 | 0.25/d | 16 | 30.4% | 33.5% (`9s`) | 0 | `0 / 0` |
| **34** | `zI_eD3vFWmE` | *The first X-ray showed a wedding ring* | `2026-09-27` (`56d`) | `25s` | 9 | 0.16/d | 9 | 50.0% | 64.0% (`16s`) | 0 | `0 / 0` |
| **35** | `LanTHJckYx8` | *What other table has empty chairs?* | `2026-09-22` (`61d`) | `26s` | 4 | 0.07/d | 4 | 33.3% | 23.1% (`6s`) | 0 | `0 / 0` |

- **3 Best HOS Shorts & What They Share:**
  1. **`xzKoHg0E0_U` (*What Is Dalton's Atomic Theory?*, `25s`)** — **`38.67` views/day** (`232` views in `6d`, #1 views/day on channel), **`51.9%` stayed-to-watch (`WATCH`)**, `61.0%` avg view %, driven by **`182` YouTube search views** in 28d (`Rule 41` proof).
  2. **`29bpGAI0wb8` (*What happens if you keep cutting gold in half?*, `25s`)** — **`33.22` views/day** (`1,229` lifetime views, #1 HOS video overall), `40.8%` stayed-to-watch, `44.1%` avg view %, `12` likes.
  3. **`-3L6HzJ_d_4` (*What Is the Pasteur Swan Neck Flask Experiment?*, `19s`)** — **`5.35` views/day** (`139` views in `26d`), channel-best **`78.7%` stayed-to-watch (`PASS ≥60%`)** and **`75.0%` avg view % (`PASS ≥70%`)**, **`129` search views (`92.8%`)** — the only mature `100+`-view HOS Short to pass both targets, and the only `19 s` cut (matching Ben's 19 Nov `16–19 s` house rule); reinforced by loop winners `pWySvZsneZg` (`112.4%` avg view %, `137`v, `82` search), `c2q7w0pgcn8` (`105.3%` avg view %, `43.5%` stayed, `138`v), and `oKqmnJNGiHg` (`88.3%` avg view %, `42.0%` stayed, `194`v).
  - **Shared pattern:** Direct positive search questions naming a specific **curriculum entity, experiment, or physical paradox** (*Dalton's Atomic Theory*, *Pasteur Swan Neck Flask Experiment*, *cutting gold in half*, *Rutherford's gold foil*) win both search discovery and stayed-to-watch (`40.8–78.7%`), while tighter cuts (`19–23s`), `≤1.0s` loop tails, zero CTA, and payoff withheld until `≥70%` push avg view % to `75–112%` (`Rules 1, 2, 3, 6, 24, 27, 28, 32, 41`).
- **3 Worst HOS Shorts & What They Share (Small-N Hypotheses):**
  1. **`LanTHJckYx8` (*What other table has empty chairs?*, `26s`)** — **`0.07` views/day** (`4` views in `61d`), `33.3%` stayed-to-watch, `23.1%` avg view % (`6s`).
  2. **`zI_eD3vFWmE` (*The first X-ray showed a wedding ring*, `25s`)** — **`0.16` views/day** (`9` views in `56d`), `50.0%` stayed-to-watch, `64.0%` avg view %.
  3. **`CnHwX1L9XHg` (*Gallium sat where the table said*, `26s`)** — **`0.25` views/day** (`16` views in `63d`), `30.4%` stayed-to-watch, `33.5%` avg view % — alongside recent feed statement flops `Wvjd8g0CpzE` (**`14.6%` stayed MISS** on `215` Studio views) and `PFj6172YU4Q` (**`16.7%` stayed MISS** on `221` Studio views) plus generic non-entity questions `ChbsigHD5_o` (`5`v, `11.3%` avg view %) and `xgx2lYHhYZM` (`4`v, `0%` feed).
  - **Shared pattern:** Cryptic riddles, past-tense statements lacking a searchable subject, generic "how/why" questions without a named experiment/device, and health/vaccine framing collapse either stayed-to-watch (`14.6–16.7%`) or impressions (`Rules 1, 28, 32, 36, 41`).

---

## 2. Overlap & Non-Duplication Check (`2026-11-22`)

Checked against:
- All folders in `02_Video-Projects/` (`000`–`018`, `099`–`119` on `main`, plus `130` in this PR),
- Open HOS topic PRs `#659` (`120` Why Do We Cry, `121` Why Do Cats Purr), `#682` (`122` Why Do We Sneeze, `123` Why Does Hair Turn Grey), `#689` (`124` Why Is the Ocean Salty, `125` What Causes the Tides), `#706` (`126` What Is the Higgs Boson, `127` How Do Airplanes Fly / Wright Brothers Wind Tunnel), and `#724` (`128` Why Do We Use AC Instead of DC / Edison vs Tesla, `129` How Was the Microwave Invented),
- All `011`–`095` backlog entries in `00_Brand/Channel-Setup/VIDEO_BACKLOG.json` and `00_Brand/Channel-Setup/ideas/` (`009_The-Falling-Moon-Gravity` covers Isaac Newton's 1666–1687 universal gravitation; `025_Young-Fresnel-Einstein-Light` covers Young's 1801 double-slit, Arago's 1819 spot, and Einstein's March 1905 photoelectric effect; **no** film covers Michelson-Morley's 1887 failed ether drift, Einstein's June 1905 Special Relativity & November 1915 General Relativity, Arthur Eddington & Frank Dyson's 29 May 1919 solar eclipse photographic proof on Príncipe and Sobral, or why GPS satellites need relativistic time corrections every day),
- `jobs/WIP.json` (`active` and `next_hos`).
- **Result:** **Zero overlap.**

---

## 3. Packaging, Why It Should Work & Search/Neighbour Evidence (`Rule 26` + `neighbours.py` + `public_search.py`)

- **Title A (Primary Proposal, `LEARNINGS.md` Rules 1, 15, 23, 26 — `48 chars ≤ 50`, `0` exact collisions):** `What Is the Theory of Relativity? (1919 Eclipse)`
- **Title B (Test & Compare Arm 2, `Rule 23` — `58 chars ≤ 70`, `0` exact collisions):** `How a 1919 Solar Eclipse Proved Einstein Beat Isaac Newton`
- **Title C (`Rule 26` / `J3224` Cluster 2 — `63 chars ≤ 70`, `0` exact collisions):** `Theory of Relativity Explained: The 1919 Eclipse That Proved It`
- **One-Line Hook:** For 230 years Isaac Newton's law of gravity seemed unbreakable — until a British astronomer sailed through pouring rain to a West African island on 29 May 1919, photographed stars beside a darkened Sun, and proved a German patent clerk had bent space and time itself.
- **Why It Should Work (Past Winners & `LEARNINGS.md` Rules):**
  - Resembles HOS's top two impression-and-view longs — **`002` Periodic Table (`AL_-qlWko_g`, `162` views, `2.45/d`, `1,163` impressions, `3.4%` CTR)** and **`004` Inside an Atom (`GHZDsiH7L7A`, `35` views, `0.92/d`, `840` impressions)** — by leading with an exact, massive-volume physics curriculum search question (`What Is the Theory of Relativity?`, `autocomplete = yes`) backed by **`5` strictly on-topic education neighbours `≥1M` views** including **`2` TED-Ed ★** videos (`5.92M` & `2.73M`), `Veritasium` (`8.55M`), `minutephysics` (`1.86M`), and `CrashCourse` (`1.45M`) (`Rules 1, 15, 26`).
  - Matches **`006` Willow Tree (`VbPubYd6Fbs`, `48.1%` Studio avg view %)** by anchoring an abstract theory inside one physical, nail-biting proof event — two eclipse glass photographic plates exposed through parting clouds on Príncipe and Sobral in May 1919 — and directly chains from HOS `009` (*Why Doesn't the Moon Fall to Earth?*) via end screens (`Rules 10, 20, 30`).
  - Directly advances **`J3224` Cluster 2** (*Nuclear, Quantum & Modern Physics Breakthroughs*): `theory of relativity` (**`29,476`/mo**, **`+84.4%` growth**, comp `49`) + `albert einstein documentary` (**`6,141`/mo**, comp `38`, **`+88.7%` growth**, **9/10 US SERP gap**), backed by verified sub-50k US breakouts (`Quantara Explains` 3.1K US → `7.6K` `8.9×`, `Think Like Feynman` 12.1K US → `6K` `7.7×`, `Science Retold` 3.4K US → `61.9K` `13×`, `Enjoy History` 10.1K → `77.3K` `9×`).
  - Resembles top HOS Shorts **`xzKoHg0E0_U` (*What Is Dalton's Atomic Theory?*, `38.67/d`, `51.9%` stayed, `182` search views)**, **`-3L6HzJ_d_4` (*What Is the Pasteur Swan Neck Flask Experiment?*, `78.7%` stayed PASS, `75.0%` avg viewed PASS)**, and **`pWySvZsneZg` (*Why Gold Foil Bounced Rutherford's Particles Back*, `112.4%` avg view % LOOP)** by turning named relativity milestones (`1919 Solar Eclipse`, `GPS Satellites`) into punchy `16–19 s` search-question loops (`Rules 2, 3, 6, 24, 27, 28, 32, 41` + Ben 19 Nov Shorts house rules).
- **3-Way Thumbnail Test & Compare Plan (`LEARNINGS.md` Rules 11, 12, 14 + `THUMBNAIL_AND_TITLE_RULES.md` §2.1–2.B):**
  - **Thumb A (Hero Object — The 1919 Eclipse Glass Plate & Shifted Star):** Painted 3D house-style key art: in warm observatory light on the right two-thirds, a brass astrographic telescope and a luminous glass photographic negative showing the black eclipsed Sun's golden corona with a bright star visibly displaced sideways by a curving golden ray; the Explorer small at lower left holding a magnifying glass; cream/gold serif text in the clear left band: `STARLIGHT BENT` (`2 words`, gold on `BENT`, zero overlap on hero).
  - **Thumb B (`Rule 14` Bright High-Contrast Variant — Daylight Sunlit Brass Clock vs Falling Lift):** Crisp bright cream-and-sky palette on the right showing two gleaming golden pocket watches ticking at different speeds beside a curved translucent light beam; Explorer small at lower left; serif text on the clear left band: `TIME SLOWS` (`2 words`, gold on `SLOWS`).
  - **Thumb C (Newton's Apple vs Bent Space):** Painted 3D close-up on the right of a glowing golden orb resting on a curved woven brass-and-vellum spacetime grid bending a beam of starlight straight past it; Explorer small at lower left; serif text on the left band: `NEWTON WAS WRONG` (`3 words`, gold on `WRONG`).
- **Signed-out YouTube Autocomplete (`2026-11-22`, `10` queries / `70` search rows in `11_Upload-Package/evidence_2026-11-22_public_search.json`):**
  - `"what is the theory of relativity"` → **`autocomplete = yes`** (`what is the theory of relativity`, `what is the theory of relativity of albert einstein`, `what is the general theory of relativity`)
  - `"theory of relativity explained"` → **`autocomplete = yes`** (`theory of relativity explained`, `theory of relativity explained simply`)
  - `"how did einstein prove relativity"` → **`autocomplete = yes`** (`how did einstein prove relativity`)
  - `"einstein 1919 solar eclipse"` → **`related: 1919 solar eclipse einstein`**
  - All `5` proposed long and Short titles → **`0` exact collisions**.
- **Rule 26(a) Two Ranking Videos (`≥10,000` views, retrieved `2026-11-22`):**
  1. `Science ABC` — [`yuD34tEpRFw`](https://youtu.be/yuD34tEpRFw) *Time Dilation - Einstein's Theory Of Relativity Explained!* (**`9,685,020` views**)
  2. `Arvin Ash` — [`tzQC3uYL67U`](https://youtu.be/tzQC3uYL67U) *General Relativity Explained simply & visually* (**`7,384,849` views**; plus `StarTalk` **`3,512,623` views**, `Vox` [`HLxvq_M4218`](https://youtu.be/HLxvq_M4218) *The eclipse photo that made Einstein famous* **`2,196,555` views**, `SpaceRip` [`g8ZO5XvHORI`](https://youtu.be/g8ZO5XvHORI) **`1,881,348` views**, and `minutephysics` [`eNhJY-R3Gwg`](https://youtu.be/eNhJY-R3Gwg) **`1,855,197` views**)
- **Neighbour Gate (`neighbours.py`):** **PASS (`7` raw / `5` strictly on-topic education videos `≥1,000,000` views, `TED-Ed/TED: yes`)** — saved in [`11_Upload-Package/evidence_2026-11-22_neighbours.json`](11_Upload-Package/evidence_2026-11-22_neighbours.json):
  1. `Veritasium` — [`eyZEqSPeMwg`](https://youtu.be/eyZEqSPeMwg) *Relativity is so much weirder than we thought...* (**`8,545,878` views**)
  2. `TED-Ed` ★ — [`h8GqaAp3cGs`](https://youtu.be/h8GqaAp3cGs) *Einstein's twin paradox explained - Amber Stuver* (**`5,919,102` views**)
  3. `TED-Ed` ★ — [`91XI7M9l3no`](https://youtu.be/91XI7M9l3no) *Einstein's miracle year - Larry Lagerstrom* (**`2,733,278` views**)
  4. `minutephysics` — [`eNhJY-R3Gwg`](https://youtu.be/eNhJY-R3Gwg) *General Relativity Explained in 7 Levels of Difficulty* (**`1,855,197` views**)
  5. `CrashCourse` — [`AInCqm5nCzw`](https://youtu.be/AInCqm5nCzw) *Special Relativity: Crash Course Physics #42* (**`1,449,325` views**; plus `TED-Ed` ★ [`gkTVlYDB21g`](https://youtu.be/gkTVlYDB21g) *The physics behind Einstein's most famous equation* **`423,973` views**, `Khan Academy` [`HIQ5hnm61LQ`](https://youtu.be/HIQ5hnm61LQ) **`363,369` views**, and `Khan Academy` [`3G_Q6AggQF8`](https://youtu.be/3G_Q6AggQF8) *Michelson–Morley Experiment* **`310,265` views**)
  - *(Transparently excluded from strict count: `TED-Ed` `1rDVz_Fb6HQ` Einstein's Riddle logic puzzle `13,415,539`, and `TED-Ed` `DbbWx2COU0E` Entangled states `1,291,010`.)*

---

## 4. Candidate 4-Act Discovery Outline (All Claims UNVERIFIED Pending `SOURCES.md` & `facts` Lane)

- **Cold Open (0:00–0:45, Proof-First Apparatus Open per `Rules 10 & 30`, UNVERIFIED):**
  - `0:00–0:05`: Tropical rain beats on a canvas tent on the island of Príncipe (`29 May 1919`) as **Arthur Eddington** peers anxiously at the clouds — minutes before a total solar eclipse that will put Isaac Newton's 230-year-old theory of gravity on trial.
  - `0:05–0:15` (Apparatus / Physical Proof): Hard cut onto Eddington's **brass astrographic telescope** tracking the darkened Sun through a sudden gap in the clouds, then straight onto the **developed glass photographic plate** under a micrometre microscope showing Hyades star dots shifted by **`1.75 arcseconds`** — twice what Newton predicted (`1.75" vs 0.87"` ink scale counter). Zero *"In this film..."* agenda line.
  - `0:15–0:45`: Those tiny pinpricks of bent starlight proved that gravity is not an invisible pulling rope at all — and without the relativity equations verified on that glass plate, your phone's GPS map would drift off course by more than **10 kilometres every single day**.
- **Act I — The 1887 Broken Speedometer & The Bern Patent Desk (1887–1905, UNVERIFIED):** Physicists in the 1880s assumed light sailed through an invisible space-filling medium called the **luminiferous ether** — meaning Earth's orbit through space should create a measurable "ether wind." In **1887** in Cleveland, **Albert Michelson** and **Edward Morley** floated a heavy sandstone interferometer on a **pool of liquid mercury** to catch that wind — and measured **zero difference** in the speed of light no matter which direction Earth moved! Eighteen years later in **June 1905**, 26-year-old patent clerk **Albert Einstein** in Bern, Switzerland (*Annalen der Physik*, *"On the Electrodynamics of Moving Bodies"*) flipped the puzzle inside out: if the **speed of light (`~300,000 km/s`)** is the exact same for every observer, then **time and distance themselves must stretch and shrink** (**Special Relativity**) — and months later (`September 1905`) mass and energy become two forms of the same thing ($E = mc^2$).
- **Act II — The "Happiest Thought" & The Missing Twist of Mercury (1907–1915, UNVERIFIED):** Special relativity had one huge gap: it ignored gravity! In **November 1907** at his Bern desk, Einstein had what he called the *"happiest thought of my life"*: a person falling freely off a roof feels **zero weight** — indistinguishable from floating in deep space, while an accelerating elevator feels identical to gravity (**the Equivalence Principle**). That meant a beam of light crossing an accelerating room must curve downward — so gravity must bend light! After eight gruelling years of curved-space geometry (**General Relativity**, **November 1915**), Einstein checked a 56-year-old astronomical mystery — **Mercury's orbit** creeping forward by an unexplained **`43 arcseconds` per century** — and his new equations spat out `43 arcseconds` on the first try!
- **Act III — The 29 May 1919 Eclipse Gamble (1919, UNVERIFIED):** Still, Britain and Germany had just fought the First World War, and physicists wanted a fresh prediction nobody had seen before. Astronomer Royal **Frank Dyson** spotted the perfect test: on **29 May 1919**, a total solar eclipse would darken the Sun directly in front of the bright **Hyades star cluster**. Newton's gravity predicted starlight grazing the Sun's rim would bend by **`0.87 arcseconds`**; Einstein's curved spacetime predicted **`1.75 arcseconds`** — **exactly double**. Dyson sent **Andrew Crommelin & Charles Davidson** to **Sobral, Brazil**, and **Arthur Eddington & Edwin Cottingham** to **Príncipe** off West Africa. Through cloudbreaks on Príncipe (yielding two usable plates out of 16) and clear skies in Sobral (where heat warped the larger mirror, leaving the smaller 4-inch lens razor-sharp), the teams measured **`1.61" ± 0.30"`** (Príncipe) and **`1.98" ± 0.12"`** (Sobral). On **6 November 1919** at the Royal Society in London, J. J. Thomson declared Einstein's work *"one of the greatest achievements in the history of human thought"* — making Einstein world-famous overnight.
- **Act IV — Why Your Phone Proves Relativity Every Second (1971–Today, UNVERIFIED):** Relativity wasn't just an eclipse curiosity. In **October 1971**, **Joseph Hafele and Richard Keating** flew four caesium atomic clocks around the world on commercial airliners and measured the exact nanosecond drift predicted by Einstein. Today, every **GPS satellite** orbits **~20,200 km** above Earth: moving at `~14,000 km/h` makes its atomic clocks tick **`~7 microseconds` slower** per day (Special Relativity), while sitting in weaker gravity makes them tick **`~45 microseconds` faster** per day (General Relativity) — a net **`+38 microseconds` per day**. Without Einstein's built-in correction, light travels **~11 kilometres in 38 microseconds**, rendering every smartphone map useless within 24 hours!

---

## 5. Two Candidate Search-Titled Shorts (`Ben 19 Nov 16–19 s Rules` + `Rules 32 & 41` — UNVERIFIED Concepts Only)

- **Short `S01`:** *How Did the 1919 Solar Eclipse Prove Einstein's Relativity?* (`59 chars`, `0` exact collisions; positive named-event search question backed by `"einstein 1919 solar eclipse"` `related: 1919 solar eclipse einstein` and `"how did einstein prove relativity"` `autocomplete = yes`)
  - **16–19 s Loop Concept (`Ben 19 Nov Rules`):**
    - **Frame 0 (`0.0 s`, premium 3D cartoon moving plate, zero Explorer, zero bars):** Moving 3D shot of the Moon snapping across the Sun into totality, revealing bright stars beside the golden corona whose light beams visibly curve around the Sun's rim. On-screen line-1 concrete fact caption: `Starlight bent twice as far` (yellow on `twice`).
    - **Spoken hook (`≤1.5 s` titled noun + surprise, zero dateline, zero meta-promise):** *"A total solar eclipse proved Isaac Newton's gravity was wrong — because starlight bent twice as far as he predicted."*
    - **Single mid-Short `Teach on screen` overlay (`~9.5 s`, inside 16:9 band):** `1.75" VS NEWTON'S 0.87"`.
    - **Payoff (`≥70%` runtime, `~13.5 s / 18.0 s`):** Arthur Eddington's 1919 eclipse plates matched Einstein's `1.75-arcsecond` curved-space prediction, proving gravity bends spacetime itself — looping smoothly back into *"A total solar eclipse proved..."* (`<0.3 s` visual seam match, `0` CTA).
- **Short `S02`:** *Why Do GPS Satellites Need Einstein's Relativity to Work?* (`57 chars`, `0` exact collisions; positive named-device search question backed by `"what is the theory of relativity"` `autocomplete = yes` and `minutephysics` `998K` ranking video)
  - **16–19 s Loop Concept (`Ben 19 Nov Rules`):**
    - **Frame 0 (`0.0 s`, premium 3D cartoon moving plate, zero Explorer, zero bars):** Moving 3D shot of a golden GPS satellite orbiting high above Earth with a glowing atomic clock ticking visibly faster than a matching clock on a smartphone map below. On-screen line-1 concrete fact caption: `GPS drifts 11 km a day` (yellow on `11 km`).
    - **Spoken hook (`≤1.5 s` titled noun + surprise, zero dateline, zero meta-promise):** *"Without Einstein's theory of relativity, your phone's GPS would drift eleven kilometres off course every single day."*
    - **Single mid-Short `Teach on screen` overlay (`~9.5 s`, inside 16:9 band):** `+38 MICROSECONDS / DAY`.
    - **Payoff (`≥70%` runtime, `~13.5 s / 18.0 s`):** High orbit speed slows satellite clocks by `7 microseconds` while weaker gravity speeds them up by `45` — a `+38-microsecond` daily mismatch fixed only by Einstein's equations, looping back into *"Without Einstein's theory of relativity..."* (`<0.3 s` visual seam match, `0` CTA).
