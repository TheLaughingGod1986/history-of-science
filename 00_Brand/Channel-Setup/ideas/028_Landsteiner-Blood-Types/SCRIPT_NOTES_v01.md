# 028 script v01: notes for review (J0462)

Script: `landsteiner_script_master_v01.md` (with `opening_and_outline_v00.md`, `SOURCES_v00.md` and `SOURCES_v01.md`).

**Draft only (J0462, Gemini Argon, 17 Oct 2026).** Built from `028_Landsteiner-Blood-Types/opening_and_outline_v00.md` and the neighbour and search evidence in `IDEAS_2026-10-17_J0454.md` (`evidence_2026-10-17_J0454/n_bloodtypes.md` PASS — 8 education videos ≥ 1M views including 6 strictly on blood types/cells and 2 exact TED-Ed blood-type films ≥ 1M: **TED-Ed ★ *Why do blood types matter? - Natalie S. Hodge* (`xfZhb6lmxjk`, 6.75M)**, **CrashCourse *Blood, Part 1 - True Blood* (`HQWlcSp9Sls`, 4.60M)**, **Amoeba Sisters *Multiple Alleles (ABO Blood Types) and Punnett Squares* (`9O5JQqlngFY`, 3.34M)**, **SciShow *What are Blood Types?* (`ttjn1jVACk8`, 1.70M)**, **SciShow *The Pros & Cons of Your Blood Type* (`cEhUj_BKzGI`, 1.48M)**, and **TED-Ed ★ *What happens if you're injected with the wrong blood type? - Bill Schutt* (`qcZKbjYyOfE`, 1.42M)**, alongside `public_search.md` showing `"karl landsteiner blood types"` and `"why do blood types matter"` both autocompleting in GB search with all 5 top GB slots for `"karl landsteiner blood types"` under 537k views). The topic isn't locked yet: Chief locks `028` and the working title pair first, then reviews/signs off this script and queues the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

Structure (*Reference lessons* §1, scripts from 011 on): every chapter opens cold and ends on a question the next one answers; the midpoint twist ("Case closed? Wrong." — even after Karl Landsteiner discovered the A, B, and O blood groups in 1900–1901 and Reuben Ottenberg introduced pre-transfusion cross-matching by 1911, hospitals still could not store a single bottle of blood because freshly drawn blood clots solid in glass within 4 to 6 minutes, forcing Alexis Carrel in 1908 to stitch a living donor's wrist artery directly to a newborn baby's leg vein until Luis Agote in November 1914 and Richard Lewisohn on 23 January 1915 proved that 0.2% sodium citrate safely prevents clotting and Oswald Hope Robertson built the world's first blood bank in iced ammunition boxes in November 1917) lands in Part 04; the popular misconception ("Many people wonder what the plus or minus sign after their blood type actually means — or assume that once A, B, and O were matched, every blood transfusion was completely safe") is raised and explained away in Part 05 via Landsteiner and Alexander S. Wiener's January 1940 Rhesus (`Rh`) factor discovery and today's 118.5 million annual blood donations; the ending hands off directly to `029` (*The Silicon Transistor & Microchip: Bardeen, Brattain & Shockley's 16 December 1947 Point-Contact Transistor at Bell Labs & Jack Kilby and Robert Noyce's 1958–1959 Integrated Circuit*), with no goodbye and no subscribe ask. Five VO parts, matching 009–027.

## Marker count (v01)

Run on `landsteiner_script_master_v01.md`: `grep -o "DATA:" … | wc -l`, and the same for each marker.

| Marker | Count | Where | Rule |
|---|---:|---|---|
| `DATA` | **6** | 1) inked 6 × 6 agglutination table on period paper from Landsteiner's 14 November 1901 paper ("Über Agglutinationserscheinungen normalen menschlichen Blutes") showing smooth mixing (–) vs fatal clumping (+) across Groups A, B, and C (O) (0:34); 2) inked coagulation & scale chart comparing 4–6 minutes (untreated blood clotting in glass) vs 2–3 weeks (with 0.2% sodium citrate in cold storage) and 118.5 million safe blood donations per year today (0:52); 3) inked timeline & survival chart on period paper comparing 1667 animal-to-human transfusions (banned 1668–1670), Blundell's 1818–1829 un-typed human-to-human transfusions (~50% random incompatibility / high mortality), and 1901 ABO-matched transfusions (1:58); 4) inked molecular diagram on period paper showing red blood cell surface antigens (A pegs, B spheres, AB both, O smooth) and Y-shaped plasma antibodies (anti-B, anti-A, none, both) demonstrating why Type O red cells pass unattacked as universal donor and Type AB accepts all red cells (3:42); 5) inked diagram on period paper showing calcium-driven fibrin clotting in untreated blood (4–6 min) vs 0.2% sodium citrate chelating Ca²⁺ ions allowing 14–26 days of cold storage in Robertson's November 1917 Western Front icebox (5:28); 6) animated timeline building Dec 1667 · 22 Dec 1818 · Feb 1900 & 14 Nov 1901 · 23 Jan 1915 & Nov 1917 · 1930 & Jan 1940 · Today alongside an inked global transfusion chart (118.5 million annual blood donations = ~3.8 donations every second, with O-negative as universal emergency donor) (6:43) | 3 or more per long, including the animated timeline |
| `SCALE` | **6** | 1) a single mismatched transfusion can clump and shatter billions of red blood cells inside a patient's veins in minutes (0:34); 2) just two grammes of sodium citrate per litre of blood — less than half a teaspoon — turned a 6-minute surgical emergency into modern blood banks (0:52); 3) flipping a coin with a patient's life — before blood typing, nearly half of all human blood transfusions triggered a dangerous or fatal immune reaction (1:58); 4) each red blood cell carries around 2 million microscopic A or B sugar markers on its skin — if the wrong antibody locks on, millions of cells glue together like Velcro (3:42); 5) storing Type O blood on ice in 1917 turned transfusion from a two-surgeon emergency operation into a bottle waiting at the front line (5:28); 6) 118.5 million blood donations every year — nearly four life-saving bags of blood collected every single second around the globe (6:43) | Every `DATA` number gets a `SCALE:` comparison (`grep -c "SCALE:"` ≥ `DATA:` count) |
| `WHO` | **12** | Jean-Baptiste Denys (0:21), Karl Landsteiner (0:34), Richard Lewisohn (0:52), James Blundell (1:58), Leonard Landois (2:32), Alfred von Decastello (3:42), Adriano Sturli (3:42), Alexis Carrel (4:53), Reuben Ottenberg (4:53), Luis Agote (5:28), Oswald Hope Robertson (5:28), Alexander S. Wiener (6:43) | First mention only, role right for the scene's year (4 words or fewer) |
| `WHEN` | **24** | Vienna February 1900 (0:00), Paris December 1667 (0:21), February 1900 (0:34), 14 November 1901 (0:34), 23 January 1915 (0:52), 15 June 1667 (1:28), December 1667 (1:28), 1670 (1:28), 22 December 1818 (1:58), 1829 (1:58), 1875 (2:32), February 1900 (3:08), 14 November 1901 (3:08), 1902 (3:42), New York 8 March 1908 (4:53), 1911 (4:53), 9 November 1914 (5:28), 23 January 1915 (5:28), Western Front November 1917 (5:28), 1930 (6:43), January 1940 (6:43), 1667–1940 (6:43), 16 December 1947 (7:45), 12 September 1958 (7:45) | Every spoken date or era; later dates drop onto the timeline |
| `FACT` | **4** | Animal blood banned in 1670 (1:28); First printed in a footnote (3:08); First blood bank in ammo boxes (5:28); 118 million donations a year (6:43) | 2–4 per long (4 words or fewer per card) |

