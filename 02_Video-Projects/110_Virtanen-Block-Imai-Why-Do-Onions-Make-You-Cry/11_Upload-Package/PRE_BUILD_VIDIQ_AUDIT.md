# Pre-Build Search & Neighbour Audit — `110_Virtanen-Block-Imai-Why-Do-Onions-Make-You-Cry` (`HOS:110` — Rule-E GO in `next_hos`)

> **RULE-E GO & VERIFICATION STATUS (`J2922` / `J2924`, `2026-11-16`):**
> - This file records the pre-build search and neighbour evidence from `00_Brand/Channel-Setup/tools/public_search.py` and `00_Brand/Channel-Setup/tools/neighbours.py` (`£0` spend), verified in `J2924` (**GO, `95 / 100` · `9.50 / 10` Opportunity Score**).
> - **Rule G (`jobs/WIP.json` `next_hos`):** This film sits in the backlog waiting line (`active` has `4 / 4` HOS slots full). All historical and scientific claims below are **UNVERIFIED** working notes until `SOURCES.md` exact quotes and the `facts` lane (`gemini-agy`) run when an active HOS WIP slot opens.

---

## 1. Search Demand & Autocomplete (`public_search.py` · `LEARNINGS.md` Rule 26)

- **Exact Search Phrase (`Rule 26a`):** `"why do onions make you cry"` (`signed-out YouTube GB autocomplete = yes`)
  - Autocomplete suggestions (`2026-11-16`): `why do onions make you cry`, `why do onions make you cry aumsum`, `why do onions make you cry muppets`, `why do onions make you cry zack d films`, `why do onions make us cry`
  - Secondary phrases:
    - `"why do we cry"` (`autocomplete = yes`, including `"why do we cry when we cut onions"`)
    - `"how enzymes work"` (`autocomplete = yes`)
- **Rule 26(a) Two Ranking Videos (`2026-11-16`):**
  - **Phrase:** `"why do onions make you cry"`
  - **Ranking Video 1:** `1OoWsiY6Lf8` — *Why Do Onions Make Us Cry? | COLOSSAL QUESTIONS* (`Colossal Cranium`, **`3,486,968` views**, retrieved `2026-11-16`)
  - **Ranking Video 2:** `9ZinH1jEhb4` — *Human Tears - Why do onions make you cry?* (`It's AumSum Time`, **`2,452,719` views**, retrieved `2026-11-16`; plus `AumSum's What-If` `dVw3DrqihIg` **`2,917,778` views**, `SciShow` `vRroj26qVb0` **`623,053` views**, `SciShow Kids` `mBiNkhigr8o` **`301,430` views**, `Seeker` `ERtlCbByqVg` **`194,407` views**, `SciShow` `IS9bo3cVmYI` **`107,920` views**, and `Reactions` `RaZpPwmWZ7Q` **`107,887` views**)
- **Decision:** Candidate primary title = `Why Do Onions Make You Cry? (The 2002 Enzyme Twist)` (Title A, `51 chars ≤ 70 chars` Rule 26) / `Why Do Onions Make You Cry? (2002 Enzyme Twist)` (Compact Title A1, `47 chars ≤ 50 chars` Rule 15) / `Why Do Onions Make You Cry? How a Second Enzyme Was Found` (Title C, `57 chars`, exact phrase first)
- **Candidate description first 100 chars (unverified until `SOURCES.md` check):** `Why do onions make you cry when you slice them, and how did a 2002 vial test find a second enzyme?`

---

## 2b. Neighbour pass (blocking · `STUDIO_PLAYBOOK.md` §2 Step 4, Retrieved `2026-11-16`)

Saved in [`evidence_2026-11-16_neighbours.json`](evidence_2026-11-16_neighbours.json) (`bigCount = 12`, `onTopicBigCount = 9`, `hasTed = true`, `gate = PASS`) and [`evidence_2026-11-16_public_search.json`](evidence_2026-11-16_public_search.json):

