# Topic Brief — `112_Provine-Gallup-Why-Do-We-Yawn` (`HOS:112` Proposal)

> **PROPOSAL & RULE-E / RULE G STATUS (`J2935` / `J2936`, `2026-11-16`):**
> - **Rule-E Topic Review Verdict (`J2936`):** **GO (`95.5 / 100` · `9.55 / 10` Opportunity Score) — Pre-cleared in `jobs/WIP.json` `next_hos` under Rule G** (`active` has 4/4 HOS films: `008`, `009`, `010`, `013`). Nothing is started in production (`status.json` stages are all `todo`).
> - **NOT CLEARED FOR SCRIPT LOCK, VO, OR PICTURE SPEND:** All historical and scientific claims in this brief are **UNVERIFIED** working notes. When an active HOS WIP slot opens under Rule G, every claim must be backed by verbatim primary-source quotes in `SOURCES.md` and verified through the `facts` lane (`gemini-agy`) before any script is locked or VO is recorded.

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
- Open topic PRs `#572`/`#576`/`#577` (`102` Ozone Hole, `103` Why Is the Sky Blue), `#581`/`#583` (`104` Speed of Light, `105` Venus Flytrap), `#588`/`#590`/`#592` (`106` Eels & Sargasso Sea, `107` Autumn Leaves & Chlorophyll), `#602`/`#603`/`#604` (`108` Why Is Ice Slippery, `109` Why Do Fingers Wrinkle in Water), `#607`/`#608`/`#609` (`110` Why Do Onions Make You Cry, `111` Why Do Knuckles Crack), and `#614` (`113` How Do Cats Land on Their Feet),
- All `011`–`097` backlog entries in `00_Brand/Channel-Setup/VIDEO_BACKLOG.json` and `00_Brand/Channel-Setup/ideas/` (`046` covers Berger, Kleitman & Aserinsky on EEG brainwaves and REM sleep; `074` covers Hooke, Lower & Bohr on lungs and oxygen transport; `084` covers Santorio, Wunderlich & Kluger on body temperature and fever; **none** cover why humans and vertebrates yawn, Robert Provine's 1987 $\text{CO}_2/\text{O}_2$ breathing-chamber experiment disproving the oxygen myth, or Andrew & Gordon Gallup's 2007–2010 forehead cold-pack and brain-thermoprobe experiments on cranial thermoregulation).
- **Result:** **Zero overlap.**

---

## 3. Packaging, Why It Should Work & Search/Neighbour Evidence (`Rule 26` + `neighbours.py` + `public_search.py`)

- **Title A (Primary Proposal, `LEARNINGS.md` Rules 1, 15, 23, 26 — `46 chars ≤ 50 chars`, `0` exact collisions):** `Why Do We Yawn? (The Brain-Cooling Experiment)`
- **Title B (Test & Compare Arm 2, `Rule 23` — `52 chars`, `0` exact collisions):** `The 1987 Gas Chamber That Proved Why You Really Yawn`
- **Title C (`Rule 26` Exact Phrase First — `55 chars`, `0` exact collisions):** `Why Do We Yawn? How a Cold Pack Broke a 2,000-Year Myth`
- **One-Line Hook:** For 2,000 years doctors taught that yawning pulls extra oxygen into tired lungs — until a 1987 gas-chamber test proved oxygen has zero effect on yawning and a 2007 forehead ice-pack experiment revealed your jaw is a radiator for an overheating brain.
- **Why It Should Work (Past Winners & `LEARNINGS.md` Rules):**
  - Resembles top HOS longs **`002` Periodic Table (`AL_-qlWko_g`, `161` views, `2.68/d`, `1,160` impressions, `3.36%` CTR)** and **`004` Inside an Atom (`GHZDsiH7L7A`, `34` views, `1.06/d`, `837` impressions)** by opening with an everyday universal search question (`Why Do We Yawn?`, `46 chars ≤ 50 chars` Rule 15 & Rule 26) backed by a `16`-video `≥1M` strictly on-topic `TED-Ed` / `TED` / `Vsauce` / `Be Smart` / `SciShow` neighbour pool (`Rules 1, 15, 26`), while pairing that search demand with a concrete laboratory apparatus story like **`006` Willow Tree (`VbPubYd6Fbs`, `53.96%` Studio / `79%` 28d YTA avg view %)** so it avoids the low-impression starvation of statement-titled `005` (`15` impressions) and `006` (`46` impressions).
  - Resembles top HOS Shorts **`29bpGAI0wb8` (*What happens if you keep cutting gold in half?*, `1,227` views, `39.58/d`)** and **`-3L6HzJ_d_4` (*What Is the Pasteur Swan Neck Flask Experiment?*, `129` views, `77.14%` stayed PASS, `75.23%` avg view % PASS)** by replacing statement titles like `Wvjd8g0CpzE` (`14.80%` stayed MISS) and `PFj6172YU4Q` (`15.98%` stayed MISS) with direct myth-busting search questions (`Rules 2, 8, 24, 27, 28, 30, 32`).
