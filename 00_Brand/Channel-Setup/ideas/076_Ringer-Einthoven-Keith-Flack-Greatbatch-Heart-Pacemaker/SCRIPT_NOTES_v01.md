# 076 script v01: notes for review (J0705)

Script: `heart_script_master_v01.md` (with `opening_and_outline_v00.md`, `SOURCES_v00.md` and `SOURCES_v01.md`).

**Draft only (J0705, Gemini Argon, 20 Oct 2026).** Built from `076_Ringer-Einthoven-Keith-Flack-Greatbatch-Heart-Pacemaker/opening_and_outline_v00.md` and the neighbour and search evidence in `IDEAS_2026-10-20_J0697.md` (`evidence_2026-10-20_J0697/n_heart_pacemaker.md` PASS — 8 education videos ≥ 1M views, ALL 8 strictly on the heart, cardiac conduction & circulatory system: **TED-Ed ★ *How blood pressure works - Wilfred Manzano* (`Ab9OZsDECZw`, 17.98M)**, **TED-Ed ★ *What happens during a heart attack? - Krishna Sudhir* (`3_PYnWVoUzM`, 9.15M)**, **CrashCourse *The Heart, Part 1 - Under Pressure: Crash Course Anatomy & Physiology #25* (`X9ZZ6tcxArI`, 8.13M — exact subject match!)**, **Amoeba Sisters *Circulatory System and Pathway of Blood Through the Heart* (`_vZ0lefPg_0`, 7.50M)**, **TED-Ed ★ *How does heart transplant surgery work? - Roni Shanoada* (`o1z2DfFZBS4`, 4.56M)**, **TED-Ed ★ *How the heart actually pumps blood - Edmond Hui* (`ruM4Xxhx32U`, 4.47M — exact SA node & cardiac cycle match!)**, **CrashCourse *The Heart, Part 2 - Heart Throbs: Crash Course Anatomy & Physiology #26* (`FLBMwcvOaEo`, 3.31M — exact pacemaker conduction & ECG match!)**, and **Khan Academy *Circulatory system and the heart* (`QhiVnFvshZg`, 1.33M)**, plus **Cognito (`608.4k`)** and **Amoeba Sisters *Conduction System of the Heart* (`bzZdJn7elaU`, 235.8k)**, alongside `public_search.md` & `public_search_titles.md` showing `"how does a pacemaker work"` is an exact YouTube autocomplete match (`yes`), all 5 top GB search results for `"sidney ringer willem einthoven wilson greatbatch pacemaker"` under 11k views, and 0 videos on YouTube matching *How a 600-Pound Machine and One Wrong Resistor Saved the Heart*). The topic isn't locked yet: Chief locks `076` and the working title pair first, then reviews/signs off this script and queues the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

Structure (*Reference lessons* §1, scripts from 011 on): every chapter opens cold and ends on a question the next one answers; the midpoint twist ("Case closed — the man who recorded the first human electrocardiogram in May eighteen eighty-seven, Augustus Waller, knew it would transform every hospital on Earth! Wrong! Even after demonstrating the heartbeat of his pet bulldog 'Jimmy' standing in jars of salt water, Waller himself declared in nineteen eleven: 'I do not imagine that electrocardiography is likely to find any very extensive use in the hospital'!" — where Willem Einthoven in 1901–1903 built a 600-pound string galvanometer with a `2.5 µm` silvered quartz thread to record the `P–Q–R–S–T` electrocardiogram) lands in Part 03; Wilson Greatbatch's 1956–7 May 1958 accidental `1 MΩ` wrong-resistor blocking-oscillator implantable pacemaker (`with surgeon William Chardack, implanted in human patient Frank Henefelt on 6 June 1960`) lands in Part 04; the ending hands off directly to `077` (*How Does Your Digestive System Turn Food Into Fuel — and How Did a Pet Buzzard, a Washed Liver & Pavlov's Dogs Unlock Digestion and Homeostasis?*), with no goodbye and no subscribe ask. Five VO parts, matching 009–075.

## Marker count (v01)

Run on `heart_script_master_v01.md`: `grep -o "DATA:" … | wc -l`, and the same for each marker.

