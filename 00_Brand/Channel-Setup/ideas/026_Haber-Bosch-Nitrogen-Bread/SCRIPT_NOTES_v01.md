# 026 script v01: notes for review (J0462)

Script: `haber_script_master_v01.md` (with `opening_and_outline_v00.md`, `SOURCES_v00.md` and `SOURCES_v01.md`).

**Draft only (J0462, Gemini Argon, 17 Oct 2026).** Built from `026_Haber-Bosch-Nitrogen-Bread/opening_and_outline_v00.md` and the neighbour and search evidence in `IDEAS_2026-10-17_J0438.md` (`evidence_2026-10-17_J0438/n_haber.md` PASS — 5 education videos ≥ 1M views led by **Veritasium *The Man Who Killed Millions and Saved Billions (Clean Version)* (`QQkmJI63ykI`, 10.55M — exact Fritz Haber / Haber-Bosch discovery match)**, **TED-Ed ★ *Nature's smallest factory: The Calvin cycle* (3.39M)**, **Amoeba Sisters *Carbon and Nitrogen Cycles* (2.85M)**, and **CrashCourse *Nitrogen & Phosphorus Cycles: Always Recycle! Part 2* (1.94M)**, plus **TED-Ed ★ *The chemical reaction that feeds the world - Daniel D. Dulek* (840.9k in `public_search.md`)**, alongside `public_search.md` showing `"fritz haber ammonia"` autocompleting in GB search with 4 of the top 5 GB slots under 841k views). The topic isn't locked yet: Chief locks `026` and the working title pair first, then reviews/signs off this script and queues the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–5) before VO.

Structure (*Reference lessons* §1, scripts from 011 on): every chapter opens cold and ends on a question the next one answers; the midpoint twist ("Case closed? Wrong." — eleven months after Carl Bosch's first industrial ammonia factory opened at Oppau on 9 September 1913 to conquer the global famine warning, the August 1914 British naval blockade cut Germany off from Chilean nitrates and turned Haber-Bosch ammonia into nitric acid for wartime explosives, while Fritz Haber personally directed the first chlorine gas attack at Ypres on 22 April 1915, condemned by his wife Dr Clara Immerwahr before her suicide on 2 May 1915 and Haber's 1933 exile under Nazi racial laws) lands in Part 04; the popular misconception ("Many people assume traditional organic farming alone could easily feed all eight billion people on Earth today without synthetic nitrogen") is raised and explained away in Part 05 via Vaclav Smil and Jan Willem Erisman et al.'s (2008) global nitrogen-balance analyses showing Haber-Bosch ammonia feeds ~50% of humanity (~4 billion people) and supplies ~50% of the nitrogen atoms in our bodies; the ending hands off directly to `027` (*The First Computer & Breaking Enigma: Ada Lovelace's August 1843 Note G & Alan Turing's 1936 Universal Machine and 18 March 1940 Bombe*), with no goodbye and no subscribe ask. Five VO parts, matching 009–025.

## Marker count (v01)

Run on `haber_script_master_v01.md`: `grep -o "DATA:" … | wc -l`, and the same for each marker.

