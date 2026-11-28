# J3871 exact-v04 recheck — still held

Codex covering. Rechecked unchanged v04 after J3965 merged (HOS main a5a8d27f97; OWB PR1420). This evidence supersedes the earlier gate result only; no media edit, Short PASS, UAT, upload, schedule, privacy, Buffer or spend. Prior failed versions and receipts are preserved. Draft ancestry: PR811 / J3816 2922143e, then PR814 / J3871 c8c3372e; this branch merges that draft with current main.

Video and NAS safety copy both SHA256 `3e21b51f9314df661b1556fc94ac313a6a73830a66c04ddfb59d33a8e2731dac`. VO and SFX also match prior hashes; see HASHES.json. No re-render ran.

## Remaining exact contract incompatibility

Source is 1280×720. The retained build recipe is `scale=3008:1692:flags=lanczos,crop=952:1692:1028:0,setsar=1,fps=30`. The validator models crop in original source coordinates, integer pixels only. The honest inverse crop is `[437.4468085106383,0,405.1063829787234,720]`; this is not representable by its supported integer-crop recipe. The diagnostic contract retains those true values and correctly fails `crop/output must contain integer pixels`. No crop was rounded or invented to secure an exemption. There is also a later exact-ratio restriction: output 952×1692 gives 952×16=15232 versus 1692×9=15228, so it is codec-rounded portrait rather than exact integer 9:16. That second restriction is established from code/arithmetic, not claimed as the first observed validator error.

The duration fix works: 17.1 s reaches framing validation. Tail source [0,0.9) still precedes opening [0.9,1.7); tail timeline [16.2,17.1), last VO word 15.78. Picture QA remains FAIL because the declaration is ineligible, and terminal reuse remains protected. No failed check waived. Separate Chief gate review is needed to decide support for the actual deterministic scale/crop recipe with rendered correspondence and codec rounding, or authorise a new edit. This exact-rerun-only brief does not authorise either.

## Fresh receipts

### open (exit 0)

```text
PASS  hos_009_s03_apple_head_v04.mp4  dur=17.1s  audio=-17.5dB  motion=24.4  f0diff=1.91  cut1=0.77s  vo_onset=0.07s  tail_gap=1.33s  vo_src=/Volumes/MiniWork/scratch/J3871-build-v04/vo.wav  dhash=dbc97cf9ddde3615
   full-bleed 0.00s  fills the frame  sharp above/middle/below=0.54/0.687/0.884  detail top/centre/bottom=13.16/12.33/19.22  spread top/bottom=39.42/33.28
   full-bleed 0.25s  fills the frame  sharp above/middle/below=0.555/0.677/0.876  detail top/centre/bottom=13.02/12.16/19.31  spread top/bottom=39.16/33.28
   full-bleed 0.50s  fills the frame  sharp above/middle/below=0.559/0.616/0.879  detail top/centre/bottom=13.11/12.32/19.34  spread top/bottom=39.19/33.31
   full-bleed whole Short  0/18 frames padded at one a second, 0/35 at two a second  padded stretches: none  no end card named in meta
   sheet /Volumes/MiniWork/scratch/J3871-recheck/02_Video-Projects/009_The-Falling-Moon-Gravity/10_Shorts/J3871/v04/recheck_20261128/hos_009_s03_apple_head_v04_open_sheet.jpg

```

### picture (exit 1)

