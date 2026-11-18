# J2537: second film-record carry, 18 November 2026

Codex acting Chief. Preserve 72 missing files from six owner-authored PRs on current main. Each is byte-identical to the named source head in FILM_RECORDS_CARRY_2.json. These are historical records, not new film approvals, a media review, or authorization to execute the restored per-film build scripts.

| PR | Records preserved | Main state retained |
|---|---|---|
| #509 | HOS 010 J2270 batch-one handoff | Obsolete PIPELINE, generated STATUS and kanban not restored |
| #511 | HOS 009 J2582 evidence and 20 still sheets | Current ignore policy |
| #514 | HOS 008 J2589 take receipts, accounting and hashes | Current production-status |
| #550 | HOS 011 J2563 preflight and timing records | Obsolete PIPELINE, generated STATUS and kanban not restored |
| #555 | HOS 008 Short C v03 recipe, builder and QA records | No existing main file overwritten |
| #556 | HOS 008 Short C v07 recipe, builder and QA records | Current production-status |

Original status additions remain in source branches; their substantive evidence is now preserved in the named per-job records. Historical FAILs, blocks, missing-media paths and proposed scopes remain historical: this carry neither clears gates nor rolls back later production decisions. No uploaded file or manifest is rewritten. No shared tooling, live status, WIP list or publishing state changes.

Validation: check_all.sh **ALL CHECKS PASS** (desk handoffs, email ratchet, no media, status board, audio checks, contract tests, package lint). All 72 source hashes verified; carried JSON parses; direct personal-address scan has zero matches. There are 20 existing JPEG review sheets and no video/audio files. Total source content is 9,321,944 bytes. Current owner authorship and exact source heads rechecked before carrying.

Close these six source PRs only after merge and verification, retaining their branches. Together with #643, this reduces the starting 17 ordinary PRs to eight: #624, #612, #579, #570, #561, #560, #551, #542. Preserve protected desk #180. Stage 2 remains incomplete; the rehearsal and planned rewrite window remain outstanding. No history rewrite occurred.
