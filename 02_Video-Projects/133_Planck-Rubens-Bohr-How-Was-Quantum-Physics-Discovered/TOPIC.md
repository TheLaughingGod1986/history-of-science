# Topic Brief — `133_Planck-Rubens-Bohr-How-Was-Quantum-Physics-Discovered` (`HOS:133` — Queued in `next_hos` pending Rule-E Review)

> **RULE G & RULE-E STATUS (`J3408`, `2026-11-23`):**
> - **Backlog placement (`Rule G`):** Added to `jobs/WIP.json` `next_hos` under Rule G (`4/4` active HOS slots full: `HOS:008`, `HOS:009`, `HOS:010`, `HOS:013`). Nothing starts in production (`status.json` stages are all `todo`). A paired `kind:review` Rule-E topic go/no-go job is queued in `orbit-with-ben`.
> - **Proposed 2027 Search Plan Alignment (`J3224`):** Directly aligns with **Cluster 2 #6** (*Nuclear, Quantum & Modern Physics Breakthroughs* — Max Planck's Desperate Guess That Invented Quantum Physics) in Ben's proposed `hos-search-2027-01` search plan (`needsBen`, waiting for Ben's lock on the studio board — no HOS rule, cadence, or backlog policy changes until Ben approves).
> - **Strict Unverified Claims Guard (`facts` Lane Required Before Script Lock):** All historical and scientific claims in this brief are **UNVERIFIED** working notes. When an active HOS WIP slot opens, every claim, date, number, `DATA+SCALE`, `WHO`, `WHEN`, and `FACT` marker must be backed by verbatim primary-source quotes in `SOURCES.md` and verified through the `facts` lane (`gemini-agy`) before any script is locked, VO is recorded, or picture credit is spent.

---

## 1. HOS Data Comparison (`2026-11-23` Snapshot + `studio_ctr.json` + `channel_daily.json`)

- **Data sources read:**
  - `05_Analytics/hos/snapshots/2026-11-23.json` (`takenAt: 2026-11-23T06:40:34.195Z`, `43` public videos = `7` longs + `36` Shorts, `4,477` total views, `6` subscribers; `+565` views in last 24 h, `+928` in last 7 d, `+2,524` views and `+3` subs in last 30 d)
  - `05_Analytics/hos/studio_ctr.json` (`readAt: 2026-11-23T07:11:17.265966+00:00`, lifetime Studio impressions, CTR, average view %, and Shorts stayed-to-watch %)
  - `05_Analytics/hos/channel_daily.json` (`through: 2026-11-21`, `87` daily rows) and `05_Analytics/hos/REPORT.md`
  - `05_Analytics/LEARNINGS.md` (rules 1–41) and `05_Analytics/hos/search_research/2026-11-20.md` (`J3224`)
- **Elapsed-day denominator (`age_days`):** `max((date(2026, 11, 23) - date.fromisoformat(publishedAt[:10])).days, 1)` (`views/day = public_views / age_days`).
- **Low-sample statistical caveat (`Rule 1`):** Five public HOS longs have `5–15` lifetime views (`17–74` impressions), and bottom-tier Shorts have `4–30` views. Patterns inferred from low-N rows are treated explicitly as hypotheses, not settled laws.

### 1a. All `7` Public HOS Longs — Ranked by Views/Day Since Publish (`2026-11-23`)

