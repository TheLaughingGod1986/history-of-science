# 022 script v01: notes for review (J0447)

Script: `fission_script_master_v01.md` (with `opening_and_outline_v00.md`, `SOURCES_v00.md` and `SOURCES_v01.md`).

**Draft only (J0447, Gemini Argon, 17 Oct 2026).** Built from `022_Meitner-Hahn-Nuclear-Fission/opening_and_outline_v00.md` and the neighbour and search evidence in `IDEAS_2026-10-17_J0421.md` (`evidence_2026-10-17_J0421/n_fission.md` PASS — 7 education videos ≥ 1M views led by **Kurzgesagt *Worst Nuclear Accidents in History* 10.86M**, **Kurzgesagt *Nuclear Energy Explained: How does it work?* 8.18M**, **Real Engineering *The Problem with Nuclear Fusion* 4.95M**, **TED-Ed ★ *How do nuclear power plants work?* 3.32M**, **TED-Ed ★ *Can you survive nuclear fallout?* 2.14M**, and **TED ★ *Taylor Wilson: My radical plan for small nuclear fission reactors* 1.24M**, plus `public_search.md` showing `"lise meitner nuclear fission"` autocompleting in GB search with all 5 top GB slots under 38k views). The topic isn't locked yet: Chief locks `022` and the working title pair first, then reviews/signs off this script and queues the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–6) before VO.

Structure (*Reference lessons* §1, scripts from 011 on): every chapter opens cold and ends on a question the next one answers; the midpoint twist ("Case closed? Wrong." — after Otto Frisch physically confirmed the 200 MeV recoiling uranium fragments in Copenhagen on 13 January 1939 and coined "nuclear fission" in his and Meitner's 11 February 1939 *Nature* paper, Otto Hahn had published the 6 January 1939 Berlin barium paper without Jewish exile Lise Meitner's name and received the delayed 1944 Nobel Prize in Chemistry alone in November 1945 while Meitner received zero Nobels despite 49 nominations, before sharing the 1966 Fermi Award and having element 109 named Meitnerium in 1997) lands in Part 04; the popular misconception ("Many people think splitting an atom annihilates its protons or neutrons into pure energy") is raised and explained away in Part 05 by showing that zero protons or neutrons are destroyed ($92 = 56 + 36$) and instead 0.1% nuclear binding mass converts into kinetic heat via $E = mc^2$, with spare neutrons tamed by Enrico Fermi's 2 December 1942 Chicago Pile-1 control rods; the ending hands off directly to `023` (*Radioactivity: Henri Becquerel's Cloudy-Day Drawer & Marie Curie's Freezing Shed*, February 1896), with no goodbye and no subscribe ask. Five VO parts, matching 009–021.

## Marker count (v01)

Run on `fission_script_master_v01.md`: `grep -o "DATA:" … | wc -l`, and the same for each marker.

| Marker | Count | Where | Rule |
|---|---:|---|---|
| `DATA` | **5** | 1) inked nuclear-fission balance comparing Uranium (92 protons) → Barium (56 protons) + Krypton (36 protons) and the 200 million electron-volts (200 MeV) released per split atom vs ~4 eV from burning one atom of carbon in coal (0:34); 2) inked energy-density scale comparing 1 kilogram of fissioned Uranium-235 against 2.7 million kilograms (2,700 tonnes) of burning coal (0:52); 3) inked atomic-number scale comparing Uranium (Z = 92) against Radium (Z = 88) and Barium (Z = 56 — 36 protons lighter than Uranium) (2:28); 4) inked liquid-drop & E = mc² calculation diagram on period paper showing 1 uranium nucleus + 1 neutron → dumbbell drop → Barium (Z = 56) + Krypton (Z = 36), where missing mass Δm ≈ 0.2 proton mass × c² = 200 MeV (3:42); 5) animated timeline building 1905 · 1934 · 13 Jul 1938 · 17 Dec 1938 · 24 Dec 1938 · 11 Feb 1939 · 2 Dec 1942 · 1997 alongside an inked nucleon balance showing 92 protons + 144 neutrons = 236 nucleons before and after fission (zero particles destroyed, 0.1% binding mass converted to heat) (6:43) | 3 or more per long, including the animated timeline |
| `SCALE` | **5** | 1) 200 million electron-volts from a single atom — fifty million times more energy than burning one atom of coal, enough to make a visible grain of sand physically jump (0:34); 2) one kilogram of uranium holds the energy of 2,700 tonnes of coal — a lump the size of a baseball matching a thirty-car freight train (0:52); 3) chipping 36 protons off a uranium nucleus in one hit — like tossing a pebble at a boulder and watching the boulder split cleanly in half (2:28); 4) one-fifth of a single proton's mass vanishes — and turns into enough energy to hurl the two atomic halves apart at a thirtieth of the speed of light (3:42); 5) zero protons or neutrons destroyed — releasing just one-thousandth (0.1%) of the atom's binding mass powers an entire city (6:43) | Every `DATA` number gets a `SCALE:` comparison (`grep -c "SCALE:"` ≥ `DATA:` count) |
| `WHO` | **7** | Otto Hahn (0:34), Fritz Strassmann (0:34), Lise Meitner (0:34), Otto Robert Frisch (0:34), Enrico Fermi (1:28), Niels Bohr (3:42), Albert Einstein (4:18) | First mention only, role right for the scene's year (4 words or fewer) |
| `WHEN` | **22** | Kungälv Sweden 24 December 1938 (0:00), December 1938 (0:21), 17 December 1938 (0:34), 24 December 1938 (0:34), Berlin 1907 (1:28), 1934 (1:28), March 1938 (1:58), 13 July 1938 (1:58), 19 December 1938 (2:28), Kungälv 24 December 1938 (3:08), 1905 (4:18), Copenhagen 3 January 1939 (4:58), 13 January 1939 (4:58), 11 February 1939 (4:58), 6 January 1939 (5:30), November 1945 (5:30), 1966 (6:00), 1997 (6:00), 2 December 1942 (6:43), 1905–1997 (6:43), February 1896 (7:45), January 1798 (7:45) | Every spoken date or era; later dates drop onto the timeline |
| `FACT` | **4** | Fled with 10 marks (1:58); Solved on a snowy log (3:08); Coined "fission" from biology (4:58); Nominated 49 times, 0 Nobels (5:30) | 2–4 per long (4 words or fewer per card) |

