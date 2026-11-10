# History of Science — Weekly Growth Audit Evidence Appendix (7 Nov 2026 · J2373)

Companion appendix to [`HOS_2026-11-07.md`](./HOS_2026-11-07.md). Contains the reconciled multi-window YTA matrix, per-video Long and Short tables, the 14-day two-target check (`60%` stayed-to-watch + `70%` average viewed), local re-cut specifications for non-public Shorts, and the 30-day competitor dataset.

---

## 1. Reconciled Channel Window Matrix (`snapshots/2026-11-07.json` & `channel_daily.json`)

| Metric | 7d Settled (`29 Oct – 4 Nov`) | Prior 7d (`22–28 Oct`) | `last7` Snapshot (`30 Oct – 4 Nov`, 6d) | 28d Settled (`8 Oct – 4 Nov`) | Prior 28d (`10 Sep – 7 Oct`) | Full Oct (`1–31 Oct`) | Full Sep (`1–30 Sep`) | Nov-to-Date (`1–4 Nov`, 4d) | Oct-to-Date (`1–4 Oct`, 4d) | Lifetime (`7 Nov 06:40Z`) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Views (daily rows)** | **517** | 609 | 406 | **2,987** | 335 | **2,769** | 588 | **235** | 8 | **3,593** live (`3,504` YTA) |
| **Views (per-video sum)** | — | — | **406** (`387`S / `19`L) | **2,970** (`2,914`S / `56`L) | — | — | — | — | — | **3,594** (`3,383`S / `211`L) |
| **Watch Time (min)** | **88** | 64 | **71** (`47`S / `19`L v-sum) | **349** (`275`S / `75`L) | 101 | **339** | 90 | **43** | 33 | **469** settled |
| **Net Subscribers** | **`+3`** (`+3`/`0`) | `0` (`+1`/`−1`) | **`+3`** | **`+5`** (`+6`/`−1`) | `+1` | **`+3`** (`+5`/`−2`) | `+1` | **`+2`** (`+2`/`0`) | `0` | **`6` live** |
| **Likes / Shares** | `10` / `1` | `15` / `0` | `8` / `1` | `55` / `1` | `2` / `0` | `53` / `0` | `4` / `0` | `3` / `1` | `0` / `0` | **`59` likes** |

### 28-Day Traffic Sources (`last28` video sum `N = 2,970`: `2,914` Shorts + `56` Longs)

| Traffic Source (`insightTrafficSourceType`) | Shorts Views (`28d`) | Shorts Share | Longs Views (`28d`) | Longs Share | Combined Views (`28d`) | Combined Share |
|---|---:|---:|---:|---:|---:|---:|
| **`SHORTS` (Shorts feed)** | **2,282** | **78.3%** | `0` | `0.0%` | **2,282** | **76.8%** |
| **`YT_SEARCH` (YouTube search)** | **603** | **20.7%** | **13** | **23.2%** | **616** | **20.7%** |
| **`RELATED_VIDEO` (Suggested videos)** | `0` | `0.0%` | **27** | **48.2%** | **27** | **0.9%** |
| **`YT_OTHER_PAGE` (Browse / other YT)** | `17` | `0.6%` | `2` | `3.6%` | **19** | **0.6%** |
| **`NO_LINK_OTHER` (Direct / unknown)** | `4` | `0.1%` | `9` | `16.1%` | **13** | **0.4%** |
| **`YT_CHANNEL` (Channel page)** | `4` | `0.1%` | `1` | `1.8%` | **5** | **0.2%** |
| **`EXT_URL` (External)** | `4` | `0.1%` | `1` | `1.8%` | **5** | **0.2%** |
| **`SHORTS_CONTENT_LINKS` (Related video link)** | `0` | `0.0%` | **`2`** (`AL_-qlWko_g`, `GHZDsiH7L7A`) | **3.6%** | **2** | **0.1%** |
| **`SUBSCRIBER` (Browse / subscriptions)** | `0` | `0.0%` | `1` | `1.8%` | **1** | **0.03%** |
| **Total** | **2,914** | **100.0%** | **56** | **100.0%** | **2,970** | **100.0%** |

> **First `SHORTS_CONTENT_LINKS` Long Conversions Recorded:** In `last28`, `SHORTS_CONTENT_LINKS` generated its first **`2` long-form views** (`1` on `002` `AL_-qlWko_g` and `1` on `004` `GHZDsiH7L7A`), confirming that Related Video links on Shorts have begun sending viewers into the Longs.

---

## 2. Long-Form Performance & Packaging Audit (`6` Public Longs)

