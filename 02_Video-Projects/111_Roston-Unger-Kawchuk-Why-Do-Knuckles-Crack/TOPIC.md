# Topic Brief — `111_Roston-Unger-Kawchuk-Why-Do-Knuckles-Crack` (`HOS:111` Proposal)

> **RULE-E GO/NO-GO & RULE G STATUS (`J2922` / `J2925`, `2026-11-16`):**
> - **Rule-E Verdict (`J2925`):** **GO (`95 / 100` · `9.50 / 10` Opportunity Score)** — Pre-cleared in the History of Science waiting line (`jobs/WIP.json` `next_hos`) under **Rule G** (`active` has `4 / 4` HOS films: `008`, `009`, `010`, `013`). Nothing is started in production (`status.json` stages are all `todo`).
> - **Awaits Active WIP Slot & `facts` Lane:** All historical and scientific claims in this brief are **UNVERIFIED** working notes. Before any script is locked or VO is recorded, every claim must be backed by verbatim primary-source quotes in `SOURCES.md` and verified through the `facts` lane (`gemini-agy`) once an active HOS WIP slot opens.

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
  - **Shared pattern:** `002` and `004` together account for **`92.9%` (`1,997 / 2,149`) of all HOS long impressions** and **`86.7%` (`195 / 225`) of all HOS long views** because they sit inside core everyday/curriculum search queries backed by multi-million-view `TED-Ed` neighbours (`LEARNINGS.md` Rules 1, 15, 26), run `8.5–9.0 min` (`525–541s`), and open with concrete physical proof (`60–71%` at `0:15`, Rule 10). Meanwhile `006` shows that a concrete experiment hook holds strong retention (`66.54%` avg view %) once clicked, whereas its non-search statement title (`36` impressions in `10d`) starved it of search impressions.
