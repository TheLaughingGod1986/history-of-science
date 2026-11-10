# 047 script v01: notes for review (J0569)

Script: `plastics_script_master_v01.md` (with `opening_and_outline_v00.md`, `SOURCES_v00.md` and `SOURCES_v01.md`).

**Draft only (J0569, Gemini Argon, 18 Oct 2026).** Built from `047_Baekeland-Staudinger-Plunkett-Kwolek-Plastics-Teflon-Kevlar/opening_and_outline_v00.md` and the neighbour and search evidence in `IDEAS_2026-10-18_J0546.md` (`evidence_2026-10-18_J0546/n_plastics.md` PASS — 4 education videos ≥ 1M views: **Kurzgesagt *Plastic Pollution: How Humans are Turning the World into Plastic* (`RS7IzU2VJIQ`, 10.08M)**, **TED-Ed ★ *What really happens to the plastic you throw away - Emma Bryce* (`_6xlNyWPpB8`, 5.67M)**, **TED-Ed ★ *Why doesn’t anything stick to Teflon? - Ashwini Bharathula* (`uXaP43Zbz7U`, 3.13M — exact Teflon match!)**, and **TED-Ed ★ *A brief history of plastic* (`9GMbRG9CZJw`, 1.51M — exact history match!)**, plus **TED-Ed ★ *From DNA to Silly Putty: The diverse world of polymers - Jan Mattingly* (`UwRVj9rz2QQ`, 454.7k)**, **TED-Ed ★ *What is kevlar, and why is it so strong? - Max G. Levy* (`HsaSaYcnTKg`, 382.9k)**, and **Veritasium *How Dangerous Are Non-Stick Pans?* (`IHkp5Kq72ro`, 1.61M)**, alongside `public_search.md` showing autocomplete match `stephanie kwolek kevlar`, all 5 top GB search results for `"roy plunkett teflon stephanie kwolek kevlar"` under 61k views, and all 4 top GB slots for *How a Frozen Gas Cylinder and Cloudy Liquid Created Teflon and Kevlar* under 61 views). The topic isn't locked yet: Chief locks `047` and the working title pair first, then reviews/signs off this script and queues the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

Structure (*Reference lessons* §1, scripts from 011 on): every chapter opens cold and ends on a question the next one answers; the midpoint twist ("Case closed — had the gas leaked out overnight? Wrong! When Plunkett put the 'empty' steel cylinder on the scales, it still weighed the exact full weight of the gas!" — when 27-year-old DuPont chemist Roy Plunkett and technician Jack Rebok opened a dry-ice-cooled cylinder of tetrafluoroethylene gas on 6 April 1938 and heard no hiss, sawing the steel tank open revealed waxy white PTFE / Teflon, whose 485 kJ/mol carbon-fluorine bonds give a 0.04 friction coefficient matching wet ice on wet ice) lands in Part 03; Stephanie Kwolek's 1965 Wilmington discovery of bulletproof Kevlar (persuading spinneret technician Charles Smullen to spin a cloudy, buttermilk-like liquid-crystalline aromatic polyamide solution whose parallel rod-like chains yielded a golden fibre with ~3.6 GPa tensile strength, five times stronger than steel by weight) lands in Part 04; the disposable-substitute misconception ("When Leo Baekeland invented Bakelite in nineteen oh seven, people assumed synthetic plastics were just cheap, harmless substitutes that would spare elephant herds and vanish into the soil like wood or cotton") is raised and explained away in Part 05 via Hermann Staudinger's unbroken covalent carbon-carbon and carbon-fluorine chains that bacterial enzymes never evolved to snip apart across 400 million tonnes of annual production; the ending hands off directly to `048` (*Malaria, Quinine, William Perkin's 1856 Accidental Purple Dye & Tu Youyou's 340 AD Cold-Ether Artemisinin*), with no goodbye and no subscribe ask. Five VO parts, matching 009–046.

## Marker count (v01)

Run on `plastics_script_master_v01.md`: `grep -o "DATA:" … | wc -l`, and the same for each marker.

