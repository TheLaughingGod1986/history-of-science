# 020 script v01: notes for review (J0429)

Script: `penicillin_script_master_v01.md` (with `opening_and_outline_v00.md`, `SOURCES_v00.md` and `SOURCES_v01.md`).

**Draft only (J0429, Gemini Argon, 17 Oct 2026).** Built from `020_Penicillin-Fleming-Florey/opening_and_outline_v00.md` and the neighbour and search evidence in `IDEAS_2026-10-17_J0421.md` (`evidence_2026-10-17_J0421/n_penicillin.md` PASS — 7 strictly on-topic education videos ≥ 1M views including **five TED-Ed videos ≥ 1M** led by **Kurzgesagt *The Antibiotic Apocalypse Explained* 8.73M**, **TED-Ed ★ *What causes antibiotic resistance?* 4.33M**, **TED-Ed ★ *What makes tuberculosis (TB) the world's most infectious killer?* 2.87M**, **TED-Ed ★ *The accident that changed the world - Allison Ramsey and Mary Staicu* (`CNbnLgetqHs`, 1.47M — exact Alexander Fleming / Florey & Chain discovery match)**, **Amoeba Sisters *Antibiotics, Antivirals, and Vaccines* 1.39M**, **TED-Ed ★ *How can we solve the antibiotic resistance crisis?* 1.27M**, and **TED-Ed ★ *The diseases that changed humanity forever* 1.02M**, plus `public_search.md` showing `"how penicillin was discovered"` and `"alexander fleming penicillin"` autocompleting in GB search with 4 of the top 5 slots under 561k views). The topic isn't locked yet: Chief locks `020` and the working title pair first, then reviews/signs off this script and queues the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–8) before VO.

Structure (*Reference lessons* §1, scripts from 011 on): every chapter opens cold and ends on a question the next one answers; the midpoint twist ("Case closed? Wrong." — when the Oxford team treated their first dying human patient, 43-year-old policeman Albert Alexander, on 12 February 1941 and Norman Heatley bicycled through the snow to recycle unabsorbed penicillin from his urine, Britain's entire supply ran out after five days and Alexander died on 15 March 1941, forcing Florey and Heatley to smear mould spores into their coat linings and fly to Peoria, Illinois, where corn steep liquor and Mary Hunt's July 1943 mouldy cantaloupe strain *Penicillium chrysogenum* NRRL 1951 multiplied yields over 1,000-fold for D-Day) lands in Part 04; the popular misconception ("Many people think antibiotics work by boosting your immune system, or take them to fight a cold or flu") is raised and explained away in Part 05 with Dorothy Hodgkin's May 1945 X-ray crystallography structure of the four-atom beta-lactam ring bursting bacterial cell walls under 20 atmospheres of internal pressure while leaving wall-less human cells and cell-less viruses untouched; the ending hands off directly to `021` (*Electromagnetism: Hans Christian Ørsted's Twitching Compass & Michael Faraday's Cup of Mercury*), with no goodbye and no subscribe ask. Five VO parts, matching 009–019.

## Marker count (v01)

Run on `penicillin_script_master_v01.md`: `grep -o "DATA:" … | wc -l`, and the same for each marker.

