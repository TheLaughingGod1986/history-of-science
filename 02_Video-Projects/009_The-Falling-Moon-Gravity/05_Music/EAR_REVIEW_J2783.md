# HOS 009 Ear Review — J2783 (`hos_009_score_joined_v01.wav`)

- **Film**: `009_The-Falling-Moon-Gravity`
- **Job**: `J2783` (`HOS 009: listen to the new score before it is accepted`)
- **Reviewer**: `gemini` (`gemini-argon`, multimodal `audio_input` verified and recorded in `capabilities.json`)
- **Date**: 13 Nov 2026
- **Files auditioned via `audio_input`**:
  1. `05_Music/hos_009_wonder_v01.mp3` (`180.04 s`, source cue 1, ElevenLabs `eleven_music`, seed `900901`)
  2. `05_Music/hos_009_teach_v01.mp3` (`360.05 s`, source cue 2, ElevenLabs `eleven_music`, seed `900902`)
  3. `05_Music/hos_009_score_joined_v01.wav` (`535.33 s` full joined bed, `-25.9 LUFS`, `-9.3 dBTP`)
  4. `168.00–186.00 s` window of `hos_009_score_joined_v01.wav` isolating the `175.28–178.28 s` crossfade around the `176.78 s` cannon chapter card
  5. Full `535.33 s` reference audition mix of `hos_009_score_joined_v01.wav` (at `-16 dB` bed level) under all 5 locked VO parts (`02_Voiceover/hos_009_part01..05_*_norm.wav` placed at `0.00 s`, `86.34 s`, `178.68 s`, `262.06 s`, and `395.76 s`)
  6. `05_Music/hos_009_stem_part05_falling_around_the_world_v01.wav` (`141.42 s`, covering `393.86–535.28 s`)
  7. `music_gate` comparison tracks:
     - `/Volumes/data/mac-mini-archive/YouTube/orbit-with-ben/02_Video-Projects/013_Why-The-Moon-Is-Slowly-Leaving-Us/05_Music/moon-leaving-part02_score_bed_v01.mp3` (`0.821` cosine similarity)
     - `/Volumes/data/studio-live/History Of Science/02_Video-Projects/002_Mechanical-Turk-Chess-Automaton/05_Music/hos_002_part01_curious_workshop_v01_norm.wav` (`0.804` / `v02` `0.811` cosine similarity)

---

## 1. Full Joined Bed (`hos_009_score_joined_v01.wav`, `0.00–535.33 s`)

- **Wonder section (`0.00–175.28 s`)**:
  - **`0:00–0:17`**: Opens with a deep, warm, sustained G-modal bowed viol/cello pedal drone (`G2/D3`) with slow, unhurried bow movement and no percussion.
  - **`0:17–0:48`**: A single warm low plucked string (lute/pizzicato bass) enters on a calm ~4-second pulse (`0:17`, `0:21`, `0:25`, `0:29`...), giving gentle forward motion without competing with the opening hook.
  - **`0:49–1:16`**: The plucked figure expands into a sparse, delicate 5-note ascending plucked arpeggio (`G–D–G–A–B`) every ~4 seconds over the warm bowed viol pad.
  - **`1:17–1:33` (`77–93 s`, spanning the `84.44 s` transition into Part 2 *An Apple in a Plague Year*)**: Upper chamber strings swell gently into a warm modal/major harmonic lift, then settle back into the intimate viol drone and sparse plucked arpeggio. There is **no** plague-horror dissonance, minor-key melodrama, or heavy theatrical sting.
  - **`1:34–2:36` (`94–156 s`)**: Returns to the quiet viol drone and sparse 4-second plucked arpeggio under the Woolsthorpe orchard / falling apple setup.
  - **`2:37–2:55` (`157–175.28 s`)**: The plucked arpeggio stops after `156 s`, leaving a pure, warm sustained G string chord that slowly tapers into the chapter break.
