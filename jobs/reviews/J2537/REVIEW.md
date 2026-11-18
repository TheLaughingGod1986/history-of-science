# J2537: current files verified; first HOS PR carry

18 November 2026, Codex acting Chief. Stage 2 remains in progress.

Both repos passed their eight email-ratchet tests. HOS main includes PR #639
(9515d89b); both allowlists are empty. The shared HOS checkout is on a worker
branch, so this work uses a separate worktree based on origin/main 98c86667.
No shared worker files or film stage states were changed.

## What this carry preserves

- #521: all four J2598 historical receipt/runner files. CREATE.json replaces one
  account address with `the studio Ultra account`. The other three files are
  byte-identical to that PR. This preserves evidence, not permission to run it.
  J2598 is done; no picture generation or receipt-pinned media was changed.
- #573: the 13 November listing audit, unchanged from its PR.
- #592: the 14 November listing-audit update, unchanged from its PR.
- #484 is superseded: main already removed the tracked settings file and added
  its example in 49ea23f0 (#536, J2637). The PR need not restore its old example.

Close #521, #573 and #592 only after this carry is merged. Keep their branches.
Close #484 as superseded; do not change the local settings file on any machine.

## Open-PR inventory

OPEN_PR_AUDIT.json records 58 exact open PR heads, their merge-base changed paths,
paths differing from main, and personal-domain address-bearing paths (no values).
All heads belong to the owner's repository. Every head still contains old
addresses, including the protected desk #180. Only #521 touches an address-bearing
file in its proposed changes. This distinction matters: an old address elsewhere
on a branch does not prove that a normal merge would restore that address.
The audit is not a merge simulation and does not certify merges or historical
commits clean. The protected desk must never be closed or merged.

J2979 completed the OWB sweep, not the HOS sweep. The remaining HOS topic,
production and system changes still require review/carry or a supported
superseded decision. No blanket closure or merger is justified by this scan.

## Next steps on this same job

1. Finish resolving the remaining HOS PRs against fresh main, preserving useful
   changes. Apply the current zero-address ratchet to each merged result. Keep
   #180 open and account for its branch in the rehearsal.
2. Only then clone a fresh mirror, inventory every branch/tag, preserve a full
   pre-rewrite bundle on the mounted NAS with matching SHA-256, and rehearse the
   approved replacements. Do not push the mirror. Verify every reachable blob,
   every branch/tag, rewritten commit counts, and exact main tree equality.
   Separately inventory author/committer/tag metadata and commit messages; the
   current-file ratchet does not inspect these. Record any scope decision before
   claiming zero addresses throughout history.
3. Publish a concrete window notice at least the day before. At the window,
   hold HOS writers, revalidate refs, perform the approved rewrite, refresh every
   machine/session, run checks, and lift the hold. No window has been announced
   by this report; there is no authorization to run that step early.
4. Complete the support draft with actual old/new IDs after the rewrite. Old PR
   references and caches may remain reachable until GitHub addresses them.
   OWB history remains a later stage after the studio move and a clean HOS run.

No history rewrite, NAS deletion, YouTube action, spend, or new film approval.

## Validation

- Both repos: email ratchet, 8 tests each, OK; HOS allowlist empty.
- After staging the carry: `check_all.sh`: ALL CHECKS PASS (including the
  ratchet, no-media, board, audio guard tests, contract and package lint).
- All staged files scanned directly for personal-domain addresses: zero.
- Five carried files compared byte-for-byte with source PR heads: identical;
  CREATE.json differs only by one role-label replacement.
- The initial dependency check failed on an inaccessible npm cache in the fresh
  worktree. Reused installed dependencies with a worktree-local link and a
  scratch npm cache; the full check suite then passed. No dependency changes.