| # | Views (`2026-11-16`) | Channel (internal) | id & URL | Title | Subject words we reuse |
|---:|------:|--------------------|----------|-------|------------------------|
| 1 | `14,043,201` | TED-Ed ★ (`neighbours.py`) | [`Og5xAdC8EUI`](https://youtu.be/Og5xAdC8EUI) | *How your digestive system works - Emma Bryce* | `enzymes`, `chemical reactions`, `cells` |
| 2 | `7,269,331` | Amoeba Sisters (`neighbours.py`) | [`qgVFkRn8f10`](https://youtu.be/qgVFkRn8f10) | *Enzymes (Updated)* | `enzymes`, `substrate`, `active site`, `reaction` |
| 3 | `6,914,192` | TED-Ed ★ (`neighbours.py` + `public_search.py`) | [`keMF8YzQoRM`](https://youtu.be/keMF8YzQoRM) | *Why do we cry? The three types of tears - Alex Gendler* | `why do we cry`, `reflex tears`, `onion`, `cornea`, `lacrimal glands` |
| 4 | `5,544,058` | AsapSCIENCE (`public_search.py`) | [`QGdHJSIr1Z0`](https://youtu.be/QGdHJSIr1Z0) | *Why Do We Cry?* | `tears`, `eyes`, `chemical irritant` |
| 5 | `4,447,334` | TED-Ed ★ (`neighbours.py`) | [`Hja0SLs2kus`](https://youtu.be/Hja0SLs2kus) | *The amazing ways plants defend themselves - Valentin Hammoudi* | `plant chemical defense`, `cells`, `volatile compounds` |
| 6 | `4,171,001` | TED-Ed ★ (`neighbours.py`) | [`n6wpNhyreDE`](https://youtu.be/n6wpNhyreDE) | *How to make the perfect cookies (according to science) - Stephanie Warren* | `food chemistry`, `chemical reactions`, `molecules` |
| 7 | `3,486,968` | Colossal Cranium (`public_search.py`) | [`1OoWsiY6Lf8`](https://youtu.be/1OoWsiY6Lf8) | *Why Do Onions Make Us Cry? \| COLOSSAL QUESTIONS* | `why do onions make you cry`, `onions`, `tears`, `eyes`, `gas` |
| 8 | `2,917,778` | AumSum's What-If (`public_search.py`) | [`dVw3DrqihIg`](https://youtu.be/dVw3DrqihIg) | *Why do Onions make us Cry?* | `why do onions make you cry`, `amino acid sulfoxides`, `synthase` |
| 9 | `2,468,735` | TED-Ed ★ (`neighbours.py`) | [`OttRV5ykP7A`](https://youtu.be/OttRV5ykP7A) | *How to speed up chemical reactions (and get a date) - Aaron Sams* | `chemical reaction`, `catalyst`, `molecules` |
| 10 | `2,452,719` | It's AumSum Time (`public_search.py`) | [`9ZinH1jEhb4`](https://youtu.be/9ZinH1jEhb4) | *Human Tears - Why do onions make you cry?* | `why do onions make you cry`, `syn-propanethial-S-oxide`, `lachrymatory factor` |
| 11 | `2,362,239` | TED-Ed ★ (`neighbours.py`) | [`ee7muQ_qKU0`](https://youtu.be/ee7muQ_qKU0) | *The wild world of carnivorous plants - Kenny Coogan* | `plants`, `enzymes`, `adaptation` |
| 12 | `1,634,395` | RCSBProteinDataBank (`public_search.py`) | [`yk14dOOvwMk`](https://youtu.be/yk14dOOvwMk) | *How Enzymes Work (from PDB-101)* | `how enzymes work`, `crystal structure`, `active site` |
| 13 | `1,151,481` | FuseSchool (`neighbours.py`) | [`rlH1ym916Fo`](https://youtu.be/rlH1ym916Fo) | *Enzymes \| Cells \| Biology \| FuseSchool* | `enzymes`, `catalyst`, `substrate` |
| 14 | `1,073,460` | TED-Ed ★ (`neighbours.py`) | [`8m6RtOpqvtU`](https://youtu.be/8m6RtOpqvtU) | *What triggers a chemical reaction? - Kareem Jarrah* | `chemical reaction`, `molecules`, `bonds` |

*(Three broad `"how ... work"` physiology hits in `evidence_2026-11-16_neighbours.json` — `PSRJfaAYkW4` `5.23M` immune system, `ClPVJ25Ka4k` `4.73M` antidepressants, and `-SPRPkLoKp8` `2.73M` hormones — are marked `"onTopic": false` and excluded from the curated table above).*

**Proposed subject-only tags (8 tags, zero channel names):**  
`why do onions make you cry, why cutting onions makes you cry, lachrymatory factor synthase, shinsuke imai onion enzyme, eric block onion chemistry, plant chemical defense, how enzymes work, history of chemistry experiments`

---

## 3. Title ABC (score before VO)

| | Title | Chars | Collisions (`2026-11-16`) | Role & Notes | Keep? |
|---|-------|------:|-----------:|--------------|-------|
| A | `Why Do Onions Make You Cry? (The 2002 Enzyme Twist)` | 51 | 0 | **Main (`LEARNINGS.md` Rules 1, 23, 26):** Starts verbatim with exact autocomplete question `"why do onions make you cry"` + 2002 second-enzyme twist (`≤70 chars` Rule 26) | **Keep (Primary Proposal)** |
| A1 | `Why Do Onions Make You Cry? (2002 Enzyme Twist)` | 47 | 0 | **Compact Main (`Rule 15` `≤50 chars` + `Rule 26`):** Exact autocomplete question first + compact 2002 twist (`47 chars ≤ 50`) | **Keep (Compact Primary Variant)** |
| B | `The Hidden Chemical Weapon Inside Every Sliced Onion` | 52 | 0 | **Test & Compare (`Rule 23`):** Leads with the plant's two-compartment chemical weapon + sliced onion subject | **Keep (T&C Arm 2)** |
| C | `Why Do Onions Make You Cry? How a Second Enzyme Was Found` | 57 | 0 | **Rule 26 Variant (`≤70 chars`):** Starts verbatim with exact autocomplete phrase `"why do onions make you cry"` + discovery story | **Keep (T&C Arm 3)** |
| Reject | `Lachrymatory Factor Synthase and Alliinase in Allium cepa \| History of Science` | 78 | — | Academic jargon + forbidden series suffix | **Reject** |

---

## 3b. Script reviewer (blocking before VO — not run; proposal only)

- [ ] `SOURCES.md` exact quotes + `facts` lane verification completed (required before script lock)
- [ ] Score ≥ **90 / 100** (`npm run review:script`)