- **Teach section (`178.28–535.33 s`)**:
  - Establishes a steady, measured ~70 BPM eighth-note baroque harpsichord/lute arpeggio ostinato in D minor over soft sustained low strings, with a gentle bell-like keyboard top note marking the bar changes (`A – F – D – E – C – A` over `Dm – Bb/F – C/Am – Dm`).
  - No drum kit, no modern synth bass, no brass fanfare, and no abrupt edits across the entire `535.33 s` span.

---

## 2. Crossfade at the Cannon Chapter Card (`175.28–178.28 s`, centred at `176.78 s`)

- **Verdict**: **Clean and musical (PASS by ear).**
- **What is heard**:
  - Because the wonder cue's plucked arpeggio has already concluded at `156 s`, the outgoing audio across `175.28–178.28 s` is a quiet, steady sustained G string chord.
  - The 3-second `acrossfade=d=3:c1=qsin:c2=qsin` smoothly brings in the D-minor harpsichord/lute pulse of `hos_009_teach_v01.mp3` right across the `176.78 s` chapter card window (after Part 2 VO ends at `176.18 s` and just as Part 3 VO begins at `178.68 s` with *"Newton's answer was so simple it is easy to miss"*).
  - There is **no click, no phase dip, and no double-rhythm clash** (since the outgoing tail has no rhythmic plucks to collide with the incoming teach pulse).

---

## 3. Bed Under the Locked Narration (`0.00–518.40 s`)

- **Level & Intelligibility**:
  - Mixed at standard HOS bed level (`-25.9 LUFS` integrated / `-16` to `-20 dB` below VO), Ben's narration is crisp, warm, and effortless to follow in all 5 parts.
  - Because both cues occupy either low-register sustained bowed strings (`G2–D3`) or soft middle-register plucked transient arpeggios, the `1.5–4 kHz` vocal presence band stays completely uncluttered.
- **Distracting Melody Check**:
  - **No distracting lead melody.** Neither cue has a solo melodic top line (no solo violin melody, no flute/oboe lead, no vocalise). The upper notes in the teach section are strictly a repetitive 2-bar/4-bar harpsichord/bell arpeggio figure (`A–F–D–E`) that acts as a rhythmic clock under the cannon geometry (Part 3) and the `3,600` inverse-square calculation (Part 4).
- **Wonder-to-Teach Contrast**:
  - **Clear, unmistakable shift at `176.78 s`.** Parts 1–2 (`0.00–176.18 s`) float on a spacious, nearly beatless G-modal viol drone with single plucks every ~4 seconds; Parts 3–4 (`178.68–391.96 s`) lock into a purposeful, forward-moving ~70 BPM D-minor harpsichord/lute eighth-note pulse that matches the mathematical derivation.

---

## 4. Part 5 (`393.86–535.28 s`, `hos_009_stem_part05_falling_around_the_world_v01.wav`)

- **Audibility & Continuity**:
  - **Stays warm and audible throughout (`393.86–518.40 s` VO + tail to `533 s`); zero silent breaks or dropouts.**
