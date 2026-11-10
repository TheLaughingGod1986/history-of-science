# 066 script v01: notes for review (J0660)

Script: `cancer_script_master_v01.md` (with `opening_and_outline_v00.md`, `SOURCES_v00.md` and `SOURCES_v01.md`).

**Draft only (J0660, Gemini Argon, 19 Oct 2026).** Built from `066_Rous-Knudson-Bishop-Varmus-Lane-Cancer-Oncogenes-p53/opening_and_outline_v00.md` and the neighbour and search evidence in `IDEAS_2026-10-19_J0652.md` (`evidence_2026-10-19_J0652/n_cancer_oncogenes.md` PASS — 7+ education videos ≥ 1M views, ALL strictly on cancer, oncogenes, cell-cycle checkpoints & tumour suppressors: **Kurzgesagt – In a Nutshell *Your Body Killed Cancer 5 Minutes Ago / How Cancer Starts, Grows and Dies* (`zFhYJRqz_xk`, 10.19M — exact subject match!)**, **TED-Ed ★ *Why is it so hard to cure cancer? - Kyuson Yun* (`h2rR77VsF5c`, 7.48M — exact subject match!)**, **Amoeba Sisters *The Cell Cycle (and cancer) [Updated]* (`QVCjdNxJreE`, 6.78M — exact `p53` & cell-cycle match!)**, **TED-Ed ★ *The immortal cells of Henrietta Lacks - Robin Bulleri* (`22lGbAVWhro`, 6.23M)**, **TED-Ed ★ *How does chemotherapy work? - Hyunsoo Joshua No* (`RgWQCGX3MOk`, 6.23M)**, **TED-Ed ★ *How do cancer cells behave differently from healthy ones? - George Zaidan* (`BmFEoCFDi-w`, 2.66M — exact subject match!)**, **TED-Ed ★ *How does cancer spread through the body? - Ivan Seah Yu Jun* (`OcigJn8UJNQ`, 2.16M)**, and **TED-Ed ★ *How to biohack your cells to fight cancer - Greg Foot* (`Mt5C5fhuU_0`, 1.33M)**, plus **Khan Academy *Cancer | Cells* (`RZhL7LDPk8w`, 969.2k)** and **TED-Ed ★ *The cancer gene we all have - Michael Windelspecht* (`pOyKFgGKmHE`, 389.2k — directly on proto-oncogenes and tumour suppressors!)**, alongside `public_search.md` & `public_search_titles.md` showing `"how do cancer cells work"` triggering exact YouTube autocomplete, all 5 top GB search results for `"peyton rous michael bishop harold varmus oncogenes"` under 27k views, and 4 of the top 5 GB slots for *How Scientists Discovered Cancer Hides Inside Our Own Genes* under 1.7k views). The topic isn't locked yet: Chief locks `066` and the working title pair first, then reviews/signs off this script and queues the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

Structure (*Reference lessons* §1, scripts from 011 on): every chapter opens cold and ends on a question the next one answers; the midpoint twist ("Case closed — cancer is just a dominant growth gene with a stuck gas pedal! Wrong! In nineteen sixty-nine, when Henry Harris fused a cancerous cell with a normal healthy cell, the hybrid cell stopped being cancerous — because normal cells carry emergency brake genes (tumour suppressors) that override a stuck gas pedal!" — where Alfred Knudson in April 1971 in *PNAS* graphed 48 cases of childhood retinoblastoma to prove the Two-Hit Hypothesis of recessive tumour-suppressor brakes, cloned on 16 October 1986) lands in Part 03; David Lane, Lionel Crawford, Arnold Levine, and Lloyd Old's March–May 1979 discovery of `p53`, Bert Vogelstein's 14 April 1989 proof that `TP53` is the master tumour suppressor broken in >50% of human cancers, and Joshua Schiffman, Carlo Maley, and Vincent Lynch's 8 October 2015 solution to Richard Peto's 1977 paradox (`40 alleles of TP53 in elephants`) land in Part 04; the misconception that knowing cancer comes from our own genes means we can only poison all dividing cells indiscriminately is raised and explained away in Part 05 via precision targeted therapy (`Brian Druker's May 2001 imatinib / Gleevec`); the ending hands off directly to `067` (*How Does a Single Fertilised Egg Know Where to Put Your Head, Heart & Hands (`Embryology, the Spemann-Mangold Organizer & Homeobox / Hox Genes`)?*), with no goodbye and no subscribe ask. Five VO parts, matching 009–065.

## Marker count (v01)

Run on `cancer_script_master_v01.md`: `grep -o "DATA:" … | wc -l`, and the same for each marker.

