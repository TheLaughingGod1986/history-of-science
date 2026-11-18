# Pre-Build Search & Neighbour Audit — `117_May-Gibson-VanWassenbergh-Why-Dont-Woodpeckers-Get-Concussions` (`HOS:117` Proposal)

> **RULE-E GO & RULE G STATUS (`J2963` / `J2966`, `2026-11-16`):**
> - **Rule-E Verdict (`J2966`):** **GO (`95.5 / 100` · `9.55 / 10` Opportunity Score)** — Pre-cleared in `jobs/WIP.json` `next_hos` under **Rule G** (`4 / 4` active HOS slots full: `008`, `009`, `010`, `013`).
> - **Claims Verification Guard:** All historical and scientific claims below are **UNVERIFIED** working notes and must be sourced with verbatim primary-source quotes in `SOURCES.md` and checked by the `facts` lane (`gemini-agy`) when an active HOS WIP slot opens, before any script lock, VO, or picture spend.

## 1. The Discovery Story (Person, Date & Twist — UNVERIFIED)

- **Familiar phenomenon:** How a woodpecker slams its beak into solid wood 20 times a second at `1,200 g` without suffering a concussion or brain damage.
- **Person, place & date:**
  - **Philip R. A. May & Joaquin M. Fuster** (with **Paul Newman, Joe Haber & Ada Hirschman**, UCLA, **28 February 1976** *The Lancet* `307(7957): 454–455` & **June 1979** *Archives of Neurology* `36(6): 370–373`): film an acorn woodpecker (*Melanerpes formicivorus*) at `2,000 frames per second`, measuring `~6–7 m/s` impact speed, `0.5–1.0 ms` deceleration duration, and `1,000–1,200 g` impact decelerations (`~10–17×` the human concussion threshold) along a straight-line trajectory that avoids rotational shearing, launching 45 years of textbook and bio-engineering claims (**Lorna J. Gibson**, **2006** *Journal of Zoology* `270(3): 462–465`; **Sang-Hee Yoon & Sungmin Park**, **2011** *Bioinspiration & Biomimetics* `6(1): 016003`; **Lizhen Wang, Ming Zhang & Yubo Fan et al.**, **26 October 2011** *PLoS ONE* `6(10): e26490`) that spongy cranial bone and the wrap-around hyoid tongue bone act as mechanical **shock absorbers**.
  - **Sam Van Wassenbergh** (with **Erica J. Ortlieb, Maja Mielke, Christine Böhmer, Anick Abourachid & Peter Aerts**, University of Antwerp, **14/25 July 2022**, *Current Biology* `32(14): 3189–3194.e3`): uses `4,000 fps` video tracking across `109` strikes in three woodpecker species (*Dryocopus martius*, *Dendrocopos major*, *Dryobates minor*) and lumped-parameter spring-mass models to prove that the skull absorbs **zero shock** between beak and brain (because a cushion inside a hammer would waste kinetic energy and force the bird to peck harder), and that woodpeckers survive because their tiny (`~1.5–4 g`), tightly packed brains generate roughly **one-seventh (`~14%`) the intracranial pressure** ($\Delta P \propto \rho \cdot a \cdot L$) of a human brain at the same deceleration (requiring `~4,600 g` or `~2×` strike speed to reach human concussion pressure).

---

## 2. Search-First Demand Check (`LEARNINGS.md` Rule 26, Retrieved `2026-11-16`)

