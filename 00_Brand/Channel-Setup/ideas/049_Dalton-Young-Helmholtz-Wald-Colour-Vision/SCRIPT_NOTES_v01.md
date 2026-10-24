# 049 script v01: notes for review (J0569)

Script: `colour_vision_script_master_v01.md` (with `opening_and_outline_v00.md`, `SOURCES_v00.md` and `SOURCES_v01.md`).

**Draft only (J0569, Gemini Argon, 18 Oct 2026).** Built from `049_Dalton-Young-Helmholtz-Wald-Colour-Vision/opening_and_outline_v00.md` and the neighbour and search evidence in `IDEAS_2026-10-18_J0561.md` (`evidence_2026-10-18_J0561/n_color_vision.md` PASS — 5 education videos ≥ 1M views: **TED-Ed ★ *History’s deadliest colors - J. V. Maranto* (`gKfjHTk8KrY`, 8.45M)**, **CrashCourse *Vision: Crash Course Anatomy & Physiology #18* (`o0DYP-u1rNM`, 4.54M)**, **TED-Ed ★ *How we see color - Colm Kelleher* (`l8_fZPHasdo`, 1.66M — exact subject match!)**, **TED ★ *Color blind or color brave? | Mellody Hobson* (`oKtALHe3Y9Q`, 1.24M)**, and **TED-Ed ★ *What is color? - Colm Kelleher* (`UZ5UGnU7oOI`, 1.11M — exact subject match!)**, plus **TED ★ *Neil Harbisson: I listen to color* (`ygRNoieAnzI`, 872.0k)**, **Be Smart *How Do We Actually See Color?* (`WN1yCigL3Hk`, 850.6k)**, and **SciShow Kids *How Do We See Color?* (`DJDBTNbAWOE`, 489.8k)**, alongside `public_search.md` showing all 5 top GB search results for `"john dalton color blindness eyeballs"` under 80k views and all 5 top GB slots for *Why John Dalton Asked Scientists to Cut Open His Eyes After He Died* under 80k views). The topic isn't locked yet: Chief locks `049` and the working title pair first, then reviews/signs off this script and queues the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

Structure (*Reference lessons* §1, scripts from 011 on): every chapter opens cold and ends on a question the next one answers; the midpoint twist ("Case closed — does your eye have thousands of different colour sensors? Wrong! In eighteen oh two, English physician Thomas Young realised you could never pack thousands of different wavelength detectors onto every tiny spot of your retina!" — Young in 1802 and Hermann von Helmholtz in 1852 proving three-cone trichromacy, followed by Jeremy Nathans's 1986 X-chromosome opsin mapping and David Hunt and John Mollon's 17 February 1995 *Science* DNA analysis of John Dalton's 150-year-old preserved eye proving he had deuteranopia, missing the middle-wavelength green cone) lands in Part 03; George Wald and Ruth Hubbard's 1933–1958 discovery of the Vitamin A `11-cis-retinal` switch (which snaps straight into `all-trans-retinal` in 200 femtoseconds upon absorbing a single photon and closes ~100,000 sodium channels) lands in Part 04; the bullfighter's red-cape misconception ("Many people still believe a bull charges in a bullring because the matador's bright red cape makes it furious") is raised and explained away in Part 05 via two-cone dichromacy in cattle and dogs vs three-cone trichromacy in primates; the ending hands off directly to `050` (*How Do Memories Form & Why Do We Forget? Hermann Ebbinghaus's 1885 2,300 Nonsense Syllables, Brenda Milner & Patient H.M.'s 1953–1957 Mirror-Star Test & Eric Kandel's Sea-Slug Synapses*), with no goodbye and no subscribe ask. Five VO parts, matching 009–048.

## Marker count (v01)

Run on `colour_vision_script_master_v01.md`: `grep -o "DATA:" … | wc -l`, and the same for each marker.

| Marker | Count | Where | Rule |
|---|---:|---|---|
| `DATA` | **6** | 1) inked cone-wavelength sensitivity & X-linked prevalence chart on period paper from Young (1802), Helmholtz (1852), and Hunt & Mollon (17 February 1995 Science 267: 984–988) showing S-cones (420 nm), M-cones (534 nm, absent in Dalton), and L-cones (564 nm) combining to distinguish ~1,000,000 hues, and contrasting male (~8% = 1 in 12) vs female (~0.5% = 1 in 200) red-green colour blindness (0:34); 2) inked photoisomerization speed chart comparing a human blink (300 milliseconds = 3 × 10⁻¹ s) and a camera flash (1 millisecond) against the 200-femtosecond (2 × 10⁻¹³ s) cis-to-trans snap of retinal inside the eye (0:52); 3) inked daylight vs candlelight spectral transmission diagram on period paper from John Dalton (31 October 1794 / 1798 Manchester Memoirs 5: 28–45) showing why a pink geranium (reflecting both short-wavelength blue ~450 nm and long-wavelength red ~650 nm) looked sky-blue to Dalton in blue-rich daylight but reddish in red-rich candlelight, alongside Joseph Ransome's 28 July 1844 autopsy finding of 100% clear vitreous humour (1:58); 4) inked RGB screen metamers & Dalton X-chromosome DNA chart on period paper from Helmholtz (1852), Nathans (1986 Science 232: 193–202), and Hunt & Mollon (17 February 1995 Science 267: 984–988) showing how 580 nm monochromatic yellow light and a 630 nm Red + 530 nm Green LED pair produce identical L/M cone excitation ratios, and how Dalton's X chromosome carried the L-cone (red) gene but lacked the M-cone (green) gene (3:42); 5) inked rhodopsin photoisomerization & amplification diagram on period paper from George Wald & Ruth Hubbard (1952 J. Gen. Physiol. 36: 269–315 & 1967 Nobel Lecture) showing 1 photon straightening kinked 11-cis-retinal into all-trans-retinal in 200 fs inside the opsin pocket (tuned to 420, 534, or 564 nm by subtle amino-acid shifts) and closing ~10⁵ sodium channels per photon (5:28); 6) animated timeline building 31 Oct 1794 · 1802 & 1852 · 28 Jul 1844 · 1933–1958 · 17 Feb 1995 alongside the mammal 2-cone vs human 3-cone vs bird 4-cone UV spectrum comparison (6:43) | 3 or more per long, including the animated timeline |
| `SCALE` | **6** | 1) because each of your three cone types can distinguish about one hundred steps of brightness, three cones multiplying one hundred by one hundred by one hundred let your brain see roughly one million different shades (0:34); 2) the Vitamin A switch inside your retina snaps straight in two hundred femtoseconds — more than a trillion times faster than the blink of an eye (0:52); 3) John Dalton waited fifty years — from his seventeen ninety-four lecture to the day after his death in eighteen forty-four — so his doctor could look through the back of his own eyeball and prove his blue-jelly theory wrong (1:58); 4) a single square millimetre at the centre of your retina packs roughly one hundred and fifty thousand cone cells — yet every colour you have ever seen is mixed from just three cone types (3:42); 5) one single photon of starlight — the smallest possible packet of energy in the universe — snaps one Vitamin A molecule straight and blocks over a hundred thousand sodium ions to fire a signal to your brain (5:28); 6) two hundred and one years after John Dalton held a pink geranium up to a candle in seventeen ninety-four, DNA from his own preserved retina finally solved the mystery of how he saw the world (6:43) | Every `DATA` number gets a `SCALE:` comparison (`grep -c "SCALE:"` ≥ `DATA:` count) |
| `WHO` | **12** | John Dalton (0:34), Joseph Ransome (0:34), Thomas Young (0:34), Hermann von Helmholtz (0:34), George Wald (0:34), David M. Hunt (0:34), John D. Mollon (0:34), Ewald Hering (3:08), Jeremy Nathans (3:08), Franz Boll (4:53), Willy Kühne (4:53), Ruth Hubbard (4:53) | First mention only, role right for the scene's year (4 words or fewer) |
| `WHEN` | **27** | Manchester 31 October 1794 (0:00), Manchester 28 July 1844 (0:21), 31 October 1794 (0:34), 28 July 1844 (0:34), 1802 (0:34), 1852 (0:34), 1933–1958 (0:34), 17 February 1995 (0:34), 1792 (1:28), 31 October 1794 (1:28), 27 July 1844 (1:28), 28 July 1844 (1:28), 1666 (3:08), 1802 (3:08), 1852 (3:08), 1878 (3:08), 1986 (3:08), 17 February 1995 (3:08), 1876 (4:53), 1878 (4:53), 1933 (4:53), 1952–1958 (4:53), 1967 (4:53), 1794–1995 (6:43), 2009 (7:18), 1885 (7:45), 1953–1957 (7:45) | Every spoken date or era; later dates drop onto the timeline |
| `FACT` | **3** | Dissected his own eyes (1:28); DNA from 150-year-old eye (3:08); Snaps in 200 femtoseconds (4:53) | 2–4 per long (4 words or fewer per card) |