| Marker | Count | Where | Rule |
|---|---:|---|---|
| `DATA` | **6** | 1) inked comparison of Fleming's 1928 mould broth (~2 units/mL, requiring 2,000 litres for 1 human course) vs the 1943 Peoria cantaloupe deep-tank strain (2,000+ units/mL, a 1,000-fold yield jump that produced 2.3 million D-Day doses) (0:34); 2) inked scale comparison showing 1 modern 500 mg penicillin tablet (~800,000 units) vs the ~2 million units needed to treat a single severe infection in 1941 (0:52); 3) inked dilution bar chart showing Fleming's 1929 mould broth killing Staphylococcus aureus at 1:800 dilution while leaving human white blood cells unharmed (2:28); 4) inked experimental outcome chart of the 25 May 1940 Oxford mouse trial (8 mice injected with 110 million Streptococcus pyogenes: 4 untreated controls 0/4 survived past 17 hours vs 4 penicillin-treated mice 4/4 survived) (4:18); 5) inked wartime production chart showing US penicillin output climbing from 21 billion units (1943) to 1,663 billion units (1944) and 6,800 billion units (1945) (6:00); 6) animated timeline building 3 Sep 1928 · Jun 1929 · 25 May 1940 · 12 Feb 1941 · Jul 1943 · 6 Jun 1944 · May 1945 alongside an inked beta-lactam cell-wall diagram showing a Staphylococcus bacterium at 20 atmospheres internal pressure bursting when penicillin blocks peptidoglycan cross-linking (6:43) | 3 or more per long, including the animated timeline |
| `SCALE` | **6** | 1) 2,000 litres of mould broth for a single patient — twenty full bathtubs of liquid just to make a few teaspoons of medicine (0:34); 2) one pill in your hand holds more penicillin than an entire Oxford laboratory could brew in months in 1940 (0:52); 3) 1 drop of mould broth in 800 drops of water — and it still stopped deadly Staphylococcus cold (2:28); 4) 110 million lethal bacteria injected into a mouse weighing less than an ounce — and every single treated mouse lived (4:18); 5) from barely enough powder on a fingernail to treat one Oxford policeman in 1941 to 6.8 trillion units a year by 1945 — enough for every Allied soldier on D-Day (6:00); 6) 20 atmospheres of pressure inside a bacterium — three times the pressure of a racing bicycle tyre, popped when penicillin unlocks its cell wall (6:43) | Every `DATA` number gets a `SCALE:` comparison (`grep -c "SCALE:"` ≥ `DATA:` count) |
| `WHO` | **11** | Alexander Fleming (0:34), Howard Florey (0:34), Ernst Chain (0:34), Norman Heatley (0:34), Merlin Pryce (1:28), Albert Alexander (4:58), Charles Fletcher (4:58), Andrew Moyer (5:30), Kenneth Raper (5:30), Mary Hunt (5:30), Dorothy Hodgkin (6:43) | First mention only, role right for the scene's year (4 words or fewer) |
| `WHEN` | **24** | London 3 September 1928 (0:00), Before 1941 (0:21), 3 September 1928 (0:34), May 1940 (0:34), July 1943 (0:34), August 1928 (1:28), London 3 September 1928 (1:28), 1922 (1:58), 7 March 1929 (1:58), June 1929 (1:58), 1931 (2:28), Oxford 1938 (3:08), 25 May 1940 (3:42), 26 May 1940 (3:42), 24 August 1940 (3:42), Oxford 12 February 1941 (4:58), 15 March 1941 (4:58), Peoria July 1941 (5:30), July 1943 (5:30), 6 June 1944 (5:30), 1945 (6:00), May 1945 (6:43), 1928–1945 (6:43), 11 December 1945 (7:18) | Every spoken date or era; later dates drop onto the timeline |
| `FACT` | **4** | Diluted 1 in 800, still lethal (1:58); Brewed in ceramic bedpans (3:42); Recycled from patient urine (4:58); Mouldy melon gave 1,000x yield (5:30) | 2–4 per long (4 words or fewer per card) |

## Craft checks (*Reference lessons* §1 + *Polish pass*)

