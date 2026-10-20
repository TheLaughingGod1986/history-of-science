# 083 script v01: notes for review (J0751)

Script: `eyes_optics_script_master_v01.md` (with `opening_and_outline_v00.md`, `SOURCES_v00.md` and `SOURCES_v01.md`).

**Draft only (J0751, Gemini Argon, 20 Oct 2026).** Built from `083_Al-Haytham-Kepler-Young-Donders-Snellen-Eyes-Glasses-Optics/opening_and_outline_v00.md` and the neighbour and search evidence in `IDEAS_2026-10-20_J0728.md` (`evidence_2026-10-20_J0728/n_eyes_glasses_optics.md` PASS — 6 education videos ≥ 1M views, with 4 strictly on glasses, eyesight & laser eye correction: **TED-Ed ★ *How does laser eye surgery work? - Dan Reinstein* (`XPDVmBg5DeE`, 6.83M — exact corneal refraction & focal-point match!)**, **MinuteEarth *Screens are NOT the reason kids need glasses 👀* (`vbCobKbLJls`, 6.70M — exact myopia & eyeball elongation match!)**, **TED-Ed ★ *How do glasses help us see? - Andrew Bastawrous and Clare Gilbert* (`ypF037wlYZg`, 2.41M — exact subject match!)**, and **SciShow *Do Glasses Ruin Your Eyesight?* (`c2ReCCjCdyI`, 1.45M — exact subject match!)**, plus **Cognito *How the Eye Works (Part 1) - Structure of the Eye & Iris Reflex* (`9SGAicn9rXY`, 687.1k)**, **Cognito *How the Eye Works (Part 2) - Accommodation* (`-BqvOucCTYg`, 479.6k)**, and **TED-Ed ★ *The story behind your glasses - Eva Timothy* (`G1KGUP2iKbE`, 137.2k)**, alongside `public_search.md` & `public_search_titles.md` showing `"how do glasses work"` is an exact YouTube autocomplete match (`yes`), all 5 top GB search results for `"ibn al haytham camera obscura johannes kepler eye"` under 31k views, and 4 of the top 5 GB slots for *How a Darkened Room in Cairo Proved Your Eyes See the World Upside Down* under 19k views). The topic isn't locked yet: Chief locks `083` and the working title pair first, then reviews/signs off this script and queues the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

