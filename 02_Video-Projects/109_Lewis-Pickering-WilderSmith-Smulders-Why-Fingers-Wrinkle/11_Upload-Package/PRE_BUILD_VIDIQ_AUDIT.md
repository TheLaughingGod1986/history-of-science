# Pre-Build vidIQ & Public Search Audit — `109_Lewis-Pickering-WilderSmith-Smulders-Why-Fingers-Wrinkle` (`HOS:109` Proposal)

> **PROPOSAL & VERIFICATION STATUS (`J2891`, `2026-11-15`):**
> - **Backlog Proposal Only (`next_hos`):** This audit accompanies the topic proposal for `HOS:109` (`109_Lewis-Pickering-WilderSmith-Smulders-Why-Fingers-Wrinkle`) waiting in `jobs/WIP.json` `next_hos` under Rule G (`active_hos` has 3 active films).
> - **All Claims Unverified:** Every historical and scientific claim below (the textbook keratin-osmosis sponge myth, Thomas Lewis and George Pickering's 1935–1936 London median-nerve clinical observations, S. O'Riain's 1973 warm-water immersion clinical test for nerve injury, Einar Wilder-Smith and Adeline Chow's 2003 laser-Doppler digital vasoconstriction proof, Mark Changizi's 2011 rain-tread drainage channel model, and Kyriacos Kareklas, Daniel Nettle, and Tom Smulders's 2013 Newcastle wet-marble grip transfer experiment) is **UNVERIFIED** and **must not be locked into a script or recorded in VO** until verified with exact quotes in `SOURCES.md` and cleared by the `facts` lane (`gemini-agy`).

---

## 1. Angle & Contract Check (`studio/RULES.md` + `LEARNINGS.md` Rules 1, 22, 23, 26)

