# J3171: non-spend paths are GET-only, and a GET cannot carry a body

19 November 2026. Implements the nonblocking follow-up in owner-authored HOS Chief ruling 7022847995, confirmed in 7022947212 and reconciled by J3169. Branched off `origin/main` at `f13cb7aed8a596806bb7fab527b0cb9e643c362b` (PR 680 exact head `7b87f15ebf6b1a74e7c1eb5df1c5b26fa9e74321`). Worker submission only: not a Chief ruling, not a PASS, no merge.

## Production change

`04_Audio/tools/el_client.py` only. `el_guard.py` is unchanged.

1. `/v1/user/subscription` and `/v1/history` are GET-only. `request()` and `multipart_post()` raise `GuardRefused("malformed_request")` for every other method (`PATCH`, `PUT`, `POST`, `DELETE`, `HEAD`, `OPTIONS`, and the same tokens in another case) before `from_client`, before `el_guard.before_spend`, and before `urllib.request.urlopen`.
2. A GET with a body (`data is not None`, including `{}`) raises the same `malformed_request` on every path, before the guard and the socket.
3. A bodyless GET of subscription or history still proceeds. `POST` speech and Scribe still go through `el_guard`. Canonical `POST /v1/music` still reaches only the disabled flight.

Prefix match is the same `startswith` the subscription allow-list already uses, so `/v1/user/subscription…` and `/v1/history…` are included. Unsafe paths stay on the existing reject path.

## Behaviour the tests lock

| Call | Result | `urlopen` |
|---|---|---|
| `GET` or `get` `/v1/user/subscription` or `/v1/history`, no body | Sent (mocked) | Yes, in the fixture |
| `GET` or `get` with `{}` or `{"text":"Hi"}` on subscription, history, `/v1/music`, speech, Scribe, or sound-generation | `malformed_request` | No |
| `PATCH` `PUT` `POST` `DELETE` `HEAD` `OPTIONS` (any listed case) on subscription or history, with or without a body | `malformed_request` | No |
| `multipart_post` on those paths | `malformed_request` | No |
| `POST /v1/text-to-speech/voice` with the guard off | Sent (mocked) | Yes |
| `POST /v1/text-to-speech/voice` while the pause file exists | `SpendRefused` | No |
| canonical `POST /v1/music` | `activation_closed` | No |

`before_spend`, `from_client` and `from_multipart` are not called on the refused rows.

## Offline results (fixture desks only, GBP 0)

- `python3 jobs/reviews/J3171/test_nonspend_get_only.py -v`: 4 test groups passed
- `python3 jobs/reviews/J3150/test_score_flight.py -v`: 23 passed
- `python3 04_Audio/tools/test_el_guard.py -v`: 11 passed
- `python3 jobs/reviews/J3162/test_routing_types.py -v`: 5 passed
- `python3 jobs/reviews/J3166/test_path_method_hardening.py -v`: 4 test groups passed
- `00_Brand/Channel-Setup/tools/check_all.sh`: every check passed except package-lint, whose only failure is the pre-existing HOS 008 line `FAIL [schedule.past] schedule is in the past` on `02_Video-Projects/008_Lightning-Franklin/11_Upload-Package/PACKAGE_MANIFEST.json`. Film 009's manifest in that same run is `PASS`.
- `npx tsx scripts/package-lint.ts --film 009`: exit 0. The manifest also prints the existing `warn [captions] no captionsFile`.

## Hashes (SHA-256)

- `04_Audio/tools/el_client.py`: `c12f6245e1deaf5fbdc4400ac31826d07563dfb9edb0a5ea1350ed80cf4bdafb` (was `3dbd09bad04ebbe36d2881c2f128ee33c7870a81905e204cced48f3366f7bbb4` at `7b87f15e`)
- `jobs/reviews/J3171/test_nonspend_get_only.py`: `323b362cd9a97fd3041f622b51c01d08fbd7fd899ede5973200edd0740bc7995`
- `jobs/reviews/J3150/HASHES.txt`: `38e2c10dd20bed275be2c17d6338ca861631ebe121380c7cb2bf8e4b7f701aef` (el_client line only; was `6a5109be48aa3fb4294ff56936ed9ea82d6fa8be245cc66c806d662fa07f5561` at `7b87f15e`)
- Unchanged `04_Audio/tools/el_guard.py`: `c1a4e32bd4fe2dd9a70d1302277f30f8bfdfb5b89e6904dbfe0fe9105af8b9c4`
- Unchanged `04_Audio/tools/hos009_score_flight.py`: `43e71321756bc56812264afd64b2946a8222f38c6bea6987376a83a8eafc922d` (`ACTIVATION_AUTHORIZED = False`)
- Unchanged `04_Audio/tools/generate_music_bed.py`: `a59f8496a8f285c830468d6dbb4333a9e2f1a12d5808fc6621341f62c62fc597`
- Unchanged pinned guard: `930d987783055d1f73e80fd9ae770f1ecde63d79b397706df74e9492b4029308`
- Unchanged pinned shape: `ba290b64740c96c3407af17da80d043be3bf840d1863518bfb011e047f9e647e`
- Unchanged `jobs/reviews/J3150/test_score_flight.py`: `2724d832e3ecffb90f8c0b96349c7f452e9e7928b72ac078e5f570bbf8e45c49`
- Unchanged `jobs/reviews/J3162/test_routing_types.py`: `e7cd8d411bc4b0cca294c130714e4c2760a927b0b02b05cb20a9c33c1402119e`
- Unchanged `jobs/reviews/J3166/test_path_method_hardening.py`: `9e767925e8684697f08ccbb56c0da8ee19e0e0b7c86edc8ef6cbc2a51e2f11e0`
- `jobs/reviews/J3166/HASHES.txt` and `HARDENING_EVIDENCE.md` stay the snapshot of `7b87f15e`.

## Guardrails unchanged

GBP 0. No account call, pricing rescan, generation, activation, deployment, merge, allowance, YouTube or Buffer change, or live lock or store edit. `ACTIVATION_AUTHORIZED` stays literal False. PR 678 and PR 679 stay review-only and unmerged. J3047 stays closed and unused. v01 and v02 stay rejected. J2035 and J2171 stay held. Film, media, timing and gates are unchanged. No replacement delivery promise. J3170 was not touched.
