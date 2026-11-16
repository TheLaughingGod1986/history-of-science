# Topic Brief — `110_Virtanen-Block-Imai-Why-Do-Onions-Make-You-Cry` (`HOS:110` — Rule-E GO in `next_hos`)

> **RULE-E GO & RULE G STATUS (`J2922` / `J2924`, `2026-11-16`):**
> - **Rule-E Topic Go/No-Go Review (`J2924`):** **GO (`95 / 100` · `9.50 / 10` Opportunity Score)** — Pre-cleared in the History of Science waiting line (`jobs/WIP.json` `next_hos`) under **Rule G** (`active` has `4 / 4` HOS films: `008`, `009`, `010`, `013`). Nothing is started in production (`status.json` stages remain `todo`).
> - **Awaits Active HOS Slot & `facts` Lane:** All historical and scientific claims in this brief are **UNVERIFIED** working notes. Before any script is locked or VO is recorded, every claim must be backed by verbatim primary-source quotes in `SOURCES.md` and verified through the `facts` lane (`gemini-agy`).

---

## 1. HOS Data Comparison (`2026-11-15` Snapshot + `studio_ctr.json` + `channel_daily.json`)

- **Data sources read:**
  - `05_Analytics/hos/snapshots/2026-11-15.json` (`takenAt: 2026-11-15T06:40:28.409Z`, `36` public videos = `7` longs + `29` Shorts, `3,902` total views, `6` subscribers)
  - `05_Analytics/hos/studio_ctr.json` (`readAt: 2026-11-15T07:53:35.291276+00:00`, lifetime Studio impressions, CTR, average view %, and Shorts stayed-to-watch %)
  - `05_Analytics/hos/channel_daily.json` (`through: 2026-11-13`) and `05_Analytics/hos/REPORT.md`
  - `05_Analytics/LEARNINGS.md` (rules 1–33)
- **Elapsed-day denominator (`age_days`):** `max((date(2026, 11, 15) - date.fromisoformat(publishedAt[:10])).days, 1)` (`views/day = views / age_days`).
- **Low-sample statistical caveat (`Rule 1` / `RULING.md`):** Several public HOS longs have only `3–10` lifetime views (`15–44` impressions), and bottom-tier Shorts have `4–30` views. Patterns inferred from those small-N rows are treated explicitly as **hypotheses**, not settled laws.

### 1a. All `7` Public HOS Longs — Ranked by Views/Day Since Publish (`2026-11-15`)

