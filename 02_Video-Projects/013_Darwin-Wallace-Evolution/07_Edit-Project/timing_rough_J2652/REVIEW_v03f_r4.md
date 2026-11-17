# J2652 (v03f-r4): £0 card & phone-readability polish per Claude #6945397541 & Chief #6957443445

17 November 2026, Gemini (`gemini`). Follows Chief timing PASS & reopen [#6957443445](https://github.com/TheLaughingGod1986/history-of-science/pull/180#issuecomment-6957443445) and Claude's 390 px sheet review [#6945397541](https://github.com/TheLaughingGod1986/history-of-science/pull/180#issuecomment-6945397541) on HOS PR #551.

**Spend:** £0 cash / 0 subscription credits. No Veo or ElevenLabs spend, no audio edit, no YouTube or Buffer change. All earlier plans (`PICTURE_PLAN_v01.json`, `PICTURE_PLAN_v02.json`, `PICTURE_PLAN_v03*.json`), NAS clips (`v03f`, `v03f_r3`), and roughs (`v01`..`v03f_r3`) remain untouched on git and on the NAS.

## Three reviewer items from #6945397541 — all closed in `v03f-r4`

1. **Unclipped bottom-left archival source credits (`ARCHIVE_CREDITS` in `_build_v03f_r4.py`):**
   - Removed the `[:52]` character slice that clipped `P2:12a`, `P3:10a`, `P4:06b`, `P5:05b`, and `P6:04b` mid-phrase/word.
   - Replaced with explicit full-word, year-terminated credits verified to fit within `x <= 1243` (`>= 677 px` right margin on `1920x1080`) in white Didot italic (`40 px`, up from `28 px`, with dark drop-shadow and `1 px` stroke weight):
     - `P2:12a` (`darwin_tree_1837`): `Cambridge University Library · MS DAR 121:36 (1837)`
     - `P2:09_beat2` (`gould_finches_1845`): `John Gould · Journal of Researches (1845)`
     - `P3:10a` (`vestiges_1844_title`): `Robert Chambers · Vestiges of the Natural History of Creation (1844)`
     - `P4:06b` (`malthus_1798_title`): `Thomas Robert Malthus · Principle of Population, 1st ed. (1798)`
     - `P5:05b` (`origin_1859_title`): `Charles Darwin · On the Origin of Species, 1st ed. (1859)`
     - `P5:09` (`darwinism_1889_title`): `Alfred Russel Wallace · Darwinism, 1st ed. (1889)`
     - `P6:04b` (`mendel_1866_paper`): `Gregor Mendel · Versuche über Pflanzen-Hybriden (1866)` (shown outside the `475.50–479.30 s` WHO window)

2. **Enlarged 390 px phone-width labels, badges, tags, and custom vector arrows:**
   - **Top-left anchored cue badges** (including `1,250 COPIES PRE-SOLD`, `ONE SHELL PER ISLAND`, `MOST NEVER SURVIVE`, `125,660 SPECIMENS`, `WASHED AWAY BY BLENDING`): enlarged `54 -> 62 px` with `1 px` Didot stroke weight and dark shadow so thin serif hairlines remain crisp after `1920 -> 390` LANCZOS downsampling.
   - **`P1:10_cg_globe_arc` year & page tags:** moved `1844 / 230 PAGES` and `1858 / PACKET` into a framed dark-brown house panel (`1015..1835`) and enlarged `34 -> 58 / 46 px`.
   - **`P3:03_cg_malthus_curve_beat1` & `beat2`:** enlarged `OFFSPRING BORN` (`40 -> 58 px`) and `FOOD SUPPLY` (`40 -> 56 px`).
   - **WHO lower-third cards & chart labels:** enlarged WHO cards (`48/34 -> 54/42 px`), `P5:07` timeline years (`36 -> 48 px`), and secondary labels across `P1:08`, `P2:06b`, `P2:09`, `P2:10b`, `P3:06`, `P3:09a`, `P3:12`, `P4:05`, `P4:07b`, `P5:02b`, `P5:04b`, and `P6:03` (`34–44 -> 46–56 px`).
   - **Custom vector arrows (`P1:08` beats 1 & 3, `P4:07b`):** `Didot.ttc` lacks `U+2192` (`→`), which produced `.notdef` boxes under stroke weight; replaced with hand-inked vector arrows (`_draw_vector_arrow`), verified directly on `CONTACT_SHEET_v03f_r4_390px.jpg`.

3. **`P2:01_card_p02` Part II title verified & sampled in window:**
   - Confirmed `P2:01_card_p02` (`75.12–81.22 s`) renders `Part II / The Birds He Forgot to Label` throughout `chapter_title_window_s` `[75.12, 77.62]` (`0.00–2.50 s`), then transitions to the animated case-file compass motif (`77.62–81.22 s`) so no card holds still over `4 s`. The `v03f-r3` contact sheet had sampled midpoint `t = 3.05 s > 2.50 s`.
   - In `v03f-r4`, `P2:01_card_p02`'s hero still is sampled at `t = 1.25 s` (`76.37 s`, mid-title window), and `code_graphics_v03f/CHAPTER_WINDOWS_v03f_r4_390px.jpg` shows both windows (`t = 1.25 s` and `t = 3.80 s`) side by side for `P2:01` and `P6:01`.

## QA gates & seven checks from Chief ruling #6808560760

- `polish_gate.py` (`code_graphics_v03f/polish_gate_v03f_r4.txt`): **PASS** (`0 of 35 rows failed`, luma mean `52.82–115.86 >= 28.0`, luma std `23.27–80.22 >= 18.0`, `near_black: PASS` on `35/35`; 2 relative 5th-percentile edge-density look-at notes on `P3:03_beat1` `0.0487` and `P6:03_beat1` `0.0464` vs `0.0490` p5, visually inspected on `picture_qa_v03f_r4/picture_qa_review.jpg`).
- `picture_qa.py` (`code_graphics_v03f/picture_qa_v03f_r4.txt`): **PASS** (`0 of 35 cuts fail`).
- Complete 515 s `v03f-r4` diagnostic rough on the NAS (`hos_013_timing_rough_J2652_v03f_r4bb.mp4`, SHA-256 `522caea01fc2077e12e2b04a330ee6ccff4904e95d91202e9019d46ee92549ed`): `93/104` real video beats (`35` finished `v03f-r4` £0 renders + `58` watermarked Pass-1 takes) + `11` explicit Part 5/6 slates awaiting `J2529`, full `ffmpeg` decode exit `0`.

| # | Check | Status | Detail |
|---:|---|---|---|
| 1 | Never a picture cut inside a word (all 14 moved) | **PASS** | `test_picture_plan_v03f.py` (`6/6 OK`) + `clip_check.py` (`passed=true`, `0` errors across 104 rows). |
| 2 | Sentence boundary preferred; internal cuts at `>=120 ms` gap / clause / breath; `<= 7.0 s` max | **PASS** | Chief `J2979` & `#6957443445` PASS on `PICTURE_PLAN_v03f.json` (unchanged SHA-256 `2d1d8b724a96bd52...`). |
| 3 | Graphic and overlay rows capped at 8 s | **PASS** | All 35 `v03f-r4` beats `<= 6.96 s`, passing `polish_gate` & `picture_qa` (`0` fails), with unclipped credits, enlarged 390 px labels, vector arrows, and zero overlaps. |
| 4 | J1310-locked WAV is source of truth (`vo_sha256` updated, audio unchanged) | **PASS** | SHA-256 `837178125a72fb250d255f1039c5cb7f8630bbb313cf23801a1155f257d796e0` verified before muxing. |
| 5 | Callback gets `<= 4.20 s` real unused tail, trimmed without stretch/loop | **PASS** | `P6:08a_reuse_study_beaks_callback` directly trims `3.82–7.38 s` (`3.56 s <= 4.20 s`) of `P01_01_study_beaks_t1.mp4`. |
| 6 | Word-level onset fields added from J1310 transcript timings | **PASS** | All 43 anchored cues carry `word_index`, `onset_s`, `display_start_s`, `display_end_s` (`<= 3.80 s`). |
| 7 | Review the three optional own-code replacements in `COST_OPTIONS_v01.md` | **PASS (retain Quality)** | `P3:05a`, `P3:07b`, `P4:09b` already have minted Pass-1 Quality takes (`0` credit savings). |

## Sheets committed in PR #551 for cloud/non-producer review

- `code_graphics_v03f/CONTACT_SHEET_v03f_r4_390px.jpg` (all 35 `v03f-r4` free renders at 390 px)
- `code_graphics_v03f/CHAPTER_WINDOWS_v03f_r4_390px.jpg` (`P2:01` & `P6:01` title vs post-title windows at 390 px)
- `timing_rough_J2652/phone_contact_v03f_r4_01.jpg` .. `phone_contact_v03f_r4_06.jpg` (all 104 rough beats at 390 px)
- Stills inspected directly via `read_file`; no audio or moving-video perception claimed (`capabilities: empty`). Parked for non-producer review (Claude `#6945397541` follow-up) rather than self-approving graphics rendered in this session.
