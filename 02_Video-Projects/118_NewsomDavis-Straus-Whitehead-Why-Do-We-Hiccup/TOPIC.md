# Topic Brief — `118_NewsomDavis-Straus-Whitehead-Why-Do-We-Hiccup` (`HOS:118` · Rule-E GO in `next_hos`)

> **RULE-E GO & RULE G STATUS (`J2970` / `J2971`, `2026-11-17`):**
> - **Rule-E Verdict:** **GO (`95.5 / 100` · `9.55 / 10` Opportunity Score)** — Pre-cleared in the History of Science backlog (`jobs/WIP.json` `next_hos`) under **Rule G** (`active` has `4 / 4` HOS films full: `008`, `009`, `010`, `013`). Nothing is started in production (`status.json` stages are all `todo`; `£0.00` spent).
> - **Awaits Active HOS Slot, `SOURCES.md` & `facts` Lane:** All historical and scientific claims in this brief are **UNVERIFIED** working notes. Before any script is locked, VO is recorded, or picture credit is spent, every claim must be backed by verbatim primary-source quotes in `SOURCES.md` and verified through the `facts` lane (`gemini-agy`).

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
- Open topic PRs `#572` (`102` Ozone Hole, `103` Why Is the Sky Blue), `#581` (`104` Speed of Light, `105` Venus Flytrap), `#588` (`106` Eels & Sargasso Sea, `107` Autumn Leaves & Chlorophyll), `#602` (`108` Why Is Ice Slippery, `109` Why Do Fingers Wrinkle in Water), `#607` (`110` Why Do Onions Make You Cry, `111` Why Do Knuckles Crack), `#614` (`112` Why Do We Yawn, `113` How Do Cats Land on Their Feet), `#618` (`114` How Do Chameleons Change Colour, `115` Why Do Zebras Have Stripes), `#625` / `#627` / `#628` (`116` Why Do We Get Goosebumps, `117` Why Don't Woodpeckers Get Concussions), and `#629` (`119` Why Do Mosquitoes Bite Some People More?),
- All `011`–`097` backlog entries in `00_Brand/Channel-Setup/VIDEO_BACKLOG.json` and `00_Brand/Channel-Setup/ideas/` (`074` covers Hooke, Lower, Bohr, Krogh, Avery & Perutz on alveolar gas exchange, haemoglobin oxygen binding, and neonatal lung surfactant; `112` covers Provine & Gallup on why we yawn; **none** cover why we hiccup, John Newsom Davis's 1970 Queen Square EMG/glottis-closure experiment, De Vries, Visser & Prechtl's 1982 fetal ultrasound study, Christian Straus & William Whitelaw's 2003 amphibian gill-ventilation CPG discovery, or Kimberley Whitehead & Lorenzo Fabrizi's 2019 UCL newborn cortical brain-mapping discovery).
- **Result:** **Zero overlap.**

---

## 3. Packaging, Why It Should Work & Search/Neighbour Evidence (`Rule 26` + `neighbours.py` + `public_search.py`)

- **Title A (Primary Proposal, `LEARNINGS.md` Rules 1, 15, 23, 26 — `42 chars`, `≤50 chars`, `0` exact collisions):** `Why Do We Hiccup? (The Tadpole Gill Twist)`
- **Title B (Test & Compare Arm 2, `Rules 15, 23` — `47 chars`, `≤50 chars`, `0` exact collisions):** `Hiccups Aren't a Mistake (The 370M-Year Reflex)`
- **Title C (`Rules 15, 26` Exact Phrase First — `50 chars`, `≤50 chars`, `0` exact collisions):** `Why Do We Hiccup? The Ancient Tadpole Brain Reflex`
- **One-Line Hook:** For centuries doctors dismissed hiccups as a useless diaphragm twitch — until a 1970 London electrode study, a 2003 evolutionary respiratory discovery, and a 2019 newborn brain scan revealed that your hiccup is actually a 370-million-year-old tadpole gill-pumping reflex kept alive to wire a baby's brain to breathe.
- **Why It Should Work (Past Winners & `LEARNINGS.md` Rules):**
  - Resembles top HOS longs **`002` Periodic Table (`AL_-qlWko_g`, `161` views, `2.68/d`, `1,160` impressions, `3.36%` CTR)** and **`004` Inside an Atom (`GHZDsiH7L7A`, `34` views, `1.06/d`, `837` impressions)** by starting with an exact, massive-volume everyday question (`Why Do We Hiccup?`, `42 chars ≤ 50 chars`) backed by `7` strictly on-topic education neighbours `≥1M` views in `neighbours.py` (`13` `≥1M` across both JSON files; `Rules 1, 15, 26`), while pairing that search demand with a concrete physiological apparatus and evolutionary twist like **`006` Willow Tree (`VbPubYd6Fbs`, `53.96%` Studio / `79%` 28d YTA avg view %)** and **`007` First Vaccine (`ETynHpIYLeY`, `7.41%` CTR)** so it avoids the low-impression starvation of statement-titled `005` (`15` impressions).
  - Resembles top HOS Shorts **`29bpGAI0wb8` (*What happens if you keep cutting gold in half?*, `1,227` views, `39.58/d`)**, **`-3L6HzJ_d_4` (*What Is the Pasteur Swan Neck Flask Experiment?*, `129` views, `77.14%` stayed PASS, `75.23%` avg view % PASS)**, and **`oKqmnJNGiHg` (*How Was Phosphorus Discovered?*, `188` views, `87.02%` avg view % PASS)** by answering a universal human-body reflex with a striking visual payoff at `≥70%` runtime (`Rules 2, 6, 8, 24, 27, 28, 30, 32`).
- **3-Way Thumbnail Test & Compare Plan (`LEARNINGS.md` Rules 11, 12, 14 + `THUMBNAIL_AND_TITLE_RULES.md` §2.1–2.B):**
  - **Thumb A (Hero Object — Human Diaphragm & Tadpole Gill Split):** Painted 3D house-style key art: on the right two-thirds, a glowing anatomical cutaway of a human chest and snapping vocal cords (`35 ms`) side by side with a translucent tadpole pumping water past its gills while closing its glottis; the Explorer small at lower left (round gold glasses, teal coat, finished hair); cream/gold serif text on the clear left band: `TADPOLE REFLEX` (`2 words`, gold on `TADPOLE`, zero overlap on the hero, `no other AI-made text`).
  - **Thumb B (`Rule 14` Bright High-Contrast Variant — Newborn Brain-Mapping Scan):** Bright sunlit hospital nursery/lab cutaway key art: a sleeping newborn with gentle glowing EEG sensor waves lighting up the somatosensory cortex in three bright pulses as the diaphragm contracts; Explorer small at lower left; serif text on the clear left band: `NOT A MISTAKE` (`3 words`, gold on `NOT`, zero overlap on the hero, `no other AI-made text`).
  - **Thumb C (Newsom Davis's 35-Millisecond Trap):** Painted 3D key art of a glowing red diaphragm pulling air downward while the vocal cords at the top of the windpipe slam shut like a brass trapdoor; Explorer small at lower left; serif text on the clear left band: `35 MILLISECONDS` (`2 words`, gold on `35`, zero overlap on the hero, `no other AI-made text`).
- **Signed-out YouTube Autocomplete (`2026-11-17`, `public_search.py` & `neighbours.py`):**
  - `"why do we hiccup"` → **`autocomplete = yes`** (`10` suggestions: `why do we hiccup`, `why do we hiccup dr. binocs`, `why do we hiccup zack d films`, `why do we hiccup ted ed`, `why do we hiccup when we eat spicy food`, `why do we get hiccups 3d animation`, etc.)
  - `"why do you hiccup"` → **`autocomplete = yes`** (`10` suggestions: `why do you hiccup`, `why do you have hiccups`, `why do i have hiccups all day`, etc.)
  - `"why do we get hiccups"` → **`autocomplete = yes`** (`10` suggestions: `why do we get hiccups`, `why do we get hiccups animation`, `why do we get hiccups mystery science`, etc.)
  - `"what causes hiccups"` → **`autocomplete = yes`** (`8` suggestions: `what causes hiccups`, `what causes hiccups in adults`, `what causes hiccups in kids`, `what causes hiccups in babies`, `what causes hiccups during pregnancy`, etc.)
  - `"why do babies hiccup in the womb"` → **`autocomplete = yes`** (`3` suggestions: `why do babies hiccup in the womb`, `why do babies get hiccups in the womb`, `does baby hiccups in the womb`)
  - `"diaphragm"`, `"respiratory"`, & `"lungs anatomy"` → **`autocomplete = yes`** (`30` anatomical/physiological suggestions in `neighbours.json`)
- **Rule 26(a) Two Ranking Videos (`≥10,000` views, retrieved `2026-11-17`):**
  1. `TED-Ed` — [`-AdQLkUkui8`](https://youtu.be/-AdQLkUkui8) *Why do we hiccup? - John Cameron* (**`3,344,659` views**)
  2. `Be Smart` — [`ylWgmSNBYtg`](https://youtu.be/ylWgmSNBYtg) *Why has no one cured hiccups yet?* (**`1,693,978` views**; plus `Zack D. Films` [`xSie-M8xVp4`](https://youtu.be/xSie-M8xVp4) **`8,844,060` views**, `Peekaboo Kidz` [`UZy2Wlh97SU`](https://youtu.be/UZy2Wlh97SU) **`2,902,625` views**, `Institute of Human Anatomy` [`MAsRkRK-S2E`](https://youtu.be/MAsRkRK-S2E) **`1,820,635` views**, `T-Series Kids Hut` [`UTLz-wHH2Pc`](https://youtu.be/UTLz-wHH2Pc) **`1,453,078` views**, `Doctor Mike` [`bDD-oM0FHko`](https://youtu.be/bDD-oM0FHko) **`1,341,797` views**, `It's AumSum Time` [`Ux9SEPRMF5Y`](https://youtu.be/Ux9SEPRMF5Y) **`1,167,955` views**, `It's AumSum Time` [`tZlUITVA_gE`](https://youtu.be/tZlUITVA_gE) **`955,763` views**, `Dr. Healthcare` [`epVaJeKlSnw`](https://youtu.be/epVaJeKlSnw) **`442,922` views**, and `SciShow Kids` [`9e5lcQycf2M`](https://youtu.be/9e5lcQycf2M) **`316,189` views**)
- **Neighbour Gate (`neighbours.py "why do we hiccup" "why do you hiccup" "cured hiccups" "diaphragm" "respiratory" "lungs anatomy" --top 25`):** **PASS (`7` strictly on-topic education videos `≥1,000,000` views, `TED-Ed/TED: yes`, `0` off-topic rows)** — saved in [`11_Upload-Package/evidence_2026-11-17_neighbours.json`](11_Upload-Package/evidence_2026-11-17_neighbours.json):
  1. `CrashCourse` — [`bHZsvBdUC2I`](https://youtu.be/bHZsvBdUC2I) *Respiratory System, Part 1: Crash Course Anatomy & Physiology #31* (**`5,923,036` views**, Tier 2)
  2. `Amoeba Sisters` — [`v_j-LD2YEqg`](https://youtu.be/v_j-LD2YEqg) *Respiratory System* (**`4,023,356` views**, Tier 2)
  3. `TED-Ed` ★ — [`8NUxvJS-_0k`](https://youtu.be/8NUxvJS-_0k) *How do lungs work? - Emma Bryce* (**`3,686,170` views**, Tier 1)
  4. `TED-Ed` ★ — [`-AdQLkUkui8`](https://youtu.be/-AdQLkUkui8) *Why do we hiccup? - John Cameron* (**`3,344,659` views**, Tier 1)
  5. `CrashCourse` — [`Cqt4LjHnMEA`](https://youtu.be/Cqt4LjHnMEA) *Respiratory System, Part 2: Crash Course Anatomy & Physiology #32* (**`3,130,640` views**, Tier 2)
  6. `Be Smart` — [`ylWgmSNBYtg`](https://youtu.be/ylWgmSNBYtg) *Why has no one cured hiccups yet?* (**`1,693,978` views**, Tier 2)
  7. `Khan Academy` — [`SPGRkexI_cs`](https://youtu.be/SPGRkexI_cs) *The lungs and pulmonary system | Health & Medicine | Khan Academy* (**`1,446,998` views**, Tier 2; plus `FuseSchool - Global Education` [`fQsgZloXNPY`](https://youtu.be/fQsgZloXNPY) **`507,164` views**, `SciShow Kids` [`9e5lcQycf2M`](https://youtu.be/9e5lcQycf2M) *Why Do We Get Hiccups?* **`316,189` views**, and `Cognito` [`Nn4ke02sW8Q`](https://youtu.be/Nn4ke02sW8Q) **`194,264` views**)

---

## 4. Candidate 4-Act Discovery Outline (All Claims UNVERIFIED Pending `SOURCES.md` & `facts` Lane)

- **Cold Open (0:00–0:45, UNVERIFIED):** Without warning, your diaphragm yanks downward, your chest jerks, and 35 milliseconds later your vocal cords slam shut with a sharp *"hic"*. Unlike coughing or sneezing, a hiccup clears nothing from your throat and brings almost no air into your lungs (`0:00–0:05`), cutting directly to a 1970 London electromyography oscilloscope trace and a side-by-side anatomical cutaway of a tadpole pumping water past its gills while slamming its glottis shut so water cannot flood its primitive lungs (`0:05–0:15`).
- **Act I — John Newsom Davis & the 35-Millisecond Glottis Trap (1970, UNVERIFIED):** For centuries after Galen, doctors assumed a hiccup was just a simple spasm of the stomach or diaphragm. In **August 1970** (*Brain* `93(4):851–872`), British neurologist **John Newsom Davis** at the National Hospital, Queen Square in London wired electromyography (EMG) electrodes and airflow sensors to patients with chronic hiccups. He proved a hiccup is a complex **brainstem command**: the diaphragm and external intercostal muscles fire together in a powerful inhalation, and roughly **35 milliseconds later** the **glottis** snaps shut before the air can fill the lungs — while raising arterial $\text{CO}_2$ (breathing into a bag or holding your breath) switches the brainstem rhythm off.
- **Act II — De Vries, Visser & Prechtl's 1982 Fetal Ultrasound Paradox (1982, UNVERIFIED):** If hiccups are just a digestive glitch, why do unborn babies do it more than anyone else? In **1982** (*Early Human Development* `7(4):301–322`), **Johanna de Vries, Gerard Visser, and Heinz Prechtl** at the University of Groningen used real-time ultrasound to watch human fetuses in the womb and found that unborn babies start hiccuping at **8 to 9 weeks of gestation** — before breathing movements even mature — spending up to **15 minutes a day** (`1–2%` of their time) hiccuping inside amniotic fluid where there is no air to breathe.
- **Act III — Christian Straus & William Whitelaw's February 2003 Tadpole Gill Discovery (2003, UNVERIFIED):** Why would mammals possess a brainstem circuit that inhales while slamming the windpipe to the lungs shut? In **February 2003** (*BioEssays* `25(2):182–188`), **Christian Straus** in Paris and **William Whitelaw** in Calgary realised the human hiccup circuit is homologous to the **370-million-year-old gill-ventilation reflex of air-breathing amphibians** like frog tadpoles. When a tadpole pumps water across its gills, it compresses its mouth and throat while slamming its glottis shut so water cannot flood its primitive lungs.
- **Act IV — Kimberley Whitehead & Lorenzo Fabrizi's November 2019 Newborn Brain-Mapping Proof (2019, UNVERIFIED):** Why didn't mammals delete the tadpole circuit once we lost our gills? In **November 2019** (*Clinical Neurophysiology* `130(11):2216–2221`) at University College London, **Kimberley Whitehead** and **Lorenzo Fabrizi** recorded EEG brainwaves in preterm and full-term newborn babies during hiccups. Every diaphragm contraction sent a massive **three-wave electrical burst** to the baby's somatosensory cortex — teaching the newborn brain to map and feel its own breathing muscles before birth.
- **Primary-Source Verification Guardrails (`J2971` — Mandatory Before Script Lock):**
  1. **Newsom Davis (`August 1970`, *Brain* `93(4):851–872`):** Verify exact patient count (`3` male patients with intractable hiccups), EMG electrode placement (`diaphragm`, `external intercostal`, `scalene`), exact latency in milliseconds from inspiratory burst onset to glottic closure (`~35 ms`), and arterial $P_{\text{CO}_2}$ suppression threshold.
  2. **De Vries, Visser & Prechtl (`1982`, *Early Human Development* `7(4):301–322`):** Verify cohort size (`11` healthy nulliparous women followed longitudinally from `7` to `19` weeks postmenstrual age), exact earliest gestational age of fetal hiccups (`8–9 weeks`), and incidence/duration figures.
  3. **Straus et al. & Whitelaw (`February 2003`, *BioEssays* `25(2):182–188`):** Verify exact co-author list (Christian Straus, Konstantinos Vasilakos, Richard J. A. Wilson, Thomas Oshima, Marc Zelter, Jean-Philippe Derenne, Thomas Similowski & William A. Whitelaw), central pattern generator (`CPG`) brainstem comparison between tadpole gill ventilation and mammalian hiccup, and the evolutionary/suckling retention hypothesis.
  4. **Whitehead et al. & Fabrizi (`November 2019`, *Clinical Neurophysiology* `130(11):2216–2221`):** Verify infant cohort (`13` newborn infants in the neonatal ward at UCLH, gestational age `30–42` weeks), exact three-event-related-potential (`ERP`) cortical waveform timings and somatosensory topography, and verbatim conclusion on respiratory somatosensory brain mapping.

---

## 5. Two Candidate Search-Titled Shorts (`Test B` / `Rule 26` / `Rule 32` — UNVERIFIED Concepts Only)

- **Short `S01`:** *Why Did Humans Keep the Tadpole Hiccup Reflex?* (`46 chars`, `0` exact collisions, positive search question)
  - **First-line answer hook (`0.0–1.5s`, `vo_onset_s ≤ 0.15s`, UNVERIFIED):** *"Your hiccup is a 370-million-year-old reflex built to pump water across tadpole gills."* (Names the titled noun `"hiccup"` and the surprise `"tadpole gills"` inside `≤1.5s` with zero meta-promise.)
  - **Frame-0, Overlay & Payoff Plan (`Rules 2, 3, 6, 24, 27`):** Frame 0 (`0.0s`, `mode: "cover"`, `0%` Explorer, `0%` bars): close moving cutaway of a human diaphragm jerking downward as the vocal cords snap shut (`BUILT FOR GILLS`, `3 words`, `#FFE000` on `GILLS` — distinct from `Thumb A`'s `TADPOLE REFLEX`, `Thumb B`'s `NOT A MISTAKE`, `Thumb C`'s `35 MILLISECONDS`, and `S02`'s `WIRING THE BRAIN`). Cut 1 `≤2.8s`, Cut 2 `≤4.8s`. Single mid-Short `Teach on screen` `WHEN` stamp: `PARIS, 2003` (white Didot italic inside the `16:9` centre band, clear of `0–2s` and the `9–14s` promoted title banner). Payoff start withheld until `≥70%` runtime (`~17.0s / 23.5s`): Christian Straus & William Whitelaw's February 2003 discovery that slamming the glottis shut 35 ms after inhaling is how a tadpole pumps water over its gills without flooding its lungs. Loop tail `<1.0s`, zero CTA.
- **Short `S02`:** *Why Do Unborn Babies Hiccup in the Womb?* (`40 chars`, `0` exact collisions, positive search question)
  - **First-line answer hook (`0.0–1.5s`, `vo_onset_s ≤ 0.15s`, UNVERIFIED):** *"Unborn babies hiccup in the womb for 15 minutes a day — long before they ever breathe air."* (Names `"unborn babies hiccup in the womb"` and the surprise `"15 minutes a day"` inside `≤1.5s` with zero meta-promise.)
  - **Frame-0, Overlay & Payoff Plan (`Rules 2, 3, 6, 24, 27`):** Frame 0 (`0.0s`, `mode: "cover"`, `0%` Explorer, `0%` bars): close moving 3D view of a fetus hiccuping as three glowing electrical waves light up its brain (`WIRING THE BRAIN`, `3 words`, `#FFE000` on `BRAIN`). Cut 1 `≤2.8s`, Cut 2 `≤4.8s`. Single mid-Short `Teach on screen` `WHEN` stamp: `LONDON, 2019` (white Didot italic inside the `16:9` centre band, clear of `0–2s` and the `9–14s` promoted title banner). Payoff start withheld until `≥70%` runtime (`~17.2s / 23.5s`): Kimberley Whitehead & Lorenzo Fabrizi's November 2019 UCL EEG discovery that each hiccup sends a three-wave signal to the baby's somatosensory cortex so the brain maps its breathing muscles before birth. Loop tail `<1.0s`, zero CTA.
