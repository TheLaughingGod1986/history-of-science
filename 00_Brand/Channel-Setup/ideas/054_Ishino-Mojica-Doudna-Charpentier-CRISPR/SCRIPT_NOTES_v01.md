# 054 script v01: notes for review (J0599)

Script: `crispr_script_master_v01.md` (with `opening_and_outline_v00.md`, `SOURCES_v00.md` and `SOURCES_v01.md`).

**Draft only (J0599, Gemini Argon, 18 Oct 2026).** Built from `054_Ishino-Mojica-Doudna-Charpentier-CRISPR/opening_and_outline_v00.md` and the neighbour and search evidence in `IDEAS_2026-10-18_J0591.md` (`evidence_2026-10-18_J0591/n_crispr.md` PASS — 7 education videos ≥ 1M views: **Kurzgesagt *Genetic Engineering Will Change Everything Forever – CRISPR* (`jAhjPd4uNFY`, 30.74M — exact subject match!)**, **Kurzgesagt *Are GMOs Good or Bad? Genetic Engineering & Our Food* (`7TmcXYp8xu4`, 14.52M)**, **TED-Ed ★ *The genes you don't get from your parents - Devin Shuman* (`0obYR-nf45I`, 2.49M)**, **TED-Ed ★ *How CRISPR lets you edit DNA - Andrea M. Henle* (`6tw_JVz_IEc`, 2.09M — exact subject match!)**, **TED ★ *How CRISPR lets us edit our DNA | Jennifer Doudna* (`TdBAHexVYzc`, 1.94M — exact match!)**, **Amoeba Sisters *Genetic Engineering* (`CDw4WPng2iE`, 1.57M)**, and **SciShow *The Successor to CRISPR May Be Even More World Changing* (`_UimlaolxiA`, 1.41M — exact match!)**, alongside `public_search.md` showing `"jennifer doudna emmanuelle charpentier crispr cas9"` triggering YouTube autocomplete and all 5 top GB search results under 732k views). The topic isn't locked yet: Chief locks `054` and the working title pair first, then reviews/signs off this script and queues the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

Structure (*Reference lessons* §1, scripts from 011 on): every chapter opens cold and ends on a question the next one answers; the midpoint twist ("Case closed — were Mojica's viral spacers just dead evolutionary fossils sitting inside bacterial DNA? Wrong! On the twenty-third of March two thousand and seven in *Science*, Danisco food scientists Rodolphe Barrangou and Philippe Horvath unleashed deadly dairy phages onto vats of yogurt bacteria and sequenced the rare survivors" — watching *Streptococcus thermophilus* physically snip a 30-letter mugshot of the attacking virus into its `CRISPR` array, cutting phage infection 100,000-fold with 1 spacer and 100,000,000-fold with 2) lands in Part 03; Emmanuelle Charpentier's 31 March 2011 `tracrRNA` discovery, her March 2011 Puerto Rico meeting with Jennifer Doudna, and Martin Jinek, Krzysztof Chylinski, Doudna, and Charpentier's 28 June 2012 *Science* breakthrough fusing `crRNA` and `tracrRNA` into a programmable 20-letter **single-guide RNA (`sgRNA`)** lands in Part 04; the germline/laboratory-origin misconception ("Many people still believe `CRISPR` gene therapy works by editing human embryos — or that it was designed from scratch in a hospital laboratory") is raised and explained away in Part 05 via its microbial/yogurt origins and the November 2023 approval of `Casgevy` editing adult somatic bone-marrow stem cells to cure sickle-cell disease; the ending hands off directly to `055` (*How Do Your Ears Turn Air Vibrations Into Music & Speech (and Why Do Living Ears Emit Their Own Sounds)? Hermann von Helmholtz's 1863 Piano-String Resonance Theory, Georg von Békésy's 1928–1947 Cochlear Travelling Wave & David Kemp's July 1978 Otoacoustic Emissions*), with no goodbye and no subscribe ask. Five VO parts, matching 009–053.

## Marker count (v01)

Run on `crispr_script_master_v01.md`: `grep -o "DATA:" … | wc -l`, and the same for each marker.

| Marker | Count | Where | Rule |
|---|---:|---|---|
| `DATA` | **6** | 1) inked CRISPR-Cas9 20-letter RNA address & specificity chart on period paper showing a 29-bp repeat / 32-bp viral spacer array and a 20-nucleotide sgRNA + NGG PAM locating a unique target among 3.2 billion human DNA base pairs (since 4^20 = 1,099,511,627,776 combinations) (0:34); 2) inked gene-editing reprogramming comparison chart contrasting protein-guided nucleases (new 3D protein required for every DNA sequence) against RNA-guided CRISPR-Cas9 (1 universal Cas9 endonuclease + interchangeable 20-nt guide RNA) (0:52); 3) inked CRISPR locus architecture & viral-spacer match chart on period paper from Ishino et al. (Dec 1987, J. Bacteriol. 169: 5429–5433), Jansen et al. (Mar 2002, Mol. Microbiol. 43: 1565–1575), and Mojica et al. (Feb 2005, J. Mol. Evol. 60: 174–182) showing 29-bp palindromic repeats interspaced with 32-bp spacers matching bacteriophage and plasmid genomes across >40% of bacteria and ~90% of archaea (1:58); 4) inked Streptococcus thermophilus phage-resistance & spacer-acquisition chart on period paper from Barrangou, Fremaux, Deveau, Richards, Boyaval, Moineau, Romero & Horvath (23 March 2007, Science 315: 1709–1712) showing phage sensitivity dropping 10^5-fold with 1 acquired 30-bp viral spacer and >10^7-fold with 2–4 spacers while cas9 (cas5) inactivation abolishes immunity (3:42); 5) inked dual-RNA vs chimeric single-guide RNA (sgRNA) Cas9 cleavage diagram on period paper from Deltcheva & Charpentier (31 Mar 2011 Nature 471: 602–607) and Jinek, Chylinski, Fonfara, Hauer, Doudna & Charpentier (28 Jun 2012 Science 337: 816–821) showing crRNA:tracrRNA fused into a single sgRNA with a customizable 20-nt 5' guide directing HNH and RuvC nuclease domains to cut both DNA strands 3 bp upstream of an NGG PAM (5:28); 6) animated timeline building Dec 1987 · Feb 2005 · 23 Mar 2007 · 28 Jun 2012 & Nov 2023 (6:43) | 3 or more per long, including the animated timeline |
| `SCALE` | **6** | 1) a twenty-letter RNA guide offers more than one trillion possible four-letter combinations — over three hundred times more addresses than there are letters in the entire three-billion-letter human genome, letting Cas9 find one exact genetic street address inside a cell (0:34); 2) before CRISPR, targeting a new gene was like forging a brand-new steel key from scratch for every door in a city — whereas with CRISPR-Cas9, the steel scissors stay the same and you simply type a new twenty-letter postcode onto a strip of RNA (0:52); 3) for every single bacterium on Earth, there are ten bacteriophage viruses hunting it — so bacteria evolved a genetic mugshot book to remember every virus their ancestors survived (1:58); 4) adding just one thirty-letter viral mugshot to a yogurt bacterium's CRISPR archive cuts virus infection a hundred thousand times — and every daughter cell inherits that shield the moment it divides (3:42); 5) the three-letter PAM sign acts like a safety catch on a pair of scissors — because the bacterium's own CRISPR mugshot album lacks that three-letter tag, Cas9 slices invading viruses to pieces without ever cutting its own DNA (5:28); 6) just twenty-five years separated Yoshizumi Ishino's puzzling bacterial repeats in nineteen eighty-seven from programmable DNA scissors in twenty twelve — and eleven years after that, the first human patients were cured of sickle-cell disease (6:43) | Every `DATA` number gets a `SCALE:` comparison (`grep -c "SCALE:"` ≥ `DATA:` count) |
| `WHO` | **10** | Yoshizumi Ishino (0:34), Francisco J. M. Mojica (0:34), Rodolphe Barrangou (0:34), Philippe Horvath (0:34), Emmanuelle Charpentier (0:34), Jennifer A. Doudna (0:34), Ruud Jansen (1:28), Martin Jinek (4:53), Feng Zhang (4:53), George M. Church (4:53) | First mention only, role right for the scene's year (4 words or fewer) |
| `WHEN` | **19** | 28 June 2012 (0:00), December 1987 (0:34), February 2005 (0:34), 23 March 2007 (0:34), 28 June 2012 (0:34), December 1987 (1:28), 1993 (1:28), March 2002 (1:28), February 2005 (1:28), 23 March 2007 (3:08), 31 March 2011 (4:53), 28 June 2012 (4:53), January 2013 (4:53), 2020 (4:53), 1987–2023 (6:43), November 2023 (7:18), 1863 (7:45), 1928–1947 (7:45), July 1978 (7:45) | Every spoken date or era; later dates drop onto the timeline |
| `FACT` | **3** | Viral mugshots in DNA (1:28); Yogurt bacteria snip viruses (3:08); 2 blades + 1 guide RNA (4:53) | 2–4 per long (4 words or fewer per card) |

