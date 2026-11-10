# 064 script v01: notes for review (J0645)

Script: `viruses_script_master_v01.md` (with `opening_and_outline_v00.md`, `SOURCES_v00.md` and `SOURCES_v01.md`).

**Draft only (J0645, Gemini Argon, 19 Oct 2026).** Built from `064_Ivanovsky-Beijerinck-Stanley-Hershey-Viruses/opening_and_outline_v00.md` and the neighbour and search evidence in `IDEAS_2026-10-19_J0637.md` (`evidence_2026-10-19_J0637/n_viruses_bacteriophage.md` PASS — 11 education videos ≥ 1M views, ALL 11 strictly on viruses & bacteriophages: **Kurzgesagt – In a Nutshell *The Deadliest Being on Planet Earth – The Bacteriophage* (`YI3tsmFsrOg`, 35.25M — exact bacteriophage match!)**, **Kurzgesagt *This Virus Shouldn't Exist (But it Does)* (`1-NxodiGPCU`, 23.92M)**, **TED-Ed ★ *Cell vs. virus: A battle for health - Shannon Stiles* (`oqGuJhOeMek`, 13.21M — exact subject match!)**, **TED-Ed ★ *How we conquered the deadly smallpox virus - Simona Zompi* (`yqUFy-t4MlQ`, 9.16M)**, **Kurzgesagt *Why Scientists Are Puzzled By This Virus* (`SbvAaDN1bpE`, 5.66M)**, **TED-Ed ★ *How does your immune system work? - Emma Bryce* (`PSRJfaAYkW4`, 5.20M)**, **TED-Ed ★ *How do viruses jump from animals to humans? - Ben Longdon* (`xjcsrU-ZmgY`, 1.63M — exact virus match!)**, and **TED-Ed ★ *What happens if an engineered virus escapes the lab?* (`WJ-XXQCcXik`, 1.57M)**, alongside `public_search.md` & `public_search_titles.md` showing `"how do viruses work"` triggering exact YouTube autocomplete, all 5 top GB search results for `"dmitri ivanovsky martinus beijerinck wendell stanley virus"` under 14k views, and 4 of the top 5 GB slots for *How Filtered Tobacco Juice Revealed Viruses Aren't Even Alive* under 17k views). The topic isn't locked yet: Chief locks `064` and the working title pair first, then reviews/signs off this script and queues the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