| Rank | Video ID | Film | Title | Published (`age_days`) | Len | Views | Views/Day | Studio Impr | Studio CTR | Studio Avg View % | YTA 28d Views / Avg % |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| **1** | `AL_-qlWko_g` | `002` | *How Did We Discover the Periodic Table?* | `2026-09-17` (`67d`) | `541s` | **162** | **2.42/d** | **1,163** | 3.35% | 21.23% (`115s`) | `13v / 23.33%` |
| **2** | `GHZDsiH7L7A` | `004` | *What's Inside an Atom? Mostly Empty Space* | `2026-10-15` (`39d`) | `525s` | **35** | **0.90/d** | **840** | 1.43% | 23.54% (`124s`) | `9v / 54.97%` |
| **3** | `VbPubYd6Fbs` | `006` | *The Willow Tree That Was Made of Air* | `2026-11-05` (`18d`) | `532s` | **15** | **0.83/d** | 74 | 4.05% | **48.15%** (`256s`) | `15v / 48.15%` |
| **4** | `ETynHpIYLeY` | `007` | *How Was the First Vaccine Made? (And Why It's Named After a Cow)* | `2026-11-12` (`11d`) | `532s` | **7** | **0.64/d** | 44 | 4.55% | 19.29% (`103s`) | `7v / 19.29%` |
| **5** | `wwcjcFfC-5M` | `005` | *The Tied Arm That Proved Your Blood Circulates* | `2026-10-29` (`25d`) | `529s` | **7** | **0.28/d** | 17 | 17.65% | **6.73%** (`36s`) | `6v / 7.78%` |
| **6** | `_C92tIJCk8A` | `001` | *How Did We Discover Germs?* | `2026-09-03` (`81d`) | `365s` | **7** | **0.09/d** | 46 | 6.52% | 48.08% (`176s`) | `0v / —` |
| **7** | `frP_YrNShsU` | `003` | *How Did We Discover X-rays?* | `2026-09-24` (`60d`) | `426s` | **5** | **0.08/d** | 43 | 2.33% | 26.65% (`114s`) | `3v / 14.12%` |

- **3 Best HOS Longs & What They Share:**
  1. **`AL_-qlWko_g` (`002` *How Did We Discover the Periodic Table?*, `541s`)** — **`2.42/d`** (`162` views in `67d`), **`1,163` impressions** (`52.2%` of all `2,227` HOS long impressions), `3.35%` CTR, `21.23%` Studio avg view % (`70%` at `0:15`, `50%` at `0:30`).
  2. **`GHZDsiH7L7A` (`004` *What's Inside an Atom? Mostly Empty Space*, `525s`)** — **`0.90/d`** (`35` views in `39d`, `+1` sub), **`840` impressions** (`37.7%` of all HOS long impressions), `1.43%` CTR, `23.54%` Studio avg view % (`54.97%` in 28d YTA; `62%` at `0:15`, `45%` at `0:30`).
  3. **`VbPubYd6Fbs` (`006` *The Willow Tree That Was Made of Air*, `532s`)** — **`0.83/d`** (`15` views in `18d`), `74` impressions, `4.05%` CTR, channel-best **`48.15%` Studio & YTA avg view % (`256s`)** (low-N hypothesis).
  - **Shared pattern:** `002` and `004` generate **`89.9%` (`2,003 / 2,227`) of all HOS long impressions** and **`82.8%` (`197 / 238`) of all HOS long views** because both target foundational physics/chemistry search questions backed by multi-million `TED-Ed` and science-explainer neighbours (`Rules 1, 15, 26`), run `8.75–9.0 min` (`525–541s`), and open with a concrete puzzle (`Rule 10`).
- **3 Worst HOS Longs & What They Share (Small-N Hypotheses):**
  1. **`frP_YrNShsU` (`003` *How Did We Discover X-rays?*, `426s`)** — **`0.08/d`** (`5` views in `60d`), `43` impressions, `2.33%` CTR, `26.65%` avg view %.
  2. **`_C92tIJCk8A` (`001` *How Did We Discover Germs?*, `365s`)** — **`0.09/d`** (`7` views in `81d`), `46` impressions, `6.52%` CTR, `48.08%` avg view %.
  3. **`wwcjcFfC-5M` (`005` *The Tied Arm That Proved Your Blood Circulates*, `529s`)** — **`0.28/d`** (`7` views in `25d`), **`17` impressions**, `17.65%` CTR, **`6.73%` Studio avg view % (`36s`)**.
  - **Shared pattern:** Literary statement titles with no search phrase (`005`, `17` impressions) and short `6–7 min` survey-formula titles (`001`, `003`) miss both search impressions and suggested-video clustering (`Rules 10, 15, 23, 26`).

### 1b. All `36` Public HOS Shorts — Ranked by Views/Day Since Publish (`2026-11-23`)

| Rank | Video ID | Title | Published (`age_days`) | Len | Views | Views/Day | Stayed % | Studio Avg View % | Likes |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|
| **1** | `el30-mHiH-0` | *How Does the Heart Pump Blood?* *(early `20h`)* | `2026-11-22` (`1d`) | `26s` | **523** | **523.00/d** | 26.77% | 66.41% (`17s`) | 5 |
| **2** | `xzKoHg0E0_U` | *What Is Dalton's Atomic Theory?* | `2026-11-16` (`7d`) | `25s` | **239** | **34.14/d** | **53.13%** | 61.49% (`15s`) | 0 |
| **3** | `29bpGAI0wb8` | *What happens if you keep cutting gold in half?* | `2026-10-16` (`38d`) | `25s` | **1,229** | **32.34/d** | 40.78% | 44.14% (`11s`) | 12 |
| **4** | `Wvjd8g0CpzE` | *The Blood Vessels Finer Than a Hair* | `2026-11-15` (`8d`) | `26s` | **218** | **27.25/d** | 15.35% | 74.94% (`19s`) | 3 |
| **5** | `Bks_JLId1ew` | *How Do Plants Make Oxygen?* *(early `44h`)* | `2026-11-21` (`2d`) | `26s` | **50** | **25.00/d** | 48.57% | 96.53% (`25s`) | 0 |
| **6** | `PFj6172YU4Q` | *One Tight Band Proved Your Blood Goes Round* | `2026-11-08` (`15d`) | `27s` | **221** | **14.73/d** | 16.67% | 61.53% (`17s`) | 3 |
| **7** | `AMSriTQ-lcQ` | *Are Marie Curie's Notebooks Still Radioactive?* | `2026-10-28` (`26d`) | `22s` | **274** | **10.54/d** | 22.66% | 76.94% (`17s`) | 6 |
| **8** | `l8bxm9L3zl8` | *How Does a Blood Pressure Cuff Work?* | `2026-11-20` (`3d`) | `24s` | **29** | **9.67/d** | 38.46% | 60.99% (`15s`) | 0 |
| **9** | `OnJ8MFu0Mi0` | *How Did John Snow Stop Cholera?* | `2026-10-26` (`28d`) | `23s` | **231** | **8.25/d** | 29.60% | 65.66% (`15s`) | 8 |
| **10** | `pWySvZsneZg` | *Why Gold Foil Bounced Rutherford's Particles Back* | `2026-11-01` (`22d`) | `25s` | **137** | **6.23/d** | 37.23% | **112.43%** (`28s`) | 2 |
| **11** | `oKqmnJNGiHg` | *How Was Phosphorus Discovered?* | `2026-10-21` (`33d`) | `23s` | **194** | **5.88/d** | 42.03% | **88.35%** (`20s`) | 7 |
| **12** | `-3L6HzJ_d_4` | *What Is the Pasteur Swan Neck Flask Experiment?* | `2026-10-27` (`27d`) | `19s` | **140** | **5.19/d** | **78.95%** | **73.84%** (`14s`) | 1 |
| **13** | `cLKDiYP55J8` | *What Was the Edward Jenner Experiment?* | `2026-11-13` (`10d`) | `23s` | 47 | 4.70/d | 43.48% | 67.71% (`16s`) | 0 |
| **14** | `clV6E10NLPw` | *The spray that stopped surgery killing patients* | `2026-10-20` (`34d`) | `25s` | 155 | 4.56/d | 23.45% | 57.79% (`14s`) | 4 |
| **15** | `qOZgess30h0` | *Invisible life is still everywhere* | `2026-10-13` (`41d`) | `24s` | 169 | 4.12/d | 25.15% | 39.82% (`10s`) | 5 |
| **16** | `c2q7w0pgcn8` | *Who Discovered Infrared Light?* | `2026-10-19` (`35d`) | `23s` | 138 | 3.94/d | 43.52% | **105.30%** (`24s`) | 1 |
| **17** | `BW_CFAX-mxc` | *Is the Heart a Pump?* | `2026-10-31` (`23d`) | `22s` | 89 | 3.87/d | 32.91% | 81.69% (`18s`) | 1 |
| **18** | `Rl2uZ-KOTl8` | *Your Heart Pumps More Blood Than You Have* | `2026-10-30` (`24d`) | `25s` | 78 | 3.25/d | 26.58% | 53.64% (`13s`) | 4 |
| **19** | `xHnIi9GqOsM` | *Why Do Veins Have Valves?* | `2026-11-05` (`18d`) | `23s` | 42 | 2.33/d | 20.59% | 61.55% (`14s`) | 0 |
| **20** | `TbMMJSRKC3U` | *He said every eighth element repeats* | `2026-10-18` (`36d`) | `27s` | 63 | 1.75/d | 26.92% | 118.07% (`32s`) | 1 |
| **21** | `qW2OsD4mujc` | *The Four Elements Were Wrong* | `2026-11-03` (`20d`) | `24s` | 34 | 1.70/d | 57.69% | 192.62% (`46s`) | 0 |
| **22** | `LCZRHUyTiq0` | *What Are Cathode Rays?* | `2026-10-23` (`31d`) | `26s` | 49 | 1.58/d | 29.79% | 50.04% (`13s`) | 2 |
| **23** | `iqToagXnjX0` | *Microbes in a drop of pond water* | `2026-09-06` (`78d`) | `25s` | 113 | 1.45/d | 28.28% | 77.86% (`19s`) | 1 |
| **24** | `H1y0DXFVmw8` | *Germs don't cast a shadow* | `2026-09-06` (`78d`) | `25s` | 80 | 1.03/d | 19.75% | 59.46% (`15s`) | 1 |
| **25** | `ChbsigHD5_o` | *How Do Plants Clean the Air?* | `2026-11-18` (`5d`) | `25s` | 5 | 1.00/d | 100.00% | 36.12% (`9s`) | 0 |
| **26** | `xvanpsLeADE` | *How did Röntgen see bones without cutting* | `2026-09-26` (`58d`) | `25s` | 40 | 0.69/d | 23.33% | 50.33% (`13s`) | 0 |
| **27** | `xgx2lYHhYZM` | *Why Is It Called a Vaccine?* | `2026-11-17` (`6d`) | `25s` | 4 | 0.67/d | 100.00% | 62.41% (`16s`) | 0 |
| **28** | `oowAOWTBoq0` | *How X-rays Were Discovered by Accident* | `2026-09-25` (`59d`) | `25s` | 32 | 0.54/d | 47.62% | 331.08% (`83s`) | 1 |
| **29** | `nba0-f7PPeU` | *Why tellurium sat before iodine* | `2026-09-21` (`63d`) | `25s` | 34 | 0.54/d | 60.71% | 42.70% (`11s`) | 1 |
| **30** | `nFQRWmpulTQ` | *He predicted a metal before it was found* | `2026-09-19` (`65d`) | `25s` | 34 | 0.52/d | 66.67% | 55.91% (`14s`) | 0 |
| **31** | `8_Edn_HCi1s` | *Germs hitch a ride on you* | `2026-09-06` (`78d`) | `25s` | 38 | 0.49/d | 33.33% | 34.25% (`9s`) | 0 |
| **32** | `uU12JA5rMWg` | *The periodic table's empty chairs* | `2026-09-18` (`66d`) | `25s` | 30 | 0.45/d | 66.67% | 58.79% (`15s`) | 0 |
| **33** | `sILtQxgYQk8` | *A flask that proved germs come from outside* | `2026-09-06` (`78d`) | `25s` | 24 | 0.31/d | 41.67% | 36.70% (`9s`) | 0 |
| **34** | `CnHwX1L9XHg` | *Gallium sat where the table said* | `2026-09-20` (`64d`) | `26s` | 16 | 0.25/d | 30.43% | 33.45% (`9s`) | 0 |
| **35** | `zI_eD3vFWmE` | *The first X-ray showed a wedding ring* | `2026-09-27` (`57d`) | `25s` | 9 | 0.16/d | 50.00% | 64.00% (`16s`) | 0 |
| **36** | `LanTHJckYx8` | *What other table has empty chairs?* | `2026-09-22` (`62d`) | `26s` | 4 | 0.06/d | 33.33% | 23.08% (`6s`) | 0 |

- **3 Best Mature HOS Shorts & What They Share:**
  1. **`xzKoHg0E0_U` (*What Is Dalton's Atomic Theory?*, `25s`)** — **`34.14/d`** (`239` views in `7d`), **`53.13%` stayed (`WATCH`)**, `61.49%` avg view %, **`197` 28d search views** (`88.3%` of YTA views).
  2. **`29bpGAI0wb8` (*What happens if you keep cutting gold in half?*, `25s`)** — **`32.34/d`** (`1,229` lifetime views, #1 HOS video, `12` likes), `40.78%` stayed, `44.14%` avg view %.
  3. **`-3L6HzJ_d_4` (*What Is the Pasteur Swan Neck Flask Experiment?*, `19s`)** — **`5.19/d`** (`140` views in `27d`), channel-best **`78.95%` stayed (`PASS ≥60%`)** and **`73.84%` Studio / `74.98%` YTA avg view % (`PASS ≥70%`)**, **`129` 28d search views** (`93.5%` search) — the ONLY mature `100+`-view HOS Short passing BOTH targets and the channel's only `19s` Short (`Rules 1, 2, 3, 6, 24, 27, 28, 32, 41`).
- **3 Worst Mature HOS Shorts & What They Share:**
  1. **`LanTHJckYx8` (*What other table has empty chairs?*, `26s`)** — `0.06/d` (`4` views), `33.33%` stayed, `23.08%` avg view %.
  2. **`zI_eD3vFWmE` (*The first X-ray showed a wedding ring*, `25s`)** — `0.16/d` (`9` views), `50.00%` stayed, `64.00%` avg view %.
  3. **`CnHwX1L9XHg` (*Gallium sat where the table said*, `26s`)** — `0.25/d` (`16` views), `30.43%` stayed, `33.45%` avg view % — plus cold-feed statement misses `Wvjd8g0CpzE` (`15.35%` stayed) and `PFj6172YU4Q` (`16.67%` stayed).

---

## 2. Overlap & Non-Duplication Check (`2026-11-23`)

Checked against:
- All folders in `02_Video-Projects/` (`000`–`018`, `099`–`119` on `main`),
- Open HOS topic PRs `#659` (`120–121`), `#682` (`122–123`), `#689` (`124–125`), `#706` (`126` Higgs Boson, `127` Airplanes), `#724` (`128` AC vs DC, `129` Microwave), `#726` (`130` Fermi Nuclear Reactor, `131` Einstein Relativity), and paired film `132` (Why Is Glass Transparent),
- All `011`–`095` folders in `00_Brand/Channel-Setup/ideas/`, `VIDEO_BACKLOG.json`, and `jobs/WIP.json`. Specifically verified against `025_Young-Fresnel-Einstein-Light` (which covers Thomas Young's 1801–1803 double-slit, Arago's 1819 spot, Einstein's 1905 photoelectric wave-vs-particle debate, Taylor 1909, and de Broglie 1924): **`HOS:133` focuses strictly on the German lightbulb efficiency race (1887–1900), PTR Berlin blackbody-oven measurements (Lummer, Pringsheim, Rubens, Kurlbaum), the Rayleigh–Jeans Ultraviolet Catastrophe, Max Planck's Sunday 7 October 1900 postcard & 14 December 1900 "act of desperation" energy-packet formula ($E = h\nu$, Planck's constant $h$), and Niels Bohr's 1913 atomic stability application** — zero narrative overlap with `025`.
- **Result:** **Zero overlap.**

---

## 3. Packaging, Why It Should Work & Search/Neighbour Evidence (`Rule 26` + `J3224` + `neighbours.py` + `public_search.py`)

- **Title A (Primary Proposal, `LEARNINGS.md` Rules 1, 15, 23, 26 — `59 chars ≤ 70 chars`, `0` exact collisions):** `How Was Quantum Physics Discovered? (The Lightbulb Problem)`
- **Title A1 (Compact `Rule 15 ≤50 chars` Variant — `48 chars`, `0` exact collisions):** `What Is Quantum Mechanics? (Planck's 1900 Guess)`
- **Title B (Test & Compare Arm 2, `Rule 23` — `49 chars ≤ 50 chars`, `0` exact collisions):** `Max Planck's 1900 Postcard (How Quantum Was Born)`
- **Title C (`Rule 26` Exact Phrase + Ultraviolet Catastrophe — `65 chars ≤ 70 chars`, `0` exact collisions):** `How Was Quantum Physics Discovered? (The Ultraviolet Catastrophe)`
- **One-Line Hook:** Quantum physics wasn't born from staring at stars or smashing atoms — it began in 1900 when German lightbulb companies asked physicist Max Planck why a hot glowing filament didn't blast out infinite ultraviolet light, forcing him into an "act of desperation" that chopped energy into tiny indivisible packets.
- **Why It Should Work (Past Winners, `J3224` Small-Channel Proof & `LEARNINGS.md` Rules):**
  - Directly fills **Cluster 2 #6** (*Max Planck's Desperate Guess That Invented Quantum Physics*) of Ben's proposed `hos-search-2027-01` search plan (`J3224`, `needsBen`), chaining seamlessly with `126` Higgs Boson, `130` Fermi Nuclear Reactor, and `131` Einstein Relativity (`Rule 20` series playlists). `J3224` verified massive US adult small-channel (`<50k` subs) breakouts on this exact story: **`Science Retold` (`3.4K` US) → `61.9K` views (`13×` breakout)** on *The Origin Of Planck's Constant*, **`Math Everywhere` (`10.3K` US) → `36.5K` views (`10×` breakout)** on *MAX PLANCK: The Tragic Story of the Father of Quantum Physics!*, and **`Cosmo Explains` (`37.0K` US) → `239.7K` views (`65×`)** on quantum physics.
  - Mirrors our top two impression-earning HOS longs — **`002` Periodic Table (`AL_-qlWko_g`, `162` views, `2.42/d`, `1,163` impressions, `3.35%` CTR)** and **`004` Inside an Atom (`GHZDsiH7L7A`, `35` views, `0.90/d`, `840` impressions)** — by pairing a massive foundational physics search question (`"how was quantum physics discovered"` and `"what is quantum mechanics"`, both `autocomplete = yes`) with `11` strictly on-topic education neighbours `≥1M` views (`Rules 1, 15, 26`) and a concrete room-and-apparatus mystery (Berlin's glowing blackbody oven + a Sunday-night postcard) like **`006` Willow Tree (`48.15%` avg view %)** (`Rules 10, 23`).
  - Mirrors our best HOS Shorts — **`xzKoHg0E0_U` (*What Is Dalton's Atomic Theory?*, `34.14/d`, `53.13%` stayed, `197` search)**, **`29bpGAI0wb8` (`1,229` views, `32.34/d`)**, and **`-3L6HzJ_d_4` (`19s`, `78.95%` stayed PASS, `73.84%` avg view % PASS)** — by pairing named-entity physics questions (`Max Planck`, `Ultraviolet Catastrophe`, `Planck's Constant`) with Ben's 19 Nov `16–19 s` looping 3D cartoon Shorts rules (`Rules 2, 3, 6, 24, 27, 28, 32, 41`).
- **3-Way Thumbnail Test & Compare Plan (`LEARNINGS.md` Rules 11, 12, 14 + `THUMBNAIL_AND_TITLE_RULES.md` §2.1–2.B; zero title-word repeats per §2.5):**
  - **Thumb A (Hero Object — Glowing 1900 Blackbody Oven & Postcard):** Painted 3D house-style key art: a brass-and-ceramic 1900 Berlin laboratory blackbody furnace glowing deep cherry-red to white-hot on the right two-thirds, with a handwritten ink equation postcard (`E = hν`) hovering beside discrete golden light packets; Explorer small at lower left; cream/gold serif text on clear left band: `1900 POSTCARD` (`2 words`, gold on `1900`, zero words repeated from Title A).
  - **Thumb B (`Rule 14` Bright High-Contrast Variant — Glowing Filament Staircase):** Bright warm cream-and-gold sunlit laboratory key art: an incandescent glass bulb filament emitting neat glowing golden step-packets instead of a smooth rainbow smear; Explorer small at lower left; serif text on clear left band: `ENERGY PACKETS` (`2 words`, gold on `PACKETS`, zero words repeated from Title A).
  - **Thumb C (The Classical Infinity Crash):** Painted 3D brass chart on aged parchment where a jagged classical violet curve rockets off the top of the frame (`∞`) while a calm golden measured bell curve bends smoothly downward beneath it; Explorer small at lower left; serif text on clear left band: `BROKEN INFINITY` (`2 words`, gold on `BROKEN`, zero words repeated from Title A).
- **Signed-out YouTube Autocomplete (`2026-11-23`, `10` queries / `75` search rows in `11_Upload-Package/evidence_2026-11-23_public_search.json`):**
  - `"how was quantum physics discovered"` → **`autocomplete = yes`**
  - `"what is quantum mechanics"` → **`autocomplete = yes`** (`what is quantum mechanics`, `what is quantum mechanics in physics`, `what is quantum mechanics in chemistry`)
  - `"what is the ultraviolet catastrophe"` → **`autocomplete = yes`** (`what is the ultraviolet catastrophe`, `what is uv catastrophe`)
  - `"max planck quantum theory"` → **`autocomplete = yes`** (`max planck quantum theory`, `max planck quantum theory explained`)
  - **Exact title collisions across all 4 long titles + 2 Short titles:** **`0` exact collisions.**
- **Rule 26(a) Two Ranking Videos (`≥10,000` views, retrieved `2026-11-23`):**
  1. `The Royal Institution` — [`5hVmeOCJjOU`](https://youtu.be/5hVmeOCJjOU) *A Brief History of Quantum Mechanics - with Sean Carroll* (**`4,686,616` views**)
  2. `minutephysics` — [`i1TVZIBj7UA`](https://youtu.be/i1TVZIBj7UA) *The Origin of Quantum Mechanics (feat. Neil Turok)* (**`3,232,924` views**; plus `Physics Explained` [`rCfPQLVzus4`](https://youtu.be/rCfPQLVzus4) **`2,714,822` views**, `PBS Space Time` [`tQSbms5MDvY`](https://youtu.be/tQSbms5MDvY) **`2,054,493` views**, and `Abide By Reason` [`1,072,051` views])
- **Neighbour Gate (`neighbours.py`):** **PASS (`13` raw / `11` strictly on-topic education videos `≥1,000,000` views, `3` `TED-Ed` `≥1M`, `TED-Ed/TED: yes`)** — saved in [`11_Upload-Package/evidence_2026-11-23_neighbours.json`](11_Upload-Package/evidence_2026-11-23_neighbours.json):
  1. `Veritasium` — [`KfODG5REyss`](https://youtu.be/KfODG5REyss) *I finally saw quantum physics with my own eyes...* (**`21,553,339` views**)
  2. `Veritasium` — [`qJZ1Ez28C-A`](https://youtu.be/qJZ1Ez28C-A) *The Strangest Implication of Quantum Mechanics* (**`20,891,298` views**)
  3. `TED-Ed` ★ — [`UjaAxUO6-Uw`](https://youtu.be/UjaAxUO6-Uw) *Schrödinger's cat: A thought experiment in quantum mechanics - Chad Orzel* (**`9,228,160` views**)
  4. `The Royal Institution` — [`5hVmeOCJjOU`](https://youtu.be/5hVmeOCJjOU) *A Brief History of Quantum Mechanics - with Sean Carroll* (**`4,686,613` views**)
  5. `TEDx Talks` ★ — [`ARWBdfWpDyc`](https://youtu.be/ARWBdfWpDyc) *Quantum Physics for 7 Year Olds | Dominic Walliman* (**`3,813,226` views**)
  6. `TED` ★ — [`QuR969uMICM`](https://youtu.be/QuR969uMICM) *A beginner's guide to quantum computing | Shohini Ghose* (**`2,665,434` views**)
  7. `PBS Space Time` — [`YSwRqNCeP9k`](https://youtu.be/YSwRqNCeP9k) *So You Want to Understand Quantum Mechanics…* (**`2,514,160` views**)
  8. `TED-Ed` ★ — [`z1GCnycbMeA`](https://youtu.be/z1GCnycbMeA) *What can Schrödinger's cat teach us about quantum mechanics? - Josh Samani* (**`2,168,361` views**)
  9. `PBS Space Time` — [`tQSbms5MDvY`](https://youtu.be/tQSbms5MDvY) *Planck's Constant and The Origin of Quantum Mechanics* (**`2,054,493` views** — exact topic match!)
  10. `TED-Ed` ★ — [`Hk3fgjHNQ2Q`](https://youtu.be/Hk3fgjHNQ2Q) *Particles and waves: The central mystery of quantum mechanics - Chad Orzel* (**`1,153,323` views**)
  11. `TED` ★ — [`_qgSz1UmcBM`](https://youtu.be/_qgSz1UmcBM) *How Quantum Biology Might Explain Life's Biggest Questions | Jim Al-Khalili* (**`1,110,967` views**)
  *(Excluded from strictly on-topic count: `2RuCfTiCDjs` TEDx manifestation talk and `uIojjqSm0m4` Khan Academy 1D motion — leaving `11` strictly on-topic `≥1M` education videos.)*

---

## 4. Candidate 4-Act Discovery Outline (All Claims UNVERIFIED Pending `SOURCES.md` & `facts` Lane)

- **Cold Open (0:00–0:45, Proof-First `0:05–0:15` Apparatus Window per `Rules 10 & 30`, UNVERIFIED):**
  - `0:00–0:05`: Inside a darkened 1900 Berlin physics lab, an iron bar and a hollow ceramic oven glow dull red, then orange, then dazzling white-hot — and according to every law of nineteenth-century physics, opening that oven door should have incinerated the room with infinite ultraviolet radiation.
  - `0:05–0:15` (Apparatus / Physical Proof): Hard cut straight into the **Physikalisch-Technische Reichsanstalt (PTR) blackbody cavity oven** (`Hohlraum`), where a brass spectrometer measures a calm, peaked glow curve while the classical prediction shoots vertically off the parchment toward `∞` (`ULTRAVIOLET CATASTROPHE` ink graph). Zero *"In this film…"* agenda line.
  - `0:15–0:45`: Quantum physics didn't begin as a grand philosophy of reality — it began as an industrial lightbulb problem in Berlin, when a conservative 42-year-old professor named **Max Planck** scribbled a desperate mathematical trick on a Sunday-night postcard in October 1900 and accidentally shattered classical physics forever.
- **Act I — Berlin's Lightbulb Race & the PTR Blackbody Oven (1887–1900, UNVERIFIED):** In late-1800s Germany, electric lighting companies were racing to build brighter, cooler filaments without wasting electricity on invisible heat. The German Imperial Bureau of Standards (**Physikalisch-Technische Reichsanstalt**, founded 1887 in Berlin-Charlottenburg) assigned experimentalists **Otto Lummer**, **Ernst Pringsheim**, **Heinrich Rubens**, and **Ferdinand Kurlbaum** to measure the exact spectrum of an ideal heated cavity ("blackbody") from glowing red into deep infrared (`DATA+SCALE` spectrum chart). Classical electromagnetism and thermodynamics — later crystallised by **Lord Rayleigh** (1900) and **James Jeans** (1905) — predicted that every higher frequency should absorb an equal share of thermal energy, making the total energy shoot to **infinity** at short ultraviolet wavelengths (the **Ultraviolet Catastrophe**, a term later coined by Paul Ehrenfest in 1911). Every kitchen toaster proved classical physics was catastrophically wrong.
- **Act II — Sunday Afternoon Tea & the 7 October 1900 Postcard (7–19 October 1900, UNVERIFIED):** **Max Planck** (1858–1947), a meticulous Berlin theoretical physicist whose own mentor **Philipp von Jolly** had once warned him in 1878 that "almost everything in physics is already discovered," had spent six years trying to derive **Wilhelm Wien's** short-wavelength curve cleanly from classical entropy. On **Sunday afternoon, 7 October 1900**, his friend **Heinrich Rubens** stopped by Planck's Grunewald home for tea and shared fresh long-wavelength infrared data proving Wien's law failed at low frequencies. That very evening, Planck mathematically spliced the short- and long-wavelength behaviours into a single interpolation formula and mailed it to Rubens on a **postcard**. Next morning, Rubens checked it against his lab data — it matched every single point to experimental precision (`19 October 1900` presentation to the German Physical Society).
- **Act III — 14 December 1900: "An Act of Desperation" ($E = h\nu$, UNVERIFIED):** *"Case closed? Wrong."* Having a formula that fits a graph is not an explanation — Planck spent two frantic months trying to prove *why* his formula worked using classical physics, and failed. In what he later called **"an act of desperation"** (letter to Robert Williams Wood, 7 October 1931), he borrowed Ludwig Boltzmann's statistical combinatorics and made a forbidden assumption: the vibrating atoms inside the oven walls cannot emit or absorb energy continuously like a ramp — they can only trade energy in discrete indivisible chunks ("quanta") of size **$E = h\nu$**, governed by a tiny new fundamental constant of nature, **`h ≈ 6.626 × 10⁻³⁴ J·s`** (`DATA+SCALE`: a single visible-light packet carries roughly `10⁻¹⁹` joules — so a dim candle flame emits trillions upon trillions of packets every second, hiding the graininess from our eyes!). On **14 December 1900**, Planck presented this derivation in Berlin — the birthday of quantum theory — still hoping the chunks were only a temporary mathematical bookkeeping device.
- **Act IV — The Constant That Wouldn't Go Away (1905–1918, UNVERIFIED):** Planck tried for years to fit his constant $h$ back inside classical physics — yet instead of disappearing, $h$ kept showing up everywhere! In **1905**, **Albert Einstein** showed light itself travels in Planck-sized packets; in **1913**, **Niels Bohr** plugged Planck's $h$ into Rutherford's nuclear atom (connecting directly back to HOS `004`!) to explain why orbiting electrons don't spiral into the nucleus and why every element glows its own razor-sharp barcode colours. In **1918**, the reluctant revolutionary received the **Nobel Prize in Physics** — for the "desperate guess" that built modern lasers, microchips, solar panels, and quantum physics itself.
- **Pre-sourced `Teach on screen` & `Polish pass` markers (all numbers UNVERIFIED pending `SOURCES.md`):** `DATA+SCALE` (5, incl. `1878 → 1918` timeline, classical `∞` vs measured blackbody curve, ramp vs staircase energy steps $E = h\nu$, Planck's constant `h = 6.626 × 10⁻³⁴ J·s` vs trillions of candle photons/sec, Bohr discrete colour lines), `WHO` (Max Planck, Philipp von Jolly, Heinrich Rubens, Lord Rayleigh, Niels Bohr), `WHEN` (`1878`, `1887`, `7 Oct 1900`, `14 Dec 1900`, `1913`, `1918`), `FACT` (4 sourced beats).

---

## 5. Two Candidate Search-Titled Shorts (`Ben 19 Nov 16–19 s Rules` + `Rules 32 & 41` — UNVERIFIED Concepts Only)

- **Short `S01`:** *How Did Max Planck Solve the Ultraviolet Catastrophe?* (`53 chars`, `0` exact collisions; named-scientist + named-phenomenon curriculum search question backed by `"what is the ultraviolet catastrophe"` and `"max planck quantum theory"` `autocomplete = yes`)
  - **16–19 s Loop Concept (`Ben 19 Nov Rules`):**
    - **Frame 0 (`0.0 s`, premium 3D cartoon moving plate, zero Explorer, zero bars):** A 1900 Berlin brass furnace glows warm orange as an inked classical curve rockets off the parchment toward `∞`, then snaps cleanly down into glowing stepped golden packets. On-screen line-1 concrete fact caption: `Classical math predicted infinite UV` (yellow on `infinite`).
    - **Spoken hook (`≤1.5 s` titled noun + surprise, zero dateline, zero meta-promise):** *"Max Planck fixed a physics bug that said every hot toaster should blast out infinite ultraviolet light."*
    - **Single mid-Short `Teach on screen` overlay (`~9.5 s`, inside 16:9 band):** `E = hν · ENERGY PACKETS`.
    - **Payoff (`≥70%` runtime, `~13.5 s / 18.0 s`):** By forcing glowing atoms to trade energy only in discrete steps instead of smooth ramps, Planck cut off the impossible high-frequency infinity — accidentally inventing quantum mechanics, looping cleanly back into *"Max Planck fixed a physics bug…"* (`<0.3 s` visual seam match, `0` CTA).
- **Short `S02`:** *How Did a Glowing Oven Invent Planck's Constant?* (`48 chars`, `0` exact collisions; concrete hero object + named curriculum constant backed by `"max planck quantum theory"` and `"how was quantum physics discovered"` `autocomplete = yes`)
  - **16–19 s Loop Concept (`Ben 19 Nov Rules`):**
    - **Frame 0 (`0.0 s`, premium 3D cartoon moving plate, zero Explorer, zero bars):** Close 3D view of a glowing ceramic blackbody oven aperture beside a vintage Berlin postcard where gold ink writes `E = hν` in real time. On-screen line-1 concrete fact caption: `A lightbulb test sparked quantum` (yellow on `lightbulb`).
    - **Spoken hook (`≤1.5 s` titled noun + surprise, zero dateline, zero meta-promise):** *"A glowing laboratory oven built to make better lightbulbs forced Max Planck to invent quantum physics."*
    - **Single mid-Short `Teach on screen` overlay (`~9.5 s`, inside 16:9 band):** `14 DEC 1900 · PLANCK'S h`.
    - **Payoff (`≥70%` runtime, `~13.5 s / 18.0 s`):** To match Berlin's furnace measurements, Planck introduced one tiny number — `h` — capping energy into indivisible packets, calling it an act of desperation that turned out to rule the whole universe, looping cleanly back into *"A glowing laboratory oven built to make better lightbulbs…"* (`<0.3 s` visual seam match, `0` CTA).
