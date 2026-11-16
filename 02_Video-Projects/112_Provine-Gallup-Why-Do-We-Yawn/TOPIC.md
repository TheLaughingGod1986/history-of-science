# Topic Brief — `112_Provine-Gallup-Why-Do-We-Yawn` (`HOS:112` Proposal)

> **PROPOSAL & RULE G STATUS (`J2935`, `2026-11-16`):**
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
  - **Shared pattern (Subject, Title Shape, Opening, Thumbnail Concept, Length):** `002` and `004` together generate **`92.0%` (`1,997 / 2,170`) of all HOS long impressions** and **`84.8%` (`195 / 230`) of all HOS long views** because their titles open with plain, high-volume curriculum/search questions (`Periodic Table`, `What's Inside an Atom?`) backed by massive `TED-Ed` neighbour pools (`LEARNINGS.md` Rules 1, 15, 26), run `8.5–9.0 min` (`525–541s`), and open on concrete physical proof (`60–71%` at `0:15`, Rule 10). Meanwhile `006` (`53.96%` Studio avg viewed) shows strong retention on a concrete tabletop experiment once clicked, but its poetic statement title without an autocomplete question (`46` impressions in `11d`) starved it of search discovery.
- **3 Worst HOS Longs & What They Share (Hypotheses on Small N):**
  1. **`frP_YrNShsU` (`003` *How Did We Discover X-rays?*, `426s`)** — **`0.09` views/day** (`5` views in `53d`), `41` impressions, `2.44%` CTR, `26.65%` avg view %.
  2. **`_C92tIJCk8A` (`001` *How Did We Discover Germs?*, `365s`)** — **`0.09` views/day** (`7` views in `74d`), `44` impressions, `6.82%` CTR, `48.08%` avg view %.
  3. **`wwcjcFfC-5M` (`005` *The Tied Arm That Proved Your Blood Circulates*, `529s`)** — **`0.28` views/day** (`5` views in `18d`), `15` impressions, `20.00%` CTR, `9.24%` avg view %.
  - **Shared pattern:** Either generic textbook-chapter questions lacking a specific hook/twist (`001`, `003`, shorter `6–7 min` runtimes) or apparatus-first declarative statements (`005` *The Tied Arm...*, `15` impressions) that omit the plain question viewers actually type into YouTube search (`LEARNINGS.md` Rules 15, 23, 26). **Lesson applied to `HOS:112`:** Start verbatim with the high-volume signed-out autocomplete question (`Why Do We Yawn?`) and follow immediately with the concrete discovery twist (`(The Brain-Cooling Experiment)`).

### 1b. All `30` Public HOS Shorts — Ranked by Views/Day Since Publish (`2026-11-16`)

| Rank | Video ID | Title | Published (`age_days`) | Views (`2026-11-16`) | Views / Day | Stayed to Watch (`studio_ctr.json`) | Studio Avg View % (`avgViewSeconds / sec`) | Likes |
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
  2. **`-3L6HzJ_d_4` (*What Is the Pasteur Swan Neck Flask Experiment?*, `19s`)** — **`6.45` views/day** (`129` views in `20d`), channel-best **`77.14%` stayed-to-watch (PASS `≥60%`)** and **`75.23%` avg view % (PASS `≥70%`)**, with **`87%` (`112 / 129`) of 28d views coming from YouTube search** — the first mature `100+` view HOS Short to pass both targets (`LEARNINGS.md` Rules 28 & 32).
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
- Open topic PRs `#572` (`102` Ozone Hole, `103` Why Is the Sky Blue), `#581` (`104` Speed of Light, `105` Venus Flytrap), `#588` (`106` Eels & Sargasso Sea, `107` Autumn Leaves & Chlorophyll), `#602` (`108` Why Is Ice Slippery, `109` Why Do Fingers Wrinkle in Water), and `#607` (`110` Why Do Onions Make You Cry, `111` Why Do Knuckles Crack),
- All `011`–`097` backlog entries in `00_Brand/Channel-Setup/VIDEO_BACKLOG.json` and `00_Brand/Channel-Setup/ideas/` (`046` covers Berger, Kleitman & Aserinsky on EEG brainwaves and REM sleep; `074` covers Hooke, Lower & Bohr on lungs and oxygen transport; `084` covers Santorio, Wunderlich & Kluger on body temperature and fever; **none** cover why humans and vertebrates yawn, Robert Provine's 1987 $\text{CO}_2/\text{O}_2$ breathing-chamber experiment disproving the oxygen myth, or Andrew & Gordon Gallup's 2007–2010 forehead cold-pack and brain-thermoprobe experiments on cranial thermoregulation).
- **Result:** **Zero overlap.**

