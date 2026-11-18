# J2537: private history-rewrite rehearsal

18 November 2026, Codex, elected acting HOS Chief. Stage 3 rehearsal succeeded on the snapshot below. No live history was rewritten or pushed. Stage 4 is not ready to execute.

## Evidence

The detached backup finished with exit 0. Its full bundle contains 1,171 advertised refs and is stored privately on the NAS at the path in REHEARSAL_RESULT.json. The backup driver verified the bundle and matching local/NAS SHA-256 before this rehearsal. The original mirror and bundle were left untouched.

Source main: `2bb159443526b87681006fdb0ff93625e5192371`.
Rehearsed main: `eecfcaa3ae67341f164f063d09fcd40a03ef4d5c`.
Both have exactly the same Git tree: `6da6bb52b631fc7f706f27ce1f13523015ab80f3`. This verifies every current filename, mode and file byte, including existing account-fingerprint comparisons.

All 2,885 commits were mapped and changed; none was dropped. All 1,171 ref names remain: 511 branches, 3 tags and 657 pull-request refs. The local commit and ref mappings are recorded beside this report. Rehearsing GitHub pull refs locally does not mean they can be pushed to GitHub.

Before: 8,530 matches across 1,157 blob objects and 2,570 commit objects, representing 11 distinct literal address strings. After: zero matches across all 2,885 commits, 15,656 trees and 18,212 blobs reachable from every ref. Ref names also have zero matches. Git fsck --full passed.

## Replacement scope decision

For this private rehearsal, the Chief includes personal author, committer and tagger email fields, names containing addresses, and commit/tag messages as well as historical file contents. Otherwise a clean file scan would leave the same information in metadata. The studio personal-domain pattern is used case-insensitively, including escaped dots. This is not a claim that arbitrary organisation addresses, images containing text, encoded strings or other personal information have been scrubbed.

Historical content uses the neutral role label `the account holder`; personal metadata addresses use deterministic non-deliverable placeholders on the reserved example.invalid domain. No identity is guessed from frequency. The private literal replacement inventory stays in scratch and is never committed or printed. Organisational addresses are outside this job's personal-account scope. Existing main's more specific role labels and hashed comparisons are unchanged. Filtering may remove cryptographic signatures and rewrites commit-ID references in commit messages; the old/new maps remain the reference for historical links.

## Retained review inputs

Every file on each retained head was compared. Non-address-bearing blobs are identical; every altered blob is exactly the declared role-label substitution. Paths, modes and file counts are unchanged.

| Retained branch | Files unchanged | Historical files scrubbed | Preserved PR inputs changed |
|---|---:|---:|---:|
| codex/J2498-timing-rough | 8,998 | 15 | 0 of 138 |
| review/013-pass1-sheets | 8,386 | 378 | 0 of 58 |
| codex/J3050-billing-proposal | 9,639 | 0 | 0 of 4 |

Thus all 200 specifically preserved review inputs keep their blob hashes. Changed historical paths and both SHA-256 values are listed in REHEARSAL_RETAINED_TREES.json. Production and independent-review holds remain unchanged; this migration evidence is not film or billing approval.

## Protected desk constraint and next checkpoint

Live PR180 still uses branch `hos-desk` at `e7cc01c9a9b6e3f3ea13367d8cefa65a00b78137`. Its rehearsal changes 322 of 4,120 files; its mapped head is `4679657236d458fd435e293deebf91485da5292e`. The standing rule and RETAINED_DISPOSITION.md explicitly say never close, merge or push this desk. That branch must therefore be excluded from any live push under present authority. Leaving it unchanged keeps affected history reachable; a blanket claim of zero public exposure would be false. Do not use git push --mirror.

Before a live window, resolve that specific protection through an explicitly authorized desk migration or exception; do not infer one from general cleanup approval. Prepare the exact allowlisted branch/tag operations and machine-refresh plan, announce the date the day before, hold all HOS writers, take an updated private backup and recheck refs/open PRs. Only the desk was open when checked this session; this evidence PR will itself need disposition. Rehearse again if refs change. The 657 GitHub pull refs and cached views require private GitHub Support follow-up; SUPPORT_REQUEST_DRAFT.md remains a draft, not sent as Ben. No window is announced here. OWB history still waits for its later separately scoped stage.

Private scratch: `/Volumes/MiniWork/scratch/j2537-rehearsal-20261118/`. Detached completion: `~/_desk/logs/j2537-rehearsal-20261118.done` is 0. The original backup directory remains separate. No history rewrite process is still running.

## Checks

Required check_all.sh: ALL CHECKS PASS. Main address report: 0 files. Full reachable-object scan, ref-set equality, commit preservation, main-tree equality, retained-input comparison and git fsck: passed. This report contains only counts, paths and hashes, never the removed addresses. No spend, generation, YouTube changes or shared-checkout edits.