## Craft checks (*Reference lessons* §1 + *Polish pass*)

- **First-minute timings:** Answer image by 0:03 (Lise Meitner and Otto Frisch on a fallen pine log in the snowy woods of Kungälv on 24 December 1938 sketching a heavy uranium nucleus stretching like a liquid drop and snapping into two spheres), title question by 0:07, promise by 0:15, stakes by 0:25, first concrete answer & real fact (Otto Hahn & Fritz Strassmann finding barium on 17 December 1938 and Lise Meitner & Otto Frisch proving the 200 MeV liquid-drop split on 24 December 1938) by 0:34.
- **Explorer limits:** 2 beats total (`[EXPLORER ACTS: once. …]`), at 1:05 (Part 01, outside the first minute) and 6:00 (Part 04 polishing the gleaming brass tile of Element 109 Meitnerium on the periodic table and tipping its hat toward Lise Meitner's portrait).
- **Chapter cold opens & cliffhanger questions:** Part 01 ends on why scientists were firing neutrons at uranium and why Lise Meitner had been forced to flee her Berlin lab five months earlier; Part 02 opens cold on Meitner's 1907 carpenter's basement workshop in Berlin, her 13 July 1938 escape across the Dutch border with 10 marks in her purse, and Hahn & Strassmann's baffled 17–19 December 1938 letter finding barium (element 56) from uranium (element 92), ending on what Meitner saw in the snowy woods of Sweden on Christmas Eve; Part 03 opens cold on Christmas Eve 24 December 1938 in Kungälv, Sweden, where Meitner and Frisch sit on a fallen tree trunk and combine Bohr's liquid-drop model ($56 + 36 = 92$) with Einstein's $E = mc^2$ ($0.2\,m_p c^2 = 200\text{ MeV}$), ending on why Otto Hahn won the Nobel Prize alone and how Frisch proved the split in Copenhagen days later; Part 04 opens cold on Bohr's 3 January 1939 forehead-slap, Frisch's 13 January 1939 ionization spikes and coining "fission" from biology (11 February 1939 *Nature*), and lands the midpoint twist ("Case closed? Wrong." — Hahn publishing without Meitner's name on 6 January 1939 and receiving the 1944 Chemistry Nobel alone in November 1945 while Meitner received 0 Nobels from 49 nominations, before the 1966 Fermi Award and 1997 Element 109 Meitnerium), ending on why people think splitting an atom destroys protons and neutrons and how scientists tamed the chain reaction; Part 05 opens cold on the particle-annihilation misconception, explains the 0.1% binding-mass conversion and Fermi's 2 December 1942 Chicago Pile-1 control rods, and hands off to Henri Becquerel's February 1896 dark desk drawer and Marie Curie's freezing shed (`023`).
- **Quirky anecdote before the hard idea:** Meitner barred from upstairs Prussian labs in 1907, working in a basement carpenter's shop and walking down the street to a restaurant to use a toilet; fleeing across the Dutch border on 13 July 1938 with 10 marks and Hahn's mother's diamond ring.
- **Rivalry / tension:** back-and-forth portrait cuts between Otto Hahn in Berlin and Lise Meitner in Stockholm over the 6 January 1939 paper and the 1944 Nobel Prize (5:30).
- **Misconception explained away:** "Many people think splitting an atom annihilates its protons or neutrons into pure energy" — explained via nucleon conservation ($92 = 56 + 36$, 236 nucleons before and after) and 0.1% tighter nuclear binding energy converted via $E = mc^2$ (Part 05, 6:43).

## For Chief to decide

1. Lock **022 = Splitting the Atom: Lise Meitner's Walk in the Swedish Snow & Otto Hahn's Barium Puzzle (Dec 1938)** and pick the 2-way Test & Compare working title pair:
   - **A (Subject + hook, §1 rule 11):** *Nuclear Fission: The Walk in the Snow That Split the Atom* (57 chars)
   - **B (Search question, §1 rule 2):** *How an Exiled Physicist in the Snow Discovered Nuclear Fission* (62 chars)
   - **Alt (Search / puzzle question):** *Why Uranium Turned Into Barium and Split the Atomic Nucleus* (59 chars)
2. Review `fission_script_master_v01.md` (92.2/100 PASS), then queue the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–6) before VO.

## Score (`npm run review:script`)

```text
# fission_script_master_v01.md

**Decision:** PASS · **Score:** 92.2 / 100

| Dimension | Score |
|---|---:|
| hook | 9.5 |
| curiosity | 9.5 |
| storytelling | 8 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 8.4 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1617 · Est. min: 10.8 · Chapters: 4

## Cold open excerpt

> How did a baffled letter from Berlin — and a Christmas Eve walk through the Swedish snow — reveal that the heaviest atom in nature had just been split in two? By the end of this film, you'll see why the world's greatest physicists insisted it was impossible to crack a heavy nucle

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 92.2/100 — proceed to VO after production checklist.

Pass threshold: 90
```
