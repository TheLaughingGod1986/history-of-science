# Pre-Build Search & Neighbour Audit — `121_Owen-Remmers-Muggenthaler-Herbst-Why-Do-Cats-Purr` (`HOS:121` · Queued in `next_hos`)

> **RULE-E QUEUE STATUS (`J3097`, `2026-11-19`):** Queued in `jobs/WIP.json` `next_hos` (Rule G; `4 / 4` active HOS slots full) and queued for a **Rule-E** topic go/no-go review (`kind: review`). All historical and scientific claims below are **UNVERIFIED** working notes and must be sourced in `SOURCES.md` and checked by the `facts` lane (`gemini-agy`) when an active HOS WIP slot opens, before any script lock, VO, or picture spend.

## 1. The Discovery Story (Person, Date & Twist — UNVERIFIED)

- **Familiar phenomenon:** Why a 4-kilogram domestic cat can purr continuously on both inhale and exhale at a deep bass pitch of **25 to 30 hertz**—and why a century of neuroscience textbooks were wrong about how a cat's throat makes the sound.
- **Person, place & date:**
  - **Richard Owen** (Zoological Society of London, **1834–1835**, *Proceedings of the Zoological Society of London*, and **Reginald Innes Pocock**, **1916**, *Annals and Magazine of Natural History* `8(18): 306–316`): dissect the voice boxes of roaring big cats (*Pantherinae*) and purring cats (*Felinae*), discovering that purring cats have a completely ossified, rigid **epihyoid bone** anchoring the larynx while roaring cats have a flexible elastic ligament.
  - **John E. Remmers & Henry Gautier** (Dartmouth Medical School, **December 1972**, *Respiration Physiology* `16(3): 351–361`, `"Neural and mechanical mechanisms of feline purring"`): wire electromyography (EMG) electrodes and airflow transducers to purring cats, showing rhythmic electrical spikes at `25–30 Hz` in the intrinsic laryngeal muscles and creating the 50-year textbook orthodoxy that a cat's brain must actively command its vocal folds to twitch 30 times every second.
  - **Elizabeth von Muggenthaler** (Fauna Communications Research Institute, **2001**, *Journal of the Acoustical Society of America* `110(5): 2666`, `"The felid purr: A healing mechanism?"`): records the acoustic spectra of domestic cats, pumas, ocelots, and cheetahs, showing that every species clusters its fundamental purr frequency at **25–50 Hz** (with `100–140 Hz` harmonics)—the exact mechanical vibration range shown to stimulate bone density and tissue healing.
  - **Christian T. Herbst, Jan G. Švec, David M. Weissengruber, Tecumseh Fitch et al.** (University of Vienna, **10 October 2023**, *Current Biology* `33(21): 4727–4732.e4`, `"Domestic cat larynges can produce purring frequencies without neural input"`): blow warm humidified air through eight excised domestic cat larynges completely disconnected from the brain and discover that all eight purr spontaneously at **25–30 Hz** via up to **4-millimetre fibrous connective-tissue cushions ("purr pads")** embedded inside the vocal folds.

---

## 2. Search-First Demand Check (`LEARNINGS.md` Rule 26, Retrieved `2026-11-19`)

