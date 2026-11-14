# J2242 source checkpoint — 11 November 2026

Codex worker. Assembly incomplete; 1 of 3 steps completed. No v04 master exists.

Current origin/main when this run started was `5655c9c9`. The shared HOS checkout is on an older working branch; do not run its old recipe or switch it underneath other workers. Continue from this clean worktree/branch: `/Volumes/MiniWork/scratch/J2242-hos`, `codex/J2242-source-preflight`.

## Completed source checks

The new `_j2242_source_preflight.py` hashes actual length-prefixed AVC sample bytes, compares each video packet to ffprobe's SHA-256, and parses VCL NAL types. All 113 random-access samples contain IDR slices rather than relying on keyframe flags. Every source frame has exactly one packet mapped by original integer PTS. Original master hash and size match the brief.

All 12,923 decoded YUV420P frame SHA-256 entries preserve original PTS and durations at timebase 1/12288, including the nonuniform gaps. All 25,296 compressed audio packets have hashes, PTS, DTS, durations and side data recorded. These are source baselines, not output identity or sync results. Evidence paths and hashes are in `SOURCE_PREFLIGHT.json`; complete local evidence is under `/Users/benjaminoats/_desk/state/J2242/source-preflight-v01/`.

`SELECTED_INPUTS.json` records independently verified hashes and complete decodes for the KEEP salon composite (61 frames), points take 3 (190), and rods take 2 (190). It also records the exact salon split and source schedule: 19 copies of f000 followed by f000–f060; source f030 lands on timeline f2635. The crop applies only to the preceding tube-plate tail. Review the resulting hold in context before locking it, as the brief requires.

Planner dry-run succeeded with six original input hashes/intervals verified and 32 caption cards. It remains `PLANNED_NOT_EXECUTABLE`. The full scratch plan contains legacy account text; do not commit or post it. Local path: `/Volumes/MiniWork/scratch/J2242-source-plan-v01.json`.

Validation:

```
Ran 18 tests — OK (existing planner)
Ran 4 tests — OK (new AVC parser/IDR, corrupt-packet and duplicate-PTS checks)
ALL CHECKS PASS (check_all.sh, full output CHECK_ALL.txt)
```

## Salon intermediate checkpoint — second run, 11 November 2026

The clean worktree remains on the same branch; PR #542 carries these checkpoints.
`_j2242_salon_patch.py` now renders the exact 160-frame salon replacement as a
lossless FFV1/NUT intermediate. `SALON_PATCH.json` records its path and hash.
All 160 decoded frame hashes independently match the cropped/scaled tube frames
99..178 followed by 19 copies of composite f000 and composite f000..f060.
The spark is therefore on master frame 2635; nothing after source f060 is used.
The intermediate muxer uses 1/49152; dividing its integer PTS and duration by
four reproduces every original master tick exactly. This is an intermediate,
not a final packet splice, and carries no audio. The hold and joins still need
in-context visual review. The final master must retain 1/12288 and original audio.

Tube hash reconciliation: J1880 inventory says `d3a0b24c996cec6d...`, but the
actual bytes match BOTH `FLOW_MINT_LOG_v03.json` and rough_v12 cut[22], namely
`d3a0b24c996c9d388baaf4e764b7561f9144e50a6fe21d94e8a3d2f9f2c45170`.
The render pins that historically recorded full hash rather than changing an
expected hash solely to accept current bytes. The old inventory is preserved.

`PATCH_TESTS.txt`: 26 tests OK (18 planner, 4 source preflight, 4 salon).
`CHECK_ALL_PATCH.txt`: ALL CHECKS PASS. These are code/repository checks;
no final picture, polish, audio, sync, phone readability or finished-film PASS
is claimed. No master, captions, packet splicer or publication was created.
No processes remain running; failed intermediate attempts v01/v02 are retained
beside successful v03, and only v03 has RESULT.json. No detached render.

## Remaining assembly and verification

1. Implement the packet/boundary splicer; current planner's execution refusal is intact. Source IDR validation resolves the source reference-reset question, but does not establish safe muxing of new encoded windows. Validate each encoded join and codec parameter handling. Copy unchanged GOP packets and original audio. Do not globally re-encode or rebuild timestamps as frame-index/24. Preserve unchanged decoded frames even inside boundary envelopes (use a lossless boundary encode where necessary), all original integer PTS/durations, and audio packet timestamps/data.
2. Build the seven defect windows plus the 32 sequential caption cards, SAFE PATH DOWN, and animated letter crossing from the exact brief. Existing master has baked text: placing new cards over it does not remove old labels or satisfy clear remainder windows. Reconstruct affected moving plates/overlays from source where needed. The planner is only a timing/inventory source. Keep 0:51 untouched; the separate 2:20 foil check is beyond the jar replacement. Use the selected composite rather than raw take 4. Never use a frame past f060.
3. Verify all unchanged output frames against the stored source hashes by PTS/duration; verify compressed audio packets and timestamps, original loudness and measured sync checkpoints. Run every mandatory media/package gate and produce the 168×94 contact sheet. Then J2243 and Chief review; no UAT, R2 or Studio action here.

This exceeds a single unattended assembly run; released at a clean source-validation checkpoint under the user's 20-minute scope rule. All processes launched by this run have ended. No detached render needs resuming. No spend, generation, media replacement, upload or final approval.

## Output-preservation verifier checkpoint — third run, 11 November 2026

`_j2242_verify_output.py` now checks a future candidate against the pinned
source evidence. Its change contract requires two separate inclusive range
lists: `modified_frames` (pixels allowed to change) and `encoded_envelopes`
(packets allowed to change). Envelopes must meet actual source IDR boundaries;
modified frames must be contained inside them. Do not declare whole envelopes
as modified merely to hide lossy changes to otherwise unchanged frames.

It checks original integer frame PTS/durations and count, decoded SHA-256 on
every unmodified frame (including inside encoded envelopes), packet SHA-256
and PTS/DTS/duration/size/flags/side data outside encoded envelopes, and every
original compressed audio packet with its timestamps and side data. It hashes
the candidate before and after measurement to reject a concurrently changing
file. Source evidence files must match their recorded hashes and byte sizes.
Results explicitly leave loudness, VO sync and visual review unmeasured; this
is a preservation check, not a media gate or approval. It does not verify
new encoded-window codec parameters or render any missing captions/splices.

`VERIFY_TESTS.txt`: 17 tests OK (4 source, 4 salon, 9 verifier). The verifier
tests reject changed audio bytes/timestamps/skip samples, changed unchanged
pixels inside encoded envelopes, copied-packet corruption, collapsed gaps,
out-of-scope modifications, invalid ranges and non-IDR boundaries.
`CHECK_ALL_VERIFY.txt`: ALL CHECKS PASS. Original planner's execution refusal
remains in force; no v04 master has been assembled.

To run on a candidate:

```sh
python3 02_Video-Projects/008_Lightning-Franklin/07_Edit-Project/_j2242_verify_output.py \
  --candidate /path/to/candidate.mp4 --contract /path/to/change-contract.json \
  --evidence jobs/reviews/J2242/SOURCE_PREFLIGHT.json --out /new/evidence/directory
```

The contract format is `{"modified_frames": [[2506, 2665]],
"encoded_envelopes": [[2506, 2665]]}` for a salon-only experiment. This does
not describe all changes in the eventual captioned film: derive those exact
ranges from the actual render plan. Unchanged frames inside wider boundary
envelopes still require pixel identity.

The real unchanged-source identity self-check completed: 12,923/12,923 decoded
frames, 12,923 copied video packets, and all 25,296 audio packets match their
pinned baselines. The newly computed framehash file is byte-identical to the
original stored framehash file (SHA-256 `7efa1f043cdf1ba83c87eef97a4e60e24904ac6d606336f17663d8054b150b65`).
See `VERIFY_IDENTITY_SELFCHECK.json`. This tests v03 against itself, not v04.
A concurrent-contract hash guard was added after that media run; comparison
logic is unchanged. The output and change contract are both hashed before and
after measurement in the final tool. No processes remain running.

Next run should implement a bounded packet-splice experiment using the already
verified salon intermediate and this verifier, preserving old master/audio and
explicitly testing encoded-window SPS/PPS compatibility, decoder reset and
DTS ordering at both joins. Do not call source IDR proof output-join validation.
Then implement the remaining source reconstructions and caption renderer, and
run every mandatory final gate. These cannot fit the current unattended run.

## Salon-only packet mux checkpoint — fourth run, 12 November 2026

`_j2242_salon_splice.py` implements a bounded single-GOP packet replacement
experiment, using PyAV 19.0.2 in `/Volumes/MiniWork/scratch/J2242-av-env`.
It verifies the source/evidence hashes, checks both source IDR boundaries,
requires replacement SPS/PPS/IDR and a no-B-frame native 24fps patch, checks
the encoded patch against all 160 verified lossless intermediate frame hashes,
and restores the original source codec via the next original IDR's in-band
SPS/PPS. It copies the remaining original video packets and every audio packet,
retaining integer PTS/DTS/duration; the replacement uses the original 1024-tick
reorder delay with exact original frame PTS/durations. The old source is checked
again after muxing. Nothing is written over a master.

Lossless patch encoding (already completed):

```sh
ffmpeg -nostdin -v error -xerror \
  -i /Volumes/MiniWork/scratch/J2242-salon-patch-v03/salon_patch.nut \
  -map 0:v:0 -an -c:v libx264 -preset fast -qp 0 -pix_fmt yuv420p \
  -x264-params 'bframes=0:repeat-headers=1:keyint=160:min-keyint=160:scenecut=0' \
  -fps_mode passthrough -enc_time_base 1/12288 -video_track_timescale 12288 \
  -n /Volumes/MiniWork/scratch/J2242-salon-encoded-v01.mp4
```

