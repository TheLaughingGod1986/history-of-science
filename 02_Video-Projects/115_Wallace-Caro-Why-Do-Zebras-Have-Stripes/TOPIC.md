# Topic Brief — `115_Wallace-Caro-Why-Do-Zebras-Have-Stripes` (`HOS:115` Proposal)

> **PROPOSAL & RULE G STATUS (`J2944`, `2026-11-16`):**
> - **Backlog Proposal Only (`next_hos`):** This topic is added to the History of Science backlog (`jobs/WIP.json` `next_hos`) under **Rule G** (`active` has 4 HOS films: `008`, `009`, `010`, `013`). Nothing is started in production (`status.json` stages are all `todo`).
> - **Awaits Rule-E Review & `facts` Lane:** All historical and scientific claims in this brief are **UNVERIFIED** working notes. Before any script is locked or VO is recorded, every claim must be backed by verbatim primary-source quotes in `SOURCES.md` and verified through the `facts` lane (`gemini-agy`).

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

## 2. Overlap & Non-Duplication Check (`2026-11-16`)

Checked against:
- All folders in `02_Video-Projects/` (`000`–`018`, `099`–`101` on `main`, plus `114` Chameleons in this PR),
- Open topic PRs `#572` (`102` Ozone Hole, `103` Why Is the Sky Blue), `#581` (`104` Speed of Light, `105` Venus Flytrap), `#588` (`106` Eels & Sargasso Sea, `107` Autumn Leaves & Chlorophyll), `#602` (`108` Why Is Ice Slippery, `109` Why Do Fingers Wrinkle in Water), `#607` (`110` Why Do Onions Make You Cry, `111` Why Do Knuckles Crack), and `#614` (`112` Why Do We Yawn, `113` How Do Cats Land on Their Feet),
- All `011`–`095` backlog entries in `00_Brand/Channel-Setup/VIDEO_BACKLOG.json` and `00_Brand/Channel-Setup/ideas/` (`013` covers Darwin & Wallace's 1858 Ternate letter on natural selection; `048` covers Perkin, Ross & Tu Youyou on quinine, mosquito malaria transmission, and artemisinin; **none** cover why zebras have black-and-white stripes, the 1871–1889 Darwin–Wallace debate over zebra stripes, Gábor Horváth's 2012 polarised-light horsefly trap experiments, or Tim Caro & Martin How's 2014–2019 Somerset experiment dressing domestic horses in zebra-striped coats).
- **Result:** **Zero overlap.**

---

## 3. Packaging, Why It Should Work & Search/Neighbour Evidence (`Rule 26` + `neighbours.py` + `public_search.py`)

- **Title A (Primary Proposal, `LEARNINGS.md` Rules 1, 15, 23, 26 — `58 chars`, `0` exact collisions):** `Why Do Zebras Have Stripes? (The Horsefly Coat Experiment)`
- **Title B (Test & Compare Arm 2, `Rule 23` — `57 chars`, `0` exact collisions):** `The Striped Horse Coat That Solved Darwin's Zebra Mystery`
- **Title C (`Rule 26` Exact Phrase First — `54 chars`, `0` exact collisions):** `Why Do Zebras Have Stripes? How a Horse Coat Solved It`
- **One-Line Hook:** For 150 years scientists argued whether zebra stripes hide them from lions or cool their skin — until biologists dressed English horses in striped zebra coats and filmed blood-sucking horseflies failing to brake and bouncing straight off them.
- **Why It Should Work (Past Winners & `LEARNINGS.md` Rules):**
  - Directly fixes the `15`-impression starvation of statement-titled **`005` Tied Arm (`wwcjcFfC-5M`)** by leading with the exact signed-out YouTube autocomplete question `"why do zebras have stripes"` (`Rule 26`), where `TED-Ed` (`QJB0nmEjbDY`, `665,336` views) and `SciShow` (`540,283` and `346,443` views) already rank in the GB top 5 and `neighbours.py` passes with `12` education videos `≥1M` views (`TED-Ed/TED: yes`), matching the discovery graph of **`002` Periodic Table (`AL_-qlWko_g`, `161` views, `2.68/d`, `1,160` impressions, `3.36%` CTR)** and **`004` Inside an Atom (`GHZDsiH7L7A`, `34` views, `1.06/d`, `837` impressions)**.
  - Pairs that universal childhood question with an unforgettable visual apparatus test (horses wearing black-and-white zebra coats while high-speed cameras track horseflies crashing into them), giving both the Long opening (`Rule 10` & `Rule 30`) and the two Shorts (`Rules 2, 8, 24, 27, 28, 32`) the same immediate visual hook that powered **`29bpGAI0wb8` (`1,227` views, `39.58/d`)** and **`-3L6HzJ_d_4` (`77.14%` stayed PASS, `75.23%` avg view % PASS)**.
- **3-Way Thumbnail Test & Compare Plan (`LEARNINGS.md` Rules 11, 12, 14 + `THUMBNAIL_AND_TITLE_RULES.md` §2.1–2.B):**
  - **Thumb A (Hero Object — The Horse in a Zebra Coat):** Painted 3D house-style key art: a brown domestic horse on the right two-thirds wearing a tailored black-and-white striped zebra coat while a glowing red trajectory line shows a giant horsefly bouncing off the stripes; the Explorer small at lower left holding a stopwatch and notebook; cream/gold serif text on the clear left band: `FLIES CAN'T LAND` (`3 words`, gold on `CAN'T`, zero overlap on the horse).
  - **Thumb B (`Rule 14` Bright High-Contrast Variant — Lion Myth Bust):** Bright sunlit African savannah key art: a zebra standing in full daylight while a red cross strikes out a prowling lion silhouette and a magnifying lens zooms in on a biting horsefly; Explorer small at lower left; serif text on the left band: `NOT FOR LIONS` (`3 words`, gold on `NOT`).
  - **Thumb C (The Sticky Striped Trap Experiment):** Painted 3D key art of three glossy test panels side by side — all black (covered in flies), all white, and narrow black-and-white stripes (zero flies); Explorer small at lower left; serif text on the left band: `BLINDS FLIES` (`2 words`, gold on `BLINDS`).
- **Signed-out YouTube Autocomplete (`2026-11-16`):**
  - `"why do zebras have stripes"` → **`autocomplete = yes`** (`why do zebras have stripes`, `why do zebras have stripes mystery doug`, `why does zebra have stripes`, `why do zebras have black and white stripes`)
- **Rule 26(a) Two Ranking Videos (`≥10,000` views, retrieved `2026-11-16`):**
  1. `TED-Ed` — [`QJB0nmEjbDY`](https://youtu.be/QJB0nmEjbDY) *The surprising reason zebras have stripes - Cella Wright* (**`665,336` views**)
  2. `SciShow` — [`LbVSYO-Y-kU`](https://youtu.be/LbVSYO-Y-kU) *We Were Totally Wrong About Zebra Stripes* (**`540,283` views**; plus `SciShow Kids` [`GhfBOyPQqX0`](https://youtu.be/GhfBOyPQqX0) **`431,527` views**, `Mystery Science` [`q57fauR3Syk`](https://youtu.be/q57fauR3Syk) **`390,742` views**, `SciShow` [`vWKDMKO-hQM`](https://youtu.be/vWKDMKO-hQM) **`346,443` views**, and `Colossal Cranium` [`J5EtNvHtl8A`](https://youtu.be/J5EtNvHtl8A) **`150,662` views**)
- **Neighbour Gate (`neighbours.py`):** **PASS (`12` education videos `≥1,000,000` views, `TED-Ed/TED: yes`)** — saved in [`11_Upload-Package/evidence_2026-11-16_neighbours.json`](11_Upload-Package/evidence_2026-11-16_neighbours.json):
  1. `TED-Ed` ★ — [`li1kO3hg4iE`](https://youtu.be/li1kO3hg4iE) *Why do we have crooked teeth when our ancestors didn’t? - G. Richard Scott* (**`4,959,777` views**)
  2. `TED-Ed` ★ — [`jdrNjHPYKz4`](https://youtu.be/jdrNjHPYKz4) *Why do cats have vertical pupils? - Emma Bryce* (**`4,610,116` views**)
  3. `TED-Ed` ★ — [`mZt1Gn0R22Q`](https://youtu.be/mZt1Gn0R22Q) *Myths and misconceptions about evolution - Alex Gendler* (**`3,297,627` views**)
  4. `TEDx Talks` ★ — [`-wkdH_wluhw`](https://youtu.be/-wkdH_wluhw) *What animals are thinking and feeling, and why it should matter | Carl Safina | TEDxMidAtlantic* (**`3,037,161` views**)
  5. `TED-Ed` ★ — [`NTeOhj6dxsU`](https://youtu.be/NTeOhj6dxsU) *Is human evolution speeding up or slowing down? - Laurence Hurst* (**`2,534,442` views**)
  6. `TEDx Talks` ★ — [`18YwBwIK_no`](https://youtu.be/18YwBwIK_no) *How we found out evolution is true: John van Wyhe at TEDxNTU* (**`2,162,694` views**)
  7. `TED` ★ — [`GcJxRqTs5nk`](https://youtu.be/GcJxRqTs5nk) *Moral behavior in animals | Frans de Waal* (**`2,041,052` views**)
  8. `TED-Ed` ★ — [`5NdMnlt2keE`](https://youtu.be/5NdMnlt2keE) *Five fingers of evolution - Paul Andersen* (**`1,926,976` views**)
  9. `TED-Ed` ★ — [`j43wzuciAkk`](https://youtu.be/j43wzuciAkk) *A year in the life of one of Earth's weirdest animals - Gilad Bino* (**`1,656,436` views**)
  10. `TED-Ed` ★ — [`qrKZBh8BL_U`](https://youtu.be/qrKZBh8BL_U) *The evolution of the human eye - Joshua Harvey* (**`1,535,781` views**)

---

## 4. Candidate 4-Act Discovery Outline (All Claims UNVERIFIED Pending `SOURCES.md` & `facts` Lane)

- **Cold Open (0:00–0:45, UNVERIFIED):** In 2019, biologists at an English horse farm dressed ordinary domestic horses in black-and-white zebra coats and pointed high-speed cameras at them. What they filmed ended a 150-year argument between Charles Darwin and Alfred Russel Wallace — proving zebra stripes aren't for hiding from lions at all, but for blinding blood-sucking flies during the final half-second of landing.
- **Act I — Darwin vs Wallace & The Four Rival Theories (1871–2010, UNVERIFIED):** In *The Descent of Man* (**1871**), **Charles Darwin** noted that black-and-white stripes give zero camouflage on the open African plains, whereas **Alfred Russel Wallace** (*Darwinism*, **1889**) argued stripes hid zebras in tall grass at dusk or dazzled attacking lions. Over the next century, biologists proposed four main hypotheses: (1) predator camouflage or "motion dazzle" against lions, (2) social recognition within herds, (3) thermoregulation via black-and-white air convection eddies, and (4) protection against biting flies carrying fatal equine diseases.
- **Act II — Gábor Horváth's 2012 Polarised-Light Sticky-Horse Experiment (1981–2012, UNVERIFIED):** Following early tsetse-fly tests by **Jeffrey Waage** (`1981`), biophysicist **Gábor Horváth** and **Susanne Åkesson** in **February 2012** (*Journal of Experimental Biology*) set out sticky, oil-coated trays and full-sized horse mannequins in a Hungarian horsefly field — dark, white, and striped with varying stripe widths and polarisation angles. Dark coats reflect horizontally polarised light that attracts blood-seeking female **tabanid horseflies**; breaking the dark surface into narrow black-and-white vertical stripes (`matching the width of real zebra stripes`) slashed horsefly capture rates dramatically (`fewer flies than even pure white models`).
- **Act III — Tim Caro's 2014 All-Africa Map & 2016 Lion-Vision Disproof (2014–2016, UNVERIFIED):** In **April 2014** (*Nature Communications*), evolutionary ecologist **Tim Caro** at UC Davis mapped body-stripe thickness, leg striping, and belly striping across all **7 wild equid species and 20 subspecies** against 29 environmental variables across Africa and Asia. Stripe intensity showed **no correlation** with lion range, woodland cover, ambient temperature, or herd size — and a **strong, statistically significant correlation with months of biting tabanid and tsetse fly activity** (where zebra hair is also shorter than horsefly mouthparts, `~2 mm`). In **2016** (*PLOS ONE*), Caro and **Amanda Melin** measured zebra stripes through lion and spotted-hyena visual acuity filters and proved that beyond `50 metres` in daylight (`or 30 metres at twilight`), a lion's eyes cannot even resolve zebra stripes — by the time a lion sees the stripes, it already smells and hears the zebra!
- **Act IV — The 2019 Somerset Horse-in-a-Zebra-Coat Experiment (2019, UNVERIFIED):** How exactly do stripes stop a horsefly? In **February 2019** (*PLOS ONE*), **Tim Caro** and **Martin How** at a livery yard in Dundry, North Somerset, UK, filmed tabanid horseflies around captive plains zebras, domestic horses, and **the same domestic horses wearing black, white, or black-and-white zebra-striped cloth coats** (with exposed heads as an internal control). High-speed video trajectories revealed the twist: horseflies approached zebras and horses at the **exact same rate** from afar, and landed normally on the uncovered horse heads — **but within the last `0.5 metres` (`last ~0.5 seconds`), flies approaching the striped coats failed to decelerate**, veering away or literally bouncing off the zebra skin (`landing rate under a quarter of that on black or white coats`), because close-range stripes disrupt the optic-flow loom reflex flies rely on to land!

---

## 5. Two Candidate Search-Titled Shorts (`Test B` / `Rule 26` / `Rule 32` — UNVERIFIED Concepts Only)

- **Short `S01`:** *Do Zebra Stripes Actually Hide Them From Lions?* (`47 chars`, `0` exact collisions, positive search question)
  - **First-line answer hook (UNVERIFIED):** *"You were taught zebra stripes camouflage them from lions — but vision tests proved a hunting lion can't even see the stripes until the zebra is already in hearing range."*
  - **Frame-0 & Payoff Plan (`Rules 2, 3, 6, 24, 27`):** Frame 0 (`0.0s`, `mode: "cover"`): close moving shot of a plains zebra standing on open grass as the view switches into a blurred lion-vision optical filter (`NOT FOR LIONS`, `#FFE000` on `NOT`). Payoff at `≥70%` runtime (`~17.0s / 23.5s`): Tim Caro's 2014–2016 proof that beyond `50 metres` lions see a zebra as a solid grey silhouette, and stripes evolved instead where blood-sucking horseflies carry fatal equine diseases. Loop tail `<1.0s`, zero CTA.
- **Short `S02`:** *Why Did Scientists Dress Horses in Zebra Coats?* (`47 chars`, `0` exact collisions, positive search question)
  - **First-line answer hook (UNVERIFIED):** *"In 2019, biologists dressed English horses in striped zebra coats — and filmed blood-sucking horseflies crashing straight into them without landing."*
  - **Frame-0 & Payoff Plan (`Rules 2, 3, 6, 24, 27`):** Frame 0 (`0.0s`, `mode: "cover"`): close moving shot of a brown horse wearing a tailored black-and-white striped coat as a horsefly ricochets off its flank (`FLIES CAN'T LAND`, `#FFE000` on `CAN'T`). Payoff at `≥70%` runtime (`~17.2s / 23.5s`): Caro & How's 2019 Somerset experiment proving that within the final `0.5 metres`, narrow stripes scramble a horsefly's optic-flow landing reflex so it fails to brake and bounces off (`cutting landings by >75%`). Loop tail `<1.0s`, zero CTA.
