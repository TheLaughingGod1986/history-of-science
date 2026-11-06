# J2169 rebuild evidence (6 Nov 2026)

Cursor rebuilt HOS 006 Short B as v02 and Short C as v03 from the plates and takes already on disk. GBP0. No generation, no upload, no schedule, no privacy change, no retitle, no Buffer write. This is not a PASS, not a KEEP, and not approval to publish. Six still frames were looked at. The moving picture was not watched and the sound was not heard. Ben's watch is still the watch-and-listen check.

J2258 asked for this rebuild. The v01 masters stay in `j2169_v01/` and on the NAS. They were not overwritten.

Standalone S7 (`hos_sa_s7_priestley_mint_v02`) was not built. It is not in `UPLOADS.json`. Short A, retired s04/s05/s06 and superseded s07/s08 were not built. Long id `VbPubYd6Fbs` is recorded only so a later scheduler can check that the long is public first. The upload record still lists that long as private with `publishAt` 2026-11-05T18:00Z. This job did not read Studio again and did not schedule either Short.

## Takes

- B is `t2_mint_fixed_vo_v03b.mp3` at `/Users/benjaminoats/_desk/006/shorts_vo_20261004/vo/`, sha256 `0f1099262037b62ea2b2a003ce86e196458fa983e9ca97877afb5600e97c7479`. That is the same hash recorded in `j2169_v01/ASSEMBLY.md`. Sentence 1 in `words.json` is "A sprig of mint repaired the air." and ends at 2.24 s. The soil take was not used. The alignment has 57 words. The last word "again." ends at 23.08 s. `spoken.txt` is that mint line. J2258 printed a different full sha256 that does not match this file.
- C is `t3_bubbles_sunlight_vo_v01.mp3` in the same desk folder, sha256 `5b5d84e560d51ed9ad6f9bf5588f458802620f48f008b9409c532f8a1ea4e269`. Same hash as the v01 assembly note. Sentence 1 is "Leaves only make oxygen in the light." and ends at 2.56 s. The alignment has 56 words. The last word "sunlight." ends at 24.16 s. The spoken line was not rewritten. J2258's printed full sha256 does not match this file either.

The film-folder copies named in `BUILD_RULE_v02.json` are not in the checkout. The desk files are the ones hashed above.

## Masters

Output is 1080×1920, 24 fps, h264. ffmpeg decode of both masters exited 0.

Desk copies and matching NAS copies (`10_Shorts/J2169/` on the 22 Oct hos-006-trees archive). SHA-256 was read from both sides on 6 Nov 2026. `SHA256SUMS_v02.txt` matches.

| Cut | File | sha256 | Duration | Frames | Bytes |
|---|---|---|---|---|---|
| B v02 | `Short_B_v02/hos006_short_b_v02.mp4` | `f4b046d41d0d6fcfbd14258abe472d57db5c9d53c1ed535141aa3281e1f3915b` | 24.250 s | 582 | 20,893,457 |
| C v03 | `Short_C_v03/hos006_short_c_v03.mp4` | `e1e3ff0ce3b5622b4a43d010a0df827bcd34e25ccd76a87338b286b0632c40c5` | 25.167 s | 604 | 30,846,220 |

Desk path: `/Users/benjaminoats/_desk/renders/J2169/`. The v01 files in `Short_B/` and `Short_C/` were left in place.

## What changed from J2258

1. Spoken captions run through the 9–14 s title. A still at 11.2 s on B shows "He slid in a sprig" under "The Willow Tree / That Was Made of Air". A still at 11.2 s on C shows "Tiny silver" under the same title. Sentence 1 stays on screen through the opening row: B's hook is still up at 2.10 s (the row ends at 2.25 s) and C's hook is still up at 2.40 s (the row ends at 2.583 s). Later lines are Didot cream chunks of a few words.
2. Frame 0 hook is Didot, one word per line, centred. B reads MINT / FIXED in cream and THE / AIR in yellow, over the jar with the mint in it. C reads ONLY / IN in cream and THE / LIGHT in yellow, over the leaf and the bubbles. The builder refuses a hook whose H cap is outside 8–10% of 1920 and this render completed. The painted pixels were not measured again after that check.
3. B S05 ends at 16.292 s, before "bright". B S06 ends at 19.458 s, before "the". B S07 takes the extra frames so the film stays 24.250 s. C S06 starts at source time 4.458 s.
4. The six 1280×720 Flow plates are scaled to 1920×1080 with lanczos before the 608×1080 crop. The cut list records upscale 1.776.

Short B does not follow the written "start both rows at source time 0 and dissolve the return" line. At source time 0 the open gate measured frame diff 1.05 and motion 5.1, which fails the open. Both B rows (opening and return) start at frame 33, source time 1.375 s. That is the same in-point, so the loop checker can compare them. A dissolve on the last part of the return would change the frame the checker samples, so none was added. After that in-point the open gate on the master is PASS: frame diff 2.15, motion 10.36, first cut 2.25 s. Short C does start at source time 0 on opening and return. It also has no dissolve, for the same checker reason. The reviewer decides whether that meets the loop note.

## Gates

Both offered masters: `picture_qa` PASS, `polish_gate` PASS, `sfx_kit.py level` PASS, `music_gate` PASS, `gate_shorts_open.py` PASS (B air date 2026-11-18, C air date 2026-11-21). B level −14.5 LUFS, −1.9 dBTP. C level −14.1 LUFS, −1.8 dBTP. The gate's own last-word time on B is 23.2 s (tail 1.05 s). The alignment's last word ends at 23.08 s.

WARNs, not fails, left for the reviewer:

- B S07 low detail on the sky plate. J2258 kept this plate and this crop.
- C S05 low detail on the jar plate in `picture_qa`. J2258 kept this plate and this crop.
- C S03 low detail on the plunge-leaf plate in `polish_gate`. This warn was not in the J2258 KEEP list.
- Terminal loop on both cuts: status `rendered_correspondence`. The tool says the samples do not establish seamless motion.
- `music_gate` could not read several older Orbit beds that are not on this disk. It did not fail the trees bed.

## What the review decides

Look at the new captions, the centred hooks, the B in-point at 1.375 s, the missing dissolve, and the warns above. Do not treat either file as approved. Do not upload, schedule, retitle or change privacy. Do not set a watch card unless the verdict is KEEP, and then only with working unique Play links. Watched and heard stay false until Ben's watch. Slots 18 Nov and 21 Nov at 11:30 are planning targets. The long `VbPubYd6Fbs` has to be public before either Short.
