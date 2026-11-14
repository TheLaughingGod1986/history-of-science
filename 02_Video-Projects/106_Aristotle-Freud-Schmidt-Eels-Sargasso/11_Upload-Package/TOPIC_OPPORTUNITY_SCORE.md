# Topic Opportunity Score — `HOS:106` (`106_Aristotle-Freud-Schmidt-Eels-Sargasso`)

> **Rule-E Topic Review Verdict (`J2836`, 14 Nov 2026):** **GO (`9.40 / 10` · `94 / 100` Opportunity Score)** — Pre-cleared in `jobs/WIP.json` `next_hos` under Rule G.
> **Unverified Claims Guard:** All historical and scientific claims in `TOPIC.md` §2 and `PRE_BUILD_VIDIQ_AUDIT.md` remain **UNVERIFIED** working notes and are **NOT CLEARED FOR NARRATION OR SHORT OPENS** until an active HOS WIP slot opens, exact primary-source quotes are recorded in `SOURCES.md`, and the `facts` lane (`gemini-agy`) verifies every claim.

**Candidate topic:** Where Do Eels Come From? — Aristotle's mud puzzle, 19-year-old Sigmund Freud's 1876 Trieste dissections of ~400 eels, Grassi & Calandruccio's 1896 transparent leaf-larva (*Leptocephalus*) metamorphosis, Johannes Schmidt's 1904–1922 Atlantic plankton-net hunt to the Sargasso Sea, and the 2022 satellite-tag proof (`HOS:106`)
**Primary search phrase:** `"where do eels come from"` / `"how do eels reproduce"` / `"eel migration"` (signed-out YouTube GB `public_search.py` autocomplete = **yes** on all three, retrieved `2026-11-14`)
**Date:** `2026-11-14` (`J2835` topic proposal · `J2836` Rule-E review by `macbook`)

---

## 1. Weighted Rubric (`00_Brand/Channel-Setup/templates/TOPIC_OPPORTUNITY_SCORE.md`)

| Dimension | Weight | Score (1–10) | Weighted | Evidence & Rationale |
|-----------|--------|--------------|----------|----------------------|
| **1. Evergreen search intent** | 25% | **9.5** | **2.375** | `"where do eels come from"` (`5` autocomplete suggestions), `"how do eels reproduce"` (`7` suggestions), `"eel migration"` (`9` suggestions), and `"sargasso sea eels"` (`1` suggestion) all autocomplete (`suggest = yes`) in signed-out YouTube GB (`evidence_2026-11-14_public_search.json`). Top ranking videos carry **`3,317,475` views** (`Thoughty2` `k61Bk63EvTM`), **`2,751,342` views** (`TED-Ed` `RFi6ISTjkR4`), **`1,629,143` views** (`Auralis` `LxNq8zOEbM8`), **`1,594,707` views** (`Bizarre Beasts` `acEIGorImGs`), and **`1,157,611` views** (`TED-Ed` `BR1enXROmgA`). |
| **2. Competition gap (wonder / clarity vs dry or crowding)** | 20% | **9.0** | **1.800** | `TED-Ed` (`RFi6ISTjkR4`, `2.75M`, `6:02`) is a short flat-2D overview; `Thoughty2` (`3.32M`, `16:08`) and `Bizarre Beasts` (`1.59M`) are talking-head / stock-footage explainers; `MinuteEarth` (`569k`, `2:53`) is a 3-minute stick-figure summary. None builds the 4-room chronological 3D detective story (Aristotle's river mud → Freud's 1876 Trieste microscope bench → Grassi's 1896 Sicilian aquarium → Schmidt's 1904–1922 *Dana* plankton nets & contour map across the Atlantic). |
| **3. Narrative & visual arc (3D world + diagram clarity)** | 20% | **9.5** | **1.900** | Extraordinary visual progression for HOS's painted-3D house look and *Teach on screen* graphics: (1) 19-year-old Freud in Trieste slicing open eel #400 (`0:05–0:15` proof-first open), (2) a glass-clear willow-leaf fish (*Leptocephalus*) shrinking and rounding into a transparent glass eel in Grassi's tank, (3) an animated period-paper Atlantic contour map (`DATA + SCALE`) where Schmidt's larval lengths shrink from `45 mm` to `<10 mm` toward the Sargasso Sea, and (4) the 2022 satellite pop-up tag twist. |
| **4. Brand & guardrail fit** | 20% | **10.0** | **2.000** | Pure History of Science discovery story with a famous scientist in an unexpected youthful failure (Freud at 19), a 2,000-year everyday biological mystery, a 20-year ocean measurement campaign, and an unfinished modern frontier. Zero fearbait, zero gore (clean anatomical ink diagrams / laboratory tray per HOS `005` guardrail), zero overlap with `000–105` or `ideas/`. |
| **5. Series / cluster potential** | 15% | **8.8** | **1.320** | Forms the **Animal Navigation & Ocean Mysteries Cluster** alongside `100_Gilbert-Wiltschko-Mouritsen-Bird-Magnetic-Compass` (robin quantum magnetoreception, already shares `TED-Ed` `BR1enXROmgA` *Eli the eel* as a migration neighbour!), `101_Corliss-Ballard-Cavanaugh-Deep-Sea-Hydrothermal-Vents` (1977 *Alvin* dive), and `089_Frisch-Lindauer-Michelsen-Honeybee-Waggle-Dance-Robot-Bee`. |
| **Total** | **100%** | — | **`9.40 / 10` (`94 / 100`)** | **GO (`≥ 7.5` threshold exceeded by `+1.90` points)** |

