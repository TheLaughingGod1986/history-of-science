# 025 script v01: notes for review (J0447)

Script: `young_script_master_v01.md` (with `opening_and_outline_v00.md`, `SOURCES_v00.md` and `SOURCES_v01.md`).

**Draft only (J0447, Gemini Argon, 17 Oct 2026).** Built from `025_Young-Fresnel-Einstein-Light/opening_and_outline_v00.md` and the neighbour and search evidence in `IDEAS_2026-10-17_J0438.md` (`evidence_2026-10-17_J0438/n_young.md` PASS — 10 education videos ≥ 1M views including **four TED-Ed videos ≥ 1M** led by **Veritasium *There Is Something Faster Than Light* (17.05M)**, **Veritasium *The Original Double Slit Experiment* (`Iuv6hY6zsd0`, 10.11M — exact Thomas Young double-slit match)**, **Kurzgesagt *What Is Light?* (9.97M)**, **TED-Ed ★ *Schrödinger's cat: A thought experiment in quantum mechanics* (9.18M)**, **PBS Space Time *The Quantum Experiment that Broke Reality* (7.08M)**, **Veritasium *How This Spot Almost Broke Physics* (4.83M in `public_search.md` — exact Poisson/Arago spot match)**, **The Royal Institution *Why reality changes when you look at it | The Double Slit Experiment* (4.41M)**, **minutephysics *What is the Wave/Particle Duality?* (1.95M)**, **TED-Ed ★ *Is light a particle or a wave? - Colm Kelleher* (`J1yIApZtLos`, 1.81M — exact subject match)**, **TED-Ed ★ *Light waves, visible and invisible* (1.26M)**, and **TED-Ed ★ *Particles and waves: The central mystery of quantum mechanics* (1.15M)**, plus `public_search.md` showing `"thomas young double slit experiment"` and `"arago spot"` both autocompleting in GB search). The topic isn't locked yet: Chief locks `025` and the working title pair first, then reviews/signs off this script and queues the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–5) before VO.

