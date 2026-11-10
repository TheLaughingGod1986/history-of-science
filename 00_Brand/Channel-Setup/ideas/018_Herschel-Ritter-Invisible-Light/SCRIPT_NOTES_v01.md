# 018 script v01: notes for review (J0412)

Script: `herschel_script_master_v01.md` (with `opening_and_outline_v00.md`, `SOURCES_v00.md` and `SOURCES_v01.md`).

**Draft only (J0412, Gemini Argon, 16 Oct 2026).** Built from `018_Herschel-Ritter-Invisible-Light/opening_and_outline_v00.md` and the neighbour and search evidence in `IDEAS_2026-10-16_J0404.md` (`evidence_2026-10-16_J0404/n_herschel.md` PASS — 8 big education videos ≥ 1M views led by **Kurzgesagt *What Is Light?* 9.97M**, CrashCourse *Light* 2.91M, minutephysics *How Do We See Light?* 2.31M, CrashCourse *Traveling Waves* 2.10M, **TED-Ed ★ *Is light a particle or a wave?* 1.81M**, CrashCourse *Light Is Waves* 1.30M, **TED-Ed ★ *Light waves, visible and invisible* 1.26M**, and TED-Ed ★ *Particles and waves* 1.15M — plus `public_search.md` & `public_search_titles.md` showing all 5 top GB slots under 75k views on `"william herschel infrared"` and all 5 under 37k views on `"johann ritter ultraviolet"`). The topic isn't locked yet: Chief locks `018` and the working title pair first, then reviews/signs off this script and queues the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–12) before VO.

Structure (*Reference lessons* §1, scripts from 011 on): every chapter opens cold and ends on a question the next one answers; the midpoint twist ("Case closed? Wrong." — William Herschel running over 200 experiments between May and November 1800 and concluding on 6 November 1800 that radiant heat and light were separate rays because clear crown glass blocked 70–90% of heat while transmitting nearly 100% of visible light, before Thomas Young's 1801 wavelengths, Macedonio Melloni's 1831–1835 rock-salt prisms, and James Clerk Maxwell's 1865 equations unified the electromagnetic spectrum) lands in Part 04; the popular misconception ("Many people think infrared is just a dim shade of red — or wonder why a car parked in winter sunshine gets roasting hot inside while the glass window stays cool") is raised and explained away in Part 05 with Herschel's glass trap, 10,000 nm human body thermal radiation at 37°C, and the James Webb Space Telescope; the ending hands off directly to `019` (*Sparks of Life & the First Battery: Luigi Galvani's Frog Legs & Alessandro Volta's Pile of Coins*), with no goodbye and no subscribe ask. Five VO parts, matching 009–017.

## Marker count (v01)

Run on `herschel_script_master_v01.md`: `grep -o "DATA:" … | wc -l`, and the same for each marker.

| Marker | Count | Where | Rule |
|---|---:|---|---|
| `DATA` | **5** | 1) inked bar chart of Herschel's thermometer readings across violet (+2°F), green (+3.25°F), red (+6.875°F) and the dark infrared zone half an inch beyond red (+9°F / 5°C in 16 minutes) (0:34); 2) inked electromagnetic spectrum scale comparing the 380–750 nm visible band (less than 0.01% of the spectrum, one octave) against infrared (750 nm – 1 mm) and ultraviolet (10–380 nm) (0:52); 3) inked dual-spectrum diagram showing Herschel's infrared heating peak 0.5 inches past the 750 nm red edge (+9°F) and Ritter's 22 February 1801 silver-chloride (AgCl) ultraviolet darkening peak beyond the 380 nm violet edge (4:15); 4) inked comparison of Herschel's November 1800 visual brightness curve (~555 nm peak) vs radiant-heat curve (>750 nm peak) and Young's 1801 wavelengths (1/36,000 inch red vs 1/60,000 inch violet) (5:28); 5) animated timeline building 1666 · 13 Mar 1781 · 11 Feb 1800 · 6 Nov 1800 · 22 Feb 1801 · Nov 1801 · 1865 alongside an inked thermal-radiation scale comparing visible red (750 nm) to human body heat at 37°C (10,000 nm / 10 µm) (6:43) | 3 or more per long, including the animated timeline |
| `SCALE` | **5** | 1) half an inch past red — the width of a thumb into complete darkness, yet hotter than the brightest visible light (0:34); 2) if the full electromagnetic spectrum stretched from London to New York, the rainbow your eyes can see would be narrower than a postage stamp (0:52); 3) 380 nm violet to 750 nm red — ultraviolet waves are twice as short as red light, packing enough punch to break chemical bonds and sunburn your skin (4:15); 4) 700 nanometres for red light — 1,400 waves of red light fit across the thickness of a single dime (5:28); 5) your body radiates at 10,000 nanometres — infrared waves 15 times longer than the deepest red your eyes can see (6:43) | Every `DATA` number gets a `SCALE:` comparison (`grep -c "SCALE:"` ≥ `DATA:` count) |
| `WHO` | **7** | William Herschel (0:34), Johann Wilhelm Ritter (0:34), Caroline Herschel (1:28), Carl Wilhelm Scheele (3:40), Thomas Young (5:28), Macedonio Melloni (5:58), James Clerk Maxwell (5:58) | First mention only, role right for the scene's year (4 words or fewer) |
| `WHEN` | **17** | Slough 11 February 1800 (0:00), 1666 (0:21), Winter 1800 (0:21), 11 February 1800 (0:34), 22 February 1801 (0:34), Bath 1773–1781 (1:28), 13 March 1781 (1:28), 27 March 1800 (2:28), 24 April 1800 (3:08), 1777 (3:40), Jena 22 February 1801 (3:40), 6 November 1800 (4:58), November 1801 (5:28), 1831–1835 (5:58), 1865 (5:58), 1666–1865 (6:43), March 1800 (7:45) | Every spoken date or era; later dates drop onto the timeline |
| `FACT` | **4** | Composed 24 symphonies first (1:28); Found ultraviolet with silver salt (3:40); Herschel thought heat wasn't light (4:58); Your body glows in infrared (6:43) | 2–4 per long (4 words or fewer per card) |

