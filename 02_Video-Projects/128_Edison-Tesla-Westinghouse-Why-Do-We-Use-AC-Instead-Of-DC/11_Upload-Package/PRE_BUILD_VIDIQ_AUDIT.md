# Pre-Build Search & Neighbour Audit — `128_Edison-Tesla-Westinghouse-Why-Do-We-Use-AC-Instead-Of-DC` (`HOS:128`)

> **STATUS (`J3659`, `2026-11-25`):** Ben approved `hos-search-2027-01` on 24 Nov 2026 and brought `HOS:128` into active production (OWB PR `#1238`, target air **Thu 10 Dec 2026 18:00 London**, slides to Thu 17 Dec if not ready for Ben's watch by Mon 7 Dec). Rule-E topic review passed (`J3346`, `GO 97.1 / 100`). Following Acting Chief ruling `J3630` (**FIX**, HOS PR `#761`) and independent `J3629` verification (HOS PR `#760`), `J3659` delivered clean `v03` (`edison_tesla_ac_dc_script_master_v03.md` as the sole `master` script, `FACT_NOTES_v03.md`, `SOURCES.md`, `10_Shorts/SHORTS_SCRIPTS_v03.md`, `PACKAGE_FIRST_SCORING_v03.md`, `evidence_2026-11-25_public_search_arm_b.json`, and `LAUNCH_PLAN.md`). Working title and unrendered thumbnail drafts retained (NOT rendered packaging PASS). Awaits `J3660` verification and Chief script lock. Zero VO or picture spend.

## 1. The Discovery Story (Person, Date & Twist — Verified Notes in `FACT_NOTES_v03.md`, Pending `J3660` Lock)

- **Familiar phenomenon:** Every wall socket delivers alternating current (AC) completing 50 full cycles per second in Britain/Europe or 60 full cycles per second in North America (reversing direction twice per cycle), even though batteries and microchips run on direct current (DC).
- **Person, place & date:**
  - **Thomas Edison** (Pearl Street Station, `257 Pearl Street`, Lower Manhattan, afternoon of **4 September 1882**, following his `12 January 1882` Holborn Viaduct central station in London when aged 34): launched his full-scale American central DC station at `110 V` (`~400` lamps, `~85` customers, `0.25 sq mi` First District, `~80,000 ft` underground copper conductors), where low-voltage resistance losses ($P_{\text{loss}} = I^2 R$) and copper costs made long-distance distribution uneconomical.
  - **Zipernowsky, Bláthy & Déri** (Ganz Works, Budapest, **1885**, building on Gaulard & Gibbs) and **William Stanley Jr. & George Westinghouse** (**20 March 1886**, Great Barrington, Massachusetts): closed-core parallel AC transformers demonstrated `500 V → 3,000 V → 500 V` step-up/step-down (30 series lamps) and `500 V` Main Street distribution via `6` basement transformers to `100 V` for `20` businesses.
  - **Nikola Tesla** (**1 May 1888** polyphase induction motor U.S. Patent `381,968`, licensed by Westinghouse **July 1888**, parallel with **Galileo Ferraris** **`18 March 1888`** Turin Royal Academy of Sciences presentation, published **April 1888**), **Chicago World's Fair** (**May 1893**, Westinghouse `$399,000` vs GE `$554,000`, `93,000` planned incandescent lamps, custom stopper lamps), and **Niagara Falls Adams Power Plant** (`27 October 1893` contract; **`26 August 1895`** local start; **`15 November 1896`** long-distance AC transmission `22 miles` to Buffalo per NPS NRIS `75001212` — accepted by Acting Chief `J3630` with ETHW `20 miles` / US DOE `Nov. 16` variance logged): wired the modern grid — with the modern twist that solid-state converters brought HVDC back for ultra-long undersea cables.

---

## 2. Search-First Demand Check (`LEARNINGS.md` Rule 26 & `J3224` Cluster 1, Dated Research `2026-11-20` & `2026-11-22`)

- **J3224 vidIQ Anglosphere Demand (`05_Analytics/hos/search_research/2026-11-20.md`, £0 extra spend):** `nikola tesla documentary` `29,205`/mo (comp `37`), `thomas edison` `28,672`/mo (**US 30%**), `thomas edison vs nikola tesla` `4,071`/mo (comp `44`), **9/10 US SERP gap**, small-channel proof `Business History Podcast` (`5.9K` US → `92.9K` `48×`), `Real-World Learning` (`36.8K` US → `13.2K` `8.5×`), `RELIQUARY ARCHIVES` (`29` subs → `2.1K` `13×`).
- **Exact signed-out YouTube autocomplete phrases (`autocomplete = yes`, `2026-11-22`):** `"why do we use ac instead of dc"`, `"thomas edison vs nikola tesla"`, `"war of the currents"`, `"ac vs dc"`, `"who invented alternating current"`.
  - **Ranking Video 1:** `S7C5sSde9e4` — *Why Use AC Instead of DC at Home??* (`ElectroBOOM`, **`6,686,558` views**)
  - **Ranking Video 2:** `vN9aR2wKv0U` — *Difference between AC and DC Current Explained | AddOhms #5* (`AddOhms`, **`3,067,900` views**; plus `Discovery UK` `pcrwTN5OEZY` **`1,603,939`**, `Arvin Ash` `ag6ltdwqfms` **`1,472,705`**, `pharmacist` `Cidg4Xfpjmc` **`1,100,111`**)
- **Working main title retained (`PACKAGE_FIRST_SCORING_v03.md`, not final packaging PASS):** `Why Do We Use AC Instead of DC? (Edison vs Tesla)` (`49 chars`, `0` exact collisions on `2026-11-22`)
- **Description first 100 chars (v03):** `Why do we use AC instead of DC? Edison's 1882 low-voltage DC needed costly copper over distance.`

---

## 2b. Neighbour Pass (Blocking · `STUDIO_PLAYBOOK.md` §2 Step 4, Retrieved `2026-11-22`)

Saved in [`evidence_2026-11-22_neighbours.json`](evidence_2026-11-22_neighbours.json), [`evidence_2026-11-22_public_search.json`](evidence_2026-11-22_public_search.json), and [`evidence_2026-11-25_public_search_arm_b.json`](evidence_2026-11-25_public_search_arm_b.json):

| # | Views (`2026-11-22`) | Channel (internal) | id & URL | Title | Subject words we reuse |
|---:|------:|--------------------|----------|-------|------------------------|
| 1 | `28,293,671` | Veritasium (`neighbours.py`) | [`bHIhgxav9LY`](https://youtu.be/bHIhgxav9LY) | *The Biggest Misconception About Electricity* | `electricity`, `current`, `wires`, `power` |
| 2 | `12,838,937` | Veritasium (`neighbours.py`) | [`oI_X2cMHNe0`](https://youtu.be/oI_X2cMHNe0) | *How Electricity Actually Works* | `how electricity works`, `circuit`, `voltage` |
| 3 | `3,624,109` | TED-Ed ★ (`neighbours.py`) | [`yc2-363MIQs`](https://youtu.be/yc2-363MIQs) | *The science of static electricity - Anuradha Bhagwat* | `electricity`, `electric charge` |
| 4 | `1,967,879` | Thoughty2 (`neighbours.py`) | [`egCsQXuBGkQ`](https://youtu.be/egCsQXuBGkQ) | *Why This Secret Invention Drove Tesla Insane* | `Nikola Tesla`, `invention`, `alternating current` |
| 5 | `1,401,838` | SciShow (`neighbours.py`) | [`pPnGvjmIgZA`](https://youtu.be/pPnGvjmIgZA) | *The Incredible Inventions of Nikola Tesla: Great Minds of Science* | `Nikola Tesla`, `AC`, `induction motor` |
| 6 | `1,041,472` | TED-Ed ★ (`neighbours.py`) | [`0SMNYivhGsc`](https://youtu.be/0SMNYivhGsc) | *How inventions change history (for better and for worse)* | `inventions`, `Thomas Edison`, `history` |
| 7 | `567,471` | CrashCourse (`neighbours.py`) | [`JoscDcbAjbY`](https://youtu.be/JoscDcbAjbY) | *Electricity: Crash Course History of Science #27* | `history of electricity`, `AC vs DC` |
| 8 | `346,459` | TED ★ (`neighbours.py`) | [`V-WkUKP1l3c`](https://youtu.be/V-WkUKP1l3c) | *Marco Tempest: The electric rise and fall of Nikola Tesla* | `Nikola Tesla`, `alternating current` |
| 9 | `100,111` | FuseSchool (`neighbours.py`) | [`tJSga2YamDc`](https://youtu.be/tJSga2YamDc) | *Alternating and Direct Current \| Electricity \| Physics* | `alternating current`, `direct current`, `AC vs DC` |

**Proposed subject-only tags (8 tags, zero channel names):**
`why do we use ac instead of dc, thomas edison vs nikola tesla, war of the currents, alternating current vs direct current, nikola tesla induction motor, george westinghouse transformer, niagara falls ac power, history of electricity`

---

## 3. Title Candidates (`PACKAGE_FIRST_SCORING_v03.md` — Working Scores Only, Not Final PASS)

| | Title | Chars | Collisions (Dated Check) | Role & Notes | Keep? |
|---|-------|------:|-----------|--------------|-------|
| A | `Why Do We Use AC Instead of DC? (Edison vs Tesla)` | 49 | `0` (`2026-11-22`) | **Working Title (`94/100` draft):** Exact autocomplete question first, rivalry tail | **Retain (Working Arm A)** |
| B | `Thomas Edison vs Nikola Tesla: How AC Won the War of Currents` | 61 | `0` (`2026-11-25`, `evidence_2026-11-25_public_search_arm_b.json`) | **Candidate T&C Arm B (`92/100` draft, Plan Title):** Named US rivalry query | **Candidate (T&C Arm B)** |
| C | `Thomas Edison vs Nikola Tesla: Why AC Won the War of Currents` | 61 | `0` (`2026-11-22`) | **Candidate T&C Arm C (`90/100` draft, J3346 Alt):** Curiosity-led `Why` variant | **Candidate (T&C Arm C)** |
| Reject | `Polyphase Alternating Current Transmission History \| HOS` | 57 | — | Textbook catalogue label + forbidden series suffix | **Reject** |

---

## 3b. Script Reviewer & Sign-Off (Draft v03 — Pending `J3660` Verification & Chief Lock)

- [x] Keywords & collisions checked (`J3224` vidIQ Anglosphere research + `evidence_2026-11-22_public_search.json` + `evidence_2026-11-25_public_search_arm_b.json` + `evidence_2026-11-22_neighbours.json`)
- [x] Title ABC & unrendered thumbnail concepts scored as working drafts (`PACKAGE_FIRST_SCORING_v03.md`; Thumb A `WASTED AS HEAT`, Thumb C `HIGH VOLTAGE`, optional Thumb B `22 MILES AWAY` — unrendered drafts only, NOT rendered packaging PASS; later rendered thumbs require independent panel, `style_sheet.py`, and `168×94` review)
- [x] Script reviewer PASS ≥ **90 / 100** (`npm run review:script` on `01_Script/edison_tesla_ac_dc_script_master_v03.md`; sole `master` file so default `gate:episode` picks `v03` and PASSes)
- [x] Independent Gemini `facts` pass (`J3629`) & direct-quote check (`J3630`) findings folded into `v03` (`FACT_NOTES_v03.md` + `SOURCES.md`)
- [ ] `J3660` verification of exact `v03` hashes & Chief script lock PASS (required before any VO or picture spend)

**Signed off by:** gemini (J3659 draft v03 pre-build audit — awaiting J3660 verification and Chief lock)
**Date:** `2026-11-25`
