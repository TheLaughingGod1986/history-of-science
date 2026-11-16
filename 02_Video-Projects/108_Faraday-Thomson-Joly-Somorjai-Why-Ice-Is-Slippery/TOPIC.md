# Topic Brief — `108_Faraday-Thomson-Joly-Somorjai-Why-Ice-Is-Slippery` (`HOS:108` Proposal)

> **PROPOSAL & RULE G STATUS (`J2891`, `2026-11-15`):**
> - **Backlog Proposal Only (`next_hos`):** This topic is added to the History of Science backlog (`jobs/WIP.json` `next_hos`) under **Rule G** (`active_hos` has 3 active films). Nothing is started in production (`status.json` stages are all `todo`).
> - **Awaits Rule-E Review & `facts` Lane:** All historical and scientific claims in this brief are **UNVERIFIED** working notes. Before any script is locked or VO is recorded, every claim must be backed by verbatim primary-source quotes in `SOURCES.md` and verified through the `facts` lane (`gemini-agy`).

---

## 1. HOS Data Comparison (`2026-11-15` Snapshot + `studio_ctr.json` + `channel_daily.json`)

- **Data sources read:**
  - `05_Analytics/hos/snapshots/2026-11-15.json` (`takenAt: 2026-11-15T06:40:28.409Z`, `36` public videos = `7` longs + `29` Shorts)
  - `05_Analytics/hos/studio_ctr.json` (`readAt: 2026-11-15T07:53:35.291276+00:00`, lifetime Studio impressions, CTR, average view %, and Shorts stayed-to-watch %)
  - `05_Analytics/hos/channel_daily.json` (`through: 2026-11-13`) and `05_Analytics/hos/REPORT.md`
  - `05_Analytics/LEARNINGS.md` (rules 1–33)
- **Elapsed-day denominator (`age_days`):** `max((date(2026, 11, 15) - date.fromisoformat(publishedAt[:10])).days, 1)` (`views/day = views / age_days`).
- **Low-sample statistical caveat (`Rule 1` / `RULING.md`):** Several public HOS longs have only `3–10` lifetime views (`15–44` impressions), and bottom-tier Shorts have `4–30` views. Patterns inferred from those small-N rows are treated explicitly as **hypotheses**, not settled laws.

### 1a. All `7` Public HOS Longs — Ranked by Views/Day Since Publish (`2026-11-15`)