- **Exact signed-out YouTube autocomplete phrases (`autocomplete = yes`):** `"why don't woodpeckers get concussions"`, `"how do woodpeckers not get brain damage"`, `"woodpecker tongue around brain"`
  - **Ranking Video 1:** `bqBxbMWd8O0` — *Why Don’t Woodpeckers Get Concussions?* (`Be Smart`, **`1,906,076–1,906,077` views**, retrieved `2026-11-16`)
  - **Ranking Video 2:** `aN5s3KV95wY` — *Why Don't Woodpeckers Get Concussions?* (`Nature Lens`, **`666,803` views**, retrieved `2026-11-16`; plus `SciShow Kids` `tJizlKZizps` **`263,813` views**, `SciShow` `Mgd-xdhjrAc` **`164,025` views**, `Wim Spronk` `xRS_4OgP7-w` **`81,258` views**, `Danny's Dose` `6MtJd8pgQq0` **`52,323` views**, `Natural History Museum` `kYMAKChBMj8` **`39,824` views**, and `MITx Videos` `3pnCVwQRxBQ` **`25,430` views**)
- **Decision:** Candidate primary title = `Why Don't Woodpeckers Get Concussions? (The Shock-Pad Myth)` (Title A, `59 chars ≤ 70`) / compact `Rule 15` (`≤50 chars`) option `Why Don't Woodpeckers Get Concussions? (1,200g)` (Title D, `47 chars`) / `Why Don't Woodpeckers Get Concussions? The 1,200g Mystery` (Title C, `57 chars`, exact phrase first)
- **Candidate description first 100 chars (unverified until `SOURCES.md` check):** `Why don't woodpeckers get concussions at 1,200g? A 2022 high-speed test disproved the shock-pad myth.`

---

## 2b. Neighbour pass (blocking · `STUDIO_PLAYBOOK.md` §2 Step 4, Retrieved `2026-11-16`)

Saved in [`evidence_2026-11-16_neighbours.json`](evidence_2026-11-16_neighbours.json) (`bigCount = 4` strictly on-topic education videos `≥1M` views, `hasTed = true`, `gate = PASS`, `0` off-topic rows across all `21` education neighbours) and [`evidence_2026-11-16_public_search.json`](evidence_2026-11-16_public_search.json):