- **3-Way Thumbnail Test & Compare Plan (`LEARNINGS.md` Rules 11, 12, 14 + `THUMBNAIL_AND_TITLE_RULES.md` §2.1–2.B, zero in-scene AI text):**
  - **Thumb A (Hero Object — Thermal Brain Radiator):** Painted 3D house-style key art: a glowing thermal cutaway profile of a yawning head on the right two-thirds showing a red-hot brain cooling to icy blue as cool air rushes into the stretched jaw; the Explorer small at lower left holding a brass thermometer; cream/gold serif text on the clear left band: `HOT BRAIN` (`2 words`, gold on `HOT`, zero overlap on the head, no other AI text).
  - **Thumb B (`Rule 14` Bright High-Contrast Variant — The Forehead Cold Pack):** Bright sunlit laboratory key art: a volunteer watching a glowing screen with a frost-covered blue ice pack pressed to their forehead while their jaw stays calmly closed; Explorer small at lower left holding a brass stopwatch; serif text on the clear left band: `ICE PACK TEST` (`3 words`, gold on `ICE`, no in-scene counter text).
  - **Thumb C (The 1987 Oxygen Chamber Myth-Bust):** Painted 3D key art of Robert Provine's 1987 breathing mask connected by ribbed rubber tubing to two colour-coded brass gas cylinders with needle pressure gauges on the right, with the volunteer yawning wide right through the pure-oxygen mask; Explorer small at lower left; serif text on the clear left band: `NOT OXYGEN` (`2 words`, gold on `NOT`, no cylinder text labels).
- **Signed-out YouTube Autocomplete (`2026-11-16`, `11_Upload-Package/evidence_2026-11-16_public_search.json` & `evidence_2026-11-16_neighbours.json`):**
  - `"why do we yawn"` → **`autocomplete = yes`** (`why do we yawn`, `why do we yawn when someone else yawns`, `why do we yawn while praying`, `why do we yawn dr binocs`, `why do we yawn factoholic`, `why do we yawn when others yawn`, `why do we yawn ted ed`, `why do we yawn while studying`, `why do we yawn when tired`, `why do we yawn animation`)
  - `"why is yawning contagious"` → **`autocomplete = yes`** (`why is yawning contagious`, `why is yawning contagious ted ed`, `why is yawning so contagious`)
  - `"why do we yawn when someone else yawns"` → **`autocomplete = yes`** (`why do we yawn when someone else yawns`, `why do i yawn when someone else yawns`, `why you yawn when someone else yawns`)
  - `"why do we sleep"` & `"staying up all night"` (`neighbours.json`) → **`autocomplete = yes`** (`10` suggestions each)