Structure (*Reference lessons* §1, scripts from 011 on): every chapter opens cold and ends on a question the next one answers; the midpoint twist ("Case closed? Wrong." — just when Young's 1801–1803 playing-card interference, Arago's 1819 bright spot, and Maxwell's 1865 equations had convinced every physicist that light is 100% a wave, Heinrich Hertz's 1887 and Philipp Lenard's 1902 photoelectric experiments showed that blinding red light knocks out zero electrons while dim ultraviolet kicks electrons out instantly, leading 26-year-old Albert Einstein on 17 March 1905 to propose discrete light quanta $E = hf$, confirmed by Robert Millikan in 1916 and awarded the 1921 Nobel Prize in Physics) lands in Part 04; the popular misconception ("Many people think wave-particle duality just means billions of light particles bump into one another like water molecules to mimic a wave") is raised and explained away in Part 05 via Geoffrey Ingram Taylor's 1909 single-photon interference and Louis de Broglie's 1924 matter waves; the ending hands off directly to `026` (*Turning Thin Air Into Bread: Fritz Haber's Ammonia Drop & Carl Bosch's Bursting Steel Reactors*, 2 July 1909), with no goodbye and no subscribe ask. Five VO parts, matching 009–024.

## Marker count (v01)

Run on `young_script_master_v01.md`: `grep -o "DATA:" … | wc -l`, and the same for each marker.

| Marker | Count | Where | Rule |
|---|---:|---|---|
| `DATA` | **6** | 1) inked wavelength scale comparing Young's 1801 measurements of Red light (1/36,000 inch = ~700 nanometres) and Violet light (1/60,000 inch = ~420 nanometres) against the thickness of a human hair (~75,000 nanometres) (0:34); 2) inked size comparison showing ~150 visible light wavelengths (~500 nm each) fitting across 1 human hair (~75 µm) (0:52); 3) inked interference path-difference diagram on period paper showing crest + crest = 2x amplitude (bright fringe at path difference 0, 1λ, 2λ) and crest + trough = 0 (dark fringe at path difference 0.5λ, 1.5λ), with Young's 1801 table from Red (1/36,000 in = ~700 nm) to Violet (1/60,000 in = ~420 nm) (1:58); 4) inked circular-diffraction geometry diagram on period paper showing a 2 mm opaque metal disc where every ray from the circular rim travels the exact same path length √(R² + L²) to the centre of the shadow (ΔL = 0), summing constructively to form Poisson's/Arago's bright spot (3:42); 5) inked photoelectric threshold graph on period paper plotting maximum electron kinetic energy K_max against light frequency f (K_max = hf - φ): below threshold frequency f_0 (red light), 0 electrons emitted regardless of brightness; above f_0 (blue/UV light), electron energy rises linearly with slope h = 6.626 × 10⁻³⁴ J·s (5:30); 6) animated timeline building 1704 · 24 Nov 1801 & 1803 · 15 Mar 1819 · 1887–1902 · 17 Mar 1905 · 1909 · 1921 alongside an inked single-photon accumulation chart (10 photons = random dots → 1,000 photons = emerging bands → 100,000 photons = full Young wave fringes) (6:43) | 3 or more per long, including the animated timeline |
| `SCALE` | **6** | 1) one fifty-thousandth of an inch from crest to crest — more than a hundred waves of light fit side by side across the width of a single human hair (0:34); 2) 150 light waves across one strand of hair — no wonder shadows look sharp to the naked eye (0:52); 3) moving just one fifty-thousandth of an inch sideways on the wall turns bright sunlight into pitch darkness (1:58); 4) behind a solid 2-millimetre metal coin-like disc, every wave around the rim meets in step to light up the dead centre of the dark shadow (3:42); 5) a billion red photons hit the metal like ping-pong balls and knock loose zero electrons — while a single ultraviolet photon hits like a cannonball and kicks an electron straight out (5:30); 6) firing one single photon at a time with kilometres of empty space between them — and they still build Young's exact wave stripes dot by dot (6:43) | Every `DATA` number gets a `SCALE:` comparison (`grep -c "SCALE:"` ≥ `DATA:` count) |
| `WHO` | **15** | Thomas Young (0:34), Christiaan Huygens (1:28), Henry Brougham (2:28), Augustin-Jean Fresnel (3:08), Pierre-Simon Laplace (3:08), Jean-Baptiste Biot (3:08), Siméon Denis Poisson (3:08), François Arago (3:08), Heinrich Hertz (4:58), Philipp Lenard (4:58), Albert Einstein (5:30), Max Planck (5:30), Robert Millikan (6:00), Geoffrey Ingram Taylor (6:43), Louis de Broglie (6:43) | First mention only, role right for the scene's year (4 words or fewer) |
| `WHEN` | **23** | London 24 November 1801 (0:00), 1704–1801 (0:21), 24 November 1801 (0:34), 1690 (1:28), 1814 (1:28), 24 November 1803 (1:58), 1803 (2:28), 1804 (2:28), France 1815 (3:08), Paris 1818 (3:08), 15 March 1819 (4:18), 1887 (4:58), 1902 (4:58), December 1900 (5:30), Bern 17 March 1905 (5:30), 1913 (6:00), 1916 (6:00), 1921 (6:00), 1909 (6:43), 1924 (6:43), 1704–1921 (6:43), 2 July 1909 (7:45), August 1843 (7:45) | Every spoken date or era; later dates drop onto the timeline |
| `FACT` | **4** | Also cracked Rosetta Stone (1:28); Pamphlet sold just 1 copy (2:28); Used honey drop as a lens (3:08); Nobel was for photoelectric, not E=mc² (6:00) | 2–4 per long (4 words or fewer per card) |

## Craft checks (*Reference lessons* §1 + *Polish pass*)