| Marker | Count | Where | Rule |
|---|---:|---|---|
| `DATA` | **6** | 1) inked cardiac electrical conduction & Einthoven P-Q-R-S-T electrocardiogram chart on period paper showing SA node pacemaker firing (60–100 bpm = 100,000 beats/day), AV node 100 ms delay, His-Purkinje ventricular sweep, skin voltage (~1 millivolt read by a 2.5 µm silvered quartz string in a 270 kg electromagnet), and Greatbatch's 1 MΩ / 1.8 ms implantable pacemaker pulse (0:34); 2) inked Willem Einthoven (1903 Pflügers Arch. 99: 472–480) string galvanometer specification & P-Q-R-S-T wave chart comparing Augustus Waller's sluggish 1887 capillary electrometer (A-B-C-D) against Einthoven's 2.5 µm quartz string galvanometer (P-Q-R-S-T) (0:52); 3) inked Sidney Ringer (1883 J. Physiol. 4: 29–42) frog-heart contraction trace alongside Keith & Flack (April 1907 J. Anat. Physiol. 41: 172–189) and Tawara (1906) SA node → AV node → Bundle of His → Purkinje conduction timing map on period paper (1:58); 4) inked Willem Einthoven (1903 Pflügers Arch. 99: 472–480 & 1906 Arch. Int. Physiol. 4: 132–164) string galvanometer P-Q-R-S-T electrocardiogram vs Waller's 1887 capillary trace & 1.5 km Leiden hospital-to-lab telecardiogram schematic on period paper (3:47); 5) inked Wilson Greatbatch (1956–7 May 1958 / October 1960 Surgery 48: 643–654 & US Patent 3,057,356) blocking-oscillator implantable pacemaker circuit schematic on period paper (5:32); 6) animated timeline building 1882–1883 & 1906 · 1901–1903 · 1956 – 7 May 1958 & 1960 (6:48) | 3 or more per long, including the animated timeline |
| `SCALE` | **6** | 1) the electrical signal that reaches your skin from your beating heart is just one millivolt — three thousand times weaker than a single AA torch battery — yet Willem Einthoven read it by watching the shadow of a quartz thread four times thinner than a red blood cell (0:34); 2) Einthoven's first ECG machine weighed as much as a grand piano, took five people to run, and needed underground telephone wires to carry heartbeats a mile from the hospital — today that same P-Q-R-S-T wave sits on a smartwatch on your wrist (0:52); 3) your heart's natural pacemaker — the sinoatrial node discovered by Keith and Flack — is smaller than a flattened grain of rice, yet that tiny speck of tissue fires three billion electrical sparks over your lifetime without a single wire from your brain (1:58); 4) Augustus Waller thought the ECG was a useless party trick for his pet bulldog — yet by stretching a quartz thread thinner than a cobweb inside a 600-pound magnet, Willem Einthoven built the lifeline that reads every heart attack on Earth (3:47); 5) misreading a single green stripe for an orange stripe on a resistor the size of a grain of wheat increased the resistance one hundred times — turning a sound recorder into a two-cubic-inch artificial SA node that now keeps over three million human hearts beating (5:32); 6) from a London tap-water mistake and a 600-pound magnet in Leiden to a single wrong resistor in a Buffalo barn, scientists learned to read and restart the electrical spark of life (6:48) | Every `DATA` number gets a `SCALE:` comparison (`grep -c "SCALE:"` ≥ `DATA:` count) |
| `WHO` | **8** | Sidney Ringer (0:34), Willem Einthoven (0:34), Arthur Keith (0:34), Martin William Flack (0:34), Wilson Greatbatch (0:34), Sunao Tawara (1:28), Augustus Desiré Waller (3:13), William M. Chardack (4:58) | First mention only, role right for the scene's year (4 words or fewer) |
| `WHEN` | **33** | Buffalo, 7 May 1958 (0:00), 1882 (0:34), 1883 (0:34), 1901 (0:34), 1903 (0:34), 1906 (0:34), 1956 (0:34), 7 May 1958 (0:34), 1839 (1:28), 1882 (1:28), 1883 (1:28), 1893 (1:28), 1906 (1:28), April 1907 (1:28), May 1887 (3:13), 1895 (3:13), 1901 (3:13), 1903 (3:13), 1906 (3:13), 1911 (3:13), 1924 (3:13), 1952 (4:58), 1956 (4:58), 31 October 1957 (4:58), 7 May 1958 (4:58), 6 June 1960 (4:58), 1970 (4:58), 1882–1970 (6:48), 1752 (7:45), 1780 (7:45), 1848 (7:45), 1855 (7:45), 1897 (7:45) | Every spoken date or era; later dates drop onto the timeline |
| `FACT` | **3** | London tap water unlocked the heart (1:28); 600-pound ECG took 5 people (3:13); 1 MΩ wrong resistor (4:58) | 2–4 per long (4 words or fewer per card) |

## Craft checks (*Reference lessons* §1 + *Polish pass*)

