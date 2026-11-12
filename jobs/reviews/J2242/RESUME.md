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
