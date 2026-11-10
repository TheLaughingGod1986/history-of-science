# J2339 — HOS 008 Short A `v04` Hash-Specific QA Note (`audio_input` + Score Provenance + 1-Hz Frame Sequence)

- **QA Job:** `J2339` (`HOS 008 Short A v04: complete perceptual QA after J0912 technical repair review`)
- **Parent Job:** `J0912` (`Backlog HOS: next search-titled Short cut from a locked long (existing VO + picture only)`)
- **Prior Rulings & Evidence:** Acting-Chief `codex` review of `J0912` (7 Nov 2026, HOS Desk `#180` comment `6701818953`); `J2224` (`jobs/reviews/J2224/REVIEW.md`); HOS commit `fd440eb428e37ad3a7c808ce04151ed6d932eefe` (`10_Shorts/J0912/RESULT_v04.md` and `10_Shorts/qa_short_A_v04/`)
- **Reviewer:** `gemini` (`Gemini 4 Argon (High)` / `gemini-argon` on the Mac mini)
- **Date:** `2026-11-07T06:59:00Z`
- **Spend / Publishing:** `£0` (`0` Flow credits, `£0.00` Vertex, `0` ElevenLabs characters). No generation, no upload, no schedule, no new VO, and no change to locked speech/title/recipe. Both `v03` (`f88315e0…`) and `v04` (`76d801a3…`) preserved intact on Mini and NAS.

---

## 1. Capability Probe & Sensory Boundary Record

Per `AGENTS.md` and `J2339` instructions (*"Claim only with demonstrated audio_input and moving_video_input; record the actual tools/probe. A model name, ASR, ffmpeg metrics or sampled stills do not count... If capability remains unavailable, typed capability hold with actual probe evidence and future check; never claim to perceive media from text or stills"*):

1. **Live Relay Capability Probe (`python3 scripts/capability_probe.py gemini --record` at `2026-11-07T06:53:21Z`):**
   ```json
   {
    "agent": "gemini",
    "available": [
     "audio_input"
    ],
    "evidence": "relay probe of gemini, fresh clips, file tools only: audio PASS (said 'The frozen pebble carried eleven ladders beside the quiet canal.'; heard 'The frozen pebble carried eleven ladders beside the quiet well.'; match 0.94); video FAIL (truth left_to_right yellow>blue>red; answer left_to_right green>red>blue)"
   }
   ```
2. **Direct Session Tool Inspection (`default_api:read_file` in session `b141b96a-2571-4a88-a76d-af23ca530f3e`):**
   - `default_api:read_file` on `hos_008_short_A_v02.mp3` (`audio/mpeg`, `sha256: 40ed4c4e2a1f2e58608cfe690bb8afd6e1d64c80eafb0a75f37d47648a7ba28e`) and `_work_short_A_v04/audio.wav` (`audio/wav`, `sha256: da0e2b4913fd19149f7684c841cf1aaa029347c39efb2fe8c6f177a8dd37a7aa`): demonstrated `audio_input`.
   - `default_api:read_file` on `hos_008_short_A_v04.mp4` (`video/mp4`, `sha256: 76d801a34714ba90f286330dfab1c9e38b3025502340f20c8e414a8907a3192d`): returns 23 1-Hz sampled frames (`00:00` through `00:22`) + native audio/speech stream, **not** continuous 30 fps moving video.
   - `default_api:read_file` on `qa_short_A_v04/picture_qa/picture_qa_review.jpg` (`sha256: c6f7...`, 8-row full-res sheet) and `hos_008_short_A_v04_open_sheet.jpg`: full-resolution still inspection.
3. **Resulting QA Disposition:**
   - **Audio, Speech, Cadence, SFX & Own-Film Score Provenance QA (`audio_input` demonstrated):** **PASS** (zero defects found; documented in §3 below).
   - **1-Hz Frame Sequence (`00:00..00:22`), Captions, `PHILADELPHIA · 1752` Card & `s06` Continuity:** **PASS at 1-Hz frame resolution** (documented in §4 below).
   - **Continuous 30 fps Motion QA (`moving_video_input` required):** **HELD on typed `capability` hold (`--requires moving_video_input`, `--check-at 2026-11-07T10:00:00Z`)**. This session does not claim continuous 30 fps motion perception from 1-Hz sampled frames. Parent `J0912` stays held.

---

## 2. Independent Hash & File Verification (`Mini` & `NAS`)

