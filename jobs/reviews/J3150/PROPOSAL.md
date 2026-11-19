# J3150 — disabled music integration, activation closed

19 November 2026. Offline preparation for HOS 009. GBP 0. This wires the reviewed guard into the music entry points and leaves the socket switched off.

The guard file is the J3147 bytes at `11ed0c86d925dca5cbbbd1a2abef71326f1b6b7a`. Its sha256 is `930d987783055d1f73e80fd9ae770f1ecde63d79b397706df74e9492b4029308`. The shape file sha256 is `ba290b64740c96c3407af17da80d043be3bf840d1863518bfb011e047f9e647e`. This job does not edit those bytes and does not reopen findings A–D.

## What is closed

`el_client.request` and `el_client.multipart_post` send `POST /v1/music` through `hos009_score_flight`. They do not call `el_guard.before_spend`, so they do not open the nested subscription GET. `generate_music_bed.compose` calls the same flight and no longer calls the client. A speech or Scribe request still uses the existing guard.

The production functions `from_generator`, `from_client` and `from_multipart` reject a caller transport, fetch, desk or path. The subscription read is `_subscription_get`, which asks `_read_one_response` for one status, one Date and one raw body. A passing decide may then make one POST through that same function. A refusal does not POST. A second call finds the single-use file and does not GET again.

`ACTIVATION_AUTHORIZED` is the literal `False`. The socket function returns before `urlopen` while that constant is false. It is not an environment switch. The flight does not bind a desk, and the pinned guard still refuses the live desk, so a fixture desk cannot be aimed at the account from the entry point.

The flight holds the `O_EXCL` recorder descriptor from before decide until after the mocked POST. It does not close or replace that descriptor. A second process cannot create the lock. A new process sees the burned single-use file. A future Date refuses and leaves the file in place. `EL_GUARD_OFF` is not read. Pause, ledger and promo checks are the pinned guard's checks.

## What is not authorized

No score, no allowance, no account call, no deploy. J3047 stays closed. Score v01 and v02 stay rejected. The long assembly and the Shorts stay held. `PRICING_EVIDENCE.md` records why a 3,000-credit and GBP 0 bound is not established, and the no-spend route.

## Review

```bash
python3 jobs/reviews/J3150/test_score_flight.py
python3 04_Audio/tools/test_el_guard.py
```

The independent reviewer is not the author of this integration. A pass of these tests is not permission to generate.