The final guarded script was run to `J2242-salon-mux-v02`. Its candidate is
byte-identical to the earlier v01 candidate (SHA-256
`0bfffbacbed21c9e9771723bfc0237b9827deb253e0b136e42d2746c60be092c`).
Both are **salon-only experiments**, never `hos_008_master_v04.mp4`.
The candidate contains 160 replacement video packets, 12,763 copied video
packets and 25,296 copied original audio packets. `SALON_ENCODE_PIXEL_CHECK.json`
records that every replacement encoded frame equals the intermediate.
`SPLICE_TESTS.txt`: 19 tests OK (source, salon, preservation verifier and splice
boundary guards). `CHECK_ALL_SPLICE.txt`: ALL CHECKS PASS. These are repository
checks and bounded preservation evidence, not final film gates.

Even with successful ffmpeg decoding, profile/parameter changes inside one
AVC sample description need delivery-player compatibility review before using
this approach for a finished master. It is not a phone-motion review, VO-sync
measurement, loudness measurement, visual approval or full assembly. All other
correction windows, source reconstructions, captions, letter animation, phone
sheets, media gates and J2243/Chief review remain outstanding. No UAT, R2,
YouTube, generation, spend or protected call was made.

### First full preservation result: REJECTED

The v01/v02 candidate above **fails** the mandatory unchanged-decoded-frame
comparison. `SALON_SPLICE_FAILURE.json` records all 266 mismatches (first f8292,
last f12845), despite exact copied video packet and audio packet equality.
Do not use that candidate as a master or as an approved splice. A direct seek
to f8292 decodes to the source hash, unlike continuous decoding, indicating a
state-dependent problem; the cause is not proven.

A second experiment encodes the same lossless intermediate with
`...:scenecut=0:sps-id=1`, avoiding the original source's SPS identifier 0
(all 113 source IDR samples were inspected). Its candidate is
`/Volumes/MiniWork/scratch/J2242-salon-mux-sps1-v01/salon_only_experiment.mp4`,
SHA-256 `74461c2640c5ea15f7e07e343a5ffe72eec15126e641ab90baf85c855cd931c1`.
The patch also passes all 160 intermediate pixel hashes before mux.
`SALON_MUX_SPS1.json` is only a mux record; the independent full verifier must
still determine preservation. Do not infer acceptance from successful muxing.

### Distinct-SPS result: also REJECTED

The distinct-SPS candidate also fails at f8292; all unchanged mismatching frame
indices are recorded in `SALON_SPS1_FAILURE.json`. Thus changing SPS ID is not
a demonstrated fix. Both edited candidates stay rejected. Do not relax the
preservation verifier or mark either candidate as v04.

A **new identity-remux control** isolates mux effects from the replacement:
`_j2242_remux_control.py` copies all original packets without replacing anything,
then the same independent verifier uses an empty modification/envelope contract.
This is distinct from the earlier self-check, which decoded v03 itself.
It runs detached in tmux `J2242-remux-control`, from
`/Users/benjaminoats/_desk/state/J2242/run-remux-control.sh`.
Log: `/Users/benjaminoats/_desk/logs/J2242-remux-control.log`.
Exit-code marker: `/Users/benjaminoats/_desk/logs/J2242-remux-control.done`.
Missing marker means still running: do not start a second copy.
Candidate: `/Volumes/MiniWork/scratch/J2242-identity-remux-v01/identity_remux.mp4`.
Verification: `/Volumes/MiniWork/scratch/J2242-identity-remux-verify-v01/`.
Read its exit marker and log first. If it fails with the same unchanged frames,
investigate mux/demux/decoder state before altering the replacement encoder.
All final-film assembly, original gates and review work remain outstanding.


## Profile-compatibility checkpoint — fifth run, 12 November 2026

The detached identity-remux control finished successfully (exit 0): all 12,923
unchanged decoded frames, 12,923 video packets and 25,296 audio packets match.
`IDENTITY_REMUX_CONTROL.json` records the result. No control remains running.
The original rejected salon mux also decodes with all 12,763 unchanged frames
matching under `ffmpeg -threads 1`; default decoding still fails on 266 frames.
`SINGLE_THREAD_DIAGNOSTIC.json` records this diagnostic only. Do not accept the
old mux by changing the verifier to a single thread.

A compatible High-profile patch resolves this observed default-decoder failure
in the bounded salon experiment. The old QP0 patch is High 4:4:4 Predictive;
the source is High. Exact decoder internals are not established. QP0 forces
x264 to disable B frames even when two are requested; that diagnostic is not a
new solution. No source or verifier acceptance criteria have been changed.

Encode used for the successful experiment:

```sh
ffmpeg -nostdin -v error -xerror \
  -i /Volumes/MiniWork/scratch/J2242-salon-patch-v03/salon_patch.nut \
  -map 0:v:0 -an -c:v libx264 -preset fast -qp 1 -profile:v high \
  -pix_fmt yuv420p \
  -x264-params 'bframes=0:repeat-headers=1:keyint=160:min-keyint=160:scenecut=0' \
  -fps_mode passthrough -enc_time_base 1/12288 -video_track_timescale 12288 \
  -n /Volumes/MiniWork/scratch/J2242-salon-high-b0-qp1-v01.mp4
```

`_j2242_salon_splice.py --patch-encoding high` now permits this near-lossless
patch only for the existing fully modified 160-frame salon GOP. It checks
H264 High profile, the verified intermediate, all 160 frame comparisons, and
minimum per-frame PSNR >=60 dB (measured minimum 62.70 dB). The default remains
exact lossless comparison. This option does **not** permit lossy changes to
unchanged boundary frames in another envelope; those still need exact hashes.
All packet, source-clock and independent unchanged-frame checks stay intact.

Guarded run:

```sh
/Volumes/MiniWork/scratch/J2242-av-env/bin/python \
  02_Video-Projects/008_Lightning-Franklin/07_Edit-Project/_j2242_salon_splice.py \
  --patch-encoding high \
  --encoded-patch /Volumes/MiniWork/scratch/J2242-salon-high-b0-qp1-v01.mp4 \
  --evidence jobs/reviews/J2242/SOURCE_PREFLIGHT.json \
  --out-dir /Volumes/MiniWork/scratch/J2242-high-profile-guarded-mux-v01
```

Its candidate SHA-256 is
`32868b561a38b31ce4a3796f080179c1c4592a6a78eddf296e821ce2f9d3cbdb`,
byte-identical to the independently verified diagnostic mux. Evidence:
`HIGH_PROFILE_MUX.json` and `HIGH_PROFILE_PRESERVATION.json`. Default full
verification confirms 12,763 unchanged decoded frames and copied video
packets, all 25,296 audio packets, and all original frame PTS/durations.
This is preservation evidence only; sync/loudness remain UNMEASURED and visual
review OUTSTANDING. The changed frames are near-lossless, not bitwise-identical
to the intermediate. The original master is unchanged.

Next: generalize safely to the remaining source reconstructions and 32 cards,
SAFE PATH DOWN and letter animation. Envelopes containing unchanged frames
still need lossless preservation; do not extrapolate the salon-only high-profile
option to those frames. Complete every original media/package gate and phone
sheet before J2243/Chief review. No v04 master, final media PASS, UAT, R2,
YouTube action, spend or generation. No detached work from this run.

## Rods intermediate checkpoint — sixth run, 12 November 2026

`_j2242_rods_patch.py` renders the approved rods take 2 f000..f134 into
`/Volumes/MiniWork/scratch/J2242-rods-patch-v01/rods_patch.nut`, replacing
master f11358..f11492 only in a future splice. `RODS_PATCH.json` records its
SHA-256. All 135 decoded YUV420P frame hashes independently match the selected
scaled source frames. Every PTS and duration maps exactly back to the original
1/12288 clock (NUT uses 1/49152, ratio 1/4). The renderer pins both the approved
retake hash and the clock evidence hash before and after work, refuses an
existing output directory, and emits success only after pixel/clock checks.
This is a lossless intermediate without audio, not a new master or media PASS.

`test_j2242_rods.py` rejects shifted PTS, changed durations/frame indices,
rescaled clocks and truncated windows. All 23 J2242 tests pass. Full repository
check output is `CHECK_ALL_RODS.txt`.

Important for the next window: the points interval f4511..f4670 has at least
one original duration of 1024 ticks while consecutive PTS increments are 512.
Do not reuse the uniform-duration rods/salon clock validator or normalize this
away. Implement and verify the exact source schedule in the packet mux; the
intermediate alone must not be called proof of final master durations.

Next work remains the points and other defect windows, source reconstruction
for all 32 captions, SAFE PATH DOWN and letter animation, generalized packet
mux with exact unchanged boundary hashes, phone sheets, all original media
and package gates, then J2243/Chief review. No v04 exists. Original masters,
audio, publication rejection and source evidence are untouched. No spend,
generation, UAT, R2 or YouTube action. No process from this run remains running.

## Points intermediate checkpoint — seventh run, 12 November 2026

`_j2242_points_patch.py` renders approved points take 3 f000..f159 as a
lossless FFV1/NUT intermediate. `POINTS_PATCH.json` records its path and hash.
All 160 decoded frame hashes equal independently scaled source frames; their
PTS rescale exactly to master frames f4511..f4670. The source hash is pinned
before and after rendering. The source clock evidence hash is also pinned.

The original f4513 has duration 1024 ticks while its next PTS advances only
512. The NUT intermediate does not preserve that overlapping duration. Its
`original_clock.json` sidecar preserves every original frame index, integer PTS
and duration, with a recorded SHA-256; the final packet mux must use that
schedule and pass the independent output verifier. This is explicitly not a
final-duration preservation result. The renderer rejects a normalized f4513
duration, shifted PTS, changed indices and wrong clocks.

All 27 J2242 tests pass (`POINTS_TESTS.txt`). Repository validation is in
`CHECK_ALL_POINTS.txt`. No final-film gate, motion/audio perception or approval
is claimed. No master v04, UAT, R2, YouTube, spend or generation. No process
remains running.

Next: remaining defect windows, baked-caption source reconstruction and the
32 cards/SAFE PATH DOWN/letter animation, general packet mux preserving
unchanged boundary pixels and all original durations, then all media/package
gates and the phone sheet. Keep original masters/audio, J1755 hold and
J2243/Chief review. This remaining work exceeds a single unattended run;
released at this verified intermediate checkpoint.

## Storm and jar intermediate checkpoint — eighth run, 12 November 2026

