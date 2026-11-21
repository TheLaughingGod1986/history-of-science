# Pre-build vidIQ & Public-Search Audit — `HOS:125` (`What Causes the Tides? (Galileo Got It Wrong)`)

**Hard gate:** Run **before** locking script, VO, prompts, or picture gen for any new long.
**Status (`J3214`, 20 Nov 2026):** Keyword & competition sections populated from signed-out GB `public_search.py` and `neighbours.py` (`£0.00`). VidIQ app numeric scores require Ben's login (or Chief/Ben waiver) when `HOS:125` enters active WIP. **All historical/scientific facts below are UNVERIFIED working notes pending `SOURCES.md` and the `facts` lane.**

---

## Episode

| Field | Value |
|-------|-------|
| ID / slug | `125_Galileo-Newton-Laplace-What-Causes-The-Tides` |
| Working title | `What Causes the Tides? (Galileo Got It Wrong)` (`45` chars) |
| Date pulled | `2026-11-20` (`J3203` + `J3214` verification) |
| Credits used (approx) | `0` (`£0.00`) |
| Brand guardrails | Wonder over fearbait · no conspiracy · HOS lane (a familiar thing, and the moment we found out) |

---

## 1. Success targets (this episode)

| Metric | Target |
|--------|--------|
| Title score | ≥ **90** (aim **95+**; vidIQ login pending active WIP) |
| Primary keyword overall | `what causes the tides` (autocomplete: **yes**, `6` GB suggestions; `9` distinct `≥1M` on-tides videos across `neighbours.json` + `public_search.json`) |
| Hook promise | How Galileo bet his most famous book on the wrong cause of the tides — and how Newton, Laplace, and a Victorian brass machine finally cracked how the ocean moves |
| Retention design | 5 cause-and-effect acts (`Kepler/Galileo barge` → `1-tide vs 2-tide contradiction` → `Newton differential tractive force` → `Laplace forced ocean-basin waves twist` → `Thomson 1872 / Doodson 1944 tide machines`) |
| Packaging | Thumb readable at `168×94`; clear left/top band, `2–3` words (`GALILEO WAS WRONG` / `TWO TIDES DAILY` / `NOT JUST PULL`), warm 3D period palette, Explorer small lower-left |

---

## 2. Keyword research (`public_search.py` / `neighbours.py`, GB signed-out, 20 Nov 2026)

| Keyword | Autocomplete | Top GB Competitors | Role (title / desc / chapter / Shorts) | Keep? |
|---------|--------------|--------------------|----------------------------------------|-------|
| `what causes the tides` | **yes** (`6` suggestions) | Waterlust `2.50M`, AtomicSchool `2.06M`, minutephysics `1.79M`, NOAA `1.11M` | **primary** (Title A + desc line 1 + tags) | **Keep** |
| `how do tides work` | **yes** (`10` suggestions) | Waterlust `2.50M`, AtomicSchool `2.06M`, BrainStuff `1.65M`, NOAA `1.11M` | **secondary** (desc + tags) | **Keep** |
| `why are there two tides a day` | **yes** (`3` suggestions) | TED-Ed `605k`, Dr. Becky `200k`, BBC `203k` | **secondary / Title B / Short S01 seed** | **Keep** |
| `tides explained` | **yes** (`8` suggestions) | StarTalk `2.98M`, Waterlust `2.50M`, PBS Space Time `2.13M`, AtomicSchool `2.06M` | **umbrella** (tags + suggested alignment) | **Keep** |

**Decision:** Primary keyword for title lead = `What Causes the Tides?`
**Description first 100 chars must include:** `What causes the tides — and why Galileo got them wrong before Newton, Laplace, and a brass machine...`

---

## 3. Title ABC (checked for collisions `2026-11-20`; vidIQ scores pending active WIP)

**Growth System v2 + LEARNINGS Rule 15 & Rule 26:** search phrase first · `≤50` characters ideal (`≤70` max) · no series suffix · `0` exact collisions with live videos.

| | Title | Chars | Exact Collisions | Keep? |
|---|---|---:|---:|---|
| **A (Primary)** | `What Causes the Tides? (Galileo Got It Wrong)` | `45` | `0` | **Keep (Lead)** |
| **B (Test & Compare)** | `Why Are There Two Tides a Day? Newton's Answer` | `46` | `0` | **Keep (T&C B)** |
| **C (Backup)** | `What Causes the Tides? Why There Are Two a Day` | `46` | `0` | **Keep (Backup)** |
| **Reject (Short S01 old)** | `Why Are There Two Tides a Day?` | `30` | **COLLISION** (`mpRJhhbKLFc` TED-Ed) | **Reject** |
| **Short S01 (Approved)** | `Why Does the Moon Make Two Tides a Day?` | `39` | `0` | **Keep (Short 1)** |
| **Short S02 (Approved)** | `What Did Galileo Get Wrong About the Tides?` | `43` | `0` | **Keep (Short 2)** |

