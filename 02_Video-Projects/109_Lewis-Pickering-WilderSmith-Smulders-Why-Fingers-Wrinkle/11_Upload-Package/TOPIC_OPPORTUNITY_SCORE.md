# Topic Opportunity Score — `HOS:109` (`109_Lewis-Pickering-WilderSmith-Smulders-Why-Fingers-Wrinkle`)

> **Rule-E Topic Review Verdict (`J2918`, 16 Nov 2026):** **GO (`9.55 / 10` · `95.5 / 100` Opportunity Score)** — Pre-cleared in `jobs/WIP.json` `next_hos` under Rule G.
> **Unverified Claims Guard:** All historical and scientific claims in `TOPIC.md` §4–§5 and `PRE_BUILD_VIDIQ_AUDIT.md` remain **UNVERIFIED** working notes and are **NOT CLEARED FOR NARRATION OR SHORT OPENS** until an active HOS WIP slot opens (`len([x for x in WIP.json["active"] if x.startswith("HOS:")]) < 4`), exact primary-source quotes are recorded in `SOURCES.md`, and the `facts` lane (`gemini-agy`) verifies every claim.

**Candidate topic:** Why Do Fingers Wrinkle in Water? — Thomas Lewis & George Pickering's 1935–1936 London cut-nerve hospital discovery, S. O'Riain's 1973 warm-water clinical nerve test, Einar Wilder-Smith's 2003 laser-Doppler digital vasoconstriction proof, Mark Changizi's 2011 rain-tread watershed hypothesis, and Tom Smulders & Kyriacos Kareklas's 2013 Newcastle wet-marble grip experiment (`HOS:109`)
**Primary search phrase:** `"why do fingers wrinkle in water"` / `"why do fingers prune in water"` (signed-out YouTube GB `public_search.py` autocomplete = **yes** on both, plus `"how skin works"` = **yes** and `"sympathetic nervous system"` = **yes**, retrieved `2026-11-15`)
**Date:** `2026-11-16` (`J2891` evidence pull on Mac mini · `J2918` Rule-E review by `macbook`)

---

## 1. Weighted Rubric (`00_Brand/Channel-Setup/templates/TOPIC_OPPORTUNITY_SCORE.md`)