| Rank | Video ID | Film | Title | Published (`age_days`) | Views (`2026-11-15`) | Views / Day | Studio Impressions (Lifetime) | Studio CTR (Lifetime) | Studio Avg View % (Lifetime) | YTA 28d Views (`through 11-13`) | YTA 28d Avg View % |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **1** | `AL_-qlWko_g` | `002` | *How Did We Discover the Periodic Table?* | `2026-09-17` (`59d`) | **161** | **2.73/d** | 1,160 | 3.36% | 21.59% (`117s / 541s`) | 37 | 23.0% |
| **2** | `GHZDsiH7L7A` | `004` | *What's Inside an Atom? Mostly Empty Space* | `2026-10-15` (`31d`) | **34** | **1.10/d** | 837 | 1.31% | 24.29% (`128s / 525s`) | 29 | 20.6% |
| **3** | `VbPubYd6Fbs` | `006` | *The Willow Tree That Was Made of Air* | `2026-11-05` (`10d`) | **10** | **1.00/d** | 36 | 2.78% | **66.54%** (`354s / 532s`) | 9 | 66.5% |
| **4** | `ETynHpIYLeY` | `007` | *How Was the First Vaccine Made? (And Why It's Named After a Cow)* | `2026-11-12` (`3d`) | **3** | **1.00/d** | 16 | 12.50% | 5.26% (`28s / 532s`) | 3 | 5.2% |
| **5** | `wwcjcFfC-5M` | `005` | *The Tied Arm That Proved Your Blood Circulates* | `2026-10-29` (`17d`) | **5** | **0.29/d** | 15 | **20.00%** | 9.24% (`49s / 529s`) | 5 | 9.2% |
| **6** | `frP_YrNShsU` | `003` | *How Did We Discover X-rays?* | `2026-09-24` (`52d`) | **5** | **0.10/d** | 41 | 2.44% | 26.65% (`114s / 426s`) | 3 | 29.8% |
| **7** | `_C92tIJCk8A` | `001` | *How Did We Discover Germs?* | `2026-09-03` (`73d`) | **7** | **0.10/d** | 44 | 6.82% | 48.08% (`176s / 365s`) | 2 | 47.4% |

- **3 Best HOS Longs & What They Share:**
  1. **`AL_-qlWko_g` (`002` *How Did We Discover the Periodic Table?*)** — **`2.73` views/day** (`161` views in `59d`), **`1,160` impressions** (`54.0%` of all HOS long impressions), `3.36%` CTR, `21.59%` avg view % (`23.0%` in 28d).
  2. **`GHZDsiH7L7A` (`004` *What's Inside an Atom? Mostly Empty Space*)** — **`1.10` views/day** (`34` views in `31d`), **`837` impressions** (`38.9%` of all HOS long impressions), `1.31%` CTR, `24.29%` avg view %.
  3. **`VbPubYd6Fbs` (`006` *The Willow Tree That Was Made of Air*)** — **`1.00` views/day** (`10` views in `10d`), `36` impressions, `2.78%` CTR, and channel-best **`66.54%` avg view %** (`354s` of `532s`; low-N hypothesis at `10` views).
  - **Shared pattern:** `002` and `004` together account for **`92.9%` (`1,997 / 2,149`) of all HOS long impressions** and **`86.7%` (`195 / 225`) of all HOS long views** because they sit inside core school-science search phrases (`periodic table`, `what's inside an atom`) with massive `TED-Ed` / `Veritasium` / `FuseSchool` neighbour clusters. Meanwhile `006` (*The Willow Tree That Was Made of Air*) shows that a concrete experiment hook holds strong retention (`66.54%` avg view %) once clicked, but a poetic/non-search title without an autocomplete phrase (`36` impressions in `10d`) gets starved of search impressions (`LEARNINGS.md` Rule 26).
- **3 Worst HOS Longs & What They Share (Hypotheses on Small N):**
  1. **`_C92tIJCk8A` (`001` *How Did We Discover Germs?*)** — **`0.10` views/day** (`7` views in `73d`), `44` impressions, `6.82%` CTR, `48.08%` avg view %.
  2. **`frP_YrNShsU` (`003` *How Did We Discover X-rays?*)** — **`0.10` views/day** (`5` views in `52d`), `41` impressions, `2.44%` CTR, `26.65%` avg view %.
  3. **`wwcjcFfC-5M` (`005` *The Tied Arm That Proved Your Blood Circulates*)** — **`0.29` views/day** (`5` views in `17d`), `15` impressions, `20.00%` CTR (3 clicks on 15 impressions), `9.24%` avg view %.
  - **Shared pattern (hypothesis given `5–7` views):** Generic textbook-chapter questions without a specific everyday mystery or visual hook (*How Did We Discover Germs?*, *How Did We Discover X-rays?*) and apparatus-only titles without the everyday search phrase (*The Tied Arm That Proved Your Blood Circulates*, `15` impressions) fail to earn YouTube search/browse impressions (`15–44` lifetime impressions). **Lesson applied to `HOS:108` & `HOS:109`:** Pair a **verbatim signed-out autocomplete question first** (`Why Is Ice Slippery?`, `Why Do Fingers Wrinkle in Water?`) with a **concrete experimental/counter-intuitive parenthetical** (`(The 150-Year Textbook Myth)`, `(The Cut-Nerve Proof)`).

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
  1. **`29bpGAI0wb8` (*What happens if you keep cutting gold in half?*)** — **`40.90` views/day** (`1,227` views in `30d`), `40.78%` stayed-to-watch, `44.12%` avg view % (`11s / 25s`), `12` likes (`+4` subs in 28d).
  2. **`PFj6172YU4Q` (*One Tight Band Proved Your Blood Goes Round*)** — **`31.29` views/day** (`219` views in `7d`), `15.98%` stayed-to-watch, `62.95%` avg view % (`17s / 27s`), `3` likes.
  3. **`AMSriTQ-lcQ` (*Are Marie Curie's Notebooks Still Radioactive?*)** — **`15.22` views/day** (`274` views in `18d`), `22.66%` stayed-to-watch, `76.94%` avg view % (`17s / 22s`), `6` likes (`+1` sub in 28d).
  - *(Also notable: #4 `OnJ8MFu0Mi0` *How Did John Snow Stop Cholera?* at `11.55/d`, `231` views, `29.60%` stayed-to-watch; #5 `pWySvZsneZg` *Why Gold Foil Bounced Rutherford's Particles Back* at `9.79/d`, `137` views, `37.23%` stayed-to-watch, `112.43%` avg view %; and #8 `-3L6HzJ_d_4` *What Is the Pasteur Swan Neck Flask Experiment?* at `6.74/d`, `128` views, channel-best **`77.14%` stayed-to-watch**.)*
  - **Shared pattern:** Immediate physical thought-experiment or tactile demonstration questions (*cutting gold in half*, *tight band on your arm*, *radioactive notebooks*, *swan-neck flask*) where the viewer can picture the physical test in the first 2 seconds (`LEARNINGS.md` Rules 18, 28, 32).
- **3 Worst HOS Shorts & What They Share (Hypotheses on Small N):**
  1. **`LanTHJckYx8` (*What other table has empty chairs?*)** — **`0.07` views/day** (`4` views in `54d`), `33.33%` stayed-to-watch, `23.08%` avg view % (`6s / 26s`).
  2. **`zI_eD3vFWmE` (*The first X-ray showed a wedding ring*)** — **`0.18` views/day** (`9` views in `49d`), `50.00%` stayed-to-watch, `64.00%` avg view %.
  3. **`CnHwX1L9XHg` (*Gallium sat where the table said*)** — **`0.29` views/day** (`16` views in `56d`), `30.43%` stayed-to-watch, `33.45%` avg view %.
  - **Shared pattern:** Cryptic riddle titles (*What other table has empty chairs?*) or flat caption statements (*Gallium sat where the table said*, *The first X-ray showed a wedding ring*) that carry zero search keywords and no self-explanatory physical question.

---

## 2. Overlap & Non-Duplication Check (`2026-11-15`)

Checked against:
- All folders in `02_Video-Projects/` (`000`–`018`, `099`–`101` on `main`),
- Open topic PRs `#572` (`102` Antikythera, `103` Deep-Sea Hydrothermal Vents), `#581` (`104` Speed of Light, `105` Stomach Acid Digestion), and `#588` (`106` Lightning Rod, `107` Photosynthesis Oxygen),
- All `011`–`097` backlog entries in `00_Brand/Channel-Setup/VIDEO_BACKLOG.json` and `00_Brand/Channel-Setup/ideas/IDEAS_*.md` (`072` covers Alfred Wegener's continental drift; `085` covers Louis Agassiz's Ice Ages; `029` covers William Thomson / Lord Kelvin's age of the Earth; `033` covers James Joule's mechanical equivalent of heat; **none** cover why ice is slippery, Faraday's 1850 regelation experiments, Joly's 1886 skate-blade pressure-melting calculation, or surface premelting).
- **Result:** **Zero overlap.**

---

## 3. Packaging & Search Evidence (`Rule 26` + `neighbours.py` + `public_search.py`)

- **Title A (Primary Proposal, `49 chars`, `0` collisions):** `Why Is Ice Slippery? (The 150-Year Textbook Myth)`
- **Title B (Test & Compare Arm 2, `52 chars`, `0` collisions):** `The 150-Year Textbook Myth About Why Ice Is Slippery`
- **Title C (Rule 26 Exact Phrase First, `53 chars`, `0` collisions):** `Why Is Ice Slippery? How Faraday Beat a 150-Year Myth`
- **Signed-out YouTube Autocomplete (`2026-11-15`):**
  - `"why is ice slippery"` → **`autocomplete = yes`** (`why is ice slippery`, `why is ice slippery veritasium`, `why is ice slippery physics`, `why is ice slippery sci show`, `why is ice slippery Hank green`, `why is ice slippery explained`)
  - `"how does ice skating work"` → **`autocomplete = yes`** (`how does ice skating work`, `how does figure skating work in the olympics`, `how does figure skating work`, `how does speed skating work`)
- **Rule 26(a) Two Ranking Videos (`≥10,000` views):**
  1. `Be Smart` — [`yjSf7Yh9UZc`](https://youtu.be/yjSf7Yh9UZc) *The Strange and Unexpected Reason Ice is Slippery* (**`1,158,527` views**)
  2. `Veritasium` — [`Stx6kLd9dYI`](https://youtu.be/Stx6kLd9dYI) *Why Is Ice Slippery?* (**`806,131` views**; plus `Dr Ben Miles` [`fzhT-hB8w0w`](https://youtu.be/fzhT-hB8w0w) **`810,742` views** and `SmarterEveryDay` [`N7rR82Zk17U`](https://youtu.be/N7rR82Zk17U) **`5,991,243` views**)
- **Neighbour Gate (`neighbours.py`):** **PASS (`9` education videos `≥1,000,000` views, `TED-Ed/TED: yes`)** — saved in [`11_Upload-Package/evidence_2026-11-15_neighbours.json`](11_Upload-Package/evidence_2026-11-15_neighbours.json).

---

## 4. Candidate 4-Act Discovery Outline (All Claims UNVERIFIED Pending `SOURCES.md` & `facts` Lane)

- **Cold Open (0:00–0:45, UNVERIFIED):** Every winter, millions of people glide across frozen rinks on steel skate blades — and for more than a century, physics textbooks gave a tidy one-sentence explanation: the pressure of your skate lowers the freezing point of ice and squeezes a thin film of liquid water beneath the blade. Until someone actually calculated the pressure of a human on an ice skate — and proved it couldn't melt ice colder than about `-3.5 °C`.
- **Act I — Faraday's Two Ice Cubes vs. The Thomson Brothers' Piston (1849–1850, UNVERIFIED):** On 7 June 1850 at the Royal Institution in London, Michael Faraday presses two moist blocks of ice together at `0 °C` and shows they freeze solid at the contact point (`regelation`). Faraday proposes that ice always carries an intrinsic, quasi-liquid microscopic film on its free outer surface because surface molecules lack neighbours on one side. Months earlier (`1849–1850`), James Thomson and his brother William Thomson (Lord Kelvin) had predicted and measured that high pressure lowers water's freezing point by `0.0075 °C` per atmosphere — and Kelvin challenges Faraday, arguing that contact pressure alone explains the liquid film.
- **Act II — John Joly's 1886 Ice-Skate Calculation That Fooled Textbooks for a Century (UNVERIFIED):** In 1886, Irish physicist John Joly applies the Thomson pressure-melting formula to ice skating, estimating that a skater's blade concentrates enough pressure (`~466 atmospheres`) to melt ice underneath. Generations of encyclopaedias and school physics textbooks copy Joly's explanation as settled fact — ignoring that a real skate blade touches a larger contact patch (`~100–150 atmospheres`, lowering the melting point to only `-1 °C` to `-3.5 °C`), whereas people skate effortlessly at `-15 °C` and `-20 °C`.
- **Act III — Bowden & Hughes in a Swiss Alpine Ice Cave (1939, UNVERIFIED):** In 1939, Cambridge physicists Frank Philip Bowden and T. P. Hughes travel to the high-altitude Jungfraujoch research station in the Swiss Alps (`-3 °C` to `-80 °C` with dry snow and solid ice) and pull sliders made of brass, ebonite, wood, and ski wax across cold ice. Poor thermal conductors (ebonite, waxed wood) glide with lower friction than brass because frictional heat stays trapped at the microscopic contact peaks instead of conducting into the slider — showing frictional heating helps moving skates and skis, yet still cannot explain why ice is slippery the instant you step onto it at rest.
- **Act IV — Gabor Somorjai & Modern Surface Spectroscopy Vindicate Faraday (1996–2018, UNVERIFIED):** Using low-energy electron diffraction (`LEED`) and atomic force microscopy (`AFM`) at UC Berkeley (`1996–2002`, followed by sum-frequency generation spectroscopy), Gabor Somorjai and modern surface physicists image the top molecular layers of crystal ice and prove Faraday was right all along: even at `-20 °C` with zero pressure and zero sliding friction, the outermost water molecules on ice cannot form a full four-bond tetrahedral lattice and vibrate/roll in a permanent nanometer-thick quasi-liquid surface film.

---

## 5. Two Candidate Search-Titled Shorts (`Test B` / `Rule 26` — UNVERIFIED Concepts Only)

- **Short `S01`:** *Why Do Two Ice Cubes Freeze Together When Pressed?* (`50 chars`, `0` exact collisions)
  - **First-line answer hook (UNVERIFIED):** *"If you press two wet ice cubes together in a warm room, they instantly weld into one solid block — and in 1850, that kitchen trick sparked a war between Michael Faraday and Lord Kelvin."*
- **Short `S02`:** *Can Skate Pressure Really Melt Ice at Minus 20 Degrees?* (`55 chars`, `0` exact collisions)
  - **First-line answer hook (UNVERIFIED):** *"Your physics textbook probably told you ice skates glide because your body weight melts the ice under the blade — until you work out the pressure and find you'd need an elephant standing on the blade at minus 20 degrees."*