## Craft checks (*Reference lessons* §1 + *Polish pass*)

- **First-minute timings:** Answer image by 0:03 (spoon lifting yogurt zooming into *Streptococcus thermophilus* snipping a 30-letter bacteriophage mugshot into its CRISPR archive and handing a 20-letter guide RNA to Cas9 molecular scissors slicing a mutated human sickle-cell gene on 28 June 2012), title question by 0:07, promise by 0:15, stakes by 0:25, first concrete answer & real fact (Yoshizumi Ishino's December 1987 29-bp bacterial repeats, Francisco Mojica's February 2005 32-bp viral spacer match, Rodolphe Barrangou and Philippe Horvath's 23 March 2007 yogurt bacteria immune proof, and Emmanuelle Charpentier and Jennifer Doudna's 28 June 2012 single-guide RNA `CRISPR-Cas9` scissors) by 0:34.
- **Explorer limits:** 2 beats total (`[EXPLORER ACTS: once. …]`), at 1:05 (Part 01, outside the first minute) and 6:05 (Part 04 stitching `crRNA` and `tracrRNA` into a single-guide RNA strip and slotting it into `Cas9` scissors).
- **Chapter cold opens & cliffhanger questions:** Part 01 ends on why a Japanese researcher in December 1987 and a Spanish microbiologist studying salt-marsh microbes kept stumbling across 29-letter DNA palindromes and what was hiding in the spaces between them; Part 02 opens cold on why a tiny bacterium would waste chromosome space repeating the same 29 letters, tells the story of Yoshizumi Ishino's December 1987 *E. coli* repeats and Francisco Mojica's 1993–February 2005 discovery (`named CRISPR with Ruud Jansen in March 2002`) that the 32-bp spacers match deadly bacteriophages, and ends on how two food scientists protecting vats of dairy yogurt in March 2007 proved Mojica right; Part 03 opens cold on the dairy industry's phage crisis and delivers the midpoint twist (Rodolphe Barrangou and Philippe Horvath's 23 March 2007 *Science* experiment showing surviving *Streptococcus thermophilus* yogurt bacteria snipping 30-bp viral mugshots into their `CRISPR` locus to cut phage infection 100,000- to 100,000,000-fold via `Cas9`), ending on how Charpentier and Doudna turned that bacterial shield into programmable gene scissors; Part 04 opens cold on how `Cas9` grips its guide RNA (`tracrRNA`, 31 March 2011), tells the story of Charpentier and Doudna's March 2011 Old San Juan meeting and their 28 June 2012 *Science* single-guide RNA (`sgRNA`) breakthrough with Martin Jinek and Krzysztof Chylinski (adapted to human cells in January 2013 by Feng Zhang and George Church), and ends on why the November 2023 approval of the first `CRISPR` medicine overturned a common myth and how genetic medicine is reaching the inner ear; Part 05 opens cold on the embryo/hospital-origin misconception, explains `Casgevy`'s somatic adult stem-cell cure for sickle-cell disease, and hands off to Hermann von Helmholtz (1863), Georg von Békésy (1928–1947), and David Kemp's July 1978 echoing inner ear (`055`).
- **Quirky anecdote before the hard idea:** Yoshizumi Ishino writing in 1987 that nobody knew what his five palindromic repeats meant; Francisco Mojica manually typing 32-letter spacers into BLAST with almost zero grant money; Danisco cheesemakers digging into company freezers to stop viruses from ruining vats of warm yogurt; and Charpentier and Doudna teaming up on a walk through Old San Juan, Puerto Rico.
- **Rivalry / tension:** Skepticism that simple bacteria could have an adaptive immune system vs Mojica, Barrangou, and Horvath's proof; custom protein engineering (`ZFNs/TALENs`) vs a universal `Cas9` reprogrammed by 20 letters of RNA.
- **Misconception explained away:** "Many people still believe `CRISPR` gene therapy works by editing human embryos — or that it was designed from scratch in a hospital laboratory" — explained via its bacterial/yogurt origin and the November 2023 somatic stem-cell therapy (`Casgevy`) curing sickle-cell patients without germline changes (Part 05, 6:43).

