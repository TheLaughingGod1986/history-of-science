# Pre-Build Search & Neighbour Audit — `116_Darwin-Cannon-Hsu-Why-Do-We-Get-Goosebumps` (`HOS:116` Proposal)

> **RULE-E GO & RULE G STATUS (`J2963` / `J2965`, `2026-11-17`):**
> - **Rule-E Verdict (`J2965`):** **GO (`95.5 / 100` · `9.55 / 10` Opportunity Score)** — Pre-cleared in `jobs/WIP.json` `next_hos` under **Rule G** (`4 / 4` active HOS slots full: `008`, `009`, `010`, `013`).
> - **Claims Verification Guard:** All historical and scientific claims below are **UNVERIFIED** working notes and must be sourced with verbatim primary-source quotes in `SOURCES.md` and checked by the `facts` lane (`gemini-agy`) when an active HOS WIP slot opens, before any script lock, VO, or picture spend.

## 1. The Discovery Story (Person, Date & Twist — UNVERIFIED)

- **Familiar phenomenon:** Why our skin breaks out in goosebumps when we are cold or startled, even though humans lack a thick fur coat.
- **Person, place & date:**
  - **Albert von Kölliker** (1817–1905, Zürich / Würzburg, **1847–1849**) & **Charles Darwin** (1809–1882, Down House, **November 1872**, *The Expression of the Emotions in Man and Animals*, Ch. IV): Kölliker identifies the microscopic smooth muscle attached to mammalian hair follicles (*arrectores pilorum* / *arrector pili*), and Darwin compares human goosebumps (*cutis anserina*) to fur-bristling in mammals and feather-fluffing in birds, concluding that in nearly hairless humans the reflex is a **useless vestigial leftover**.
  - **Walter Bradford Cannon** (1871–1945, Harvard Medical School, **1915**, *Bodily Changes in Pain, Hunger, Fear and Rage* & **1929** sympathectomy studies): maps how the **sympathetic nervous system** and adrenaline drive involuntary piloerection during cold or fear ("fight-or-flight"), cementing a century of textbook consensus that the circuit ends at the muscle.
  - **Ya-Chieh Hsu & Yulia Shwartz** (Harvard University, **online 16 July 2020 / print 20 August 2020**, *Cell* `182(3):578–593.e19`): use transmission electron microscopy and genetic knockouts to discover that the sympathetic nerve wraps directly around **hair-follicle stem cells** in synapse-like junctions, and that the *arrector pili* muscle is the indispensable **structural bridge** holding the nerve against those stem cells so sustained cold triggers **norepinephrine** release (`ADRB2`) to wake dormant stem cells and grow new hair.

---

## 2. Search-First Demand Check (`LEARNINGS.md` Rule 26, Retrieved `2026-11-16` / `2026-11-17`)

- **Exact signed-out YouTube autocomplete phrases (`autocomplete = yes`):** `"why do we get goosebumps"`, `"why do you get goosebumps"`, `"what causes goosebumps"`, `"arrector pili muscle"`, `"hair follicle"`
  - **Ranking Video 1:** `D95vHi3mQ5I` — *Why Do We Get Goosebumps? | The Dr. Binocs Show* (`Peekaboo Kidz`, **`5,779,906` views**, retrieved `2026-11-17`)
  - **Ranking Video 2:** `-EA2eWZuYDs` — *The Science of Goosebumps and Music Chills* (`AsapSCIENCE`, **`1,976,968` views**, retrieved `2026-11-17`; plus `It's AumSum Time` `TDkDcz5TsVs` **`589,125` views**, `Institute of Human Anatomy` `_WH8ISdxVkQ` **`361,068` views**, `Doctor Myro` `dmA9F9zyioA` **`197,271` views**, `SciShow Kids` `KD78ZlViWt4` **`150,165` views**, `Kenhub - Learn Human Anatomy` `VZ7qgSpBYHY` **`18,503` views**, and `Walter Jahn` `EkZTxbnALoE` **`15,115` views**)
- **Decision:** Candidate primary title = `Why Do We Get Goosebumps? (The 2020 Stem-Cell Twist)` (Title A, `52 chars ≤ 70`) / compact `Rule 15` (`≤50 chars`) option `Why Do We Get Goosebumps? (The Stem-Cell Twist)` (Title A1, `47 chars`) / `Why Do We Get Goosebumps? The Hidden Nerve-Muscle Switch` (Title C, `56 chars`, exact phrase first)
- **Candidate description first 100 chars (unverified until `SOURCES.md` check):** `Why do we get goosebumps without fur? A 2020 Harvard test found they wire nerves to hair stem cells.`

---

## 2b. Neighbour pass (blocking · `STUDIO_PLAYBOOK.md` §2 Step 4, Retrieved `2026-11-17`)

Saved in [`evidence_2026-11-16_neighbours.json`](evidence_2026-11-16_neighbours.json) (`bigCount = 7` strictly on-topic education videos `≥1M` views, `hasTed = true`, `gate = PASS`, `0` off-topic rows) and [`evidence_2026-11-16_public_search.json`](evidence_2026-11-16_public_search.json):

