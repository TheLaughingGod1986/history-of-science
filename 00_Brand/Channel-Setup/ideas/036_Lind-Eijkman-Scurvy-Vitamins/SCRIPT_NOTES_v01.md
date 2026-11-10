# 036 script v01: notes for review (J0508)

Script: `vitamins_script_master_v01.md` (with `opening_and_outline_v00.md`, `SOURCES_v00.md` and `SOURCES_v01.md`).

**Draft only (J0508, Gemini Argon, 18 Oct 2026).** Built from `036_Lind-Eijkman-Scurvy-Vitamins/opening_and_outline_v00.md` and the neighbour and search evidence in `IDEAS_2026-10-17_J0500.md` (`evidence_2026-10-17_J0500/n_vitamins.md` PASS — 4 TED-Ed videos ≥ 1M views: **TED-Ed ★ *How your digestive system works - Emma Bryce* (`Og5xAdC8EUI`, 13.91M)**, **TED-Ed ★ *How do vitamins work? - Ginnie Trinh Nguyen* (`ISZLTJH5lYg`, 6.85M)**, **TED-Ed ★ *How does your immune system work? - Emma Bryce* (`PSRJfaAYkW4`, 5.19M)**, and **TED-Ed ★ *How do your kidneys work? - Emma Bryce* (`FN3MFhYPWWo`, 3.11M)**, plus **SciShow *Why Scurvy Doesn't Make Sense to Science* (`rn5I5tfsFN8`, 814k)**, **Khan Academy *Introduction to vitamins and minerals* (`TBNCqRCsSvY`, 360k)**, **SciShow *We Forgot How to Cure Scurvy 7ish Times* (`Py__GJjQzCA`, 355k)**, and **Khan Academy *Vitamin C and the Limeys* (`Mp9II8MmuoA`, 114k)**, alongside `public_search.md` showing all 5 top GB search results for `"james lind scurvy clinical trial"` under 9k views and all 5 top GB results for `"christiaan eijkman beriberi vitamin"` under 4k views). The topic isn't locked yet: Chief locks `036` and the working title pair first, then reviews/signs off this script and queues the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

Structure (*Reference lessons* §1, scripts from 011 on): every chapter opens cold and ends on a question the next one answers; the midpoint twist ("Case closed? Not yet." — Lind himself recommended boiling lemon juice into "rob" syrup, unknowingly destroying heat-sensitive vitamin C; after Gilbert Blane wiped out fleet scurvy in 1795 with unboiled Mediterranean lemon juice, the Admiralty lost the cure again in the 1860s by swapping to West Indian limes with half the vitamin C, while Pasteur's Germ Theory blinded doctors to deficiency diseases until Christiaan Eijkman's paralysed chickens in Java recovered in November 1890 when a strict military cook switched them from white to brown rice) lands across Parts 03–04; the popular misconception ("if ten milligrams of Vitamin C prevents scurvy, does swallowing two-thousand-milligram mega-dose pills make you two hundred times healthier?") is raised and explained away in Part 05 via water-soluble plasma/tissue saturation at ~200 mg/day and renal excretion, paired with Albert Szent-Györgyi's October 1932 Hungarian paprika extraction of ascorbic acid; the ending hands off directly to `037` (*Superconductivity & Absolute Zero: Heike Kamerlingh Onnes's 10 July 1908 Liquid Helium & 8 April 1911 Zero-Resistance Mercury in Leiden*), with no goodbye and no subscribe ask. Five VO parts, matching 009–035.

## Marker count (v01)

Run on `vitamins_script_master_v01.md`: `grep -o "DATA:" … | wc -l`, and the same for each marker.

