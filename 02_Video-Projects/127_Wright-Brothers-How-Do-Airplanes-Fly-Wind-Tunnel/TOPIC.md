# Topic Brief — `127_Wright-Brothers-How-Do-Airplanes-Fly-Wind-Tunnel` (`HOS:127` · Rule-E GO in `next_hos`)

> **RULE-E GO & RULE G STATUS (`J3245` proposal · `J3264` Rule-E GO `97.2 / 100`, `2026-11-21`):**
> - **Status:** Added to the History of Science backlog (`jobs/WIP.json` `next_hos`, OWB PR `#1094`) and **pre-cleared GO (`97.2 / 100` · `9.72 / 10`)** by `J3264` under **Rule E**. Stays in `next_hos` under **Rule G** (`active` has `4 / 4` HOS slots full: `008`, `009`, `010`, `013`). Nothing is started in production (`status.json` stages are all `todo`; `£0.00` spent). Full review: [`11_Upload-Package/TOPIC_GO_NO_GO_SHEET.md`](11_Upload-Package/TOPIC_GO_NO_GO_SHEET.md) and [`11_Upload-Package/TOPIC_OPPORTUNITY_SCORE.md`](11_Upload-Package/TOPIC_OPPORTUNITY_SCORE.md).
> - **2027 Search Plan Alignment (`J3224`, approved by Ben `2026-11-20` in `orbit-with-ben` `2803f878c`):** Directly implements **Cluster 4 Lead Film (Thu 28 Jan 2027)** from `05_Analytics/hos/search_research/2026-11-20.md` (`wright brothers first flight`: `19,018` est. monthly searches, comp `45`, `the wright brothers` `+74.8%` growth, `10/10` US SERP gap, verified sub-50k breakouts `History Dude` 1.1K US → `51.9K` 13× & `Acta Historia` 1.2K CA → `1.4K` 12×).
> - **Awaits Active HOS Slot, `SOURCES.md` & `facts` Lane:** All historical and scientific claims in this brief are **UNVERIFIED** working notes. Before any script is locked, VO is recorded, or picture credit is spent, every claim must be backed by verbatim primary-source quotes in `SOURCES.md` and verified through the `facts` lane (`gemini-agy`).

---

## 1. HOS Data Comparison (`2026-11-20` Snapshot + `studio_ctr.json` + `channel_daily.json`)

- **Data sources read:**
  - `05_Analytics/hos/snapshots/2026-11-20.json` (`takenAt: 2026-11-20T06:40:34.014Z`, `40` public videos = `7` longs + `33` Shorts, `4,387` total views, `6` subscribers)
  - `05_Analytics/hos/studio_ctr.json` (`readAt: 2026-11-20T07:16:24.533881+00:00`, lifetime Studio impressions, CTR, average view %, and Shorts stayed-to-watch %)
  - `05_Analytics/hos/channel_daily.json` (`through: 2026-11-18`, `84` daily rows; peak days `2026-10-16` `1,173` views / `105` min, `2026-11-15` `223` views, `2026-11-08` `216` views, `2026-10-26` `207` views) and `05_Analytics/hos/REPORT.md`
  - `05_Analytics/LEARNINGS.md` (rules `1–22`, plus active HOS rules `23–38`) and `05_Analytics/hos/search_research/2026-11-20.md` (`J3224`)
- **Elapsed-day denominator (`age_days`):** `max((date(2026, 11, 20) - date.fromisoformat(publishedAt[:10])).days, 1)` (`views/day = views / age_days`).
- **Small-sample caveat (`Rule 1`):** Five of the seven public HOS longs have `5–14` lifetime views (`17–64` impressions), and bottom-tier Shorts have `3–24` views. Patterns from `<100`-view videos are descriptive hypotheses only.

### 1a. All `7` Public HOS Longs — Ranked by Views/Day Since Publish (`2026-11-20`)

