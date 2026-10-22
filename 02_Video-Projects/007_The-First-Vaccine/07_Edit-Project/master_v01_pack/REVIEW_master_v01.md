# HOS 007 master v01 — worker evidence for Chief (J0830)

Original £0 warm chamber score at 60 BPM and HOS house ink ticks added under the locked VO. Approved join picture copied as a video stream with no edits. Chief authority: OWB #99 comment 6347492456, 22 Oct 2026. No spend, publishing or approval action.

Master: `/Volumes/data/mac-mini-archive/hos-007-vaccine/master_v01_J0830/hos_007_master_v01.mp4`

SHA-256: `e1880dd10bd627f0b36250eb688c6e3df8acd4f96fa7c46c740a834f96a31d83`. Duration 505.147 s. Separate VO, bed, SFX and mixed audio are SHA-verified in the same NAS folder; see MASTER_META_v01.json.

Measured encoded master: **−14.0 LUFS, −2.0 dBTP**.

## Tool outputs

### sfx_level.txt

```text
SFX level PASS: VO -16.1 LUFS, SFX -39.9 LUFS, 5 hits
WARN present: 5 hits in 8.4 min (fewer than 1 a minute)
```

### music_gate.txt

```text
music gate PASS: vaccine_score_bed_v01.mp3, 505.1 s, about None BPM, brief Pace: 58-64 BPM
```

### polish_gate.txt

```text
12_kite_storm   502.6s 12_kite_storm_t1.mp4         ok
polish gate PASS: 0 of 97 rows failed, 5 to look at -> /private/tmp/codex-j0830-wt/02_Video-Projects/007_The-First-Vaccine/07_Edit-Project/master_v01_pack/polish_gate.json
```

### picture_qa.txt

```text
WARN   0:15 row 03_table_three 03_table_three_t1.mp4: low detail: edge density 0.0154 < film p5 0.0224
WARN   4:26 row 05_quill_writes 05_quill_writes_t1.mp4: low detail: edge density 0.0184 < film p5 0.0224
WARN   4:51 row 08b_uneasy_hand 08b_uneasy_hand_t1.mp4: low detail: edge density 0.0223 < film p5 0.0224
WARN   5:11 row 01_page_turns 05_quill_writes_t1.mp4: low detail: edge density 0.0152 < film p5 0.0224
WARN   5:47 row 07b_quill_again 05_quill_writes_t1.mp4: low detail: edge density 0.0183 < film p5 0.0224
picture QA PASS: 0 of 97 cuts fail, 5 to look at -> /private/tmp/codex-j0830-wt/02_Video-Projects/007_The-First-Vaccine/07_Edit-Project/master_v01_pack/PICTURE_QA.md, /private/tmp/codex-j0830-wt/02_Video-Projects/007_The-First-Vaccine/07_Edit-Project/master_v01_pack/picture_qa_review.jpg
```

### gate_episode.txt

```text
> content-ops@0.1.0 gate:episode
> tsx scripts/gate-episode.ts --project /private/tmp/codex-j0830-wt/02_Video-Projects/007_The-First-Vaccine

# Episode gate — 007_The-First-Vaccine

**Decision:** PASS — VO / Gemini Veo allowed

| Check | Status | Detail |
|---|---|---|
| project_dir | OK | Project: /private/tmp/codex-j0830-wt/02_Video-Projects/007_The-First-Vaccine |
| prebuild_vidiq | OK | Pre-build vidIQ audit present and looks signed off. |
| script_file | OK | Script: 01_Script/vaccine_script_master_v01.md |
| script_review | OK | Script reviewer PASS 92.3/90 (need ≥90). |
| explorer_acts | OK | [EXPLORER ACTS] beats 3 (need ≥1). |
| visual_must | OK | [VISUAL MUST] count 26 (need ≥4). |
| teach | OK | [TEACH] count 5 (need ≥4). |
| chapters | OK | [CHAPTER CARD] count 4 (aim 4–6 film acts). |
| production_checklist | WARN | No PRODUCTION_CHECKLIST_V2.md yet — add before publish. |

Script score: **92.3/100** · PASS

Cold open: Every vaccine in the world is named after a cow. So how did a cow end up inside the most important medicine ever made? By the end of this film, you'll know how a milkmaid's hand, a country doctor and …
```

## Chief review still required

Hear the original score for period fit, mood changes, VO clarity and restrained ticks. Five existing low-detail picture warnings remain at 0:15, 4:26, 4:51, 5:11 and 5:47; the prior join reviewed-ok file is reused without additions. Five SFX hits across 8.4 min produce a sparse-hit warning. Tempo estimator reports no stable BPM on the restrained score; composition pulse is 60 BPM. Episode gate warns PRODUCTION_CHECKLIST_V2.md is absent; add before publishing. This report records tool results only and grants no film-stage PASS, final OK or UAT release.

## Additional verification

Source/master compressed video-stream SHA-256 hashes match exactly (`VIDEO_STREAM_VERIFY.json`). HOS `check_all.sh 007`: **ALL CHECKS PASS**. Generated untracked audio was excluded using a local Git ignore file; staged media remains checked. No media is staged or committed.
