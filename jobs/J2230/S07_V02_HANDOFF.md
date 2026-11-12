# J2230 — Harvey heart-pump Short v02 (not a KEEP)

Cursor, 6 Nov 2026. £0. No upload, no awaits, no new voice or picture.

## What this cut is

`How Does the Heart Pump Blood?` rebuilt from the locked Part 03 voice and the existing plates. Sentence 1 is "The heart isn't a stove." The end-card line "watch the full film" is gone. The last 3 seconds are the opening plate only.

- File: `/Users/benjaminoats/_desk/renders/J2230/s07_v02/hos_005_s07_heart_pulse_v02.mp4`
- sha256: `51a4b10d74ae0981c8dfc66e59696f3174802ef6da5c2697861dbce877970703`
- 25.10 s, 64 words. Conditional slot 23 Nov 2026, 11:30 London. Not scheduled.
- Plates and raw voice: NAS `hos-worktrees/2026-10-22/hos-005-blood`. Raw voice sha256 matches `VO_FINISH_v01.json` (`0c1f5c5467a01ccc3d21dc59183c069ade6c6ec100138491617692eb86cf4e89`).
- v01 on the NAS was left untouched (`a6513555…`).

## Gates

- `gate_shorts_open.py check --air-date 2026-11-23`: **PASS** (onset 0.09 s, first cut 1.53 s, tail 0.58 s).
- polish_gate exit 0. picture_qa exit 0, with one full-size look at 0:10 (low detail on the wrist plate).
- music_gate exit 0. It also warns the bed measures about 48 BPM against a 60–80 brief, and several older comparison files could not be read. A listener still has to judge the pace.
- `vo_check_py312.sh` on the voice stem: mean −23.8 dB, peak −5.1 dB, and a word-check **FAIL** — heard "about a minute it circulates" where the script ends "about a minute" (~0:24.22). The alignment cut ends at 92.859 s, and the next locked word ("But") starts at 93.020 s, so that extra phrase is not in the planned interval. This session cannot listen. Do not treat the cut as KEEP until a reviewer with audio decides whether the insert is real.

The same word check on the mixed file fails mean loudness (−17.6 dB). That is the −14 LUFS mix the open gate requires. The stem, not the mix, is the speech-level check.

## Still to do on this job

Willow's two cuts stay with J2263. Do not rebuild them.

Still to build, same rules, no new generation:

1. Harvey blood-pressure cuff. The archived s06 opens on "Your blood…", not the cuff, and it fails the open gate on loudness. A new version has to name the cuff in sentence 1 using locked words only.
2. Two Vaccine lifts. The inputs in `_desk/renders/J2230/vaccine_inputs_v01` are not finished Shorts. Eradication still opens on "A disease". Variolation's recommended title is "What Is Variolation?" The Vaccine long was still private in the 6 Nov snapshot (`ETynHpIYLeY`, publishAt 12 Nov 18:00Z). Recheck that it is public before any schedule.

No Ben watch card until a reviewer says KEEP.
