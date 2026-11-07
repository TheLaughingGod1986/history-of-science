# J0912 — HOS 008 Short A v04

Cursor, 7 Nov 2026. £0. Locked VO unchanged (`hos_008_short_A_v02.mp3`, sha256 `40ed4c4e2a1f2e58608cfe690bb8afd6e1d64c80eafb0a75f37d47648a7ba28e`). No upload, no generation, no schedule.

J2224 FIX: row s06 (15.76–19.52 s) is `09_charge_string_c1_t1.mp4` at 0.60 s (sha256 `611e2633f2ea7f4417272b91af41b857bb6733d416363918a17a111be56f9c80`), in place of the second stretch of `13_key_ribbon_t1.mp4`. The other seven rows, the NEVER HIT IT hook, the PHILADELPHIA · 1752 card (2.7–6.2 s), the 9–14 s long title, and the locked speech are the same as v03.

Title draft: **Why Was Franklin's Kite Experiment So Dangerous?**
On-screen long title at 9–14 s: **Why Did Franklin Fly a Kite in a Storm?**

Master: `10_Shorts/hos_008_short_A_v04.mp4`
sha256 `76d801a34714ba90f286330dfab1c9e38b3025502340f20c8e414a8907a3192d`
23.300 s, 952×1692. Same file on the Mini checkout and the NAS.
Loudness −14.3 LUFS, true peak −1.9 dBTP. Payoff “If” at 17.84 s (0.768 of 23.24 s). First word at 0.14 s.

| Gate | Result |
|---|---|
| `gate_shorts_open.py check --air-date 2026-11-18` | PASS. dur=23.3s, cut1=2.57s, vo_onset=0.14s, tail_gap=1.13s. The date is the comparison date only. Nothing is scheduled. |
| `polish_gate.py` | PASS. 0 of 8 rows failed. Loop plate s08 is a low-detail look-at (edge 0.0278 < film p5 0.0297). |
| `picture_qa.py` | PASS. 0 of 8 cuts fail. The v03 reuse at 0:18 is gone. Sharpness warns are the 2.35× cap, the same as v03. |
| `music_gate.py` | PASS. Own bed, about 66.7 BPM, brief Pace 64–76. Unreadable OWB UAT files are warnings. |
| `sfx_kit.py level` | PASS. VO −20.7 LUFS, SFX −50.6 LUFS. |

v03 (`f88315e0`) is left in place. This cut is for Chief review. It is not a Short PASS and it is not uploaded.
