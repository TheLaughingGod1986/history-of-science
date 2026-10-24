# 079 script v01: notes for review (J0721)

Script: `bones_script_master_v01.md` (with `opening_and_outline_v00.md`, `SOURCES_v00.md` and `SOURCES_v01.md`).

**Draft only (J0721, Gemini Argon, 20 Oct 2026).** Built from `079_Belchier-Duhamel-Kolliker-Wolff-Mellanby-Chick-Bones-Skeleton/opening_and_outline_v00.md` and the neighbour and search evidence in `IDEAS_2026-10-20_J0713.md` (`evidence_2026-10-20_J0713/n_bones_skeleton.md` PASS — 5 education videos ≥ 1M views: **TED-Ed ★ *What makes muscles grow? - Jeffrey Siegel* (`2tM1LFFxeKg`, 23.70M)**, **CrashCourse *The Skeletal System: Crash Course Anatomy & Physiology #19* (`rDGqkMHPDqE`, 6.79M — exact osteoblasts, osteoclasts & bone remodelling match!)**, **TED-Ed ★ *How your muscular system works - Emma Bryce* (`VVL-8zr2hk4`, 3.24M)**, **Amoeba Sisters *Skeletal System* (`m26gr04HIVE`, 1.66M — exact subject match!)**, and **TED-Ed ★ *How to grow a bone - Nina Tandon* (`yJoQj5-TIvE`, 1.38M — exact subject match!)**, plus **TED-Ed ★ *How bones make blood - Melody Smith* (`1Qfmkd6C8u8`, 981.7k)** and **TED-Ed ★ *What happens when you break a bone?* (`gVXoAbeB8QI`, 423.1k)**, alongside `public_search.md` & `public_search_titles.md` showing `"how do bones heal"` is an exact YouTube autocomplete match (`yes`) and 4 of the top 5 GB search results for `"julius wolff osteoblasts osteoclasts vitamin d rickets"` under 800k views). The topic isn't locked yet: Chief locks `079` and the working title pair first, then reviews/signs off this script and queues the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

Structure (*Reference lessons* §1, scripts from 011 on): every chapter opens cold and ends on a question the next one answers; John Belchier's 1736 crimson madder-dyed pig bones, Duhamel du Monceau's 1739 alternating red-and-white bone rings, and Goodsir, Gegenbaur & Albert von Kölliker's 1845–1873 `osteoblasts` and `osteoclasts` land in Part 02; the midpoint twist ("Case closed — the spongy honeycomb of bone struts inside your hip and heel is just a random tangle of scaffolding stamped out from a fixed blueprint at birth! Wrong! In eighteen sixty-six in Zurich and eighteen ninety-two in Berlin, an iron-bridge engineer and an orthopaedic surgeon proved that your bones are living mathematical computers that re-engineer their own arches every time you move!" — where Karl Culmann spotted his Fairbairn crane stress curves inside Georg Hermann von Meyer's sliced femur and Julius Wolff formulated `Wolff's Law`) lands in Part 03; Edward Mellanby, Kurt Huldschinsky, Elmer McCollum, and Harriette Chick & Elsie Dalyell's 1919–1922 cod-liver oil and sunlight proof of `Vitamin D` lands in Part 04; the ending hands off directly to `080` (*How Did Scientists Crack the 4-Letter Genetic Code — and How Did an Unknown Scientist at 3:00 a.m. Beat the World's Greatest Biologists to Read Life's First Word?*), with no goodbye and no subscribe ask. Five VO parts, matching 009–078.

## Marker count (v01)

Run on `bones_script_master_v01.md`: `grep -o "DATA:" … | wc -l`, and the same for each marker.

