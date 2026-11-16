# Topic Brief — `109_Lewis-Pickering-WilderSmith-Smulders-Why-Fingers-Wrinkle` (`HOS:109` Proposal)

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
  - **Shared pattern:** `002` and `004` together account for **`92.9%` (`1,997 / 2,149`) of all HOS long impressions** and **`86.7%` (`195 / 225`) of all HOS long views** because they sit inside core school-science search phrases (`periodic table`, `what's inside an atom`) with massive `TED-Ed` / `Veritasium` / `CrashCourse` neighbour clusters. Meanwhile `006` (*The Willow Tree That Was Made of Air*) shows that a concrete experiment hook holds strong retention (`66.54%` avg view %) once clicked, but a poetic/non-search title without an autocomplete phrase (`36` impressions in `10d`) gets starved of search impressions (`LEARNINGS.md` Rule 26).
- **3 Worst HOS Longs & What They Share (Hypotheses on Small N):**
  1. **`_C92tIJCk8A` (`001` *How Did We Discover Germs?*)** — **`0.10` views/day** (`7` views in `73d`), `44` impressions, `6.82%` CTR, `48.08%` avg view %.
  2. **`frP_YrNShsU` (`003` *How Did We Discover X-rays?*)** — **`0.10` views/day** (`5` views in `52d`), `41` impressions, `2.44%` CTR, `26.65%` avg view %.
  3. **`wwcjcFfC-5M` (`005` *The Tied Arm That Proved Your Blood Circulates*)** — **`0.29` views/day** (`5` views in `17d`), `15` impressions, `20.00%` CTR (3 clicks on 15 impressions), `9.24%` avg view %.
  - **Shared pattern (hypothesis given `5–7` views):** Generic textbook-chapter questions without a specific everyday mystery or visual hook (*How Did We Discover Germs?*, *How Did We Discover X-rays?*) and apparatus-only titles without the everyday search phrase (*The Tied Arm That Proved Your Blood Circulates*, `15` impressions) fail to earn YouTube search/browse impressions (`15–44` lifetime impressions). **Lesson applied to `HOS:109`:** Start Title A verbatim with the exact signed-out autocomplete phrase `"Why Do Fingers Wrinkle in Water?"` and add the concrete clinical discovery hook `(The Cut-Nerve Proof)`.

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
  - **Shared pattern:** Immediate physical or human-body test questions (*cutting gold in half*, *tight band on your arm*, *radioactive notebooks*) where the viewer can visualize or try the test on their own hand in 2 seconds (`LEARNINGS.md` Rules 18, 28, 32). Notice that `#2` (`PFj6172YU4Q` *One Tight Band Proved Your Blood Goes Round*, `31.29/d`) is a direct human-arm experiment — and `HOS:109` (*Why Do Fingers Wrinkle in Water? (The Cut-Nerve Proof)*) is an even more universal human-hand mystery with massive search demand.
- **3 Worst HOS Shorts & What They Share (Hypotheses on Small N):**
  1. **`LanTHJckYx8` (*What other table has empty chairs?*)** — **`0.07` views/day** (`4` views in `54d`), `33.33%` stayed-to-watch, `23.08%` avg view % (`6s / 26s`).
  2. **`zI_eD3vFWmE` (*The first X-ray showed a wedding ring*)** — **`0.18` views/day** (`9` views in `49d`), `50.00%` stayed-to-watch, `64.00%` avg view %.
  3. **`CnHwX1L9XHg` (*Gallium sat where the table said*)** — **`0.29` views/day** (`16` views in `56d`), `30.43%` stayed-to-watch, `33.45%` avg view %.
  - **Shared pattern:** Cryptic riddle titles (*What other table has empty chairs?*) or flat caption statements (*Gallium sat where the table said*, *The first X-ray showed a wedding ring*) with zero search intent and no self-contained physical question.

---

## 2. Overlap & Non-Duplication Check (`2026-11-15`)

Checked against:
- All folders in `02_Video-Projects/` (`000`–`018`, `099`–`101` on `main`),
- Open topic PRs `#572` (`102` Antikythera, `103` Deep-Sea Hydrothermal Vents), `#581` (`104` Speed of Light, `105` Stomach Acid Digestion), and `#588` (`106` Lightning Rod, `107` Photosynthesis Oxygen),
- All `011`–`097` backlog entries in `00_Brand/Channel-Setup/VIDEO_BACKLOG.json` and `00_Brand/Channel-Setup/ideas/IDEAS_*.md` (`005` covers William Harvey's blood circulation; `017` covers Galvani & Volta's bioelectricity; `031` covers Santiago Ramón y Cajal's neurons; `037` covers Otto Loewi's neurotransmitters; `046` covers Hodgkin & Huxley's giant squid axon; **none** cover why fingers wrinkle in water, Lewis & Pickering's 1935–1936 denervated finger clinical discovery, Wilder-Smith's 2003 glomus-body vasoconstriction proof, or Changizi & Smulders's rain-tread wet-grip experiments).
- **Result:** **Zero overlap.**

---

## 3. Packaging & Search Evidence (`Rule 26` + `neighbours.py` + `public_search.py`)

