# Final QC Release Gate — Bold Explainer v05

Date: 2026-07-28  
Status: **TECHNICAL PASS — READY FOR USER LISTENING REVIEW**

This is a release candidate, not a published video. No upload or publication
has been performed.

## Approved review master

`09_Final-Export/aliens_BOLD_EXPLAINER_REBUILD_v05_QC_MASTER_v05.mp4`

- SHA-256:
  `53c1b21b1014fd082c979a758449d23d584cef7b75966adf5cb46f559bda343c`
- Container duration: 18:50.986
- Video: H.264, 1920×1080, 30 fps, yuv420p
- Audio: AAC, 48 kHz, stereo, approximately 234 kb/s
- Watermark: none added

## 1. Scientific truth check

### Result

**Pass with one wording correction applied.**

The narration distinguishes established observations from hypotheses and
speculation. The Great Filter, zoo hypothesis, early-civilisation idea and
quiet-civilisation idea are framed as possible explanations rather than
discoveries.

The radio-leakage paragraph was corrected to distinguish weak ordinary leakage
from powerful but directional and intermittent emissions such as planetary
radar.

### Verified claim groups

| Claim group | Status | Primary support |
|---|---|---|
| Proxima/Alpha Centauri is just over four light-years away | Pass | NASA light-year guidance |
| The Milky Way is approximately 100,000 light-years across and older than 13 billion years | Pass | NASA educational and galaxy-age resources |
| Earth is approximately 4.5 billion years old | Pass | NASA galaxy/Earth-age resource |
| Fermi’s question and tens-of-millions-of-years expansion argument | Pass | SETI Institute Fermi Paradox |
| More than 6,200 confirmed exoplanets; thousands of candidates | Pass | NASA Exoplanets, current 2026 page |
| First confirmed exoplanets arrived in the 1990s | Pass | NASA Exoplanets |
| The habitable zone permits possible surface liquid water but does not imply life | Pass | NASA Exoplanets |
| Drake Equation as an uncertainty framework, created in 1961 | Pass | SETI/Drake educational material |
| Early terrestrial life and a long microbial history | Pass | NASA/JPL astrobiology resources |
| Radio, lasers, atmospheric pollution and infrared waste heat as technosignatures | Pass | NASA technosignature guidance |
| Wow! signal: 1977, 72 seconds, not confirmed | Pass | SETI Institute FAQ and published research |
| Oxygen and methane require planetary context and can have abiotic explanations | Pass | NASA biosignature guidance |
| Mars preserves ancient river and lake evidence | Pass | NASA/JPL Mars results |
| Europa and Enceladus have strong evidence for subsurface oceans | Pass | NASA Europa and Cassini resources |
| Enceladus ejects ocean material that spacecraft can sample without drilling | Pass | NASA Cassini |
| Organic signatures may survive within accessible depths on Europa/Enceladus | Pass | NASA Goddard experiment |
| Low-mass red dwarfs can live for trillions of years | Pass | NASA star-types guidance |

### Source register

- https://science.nasa.gov/exoplanets/how-many-exoplanets-are-there/
- https://spaceplace.nasa.gov/light-year/en/
- https://spaceplace.nasa.gov/galaxies-age/en/
- https://www.seti.org/research/seti-101/fermi-paradox/
- https://www.seti.org/about/faq
- https://science.nasa.gov/universe/search-for-life/searching-for-signs-of-intelligent-life-technosignatures/
- https://science.nasa.gov/universe/exoplanets/life-or-illusion-avoiding-false-positives-in-the-search-for-living-worlds/
- https://science.nasa.gov/science-research/planetary-science/astrobiology/nasa-life-signs-could-survive-near-surfaces-of-enceladus-and-europa/
- https://science.nasa.gov/mission/cassini/science/enceladus/
- https://www.jpl.nasa.gov/news/nasas-curiosity-rover-team-confirms-ancient-lakes-on-mars/
- https://science.nasa.gov/universe/stars/types/

## 2. Voice and audio

### Result

**Technical pass. Human listening approval remains required.**

