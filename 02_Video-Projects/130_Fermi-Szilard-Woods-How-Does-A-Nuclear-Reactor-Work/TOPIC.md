# Topic Brief — `130_Fermi-Szilard-Woods-How-Does-A-Nuclear-Reactor-Work` (`HOS:130` — Rule-E Pre-Cleared GO `96.6 / 100` in `next_hos`)

> **RULE-E & RULE G STATUS (`J3348` → `J3350`, `2026-11-22`):**
> - **Rule-E Topic Verdict (`J3350`, `macbook` / `review` lane):** **GO (`96.6 / 100` · `9.66 / 10` Opportunity Score)** — pre-cleared in `jobs/WIP.json` `next_hos` under **Rule G** (`active` holds `4/4` HOS slots: `008`, `009`, `010`, `013`). See [`11_Upload-Package/TOPIC_GO_NO_GO_SHEET.md`](11_Upload-Package/TOPIC_GO_NO_GO_SHEET.md) and [`11_Upload-Package/TOPIC_OPPORTUNITY_SCORE.md`](11_Upload-Package/TOPIC_OPPORTUNITY_SCORE.md). Nothing starts in production (`status.json` stages remain all `todo`) until an active HOS WIP slot opens.
> - **2027 Search Plan Alignment (`J3224` `hos-search-2027-01`, `needsBen` in `studio/plan.json`):** Fits **Cluster 2 (*Nuclear, Quantum & Modern Physics Breakthroughs*, Film #2)** — strictly laboratory physics and engineering inside HOS's 3D cartoon discovery lane (zero combat/military overlap with Field Order History; zero overlap with `022_Meitner-Hahn-Nuclear-Fission`, which ends with the December 1938 discovery of fission). Independently passes every currently in-force HOS topic gate.
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
  3. **`-3L6HzJ_d_4` (*What Is the Pasteur Swan Neck Flask Experiment?*, `19s`)** — **`5.35` views/day** (`139` views in `26d`), channel-best **`78.7%` stayed-to-watch (`PASS ≥60%`)** and **`75.0%` avg view % (`PASS ≥70%`)**, **`129` search views (`92.8%`)** — the only mature `100+`-view HOS Short to pass both targets, and notably the **only 19 s Short** on the channel (matching Ben's 19 Nov `16–19 s` house rule); reinforced by loop winners `pWySvZsneZg` (`112.4%` avg view %, `137`v, `82` search), `c2q7w0pgcn8` (`105.3%` avg view %, `43.5%` stayed, `138`v), and `oKqmnJNGiHg` (`88.3%` avg view %, `42.0%` stayed, `194`v).
  - **Shared pattern:** Direct positive search questions naming a specific **curriculum entity, experiment, or physical paradox** (*Dalton's Atomic Theory*, *Pasteur Swan Neck Flask Experiment*, *cutting gold in half*, *Rutherford's gold foil*) win both search discovery and stayed-to-watch (`40.8–78.7%`), while tighter cuts (`19–23s`), `≤1.0s` loop tails, zero CTA, and payoff withheld until `≥70%` push avg view % to `75–112%` (`Rules 1, 2, 3, 6, 24, 27, 28, 32, 41`).
- **3 Worst HOS Shorts & What They Share (Small-N Hypotheses):**
  1. **`LanTHJckYx8` (*What other table has empty chairs?*, `26s`)** — **`0.07` views/day** (`4` views in `61d`), `33.3%` stayed-to-watch, `23.1%` avg view % (`6s`).
  2. **`zI_eD3vFWmE` (*The first X-ray showed a wedding ring*, `25s`)** — **`0.16` views/day** (`9` views in `56d`), `50.0%` stayed-to-watch, `64.0%` avg view %.
  3. **`CnHwX1L9XHg` (*Gallium sat where the table said*, `26s`)** — **`0.25` views/day** (`16` views in `63d`), `30.4%` stayed-to-watch, `33.5%` avg view % — alongside recent feed statement flops `Wvjd8g0CpzE` (**`14.6%` stayed MISS** on `215` Studio views) and `PFj6172YU4Q` (**`16.7%` stayed MISS** on `221` Studio views) plus generic non-entity questions `ChbsigHD5_o` (*How Do Plants Clean the Air?*, `5`v, `11.3%` avg view %) and `xgx2lYHhYZM` (*Why Is It Called a Vaccine?*, `4`v, `0%` feed).
  - **Shared pattern:** Cryptic riddles, past-tense statements lacking a searchable subject, generic "how/why" questions without a named experiment/device, and health/vaccine framing collapse either stayed-to-watch (`14.6–16.7%`) or impressions (`Rules 1, 28, 32, 36, 41`).

---

## 2. Overlap & Non-Duplication Check (`2026-11-22`)

Checked against:
- All folders in `02_Video-Projects/` (`000`–`018`, `099`–`119` on `main`),
- Open HOS topic PRs `#659` (`120` Why Do We Cry, `121` Why Do Cats Purr), `#682` (`122` Why Do We Sneeze, `123` Why Does Hair Turn Grey), `#689` (`124` Why Is the Ocean Salty, `125` What Causes the Tides), `#706` (`126` What Is the Higgs Boson, `127` How Do Airplanes Fly / Wright Brothers Wind Tunnel), and `#724` (`128` Why Do We Use AC Instead of DC / Edison vs Tesla, `129` How Was the Microwave Invented),
- All `011`–`095` backlog entries in `00_Brand/Channel-Setup/VIDEO_BACKLOG.json` and `00_Brand/Channel-Setup/ideas/` (`022_Meitner-Hahn-Nuclear-Fission` covers Lise Meitner & Otto Hahn's December 1938 discovery that a neutron can split a uranium nucleus; **no** film covers how a controlled nuclear chain reaction works, Leo Szilard's 1933 chain-reaction patent, Enrico Fermi's 1934 Rome slow-neutron paraffin experiment, or the 2 December 1942 Chicago Pile-1 graphite reactor under Stagg Field stadium with Leona Woods, Walter Zinn, and George Weil),
- `jobs/WIP.json` (`active` and `next_hos`).
- **Result:** **Zero overlap.**

---

## 3. Packaging, Why It Should Work & Search/Neighbour Evidence (`Rule 26` + `neighbours.py` + `public_search.py`)

- **Title A (Primary Proposal, `LEARNINGS.md` Rules 1, 15, 23, 26 — `50 chars ≤ 50`, `0` exact collisions):** `How Does a Nuclear Reactor Work? (Under a Stadium)`
- **Title B (Test & Compare Arm 2, `Rule 23` — `60 chars ≤ 70`, `0` exact collisions):** `The First Nuclear Reactor Was Built on a Squash Court (1942)`
- **Title C (`Rule 26` / `J3224` Cluster 2 Named Scientist — `60 chars ≤ 70`, `0` exact collisions):** `Enrico Fermi: How Scientists Built the First Nuclear Reactor`
- **One-Line Hook:** Beneath the empty bleachers of a Chicago football stadium in freezing December 1942, Enrico Fermi stacked 40,000 hand-carved black graphite bricks with no concrete shield and no cooling pipes — and bet the city on one wooden safety rod tied to a rope that humans could start and stop a nuclear chain reaction.
- **Why It Should Work (Past Winners & `LEARNINGS.md` Rules):**
  - Resembles HOS's top two impression-and-view longs — **`002` Periodic Table (`AL_-qlWko_g`, `162` views, `2.45/d`, `1,163` impressions, `3.4%` CTR)** and **`004` Inside an Atom (`GHZDsiH7L7A`, `35` views, `0.92/d`, `840` impressions)** — by opening with an exact, high-demand physics search question (`How Does a Nuclear Reactor Work?`, `autocomplete = yes`) surrounded by **`9` strictly on-topic education neighbours `≥1M` views** including `TED-Ed` ★ (`3.33M`), `Kurzgesagt` (`8.22M`), and `SmarterEveryDay` (`7.52M` & `3.85M`) (`Rules 1, 15, 26`).
  - Matches **`006` Willow Tree (`VbPubYd6Fbs`, `48.1%` Studio avg view %)** by centring the entire film on one dramatic, self-contained laboratory apparatus (a 20-foot graphite dome inside an abandoned squash court) with a concrete proof moment (`Rule 10`, `Rule 30`).
  - Directly advances **`J3224` Cluster 2** (*Nuclear, Quantum & Modern Physics Breakthroughs*): `enrico fermi` (`9,601`/mo, comp `35`, **9/10 US SERP gap**), parent `manhattan project` (`35,203`/mo, **US 18%, GB 9%**), and proven sub-50k US channel breakouts (`Science Retold` 3.4K US → `28.5K` `6.1×`, `Cosmo Explains` 37K US → `73.4K` `40×`, `Unifying Lens` 1.5K US → `1.7K` `15×`), shifting HOS toward adult US/UK/CA/AU viewers (`$3.42` mid US Education RPM).
  - Resembles top HOS Shorts **`xzKoHg0E0_U` (*What Is Dalton's Atomic Theory?*, `38.67/d`, `51.9%` stayed, `182` search views)**, **`-3L6HzJ_d_4` (*What Is the Pasteur Swan Neck Flask Experiment?*, `78.7%` stayed PASS, `75.0%` avg viewed PASS)**, and **`29bpGAI0wb8` (*What happens if you keep cutting gold in half?*, `1,229` views, `33.22/d`)** by pairing named-entity physics questions with unmistakable 3D cartoon hero objects in the `16–19 s` loop format (`Rules 2, 3, 6, 24, 27, 28, 32, 41` + Ben 19 Nov Shorts house rules).
- **3-Way Thumbnail Test & Compare Plan (`LEARNINGS.md` Rules 11, 12, 14 + `THUMBNAIL_AND_TITLE_RULES.md` §2.1–2.B):**
  - **Thumb A (Hero Object — The Graphite Dome & Cadmium Rod):** Painted 3D house-style key art: warm golden workshop light inside the Stagg Field squash court; on the right two-thirds, the towering stepped black graphite-brick dome with glowing amber uranium cores peeking through a cutaway and a single hand pulling a gleaming silver-cadmium control rod out by inches; the Explorer small at lower left holding a ticking Geiger needle; cream/gold serif lettering in the clear left band: `NO SHIELDING` (`2 words`, gold on `NO`, zero overlap on hero).
  - **Thumb B (`Rule 14` Bright High-Contrast Variant — Snow-Covered Football Stadium Cutaway):** Crisp bright winter daylight cutaway of Stagg Field's concrete football bleachers on the right, slicing open to reveal the warm glowing graphite reactor pile hidden directly underneath the empty stands; Explorer small at lower left; serif lettering on the clear left band: `HIDDEN GRAPHITE PILE` (`3 words`, gold on `HIDDEN`, zero words repeated from Titles A, B, or C per `THUMBNAIL_AND_TITLE_RULES.md` §2.5; refined in `J3350` from `UNDER STAGG FIELD`).
  - **Thumb C (The Axe & Safety Rope):** Painted 3D dramatic close-up on the right of the emergency "ZIP" cadmium control rod suspended by a taut hemp rope above the graphite pile, with a gleaming fire-axe poised beside the rope and a climbing red ink chart behind it; Explorer small at lower left; serif lettering on the left band: `ONE ROPE` (`2 words`, gold on `ONE`).
- **Signed-out YouTube Autocomplete (`2026-11-22`, `11` queries / `80` search rows in `11_Upload-Package/evidence_2026-11-22_public_search.json`; refreshed in `J3350` so Title A and parentheses-stripped Title B carry live 8-row collision proof):**
  - `"how does a nuclear reactor work"` → **`autocomplete = yes`** (`how does a nuclear reactor work`, `how does a nuclear reactor work chernobyl`, `how does a nuclear reactor work on a submarine`, `how does a nuclear reactor work on an aircraft carrier`)
  - `"chicago pile 1"` → **`autocomplete = yes`** (`chicago pile 1`, `chicago pile 1 reactor`, `chicago pile 1 oppenheimer`, `chicago pile one`)
  - `"enrico fermi nuclear reactor"` → **`autocomplete = yes`** (`enrico fermi nuclear reactor`)
  - `"nuclear chain reaction"` → **`autocomplete = yes`** (`nuclear chain reaction`, `nuclear chain reaction animation`, `nuclear chain reaction explained`)
  - All `5` proposed long and Short titles → **`0` exact collisions**.
- **Rule 26(a) Two Ranking Videos (`≥10,000` views, retrieved `2026-11-22`):**
  1. `Kurzgesagt – In a Nutshell` — [`rcOFV4y5z8c`](https://youtu.be/rcOFV4y5z8c) *Nuclear Energy Explained: How does it work? 1/3* (**`8,224,844` views**)
  2. `Elearnin` — [`1U6Nzcv9Vws`](https://youtu.be/1U6Nzcv9Vws) *Nuclear Reactor - Understanding how it works | Physics Elearnin* (**`5,024,242` views**; plus `SmarterEveryDay` [`JVROsxtjoCw`](https://youtu.be/JVROsxtjoCw) **`3,847,425–3,847,436` views**, `TED-Ed` ★ [`R7WPEYGr1Vs`](https://youtu.be/R7WPEYGr1Vs) **`3,332,507` views**, `Animagraffs` [`PRWwXeRIvoI`](https://youtu.be/PRWwXeRIvoI) **`825,335` views**, and `SciShow` [`MLJ1ebNcNLM`](https://youtu.be/MLJ1ebNcNLM) *The World's First Human-Made Nuclear Reactor* **`457,251` views**)
- **Neighbour Gate (`neighbours.py`):** **PASS (`12` raw / `9` strictly on-topic education videos `≥1,000,000` views, `TED-Ed/TED: yes`)** — saved in [`11_Upload-Package/evidence_2026-11-22_neighbours.json`](11_Upload-Package/evidence_2026-11-22_neighbours.json):
  1. `Kurzgesagt – In a Nutshell` — [`Jzfpyo-q-RM`](https://youtu.be/Jzfpyo-q-RM) *Worst Nuclear Accidents in History* (**`10,888,517` views**)
  2. `Kurzgesagt – In a Nutshell` — [`EhAemz1v7dQ`](https://youtu.be/EhAemz1v7dQ) *Do we Need Nuclear Energy to Stop Climate Change?* (**`9,916,883` views**)
  3. `Kurzgesagt – In a Nutshell` — [`rcOFV4y5z8c`](https://youtu.be/rcOFV4y5z8c) *Nuclear Energy Explained: How does it work? 1/3* (**`8,224,844` views**)
  4. `SmarterEveryDay` — [`v0afQ6w3Bjw`](https://youtu.be/v0afQ6w3Bjw) *Refueling a NUCLEAR REACTOR - Smarter Every Day 311* (**`7,524,461` views**)
  5. `SmarterEveryDay` — [`JVROsxtjoCw`](https://youtu.be/JVROsxtjoCw) *I Explored the World's First Nuclear Power Plant (and How It Works) - Smarter Every Day 306* (**`3,847,436` views**)
  6. `TED-Ed` ★ — [`R7WPEYGr1Vs`](https://youtu.be/R7WPEYGr1Vs) *How do nuclear power plants work? - M. V. Ramana and Sajan Saini* (**`3,332,507` views**)
  7. `TEDx Talks` ★ — [`ciStnd9Y2ak`](https://youtu.be/ciStnd9Y2ak) *Why I changed my mind about nuclear power | Michael Shellenberger* (**`2,322,050` views**)
  8. `TEDx Talks` ★ — [`-tAsHGFA-74`](https://youtu.be/-tAsHGFA-74) *How I built a nuclear reactor at the age of 13 | Jamie Edwards* (**`1,576,494` views**)
  9. `TED` ★ — [`5HL1BEC024g`](https://youtu.be/5HL1BEC024g) *Taylor Wilson: My radical plan for small nuclear fission reactors* (**`1,243,751` views**)
  - *(Transparently excluded from strict count: `Kurzgesagt` `mZsaaturR6E` Fusion Power `15,253,905`, `TED-Ed` `GHBb25lzNVM` Nuclear Fallout `2,149,234`, and `TED-Ed` `dcZ0BXJYlUA` Three Gorges hydroelectric dam `1,352,160`.)*

---

## 4. Candidate 4-Act Discovery Outline (All Claims UNVERIFIED Pending `SOURCES.md` & `facts` Lane)

- **Cold Open (0:00–0:45, Proof-First Apparatus Open per `Rules 10 & 30`, UNVERIFIED):**
  - `0:00–0:05`: Snow blows over the empty bleachers of Stagg Field football stadium in Chicago (`2 December 1942`) before plunging through the concrete floor into an unheated squash court filled with a 20-foot-tall black dome of graphite bricks.
  - `0:05–0:15` (Apparatus / Physical Proof): Hard cut onto physicist **George Weil's** hands pulling a single cadmium-coated wooden control rod out of the graphite pile inch by inch while **Enrico Fermi** watches the ink pen on a chart recorder climb without flattening — and three safety engineers stand on a balcony with glass jugs of cadmium sulphate ready to douse the core. Zero *"In this film..."* agenda line.
  - `0:15–0:45`: Every nuclear power station on Earth runs on the physics proved inside that squash court — yet just ten years earlier, Ernest Rutherford had called tapping atomic energy "moonshine," and building a reactor inside a major city seemed one miscalculation away from runaway meltdown.
- **Act I — Leo Szilard's Traffic-Light Idea & Enrico Fermi's Paraffin Surprise (1933–1939, UNVERIFIED):** In **September 1933**, Hungarian physicist **Leo Szilard** waited at a red traffic light on Southampton Row in London after reading Ernest Rutherford's dismissal of atomic power — and imagined a neutron-driven **chain reaction** where splitting one nucleus releases two neutrons that split two more. One year later in **October 1934** in Rome, **Enrico Fermi** made an accidental breakthrough: slipping a **block of paraffin wax** between a neutron source and a silver target boosted radioactivity **dozens of times over**, proving **slow (thermal) neutrons** are vastly better at being captured by nuclei than fast ones! After Hahn, Strassmann, Meitner & Frisch proved uranium fission in **1938–1939** (`022`), Fermi and Szilard realised graphite could act as a **moderator** to slow neutrons down — if only it were pure enough.
- **Act II — The Boron Trap & The Squash-Court Dome (1940–November 1942, UNVERIFIED):** Early graphite tests failed: commercial graphite contained tiny traces of **boron**, a voracious neutron sponge that killed the chain reaction dead. Szilard persuaded chemical suppliers to manufacture ultra-pure boron-free graphite (**AGOT graphite**). When a strike blocked construction at Argonne Woods, Fermi convinced project director Arthur Compton to build the reactor right inside Chicago — in the abandoned West Stands doubles squash court at the University of Chicago. Working 24-hour shifts covered head to toe in black graphite dust, teams led by **Walter Zinn**, **Herbert Anderson**, and 23-year-old physicist **Leona Woods** (the only woman on the CP-1 team) machined and stacked roughly **40,000 graphite bricks** (~385 tons) interwoven with **~40 tons of uranium oxide and uranium metal** into a flattened sphere **57 layers high** — with **zero shielding and zero cooling**.
- **Act III — 2 December 1942: Inch by Inch to Criticality (2 December 1942, UNVERIFIED):** At **9:45 AM** in sub-zero cold, Fermi began ordering control rods withdrawn step by step, checking his **slide rule** at every halt. When the automatic safety rod slammed shut with a loud bang at 11:30 AM (set too low), Fermi calmly broke for lunch! At **3:25 PM**, George Weil pulled the final cadmium control rod out one more foot. Fermi announced: *"This is going to do it. Now it will become self-sustaining."* The Geiger clicks fused into a continuous hum, the ink trace curved exponentially upward (`k = 1.0006`) for **28 minutes** at **0.5 watts** — barely enough to dim-glow a torch bulb, yet the first self-sustaining controlled nuclear chain reaction in history — before Fermi ordered *"Zip in!"* and Arthur Compton phoned James Conant with the coded message: *"The Italian navigator has just landed in the New World."*
- **Act IV — The Twist That Makes Nuclear Reactors Controllable (Delayed Neutrons, UNVERIFIED):** Why didn't Chicago Pile-1 run away into a thermal meltdown in milliseconds the moment `k` passed `1.0`? (A graphite-and-natural-uranium reactor cannot detonate like a nuclear weapon, but an uncontrolled prompt excursion would rapidly overheat and damage the core.) Roughly **99.35%** of fission neutrons emerge instantaneously (`prompt neutrons`, emitted in `~10⁻¹⁴ s` with a thermal graphite generation time of `~10⁻³ s` / milliseconds), which would multiply far too fast for any human hand or mechanical rod to steer — **but about `0.65%` are `delayed neutrons`**, emitted seconds later by decaying fission fragments! Keeping the reactor in the narrow window between delayed-supercritical (`k > 1`) and prompt-critical (`k < 1 + β`) stretches the reactor's doubling period from milliseconds to **tens of seconds**, giving cadmium control rods time to steer the power smoothly — the exact physical principle that still keeps every nuclear power plant stable today.

---

## 5. Two Candidate Search-Titled Shorts (`Ben 19 Nov 16–19 s Rules` + `Rules 32 & 41` — UNVERIFIED Concepts Only)

- **Short `S01`:** *How Does a Nuclear Reactor Control a Chain Reaction?* (`52 chars`, `0` exact collisions; positive curriculum search question backed by `"how does a nuclear reactor work"` and `"nuclear chain reaction"` `autocomplete = yes`)
  - **16–19 s Loop Concept (`Ben 19 Nov Rules`):**
    - **Frame 0 (`0.0 s`, premium 3D cartoon moving plate, zero Explorer, zero bars):** Close moving 3D shot of silver cadmium control rods sliding smoothly into a glowing amber graphite-and-uranium lattice as speeding neutron sparks slow and vanish. On-screen line-1 concrete fact caption: `0.65% of neutrons arrive late` (yellow on `0.65%`).
    - **Spoken hook (`≤1.5 s` titled noun + surprise, zero dateline, zero meta-promise):** *"A nuclear reactor would run away in a millisecond — except for a tiny batch of late neutrons."*
    - **Single mid-Short `Teach on screen` overlay (`~9.5 s`, inside 16:9 band):** `0.65% DELAYED NEUTRONS`.
    - **Payoff (`≥70%` runtime, `~13.5 s / 18.0 s`):** Because `0.65%` of fission neutrons are delayed by seconds, cadmium control rods have time to absorb extras and hold the chain reaction steady — looping smoothly back into *"A nuclear reactor would run away..."* (`<0.3 s` visual seam match, `0` CTA).
- **Short `S02`:** *Why Did Enrico Fermi Build a Reactor Under a Stadium?* (`53 chars`, `0` exact collisions; positive named-scientist search question backed by `"enrico fermi nuclear reactor"` and `"chicago pile 1"` `autocomplete = yes`)
  - **16–19 s Loop Concept (`Ben 19 Nov Rules`):**
    - **Frame 0 (`0.0 s`, premium 3D cartoon moving plate, zero Explorer, zero bars):** Snow blowing across empty football bleachers melting away in a 3D cutaway to reveal scientists stacking giant black graphite bricks inside an underground squash court. On-screen line-1 concrete fact caption: `40,000 bricks under a stadium` (yellow on `40,000`).
    - **Spoken hook (`≤1.5 s` titled noun + surprise, zero dateline, zero meta-promise):** *"Enrico Fermi built the world's first nuclear reactor under a Chicago football stadium with zero shielding."*
    - **Single mid-Short `Teach on screen` overlay (`~9.5 s`, inside 16:9 band):** `CHICAGO PILE-1 · 0.5 WATTS`.
    - **Payoff (`≥70%` runtime, `~13.5 s / 18.0 s`):** A labour strike stalled his suburban site, so Fermi bet his slide-rule math and one rope-tied cadmium rod that a half-watt controlled chain reaction could run safely indoors — looping back into *"Enrico Fermi built the world's first nuclear reactor..."* (`<0.3 s` visual seam match, `0` CTA).
