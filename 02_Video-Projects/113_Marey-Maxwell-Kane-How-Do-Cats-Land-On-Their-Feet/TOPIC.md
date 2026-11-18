# Topic Brief — `113_Marey-Maxwell-Kane-How-Do-Cats-Land-On-Their-Feet` (`HOS:113` Proposal)

> **RULE-E GO & RULE G STATUS (`J2935` / `J2937`, `2026-11-16`):**
> - **Rule-E Verdict (`J2937`):** **GO (`95.5 / 100` · `9.55 / 10` Opportunity Score)** — Pre-cleared in the History of Science waiting line (`jobs/WIP.json` `next_hos`) under **Rule G** (`active` has `4 / 4` HOS slots full: `008`, `009`, `010`, `013`). Nothing is started in production (`status.json` stages are all `todo`).
> - **Awaits Active HOS WIP Slot, `SOURCES.md` & `facts` Lane:** All historical and scientific claims in this brief are **UNVERIFIED** working notes. Before any script is locked, VO is recorded, or picture credit is spent, an active HOS WIP slot must open and every claim must be backed by verbatim primary-source quotes in `SOURCES.md` and verified through the `facts` lane (`gemini-agy`).

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
  - **Shared pattern:** Either generic textbook-chapter questions lacking a specific hook/twist (`001`, `003`, shorter `6–7 min` runtimes) or apparatus-first declarative statements (`005` *The Tied Arm...*, `15` impressions) that omit the plain question viewers actually type into YouTube search (`LEARNINGS.md` Rules 15, 23, 26). **Lesson applied to `HOS:113`:** Start verbatim with the high-volume signed-out autocomplete question (`How Do Cats Land on Their Feet?`) and follow immediately with the concrete discovery twist (`(The 1894 Camera Twist)` / `(1894 Photo Proof)`).

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
- Open topic PRs `#572` (`102` Ozone Hole, `103` Why Is the Sky Blue), `#581` (`104` Speed of Light, `105` Venus Flytrap), `#588` (`106` Eels & Sargasso Sea, `107` Autumn Leaves & Chlorophyll), `#602` (`108` Why Is Ice Slippery, `109` Why Do Fingers Wrinkle in Water), `#607` (`110` Why Do Onions Make You Cry, `111` Why Do Knuckles Crack), and sibling proposal `112` (Why Do We Yawn),
- All `011`–`097` backlog entries in `00_Brand/Channel-Setup/VIDEO_BACKLOG.json` and `00_Brand/Channel-Setup/ideas/` (`009` covers Newton's falling Moon and universal gravitation; `094` covers gecko van der Waals adhesion and spider silk; **none** cover the falling-cat righting reflex, conservation of angular momentum in a zero-torque flip, Étienne-Jules Marey's 1894 60-fps chronophotographic camera proof at the Paris Academy of Sciences, or Thomas Kane & M. P. Scher's 1969 Stanford/NASA zero-gravity astronaut maneuvering equations).
- **Result:** **Zero overlap.**

---

## 3. Packaging, Why It Should Work & Search/Neighbour Evidence (`Rule 26` + `neighbours.py` + `public_search.py`)

- **Title A (Primary Proposal, `LEARNINGS.md` Rules 1, 15, 23, 26 — `55 chars ≤ 70`, `0` exact collisions):** `How Do Cats Land on Their Feet? (The 1894 Camera Twist)`
- **Title A1 (Compact `Rule 15` `≤50 chars` Variant — `50 chars`, `0` exact collisions):** `How Do Cats Land on Their Feet? (1894 Photo Proof)`
- **Title B (Test & Compare Arm 2, `Rule 23` — `50 chars`, `0` exact collisions):** `The 60-Photo Gun That Solved How Falling Cats Flip`
- **Title B1 (Chronophotographic Camera Precision Variant — `49 chars ≤ 50`, `0` exact collisions):** `The 1894 Camera That Solved How Falling Cats Flip` *(use if primary sources in `SOURCES.md` distinguish Marey's 1894 `60-fps` moving-film chronophotographic camera from his 1882 `12-fps` photographic gun)*
- **Title C (`Rule 26` Exact Phrase First — `59 chars ≤ 70`, `0` exact collisions):** `How Do Cats Land on Their Feet? The Zero-Spin Physics Twist`
- **One-Line Hook:** In 1894, physicists swore a falling cat could never flip upright in mid-air without pushing off something — until a French physiologist pointed a 60-frames-per-second chronophotographic camera at a falling cat and uncovered a zero-spin geometry trick that NASA later taught Apollo astronauts.
- **Why It Should Work (Past Winners & `LEARNINGS.md` Rules):**
  - Resembles top HOS longs **`002` Periodic Table (`AL_-qlWko_g`, `161` views, `2.68/d`, `1,160` impressions, `3.36%` CTR)** and **`004` Inside an Atom (`GHZDsiH7L7A`, `34` views, `1.06/d`, `837` impressions)** by starting verbatim with an everyday physics/biology search phrase (`How Do Cats Land on Their Feet?`) backed by a `6`-video `≥1M` `TED-Ed` / `SmarterEveryDay` / `minutephysics` neighbour pool (`Rules 1, 15, 26`), while anchoring the narrative on a single famous historical apparatus (`Marey's 1894 chronophotographic camera`) like **`006` Willow Tree (`VbPubYd6Fbs`, `53.96%` Studio / `79%` 28d YTA avg view %)**.
  - Resembles top HOS Shorts **`29bpGAI0wb8` (*What happens if you keep cutting gold in half?*, `1,227` views, `39.58/d`)**, **`pWySvZsneZg` (*Why Gold Foil Bounced Rutherford's Particles Back*, `137` views, `112.43%` LOOP)**, and **`-3L6HzJ_d_4` (*What Is the Pasteur Swan Neck Flask Experiment?*, `129` views, `77.14%` stayed PASS, `75.23%` avg view % PASS)** by opening at Frame 0 on an unmistakable moving physical paradox — an upside-down cat twisting its front and rear halves in opposite directions in mid-air (`Rules 2, 8, 24, 27, 28, 30, 32`).
- **3-Way Thumbnail Test & Compare Plan (`LEARNINGS.md` Rules 11, 12, 14 + `THUMBNAIL_AND_TITLE_RULES.md` §2.1–2.B):**
  - **Thumb A (Hero Object — The Mid-Flip Cat & Brass Chronophotographic Camera):** Painted 3D house-style key art: a ginger-and-white cat suspended mid-flip on the right two-thirds with its front paws tucked tight and hind legs extended wide (clean hero subject, zero diagram clutter over the cat); the Explorer small at lower left aiming Marey's brass chronophotographic camera; cream/gold serif text on the clear left band: **`NO PUSH-OFF`** (`2 words`, gold on `NO`, zero word overlap with Titles A, A1, B, B1, or C).
  - **Thumb B (`Rule 14` Bright High-Contrast Variant — 1894 Paris Sequence Strip):** Bright sunlit courtyard key art: three sequential glowing stroboscopic poses of the falling cat turning from upside-down to four-paws-down over a soft cushion on the right; Explorer small at lower left holding a glass photographic plate; serif text on the left band: **`19 FRAMES`** (`2 words`, gold on `19`, zero word overlap with Titles A, A1, B, B1, or C).
  - **Thumb C (Cat vs Apollo Astronaut in Zero Gravity):** Painted 3D split comparison key art on the right showing a twisting cat above and an Apollo astronaut in a white spacesuit executing the exact same waist-bend turn in weightless space below; Explorer small at lower left; serif text on the left band: **`NASA COPIED IT`** (`3 words`, gold on `NASA`, zero word overlap with Titles A, A1, B, B1, or C).
- **Signed-out YouTube Autocomplete (`2026-11-16`):**
  - `"how do cats land on their feet"` → **`autocomplete = yes`** (`how do cats land on their feet`, `how can cats land on their feet`, `how does a cat land on its feet`, `how cats land on their feet physics`, `do cats always land on their feet planet dolan`)
  - `"why do cats always land on their feet"` → **`autocomplete = yes`** (`why do cats always land on their feet`, `do cats always land on their feet planet dolan`, `why cats always land on their feet`)
  - `"why a cat always lands on its feet"` → **`autocomplete = yes`** (`why a cat always lands on its feet`, `do cats always land on their feet`, `why do cats always land on their feet`, `do cats always land on their feet planet dolan`)
- **Rule 26(a) Two Ranking Videos (`≥10,000` views, retrieved `2026-11-16`):**
  1. `SmarterEveryDay` — [`RtWbpyjJqrU`](https://youtu.be/RtWbpyjJqrU) *Slow Motion Flipping Cat Physics | Smarter Every Day 58* (**`11,253,700` views**)
  2. `Vox` — [`Xs87FijgVaA`](https://youtu.be/Xs87FijgVaA) *Why a cat always lands on its feet* (**`2,534,162` views**; plus `AIRBOYD` [`O9XtK6R1QAk`](https://youtu.be/O9XtK6R1QAk) **`3,483,146` views**, `Insider Science` [`0m5CtIknAg4`](https://youtu.be/0m5CtIknAg4) **`1,944,696` views**, `BBC` [`sepYP_knGWc`](https://youtu.be/sepYP_knGWc) **`442,041` views**, `Explore & Discover` [`qjf472A83N8`](https://youtu.be/qjf472A83N8) **`198,955` views**, and `The Telegraph` [`0u26gpLmKe4`](https://youtu.be/0u26gpLmKe4) **`171,040` views**)
- **Neighbour Gate (`neighbours.py`):** **PASS (`6` education videos `≥1,000,000` views, `TED-Ed/TED: yes`)** — saved in [`11_Upload-Package/evidence_2026-11-16_neighbours.json`](11_Upload-Package/evidence_2026-11-16_neighbours.json):
  1. `TED-Ed` ★ — [`sI8NsYIyQ2A`](https://youtu.be/sI8NsYIyQ2A) *Why do cats act so weird? - Tony Buffington* (**`13,421,747` views**)
  2. `SmarterEveryDay` — [`RtWbpyjJqrU`](https://youtu.be/RtWbpyjJqrU) *Slow Motion Flipping Cat Physics | Smarter Every Day 58* (**`11,253,700` views**)
  3. `TED-Ed` ★ — [`Jsj-hDW9bS8`](https://youtu.be/Jsj-hDW9bS8) *The history of the world according to cats - Eva-Maria Geigl* (**`10,537,826` views**)
  4. `TED-Ed` ★ — [`jdrNjHPYKz4`](https://youtu.be/jdrNjHPYKz4) *Why do cats have vertical pupils? - Emma Bryce* (**`4,609,915` views**)
  5. `TED-Ed` ★ — [`l5VgOdgptRg`](https://youtu.be/l5VgOdgptRg) *The physics of the "hardest move" in ballet - Arleen Sugano* (**`2,600,485` views**)
  6. `minutephysics` — [`iWSu6U0Ujs8`](https://youtu.be/iWSu6U0Ujs8) *What IS Angular Momentum?* (**`1,865,351` views**)

---

## 4. Candidate 4-Act Discovery Outline (All Claims UNVERIFIED Pending `SOURCES.md` & `facts` Lane)

- **Cold Open (0:00–0:45, UNVERIFIED):** Drop a rigid weight upside-down with zero spin, and Newton's laws say it cannot rotate in mid-air without pushing off something (`0:00–0:05`: a brass cylinder dropped upside-down falls straight without turning). At `0:05–0:15` (visual proof-first hook), cut directly to Étienne-Jules Marey's **22 October 1894** high-speed chronophotographic sequence on the table of the Paris Academy of Sciences: `19` consecutive exposures shot at `60 frames per second` showing a white cat flipping `180 degrees` in less than one-fifth of a second (`~0.12–0.20 s`) with zero push-off.
- **Act I — Maxwell's Cambridge Cat Drops & The Conservation of Angular Momentum Paradox (1850–1894, UNVERIFIED):** In the **1850s–1870s**, physicist James Clerk Maxwell (alongside George Gabriel Stokes) was famous at Trinity College, Cambridge, for gently dropping cats onto cushions and beds from smaller and smaller heights to find the speed limit of the cat-righting reflex. Yet 19th-century classical mechanics insisted on a strict theorem: a body released from rest with **zero net angular momentum (`L = 0`)** cannot rotate itself in mid-air unless an external torque acts on it — so mathematicians insisted the cat *must* be kicking off the dropper's hands at the instant of release.
  - **Primary-Source Guardrail (`SOURCES.md` & `facts` lane):** Verify the exact wording and drop-height figure (`~2 inches` vs `2 feet`) in Maxwell's 1870 letter to his wife Katherine Mary Dewar (reproduced in Lewis Campbell & William Garnett, *The Life of James Clerk Maxwell*, 1882) before citing a specific inch/foot threshold in the script.
- **Act II — Étienne-Jules Marey's 1894 Chronophotographic Camera Proof (October 1894, UNVERIFIED):** Using his custom **chronophotographic camera** shooting **`60` exposures per second** on a moving film strip at the Station Physiologique in Paris (**22 October 1894**, *Comptes Rendus de l'Académie des Sciences* 119:714–717, and **22 November 1894**, *Nature* 51:80–81), Étienne-Jules Marey photographed a falling cat from the side and from the end. The opening frames proved the cat left the hands completely upside-down with **zero initial spin** — and revealed the mechanism Marey proposed: first, the cat tucks its front legs tight against its chest (shrinking its front moment of inertia, like a spinning figure skater pulling in her arms) while stretching its rear legs wide, so its front half twists sharply upright while its wide rear half barely counter-rotates; second, it extends its front legs and tucks its rear legs to bring the back half around.
  - **Primary-Source Guardrail (`SOURCES.md` & `facts` lane):** Distinguish Marey's **1882 rotating-glass-plate photographic gun (`fusil photographique`, `12 fps`)** used on flying birds from his **1894 moving-film chronophotographic camera (`chronophotographe à pellicule mobile`, `60 fps`)** used on the falling cat (*Comptes Rendus* 119:714–717). Verify the exact frame count per strip (`14` vs `19` exposures) and drop height (`~1.2 m`) directly from Marey's 1894 paper, and use `Title B1` (*The 1894 Camera That Solved How Falling Cats Flip*) if primary sources reserve "photographic gun" strictly for the 1882 `12-fps` instrument.
- **Act III — Lévy, Guyou, Peano & Rademaker's Bend-and-Twist Non-Rigid Solution (1894–1935, UNVERIFIED):** In the very same and following sessions of the Paris Academy (**22 & 29 October 1894**, *Comptes Rendus* 119:717–721), mathematicians Maurice Lévy and Émile Guyou, followed by Giuseppe Peano (`1895`, *Rivista di Matematica* 5:74–78), proved mathematically that a deformable body can rotate `180°` while total angular momentum stays **strictly zero (`L = 0`)** at every millisecond of the fall. Then in **1935**, Dutch physiologists **G. G. J. Rademaker and J. W. G. ter Braak** (*Acta Oto-Laryngologica* 23:313–343) showed both the sensory trigger (the inner ear's **vestibular otolith organs** detecting gravity) and a deeper mechanical insight: rather than relying mainly on figure-skater paw tucking, the cat **bends its flexible spine at the waist (`knick-und-dreh`)** into two tilted cylinders and sweeps that bend around like a conical hula-hoop so both halves rotate the same way while their local axial spins cancel to `L = 0`.
  - **Primary-Source Guardrail (`SOURCES.md` & `facts` lane):** Verify the exact distinction between Marey/Guyou/Peano's variable-inertia "tuck-and-turn" (`1894–1895`) and Rademaker & ter Braak's "bend-and-twist" (`1935`) in `SOURCES.md`.
- **Act IV — Thomas Kane's 1969 NASA Equations & Apollo Astronauts in Zero Gravity (1968–1969, UNVERIFIED):** In **1968–1969**, Stanford dynamicists **Thomas R. Kane and M. P. Scher** (*International Journal of Solids and Structures* 5(7):663–670, 1969; NASA Contractor Report `NASA CR-1271` / NASA grant `NGR 05-020-209`) formulated the exact differential equations of the falling cat as a two-cylinder bent-spine dynamical system (and in `1993`, mathematician **Richard Montgomery** proved in *Communications in Mathematical Physics* 155:215–245 that Kane's bend-and-twist is the mathematically optimal geodesic path in gauge theory) — training spacesuited astronauts on trampolines at Stanford/NASA to turn their bodies in weightless space without firing a single thruster jet.
  - **Primary-Source Guardrail (`SOURCES.md` & `facts` lane):** Verify Kane & Scher's (1969) exact two-cylinder **no-twist bent-spine condition**, the exact NASA grant/report numbers (`NGR 05-020-209` / `NASA CR-1271`), and the trampoline gymnast/astronaut experiments before locking Act IV or Short `S02`.

---

## 5. Two Candidate Search-Titled Shorts (`Test B` / `Rule 26` / `Rule 32` — UNVERIFIED Concepts Only)

- **Short `S01`:** *How Can a Falling Cat Flip With Zero Push?* (`42 chars`, `0` exact collisions, positive search question)
  - **First-line answer hook (`0.0–1.5 s` titled noun + action, UNVERIFIED):** *"A falling cat flips upright in mid-air with zero push-off — and in 1894, a 60-photo-per-second camera finally caught how."*
  - **Frame-0 & Payoff Plan (`Rules 2, 3, 6, 24, 27`):** Frame 0 (`0.0s`, `mode: "cover"`, `0%` Explorer, `0%` bars): close moving shot of an upside-down cat mid-air twisting its tucked front paws one way while its stretched hind legs counter-rotate; Frame-0 caption **`19 HIGH-SPEED FRAMES`** (`3 words`, `#FFE000` on `19`, inside 16:9 centre band, zero word overlap with `S01` title). Single mid-Short overlay: `PARIS, 1894` (`WHEN` stamp inside 16:9 band, clear of `0–2s` and `9–14s` title card). Payoff at `≥70%` runtime (`~17.0s / 23.5s`): Étienne-Jules Marey's 1894 high-speed chronophotographic strip proving the cat bends its spine and counter-rotates its front and rear halves so total angular momentum stays strictly zero (`L = 0`) throughout the flip. Loop tail `<1.0s`, zero CTA.
- **Short `S02`:** *Why Did NASA Study Falling Cats for Apollo Astronauts?* (`54 chars`, `0` exact collisions, positive search question)
  - **First-line answer hook (`0.0–1.5 s` titled noun + action, UNVERIFIED):** *"NASA studied falling cats so Apollo astronauts could flip their bodies in weightless space without firing a single thruster."*
  - **Frame-0 & Payoff Plan (`Rules 2, 3, 6, 24, 27`):** Frame 0 (`0.0s`, `mode: "cover"`, `0%` Explorer, `0%` bars): close moving split-view of a floating astronaut in a white spacesuit and a falling cat executing the exact same waist-bend counter-twist; Frame-0 caption **`ZERO-GRAVITY FLIP`** (`2 words`, `#FFE000` on `ZERO-GRAVITY`, inside 16:9 centre band, zero word overlap with `S02` title). Single mid-Short overlay: `STANFORD, 1969` (`WHEN` stamp inside 16:9 band, clear of `0–2s` and `9–14s` title card). Payoff at `≥70%` runtime (`~17.2s / 23.5s`): Stanford's Thomas Kane and M. P. Scher (`1969`) turning Marey's 1894 falling-cat camera strip into exact two-cylinder equations that taught astronauts on NASA trampolines to rotate in weightless space with zero propellant. Loop tail `<1.0s`, zero CTA.