- **Exact Structural Behavior by Ear (Important Nuance for Chief)**:
  - `hos_009_teach_v01.mp3` has a quieter, thinned B-section from `188.0 s` to `252.0 s` of the raw cue (where the brighter upper harpsichord/bell notes `F–E–D–C` drop out, leaving a warm, subdued middle-register repeating `A` pluck over soft low strings).
  - In the joined timeline (`hos_009_score_joined_v01.wav`), that thinned B-section runs from **`363.28 s` to `427.28 s`**—meaning it begins in late Part 4 (as Halley visits Newton in Cambridge in 1684) and covers the **first `33.4 seconds` of Part 5 (`393.86–427.28 s`**, `0:00–0:33.4` of `stem_part05`, through the 1687 *Principia* publication and Halley's 1758 comet return).
  - At **`428.0 s`** (`0:34` into `stem_part05`, right as VO says *"And you can see Newton's cannon at work today. The International Space Station..."*), the main teach A-section harpsichord/bell arpeggio returns (with a single gentle high `G` bell note at `444 s` / `0:50` of Part 5) and plays steadily beneath the ISS orbit explanation and closing reflection through `518.40 s`.
  - From **`520.0 s` to `533.0 s`** (`2:06–2:19` of `stem_part05`, after the narration ends at `518.40 s`), the upper notes drop away and the cue thins into a warm, solo plucked D-minor decay that resolves cleanly before `535.28 s`.
  - **Musical assessment**: Even though the A-section arpeggio returns at `428–519 s` rather than staying thinned for the entire back half of Part 5, it works very naturally under the narration because `428 s` is the exact script pivot from 17th-century history back to the modern physical demonstration (*"And you can see Newton's cannon at work today"*), and it remains gentle, warm, and non-intrusive right to the final fade.

---

## 5. Ear Check of `music_gate` Failures (`music_gate_j2664.json`)

`music_gate.py` failed `hos_009_score_joined_v01.wav` on two technical counts:
1. **Cosine feature similarity `> 0.80`** (comparing the first 300s chroma/spectral summary vector):
   - **`0.821` vs `moon-leaving-part02_score_bed_v01.mp3` (OWB 013)**:
     - **By ear**: Completely different genre, instrumentation, and composition. OWB 013's `moon-leaving-part02` is a pure electronic space-ambient synthesizer pad drone with slow resonant filter sweeps and zero acoustic or plucked instruments. It shares high time-averaged spectral/chroma cosine similarity with the first 175 seconds of HOS 009 only because both feature long, continuous sustained bass/mid drone pedals (`wonder`). No human listener could ever hear them as the same or reused music.
   - **`0.804` / `0.811` vs `hos_002_part01_curious_workshop_v01_norm.wav` / `v02` (HOS 002)**:
     - **By ear**: Completely different composition, tempo, and lead instrument. HOS 002's `curious_workshop` is a prominent solo woodwind (flute/recorder) melody over chamber strings and piano in a light workshop waltz feel. HOS 009 has **no woodwind/flute** and shares no melody or rhythmic hook with HOS 002; the `0.804–0.811` cosine score comes purely from broad timbral/spectral overlap of period chamber strings + keyboard.
2. **`library_state: "unresolved"` (15 unreadable earlier files)**:
   - 15 comparison tracks in `/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/OWB UAT` and `HOS UAT` (including `001_How-Big-Is-Jupiter/05_Music/jupiter-music.mp3`) threw `OSError` because they are currently evicted/dataless iCloud files on the Mini.

---

## 6. Overall Ear Verdict & Recommendation for Elected Chief (`codex`)

- **Musical & Editorial Verdict (by ear)**: **PASS.**
  - The joined bed (`hos_009_score_joined_v01.wav`), the `175.28–178.28 s` crossfade at the `176.78 s` cannon chapter card, the voice-to-bed balance, the absence of a competing melody, the contrast between the Wonder (`0–175.28 s`) and Teach (`178.28–535.33 s`) sections, and the audibility/warmth of Part 5 all work cleanly by ear.
  - The two `music_gate` similarity hits (`0.821` vs OWB 013 `moon-leaving-part02` and `0.804/0.811` vs HOS 002 `curious_workshop`) are false positives of the 300-second time-averaged spectral/chroma cosine metric, not actual musical similarity or reuse.
- **Gate / Scope Decision Required from Chief (`codex`)**:
  - `SCORE_SCOPE_J2663.json` stipulates `"music_gate PASS including earlier beds on NAS and both channels ... No gate waivers."`
  - If Chief (`codex`) accepts the ear review as clearing the false-positive `0.804–0.821` cosine similarity, `music_gate_j2664.json` still has `library_state: "unresolved"` until those 15 iCloud UAT files are either materialized locally or excluded/mapped to their `/Volumes/data/mac-mini-archive` / `/Volumes/data/studio-live` counterparts.
  - Alternatively, if Chief requires a strict numeric `< 0.80` on `music_gate.py` without changing the metric, the first 175 seconds (`wonder`) is what drives the `0.821` drone-pad cosine match against `moon-leaving-part02`.
  - Per `J2783` constraints, no new takes were generated (`0` spend), locked narration was untouched, and the long assembly remains held pending Chief's decision.
