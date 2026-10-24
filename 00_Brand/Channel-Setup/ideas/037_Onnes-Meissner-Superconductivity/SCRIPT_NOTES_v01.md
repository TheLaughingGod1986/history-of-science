# 037 script v01: notes for review (J0508)

Script: `superconductivity_script_master_v01.md` (with `opening_and_outline_v00.md`, `SOURCES_v00.md` and `SOURCES_v01.md`).

**Draft only (J0508, Gemini Argon, 18 Oct 2026).** Built from `037_Onnes-Meissner-Superconductivity/opening_and_outline_v00.md` and the neighbour and search evidence in `IDEAS_2026-10-17_J0500.md` (`evidence_2026-10-17_J0500/n_superconductivity.md` PASS — 13 education videos ≥ 1M views: **TED-Ed ★ *Why can't you divide by zero?* (`NKmGVE85GUU`, 12.76M)**, **TED-Ed ★ *Schrödinger's cat: A thought experiment in quantum mechanics - Chad Orzel* (`UjaAxUO6-Uw`, 9.19M)**, **TEDx Talks ★ *Quantum Physics for 7 Year Olds | Dominic Walliman* (`ARWBdfWpDyc`, 3.80M)**, **SciShow *Absolute Zero: Absolute Awesome* (`TNUDBdv3jWI`, 2.24M)**, **TED-Ed ★ *What can Schrödinger's cat teach us about quantum mechanics? - Josh Samani* (`z1GCnycbMeA`, 2.17M)**, and **TED-Ed ★ *Particles and waves: The central mystery of quantum mechanics - Chad Orzel* (`Hk3fgjHNQ2Q`, 1.15M)**, plus **TED-Ed ★ *What in the world is topological quantum matter? - Fan Zhang* (`GJHhnr9R_ZM`, 679k)** and **TED-Ed ★ *The high-stakes race to make quantum computers work* (`r_t96FqWE4M`, 412k)**, alongside `public_search.md` showing all 5 top GB search results for `"heike kamerlingh onnes superconductivity"` under 84k views). The topic isn't locked yet: Chief locks `037` and the working title pair first, then reviews/signs off this script and queues the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

Structure (*Reference lessons* §1, scripts from 011 on): every chapter opens cold and ends on a question the next one answers; the midpoint twist ("Case closed? Not yet." — in October 1933 in Berlin, Walther Meissner and Robert Ochsenfeld discovered that a superconductor doesn't merely have zero resistance, it actively expels magnetic fields from its interior to levitate magnets in mid-air, while the 46-year quantum mystery that defeated Einstein, Bohr, and Feynman was finally solved in February 1957 by John Bardeen, Leon Cooper, and Robert Schrieffer's BCS Cooper-pair theory) lands in Part 04; the popular misconception ("Many people assume only shiny pure metals can conduct electricity without resistance, or that every superconductor needs rare liquid helium near Absolute Zero") is raised and explained away in Part 05 via Bednorz & Müller's 1986 ceramic cuprates and Wu & Chu's 93 K YBCO crossing the 77 K boiling point of cheap liquid nitrogen, paired with hospital MRI scanners and maglev trains; the ending hands off directly to `038` (*Sound Waves, the Doppler Effect & the Sound Barrier: Christian Doppler's 1842 Wave Equation, Buys Ballot's June 1845 Steam Train of Horn Players in Utrecht & Ernst Mach's 1887 Supersonic Bullet Spark Photo*), with no goodbye and no subscribe ask. Five VO parts, matching 009–036.

## Marker count (v01)

Run on `superconductivity_script_master_v01.md`: `grep -o "DATA:" … | wc -l`, and the same for each marker.

| Marker | Count | Where | Rule |
|---|---:|---|---|
| `DATA` | **6** | 1) inked resistance-vs-temperature graph on period paper from Kamerlingh Onnes's April 1911 Leiden measurements showing frozen mercury's resistance plunging by a factor of >10,000 across a 0.01 Kelvin cliff at 4.20 K (−268.95 °C) to <10⁻⁷ ohms (0:34); 2) inked cryogenic temperature bar comparing room temperature (293 K), liquid nitrogen (77 K), liquid hydrogen (20.4 K), liquid helium boiling point (4.22 K / −268.93 °C), cosmic microwave background of deep space (2.7 K), and Leiden's pumped helium (1.04 K / −272.11 °C) (0:52); 3) inked cascade cooling diagram on period paper showing Kamerlingh Onnes's 4-stage Leiden liquefier on 10 July 1908: methyl chloride (183 K) → ethylene (169 K) → oxygen/air (77 K) → liquid hydrogen (20.4 K) → 60 mL of liquid helium at 4.22 K (−268.93 °C), pumped down to 1.04 K (1:58); 4) inked resistance cliff chart on period paper from Kamerlingh Onnes's 1911 Leiden Communication No. 122b showing solid mercury resistance falling from 0.115 Ω at 4.3 K to <10⁻⁵ Ω at 4.20 K, alongside lead (Tc = 7.2 K) and tin (Tc = 3.7 K) (3:42); 5) inked two-panel diagram on period paper comparing a classical metal above Tc (magnetic field lines pass straight through; single electrons scatter off vibrating lattice ions, wasting heat) vs a superconductor below Tc (Meissner Effect expels magnetic field B = 0 to levitate a magnet; phonon lattice attraction binds electrons into frictionless BCS Cooper pairs) (5:28); 6) animated timeline building 10 Jul 1908 · 8 Apr 1911 · Oct 1933 · Feb 1957 · Jan 1986 – Feb 1987 alongside critical temperature climbing from 4.2 K (1911 Hg) to 35 K (1986 LBCO) and 93 K (1987 YBCO) above the 77 K (−196 °C) boiling point of liquid nitrogen (6:43) | 3 or more per long, including the animated timeline |
| `SCALE` | **6** | 1) within a single hundredth of a degree at four point two Kelvin, the electrical friction inside solid mercury didn't fade away — it fell off a cliff by more than ten thousand times to zero (0:34); 2) at one point zero four degrees above Absolute Zero, Kamerlingh Onnes's glass flask in the Netherlands was more than twice as cold as the deepest voids of outer space (0:52); 3) sixty millilitres of liquid helium — barely enough to fill an espresso cup — made a room in Leiden colder than any natural place in the known universe (1:58); 4) a current started inside a superconducting ring with the battery unplugged will keep circling longer than the entire history of human civilisation (3:42); 5) forty-six years elapsed between Kamerlingh Onnes seeing zero resistance in 1911 and Bardeen, Cooper, and Schrieffer explaining how two negative electrons team up through crystal vibrations in 1957 (5:28); 6) jumping from 4.2 Kelvin liquid helium in 1911 to 93 Kelvin YBCO in 1987 meant cooling a superconductor with liquid nitrogen that costs pennies a litre instead of rare helium near Absolute Zero (6:43) | Every `DATA` number gets a `SCALE:` comparison (`grep -c "SCALE:"` ≥ `DATA:` count) |
| `WHO` | **6** | Heike Kamerlingh Onnes (0:34), Gilles Holst (0:34), Walther Meissner (0:34), James Dewar (1:28), Leon Cooper (4:53), Robert Schrieffer (4:53) | First mention only, role right for the scene's year (4 words or fewer) |
| `WHEN` | **23** | Leiden 8 April 1911 (0:00), 1902 (0:21), 10 July 1908 (0:34), 8 April 1911 (0:34), 1933 (0:34), 1957 (0:34), 1702 (1:28), 1848 (1:28), 1898 (1:28), 10 July 1908 (1:28), 8 April 1911 (3:08), 1913 (3:08), 1914 (3:08), October 1933 (4:53), 1945 (4:53), February 1957 (4:53), 1972 (4:53), January 1986 (6:43), February 1987 (6:43), 1908–1987 (6:43), 25 May 1842 (7:45), 3 June 1845 (7:45), 1887 (7:45) | Every spoken date or era; later dates drop onto the timeline |
| `FACT` | **4** | Colder than deep space (1:28); Current flows 100,000+ years (3:08); Bardeen won 2 Physics Nobels (4:53); Liquid nitrogen is cheaper than milk (6:43) | 2–4 per long (4 words or fewer per card) |