`_j2242_archive_patches.py` renders the two existing, hash-pinned archive
replacements without generation: storm source f000..f095 for master
f744..f839, and jar-crack source f000..f083 for master f3260..f3343.
`STORM_PATCH.json` and `JAR_PATCH.json` record output paths and hashes.
All 180 independently scaled source pixel hashes match the decoded lossless
FFV1 intermediates. Every original presentation timestamp matches after
rescaling the NUT clock by 1/4. No master or audio is written.

Storm f745 has an original duration of 1024 ticks despite the next PTS
advancing 512 ticks. As with the points replacement, its NUT intermediate
normalizes that overlapping duration. The hashed `original_clock.json`
sidecar preserves the original schedule for final packet assembly; final mux
must restore it and pass the unchanged independent verifier. Jar's 84 PTS
and durations all match. Jar f3168..f3259 is NOT part of the new intermediate
and must remain pixel-identical inside its future boundary envelope.
The 2:18 jar flip is inside this replacement; the separate f3353 / 2:20
foil check is outside it and remains unresolved. Storm speech alignment and
both replacements' in-context visual checks remain outstanding. Captions are
not yet rendered onto these clean source intermediates.

32 J2242 tests pass, including rejection of absolute PTS/index/duration
changes, normalization of the storm overlap, truncated/rescaled clocks and
shifted/short native sources. See `ARCHIVE_PATCH_TESTS.txt` and full repository
checks in `CHECK_ALL_ARCHIVE_PATCHES.txt`.

Resume the same clean branch/worktree. Next: caption source reconstruction,
all 32 cards, SAFE PATH DOWN and letter crossing, generalized mux preserving
unchanged boundary pixels and exact source durations, independent full-output
preservation, every mandatory film/package gate and phone sheet, J2243 and
Chief review. No v04, approval, UAT, R2, Studio, generation or spend. No process
from this checkpoint remains running; no detached render was started.


## Caption layers and letter crossing checkpoint — ninth run, 12 November 2026

`_j2242_caption_layers.py` renders all 32 planned caption cards and SAFE PATH
DOWN as 33 transparent FFV1/BGRA layers (2,738 frames) in
`/Volumes/MiniWork/scratch/J2242-caption-layers-v03/`. `CAPTION_LAYERS.json`
records each PNG/video hash, exact original PTS schedule and hashed duration
sidecar. It regenerates the plan from tracked labels and FACT_NOTES, verifies
the pinned source clock, and checks inputs again after rendering.

House design: white Didot Italic, 128 px, one or two balanced lines (still at
most four words per card), plain unbordered translucent umber panel, no gold
rule/pill/border. Layers are 1920x300 at x=0,y=720 in a 1920x1080 composite.
Both fades are 3/8 second on original PTS. Decoding a panel pixel across all
2,738 frames verifies fades/plateau with at most two alpha levels of error.
Every rendered presentation timestamp matches. The Gazette and house-rod
cards have original overlapping durations that NUT normalizes: the final mux
must restore their hashed original clocks; do not infer final preservation.

`LAYER_DESIGN_168_SHEET.jpg` in that scratch directory is a layer-only design
preview on a neutral background, visually inspected as stills. The earlier
v01/v02 layers used smaller lettering and are superseded. This is NOT the
required final phone composite sheet. Existing baked labels must be removed
by clean source reconstruction, including the clear remainder windows. Never
just paste these layers over old text. When compositing, retain absolute PTS,
restrict each layer to its original window, and use repeatlast=0/eof_action=pass
so the last label cannot leak past its planned end.

`_j2242_letter_patch.py` renders source f000..f100 of the pinned moving
07_slow_news plate into master f4977..f5077. Output:
`/Volumes/MiniWork/scratch/J2242-letter-patch-v02/letter_patch.nut` (hash and
clock in `LETTER_PATCH.json`). One cream ink folded letter crosses the clear
upper-left sky, with no banner, map, city/date/distance text or brown boxes.
Half-second stills were visually inspected from the byte-identical v01 render:
letter stays off the ship, source picture continues beneath it. This is not
motion/audio perception or a film PASS. The ship/right region, lower sea and
upper sky each match all 101 independently scaled source frame hashes exactly.
The original long f5068 duration (1536 ticks) is normalized in the intermediate;
the original schedule is preserved in its hashed sidecar for final mux restoration.

Validation: 42 J2242 tests OK; check_all.sh ALL CHECKS PASS (full outputs
CAPTION_LETTER_TESTS.txt and CHECK_ALL_CAPTION_LETTER.txt). These are code,
clock, alpha and intermediate checks, not the mandatory final-film gates.

Remaining: caption source reconstruction/composites, table-three correction,
the independent 2:20 foil check and ten code-graphic bottom-text reviews,
final generalized packet mux with exact original durations and unchanged
boundary pixels, original audio packet/timestamp identity, measured loudness
and sync, every mandatory media/package gate and final phone sheet. Then
J2614/J2243 and Chief review before UAT/R2/Studio. No v04 master, spend,
generation, publication or final approval. All work from this run has ended;
no detached process remains. Resume this clean existing PR #542 branch.

## Jar source-interval correction — tenth run, 12 November 2026

The previous archive renderer incorrectly trimmed the jar plate from source
f000..f083. The approved J1880/J2163 recipe requires 4.000–7.500 seconds,
so that intermediate is rejected. Its evidence remains in
`JAR_PATCH_V01_REJECTED.json`; do not mux the v01 jar intermediate.

The renderer now selects native source f096..f179 (84 frames) and validates
the actual selected timestamps before rendering. `JAR_PATCH.json` points to
`/Volumes/MiniWork/scratch/J2242-jar-patch-v02/jar_patch.nut`. All 84 decoded
YUV420P frame hashes match the independently trimmed/scaled approved source
interval. Every original master PTS and duration matches after timebase
rescaling. The corrected output hash is
`28aa4ec861a21181182632c50cccf5779ed978e6a7dd5217280c8ba0d7251c11`.

43 J2242 unit tests pass, including an approved-interval regression rejecting
a truncated tail and shifted selected source timestamp. Full repository
checks: `CHECK_ALL_JAR_INTERVAL.txt`, ALL CHECKS PASS. These are intermediate
and code checks; no final-film gate or perceptual review is claimed.

The prior storm intermediate is unaffected. Jar keep frames f3168..f3259
remain outside the replacement, and the distinct f3353 foil check is still
outside its end. No original master, source or audio changed. No v04 master,
UAT, R2, Studio, spend, generation or approval. All processes have finished.

Remaining assembly (caption clean-plate reconstruction and composites, table
row, independent foil check, bottom-text reviews, generalized mux, exact
output preservation/audio/sync checks and all mandatory gates) exceeds a
single unattended run. Resume this existing PR #542 worktree; J2614/J2243
and Chief review remain required.

## Clean caption composites checkpoint — eleventh run, 12 November 2026

`_j2242_opening_caption.py` reconstructs f0..141 directly from the clean KEEP
kite plate and composites the existing opening layer at original timestamps.
`OPENING_COMPOSITE.json` pins the 142-frame FFV1 intermediate. All presentation
timestamps and durations match; f96..141 (46 frames) and the zero-alpha first
frame match clean-source pixel hashes exactly. Every frame above y720 also
matches. An initial failed attempt v01 is retained without a success record:
FFmpeg reset the layer start time, shifting the overlay three frames early.
The corrected v02 uses `-copyts` and passes all boundary/pixel checks.

`_j2242_caption_source_map.py` compared 3,491 master frames across all 27
caption rows to their hash-pinned clean sources. `CAPTION_SOURCE_MAP.json`
records every candidate source index, upper-band MSE, runner-up margin,
ambiguity and poor-match flags. These are low-resolution mapping candidates,
not full-frame identity or visual approval. It correctly flags table-window
f423..426 as poor matches to the table source; the actual table begins f427.
Do not reconstruct those four frames from a guessed table source frame.
Some other rows contain actual pause-removal jumps/duplicate frames or very
similar candidates; they require separate handling, not a CFR assumption.
The mapper uses NumPy from `~/_desk/venvs/owb-cg/bin/python`.

`_j2242_caption_composites.py` reconstructs only the 17 unambiguous, contiguous
mapped rows. It validates source hashes, native source timestamps, approved
caption windows, original master clock and all layer hashes. Each caption is
over the clean source plate, with no old baked text underneath. Both overlay
EOF behavior and input timestamps are explicit. Every output presentation
timestamp matches; every clear-tail frame and every frame above the caption
band matches the independent clean-source decode exactly. Caption midpoints
are present. Original clocks are recorded in hashed sidecars; intermediate
normalized durations are declared individually, and final mux must restore
them and pass the independent verifier.

`CAPTION_COMPOSITES.json` pins the batch under
`/Volumes/MiniWork/scratch/J2242-caption-composites-v01/`. Together with the
opening, this is **18 rows / 20 cards / 2,277 frames**. The detached batch
finished exit **0**; log and marker are
`~/_desk/logs/J2242-caption-composites.log` and `.done`. No process remains.
The 20-card phone still sheet is
`/Volumes/MiniWork/scratch/J2242-caption-composites-v01/PHONE_INTERMEDIATES.jpg`.
It was inspected as stills at 168x94 per card; this is a partial intermediate
sheet, not the required complete final-film sheet (32+SAFE PATH+letter).

Validation:

```
Ran 54 tests in 0.317s
OK
ALL CHECKS PASS
```

Full outputs: `COMPOSITE_TESTS.txt`, `CHECK_ALL_COMPOSITES.txt`. These are code,
clock and intermediate checks, not final-film media gates. NumPy tests run in
the existing `owb-cg` environment. No new packages, generation or credits.

Next: reconstruct the **nine remaining caption rows** (the generic batch's
skipped list also includes the separately completed opening), including the
four preceding-shot table boundary frames, source-map ambiguities and pause
jumps; composite the remaining 12 cards and SAFE PATH DOWN; finish the distinct
f3353 foil check and ten code-graphic bottom-text checks. Then generalized
packet mux preserving unchanged boundary pixels, original durations/audio,
full independent output preservation, loudness/sync and every mandatory
film/package gate, complete phone sheet and J2614/J2243/Chief review.

