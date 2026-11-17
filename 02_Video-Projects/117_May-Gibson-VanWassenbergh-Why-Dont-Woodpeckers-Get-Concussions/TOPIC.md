# Topic Brief — `117_May-Gibson-VanWassenbergh-Why-Dont-Woodpeckers-Get-Concussions` (`HOS:117` Proposal)

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
- Open topic PRs `#572` (`102` Ozone Hole, `103` Why Is the Sky Blue), `#581` (`104` Speed of Light, `105` Venus Flytrap), `#588` (`106` Eels & Sargasso Sea, `107` Autumn Leaves & Chlorophyll), `#602` (`108` Why Is Ice Slippery, `109` Why Do Fingers Wrinkle in Water), `#607` (`110` Why Do Onions Make You Cry, `111` Why Do Knuckles Crack), `#614` (`112` Why Do We Yawn, `113` How Do Cats Land on Their Feet), `#618` (`114` How Do Chameleons Change Colour, `115` Why Do Zebras Have Stripes), and companion proposal `116` (Why Do We Get Goosebumps),
- All `011`–`095` backlog entries in `00_Brand/Channel-Setup/VIDEO_BACKLOG.json` and `00_Brand/Channel-Setup/ideas/` (`078` covers Broca, Wernicke, Penfield & Sperry on split-brain neuroscience; `079` covers Belchier, Duhamel, Kölliker, Wolff & Mellanby on bone growth and rickets; `100` covers migrating birds' cryptochrome magnetic compass; **none** cover why woodpeckers don't get concussions, Philip May & Jaroslav Hrdlicka's 1976–1979 high-speed `1,200 g` woodpecker cinematography, the 45-year spongy-bone shock-absorber myth, or Sam Van Wassenbergh's July 2022 *Current Biology* discovery that woodpecker skulls act as rigid hammers and survive via brain-size scaling).
- **Result:** **Zero overlap.**

---

## 3. Packaging, Why It Should Work & Search/Neighbour Evidence (`Rule 26` + `neighbours.py` + `public_search.py`)