| Rank | Video ID | Film | Title | Published (`age_days`) | Views (`2026-11-15`) | Views / Day | Studio Impressions (Lifetime) | Studio CTR (Lifetime) | Studio Avg View % (Lifetime) | YTA 28d Views (`through 11-13`) | YTA 28d Avg View % |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **1** | `AL_-qlWko_g` | `002` | *How Did We Discover the Periodic Table?* | `2026-09-17` (`59d`) | **161** | **2.73/d** | 1,160 | 3.36% | 21.59% (`117s / 541s`) | 16 | 19.16% |
| **2** | `GHZDsiH7L7A` | `004` | *What's Inside an Atom? Mostly Empty Space* | `2026-10-15` (`31d`) | **34** | **1.10/d** | 837 | 1.31% | 24.29% (`128s / 525s`) | 22 | 29.91% |
| **3** | `VbPubYd6Fbs` | `006` | *The Willow Tree That Was Made of Air* | `2026-11-05` (`10d`) | **10** | **1.00/d** | 36 | 2.78% | **66.54%** (`354s / 532s`) | 10 | 79.36% |
| **4** | `ETynHpIYLeY` | `007` | *How Was the First Vaccine Made? (And Why It's Named After a Cow)* | `2026-11-12` (`3d`) | **3** | **1.00/d** | 16 | 12.50% | 5.26% (`28s / 532s`) | 1 | 3.35% |
| **5** | `wwcjcFfC-5M` | `005` | *The Tied Arm That Proved Your Blood Circulates* | `2026-10-29` (`17d`) | **5** | **0.29/d** | 15 | **20.00%** | 9.24% (`49s / 529s`) | 5 | 9.24% |
| **6** | `frP_YrNShsU` | `003` | *How Did We Discover X-rays?* | `2026-09-24` (`52d`) | **5** | **0.10/d** | 41 | 2.44% | 26.65% (`114s / 426s`) | 3 | 14.12% |
| **7** | `_C92tIJCk8A` | `001` | *How Did We Discover Germs?* | `2026-09-03` (`73d`) | **7** | **0.10/d** | 44 | 6.82% | 48.08% (`176s / 365s`) | 0 | — |

- **3 Best HOS Longs & What They Share:**
  1. **`AL_-qlWko_g` (`002` *How Did We Discover the Periodic Table?*, `541s`)** — **`2.73` views/day** (`161` views in `59d`), **`1,160` impressions** (`54.0%` of all HOS long impressions), `3.36%` CTR, `21.59%` Studio avg view % (`71%` at `0:15`, `51%` at `0:30`).
  2. **`GHZDsiH7L7A` (`004` *What's Inside an Atom? Mostly Empty Space*, `525s`)** — **`1.10` views/day** (`34` views in `31d`), **`837` impressions** (`38.9%` of all HOS long impressions), `1.31%` CTR, `24.29%` Studio avg view % (`29.91%` in 28d YTA; `60%` at `0:15`, `47%` at `0:30`).
  3. **`VbPubYd6Fbs` (`006` *The Willow Tree That Was Made of Air*, `532s`)** — **`1.00` views/day** (`10` views in `10d`), `36` impressions, `2.78%` CTR, and channel-best **`66.54%` Studio / `79.36%` 28d YTA avg view %** (`354s / 532s`; low-N hypothesis at `10` views).
  - **Shared pattern (Subject, Title Shape, Opening, Thumbnail Concept, Length):** `002` and `004` together generate **`92.9%` (`1,997 / 2,149`) of all HOS long impressions** and **`86.7%` (`195 / 225`) of all HOS long views** because their titles open with plain, high-volume curriculum/search questions (`Periodic Table`, `What's Inside an Atom?`) backed by massive `TED-Ed` neighbour pools (`LEARNINGS.md` Rules 1, 15, 26), run `8.5–9.0 min` (`525–541s`), and open on concrete physical proof (`60–71%` at `0:15`, Rule 10). `006` proves that a concrete tabletop experiment (`5-year` weighed willow tree) holds viewers once clicked (`66.54%` Studio avg view %), while its poetic statement title (`The Willow Tree That Was Made of Air`) starved it of search impressions (`36` impressions vs `1,160` on `002`).
- **3 Worst HOS Longs & What They Share (Hypotheses on Small N):**
  1. **`_C92tIJCk8A` (`001` *How Did We Discover Germs?*, `365s`)** — **`0.10` views/day** (`7` views in `73d`), `44` impressions, `6.82%` CTR, `48.08%` avg view % (`50%` at `0:15`, `33%` at `0:30`).
  2. **`frP_YrNShsU` (`003` *How Did We Discover X-rays?*, `426s`)** — **`0.10` views/day** (`5` views in `52d`), `41` impressions, `2.44%` CTR, `26.65%` avg view % (`25%` at `0:15`, `0%` at `0:30`).
  3. **`wwcjcFfC-5M` (`005` *The Tied Arm That Proved Your Blood Circulates*, `529s`)** — **`0.29` views/day** (`5` views in `17d`), `15` impressions, `20.00%` CTR, `9.24%` avg view %.
  - **Shared pattern:** Either generic textbook-chapter questions lacking a specific hook/twist (`001`, `003`, shorter `6–7 min` runtimes) or apparatus-first declarative statements (`005` *The Tied Arm...*, `15` impressions) that omit the plain question viewers actually type into YouTube search (`LEARNINGS.md` Rules 15, 23, 26). **Lesson applied to `HOS:110`:** Start verbatim with the high-volume signed-out autocomplete question (`Why Do Onions Make You Cry?`) and follow immediately with the concrete discovery twist (`(The 2002 Enzyme Twist)` / `(2002 Enzyme Twist)`).

### 1b. All `29` Public HOS Shorts — Ranked by Views/Day Since Publish (`2026-11-15`)

| Rank | Video ID | Title | Published (`age_days`) | Views (`2026-11-15`) | Views / Day | Stayed to Watch (`studio_ctr.json`) | Studio Avg View % (`avgViewSeconds / sec`) | Likes |
|---:|---|---|---:|---:|---:|---:|---:|---:|
| **1** | `29bpGAI0wb8` | *What happens if you keep cutting gold in half?* | `2026-10-16` (`30d`) | **1,227** | **40.90/d** | 40.78% | 44.12% (`11s / 25s`) | 12 |
| **2** | `PFj6172YU4Q` | *One Tight Band Proved Your Blood Goes Round* | `2026-11-08` (`7d`) | **219** | **31.29/d** | 15.98% | 62.95% (`17s / 27s`) | 3 |
| **3** | `AMSriTQ-lcQ` | *Are Marie Curie's Notebooks Still Radioactive?* | `2026-10-28` (`18d`) | **274** | **15.22/d** | 22.66% | 76.94% (`17s / 22s`) | 6 |
| **4** | `OnJ8MFu0Mi0` | *How Did John Snow Stop Cholera?* | `2026-10-26` (`20d`) | **231** | **11.55/d** | 29.60% | 65.66% (`15s / 23s`) | 8 |
| **5** | `pWySvZsneZg` | *Why Gold Foil Bounced Rutherford's Particles Back* | `2026-11-01` (`14d`) | **137** | **9.79/d** | 37.23% | 112.43% (`28s / 25s`) | 2 |
| **6** | `cLKDiYP55J8` | *What Was the Edward Jenner Experiment?* | `2026-11-13` (`2d`) | **16** | **8.00/d** | 26.67% | 50.02% (`12s / 23s`) | 0 |
| **7** | `oKqmnJNGiHg` | *How Was Phosphorus Discovered?* | `2026-10-21` (`25d`) | **187** | **7.48/d** | 41.18% | 87.02% (`20s / 23s`) | 7 |
| **8** | `-3L6HzJ_d_4` | *What Is the Pasteur Swan Neck Flask Experiment?* | `2026-10-27` (`19d`) | **128** | **6.74/d** | **77.14%** | 75.23% (`14s / 19s`) | 1 |
| **9** | `BW_CFAX-mxc` | *Is the Heart a Pump?* | `2026-10-31` (`15d`) | **89** | **5.93/d** | 32.91% | 81.69% (`18s / 22s`) | 1 |
| **10** | `clV6E10NLPw` | *The spray that stopped surgery killing patients* | `2026-10-20` (`26d`) | **153** | **5.88/d** | 23.08% | 56.16% (`14s / 25s`) | 4 |
| **11** | `qOZgess30h0` | *Invisible life is still everywhere* | `2026-10-13` (`33d`) | **169** | **5.12/d** | 25.15% | 39.82% (`10s / 24s`) | 5 |
| **12** | `c2q7w0pgcn8` | *Who Discovered Infrared Light?* | `2026-10-19` (`27d`) | **138** | **5.11/d** | 43.52% | 105.30% (`24s / 23s`) | 1 |
| **13** | `Rl2uZ-KOTl8` | *Your Heart Pumps More Blood Than You Have* | `2026-10-30` (`16d`) | **78** | **4.88/d** | 26.58% | 53.64% (`13s / 25s`) | 4 |
| **14** | `xHnIi9GqOsM` | *Why Do Veins Have Valves?* | `2026-11-05` (`10d`) | **41** | **4.10/d** | 20.59% | 61.55% (`14s / 23s`) | 0 |
| **15** | `qW2OsD4mujc` | *The Four Elements Were Wrong* | `2026-11-03` (`12d`) | **35** | **2.92/d** | 57.69% | 192.62% (`46s / 24s`) | 0 |
| **16** | `TbMMJSRKC3U` | *He said every eighth element repeats* | `2026-10-18` (`28d`) | **62** | **2.21/d** | 25.49% | 123.27% (`33s / 27s`) | 1 |
| **17** | `LCZRHUyTiq0` | *What Are Cathode Rays?* | `2026-10-23` (`23d`) | **49** | **2.13/d** | 29.79% | 50.04% (`13s / 26s`) | 2 |
| **18** | `iqToagXnjX0` | *Microbes in a drop of pond water* | `2026-09-06` (`70d`) | **112** | **1.60/d** | 28.28% | 77.86% (`19s / 25s`) | 1 |
| **19** | `H1y0DXFVmw8` | *Germs don't cast a shadow* | `2026-09-06` (`70d`) | **80** | **1.14/d** | 19.75% | 59.46% (`15s / 25s`) | 1 |
| **20** | `xvanpsLeADE` | *How did Röntgen see bones without cutting* | `2026-09-26` (`50d`) | **40** | **0.80/d** | 23.33% | 50.33% (`13s / 25s`) | 0 |
| **21** | `oowAOWTBoq0` | *How X-rays Were Discovered by Accident* | `2026-09-25` (`51d`) | **32** | **0.63/d** | 47.62% | **331.08%** (`83s / 25s`) | 1 |
| **22** | `nba0-f7PPeU` | *Why tellurium sat before iodine* | `2026-09-21` (`55d`) | **34** | **0.62/d** | 60.71% | 42.70% (`11s / 25s`) | 1 |
| **23** | `nFQRWmpulTQ` | *He predicted a metal before it was found* | `2026-09-19` (`57d`) | **34** | **0.60/d** | 66.67% | 55.91% (`14s / 25s`) | 0 |
| **24** | `uU12JA5rMWg` | *The periodic table's empty chairs* | `2026-09-18` (`58d`) | **30** | **0.52/d** | 66.67% | 58.79% (`15s / 25s`) | 0 |
| **25** | `8_Edn_HCi1s` | *Germs hitch a ride on you* | `2026-09-06` (`70d`) | **30** | **0.43/d** | 22.22% | 38.78% (`10s / 25s`) | 0 |
| **26** | `sILtQxgYQk8` | *A flask that proved germs come from outside* | `2026-09-06` (`70d`) | **24** | **0.34/d** | 41.67% | 36.70% (`9s / 25s`) | 0 |
| **27** | `CnHwX1L9XHg` | *Gallium sat where the table said* | `2026-09-20` (`56d`) | **16** | **0.29/d** | 30.43% | 33.45% (`9s / 26s`) | 0 |
| **28** | `zI_eD3vFWmE` | *The first X-ray showed a wedding ring* | `2026-09-27` (`49d`) | **9** | **0.18/d** | 50.00% | 64.00% (`16s / 25s`) | 0 |
| **29** | `LanTHJckYx8` | *What other table has empty chairs?* | `2026-09-22` (`54d`) | **4** | **0.07/d** | 33.33% | 23.08% (`6s / 26s`) | 0 |

- **3 Best HOS Shorts & What They Share:**
  1. **`29bpGAI0wb8` (*What happens if you keep cutting gold in half?*, `25s`)** — **`40.90` views/day** (`1,227` views in `30d`), `40.78%` stayed-to-watch, `44.12%` avg view % (`11s / 25s`), `12` likes.
  2. **`-3L6HzJ_d_4` (*What Is the Pasteur Swan Neck Flask Experiment?*, `19s`)** — **`6.74` views/day** (`128` views in `19d`), channel-best **`77.14%` stayed-to-watch (PASS `≥60%`)** and **`75.23%` avg view % (PASS `≥70%`)**, with **`92.9%` (`118 / 127`) of 28d views coming from YouTube search** — the first mature `100+` view HOS Short to pass both targets (`LEARNINGS.md` Rules 28 & 32).
  3. **`AMSriTQ-lcQ` (*Are Marie Curie's Notebooks Still Radioactive?*, `22s`)** — **`15.22` views/day** (`274` views in `18d`), **`76.94%` avg view % (PASS `≥70%`)**, `22.66%` stayed-to-watch, `6` likes — alongside loop winners `pWySvZsneZg` (*Why Gold Foil Bounced Rutherford's Particles Back*, `9.79/d`, `137` views, `37.23%` stayed, **`112.43%` avg view % LOOP**) and `c2q7w0pgcn8` (*Who Discovered Infrared Light?*, `5.11/d`, `138` views, `43.52%` stayed, **`105.30%` avg view % LOOP**) and feed velocity #2 `PFj6172YU4Q` (`31.29/d`, `219` views, `62.95%` avg view %, `15.98%` stayed).
  - **Shared pattern:** Positive search-question titles (`What happens if...`, `What Is...`, `Are...`, `Why...`, `Who Discovered...`, `How Was...`) outperform statement titles (`PFj6172YU4Q` dropped to `15.98%` stayed despite `31.29/d` feed reach; `LEARNINGS.md` Rule 32), while `≤1.0s` loop tails with zero CTA and payoff withheld until `≥70%` runtime lift avg view % to `75–112%+` (`Rules 3, 6, 24, 27`).
- **3 Worst HOS Shorts & What They Share (Hypotheses on Small N):**
  1. **`LanTHJckYx8` (*What other table has empty chairs?*, `26s`)** — **`0.07` views/day** (`4` views in `54d`), `33.33%` stayed-to-watch, `23.08%` avg view % (`6s / 26s`).
  2. **`zI_eD3vFWmE` (*The first X-ray showed a wedding ring*, `25s`)** — **`0.18` views/day** (`9` views in `49d`), `50.00%` stayed-to-watch, `64.00%` avg view %.
  3. **`CnHwX1L9XHg` (*Gallium sat where the table said*, `26s`)** — **`0.29` views/day** (`16` views in `56d`), `30.43%` stayed-to-watch, `33.45%` avg view %.
  - **Shared pattern:** Cryptic riddles (*What other table has empty chairs?*) and flat past-tense statements (*Gallium sat where the table said*, *The first X-ray showed a wedding ring*) omit the searchable subject noun and fail both Shorts-feed stayed-to-watch and YouTube search discovery (`LEARNINGS.md` Rules 1, 28, 32).

---

## 2. Overlap & Non-Duplication Check (`2026-11-16`)

Checked against:
- All folders in `02_Video-Projects/` (`000`–`018`, `099`–`101` on `main`),
- Open topic PRs `#572` (`102` Ozone Hole, `103` Why Is the Sky Blue), `#581` (`104` Speed of Light, `105` Venus Flytrap), `#588` (`106` Eels & Sargasso Sea, `107` Autumn Leaves & Chlorophyll), `#602` / `#603` / `#604` (`108` Why Is Ice Slippery, `109` Why Do Fingers Wrinkle in Water), and `#607` (`111` Why Do Knuckles Crack),
- All `011`–`095` backlog entries in `00_Brand/Channel-Setup/VIDEO_BACKLOG.json` and `00_Brand/Channel-Setup/ideas/` (`051` covers Scoville, Julius & Patapoutian on spicy capsaicin and `TRPV1`; `056` covers Buck & Axel on smell/olfaction; `070` covers Fischer, Buchner & Sumner on general enzymes; `085` covers taste buds and umami; **none** cover why slicing onions makes you cry, Virtanen's `isoalliin`/`alliinase` compartment puzzle, Brodnitz & Pascale / Eric Block's characterization of `(Z)-propanethial S-oxide`, or Shinsuke Imai's 2002 *Nature* discovery of lachrymatory-factor synthase `LFS`).
- **Result:** **Zero overlap.**

---

## 3. Packaging, Why It Should Work & Search/Neighbour Evidence (`Rule 26` + `neighbours.py` + `public_search.py`)

- **Title A (Primary Proposal, `LEARNINGS.md` Rules 1, 23, 26 — `51 chars ≤ 70 chars`, `0` exact collisions):** `Why Do Onions Make You Cry? (The 2002 Enzyme Twist)`
- **Title A1 (Compact Rule 15 + Rule 26 Variant — `47 chars ≤ 50 chars`, `0` exact collisions):** `Why Do Onions Make You Cry? (2002 Enzyme Twist)`
- **Title B (Test & Compare Arm 2, `Rule 23` — `52 chars`, `0` exact collisions):** `The Hidden Chemical Weapon Inside Every Sliced Onion`
- **Title C (`Rule 26` Exact Phrase First — `57 chars`, `0` exact collisions):** `Why Do Onions Make You Cry? How a Second Enzyme Was Found`
- **One-Line Hook:** An intact onion holds zero tear gas — until your kitchen knife smashes two microscopic vaults together and a hidden second enzyme discovered only in 2002 hijacks the onion's flavour chemistry in milliseconds.
- **Why It Should Work (Past Winners & `LEARNINGS.md` Rules):**
  - Resembles top HOS longs **`002` Periodic Table (`AL_-qlWko_g`, `161` views, `2.73/d`, `1,160` impressions, `3.36%` CTR)** and **`004` Inside an Atom (`GHZDsiH7L7A`, `34` views, `1.10/d`, `837` impressions)** by leading with an everyday household/curriculum question backed by `TED-Ed` chemistry/biology neighbours (`Rules 1, 15, 26`), while combining the tabletop experimental retention of **`006` Willow Tree (`VbPubYd6Fbs`, `66.54%` Studio / `79.36%` YTA 28d avg view %)** with a search-first title so it is not starved of impressions.
  - Resembles top HOS Shorts **`29bpGAI0wb8` (*What happens if you keep cutting gold in half?*, `1,227` views, `40.90/d`)** and **`-3L6HzJ_d_4` (*What Is the Pasteur Swan Neck Flask Experiment?*, `128` views, `77.14%` stayed PASS, `75.23%` avg view % PASS, `92.9%` YT_SEARCH)** by anchoring Frame 0 on a familiar kitchen blade slicing an onion cell (`Rules 2, 8, 24, 27, 28, 30, 32`).
- **3-Way Thumbnail Test & Compare Plan (`LEARNINGS.md` Rules 11, 12, 14 + `THUMBNAIL_AND_TITLE_RULES.md` §2.1–2.B):**
  - **Thumb A (Hero Object — The Knife & Bursting Cell Vaults):** Painted 3D house-style key art: a gleaming steel chef's blade slicing into a translucent golden onion on the right two-thirds, releasing a rising emerald-gold mist of tear-gas molecules; the Explorer small at lower left shielding his eyes; cream/gold serif text on the clear left band: `TWO VAULTS` (`2 words`, gold on `TWO`, zero overlap on the onion).
  - **Thumb B (`Rule 14` Bright High-Contrast Variant — Garlic vs Onion Paradox):** Bright sunlit laboratory bench key art: a white garlic clove and a sliced red-gold onion side by side under a magnifying glass, with a glowing red warning arrow rising only from the onion; Explorer small at lower left; serif text on the left band: `WHY NOT GARLIC?` (`3 words`, gold on `GARLIC?`).
  - **Thumb C (The 2002 Glass Vial Twist):** Painted 3D key art of Shinsuke Imai's two clear glass laboratory vials on the right — one peaceful, one erupting with golden vapour as the second enzyme (`LFS`) drops in from a pipette; Explorer small at lower left; serif text on the left band: `HIDDEN ENZYME` (`2 words`, gold on `HIDDEN`).
- **Signed-out YouTube Autocomplete (`2026-11-16`):**
  - `"why do onions make you cry"` → **`autocomplete = yes`** (`why do onions make you cry`, `why do onions make you cry aumsum`, `why do onions make you cry muppets`, `why do onions make you cry zack d films`, `why do onions make us cry`)
  - `"why do we cry"` → **`autocomplete = yes`** (`why do we cry`, **`why do we cry when we cut onions`**, `why do we cry when we're sad`, `why do we cry dr binocs`, `why do we cry when we laugh`, etc.)
  - `"how enzymes work"` → **`autocomplete = yes`** (`how enzymes work`, `how enzymes work in our body`, `how enzymes work biochemistry`, `how enzymes work (from pdb-101)`, `how enzymes work 3d animation`, `how enzymes work in digestion`)
- **Rule 26(a) Two Ranking Videos (`≥10,000` views, retrieved `2026-11-16`):**
  1. `Colossal Cranium` — [`1OoWsiY6Lf8`](https://youtu.be/1OoWsiY6Lf8) *Why Do Onions Make Us Cry? | COLOSSAL QUESTIONS* (**`3,486,968` views**)
  2. `It's AumSum Time` — [`9ZinH1jEhb4`](https://youtu.be/9ZinH1jEhb4) *Human Tears - Why do onions make you cry?* (**`2,452,719` views**; plus `AumSum's What-If` [`dVw3DrqihIg`](https://youtu.be/dVw3DrqihIg) **`2,917,778` views**, `SciShow` [`vRroj26qVb0`](https://youtu.be/vRroj26qVb0) *Onions, Emotions, and Why We Cry* **`623,053` views**, `SciShow Kids` [`mBiNkhigr8o`](https://youtu.be/mBiNkhigr8o) **`301,430` views**, `Seeker` [`ERtlCbByqVg`](https://youtu.be/ERtlCbByqVg) **`194,407` views**, `SciShow` [`IS9bo3cVmYI`](https://youtu.be/IS9bo3cVmYI) **`107,920` views**, and `Reactions` [`RaZpPwmWZ7Q`](https://youtu.be/RaZpPwmWZ7Q) **`107,887` views**)
- **Neighbour Gate (`neighbours.py`):** **PASS (`12` total `≥1,000,000` view education videos, of which `9` are strictly on-topic `onTopic: true`; `TED-Ed/TED: yes`)** — saved in [`11_Upload-Package/evidence_2026-11-16_neighbours.json`](11_Upload-Package/evidence_2026-11-16_neighbours.json):
  1. `TED-Ed` ★ — [`Og5xAdC8EUI`](https://youtu.be/Og5xAdC8EUI) *How your digestive system works - Emma Bryce* (**`14,043,201` views**, digestive enzymes)
  2. `Amoeba Sisters` — [`qgVFkRn8f10`](https://youtu.be/qgVFkRn8f10) *Enzymes (Updated)* (**`7,269,331` views**, enzyme-substrate catalysis)
  3. `TED-Ed` ★ — [`keMF8YzQoRM`](https://youtu.be/keMF8YzQoRM) *Why do we cry? The three types of tears - Alex Gendler* (**`6,914,192` views**, reflex tears triggered by onion `syn-propanethial-S-oxide` vapor; found by `"ted-ed why do onions make you cry"`)
  4. `TED-Ed` ★ — [`Hja0SLs2kus`](https://youtu.be/Hja0SLs2kus) *The amazing ways plants defend themselves - Valentin Hammoudi* (**`4,447,334` views**, plant chemical defenses)
  5. `TED-Ed` ★ — [`n6wpNhyreDE`](https://youtu.be/n6wpNhyreDE) *How to make the perfect cookies (according to science) - Stephanie Warren* (**`4,171,001` views**, kitchen food chemistry)
  6. `TED-Ed` ★ — [`OttRV5ykP7A`](https://youtu.be/OttRV5ykP7A) *How to speed up chemical reactions (and get a date) - Aaron Sams* (**`2,468,735` views**, chemical reaction rates & catalysts)
  7. `TED-Ed` ★ — [`ee7muQ_qKU0`](https://youtu.be/ee7muQ_qKU0) *The wild world of carnivorous plants - Kenny Coogan* (**`2,362,239` views**, plant enzymes & defense)
  8. `FuseSchool - Global Education` — [`rlH1ym916Fo`](https://youtu.be/rlH1ym916Fo) *Enzymes | Cells | Biology | FuseSchool* (**`1,151,481` views**, enzyme catalysis)
  9. `TED-Ed` ★ — [`8m6RtOpqvtU`](https://youtu.be/8m6RtOpqvtU) *What triggers a chemical reaction? - Kareem Jarrah* (**`1,073,460` views**, reaction activation)
  - *(Note: 3 broad `"how ... work"` human-physiology matches in `neighbours.json` — `PSRJfaAYkW4` `5.23M` immune system, `ClPVJ25Ka4k` `4.73M` antidepressants, and `-SPRPkLoKp8` `2.73M` hormones — are marked `"onTopic": false` and excluded from the `9` strictly on-topic `≥1M` neighbours above).*

---

## 4. Candidate 4-Act Discovery Outline (All Claims UNVERIFIED Pending `SOURCES.md` & `facts` Lane)

- **Cold Open (0:00–0:45, UNVERIFIED):** A whole onion on your chopping board has zero smell and zero tear gas — until a steel knife blade slices through its cells and within 5 seconds your eyes sting and flood with tears. For over 40 years, chemists thought a single flavour enzyme (`alliinase`) automatically produced that tear gas — until a 2002 experiment in Japan proved everyone had missed a hidden second enzyme.
- **Act I — Stoll, Seebeck & Virtanen's Two-Vault Binary Bomb (1948–1963, UNVERIFIED):** After Arthur Stoll and Ewald Seebeck (`1948`, Basel, *Helvetica Chimica Acta* 31: 189–210) isolate `alliin` and the enzyme `alliinase` in garlic, Finnish Nobel laureate Artturi Ilmari Virtanen and Claes-Gösta Spåre (`1961–1963`, Helsinki, *Acta Chemica Scandinavica* 17: 641–650) map the tear-factor precursor of onions (`isoalliin`, *trans*-(+)-*S*-(1-propenyl)-L-cysteine sulfoxide — a structural isomer of garlic's `alliin`). Inside an intact onion cell, the fuel (`isoalliin`) floats in the cytoplasm while the trigger enzyme (`alliinase`) sits locked inside a membrane-bound vacuole — a biological binary weapon that detonates only when a rodent's teeth or a kitchen knife breaks the wall between them.
- **Act II — Brodnitz, Pascale & Eric Block Trap the Vanishing Tear Gas & The Garlic Paradox (1964–1992, UNVERIFIED):** Because the onion tear gas decomposes in seconds, early chemists misidentified it for decades. After Walter F. Wilkens (`1964`) and M. H. Brodnitz & J. V. Pascale (`1971`, *J. Agric. Food Chem.* 19: 269–272) isolate thiopropanal *S*-oxide (propanethial *S*-oxide) by gas chromatography and mass spectrometry, American chemist Eric Block and colleagues (`1979–1992`, *J. Am. Chem. Soc.* 1979/1980; *Angewandte Chemie* 1992, 31: 1135–1178) use flash-vacuum pyrolysis, microwave spectroscopy, and low-temperature NMR to prove the true lachrymatory factor is **`(Z)`-propanethial *S*-oxide** (`syn`-propanethial-*S*-oxide) — a volatile three-carbon sulfine gas formed from `1-propenylsulfenic acid` that rises into the air and activates pain receptors on the wet cornea, triggering the lacrimal glands (`TED-Ed` `keMF8YzQoRM` reflex tears) to wash the eye. Yet a puzzle remained: chemists assumed `1-propenylsulfenic acid` rearranged spontaneously into tear gas after `alliinase` cut it — so why could nobody control the tear gas without destroying the onion's flavour?
- **Act III — Shinsuke Imai's 2002 *Nature* Vial Twist: The Hidden Second Enzyme (`LFS`) (2002, UNVERIFIED):** In **October 2002** (*Nature* 419: 685, 17 Oct 2002), biochemist Shinsuke Imai and colleagues at House Foods Corporation in Chiba, Japan (with T. Nagata & H. Kumagai), mix purified garlic `alliinase` with the purified onion precursor (`isoalliin`) in a test tube — and discover **no tear gas forms at all**! Only when they add a previously unknown second onion protein — **lachrymatory-factor synthase (`LFS`)** — does `1-propenylsulfenic acid` twist into `(Z)`-propanethial *S*-oxide instead of condensing peacefully into savoury thiosulfinate flavour compounds.
- **Act IV — Atomic Crystal Structure & Tearless Onions (2008–2017, UNVERIFIED):** By silencing the `LFS` gene with RNA interference (`Colin C. Eady, S. Imai et al., 2008`, *Plant Physiology* 147: 2096–2106, Crop & Food Research New Zealand & House Foods, and later conventional cross-breeding of tearless `Sunions`) and solving the X-ray crystal structure of `LFS` bound to its substrate analog (`Josiah A. Silvaroli, Marcia E. Newcomer et al., 2017`, *ACS Chemical Biology* 12: 2097–2104), scientists prove that switching off `LFS` stops the tear gas while redirecting the sulfur intermediate into savoury flavour compounds that `LFS` used to steal.

---

## 5. Two Candidate Search-Titled Shorts (`Test B` / `Rule 26` / `Rule 32` — UNVERIFIED Concepts Only)

- **Short `S01`:** *Why Do Sliced Onions Make Your Eyes Water?* (`42 chars`, `0` exact collisions, positive search question)
  - **First-line answer hook (UNVERIFIED):** *"An uncut onion contains zero tear gas — until your knife blade smashes two microscopic vaults together inside its cells."*
  - **Frame-0 & Payoff Plan (`Rules 2, 3, 6, 24, 27`):** Frame 0 (`0.0s`, `mode: "cover"`): close moving shot of a steel knife slicing into a translucent onion cell as two glowing compartments burst together (`TWO VAULTS`, `#FFE000` on `TWO`). Payoff at `≥70%` runtime (`~17.0s / 23.5s`): Shinsuke Imai's 2002 *Nature* discovery that a hidden second enzyme (`LFS`) converts the harmless flavour acid into volatile `syn`-propanethial-*S*-oxide gas within milliseconds. Loop tail `<1.0s`, zero CTA.
- **Short `S02`:** *How Did Scientists Breed a Tearless Onion?* (`42 chars`, `0` exact collisions, positive search question)
  - **First-line answer hook (UNVERIFIED):** *"For 40 years, chemists thought you couldn't stop an onion making you cry without ruining its taste — until a 2002 vial test in Japan proved them wrong."*
  - **Frame-0 & Payoff Plan (`Rules 2, 3, 6, 24, 27`):** Frame 0 (`0.0s`, `mode: "cover"`): close moving shot of two clear laboratory glass vials beside a sliced onion, one steaming with golden tear-gas vapour and one completely clear (`SECOND ENZYME`, `#FFE000` on `SECOND`). Payoff at `≥70%` runtime (`~17.2s / 23.5s`): when Imai's team mixed onion fuel with `alliinase` alone, zero tear gas formed — proving a separate enzyme (`lachrymatory-factor synthase`) hijacks the flavour molecule, and silencing it yields a tearless onion. Loop tail `<1.0s`, zero CTA.
