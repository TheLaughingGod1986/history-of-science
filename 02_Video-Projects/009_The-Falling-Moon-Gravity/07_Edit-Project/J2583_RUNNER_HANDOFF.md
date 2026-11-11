# J2583 retake runner for Chief review

No generation or credit spend in this change. J2585's completion record requires a separate runner PR before execution; this is that PR. The approved prompts from merged HOS #512 are unchanged.

The existing submit command gains `--retakes-j2583`. It selects only P03:01_really_falling_c1, P02:08_the_apple_c1, P04:05_minute_second_c1, in that order. Each must have exactly one verified original take and an unused take-2 path. Any take-2 intent, refusal, failure or output prevents another automatic run: partial-run recovery goes to Chief. The fourth shot (c2) cannot run through this option and still waits for the c1 sheet review.

Both the original twenty-row scope and the retake scope board hashes are checked. The existing shared writer/accounting lock, canonical spend export, live account/balance/exact 100-credit Quality x1 price checks before every Create, original 6,000 cap, 3,000 floor and remaining-cap reservation remain in force. Three rows at 100 credits limits this run to 300 subscription credits. No prompt edits, new stills requested by this change, KEEP decisions or publishing actions.

After Chief reviews and merges: use the existing canonical J2033 ledger/media/archive/lock paths and the existing explicitly armed `submit` command, adding `--retakes-j2583`. Run detached with a fresh log and done path; do not run alongside another writer. Read prior runner state before launch. Preserve any unresolved intent for reconciliation. Produce full-clip half-second sheets for J2584 after generation; c2 remains J2586/J2587 work.

Validation: the tranche-2 runner unittest suite, including retake selection, unrelated/c2 rejection, retry/refusal blocking, immutable take-2 files, changed cap/hash and missing verified original checks. No browser Create was called.