| Dimension | Weight | Score (1–10) | Weighted | Evidence & Rationale |
|-----------|--------|--------------|----------|----------------------|
| **1. Evergreen search intent** | 25% | **10.0** | **2.50** | `"why do fingers wrinkle in water"` (`4` autocomplete suggestions: `"why do fingers wrinkle in water"`, `"why do fingers get wrinkly in water"`, `"why do my hands wrinkle in water so fast"`, `"why fingers prune in water"`), `"why do fingers prune in water"` (`3` suggestions), `"how skin works"` (`10` suggestions), and `"sympathetic nervous system"` (`10` suggestions) all autocomplete (`suggest = yes`) in signed-out YouTube GB (`evidence_2026-11-15_public_search.json`, `evidence_2026-11-15_neighbours.json`). Direct ranking explainers on the exact query carry **`1,370,412` views** (`Colossal Cranium` `DspDvog4W00`) and **`1,180,364` views** (`SciShow` `kqhoLNUTS8I`), supported by `BYJU'S` (`505,669`), `SciShow Kids` (`398,961`), `Seeker` (`172,928`), and `TED-Ed` (`115,153`). |
| **2. Competition gap (wonder / clarity vs dry or crowding)** | 20% | **9.0** | **1.80** | The top direct explainers (`SciShow` `2:10` from `11 yr ago`, `Colossal Cranium` `2:17` from `7 yr ago`, `TED-Ed` `4:21` from `13 yr ago`, `Today I Found Out` `5:01` from `7 yr ago`) are brief `2–5 min` summaries that state either the rain-tread hypothesis or the nerve fact without dramatising the full chronological `80-year` experimental chain (`1935–1936` London median-nerve palsy ward → `1973` O'Riain bedside diagnostic soak → `2003` Singapore laser-Doppler glomus-body vasoconstriction measurement → `2011/2013` Changizi & Smulders wet-marble rain-tread test). All 5 candidate titles (`A`, `B`, `C`, `S01`, `S02`) have `0` exact title collisions. |
| **3. Narrative & visual arc (3D world + diagram clarity)** | 20% | **9.5** | **1.90** | Opens on an unmistakable `0:05–0:15` physical proof: a patient's hand lifted from a warm hospital water basin in `1935` London where the three median-nerve-supplied fingers remain completely smooth right beside two deeply wrinkled fingers. Each subsequent act turns on a clear visual mechanism and house-style inked diagram: digital `glomus bodies` constricting beneath the skin ridges (`2003`), diverging watershed drainage channels pressed against wet glass (`2011`), and the timed submerged glass-marble transfer box (`2013`). Directly builds on HOS `#2` Short `PFj6172YU4Q` (*One Tight Band Proved Your Blood Goes Round*, `31.29` views/day). |
| **4. Brand & guardrail fit** | 20% | **10.0** | **2.00** | Pure History of Science house lane: takes a universal human-hand question every viewer has experienced in the bath and overturns the textbook osmosis/sponge myth through clinical observation and laboratory proof. Zero medical advice, zero fearbait, and zero duplication across `02_Video-Projects/000–108`, `ideas/011–095`, or `WIP.json`. |
| **5. Series / cluster potential** | 15% | **9.0** | **1.35** | Forms a strong **Human Body & Nervous Reflex Cluster** alongside `005_How-Harvey-Proved-Blood-Circulates` (live; Short `PFj6172YU4Q` `#2` on channel at `31.29/d`), `011_Surgery-Before-Anaesthesia` (`next_hos`), `019_Galvani-Volta-Sparks-Battery` (`ideas/`), `033_Cajal-Loewi-Neurons-Synapses` (`ideas/`), `051_Scoville-Julius-Patapoutian-Spicy-Capsaicin-TRPV1` (`ideas/`), and `086_Sherrington-Beecher-Melzack-Wall-Pert-Endorphins-Pain` (`ideas/`). |
| **Total** | **100%** | — | **`9.55 / 10` (`95.5 / 100`)** | **GO (`≥ 7.5` threshold exceeded by `+2.05` points)** |

**Rule:** Proceed (`GO`) if **Total ≥ 7.5** and **Brand fit ≥ 8**. Both pass (`9.55 / 10` total, `10.0 / 10` brand fit).

---

## 2. Education Neighbour Gate (`neighbours.py` + `public_search.py`, Retrieved `2026-11-15`)

Saved in [`evidence_2026-11-15_neighbours.json`](evidence_2026-11-15_neighbours.json) (`bigCount = 11`, `hasTed = true`, `gate = PASS`, `failedQueries = []`) and [`evidence_2026-11-15_public_search.json`](evidence_2026-11-15_public_search.json):

| # | Channel | Views (`2026-11-15`) | Video ID & URL | Title | Source File |
|---:|---|---:|---|---|---|
| 1 | **CrashCourse** | `5,936,558` | [`Orumw-PyNjw`](https://youtu.be/Orumw-PyNjw) | *The Integumentary System, Part 1 - Skin Deep: Crash Course Anatomy & Physiology #6* | `neighbours.json` |
| 2 | **Veritasium** | `4,836,911` | [`jn5M48MVWyg`](https://youtu.be/jn5M48MVWyg) | *Is Dust Mostly Dead Skin?* | `neighbours.json` |
| 3 | **Amoeba Sisters** | `4,319,411` | [`RNLceVI8jcc`](https://youtu.be/RNLceVI8jcc) | *Nervous System* | `neighbours.json` |
| 4 | **CrashCourse** | `3,644,422` | [`71pCilo8k4M`](https://youtu.be/71pCilo8k4M) | *Autonomic Nervous System: Crash Course Anatomy & Physiology #13* | `neighbours.json` |
| 5 | **TED-Ed ★** | `3,540,088` | [`_r4c2NT4naQ`](https://youtu.be/_r4c2NT4naQ) | *The science of skin color - Angela Koine Flynn* | `neighbours.json` |
| 6 | **TED-Ed ★** | `3,268,747` | [`VVL-8zr2hk4`](https://youtu.be/VVL-8zr2hk4) | *How your muscular system works - Emma Bryce* | `neighbours.json` |
| 7 | **CrashCourse** | `2,837,651` | [`0IDgBlCHVsA`](https://youtu.be/0IDgBlCHVsA) | *Sympathetic Nervous System: Crash Course Anatomy & Physiology #14* | `neighbours.json` |
| 8 | **TED-Ed ★** | `2,363,909` | [`gsV7SJDDCY4`](https://youtu.be/gsV7SJDDCY4) | *How X-rays see through your skin - Ge Wang* | `neighbours.json` |
| 9 | **TED-Ed ★** | `2,361,774` | [`OxPlCkTKhzY`](https://youtu.be/OxPlCkTKhzY) | *The science of skin - Emma Bryce* | `neighbours.json` |
| 10 | **Amoeba Sisters** | `1,639,077` | [`t1iQHHJ0YyE`](https://youtu.be/t1iQHHJ0YyE) | *Integumentary System* | `neighbours.json` |
| 11 | **Colossal Cranium** | `1,370,412` | [`DspDvog4W00`](https://youtu.be/DspDvog4W00) | *Why Does Skin Wrinkle in Water? \| COLOSSAL QUESTIONS* | `public_search.json` |
| 12 | **SciShow** | `1,180,364` | [`kqhoLNUTS8I`](https://youtu.be/kqhoLNUTS8I) | *Why Do We Wrinkle When Wet?* | `neighbours.json` + `public_search.json` (`1,180,362`) |
| 13 | **TED-Ed ★** | `115,153` | [`k7ve_ibAY1s`](https://youtu.be/k7ve_ibAY1s) | *Why do fingers become pruney? - Mark Changizi* | `neighbours.json` (on-subject Tier-1 TED-Ed) |

---

## 3. Cluster Sketch (3 Adjacent Episodes)

1. **`HOS:109` (This Episode):** *Why Do Fingers Wrinkle in Water? (The Cut-Nerve Proof)* — Lewis & Pickering's 1935–1936 London median-nerve clinical discovery, O'Riain's 1973 warm-water test, Wilder-Smith's 2003 digital vasoconstriction proof, and Changizi/Smulders's 2011–2013 rain-tread wet-grip experiment.
2. **`HOS:005` (`005_How-Harvey-Proved-Blood-Circulates`, Live):** *The Tied Arm That Proved Your Blood Circulates* — William Harvey's 1628 forearm vein-valve and tourniquet proof (parent of `#2` HOS Short `PFj6172YU4Q`, `31.29` views/day).
3. **`HOS:033` (`033_Cajal-Loewi-Neurons-Synapses`, in `ideas/`):** *How Do Nerves Talk to Each Other?* — Santiago Ramón y Cajal's silver-stained neurons and Otto Loewi's 1921 two-frog-heart vagus nerve experiment.
4. **`HOS:051` (`051_Scoville-Julius-Patapoutian-Spicy-Capsaicin-TRPV1`, in `ideas/`):** *Why Does Chili Feel Hot?* — Wilbur Scoville's dilution scale, David Julius's `TRPV1` heat-and-capsaicin receptor, and Ardem Patapoutian's `PIEZO` touch-pressure channels.
