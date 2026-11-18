# Topic Opportunity Score — `HOS:107` (`107_Tswett-Willstatter-Autumn-Leaves-Chlorophyll`)

> **Rule-E Topic Review Verdict (`J2837`, 14 Nov 2026):** **GO (`9.00 / 10` · `90 / 100` Opportunity Score)** — Pre-cleared in `jobs/WIP.json` `next_hos` behind `HOS:106` under Rule G (recommended late-August / September seasonal release window).
> **Unverified Claims Guard:** All historical and scientific claims in `TOPIC.md` §2 and `PRE_BUILD_VIDIQ_AUDIT.md` remain **UNVERIFIED** working notes and are **NOT CLEARED FOR NARRATION OR SHORT OPENS** until an active HOS WIP slot opens, exact primary-source quotes are recorded in `SOURCES.md`, and the `facts` lane (`gemini-agy`) verifies every claim.

**Candidate topic:** Why Do Leaves Change Colour? — Pelletier & Caventou's 1817 naming of chlorophyll, Mikhail Tswett's 1903 Warsaw chalk-tube column separating green leaf extract into emerald and golden-yellow rings (inventing chromatography), Richard Willstätter's 1915 Nobel work on magnesium at the core of chlorophyll, and why yellow carotenoids hide in leaves all summer while red anthocyanins are made new in autumn (`HOS:107`)
**Primary search phrase:** `"why do leaves change colour"` / `"why do leaves change color in the fall"` / `"what is chromatography"` / `"chlorophyll"` (signed-out YouTube GB `public_search.py` autocomplete = **yes** on all four, retrieved `2026-11-14`)
**Date:** `2026-11-14` (`J2835` topic proposal · `J2837` Rule-E review by `macbook`)

---

## 1. Weighted Rubric (`00_Brand/Channel-Setup/templates/TOPIC_OPPORTUNITY_SCORE.md`)

| Dimension | Weight | Score (1–10) | Weighted | Evidence & Rationale |
|-----------|--------|--------------|----------|----------------------|
| **1. Evergreen search intent** | 25% | **8.5** | **2.125** | `"why do leaves change colour"` (`10` autocomplete suggestions), `"why do leaves change color"` (`10` suggestions), `"why do leaves change color in the fall"` (`6` suggestions), `"what is chromatography"` (`10` suggestions), and `"chlorophyll"` (`10` suggestions) all autocomplete (`suggest = yes`) in signed-out YouTube GB (`evidence_2026-11-14_public_search.json`). While leaf-colour queries peak seasonally in September–November (`SciShow Kids` `1,916,547` & `1,850,236` views, `MinuteEarth` `1,558,957` views), pairing the topic with **chromatography** (`Cognito` `1,532,858` views, `Khan Academy` `1,328,589` views, `It's AumSum Time` `2,116,418` views) anchors year-round GCSE / AP Chemistry / MCAT curriculum search (`Rule 28`). Placed behind `HOS:106` in `next_hos` with a late-August / September release window recommendation. |
| **2. Competition gap (wonder / clarity vs dry or crowding)** | 20% | **9.0** | **1.800** | Top leaf-colour videos (`SciShow Kids` `3:22`, `MinuteEarth` `2:02`, `Peekaboo Kidz` `5:49`) are 2–5 minute children's explainers that never name how scientists actually separated the hidden pigments; top chromatography videos (`Cognito`, `Khan Academy`, `Freesciencelessons`) are dry GCSE/MCAT exam whiteboard lessons that never tell Mikhail Tswett's 1903 Warsaw chalk-tube story or his rivalry with Richard Willstätter. None combines the everyday autumn leaf question with the 1903 chalk column in a 7–9 minute 3D historical detective film. |
| **3. Narrative & visual arc (3D world + diagram clarity)** | 20% | **9.5** | **1.900** | Built for HOS's proof-first `0:05–0:15` rule and *Teach on screen* graphics: (1) crushed emerald spinach/maple leaf juice poured into Tswett's 1903 glass column of white chalk (`CaCO3`) and separating before the viewer's eyes into green, yellow-green, and golden-orange rings (`0:05–0:15`), (2) Pelletier & Caventou's 1817 Paris apothecary flasks, (3) Willstätter's Zurich laboratory isolating the porphyrin ring with a central magnesium (`Mg`) atom, and (4) Tswett's 25-year vindication in 1931. |
| **4. Brand & guardrail fit** | 20% | **9.5** | **1.900** | Pure History of Science discovery story linking a universal ground-level phenomenon (`Rule 31`) to a foundational laboratory instrument (`chromatography`). Zero overlap with `HOS:006` (which covers van Helmont's willow tree mass, Priestley's mint, Ingenhousz's bubbles, and Calvin's `14C` carbon fixation) or `ideas/070` (Sumner vs Willstätter on protein enzymes). Adult historical framing avoids any `Made for Kids` tone. |
| **5. Series / cluster potential** | 15% | **8.5** | **1.275** | Forms the **Botany & Analytical Chemistry Cluster** alongside `HOS:006` (*The Willow Tree That Was Made of Air*, live), `HOS:105` (*How Does a Venus Flytrap Count to Two?*, in `next_hos`), and `ideas/081` (*How Does Water Climb a 100-Metre Tree?* — Dixon & Joly cohesion-tension). |
| **Total** | **100%** | — | **`9.00 / 10` (`90 / 100`)** | **GO (`≥ 7.5` threshold exceeded by `+1.50` points; ordered behind `HOS:106` at `9.40 / 10`)** |