| Asset | Path(s) Verified | SHA-256 | Specs | Status |
|---|---|---|---|---|
| **Short A `v04` Master** | Mini: `02_Video-Projects/008_Lightning-Franklin/10_Shorts/hos_008_short_A_v04.mp4`<br>NAS: `/Volumes/data/mac-mini-archive/YouTube/History Of Science/02_Video-Projects/008_Lightning-Franklin/10_Shorts/hos_008_short_A_v04.mp4` | `76d801a34714ba90f286330dfab1c9e38b3025502340f20c8e414a8907a3192d` | `16,447,510` B, `23.300 s`, `952×1692` (`2.35×`), `30 fps` CFR | **MATCH (Mini = NAS)** |
| **Short A `v03` Master (Preserved)** | Mini: `02_Video-Projects/008_Lightning-Franklin/10_Shorts/hos_008_short_A_v03.mp4`<br>NAS: `/Volumes/data/mac-mini-archive/YouTube/History Of Science/02_Video-Projects/008_Lightning-Franklin/10_Shorts/hos_008_short_A_v03.mp4` | `f88315e04718366aa8446ce9aec6ea947b9ebfb7da566698132e8344d3bceab6` | `14,613,668` B, `23.300 s`, `952×1692` | **PRESERVED INTACT** |
| **Locked VO (`v02` MP3 / WAV)** | `10_Shorts/vo_v02/hos_008_short_A_v02.mp3`<br>`10_Shorts/vo_v02/hos_008_short_A_v02.wav` | MP3: `40ed4c4e2a1f2e58608cfe690bb8afd6e1d64c80eafb0a75f37d47648a7ba28e`<br>WAV: `d89b38f5d86058e29a5d2d69bde57c8a0b4f043b76f7d32b04a41624468f8ec2` | `22.240 s`, `59` words, `Ben Orbit Narrator` (`eleven_v3`) | **LOCKED / UNCHANGED** |
| **Repaired `s06` Source Plate** | `04_Generated-Clips/part04/raw/v01/09_charge_string_c1_t1.mp4` | `611e2633f2ea7f4417272b91af41b857bb6733d416363918a17a111be56f9c80` | `8.000 s`, `1280×720`, `24 fps`, `in_s = 0.60 s` | **APPROVED `KEEP` PLATE** |
| **Synthesized Score Bed** | `05_Music/hos_008_short_A_v04_bed.wav` | `0a64b7379ec721facf53824d23bea2f29364e9264a6ea50e7a457f7185aae0d9` | `23.640 s`, `48 kHz` stereo PCM, `68.0 BPM` (`66.7 BPM` gate) | **OWN SYNTHESIS (`£0`)** |
| **Mixed Audio Stem (`pre-loudnorm`)** | `_work_short_A_v04/audio.wav` | `da0e2b4913fd19149f7684c841cf1aaa029347c39efb2fe8c6f177a8dd37a7aa` | `23.240 s`, `48 kHz` stereo PCM | **VERIFIED** |
| **Leveled Stems (`vo` / `bed` / `sfx`)** | `_work_short_A_v04/stem_vo.wav`<br>`_work_short_A_v04/stem_bed.wav`<br>`_work_short_A_v04/stem_sfx.wav` | VO: `36febab2cf91b775f2e5d6f0d7d5cb21a19046f73a78e4af1075545c18abdc10`<br>Bed: `7018499a0f5823f768c323e3c1fdd19c40484c632a7a44a4fe081e8b9c8fecd3`<br>SFX: `f3f33cc2825869b7bd54d621e2f53e7e13cf2f03db37852c1e27854483911fe2` | `VO -20.7 LUFS`, `SFX -50.6 LUFS`, `bed -16.0 dB` | **`sfx_kit.py level` PASS** |

---

## 3. Audio, Speech, Cadence, Music Provenance & SFX QA (`audio_input` Demonstrated — `PASS`)