## Craft checks (*Reference lessons* §1 + *Polish pass*)

- **First-minute timings:** Answer image by 0:03 (Heike Kamerlingh Onnes and Gilles Holst at Leiden University at 4:00 p.m. on 8 April 1911 watching the mirror galvanometer needle drop to 0.00000 ohms as solid mercury cools in liquid helium to 4.20 K), title question by 0:07, promise by 0:15, stakes by 0:25, first concrete answer & real fact (Kamerlingh Onnes liquefying helium on 10 July 1908 and discovering zero electrical resistance in mercury at 4.20 K on 8 April 1911, followed by Meissner in 1933 and BCS Theory in 1957) by 0:34.
- **Explorer limits:** 2 beats total (`[EXPLORER ACTS: once. …]`), at 1:05 (Part 01, outside the first minute) and 6:05 (Part 04 pouring liquid helium over a superconductor so invisible magnetic field lines lift a magnet with the Explorer sitting on top).
- **Chapter cold opens & cliffhanger questions:** Part 01 ends on how a Dutch laboratory got colder than outer space in 1908 and why Onnes thought his meter was broken by a short circuit; Part 02 opens cold on Amontons (1702), Kelvin (1848), James Dewar's 1898 liquid hydrogen, and Kamerlingh Onnes's 14-hour 10 July 1908 cascade producing 60 mL of liquid helium at 4.22 K (pumped to 1.04 K), ending on what happened on 8 April 1911 when he dipped a frozen wire into it; Part 03 opens cold on Kelvin's 1902 infinite-resistance prediction, quadruple-distilled mercury, the 8 April 1911 4:00 p.m. resistance cliff at 4.20 K (*"Kwik nagenoeg nul"*), and the 1914 battery-free ring current lasting >100,000 years, ending on what happened in Berlin in October 1933 when two physicists placed a magnet beside a superconductor; Part 04 opens cold on the midpoint twist ("Case closed? Not yet." — Walther Meissner and Robert Ochsenfeld's October 1933 magnetic expulsion shock and Bardeen, Cooper, and Schrieffer's February 1957 Cooper-pair breakthrough), ending on why a brittle ceramic coffee-mug material can superconduct above liquid nitrogen; Part 05 opens cold on the pure-metal/liquid-helium misconception, explains 1986–1987 cuprate superconductors (93 K YBCO above 77 K liquid nitrogen) and hospital MRI scanners, and hands off to Christian Doppler's 25 May 1842 wave equation, Buys Ballot's 3 June 1845 steam train of horn players, and Ernst Mach's 1887 supersonic bullet photo (`038`).
- **Quirky anecdote before the hard idea:** Kamerlingh Onnes and Gilles Holst assuming a loose wire had short-circuited their mercury tube when the needle dropped to zero; Onnes unplugging the battery from a lead ring in 1914 and watching the current keep circling with a pocket compass; John Bardeen winning a second Physics Nobel in 1972 after already winning for the transistor in 1956.
- **Rivalry / tension:** Sir James Dewar in London vs Heike Kamerlingh Onnes in Leiden racing to liquefy helium; Lord Kelvin's 1902 prediction that resistance would shoot to infinity near Absolute Zero vs the sudden cliff to zero at 4.20 K.
- **Misconception explained away:** "Many people assume only shiny pure metals can conduct electricity without resistance, or that every superconductor needs rare liquid helium near Absolute Zero" — explained via 1986–1987 ceramic copper-oxide superconductors (`YBCO`, `93 K`) operating in cheap `77 K` liquid nitrogen (Part 05, 6:43).

