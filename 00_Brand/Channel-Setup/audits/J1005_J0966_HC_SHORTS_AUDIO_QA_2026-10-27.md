# J1005 — J0966 HC Multimodal Audio + Video QA Report (Four Rebuilt HOS Shorts Masters)

- **Job:** `J1005` (`J0966 HC: audition four finished masters and resolve vaccine pronunciation warnings (GBP0)`)
- **Parent Job:** `J0966` (`HOS:004,HOS:005,HOS:007` — held at step `5/5` pending final Chief decision)
- **Date:** 2026-10-27
- **Reviewer / Tool Route:** `gemini` (`--model gemini-argon`), native multimodal audio (`audio/mp3`, 192 kbps 48 kHz stereo extracted from each master `.mp4`) + native multimodal video (`video/mp4`, `_PHONE.mp4` 1080×1920 30 fps) ingestion via `read_file` on the local subscription route, cross-checked against 15 ms PCM RMS envelopes on the VO stems (`_work_*/hos_*_vo_*.wav`).
- **Spend:** **£0.00** (zero ElevenLabs TTS or video generation; all four masters, `_PHONE` copies, and UAT/NAS copies preserved untouched).

---

## 1. Executive Summary & Verdicts

| # | Short Master | YouTube ID | Air Date | Duration | Master SHA256 | `vo_check.py` Warnings Ruling | End-to-End Audition Verdict |
|---|---|---|---|---|---|---|---|
| 1 | `007_The-First-Vaccine/10_Shorts/hos_007_s04_smallpox_test_v03.mp4` | `-I_GHK-GcFs` | Fri 13 Nov 2026 | `22.400s` | `858495ea7dcb28788f1277367dbd4d1d30e4c95ca95ffd230f1c1a82a0513ea5` | `PASS` (0 warnings, `155 wpm`) | **OPENING TRIM DEFECT (`0:00.00–0:00.085`):** residual `"a-/...y"` phoneme bleed from dropped word `"July,"` before `"Jenner did the test."` Body VO, `variolation` pronunciation, picture, overlay, and mix all **PASS**. £0 75 ms start-trim/fade fix below. |
| 2 | `005_How-Harvey-Proved-Blood-Circulates/10_Shorts/hos_005_s03_never_saw_v04.mp4` | `x_3L_IdYgEc` | Sun 15 Nov 2026 | `25.259s` | `e1f862ba737acc4276dd676fc93181b41e729fce029fed57318bf43add3e9f63` | `143 wpm` pace warn **RESOLVED PASS** (natural, measured cadence at `25.259s`) | **FULL PASS (Ready to Ship As-Is):** clean open, crisp `Marcello Malpighi` & `Capillaries` pronunciation, single Malpighi overlay, clean bed/SFX mix, seamless visual + audio loop join. |
| 3 | `004_Whats-Really-Inside-An-Atom/10_Shorts/hos_004_s05_dalton_v03.mp4` | `-sa2t7dAtCk` | Mon 16 Nov 2026 | `24.533s` | `f93745e955586097293b7e37cad73c025ec99d79b0ee3b8e34bd955df6380edc` | `PASS` (0 warnings, `160 wpm`) | **OPENING TRIM DEFECT (`0:00.00–0:00.060`):** residual `"z-/t-"` alveolar consonant bleed from dropped word `"says"` (`"His atomic theory says every..."`) before `"Every element"`. Body VO, clause join, picture, overlay, and mix all **PASS**. £0 60 ms start-trim/fade fix below. |
| 4 | `007_The-First-Vaccine/10_Shorts/hos_007_s05_vacca_jesty_v05.mp4` | `4WUs0beKn0A` | Tue 17 Nov 2026 | `24.533s` | `e5ea76f012fb94c54c4a7224140d2d8ca342ea8c02a2fbdb30df17661f94f1ad` | `variolae vaccinae` (`~12.10s`) & `vacca` (`~17.56s`) **RESOLVED PASS** (ASR false positives; spoken Latin is exact) | **PASS on Pronunciation, Open, Picture, Mix & Loop; Minor Prosodic Note at `0:05.536s` Splice:** `"Jenner"` (`5.536–5.827s`) and `"tested"` (`5.888–6.221s`) are 100% intelligible and unclipped, with a slightly tight/abrupt prosodic step across the `44 ms` `-120 dBFS` gap. Can ship as-is or apply optional £0 micro-crossfade. |

