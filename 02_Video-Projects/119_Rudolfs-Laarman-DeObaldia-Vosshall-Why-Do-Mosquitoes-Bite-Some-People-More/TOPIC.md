# Topic Brief — `119_Rudolfs-Laarman-DeObaldia-Vosshall-Why-Do-Mosquitoes-Bite-Some-People-More` (`HOS:119` — Rule-E GO in `next_hos`)

> **RULE-E GO & RULE G STATUS (`J2970` / `J2972`, `2026-11-17`):**
> - **Rule-E GO (`96.6 / 100` · `9.66 / 10` Opportunity Score) in `next_hos`:** Pre-cleared by `J2972` in the History of Science backlog (`jobs/WIP.json` `next_hos`) under **Rule G** (`active` has 4 HOS films: `008`, `009`, `010`, `013`). Nothing is started in production (`status.json` stages are all `todo`).
> - **Strict Unverified Claims Guard (`facts` Lane Required Before Script Lock):** All historical and scientific claims in this brief are **UNVERIFIED** working notes. When an active HOS WIP slot opens, every claim, date, and number must be backed by verbatim primary-source quotes in `SOURCES.md` and verified through the `facts` lane (`gemini-agy`) before any script is locked, VO is recorded, or picture credit is spent.

---

## 1. HOS Data Comparison (`2026-11-16` Snapshot + `studio_ctr.json` + `channel_daily.json`)

- **Data sources read:**
  - `05_Analytics/hos/snapshots/2026-11-16.json` (`takenAt: 2026-11-16T06:40:22.396Z`, `37` public videos = `7` longs + `30` Shorts, `4,118` total views, `6` subscribers)
  - `05_Analytics/hos/studio_ctr.json` (`readAt: 2026-11-16T08:57:01.670060+00:00`, lifetime Studio impressions, CTR, average view %, and Shorts stayed-to-watch %)
  - `05_Analytics/hos/channel_daily.json` (`through: 2026-11-14`) and `05_Analytics/hos/REPORT.md`
  - `05_Analytics/LEARNINGS.md` (rules 1–33)
- **Elapsed-day denominator (`age_days`):** `max((date(2026, 11, 16) - date.fromisoformat(publishedAt[:10])).days, 1)` (`views/day = views / age_days`).
- **Low-sample statistical caveat (`Rule 1` / `RULING.md`):** Five public HOS longs have only `5–13` lifetime views (`15–46` impressions), and bottom-tier Shorts have `4–30` views. Patterns inferred from those small-N rows are treated explicitly as **hypotheses**, not settled laws.

### 1a. All `7` Public HOS Longs — Ranked by Views/Day Since Publish (`2026-11-16`)

