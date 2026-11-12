# J2230 — Harvey cuff Short v02 (not a KEEP)

Cursor, 6 Nov 2026. £0. No upload, no awaits, no new voice or picture.

## What this cut is

`How Does a Blood Pressure Cuff Work?` lifted from locked Part 05, indices 193–251 (59 words). Sentence 1 is "A blood pressure cuff is his band." It ends at 2.52 s. The v01 opening "Your blood leaves your heart…" is not in this cut. v01 on disk is untouched.

- File: `/Users/benjaminoats/_desk/renders/J2230/s06_v02/hos_005_s06_blood_pressure_cuff_v02.mp4`
- sha256: `8ac9a2917a9842a872131554ad0c898df69fc226dae193a94f9195d9b8baa888`
- 23.10 s. Conditional slot Fri 20 Nov 2026, 11:30 London. 18 and 21 Nov are the Willow pair (J2263). Not scheduled.
- Frame 0 is `14_cuff_release_t2` at 2.0 s, crop x 700: the grey cuff on the arm, already moving.
- Voice and plates: NAS `hos-worktrees/2026-10-22/hos-005-blood`. Bed: the film's Part 05 bed.

## Gates

- `gate_shorts_open.py check --air-date 2026-11-20`: **PASS** (onset 0.06 s, first cut 2.67 s, motion 25.23, frame-0 diff 3.17, tail 0.64 s).
- Voice stem `vo_trimmed.wav`: **PASS**, mean −23.4 dB, peak −4.3 dB, 157 wpm. The mixed file fails mean loudness at −17.5 dB because the open-gate mix is about −14 LUFS. The stem is the speech check.
- polish_gate exit 0. picture_qa exit 0. One full-size look at 0:22 (low detail on the loop plate).
- music_gate exit 0. It warns the bed measures about 150 BPM against a 60–80 brief, and several older comparison files could not be read. A listener still has to judge the pace.
- freezedetect: no events. Caption check: 18 changes, ratio 1.0.

This session cannot listen or watch the moving cut. Do not treat it as KEEP, and do not put it on Ben's watch, until a reviewer with audio and picture says so.

## Still to do on this job

Willow's two cuts stay with J2263. Do not rebuild them.

1. Heart-pump v02 (`_desk/renders/J2230/s07_v02`, sha256 `51a4b10d74ae…`) still needs a listener on the possible extra "it circulates". Open gate already PASSed. Not KEEP.
2. Two Vaccine lifts. Inputs in `_desk/renders/J2230/vaccine_inputs_v01` are not finished Shorts. Eradication still opens on "A disease". The Vaccine long was still private in the 6 Nov snapshot (`ETynHpIYLeY`, publishAt 12 Nov 18:00Z). Recheck that it is public before any schedule. Conditional slots left: 25 Nov and 28 Nov.
