# 006 teach lay v01 (J0351)

21 silent teach overlays from `teach_overlays_v01/` are composited onto `hos_006_full_join_v01.mp4`. The voice is a straight copy of the join. No music bed. No mint. No spend.

The master is on the Mini (gitignored):

`02_Video-Projects/006_Trees-Are-Made-Of-Air/07_Edit-Project/full_join_v01_teach/hos_006_full_join_v01_teach.mp4`

- sha256 `e505469682711d68c3609916ca08e1f572a81dd97ead5f1d3e4bf1d02e436105`
- video 507.833 s, 12,188 frames
- audio byte-matches the join (`cmp` of the ADTS copies)
- same file also at `/private/tmp/j0351-lay/hos_006_full_join_v01_teach.mp4`

The NAS folder `full_join_v01_teach` was not written. Listing `006_Trees-Are-Made-Of-Air` on the share hung, and `mkdir` on that path sat for six minutes before it was killed. The share's top level still answers `ls -ld`. Nothing was written under `/Volumes/data` in this run.

Three pairs that share a clock are sequenced, not stacked (see `_lay_teach_overlays_v01.py`): Stephen Hales then the Teddington timeline, the Bubbles chapter card then the Near London timeline, and de Saussure then the Geneva timeline. Jean Senebier's card ends as the de Saussure card starts.

## Gates (not a film PASS)

`picture_qa` and `polish_gate` both FAIL: 9 of 91 cuts. Six further cuts are warnings for a full-size look. Reports: `PICTURE_QA.md`, `polish_gate.json`, `picture_qa_review.jpg`, `teach_laid_sheet.jpg`.

Every fail falls inside an overlay window:

| time | cut | seam | overlay |
|---|---|---|---|
| 0:28 | 06_aristotle | horizontal 0.73 | who_aristotle, lower third |
| 0:42 | 09_vilvoorde | horizontal 0.465 | timeline_d1, full-frame timeline |
| 0:48 | 10_van_helmont_sack | horizontal 0.73 | who_helmont, lower third |
| 1:43 | 09_weights_169 | horizontal 0.73 | num_169, lower third |
| 1:47 | 10_fallen_leaves | horizontal 0.73 | fact_leaves, lower third |
| 3:07 | 02_hales_branch | horizontal 0.73 | who_hales, lower third |
| 3:28 | 06_leeds_brewery | horizontal 0.465 | timeline_d3, full-frame timeline |
| 3:33 | 07_priestley | horizontal 0.731 | who_priestley, lower third |
| 4:50 | 03_plunge_leaf | horizontal 0.73 | num_500, lower third |

The 0.73 line is the top of the lower-third card. The 0.465 line is the timeline rule. Parked for Chief. This is not a film PASS.
