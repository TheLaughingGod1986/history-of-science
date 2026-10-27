# 024 script v01: notes for review (J0447)

Script: `joule_script_master_v01.md` (with `opening_and_outline_v00.md`, `SOURCES_v00.md` and `SOURCES_v01.md`).

**Draft only (J0447, Gemini Argon, 17 Oct 2026).** Built from `024_Rumford-Joule-Thermodynamics/opening_and_outline_v00.md` and the neighbour and search evidence in `IDEAS_2026-10-17_J0438.md` (`evidence_2026-10-17_J0438/n_joule.md` PASS — 9 education videos ≥ 1M views including **three TED-Ed videos ≥ 1M** led by **TED-Ed ★ *Why don't perpetual motion machines ever work?* (17.72M)**, **TED-Ed ★ *The law of conservation of mass* (2.43M)**, **Cognito *GCSE Physics - Energy Stores, Transferring Energy & Work Done* (2.41M)**, **CrashCourse *Thermodynamics* (2.04M)**, **Khan Academy *First law of thermodynamics / internal energy* (1.57M)**, **Khan Academy *Enthalpy | Thermodynamics* (1.56M)**, **TED-Ed ★ *A guide to the energy of the Earth* (1.37M)**, **Khan Academy *Conservation of energy* (1.17M)**, and **minutephysics *A Simple Proof of Conservation of Energy* (1.08M)**, plus `public_search.md` showing `"count rumford heat"` autocompleting with all 5 top GB slots under 1,000 views and all 5 top GB slots for `"james prescott joule paddle wheel"` under 16k views). The topic isn't locked yet: Chief locks `024` and the working title pair first, then reviews/signs off this script and queues the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–5) before VO.

Structure (*Reference lessons* §1, scripts from 011 on): every chapter opens cold and ends on a question the next one answers; the midpoint twist ("Case closed? Wrong." — after the Royal Society refused to print Joule's full paper in their *Transactions* and the Oxford BAAS chairman on 23 June 1847 ordered him to give only a brief verbal summary without discussion, 23-year-old William Thomson stood up in the back row to electrify the hall and two months later in August 1847 met Joule on his Swiss Alps honeymoon carrying a long laboratory thermometer to measure waterfall spray, joining Julius Robert Mayer and Hermann von Helmholtz to establish the First Law of Thermodynamics) lands in Part 04; the popular misconception ("If Joule proved that stirring water with a paddle heats it up, why can't you boil your morning tea by stirring it with a spoon — and if energy is never lost, why can't a machine recycle its own heat and run forever?") is raised and explained away in Part 05 via water's 4,184 J/(kg·°C) heat capacity and Rudolf Clausius and Lord Kelvin's 1850 Second Law of Thermodynamics; the ending hands off directly to `025` (*Is Light a Particle or a Wave? Thomas Young's Playing Card in a Sunbeam, Poisson's Bright Spot & Einstein's Photoelectric Quanta*, 24 November 1801 & 15 March 1819), with no goodbye and no subscribe ask. Five VO parts, matching 009–023.

## Marker count (v01)

Run on `joule_script_master_v01.md`: `grep -o "DATA:" … | wc -l`, and the same for each marker.