- **First-minute timings:** Answer image by 0:03 (Thomas Young holding the thin edge of a playing card inside a narrow pinhole sunbeam in London on 24 November 1801 as the shadow on the wall breaks into rainbow-edged zebra stripes with a bright white band right down the middle), title question by 0:07, promise by 0:15, stakes by 0:25, first concrete answer & real fact (Thomas Young splitting a sunbeam with a 1/30th-inch card on 24 November 1801 and measuring red light at 1/36,000 inch and violet light at 1/60,000 inch) by 0:34.
- **Explorer limits:** 2 beats total (`[EXPLORER ACTS: once. …]`), at 1:05 (Part 01, outside the first minute) and 6:00 (Part 04 tossing a basket of soft red balls at a latched trapdoor without budging it, then rolling a single violet cannonball that pops the latch open on the first hit).
- **Chapter cold opens & cliffhanger questions:** Part 01 ends on why Britain's press mocked Young so fiercely that his reply sold only one copy and how a French judge who hated the wave theory accidentally designed the experiment that proved it right; Part 02 opens cold on "Phenomenon Young" deciphering the Rosetta Stone (*Ptolemy*) and splitting a sunbeam with a 1/30th-inch card on 24 November 1801 & 24 November 1803 (blocking one side to make the bright fringes vanish), plus Henry Brougham's *Edinburgh Review* attack and the 1804 pamphlet selling one copy, ending on how a young French road engineer revived the wave theory 14 years later and walked into an ambush in Paris; Part 03 opens cold on Augustin-Jean Fresnel using a drop of honey as a lens in 1815, Poisson's 1818 mathematical trap predicting an "absurd" bright spot at the centre of a circular shadow, and François Arago's 2-millimetre brass disc proving the bright spot real on 15 March 1819, ending on why an experiment with ultraviolet light and a metal plate 80 years later blew the case wide open again; Part 04 opens cold on the midpoint twist ("Case closed? Wrong." — Hertz and Lenard's 1887–1902 photoelectric paradox, Einstein's 17 March 1905 $E = hf$ light quanta, Planck's 1913 skepticism, and Millikan's 1916 confirmation winning Einstein the 1921 Nobel Prize), ending on what happens when you fire one single photon at a time through Young's two slits; Part 05 opens cold on the "particles bumping into each other" misconception, explains G. I. Taylor's 1909 single-photon interference and de Broglie's 1924 matter waves, and hands off to Fritz Haber and Robert Le Rossignol's 2 July 1909 high-pressure ammonia synthesis (`026`).
- **Quirky anecdote before the hard idea:** "Phenomenon Young" deciphering the Rosetta Stone and his 1804 defence pamphlet selling only a single copy; Fresnel suspended from road-building in 1815 and using a drop of honey in a hole in a metal sheet as a lens.
- **Rivalry / tension:** Poisson's 1818 mathematical ambush against Fresnel at the French Academy of Sciences, and back-and-forth portrait cuts between Max Planck (1913) and Robert Millikan (1916) trying to disprove Einstein's light quanta (6:00).
- **Misconception explained away:** "Many people think wave-particle duality just means billions of light particles bump into one another like water molecules to mimic a wave" — explained via G. I. Taylor's 1909 single-photon experiment showing each individual photon interferes with itself and lands as a single dot that builds Young's stripes over time (Part 05, 6:43).

## For Chief to decide

1. Lock **025 = Is Light a Particle or a Wave? Thomas Young's Playing Card in a Sunbeam, Poisson's Bright Spot & Einstein's Photoelectric Quanta (1801–1905)** and pick the 2-way Test & Compare working title pair:
   - **A (Subject + hook, §1 rule 11):** *The Double-Slit Experiment: How a Playing Card Broke Physics* (60 chars)
   - **B (Search question, §1 rule 2):** *How a Playing Card in a Sunbeam Proved Light Is a Wave* (54 chars)
   - **Alt (Search / twist question):** *Is Light a Particle or a Wave? The Trap That Backfired* (54 chars)
2. Review `young_script_master_v01.md` (91.0/100 PASS), then queue the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–5) before VO.

## Score (`npm run review:script`)

```text
# young_script_master_v01.md

**Decision:** PASS · **Score:** 91 / 100

| Dimension | Score |
|---|---:|
| hook | 9.5 |
| curiosity | 8.7 |
| storytelling | 8 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 8 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1487 · Est. min: 9.9 · Chapters: 4

## Cold open excerpt

> How can adding a second beam of bright sunlight to a wall make the light vanish into pitch darkness — and prove what light really is? By the end of this film, you'll see how a London doctor who helped decipher the Rosetta Stone overturned Isaac Newton with a slip of card one-thir

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 91/100 — proceed to VO after production checklist.

Pass threshold: 90
```
