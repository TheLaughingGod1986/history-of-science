# HOS Compilation Film: Full Assembly & Gate Report v02 (J0175)

**Worker:** Gemini (`gemini-agy`) — 23 Oct 2026  
**Branch / PR:** `cursor/j0175-compilation-assembly` (HOS PR #300)  
**Spend:** £0 / 0 credits (house SFX kit, £0 Pillow/Didot closing end card, J0204 code graphics, existing 004 score bed under new segments).  
**v02 Change (Chief FIX on J0176):** Trimmed mid-film end cards on `001` (`359.35 s`, before `359.40 s` card xfade), `002` (`530.15 s`, before `530.20 s` card xfade), and `003` (`406.20 s`, before `406.25 s` card xfade) so no mid-compilation end screens or subscribe cards appear inside the 6-film arc.

---

## 1. Deliverable Master & Loudness

- **Output MP4 (NAS):** `/Volumes/data/mac-mini-archive/mini-tmp-scratch/2026-10-23/hos_comp_j0175_prep0540/hos_compilation_full_v02.mp4`
- **SHA-256:** `8282ffa8eb09e3a7cf1420562d70e14a428a0ae0489b3fdeccf5e4aeffe98490`
- **Duration:** `2958.188 s` (**`49:18`**, inside the 45–60 min lock)
- **Format:** `1920x1080`, `30/1` fps CFR, `yuv420p`, AAC `48000 Hz` stereo (`256 kbps`, `+faststart`)
- **Whole-Cut Loudness (`ffmpeg loudnorm` measurement):**
  - Integrated: **`-14.32 LUFS`** (target `-14.0 LUFS`)
  - True Peak: **`-1.16 dBTP`** (ceiling `-1.0 dBTP`)
  - LRA: **`4.10 LU`**

---

## 2. Chapters List (for YouTube Description)

From `COMPILATION_CHAPTERS_v02.txt`:

```text
0:00 Six discoveries, one question
0:53 The Hidden Circle
9:23 Built From Air
17:57 The Invisible Enemy
24:14 The Empty Chairs
33:22 A Light Through Skin
40:27 Inside the Atom
```

---

## 3. Running Order & Segment Timeline (v02 — All 6 Mid-Film Hand-Offs & End Cards Trimmed)

| # | Start (`m:ss`) | Start (`s`) | Duration (`s`) | Kind | Segment / Film | Notes |
|---|---:|---:|---:|---|---|---|
| 1 | `0:00` | `0.000` | `52.533` | `segment` | `intro` | 14 label-free windows across all 6 masters, 2 ink ticks |
| 2 | `0:53` | `52.533` | `3.000` | `card` | `card_01` | *The Hidden Circle* (J0204 chapter card + tick) |
| 3 | `0:56` | `55.533` | `489.200` | `film` | `005` | Harvey master normalised, trimmed at `489.20 s` (pause `488.69–489.25 s`, before hand-off & end card) |
| 4 | `9:05` | `544.733` | `18.000` | `segment` | `bridge1` | 005 loop -> `code_graphic_comp_timeline_b1` (`1628 · HARVEY`) -> 006 canopy/willow/balance |
| 5 | `9:23` | `562.733` | `3.000` | `card` | `card_02` | *Built From Air* (J0204 chapter card + tick) |
| 6 | `9:26` | `565.733` | `493.567` | `film` | `006` | Trees master normalised, trimmed at `493.55 s` (pause `493.13–493.76 s`, before hand-off & end card) |
| 7 | `17:39` | `1059.300` | `17.900` | `segment` | `bridge2` | 006 leaf & shutters -> 001 microbes & ward basin + 1 ink tick |
| 8 | `17:57` | `1077.200` | `3.000` | `card` | `card_03` | *The Invisible Enemy* (J0204 chapter card + tick) |
| 9 | `18:00` | `1080.200` | `359.367` | `film` | `001` | Germs master normalised (`720p24` -> `1080p30`, `1.5x` upscale), trimmed at `359.35 s` (before `359.40 s` end card xfade; last word `357.64 s`) |
| 10 | `24:00` | `1439.567` | `14.700` | `segment` | `bridge3` | 001 basin -> 002 cards -> `code_graphic_comp_timeline_b3` (`1779`, `1860s`) -> desk |
| 11 | `24:14` | `1454.267` | `3.000` | `card` | `card_04` | *The Empty Chairs* (J0204 chapter card + tick) |
| 12 | `24:17` | `1457.267` | `530.167` | `film` | `002` | Periodic table master normalised (`1080p24` -> `1080p30`), trimmed at `530.15 s` (before `530.20 s` end card xfade; last word `528.88 s`) |
| 13 | `33:07` | `1987.433` | `14.300` | `segment` | `bridge4` | 002 vacancy -> 003 dark screen -> lit screen reveal + 1 ink tick |
| 14 | `33:22` | `2001.733` | `3.000` | `card` | `card_05` | *A Light Through Skin* (J0204 chapter card + tick) |
| 15 | `33:25` | `2004.733` | `406.200` | `film` | `003` | X-rays master normalised (`1080p24` -> `1080p30`), trimmed at `406.20 s` (before `406.25 s` end card xfade; last word `403.52 s`) |
| 16 | `40:11` | `2410.933` | `15.733` | `segment` | `bridge5` | 003 screen -> 004 gold foil -> `code_graphic_comp_timeline_b5` (`1869`, `1895`) -> foil |
| 17 | `40:27` | `2426.667` | `3.000` | `card` | `card_06` | *Inside the Atom* (J0204 chapter card + tick) |
| 18 | `40:30` | `2429.667` | `491.400` | `film` | `004` | Atom master normalised, trimmed at `491.40 s` (pause `491.06–491.68 s`, before hand-off & end card) |
| 19 | `48:41` | `2921.067` | `37.100` | `segment` | `closing` | Six objects pullback -> `code_graphic_comp_timeline_close` (`1911`) -> cream Didot closing card (`31.09–34.59 s`) + 2.5 s hold & fade |

---

## 4. Automated Gate Outputs (Pasted Verbatim)

### 4.1 Whole-Cut Polish Gate (`polish_gate.py`)

Command:
```bash
python3 "/Users/benjaminoats/YouTube/orbit-with-ben/scripts/polish_gate.py" \
  /Volumes/data/mac-mini-archive/mini-tmp-scratch/2026-10-23/hos_comp_j0175_prep0540/hos_compilation_full_v02.mp4 \
  --cuts /Volumes/data/mac-mini-archive/mini-tmp-scratch/2026-10-23/hos_comp_j0175_prep0540/cuts_new_v02.json \
  --out /Users/benjaminoats/_desk/logs/J0175-v02-polish.json
```

Output (`COMPILATION_POLISH_GATE_v02.json`):
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
bridge3_01  1441.7s /Volumes/data/mac-mini-archi ok
bridge3_02  1445.6s /Volumes/data/mac-mini-archi ok
bridge3_03  1449.4s code_graphic_comp_timeline_b ok
bridge3_04  1452.6s /Volumes/data/mac-mini-archi ok
code_graphic_comp_card_04  1455.8s code_graphic_comp_card_04.mp ok
bridge4_01  1989.8s /Volumes/data/mac-mini-archi ok
bridge4_02  1994.9s /Volumes/data/mac-mini-archi ok
bridge4_03  1999.7s /Volumes/data/mac-mini-archi ok
code_graphic_comp_card_05  2003.2s code_graphic_comp_card_05.mp ok
bridge5_01  2413.7s /Volumes/data/mac-mini-archi ok
bridge5_02  2418.6s /Volumes/data/mac-mini-archi ok
bridge5_03  2422.7s code_graphic_comp_timeline_b ok
bridge5_04  2425.4s /Volumes/data/mac-mini-archi ok
code_graphic_comp_card_06  2428.2s code_graphic_comp_card_06.mp WARN low detail: edge density 0.0092 < film p5 0.0105
closing_01  2922.7s /Volumes/data/mac-mini-archi ok
closing_02  2924.8s /Volumes/data/mac-mini-archi ok
closing_03  2926.4s /Volumes/data/mac-mini-archi ok
closing_04  2928.4s /Volumes/data/mac-mini-archi ok
closing_05  2930.8s /Volumes/data/mac-mini-archi ok
closing_06  2933.9s /Volumes/data/mac-mini-archi ok
closing_07  2936.9s /Volumes/data/mac-mini-archi ok
closing_08  2942.9s /Volumes/data/mac-mini-archi ok
closing_09  2949.3s code_graphic_comp_timeline_c ok
closing_10  2954.5s /Volumes/data/mac-mini-archi ok
code_graphic_comp_closing_end_card  2953.9s /Volumes/data/mac-mini-archi ok
polish gate PASS: 0 of 51 rows failed, 3 to look at -> /Users/benjaminoats/_desk/logs/J0175-v02-polish.json
```

### 4.2 Whole-Cut Picture QA (`picture_qa.py`)

Command:
```bash
python3 "/Users/benjaminoats/YouTube/orbit-with-ben/scripts/picture_qa.py" \
  /Volumes/data/mac-mini-archive/mini-tmp-scratch/2026-10-23/hos_comp_j0175_prep0540/hos_compilation_full_v02.mp4 \
  --cuts /Volumes/data/mac-mini-archive/mini-tmp-scratch/2026-10-23/hos_comp_j0175_prep0540/cuts_new_v02.json \
  --pool /Volumes/data/mac-mini-archive/mini-tmp-scratch/2026-10-23/hos_comp_j0175_prep0540/pool_v01.json \
  --out-dir /Users/benjaminoats/_desk/logs/J0175-v02-picture-qa
```

Output (`COMPILATION_PICTURE_QA_v02.md` / `COMPILATION_PICTURE_QA_v02.json`):
```text
WARN   0:54 row code_graphic_comp_card_01 code_graphic_comp_card_01.mp4: low detail: edge density 0.0104 < film p5 0.0105
WARN   9:24 row code_graphic_comp_card_02 code_graphic_comp_card_02.mp4: low detail: edge density 0.0083 < film p5 0.0105
WARN  40:28 row code_graphic_comp_card_06 code_graphic_comp_card_06.mp4: low detail: edge density 0.0092 < film p5 0.0105
picture QA PASS: 0 of 51 cuts fail, 3 to look at -> /Users/benjaminoats/_desk/logs/J0175-v02-picture-qa/PICTURE_QA.md, /Users/benjaminoats/_desk/logs/J0175-v02-picture-qa/picture_qa_review.jpg
```

*(Note on the 3 `WARN` rows: all 3 are the J0204 chapter cards `card_01`, `card_02`, `card_06`, which intentionally use blurred background plates behind the centre Didot italic title; inspected full-size on `/Users/benjaminoats/_desk/logs/J0175-v02-picture-qa/picture_qa_review.jpg`.)*

### 4.3 Whole New-Material & Per-Segment SFX / Bed Level Gate (`sfx_kit.py level`)

Whole new-material concatenated stems (`186.38 s` = `3.11 min`, `intro` + `card_01..06` + `bridge1..5` + `closing`, `COMPILATION_SFX_LEVEL_v02.json`):
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

1. **Final review & stage PASS** on the assembled 6-film compilation master `v02` (`/Volumes/data/mac-mini-archive/mini-tmp-scratch/2026-10-23/hos_comp_j0175_prep0540/hos_compilation_full_v02.mp4`, `49:18`, sha256 `8282ffa8eb09e3a7cf1420562d70e14a428a0ae0489b3fdeccf5e4aeffe98490`), with all 6 mid-film end cards and hand-offs trimmed (`005 @ 489.20s`, `006 @ 493.55s`, `001 @ 359.35s`, `002 @ 530.15s`, `003 @ 406.20s`, `004 @ 491.40s`).
2. **Reused `004` bed under new material:** confirm the compilation exception for reusing `hos004-full_score_bed_v01.mp3` under the intro, cards, bridges, and closing during the pre-30 Oct credit hold.