| Marker | Count | Where | Rule |
|---|---:|---|---|
| `DATA` | **5** | 1) inked comparison of Rumford's 1798 cannon-boring water temperature curve (0 min: 60°F · 60 min: 107°F · 90 min: 142°F · 120 min: 178°F · 150 min: 212°F boiling) and Joule's mechanical equivalent of heat (772 foot-pounds per 1°F in 1 lb of water = 4.184 J/cal) (0:34); 2) inked thermometer scale comparing 1 full degree Fahrenheit against Joule's 0.005°F (1/200th °F) measurement resolution and the ~0.56°F rise per 20-drop paddle-wheel run (0:52); 3) inked comparison on period paper of the 54 grams (837 grains) of brass dust abraded by Rumford's blunt borer vs the 8,514 grams (18.77 lb) of cold water brought from 60°F to a full 212°F boil in 150 minutes (1:58); 4) inked convergence chart on period paper showing Joule's independent 1845–1849 measurements of the mechanical equivalent of heat across three different materials: Water paddle wheel = 772.69 ft·lbf, Mercury iron paddle wheel = 774.08 ft·lbf, Cast-iron friction = 774.98 ft·lbf (vs modern exact value 778.17 ft·lbf) (4:18); 5) animated timeline building 1789 · 25 Jan 1798 · Jul 1840 · 1843–1849 · 23 Jun & Aug 1847 · 1850 alongside an inked heat-capacity scale showing 4,184 joules required to raise 1 kg of water by 1°C (6:43) | 3 or more per long, including the animated timeline |
| `SCALE` | **5** | 1) 772 foot-pounds of work for a single degree Fahrenheit — you have to drop a twenty-nine-pound weight twenty times from chest height just to warm one pint of water by a single degree (0:34); 2) reading one two-hundredth of a degree Fahrenheit by eye — like spotting the thickness of a human hair on a ruler from across a table (0:52); 3) less than two ounces of brass dust — the weight of ten coins — while boiling more than two gallons of water with zero fire (1:58); 4) three completely different substances — water, liquid mercury, and solid iron — all landing within less than one percent of the exact same number (4:18); 5) 4,184 joules to warm one kilogram of water by one degree Celsius — equal to lifting a 42-kilogram suitcase ten metres into the air (6:43) | Every `DATA` number gets a `SCALE:` comparison (`grep -c "SCALE:"` ≥ `DATA:` count) |
| `WHO` | **8** | Benjamin Thompson Count Rumford (0:34), James Prescott Joule (0:34), Marie-Anne Paulze Lavoisier (2:28), John Benjamin Dancer (3:42), William Thomson Lord Kelvin (4:58), Julius Robert Mayer (6:00), Hermann von Helmholtz (6:00), Rudolf Clausius (6:43) | First mention only, role right for the scene's year (4 words or fewer) |
| `WHEN` | **19** | Munich January 1798 (0:00), 1789–1798 (0:21), January 1798 (0:34), 1843–1849 (0:34), Munich 25 January 1798 (1:28), October 1805 (2:28), Manchester 1840 (3:08), June 1845 (3:08), 1849 (3:42), Oxford 23 June 1847 (4:58), 18 August 1847 (5:30), August 1847 (5:30), Java July 1840 (6:00), May 1842 (6:00), 1847 (6:00), 1850 (6:43), 1789–1850 (6:43), 24 November 1801 (7:45), 15 March 1819 (7:45) | Every spoken date or era; later dates drop onto the timeline |
| `FACT` | **4** | Married Lavoisier's widow (2:28); Within 0.8% of modern value (3:42); Brought thermometer on honeymoon (5:30); Venous blood redder in tropics (6:00) | 2–4 per long (4 words or fewer per card) |

## Craft checks (*Reference lessons* §1 + *Polish pass*)