**Rule:** Proceed (`GO`) if **Total ≥ 7.5** and **Brand fit ≥ 8**. Both pass (`9.40 / 10` total, `10.0 / 10` brand fit).

---

## 2. Education Neighbour Gate (`neighbours.py` + `public_search.py`, Retrieved `2026-11-14`)

Saved in [`evidence_2026-11-14_neighbours.json`](evidence_2026-11-14_neighbours.json) (`bigCount = 3`, `hasTed = true`, `gate = PASS`) and [`evidence_2026-11-14_public_search.json`](evidence_2026-11-14_public_search.json):

| # | Channel | Views (`2026-11-14`) | Video ID & URL | Title | Source File |
|---:|---|---:|---|---|---|
| 1 | **Thoughty2** | `3,317,475` | [`k61Bk63EvTM`](https://youtu.be/k61Bk63EvTM) | *Why Nobody Knows How Eels Reproduce* | `neighbours.json` (Tier 2) + `public_search.json` |
| 2 | **TED-Ed ★** | `2,751,342` | [`RFi6ISTjkR4`](https://youtu.be/RFi6ISTjkR4) | *No one can figure out how eels have sex - Lucy Cooke* | `neighbours.json` (Tier 1) + `public_search.json` |
| 3 | **Auralis** | `1,629,143` | [`LxNq8zOEbM8`](https://youtu.be/LxNq8zOEbM8) | *Eels Shouldn't Be Able To Exist...* | `public_search.json` |
| 4 | **Bizarre Beasts** (Complexly / Hank Green) | `1,594,707` | [`acEIGorImGs`](https://youtu.be/acEIGorImGs) | *We Finally Know Where Eels Come From* | `public_search.json` |
| 5 | **TED-Ed ★** | `1,157,611` | [`BR1enXROmgA`](https://youtu.be/BR1enXROmgA) | *Eli the eel: A mysterious migration - James Prosek* | `neighbours.json` (Tier 1) + `public_search.json` |
| 6 | **MinuteEarth** | `569,775` | [`DQVUuBQtb7w`](https://youtu.be/DQVUuBQtb7w) | *Why We Haven’t Learned More In 101 Years Of Trying* | `public_search.json` (Tier 2) |

---

## 3. Cluster Sketch (3 Adjacent Episodes)

1. **`HOS:106` (This Episode):** *Where Do Eels Come From? (The Sargasso Sea Hunt)* — Aristotle's mud puzzle, Freud's 1876 Trieste dissections, Grassi's 1896 *Leptocephalus* metamorphosis, and Johannes Schmidt's 1904–1922 Atlantic larval contour map to the Sargasso Sea.
2. **`HOS:100` (`100_Gilbert-Wiltschko-Mouritsen-Bird-Magnetic-Compass`, in `next_hos`):** *How Do Birds Know Which Way Is South?* — William Gilbert's Earth-as-magnet, the Wiltschkos' 1972 inclination compass, and radical-pair magnetoreception in the robin's eye.
3. **`HOS:101` (`101_Corliss-Ballard-Cavanaugh-Deep-Sea-Hydrothermal-Vents`, in `next_hos`):** *How Does Life Survive at the Bottom of the Ocean Without Sunlight?* — The 1977 *Alvin* dive to the Galápagos Rift and Colleen Cavanaugh's chemosynthesis discovery.
4. **`HOS:089` (`089_Frisch-Lindauer-Michelsen-Honeybee-Waggle-Dance-Robot-Bee`, in `ideas/`):** *How Do Honeybees Tell Each Other Where the Flowers Are?* — Karl von Frisch's waggle dance and Axel Michelsen's mechanical robot bee proof.
