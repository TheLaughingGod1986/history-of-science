# HOS 007 master v02 — worker evidence for Chief (J0856 / J0830)

Original £0 warm chamber score at **60.0 BPM** (`ac[20]/ac[0] = 0.8926`) with envelope ducking (`~18.1 dB` mean under VO in speech, `0` breaches, rising `+1.53 dB` in pauses) and **43 HOS house SFX cues** (39 soft ink ticks on every WHO card, date/place stamp, data pill, teach label and code graphic + 4 gentle page-turn whooshes on the chapter cards; never over the VO's first word). Approved join picture copied as a lossless video stream (`-c:v copy`) with no picture edits. Chief authority: OWB #99 comment 6347492456 & J0856 (Claude, acting Chief, 22 Oct 2026). No spend (`£0`), no ElevenLabs, no publishing or approval action.

Master v02: `/Volumes/data/mac-mini-archive/hos-007-vaccine/master_v02_J0856/hos_007_master_v02.mp4`  
SHA-256: `e55f680db246e12620a7827599415e6d9f513d614563bd213c0b2a42f9c69c97` · Duration: `505.147 s` (`12,123` frames)  
Separate VO, bed, SFX and mixed audio stems are SHA-verified in `/Volumes/data/mac-mini-archive/hos-007-vaccine/master_v02_J0856/` (prior `master_v01_J0830/` retained intact on NAS). See `MASTER_META_v01.json`.

## Before vs After (J0830 v01 → J0856 v02)

| Metric | Master v01 (J0830) | Master v02 (J0856) |
|---|---|---|
| Master file (NAS) | `master_v01_J0830/hos_007_master_v01.mp4` (`e1880dd1…`) | `master_v02_J0856/hos_007_master_v02.mp4` (`e55f680d…`) |
| Picture stream SHA-256 | `0aa1cf6383b02034…` (untouched copy) | `0aa1cf6383b02034…` (untouched copy, verified identical) |
| Encoded loudness / true peak | **−14.0 LUFS / −2.0 dBTP** | **−14.0 LUFS / −1.4 dBTP** |
| House SFX cues (`sfx_cues_v01.json`) | **5 hits** (`WARN: fewer than 1 a minute`) | **43 hits** (39 ink ticks + 4 chapter whooshes; **5.1 hits/min**, **0 WARNs**) |
| WHO cards cued (`tick`) | 0 / 6 | **6 / 6** (Jesty `150.83s`, Jenner `173.98s`, Hunter `203.03s`, Nelmes `235.01s`, Phipps `258.56s`, Pasteur `403.66s`) |
| Date/place stamps & data pills (`tick`) | 0 / 12 | **12 / 12** (`1700s · Smallpox`, `3 in 10 died`, `Dorset, 1774`, `Berkeley, Gloucestershire`, `14 May 1796`, `1 July 1796`, `One day · Three days`, `One week`, `22 years earlier`, `Soho, London · 1798`, `8 May 1980`, `300 million deaths`) |
| Teach labels & code graphics (`tick`) | 5 | **21 / 21** (all teach labels after `0.25s` + 3 standalone code graphics; `p1_vacca` at `0.25s` skipped so VO's first word is clean) |
| Chapter cards (`whoosh_card`) | 0 / 4 | **4 / 4** (`100.68s`, `230.31s`, `309.06s`, `401.81s`) |
| SFX integrated loudness (`sfx_kit.py level`) | **−39.9 LUFS** (VO −16.1 LUFS) | **−35.0 LUFS** (VO −16.1 LUFS; 18.9 LU under VO, 0 breaches) |
| Bed integrated loudness | −37.7 LUFS | **−34.4 LUFS** |
| Bed vs VO in speech (`vo_m - bed_m`) | Not measured | **18.12 dB under VO mean** (`p10 = 13.1 dB`, `p50 = 18.6 dB`, `p90 = 21.4 dB`, `min = 11.2 dB`, **0 breaches < 10 LU**) |
| Bed in speech vs pauses | Not measured | Speech **−35.21 LUFS** → Pause **−33.68 LUFS** (**+1.53 dB rise in pauses**) |
| `music_gate.py` tempo (`bpm`) | `None` (no pulse detected) | **60.0 BPM** (`Pace: 58-64 BPM`, onset autocorr `ac[20]/ac[0] = 0.8926 >= 0.10`) |

## Tool outputs

### sfx_level.txt (`sfx_kit.py level --vo ... --sfx ... --bed ...`)

```text
SFX level PASS: VO -16.1 LUFS, SFX -35.0 LUFS, 43 hits
```

### sfx_level.json (including `bed_vs_vo` and 60 BPM onset check)

```json
{
  "verdict": "PASS",
  "vo_integrated": -16.1,
  "sfx_integrated": -35.0,
  "hits": 43,
  "fails": [],
  "warns": [],
  "bed_integrated": -34.4,
  "bed_vs_vo": {
    "vo_integrated_lufs": -16.1,
    "bed_integrated_lufs": -34.4,
    "speech_bed_mean_lufs": -35.21,
    "pause_bed_mean_lufs": -33.68,
    "pause_rise_over_speech_db": 1.53,
    "speech_diff_under_vo_db": {
      "mean": 18.12,
      "p10": 13.1,
      "p50": 18.6,
      "p90": 21.4,
      "min": 11.2,
      "breaches_under_10lu": 0
    },
    "onset_check_60bpm": {
      "measured_bpm": 60.0,
      "lag_hops_50ms": 20,
      "autocorr_ratio_ac20_ac0": 0.8926,
      "threshold_ac0": 0.1
    }
  }
}
```

### music_gate.txt

```text
music gate PASS: vaccine_score_bed_v01.mp3, 505.1 s, about 60.0 BPM, brief Pace: 58-64 BPM
```

### polish_gate.txt

```text
12_kite_storm   502.6s 12_kite_storm_t1.mp4         ok
polish gate PASS: 0 of 97 rows failed, 5 to look at -> /private/tmp/j0856-hos-wt/02_Video-Projects/007_The-First-Vaccine/07_Edit-Project/master_v01_pack/polish_gate.json
```

### picture_qa.txt

```text
WARN   0:15 row 03_table_three 03_table_three_t1.mp4: low detail: edge density 0.0154 < film p5 0.0224
WARN   4:26 row 05_quill_writes 05_quill_writes_t1.mp4: low detail: edge density 0.0184 < film p5 0.0224
WARN   4:51 row 08b_uneasy_hand 08b_uneasy_hand_t1.mp4: low detail: edge density 0.0223 < film p5 0.0224
WARN   5:11 row 01_page_turns 05_quill_writes_t1.mp4: low detail: edge density 0.0152 < film p5 0.0224
WARN   5:47 row 07b_quill_again 05_quill_writes_t1.mp4: low detail: edge density 0.0183 < film p5 0.0224
picture QA PASS: 0 of 97 cuts fail, 5 to look at -> /private/tmp/j0856-hos-wt/02_Video-Projects/007_The-First-Vaccine/07_Edit-Project/master_v01_pack/PICTURE_QA.md, /private/tmp/j0856-hos-wt/02_Video-Projects/007_The-First-Vaccine/07_Edit-Project/master_v01_pack/picture_qa_review.jpg
```

### gate_episode.txt

```text
> content-ops@0.1.0 gate:episode
> tsx scripts/gate-episode.ts --project /private/tmp/j0856-hos-wt/02_Video-Projects/007_The-First-Vaccine

# Episode gate — 007_The-First-Vaccine

**Decision:** PASS — VO / Gemini Veo allowed

| Check | Status | Detail |
|---|---|---|
| project_dir | OK | Project: /private/tmp/j0856-hos-wt/02_Video-Projects/007_The-First-Vaccine |
| prebuild_vidiq | OK | Pre-build vidIQ audit present and looks signed off. |
| script_file | OK | Script: 01_Script/vaccine_script_master_v01.md |
| script_review | OK | Script reviewer PASS 92.3/90 (need ≥90). |
| explorer_acts | OK | [EXPLORER ACTS] beats 3 (need ≥1). |
| visual_must | OK | [VISUAL MUST] count 26 (need ≥4). |
| teach | OK | [TEACH] count 5 (need ≥4). |
| chapters | OK | [CHAPTER CARD] count 4 (aim 4–6 film acts). |
| production_checklist | WARN | No PRODUCTION_CHECKLIST_V2.md yet — add before publish. |

Script score: **92.3/100** · PASS
```

## Chief review still required

Hear master v02 for musical fit, 60.0 BPM harp pulse, VO clarity and the 43 house SFX cues across all teaching moments and chapter cards. Picture stream is identical (`VIDEO_STREAM_VERIFY.json`: `SHA256=0aa1cf6383b02034c5a7b6ded41ea24549e59b0bb4d7031445775d5ce9fd9915`). This report records tool results only and grants no film-stage PASS, final OK or UAT release.
