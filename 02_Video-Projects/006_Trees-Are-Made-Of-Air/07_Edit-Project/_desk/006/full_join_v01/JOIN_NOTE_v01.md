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

## picture_qa — PASS after Chief ruling (a), 16 Oct 2026 (J0331)

The first run (J0312) FAILed 6 of 91. All six were the same plate coming back later in the film on the stretch it already used. Each part passed on its own, because the repeat is in another part. The plates are 6–8 s with the first stretch at offset 0, so a legal second stretch would need a longer plate.

Chief ruling (a) (16 Oct, HOS #180): reuse waived, no mint, no full_join_v02. Recorded in `picture_qa_reviewed_ok_v01.json` (`kinds: ["reuse"]`). Re-run on the same master (`sha256 7bf649f8…`, NAS `full_join_v01/hos_006_full_join_v01.mp4`): **PASS, 0 of 91 fail.** The six callbacks are listed under "Passed on Claude's ruling" in `PICTURE_QA.md`. Log: `picture_qa_v02.txt`. The original FAIL log stays in `picture_qa_v01.txt`.

- 5:12 `07_priestley_callback` (`11_candle_tall_t1.mp4`) same stretch as 3:57 — waived
- 6:55 `09_helmont_willow` (`06_garden_years_t2.mp4`) same stretch as 1:33 — waived
- 7:00 `10_air_threads` (`01_willow_air_t1.mp4`) same stretch as 0:02 — waived
- 7:11 `12_scales_barely` (`12_pointer_short_t1.mp4`) same stretch as 1:57 — waived
- 7:16 `13_water_in_tree` (`05_pure_water_t1.mp4`) same stretch as 1:26 — waived
- 8:04 `21_three_objects` (`03_pot_jar_leaf_t1.mp4`) same stretch as 0:11 — waived

Five WARNs (low detail), unchanged, including the Part 02 pounds graphic that J0290 already reported as a WARN. Sheet: `picture_qa_review.jpg`.

## polish_gate — PASS

0 of 91 rows failed. The same five low-detail WARNs as picture_qa (the pounds graphic, two plates, the shimmer, the night jars). `polish_gate_v01.txt`.

## vo_check — FAIL (one word)

`vo_check_py312.sh` on the joined file against `trees_script_master_v02.md`. 8:27.81, 1,213 words heard and 1,213 in the script, 151 wpm, mean −21.9 dB, peak −2.2 dB, no pause over 1 s. The four part joins did not open a hole.

FAIL: at 1:08.32 the script says "hidden water could fool the scales then" and small.en heard "fall". The checker did not mark it sounds-alike. Three other swaps (take/takes, Ingenhousz, Théodore) are warns and marked sounds-alike.

No new take. The VO is the locked v02 already accepted on the parts. Regenerating would spend ElevenLabs. Chief can listen to that one second and say whether it is the take or the transcriber.

## Not a film PASS

Parked for Chief final OK and squash-merge of #335 (J0331). picture_qa now PASSes on ruling (a). The vo_check "fool"/"fall" word was already waived. No bed. No full_join_v02 and no mint. Teach rows for Codex are in `TEACH_OVERLAYS_v01.md`; J0332 waits on that merge.
