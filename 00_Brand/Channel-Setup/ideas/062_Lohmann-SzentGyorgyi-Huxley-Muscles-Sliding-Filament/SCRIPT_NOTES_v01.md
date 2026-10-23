# 062 script v01: notes for review (J0645)

Script: `muscles_script_master_v01.md` (with `opening_and_outline_v00.md`, `SOURCES_v00.md` and `SOURCES_v01.md`).

**Draft only (J0645, Gemini Argon, 19 Oct 2026).** Built from `062_Lohmann-SzentGyorgyi-Huxley-Muscles-Sliding-Filament/opening_and_outline_v00.md` and the neighbour and search evidence in `IDEAS_2026-10-19_J0621.md` (`evidence_2026-10-19_J0621/n_muscles_sliding_filament.md` PASS — 8 education videos ≥ 1M views, ALL 8 strictly on muscles & sliding filaments: **TED-Ed ★ *What makes muscles grow? - Jeffrey Siegel* (`2tM1LFFxeKg`, 23.70M — exact subject match!)**, **TED-Ed ★ *How stretching actually changes your muscles - Malachy McHugh* (`g1pb2aK2we4`, 12.93M — exact subject match!)**, **CrashCourse *Muscles, Part 1 - Muscle Cells: Crash Course Anatomy & Physiology #21* (`Ktv-CaOt6UQ`, 8.24M — exact subject match!)**, **TED-Ed ★ *The surprising reason our muscles get tired - Christian Moro* (`rLsimrBoYXc`, 5.82M — exact subject match!)**, **TED-Ed ★ *How do steroids affect your muscles* (`itEXhxjOPjk`, 3.95M)**, **TED-Ed ★ *How your muscular system works - Emma Bryce* (`VVL-8zr2hk4`, 3.23M — exact subject match!)**, **Amoeba Sisters *Muscle Tissues and Sliding Filament Model* (`dpxalWACO7k`, 2.86M — exact sliding filament match!)**, and **Khan Academy *Myosin and actin* (`zopoN2i7ALQ`, 1.08M — exact myosin & actin match!)**, alongside `public_search.md` & `public_search_titles.md` showing `"sliding filament theory muscle contraction"` triggering exact YouTube autocomplete and 3 of the top 5 GB search results for `"hugh huxley andrew huxley sliding filament muscle"` under 53k views). The topic isn't locked yet: Chief locks `062` and the working title pair first, then reviews/signs off this script and queues the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

Structure (*Reference lessons* §1, scripts from 011 on): every chapter opens cold and ends on a question the next one answers; the midpoint twist ("Case closed — when a muscle contracts, its long protein molecules must coil up and shrink like tiny rubber springs! Wrong! Neither the thick myosin rods nor the thin actin ropes get a single nanometre shorter — they slide past each other like interlocking fingers!" — where Hugh Huxley & Jean Hanson at MIT and Andrew Huxley & Rolf Niedergerke at Cambridge published back-to-back in *Nature* on 22 May 1954 proving the Sliding Filament Theory) lands in Part 03; Hugh Huxley's 1957–1969 electron micrographs of swinging myosin cross-bridges, Richard Lymn and Edwin Taylor's December 1971 four-step ATPase cross-bridge cycle (`ATP` binding detaches myosin from rigor), and Setsuro Ebashi's 1963 `troponin` & calcium (`Ca²⁺`) safety lock land in Part 04; the "lactic acid poison" misconception ("Many people still blame 'lactic acid' for why their muscles burn during a hard sprint and ache the next morning") is raised and explained away in Part 05 via lactate as clean heart/muscle fuel vs free inorganic phosphate (`Pi`) ions jamming the cross-bridge power stroke and calcium release; the ending hands off directly to `063` (*Why Are Mitochondria the Powerhouse of the Cell (and How Do They Burn Food Without Setting You on Fire — `The Krebs Cycle, Chemiosmosis & Endosymbiosis`)? Hans Krebs's June 1937 Rejected Citric Acid Cycle, Peter Mitchell's July 1961 Country-Mansion Proton Dam (`Chemiosmosis`), and Lynn Margulis's March 1967 Ancient Swallowed-Bacteria Proof*), with no goodbye and no subscribe ask. Five VO parts, matching 009–061.

## Marker count (v01)

Run on `muscles_script_master_v01.md`: `grep -o "DATA:" … | wc -l`, and the same for each marker.