| Marker | Count | Where | Rule |
|---|---:|---|---|
| `DATA` | **5** | 1) inked reaction and population chart on period paper showing N₂ + 3H₂ → 2NH₃ at 200 atmospheres and 500°C and the share of humanity fed by synthetic Haber-Bosch nitrogen fertilizer (~50% of global food protein = ~4 billion people alive today) (0:34); 2) inked pressure scale comparing 1 atmosphere (sea-level air) vs 200 atmospheres inside Haber and Bosch's 500°C ammonia reactor (0:52); 3) inked bond-energy & equilibrium chart on period paper comparing the N≡N triple bond (945 kJ/mol, nearly triple a C–C single bond at 348 kJ/mol) and ammonia yield at 500°C jumping from ~0.13% at 1 atm to ~15–20% per pass at 200 atm with continuous recirculation (1:58); 4) inked cross-section diagram on period paper of Carl Bosch's double-walled reactor: 200 atm / 500°C N₂ + H₂ core → thin carbon-free soft-iron inner liner → perforated strong carbon-steel outer shell drilled with "Bosch holes" venting diffusing H₂ safely before methane blistering can occur (3:42); 5) animated timeline building Sep 1898 · 2 Jul 1909 · 9 Sep 1913 · 1914–1918 · 1931 · 2008–Today alongside an inked global nitrogen balance chart showing ~1–2% of world energy producing ~150–180 million tonnes of ammonia/year, feeding ~50% of humanity (~4 billion people) (6:43) | 3 or more per long, including the animated timeline |
| `SCALE` | **5** | 1) half of all the nitrogen atoms inside your muscles and DNA right now came out of a high-pressure Haber-Bosch tube (0:34); 2) 200 atmospheres of pressure at 500 degrees Celsius — like squeezing red-hot gas under the weight of two kilometres of ocean water (0:52); 3) 945 kilojoules per mole — a molecular lock nearly three times stronger than the carbon bonds holding wood or diamond together (1:58); 4) hydrogen atoms are so small they slip straight between the iron atoms of solid red-hot cannon steel and rot it from within — until Bosch drilled tiny escape holes in the outer armour (3:42); 5) 1 to 2 percent of all the energy humanity uses on Earth goes into one single chemical reaction — putting half the nitrogen atoms into your body (6:43) | Every `DATA` number gets a `SCALE:` comparison (`grep -c "SCALE:"` ≥ `DATA:` count) |
| `WHO` | **7** | William Crookes (0:21), Fritz Haber (0:34), Robert Le Rossignol (0:34), Carl Bosch (0:34), Walther Nernst (2:28), Alwin Mittasch (2:28), Clara Immerwahr (5:30) | First mention only, role right for the scene's year (4 words or fewer) |
| `WHEN` | **21** | Karlsruhe 2 July 1909 (0:00), Bristol September 1898 (0:21), 2 July 1909 (0:34), September 1913 (0:34), September 1898 (1:28), 1907 (2:28), 2 July 1909 (2:28), Ludwigshafen 1909–1910 (3:08), Oppau 9 September 1913 (4:18), 1918 (4:18), 1931 (4:18), August 1914 (4:58), Ypres 22 April 1915 (4:58), December 1900 (5:30), 2 May 1915 (5:30), April 1933 (6:05), Basel 29 January 1934 (6:05), 2008 (6:43), 1898–2008 (6:43), August 1843 (7:45), 18 March 1940 (7:45) | Every spoken date or era; later dates drop onto the timeline |
| `FACT` | **4** | 78% of air, yet unusable (1:28); 20,000 catalyst tests (3:08); First female PhD at Breslau (5:30); Uses 1–2% of world energy (6:43) | 2–4 per long (4 words or fewer per card) |

## Craft checks (*Reference lessons* §1 + *Polish pass*)