## For Chief to decide

1. Lock **054 = How Did Yogurt Bacteria's 3-Billion-Year-Old Viral Mugshot Album Become Programmable Gene Scissors (`CRISPR`)? Yoshizumi Ishino's December 1987 Mystery Repeats, Francisco Mojica's 1993–2005 Salt-Marsh Viral Spacers, Rodolphe Barrangou & Philippe Horvath's 2007 Yogurt Bacteria Trial & Emmanuelle Charpentier and Jennifer Doudna's 28 June 2012 `CRISPR-Cas9` Scissors (1987–2012)** and pick the 2-way Test & Compare working title pair:
   - **A (Subject + hook, §1 rule 11):** *CRISPR Gene Scissors: The Secret Inside Yogurt Bacteria* (55 chars)
   - **B (Search question, §1 rule 2):** *How Yogurt Bacteria Gave Scientists Molecular Scissors to Edit Human DNA* (72 chars)
   - **Alt (Search / twist question):** *How a 3-Billion-Year-Old Bacterial Virus Trap Became Programmable DNA Scissors* (78 chars)
2. Review `crispr_script_master_v01.md` (91.2/100 PASS), then queue the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

## Score (`npm run review:script`)

```text
# crispr_script_master_v01.md

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

Words: 1466 · Est. min: 9.8 · Chapters: 4

## Cold open excerpt

> How did a spoonful of dairy yogurt reveal that bacteria carry a three-billion-year-old "Most Wanted" mugshot album of enemy viruses inside their DNA? And how did Emmanuelle Charpentier and Jennifer Doudna on the twenty-eighth of June twenty twelve turn that bacterial weapon into 

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 91.2/100 — proceed to VO after production checklist.

Pass threshold: 90
```