Structure (*Reference lessons* §1, scripts from 011 on): every chapter opens cold and ends on a question the next one answers; Ibn al-Haytham's 1011–1021 AD Cairo `camera obscura` refutation of Greek `extramission` eye-beams lands in Part 02; the midpoint twist ("Case closed — since we see the sky above us and the ground beneath our feet, the crystal lens inside our eye must somehow flip light rays back right-side up before they reach the back of the eyeball! Wrong! In sixteen hundred and four in Prague and sixteen nineteen in Ingolstadt, two scientists proved that you really *do* see the entire world upside down — and scraped open an eyeball to show the inverted picture with their own eyes!") with Johannes Kepler's 1604 inverted retinal image and Christoph Scheiner's 1619 peeled ox-eye demonstration lands in Part 03; Benjamin Franklin's May 1784 `bifocals`, Thomas Young's 27 November 1800 (`Phil. Trans.` 1801) underwater immersion and iron calliper ring proof of `crystalline lens accommodation` and `astigmatism`, and Franciscus Donders & Herman Snellen's 1862–1864 `20/20` Big "E" Eye Chart land in Part 04; the ending hands off directly to `084` (*How Does Your Body Keep Its Temperature at Exactly 37 °C in Freezing Snow or Desert Heat — and Why Does Your Brain Give You a Fever When You're Sick?*), with no goodbye and no subscribe ask. Five VO parts, matching 009–082.

## Marker count (v01)

Run on `eyes_optics_script_master_v01.md`: `grep -o "DATA:" … | wc -l`, and the same for each marker.

| Marker | Count | Where | Rule |
|---|---:|---|---|
| `DATA` | **6** | 1) inked Kepler (1604) & Donders/Snellen (1862) human eye ray-tracing diagram (`cornea ~43 dioptres + crystalline lens ~15–20 dioptres = ~58–60 dioptres` at `24 mm`; `±1 mm = ∓3 dioptres`) (0:34); 2) inked Herman Snellen (1862) `20/200` to `20/20` visual acuity chart geometry (`5 arcminutes` letter height, `1 arcminute` stroke width at `20 feet / 6 metres`) (0:52); 3) inked Ibn al-Haytham (1011–1021 AD *Book of Optics*) 5-lamp `camera obscura` straight-line ray crossing diagram (1:58); 4) inked Johannes Kepler (1604 *Ad Vitellionem Paralipomena*) & Christoph Scheiner (1619 *Oculus*) inverted retinal image & concave vs convex spectacle lens ray-tracing chart (3:47); 5) inked Thomas Young (1801 *Phil. Trans.*) ciliary-lens accommodation & astigmatism chart + Donders & Snellen (1862–1864) refractive error & acuity scale (5:32); 6) animated timeline 1011–1864 (6:48) | ≥ 3 per long, including the timeline |
| `SCALE` | **6** | 1) every 1 mm your eyeball grows too long throws focus off by 3 dioptres — smaller than a British pound coin's thickness turning a street sign into a smudge (0:34); 2) reading Snellen's 20/20 line at 20 feet requires resolving 1/60th of a degree — like spotting the gap between two fingers at the far end of a tennis court (0:52); 3) if extramission eye-beams were real, opening your eyes at midnight would light up a bedroom like car headlights and staring at the sun wouldn't hurt (1:58); 4) your eye's lens lets your pupil open 100× wider than a pinhole in the dark while bending every ray back to a pinpoint on your retina (3:47); 5) looking up from a phone to a street sign flattens your lens curve by <0.5 mm in 1/3 s — faster and smoother than a digital camera autofocus motor (5:32); 6) from five oil lamps outside a darkened Cairo room to a peeled ox eye and the big letter E on an optician's wall (6:48) | `SCALE:` on every `DATA:` (`grep -c` matches) |
| `WHO` | **8** | Ibn al-Haytham (c. 965–c. 1040) — Arab mathematician and physicist; Johannes Kepler (1571–1630) — German astronomer and mathematician; Christoph Scheiner (1573–1650) — German Jesuit physicist and astronomer; Thomas Young (1773–1829) — British physician and physicist; Franciscus Cornelis Donders (1818–1889) — Dutch ophthalmologist and physiologist; Herman Snellen (1834–1908) — Dutch ophthalmologist; Felix Platter (1536–1614) — Swiss physician and anatomist; Benjamin Franklin (1706–1790) — American statesman and natural philosopher | Every named person at first mention, role right for the scene's year |
| `WHEN` | **24** | Cairo, 1011 AD (0:00); 1011 AD, 1021 AD, 1604, 1619, 1801, 1862 (0:34); 1011 AD, 1021 AD (1:28); 1286, 1583, 1604, 1619 (3:13); May 1784, 27 November 1800, 1801, 1825, 1862, 1864 (4:58); 1011–1864 timeline marker (6:48); 1612, 23 January 1775, 1868, 1975 (7:45) | Every spoken date or era |
| `FACT` | **3** | `Pinhole proved light enters` (1:28); `Retina sees world upside down` (3:13); `Iron ring proved lens flexes` (4:58) | 2–4 per long, ≤ 4 words per card |

## Craft lessons check (*Reference lessons* §1)

