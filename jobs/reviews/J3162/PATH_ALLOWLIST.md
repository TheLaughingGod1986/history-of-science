# J3162 path allow-list

19 November 2026. Follows Chief ruling 7021895689 on Claude's review 7021875555 of `faa8f75731a91d50b9ce999a4b80c4fa4562fce9`. Not a Chief ruling, not a PASS, no merge.

`other` is now an allow-list. A built-in string is `other` only when it is a clean `/v1/text-to-speech`, `/v1/speech-to-speech`, `/v1/speech-to-text` or `/v1/user/subscription` path. Canonical `/v1/music` stays on the disabled flight. Everything else is `reject`, including `/v1/sound-generation`.

Before that match, any path containing `%`, `\`, `//`, `/./`, `/../`, whitespace or a control character, or not starting with `/`, is `reject`. Music is recognised case-insensitively, so `/V1/MUSIC` is `reject`. The same check is in `el_guard.is_spend`: those POST forms return True, so the legacy guard fails closed.

`generate_sfx_from_script.py` POSTs `/v1/sound-generation`. That call now raises `malformed_request` and does not reach the socket. Speech, Scribe and the subscription read are unchanged.

Hashes: `el_client.py` `98c861e0bdbd6ea87d6c5b7861cd930db60c172dfa5b3edae9d450a1ca6aadc0` (was `aabdc7502bf6edcedb735e32427a89046d9794c0cea6c90eabb8d793b9692bb5` at faa8f757). `el_guard.py` `2465a18393efeacfe80f25fffe97095be7fcee3270df6a82e79f538df72450e1`. Pinned guard `930d987783055d1f73e80fd9ae770f1ecde63d79b397706df74e9492b4029308` and shape `ba290b64740c96c3407af17da80d043be3bf840d1863518bfb011e047f9e647e` are unchanged. `jobs/reviews/J3162/HASHES.txt` still records faa8f757.

Offline, fixture desks only: 5 routing tests, 23 flight tests and 11 guard tests passed. `check_all.sh` passed except package-lint `schedule.past` on the unchanged 008 manifest, the same baseline as the faa8f757 repair. 009 package-lint passed. Contract tests: 28 passed. No account call, no network, no live lock or store. Activation stays false. The pricing evidence still does not establish a 3,000-credit, £0 bound. v01/v02 stay rejected, J2035/J2171 held, J3047 closed unused. £0. Nothing for Ben.