No v04 master, final film PASS, UAT, R2, Studio, publication or spend. Original
masters/audio and J1755 remain untouched. This remaining assembly exceeds a
single unattended run; release at the verified checkpoint rather than claiming
completion. Continue this existing PR #542 branch/worktree.


## Measured repeat-frame caption composites — twelfth run, 12 November 2026

The caption compositor now reconstructs unambiguous monotonic schedules that
contain measured repeats or forward jumps, using explicit source trim runs
and concat before applying the original absolute master clock. It never fills
ambiguous mappings with a guessed CFR schedule. Requested row names are
validated before rendering; poor matches, ambiguous matches and backwards
maps remain rejected. Independent source pixel hashes are indexed by the
measured schedule, separately from the concat graph, to catch missing,
duplicated or shifted frames.

`REPEAT_CAPTION_COMPOSITES.json` records two newly verified intermediates in
`/Volumes/MiniWork/scratch/J2242-caption-composites-v02/`: `01_salon_tube`
(f2407..2505, 99 frames) and `10_richmann_rod` (f8849..9003, 155 frames).
Both use the measured source sequence f000, f000, f002 onward. All 254 output
presentation timestamps match the master. Every upper-band frame and each
clear-tail frame matches its independently selected/scaled source pixel hash;
caption presence is checked at its midpoint. Original duration sidecars are
hashed for final mux restoration. This is **20 rows / 22 caption cards** in
combination with the earlier verified opening and 17-row batch.

`PHONE_INTERMEDIATES.jpg` in this new scratch folder was inspected as two
168x94 stills. ELECTRICITY A PARTY TRICK and ST PETERSBURG 1753 read clearly.
This partial intermediate sheet is not the complete final-master phone sheet,
a motion review, audio review or approval.

Validation: 55 J2242 unit tests OK (`REPEAT_COMPOSITE_TESTS.txt`), and
`CHECK_ALL_REPEAT_COMPOSITES.txt` ends ALL CHECKS PASS. The tests verify exact
repeat/jump reconstruction and rejection of backwards/invalid schedules.
No final-film gate is claimed. No v04 exists and no original master changed.

Remaining: seven ambiguous/boundary caption rows, SAFE PATH DOWN, the table
correction, independent f3353 foil/bottom-text checks, general packet mux,
full preservation/audio/loudness/sync checks and mandatory film gates. Then
J2614/J2243 and Chief review before UAT/R2/Studio. Continue this existing PR542
worktree. All processes finished; no detached work, generation, spend or
publication. The full remaining assembly exceeds this unattended run.

## Table-body composite — thirteenth run, 12 November 2026

Cursor worker. The six still-ambiguous caption rows were not rendered.
Full-resolution upper-band comparison was finished for `02_tower_tilt`,
`04_franklin_watches` and `02_sentry_box`. Even the low-resolution best frame
differs from the master by thousands of MSE, and the adjacent-frame margin is
smaller than that error (several comparisons flip the winner). That measurement
does not identify a unique source frame. `02_knuckle_spark`, `14_royal_society`
and `07_giant_spark` were not finished in the same pass. All six stay rejected.

`_j2242_table_body.py` reconstructs only master f427..f544 from table source
f000..f117. Master f423..f426 stay out: they map to table source f052 at
low-resolution MSE about 3380, and the body does not guess a plate for them.
`TABLE_BODY.json` records `/Volumes/MiniWork/scratch/J2242-table-body-v01/table_body.nut`,
SHA-256 `3a58cf6160bfb05346d7d0f09365322472b9561ef1d6edbfb8330760997e7f65`.
All 118 presentation timestamps match. Durations match in this intermediate.
The picture above the caption band matches the clean source. The first body
frame and each card midpoint carry a caption. There is no clear tail inside
this body because `A JAR` ends on f544.

Three 168×94 stills in that scratch folder's `stills/` read A KITE, A KEY and
A JAR. This is a partial intermediate sheet, not the required 32-card sheet,
and not a motion or audio review.

57 J2242 unit tests OK (`TABLE_BODY_TESTS.txt`). No v04 master. Original
masters and audio are unchanged. No spend, generation, UAT, R2 or YouTube
action. No detached process.

Remaining: six ambiguous caption rows, the four table lead-in frames, SAFE PATH
DOWN on its plate, the foil check at f3353, bottom-text reviews, generalized
packet mux, preservation and loudness/sync checks, and the mandatory film gates.
Then J2243 and Chief review. Continue this PR #542 worktree.

## Full-resolution ambiguous rows — fourteenth run, 12 November 2026

Cursor worker. `_j2242_ambiguous_fullres.py` compares the upper 1920×720 band,
after the same lanczos scale the composites use, against every frame of the
clean source. A row is unique only when every winner matches the low-resolution
index, per-pixel MSE stays at or below 9, and the runner-up margin is at least
0.1. Nothing is rendered from this measurement.

`12_steeple_fire` is the control. It was already an eligible low-resolution row.
Full resolution agrees on all 78 frames: maximum MSE 8.693, minimum margin
15.228, no winner changes. That shows a real plate match can clear the rule.
It was not reconstructed again.

The three rows left unmeasured last run stay rejected:

- `02_knuckle_spark`, 89 frames. Maximum MSE 6.869. Minimum margin 0.075.
  Winners differ from the low-resolution index at local frames 2, 3, 7, 20,
  21, 22, 23, 26, 27 and 29.
- `14_royal_society`, 127 frames. Maximum MSE 7.206. Minimum margin 0.031.
  Winners differ at local frames 31 and 33.
- `07_giant_spark`, 151 frames. Maximum MSE 7.350. Minimum margin 0.753.
  Winners differ at local frames 9, 54 and 92.

`AMBIGUOUS_FULLRES.json` holds every frame. Raw decodes stay in
`/Volumes/MiniWork/scratch/J2242-ambiguous-fullres-v01/` and are not in git.
62 J2242 unit tests OK (`AMBIGUOUS_FULLRES_TESTS.txt`).
`CHECK_ALL_AMBIGUOUS_FULLRES.txt` ends ALL CHECKS PASS. These are code and
mapping checks. No composite, v04 master, motion review or approval.

The six ambiguous caption rows, including the three measured and rejected on
the previous run, stay unrendered. Frames 423–426 stay out. No original master
or audio changed. No spend, generation, UAT, R2 or YouTube action. No detached
process.

Remaining: those six caption rows by a method other than guessing a source
frame, the four table lead-in frames, SAFE PATH DOWN, the foil check at f3353,
bottom-text reviews, generalized packet mux, preservation and loudness/sync
checks, and the mandatory film gates. Then J2243 and Chief review. Continue
this PR #542 worktree.

## Giant spark full-resolution composite — fifteenth run, 12 November 2026

Cursor worker. `_j2242_fullres_caption.py` composites a row only when every
full-resolution upper-band winner has per-pixel MSE at or below 9 and a
runner-up margin of at least 0.1. The schedule may disagree with the coarser
low-resolution index. A single weak frame rejects the whole row. The control
row cannot use this path.

`07_giant_spark` passes. Its schedule is source frames 0 through 150, one
contiguous run, on master frames 10626 through 10776. Maximum MSE is 7.350
and the smallest runner-up margin is 0.753. Low resolution disagreed on local
frames 9, 54 and 92, each by one source frame, with margins 0.753, 1.400 and
3.981. Those three low-resolution indices were not used.

`02_knuckle_spark` and `14_royal_society` still fail the margin rule, so they
stay unrendered. The other three ambiguous rows were already rejected for a
large plate error and were not remeasured.

The intermediate is
`/Volumes/MiniWork/scratch/J2242-giant-spark-fullres-v01/caption_composite.nut`,
SHA-256 `0124237ed4dda1be59d7385b193de8840957df95ff18aa53ea95afd0279782d6`,
recorded in `GIANT_SPARK_FULLRES.json`. All 151 presentation timestamps and
durations match the master. The picture above the caption band matches the
selected clean source, the 55-frame clear tail matches, and the caption is
present at its midpoint. The card reads HOTTER THAN THE SUN on the midpoint
still, including the 168×94 still in that scratch folder. That still is one
card, not the finished phone sheet, and it is not a motion or audio review.

66 J2242 unit tests pass. No v04 master. Original masters and audio are
unchanged. No spend, generation, UAT, R2 or YouTube action. No detached
process.

Remaining: five ambiguous caption rows, the four table lead-in frames, SAFE
PATH DOWN, the foil check at f3353, bottom-text reviews, generalized packet
mux, preservation and loudness/sync checks, and the mandatory film gates.
Then J2243 and Chief review. Continue this PR #542 worktree.

## Unique full-resolution spans — sixteenth run, 13 November 2026

Cursor worker. The earlier note that `02_tower_tilt`, `04_franklin_watches`
and `02_sentry_box` differ from their named plates by thousands of MSE was
wrong. Full-resolution upper-band search against those same plates gives a
best per-pixel MSE of 5.374, 7.424 and 8.323. `THREE_ROW_FULLRES.json` records
every frame. The plates are the right sources. What still fails the existing
rule is a runner-up margin under 0.1 on a few frames. That rule is unchanged.

`_j2242_unique_spans.py` reconstructs only a contiguous span in which every
frame is unique, and only when a later or earlier near-tie is still present
so a finished row cannot be shortened by silence. Two spans passed:

- `04_franklin_watches` master frames 2718–2864, source frames 0–146, 147
  frames. The whole BENJAMIN FRANKLIN / PHILADELPHIA card sits inside it,
  with a clear tail through 2864. Frames 2865–2887 stay out: nine of them
  are near-ties, the closest margin 0.004.
- `02_tower_tilt` master frames 347–422, source frames 75–150, 76 frames.
  This is the complete ON THE ROOF card. Frames 272–346 stay out because
  THE ANSWER IS contains three near-ties.

`02_sentry_box` has one near-tie on local frame 2, inside THE SENTRY-BOX.
`02_knuckle_spark` has one on local frame 29, inside A SPARK.
`14_royal_society` has two, on local frames 1 and 29, inside THE ROYAL
SOCIETY. Neighbours do not force a single index on those frames, because a
repeat of the previous source frame stays monotonic. All three cards stay
unrendered.

Intermediates, hashes and clocks:

