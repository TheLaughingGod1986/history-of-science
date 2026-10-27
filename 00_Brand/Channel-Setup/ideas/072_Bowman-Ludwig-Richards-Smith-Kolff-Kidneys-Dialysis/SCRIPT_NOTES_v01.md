# 072 script v01: notes for review (J0690)

Script: `kidneys_script_master_v01.md` (with `opening_and_outline_v00.md`, `SOURCES_v00.md` and `SOURCES_v01.md`).

**Draft only (J0690, Gemini Argon, 20 Oct 2026).** Built from `072_Bowman-Ludwig-Richards-Smith-Kolff-Kidneys-Dialysis/opening_and_outline_v00.md` and the neighbour and search evidence in `IDEAS_2026-10-19_J0682.md` (`evidence_2026-10-19_J0682/n_kidneys_dialysis.md` PASS — 6 education videos ≥ 1M views, with 5 strictly on kidneys, the nephron & urinary filtration: **TED-Ed ★ *Is it bad to hold your pee? - Heba Shaheed* (`Ze4Qmpq48AQ`, 9.55M)**, **CrashCourse *Urinary System, Part 1: Crash Course Anatomy & Physiology #38* (`l128tW1H5a8`, 5.76M — exact subject match!)**, **TED-Ed ★ *How do your kidneys work? - Emma Bryce* (`FN3MFhYPWWo`, 3.11M — exact subject match!)**, **Khan Academy *The kidney and nephron | Renal system physiology* (`cc8sUv2SuaY`, 2.94M — exact subject match!)**, and **Amoeba Sisters *Excretory System and the Nephron* (`q5qaGHfdmYM`, 2.93M — exact subject match!)**, plus **Khan Academy *Secondary active transport in the nephron* (`czY5nyvZ7cU`, 764.7k)**, **Cognito *How the Kidneys Work* (`gWnIFIdDeto`, 716.0k)**, **TED-Ed ★ *How does kidney transplant surgery work? - Alexander H. Toledo* (`al_H8f1cG-I`, 439.5k)**, and **TEDx *Queen of dialysis describes her dependence on a machine* (`wxhbkn4H02U`, 160.4k)**, alongside `public_search.md` & `public_search_titles.md` showing `"how do your kidneys work"` is an exact YouTube autocomplete match (`yes`), all 5 top GB search results for `"william bowman alfred richards willem kolff dialysis"` under 13k views, and all 3 top GB slots for *How Sausage Casings and a Tin Can Built the First Artificial Kidney* under 120 views). The topic isn't locked yet: Chief locks `072` and the working title pair first, then reviews/signs off this script and queues the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

Structure (*Reference lessons* §1, scripts from 011 on): every chapter opens cold and ends on a question the next one answers; the midpoint twist ("Case closed — no engineer would ever build a factory that throws away ninety-nine percent of its raw material every forty minutes and spends all day picking it back up off the floor! Wrong! That is exactly how your kidney works — because your kidney was originally designed four hundred million years ago inside a prehistoric fish drowning in fresh river water!" — where Homer Smith and James Shannon in 1934–July 1935 in *J. Clin. Invest.* measured the human glomerular filtration rate at `125 mL/min = 180 L/day` with Jerusalem artichoke `inulin`, and Smith in *From Fish to Philosopher* 1953 alongside Friedrich Henle's 1862 and Werner Kuhn's 1951 `Loop of Henle` countercurrent multiplier explained why vertebrates dump 180 L a day and reabsorb 99%) lands in Part 03; Willem Kolff's 17 March 1943 – 11 September 1945 rotating-drum cellophane sausage-casing artificial kidney in Nazi-occupied Kampen (waking Patient #16 Sofia Schafstadt from a terminal uremic coma after 11.5 hours of hemodialysis) lands in Part 04; how modern dialysis and kidney transplants (`Joseph Murray, 23 December 1954`) save millions is explained in Part 05; the ending hands off directly to `073` (*How Do Giant Trees Drink Water 100 Metres Into the Sky When Suction Fails Above 10 Metres (`Xylem, Transpiration Pull & the Cohesion-Tension Theory`)?*), with no goodbye and no subscribe ask. Five VO parts, matching 009–071.

## Marker count (v01)

Run on `kidneys_script_master_v01.md`: `grep -o "DATA:" … | wc -l`, and the same for each marker.

| Marker | Count | Where | Rule |
|---|---:|---|---|
| `DATA` | **6** | 1) inked nephron filtration & reabsorption balance chart on period paper showing 5 litres total blood volume filtered 36 times/day at 125 mL/min = 180 litres/day glomerular filtrate, 99% water and 100% glucose reabsorbed, and 1.5 litres/day urine output (0:34); 2) inked Wearn & Richards (1 October 1924 Am. J. Physiol. 71: 209–227) frog glomerular fluid vs bladder urine chemical table showing glomerular filtrate has 0 protein, full blood glucose, and full NaCl, while final bladder urine has 0 glucose and ~1/10th the salt (0:52); 3) inked Bowman (17 February 1842 Phil. Trans. R. Soc. 132: 57–80) glomerular capsule diagram & Wearn & Richards (1 October 1924 Am. J. Physiol. 71: 209–227) micropuncture reabsorption profile along the nephron on period paper (1:58); 4) inked Homer Smith & James Shannon (July 1935 J. Clin. Invest. 14: 393–401) human inulin clearance chart (GFR = 125 mL/min = 180 L/day) alongside Werner Kuhn (1951) Loop of Henle countercurrent osmotic gradient diagram (300 to 1,200 mOsm/L) on period paper (3:47); 5) inked Willem Kolff (1944 Acta Med. Scand. 117: 121–134 & 11 September 1945 Sofia Schafstadt Kampen chart) rotating-drum cellophane dialyser schematic & blood urea clearance curve on period paper (5:32); 6) animated timeline building 17 Feb 1842 & 1844 · 1 Oct 1924 & 1934 · 17 Mar 1943 – 11 Sep 1945 (6:48) | 3 or more per long, including the animated timeline |
| `SCALE` | **6** | 1) your kidneys clean your house by throwing every single piece of furniture out the window thirty-six times a day — and then running downstairs to carry ninety-nine percent of the furniture back inside while leaving the rubbish on the pavement (0:34); 2) puncturing a single Bowman's capsule with a quartz needle ten micrometres wide is like threading a needle thinner than a human hair into a water balloon the size of a grain of sand without popping the blood vessels inside (0:52); 3) your two fist-sized kidneys pack two million microscopic filter cups connected to eighty kilometres of hair-thin tubing — enough microscopic plumbing coiled inside your lower back to stretch from London to Brighton (1:58); 4) because our ancient fish ancestors needed a giant bilge pump to bail out river water, your kidneys still dump a 180-litre bathtub of fluid every day — and use the hairpin Loop of Henle like a salt sponge to wring 99% of that bathtub back into your veins (3:47); 5) Willem Kolff replaced two million microscopic Bowman's capsules with forty metres of butcher's sausage skin wrapped round a wooden drum — using tiny pores in cellulose that let small urea poison molecules slip out into salt water while holding every red blood cell inside (5:32); 6) from a 25-year-old surgeon's microscope in London to a hair-thin quartz needle in Philadelphia and forty metres of sausage skin in wartime Holland, scientists unlocked the two-million-filter cleaning plant that keeps our blood pure (6:48) | Every `DATA` number gets a `SCALE:` comparison (`grep -c "SCALE:"` ≥ `DATA:` count) |
| `WHO` | **11** | William Bowman (0:34), Carl Ludwig (0:34), Joseph T. Wearn (0:34), Alfred Newton Richards (0:34), Homer W. Smith (0:34), Willem Johan Kolff (0:34), James A. Shannon (3:13), Friedrich Gustav Jakob Henle (3:13), Werner Kuhn (3:13), Thomas Graham (4:58), Sofia Maria Schafstadt (4:58) | First mention only, role right for the scene's year (4 words or fewer) |
| `WHEN` | **28** | Kampen, 11 September 1945 (0:00), 17 February 1842 (0:34), 1844 (0:34), 1 October 1924 (0:34), 1934 (0:34), 11 September 1945 (0:34), 1666 (1:28), 17 February 1842 (1:28), 1844 (1:28), 1874 (1:28), 1 October 1924 (1:28), 1862 (3:13), 1934 (3:13), July 1935 (3:13), 1951 (3:13), 1953 (3:13), 1861 (4:58), October 1938 (4:58), 17 March 1943 (4:58), 1944 (4:58), 11 September 1945 (4:58), 1960 (4:58), 1842–1960 (6:48), 23 December 1954 (7:20), 1727 (7:45), 1891 (7:45), 15 November 1894 (7:45), 16 April 1965 (7:45) | Every spoken date or era; later dates drop onto the timeline |
| `FACT` | **3** | 80 km of kidney tubes (1:28); 36x your blood filtered daily (3:13); Built from sausage skin (4:58) | 2–4 per long (4 words or fewer per card) |