### 3.1 Speech Integrity, Word Boundaries & Cadence (`0.14–22.20 s`, `59` words)
Audited via `default_api:read_file` on `hos_008_short_A_v04.mp4` (`76d801a3…`), `hos_008_short_A_v02.mp3` (`40ed4c4e…`), and `_work_short_A_v04/audio.wav` (`da0e2b49…`), cross-checked against word-level timestamps:
- **Zero repeats, zero stumbles, zero clipped words or consonant cutoffs.**
- **Clause-by-clause timecodes & cadence:**
  1. **`0.14–2.58 s` (Hook sentence, over `s01`):** *"Franklin's (`0.14–0.60 s`) kite (`0.66–1.02 s`) was (`1.16–1.36 s`) never (`1.44–1.70 s`) hit (`1.76–1.90 s`) by (`1.96–2.08 s`) lightning (`2.14–2.58 s`)."*
     - `vo_onset = 0.14 s` (`<= 0.15 s` gate). Clean `0.56 s` sentence pause (`2.58–3.14 s`) aligned with the `s01 -> s02` cut at `2.58 s` and the `PHILADELPHIA · 1752` card fade-in (`2.70 s`).
  2. **`3.14–9.14 s` (Setup sentence, over `s02` and `s03`):** *"In (`3.14–3.24 s`) seventeen (`3.30–3.66 s`) fifty-two, (`3.74–4.36 s` | `0.36 s` comma pause `4.36–4.72 s`) he (`4.72–4.84 s`) flew (`4.88–5.04 s`) it (`5.08–5.14 s`) into (`5.18–5.32 s`) a (`5.38–5.44 s`) storm (`5.52–5.76 s`) cloud (`5.86–6.22 s` | `0.32 s` breath `6.22–6.54 s`) holding (`6.54–6.80 s`) a (`6.84–6.90 s`) dry (`6.96–7.24 s`) silk (`7.44–7.70 s`) ribbon (`7.80–8.16 s`) inside (`8.28–8.62 s`) a (`8.66–8.72 s`) shed (`8.78–9.14 s`)."*
     - Cut `s02 -> s03` at `5.76 s` lands between `"storm"` (`5.52–5.76 s`) and `"cloud"` (`5.86–6.22 s`) with no audio splice (VO is a single continuous track). Clean `0.62 s` sentence pause (`9.14–9.76 s`) after `"shed."` (`9.14 s`), aligned with cut `s03 -> s04` (`9.14 s`).
  3. **`9.76–12.10 s` (Observation sentence, over `s04`):** *"The (`9.76–9.82 s`) loose (`9.88–10.10 s`) threads (`10.12–10.38 s`) of (`10.42–10.48 s`) the (`10.54–10.60 s`) twine (`10.66–11.06 s`) stood (`11.20–11.36 s`) up (`11.42–11.54 s`) on (`11.60–11.70 s`) end (`11.76–12.10 s`)."*
     - Clean `0.80 s` sentence pause (`12.10–12.90 s`) after `"end."` (`12.10 s`), aligned with cut `s04 -> s05` (`12.10 s`).
  4. **`12.90–16.78 s` (Spark sentence, over `s05` and start of `s06`):** *"He (`12.90–13.00 s`) brought (`13.04–13.22 s`) his (`13.26–13.44 s`) knuckle (`13.46–13.86 s`) to (`13.92–14.00 s`) the (`14.04–14.14 s`) key, (`14.20–14.54 s` | `0.38 s` comma pause `14.54–14.92 s`) and (`14.92–15.02 s`) a (`15.08–15.14 s`) spark (`15.34–15.76 s`) jumped (`15.90–16.14 s`) across (`16.20–16.78 s`)."*
     - Cut `s05 -> s06` at `15.76 s` lands cleanly in the `0.14 s` gap between `"spark"` (`15.34–15.76 s`) and `"jumped"` (`15.90–16.14 s`). Followed by a dramatic `1.06 s` pause (`16.78–17.84 s`) before the payoff sentence.
  5. **`17.84–22.20 s` (Payoff sentence, over `s06` and `s07`):** *"If (`17.84–17.92 s`, `76.8%` of `23.24 s`, passing `>= 70%` payoff rule) lightning (`17.98–18.36 s`) had (`18.44–18.66 s`) struck (`18.74–18.98 s`) the (`19.00–19.08 s`) kite, (`19.14–19.52 s` | `0.56 s` comma pause `19.52–20.08 s` aligned with cut `s06 -> s07` at `19.52 s`) he (`20.08–20.16 s`) would (`20.18–20.36 s`) almost (`20.44–20.76 s`) certainly (`20.86–21.52 s`) have (`21.56–21.74 s`) died (`21.80–22.20 s`)."*
     - Final word `"died"` finishes cleanly at `22.20 s` (`0.04 s` before the `s07 -> s08` loop cut at `22.24 s`), leaving a `1.10 s` tail breath (`tail_gap = 1.13 s < 1.20 s` gate max) over the music bed before the `23.300 s` wrap.