| Marker | Count | Where | Rule |
|---|---:|---|---|
| `DATA` | **6** | 1) inked accelerator vs dual-brake cancer genetics chart on period paper showing proto-oncogene activation (1 mutated allele = stuck gas pedal, e.g. c-src or HRAS codon 12 G->T single-letter typo) plus Knudson's Two-Hit tumour-suppressor inactivation (both maternal and paternal alleles of RB1 or TP53 cut, with p53 broken in >50% of human cancers) (0:34); 2) inked Peto's Paradox chart comparing human TP53 gene copies (1 locus = 2 alleles, ~11–25% lifetime cancer mortality across ~37 trillion cells) vs elephant TP53 copies (20 loci = 40 alleles across ~100x more cells, <4.8% cancer mortality via hyper-sensitive p53 DNA-damage self-destruction) (0:52); 3) inked Stehelin, Varmus, Bishop & Vogt (11 March 1976, Nature 260: 170–173) radioactive cDNA hybridization curve on period paper showing viral v-src probe binding strongly to uninfected normal chicken, duck, quail, turkey, and emu cellular DNA (1:58); 4) inked Knudson (April 1971, PNAS 68: 820–823) semi-logarithmic retinoblastoma survival curve on period paper plotting 48 bilateral (hereditary, one-hit linear exponential log S = -kt, mean 3 tumors) vs unilateral (non-hereditary, two-hit quadratic curve, 1 tumor) cases (3:47); 5) inked Vogelstein (14 April 1989, Science 244: 217–221) chromosome 17p TP53 two-hit loss & Schiffman/Lynch (8 October 2015, JAMA 314: 1850–1860) ionizing-radiation lymphocyte apoptosis chart on period paper showing elephant cells (40 TP53 alleles) undergoing p53-mediated apoptosis at >2x the rate of healthy human cells (2 TP53 alleles) and >5x the rate of Li-Fraumeni syndrome cells (1 TP53 allele) (5:32); 6) animated timeline building 21 Jan 1911 · Apr 1971 & Oct 1986 · 11 Mar 1976 · May 1979, Apr 1989 & Oct 2015 (6:48) | 3 or more per long, including the animated timeline |
| `SCALE` | **6** | 1) turning a healthy cell into a tumour is like a runaway car — it takes a stuck gas pedal in a single growth gene plus cutting both independent emergency brake cables (0:34); 2) an elephant has a hundred times more cells than you do, yet because every elephant cell carries forty copies of the p53 brake gene instead of two, elephants almost never get cancer (0:52); 3) Peyton Rous's virus didn't bring an alien poison into the cell — like a car thief who hot-wires your own ignition, it stole a normal growth gene that every healthy cell uses to heal wounds and welded the gas pedal to the floor (1:58); 4) having two copies of every tumour-suppressor gene is like flying on an airliner with twin backup hydraulic brakes — if random chance cuts one cable in a million cells, the backup cable still stops the plane, unless lightning strikes the exact same cell twice (3:47); 5) instead of repairing borderline DNA damage and risking a typo, an elephant cell with forty p53 guardians hits the self-destruct button the instant its DNA is scratched (5:32); 6) from a Long Island chicken in 1911 to forty guardian genes inside an elephant, a century of detective work revealed that cancer is the shadow of the very genes that built us (6:48) | Every `DATA` number gets a `SCALE:` comparison (`grep -c "SCALE:"` ≥ `DATA:` count) |
| `WHO` | **13** | Peyton Rous (0:34), Alfred G. Knudson Jr. (0:34), J. Michael Bishop (0:34), Harold E. Varmus (0:34), Dominique Stehelin (0:34), David P. Lane (0:34), Arnold J. Levine (0:34), Lloyd J. Old (0:34), Peter K. Vogt (1:28), Robert A. Weinberg (1:28), Thaddeus P. Dryja (3:13), Bert Vogelstein (4:58), Richard Peto (4:58) | First mention only, role right for the scene's year (4 words or fewer) |
| `WHEN` | **29** | New York, 21 January 1911 (0:00), 21 January 1911 (0:34), April 1971 (0:34), 11 March 1976 (0:34), May 1979 (0:34), 1775 (1:28), 21 January 1911 (1:28), 1966 (1:28), 1970 (1:28), 11 March 1976 (1:28), 1982 (1:28), 1989 (1:28), 1969 (3:13), April 1971 (3:13), 1983 (3:13), 16 October 1986 (3:13), March 1979 (4:58), May 1979 (4:58), 14 April 1989 (4:58), 1992 (4:58), 1977 (4:58), 8 October 2015 (4:58), 1911–2015 (6:48), May 2001 (7:20), 1891 (7:45), May 1921 (7:45), December 1978 (7:45), October 1980 (7:45), 1984 (7:45) | Every spoken date or era; later dates drop onto the timeline |
| `FACT` | **3** | Cancer genes are our own genes (1:28); Two brake cables in every cell (3:13); Elephants carry 40 p53 alleles (4:58) | 2–4 per long (4 words or fewer per card) |

## Craft checks (*Reference lessons* §1 + *Polish pass*)