| # | Views (`2026-11-16`) | Channel (internal) | id & URL | Title | Subject words we reuse |
|---:|------:|--------------------|----------|-------|------------------------|
| 1 | `6,880,115` | CrashCourse (`neighbours.py`) | [`rDGqkMHPDqE`](https://youtu.be/rDGqkMHPDqE) | *The Skeletal System: Crash Course Anatomy & Physiology #19* | `skull`, `bone`, `spongy bone`, `skeleton` |
| 2 | `2,561,046` | TED-Ed ★ (`neighbours.py`) | [`xvjK-4NXRsM`](https://youtu.be/xvjK-4NXRsM) | *What happens when you have a concussion? - Clifford Robbins* | `concussion`, `brain`, `impact`, `skull` |
| 3 | `1,906,077` | Be Smart (`neighbours.py` & `public_search.py`) | [`bqBxbMWd8O0`](https://youtu.be/bqBxbMWd8O0) | *Why Don’t Woodpeckers Get Concussions?* | `why don't woodpeckers get concussions`, `1200 g`, `hyoid bone`, `brain` |
| 4 | `1,736,916` | Amoeba Sisters (`neighbours.py`) | [`m26gr04HIVE`](https://youtu.be/m26gr04HIVE) | *Skeletal System* | `bone structure`, `skull`, `protection` |
| 5 | `666,803` | Nature Lens (`public_search.py`) | [`aN5s3KV95wY`](https://youtu.be/aN5s3KV95wY) | *Why Don't Woodpeckers Get Concussions?* | `woodpecker concussion`, `tongue around skull`, `shock absorber` |
| 6 | `306,193` | TEDx Talks ★ (`neighbours.py`) | [`5nBqLwg2Eug`](https://youtu.be/5nBqLwg2Eug) | *Brain concussion - Shake it and you break it \| Steven Laureys \| TEDxLiège* | `brain concussion`, `impact`, `deceleration` |
| 7 | `305,324` | TED ★ (`neighbours.py`) | [`druJDI6hiiY`](https://youtu.be/druJDI6hiiY) | *Why helmets don't prevent concussions -- and what might \| David Camarillo* | `helmets`, `concussions`, `rotational force`, `shock` |
| 8 | `263,813` | SciShow Kids (`neighbours.py`) | [`tJizlKZizps`](https://youtu.be/tJizlKZizps) | *Why Don't Woodpeckers' Heads Hurt?* | `woodpecker`, `beak`, `skull`, `brain` |
| 9 | `164,025` | SciShow (`neighbours.py`) | [`Mgd-xdhjrAc`](https://youtu.be/Mgd-xdhjrAc) | *Woodpecker Heads are Helmets...AND Hammers* | `woodpecker heads`, `hammers`, `shock absorber myth`, `2022` |
| 10 | `81,258` | Wim Spronk (`public_search.py`) | [`xRS_4OgP7-w`](https://youtu.be/xRS_4OgP7-w) | *How the Woodpecker's tongue wraps around its brain* | `woodpecker tongue around brain`, `hyoid bone` |
| 11 | `73,573` | TED ★ (`neighbours.py`) | [`ZLiUelSu7s8`](https://youtu.be/ZLiUelSu7s8) | *Can I have your brain? The quest for truth on concussions and CTE \| Chris Nowinski* | `concussions`, `brain injury`, `impact` |
| 12 | `39,824` | Natural History Museum (`public_search.py`) | [`kYMAKChBMj8`](https://youtu.be/kYMAKChBMj8) | *Why Don't Woodpeckers Get Brain Damage? \| Natural History Museum* | `why don't woodpeckers get brain damage`, `skull` |

**Proposed subject-only tags (8 tags, zero channel names):**  
`why don't woodpeckers get concussions, how do woodpeckers not get brain damage, woodpecker tongue around brain, woodpecker skull shock absorber myth, sam van wassenbergh woodpecker, 1200g impact biomechanics, animal adaptations explained, history of science experiments`

---

## 3. Title ABCD (score before VO)

| | Title | Chars | Collisions (`2026-11-16`) | Role & Notes | Keep? |
|---|-------|------:|-----------:|--------------|-------|
| A | `Why Don't Woodpeckers Get Concussions? (The Shock-Pad Myth)` | 59 | 0 | **Main (`LEARNINGS.md` Rules 1, 23, 26):** Starts verbatim with exact autocomplete question `"why don't woodpeckers get concussions"` + shock-pad myth twist | **Keep (Primary Proposal)** |
| B | `Woodpecker Skulls Have No Shock Absorber (The 2022 Proof)` | 57 | 0 | **Test & Compare (`Rule 23`):** Leads with the zero-shock-absorber reversal + 2022 high-speed proof | **Keep (T&C Arm 2)** |
| C | `Why Don't Woodpeckers Get Concussions? The 1,200g Mystery` | 57 | 0 | **Rule 26 Variant (`≤70 chars`):** Starts verbatim with exact autocomplete phrase + `1,200g` stakes | **Keep (T&C Arm 3)** |
| D | `Why Don't Woodpeckers Get Concussions? (1,200g)` | 47 | 0 | **Compact `Rule 15` (`≤50 chars`) & `Rule 26` Option:** Exact autocomplete phrase first + `1,200g` stakes in `47 chars ≤ 50` | **Keep (Compact Option)** |
| Reject | `Cranial Kinematics and Intracranial Pressure in Picidae \| HOS` | 61 | — | Academic jargon + forbidden series suffix | **Reject** |

---

## 3b. Script reviewer (blocking before VO — not run; proposal only)

- [x] Rule-E topic go/no-go review passed (`J2966`, **GO `95.5 / 100`**, [`TOPIC_GO_NO_GO_SHEET.md`](TOPIC_GO_NO_GO_SHEET.md) & [`TOPIC_OPPORTUNITY_SCORE.md`](TOPIC_OPPORTUNITY_SCORE.md))
- [ ] `SOURCES.md` exact quotes + `facts` lane verification completed (required before script lock when an active HOS WIP slot opens)
- [ ] Score ≥ **90 / 100** (`npm run review:script`)