- **First-minute timings:** Answer image by 0:03 (two horses walking in a circle in the Munich arsenal in January 1798 turning a blunt steel borer inside a submerged brass cannon cylinder as thick white steam erupts from the boiling water box), title question by 0:07, promise by 0:15, stakes by 0:25, first concrete answer & real fact (Count Rumford boiling 18.77 pounds of water in 2.5 hours in January 1798 and James Prescott Joule proving 772 foot-pounds per degree Fahrenheit in 1843–1849) by 0:34.
- **Explorer limits:** 2 beats total (`[EXPLORER ACTS: once. …]`), at 1:05 (Part 01, outside the first minute) and 6:00 (Part 04 holding an oversized brass thermometer out into the flying mist at the foot of the Alpine waterfall and shaking the spray off its goggles).
- **Chapter cold opens & cliffhanger questions:** Part 01 ends on why scientists still clung to the invisible "caloric" fluid for 45 years after Rumford boiled a cannon and why Rumford married the widow of the man whose theory he destroyed; Part 02 opens cold on Rumford's period quote (*"It would be difficult to describe the surprise and astonishment..."*), his 25 January 1798 Royal Society cannon-boring report, and his October 1805 marriage to Marie-Anne Paulze Lavoisier, ending on who finally measured the exact exchange rate between mechanical work and heat to 1/200th of a degree; Part 03 opens cold on brewer James Prescott Joule in Manchester (1840–1849), his 29-pound falling weights, brass paddle wheel, and John Benjamin Dancer's 1/200th °F thermometer fixing 772 ft·lbf across water, mercury and iron, ending on why the scientific establishment brushed him aside until Oxford and a waterfall in the Swiss Alps; Part 04 opens cold on the midpoint twist ("Case closed? Wrong." — the 23 June 1847 Oxford BAAS interruption by 23-year-old William Thomson, Thomson spotting Joule carrying a long thermometer on his August 1847 Chamonix honeymoon, and Mayer's 1840 Java venous-blood discovery + Helmholtz's 1847 treatise), ending on why stirring tea doesn't boil it and why perpetual-motion machines always fail; Part 05 opens cold on the tea-stirring and perpetual-motion misconceptions, explains water's 4,184 J/(kg·°C) heat capacity and Clausius & Kelvin's 1850 Second Law of Thermodynamics, and hands off to Thomas Young's 24 November 1801 playing card in a sunbeam and Arago & Fresnel's 15 March 1819 bright spot (`025`).
- **Quirky anecdote before the hard idea:** Rumford spying with invisible ink in the American Revolution, boiling water with a blunt cannon, and marrying Lavoisier's widow; Joule carrying a several-foot-long laboratory thermometer on his Swiss Alps honeymoon to measure waterfall spray; Mayer noticing sailors' bright-red venous blood in tropical Java.
- **Rivalry / tension:** back-and-forth portrait cuts at the 23 June 1847 Oxford meeting between the impatient chairman rushing Joule off the stage and 23-year-old William Thomson standing up in the back row (4:58).
- **Misconception explained away:** "Why can't you boil your morning tea by stirring it with a spoon — and if energy is never lost, why can't a machine recycle its own heat and run forever?" — explained via water's 4,184 J/(kg·°C) heat capacity and the 1850 Second Law of Thermodynamics (Part 05, 6:43).

## For Chief to decide

1. Lock **024 = Thermodynamics & Conservation of Energy: Count Rumford's Boiled Cannon & James Prescott Joule's Falling-Weight Paddle Wheel (1798–1847)** and pick the 2-way Test & Compare working title pair:
   - **A (Subject + hook, §1 rule 11):** *Conservation of Energy: How a Blunt Cannon Boiled Water* (55 chars)
   - **B (Search question, §1 rule 2):** *How a Blunt Cannon and a Paddle Wheel Proved What Heat Is* (57 chars)
   - **Alt (Search / twist question):** *Why Scientists Thought Heat Was a Liquid Until a Cannon Boiled* (62 chars)
2. Review `joule_script_master_v01.md` (90.9/100 PASS), then queue the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–5) before VO.

## Score (`npm run review:script`)

```text
# joule_script_master_v01.md

**Decision:** PASS · **Score:** 90.9 / 100

| Dimension | Score |
|---|---:|
| hook | 9.5 |
| curiosity | 9.5 |
| storytelling | 7.5 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 7.6 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1542 · Est. min: 10.3 · Chapters: 4

## Cold open excerpt

> How did two horses turning a blunt steel borer inside a brass cannon boil eighteen pounds of icy water with zero fire — and destroy a century of physics? By the end of this film, you'll see why the world's greatest chemists swore heat was an invisible liquid trapped inside metal,

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 90.9/100 — proceed to VO after production checklist.

Pass threshold: 90
```
