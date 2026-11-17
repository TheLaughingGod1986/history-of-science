# HOS 009 Score Disposition — J2808 (`hos_009_wonder_v02.mp3` & `hos_009_score_joined_v02.wav`)

- **Film**: `009_The-Falling-Moon-Gravity` (*Why Doesn't the Moon Fall to Earth?*, air date Thu 26 Nov 2026 18:00 London, `ready_by` 22 Nov 2026)
- **Job**: `J2808` (`HOS 009: decide revised score acceptance or bounded failure route`)
- **Acting Chief**: `gemini` (`Grok -> Claude -> Codex -> Gemini`; `chief_relay.py status` rechecked before decision: `chief` Grok Bot down, `claude` out of usage until `2026-11-18T07:50:00Z`, `codex` down until `2026-11-17T23:22:00Z`, `gemini` UP)
- **Date**: 17 Nov 2026
- **Spend**: `£0.00` cash, `0` subscription credits, `0` requests, `0` extra takes
- **Listening Claim in `J2808`**: None (`capabilities: []` recorded at `J2808` session start; all musical/audition evidence is read from the completed `J2807` multimodal `audio_input` ear review `EAR_REVIEW_J2807.md` and prior `J2783` ear review `EAR_REVIEW_J2783.md`, never inferred from waveforms or measurements)
- **Disposition Verdict**: **NOT ACCEPTED (`HOLD` — `J2035` and `J2171` remain held; no compliant route presently available under `J2805`/`J2808` constraints)**

---

## 1. Evidence Read & Verified

1. **`05_Music/SCORE_SCOPE_J2805.json` (`sha256: 1298c09d6b6000e474bd5e359a767272edd63f452c5d4171872e1ec29d3269b1`) & `SCORE_DECISION_J2805.md` (HOS PR #633, merged `1725198c`)**:
   - Authorized **one** 180-second `music_v2` opening cue (`hos_009_wonder_v02.mp3`), `1` request, `1` take, `0` retries, `3,000` subscription-credit cap, `£0` cash, retaining `hos_009_teach_v01.mp3` (`sha256: 4c1f0a17364ad5ba96fdd2d42730b2f857d19017fab52b221701bd4e15d07bb1`) from `175.28 s` to `535.33 s` with a 3-second equal-power crossfade (`175.28–178.28 s`, centred on the `176.78 s` cannon chapter card).
   - Required **both** unchanged production `music_gate.py` over the complete current library (`>= 77` comparisons, `0` unreadable) **and** a capable `audio_input` ear review (`J2807`) to pass before `J2808` could accept the score and release `J2035`.
   - Explicitly barred any second take, loop, silent padding, timing alteration, gate-evasion filtering, favourable excerpt selection, waiver, unchanged verification loop, or deployment of `PR908`.

2. **`05_Music/J2806_PROVENANCE.json` & `05_Music/music_gate_j2806.json` (HOS PR #636, merged)**:
   - **Pre-spend guards & spend**: **PASS** (`1` request, `0` retries, `2,475 <= 3,000` subscription credits spent, `£0` cash, `0` overage, `77,389` subscription credits remaining after POST, extension limits `0`/`false`).
   - **Exact SHA-256 parity & preserved locks**: **PASS**. All 12 preserved locks (`hos_009_wonder_v01.mp3` `95dfe11d...`, `hos_009_teach_v01.mp3` `4c1f0a17...`, `hos_009_score_joined_v01.wav` `d7f5bf3d...`, 5 `v01` stems, `VO_TAKES_KEEP.json` `530743c5...`, `VO_RETIME_v01.json` `75a2e7af...`, `code_graphic_009_p4_05_minute_second.mp4` `e35f9a98...`, `J2632_r4/code_graphic_009_p3_01_really_falling_c1.mp4` `23c832b0...`) and all 12 `v02` deliverables (`hos_009_wonder_v02.mp3` `b38ae892...`, `hos_009_score_joined_v02.wav` `6fc8628a...`, 5 `v02` stems, 4 `audio_review_j2806/*.wav` artifacts) verified byte-for-byte across the Mini checkout and `/Volumes/data/studio-live/History Of Science/02_Video-Projects/009_The-Falling-Moon-Gravity/`.
   - **Complete-library unchanged production `music_gate.py`**: **PASS**
     - `verdict: "PASS"`, `library_state: "complete"`, `comparison_count: 89` (`>= 77` minimum historical inventory), `unreadable_warn_count: 0`, `fail: []`, `matches: []`, `waived: []`, `waiver: null`.
     - All 9 library roots scanned; all 15 iCloud UAT tracks (`icloud-uat/HOS UAT` and `icloud-uat/OWB UAT`, including `jupiter-music.mp3` `38ab6e3e8768`, similarity `0.3059`) materialized and hash-verified.
     - Top joined `v02` similarities (`< 0.80` fail threshold): `0.6615` (`hos_002_part01_curious_workshop_v02_norm.wav`), `0.6359` (`v01_norm`), `0.5822` (`moon-leaving-part02_score_bed_v01.mp3`, down from `0.821` in `v01`), `0.5610` (`nearest-star_score_bed_v01.mp3`).
     - Top `wonder_v02`-only similarity: `0.4822` (`lightning008_score_bed_v01_take.mp3`).

3. **`05_Music/EAR_REVIEW_J2807.md` (HOS PR #637, merged `dda3ba3f`)**:
   - **What passed by ear in `J2807`**:
     - `175.28–178.28 s` cannon chapter-card crossfade (`168.00–186.00 s` bed & VO mix): **PASS by ear** (quiet `D4/A4` bowed open fifth tapering into the `D`-minor harpsichord/lute arpeggio of `teach_v01` in the same `D` tonal center; zero click, phase dip, or rhythmic clash).
     - Tempo (`171.4 BPM` gate warning vs `60–72 BPM` brief): **PASS by ear** (`wonder_v02` is slow rubato `~55–60 BPM`; `teach_v01` moves at a calm `~70 BPM` quarter-note pulse in D minor; `171.4 BPM` is onset-detector subdivision counting of rapid plucked harpsichord notes).
     - Wonder/teach contrast, Parts 3–5 continuity (`175.28–535.33 s`), speech clarity across all 5 locked VO parts (`0.00–518.40 s` at `-16.0 dB` bed gain), and tail coverage past `518.40 s` VO end and `526.00 s` reference master endpoint (`hos_009_reference_endpoint_526s_v02.wav` / `535.33 s` stem end): **PASS by ear**.
   - **Exact Blocker — Why `J2807` Failed `wonder_v02` (`0.00–178.28 s`) by Ear**:
     - **Six `< -45 dB` inter-phrase silent dropouts (`0.61–2.29 s` dead air) across `18.95–97.92 s` (Part 1 and early Part 2)**:
       1. `18.95–21.00 s` (`2.05 s` silent dropout in Part 1 under *"showed that the pull that drops an apple..."*)
       2. `66.48–67.83 s` (`1.35 s` silent dropout in Part 1 after *"You would see the Moon rise over the fields, huge and silent."*)
       3. `73.04–75.33 s` (`2.29 s` silent dropout in Part 1 under *"Would you ever think that the stone and the Moon..."*)
       4. `81.70–82.84 s` (`1.15 s` silent dropout at Part 1 end after *"...when the whole country was afraid"*)
       5. `88.91–90.39 s` (`1.48 s` silent dropout in early Part 2 under *"To keep students safe, the university at Cambridge..."*)
       6. `97.31–97.92 s` (`0.61 s` silent dropout in early Part 2; plus `~0.6–0.7 s` bow-breath dips at `37.20–37.90 s`, `51.80–52.40 s`, `59.80–60.40 s`).
     - **Missing gut-string lute (`FLAG`)**: `wonder_v02` is played solely by bowed chamber strings (`viol/violin/viola/cello`) with no plucked gut-string lute despite the prompt.
     - **Causal mechanism**: `SCORE_SCOPE_J2805.json`'s prompt stated *"Wonder comes from space between short, gently changing phrases and warm harmony, not a continuous bass drone."* ElevenLabs `music_v2` interpreted *"space between short, gently changing phrases"* as full rests between bowed-string chord swells during `0.00–97.92 s` (ignoring *"Keep a quiet audible musical bed beneath the sparse phrases"*), before playing connected overlapping phrases across `97.92–178.28 s`. Although each pause is under `music_gate.py`'s `6.0 s` numeric gap threshold, six `0.61–2.29 s` dead-air dropouts violate `studio/RULES.md` Polish pass §2 (*"The music covers the full runtime, never drops out"*) and `SCORE_SCOPE_J2805.json` acceptance criteria.

---

## 2. Disposition & Why No Compliant Route Is Presently Available

1. **Score Acceptance Refused (`HOLD`)**:
   - Because `EAR_REVIEW_J2807.md` recorded a concrete ear review **FAIL** on `wonder_v02` continuous bed coverage (`18.95–97.92 s` silent dropouts) and `SCORE_SCOPE_J2805.json` / `J2808` require both the complete-library `music_gate.py` and the capable ear review to pass without waiver, **`hos_009_score_joined_v02.wav` is NOT accepted**.
   - Both **`J2035`** (long assembly; retaining recorded `2026-11-15T18:00:00Z` / refreshed `2026-11-18T18:00:00Z` deadline metadata) and **`J2171`** (Shorts A/B assembly) remain **held (`blocked`)**.

2. **Why No Compliant Route Is Presently Available Under `J2805`/`J2808` Constraints**:
   - **Candidate `v01` (`hos_009_score_joined_v01.wav`, `sha256: d7f5bf3d...`) is blocked by `music_gate.py`**: It passed `J2783` ear review (`0` dropouts, continuous opening viol drone + sparse lute plucks), but failed unchanged production `music_gate.py` (`0.821` vs OWB 013 `moon-leaving-part02` and `0.804/0.811` vs HOS 002 `curious_workshop` on `0–21 s`). Prototype `PR908` failed `J2803` validation (`0.693` on 0.37s trim, `0.633` on combined transform) and cannot be deployed (`J2805`/`J2808`). Waiving `music_gate.py` is prohibited.
   - **Candidate `v02` (`hos_009_score_joined_v02.wav`, `sha256: 6fc8628a...`) is blocked by `EAR_REVIEW_J2807.md`**: It passed unchanged 89-bed `music_gate.py` (`0` fails, max similarity `0.6615 < 0.80`) and passed ear review on `97.92–535.33 s` (including the `175.28–178.28 s` crossfade and `teach_v01`), but failed `J2807` ear review on six `0.61–2.29 s` `< -45 dB` inter-phrase silent dropouts in `18.95–97.92 s` of `wonder_v02`. Waiving `EAR_REVIEW_J2807.md` is prohibited.
   - **Post-hoc audio editing / hybrid splicing of `v01` and `v02` is barred**: `SCORE_SCOPE_J2805.json` explicitly prohibits *"loop, silent padding, timing alteration, gate-evasion filtering or favourable excerpt selection"*, ruling out looping the continuous `97.92–178.28 s` half of `wonder_v02`, splicing `wonder_v02` (`0–18.95 s`) with `wonder_v01` (`21.00–178.28 s`), or filtering `wonder_v01` to reduce its `0–21 s` cosine score.
   - **No extra take is authorized by `J2808`**: `J2808` explicitly states *"No extra take is authorized by this job; do not repeat unchanged verification or deploy PR908."*
   - Consequently, **no compliant route is presently available within `J2808`'s no-extra-take, no-edit, no-waiver, no-`PR908` boundaries**. Unblocking HOS 009 `05_Music` requires an explicit desk `#180` Chief/owner decision beyond `J2808`'s authority (such as authorizing a new bounded `wonder_v03` single-take scope that removes the *"space between short, gently changing phrases"* prompt wording and mandates unbroken continuous lute/viol arpeggiation with zero rests, or a desk ruling on `v01` vs `v02`). No generic verification loop is queued.