## Craft checks (*Reference lessons* §1 + *Polish pass*)

- **First-minute timings:** Answer image by 0:03 (Karl Landsteiner in Vienna in February 1900 pipetting serum onto a 6 × 6 grid of blood drops on glass slides as half stay smooth ruby-red and half curdle into brick-red clumps), title question by 0:07, promise by 0:15, stakes by 0:25, first concrete answer & real fact (Karl Landsteiner mixing the red blood cells and serum of himself and five colleagues in February 1900 and 14 November 1901 to discover the A, B, and O blood groups) by 0:34.
- **Explorer limits:** 2 beats total (`[EXPLORER ACTS: once. …]`), at 1:05 (Part 01, outside the first minute) and 6:05 (Part 04 tipping 0.2% sodium citrate into one of two blood flasks as the untreated flask clots solid at 6 minutes).
- **Chapter cold opens & cliffhanger questions:** Part 01 ends on why nineteenth-century doctors thought clumping blood was caused by a disease and how Landsteiner's seven-line footnote in February 1900 overturned two centuries of medical guesswork; Part 02 opens cold on Jean-Baptiste Denys's June and December 1667 sheep- and calf-blood transfusions, the 1668–1670 bans, James Blundell's 22 December 1818 human-to-human revival (~50% random incompatibility), and Leonard Landois's 1875 agglutination findings, ending on how a 31-year-old researcher in Vienna proved every doctor in Europe wrong without touching a single sick patient; Part 03 opens cold on Landsteiner drawing blood from six healthy scientists in his own lab (including himself, Group O), spinning it in a centrifuge, and mixing a 6 × 6 grid of 36 drops to discover Groups A, B, and C/O (with AB added in 1902 by Decastello and Sturli), ending on why almost no surgeon used Landsteiner's discovery for another decade and why doctors still had to sew a living donor's wrist artery directly to a patient's vein; Part 04 opens cold on the midpoint twist ("Case closed? Wrong." — the 4–6 minute calcium clotting trap, Alexis Carrel's 8 March 1908 live artery-to-vein stitch, Luis Agote and Richard Lewisohn's 23 January 1915 0.2% sodium citrate breakthrough, and Oswald Hope Robertson's November 1917 WWI blood bank in iced ammunition boxes), ending on why some patients given matched A, B, or O blood still suffered dangerous reactions until Landsteiner made one last discovery at age 71; Part 05 opens cold on the `Rh` plus/minus misconception, explains Landsteiner and Alexander S. Wiener's January 1940 Rhesus factor discovery and 118.5 million annual blood donations, and hands off to John Bardeen and Walter Brattain's 16 December 1947 point-contact transistor at Bell Labs and Jack Kilby and Robert Noyce's 1958–1959 silicon microchip (`029`).
- **Quirky anecdote before the hard idea:** Landsteiner first announcing the discovery of human blood groups in a seven-line footnote in February 1900 using his own blood (Group O) and five labmates; Oswald Hope Robertson building the world's first blood bank on the Western Front in November 1917 by packing citrated bottles in sawdust and ice inside old artillery ammunition boxes.
- **Rivalry / tension:** Two centuries of fatal medical guesswork (from Denys's 1667 calf-blood crisis to Carrel's 1908 artery-to-vein emergency surgery) overturned by Landsteiner's 6 × 6 slide grid and Lewisohn's 0.2% pinch of citrus salt.
- **Misconception explained away:** "Many people wonder what the plus or minus sign after their blood type actually means — or assume that once A, B, and O were matched, every blood transfusion was completely safe" — explained via Landsteiner and Wiener's January 1940 Rhesus (`Rh`) factor discovery (Part 05, 6:43).

