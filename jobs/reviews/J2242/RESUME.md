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
