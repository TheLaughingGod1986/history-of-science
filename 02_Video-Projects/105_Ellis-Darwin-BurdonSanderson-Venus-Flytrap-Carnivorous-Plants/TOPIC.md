# Topic Brief — `HOS:105` (`105_Ellis-Darwin-BurdonSanderson-Venus-Flytrap-Carnivorous-Plants`)

> **PROPOSAL & UNVERIFIED CLAIMS NOTICE (`J2809` / `J2811`, 14 Nov 2026):**
> This topic (`HOS:105`) is a **pre-cleared backlog topic proposal (`jobs/WIP.json` `next_hos`, Rule G; `GO` `95 / 100` in `J2811`)** awaiting an open active HOS WIP slot (`4/4` currently full).
> - **All historical and scientific claims in §2 and §3 are UNVERIFIED working notes** and are **NOT CLEARED FOR NARRATION OR SHORT OPENS**.
> - `01_Script/episode_script_draft_v01.md` remains the blank template. Before any script lock, every claim, date, quote, electrical voltage/time constant, and touch-count number must be backed by an exact quote in `SOURCES.md` and verified through the `facts` lane (`gemini-agy`).

---

## Summary Table

| Field | Value |
|---|---|
| **Film ID & Folder** | `HOS:105` · `02_Video-Projects/105_Ellis-Darwin-BurdonSanderson-Venus-Flytrap-Carnivorous-Plants` |
| **Status** | Pre-cleared backlog proposal (`jobs/WIP.json` `next_hos`, Rule G) · Rule-E Topic Review **`GO` (`95 / 100`, `J2811`)** · `status.json` all stages `todo` until an active HOS WIP slot opens |
| **Title A (Primary Proposal, Rule 26)** | `How Do Venus Flytraps Work? (The Plant That Counts to Five)` (`59 chars`, `0` exact collisions; `≤50`-char Rule 15 variant: `How Do Venus Flytraps Work? (Counting to Five)`, `46 chars`, `0` exact collisions) |
| **Title B (Test & Compare, Rule 15 + Rule 23, disambiguated in `J2811`)** | `The Leaf That Counts to Five Before It Digests` (`46 chars`, `0` exact collisions; or Rule 26 phrase-first `How Do Venus Flytraps Work? (1873 Electric Leaf)`, `48 chars`, `0` exact collisions; bare `The Plant That Counts to Five Before It Eats` rejected due to result #7 `ay4_XzfjXm8` on `The Know-It-Owl`) |
| **Title C (Rule 26 Exact Phrase First)** | `Carnivorous Plants: Why Darwin Fed Roast Beef to a Leaf` (`55 chars`, `0` exact collisions) |
| **Short S01 (Candidate Question Title, disambiguated in `J2811`)** | `How Does a Venus Flytrap Count to Five? (Two-Touch Test)` (`56 chars`, `0` exact collisions; bare `How Does a Venus Flytrap Count to Five?` rejected due to result #6 `BL4G1n7g6VI` *How does a Venus flytrap count to five? 🪴* on `BearlyBelievable`) |
| **Short S02 (Candidate Question Title)** | `Why Do Venus Flytraps Eat Insects? (Darwin's Bog Test)` (`54 chars`, `0` exact collisions) |
| **Autocomplete (`public_search.py`, `2026-11-14`)** | `"how do venus flytraps work"` = **yes** · `"carnivorous plants"` = **yes** · `"why do some plants eat insects"` = **yes** |
| **Rule 26 Ranking Videos (`2026-11-14`)** | 1) **BBC** [`O7eQKSf0LmY`](https://youtu.be/O7eQKSf0LmY) *Hungry Venus flytraps snap shut on a host of unfortunate flies \| Life - BBC* (**`13,770,762` views**) · 2) **Insider Science** [`YPzp-p-na88`](https://youtu.be/YPzp-p-na88) *What's Inside A Venus Flytrap?* (**`7,610,046` views**) |
| **Neighbour Gate (`neighbours.py`, `2026-11-14`)** | **PASS** — **`6` education videos `≥1,000,000` views** (`TED-Ed/TED: yes`, led by TED-Ed `4.45M` `Hja0SLs2kus`, TED `3.30M` `pvBlSFVmoaw`, TED-Ed `2.36M` `ee7muQ_qKU0`, TED-Ed `1.74M` `fSaHVHTqDY0`, Amoeba Sisters `1.29M` `DGpPHrLF-5M`, Amoeba Sisters `1.18M` `A_DF246uVlU`) |
| **Spend** | `£0.00` (free signed-out YouTube GB public search + `neighbours.py`) |

---

## 1. Learn From Our Data First (`2026-11-12` & `2026-11-13` Snapshots vs Lifetime Studio Read)

### 1.1 Data Sources, Timestamps, Numerators & Elapsed-Day Convention
To avoid mixing rolling YouTube Analytics windows with lifetime Studio reads or changing denominators mid-comparison, all figures below state their exact source and window:

1. **Daily Public Snapshots (`05_Analytics/hos/snapshots/2026-11-12.json` & `2026-11-13.json`):**
   - **`2026-11-12.json` taken at:** `2026-11-12T06:40:28.196Z` (`34` public videos: `6` longs + `28` Shorts; `6` subscribers; `3,852` public views). Rolling YouTube Analytics windows (`last28` and `last7`) in this file are settled through **`2026-11-10`**.
   - **`2026-11-13.json` taken at:** `2026-11-13T06:40:29.166Z` (`35` public videos: `7` longs + `28` Shorts, after `007` `ETynHpIYLeY` went public at `2026-11-12T18:00:36Z`; `6` subscribers; `3,897` public views). Rolling YouTube Analytics windows (`last28` and `last7`) in this file are settled through **`2026-11-11`**.
   - **Views/day formula (`07_Content-Ops/src/lib/analytics/channel-tracker.ts:596,611`):**
     - **Numerator:** `video.views` (public view count recorded in the snapshot JSON).
     - **Denominator (`ageDays`):** `max(daysBetween(publishedAt.slice(0, 10), snapshot.date), 1)` (calendar-day difference in UTC between the publish date `YYYY-MM-DD` and the snapshot date `YYYY-MM-DD`, floored at `1` day).
     - **Rate (`views/day`):** `round((views / ageDays) * 10) / 10`.
2. **Lifetime Studio Scrape (`05_Analytics/hos/studio_ctr.json`):**
   - **Read at:** `2026-11-12T07:07:54.728116+00:00` (`period: "lifetime"`).
   - Supplies **lifetime Studio impressions**, **lifetime Studio impressions CTR (%)**, **lifetime Studio views**, **lifetime Studio average % viewed (`avg_pct_viewed`)**, **lifetime Studio average view duration (`avd`)**, and **lifetime Studio Shorts stayed-to-watch (`stayed_pct`, "Viewed vs. swiped away")**.
   - Kept strictly separate from the rolling 7-day / 28-day YouTube Analytics (`YTA`) columns below.
3. **28-Day Channel Traffic Split (`05_Analytics/hos/REPORT.md` & `snapshots/2026-11-13.json` `last28` through `2026-11-11`):**
   - **Shorts (`2,906` views, `13.4` watch-hours in 28d; `2,994` views in `12 Nov` snapshot):** `77%` Shorts feed (`2,248` views on `13 Nov` / `2,311` on `12 Nov`, `67%` avg viewed), `22%` YouTube search (`630` views on `13 Nov` / `650` on `12 Nov`, `63–64%` avg viewed), `1%` Other/Channel pages.
   - **Longs (`61` views, `1.6` watch-hours in 28d on `13 Nov`; `62` views on `12 Nov`):** `46%` Suggested videos (`28` views, `19%` avg viewed; `45%` on `12 Nov`), `21%` YouTube search (`13` views, `27%` avg viewed; `23%` on `12 Nov`), `21%` Direct/unknown (`13` views), `5%` Browse features (`3` views), `3%` Shorts feed (`2` views via `SHORTS_CONTENT_LINKS`).

---

### 1.2 All Eligible Public HOS Longs — Consistently Ranked by `Views/Day`

*(Note: `ETynHpIYLeY` [007, *How Was the First Vaccine Made? (And Why It's Named After a Cow)*] went public on `2026-11-12T18:00:36Z` after the `12 Nov` snapshot and `studio_ctr.json` read; it is shown at the bottom of the `13 Nov` ranking with `0` views and `UNKNOWN` Studio metrics.)*

| Rank (`12 Nov` / `13 Nov` by Views/d) | Video ID & Film | Title | Pub Date & Length | `12 Nov` Snapshot (`Views / ageDays = Views/d`) | `13 Nov` Snapshot (`Views / ageDays = Views/d`) | Lifetime Studio (`studio_ctr.json` `12 Nov`: Impr · CTR · Studio Views · Studio Avg % Viewed) | Rolling 28d YTA (`12 Nov` / `13 Nov`: Views · Avg % Viewed) | Lifetime / YTA Retention Curve (`0:15` / `0:30` / `1:00` / End) & Stayed-to-Watch |
|---:|---|---|---|---|---|---|---|---|
| **#1 / #1** | `AL_-qlWko_g` (`002`) | *How Did We Discover the Periodic Table?* | `2026-09-17` · `541 s` (`9:01`) | `161 / 56 d` = **`2.9 / day`** | `161 / 57 d` = **`2.8 / day`** | `1,141` impr · **`3.42%` CTR** · `161` v · **`21.59%`** (`1:56`) | `18` v (`19.05%`) / `17` v (`19.16%`) | YTA curve (`161` v): `75.0%` at `0:11`, **`70–71%` at `0:15`**, **`51%` at `0:30`**, **`43%` at `1:00`**, `13%` end (`lower` vs similar) · Stayed: `not applicable (long)` |
| **#2 / #3** | `GHZDsiH7L7A` (`004`) | *What's Inside an Atom? Mostly Empty Space* | `2026-10-15` · `525 s` (`8:45`) | `32 / 28 d` = **`1.1 / day`** | `33 / 29 d` = **`1.1 / day`** | `816` impr · **`1.23%` CTR** · `31` v · **`20.89%`** (`1:49`) | `32` v (`20.89%`) / `25` v (`19.86%`) | YTA curve (`31` v): **`61%` at `0:15`**, **`41%` at `0:30`**, **`32%` at `1:00`**, `12%` end (`lower` vs similar) · Stayed: `not applicable (long)` |
| **#3 / #2** | `VbPubYd6Fbs` (`006`) | *The Willow Tree That Was Made of Air* | `2026-11-05` · `532 s` (`8:52`) | `4 / 7 d` = **`0.6 / day`** | `10 / 8 d` = **`1.3 / day`** | `22` impr · **`0.0%` CTR** · `2` v · **`99.99%`** (`8:51`, `n=2` views — too few to judge) | `1` v (`99.78%`) / `3` v (`55.14%`) | Curve: `UNKNOWN` (`too few views` in YTA) · Stayed: `not applicable (long)` |
| **#4 / #4** | `wwcjcFfC-5M` (`005`) | *The Tied Arm That Proved Your Blood Circulates* | `2026-10-29` · `529 s` (`8:49`) | `5 / 14 d` = **`0.4 / day`** | `5 / 15 d` = **`0.3 / day`** | `14` impr · **`21.43%` CTR** (`n=14` impr) · `5` v · **`9.24%`** (`0:48`) | `4` v (`11.43%`) / `4` v (`11.43%`) | Curve: `UNKNOWN` (`too few views` in YTA; Studio 4-pt `25%` at `0:15`) · Stayed: `not applicable (long)` |
| **#5 / #5 (tie)** | `frP_YrNShsU` (`003`) | *How Did We Discover X-rays?* | `2026-09-24` · `426 s` (`7:06`) | `5 / 49 d` = **`0.1 / day`** | `5 / 50 d` = **`0.1 / day`** | `41` impr · **`2.44%` CTR** · `5` v · **`26.65%`** (`1:53`) | `3` v (`14.12%`) / `3` v (`14.12%`) | Curve: `UNKNOWN` (`too few views` in YTA) · Stayed: `not applicable (long)` |
| **#5 / #5 (tie)** | `_C92tIJCk8A` (`001`) | *How Did We Discover Germs?* | `2026-09-03` · `365 s` (`6:05`) | `7 / 70 d` = **`0.1 / day`** | `7 / 71 d` = **`0.1 / day`** | `44` impr · **`6.82%` CTR** · `7` v · **`48.08%`** (`2:55`) | `1` v (`192.76%`) / `0` v (`UNKNOWN`) | Curve: `UNKNOWN` (`too few views` in YTA) · Stayed: `not applicable (long)` |
| **— / #7 (new)** | `ETynHpIYLeY` (`007`) | *How Was the First Vaccine Made? (And Why It's Named After a Cow)* | `2026-11-12` · `532 s` (`8:52`) | *(private at `06:40Z`)* | `0 / 1 d` = **`0.0 / day`** | `UNKNOWN` (not public at `12 Nov 07:07Z` Studio read) | `UNKNOWN` | Curve: `UNKNOWN` · Stayed: `not applicable (long)` |

#### Top 3 and Bottom 3 Public HOS Longs by `Views/Day` (Consistent Metric Ranking)
- **Top 3 by `Views/Day` (`12 Nov` and `13 Nov` snapshots):**
  1. **`AL_-qlWko_g` (`002`, *How Did We Discover the Periodic Table?*):** `2.9/day` on `12 Nov` (`161v / 56d`) and `2.8/day` on `13 Nov` (`161v / 57d`); lifetime Studio: `1,141` impressions, `3.42%` CTR, `21.59%` avg viewed (`1:56`), stayed `not applicable`.
  2. **`GHZDsiH7L7A` (`004`, *What's Inside an Atom? Mostly Empty Space*)** on `12 Nov` (`1.1/day`, `32v / 28d`; `#3` on `13 Nov` at `1.1/day`, `33v / 29d`); lifetime Studio: `816` impressions, `1.23%` CTR, `20.89%` avg viewed (`1:49`), stayed `not applicable`.
  3. **`VbPubYd6Fbs` (`006`, *The Willow Tree That Was Made of Air*)** on `12 Nov` (`0.6/day`, `4v / 7d`; rises to `#2` on `13 Nov` at `1.3/day`, `10v / 8d`); lifetime Studio (`12 Nov` on `2` Studio views): `22` impressions, `0.0%` CTR, `99.99%` avg viewed (`8:51` on `2` views — sample too small to interpret), stayed `not applicable`.
- **Bottom 3 by `Views/Day` (among the 6 settled longs public `≥7` days):**
  1. **`frP_YrNShsU` (`003`, *How Did We Discover X-rays?*):** `0.1/day` (`5v / 49d` on `12 Nov`; `5v / 50d` on `13 Nov`); lifetime Studio: `41` impressions, `2.44%` CTR, `26.65%` avg viewed (`1:53`), stayed `not applicable`.
  2. **`_C92tIJCk8A` (`001`, *How Did We Discover Germs?*):** `0.1/day` (`7v / 70d` on `12 Nov`; `7v / 71d` on `13 Nov`); lifetime Studio: `44` impressions, `6.82%` CTR, `48.08%` avg viewed (`2:55`), stayed `not applicable`.
  3. **`wwcjcFfC-5M` (`005`, *The Tied Arm That Proved Your Blood Circulates*):** `0.4/day` on `12 Nov` (`5v / 14d`) and `0.3/day` on `13 Nov` (`5v / 15d`); lifetime Studio: `14` impressions, `21.43%` CTR (on only `14` impressions), `9.24%` avg viewed (`0:48`), stayed `not applicable`. *(If newly published `007` `ETynHpIYLeY` [`0.0/day`, `0v / 1d` on `13 Nov`, CTR/AVD `UNKNOWN`] is included, it is lowest on `13 Nov` at `<1` day old.)*

#### Separate Long Rankings by Other Metrics (Avoiding Metric Conflation)
- **By Lifetime Studio Impressions:** `#1` `002` Periodic Table (`1,141` impr) → `#2` `004` Atom (`816` impr) → `#3` `001` Germs (`44` impr) → `#4` `003` X-rays (`41` impr) → `#5` `006` Willow Tree (`22` impr) → `#6` `005` Tied Arm (`14` impr).
- **By Lifetime Studio CTR (among longs with `≥100` impressions):** `#1` `002` Periodic Table (`3.42%` on `1,141` impr) → `#2` `004` Atom (`1.23%` on `816` impr). *(Among low-impression longs `<50` impr, `005` has `21.43%` on `14` impr and `001` has `6.82%` on `44` impr, both too small for statistical confidence.)*
- **By Lifetime Studio Avg % Viewed:** `#1` (on `≥30` views) `002` Periodic Table (`21.59%` on `161` views) → `#2` `004` Atom (`20.89%` on `31` Studio views). *(On `<10` views, `006` Willow has `99.99%` on `2` views, `001` Germs has `48.08%` on `7` views, `003` X-rays has `26.65%` on `5` views, and `005` Tied Arm has `9.24%` on `5` views — all `<10`-view averages are descriptive only and too small to establish a winning or losing retention format.)*

#### Measured Attributes vs `UNKNOWN` for Longs (Hypotheses, Not Absolutes)
- **Subject & Title Shape (Hypothesis):** Our only two longs with `>800` impressions (`002` Periodic Table `1,141` impr and `004` Atom `816` impr) carry plain questions on core school-chemistry/physics nouns, whereas our two story-statement titles (`005` *The Tied Arm That Proved Your Blood Circulates* `14` impr; `006` *The Willow Tree That Was Made of Air* `22` impr) received very few impressions in their first 1–2 weeks. **Caveat:** A plain question title is **not** sufficient on its own — `003` (*How Did We Discover X-rays?*) and `001` (*How Did We Discover Germs?*) use the exact same *"How Did We Discover…?"* question shape yet sit at `41` and `44` lifetime impressions (`0.1/day`). This matches `LEARNINGS.md` Rule 26: topic search demand and neighbour graph fit are hypotheses under active test alongside title shape.
- **Opening (Measured Script & Curve Evidence vs `UNKNOWN`):**
  - `002` (`541 s`): `01_Script/periodic_table_script_master_v01.md` opens with rhetorical questions on a "secret seating plan" and workshop jars/ores (`75.0%` at `0:11`, `70–71%` at `0:15`, `51%` at `0:30` on `161` views).
  - `004` (`525 s`): `01_Script/atom_script_master_v02.md` opens cold on physical action (*"Cut a gold coin in half. Then cut it again."* with atom answer image by `0:05`, zero agenda line; `61%` at `0:15`, `41%` at `0:30` on `31` views).
  - `005` (`529 s`) & `006` (`532 s`): `blood_script_master_v02.md` (`0:16`) and `trees_script_master_v02.md` (`0:09`) both contain an early *"By the end of this film, you'll know..."* agenda line (pre-Rule 10), and `001` (`365 s`) and `003` (`426 s`) open with `"What if..."` rhetorical questions. However, because `001`, `003`, `005`, and `006` each have `2–10` views, their YTA retention curves are **`UNKNOWN` (`too few views`)**, so we cannot draw causal retention conclusions from their openings yet.
- **Thumbnail Concept (Measured Repo Evidence vs `UNKNOWN`):**
  - `001`–`004` launched with painted 3D Animistry-style key art repeating the full title in serif type (`08_Thumbnail/LIVE_THUMB_LOCK.md`: swan-neck flask on `001`, molten gallium on `002`, X-ray hand on `003`, glowing atom on `004`), while `005` (`ONE TIGHT BAND`) and `006` (`WOOD FROM SKY?`) used short 3-word hooks (`08_Thumbnail/THUMBS_INDEX_v01.json`). In `05_Analytics/tests/THUMB_LEDGER.json`, `T001` (`003` X-rays) ended as a **`draw` (`Not enough impressions to declare a winner` on `41` impr)**, and `T009` (`001`) and `T023` (`002`) are still running (`result: UNKNOWN`). Thus thumbnail variant performance on HOS longs remains **`UNKNOWN`** pending higher impression volume.
- **Length (Measured Repo Evidence):** `002` (`541 s`), `006` (`532 s`), `007` (`532 s`), `005` (`529 s`), and `004` (`525 s`) all sit in the `8:45–9:01` house target band, while earlier `001` (`365 s` / `6:05`) and `003` (`426 s` / `7:06`) are shorter.

---

### 1.3 All 28 Public HOS Shorts — Consistently Ranked by `Views/Day`

*(Denominator note for `PFj6172YU4Q`: published `2026-11-08T11:30:25Z`. In the `2026-11-12` snapshot [`takenAt: 2026-11-12T06:40:28Z`], `ageDays = daysBetween('2026-11-08', '2026-11-12') = 4` days, so `215 / 4 = 53.75 → 53.8/day`. In the `2026-11-13` snapshot, `ageDays = 5` days, so `216 / 5 = 43.2/day`. Lifetime Studio CTR is `not applicable` to Shorts, which are served primarily in the Shorts feed and search.)*

| Rank (`12 Nov` / `13 Nov` by Views/d) | Video ID & Film | Title | Pub Date & Len | `12 Nov` Snapshot (`Views / ageDays = Views/d`) | `13 Nov` Snapshot (`Views / ageDays = Views/d`) | Lifetime Studio (`studio_ctr.json` `12 Nov`: Views · Stayed % · Avg % Viewed · AVD · D1 Feed) | Rolling 28d YTA (`12 Nov` / `13 Nov`: Views · Avg % Viewed) |
|---:|---|---|---|---|---|---|---|
| **#1 / #2** | `PFj6172YU4Q` (`005`) | *One Tight Band Proved Your Blood Goes Round* | `2026-11-08` · `27 s` | `215 / 4 d` = **`53.8 / d`** | `216 / 5 d` = **`43.2 / d`** | `218` v · **`15.21%` stayed** (`MISS`) · **`61.08%`** (`0:16`) · `89%` d1 feed | `215` v (`61.02%`) / `215` v (`61.04%`) |
| **#2 / #1** | `29bpGAI0wb8` (`004`) | *What happens if you keep cutting gold in half?* | `2026-10-16` · `25 s` | `1,226 / 27 d` = **`45.4 / d`** | `1,226 / 28 d` = **`43.8 / d`** | `1,226` v · **`40.78%` stayed** (`MISS`) · **`44.12%`** (`0:11`) · `93%` d1 feed | `1,226` v (`44.12%`) / `1,226` v (`44.12%`) |
| **#3 / #3** | `AMSriTQ-lcQ` (`004`) | *Are Marie Curie's Notebooks Still Radioactive?* | `2026-10-28` · `22 s` | `274 / 15 d` = **`18.3 / d`** | `274 / 16 d` = **`17.1 / d`** | `274` v · **`22.66%` stayed** (`MISS`) · **`76.94%`** (`0:16`, `PASS`) · `86%` d1 feed | `273` v (`78.30%`) / `273` v (`78.30%`) |
| **#4 / #4** | `OnJ8MFu0Mi0` (`001`) | *How Did John Snow Stop Cholera?* | `2026-10-26` · `23 s` | `234 / 17 d` = **`13.8 / d`** | `235 / 18 d` = **`13.1 / d`** | `234` v · `30.89%` stayed · `66.15%` (`0:15`) · `95%` d1 feed | `233` v (`65.87%`) / `234` v (`66.15%`) |
| **#5 / #5** | `pWySvZsneZg` (`004`) | *Why Gold Foil Bounced Rutherford's Particles Back* | `2026-11-01` · `25 s` | `137 / 11 d` = **`12.5 / d`** | `137 / 12 d` = **`11.4 / d`** | `137` v · `37.23%` stayed · **`112.43%`** (`0:28`) · `69%` d1 feed | `136` v (`113.15%`) / `136` v (`113.15%`) |
| **#6 / #6** | `oKqmnJNGiHg` (`002`) | *How Was Phosphorus Discovered?* | `2026-10-21` · `23 s` | `183 / 22 d` = **`8.3 / d`** | `183 / 23 d` = **`8.0 / d`** | `183` v · `40.30%` stayed · **`87.29%`** (`0:20`, `PASS`) · `15%` d1 feed | `182` v (`86.90%`) / `182` v (`86.90%`) |
| **#7 / #7** | `-3L6HzJ_d_4` (`001`) | *What Is the Pasteur Swan Neck Flask Experiment?* | `2026-10-27` · `19 s` | `123 / 16 d` = **`7.7 / d`** | `127 / 17 d` = **`7.5 / d`** | `122` v · **`76.47%` stayed** (`PASS`) · **`74.54%`** (`0:14`, `PASS`) · `13%` d1 feed | `117` v (`70.82%`) / `122` v (`70.72%`) |
| **#8 / #8** | `clV6E10NLPw` (`001`) | *The spray that stopped surgery killing patients* | `2026-10-20` · `25 s` | `153 / 23 d` = **`6.7 / d`** | `153 / 24 d` = **`6.4 / d`** | `153` v · `22.39%` stayed · `56.71%` (`0:14`) · `88%` d1 feed | `153` v (`56.71%`) / `153` v (`56.71%`) |
| **#9 / #9** | `c2q7w0pgcn8` (`002`) | *Who Discovered Infrared Light?* | `2026-10-19` · `23 s` | `138 / 24 d` = **`5.8 / d`** | `139 / 25 d` = **`5.6 / d`** | `138` v · **`43.52%` stayed** · **`105.30%`** (`0:24`) · `82%` d1 feed | `138` v (`108.40%`) / `138` v (`108.40%`) |
| **#10 / #10** | `qOZgess30h0` (`001`) | *Invisible life is still everywhere* | `2026-10-13` · `24 s` | `169 / 30 d` = **`5.6 / d`** | `169 / 31 d` = **`5.5 / d`** | `169` v · `25.23%` stayed · `39.75%` (`0:09`) · `94%` d1 feed | `122` v (`43.40%`) / `37` v (`49.09%`) |
| **#11 / #11** | `mTY67qet7cM` (`005`) | *Your Heart Pumps More Blood Than You Have* | `2026-11-02` · `25 s` | `51 / 10 d` = **`5.1 / d`** | `51 / 11 d` = **`4.6 / d`** | `51` v · `25.00%` stayed · `63.61%` (`0:15`) · `88%` d1 feed | `50` v (`63.16%`) / `51` v (`63.48%`) |
| **#12 / #12** | `xHnIi9GqOsM` (`005`) | *Why Do Veins Have Valves?* | `2026-11-05` · `23 s` | `35 / 7 d` = **`5.0 / d`** | `36 / 8 d` = **`4.5 / d`** | `35` v · `38.46%` stayed · `71.09%` (`0:16`) · `83%` d1 feed | `35` v (`71.09%`) / `35` v (`71.09%`) |
| **#13 / #13** | `_xh-G9n88hU` (`003`) | *What Are Cathode Rays?* | `2026-10-24` · `26 s` | `64 / 19 d` = **`3.4 / d`** | `64 / 20 d` = **`3.2 / d`** | `63` v · `67.57%` stayed · `68.58%` (`0:17`) · `75%` d1 feed | `63` v (`68.59%`) / `63` v (`68.59%`) |
| **#14 / #14** | `Ooc31g0eeP0` (`003`) | *Why Didn't Röntgen Patent the X-Ray?* | `2026-10-23` · `21 s` | `61 / 20 d` = **`3.0 / d`** | `61 / 21 d` = **`2.9 / d`** | `61` v · `16.44%` stayed · `94.82%` (`0:19`) · `74%` d1 feed | `61` v (`94.81%`) / `61` v (`94.81%`) |
| **#15 / #15** | `vPecjT3F1z0` (`004`) | *Every Element Has an Atomic Number* | `2026-10-18` · `27 s` | `51 / 25 d` = **`2.0 / d`** | `51 / 26 d` = **`2.0 / d`** | `51` v · `32.43%` stayed · `61.49%` (`0:16`) · `77%` d1 feed | `50` v (`61.49%`) / `51` v (`62.54%`) |
| **#16 / #16 (tie)** | `5n7xFQRBUvI` (`005`) | *Is the Heart a Pump?* | `2026-10-30` · `22 s` | `23 / 13 d` = **`1.8 / d`** | `24 / 14 d` = **`1.7 / d`** | `23` v · `9.52%` stayed · `55.66%` (`0:12`) · `78%` d1 feed | `23` v (`55.65%`) / `23` v (`55.65%`) |
| **#16 / #16 (tie)** | `E9sbfgMS6vA` (`004`) | *The Four Elements Were Wrong* | `2026-10-17` · `24 s` | `44 / 26 d` = **`1.7 / d`** | `44 / 27 d` = **`1.6 / d`** | `44` v · `41.38%` stayed · `68.58%` (`0:16`) · `0%` d1 feed | `42` v (`68.70%`) / `44` v (`68.57%`) |
| **#18 / #18** | `7yH0tcaS2K0` (`001`) | *You are the vector* | `2026-09-06` · `25 s` | `80 / 67 d` = **`1.2 / d`** | `80 / 68 d` = **`1.2 / d`** | `79` v · `21.21%` stayed · `48.62%` (`0:12`) · `79%` d1 feed | `8` v (`92.75%`) / `9` v (`85.11%`) |
| **#19 / #19** | `3y_0VdfxU30` (`001`) | *An enemy that does not cast a shadow* | `2026-09-04` · `25 s` | `84 / 69 d` = **`1.2 / d`** | `84 / 70 d` = **`1.2 / d`** | `84` v · `27.38%` stayed · `44.91%` (`0:11`) · `83%` d1 feed | `1` v (`34.00%`) / `1` v (`34.00%`) |
| **#20 / #20** | `56b6w-ca3vU` (`001`) | *A drop of pond water is not empty* | `2026-09-05` · `25 s` | `62 / 68 d` = **`0.9 / d`** | `62 / 69 d` = **`0.9 / d`** | `62` v · `36.36%` stayed · `51.80%` (`0:12`) · `86%` d1 feed | `0` v (`UNKNOWN`) / `0` v (`UNKNOWN`) |
| **#21 / #22** | `7p9VLH442eb` (`006`) | *Did Plants Almost Freeze the Earth?* | `2026-11-07` · `24 s` | `5 / 5 d` = **`1.0 / d`** | `5 / 6 d` = **`0.8 / d`** | `5` v · `50.00%` stayed · `107.12%` (`0:25`, `n=5`) · `40%` d1 feed | `5` v (`107.12%`) / `5` v (`107.12%`) |
| **#22 / #21** | `41fF9_08V6A` (`006`) | *Do Plants Eat Dirt?* | `2026-11-10` · `24 s` | `2 / 2 d` = **`1.0 / d`** | `3 / 3 d` = **`1.0 / d`** | `2` v · `100.0%` stayed (`n=2`) · `92.60%` (`0:22`, `n=2`) · `UNKNOWN` d1 feed | `UNKNOWN` (published `10 Nov`) / `2` v (`92.62%`) |
| **#23 / #23** | `7R8xG6rE2mE` (`001`) | *A flask shaped like a question mark* | `2026-09-07` · `25 s` | `47 / 66 d` = **`0.7 / d`** | `47 / 67 d` = **`0.7 / d`** | `47` v · `45.45%` stayed · `50.40%` (`0:12`) · `79%` d1 feed | `0` v (`UNKNOWN`) / `0` v (`UNKNOWN`) |
| **#24 / #24** | `R-H22S43bOs` (`002`) | *He predicted a metal before anyone found it* | `2026-09-19` · `26 s` | `31 / 54 d` = **`0.6 / d`** | `31 / 55 d` = **`0.6 / d`** | `31` v · `24.00%` stayed · `58.91%` (`0:15`) · `67%` d1 feed | `3` v (`87.69%`) / `3` v (`87.69%`) |
| **#25 / #25** | `W8h6d9S0M0A` (`002`) | *Tellurium broke the rule and Mendeleev moved it anyway* | `2026-09-21` · `26 s` | `28 / 52 d` = **`0.5 / d`** | `28 / 53 d` = **`0.5 / d`** | `28` v · `34.78%` stayed · `56.60%` (`0:14`) · `73%` d1 feed | `1` v (`70.38%`) / `1` v (`70.38%`) |
| **#26 / #26** | `CnHwX1L9XHg` (`002`) | *Gallium sat where the table said* | `2026-09-20` · `26 s` | `16 / 53 d` = **`0.3 / d`** | `16 / 54 d` = **`0.3 / d`** | `16` v · `30.43%` stayed · `33.45%` (`0:08`) · `53%` d1 feed | `0` v (`UNKNOWN`) / `0` v (`UNKNOWN`) |
| **#27 / #27** | `zI_eD3vFWmE` (`003`) | *The first X-ray showed a wedding ring* | `2026-09-27` · `25 s` | `9 / 46 d` = **`0.2 / d`** | `9 / 47 d` = **`0.2 / d`** | `9` v · `50.00%` stayed (`n=9`) · `64.00%` (`0:16`) · `0%` d1 feed | `0` v (`UNKNOWN`) / `0` v (`UNKNOWN`) |
| **#28 / #28** | `LanTHJckYx8` (`002`) | *What other table has empty chairs?* | `2026-09-22` · `26 s` | `4 / 51 d` = **`0.1 / d`** | `4 / 52 d` = **`0.1 / d`** | `4` v · `33.33%` stayed (`n=4`) · `23.08%` (`0:06`) · `33%` d1 feed | `0` v (`UNKNOWN`) / `0` v (`UNKNOWN`) |

#### Top 3 and Bottom 3 Public HOS Shorts by `Views/Day` (Plus Separate Retention Rankings)
- **Top 3 Shorts by `Views/Day`:**
  1. **`PFj6172YU4Q` (*One Tight Band Proved Your Blood Goes Round*, `27 s`):** `53.8/day` on `12 Nov` (`215` views across **`4` elapsed days**, `2026-11-08` to `2026-11-12`) and `43.2/day` on `13 Nov` (`216` views across **`5` elapsed days**, `#2` on `13 Nov`); lifetime Studio: `218` views, `15.21%` stayed (`MISS`), `61.08%` avg viewed (`0:16`), CTR `not applicable`.
  2. **`29bpGAI0wb8` (*What happens if you keep cutting gold in half?*, `25 s`):** `45.4/day` on `12 Nov` (`1,226` views / `27 d`) and `43.8/day` on `13 Nov` (`1,226` views / `28 d`, `#1` on `13 Nov`); lifetime Studio: `1,226` views, `40.78%` stayed (`MISS`), `44.12%` avg viewed (`0:11`), CTR `not applicable`.
  3. **`AMSriTQ-lcQ` (*Are Marie Curie's Notebooks Still Radioactive?*, `22 s`):** `18.3/day` on `12 Nov` (`274` views / `15 d`) and `17.1/day` on `13 Nov` (`274` views / `16 d`); lifetime Studio: `274` views, `22.66%` stayed (`MISS`), `76.94%` avg viewed (`0:16`, `PASS`), CTR `not applicable`.
- **Bottom 3 Shorts by `Views/Day`:**
  1. **`LanTHJckYx8` (*What other table has empty chairs?*, `26 s`):** `0.1/day` (`4` views / `51 d` on `12 Nov`, `52 d` on `13 Nov`); lifetime Studio (`n=4` views — too few to judge): `33.33%` stayed, `23.08%` avg viewed (`0:06`), CTR `not applicable`.
  2. **`zI_eD3vFWmE` (*The first X-ray showed a wedding ring*, `25 s`):** `0.2/day` (`9` views / `46 d` on `12 Nov`, `47 d` on `13 Nov`); lifetime Studio (`n=9` views — too few to judge): `50.00%` stayed, `64.00%` avg viewed (`0:16`), `0%` d1 feed, CTR `not applicable`.
  3. **`CnHwX1L9XHg` (*Gallium sat where the table said*, `26 s`):** `0.3/day` (`16` views / `53 d` on `12 Nov`, `54 d` on `13 Nov`); lifetime Studio (`n=16` views — too few to judge): `30.43%` stayed, `33.45%` avg viewed (`0:08`), CTR `not applicable`.
- **Separate Short Rankings by Retention Metrics (`≥100` Studio Views):**
  - **By Stayed-to-Watch (`studio_ctr.json` `≥100` views):** `#1` **`-3L6HzJ_d_4`** (*What Is the Pasteur Swan Neck Flask Experiment?*, `19 s`, `122` Studio views: **`76.47%` stayed**, `74.54%` avg viewed, `92%` of 28d views from `YT_SEARCH`) → `#2` **`c2q7w0pgcn8`** (*Who Discovered Infrared Light?*, `23 s`, `138` Studio views: **`43.52%` stayed**, `105.30%` avg viewed) → `#3` **`29bpGAI0wb8`** (`1,226` Studio views: **`40.78%` stayed**, `44.12%` avg viewed) → `#4` **`oKqmnJNGiHg`** (*How Was Phosphorus Discovered?*, `23 s`, `183` Studio views: **`40.30%` stayed**, `87.29%` avg viewed).
  - **By Lifetime Studio Avg % Viewed (`studio_ctr.json` `≥100` views):** `#1` **`pWySvZsneZg`** (*Why Gold Foil Bounced Rutherford's Particles Back*, `25 s`, `137` Studio views: **`112.43%` avg viewed** [`0:28`], `37.23%` stayed) → `#2` **`c2q7w0pgcn8`** (**`105.30%` avg viewed** [`0:24`], `43.52%` stayed) → `#3` **`oKqmnJNGiHg`** (**`87.29%` avg viewed** [`0:20`], `40.30%` stayed) → `#4` **`AMSriTQ-lcQ`** (**`76.94%` avg viewed** [`0:16`], `22.66%` stayed) → `#5` **`-3L6HzJ_d_4`** (**`74.54%` avg viewed** [`0:14`], `76.47%` stayed).
- **Hypotheses & Caveats on Short Patterns:**
  - **Replay vs Seamless Loop:** `112.43%` avg viewed on `pWySvZsneZg` and `105.30%` on `c2q7w0pgcn8` indicate that average view duration exceeded the clip length (consistent with viewer replay/rewatching alongside short `0.30–1.00 s` tails and late payoffs at `70.5–92.8%` of runtime documented in `LEARNINGS.md` Rules 3, 6, 27); they are **not** proof that an intentional seamless loop alone caused the replay.
  - **Feed Velocity vs Swipe Gate:** `PFj6172YU4Q` (*One Tight Band Proved Your Blood Goes Round*) achieved `#1` 4-day velocity (`53.8/day`) despite a statement title and a low `15.21%` stayed rate (`89%` d1 feed test pool), whereas `-3L6HzJ_d_4` (`76.47%` stayed) got only `13%` d1 feed and grew slowly (`7.5–7.7/day`) via `YT_SEARCH` (`92%` of 28d views). Thus question titles (`LEARNINGS.md` Rules 1 & 28) and Frame-0 hero-object opens (`Rules 2, 24, 27`) are treated as **hypotheses** aimed at pairing feed test pools with higher stayed-to-watch and search compounding.

---

## 2. Topic Proposal — `HOS:105` (*How Do Venus Flytraps Work? (The Plant That Counts to Five)*)

> **UNVERIFIED HISTORICAL & SCIENTIFIC CLAIMS NOTICE:**
> Every date, person, instrument detail, and scientific number in §2 and §3 below — including John Ellis's 1768–1770 letter to Carl Linnaeus and Linnaeus's reply, Charles Darwin's 1875 *Insectivorous Plants* feeding experiments, John Scott Burdon-Sanderson's 1873 Venus flytrap electrical action-potential galvanometer measurements, and Rainer Hedrich's 2016 five-touch counting mechanism — is **UNVERIFIED** and **NOT CLEARED FOR NARRATION OR SHORT OPENS**. No spoken script draft is approved (`01_Script/episode_script_draft_v01.md` remains the blank template). Before any script lock, every claim must be backed by an exact quote in `SOURCES.md` and verified through the `facts` lane (`gemini-agy`).

### 2.1 One-Line Hook & Candidate Discovery Outline (Unverified Working Notes)
- **One-line hook (unverified):** Touch one sensory hair inside a Venus flytrap and nothing happens; touch a second hair within twenty seconds and the leaf fires an electrical nerve-like pulse to snap shut — then waits until it counts to five before digesting its meal.
- **Candidate 4-act outline to verify in `SOURCES.md` before scripting:**
  1. **John Ellis vs Carl Linnaeus (London & Uppsala, 1768–1770, *UNVERIFIED*):** London merchant-naturalist John Ellis receives living specimens of *Dionaea muscipula* from the North Carolina bogs and sends an illustrated description to Carl Linnaeus, proposing that the plant catches and eats insects for nourishment. Linnaeus — whose great chain of nature places plants strictly below animals — refuses to believe a plant eats meat, declaring it against the order of nature and merely an accidental trap. *(Requires exact quotes from Ellis's 1769/1770 letter/pamphlet *Directions for Bringing Over Seeds and Plants* and Linnaeus's reply in `SOURCES.md`.)*
  2. **Charles Darwin (Down House greenhouse, 1860–1875, *Insectivorous Plants*, *UNVERIFIED*):** Obsessed with sundews (*Drosera*) and Venus flytraps in his greenhouse ("I care more about Drosera than the origin of all the species in the world"), Darwin feeds leaves tiny cubes of roast beef, boiled egg white, cheese, glass, chalk, and raindrops. He proves the traps ignore raindrops and non-nitrogenous grit, secrete an acidic pepsin-like digestive fluid only for nitrogen-rich animal matter, and evolve carnivory because bog soils are starved of nitrogen. *(Requires exact quotes from Darwin's 1860 letter to Lyell and his 1875 book *Insectivorous Plants* in `SOURCES.md`.)*
  3. **John Scott Burdon-Sanderson (University College London / Royal Society, 1873, *UNVERIFIED*):** Encouraged by Darwin to test whether the leaf's snap is electrical like an animal nerve or muscle, physiologist John Scott Burdon-Sanderson connects electrodes and a sensitive mirror **galvanometer** to a Venus flytrap leaf — discovering that touching a trigger hair fires a measurable electrical **action potential** across the leaf before the trap snaps shut. *(Requires exact quote from Burdon-Sanderson's 1873 *Proceedings of the Royal Society* / *Nature* paper in `SOURCES.md`.)*
  4. **Rainer Hedrich & Colleagues (*Current Biology*, 2016, *UNVERIFIED*):** Modern electrophysiology solves how the trap avoids wasting energy on false alarms: **Touch 1** primes the calcium clock (`~20 s` window); **Touch 2** fires the second action potential that snaps the prison bars shut (`~0.1 s`); **Touches 3, 4, and 5** by the struggling insect trigger jasmonic acid hormones and digestive enzyme glands to seal and digest the prey and absorb its nitrogen. *(Requires exact quote from Böhm et al. / Hedrich, *Current Biology* 26, 286–295, 2016 in `SOURCES.md`.)*
- **Planned Teach-on-Screen Visuals (Once Sourced):** `DATA`: Touch-count timeline (`Touch 1 -> Touch 2 snap -> Touches 3–5 enzyme secretion`) vs electrical action-potential spikes (mV); `DATA`: Darwin's nitrogen vs non-nitrogen feeding test table (roast beef/egg white vs glass/chalk/water); `WHEN`: timeline cards (`1768 -> 1873 -> 1875 -> 2016`).
- **3-Way Thumbnail Concept Plan (Rule 12 / Rule 14 — Concepts Only, Zero Spend):**
  - **Thumb A (Biological Mechanism):** Painted 3D house style: extreme close-up inside the crimson-and-green jaws of a **Venus flytrap** where three sensory trigger hairs glow with golden electrical pulses (`1... 2... 5`), Explorer small lower-left, cream/gold serif text: `COUNTS TO FIVE` (`3 words`).
  - **Thumb B (Rule 14 Bright High-Contrast Variant):** Bright sunlit Victorian greenhouse contrast: Charles Darwin's brass tweezers lowering a tiny cube of roast beef into an open green Venus flytrap jaw; serif text: `FED ROAST BEEF` (`3 words`).
  - **Thumb C (Electrical Apparatus):** A green Venus flytrap wired with copper leads to an 1873 brass mirror galvanometer whose needle spikes as a fly touches a trigger hair; serif text: `ELECTRIC LEAF` (`2 words`).

### 2.2 Why Our Data Suggests Testing This Topic (Hypotheses, Not Guarantees)
1. **Plain Search Question + Multi-Million Biology & TED/TED-Ed Neighbours (Hypothesis):** `"how do venus flytraps work"`, `"carnivorous plants"`, and `"why do some plants eat insects"` are all verified YouTube GB autocomplete phrases (`suggest = yes`, `2026-11-14`), backed by `BBC` (`13.77M` views), `Insider Science` (`7.61M` views), `TED-Ed` (`4.45M` *The amazing ways plants defend themselves* and `2.36M` *The wild world of carnivorous plants*), and `TED` (`3.30M` *Electrical experiments with plants that count and communicate*). On our channel, YouTube Search already drives `22%` of Shorts views and `21%` of long views (`REPORT.md`), and our #1 Short by stayed-to-watch (`-3L6HzJ_d_4` *What Is the Pasteur Swan Neck Flask Experiment?*, `76.47%` stayed) gets `92%` of its 28-day traffic from YouTube Search.
2. **Concrete Counting & Electrical Proof in the First 15 Seconds (Rule 10 & Rule 30 `HOS-2026-11-E2` Hypothesis):** Unlike `006` (*The Willow Tree That Was Made of Air*, which used a poetic statement title and an early agenda line at `0:09` and sits at `22` impressions), `HOS:105` tests a direct autocomplete question title (`How Do Venus Flytraps Work? (The Plant That Counts to Five)`) paired with an immediate physical `0:05–0:15` demonstration of the two-touch electrical snap and five-touch digestive lock.

### 2.3 Evidence — `neighbours.py` (`PASS`, `6` Videos `≥1M`) & `public_search.py` (`2026-11-14`)

#### A. Pasted `neighbours.py` Output (`2026-11-14`, Saved at `11_Upload-Package/evidence_2026-11-14_neighbours.json`)

```text
$ python3 00_Brand/Channel-Setup/tools/neighbours.py "venus flytrap" "carnivorous plants" "plant adaptations" --out 02_Video-Projects/105_Ellis-Darwin-BurdonSanderson-Venus-Flytrap-Carnivorous-Plants/11_Upload-Package/evidence_2026-11-14_neighbours.json
| # | Channel | Views | Title | Found by |
|---|---|---|---|---|
| 1 | TED-Ed ★ | 4,447,004 views | [The amazing ways plants defend themselves - Valentin Hammoudi](https://youtu.be/Hja0SLs2kus) | ted-ed carnivorous plants |
| 2 | TED ★ | 3,302,069 views | [Electrical experiments with plants that count and communicate | Greg Gage](https://youtu.be/pvBlSFVmoaw) | venus flytrap ted |
| 3 | TED-Ed ★ | 2,362,056 views | [The wild world of carnivorous plants - Kenny Coogan](https://youtu.be/ee7muQ_qKU0) | carnivorous plants |
| 4 | TED-Ed ★ | 1,742,029 views | [These animals are also plants … wait, what? - Luka Seamus Wright](https://youtu.be/fSaHVHTqDY0) | ted-ed carnivorous plants |
| 5 | TED-Ed ★ | 367,273 views | [How plants tell time - Dasha Savage](https://youtu.be/3jIW5wW2WC0) | ted-ed plant adaptations |
| 6 | Amoeba Sisters | 1,289,643 views | [(OLD VIDEO) Plant Structure and Adaptations](https://youtu.be/DGpPHrLF-5M) | plant adaptations |
| 7 | Amoeba Sisters | 1,182,864 views | [Plants: Diversity, Structure, & Adaptations](https://youtu.be/A_DF246uVlU) | plant adaptations |
| 8 | Khan Academy | 312,997 views | [CAM Plants](https://youtu.be/xp6Zj24h8uA) | khan academy carnivorous plants |
| 9 | Khan Academy | 305,589 views | [Plant cell walls | Structure of a cell | Biology | Khan Academy](https://youtu.be/zdvKhaQxvag) | khan academy plant adaptations |
| 10 | Khan Academy | 300,297 views | [Overview of animal and plant cells | Biology | Khan Academy](https://youtu.be/24YMQ9GvLss) | khan academy carnivorous plants |
| 11 | Cognito | 243,546 views | [GCSE Biology - Structure of a Leaf | Plant Cell Organisation (2027/28 exams)](https://youtu.be/c9aUWHleZ_k) | plant adaptations |
| 12 | Khan Academy | 182,659 views | [Photoperiodism  | Plant Biology | Khan Academy](https://youtu.be/AQf3gKTCffs) | khan academy plant adaptations |

Words the top neighbours share: biology khan, khan academy
TED-Ed/TED neighbour: yes
Big neighbours (≥ 1,000,000 views): 6 (need 3)
Neighbour gate (≥ 3 education videos with 1,000,000+ views): PASS
Raw pull: 02_Video-Projects/105_Ellis-Darwin-BurdonSanderson-Venus-Flytrap-Carnivorous-Plants/11_Upload-Package/evidence_2026-11-14_neighbours.json
```

#### B. Pasted `public_search.py` Output & Title Collision Check (`2026-11-14`, Saved at `11_Upload-Package/evidence_2026-11-14_public_search.json`)

```text
$ python3 00_Brand/Channel-Setup/tools/public_search.py "how do venus flytraps work" "carnivorous plants" "why do some plants eat insects" "How Do Venus Flytraps Work? (The Plant That Counts to Five)" "Carnivorous Plants: Why Darwin Fed Roast Beef to a Leaf" "The Plant That Counts to Five Before It Eats" "How Does a Venus Flytrap Count to Five?" "Why Do Venus Flytraps Eat Insects? (Darwin's Bog Test)" --out 02_Video-Projects/105_Ellis-Darwin-BurdonSanderson-Venus-Flytrap-Carnivorous-Plants/11_Upload-Package/evidence_2026-11-14_public_search.json
| Phrase | Autocomplete? | Top results (GB) |
|---|---|---|
| how do venus flytraps work | yes | Insider Science 7,610,046 · Peekaboo Kidz 2,333,002 · BBC 13,770,762 · Colossal Cranium 1,352,980 · BBC 801,816 |
| carnivorous plants | yes | Terra Mater 1,283,419 · BBC 13,770,753 · Learn Bright 1,966,853 · Ze Frank 15,868,859 · benjiplant 952,419 |
| why do some plants eat insects | yes | Learn Bright 1,966,853 · Peekaboo Kidz 2,333,002 · Peekaboo Kidz 14,409,773 · Ze Frank 15,868,859 · BBC 13,770,762 |
| How Do Venus Flytraps Work? (The Plant That Counts to Five) | no | BBC 13,770,753 · BBC 801,804 · Peekaboo Kidz 2,333,002 · Colossal Cranium 1,352,996 · THE WILD PARADOX 404 |
| Carnivorous Plants: Why Darwin Fed Roast Beef to a Leaf | no | BBC 13,770,753 · Ze Frank 15,868,859 · Peekaboo Kidz 14,409,773 · ABC10 832 · SciShow 1,202,692 |
| The Plant That Counts to Five Before It Eats | no | Redbeard 3,840 · Biology Did What 947 · Odd Knowledge 50 · CurioFrame 15,123 · SCIENz 2,593 |
| How Does a Venus Flytrap Count to Five? | no | Now Wait, Why? 1,447 · Rude Plants 1,468 · BBC 801,804 · edushorts 131 · Brightnaut 2 |
| Why Do Venus Flytraps Eat Insects? (Darwin's Bog Test) | no | BBC 13,770,762 · Peekaboo Kidz 2,333,002 · Venus Flytrap World 46,664 · California_Carnivores 13,984 · Crazy Creatures 414,378 |

Raw pull: 02_Video-Projects/105_Ellis-Darwin-BurdonSanderson-Venus-Flytrap-Carnivorous-Plants/11_Upload-Package/evidence_2026-11-14_public_search.json
```

- **Title Collision Check (`evidence_2026-11-14_public_search.json`, audited across all 8 search hits per query in `J2811`):**
  - **Title A (`How Do Venus Flytraps Work? (The Plant That Counts to Five)`, `59 chars`, and `≤50`-char `How Do Venus Flytraps Work? (Counting to Five)`, `46 chars`):** **0 exact collisions**.
  - **Title B (`The Leaf That Counts to Five Before It Digests`, `46 chars`, or `How Do Venus Flytraps Work? (1873 Electric Leaf)`, `48 chars`):** **0 exact collisions**. *(Bare `The Plant That Counts to Five Before It Eats` [`44 chars`] is **rejected** because result #7 in `evidence_2026-11-14_public_search.json` collides verbatim with `The Know-It-Owl` `ay4_XzfjXm8` [`997` views, `0:31`], which was omitted by `public_search.py`'s top-5 stdout summary.)*
  - **Title C (`Carnivorous Plants: Why Darwin Fed Roast Beef to a Leaf`, `55 chars`):** **0 exact collisions** (starts verbatim with exact autocomplete phrase `"carnivorous plants"`).
  - **Short S01 (`How Does a Venus Flytrap Count to Five? (Two-Touch Test)`, `56 chars`) & Short S02 (`Why Do Venus Flytraps Eat Insects? (Darwin's Bog Test)`, `54 chars`):** **0 exact collisions**. *(Bare `How Does a Venus Flytrap Count to Five?` [`39 chars`] is **rejected** because result #6 in `evidence_2026-11-14_public_search.json` collides with `BearlyBelievable` `BL4G1n7g6VI` *How does a Venus flytrap count to five? 🪴* [`1,004` views, `0:21`].)*

---

### 2.4 Overlap Check Across Projects, Ideas, Backlog, WIP & Open PRs
Rechecked on `2026-11-14`:
- **`02_Video-Projects/` (`000`–`015`, `018`, `099`–`101` on `main`, plus `102` Ozone Hole and `103` Why Is the Sky Blue on open PRs `#572`/`#576`/`#577`):**
  - `006_How-Trees-Turn-Air-Into-Wood` covers van Helmont's willow tree, Priestley's mint-and-mouse bell jar, and Ingenhousz's underwater leaf bubbles (photosynthesis).
  - `012_Mendel-Pea-Plants` covers Gregor Mendel's pea-plant inheritance ratios.
  - `013_Darwin-Wallace-Evolution` covers natural selection, Galápagos finches, and Wallace's Ternate letter.
  - None covers carnivorous plants, John Ellis vs Linnaeus, Darwin's 1875 *Insectivorous Plants* bog-nitrogen feeding tests, Burdon-Sanderson's 1873 plant action potential, or Hedrich's 2016 five-touch counter.
- **`00_Brand/Channel-Setup/ideas/` (`011`–`095` & `IDEAS_2026-10-21_J0790.md` `096`–`097`):**
  - `073_Hales-Dixon-Joly-Transpiration-Trees` covers how tall trees pull water up xylem tubes via cohesion-tension.
  - `081_Darwin-Went-Auxin-Phototropism` covers how grass seedlings bend toward light via auxin hormone tips.
  - `091_Frank-Simard-Wood-Wide-Web` covers mycorrhizal fungi networks between tree roots.
  - None covers Venus flytraps or carnivorous plants.
- **`00_Brand/Channel-Setup/VIDEO_BACKLOG.json` & `orbit-with-ben/jobs/WIP.json`:** Not in active `hos` (`007`, `008`, `009`, `010`, `011`, `013`) and not in `next_hos` (`012`, `014`, `015`, `016`, `017`, `018`, `019`, `100`, `101`, or open PRs `102`, `103`).

---

## 3. Two Candidate Short Angles (22–27 s, Question Titles — UNVERIFIED CONCEPTS ONLY)

> **Important:** Neither Short below is cleared for VO or production. Every historical and scientific claim — including the 20-second two-touch calcium window and five-touch enzyme threshold in S01, and Darwin's roast-beef/glass/raindrop tests in S02 — must be verified with exact quotes in `SOURCES.md` through the `facts` lane before any Short script is locked.

| Short | Candidate Title (`0` exact collisions) | Frame-0 Visual Concept & Candidate Opening Idea (*UNVERIFIED*) | Candidate Payoff Idea (`≥70%` of runtime, *UNVERIFIED*) |
|---|---|---|---|
| **S01** | **How Does a Venus Flytrap Count to Five? (Two-Touch Test)** *(56 chars, disambiguated from `BL4G1n7g6VI`)* | **Frame 0 (`mode: "cover"`):** Full-bleed macro moving shot inside a Venus flytrap jaw as a beetle brushes a glowing sensory hair and a golden electrical ripple fires across the red lobe (`0%` Explorer, `0%` bars); `0.0 s` hook text: `TOUCH #1: WAIT` (`#FFE000` on `WAIT`). Candidate opening concept: a single raindrop or brush on a Venus flytrap hair will not close the trap — the plant is counting. | **Payoff (`≥70%` runtime, `<1.0 s` loop tail, zero CTA):** Touch 1 starts a ~20-second electrical calcium timer; Touch 2 snaps the jaws shut; and only after Touches 3, 4, and 5 from struggling prey does the plant flood the sealed stomach with digestive enzymes (verify exact 2016 Hedrich paper numbers in `SOURCES.md`). |
| **S02** | **Why Do Venus Flytraps Eat Insects? (Darwin's Bog Test)** *(54 chars)* | **Frame 0 (`mode: "cover"`):** Close moving shot of Charles Darwin's brass tweezers placing a tiny cube of roast beef onto a Venus flytrap / sundew leaf while a shard of glass sits ignored on an adjacent leaf (`0%` Explorer, `0%` bars); `0.0 s` hook text: `FED ROAST BEEF` (`#FFE000` on `BEEF`). Candidate opening concept: in the 1860s and 1870s, Charles Darwin fed his greenhouse plants tiny cubes of roast beef, egg white, glass, and chalk. | **Payoff (`≥70%` runtime, `<1.0 s` loop tail, zero CTA):** The leaves ignored glass and water drops but digested nitrogen-rich meat — proving bog plants evolved to hunt insects not for energy (which they still get from sunlight), but for the nitrogen missing from acidic swamp soil (verify exact 1875 *Insectivorous Plants* details in `SOURCES.md`). |