- **First-minute timings:** Answer image by 0:03 (gloved hand lifting lid of unwashed Petri dish in London on 3 September 1928 as golden Staphylococcus colonies melt into a clear halo around blue-green Penicillium mould), title question by 0:07, promise by 0:15, stakes by 0:25, first concrete answer & real fact (Alexander Fleming on 3 September 1928, Florey/Chain/Heatley in May 1940, and the July 1943 Peoria cantaloupe 1,000-fold yield jump) by 0:34.
- **Explorer limits:** 2 beats total (`[EXPLORER ACTS: once. …]`), at 1:05 (Part 01, outside the first minute) and 6:00 (Part 04 comparing a tiny eyedropper vial against a towering Peoria fermentation tank and saluting the golden cantaloupe melon).
- **Chapter cold opens & cliffhanger questions:** Part 01 ends on why Fleming left deadly bacteria sitting unwashed for a month and why he walked away from penicillin before curing a single patient; Part 02 opens cold on Fleming's period quote (*"That's funny"*) on 3 September 1928 at St Mary's Hospital, contrasts his 1922 tear-drop lysozyme with 1:800 penicillin broth, and explains why he gave up by 1931, ending on who pulled his paper off the shelf on the eve of WWII and why they brewed medicine in hospital bedpans; Part 03 opens cold on Florey, Chain and Heatley at Oxford (1938–1940), Heatley's chilled extraction rig and ceramic bedpans, and the 25–26 May 1940 eight-mouse trial (4/4 treated survived, 0/4 controls), ending on what happened when they tried to treat a human weighing 3,000 times more than a mouse and ran out halfway through; Part 04 opens cold on the midpoint twist ("Case closed? Wrong." — Constable Albert Alexander's 12 February 1941 recovery, urine recycling, and tragic 15 March 1941 death when Britain's supply ran out, followed by spores in coat linings, Peoria corn steep liquor, and Mary Hunt's July 1943 mouldy cantaloupe strain brewing 2.3 million doses for D-Day), ending on how a melon mould bursts bacteria open without hurting human cells and what Fleming warned in 1945; Part 05 opens cold on the cold/flu & immune-booster misconception, explains Dorothy Hodgkin's May 1945 beta-lactam structure and 20-atmosphere bacterial lysis plus Fleming's 11 December 1945 Nobel warning, and hands off to Michael Faraday's 1821 mercury-cup electric motor (`021`).
- **Quirky anecdote before the hard idea:** Fleming dripping his own tears onto a dish in 1922 and stacking Petri dishes high enough in a Lysol tray that the top dish stayed dry on 3 September 1928; Heatley building an extraction rig from doorbell buzzers and milk churns and growing mould in ceramic hospital bedpans; Florey and Heatley smearing mould spores into their coat linings.
- **Misconception explained away:** "Many people think antibiotics work by boosting your immune system, or take them to fight a cold or flu" — explained via Dorothy Hodgkin's May 1945 beta-lactam ring jamming bacterial cell-wall cross-linking under 20 atmospheres of pressure while wall-less human cells and cell-less viruses are untouched (Part 05, 6:43).

## For Chief to decide

1. Lock **020 = Penicillin & Antibiotics: Alexander Fleming's Mouldy Dish & the Oxford Bedpan Factory (1928–1943)** and pick the 2-way Test & Compare working title pair:
   - **A (Subject + hook, §1 rule 11):** *Penicillin: The Mouldy Dish That Saved 200 Million Lives* (56 chars)
   - **B (Search question, §1 rule 2):** *How a Forgotten Petri Dish and a Mouldy Melon Changed Medicine* (62 chars)
   - **Alt (Search / twist question):** *Why Alexander Fleming Gave Up on the Mould That Saved the World* (63 chars)
2. Review `penicillin_script_master_v01.md` (93.4/100 PASS), then queue the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–8) before VO.

## Score (`npm run review:script`)

```text
# penicillin_script_master_v01.md

**Decision:** PASS · **Score:** 93.4 / 100

| Dimension | Score |
|---|---:|
| hook | 9.5 |
| curiosity | 9.5 |
| storytelling | 8 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 9.6 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1539 · Est. min: 10.3 · Chapters: 4

## Cold open excerpt

> How did a stray speck of blue-green mould on an unwashed glass dish — and a rotting cantaloupe melon from an Illinois grocery shop — save two hundred million human lives? By the end of this film, you'll see why the scientist who spotted that famous dish actually gave up on turnin

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 93.4/100 — proceed to VO after production checklist.

Pass threshold: 90
```
