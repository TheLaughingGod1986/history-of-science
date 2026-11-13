# HOS 102 — Topic Proposal & Data Learnings (`J2748`, Corrected 13 Nov 2026)

| Field | Value |
|---|---|
| **ID / Folder** | `HOS:102` — `02_Video-Projects/102_Molina-Rowland-Farman-Ozone-Hole` |
| **Proposal Status** | **RULE-E TOPIC REVIEW: `GO` IN BACKLOG `next_hos` (`J2775`, `94.5 / 100`, 13 Nov 2026) — NOT YET IN ACTIVE PRODUCTION.** Waiting in `jobs/WIP.json` `next_hos` under Rule G (`4/4` HOS active slots full). No script lock, VO, or picture generation starts until an active HOS WIP slot opens and `SOURCES.md` + `facts` lane run. |
| **Working Title A (Rule 26 Search Question, `44 chars`, `0` exact collisions)** | **How Did We Find the Hole in the Ozone Layer?** |
| **Title B (Rule 23 Story + Stakes, `54 chars`, `0` exact collisions)** | **The Ozone Hole (Found by an Instrument From the 1950s)** |
| **Title C (Rule 26 Exact Search Phrase First + Stakes, `64 chars`, `0` exact collisions)** | **Hole in the Ozone Layer: How a 1950s Ground Instrument Found It** |
| **Verified Plain Search Phrases (`public_search.py`, retrieved `2026-11-13`)** | `"hole in the ozone layer"` (`autocomplete = yes`), `"ozone layer"` (`autocomplete = yes`), `"ozone hole"` (`autocomplete = yes`) |
| **Two Ranking Videos for Plain Search Phrase (`"hole in the ozone layer"` / `"ozone hole"`, retrieved `2026-11-13`)** | 1. **Vox** — *Why you don't hear about the ozone layer anymore* (`https://youtu.be/CaLOiGEDPJQ`, **`10,161,545` views**, retrieved `2026-11-13`)<br>2. **Astrum Earth** — *Why Nobody Talks About the Ozone Hole Anymore* (`https://youtu.be/EmaQVbdd6Ko`, **`1,673,345` views**, retrieved `2026-11-13`; alongside **TED-Ed** *Whatever happened to the hole in the ozone layer?* `https://youtu.be/5wVJeq4mLL0`, **`670,049` views**, #1 GB result for `"hole in the ozone layer"`) |
| **Saved Tool Evidence (`2026-11-13`)** | `11_Upload-Package/evidence_2026-11-13_neighbours.json` (`neighbours.py`)<br>`11_Upload-Package/evidence_2026-11-13_public_search.json` (`public_search.py`) |
| **Facts & Script Status** | **UNVERIFIED — NOT CLEARED FOR NARRATION OR SHORT OPENS.** No spoken draft is approved. All historical and scientific claims (including the remembered NASA satellite-processing story, Halley Bay Dobson values, and chlorine/ozone numbers) must be sourced with exact quotes in `SOURCES.md` and checked through the `facts` lane before any script lock. |
| **Spend** | **£0** (no paid API, TTS, or picture generation; no Studio or publish change) |

---

## 0. Mandatory Public-Search Probe (`J2748` Routing Preflight, 13 Nov 2026)

Per `J2748` routing instructions (`desk 6853484674`), `public_search.py` was probed from the Mac mini before making any corrections:

```text
$ python3 00_Brand/Channel-Setup/tools/public_search.py "why is the sky blue"
| Phrase | Autocomplete? | Top results (GB) |
|---|---|---|
| why is the sky blue | yes | NASA Space Place 937,894 · Nick Cope 614,119 · SciShow Kids 530,954 · StarTalk 3,394,674 · National Space Centre 33,168 |
```

---

## 1. Learn From Our Data First (Corrected Analytics Comparison — `2026-11-12` & `2026-11-13` Snapshots vs Lifetime Studio Read)

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

