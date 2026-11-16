# Pre-Build Search & Neighbour Audit — `111_Roston-Unger-Kawchuk-Why-Do-Knuckles-Crack` (`HOS:111`)

> **RULE-E GO/NO-GO & VERIFICATION STATUS (`J2922` / `J2925`, `2026-11-16`):**
> - This file records the pre-build search and neighbour evidence from `00_Brand/Channel-Setup/tools/public_search.py` and `00_Brand/Channel-Setup/tools/neighbours.py` (`£0` spend), verified and expanded in `J2925` (**Rule-E GO: `95 / 100` · `9.50 / 10` Opportunity Score**).
> - **Rule G (`jobs/WIP.json` `next_hos`):** This film remains in the `next_hos` waiting line (`4 / 4` active HOS slots full). All historical and scientific claims below are **UNVERIFIED** until `SOURCES.md` exact quotes and the `facts` lane (`gemini-agy`) run when an active HOS WIP slot opens.

---

## 1. Search Demand & Autocomplete (`public_search.py` · `LEARNINGS.md` Rule 26)

- **Exact Search Phrase (`Rule 26a`):** `"why do knuckles crack"` (`signed-out YouTube GB autocomplete = yes`)
  - Autocomplete suggestions (`2026-11-16`, `10` hits): `why do knuckles crack`, `why does cracking knuckles feel good`, `why is cracking knuckles bad`, `why does your knuckles crack`, `why do we crack knuckles`, `why do your knuckles pop`, `why do my knuckles pop`, `why do my knuckles not crack`, `why do you crack your knuckles`
  - Additional verified autocomplete phrases (`2026-11-16`):
    - `"does cracking knuckles cause arthritis"` (`autocomplete = yes`)
    - `"why do your knuckles pop"` (`autocomplete = yes`, `9` suggestions: `why do your knuckles pop`, `why do your joints pop`, `why do my knuckles pop`, `why does your knuckles crack`, `why do my joints pop`, `why do our knuckles crack`, `why do my knuckles crack`, `dr binocs why do your knuckles pop`, `why do my knuckles not crack`)
    - `"why do joints pop"`, `"synovial joints"`, & `"skeletal system bones joints"` (`autocomplete = yes` in `evidence_2026-11-16_neighbours.json`)
- **Rule 26(a) Two Ranking Videos (`2026-11-16`):**
  - **Phrase:** `"why do knuckles crack"` / `"why do your knuckles pop"`
  - **Ranking Video 1:** `n3IYmdy6d4Y` — *Here's what happens to your knuckles when you crack them* (`Vox`, **`67,776,939` views**, retrieved `2026-11-16`)
  - **Ranking Video 2:** `IjiKUmfaZr4` — *Why do your knuckles pop? - Eleanor Nelsen* (`TED-Ed`, **`5,783,001` views**, retrieved `2026-11-16`; plus `Doctor Mike` `PAKaVmcOPBY` **`6,910,969` views**, `Doctor Myro` `YNbzxNmxn90` **`5,308,015` views**, `Matthew Harb, M.D` `B3uL39b-9wo` **`4,850,525` views**, `The Iced Coffee Hour` `sAg07qAM7Xc` **`4,452,046` views**, `RehabMedicineUofA` `BHEcQluSzmM` **`2,187,642` views**, `Institute of Human Anatomy` `j43kNmg2x2U` **`1,814,225` views**, and `Peekaboo Kidz` `ccLQYDVJB0A` **`1,253,656` views**)
- **Decision:** Candidate primary title = `Why Do Knuckles Crack? (The 50-Year Self-Experiment)` (Title A, `52 chars`, `0` exact collisions; `50-char` tightened option `Why Do Knuckles Crack? (A 50-Year Self-Experiment)`) / `Why Do Knuckles Crack? How an MRI Reversed a 44-Year Myth` (Title C, `57 chars`, exact phrase first)
- **Candidate description first 100 chars (unverified until `SOURCES.md` check):** `Why do knuckles crack when you pull them, and how did a 2015 MRI reverse a 44-year textbook myth?` (`97 chars`)

---

## 2b. Neighbour pass (blocking · `STUDIO_PLAYBOOK.md` §2 Step 4, Retrieved `2026-11-16`)

Saved in [`evidence_2026-11-16_neighbours.json`](evidence_2026-11-16_neighbours.json) (`bigCount = 6` strictly on-topic education videos `≥1M` views, `hasTed = true`, `gate = PASS`, `0` off-topic rows) and [`evidence_2026-11-16_public_search.json`](evidence_2026-11-16_public_search.json) (`8` queries, `48` search results):

