# J2537: topic records carry, 18 November 2026

Codex acting Chief. Stage 2 remains in progress.

Preserve the final topic-review records for HOS 104–119 from 24 owner-authored PRs on fresh main 588b9c14. The 272 carried files are byte-identical to their source heads, recorded with SHA-256 in TOPIC_CARRY_2026-11-18.json. No existing main file is overwritten. Where proposal and review differ, keep the final reviewer version (including refreshed search evidence, corrected wording, scores and status summaries). The source branches remain available for the history inventory.

| Films | Proposal PR | Final review PRs |
|---|---|---|
| 104–105 | #581 | #582, #583 |
| 106–107 | #588 | #589, #591 |
| 108–109 | #602 | #604, #603 |
| 110–111 | #607 | #608, #609 |
| 112–113 | #614 | #617, #616 |
| 114–115 | #618 | #619, #620 |
| 116–117 | #625 | #627, #628 |
| 118–119 | #629 | #632, #631 |

These are existing reviewers' backlog decisions, not a fresh fact check or production authorization. Every carried status.json keeps all stages todo; the summaries explicitly require an available HOS WIP slot and the sources/facts lane. No film is added to active production or scheduled. The script files are template stubs, not locked narration. No shared code, active film, settings, gate or current WIP list is changed.

Close the 24 source PRs only after this carry passes checks and is merged. Preserve desk #180. The remaining 17 ordinary PRs require separate decisions within J2537, including the older 102–103 topic set and the explicitly review-only #561. Stage 3 rehearsal and the day-before rewrite notice remain outstanding. No history rewrite or public video action occurred.

## Validation and limits

- `check_all.sh`: **ALL CHECKS PASS** (email ratchet, no-media, status board, audio guards, contract tests and package lint).
- All 272 carried hashes match the recorded source; all carried JSON parses; direct address scan finds zero matches.
- All 16 status records retain every stage as todo.
- Historical review text sometimes names an obsolete WIP array or cap (for example HOS 104 mentions six slots). This carry preserves the original review evidence; current AGENTS.md and jobs/WIP.json govern admission, not those historical instructions. No new approval is inferred from the old scores or evidence.