## Craft checks (*Reference lessons* §1 + *Polish pass*)

- **First-minute timings:** Answer image by 0:03 (glowing human kidney cross-section zooming into a nephron as high-pressure blood enters the glomerulus inside Bowman's capsule while Willem Kolff's cellophane sausage-casing drum spins in Kampen), title question by 0:07, promise by 0:15, stakes by 0:25, first concrete answer & real fact (Bowman's 17 February 1842 glomerular capsule, Ludwig's 1844 ultrafiltration, Wearn & Richards's 1 October 1924 quartz micropipette puncture, Smith's 1934 `180 L/day` inulin clearance, and Kolff's 11 September 1945 sausage-casing artificial kidney) by 0:34.
- **Explorer limits:** 2 beats total (`[EXPLORER ACTS: once. …]`), at 1:05 (Part 01, outside the first minute) and 6:08 (Part 04 turning Kolff's wooden-slat drum handle as grey urea motes diffuse out through the cellophane sausage pores while red blood marbles stay safely inside).
- **Chapter cold opens & cliffhanger questions:** Part 01 ends on why nineteenth-century scientists fought an 80-year war over how a kidney makes urine and how William Bowman (1842) and Alfred Richards (1924) proved what happens inside those two million microscopic cups; Part 02 opens cold on the two-century puzzle after Marcello Malpighi (1666), tells the story of William Bowman's 17 February 1842 *Phil. Trans. R. Soc.* capsule, Carl Ludwig's 1844 mechanical pressure sieve, and Joseph Wearn & Alfred Newton Richards's 1 October 1924 *Am. J. Physiol.* `10-micrometre` quartz micropipette proof, and ends on why Homer Smith's 1934 measurement with artichoke sugar shocked every doctor in the world; Part 03 opens cold on the midpoint twist ("Case closed — no engineer would ever build a factory that throws away ninety-nine percent of its raw material every forty minutes and spends all day picking it back up off the floor! Wrong!"), tells the story of Homer Smith and James Shannon's 1934–July 1935 *J. Clin. Invest.* `125 mL/min = 180 L/day` `inulin` clearance and Smith's 1953 freshwater-fish evolutionary explanation alongside Henle's 1862 and Werner Kuhn's 1951 `Loop of Henle` countercurrent multiplier, and ends on how a young Dutch doctor under Nazi occupation built the first working artificial kidney out of butcher's sausage casings and a laundry tub; Part 04 opens cold on fifteen patients in a row dying until 67-year-old Sofia Schafstadt woke up on 11 September 1945, explains Willem Kolff's 1943–1945 Kampen rotating-drum cellophane dialyser, and ends on how a 100-metre giant redwood tree hauls 2,000 litres of water a day into the sky with zero heart and zero moving parts when suction fails at 10.3 metres; Part 05 opens cold on how Kolff's machine and Joseph Murray's 23 December 1954 twin kidney transplant save millions today, and hands off to Stephen Hales (1727), Eduard Strasburger (1891), Henry Dixon and John Joly (15 November 1894), and Per Scholander (16 April 1965) (`073`).
- **Quirky anecdote before the hard idea:** Homer Smith using sugar from Jerusalem artichoke tubers (`inulin`) to clock the human kidney at 180 litres a day; Willem Kolff building the first life-saving artificial kidney in Nazi-occupied Holland out of 40 metres of butcher's cellophane sausage casing, wooden slats, a porcelain enamel laundry tub, a sewing-machine motor, and a Ford Model T water-pump coupling!
- **Rivalry / tension:** Vitalist tubular secretion (`Bowman, Heidenhain`) vs mechanical pressure filtration (`Ludwig`), settled after 80 years by Wearn & Richards's quartz needle; 15 straight fatal dialysis trials vs Patient #16 Sofia Schafstadt waking up on 11 September 1945.
- **Misconception explained away:** "Why doesn't the kidney just selectively filter out the 1.5 litres of waste instead of dumping 180 litres of water and sugar every day?" — explained via freshwater fish osmosis evolution and the hairpin `Loop of Henle` countercurrent salt multiplier (Part 03).

## For Chief to decide

1. Lock **072 = How Do Two Fist-Sized Kidneys Filter 180 Litres of Blood Every Day (and How Did Sausage Casings & a Tin Can Build the First Artificial Kidney — `Kidneys, the Nephron & Willem Kolff's 1943 Dialysis Machine`)? William Bowman's 17 February 1842 Microscopic Capsule, Carl Ludwig's 1844 Physical Filtration Theory, Joseph Wearn & Alfred N. Richards's October 1924 Quartz Micropipette Puncture of a Living Frog Glomerulus, Homer Smith's 1934 Inulin Clearance, and Willem Kolff's 1943–11 September 1945 Nazi-Occupied Kampen Sausage-Casing Artificial Kidney (1842–1960)** and pick the 2-way Test & Compare working title pair:
   - **A (Subject + hook, §1 rule 11):** *The Kidney: How Sausage Skin Saved Millions* (43 chars)
   - **B (Search question, §1 rule 2):** *How Sausage Casings and a Tin Can Built the First Artificial Kidney* (67 chars)
   - **Alt (Search / twist question):** *Why Your Kidneys Filter a Bathtub of Blood Every Single Day* (59 chars)
2. Review `kidneys_script_master_v01.md` (91.5/100 PASS), then queue the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

## Score (`npm run review:script`)

```text
# kidneys_script_master_v01.md

**Decision:** PASS · **Score:** 91.5 / 100

| Dimension | Score |
|---|---:|
| hook | 9.5 |
| curiosity | 9.1 |
| storytelling | 8 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 8.4 |
| retentionPotential | 8.7 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1820 · Est. min: 12.1 · Chapters: 4

## Cold open excerpt

> How do two fist-sized kidneys filter one hundred and eighty litres of blood every single day — enough to fill a bathtub — when your entire body only holds five litres of blood ? Why did evolution build a cleaning plant that dumps ninety-nine percent of your water just to haul it 

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 91.5/100 — proceed to VO after production checklist.

Pass threshold: 90
```