- Narrator: the user's Professional Voice Clone, not the earlier Instant Voice
  Clone `kDch6ACCIpqgQ0NsU9kk`.
- ElevenLabs model: Eleven Multilingual v2.
- Four generated sections were combined non-destructively.
- Raw generations remain preserved.
- Processing: gentle high-pass filtering, narrow 100/200 Hz hum reduction,
  light broadband denoising, low-pass filtering and conservative limiting.
- Only silence longer than 1.2 seconds: the intentional 1.994-second brand gap.
- Integrated programme loudness: -16.5 LUFS.
- Loudness range: 6.4 LU.
- True peak: -1.2 dBFS.
- Clipping detected: none.
- The full-programme spectrogram shows no persistent narrow-band hum line.
- Music is side-chain ducked beneath narration.

The user should still listen once with earbuds because automated analysis cannot
reliably judge every scientific pronunciation, naturalness, or subjective voice
identity.

## 3. Visual sources and repetition

### Result

**Pass.**

- Required illustrated scenes: 96.
- Present in timeline: 96.
- Dimensions: 1920×1080.
- Unique scene IDs: 96 of 96.
- Unique SHA-256 source hashes: 96 of 96.
- Exact repeated scene sources: zero.
- Generated text artifacts found in contact-sheet review: none.
- Visual style continuity: pass.
- Full-file black-frame scan: no black interval detected.
- Full-file freeze scan: two short near-static holds, approximately 3.6 and
  3.43 seconds; inspected frames remain clean and intentional.
- Opening, act transitions, board midpoints and final sequence were sampled from
  the encoded master, not only from source artwork.

## 4. Orbit mascot

### Result

**Pass.**

- Five approved transparent six-second animation loops.
- 580×430, 30 fps, alpha channel preserved at source.
- Animated appearances: 40 of 96 content scenes.
- Measured Orbit coverage: 496.642 seconds, or 44.0% of content runtime.
- Position: stable lower-right stage.
- Pose variants: present, thinking, amazed, neutral and wave-to-camera.
- Eye direction is staged toward the visual subject.
- Hover movement, blinking and restrained fades are present.
- Motion was sampled across consecutive encoded frames and is visible.
- Orbit does not jump between corners.

## 5. Narration-to-visual sync

### Result

**Structural and encoded-timeline pass.**

- Narration is the master timeline.
- Each of the 24 subject boards has an exact narration start phrase and end
  phrase.
- Each board uses four unique illustrated panels.
- Voice section 01 maps to boards 01–06.
- Voice section 02 maps to boards 07–13.
- Voice section 03 maps to boards 14–20.
- Voice section 04 maps to boards 21–24.
- The final archive imagery lands on the archive-pattern cliffhanger.
- Encoded samples at the opening, section boundaries and ending show the
  expected subject.
- Video and audio differ in stream duration by approximately 0.353 seconds at
  the final tail only; the MP4 container retains the complete audio and holds
  the final visual. No cumulative drift was detected at section boundaries.

This verifies editorial alignment, not phoneme-level lip sync; Orbit is a
reactive guide rather than a lip-synced talking head.

## 6. Branding and information cards

### Result

**Pass.**

- The hook plays first.
- The Orbit brand card begins at approximately 00:19.17.
- The card holds for two seconds with a soft fade.
- The black branding-slot defect found in the earlier render was repaired and
  visually rechecked in the full master.
- No rapid-fire information-card overlays were added to this review master.
- Scientific concepts are carried primarily by the illustrated explainer
  scenes, avoiding competition with narration.

## 7. Reproducibility

The build script was corrected so future renders insert the brand card by a
frame-accurate trim/concat operation instead of relying on the faulty
stream-copy insertion that produced the black slot.

`07_Edit-Project/_build_bold_explainer_v05.py` passes Python syntax validation.

## Decision

**The technical release gate passes.**

The remaining approval step is a single end-to-end human listening review,
preferably with earbuds, focused on:

1. narrator naturalness and any residual electronic tone;
2. pronunciation of scientific terms;
3. subjective music level;
4. whether the final cliffhanger lands emotionally.

Do not publish until that listening review is accepted by the user.
