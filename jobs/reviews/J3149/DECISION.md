# J3149 — HOS 009 music safeguard decision

19 November 2026. Codex, elected acting Chief; relay status rechecked before ruling.

## Decision: accept offline repair; do not approve production

Accept J3148 PASS only for its explicitly offline scope. No merge/deployment of PR669, live integration, subscription request, music request or new allowance is authorized. PR670 remains independent review evidence. No failed gate is waived.

Repair: HOS PR669 commit `11ed0c86d925dca5cbbbd1a2abef71326f1b6b7a`. Independent review: HOS PR670 commit `aada28a66e9b378d37bb24bdedfa321005e43410`, Gemini reviewing Cursor's implementation.

| Artifact | SHA-256 |
|---|---|
| guard | `930d987783055d1f73e80fd9ae770f1ecde63d79b397706df74e9492b4029308` |
| adapter | `0550bb49bec3d6e55706beba73618e4aa9560487a2935ea9eb8cec84fa912819` |
| subscription shape | `ba290b64740c96c3407af17da80d043be3bf840d1863518bfb011e047f9e647e` |
| independent review | `0569ff65f5af6a095ab3875976bfa20abc1e1168ed76ea0f439e76fc5b7f6170` |
| independent probes | `5074b646a4517358012763c00707d9a81f1022615667cd509e2f4525ad152efe` |

Hashes independently reproduced from git objects. Reran 22 unit tests and 12 adversarial suites: all passed. Initial unit extraction omitted three unchanged production files needed by one test; extracting those from the exact repair commit resolved that fixture error. No production state or account used.

## Remaining requirements

The proposal explicitly sets TARIFF_CURRENT_GUARANTEE false. Its 2475 measured credits, 2700 published estimate, 2970 margin and 1:1 capacity ratio come from one historical take, not proof that the next request stays within 3000 subscription credits and GBP0. J3149 explicitly says uncertain tariff/capacity retains holds.

Live el_client still performs a nested subscription GET; generate_music_bed still bypasses this guard. The integration note is not an implemented patch. The receipt seal trusts its fetch callback; production transport and desk binding must be internal and isolated from fixtures. Unknown promo structures and clock skew must fail closed without automatic single-use resets.

J3150 owns a disabled-by-default offline integration proposal and current official tariff/capacity evidence. It requires one mocked GET and at most one mocked POST through every music entry point, continuous actual recorder ownership, restart durability, and no bypass. It must queue independent review and an elected-Chief activation decision before deployment or account activity. If the <=3000-credit/GBP0 bound cannot be established, report the exact missing evidence and a concrete no-spend existing-score route. Do not repeat the unchanged A-D repair loop or make exploratory account requests. Full scope is in the queue.

## Conditions for a later separate score scope — not opened here

Only after the integration, current cost/capacity evidence and explicit Chief deployment decision pass may a separate scope authorize one fresh subscription GET preserving nested overage amount/currency, then at most one 180-second instrumental music_v2 request on a fresh passing guard. Maximum 3000 subscription credits, GBP0, no retries; stop on ambiguity or failure. No renewal or pooling of old allowances.

A later prompt must request continuous instrumental accompaniment with no silent breaks, dropouts or stop-start passages (addressing J2808 v02), restrained period instruments beneath narration, and distinct wonder/teach sections. The arrangement must cover the entire locked film, joins and tail, and pass music_gate and current levels/coverage checks. Require independently demonstrated audio review and a separate exact-hash score disposition before reopening J2035. This session claims no audio or motion perception.

J3047 closure of J3043/J3045 remains permanent. J2808 score v01/v02 remain rejected. J2035 remains blocked for a separately accepted compliant score. J2171 remains blocked for that score, completed long and its own gates. No schedule changes or new ready-by promise. Zero ElevenLabs account calls, generation, deployment or spend. No action is needed from Ben for this internal decision.

Repository validation: check_all.sh passed all checks using the existing installed dependencies; git diff --check clean. Initial sandbox cache access failure was resolved by using the isolated worktree with existing dependencies and normal filesystem access.