| # | Views (`2026-11-17`) | Channel (internal) | id & URL | Title | Subject words we reuse |
|---:|------:|--------------------|----------|-------|------------------------|
| 1 | `5,938,648` | CrashCourse (`neighbours.py`) | [`Orumw-PyNjw`](https://youtu.be/Orumw-PyNjw) | *The Integumentary System, Part 1 - Skin Deep: Crash Course Anatomy & Physiology #6* | `skin`, `hair follicle`, `arrector pili`, `goosebumps` |
| 2 | `5,779,906` | Peekaboo Kidz (`public_search.py`) | [`D95vHi3mQ5I`](https://youtu.be/D95vHi3mQ5I) | *Why Do We Get Goosebumps? \| The Dr. Binocs Show* | `why do we get goosebumps`, `cold`, `adrenaline` |
| 3 | `5,584,277` | TEDx Talks ★ (`neighbours.py`) | [`rXNt_X5F67I`](https://youtu.be/rXNt_X5F67I) | *Healthy skin starts from within \| Barbara Paldus \| TEDxPrague* | `skin`, `cells`, `regeneration` |
| 4 | `5,439,161` | TED-Ed ★ (`neighbours.py`) | [`wd18yfQqa8A`](https://youtu.be/wd18yfQqa8A) | *Why do we have hair in such random places? - Nina G. Jablonski* | `why do we have hair`, `evolution`, `fur`, `skin` |
| 5 | `3,540,388` | TED-Ed ★ (`neighbours.py`) | [`_r4c2NT4naQ`](https://youtu.be/_r4c2NT4naQ) | *The science of skin color - Angela Koine Flynn* | `science of skin`, `cells`, `evolution` |
| 6 | `2,362,721` | TED-Ed ★ (`neighbours.py`) | [`OxPlCkTKhzY`](https://youtu.be/OxPlCkTKhzY) | *The science of skin - Emma Bryce* | `the science of skin`, `epidermis`, `dermis`, `follicles` |
| 7 | `1,976,968` | AsapSCIENCE (`public_search.py`) | [`-EA2eWZuYDs`](https://youtu.be/-EA2eWZuYDs) | *The Science of Goosebumps and Music Chills* | `goosebumps`, `nervous system`, `evolution` |
| 8 | `1,137,284` | TED ★ (`neighbours.py`) | [`OeGpf1MyM2M`](https://youtu.be/OeGpf1MyM2M) | *5 Skin Health Myths to Stop Believing Now \| Body Stuff with Dr. Jen Gunter* | `skin myths`, `human body` |
| 9 | `1,073,609` | Be Smart (`neighbours.py`) | [`sMCgOQj37IY`](https://youtu.be/sMCgOQj37IY) | *Why Does Hair Grow The Way It Does?* | `hair growth`, `hair follicle`, `stem cells` |
| 10 | `968,998` | TEDx Talks ★ (`neighbours.py`) | [`Rat1n34l_wI`](https://youtu.be/Rat1n34l_wI) | *The hidden brain in your skin \| Claudia Aguirre \| TEDxUCLA* | `skin nerves`, `nervous system`, `hair follicles` |
| 11 | `812,324` | TED-Ed ★ (`neighbours.py`) | [`iCBzEZek5cY`](https://youtu.be/iCBzEZek5cY) | *How long can hair grow? - Maksim Plikus* | `hair follicle`, `stem cells`, `growth cycle` |
| 12 | `150,165` | SciShow Kids (`neighbours.py`) | [`KD78ZlViWt4`](https://youtu.be/KD78ZlViWt4) | *Why Do We Get Goosebumps?* | `why do we get goosebumps`, `tiny muscles`, `fur` |

**Proposed subject-only tags (8 tags, zero channel names):**  
`why do we get goosebumps, what causes goosebumps, arrector pili muscle, hair follicle stem cells, ya chieh hsu goosebumps, charles darwin vestigial organs, sympathetic nervous system skin, history of science experiments`

---

## 3. Title ABC (score before VO)

| | Title | Chars | Collisions (`2026-11-17`) | Role & Notes | Keep? |
|---|-------|------:|-----------:|--------------|-------|
| A | `Why Do We Get Goosebumps? (The 2020 Stem-Cell Twist)` | 52 | 0 | **Main (`LEARNINGS.md` Rules 1, 23, 26):** Starts verbatim with exact autocomplete question `"why do we get goosebumps"` + 2020 Harvard stem-cell twist | **Keep (Primary Proposal)** |
| A1 | `Why Do We Get Goosebumps? (The Stem-Cell Twist)` | 47 | 0 | **Compact `Rule 15` (`≤50 chars`) & `Rule 26` Option:** Exact autocomplete phrase first + `47 chars ≤ 50` | **Keep (Compact Option)** |
| B | `Goosebumps Aren't Useless (The Hidden Hair-Growth Nerve)` | 56 | 0 | **Test & Compare (`Rule 23`):** Leads with the vestigial myth reversal + hidden hair-growth nerve | **Keep (T&C Arm 2)** |
| B1 | `Goosebumps Aren't Useless (The Stem-Cell Twist)` | 47 | 0 | **Compact `Rule 15` (`≤50 chars`) T&C Option:** Vestigial myth reversal in `47 chars ≤ 50` | **Keep (Compact T&C Option)** |
| C | `Why Do We Get Goosebumps? The Hidden Nerve-Muscle Switch` | 56 | 0 | **Rule 26 Variant (`≤70 chars`):** Starts verbatim with exact autocomplete phrase + nerve-muscle switch story | **Keep (T&C Arm 3)** |
| Reject | `Sympathetic Noradrenergic Regulation of Hair Follicle Stem Cells \| HOS` | 70 | — | Academic jargon + forbidden series suffix | **Reject** |

---

## 3b. Script reviewer (blocking before VO — not run; proposal only)

- [x] Rule-E topic go/no-go review passed (`J2965`, **GO `95.5 / 100`**, [`TOPIC_GO_NO_GO_SHEET.md`](TOPIC_GO_NO_GO_SHEET.md) & [`TOPIC_OPPORTUNITY_SCORE.md`](TOPIC_OPPORTUNITY_SCORE.md))
- [ ] `SOURCES.md` exact quotes + `facts` lane verification completed (required before script lock when an active HOS WIP slot opens)
- [ ] Score ≥ **90 / 100** (`npm run review:script`)
