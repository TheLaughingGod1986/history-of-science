# Pre-build vidIQ audit — History of Science (`HOS:104` — Rule-E `GO` in `next_hos`)

> **RULE-E TOPIC REVIEW & UNVERIFIED CLAIMS NOTICE (`J2809` / `J2810`, 14 Nov 2026):**
> This topic (`HOS:104`) passed its **Rule-E topic go/no-go review (`J2810`: `GO`, `96 / 100` · `9.60 / 10` Opportunity Score; see [`TOPIC_GO_NO_GO_SHEET.md`](TOPIC_GO_NO_GO_SHEET.md) and [`TOPIC_OPPORTUNITY_SCORE.md`](TOPIC_OPPORTUNITY_SCORE.md))** and remains pre-cleared in **`jobs/WIP.json` `next_hos` (Rule G)** awaiting an open active HOS WIP slot.
> All historical and scientific claims below — including Galileo's 1638 lantern test, Ole Rømer's 1676 Jupiter moon Io eclipse timing numbers, Hippolyte Fizeau's 1849 720-tooth brass wheel RPM/distance/speed numbers across Paris, and Léon Foucault's 1850/1862 rotating-mirror water-tube and speed numbers — remain **UNVERIFIED** working notes and are **not cleared for narration or Short opens**. Before any script lock, every claim must be backed by an exact quote in `SOURCES.md` and verified through the `facts` lane (`gemini-agy`).

---

## Episode

| Field | Value |
|-------|-------|
| ID / slug | `104_Roemer-Fizeau-Foucault-Speed-Of-Light` (`HOS:104`) |
| Working title (A) | `How Did We Measure the Speed of Light? (A 720-Tooth Wheel)` (`58 chars`, `0` exact collisions) |
| Title B (T&C) | `The 720-Tooth Wheel That Measured the Speed of Light` (`52 chars`, `0` exact collisions) |
| Title C (Rule 26) | `Speed of Light: How a 720-Tooth Wheel Measured It in 1849` (`57 chars`, `0` exact collisions) |
| Date pulled | `2026-11-14` (`J2809` on Mac mini · Rule-E `GO` review `J2810` on MacBook) |
| Rule-E Opportunity Score | **`9.60 / 10` (`96 / 100`) — `GO`** ([`TOPIC_OPPORTUNITY_SCORE.md`](TOPIC_OPPORTUNITY_SCORE.md) · [`TOPIC_GO_NO_GO_SHEET.md`](TOPIC_GO_NO_GO_SHEET.md)) |
| Credits used (approx) | `£0.00` (signed-out YouTube GB public search + `neighbours.py`) |
| Brand guardrails | Wonder over fearbait · no conspiracy · HOS lane (a familiar thing — flipping a light switch — and the mechanical brass wheel and telescopes that timed light before electronics) |

---

## 1. Success targets (this episode)

| Metric | Target |
|--------|--------|
| Title score | ≥ **90** (aim **95+**) |
| Primary keyword overall | `"how did we measure the speed of light"` / `"speed of light"` (`autocomplete = yes` in YouTube GB, retrieved `2026-11-14`) |
| Hook promise | Candidate hook (unverified): In 1849 a French physicist spun a 720-tooth brass wheel in a Paris tower and fired a lantern beam across the city to a mirror 8.6 km away — timing the speed of light on Earth when a spinning tooth blocked the returning flash |
| Retention design | Proof-first `0:05–0:15` on the spinning 720-tooth brass cogwheel eclipsing the returning pinpoint of light + 4 chronological acts (`1638 -> 1676 -> 1849 -> 1850/1862`) that earn the next minute |
| Packaging | 3-way Thumbnail Test & Compare concept (`720 TEETH` brass cogwheel slicing a golden beam vs Rule 14 bright `FASTER THAN HAND` Galileo hilltop lanterns vs `JUPITER WAS LATE` Io eclipse orbital clock; readable at `168×94`) |

---

## 2. Keyword research (Signed-Out YouTube Autocomplete & Competition Check · Rule 26, Retrieved `2026-11-14`)

Saved in `11_Upload-Package/evidence_2026-11-14_public_search.json`:

| Keyword | Autocomplete (`suggest()`) | GB Top-5 Competition (`public_search.py`, `2026-11-14`) | Role (title / desc / chapter / Shorts) | Keep? |
|---------|---------------------------|----------------------------------------------------------|----------------------------------------|-------|
| `how did we measure the speed of light` | **yes** (`how did we measure the speed of light`, `how did they measure the speed of light`) | `Think Like Feynman` `52,487` · `Rational Thinker` `2,001,964` · `Carter Studios - Physics` `799,836` · `Veritasium` `24,352,264` · `Science Simplified 4 All` `15,073` | Primary search phrase (Title A + Desc line 1 + tags) | **Keep** |
| `speed of light` | **yes** (`speed of light`, `speed of light explained`, `speed of light visualization`) | `Feynman Reborn` `254,511` · `Veritasium` `24,352,264` · `The Sleepy Scientist` `53,862` · `Calm Space` `7,646` · `Sleep On Science` `80,681` | Umbrella subject noun (Title A, B, C + Desc + tags) | **Keep** |
| `How Did Jupiter's Moons Measure the Speed of Light?` | **no** | `SciShow Space` `214,651` · `David Butler` `20,436` · `Tycho` `3,990` · `VideoFromSpace` `3,315` · `Rational Thinker` `2,001,976` | Short `S01` candidate question title (`0` exact collisions) | **Keep** |
| `Why Does Light Slow Down in Water? (Foucault's 1850 Test)` | **no** | `FloatHeadPhysics` `152,451` · `Fermilab` `1,309,684` · `Looking Glass Universe` `116,595` · `Arvin Ash` `303,924` · `3Blue1Brown` `2,896,005` | Short `S02` candidate question title (`0` exact collisions) | **Keep** |

