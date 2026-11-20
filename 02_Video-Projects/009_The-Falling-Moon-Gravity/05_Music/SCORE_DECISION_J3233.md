# J3233 — Elected-Chief Replacement Score Route Decision (`HOS 009`, Option a: £0 Own-Synthesis Opening Joined to Retained `teach_v01`)

- **Film:** `009_The-Falling-Moon-Gravity` (*Why Doesn't the Moon Fall to Earth?*, historical air target `Thu 26 Nov 2026`, `ready_by: 2026-11-22` at risk)
- **Job:** `J3233` (`HOS 009: decide post-J3174 compliant replacement score route`, `--kind chief`, `ref: J3228`)
- **Acting Chief:** `gemini` (`Grok -> Claude -> Codex -> Gemini`; `chief_relay.py status` verified before decision: `claude` down until `17:50Z`, `chief` Grok Bot down until `17:33Z`, `codex` down until `14:55Z`, `gemini` UP as elected Chief)
- **Date:** 20 Nov 2026
- **Spend & API Calls:** `£0.00` cash, `0` subscription credits, `0` account GETs, `0` ElevenLabs POSTs
- **Audio/Video Perception Claim in `J3233`:** None (`capabilities: []` recorded at session start; all acoustic references cite completed `J2783` and `J2807` multimodal ear reviews)
- **Decision:** **Select Option (a) — Compliant £0 Non-ElevenLabs Own-Score Route** (`_build_hos009_wonder_v03_synth.py`, pure Python/NumPy synthesis covering `0.00–178.28 s` joined via exact 3.0 s equal-power crossfade at `175.28–178.28 s` to byte-unchanged `hos_009_teach_v01.mp3`), gated by complete-library unchanged `music_gate.py`, continuity telemetry, independent demonstrated-audio review (`J3235`), and separate elected-Chief disposition (`J3236`). This decision opens production scope only; it is **not** a score acceptance, film PASS, or Ben-watch waiver.

---

## 1. Verified Post-`J3174` Baseline (`J3228`, 20 Nov 2026)

1. The offline billing-guard and disabled-flight hardening chain (`J3139`–`J3174`) completed and merged onto HOS `main` via PR `#675` (`327c220d`), PR `#680` (`f13cb7ae`), and PR `#681` (`3211c7de`, exact approved head `a76bfa8f57250935b7818dc126bb3d42f74fb87d`).
2. `ACTIVATION_AUTHORIZED` remains literal `False` in `04_Audio/tools/hos009_score_flight.py:34` because `jobs/reviews/J3150/PRICING_EVIDENCE.md` (19 Nov 2026) demonstrates that public ElevenLabs pricing pages do not establish both `<= 3,000` subscription credits and `£0` cash for one 180 s `music_v2` request (`elevenlabs.io/pricing` gives an approximate ~900 credits/min with no numeric single-request max; `elevenlabs.io/pricing/api` prices API Music in USD at `$0.15/min`).
3. `J3043`/`J3045` allowance remains permanently closed unused (`J3047`); `v01` (`music_gate` fail `0.821`) and `v02` (`J2807` ear-review fail on six `0.61–2.29 s` `< -45 dB` inter-phrase silent dropouts across `18.95–97.92 s`) remain rejected (`J2808`).
4. `hos_009_teach_v01.mp3` (`sha256: 4c1f0a17364ad5ba96fdd2d42730b2f857d19017fab52b221701bd4e15d07bb1`, `360.045688 s`, D-minor harpsichord + low strings, covering `175.28–535.33 s`) passed demonstrated-audio ear review twice (`J2783` and `J2807`) on musical fit, narration clarity, Part 5 discovery thinning, and tail coverage past `518.40 s` VO end and `526.00 s` reference endpoint.
5. `02_Video-Projects/009_The-Falling-Moon-Gravity/status.json` still cited completed `J3050` and is reconciled in this PR.

---

## 2. Evaluation of the Three Candidate Routes

| Route | Assessment | Verdict |
|---|---|---|
| **(a) Compliant £0 non-ElevenLabs own-score route** | Proven HOS house precedent: both shipped longs **HOS 006** (`trees006_score_bed_v01.mp3`, `531.83 s`, own Python/NumPy synthesis) and **HOS 007** (`vaccine_score_bed_v01.mp3`, `531.08 s`, own NumPy synthesis) cost `£0` / `0` credits and passed `music_gate.py`. Retaining ear-passed `hos_009_teach_v01.mp3` byte-for-byte for `175.28–535.33 s` and synthesizing a deterministic pure-Python/NumPy 17th-century D-minor chamber opening (`0.00–178.28 s`, Karplus-Strong plucked gut-string lute + warm multi-voice bowed viols, evolving modal harmony, zero silent rests, zero third-party/GPL samples) directly eliminates both `v01` (static bass drone) and `v02` (inter-phrase dropouts), preserves `ACTIVATION_AUTHORIZED = False`, spends `£0` / `0` credits, needs no Ben billing escalation, and unblocks November's 4th HOS film (`3/4` complete). | **SELECTED** |
| **(b) Establish proven ElevenLabs credit/cash bound** | Public pricing pages do not prove both `<= 3,000` credits and `£0` cash (`PRICING_EVIDENCE.md`). Proving the bound without unauthorized account calls requires escalating to Ben for login/billing confirmation or waiting on vendor docs, still consumes shared TTS subscription credits, and remains exposed to generative nondeterminism (`v01` reuse fail, `v02` rest dropouts). Unnecessary while a proven `£0` house route exists. | **REJECTED NOW** (retained only as bounded fallback if own-synthesis fails ear review) |
| **(c) Indefinite hold / schedule slip** | Leaves HOS 009 stalled indefinitely with no active work unblocking `J2035`/`J2171`, shorting HOS's 4-videos/month November cadence (`3/4` complete) despite an established `£0` house synthesis route. | **REJECTED** |

---

## 3. Approved Production Scope & Hard Guardrails (`SCORE_SCOPE_J3233.json`)

- **Tooling & provenance:** Deterministic pure Python/NumPy DSP script `02_Video-Projects/009_The-Falling-Moon-Gravity/05_Music/_build_hos009_wonder_v03_synth.py`. Zero third-party copyrighted samples, zero GPL soundfonts (`TimGM6mb.sf2` excluded), zero macOS system soundfonts (`gs_instruments.dls` excluded), zero network/API calls.
- **Musical brief (`hos_009_wonder_v03_synth.wav`, `180.00 s` raw, `0.00–178.28 s` source window, 48 kHz 16-bit stereo PCM):**
  - 17th-century D-minor (`A4 = 440 Hz`) chamber underscore matching `teach_v01`'s tonal centre: Karplus-Strong plucked gut-string lute arpeggios + warm multi-voice bowed viols (gentle vibrato, wooden body low-pass/formant shaping, subtle stereo chamber room resonance).
  - `60–66 BPM`, evolving modal chord progressions every 2–4 bars (NO static bass-drone opening), continuously overlapping voices from `0.00 s` to `178.28 s` with ZERO silent rests/dropouts (`0` interior `< -45 dB` stretches), warm Woolsthorpe orchard colour shift at `84.44 s` (Part 2 card), tapering onto a quiet sustained `D4/A4` D-minor handoff across `175.28–178.28 s` loudness-matched to `hos_009_teach_v01.mp3`.
- **Join & stems:** Exact 3.0 s equal-power crossfade (`acrossfade=d=3:c1=qsin:c2=qsin` at `175.28–178.28 s`, centred on the `176.78 s` cannon chapter card) into byte-unchanged `hos_009_teach_v01.mp3` (`4c1f0a17364ad5ba96fdd2d42730b2f857d19017fab52b221701bd4e15d07bb1`) -> `hos_009_score_joined_v03.wav` (`~535.33 s`), plus 5 part stems (`hos_009_stem_part01..05_*_v03.wav`) and audition clips (`audio_review_v03_synth/`).
- **Mandatory gates (no waivers):**
  1. Unchanged production `orbit-with-ben/scripts/music_gate.py` PASS over complete current library (`>= 89` comparisons across all 9 roots including all 77+ historical HOS/OWB beds and all 15 hash-verified iCloud UAT tracks, `0` unreadable, `< 0.80` max similarity, `0` fails) on BOTH `hos_009_wonder_v03_synth.wav` and `hos_009_score_joined_v03.wav`.
  2. Explicit continuity telemetry (`ffmpeg silencedetect=noise=-45dB:d=0.25` and `d=0.50` + 1-second RMS floor table across `0.00–178.28 s` confirming `0` interior dropouts) and EBU R128 loudness parity against locked VO.
  3. Mini & NAS (`/Volumes/data/studio-live/.../05_Music/`) SHA-256 parity for all `v03` files and all preserved locks; media kept out of git.
  4. Independent demonstrated-audio (`audio_input`) ear review (`J3235`) explicitly passing period warmth/realism, continuity, `175.28–178.28 s` join blend into `teach_v01`, wonder/teach contrast, VO intelligibility, tempo fit, and tail coverage.
  5. Separate elected-Chief score acceptance (`J3236`).
- **Pre-decided bounded fallback:** If `v03_synth` fails `music_gate.py` or fails `J3235` ear review, `J3236` refuses acceptance, keeps `J2035`/`J2171` held, and selects either (i) at most ONE bounded `£0` DSP/timbre revision (`v04_synth`, or full-runtime `0–535.33 s` own-synthesis bed if join timbre mismatch is the sole blocker) OR (ii) one explicit billing/pricing confirmation escalation to Ben for ElevenLabs `music_v2`.
- **Unconditional guardrails preserved:** `£0` cash, `0` credits, no account GET, no ElevenLabs POST, `ACTIVATION_AUTHORIZED` stays literal `False`, `J3043`/`J3045` stays permanently closed unused (`J3047`), `v01`/`v02` remain rejected (`J2808`), no looping/stretching of `hos_009_teach_v01.mp3`, `J2035` and `J2171` remain held, all locked picture/VO/diagram/music hashes preserved byte-for-byte, and no YouTube/Buffer/schedule changes.

---

## 4. Queued Concrete Handoff Chain

1. **`J3234`** (`--kind assembly`, Mini, `after: J3233`, due `2026-11-21T06:00:00Z`): Synthesize `hos_009_wonder_v03_synth.wav` in pure Python/NumPy, join to retained `teach_v01` at `175.28–178.28 s`, verify complete-library `music_gate.py`, continuity telemetry, and Mini/NAS SHA-256 parity, and open HOS PR.
2. **`J3235`** (`--kind review`, `--requires audio_input`, Mini, `after: J3234`, due `2026-11-21T10:00:00Z`): Independent demonstrated-audio listening review of `hos_009_wonder_v03_synth.wav`, `hos_009_score_joined_v03.wav`, `168–186 s` join, 5-part VO reference mix, and tail; commit `05_Music/EAR_REVIEW_v03_synth.md`.
3. **`J3236`** (`--kind chief`, `after: J3235`, due `2026-11-21T12:00:00Z`): Separate elected-Chief score disposition after verifying `J3234` gates and `J3235` independent ear review, or invoking the bounded fallback.
