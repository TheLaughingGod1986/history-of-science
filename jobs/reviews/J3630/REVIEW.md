# HOS 128 — Direct Quote Verification & Chief Lock Ruling (`J3630`)

- **Job:** `J3630` (`kind: review`)
- **Reviewer & Decision Authority:** `gemini` (elected Acting Chief under Ben's 24 Nov 2026 chain `Claude -> Codex -> Gemini -> Grok`; `chief_relay.py status` re-verified `Chief: Gemini` immediately prior to ruling)
- **Date:** `2026-11-25` (UTC)
- **Verdict:** **`FIX` (NOT `KEEP` · NOT LOCKED)**
- **Protected-call disposition:**
  - **PR `#758` (`macbook/J3628`) & PR `#760` (`gemini/J3629-hos128-facts`):** **NOT merged.** Only complete `KEEP` permits merging the script PR and queueing VO.
  - **VO / Picture / Scheduling / Spend:** **None queued, none scheduled, £0.00 / 0 credits spent.** Picture continues to wait for VO PASS after script lock.
  - **Original `J3547`:** **Ruling recorded; remains `blocked`** (closed only when actual script lock is achieved on a clean `KEEP`).
  - **Target & contingency:** Preserves **Thu 10 Dec 2026, 18:00 London** target and **Mon 7 Dec → Thu 17 Dec** slip contingency.
  - **Packaging caveat:** Draft thumbnail concepts (`WASTED AS HEAT`, `HIGH VOLTAGE`, held `22 MILES AWAY`) are **unrendered concepts, NOT rendered packaging PASS** (later rendered thumbs still require independent packaging panel, `style_sheet.py`, and `168×94` review after VO PASS).

---

## 1. Exact Audited Input Hashes (PR `#760` head `6f0ff4a3` / PR `#758` head `dc99d234`)

```text
32781f64a5d201970b90ec3d3ba14bd72c59290aa26b6732197e0d0fc30fe359  02_Video-Projects/128_Edison-Tesla-Westinghouse-Why-Do-We-Use-AC-Instead-Of-DC/01_Script/edison_tesla_ac_dc_script_master_v02.md
fbb43d3cd3fee9329279e20ec769daca60020cab7a637fd6bceb3bafa40a9c95  02_Video-Projects/128_Edison-Tesla-Westinghouse-Why-Do-We-Use-AC-Instead-Of-DC/10_Shorts/SHORTS_SCRIPTS_v02.md
15099bcec09648c9c429e468c7a51161cef3be6da5d4c45a93f2531d7271f21d  02_Video-Projects/128_Edison-Tesla-Westinghouse-Why-Do-We-Use-AC-Instead-Of-DC/01_Script/FACT_NOTES_v02.md
9f6b8d3159c5865b29f5da61afae4714e883fb54e85ee6e5bb4819fa5f4818f8  02_Video-Projects/128_Edison-Tesla-Westinghouse-Why-Do-We-Use-AC-Instead-Of-DC/01_Script/SOURCES.md
442f259ddd6e854c6a25aae3ae5a5bb4e7a5a2db7e5c4f4fd5bf1b5b6ede0c08  02_Video-Projects/128_Edison-Tesla-Westinghouse-Why-Do-We-Use-AC-Instead-Of-DC/01_Script/GEMINI_FACTS_CHECK_v02.md
ffdbdd884e5626b28b1db3dc40bcaf3391405d4ac1e3ec7c99ee84125a3e9465  02_Video-Projects/128_Edison-Tesla-Westinghouse-Why-Do-We-Use-AC-Instead-Of-DC/11_Upload-Package/PACKAGE_FIRST_SCORING_v02.md
176ea5500d7622e6f6dda6d99ddc47d9c32de69e338cd23dda3e4267ec85b2df  02_Video-Projects/128_Edison-Tesla-Westinghouse-Why-Do-We-Use-AC-Instead-Of-DC/11_Upload-Package/LAUNCH_PLAN.md
3436a0637507ec883664ee350deb88bd24eae2a6325008adf03387db1b7dfc03  02_Video-Projects/128_Edison-Tesla-Westinghouse-Why-Do-We-Use-AC-Instead-Of-DC/11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md
```

---

## 2. Six Blocking `FIX` Items Preventing Lock on `v02`

Every blocking item below was **independently verified directly against live institutional/primary pages, the scanned NPS PDF, repo JSON artifacts, and live CLI gates on `2026-11-25`** (zero `21 OK` inherited from `v01`):

1. **`FIX-1` (Spoken factual error — Long Part 01, line 21; confirms `J3629` FLAG-1):**
   - **Current `v02` text:** *"Eight months earlier, thirty-five-year-old Edison had proved the concept under London's Holborn Viaduct."*
   - **Direct verification:** NPS Edison Biography (`200 OK`) verbatim: `"Thomas Alva Edison was born on February 11, 1847 in Milan, Ohio"`. Rutgers Edison Papers 1882 Chronology (`200 OK`) verbatim: `"Jan 12 Edison's central station on Holborn Viaduct in London begins operation."` On 12 January 1882 Edison was **34 years old** (turning 35 on 11 Feb 1882; 35 at Pearl Street on 4 Sep 1882).
   - **Required `v03` fix:** Change Holborn Viaduct to `"thirty-four-year-old Edison"` (or move `"thirty-five-year-old"` to Pearl Street in September 1882).

2. **`FIX-2` (Spoken & visual `WHEN` card factual error — Long Part 03, lines 87 & 90; `FACT_NOTES` Row 11; `PRE_BUILD_VIDIQ_AUDIT.md` line 11; confirms `J3629` FLAG-2):**
   - **Current `v02` text:** *"On the eleventh of March, eighteen eighty-eight, Italian physics professor Galileo Ferraris published the same rotating-field discovery in Turin — yet never patented his work."* · `WHEN: Turin, 11 March 1888`.
   - **Direct verification:** Italian institutional records (*Accademia delle Scienze di Torino*, *MuseoTorino*, *Treccani*, *UniPi*, *AIF*, and `it.wikipedia.org/wiki/Galileo_Ferraris`) confirm Ferraris **presented** his memoir (*"Rotazioni elettrodinamiche prodotte per mezzo di correnti alternate"*) to the Royal Academy of Sciences of Turin on **18 March 1888** (`18 marzo 1888`), and it was **published** in **April 1888** (also confirmed verbatim on live `en.wikipedia.org/wiki/Induction_motor`: `"In April 1888, the Royal Academy of Science of Turin published Ferraris's research"`). English Wikipedia `Galileo_Ferraris`'s `"11 March 1888 published"` is wrong on both day and verb.
   - **Required `v03` fix:** Update line 87 to `"On the eighteenth of March, eighteen eighty-eight, Italian physics professor Galileo Ferraris presented the same rotating-field discovery in Turin — yet never patented his work."` Update line 90 to `WHEN: Turin, 18 March 1888` (and visual note to `"Ferraris's Turin lecture paper"`), plus align `FACT_NOTES_v03.md`, `SOURCES.md`, and `PRE_BUILD_VIDIQ_AUDIT.md`.

3. **`FIX-3` (Misquoted birthdate in `FACT_NOTES_v02.md` Row 8; confirms `J3629` FLAG-3):**
   - **Current `v02` note:** Quotes `https://ethw.org/William_Stanley` as `"born 28 November 1858"`.
   - **Direct verification:** Live `ethw.org/William_Stanley` (`200 OK`) does **not** contain `"28 November 1858"`; it verbatim reads `"William Stanley was born in Brooklyn, New York, 22 November 1858"`. (`WHO` card `1858–1916` is OK.)
   - **Required `v03` fix:** Correct `FACT_NOTES_v03.md` Row 8 to verbatim `"William Stanley was born in Brooklyn, New York, 22 November 1858"`.

4. **`FIX-4` (Non-existent quotation attributed to Wikipedia in `FACT_NOTES_v02.md` Row 10; confirms `J3629` FLAG-4):**
   - **Current `v02` note:** Attributes `"The induction motor relies on a rotating magnetic field to create torque without requiring physical electrical connections (brushes or commutators) to the rotating part"` to `https://en.wikipedia.org/wiki/Induction_motor`.
   - **Direct verification:** That string does **not** exist on live `en.wikipedia.org/wiki/Induction_motor` (`200 OK`). Live page verbatim quotes Sylvanus P. Thompson: `"no commutator or connection of any kind with the armature was required"`, alongside primary USPTO `US381968A` (`1888-05-01`, `200 OK`).
   - **Required `v03` fix:** Replace Row 10's non-existent quote with verbatim USPTO `US381968A` + Thompson quotes; add `[...]` ellipsis in Row 2; fold in the 6 verified primary institutional upgrades from `GEMINI_FACTS_CHECK_v02.md` (Rutgers Edison death & 1888 Harold Brown experiments, ETHW Westinghouse death, LOC Kemmler execution, UK SI 2002/2665 50 Hz / 230 V, US DOE 110–120 V / 60 Hz).

5. **`FIX-5` (False `0 exact collisions` claim for Candidate Title Arm B; confirms `J3629` FLAG-5):**
   - **Current `v02` packaging (`PACKAGE_FIRST_SCORING_v02.md` L30, `PRE_BUILD_VIDIQ_AUDIT.md` L52, `LAUNCH_PLAN.md` L24):** Reports `0` exact collisions (`2026-11-22`) for Candidate Arm B (*Thomas Edison vs Nikola Tesla: How AC Won the War of Currents*).
   - **Direct verification:** Programmatic inspection of `11_Upload-Package/evidence_2026-11-22_public_search.json` confirms its 11 query keys include Arm A, Arm C (`...Why AC Won`), `S01`, and `S02`, **but omit Candidate Arm B (`...How AC Won`)**.
   - **Required `v03` fix:** Run `public_search.py` on Candidate Arm B and save dated evidence (or explicitly mark Arm B's collision check `pending` until run).

6. **`FIX-6` (NEW mechanical defect caught in `J3630` — duplicate `master` filename breaks default `gate:episode`, violating `STUDIO_PLAYBOOK.md` §3 L85):**
   - **Direct verification:** Running `npm run gate:episode -- --project ../02_Video-Projects/128_...` (without `--script`) picked superseded **`01_Script/edison_tesla_ac_dc_script_master_v01.md`** (`92/100`, 20 `[VISUAL MUST]`, `v01` cold open) because `gate:episode` selects the first `master` file alphabetically.
   - **Required `v03` fix:** Rename superseded `v01` and `v02` scripts without `master` (e.g. `edison_tesla_ac_dc_script_v01_draft.md`, `edison_tesla_ac_dc_script_v02_draft.md`) so ONLY `edison_tesla_ac_dc_script_master_v03.md` carries `master` and default `gate:episode` (no `--script`) scores `v03` cleanly.

### Chief Ruling on Variance & Minor Alignment Polishes to Fold into `v03`

- **Niagara Falls distance (`22 miles` NPS vs `20 miles` ETHW) & Thumb B (`22 MILES AWAY`):** Directly inspected all 14 pages of scanned NPS National Register Nomination Form `NRIS 75001212` (`bccab15f-4fe0-4909-82a6-ca499a8883c2`, `200 OK`). Item 8 p. 5 (PDF p. 11) verbatim states: `"On November 15, 1896, the Niagara station began long-distance transmission to Buffalo, N.Y., 22 miles away."` Item 8 p. 4 (PDF p. 10) and Item 7 p. 1 (PDF p. 5) verbatim verify `27 October 1893` (`5,000-hp` Westinghouse contract) and `26 August 1895` local delivery. **Acting Chief ruling:** Accept federal NPS NRIS `75001212` as authoritative for `"15 November 1896"` and `"twenty-two miles"` in Long Part 05 and Short `S02`, while logging the ETHW `20 miles` / US DOE `Nov. 16` variance transparently in `FACT_NOTES_v03.md`. Keep **Thumb A (`WASTED AS HEAT`)** and **Thumb C (`HIGH VOLTAGE`)** as the working primary concepts and leave **Thumb B (`22 MILES AWAY`)** optional/secondary; **none** of the unrendered concepts is a rendered packaging PASS.
- **Three zero-churn polishes for `v03`:**
  1. Part 01 line 19 visual note: change `"six giant coal-fired iron dynamos"` → `"six giant iron dynamos driven by coal-fired steam engines"` (matches ETHW verbatim).
  2. Part 06 line 161 `DATA` #6 card: align on-screen text strictly to spoken numbers (`50 or 60 cycles per second`, removing unspoken `120 V or 230 V` from the card unless spoken) while keeping UK SI 2002/2665 and US DOE citations in `FACT_NOTES_v03.md`.
  3. Short `S02` overlay window: shift `TESLA PATENT · 1888` from `6.0–8.6 s` → `6.4–8.6 s` so it enters strictly on the `6.4 s` spoken patent clause (staying clear of the `9.0–14.0 s` title row).

---

## 3. Resolution Matrix — All 8 PR `#752` (`J3547`) Items + Teach/Polish/Craft

| PR `#752` Item | `v02` Status | Direct `J3630` Verification |
|---|---|---|
| **1. Pearl Street qualified & `3pm` removed** | **PARTIAL → `FIX-1`** | Holborn Viaduct (`12 Jan 1882`) and `"on the afternoon"` verified verbatim; `3:00 PM` gone. **Blocked by `FIX-1`:** Edison was **34**, not 35, on 12 Jan 1882. |
| **2. Stanley demo vs distribution, broken-one-mile, pitch scale** | **PARTIAL → `FIX-3`** | `500→3,000→500 V` (30 series lamps) cleanly separated from `500→100 V` Main St distribution (6 basement transformers, 20 businesses); broken-one-mile & pitch scale removed. **Blocked by `FIX-3`:** `FACT_NOTES` Row 8 misquotes `28 Nov` vs `22 Nov 1858`. |
| **3. Part 06 cycles vs reversals** | **RESOLVED** *(minor `DATA` #6 polish)* | Part 06 correctly states `50` / `60` full **cycles** per second, reversing twice per cycle (EIA verbatim). Remove unspoken `120 V / 230 V` from `DATA` #6 card in `v03`. |
| **4. Niagara element-by-element sourcing** | **RESOLVED** *(Chief ruling recorded)* | Scanned NPS NRIS `75001212` PDF pp. 5, 10, 11 & ETHW Adams Milestone visually/directly verified (`27 Oct 1893`, `26 Aug 1895`, `15 Nov 1896`, `22 miles`); `"at midnight"` & `"11,000 volts"` removed. Chief adopts NPS `22 miles` with ETHW `20 miles` variance logged. |
| **5. Mislabelled Wikipedia links, bids, motives, cable dims, causality** | **PARTIAL → `FIX-2`, `FIX-4`** | Direct institutional URLs separated honestly from `Secondary (Wikipedia)`; `$554k` vs `$399k` (US DOE), `80,000 ft` twin half-moon copper (ETHW), 1891+1893 Niagara causality (NPS), and motive removals verified. **Blocked by `FIX-2`** (Ferraris 18 vs 11 Mar 1888 & verb) and **`FIX-4`** (non-existent Wikipedia quote in Row 10). |
| **6. Long opening actual spoken timings** | **RESOLVED (planning check PASS)** | Direct word counts on `v02`: L05 `13w` (`5.2 s @150wpm`, `5.6 s @140wpm` ≤ `0:08` title question); L09 `cum 33w` (`13.2 s @150wpm`, `14.1 s @140wpm` ≤ `0:15` core answer + promise); L13 `cum 56w` (`22.4 s @150wpm`, `24.0 s @140wpm` ≤ `0:25` stakes); L17 `cum 87w` (`34.8 s @150wpm`, `37.3 s @140wpm` < `0:45` first real fact). Planning estimate only until measured VO. |
| **7. Shorts word counts & opening surprise** | **RESOLVED (planning check PASS)** | Direct counts on `SHORTS_SCRIPTS_v02.md`: `S01` `38` ws / `39` spoken (`15.6 s @150wpm`, `16.7 s @140wpm`, + pauses ≈ `~17.1 s`; first 4 words `"Edison's direct current couldn't"` ≈ `~1.6 s`); `S02` `38` ws / `40` spoken (`16.0 s @150wpm`, `17.1 s @140wpm`, + pauses ≈ `~17.4 s`; first 4 words `"Tesla's brushless motor broke"` ≈ `~1.6 s`). |
| **8. Shorts causal loop, caption, overlay plan** | **RESOLVED** *(minor `S02` `6.4 s` nudge)* | `S01` causal loop repaired, fixed 1-mile wall & red-hot wire removed, concrete-fact caption line 1, `10× VOLTS = 1/100 HEAT` (`4.5–8.5 s`, clear of `0–2 s` & `9–14 s`). `S02` replaces anachronistic Niagara stamp with `TESLA PATENT · 1888`, clear of `9.0–14.0 s` title row (nudge start `6.0→6.4 s`). Full `OPEN/LENGTH/LOOP` gate awaits rendered cuts. |
| **Teach / Polish / Craft** | **RESOLVED** *(with `FIX-2` card fix)* | `6 DATA` + `6 SCALE` (all quantitative, all spoken except `DATA` #6 voltage polish), `7 WHO` (Kemmler added; all roles `≤4w`), `14 WHEN` (`1886/1888` aligned; `Turin, 11 March 1888` fixed in `FIX-2`), `4 FACT` (all `≤4w`), `9 LABEL` (all `≤4w`), `2 Explorer` beats outside first minute, `5` chapter cards aligned to `LAUNCH_PLAN.md`, `6 TEACH`, Trinity handoff verified verbatim on US DOE OSTI, zero Topsy myth. Media-stage Polish checks remain unverified until media exists. |
| **Packaging & Mechanical Gates** | **BLOCKED → `FIX-5`, `FIX-6`** | Working Title Arm A (*Why Do We Use AC Instead of DC? (Edison vs Tesla)*, `49 chars`, `0` collisions) retained as working title only. Blocked by **`FIX-5`** (Arm B omitted from `public_search.json`) and **`FIX-6`** (duplicate `_master_` filename breaks default `gate:episode`). |

---

## 4. Direct Exact-Quote Verification Log (All MUST QUOTE Sources Opened `2026-11-25`)

- **Rutgers Edison Papers (`200 OK`):**
  - `1882` chronology: `"Jan 12 Edison's central station on Holborn Viaduct in London begins operation."` · `"Sep 4 Opens the Pearl Street central station in the Wall Street district of New York."` — **MATCH**
  - `1888` chronology (primary upgrade): `"Conducts electrocution experiments upon dogs and other animals with Arthur E. Kennelly and Harold P. Brown."` — **MATCH**
  - `1892` chronology: `"Apr 15 The General Electric Company is organized."` — **MATCH**
  - Biography (primary upgrade): `"By the time of his death on October 18, 1931"` — **MATCH**
- **NPS Edison NHP (`200 OK`):** `"Thomas Alva Edison was born on February 11, 1847 in Milan, Ohio"` — **MATCH** (**confirms `FIX-1`**: age 34 on 12 Jan 1882)
- **IEEE ETHW (`200 OK` across all 7 pages):**
  - `Milestones:Pearl_Street_Station,_1882`: Holborn Viaduct Jan 1882, `257 Pearl Street`, `0.25 sq mi`, `"on the afternoon of 4 September 1882"`, `~85` customers, `~400` lamps, `110 V dc`, six `100 kW` dynamos driven by steam engines supplied by four coal-fired boilers, `~80,000 ft` twin half-moon copper conductors, costliest component — **ALL MATCH**
  - `Milestones:Alternating_Current_Electrification,_1886`: Gaulard & Gibbs, `20 March 1886`, Great Barrington old rubber mill, `500 V → 3,000 V` (30 series 100 V lamps) `→ 500 V`, elm trees, `6` basement step-down transformers to `100 V`, `20` business establishments — **ALL MATCH**
  - `William_Stanley`: `>1 mile` resistance/voltage-drop quote & `14 May 1916` death — **MATCH**; `"28 November 1858"` — **MISS (`FIX-3`)**, live text reads `"William Stanley was born in Brooklyn, New York, 22 November 1858"` — **MATCH**
  - `Westinghouse_Electric_Corporation` & `George_Westinghouse`: `6 Oct 1846` birth, `1868/1872` air brake, `1914/03/12` death (primary upgrade), `"sent power 20 miles away to Buffalo"` (variance logged) — **ALL MATCH**
  - `Nikola_Tesla`: `1856/07/10` birth, Croatia, `1884` New York/Edison — **MATCH**
  - `AC_vs._DC`: 1886 Sprague report — **MATCH**
  - `Milestones:Adams_Hydroelectric_Generating_Plant,_1895`: `"When the Adams Plant went into operation on August 26, 1895..."` — **MATCH**
- **USPTO via Google Patents `US381968A` (`200 OK`):** `"Electro-magnetic motor"`, `1888-05-01` — **MATCH**
- **Scanned NPS NRIS `75001212` PDF (`200 OK`, 14 pages visually inspected):**
  - PDF p. 5 (Item 7 p. 1) & p. 11 (Item 8 p. 5): `"August 26, 1895"` local delivery to Pittsburgh Reduction Company — **MATCH**
  - PDF p. 10 (Item 8 p. 4): August 1891 Oerlikon >100-mile polyphase demo, 1893 Chicago showcase, `"October 27, 1893"` contract for ten `5,000-hp` polyphase AC generators — **MATCH**
  - PDF p. 11 (Item 8 p. 5): `"On November 15, 1896, the Niagara station began long-distance transmission to Buffalo, N.Y., 22 miles away."` — **MATCH**
- **US DOE (`200 OK`):** `war-currents-ac-vs-dc-power` (DC royalties, `$554,000` GE vs `$399,000` Westinghouse, `Nov. 16, 1896`, GE adopted AC, modern DC & HVDC) & `electricity-101` (`110-120V (60 Hz)`, `220-240V (50 Hz)`) — **ALL MATCH**
- **US EIA (`200 OK`):** `930-content/about.html` (`60 cycles per second (hertz)`) & `delivery-to-consumers.php` (high-voltage transmission lines & step-up/step-down substation transformers) — **ALL MATCH**
- **UK Legislation SI 2002/2665 Reg. 27 (`200 OK`, primary upgrade):** `"50 hertz"` & `"230 volts"` — **MATCH**
- **Library of Congress Chronicling America (`200 OK`, primary upgrade):** `"August 6, 1890 Murderer William Kemmler is the first to be electrocuted; second shock is needed when he returned to consciousness after the initial shock."` — **MATCH**
- **US DOE OSTI (`200 OK`):** `trinity_safety.htm` (`"discussed the possibility that the atmosphere itself might be ignited..."`) — **MATCH**
- **Secondary (Wikipedia, `200 OK`) & Italian Ferraris Records:**
  - `Alternating_current`, `War_of_the_currents`, `Nikola_Tesla`, `Harold_P._Brown`, `William_Kemmler`, `World's_Columbian_Exposition`, `High-voltage_direct_current` — **MATCH**
  - `Induction_motor`: `FACT_NOTES_v02.md` Row 10 quoted string — **MISS (`FIX-4`)**; Thompson `"no commutator or connection of any kind with the armature was required"` & `"In April 1888, the Royal Academy of Science of Turin published Ferraris's research"` — **MATCH**
  - `Galileo_Ferraris` (`it.wikipedia.org` + *Accademia delle Scienze di Torino* / *MuseoTorino* / *Treccani*): **`18 marzo 1888`** presentation, **April 1888** publication — **MATCH (`FIX-2`)**

---

## 5. Fresh Local Mechanical Gate Outputs (Not Production Approval)

```text
npm run review:script -- --file ../.../edison_tesla_ac_dc_script_master_v02.md
Decision: PASS · Score: 92.3 / 100
Words: 1314 · Est. min: 8.8 · Chapters: 5 · Structure gates 8/8

npm run gate:episode -- --project ../...  (WITHOUT --script — PROVES FIX-6)
script_file: OK | Script: 01_Script/edison_tesla_ac_dc_script_master_v01.md  <-- PICKED SUPERSEDED v01!
Script score: 92/100 · PASS

npm run gate:episode -- --project ../... --script ../.../edison_tesla_ac_dc_script_master_v02.md
Decision: PASS — VO / Gemini Veo allowed
script_file: OK | Script: 01_Script/edison_tesla_ac_dc_script_master_v02.md
script_review: PASS 92.3/90 | explorer_acts: 2 | visual_must: 41 | teach: 6 | chapters: 5

bash 00_Brand/Channel-Setup/tools/check_all.sh 02_Video-Projects/128_Edison-Tesla-Westinghouse-Why-Do-We-Use-AC-Instead-Of-DC
ALL CHECKS PASS
```

---

## 6. Next Actions Queued by Acting Chief (`gemini`)

1. **Follow-up `script` job (`v03`):** Apply `FIX-1` through `FIX-6` + the 3 minor alignment polishes cleanly from PR `#760` (`6f0ff4a3`), run `public_search.py` on Candidate Arm B, verify `review:script` ≥ 90 and **default** `gate:episode` (no `--script`) PASS on exact `edison_tesla_ac_dc_script_master_v03.md`, and open the `v03` PR. Zero VO or picture spend.
2. **Follow-up `review` job (`v03` lock, `--after` `v03` script job):** Verify exact `v03` hashes/diffs against `FIX-1`..`FIX-6` and default `gate:episode`; on complete `KEEP`, elected Chief merges the `v03` PR, closes original `J3547`, and queues long + Shorts VO under normal credit rules.