## Craft checks (*Reference lessons* §1 + *Polish pass*)

- **First-minute timings:** Answer image by 0:03 (sunlight passing through a prism in Slough on 11 February 1800 as a blackened mercury thermometer climbs in the dark shadow half an inch past the red edge), title question by 0:07, promise by 0:15, stakes by 0:25, first concrete answer & real fact (William Herschel on 11 February 1800, +9°F in 16 minutes half an inch past red; Johann Wilhelm Ritter on 22 February 1801 beyond violet) by 0:34.
- **Explorer limits:** 2 beats total (`[EXPLORER ACTS: once. …]`), at 1:05 (Part 01, outside the first minute) and 5:58 (Part 04 swapping a pane of window glass for a clear block of rock salt in front of Melloni's brass thermopile).
- **Chapter cold opens & cliffhanger questions:** Part 01 ends on why an astronomer famous for studying the night sky was staring at the midday Sun and how a composer of symphonies unlocked invisible light; Part 02 opens cold on Herschel's 24 symphonies and hand-grinding speculum mirrors with Caroline in Bath (discovering Uranus on 13 March 1781) before his solar filter puzzle and three-thermometer prism experiment (+2°F violet, +3.25°F green, +6.875°F red), ending on why the temperature would stop just because human eyes stop seeing red; Part 03 opens cold on Herschel's five parallel lines beyond red (+9°F half an inch into the dark) and Johann Wilhelm Ritter's 22 February 1801 silver-chloride discovery of ultraviolet in Jena, ending on whether Herschel celebrated discovering two new kinds of light; Part 04 opens cold on the midpoint twist ("Case closed? Wrong." — Herschel's 6 November 1800 glass-trap conclusion that heat and light were different rays, resolved by Young's 1801 wave interference, Melloni's 1831–1835 rock-salt prisms, and Maxwell's 1865 electromagnetic waves), ending on what happens when sunlight hits a car window or a space telescope; Part 05 opens cold on the winter car window & thermal-camera misconception, connects 10,000 nm body heat and the James Webb Space Telescope back to Slough, and hands off to Alessandro Volta's March 1800 battery and Luigi Galvani's twitching frog legs (`019`).
- **Quirky anecdote before the hard idea:** William Herschel composing 24 symphonies and grinding speculum-metal mirrors for 16 hours straight while his sister Caroline spoon-fed him supper in Bath before his 1800 prism heat-refraction experiments.
- **Rivalry / symmetry:** back-and-forth portrait cuts between William Herschel in Slough (1800) measuring infrared heat beyond the red edge and Johann Wilhelm Ritter in Jena (1801) laying silver-chloride paper beyond the violet edge (3:40).
- **Misconception explained away:** "Many people think infrared is just a dim shade of red — or wonder why a car parked in winter sunshine gets roasting hot inside while the glass window stays cool" — explained via Herschel's November 1800 glass trap and 10,000 nm thermal radiation (Part 05, 6:43).

## For Chief to decide

1. Lock **018 = Invisible Light: William Herschel's Thermometer Past the Rainbow & Ritter's Ultraviolet (1800–1801)** and pick the 2-way Test & Compare working title pair:
   - **A (Subject + hook, §1 rule 11):** *Infrared: The Thermometer Experiment That Found Invisible Light* (63 chars)
   - **B (Search question, §1 rule 2):** *How a Thermometer Past the Rainbow Discovered Invisible Light* (61 chars)
   - **Alt (Search / action question):** *Why William Herschel Put a Thermometer Outside a Rainbow* (56 chars)
2. Review `herschel_script_master_v01.md` (94.8/100 PASS), then queue the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–12) before VO.

## Score (`npm run review:script`)

```text
# herschel_script_master_v01.md

**Decision:** PASS · **Score:** 94.8 / 100

| Dimension | Score |
|---|---:|
| hook | 9.5 |
| curiosity | 9.5 |
| storytelling | 9 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 10 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1495 · Est. min: 10 · Chapters: 4

## Cold open excerpt

> Why did an astronomer place a mercury thermometer in the dark shadow outside a sunlit rainbow? And how did that single experiment reveal that human eyes are completely blind to more than ninety-nine point nine nine percent of the light in the universe? By the end of this film, yo

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 94.8/100 — proceed to VO after production checklist.

Pass threshold: 90
```