| Marker | Count | Where | Rule |
|---|---:|---|---|
| `DATA` | **6** | 1) inked tensile-strength & friction comparison chart on period paper contrasting structural steel (tensile strength ~0.5–0.8 GPa, density 7.8 g/cm³) against Stephanie Kwolek's 1965 Kevlar aramid fibre (tensile strength ~3.6 GPa, density 1.44 g/cm³ = 5× stronger than steel on an equal-weight basis) and Roy Plunkett's 1938 PTFE / Teflon (coefficient of friction ~0.04, matching wet ice on wet ice, stable up to 260 °C) (0:34); 2) inked monomer vs macromolecule chain-length chart comparing small organic molecules (<500 Da) and the 1920 "5,000 Da ceiling" dogma against Staudinger's covalent polymer chains (100,000 to >1,000,000 Da) (0:52); 3) inked polymer-chain vs colloidal-clump comparison diagram on period paper from Hermann Staudinger (1920, Berichte der deutschen chemischen Gesellschaft 53: 1073–1085) contrasting the old micelle/aggregate myth (<5,000 Da rings) against Staudinger's covalent macromolecule chains (10,000 to >100,000 repeating monomer units remaining giant chains even after hydrogenation) (1:58); 4) inked cylinder mass-balance & carbon-fluorine bond chart on period paper from Roy Plunkett (6 April 1938 notebook & US Patent 2,230,654) showing gaseous C2F4 polymerising at 100% mass conservation into solid PTFE chains armored by 485 kJ/mol C–F bonds (coefficient of friction 0.04, melting point 327 °C) (3:42); 5) inked polymer-alignment & strength diagram on period paper from Stephanie Kwolek (1965 notebook & US Patent 3,671,542) comparing tangled amorphous nylon chains (~0.8 GPa tensile strength) against Kwolek's parallel liquid-crystalline poly-para-phenylene terephthalamide (Kevlar) rods linked by inter-chain hydrogen bonds (~3.6 GPa tensile strength at 1.44 g/cm³ density vs steel's ~0.5–0.8 GPa at 7.8 g/cm³) (5:28); 6) animated timeline building Jul 1907 · 1920–1926 · 6 Apr 1938 · 1954 · 1965 alongside the global polymer production curve rising to ~400 million tonnes per year (6:43) | 3 or more per long, including the animated timeline |
| `SCALE` | **6** | 1) pound for pound, Stephanie Kwolek's golden Kevlar thread is five times stronger than steel — while Roy Plunkett's white Teflon is as slippery as wet ice sliding on wet ice (0:34); 2) if a single monomer gas molecule were the size of a paperclip, a single polymer molecule inside a Teflon pan would be a continuous chain of paperclips stretching across a football pitch (0:52); 3) chemists in nineteen twenty insisted no single molecule could hold more than a few hundred atoms — yet Hermann Staudinger proved a single strand of rubber or plastic is a continuous chain of hundreds of thousands of atoms bolted together (1:58); 4) the fluorine armour around a Teflon chain is so aloof that boiling acid, molten sodium, and burnt egg whites slide off it with the same friction as wet ice on wet ice (3:42); 5) a strand of Stephanie Kwolek's Kevlar thinner than a shoelace can hold up an entire family car — five times the strength of a steel wire of the exact same weight (5:28); 6) humanity went from Leo Baekeland's single iron pot in nineteen oh seven to making four hundred million tonnes of synthetic polymers every single year — more than the total weight of every human alive on Earth (6:43) | Every `DATA` number gets a `SCALE:` comparison (`grep -c "SCALE:"` ≥ `DATA:` count) |
| `WHO` | **7** | Leo Baekeland (0:34), Hermann Staudinger (0:34), Roy J. Plunkett (0:34), Stephanie Kwolek (0:34), Jack Rebok (3:08), Marc Grégoire (3:08), Charles Smullen (4:53) | First mention only, role right for the scene's year (4 words or fewer) |
| `WHEN` | **21** | Deepwater New Jersey 6 April 1938 (0:00), Wilmington 1965 (0:00), 6 April 1938 (0:21), July 1907 (0:34), 1920 (0:34), 6 April 1938 (0:34), 1965 (0:34), July 1907 (1:28), 1920 (1:28), 1926 (1:28), 1953 (1:28), 6 April 1938 (3:08), 1943 (3:08), 1945 (3:08), 1954 (3:08), 1964 (4:53), 1965 (4:53), 1907–1965 (6:43), Easter 1856 (7:45), 20 August 1897 (7:45), 4 October 1971 (7:45) | Every spoken date or era; later dates drop onto the timeline |
| `FACT` | **4** | Warned giant molecules impossible (1:28); Sawed steel tank open (3:08); Five times steel's strength (4:53); Saved 3,000+ police officers (6:43) | 2–4 per long (4 words or fewer per card) |

## Craft checks (*Reference lessons* §1 + *Polish pass*)