- **Cold opens & cliffhanger hand-offs:** Part 01 opens cold on why the image on the back of your eyeballs right now is upside down and how a darkened room in Cairo in 1011 AD, a peeled ox eye in 1619, and Snellen's 1862 Big "E" unlocked why 4 billion people wear glasses, and ends on why ancient Greeks believed eyes shoot beams of fire; Part 02 opens cold on Euclid and Ptolemy's `extramission` eye-beam theory vs Ibn al-Haytham's sun-glare and 5-lamp `camera obscura` proof in Cairo (1011–1021 AD), and ends on why the pinhole image is upside down and how Kepler (1604) and a peeled ox eye (1619) solved the paradox; Part 03 opens cold on the midpoint twist ("Case closed — since we see the sky above us and the ground beneath our feet, the crystal lens inside our eye must somehow flip light rays back right-side up before they reach the back of the eyeball! Wrong!"), tells the story of Kepler's 1604 ray-tracing and Scheiner's 1619 peeled ox eye, and ends on how a living eye focuses near and far (`accommodation`) and why Thomas Young in 1800 clamped iron rings onto his own eyeball; Part 04 opens cold on Franklin's 1784 bifocals, Young's 1800 underwater & iron-ring accommodation proof and `astigmatism`, and Donders & Snellen's 1862 `20/20` Big "E" chart, and ends on how our bodies stay locked at `37 °C` and why Charles Blagden stepped into a `126 °C` heated room with a raw beefsteak; Part 05 opens cold on the living camera in your head, and hands off to Santorio (1612), Blagden (1775), Wunderlich (1868), and Kluger (1975) (`084`).
- **Quirky anecdote before the hard idea:** Ibn al-Haytham hanging five oil lamps outside a shutter pinhole under house arrest in Cairo; Christoph Scheiner scraping the back off an ox eyeball to watch an upside-down candle flame; Thomas Young plunging his open eye underwater and pressing an iron ring behind his own eyeball; Herman Snellen designing the Big "E" on a 5×5 grid!
- **Rivalry / tension:** Euclid & Ptolemy's 1,000-year `extramission` eye-beams vs Ibn al-Haytham's `intromission`; Renaissance fear of an inverted image vs Kepler & Scheiner's upside-down retina; eyeball-stretching vs Young's flexing crystalline lens.
- **Misconception explained away:** "Do we see because rays shoot out of our eyes, and does our eye's lens flip the image upright on the retina?" — refuted by Ibn al-Haytham's camera obscura and Kepler & Scheiner's inverted retinal image (Parts 01–03).

## For Chief to decide

1. Lock **083 = How Do Your Eyes Focus Light & How Do Glasses Cure Blurry Vision — and How Did a Darkened Room in Cairo Prove Your Eyes See the World Upside Down (`Optics of the Eye, Ibn al-Haytham's 1011 Camera Obscura, Johannes Kepler's 1604 Upside-Down Retinal Image, Thomas Young's 1801 Accommodation & Herman Snellen's 1862 20/20 Eye Chart`)? Ibn al-Haytham's 1011–1021 AD Cairo `Camera Obscura` Proof (`Book of Optics`), Johannes Kepler's 1604 Inverted Retinal Image & Christoph Scheiner's 1619 Peeled Ox-Eye Demonstration, Thomas Young's 1801 Discovery of Lens `Accommodation` & `Astigmatism`, and Franciscus Donders & Herman Snellen's 1862 `20/20` Big "E" Eye Chart (1011–1864)** and pick the 2-way Test & Compare working title pair:
   - **A (Subject + hook, §1 rule 11):** *Your Eyes: Why You See the World Upside Down* (44 chars)
   - **B (Search question, §1 rule 2):** *How a Darkened Room in Cairo Proved Your Eyes See the World Upside Down* (71 chars)
   - **Alt (Search / twist question):** *How Your Eyes Focus Light and How Glasses Cure Blurry Vision* (60 chars)
2. Review `eyes_optics_script_master_v01.md` (91.1/100 PASS), then queue the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

## Score (`npm run review:script`)

```text
# eyes_optics_script_master_v01.md

**Decision:** PASS · **Score:** 91.1 / 100

| Dimension | Score |
|---|---:|
| hook | 9.5 |
| curiosity | 9.5 |
| storytelling | 7.5 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 7.8 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1690 · Est. min: 11.3 · Chapters: 4

## Cold open excerpt

> Why is the image on the back of your eyeballs right now completely upside down ? Over four billion people on Earth wear glasses or contact lenses because their eyeballs are just one to two millimetres too long or too short — so how did an Arab scientist locked under house arrest 

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 91.1/100 — proceed to VO after production checklist.

Pass threshold: 90
```