| Marker | Count | Where | Rule |
|---|---:|---|---|
| `DATA` | **6** | 1) inked sarcomere sliding-filament chart on period paper comparing relaxed (~2.5 micrometres) and contracted (~1.6 micrometres) muscle sarcomeres, proving thick myosin filaments (A-band, 1.6 micrometres) and thin actin filaments (1.0 micrometre) never shorten, but slide past each other powered by ~50–75 kg/day of recycled ATP (0:34); 2) inked 4-step actomyosin cross-bridge cycle diagram showing ATP binding (detachment from rigor), ATP hydrolysis to ADP + Pi (cocking the myosin lever arm), actin re-attachment, and phosphate release driving a ~5–10 nanometre, ~4 piconewton power stroke (0:52); 3) inked ATP hydrolysis energy & Szent-Györgyi actomyosin contraction chart on period paper from Lohmann (August 1929, Naturwissenschaften 17: 624–625), Fiske & SubbaRow (October 1929, Science 70: 381–382), Engelhardt & Lyubimova (1939, Nature 144: 668–669), and Szent-Györgyi (1942) showing ATP splitting into ADP + Pi (~30.5 to 50 kJ/mol released) to drive actomyosin thread superprecipitation and contraction, with the human body holding ~50–100 g of ATP and recycling ~50–75 kg/day (1:58); 4) inked Andrew Huxley & Niedergerke (22 May 1954, Nature 173: 971–973) and Hugh Huxley & Hanson (22 May 1954, Nature 173: 973–976) sarcomere striation measurement chart on period paper plotting A-band width (constant at ~1.6 micrometres across all sarcomere lengths from 3.0 down to 1.6 micrometres) vs I-band and H-zone widths decreasing linearly as thin actin filaments slide past thick myosin filaments (3:42); 5) inked Hugh Huxley (1969, Science 164: 1356–1365), Lymn & Taylor (December 1971, Biochemistry 10: 4617–4624), and Ebashi (1963–1965, Nature) calcium-troponin switch & actomyosin cross-bridge cycle chart on period paper showing Ca2+ binding troponin to shift tropomyosin off actin binding sites, followed by ATP detachment, hydrolysis cocking, and Pi-release 10-nm power stroke (5:28); 6) animated timeline building Aug–Oct 1929 & 1939 · 1941–1942 · 22 May 1954 · 1957–1971 (6:43) | 3 or more per long, including the animated timeline |
| `SCALE` | **6** | 1) when you lift a heavy suitcase, not a single protein fibre inside your arm actually shrinks — instead, billions of microscopic myosin hands haul actin ropes hand-over-hand like a tug-of-war team pulling a ship into harbour (0:34); 2) each individual myosin hand pulls the rope just ten billionths of a metre — ten nanometres — yet trillions of them firing together in your legs can launch your entire body into the air (0:52); 3) your body holds only about fifty grams of ATP at any one moment, yet because every molecule is discharged and recharged nearly a thousand times a day, you burn through your own body weight in ATP every twenty-four hours (1:58); 4) if you interlace the fingers of your left and right hands and slide your palms together, your overall span gets shorter even though not a single finger changed length — and that is how every muscle in your body contracts (3:42); 5) counterintuitively, a muscle doesn't need fresh ATP to grab the rope — it needs fresh ATP to let go of the rope for the next pull, which is why running out of ATP after death locks muscles rigid in rigor mortis (5:28); 6) from rabbit muscle threads shrinking on a table in war-torn Hungary to two Englishmen named Huxley publishing side by side in Nature, science revealed the walking molecular motors that move every breath, heartbeat, and step of your life (6:43) | Every `DATA` number gets a `SCALE:` comparison (`grep -c "SCALE:"` ≥ `DATA:` count) |
| `WHO` | **10** | Karl Lohmann (0:34), Cyrus H. Fiske (0:34), Yellapragada SubbaRow (0:34), Albert Szent-Györgyi (0:34), Hugh E. Huxley (0:34), Jean Hanson (0:34), Andrew F. Huxley (0:34), Rolf Niedergerke (0:34), Brunó F. Straub (1:28), Setsuro Ebashi (4:53) | First mention only, role right for the scene's year (4 words or fewer) |
| `WHEN` | **20** | London, 22 May 1954 (0:00), August 1929 (0:34), October 1929 (0:34), 1942 (0:34), 22 May 1954 (0:34), August 1929 (1:28), October 1929 (1:28), 1939 (1:28), 1941 (1:28), 1942 (1:28), 1953 (3:08), 22 May 1954 (3:08), 1957 (4:53), 1963 (4:53), 20 June 1969 (4:53), December 1971 (4:53), 1929–1971 (6:43), June 1937 (7:45), July 1961 (7:45), March 1967 (7:45) | Every spoken date or era; later dates drop onto the timeline |
| `FACT` | **3** | Lifeless threads contracted in a dish (1:28); 22 May 1954: two Huxleys, one issue (3:08); No ATP locks muscles stiff (4:53) | 2–4 per long (4 words or fewer per card) |

## Craft checks (*Reference lessons* §1 + *Polish pass*)

