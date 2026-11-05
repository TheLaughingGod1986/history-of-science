# J2169 assembly evidence (5 Nov 2026)

Cursor built HOS 006 Short B and Short C from existing media. GBP0. No generation, no upload, no schedule, no privacy change, no Buffer write. This is not a PASS, not a KEEP, and not approval to publish. Nobody watched the picture or heard the sound in this session. Ben's watch is still the watch-and-listen check.

Standalone S7 (`hos_sa_s7_priestley_mint_v02`) was not built. Short A and retired s04/s05/s06 and superseded s07/s08 were not built. Long id `VbPubYd6Fbs` is recorded only so a later scheduler can check that the long is public first.

## Takes

- B is `t2_mint_fixed_vo_v03b.mp3`, sha256 `0f1099262037b62ea2b2a003ce86e196458fa983e9ca97877afb5600e97c7479`. Sentence 1 is "A sprig of mint repaired the air." and the alignment ends that sentence at 2.24 s. The soil take was not used. Last word "again." ends at 23.08 s.
- C is `t3_bubbles_sunlight_vo_v01.mp3`, sha256 `5b5d84e560d51ed9ad6f9bf5588f458802620f48f008b9409c532f8a1ea4e269`. Words were grouped from the character alignment. Last word "sunlight." ends at 24.16 s. The spoken line was not rewritten.

## Masters

Desk copies and matching NAS copies (`10_Shorts/J2169/` on the archive, `SHA256SUMS.txt` beside them):

| Cut | File | sha256 | Duration | Frames |
|---|---|---|---|---|
| B | `hos006_short_b_v01.mp4` | `08e3d6036744da57ae3fce1d12b996f913cd1d180161eba18590cffd23aeee0f` | 24.25 s | 582 |
| C | `hos006_short_c_v01.mp4` | `883cee08cb5e197ef6dfe5f44a1f8ae47cfeaa5c576a14f5aad2670fe516fbc2` | 25.166667 s | 604 |

Clean pictures: B `d1153d948ec85288fdc609c88ce93b7c071d53c489639a5f1cc06184790090c4`, C `900afaf937e7f2b3df57d2251988aa36c1cab8c076efddc297ab90aa7bf324a9`.

Output is 720×1280. A 720p plate cannot fill 1080×1920 under the 2.35× upscale fail. Cuts are integer 24 fps frames. Opening and return use the same source offset, because the terminal-loop contract requires that. The 0–1 s preroll on the C insert is unused. The return replays the opening's first second.

## Gates

Short B, clean picture and captioned master: `picture_qa` PASS (terminal-loop status `rendered_correspondence`; frame MAE on the clean picture 0.1509, 0.108, 0.2131, 0.2723). `polish_gate` PASS. `sfx_kit.py level` PASS. `music_gate` PASS. `gate_shorts_open.py` PASS for air date 2026-11-18 (24.25 s, −14.5 LUFS, −1.9 dBTP, first cut 2.25 s, open audio, frame-0 motion). WARNs, not fails: S07 low detail (edge density under the film p5), and the terminal-loop note that samples do not establish seamless motion. The locked first sentence ends at 2.24 s, so the 1.5 s surprise target is missed by the locked line. The line was not changed.

Short C, clean picture and captioned master: `picture_qa` FAIL and `polish_gate` FAIL. The only fail is S02, `01_villa_t1.mp4`, split panel, horizontal seams from the brick courses (clean picture: 0.057, 0.067, 0.076, 0.087, 0.107, 0.117, 0.417, 0.431, 0.437, 0.485). The terminal loop itself classified (`rendered_correspondence`; clean-picture MAE 0.2577, 0.1816, 0.3181, 0.3918). `sfx_kit.py level` PASS. `music_gate` PASS. `gate_shorts_open.py` PASS for air date 2026-11-21 (25.17 s, −14.1 LUFS, −1.8 dBTP, first cut 2.58 s). WARNs: S05 low detail, and the same terminal-loop human-review note.

The villa fail was not waived. A scan of other 9:16 crops found no crop that shows the house and stays clear of a full-width seam across the shot. No replacement plate was generated. The missing input for a passing C is a plate for "In 1779, a Dutch doctor" that still shows that house and does not trip `polish_gate` seams.

Hook text on C is two lines, "ONLY IN" and "THE LIGHT". One line spanned the frame and the captioned master then failed a seam on S01. The two-line hook clears that. It does not clear the villa.

## What the review decides

Look at S07 on B and S05 on C (low detail), and at the villa frame on C. Do not mark C ready for Ben while the split-panel fail stands. Do not set a watch card, do not upload, and do not treat either file as approved. A ruling that the brick courses are the house, rather than a split screen, is the reviewer's to write. A different existing plate is a new assembly job.