```text
FAIL   0:17 row apple_6 /Volumes/data/mac-mini-archive/YouTube/History Of Science/02_Video-Projects/009_The-Falling-Moon-Gravity/04_Generated-Clips/part02/raw/v01/08_the_apple_t1.mp4: reuse: same stretch as 0:00 (give it a new stretch, or a new render); terminal loop: crop/output must contain integer pixels
WARN   0:00 row apple_1 /Volumes/data/mac-mini-archive/YouTube/History Of Science/02_Video-Projects/009_The-Falling-Moon-Gravity/04_Generated-Clips/part02/raw/v01/08_the_apple_t1.mp4: sharpness: upscaled 2.35x, may look soft
WARN   0:03 row apple_2 /Volumes/data/mac-mini-archive/YouTube/History Of Science/02_Video-Projects/009_The-Falling-Moon-Gravity/04_Generated-Clips/part02/raw/v01/06_old_newton_tells_t1.mp4: sharpness: upscaled 2.35x, may look soft; low detail: edge density 0.0272 < film p5 0.0273
WARN   0:07 row apple_3 /Volumes/data/mac-mini-archive/YouTube/History Of Science/02_Video-Projects/009_The-Falling-Moon-Gravity/04_Generated-Clips/part02/raw/v01/06_old_newton_tells_t1.mp4: sharpness: upscaled 2.35x, may look soft
WARN   0:10 row apple_4 /Volumes/data/mac-mini-archive/YouTube/History Of Science/02_Video-Projects/009_The-Falling-Moon-Gravity/04_Generated-Clips/part02/raw/v01/07_orchard_bench_t1.mp4: sharpness: upscaled 2.35x, may look soft
WARN   0:14 row apple_5 /Volumes/data/mac-mini-archive/YouTube/History Of Science/02_Video-Projects/009_The-Falling-Moon-Gravity/04_Generated-Clips/part02/raw/v01/07_orchard_bench_t1.mp4: sharpness: upscaled 2.35x, may look soft
picture QA FAIL: 1 of 6 cuts fail, 5 to look at -> /Volumes/MiniWork/scratch/J3871-recheck/02_Video-Projects/009_The-Falling-Moon-Gravity/10_Shorts/J3871/v04/recheck_20261128/picture/PICTURE_QA.md, /Volumes/MiniWork/scratch/J3871-recheck/02_Video-Projects/009_The-Falling-Moon-Gravity/10_Shorts/J3871/v04/recheck_20261128/picture/picture_qa_review.jpg

```

### polish (exit 0)

```text
apple_1     0.4s /Volumes/data/mac-mini-archi ok
apple_2     2.9s /Volumes/data/mac-mini-archi WARN low detail: edge density 0.0272 < film p5 0.0273
apple_3     6.6s /Volumes/data/mac-mini-archi ok
apple_4     9.9s /Volumes/data/mac-mini-archi ok
apple_5    13.9s /Volumes/data/mac-mini-archi ok
apple_6    16.6s /Volumes/data/mac-mini-archi ok
polish gate PASS: 0 of 6 rows failed, 1 to look at -> /Volumes/MiniWork/scratch/J3871-recheck/02_Video-Projects/009_The-Falling-Moon-Gravity/10_Shorts/J3871/v04/recheck_20261128/polish.json

```

### music (exit 0)

```text
WARN reused: couldn't read part01_zoo_of_stuff_v02.mp3 to compare (OSError); download it or pass --others
WARN reused: couldn't read part01_zoo_of_stuff_v02.wav to compare (OSError); download it or pass --others
music gate PASS: hos_009_score_v04_synth.wav, 535.3 s, about 52.2 BPM, brief Pace: 60-68 BPM

```

### sfx (exit 0)

```text
SFX level PASS: VO -19.8 LUFS, SFX -44.1 LUFS, 1 hits

```

### vo (exit 0)

```text
PASS  vo.wav  0:17.10  mean -23.1 dB  peak -4.1 dB  179 wpm

```

## Handoff

J3871 incomplete; J3816 stays held and J3872 cannot review yet. Five picture softness/low-detail warnings remain for the later capable reviewer. Music PASS retains two unreadable comparison-track warnings. Heard=false, watched=false: this session has shell and still-image tools but no demonstrated audio_input or moving_video_input; no quality KEEP inferred from measurements. Final audio/motion/phone review remains J3872 after technical gates pass.

Publish text evidence through the designated Claude Code route, keeping all Short PRs draft. Prior automatic review rejected the public push on J3871 as sensitive egress to an unverified remote; this run did not retry or bypass it. Worktree /Volumes/MiniWork/scratch/J3871-recheck, branch codex/J3871-recheck. Nothing for Ben. System disk 8.4GB: required nas_offload.py --apply found no old eligible scratch; all new scratch is on MiniWork.
