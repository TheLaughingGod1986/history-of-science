# J3166: offline music path and method hardening

19 November 2026. Implements only the nonblocking follow-up from owner-authored HOS Chief ruling 7022139984, branched off `origin/main` after PR 675 (`d1f9e54549cef037c6551ec26b2990622a8742c3`, merged at `327c220d306632f79e6d7d9c15b6618415df9601`). Worker submission only: not a Chief ruling, not a PASS, no merge.

## Production changes

1. **`04_Audio/tools/el_guard.py`**
   - Added `";"` to `path_is_unsafe(path)`: `/v1/text-to-speech/..;/music` (and any path containing `;`) returns `True`, so `_music_route` returns `"reject"` and `is_spend` fails closed (`True`) for non-GET requests.
   - Updated `is_spend(method, path)`: normalizes built-in `str` methods via `strip().upper()`, fails closed (`True`) on non-built-in `str` methods or methods containing whitespace/control characters (including `" POST"`, `"POST "`, `"\tPOST"`, `" GET"`, `""`), returns `False` only for clean `GET`, and evaluates all other methods (`POST`, `PUT`, `PATCH`, `DELETE`, `HEAD`, `OPTIONS`, etc.) against `path_is_unsafe` and `SPEND_PREFIXES`.
2. **`04_Audio/tools/el_client.py`**
   - Added `_normalize_method(method)` using `strip().upper()` and validating built-in `str` with no whitespace or control characters.
   - In `request()`:
     - Any invalid/padded/non-`str` method (`" POST"`, `"POST "`, `"\tPOST"`, `" post"`, `" GET"`, `""`, `None`, `bytes`, `str` subclass) raises `guard.GuardRefused("malformed_request")` before `from_client`, before `el_guard.before_spend`, and before `urllib.request.urlopen` (zero transport).
     - Normalized `"POST"` continues through `_music_flight_query(path, query)`: canonical `/v1/music` (empty query or `output_format=mp3_44100_128`) stays on the disabled guarded flight (`hos009_score_flight.from_client`); rejected paths including `/v1/text-to-speech/..;/music` and `/v1/sound-generation` raise `malformed_request` with zero transport; clean allowlisted speech/Scribe/subscription paths continue to `el_guard`.
     - Any clean method other than `"GET"` and `"POST"` (`PUT`, `PATCH`, `DELETE`, `HEAD`, `OPTIONS`, etc.) checks `_music_route(path, query)`: if `!= "other"` (including canonical `/v1/music` and any obfuscated, music-shaped, or non-allowlisted path), raises `guard.GuardRefused("malformed_request")` before `from_client`, before `el_guard.before_spend`, and before `urllib.request.urlopen` (zero transport).
     - Passes normalized `norm_method` to `el_guard.is_spend` and `urllib.request.Request`.

## Exact behavior matrix (for independent reviewer and Chief)

| Method | Path | `el_client.request(...)` | `from_client` | `before_spend` | `urlopen` | `el_guard.is_spend` |
|---|---|---|---|---|---|---|
| `"POST"` | `"/v1/music"` (`""` or canonical query) | Disabled guarded flight -> `GuardRefused("activation_closed")` | Yes (disabled) | No | No | `True` |
| `"post"` | `"/v1/music"` (`""` or canonical query) | Normalized via `strip().upper()` to `"POST"` -> disabled guarded flight -> `GuardRefused("activation_closed")` | Yes (disabled) | No | No | `True` |
| `" POST"`, `"POST "`, `"\tPOST"`, `"POST\n"`, `" post"`, `"PO ST"` | `"/v1/music"` or any path | `GuardRefused("malformed_request")` | No | No | No | `True` |
| `"PUT"`, `"PATCH"`, `"DELETE"`, `"HEAD"`, `"OPTIONS"` (any case) | `"/v1/music"` (any query), `"/V1/MUSIC"`, `"/v1/music/extra"`, `"/v1/text-to-speech/..;/music"` | `GuardRefused("malformed_request")` | No | No | No | `True` |
| `"GET"`, `"get"` | `"/v1/user/subscription"` | Normal GET (`method="GET"`) | No | No | Mocked in tests | `False` |
| `"GET"` | `"/v1/music"` | Not refused (per ruling: *"refuse any method other than GET on a music-shaped path"*) | No | No | Mocked in tests | `False` |
| `" GET"`, `"GET "` | `"/v1/music"` or any path | `GuardRefused("malformed_request")` | No | No | No | `True` |
| `""`, `"   "`, `None`, `b"POST"`, `str` subclass | `"/v1/music"` or any path | `GuardRefused("malformed_request")` | No | No | No | `True` |
| `"POST"` (or `multipart_post`) | `"/v1/text-to-speech/..;/music"`, `"/v1/music;param"` | `GuardRefused("malformed_request")` | No | No | No | `True` |
| `"POST"` (or `multipart_post`) | `"/v1/text-to-speech/voice"`, `"/v1/speech-to-text"` | Unchanged legacy `el_guard` path | No | Yes | Mocked in tests | `True` |
| `"POST"` (or `multipart_post`) | `"/v1/sound-generation"` | `GuardRefused("malformed_request")` (accepted PR 675 behavior) | No | No | No | `True` |

### Ambiguities recorded explicitly for reviewer/Chief

