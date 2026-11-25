# Topic Brief — `129_Spencer-Boot-Randall-How-Was-The-Microwave-Invented` (`HOS:129` · Proposal in `next_hos`)

> **PROPOSAL STATUS (`J3270` -> `J3347` Rule-E GO `96.4 / 100`, `2026-11-22`):**
> - **Backlog & Rule G:** Added to History of Science backlog (`jobs/WIP.json` `next_hos`) and **Rule-E pre-cleared (`GO`, `96.4 / 100` · `9.64 / 10` Opportunity Score, `J3347`)** in [`11_Upload-Package/TOPIC_GO_NO_GO_SHEET.md`](11_Upload-Package/TOPIC_GO_NO_GO_SHEET.md). Under **Rule G**, `active` holds `4 / 4` HOS films (`008`, `009`, `010`, `013`), so nothing enters production until a slot opens (`status.json` stages remain `todo`; `£0.00` spent).
> - **2027 Search Plan Fit (`J3224`, pending Ben's OK in `studio/plan.json`):** Directly serves **Cluster 3 — Accidental & World-Changing Inventions** from `05_Analytics/hos/search_research/2026-11-20.md` (`hos-search-2027-01`, currently `needsBen` under `LEARNINGS.md` rule 34 item 7): explosive growth (`accidental discoveries` `+93.0%` comp `39`, `accidental inventions that changed the world` `+73.9%`, `inventions that changed the world` `35,881`/mo **US 23%**), **9/10–10/10 US SERP gap**, verified sub-50k US breakouts (`Counter Facts Lab` `1.4K` → `1.5K` `22×`, `Invention Flex` `6.2K` US → `9.6K` `8.3×`, `Industrial Case Files` `138` US → `4.7K` `8.6×`), plus a wide-open signed-out YouTube SERP on `percy spencer microwave` where positions `#2–#4` sit at `224–795` views. Independently passes every currently in-force HOS topic gate (`neighbours.py PASS`, `public_search.py` autocomplete + `0` collisions).
> - **Strict Unverified Claims Guard:** All historical and scientific claims in this brief are **UNVERIFIED** working notes. Before any script is locked, VO is recorded, or picture credit is spent, every claim, date, and number must be backed by verbatim primary-source quotes in `SOURCES.md` and verified through the `facts` lane (`gemini-agy`).

---

## 1. HOS Data Comparison (`2026-11-22` Snapshot + `studio_ctr.json` + `channel_daily.json`)

- **Data sources read:**
  - `05_Analytics/hos/snapshots/2026-11-22.json` (`takenAt: 2026-11-22T06:40:31.126Z`, `42` public videos = `7` longs + `35` Shorts, `4,422` total views, `6` subscribers)
  - `05_Analytics/hos/studio_ctr.json` (`readAt: 2026-11-22T07:12:32.334030+00:00`, lifetime Studio impressions, CTR, average view %, and Shorts stayed-to-watch %)
  - `05_Analytics/hos/channel_daily.json` (`through: 2026-11-20`) and `05_Analytics/hos/REPORT.md`
  - `05_Analytics/LEARNINGS.md` (rules 1–41)
- **Elapsed-day denominator (`age_days`):** `max((date(2026, 11, 22) - date.fromisoformat(publishedAt[:10])).days, 1)` (`views/day = views / age_days`).
- **Low-sample statistical caveat:** Five of `7` public HOS longs have `5–15` lifetime views (`17–69` impressions), and bottom-tier or `<48h` Shorts have `<100` Studio views. Inferences from `<100`-view rows are treated explicitly as **descriptive hypotheses**, not settled laws.

### 1a. All `7` Public HOS Longs — Ranked by Views/Day Since Publish (`2026-11-22`)

| Rank | Video ID | Film | Title | Published (`age_days`) | Length | Views (`2026-11-22`) | Views / Day | Studio Impressions | Studio CTR | Studio Avg View % | YTA 28d Views / Avg % |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| **1** | `AL_-qlWko_g` | `002` | *How Did We Discover the Periodic Table?* | `2026-09-17` (`66d`) | `541s` | **162** | **2.45/d** | **1,163** | `3.4%` | `21.2%` (`115s`) | `13v` / `23.3%` |
| **2** | `GHZDsiH7L7A` | `004` | *What's Inside an Atom? Mostly Empty Space* | `2026-10-15` (`38d`) | `525s` | **35** | **0.92/d** | **840** | `1.4%` | `23.5%` (`124s`) | `9v` / `55.0%` |
| **3** | `VbPubYd6Fbs` | `006` | *The Willow Tree That Was Made of Air* | `2026-11-05` (`17d`) | `532s` | **15** | **0.88/d** | `69` | `4.3%` | **48.1%** (`256s`) | `15v` / `48.2%` |
| **4** | `ETynHpIYLeY` | `007` | *How Was the First Vaccine Made? (And Why It's Named After a Cow)* | `2026-11-12` (`10d`) | `532s` | **7** | **0.70/d** | `43` | `4.7%` | `19.3%` (`103s`) | `7v` / `19.3%` |
| **5** | `wwcjcFfC-5M` | `005` | *The Tied Arm That Proved Your Blood Circulates* | `2026-10-29` (`24d`) | `529s` | **6** | **0.25/d** | `17` | `17.6%` | **7.8%** (`41s`) | `6v` / `7.8%` |
| **6** | `_C92tIJCk8A` | `001` | *How Did We Discover Germs?* | `2026-09-03` (`80d`) | `365s` | **7** | **0.09/d** | `45` | `6.7%` | `48.1%` (`176s`) | `0v` / `—` |
| **7** | `frP_YrNShsU` | `003` | *How Did We Discover X-rays?* | `2026-09-24` (`59d`) | `426s` | **5** | **0.08/d** | `43` | `2.3%` | `26.6%` (`114s`) | `3v` / `14.1%` |

- **3 Best HOS Longs & What They Share:**
  1. **`AL_-qlWko_g` (`002` *How Did We Discover the Periodic Table?*, `541s`):** **`2.45/d`** (`162v`), **`1,163` impressions** (`52.4%` of all HOS long impressions), `3.4%` CTR, `21.2%` Studio avg viewed (`70%` at `0:15`, `50%` at `0:30`).
  2. **`GHZDsiH7L7A` (`004` *What's Inside an Atom? Mostly Empty Space*, `525s`):** **`0.92/d`** (`35v`), **`840` impressions** (`37.8%` of all HOS long impressions), `1.4%` CTR, `23.5%` Studio avg viewed (`55.0%` 28d YTA; `62%` at `0:15`, `45%` at `0:30`).
  3. **`VbPubYd6Fbs` (`006` *The Willow Tree That Was Made of Air*, `532s`):** **`0.88/d`** (`15v`, low-N), `69` impressions, `4.3%` CTR, channel-best **`48.1%` Studio avg viewed (`256s / 532s`)**.
  - **What they share:** `002` and `004` drive **`90.2%` (`2,003 / 2,220`) of HOS long impressions** via plain search questions backed by big education neighbours (`Rules 1, 15, 26`) at `8.7–9.0 min` (`525–541s`), while `006` (`48.1%` avg viewed) shows a single physical bench-top surprise retains viewers once they click.
- **3 Worst HOS Longs & What They Share (Small-N Hypotheses):**
  1. **`frP_YrNShsU` (`003` *How Did We Discover X-rays?*, `426s`):** **`0.08/d`** (`5v` in `59d`), `43` impressions, `2.3%` CTR, `26.6%` Studio avg viewed.
  2. **`_C92tIJCk8A` (`001` *How Did We Discover Germs?*, `365s`):** **`0.09/d`** (`7v` in `80d`), `45` impressions, `6.7%` CTR, `48.1%` Studio avg viewed.
  3. **`wwcjcFfC-5M` (`005` *The Tied Arm That Proved Your Blood Circulates*, `529s`):** **`0.25/d`** (`6v` in `24d`), **`17` impressions**, `17.6%` CTR, **`7.8%` Studio avg viewed (`41s`)**.
  - **What they share:** Literary non-search statement titles (`005`, `17` impr) or generic textbook survey titles (`001`, `003`) with shorter `6–7 min` cuts (`Rules 10, 15, 26`).

### 1b. All `35` Public HOS Shorts — Ranked by Views/Day Since Publish (`2026-11-22`)

| Rank | Video ID | Title | Published (`age_days`) | Len | Views | Views/d | Stayed % | Avg % (`s`) | 28d Search | Likes |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **1** | `xzKoHg0E0_U` | *What Is Dalton's Atomic Theory?* | `2026-11-16` (`6d`) | `25s` | **232** | **38.67** | `51.9%` | `61.0%` (`15s`) | `182/208` | `0` |
| **2** | `29bpGAI0wb8` | *What happens if you keep cutting gold in half?* | `2026-10-16` (`37d`) | `25s` | **1,229** | **33.22** | `40.8%` | `44.1%` (`11s`) | `9/9` | `12` |
| **3** | `Wvjd8g0CpzE` | *The Blood Vessels Finer Than a Hair* | `2026-11-15` (`7d`) | `26s` | **217** | **31.00** | `14.6%` | `76.6%` (`20s`) | `15/215` | `3` |
| **4** | `Bks_JLId1ew` | *How Do Plants Make Oxygen?* | `2026-11-21` (`1d`) | `26s` | `21` | `21.00` | `—` | `—` | `—` | `0` |
| **5** | `PFj6172YU4Q` | *One Tight Band Proved Your Blood Goes Round* | `2026-11-08` (`14d`) | `27s` | `221` | `15.79` | `16.7%` | `61.5%` (`17s`) | `32/221` | `3` |
| **6** | `l8bxm9L3zl8` | *How Does a Blood Pressure Cuff Work?* | `2026-11-20` (`2d`) | `24s` | `27` | `13.50` | `36.0%` | `67.8%` (`16s`) | `—` | `0` |
| **7** | `AMSriTQ-lcQ` | *Are Marie Curie's Notebooks Still Radioactive?* | `2026-10-28` (`25d`) | `22s` | `274` | `10.96` | `22.7%` | `76.9%` (`17s`) | `41/274` | `6` |
| **8** | `OnJ8MFu0Mi0` | *How Did John Snow Stop Cholera?* | `2026-10-26` (`27d`) | `23s` | `231` | `8.56` | `29.6%` | `65.7%` (`15s`) | `27/231` | `8` |
| **9** | `pWySvZsneZg` | *Why Gold Foil Bounced Rutherford's Particles Back* | `2026-11-01` (`21d`) | `25s` | `137` | `6.52` | `37.2%` | **112.4%** (`28s`) | `82/137` | `2` |
| **10** | `oKqmnJNGiHg` | *How Was Phosphorus Discovered?* | `2026-10-21` (`32d`) | `23s` | `194` | `6.06` | `42.0%` | **88.3%** (`20s`) | `32/34` | `7` |
| **11** | `-3L6HzJ_d_4` | *What Is the Pasteur Swan Neck Flask Experiment?* | `2026-10-27` (`26d`) | `19s` | `139` | `5.35` | **78.7%** | **75.0%** (`14s`) | `129/138` | `1` |
| **12** | `cLKDiYP55J8` | *What Was the Edward Jenner Experiment?* | `2026-11-13` (`9d`) | `23s` | `47` | `5.22` | `43.5%` | `67.7%` (`16s`) | `40/43` | `0` |
| **13** | `clV6E10NLPw` | *The spray that stopped surgery killing patients* | `2026-10-20` (`33d`) | `25s` | `155` | `4.70` | `23.4%` | `57.8%` (`14s`) | `5/12` | `4` |
| **14** | `qOZgess30h0` | *Invisible life is still everywhere* | `2026-10-13` (`40d`) | `24s` | `169` | `4.22` | `25.1%` | `39.8%` (`10s`) | `1/1` | `5` |
| **15** | `c2q7w0pgcn8` | *Who Discovered Infrared Light?* | `2026-10-19` (`34d`) | `23s` | `138` | `4.06` | `43.5%` | **105.3%** (`24s`) | `8/9` | `1` |
| **16** | `BW_CFAX-mxc` | *Is the Heart a Pump?* | `2026-10-31` (`22d`) | `22s` | `89` | `4.05` | `32.9%` | `81.7%` (`18s`) | `25/89` | `1` |
| **17** | `Rl2uZ-KOTl8` | *Your Heart Pumps More Blood Than You Have* | `2026-10-30` (`23d`) | `25s` | `78` | `3.39` | `26.6%` | `53.6%` (`13s`) | `12/78` | `4` |
| **18** | `xHnIi9GqOsM` | *Why Do Veins Have Valves?* | `2026-11-05` (`17d`) | `23s` | `42` | `2.47` | `20.6%` | `61.5%` (`14s`) | `16/42` | `0` |
| **19** | `qW2OsD4mujc` | *The Four Elements Were Wrong* | `2026-11-03` (`19d`) | `24s` | `34` | `1.79` | `57.7%` | `192.6%` (`46s`) | `31/34` | `0` |
| **20** | `TbMMJSRKC3U` | *He said every eighth element repeats* | `2026-10-18` (`35d`) | `27s` | `62` | `1.77` | `25.5%` | `123.3%` (`33s`) | `5/5` | `1` |
| **21** | `LCZRHUyTiq0` | *What Are Cathode Rays?* | `2026-10-23` (`30d`) | `26s` | `49` | `1.63` | `29.8%` | `50.0%` (`13s`) | `10/12` | `2` |
| **22** | `iqToagXnjX0` | *Microbes in a drop of pond water* | `2026-09-06` (`77d`) | `25s` | `113` | `1.47` | `28.3%` | `77.9%` (`19s`) | `3/3` | `1` |
| **23** | `ChbsigHD5_o` | *How Do Plants Clean the Air?* | `2026-11-18` (`4d`) | `25s` | `5` | `1.25` | `—` | `11.3%` (`3s`) | `1/3` | `0` |
| **24** | `H1y0DXFVmw8` | *Germs don't cast a shadow* | `2026-09-06` (`77d`) | `25s` | `80` | `1.04` | `19.8%` | `59.5%` (`15s`) | `1/1` | `1` |
| **25** | `xgx2lYHhYZM` | *Why Is It Called a Vaccine?* | `2026-11-17` (`5d`) | `25s` | `4` | `0.80` | `100.0%` | `62.4%` (`16s`) | `3/4` | `0` |
| **26** | `xvanpsLeADE` | *How did Röntgen see bones without cutting* | `2026-09-26` (`57d`) | `25s` | `40` | `0.70` | `23.3%` | `50.3%` (`13s`) | `1/1` | `0` |
| **27** | `oowAOWTBoq0` | *How X-rays Were Discovered by Accident* | `2026-09-25` (`58d`) | `25s` | `32` | `0.55` | `47.6%` | `331.1%` (`83s`) | `5/5` | `1` |
| **28** | `nba0-f7PPeU` | *Why tellurium sat before iodine* | `2026-09-21` (`62d`) | `25s` | `34` | `0.55` | `60.7%` | `42.7%` (`11s`) | `3/3` | `1` |
| **29** | `nFQRWmpulTQ` | *He predicted a metal before it was found* | `2026-09-19` (`64d`) | `25s` | `34` | `0.53` | `66.7%` | `55.9%` (`14s`) | `0/0` | `0` |
| **30** | `8_Edn_HCi1s` | *Germs hitch a ride on you* | `2026-09-06` (`77d`) | `25s` | `38` | `0.49` | `34.4%` | `34.2%` (`9s`) | `6/6` | `0` |
| **31** | `uU12JA5rMWg` | *The periodic table's empty chairs* | `2026-09-18` (`65d`) | `25s` | `30` | `0.46` | `66.7%` | `58.8%` (`15s`) | `0/0` | `0` |
| **32** | `sILtQxgYQk8` | *A flask that proved germs come from outside* | `2026-09-06` (`77d`) | `25s` | `24` | `0.31` | `41.7%` | `36.7%` (`9s`) | `0/0` | `0` |
| **33** | `CnHwX1L9XHg` | *Gallium sat where the table said* | `2026-09-20` (`63d`) | `26s` | `16` | `0.25` | `30.4%` | `33.5%` (`9s`) | `0/0` | `0` |
| **34** | `zI_eD3vFWmE` | *The first X-ray showed a wedding ring* | `2026-09-27` (`56d`) | `25s` | `9` | `0.16` | `50.0%` | `64.0%` (`16s`) | `0/0` | `0` |
| **35** | `LanTHJckYx8` | *What other table has empty chairs?* | `2026-09-22` (`61d`) | `26s` | `4` | `0.07` | `33.3%` | `23.1%` (`6s`) | `0/0` | `0` |

- **3 Best HOS Shorts & What They Share (`≥100` Mature Studio Views):**
  1. **`xzKoHg0E0_U` (*What Is Dalton's Atomic Theory?*, `25s`):** **`38.67/d`** (`232v` in `6d`), **`51.9%` stayed (WATCH)**, `61.0%` avg viewed, `182/208` search.
  2. **`29bpGAI0wb8` (*What happens if you keep cutting gold in half?*, `25s`):** **`33.22/d`** (`1,229v` in `37d`), `40.8%` stayed, `44.1%` avg viewed, `12` likes.
  3. **`-3L6HzJ_d_4` (*What Is the Pasteur Swan Neck Flask Experiment?*, `19s`):** **`5.35/d`** (`139v`), **`78.7%` stayed (PASS)** and **`75.0%` avg viewed (PASS)**, `129/138` search — alongside loop/retention winners `pWySvZsneZg` (`112.4%` LOOP), `c2q7w0pgcn8` (`105.3%` LOOP, `43.5%` stayed), and `oKqmnJNGiHg` (`88.3%` PASS, `42.0%` stayed).
  - **What they share:** Named-entity positive search questions (`Rules 1, 28, 32, 41`), `19–25s` tight cuts with `≤1.0s` loop tails (`Rules 3, 6, 27`), and recognisable hero objects at Frame 0 (`Rule 24`), outperforming statement titles (`Wvjd8g0CpzE` `14.6%` stayed, `PFj6172YU4Q` `16.7%` stayed).
- **3 Worst HOS Shorts & What They Share (Small-N Hypotheses):**
  1. **`LanTHJckYx8` (*What other table has empty chairs?*, `26s`):** **`0.07/d`** (`4v`), `33.3%` stayed, `23.1%` avg viewed.
  2. **`zI_eD3vFWmE` (*The first X-ray showed a wedding ring*, `25s`):** **`0.16/d`** (`9v`), `50.0%` stayed, `64.0%` avg viewed.
  3. **`CnHwX1L9XHg` (*Gallium sat where the table said*, `26s`):** **`0.25/d`** (`16v`), `30.4%` stayed, `33.5%` avg viewed.
  - **What they share:** Cryptic riddles or flat past-tense statements with zero searchable subject noun (`Rules 1, 28, 32, 41`), `25–26s` legacy cuts, and zero search capture.

---

## 2. Overlap & Non-Duplication Check (`2026-11-22`)

Checked against:
- All `02_Video-Projects/` folders on `main` (`000`–`018`, `099`–`119`),
- Open HOS topic PRs `#659` (`120–121`), `#682` (`122–123`), `#689` (`124–125`), `#706` (`126–127`), `#724`/`#725` (`128` *Why Do We Use AC Instead of DC?*), and `#726` (`130` nuclear reactor, `131` theory of relativity),
- All `011`–`095` folders in `00_Brand/Channel-Setup/ideas/`, `VIDEO_BACKLOG.json`, and `jobs/WIP.json` (`018` covers Herschel & Ritter's 1800–1801 infrared/UV discovery; `042` covers Maiman & Kao's laser and fibre optics — **none** cover the 1940 Birmingham cavity magnetron by John Randall & Harry Boot, Percy Spencer's 1945 Raytheon melted candy-bar accident, his popcorn and exploding-egg bench tests, the 1947 Radarange, or dielectric heating of water molecules inside a microwave oven).
- **Result:** **Zero overlap.**

---

## 3. Packaging, Why It Should Work & Search/Neighbour Evidence (`Rule 26` + `neighbours.py` + `public_search.py`)

- **Title A (Primary Proposal, `LEARNINGS.md` Rules 1, 15, 23, 26 — `50 chars ≤ 50`, `0` exact collisions):** `How Was the Microwave Invented? (A Radar Accident)`
- **Title B (T&C Arm 2, `Rules 15, 23, 26` — `49 chars ≤ 50`, `0` exact collisions):** `How Does a Microwave Work? (The 1945 Radar Twist)`
- **Title C (`Rule 26` Exact Search Phrase + Named Person & Apparatus — `64 chars ≤ 70`, `0` exact collisions):** `How Was the Microwave Invented? (Percy Spencer's 1945 Magnetron)`
- **One-Line Hook:** In 1945, self-taught Raytheon engineer Percy Spencer stepped in front of a wartime radar magnetron, felt a peanut candy bar melt inside his pocket — and turned a secret British anti-submarine weapon into the box sitting on nearly every kitchen counter on Earth.
- **Why It Should Work (Past Winners, `J3224` & `LEARNINGS.md` Rules):**
  - Resembles top HOS longs **`002` Periodic Table (`AL_-qlWko_g`, `162v`, `2.45/d`, `1,163` impr, `3.4%` CTR)** and **`004` Inside an Atom (`GHZDsiH7L7A`, `35v`, `0.92/d`, `840` impr)** by opening with an exact, universal kitchen-counter question (`How Was the Microwave Invented?`, `50 chars ≤ 50`) backed by `3` strictly on-topic `≥1M` education neighbours (`0` off-topic `≥1M` rows: `Tom Scott` `8.96M`, `TED-Ed` ★ `2.11M`, `SciShow` `1.33M`; `Rules 1, 15, 26`), while pairing that query with a vivid, humorous bench-top accident (melted candy bar → exploding egg → popcorn) that holds retention like **`006` Willow Tree (`48.1%` Studio avg viewed)**.
  - Directly targets **Cluster 3 — Accidental & World-Changing Inventions** (`J3224`: `accidental discoveries` `+93.0%` comp `39`, `inventions that changed the world` `US 23%`, `9/10–10/10` US SERP gap, and `percy spencer microwave` showing `224–795` view videos right in the top 5!).
  - Resembles top HOS Shorts **`xzKoHg0E0_U` (`38.67/d`, `51.9%` stayed)**, **`29bpGAI0wb8` (`1,229v`, `33.22/d`)**, **`-3L6HzJ_d_4` (`78.7%` stayed PASS, `75.0%` avg viewed PASS, `19s`)**, and **`oKqmnJNGiHg` (`88.3%` PASS)** — especially `S02` (*Why Can't You Put Metal in a Microwave Oven?*), which mirrors a `2.11M` TED-Ed + `1.33M` SciShow + `5.80M` ElectroBOOM search question inside Ben's 19 Nov `16–19s` looping 3D-cartoon format (`Rules 2, 3, 6, 24, 27, 28, 32, 39, 41`).
- **3-Way Thumbnail Test & Compare Plan (`LEARNINGS.md` Rules 11, 12, 14 + `THUMBNAIL_AND_TITLE_RULES.md` §2.5 & §2.B — refined in `J3347`):**
  - **Thumb A (Hero Moment — Melted Bar Beside the Brass Magnetron):** Painted 3D house-style key art: on a 1945 Raytheon wooden lab bench on the right two-thirds, a glowing copper wartime cavity magnetron emits warm shimmering concentric waves toward a melting chocolate-peanut bar and a kernel bursting into popcorn; Explorer small at lower left; cream/gold serif text on clear left band: `MELTED CANDY BAR` (`3 words`, gold on `MELTED`, zero word overlap with Titles A/B/C per §2.5, concretely names the hero object per §2.B.1, zero overlap on hero, no AI text; replaced draft `RADAR ACCIDENT` which repeated Title A/B).
  - **Thumb B (`Rule 14` Bright High-Contrast Kitchen Cutaway — Water Molecules Spinning):** Bright sunlit modern kitchen cutaway of a humming microwave oven whose glass door reveals spinning blue-and-red polar water molecules driven by an electric field oscillating through `2.45 billion` full wave cycles per second (`4.9 billion` polarity reversals/s) beside a glowing copper magnetron behind the wall; Explorer small at lower left; left band serif text: `2.45 BILLION/SEC` (`2 tokens`, gold on `2.45`, zero overlap with Titles A/B/C).
  - **Thumb C (The Exploding Egg Experiment):** Painted 3D key art of a brass metal box with a hole cut in the side on Spencer's lab bench as a whole egg bursts mid-air inside a glowing microwave beam; Explorer small at lower left; left band serif text: `THE EGG EXPLODED` (`3 words`, gold on `EXPLODED`, zero overlap with Titles A/B/C, concretely names the hero object per §2.B.1; replaced draft pronoun teaser `IT EXPLODED`).
- **Signed-Out YouTube Autocomplete (`2026-11-22`, `10` queries saved in [`11_Upload-Package/evidence_2026-11-22_public_search.json`](11_Upload-Package/evidence_2026-11-22_public_search.json)):**
  - `"how was the microwave invented"` → **`autocomplete = yes`**
  - `"how does a microwave work"` → **`autocomplete = yes`**
  - `"who invented the microwave"` → **`autocomplete = yes`**
  - `"percy spencer microwave"` → **`autocomplete = yes`**
  - `"why can't you put metal in a microwave"` → **`autocomplete = yes`**
  - **Exact title collisions:** **`0`** across Titles A, B, C and Shorts S01, S02.
- **Rule 26(a) Two Ranking Videos (`≥10,000` views, retrieved `2026-11-22`):**
  1. `Tom Scott` — [`2tdiKTSdE9Y`](https://youtu.be/2tdiKTSdE9Y) *I promise this story about microwaves is interesting.* (**`8,957,052` views**)
  2. `engineerguy` — [`kp33ZprO0Ck`](https://youtu.be/kp33ZprO0Ck) *How a Microwave Oven Works* (**`5,389,161` views**; plus `Sabin Civil Engineering` **`8,011,520`**, `ElectroBOOM` `OyTmJX_TC84` **`5,795,769`**, `TED-Ed` `ZExGV6jSuBw` **`2,114,632`**, `SciShow` `ZqAZz-JhvYA` **`1,329,055`**, `Peekaboo Kidz` `qCRm503O0po` **`1,071,628`**, `Weird History Food` `UJBZk88O6BU` **`340,942`**)
- **Neighbour Gate (`neighbours.py "how does a microwave work" "microwave oven" "why can't you put metal in a microwave" --top 25`):** **PASS (`3` raw / `3` strictly on-topic education videos `≥1,000,000` views, `TED-Ed/TED: yes`, `0` off-topic `≥1M` rows)** — saved in [`11_Upload-Package/evidence_2026-11-22_neighbours.json`](11_Upload-Package/evidence_2026-11-22_neighbours.json):
  1. `Tom Scott` — [`2tdiKTSdE9Y`](https://youtu.be/2tdiKTSdE9Y) *I promise this story about microwaves is interesting.* (**`8,957,052` views**, Tier 2)
  2. `TED-Ed` ★ — [`ZExGV6jSuBw`](https://youtu.be/ZExGV6jSuBw) *Why can't you put metal in a microwave? - Aaron Slepkov* (**`2,114,636` views**, Tier 1)
  3. `SciShow` — [`ZqAZz-JhvYA`](https://youtu.be/ZqAZz-JhvYA) *Why Can't I Put Metal in the Microwave?* (**`1,329,055` views**, Tier 2; plus `National Geographic` `l_M5HzWlM40` **`56,191` views** *Microwave Oven | I Didn't Know That*)

---

## 4. Candidate 4-Act Discovery Outline (All Claims UNVERIFIED Pending `SOURCES.md` & `facts` Lane)

- **Cold Open (`0:00–0:45`, Proof-First Apparatus Window per `Rules 10 & 30`, UNVERIFIED):**
  - `0:00–0:05`: A glowing copper disc machined with six circular cavities — a 1940 wartime radar tube — sits humming on a laboratory bench as a chocolate-peanut candy bar melts inside an engineer's coat pocket (`0:05–0:15`, apparatus proof; zero *"In this film..."* agenda line).
  - `0:15–0:45`: The machine that reheats your dinner wasn't designed for cooking at all: it began as a top-secret British radar breakthrough in 1940, nearly exploded an egg in an engineer's colleague's face in 1945, and uses invisible waves flipping water molecules billions of times a second.
- **Act I — John Randall, Harry Boot & the 1940 Birmingham Cavity Magnetron (1940, UNVERIFIED):** Early radar sets used long radio waves that required giant antennas too big for aircraft. In **February 1940** at the **University of Birmingham**, physicists **John Randall** and **Harry Boot** machined a solid block of copper with resonant cylindrical cavities and placed it inside a magnetic field — creating the **cavity magnetron**, which produced powerful centimetre-wavelength microwaves (`~10 cm` initially) hundreds of times stronger than earlier tubes. Secretly carried to the United States in a black metal box during the **Tizard Mission (autumn 1940)**, it became one of the most consequential laboratory devices of the twentieth century, and Raytheon in Massachusetts was contracted to mass-produce it.
- **Act II — Percy Spencer's Melted Candy Bar, Popcorn & Exploding Egg (1945, UNVERIFIED):** Self-taught Raytheon engineer **Percy Spencer** (who had left school as a boy to work in a mill and taught himself physics and calculus) figured out how to stamp magnetrons out rapidly instead of hand-machining every block. In **1945**, while standing beside an active magnetron test rig in Waltham/Newton, Massachusetts, Spencer noticed a **peanut cluster candy bar** in his pocket had melted into warm goo. Curious rather than alarmed, he sent out for **unpopped popcorn kernels** — which popped all over the lab floor — and then placed a **whole egg** inside a metal kettle with a hole cut in the side, where steam pressure built inside the shell until the egg exploded in a curious colleague's face.
- **Act III — The Physics Twist: Dielectric Heating, Standing Waves & Metal (1945–1947, UNVERIFIED):** How can an invisible wave heat food while the air and ceramic plate stay cool? Unlike a conventional oven that heats from the outside in, a domestic microwave oven operating in the **2.45 GHz** ISM radio band (`2.45 billion` full wave cycles per second = **`4.9 billion` electric-field polarity reversals per second**; *script guardrail: never call `2.45 GHz` a "resonant frequency of water" — it is a non-resonant ISM frequency chosen so waves penetrate several centimetres into food*) drives polar **water molecules** (plus fats and sugars) to twist back and forth via **dielectric heating / dipolar relaxation**, jostling neighbouring molecules into heat. On **8 October 1945**, Raytheon filed Spencer's patent (**US 2,495,429**, granted January 1950), enclosing the magnetron inside a reflective metal cavity — explaining both why a turntable is needed (to smooth out standing-wave hot and cold spots) and why smooth cavity walls safely reflect waves while thin sharp metal edges like forks or crumpled foil concentrate induced charge until the electric field breaks down the air into sparks.
- **Act IV — From the 750-Pound Radarange to the Kitchen Counter (1947–1967, UNVERIFIED):** Raytheon's first commercial microwave oven, the **1947 Radarange**, stood nearly **six feet tall**, weighed roughly **750 pounds (340 kg)**, needed water plumbing to cool its magnetron, and cost several thousand dollars — confining it to ships, trains, and restaurants. It took another two decades of compact air-cooled magnetron engineering before **Amana** (acquired by Raytheon) launched the countertop **Radarange RR-1 in 1967** (`~$495`), turning a wartime copper radar tube into one of the most familiar appliances in human history.

---

## 5. Two Candidate Search-Titled Shorts (`Ben 19 Nov 16–19s Rules` + `Rules 32 & 41` — UNVERIFIED Concepts Only)

- **Short `S01`:** *How Did Percy Spencer Accidentally Invent the Microwave?* (`56 chars`, `0` exact collisions, named-entity search question)
  - **First-line answer hook (`≤1.5s`, zero dateline opener per `Rule 39`, UNVERIFIED):** *"Percy Spencer invented the microwave oven when a radar tube melted a candy bar in his pocket."*
  - **16–19 s House-Rules Plan (`Ben 19 Nov` + `Rules 2, 3, 6, 24, 27, 41`):** Frame 0 (`0.0s`, 3D cartoon moving plate, `0%` Explorer, `0%` bars): a glowing copper cavity magnetron humming on a bench beside a melting chocolate-peanut bar and popping corn kernels; line-1 concrete-fact caption: `A radar tube melted his candy bar` (yellow keyword `RADAR TUBE`, never a two-word ALL CAPS stamp). Single `Teach on screen` WHEN stamp (`MASSACHUSETTS, 1945`, inside `16:9` band, clear of `0–2s` and `9–14s`). Payoff at `≥70%` (`~13.0s / 18.0s`): Spencer aimed the magnetron into a sealed metal box to trap the waves, filing the first microwave oven patent and turning a wartime radar tube into a kitchen appliance. Seamless `16–19s` spoken & visual loop into Frame 0, zero CTA.
- **Short `S02`:** *Why Can't You Put Metal in a Microwave Oven?* (`44 chars`, `0` exact collisions, exact `autocomplete = yes` named-device search question)
  - **First-line answer hook (`≤1.5s`, zero dateline opener per `Rule 39`, UNVERIFIED):** *"A microwave's own walls are made of metal — yet a fork inside it bursts into sparks."*
  - **16–19 s House-Rules Plan (`Ben 19 Nov` + `Rules 2, 3, 6, 24, 27, 41`):** Frame 0 (`0.0s`, 3D cartoon moving plate, `0%` Explorer, `0%` bars): close 3D view inside a glowing metal microwave cavity as blue electric arcs jump between the sharp prongs of a fork; line-1 concrete-fact caption: `Your microwave's walls are metal` (yellow keyword `ARE METAL`). Single `Teach on screen` DATA overlay (`2.45 BILLION CYCLES/S`, inside `16:9` band). Payoff at `≥70%` (`~13.0s / 18.0s`): smooth metal walls safely bounce microwaves back into your food, but on thin fork tines or crumpled foil, oscillating electrons crowd onto sharp points until voltage strips the air into plasma sparks. Seamless `16–19s` spoken & visual loop into Frame 0, zero CTA.