---

## 2. SHA256 & Copy Verification Across All Three Storage Tiers

All 24 files (master `.mp4`, `_PHONE.mp4`, and `2fps_sheet.jpg` across the shared HOS checkout, iCloud `HOS UAT`, and `/Volumes/data/mac-mini-archive` NAS) were verified bit-for-bit prior to and after audition:

1. **`hos_007_s04_smallpox_test_v03` (`-I_GHK-GcFs`, `22.400s`, `-14.2 LUFS`, `-1.6 dBFS` TP)**
   - Master `.mp4`: `858495ea7dcb28788f1277367dbd4d1d30e4c95ca95ffd230f1c1a82a0513ea5`
   - `_PHONE.mp4`: `8b31dc1a6a758494e0484bf197bb6773ccd87027e0d6e0c1c2fbb97a591be907`
   - `2fps_sheet.jpg`: `7ec9496e2fb53ffa11c2dfae26388d6a679dd3b6b8d8ebb8445d0ef018b90704`
2. **`hos_005_s03_never_saw_v04` (`x_3L_IdYgEc`, `25.259s`, `-14.0 LUFS`, `-1.8 dBFS` TP)**
   - Master `.mp4`: `e1f862ba737acc4276dd676fc93181b41e729fce029fed57318bf43add3e9f63`
   - `_PHONE.mp4`: `1cd37e5fbf2b6b3cf4f04c0e3d25680858ce4414ea8598889f09c1c5f7d3b2d0`
   - `2fps_sheet.jpg`: `200384cb04989033fe4a92f7ad97704f4dbe2eb476fc5533e6ac0b9321e5c8cd`
3. **`hos_004_s05_dalton_v03` (`-sa2t7dAtCk`, `24.533s`, `-14.2 LUFS`, `-1.7 dBFS` TP)**
   - Master `.mp4`: `f93745e955586097293b7e37cad73c025ec99d79b0ee3b8e34bd955df6380edc`
   - `_PHONE.mp4`: `c26430c5753aa9bd5bd4b93a1065407e0ff8d4aee2bb07590866c200064bef55`
   - `2fps_sheet.jpg`: `085563081830e454eb5b1154a594c3c78167a75a130092fd9655a40a7ff946a2`
4. **`hos_007_s05_vacca_jesty_v05` (`4WUs0beKn0A`, `24.533s`, `-14.2 LUFS`, `-1.6 dBFS` TP)**
   - Master `.mp4`: `e5ea76f012fb94c54c4a7224140d2d8ca342ea8c02a2fbdb30df17661f94f1ad`
   - `_PHONE.mp4`: `066c6774add20b1ad8c5859d27b5e14ca094d9de153597c1b7105e648a62afe1`
   - `2fps_sheet.jpg`: `6d80ca34cd9e65e0822117f59fada8933824f02f2b8128bf2d0bca646669f726`

---

## 3. Per-Short End-to-End Audition & Moving-Picture Inspection

### 3.1 `hos_007_s04_smallpox_test_v03.mp4` (`-I_GHK-GcFs`, `22.400s`)

- **Spoken Script Auditioned:**
  > *"Jenner did the test. He gave James a standard variolation, the old treatment that used real smallpox matter, which would normally cause at least a mild illness. Then he waited. One day. Three days. A week. Nothing happened. In Jenner's words, no disease followed. Months later, he tried again. Still nothing. The cowpox had protected the boy."*
