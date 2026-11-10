# 092 script v01: notes for review (J0803)

Script: `bioluminescence_gfp_script_master_v01.md` (with `opening_and_outline_v00.md`, `SOURCES_v00.md` and `SOURCES_v01.md`).

**Draft only (J0803, Gemini Argon, 21 Oct 2026).** Built from `092_Boyle-Dubois-Shimomura-Chalfie-Bioluminescence-GFP/opening_and_outline_v00.md` and the neighbour and search evidence in `IDEAS_2026-10-21_J0774.md` (`evidence_2026-10-21_J0774/n_bioluminescence_gfp.md` PASS — 9 education videos ≥ 1M views: **TED-Ed ★ *The brilliance of bioluminescence - Leslie Kenna* (`oKjFVBVGad0`, 2.41M — exact bioluminescence & luciferin/luciferase match!)**, **TED-Ed ★ *The otherworldly creatures in the ocean's deepest depths - Lidia Lins* (`U69LIr0OrNc`, 2.33M)**, **TED-Ed ★ *These animals are also plants … wait, what?* (`fSaHVHTqDY0`, 1.74M)**, **TED-Ed ★ *A year in the life of one of Earth's weirdest animals* (`j43wzuciAkk`, 1.65M)**, **TED ★ *This deep-sea mystery is changing our understanding of life | Karen Lloyd* (`PbgB2TaYhio`, 1.55M)**, **TED-Ed ★ *How do animals see in the dark? - Anna Stöckl* (`t3CjTU7TaNA`, 1.31M)**, and **TED-Ed ★ *Deep ocean mysteries and wonders - David Gallo* (`Uqly8ERIkHM`, 1.16M)**, plus **TED-Ed ★ *Earth's mysterious red glow, explained* (`3jpy8UZUEOw`, 634.7k)**, **TED ★ *Glow-in-the-dark sharks and other stunning sea creatures | David Gruber* (`96HHmILhyrE`, 498.5k — exact marine biofluorescence & GFP match!)**, **TED ★ *Edith Widder: The weird and wonderful world of bioluminescence* (`IDkSDPgrtjs`, 147.0k)**, and **TED-Ed ★ *How do fireflies create light? - Emily A. Geest* (`XsFP8fpuQR4`, 142.5k)**, alongside `public_search.md` & `public_search_titles.md` showing `"what is bioluminescence"` is an exact YouTube autocomplete match (`yes`), 4 of the top 5 GB search results for `"what is bioluminescence"` under 56k views, all 5 top GB slots for `"osamu shimomura green fluorescent protein jellyfish"` under 95k views, and all 5 top GB slots for *How 10,000 Glowing Jellyfish Lit Up the Inside of Living Cells* under 434k views). The topic isn't locked yet: Chief locks `092` and the working title pair first, then reviews/signs off this script and queues the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

Structure (*Reference lessons* §1, scripts from 011 on): every chapter opens cold and ends on a question the next one answers; Robert Boyle's 29 October 1667 vacuum air-pump glowing-wood proof and Raphaël Dubois's 1885–1887 hot-and-cold water discovery of `luciferin` and `luciferase` land in Part 02; the midpoint twist ("Case closed — every glowing animal on Earth makes light by mixing a luciferin fuel with a luciferase enzyme! Wrong!") with Osamu Shimomura and Frank Johnson's Summer 1961 harvest of 10,000 *Aequorea victoria* jellyfish, the seawater-wet laboratory sink flash, and the June 1962 discovery of calcium-triggered `aequorin` and `Green Fluorescent Protein (GFP)` lands in Part 03; Douglas Prasher's May 1992 cloning of the `GFP` gene, Martin Chalfie's 11 February 1994 *Science* glowing *C. elegans* neurons, and Roger Tsien's 1994–1995 oxygen-driven `beta-barrel` chromophore and rainbow fluorescent tags (`2008 Nobel Prize`) land in Part 04; the ending hands off directly to `093` (*How Do Bats Fly in Pitch Darkness and Dolphins Hunt in Muddy Water Using Sound — and How Did Submarine Sonar Birth the Medical Ultrasound That Sees Unborn Babies?*), with no goodbye and no subscribe ask. Five VO parts, matching 009–091.

## Marker count (v01)

Run on `bioluminescence_gfp_script_master_v01.md`: `grep -o "DATA:" … | wc -l`, and the same for each marker.

| Marker | Count | Where | Rule |
|---|---:|---|---|
| `DATA` | **6** | 1) inked Raphaël Dubois (1885–1887) luciferin + luciferase reaction chart & Osamu Shimomura (1962 *J. Cell. Comp. Physiol.* 59: 223–239) Aequorin (470 nm) to GFP (509 nm) energy-transfer spectrum (0:34); 2) inked Shimomura (1961–1979) jellyfish harvest scale (10,000 → 850,000) & Chalfie/Tsien (1994–1998) GFP spectral rainbow palette (0:52); 3) inked Robert Boyle (1667 *Phil. Trans.* 2: 581–600) vacuum air-pump glowing-wood curve & Dubois (1885–1887) cold + boiled extract reconstitution chart (1:58); 4) inked Shimomura, Johnson & Saiga (June 1962) calcium-triggered Aequorin & GFP emission spectrum + 1961–1979 jellyfish collection chart (3:47); 5) inked Douglas Prasher (May 1992 *Gene*), Martin Chalfie et al. (11 Feb 1994 *Science*) *C. elegans* glowing touch-neuron map & Roger Tsien (1994–1998) 11-strand GFP beta-barrel chromophore chart (5:32); 6) animated timeline 1667–2008 (6:48) | ≥ 3 per long, including the timeline |
| `SCALE` | **6** | 1) to isolate 5 mg of glowing jellyfish protein — lighter than a raindrop — Shimomura scooped 10,000 crystal jellyfish by hand (0:34); 2) before GFP in 1994, biologists had to kill, slice, and stain cells like frozen photos — GFP turned the cell into a live movie camera (0:52); 3) a firefly lantern is nearly 20× more efficient at making visible light than a tungsten bulb, turning ~90% of its energy into cold photons (1:58); 4) over 19 summers at Friday Harbor, Shimomura and his family netted >850,000 jellyfish by hand (3:47); 5) a single GFP molecule is a nano-lantern just 4 nm tall — 25,000× thinner than a sheet of paper (5:32); 6) from glowing forest wood in a 17th-century air-pump to 10,000 jellyfish in a Washington harbour, nature's cold light illuminated the living cell (6:48) | `SCALE:` on every `DATA:` (`grep -c` matches) |
| `WHO` | **7** | Robert Boyle (1627–1691) — Anglo-Irish natural philosopher and chemist; Raphaël Dubois (1849–1929) — French physiologist and pharmacologist; Osamu Shimomura (1928–2018) — Japanese organic chemist and marine biologist; Martin Chalfie (born 1947) — American neurobiologist and geneticist; Roger Y. Tsien (1952–2016) — American biochemist; Frank Harris Johnson (1908–1990) — American biologist; Douglas C. Prasher (born 1951) — American molecular biologist | Every named person at first mention, role right for the scene's year |
| `WHEN` | **23** | Friday Harbor, Washington, Summer 1961 (0:00); 1667, 1885, Summer 1961, June 1962, 1992, 11 February 1994 (0:34); 29 October 1667, 1885, 1887, 1947 (1:28); Summer 1961, June 1962, 1979 (3:13); May 1992, 11 February 1994, 1995, 2008 (4:58); 1667–2008 timeline marker (6:48); 1793, 1880, 1938, 21 June 1958 (7:45) | Every spoken date or era |
| `FACT` | **3** | `Cold light needs oxygen` (1:28); `Seawater made the sink flash` (3:13); `GFP glows with oxygen alone` (4:58) | 2–4 per long, ≤ 4 words per card |

