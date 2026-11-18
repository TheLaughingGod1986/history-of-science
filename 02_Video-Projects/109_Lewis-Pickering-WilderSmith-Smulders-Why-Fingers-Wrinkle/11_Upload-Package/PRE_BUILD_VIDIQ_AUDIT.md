# Pre-Build vidIQ & Public Search Audit — `109_Lewis-Pickering-WilderSmith-Smulders-Why-Fingers-Wrinkle` (`HOS:109` — Rule-E `GO` in `next_hos`)

> **RULE-E VERDICT & VERIFICATION STATUS (`J2891` / `J2918`, `2026-11-16`):**
> - **Rule-E Topic Review (`J2918`): `GO` (`95.5 / 100` · `9.55 / 10` Opportunity Score)** — Pre-cleared in `jobs/WIP.json` `next_hos` under Rule G (`active` has `4 / 4` HOS films full: `HOS:008`, `HOS:009`, `HOS:010`, `HOS:013`).
> - **All Claims Unverified:** Every historical and scientific claim below (the textbook keratin-osmosis sponge myth, Thomas Lewis and George Pickering's 1935–1936 London median-nerve clinical observations, S. O'Riain's 1973 warm-water immersion clinical test for nerve injury, Einar Wilder-Smith and Adeline Chow's 2003 laser-Doppler digital vasoconstriction proof, Mark Changizi's 2011 rain-tread drainage channel model, and Kyriacos Kareklas, Daniel Nettle, and Tom Smulders's 2013 Newcastle wet-marble grip transfer experiment) is **UNVERIFIED** and **must not be locked into a script or recorded in VO** until an active HOS WIP slot opens, exact quotes are recorded in `SOURCES.md`, and the `facts` lane (`gemini-agy`) verifies every claim.

---

## 1. Angle & Contract Check (`studio/RULES.md` + `LEARNINGS.md` Rules 1, 22, 23, 26)

