# Pre-Build Search & Neighbour Audit — `127_Wright-Brothers-How-Do-Airplanes-Fly-Wind-Tunnel` (`HOS:127` · Proposed for `next_hos`)

> **PROPOSAL STATUS (`J3245`, `2026-11-21`):** Appended to `jobs/WIP.json` `next_hos` (Rule G; `4 / 4` active HOS slots full) and queued for Rule-E topic go/no-go review. Directly implements **Cluster 4 Lead Film (Thu 28 Jan 2027)** of Ben's approved `hos-search-2027-01` plan (`J3224`). All historical and scientific claims below are **UNVERIFIED** working notes and must be sourced in `SOURCES.md` and checked by the `facts` lane (`gemini-agy`) when an active HOS WIP slot opens, before any script lock, VO, or picture spend.

## 1. The Discovery Story (Person, Date & Twist — UNVERIFIED)

- **Familiar phenomenon:** How an airplane wing generates lift and stays under a pilot's control — and why two Ohio bicycle mechanics solved flight not with a bigger engine, but by proving a 142-year-old physics table wrong inside a homemade wind tunnel.
- **Person, place & date:**
  - **Wilbur & Orville Wright** (Dayton, Ohio bicycle shop & Kill Devil Hills / Kitty Hawk, North Carolina, **October–December 1901** → **17 December 1903**): after their 1901 glider built to Otto Lilienthal's lift tables and John Smeaton's 1759 air-pressure coefficient (`0.005`) produces barely a third of the expected lift, they build a **6-foot wooden wind tunnel** with hacksaw-blade and bicycle-spoke balances, test over **200 miniature metal airfoil shapes** in two months, prove Smeaton's coefficient is ~50% too high (`0.0033`), invent linked **wing-warping + movable rudder** three-axis control (1902), and achieve controlled powered flight on **17 December 1903** (`12 s / 120 ft` to `59 s / 852 ft`).

---

## 2. Search-First Demand Check (`LEARNINGS.md` Rule 26 + `J3224`, Retrieved `2026-11-21`)