| Rank | Video ID | Film | Title | Published (`age_days`) | Length | Views (`11-20`) | Views / Day | Studio Impressions | Studio CTR | Studio Avg View % (Lifetime) | YTA Lifetime Avg View % |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **1** | `AL_-qlWko_g` | `002` | *How Did We Discover the Periodic Table?* | `2026-09-17` (`64d`) | `541s` | **162** | **2.53/d** | **1,139** | 3.4% | 21.0% (`114s`) | 21.23% |
| **2** | `GHZDsiH7L7A` | `004` | *What's Inside an Atom? Mostly Empty Space* | `2026-10-15` (`36d`) | `525s` | **35** | **0.97/d** | **840** | 1.4% | 23.0% (`128s`) | 23.54% |
| **3** | `VbPubYd6Fbs` | `006` | *The Willow Tree That Was Made of Air* | `2026-11-05` (`15d`) | `532s` | **14** | **0.93/d** | 64 | 4.7% | **48.12%** (`256s`) | **53.96%** |
| **4** | `ETynHpIYLeY` | `007` | *How Was the First Vaccine Made? (And Why It's Named After a Cow)* | `2026-11-12` (`8d`) | `532s` | **7** | **0.88/d** | 44 | 4.6% | 19.17% (`102s`) | 28.49% |
| **5** | `wwcjcFfC-5M` | `005` | *The Tied Arm That Proved Your Blood Circulates* | `2026-10-29` (`22d`) | `529s` | **6** | **0.27/d** | **17** | 17.6% | **7.75%** (`41s`) | **9.24%** |
| **6** | `_C92tIJCk8A` | `001` | *How Did We Discover Germs?* | `2026-09-03` (`78d`) | `365s` | **7** | **0.09/d** | 41 | 7.3% | 47.95% (`175s`) | 48.08% |
| **7** | `frP_YrNShsU` | `003` | *How Did We Discover X-rays?* | `2026-09-24` (`57d`) | `426s` | **5** | **0.09/d** | 40 | 2.5% | 26.53% (`113s`) | 26.65% |

- **3 Best HOS Longs & What They Share:**
  1. **`AL_-qlWko_g` (`002` *How Did We Discover the Periodic Table?*, `541s`)** — **`2.53/d`** (`162` views, `1,139` impressions, `3.4%` CTR, `21.0%` Studio avg view %).
  2. **`GHZDsiH7L7A` (`004` *What's Inside an Atom? Mostly Empty Space*, `525s`)** — **`0.97/d`** (`35` views, `840` impressions, `1.4%` CTR, `23.0%` Studio avg view %).
  3. **`VbPubYd6Fbs` (`006` *The Willow Tree That Was Made of Air*, `532s`)** — **`0.93/d`** (`14` views, `64` impressions, `4.7%` CTR, channel-best **`48.12%` Studio / `53.96%` YTA avg view %**).
  - **Shared pattern:** `002` and `004` capture **`90.6%` (`1,979 / 2,185`) of all HOS long impressions** through direct, high-volume search questions backed by TED-Ed/education neighbours (`Rules 1, 15, 26`), run `8:45–9:01` (`525–541s`), use a single 3D painted hero object on the right with clear left-band serif text (`Rules 12, 14`), and open with a concrete physical experiment/paradox rather than a generic survey (`Rule 10`; `006`'s physical measurement paradox holds `48–54%` avg view %).
- **3 Worst HOS Longs & What They Share (Small-N Hypotheses):**
  1. **`frP_YrNShsU` (`003` *How Did We Discover X-rays?*, `426s`)** — **`0.09/d`** (`5` views, `40` impressions, `2.5%` CTR, `26.53%` Studio avg view %).
  2. **`_C92tIJCk8A` (`001` *How Did We Discover Germs?*, `365s`)** — **`0.09/d`** (`7` views, `41` impressions, `7.3%` CTR, `47.95%` Studio avg view %).
  3. **`wwcjcFfC-5M` (`005` *The Tied Arm That Proved Your Blood Circulates*, `529s`)** — **`0.27/d`** (`6` views, **`17` impressions**, `17.6%` CTR, **`7.75%` Studio avg view %**).
  - **Shared pattern:** Literary statement title with no search phrase (`005`, `17` impressions, `7.75%` retention) or shorter early survey titles (`001` `365s`, `003` `426s`) lacking a concrete twist or stakes tail (`Rules 11, 15, 23, 26`).

### 1b. All `33` Public HOS Shorts — Summary Ranking (`2026-11-20`)

Full `33`-row table mirrors `HOS:126` (`2026-11-20.json` + `studio_ctr.json`):
- **Top velocity & mature winners (`≥100` views):** `#1` `xzKoHg0E0_U` (*What Is Dalton's Atomic Theory?*, `208`v, **`52.00/d`**, `52.0%` stayed, `60.0%` avg viewed), `#2` `Wvjd8g0CpzE` (*The Blood Vessels Finer Than a Hair*, `215`v, **`43.00/d`**, `14.6%` stayed MISS, `76.0%` avg viewed), `#3` `29bpGAI0wb8` (*What happens if you keep cutting gold in half?*, **`1,228`v**, **`35.09/d`**, `40.8%` stayed, `44.0%` avg viewed, `12` likes), plus double-PASS champion **`-3L6HzJ_d_4`** (*What Is the Pasteur Swan Neck Flask Experiment?*, `19s`, `138`v, `5.75/d`, **`78.7%` stayed PASS**, **`74.0%` avg viewed PASS**) and loop winners **`oKqmnJNGiHg`** (`193`v, `6.43/d`, `42.0%` stayed, **`87.0%` PASS**), **`pWySvZsneZg`** (`137`v, `7.21/d`, `37.2%` stayed, **`112.0%` LOOP**), and **`c2q7w0pgcn8`** (`138`v, `4.31/d`, `43.5%` stayed, **`105.0%` LOOP**).
- **3 Worst HOS Shorts:** `#33` `LanTHJckYx8` (*What other table has empty chairs?*, `26s`, `4`v, `0.07/d`, `33.3%` stayed, `23.08%` avg viewed), `#32` `zI_eD3vFWmE` (*The first X-ray showed a wedding ring*, `25s`, `9`v, `0.17/d`, `50.0%` stayed, `64.0%` avg viewed), `#31` `CnHwX1L9XHg` (*Gallium sat where the table said*, `26s`, `16`v, `0.26/d`, `30.4%` stayed, `30.77%` avg viewed).
- **Shared lesson:** Positive search questions naming a physical experiment or famous object + moving 3D cartoon frame 0 + payoff withheld past `≥70%` + tight `16–19s` loop cut (`Ben 19 Nov Shorts house rules`, `LEARNINGS.md` Rules 1, 2, 3, 6, 8, 24, 27, 28, 32) beat cryptic riddles and declarative statements by `3–5×` on stayed-to-watch (`40.8–78.7%` vs `14.6–16.7%`).

---

## 2. Overlap & Non-Duplication Check (`2026-11-21`)

Checked across:
- All folders in `02_Video-Projects/` (`000`–`018`, `099`–`119` on `main`),
- Open HOS backlog PRs (`#682`–`#692` & OWB `#1033`/`#1051`/`#1059`): `120` *Why Do We Cry?*, `121` *Why Do Cats Purr?*, `122` *Why Do We Sneeze?*, `123` *Why Does Hair Turn Grey?*, `124` *Why Is the Ocean Salty?*, `125` *What Causes the Tides?*, plus `126` *What Is the Higgs Boson?* (paired in `J3245`),
- All `011`–`095` ideas folders and `IDEAS_*.md` files under `00_Brand/Channel-Setup/ideas/`, `VIDEO_BACKLOG.json`, and `jobs/WIP.json` (`active` + `next_hos`).
- **None** cover the Wright brothers, their 1901 Dayton bicycle-shop wind tunnel, John Smeaton's flawed 1759 air-pressure coefficient (`0.005` vs `0.0033`), Otto Lilienthal's lift tables, wing-warping three-axis control, or how an airplane wing generates lift.
- **Result:** **Zero overlap.**

---

## 3. Packaging, Why It Should Work & Search/Neighbour Evidence (`Rule 26` + `J3224` + `neighbours.py` + `public_search.py`)

- **Title A (Primary Proposal, `LEARNINGS.md` Rules 1, 15, 23, 26 — `44 chars ≤ 50`, `0` exact collisions):** `How Do Airplanes Fly? (The 1901 Wind Tunnel)`
- **Title B (Test & Compare Arm 2, `J3224` Lead Film 4 Exact Phrase — `50 chars ≤ 50`, `0` exact collisions):** `Wright Brothers First Flight: The 1901 Wind Tunnel`
- **Title C (`Rules 1, 15, 23` — `48 chars ≤ 50`, `0` exact collisions):** `How Did the Wright Brothers Solve Flight? (1901)`
- **One-Line Hook:** After their 1901 glider produced barely a third of the lift promised by 142-year-old textbooks, Wilbur and Orville Wright built a 6-foot wooden wind tunnel in their Ohio bicycle shop, tested over 200 tiny metal wings in two months, proved the flight tables wrong — and unlocked controlled powered flight.
- **Why It Should Work (Past Winners, `LEARNINGS.md` Rules & `J3224` Search Demand):**
  - Combines the two winning signals in our HOS data: high-demand everyday/school search framing like **`002` Periodic Table (`AL_-qlWko_g`, `162` views, `2.53/d`, `1,139` impressions, `3.4%` CTR)** and **`004` Inside an Atom (`GHZDsiH7L7A`, `35` views, `0.97/d`, `840` impressions)** (`Rules 1, 15, 26`), paired with a single-apparatus experimental proof story (a wooden bike-shop wind tunnel with hacksaw-blade balances) that holds watch time like **`006` Willow Tree (`VbPubYd6Fbs`, `48.12%` Studio / `53.96%` YTA avg view %)** (`Rule 10`).
  - Directly implements **Lead Film 4 (Thu 28 Jan 2027)** of Ben's approved `hos-search-2027-01` plan (`J3224`, `05_Analytics/hos/search_research/2026-11-20.md` Cluster 4): `wright brothers first flight` averages `19,018` searches/mo (comp `45`, `the wright brothers` `+74.8%` growth) with a **`10/10` US signed-out SERP gap** (old 3+ yr raw newsreel clips, zero 3D narrative science explainers) and strong US/UK/CA/AU adult curiosity (`History Dude` 1.1K US → `51.9K` 13×; `Acta Historia` 1.2K CA → `1.4K` 12×).
  - Ideal fit for HOS's warm 3D cartoon period craft (1901 Dayton bicycle workshop, spinning fan blades, brass airfoil balances, Kill Devil Hills wind-blown sand dunes) and `16–19 s` question Shorts (`Rules 2, 3, 6, 8, 24, 27, 28, 32`).
- **3-Way Thumbnail Test & Compare Plan (`LEARNINGS.md` Rules 11, 12, 14 + `THUMBNAIL_AND_TITLE_RULES.md` §2.1–2.B):**
  - **Thumb A (Hero Object — The 1901 Wooden Wind Tunnel):** Warm 3D painted key art of the Wrights' 6-foot wooden wind tunnel with a glass viewing top showing streamlines curving over a glowing miniature brass airfoil mounted on a bicycle-spoke balance; Explorer small lower left; clear left-band cream/gold serif lettering: `200 TINY WINGS` (`3 words`, gold on `200`, zero overlap on hero, no other AI-made text).
  - **Thumb B (`Rule 14` Bright High-Contrast Variant — Kitty Hawk Wing-Warp Flight):** Bright sunlit coastal sand dunes and crisp blue sky: the 1903 Wright Flyer banking cleanly just above the sand with subtle golden airflow ribbons curving over its twisted canvas wing; Explorer small lower left; clear left-band serif lettering: `THE TABLES LIED` (`3 words`, gold on `LIED`, zero overlap).
  - **Thumb C (Apparatus vs Textbook Twist):** Warm 3D painted workshop bench: an open leather 1759 physics ledger crossed with a dramatic red ink line beside a tiny gleaming metal wing tilting upward on a brass balance; Explorer small lower left; clear left-band serif lettering: `50% TOO HIGH` (`3 words`, gold on `50%`, zero overlap; corrected from `WRONG BY 40%` in `J3264` to match `0.005` vs `0.0033` = `+51.5%`, pending `SOURCES.md`).
- **Signed-out YouTube Autocomplete (`2026-11-21`, `public_search.py`):**
  - `"how do airplanes fly"` → **`autocomplete = yes`** (`10` suggestions; note `search = []` on this single query while paired queries returned `64` search rows)
  - `"wright brothers first flight"` → **`autocomplete = yes`** (`10` suggestions)
  - `"wright brothers wind tunnel"` → **`autocomplete = yes`** (`1` exact suggestion)
  - `"how does an airplane wing work"` → **`autocomplete = yes`** (`3` suggestions — exact JSON count verified in `J3264`)
  - **Exact title collisions:** `0` across all `3` long title options (`A`, `B`, `C`) and both Short titles (`S01`, `S02`).
- **Rule 26(a) Two Ranking Videos (`≥10,000` views, retrieved `2026-11-21`):**
  1. `TED-Ed` — [`p4VHMsIuPmk`](https://youtu.be/p4VHMsIuPmk) *How do airplanes actually fly? - Raymond Adkins* (**`2,568,211` views**)
  2. `Simple History` — [`YDlk4Ky_ahs`](https://youtu.be/YDlk4Ky_ahs) *The Wright Brothers, First Successful Airplane (1903)* (**`1,410,350` views**; plus `Sabin Civil Engineering` [`LigpsX1KoQE`](https://youtu.be/LigpsX1KoQE) **`4,461,586` views**, `minutephysics` [`Gg0TXNXgz-w`](https://youtu.be/Gg0TXNXgz-w) **`2,481,276` views**, `Math and Science` **`2,044,514` views**, `Veritasium` [`aFO4PBolwFg`](https://youtu.be/aFO4PBolwFg) **`1,662,162` views**, and `Naked Science` **`1,583,808` views**)
- **Neighbour Gate (`neighbours.py "how do airplanes actually fly" "wright brothers airplane" "airfoil lift" --top 25 --phrase "how do airplanes fly"`):** **PASS (`8` education videos `≥1,000,000` views in raw output, of which `6` are strictly on-topic `≥1M` after excluding `2` airplane-keyword false positives `dzrwnwOx0fw` riddle & `iKYHf22qVdM` airplane mode; `TED-Ed/TED: yes`)** — saved in [`11_Upload-Package/evidence_2026-11-21_neighbours.json`](11_Upload-Package/evidence_2026-11-21_neighbours.json):
  1. `TED-Ed` ★ — [`p4VHMsIuPmk`](https://youtu.be/p4VHMsIuPmk) *How do airplanes actually fly? - Raymond Adkins* (**`2,568,211` views**, Tier 1, strictly on-topic)
  2. `TED-Ed` ★ — [`hd8tYiLSmn0`](https://youtu.be/hd8tYiLSmn0) *Why are airplanes slower than they used to be? - Alex Gendler* (**`2,519,461` views**, Tier 1, aviation/aerodynamics)
  3. `minutephysics` — [`Gg0TXNXgz-w`](https://youtu.be/Gg0TXNXgz-w) *How Do Airplanes Fly?* (**`2,481,276` views**, Tier 2, strictly on-topic)
  4. `SciShow Kids` — [`VLpSxHwfU04`](https://youtu.be/VLpSxHwfU04) *How Airplanes Fly! | Airplane Science | SciShow Kids* (**`1,754,830` views**, Tier 2, strictly on-topic)
  5. `Veritasium` — [`aFO4PBolwFg`](https://youtu.be/aFO4PBolwFg) *How Does A Wing Actually Work?* (**`1,662,146` views**, Tier 2, strictly on-topic)
  6. `Simple History` — [`YDlk4Ky_ahs`](https://youtu.be/YDlk4Ky_ahs) *The Wright Brothers, First Successful Airplane (1903)* (**`1,410,350` views**, Tier 2, strictly on-topic; plus `Real Engineering` [`WCPapu78SNM`](https://youtu.be/WCPapu78SNM) **`384,056` views** & `SciShow` [`9S7H8TlkBC4`](https://youtu.be/9S7H8TlkBC4) **`293,525` views**; note: `5` of the `6` `≥1M` rows are strictly on lift/Wright brothers if broader aviation `hd8tYiLSmn0` is set aside — still well above the `3`-video gate)

---

## 4. Candidate 4-Act Discovery Outline (All Claims UNVERIFIED Pending `SOURCES.md` & `facts` Lane)

- **Cold Open (0:00–0:45, UNVERIFIED):** Open straight on the 6-foot wooden wind tunnel roaring inside the Wright brothers' 1901 Dayton bicycle shop (`0:00–0:05`), cutting to a tiny curved metal airfoil tilting upward on a hacksaw-blade and bicycle-spoke balance (`0:05–0:15`). Zero agenda line (`Rules 10, 38`). State the twist: everyone remembers Kitty Hawk in 1903, but the real breakthrough happened two years earlier inside a noisy back room in Ohio — when two bicycle mechanics proved a 142-year-old flight equation was fatally wrong.
- **Act I — The 1901 Failure & Wilbur's 1,000-Year Despair (1900–1901, UNVERIFIED):** At Kill Devil Hills in summer **1901**, the Wright brothers built their largest glider strictly from **Otto Lilienthal's** lift tables and **John Smeaton's 1759** air-pressure coefficient (`0.005`). In steady Atlantic wind, the glider generated barely a third of its predicted lift and pitched wildly backward. On the train home to Dayton, **Wilbur Wright** reportedly told **Orville** that man would not fly for a thousand years.
- **Act II — The Bicycle-Shop Wind Tunnel & 200 Miniature Wings (Autumn 1901, UNVERIFIED):** Rather than quit, the brothers suspected the textbooks themselves. First they mounted a flat metal plate and a curved wing on a horizontal third bicycle wheel bolted to the front of a bike and pedalled down Dayton streets; then in October–December **1901** they built a **6-foot-long wooden wind tunnel** (`16-inch` square cross-section) driven by a belt-powered fan with a honeycomb grid to straighten the air. Using two ingenious balances made from **hacksaw blades and bicycle spokes**, they tested over **200 miniature tin/steel airfoil shapes** at different angles — measuring lift-to-drag ratios directly without needing to know exact wind speed.
- **Act III — Catching Smeaton's Error & Solving Three-Axis Control (1901–1902, UNVERIFIED):** Their tunnel data exposed the hidden culprit: Smeaton's `0.005` coefficient was roughly **50% too high** (the true value sits near **`0.0033`**), and long, narrow, gently cambered wings dramatically outperformed thick, deeply curved ones. Returning with the **1902 glider**, they hit one final killer mystery — **adverse yaw** (the rising wing dragged more, spinning the glider sideways) — and solved it by linking **wing-warping** (roll) to a **movable rear rudder** (yaw) alongside the front elevator (pitch): the three-axis control system every airplane still uses today.
- **Act IV — 17 December 1903: 12 Seconds That Rewrote Aerodynamics (1903, UNVERIFIED):** With accurate wing tables, custom hand-carved propellers treated as rotating wings (achieving ~66% efficiency), and a lightweight cast-aluminium engine built with machinist **Charlie Taylor**, the **1903 Wright Flyer** lifted off at **10:35 a.m. on 17 December 1903** for **12 seconds and 120 feet**, reaching **59 seconds and 852 feet** on the fourth flight that same morning — proving flight wasn't about brute engine power, but about measuring lift and mastering control.
- **Primary-Source Verification Guardrails (Mandatory Before Script Lock):**
  1. **Wright Brothers' 1901 wind tunnel & balances (Smithsonian NASM / Wright Papers, McFarland ed.):** Verify exact tunnel dimensions (`~6 ft` long, `16 in` square), dates (`Oct–Dec 1901`), number of model airfoils tested (`~200`, detailed measurements on `~40–50`), and hacksaw-blade / bicycle-spoke lift and drift balance mechanics.
  2. **Smeaton's coefficient (`1759` vs `1901`):** Verify John Smeaton's 1759 Royal Society windmill paper value (`0.005 lb/ft²/mph²`) vs the Wright brothers' empirically corrected `0.0033` (and modern standard sea-level value `~0.00327`).
  3. **1901 despair quote & 1902 three-axis control:** Verify Wilbur's exact wording (`"not within a thousand years"` / `"fifty years"` in Orville's recollections — do not conflate variants) and the Oct 1902 hip-cradle linkage of wing-warping + movable rudder.
  4. **17 December 1903 flights (Orville Wright diary / Telegram to Milton Wright):** Verify all four flight durations and distances (`12s / 120 ft`, `12s / 175 ft`, `15s / 200 ft`, `59s / 852 ft`), Charlie Taylor's engine weight/horsepower (`~12 hp`), and propeller efficiency.
- **Additional Rule-E Script-Stage Guardrails (`J3264`, `2026-11-21`):**
  5. **Smeaton percentage math:** Keep the denominator consistent (`0.005` vs `0.0033` = `+51.5%` / ~50% too high, or `−34.0%` going the other direction — never `"40%"`); verify `0.0033` vs `0.00327` in `SOURCES.md`.
  6. **No equal-transit-time lift fallacy:** Explain wing lift via **pressure difference + downward deflection of airflow** (momentum conservation / Newton's 3rd law + Bernoulli pressure gradient) and empirical wind-tunnel lift-to-drag ratios — never claim split air parcels must reunite at the trailing edge.
  7. **5-part HOS structure & geography/WHO accuracy:** Expand the 4-act sketch to 5 parts (`7–9 min`, mapped in `11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md` §5); distinguish **Kill Devil Hills** (flight site) from **Kitty Hawk** (post office/telegraph); keep every `WHO` card role accurate for 1901–1903 with birth–death years verified in `SOURCES.md`.

---

## 5. Two Candidate Search-Titled Shorts (`16–19 s` Ben 19 Nov House Rules · `Rule 32` · UNVERIFIED Concepts Only)

- **Short `S01`:** *Why Did the Wright Brothers Build a Wind Tunnel?* (`48 chars`, `0` exact collisions, positive search question)
  - **First-line answer hook (`0.0–1.5s`, `vo_onset_s ≤ 0.15s`, UNVERIFIED):** *"The Wright brothers proved a 142-year-old flight equation was wrong inside a bicycle shop."* (Concrete fact on line 1, names the subject and surprise within `1.5 s`, zero meta-promise.)
  - **Frame-0, Runtime & Loop Plan (Ben 19 Nov Shorts house rules · `16–19 s` · `Rules 2, 3, 6, 24, 27, 32`):**
    - Frame 0 (`0.0s`, full-bleed `9:16` premium **3D cartoon** moving plate, `0%` Explorer, `0%` bars/stills): glowing airflow ribbons racing through the Wrights' 6-foot wooden wind tunnel over a tiny curved brass wing tilting on a spoke balance; frame-0 caption line 1 carries the concrete fact (`A 142-YEAR-OLD EQUATION WAS WRONG`, yellow on `WRONG`).
    - Target runtime: **`17.5 s`** (`16.0–19.0 s` house band). Cut 1 `≤2.8s`, all holds `≤3.5s`. Single mid-Short `WHEN` stamp: `DAYTON, 1901` (white Didot italic inside `16:9` centre band, clear of `0–2s` and `9–14s`).
    - Payoff start at `≥70%` (`~12.5s / 17.5s`): after testing 200 miniature wings, they discovered the textbook lift number was 50% too high — fixing the tables that let their 1903 plane fly, because *(loops cleanly into line 1: "The Wright brothers proved a 142-year-old flight equation…")*. Crossfade `≤0.3s` back to frame 0, zero CTA.
- **Short `S02`:** *How Did the Wright Brothers Steer the First Plane?* (`50 chars`, `0` exact collisions, positive search question)
  - **First-line answer hook (`0.0–1.5s`, `vo_onset_s ≤ 0.15s`, UNVERIFIED):** *"Early flyers crashed by steering like ships — the Wright brothers twisted the wings instead."* (Concrete fact on line 1 within `1.5 s`, zero meta-promise.)
  - **Frame-0, Runtime & Loop Plan (Ben 19 Nov Shorts house rules · `16–19 s` · `Rules 2, 3, 6, 24, 27, 32`):**
    - Frame 0 (`0.0s`, full-bleed `9:16` premium **3D cartoon** moving plate, `0%` Explorer, `0%` bars/stills): close moving 3D shot of the 1903 Wright Flyer's taut canvas wing flexing and twisting cleanly as it banks over sunlit Kitty Hawk dunes; frame-0 caption line 1 carries the concrete fact (`THEY TWISTED THE WHOLE WING`, yellow on `TWISTED`).
    - Target runtime: **`18.0 s`** (`16.0–19.0 s` band). Cut 1 `≤2.8s`, all holds `≤3.5s`. Single mid-Short `WHEN` stamp: `KITTY HAWK, 1902` (white Didot italic, clear of `0–2s` and `9–14s`).
    - Payoff start at `≥70%` (`~13.0s / 18.0s`): twisting a cardboard inner-tube box showed Wilbur how to roll a wing like a bird — and linking it to a rear rudder stopped the spin that doomed everyone else, which is why *(loops cleanly into line 1: "Early flyers crashed by steering like ships…")*. Crossfade `≤0.3s` back to frame 0, zero CTA.
