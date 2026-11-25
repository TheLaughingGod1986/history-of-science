# Pre-build Search & Packaging Audit — `HOS:132` (`132_Zachariasen-Zanotto-Pilkington-Why-Is-Glass-Transparent`)

> **Status (`J3409`, `2026-11-23`):** Draft pre-build audit completed during Rule-E topic go/no-go review (**GO `95.1 / 100` in `jobs/WIP.json` `next_hos` under Rule G**). Active `WIP.json["active"]` holds `4 / 4` HOS slots (`008`, `009`, `010`, `013`). **Zero production spend; all historical and scientific claims remain UNVERIFIED** pending an active HOS WIP slot, verbatim primary-source quotes in `SOURCES.md`, and `facts` lane (`gemini-agy`) verification before script lock.

---

## Episode

| Field | Value |
|-------|-------|
| ID / slug | `HOS:132` · `132_Zachariasen-Zanotto-Pilkington-Why-Is-Glass-Transparent` |
| Working title (Primary A) | `Why Is Glass Transparent? (The Quantum Gap)` (`43 chars ≤ 50`, `0` exact collisions) |
| Date pulled | `2026-11-23` (`public_search.py` & `neighbours.py`, signed-out YouTube GB; £0 paid spend) |
| Credits used (approx) | `£0.00` (topic proposal & Rule-E review only) |
| Brand guardrails | Wonder over fearbait · no conspiracy · HOS lane (a familiar everyday object — a glass window — and the discoveries that explained why light passes through it) |

---

## 1. Success Targets (This Episode)

| Metric | Target |
|--------|--------|
| Rule-E Opportunity Score | **`95.1 / 100` (`9.51 / 10`) — PASS** |
| Primary keyword demand | `"why is glass transparent"` (`autocomplete = yes`, backed by `5.03M` TED-Ed, `1.85M` Be Smart, `1.53M` Sixty Symbols) |
| Hook promise | Opaque beach sand and clear window glass are built from the same silicon and oxygen atoms — why does visible light glide straight through one while sunburn UVB stops dead? |
| Retention design | 4-act proof-first discovery arc (sand→glass optical-bench proof → Venetian *cristallo* & Zachariasen/Warren random network → midpoint obsidian/quantum band-gap twist → Zanotto's cathedral-glass myth bust → Pilkington's molten-tin float glass) |
| Packaging | 3 painted 3D thumbs (`LIGHT PASSES THROUGH`, `WINDOWS NEVER FLOW`, `MOLTEN TIN`) — zero title-word repeats (§2.5), zero AI-painted text on art (§2.6), readable at `168×94` |

---

## 2. Search-First Demand Check (`LEARNINGS.md` Rule 26, Retrieved `2026-11-23`)

Saved in [`evidence_2026-11-23_public_search.json`](evidence_2026-11-23_public_search.json) (`10` queries, `75` rows, `0` empty searches):

- **Exact signed-out YouTube autocomplete phrases (`autocomplete = yes`):**
  1. `"why is glass transparent"` (`why is glass transparent`, `why is glass clear`)
  2. `"is glass a liquid"` (`is glass a liquid`, `is glass a liquid or a solid`)
  3. `"why does light pass through glass"` (`why does light pass through glass`)
  4. `"how is float glass made"` (`how is float glass made`, `how is plate glass made`, `how is sheet glass made`)
  5. `"how glass is made"` (`10` suggestions in `evidence_2026-11-23_neighbours.json`)
- **Rule 26(a) Two Ranking Videos (`≥10,000` views, saved `2026-11-23`):**
  - **Ranking Video 1:** `VwRLIt6jgdM` — *Why is glass transparent? - Mark Miodownik* (`TED-Ed`, **`5,032,342` views**)
  - **Ranking Video 2:** `FnDP1sjKGfU` — *Glass is Solid… So Why Is It Clear?* (`Be Smart`, **`1,854,079` views**; plus `Veritasium` `2oDXbFcHliM` **`9,814,172`**, `Veritasium` `c6wuh0NRG1s` *Is Glass a Liquid?* **`5,789,606`**, and `Sixty Symbols` `Omr0JNyDBI0` **`1,526,530`**)
- **Candidate primary title:** `Why Is Glass Transparent? (The Quantum Gap)` (`43 chars ≤ 50`, `0` exact collisions)
- **Candidate description first 100 chars (UNVERIFIED until `SOURCES.md`):** `Why is glass transparent when beach sand isn't? Inside the quantum energy gap that lets sunlight pass.`

---

## 2b. Neighbour Pass (Blocking · `STUDIO_PLAYBOOK.md` §2 Step 4, Retrieved `2026-11-23`)

Saved in [`evidence_2026-11-23_neighbours.json`](evidence_2026-11-23_neighbours.json) (`gate = PASS`, `bigCount = 4`, `hasTed = true`, `failedQueries = []`):

