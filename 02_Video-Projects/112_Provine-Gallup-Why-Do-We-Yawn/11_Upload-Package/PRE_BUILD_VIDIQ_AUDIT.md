# Pre-Build Search & Neighbour Audit — `112_Provine-Gallup-Why-Do-We-Yawn` (`HOS:112` Proposal)

> **PROPOSAL & RULE-E STATUS (`J2935` / `J2936`, `2026-11-16`):** Rule-E topic go/no-go review **GO (`95.5 / 100` · `9.55 / 10`)**, pre-cleared in `jobs/WIP.json` `next_hos` (Rule G; `4 / 4` active HOS slots full). All historical and scientific claims below remain **UNVERIFIED** working notes and must be sourced in `SOURCES.md` and checked by the `facts` lane (`gemini-agy`) when an active HOS WIP slot opens before script lock.

## 1. The Discovery Story (Person, Date & Twist — UNVERIFIED)

- **Familiar phenomenon:** Why we yawn (and why seeing, hearing, or reading about a yawn triggers one).
- **Person, place & date:**
  - **Hippocrates of Kos & Respiratory Physiology Textbooks (`~400 BC–1986`, UNVERIFIED):** Hippocrates' *De flatibus* (*On Breaths* / *On Winds*, `~400 BC`, §8) claims yawning before a fever vents hot accumulated air like steam from a cauldron; post-Lavoisier 18th–20th-century physiology textbooks codify the belief that yawning is a respiratory reflex triggered by low blood $\text{O}_2$ or high $\text{CO}_2$.
  - **Robert R. Provine, B. C. Tate & L. L. Geldmacher** (`1943–2019`, University of Maryland Baltimore County, *Ethology* `1986` & *Bulletin of the Psychonomic Society* **1987**, UNVERIFIED): after measuring the stereotyped `~6 s` (`5.9 s`) human yawn and `~55%` contagious release (`1986`), Provine's team tests volunteers breathing `3%–5%` $\text{CO}_2$ (`100×–166×` atmospheric) and `100%` pure $\text{O}_2$ in a chamber — proving breathing rates double under high $\text{CO}_2$ while yawning frequency does not change at all, and vigorous exercise has no effect on yawning either, overturning the 2,000-year-old oxygen myth.
  - **Andrew C. Gallup & Gordon G. Gallup Jr.** (SUNY Albany, *Evolutionary Psychology* **May 2007**, UNVERIFIED) and **Michael L. Shoup-Knox, Andrew C. Gallup, Gordon G. Gallup Jr. & Ewan C. McNay** (*Frontiers in Evolutionary Neuroscience* **2010**, UNVERIFIED): test the **cranial thermoregulation (brain-cooling) hypothesis**, showing exclusive nasal breathing drops contagious yawning from `48%` to `0%` (Experiment 1) and a `4°C` forehead cold pack drops contagious yawning from `41%` to `9%` compared to warm/room-temp packs (`46°C`, Experiment 2), followed by rat prelimbic cortical micro-thermoprobes (`2010`, recording brain temperature rising `~0.10–0.15°C` [`+0.11°C`] before a yawn and returning to baseline within `3 minutes` after) and outdoor thermal-window trials in Arizona (`2011`) and Vienna (`2014`).

---

## 2. Search-First Demand Check (`LEARNINGS.md` Rule 26, Retrieved `2026-11-16`)

- **Exact signed-out YouTube autocomplete phrases (`autocomplete = yes`):** `"why do we yawn"`, `"why is yawning contagious"`, and `"why do we yawn when someone else yawns"` (plus `"why do we sleep"` and `"staying up all night"` in `neighbours.json`)
  - **Ranking Video 1:** `jGIbUK4nw00` — *Why Is Yawning Contagious?* (`Vsauce`, **`4,827,757` views**, retrieved `2026-11-16`)
  - **Ranking Video 2:** `I0dQx4SNSwE` — *Why Do We Yawn?* (`AsapSCIENCE`, **`4,651,480` views**, retrieved `2026-11-16`; plus `TED-Ed` `4NpG4F9yq00` *Why is yawning contagious? - Claudia Aguirre* **`2,452,078` views**, `Smart Nonsense` `KLwxaRtiJ7k` *Why is yawning contagious??* **`1,162,824` views**, `Peekaboo Kidz` `0lsySXHa5l0` *Why Do We Yawn? \| The Dr. Binocs Show* **`1,049,429` views**, `SciShow` `ew_iZTPoC3c` *Why Do We Yawn?* **`466,447` views**, `Today I Learned Science` `mCHoseE8nJc` *Scientists Finally Cracked Why We Yawn* **`401,786` views**, and `SciShow Kids` `3jmp5yF5rYM` *Why Do We Yawn?* **`125,294` views**)
- **Decision:** Candidate primary title = `Why Do We Yawn? (The Brain-Cooling Experiment)` (Title A, `46 chars ≤ 50 chars` Rule 15 & Rule 26) / `Why Do We Yawn? How a Cold Pack Broke a 2,000-Year Myth` (Title C, `55 chars ≤ 70 chars`, exact phrase first)
- **Candidate description first 100 chars (unverified until `SOURCES.md` check):** `Why do we yawn, and how did a 1987 oxygen chamber and a forehead cold pack prove it cools the brain?`

---

## 2b. Neighbour pass (blocking · `STUDIO_PLAYBOOK.md` §2 Step 4, Retrieved `2026-11-16`)

