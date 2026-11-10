# 030 script v01: notes for review (J0478)

Script: `tectonics_script_master_v01.md` (with `opening_and_outline_v00.md`, `SOURCES_v00.md` and `SOURCES_v01.md`).

**Draft only (J0478, Gemini Argon, 17 Oct 2026).** Built from `030_Wegener-Tharp-Plate-Tectonics/opening_and_outline_v00.md` and the neighbour and search evidence in `IDEAS_2026-10-17_J0470.md` (`evidence_2026-10-17_J0470/n_tectonics.md` PASS — 6 strictly on-topic education videos ≥ 1M views, including 3 TED-Ed ≥ 1M: **MinuteEarth *Plate Tectonics Explained* (`kwfNGatxUJI`, 3.27M)**, **TED-Ed ★ *The colossal consequences of supervolcanoes - Alex Gendler* (`hDNlu7Qf6_E`, 2.33M)**, **SciShow Kids *All About Volcanoes* (`K7Oq9_DU1Mc`, 2.02M)**, **TED-Ed ★ *Why do buildings fall in earthquakes? - Vicki V. May* (`H4VQul_SmCg`, 1.90M)**, **SciShow Kids *What Causes Earthquakes?* (`AArne-wh_Uc`, 1.76M)**, and **TED-Ed ★ *Why are earthquakes so hard to predict? - Jean-Baptiste P. Koehl* (`jhRuUoTnA6g`, 1.39M)**, plus **National Geographic *Continental Drift 101* (`Wq9kLzm36h0`, 984.4k)** and **CrashCourse *The Plate Tectonics Revolution* (`7CPv0NSIG2M`, 816.8k)**, alongside `public_search.md` showing `"alfred wegener continental drift"` autocompleting in GB search and all 5 top GB slots for `"marie tharp ocean floor"` under 191k views). The topic isn't locked yet: Chief locks `030` and the working title pair first, then reviews/signs off this script and queues the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

