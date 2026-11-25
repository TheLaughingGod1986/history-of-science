# Pre-Build Search & Neighbour Audit — `129_Spencer-Boot-Randall-How-Was-The-Microwave-Invented` (`HOS:129` — Proposal in `next_hos`)

> **PROPOSAL & UNVERIFIED CLAIMS GUARD (`J3270`, `2026-11-22`):** Appended to `jobs/WIP.json` `next_hos` under **Rule G** (`4 / 4` active HOS slots full) and queued for **Rule-E topic go/no-go review**. All historical and scientific claims below are **UNVERIFIED** working notes and must be sourced in `SOURCES.md` and verified through the `facts` lane (`gemini-agy`) before any script lock, VO, or picture spend.

## 1. The Discovery Story (Person, Date & Twist — UNVERIFIED)

- **Familiar phenomenon:** A kitchen microwave oven heats food in seconds while its glass plate and the air inside stay cool — and sparks if you leave a fork inside even though its own walls are metal.
- **Person, place & date:**
  - **John Randall & Harry Boot** (University of Birmingham, **February 1940**): machined the resonant **cavity magnetron**, generating powerful centimetre-wavelength microwaves for airborne wartime radar (brought to the US via the autumn 1940 Tizard Mission).
  - **Percy Spencer** (Raytheon, Massachusetts, **1945**, patent **US 2,495,429** filed **8 October 1945**): standing beside an active magnetron test rig, noticed a peanut candy bar melt in his pocket; tested popcorn kernels and an exploding whole egg inside a pierced metal kettle, then built a sealed reflective box to turn dielectric heating of polar water molecules (`2.45 GHz`) into the **1947 Radarange** (followed by the countertop **1967 Amana Radarange**).

---

## 2. Search-First Demand Check (`LEARNINGS.md` Rule 26 & `J3224` Cluster 3, Retrieved `2026-11-22`)

- **J3224 vidIQ Anglosphere Demand (`05_Analytics/hos/search_research/2026-11-20.md`, £0 extra spend here):** `inventions that changed the world` `35,881`/mo (**US 23%**), `accidental discoveries` `9,367`/mo (comp `39`, **`+93.0%`**), `accidental inventions that changed the world` `8,092`/mo (**`+73.9%`**), **9/10–10/10 US SERP gap**, small-channel proof `Counter Facts Lab` (`1.4K` → `1.5K` `22×`), `Invention Flex` (`6.2K` US → `9.6K` `8.3×`), `Industrial Case Files` (`138` US → `4.7K` `8.6×`).
- **Exact signed-out YouTube autocomplete phrases (`autocomplete = yes`, `2026-11-22`):** `"how was the microwave invented"`, `"how does a microwave work"`, `"who invented the microwave"`, `"percy spencer microwave"`, `"why can't you put metal in a microwave"`.
  - **Ranking Video 1:** `2tdiKTSdE9Y` — *I promise this story about microwaves is interesting.* (`Tom Scott`, **`8,957,052` views**)
  - **Ranking Video 2:** `kp33ZprO0Ck` — *How a Microwave Oven Works* (`engineerguy`, **`5,389,161` views**; plus `Sabin Civil Engineering` **`8,011,520`**, `ElectroBOOM` `OyTmJX_TC84` **`5,795,769`**, `TED-Ed` `ZExGV6jSuBw` **`2,114,632`**, `SciShow` `ZqAZz-JhvYA` **`1,329,055`**, `Weird History Food` `UJBZk88O6BU` **`340,942`**)
- **Candidate primary title:** `How Was the Microwave Invented? (A Radar Accident)` (`50 chars ≤ 50`, `0` exact collisions)
- **Candidate description first 100 chars (unverified until `SOURCES.md`):** `How was the microwave invented? In 1945 a wartime radar tube melted a candy bar in Percy Spencer's pocket.`

---

## 2b. Neighbour Pass (Blocking · `STUDIO_PLAYBOOK.md` §2 Step 4, Retrieved `2026-11-22`)

Saved in [`evidence_2026-11-22_neighbours.json`](evidence_2026-11-22_neighbours.json) and [`evidence_2026-11-22_public_search.json`](evidence_2026-11-22_public_search.json):

| # | Views (`2026-11-22`) | Channel (internal) | id & URL | Title | Subject words we reuse |
|---:|------:|--------------------|----------|-------|------------------------|
| 1 | `8,957,052` | Tom Scott (`neighbours.py`) | [`2tdiKTSdE9Y`](https://youtu.be/2tdiKTSdE9Y) | *I promise this story about microwaves is interesting.* | `microwave`, `cavity magnetron`, `history`, `invention` |
| 2 | `2,114,636` | TED-Ed ★ (`neighbours.py`) | [`ZExGV6jSuBw`](https://youtu.be/ZExGV6jSuBw) | *Why can't you put metal in a microwave? - Aaron Slepkov* | `microwave`, `metal`, `electromagnetic waves`, `sparks` |
| 3 | `1,329,055` | SciShow (`neighbours.py`) | [`ZqAZz-JhvYA`](https://youtu.be/ZqAZz-JhvYA) | *Why Can't I Put Metal in the Microwave?* | `microwave oven`, `metal`, `water molecules`, `heating` |
| 4 | `56,191` | National Geographic (`neighbours.py`) | [`l_M5HzWlM40`](https://youtu.be/l_M5HzWlM40) | *Microwave Oven \| I Didn't Know That* | `microwave oven`, `magnetron`, `Radarange` |

**Proposed subject-only tags (8 tags, zero channel names):**
`how was the microwave invented, how does a microwave work, percy spencer microwave, cavity magnetron radar, why can't you put metal in a microwave, accidental inventions that changed the world, radarange 1947, dielectric heating water molecules`

---

## 3. Title ABC (Score Before VO)

| | Title | Chars | Collisions (`2026-11-22`) | Role & Notes | Keep? |
|---|-------|------:|-----------:|--------------|-------|
| A | `How Was the Microwave Invented? (A Radar Accident)` | 50 | 0 | **Main (`Rules 1, 15, 23, 26`):** Starts verbatim with exact autocomplete question, fits `≤50 chars`, concrete radar-accident twist | **Keep (Primary Proposal)** |
| B | `How Does a Microwave Work? (The 1945 Radar Twist)` | 49 | 0 | **T&C Arm 2 (`Rules 15, 23, 26`):** Leads with huge `"how does a microwave work"` search query + 1945 origin twist, `≤50 chars` | **Keep (T&C Arm 2)** |
| C | `How Was the Microwave Invented? (Percy Spencer's 1945 Magnetron)` | 64 | 0 | **T&C Arm 3 (`Rule 26`):** Exact search phrase + named scientist and apparatus | **Keep (T&C Arm 3)** |
| Reject | `Dielectric Heating via Cavity Magnetron Resonators \| HOS` | 57 | — | Academic jargon + forbidden series suffix | **Reject** |

---

## 3b. Script Reviewer (Blocking Before VO — Not Run; Proposal Only)

- [ ] Rule-E topic go/no-go review PASS
- [ ] `SOURCES.md` exact quotes + `facts` lane verification completed (required before script lock)
- [ ] Score ≥ **90 / 100** (`npm run review:script`)
