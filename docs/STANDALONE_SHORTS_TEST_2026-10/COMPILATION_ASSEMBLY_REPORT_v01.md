# HOS Compilation Film: Full Assembly & Gate Report v01 (J0175)

**Worker:** Gemini (`gemini-agy`) — 23 Oct 2026  
**Branch / PR:** `cursor/j0175-compilation-assembly` (HOS PR #300)  
**Spend:** £0 / 0 credits (house SFX kit, £0 Pillow/Didot closing end card, J0204 code graphics, existing 004 score bed under new segments).

---

## 1. Deliverable Master & Loudness

- **Output MP4 (NAS):** `/Volumes/data/mac-mini-archive/mini-tmp-scratch/2026-10-23/hos_comp_j0175_prep0540/hos_compilation_full_v01.mp4`
- **SHA-256:** `4166f5b892953f75c5a3cd8147fdcb00a390ff848456d421072f7c68751c131c`
- **Duration:** `2993.493 s` (**`49:53`**, inside the 45–60 min lock)
- **Format:** `1920x1080`, `30/1` fps CFR, `yuv420p`, AAC `48000 Hz` stereo (`256 kbps`, `+faststart`)
- **Whole-Cut Loudness (`ffmpeg loudnorm` measurement):**
  - Integrated: **`-14.32 LUFS`** (target `-14.0 LUFS`)
  - True Peak: **`-1.19 dBTP`** (ceiling `-1.0 dBTP`)
  - LRA: **`4.20 LU`**

---

## 2. Chapters List (for YouTube Description)

From `COMPILATION_CHAPTERS_v01.txt`:

```text
0:00 Six discoveries, one question
0:53 The Hidden Circle
9:23 Built From Air
17:57 The Invisible Enemy
24:20 The Empty Chairs
33:38 A Light Through Skin
41:02 Inside the Atom
```

---

## 3. Running Order & Segment Timeline

| # | Start (`m:ss`) | Start (`s`) | Duration (`s`) | Kind | Segment / Film | Notes |
|---|---:|---:|---:|---|---|---|
| 1 | `0:00` | `0.000` | `52.533` | `segment` | `intro` | 14 label-free windows across all 6 masters, 2 ink ticks |
| 2 | `0:53` | `52.533` | `3.000` | `card` | `card_01` | *The Hidden Circle* (J0204 chapter card + tick) |
| 3 | `0:56` | `55.533` | `489.200` | `film` | `005` | Harvey master normalised, trimmed at `489.20 s` (pause `488.69–489.25 s`) |
| 4 | `9:05` | `544.733` | `18.000` | `segment` | `bridge1` | 005 loop -> `code_graphic_comp_timeline_b1` (`1628 · HARVEY`) -> 006 canopy/willow/balance |
| 5 | `9:23` | `562.733` | `3.000` | `card` | `card_02` | *Built From Air* (J0204 chapter card + tick) |
| 6 | `9:26` | `565.733` | `493.567` | `film` | `006` | Trees master normalised, trimmed at `493.55 s` (pause `493.13–493.76 s`) |
| 7 | `17:39` | `1059.300` | `17.900` | `segment` | `bridge2` | 006 leaf & shutters -> 001 microbes & ward basin + 1 ink tick |
| 8 | `17:57` | `1077.200` | `3.000` | `card` | `card_03` | *The Invisible Enemy* (J0204 chapter card + tick) |
| 9 | `18:00` | `1080.200` | `364.638` | `film` | `001` | Germs master normalised (`720p24` -> `1080p30`, `1.5x` upscale) |
| 10 | `24:05` | `1444.838` | `14.700` | `segment` | `bridge3` | 001 basin -> 002 cards -> `code_graphic_comp_timeline_b3` (`1779`, `1860s`) -> desk |
| 11 | `24:20` | `1459.538` | `3.000` | `card` | `card_04` | *The Empty Chairs* (J0204 chapter card + tick) |
| 12 | `24:23` | `1462.538` | `540.700` | `film` | `002` | Periodic table master normalised (`1080p24` -> `1080p30`) |
| 13 | `33:23` | `2003.238` | `14.300` | `segment` | `bridge4` | 002 vacancy -> 003 dark screen -> lit screen reveal + 1 ink tick |
| 14 | `33:38` | `2017.538` | `3.000` | `card` | `card_05` | *A Light Through Skin* (J0204 chapter card + tick) |
| 15 | `33:41` | `2020.538` | `425.700` | `film` | `003` | X-rays master normalised (`1080p24` -> `1080p30`) |
| 16 | `40:46` | `2446.238` | `15.733` | `segment` | `bridge5` | 003 screen -> 004 gold foil -> `code_graphic_comp_timeline_b5` (`1869`, `1895`) -> foil |
| 17 | `41:02` | `2461.972` | `3.000` | `card` | `card_06` | *Inside the Atom* (J0204 chapter card + tick) |
| 18 | `41:05` | `2464.972` | `491.400` | `film` | `004` | Atom master normalised, trimmed at `491.40 s` (pause `491.06–491.68 s`) |
| 19 | `49:16` | `2956.372` | `37.100` | `segment` | `closing` | Six objects pullback -> `code_graphic_comp_timeline_close` (`1911`) -> cream Didot closing card (`31.09–34.59 s`) + 2.5 s hold & fade |

---

## 4. Automated Gate Outputs (Pasted Verbatim)

### 4.1 Whole-Cut Polish Gate (`polish_gate.py`)

Command:
```bash
python3 "/Users/benjaminoats/YouTube/orbit-with-ben/scripts/polish_gate.py" \
  /Volumes/data/mac-mini-archive/mini-tmp-scratch/2026-10-23/hos_comp_j0175_prep0540/hos_compilation_full_v01.mp4 \
  --cuts /Volumes/data/mac-mini-archive/mini-tmp-scratch/2026-10-23/hos_comp_j0175_prep0540/cuts_new_v01.json \
  --out /Users/benjaminoats/_desk/logs/J0175-full-polish.json
```

Output (`COMPILATION_POLISH_GATE_v01.json`):
```text
intro_01     2.4s /Volumes/data/mac-mini-archi ok
intro_02     6.7s /Volumes/data/mac-mini-archi ok
intro_03    11.2s /Volumes/data/mac-mini-archi ok
intro_04    15.7s /Volumes/data/mac-mini-archi ok
intro_05    19.4s /Volumes/data/mac-mini-archi ok
intro_06    22.1s /Volumes/data/mac-mini-archi ok
intro_07    24.5s /Volumes/data/mac-mini-archi ok
intro_08    27.0s /Volumes/data/mac-mini-archi ok
intro_09    29.5s /Volumes/data/mac-mini-archi ok
intro_10    32.6s /Volumes/data/mac-mini-archi ok
intro_11    36.6s /Volumes/data/mac-mini-archi ok
intro_12    40.8s /Volumes/data/mac-mini-archi ok
intro_13    45.0s /Volumes/data/mac-mini-archi ok
intro_14    49.8s /Volumes/data/mac-mini-archi ok
code_graphic_comp_card_01    54.0s code_graphic_comp_card_01.mp WARN low detail: edge density 0.0104 < film p5 0.0105
bridge1_01   546.6s /Volumes/data/mac-mini-archi ok
bridge1_02   549.8s code_graphic_comp_timeline_b ok
bridge1_03   553.1s /Volumes/data/mac-mini-archi ok
bridge1_04   557.0s /Volumes/data/mac-mini-archi ok
bridge1_05   560.7s /Volumes/data/mac-mini-archi ok
code_graphic_comp_card_02   564.2s code_graphic_comp_card_02.mp WARN low detail: edge density 0.0083 < film p5 0.0105
bridge2_01  1061.8s /Volumes/data/mac-mini-archi ok
bridge2_02  1066.2s /Volumes/data/mac-mini-archi ok
bridge2_03  1070.5s /Volumes/data/mac-mini-archi ok
bridge2_04  1074.7s /Volumes/data/mac-mini-archi ok
code_graphic_comp_card_03  1078.7s code_graphic_comp_card_03.mp ok
bridge3_01  1447.0s /Volumes/data/mac-mini-archi ok
bridge3_02  1450.9s /Volumes/data/mac-mini-archi ok
bridge3_03  1454.6s code_graphic_comp_timeline_b ok
bridge3_04  1457.8s /Volumes/data/mac-mini-archi ok
code_graphic_comp_card_04  1461.0s code_graphic_comp_card_04.mp ok
bridge4_01  2005.6s /Volumes/data/mac-mini-archi ok
bridge4_02  2010.7s /Volumes/data/mac-mini-archi ok
bridge4_03  2015.5s /Volumes/data/mac-mini-archi ok
code_graphic_comp_card_05  2019.0s code_graphic_comp_card_05.mp ok
bridge5_01  2449.0s /Volumes/data/mac-mini-archi ok
bridge5_02  2453.9s /Volumes/data/mac-mini-archi ok
bridge5_03  2458.0s code_graphic_comp_timeline_b ok
bridge5_04  2460.8s /Volumes/data/mac-mini-archi ok
code_graphic_comp_card_06  2463.5s code_graphic_comp_card_06.mp WARN low detail: edge density 0.0092 < film p5 0.0105
closing_01  2958.0s /Volumes/data/mac-mini-archi ok
closing_02  2960.2s /Volumes/data/mac-mini-archi ok
closing_03  2961.8s /Volumes/data/mac-mini-archi ok
closing_04  2963.7s /Volumes/data/mac-mini-archi ok
closing_05  2966.1s /Volumes/data/mac-mini-archi ok
closing_06  2969.2s /Volumes/data/mac-mini-archi ok
closing_07  2972.2s /Volumes/data/mac-mini-archi ok
closing_08  2978.2s /Volumes/data/mac-mini-archi ok
closing_09  2984.6s code_graphic_comp_timeline_c ok
closing_10  2989.8s /Volumes/data/mac-mini-archi ok
code_graphic_comp_closing_end_card  2989.2s /Volumes/data/mac-mini-archi ok
polish gate PASS: 0 of 51 rows failed, 3 to look at -> /Users/benjaminoats/_desk/logs/J0175-full-polish.json
```

*(Per-segment `polish_gate.py` also ran individually on `intro`, `bridge1..5`, `closing`, and `card_01..06` in `~/_desk/logs/J0175-seg-*-polish.json`: all 13 segments `verdict: PASS`, `0 failed`.)*

### 4.2 Whole-Cut Picture QA (`picture_qa.py`)

Command:
```bash
python3 "/Users/benjaminoats/YouTube/orbit-with-ben/scripts/picture_qa.py" \
  /Volumes/data/mac-mini-archive/mini-tmp-scratch/2026-10-23/hos_comp_j0175_prep0540/hos_compilation_full_v01.mp4 \
  --cuts /Volumes/data/mac-mini-archive/mini-tmp-scratch/2026-10-23/hos_comp_j0175_prep0540/cuts_new_v01.json \
  --pool /Volumes/data/mac-mini-archive/mini-tmp-scratch/2026-10-23/hos_comp_j0175_prep0540/pool_v01.json \
  --out-dir /Users/benjaminoats/_desk/logs/J0175-full-picture-qa
```

Output (`COMPILATION_PICTURE_QA_v01.md` / `COMPILATION_PICTURE_QA_v01.json`):
```text
WARN   0:54 row code_graphic_comp_card_01 code_graphic_comp_card_01.mp4: low detail: edge density 0.0104 < film p5 0.0105
WARN   9:24 row code_graphic_comp_card_02 code_graphic_comp_card_02.mp4: low detail: edge density 0.0083 < film p5 0.0105
WARN  41:03 row code_graphic_comp_card_06 code_graphic_comp_card_06.mp4: low detail: edge density 0.0092 < film p5 0.0105
picture QA PASS: 0 of 51 cuts fail, 3 to look at -> /Users/benjaminoats/_desk/logs/J0175-full-picture-qa/PICTURE_QA.md, /Users/benjaminoats/_desk/logs/J0175-full-picture-qa/picture_qa_review.jpg
```

*(Note on the 3 `WARN` rows: all 3 are the J0204 chapter cards `card_01`, `card_02`, `card_06`, which intentionally use blurred background plates behind the centre Didot italic title; inspected full-size on `/Users/benjaminoats/_desk/logs/J0175-full-picture-qa/picture_qa_review.jpg`.)*

### 4.3 Whole New-Material & Per-Segment SFX / Bed Level Gate (`sfx_kit.py level`)

Whole new-material concatenated stems (`186.38 s`, `intro` + `card_01..06` + `bridge1..5` + `closing`, `COMPILATION_SFX_LEVEL_v01.json`):
```text
SFX level PASS: VO -16.0 LUFS, SFX -49.1 LUFS, 16 hits
```

Per-segment `sfx_kit.py level` results (`~/_desk/logs/J0175-seg-*-sfx.json`):
- `intro`: `PASS` (`VO -16.1 LUFS, SFX -49.1 LUFS, 2 hits`)
- `bridge1`: `PASS` (`VO -16.5 LUFS, SFX -49.1 LUFS, 1 hit`)
- `bridge2`: `PASS` (`VO -15.4 LUFS, SFX -49.1 LUFS, 1 hit`)
- `bridge3`: `PASS` (`VO -15.7 LUFS, SFX -49.1 LUFS, 2 hits`)
- `bridge4`: `PASS` (`VO -15.3 LUFS, SFX -49.1 LUFS, 1 hit`)
- `bridge5`: `PASS` (`VO -16.3 LUFS, SFX -49.1 LUFS, 2 hits`)
- `closing`: `PASS` (`VO -16.1 LUFS, SFX -49.1 LUFS, 1 hit`)

### 4.4 Music Continuity & Gap Check (`music_gate.py`)

- Each of the 6 films retains its own approved master score bed inside `film_NNN_norm.mp4`.
- Under the `186.38 s` of new material (`intro`, `card_01..06`, `bridge1..5`, `closing`), `004`'s score bed (`02_Video-Projects/004_Whats-Really-Inside-An-Atom/05_Music/hos004-full_score_bed_v01.mp3`, `75.0 BPM`) plays from distinct offsets (`BED_IN`) at `-32.0 LUFS` with sidechain ducking (`ratio=20, threshold=0.003`).
- `music_gate.longest_gap` on `hos_comp_new_bed_stem.wav`: `4.0 s` at `141.3 s` (passes the `<= 6.0 s` gap threshold).

---

## 5. Calls Parked for Chief (J0176)

1. **Final review & stage PASS** on the assembled 6-film compilation master (`/Volumes/data/mac-mini-archive/mini-tmp-scratch/2026-10-23/hos_comp_j0175_prep0540/hos_compilation_full_v01.mp4`, `49:53`, sha256 `4166f5b892953f75c5a3cd8147fdcb00a390ff848456d421072f7c68751c131c`).
2. **Mid-film end cards on `001`, `002`, `003`:** kept per `COMPILATION_PLAN_v01.md` risk 2 (only the 3 directional hand-offs on `005`, `006`, `004` were trimmed). Confirm whether to keep as assembled or trim `001`/`002`/`003` end cards.
3. **Reused `004` bed under new material:** confirm the compilation exception for reusing `hos004-full_score_bed_v01.mp3` under the intro, cards, bridges, and closing during the pre-30 Oct credit hold.