- **Opening Trim Defect (`0:00.00–0:00.085`):**
  - **What is heard:** Immediately at `0:00.00`, before `"Jenner did the test"`, there is a short vocalized syllable/phoneme bleed that sounds like `"a Jenner did the test"` (`"...y Jenner"`).
  - **Root cause in build script & alignment:** `_build_short_s04_smallpox_test_v03.py` drops `"On the first of July,"` (`words[0..4]` of `part04_the_test_v01b.mp3`, where `word[4]` `"July,"` is aligned at `0.720–1.040s` and `word[5]` `"Jenner"` is aligned at `1.166–1.440s`) and trims `TAKE[0]` from `s0 = 1.166 - 0.020 = 1.146s`. In the actual waveform (`hos_007_s04_smallpox_test_vo_v03.wav`), the trailing `/aɪ/` diphthong release of `"July,"` rings at `-29.9 dBFS` to `-38.2 dBFS` across `0.000–0.055s`, reaches the true inter-word silence trough (`-47.8 dBFS`) at `0.060–0.085s`, and the `/dʒ/` onset of `"Jenner"` begins at `0.090s` (`-36.0 dBFS` rising to `-17.1 dBFS` at `0.150s`).
- **Pronunciation & Body Intelligibility (`0:00.09–0:21.98`):**
  - **PASS.** Every word from `"Jenner"` (`0:00.09s`) to `"boy."` (`0:21.98s`) is crisp, natural, and unclipped.
  - `"variolation"` (`0:02.75s–0:03.59s`) is pronounced `/ˌvɛər.i.əˈleɪ.ʃən/` ("vair-ee-uh-LAY-shun") clearly.
  - Zero repeated or stumbled words; all sentence-break pause caps (`MAX_PAUSE = 0.16s` at `ATEMPO = 1.05`) sound natural.
- **Bed / SFX Fit & Moving Picture / Loop Join:**
  - **Bed & SFX (`PASS`):** D-major/B-minor plucked bed (`64 BPM`, `-14.0 dB`) + soft opening whoosh and subtle ink ticks at `2.05s` (`EDWARD JENNER` card) and `20.11s` (`"The cowpox had protected the boy."`) sit cleanly beneath the VO (`VO -21.0 LUFS, SFX -49.6 LUFS`).
  - **Picture & Overlays (`PASS`):** Frame 0 (`THE FIRST TEST` with yellow `TEST`, `0.0–2.0s` over `03b_lancet_case_t1.mp4`), single educational WHO card (`EDWARD JENNER / 1 July 1796 · Berkeley`, `2.05–5.45s`), and parent title (`Why Vaccines Are Named After a Cow`, `9.0–14.0s`) all read cleanly with zero caption overlap (`max_active_vo_captions_any_frame = 1`).
  - **Loop Join (`21.25s–22.40s -> 0.00s`):** Visually returns smoothly to `03b_lancet_case_t1.mp4` (`in_s = 0.05s` matching frame 0 `in_s = 1.20s`), and `"The cowpox had protected the boy."` (`ends 21.98s`) leaves a clean `0.42s` tail breath — but when looping back to `0:00.00`, the listener hears the `"a-"` pre-word bleed before `"Jenner"`.
- **£0 Repair Recommendation for `hos_007_s04_smallpox_test_v03`:**
  - **In-place £0 VO stem trim/fade (no TTS spend, no cut/caption shift):** Mute the first `75 ms` (`0.000–0.075s`, where the `"July"` tail sits before the `-47.8 dBFS` trough) and apply a `20 ms` fade-in at `0.075s` on `hos_007_s04_smallpox_test_vo_v03.wav`:
    ```
    volume=enable='lt(t,0.075)':volume=0,afade=t=in:st=0.075:d=0.020
    ```
    (Alternatively, in `_build_short_s04_smallpox_test_v03.py` line 366, change `s0` for `i == 0` from `s - 0.02` to `s + 0.060` (`1.226s` in `part04_the_test_v01b.mp3`) and add `0.075s` to `TAIL_S`.) `"Jenner"` still attacks at `0.085–0.090s` (`<= 0.15s` VO onset gate), completely removing the opening bleed.

---

### 3.2 `hos_005_s03_never_saw_v04.mp4` (`x_3L_IdYgEc`, `25.259s`)

- **Spoken Script Auditioned:**
  > *"Harvey never saw the last link. He proved your blood goes round, but not how it crosses from arteries to veins. He died in sixteen fifty-seven, still guessing. Four years later, Marcello Malpighi put a frog's lung under a microscope. There it was: a net of vessels finer than hairs. Capillaries. The last link Harvey never saw."*