- `/Volumes/MiniWork/scratch/J2242-unique-spans-v01/04_franklin_watches/caption_composite.nut`
  SHA-256 `17163f3e57e07c6a0006ee2087ed8322166d7f33648c603fa93e784765af9c0c`
- `/Volumes/MiniWork/scratch/J2242-unique-spans-v01/02_tower_tilt/caption_composite.nut`
  SHA-256 `2fb23d65d70a60a67796ec9c1a1c719a4a9dd021807581ecd81dda40041b69a2`

Both keep original presentation timestamps and durations. The picture above
the caption matches the clean source. Midpoint stills, including 168×94,
read BENJAMIN FRANKLIN / PHILADELPHIA and ON THE ROOF. Those are stills, not
a motion review, an audio review, or a film approval. No v04 master. Original
masters and audio are unchanged. No spend, generation, UAT, R2 or YouTube
action. No detached process.

Remaining: the sentry, knuckle and royal-society cards, the tower opening
card, the four table lead-in frames, SAFE PATH DOWN, the foil check at
f3353, bottom-text reviews, generalized packet mux, preservation and
loudness/sync checks, and the mandatory film gates. Then J2243 and Chief
review. Continue this PR #542 worktree.

## Near-tie source pairs differ — seventeenth run, 13 November 2026

Cursor worker. The sixteen full-resolution near-ties were compared as source
pictures, not as another guess at the master. Each pair is the winning source
frame and its runner-up, in the same upper 1920×720 band. `same_picture`
accepts a pair only when that difference is below 0.1 per-pixel MSE, the
margin that already makes a winner unique. Every measured pair fails.

The smallest difference is 0.197, on Franklin master frame 2872 (source
frames 154 and 156). The knuckle near-tie at master frame 7777 differs by
4.054. Tower frames 274, 275 and 278 differ by 1.28 to 1.40. Sentry frame
4673 differs by 0.800. Royal Society frames 9304 and 9332 differ by 0.825
and 0.575. `NEAR_TIE_SOURCE_PAIRS.json` lists all sixteen. None is
reconstructed.

`resolve_near_tie` refuses a unique frame and refuses these pairs. The
uniqueness rule is unchanged. The sentry, knuckle, royal-society and tower
opening cards stay out, as do Franklin frames 2865–2887 and table frames
423–426. No v04 master. Original masters and audio are unchanged. No spend,
generation, UAT, R2 or YouTube action. No detached process.

Remaining: those caption cards by a method other than picking between
different source frames, the four table lead-in frames, SAFE PATH DOWN, the
foil check at f3353, bottom-text reviews, generalized packet mux,
preservation and loudness/sync checks, and the mandatory film gates. Then
J2243 and Chief review. Continue this PR #542 worktree.

## Centre-window confirmation — eighteenth run, 13 November 2026

Cursor worker. The sixteen near-ties were scored again on a window fixed
before the scores: the central half of the upper band, x=480, y=180,
960×360. A frame is confirmed only when that window's error on the existing
full-band winner is at most 9 and at least 0.1 under the recorded runner-up.
The runner-up is never adopted. Full-band alignment was checked against the
recorded error before any window score was kept.

Five frames confirm. Only Royal Society has every weak frame confirmed
(master 9304, window margin 0.318; master 9332, window margin 0.238). That
row is now a 127-frame intermediate:

- `/Volumes/MiniWork/scratch/J2242-royal-subject-v01/caption_composite.nut`
  SHA-256 `4774997f245ae2fa25c42d67b879fad305af82ebd3dda3fc11610a66f941a056`

Original presentation timestamps and durations match. The picture above the
caption matches the clean source, and the 31-frame clear tail matches it
too. A midpoint still reads THE ROYAL SOCIETY. That is a still, not a motion
review, an audio review, or a film approval.

Franklin frames 2865, 2868 and 2871 also confirm, but 2869 does not, and the
window prefers the other source picture there. Those frames stay out. Tower
274, 275 and 278, sentry 4673, and knuckle 7777 stay out; on the knuckle
frame the window prefers the runner-up by 1.019 and the winner was not
switched. The uniqueness rule on the full band is unchanged.

80 unit tests OK. check_all ALL CHECKS PASS. No v04 master. Original masters
and audio are unchanged. No spend, generation, UAT, R2 or YouTube action.
No detached process.

Remaining: the sentry, knuckle and tower-opening cards, the Franklin tail,
the four table lead-in frames, SAFE PATH DOWN, the foil check at f3353,
bottom-text reviews, generalized packet mux, preservation and loudness/sync
checks, and the mandatory film gates. Then J2243 and Chief review. Continue
this PR #542 worktree.

## Outside-hold captions — nineteenth run, 13 November 2026

Cursor worker. The sentry, knuckle and tower-opening near-ties stay different
pictures, so neither candidate is used. `_j2242_outside_hold.py` repeats the
nearest unique source frame that is outside that pair. The previous unique
frame is used when it qualifies. The next unique frame is used only when the
previous one is itself a candidate. A near-tie with no such neighbour is
refused, and so is a backward schedule.

The three rendered rows:

- `02_sentry_box`, master frames 4671–4820, 150 frames. Local 2 repeats
  source 0. Sources 1 and 2 stay unused. SHA-256
  `c18af4d10a2f1d126e003b0728e2d60f98470bb3a654e79eebedcfa8b2b2aceb`.
  The 54-frame clear tail matches the clean source.
- `02_knuckle_spark`, master frames 7748–7836, 89 frames. Local 29 repeats
  source 30. Sources 28 and 29 stay unused. SHA-256
  `fe3486e568db7dcfafd8451559d94ecc3d4522c51feec79cb9f3a509488d61cf`.
- `02_tower_tilt` opening card only, master frames 272–346, 75 frames.
  Locals 2 and 3 repeat source 0. Local 6 repeats source 4. SHA-256
  `db3aec3fed6498b6bb5590966e1dd81da9a77e2d12ddd14aa8c661fff3528a49`.
  Frame 346 is source 74, so it meets the already rendered ON THE ROOF span.

Original presentation timestamps and durations match. The picture above the
caption matches the selected clean source, including the repeated frames.
Midpoint stills, including the 168×94 stills, read THE SENTRY-BOX, A SPARK
and THE ANSWER IS. Those are stills, not a motion review, an audio review,
or a film approval.

86 J2242 unit tests OK. check_all ALL CHECKS PASS. No v04 master. Original
masters and audio are unchanged. No spend, generation, UAT, R2 or YouTube
action. No detached process.

Remaining: the Franklin tail, the four table lead-in frames, SAFE PATH DOWN,
the foil check at f3353, bottom-text reviews, generalized packet mux,
preservation and loudness/sync checks, and the mandatory film gates. Then
J2243 and Chief review. Continue this PR #542 worktree.

## Franklin forward hold — twentieth run, 13 November 2026

Cursor worker. `outside_hold` refuses the whole Franklin row: looking forward
for a blocked near-tie, then holding an earlier picture, makes the schedule
backward. `_j2242_franklin_tail.py` does not look forward. A near-tie repeats
the nearest earlier unique source frame only when that frame is neither
candidate. A backward hold is refused. Unique frames keep their winner. The
rendered prefix, source frames 0–146, is unchanged and was not rendered again.

Two clean-plate spans, with no caption on them (the card already ended at
frame 2813):

- Master frames 2865–2867, 3 frames. Local 147 repeats source 146. Sources
  147 and 148 stay unused. SHA-256
  `b34d2e629ce68d1f5189120a0e87290ef48807a0dcabc27c919bfc85a7fcb0c6`.
- Master frames 2870–2887, 18 frames. Locals 152–157 repeat source 148.
  Their own winners and runners stay unused. SHA-256
  `0bc4fc2b3c0bf3476f09c5637cce4789422e8d921f732fbd8f8c5b3809cb2671`.

Original presentation timestamps and durations match. Every decoded frame
matches the selected clean source, so the old caption is not on these
frames. Master frames 2868 and 2869 stay out: the nearest earlier unique
picture is itself one of the two candidates. These are pixel checks, not a
motion review, an audio review, or a film approval.

90 J2242 unit tests OK. check_all ALL CHECKS PASS. No v04 master. Original
masters and audio are unchanged. No spend, generation, UAT, R2 or YouTube
action. No detached process.

Remaining: master frames 2868–2869, the four table lead-in frames, SAFE PATH
DOWN, the foil check at f3353, bottom-text reviews, generalized packet mux,
preservation and loudness/sync checks, and the mandatory film gates. Then
J2243 and Chief review. Continue this PR #542 worktree.

## Confirmed-neighbour bridge — twenty-first run, 13 November 2026

Cursor worker. The forward hold still refuses frames 2868 and 2869, because
the nearest earlier unique source is one of the two candidates. A separate
rule fills a refused frame only when three things are already true: the
accepted source on both sides is the same, that source is the full-band
winner, and the pre-declared centre window confirms that winner. The
runner-up is not used. A newly filled frame does not become a flank for
another refused frame.

The centre window was scored again from the raw upper band. It still matches
the recorded scores.

- Master frame 2868, one clean frame, source 148. The runner, source 150, is
  unused. There is no caption on this frame. SHA-256
  `bb674f3108d3affd0b37e91d230da30f1e662eadcd5fbbd0b827dd72a4ee90f4`.
  Original presentation timestamp and duration match, and the decoded frame
  matches the selected source.
- Master frame 2869 stays out. Its full-band winner is source 150, which is
  not the accepted neighbour. The centre window prefers source 148, and this
  rule does not switch to that runner-up.

94 J2242 unit tests OK. check_all ALL CHECKS PASS. No v04 master. Original masters and audio are
unchanged. No spend, generation, UAT, R2 or YouTube action. No detached
process. These are pixel checks, not a motion review or an audio review.

Remaining: master frame 2869, the four table lead-in frames, SAFE PATH DOWN,
the foil check at f3353, bottom-text reviews, generalized packet mux,
preservation and loudness/sync checks, and the mandatory film gates. Then
J2243 and Chief review. Continue this PR #542 worktree.

## Table lead-in — twenty-second run, 13 November 2026