## Craft lessons check (*Reference lessons* §1)

- **Cold opens & cliffhanger hand-offs:** Part 01 opens cold on why a firefly or deep-sea jellyfish shines in pitch darkness yet feels completely cold to the touch and how 10,000 crushed jellyfish and a splash of seawater in a sink in Summer 1961 turned living cells into a neon rainbow, and ends on what happened in October 1667 when Robert Boyle locked glowing wood in his vacuum pump and how Raphaël Dubois in 1885 proved living light is an enzyme reaction; Part 02 opens cold on the ancient mystery of "cold fire", tells the story of Boyle's 29 October 1667 vacuum air-pump experiment and Dubois's 1885–1887 hot-and-cold water discovery of `luciferin` and `luciferase`, and ends on why every luciferin test failed when Osamu Shimomura netted 10,000 crystal jellyfish in Summer 1961; Part 03 opens cold on the midpoint twist ("Case closed — every glowing animal on Earth makes light by mixing a luciferin fuel with a luciferase enzyme! Wrong!"), tells the story of Shimomura's seawater sink flash and June 1962 isolation of calcium-triggered `aequorin` and `Green Fluorescent Protein (GFP)`, and ends on how Douglas Prasher, Martin Chalfie, and Roger Tsien proved the `GFP` gene glows inside any living cell without jellyfish enzymes; Part 04 opens cold on Douglas Prasher cloning the `GFP` gene before losing his funding and becoming a shuttle driver, tells the story of Chalfie's 11 February 1994 *Science* glowing *C. elegans* neurons and Tsien's 1994–1995 oxygen-driven `beta-barrel` rainbow, and ends on how doctors see deep inside a living body where light cannot reach using ultrasonic echoes; Part 05 opens cold on `GFP` lighting up laboratories worldwide, and hands off to Lazzaro Spallanzani (1793), Pierre Curie (1880), Donald Griffin (1938), and Ian Donald & Tom Brown (`Echolocation & Medical Ultrasound`, `093`).
- **Quirky anecdote before the hard idea:** Pouring two dark beakers of crushed clams together in a pitch-black Lyon lab to make cold light erupt; Shimomura dumping ruined jellyfish extracts into a dirty seawater sink at night and watching the drain flash blue; Douglas Prasher mailing the cloned `GFP` gene before driving an Alabama courtesy shuttle van, then flying to Stockholm as guest of honour at the 2008 Nobel ceremony!
- **Rivalry / tension:** Classical textbook dogma that all bioluminescence is `luciferin + luciferase` vs Shimomura's calcium-triggered `aequorin`; skepticism that `GFP` could never fold and glow outside a jellyfish vs Chalfie and Tsien's 1994 proof.
- **Misconception explained away:** "Doesn't light require heat, and doesn't `GFP` need jellyfish enzymes to glow?" — refuted by Boyle (1667), Dubois (1885), Shimomura (1962), and Chalfie & Tsien (1994) (Parts 01–04).

