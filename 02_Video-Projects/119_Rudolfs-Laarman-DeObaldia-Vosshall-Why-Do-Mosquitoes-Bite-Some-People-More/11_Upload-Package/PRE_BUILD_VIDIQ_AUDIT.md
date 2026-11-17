# Pre-Build Search & Neighbour Audit — `119_Rudolfs-Laarman-DeObaldia-Vosshall-Why-Do-Mosquitoes-Bite-Some-People-More` (`HOS:119` Proposal)

> **PROPOSAL STATUS (`J2970`, `2026-11-17`):** Waiting in `jobs/WIP.json` `next_hos` (Rule G). All historical and scientific claims below are **UNVERIFIED** working notes and must be sourced in `SOURCES.md` and checked by the `facts` lane before script lock.

## 1. The Discovery Story (Person, Date & Twist — UNVERIFIED)

- **Familiar phenomenon:** Why two people can sit side by side on a summer evening while one is bitten dozens of times and the other is barely touched ("mosquito magnets").
- **Person, place & date:**
  - **Willem Rudolfs** (New Jersey Agricultural Experiment Station, Rutgers University, **1922**, *Bulletin 367*) & **Jakob J. Laarman** (University of Leiden, **1955–1958**): Rudolfs tests dozens of isolated chemicals, sweat, and exhaled breath on *Aedes* mosquitoes, identifying **carbon dioxide ($\text{CO}_2$)** and body warmth as the long-range activators that wake mosquitoes up, while Laarman builds a precision **two-stream wind-tunnel olfactometer** proving that once $\text{CO}_2$ activates a mosquito, she steers toward specific, invisible human skin odours that differ sharply from person to person (later traced in part to **L-lactic acid** by Acree et al. in **1968**).
  - **Matthew DeGennaro & Leslie B. Vosshall** (Rockefeller University, **May 2013**, *Nature*): use zinc-finger nucleases to mutate the master odorant co-receptor gene **`Orco`** in *Aedes aegypti* mosquitoes — expecting them to become odour-blind to humans — only to discover that in the presence of $\text{CO}_2$, `Orco`-mutant mosquitoes still home in on human skin via a backup ionotropic acid-sensing pathway (`IR8a` / `IR25a` / `IR76b`).
  - **Maria Elena De Obaldia, Takeshi Morita, Laura C. Dedmon & Leslie B. Vosshall** (Rockefeller University, **18 October 2022**, *Cell*, alongside **Margaret Herre et al.**, **18 October 2022**, *Cell*): have 64 human volunteers wear **nylon stockings** over their forearms for 6 hours a day across a 3-year longitudinal tournament, cutting the stockings into 5 cm pieces and pitting them head-to-head in a two-choice olfactometer trap. They discover that **"Subject 33"** was **100 times more attractive** than the least-attracting volunteer (`Subject 19`) and stayed an unbeatable **"forever mosquito magnet"** for years because mosquito-magnet skin sebum produces dramatically higher levels of three long-chain **carboxylic acids** (pentadecanoic, heptadecanoic, and nonadecanoic acid) — and even when scientists knocked out entire families of smell receptors, mosquitoes broke the textbook "one-receptor-per-neuron" rule by co-expressing both odorant and ionotropic acid receptors inside the same sensory neuron so they can never lose our scent!

---

## 2. Search-First Demand Check (`LEARNINGS.md` Rule 26, Retrieved `2026-11-17`)

- **Exact signed-out YouTube autocomplete phrase (`autocomplete = yes`):** `"why do mosquitoes bite some people more"` and `"why do mosquitoes bite some people more than others"` (plus `"why are some people mosquito magnets"`)
  - **Ranking Video 1:** `38gVZgE39K8` — *Why Mosquitoes Bite Some People More Than Others* (`Veritasium`, **`10,410,342` views**, retrieved `2026-11-17`)
  - **Ranking Video 2:** `V6rRifwIaio` — *Why mosquitoes bite some people more than others - Maria Elena De Obaldia* (`TED-Ed`, **`2,203,920` views**, retrieved `2026-11-17`; plus `MinuteEarth` `bvKKHRCCkfI` **`3,091,491` views**, `Business Insider` **`1,560,180` views**, and `Peekaboo Kidz` **`1,517,060` views**)
- **Decision:** Candidate primary title = `Why Do Mosquitoes Bite Some People More? (The Stocking Test)` (Title A, `60 chars`) / `Why Do Mosquitoes Bite Some People More? (Solved)` (Title A1, `49 chars`, `≤50 chars`)
- **Candidate description first 100 chars (unverified until `SOURCES.md` check):** `Why do mosquitoes bite some people more? A 2022 nylon stocking test found the skin acids they hunt.`

---

## 2b. Neighbour pass (blocking · `STUDIO_PLAYBOOK.md` §2 Step 4, Retrieved `2026-11-17`)

Saved in [`evidence_2026-11-17_neighbours.json`](evidence_2026-11-17_neighbours.json) and [`evidence_2026-11-17_public_search.json`](evidence_2026-11-17_public_search.json):