- **First-minute timings:** Answer image by 0:03 (inside a flexing human bicep, thick myosin motor heads grabbing thin actin ropes, snapping a phosphate off `ATP`, and hauling the ropes hand-over-hand without either filament changing length), title question by 0:07, promise by 0:15, stakes by 0:25, first concrete answer & real fact (Lohmann and Fiske & SubbaRow's 1929 `ATP`, Szent-Györgyi's 1942 contracting actomyosin threads, and Hugh Huxley & Andrew Huxley's back-to-back 22 May 1954 *Nature* Sliding Filament Theory) by 0:34.
- **Explorer limits:** 2 beats total (`[EXPLORER ACTS: once. …]`), at 1:05 (Part 01, outside the first minute) and 6:05 (Part 04 dropping a `Ca2+ CALCIUM` key into the `TROPONIN-TROPOMYOSIN LOCK` so cocked myosin hands can pull).
- **Chapter cold opens & cliffhanger questions:** Part 01 ends on how chemists first found the three-phosphate battery (`ATP`) and what happened in 1942 when Albert Szent-Györgyi dripped it onto lifeless protein threads; Part 02 opens cold on the century-old heat-engine/lactic-acid assumption, tells the story of Karl Lohmann and Cyrus Fiske & Yellapragada SubbaRow's August–October 1929 discovery of `ATP`, Vladimir Engelhardt & Militsa Lyubimova's 1939 proof that myosin is an `ATPase`, and Albert Szent-Györgyi & Brunó Straub's 1941–1942 discovery of `actin` and contracting actomyosin threads in Szeged, and ends on how two unrelated Englishmen both named Huxley proved on the exact same Saturday in 1954 that the proteins never shrink at all; Part 03 opens cold on the midpoint twist ("Case closed — when a muscle contracts, its long protein molecules must coil up and shrink like tiny rubber springs! Wrong!"), tells the story of Hugh Huxley & Jean Hanson at MIT and Andrew Huxley & Rolf Niedergerke at Cambridge publishing back-to-back in *Nature* on 22 May 1954 to prove the **Sliding Filament Theory**, and ends on what invisible force pulls the actin ropes and why muscles lock in rigor mortis when `ATP` runs out; Part 04 opens cold on the rigor mortis paradox, explains Hugh Huxley's 1957–1969 myosin cross-bridges, Lymn & Taylor's December 1971 four-step ATPase cycle (`ATP` detaches the hand, hydrolysis cocks it back, phosphate release fires the 10-nm power stroke), and Setsuro Ebashi's 1963 calcium-troponin switch, and ends on what microscopic power station recharges 60 kg of `ATP` a day; Part 05 opens cold on the "lactic acid" muscle fatigue myth, explains lactate as fuel vs inorganic phosphate (`Pi`) jamming the cross-bridge motor, and hands off to Hans Krebs (June 1937 Citric Acid Cycle, rejected by *Nature*), Peter Mitchell (July 1961 `30 MV/m` proton dam), and Lynn Margulis (March 1967 endosymbiosis) (`063`).
- **Quirky anecdote before the hard idea:** Albert Szent-Györgyi in wartime Hungary squirting rabbit muscle proteins into threads and watching them contract in a dish like living muscle; two completely unrelated Englishmen named Hugh Huxley and Andrew Huxley publishing back-to-back in the same issue of *Nature* on 22 May 1954!
- **Rivalry / tension:** Folding-protein-chain dogma (held by Szent-Györgyi and Pauling) vs the two Huxleys' sliding filaments; friendly transatlantic convergence between MIT and Cambridge.
- **Misconception explained away:** "Many people still blame 'lactic acid' for why their muscles burn during a hard sprint and ache the next morning" — explained via lactate as clean fuel vs inorganic phosphate (`Pi`) ions from rapid `ATP` breakdown jamming cross-bridge force and calcium release (Part 05, 6:43).

## For Chief to decide

1. Lock **062 = How Do Your Muscles Turn Food Into Motion (and Why Do You Recycle Your Entire Body Weight in `ATP` Every Single Day — `Muscles, ATP & the Sliding Filament Motor`)? Karl Lohmann, Cyrus Fiske & Yellapragada SubbaRow's 1929 Discovery of `ATP`, Albert Szent-Györgyi's 1942 Contracting Rabbit Muscle Threads, and Hugh Huxley & Jean Hanson and Andrew Huxley & Rolf Niedergerke's Back-to-Back 22 May 1954 Sliding-Filament Proof (1929–1971)** and pick the 2-way Test & Compare working title pair:
   - **A (Subject + hook, §1 rule 11):** *How Muscles Work: The Walking Motors Inside Your Cells* (54 chars)
   - **B (Search question, §1 rule 2):** *How Your Muscles Turn Food Into Motion and Lift Heavy Weight* (60 chars)
   - **Alt (Search / twist question):** *Why You Burn Your Entire Body Weight in ATP Every Single Day* (60 chars)
2. Review `muscles_script_master_v01.md` (91.2/100 PASS), then queue the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

## Score (`npm run review:script`)

```text
# muscles_script_master_v01.md

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

Words: 1485 · Est. min: 9.9 · Chapters: 4

## Cold open excerpt

> Why do you burn through your entire body weight in a single chemical battery every twenty-four hours just to move your muscles? And how did contracting rabbit threads in war-torn Hungary and two unrelated Englishmen both named Huxley on the twenty-second of May nineteen fifty-fou

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 91.2/100 — proceed to VO after production checklist.

Pass threshold: 90
```