| # | Views (`2026-11-16`) | Channel (internal) | id & URL | Title | Subject words we reuse |
|---:|------:|--------------------|----------|-------|------------------------|
| 1 | `67,776,939` | Vox (`public_search.py`) | [`n3IYmdy6d4Y`](https://youtu.be/n3IYmdy6d4Y) | *Here's what happens to your knuckles when you crack them* | `why do knuckles crack`, `knuckles`, `synovial fluid`, `mri`, `cavity` |
| 2 | `6,910,969` | Doctor Mike (`public_search.py`) | [`PAKaVmcOPBY`](https://youtu.be/PAKaVmcOPBY) | *The Truth About Cracking Your Knuckles \| Responding to Comments #15* | `cracking knuckles`, `arthritis`, `joints` |
| 3 | `6,877,432` | CrashCourse (`neighbours.py` Tier 2) | [`rDGqkMHPDqE`](https://youtu.be/rDGqkMHPDqE) | *The Skeletal System: Crash Course Anatomy & Physiology #19* | `skeletal system`, `bones`, `joints`, `anatomy` |
| 4 | `5,783,001` | TED-Ed ★ (`neighbours.py` Tier 1) | [`IjiKUmfaZr4`](https://youtu.be/IjiKUmfaZr4) | *Why do your knuckles pop? - Eleanor Nelsen* | `knuckles pop`, `synovial fluid`, `gas bubbles`, `donald unger`, `arthritis` |
| 5 | `4,388,768` | CrashCourse (`neighbours.py` Tier 2) | [`DLxYDoN634c`](https://youtu.be/DLxYDoN634c) | *Joints: Crash Course Anatomy & Physiology #20* | `joints`, `synovial joints`, `cartilage`, `anatomy` |
| 6 | `3,268,946` | TED-Ed ★ (`neighbours.py` Tier 1) | [`VVL-8zr2hk4`](https://youtu.be/VVL-8zr2hk4) | *How your muscular system works - Emma Bryce* | `bones`, `joints`, `movement`, `physiology` |
| 7 | `2,187,642` | RehabMedicineUofA (`public_search.py`) | [`BHEcQluSzmM`](https://youtu.be/BHEcQluSzmM) | *Pull my finger: Why joints crack* | `joints crack`, `greg kawchuk`, `mri`, `tribonucleation` |
| 8 | `1,814,225` | Institute of Human Anatomy (`public_search.py`) | [`j43kNmg2x2U`](https://youtu.be/j43kNmg2x2U) | *How Harmful Is It to "Pop" Your Knuckles?* | `pop your knuckles`, `synovial capsule`, `cavitation` |
| 9 | `1,734,355` | Amoeba Sisters (`neighbours.py` Tier 2) | [`m26gr04HIVE`](https://youtu.be/m26gr04HIVE) | *Skeletal System* | `skeletal system`, `bones`, `joints`, `cartilage` |
| 10 | `1,192,035` | SciShow (`neighbours.py` Tier 2) | [`pqfK-GLNjgA`](https://youtu.be/pqfK-GLNjgA) | *Why Do Joints Pop And Crack?* | `why do joints pop and crack`, `synovial fluid`, `cavitation`, `knuckles` |
| 11 | `987,420` | TED-Ed ★ (`neighbours.py` Tier 1) | [`1Qfmkd6C8u8`](https://youtu.be/1Qfmkd6C8u8) | *How bones make blood - Melody Smith* | `bones`, `skeletal system` |
| 12 | `329,972` | FuseSchool (`neighbours.py` Tier 2) | [`NF51ioK6U14`](https://youtu.be/NF51ioK6U14) | *Joints \| Physiology \| Biology \| FuseSchool* | `joints`, `synovial joints`, `physiology` |

**Proposed subject-only tags (8 tags, zero channel names):**  
`why do knuckles crack, why do your knuckles pop, does cracking knuckles cause arthritis, donald unger 50 year experiment, greg kawchuk knuckle mri, synovial fluid cavitation, tribonucleation joints, history of medicine experiments`

---

## 3. Title ABC & Shorts (score before VO; `0` exact collisions verified across all `8` queries / `48` search results)

| | Title | Chars | Collisions (`2026-11-16`) | Role & Notes | Keep? |
|---|-------|------:|-----------:|--------------|-------|
| A | `Why Do Knuckles Crack? (The 50-Year Self-Experiment)` | 52 | 0 | **Main (`LEARNINGS.md` Rules 1, 23, 26):** Starts verbatim with exact autocomplete question `"why do knuckles crack"` + 50-year self-experiment hook (`50-char` tightened option: `Why Do Knuckles Crack? (A 50-Year Self-Experiment)`) | **Keep (Primary Proposal)** |
| B | `The 2015 MRI That Proved Why Your Knuckles Crack` | 48 | 0 | **Test & Compare (`Rule 15 ≤50 chars` & `Rule 23`):** Leads with the 2015 real-time MRI proof + exact search phrase | **Keep (T&C Arm 2)** |
| C | `Why Do Knuckles Crack? How an MRI Reversed a 44-Year Myth` | 57 | 0 | **Rule 26 Variant (`≤70 chars`):** Starts verbatim with exact autocomplete phrase `"why do knuckles crack"` + 44-year textbook reversal | **Keep (T&C Arm 3)** |
| S01 | `Why Did One Doctor Crack Only His Left Hand for 50 Years?` | 57 | 0 | **Short S01 (`Test B` / `Rule 32`):** Positive search question on Donald Unger's 50-year single-hand control experiment | **Keep (Short 1)** |
| S02 | `What Actually Makes the Pop When You Crack a Knuckle?` | 53 | 0 | **Short S02 (`Test B` / `Rule 32`):** Direct mechanism question on Kawchuk's 2015 cine-MRI cavity inception proof | **Keep (Short 2)** |
| Reject | `Tribonucleation and Synovial Joint Cavitation \| History of Science` | 67 | — | Academic jargon + forbidden series suffix | **Reject** |

---

## 3b. Script reviewer (blocking before VO — not run; backlog `next_hos` only)

- [ ] Active HOS WIP slot opens under Rule G (`jobs/WIP.json` `next_hos`)
- [ ] `SOURCES.md` exact quotes + `facts` lane verification completed (required before script lock)
- [ ] Score ≥ **90 / 100** (`npm run review:script`)