| Film & ID | Title | Published | Dur | Views (Live / YTA / St) | 7d / 28d Views | Impr (`Δ vs 26 Oct`) | Studio CTR (`Δ`) | AVD (St / YTA) | Avg Viewed (St / YTA) | `0:30` / End Ret. | Lifetime Traffic Mix & T&C Status |
|---|---|---|---:|---:|---:|---:|---:|---|---|---|---|
| **`001` `_C92tIJCk8A`** | *How Did We Discover Germs?* | `17 Sep` | `365 s` | `7` / `7` / `7` | `0` / `0` | `44` (`+3`) | **6.8%** (`−0.5 pp`) | `175 s` / `175 s` | **47.9%** / `47.88%` | `—` | `NO_LINK_OTHER:4`, `YT_CHANNEL:3` |
| **`002` `AL_-qlWko_g`** | *How Did We Discover the Periodic Table?* | `24 Sep` | `536 s` | **161** / **160** / **156** | **`+9`** / **`+25`** | **1,122** (`+52`) | **3.4%** (`+0.2 pp`) | `114 s` / `109 s` | **21.3%** / `20.16%` | **50%** / **11%** | `RELATED:89` (`55.6%`), `SEARCH:40` (`25.0%`), `OTHER:15`, `NO_LINK:7`, `CH:6`, `EXT:2`, `SHORTS_LINK:1` |
| **`003` `frP_YrNShsU`** | *How We Discovered X-Rays by Accident* | `1 Oct` | `425 s` | `5` / `5` / `5` | `0` / `4` | `41` (`+16`) | **2.4%** (`−1.6 pp`) | `113 s` / `112 s` | **26.5%** / `26.54%` | `—` | `NO_LINK_OTHER:3`, `YT_CHANNEL:2` |
| **`004` `GHZDsiH7L7A`** | *What's Really Inside an Atom?* | `8 Oct` | `525 s` | **31** / **30** / **29** | **`+4`** / **`+23`** | **811** (`+34`) | **1.1%** (`+0.1 pp`) | `96 s` / `92 s` (`244 s` in 7d!) | **18.3%** / `17.59%` (`46.5%` in 7d!) | **38%** / **6%** | `RELATED:16` (`53.3%`), `SEARCH:9` (`30.0%`), `NO_LINK:3`, `SHORTS_LINK:1`, `SUB:1` · **`+1` sub** · T&C armed `25 Oct` (`+34` impr, inconclusive) |
| **`005` `wwcjcFfC-5M`** | *The Tied Arm That Proved Your Blood Circulates* | `29 Oct` | `528 s` | `5` / `4` / `3` | `4` / `4` | `7` (`+7`) | **28.6%** | `76 s` / `60 s` | **14.4%** / `11.44%` | `—` | `NO_LINK_OTHER:3`, `EXT_URL:1` · T&C armed `25 Oct` (inconclusive) |
| **`006` `VbPubYd6Fbs`** | *The Willow Tree That Was Made of Air* | `5 Nov` | `475 s` | `2` / `—` / `—` | `—` (`+2` live) | `—` | `—` | `—` | `—` | `—` | Public `5 Nov 18:00Z` (`2` live views, `1` comment; T&C armed `25 Oct`) |

---

## 3. 14-Day Two-Target Check (`60%` Stayed-to-Watch + `70%` Average Viewed)

Per rule `4d` (`orbit-build-shorts.mdc` / `hos-build-shorts.mdc`), every HOS Short with a `48 h+` Studio read in the last 14 days (`24 Oct – 7 Nov 2026`, `studio_ctr.json` read `2026-11-04T14:56Z`) plus `xHnIi9GqOsM` (`5 Nov 11:30Z`, `52.6 h` old) is graded below on both targets:
- **Stayed-to-watch (`60%` floor):** `PASS ≥ 60%`, `WATCH 45–59.9%`, `MISS < 45%`, or `too few (<100 Studio views)` (descriptive only).
- **Average % viewed (`70%` floor / `100%` loop aim):** `LOOP ≥ 100%`, `PASS ≥ 70%`, `WATCH 50–69.9%`, `MISS < 50%` (`<100` Studio views noted as `too few`).
- **Six 60% stayed-to-watch rules:** **R1** Frame-0 moving video of titled subject (or still with `≥15%` zoom in `0–1.0 s`, `<25%` black, no year/place stamp); **R2** First word onset `≤ 0.15 s`; **R3** Surprising half of claim heard by `≤ 1.50 s` (no `>0.15 s` internal pause in sentence 1); **R4** First cut `≤ 3.0 s` & max hold `≤ 4.0 s`; **R5** Last word to loop `≤ 1.5 s` with no end-card/CTA in last `2.0 s`; **R6** Zero meta-promise lines.

