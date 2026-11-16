# Pre-Build Search & Neighbour Audit — `111_Roston-Unger-Kawchuk-Why-Do-Knuckles-Crack` (Proposal Only)

> **PROPOSAL & VERIFICATION STATUS (`J2922`, `2026-11-16`):**
> - This file records the pre-build search and neighbour evidence from `00_Brand/Channel-Setup/tools/public_search.py` and `00_Brand/Channel-Setup/tools/neighbours.py` (`£0` spend).
> - **Rule G (`jobs/WIP.json` `next_hos`):** This film is a backlog proposal only. All historical and scientific claims below are **UNVERIFIED** until `SOURCES.md` exact quotes and the `facts` lane (`gemini-agy`) run when an active HOS WIP slot opens.

---

## 1. Search Demand & Autocomplete (`public_search.py` · `LEARNINGS.md` Rule 26)

- **Exact Search Phrase (`Rule 26a`):** `"why do knuckles crack"` (`signed-out YouTube GB autocomplete = yes`)
  - Autocomplete suggestions (`2026-11-16`): `why do knuckles crack`, `why does cracking knuckles feel good`, `why is cracking knuckles bad`, `why does your knuckles crack`, `why do we crack knuckles`, `why do your knuckles pop`, `why do my knuckles pop`
  - Secondary phrase: `"does cracking knuckles cause arthritis"` (`autocomplete = yes`)
- **Rule 26(a) Two Ranking Videos (`2026-11-16`):**
  - **Phrase:** `"why do knuckles crack"`
  - **Ranking Video 1:** `n3IYmdy6d4Y` — *Here's what happens to your knuckles when you crack them* (`Vox`, **`67,776,939` views**, retrieved `2026-11-16`)
  - **Ranking Video 2:** `IjiKUmfaZr4` — *Why do your knuckles pop? - Eleanor Nelsen* (`TED-Ed`, **`5,782,999` views**, retrieved `2026-11-16`; plus `Doctor Mike` `PAKaVmcOPBY` **`6,910,969` views**, `RehabMedicineUofA` `BHEcQluSzmM` **`2,187,642` views**, and `Institute of Human Anatomy` `j43kNmg2x2U` **`1,814,225` views**)
- **Decision:** Candidate primary title = `Why Do Knuckles Crack? (The 50-Year Self-Experiment)` (Title A, `52 chars`) / `Why Do Knuckles Crack? How an MRI Reversed a 44-Year Myth` (Title C, `57 chars`, exact phrase first)
- **Candidate description first 100 chars (unverified until `SOURCES.md` check):** `Why do knuckles crack when you pull them, and how did a 2015 MRI reverse a 44-year textbook myth?`

---

## 2b. Neighbour pass (blocking · `STUDIO_PLAYBOOK.md` §2 Step 4, Retrieved `2026-11-16`)

Saved in [`evidence_2026-11-16_neighbours.json`](evidence_2026-11-16_neighbours.json) and [`evidence_2026-11-16_public_search.json`](evidence_2026-11-16_public_search.json):

