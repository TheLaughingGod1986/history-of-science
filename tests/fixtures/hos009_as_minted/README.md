# Film 009: the boards as they were when the takes were made

The five v05 boards and `TRANCHE2_SCOPE_J2026.json` exactly as they were at history-of-science #528 (`4d94db91`,
11 Nov 2026), the last change before any of the twenty approved shots became a drawn diagram.

The picture tool (`07_Edit-Project/_mint_flow_v05_tranche2.py`) pins its boards by hash. Its tests of how a take is
guarded, priced, made and recorded stand on these copies (`tests/hos009_then.py`), so a later change to a real board
cannot break them. What is true of the real boards is tested in `tests/test_hos009_final_boards.py`.

When a real board changes (a KEEP record, a splice flag, a shot that becomes a drawn diagram), run
`python3 02_Video-Projects/009_The-Falling-Moon-Gravity/07_Edit-Project/_repin_tranche2_scope.py --write` in the same
pull request. These copies stay as they are.

Do not edit these files. `test_the_frozen_copies_are_not_edited` holds each one's sha256. If a shot the tool may
still make is changed on its real board, `test_every_other_row_reads_as_it_did_when_its_take_was_made` fails: copy
the new board here, and update the hashes, in the same reviewed change.
