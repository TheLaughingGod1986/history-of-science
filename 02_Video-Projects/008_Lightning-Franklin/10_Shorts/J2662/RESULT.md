# J2662 — HOS 008 Short C v07 (J2485 Fix List)

MacBook (`macbook`, Gemini 4 Carbon), 17 Nov 2026. £0. No upload, no schedule, no new Flow, Vertex or ElevenLabs take.

Master (on `studio-live` NAS, not in git): `/Volumes/data/studio-live/History Of Science/02_Video-Projects/008_Lightning-Franklin/10_Shorts/hos_008_short_C_v07.mp4`
- **SHA-256:** `a3404a314a444a0fd987ca648c28425be8afb768f83748ee64e553951c8f06a8`
- **Format / Duration:** `22.083 s` (`530` frames at `24 fps`, `936×1664`), integrated loudness **`-14.0 LUFS`**, true peak **`-2.5 dBTP`**.
- **Stems on NAS (`10_Shorts/J2662_v07/` & `05_Music/`):**
  - `vo.wav`: `50d65ab8eaf1bd11d3fe93a39691da5ed4e00231019d975d41c21e12d65c9a57`
  - `bed.wav`: `62a8c10394aea7bdd394f03fafd2ed09fbb6d0ee05a1dc1a323faef3c8408517`
  - `sfx.wav`: `ecd5b8b9add107deacf98a17c2b992da3cf8aa3501f18ebf412b396535939b0c`
  - `05_Music/hos_008_short_C_v07_bed.wav`: `cf4143abdb8276185d7229664dd32a53adf1d80e018a451d23683a6f2f3cd690`
- **QA Contact Sheets on NAS (`10_Shorts/J2662_v07/sheets/`):**
  - `hos_008_short_C_v07_open_sheet.jpg`: `2cf9944bddb85cb0ea469a90c7497c77cde63412d77cae4d1c3a5abffac3c72a`
  - `picture_qa_review_v07.jpg`: `90135e645f52f264cbdefff5f5cbd70ce04937580fbf481a058569fc82322dee`
  - `v07_1fps_sheet.jpg`: `0e7288f43601782cb0484235ad192799c0e08443a48dff2f5569bfb2e68b6ad6`
- **Prior NAS versions preserved untouched:** `hos_008_short_C_v03.mp4` (`9f25a16de5fc7d454be7adbc0e301614c7b060cd28b10cd076bcd2b4a6642161`) and interim `v04`–`v06` remain untouched on the NAS.

## J2485 Fixes Verified

1. **FIX 1 (`S01` VO surprise word `<= 1.50 s`, £0):** Chief h94 pre-approved 6-word sentence 1 (`"That lightning rod was Franklin's idea."`, 55 spoken words total across the Short) built from `hos_008_short_C_s01_v03.wav` (`0.065 s` lead trim, zero-crossing `"rooftop"` excision with `15 ms` crossfade, `atempo=1.06`):
   - `"That"`: `0.033–0.146 s` (`vo_onset = 0.00–0.033 s <= 0.15 s`; independent `faster-whisper` ASR `0.000–0.100 s`)
   - `"lightning"`: `0.187–0.489 s` (ASR `0.100–0.300 s`)
   - `"rod"`: `0.565–0.753 s` (subject completed at **`0.753 s <= 1.50 s`**; ASR `0.300–0.640 s`)
   - `"was"`: `0.791–0.961 s` (ASR `0.640–0.820 s`)
   - `"Franklin's"`: **`0.980–1.489 s`** (surprise word starts at **`0.980 s`** and finishes at **`1.489 s <= 1.50 s`**; independent ASR **`0.820–1.480 s <= 1.50 s`**)
   - `"idea"`: `1.565–1.886 s` (ASR `1.480–1.780 s`)
   - Longest inter-word pause in sentence 1: **`0.076 s <= 0.15 s`**.
   - `S01` cut1 = `49` frames (`2.042 s <= 3.0 s`); unmodified body VO (`5.720–24.400 s` of `hos_008_short_C_v02.wav`) starts at `2.100 s` and ends at `20.780 s` (`tail_gap = 1.303 s <= 1.50 s`).
2. **FIX 2 (Body captions):** Every body caption `t1` clamped to `min(end + 0.18, next_chunk_t0 - 0.04, TOTAL - 1.05)` (`>= 40 ms` gap at every boundary, zero double-rendered overlaps); balanced 9-chunk sentence/clause grouping (`4–7` words per chunk, zero 1–2 word orphans).
3. **FIX 3 (`S07`, `06_rod_fitting_c1_t1.mp4`):** Source offset shifted `1.50 s -> 3.10 s` (`3.10–5.808 s`), eliminating the `1.8–2.9 s` shovel-blade morph.
4. **FIX 4 (`S06`, `06_rod_fitting_t1.mp4`):** Source offset shifted `1.50 s -> 4.00 s` (`4.00–6.792 s`), eliminating the `2.8–3.7 s` vanishing hammer handle.
5. **FIX 5 (`S01`, `S02`, `loop_tail` crops):** `S01` & `loop_tail` (`19_skyline_strike_t1.mp4`) `crop = [600, 0, 405, 720]` (centres struck skyscraper spire); `S02` (`01_house_rod_t1.mp4`) `crop = [180, 0, 405, 720]` (centres Franklin's brick gable, chimney, and lightning rod); `S03–S08` `crop = [438, 0, 405, 720]` (`2.3111x <= 2.35x`).

## Gate Outputs

| Gate | Result |
|---|---|
| `gate_shorts_open.py check --air-date 2026-12-02` | **PASS** (`dur=22.08s`, `motion=43.08`, `f0diff=7.71`, `cut1=2.04s`, `vo_onset=0.00s`, `tail_gap=1.30s`, `-14.0 LUFS`, `-2.5 dBTP`, `0/23` & `0/45` padded frames) |
| `polish_gate.py` | **PASS** (`0 of 9 rows failed`, 1 low-detail warn on `S08`) |
| `picture_qa.py --terminal-loop contract.json` | **PASS** (`0 of 9 cuts fail`, `2.31x` sharpness warns, prescribed terminal loop classified) |
| `music_gate.py` | **PASS** (`hos_008_short_C_v07_bed.wav`, `23.1 s`, ~`66.7 BPM`, brief `Pace: 64-72 BPM`) |
| `sfx_kit.py level` | **PASS** (`VO -20.0 LUFS, SFX -40.8 LUFS, 5 hits`) |
| `atempo_check.py` | **PASS** (`no new build above 1.06`) |
| `check_all.sh 02_Video-Projects/008_Lightning-Franklin` | **ALL CHECKS PASS** |

Both the muxed audio stream and all 23 1-fps frames (`00s..22s`) plus the 9 `picture_qa` review frames were inspected directly; Ben's final watch remains the required human watch-and-listen UAT step after review.
