# Topic Brief — `128_Edison-Tesla-Westinghouse-Why-Do-We-Use-AC-Instead-Of-DC` (`HOS:128` · Proposal in `next_hos`)

> **PROPOSAL & RULE-E REVIEW STATUS (`J3270` -> `J3346`, `2026-11-22`):**
> - **Rule-E Verdict (`J3346`, `2026-11-22`):** **GO (`97.1 / 100` · `9.71 / 10` Opportunity Score)** — pre-cleared in `jobs/WIP.json` `next_hos` under **Rule G** (`4 / 4` active HOS slots full: `008`, `009`, `010`, `013`). Nothing enters script lock, VO, or picture spend until an active HOS WIP slot opens (`status.json` stages remain all `todo`; `£0.00` spent). See [`11_Upload-Package/TOPIC_GO_NO_GO_SHEET.md`](11_Upload-Package/TOPIC_GO_NO_GO_SHEET.md) and [`11_Upload-Package/TOPIC_OPPORTUNITY_SCORE.md`](11_Upload-Package/TOPIC_OPPORTUNITY_SCORE.md).
> - **2027 Search Plan Fit (`J3224`, proposed / `needsBen` in `studio/plan.json`):** Directly serves **Cluster 1 — Electricity, Inventors & Famous Rivalries (Lead Film 1)** from `05_Analytics/hos/search_research/2026-11-20.md` (`hos-search-2027-01`, pending Ben's OK per `LEARNINGS.md` rule 34 item 7): US-led Anglosphere adult demand (`thomas edison` `28,672`/mo **US 30%**, `nikola tesla documentary` `29,205`/mo comp `37`, `thomas edison vs nikola tesla` `4,071`/mo comp `44`), **9/10 US SERP gap**, and verified sub-50k US breakouts (`Business History Podcast` `5.9K` → `92.9K` `48×`; `Real-World Learning` `36.8K` → `13.2K` `8.5×`; `RELIQUARY ARCHIVES` `29` subs → `2.1K` `13×`). Independently passes all currently in-force HOS topic gates (`neighbours.py`, `public_search.py`, `Rule E`, `Rule 26`).
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
  - **What they share (subject, title shape, opening, thumbnail concept, length):** `002` and `004` generate **`90.2%` (`2,003 / 2,220`) of all HOS long impressions** and **`83.1%` (`197 / 237`) of all HOS long views** because both open with plain, high-demand search questions backed by massive education neighbour pools (`Rules 1, 15, 26`), run **`8.7–9.0 min` (`525–541s`)**, pair one physical mystery/apparatus in the opening `15s` (`Rule 10`), and feature a single focal object on painted 3D key art. `006` (`48.1%` avg viewed) shows that one unforgettable physical experiment holds viewers once clicked, while its low impressions (`69`) prove that a literary title without a search phrase starves reach.
- **3 Worst HOS Longs & What They Share (Small-N Hypotheses):**
  1. **`frP_YrNShsU` (`003` *How Did We Discover X-rays?*, `426s`):** **`0.08/d`** (`5v` in `59d`), `43` impressions, `2.3%` CTR, `26.6%` Studio avg viewed.
  2. **`_C92tIJCk8A` (`001` *How Did We Discover Germs?*, `365s`):** **`0.09/d`** (`7v` in `80d`), `45` impressions, `6.7%` CTR, `48.1%` Studio avg viewed.
  3. **`wwcjcFfC-5M` (`005` *The Tied Arm That Proved Your Blood Circulates*, `529s`):** **`0.25/d`** (`6v` in `24d`), **`17` impressions** (channel floor), `17.6%` CTR (3 clicks on 17 impressions), **`7.8%` Studio avg viewed (`41s`)**.
  - **What they share:** `005` used a literary statement title with no search query (`Rule 26` miss), getting only `17` impressions, while `001` (`365s`) and `003` (`426s`) used broad textbook survey titles (`How Did We Discover...`), shorter `6–7 min` runtimes, and Premiere launches (`Rules 10, 15, 26`). (`007` Vaccine also stalled at `43` impressions / `7` views and `0%` Suggested, reinforcing `J3224`'s warning to steer clear of health/vaccine sensitivity.)

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
  1. **`xzKoHg0E0_U` (*What Is Dalton's Atomic Theory?*, `25s`):** **`38.67/d`** (`232v` in `6d`, #1 views/day), **`51.9%` stayed (WATCH, #2 mature)**, `61.0%` avg viewed, **`182 / 208` (`87.5%`) from YouTube search**.
  2. **`29bpGAI0wb8` (*What happens if you keep cutting gold in half?*, `25s`):** **`33.22/d`** (`1,229v` in `37d`, #1 total views), `40.8%` stayed, `44.1%` avg viewed, `12` likes.
  3. **`-3L6HzJ_d_4` (*What Is the Pasteur Swan Neck Flask Experiment?*, `19s`):** **`5.35/d`** (`139v` in `26d`), channel-best **`78.7%` stayed (PASS `≥60%`)** and **`75.0%` avg viewed (PASS `≥70%`)**, **`129 / 138` (`93.5%`) search** — the only mature `≥100v` HOS Short passing both targets, and notably the **only `19s` Short** (matching Ben's 19 Nov `16–19s` Shorts rule!), backed by loop/retention winners `pWySvZsneZg` (`112.4%` LOOP, `37.2%` stayed), `c2q7w0pgcn8` (`105.3%` LOOP, `43.5%` stayed), and `oKqmnJNGiHg` (`88.3%` PASS, `42.0%` stayed).
  - **What they share:** Named-entity positive search questions (`Dalton's Atomic Theory`, `Pasteur Swan Neck Flask`, `Rutherford's Gold Foil`, `Infrared Light`, `Phosphorus`; `Rules 1, 28, 32, 41`), tight `19–25s` pacing with `≤1.0s` loop tails and zero CTA (`Rules 3, 6, 27`), and concrete physical objects at Frame 0 (`Rule 24`). By contrast, statement-titled feed Shorts (`Wvjd8g0CpzE` `14.6%` stayed, `PFj6172YU4Q` `16.7%` stayed) lost 83–85% of feed viewers in the first 2 seconds.
- **3 Worst HOS Shorts & What They Share (Small-N Hypotheses):**
  1. **`LanTHJckYx8` (*What other table has empty chairs?*, `26s`):** **`0.07/d`** (`4v` in `61d`), `33.3%` stayed, `23.1%` avg viewed (`6s`).
  2. **`zI_eD3vFWmE` (*The first X-ray showed a wedding ring*, `25s`):** **`0.16/d`** (`9v` in `56d`), `50.0%` stayed, `64.0%` avg viewed.
  3. **`CnHwX1L9XHg` (*Gallium sat where the table said*, `26s`):** **`0.25/d`** (`16v` in `63d`), `30.4%` stayed, `33.5%` avg viewed (`9s`).
  - **What they share:** Cryptic riddles or flat past-tense statements with zero named searchable concept (`Rules 1, 28, 32, 41`), longer `25–26s` runtimes with legacy slow opens/CTAs (`Rules 3, 27`), and zero search capture (`0` 28d search views).

---

## 2. Overlap & Non-Duplication Check (`2026-11-22`)

Checked against:
- All `02_Video-Projects/` folders on `main` (`000`–`018`, `099`–`119`),
- Open HOS topic PRs `#659` (`120` *Why Do We Cry?*, `121` *Why Do Cats Purr?*), `#682` (`122` *Why Do We Sneeze?*, `123` *Why Does Hair Turn Grey?*), `#689` (`124` *Why Is the Ocean Salty?*, `125` *What Causes the Tides?*), and `#706` (`126` *What Is the Higgs Boson?*, `127` *How Do Airplanes Fly?*),
- All `011`–`095` folders in `00_Brand/Channel-Setup/ideas/`, `VIDEO_BACKLOG.json`, and `jobs/WIP.json` (`008` covers Franklin's 1752 lightning-electricity kite; `019` covers Galvani & Volta's 1800 voltaic pile; `021` covers Oersted & Faraday's 1820–1831 electromagnetic induction — **none** cover the 1882–1896 War of the Currents, Thomas Edison's Pearl Street DC grid, William Stanley's 1886 Great Barrington AC transformer, Nikola Tesla's 1888 polyphase AC induction motor, George Westinghouse's 1893 Chicago World's Fair lighting, or the 1895–1896 Niagara Falls AC transmission proof).
- **Result:** **Zero overlap.**

---

## 3. Packaging, Why It Should Work & Search/Neighbour Evidence (`Rule 26` + `neighbours.py` + `public_search.py`)

- **Title A (Primary Proposal, `LEARNINGS.md` Rules 1, 15, 23, 26 — `49 chars ≤ 50`, `0` exact collisions):** `Why Do We Use AC Instead of DC? (Edison vs Tesla)`
- **Title B (T&C Arm 2, `J3224` Cluster 1 Lead Shape, `Rule 23` — `61 chars ≤ 70`, `0` exact collisions):** `Thomas Edison vs Nikola Tesla: Why AC Won the War of Currents`
- **Title C (`Rule 26` Exact Search Phrase + Apparatus Twist — `58 chars ≤ 70`, `0` exact collisions):** `Why Do We Use AC Instead of DC? (The 1886 Transformer Bet)` *(refined in `J3346` from `1888` to `1886` so Stanley's March 1886 Great Barrington transformer proof is not conflated with Tesla's May 1888 induction-motor patents; `0` exact collisions verified `2026-11-22`)*
- **One-Line Hook:** In 1882, Thomas Edison lit up Lower Manhattan with direct current — yet his copper cables grew so thick that power died a mile from the plant, setting off a fierce battle with Nikola Tesla and George Westinghouse whose alternating-current transformers and spinning induction motor wired the entire planet.
- **Why It Should Work (Past Winners, `J3224` & `LEARNINGS.md` Rules):**
  - Resembles top HOS longs **`002` Periodic Table (`AL_-qlWko_g`, `162v`, `2.45/d`, `1,163` impr, `3.4%` CTR)** and **`004` Inside an Atom (`GHZDsiH7L7A`, `35v`, `0.92/d`, `840` impr)** by opening with an exact, high-demand everyday question (`Why Do We Use AC Instead of DC?`, `49 chars ≤ 50`) backed by `6` strictly on-topic electricity/Tesla education neighbours `≥1M` views (`Rules 1, 15, 26`), while adding the iconic Edison-vs-Tesla rivalry and concrete transformer/motor physics (`Rules 10, 23`, HOTU rivalry portrait cuts in `studio/RULES.md`) that keep viewers watching like **`006` Willow Tree (`48.1%` Studio avg viewed)**.
  - Directly targets **US/UK/CA/AU adult viewers** per `J3224` Cluster 1 (`thomas edison` `US 30%`, `nikola tesla documentary` `29,205`/mo comp `37`, `9/10` US SERP gap, sub-50k US breakouts `Business History Podcast` `5.9K → 92.9K` `48×`), escaping the low-RPM school-cram trap and vaccine throttling (`007` `43` impr).
  - Resembles top HOS Shorts **`xzKoHg0E0_U` (`38.67/d`, `51.9%` stayed)**, **`29bpGAI0wb8` (`1,229v`, `33.22/d`)**, and **`-3L6HzJ_d_4` (`78.7%` stayed PASS, `75.0%` avg viewed PASS, `19s`)** by pairing named-entity search questions (`Thomas Edison`, `Nikola Tesla`, `AC vs DC`) with Ben's 19 Nov `16–19s` 3D-cartoon frame-0 loop format (`Rules 2, 3, 6, 24, 27, 28, 32, 39, 41`).
- **3-Way Thumbnail Test & Compare Plan (`LEARNINGS.md` Rules 11, 12, 14 + `THUMBNAIL_AND_TITLE_RULES.md` §2.B):**
  - **Thumb A (Hero Apparatus — The Copper Cable vs Glowing Transformer):** Painted 3D house-style key art: on the right two-thirds, a glowing bronze AC step-up transformer sending crisp blue-gold arcs along thin wires across a city skyline while a massive, sagging bundle of thick DC copper cable overheats below; Explorer small at lower left; cream/gold serif text on clear left band: `1 MILE LIMIT` (`3 words`, gold on `1 MILE`, zero overlap on hero, no AI text).
  - **Thumb B (`Rule 14` Bright High-Contrast Rivalry Variant — Edison vs Tesla Split):** Bright sunlit 1893 Chicago World's Fair white-city pavilion glowing with thousands of AC bulbs, framed in sharp contrast between a DC pearl-street dynamo and a spinning brass AC induction rotor; Explorer small at lower left; left band serif text: `HIGH VOLTAGE` (`2 words`, gold on `HIGH`, zero words repeated from Titles A, B, or C per `THUMBNAIL_AND_TITLE_RULES.md` §2.5; refined in `J3346` from `AC BEAT DC`).
  - **Thumb C (Niagara Falls 1896 Transmission Proof):** Dramatic 3D painted cutaway of water plunging into Niagara's turbines driving giant blue-glowing Tesla-Westinghouse polyphase generators wired to distant Buffalo streetlights; Explorer small at lower left; left band serif text: `26 MILES AWAY` (`3 words`, gold on `26 MILES`).
- **Signed-Out YouTube Autocomplete (`2026-11-22`, `11` queries saved in [`11_Upload-Package/evidence_2026-11-22_public_search.json`](11_Upload-Package/evidence_2026-11-22_public_search.json)):**
  - `"why do we use ac instead of dc"` → **`autocomplete = yes`**
  - `"thomas edison vs nikola tesla"` → **`autocomplete = yes`**
  - `"war of the currents"` → **`autocomplete = yes`**
  - `"ac vs dc"` → **`autocomplete = yes`**
  - `"who invented alternating current"` → **`autocomplete = yes`**
  - **Exact title collisions:** **`0`** across Titles A, B, C and Shorts S01, S02.
- **Rule 26(a) Two Ranking Videos (`≥10,000` views, retrieved `2026-11-22`):**
  1. `ElectroBOOM` — [`S7C5sSde9e4`](https://youtu.be/S7C5sSde9e4) *Why Use AC Instead of DC at Home??* (**`6,686,558` views**)
  2. `AddOhms` — [`vN9aR2wKv0U`](https://youtu.be/vN9aR2wKv0U) *Difference between AC and DC Current Explained | AddOhms #5* (**`3,067,900` views**; plus `Discovery UK` `pcrwTN5OEZY` **`1,603,939`**, `Arvin Ash` `ag6ltdwqfms` **`1,472,705`**, `pharmacist` `Cidg4Xfpjmc` **`1,100,111`**, `Brain Station Advanced` `CCHGatqIkAI` **`697,871`**, `Naked Science` `lFa8Wydalyw` **`588,564`**)
- **Neighbour Gate (`neighbours.py "how electricity works" "ac vs dc" "edison" "nikola tesla inventions" --top 25`):** **PASS (`8` raw / `6` strictly on-topic education videos `≥1,000,000` views, `TED-Ed/TED: yes`)** — saved in [`11_Upload-Package/evidence_2026-11-22_neighbours.json`](11_Upload-Package/evidence_2026-11-22_neighbours.json):
  1. `Veritasium` — [`bHIhgxav9LY`](https://youtu.be/bHIhgxav9LY) *The Biggest Misconception About Electricity* (**`28,293,671` views**, Tier 2 — on-topic)
  2. `Veritasium` — [`oI_X2cMHNe0`](https://youtu.be/oI_X2cMHNe0) *How Electricity Actually Works* (**`12,838,937` views**, Tier 2 — on-topic)
  3. `TED-Ed` ★ — [`yc2-363MIQs`](https://youtu.be/yc2-363MIQs) *The science of static electricity - Anuradha Bhagwat* (**`3,624,109` views**, Tier 1 — on-topic)
  4. `Thoughty2` — [`egCsQXuBGkQ`](https://youtu.be/egCsQXuBGkQ) *Why This Secret Invention Drove Tesla Insane* (**`1,967,879` views**, Tier 2 — on-topic)
  5. `SciShow` — [`pPnGvjmIgZA`](https://youtu.be/pPnGvjmIgZA) *The Incredible Inventions of Nikola Tesla: Great Minds of Science* (**`1,401,838` views**, Tier 2 — on-topic)
  6. `TED-Ed` ★ — [`0SMNYivhGsc`](https://youtu.be/0SMNYivhGsc) *How inventions change history (for better and for worse) - Kenneth C. Davis* (**`1,041,472` views**, Tier 1 — on-topic)
  *(Two raw `≥1M` rows transparently excluded as off-topic: `Khan Academy` `vDwzmJpI4io` Elon Musk / Tesla Motors `6,972,397` and `TED-Ed` `z0M7_HPSi14` electric fish `3,643,082`. Additional on-topic neighbours `<1M`: `Simple History` `ty1Fk0JZfQk` `965,299`, `TED-Ed` ★ `MBRTR2dlwvA` `695,179`, `CrashCourse` `JoscDcbAjbY` `567,471` Electricity: Crash Course History of Science #27, `TED-Ed` ★ `tjwrG4Debc4` `476,489`, `TED` ★ `V-WkUKP1l3c` `346,459`, `FuseSchool` `tJSga2YamDc` `100,111` Alternating and Direct Current.)*

---

## 4. Candidate 4-Act Discovery Outline (All Claims UNVERIFIED Pending `SOURCES.md` & `facts` Lane)

- **Cold Open (`0:00–0:45`, Proof-First Apparatus Window per `Rules 10 & 30`, UNVERIFIED):**
  - `0:00–0:05`: A glowing filament bulb in 1882 Manhattan dims to orange as copper street cables heat up, cutting directly to a brass step-up transformer coil stepping voltage up so hair-thin wires carry power across an entire city (`0:05–0:15`, apparatus proof; zero *"In this film..."* agenda line).
  - `0:15–0:45`: Every wall socket in your home reverses direction 100 or 120 times every second (50 Hz in the UK/Europe, 60 Hz in the US — two direction reversals per full cycle) — because Thomas Edison's low-voltage direct current ran straight into Joule heating ($P_{\text{loss}} = I^2 R$, combined with Ohm's law $V = IR$), and a bitter ten-year engineering duel with Nikola Tesla and George Westinghouse decided how the modern grid works.
- **Act I — Edison's 1882 Pearl Street Station & the One-Mile Copper Trap (1882–1885, UNVERIFIED):** On **4 September 1882**, **Thomas Edison** switched on the Pearl Street Station in Lower Manhattan, lighting 110-volt direct-current bulbs for nearby customers. The catch was simple physics: at low voltage, sending power farther demanded huge current, and heating loss rises with the **square of current ($I^2 R$)** — meaning a DC station could barely reach about a mile without burying impossibly thick, expensive copper bars under every street.
- **Act II — Lucien Gaulard, William Stanley & the 1886 Great Barrington Transformer (1885–1886, UNVERIFIED):** Alternating current could solve the distance problem using a **transformer** — stepping voltage way up for long-distance transmission (slashing current and heat loss) and stepping it back down for safe indoor bulbs. After **Lucien Gaulard** and **John Dixon Gibbs** demonstrated secondary generators in Europe and **Otto Bláthy, Miksa Déri, and Károly Zipernowsky** refined the closed-core transformer in Budapest (1885), **George Westinghouse** hired **William Stanley**, who lit the streets and shops of **Great Barrington, Massachusetts on 20 March 1886** over a 4,000-foot line using stepped-up AC — yet AC still lacked a practical motor for factories.
- **Act III — Nikola Tesla's 1888 Polyphase Induction Motor & the War of the Currents (1888–1893, UNVERIFIED):** In **May 1888**, Serbian-born engineer **Nikola Tesla** patented his **polyphase alternating-current induction motor**, using out-of-phase AC coils to create a rotating magnetic field that spun a rotor with no sparking brushes. Westinghouse licensed Tesla's patents in July 1888, triggering the **War of the Currents**: Edison's camp campaigned publicly that high-voltage AC was lethal, culminating in Harold Brown's electrocution demonstrations and New York's 1890 adoption of an AC electric chair. The decisive public test came in **May 1893**, when Westinghouse underbid Edison's General Electric to illuminate the **Chicago World's Columbian Exposition** with roughly 100,000+ AC lamps powered by Tesla's polyphase generators.
- **Act IV — Niagara Falls & the 26-Mile Proof (1895–1896, UNVERIFIED):** The final verdict arrived at **Niagara Falls**. Westinghouse built the giant polyphase AC generators at the **Edward Dean Adams Power Plant** (first power in **1895**), and on **15–16 November 1896** alternating current travelled roughly **26 miles** over transmission lines to power the streetcars and lights of **Buffalo, New York** — proving long-distance AC power and setting the blueprint for every electrical grid on Earth (with a modern coda noting that ultra-high-voltage DC [HVDC] later returned for undersea interconnector cables once solid-state power electronics solved voltage conversion).

---

## 5. Two Candidate Search-Titled Shorts (`Ben 19 Nov 16–19s Rules` + `Rules 32 & 41` — UNVERIFIED Concepts Only)

- **Short `S01`:** *Why Couldn't Thomas Edison's DC Power Cross a City?* (`51 chars`, `0` exact collisions, named-entity search question)
  - **First-line answer hook (`≤1.5s`, zero dateline opener per `Rule 39`, UNVERIFIED):** *"Thomas Edison's direct-current wires lost so much heat that power died after one mile."*
  - **16–19 s House-Rules Plan (`Ben 19 Nov` + `Rules 2, 3, 6, 24, 27, 41`):** Frame 0 (`0.0s`, 3D cartoon moving plate, `0%` Explorer, `0%` bars): a glowing copper street cable overheating in 3D cutaway beside a dimming light bulb; line-1 concrete-fact caption: `Edison's DC died after 1 mile` (yellow keyword `1 MILE`, never a two-word ALL CAPS stamp). Single `Teach on screen` DATA/WHEN overlay (`I²R HEAT LOSS`, inside `16:9` band, clear of `0–2s` and `9–14s`). Payoff at `≥70%` (`~13.0s / 18.0s`): doubling voltage halves current and cuts wire heat loss by four — something only alternating-current transformers could do in the 1880s. Last line loops directly into line 1 (`≤0.3s` crossfade back to Frame 0, zero CTA).
- **Short `S02`:** *How Did Nikola Tesla's AC Beat Edison's DC?* (`43 chars`, `0` exact collisions, named-entity search question)
  - **First-line answer hook (`≤1.5s`, zero dateline opener per `Rule 39`, UNVERIFIED):** *"Nikola Tesla beat Edison's direct current by building a motor driven by a spinning magnetic field."*
  - **16–19 s House-Rules Plan (`Ben 19 Nov` + `Rules 2, 3, 6, 24, 27, 41`):** Frame 0 (`0.0s`, 3D cartoon moving plate, `0%` Explorer, `0%` bars): brass polyphase AC coils lighting in sequence around a spinning copper rotor with glowing magnetic field arcs; line-1 concrete-fact caption: `Tesla's AC spun without brushes` (yellow keyword `WITHOUT BRUSHES`). Single `Teach on screen` WHEN stamp (`NIAGARA, 1896`, inside `16:9` band). Payoff at `≥70%` (`~13.0s / 18.0s`): paired with Westinghouse's step-up transformers, Tesla's polyphase AC sent power 26 miles from Niagara Falls to Buffalo and won the world's power grid. Seamless `16–19s` spoken & visual loop into Frame 0, zero CTA.
