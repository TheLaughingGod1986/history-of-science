# HOS 009 Ear Review — J3235 (`hos_009_wonder_v03_synth.wav` & `hos_009_score_joined_v03.wav`)

- **Film**: `009_The-Falling-Moon-Gravity` (*Why Doesn't the Moon Fall to Earth?*)
- **Job**: `J3235` (`HOS 009: independent audio_input ear review of own-score v03_synth and joined v03`)
- **Scope Authority**: `05_Music/SCORE_SCOPE_J3233.json` & `05_Music/SCORE_DECISION_J3233.md` (HOS PR `#696`, merged `56d5bf4a`)
- **Predecessor Production Job (`J3234`)**: Executed by `cursor` (HOS PR `#697`, branch `cursor/j3234-hos009-v03-synth`)
- **Independent Reviewer (`J3235`)**: `gemini` (`gemini-argon`, distinct worker seat from `J3234` producer `cursor`; fresh demonstrated `audio_input` verified in-session `60ec1c3b-afa8-4115-914c-ca6d29a04973` and recorded via `chief_relay.py capabilities`)
- **Date**: `2026-11-20`
- **Spend**: `£0.00` cash, `0` subscription credits, `0` API calls, `0` media edits
- **Overall Verdict**: **`FAIL — DO NOT ACCEPT (HOLD FOR J3236 ELECTED-CHIEF DISPOSITION)`**

---

## 0. Reviewer Independence & Demonstrated `audio_input` Verification

1. **Independence from Production Author**:
   - Production job `J3234` (authoring `_build_hos009_wonder_v03_synth.py` and generating `v03_synth` / `score_joined_v03` in HOS PR `#697`) was executed by **`cursor`**.
   - Review job `J3235` is executed by **`gemini`**, a separate worker seat.
   - `J3235` is a worker review only: **no** score acceptance, **no** Chief ruling, **no** waiver of any gate or ear defect, and `J2035` / `J2171` remain held (`blocked`) for `J3236` elected-Chief disposition.
2. **Demonstrated `audio_input` in THIS Session (`60ec1c3b-afa8-4115-914c-ca6d29a04973`)**:
   - Directly decoded and listened to binary audio streams via `read_file` (`audio/wav` and `audio/mpeg`), including verbatim narration verification on `hos_009_transition_168_186_mix_v03.wav` (*"Then the Moon should be falling. But it was still up there, night after night. So what was holding it up? ... Newton's answer was so simple it is easy to miss. The Moon isn't held up at all. It really is falling."*) and across all five parts of `hos_009_reference_mix_0_518s40_v03.wav`.
   - Recorded in `~/_desk/state/chief/capabilities.json` via `python3 scripts/chief_relay.py capabilities --agent gemini --available "audio_input"`.
   - Every musical, timbral, continuity, join-blend, narration-clarity, tempo, and tail judgment below comes directly from ear audition, never from waveforms, spectrograms, or text telemetry.

---

## 1. Exact SHA-256 Parity & Preserved Lock Verification (Mini & NAS `studio-live`)

### A. All 18 `J3234` Deliverables (`PROVENANCE_v03_synth.json` — `18/18` Exact Match on Mini & NAS)

| File (under `05_Music/`) | Duration | Bytes | Verified SHA-256 (Mini & NAS `studio-live`) | Auditioned by Ear (`audio_input`) |
|---|---:|---:|---|---|
| `_build_hos009_wonder_v03_synth.py` | — | `36,305` | `bd8e20d98f87fe4253d4e4feb05cd01e44c2d904ad08c09fe9d581fa3ed9bb63` | Audited (pure Python/NumPy; `0` samples/soundfonts/network) |
| `hos_009_wonder_v03_synth.wav` | `180.000 s` | `34,560,044` | `41af45be88bcfd07af5ca7a1a03d8f691b7fcba0262a533b84a63b23c4c6f712` | **Yes (`0.00–180.00 s` complete**: `stem_part01` `0–84.44 s` WAV, `stem_part02` `84.44–176.78 s` WAV, `120–180 s` slice) |
| `hos_009_wonder_v03_synth_plan.json` | — | `1,315` | `1f9a53dd9ccc7631a5dcd7cb748293f4a1584bbe1ad87bb47eed384f21af994a` | Verified (`Pace: 60-66 BPM`, explicit `NOT ...` list) |
| `hos_009_score_joined_v03.wav` | `535.326 s` | `102,782,618` | `afeba8079e247bca8f27960dd7fc7ed3876deda5bbc652f464f0fdc3ef6f4a45` | **Yes (`0.00–535.33 s` complete**: `0–176.78 s` stems + `175–295 s`, `295–415 s`, `415–535.33 s` slices) |
| `hos_009_score_joined_v03_plan.json` | — | `2,037` | `28cf092439d74da594e3158a829142dbfc7f52a4ce03fe64cc1a822b728dcca2` | Verified (`Pace: 60-72 BPM`, `acrossfade=d=3:c1=qsin:c2=qsin`) |
| `hos_009_stem_part01_the_falling_moon_v03.wav` | `84.440 s` | `16,212,558` | `c6825e86f9f491375c7e415b1e611dc60d06ba11f6bdd8daa914d56db3d1651c` | **Yes (`audio/wav`, `0.00–84.44 s` direct)** |
| `hos_009_stem_part02_an_apple_in_a_plague_year_v03.wav` | `92.340 s` | `17,729,358` | `fb167b914f177c166b6e7083ea285eee8c3e004793ceb2639d28dac04ccd0046` | **Yes (`audio/wav`, `84.44–176.78 s` direct)** |
| `hos_009_stem_part03_the_cannon_on_the_mountain_v03.wav` | `83.380 s` | `16,009,038` | `1437dc35d97841f85002446a3f1036990eedd7f55724f37b77e903fa3cb2cfcf` | Covered (`joined` `175–295 s` + `refmix` Part 3) |
| `hos_009_stem_part04_the_moon_test_v03.wav` | `133.700 s` | `25,670,478` | `97ca7aa7e040ab50ba6774af2d1a98b8fb725b29c846bb07c2ae534e38f81074` | Covered (`joined` `260–394 s` + `refmix` Part 4) |
| `hos_009_stem_part05_falling_around_the_world_v03.wav` | `141.420 s` | `27,152,718` | `8fa0b60ab595a6020b48b2e919c8db345d9ba39ac53011436caaa4ec41e2df7b` | Covered (`joined` `394–535.33 s` + `refmix` Part 5) |
| `audio_review_v03_synth/hos_009_transition_168_186_bed_v03.wav` | `18.000 s` | `3,456,044` | `5a5b8ef4a6abaea4cb2a530e6277b1d8e31fa759c9d047afdf1c659d671e4c24` | **Yes (`audio/wav`, `168.00–186.00 s` direct)** |
| `audio_review_v03_synth/hos_009_transition_168_186_mix_v03.wav` | `18.000 s` | `3,456,044` | `48d0c3e2277a7fe504d781cffaad52e67eb1bedb501c9976ca9e95bcb7b611cb` | **Yes (`audio/wav`, `168.00–186.00 s` direct)** |
| `audio_review_v03_synth/hos_009_reference_mix_0_518s40_v03.wav` | `518.400 s` | `99,532,844` | `cdc65dc4b1c6ab86bfa7791105a606fc152191815f9eb62370fdcf729e40a16c` | **Yes (`0.00–518.40 s` complete**: 5 contiguous part slices `0–85`, `84–178`, `176–261`, `260–394`, `393–518.4 s`) |
| `audio_review_v03_synth/hos_009_tail_518s40_v03.wav` | `16.926 s` | `3,249,784` | `395c6a27f3191e98971a15777efb05b58caa8370180c8d16e3c367f5f0b7242f` | **Yes (`audio/wav`, `518.40–535.33 s` direct)** |
| `audio_review_v03_synth/hos_009_reference_endpoint_526s_v03.wav` | `526.000 s` | `100,992,044` | `d56bfff2a877463dc28bf4a534f195d4e95a81b7724c7b703605dadc1c4df48b` | **Yes (`505.00–526.00 s` endpoint slice)** |
| `music_gate_v03_wonder.json` | — | `1,886` | `fe5a3346ec329ffc93ac74d677702bfcfb857d1a5b8aabaaf7085680a174b141` | Verified (`PASS`, `94` beds, `0` unreadable, max `0.3961`) |
| `music_gate_v03_joined.json` | — | `1,889` | `5d89c827343006ab91921a6fbd9217af858a20b4dab94b82550b5196e109c682` | Verified (`PASS`, `94` beds, `0` unreadable, max `0.3868`) |
| `CONTINUITY_v03_synth.json` | — | `3,829` | `46969358626f4bd9895d6c17971f9a24fdde01ff7c2077070553746cad91bcdc` | Verified (`0` `< -45 dB` dropouts, min 1-s RMS `-20.38 dBFS`) |

### B. Preserved Prior Locks & Hard Guardrails Verified Unchanged

- `05_Music/hos_009_teach_v01.mp3`: `4c1f0a17364ad5ba96fdd2d42730b2f857d19017fab52b221701bd4e15d07bb1` (Mini & NAS exact match)
- `05_Music/hos_009_wonder_v01.mp3`: `95dfe11d7c21c9347e9b962ef2f9ecd35116f2fce60df6f123578c11a1debaf0` (Mini & NAS exact match)
- `05_Music/hos_009_score_joined_v01.wav`: `d7f5bf3d7553d7c611a913e93602b8ec83419821059294ddeaee32269a4f9572` (Mini & NAS exact match)
- `05_Music/hos_009_wonder_v02.mp3`: `b38ae8922e8d633b9f085a8bb9634c96d889a9293fcab277f7a3a23f4839d148` (Mini & NAS exact match)
- `05_Music/hos_009_score_joined_v02.wav`: `6fc8628a96b8267eaf5be6c19d7e30d9e473eb86c886ee3106c3219b375b1f68` (Mini & NAS exact match)
- `02_Voiceover/VO_TAKES_KEEP.json`: `530743c507af8d5f9049179d4e9d380b5c1b8aca4f180ada133d0b673f5925e0` (Mini & NAS exact match)
- `07_Edit-Project/VO_RETIME_v01.json`: `75a2e7afa1d822b04371511c81a52082e1b80713b0e59711702cfd05fe45a972` (Mini & NAS exact match)
- `07_Edit-Project/code_graphics_v01/code_graphic_009_p4_05_minute_second.mp4`: `e35f9a9879c8e590ec66853b85307999f39bfe30c67b9bed193ca224cab42da3` (Mini & NAS exact match)
- `07_Edit-Project/code_graphics_v01/J2632_r4/code_graphic_009_p3_01_really_falling_c1.mp4`: `23c832b09e70f78d8eeece657dac11d6148e2a5f5c701f2ad88b868845b5f3b3` (NAS `studio-live` exact match; note `J2632_r4/` subdir lives on NAS while Mini checkout holds only the earlier un-suffixed file `73e77846090c...` in `code_graphics_v01/`)
- `04_Audio/tools/hos009_score_flight.py`: `ACTIVATION_AUTHORIZED = False` verified untouched.

---

## 2. Complete-Library Unchanged `music_gate.py` Verification (`PASS`)

- **Production script verified unchanged**: `orbit-with-ben/scripts/music_gate.py` SHA-256 on disk is `62b5159f95598eaca5256b30ba66144812bad97dc86fd0c9de4618e4a1dd5385`, matching `music_gate_sha256` recorded in both `music_gate_v03_wonder.json` and `music_gate_v03_joined.json`. `_build_hos009_wonder_v03_synth.py` invokes `music_gate.judge(FILM, bed, others=others)` without modifying its rules or passing any waiver.
- **`hos_009_wonder_v03_synth.wav` (`music_gate_v03_wonder.json`)**: `verdict: "PASS"`, `comparison_count: 94` (`>= 89` across all 9 roots including 15 hash-verified materialized iCloud UAT tracks), `unreadable_warn_count: 0`, `fail: []`, `warn: []`, `matches: []`, `waiver: null`, `waiver_used: false`, `max_similarity: 0.3961` (`< 0.80`).
- **`hos_009_score_joined_v03.wav` (`music_gate_v03_joined.json`)**: `verdict: "PASS"`, `comparison_count: 94` (`>= 89`), `unreadable_warn_count: 0`, `fail: []`, `warn: []`, `matches: []`, `waiver: null`, `waiver_used: false`, `max_similarity: 0.3868` (`< 0.80`).
- **Numeric gate conclusion**: **PASS** (no reuse violation, no unreadable tracks, no waivers). However, per `SCORE_SCOPE_J3233.json`, passing numeric `music_gate.py` and continuity telemetry does **not** waive ear-review quality.

---

## 3. Explicit Timestamped Ear Audition Findings & Rubric Scores

### A. Period Chamber Musicality & Warmth (`0.00–178.28 s`) — **`FAIL`**

- **Files auditioned**: `hos_009_stem_part01_the_falling_moon_v03.wav` (`0.00–84.44 s`), `hos_009_stem_part02_an_apple_in_a_plague_year_v03.wav` (`84.44–176.78 s`), `hos_009_wonder_v03_synth.wav` (`120.00–180.00 s`), `hos_009_reference_mix_0_518s40_v03.wav` Parts 1–2 (`0.00–178.00 s`).
- **What is heard by ear**:
  - **`0.00–84.44 s` (Part 1, *The Falling Moon*)**: Neither synthesized voice reads as a warm, organic acoustic instrument. The sustained "bowed viols" layer sounds like a **harsh, buzzy, nasal electronic reed organ / sawtooth synthesizer pad** with uniform mechanical vibrato and a flat synthetic hiss. The "Karplus-Strong lute" arpeggio sounds like **thin, metallic, nasal MIDI/chiptune electronic plucks/pings** (closer to a digital clavinet/koto/video-game synth tone than plucked gut strings), landing on a completely rigid metronomic grid with zero human timing or dynamic nuance.
  - **`84.44–168.00 s` (Part 2, *An Apple in a Plague Year*)**: The synthetic artifacts become **more pronounced, brighter, and more piercing**. The plucked line jumps up an octave into thin, glassy, bell-like digital chimes/pings over an even more nasal electronic organ chord layer.
  - **`168.00–178.28 s` (Handoff window)**: The bass pluck drops out at `168.00 s`, leaving sparse, cold, tubular electronic bell/ping strikes over a hollow metallic synth drone (`170.00–178.28 s`).
- **Verdict**: **`FAIL`** against `J3235` Criterion 1 (*"do the synthesized lute and bowed viols sound warm, organic, and suitable for History of Science narration (no harsh, buzzy, metallic, or cheap MIDI/beepy synth artifacts)?"*). Even under narration at `-20.18 dB` bed gain, the artificial MIDI/chiptune synth timbre is unmistakable and below HOS house standard.

### B. Continuity (`0.00–178.28 s` & `0.00–535.33 s`) — **`PASS`**

- **What is heard by ear**:
  - **`0.00–178.28 s` (`wonder_v03_synth`)**: **Zero** inter-phrase silent dropouts anywhere in Part 1 or Part 2. Overlapping sustained chords bridge every harmonic change and the `84.44 s` Part 2 chapter card smoothly, completely remediating the six `0.61–2.29 s` `< -45 dB` dead-air dropouts that failed `wonder_v02` in `J2807` (`18.95–21.00 s`, `66.48–67.83 s`, `73.04–75.33 s`, `81.70–82.84 s`, `88.91–90.39 s`, `97.31–97.92 s`). Consistent with `CONTINUITY_v03_synth.json` (`0` silencedetect hits at `-45 dB`, min 1-s RMS `-20.38 dBFS`).
  - **`178.28–535.33 s` (`teach_v01`)**: Completely continuous throughout Parts 3, 4, and 5 (`176.78–533.0 s`) with natural decay into `535.33 s`.
- **Verdict**: **`PASS`**.

### C. `175.28–178.28 s` Join Quality (`168.00–186.00 s` Bed & VO+Bed Mix) — **`FAIL` (Timbral Cliff)**

- **Files auditioned**: `hos_009_transition_168_186_bed_v03.wav` (`audio/wav` direct), `hos_009_transition_168_186_mix_v03.wav` (`audio/wav` direct), `hos_009_score_joined_v03.wav` (`175.00–295.00 s`).
- **What is heard by ear**:
  - **Tonal match, clicks, phase (`PASS`)**: Both sides sit in D minor (`A4 = 440 Hz`), with no pitch clash, click, pop, or phase hollowing during the `175.28–178.28 s` 3-second equal-power crossfade centred on the `176.78 s` *The Cannon on the Mountain* chapter card.
  - **Timbral blend (`FAIL`)**: Across `175.28–178.28 s`, there is a **jarring, unmistakable timbral cliff**. Up to `175.28 s` (under Ben's *"Then the Moon should be falling. But it was still up there, night after night. So what was holding it up?"*), the underscore is a cold, thin, metallic electronic synth drone with digital bell pings. Over the 3-second fade into `178.28 s` (entering *"Newton's answer was so simple it is easy to miss. The Moon isn't held up at all. It really is falling."*), a rich, warm, natural studio-sounding acoustic chamber ensemble (`hos_009_teach_v01.mp3`: warm plucked acoustic harpsichord/lute with natural room air and gentle organic strings) abruptly replaces the synth. Both bed-only and VO+bed mixes sound like two completely different productions spliced together at `2:57`.
  - **Level transition (`WARN` / secondary)**: While RMS loudness is matched on paper (`-16.0` vs `-15.1 LUFS`, `0.0 dB` handoff difference), the sudden arrival of rich acoustic harmonic warmth and full stereo room tone in `teach_v01` creates a noticeable perceived fullness jump at `177–179 s`.
- **Verdict**: **`FAIL`** (fails *"seamless ... timbral ... blend from synthesized opening into retained `hos_009_teach_v01.mp3` with no jarring timbral cliff"*).

### D. Part 2 Orchard Colour Shift (`~84.44 s`) — **`FAIL`**

- **What is heard by ear**:
  - At `84.44 s` (*An Apple in a Plague Year*, *"In 1665, a terrible plague swept through England"*), the arrangement shifts harmonically right on the chapter card, **but the shift degrades rather than warms the sound**: the metallic plucked synth jumps an entire octave higher (`84.44–168.00 s`) into piercing upper-mid chimes/pings while the bed steps up roughly `2.2–2.5 dB` in RMS (`-19.2 dBFS` at `83 s` → `-16.7 to -17.8 dBFS` across `85–175 s`, confirmed in `CONTINUITY_v03_synth.json`). Instead of a warmer Woolsthorpe orchard colour, Part 2 sounds sharper, thinner, and more synthetic under Ben's voice than Part 1.
- **Verdict**: **`FAIL`**.

### E. Wonder-to-Teach Contrast (`0.00–176.78 s` vs `176.78–535.33 s`) — **`FAIL` (Timbral Cohesion)**

- Structurally, Parts 1–2 (`~63 BPM` chordal pattern) contrast with Parts 3–5 (`~70 BPM` rhythmic D-minor harpsichord/lute pulse) at the `176.78 s` chapter card. However, because Parts 1–2 sound unmistakably synthetic/electronic while Parts 3–5 sound like a warm acoustic chamber recording, the contrast registers as a **production-quality disconnect** rather than two cohesive moods within one score.
- **Verdict**: **`FAIL`**.

### F. Narration Clarity Under Ben's Voice (`0.00–518.40 s`) — **`PASS` (Intelligibility) / `FLAG` (Parts 1–2 Distraction)**

- **Files auditioned**: All five contiguous parts of `hos_009_reference_mix_0_518s40_v03.wav`:
  - **Part 1 (`0.00–82.54 s`, *"Right now, as you watch this..."* → *"...when the whole country was afraid"*)**: Ben's narration is 100% intelligible with no clipped or masked words at `-20.18 dB` bed gain, **but** the nasal electronic buzz-organ pad and metallic synth plucks sit noticeably in the vocal presence band (`1–3.5 kHz`) and feel artificial behind his voice.
  - **Part 2 (`86.34–176.18 s`, *"In 1665, a terrible plague..."* → *"...So what was holding it up?"*)**: Narration remains fully intelligible, **but** the higher-octave piercing metallic pings and `+2.2 dB` RMS step-up from `84.44 s` onward are noticeably more distracting than Part 1.
  - **Part 3 (`178.68–258.26 s`, *"Newton's answer was so simple..."* → *"...Could he?"*)**: **PASS.** Clean, warm, unobtrusive acoustic chamber accompaniment under Ben's voice.
  - **Part 4 (`262.06–391.96 s`, *"Newton worked out that a pull like this..."* → *"...Halley paid to print it himself"*)**: **PASS.** Clear speech throughout the inverse-square spray-paint explanation, 3,600× Moon test, and Halley's 1684 Cambridge visit (where `teach_v01` naturally thins at `363.28 s`).
  - **Part 5 (`395.76–518.40 s`, *"Newton's law didn't stop at the Moon..."* → *"...in a thin layer of clay"*)**: **PASS.** Spacious thinned accompaniment through the 1758 comet return (`395–427 s`), smooth re-entry of the D-minor harpsichord arpeggio at `428 s` on *"And you can see Newton's cannon at work today. The International Space Station..."*, and crystal-clear closing handoff through `518.40 s`.
- **Verdict**: **`PASS` for speech intelligibility; `FLAG` for Parts 1–2 (`0.00–176.18 s`) synthetic timbral distraction**.

### G. Tempo Fit (`60–66` / `68–72 BPM`) — **`PASS`**

- By ear, `wonder_v03_synth` moves at a calm, unhurried **~`63 BPM`** pulse (within `60–66 BPM`), and retained `teach_v01` moves at a measured **~`70 BPM`** quarter-note pulse (within `68–72 BPM`). The `133.3 BPM` reading in `music_gate_v03_wonder.json` and `music_gate_v03_joined.json` is an onset-autocorrelation subdivision multiple (~`2×` the musical pulse), not a fast tempo.
- **Verdict**: **`PASS`**.

### H. Final Tail Coverage (`518.40–535.33 s` & `526.00 s` Endpoint) — **`PASS`**

- **Files auditioned**: `hos_009_tail_518s40_v03.wav` (`518.40–535.33 s` direct WAV) and `hos_009_reference_endpoint_526s_v03.wav` (`505.00–526.00 s` slice).
- **What is heard by ear**: After Ben's last word (*"...in a thin layer of clay"* at `518.40 s`), retained `teach_v01` carries forward cleanly, thins at `~520 s` into gentle solo plucked acoustic D-minor arpeggio notes, smoothly covers the `526.00 s` reference endpoint with no cut or jump, and decays naturally to silence by `~533 s` through `535.33 s` with zero looping or silence padding.
- **Verdict**: **`PASS`**.

---

## 4. Technical Root-Cause Notes & Handoff to `J3236` (Elected-Chief Disposition)

### Summary Scorecard

| Criterion | Window | Verdict | Key Ear Finding |
|---|---|---|---|
| **SHA-256 parity & locks** | 18 deliverables + preserved locks | **PASS** | `18/18` Mini/NAS SHA-256 exact match; `ACTIVATION_AUTHORIZED = False`; `£0` / `0` credits |
| **Unchanged complete-library `music_gate.py`** | `94` beds (`9` roots / `15` UAT) | **PASS** | `0` fails, `0` unreadable, no waiver (`0.3961` wonder / `0.3868` joined, `< 0.80`) |
| **1. Period chamber musicality & warmth** | `0.00–178.28 s` | **FAIL** | Harsh, buzzy, nasal electronic reed-organ/synth pad + thin metallic MIDI/chiptune Karplus-Strong plucks |
| **2. Continuity (zero dropouts)** | `0.00–178.28 s` & `0.00–535.33 s` | **PASS** | `0` silent dropouts (remediates `v02`'s six `J2807` `< -45 dB` dropouts) |
| **3. `175.28–178.28 s` join quality** | `168.00–186.00 s` (bed & mix) | **FAIL** | Tonal/click-free D-minor crossfade, **but jarring timbral cliff** from metallic synth into warm acoustic `teach_v01` |
| **4. Part 2 orchard colour shift** | `~84.44–168.00 s` | **FAIL** | Extra `+12` semitone octave jump + `+2.2–2.5 dB` RMS bump turns Part 2 sharper/more piercing instead of warmer |
| **5. Wonder-to-teach contrast** | `0.00–535.33 s` | **FAIL** | Reads as electronic synth vs studio acoustic recording rather than unified chamber moods |
| **6. Narration clarity under Ben** | `0.00–518.40 s` (5 parts) | **PASS / FLAG** | 100% intelligible across all 5 parts; Parts 1–2 synth timbre distracts in `1–3.5 kHz`; Parts 3–5 clean **PASS** |
| **7. Tempo fit (`60–66` / `68–72 BPM`)** | `0.00–535.33 s` | **PASS** | `~63 BPM` wonder / `~70 BPM` teach by ear (`133.3 BPM` gate value is `2×` subdivision) |
| **8. Tail coverage (`526 s` / `535.33 s`)** | `518.40–535.33 s` | **PASS** | Warm acoustic D-minor decay past `518.40 s` VO end through `526.00 s` and `535.33 s` |

### Why `v03_synth` Sounded Synthetic (for `J3236` Fallback Evaluation)

Inspection of `_build_hos009_wonder_v03_synth.py` (lines `207–315`) explains every ear artifact directly:
1. `bowed()` (`L239–249`) is a 4-harmonic static additive sine organ (`sin + 0.32 sin2 + 0.10 sin3 + 0.035 sin4`) with uniform sinusoidal vibrato and fixed broadband noise — no wooden body formant EQ, no bow-stroke dynamics, and no ensemble micro-detuning, producing the nasal electronic reed-organ buzz.
2. `karplus()` (`L207–229`) uses an integer-sample delay (`int(round(SR/freq))`, causing slight pitch quantization at upper pitches), a single-pass 2-point loop filter with high decay (`0.988–0.991`), and peak normalization (`y / peak`), placed on a rigid exact half-beat clock grid (`t += half`) with zero timing/velocity humanization — producing the metallic MIDI/chiptune ping quality.
3. At `t >= ORCHARD` (`84.44 s`, `L291–292`), `midi += 12` pushes the Karplus-Strong plucks an extra octave higher (`+24` semitones above the chord tones) while adding an upper `bowed()` harmonic (`L276`), creating the piercing upper-mid timbre and `+2.2–2.5 dB` RMS step-up in Part 2.

### Handoff to `J3236` (Elected HOS Chief)

- **No score acceptance is granted in `J3235`**, HOS PR `#697` (`J3234`) is **not** approved for acceptance, and **`J2035` (long assembly) / `J2171` (Shorts A/B) remain held (`blocked`)**.
- Under `SCORE_SCOPE_J3233.json`'s pre-decided bounded fallback, `J3236` (elected HOS Chief) must now refuse acceptance of `v03_synth` and choose between:
  - **(i) At most ONE bounded `£0` DSP/timbre revision** (`v04_synth` — or a full-runtime `0–535.33 s` own-synthesis bed if join timbre mismatch against studio-acoustic `teach_v01` cannot be bridged by pure NumPy DSP; note candidly from ear audition that pure Python/NumPy synthesis matching the acoustic realism of `teach_v01` is genuinely difficult without real instrument acoustics), **OR**
  - **(ii) Escalating one single explicit billing/pricing confirmation question to Ben** for ElevenLabs `music_v2` (confirming single-request credit bound & `£0` cash under his Creator plan) so a studio-quality acoustic opening can match retained `hos_009_teach_v01.mp3`.