Structure (*Reference lessons* §1, scripts from 011 on): every chapter opens cold and ends on a question the next one answers; the midpoint twist ("Case closed — anything that multiplies inside a living plant or animal must be a living cell! Wrong! You can crystallise a virus into dry white needles in a jar like table salt, store it on a shelf for years, and watch it explode back to life the instant it touches a cell!" — where Wendell Stanley on 28 June 1935 in *Science* crystallised Tobacco Mosaic Virus into pure needles, proven by Bawden & Pirie on 19 December 1936 to be 95% protein and 5% RNA and photographed by Helmut Ruska in 1938–1939) lands in Part 03; Alfred Hershey and Martha Chase's 20 September 1952 radioactive `³⁵S`/`³²P` Waring kitchen blender experiment proving that viruses inject genetic code (`DNA`) while leaving their protein shells outside lands in Part 04; the "antibiotics for a viral cold" misconception ("Every winter, millions of people ask for antibiotics like penicillin to treat a viral cold or flu") is raised and explained away in Part 05 via viruses lacking cell walls, ribosomes, or independent metabolism (`plus Baltimore & Temin's June 1970 retroviral reverse transcriptase`); the ending hands off directly to `065` (*How Does Your Immune System Recognise a Billion Invaders It Has Never Seen Before (`Phagocytes, Antibodies, Clonal Selection & V(D)J Recombination`)? Élie Metchnikoff's December 1882 Rose-Thorn Starfish Larva (`Phagocytes`), Emil von Behring & Shibasaburo Kitasato's 4 December 1890 Diphtheria Antitoxin (`Antibodies`), Frank Macfarlane Burnet's 1957 Clonal Selection Theory, and Susumu Tonegawa's October 1976 Genetic Slot-Machine Proof (`V(D)J Recombination`)*), with no goodbye and no subscribe ask. Five VO parts, matching 009–063.

## Marker count (v01)

Run on `viruses_script_master_v01.md`: `grep -o "DATA:" … | wc -l`, and the same for each marker.

| Marker | Count | Where | Rule |
|---|---:|---|---|
| `DATA` | **6** | 1) inked microbial filtration & Hershey-Chase blender chart on period paper comparing human red blood cell (8,000 nm), E. coli bacterium (2,000 nm), Chamberland porcelain filter pore (100–200 nm), TMV rod (300 × 18 nm, 95% protein : 5% RNA), and rhinovirus (30 nm), plus Hershey-Chase 35S protein (80% extracellular) vs 32P DNA (intracellular injection) (0:34); 2) inked Tobacco Mosaic Virus (TMV) architecture diagram showing a 300 nm × 18 nm hollow helical rod built from 2,130 identical coat-protein subunits (95% by mass) wrapped around a single 6,395-nucleotide strand of RNA (5% by mass) (0:52); 3) inked Ivanovsky (1892) & Beijerinck (1898) serial-dilution vs chemical toxin chart on period paper showing a chemical toxin's potency dropping to zero across 10-fold serial dilutions while Beijerinck's porcelain-filtered Tobacco Mosaic Virus ("contagium vivum fluidum") amplifies exponentially back to 100% infectious titre inside each living host leaf (1:58); 4) inked Stanley (28 June 1935, Science 81: 644–645), Bawden & Pirie (19 December 1936, Nature 138: 1051–1052), and Ruska & Kausche (May 1939, Naturwissenschaften 27: 292–299) TMV composition & electron-microscope resolution chart on period paper showing visible-light microscopy limit (~200 nm) vs electron-microscope imaging of 300 × 18 nm TMV rods (95% protein coat + 5% RNA core, infectious at 10^-9 g/mL) (3:42); 5) inked Hershey & Chase Waring blender experiment chart on period paper (from Hershey & Chase, 20 September 1952, J. Gen. Physiol. 36: 39–56) plotting blender agitation time (0 to 8 minutes) vs extracellular 35S protein coat sheared into the supernatant (~80%) while ~70–85% of 32P viral DNA remains inside the infected E. coli pellet to direct progeny phage assembly (5:28); 6) animated timeline building 12 Feb 1892 & 1898 · 1915–1917 · 28 June 1935 & Dec 1936 · 20 Sep 1952 (6:43) | 3 or more per long, including the animated timeline |
| `SCALE` | **6** | 1) if a single E. coli bacterium were the size of a double-decker bus, a cold virus beside it would be no bigger than a football — easily slipping straight through a bacterium-proof porcelain filter (0:34); 2) a tobacco mosaic virus is just one strand of genetic instructions wrapped in 2,130 identical protein bricks — so uniform that billions of them stack together in a jar like salt crystals (0:52); 3) if you drop a pinch of poison into a lake, it dilutes until it is harmless — yet one microscopic drop of Beijerinck's filtered liquid turned an entire field of healthy plants into factories making millions of new copies (1:58); 4) a tobacco mosaic virus is ten times smaller than the wavelength of green light, making it physically invisible to any optical microscope on Earth until Helmut Ruska used a beam of electrons to photograph it in 1939 (3:42); 5) the Hershey-Chase blender experiment proved that a virus protein coat is nothing more than a disposable delivery van — it parks on the outside of your cell wall, injects its DNA or RNA instructions inside, and gets left behind (5:28); 6) from crushed tobacco leaves in Russia to sparkling crystals in New Jersey and a kitchen blender in New York, sixty years of detective work revealed the non-living genetic pirates that shaped all life on Earth (6:43) | Every `DATA` number gets a `SCALE:` comparison (`grep -c "SCALE:"` ≥ `DATA:` count) |
| `WHO` | **9** | Dmitri Ivanovsky (0:34), Martinus Beijerinck (0:34), Wendell M. Stanley (0:34), Frederick C. Bawden (0:34), Norman W. Pirie (0:34), Alfred D. Hershey (0:34), Martha Chase (0:34), Félix d'Hérelle (1:28), Helmut Ruska (3:08) | First mention only, role right for the scene's year (4 words or fewer) |
| `WHEN` | **22** | St. Petersburg, 12 February 1892 (0:00), 12 February 1892 (0:34), 1898 (0:34), 28 June 1935 (0:34), 19 December 1936 (0:34), 20 September 1952 (0:34), 1884 (1:28), 12 February 1892 (1:28), 1898 (1:28), 4 December 1915 (1:28), 3 September 1917 (1:28), 28 June 1935 (3:08), 19 December 1936 (3:08), 1938 (3:08), 1939 (3:08), 20 September 1952 (4:53), 1892–1952 (6:43), June 1970 (7:18), December 1882 (7:45), 4 December 1890 (7:45), October 1957 (7:45), October 1976 (7:45) | Every spoken date or era; later dates drop onto the timeline |
| `FACT` | **3** | Multiplied after passing through porcelain (1:28); Crystallised in a jar like salt (3:08); Protein stays outside; DNA goes in (4:53) | 2–4 per long (4 words or fewer per card) |

## Craft checks (*Reference lessons* §1 + *Polish pass*)

- **First-minute timings:** Answer image by 0:03 (sparkling white needle crystals of Tobacco Mosaic Virus dissolving on a leaf, zooming in 100,000× to show lunar-lander bacteriophages injecting glowing golden DNA into a bacterium while a Waring blender spins behind them), title question by 0:07, promise by 0:15, stakes by 0:25, first concrete answer & real fact (Ivanovsky's 12 February 1892 and Beijerinck's 1898 porcelain filter, Stanley's 28 June 1935 virus crystals, Bawden & Pirie's December 1936 RNA proof, and Hershey & Chase's 20 September 1952 Waring blender proof) by 0:34.
- **Explorer limits:** 2 beats total (`[EXPLORER ACTS: once. …]`), at 1:05 (Part 01, outside the first minute) and 6:05 (Part 04 holding a Geiger counter up to the centrifuge tube's `35S` protein supernatant and `32P` DNA bacterial pellet).
- **Chapter cold opens & cliffhanger questions:** Part 01 ends on what happened on 12 February 1892 when Dmitri Ivanovsky poured diseased tobacco sap through a filter that trapped every known germ on Earth; Part 02 opens cold on Charles Chamberland's 1884 porcelain water filter, tells the story of Ivanovsky (12 February 1892), Martinus Beijerinck's 1898 serial-dilution proof of *contagium vivum fluidum* (`virus`), and Twort & d'Hérelle's 1915–1917 discovery of `bacteriophages`, and ends on what happened on 28 June 1935 when Wendell Stanley boiled down a ton of infected tobacco plants; Part 03 opens cold on the midpoint twist ("Case closed — anything that multiplies inside a living plant or animal must be a living cell! Wrong!"), tells the story of Wendell Stanley's 28 June 1935 crystallization of Tobacco Mosaic Virus, Bawden & Pirie's 19 December 1936 `95% protein + 5% RNA` discovery, and Helmut Ruska's 1938–1939 electron-microscope photographs, and ends on how a kitchen blender in 1952 settled whether protein or DNA enters the cell; Part 04 opens cold on how to track which half of a 200-nm virus enters a bacterium, explains Alfred Hershey and Martha Chase's 20 September 1952 `³⁵S`/`³²P` Waring blender experiment (`1969 Nobel Prize`), and ends on why viruses haven't wiped out every human on Earth; Part 05 opens cold on why antibiotics never cure a viral cold, and hands off to Élie Metchnikoff (December 1882 phagocytes), Behring & Kitasato (4 December 1890 antibodies), Frank Macfarlane Burnet (October 1957 Clonal Selection), and Susumu Tonegawa's October 1976 `V(D)J recombination` (`065`).
- **Quirky anecdote before the hard idea:** Wendell Stanley grinding up a literal ton of tobacco leaves in Princeton to pull out sparkling salt-like crystals that still infected plants at 1 part per billion; Alfred Hershey and Martha Chase using a Waring milkshake blender to shear viruses off bacteria!
- **Rivalry / tension:** Cellular-germ dogma vs Beijerinck's "contagious living fluid"; Stanley's "100% pure protein" claim vs Bawden & Pirie's `5% RNA` proof; protein-as-genes vs DNA-as-genes settled by the Hershey-Chase blender.
- **Misconception explained away:** "Why don't antibiotics cure a viral cold or flu?" — explained via viruses having no cell walls, no ribosomes, and hiding inside host cells (Part 05, 6:43).

## For Chief to decide

1. Lock **064 = How Did Filtered Tobacco Juice & a Kitchen Blender Reveal That Viruses Aren't Even Alive (`Viruses, Crystallization & the Hershey-Chase Blender`)? Dmitri Ivanovsky's 12 February 1892 Porcelain Filter, Martinus Beijerinck's 1898 "Contagious Living Fluid" (`Virus`), Wendell Stanley's 28 June 1935 Tobacco Mosaic Virus Crystals, and Alfred Hershey & Martha Chase's 20 September 1952 Waring Blender Experiment (1892–1952)** and pick the 2-way Test & Compare working title pair:
   - **A (Subject + hook, §1 rule 11):** *Viruses: The Living Crystals That Hijack Your Cells* (51 chars)
   - **B (Search question, §1 rule 2):** *How Filtered Tobacco Juice Revealed Viruses Aren't Even Alive* (61 chars)
   - **Alt (Search / twist question):** *How a Kitchen Blender Proved How Viruses Hijack Living Cells* (60 chars)
2. Review `viruses_script_master_v01.md` (92.7/100 PASS), then queue the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

## Score (`npm run review:script`)

```text
# viruses_script_master_v01.md

**Decision:** PASS · **Score:** 92.7 / 100

| Dimension | Score |
|---|---:|
| hook | 9.5 |
| curiosity | 9.1 |
| storytelling | 9.5 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 7.8 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1409 · Est. min: 9.4 · Chapters: 4

## Cold open excerpt

> How can a deadly disease agent be crystallised in a glass jar like table salt for years — yet spring back to life on a green leaf? And how did filtered tobacco juice in eighteen ninety-two that could cross a bacteria-proof porcelain filter and a Waring kitchen blender in nineteen

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 92.7/100 — proceed to VO after production checklist.

Pass threshold: 90
```
