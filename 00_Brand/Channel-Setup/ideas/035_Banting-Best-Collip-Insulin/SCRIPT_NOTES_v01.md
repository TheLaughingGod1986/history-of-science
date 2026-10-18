# 035 script v01: notes for review (J0508)

Script: `insulin_script_master_v01.md` (with `opening_and_outline_v00.md`, `SOURCES_v00.md` and `SOURCES_v01.md`).

**Draft only (J0508, Gemini Argon, 18 Oct 2026).** Built from `035_Banting-Best-Collip-Insulin/opening_and_outline_v00.md` and the neighbour and search evidence in `IDEAS_2026-10-17_J0485.md` (`evidence_2026-10-17_J0485/n_insulin.md` PASS — 5 education videos ≥ 1M views: **TED-Ed ★ *How sugar affects the brain - Nicole Avena* (`lEXBxijQREo`, 19.25M)**, **TEDx Talks ★ *Type 2 diabetes | Sarah Hallberg* (`da1vvigy5tQ`, 11.93M)**, **TEDx Talks ★ *Sugar is Not a Treat | Jody Stanislaw* (`tic7X3ET4gE`, 5.97M)**, **TED ★ *Peter Attia: What if we're wrong about diabetes?* (`UMhLBPPtlrY`, 2.73M)**, and **TED-Ed ★ *What does the pancreas do? - Emma Bryce* (`8dgoeYPoE-0`, 1.33M)**, plus **TED-Ed ★ *What did dogs teach humans about diabetes? - Duncan C. Ferguson* (`k_3hbrqLZ5U`, 391k)**, **FuseSchool *Insulin and Glucagon* (`y9Bdi4dnSlg`, 756k)**, and **Khan Academy *Glucose Insulin and Diabetes* (`rPLjSY00JlE`, 756k)**, alongside `public_search.md` showing 4 of the top 5 GB search results for `"frederick banting charles best insulin"` under 44k views). The topic isn't locked yet: Chief locks `035` and the working title pair first, then reviews/signs off this script and queues the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

Structure (*Reference lessons* §1, scripts from 011 on): every chapter opens cold and ends on a question the next one answers; the midpoint twist ("Case closed? Not yet." — after Banting and Best's crude brownish extract failed to clear ketones and caused a sterile abscess in 14-year-old Leonard Thompson on 11 January 1922, visiting biochemist James Collip unlocked 90%–95% fractional alcohol precipitation to purify insulin, dropping Thompson's blood glucose from 520 to 120 mg/dL in 24 hours on 23 January 1922 and waking comatose children across a Toronto ward before Banting, Best, and Collip assigned the US patent for $1 each) lands in Part 04; the popular misconception ("Many people still think eating too much candy causes Type 1 diabetes in children, or that Type 1 and Type 2 are the same thing") is raised and explained away in Part 05 via autoimmune beta-cell loss (missing insulin key) vs cellular insulin resistance (rusted lock), paired with Frederick Sanger's 51-amino-acid sequence (1955) and recombinant bacterial production (1978); the ending hands off directly to `036` (*Scurvy & the Discovery of Vitamins: James Lind's 20 May 1747 Trial on HMS Salisbury & Christiaan Eijkman's Beriberi Chickens in Java*), with no goodbye and no subscribe ask. Five VO parts, matching 009–034.

## Marker count (v01)

Run on `insulin_script_master_v01.md`: `grep -o "DATA:" … | wc -l`, and the same for each marker.

| Marker | Count | Where | Rule |
|---|---:|---|---|
| `DATA` | **6** | 1) inked blood-sugar and islet chart on period paper showing Islets of Langerhans making up just 1%–2% of pancreas mass, and Leonard Thompson's blood glucose dropping from 520 mg/dL (5.2× normal) to 120 mg/dL within 24 hours of Collip's purified insulin injection on 23 January 1922 (0:34); 2) inked mass & concentration bar comparing an ~85 g human pancreas (98% digestive enzyme tissue) vs ~1 g of Islets of Langerhans (1%–2%) and blood glucose falling from 520 mg/dL to 120 mg/dL (0:52); 3) inked comparison diagram on period paper showing a whole ground pancreas (98% acinar trypsin enzymes digesting and destroying the 1%–2% islet insulin) vs Banting's 31 October 1920 duct-ligation method (acinar enzyme cells degenerate over 6–8 weeks, leaving pure insulin-producing Islets of Langerhans intact) (1:58); 4) inked blood-glucose curve on period paper from Banting & Best's 30 July 1921 Toronto lab notebook (Dog #408) showing venous blood glucose falling from 0.20% (200 mg/dL) to 0.12% (120 mg/dL) in 1 hour after 4 mL of degenerated pancreas extract, and rising again only when injections stopped (3:42); 5) inked purification & clinical chart on period paper comparing Banting & Best's 11 January 1922 crude extract (blood glucose 440 → 320 mg/dL, abscess, ketones unchanged) vs James Collip's 90%–95% alcohol-purified insulin on 23 January 1922 (Leonard Thompson's blood glucose 520 → 120 mg/dL in 24h; 24-hour urine glucose 71.1 g → 8.7 g) (5:28); 6) animated timeline building 1869 & 1889 · 31 Oct 1920 · 30 Jul 1921 · 23 Jan 1922 · 23 Jan & Oct 1923 alongside Type 1 (autoimmune destruction of islet beta cells = 0 insulin keys) vs Type 2 (insulin resistance = rusted receptor locks) and Frederick Sanger's 51-amino-acid sequence (6:43) | 3 or more per long, including the animated timeline |
| `SCALE` | **6** | 1) the insulin-making islets make up barely one percent of your pancreas — a pinch of cells weighing a single gram — yet one purified shot dropped a dying boy's blood sugar more than fourfold in a single day (0:34); 2) one gram of islet cells is lighter than a single paperclip — hidden inside ninety-eight percent digestive tissue that destroys them the moment you grind the organ up (0:52); 3) ninety-eight percent of the pancreas is a factory of meat-dissolving digestive enzymes — so grinding up a whole pancreas was like throwing a delicate hormone key straight into a vat of acid (1:58); 4) four millilitres of chilled saltwater extract — less than a single teaspoon — dropped a dying dog's blood sugar by forty percent in sixty minutes (3:42); 5) raising alcohol from 80% to 95% turned a muddy extract that caused abscesses into a crystal-clear cure that dropped a dying teenager's blood sugar from 520 to 120 in a single day (5:28); 6) fifty-one amino acids linked into one tiny protein molecule — sold for a single dollar in 1923 so hundreds of millions of people could live (6:43) | Every `DATA` number gets a `SCALE:` comparison (`grep -c "SCALE:"` ≥ `DATA:` count) |
| `WHO` | **5** | Frederick Banting (0:34), Charles Best (0:34), John Macleod (0:34), James Collip (0:34), Oskar Minkowski (1:28) | First mention only, role right for the scene's year (4 words or fewer) |
| `WHEN` | **22** | London Ontario 31 October 1920 (0:00), Toronto 23 January 1922 (0:00), Toronto 11 January 1922 (0:21), 31 October 1920 (0:34), 30 July 1921 (0:34), 23 January 1922 (0:34), 1674 (1:28), 1869 (1:28), 1889 (1:28), 31 October 1920 (1:28), 17 May 1921 (3:08), 30 July 1921 (3:08), November 1921 (3:08), 11 January 1922 (4:53), 23 January 1922 (4:53), 23 January 1923 (4:53), October 1923 (4:53), 1955 (6:43), 1978 (6:43), 1869–1923 (6:43), 20 May 1747 (7:45), 1890 (7:45) | Every spoken date or era; later dates drop onto the timeline |
| `FACT` | **4** | Earned $4 his first month (1:28); Best won a coin toss (3:08); Sold patent for $1 each (4:53); 51 amino acids save millions (6:43) | 2–4 per long (4 words or fewer per card) |

