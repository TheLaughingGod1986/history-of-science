# Topic Brief — `116_Darwin-Cannon-Hsu-Why-Do-We-Get-Goosebumps` (`HOS:116` Proposal)

> **PROPOSAL & RULE G STATUS (`J2963`, `2026-11-16`):**
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
- All folders in `02_Video-Projects/` (`000`–`018`, `099`–`101` on `main`),
- Open topic PRs `#572` (`102` Ozone Hole, `103` Why Is the Sky Blue), `#581` (`104` Speed of Light, `105` Venus Flytrap), `#588` (`106` Eels & Sargasso Sea, `107` Autumn Leaves & Chlorophyll), `#602` (`108` Why Is Ice Slippery, `109` Why Do Fingers Wrinkle in Water), `#607` (`110` Why Do Onions Make You Cry, `111` Why Do Knuckles Crack), `#614` (`112` Why Do We Yawn, `113` How Do Cats Land on Their Feet), and `#618` (`114` How Do Chameleons Change Colour, `115` Why Do Zebras Have Stripes),
- All `011`–`095` backlog entries in `00_Brand/Channel-Setup/VIDEO_BACKLOG.json` and `00_Brand/Channel-Setup/ideas/` (including `096` Axolotl Regeneration and `097` Octopus/Chameleon Camouflage in `IDEAS_2026-10-21_J0790.md`; `058` covers McCulloch, Gurdon & Yamanaka on bone-marrow stem cells and iPSCs; `084` covers Santorio, Blagden, Wunderlich & Kluger on body temperature and fever; **none** cover why humans get goosebumps, Charles Darwin's 1872 vestigial *arrector pili* theory, Walter Bradford Cannon's 1915 sympathetic piloerection experiments, or Ya-Chieh Hsu & Yulia Shwartz's July 2020 Harvard discovery of the sympathetic nerve–muscle–stem-cell bridge).
- **Result:** **Zero overlap.**

---

## 3. Packaging, Why It Should Work & Search/Neighbour Evidence (`Rule 26` + `neighbours.py` + `public_search.py`)

- **Title A (Primary Proposal, `LEARNINGS.md` Rules 1, 15, 23, 26 — `52 chars`, `0` exact collisions):** `Why Do We Get Goosebumps? (The 2020 Stem-Cell Twist)`
- **Title B (Test & Compare Arm 2, `Rule 23` — `56 chars`, `0` exact collisions):** `Goosebumps Aren't Useless (The Hidden Hair-Growth Nerve)`
- **Title C (`Rule 26` Exact Phrase First — `56 chars`, `0` exact collisions):** `Why Do We Get Goosebumps? The Hidden Nerve-Muscle Switch`
- **One-Line Hook:** For 150 years since Charles Darwin, every biology textbook taught that human goosebumps are a useless evolutionary leftover from furry ancestors — until a July 2020 Harvard electron-microscopy experiment proved the tiny muscle that pulls your hair upright is actually a physical bridge linking your nerves directly to stem cells to trigger new hair growth in the cold.
- **Why It Should Work (Past Winners & `LEARNINGS.md` Rules):**
  - Resembles top HOS longs **`002` Periodic Table (`AL_-qlWko_g`, `161` views, `2.68/d`, `1,160` impressions, `3.36%` CTR)** and **`004` Inside an Atom (`GHZDsiH7L7A`, `34` views, `1.06/d`, `837` impressions)** by opening with an exact, high-volume everyday question people type into YouTube (`Why Do We Get Goosebumps?`) backed by `6` education neighbours `≥1M` views (`Rules 1, 15, 26`), while pairing that search demand with a concrete bodily mechanism like **`006` Willow Tree (`VbPubYd6Fbs`, `53.96%` Studio / `79%` 28d YTA avg view %)** and **`007` First Vaccine (`ETynHpIYLeY`, `7.41%` CTR)** so it avoids the low-impression starvation of statement-titled `005` (`15` impressions).
  - Resembles top HOS Shorts **`29bpGAI0wb8` (*What happens if you keep cutting gold in half?*, `1,227` views, `39.58/d`)**, **`-3L6HzJ_d_4` (*What Is the Pasteur Swan Neck Flask Experiment?*, `129` views, `77.14%` stayed PASS, `75.23%` avg view % PASS)**, and **`oKqmnJNGiHg` (*How Was Phosphorus Discovered?*, `188` views, `87.02%` avg view % PASS)** by answering a universal human-body mystery with a microscopic anatomical reveal at `≥70%` runtime (`Rules 2, 6, 8, 24, 27, 28, 30, 32`).
- **3-Way Thumbnail Test & Compare Plan (`LEARNINGS.md` Rules 11, 12, 14 + `THUMBNAIL_AND_TITLE_RULES.md` §2.1–2.B):**
  - **Thumb A (Hero Object — The Cutaway Hair Follicle Bridge):** Painted 3D house-style key art: a dramatic cross-section of a goosebump rising on human skin on the right two-thirds, showing the red *arrector pili* muscle pulling a hair shaft upright while a glowing gold sympathetic nerve ribbon wraps around blue stem cells at the base; the Explorer small at lower left; cream/gold serif text on the clear left band: `NOT USELESS` (`2 words`, gold on `NOT`, zero overlap on the follicle).
  - **Thumb B (`Rule 14` Bright High-Contrast Variant — Cold Air vs Stem-Cell Switch):** Bright sunlit Harvard laboratory cutaway key art: a frost-chilled patch of skin on the right where a glowing nerve-muscle triad lights up a cluster of hair-follicle stem cells like a switchboard; Explorer small at lower left; serif text on the left band: `HIDDEN SWITCH` (`2 words`, gold on `SWITCH`).
  - **Thumb C (Darwin's Vestigial Myth-Bust):** Painted 3D key art comparing a bristling furry mammal coat beside a human arm with raised goosebumps and a glowing microscope lens revealing the deep stem-cell connection; Explorer small at lower left; serif text on the left band: `DARWIN MISSED THIS` (`3 words`, gold on `MISSED`).
- **Signed-out YouTube Autocomplete (`2026-11-16`):**
  - `"why do we get goosebumps"` → **`autocomplete = yes`** (`why do we get goosebumps`, `why do we get goosebumps when listening to music`, `why do we get goosebumps dr binocs show`, `why do we get goosebumps when we are cold`, `why do we get goosebumps zack d films`)
  - `"what causes goosebumps"` → **`autocomplete = yes`** (`what causes goosebumps`, `what causes chills in your body`, `what causes chills without fever`)
  - `"arrector pili muscle"` → **`autocomplete = yes`** (`arrector pili muscle`, `arrector pili muscle pronunciation`)
- **Rule 26(a) Two Ranking Videos (`≥10,000` views, retrieved `2026-11-16`):**
  1. `Peekaboo Kidz` — [`D95vHi3mQ5I`](https://youtu.be/D95vHi3mQ5I) *Why Do We Get Goosebumps? | The Dr. Binocs Show* (**`5,779,913` views**)
  2. `AsapSCIENCE` — [`-EA2eWZuYDs`](https://youtu.be/-EA2eWZuYDs) *The Science of Goosebumps and Music Chills* (**`1,976,968` views**; plus `It's AumSum Time` [`TDkDcz5TsVs`](https://youtu.be/TDkDcz5TsVs) **`589,125` views**, `Institute of Human Anatomy` [`_WH8ISdxVkQ`](https://youtu.be/_WH8ISdxVkQ) **`361,068` views**, `Doctor Myro` [`dmA9F9zyioA`](https://youtu.be/dmA9F9zyioA) **`197,271` views**, and `SciShow Kids` [`KD78ZlViWt4`](https://youtu.be/KD78ZlViWt4) **`150,169` views**)
- **Neighbour Gate (`neighbours.py`):** **PASS (`6` education videos `≥1,000,000` views, `TED-Ed/TED: yes`)** — saved in [`11_Upload-Package/evidence_2026-11-16_neighbours.json`](11_Upload-Package/evidence_2026-11-16_neighbours.json):
  1. `CrashCourse` — [`Orumw-PyNjw`](https://youtu.be/Orumw-PyNjw) *The Integumentary System, Part 1 - Skin Deep: Crash Course Anatomy & Physiology #6* (**`5,938,621` views**)
  2. `TEDx Talks` ★ — [`rXNt_X5F67I`](https://youtu.be/rXNt_X5F67I) *Healthy skin starts from within | Barbara Paldus | TEDxPrague* (**`5,584,292` views**)
  3. `TED-Ed` ★ — [`_r4c2NT4naQ`](https://youtu.be/_r4c2NT4naQ) *The science of skin color - Angela Koine Flynn* (**`3,540,388` views**)
  4. `TED-Ed` ★ — [`OxPlCkTKhzY`](https://youtu.be/OxPlCkTKhzY) *The science of skin - Emma Bryce* (**`2,362,721` views**)
  5. `TED` ★ — [`OeGpf1MyM2M`](https://youtu.be/OeGpf1MyM2M) *5 Skin Health Myths to Stop Believing Now | Body Stuff with Dr. Jen Gunter* (**`1,137,270` views**)
  6. `Be Smart` — [`sMCgOQj37IY`](https://youtu.be/sMCgOQj37IY) *Why Does Hair Grow The Way It Does?* (**`1,073,609` views**; plus `TED-Ed` [`iCBzEZek5cY`](https://youtu.be/iCBzEZek5cY) *How long can hair grow? - Maksim Plikus* **`812,308` views** and `SciShow Kids` [`KD78ZlViWt4`](https://youtu.be/KD78ZlViWt4) *Why Do We Get Goosebumps?* **`150,169` views**)

---

## 4. Candidate 4-Act Discovery Outline (All Claims UNVERIFIED Pending `SOURCES.md` & `facts` Lane)

- **Cold Open (0:00–0:45, UNVERIFIED):** Step into cold air and millions of microscopic muscles across your skin contract at once, pulling every hair upright into goosebumps. Since Charles Darwin in 1872, every textbook taught that human goosebumps are a useless evolutionary leftover because we lost our thick fur coat — until a July 2020 Harvard experiment discovered why evolution refused to delete them.
- **Act I — Kölliker's Microscopic Muscle (1849) & Charles Darwin's 1872 Vestigial Verdict (1849–1872, UNVERIFIED):** In **1849**, Swiss histologist **Albert von Kölliker** identified the microscopic smooth muscle fibres attached to every mammalian hair follicle (*arrector pili*). Twenty-three years later, in **November 1872** (*The Expression of the Emotions in Man and Animals*), **Charles Darwin** compared human goosebumps ("cutis anserina") to a frightened cat puffing its fur to look larger or a chilled bird fluffing its feathers to trap warm air — concluding that on nearly hairless human skin, the reflex is a **vestigial evolutionary relic** that no longer serves any thermal or defensive use.
- **Act II — Walter Bradford Cannon & the 1915 Fight-or-Flight Adrenaline Wire (1915–1929, UNVERIFIED):** In **1915** (*Bodily Changes in Pain, Hunger, Fear and Rage*), Harvard physiologist **Walter Bradford Cannon** traced how the **sympathetic nervous system** and adrenal medulla fire together during cold or sudden fear, sending norepinephrine down autonomic nerve fibres to contract the *arrector pili* muscles in seconds. For the next century, physiology textbooks treated the goosebump circuit as a one-way wire from nerve to muscle: an involuntary spasm that dimples the skin and does nothing else.
- **Act III — Ya-Chieh Hsu & Yulia Shwartz's July 2020 Electron-Microscope Surprise (2020, UNVERIFIED):** If goosebumps are useless in hairless skin, why does the body maintain a dense web of sympathetic nerves and smooth muscles around every single follicle? In **July 2020** (*Cell*), Harvard stem-cell biologist **Ya-Chieh Hsu** and postdoc **Yulia Shwartz** used high-resolution electron microscopy to trace the exact path of the sympathetic nerve at the base of the follicle. They discovered the nerve doesn't stop at the *arrector pili* muscle: it continues past the muscle and wraps directly around **hair-follicle stem cells** like a ribbon, forming direct **synapse-like junctions** with the stem cells themselves!
- **Act IV — The Two-Speed Cold Switch & Missing-Muscle Proof (2020, UNVERIFIED):** Hsu and Shwartz proved that the *arrector pili* muscle is actually the **structural scaffold** that holds the sympathetic nerve pressed against the hair-follicle stem cells. When they genetically deleted the *arrector pili* muscle, the sympathetic nerve retracted away from the follicle and the stem cells went dormant. Together, nerve, muscle, and stem cell act as a **two-speed cold sensor**: a brief chill triggers a fast muscle contraction (a goosebump in seconds), whereas prolonged cold causes the nerve to release higher levels of **norepinephrine** directly onto the stem cells via `ADRB2` receptors, waking them up to regenerate the follicle and grow a new coat of hair!

---

## 5. Two Candidate Search-Titled Shorts (`Test B` / `Rule 26` / `Rule 32` — UNVERIFIED Concepts Only)

- **Short `S01`:** *Why Do We Still Get Goosebumps Without Fur?* (`43 chars`, `0` exact collisions, positive search question)
  - **First-line answer hook (UNVERIFIED):** *"You were taught goosebumps are a useless leftover from when our ancestors had fur — but a 2020 Harvard experiment found their hidden second job."*
  - **Frame-0 & Payoff Plan (`Rules 2, 3, 6, 24, 27`):** Frame 0 (`0.0s`, `mode: "cover"`): extreme close moving cutaway of a human hair follicle pulling upright into a goosebump as a glowing gold nerve lights up beneath the skin (`NOT USELESS`, `#FFE000` on `NOT`). Payoff at `≥70%` runtime (`~17.0s / 23.5s`): Ya-Chieh Hsu & Yulia Shwartz's July 2020 Harvard discovery that the tiny goosebump muscle acts as a physical bridge holding sympathetic nerves against hair-follicle stem cells to trigger new hair growth in sustained cold. Loop tail `<1.0s`, zero CTA.
- **Short `S02`:** *How Do Goosebumps Wake Up Your Hair Stem Cells?* (`47 chars`, `0` exact collisions, positive search question)
  - **First-line answer hook (UNVERIFIED):** *"Every goosebump on your arm is wired directly to a cluster of stem cells — and removing that tiny muscle shuts new hair growth down."*
  - **Frame-0 & Payoff Plan (`Rules 2, 3, 6, 24, 27`):** Frame 0 (`0.0s`, `mode: "cover"`): close moving 3D view of the red *arrector pili* muscle contracting and pressing a glowing nerve ribbon against blue stem cells (`STEM CELL SWITCH`, `#FFE000` on `SWITCH`). Payoff at `≥70%` runtime (`~17.2s / 23.5s`): when Harvard researchers removed the goosebump muscle in 2020, the sympathetic nerve pulled away from the follicle and cold-induced hair regeneration stopped — proving muscle, nerve, and stem cell form a three-part cold switch. Loop tail `<1.0s`, zero CTA.