| ID & Air Date | Title & Version | Studio Views (`YTA` / `Live`) | Stayed % & Grade (`60%` Floor) | Avg Viewed % & Grade (`70%` Floor) | R1: Frame-0 Source & Motion | R2: Onset | R3: Surprise Time (`≤1.5s`) | R4: 1st Cut & Max Hold | R5: Loop Tail & CTA | R6: Meta-Promise | Payoff Time (`≥70%`) & Loop Sentence | Rules Broken by Misses |
|---|---|---:|---|---|---|---|---|---|---|---|---|---|
| **`c2q7w0pgcn8`**<br>`19 Oct` (SA S1) | *Who Discovered Infrared Light?* (`v01`, `22.43 s`) | **495** (`531` / `545`) | **41.4% `MISS`** | **108.4% St / 111.5% YTA `LOOP`** | **FAIL** — NB2 still (`01_beyond_red_v01.jpg`, zoom `1.22→1.00` slows after `0.95 s`) | `0.13 s` PASS | **FAIL** — `2.84 s` (*"In 1800, [0.41s gap] a thermometer found light no one could see"*) | **FAIL** — `4.96 s` cut 1; `7.44 s` max hold (`s04`) | `0.31 s` PASS (no CTA) | PASS | `15.82 s` (`70.5%` PASS), loops into *"In 1800..."* | **Breaks R1, R3, R4** (`b08→b09` `1.79–2.02s` `−12.02 pp`; `b35→b36` `7.85–8.07s` `−12.40 pp`) |
| **`gh96Yl9385A`**<br>`21 Oct` (SA S2) | *How the Deadliest Birth Clinic Was Fixed With Handwashing* (`v01`, `22.27 s`) | **20** (`17` / `23`) | **55.0%** (`too few <100`) | **86.8% St / 100.3% YTA** (`too few <100`) | **FAIL** — NB2 still (`01_two_wards_v01.jpg`, zoom `1.22→1.00`) | **FAIL** — `0.21 s` | **FAIL** — `1.92 s` (*"In 1847, [0.16s gap] washing hands..."*) | **FAIL** — `4.10 s` cut 1; `6.24 s` max hold | `0.31 s` PASS (no CTA) | PASS | `16.40 s` (`73.6%` PASS), loops | **Breaks R1, R2, R3, R4** (`<100` views, descriptive) |
| **`OnJ8MFu0Mi0`**<br>`26 Oct` (SA S3) | *How Did John Snow Stop Cholera?* (`v02`, `22.14 s`) | **231** (`231` / `231`, **`+1` sub**) | **29.6% `MISS`** | **65.7% St / 65.66% YTA `WATCH`** | **FAIL** — NB2 still (`05_handle_off_v03.jpg`, zoom `1.00→1.18`) | `0.06 s` PASS | **FAIL** — `2.76 s` (*"In 1854, [0.20s gap] a killer was hiding in a water pump"*) | **FAIL** — `4.66 s` cut 1; `6.38 s` max hold (`s02`) | `0.33 s` PASS (no CTA) | PASS | `15.70 s` (`70.9%` PASS), loops | **Breaks R1, R3, R4** (`b07→b08` `1.55–1.77s` `−8.93 pp`; `b21→b32` `4.65–7.08s` `−37.50 pp`) |
| **`-3L6HzJ_d_4`**<br>`27 Oct` (`001` `s11`) | *What Is the Pasteur Swan Neck Flask Experiment?* (`v07`, `18.17 s` / `19 s`) | **93** (`104` / `112`) | **73.1%** (`too few <100` St; **PASS pace**) | **64.4% St / 68.04% YTA** (`74.12%` in `last7`) | **PASS** — Moving Flow video (`01_question_mark_flask_v17.mp4`, `motion=11.51`, no zoom) | `0.00 s` PASS | **PASS** — `0.81 s` / `1.21 s` (*"a flask [0.13] stays [0.81] clear [1.21–1.68]"*) | **PASS** — `1.87 s` cut 1; `2.93 s` max hold (`s05`) | `0.97 s` PASS (no CTA) | PASS | `13.52 s` (`74.4%` PASS), loops (*"Keep the swan neck intact. → A flask stays clear."*) | **Breaks 0/6 rules** (`18.17 s` duration is below `22 s` floor; `91.3%` search traffic) |
| **`AMSriTQ-lcQ`**<br>`28 Oct` (SA S4) | *Are Marie Curie's Notebooks Still Radioactive?* (`v07`, `21.10 s` / `22 s`) | **269** (`270` / `270`) | **21.7% `MISS`** | **78.6% St / 78.61% YTA `PASS`** | **FAIL (R1 subject)** — Moving `003` Würzburg lab (`02_wurzburg_lab_establishing_v03.mp4`, `f0_diff=3.56`), no notebooks/lead box at frame 0 | `0.04 s` (`0.08 s` word) PASS | **FAIL** — `1.73 s` (*"Marie Curie's notebooks [0.70–1.32] are still [1.41–1.71] radioactive [1.73–2.55]"*) | **PASS** — `2.20 s` cut 1; `2.90 s` max hold (`s02`/`s03`/`s10`) | `0.98 s` PASS (no CTA) | PASS | `19.18 s` (`90.9%` PASS), loops (*"...lose half its strength. → Marie Curie's notebooks..."*) | **Breaks R1 (frame-0 subject mismatch: `003` X-ray lab instead of Curie notebooks) & R3 (`"radioactive"` at `1.73 s > 1.5 s`)** |
| **`Rl2uZ-KOTl8`**<br>`30 Oct` (`005` `s01`) | *Your Heart Pumps More Blood Than You Have* (`v04`, `24.07 s` / `25 s`) | **78** (`76` / `76`, **`+1` sub**) | **25.9%** (`too few <100`; MISS pace) | **53.6% St / 53.64% YTA** (`too few <100`; WATCH pace) | **WARN (R1 subject)** — Moving wrist finger-pulse (`01_pulse_wrist_t1.mp4`, `motion=27.43`), not heart/blood volume | `0.00 s` (`0.06 s` gate) PASS | **PASS** — `0.59 s` / `0.84 s` (*"You pump more [0.59] blood [0.84] than you have [1.24–2.14]"*) | **PASS** — `2.17 s` cut 1; `2.88 s` max hold (`s02`) | `0.57 s` PASS (no CTA) | PASS | `19.82 s` (`82.3%` PASS), loops (*"...going round and round. → You pump more blood..."*) | **Frame-0 wrist-pulse visual doesn't show `"more blood than you have"`, and `5.05–14.54 s` arithmetic setup slows mid-body retention** |
| **`BW_CFAX-mxc`**<br>`31 Oct` (`005` `s04`) | *Is the Heart a Pump?* (`v04`, `21.50 s` / `22 s`) | **86** (`86` / `89`) | **32.1%** (`too few <100`; MISS pace) | **84.0% St / 83.99% YTA** (`too few <100`; **PASS pace**) | **PASS** — Moving `05_heart_stove_t1.mp4` (`motion=24.39`, no zoom) | `0.03 s` PASS | **PASS** — `0.58 s` / `0.96 s` (*"The heart wasn't [0.58] a pump [0.96–1.41] at all"*) | **PASS** — `2.15 s` cut 1; `2.97 s` max hold (`s05–s08`) | `0.88 s` PASS (no CTA) | PASS | `16.62 s` (`77.3%` PASS), loops (*"...argue with his books. → The heart wasn't a pump..."*) | **Passes 6/6 rules technically** (`"warm stove"` counterpoint lands in sentence 2 at `2.53–3.97 s`; `<100` Studio views) |
| **`pWySvZsneZg`**<br>`1 Nov` (`004` `gold_foil`) | *Why Gold Foil Bounced Rutherford's Particles Back* (`v03`, `24.73 s` / `25 s`) | **127** (`130` / `130`, **`+1` sub**) | **35.6% `MISS`** | **115.3% St / 115.32% YTA `LOOP`** | **PASS** — Moving `12_shell_comes_back_v02.mp4` (`motion=33.05`, no zoom) | `0.00 s` (`0.05 s` gate) PASS | **FAIL** — `2.30 s` (*"Tiny particles [0.00–1.11] bounced back [1.18–2.07] off gold foil [2.30–3.19]"* — `"gold foil"` after `1.5 s`) | **PASS** — `2.75 s` cut 1; `3.75 s` max hold (`s06`) | `1.00 s` PASS (no CTA) | PASS | `22.94 s` (`92.8%` PASS), loops (*"...one tiny centre: the nucleus. → Tiny particles..."*) | **Breaks R3 (`"gold foil"` named at `2.30–3.19 s > 1.5 s` and `"shell at tissue paper"` analogy at `15.55 s`)**; achieves **`115.3% LOOP`** & **`+1` sub** |
| **`qW2OsD4mujc`**<br>`3 Nov` (`002` `four_elem`) | *The Four Elements Were Wrong* (`v03`, `23.57 s` / `24 s`) | **16** (`33` / `35`) | **62.5%** (`too few <100`; PASS pace) | **75.0% St / 204.33% YTA** (`too few <100`; LOOP pace) | **PASS** — Moving `03_four_elements_crumble_v01.mp4` (`motion=31.25`, no zoom) | `0.00 s` (`0.04 s` gate) PASS | **PASS** — `1.47 s` (*"Earth, air, fire and water [0.00–1.42] aren't [1.47–1.82] elements [1.87–2.39]"*) | **PASS** — `2.57 s` cut 1; `3.02 s` max hold (`s04`) | `1.00 s` PASS (no CTA) | PASS | `18.95 s` (`80.5%` PASS), loops (*"Two were light and heat. → Earth, air, fire..."*) | **Breaks 0/6 rules** (`<100` views, descriptive) |
| **`xHnIi9GqOsM`**<br>`5 Nov` (`005` `s05`) | *Why Do Veins Have Valves?* (`v03`, `22.17 s` / `23 s`) | `—` (`—` / `32` live) | Pending next Studio read | Pending next YTA read | **PASS** — Moving `13_one_way_t3.mp4` (`motion=14.00`, no zoom) | `0.00 s` (`0.13 s` gate) PASS | **WARN** — `"veins"` at `1.07 s`, `"knots"` at `2.59 s`, `"valve"` at `4.43 s` | **PASS** — `2.45 s` cut 1; `3.39 s` max hold (`s03`) | `1.35 s` PASS (no CTA) | PASS | `17.66 s` (`79.7%` PASS), loops (*"...slides through easily. → Along the swollen veins..."*) | Pending first 48h Studio read (published after `4 Nov 14:56Z` Studio read) |

