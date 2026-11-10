# 042 script v01: notes for review (J0539)

Script: `laser_script_master_v01.md` (with `opening_and_outline_v00.md`, `SOURCES_v00.md` and `SOURCES_v01.md`).

**Draft only (J0539, Gemini Argon, 18 Oct 2026).** Built from `042_Maiman-Kao-Einstein-Laser-Fibre-Optics/opening_and_outline_v00.md` and the neighbour and search evidence in `IDEAS_2026-10-18_J0530.md` (`evidence_2026-10-18_J0530/n_laser.md` PASS — 4 education videos ≥ 1M views: **TED-Ed ★ *How does laser eye surgery work? - Dan Reinstein* (`XPDVmBg5DeE`, 6.83M)**, **TED-Ed ★ *How does chemotherapy work? - Hyunsoo Joshua No* (`RgWQCGX3MOk`, 6.23M)**, **minutephysics *How lasers work (in theory)* (`y3SBSbsdiYg`, 3.15M)**, and **SmarterEveryDay *How Lasers Work (in practice) - Smarter Every Day 33* (`lW4Uq_2VPhE`, 1.60M)**, plus **Khan Academy *Total internal reflection* (`WRuatAcd2WY`, 557.1k)** and ***Convex lenses* (`K0sjZ5nqQ7g`, 463.3k)**, alongside Veritasium's 12 Oct breakout ***The Absurd Engineering Behind the Internet* (`NiCgcUTL9_Q`, 9.03M views)** and `public_search.md` showing all 5 top GB search results for `"theodore maiman first ruby laser"` under 3k views and all 5 for `"charles kao fiber optics glass"` under 54k views). The topic isn't locked yet: Chief locks `042` and the working title pair first, then reviews/signs off this script and queues the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

Structure (*Reference lessons* §1, scripts from 011 on): every chapter opens cold and ends on a question the next one answers; the midpoint twist ("Case closed? Wrong! Arthur Schawlow and Charles Townes publicly declared that pink ruby could never work as a laser!" — after experts dismissed synthetic pink ruby based on a mistaken 1% fluorescence quantum efficiency measurement, 32-year-old Theodore Maiman at Hughes Research Laboratories in Malibu measured ruby's true efficiency at ~70%, pumped a 1 cm × 2 cm silvered synthetic ruby rod inside a coiled GE xenon photographer's flashlamp on 16 May 1960 to fire the first 694.3 nm laser beam, and published in *Nature* on 6 August 1960 after *Physical Review Letters* rejected his paper without review) lands in Part 03; Daniel Colladon's 1842 sunlit water-fountain demonstration of total internal reflection and Charles Kao & George Hockham's January–July 1966 Harlow proof that trace iron (`Fe2+`) impurities caused the 1,000 dB/km loss in optical glass and that purifying fused silica below 20 dB/km would unlock long-distance optical fibre communication land in Part 04; the glassmakers' skepticism ("When Charles Kao claimed in nineteen sixty-six that glass could be made five thousand times clearer than a camera lens, critics scoffed that no furnace on Earth could remove every speck of iron from melted sand") is raised and explained away in Part 05 via Maurer, Keck, and Schultz's August 1970 17 dB/km vapour-deposited silica fibre at Corning (refined to 0.2 dB/km by 1979 and paired with 1987 erbium-doped fibre amplifiers to carry 99% of intercontinental internet traffic across >1.4 million km of undersea cables); the ending hands off directly to `043` (*Cholera, the 1854 Broad Street Pump & How Clean Water Saved Millions: John Snow's 2 September 1854 Ghost Map in Soho, the Brewery Clue & Robert Koch's 1883 Comma Bacillus*), with no goodbye and no subscribe ask. Five VO parts, matching 009–041.

## Marker count (v01)

Run on `laser_script_master_v01.md`: `grep -o "DATA:" … | wc -l`, and the same for each marker.

| Marker | Count | Where | Rule |
|---|---:|---|---|
| `DATA` | **6** | 1) inked comparison chart on period paper contrasting ordinary torchlight (incoherent waves of many wavelengths spreading wide) vs Maiman's 16 May 1960 ruby laser (single 694.3-nanometre wavelength, coherent waves in lockstep) and 1960s optical glass (1,000 dB/km attenuation, losing 99% of light in 20 metres) vs Charles Kao's 1966 target (<20 dB/km) and modern silica fibre (0.2 dB/km, carrying 99% of intercontinental internet data at ~200,000 km/s) (0:34); 2) inked scale & bandwidth bar comparing a 100-micrometre human hair to a 9-micrometre optical fibre core carrying terabits of laser data per second across 99% of transoceanic internet routes (0:52); 3) inked quantum cascade diagram on period paper showing Einstein's 1917 stimulated emission (1 photon → 2 → 4 → 8 → 2^n coherent photons in phase) inside a parallel-mirror optical cavity once population inversion (>50% of atoms in excited state) is reached (1:58); 4) inked ruby-cavity & spectrum chart on period paper from Maiman (16 May 1960 / Nature 6 Aug 1960) showing the 1 cm × 2 cm pink ruby rod (0.05% Cr2O3 in Al2O3, ~70% fluorescence efficiency vs the mistaken 1% estimate) pumped above threshold (>950 V xenon flash) collapsing its red glow into a narrow, intense 694.3-nanometre laser spike (3:42); 5) inked attenuation-drop chart on period paper from Kao & Hockham (1966) and Corning (1970–1979) showing 1960s optical glass (1,000 dB/km loss — 99% lost in 20 m) vs Charles Kao's 1966 target threshold (20 dB/km — 1% surviving 1,000 m), Corning's August 1970 titanium-doped silica fibre (17 dB/km), and modern 1,550 nm silica fibre (0.2 dB/km — >95% surviving 1 km) (5:28); 6) animated timeline building 1842 · 1917 · 13 Nov 1957–1958 · 16 May 1960 · Jan–Jul 1966 · Aug 1970–1987 alongside >1.4 million kilometres of submarine optical cables carrying 99% of intercontinental internet traffic (6:43) | 3 or more per long, including the animated timeline |
| `SCALE` | **6** | 1) ordinary glass in nineteen sixty swallowed ninety-nine percent of a light beam in just twenty metres — the length of a cricket pitch — whereas today's purified glass fibres carry a laser pulse a hundred kilometres without losing the signal (0:34); 2) the glass core guiding this video across the ocean floor is just nine micrometres wide — ten times thinner than a single strand of your hair (0:52); 3) bounce a single photon back and forth between two mirrors just seventy times while triggering stimulated emission, and one particle of light multiplies into more than a sextillion identical waves marching in step (1:58); 4) inside a pink ruby crystal no bigger than the tip of your little finger, Maiman unleashed a pulse of red light brighter than the surface of the Sun (3:42); 5) purifying just a few parts per billion of iron out of melted quartz made glass five thousand times clearer than a camera lens — clear enough that a window pane a hundred kilometres thick would still let you see the light on the other side (5:28); 6) over one point four million kilometres of hair-thin glass fibres now lie across the ocean floor — enough to wrap around the Earth thirty-five times (6:43) | Every `DATA` number gets a `SCALE:` comparison (`grep -c "SCALE:"` ≥ `DATA:` count) |
| `WHO` | **7** | Albert Einstein (0:34), Theodore Maiman (0:34), Charles Kao (0:34), Charles Townes (1:28), Gordon Gould (1:28), Arthur Schawlow (3:08), Daniel Colladon (4:53) | First mention only, role right for the scene's year (4 words or fewer) |
| `WHEN` | **22** | Malibu 16 May 1960 (0:00), Harlow January 1966 (0:00), Malibu 16 May 1960 (0:21), 1917 (0:34), 16 May 1960 (0:34), January 1966 (0:34), 1916 (1:28), 1917 (1:28), 1954 (1:28), 13 November 1957 (1:28), December 1958 (1:28), 16 May 1960 (3:08), 6 August 1960 (3:08), 21 July 1969 (3:08), 1842 (4:53), July 1966 (4:53), 2009 (4:53), August 1970 (6:43), 1979 (6:43), 1987 (6:43), 1842–1987 (6:43), September 1854 (7:45) | Every spoken date or era; later dates drop onto the timeline |
| `FACT` | **4** | Notarised in a candy store (1:28); Paper rejected by top journal (3:08); Guided light inside a fountain (4:53); 99% of ocean internet is glass (6:43) | 2–4 per long (4 words or fewer per card) |