- **First-minute timings:** Answer image by 0:03 (human heart beating as a golden electrical wave flashes from the SA node to the AV node, Bundle of His, and Purkinje fibres to trace a P–Q–R–S–T wave beside Greatbatch's two-cubic-inch pacemaker), title question by 0:07, promise by 0:15, stakes by 0:25, first concrete answer & real fact (Ringer's 1882–1883 calcium ion discovery, Einthoven's 1901–1903 string galvanometer ECG, Keith & Flack's 1906 `SA node`, and Greatbatch's 1956–1958 wrong-resistor implantable pacemaker) by 0:34.
- **Explorer limits:** 2 beats total (`[EXPLORER ACTS: once. …]`), at 1:05 (Part 01, outside the first minute) and 6:08 (Part 04 swapping a `10,000-ohm` orange-stripe resistor for a `1,000,000-ohm` green-stripe resistor to turn a continuous buzz into a steady 1-beat-per-second pulse).
- **Chapter cold opens & cliffhanger questions:** Part 01 ends on why Sidney Ringer's frog hearts kept beating in 1882 only when his technician broke the rules and how a Kent farmhouse microscope in 1906 found the tiny patch of cells that sparks every heartbeat; Part 02 opens cold on Sidney Ringer's 1882–1883 London pipe-water discovery of calcium-driven heartbeats and Keith & Flack's 1906 discovery of the `sinoatrial (SA) node`, and ends on why Augustus Waller stood his pet bulldog "Jimmy" in jars of salt water in May 1887 yet called his own invention useless; Part 03 opens cold on the midpoint twist ("Case closed — the man who recorded the first human electrocardiogram in May eighteen eighty-seven, Augustus Waller, knew it would transform every hospital on Earth! Wrong!"), tells the story of Willem Einthoven's 1901–1903 600-pound quartz-filament string galvanometer and 1906 telecardiogram, and ends on how engineer Wilson Greatbatch in 1956 grabbed a resistor 100 times too big by mistake and put a permanent pacemaker inside the human chest; Part 04 opens cold on Greatbatch reaching into his Buffalo workshop box for a brown-black-orange resistor and pulling out a brown-black-green `1 MΩ` resistor, explains the 7 May 1958 dog trial and 6 June 1960 human implant with surgeon William Chardack, and ends on how a pet buzzard in 1752, a washed dead liver in 1855, and Ivan Pavlov's dogs in 1897 unlocked digestion and `homeostasis`; Part 05 opens cold on 3 million pacemakers and wristwatches tracing Einthoven's `P–Q–R–S–T` wave today, and hands off to René-Antoine de Réaumur (1752), Lazzaro Spallanzani (1780), Claude Bernard (1848–1857), and Ivan Pavlov (1897) (`077`).
- **Quirky anecdote before the hard idea:** Sidney Ringer's technician secretly using London kitchen tap water instead of distilled water; Augustus Waller demonstrating the ECG with his pet bulldog "Jimmy" standing in salt-water jars; Willem Einthoven shooting molten quartz arrows across his room; Wilson Greatbatch misreading the third colour stripe on a resistor!
- **Rivalry / tension:** Augustus Waller dismissing the clinical usefulness of the ECG (`1911`) vs Willem Einthoven's 600-pound string galvanometer; external tethered pacemakers (`Zoll, Bakken`) vs Greatbatch & Chardack's sealed implantable epoxy pacemaker.
- **Misconception explained away:** "Does your brain have to tell your heart to beat every second?" — refuted by Keith & Flack's `sinoatrial node` (`autorhythmic pacemaker`) and Sidney Ringer's ionic solution keeping an isolated heart beating outside the body with zero brain connections (Part 02).

## For Chief to decide

1. Lock **076 = Why Does Your Heart Beat 100,000 Times a Day (Even Outside Your Body) — and How Did a 600-Pound Salt-Bucket Machine & One Wrong Resistor Invent the ECG and Implantable Pacemaker (`The Heart's Electrical Conduction System, Willem Einthoven's 1901 Electrocardiogram & Wilson Greatbatch's 1958 Pacemaker`)? Sidney Ringer's 1882 Tap-Water Calcium Heartbeat Discovery, Arthur Keith & Martin Flack's 1906 `Sinoatrial Node` Pacemaker, Willem Einthoven's 1901–1903 `String Galvanometer` (`ECG`), and Wilson Greatbatch's 1956–7 May 1958 Accidental Wrong-Resistor Implantable Pacemaker (1882–1970)** and pick the 2-way Test & Compare working title pair:
   - **A (Subject + hook, §1 rule 11):** *The Pacemaker: One Wrong Resistor Saved Millions* (48 chars)
   - **B (Search question, §1 rule 2):** *How a 600-Pound Machine and One Wrong Resistor Saved the Heart* (62 chars)
   - **Alt (Search / twist question):** *Why Your Heart Beats 100,000 Times a Day Even Outside Your Body* (63 chars)
2. Review `heart_script_master_v01.md` (90.8/100 PASS), then queue the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

## Score (`npm run review:script`)

```text
# heart_script_master_v01.md

**Decision:** PASS · **Score:** 90.8 / 100

| Dimension | Score |
|---|---:|
| hook | 9.5 |
| curiosity | 9.1 |
| storytelling | 8 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 7.4 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1709 · Est. min: 11.4 · Chapters: 4

## Cold open excerpt

> Why does your heart beat one hundred thousand times every single day — even if a surgeon lifts it completely out of your chest and places it in a dish of warm salt water ? How did a lazy technician's London tap-water mistake in eighteen eighty-two , a six-hundred-pound electromag

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 90.8/100 — proceed to VO after production checklist.

Pass threshold: 90
```
