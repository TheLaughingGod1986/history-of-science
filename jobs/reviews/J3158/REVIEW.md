# J3158 — FIX: repaired disabled music integration

19 November 2026. Independent worker review by Codex. HOS PR #675,
commit `c2dc9859c1c0242362fa7d611a7dc9de6dca5b12`, against integration
parent `f21ab5b9a4f0a2143fb4cb91b1c82822185b1783`.

**Recommendation: FIX.** The one-read reservation repair holds in the reviewed
failure/restart cases. The routing repair still permits music to reach the
legacy transport for a `str` subclass. This is advisory, not a Chief ruling.

## Exact fix list

1. In `04_Audio/tools/el_client.py`, `_music_route` (lines 29–30) must not return `other`
   merely because `type(path) is not str` or `type(query) is not str`.
   Fail closed for unsupported types before legacy dispatch, or safely handle
   string subclasses and apply the same canonical/fragment checks. Both public
   client entry points must share the rejection. Do not weaken the literal
   false activation switch or the speech/Scribe guard.
2. Add transport-spy regression cases for string-subclass paths (canonical
   `/v1/music` and `/v1/music#fragment`) through both `request` and
   `multipart_post`, plus an unsupported/subclass query through `request`.
   With activation false, a fixture TTS_PAUSE, and EL_GUARD_OFF=1, expect zero
   music POSTs and no fallback to the legacy spend path. Keep the existing
   plain-string fragment/query checks and speech/Scribe controls.

## Routing evidence

`probe_normalization.py` defines an ordinary `class ClientPath(str): pass`.
Both `ClientPath('/v1/music')` and `ClientPath('/v1/music#fragment')` classify as
`other`. Each public client entry reaches the mocked `urllib.request.urlopen`
with method POST and selector `/v1/music`. Four music POSTs are observed for the subclass paths; another two occur with a
built-in canonical path and either an empty string-subclass query or None.
Six mocked POSTs are observed in total;
`ROUTING_REPRO.txt` records them. The fragment is removed by Request after the
classifier has already sent the call to the legacy path.

This is a local API safety-boundary failure, not a claim of a remote exploit or
an actual account request. A string subclass satisfies the annotated string
interface; the exact-type rejection currently routes it around the safety
boundary instead of refusing it. All credentials are fixture literals and the
transport is patched. The source activation constant remains False throughout.

The supplied plain-string fragment and noncanonical cases do refuse before
transport. Canonical built-in strings use the disabled flight. Supplied controls
confirm speech/Scribe retain their legacy guard; compose retains the flight.
`generate_music_bed.py` and `el_guard.py` have no diff against the integration
parent. No production code was changed in this review.

## Reservation evidence

`_reserve_one_read` verifies the held descriptor, creates the reservation with
O_EXCL, writes and fsyncs it, fsyncs its directory, and verifies the same holder
again before `read_subscription` is reached. There is no deletion on failure.

Independent `probe_reservation.py` checks the reservation exists and its recorder
inode matches the open descriptor inside the mocked GET. It then releases the
test holder and starts a fresh interpreter on the same fixture directory:

- Failed transport: one mocked GET, zero POST; restart refuses `read_reserved`
  before transport; reservation bytes unchanged.
- Untrusted receipt: one mocked GET, zero POST; restart refuses `read_reserved`
  before transport; reservation bytes unchanged.
- Reservation followed by restart before transport: zero GET and zero POST;
  restart refuses `read_reserved`; reservation bytes unchanged.

The pinned decide/consume store remains absent in these pre-decision cases;
reservation and pinned store use different filenames. Supplied success and
post-decision refusal tests exercise the pinned store alongside the reservation.
Neither live file was read, cleared, reconciled, or changed. Only temporary
fixture directories were used. No additional fix is requested for repair 2.

## Verification and limits

- Supplied flight suite: 23 tests passed.
- Existing ElevenLabs guard suite: 11 tests passed.
- All eight entries in J3150/HASHES.txt match.
- Pinned guard SHA-256:
  `930d987783055d1f73e80fd9ae770f1ecde63d79b397706df74e9492b4029308`.
- Pinned shape SHA-256:
  `ba290b64740c96c3407af17da80d043be3bf840d1863518bfb011e047f9e647e`.
- ACTIVATION_AUTHORIZED remains the literal False. The supplied socket-binding
  unit test temporarily flips it only in its process with urlopen mocked; no
  source activation or real transport occurs.

Passing these tests does not prove a 3,000 subscription-credit and GBP 0 bound.
No score, merge, account call, activation, deployment, or spend is authorized.
GBP 0. J3047 stays closed. Score v01 and v02 stay rejected. Long assembly and
Shorts stay held. The elected-Chief follow-up owns disposition and repair work.

The required repository check_all.sh was run. All checks except package-lint
passed (including 28 contract tests). Package-lint fails on the unchanged HOS
008 manifest because its schedule is in the past. HOS 009 package lint passes.
This unrelated schedule record was not modified. git diff --check is clean.