- **3 Worst HOS Longs & What They Share (Hypotheses on Small N):**
  1. **`_C92tIJCk8A` (`001` *How Did We Discover Germs?*, `365s`)** — **`0.10` views/day** (`7` views in `73d`), `44` impressions, `6.82%` CTR, `48.08%` avg view %.
  2. **`frP_YrNShsU` (`003` *How Did We Discover X-rays?*, `426s`)** — **`0.10` views/day** (`5` views in `52d`), `41` impressions, `2.44%` CTR, `26.65%` avg view %.
  3. **`wwcjcFfC-5M` (`005` *The Tied Arm That Proved Your Blood Circulates*, `529s`)** — **`0.29` views/day** (`5` views in `17d`), `15` impressions, `20.00%` CTR, `9.24%` avg view %.
  - **Shared pattern:** Generic textbook-chapter questions without a specific everyday mystery (`001`, `003`) or apparatus-only statement titles that omit the search phrase (`005`, `15` impressions) fail to earn YouTube search/browse impressions (`15–44` lifetime impressions). **Lesson applied to `HOS:111`:** Lead verbatim with the exact signed-out autocomplete question (`Why Do Knuckles Crack?`, where `TED-Ed`'s *Why do your knuckles pop?* has `5.78M` views and `Vox` has `67.78M` views) and add the human/experimental hook (`(The 50-Year Self-Experiment)`).

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
  2. **`-3L6HzJ_d_4` (*What Is the Pasteur Swan Neck Flask Experiment?*, `19s`)** — **`6.74` views/day** (`128` views in `19d`), channel-best **`77.14%` stayed-to-watch (PASS `≥60%`)** and **`75.23%` avg view % (PASS `≥70%`)**, with **`92.9%` (`118 / 127`) of 28d views from YouTube search** (`LEARNINGS.md` Rules 28 & 32).
  3. **`AMSriTQ-lcQ` (*Are Marie Curie's Notebooks Still Radioactive?*, `22s`)** — **`15.22` views/day** (`274` views in `18d`), **`76.94%` avg view % (PASS `≥70%`)**, `22.66%` stayed-to-watch, `6` likes — alongside loop winners `pWySvZsneZg` (`9.79/d`, `137` views, **`112.43%` avg view % LOOP**) and `c2q7w0pgcn8` (`5.11/d`, `138` views, `43.52%` stayed, **`105.30%` avg view % LOOP**) and feed velocity #2 `PFj6172YU4Q` (`31.29/d`, `219` views, `62.95%` avg view %, `15.98%` stayed).
  - **Shared pattern:** Immediate physical or body-experiment questions (`cutting gold in half`, `Swan Neck Flask`, `radioactive notebooks`) where the viewer can picture the action in the first 2 seconds (`LEARNINGS.md` Rules 2, 18, 24, 27, 28, 32).
- **3 Worst HOS Shorts & What They Share (Hypotheses on Small N):**
  1. **`LanTHJckYx8` (*What other table has empty chairs?*, `26s`)** — **`0.07` views/day** (`4` views in `54d`), `33.33%` stayed-to-watch, `23.08%` avg view % (`6s / 26s`).
  2. **`zI_eD3vFWmE` (*The first X-ray showed a wedding ring*, `25s`)** — **`0.18` views/day** (`9` views in `49d`), `50.00%` stayed-to-watch, `64.00%` avg view %.
  3. **`CnHwX1L9XHg` (*Gallium sat where the table said*, `26s`)** — **`0.29` views/day** (`16` views in `56d`), `30.43%` stayed-to-watch, `33.45%` avg view %.
  - **Shared pattern:** Cryptic riddles (*What other table has empty chairs?*) and flat past-tense statements (*Gallium sat where the table said*, *The first X-ray showed a wedding ring*) omit the searchable subject noun and fail both Shorts-feed stayed-to-watch and YouTube search discovery (`LEARNINGS.md` Rules 1, 28, 32).

---

## 2. Overlap & Non-Duplication Check (`2026-11-16`)

Checked against:
- All folders in `02_Video-Projects/` (`000`–`018`, `099`–`101` on `main`),
- Open topic PRs `#572` (`102` Ozone Hole, `103` Why Is the Sky Blue), `#581` (`104` Speed of Light, `105` Venus Flytrap), `#588` / `#589` / `#591` (`106` Eels & Sargasso Sea, `107` Autumn Leaves & Chlorophyll), `#602` / `#603` / `#604` (`108` Why Is Ice Slippery, `109` Why Do Fingers Wrinkle in Water), and `#607` (`110` Why Do Onions Make You Cry),
- All `011`–`095` backlog entries in `00_Brand/Channel-Setup/VIDEO_BACKLOG.json` and `00_Brand/Channel-Setup/ideas/` (`003` covers Röntgen's 1895 discovery of X-rays; `079` covers Belchier, Duhamel, Wolff & Mellanby on bone growth and rickets; `109` covers why fingers wrinkle in water; **none** cover why knuckles crack, Roston & Haines's 1947 spring-loaded finger pull, Unsworth's 1971 bubble-collapse theory, Donald Unger's 50-year single-hand knuckle-cracking self-experiment, or Greg Kawchuk's 2015 cine-MRI proof of tribonucleation cavity formation).
- **Result:** **Zero overlap.**

---

## 3. Packaging, Why It Should Work & Search/Neighbour Evidence (`Rule 26` + `neighbours.py` + `public_search.py`)

- **Title A (Primary Proposal, `LEARNINGS.md` Rules 1, 15, 23, 26 — `52 chars`, `0` exact collisions):** `Why Do Knuckles Crack? (The 50-Year Self-Experiment)` *(50-char Rule 15 tightened option: `Why Do Knuckles Crack? (A 50-Year Self-Experiment)`)*
- **Title B (Test & Compare Arm 2, `Rule 23` — `48 chars ≤ 50`, `0` exact collisions):** `The 2015 MRI That Proved Why Your Knuckles Crack`
- **Title C (`Rule 26` Exact Phrase First — `57 chars ≤ 70`, `0` exact collisions):** `Why Do Knuckles Crack? How an MRI Reversed a 44-Year Myth`
- **One-Line Hook:** For 44 years, textbooks insisted the pop in your knuckle was a collapsing bubble — until one doctor cracked only his left hand for 50 years (`36,500` times) and a 2015 real-time MRI caught the exact millisecond of the sound and proved the textbooks had it backwards.
- **Why It Should Work (Past Winners & `LEARNINGS.md` Rules):**
  - Resembles top HOS longs **`002` Periodic Table (`AL_-qlWko_g`, `161` views, `2.73/d`, `1,160` impressions, `3.36%` CTR)** and **`004` Inside an Atom (`GHZDsiH7L7A`, `34` views, `1.10/d`, `837` impressions)** by starting verbatim with a massive signed-out autocomplete question (`"why do knuckles crack"`) where **`TED-Ed`'s own lesson (`IjiKUmfaZr4`, *Why do your knuckles pop?*) has `5,783,001` views** and **`Vox` (`n3IYmdy6d4Y`) has `67,776,939` views** (`Rules 1, 15, 23, 26`).
  - Fixes the packaging failure of **`005` Tied Arm (`wwcjcFfC-5M`, `15` impressions, `0.29/d`)**: both are human-hand anatomy experiments, but instead of hiding the topic behind an unfamiliar prop statement (*The Tied Arm...*), `HOS:111` puts the universal body question first (`Why Do Knuckles Crack?`) and pairs it with the 50-year self-experiment and the 2015 MRI reversal.
  - Resembles top HOS Shorts **`29bpGAI0wb8` (`1,227` views, `40.90/d`)**, **`PFj6172YU4Q` (`219` views, `31.29/d`)**, and **`-3L6HzJ_d_4` (`128` views, `77.14%` stayed PASS, `75.23%` avg view % PASS)** by putting a human hand and joint cavity at Frame 0 with positive search questions (`Rules 2, 8, 24, 27, 28, 30, 32`).
- **3-Way Thumbnail Test & Compare Plan (`LEARNINGS.md` Rules 11, 12, 14 + `THUMBNAIL_AND_TITLE_RULES.md` §2.1–2.B):**
  - **Thumb A (Hero Object — The Glowing Joint Bubble Inside the Finger):** Painted 3D house-style key art: a translucent anatomical cutaway of two finger bones being pulled apart on the right two-thirds, revealing a bright glowing silver-blue vapour cavity suddenly snapping open in the synovial gap; the Explorer small at lower left wincing; cream/gold serif text on the clear left band: `FORMING, NOT POPPING` (`3 words`, gold on `FORMING,`, zero overlap on the joint).
  - **Thumb B (`Rule 14` Bright High-Contrast Variant — Left Hand vs Right Hand After 50 Years):** Bright sunlit clinical study key art: Donald Unger's two unlabelled hands held up side by side in front of a bright X-ray light-box on the right — both finger joints identically healthy; Explorer small at lower left; serif text on the clear left band: `36,500 CRACKS` (`2 words`, gold on `36,500`, adding the concrete `36,500` number without repeating Title A's `"50-Year"` and keeping all text off the hero hands per `THUMBNAIL_AND_TITLE_RULES.md` §2.5 & §2.B.2).
  - **Thumb C (The 2015 Real-Time MRI Tube):** Painted 3D key art of a finger joint inside the glowing white bore of Greg Kawchuk's 2015 MRI scanner on the right, with a crisp acoustic waveform spike aligned to the dark cavity birth; Explorer small at lower left; serif text on the clear left band: `TEXTBOOKS WRONG` (`2 words`, gold on `WRONG`).
- **Signed-out YouTube Autocomplete (`2026-11-16`):**
  - `"why do knuckles crack"` → **`autocomplete = yes`** (`10` suggestions: `why do knuckles crack`, `why does cracking knuckles feel good`, `why is cracking knuckles bad`, `why does your knuckles crack`, `why do we crack knuckles`, `why do your knuckles pop`, `why do my knuckles pop`, `why do my knuckles not crack`, `why do you crack your knuckles`)
  - `"does cracking knuckles cause arthritis"` → **`autocomplete = yes`** (`does cracking knuckles cause arthritis`)
  - `"why do your knuckles pop"` → **`autocomplete = yes`** (`9` suggestions: `why do your knuckles pop`, `why do your joints pop`, `why do my knuckles pop`, `why does your knuckles crack`, `why do my joints pop`, `why do our knuckles crack`, `why do my knuckles crack`, `dr binocs why do your knuckles pop`, `why do my knuckles not crack`)
  - `"why do joints pop"`, `"synovial joints"`, & `"skeletal system bones joints"` → **`autocomplete = yes`** (in `evidence_2026-11-16_neighbours.json`)
- **Rule 26(a) Two Ranking Videos (`≥10,000` views, retrieved `2026-11-16`):**
  1. `Vox` — [`n3IYmdy6d4Y`](https://youtu.be/n3IYmdy6d4Y) *Here's what happens to your knuckles when you crack them* (**`67,776,939` views**)
  2. `TED-Ed` ★ — [`IjiKUmfaZr4`](https://youtu.be/IjiKUmfaZr4) *Why do your knuckles pop? - Eleanor Nelsen* (**`5,783,001` views**; plus `Doctor Mike` [`PAKaVmcOPBY`](https://youtu.be/PAKaVmcOPBY) **`6,910,969` views**, `Doctor Myro` [`YNbzxNmxn90`](https://youtu.be/YNbzxNmxn90) **`5,308,015` views**, `Matthew Harb, M.D` [`B3uL39b-9wo`](https://youtu.be/B3uL39b-9wo) **`4,850,525` views**, `The Iced Coffee Hour` [`sAg07qAM7Xc`](https://youtu.be/sAg07qAM7Xc) **`4,452,046` views**, `RehabMedicineUofA` [`BHEcQluSzmM`](https://youtu.be/BHEcQluSzmM) **`2,187,642` views**, `Institute of Human Anatomy` [`j43kNmg2x2U`](https://youtu.be/j43kNmg2x2U) **`1,814,225` views**, and `Peekaboo Kidz` [`ccLQYDVJB0A`](https://youtu.be/ccLQYDVJB0A) **`1,253,656` views**)
- **Neighbour Gate (`neighbours.py`):** **PASS (`6` strictly on-topic education videos `≥1,000,000` views, `TED-Ed/TED: yes`, `0` off-topic rows)** — saved in [`11_Upload-Package/evidence_2026-11-16_neighbours.json`](11_Upload-Package/evidence_2026-11-16_neighbours.json):
  1. `CrashCourse` — [`rDGqkMHPDqE`](https://youtu.be/rDGqkMHPDqE) *The Skeletal System: Crash Course Anatomy & Physiology #19* (**`6,877,432` views**, Tier 2)
  2. `TED-Ed` ★ — [`IjiKUmfaZr4`](https://youtu.be/IjiKUmfaZr4) *Why do your knuckles pop? - Eleanor Nelsen* (**`5,783,001` views**, Tier 1)
  3. `CrashCourse` — [`DLxYDoN634c`](https://youtu.be/DLxYDoN634c) *Joints: Crash Course Anatomy & Physiology #20* (**`4,388,768` views**, Tier 2)
  4. `TED-Ed` ★ — [`VVL-8zr2hk4`](https://youtu.be/VVL-8zr2hk4) *How your muscular system works - Emma Bryce* (**`3,268,946` views**, Tier 1)
  5. `Amoeba Sisters` — [`m26gr04HIVE`](https://youtu.be/m26gr04HIVE) *Skeletal System* (**`1,734,355` views**, Tier 2)
  6. `SciShow` — [`pqfK-GLNjgA`](https://youtu.be/pqfK-GLNjgA) *Why Do Joints Pop And Crack?* (**`1,192,035` views**, Tier 2)
  - Plus `4` additional strictly on-topic `<1M` education videos in `neighbours.json`: `TED-Ed` ★ [`1Qfmkd6C8u8`](https://youtu.be/1Qfmkd6C8u8) *How bones make blood - Melody Smith* (`987,420` views), `TED` ★ [`1Zh045t0xcE`](https://youtu.be/1Zh045t0xcE) *Why Healthy Bones Are About So Much More than Milk* (`411,542` views), `FuseSchool` [`NF51ioK6U14`](https://youtu.be/NF51ioK6U14) *Joints | Physiology | Biology* (`329,972` views), and `Cognito` [`jbuGFWsOSlw`](https://youtu.be/jbuGFWsOSlw) *KS3 Biology - Skeletal System - Structure of Bones* (`24,609` views).

---

## 4. Candidate 4-Act Discovery Outline & Fact-Check Guardrails (All Claims UNVERIFIED Pending `SOURCES.md` & `facts` Lane)

- **Cold Open (0:00–0:45, UNVERIFIED):** Pull or bend your finger far enough and it lets out a sharp crack — followed by a 20-minute refractory silence before it can pop again. From `0:05–0:15` (`Rule 10` / `Rule 30` visual proof-first hook), we see the physical apparatus directly: a human finger attached to a brass spring balance in front of a 1947 X-ray plate and inside the glowing bore of a 2015 cine-MRI scanner. For 44 years, doctors and textbooks taught that the sound was a gas bubble *collapsing* inside your joint fluid — until a real-time MRI scanner in 2015 filmed the pop at `3.2 frames per second` (`~310 ms/frame`) and proved the textbooks had it backwards.
- **Act I — Roston & Haines's 1947 Spring-Scale X-Ray Pull vs Unsworth's 1971 Collapse Theory (1947–1971, UNVERIFIED):** In **May 1947** (*Journal of Anatomy*, Vol. 81, Pt 2, pp. 165–173), J. B. Roston and R. Wheeler Haines at St Thomas's Hospital Medical School in London attach a human finger (`metacarpophalangeal joint`) to a spring balance in front of an X-ray machine, increasing axial tension kg by kg (`~7 kg` critical pull; exact per-subject force and joint-space separation values `~0.5 mm → ~1.8–2.5 mm` to be quote-verified in `SOURCES.md`) until the joint suddenly jumps apart with an audible crack and a dark radiolucent vapour "clear space" appears in the synovial fluid. Roston and Haines conclude the **sudden formation** of that low-pressure cavity makes the sound. Twenty-four years later, in **July 1971** (*Annals of the Rheumatic Diseases*, Vol. 30, No. 4, pp. 348–358), University of Leeds bioengineers Anthony Unsworth, Duncan Dowson, and Verna Wright build a mechanized finger-cracking rig and argue the opposite: that the loud crack comes from the rapid **collapse** of the vapour cavitation bubble, an explanation copied into medical and physics textbooks for the next 44 years.
- **Act II — Donald Unger's 50-Year Single-Hand Self-Experiment (1948–1998, UNVERIFIED):** Meanwhile, every child heard the warning that cracking your knuckles causes arthritis. To test his mother's warning, California allergist **Donald L. Unger** spends **50 years** cracking the knuckles of his left hand at least twice every day (`≥36,500` cracks) while leaving his right hand uncracked as a control (`WHO: Donald L. Unger — California physician`; exact birth/death years and 1998 letter wording in *Arthritis & Rheumatism* Vol. 41, No. 5, pp. 949–950 + 2009 Ig Nobel Prize in Medicine citation to be verified in `SOURCES.md`). X-raying and examining both hands after five decades, Unger finds neither hand has arthritis and there is zero difference between them.
- **Act III — Greg Kawchuk's 2015 Real-Time Cine-MRI Reverses 44 Years of Textbooks (2015, UNVERIFIED):** On **15 April 2015** (*PLOS ONE* 10(4): e0119470), University of Alberta rehabilitation scientist **Greg N. Kawchuk** and colleagues (Jerome Fryer, Jacob L. Jaremko, Hongbo Zeng, Laurent Rowe, Richard Thompson) recruit chiropractor Jerome Fryer — who can crack all ten MCP knuckles on demand — and place his fingers one by one inside a real-time **cine-MRI** scanner (`~3.2 frames per second` / `310 ms` per frame). As the joint surfaces resist separation and then suddenly spring apart, a dark gas-filled cavity forms by **tribonucleation** at the *exact frame* of the popping sound — and the cavity remains clearly visible inside the joint *after* the sound has finished, proving Roston and Haines (`1947`) were right about cavity inception and the 1971 total-collapse textbook story was wrong.
- **Act IV — The 20-Minute Refractory Timer & 2018 Acoustic Physics (2015–2018, UNVERIFIED):** Why can't you crack the same knuckle twice right away? Because the dissolved gas (predominantly carbon dioxide, ~80% of dissolved synovial gas) drawn out of the synovial fluid takes roughly **20 minutes** to redissolve back into solution. On **29 March 2018** (*Scientific Reports* 8:4605), Stanford / École Polytechnique engineers Vineeth Chandran Suja and Abdul I. Barakat mathematically model Rayleigh–Plesset acoustic radiation in the joint gap and show that a **partial (incomplete) radial collapse / pressure recovery** (`~30–40%` radius drop) of the newly nucleated cavitation bubble during inception can radiate the measured acoustic peak (`~65–83 dB`, to be exact-quote verified in `SOURCES.md`) while leaving a persistent microbubble visible on Kawchuk's `3.2 fps` MRI — reconciling both experiments.

---

## 5. Two Candidate Search-Titled Shorts (`Test B` / `Rule 26` / `Rule 32` — UNVERIFIED Concepts Only)

- **Short `S01`:** *Why Did One Doctor Crack Only His Left Hand for 50 Years?* (`57 chars`, `0` exact collisions, positive search question)
  - **First-line answer hook (`Rules 2, 8, 24, 27` — titled noun + action in `≤1.5 s`, UNVERIFIED):** *"One doctor cracked the knuckles of his left hand twice a day for 50 years — and never touched his right."*
  - **Frame-0 & Payoff Plan (`Rules 2, 3, 6, 24, 27`):** Frame 0 (`0.0s`, `mode: "cover"`): close moving shot of two hands held up side by side against a glowing X-ray light-box (`36,500 CRACKS`, `#FFE000` on `36,500`). Mid-Short `WHEN` stamp (`8.5–11.5s`, inside 16:9 band): `CALIFORNIA, 1998` (`2 words`, withholding the zero-arthritis payoff until `≥70%` runtime per `Rule 6`). Payoff at `≥70%` runtime (`~17.0s / 23.5s`): after `36,500` cracks on the left hand and zero on the right over five decades (`1998`, *Arthritis & Rheumatism*), X-rays showed both hands were identically healthy with zero arthritis. Loop tail `<1.0s`, zero CTA.
- **Short `S02`:** *What Actually Makes the Pop When You Crack a Knuckle?* (`53 chars`, `0` exact collisions, positive search question)
  - **First-line answer hook (`Rules 2, 8, 24, 27` — titled noun + action in `≤1.5 s`, UNVERIFIED):** *"Crack a knuckle inside an MRI scanner, and the pop isn't a bubble bursting."*
  - **Frame-0 & Payoff Plan (`Rules 2, 3, 6, 24, 27`):** Frame 0 (`0.0s`, `mode: "cover"`): close moving anatomical cutaway of two finger joint bones pulling apart as a dark gas cavity snaps open in the synovial fluid (`GAS CAVITY BIRTH`, `#FFE000` on `CAVITY`). Mid-Short `DATA` scale bar (`8.0–11.0s`, inside 16:9 band): `3.2 FRAMES / SEC MRI` (`4 words`, withholding the cavity-formation reversal until `≥70%` runtime per `Rule 6`). Payoff at `≥70%` runtime (`~17.2s / 23.5s`): Greg Kawchuk's **2015** cine-MRI proved the crack happens at the exact instant the vacuum cavity *forms* (`tribonucleation`), and the bubble stays floating in the joint for 20 minutes *after* the sound is over. Loop tail `<1.0s`, zero CTA.