## Craft checks (*Reference lessons* §1 + *Polish pass*)

- **First-minute timings:** Answer image by 0:03 (Frederick Banting at 2:00 a.m. on 31 October 1920 in London, Ontario, scribbling his 25-word note, dissolving to 14-year-old Leonard Thompson waking at Toronto General Hospital on 23 January 1922), title question by 0:07, promise by 0:15, stakes by 0:25, first concrete answer & real fact (Banting, Best, Macleod, and Collip isolating insulin from the 1%–2% Islets of Langerhans and dropping Thompson's blood glucose from 520 to 120 mg/dL in 24 hours on 23 January 1922) by 0:34.
- **Explorer limits:** 2 beats total (`[EXPLORER ACTS: once. …]`), at 1:05 (Part 01, outside the first minute) and 6:05 (Part 04 precipitating snow-white insulin crystals past 90% alcohol and stamping a "$1.00 — For the World" seal).
- **Chapter cold opens & cliffhanger questions:** Part 01 ends on why eating food made diabetic patients starve to death and how a struggling doctor who earned $4 in his first month solved the puzzle; Part 02 opens cold on Thomas Willis (1674), Paul Langerhans (1869), Oskar Minkowski (1889), and Frederick Banting's 2:00 a.m. 31 October 1920 note on tying off pancreatic ducts so trypsin enzymes don't digest islet hormone, ending on how a coin toss between two students and a stray terrier in a sweltering Toronto attic turned those 25 words into a living cure; Part 03 opens cold on Charles Best winning the May 1921 coin toss, Banting frying sausages over a Bunsen burner, and the 30 July 1921 breakthrough dropping Dog #408's blood sugar by 40% in 1 hour and keeping Marjorie alive 70 days, ending on why the first human injection on 11 January 1922 failed; Part 04 opens cold on the midpoint twist ("Case closed? Not yet." — Leonard Thompson's failed 11 January 1922 shot, James Collip's 90%–95% fractional alcohol precipitation saving Thompson on 23 January 1922, the Toronto coma-ward awakening, the $1 patent assignment on 23 January 1923, and the four-way 1923 Nobel split), ending on whether eating candy causes Type 1 diabetes; Part 05 opens cold on the Type 1 vs Type 2 misconception, explains Sanger's 51-amino-acid sequence (1955) and recombinant bacterial production (1978), and hands off to James Lind's 20 May 1747 scurvy clinical trial on HMS *Salisbury* and Christiaan Eijkman's 1890 Java chickens (`036`).
- **Quirky anecdote before the hard idea:** Frederick Banting earning just $4 in his entire first month of medical practice; Charles Best and Clark Noble flipping a coin for the summer shift that put Best into the history books; Banting and Best frying eggs and sausages over a Bunsen burner in the sweltering attic lab.
- **Rivalry / tension:** Banting and Best's crude first human injection failing on 11 January 1922 vs James Collip's 90% alcohol breakthrough; the October 1923 Nobel Prize omitting Best and Collip, triggering Banting and Macleod to publicly split their prize money 50/50.
- **Misconception explained away:** "Many people still think eating too much candy causes Type 1 diabetes in children, or that Type 1 and Type 2 are the same thing" — explained via autoimmune destruction of beta cells (zero insulin keys, unrelated to eating sweets) vs cellular insulin resistance (rusted locks) (Part 05, 6:43).

## For Chief to decide

1. Lock **035 = The $1 Miracle: How Insulin Turned Diabetes From a Death Sentence Into Life — Frederick Banting's 31 October 1920 2:00 a.m. Note, Charles Best & James Collip's January 1922 Toronto Ward Awakening (1869–1923)** and pick the 2-way Test & Compare working title pair:
   - **A (Subject + hook, §1 rule 11):** *Insulin & Diabetes: The 2 AM Note and the One-Dollar Patent* (59 chars)
   - **B (Search question, §1 rule 2):** *How a Struggling Doctor and a Student Discovered Insulin* (56 chars)
   - **Alt (Search / twist question):** *Why the Scientists Who Discovered Insulin Sold It for $1* (56 chars)
2. Review `insulin_script_master_v01.md` (93.3/100 PASS), then queue the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

## Score (`npm run review:script`)

```text
# insulin_script_master_v01.md

**Decision:** PASS · **Score:** 93.3 / 100

| Dimension | Score |
|---|---:|
| hook | 9.5 |
| curiosity | 9.5 |
| storytelling | 9.5 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 8 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1669 · Est. min: 11.1 · Chapters: 4

## Cold open excerpt

> Why did every attempt to save diabetic children fail for thirty years — until a broke Canadian surgeon woke at two in the morning and scribbled twenty-five misspelled words? By the end of this film, you'll see why the pancreas's own digestive juices destroyed the hormone before a

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 93.3/100 — proceed to VO after production checklist.

Pass threshold: 90
```