- **Opening, Body Intelligibility & Pace (`0:00.00–0:24.26`):**
  - **FULL PASS.** Starts cleanly at `0:00.00` on `"Harvey never saw the last link."` with zero pre-word bleed or clipping.
  - **Pronunciation Rulings:**
    - `"Marcello Malpighi"` (`0:12.32s–0:13.46s`): Pronounced clearly and accurately as `/mɑːrˈtʃɛloʊ mælˈpiːɡi/` ("Mar-CHELL-oh Mal-PEE-gee").
    - `"Capillaries."` (`0:20.38s–0:21.46s`): Pronounced clearly in standard British English `/kəˈpɪləriz/` (stress on second syllable).
  - **Pace Warning Ruling (`143 wpm` vs `145 wpm` long-form floor):** Audition confirms the `143 wpm` delivery sounds deliberate, clear, and suspenseful (`"There it was: a net of vessels finer than hairs. Capillaries."`), with zero sluggishness or artificial drag.
  - Zero repeated, stumbled, or clipped words across all 57 words.
- **Bed / SFX Fit & Moving Picture / Loop Join:**
  - **Bed & SFX (`PASS`):** E-minor/G-major glass-bell and lute bed (`62 BPM`) + soft opening whoosh and two ink ticks (`14.15s` on the Malpighi card and `20.38s` on `"Capillaries."`; the extra `2.20s` Harvey tick from `v03` is gone) sit cleanly under the VO (`VO -18.6 LUFS, SFX -49.6 LUFS`, master `-14.0 LUFS`, `-1.8 dBFS` TP).
  - **Picture & Overlays (`PASS`):** Frame 0 (`HE NEVER SAW THIS` with yellow `SAW`, `0.0–2.04s`), single educational WHO card (`MARCELLO MALPIGHI / Bologna, 1661`, `14.15–17.35s`), and parent title (`The Tied Arm That Proved Your Blood Circulates`, `9.0–14.0s`) are clean and well-timed.
  - **Loop Join (`24.26s–25.26s -> 0.00s`):** **PASS.** Visual loop on `06_eyepiece_mesh_t1.mp4` (`in_s = 0.40s` running `1.00s` into frame 0 `in_s = 1.40s`) and audio loop from `"The last link Harvey never saw."` back into `"Harvey never saw the last link."` are seamless.

---

### 3.3 `hos_004_s05_dalton_v03.mp4` (`-sa2t7dAtCk`, `24.533s`)

- **Spoken Script Auditioned:**
  > *"Every element is made of its own kind of atom, and each kind has its own weight. Hydrogen is the lightest. Oxygen is heavier. Gold is heavier still. Why believe him? Because elements always combine in the same fixed amounts. Water is always the same mix of hydrogen and oxygen, That only makes sense if both are made of tiny pieces with fixed weights."*
- **Opening Trim Defect (`0:00.00–0:00.060`):**
  - **What is heard:** Immediately at `0:00.00`, right on the attack of `"Every"`, there is a brief alveolar sibilant/consonant artifact (`"z-/t- Every element..."`).
  - **Root cause in build script & alignment:** In `004_Whats-Really-Inside-An-Atom/01_Script/atom_script_master_v02.md` (line 85), the source sentence is `"His atomic theory says every element is made of its own kind of atom..."`. In continuous speech, the final `/z/` of `"says"` (`word[16]`) coarticulates directly into `"every"` (`word[17]`). When `_build_short_s05_dalton_v03.py` (line 343) cut at `s0 = s` (`word[17]`), the trailing alveolar release of `"says"` (`-26.7 dBFS` to `-25.7 dBFS` across `0.000–0.055s` in `hos_004_s05_dalton_vo_v03.wav`) was included before the `-35.1 dBFS` inflection trough at `0.060s` and the `/ɛ/` vowel onset of `"Every"` (`-29.2 dBFS` at `0.075s` rising to `-14.7 dBFS` at `0.120s`).
- **Pronunciation, Clause Skip & Body Intelligibility (`0:00.06–0:23.89`):**
  - **PASS.** From `0:00.06s` onward, all 64 words are clear and natural (`160 wpm`).
  - **Clause-skip splice (`"Water is always the same mix of hydrogen and oxygen, [skip: however you make it.] That only makes sense..."` at `0:19.22s–0:19.79s`):** Sounds completely natural, with a normal breath intake during the `0.45s` pause before `"That only makes sense"`. Zero stumbled or repeated words.
