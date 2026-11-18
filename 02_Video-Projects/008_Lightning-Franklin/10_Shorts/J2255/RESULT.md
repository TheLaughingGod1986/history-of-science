# J2255 — HOS 008 Short C v03

Cursor, 6 Nov 2026. £0. No upload, no schedule, no new Flow, Vertex or ElevenLabs take.

Master (not in git): `02_Video-Projects/008_Lightning-Franklin/10_Shorts/hos_008_short_C_v03.mp4`
sha256 `9f25a16de5fc7d454be7adbc0e301614c7b060cd28b10cd076bcd2b4a6642161`
22.708 s, 936×1664, 545 frames. Loudness −14.1 LUFS, true peak −1.9 dBTP.

Opening line ends at 2.68 s. First cut is at 2.833 s. Body audio is the unmodified 5.720–24.400 s slice of `hos_008_short_C_v02.wav`, starting at 2.90 s. The 2 Dec 11:30 slot stays empty.

| Gate | Result |
|---|---|
| `gate_shorts_open.py check --air-date 2026-12-02` | PASS. Comparison date only. Nothing is scheduled. dur=22.71s, motion=44.49, cut1=2.83s, vo_onset=0.09s, tail_gap=1.13s |
| `picture_qa.py` with the terminal-loop contract | PASS. 0 of 9 cuts fail. Sharpness warns at 2.31×. S08 low-detail warn (edge 0.0253 vs film p5 0.0258). Loop return classified. |
| `music_gate.py` | PASS. Own slice of `lightning008_score_bed_v02`, Pace 64–72, measured about 66.7 BPM. |
| `sfx_kit.py level` | PASS. VO −20.0 LUFS, SFX −37.5 LUFS. |
| `atempo_check.py` | PASS. No atempo above 1.06. |

Stills of frame 0, the 9–14 s title, a caption and the S08 card were looked at as stills. Moving picture and the mix were not watched or heard. That stays with Ben after Chief review.
