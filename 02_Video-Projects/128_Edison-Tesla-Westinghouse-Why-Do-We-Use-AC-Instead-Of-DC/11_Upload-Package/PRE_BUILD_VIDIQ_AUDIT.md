# Pre-Build Search & Neighbour Audit — `128_Edison-Tesla-Westinghouse-Why-Do-We-Use-AC-Instead-Of-DC` (`HOS:128` — Proposal in `next_hos`)

> **PROPOSAL & UNVERIFIED CLAIMS GUARD (`J3270`, `2026-11-22`):** Appended to `jobs/WIP.json` `next_hos` under **Rule G** (`4 / 4` active HOS slots full) and queued for **Rule-E topic go/no-go review**. All historical and scientific claims below are **UNVERIFIED** working notes and must be sourced in `SOURCES.md` and verified through the `facts` lane (`gemini-agy`) before any script lock, VO, or picture spend.

## 1. The Discovery Story (Person, Date & Twist — UNVERIFIED)

- **Familiar phenomenon:** Every wall outlet in your house delivers alternating current (AC) reversing direction 100 or 120 times per second, even though batteries and electronics run on direct current (DC).
- **Person, place & date:**
  - **Thomas Edison** (Pearl Street Station, Lower Manhattan, **4 September 1882**): launched the first central commercial DC power plant at 110 V, but resistive heating losses ($P = I^2 R$) meant DC could barely supply customers a mile away without prohibitively thick copper cables.
  - **Lucien Gaulard, John Dixon Gibbs, Otto Bláthy / Miksa Déri / Károly Zipernowsky, and William Stanley** (**1885–20 March 1886**, Great Barrington, Massachusetts): perfected closed-core AC transformers that stepped voltage up for efficient long-distance transmission and stepped it back down safely for indoor lighting — backed by **George Westinghouse**.
  - **Nikola Tesla** (New York / Pittsburgh, **May 1888** polyphase AC induction motor patents; **May 1893** Chicago World's Columbian Exposition; **1895–16 November 1896** Niagara Falls Adams Power Plant transmitting AC ~26 miles to Buffalo): supplied the missing brushless AC motor that let alternating current power factories as well as lights, winning the War of the Currents and wiring the modern world.

---

## 2. Search-First Demand Check (`LEARNINGS.md` Rule 26 & `J3224` Cluster 1, Retrieved `2026-11-22`)

- **J3224 vidIQ Anglosphere Demand (`05_Analytics/hos/search_research/2026-11-20.md`, £0 extra spend here):** `nikola tesla documentary` `29,205`/mo (comp `37`), `thomas edison` `28,672`/mo (**US 30%**), `thomas edison vs nikola tesla` `4,071`/mo (comp `44`), **9/10 US SERP gap**, small-channel proof `Business History Podcast` (`5.9K` US → `92.9K` `48×`), `Real-World Learning` (`36.8K` US → `13.2K` `8.5×`), `RELIQUARY ARCHIVES` (`29` subs → `2.1K` `13×`).
- **Exact signed-out YouTube autocomplete phrases (`autocomplete = yes`, `2026-11-22`):** `"why do we use ac instead of dc"`, `"thomas edison vs nikola tesla"`, `"war of the currents"`, `"ac vs dc"`, `"who invented alternating current"`.
  - **Ranking Video 1:** `S7C5sSde9e4` — *Why Use AC Instead of DC at Home??* (`ElectroBOOM`, **`6,686,558` views**)
  - **Ranking Video 2:** `vN9aR2wKv0U` — *Difference between AC and DC Current Explained | AddOhms #5* (`AddOhms`, **`3,067,900` views**; plus `Discovery UK` `pcrwTN5OEZY` **`1,603,939`**, `Arvin Ash` `ag6ltdwqfms` **`1,472,705`**, `pharmacist` `Cidg4Xfpjmc` **`1,100,111`**)
- **Candidate primary title:** `Why Do We Use AC Instead of DC? (Edison vs Tesla)` (`49 chars ≤ 50`, `0` exact collisions)
- **Candidate description first 100 chars (unverified until `SOURCES.md`):** `Why do we use AC instead of DC? Edison's 1882 copper wires failed past a mile—until Tesla's AC won.`

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

## 3. Title ABC (Score Before VO)

| | Title | Chars | Collisions (`2026-11-22`) | Role & Notes | Keep? |
|---|-------|------:|-----------:|--------------|-------|
| A | `Why Do We Use AC Instead of DC? (Edison vs Tesla)` | 49 | 0 | **Main (`Rules 1, 15, 23, 26`):** Starts verbatim with exact autocomplete question, fits `≤50 chars`, names the iconic rivalry | **Keep (Primary Proposal)** |
| B | `Thomas Edison vs Nikola Tesla: Why AC Won the War of Currents` | 61 | 0 | **T&C Arm 2 (`J3224` Cluster 1 Lead Shape):** Exact `"thomas edison vs nikola tesla"` + `"war of the currents"` Anglosphere queries | **Keep (T&C Arm 2)** |
| C | `Why Do We Use AC Instead of DC? (The 1888 Transformer Bet)` | 58 | 0 | **T&C Arm 3 (`Rule 26`):** Exact search question + concrete apparatus twist (`1888 Transformer`) | **Keep (T&C Arm 3)** |
| Reject | `Polyphase Alternating Current Transmission History \| HOS` | 57 | — | Textbook catalogue label + forbidden series suffix | **Reject** |

---

## 3b. Script Reviewer (Blocking Before VO — Not Run; Proposal Only)

- [ ] Rule-E topic go/no-go review PASS
- [ ] `SOURCES.md` exact quotes + `facts` lane verification completed (required before script lock)
- [ ] Score ≥ **90 / 100** (`npm run review:script`)