- **First-minute timings:** Answer image by 0:03 (dividing human cell nucleus showing a green proto-oncogene accelerator pedal jammed down and two red RB1/p53 emergency brake levers snapped), title question by 0:07, promise by 0:15, stakes by 0:25, first concrete answer & real fact (Rous's 21 January 1911 RSV virus, Knudson's April 1971 Two-Hit tumour-suppressor equation, Bishop, Varmus, Stehelin & Vogt's 11 March 1976 `c-src` proto-oncogene discovery, and Lane, Crawford, Levine & Old's May 1979 `p53` guardian discovery) by 0:34.
- **Explorer limits:** 2 beats total (`[EXPLORER ACTS: once. …]`), at 1:05 (Part 01, outside the first minute) and 6:08 (Part 04 at the elephant cell DNA inspection desk with 40 p53 guardians).
- **Chapter cold opens & cliffhanger questions:** Part 01 ends on what happened in New York in January 1911 when a farmer brought Peyton Rous a barred Plymouth Rock hen; Part 02 opens cold on the 2,000-year "black bile" / chimney-soot / parasite debate, tells the story of Peyton Rous's 21 January 1911 filterable chicken sarcoma virus (`55-year wait for the 1966 Nobel Prize`) and Stehelin, Varmus, Bishop, and Vogt's 11 March 1976 discovery that viral `src` is a stolen normal cellular `proto-oncogene` (`c-src`), and ends on why every person doesn't develop thousands of tumours in childhood; Part 03 opens cold on the midpoint twist ("Case closed — cancer is just a dominant growth gene with a stuck gas pedal! Wrong!"), tells the story of Henry Harris's 1969 cell-fusion experiment, Alfred Knudson's April 1971 Two-Hit retinoblastoma equation, and the 16 October 1986 cloning of `RB1`, and ends on how `p53` turned out to be the master guardian of the genome; Part 04 opens cold on how `p53` was mistaken for an oncogene for ten years before Bert Vogelstein's 14 April 1989 proof, explains `p53`-mediated apoptosis and Schiffman, Maley & Lynch's 8 October 2015 solution to Richard Peto's 1977 elephant paradox (`20 copies / 40 alleles of TP53`), and ends on how one single fertilised egg cell knows where to build your head, heart, and hands; Part 05 opens cold on precision targeted drugs (`imatinib / Gleevec`, May 2001), and hands off to Hans Driesch (1891), Hilde Mangold & Hans Spemann (May 1921), Edward Lewis (December 1978), and Nüsslein-Volhard, Wieschaus, Scott & Gehring (1980–1984 `Homeobox` / `Hox` genes) (`067`).
- **Quirky anecdote before the hard idea:** Peyton Rous waiting 55 years until age 87 for the Nobel Prize after filtering a chicken tumour in 1911; giant 5-ton elephants having 100× more cells than humans yet almost never getting cancer because they carry 40 alleles of the `p53` brake gene!
- **Rivalry / tension:** Infectious-virus camp vs anti-viral cancer dogma (1911–1966); dominant oncogene model vs Henry Harris & Alfred Knudson's recessive tumour-suppressor brakes; `p53` mistaken for an oncogene (1979–1988) vs unmasked as the master tumour suppressor (1989).
- **Misconception explained away:** "If cancer comes from our own cells and genes, can we only fight it with blunt chemotherapy that poisons all dividing cells?" — explained via precision targeted drugs like `imatinib` (`Gleevec`) that lock the stuck oncogene accelerator pocket (Part 05, 6:48).

## For Chief to decide

1. Lock **066 = How Did Scientists Discover That Cancer Comes From Our Own Genes With a Stuck Accelerator or Broken Brakes (`Oncogenes, Tumour Suppressors & p53`)? Peyton Rous's 21 January 1911 Chicken Sarcoma Virus, Alfred Knudson's April 1971 "Two-Hit" Retinoblastoma Equation, J. Michael Bishop & Harold Varmus's 11 March 1976 Discovery of `src` Proto-Oncogenes Inside Normal DNA, and David Lane, Arnold Levine & Lloyd Old's May 1979 Discovery of `p53` ("The Guardian of the Genome") (1911–2015)** and pick the 2-way Test & Compare working title pair:
   - **A (Subject + hook, §1 rule 11):** *Cancer Genes: The Stuck Gas Pedal Inside Your Own DNA* (53 chars)
   - **B (Search question, §1 rule 2):** *How Scientists Discovered Cancer Hides Inside Our Own Genes* (59 chars)
   - **Alt (Search / twist question):** *Why Elephants Have 100 Times More Cells Yet Rarely Get Cancer* (61 chars)
2. Review `cancer_script_master_v01.md` (90.8/100 PASS), then queue the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

## Score (`npm run review:script`)

```text
# cancer_script_master_v01.md

**Decision:** PASS · **Score:** 90.8 / 100

| Dimension | Score |
|---|---:|
| hook | 9.5 |
| curiosity | 9.5 |
| storytelling | 8 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 7 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1554 · Est. min: 10.4 · Chapters: 4

## Cold open excerpt

> Why do five-ton elephants — with a hundred times more cells than humans — almost never get cancer ? And how did a filtered chicken tumour in nineteen eleven , a childhood eye-cancer equation in nineteen seventy-one , and a gene hunt in nineteen seventy-six prove that cancer comes

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 90.8/100 — proceed to VO after production checklist.

Pass threshold: 90
```
