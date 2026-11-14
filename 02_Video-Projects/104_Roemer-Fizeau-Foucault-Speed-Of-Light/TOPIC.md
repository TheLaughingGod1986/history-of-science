# Topic Brief — `HOS:104` (`104_Roemer-Fizeau-Foucault-Speed-Of-Light`)

> **RULE-E TOPIC REVIEW & UNVERIFIED CLAIMS NOTICE (`J2809` / `J2810`, 14 Nov 2026):**
> This topic (`HOS:104`) passed its **Rule-E topic go/no-go review (`J2810`: `GO`, `96 / 100` · `9.60 / 10` Opportunity Score)** and stays pre-cleared in **`jobs/WIP.json` `next_hos` (Rule G)** awaiting an open active HOS WIP slot (`len(WIP.json["hos"]) < 6`).
> - **All historical and scientific claims in §2 and §3 remain UNVERIFIED working notes** and are **NOT CLEARED FOR NARRATION OR SHORT OPENS**.
> - `01_Script/episode_script_draft_v01.md` remains the blank template. Before any script lock, every claim, date, distance, tooth count, RPM, and speed figure must be backed by an exact quote in `SOURCES.md` and verified through the `facts` lane (`gemini-agy`).

---

## Summary Table

| Field | Value |
|---|---|
| **Film ID & Folder** | `HOS:104` · `02_Video-Projects/104_Roemer-Fizeau-Foucault-Speed-Of-Light` |
| **Status** | Backlog proposal (`jobs/WIP.json` `next_hos`, Rule G) · `status.json` all stages `todo` · **Rule-E Topic Review: `GO` (`96 / 100`, `J2810`)** |
| **Rule-E Review Artifacts** | [`11_Upload-Package/TOPIC_GO_NO_GO_SHEET.md`](11_Upload-Package/TOPIC_GO_NO_GO_SHEET.md) · [`11_Upload-Package/TOPIC_OPPORTUNITY_SCORE.md`](11_Upload-Package/TOPIC_OPPORTUNITY_SCORE.md) |
| **Title A (Primary Proposal, Rule 26)** | `How Did We Measure the Speed of Light? (A 720-Tooth Wheel)` (`58 chars`, `0` exact collisions) |
| **Title B (Test & Compare, Rule 23)** | `The 720-Tooth Wheel That Measured the Speed of Light` (`52 chars`, `0` exact collisions) |
| **Title C (Rule 26 Exact Phrase First)** | `Speed of Light: How a 720-Tooth Wheel Measured It in 1849` (`57 chars`, `0` exact collisions) |
| **Short S01 (Candidate Question Title)** | `How Did Jupiter's Moons Measure the Speed of Light?` (`51 chars`, `0` exact collisions) |
| **Short S02 (Candidate Question Title)** | `Why Does Light Slow Down in Water? (Foucault's 1850 Test)` (`57 chars`, `0` exact collisions) |
| **Autocomplete (`public_search.py`, `2026-11-14`)** | `"how did we measure the speed of light"` = **yes** · `"speed of light"` = **yes** |
| **Rule 26 Ranking Videos (`2026-11-14`)** | 1) **Veritasium** [`pTn6Ewhb27k`](https://youtu.be/pTn6Ewhb27k) *Why No One Has Measured The Speed Of Light* (**`24,352,264` views**) · 2) **Rational Thinker** [`Jl1I4MA-TaU`](https://youtu.be/Jl1I4MA-TaU) *How the Speed of Light Was First Measured* (**`2,001,964` views**) |
| **Neighbour Gate (`neighbours.py`, `2026-11-14`)** | **PASS** — **`11` education videos `≥1,000,000` views** (`TED-Ed/TED: yes`, led by Veritasium `24.35M`, Veritasium `17.60M`, Vsauce `10.05M`, Kurzgesagt `9.99M`, PBS Space Time `7.13M`, minutephysics `4.30M`, TED-Ed `3.70M`, Veritasium `2.29M`, TED-Ed `1.82M`, TED-Ed `1.28M`, TED-Ed `1.02M`) |
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

## 2. Topic Proposal — `HOS:104` (*How Did We Measure the Speed of Light? (A 720-Tooth Wheel)*)

> **UNVERIFIED HISTORICAL & SCIENTIFIC CLAIMS NOTICE:**
> Every date, person, instrument detail, and scientific number in §2 and §3 below — including Galileo's 1638 lantern test, Ole Rømer's 1676 Jupiter moon Io eclipse timing numbers, Hippolyte Fizeau's 1849 720-tooth brass wheel RPM/distance/speed numbers across Paris, and Léon Foucault's 1850/1862 rotating-mirror water-tube and speed numbers — is **UNVERIFIED** and **NOT CLEARED FOR NARRATION OR SHORT OPENS**. No spoken script draft is approved (`01_Script/episode_script_draft_v01.md` remains the blank template). Before any script lock, every claim must be backed by an exact quote in `SOURCES.md` and verified through the `facts` lane (`gemini-agy`).

### 2.1 One-Line Hook & Candidate Discovery Outline (Unverified Working Notes)
- **One-line hook (unverified):** Before anyone had electronics or lasers, a French physicist in a Paris tower spun a 720-tooth brass wheel in front of a lantern beam aimed at a mirror five miles away — and timed the speed of light on Earth by watching a spinning brass tooth block the returning flash.
- **Candidate 4-act outline to verify in `SOURCES.md` before scripting:**
  1. **Galileo Galilei (*Two New Sciences*, 1638, *UNVERIFIED*):** Proposes that two observers with covered lanterns stand on distant hilltops, uncovering the second lantern when they see the first. Concludes only that light is either instantaneous or extraordinarily fast compared to human hand reaction time. *(Requires exact quote from Galileo's 1638 *Discorsi* in `SOURCES.md`.)*
  2. **Ole Rømer & Giovanni Domenico Cassini (Paris Observatory, 1676, *UNVERIFIED*):** Timing the eclipses of Jupiter's innermost moon **Io** as it disappears behind Jupiter's shadow. Rømer notices that when Earth is moving away from Jupiter, the eclipses arrive progressively later than when Earth is moving toward Jupiter — because light takes extra minutes to cross Earth's orbit. Christiaan Huygens later uses Rømer's delay to estimate the first finite speed of light. *(Requires exact quotes from Rømer's December 1676 *Journal des Sçavans* paper and Huygens's 1690 *Traité de la Lumière* in `SOURCES.md`.)*
  3. **Hippolyte Fizeau (Suresnes to Montmartre, Paris, July 1849, *UNVERIFIED*):** Replaces astronomical distances with a mechanical clockwork chopper: a **720-tooth brass cogwheel** spun by weights and gears. A beam of light passes through a gap between two teeth, travels ~8.63 km across Paris to a mirror on Montmartre, and reflects back. As Fizeau speeds up the wheel (to ~12.6 revolutions per second), the next brass tooth rotates into place just in time to eclipse the returning flash — yielding the first terrestrial measurement of the speed of light (~313,000–315,000 km/s). *(Requires exact quote from Fizeau's 1849 *Comptes Rendus* paper on tooth count, path length, rotation rate, and calculated speed in `SOURCES.md`.)*
  4. **Léon Foucault (Paris, 1850 & 1862, *UNVERIFIED*):** Replaces the toothed wheel with a high-speed steam/air-driven **rotating mirror** inside a room, sending one beam through air and one through a tube of **water** (1850) to prove light travels **slower in water than in air** (deciding the century-long corpuscular vs wave debate against Newton's particle prediction), and in 1862 refines the speed of light in air to ~298,000 km/s (within <1% of the modern value). *(Requires exact quotes from Foucault's 1850 and 1862 *Comptes Rendus* papers in `SOURCES.md`.)*
- **Planned Teach-on-Screen Visuals (Once Sourced):** `SCALE + DATA`: Earth–Jupiter orbital chord diagram showing Io eclipse delay; `DATA`: Fizeau's 720-tooth wheel RPM vs returning beam brightness drop to zero; `DATA`: Air vs water beam deflection angle in Foucault's rotating mirror; `WHEN`: timeline cards (`1638 -> 1676 -> 1849 -> 1850/1862`).
- **3-Way Thumbnail Concept Plan (Rule 12 / Rule 14 — Concepts Only, Zero Spend):**
  - **Thumb A (Mechanical Apparatus):** Painted 3D house style: close-up of Fizeau's gleaming brass **720-tooth cogwheel** spinning in a dark Paris tower as a razor-sharp golden beam of light is sliced off by a brass tooth, Explorer small lower-left, cream/gold serif text: `720 TEETH` (`2 words`).
  - **Thumb B (Rule 14 Bright High-Contrast Variant):** Bright daylight/twilight contrast over Paris rooftops: a brilliant golden beam shooting from a brass telescope across to a distant mirror on Montmartre while a giant brass gear turns in the foreground; serif text: `TIMED BY GEARS` (`3 words`).
  - **Thumb C (Astronomical Scale):** Glowing Jupiter and its moon Io casting a sharp black shadow cone toward a brass Paris Observatory telescope and pocket watch; serif text: `22 MINUTES LATE` *(exact number to be verified in `SOURCES.md` before any render)*.

### 2.2 Why Our Data Suggests Testing This Topic (Hypotheses, Not Guarantees)
1. **Plain Curriculum Search Question + Massive Education Neighbour Cluster (Hypothesis):** Our only two longs above `800` lifetime impressions (`002` Periodic Table `1,141` impr, `3.42%` CTR, `2.8–2.9/day`; `004` Atom `816` impr, `1.1/day`) ask plain school-physics/chemistry questions. `"how did we measure the speed of light"` and `"speed of light"` are both verified YouTube GB autocomplete phrases (`suggest = yes`, `2026-11-14`), and `neighbours.py` returns **`11` education videos above `1,000,000` views** (`Veritasium` `24.35M` and `17.60M`, `Vsauce` `10.05M`, `Kurzgesagt` `9.99M`, `PBS Space Time` `7.13M`, `minutephysics` `4.30M`, plus four `1M–3.7M` `TED-Ed` lessons). Moreover, on our Shorts, `c2q7w0pgcn8` (*Who Discovered Infrared Light?*) is `#2` on the entire channel by both stayed-to-watch (`43.52%`) and avg % viewed (`105.30%`), suggesting physics-of-light experiments hold viewer attention when anchored to a physical instrument.
2. **Concrete Mechanical Proof in the First 15 Seconds (Rule 10 & Rule 30 `HOS-2026-11-E2` Hypothesis):** Fizeau's spinning 720-tooth brass wheel physically chopping a lantern beam in half gives an unmistakable visual mechanism for the `0:05–0:15` proof-first window (avoiding any early agenda line).

### 2.3 Evidence — `neighbours.py` (`PASS`, `11` Videos `≥1M`) & `public_search.py` (`2026-11-14`)

#### A. Pasted `neighbours.py` Output (`2026-11-14`, Saved at `11_Upload-Package/evidence_2026-11-14_neighbours.json`)

```text
$ python3 00_Brand/Channel-Setup/tools/neighbours.py "how did we measure the speed of light" "speed of light" "fizeau" --out 02_Video-Projects/104_Roemer-Fizeau-Foucault-Speed-Of-Light/11_Upload-Package/evidence_2026-11-14_neighbours.json
| # | Channel | Views | Title | Found by |
|---|---|---|---|---|
| 1 | TED-Ed ★ | 3,695,293 views | [Light seconds, light years, light centuries: How to measure extreme distances - Yuan-Sen Ting](https://youtu.be/Op3AYaJc0Xw) | how did we measure the speed of light |
| 2 | TED-Ed ★ | 1,816,164 views | [Is light a particle or a wave? - Colm Kelleher](https://youtu.be/J1yIApZtLos) | ted-ed speed of light |
| 3 | TED-Ed ★ | 1,276,309 views | [Light waves, visible and invisible](https://youtu.be/O0PawPSdk28) | ted-ed speed of light |
| 4 | TED-Ed ★ | 1,015,443 views | [How fast is the speed of thought? - Seena Mathew](https://youtu.be/g12bxfYVhMk) | how did we measure the speed of light ted |
| 5 | TED-Ed ★ | 332,553 views | [What light can teach us about the universe - Pete Edwards](https://youtu.be/HZ7hwUduMoU) | ted-ed speed of light |
| 6 | TED ★ | 148,602 views | [Ed Boyden: A light switch for neurons](https://youtu.be/hupHAPF1fHY) | fizeau ted |
| 7 | Veritasium | 24,352,264 views | [Why No One Has Measured The Speed Of Light](https://youtu.be/pTn6Ewhb27k) | how did we measure the speed of light |
| 8 | Veritasium | 17,596,419 views | [There Is Something Faster Than Light](https://youtu.be/NIk_0AW5hFU) | speed of light ted |
| 9 | Vsauce | 10,047,754 views | [Would Headlights Work at Light Speed?](https://youtu.be/ACUuFg9Y9dY) | ted-ed speed of light |
| 10 | Kurzgesagt – In a Nutshell | 9,990,677 views | [What Is Light?](https://youtu.be/IXxZRZxafEQ) | ted-ed speed of light |
| 11 | PBS Space Time | 7,134,459 views | [The Speed of Light is NOT About Light](https://youtu.be/msVuCEs8Ydo) | ted-ed how did we measure the speed of light |
| 12 | minutephysics | 4,304,501 views | [How to break the speed of light](https://youtu.be/lR4tJr7sMPM) | ted-ed speed of light |

Words the top neighbours share: is light, the speed, speed of
TED-Ed/TED neighbour: yes
Big neighbours (≥ 1,000,000 views): 11 (need 3)
Neighbour gate (≥ 3 education videos with 1,000,000+ views): PASS
Raw pull: 02_Video-Projects/104_Roemer-Fizeau-Foucault-Speed-Of-Light/11_Upload-Package/evidence_2026-11-14_neighbours.json
```

*(Note: The 11th `≥1M` neighbour in `evidence_2026-11-14_neighbours.json` beyond the top-12 table above is `Veritasium` [`vVKFBaaL4uM`](https://youtu.be/vVKFBaaL4uM) *Can You Go the Speed of Light?* at **`2,289,873` views**, alongside `3Blue1Brown` [`KTzGBJPuJwM`](https://youtu.be/KTzGBJPuJwM) *But why would light "slow down"? | Visualizing Feynman's lecture on the refractive index* at **`2,896,005` views**, `Rational Thinker` [`Jl1I4MA-TaU`](https://youtu.be/Jl1I4MA-TaU) *How the Speed of Light Was First Measured* at **`2,001,964` views**, `Fermilab` [`CUjt36SD3h8`](https://youtu.be/CUjt36SD3h8) *Why does light slow down in water?* at **`1,309,684` views**, and `Susskind Speaks` [`QqcLRZdVBIg`](https://youtu.be/QqcLRZdVBIg) *Why the Speed of Light Is NOT a Speed - Leonard Susskind* at **`1,130,896` views** in `evidence_2026-11-14_public_search.json`.)*

#### B. Pasted `public_search.py` Output & Title Collision Check (`2026-11-14`, Saved at `11_Upload-Package/evidence_2026-11-14_public_search.json`)

```text
$ python3 00_Brand/Channel-Setup/tools/public_search.py "how did we measure the speed of light" "speed of light" "How Did We Measure the Speed of Light? (A 720-Tooth Wheel)" "Speed of Light: How a 720-Tooth Wheel Measured It in 1849" "The 720-Tooth Wheel That Measured the Speed of Light" "How Did Jupiter's Moons Measure the Speed of Light?" "Why Does Light Slow Down in Water? (Foucault's 1850 Test)" --out 02_Video-Projects/104_Roemer-Fizeau-Foucault-Speed-Of-Light/11_Upload-Package/evidence_2026-11-14_public_search.json
| Phrase | Autocomplete? | Top results (GB) |
|---|---|---|
| how did we measure the speed of light | yes | Think Like Feynman 52,487 · Rational Thinker 2,001,964 · Carter Studios - Physics 799,836 · Veritasium 24,352,264 · Science Simplified 4 All 15,073 |
| speed of light | yes | Feynman Reborn 254,511 · Veritasium 24,352,264 · The Sleepy Scientist  53,862 · Calm Space 7,646 · Sleep On Science 80,681 |
| How Did We Measure the Speed of Light? (A 720-Tooth Wheel) | no | Rational Thinker 2,001,976 · ayuta 512,450 · SlightlyTechnical 19 · uclaphysicsvideo 281,879 · Orbit with Ivy 27 |
| Speed of Light: How a 720-Tooth Wheel Measured It in 1849 | no | SlightlyTechnical 19 · Rational Thinker 2,001,956 · ayuta 512,454 · Beautiful Experiments 54 · 邱博文 9 |
| The 720-Tooth Wheel That Measured the Speed of Light | no | Orbit with Ivy 27 · SlightlyTechnical 19 · AlphaPhoenix 330,599 · Rational Thinker 2,001,964 · ayuta 512,454 |
| How Did Jupiter's Moons Measure the Speed of Light? | no | SciShow Space 214,651 · David Butler 20,436 · Tycho 3,990 · VideoFromSpace 3,315 · Rational Thinker 2,001,976 |
| Why Does Light Slow Down in Water? (Foucault's 1850 Test) | no | FloatHeadPhysics 152,451 · Fermilab 1,309,684 · Looking Glass Universe 116,595 · Arvin Ash 303,924 · 3Blue1Brown 2,896,005 |

Raw pull: 02_Video-Projects/104_Roemer-Fizeau-Foucault-Speed-Of-Light/11_Upload-Package/evidence_2026-11-14_public_search.json
```

- **Title Collision Check (`evidence_2026-11-14_public_search.json`):**
  - **Title A (`How Did We Measure the Speed of Light? (A 720-Tooth Wheel)`):** **0 exact collisions**.
  - **Title B (`The 720-Tooth Wheel That Measured the Speed of Light`):** **0 exact collisions**.
  - **Title C (`Speed of Light: How a 720-Tooth Wheel Measured It in 1849`):** **0 exact collisions** (starts verbatim with exact autocomplete phrase `"speed of light"`).
  - **Short S01 (`How Did Jupiter's Moons Measure the Speed of Light?`) & Short S02 (`Why Does Light Slow Down in Water? (Foucault's 1850 Test)`):** **0 exact collisions**.

---

### 2.4 Overlap Check Across Projects, Ideas, Backlog, WIP & Open PRs
Rechecked on `2026-11-14`:
- **`02_Video-Projects/` (`000`–`015`, `018`, `099`–`101` on `main`, plus `102` Ozone Hole and `103` Why Is the Sky Blue on open PRs `#572`/`#576`/`#577`):**
  - `018_Herschel-Ritter-Infrared` covers William Herschel's 1800 prism thermometer discovery of infrared heat and Johann Ritter's 1801 silver-chloride discovery of ultraviolet light — spectrum wavelengths, not the velocity of light.
  - `103_Rayleigh-Einstein-Smoluchowski-Blue-Sky` (open PR `#572`/`#576`/`#577`) covers atmospheric Rayleigh scattering and why the sky is blue.
  - None covers Galileo's 1638 lantern test, Ole Rømer's 1676 Io eclipse timing, Hippolyte Fizeau's 1849 720-tooth cogwheel, or Léon Foucault's 1850/1862 rotating mirror.
- **`00_Brand/Channel-Setup/ideas/` (`011`–`095` & `IDEAS_2026-10-21_J0790.md` `096`–`097`):**
  - `025_Young-Fresnel-Einstein-Light` covers wave-particle duality (Thomas Young's 1801 double slit, Arago/Fresnel's 1818 Poisson bright spot, and Einstein's 1905 photoelectric effect); verified `025/TOPIC.md` has zero mention of Rømer, Fizeau, or Foucault's speed-of-light experiments.
  - `032_Michelson-Morley-Aether` covers the 1887 interferometer failure to detect the luminiferous aether wind.
- **`00_Brand/Channel-Setup/VIDEO_BACKLOG.json` & `orbit-with-ben/jobs/WIP.json`:** Not in active `hos` (`007`, `008`, `009`, `010`, `011`, `013`) and not in `next_hos` (`012`, `014`, `015`, `016`, `017`, `018`, `019`, `100`, `101`, or open PRs `102`, `103`).

---

## 3. Two Candidate Short Angles (22–27 s, Question Titles — UNVERIFIED CONCEPTS ONLY)

> **Important:** Neither Short below is cleared for VO or production. Every historical and scientific claim — including Rømer's eclipse delay minutes in S01 and Foucault's 1850 rotating-mirror water-tube setup in S02 — must be verified with exact quotes in `SOURCES.md` through the `facts` lane before any Short script is locked.

| Short | Candidate Title (`0` exact collisions) | Frame-0 Visual Concept & Candidate Opening Idea (*UNVERIFIED*) | Candidate Payoff Idea (`≥70%` of runtime, *UNVERIFIED*) |
|---|---|---|---|
| **S01** | **How Did Jupiter's Moons Measure the Speed of Light?** *(51 chars)* | **Frame 0 (`mode: "cover"`):** Full-bleed moving shot of Jupiter's moon Io disappearing into Jupiter's deep shadow while a brass Paris Observatory pocket watch ticks in the foreground (`0%` Explorer, `0%` bars); `0.0 s` hook text: `1676 ECLIPSE` (`#FFE000` on `1676`). Candidate opening concept: in 1676, Jupiter's moon Io arrived late to its own eclipse whenever Earth moved away from Jupiter. | **Payoff (`≥70%` runtime, `<1.0 s` loop tail, zero CTA):** Ole Rømer realised the moon wasn't slowing down — its light was taking extra minutes to cross Earth's orbit, giving humanity its first proof that light has a finite speed (verify exact minutes and Huygens's speed calculation in `SOURCES.md`). |
| **S02** | **Why Does Light Slow Down in Water? (Foucault's 1850 Test)** *(57 chars)* | **Frame 0 (`mode: "cover"`):** Close moving shot of a high-speed spinning brass mirror splitting a bright beam of light through a glass tube of water (`0%` Explorer, `0%` bars); `0.0 s` hook text: `SLOWER IN WATER` (`#FFE000` on `SLOWER`). Candidate opening concept: Isaac Newton predicted that light particles actually speed up when they enter water — until Léon Foucault tested it in 1850. | **Payoff (`≥70%` runtime, `<1.0 s` loop tail, zero CTA):** Using a steam-spun rotating mirror in Paris, Foucault showed the beam passing through water arrived later and deflected further than the beam in air — proving light slows down in water (verify exact 1850 setup details in `SOURCES.md`). |