## For Chief to decide

1. Lock **028 = Blood Types & Safe Transfusions: Why Blood Clumps — Karl Landsteiner's 1900 Vienna Blood-Mixing Experiment & Richard Lewisohn's 1915 Sodium Citrate (1667–1915)** and pick the 2-way Test & Compare working title pair:
   - **A (Subject + hook, §1 rule 11):** *Blood Types: Why Transfusions Killed Half of All Patients* (57 chars)
   - **B (Search question, §1 rule 2):** *How Mixing Six Scientists' Blood Solved Safe Transfusions* (57 chars)
   - **Alt (Search / twist question):** *Why Doctors Were Banned From Transfusing Blood for 150 Years* (60 chars)
2. Review `landsteiner_script_master_v01.md` (94.4/100 PASS), then queue the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

## Score (`npm run review:script`)

```text
# landsteiner_script_master_v01.md

**Decision:** PASS · **Score:** 94.4 / 100

| Dimension | Score |
|---|---:|
| hook | 9.5 |
| curiosity | 9.5 |
| storytelling | 9.5 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 9.1 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1526 · Est. min: 10.2 · Chapters: 4

## Cold open excerpt

> Why did giving blood from one healthy human being to another randomly kill nearly half of all patients for two hundred years — until a Viennese doctor mixed six scientists' blood? By the end of this film, you'll see why seventeenth-century doctors put patients in deadly danger by

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 94.4/100 — proceed to VO after production checklist.

Pass threshold: 90
```
