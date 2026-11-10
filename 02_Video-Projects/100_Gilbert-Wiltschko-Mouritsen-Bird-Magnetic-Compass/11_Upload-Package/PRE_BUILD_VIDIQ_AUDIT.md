# Pre-build vidIQ audit — History of Science (`HOS:100`)

**Hard gate:** Run **before** locking script, VO, prompts, or picture gen for any new long.  
**Also follow:** `00_Brand/Channel-Setup/HOS_STRATEGY.md`, `THUMBNAIL_AND_TITLE_RULES.md`, `STUDIO_PLAYBOOK.md` §2–§8, and `orbit-with-ben/05_Analytics/LEARNINGS.md` (Rules 1–30, including Rule 26 Search-Led Longs and Rule 30 `HOS-2026-11-E2`).

---

## Episode

| Field | Value |
|-------|-------|
| ID / slug | `100_Gilbert-Wiltschko-Mouritsen-Bird-Magnetic-Compass` (`HOS:100`) |
| Working title | `How Do Migrating Birds See Earth's Magnetic Field?` (`50 chars`) |
| Date pulled | `2026-11-08` (`J2411`) · Verified `2026-11-10` (`J2473` Rule-E Review) |
| Credits used (approx) | `£0.00` (signed-out YouTube public search + primary-source literature verification; vidIQ waived by Ben per `STUDIO_PLAYBOOK.md` §2 Step 6) |
| Brand guardrails | Wonder over fearbait · no conspiracy · HOS lane (a familiar thing — a garden robin migrating at night — and the moment we found out how it sees Earth's magnetic field) |

---

## 1. Success targets (this episode)

| Metric | Target |
|--------|--------|
| Title score | ≥ **90** (aim **95+**) |
| Primary keyword overall | `how do birds navigate` / `how do birds navigate using magnetic fields` (`autocomplete = yes`, all GB top-5 results `<293k` views) |
| Hook promise | Every autumn, a thumb-sized European robin flies `4,000 km` in the dark—guided by a quantum-entangled magnetic compass (`CRY4`) inside its own eye |
| Retention design | `HOS-2026-11-E2` proof-first `0:00–0:30` (`<4.5 s` cuts, `≥7` moving plates, `0:05–0:15` apparatus/proof, first animated `DATA+SCALE` graphic at `0:25–0:40`) + 5 acts that earn the next minute |
| Packaging | 3-way Thumbnail Test & Compare from day 1 (`HE SEES NORTH` robin pupil grid vs Rule 14 bright copper coil lab `100× WEAKER` vs `QUANTUM EYE` retina radical pair; readable at `168×94`) |

---

## 2. Keyword research (Signed-Out YouTube Autocomplete & Competition Check · Rule 26)

| Keyword | Autocomplete (`suggest()`) | GB Top-5 Competition (`public_search.py`) | Role (title / desc / chapter / Shorts) | Keep? |
|---------|---------------------------|-------------------------------------------|----------------------------------------|-------|
| `how do birds navigate` | **yes** (`how do birds navigate`, `how do birds navigate using magnetic fields`) | Low (`nature video` `292k`, `History of Simple Things` `193k`, `Seeker` `147k`, `BioBush` `74k`) | Primary search phrase (Title D lead + Desc line 1 + tags) | **Keep** |
| `how do birds navigate using magnetic fields` | **yes** (direct autocomplete suggestion) | Very Low (`nature video` `292k`, `Science Magazine` `156k`, `Arbor Scientific` `37k`) | Primary long-tail search phrase (Title A + Desc line 1 + Ch 3) | **Keep** |
| `bird migration` | **yes** (`bird migration`, `bird migration documentary`, `bird migration patterns`) | Medium (`TED-Ed` `292k`, `SciShow Kids` `910k`) | Umbrella subject noun (Title A + Desc + tags) | **Keep** |
| `quantum biology` | Related (`1.59M` Royal Institution & `1.11M` TED Jim Al-Khalili neighbours) | Low for dedicated narrative films (`nature video` `292k`, `Up and Atom` `111k`) | Suggested-graph bridge keyword (Ch 4–5 + tags) | **Keep** |
| `earth's magnetic field` | **yes** (`TED-Ed` `1.38M` & `443k`) | Low in biological navigation context | Title A + Ch 1 (`William Gilbert 1600 terrella`) + Short `S01` | **Keep** |
| `cryptochrome robin eye` | Niche mechanism term (`Nature` 2021 Mouritsen & Hore) | Very Low | Title B + Ch 5 + Short `S01` payoff | **Keep** |

- **Rule 26(a) Exact Phrase & Two Ranking Videos:**
  - **Phrase:** `"how do birds navigate"` / `"how do birds navigate using magnetic fields"`
  - **Ranking Video 1:** `0SPD2r0xV8k` — *How quantum mechanics help birds find their way* (`nature video`, **292,033 views**)
  - **Ranking Video 2:** `_2n0H8X9HhY` — *How Do Birds Navigate Thousands of Miles Without Getting Lost?* (`History of Simple Things`, **193,439 views**; plus `PRYmx7Lk9F0` *Seeker* `146,620` views)
- **Decision:** Primary keyword for title lead = `How Do Migrating Birds See Earth's Magnetic Field?` (Title A) / `How Do Birds Navigate? (The Quantum Compass in a Robin's Eye)` (Title D, Rule 26)
- **Description first 100 chars must include (Rule 26c):** `How do birds navigate using magnetic fields across 4,000 kilometres in the dark? Inside a robin's eye...`

---

## 2b. Neighbour pass (blocking · `STUDIO_PLAYBOOK.md` §2 Step 4)

| # | Views (`2026-11-08`) | Channel (internal) | id | Title | Subject words we reuse |
|---:|------:|--------------------|----|-------|------------------------|
| 1 | `9,213,259` | TED-Ed ★ | `UjaAxUO6-Uw` | *Schrödinger's cat: A thought experiment in quantum mechanics - Chad Orzel* | `quantum`, `quantum mechanics`, `entanglement` |
| 2 | `2,218,334` | TED-Ed ★ | `m8bDCaPhOek` | *How did Polynesian wayfinders navigate the Pacific Ocean? - Alan Tamayose and Shantell De Silva* | `navigate`, `navigation`, `compass`, `stars` |
| 3 | `2,110,060` | TED-Ed ★ | `hRzRjHzvOts` | *Why can't some birds fly? - Gillian Gibb* | `birds`, `bird`, `flight` |
| 4 | `1,590,173` | The Royal Institution | `wwgQVZju1ZM` | *Jim Al-Khalili - Quantum Life: How Physics Can Revolutionise Biology* | `quantum biology`, `european robin`, `magnetic field`, `cryptochrome` |
| 5 | `1,157,123` | TED-Ed ★ | `BR1enXROmgA` | *Eli the eel: A mysterious migration - James Prosek* | `migration`, `magnetic field`, `navigate` |
| 6 | `1,110,062` | TED ★ | `_qgSz1UmcBM` | *How Quantum Biology Might Explain Life's Biggest Questions \| Jim Al-Khalili \| TED Talks* | `quantum biology`, `robin`, `birds navigate`, `quantum entanglement` |

**Proposed description first line(s):**  
`How do birds navigate using magnetic fields across 4,000 kilometres in the dark? From William Gilbert's 1600 lodestone globe and Wolfgang Wiltschko's 1972 Frankfurt copper coils to Henrik Mouritsen and Peter Hore's 2021 Nature discovery of retinal cryptochrome 4 (CRY4), this is how we discovered the quantum magnetic compass inside a migrating bird's eye.`

**Proposed subject-only tags (8 tags, zero channel names):**  
`how do birds navigate, how do birds see magnetic fields, bird migration, magnetic field, quantum biology, cryptochrome 4 robin eye, wolfgang wiltschko inclination compass, magnetoreception`

---

## 3. Title ABC (score before VO)

| | Title | Chars | Collisions | Role & Notes | Keep? |
|---|-------|------:|-----------:|--------------|-------|
| A | `How Do Migrating Birds See Earth's Magnetic Field?` | 50 | 0 | **Main (`LEARNINGS.md` Rules 1 & 15):** Plain-English positive question `≤50` chars with `birds` and `Earth's magnetic field` | **Keep (Primary)** |
| B | `The Quantum Compass Hidden Inside a Robin's Eye` | 47 | 0 | **Test & Compare (`THUMBNAIL_AND_TITLE_RULES.md` §1):** Concrete biological object + mystery | **Keep (T&C Arm 2)** |
| C | `How a Caged Robin Proved Birds See Magnetism` | 44 | 0 | **Experiment Variant:** Names the 1972 Frankfurt caged-robin proof | **Keep (Alt)** |
| D | `How Do Birds Navigate? (The Quantum Compass in a Robin's Eye)` | 61 | 0 | **Rule 26 + Rule 23 Variant (`≤70 chars`):** Starts verbatim with exact autocomplete phrase `"How Do Birds Navigate?"` + bracketed story/stakes tail | **Keep (T&C Arm 3 / Rule 26)** |
| Reject | `How Did We Discover Magnetoreception? \| History of Science` | 59 | — | Overused *How Did We Discover X?* formula + jargon noun + forbidden series suffix | **Reject** |

**Locked title:** `How Do Migrating Birds See Earth's Magnetic Field?` (paired with Rule 26 Title D `How Do Birds Navigate? (The Quantum Compass in a Robin's Eye)` and Title B `The Quantum Compass Hidden Inside a Robin's Eye` for Test & Compare).  
**Why it wins (score + brand + keyword):** Combines our #1/#2 Long question shape (`002` & `004`) with direct search and TED/Royal Institution neighbour keywords (`birds`, `navigate`, `magnetic field`, `quantum`, `robin`), `≤50 chars` on Title A (`61 chars ≤ 70` on Rule 26 Title D), and `0` exact collisions on YouTube.

---

## 3b. Script reviewer (blocking before VO — to run when film enters active HOS WIP)

```bash
cd 07_Content-Ops && npm run review:script -- --file ../02_Video-Projects/100_Gilbert-Wiltschko-Mouritsen-Bird-Magnetic-Compass/01_Script/100_gilbert_wiltschko_mouritsen_bird_magnetic_compass_script_master_v01.md
npm run gate:episode -- --project ../02_Video-Projects/100_Gilbert-Wiltschko-Mouritsen-Bird-Magnetic-Compass
```

- [ ] Score ≥ **90 / 100** (pending active Script stage under Rule G)

---

## 4. Outlier / competitive patterns (on-brand only)

| Outlier / pattern | Views | Steal (structure) | Do **not** copy |
|-------------------|------:|-------------------|-----------------|
| `_qgSz1UmcBM` (*How Quantum Biology Might Explain Life's Biggest Questions \| Jim Al-Khalili*, TED ★) & `wwgQVZju1ZM` (Royal Institution) | `1.11M` & `1.59M` | Clear contrast between classical thermal noise (`kT`) and quantum-entangled radical pairs in the European robin's eye | Lecture-hall stage talk (we show the `1600`, `1966`, `1972`, and `2021` experiments in 3D cartoon rooms) |
| `0SPD2r0xV8k` (*How quantum mechanics help birds find their way*, nature video) | `292K` | Visualising the `CRY4` protein and tryptophan electron-hopping chain from the June 2021 *Nature* paper | Short `4-min` news summary that skips Gilbert (`1600`), Emlen (`1966`), and the Wiltschkos' `1972` coil experiments |
| `AL_-qlWko_g` (*How Did We Discover the Periodic Table?*, HOS `002` `#1` Long) | `161` views (`3.1/d`, `3.4%` CTR, `70%` `0:15` hold) | Tactile laboratory props (ink-pad funnel, copper coils, lodestone globe) + midpoint assumption flip | Formulaic *How Did We Discover X?* title |

**Patterns we will use in this script:**

- [x] Assumption-flip / open-loop title (birds don't have a north-seeking iron needle compass — they *see* the magnetic dip angle using blue light and quantum entanglement)
- [x] Numbered 5-act chronological escalation (`1600 → 1855/1966 → 1972 → 1978/2000 → 2021`)
- [x] Everyday scale anchor (`50 µT` Earth field = **`100×` weaker than a `5,000 µT` fridge magnet**; `18-gram` robin flying `4,000 km`)
- [x] Slow reveal / delayed molecular answer (`ErCRY4` 4-tryptophan chain `[FAD•− … TrpH•+]` in Act 5)

---

## 5. Incorporate into the build (required)

| Data finding | Change to script / chapters / visuals / packaging |
|--------------|-----------------------------------------------------|
| Primary search phrases (`how do birds navigate`, `magnetic field`) | In Title A/D, spoken in the first `8 s`, and in line 1 of the description (Rule 26) |
| Precision check #1 (`J2473`): Gilbert's `1600` role & Norman (`1576`/`1581`) | Set `WHO: William Gilbert (1544–1603) — English physician & physicist` (`1600` *De Magnete*, appointed Elizabeth I's physician in Feb `1601`) and credit Robert Norman (`1576`/`1581`) for first measuring needle dip |
| Precision check #2 (`J2473`): Emlen (`1966`) & Wiltschko (`1972`) | Set `WHO: Stephen Emlen (born 1940) — Avian behavioral ecologist` (`WHEN: Michigan & Cornell, 1966`) and include both `WHO: Wolfgang Wiltschko (born 1938)` and `WHO: Roswitha Wiltschko (born 1947)` |
| Precision check #3 (`J2473`): `2021` *Nature* team | Include both `WHO: Henrik Mouritsen (born 1971) — Sensory neurobiologist` and `WHO: Peter Hore (born 1954) — Oxford physical chemist` |
| 3-way Thumbnail Test & Compare (Rules 11, 12, 14) | Build Thumb A (`HE SEES NORTH`), Thumb B (`100× WEAKER` bright copper-coil room), and Thumb C (`QUANTUM EYE`) |

**Chapter list after audit** (5 acts, each with a teach-point + `Teach on screen` markers):

1. **Part 01 (Cold Open, no chapter card): The Little Earth That Dipped** — Night-migrating European robin (`4,000 km`) → Robert Norman (`1576`/`1581`) and **William Gilbert** (`1600`, London, *De Magnete*) carving a spherical lodestone (*terrella*) to prove Earth's magnetic field lines dip downward toward the poles (`WHO: William Gilbert (1544–1603) — English physician & physicist`, `WHEN: London, 1600`, `DATA #1 + SCALE` at `0:25–0:40`: `Earth's field 50 µT vs fridge magnet 5,000 µT · SCALE: 100 times weaker than a fridge magnet`).
2. **Part 02: Footprints in an Ink Cone** — Why physicists dismissed **Alexander von Middendorff** (`1855`) because thermal noise (`kT`) is ten million times stronger than a `50 µT` magnetic nudge → **Stephen Emlen** (`1966`, Michigan & Cornell) inventing the blotter-paper **Emlen funnel** with an ink pad at the base to record a captive night migrant's directional hops (`WHO: Alexander von Middendorff (1815–1894) — Russian zoologist`, `WHO: Stephen Emlen (born 1940) — Avian behavioral ecologist`, `WHEN: Michigan & Cornell, 1966`, `EXPLORER BEAT #1`).
3. **Part 03: The Room Wrapped in Copper Coils** — **Wolfgang and Roswitha Wiltschko** (`1972`, Frankfurt, *Science*) place European robins inside giant **Helmholtz copper coils** and flip horizontal north and south—and the robins don't care! Flipping the vertical coil proves birds read the **inclination dip angle** against gravity (`66°` in Frankfurt vs `0°` flat at the equator), not north/south polarity (`WHO: Wolfgang Wiltschko (born 1938) — Frankfurt zoologist`, `WHO: Roswitha Wiltschko (born 1947) — Behavioral zoologist`, `WHEN: Frankfurt, 1972`, `DATA #2 + SCALE`: inclination dip-angle chart `66° Frankfurt vs 0° equator`, `FACT: Birds read angle, not north`).
4. **Part 04: The Compass That Goes Blind in Red Light** — The Wiltschkos discover the robin's magnetic compass works under blue/green light (`~450 nm`) but fails completely under red light (`FACT: Compass fails in red light`, `EXPLORER BEAT #2`) → chemical physicist **Klaus Schulten** (`1978`, and `2000` with **Thorsten Ritz**) proposes that blue light creates quantum-entangled **radical pairs** inside a retinal protein (`WHO: Klaus Schulten (1947–2016) — Chemical physicist`, `WHO: Thorsten Ritz (born 1972) — Biophysics theorist`, `WHEN: Urbana, 1978 & 2000`).
5. **Part 05: The Quantum Protein in a Robin's Eye** — In **June 2021** (*Nature*), **Henrik Mouritsen** (`Oldenburg`) and **Peter Hore** (`Oxford`) isolate **cryptochrome 4 (`ErCRY4`)** from the European robin's retina, showing an electron hopping across **four tryptophan amino acids** in picoseconds (`[FAD•− … TrpH•+]`) with far higher magnetic sensitivity than in non-migratory chickens or pigeons (`WHO: Henrik Mouritsen (born 1971) — Sensory neurobiologist`, `WHO: Peter Hore (born 1954) — Oxford physical chemist`, `WHEN: Oldenburg & Oxford, 2021`, `DATA #3 + SCALE`: animated timeline `1600 -> 1855 -> 1966 -> 1972 -> 2000 -> 2021` + `CRY4` magnetic sensitivity comparison chart `Robin vs Chicken & Pigeon`, `FACT: Robins see magnetic shadows`).

---

## 6. Retention plan (`STUDIO_PLAYBOOK.md` §3 & `LEARNINGS.md` Rule 30 `HOS-2026-11-E2`)

| Minute zone | Job | Picture / VO note |
|-------------|-----|-------------------|
| `0:00–0:05` | Answer image on screen | Moving 3D house-style robin flying through starlit darkness as faint blue magnetic lines curve inside its eye (no logo, no title card, no Explorer) |
| `0:05–0:15` | Title question (`0:08`) + apparatus proof (`0:05–0:15`) + promise (`0:15`) | Spoken question by `0:08`; cut `<4.5 s` to Wiltschko's copper Helmholtz coils and ink-stained Emlen funnel (`0:05–0:15` physical proof per `HOS-2026-11-E2`) |
| `0:15–0:40` | Stakes (`0:25`) + first `DATA+SCALE` (`0:25–0:40`) + first real fact (`<0:45`) | At least 7 distinct moving plates in `0:00–0:30` (all holds `<4.5 s`); first animated ink `DATA+SCALE` chart (`50 µT Earth vs 5,000 µT fridge magnet · 100× weaker`) at `0:25–0:40`; William Gilbert (`London, 1600`) before `0:45` |
| Chapter starts | Re-hook + chapter card | Parts 02–05 open with `[CHAPTER CARD]` (`0.5–0.8 s` breath, `0.4 s` xfade) and end on an unanswered physical puzzle |
| Mid (`Parts 02–04`) | Teach while story continues | Every experiment (`terrella`, `Emlen ink cone`, `Helmholtz coil flip`, `red vs blue light`) happens on screen as spoken; music lifts from ambient wonder drone to plucked period arpeggio on the mechanism teach |
| Final chapter (`Part 05`) | Payoff + hand-off | `2021` `ErCRY4` 4-tryptophan quantum radical-pair reveal + robin's-eye bright/dark inclination dome → hand off to next film → `3–4 s` cream end card → `20 s` Studio end screen |

- [x] No 30s+ stretch without a new teach or turn  
- [x] Every chapter earns the next one  
- [x] Runtime target **7–9 min** (`1,200–1,300` spoken words)

---

## 7. Sign-off (block production until checked — complete §3b when film enters active WIP)

- [x] Keywords pulled and primary locked (`public_search.py` + `neighbours.py` saved; vidIQ waived by Ben per `STUDIO_PLAYBOOK.md` §2 Step 6)
- [x] Title variants pre-cleared (`0` exact collisions; Rule 15 Question + Rule 26 Search-Phrase-First + T&C Statement)
- [ ] Script reviewer ≥ 90 (to run when `HOS:100` enters `active` from `jobs/WIP.json` `next_hos`)
- [x] Outlier patterns mapped into 5-act chapter arc
- [x] Thumb concepts match title promise (3-way painted 3D key-art Test & Compare, Explorer lower-left, `≤3` words off hero)
- [x] Chapter teach-points listed (5 acts with `3+ DATA`, `SCALE`, `WHO`, `WHEN`, `3 FACT`)
- [x] Cold-open clock (`0:05` / `0:08` / `0:15` / `0:25` / `0:25–0:40 DATA+SCALE` / `<0:45` fact per `HOS-2026-11-E2`) written
- [x] Retention plan filled
- [x] Production checklist path noted: `11_Upload-Package/PRODUCTION_CHECKLIST_V2.md`

**Pre-build Topic Audit (`§1–§6`) Reviewed by:** `macbook-2` (`J2473` Rule-E Review) on `2026-11-10`  
**Final Pre-VO Sign-off (`§7` after Script `≥90` & `FACT_NOTES` gates):** *(leave unsigned until script scores `≥90` upon active WIP entry)*