- **Rule 26(a) Exact Phrase & Two Ranking Videos (`2026-11-14`):**
  - **Phrase:** `"how did we measure the speed of light"` / `"speed of light"`
  - **Ranking Video 1:** `pTn6Ewhb27k` — *Why No One Has Measured The Speed Of Light* (`Veritasium`, **`24,352,264` views**, retrieved `2026-11-14`)
  - **Ranking Video 2:** `Jl1I4MA-TaU` — *How the Speed of Light Was First Measured* (`Rational Thinker`, **`2,001,964` views**, retrieved `2026-11-14`; plus `Carter Studios - Physics` `8z1WR4b0hJY` **`799,836` views** and `ayuta` `a6gl8KZM0PM` *How to find the speed of light (Fizeau experiment)* **`512,454` views**)
- **Decision:** Candidate primary title = `How Did We Measure the Speed of Light? (A 720-Tooth Wheel)` (Title A, `58 chars`) / `Speed of Light: How a 720-Tooth Wheel Measured It in 1849` (Title C, `57 chars`, exact phrase first)
- **Candidate description first 100 chars (unverified until `SOURCES.md` check):** `How did we measure the speed of light on Earth in 1849 using a spinning 720-tooth brass cogwheel?`

---

## 2b. Neighbour pass (blocking · `STUDIO_PLAYBOOK.md` §2 Step 4, Retrieved `2026-11-14`)

Saved in `11_Upload-Package/evidence_2026-11-14_neighbours.json` and `11_Upload-Package/evidence_2026-11-14_public_search.json`:

| # | Views (`2026-11-14`) | Channel (internal) | id & URL | Title | Subject words we reuse |
|---:|------:|--------------------|----------|-------|------------------------|
| 1 | `24,352,264` | Veritasium (`neighbours.py`) | [`pTn6Ewhb27k`](https://youtu.be/pTn6Ewhb27k) | *Why No One Has Measured The Speed Of Light* | `speed of light`, `measure`, `fizeau`, `roemer`, `mirror` |
| 2 | `17,596,419` | Veritasium (`neighbours.py`) | [`NIk_0AW5hFU`](https://youtu.be/NIk_0AW5hFU) | *There Is Something Faster Than Light* | `speed of light`, `light` |
| 3 | `10,047,754` | Vsauce (`neighbours.py`) | [`ACUuFg9Y9dY`](https://youtu.be/ACUuFg9Y9dY) | *Would Headlights Work at Light Speed?* | `light speed`, `speed of light` |
| 4 | `9,990,677` | Kurzgesagt (`neighbours.py`) | [`IXxZRZxafEQ`](https://youtu.be/IXxZRZxafEQ) | *What Is Light?* | `light`, `speed of light`, `wavelength` |
| 5 | `7,134,459` | PBS Space Time (`neighbours.py`) | [`msVuCEs8Ydo`](https://youtu.be/msVuCEs8Ydo) | *The Speed of Light is NOT About Light* | `speed of light`, `vacuum` |
| 6 | `4,304,501` | minutephysics (`neighbours.py`) | [`lR4tJr7sMPM`](https://youtu.be/lR4tJr7sMPM) | *How to break the speed of light* | `speed of light`, `water` |
| 7 | `3,695,293` | TED-Ed ★ (`neighbours.py`) | [`Op3AYaJc0Xw`](https://youtu.be/Op3AYaJc0Xw) | *Light seconds, light years, light centuries: How to measure extreme distances - Yuan-Sen Ting* | `light`, `measure`, `distance`, `speed of light` |
| 8 | `2,001,964` | Rational Thinker (`public_search.py`) | [`Jl1I4MA-TaU`](https://youtu.be/Jl1I4MA-TaU) | *How the Speed of Light Was First Measured* | `speed of light`, `measured`, `roemer`, `io` |
| 9 | `1,816,164` | TED-Ed ★ (`neighbours.py`) | [`J1yIApZtLos`](https://youtu.be/J1yIApZtLos) | *Is light a particle or a wave? - Colm Kelleher* | `light`, `wave`, `particle` |
| 10 | `1,276,309` | TED-Ed ★ (`neighbours.py`) | [`O0PawPSdk28`](https://youtu.be/O0PawPSdk28) | *Light waves, visible and invisible* | `light`, `waves` |

**Proposed subject-only tags (8 tags, zero channel names):**  
`how did we measure the speed of light, speed of light, fizeau speed of light experiment, ole roemer jupiter io speed of light, foucault rotating mirror speed of light, history of physics experiments, 720 tooth wheel speed of light, galileo speed of light lanterns`

---

## 3. Title ABC (score before VO)

| | Title | Chars | Collisions (`2026-11-14`) | Role & Notes | Keep? |
|---|-------|------:|-----------:|--------------|-------|
| A | `How Did We Measure the Speed of Light? (A 720-Tooth Wheel)` | 58 | 0 | **Main (`LEARNINGS.md` Rules 1, 23, 26):** Exact autocomplete question `"how did we measure the speed of light"` + concrete apparatus hook | **Keep (Primary Proposal)** |
| B | `The 720-Tooth Wheel That Measured the Speed of Light` | 52 | 0 | **Test & Compare (`Rule 23`):** Concrete mechanical apparatus + outcome stakes | **Keep (T&C Arm 2)** |
| C | `Speed of Light: How a 720-Tooth Wheel Measured It in 1849` | 57 | 0 | **Rule 26 Variant (`≤70 chars`):** Starts verbatim with exact autocomplete phrase `"speed of light"` | **Keep (T&C Arm 3)** |
| Reject | `The Determination of the Velocity of Light \| History of Science` | 64 | — | Textbook jargon + forbidden series suffix | **Reject** |

---

## 3b. Script reviewer (blocking before VO — not run; waits on Rule G slot + `SOURCES.md` / `facts` lane)

- [x] **Rule-E Topic Go/No-Go Review (`J2810`, `2026-11-14`, `macbook`):** **GO (`96 / 100` · `9.60 / 10` Opportunity Score)** — Pre-cleared in `jobs/WIP.json` `next_hos` under Rule G ([`TOPIC_GO_NO_GO_SHEET.md`](TOPIC_GO_NO_GO_SHEET.md), [`TOPIC_OPPORTUNITY_SCORE.md`](TOPIC_OPPORTUNITY_SCORE.md))
- [ ] Active HOS WIP slot open (`len(WIP.json["hos"]) < 6`)
- [ ] `SOURCES.md` exact quotes + `facts` lane verification completed (required before script lock)
- [ ] Score ≥ **90 / 100** (`npm run review:script`)

---

## 4. Packaging & Thumbnail Test Plan (Zero Spend Until Script + VO PASS)

| Variant | Concept (Painted 3D House Style, Explorer ≤18% Lower-Left) | Hook Text (`≤3` Words, Clear of `168×94` Badge) | Role |
|---|---|---|---|
| **Thumb A** | Close-up of Fizeau's gleaming **720-tooth brass cogwheel** spinning in a dark Paris tower as a razor-sharp golden beam of light is sliced off by a brass tooth | `720 TEETH` | Control (Apparatus mechanism) |
| **Thumb B (Rule 14)** | Bright daylight/twilight contrast over Paris rooftops: a brilliant golden beam shooting from a brass telescope across to a distant mirror on Montmartre while a giant brass gear turns in the foreground | `TIMED BY GEARS` | Test & Compare Arm B (Bright contrast) |
| **Thumb C** | Glowing Jupiter and its moon Io casting a sharp black shadow cone toward a brass Paris Observatory telescope and pocket watch | `22 MINUTES LATE` *(verify exact number in `SOURCES.md` before render)* | Test & Compare Arm C (Astronomical scale) |

---

## 5. Two Search-Titled Shorts (`LEARNINGS.md` Rules 1, 2, 24, 27, 28 — Unverified Concepts Only)

| Short | Candidate Question Title (`0` Exact Collisions) | Frame 0 (`mode: "cover"`, `0%` Explorer, `0%` Bars) & `0.0 s` Hook Text | Payoff (`≥70%` Runtime, `<1.0 s` Tail, Zero CTA) |
|---|---|---|---|
| **S01** | `How Did Jupiter's Moons Measure the Speed of Light?` (`51 chars`) | Full-bleed moving shot of Jupiter's moon Io disappearing into Jupiter's shadow cone while a brass Paris Observatory pocket watch ticks · Hook: `1676 ECLIPSE` (`#FFE000` on `1676`) | Rømer realised Io wasn't slowing down — its light took extra minutes to cross Earth's orbit, giving the first proof that light has a finite speed *(verify in `SOURCES.md`)* |
| **S02** | `Why Does Light Slow Down in Water? (Foucault's 1850 Test)` (`57 chars`) | Close moving shot of a high-speed spinning brass mirror splitting a bright beam of light through a glass tube of water · Hook: `SLOWER IN WATER` (`#FFE000` on `SLOWER`) | Foucault's 1850 rotating mirror proved the water beam arrived later and deflected further than the air beam — refuting Newton's particle prediction *(verify in `SOURCES.md`)* |