- **Bed / SFX Fit & Moving Picture / Loop Join:**
  - **Bed & SFX (`PASS`):** C-major/A-minor clavichord and plucked string bed (`66 BPM`) + soft opening whoosh and ink ticks at `2.20s` (`JOHN DALTON` card) and `22.33s` (`"pieces"`) sit cleanly under the VO (`VO -18.7 LUFS, SFX -49.6 LUFS`, master `-14.2 LUFS`, `-1.7 dBFS` TP).
  - **Picture & Overlays (`PASS`):** Frame 0 (`EACH ATOM` with yellow `ATOM`, `0.0–2.0s`), single WHO card (`JOHN DALTON / Manchester, 1808`, `2.20–5.60s`), parent title (`What's Really Inside an Atom?`, `9.0–14.0s`), and letter-free replacement plates (`15_knife_coin_return_v01` at `2.56–4.77s` and `03_atom_turns_v01` at `20.87–23.36s`) all pass cleanly.
  - **Loop Join (`23.36s–24.53s -> 0.00s`):** Visually returns smoothly to `01_dalton_schoolroom_v01` (`in_s = 1.65s` running `1.15s` into frame 0 `in_s = 2.80s`), though aurally the loop back to `0:00.00` hits the `"z-/t-"` onset artifact on `"Every"`.
- **£0 Repair Recommendation for `hos_004_s05_dalton_v03`:**
  - **In-place £0 VO stem trim/fade (no TTS spend, no cut/caption shift):** Mute the first `60 ms` (`0.000–0.060s`, where the trailing `/z/` release of `"says"` sits) and apply a `20 ms` fade-in at `0.060s` on `hos_004_s05_dalton_vo_v03.wav`:
    ```
    volume=enable='lt(t,0.060)':volume=0,afade=t=in:st=0.060:d=0.020
    ```
    (Alternatively, in `_build_short_s05_dalton_v03.py` line 343, change `s0 = s if i == 0 else s - 0.06` to `s0 = s + 0.062 if i == 0 else s - 0.06` and add `0.060s` to `TAIL_S`.) `"Every"` attacks cleanly on its `/ɛ/` vowel at `0.060s` (`<= 0.15s` VO onset gate), eliminating the `"z-/t-"` consonant bleed at £0.

---

### 3.4 `hos_007_s05_vacca_jesty_v05.mp4` (`4WUs0beKn0A`, `24.533s`)

- **Spoken Script Auditioned:**
  > *"Jenner wasn't the first to try cowpox. Benjamin Jesty had done it twenty-two years earlier. Jenner tested more people, and in seventeen ninety-eight he paid to print a short book. He called the disease by a Latin name, variolae vaccinae, which means smallpox of the cow. From vacca, the Latin word for cow, came the name for the treatment: vaccination."*
- **Resolution of `vo_check.py` Sounds-Alike Warnings (Both PASS):**
  1. **`variolae vaccinae` (`~0:12.10s` in VO check report / `0:12.97s–0:14.93s` in master):**
     - **Ruling: PASS (ASR Transcriber False Positive).**
     - **Audition evidence:** Ben pronounces `"variolae"` (`0:12.97s–0:14.00s`) clearly as `/ˌvær.iˈoʊ.laɪ/` ("va-ree-OH-lye") and `"vaccinae"` (`0:14.09s–0:14.93s`) clearly as `/vækˈsiː.neɪ/` ("vak-SEE-nay"). Faster-Whisper transcribed `variolae` as `varioli` solely because English ASR models map the classical Latin `-ae` diphthong to `-i`. No pronunciation defect exists in the audio.
  2. **`vacca` (`~0:17.56s` in VO check report / `0:18.69s–0:19.14s` in master):**
     - **Ruling: PASS (ASR Homophone Spelling).**
     - **Audition evidence:** In `"From vacca, the Latin word for cow..."` (`0:18.22s–0:20.85s`), Ben pronounces `"vacca"` (`0:18.69s–0:19.14s`) clearly as `/ˈvæk.ə/` ("VAK-uh"). Faster-Whisper spelled the phonetic homophone `vaca` with one `c`.
  3. **`Benjamin Jesty` (`0:02.36s–0:03.51s`):** Pronounced clearly as `/ˈbɛndʒəmɪn ˈdʒɛsti/`.