- **Title A (Primary Proposal, `LEARNINGS.md` Rules 1, 15, 23, 26 — `59 chars`, `0` exact collisions):** `Why Don't Woodpeckers Get Concussions? (The Shock-Pad Myth)`
- **Title B (Test & Compare Arm 2, `Rule 23` — `57 chars`, `0` exact collisions):** `Woodpecker Skulls Have No Shock Absorber (The 2022 Proof)`
- **Title C (`Rule 26` Exact Phrase First — `57 chars`, `0` exact collisions):** `Why Don't Woodpeckers Get Concussions? The 1,200g Mystery`
- **One-Line Hook:** A woodpecker slams its beak into solid oak 20 times a second at 1,200 times the force of gravity, and for 45 years engineers copied its spongy skull bone as a "natural shock absorber" — until a 2022 high-speed video experiment proved a shock absorber would actually cripple the bird, and revealed the real physics keeping its brain safe.
- **Why It Should Work (Past Winners & `LEARNINGS.md` Rules):**
  - Resembles top HOS longs **`002` Periodic Table (`AL_-qlWko_g`, `161` views, `2.68/d`, `1,160` impressions, `3.36%` CTR)** and **`004` Inside an Atom (`GHZDsiH7L7A`, `34` views, `1.06/d`, `837` impressions)** by opening with an exact, high-volume everyday question (`Why Don't Woodpeckers Get Concussions?`) backed by `4` education neighbours `≥1M` views (`Rules 1, 15, 26`), while pairing that search demand with an immediate physical-apparatus twist like **`006` Willow Tree (`VbPubYd6Fbs`, `53.96%` Studio / `79%` 28d YTA avg view %)** and **`007` First Vaccine (`ETynHpIYLeY`, `7.41%` CTR)** so it avoids the low-impression starvation of statement-titled `005` (`15` impressions).
  - Resembles top HOS Shorts **`29bpGAI0wb8` (*What happens if you keep cutting gold in half?*, `1,227` views, `39.58/d`)**, **`pWySvZsneZg` (*Why Gold Foil Bounced Rutherford's Particles Back*, `137` views, `112.43%` avg view % LOOP)**, and **`-3L6HzJ_d_4` (*What Is the Pasteur Swan Neck Flask Experiment?*, `129` views, `77.14%` stayed PASS, `75.23%` avg view % PASS)** by combining an extreme number (`1,200 g`, `17×` what gives a human a concussion) with a textbook myth-bust at `≥70%` runtime (`Rules 2, 6, 8, 24, 27, 28, 30, 32`).
- **3-Way Thumbnail Test & Compare Plan (`LEARNINGS.md` Rules 11, 12, 14 + `THUMBNAIL_AND_TITLE_RULES.md` §2.1–2.B):**
  - **Thumb A (Hero Object — The Cutaway Woodpecker Skull & Tongue):** Painted 3D house-style key art: a giant side-profile X-ray cutaway of a woodpecker mid-strike against oak bark on the right two-thirds, showing the long red hyoid tongue bone wrapping all the way around the back of its skull and its compact brain glowing inside; the Explorer small at lower left; cream/gold serif text on the clear left band: `1,200 G IMPACT` (`3 words`, gold on `1,200 G`, zero overlap on the bird).
  - **Thumb B (`Rule 14` Bright High-Contrast Variant — Hammer vs Sponge Myth-Bust):** Bright sunlit laboratory bench key art comparing a rigid steel hammer driving into wood beside a springy foam-padded hammer bouncing uselessly back, with a woodpecker skull cutaway above; Explorer small at lower left; serif text on the left band: `NO SHOCK PAD` (`3 words`, gold on `NO`).
  - **Thumb C (Human Helmet vs Tiny Bird Brain Scale):** Painted 3D key art contrasting a cracked human crash helmet at `70 g` beside an unharmed woodpecker striking oak at `1,200 g`; Explorer small at lower left; serif text on the left band: `17× HUMAN LIMIT` (`3 words`, gold on `17×`).
- **Signed-out YouTube Autocomplete (`2026-11-16`):**
  - `"why don't woodpeckers get concussions"` → **`autocomplete = yes`**
  - `"how do woodpeckers not get brain damage"` → **`autocomplete = yes`**
  - `"woodpecker tongue around brain"` → **`autocomplete = yes`**
- **Rule 26(a) Two Ranking Videos (`≥10,000` views, retrieved `2026-11-16`):**
  1. `Be Smart` — [`bqBxbMWd8O0`](https://youtu.be/bqBxbMWd8O0) *Why Don’t Woodpeckers Get Concussions?* (**`1,906,077` views**)
  2. `Nature Lens` — [`aN5s3KV95wY`](https://youtu.be/aN5s3KV95wY) *Why Don't Woodpeckers Get Concussions?* (**`666,803` views**; plus `SciShow Kids` [`tJizlKZizps`](https://youtu.be/tJizlKZizps) **`263,813` views**, `SciShow` [`Mgd-xdhjrAc`](https://youtu.be/Mgd-xdhjrAc) **`164,025` views**, `Wim Spronk` [`xRS_4OgP7-w`](https://youtu.be/xRS_4OgP7-w) **`81,258` views**, `Danny's Dose` [`6MtJd8pgQq0`](https://youtu.be/6MtJd8pgQq0) **`52,323` views**, and `Natural History Museum` [`kYMAKChBMj8`](https://youtu.be/kYMAKChBMj8) **`39,824` views**)
- **Neighbour Gate (`neighbours.py`):** **PASS (`4` education videos `≥1,000,000` views, `TED-Ed/TED: yes`)** — saved in [`11_Upload-Package/evidence_2026-11-16_neighbours.json`](11_Upload-Package/evidence_2026-11-16_neighbours.json):
  1. `TED-Ed` ★ — [`xvjK-4NXRsM`](https://youtu.be/xvjK-4NXRsM) *What happens when you have a concussion? - Clifford Robbins* (**`2,561,046` views**)
  2. `TED-Ed` ★ — [`hRzRjHzvOts`](https://youtu.be/hRzRjHzvOts) *Why can't some birds fly? - Gillian Gibb* (**`2,110,951` views**)
  3. `Be Smart` — [`bqBxbMWd8O0`](https://youtu.be/bqBxbMWd8O0) *Why Don’t Woodpeckers Get Concussions?* (**`1,906,076` views**)
  4. `TED` ★ — [`3VEkzweBJPM`](https://youtu.be/3VEkzweBJPM) *Birds Aren’t Real? How a Conspiracy Takes Flight | Peter McIndoe | TED* (**`1,369,748` views**; plus `TED-Ed` [`0EBFpj60LRY`](https://youtu.be/0EBFpj60LRY) *The real reason dodo birds went extinct* **`793,064` views**, `TED-Ed` [`r5_ZSnFDPRg`](https://youtu.be/r5_ZSnFDPRg) *The surprising reason birds sing* **`703,198` views**, `TEDx Talks` [`5nBqLwg2Eug`](https://youtu.be/5nBqLwg2Eug) *Brain concussion - Shake it and you break it | Steven Laureys* **`306,191` views**, `TED` [`druJDI6hiiY`](https://youtu.be/druJDI6hiiY) *Why helmets don't prevent concussions -- and what might | David Camarillo* **`305,325` views**, and `SciShow Kids` [`tJizlKZizps`](https://youtu.be/tJizlKZizps) *Why Don't Woodpeckers' Heads Hurt?* **`263,813` views**)

---

## 4. Candidate 4-Act Discovery Outline (All Claims UNVERIFIED Pending `SOURCES.md` & `facts` Lane)

- **Cold Open (0:00–0:45, UNVERIFIED):** A woodpecker slams its beak into solid oak 20 times a second, stopping dead from `7 metres per second` in half a millisecond — a deceleration of **`1,200 g`**, seventeen times the impact that gives a human a concussion. For 45 years textbooks claimed a spongy bone behind its beak acts like a built-in shock absorber — until a 2022 high-speed video test proved a shock absorber would actually ruin the bird's strike.
- **Act I — Philip May & Jaroslav Hrdlicka's 1976 High-Speed Camera (`1,200 g`) & the Spongy-Bone Hypothesis (1976–2011, UNVERIFIED):** In **1976** (*The Lancet*) and **1979** (*Archives of Neurology*), UCLA neurologist **Philip R. A. May** and filmmaker **Jaroslav Hrdlicka** filmed an acorn woodpecker (*Melanerpes formicivorus*) at **`2,000 frames per second`**. They measured impacts reaching **`1,200 g`** (compared with `~70–100 g` for human concussion), noted that the bird hammers in a straight line to avoid rotational whiplash, and sparked four decades of engineering studies (including **Lorna Gibson** in 2006 and **Yubo Fan & Ming Zhang** in 2011) proposing that the spongy hyoid bone wrapping around the skull and porous cranial bone act as mechanical **shock absorbers** to cushion the brain.
- **Act II — Why Would a Hammer Have a Cushion Inside It? Sam Van Wassenbergh's 2022 Paradox (2022, UNVERIFIED):** If you put a springy shock absorber inside a hammer, what happens when you hit a nail? The cushion absorbs the kinetic energy before the tip can drive into the wood! In **July 2022** (*Current Biology*), evolutionary biomechanist **Sam Van Wassenbergh** and colleagues at the University of Antwerp filmed three species of woodpeckers (*Dryocopus martius*, *Dryobates minor*, and *Dendrocopos major*) at **`4,000 frames per second`** while tracking microscopic markers on both the beak and the eye/braincase during more than 100 strikes.
- **Act III — The Rigid-Hammer Proof (2022, UNVERIFIED):** Van Wassenbergh's high-speed tracking revealed a surprise: during impact, the braincase decelerates at the **exact same rate** as the beak (`zero shock absorption` between beak and brain)! Even more striking, biomechanical models showed that if the spongy bone actually absorbed impact shock, the woodpecker would waste kinetic energy and have to hammer **harder** to reach the same depth in the tree — canceling out any protective benefit. The woodpecker's head isn't a shock-absorbing helmet; it is built as a **stiff, rigid hammer** to transfer maximum energy into the wood!
- **Act IV — Galileo's Scaling Law & Why Small Brains Don't Concuss (2022, UNVERIFIED):** If the skull absorbs zero shock, how does the woodpecker's brain survive `400–1,200 g`? Van Wassenbergh's team calculated the intracranial pressure inside the woodpecker's tiny skull (`~2 grams` brain mass vs `~1,400 grams` in humans). Because pressure scales with **brain length × deceleration** ($\Delta P \propto \rho \cdot a \cdot L$), a woodpecker's short, light brain experiences only **one-seventh the intracranial pressure** of a human brain at the same deceleration — meaning a woodpecker would have to hit a tree at **`~4,600 g`** (`twice as fast`, or `4×` the impact energy) just to reach the human concussion threshold, while its tight skull cavity with minimal cerebrospinal fluid prevents brain slosh!

---

## 5. Two Candidate Search-Titled Shorts (`Test B` / `Rule 26` / `Rule 32` — UNVERIFIED Concepts Only)

- **Short `S01`:** *How Do Woodpeckers Survive 1,200g Impacts?* (`42 chars`, `0` exact collisions, positive search question)
  - **First-line answer hook (UNVERIFIED):** *"A woodpecker slams its head into oak at 1,200 Gs — seventeen times the force that gives a human a concussion — with zero shock absorber."*
  - **Frame-0 & Payoff Plan (`Rules 2, 3, 6, 24, 27`):** Frame 0 (`0.0s`, `mode: "cover"`): extreme slow-motion close-up of a woodpecker beak striking oak bark as a glowing X-ray cutaway reveals its skull and brain (`1,200 G IMPACT`, `#FFE000` on `1,200 G`). Payoff at `≥70%` runtime (`~17.0s / 23.5s`): Sam Van Wassenbergh's 2022 high-speed camera proof that woodpecker skulls act as rigid hammers with zero shock absorption, and their brains survive because a tiny `2-gram` brain generates 7 times less pressure than a human brain. Loop tail `<1.0s`, zero CTA.
- **Short `S02`:** *Do Woodpecker Skulls Really Have Shock Absorbers?* (`49 chars`, `0` exact collisions, positive search question)
  - **First-line answer hook (UNVERIFIED):** *"You were taught woodpecker skulls have spongy shock absorbers to protect their brains — until a 2022 high-speed camera test proved the opposite."*
  - **Frame-0 & Payoff Plan (`Rules 2, 3, 6, 24, 27`):** Frame 0 (`0.0s`, `mode: "cover"`): split comparison of a foam-padded hammer bouncing off wood vs a woodpecker skull striking rigid and clean (`NO SHOCK PAD`, `#FFE000` on `NO`). Payoff at `≥70%` runtime (`~17.2s / 23.5s`): 4,000-fps tracking showed the braincase stops just as fast as the beak because any shock pad would waste hammering energy — instead, small brain size and a snug skull keep intracranial pressure well below concussion limits. Loop tail `<1.0s`, zero CTA.