| # | Views (`2026-11-16`) | Channel (internal) | id & URL | Title | Subject words we reuse |
|---:|------:|--------------------|----------|-------|------------------------|
| 1 | `67,776,939` | Vox (`public_search.py`) | [`n3IYmdy6d4Y`](https://youtu.be/n3IYmdy6d4Y) | *Here's what happens to your knuckles when you crack them* | `why do knuckles crack`, `knuckles`, `synovial fluid`, `mri`, `cavity` |
| 2 | `6,910,969` | Doctor Mike (`public_search.py`) | [`PAKaVmcOPBY`](https://youtu.be/PAKaVmcOPBY) | *The Truth About Cracking Your Knuckles \| Responding to Comments #15* | `cracking knuckles`, `arthritis`, `joints` |
| 3 | `5,782,999` | TED-Ed ★ (`neighbours.py`) | [`IjiKUmfaZr4`](https://youtu.be/IjiKUmfaZr4) | *Why do your knuckles pop? - Eleanor Nelsen* | `knuckles pop`, `synovial fluid`, `gas bubbles`, `donald unger`, `arthritis` |
| 4 | `4,388,731` | CrashCourse (`neighbours.py`) | [`DLxYDoN634c`](https://youtu.be/DLxYDoN634c) | *Joints: Crash Course Anatomy & Physiology #20* | `joints`, `synovial joints`, `cartilage`, `anatomy` |
| 5 | `4,266,670` | TED-Ed ★ (`neighbours.py`) | [`9mcuIc5O-DE`](https://youtu.be/9mcuIc5O-DE) | *How Do Pain Relievers Work? - George Zaidan* | `human body`, `physiology`, `medicine` |
| 6 | `3,268,923` | TED-Ed ★ (`neighbours.py`) | [`VVL-8zr2hk4`](https://youtu.be/VVL-8zr2hk4) | *How your muscular system works - Emma Bryce* | `bones`, `joints`, `movement`, `physiology` |
| 7 | `2,187,642` | RehabMedicineUofA (`public_search.py`) | [`BHEcQluSzmM`](https://youtu.be/BHEcQluSzmM) | *Pull my finger: Why joints crack* | `joints crack`, `greg kawchuk`, `mri`, `tribonucleation` |
| 8 | `1,814,225` | Institute of Human Anatomy (`public_search.py`) | [`j43kNmg2x2U`](https://youtu.be/j43kNmg2x2U) | *How Harmful Is It to "Pop" Your Knuckles?* | `pop your knuckles`, `synovial capsule`, `cavitation` |
| 9 | `1,312,995` | TED-Ed ★ (`neighbours.py`) | [`I5ZR0jMlxX0`](https://youtu.be/I5ZR0jMlxX0) | *What causes economic bubbles? - Prateek Singh* | `bubbles` |
| 10 | `1,192,035` | SciShow (`neighbours.py`) | [`pqfK-GLNjgA`](https://youtu.be/pqfK-GLNjgA) | *Why Do Joints Pop And Crack?* | `why do joints pop and crack`, `synovial fluid`, `cavitation`, `knuckles` |

**Proposed subject-only tags (8 tags, zero channel names):**  
`why do knuckles crack, why do your knuckles pop, does cracking knuckles cause arthritis, donald unger 50 year experiment, greg kawchuk knuckle mri, synovial fluid cavitation, tribonucleation joints, history of medicine experiments`

---

## 3. Title ABC (score before VO)

| | Title | Chars | Collisions (`2026-11-16`) | Role & Notes | Keep? |
|---|-------|------:|-----------:|--------------|-------|
| A | `Why Do Knuckles Crack? (The 50-Year Self-Experiment)` | 52 | 0 | **Main (`LEARNINGS.md` Rules 1, 23, 26):** Starts verbatim with exact autocomplete question `"why do knuckles crack"` + 50-year self-experiment hook | **Keep (Primary Proposal)** |
| B | `The 2015 MRI That Proved Why Your Knuckles Crack` | 48 | 0 | **Test & Compare (`Rule 23`):** Leads with the 2015 real-time MRI proof + exact search phrase | **Keep (T&C Arm 2)** |
| C | `Why Do Knuckles Crack? How an MRI Reversed a 44-Year Myth` | 57 | 0 | **Rule 26 Variant (`≤70 chars`):** Starts verbatim with exact autocomplete phrase `"why do knuckles crack"` + 44-year textbook reversal | **Keep (T&C Arm 3)** |
| Reject | `Tribonucleation and Synovial Joint Cavitation \| History of Science` | 67 | — | Academic jargon + forbidden series suffix | **Reject** |

---

## 3b. Script reviewer (blocking before VO — not run; proposal only)

- [ ] `SOURCES.md` exact quotes + `facts` lane verification completed (required before script lock)
- [ ] Score ≥ **90 / 100** (`npm run review:script`)