---

## 4. Non-Public Shorts Status & Local Re-Cut Proposals (Local Renders Only · £0 Spend)

Per rule `4d`, we propose re-cuts **only for Shorts not yet public** (local renders only; any swap on YouTube goes to Ben first):

1. **Already Re-Cut & Swapped on Scheduled Slate (`7–21 Nov 2026`, `J0955` — No Further Action Needed unless Ben requests):**
   - `PFj6172YU4Q` (`005` `s02_the_tied_arm_v05`, airs Sun 8 Nov `11:30Z`): `26.27 s`, `0.06 s` onset, `"band"` at `0.27 s` / `"proved"` at `0.78 s`, `2.67 s` first cut, `3.65 s` max hold, `1.01 s` loop tail, `74.3%` payoff, 0 CTA. **Passes 6/6 rules.**
   - `xgx2lYHhYZM` (`007` `s05_vacca_jesty_v05`, airs Sat 14 Nov `11:30Z` — go-public-day Short for `007`): `24.53 s`, `0.02 s` onset, `"wasn't the first"` at `0.28 s`, `2.27 s` first cut, `3.48 s` max hold, `0.42 s` tail (`1.15 s` loop clip), `74.3%` payoff, 0 CTA. **Passes 6/6 rules.**
   - `Bks_JLId1ew` (`005` `s03_never_saw_v04`, airs Sun 15 Nov `11:30Z`): `25.26 s`, `0.06 s` onset, `"never saw"` at `0.50–0.78 s`, `2.04 s` first cut, `3.30 s` max hold, `1.00 s` loop tail, `80.7%` payoff, 0 CTA. **Passes 6/6 rules.**
   - `cLKDiYP55J8` (`007` `s04_smallpox_test_v04`, airs Tue 17 Nov `11:30Z`): `22.40 s`, `0.02 s` (`0.095 s` gate) onset, `"Jenner did the test"` at `0.02–1.10 s`, `1.18 s` first cut, `2.98 s` max hold, `0.42 s` tail (`1.15 s` loop clip), `89.8%` payoff, 0 CTA. **Passes 6/6 rules.**
   - `ChbsigHD5_o` (`004` `s05_dalton_v04`, airs Sat 21 Nov `11:30Z`): `24.53 s`, `0.08 s` onset, `"element"` at `0.31 s` (`"atom"` at `1.79 s`), `2.56 s` first cut, `3.77 s` max hold, `0.64 s` tail, `88.7%` payoff, 0 CTA.