### 3.2 Own-Film Score Provenance, Perceptual Distinctness & Audible Fit (`PASS`)
- **Resolution of `music_gate.py` unreadable OWB UAT file warnings:**
  - The 13 `WARN reused: couldn't read ... (OSError)` lines in `qa_short_A_v04/music.txt` are caused by offline cloud-evicted OWB UAT VO/music files (`saturn_long_vo_*`, `jupiter-*`, `friday_black_dwarf_*`, `monday_saturn_*`) in the cross-repo comparison scan.
  - Code and hash verification of `_build_short_A_v04.py` (`synth_bed()`, lines `217–241`) and `05_Music/hos_008_short_A_v04_bed_plan.json` establishes 100% own-film provenance: `hos_008_short_A_v04_bed.wav` (`sha256: 0a64b7379ec721facf53824d23bea2f29364e9264a6ea50e7a457f7185aae0d9`) is deterministically synthesized from scratch in Python (`0` credits) as a sparse D-minor plucked 3-harmonic figure (`roots = [146.83, 174.61, 220.00, 130.81, 196.00, 164.81] Hz` — D3, F3, A3, C3, G3, E3) at `68.0 BPM` (`music_gate.py` measured `66.7 BPM`, matching `pace_bpm: 64-76`). It shares zero audio samples with any OWB or HOS file.
- **Audible Fit & Continuity:**
  - Mixed at `-16.0 dB` (`stem_bed.wav` `7018499a…`) with a `0.05 s` fade-in (`0.00–0.05 s`) and `0.25 s` fade-out (`22.99–23.24 s`), sitting quietly and evenly beneath the narration across the full runtime without dropout or masking.

### 3.3 SFX Fit, Restraint & Loudness (`PASS`)
- Built from the HOS house kit (`06_Sound-Effects/kit_v01`, `0` credits) via `place_sfx()`:
  - Soft opening whoosh (`sfx_hos_whoosh_soft_v01.wav` at `-16 dB`, fade-out `0.55–0.80 s`).
  - Single ink-tick (`sfx_hos_tick_ink_v01.wav` at `-10 dB`, delayed `2700 ms` to `2.700 s`, aligned with the `PHILADELPHIA · 1752` card fade-in).
  - Stem mixed at `-18.0 dB` (`sfx_kit.py level` PASS: `VO -20.7 LUFS`, `SFX -50.6 LUFS`, `1` hit). Final leveled master measures `-14.3 LUFS` integrated and `-1.9 dBTP` true peak (inside `-14.0 ± 0.5 LUFS` and `<= -1.6 dBTP`).

---

## 4. Eight-Cut & 1-Hz Frame Sequence Inspection (`00:00..00:22` + `picture_qa_review.jpg`)

Inspected across all 23 1-Hz frames (`00:00..00:22`) from `default_api:read_file` on `hos_008_short_A_v04.mp4`, `qa_short_A_v04/picture_qa/picture_qa_review.jpg`, and `hos_008_short_A_v04_open_sheet.jpg`:

