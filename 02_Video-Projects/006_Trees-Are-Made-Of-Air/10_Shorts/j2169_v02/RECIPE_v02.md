# J2169 v02 assembly

Short B v02 uses locked take t2_mint_fixed_vo_v03b. Sentence 1 is "A sprig of mint repaired the air." This is not the soil take.

Short C v03 uses locked take t3_bubbles_sunlight_vo_v01.

Output is 1080x1920. The six 1280x720 Flow plates are scaled to 1920x1080 with lanczos first, then cropped 608x1080, so the upscale into the frame is 1.776. The v01 masters at 720x1280 are kept.

Short C's opening and return both start at source time 0. That plate is already moving. Short B's pot plate is an ease-in at time 0: the open gate measured frame diff 1.05 and motion 5.1, under the 1.50 fail and the 10 warn. Both B rows therefore start at frame 33 (1.375 s), the earliest 608-wide in-point that still clears the gate once the centred hook is on the picture. The checker samples the opening and the return at that shared in-point and one frame before the return ends, and fails if those frames differ from the source by more than 8. A dissolve on the last part of the return would change that last frame, so this cut does not add one.

Short B cuts: the candle row ends at 16.292s, before "bright". The mint-and-candle row ends at 19.458s, before "the". The sky row takes the extra frame so the film stays 24.250s.

Short C shade row starts at 4.458s of short_c_s06_t01 (frame 107) and uses the 83 frames that remain. The sunlit-leaf row is one frame longer so the return still starts after the last word.

The frame-0 hook is Didot Bold, one word per line, cap about 8.2% of the frame, centred. Cream on the setup words, yellow on the hook words. Spoken captions are Didot cream chunks of a few words, including through the 9-14s title. The title is The Willow Tree / That Was Made of Air.

No generation, no upload. Long id VbPubYd6Fbs is not a publish instruction. Standalone S7 stays planned and is not built. Short A, s04, s05, s06, s07 and s08 are not built.
