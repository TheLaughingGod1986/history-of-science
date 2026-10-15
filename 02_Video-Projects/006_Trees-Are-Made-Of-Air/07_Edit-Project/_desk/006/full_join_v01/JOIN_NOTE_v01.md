# HOS 006 full join v01 (J0312, 15 Oct 2026)

Stream-copy of the five roughs that passed `picture_qa` and `polish_gate` on their own. No re-encode. Voice is the audio already in each rough. No music bed: `05_Music` does not exist, and a new bed waits for the Chief (credit hold until 30 Oct).

| Part | File | sha256 prefix | Duration |
|---|---|---|---|
| 01 v01 | `hos_006_part01_rough_v01.mp4` | `69974f305a34` | 61.667 s |
| 02 v03 | `hos_006_part02_rough_v03.mp4` | `7ef9c117b295` | 117.000 s |
| 03 v03 | `hos_006_part03_rough_v03.mp4` | `1067c0661b8e` | 94.833 s |
| 04 v02 | `hos_006_part04_rough_v02.mp4` | `e639e9bbe2b6` | 91.917 s |
| 05 v01 | `hos_006_part05_rough_v01.mp4` | `b3ca1afb9cd9` | 142.375 s |

Joined file: `hos_006_full_join_v01.mp4`, 507.813 s (8:27.8), sha256 `7bf649f857acc6a66b88347dd5351fb183c73a491f268e7543e14efc5155cde6`, 91 cuts. ffmpeg reported non-monotonic DTS at the four part joins (each part was encoded on its own). The file duration matches the sum within 0.03 s.

NAS copy: `/Volumes/data/mac-mini-archive/YouTube/History Of Science/02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project/full_join_v01/hos_006_full_join_v01.mp4`

## picture_qa — FAIL, 6 of 91

All six are the same plate coming back later in the film on the stretch it already used. Each part passed on its own, because the repeat is in another part.

- 5:12 `07_priestley_callback` (`11_candle_tall_t1.mp4`) same stretch as 3:57
- 6:55 `09_helmont_willow` (`06_garden_years_t2.mp4`) same stretch as 1:33
- 7:00 `10_air_threads` (`01_willow_air_t1.mp4`) same stretch as 0:02
- 7:11 `12_scales_barely` (`12_pointer_short_t1.mp4`) same stretch as 1:57
- 7:16 `13_water_in_tree` (`05_pure_water_t1.mp4`) same stretch as 1:26
- 8:04 `21_three_objects` (`03_pot_jar_leaf_t1.mp4`) same stretch as 0:11

Five WARNs (low detail), including the Part 02 pounds graphic that J0290 already reported as a WARN. Sheet: `picture_qa_review.jpg`.

This is not a film PASS. Chief decides whether those six callbacks get a new stretch or a reviewed-ok.

## polish_gate — PASS

0 of 91 rows failed. The same five low-detail WARNs as picture_qa (the pounds graphic, two plates, the shimmer, the night jars). `polish_gate_v01.txt`.

## vo_check — FAIL (one word)

`vo_check_py312.sh` on the joined file against `trees_script_master_v02.md`. 8:27.81, 1,213 words heard and 1,213 in the script, 151 wpm, mean −21.9 dB, peak −2.2 dB, no pause over 1 s. The four part joins did not open a hole.

FAIL: at 1:08.32 the script says "hidden water could fool the scales then" and small.en heard "fall". The checker did not mark it sounds-alike. Three other swaps (take/takes, Ingenhousz, Théodore) are warns and marked sounds-alike.

No new take. The VO is the locked v02 already accepted on the parts. Regenerating would spend ElevenLabs. Chief can listen to that one second and say whether it is the take or the transcriber.

## Not a film PASS

Parked for Chief. The six cross-part reuse FAILs and the one vo_check word are the open items. Teach rows for Codex are in `TEACH_OVERLAYS_v01.md`. No bed.