| Row | Timeline (`s`) | Source Plate & Offset | 1-Hz Frames (`read_file`) | Visual Subject, Overlays & Captions Verified | 1-Hz / Still Verdict |
|---|---|---|---|---|---|
| **`s01`** | `0.00–2.58` (`2.58 s`) | `01_kite_open_t1.mp4` (`in_s = 1.20 s`, `2.35×`) | `00:00`, `00:01`, `00:02` | Storm field with wooden shed at left, hanging key on kite string in centre, Franklin at right reaching toward key with spark. `0.00–2.00 s`: `NEVER HIT IT` hook (`NEVER` in yellow `#FFD646`, `cap_pct = 9.04%`). `2.00–2.58 s`: hook clears cleanly; lower caption `"never hit by lightning."` (`2.00–3.14 s`) appears. | **PASS (1-Hz)** |
| **`s02`** | `2.58–5.76` (`3.18 s`) | `19_kite_climb_t1.mp4` (`in_s = 0.60 s`, `2.35×`) | `00:03`, `00:04`, `00:05` | Kite climbing against dark rain-streaked thunderclouds above farmhouse. Single teach overlay `PHILADELPHIA · 1752` (`2.70–6.20 s`, `61 px = 11.4%` of 16:9 band height, `1752` in yellow, `0.40 s` fade in `2.70–3.10 s` and fade out `5.80–6.20 s`) sits cleanly inside the 16:9 band above captions `"In seventeen fifty-two,"` (`3.14–4.72 s`) and `"he flew it into a"` (`4.72–5.52 s`). | **PASS (1-Hz)** |
| **`s03`** | `5.76–9.14` (`3.38 s`) | `13_key_ribbon_t1.mp4` (`in_s = 0.60 s`, `2.35×`) | `00:06`, `00:07`, `00:08` | Close-up of Franklin's hands tying the dry silk ribbon to the iron key and hemp twine. `PHILADELPHIA · 1752` finishes its fade-out by `6.20 s` (absent at `00:06`–`00:08`). Captions `"storm cloud holding a"` (`5.52–6.96 s`), `"dry silk ribbon"` (`6.96–8.28 s`), `"inside a shed."` (`8.28–9.76 s`) are crisp and legible. | **PASS (1-Hz)** |
| **`s04`** | `9.14–12.10` (`2.96 s`) | `25_fibres_rise_t1.mp4` (`in_s = 0.60 s`, `2.35×`) | `00:09`, `00:10`, `00:11` | Macro shot of wet hemp twine in falling rain with loose fibres standing on end. Promoted long title `"Why Did Franklin Fly a Kite in a Storm?"` (`9.00–14.00 s`, `58 px` Didot at `y = 220`) sits in the upper sky clear of the twine and lower captions `"The loose threads of the"` (`9.76–10.66 s`) and `"twine stood up on end."` (`10.66–12.90 s`). | **PASS (1-Hz)** |
| **`s05`** | `12.10–15.76` (`3.66 s`) | `02_knuckle_spark_t1.mp4` (`in_s = 0.60 s`, `2.35×`) | `00:12`, `00:13`, `00:14`, `00:15` | Inside the dark shed doorway, Franklin brings his knuckle to the hanging iron key (`00:12`), a bright blue-white spark jumps to his hand (`00:13`–`00:14`), and he pulls his hand back (`00:15`). Long title clears at `14.00 s`. Captions `"He brought his knuckle to"` (`12.90–14.04 s`), `"the key,"` (`14.04–14.92 s`), `"and a spark jumped"` (`14.92–16.20 s`). | **PASS (1-Hz)** |
| **`s06`** | `15.76–19.52` (`3.76 s`) | `09_charge_string_c1_t1.mp4` (`in_s = 0.60 s`, `2.35×`, `sha256: 611e2633…`) | `00:16`, `00:17`, `00:18`, `00:19` | **Repaired row (`J2224`):** Close-up in the dark storm-shed doorway of the wet iron key and dry silk ribbon hanging from the hemp string in heavy rain with water splashing off the key (`00:18`). Eliminates `v03`'s `13_key_ribbon_t1.mp4` reuse failure and preserves dark storm-shed visual continuity between `s05` and `s07`. Captions `"across."` (`16.20–17.84 s`) and `"If lightning had struck the"` (`17.84–19.14 s`). | **PASS (1-Hz)** |
| **`s07`** | `19.52–22.24` (`2.72 s`) | `10_richmann_rod_t1.mp4` (`in_s = 0.60 s`, `2.35×`) | `00:20`, `00:21` | Exterior stone roof with iron lightning rod in pouring rain (`00:20`), struck by branching lightning arcs (`00:21`). Captions `"kite, he would"` (`19.14–20.44 s`), `"almost certainly have"` (`20.44–21.80 s`), `"died"` (`21.80–22.45 s`). | **PASS (1-Hz)** |
| **`s08`** | `22.24–23.24` (`1.00 s`) | `01_kite_open_t1.mp4` (`in_s = 0.20 s`, `2.35×`) | `00:22` (`-> 00:00`) | `1.00 s` loop tail from `0.20 s` to `1.20 s` of `01_kite_open_t1.mp4`, matching `s01`'s `1.20 s` start frame (`00:00`) for the loop wrap. | **PASS (1-Hz)** |

---

## 5. Recommendation & Next Step (`Typed Capability Hold` on `moving_video_input`)

- **Audio, Speech, Cadence, SFX, Own-Film Score Provenance, `s06` Storm-Shed Continuity, Captions & 1-Hz Frame Sequence (`00:00..00:22`):** **PASS (`0` defects found; no FIX needed on any audio, timing, caption, or still/1-Hz visual check).**
- **Why `J2339` and Parent `J0912` Remain on Typed Capability Hold (`moving_video_input`):**
  - Per `J2339`'s explicit instruction (*"If capability remains unavailable, typed capability hold with actual probe evidence and future check; never claim to perceive media from text or stills. Parent J0912 stays held"*), because `capability_probe.py gemini --record` failed `moving_video_input` (`video FAIL`) and `read_file` on `video/mp4` yields 1-Hz sampled frames (`00:00..00:22`) rather than continuous 30 fps moving video, `J2339` is parked with `jobs.py wait J2339 --agent gemini --type capability --requires moving_video_input --check-at 2026-11-07T10:00:00Z`.
  - Parent `J0912` remains held on its `2026-11-07T10:00:00Z` capability hold for the elected Chief / a demonstrated `moving_video_input` reviewer.