- **Audition of the `"Jenner"` Attribution Splice (`0:05.536s–0:06.221s`):**
  - **What was built:** `_build_short_s05_vacca_jesty_v05.py` replaced word 103 (`"He"`) after `"Benjamin Jesty had done it twenty-two years earlier."` (`ends 5.298s`) with sentence-initial word 176 (`"Jenner"`, trimmed at `[76.500, 76.835]s` from `"Jenner sent cowpox matter..."` in `part04_the_test_v01b.mp3`), followed by a `44 ms` (`0.045 / 1.03`) `anullsrc` gap (`5.840s–5.880s` at `-120.0 dBFS`) into word 104 (`"tested"`, trimmed from `45.095s`).
  - **What is heard:**
    1. `"Jenner"` (`0:05.536s–0:05.827s`, peaking at `-13.2 dBFS`) and `"tested more people"` (`0:05.888s–0:06.843s`, peaking at `-12.5 dBFS`) are **100% intelligible, unclipped, and unambiguous** — the listener clearly hears `"Jenner tested more people, and in seventeen ninety-eight he paid to print a short book."`
    2. **Prosodic note:** Because `"Jenner"` was spoken at the start of `"Jenner sent..."` and fades to `-120 dBFS` digital zero for `44 ms` (`5.840–5.880s`) before `"tested"` enters from mid-phrase `"He tested"` (`-12.5 dBFS`), the join between `"Jenner"` and `"tested"` sounds slightly tight/abrupt in cadence (`"Jenner-tested"`, with a slight upward energy/pitch step on `"tested"`).
  - **Optional £0 Polish (if Chief wants `v06`; `v05` is also shippable as-is):**
    - In `_build_short_s05_vacca_jesty_v05.py`, widen `INLINE_SPLICE[(176, 104)]` from `0.045s` to `0.075s`, extend word 176's end trim from `76.835s` to `76.855s` with a `45 ms` fade-out (`afade=t=out:st=0.310:d=0.045`), and attenuate the `"tested more people,"` span by `-1.0 dB` so the prosodic contour matches `"Jenner"`.
- **Opening, Bed / SFX Fit & Moving Picture / Loop Join:**
  - **Opening (`0:00.00–0:02.19`):** **PASS.** `"Jenner wasn't the first to try cowpox."` (`word[62]` of `part04_the_test_v01b.mp3`, preceded by a full sentence break after `"boy."`) starts cleanly at `0:00.019s` with zero pre-word bleed.
  - **Bed & SFX (`PASS`):** G-major/E-minor pastoral plucked figure (`68 BPM`, `-17.0 dB`) + soft opening whoosh and ink ticks at `2.36s` (`BENJAMIN JESTY` card) and `18.22s` (`"From vacca..."`) sit cleanly under the VO (`VO -20.7 LUFS, SFX -52.6 LUFS`, master `-14.2 LUFS`, `-1.6 dBFS` TP).
  - **Picture & Overlays (`PASS`):** Frame 0 (`NOT THE FIRST` with yellow `FIRST`, `0.0–2.0s`), single WHO card (`BENJAMIN JESTY / Dorset · 1774`, `2.36–5.25s`, strictly inside `s02` `06_jesty_family_t1.mp4` `2.273–5.417s` and fully faded out before the cut to Jenner's garden hut at `5.417s`), parent title (`Why Vaccines Are Named After a Cow`, `9.0–14.0s`), and all 8 inter-word pause-midpoint cuts pass cleanly.
  - **Loop Join (`23.37s–24.53s -> 0.00s`):** **PASS.** Visual loop on `09_meadow_golden_t1.mp4` (`in_s = 3.05s` running `1.15s` into frame 0 `in_s = 4.20s`) and audio loop from `"...came the name for the treatment: vaccination."` (`ends 24.11s`) back into `"Jenner wasn't the first to try cowpox."` (`0.019s`) are clean.