- **Title A (Primary Proposal, `54 chars`, `0` collisions):** `Why Do Fingers Wrinkle in Water? (The Cut-Nerve Proof)`
- **Title B (Test & Compare Arm 2, `54 chars`, `0` collisions):** `The Cut Nerve That Proved Why Fingers Wrinkle in Water`
- **Title C (Rule 26 Exact Phrase First, `60 chars`, `0` collisions):** `Why Do Fingers Wrinkle in Water? Not Because Skin Absorbs It`
- **Signed-out YouTube Autocomplete (`2026-11-15`):**
  - `"why do fingers wrinkle in water"` → **`autocomplete = yes`** (`why do fingers wrinkle in water`, `why do fingers wrinkle in water ted ed`, `why do fingers get wrinkled in water`, `why do fingers wrinkle in cold water`, `why do fingers wrinkle in water for kids`, `why do our fingers wrinkle in water`)
- **Rule 26(a) Two Ranking Videos (`≥10,000` views):**
  1. `Colossal Cranium` — *Why Do Your Fingers Wrinkle in Water?* (**`1,370,412` views**)
  2. `SciShow` — *Why Do Our Fingers and Toes Wrinkle in the Bath?* (**`1,180,362` views**; plus `TED-Ed` [`k7ve_ibAY1s`](https://youtu.be/k7ve_ibAY1s) *Why do fingers become pruney? - Mark Changizi* **`115,153` views**)
- **Neighbour Gate (`neighbours.py`):** **PASS (`11` education videos `≥1,000,000` views, `TED-Ed/TED: yes`)** — saved in [`11_Upload-Package/evidence_2026-11-15_neighbours.json`](11_Upload-Package/evidence_2026-11-15_neighbours.json).

---

## 4. Candidate 4-Act Discovery Outline (All Claims UNVERIFIED Pending `SOURCES.md` & `facts` Lane)

- **Cold Open (0:00–0:45, UNVERIFIED):** Stay in a warm bath for ten minutes and the skin on your fingertips and toes puckers into deep ridges and valleys. For generations, textbooks and doctors taught a simple osmotic explanation: the dead outer keratin layer of your skin absorbs water and swells up like a wet sponge. Until two London doctors in 1935 soaked the hands of patients with severed median nerves — and saw that the numb fingers stayed completely smooth while the healthy fingers right beside them wrinkled.
- **Act I — The Sponge Myth vs. Lewis & Pickering's 1935–1936 London Clinic (UNVERIFIED):** Under the classic osmosis explanation, fingertip skin wrinkles passively because water diffuses into the thick outer `stratum corneum` tethered to deeper tissue. Working at University College Hospital in London (`1935–1936`), Thomas Lewis and George Pickering study patients suffering from median-nerve palsy and sympathetic nerve injuries. When those patients immerse their hands in warm water, the fingers supplied by the cut nerve **fail to wrinkle at all** — proving that water wrinkling cannot be passive swelling of dead skin, and in `1973` plastic surgeon S. O'Riain turns the warm-water soak into a bedside clinical test to check whether a child's hand nerve is severed without needles or shocks.
- **Act II — Einar Wilder-Smith's 2003 Laser-Doppler Vasoconstriction Proof (UNVERIFIED):** If nerves control wrinkling, how does a nerve pull skin into grooves? In `2003` at the National University Hospital in Singapore, neurologist Einar Wilder-Smith and Adeline Chow attach laser-Doppler blood-flow sensors to volunteers' fingertips in warm water. They discover that as water enters sweat ducts and shifts electrolyte balance around sympathetic nerve fibres, the sympathetic nervous system triggers sudden vasoconstriction in the tiny digital `glomus bodies` (arteriovenous shunts beneath the fingertip ridges) — draining blood volume from the fingertip pulp and pulling the overlying skin downward into valleys.
- **Act III — Mark Changizi's 2011 Rain-Tread Drainage Hypothesis (UNVERIFIED):** Why would evolution wire an active sympathetic nerve reflex just to wrinkle wet hands and feet? In `2011`, evolutionary neurobiologist Mark Changizi and colleagues analyse the geometry of wet fingertip wrinkles and show they are not random buckles: they form a branching network of watershed channels all connected at the top and diverging toward the edges — identical to river drainage basins and car-tyre rain treads designed to channel sheets of water out from under the contact pad during a press.
- **Act IV — Smulders & Kareklas's 2013 Newcastle Wet-Marble Experiment (UNVERIFIED):** In `2013` at Newcastle University, Kyriacos Kareklas, Daniel Nettle, and Tom Smulders put Changizi's rain-tread prediction to a timed experimental test: volunteers transfer submerged wet glass marbles and lead fishing weights from one container to another through a thumb-and-index-finger slot, once with smooth dry-soaked fingers and once after 30 minutes in `40 °C` water. Wrinkled fingers transfer submerged objects **`~12%` faster** than unwrinkled fingers, while providing **zero speed advantage** on dry marbles — explaining why the reflex fires in water but leaves fingers smooth on dry land.

---

## 5. Two Candidate Search-Titled Shorts (`Test B` / `Rule 26` — UNVERIFIED Concepts Only)

- **Short `S01`:** *Why Doesn't Cut-Nerve Skin Wrinkle in Warm Water?* (`49 chars`, `0` exact collisions)
  - **First-line answer hook (UNVERIFIED):** *"If you cut the median nerve in your wrist and soak your hand in warm bathwater, three of your fingers won't wrinkle at all — and in 1935, that hospital accident destroyed the sponge myth forever."*
- **Short `S02`:** *Do Wrinkled Fingers Really Help You Grip Wet Objects?* (`53 chars`, `0` exact collisions)
  - **First-line answer hook (UNVERIFIED):** *"Your fingers don't wrinkle in the bath because your skin absorbs water — your nervous system carves temporary rain treads into your fingertips, and in 2013 scientists timed it with wet marbles."*