## For Chief to decide

1. Lock **092 = How Do Fireflies and Deep-Sea Jellyfish Glow in the Dark Without Heat — and How Did 10,000 Crushed Jellyfish Turn Living Cells Into Neon Microscopes (`Bioluminescence, Luciferin/Luciferase & Osamu Shimomura's 1961–1994 Green Fluorescent Protein / GFP`)? Robert Boyle's 1667 Vacuum Air-Pump Glowing-Wood Proof, Raphaël Dubois's 1885–1887 Discovery of `Luciferin` & `Luciferase`, Osamu Shimomura's Summer 1961–1962 Extraction of `Aequorin` & `Green Fluorescent Protein (GFP)` From 10,000 *Aequorea victoria* Jellyfish, and Douglas Prasher (1992), Martin Chalfie (1994) & Roger Tsien's (1994–1995) Glowing-Cell Revolution (1667–2008)** and pick the 2-way Test & Compare working title pair:
   - **A (Subject + hook, §1 rule 11):** *Bioluminescence: How 10,000 Jellyfish Lit Up Living Cells* (57 chars)
   - **B (Search question, §1 rule 2):** *How 10,000 Glowing Jellyfish Lit Up the Inside of Living Cells* (62 chars)
   - **Alt (Search / twist question):** *How Fireflies and Jellyfish Make Cold Light and Changed Medicine* (64 chars)
2. Review `bioluminescence_gfp_script_master_v01.md` (91.8/100 PASS), then queue the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

## Score (`npm run review:script`)

```text
# bioluminescence_gfp_script_master_v01.md

**Decision:** PASS · **Score:** 91.8 / 100

| Dimension | Score |
|---|---:|
| hook | 9.5 |
| curiosity | 9.1 |
| storytelling | 8 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 8.4 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1506 · Est. min: 10 · Chapters: 4

## Cold open excerpt

> How can a firefly or a deep-sea jellyfish shine bright enough to read by in pitch darkness — yet feel completely cold to the touch ? And how did ten thousand crushed jellyfish and a splash of seawater in a laboratory sink in Summer nineteen sixty-one turn the inside of living hum

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 91.8/100 — proceed to VO after production checklist.

Pass threshold: 90
```