| Check | Result |
|---|---|
| Channel | `@HistoryOfScienceYT` (`history-of-science`) |
| Film Number & Slug | `109_Lewis-Pickering-WilderSmith-Smulders-Why-Fingers-Wrinkle` (`HOS:109`) |
| Core Everyday Question | *Why do your fingers and toes wrinkle in warm bathwater — and how did surgeons treating severed hand nerves in 1935 accidentally prove that pruney skin isn't absorbing water like a sponge, but firing an active brain-and-nerve reflex?* |
| Rule 26 Autocomplete Phrase | `"why do fingers wrinkle in water"` (`autocomplete = yes`, 6 suggestions in signed-out YouTube autocomplete on `2026-11-15`, including `why do fingers wrinkle in water ted ed`) |
| Rule 26(a) Two Ranking Videos (`≥10,000` views) | 1. **Colossal Cranium** — *Why Do Your Fingers Wrinkle in Water?* (**`1,370,412` views**, retrieved `2026-11-15`)<br>2. **SciShow** — *Why Do Our Fingers and Toes Wrinkle in the Bath?* (**`1,180,362` views**, retrieved `2026-11-15`; plus **TED-Ed** [`k7ve_ibAY1s`](https://youtu.be/k7ve_ibAY1s) *Why do fingers become pruney? - Mark Changizi* **`115,153` views**) |
| Neighbour Gate (`neighbours.py`) | **PASS (`2026-11-15`)** — **`11` education videos `≥1,000,000` views** (`TED-Ed/TED: yes`, topped by `CrashCourse` `5.94M` `Orumw-PyNjw`, `Veritasium` `4.84M` `jn5M48MVWyg`, `Amoeba Sisters` `4.32M` `RNLceVI8jcc`, `CrashCourse` `3.64M` `71pCilo8k4M`, `TED-Ed` `3.54M` `_r4c2NT4naQ`, `TED-Ed` `3.27M` `VVL-8zr2hk4`, `TED-Ed` `2.36M` `gsV7SJDDCY4`, `TED-Ed` `2.36M` `OxPlCkTKhzY`, `CrashCourse` `2.30M` `LM682F16ebU`, `Cognito` `2.18M` `HiuXfbwND9s`, `CrashCourse` `1.65M` `x8tF2aQ3V1k`, plus `TED-Ed` `115.2k` `k7ve_ibAY1s`). Raw output saved at [`evidence_2026-11-15_neighbours.json`](evidence_2026-11-15_neighbours.json). |

---

## 2. Keyword & Public Search Table (`public_search.py`, Retrieved `2026-11-15`)

Saved in [`evidence_2026-11-15_public_search.json`](evidence_2026-11-15_public_search.json):

| Query / Candidate Title | Autocomplete (`2026-11-15`) | Top Public Results & Views (`2026-11-15`) | Role | Decision |
|---|---|---|---|---|
| `why do fingers wrinkle in water` | **yes** (6 suggestions: `why do fingers wrinkle in water`, `why do fingers wrinkle in water ted ed`, `why do fingers get wrinkled in water`, `why do fingers wrinkle in cold water`, `why do fingers wrinkle in water for kids`, `why do our fingers wrinkle in water`) | `Colossal Cranium` **`1,370,412`** · `SciShow` **`1,180,362`** · `TED-Ed` [`k7ve_ibAY1s`](https://youtu.be/k7ve_ibAY1s) **`115,153`** | Primary search phrase (Rule 26) | **Lock as primary keyword** |
| `Why Do Fingers Wrinkle in Water? (The Cut-Nerve Proof)` | — (Title A candidate, `54 chars`) | `Colossal Cranium` `1,370,412` · `SciShow` `1,180,362` · `TED-Ed` `115,153` | Long Title A (`0` exact collisions) | **Keep (Primary Proposal)** |
| `The Cut Nerve That Proved Why Fingers Wrinkle in Water` | — (Title B candidate, `54 chars`) | `Colossal Cranium` `1,370,412` · `SciShow` `1,180,362` · `TED-Ed` `115,153` | Long Title B (`0` exact collisions, T&C Arm 2) | **Keep (T&C Arm 2)** |
| `Why Do Fingers Wrinkle in Water? Not Because Skin Absorbs It` | — (Title C candidate, `60 chars`) | `Colossal Cranium` `1,370,412` · `SciShow` `1,180,362` · `TED-Ed` `115,153` | Long Title C (`0` exact collisions, exact phrase first) | **Keep (T&C Arm 3)** |
| `Why Doesn't Cut-Nerve Skin Wrinkle in Warm Water?` | — (Short `S01` candidate, `49 chars`) | `Colossal Cranium` `1,370,412` · `SciShow` `1,180,362` | Short `S01` candidate question title (`0` exact collisions) | **Keep** |
| `Do Wrinkled Fingers Really Help You Grip Wet Objects?` | — (Short `S02` candidate, `53 chars`) | `Colossal Cranium` `1,370,412` · `SciShow` `1,180,362` | Short `S02` candidate question title (`0` exact collisions) | **Keep** |

- **Rule 26(a) Exact Phrase & Two Ranking Videos (`2026-11-15`):**
  - **Phrase:** `"why do fingers wrinkle in water"`
  - **Ranking Video 1:** *Why Do Your Fingers Wrinkle in Water?* (`Colossal Cranium`, **`1,370,412` views**, retrieved `2026-11-15`)
  - **Ranking Video 2:** *Why Do Our Fingers and Toes Wrinkle in the Bath?* (`SciShow`, **`1,180,362` views**, retrieved `2026-11-15`; plus `TED-Ed` `k7ve_ibAY1s` *Why do fingers become pruney? - Mark Changizi* **`115,153` views**)
- **Decision:** Candidate primary title = `Why Do Fingers Wrinkle in Water? (The Cut-Nerve Proof)` (Title A, `54 chars`) / `Why Do Fingers Wrinkle in Water? Not Because Skin Absorbs It` (Title C, `60 chars`, exact phrase first)
- **Candidate description first 100 chars (unverified until `SOURCES.md` check):** `Why do fingers wrinkle in water, and how did a cut hand nerve in 1935 prove it's a nervous reflex?`

---

## 2b. Neighbour pass (blocking · `STUDIO_PLAYBOOK.md` §2 Step 4, Retrieved `2026-11-15`)

Saved in [`evidence_2026-11-15_neighbours.json`](evidence_2026-11-15_neighbours.json) and [`evidence_2026-11-15_public_search.json`](evidence_2026-11-15_public_search.json):

| # | Views (`2026-11-15`) | Channel (internal) | id & URL | Title | Subject words we reuse |
|---:|------:|--------------------|----------|-------|------------------------|
| 1 | `5,941,690` | CrashCourse (`neighbours.py`) | [`Orumw-PyNjw`](https://youtu.be/Orumw-PyNjw) | *The Integumentary System, Part 1 - Skin Deep: Crash Course Anatomy & Physiology #6* | `skin`, `epidermis`, `sweat glands`, `dermis` |
| 2 | `4,840,049` | Veritasium (`neighbours.py`) | [`jn5M48MVWyg`](https://youtu.be/jn5M48MVWyg) | *Is Dust Mostly Dead Skin?* | `skin`, `outer layer`, `keratin` |
| 3 | `4,321,347` | Amoeba Sisters (`neighbours.py`) | [`RNLceVI8jcc`](https://youtu.be/RNLceVI8jcc) | *Nervous System* | `nervous system`, `nerves`, `reflex` |
| 4 | `3,639,077` | CrashCourse (`neighbours.py`) | [`71pCilo8k4M`](https://youtu.be/71pCilo8k4M) | *Autonomic Nervous System: Crash Course Anatomy & Physiology #13* | `autonomic nervous system`, `sympathetic`, `reflex` |
| 5 | `3,540,775` | TED-Ed ★ (`neighbours.py`) | [`_r4c2NT4naQ`](https://youtu.be/_r4c2NT4naQ) | *The science of skin color - Angela Koine Flynn* | `skin`, `human body` |
| 6 | `2,360,295` | TED-Ed ★ (`neighbours.py`) | [`gsV7SJDDCY4`](https://youtu.be/gsV7SJDDCY4) | *Why do your knuckles pop? - Eleanor Nelsen* | `fingers`, `hands`, `body` |
| 7 | `2,355,668` | TED-Ed ★ (`neighbours.py`) | [`OxPlCkTKhzY`](https://youtu.be/OxPlCkTKhzY) | *The science of skin - Emma Bryce* | `skin`, `water`, `sweat`, `nerves` |
| 8 | `1,654,487` | CrashCourse (`neighbours.py`) | [`x8tF2aQ3V1k`](https://youtu.be/x8tF2aQ3V1k) | *Sympathetic Nervous System: Crash Course Anatomy & Physiology #14* | `sympathetic nervous system`, `blood vessels`, `vasoconstriction` |
| 9 | `1,370,412` | Colossal Cranium (`public_search.py`) | [`fMTHrv91-2E`](https://youtu.be/fMTHrv91-2E) | *Why Do Your Fingers Wrinkle in Water?* | `why do fingers wrinkle in water`, `nerves`, `grip` |
| 10 | `115,153` | TED-Ed ★ (`neighbours.py`) | [`k7ve_ibAY1s`](https://youtu.be/k7ve_ibAY1s) | *Why do fingers become pruney? - Mark Changizi* | `fingers`, `pruney`, `wrinkle in water`, `rain treads` |

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
