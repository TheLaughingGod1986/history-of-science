# J0217 — HOS S5–S8 covers for Chief KEEP

Codex covering, 13 October 2026. Four draft covers composed from the exact existing frame-0 plates; no generation or spend. Chief owns KEEP, HOOK / BAND / PHONE and final approval.

| Short | Cover wording |
|---|---|
| S5 | BLAMED the PIGEONS |
| S6 | SAVED by MOULD |
| S7 | MINT fixed AIR |
| S8 | BLOOD eight feet UP |

Media on Mini: `docs/STANDALONE_SHORTS_TEST_2026-10/covers_j0209_v01/hos_sa_s{5..8}_cover_v01.png`, each 1080×1920. Combined sheet: `s5_s8_drafts_j0217.jpg`; individual `_style.jpg` and `_phone.jpg` files beside them. Manifest `COVERS_J0217_v01.json` records exact source/output SHA-256s and lettering boxes. All pixels below y=530 are unchanged. Existing S1–S4 remain the composer's default; explicit `--only s5 s6 s7 s8 --job J0217` selects this batch.

Advisory visual observations: S5's last line is raised 25 px to clear the horn. S8's lower two lines use the clear left side of the top band to avoid its tube mounting, so its stack is asymmetric and its middle phrase smaller. Chief should judge that balance and phone legibility. All four hooks complement rather than repeat their listing titles. As in J0209, the centre 16:9 preview excludes top-band lettering; this limitation remains explicit, not a creative PASS. Full-height previews show the lettering. No final OK asserted.

## Check evidence

`style_sheet.py short` and `thumb_preview.py short` completed for all four covers, exit 0 ×8. Exact commands/stdout: `COVERS_J0217_CHECKS_v01.json`. These tools create evidence, not creative verdicts.

Requested `_stems_level_v01.py --only s5 s6 s7 s8 --sfx-kit <OWB>/scripts/sfx_kit.py` completed with exit 0:

```
s5_penzias_pigeons: level exit 0 cover ok
SFX level PASS: VO -19.3 LUFS, SFX -38.9 LUFS, 1 hits
s6_fleming_mould: level exit 0 cover ok
SFX level PASS: VO -19.9 LUFS, SFX -34.9 LUFS, 1 hits
s7_priestley_mint: level exit 0 cover ok
SFX level PASS: VO -19.2 LUFS, SFX -34.9 LUFS, 1 hits
s8_hales_blood: level exit 0 cover ok
SFX level PASS: VO -20.0 LUFS, SFX -34.9 LUFS, 1 hits
```

`SFX_LEVEL_v01.json` now has all four cover paths and `all_pass: true` (technical check only). No cuts or spoken lines changed.

Repository `check_all.sh`: exit 1 solely because the base branch's generated STATUS.md and kanban/index.html are stale. No board input or output is changed by this cover PR. No-media, ElevenLabs guard, VO word tests, contract tests and package lint passed. Exact log: `COVERS_J0217_REPO_CHECKS_v01.txt`. Chief's board owner must resolve the existing stale-board check before merge; no gate is waived.

Work committed from clean worktree `/private/tmp/j0217-hos-wt`, based on origin/main 5587eab. Shared-checkout production changes preserved; only the requested level script ran there, and only S5–S8 report changes were copied into this PR. The queue claim is the owner record for this standalone task (no numbered film stage).

Next: Chief KEEP / layout decision, then remaining listings and package approval through their own jobs. J0217 parked for Chief. No upload, scheduling or YouTube changes; nothing needed from Ben.