## 2. Topic Proposal — `HOS:102` (*How Did We Find the Hole in the Ozone Layer?*)

> **UNVERIFIED HISTORICAL & SCIENTIFIC CLAIMS NOTICE (Correction 4):**
> Every date, person, instrument detail, and scientific number in §2 and §3 below — including the remembered NASA Nimbus-7 satellite software/flagging story, the Halley Bay Dobson spectrophotometer readings, the chlorine-to-ozone catalytic destruction ratio, and the recovery forecast — is **UNVERIFIED** and **NOT CLEARED FOR NARRATION OR SHORT OPENS**. No spoken script draft is approved (`01_Script/episode_script_draft_v01.md` remains the blank template). Before any script lock, every claim must be backed by an exact quote in `SOURCES.md` and verified through the `facts` lane (`gemini-agy`).

### 2.1 One-Line Hook & Candidate Discovery Outline (Unverified Working Notes)
- **One-line hook (unverified):** In 1985 three British Antarctic Survey scientists using a 1950s ground-based optical instrument at Halley Bay reported that spring ozone overhead had fallen sharply since the 1970s — an atmospheric loss that satellite data-processing had not yet flagged in published reports.
- **Candidate 4-act outline to verify in `SOURCES.md` before scripting:**
  1. **Thomas Midgley Jr. (c. 1930, *UNVERIFIED*):** Synthesises chlorofluorocarbons (CFCs / Freon) as a non-flammable, non-toxic refrigerant and aerosol propellant. *(Requires exact primary/secondary source quote on date, compound, and demonstration.)*
  2. **Mario Molina & F. Sherwood Rowland (*Nature*, June 1974, *UNVERIFIED*):** Calculate that inert CFCs reach the stratosphere, where UV light cleaves chlorine radicals that catalytically destroy ozone ($O_3$). *(Requires exact quote from Molina & Rowland, Nature 249, 810–812, 1974 for the mechanism and any catalytic number.)*
  3. **Joe Farman, Brian Gardiner & Jonathan Shanklin (*Nature*, May 1985, *UNVERIFIED*):** Measure steep October ozone depletion over Halley Bay, Antarctica using a ground-based **Dobson spectrophotometer**. **Twist to verify carefully:** Check primary NASA/BAS historical sources on what Nimbus-7 TOMS recorded, why low values were initially flagged or overlooked, and when NASA confirmed the spatial map of the hole — do **not** narrate the "computers automatically threw out the data" version unless primary sources in `SOURCES.md` verify the exact mechanism.
  4. **Montreal Protocol (September 1987) & Recovery Forecast (*UNVERIFIED*):** International phase-out treaty signed in 1987; Molina, Rowland, and Crutzen share the 1995 Nobel Prize in Chemistry; verify current WMO/UNEP/NASA recovery projection dates in `SOURCES.md`.
- **Planned Teach-on-Screen Visuals (Once Sourced):** `DATA`: Halley Bay October total ozone (Dobson units) over time; `DATA + SCALE`: UV absorption in the stratosphere / catalytic cycle diagram; `WHEN`: timeline cards (`1930 -> 1974 -> 1985 -> 1987`); `WHO` cards for Midgley, Molina, Rowland, Farman.
- **3-Way Thumbnail Concept Plan (Rule 12 / Rule 14 — Concepts Only, Zero Spend):**
  - **Thumb A (Object / Instrument):** Painted 3D house style: the brass-and-steel **Dobson spectrophotometer** on the Antarctic snow at Halley Bay under a purple-blue polar sky hole on the right, Explorer small lower-left, cream/gold serif text on left band: `MISSED BY SPACE` (`3 words`).
  - **Thumb B (Rule 14 Bright High-Contrast Variant):** Bright sunlit 1950s kitchen/lab contrast: a gleaming chrome spray can releasing a green-tinted plume that rises into a split stratospheric ozone shield; serif text: `ONE SPRAY CAN` (`3 words`).
  - **Thumb C (Data / Map):** 3D globe of Antarctica with a deep violet cavity opening over the continent and a 1985 strip-chart line plunging downward; serif text: `1985 ALARM` (`2 words`).