| Marker | Count | Where | Rule |
|---|---:|---|---|
| `DATA` | **6** | 1) inked bone remodelling & Wolff's Law mechanical stress chart on period paper showing osteoclast HCl/protease resorption vs osteoblast collagen + hydroxyapatite deposition (10% annual turnover = 10-year complete renewal), Culmann's 1866 Fairbairn crane stress trajectories in the femoral neck, and Vitamin D calcium mineralization (0:34); 2) inked Julius Wolff (1892 Das Gesetz der Transformation der Knochen, Plates I–II) & Karl Culmann (1866) mathematical principal-stress trajectories in the iron crane vs human proximal femur trabecular arches on period paper (0:52); 3) inked John Belchier (1736 Phil. Trans. R. Soc. 39: 287–288) & Duhamel du Monceau (1739 Mém. Acad. Roy. Sci. 1–13) alternating red-and-white madder-root periosteal bone growth rings alongside Albert von Kölliker's (1873) osteoclast acid resorption pit and osteoblast collagen-hydroxyapatite deposition diagram on period paper (1:58); 4) inked Karl Culmann (1866) & Julius Wolff (1892 Das Gesetz der Transformation der Knochen) femoral trabecular stress-trajectory chart alongside tennis-player dominant vs non-dominant humeral cortical thickness (+20–35%) and astronaut microgravity bone loss (−1% to −2% per month) on period paper (3:47); 5) inked Elmer McCollum (1922 J. Biol. Chem. 53: 293–312) oxidized cod-liver oil Vitamin D proof & Harriette Chick (1 July 1922 The Lancet 200: 7–11) Vienna infant rickets X-ray healing chart on period paper (5:32); 6) animated timeline building 1736–1739 & 1873 · 1866 & 1892 · 1919–1928 (6:48) | 3 or more per long, including the animated timeline |
| `SCALE` | **6** | 1) your skeleton is not a stone monument — it is a busy highway under non-stop roadworks, where microscopic crews rip up ten percent of the pavement every year so every bone in your body is completely replaced every ten years (0:34); 2) hollowing out the middle of your thighbone and stringing microscopic bone arches only along the exact lines of force makes your femur half as heavy as solid rock yet just as strong — the exact trick engineers use to build iron bridges and cranes (0:52); 3) bone gets its secret strength from the exact same partnership as reinforced concrete — flexible collagen protein ropes act like the steel rebar that stops bone from snapping, while hard calcium crystals act like the poured cement that stops it from squashing (1:58); 4) astronauts on the International Space Station have to strap themselves to treadmills and vacuum-resistance machines for two hours every day — because without gravity tugging on their bones, their own osteoclasts assume they don't need a skeleton anymore and start dissolving it away (3:47); 5) Harriette Chick proved that Vitamin D isn't really a vitamin at all — it is a sunlight-powered hormone that your skin brews out of cholesterol whenever ultraviolet rays hit your arms, unlocking the gate that lets calcium from your lunch enter your bones (5:32); 6) from crimson pig bones on a London dinner table to an iron crane in Zurich and sunny hospital balconies in Vienna, scientists discovered how your body rebuilds its entire skeleton every ten years (6:48) | Every `DATA` number gets a `SCALE:` comparison (`grep -c "SCALE:"` ≥ `DATA:` count) |
| `WHO` | **13** | John Belchier (0:34), Henri-Louis Duhamel du Monceau (0:34), John Goodsir (0:34), Albert von Kölliker (0:34), Karl Culmann (0:34), Julius Wolff (0:34), Edward Mellanby (0:34), Elmer Verner McCollum (0:34), Harriette Chick (0:34), Carl Gegenbaur (1:28), Georg Hermann von Meyer (3:13), Kurt Huldschinsky (4:58), Elsie Jean Dalyell (4:58) | First mention only, role right for the scene's year (4 words or fewer) |
| `WHEN` | **28** | London, 1736 (0:00), 1736 (0:34), 1739 (0:34), 1845 (0:34), 1866 (0:34), 1873 (0:34), 1892 (0:34), 1919 (0:34), 1922 (0:34), 1736 (1:28), 1739 (1:28), 1845 (1:28), 1864 (1:28), 1873 (1:28), 1866 (3:13), 1867 (3:13), 1870 (3:13), 1892 (3:13), 15 March 1919 (4:58), August 1922 (4:58), 1 July 1922 (4:58), 1924 (4:58), 1928 (4:58), 1736–1928 (6:48), 1941 (7:45), 1955 (7:45), 15 April 1960 (7:45), 27 May 1961 (7:45) | Every spoken date or era; later dates drop onto the timeline |
| `FACT` | **3** | Red dye revealed bone rings (1:28); Crane matched human thighbone (3:13); Sunlight makes bone vitamin (4:58) | 2–4 per long (4 words or fewer per card) |

## Craft checks (*Reference lessons* §1 + *Polish pass*)