1. **Lowercase clean `"post"` on `/v1/music`:** Ruling 7022139984 specifies both normalizing the method with `strip().upper()` and preserving canonical `POST /v1/music` on the disabled guarded flight while rejecting spaced `" POST"` before flight/guard/transport. This implementation routes clean `"POST"` and `"post"` (no whitespace) to the disabled guarded flight (`activation_closed`, zero transport), and rejects any whitespace-padded variant (`" POST"`, `"POST "`, `" post"`, `"\tPOST"`) as `malformed_request` before `from_client`, `before_spend`, and `urlopen`. If the reviewer/Chief prefers rejecting lowercase `"post"` on `/v1/music` as `malformed_request` too, that is a one-line tightening (`method != "POST"` on flight).
2. **Clean `"GET"` on `/v1/music`:** Ruling 7022139984 states *"refuse any method other than GET on a music-shaped path"*, matching existing `el_guard.is_spend("GET", ...)` tests (`False`). Accordingly, clean `"GET"` on `/v1/music` is not refused here (while spaced `" GET"` is refused as `malformed_request`). No repo caller issues `GET /v1/music`; if the reviewer/Chief also wants `GET` on `/v1/music` or unsafe paths refused in `el_client.request`, that can be decided on review.

## Offline test results (fixture desks only, zero network, GBP 0)

- `python3 jobs/reviews/J3150/test_score_flight.py -v`: **23 passed** (OK)
- `python3 04_Audio/tools/test_el_guard.py -v`: **11 passed** (OK)
- `python3 jobs/reviews/J3162/test_routing_types.py -v`: **5 passed** (OK)
- `python3 jobs/reviews/J3166/test_path_method_hardening.py -v`: **4 test groups passed** (OK)
- `00_Brand/Channel-Setup/tools/check_all.sh`:
  - `durable desk handoffs`: PASS (28 tests)
  - `email ratchet`: PASS (8 tests)
  - `no media`: PASS
  - `status board in sync`: PASS (33 status files and BOARD.json)
  - `ElevenLabs guard tests`: PASS (11 tests)
  - `vo_check word tests`: PASS (9 tests)
  - `atempo check tests`: PASS (9 tests)
  - `voice speed (atempo <= 1.06)`: PASS
  - `contract tests`: PASS (28 tests)
  - `package-lint`: FAIL solely on pre-existing unchanged HOS 008 baseline (`02_Video-Projects/008_Lightning-Franklin/11_Upload-Package/PACKAGE_MANIFEST.json`: `FAIL [schedule.past] schedule is in the past`).
  - `npx tsx scripts/package-lint.ts --film 009`: **PASS** (exit 0).

## Hashes (SHA-256)

- Modified `04_Audio/tools/el_client.py`: `3dbd09bad04ebbe36d2881c2f128ee33c7870a81905e204cced48f3366f7bbb4` (was `98c861e0bdbd6ea87d6c5b7861cd930db60c172dfa5b3edae9d450a1ca6aadc0` at `d1f9e545`)
- Modified `04_Audio/tools/el_guard.py`: `c1a4e32bd4fe2dd9a70d1302277f30f8bfdfb5b89e6904dbfe0fe9105af8b9c4` (was `2465a18393efeacfe80f25fffe97095be7fcee3270df6a82e79f538df72450e1` at `d1f9e545`)
- Modified `04_Audio/tools/test_el_guard.py`: `6ed2501f07fef2e0b617baef87d803bae4f5b290a5d73b3451105a0131580b98`
- Added `jobs/reviews/J3166/test_path_method_hardening.py`: `9e767925e8684697f08ccbb56c0da8ee19e0e0b7c86edc8ef6cbc2a51e2f11e0`
- Unchanged `04_Audio/tools/hos009_score_flight.py`: `43e71321756bc56812264afd64b2946a8222f38c6bea6987376a83a8eafc922d` (`ACTIVATION_AUTHORIZED = False`, durable reservation unchanged)
- Unchanged `04_Audio/tools/generate_music_bed.py`: `a59f8496a8f285c830468d6dbb4333a9e2f1a12d5808fc6621341f62c62fc597`
- Unchanged `jobs/reviews/J3150/pinned/score_billing_guard.py`: `930d987783055d1f73e80fd9ae770f1ecde63d79b397706df74e9492b4029308`
- Unchanged `jobs/reviews/J3150/pinned/subscription_shape.json`: `ba290b64740c96c3407af17da80d043be3bf840d1863518bfb011e047f9e647e`
- Unchanged `jobs/reviews/J3150/test_score_flight.py`: `2724d832e3ecffb90f8c0b96349c7f452e9e7928b72ac078e5f570bbf8e45c49`
- Unchanged `jobs/reviews/J3162/test_routing_types.py`: `e7cd8d411bc4b0cca294c130714e4c2760a927b0b02b05cb20a9c33c1402119e`

## Guardrails unchanged

- GBP 0: no account call, no pricing rescan, no generation, no activation, no deployment, no merge, no allowance, no YouTube/Buffer changes, no live lock/store changes.
- `ACTIVATION_AUTHORIZED = False` literal preserved; durable reservation and pinned guard/shape safeguards preserved.
- PR 678 / PR 679 remain review-only unmerged; J3047 closed unused; v01/v02 rejected; J2035/J2171 held; film/media/timing/gates unchanged; no replacement delivery promise.