| # | Views (`2026-11-23`) | Channel (internal only) | ID & URL | Title | Relevance & Subject Words Reused |
|---:|------:|--------------------|----------|-------|------------------------|
| 1 | `9,814,162` | Veritasium (`neighbours.py`) | [`2oDXbFcHliM`](https://youtu.be/2oDXbFcHliM) | *The Most Important Material Ever Made* | Direct glass history/material; `glass`, `silica`, `transparency`, `lenses` |
| 2 | `5,032,327` | TED-Ed ★ (`neighbours.py`) | [`VwRLIt6jgdM`](https://youtu.be/VwRLIt6jgdM) | *Why is glass transparent? - Mark Miodownik* | Direct transparency physics; `why is glass transparent`, `electrons`, `photons`, `energy gap` |
| 3 | `2,031,710` | TED-Ed ★ (`neighbours.py`) | [`oULkYytYPgs`](https://youtu.be/oULkYytYPgs) | *What is metallic glass? - Ashwini Bharathula* | Adjacent amorphous glass structure; `amorphous solid`, `random atomic network`, `crystal` |
| 4 | `1,854,087` | Be Smart (`neighbours.py`) | [`FnDP1sjKGfU`](https://youtu.be/FnDP1sjKGfU) | *Glass is Solid… So Why Is It Clear?* | Direct transparency physics; `glass is solid`, `clear`, `light`, `sand` |
| 5 | `103,912` | The Science Asylum (`neighbours.py`) | [`wDu0KMdDD1I`](https://youtu.be/wDu0KMdDD1I) | *Why Are Some Things Transparent?* | On-topic `<1M`; `transparent`, `absorption`, `visible light` |

*(Three `<1M` rows in `evidence_2026-11-23_neighbours.json` are transparently excluded as off-topic/tangential: `TED-Ed` `d5_h1VuwD6g` Rapid prototyping Google Glass `466,294`, `Khan Academy` `sv8-y7N0Ryw` Refraction in a glass of water `12,411`, and `TEDx Talks` `dlrNp_Vgw7o` The Alchemy of Glass `1,471`. `0` off-topic rows at `≥1M`. Never use channel names or Google Glass terms in metadata.)*

**Proposed subject-only tags (8 tags, zero channel names):**
`why is glass transparent, why is glass clear, is glass a liquid, why does light pass through glass, quantum band gap glass, how is float glass made, medieval cathedral glass myth, how sand becomes glass`

---

## 3. Title ABC (Score Before VO)

| | Title | Chars | Collisions (`2026-11-23`) | Role & Notes | Keep? |
|---|-------|------:|-----------:|--------------|-------|
| A | `Why Is Glass Transparent? (The Quantum Gap)` | 43 | 0 | **Main (`Rules 1, 15, 23, 26`):** Verbatim autocomplete question + crisp quantum twist, `≤50 chars` | **Keep (Primary Proposal)** |
| A1 | `Why Is Glass Transparent? (Made From Opaque Sand)` | 49 | 0 | **Variant (`Rules 15, 26`):** Verbatim search phrase + concrete everyday sand paradox, `≤50 chars` | **Keep (Alt Primary / T&C)** |
| B | `Glass Isn't a Liquid (The Quantum Reason It's Clear)` | 52 | 0 | **T&C Arm 2 (`Rule 23`):** Myth-bust hook + quantum reason, `≤70 chars` | **Keep (T&C Arm 2)** |
| C | `Why Is Glass Transparent? (How Melting Sand Turns Clear)` | 56 | 0 | **T&C Arm 3 (`Rule 26`):** Verbatim search phrase + process curiosity, `≤70 chars` | **Keep (T&C Arm 3)** |
| Reject | `Amorphous Silicon Dioxide Electronic Band Gaps \| History of Science` | 68 | — | Textbook jargon + forbidden series suffix | **Reject** |

---

## 3b. Script Reviewer & Gates (Blocking Before VO — Not Run Yet Under Rule G)

- [x] Rule-E topic go/no-go review PASS (`J3409`, `95.1 / 100` GO in `next_hos` under Rule G, `2026-11-23`)
- [ ] `SOURCES.md` exact primary-source quotes + `facts` lane (`gemini-agy`) completed (required before script lock)
- [ ] Score ≥ **90 / 100** (`npm run review:script`) and `npm run gate:episode` PASS
- [ ] Live vidIQ keyword/title score check when promoted from `next_hos` into active WIP

---

## 4. Retention & Packaging Plan (`7–9 min`, 4 Acts + Cold Open)

- **0:00–0:05:** Opaque golden beach sand melts in a white-hot crucible into a clear glass sheet; sunlight passes straight through.
- **0:05–0:15 (Proof-First Apparatus):** Side-by-side optical bench showing visible sunlight gliding through window glass while sunburn UVB stops dead at the pane (no meta-promise).
- **Act I:** Venetian *cristallo* (~1450) → Zachariasen's 1932 theoretical continuous random network & Warren's X-ray diffraction confirmation.
- **Act II (Midpoint Twist):** *"Case closed? Wrong."* Why is obsidian volcanic glass black? Short-range $\text{Si–O}$ bonding, quantum energy gaps (`~9 eV` pure fused silica vs `~3.9–4.1 eV` soda-lime window glass UVB cutoff vs `~1.8–3.1 eV` visible light).
- **Act III:** Zanotto (1998/1999) busts the slow-flowing medieval cathedral-glass myth (`>13.8B`-year universe age) + uneven hand-blown cylinder/crown glass panes.
- **Act IV:** Alastair Pilkington's 1952 dishwashing spark → 1959 molten-tin float glass revolution.
- **Shorts (`Ben 19 Nov 16–19 s rules`):** `S01` *Is Medieval Cathedral Glass Really a Slow Liquid?* (`49 chars`, `0` collisions) · `S02` *Why Does Window Glass Block Sunburn UV Rays?* (`44 chars`, `0` collisions).