Structure (*Reference lessons* §1, scripts from 011 on): every chapter opens cold and ends on a question the next one answers; the midpoint twist ("Case closed? Wrong." — even after Marie Tharp discovered the V-shaped rift valley splitting the 16,000-kilometre Mid-Atlantic Ridge in Autumn 1952 and Howard Foster's 1953 earthquake epicentre map matched her rift along a 65,000-kilometre global seam, geologists still couldn't explain why the planet didn't expand until Harry Hess proposed seafloor spreading in November 1962 and Fred Vine and Drummond Matthews proved it on 7 September 1963 using symmetrical normal and reversed magnetic zebra stripes frozen into cooling basalt below 580 °C) lands in Part 04; the popular misconception ("Many people picture Earth's tectonic plates floating on an underground ocean of liquid red-hot magma") is raised and explained away in Part 05 via solid mantle creep and continental buoyancy (`2.7 g/cm³` granite vs `3.0 g/cm³` basalt on `3.3 g/cm³` solid mantle); the ending hands off directly to `031` (*Archimedes' Bathtub, the Golden Crown & Buoyancy: Archimedes of Syracuse (~250 BC) & Galileo's 1586 Hydrostatic Balance*), with no goodbye and no subscribe ask. Five VO parts, matching 009–029.

## Marker count (v01)

Run on `tectonics_script_master_v01.md`: `grep -o "DATA:" … | wc -l`, and the same for each marker.

| Marker | Count | Where | Rule |
|---|---:|---|---|
| `DATA` | **6** | 1) inked parchment map and cross-section comparing Wegener's 1912 continental-shelf jigsaw fit (South America and Africa matching across 4,500 km, with Mesosaurus fossils separated today by 5,000 km of salt ocean) and Marie Tharp's 1952 Mid-Atlantic Ridge rift valley (16,000 km long, 1.5–3 km deep, spreading at 2.5 cm/year) (0:34); 2) inked rate-and-time scale bar showing 2.5 cm/year × 200,000,000 years = 5,000 km (Width of the Atlantic Ocean) (0:52); 3) inked four-line "torn newspaper" diagram on period paper showing (1) 200 m continental shelf fit, (2) Appalachian–Caledonian mountain chain alignment, (3) Mesosaurus & Glossopteris fossil bands across 5,000 km, and (4) Harold Jeffreys's 1924 calculation that tidal force is 10¹⁰× too weak to plough granite through solid basalt (1:58); 4) inked cross-section and overlay on period paper showing sonar echo depth (d = ½ v t) revealing the Mid-Atlantic Ridge with Marie Tharp's 1.5–3 km deep V-shaped rift valley at its crest, matched 1-to-1 by Howard Foster's 1953 earthquake epicentre dots along a 65,000 km global seam (3:42); 5) inked seafloor conveyor-belt and magnetic-barcode diagram on period paper showing mantle upwelling at the mid-ocean rift, magnetite locking in Earth's magnetic field below ~580 °C, symmetrical normal/reversed magnetic stripes on both sides of the ridge, and oceanic crust age (≤ 200 million years vs 4,000 million years for continents) (5:28); 6) animated timeline building 6 Jan 1912 & 1915 · 1924, 15 Nov 1926 & Nov 1930 · Autumn 1952 & 1953 · Nov 1962 · 7 Sep 1963 · Today alongside an inked density diagram comparing continental granite (2.7 g/cm³) and oceanic basalt (3.0 g/cm³) floating on solid mantle rock (3.3 g/cm³) (6:43) | 3 or more per long, including the animated timeline |
| `SCALE` | **6** | 1) 2.5 centimetres a year — the exact speed your fingernails grow, yet over 200 million years enough to open the 5,000-kilometre Atlantic Ocean (0:34); 2) moving no faster than your fingernail grows, two continents drift 5,000 kilometres apart in 200 million years (0:52); 3) the tidal push Wegener relied on was ten billion times too weak — like trying to push a brick wall through solid concrete by blowing on it (1:58); 4) a continuous underwater mountain chain and rift valley stretching 65,000 kilometres around the planet — long enough to wrap around Earth's equator more than one and a half times (3:42); 5) while continental rocks are up to 4 billion years old, the entire ocean floor recycles itself like a conveyor belt every 200 million years (5:28); 6) granite continents (2.7 g/cm³) float high above basalt ocean crust (3.0 g/cm³) on the denser mantle (3.3 g/cm³) like tall wooden blocks floating beside thin iron plates (6:43) | Every `DATA` number gets a `SCALE:` comparison (`grep -c "SCALE:"` ≥ `DATA:` count) |
| `WHO` | **10** | Alfred Wegener (0:34), Marie Tharp (0:34), Harold Jeffreys (1:58), Rollin T. Chamberlin (2:32), Bruce Heezen (3:08), Howard Foster (3:42), Harry Hess (4:53), Arthur Holmes (4:53), Fred Vine (4:53), Drummond Matthews (4:53) | First mention only, role right for the scene's year (4 words or fewer) |
| `WHEN` | **19** | Frankfurt 6 January 1912 (0:00), New York Autumn 1952 (0:00), 6 January 1912 (0:34), Autumn 1952 (0:34), December 1910 (1:28), 6 January 1912 (1:28), 1915 (1:28), 1924 (1:58), 15 November 1926 (2:32), November 1930 (2:32), Autumn 1952 (3:08), 1953 (3:42), 1957 (3:42), 1929 (4:53), November 1962 (4:53), 7 September 1963 (4:53), 1912–1963 (6:43), ~250 BC (7:45), 1586 (7:45) | Every spoken date or era; later dates drop onto the timeline |
| `FACT` | **4** | Died rescuing Arctic team (1:28); Barred from research ships (3:08); Magnetic field flips north-south (4:53); Earth's mantle is solid rock (6:43) | 2–4 per long (4 words or fewer per card) |

## Craft checks (*Reference lessons* §1 + *Polish pass*)