### 2.2 Why Our Data Suggests Testing This Topic (Hypotheses, Not Guarantees)
1. **Plain Curriculum Search Noun + Rule 26 Search Demand (Hypothesis):** `"ozone layer"`, `"ozone hole"`, and `"hole in the ozone layer"` are active YouTube GB autocomplete phrases (`suggest = yes`, verified `2026-11-13` below), and `Vox` (`10.16M`), `Cleo Abram` (`8.53M`), `Peekaboo Kidz` (`4.28M`), `Seeker` (`2.49M`), `Astrum Earth` (`1.67M`), and `TED-Ed` (`670k`) demonstrate multi-million-view audience demand on YouTube. On our channel, the two longs that passed `800` impressions (`002` Periodic Table `1,141` impr, `3.42%` CTR; `004` Atom `816` impr) paired a school-science noun with large education neighbours (though `003` X-rays shows a plain question title can still stall at `41` impr if Suggested/Search traction does not kick in).
2. **Physical Instrument Proof in the First 15 Seconds (Rule 10 & Rule 30 `HOS-2026-11-E2` Hypothesis):** The Dobson spectrophotometer at Halley Bay and its falling October ozone chart provide a concrete physical apparatus and visual measurement for the `0:05–0:15` proof-first window (testing whether avoiding `005`/`006`'s early agenda line improves 0:15 and 0:30 hold toward `002`'s `70–71%` at `0:15` and `51%` at `0:30`).
3. **"Is It Still…?" Search Short Pairing (Rule 1, Rule 24, Rule 28 Hypothesis):** YouTube GB autocomplete for `"Is the Hole in the Ozone Layer Still There?"` returns `"is there still a hole in the ozone layer"` (`2026-11-13`), allowing us to test a search-intent `"Is X Still Y?"` Short shape alongside our `004` Short `AMSriTQ-lcQ` (*Are Marie Curie's Notebooks Still Radioactive?*, `274` views, `18.3/d` on `12 Nov`, `76.94%` Studio avg viewed, `22.66%` stayed — testing whether putting the Antarctic ozone map at Frame 0 improves stayed-to-watch over `AMSriTQ-lcQ`'s borrowed lab room).

---

### 2.3 Complete Neighbour & Public-Search Evidence (`2026-11-13`)

#### A. Three+ Actual On-Topic Education Videos (`≥1,000,000` Views) with URLs, View Counts & Retrieval Date
Retrieved `2026-11-13` via `neighbours.py` and `public_search.py` (saved in `11_Upload-Package/evidence_2026-11-13_neighbours.json` and `11_Upload-Package/evidence_2026-11-13_public_search.json`):