**Rule:** Proceed (`GO`) if **Total ≥ 7.5** and **Brand fit ≥ 8**. Both pass (`9.00 / 10` total, `9.5 / 10` brand fit).

---

## 2. Education Neighbour Gate (`neighbours.py` + `public_search.py`, Retrieved `2026-11-14`)

Saved in [`evidence_2026-11-14_neighbours.json`](evidence_2026-11-14_neighbours.json) (`bigCount = 5`, `hasTed = true`, `gate = PASS`) and [`evidence_2026-11-14_public_search.json`](evidence_2026-11-14_public_search.json):

| # | Channel | Views (`2026-11-14`) | Video ID & URL | Title | Source File |
|---:|---|---:|---|---|---|
| 1 | **SciShow Kids** | `1,916,547` | [`xB2DiiAOpCg`](https://youtu.be/xB2DiiAOpCg) | *The Science of Fall \| Compilation \| SciShow Kids* | `neighbours.json` (Tier 2, on-subject) |
| 2 | **SciShow Kids** | `1,850,236` | [`Xk4-6II8l5Q`](https://youtu.be/Xk4-6II8l5Q) | *Why Do Leaves Change Colors in the Fall? \| Biology for Kids \| SciShow Kids* | `neighbours.json` (Tier 2) + `public_search.json` |
| 3 | **MinuteEarth** | `1,558,957` | [`JWva5AaDkXw`](https://youtu.be/JWva5AaDkXw) | *The Real Reason Leaves Change Color In the Fall* | `neighbours.json` (Tier 2) + `public_search.json` |
| 4 | **Cognito** | `1,532,858` | [`TdJ57SQ6GAQ`](https://youtu.be/TdJ57SQ6GAQ) | *GCSE Chemistry - Paper Chromatography* | `public_search.json` (Tier 2 in `neighbours.py`) |
| 5 | **Khan Academy** | `1,328,589` | [`SnbXQTTHGs4`](https://youtu.be/SnbXQTTHGs4) | *Basics of chromatography \| Chemical processes \| MCAT \| Khan Academy* | `public_search.json` (Tier 2 in `neighbours.py`) |
| 6 | **TED-Ed ★** (adjacent on `006`) | `2,218,164` | [`eo5XndJaz-Y`](https://youtu.be/eo5XndJaz-Y) | *The simple story of photosynthesis and food - Amanda Ooten* | Adjacent plant/chlorophyll `TED-Ed` (`006`) |
| 7 | **TED-Ed ★** (colour query) | `8,462,196` | [`gKfjHTk8KrY`](https://youtu.be/gKfjHTk8KrY) | *History's deadliest colors - J. V. Maranto* | `neighbours.json` (`ted-ed chlorophyll`, Tier 1) |
| 8 | **TED-Ed ★** (colour query) | `1,109,978` | [`UZ5UGnU7oOI`](https://youtu.be/UZ5UGnU7oOI) | *What is color? - Colm Kelleher* | `neighbours.json` (`ted-ed chlorophyll`, Tier 1) |
| 9 | **SciShow** | `269,611` | [`rwA1QVsbD6g`](https://youtu.be/rwA1QVsbD6g) | *Why Do Leaves Change Color and Fall?* | `neighbours.json` (Tier 2) + `public_search.json` |

---

## 3. Cluster Sketch (3 Adjacent Episodes)

1. **`HOS:107` (This Episode):** *Why Do Leaves Change Colour? (A Chalk Tube Showed Why)* — Pelletier & Caventou's 1817 chlorophyll, Mikhail Tswett's 1903 Warsaw chalk column separating hidden yellow carotenoids from green chlorophyll, and Richard Willstätter's 1915 Nobel pigment chemistry.
2. **`HOS:006` (`006_Trees-Are-Made-Of-Air`, live):** *The Willow Tree That Was Made of Air* — Van Helmont's 1648 willow tree, Priestley's mint, Ingenhousz's sunlit leaf bubbles, and Calvin's `14C` carbon fixation.
3. **`HOS:105` (`105_Darwin-Burdon-Sanderson-Hodick-Venus-Flytrap`, in `next_hos`):** *How Does a Venus Flytrap Count to Two?* — Darwin's 1875 carnivorous plant experiments, Burdon-Sanderson's plant action potential, and the two-touch calcium clock.
4. **`HOS:081` (`081_Hales-Boehm-Dixon-Joly-How-Water-Climbs-Tall-Trees`, in `ideas/`):** *How Does Water Climb a 100-Metre Tree Without a Pump?* — Stephen Hales's root pressure, Josef Böhm's mercury tubes, and Dixon & Joly's 1894 cohesion-tension proof.
