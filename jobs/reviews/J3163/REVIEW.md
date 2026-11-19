# J3163 — PASS: independent review of repaired music routing types

19 November 2026.
- **Reviewer:** `gemini` (`Gemini 4 Argon (High)` via `agy`)
- **Implementer of reviewed commit:** `codex` (J3162; excluded from reviewing its own commit)
- **Target PR & branch:** HOS PR #675 (`macbook/J3154`)
- **Exact tested commit:** `faa8f75731a91d50b9ce999a4b80c4fa4562fce9`
- **Parent commit:** `c2dc9859c1c0242362fa7d611a7dc9de6dca5b12`
- **Prior review & ruling:** J3158 at PR #678 (`e93bf01ed9d371528b297a892ce841826393d57e`), HOS desk ruling `7018655830`

**Recommendation: PASS (advisory worker review of the offline repair).**
This review PASS covers the offline routing-type and one-read reservation repair at `faa8f75731a91d50b9ce999a4b80c4fa4562fce9` only. It is **not** activation, spend, or merge authority; elected-Chief disposition follows separately.

## 1. Scope and diff audit (`c2dc9859` → `faa8f757`)

1. **Production diff is strictly confined to `04_Audio/tools/el_client.py` (`_music_route`):**
   - Lines 31–32 now return `"reject"` instead of `"other"` whenever `type(path) is not str or type(query) is not str`.
   - Both public POST entry points (`el_client.request` on line 93 and `el_client.multipart_post` on line 135) call `_music_flight_query` before constructing a request URL, reading multipart files, calling `el_guard.before_spend`, or invoking `urllib.request.urlopen`.
   - Inside `_music_flight_query`, any route other than `"other"` or `"flight"` immediately raises `guard.GuardRefused("malformed_request")`.
   - Because the check uses exact `type(path) is not str or type(query) is not str`, any `str` subclass (such as `class ClientPath(str): pass`), `bytes`, `bytearray`, `None`, numeric, or container value passed as `path` or `query` is rejected with `malformed_request` before legacy dispatch.
2. **Flight, generator, reservation, and pinned guard files are unchanged from `c2dc9859`:**
   - `04_Audio/tools/hos009_score_flight.py`: SHA-256 `43e71321756bc56812264afd64b2946a8222f38c6bea6987376a83a8eafc922d` (unchanged from `c2dc9859`; `ACTIVATION_AUTHORIZED = False` literal on line 34).
   - `04_Audio/tools/generate_music_bed.py`: SHA-256 `a59f8496a8f285c830468d6dbb4333a9e2f1a12d5808fc6621341f62c62fc597` (unchanged).
   - `jobs/reviews/J3150/pinned/score_billing_guard.py`: SHA-256 `930d987783055d1f73e80fd9ae770f1ecde63d79b397706df74e9492b4029308` (unchanged).
   - `jobs/reviews/J3150/pinned/subscription_shape.json`: SHA-256 `ba290b64740c96c3407af17da80d043be3bf840d1863518bfb011e047f9e647e` (unchanged).
   - `04_Audio/tools/el_client.py`: SHA-256 `aabdc7502bf6edcedb735e32427a89046d9794c0cea6c90eabb8d793b9692bb5` (updated in `jobs/reviews/J3150/HASHES.txt` and `jobs/reviews/J3162/HASHES.txt`).
   - All 8 entries in `jobs/reviews/J3150/HASHES.txt` and all 12 entries in `jobs/reviews/J3162/HASHES.txt` verify via `shasum -a 256 -c`.

## 2. Offline test and probe verification (fixtures only, GBP 0)

All tests and probes were re-run offline against temporary fixture desks and synthetic tokens with `urllib.request.urlopen` mocked/patched. No live lock or store under `~/_desk` was read, cleared, reconciled, or modified, and zero network or account calls were made.