| # | Channel | Video Title & URL | View Count (Retrieved `2026-11-13`) | Length & Age | Relevance to `HOS:102` | Tool Source |
|---:|---|---|---:|---|---|---|
| **1** | **Veritasium** (`Tier 2` in `neighbours.py`) | [*The Man Who Accidentally Killed The Most People In History*](https://youtu.be/IV3dnLzthDA) | **`43,564,438` views** | `24:57` · 4 yr ago | Direct coverage of Thomas Midgley Jr.'s invention of CFCs (Freon), Rowland & Molina's stratospheric chlorine-ozone chemistry, and the Antarctic ozone hole | `neighbours.py` (`#12` in JSON) |
| **2** | **Vox** (Education/explainer via `public_search.py`) | [*Why you don’t hear about the ozone layer anymore*](https://youtu.be/CaLOiGEDPJQ) | **`10,161,545` views** | `8:35` · 4 yr ago | Direct history of the 1985 Antarctic ozone hole discovery, CFCs, and the 1987 Montreal Protocol | `public_search.py` (`"ozone layer"` `#4`, `"ozone hole"` `#6`) |
| **3** | **Cleo Abram** (Science explainer via `public_search.py`) | [*Something’s Happening to the Ozone Hole*](https://youtu.be/yWgHx0HE8m8) | **`8,528,291` views** | `16:09` · 2 mo ago | Direct explainer on the Antarctic ozone hole and its recovery | `public_search.py` (`"ozone hole"` `#7`) |
| **4** | **Peekaboo Kidz** (Education via `public_search.py`) | [*What Is The Ozone Layer? \| Ozone Layer Depletion \| Dr Binocs Show*](https://youtu.be/ckULkfv3Hb0) | **`4,284,034` views** | `6:49` · 6 yr ago | Curriculum explainer on the stratospheric ozone layer, UV shield, and CFC ozone depletion (`#1` GB result for `"ozone layer"`) | `public_search.py` (`"ozone layer"` `#1`) |
| **5** | **TED-Ed ★** (`Tier 1` in `neighbours.py`) | [*How a single-celled organism almost wiped out life on Earth - Anusuya Willis*](https://youtu.be/dO2xx-aeZ4w) | **`2,795,894` views** | `4:14` · 10 yr ago | Formation of Earth's oxygen atmosphere and stratospheric ozone layer | `neighbours.py` (`#1` in JSON) |
| **6** | **Seeker** (Science explainer via `public_search.py`) | [*What Ever Happened To The Hole In The Ozone Layer?*](https://youtu.be/0ZfBgjUnXIs) | **`2,494,747` views** | `4:30` · 10 yr ago | Direct explainer on the ozone hole and Montreal Protocol recovery | `public_search.py` (`"Is the Hole in the Ozone Layer Still There?"` `#7`) |
| **7** | **Astrum Earth** (Science explainer via `public_search.py`) | [*Why Nobody Talks About the Ozone Hole Anymore*](https://youtu.be/EmaQVbdd6Ko) | **`1,673,345` views** | `28:20` · 3 mo ago | Full documentary on CFCs, Molina & Rowland, Farman's Halley Bay discovery, and the Montreal Protocol (`#3` GB result for `"hole in the ozone layer"`) | `public_search.py` (`"hole in the ozone layer"` `#3`) |
| **8** | **Tom Scott** (`Tier 2` in `neighbours.py`) | [*Thomas Midgley Jr and a Pope Infestation: Citation Needed 5x02*](https://youtu.be/4og8wG8VQWM) | **`940,553` views** | `17:47` · 10 yr ago | Thomas Midgley Jr.'s CFC refrigerant invention | `neighbours.py` (`#14` in JSON) |
| **9** | **TED-Ed ★** (`Tier 1` in `neighbours.py`) | [*Whatever happened to the hole in the ozone layer? - Stephanie Honchell Smith*](https://youtu.be/5wVJeq4mLL0) | **`670,049` views** | `5:13` · 3 yr ago | Direct TED-Ed lesson on the ozone hole (`#1` GB result for `"hole in the ozone layer"` and `#2` for `"ozone layer"`) | `neighbours.py` (`#6` in JSON) & `public_search.py` (`#1`) |

#### B. Transparent Disclosure of `neighbours.py` Query Scope
- **How `neighbours.py` filters results:** `00_Brand/Channel-Setup/tools/neighbours.py` only counts videos from its hardcoded `TIER1` (`TED-Ed`, `TED`, `TEDx Talks`) and `TIER2` (`Kurzgesagt`, `Veritasium`, `SmarterEveryDay`, `minutephysics`, `SciShow`, `CrashCourse`, `3Blue1Brown`, `Numberphile`, `Stand-up Maths`, `Steve Mould`, `Practical Engineering`, `Real Engineering`, `Tom Scott`, `Be Smart`, `PBS Space Time`, ` PBS Eons`, `Royal Institution`, `Khan Academy`, `FuseSchool`, `Cognito`, `Natural History Museum`, `Wellcome Collection`) channel lists whose titles match words in `phrases`.
- **Narrow vs Broad `neighbours.py` Pull:** If `neighbours.py` is run strictly on `"ozone layer" "ozone hole"` alone, it returns `TED-Ed` `5wVJeq4mLL0` (`670,049` views), `FuseSchool` `J0bx2BuxT-I` (`218,515` views), `TED` `08z_xW-szwM` (`197,607` views), `Khan Academy` `E1P79uFLCMc` (`101,249` views), `Natural History Museum` `7QGD-KiqKdE` (`59,486` views), and `Khan Academy` `5CGtESB40Rc` (`23,563` views) — all under `1,000,000` views — because the four `1M–10M+` direct ozone-hole explainers (`Vox` `10.16M`, `Cleo Abram` `8.53M`, `Peekaboo Kidz` `4.28M`, `Seeker` `2.49M`, `Astrum Earth` `1.67M`) are on channels outside `neighbours.py`'s `TIER1`/`TIER2` list, and `Veritasium`'s `43.56M`-view film on Thomas Midgley's CFCs (`IV3dnLzthDA`) does not have the word `"ozone"` in its title.
- **Full `neighbours.py` Pull (`PASS`, `7` big neighbours `≥1M` views):** Including `"earth atmosphere"` and `"thomas midgley killed"` in `neighbours.py` captures `Veritasium` (`IV3dnLzthDA`, `43,564,438` views), `Kurzgesagt` (`JGXi_9A__Vc`, `14,084,839` views), and five `1M+` `TED-Ed` Earth-atmosphere/climate lessons (`2.80M`, `1.62M`, `1.58M`, `1.38M`, `1.38M`):

```text
$ python3 00_Brand/Channel-Setup/tools/neighbours.py "ozone layer" "ozone hole" "earth atmosphere" "thomas midgley killed" --out 02_Video-Projects/102_Molina-Rowland-Farman-Ozone-Hole/11_Upload-Package/evidence_2026-11-13_neighbours.json
| # | Channel | Views | Title | Found by |
|---|---|---|---|---|
| 1 | TED-Ed ★ | 2,795,894 views | [How a single-celled organism almost wiped out life on Earth - Anusuya Willis](https://youtu.be/dO2xx-aeZ4w) | ted-ed earth atmosphere |
| 2 | TED-Ed ★ | 1,615,069 views | [The mysterious origins of life on Earth - Luka Seamus Wright](https://youtu.be/de1hiS_XjWg) | ted-ed earth atmosphere |
| 3 | TED-Ed ★ | 1,582,917 views | [What Earth in 2050 could look like - Shannon Odell](https://youtu.be/2njn71TqkjA) | ted-ed ozone layer |
| 4 | TED-Ed ★ | 1,383,635 views | [Climate change: Earth's giant game of Tetris - Joss Fong](https://youtu.be/ztWHqUFJRTs) | ted-ed ozone layer |
| 5 | TED-Ed ★ | 1,378,649 views | [A guide to the energy of the Earth - Joshua M. Sneideman](https://youtu.be/fHztd6k5ZXY) | earth atmosphere ted |
| 6 | TED-Ed ★ | 670,049 views | [Whatever happened to the hole in the ozone layer? - Stephanie Honchell Smith](https://youtu.be/5wVJeq4mLL0) | ozone layer |
| 7 | TED-Ed ★ | 587,561 views | [The most lightning-struck place on Earth - Graeme Anderson](https://youtu.be/doy2BsHc-44) | ted-ed earth atmosphere |
| 8 | TED-Ed ★ | 442,984 views | [What's happening to Earth's core? - Shannon Odell](https://youtu.be/XLjdNXBZm3I) | ted-ed earth atmosphere |
| 9 | Veritasium | 43,564,438 views | [The Man Who Accidentally Killed The Most People In History](https://youtu.be/IV3dnLzthDA) | thomas midgley killed |
| 10 | Kurzgesagt – In a Nutshell | 14,084,839 views | [Everything You Need to Know About Planet Earth](https://youtu.be/JGXi_9A__Vc) | earth atmosphere |
| 11 | Tom Scott | 940,553 views | [Thomas Midgley Jr and a Pope Infestation: Citation Needed 5x02](https://youtu.be/4og8wG8VQWM) | thomas midgley killed ted |
| 12 | CrashCourse | 521,636 views | [What Does the Atmosphere Do? Crash Course Geography #6](https://youtu.be/11ZI9aqurfA) | earth atmosphere |

Words the top neighbours share: on earth, life on, shannon odell, to the
TED-Ed/TED neighbour: yes
Big neighbours (≥ 1,000,000 views): 7 (need 3)
Neighbour gate (≥ 3 education videos with 1,000,000+ views): PASS
Raw pull: 02_Video-Projects/102_Molina-Rowland-Farman-Ozone-Hole/11_Upload-Package/evidence_2026-11-13_neighbours.json
```

#### C. Pasted `public_search.py` Output & Title Collision Check (`2026-11-13`)

```text
$ python3 00_Brand/Channel-Setup/tools/public_search.py "hole in the ozone layer" "ozone layer" "ozone hole" "how did we find the hole in the ozone layer" "How Did We Find the Hole in the Ozone Layer?" "The Ozone Hole (Found by an Instrument From the 1950s)" "Is the Hole in the Ozone Layer Still There?" "Why Did a Satellite Miss the Ozone Hole?" --out 02_Video-Projects/102_Molina-Rowland-Farman-Ozone-Hole/11_Upload-Package/evidence_2026-11-13_public_search.json
| Phrase | Autocomplete? | Top results (GB) |
|---|---|---|
| hole in the ozone layer | yes | TED-Ed 670,049 · NOVA PBS Official 154,697 · Astrum Earth 1,673,345 · NASA Goddard 124,199 · ABC News (Australia) 122,410 |
| ozone layer | yes | Peekaboo Kidz 4,284,034 · TED-Ed 670,049 · Astrum Earth 1,673,345 · Vox 10,161,545 · NOVA PBS Official 154,697 |
| ozone hole | yes | NASA Earth 285,619 · TED-Ed 670,049 · Astrum Earth 1,673,345 · NOVA PBS Official 154,697 · NASA Goddard 124,199 |
| how did we find the hole in the ozone layer | no | Peekaboo Kidz 4,284,034 · TED-Ed 670,049 · NOVA PBS Official 154,697 · NASA Goddard 124,204 · Vox 10,161,546 |
| How Did We Find the Hole in the Ozone Layer? | no | NOVA PBS Official 154,697 · OpenMind 6,661 · TED-Ed 670,049 · Peekaboo Kidz 4,284,034 · NASA Goddard 124,205 |
| The Ozone Hole (Found by an Instrument From the 1950s) | no | OpenMind 6,661 · NOVA PBS Official 154,697 · Natural History Museum 59,486 · NASA Earth 285,622 · Daniel Izzo 10,640 |
| Is the Hole in the Ozone Layer Still There? | related: is there still a hole in the ozone layer | NOVA PBS Official 154,697 · TED-Ed 670,049 · NASA Goddard 238,984 · Vox 10,161,545 · JRE Clips 2,460,969 |
| Why Did a Satellite Miss the Ozone Hole? | no | CBC News 116,207 · Singularity Rewound 2 · TED-Ed 670,049 · NASA Goddard 238,984 · OpenMind 6,661 |

Raw pull: 02_Video-Projects/102_Molina-Rowland-Farman-Ozone-Hole/11_Upload-Package/evidence_2026-11-13_public_search.json
```

- **Title Collision Check (`evidence_2026-11-13_public_search.json`):**
  - **Title A (`How Did We Find the Hole in the Ozone Layer?`):** **0 exact collisions** (nearest is `NERCscience` `HiQTs2omG4M` *How did we discover the hole in the ozone layer?*, `462` views, 8 yr ago).
  - **Title B (`The Ozone Hole (Found by an Instrument From the 1950s)`):** **0 exact collisions**.
  - **Title C (`Hole in the Ozone Layer: How a 1950s Ground Instrument Found It`):** **0 exact collisions** (starts with exact autocomplete phrase `"hole in the ozone layer"`).
  - **Short S01 (`Is the Hole in the Ozone Layer Still There?`) & Short S02 (`Why Did a Satellite Miss the Ozone Hole?`):** **0 exact collisions**.

---

### 2.4 Overlap Check Across Projects, Ideas, Backlog & WIP (Correction 5)
Rechecked on `2026-11-13`:
- **`02_Video-Projects/` (`000`–`013`, `099`–`101`):** None covers CFCs, Molina/Rowland, Farman/Halley Bay, or stratospheric ozone depletion.
- **`00_Brand/Channel-Setup/ideas/` (`011`–`095` & `IDEAS_*.md`):** Idea `034_Foote-Tyndall-Arrhenius-Greenhouse` covers infrared heat absorption by $CO_2$ and water vapour (1856–1896), a completely different gas, mechanism, atmospheric layer, and cast. No idea folder covers the ozone layer or CFCs.
- **`00_Brand/Channel-Setup/VIDEO_BACKLOG.json` & `orbit-with-ben/jobs/WIP.json`:** Not in active `hos` (`007`, `008`, `009`, `010`, `011`, `013`) and not in `next_hos` (`012`, `014`, `015`, `016`, `017`, `100`, `101` prior to this PR).

---

## 3. Two Candidate Short Angles (22–27 s, Question Titles — UNVERIFIED CONCEPTS ONLY)

> **Important:** Neither Short below is cleared for VO or production. Every historical and scientific claim — especially the NASA satellite data-processing detail in S02 and the recovery timeline in S01 — must be verified with exact quotes in `SOURCES.md` through the `facts` lane before any Short script is locked.

| Short | Candidate Title (`0` exact collisions) | Frame-0 Visual Concept & Candidate Opening Idea (*UNVERIFIED*) | Candidate Payoff Idea (`≥70%` of runtime, *UNVERIFIED*) |
|---|---|---|---|
| **S01** | **Is the Hole in the Ozone Layer Still There?** *(43 chars; matches autocomplete `"is there still a hole in the ozone layer"`)* | **Frame 0 (`mode: "cover"`):** Full-bleed moving false-colour satellite map of the Antarctic ozone hole pulsing in spring (`0%` Explorer, `0%` bars); `0.0 s` hook text: `STILL OPEN?` (`#FFE000` on `STILL`). Candidate opening concept: state directly that the Antarctic ozone hole still opens every southern spring. | **Payoff (`≥70%` runtime, `<1.0 s` loop tail, zero CTA):** After the 1987 Montreal Protocol phased out CFCs, chlorine levels peaked and began falling; verify exact WMO/NASA forecast decade (`~2060s`) in `SOURCES.md` before scripting. |
| **S02** | **Why Did a Satellite Miss the Ozone Hole?** *(40 chars)* | **Frame 0 (`mode: "cover"`):** Close moving shot of the brass **Dobson spectrophotometer** on the Halley Bay ice as an overhead satellite pass blanks out a purple polar patch (`0%` Explorer, `0%` bars); `0.0 s` hook text: `MISSED FROM SPACE` (`#FFE000` on `MISSED`). Candidate opening concept: a 1950s ground instrument in Antarctica reported the ozone hole before NASA's satellite team did. | **Payoff (`≥70%` runtime, `<1.0 s` loop tail, zero CTA):** Verify in `SOURCES.md` how Farman, Gardiner, and Shanklin's May 1985 *Nature* paper prompted NASA to re-examine raw Nimbus-7 TOMS readings that had been flagged as out-of-range anomalies. |
