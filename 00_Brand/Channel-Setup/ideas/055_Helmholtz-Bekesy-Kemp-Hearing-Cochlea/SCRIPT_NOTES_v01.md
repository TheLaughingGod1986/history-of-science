# 055 script v01: notes for review (J0599)

Script: `hearing_script_master_v01.md` (with `opening_and_outline_v00.md`, `SOURCES_v00.md` and `SOURCES_v01.md`).

**Draft only (J0599, Gemini Argon, 18 Oct 2026).** Built from `055_Helmholtz-Bekesy-Kemp-Hearing-Cochlea/opening_and_outline_v00.md` and the neighbour and search evidence in `IDEAS_2026-10-18_J0591.md` (`evidence_2026-10-18_J0591/n_hearing_cochlea.md` PASS — 4+ education videos ≥ 1M views: **TED-Ed ★ *What’s that ringing in your ears? - Marc Fagelson* (`TnsCsR2wDdk`, 7.45M — exact hair-cell & tinnitus match!)**, **CrashCourse *Hearing & Balance: Crash Course Anatomy & Physiology #17* (`Ie2j7GpC4JU`, 4.02M — exact subject match!)**, **TEDx Talks ★ *Tinnitus: Ringing in the Brain* (`XGq3MXQlRJs`, 2.24M)**, **SciShow *What a Cochlear Implant Actually Sounds Like* (`lzgQrHFDNLE`, 1.38M — exact cochlear tonotopic map match!)**, and **TED-Ed ★ *The science of hearing - Douglas L. Oliver* (`LkGOGzpbrCk`, 1.30M — exact subject match!)**, alongside `public_search.md` showing `"georg von bekesy cochlea hearing hair cells"` triggering YouTube autocomplete and all 5 top GB search results under 612k views). The topic isn't locked yet: Chief locks `055` and the working title pair first, then reviews/signs off this script and queues the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

Structure (*Reference lessons* §1, scripts from 011 on): every chapter opens cold and ends on a question the next one answers; the midpoint twist ("Case closed — was Békésy's passive wave in dead cadaver ears enough to explain human hearing? Wrong! In nineteen forty-eight, twenty-eight-year-old radar physicist Thomas Gold pointed out that trying to vibrate a delicate membrane inside thick cochlear fluid is like trying to swing a pendulum inside a bucket of syrup!" — vindicated 30 years later when David Kemp in July 1978 sealed a microphone into a human ear canal and recorded **otoacoustic emissions** ringing back out, powered by 12,000 dancing outer hair cells discovered by William Brownell on 11 January 1985 and Peter Dallos's prestin motor protein on 11 May 2000) lands in Part 03; Jim Hudspeth and David Corey's 1977–1983 proof of `10-microsecond` mechanical hair-cell gating (`1,000× faster than vision`) and James Pickles's 1984 electron-microscope discovery of the **tip-link** gating spring across our `~15,500` non-regenerating hair cells lands in Part 04; the tinnitus/healing misconception ("Many people still believe that the high-pitched ringing of tinnitus after a loud concert is the ear itself vibrating noisily — or that blasted hair cells simply heal over the weekend") is raised and explained away in Part 05 via non-regenerating hair-cell loss and central auditory cortex gain alongside universal newborn otoacoustic hearing screening; the ending hands off directly to `056` (*How Does Your Nose Smell 10,000 Scents (and Why Does Food Lose Its Flavour With a Blocked Nose)? Linda Buck & Richard Axel's 5 April 1991 `1,000-gene` olfactory receptor family & 5 March 1999 combinatorial piano-chord code*), with no goodbye and no subscribe ask. Five VO parts, matching 009–054.

## Marker count (v01)

Run on `hearing_script_master_v01.md`: `grep -o "DATA:" … | wc -l`, and the same for each marker.

| Marker | Count | Where | Rule |
|---|---:|---|---|
| `DATA` | **6** | 1) inked cochlear tonotopic map & active amplification chart on period paper showing the 35-mm basilar membrane sorting 20,000 Hz (stiff 0.1 mm base) to 20 Hz (flexible 0.5 mm apex) and outer hair cells providing +40 dB (100-fold) mechanical gain down to ~0.1 nm displacement (0:34); 2) inked sensory transduction speed chart comparing retinal phototransduction (~20,000–50,000 µs chemical cascade) against cochlear hair-cell tip-link channel opening (~10 µs direct mechanical gating up to 20,000 Hz) (0:52); 3) inked basilar membrane width, stiffness & travelling-wave envelope chart on period paper from Helmholtz (1863) and Békésy (1928–1947 / 1960 Experiments in Hearing) showing membrane width widening from ~0.1 mm at the base (20,000 Hz) to ~0.5 mm at the apex (20 Hz) while stiffness drops ~10,000-fold, causing each frequency's travelling wave to crest at a unique distance (1:58); 4) inked passive (dead) vs active (living +40 dB outer-hair-cell amplified) cochlear tuning curve & Kemp otoacoustic emission waveform on period paper from Gold (1948), Kemp (July 1978, JASA 64: 1386–1391), Brownell et al. (11 Jan 1985, Science 227: 194–196), and Zheng & Dallos (11 May 2000, Nature 405: 149–155) showing 12,000 prestin-driven outer hair cells sharpening frequency tuning and amplifying basilar-membrane motion 100-fold (+40 dB) (3:42); 5) inked hair-cell stereocilia staircase & tip-link gating-spring chart on period paper from Corey & Hudspeth (1979 PNAS / 1983 J. Neurosci.) and Pickles, Comis & Osborne (1984 Hearing Research 15: 103–112) showing a ~150-nm tip-link filament pulling open TMC1 mechanotransduction channels in ~10 µs across a 0.1–100 nm bundle deflection (5:28); 6) animated timeline building 1863 · 1928–1947 · Jul 1978 & Jan 1985 · 1979–1984 (6:43) | 3 or more per long, including the animated timeline |
| `SCALE` | **6** | 1) if you scaled a hair cell's microscopic bristle up to the height of the Eiffel Tower, the whisper-quiet motion it detects at the threshold of hearing would be like tilting the top of the tower by just the width of your thumb (0:34); 2) your ear's mechanical trapdoors snap open in ten millionths of a second — more than a thousand times faster than the chemical sensors in your eye, which is why you can hear two drumsticks hit a millisecond apart when your eyes only see a blur (0:52); 3) unrolled from its snail shell, your basilar membrane is just thirty-five millimetres long — the length of a paperclip, yet it sorts a thousand musical pitches from twenty hertz to twenty thousand hertz along its ribbon (1:58); 4) twelve thousand outer hair cells in each ear dance up and down up to twenty thousand times a second — acting like microscopic pogo sticks that boost a whisper a hundred times louder before your nerve cells even measure it (3:42); 5) each ear has only fifteen thousand five hundred hair cells to last your entire life — fewer than the seats in a single sports arena, compared with more than a hundred million light sensors in a single eye (5:28); 6) every time you listen to a song or hear a friend's voice, twelve thousand microscopic hair motors in each ear are dancing in time with the music to amplify vibrations smaller than an atom (6:43) | Every `DATA` number gets a `SCALE:` comparison (`grep -c "SCALE:"` ≥ `DATA:` count) |
| `WHO` | **9** | Hermann von Helmholtz (0:34), Georg von Békésy (0:34), Thomas Gold (0:34), David T. Kemp (0:34), William E. Brownell (0:34), Peter Dallos (3:08), A. James Hudspeth (4:53), David P. Corey (4:53), James O. Pickles (4:53) | First mention only, role right for the scene's year (4 words or fewer) |
| `WHEN` | **18** | July 1978 (0:00), 1863 (0:34), 1928–1947 (0:34), 1948 (0:34), July 1978 (0:34), January 1985 (0:34), 1863 (1:28), 1928–1947 (1:28), 1961 (1:28), 1948 (3:08), July 1978 (3:08), 11 January 1985 (3:08), 11 May 2000 (3:08), 1977–1983 (4:53), 1984 (4:53), 1863–2000 (6:43), 5 April 1991 (7:45), 5 March 1999 (7:45) | Every spoken date or era; later dates drop onto the timeline |
| `FACT` | **3** | 35 mm snail-shell wave (1:28); Living ears emit sound (3:08); 10-microsecond tip-link spring (4:53) | 2–4 per long (4 words or fewer per card) |