- **First-minute timings:** Answer image by 0:03 (Fritz Haber and Robert Le Rossignol in Karlsruhe on 2 July 1909 watching clear drops of liquid ammonia condense from a 200-atmosphere, 500°C tube and morph into golden fields of wheat), title question by 0:07, promise by 0:15, stakes by 0:25, first concrete answer & real fact (Haber and Le Rossignol squeezing nitrogen and hydrogen at 200 atmospheres and 500°C over an osmium catalyst on 2 July 1909 and Carl Bosch scaling it by September 1913 to feed half of humanity) by 0:34.
- **Explorer limits:** 2 beats total (`[EXPLORER ACTS: once. …]`), at 1:05 (Part 01, outside the first minute) and 6:05 (Part 04 pouring white nitrogen crystals into a balance scale between a wheat sheaf and an artillery shell).
- **Chapter cold opens & cliffhanger questions:** Part 01 ends on why crops were starving in an atmosphere of 78% nitrogen and how Carl Bosch stopped hot hydrogen from eating solid steel reactors from the inside out; Part 02 opens cold on the 945 kJ/mol triple-bond lock, Sir William Crookes's September 1898 Bristol famine warning, Walther Nernst's 1907 challenge, and Haber & Le Rossignol's 2 July 1909 Karlsruhe demonstration condensing 80 mL/hour of ammonia over scarce osmium, ending on how Bosch could scale a fragile tabletop tube when 200 atmospheres of hot hydrogen started blowing solid steel walls apart; Part 03 opens cold on Alwin Mittasch's 20,000 catalyst tests discovering promoted magnetite iron and Bosch's discovery of hydrogen embrittlement / methane blistering, solved by his soft-iron liner and perforated outer steel shell ("Bosch holes") at Oppau on 9 September 1913, ending on why the outbreak of war 11 months later turned their life-saving machine into a heartbreak that tore Haber's family apart; Part 04 opens cold on the midpoint twist ("Case closed? Wrong." — the August 1914 blockade, Haber-Bosch ammonia converted into nitric acid munitions, Haber's 22 April 1915 Ypres chlorine attack, Dr Clara Immerwahr's condemnation and 2 May 1915 death, and Haber's April 1933 resignation and 29 January 1934 death in Basel), ending on why half the nitrogen atoms in your body come from a Haber-Bosch factory and how soil bacteria pull off the same trick at room temperature; Part 05 opens cold on the organic-farming misconception, explains Smil and Erisman et al.'s (2008) 50%-of-humanity nitrogen balance and nature's iron-molybdenum nitrogenase enzyme, and hands off to Ada Lovelace's August 1843 Note G and Alan Turing's 1936 Universal Machine and 18 March 1940 Bombe (`027`).
- **Quirky anecdote before the hard idea:** World supply of osmium weighing barely 100 kilograms; thick Krupp cannon-steel tubes blistering like rotten wood from microscopic hydrogen atoms turning carbon into methane gas inside the solid metal wall.
- **Rivalry / tension:** Back-and-forth portrait cuts between Walther Nernst challenging Haber's low-pressure yields in 1907 and Haber & Le Rossignol's 200-atmosphere demonstration (2:28), plus Clara Immerwahr confronting Haber in 1915 (5:30).
- **Misconception explained away:** "Many people assume traditional organic farming alone could easily feed all eight billion people on Earth today without synthetic nitrogen" — explained via global nitrogen-balance data showing Haber-Bosch ammonia sustains ~50% of humanity (~4 billion people) and provides half the nitrogen atoms in our tissues (Part 05, 6:43).

## For Chief to decide

1. Lock **026 = Turning Thin Air Into Bread: Fritz Haber's Tabletop Ammonia Drop & Carl Bosch's Bursting Steel Reactors (1909–1913)** and pick the 2-way Test & Compare working title pair:
   - **A (Subject + hook, §1 rule 11):** *The Haber-Bosch Process: How Thin Air Feeds Half the World* (58 chars)
   - **B (Search question, §1 rule 2):** *How Turning Thin Air Into Bread Saved Four Billion Lives* (56 chars)
   - **Alt (Search / twist question):** *Why Half the Nitrogen in Your Body Came From a Steel Tube* (57 chars)
2. Review `haber_script_master_v01.md` (92.6/100 PASS), then queue the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–5) before VO.

## Score (`npm run review:script`)

```text
# haber_script_master_v01.md

**Decision:** PASS · **Score:** 92.6 / 100

| Dimension | Score |
|---|---:|
| hook | 9.5 |
| curiosity | 8.7 |
| storytelling | 9 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 8.6 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1503 · Est. min: 10 · Chapters: 4

## Cold open excerpt

> How did squeezing thin air inside a hot metal tube on a German lab bench — until clear liquid dripped from a tap — let four billion people survive global starvation? By the end of this film, you'll see why humanity stood in deadly danger of global famine even though you feel an o

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 92.6/100 — proceed to VO after production checklist.

Pass threshold: 90
```
