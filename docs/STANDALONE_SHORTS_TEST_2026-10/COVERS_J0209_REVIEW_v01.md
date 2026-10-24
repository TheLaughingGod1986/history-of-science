# J0209 — S1–S4 cover drafts for Chief

Codex covering, 12 October 2026. Draft only: Chief picks the words and scores HOOK / BAND / PHONE. No final OK or creative PASS is asserted here.

## Deliverables

All files are under the Mini HOS checkout:
`docs/STANDALONE_SHORTS_TEST_2026-10/covers_j0209_v01/`.

| Short | Draft words | Cover |
|---|---|---|
| S1 Herschel | HEAT beyond RED | hos_sa_s1_cover_v01.png |
| S2 Brand | GLOW not GOLD | hos_sa_s2_cover_v01.png |
| S3 Snow | REMOVE the HANDLE | hos_sa_s3_cover_v01.png |
| S4 Curie | BOOKS behind LEAD | hos_sa_s4_cover_v01.png |

Each PNG is 1080×1920. Each has a `_style.jpg` comparison against eight live covers and a `_phone.jpg` preview; `all_four_drafts.jpg` shows all four together. `COVERS_J0209_v01.json` records input/output SHA-256s, exact paths, font checksum and text boxes. No image files are included in this PR; review sheets are posted through the desk's image mechanism.

The composer uses only the four exact plates named in the brief, plus code-rendered rounded cream/gold type, thick dark outlines and one small teal middle word. No Explorer, crop, background generation or grade. All pixels below y=530 remain byte-for-byte identical to the decoded input plate (asserted before PNG save). No spend, uploads, schedule changes or Studio activity.

## Advisory visual observations — Chief decides

- HOOK: each draft has three words, adds to its listing title and names the physical effect/object or gives a concrete instruction. S2 follows the locked line “No gold. Instead, a white substance that glowed in the dark.”
- BAND: lettering sits above the thermometer, flask, handle-free pump and notebook box; the stack is in the top third. Top line spans approximately 85–90% of the frame.
- PHONE: all hooks remain legible in the vertical 110×196 tile. The centre 16:9 preview omits the top-third lettering on every cover; S1's crop also shows only part of its thermometer. This is a real limitation, not a passed phone gate. Moving the hook to the centre would conflict with the requested top-band placement and cover the hero object. Chief must decide the layout/crop trade-off before use; these drafts are not upload-ready.
- The code type follows the specified rounded/cream/gold/teal family but is more regular than the hand-painted live reference lettering. Chief should assess that style difference on the attached comparison sheets.

## Validation

Both required preview tools ran for every cover, exit 0 (eight invocations). Their exact commands and stdout are in `COVERS_J0209_CHECKS_v01.json`. These tools generate evidence sheets; they do not return a creative PASS/FAIL.

The required repository check suite returned exit 0:

```
-- no media: PASS
-- status board in sync: PASS
-- ElevenLabs guard tests: PASS
-- vo_check word tests: PASS
-- contract tests: PASS
-- package-lint: PASS
ALL CHECKS PASS
```

Contract tests: 20 passed. Existing package warnings remain for 004 neighbour title/Related video and missing caption files on 006–010; unrelated to the cover drafts. Full log: `COVERS_J0209_REPO_CHECKS_v01.txt`.

## Handoff

Park J0209 for Chief: choose draft wording and rule on HOOK / BAND / PHONE, including the centre-crop limitation. No action needed from Ben.

HOS `git pull` fetched current main but could not update the shared checkout because local untracked production files would be overwritten. Those files were preserved. Work was committed from a clean new worktree based on `origin/main` at `95b921b`, branch `codex/j0209-hos-covers`. The queue claim/progress is the owner record for this standalone job; no numbered film stage was taken over.

Rebuild on the Mini:

```sh
/opt/homebrew/opt/python@3.14/bin/python3.14 docs/STANDALONE_SHORTS_TEST_2026-10/compose_covers_j0209.py --media-root '/Users/benjaminoats/YouTube/History Of Science'
```