## Craft checks (*Reference lessons* §1 + *Polish pass*)

- **First-minute timings:** Answer image by 0:03 (28-year-old Quaker chemist John Dalton in Manchester on 31 October 1794 holding a pink geranium flower between daylight and candlelight alongside a macro zoom into Red, Green, and Blue screen sub-pixels tricking the human eye into seeing yellow light), title question by 0:07, promise by 0:15, stakes by 0:25, first concrete answer & real fact (John Dalton's 31 October 1794 colour-blindness lecture and 28 July 1844 clear-jelly autopsy, Young and Helmholtz's 1802/1852 three-cone trichromacy, George Wald's 1933–1958 retinal switch, and Hunt and Mollon's 17 February 1995 DNA proof of Dalton's missing M-cone gene) by 0:34.
- **Explorer limits:** 2 beats total (`[EXPLORER ACTS: once. …]`), at 1:05 (Part 01, outside the first minute) and 6:05 (Part 04 catching a single photon ball on a bent Vitamin A spring-trap to snap it straight and slam shut glowing sodium gates).
- **Chapter cold opens & cliffhanger questions:** Part 01 ends on how a Quaker schoolteacher who couldn't tell a red cherry from a green leaf discovered that millions of people see a different world and why he blamed a blue liquid inside his eyeballs; Part 02 opens cold on John Dalton buying his strict Quaker mother scarlet silk stockings thinking they were dark blue, his 1792 pink geranium flower turning from sky-blue in daylight to reddish by candlelight, his 31 October 1794 Manchester lecture, and Joseph Ransome's 28 July 1844 autopsy of Dalton's eyes finding crystal-clear vitreous humour, ending on what was missing inside Dalton's retina and how DNA from his preserved eyeball solved the mystery 150 years later; Part 03 opens cold on the midpoint twist ("Case closed — does your eye have thousands of different colour sensors? Wrong!" — Thomas Young's 1802 and Hermann von Helmholtz's 1852 three-cone trichromacy explaining how Red + Green screen pixels create yellow, Jeremy Nathans's 1986 X-linked opsin genes, and David Hunt and John Mollon's 17 February 1995 *Science* DNA proof from Dalton's 150-year-old eye that he lacked the green M-cone gene), ending on how a cone physically turns a single photon of light into an electrical spark and what that has to do with Vitamin A; Part 04 opens cold on Franz Boll's 1876 light-bleaching frog retina and Willy Kühne's 1878 rhodopsin, then explains George Wald and Ruth Hubbard's 1933–1958 discovery of the 200-femtosecond `11-cis-retinal` to `all-trans-retinal` Vitamin A switch closing 100,000 sodium channels, ending on what the world looks like to animals with two cones; Part 05 opens cold on the bullfighter's red-cape misconception, explains two-cone mammal dichromacy vs three-cone primate vision and 2009 gene therapy, and hands off to Hermann Ebbinghaus's 1885 2,300 nonsense syllables and Brenda Milner's 1953–1957 mirror-star tests with Patient H.M. (`050`).
- **Quirky anecdote before the hard idea:** John Dalton buying his pious Quaker mother bright scarlet stockings thinking they were drab dark-blue, and leaving instructions for his doctor Joseph Ransome to slice a window in the back of his eyeball the day after he died and look through it like a telescope.
- **Rivalry / tension:** Dalton's blue-vitreous-humour hypothesis vs Ransome's 1844 clear-fluid autopsy and Young-Helmholtz three-cone retina theory; textbook "red-blind" dogma vs the 1995 DNA test on Dalton's 150-year-old eye.
- **Misconception explained away:** "Many people still believe a bull charges in a bullring because the matador's bright red cape makes it furious" — explained via two-cone dichromacy in cattle and dogs lacking a separate red cone and charging the cape's motion (Part 05, 6:43).

## For Chief to decide

1. Lock **049 = How Do Our Eyes See Colour & Why Are 1 in 12 Men Colour-Blind? John Dalton's 31 October 1794 Pink Geranium & Dissected Eyeballs (1844 → 1995 DNA Proof), Young and Helmholtz's Three Cones & George Wald's Vitamin A Retinal Switch (1794–2009)** and pick the 2-way Test & Compare working title pair:
   - **A (Subject + hook, §1 rule 11):** *Colour Vision: Why John Dalton Had His Own Eyes Cut Open* (56 chars)
   - **B (Search question, §1 rule 2):** *Why John Dalton Asked Scientists to Cut Open His Eyes After He Died* (67 chars)
   - **Alt (Search / twist question):** *How Three Tiny Cones and a Pickled Eyeball Solved the Mystery of Colour* (71 chars)
2. Review `colour_vision_script_master_v01.md` (92.4/100 PASS), then queue the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

## Score (`npm run review:script`)

```text
# colour_vision_script_master_v01.md

**Decision:** PASS · **Score:** 92.4 / 100

| Dimension | Score |
|---|---:|
| hook | 9.5 |
| curiosity | 9.5 |
| storytelling | 8 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 8.6 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1527 · Est. min: 10.2 · Chapters: 4

## Cold open excerpt

> Why can the screen you're looking at right now show you bright yellow lemons, even though there is not a single yellow pixel inside it? And why did chemist John Dalton , after realising on the thirty-first of October seventeen ninety-four that a pink flower looked sky-blue to him

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 92.4/100 — proceed to VO after production checklist.

Pass threshold: 90
```