- **`J3224` vidIQ demand (`2026-11-20`):** `wright brothers first flight` = **`19,018` est. monthly searches**, competition **`45`** (`the wright brothers` `+74.8%` growth), **`10/10` US signed-out SERP gap** (archival clips and 3+ yr uploads, zero 3D narrative explainers), strong US/UK/CA/AU adult curiosity (`History Dude` 1.1K US → `51.9K` 13×; `Acta Historia` 1.2K CA → `1.4K` 12×).
- **Exact signed-out YouTube autocomplete phrases (`autocomplete = yes`, `2026-11-21`):** `"how do airplanes fly"`, `"wright brothers first flight"`, `"wright brothers wind tunnel"`, `"how does an airplane wing work"`.
  - **Ranking Video 1:** [`p4VHMsIuPmk`](https://youtu.be/p4VHMsIuPmk) — *How do airplanes actually fly? - Raymond Adkins* (`TED-Ed`, **`2,568,211` views**, retrieved `2026-11-21`)
  - **Ranking Video 2:** [`YDlk4Ky_ahs`](https://youtu.be/YDlk4Ky_ahs) — *The Wright Brothers, First Successful Airplane (1903)* (`Simple History`, **`1,410,350` views**, retrieved `2026-11-21`)
- **Decision:** Candidate primary title = `How Do Airplanes Fly? (The 1901 Wind Tunnel)` (Title A, `44 chars ≤ 50`, `0` collisions) / `Wright Brothers First Flight: The 1901 Wind Tunnel` (Title B, `50 chars ≤ 50`, `0` collisions).
- **Candidate description first 100 chars (unverified until `SOURCES.md` check):** `How do airplanes fly? How the Wright brothers' 1901 bicycle-shop wind tunnel proved the flight tables wrong.`

---

## 2b. Neighbour pass (blocking · `STUDIO_PLAYBOOK.md` §2 Step 4, Retrieved `2026-11-21`)

Saved in [`evidence_2026-11-21_neighbours.json`](evidence_2026-11-21_neighbours.json) (`bigCount = 8` raw / **`6` strictly on-topic** education videos `≥1M` views after excluding `2` airplane-keyword false positives `dzrwnwOx0fw` & `iKYHf22qVdM`, `hasTed = true`, `gate = PASS`) and [`evidence_2026-11-21_public_search.json`](evidence_2026-11-21_public_search.json) (`9` queries, `0` exact title collisions):

| # | Views (`2026-11-21`) | Channel (internal) | id & URL | Title | Subject words we reuse |
|---:|------:|--------------------|----------|-------|------------------------|
| 1 | `4,461,586` | Sabin Civil Engineering (`public_search.py`) | [`LigpsX1KoQE`](https://youtu.be/LigpsX1KoQE) | *The Brilliant Engineering of FIRST FLIGHT !* | `first flight`, `wright brothers`, `lift`, `wing` |
| 2 | `2,568,211` | TED-Ed ★ (`neighbours.py`) | [`p4VHMsIuPmk`](https://youtu.be/p4VHMsIuPmk) | *How do airplanes actually fly? - Raymond Adkins* | `how do airplanes fly`, `lift`, `airfoil` |
| 3 | `2,519,461` | TED-Ed ★ (`neighbours.py`) | [`hd8tYiLSmn0`](https://youtu.be/hd8tYiLSmn0) | *Why are airplanes slower than they used to be? - Alex Gendler* | `airplanes`, `drag`, `aerodynamics` |
| 4 | `2,481,276` | minutephysics (`neighbours.py`) | [`Gg0TXNXgz-w`](https://youtu.be/Gg0TXNXgz-w) | *How Do Airplanes Fly?* | `how do airplanes fly`, `wings`, `airflow` |
| 5 | `1,754,830` | SciShow Kids (`neighbours.py`) | [`VLpSxHwfU04`](https://youtu.be/VLpSxHwfU04) | *How Airplanes Fly! \| Airplane Science* | `how airplanes fly`, `lift`, `thrust`, `drag` |
| 6 | `1,662,146` | Veritasium (`neighbours.py`) | [`aFO4PBolwFg`](https://youtu.be/aFO4PBolwFg) | *How Does A Wing Actually Work?* | `how does a wing work`, `lift`, `airflow` |
| 7 | `1,410,350` | Simple History (`neighbours.py`) | [`YDlk4Ky_ahs`](https://youtu.be/YDlk4Ky_ahs) | *The Wright Brothers, First Successful Airplane (1903)* | `wright brothers`, `first flight`, `1903`, `Kitty Hawk` |
| 8 | `384,058` | Real Engineering (`neighbours.py`) | [`WCPapu78SNM`](https://youtu.be/WCPapu78SNM) | *Wright Brothers Didn't Invent Flight* | `wright brothers`, `control`, `wing warping` |
| 9 | `293,525` | SciShow (`neighbours.py`) | [`9S7H8TlkBC4`](https://youtu.be/9S7H8TlkBC4) | *How the Wright Brothers Changed Everything We Know About Flying* | `wright brothers`, `wind tunnel`, `flight` |

**Proposed subject-only tags (8 tags, zero channel names):**  
`how do airplanes fly, wright brothers first flight, wright brothers wind tunnel, how does an airplane wing work, 1901 wind tunnel experiment, smeaton coefficient lift, wing warping three axis control, history of engineering breakthroughs`

---

## 3. Title ABC (score before VO)

| | Title | Chars | Collisions (`2026-11-21`) | Role & Notes | Keep? |
|---|-------|------:|-----------:|--------------|-------|
| A | `How Do Airplanes Fly? (The 1901 Wind Tunnel)` | 44 | 0 | **Main (`Rules 1, 15, 23, 26`):** Compact `≤50 chars`, exact autocomplete question `"how do airplanes fly"` first + concrete 1901 wind tunnel twist | **Keep (Primary Proposal)** |
| B | `Wright Brothers First Flight: The 1901 Wind Tunnel` | 50 | 0 | **Test & Compare (`J3224`, `Rules 15, 23, 26`):** Compact `≤50 chars`, exact `J3224` Lead Film 4 query `"wright brothers first flight"` + 1901 wind tunnel | **Keep (T&C Arm 2)** |
| C | `How Did the Wright Brothers Solve Flight? (1901)` | 48 | 0 | **Rule 1/15 Variant (`≤50 chars`):** Direct discovery question + 1901 date hook | **Keep (T&C Arm 3)** |
| Reject | `Aerodynamic Lift Coefficients and Control Surfaces \| HOS` | 57 | — | Academic jargon + forbidden series suffix | **Reject** |

---

## 3b. Script reviewer (blocking before VO — not run; proposal only)

- [ ] `SOURCES.md` exact quotes + `facts` lane verification completed (required before script lock)
- [ ] Score ≥ **90 / 100** (`npm run review:script`)