| Rank | Video ID | Film | Title | Published (`age_days`) | Views (`2026-11-16`) | Views / Day | Studio Impressions (Lifetime) | Studio CTR (Lifetime) | Studio Avg View % (Lifetime) | YTA 28d Views (`through 11-14`) | YTA 28d Avg View % |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **1** | `AL_-qlWko_g` | `002` | *How Did We Discover the Periodic Table?* | `2026-09-17` (`60d`) | **161** | **2.68/d** | 1,160 | 3.36% | 21.59% (`117s / 541s`) | 16 | 19% |
| **2** | `ETynHpIYLeY` | `007` | *How Was the First Vaccine Made? (And Why It's Named After a Cow)* | `2026-11-12` (`4d`) | **5** | **1.25/d** | 27 | 7.41% | 28.49% (`152s / 532s`) | 5 | 5% |
| **3** | `VbPubYd6Fbs` | `006` | *The Willow Tree That Was Made of Air* | `2026-11-05` (`11d`) | **13** | **1.18/d** | 46 | 6.52% | **53.96%** (`287s / 532s`) | 13 | 79% |
| **4** | `GHZDsiH7L7A` | `004` | *What's Inside an Atom? Mostly Empty Space* | `2026-10-15` (`32d`) | **34** | **1.06/d** | 837 | 1.31% | 24.29% (`128s / 525s`) | 24 | 35% |
| **5** | `wwcjcFfC-5M` | `005` | *The Tied Arm That Proved Your Blood Circulates* | `2026-10-29` (`18d`) | **5** | **0.28/d** | 15 | **20.00%** | 9.24% (`49s / 529s`) | 5 | 9% |
| **6** | `_C92tIJCk8A` | `001` | *How Did We Discover Germs?* | `2026-09-03` (`74d`) | **7** | **0.09/d** | 44 | 6.82% | 48.08% (`176s / 365s`) | 0 | — |
| **7** | `frP_YrNShsU` | `003` | *How Did We Discover X-rays?* | `2026-09-24` (`53d`) | **5** | **0.09/d** | 41 | 2.44% | 26.65% (`114s / 426s`) | 3 | 14% |

- **3 Best HOS Longs & What They Share:**
  1. **`AL_-qlWko_g` (`002` *How Did We Discover the Periodic Table?*, `541s`)** — **`2.68` views/day** (`161` views in `60d`), **`1,160` impressions** (`53.5%` of all HOS long impressions), `3.36%` CTR, `21.59%` Studio avg view % (`71%` at `0:15`, `51%` at `0:30`).
  2. **`ETynHpIYLeY` (`007` *How Was the First Vaccine Made? (And Why It's Named After a Cow)*, `532s`)** / **`VbPubYd6Fbs` (`006` *The Willow Tree That Was Made of Air*, `532s`)** — **`1.25/d`** (`5` views in `4d`, `27` impressions, `7.41%` CTR, `28.49%` Studio avg view %) and **`1.18/d`** (`13` views in `11d`, `46` impressions, `6.52%` CTR, channel-best **`53.96%` Studio / `79%` 28d YTA avg view %**; low-N hypotheses at `5–13` views).
  3. **`GHZDsiH7L7A` (`004` *What's Inside an Atom? Mostly Empty Space*, `525s`)** — **`1.06` views/day** (`34` views in `32d`), **`837` impressions** (`38.6%` of all HOS long impressions), `1.31%` CTR, `24.29%` Studio avg view % (`35%` in 28d YTA; `60%` at `0:15`, `47%` at `0:30`).
  - **Shared pattern (Subject, Title Shape, Opening, Thumbnail Concept, Length):** `002` and `004` together generate **`92.0%` (`1,997 / 2,170`) of all HOS long impressions** and **`84.8%` (`195 / 230`) of all HOS long views** because their titles open with plain, high-volume curriculum/search questions (`Periodic Table`, `What's Inside an Atom?`) backed by massive `TED-Ed` neighbour pools (`LEARNINGS.md` Rules 1, 15, 26), run `8.5–9.0 min` (`525–541s`), and open with a concrete physical mystery in the first `15s` (`Rule 10`). Meanwhile `006` (`53.96%` Studio avg view %) and `007` (`7.41%` CTR) show that a concrete single-apparatus twist holds viewers once clicked.
- **3 Worst HOS Longs & What They Share (Hypotheses on Small N):**
  1. **`frP_YrNShsU` (`003` *How Did We Discover X-rays?*, `426s`)** — **`0.09` views/day** (`5` views in `53d`), `41` impressions, `2.44%` CTR, `26.65%` Studio avg view %.
  2. **`_C92tIJCk8A` (`001` *How Did We Discover Germs?*, `365s`)** — **`0.09` views/day** (`7` views in `74d`), `44` impressions, `6.82%` CTR, `48.08%` Studio avg view %.
  3. **`wwcjcFfC-5M` (`005` *The Tied Arm That Proved Your Blood Circulates*, `529s`)** — **`0.28` views/day** (`5` views in `18d`), **`15` impressions**, `20.00%` CTR, **`9.24%` Studio avg view % (`49s / 529s`)**.
  - **Shared pattern:** `005` (`The Tied Arm...`, `15` impressions) used a literary statement title with no search phrase (`Rule 26` violation), starving it of impressions, while `001` (`365s`) and `003` (`426s`) used broad textbook survey titles (`How Did We Discover...`) and shorter `6–7 min` runtimes rather than a specific search question + physical experiment twist (`Rules 10, 15, 23, 26`).

### 1b. All `30` Public HOS Shorts — Ranked by Views/Day Since Publish (`2026-11-16`)

| Rank | Video ID | Title | Published (`age_days`) | Views (`2026-11-16`) | Views / Day | Studio Stayed % (Lifetime) | Studio Avg View % (Lifetime) | Likes |
|---:|---|---|---:|---:|---:|---:|---:|---:|
| **1** | `Wvjd8g0CpzE` | *The Blood Vessels Finer Than a Hair* | `2026-11-15` (`1d`) | **212** | **212.00/d** | 14.80% | 76.58% (`20s / 26s`) | 3 |
| **2** | `29bpGAI0wb8` | *What happens if you keep cutting gold in half?* | `2026-10-16` (`31d`) | **1,227** | **39.58/d** | 40.78% | 44.12% (`11s / 25s`) | 12 |
| **3** | `PFj6172YU4Q` | *One Tight Band Proved Your Blood Goes Round* | `2026-11-08` (`8d`) | **219** | **27.38/d** | 15.98% | 62.95% (`17s / 27s`) | 3 |
| **4** | `AMSriTQ-lcQ` | *Are Marie Curie's Notebooks Still Radioactive?* | `2026-10-28` (`19d`) | **274** | **14.42/d** | 22.66% | 76.94% (`17s / 22s`) | 6 |
| **5** | `OnJ8MFu0Mi0` | *How Did John Snow Stop Cholera?* | `2026-10-26` (`21d`) | **231** | **11.00/d** | 29.60% | 65.66% (`15s / 23s`) | 8 |
| **6** | `pWySvZsneZg` | *Why Gold Foil Bounced Rutherford's Particles Back* | `2026-11-01` (`15d`) | **137** | **9.13/d** | 37.23% | 112.43% (`28s / 25s`) | 2 |
| **7** | `oKqmnJNGiHg` | *How Was Phosphorus Discovered?* | `2026-10-21` (`26d`) | **188** | **7.23/d** | 41.18% | 87.02% (`20s / 23s`) | 7 |
| **8** | `-3L6HzJ_d_4` | *What Is the Pasteur Swan Neck Flask Experiment?* | `2026-10-27` (`20d`) | **129** | **6.45/d** | **77.14%** | 75.23% (`14s / 19s`) | 1 |
| **9** | `clV6E10NLPw` | *The spray that stopped surgery killing patients* | `2026-10-20` (`27d`) | **153** | **5.67/d** | 23.08% | 56.16% (`14s / 25s`) | 4 |
| **10** | `cLKDiYP55J8` | *What Was the Edward Jenner Experiment?* | `2026-11-13` (`3d`) | **17** | **5.67/d** | 29.41% | 87.58% (`20s / 23s`) | 0 |
| **11** | `BW_CFAX-mxc` | *Is the Heart a Pump?* | `2026-10-31` (`16d`) | **89** | **5.56/d** | 32.91% | 81.69% (`18s / 22s`) | 1 |
| **12** | `qOZgess30h0` | *Invisible life is still everywhere* | `2026-10-13` (`34d`) | **169** | **4.97/d** | 25.15% | 39.82% (`10s / 24s`) | 5 |
| **13** | `c2q7w0pgcn8` | *Who Discovered Infrared Light?* | `2026-10-19` (`28d`) | **138** | **4.93/d** | 43.52% | 105.30% (`24s / 23s`) | 1 |
| **14** | `Rl2uZ-KOTl8` | *Your Heart Pumps More Blood Than You Have* | `2026-10-30` (`17d`) | **78** | **4.59/d** | 26.58% | 53.64% (`13s / 25s`) | 4 |
| **15** | `xHnIi9GqOsM` | *Why Do Veins Have Valves?* | `2026-11-05` (`11d`) | **41** | **3.73/d** | 20.59% | 61.55% (`14s / 23s`) | 0 |
| **16** | `qW2OsD4mujc` | *The Four Elements Were Wrong* | `2026-11-03` (`13d`) | **35** | **2.69/d** | 57.69% | 192.62% (`46s / 24s`) | 0 |
| **17** | `TbMMJSRKC3U` | *He said every eighth element repeats* | `2026-10-18` (`29d`) | **62** | **2.14/d** | 25.49% | 123.27% (`33s / 27s`) | 1 |
| **18** | `LCZRHUyTiq0` | *What Are Cathode Rays?* | `2026-10-23` (`24d`) | **49** | **2.04/d** | 29.79% | 50.04% (`13s / 26s`) | 2 |
| **19** | `iqToagXnjX0` | *Microbes in a drop of pond water* | `2026-09-06` (`71d`) | **112** | **1.58/d** | 28.28% | 77.86% (`19s / 25s`) | 1 |
| **20** | `H1y0DXFVmw8` | *Germs don't cast a shadow* | `2026-09-06` (`71d`) | **80** | **1.13/d** | 19.75% | 59.46% (`15s / 25s`) | 1 |
| **21** | `xvanpsLeADE` | *How did Röntgen see bones without cutting* | `2026-09-26` (`51d`) | **40** | **0.78/d** | 23.33% | 50.33% (`13s / 25s`) | 0 |
| **22** | `oowAOWTBoq0` | *How X-rays Were Discovered by Accident* | `2026-09-25` (`52d`) | **32** | **0.62/d** | 47.62% | 331.08% (`83s / 25s`) | 1 |
| **23** | `nba0-f7PPeU` | *Why tellurium sat before iodine* | `2026-09-21` (`56d`) | **34** | **0.61/d** | 60.71% | 42.70% (`11s / 25s`) | 1 |
| **24** | `nFQRWmpulTQ` | *He predicted a metal before it was found* | `2026-09-19` (`58d`) | **34** | **0.59/d** | 66.67% | 55.91% (`14s / 25s`) | 0 |
| **25** | `uU12JA5rMWg` | *The periodic table's empty chairs* | `2026-09-18` (`59d`) | **30** | **0.51/d** | 66.67% | 58.79% (`15s / 25s`) | 0 |
| **26** | `8_Edn_HCi1s` | *Germs hitch a ride on you* | `2026-09-06` (`71d`) | **30** | **0.42/d** | 22.22% | 38.78% (`10s / 25s`) | 0 |
| **27** | `sILtQxgYQk8` | *A flask that proved germs come from outside* | `2026-09-06` (`71d`) | **24** | **0.34/d** | 41.67% | 36.70% (`9s / 25s`) | 0 |
| **28** | `CnHwX1L9XHg` | *Gallium sat where the table said* | `2026-09-20` (`57d`) | **16** | **0.28/d** | 30.43% | 33.45% (`9s / 26s`) | 0 |
| **29** | `zI_eD3vFWmE` | *The first X-ray showed a wedding ring* | `2026-09-27` (`50d`) | **9** | **0.18/d** | 50.00% | 64.00% (`16s / 25s`) | 0 |
| **30** | `LanTHJckYx8` | *What other table has empty chairs?* | `2026-09-22` (`55d`) | **4** | **0.07/d** | 33.33% | 23.08% (`6s / 26s`) | 0 |

- **3 Best HOS Shorts & What They Share:**
  1. **`29bpGAI0wb8` (*What happens if you keep cutting gold in half?*, `25s`)** — **`39.58` views/day** (`1,227` views in `31d`, #1 mature HOS Short), `40.78%` stayed-to-watch, `44.12%` avg view % (`11s / 25s`), `12` likes.
  2. **`-3L6HzJ_d_4` (*What Is the Pasteur Swan Neck Flask Experiment?*, `19s`)** — **`6.45` views/day** (`129` views in `20d`), channel-best **`77.14%` stayed-to-watch (PASS `≥60%`)** and **`75.23%` avg view % (PASS `≥70%`)**, with **`92.2%` (`119 / 129`) of 28d views coming from YouTube search** — the first mature `100+` view HOS Short to pass both targets (`LEARNINGS.md` Rules 28 & 32).
  3. **`oKqmnJNGiHg` (*How Was Phosphorus Discovered?*, `23s`)** — **`7.23` views/day** (`188` views in `26d`), **`41.18%` stayed-to-watch** and **`87.02%` avg view % (PASS `≥70%`)**, `7` likes — alongside loop winners `pWySvZsneZg` (*Why Gold Foil Bounced Rutherford's Particles Back*, `9.13/d`, `137` views, `37.23%` stayed, **`112.43%` avg view % LOOP**) and `c2q7w0pgcn8` (*Who Discovered Infrared Light?*, `4.93/d`, `138` views, `43.52%` stayed, **`105.30%` avg view % LOOP**), while day-1 feed cohort `Wvjd8g0CpzE` (`212.00/d` at `21h`, **`76.58%` avg view % PASS**, **`14.80%` stayed MISS**) and `PFj6172YU4Q` (`27.38/d`, `219` views, `62.95%` avg view %, **`15.98%` stayed MISS**) confirm that `≤1.0s` loop tails fix avg view % (`76.6%` PASS) while statement titles (`The Blood Vessels Finer Than a Hair`, `One Tight Band...`) fail cold-feed stayed-to-watch (`14.8–16.0%`).
  - **Shared pattern:** Positive search-question titles (`What happens if...`, `What Is...`, `How Was...`, `Why...`, `Who Discovered...`) outperform statement titles on stayed-to-watch (`40.8–77.1%` vs `14.8–16.0%`; `LEARNINGS.md` Rule 32), while `≤1.0s` loop tails with zero CTA and payoff withheld until `≥70%` runtime lift avg view % to `75–112%+` (`Rules 3, 6, 24, 27`).
- **3 Worst HOS Shorts & What They Share (Hypotheses on Small N):**
  1. **`LanTHJckYx8` (*What other table has empty chairs?*, `26s`)** — **`0.07` views/day** (`4` views in `55d`), `33.33%` stayed-to-watch, `23.08%` avg view % (`6s / 26s`).
  2. **`zI_eD3vFWmE` (*The first X-ray showed a wedding ring*, `25s`)** — **`0.18` views/day** (`9` views in `50d`), `50.00%` stayed-to-watch, `64.00%` avg view %.
  3. **`CnHwX1L9XHg` (*Gallium sat where the table said*, `26s`)** — **`0.28` views/day** (`16` views in `57d`), `30.43%` stayed-to-watch, `33.45%` avg view %.
  - **Shared pattern:** Cryptic riddles (*What other table has empty chairs?*) and flat past-tense statements (*Gallium sat where the table said*, *The first X-ray showed a wedding ring*) omit the searchable subject noun and fail both Shorts-feed stayed-to-watch and YouTube search discovery (`LEARNINGS.md` Rules 1, 28, 32).

---

## 2. Overlap & Non-Duplication Check (`2026-11-17`)

Checked against:
- All folders in `02_Video-Projects/` (`000`–`018`, `099`–`101` on `main`),
- Open topic PRs `#572` (`102` Ozone Hole, `103` Why Is the Sky Blue), `#581` (`104` Speed of Light, `105` Venus Flytrap), `#588` (`106` Eels & Sargasso Sea, `107` Autumn Leaves & Chlorophyll), `#602` (`108` Why Is Ice Slippery, `109` Why Do Fingers Wrinkle in Water), `#607` (`110` Why Do Onions Make You Cry, `111` Why Do Knuckles Crack), `#614` (`112` Why Do We Yawn, `113` How Do Cats Land on Their Feet), `#618` (`114` How Do Chameleons Change Colour, `115` Why Do Zebras Have Stripes), and `#625` (`116` Why Do We Get Goosebumps, `117` Why Don't Woodpeckers Get Concussions), plus `118` (`Why Do We Hiccup?`),
- All `011`–`097` backlog entries in `00_Brand/Channel-Setup/VIDEO_BACKLOG.json` and `00_Brand/Channel-Setup/ideas/` (`048` covers Pelletier & Caventou's 1820 quinine, Perkin's 1856 Mauveine dye, Ronald Ross's 1897 *Plasmodium* malaria parasite, and Tu Youyou's 1971 artemisinin; `056` covers Buck & Axel's mammalian olfactory GPCR gene family; **none** cover why mosquitoes bite some people more than others, Willem Rudolfs's 1922 $\text{CO}_2$/sweat tests, Jakob Laarman's 1955 two-stream wind-tunnel olfactometer, Matthew DeGennaro & Leslie Vosshall's 2013 `Orco` mutant mosquito experiment, or Maria Elena De Obaldia & Leslie Vosshall's October 2022 Rockefeller University nylon-stocking carboxylic-acid & co-receptor discovery).
- **Result:** **Zero overlap.**

---

## 3. Packaging, Why It Should Work & Search/Neighbour Evidence (`Rule 26` + `neighbours.py` + `public_search.py`)

- **Title A (Primary Proposal, `LEARNINGS.md` Rules 1, 15, 23, 26 — `60 chars`, `0` exact collisions):** `Why Do Mosquitoes Bite Some People More? (The Stocking Test)`
- **Title A1 (Compact `Rule 15 ≤50 chars` Variant — `49 chars`, `0` exact collisions):** `Why Do Mosquitoes Bite Some People More? (Solved)`
- **Title B (Test & Compare Arm 2, `Rule 23` — `50 chars`, `≤50 chars`, `0` exact collisions):** `Mosquito Magnets Are Real (The 2022 Stocking Test)`
- **Title C (`Rule 26` Exact Phrase First — `65 chars`, `0` exact collisions):** `Why Do Mosquitoes Bite Some People More? The Skin-Acid Experiment`
- **One-Line Hook:** Everyone knows one "mosquito magnet" who gets eaten alive while friends sitting right next to them are untouched — and in October 2022, a 3-year Rockefeller University tournament using 64 volunteers' worn nylon stockings finally proved what makes certain human skin 100 times more irresistible to mosquitoes.
- **Why It Should Work (Past Winners & `LEARNINGS.md` Rules):**
  - Resembles top HOS longs **`002` Periodic Table (`AL_-qlWko_g`, `161` views, `2.68/d`, `1,160` impressions, `3.36%` CTR)** and **`004` Inside an Atom (`GHZDsiH7L7A`, `34` views, `1.06/d`, `837` impressions)** by opening with an exact, massive-demand search question (`Why Do Mosquitoes Bite Some People More?`, where `Veritasium` has `10.41M` views and `TED-Ed` has `2.20M` views) backed by `5` education neighbours `≥1M` views (`Rules 1, 15, 26`), while pairing that search demand with a concrete, unforgettable laboratory apparatus (pitting strips of worn nylon stockings against each other in a two-trap wind tunnel) like **`006` Willow Tree (`VbPubYd6Fbs`, `53.96%` Studio / `79%` 28d YTA avg view %)** and **`007` First Vaccine (`ETynHpIYLeY`, `7.41%` CTR)**.
  - Resembles top HOS Shorts **`29bpGAI0wb8` (*What happens if you keep cutting gold in half?*, `1,227` views, `39.58/d`)**, **`-3L6HzJ_d_4` (*What Is the Pasteur Swan Neck Flask Experiment?*, `129` views, `77.14%` stayed PASS, `75.23%` avg view % PASS)**, and **`oKqmnJNGiHg` (*How Was Phosphorus Discovered?*, `188` views, `87.02%` avg view % PASS)** by turning an everyday human question into a visual head-to-head experiment (`Rules 2, 6, 8, 24, 27, 28, 30, 32`).
- **3-Way Thumbnail Test & Compare Plan (`LEARNINGS.md` Rules 11, 12, 14 + `THUMBNAIL_AND_TITLE_RULES.md` §2.1–2.B):**
  - **Thumb A (Hero Object — The Two-Trap Nylon Stocking Arena):** Painted 3D house-style key art: inside a glass wind-tunnel chamber on the right two-thirds, a swarm of mosquitoes ignores Nylon Stocking A to crowd onto Nylon Stocking B (`Subject 33`) glowing with golden skin-acid plumes; the Explorer small at lower left; cream/gold serif text on the clear left band: `100X MORE BITES` (`3 words`, gold on `100X`, zero overlap on the hero).
  - **Thumb B (`Rule 14` Bright High-Contrast Variant — Two Arms in Sunlight):** Bright sunlit summer garden/lab split key art: two human forearms side by side — one completely untouched, the other surrounded by landing mosquitoes homing in on a glowing golden skin-chemistry aura; Explorer small at lower left; serif text on the left band: `MOSQUITO MAGNET` (`2 words`, gold on `MAGNET`).
  - **Thumb C (The Unstoppable Backup Antenna):** Painted 3D close-up of a female *Aedes aegypti* mosquito's feathery antenna lighting up with two different colour-coded receptor pathways (gold and teal) simultaneously tracking a trail of skin carboxylic acids; Explorer small at lower left; serif text on the left band: `BACKUP SMELL` (`2 words`, gold on `BACKUP`).
- **Signed-out YouTube Autocomplete (`2026-11-17`, `11` queries / `80` search rows in `evidence_2026-11-17_public_search.json`):**
  - `"why do mosquitoes bite some people more"` → **`autocomplete = yes`** (`why do mosquitoes bite some people more`, `why do mosquitoes bite some people more than others`, `why mosquitoes bite some people more than others - maria elena de obaldia`, `why mosquitoes bite some people more`)
  - `"why do mosquitoes bite some people more than others"` → **`autocomplete = yes`** (`why do mosquitoes bite some people more than others`, `why mosquitoes bite some people more than others - maria elena de obaldia`, `why do some people get more mosquito bites than others`)
  - `"why are some people mosquito magnets"` → **`autocomplete = yes`** (`why are some people mosquito magnets`)
  - `"how do mosquitoes find you"` → **`autocomplete = yes`** (`how do mosquitoes find you`)
  - `"What Makes Some People Mosquito Magnets?"` → **`related: why are some people mosquito magnets`**
  - `"mosquito"` (`neighbours.json`) → **`autocomplete = yes`**
- **Rule 26(a) Two Ranking Videos (`≥10,000` views, retrieved `2026-11-17`):**
  1. `Veritasium` — [`38gVZgE39K8`](https://youtu.be/38gVZgE39K8) *Why Mosquitoes Bite Some People More Than Others* (**`10,410,329–10,410,342` views**)
  2. `TED-Ed` — [`V6rRifwIaio`](https://youtu.be/V6rRifwIaio) *Why mosquitoes bite some people more than others - Maria Elena De Obaldia* (**`2,203,899–2,203,923` views**; plus `MinuteEarth` [`bvKKHRCCkfI`](https://youtu.be/bvKKHRCCkfI) **`3,091,491–3,091,500` views**, `Anton Petrov` [`fREwyj53FPg`](https://youtu.be/fREwyj53FPg) **`3,050,554` views**, `Business Insider` [`AqIllCxn4YE`](https://youtu.be/AqIllCxn4YE) **`1,560,180–1,560,189` views**, `Peekaboo Kidz` [`ieVANEUe198`](https://youtu.be/ieVANEUe198) **`1,517,057–1,517,079` views**, `The Infographics Show` [`KFJ7SqQULeI`](https://youtu.be/KFJ7SqQULeI) **`1,116,265` views**, and `AXIOM` [`8H-lwLVlNtc`](https://youtu.be/8H-lwLVlNtc) **`715,961` views**)
- **Neighbour Gate (`neighbours.py`):** **PASS (`5` strictly on-topic education videos `≥1,000,000` views, `TED-Ed/TED: yes`, `0` off-topic rows across all `18` education neighbours)** — saved in [`11_Upload-Package/evidence_2026-11-17_neighbours.json`](11_Upload-Package/evidence_2026-11-17_neighbours.json):
  1. `TED-Ed` ★ — [`IkmjCmvfeFI`](https://youtu.be/IkmjCmvfeFI) *The loathsome, lethal mosquito - Rose Eveleth* (**`12,513,522` views**)
  2. `Veritasium` — [`38gVZgE39K8`](https://youtu.be/38gVZgE39K8) *Why Mosquitoes Bite Some People More Than Others* (**`10,410,341` views**)
  3. `MinuteEarth` — [`bvKKHRCCkfI`](https://youtu.be/bvKKHRCCkfI) *Why Are Some People Mosquito Magnets?* (**`3,091,491` views**)
  4. `TED-Ed` ★ — [`V6rRifwIaio`](https://youtu.be/V6rRifwIaio) *Why mosquitoes bite some people more than others - Maria Elena De Obaldia* (**`2,203,920` views**)
  5. `TED-Ed` ★ — [`H7i9Anh0_Dg`](https://youtu.be/H7i9Anh0_Dg) *Ethical dilemma: Should we get rid of mosquitoes? - Talya Hackett* (**`1,317,427` views**; plus `TED` [`tsgvhP07BC8`](https://youtu.be/tsgvhP07BC8) **`689,694` views**, `TED-Ed` [`ZLkbWUNQbgk`](https://youtu.be/ZLkbWUNQbgk) **`298,099` views**, `TED` [`Rcm3rPz_Q94`](https://youtu.be/Rcm3rPz_Q94) *The real reason why mosquitoes buzz* **`237,081` views**, `TED` [`cpsRAk5HpK4`](https://youtu.be/cpsRAk5HpK4) **`96,968` views**, and `TED` [`ZJPdJuhI03U`](https://youtu.be/ZJPdJuhI03U) **`74,856` views**)

---

## 4. Candidate 4-Act Discovery Outline (All Claims UNVERIFIED Pending `SOURCES.md` & `facts` Lane)

- **Cold Open (0:00–0:45, Proof-First `0:05–0:15` Apparatus Window per `Rules 10 & 30`, UNVERIFIED):**
  - `0:00–0:05`: Two human forearms rest side by side on a warm summer evening as a swarm of female *Aedes aegypti* mosquitoes completely ignores the left arm and crowds onto the right arm.
  - `0:05–0:15` (Apparatus / Physical Proof): Hard cut directly into Rockefeller University's **two-trap acrylic wind-tunnel olfactometer**, where two **5 cm ribbons of worn nylon stocking** (`Subject 19` on the left trap, `Subject 33` on the right trap) release invisible skin-odour plumes — and almost every single mosquito flies straight into `Subject 33`'s trap (`100× MORE BITES` ink scale counter). Zero *"In this film..."* agenda line.
  - `0:15–0:45`: For a century, folk wisdom blamed blood type, sweet blood, garlic, or beer — until a 3-year tournament using 64 volunteers' worn nylon stockings uncovered the invisible skin acids that make someone a lifelong "mosquito magnet."
- **Act I — Willem Rudolfs's 1922 Breath Test & Jakob Laarman's 1955 Wind-Tunnel Olfactometer (1922–1968, UNVERIFIED):** In **June 1922**, biochemist **Willem Rudolfs** at Rutgers University (*New Jersey Agricultural Experiment Stations Bulletin* `367: 1–23`, *"Chemotropism of Mosquitoes"*) tested isolated human sweat, sebaceous secretions, blood, and breath on *Aedes* mosquitoes inside glass assay tubes, proving that exhaled **carbon dioxide ($\text{CO}_2$)** and warmth wake mosquitoes up and tell them a warm-blooded host is nearby. In **1955**, Dutch biologist **Jakob Jan Laarman** at the University of Leiden (*Acta Leidensia* `25: 1–144`; **1958** *Trop. Geogr. Med.* `10: 293–305`) built a precision **two-stream wind-tunnel olfactometer** proving that even when temperature, humidity, and $\text{CO}_2$ are equalised, an activated mosquito steers specifically toward invisible chemical vapours rising from human skin — with **Fred Acree Jr., R. B. Turner, H. K. Gouck, Morton Beroza & N. Smith** (**1968**, *Science* `161(3848): 1346–1347`) isolating **L-lactic acid** from human arms as the first synergistic human skin attractant.
- **Act II — Matthew DeGennaro & Leslie Vosshall's 2013 Mutant Mosquito Shock (2013–2019, UNVERIFIED):** How do you stop a mosquito from smelling human skin? In **May 2013** (*Nature* `498(7455): 487–491`, **Matthew DeGennaro, Carolyn S. McBride et al. & Leslie B. Vosshall**), Rockefeller University researchers used zinc-finger nucleases to mutate **`Orco`**, the master co-receptor gene required for all standard insect odorant receptors. Without `Orco`, mosquitoes lost their preference for humans over guinea pigs in plain air — yet the moment the scientists added a puff of $\text{CO}_2$, the `Orco`-mutant mosquitoes still locked onto human skin via a backup ionotropic acid-sensing pathway (**`Ir8a`**, confirmed by **Joshua I. Raji & Matthew DeGennaro**, **2019**, *Current Biology* `29(8): 1253–1262.e7`, alongside **`Ir25a`** and **`Ir76b`**)!
- **Act III — Maria Elena De Obaldia's October 2022 Nylon-Stocking Tournament (2022, UNVERIFIED):** To discover what chemical makes one human far more attractive than another without exposing volunteers to hundreds of bites, postdoc **Maria Elena De Obaldia, Takeshi Morita, Laura C. Dedmon, Daniel J. Boehmler, Caroline S. Jiang, Emely V. Zeledon, Justin R. Cross & Leslie B. Vosshall** (**18 October 2022**, *Cell* `185(22): 4099–4116.e13`) had **64 volunteers** wear **nylon stockings** over their forearms for **6 hours** at a time to trap their natural skin odour (`sebum`). They cut the stockings into **5 cm (2-inch) ribbons** and ran a **3-year longitudinal round-robin tournament** inside a two-choice olfactometer chamber. **"Subject 33"** was **more than 100 times more attractive** than the two least-attractive volunteers (**`Subject 19`** and **`Subject 28`**) (`4×` more attractive than the next highest volunteer) and won every single match across all three years!
- **Act IV — Carboxylic Acids & Margaret Herre's Rule-Breaking Fail-Safe Neuron (August–October 2022, UNVERIFIED):** Two-dimensional gas chromatography–mass spectrometry (`GC×GC-MS`) revealed `50` enriched molecular features on high-attractor skin: "mosquito magnets" like Subject 33 produce dramatically higher levels of long-chain saturated **carboxylic acids** (`C10–C20`, led by **pentadecanoic acid (`C15:0`)**, **heptadecanoic acid (`C17:0`)**, and **nonadecanoic acid (`C19:0`)**) in their skin's moisturizing **sebum** layer, which skin microbiota convert into an inescapable scent plume. And in a companion Rockefeller study (**Margaret Herre, Olivia V. Goldman et al. & Leslie B. Vosshall**, **18 August 2022**, *Cell* `185(17): 3104–3123.e28`, *"Non-canonical odor coding in the mosquito"*), single-nucleus RNA sequencing and electrophysiology revealed why gene knockouts couldn't blind mosquitoes: female *Aedes aegypti* violate the textbook "one-receptor-per-neuron" law by co-expressing both `Orco` odorant receptors and `Ir` ionotropic acid receptors inside the **very same olfactory sensory neuron**, creating a fail-safe human detector!

---

## 5. Two Candidate Search-Titled Shorts (`Test B` / `Rule 26` / `Rule 32` — UNVERIFIED Concepts Only)

- **Short `S01`:** *What Makes Some People Mosquito Magnets?* (`40 chars`, `0` exact collisions, positive search question; backed by `"why are some people mosquito magnets"` `autocomplete = yes`)
  - **First-line answer hook (`≤1.5 s` titled noun + claim, UNVERIFIED):** *"Mosquito magnets are real: in a 3-year nylon stocking tournament, one volunteer attracted 100 times more mosquitoes than the least-bitten person."*
  - **Frame-0, `Teach on screen` Overlay & Payoff Plan (`Rules 2, 3, 6, 24, 27` + `studio/RULES.md`):** Frame 0 (`0.0s`, `mode: "cover"`, `0%` Explorer, `0%` bars): close moving 3D view of mosquitoes swarming one nylon stocking ribbon while ignoring the ribbon beside it (`100X MORE BITES`, `#FFE000` on `100X`). Single mid-Short word-for-word `Teach on screen` overlay at `~11.0s` (inside `16:9` centre band, clear of `0–2s` and `9–14s` title): `100 TIMES MORE ATTRACTIVE`. Payoff at `≥70%` runtime (`~17.0s / 23.5s`): Maria Elena De Obaldia & Leslie Vosshall's October 2022 Rockefeller University discovery that lifelong "mosquito magnets" produce high levels of three carboxylic acids (`pentadecanoic`, `heptadecanoic`, `nonadecanoic`) in their skin sebum. Loop tail `<1.0s`, zero CTA.
- **Short `S02`:** *How Do Mosquitoes Still Find You Without Smell Receptors?* (`57 chars`, `0` exact collisions, positive search question; backed by `"how do mosquitoes find you"` `autocomplete = yes`)
  - **First-line answer hook (`≤1.5 s` titled noun + claim, UNVERIFIED):** *"Delete a mosquito's master smell gene, and a single breath of carbon dioxide still guides her straight to your skin."*
  - **Frame-0, `Teach on screen` Overlay & Payoff Plan (`Rules 2, 3, 6, 24, 27` + `studio/RULES.md`):** Frame 0 (`0.0s`, `mode: "cover"`, `0%` Explorer, `0%` bars): extreme close moving 3D view of a mosquito antenna lighting up with dual gold and teal receptor signals as it tracks a skin-acid plume (`BACKUP SMELL`, `#FFE000` on `BACKUP`). Single mid-Short word-for-word `Teach on screen` overlay at `~11.5s` (inside `16:9` centre band, clear of `0–2s` and `9–14s` title): `TWO RECEPTORS ONE NEURON`. Payoff at `≥70%` runtime (`~17.2s / 23.5s`): Margaret Herre & Leslie Vosshall's August 2022 *Cell* discovery that mosquitoes break the textbook one-receptor-per-neuron rule by wiring both odorant (`Orco`) and acid (`Ir`) receptors into the same olfactory neuron as a fail-safe human detector. Loop tail `<1.0s`, zero CTA.