2. **Unscheduled Local Renders & Plans to Re-Cut / Update Locally (`006–010` + `SA S5–S8`, £0):**
   - **`006` Local Built Shorts (`s04_photosynthesis_v01`, `s05_charcoal_gas_v01`, `s06_ingenhousz_oxygen_v01`, `s07_priestley_mint_v01`, `s08_willow_pot_v01`):** Strip the `3.0–3.2 s` `"watch the full film →"` CTA overlay (`≤1.0 s` loop tail), move `s04–s07` first cuts from `3.05–3.95 s` to `≤2.65 s`, and split `>4.0 s` holds (`s04:s03` `4.51 s`, `s05:s03` `5.31 s`, `s06:s04/s05` `4.41/4.08 s`, `s07:s04` `4.63 s`).
   - **`006` Locked `t1–t3` Shorts (`Short A` `t1_willow_air_vo_v02`, `Short B` `t2_mint_fixed_vo_v03`, `Short C` `t3_bubbles_sunlight_vo_v01`):** Assemble `Short B` (`21.60 s` VO + `0.80 s` loop = `22.40 s`) and `Short C` (`24.16 s` VO + `0.80 s` loop = `24.96 s`) first — both VOs already pass all 6 rules with `0.00 s` onset and surprise by `0.93–1.12 s`; trim the spoken title (`19.94–22.64 s`) from `Short A` before assembly.
   - **`007–010` Unscheduled Planned Shorts (`007 Short_B/C`, `008 Short_A/C`, `009 Short_A/B`, `010 Short_A/C` in `SHORTS_PICTURE_PLAN_v01.json`):** Update `SHORTS_PICTURE_PLAN_v01.json` before rendering so every `S01` first cut lands at `≤2.80 s` (`007 Short_B` `4.60→2.20 s`, `008 Short_C` `4.84→2.60 s`, `009 Short_B` `4.58→2.50 s`, `010 Short_A` `3.28→2.80 s`), unbundle every multi-plate body row (`4.1–10.96 s`) into `2.5–3.8 s` single-plate cuts, trim the `0.41 s` pause (`0.68→1.09 s`) in `009 Short_B_v02` VO, and end on a `≤1.0 s` loop tail with zero CTA.
   - **Standalone `S5–S8` (`hos_sa_s5_penzias_pigeons_v01`, `s6_fleming_mould_v01`, `s7_priestley_mint_v01`, `s8_hales_blood_v01`):** Trim `"In 1964,"` / `"In 1928,"` / `"In 1771,"` (`0.00–1.80 s`) from `S5–S7` so the surprise claim opens at `0.06 s`, move first cuts from `4.08–5.52 s` to `≤2.70 s`, split `4.1–5.6 s` holds, and swap `S7`'s stills for `006` Part 03 moving Veo mint/candle plates (`£0`).