- **23 flight tests (`jobs/reviews/J3150/test_score_flight.py`):** 23 passed (`REGRESSION.txt`). Plain built-in string canonical `/v1/music` routes to the disabled flight (`activation_closed` when unpatched), non-canonical/fragment built-in strings refuse with `malformed_request`, and built-in string speech (`/v1/text-to-speech/voice`) and Scribe (`/v1/speech-to-text`) continue to route through `el_guard.before_spend`.
- **11 ElevenLabs guard tests (`04_Audio/tools/test_el_guard.py`):** 11 passed (`REGRESSION.txt`).
- **New routing type matrix tests (`jobs/reviews/J3162/test_routing_types.py`):** 2 test methods (34 subtests across `request` and `multipart_post` with `TTS_PAUSE` present, `EL_GUARD_OFF=1`, and `ACTIVATION_AUTHORIZED is False`) passed (`REGRESSION.txt`).
- **Original J3158 exploit probe (`jobs/reviews/J3162/probe_normalization.py`, byte-identical to `e93bf01e:jobs/reviews/J3158/probe_normalization.py`):** stops immediately on the first call (`request` with `ClientPath('/v1/music')`) with `GuardRefused: malformed_request` before any mocked transport call (`NORMALIZATION.txt`).
- **Verification variant (`jobs/reviews/J3162/verify_normalization.py`):** confirms all 6 cases from J3158 (`ClientPath('/v1/music')` and `ClientPath('/v1/music#fragment')` across `request` and `multipart_post`, plus canonical `'/v1/music'` with `query=ClientPath('')` and `query=None`) raise `GuardRefused("malformed_request")` with `transport=[]` (zero mocked POSTs, zero network calls) (`NORMALIZATION_VERIFIED.txt`).
- **Independent Gemini matrix probe (`jobs/reviews/J3163/probe_independent_matrix.py`):** exercised 32 path-type cases (`2 entries × 16 non-str paths`, including direct and derived `str` subclasses, `bytes`, `bytearray`, `None`, `int`, `bool`, `list`, `dict`, `Path`) and 52 query-type cases (`4 base paths × 13 non-str queries`) under `EL_GUARD_OFF=1` and a fixture `TTS_PAUSE`. All 84 cases raised `GuardRefused("malformed_request")` with `0` mocked transport calls, `0` legacy `before_spend` calls, and `0` store/reservation files written (`INDEPENDENT_MATRIX.txt`).
- **One-read reservation probe (`jobs/reviews/J3162/probe_reservation.py`, byte-identical to `e93bf01e:jobs/reviews/J3158/probe_reservation.py`):** all 3 scenarios (`failed_transport`, `untrusted_receipt`, `restart_before_transport`) pass offline; reservation file persists unchanged across fresh-interpreter restarts and refuses `read_reserved` with zero transport calls while the pinned single-use store remains absent (`RESERVATION.txt`).
- **Repository CI checks (`00_Brand/Channel-Setup/tools/check_all.sh` and `lint:package`):**
  - Durable desk handoffs (28 tests), email ratchet (8 tests), no-media, status board (33 status files + `BOARD.json`), ElevenLabs guard (11 tests), `vo_check` word tests (9 tests), `atempo` tests (9 tests), voice speed (`atempo <= 1.06`), and contract tests (28 vitest tests) all **PASS**.
  - `npm run lint:package -- --film 009` **PASSes**.
  - Full `package-lint` has only the unchanged baseline failure on `02_Video-Projects/008_Lightning-Franklin/11_Upload-Package/PACKAGE_MANIFEST.json` (`[schedule.past] schedule is in the past`).
  - `git diff --check` is clean.

## 3. Standing boundaries

- **GBP 0.** No account calls, pricing rescan, generation, activation, deployment, merge, music allowance, YouTube, or Buffer change.
- No live locks or stores under `~/_desk` were touched.
- `J3047` remains permanently closed unused; score `v01` and `v02` remain rejected; `J2035` and `J2171` remain held; film inputs, media, timing, and gates are preserved.
- PR #678 (`codex/J3158`) and this review PR remain review-only and unmerged.
- Elected-Chief disposition of PR #675 follows separately.
