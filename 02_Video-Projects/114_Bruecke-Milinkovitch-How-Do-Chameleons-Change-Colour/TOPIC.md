# Topic Brief — `114_Bruecke-Milinkovitch-How-Do-Chameleons-Change-Colour` (`HOS:114` Proposal)

> **RULE-E GO & RULE G STATUS (`J2944` / `J2945`, `2026-11-16`):**
> - **Rule-E Verdict (`J2945`):** **GO (`95.5 / 100` · `9.55 / 10` Opportunity Score)** — Pre-cleared in the History of Science waiting line (`jobs/WIP.json` `next_hos`) under **Rule G** (`active` has `4 / 4` HOS slots full: `008`, `009`, `010`, `013`). Nothing is started in production (`status.json` stages are all `todo`).
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
- Open topic PRs `#572` (`102` Ozone Hole, `103` Why Is the Sky Blue), `#581` (`104` Speed of Light, `105` Venus Flytrap), `#588` (`106` Eels & Sargasso Sea, `107` Autumn Leaves & Chlorophyll), `#602` (`108` Why Is Ice Slippery, `109` Why Do Fingers Wrinkle in Water), `#607` (`110` Why Do Onions Make You Cry, `111` Why Do Knuckles Crack), `#614` (`112` Why Do We Yawn, `113` How Do Cats Land on Their Feet), and `#618` (`115` Why Do Zebras Have Stripes),
- All `011`–`095` backlog entries in `00_Brand/Channel-Setup/VIDEO_BACKLOG.json` and `00_Brand/Channel-Setup/ideas/` (`049` covers Dalton, Young, Helmholtz & Wald on human retinal colour vision and colour blindness; `092` covers Shimomura & Chalfie on jellyfish bioluminescence and GFP; `094` covers gecko van der Waals footpad adhesion; `095` covers butterfly metamorphosis; **none** cover how chameleons change colour, Ernst Brücke's 1851 Vienna chromatophore investigation, Devon Stuart-Fox & Adnan Moussalli's 2008 social-signalling spectrometry proof, or Michel Milinkovitch & Jérémie Teyssier's 2015 discovery of tunable guanine-nanocrystal photonic lattices inside chameleon iridophores).
- **Result:** **Zero overlap.**

---

## 3. Packaging, Why It Should Work & Search/Neighbour Evidence (`Rule 26` + `neighbours.py` + `public_search.py`)

- **Title A (Primary Proposal, `LEARNINGS.md` Rules 1, 15, 23, 26 — `56 chars`, `0` exact collisions):** `How Do Chameleons Change Colour? (The Nanocrystal Twist)`
- **Title A1 (Compact `Rule 15` `≤50 chars` & `Rule 26` Option — `48 chars`, `0` exact collisions):** `How Do Chameleons Change Colour? (Crystal Proof)`
- **Title B (Test & Compare Arm 2, `Rule 23` — `57 chars`, `0` exact collisions):** `Chameleons Have No Green Pigment (The 2015 Crystal Proof)`
- **Title B1 (Compact `Rule 15` `≤50 chars` T&C Option — `48 chars`, `0` exact collisions):** `Chameleons Have No Green Pigment (Crystal Proof)`
- **Title C (`Rule 26` Exact Phrase First — `59 chars`, `0` exact collisions):** `How Do Chameleons Change Colour? The Skin-Crystal Discovery`
- **One-Line Hook:** For over 2,000 years we believed chameleons change colour to blend into leaves by spreading bags of pigment — until a 2015 Geneva experiment proved panther chameleons have zero green pigment and instead tune a microscopic lattice of crystals like an accordion to bend light for rival duels.
- **Why It Should Work (Past Winners & `LEARNINGS.md` Rules):**
  - Resembles top HOS longs **`002` Periodic Table (`AL_-qlWko_g`, `161` views, `2.68/d`, `1,160` impressions, `3.36%` CTR)** and **`004` Inside an Atom (`GHZDsiH7L7A`, `34` views, `1.06/d`, `837` impressions)** by opening with an exact, high-volume everyday search question (`How Do Chameleons Change Colour?`) backed by `9` strictly on-topic `neighbours.py` education videos `≥1M` views (`15` `≥1M` videos across `neighbours.json` + `public_search.json`; `Rules 1, 15, 26`), while pairing that search demand with a tactile microscopic mechanism like **`006` Willow Tree (`VbPubYd6Fbs`, `53.96%` Studio / `79%` 28d YTA avg view %)** so it avoids the low-impression starvation of statement-titled `005` (`15` impressions).
  - Resembles top HOS Shorts **`29bpGAI0wb8` (*What happens if you keep cutting gold in half?*, `1,227` views, `39.58/d`)**, **`c2q7w0pgcn8` (*Who Discovered Infrared Light?*, `138` views, `43.52%` stayed, `105.30%` avg view % LOOP)**, and **`-3L6HzJ_d_4` (*What Is the Pasteur Swan Neck Flask Experiment?*, `129` views, `77.14%` stayed PASS, `75.23%` avg view % PASS)** by pairing a visible optical spectacle (green skin shifting to fiery red as crystal spacing expands) with direct myth-busting search questions (`Rules 2, 8, 24, 27, 28, 30, 32`).
- **3-Way Thumbnail Test & Compare Plan (`LEARNINGS.md` Rules 11, 12, 14 + `THUMBNAIL_AND_TITLE_RULES.md` §2.1–2.B):**
  - **Thumb A (Hero Object — The Half-Crystal Chameleon):** Painted 3D house-style key art: a giant close-up of a panther chameleon on the right two-thirds, its skin mid-shift from emerald green to fiery red, with a glowing magnifying lens revealing a geometric lattice of blue-and-gold nanocrystals beneath the scales (no AI-made text or numbers on the lens or lattice); the Explorer small at lower left; cream/gold serif text on the clear left band: `NO GREEN INK` (`3 words`, gold on `NO`, zero overlap on the chameleon).
  - **Thumb B (`Rule 14` Bright High-Contrast Variant — The Prism Skin Strip):** Bright sunlit Geneva laboratory key art: a beam of white light striking a stretched microscopic crystal lattice inside a chameleon scale and splitting into a vivid rainbow from blue to red (no AI-made numbers or wavelength labels in the scene); Explorer small at lower left; serif text on the left band: `TINY MIRRORS` (`2 words`, gold on `MIRRORS`).
  - **Thumb C (The Rival Duel Myth-Bust):** Painted 3D key art of two male panther chameleons facing off on a plain white branch, one flashing bright neon yellow-red while the leaf behind him stays dull green; Explorer small at lower left; serif text on the left band: `RIVAL DUEL` (`2 words`, gold on `RIVAL`).
- **Signed-out YouTube Autocomplete (`2026-11-16`):**
  - `"how do chameleons change color"` → **`autocomplete = yes`** (`8` suggestions: `how do chameleons change color`, `how does chameleons change color`, `how do chameleons change their color`, …)
  - `"how do chameleons change colour"` → **`autocomplete = yes`** (`4` suggestions: `how do chameleons change colour`, `how do chameleons change their color`, `how do chameleons change their colour`, …)
  - `"why do chameleons change color"` → **`autocomplete = yes`** (`3` suggestions: `why do chameleons change color`, `why does chameleon change color`, `why chameleons change color`)
  - `"why do chameleons change colour"` → **`autocomplete = yes`** (`4` suggestions: `why do chameleons change colour`, `why do chameleons change colors`, `why chameleon changes colour`, …)
- **Rule 26(a) Two Ranking Videos (`≥10,000` views, retrieved `2026-11-16`):**
  1. `Veritasium` — [`SQggDnScsvI`](https://youtu.be/SQggDnScsvI) *How Do Chameleons Change Color?* (**`3,475,292` views**)
  2. `Odd Animal Specimens` — [`Dd7UVLkuxC4`](https://youtu.be/Dd7UVLkuxC4) *The REAL Reason Chameleons Change Color* (**`2,255,381` views**; plus `The Animal Box Office` [`ioblgpA5eTo`](https://youtu.be/ioblgpA5eTo) **`21,524,829` views**, `Peekaboo Kidz` [`y9mr02mE5XE`](https://youtu.be/y9mr02mE5XE) **`1,488,401` views**, `Deep Look` [`Kp9W-_W8rCM`](https://youtu.be/Kp9W-_W8rCM) **`1,296,335` views**, `Happy Learning English` [`aZuxerppygM`](https://youtu.be/aZuxerppygM) **`1,104,566` views**, `Colossal Cranium` [`mGijLaiVqsU`](https://youtu.be/mGijLaiVqsU) **`429,445` views**, `Seeker` [`xWwgOIHSc1o`](https://youtu.be/xWwgOIHSc1o) **`166,206` views**, `National Geographic` [`1xVttpwEREs`](https://youtu.be/1xVttpwEREs) **`92,446` views**, and `New Scientist` [`IK_6Bq22nBo`](https://youtu.be/IK_6Bq22nBo) **`36,359` views**)
- **Neighbour Gate (`neighbours.py "chameleon" "camouflage" "how we see color" "rarest color"`):** **PASS (`9` strictly on-topic education videos `≥1,000,000` views, `TED-Ed/TED: yes`, `0` off-topic rows)** — saved in [`11_Upload-Package/evidence_2026-11-16_neighbours.json`](11_Upload-Package/evidence_2026-11-16_neighbours.json):
  1. `TED-Ed` ★ — [`gKfjHTk8KrY`](https://youtu.be/gKfjHTk8KrY) *History’s deadliest colors - J. V. Maranto* (**`8,462,817` views**)
  2. `TED-Ed` ★ — [`_r4c2NT4naQ`](https://youtu.be/_r4c2NT4naQ) *The science of skin color - Angela Koine Flynn* (**`3,540,205` views**)
  3. `Veritasium` — [`SQggDnScsvI`](https://youtu.be/SQggDnScsvI) *How Do Chameleons Change Color?* (**`3,475,292` views**)
  4. `Tom Scott` — [`rApTzWboLrA`](https://youtu.be/rApTzWboLrA) *The library of rare colors* (**`3,307,937` views**)
  5. `TED-Ed` ★ — [`rkRbebvoYqI`](https://youtu.be/rkRbebvoYqI) *What color is Tuesday? Exploring synesthesia - Richard E. Cytowic* (**`1,906,840` views**)
  6. `TED-Ed` ★ — [`l8_fZPHasdo`](https://youtu.be/l8_fZPHasdo) *How we see color - Colm Kelleher* (**`1,672,051` views**)
  7. `TED-Ed` ★ — [`yRwoReHd7XU`](https://youtu.be/yRwoReHd7XU) *What is the rarest color in nature? - Victoria Hwang* (**`1,326,018` views**)
  8. `SciShow Kids` — [`YOIRci0CKzg`](https://youtu.be/YOIRci0CKzg) *Camouflage: Animal Hide & Seek* (**`1,156,372` views**)
  9. `TED-Ed` ★ — [`UZ5UGnU7oOI`](https://youtu.be/UZ5UGnU7oOI) *What is color? - Colm Kelleher* (**`1,110,173` views**)

---

## 4. Candidate 4-Act Discovery Outline (All Claims UNVERIFIED Pending `SOURCES.md` & `facts` Lane)

- **Cold Open (0:00–0:45, UNVERIFIED):** Watch a bright green panther chameleon spot a rival male and flush blazing yellow and red in under two minutes (`0:00–0:05`), cutting directly to an excised patch of chameleon skin under a Geneva microscope lens shifting backwards through the rainbow from red to green to blue inside a salt bath (`0:05–0:15`). For 2,000 years we were taught chameleons change colour to blend into their surroundings by pumping coloured ink into their skin — until a 2015 physics experiment in Geneva proved a green chameleon has **zero green pigment** in its body, and instead tunes a microscopic lattice of crystals like an accordion.
- **Act I — Aristotle's Fear Myth & Ernst Brücke's 1851 Vienna Microscope (350 BC–1990s, UNVERIFIED):** From Aristotle's *History of Animals* (`~350 BC`, Book II, Ch. 11, `503b`, claiming the chameleon changes colour when inflated with air out of fear) to **Ernst Wilhelm von Brücke's** landmark **1851/1852** Vienna monograph (*Untersuchungen über den Farbenwechsel des afrikanischen Chamäleons*, *Denkschriften der Kaiserlichen Akademie der Wissenschaften* `4:179–210`), naturalists sliced chameleon skin under early microscopes. Brücke noticed layered cells and interference colours (`Interferenzfarben`), yet for the next 160 years biology textbooks simplified chameleon colour change into two myths: (1) chameleons change colour primarily to match any background, and (2) they do it solely by dispersing or clumping dark pigment sacks (`melanosomes`) inside spider-shaped cells.
- **Act II — Devon Stuart-Fox & Adnan Moussalli's 2008 Rival-Signal Proof (2008, UNVERIFIED):** In **January 2008** (*PLoS Biology* `6(1):e25`), evolutionary biologists **Devon Stuart-Fox** and **Adnan Moussalli** tested `21` lineages of southern African dwarf chameleons (*Bradypodion*) in the field using a portable reflectance spectrometer (`300–700 nm`) and photoreceptor vision models of both avian/snake predators and chameleons. When placed in front of a rival male or a female, chameleons flashed high-contrast colours that made them **more conspicuous, not more camouflaged** — proving dramatic colour shifts evolved primarily for **social signalling** (dominance contests and courtship) and **thermoregulation** (darkening to absorb morning heat), while resting green/brown is their baseline camouflage.
- **Act III — Michel Milinkovitch & Jérémie Teyssier's 2015 Photonic Crystal Discovery (2015, UNVERIFIED):** If pigment sacks only darken or lighten skin, how does a male panther chameleon (*Furcifer pardalis*) switch from green (`~520 nm`) to yellow, orange, and red (`>600 nm`) without any green or blue pigment? In **March 2015** (*Nature Communications* `6:6368`), physicist-biologist **Michel C. Milinkovitch** and **Jérémie Teyssier** (with **Sofia V. Saenko** and **Dirk van der Marel**) at the University of Geneva examined chameleon skin under transmission electron microscopy. Beneath the yellow pigment layer they found **two thick stacked layers of iridophore cells**: an upper **S-iridophore** layer packed with **`~127.4 ± 17.8 nm` (`~130 nm`) guanine nanocrystals** arranged in a 3D triangular **photonic crystal lattice** that actively tunes visible light, and a deeper **D-iridophore** layer of larger brick-shaped crystals (`~100–600 nm`) that reflects **`~45%` of direct sunlight energy in the near-infrared** as a passive thermal shield!
- **Act IV — The Osmotic Skin-Squeeze Proof (2015, UNVERIFIED):** When the chameleon is calm, the upper guanine nanocrystals sit close together, reflecting blue wavelengths (`~450 nm`) through the yellow top layer to look **green**. When excited by a rival, the chameleon relaxes the iridophore cell framework so the guanine crystal lattice distance expands by **`~30%`**, shifting the reflected light from blue to yellow, orange, and red! To prove that crystal lattice spacing alone causes the colour shift, Milinkovitch's team placed an excised patch of chameleon skin in hypertonic salt solutions: as osmotic pressure drew water out of the cells and the nanocrystal lattice shrank back together, the isolated skin strip ran **backwards through the rainbow from red to yellow to green to blue** right under the microscope lens.
- **Primary-Source Verification Guardrails (Required before Script Lock):**
  1. Verify exact wording and citation for Aristotle (*Historia Animalium* II.11 `503b`) and Ernst Wilhelm von Brücke (`1851` Academy presentation / `1852` *Denkschriften* `4:179–210`).
  2. Verify exact taxon count (`21` lineages of *Bradypodion*), spectral range (`300–700 nm`), and chromatic/achromatic contrast metrics (`JNDs`) in Stuart-Fox & Moussalli (`2008`, *PLoS Biology* `6(1):e25`).
  3. Verify exact guanine crystal diameters (`127.4 ± 17.8 nm` in S-iridophores), lattice distance shift (`~30%`), near-infrared reflectance fraction (`~45%`), and hypertonic osmotic pressure protocol in Teyssier, Saenko, van der Marel & Milinkovitch (`2015`, *Nature Communications* `6:6368`).

---

## 5. Two Candidate Search-Titled Shorts (`Test B` / `Rule 26` / `Rule 32` — UNVERIFIED Concepts Only)

- **Short `S01`:** *Why Do Chameleons Really Change Colour?* (`39 chars`, `0` exact collisions, positive search question)
  - **First-line answer hook (`0.0–1.5s`, UNVERIFIED):** *"Chameleons don't flash bright colours to blend in — when two rivals meet on a branch, they light up like neon signs to stand out."*
  - **Frame-0, Overlay & Payoff Plan (`Rules 2, 3, 6, 24, 27`):** Frame 0 (`0.0s`, `mode: "cover"`): close moving shot of a male panther chameleon flushing from emerald green to blazing red-gold on a bare branch (`NOT CAMOUFLAGE`, `#FFE000` on `NOT`, `0%` Explorer, `0%` bars). Single mid-Short `Teach on screen` overlay: `MELBOURNE, 2008` (`WHEN` stamp inside `16:9` centre band, clear of `0–2s` and the `9–14s` long-title banner). Payoff start at `≥70%` runtime (`~17.0s / 23.5s`): Stuart-Fox & Moussalli's 2008 field spectrometer proof across `21` dwarf chameleon lineages showing resting green is already camouflaged, and rapid colour shifts evolved to signal dominance to rivals and regulate body heat. Loop tail `<1.0s`, zero CTA.
- **Short `S02`:** *How Do Chameleons Turn Green Without Green Pigment?* (`51 chars`, `0` exact collisions, positive search question)
  - **First-line answer hook (`0.0–1.5s`, UNVERIFIED):** *"A green chameleon has zero green pigment in its skin — crush a green scale under a microscope and there isn't a drop of green ink."*
  - **Frame-0, Overlay & Payoff Plan (`Rules 2, 3, 6, 24, 27`):** Frame 0 (`0.0s`, `mode: "cover"`): extreme close zoom into a green chameleon scale splitting into a glowing lattice of blue-reflecting guanine nanocrystals (`ZERO GREEN INK`, `#FFE000` on `ZERO`, `0%` Explorer, `0%` bars). Single mid-Short `Teach on screen` overlay: `GENEVA, 2015` (`WHEN` stamp inside `16:9` centre band, clear of `0–2s` and the `9–14s` long-title banner). Payoff start at `≥70%` runtime (`~17.2s / 23.5s`): Michel Milinkovitch's 2015 Geneva experiment showing that expanding the spacing between `~130 nm` guanine nanocrystals by `~30%` shifts reflected light from blue (which mixes with yellow skin to look green) all the way to red — proved by shrinking an excised skin strip in salt water. Loop tail `<1.0s`, zero CTA.