## Craft checks (*Reference lessons* §1 + *Polish pass*)

- **First-minute timings:** Answer image by 0:03 (Theodore Maiman on 16 May 1960 at Hughes Research Laboratories in Malibu firing the first 694.3 nm red laser beam from a pink synthetic ruby inside a coiled photographer's flashlamp, transitioning into laser pulses inside Charles Kao's 1966 glass optical fibre), title question by 0:07, promise by 0:15, stakes by 0:25, first concrete answer & real fact (Einstein's 1917 stimulated emission, Maiman's 16 May 1960 silvered pink ruby laser, and Kao's January 1966 pure-silica glass fibre) by 0:34.
- **Explorer limits:** 2 beats total (`[EXPLORER ACTS: once. …]`), at 1:05 (Part 01, outside the first minute) and 6:05 (Part 04 plucking rusty `Fe2+` iron specks out of a glass rod with a miniature magnetic wand so the red laser pulse zips cleanly from end to end).
- **Chapter cold opens & cliffhanger questions:** Part 01 ends on how Albert Einstein in 1917 discovered a hidden rule of atoms that let one particle of light clone itself into trillions; Part 02 opens cold on why candle/torch light scatters (spontaneous emission), Einstein's 1916–1917 stimulated emission, Charles Townes's 1954 ammonia microwave MASER, and Gordon Gould's 13 November 1957 Bronx candy-store notarised notebook coining "LASER", ending on why top experts insisted Theodore Maiman's pink ruby crystal could never work; Part 03 opens cold on the midpoint twist ("Case closed? Wrong! Arthur Schawlow and Charles Townes publicly declared that pink ruby could never work as a laser!" — the mistaken 1% textbook quantum efficiency vs Maiman's 70% measurement, the $25 coiled GE xenon flashlamp, the 16 May 1960 694.3 nm ruby laser, the *Physical Review Letters* rejection, and the 21 July 1969 Apollo 11 lunar retroreflector), ending on why 99% of laser light vanished after 20 metres inside 1960s glass fibres and how an engineer in England solved it; Part 04 opens cold on Daniel Colladon's 1842 sunlit water-fountain demonstration of total internal reflection and Charles Kao & George Hockham's January–July 1966 Harlow proof that trace iron (`Fe2+`) impurities caused the 1,000 dB/km loss and that <20 dB/km silica glass would carry laser data across oceans, ending on who took Kao's dare; Part 05 opens cold on glassmakers' skepticism, explains Corning's August 1970 17 dB/km vapour-deposited silica fibre ("Whoopee!"), the 1979 0.2 dB/km refinement, 1987 erbium-doped fibre amplifiers, and >1.4 million km of undersea cables carrying 99% of intercontinental internet traffic, and hands off to John Snow's September 1854 Broad Street pump cholera map in Soho, London (`043`).
- **Quirky anecdote before the hard idea:** Gordon Gould racing to a Bronx candy store on 13 November 1957 to have the shopkeeper notarise his "LASER" notebook; *Physical Review Letters* editor Samuel Goudsmit rejecting Maiman's discovery of the first laser without review; Donald Keck writing "Whoopee!" in his Corning lab notebook in August 1970.
- **Rivalry / tension:** Gordon Gould vs Charles Townes & Arthur Schawlow; underdog Theodore Maiman at Hughes Malibu vs Bell Labs, Columbia, and the Pentagon; Charles Kao & Corning vs telecom giants who dismissed glass fibres as too lossy.
- **Misconception explained away:** "When Charles Kao claimed in nineteen sixty-six that glass could be made five thousand times clearer than a camera lens, critics scoffed that no furnace on Earth could remove every speck of iron from melted sand" — explained via vapour-phase deposition of silicon tetrachloride at Corning in August 1970 achieving 17 dB/km and then 0.2 dB/km (Part 05, 6:43).

## For Chief to decide

1. Lock **042 = How Do Lasers & Fibre Optics Work? Albert Einstein's 1917 Stimulated Emission, Theodore Maiman's 16 May 1960 Flashlamp Ruby Laser in Malibu & Charles Kao's 1966 Pure Glass Fibre in Harlow (1842–1987)** and pick the 2-way Test & Compare working title pair:
   - **A (Subject + hook, §1 rule 11):** *Lasers & Fibre Optics: The Pink Ruby That Built the Internet* (60 chars)
   - **B (Search question, §1 rule 2):** *How a Tiny Pink Ruby and Pure Glass Built the Modern Internet* (61 chars)
   - **Alt (Search / twist question):** *Why Top Physicists Said the First Ruby Laser Could Never Work* (61 chars)
2. Review `laser_script_master_v01.md` (91.2/100 PASS), then queue the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

## Score (`npm run review:script`)

```text
# laser_script_master_v01.md

**Decision:** PASS · **Score:** 91.2 / 100

| Dimension | Score |
|---|---:|
| hook | 9.5 |
| curiosity | 9.5 |
| storytelling | 8 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 7.4 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1728 · Est. min: 11.5 · Chapters: 4

## Cold open excerpt

> Why does a torch beam spread out and fade across a dark room, while a laser beam stays pencil-thin all the way to the Moon? And how did a fingertip-sized pink ruby crystal flashed by a photographer's lamp in nineteen sixty — paired with a hair-thin thread of ultra-pure glass in E

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 91.2/100 — proceed to VO after production checklist.

Pass threshold: 90
```