---

## 3. Packaging, Why It Should Work & Search/Neighbour Evidence (`Rule 26` + `neighbours.py` + `public_search.py`)

- **Title A (Primary Proposal, `LEARNINGS.md` Rules 1, 15, 23, 26 — `46 chars`, `0` exact collisions):** `Why Do We Yawn? (The Brain-Cooling Experiment)`
- **Title B (Test & Compare Arm 2, `Rule 23` — `52 chars`, `0` exact collisions):** `The 1987 Gas Chamber That Proved Why You Really Yawn`
- **Title C (`Rule 26` Exact Phrase First — `55 chars`, `0` exact collisions):** `Why Do We Yawn? How a Cold Pack Broke a 2,000-Year Myth`
- **One-Line Hook:** For 2,000 years doctors taught that yawning pulls extra oxygen into tired lungs — until a 1987 gas-chamber test proved oxygen has zero effect on yawning and a 2007 forehead ice-pack experiment revealed your jaw is a radiator for an overheating brain.
- **Why It Should Work (Past Winners & `LEARNINGS.md` Rules):**
  - Resembles top HOS longs **`002` Periodic Table (`AL_-qlWko_g`, `161` views, `2.68/d`, `1,160` impressions, `3.36%` CTR)** and **`004` Inside an Atom (`GHZDsiH7L7A`, `34` views, `1.06/d`, `837` impressions)** by opening with an everyday universal search phrase (`Why Do We Yawn?`) backed by a `15`-video `≥1M` `TED-Ed` / `TED` neighbour pool (`Rules 1, 15, 26`), while pairing that search demand with a concrete laboratory apparatus story like **`006` Willow Tree (`VbPubYd6Fbs`, `53.96%` Studio / `79%` 28d YTA avg view %)** so it avoids the low-impression starvation of statement-titled `005` (`15` impressions) and `006` (`46` impressions).
  - Resembles top HOS Shorts **`29bpGAI0wb8` (*What happens if you keep cutting gold in half?*, `1,227` views, `39.58/d`)** and **`-3L6HzJ_d_4` (*What Is the Pasteur Swan Neck Flask Experiment?*, `129` views, `77.14%` stayed PASS, `75.23%` avg view % PASS)** by replacing statement titles like `Wvjd8g0CpzE` (`14.80%` stayed MISS) and `PFj6172YU4Q` (`15.98%` stayed MISS) with direct myth-busting search questions (`Rules 2, 8, 24, 27, 28, 30, 32`).
- **3-Way Thumbnail Test & Compare Plan (`LEARNINGS.md` Rules 11, 12, 14 + `THUMBNAIL_AND_TITLE_RULES.md` §2.1–2.B):**
  - **Thumb A (Hero Object — Thermal Brain Radiator):** Painted 3D house-style key art: a glowing thermal cutaway profile of a yawning head on the right two-thirds showing a red-hot brain cooling to icy blue as cool air rushes into the stretched jaw; the Explorer small at lower left holding a brass thermometer; cream/gold serif text on the clear left band: `HOT BRAIN` (`2 words`, gold on `HOT`, zero overlap on the head).
  - **Thumb B (`Rule 14` Bright High-Contrast Variant — The Forehead Cold Pack):** Bright sunlit laboratory key art: a volunteer watching a screen with a glowing blue ice pack pressed to their forehead while a red `0 YAWNS` counter ticks beside them; Explorer small at lower left; serif text on the left band: `ICE PACK TEST` (`3 words`, gold on `ICE`).
  - **Thumb C (The 1987 Oxygen Chamber Myth-Bust):** Painted 3D key art of Robert Provine's 1987 breathing mask and glass gas cylinders labelled `O₂` and `CO₂` on the right, with the volunteer yawning right through pure oxygen; Explorer small at lower left; serif text on the left band: `NOT OXYGEN` (`2 words`, gold on `NOT`).
- **Signed-out YouTube Autocomplete (`2026-11-16`):**
  - `"why do we yawn"` → **`autocomplete = yes`** (`why do we yawn`, `why do we yawn when someone else yawns`, `why do we yawn while praying`, `why do we yawn dr binocs`, `why do we yawn factoholic`)
  - `"why is yawning contagious"` → **`autocomplete = yes`** (`why is yawning contagious`, `why is yawning contagious ted ed`, `why is yawning so contagious`)