| Check | Result |
|---|---|
| Channel | `@HistoryOfScienceYT` (`history-of-science`) |
| Film Number & Slug | `109_Lewis-Pickering-WilderSmith-Smulders-Why-Fingers-Wrinkle` (`HOS:109`) |
| Core Everyday Question | *Why do your fingers and toes wrinkle in warm bathwater — and how did doctors treating severed hand nerves in 1935 accidentally prove that pruney skin isn't absorbing water like a sponge, but firing an active brain-and-nerve reflex?* |
| Rule 26 Autocomplete Phrase | `"why do fingers wrinkle in water"` (`autocomplete = yes`, `4` suggestions in signed-out YouTube GB autocomplete on `2026-11-15`: `why do fingers wrinkle in water`, `why do fingers get wrinkly in water`, `why do my hands wrinkle in water so fast`, `why fingers prune in water`) |
| Rule 26(a) Two Ranking Videos (`≥10,000` views) | 1. **Colossal Cranium** — [`DspDvog4W00`](https://youtu.be/DspDvog4W00) *Why Does Skin Wrinkle in Water? \| COLOSSAL QUESTIONS* (**`1,370,412` views**, retrieved `2026-11-15`)<br>2. **SciShow** — [`kqhoLNUTS8I`](https://youtu.be/kqhoLNUTS8I) *Why Do We Wrinkle When Wet?* (**`1,180,362` views** in `public_search.json` / **`1,180,364` views** in `neighbours.json`, retrieved `2026-11-15`; plus **BYJU'S** [`-5V5BjunAwE`](https://youtu.be/-5V5BjunAwE) **`505,669` views**, **SciShow Kids** [`uWjlRlpHlbA`](https://youtu.be/uWjlRlpHlbA) **`398,961` views**, and **TED-Ed** [`k7ve_ibAY1s`](https://youtu.be/k7ve_ibAY1s) *Why do fingers become pruney? - Mark Changizi* **`115,153` views**) |
| Neighbour Gate (`neighbours.py`) | **PASS (`2026-11-15`)** — **`11` education videos `≥1,000,000` views** (`TED-Ed/TED: yes`, topped by `CrashCourse` `5,936,558` `Orumw-PyNjw`, `Veritasium` `4,836,911` `jn5M48MVWyg`, `Amoeba Sisters` `4,319,411` `RNLceVI8jcc`, `CrashCourse` `3,644,422` `71pCilo8k4M`, `TED-Ed` `3,540,088` `_r4c2NT4naQ`, `TED-Ed` `3,268,747` `VVL-8zr2hk4`, `CrashCourse` `2,837,651` `0IDgBlCHVsA`, `TED-Ed` `2,363,909` `gsV7SJDDCY4`, `TED-Ed` `2,361,774` `OxPlCkTKhzY`, `Amoeba Sisters` `1,639,077` `t1iQHHJ0YyE`, `SciShow` `1,180,364` `kqhoLNUTS8I`, plus `TED-Ed` `115,153` `k7ve_ibAY1s`). Raw output saved at [`evidence_2026-11-15_neighbours.json`](evidence_2026-11-15_neighbours.json). |

---

## 2. Keyword & Public Search Table (`public_search.py`, Retrieved `2026-11-15`)

Saved in [`evidence_2026-11-15_public_search.json`](evidence_2026-11-15_public_search.json):

| Query / Candidate Title | Autocomplete (`2026-11-15`) | Top Public Results & Views (`2026-11-15`) | Role | Decision |
|---|---|---|---|---|
| `why do fingers wrinkle in water` | **yes** (`4` suggestions: `why do fingers wrinkle in water`, `why do fingers get wrinkly in water`, `why do my hands wrinkle in water so fast`, `why fingers prune in water`) | `Colossal Cranium` (`DspDvog4W00`) **`1,370,412`** · `SciShow` (`kqhoLNUTS8I`) **`1,180,362`** · `AumSum's Science` (`Ya71oUns8kI`) **`112,286`** · `It's AumSum Time` (`V0ktjS1ts74`) **`103,166`** · `Dr. Eric Berg DC` (`g5U9K1ZqVyo`) **`102,336`** · `Today I Found Out` (`71939OP-NvM`) **`66,280`** | Primary search phrase (Rule 26) | **Lock as primary keyword** |
| `why do fingers prune in water` | **yes** (`3` suggestions: `why do fingers wrinkle in water`, `why do my hands wrinkle in water so fast`, `why fingers prune in water`) | `Colossal Cranium` (`DspDvog4W00`) **`1,370,399`** · `SciShow` (`kqhoLNUTS8I`) **`1,180,364`** · `BYJU'S` (`-5V5BjunAwE`) **`505,669`** · `Seeker` (`Aa1FRQ2o-wI`) **`172,928`** | Secondary search phrase (Rule 26) | **Keep in description & tags** |
| `Why Do Fingers Wrinkle in Water? (The Cut-Nerve Proof)` | — (Title A candidate, `54 chars`) | `Why, is that then` (`I8Kl40TDG6s`) `4` · `Clear Cut, Big Science` (`24G3FWf2PYw`) `17` · `The Cold Truth` (`7xslLm0VRMw`) `5` · `The Mundane Lab` (`el-MsC2adlI`) `24` | Long Title A (`0` exact collisions) | **Keep (Primary Proposal)** |
| `The Cut Nerve That Proved Why Fingers Wrinkle in Water` | — (Title B candidate, `54 chars`) | `Today I Found Out` (`71939OP-NvM`) `66,280` · `Curious Tom` (`DPnz559YsQI`) `19` · `Oddly Explained` (`7FKN9FkYEsA`) `4` · `Everyday Science` (`vuOOAQQLdLg`) `27` · `Vera's History` (`2DtV5dkkG5Q`) `75` | Long Title B (`0` exact collisions, T&C Arm 2) | **Keep (T&C Arm 2)** |
| `Why Do Fingers Wrinkle in Water? Not Because Skin Absorbs It` | — (Title C candidate, `60 chars`) | `Colossal Cranium` (`DspDvog4W00`) `1,370,412` · `Today I Found Out` (`71939OP-NvM`) `66,280` · `Know Science and Technology` (`4kR-Whs2nXc`) `12` · `Zayne.` (`qP7_Z1b4pHw`) `32` | Long Title C (`0` exact collisions, exact phrase first) | **Keep (T&C Arm 3)** |
| `Why Doesn't Cut-Nerve Skin Wrinkle in Warm Water?` | — (Short `S01` candidate, `49 chars`) | `See Inside` (`g0ILsOr1S7k`) `3` · `Frem` (`zpxW3w37qWY`) `19` | Short `S01` candidate question title (`0` exact collisions) | **Keep** |
| `Do Wrinkled Fingers Really Help You Grip Wet Objects?` | — (Short `S02` candidate, `53 chars`) | `SciShow` (`kqhoLNUTS8I`) `1,180,364` · `BYJU'S` (`-5V5BjunAwE`) `505,669` · `Dr. Eric Berg DC` (`g5U9K1ZqVyo`) `102,340` · `The Royal Society` (`KG5HGQ3RvrE`) `3,524` · `The Why Guy` (`COh-Hcn0lic`) `1,275` · `TheBiotic` (`YqMTQahSk7Q`) `1,115` | Short `S02` candidate question title (`0` exact collisions) | **Keep** |

- **Rule 26(a) Exact Phrase & Two Ranking Videos (`2026-11-15`):**
  - **Phrase:** `"why do fingers wrinkle in water"`
  - **Ranking Video 1:** *Why Does Skin Wrinkle in Water? | COLOSSAL QUESTIONS* (`Colossal Cranium` [`DspDvog4W00`](https://youtu.be/DspDvog4W00), **`1,370,412` views**, retrieved `2026-11-15`)
  - **Ranking Video 2:** *Why Do We Wrinkle When Wet?* (`SciShow` [`kqhoLNUTS8I`](https://youtu.be/kqhoLNUTS8I), **`1,180,362` views** in `public_search.json` / **`1,180,364` views** in `neighbours.json`, retrieved `2026-11-15`; plus `TED-Ed` [`k7ve_ibAY1s`](https://youtu.be/k7ve_ibAY1s) *Why do fingers become pruney? - Mark Changizi* **`115,153` views**)
- **Decision:** Candidate primary title = `Why Do Fingers Wrinkle in Water? (The Cut-Nerve Proof)` (Title A, `54 chars`) / `Why Do Fingers Wrinkle in Water? Not Because Skin Absorbs It` (Title C, `60 chars`, exact phrase first)
- **Candidate description first 100 chars (unverified until `SOURCES.md` check):** `Why do fingers wrinkle in water, and how did a cut hand nerve in 1935 prove it's a nervous reflex?`

---

## 2b. Neighbour pass (blocking · `STUDIO_PLAYBOOK.md` §2 Step 4, Retrieved `2026-11-15`)

Saved in [`evidence_2026-11-15_neighbours.json`](evidence_2026-11-15_neighbours.json) (`bigCount = 11`, `gate = PASS`, `hasTed = true`) and [`evidence_2026-11-15_public_search.json`](evidence_2026-11-15_public_search.json):

| # | Views (`2026-11-15`) | Channel (internal) | id & URL | Title | Subject words we reuse |
|---:|------:|--------------------|----------|-------|------------------------|
| 1 | `5,936,558` | CrashCourse (`neighbours.py`) | [`Orumw-PyNjw`](https://youtu.be/Orumw-PyNjw) | *The Integumentary System, Part 1 - Skin Deep: Crash Course Anatomy & Physiology #6* | `skin`, `epidermis`, `sweat glands`, `dermis` |
| 2 | `4,836,911` | Veritasium (`neighbours.py`) | [`jn5M48MVWyg`](https://youtu.be/jn5M48MVWyg) | *Is Dust Mostly Dead Skin?* | `skin`, `outer layer`, `keratin` |
| 3 | `4,319,411` | Amoeba Sisters (`neighbours.py`) | [`RNLceVI8jcc`](https://youtu.be/RNLceVI8jcc) | *Nervous System* | `nervous system`, `nerves`, `reflex` |
| 4 | `3,644,422` | CrashCourse (`neighbours.py`) | [`71pCilo8k4M`](https://youtu.be/71pCilo8k4M) | *Autonomic Nervous System: Crash Course Anatomy & Physiology #13* | `autonomic nervous system`, `sympathetic`, `reflex` |
| 5 | `3,540,088` | TED-Ed ★ (`neighbours.py`) | [`_r4c2NT4naQ`](https://youtu.be/_r4c2NT4naQ) | *The science of skin color - Angela Koine Flynn* | `skin`, `human body` |
| 6 | `3,268,747` | TED-Ed ★ (`neighbours.py`) | [`VVL-8zr2hk4`](https://youtu.be/VVL-8zr2hk4) | *How your muscular system works - Emma Bryce* | `human body`, `nerves`, `movement` |
| 7 | `2,837,651` | CrashCourse (`neighbours.py`) | [`0IDgBlCHVsA`](https://youtu.be/0IDgBlCHVsA) | *Sympathetic Nervous System: Crash Course Anatomy & Physiology #14* | `sympathetic nervous system`, `blood vessels`, `vasoconstriction` |
| 8 | `2,363,909` | TED-Ed ★ (`neighbours.py`) | [`gsV7SJDDCY4`](https://youtu.be/gsV7SJDDCY4) | *How X-rays see through your skin - Ge Wang* | `skin`, `hands`, `medical` |
| 9 | `2,361,774` | TED-Ed ★ (`neighbours.py`) | [`OxPlCkTKhzY`](https://youtu.be/OxPlCkTKhzY) | *The science of skin - Emma Bryce* | `skin`, `water`, `sweat`, `nerves` |
| 10 | `1,639,077` | Amoeba Sisters (`neighbours.py`) | [`t1iQHHJ0YyE`](https://youtu.be/t1iQHHJ0YyE) | *Integumentary System* | `skin`, `layers`, `sweat ducts` |
| 11 | `1,370,412` | Colossal Cranium (`public_search.py`) | [`DspDvog4W00`](https://youtu.be/DspDvog4W00) | *Why Does Skin Wrinkle in Water? \| COLOSSAL QUESTIONS* | `why do fingers wrinkle in water`, `nerves`, `grip` |
| 12 | `1,180,364` | SciShow (`neighbours.py` + `public_search.py`) | [`kqhoLNUTS8I`](https://youtu.be/kqhoLNUTS8I) | *Why Do We Wrinkle When Wet?* | `wrinkle when wet`, `fingers`, `nervous system`, `grip` |
| 13 | `115,153` | TED-Ed ★ (`neighbours.py`) | [`k7ve_ibAY1s`](https://youtu.be/k7ve_ibAY1s) | *Why do fingers become pruney? - Mark Changizi* | `fingers`, `pruney`, `wrinkle in water`, `rain treads` |

**Proposed subject-only tags (8 tags, zero channel names):**  
`why do fingers wrinkle in water, why do fingers get pruney, thomas lewis george pickering nerve, sympathetic nervous system skin wrinkling, mark changizi rain treads fingers, einar wilder smith vasoconstriction, history of medicine experiments, human body reflexes`

---

## 3. Title ABC (score before VO)

| | Title | Chars | Collisions (`2026-11-15`) | Role & Notes | Keep? |
|---|-------|------:|-----------:|--------------|-------|
| A | `Why Do Fingers Wrinkle in Water? (The Cut-Nerve Proof)` | 54 | 0 | **Main (`LEARNINGS.md` Rules 1, 23, 26):** Starts verbatim with exact autocomplete question `"why do fingers wrinkle in water"` + concrete clinical discovery hook | **Keep (Primary Proposal)** |
| B | `The Cut Nerve That Proved Why Fingers Wrinkle in Water` | 54 | 0 | **Test & Compare (`Rule 23`):** Leads with the clinical cut-nerve mystery + exact search phrase | **Keep (T&C Arm 2)** |
| C | `Why Do Fingers Wrinkle in Water? Not Because Skin Absorbs It` | 60 | 0 | **Rule 26 Variant (`≤70 chars`):** Starts verbatim with exact autocomplete phrase `"why do fingers wrinkle in water"` + myth-busting hook | **Keep (T&C Arm 3)** |
| Reject | `Autonomic Vasoconstriction and Digital Skin Wrinkling \| History of Science` | 74 | — | Clinical jargon + forbidden series suffix | **Reject** |

---

## 3b. Script reviewer (blocking before VO — not run; proposal only)

- [ ] `SOURCES.md` exact quotes + `facts` lane verification completed (required before script lock)
- [ ] Score ≥ **90 / 100** (`npm run review:script`)