---

## 4. Outlier / competitive patterns (on-brand only)

| Outlier / pattern | Views | Steal (structure) | Do **not** copy |
|---|---|---|---|
| `PBS Space Time` *What Physics Teachers Get Wrong About Tides!* (`pwChk4S99i4`) | `2,133,852` | Myth-correction tension (horizontal tractive force vs naive vertical pull) | Modern studio lecture format / heavy vector calculus |
| `Waterlust` *How the tides REALLY work* (`bPhhYhN0FAc`) | `2,501,261` | Real coastal visual stakes + dynamic ocean-basin wave framing | Drone-documentary pacing |
| `TED-Ed` *Why are there two tides a day?* (`mpRJhhbKLFc`) | `605,383` | Clean two-tide paradox hook | Exact title (collision) or textbook-only explanation |

---

## 5. Incorporate into the build (chapter arc & physics guardrails — UNVERIFIED)

**5-part chapter list (draft for script stage):**
1. **Part 01 (0:00–1:30, no chapter card):** Proof-first open at a draining Bay of Fundy harbour (boats on mud → floating 6 h later, `>10 m` / up to `~16 m` range; "twice a day on most coasts" — never "everywhere"); Kepler (`1609`) proposes lunar attraction.
2. **Part 02 (1:30–3:15):** Galileo (`1616` *Discourse on the Tides*, `1632` *Dialogue* Day 4) rejects the Moon as "occult" and bets everything on his Venetian fresh-water barge analogy — but his mechanism predicts one tide a day instead of two.
3. **Part 03 (3:15–5:00):** Newton (`1687` *Principia*) applies universal gravitation — differential horizontal (tractive) forces sliding water toward both sides of Earth, plus the Sun's ~46% share creating spring and neap tides.
4. **Part 04 (5:00–6:50, Midpoint Twist):** "Case closed? Wrong." Laplace (`1775–1776`) proves the ocean cannot keep up with the Moon; tides are forced waves sloshing around rotating ocean basins and coastlines — explaining diurnal coasts, phase lags, and Fundy's basin resonance.
5. **Part 05 (6:50–8:45):** Sir William Thomson (`1872–1873`, later Lord Kelvin — WHO card must use `Sir William Thomson` in 1872 scenes) builds the brass harmonic tide-predicting machine; Arthur Doodson runs tide machines at Bidston Observatory ("Position Z") to pick the Normandy D-Day window (`1944`); hand-off to next film.

---

## 6. Retention plan (whole-video watch)

| Minute zone | Job | Picture / VO note |
|---|---|---|
| `0:00–0:05` | Answer image / curiosity spike | Bay of Fundy harbour boats stranded on wet mud, sea rushing back in (3D cartoon, moving) |
| `~0:08` | Title question | "What causes the tides — and why did Galileo get them completely wrong?" |
| `~0:15` | Promise | How a sloshing barge, a differential pull, and a brass machine cracked the moving sea |
| `~0:25` | Stakes | Why predicting the tides mattered to every sailor, harbour, and fleet |
| `0:25–0:45` | First fact + early DATA+SCALE | Bay of Fundy `~16 m` tidal range vs a 4–5 storey house (`SOURCES.md` required) |
| `~5:00` | Midpoint twist | Newton's two smooth bulges fail real ports → Laplace's dynamic ocean waves |
| `~8:30` | Payoff + hand-off | Brass predictor → D-Day window → hand-off line (no goodbye, no subscribe ask) |

---

## 7. Sign-off (block production until checked)

- [x] Signed-out public search & neighbour gate PASS (`2026-11-20`)
- [x] Title ABC collision-checked (`0` collisions) & Short S01 disambiguated (`J3214`)
- [ ] VidIQ app numeric scores pulled (or waived) when entering active WIP
- [ ] `SOURCES.md` verbatim quotes + `facts` lane (`gemini-agy`) PASS
- [ ] Script reviewer ≥ `90` & `gate:episode` PASS

**Rule-E Topic Review Sign-off:** `macbook-2` (`Gemini 4 Argon (High)`, `J3214`, `2026-11-20`) — **GO (`95.9 / 100`) in `next_hos` under Rule G. NOT cleared for script lock, VO, or picture spend until active WIP slot opens.**