| Marker | Count | Where | Rule |
|---|---:|---|---|
| `DATA` | **6** | 1) inked clinical-trial & mortality chart on period paper comparing George Anson's 1740–1744 voyage (1,955 men embarked; ~1,300 died of disease/scurvy vs only 4 killed by enemy action) against James Lind's 20 May 1747 HMS Salisbury 12-man 6-pair trial (only the 2 men given 2 oranges + 1 lemon daily recovered within 6 days) (0:34); 2) inked bar chart comparing 1,955 total crew vs ~1,300 disease/scurvy deaths and 4 battle deaths (1740–1744), contrasted with ~130 mg/day of Vitamin C in 2 oranges + 1 lemon vs the 10 mg/day minimum needed to prevent scurvy (0:52); 3) inked six-row clinical trial table on period paper showing James Lind's 20 May 1747 HMS Salisbury experiment (12 sailors, 6 pairs, identical diet, 6 treatments over 6 days: cider, vitriol, vinegar, half-pint seawater, garlic-mustard paste, vs 2 oranges + 1 lemon = 2/2 recovered in 6 days) (1:58); 4) inked comparison bar on period paper showing raw Mediterranean lemon juice (~53 mg Vitamin C / 100 g) vs West Indian lime juice (~29 mg / 100 g before copper oxidation) vs Lind's boiled "rob" syrup (~0–5 mg / 100 g after prolonged boiling), alongside Haslar Naval Hospital scurvy admissions dropping from 1,457 in 1780 to 2 in 1806 after Blane's 1795 lemon mandate (3:42); 5) inked epidemiological chart on period paper from Eijkman & Vorderman's 1895–1896 Java prison survey (~280,000 prisoners across 101 prisons): prisons feeding polished white rice suffered ~278 beriberi cases per 10,000 inmates (1 in 36) vs ~0.9 per 10,000 (1 in 10,000) in prisons feeding unpolished brown rice — a 300-fold difference from the rice bran skin alone (5:32); 6) animated timeline building 20 May 1747 · 1795 · Jun–Nov 1890 · 1912 · 1932 alongside Hungarian paprika (~200 mg Vitamin C / 100 g, 4× citrus) and human plasma saturation at ~200 mg/day (6:48) | 3 or more per long, including the animated timeline |
| `SCALE` | **6** | 1) on Anson's four-year voyage around the world, scurvy killed more than two hundred and fifty sailors for every single man killed by enemy cannon fire (0:34); 2) ten milligrams of vitamin C a day — the weight of a single grain of rice — is all it takes to keep your body's collagen from falling apart (0:52); 3) two oranges and a lemon held about 130 milligrams of vitamin C a day — thirteen times the ten-milligram daily threshold needed to restart collagen synthesis within forty-eight hours (1:58); 4) swapping Mediterranean lemons for copper-pumped West Indian limes cut the anti-scurvy power of a sailor's daily ration by more than half (3:42); 5) stripping the paper-thin silver bran skin off white rice raised a prisoner's risk of beriberi paralysis three hundred times over (5:32); 6) a single medium orange (~70 mg of Vitamin C) holds seven times the ten-milligram daily dose that would have saved two million sailors across the Age of Sail (6:48) | Every `DATA` number gets a `SCALE:` comparison (`grep -c "SCALE:"` ≥ `DATA:` count) |
| `WHO` | **6** | James Lind (0:34), Christiaan Eijkman (0:34), Casimir Funk (0:34), Gilbert Blane (3:08), Frederick Gowland Hopkins (4:58), Albert Szent-Györgyi (6:48) | First mention only, role right for the scene's year (4 words or fewer) |
| `WHEN` | **21** | HMS Salisbury 20 May 1747 (0:00), 1740–1747 (0:21), 20 May 1747 (0:34), 1890 (0:34), 1912 (0:34), 1741 (1:28), 20 May 1747 (1:28), 1753 (1:28), 1795 (3:08), 1860s (3:08), 1912 (3:08), 17 June 1890 (4:58), 27 November 1890 (4:58), 1901 (4:58), 1912 (4:58), 1929 (4:58), 1932 (6:48), 1937 (6:48), 1747–1932 (6:48), 10 July 1908 (7:45), 8 April 1911 (7:45) | Every spoken date or era; later dates drop onto the timeline |
| `FACT` | **4** | First controlled clinical trial (1:28); Limes had half the vitamin C (3:08); A stingy cook cured the chickens (4:58); Paprika has 4× lemon's vitamin C (6:48) | 2–4 per long (4 words or fewer per card) |

## Craft checks (*Reference lessons* §1 + *Polish pass*)