- **Exact signed-out YouTube autocomplete phrases (`autocomplete = yes`):** `"why do cats purr"`, `"how do cats purr"`, `"how does a cat purr"`, `"cat purring"`, and `"why do cats act so weird"`
  - **Ranking Video 1:** [`7KowU4tPi7Q`](https://youtu.be/7KowU4tPi7Q) — *Why Do Cats Purr?* (`SciShow`, **`1,895,855` views**, retrieved `2026-11-19`)
  - **Ranking Video 2:** [`sI8NsYIyQ2A`](https://youtu.be/sI8NsYIyQ2A) — *Why do cats act so weird? - Tony Buffington* (`TED-Ed`, **`13,424,182` views**, retrieved `2026-11-19`; plus `BrainStuff - HowStuffWorks` [`7_zKkBKu1fs`](https://youtu.be/7_zKkBKu1fs) *How (And Why) Do Cats Purr?* **`1,010,104` views**, `Colossal Cranium` [`_UCM5hsirhM`](https://youtu.be/_UCM5hsirhM) *Why Do Cats Purr?* **`1,419,224` views**, `Big Cat Rescue` [`eHZJrx7RZ2w`](https://youtu.be/eHZJrx7RZ2w) *Do Big Cats Purr?* **`1,405,918` views**, and `Mystery Science` [`83zcCB5zI5M`](https://youtu.be/83zcCB5zI5M) *Why do cats purr?* **`1,018,844` views**)
- **Decision:** Candidate primary title = `Why Do Cats Purr? (The 2023 Vocal Cord Twist)` (Title A, `45 chars`, `≤50 chars`) / `Why Do Cats Purr? The Secret Inside Cat Vocal Cords` (Title C, `51 chars`, exact phrase first)
- **Candidate description first 100 chars (unverified until `SOURCES.md` check):** `Why do cats purr? A 2023 Vienna larynx experiment proved cat vocal cords have built-in purr pads.`

---

## 2b. Neighbour pass (blocking · `STUDIO_PLAYBOOK.md` §2 Step 4, Retrieved `2026-11-19`)

Saved in [`evidence_2026-11-19_neighbours.json`](evidence_2026-11-19_neighbours.json) (`bigCount = 6` strictly on-topic education videos `≥1M` views, `hasTed = true`, `gate = PASS`, `0` off-topic rows) and [`evidence_2026-11-19_public_search.json`](evidence_2026-11-19_public_search.json) (`9` queries, `0` exact title collisions):

| # | Views (`2026-11-19`) | Channel (internal) | id & URL | Title | Subject words we reuse |
|---:|------:|--------------------|----------|-------|------------------------|
| 1 | `13,424,182` | TED-Ed ★ (`neighbours.py`) | [`sI8NsYIyQ2A`](https://youtu.be/sI8NsYIyQ2A) | *Why do cats act so weird? - Tony Buffington* | `why do cats`, `cat behaviour`, `feline` |
| 2 | `10,540,579` | TED-Ed ★ (`neighbours.py`) | [`Jsj-hDW9bS8`](https://youtu.be/Jsj-hDW9bS8) | *The history of the world according to cats - Eva-Maria Geigl* | `cats`, `domestic cat`, `evolution` |
| 3 | `4,837,753` | Jackson Galaxy (`public_search.py`) | [`LxhT_q9oUf8`](https://youtu.be/LxhT_q9oUf8) | *Cat Vocalizations and What They Mean* | `cat vocalizations`, `purring`, `vocal cords` |
| 4 | `4,611,737` | TED-Ed ★ (`neighbours.py`) | [`jdrNjHPYKz4`](https://youtu.be/jdrNjHPYKz4) | *Why do cats have vertical pupils? - Emma Bryce* | `why do cats`, `anatomy`, `predator` |
| 5 | `2,308,322` | SciShow (`neighbours.py`) | [`50feMMYsFWY`](https://youtu.be/50feMMYsFWY) | *Why Do Cats Do That? Baffling Cat Questions Explained!* | `why do cats`, `purr`, `cat questions` |
| 6 | `2,027,208` | TED-Ed ★ (`neighbours.py`) | [`rqno7K2zXi4`](https://youtu.be/rqno7K2zXi4) | *Is there a disease that makes us love cats? - Jaap de Roode* | `cats`, `biology` |
| 7 | `1,895,855` | SciShow (`neighbours.py`) | [`7KowU4tPi7Q`](https://youtu.be/7KowU4tPi7Q) | *Why Do Cats Purr?* | `why do cats purr`, `larynx`, `vocal cords`, `25 hertz` |
| 8 | `1,419,224` | Colossal Cranium (`public_search.py`) | [`_UCM5hsirhM`](https://youtu.be/_UCM5hsirhM) | *Why Do Cats Purr? 🐈 \| COLOSSAL QUESTIONS* | `why do cats purr`, `voice box`, `vibrations` |
| 9 | `1,405,918` | Big Cat Rescue (`public_search.py`) | [`eHZJrx7RZ2w`](https://youtu.be/eHZJrx7RZ2w) | *Do Big Cats Purr?* | `big cats purr`, `roar`, `hyoid bone` |
| 10 | `1,018,844` | Mystery Science (`public_search.py`) | [`83zcCB5zI5M`](https://youtu.be/83zcCB5zI5M) | *Why do cats purr?* | `why do cats purr`, `purring` |
| 11 | `1,010,104` | BrainStuff - HowStuffWorks (`public_search.py`) | [`7_zKkBKu1fs`](https://youtu.be/7_zKkBKu1fs) | *How (And Why) Do Cats Purr?* | `how do cats purr`, `why do cats purr`, `laryngeal muscles` |
| 12 | `377,296` | TED-Ed ★ (`neighbours.py`) | [`HDt_rTPPh70`](https://youtu.be/HDt_rTPPh70) | *Why does catnip make cats go crazy? - Jaap de Roode* | `why do cats`, `feline` |

**Proposed subject-only tags (8 tags, zero channel names):**  
`why do cats purr, how do cats purr, christian herbst cat purr pads, cat vocal cords larynx, why do cats purr at 25 hertz, why can cats purr but lions roar, elizabeth von muggenthaler cat purr, history of science experiments`

---

## 3. Title ABC (score before VO)

| | Title | Chars | Collisions (`2026-11-19`) | Role & Notes | Keep? |
|---|-------|------:|-----------:|--------------|-------|
| A | `Why Do Cats Purr? (The 2023 Vocal Cord Twist)` | 45 | 0 | **Main (`LEARNINGS.md` Rules 1, 15, 23, 26):** Compact `≤50 chars`, starts verbatim with exact autocomplete question `"why do cats purr"` + 2023 Vienna vocal-cord twist | **Keep (Primary Proposal)** |
| B | `Cats Don't Purr With Their Brain (The Vocal Pad)` | 48 | 0 | **Test & Compare (`Rules 15, 23`):** Compact `≤50 chars`, leads with the 50-year brain-twitch myth reversal + passive vocal pad | **Keep (T&C Arm 2)** |
| C | `Why Do Cats Purr? The Secret Inside Cat Vocal Cords` | 51 | 0 | **Rule 26 Variant (`≤70 chars`):** Starts verbatim with exact autocomplete phrase + vocal cord discovery | **Keep (T&C Arm 3)** |
| Reject | `Myoelastic-Aerodynamic Mechanisms of Feline Purring \| HOS` | 58 | — | Academic jargon + forbidden series suffix | **Reject** |

---

## 3b. Script reviewer (blocking before VO — not run; proposal only)

- [ ] `SOURCES.md` exact quotes + `facts` lane verification completed (required before script lock)
- [ ] Score ≥ **90 / 100** (`npm run review:script`)