| # | Views (`2026-11-17`) | Channel (internal) | id & URL | Title | Subject words we reuse |
|---:|------:|--------------------|----------|-------|------------------------|
| 1 | `12,513,522` | TED-Ed ★ (`neighbours.py`) | [`IkmjCmvfeFI`](https://youtu.be/IkmjCmvfeFI) | *The loathsome, lethal mosquito - Rose Eveleth* | `mosquito`, `carbon dioxide`, `skin`, `bite` |
| 2 | `10,410,341` | Veritasium (`neighbours.py`) | [`38gVZgE39K8`](https://youtu.be/38gVZgE39K8) | *Why Mosquitoes Bite Some People More Than Others* | `why mosquitoes bite some people more than others`, `lactic acid` |
| 3 | `3,091,491` | MinuteEarth (`neighbours.py`) | [`bvKKHRCCkfI`](https://youtu.be/bvKKHRCCkfI) | *Why Are Some People Mosquito Magnets?* | `mosquito magnets`, `body odour`, `skin bacteria` |
| 4 | `2,203,920` | TED-Ed ★ (`neighbours.py`) | [`V6rRifwIaio`](https://youtu.be/V6rRifwIaio) | *Why mosquitoes bite some people more than others - Maria Elena De Obaldia* | `nylon stockings`, `carboxylic acids`, `sebum`, `Subject 33` |
| 5 | `1,560,180` | Business Insider (`public_search.py`) | [`why do mosquitoes bite`](https://www.youtube.com/results?search_query=why+do+mosquitoes+bite+some+people+more) | *Why Mosquitoes Bite Some People More Than Others* | `mosquitoes bite`, `heat`, `sweat` |
| 6 | `1,517,060` | Peekaboo Kidz (`public_search.py`) | [`why do mosquitoes bite`](https://www.youtube.com/results?search_query=why+do+mosquitoes+bite+some+people+more) | *Why Do Mosquitoes Bite Some People More? \| The Dr. Binocs Show* | `why do mosquitoes bite some people more` |
| 7 | `1,317,427` | TED-Ed ★ (`neighbours.py`) | [`H7i9Anh0_Dg`](https://youtu.be/H7i9Anh0_Dg) | *Ethical dilemma: Should we get rid of mosquitoes? - Talya Hackett* | `mosquitoes`, `Aedes aegypti`, `ecology` |
| 8 | `689,694` | TED ★ (`neighbours.py`) | [`tsgvhP07BC8`](https://youtu.be/tsgvhP07BC8) | *Mosquitos, malaria and education \| Bill Gates* | `mosquitoes`, `bites` |
| 9 | `298,099` | TED-Ed ★ (`neighbours.py`) | [`ZLkbWUNQbgk`](https://youtu.be/ZLkbWUNQbgk) | *Mosquitos, malaria and education - Bill Gates* | `mosquitoes` |
| 10 | `237,081` | TED ★ (`neighbours.py`) | [`Rcm3rPz_Q94`](https://youtu.be/Rcm3rPz_Q94) | *The real reason why mosquitoes buzz \| DIY Neuroscience, a TED series* | `mosquitoes`, `antennae`, `sensory` |

**Proposed subject-only tags (8 tags, zero channel names):**  
`why do mosquitoes bite some people more, why are some people mosquito magnets, maria elena de obaldia, leslie vosshall mosquitoes, carboxylic acids skin mosquito, nylon stocking mosquito experiment, mosquito smell receptors, history of science experiments`

---

## 3. Title ABC (score before VO)

| | Title | Chars | Collisions (`2026-11-17`) | Role & Notes | Keep? |
|---|-------|------:|-----------:|--------------|-------|
| A | `Why Do Mosquitoes Bite Some People More? (The Stocking Test)` | 60 | 0 | **Main (`LEARNINGS.md` Rules 1, 23, 26):** Starts verbatim with exact autocomplete question `"why do mosquitoes bite some people more"` + 2022 nylon stocking test | **Keep (Primary Proposal)** |
| A1 | `Why Do Mosquitoes Bite Some People More? (Solved)` | 49 | 0 | **Compact `Rule 15 ≤50 chars` Variant:** Starts verbatim with exact autocomplete question, fits `≤50 chars` | **Keep (Compact Option)** |
| B | `Mosquito Magnets Are Real (The 2022 Stocking Test)` | 50 | 0 | **Test & Compare (`Rule 23`):** Compact `≤50 chars`, leads with the "mosquito magnet" hook + 2022 Rockefeller stocking tournament | **Keep (T&C Arm 2)** |
| C | `Why Do Mosquitoes Bite Some People More? The Skin-Acid Experiment` | 65 | 0 | **Rule 26 Variant (`≤70 chars`):** Starts verbatim with exact autocomplete phrase + skin carboxylic-acid experiment | **Keep (T&C Arm 3)** |
| Reject | `Differential Attraction of Aedes aegypti to Carboxylic Acids \| HOS` | 67 | — | Academic jargon + forbidden series suffix | **Reject** |

---

## 3b. Script reviewer (blocking before VO — not run; proposal only)

- [ ] `SOURCES.md` exact quotes + `facts` lane verification completed (required before script lock)
- [ ] Score ≥ **90 / 100** (`npm run review:script`)
