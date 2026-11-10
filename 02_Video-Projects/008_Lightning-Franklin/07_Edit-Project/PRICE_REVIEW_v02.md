# J0184 — HOS 008 v02 price revision (14 Oct 2026)

Codex covering. Applies the Chief FIX of 12 Oct on PR #296. Draft for Chief's price review; no final OK, PASS, mint or spend.

112 timed rows: **15 proposed Quality hero/cover plates, 82 Fast, 15 reuse**. All 12 continuation holds are now reuse proposals; 42 original Quality rows move to the conditional Fast plan. Existing three callbacks remain. VO hashes, anchors, durations, spoken lines and references are unchanged. The v01 files remain for comparison. Run `_reprice_plate_boards_v02.py` to reproduce v02.

| Route | v01 try 1 | v02 try 1 | v01 expected | v02 expected |
|---|---:|---:|---:|---:|
| Flow | 6,850 cr | 2,320 cr | 17,476 cr | 5,525 cr |
| Vertex | £88.96 | £58.08 | £223.64 | £130.95 |

Expected Flow reduction: 68.4%; expected Vertex reduction: 41.4%. Prices reuse v01 list rates, 0.80 GBP/USD and HOS 005 takes-per-KEEP; these are planning estimates, not quotes or a live budget check. The 12 Oct balances are explicitly historical. No route selected; Flow/Vertex split waits for Ultra refill and a live credit reading.

## Checks and limits

Validated all 112 row IDs, VO anchors/text, durations and references against v01; every Quality row is in the explicit hero candidate list; every continuation is reuse; every reuse has zero new-mint price; row prices sum to each plan total. Generator completed without API calls.

**Fast price is conditional.** Downgraded v01 prompts are retained so the creative change is reviewable. Several contain candles, sparks or flickers. They are flagged and generation-disabled: the unchanged prompt must never run on Fast. Claude/Chief must agree eligible non-emissive framing or a compatible reviewed KEEP substitution before generation. Existing explanatory flat-card/diagram prompts also need own code-graphic treatment, and are flagged separately; video pricing there is conservative.

**Reuse is conditional.** Sources are planned clips, not measured KEEP media. Continuation rows specify no executable clip window: the original 8 s clip may not supply enough unused moving footage for both windows. Select a distinct matching KEEP cutaway where required, or reprice a longer source. Never loop, freeze-pad or replay frames. This proposal does not claim the reuse edit is feasible yet.

**Next:** Chief reviews the 15 hero candidates and price assumptions; creative review resolves flagged Fast prompts and reuse coverage; split routes only after refill and current credit. Parked for Chief: price pass. No Ben action requested.
