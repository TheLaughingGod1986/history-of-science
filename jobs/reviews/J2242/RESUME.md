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