- **First-minute timings:** Answer image by 0:03 (living human femur with osteoclasts and osteoblasts weaving collagen and hydroxyapatite along Culmann's 1866 crane stress lines beside Belchier's 1736 crimson pig bone and Harriette Chick's 1922 Vienna sunlight ward), title question by 0:07, promise by 0:15, stakes by 0:25, first concrete answer & real fact (Belchier 1736 & Duhamel 1739 madder-root bone growth rings, Goodsir 1845 & Kölliker 1873 `osteoblasts` and `osteoclasts`, Culmann & Wolff 1866–1892 `Wolff's Law`, and Mellanby, McCollum & Chick 1919–1922 `Vitamin D`) by 0:34.
- **Explorer limits:** 2 beats total (`[EXPLORER ACTS: once. …]`), at 1:05 (Part 01, outside the first minute) and 6:08 (Part 04 turning a UV-forged golden Vitamin D key in the Gut Calcium Gate).
- **Chapter cold opens & cliffhanger questions:** Part 01 ends on how a roast-pork dinner at a London fabric printer's house in 1736 first revealed that solid bone is alive; Part 02 opens cold on Belchier staring at glowing crimson pig bones at a London cloth-printer's dinner in 1736, explains Duhamel's 1739 red-and-white bone rings and Kölliker's 1873 acid-spraying `osteoclasts` and bricklayer `osteoblasts`, and ends on how those blind microscopic cells know where to place every bone strut and why a Zurich crane engineer gasped in 1866 when he looked inside a human thighbone; Part 03 opens cold on the midpoint twist ("Case closed — the spongy honeycomb of bone struts inside your hip and heel is just a random tangle of scaffolding stamped out from a fixed blueprint at birth! Wrong!"), tells the story of Karl Culmann spotting his Fairbairn crane stress curves in Meyer's sliced femur (1866) and Julius Wolff's 1892 `Wolff's Law`, and ends on why 4 out of 5 children in smoky industrial cities by 1900 developed bowed legs (`rickets`) and how cod-liver oil and sunlight in Vienna in 1922 unlocked `Vitamin D`; Part 04 opens cold on the war between food-deficiency doctors and sunlight doctors over rickets, explains Mellanby's 1919 puppies, McCollum's August 1922 oxidized cod-liver oil naming `Vitamin D`, and Harriette Chick & Elsie Dalyell's July 1922 Vienna infant X-ray trial, and ends on how an osteoblast reads the 4-letter `DNA` alphabet (`A, T, C, G`) to weave collagen protein and how an unknown scientist at 3:00 a.m. in May 1961 cracked the `Genetic Code`; Part 05 opens cold on the living cathedral inside you, and hands off to George Beadle & Edward Tatum (1941), George Palade (1955), Sydney Brenner, François Jacob & Matthew Meselson (1960), and Marshall Nirenberg & Heinrich Matthaei (27 May 1961) (`080`).
- **Quirky anecdote before the hard idea:** A cloth printer feeding red dye-soaked bran to his pigs and serving glowing crimson pork chops to surgeon John Belchier; bridge engineer Karl Culmann shouting that a human thighbone was his harbour crane; Elmer McCollum bubbling oxygen through hot cod-liver oil; astronauts losing 1–2% of their bone mass per month in zero gravity!
- **Rivalry / tension:** Dead-stone skeleton myth vs Belchier, Duhamel & Kölliker's living turnover; diet-deficiency camp vs sunlight camp in rickets resolved by McCollum and Harriette Chick's `Vitamin D`.
- **Misconception explained away:** "Are your bones permanent, solid rock once you finish growing?" — refuted by Kölliker's `osteoclasts` and `osteoblasts` replacing ~10% of adult bone every year (~100% every 10 years) along Wolff's mechanical stress lines (Parts 02–03).

## For Chief to decide

1. Lock **079 = How Do Your Bones Dissolve and Rebuild Your Entire Skeleton Every 10 Years — and How Did Red Plant Roots, a Harbour Crane & Cod-Liver Oil Unlock the Living Skeleton (`Bone Remodelling, Osteoblasts, Osteoclasts, Julius Wolff's 1892 Law & Vitamin D / Rickets`)? John Belchier & Henri-Louis Duhamel du Monceau's 1736–1739 Madder-Root Bone-Growth Rings, John Goodsir & Albert von Kölliker's 1845–1873 Discovery of Bone-Building `Osteoblasts` & Bone-Dissolving `Osteoclasts`, Karl Culmann & Julius Wolff's 1866–1892 Crane-in-the-Femur `Wolff's Law`, and Edward Mellanby, Elmer McCollum & Harriette Chick's 1919–1922 Cod-Liver Oil & Sunlight Cure for `Rickets` (`Vitamin D`) (1736–1928)** and pick the 2-way Test & Compare working title pair:
   - **A (Subject + hook, §1 rule 11):** *Your Skeleton: Rebuilt From Scratch Every 10 Years* (50 chars)
   - **B (Search question, §1 rule 2):** *How Your Bones Dissolve and Rebuild Your Entire Skeleton Every 10 Years* (71 chars)
   - **Alt (Search / twist question):** *Why Your Bones Are Alive and How Sunlight and Cod-Liver Oil Saved Them* (70 chars)
2. Review `bones_script_master_v01.md` (91.0/100 PASS), then queue the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

## Score (`npm run review:script`)

```text
# bones_script_master_v01.md

**Decision:** PASS · **Score:** 91 / 100

| Dimension | Score |
|---|---:|
| hook | 9.5 |
| curiosity | 9.5 |
| storytelling | 8 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 7.2 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1571 · Est. min: 10.5 · Chapters: 4

## Cold open excerpt

> Why do we picture our two hundred and six bones as dead, dry white stone? Right now, microscopic wrecking-crew cells are spraying hydrochloric acid inside your bones to dissolve old mineral while bricklayer cells weave fresh bone so fast that you get a brand-new skeleton every te

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 91/100 — proceed to VO after production checklist.

Pass threshold: 90
```
