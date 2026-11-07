# J2190 — six-shot Vertex no-spend preflight

Preparation only. **GBP0 spent; generation is not authorised.** This isolated offline tool does not import a Google SDK, obtain credentials, submit, poll, download or write media. Existing minters, boards and production logs are untouched. A dry-run is the selected deliverable, not an executable billable caller; the unverified price/liability evidence prevents safely implementing a live entry point under this scope.

```
python3 jobs/reviews/J2190/preflight.py --briefs jobs/reviews/J2190/SIX_INPUT_BRIEFS.json --version v01
python3 -m unittest discover -s jobs/reviews/J2190 -p 'test_*.py' -v
```

Add `--evidence <json> --ledger <global-ai-spend-jsonl>` to run the budget guard. Missing evidence blocks. Tests use explicitly fictional pricing/linkage/settlement fixtures, never actual spending authority. `--output-root <film>` rejects existing planned version files. `--require-lock` verifies the canonical live owned `~/_desk/locks/vertex.lock` from the existing desk-lock wrapper. Offline planning need not hold a spending lock.

The manifest contains six distinct text-to-video inputs and two proposed takes each (12 requests, no automatic retries). Each fixes HOS project/us-central1/Quality/1080p/9:16/8s/silent/one output. It carries full request+SHA256, per-input take identity, fresh version path, and explicitly null operation/output hash. Null fields are not evidence of an output. References remain style-only and are not attached as start frames. C S06 is the water jar entering daytime shade; C S07 returns it to sun. C S01 preserves source 0–1s preroll and contiguous 1–3.56s opening. Exact locked VO/timing is unchanged.

The guard requires fresh (<=5 min) credits, exact GBP/second Quality SKU, billing linkage and authoritative all-project usage evidence. Only Available eligible GBP promo rows count; a live monthly row is mandatory. It subtracts global logged spend after a **proved** settlement cutoff, all outstanding reserve/started events, per-row upper bounds for unknown/zero costs, and an unlogged usage upper bound. Missing bounds stop; time elapsed does not settle usage. It budgets all 12 proposed takes at the supplied cap and retains GBP5. Any prior J2190 request/reservation stops replay rather than silently allowing a new batch. A later producer must implement atomic global reservation under desk-lock, durable operation recording before any resume, and output hashing after generation; this dry-run is intentionally not that producer.

## Validation

`TESTS.txt`: 19 tests PASS, including unknown/stale/future credit evidence, wrong price/unit/model, unpriced historic spend, pending events, global other-film cost, explicit unknown bound, cap/floor, take/replay limit, absent lock, exact requests and socket/write-denied dry-run. `REPO_CHECKS.txt`: ALL CHECKS PASS. These validate the offline preflight, not generation or source KEEP. No image/audio/moving-video review is claimed.

J2191 is the already queued elected-Chief code/scope review after this job; it must rule on exact blockers and a concrete route decision. J2169 remains blocked 1/3. Preserve B 0f109926 / C 5b5d84e5, J1004, exclusions/S7 planned-only collision, all long/live stages, rendered gates and Ben's final watch. No awaits and no generic timed retry added.