- **First-minute timings:** Answer image by 0:03 (Alfred Wegener in Frankfurt on 6 January 1912 sliding South America and Africa together on a globe as the Atlantic drains to reveal Marie Tharp in 1952 inking the 16,000-kilometre Mid-Atlantic Ridge V-shaped rift valley), title question by 0:07, promise by 0:15, stakes by 0:25, first concrete answer & real fact (Wegener's 6 January 1912 continental-shelf and fossil fit + Marie Tharp's Autumn 1952 16,000 km Mid-Atlantic Ridge rift valley spreading at 2.5 cm/year) by 0:34.
- **Explorer limits:** 2 beats total (`[EXPLORER ACTS: once. …]`), at 1:05 (Part 01, outside the first minute) and 6:05 (Part 04 standing astride Marie Tharp's mid-ocean rift with a flipping brass compass as symmetrical magnetic zebra stripes paint onto the spreading seabed).
- **Chapter cold opens & cliffhanger questions:** Part 01 ends on why geologists mocked Wegener as a crank and what fatal mistake in his theory cost him the argument before he vanished into the Arctic snow; Part 02 opens cold on Wegener's December 1910 atlas discovery, his 6 January 1912 Frankfurt lecture and 1915 Pangaea book ("torn newspaper" analogy, Appalachian–Caledonian mountains, freshwater *Mesosaurus* fossils), Harold Jeffreys's 1924 10¹⁰× tidal-force refutation, the 15 November 1926 New York symposium, and Wegener's November 1930 Greenland rescue trek and death, ending on how continents move if they cannot plough through the seabed and why the answer stayed hidden underwater until a woman barred from ships drew the bottom of the Atlantic; Part 03 opens cold on Marie Tharp plotting six transatlantic sonar profiles at Columbia in Autumn 1952, discovering the V-shaped rift valley along the 16,000-kilometre Mid-Atlantic Ridge, Bruce Heezen dismissing it as "girl talk", and Howard Foster's 1953 transparent earthquake overlay matching her rift along a 65,000-kilometre seam, ending on why Earth doesn't swell up like a balloon and what proved the seabed is a moving conveyor belt; Part 04 opens cold on the midpoint twist ("Case closed? Wrong." — Harry Hess's November 1962 seafloor-spreading conveyor belt and Fred Vine and Drummond Matthews's 7 September 1963 *Nature* discovery of symmetrical magnetic zebra stripes frozen below 580 °C), ending on whether continents float on an underground sea of liquid red-hot magma; Part 05 opens cold on the liquid-magma misconception, explains solid mantle creep and continental buoyancy, and hands off to Archimedes (~250 BC) and 22-year-old Galileo Galilei's 1586 hydrostatic balance (`031`).
- **Quirky anecdote before the hard idea:** Alfred Wegener comparing South America and Africa to two pieces of torn newspaper where every line of type reads across the tear; Bruce Heezen dismissing Marie Tharp's V-shaped rift valley as "girl talk" and making her erase the map until Howard Foster's transparent plastic sheet of earthquake dots landed dead-centre along her canyon.
- **Rivalry / tension:** Outsider meteorologist Alfred Wegener savaged by the geological establishment in 1924–1926 and dying on the Greenland ice sheet in 1930, vindicated 33 years later by a woman barred from boarding research ships and two 1963 Cambridge geophysicists.
- **Misconception explained away:** "Many people picture Earth's tectonic plates floating on an underground ocean of liquid red-hot magma" — explained via earthquake waves proving Earth's mantle is 99% solid rock that creeps slowly like glacier ice while lighter granite continents (`2.7 g/cm³`) float high above basalt ocean plates (`3.0 g/cm³`) on the denser mantle (`3.3 g/cm³`) (Part 05, 6:43).

## For Chief to decide

1. Lock **030 = Continental Drift & Plate Tectonics: Alfred Wegener's 1912 Jigsaw Map & Marie Tharp's 1952 Mid-Atlantic Ocean Rift (1912–1963)** and pick the 2-way Test & Compare working title pair:
   - **A (Subject + hook, §1 rule 11):** *Continental Drift: The Woman Who Mapped the Hidden Ocean Rift* (61 chars)
   - **B (Search question, §1 rule 2):** *Why Geologists Mocked Moving Continents Until They Mapped the Sea* (65 chars)
   - **Alt (Search / twist question):** *How a Map Drawn by a Woman Barred From Ships Proved Plate Tectonics* (67 chars)
2. Review `tectonics_script_master_v01.md` (92.0/100 PASS), then queue the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

## Score (`npm run review:script`)

```text
# tectonics_script_master_v01.md

**Decision:** PASS · **Score:** 92 / 100

| Dimension | Score |
|---|---:|
| hook | 9.5 |
| curiosity | 9.1 |
| storytelling | 8 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 8.6 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1643 · Est. min: 11 · Chapters: 4

## Cold open excerpt

> Why did geologists laugh a German explorer out of the room for saying South America and Africa were once joined — until a woman barred from ships mapped the ocean floor? By the end of this film, you'll see why Alfred Wegener risked his life and froze to death on the Greenland ice

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 92/100 — proceed to VO after production checklist.

Pass threshold: 90
```