- **Rule 26(a) Two Ranking Videos (`≥10,000` views, retrieved `2026-11-16`):**
  1. `AsapSCIENCE` — [`I0dQx4SNSwE`](https://youtu.be/I0dQx4SNSwE) *Why Do We Yawn?* (**`4,651,480` views**)
  2. `Vsauce` — [`jGIbUK4NwIw`](https://youtu.be/jGIbUK4NwIw) *Why Do We Yawn?* (**`4,827,754` views**; plus `TED-Ed` [`4NpG4F9yq00`](https://youtu.be/4NpG4F9yq00) *Why is yawning contagious? - Claudia Aguirre* **`2,452,069` views**, `Peekaboo Kidz` [`CF9bd42dc6I`](https://youtu.be/CF9bd42dc6I) **`1,049,428` views**, and `SciShow` [`ew_iZTPoC3c`](https://youtu.be/ew_iZTPoC3c) **`466,444` views**)
- **Neighbour Gate (`neighbours.py`):** **PASS (`15` education videos `≥1,000,000` views, `TED-Ed/TED: yes`)** — saved in [`11_Upload-Package/evidence_2026-11-16_neighbours.json`](11_Upload-Package/evidence_2026-11-16_neighbours.json):
  1. `TED` ★ — [`5MuIMqhT8DM`](https://youtu.be/5MuIMqhT8DM) *Sleep Is Your Superpower | Matt Walker | TED* (**`17,757,465` views**)
  2. `TED-Ed` ★ — [`dqONk48l5vY`](https://youtu.be/dqONk48l5vY) *What would happen if you didn't sleep? - Claudia Aguirre* (**`15,049,764` views**)
  3. `TED-Ed` ★ — [`v-t1Z5-oPtU`](https://youtu.be/v-t1Z5-oPtU) *How stress affects your body - Sharon Horesh Bergquist* (**`9,128,903` views**)
  4. `TED-Ed` ★ — [`WuyPuH9ojCE`](https://youtu.be/WuyPuH9ojCE) *How stress affects your brain - Madhumita Murgia* (**`9,029,031` views**)
  5. `TED-Ed` ★ — [`gedoSfZvBgE`](https://youtu.be/gedoSfZvBgE) *The benefits of a good night's sleep - Shai Marcu* (**`7,504,199` views**)
  6. `TED-Ed` ★ — [`idrbwnWLJ7w`](https://youtu.be/idrbwnWLJ7w) *What staying up all night does to your brain - Anna Rothschild* (**`7,295,896` views**)
  7. `TED` ★ — [`fQUeDdaVoWo`](https://youtu.be/fQUeDdaVoWo) *Do You Really Need 8 Hours of Sleep Every Night? | Body Stuff with Dr. Jen Gunter | TED* (**`4,613,278` views**)
  8. `TED` ★ — [`t0kACis_dJE`](https://youtu.be/t0kACis_dJE) *6 tips for better sleep | Sleeping with Science, a TED series* (**`2,893,294` views**)
  9. `TED-Ed` ★ — [`Amkg1cdDCpM`](https://youtu.be/Amkg1cdDCpM) *Can you change your sleep schedule?* (**`2,713,053` views**)
  10. `TED-Ed` ★ — [`4NpG4F9yq00`](https://youtu.be/4NpG4F9yq00) *Why is yawning contagious? - Claudia Aguirre* (**`2,452,069` views**)

---

## 4. Candidate 4-Act Discovery Outline (All Claims UNVERIFIED Pending `SOURCES.md` & `facts` Lane)

- **Cold Open (0:00–0:45, UNVERIFIED):** Right now, just reading the word *yawn* is trying to force your jaw wide open. For 2,000 years, doctors taught that you yawn because your blood is low on oxygen — until a 1987 gas-chamber experiment proved pure oxygen doesn't stop a single yawn, and a 2007 ice-pack experiment revealed your jaw is actually a radiator for an overheating brain.
- **Act I — Hippocrates' "Bad Air" & The 2,000-Year Oxygen Myth (400 BC–1986, UNVERIFIED):** From Hippocrates' treatise *On Winds* (`~400 BC`, claiming yawning vents hot "bad air" before a fever) to 18th- and 20th-century physiology textbooks, medicine assumed yawning is a respiratory reflex triggered when blood carbon dioxide ($\text{CO}_2$) rises and oxygen ($\text{O}_2$) falls in a stuffy room.
- **Act II — Robert Provine's 1987 Gas-Chamber Experiment (1986–1987, UNVERIFIED):** In **1987** (*Bulletin of the Psychonomic Society*), neuroscientist Robert R. Provine and colleagues at the University of Maryland Baltimore County put volunteers inside breathing masks fed by compressed gas cylinders: normal air, `3%–5%` $\text{CO}_2$ (over `100×` normal atmospheric $\text{CO}_2$), or `100%` pure medical $\text{O}_2$. Breathing rates doubled under high $\text{CO}_2$ — **yet yawning frequency did not change at all**, and exercise that doubled oxygen demand didn't alter yawning either, demolishing the 2,000-year oxygen hypothesis in one afternoon.
- **Act III — Andrew & Gordon Gallup's 2007 Forehead Cold-Pack Experiment (2007, UNVERIFIED):** Why, then, does a yawn require a `5-second` maximal jaw stretch alongside a deep inhalation? In **May 2007** (*Evolutionary Psychology*), Andrew C. Gallup and Gordon G. Gallup Jr. at SUNY Albany propose the **cranial thermoregulation (brain-cooling) hypothesis**: stretching the jaw flexes the pterygoid venous plexus around the sinus walls while cool air cools venous blood returning to the skull. When volunteers watch contagious-yawning videos while holding a **warm pack (`46°C`)** vs a **cold pack (`4°C`)** to their foreheads, or breathing strictly through the nose, nasal breathing and the forehead cold pack drop contagious yawning from **`41%` down to `9%` (`0%` with nasal cooling)**!
- **Act IV — Brain Thermoprobes & Why Yawning Is Contagious (2010–2014, UNVERIFIED):** In **2010** (*Frontiers in Evolutionary Neuroscience*), Gallup and colleagues implant micro-thermoprobes directly into the frontal cortex of rats and record cortical temperature rising **`~0.1–0.2°C`** in the seconds before a yawn — then dropping back to baseline immediately after the yawn finishes (`with an optimal 20°C ambient "thermal window" proved in Vienna & Arizona in 2011–2014`), explaining contagious yawning as a herd-vigilance reflex that cools the brains of an entire group at once.

---

## 5. Two Candidate Search-Titled Shorts (`Test B` / `Rule 26` / `Rule 32` — UNVERIFIED Concepts Only)

- **Short `S01`:** *Does Yawning Actually Give You More Oxygen?* (`43 chars`, `0` exact collisions, positive search question)
  - **First-line answer hook (UNVERIFIED):** *"You were taught you yawn because your lungs need extra oxygen — but a 1987 gas mask experiment proved pure oxygen doesn't stop a single yawn."*
  - **Frame-0 & Payoff Plan (`Rules 2, 3, 6, 24, 27`):** Frame 0 (`0.0s`, `mode: "cover"`): close moving shot of a volunteer yawning inside a clear glass breathing mask connected to a `100% O₂` cylinder (`NOT OXYGEN`, `#FFE000` on `NOT`). Payoff at `≥70%` runtime (`~17.0s / 23.5s`): Robert Provine's 1987 discovery that neither `100%` oxygen nor `100×` carbon dioxide changes yawning, because yawning flexing the jaw cools an overheating brain. Loop tail `<1.0s`, zero CTA.
- **Short `S02`:** *Why Does a Cold Pack on Your Forehead Stop Yawning?* (`51 chars`, `0` exact collisions, positive search question)
  - **First-line answer hook (UNVERIFIED):** *"Pressing a cold pack against your forehead nearly switches off contagious yawning — because your jaw is actually a radiator for your brain."*
  - **Frame-0 & Payoff Plan (`Rules 2, 3, 6, 24, 27`):** Frame 0 (`0.0s`, `mode: "cover"`): close moving thermal cutaway of a glowing red brain cooling to blue as a frost-covered cold pack touches the forehead (`BRAIN COOLER`, `#FFE000` on `COOLER`). Payoff at `≥70%` runtime (`~17.2s / 23.5s`): Andrew Gallup's 2007 experiment showing a forehead cold pack drops contagious yawning from `41%` to `9%` by cooling the venous blood before a yawn is needed. Loop tail `<1.0s`, zero CTA.
