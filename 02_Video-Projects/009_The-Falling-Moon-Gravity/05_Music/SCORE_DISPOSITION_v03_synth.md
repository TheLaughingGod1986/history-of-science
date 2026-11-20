# HOS 009 Score Disposition — J3236 (`hos_009_wonder_v03_synth.wav` & `hos_009_score_joined_v03.wav`)

- **Film**: `009_The-Falling-Moon-Gravity` (*Why Doesn't the Moon Fall to Earth?*, historical internal air target `Thu 26 Nov 2026`, `ready_by: 2026-11-22` at risk)
- **Job**: `J3236` (`HOS 009: Chief score disposition for own-score v03_synth`, `--kind chief`, `ref: J3233`)
- **Acting Chief**: `gemini` (`Grok -> Claude -> Codex -> Gemini`; `chief_relay.py status` rechecked immediately before protected actions: `claude` down until `2026-11-20T17:50:00Z`, `chief` Grok Bot down until `2026-11-20T17:33:46Z`, `codex` down until `2026-11-20T16:12:29Z`, `gemini` UP as elected HOS Chief)
- **Date**: `2026-11-20`
- **Spend & API Calls**: `£0.00` cash, `0` subscription credits, `0` account GETs, `0` ElevenLabs POSTs
- **Session Capability**: Demonstrated `audio_input` recorded via `chief_relay.py capabilities --agent gemini --available "audio_input"` (directly auditioned `hos_009_transition_168_186_bed_v03.wav` plus 12 s reference excerpts of shipped £0 own-synthesis beds HOS 006 `trees006_score_bed_v01.mp3` and HOS 007 `vaccine_score_bed_v01.mp3` to inform the bounded fallback choice; independent full-score ear review remains `J3235` `EAR_REVIEW_v03_synth.md`).
- **Disposition Verdict**: **`NOT ACCEPTED (REFUSED — BOUNDED FALLBACK OPTION (i) INVOKED: ONE FINAL £0 FULL-RUNTIME WARM OWN-SYNTHESIS REVISION v04_synth)`**

---

## 1. Independent Gate & Evidence Verification (No Waivers)

| Gate / Criterion | Independent Verification Result | Verdict |
|---|---|---|
| **Production script provenance (`J3234`, HOS PR `#697`)** | Merged strictly as rejected-attempt audit provenance (`03042715`, head `fd6b4174c41f2039804d57ba9d4d9c42ded59c52`, 5/5 CI green). Audited `_build_hos009_wonder_v03_synth.py` (`bd8e20d98f87...`): deterministic pure Python/NumPy, zero third-party samples, zero GPL/system soundfonts (`TimGM6mb.sf2` / `gs_instruments.dls` absent), zero network/API calls, `£0` / `0` credits. | **PASS (Audit Only)** |
| **Exact Mini & NAS SHA-256 parity** | Independently hashed all 18 `v03` deliverables plus `PROVENANCE_v03_synth.json` (`96e77084b125...`) across Mini and `/Volumes/data/studio-live/History Of Science/02_Video-Projects/009_The-Falling-Moon-Gravity/05_Music/`: `19/19` exact match (`ALL_V03_PARITY=True`). | **PASS** |
| **Preserved locks & hard guardrails** | Independently verified all 9 locks unchanged: `hos_009_teach_v01.mp3` (`4c1f0a17...`), `wonder_v01` (`95dfe11d...`), `score_joined_v01` (`d7f5bf3d...`), `wonder_v02` (`b38ae892...`), `score_joined_v02` (`6fc8628a...`), `VO_TAKES_KEEP.json` (`530743c5...`), `VO_RETIME_v01.json` (`75a2e7af...`), `J2631` (`e35f9a98...`), `J2632_r4` on NAS (`23c832b0...`). Verified `04_Audio/tools/hos009_score_flight.py` retains literal `ACTIVATION_AUTHORIZED = False`. | **PASS** |
| **Unchanged complete-library `music_gate.py`** | Verified `orbit-with-ben/scripts/music_gate.py` SHA-256 `62b5159f95598eaca5256b30ba66144812bad97dc86fd0c9de4618e4a1dd5385` matches both `music_gate_v03_wonder.json` (`PASS`, `94` comparisons across all 9 roots including 15 materialized UAT tracks, `0` unreadable, max `0.3961 < 0.80`, `0` fails, no waiver) and `music_gate_v03_joined.json` (`PASS`, `94` comparisons, `0` unreadable, max `0.3868 < 0.80`, `0` fails, no waiver). | **PASS** |
| **Continuity telemetry (`0.00–178.28 s`)** | Independently ran `ffmpeg silencedetect=noise=-45dB:d=0.25` and `d=0.50` on `hos_009_wonder_v03_synth.wav`: `[]` / `[]` (`0` interior dropouts; matches `CONTINUITY_v03_synth.json`, min 1-s RMS `-20.38 dBFS`). | **PASS** |
| **Independent demonstrated-audio ear review (`J3235`, HOS PR `#698`)** | `EAR_REVIEW_v03_synth.md` (distinct reviewer `gemini` vs producer `cursor`, fresh demonstrated `audio_input` session `60ec1c3b-afa8-4115-914c-ca6d29a04973`) returned explicit **`FAIL — DO NOT ACCEPT`** on: (1) period chamber musicality & warmth (`0.00–178.28 s`: harsh/buzzy reed-organ `bowed()` pad + metallic MIDI/chiptune `karplus()` plucks), (2) `175.28–178.28 s` join quality (jarring timbral cliff into warm studio-acoustic `teach_v01`), (3) Part 2 `~84.44 s` orchard shift (`+12` semitone octave jump & `+2.2–2.5 dB` RMS bump turned sharper/piercing), and (4) wonder-to-teach cohesion (`0.00–535.33 s`), plus `FLAG` on Parts 1–2 `1–3.5 kHz` timbral distraction under Ben's voice. Confirmed directly by Chief audition on `hos_009_transition_168_186_bed_v03.wav`. | **FAIL (BLOCKING)** |

---

## 2. Disposition Ruling & Bounded Fallback Choice

1. **Formal Refusal of `v03_synth`**:
   - Because independent `audio_input` ear review (`J3235`) **FAILED** four rubric criteria without waiver, **`hos_009_wonder_v03_synth.wav` and `hos_009_score_joined_v03.wav` are NOT ACCEPTED**.
   - Both **`J2035`** (long assembly; also separately awaiting `J2632` r4 falling-Moon diagram picture KEEP on PR `#543`) and **`J2171`** (Shorts A/B assembly) remain **held (`blocked`)**.
   - Neither `v01`, `v02`, nor `v03_synth` may be used for assembly.

2. **Selection Between Bounded Fallback Options `(i)` and `(ii)` (`SCORE_SCOPE_J3233.json`)**:
   - **Selected: Option `(i)` — ONE AND FINAL bounded £0 full-runtime (`0.00–535.33 s`) warm own-synthesis revision (`v04_synth`, `hos_009_score_v04_synth.wav`)**, modeled on the proven shipped HOS 006 (`trees006_score_bed_v01.mp3`, `_build_trees006_audio_v01.py`) and HOS 007 (`vaccine_score_bed_v01.mp3`) warm own-synthesis architecture.
   - **Why full-runtime warm `v04_synth` over splicing a `v04` opening into `teach_v01` or escalating to Ben right now**:
     1. Direct ear comparison of `hos_009_transition_168_186_bed_v03.wav` against shipped HOS 006 (`55–67 s`) and HOS 007 (`95–107 s`) shows that `v03_synth`'s failure came from **two avoidable causes**: (a) harsh 4-harmonic buzz + broadband hiss + metallic integer-delay Karplus-Strong pings + a Part 2 `+24` semitone octave jump in `_build_hos009_wonder_v03_synth.py`, and (b) splicing pure NumPy synthesis directly into studio-recorded acoustic `hos_009_teach_v01.mp3` at `175.28–178.28 s`.
     2. Shipped HOS 006 and HOS 007 both use a **single cohesive full-runtime warm low-harmonic pure-NumPy score** (`sin + <=0.14*sin2 + <=0.035*sin3` warm pads + clean soft exponential-decay harp tones, smooth 3.0 s chapter-card mood transitions, zero metallic Karplus-Strong artifacts, zero synth-to-recording timbral cliff) at `£0` / `0` credits and passed ear review and Ben's watch.
     3. Under Ben's standing order (11 Nov 2026: *"All I'll do is UAT films. All the other decisions, use your team of agents to come up with the best course"*), the team must exhaust this single bounded proven £0 HOS house method before interrupting Ben with an ElevenLabs billing/pricing escalation.
   - **Hard Terminal Cap (NO `v05_synth` ALLOWED)**:
     - `v04_synth` is strictly the **ONE AND FINAL £0 synthesis attempt**.
     - If `v04_synth` fails either unchanged complete-library `music_gate.py` or independent `audio_input` ear review (`J3240`), then **`J3241` MUST refuse acceptance, MUST NOT authorize `v05_synth`, and MUST immediately invoke Option `(ii)`** — escalating one single explicit billing/pricing confirmation question to Ben for ElevenLabs `music_v2` (confirming single-request subscription credit max `<= 3,000` and `£0` cash under his Creator plan so an acoustic studio opening can match retained `hos_009_teach_v01.mp3`).

---

## 3. Queued Final Bounded Fallback Chain (`SCORE_SCOPE_v04_synth.json`)

1. **`J3239`** (`--kind assembly`, Mini, due `2026-11-21T06:00:00Z`): Synthesize unified full-runtime `0.00–535.33 s` warm D-minor chamber score `hos_009_score_v04_synth.wav` (`_build_hos009_score_v04_synth.py`), 5 part stems, audition clips (`audio_review_v04_synth/`), continuity telemetry (`0` `< -45 dB` dropouts across `0.00–526.00 s`, balanced `<= 1.0 dB` per-part loudness), unchanged complete-library `music_gate.py` (`>= 89` comparisons, `0` unreadable, `< 0.80`, no waiver), Mini/NAS SHA-256 parity, HOS PR.
2. **`J3240`** (`--kind review`, `--requires audio_input`, Mini, `after: J3239`, due `2026-11-21T10:00:00Z`): Independent demonstrated-audio listening review by a distinct worker seat across full `0.00–535.33 s` bed, all 4 chapter transitions (`84.44 / 176.78 / 260.16 / 393.86 s`), full 5-part VO+bed mix (`0.00–518.40 s`), and `518.40–535.33 s` / `526.00 s` tail; commit `05_Music/EAR_REVIEW_v04_synth.md` via HOS PR.
3. **`J3241`** (`--kind chief`, Mini, `after: J3240`, due `2026-11-21T12:00:00Z`): Final elected-Chief disposition on `v04_synth` — accept if all gates and independent ear review PASS (then check remaining `J2035` prerequisites including `J2632` picture KEEP before any release), OR immediately escalate Option `(ii)` billing/pricing confirmation to Ben with zero further synthesis retries.

---

## 4. Unconditional Guardrails Preserved

- `£0.00` cash, `0` subscription credits, `0` account GETs, `0` ElevenLabs POSTs.
- `ACTIVATION_AUTHORIZED` in `04_Audio/tools/hos009_score_flight.py` remains literal `False`.
- `J3043`/`J3045` allowance remains permanently closed unused (`J3047`).
- `v01`/`v02` remain rejected (`J2808`); `v03_synth` is now formally rejected (`J3236`).
- `hos_009_teach_v01.mp3` (`4c1f0a17...`) remains preserved untouched byte-for-byte on Mini and NAS (never looped, stretched, or deleted).
- `J2035` and `J2171` remain held (`blocked`); no YouTube, Buffer, or schedule changes.