Cursor worker. Frame 2869 stays out. Master frames 423–426 are not the table
plate: full-resolution upper-band MSE against table source 52 is about 3554
to 3559. They are the tower plate, a forward jump from source 150 on master
frame 422 to source frames 170–173. Each match is unique (MSE 2.94 to 3.54,
runner-up margin 16.1 to 17.7). Sources 151–169 are not used. The guessed
continuation 151–154 was measured and refused before this render.

`_j2242_table_leadin.py` composites the existing A KITE layer onto those four
tower frames. The first frame of the fade stays clear. The next three carry
the card. Original presentation timestamps and durations match, and the
picture above the caption matches the clean tower source.

- `/Volumes/MiniWork/scratch/J2242-table-leadin-v01/table_leadin.nut`
  SHA-256 `bf087a9865c270d3fa6e29b304b9c31276878f107cbf6f5bd3305bf6184859d3`

A full-size still of local frame 2 reads A KITE over the tower, not over the
table. The same frame at 168×94 is still inside the fade, so the card is not
readable there yet. The readable hold of A KITE remains on the table body
already rendered. This is a still check, not a motion review, an audio
review, or a film approval.

98 J2242 unit tests OK. check_all ALL CHECKS PASS. No v04 master. Original masters and audio are
unchanged. No spend, generation, UAT, R2 or YouTube action. No detached
process.

Remaining: SAFE PATH DOWN on its plate, the foil check at f3353,
bottom-text reviews, generalized packet mux, preservation and loudness/sync
checks, and the mandatory film gates. Then J2243 and Chief review. Continue
this PR #542 worktree. Frame 2869 stays out.

## SAFE PATH on the v12 card — twenty-third run, 13 November 2026

Cursor worker. Frame 2869 stays out. Master frames 11038–11117 are the v12
card `body.mp4`, not either code-graphic file. The upper 1920×720 band
matches that card at per-pixel MSE 0. The schedule is monotonic: body frames
0–44, a second copy of 44, then 46–48 with 48 held twice more, then 51–79.
Body frames 45, 49 and 50 stay unused. Weak runner-up pairs are the same
picture, and the exact frame is the one that was used.

`_j2242_safe_path.py` composites the existing SAFE PATH DOWN layer onto those
frames. Original presentation timestamps and durations match. The picture
above the caption matches the card. The first fade frame stays clear.

- `/Volumes/MiniWork/scratch/J2242-safe-path-v01/safe_path.nut`
  SHA-256 `e0899746864f60d476c70f08ce464f6277df6deb9bca0bda1c75ba838fca3bb0`

Stills, not a motion review or an audio review: local frame 24 is the brown
lead-in, and local frame 70 is the steeple diagram. Both show the plate's own
upper title and the new bottom card, and both titles read SAFE PATH DOWN.
The bottom card is readable at 168×94. One label at a time is not met, so
this intermediate is not a finished card and not a film approval.

101 J2242 unit tests OK. check_all ALL CHECKS PASS. No v04 master. Original
masters and audio are unchanged. No spend, generation, UAT, R2 or YouTube
action. No detached process.

Remaining: the duplicate SAFE PATH title, the foil check at f3353,
bottom-text reviews, generalized packet mux, preservation and loudness/sync
checks, and the mandatory film gates. Then J2243 and Chief review. Continue
this PR #542 worktree. Frame 2869 stays out.

## One SAFE PATH title — twenty-fourth run, 13 November 2026

Cursor worker. Frame 2869 stays out. The v12 card draws SAFE PATH DOWN in
x 640–1280, y 115–182. Body frame 0 is that field before the title fades in.
On every later frame in this window the corners of the box are still that
field (maximum luma MSE 0.770) and the centre is the title (held-frame centre
MSE at least 2808.98). The steeple stays outside the box. `_j2242_safe_path_title.py`
copies body frame 0 into a chroma-aligned box, y 114–182, and composites the
existing bottom card. The row above the ink is included so a 4:2:0 sample does
not change it.

- `/Volumes/MiniWork/scratch/J2242-safe-path-v02/safe_path.nut`
  SHA-256 `7ef30a0f50982fe4e58e4f9f6a112937c5e688cf20958f2b0229cbd8d42264cf`

Original presentation timestamps and durations match. The picture above the
caption matches the cleared field. The first fade frame stays clear. On local
frame 70 the cleared box matches body frame 0 at MSE 0, and the picture
outside the box matches the titled body at MSE 0.

Stills, not a motion review or an audio review: local frame 24 is the brown
lead-in, and local frame 70 is the steeple. Each shows one SAFE PATH DOWN,
the bottom card. The upper title is gone. The card is readable at 168×94.
This is one label on these stills. It is not a film approval.

104 J2242 unit tests OK. check_all ALL CHECKS PASS. No v04 master. Original
masters and audio are unchanged. No spend, generation, UAT, R2 or YouTube
action. No detached process.

Remaining: the foil check at f3353, bottom-text reviews, generalized packet
mux, preservation and loudness/sync checks, and the mandatory film gates.
Then J2243 and Chief review. Continue this PR #542 worktree. Frame 2869
stays out.

## Foil check at frame 3353 — twenty-fifth run, 13 November 2026

Cursor worker. Frame 2869 stays out. The 138s jar flip stays inside the
replacement, and the 140s foil frame stays outside it. `_j2242_foil_check.py`
reads the original clock and compares the upper band of three master frames
with the pinned foil-jar and jar-spark plates. The note stays open. This
envelope is not a splice.

- Master frame 3343, the last frame of replacement 3260–3343, ends at
  139.625s. It matches foil-jar source 175, MSE 5.667, unique by 118.7.
  The jar-spark plate is 5943 worse. The still shows that foil-jar tail:
  a glass jar in a hand, foil at the rim.
- Master frame 3344 is the next keyframe. It matches jar-spark source 0,
  MSE 2.129, unique by 10.4.
- Master frame 3353 is 140s, inside keyframe envelope 3344–3404. It matches
  jar-spark source 9, MSE 4.541, unique by 199.0. The foil-jar plate is
  5652 worse. The still shows the spark plate: a foil-lined jar on the
  bench and a spark at a fingertip. The same still of spark source 9 matches
  it. Source 9 is 0.375s, inside the plate's existing head.

Replacing 3260–3343 does not cover frame 3353. No new intermediate was
rendered for this envelope. These are stills and pixel checks, not a motion
review, an audio review, or a film approval.

109 J2242 unit tests OK. check_all result is in `CHECK_ALL_FOIL.txt`. No v04
master. Original masters and audio are unchanged. No spend, generation, UAT,
R2 or YouTube action. No detached process.

Remaining: bottom-text reviews, generalized packet mux, preservation and
loudness/sync checks, and the mandatory film gates. Then J2243 and Chief
review. Continue this PR #542 worktree. Frame 2869 stays out.

## Ten code-graphic titles — twenty-sixth run, 13 November 2026

Cursor worker. Frame 2869 stays out. `_j2242_bottom_text.py` reads the ten
code-graphic rows from `reconcile_bottom_text()`. None of them has a side
label, so the 32 caption cards do not cover them. Safe path stays its own
title row. One midpoint frame of master v03 was decoded for each row.
A frame is a flat field when its luma mean is 70–95 and its standard
deviation is at most 26. A bottom panel would be a flat fill in rows
760–999 on a picture. None of these midpoints has one.

Flat fields, where the brown diagram is the background:

- `14_likeness_pairs`, frame 3955. The still reads SAME COLOUR · CROOKED LINES at the top.
- `03_rod_cloud`, frame 4898. The still reads DRAWING CHARGE FROM CLOUD at the bottom.
- `15_wet_dry`, frame 6410. The still reads WET TWINE · DRY SILK.
- `08_teach_charge`, frame 8506. The still reads NO BOLT, JUST CHARGE.
- `09_wood_vs_metal`, frame 10913. The still reads WOOD AND STONE RESIST.

Pictures with no bottom panel:

- `15_likeness_fire`, frame 4073. The still reads CRACK · FIRE · SHOCK over the picture. A gold line frames the diagram.
- `04_letter_crosses`, frame 5021. The still reads PHILADELPHIA TO PARIS over the ship, and the two boxes read PHILADELPHIA and PARIS. That is three labels at once. This is the current master, not the separate letter intermediate.
- `06_same_thing`, frame 8268. The midpoint has line diagrams and no title. A later still in the same row reads ELECTRICITY over the picture, still with no panel.
- `08_looking_path`, frame 10793. The still reads EASIEST PATH DOWN over cloud. An earlier frame of the row has no title.
- `10_metal_easy`, frame 11017. The still reads METAL CONDUCTS over the brick.

Every title that was read is four words or fewer. The five picture rows are the ones that still match the note about text over a moving picture with no background. The note stays open. These are stills and pixel checks, not a motion review, an audio review, or a film approval.

116 J2242 unit tests OK. check_all result is in `CHECK_ALL_BOTTOM_TEXT.txt`. No v04 master. Original masters and audio are unchanged. No spend, generation, UAT, R2 or YouTube action. No detached process.

Remaining: a background behind the five picture titles, the generalized packet mux, preservation and loudness/sync checks, and the mandatory film gates. Then J2243 and Chief review. Continue this PR #542 worktree. Frame 2869 stays out.

## Umber panels behind the picture titles — twenty-seventh run, 13 November 2026

Cursor worker. Frame 2869 stays out. `_j2242_title_panel.py` paints the caption umber, RGB 48,30,20, behind a title and nowhere else. Changed pixels are that colour only, so the panel has no border, gold rule or pill. The words themselves are the alpha glyphs and are left as they were.

The letter row is not painted. Its replacement is the cream letter on the moving ship plate, which has no banner and no boxes. The other four titles get the panel:

- `15_likeness_fire`, CRACK · FIRE · SHOCK, alignment MAE 16.488.
- `06_same_thing`, ELECTRICITY, alignment MAE 6.343. The midpoint of this row has no title; the still is the later frame where the word is on screen.
- `08_looking_path`, EASIEST PATH DOWN, alignment MAE 8.453.
- `10_metal_easy`, METAL CONDUCTS, alignment MAE 20.279, taken from master frame 11017 because the old composite file is not on disk. The rod graphic still crosses the panel, because those pixels are part of the graphic.

