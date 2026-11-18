# HOS 009 Revised Continuous Opening Score Scope — J3042 (`wonder_v03` Proposal for `J3043` Elected-Chief Review)

- **Film**: `009_The-Falling-Moon-Gravity` (*Why Doesn't the Moon Fall to Earth?*, air date Thu 26 Nov 2026 18:00 London, `ready_by` 22 Nov 2026)
- **Job**: `J3042` (`HOS 009: revise opening music scope after silent phrase gaps`, `--kind review`, 20-minute text-work budget)
- **Author**: `gemini` (`Gemini 4 Argon (High)`, specialist worker on the Mac mini; no Chief authority claimed)
- **Predecessor Rulings**: `J3038` (`jobs/reviews/J3038/REVIEW.md`, condition `NOT MET`), `J2808` (`05_Music/SCORE_DISPOSITION_J2808.json` & `.md`, `NOT_ACCEPTED_HOLD`), `J2807` (`05_Music/EAR_REVIEW_J2807.md`, `FAIL_BY_EAR`), `J2805` (`05_Music/SCORE_SCOPE_J2805.json`, `sha256: 1298c09d6b6000e474bd5e359a767272edd63f452c5d4171872e1ec29d3269b1`)
- **Queued Elected-Chief Successor**: `J3043` (`HOS 009: decide revised continuous opening score scope`, `--kind chief`, `after: J3042`)
- **Spend / Media / Listening Claim in `J3042`**: `£0.00` cash, `0` credits, `0` requests, `0` media changes, `0` YouTube/Buffer changes, and **no hearing claim** (`capabilities: []` recorded at session start; all acoustic/ear references cite completed `J2783` and `J2807` reports). This is a **scope proposal only**, not a spend release.

---

## 1. Exact Diagnosis of Both Earlier Failure Modes (`v01` and `v02` Remain Failed)

| Candidate | Unchanged `music_gate.py` (`89` beds across all 9 roots + 15 UAT tracks) | Demonstrated `audio_input` Ear Review (`J2783` / `J2807`) | Root Cause in Prompt / Generation | Status |
|---|---|---|---|---|
| **`v01` (`J2664` / `J2783`)**<br>`hos_009_wonder_v01.mp3` (`95dfe11d...`)<br>`hos_009_score_joined_v01.wav` (`d7f5bf3d...`) | **FAIL** (`0.821` vs OWB 013 `moon-leaving-part02`, `0.804/0.811` vs HOS 002 `curious_workshop` on `0–21 s`; `PR908` failed `J2803` validation at `0.693`/`0.633` and remains undeployed) | **PASS** (`J2783`: continuous sustained bowed-viol drone with sparse lute plucks; `0` silent dropouts) | `J2663` prompted for *"warm viol drone, sparse plucks"*, producing a static sustained low bass-drone opening across `0–21 s` whose spectral/envelope profile matched earlier drone-led openings above the `0.80` cosine ceiling. | **FAILED (preserved byte-for-byte)** |
| **`v02` (`J2806` / `J2807`)**<br>`hos_009_wonder_v02.mp3` (`b38ae892...`)<br>`hos_009_score_joined_v02.wav` (`6fc8628a...`) | **PASS** (`89` comparisons, `0` unreadable, `0` fails, max joined similarity `0.6615 < 0.80`, max `wonder_v02` similarity `0.4822 < 0.80`) | **FAIL_BY_EAR** (`J2807`: passed `175.28–178.28 s` D-minor crossfade, tempo `~55–60`/`~70 BPM`, VO clarity `0.00–518.40 s`, and `526.00 s`/`535.33 s` tail, but **FAILED `wonder_v02` (`0.00–178.28 s`)** on **six `0.61–2.29 s` `< -45 dB` inter-phrase silent dropouts** across `18.95–97.92 s` plus missing gut-string lute `FLAG`) | `SCORE_SCOPE_J2805.json` prompted *"Wonder comes from space between short, gently changing phrases and warm harmony, not a continuous bass drone. Keep a quiet audible musical bed beneath the sparse phrases."* ElevenLabs `music_v2` interpreted *"space between short, gently changing phrases"* literally as full rests / fade-to-silence between 15 discrete bowed-string chord swells across `0.00–97.92 s` (`18.95–21.00 s` [`2.05 s`], `66.48–67.83 s` [`1.35 s`], `73.04–75.33 s` [`2.29 s`], `81.70–82.84 s` [`1.15 s`], `88.91–90.39 s` [`1.48 s`], `97.31–97.92 s` [`0.61 s`]). | **FAILED (`J2808` `NOT_ACCEPTED_HOLD`, preserved byte-for-byte)** |

---

## 2. Exact Prompt Revisions for `wonder_v03` Addressing Both Failure Modes

### Removed from `J2805` Prompt
- Removed: `"Wonder comes from space between short, gently changing phrases and warm harmony, not a continuous bass drone."`
- Removed: `"Keep a quiet audible musical bed beneath the sparse phrases, with subtle variation in register and voicing."`

### Replaced With in `SCORE_SCOPE_J3042.json` (`wonder_v03`)
```text
Original instrumental opening underscore exclusively for HOS 009 The Falling Moon, Newton connecting an apple with the Moon. Intimate 17th-century period chamber music for soft plucked gut-string lute and warm bowed viols in D minor and related modal harmony, with continuously overlapping instrumental parts and quiet audible accompaniment from the first second to the last. As each viol line tapers, gentle lute arpeggios or a companion viol voice are already sounding underneath so the harmonic weave never drops out, pauses, or fades to silence. Harmonic progression and register shift gently from bar to bar with no static bass-drone opening. Breathing room for British narration comes from restrained dynamics, soft articulation, and warm low-to-mid register, never from rests, caesuras, or silence between phrases; no solo lead melody. Begin softly and immediately in full continuous chamber texture with no fade-in, swell, or sting. Around 84 seconds, warm into an intimate Woolsthorpe orchard colour while keeping unbroken overlapping lute and viol accompaniment. End on a quiet, continuous sustained D-minor harmonic handoff suitable for a three-second equal-power crossfade into the existing D-minor harpsichord teach cue.
Pace: 60-66 BPM, flowing continuous chamber motion; no driving ostinato and no silent pauses.
NOT any earlier HOS or Orbit bed, the previous HOS009 wonder cues, jupiter-music.mp3, silent gaps or rests between phrases, isolated chord swells fading to silence, static or sustained bass-drone opening, cosmic shimmer, piano space-documentary music, solo woodwind workshop waltz, borrowed melody, named-composer imitation, heroic brass, horror, vocals, lyrics, pop drums, EDM or comedy stings.
```

### How Every Constraint Is Met
1. **Eliminates `v02`'s inter-phrase silent dropouts (`18.95–97.92 s`)**:
   - Explicitly replaces *"space between short, gently changing phrases"* with *"continuously overlapping instrumental parts and quiet audible accompaniment from the first second to the last. As each viol line tapers, gentle lute arpeggios or a companion viol voice are already sounding underneath so the harmonic weave never drops out, pauses, or fades to silence."*
   - Explicitly defines narration breathing room as *"restrained dynamics, soft articulation, and warm low-to-mid register, never from rests, caesuras, or silence between phrases"*.
   - Adds *"no silent pauses"* to `Pace:` and *"silent gaps or rests between phrases, isolated chord swells fading to silence"* to `NOT`.
2. **Fixes `v02`'s missing lute (`FLAG`)**:
   - Explicitly pairs *"soft plucked gut-string lute and warm bowed viols"* in both the opening texture and the `84 s` Woolsthorpe orchard section (*"gentle lute arpeggios or a companion viol voice are already sounding underneath"*).
3. **Prevents `v01`'s `0–21 s` reuse-detector match (`0.821`)**:
   - Retains the ban on any static or sustained bass-drone opening (*"Harmonic progression and register shift gently from bar to bar with no static bass-drone opening"*, *"NOT ... static or sustained bass-drone opening"*) and keeps `60–66 BPM` chamber motion with no lead melody and no driving ostinato.
4. **Preserves the verified `175.28–178.28 s` D-minor join & `teach_v01`**:
   - Keeps `hos_009_teach_v01.mp3` (`sha256: 4c1f0a17364ad5ba96fdd2d42730b2f857d19017fab52b221701bd4e15d07bb1`) untouched from `175.28 s` to `535.28 s`, the 3-second equal-power crossfade (`175.28–178.28 s`, centred on the `176.78 s` cannon chapter card), the D-minor harmonic handoff, all 5 locked VO parts (`0.00–518.40 s`), all approved Flow plates and `J2631`/`J2632` diagram locks, and full tail coverage past `518.40 s` VO end and `526.00 s` reference master endpoint (`535.28 s` available stem end).

---

## 3. Bounded Request Cap, Billing Guards, & Verification Chain (For `J3043` Review)

1. **Single Bounded Request Proposal (No Spend Released by `J3042`)**:
   - **Tool**: `04_Audio/tools/generate_music_bed.py` via `el_client` / `el_guard` on the Mac mini.
   - **Model**: `music_v2` (`force_instrumental: true`).
   - **Allowance (only upon `J3043` approval and merge of this PR)**: At most **1 request**, **1 take**, **180 seconds** (`180,000 ms`), **`<= 3,000` ElevenLabs subscription credits**, **`£0.00` cash**, **`0` overage**, **`0` retries**.
   - Every `J2805` pre-spend guard applies unchanged: verify live subscription balance, duration-based worst-case tariff for 180 seconds, `TTS_PAUSE` absent, one-recorder lock held, `can_extend_character_limit: false`, `allowed_to_extend_character_limit: false`, `current_overage_amount: 0`, and `worst_case_charge <= min(3000, live_remaining - pending)`. Any unknown, missing, or contradictory billing field halts before `POST`.
2. **Preservation & Provenance**:
   - Preserve all `v01` and `v02` audio files, stems, plans, gate JSONs, and ear/disposition reports byte-for-byte on both the Mini and `/Volumes/data/studio-live/History Of Science/02_Video-Projects/009_The-Falling-Moon-Gravity/`.
   - Write `v03` outputs (`hos_009_wonder_v03.mp3`, `hos_009_score_joined_v03.wav`, 5 part stems `_v03.wav`, and `168–186 s` / full reference mix `_v03.wav`) alongside full SHA-256 provenance and Mini/NAS parity checks.
3. **Complete-Library Unchanged `music_gate.py` + Explicit Timestamped Silence/Continuity Evidence**:
   - Run unchanged production `music_gate.py` over the complete current library (`>= 89` comparisons across all 9 roots including all 77+ historical beds and all 15 hash-verified iCloud UAT tracks, `0` unreadable, `< 0.80` similarity; no waivers, no loops/patches/filtering/padding, no `PR908` deployment).
   - Record **explicit timestamped silence/continuity telemetry** on `hos_009_wonder_v03.mp3` (`0.00–180.04 s`) and `hos_009_score_joined_v03.wav` (`0.00–535.33 s`), including `ffmpeg silencedetect=noise=-45dB:d=0.25` and `d=0.50` plus 1-second RMS window floor table across `0.00–178.28 s` confirming zero inter-phrase silent dropouts.
4. **Fresh Demonstrated `audio_input` Ear Review & Elected-Chief Acceptance**:
   - A reviewer with fresh demonstrated `audio_input` capability auditions `hos_009_wonder_v03.mp3`, `hos_009_score_joined_v03.wav`, the `168.00–186.00 s` transition (bed and VO+bed mix), the 5-part locked-VO reference mix (`0.00–518.40 s`), and the tail (`518.40–535.33 s` / `526.00 s` endpoint).
   - Elected-Chief score acceptance is required before `J2035` (long assembly) and `J2171` (Shorts A/B assembly) can leave their `blocked` state. No duplicate successor jobs are created by `J3042`; `J3043` is already queued in `jobs/QUEUE.json` (`after: J3042`).
