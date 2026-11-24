# Pre-Build Search & Neighbour Audit — `128_Edison-Tesla-Westinghouse-Why-Do-We-Use-AC-Instead-Of-DC` (`HOS:128`)

> **STATUS (`J3496`, `2026-11-24`):** Ben approved `hos-search-2027-01` on 24 Nov 2026 and brought `HOS:128` into active production (OWB PR `#1238`, target air **Thu 10 Dec 2026 18:00 London**, slides to Thu 17 Dec if not ready for Ben's watch by Mon 7 Dec). Rule-E topic review passed (`J3346`, `GO 97.1 / 100`). Package-first scoring (`PACKAGE_FIRST_SCORING_v01.md`), script draft v01 (`edison_tesla_ac_dc_script_master_v01.md`), `FACT_NOTES_v01.md` (`21 OK · 0 PARTIAL · 0 FLAG`), `SOURCES.md`, and `10_Shorts/SHORTS_SCRIPTS_v01.md` (`16–19 s`) are complete and awaiting HOS script review + Chief lock. Zero VO or picture spend.

## 1. The Discovery Story (Person, Date & Twist — Verified in `FACT_NOTES_v01.md`)

- **Familiar phenomenon:** Every wall socket delivers alternating current (AC) reversing 50 or 60 times per second, even though batteries and microchips run on direct current (DC).
- **Person, place & date:**
  - **Thomas Edison** (Pearl Street Station, Lower Manhattan, **4 September 1882**): launched the first central commercial DC power plant at `110 V` (`400` lamps, `82` customers), but resistive heating losses ($P_{\text{loss}} = I^2 R$) limited economic reach to under a mile.
  - **Zipernowsky, Bláthy & Déri** (Budapest, **May 1885**, building on Gaulard & Gibbs 1882–1884) and **William Stanley Jr. & George Westinghouse** (**20 March 1886**, Great Barrington, Massachusetts): closed-core parallel AC transformers stepped `500 V` up to `3,000 V` over `4,000 feet` and back down to `100 V` for 20 shops.
  - **Nikola Tesla** (**1 May 1888** polyphase induction motor US Patent `381,968`, licensed by Westinghouse **July 1888**, parallel with **Galileo Ferraris** March 1888), **Chicago World's Fair** (**May 1893**, Westinghouse `$399,000` vs GE `$554,000`, custom stopper lamps), and **Niagara Falls Adams Power Plant** (`25 August 1895` local; **15–16 November 1896**, `11,000 V` AC transmitted `~22 miles` to Buffalo): won the War of the Currents and wired the modern grid — with the modern twist that solid-state electronics have brought HVDC back for ultra-long undersea cables.

---

## 2. Search-First Demand Check (`LEARNINGS.md` Rule 26 & `J3224` Cluster 1, Retrieved `2026-11-22`)

- **J3224 vidIQ Anglosphere Demand (`05_Analytics/hos/search_research/2026-11-20.md`, £0 extra spend):** `nikola tesla documentary` `29,205`/mo (comp `37`), `thomas edison` `28,672`/mo (**US 30%**), `thomas edison vs nikola tesla` `4,071`/mo (comp `44`), **9/10 US SERP gap**, small-channel proof `Business History Podcast` (`5.9K` US → `92.9K` `48×`), `Real-World Learning` (`36.8K` US → `13.2K` `8.5×`), `RELIQUARY ARCHIVES` (`29` subs → `2.1K` `13×`).
- **Exact signed-out YouTube autocomplete phrases (`autocomplete = yes`, `2026-11-22`):** `"why do we use ac instead of dc"`, `"thomas edison vs nikola tesla"`, `"war of the currents"`, `"ac vs dc"`, `"who invented alternating current"`.
  - **Ranking Video 1:** `S7C5sSde9e4` — *Why Use AC Instead of DC at Home??* (`ElectroBOOM`, **`6,686,558` views**)
  - **Ranking Video 2:** `vN9aR2wKv0U` — *Difference between AC and DC Current Explained | AddOhms #5* (`AddOhms`, **`3,067,900` views**; plus `Discovery UK` `pcrwTN5OEZY` **`1,603,939`**, `Arvin Ash` `ag6ltdwqfms` **`1,472,705`**, `pharmacist` `Cidg4Xfpjmc` **`1,100,111`**)
- **Primary title picked (`PACKAGE_FIRST_SCORING_v01.md`):** `Why Do We Use AC Instead of DC? (Edison vs Tesla)` (`49 chars ≤ 50`, `0` exact collisions)
- **Description first 100 chars:** `Why do we use AC instead of DC? Edison's 1882 copper wires lost heat past a mile—until AC won.`

---

## 2b. Neighbour Pass (Blocking · `STUDIO_PLAYBOOK.md` §2 Step 4, Retrieved `2026-11-22`)

Saved in [`evidence_2026-11-22_neighbours.json`](evidence_2026-11-22_neighbours.json) and [`evidence_2026-11-22_public_search.json`](evidence_2026-11-22_public_search.json):

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

## 3. Title ABC (`PACKAGE_FIRST_SCORING_v01.md`)

| | Title | Chars | Collisions (`2026-11-22`) | Role & Notes | Keep? |
|---|-------|------:|-----------:|--------------|-------|
| A | `Why Do We Use AC Instead of DC? (Edison vs Tesla)` | 49 | 0 | **Main (`95/100`):** Exact autocomplete question first, `≤50 chars` zero clip, iconic rivalry tail | **Keep (Primary Arm A)** |
| B | `Thomas Edison vs Nikola Tesla: How AC Won the War of Currents` | 61 | 0 | **T&C Arm B (`93/100`, Plan Title):** Exact US rivalry query + `war of the currents` | **Keep (T&C Arm B)** |
| C | `Thomas Edison vs Nikola Tesla: Why AC Won the War of Currents` | 61 | 0 | **T&C Arm C (`91/100`, J3346 Alt):** Curiosity-led `Why` variant on exact rivalry query | **Keep (T&C Arm C)** |
| Reject | `Polyphase Alternating Current Transmission History \| HOS` | 57 | — | Textbook catalogue label + forbidden series suffix | **Reject** |

---

## 3b. Script Reviewer & Sign-Off (Draft v01 Ready for Chief Lock)

- [x] Keywords checked (`J3224` vidIQ Anglosphere research + `evidence_2026-11-22_public_search.json` + `evidence_2026-11-22_neighbours.json`)
- [x] Title ABC & 2 thumbnail ideas scored vs Cluster 1 outliers (`PACKAGE_FIRST_SCORING_v01.md`)
- [x] Script reviewer PASS ≥ **90 / 100** (`npm run review:script` on `01_Script/edison_tesla_ac_dc_script_master_v01.md`)
- [x] `FACT_NOTES_v01.md` (`21 OK`) + `SOURCES.md` prepared for independent `facts`/Chief script lock review
- [ ] Chief script lock PASS (required before any VO or picture spend)

**Signed off by:** Gemini (J3496 draft package & script v01 — awaiting HOS script review / Chief lock)  
**Date:** `2026-11-24`