Stills, including the 168×94 phone stills, are in `/Volumes/MiniWork/scratch/J2242-title-panels-v01/`. The four titles read on those stills. This is a still check, not a motion review, an audio review, or a film approval. The panels are not yet on every frame of those rows, and they are not in a master.

122 J2242 unit tests OK, 6 of them new. No v04 master. Original masters and audio are unchanged. No spend, generation, UAT, R2 or YouTube action. No detached process.

Remaining: the same panel on every frame of those four rows, the generalized packet mux, preservation and loudness/sync checks, and the mandatory film gates. Then J2243 and Chief review. Continue this PR #542 worktree. Frame 2869 stays out.

## Umber panel on every aligned frame — twenty-eighth run, 13 November 2026

Cursor worker. Frame 2869 stays out. The letter row stays the cream letter, with no banner. `_j2242_title_panel.py --every-frame` paints the same unbordered umber, RGB 48,30,20, on every frame where the title is actually aligned. Changed pixels are that colour only. Frames with no title, and metal frames whose title does not match the aligned mask, are copied unchanged. The title box does not move inside a row.

The four lossless intermediates are FFV1 in RGB. Each file decodes back to the same bytes that were painted. They are not a master and they have no audio.

- `15_likeness_fire`: 95 of 114 frames painted, 19 kept because the title is not on screen yet. Check frame 53, MAE 16.488. SHA-256 `27e334e11f00` prefix, 84,545,944 bytes.
- `06_same_thing`: 53 of 160 frames painted, 107 kept with no title. The word arrives late. Check frame 134, MAE 6.364. SHA-256 `d561ae545199` prefix, 135,059,338 bytes.
- `08_looking_path`: 59 of 76 frames painted, 17 kept with no title. Check frame 48, MAE 8.453. SHA-256 `04617128a022` prefix, 75,607,282 bytes.
- `10_metal_easy`: master frames 10996 through 11037, which is the 42-frame row. Frame 11038 is the safe-path frame and is not in the row. 31 frames painted, 11 kept because the fade does not match the solid title at 1.5 s. Master frame 11017, MAE 20.279. SHA-256 `7da3cc334b60` prefix, 66,328,943 bytes.

Full hashes are in `TITLE_ROWS.json`. The files and the 168×94 stills are in `/Volumes/MiniWork/scratch/J2242-title-rows-v01/`. The rod graphic still crosses the metal panel, because those pixels are part of the graphic.

126 J2242 unit tests OK, 4 of them new. check_all result is in `CHECK_ALL_TITLE_ROWS.txt`. Every painted frame was checked as it was written: changed pixels are umber only, and the words stay. Each lossless file decodes back to those same frames. This is not a motion review, an audio review, or a film approval. No v04 master. Original masters and audio are unchanged. No spend, generation, UAT, R2 or YouTube action. No detached process.

Remaining: the generalized packet mux, preservation and loudness/sync checks, and the mandatory film gates. Then J2243 and Chief review. Continue this PR #542 worktree. Frame 2869 stays out.

## Closed-IDR packet plan — twenty-ninth run, 13 November 2026

Cursor worker. Frame 2869 stays out. No master was muxed. `_j2242_packet_mux.py --plan` reads the 113 IDR samples proved in `SOURCE_PREFLIGHT.json` and the placed intermediates. A changed frame expands to its whole IDR group. Frames outside those groups stay copied source packets. Replacement timestamps copy the original PTS and duration, including a 1024-tick step, and never use `setpts=N/24`.

41 placed changes become 35 groups. 4,569 frames would be re-encoded. 8,354 frames stay copied packets. 32 groups already have pixels for every frame. Three groups still need source pixels stitched in before an encode:

- Frames 2718–2887. The Franklin pieces stop around frame 2869. That one frame stays the master picture.
- Frames 3168–3343. The jar patch is 3260–3343. Frames 3168–3259 stay the master picture. Frame 3353 stays a copied packet, past this group.
- Frames 11038–11245. The safe-path intermediate is 11038–11117. Frames 11118–11245 stay the master picture. Frame 11118 is not in the intermediate.

The seven job groups are closed IDR groups: 423–544, 744–839, 2506–2665, 3168–3343, 4511–4670, 4977–5077 and 11358–11492. The 0:51 night street, frames 1129–1231, is a copied packet run. The rejected jar patch is not in the plan.

Three picture titles still have no master frame numbers, so they are not in this plan: `15_likeness_fire`, `06_same_thing` and `08_looking_path`. Metal is in it, frames 10996–11037. The letter row stays the cream-letter intermediate.

131 J2242 unit tests OK, 5 of them new. `check_all.sh` result is in `CHECK_ALL_PACKET_PLAN.txt`. This is not a motion review, an audio review, or a film approval. No v04 master. Original masters and audio are unchanged. No spend, generation, UAT, R2 or YouTube action. No detached process. H.264 packets, unchanged-frame hashes, loudness and sync are still outstanding.

Remaining: stitch the three partial groups from master pixels, encode each closed group, mux copied packets around them, then preservation, loudness and sync, and the film gates. Place the three unplaced title rows before that mux if they belong on the master. Then J2243 and Chief review. Continue this PR #542 worktree. Frame 2869 stays out.

## Master pixels in the three partial groups — thirtieth run, 13 November 2026

Cursor worker. No master was muxed. `_j2242_stitch_groups.py --render` fills the three groups that the packet plan left short. A timestamp join dropped frame 2870, so v01 and v02 are not used. v03 joins the decoded YUV frames instead. Each kept master frame matches the source framehash. Each replacement frame is unchanged. The pictures have no audio.

- Frames 2718–2887, 170 frames. Frame 2869 is the master picture between the Franklin pieces. SHA-256 `075e16561325345e522b98e020a7dd1910b3e34e6439b23f57adfcd20c0fabe4`.
- Frames 3168–3343, 176 frames. Frames 3168–3259 are the master picture, then the jar patch. Frame 3353 stays a copied packet, past this group. SHA-256 `2ce4d932995c30f73baea94bdaaa070f06566cb3b82a6ec3615d69d6df27a404`.
- Frames 11038–11245, 208 frames. The one-title safe path covers 11038–11117. The earlier safe path, which still has two titles, is not in the file. Frames 11118–11245 are the master picture. SHA-256 `9d3daceffd24872e868cde040a08b19bf1c46f212ce2f470444d5aea8877278e`.

The files and clocks are in `/Volumes/MiniWork/scratch/J2242-stitch-v03/`. `STITCH_GROUPS.json` records them. The original clock is in each sidecar. The nut timestamps are not the master clock.

136 J2242 unit tests OK, 5 of them new. `check_all.sh` result is in `CHECK_ALL_STITCH.txt`. This is a pixel check, not a motion review, an audio review, or a film approval. No v04 master. Original masters and audio are unchanged. No spend, generation, UAT, R2 or YouTube action. No detached process.

Remaining: give `15_likeness_fire`, `06_same_thing` and `08_looking_path` master frame numbers if they belong on the master, encode each closed group, mux copied packets and the original audio, then preservation, loudness and sync, and the film gates. Then J2243 and Chief review. Continue this PR #542 worktree. Frame 2869 stays the master picture inside its group.

## Picture-title placement — thirty-first run, 14 November 2026

Cursor worker. No master was muxed. The three picture titles now have master frame numbers, chosen by a unique full-frame match rather than the cut clock. `_j2242_title_place.py` slides each overlay across a 96×54 gray copy of all 12,923 master frames. A match has to stay under mean absolute error 0.5, with the next-best alignment at least 0.9 worse. Frame 2869 stays the master picture.

- `15_likeness_fire`, frames 4016–4129, 114 frames. The clock window is the same span. Mean error 0.2098, margin 1.7652. The last frame's full-resolution error is 5.384 because the diagram on the plate moves; the plate is the same picture. Stills of master frame 4129 and overlay frame 113 show that. This is a still check.
- `06_same_thing`, frames 8189–8348, 160 frames. Clock frame 8188 is the previous picture, full-resolution error 39.773 against overlay frame 0, so it stays the master. Mean error 0.2039, margin 2.5839.
- `08_looking_path`, frames 10777–10852, 76 frames. The cut clock is 10755–10830, which does not match the picture (full-resolution error 54.880 at frame 10755). The match runs 22 frames past that cut, through 10831–10852. Mean error 0.4175, margin 0.9256.

None of the three ranges overlaps an existing splice. The closed-IDR plan is now 44 changes, 4,928 frames to rebuild and 7,995 copied. 39 groups, 35 already complete. Four still need master pixels inside the group: 2869 inside 2718–2887, 3168–3259 ahead of the jar, 4130–4138 after the fire title, and 11118–11245 after the one-title safe path. Electricity and the path title fill their own groups. Night street 1129–1231 stays copied. Frame 3353 stays copied.

140 J2242 unit tests OK, 4 of them new. `check_all.sh` result is in `CHECK_ALL_TITLE_PLACE.txt`. This is a pixel check, not a motion review, an audio review, or a film approval. No v04 master. Original masters and audio are unchanged. No spend, generation, UAT, R2 or YouTube action. No detached process.

Remaining: stitch master frames 4130–4138 onto the fire title, encode each closed group, mux copied packets and the original audio, then preservation, loudness and sync, and the film gates. Then J2243 and Chief review. Continue this PR #542 worktree. Frame 2869 stays the master picture inside its group.

## Fire title tail — thirty-second run, 14 November 2026

Cursor worker. No master was muxed. `_j2242_stitch_groups.py --render` filled the four incomplete groups, including the nine master frames after the fire title. The three groups from the thirtieth run came back with the same picture hashes. Each kept master frame matches the source framehash. Each replacement frame is unchanged. The pictures have no audio.