## For Chief to decide

1. Lock **037 = Superconductivity & Absolute Zero: Heike Kamerlingh Onnes's 10 July 1908 Liquid Helium & 8 April 1911 Zero-Resistance Mercury in Leiden (1908–1987)** and pick the 2-way Test & Compare working title pair:
   - **A (Subject + hook, §1 rule 11):** *Superconductivity: The 1911 Lab That Made Electricity Flow Forever* (66 chars)
   - **B (Search question, §1 rule 2):** *How Liquid Helium and Frozen Mercury Revealed Superconductivity* (63 chars)
   - **Alt (Search / twist question):** *What Happens to Electricity Two Degrees Above Absolute Zero?* (60 chars)
2. Review `superconductivity_script_master_v01.md` (92.4/100 PASS), then queue the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

## Score (`npm run review:script`)

```text
# superconductivity_script_master_v01.md

**Decision:** PASS · **Score:** 92.4 / 100

| Dimension | Score |
|---|---:|
| hook | 9.5 |
| curiosity | 9.5 |
| storytelling | 9 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 7.6 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1561 · Est. min: 10.4 · Chapters: 4

## Cold open excerpt

> What happens when you cool a metal wire down to four degrees above Absolute Zero — and why did the electrical resistance inside frozen mercury suddenly fall to nothing? By the end of this film, you'll see how a Dutch laboratory became colder than deep space, why a loop of frozen 

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 92.4/100 — proceed to VO after production checklist.

Pass threshold: 90
```