- **First-minute timings:** Answer image by 0:03 (James Lind in the dark sickbay of HMS *Salisbury* on 20 May 1747 handing two oranges and a lemon to a pair of scurvy-crippled sailors while five other pairs receive cider, vinegar, seawater, vitriol, or spice paste), title question by 0:07, promise by 0:15, stakes by 0:25, first concrete answer & real fact (Lind's 20 May 1747 six-pair trial curing the citrus pair in 6 days, Eijkman in Java in 1890, and Funk in 1912 naming vitamins) by 0:34.
- **Explorer limits:** 2 beats total (`[EXPLORER ACTS: once. …]`), at 1:05 (Part 01, outside the first minute) and 6:08 (Part 04 peeling the silver bran coat off a brown rice grain to reveal glowing B1 crystals).
- **Chapter cold opens & cliffhanger questions:** Part 01 ends on why the ship's rats and dogs never caught scurvy and how James Lind designed the experiment that invented clinical medicine; Part 02 opens cold on the broken human *GULO* gene, collagen cross-linking (30% of body protein), and Lind's 20 May 1747 six-pair HMS *Salisbury* trial, ending on why the Navy waited 42 years and how boiling juice and swapping to limes brought scurvy back; Part 03 opens cold on the midpoint twist ("Case closed? Not yet." — Lind's boiled "rob" syrup destroying vitamin C, Gilbert Blane's 1795 lemon mandate dropping Haslar admissions from 1,457 to 2, the 1860s West Indian lime swap, and Pasteur's Germ Theory blinding medicine), ending on how a stingy cook and paralysed chickens in Indonesia in 1890 cracked the mystery; Part 04 opens cold on Christiaan Eijkman's 17 June – 27 November 1890 Java chickens, the 280,000-prisoner survey (300× difference), Hopkins's accessory factors, and Casimir Funk coining "vitamine" in 1912, ending on how a Hungarian scientist who hated red paprika peppers isolated pure Vitamin C; Part 05 opens cold on Albert Szent-Györgyi's October 1932 Szeged paprika extraction, debunks the 2,000 mg mega-dose misconception via ~200 mg water-soluble kidney saturation, and hands off to Heike Kamerlingh Onnes's 10 July 1908 liquid helium and 8 April 1911 zero-resistance mercury in Leiden (`037`).
- **Quirky anecdote before the hard idea:** James Lind feeding two sailors half a pint of cold seawater a day; a strict military hospital cook in Java refusing to give "military white rice to civilian chickens"; Albert Szent-Györgyi slipping his wife's dinner paprika peppers into his pocket to test in his lab.
- **Rivalry / tension:** Boiled lemon "rob" and colonial West Indian limes undoing Lind's cure; Pasteur's Germ Theory blinding doctors to nutritional deficiencies until Eijkman's uninjected control chickens got sick too.
- **Misconception explained away:** "if ten milligrams of Vitamin C prevents scurvy, does swallowing two-thousand-milligram mega-dose pills make you two hundred times healthier?" — explained via water-soluble saturation around ~200 mg/day and renal excretion into urine (Part 05, 6:48).

## For Chief to decide

1. Lock **036 = Scurvy & the Discovery of Vitamins: James Lind's 12 Sailors on HMS *Salisbury* (20 May 1747) & Christiaan Eijkman's Beriberi Chickens in Java (1747–1932)** and pick the 2-way Test & Compare working title pair:
   - **A (Subject + hook, §1 rule 11):** *Scurvy & Vitamins: The 1747 Ship Trial That Saved Two Million Men* (65 chars)
   - **B (Search question, §1 rule 2):** *How Twelve Sailors and Two Oranges Solved the Scurvy Mystery* (60 chars)
   - **Alt (Search / twist question):** *Why the Royal Navy Found the Cure for Scurvy — Then Lost It Twice* (65 chars)
2. Review `vitamins_script_master_v01.md` (92.9/100 PASS), then queue the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

## Score (`npm run review:script`)

```text
# vitamins_script_master_v01.md

**Decision:** PASS · **Score:** 92.9 / 100

| Dimension | Score |
|---|---:|
| hook | 9.5 |
| curiosity | 9.5 |
| storytelling | 9 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 8.1 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1578 · Est. min: 10.5 · Chapters: 4

## Cold open excerpt

> How did a mystery disease kill two million sailors — until a Scottish surgeon divided twelve dying men into six pairs and cured a pair in six days with two oranges? By the end of this film, you'll see how the world's first controlled clinical trial helped dying sailors survive, w

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 92.9/100 — proceed to VO after production checklist.

Pass threshold: 90
```
