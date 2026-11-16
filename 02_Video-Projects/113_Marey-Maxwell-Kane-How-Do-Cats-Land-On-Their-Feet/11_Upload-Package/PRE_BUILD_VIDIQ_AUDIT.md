# Pre-Build Search & Neighbour Audit — `113_Marey-Maxwell-Kane-How-Do-Cats-Land-On-Their-Feet` (`HOS:113` Proposal)

> **PROPOSAL STATUS (`J2935`, `2026-11-16`):** Waiting in `jobs/WIP.json` `next_hos` (Rule G). All historical and scientific claims below are **UNVERIFIED** working notes and must be sourced in `SOURCES.md` and checked by the `facts` lane before script lock.

## 1. The Discovery Story (Person, Date & Twist — UNVERIFIED)

- **Familiar phenomenon:** How a falling cat flips `180 degrees` in mid-air to land on all four feet with zero external push-off.
- **Person, place & date:**
  - **James Clerk Maxwell** (Trinity College, Cambridge, **1850s–1870s**): tests how little drop height a cat needs to flip upright — highlighting a famous paradox in classical mechanics (how can a body with zero net angular momentum rotate `180°` in mid-air without external torque?).
  - **Étienne-Jules Marey** (1830–1904, Paris Academy of Sciences, **22 October 1894**, *Comptes Rendus* / *Nature*): shoots **`60` photographs per second** with his chronophotographic gun, proving the cat leaves the hands with zero spin and flips by tucking its front legs first while stretching its back legs (changing each half's moment of inertia), then swapping and bending at the waist so net angular momentum stays zero (`L = 0`).
  - **Thomas R. Kane & M. P. Scher** (Stanford University / NASA, **1968–1969**, *International Journal of Solids and Structures*): solve the exact two-cylinder equations of Marey's falling cat to train Apollo astronauts to turn their bodies in zero gravity without firing thrusters.

---

## 2. Search-First Demand Check (`LEARNINGS.md` Rule 26, Retrieved `2026-11-16`)

- **Exact signed-out YouTube autocomplete phrase (`autocomplete = yes`):** `"how do cats land on their feet"` (plus `"why do cats always land on their feet"`)
  - **Ranking Video 1:** `RtWbpyjJqrU` — *Slow Motion Flipping Cat Physics \| Smarter Every Day 58* (`SmarterEveryDay`, **`11,253,700` views**, retrieved `2026-11-16`)
  - **Ranking Video 2:** `Xs87FijgVaA` — *Why a cat always lands on its feet* (`Vox`, **`2,534,162` views**, retrieved `2026-11-16`; plus `BBC` `sepYP_knGWc` **`442,041` views**, `Explore & Discover` `qjf472A83N8` **`198,955` views**, and `The Telegraph` `0u26gpLmKe4` **`171,040` views**)
- **Decision:** Candidate primary title = `How Do Cats Land on Their Feet? (The 1894 Camera Twist)` (Title A, `55 chars`) / `How Do Cats Land on Their Feet? The Zero-Spin Physics Twist` (Title C, `59 chars`, exact phrase first)
- **Candidate description first 100 chars (unverified until `SOURCES.md` check):** `How do cats land on their feet with zero push-off, and how did an 1894 high-speed camera prove it?`

---

## 2b. Neighbour pass (blocking · `STUDIO_PLAYBOOK.md` §2 Step 4, Retrieved `2026-11-16`)

Saved in [`evidence_2026-11-16_neighbours.json`](evidence_2026-11-16_neighbours.json) and [`evidence_2026-11-16_public_search.json`](evidence_2026-11-16_public_search.json):

| # | Views (`2026-11-16`) | Channel (internal) | id & URL | Title | Subject words we reuse |
|---:|------:|--------------------|----------|-------|------------------------|
| 1 | `13,421,747` | TED-Ed ★ (`neighbours.py`) | [`sI8NsYIyQ2A`](https://youtu.be/sI8NsYIyQ2A) | *Why do cats act so weird? - Tony Buffington* | `why do cats`, `reflexes`, `evolution` |
| 2 | `11,253,700` | SmarterEveryDay (`neighbours.py` & `public_search.py`) | [`RtWbpyjJqrU`](https://youtu.be/RtWbpyjJqrU) | *Slow Motion Flipping Cat Physics \| Smarter Every Day 58* | `how do cats land on their feet`, `flipping cat physics`, `slow motion`, `angular momentum` |
| 3 | `10,537,826` | TED-Ed ★ (`neighbours.py`) | [`Jsj-hDW9bS8`](https://youtu.be/Jsj-hDW9bS8) | *The history of the world according to cats - Eva-Maria Geigl* | `cats`, `history`, `biology` |
| 4 | `4,609,915` | TED-Ed ★ (`neighbours.py`) | [`jdrNjHPYKz4`](https://youtu.be/jdrNjHPYKz4) | *Why do cats have vertical pupils? - Emma Bryce* | `why do cats`, `anatomy`, `predator` |
| 5 | `2,600,485` | TED-Ed ★ (`neighbours.py`) | [`l5VgOdgptRg`](https://youtu.be/l5VgOdgptRg) | *The physics of the "hardest move" in ballet - Arleen Sugano* | `physics`, `angular momentum`, `moment of inertia`, `rotation` |
| 6 | `2,534,162` | Vox (`public_search.py`) | [`Xs87FijgVaA`](https://youtu.be/Xs87FijgVaA) | *Why a cat always lands on its feet* | `why a cat always lands on its feet`, `1894 photographs`, `marey` |
| 7 | `1,865,351` | minutephysics (`neighbours.py`) | [`iWSu6U0Ujs8`](https://youtu.be/iWSu6U0Ujs8) | *What IS Angular Momentum?* | `angular momentum`, `conservation of angular momentum`, `torque` |
| 8 | `568,507` | Khan Academy (`neighbours.py`) | [`nFSMu3bxXVA`](https://youtu.be/nFSMu3bxXVA) | *Angular momentum \| Moments, torque, and angular momentum \| Physics* | `angular momentum`, `torque`, `physics` |

**Proposed subject-only tags (8 tags, zero channel names):**  
`how do cats land on their feet, why do cats always land on their feet, falling cat problem physics, etienne jules marey falling cat, conservation of angular momentum, cat righting reflex, nasa falling cat astronauts, history of physics experiments`

---

## 3. Title ABC (score before VO)

| | Title | Chars | Collisions (`2026-11-16`) | Role & Notes | Keep? |
|---|-------|------:|-----------:|--------------|-------|
| A | `How Do Cats Land on Their Feet? (The 1894 Camera Twist)` | 55 | 0 | **Main (`LEARNINGS.md` Rules 1, 23, 26):** Starts verbatim with exact autocomplete question `"how do cats land on their feet"` + 1894 camera twist | **Keep (Primary Proposal)** |
| B | `The 60-Photo Gun That Solved How Falling Cats Flip` | 50 | 0 | **Test & Compare (`Rule 23`):** Leads with Marey's 60-fps photographic gun + falling cats | **Keep (T&C Arm 2)** |
| C | `How Do Cats Land on Their Feet? The Zero-Spin Physics Twist` | 59 | 0 | **Rule 26 Variant (`≤70 chars`):** Starts verbatim with exact autocomplete phrase `"how do cats land on their feet"` + zero-spin physics twist | **Keep (T&C Arm 3)** |
| Reject | `Non-Holonomic Zero-Angular-Momentum Cat Righting \| History of Science` | 70 | — | Academic jargon + forbidden series suffix | **Reject** |

---

## 3b. Script reviewer (blocking before VO — not run; proposal only)

- [ ] `SOURCES.md` exact quotes + `facts` lane verification completed (required before script lock)
- [ ] Score ≥ **90 / 100** (`npm run review:script`)
