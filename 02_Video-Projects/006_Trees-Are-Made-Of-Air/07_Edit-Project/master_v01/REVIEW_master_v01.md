# HOS 006 master v01 — J0835

Worker delivery for Chief review, not a final PASS or upload authorization.

Chief authority: J0835 reopened by Claude acting Chief, 22 Oct 2026 17:52Z. The reopening supersedes the original 30 Oct music-credit wait: original numpy score + house SFX, £0; no ElevenLabs spend.

## Delivery

- Master: `/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project/master_v01/hos_006_master_v01.mp4`
- NAS (copied, SHA-256 verified): `/Volumes/data/mac-mini-archive/YouTube/History Of Science/02_Video-Projects/006_Trees-Are-Made-Of-Air/09_Final-Export/master_v01/hos_006_master_v01.mp4`
- SHA-256 (both copies): `bcafbf4e04ce72f230569f9c4050b9d43b6a364374c4d7e14360c4b62c8e67ee`
- Video: 1920×1080 H264, 24 fps, 12,188 frames, 507.833333 s. Container/audio: 508.000 s (0.167 s AAC audio tail).
- Source: full_join_v03_teach, SHA-256 `d24a08ee94489379dd8e550700b9e31ec2fd4636c35158d037949248ecf8eb34`.
- Source and master compressed video SHA-256: `a67d3735f75f8763d77b063342c68e6b3946f27617555c7ec03802f051399abe` — byte-identical picture; no recut or new picture generation.
- Separate stems: `/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project/master_v01/stem_vo_v01.wav` (`-16.1 LUFS`); `/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/006_Trees-Are-Made-Of-Air/05_Music/trees006_score_bed_v01.mp3` (`-32.9 LUFS`, speech diff under VO: mean `16.3 dB`, p50 `16.1 dB`, p90 `20.3 dB`, min `11.6 dB >= 10.0 dB`, `0` breaches); `/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/006_Trees-Are-Made-Of-Air/06_Sound-Effects/stem_sfx_v01.wav` (`-33.6 LUFS`). Mix: `/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project/master_v01/audio_master_v01.m4a`.
- New original HOS score: G-major/E-minor/C/D family, warm sustained viol-like harmonics, soft harp notes at `66.7 BPM` (`0.900 s` beat); 3 s transitions at chapter cards (61.667 / 178.667 / 273.500 / 365.417 s). Explain chapters lift the harp; wonder chapters soften it. Full-runtime bed; no loops of an earlier film's music.
- House HOS ink ticks on all 17 teach overlays + all 3 DATA code graphics (`#14` 200 lb balance counter at `67.425 s`, `#78` 50% carbon pie chart at `423.675 s`, `#86` 4 in 10,000 specimen lens at `470.758 s`) and restrained soft chapter whooshes on all 4 chapter cards: **24 cues total** (`0` fails, `0` warns). No rumbles on this quiet experiment story. Cues/levels in `sfx_cues_v01.json` and `sfx_level_v01.json`.
- Two-pass loudnorm target -14 LUFS/-1.5 dBTP (headroom below the -1 dBTP ceiling); no speech retiming or script changes.

## Machine checks (pasted outputs)

### music_gate.txt

```text
music gate PASS: trees006_score_bed_v01.mp3, 507.8 s, about 66.7 BPM, brief Pace: 60-72 BPM
```

### picture_qa.txt

```text
WARN   2:18 row 15_desk_candle 15_desk_candle_t1_above_desk_v03.mp4: low detail: edge density 0.0271 < film p5 0.0272
WARN   3:01 row 01_soil_to_sky 01_soil_to_sky_t1.mp4: low detail: edge density 0.0219 < film p5 0.0272
WARN   5:24 row 09_bubbles_again 05_bubbles_macro_t1_from4.500.mp4: low detail: edge density 0.0245 < film p5 0.0272
WARN   6:32 row 05_sums_add_up 05_sums_add_up_t1.mp4: low detail: edge density 0.0248 < film p5 0.0272
WARN   8:17 row 23_carbon_atom 23_carbon_atom_t1.mp4: low detail: edge density 0.0238 < film p5 0.0272
picture QA PASS: 0 of 91 cuts fail, 5 to look at -> /Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project/master_v01/PICTURE_QA.md, /Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project/master_v01/picture_qa_review.jpg
```

### polish_gate.txt

```text
15_desk_candle   138.0s 15_desk_candle_t1_above_desk WARN low detail: edge density 0.0271 < film p5 0.0272
01_soil_to_sky   181.2s 01_soil_to_sky_t1.mp4        WARN low detail: edge density 0.0219 < film p5 0.0272
09_bubbles_again   324.2s 05_bubbles_macro_t1_from4.50 WARN low detail: edge density 0.0245 < film p5 0.0272
05_sums_add_up   392.4s 05_sums_add_up_t1.mp4        WARN low detail: edge density 0.0248 < film p5 0.0272
23_carbon_atom   497.5s 23_carbon_atom_t1.mp4        WARN low detail: edge density 0.0238 < film p5 0.0272
polish gate PASS: 0 of 91 rows failed, 5 to look at -> /Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project/master_v01/polish_gate.json
```

### episode_gate.txt

```text
**Decision:** PASS — VO / Gemini Veo allowed
Script score: **93.7/100** · PASS
```

```text
SFX level PASS: VO -16.1 LUFS, SFX -33.6 LUFS, 24 hits
{
  "verdict": "PASS",
  "vo_integrated": -16.1,
  "sfx_integrated": -33.6,
  "hits": 24,
  "fails": [],
  "warns": []
}
ALL CHECKS PASS (repository check_all.sh 006)
```

Final mux measurement:

```text
Summary:

  Integrated loudness:
    I:         -14.0 LUFS
    Threshold: -24.6 LUFS

  Loudness range:
    LRA:         3.0 LU
    Threshold: -34.6 LUFS
    LRA low:   -16.1 LUFS
    LRA high:  -13.1 LUFS

  True peak:
    Peak:       -1.5 dBFS
[out#0/null @ 0xbe1044300] video:5047KiB audio:95239KiB subtitle:0KiB other streams:0KiB global headers:0KiB muxing overhead: unknown
frame=12188 fps=493 q=-0.0 Lsize=N/A time=00:08:28.00 bitrate=N/A speed=20.6x elapsed=0:00:24.70
```

## Chief review still required

- Listen to the complete film for musical fit, mix comfort, repeated/stumbled VO and chapter transitions. Worker has not made an aesthetic PASS.
- Tempo & bed level: `music_gate.py` reads `66.7 BPM` directly against the brief's `Pace: 60-72 BPM` (0 pace WARN, 0 fails), and `sfx_kit.py level --bed` PASSes with bed `-32.9 LUFS` vs VO `-16.1 LUFS` (mean `16.3 dB` under VO in speech, `0` breaches).
- Picture/polish use the unchanged `full_join_v02_teach/picture_qa_reviewed_ok_v02_teach.json` already used for v03: prior Chief reuse rulings and teach-card-edge seam rulings. No new waiver. First raw run without those rulings is preserved as `picture_qa_without_prior_rulings.txt`.
- Five existing low-detail WARNs remain at 2:18, 3:01, 5:24, 6:32 and 8:17. Review sheet remains in the local master pack (`picture_qa_review.jpg`); see v03 review for Chief's earlier inspection.
- No upload, scheduling or YouTube state change. £0 spend. Next: Chief listens/reviews, decides final PASS and Ben watch; Ben final check remains due 1 Nov.
