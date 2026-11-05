# J2169 assembly evidence (5 Nov 2026)

Cursor built HOS 006 Short B and Short C from existing media. GBP0. No generation, no upload, no schedule, no privacy change, no Buffer write. This is not a PASS, not a KEEP, and not approval to publish. Nobody watched the picture or heard the sound in this session. Ben's watch is still the watch-and-listen check.

Standalone S7 (`hos_sa_s7_priestley_mint_v02`) was not built. It remains a separate planned standalone export. Short A and retired s04/s05/s06 and superseded s07/s08 were not built. Long id `VbPubYd6Fbs` is recorded only so a later scheduler can check that the long is public first.

## Takes

- B is `t2_mint_fixed_vo_v03b.mp3`, sha256 `0f1099262037b62ea2b2a003ce86e196458fa983e9ca97877afb5600e97c7479`. Sentence 1 is "A sprig of mint repaired the air." and the alignment ends that sentence at 2.24 s. The soil take was not used. Last word "again." ends at 23.08 s. 57 words.
- C is `t3_bubbles_sunlight_vo_v01.mp3`, sha256 `5b5d84e560d51ed9ad6f9bf5588f458802620f48f008b9409c532f8a1ea4e269`. Words were grouped from the character alignment. Sentence 1 is "Leaves only make oxygen in the light." and ends at 2.56 s. Last word "sunlight." ends at 24.16 s. 56 words. The spoken line was not rewritten.

## Masters

Desk copies and matching NAS copies (`10_Shorts/J2169/` on the 22 Oct hos-006-trees archive, `SHA256SUMS.txt` checked on the NAS):

| Cut | File | sha256 | Duration | Frames |
|---|---|---|---|---|
| B | `hos006_short_b_v01.mp4` | `08e3d6036744da57ae3fce1d12b996f913cd1d180161eba18590cffd23aeee0f` | 24.25 s | 582 |
| C centre crop, kept | `hos006_short_c_v01.mp4` | `883cee08cb5e197ef6dfe5f44a1f8ae47cfeaa5c576a14f5aad2670fe516fbc2` | 25.17 s | 604 |
| C corner crop | `hos006_short_c_v02.mp4` | `3f8c1390523cbf05632abefb592b178b2b211c0e74ae31e9c4b7b96423091327` | 25.17 s | 604 |

Clean pictures: B `d1153d948ec85288fdc609c88ce93b7c071d53c489639a5f1cc06184790090c4`, C v02 `a1ef55df1c7ea819a76b806d34bd3ce623ab589b4e6667129c58a9974f77d952`.

Output is 720×1280. A 720p plate cannot fill 1080×1920 under the 2.35× upscale fail. Cuts are integer 24 fps frames. Opening and return use the same source offset, because the terminal-loop contract requires that. The 0–1 s preroll on the C insert is unused. The return replays the opening's first second.

## Gates

Short B, clean picture and captioned master: `picture_qa` PASS (terminal-loop status `rendered_correspondence`; frame MAE on the clean picture 0.1509). `polish_gate` PASS. `sfx_kit.py level` PASS. `music_gate` PASS. `gate_shorts_open.py` PASS for air date 2026-11-18 (24.25 s, −14.5 LUFS, −1.9 dBTP, first cut 2.25 s). WARNs, not fails: S07 low detail, and the terminal-loop note that samples do not establish seamless motion.

Short C v01 (centre crop 656,0,608,1080) failed `picture_qa` and `polish_gate` on S02. The brick courses of `01_villa_t1` are full-width straight lines. That file is kept. It is not the cut offered for review.

Short C v02 uses the same plate at crop 144,0,608,1080. That window still shows the house, the corner stones and the jars. Sampled frames through the 75-frame shot, scaled the way the gate scales them, had no seam, including the last included frame at 3.083 s. Clean picture and captioned master: `picture_qa` PASS and `polish_gate` PASS. The terminal loop classified (`rendered_correspondence`; clean-picture frame-0 MAE 0.258). `sfx_kit.py level` PASS. `music_gate` PASS. `gate_shorts_open.py` PASS for air date 2026-11-21 (25.17 s, −14.1 LUFS, −1.8 dBTP, first cut 2.58 s, open audio, frame-0 motion). WARNs: S05 low detail, and the same terminal-loop human-review note.

## LEARNINGS rule 8

Frame 0 of both cuts is moving footage of the named thing. Neither line contains a meta-promise. Sentence 1 of each names the subject and the surprise: mint repaired the air; leaves make oxygen only in the light. Both sentences end after 1.5 s (2.24 s and 2.56 s) because the locked takes were not rewritten. No new voice was spent. Scheduling is not requested.

## What the review decides

Look at B S07 and C S05 (low detail) and at the terminal-loop note. Do not treat either file as approved. Do not upload, schedule, retitle or change privacy. Do not set a watch card unless the review is KEEP. Watched and heard stay false until Ben's watch. Slots 18 Nov and 21 Nov at 11:30 are planning targets. The long `VbPubYd6Fbs` has to be public before either Short.