## Craft checks (*Reference lessons* §1 + *Polish pass*)

- **First-minute timings:** Answer image by 0:03 (sound wave rippling into the pea-sized spiral cochlea where silver dust glitters along Georg von Békésy's 1928–1947 travelling wave and David Kemp's July 1978 microphone records an echo ringing back out from dancing outer hair cells), title question by 0:07, promise by 0:15, stakes by 0:25, first concrete answer & real fact (Hermann von Helmholtz's 1863 resonance theory, Georg von Békésy's 1928–1947 35-mm basilar membrane travelling wave, Thomas Gold's 1948 amplifier prediction, and David Kemp's July 1978 and William Brownell's January 1985 proof of 12,000 dancing outer hair cells and 3,500 inner hair cells) by 0:34.
- **Explorer limits:** 2 beats total (`[EXPLORER ACTS: once. …]`), at 1:05 (Part 01, outside the first minute) and 6:05 (Part 04 tugging a golden 10-microsecond tip-link rope atop a hair-cell bristle staircase to pop open a spring-loaded potassium trapdoor).
- **Chapter cold opens & cliffhanger questions:** Part 01 ends on why a telephone engineer in Budapest in 1928 decided to dissect the human skull and how a sprinkle of silver dust revealed an ocean wave rolling inside the ear; Part 02 opens cold on singing into a grand piano's open strings (`Helmholtz, 1863`), tells the story of Georg von Békésy's 1928–1947 underwater dental drill, glittering silver dust, and stroboscopic discovery of the 35-mm cochlear travelling wave (`1961 Nobel Prize`), and ends on what was missing inside Békésy's dead cadaver ears that only a living ear possesses; Part 03 opens cold on the midpoint twist ("Case closed — was Békésy's passive wave in dead cadaver ears enough to explain human hearing? Wrong!"), tells the story of Thomas Gold's ridiculed 1948 active-amplifier prediction, David Kemp's July 1978 ear-canal microphone recording **otoacoustic emissions**, and William Brownell's 11 January 1985 (`prestin`, Peter Dallos, 11 May 2000) discovery of 12,000 dancing outer hair cells (`+40 dB / 100-fold` gain), and ends on how the 3,500 inner hair cells turn that motion into a nerve spark 1,000× faster than vision; Part 04 opens cold on why vision's 20–50 ms chemical cascade is too slow for hearing, explains Jim Hudspeth and David Corey's 1977–1983 `10-microsecond` mechanical gating and James Pickles's 1984 electron-microscope **tip-link** rope across our 15,500 non-regenerating hair cells, and ends on what causes the phantom ringing of **tinnitus** and how the nose smells 10,000 scents; Part 05 opens cold on the tinnitus/hair-cell-healing misconception, explains central auditory gain and newborn OAE hearing tests, and hands off to Linda Buck and Richard Axel's 5 April 1991 `1,000-gene` olfactory receptor family and 5 March 1999 combinatorial piano-chord code (`056`).
- **Quirky anecdote before the hard idea:** Georg von Békésy working at the Hungarian Post Office telephone laboratory and sprinkling glittering silver dust into cadaver skulls under a strobe lamp to see if the human ear beat a telephone earpiece; Thomas Gold being laughed out of the room in 1948 for predicting that living ears emit sound; and David Kemp sealing a tiny microphone into an ear canal in 1978 and hearing the ear echo back!
- **Rivalry / tension:** Helmholtz's independent piano strings vs Békésy's continuous hydrodynamic wave; passive dead-ear mechanics vs Thomas Gold and David Kemp's active living cochlear amplifier.
- **Misconception explained away:** "Many people still believe that the high-pitched ringing of tinnitus after a loud concert is the ear itself vibrating noisily — or that blasted hair cells simply heal over the weekend" — explained via non-regenerating hair-cell loss silencing a frequency spot on the 35-mm membrane while the brain's auditory cortex turns up its internal amplifier gain into phantom static (Part 05, 6:43).

## For Chief to decide

1. Lock **055 = How Do Your Ears Turn Air Vibrations Into Music & Speech (and Why Do Living Ears Emit Their Own Sounds)? Hermann von Helmholtz's 1863 Piano-String Resonance Theory, Georg von Békésy's 1928–1947 Cochlear Travelling Wave & David Kemp's July 1978 Otoacoustic Emissions (1863–1985)** and pick the 2-way Test & Compare working title pair:
   - **A (Subject + hook, §1 rule 11):** *How Hearing Works: The Amplifier Inside Your Inner Ear* (54 chars)
   - **B (Search question, §1 rule 2):** *How a Snail-Shell Organ in Your Skull Turns Air Waves Into Music and Speech* (75 chars)
   - **Alt (Search / twist question):** *Why Living Human Ears Literally Emit Their Own Sounds Back Into the Room* (72 chars)
2. Review `hearing_script_master_v01.md` (91.4/100 PASS), then queue the Gemini facts pass (`--kind facts`) on `SOURCES_v01.md` (rows 1–4) before VO.

## Score (`npm run review:script`)

```text
# hearing_script_master_v01.md

**Decision:** PASS · **Score:** 91.4 / 100

| Dimension | Score |
|---|---:|
| hook | 9.5 |
| curiosity | 9.5 |
| storytelling | 8 |
| scientificAccuracy | 10 |
| emotion | 9.6 |
| escalation | 7.6 |
| retentionPotential | 9 |
| searchPotential | 9.1 |
| visualOpportunities | 9.5 |
| narrationFlow | 9.6 |

Words: 1520 · Est. min: 10.1 · Chapters: 4

## Cold open excerpt

> How does a fluid-filled snail shell ( the cochlea ) the size of a garden pea detect air vibrations smaller than a single hydrogen atom ? And why did British physicist David Kemp in July nineteen seventy-eight seal a sensitive microphone into a quiet human ear and discover that li

## Findings

- **[info] overall:** Structure gates 8/8 — applied +1.05 completeness boost to supporting dimensions.
- **[info] overall:** PASS 91.4/100 — proceed to VO after production checklist.

Pass threshold: 90
```