Saved in [`evidence_2026-11-16_neighbours.json`](evidence_2026-11-16_neighbours.json) (`16` strictly on-topic `≥1M` education neighbours, `0` off-topic rows) and [`evidence_2026-11-16_public_search.json`](evidence_2026-11-16_public_search.json):

| # | Views (`2026-11-16`) | Channel (internal) | id & URL | Title | Subject words we reuse |
|---:|------:|--------------------|----------|-------|------------------------|
| 1 | `17,757,665` | TED ★ (`neighbours.py`) | [`5MuIMqhT8DM`](https://youtu.be/5MuIMqhT8DM) | *Sleep Is Your Superpower \| Matt Walker \| TED* | `sleep`, `brain`, `tiredness`, `body` |
| 2 | `15,049,789` | TED-Ed ★ (`neighbours.py`) | [`dqONk48l5vY`](https://youtu.be/dqONk48l5vY) | *What would happen if you didn't sleep? - Claudia Aguirre* | `sleep`, `your brain`, `fatigue` |
| 3 | `7,504,218` | TED-Ed ★ (`neighbours.py`) | [`gedoSfZvBgE`](https://youtu.be/gedoSfZvBgE) | *The benefits of a good night's sleep - Shai Marcu* | `sleep`, `brain function`, `rest` |
| 4 | `7,295,937` | TED-Ed ★ (`neighbours.py`) | [`idrbwnWLJ7w`](https://youtu.be/idrbwnWLJ7w) | *What staying up all night does to your brain - Anna Rothschild* | `staying up all night`, `your brain`, `exhaustion` |
| 5 | `4,827,757` | Vsauce (`neighbours.py` + `public_search.py`) | [`jGIbUK4nw00`](https://youtu.be/jGIbUK4nw00) | *Why Is Yawning Contagious?* | `why is yawning contagious`, `why do we yawn`, `brain cooling` |
| 6 | `4,651,480` | AsapSCIENCE (`public_search.py`) | [`I0dQx4SNSwE`](https://youtu.be/I0dQx4SNSwE) | *Why Do We Yawn?* | `why do we yawn`, `oxygen myth`, `brain temperature` |
| 7 | `4,613,307` | TED ★ (`neighbours.py`) | [`fQUeDdaVoWo`](https://youtu.be/fQUeDdaVoWo) | *Do You Really Need 8 Hours of Sleep Every Night? \| Body Stuff with Dr. Jen Gunter \| TED* | `sleep`, `hours of sleep`, `body` |
| 8 | `3,394,475` | Be Smart (`neighbours.py`) | [`3mufsteNrTI`](https://youtu.be/3mufsteNrTI) | *Why Do We Have To Sleep?* | `sleep`, `brain`, `thermoregulation` |
| 9 | `2,926,207` | TED ★ (`neighbours.py`) | [`LWULB9Aoopc`](https://youtu.be/LWULB9Aoopc) | *Why do we sleep? \| Russell Foster* | `why do we sleep`, `circadian`, `brain` |
| 10 | `2,452,078` | TED-Ed ★ (`neighbours.py` + `public_search.py`) | [`4NpG4F9yq00`](https://youtu.be/4NpG4F9yq00) | *Why is yawning contagious? - Claudia Aguirre* | `why is yawning contagious`, `yawning`, `brain` |
| 11 | `2,272,025` | SciShow (`neighbours.py`) | [`pwNMvUXTgDY`](https://youtu.be/pwNMvUXTgDY) | *Sleep: Why We Need It and What Happens Without It* | `sleep`, `fatigue`, `brain` |
| 12 | `1,049,429` | Peekaboo Kidz (`public_search.py`) | [`0lsySXHa5l0`](https://youtu.be/0lsySXHa5l0) | *Why Do We Yawn? \| The Dr. Binocs Show \| Best Learning Videos For Kids \| Peekaboo Kidz* | `why do we yawn`, `brain cooling`, `oxygen` |

**Proposed subject-only tags (8 tags, zero channel names):**  
`why do we yawn, why is yawning contagious, does yawning give you oxygen, brain cooling hypothesis yawning, robert provine yawning experiment, andrew gallup yawning, human body physiology, history of science experiments`

---

## 3. Title ABC (score before VO)

| | Title | Chars | Collisions (`2026-11-16`) | Role & Notes | Keep? |
|---|-------|------:|-----------:|--------------|-------|
| A | `Why Do We Yawn? (The Brain-Cooling Experiment)` | 46 | 0 | **Main (`LEARNINGS.md` Rules 1, 15, 23, 26):** Starts verbatim with exact autocomplete question `"why do we yawn"` + brain-cooling experimental twist (`≤ 50 chars`) | **Keep (Primary Proposal)** |
| B | `The 1987 Gas Chamber That Proved Why You Really Yawn` | 52 | 0 | **Test & Compare (`Rule 23`):** Leads with Provine's 1987 gas chamber + yawning subject | **Keep (T&C Arm 2)** |
| C | `Why Do We Yawn? How a Cold Pack Broke a 2,000-Year Myth` | 55 | 0 | **Rule 26 Variant (`≤70 chars`):** Starts verbatim with exact autocomplete phrase `"why do we yawn"` + cold-pack discovery story | **Keep (T&C Arm 3)** |
| Reject | `Cranial Thermoregulation and Chasmology \| History of Science` | 61 | — | Academic jargon + forbidden series suffix | **Reject** |

---

## 3b. Script reviewer (blocking before VO — not run; proposal only)

- [ ] `SOURCES.md` exact quotes + `facts` lane verification completed (required before script lock)
- [ ] Score ≥ **90 / 100** (`npm run review:script`)