- Frames 2718–2887, 170 frames. Frame 2869 is the master picture. SHA-256 `075e16561325345e522b98e020a7dd1910b3e34e6439b23f57adfcd20c0fabe4`.
- Frames 3168–3343, 176 frames. Frames 3168–3259 are the master picture, then the jar patch. Frame 3353 stays a copied packet. SHA-256 `2ce4d932995c30f73baea94bdaaa070f06566cb3b82a6ec3615d69d6df27a404`.
- Frames 4016–4138, 123 frames. The fire title covers 4016–4129. Frames 4130–4138 are the master picture. SHA-256 `c9f8733fcd5c317014aa0c25c22159407e40c7ce67aa5d21e416af281aac5000`.
- Frames 11038–11245, 208 frames. The one-title safe path covers 11038–11117. Frames 11118–11245 are the master picture. SHA-256 `9d3daceffd24872e868cde040a08b19bf1c46f212ce2f470444d5aea8877278e`.

The files and clocks are in `/Volumes/MiniWork/scratch/J2242-stitch-v04/`. `STITCH_GROUPS.json` records them. The original clock is in each sidecar. The nut timestamps are not the master clock.

140 J2242 unit tests OK. `check_all.sh` result is in `CHECK_ALL_FIRE_TAIL.txt`. This is a pixel check, not a motion review, an audio review, or a film approval. No v04 master. Original masters and audio are unchanged. No spend, generation, UAT, R2 or YouTube action. No detached encode is running.

Remaining: encode each closed group, mux copied packets and the original audio, then preservation, loudness and sync, and the film gates. The packet planner still only writes the plan. Then J2243 and Chief review. Continue this PR #542 worktree. Frame 2869 stays the master picture inside its group.

## First High-profile group encode — thirty-third run, 14 November 2026

Cursor worker. No master was muxed. x264 rejects lossless High profile. A group that still holds master frames is refused, because those frames have to match the source hashes and this encode is not lossless. `_j2242_encode_groups.py` encodes one fully changed yuv420p nut with the salon recipe: H264 High, qp 1, no B frames, one IDR for the group, no audio.

The Copley group, frames 9430–9486, is 57 frames. The nut hash is `6d3a1e1155ec8d787b4d6c6133c2cb701c7bdee53896c58dd44337889bf0d158`. The encode is `/Volumes/MiniWork/scratch/J2242-encode-v01/group_9430_9486_high.mp4`, 28,770,528 bytes, SHA-256 `f072d61f5eed6d5300ff9d79ac7bace45c25de13dc8e670da9a8967e8031d7a7`. ffprobe reads H264 High, yuv420p, 1920×1080, 57 packets and no audio. The lowest frame PSNR against the nut is 63.32 dB. The file's own timestamps are not the master clock. Evidence is `ENCODE_9430_9486.json`.

The same command then encoded every other fully changed yuv420p group that is already one nut. It finished with exit 0. 28 groups, 3,540 frames, are H264 High, silent, and at least 62.59 dB against their nuts. The files are in `/Volumes/MiniWork/scratch/J2242-encode-v01/`. Each `ENCODE_<first>_<last>.json` records the nut hash, the encode hash and the lowest frame PSNR. None of them is a master, and none carries the master clock.

Four groups stay refused because they still contain master frames: 2718–2887 (frame 2869), 3168–3343 (the jar keep), 4016–4138 (the fire tail) and 11038–11245 (the safe-path tail). These were also skipped: 272–422 and 423–544 because each is two nuts, salon 2506–2665 because its nut is not in the placed-file list, electricity 8189–8348 because the title nut is split across two IDR groups, the path title 10777–10852 because that nut is not yuv420p, and the metal title 10996–11037 because its nut is not in the placed-file list.

143 J2242 unit tests OK, 3 of them new. check_all result is in CHECK_ALL_ENCODE.txt. This is a frame measurement, not a motion review, an audio review, or a film approval. No v04 master. Original masters and audio are unchanged. No spend, generation, UAT, R2 or YouTube action. The encode process has ended. No detached encode is still running.

Remaining: encode the skipped and refused groups without giving up exact master pixels or the High profile, then mux copied packets and the original audio. Then preservation, loudness and sync, and the film gates. Then J2243 and Chief review. Continue this PR #542 worktree. Frame 2869 stays the master picture inside its group.

## Seven skipped groups encoded — thirty-fourth run, 14 November 2026

Cursor worker. No master was muxed. The seven fully changed groups that the single-nut pass skipped now have H264 High, qp 1, silent encodes, with no B frames. A group that still holds a master frame was not encoded. x264 still will not make a lossless High-profile encode, so those four groups stay pictures only.

`_j2242_group_nuts.py` builds one yuv420p nut per skipped group, then the existing High-profile recipe encodes it. The yuv view of each prepared nut matches the source frames. The nut clock is not the master clock.

- Frames 272–422, 151 frames, two nuts joined. Lowest frame 63.43 dB.
- Frames 423–544, 122 frames, two nuts joined. Lowest frame 62.91 dB.
- Frames 2506–2665, the 160-frame salon nut, used as it was. Lowest frame 62.70 dB. Nothing after source f060 is in that nut.
- Frames 8189–8268 and 8269–8348, the electricity title split across two IDR groups. The bgr0 nut was converted to yuv420p. Lowest frames 64.49 dB and 64.37 dB.
- Frames 10777–10852, the path title, 76 frames, bgr0 converted to yuv420p. Lowest frame 63.67 dB.
- Frames 10996–11037, the metal title, 42 frames, bgr0 converted to yuv420p. Lowest frame 63.62 dB.

The nuts are in `/Volumes/MiniWork/scratch/J2242-group-nuts-v01/`. The encodes joined the earlier files in `/Volumes/MiniWork/scratch/J2242-encode-v01/`. `GROUP_NUTS.json` and the seven `ENCODE_` records are the evidence. These files are not `hos_008_master_v04.mp4`.

Still refused, because each one still contains master frames that have to match the source hashes: 2718–2887 (frame 2869), 3168–3343 (the jar keep), 4016–4138 (the fire tail) and 11038–11245 (the safe-path tail).

145 J2242 unit tests OK, 2 of them new. check_all result is in `CHECK_ALL_GROUP_NUTS.txt`. This is a frame measurement, not a motion review, an audio review, or a film approval. No v04 master. Original masters and audio are unchanged. No spend, generation, UAT, R2 or YouTube action. The encode process has ended. No detached encode is still running.

Remaining: encode the four groups that still hold master frames without giving up those pixels or the High profile, then mux copied packets and the original audio. Then preservation, loudness and sync, and the film gates. Then J2243 and Chief review. Continue this PR #542 worktree. Frame 2869 stays the master picture inside its group.

## Changed runs inside the mixed groups — thirty-fifth run, 14 November 2026

Cursor worker. No master was muxed. The v03 master is H264 High and reports `has_b_frames` 2, so a kept frame inside these IDR groups can look forward into a frame this job replaces. x264 still will not make a lossless High encode, and a 4:4:4 lossless patch already broke later copied packets. `_j2242_mixed_split.py` therefore encodes only the changed runs, with the existing High qp 1 recipe, and leaves every master run unencoded.

- Frames 2718–2868, 151 frames. Frame 2869 is not in this file. Lowest frame 62.43 dB.
- Frames 2870–2887, 18 frames, after that one master frame. Lowest frame 62.66 dB.
- Frames 3260–3343, 84 frames. The jar keep 3168–3259 is not in this file. Lowest frame 63.09 dB.
- Frames 4016–4129, 114 frames. The fire tail 4130–4138 is not in this file. Lowest frame 64.28 dB.
- Frames 11038–11117, 80 frames. The safe-path tail 11118–11245 is not in this file. Lowest frame 68.45 dB.

447 frames. Each nut slice matches the stitched pictures for that run. The encodes are H264 High, silent, with no B-frames, in `/Volumes/MiniWork/scratch/J2242-encode-v01/`. These files are not `hos_008_master_v04.mp4`, and their clocks are not the master clock.

Still unencoded, because a High qp 1 picture would not keep the source hash: frame 2869, frames 3168–3259, frames 4130–4138, and frames 11118–11245. B-frames block treating any of those as a packet copy until a reference check says a frame does not look into a replaced frame.

148 J2242 unit tests OK, 3 of them new. check_all result is in `CHECK_ALL_MIXED_SPLIT.txt`. This is a frame measurement, not a motion review, an audio review, or a film approval. No v04 master. Original masters and audio are unchanged. No spend, generation, UAT, R2 or YouTube action. The encode process has ended. No detached encode is still running.

Remaining: a way to keep those four master runs exact while the changed pictures around them are High, then mux copied packets and the original audio. Then preservation, loudness and sync, and the film gates. Then J2243 and Chief review. Continue this PR #542 worktree. Frame 2869 stays the master picture inside its group.

## Reference check — thirty-sixth run, 14 November 2026

Cursor worker. No master was muxed. `_j2242_ref_check.py` reads the v03 slice headers and builds each picture's reference list inside the four mixed groups. The opening GOP matches the x264 pattern: the first P uses the IDR, and the B between them uses both. Inside every checked group, display order follows POC, a one-reference P uses the previous reference picture, and a one-reference B uses the nearest past and future reference pictures. Reference-list reordering and the short marking command that drops one older picture are both applied. Nothing here is a motion review or an audio review.

One kept run does not look at a replaced picture, so its original packets can stay:

- Frames 3168–3258, 91 frames, the jar keep up to but not including the last frame. These packets reference only pictures inside that run.

Four runs look at a picture this job replaces, so those original packets cannot sit beside the new High encode and still decode to the source hash:

- Frame 2869 is a P. It references frame 2866, which is inside the changed Franklin run 2718–2868.
- Frame 3259 is a B. It references kept frame 3258 and replaced frame 3260. Keeping 3259 exact would also keep the original picture at 3260.
- Frames 4130–4138, the fire tail. Frame 4130 references replaced frame 4129.
- Frames 11118–11245, the safe-path tail. Frame 11118 references replaced frame 11117.

153 J2242 unit tests OK, 5 of them new. check_all result is in `CHECK_ALL_REF_CHECK.txt`. This is a packet reference check, not a film approval. No v04 master. Original masters and audio are unchanged. No spend, generation, UAT, R2 or YouTube action. No detached process.

Remaining: copy frames 3168–3258 as original packets. The four blocked runs still need exact pixels while the pictures they reference stay the new High encodes. Then mux the copied packets and the original audio, and run preservation, loudness, sync and the film gates. Then J2243 and Chief review. Continue this PR #542 worktree. Frame 2869 stays the master picture inside its group.
