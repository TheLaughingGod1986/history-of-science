# Pre-Build Search & Neighbour Audit — `112_Provine-Gallup-Why-Do-We-Yawn` (`HOS:112` Proposal)

> **PROPOSAL STATUS (`J2935`, `2026-11-16`):** Waiting in `jobs/WIP.json` `next_hos` (Rule G). All historical and scientific claims below are **UNVERIFIED** working notes and must be sourced in `SOURCES.md` and checked by the `facts` lane before script lock.

## 1. The Discovery Story (Person, Date & Twist — UNVERIFIED)

- **Familiar phenomenon:** Why we yawn (and why seeing or reading about a yawn triggers one).
- **Person, place & date:**
  - **Robert R. Provine** (1943–2019, University of Maryland Baltimore County, **1987**): tests volunteers breathing `3%–5%` $\text{CO}_2$ (`>100×` atmospheric) and `100%` pure $\text{O}_2$ in a chamber — proving breathing rates double under $\text{CO}_2$ while yawning frequency does not change at all, overturning the 2,000-year-old oxygen myth.
  - **Andrew C. Gallup & Gordon G. Gallup Jr.** (SUNY Albany / Princeton, **May 2007 – 2010**): test the **cranial thermoregulation (brain-cooling) hypothesis** using forehead cold packs (`4°C` vs `46°C` warm packs, dropping contagious yawning from `41%` to `9%`) and cortical micro-thermoprobes in rats (`2010`, recording brain temperature rising `~0.1–0.2°C` before a yawn and falling immediately after).

---

## 2. Search-First Demand Check (`LEARNINGS.md` Rule 26, Retrieved `2026-11-16`)

- **Exact signed-out YouTube autocomplete phrase (`autocomplete = yes`):** `"why do we yawn"` (plus `"why is yawning contagious"`)
  - **Ranking Video 1:** `jGIbUK4NwIw` — *Why Do We Yawn?* (`Vsauce`, **`4,827,754` views**, retrieved `2026-11-16`)
  - **Ranking Video 2:** `I0dQx4SNSwE` — *Why Do We Yawn?* (`AsapSCIENCE`, **`4,651,480` views**, retrieved `2026-11-16`; plus `TED-Ed` `4NpG4F9yq00` **`2,452,069` views**, `Peekaboo Kidz` `CF9bd42dc6I` **`1,049,428` views**, and `SciShow` `ew_iZTPoC3c` **`466,444` views**)
- **Decision:** Candidate primary title = `Why Do We Yawn? (The Brain-Cooling Experiment)` (Title A, `46 chars`) / `Why Do We Yawn? How a Cold Pack Broke a 2,000-Year Myth` (Title C, `55 chars`, exact phrase first)
- **Candidate description first 100 chars (unverified until `SOURCES.md` check):** `Why do we yawn, and how did a 1987 oxygen chamber and a forehead cold pack prove it cools the brain?`

---

## 2b. Neighbour pass (blocking · `STUDIO_PLAYBOOK.md` §2 Step 4, Retrieved `2026-11-16`)

Saved in [`evidence_2026-11-16_neighbours.json`](evidence_2026-11-16_neighbours.json) and [`evidence_2026-11-16_public_search.json`](evidence_2026-11-16_public_search.json):

