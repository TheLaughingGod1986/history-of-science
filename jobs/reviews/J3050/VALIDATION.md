# Validation — J3050

18 November 2026, isolated worktree from origin/main f60a3f65.

- Synthetic normalizer tests: 8 tests, OK (all refusal matrices passed).
- Required repository check_all.sh: ALL CHECKS PASS.
- Durable desk handoffs: PASS (24 tests).
- Email ratchet: PASS (8 tests).
- No media: PASS.
- Status board in sync: PASS.
- ElevenLabs guard tests: PASS (11 tests).
- VO word tests: PASS (9 tests).
- atempo tests: PASS (9 tests); voice speed: PASS.
- Contract tests: PASS; package-lint: PASS.
- git diff --check: clean.

The first check attempt could not write the restricted default npm cache; the
second lacked installed worktree dependencies. Final run used a task-local npm
cache and a symlink to the existing HOS node_modules, and passed. No credentials,
network account requests, production imports, deployment, generation or media
changes were involved. Existing package caption warnings remain warnings.

## J3057 correction validation — 18 November 2026

Isolated worktree from PR651 ff02370bdc671a270c2ee88b4c9efb3fd018ea70.

- Updated synthetic suite: 11 tests PASS, including integer-zero refusal, raw
  refusal of either flattened key, historical dual agreement/contradiction,
  historical nested-only acceptance, canonical zero and freshness markers.
- Original J3052 probe.py from 80dc8fe06b31d1c49cfc0e808bc908c1b4cd905a:
  all 28 synthetic probes run and inspected, no crashes. Integer zero, leading
  zero strings and derived fields labelled raw now refuse. Historical evidence
  remains labelled historical and all accepted results deny generation and
  explicitly report freshness_assessed false.
- The stale-payload and two default-json-loader duplicate probes still return
  evidence only. This is deliberate at this dictionary-only boundary: lost
  duplicate keys cannot be recovered. FINDINGS now requires duplicate rejection
  by a future raw-body loader and separate freshness/account checks before any
  integration review. These outputs are not a successful raw-body validation.
- Required check_all.sh: ALL CHECKS PASS, with existing package warnings only.
  Used the existing checkout's node_modules and task-local npm cache.
- git diff --check: clean.

No account requests, POSTs, generation, billing change, deployment, production
imports, integration or guard relaxation. The closed allowances and existing
holds are unchanged. Independent exact-commit review and Chief decision remain.