- **First-minute timings:** Answer image by 0:03 (Roy Plunkett and Jack Rebok sawing open a frozen steel gas cylinder in Deepwater, New Jersey, on 6 April 1938 to reveal waxy white Teflon powder, alongside Stephanie Kwolek in Wilmington in 1965 spinning a cloudy liquid-crystalline solution into golden Kevlar fibre five times stronger than steel), title question by 0:07, promise by 0:15, stakes by 0:25, first concrete answer & real fact (Leo Baekeland's July 1907 Bakelite, Hermann Staudinger's 1920 macromolecule chains, Roy Plunkett's 6 April 1938 Teflon, and Stephanie Kwolek's 1965 Kevlar five times stronger than steel by weight) by 0:34.
- **Explorer limits:** 2 beats total (`[EXPLORER ACTS: once. …]`), at 1:05 (Part 01, outside the first minute) and 6:05 (Part 04 comparing a tangled bowl of spaghetti against rigid logs aligning down a narrow chute into a bulletproof Kevlar barrier).
- **Chapter cold opens & cliffhanger questions:** Part 01 ends on how humans went from carving billiard balls out of elephant tusks to cooking up synthetic molecules and why leading chemists told Hermann Staudinger in 1920 that giant molecules were impossible; Part 02 opens cold on the $10,000 gold prize for an elephant-ivory substitute, Leo Baekeland's July 1907 cast-iron Bakelizer in Yonkers, and Hermann Staudinger's 1920 ETH Zurich proof of covalent macromolecules against the "molecular weight above 5,000 do not exist" dogma, ending on what happened on 6 April 1938 when a young DuPont chemist opened a tank of frozen gas and nothing came out; Part 03 opens cold on the midpoint twist ("Case closed — had the gas leaked out overnight? Wrong! When Plunkett put the 'empty' steel cylinder on the scales, it still weighed the exact full weight of the gas!" — sawing open the steel cylinder with a hacksaw to find PTFE / Teflon and explaining its carbon-fluorine armour from 1943 Manhattan Project seals to Marc Grégoire's 1954 non-stick pan), ending on why Stephanie Kwolek in 1965 refused to pour a cloudy, watery beaker down the drain; Part 04 opens cold on Kwolek's 1964–1965 search for lightweight tyre cord, spinneret operator Charles Smullen refusing to spin her cloudy buttermilk-like liquid, and the liquid-crystal alignment that made Kevlar five times stronger than steel by weight, ending on what happened when materials built to last forever were used to make wrappers thrown away after five minutes; Part 05 opens cold on the harmless-substitute misconception, explains why bacterial enzymes cannot cleave synthetic covalent chains across 400 million tonnes of annual production, and hands off to William Henry Perkin's Easter 1856 accidental purple dye, Ronald Ross's 20 August 1897 mosquito dissection, and Tu Youyou's 4 October 1971 340 AD cold-ether artemisinin (`048`).
- **Quirky anecdote before the hard idea:** Roy Plunkett and Jack Rebok poking a wire through a silent cylinder valve, weighing the "empty" tank on the scales, and sawing the steel cylinder in half with a hacksaw; Charles Smullen refusing to let Stephanie Kwolek pour her cloudy "buttermilk" solution into his platinum spinneret holes for fear it would clog the machine.
- **Rivalry / tension:** Staudinger vs the 1920s organic chemistry establishment ("organic molecules with a molecular weight above 5,000 do not exist!"); Kwolek vs the textbook rule that only crystal-clear syrups can be spun into fibres.
- **Misconception explained away:** "When Leo Baekeland invented Bakelite in nineteen oh seven, people assumed synthetic plastics were just cheap, harmless substitutes that would spare elephant herds and vanish into the soil like wood or cotton" — explained via Staudinger's unbroken covalent carbon-carbon and carbon-fluorine chains that bacterial enzymes never evolved to snip apart (Part 05, 6:43).

## For Chief to decide

1. Lock **047 = Accidental Plastics & Bulletproof Kevlar: Leo Baekeland's 1907 Bakelite, Hermann Staudinger's 1920 Giant-Chain Proof, Roy Plunkett's 6 April 1938 Frozen Teflon Cylinder & Stephanie Kwolek's 1965 Cloudy Kevlar (1907–1965)** and pick the 2-way Test & Compare working title pair:
   - **A (Subject + hook, §1 rule 11):** *Teflon & Kevlar: The Lab Accidents Stronger Than Steel* (54 chars)
   - **B (Search question, §1 rule 2):** *How a Frozen Gas Cylinder and Cloudy Liquid Created Teflon and Kevlar* (69 chars)
   - **Alt (Search / twist question):** *Why an "Empty" Gas Tank and a Cloudy Beaker Changed Modern Materials* (68 chars)
2. Review `plastics_script_master_v01.md` (91.0/100 PASS), then queue the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

## Score (`npm run review:script`)

```text
# plastics_script_master_v01.md

**Decision:** PASS · **Score:** 91 / 100

| Dimension | Score |
|---|---:|
| hook | 9.5 |
| curiosity | 9.5 |
| storytelling | 8 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 7.2 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1553 · Est. min: 10.4 · Chapters: 4

## Cold open excerpt

> Why doesn't a fried egg stick to your non-stick pan — and how can a thin vest of yellow cloth stop a speeding pistol bullet? How did a twenty-seven-year-old chemist on the sixth of April nineteen thirty-eight, sawing open an "empty" steel gas cylinder that still weighed full weig

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 91/100 — proceed to VO after production checklist.

Pass threshold: 90
```