- **Rule 26(a) Ranking Videos (`≥10,000` views, retrieved `2026-11-16`):**
  1. `Vsauce` — [`jGIbUK4nw00`](https://youtu.be/jGIbUK4nw00) *Why Is Yawning Contagious?* (**`4,827,757` views**)
  2. `AsapSCIENCE` — [`I0dQx4SNSwE`](https://youtu.be/I0dQx4SNSwE) *Why Do We Yawn?* (**`4,651,480` views**; plus `TED-Ed` [`4NpG4F9yq00`](https://youtu.be/4NpG4F9yq00) *Why is yawning contagious? - Claudia Aguirre* **`2,452,078` views**, `Smart Nonsense` [`KLwxaRtiJ7k`](https://youtu.be/KLwxaRtiJ7k) *Why is yawning contagious??* **`1,162,824` views**, `Peekaboo Kidz` [`0lsySXHa5l0`](https://youtu.be/0lsySXHa5l0) *Why Do We Yawn? | The Dr. Binocs Show | Best Learning Videos For Kids | Peekaboo Kidz* **`1,049,429` views**, `SciShow` [`ew_iZTPoC3c`](https://youtu.be/ew_iZTPoC3c) *Why Do We Yawn?* **`466,447` views**, `Today I Learned Science` [`mCHoseE8nJc`](https://youtu.be/mCHoseE8nJc) *Scientists Finally Cracked Why We Yawn* **`401,786` views**, and `SciShow Kids` [`3jmp5yF5rYM`](https://youtu.be/3jmp5yF5rYM) *Why Do We Yawn?* **`125,294` views**)
- **Neighbour Gate (`neighbours.py "why do we yawn" "why is yawning contagious" "why do we sleep" "staying up all night"`):** **PASS (`16` strictly on-topic education videos `≥1,000,000` views, `TED-Ed/TED: yes`, `0` off-topic rows)** — saved in [`11_Upload-Package/evidence_2026-11-16_neighbours.json`](11_Upload-Package/evidence_2026-11-16_neighbours.json):
  1. `TED` ★ — [`5MuIMqhT8DM`](https://youtu.be/5MuIMqhT8DM) *Sleep Is Your Superpower | Matt Walker | TED* (**`17,757,665` views**)
  2. `TED-Ed` ★ — [`dqONk48l5vY`](https://youtu.be/dqONk48l5vY) *What would happen if you didn't sleep? - Claudia Aguirre* (**`15,049,789` views**)
  3. `TED-Ed` ★ — [`gedoSfZvBgE`](https://youtu.be/gedoSfZvBgE) *The benefits of a good night's sleep - Shai Marcu* (**`7,504,218` views**)
  4. `TED-Ed` ★ — [`idrbwnWLJ7w`](https://youtu.be/idrbwnWLJ7w) *What staying up all night does to your brain - Anna Rothschild* (**`7,295,937` views**)
  5. `Vsauce` — [`jGIbUK4nw00`](https://youtu.be/jGIbUK4nw00) *Why Is Yawning Contagious?* (**`4,827,757` views**)
  6. `TED` ★ — [`fQUeDdaVoWo`](https://youtu.be/fQUeDdaVoWo) *Do You Really Need 8 Hours of Sleep Every Night? | Body Stuff with Dr. Jen Gunter | TED* (**`4,613,307` views**)
  7. `Be Smart` — [`3mufsteNrTI`](https://youtu.be/3mufsteNrTI) *Why Do We Have To Sleep?* (**`3,394,475` views**)
  8. `TED` ★ — [`LWULB9Aoopc`](https://youtu.be/LWULB9Aoopc) *Why do we sleep? | Russell Foster* (**`2,926,207` views**)
  9. `TED` ★ — [`t0kACis_dJE`](https://youtu.be/t0kACis_dJE) *6 tips for better sleep | Sleeping with Science, a TED series* (**`2,893,340` views**)
  10. `TED-Ed` ★ — [`Amkg1cdDCpM`](https://youtu.be/Amkg1cdDCpM) *Can you change your sleep schedule?* (**`2,713,053` views**)
  11. `TED-Ed` ★ — [`4NpG4F9yq00`](https://youtu.be/4NpG4F9yq00) *Why is yawning contagious? - Claudia Aguirre* (**`2,452,078` views**)
  12. `TED` ★ — [`1U2qMRGihGg`](https://youtu.be/1U2qMRGihGg) *The brain benefits of deep sleep -- and how to get more of it | Dan Gartenberg* (**`2,272,907` views**)
  13. `SciShow` — [`pwNMvUXTgDY`](https://youtu.be/pwNMvUXTgDY) *Sleep: Why We Need It and What Happens Without It* (**`2,272,025` views**)
  14. `TED-Ed` ★ — [`_GI9-J-sE5k`](https://youtu.be/_GI9-J-sE5k) *What's the best position to sleep in? - Rachel Marie E. Salas* (**`2,225,329` views**)
  15. `TED-Ed` ★ — [`WJhCa12UTsg`](https://youtu.be/WJhCa12UTsg) *What lack of sleep does to the teenage brain - Wendy Troxel* (**`2,092,313` views**)
  16. `TED` ★ — [`MJK-dMlATmM`](https://youtu.be/MJK-dMlATmM) *One more reason to get a good night's sleep | Jeff Iliff* (**`1,746,469` views**)

---

## 4. Candidate 4-Act Discovery Outline (All Claims UNVERIFIED Pending `SOURCES.md` & `facts` Lane)

- **Cold Open (0:00–0:45, UNVERIFIED):** Right now, just reading the word *yawn* is trying to force your jaw wide open (`0:00–0:05`: close moving cutaway of a jaw stretching wide inside a glass breathing mask, cutting at `0:05–0:15` to a glowing thermal brain map cooled by a forehead cold pack — zero exterior establishing shot, zero *"In this film..."* agenda line). For 2,000 years, doctors taught that you yawn because your blood is low on oxygen — until a 1987 gas-chamber experiment proved pure oxygen doesn't stop a single yawn, and a 2007 ice-pack experiment revealed your jaw is actually a radiator for an overheating brain.
- **Act I — Hippocrates' *De Flatibus* ("Bad Air") & The 2,000-Year Oxygen Myth (~400 BC–1986, UNVERIFIED):** From Hippocrates' treatise *De flatibus* (*On Breaths* / *On Winds*, `~400 BC`, §8, claiming yawning before a fever vents hot accumulated air like steam from a cauldron) to 18th–20th-century respiratory physiology textbooks (following Johannes de Gorter `1744` and post-Lavoisier blood-gas medicine), doctors assumed yawning is a respiratory reflex triggered when blood carbon dioxide ($\text{CO}_2$) rises and oxygen ($\text{O}_2$) falls in a stuffy room.
  - *Primary-source verification guardrail (`SOURCES.md` + `facts` lane):* Verify the exact translation of Hippocrates *De flatibus* §8 and distinguish Hippocrates' "expelling hot/bad air" from the modern post-Lavoisier hypoxia/hypercapnia ($\text{O}_2/\text{CO}_2$) textbook hypothesis.
- **Act II — Robert Provine's 1986–1987 Gas-Chamber & Exercise Experiments (1986–1987, UNVERIFIED):** After quantifying the human yawn as a stereotyped `~6-second` (`5.9 s`) motor pattern and proving that merely reading about or viewing a yawn triggers contagious yawning in `~55%` of subjects (**Robert R. Provine**, `1986`, *Ethology* 72(2): 109–122), neuroscientist **Robert R. Provine**, **B. C. Tate**, and **L. L. Geldmacher** (`1987`, *Bulletin of the Psychonomic Society* 25(6): 458–460) at the University of Maryland Baltimore County put student volunteers inside breathing masks fed by compressed gas mixtures: compressed normal air (`20.95%` $\text{O}_2$, `0.03%` $\text{CO}_2$), `3%` or `5%` $\text{CO}_2$ (`100×–166×` normal atmospheric $\text{CO}_2$, with `21%` $\text{O}_2$), or `100%` pure medical $\text{O}_2$. Breathing rates rose dramatically under `3%–5%` $\text{CO}_2$ — **yet yawning frequency did not change at all**, and vigorous exercise that doubled breathing rates didn't alter yawning either, demolishing the oxygen hypothesis (`DATA #1 + SCALE: 100×–166× atmospheric CO₂ & 100% O₂ → 0 statistically significant change in yawning rate`).
  - *Primary-source verification guardrail (`SOURCES.md` + `facts` lane):* Verify exact gas percentages, sample sizes, breathing-rate numbers, and exercise protocol directly from Provine, Tate & Geldmacher (`1987`), *Bull. Psychon. Soc.* 25(6): 458–460.
- **Act III — Andrew & Gordon Gallup's 2007 Nasal-Breathing & Forehead Cold-Pack Experiments (2007, UNVERIFIED):** Why, then, does a yawn require a `~6-second` maximal jaw stretch alongside a deep inhalation? In **May 2007** (*Evolutionary Psychology* 5(1): 92–101), **Andrew C. Gallup** and **Gordon G. Gallup Jr.** at SUNY Albany propose the **cranial thermoregulation (brain-cooling) hypothesis**: stretching the jaw flexes the pterygoid venous plexus around the thin sinus walls while cool inhaled air cools venous blood returning to the skull. They run two back-to-back experiments on volunteers watching contagious-yawning videos: in **Experiment 1**, `48%` of oral/normal breathers yawn vs **`0%`** of exclusively nasal breathers (because nasal breathing already cools blood in the nasal cavity); in **Experiment 2**, holding a **warm (`46°C` / `115°F`) or room-temperature pack** to the forehead produces **`41%`** contagious yawning, whereas holding a **cold pack (`4°C` / `40°F`)** to the forehead drops contagious yawning to **`9%`** (`DATA #2 + SCALE: 48% → 0% with nasal breathing; 41% → 9% with a 4°C forehead cold pack`).
  - *Primary-source verification guardrail (`SOURCES.md` + `facts` lane):* Keep Experiment 1 (`48%` oral vs `0%` nasal breathing) and Experiment 2 (`41%` warm/room-temp pack vs `9%` cold pack at `4°C`) explicitly distinct and verify exact group sizes and percentages from Gallup & Gallup (`2007`), *Evolutionary Psychology* 5(1): 92–101.
- **Act IV — Cortical Thermoprobes & the `20°C` Thermal Window (2010–2014, UNVERIFIED):** In **2010** (*Frontiers in Evolutionary Neuroscience* 2: 108), **Michael L. Shoup-Knox**, **Andrew C. Gallup**, **Gordon G. Gallup Jr.**, and **Ewan C. McNay** implant micro-thermoprobes directly into the prelimbic frontal cortex of freely moving rats and record cortical temperature rising **`~0.10–0.15°C` (`+0.11°C` above baseline `37.47°C` to `~37.58°C`)** in the three minutes before a yawn — then dropping back to baseline within three minutes after the yawn finishes (`DATA #3 + SCALE: +0.11°C pre-yawn cortical spike cooled back to 37.47°C baseline in 3 minutes`). Field studies in **Tucson, Arizona** (**Gallup & Eldakar**, `2011`, *Front. Evol. Neurosci.* 3: 3; `45%` winter vs `24%` in `37°C` summer heat) and **Vienna, Austria** (**Massen, Dusch, Eldakar & Gallup**, `2014`, *Physiology & Behavior* 130: 145–148; `41.7%` summer vs `18.3%` in `1.4°C` winter cold) confirm the **"thermal window" hypothesis** (`~20°C` optimal ambient air), explaining contagious yawning as a group-vigilance reflex that cools the brains of an entire troop at once.

---

## 5. Two Candidate Search-Titled Shorts (`Test B` / `Rule 26` / `Rule 32` — UNVERIFIED Concepts Only)

- **Short `S01`:** *Does Yawning Actually Give You More Oxygen?* (`43 chars`, `0` exact collisions, positive search question)
  - **First-line anomaly hook (`≤1.5 s` surprise, `Rule 2` & `Rule 6`, UNVERIFIED):** *"Breathing pure oxygen inside a sealed mask doesn't stop a single yawn — even though doctors taught the oxygen myth for two thousand years."* (Titled words `oxygen` and `yawn` + surprise `doesn't stop` land in words 1–12 without giving away the brain-cooling answer in sentence 1.)
  - **Frame-0, Overlay & Payoff Plan (`Rules 2, 3, 6, 24, 27` + `Teach on screen`):** Frame 0 (`0.0s`, `mode: "cover"`, `0%` Explorer, `0%` bars): close moving shot of a volunteer yawning wide inside a clear glass breathing mask connected by ribbed tubing to a brass oxygen regulator (`NOT OXYGEN`, `#FFE000` on `NOT`). Single mid-Short `Teach on screen` overlay in the 16:9 centre band at `~16.8s` (clear of `0–2s` and the `9–14s` promo title): `0% YAWN CHANGE` (`3 words`). Payoff at `≥70%` runtime (`~17.0s / 23.5s`): Robert Provine's 1987 discovery that neither `100%` oxygen nor `100×` carbon dioxide changes yawning, because stretching the jaw cools an overheating brain. Loop tail `<1.0s`, zero CTA.
- **Short `S02`:** *Why Does a Cold Pack on Your Forehead Stop Yawning?* (`51 chars`, `0` exact collisions, positive search question)
  - **First-line anomaly hook (`≤1.5 s` surprise, `Rule 2` & `Rule 6`, UNVERIFIED):** *"Pressing a cold pack against your forehead switches off contagious yawning in seconds — while a warm pack leaves you yawning at the screen."* (Titled words `cold pack`, `forehead`, and `yawning` + surprise `switches off` land in sentence 1 while withholding the cranial-radiator mechanism until `≥70%` runtime.)
  - **Frame-0, Overlay & Payoff Plan (`Rules 2, 3, 6, 24, 27` + `Teach on screen`):** Frame 0 (`0.0s`, `mode: "cover"`, `0%` Explorer, `0%` bars): close moving thermal cutaway of a glowing red forehead cooling to icy blue as a frost-covered cold pack touches the brow (`BRAIN COOLER`, `#FFE000` on `COOLER`). Single mid-Short `Teach on screen` overlay in the 16:9 centre band at `~17.0s`: `41% DOWN TO 9%` (`4 words`). Payoff at `≥70%` runtime (`~17.2s / 23.5s`): Andrew Gallup's 2007 experiment showing a `4°C` forehead cold pack drops contagious yawning from `41%` to `9%` because your jaw is actually a radiator that cools venous blood returning to an overheating brain. Loop tail `<1.0s`, zero CTA.
