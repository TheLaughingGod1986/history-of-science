# J1200 — restore four playable J0966 review copies (29 Oct 2026)

Worker: cursor. GBP0. No upload, privacy, schedule or rebuild.

## Problem
Prior HOS UAT paths under film `10_Shorts/` for these four masters hit `OSError: [Errno 11] Resource deadlock avoided` (EDEADLK) on read — the J1121 delivery failure mode. Local checkout masters remained readable and SHA-matched.

## Delivery
New versioned folder (did not overwrite locked UAT paths):

`HOS UAT/J1200_J0966_review_2026-10-29/`

NAS mirror: `/Volumes/data/mac-mini-archive/YouTube/History Of Science/J1200_J0966_review_2026-10-29/`

| YouTube id | File | Master SHA256 (12) | PHONE SHA256 (12) | Decode 1.5s |
|---|---|---|---|---|
| `-I_GHK-GcFs` | `hos_007_s04_smallpox_test_v04` | `3ef3fa773750` | `17c916d2d586` | PASS |
| `x_3L_IdYgEc` | `hos_005_s03_never_saw_v04` | `e1f862ba737a` | `1cd37e5fbf2b` | PASS |
| `-sa2t7dAtCk` | `hos_004_s05_dalton_v04` | `8ce07a605697` | `ef760260e1da` | PASS |
| `4WUs0beKn0A` | `hos_007_s05_vacca_jesty_v05` | `e5ea76f012fb` | `066c6774add2` | PASS |

Hashes match `8df16983` / J1083 recorded manifests. Gates and Chief PASS from that delivery still attach to these exact versions. J0966 worker progress left at 5/5; job remains blocked awaiting Ben swap OK.

## Board cards
Four `jobs.py awaits J0966` entries set with PHONE paths in the new folder, air dates 13/15/16/17 Nov, due 10:30 London air day, if-not = originals air unchanged.

## Next
Elected Chief: verify hold/cards, then Ben swap OK per Short. HOS-007/J0925 OK is the long only — not these swaps. First pack cutoff 12 Nov 20:00Z.

## Play link verify (published board)

`board_check.py` ok (4/4). Each Ready-for-OK Play URL returned `video/mp4` from R2; full-file SHA matched the local PHONE; `ffmpeg -t 1` decode PASS. Not a 302-only check.