---

## 5. Complete HOS Public Shorts Inventory (`27` Public Shorts at `7 Nov 2026`)

| # | ID | Published | Title | Dur | Live Views | YTA Views | Studio Views | Stayed % | Avg Viewed % (St / YTA) | 28d Feed / Search | Subs |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|---|---:|
| 1 | `29bpGAI0wb8` | `9 Oct` | *What happens if you keep cutting gold in half?* | `25 s` | **1,226** | `1,223` | `1,223` | **40.6%** | `44.0%` / `44.03%` | `1,152` / `61` | `0` |
| 2 | `c2q7w0pgcn8` | `19 Oct` | *Who Discovered Infrared Light?* | `23 s` | **545** | `531` | `495` | **41.4%** | **108.4%** / **111.53%** | `248` / **`279`** | `0` |
| 3 | `AMSriTQ-lcQ` | `28 Oct` | *Are Marie Curie's Notebooks Still Radioactive?* (`v07`) | `22 s` | **270** | `270` | `269` | **21.7%** | **78.6%** / **78.61%** | `227` / `41` | `0` |
| 4 | `OnJ8MFu0Mi0` | `26 Oct` | *How Did John Snow Stop Cholera?* (`v02`) | `23 s` | **231** | `231` | `231` | **29.6%** | `65.7%` / `65.66%` | `202` / `28` | **`+1`** |
| 5 | `clV6E10NLPw` | `22 Sep` | *The spray that stopped surgery killing patients* | `25 s` | **215** | `215` | `215` | **22.2%** | `53.2%` / `53.19%` | `0` / `0` (Sep) | **`+1`** |
| 6 | `oowAOWTBoq0` | `19 Sep` | *Why Childbed Fever Killed Mothers* | `25 s` | **192** | `191` | `192` | **33.2%** | `46.5%` / `46.51%` | `0` / `0` (Sep) | **`+1`** |
| 7 | `pWySvZsneZg` | `1 Nov` | *Why Gold Foil Bounced Rutherford's Particles Back* (`v03`) | `25 s` | **130** | `130` | `127` | **35.6%** | **115.3%** / **115.32%** | `54` / **`74`** | **`+1`** |
| 8 | `-3L6HzJ_d_4` | `27 Oct` | *What Is the Pasteur Swan Neck Flask Experiment?* (`v07`) | `19 s` | **112** | `104` | `93` | **73.1%** | `64.4%` / `68.04%` | `9` / **`95`** | `0` |
| 9 | `BW_CFAX-mxc` | `31 Oct` | *Is the Heart a Pump?* (`v04`) | `22 s` | **89** | `86` | `86` | **32.1%** | **84.0%** / **83.99%** | `64` / `20` | `0` |
| 10 | `tG3ce636-ac` | `11 Oct` | *Why Gold Is So Heavy* | `26 s` | **84** | `84` | `83` | **30.5%** | `42.2%` / `42.23%` | `82` / `2` | `0` |
| 11 | `Rl2uZ-KOTl8` | `30 Oct` | *Your Heart Pumps More Blood Than You Have* (`v04`) | `25 s` | **76** | `76` | `78` | **25.9%** | `53.6%` / `53.64%` | `64` / `11` | **`+1`** |
| 12 | `rI381l6N814` | `12 Oct` | *A Pea in a Stadium: How Empty Is an Atom?* | `27 s` | **69** | `69` | `68` | **27.8%** | `63.6%` / `63.64%` | `67` / `0` | `0` |
| 13 | `qW2OsD4mujc` | `3 Nov` | *The Four Elements Were Wrong* (`v03`) | `24 s` | **35** | `33` | `16` | **62.5%** | `75.0%` / **204.33%** | `4` / **`27`** | `0` |
| 14 | `xHnIi9GqOsM` | `5 Nov` | *Why Do Veins Have Valves?* (`v03`) | `23 s` | **32** | `—` | `—` | `—` | `—` | `—` | `0` |
| 15 | `gh96Yl9385A` | `21 Oct` | *How the Deadliest Birth Clinic Was Fixed With Handwashing* | `23 s` | **23** | `17` | `20` | **55.0%** | **86.8%** / **100.27%** | `7` / `9` | `0` |
| 16 | `tibf10a619M` | `3 Oct` | *His Wife Saw Her Own Skeleton and Said She Saw Death* | `25 s` | **16** | `16` | `16` | **11.1%** | `59.4%` / `59.44%` | `0` / `0` | `0` |
| 17 | `iT2cL_wF6z8` | `25 Sep` | *Why Hospitals Used to Smell Like Rot* | `26 s` | **8** | `8` | `8` | **80.0%** | `85.2%` / `85.23%` | `0` / `2` | `0` |
| 18 | `E0x65dEFv2w` | `15 Oct` | *He Left Gap Cards in the Periodic Table for Unfound Elements* | `24 s` | **7** | `7` | `7` | **60.0%** | `91.4%` / `91.45%` | `0` / `6` | `0` |
| 19 | `wCA91qef-p8` | `2 Oct` | *The First Medical X-Ray Was a Wedding Ring and Bones* | `25 s` | **7** | `7` | `7` | **50.0%** | `39.7%` / `39.72%` | `0` / `0` | `0` |
| 20 | `3A9tfdLBBP0` | `29 Sep` | *Why Doctors Refused to Wash Their Hands* | `27 s` | **6** | `6` | `6` | **60.0%** | `91.4%` / `91.37%` | `0` / `0` | `0` |
| 21 | `dZTN1 Cfb1Rw` | `17 Oct` | *Every Hospital Took X-Rays Within One Year* | `26 s` | **3** | `3` | `3` | **100.0%** | `79.6%` / `79.63%` | `0` / `1` | `0` |
| 22 | `T0caG2ba59I` | `26 Sep` | *He Played Chemical Solitaire on a Train and Built the Periodic Table* | `25 s` | **2** | `2` | `2` | `—` | `102.9%` / `102.92%` | `0` / `0` | `0` |
| 23 | `G_wca36019Q` | `27 Sep` | *He Predicted Three Unknown Elements and Their Weights* | `26 s` | **2** | `2` | `2` | **50.0%** | `69.9%` / `69.92%` | `0` / `0` | `0` |
| 24 | `O1eH26G2bZc` | `14 Oct` | *Why Couldn't Cathode Rays Pass Through Black Card?* | `23 s` | **1** | `1` | `1` | **100.0%** | `144.0%` / `144.04%` | `0` / `0` | `0` |
| 25 | `8hO_L3W24vM` | `18 Oct` | *Why Did Mendeleev Leave Gaps in the Periodic Table?* | `27 s` | **1** | `1` | `1` | `—` | `21.2%` / `21.22%` | `0` / `0` | `0` |
| 26 | `tE-hM6Y2gE0` | `5 Oct` | *Why X-Rays Go Straight Through Skin Ready-Made* | `25 s` | **1** | `1` | `1` | `0.0%` | `3.1%` / `3.12%` | `0` / `0` | `0` |
| 27 | `zM8K_9wG1kY` | `7 Oct` | *Why Did Mendeleev Put Iodine After Tellurium?* | `25 s` | **0** | `0` | `0` | `—` | `—` | `0` / `0` | `0` |

