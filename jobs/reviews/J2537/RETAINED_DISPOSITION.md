# J2537: migration disposition of retained review PRs

18 November 2026, Codex, elected acting HOS Chief. This decision supersedes only the **keep open** portions of the earlier rulings below, for the repository migration. It authorizes closing these three PRs unmerged after this record is merged. It does not authorize merging their contents, deleting their branches, changing production pins, accepting pictures or integrating billing code.

| PR | Earlier ruling | Migration disposition |
|---|---|---|
| [551](https://github.com/TheLaughingGod1986/history-of-science/pull/551) | desk6808560760; J2652 awaits independent review of ad52a2dc | Close unmerged; retain codex/J2498-timing-rough and exact source tree. Pending review remains pending and can use the closed PR's Files tab and existing branch URLs. |
| [561](https://github.com/TheLaughingGod1986/history-of-science/pull/561) | desk6822483718; review-only sheets, never merge | Close unmerged; retain review/013-pass1-sheets. All images, index hashes and branch URLs stay available; no KEEP ruling is inferred. |
| [651](https://github.com/TheLaughingGod1986/history-of-science/pull/651) | J3059 comment6984410397: exact d047b064 offline only | Close unmerged; retain codex/J3050-billing-proposal. Offline acceptance and every production hold remain unchanged. Future integration requires its own scoped PR and independent review. |

The three RETAINED_PR_*_TREE.json records pin each full source tree by Git tree OID and SHA-256 of its complete NUL-delimited git ls-tree inventory. They also record each added/modified file in the PR's merge-base diff with its Git blob OID and SHA-256. Deleted paths remain recoverable from the recorded diff base and head. This is a preservation inventory, not a copy of these unreviewed files onto main.

Closing a PR does not delete its source branch or prevent a reviewer opening its files/comments. These heads and branch names must be checked immediately before closure; if any changed, refresh the inventory first. Never close, merge or push the protected desk PR180.

## Rehearsal and cutover prerequisites

Stage 2 is complete only after this record merges and the ordinary open-PR list is empty. Recheck the list at the actual cutover, since new work may arrive. Stage 3 must capture all old refs, including these three source branches, in the full NAS bundle and verify that bundle before rewriting any mirror. Keep the bundle private, never push it, never delete it. Record bundle checksum and ref inventory in the rehearsal evidence.

The eventual rewrite must preserve branch names and produce an old-to-new commit map. Compare every non-address-bearing blob on these retained heads byte for byte; enumerate every altered blob, including any changed hash-pinned input. If a changed blob is still an active production input, resolve and re-pin with its owning job before cutover, never silently. Until then the production branches and all existing pins remain untouched. Review URLs referring to a branch keep the same branch name; commit-specific URLs need the recorded old-to-new mapping after cutover. Old PR/cached commit visibility needs GitHub Support; closure alone does not remove it.

No history is rewritten by this record. A successful rehearsal, day-before notice to Ben, HOS writer hold, verified NAS backup and machine refresh/checks remain mandatory for the live window. OWB history waits for the later separately scoped stage after the studio move. No money, generation, film approval or YouTube change.

## Validation

All three complete tree inventories and all 200 changed-file SHA-256 values match their recorded source commits. Required `check_all.sh`: **ALL CHECKS PASS**. `git diff --check`: clean. No personal addresses were copied into these records.