| # | Views (`2026-11-16`) | Channel (internal) | id & URL | Title | Subject words we reuse |
|---:|------:|--------------------|----------|-------|------------------------|
| 1 | `17,757,465` | TED ★ (`neighbours.py`) | [`5MuIMqhT8DM`](https://youtu.be/5MuIMqhT8DM) | *Sleep Is Your Superpower \| Matt Walker \| TED* | `sleep`, `brain`, `tiredness`, `body` |
| 2 | `15,049,764` | TED-Ed ★ (`neighbours.py`) | [`dqONk48l5vY`](https://youtu.be/dqONk48l5vY) | *What would happen if you didn't sleep? - Claudia Aguirre* | `sleep`, `your brain`, `fatigue` |
| 3 | `9,128,903` | TED-Ed ★ (`neighbours.py`) | [`v-t1Z5-oPtU`](https://youtu.be/v-t1Z5-oPtU) | *How stress affects your body - Sharon Horesh Bergquist* | `nervous system`, `blood flow`, `breathing` |
| 4 | `9,029,031` | TED-Ed ★ (`neighbours.py`) | [`WuyPuH9ojCE`](https://youtu.be/WuyPuH9ojCE) | *How stress affects your brain - Madhumita Murgia* | `your brain`, `neurons`, `reflex` |
| 5 | `7,504,199` | TED-Ed ★ (`neighbours.py`) | [`gedoSfZvBgE`](https://youtu.be/gedoSfZvBgE) | *The benefits of a good night's sleep - Shai Marcu* | `sleep`, `brain function`, `rest` |
| 6 | `7,295,896` | TED-Ed ★ (`neighbours.py`) | [`idrbwnWLJ7w`](https://youtu.be/idrbwnWLJ7w) | *What staying up all night does to your brain - Anna Rothschild* | `staying up all night`, `your brain`, `exhaustion` |
| 7 | `4,827,754` | Vsauce (`public_search.py`) | [`jGIbUK4NwIw`](https://youtu.be/jGIbUK4NwIw) | *Why Do We Yawn?* | `why do we yawn`, `contagious yawning`, `brain cooling` |
| 8 | `4,651,480` | AsapSCIENCE (`public_search.py`) | [`I0dQx4SNSwE`](https://youtu.be/I0dQx4SNSwE) | *Why Do We Yawn?* | `why do we yawn`, `oxygen myth`, `brain temperature` |
| 9 | `2,452,069` | TED-Ed ★ (`neighbours.py`) | [`4NpG4F9yq00`](https://youtu.be/4NpG4F9yq00) | *Why is yawning contagious? - Claudia Aguirre* | `why is yawning contagious`, `empathy`, `mirror neurons` |
| 10 | `2,225,329` | TED-Ed ★ (`neighbours.py`) | [`_GI9-J-sE5k`](https://youtu.be/_GI9-J-sE5k) | *What's the best position to sleep in? - Rachel Marie E. Salas* | `sleep`, `breathing`, `physiology` |

**Proposed subject-only tags (8 tags, zero channel names):**  
`why do we yawn, why is yawning contagious, does yawning give you oxygen, brain cooling hypothesis yawning, robert provine yawning experiment, andrew gallup yawning, human body physiology, history of science experiments`

---

## 3. Title ABC (score before VO)

| | Title | Chars | Collisions (`2026-11-16`) | Role & Notes | Keep? |
|---|-------|------:|-----------:|--------------|-------|
| A | `Why Do We Yawn? (The Brain-Cooling Experiment)` | 46 | 0 | **Main (`LEARNINGS.md` Rules 1, 23, 26):** Starts verbatim with exact autocomplete question `"why do we yawn"` + brain-cooling experimental twist | **Keep (Primary Proposal)** |
| B | `The 1987 Gas Chamber That Proved Why You Really Yawn` | 52 | 0 | **Test & Compare (`Rule 23`):** Leads with Provine's 1987 gas chamber + yawning subject | **Keep (T&C Arm 2)** |
| C | `Why Do We Yawn? How a Cold Pack Broke a 2,000-Year Myth` | 55 | 0 | **Rule 26 Variant (`≤70 chars`):** Starts verbatim with exact autocomplete phrase `"why do we yawn"` + cold-pack discovery story | **Keep (T&C Arm 3)** |
| Reject | `Cranial Thermoregulation and Chasmology \| History of Science` | 61 | — | Academic jargon + forbidden series suffix | **Reject** |

---

## 3b. Script reviewer (blocking before VO — not run; proposal only)

- [ ] `SOURCES.md` exact quotes + `facts` lane verification completed (required before script lock)
- [ ] Score ≥ **90 / 100** (`npm run review:script`)