---

## 6. Competitor 30-Day Public Dataset (Signed-Out Fetch · 7 Nov 2026)

| Channel | Video ID | Title | Format | Published | Public Views | Packaging & Hook Takeaway for HOS |
|---|---|---|---|---|---:|---|
| **Veritasium** | `KfODG5REyss` | *I finally saw quantum physics with my own eyes...* | Long | `3 days ago` | **9.1M** | Macro-visible proof of an invisible phenomenon (matches `004` atom / `006` oxygen bubbles) |
| **Veritasium** | `eyZEqSPeMwg` | *No device could prove Einstein wrong... until now* | Long | `2 weeks ago` | **7.7M** | Apparatus-first historical test (*No device could prove X... until now*) |
| **Veritasium** | `NiCgcUTL9_Q` | *Fiber Optics are so much cooler than I thought* | Long | `3 weeks ago` | **15M** | Everyday technology traced back to its physical light-bending discovery |
| **Veritasium** | `JsBZOcqZerk` | *The Insane Real Engineering of the Nazi Enigma Machine* | Long | `1 month ago` | **21M** | Physical mechanism teardown of a famous historical instrument |
| **Veritasium** | `zEmabFZvdqA` | *What happens if I lower this weight into the water?* | Short | `<30d` | **3.2M** | Counter-intuitive scale/balance question (same physics-riddle shape as `006` Van Helmont's willow scale) |
| **Veritasium** | `Kap7mRzr13w` | *Why doesn't your heart get tired like other muscles do?* | Short | `<30d` | **1.4M** | Direct neighbour to `005` Harvey (*Your Heart Pumps More Blood Than You Have* / *Is the Heart a Pump?*) |
| **TED-Ed** | `8RPK5KwYhgA` | *What if you didn't brush your teeth for a year? - Justin Merritt* | Long | `9 days ago` | **1.2M** | Bodily microbial stakes + concrete time horizon (`for a year`) |
| **TED-Ed** | `av3zdxYvCp8` | *3 things to never do with a credit card* | Long | `3 weeks ago` | **1.1M** | Direct utility / numbered stakes |
| **TED-Ed** | `h6CmKF-mN2U` | *Which is better: Buying or renting a home? - Ella Feldman* | Long | `4 weeks ago` | **773K** | Head-to-head comparison framing |
| **TED-Ed** | `8EtdC9Bjubk` | *Can you solve the Billy Bonka riddle? - Edwin F. Meyer* | Long | `4 days ago` | **631K** | Math/proportion riddle (`631K` in 4d) |
| **SciShow** | `1nVwqDL3XCI` | *AI Psychosis Is Killing People. It's Time to Talk About It* | Long | `9 days ago` | **920K** | High-urgency medical/psychological phenomenon |
| **SciShow** | `i7esSCr2UJk` | *Why Is There No Vitamin F?* | Long | `2 days ago` | **554K** | Naming-gap mystery in medical/biochemical history (`554K` in 48h — validates Idea #3 & `007` *Why Vaccines Are Named After a Cow*) |
| **SciShow** | `dfA_VA20A2Y` | *How To Hold Something That's 10,000,000 Degrees* | Long | `10 days ago` | **248K** | Extreme scale number in title |
| **SciShow** | `cqDZt0BOlBI` | *The Plane Crash That Gave Us Cataract Surgery* | Long | `2 weeks ago` | **186K** | *The [Unexpected Event] That Gave Us [Medical Breakthrough]* — exact HOS title template |
| **SciShow** | `M6nefnNpOZA` | *What Was the First Alcohol?* | Long | `3 days ago` | **179K** | *What Was the First [Everyday Substance]?* |
| **Real Engineering** | `6B96xetwrqI` | *The Plane That's 38% Nose* | Long | `1 month ago` | **2.5M** | Specific physical percentage anomaly (`38% Nose` vs `556K` for generic *Rise and Fall of the Concorde*) |
| **Real Engineering** | `y1KipwEoRBA` | *The Rise and Fall of the Concorde* | Long | `8 days ago` | **556K** | Chronicle framing underperforms anomaly framing by `4.5×` |
| **Kings and Generals** | `H2xV6FnbSkQ` | *Why Spain Collapsed Into Civil War* | Long | `11 days ago` | **439K** | Causal `Why [System] Collapsed` hook |
| **Kings and Generals** | `hSMwc_RRqiQ` | *How the Ottomans Became a Superpower and Tripled in Size* | Long | `13 days ago` | **363K** | Causal `How` + concrete multiplier (`Tripled in Size`) |
| **Big Think** | `HdJxqW0-uZA` | *The shock of doing nothing | Andrew Holecek* | Long | `3 weeks ago` | **692K** | Paradoxical 5-word hook |
| **Big Think** | `XfxQL1LP2BM` | *1 in 6 people are narcissists. Learn to spot them early* | Long | `8 days ago` | **287K** | Concrete ratio opener (`1 in 6`) |
| **Big Think** | `8RUjEGFFLTc` | *The famous tree-falling thought experiment has a new answer* | Long | `2 weeks ago` | **188K** | Classic science thought experiment overturned (`new answer`) |
