# J3162 path allow-list

19 November 2026. Follow-up to Claude's review of `faa8f75731a91d50b9ce999a4b80c4fa4562fce9` (desk 7021875555). Not a Chief ruling, not a PASS, no merge.

`_music_route` treated every path that did not start with `/v1/music` as `other`. These then went to the legacy client, and `el_guard.is_spend` missed them too, so they were a plain POST with no flight and no guard: `/v1/%6dusic`, `/v1//music`, `/v1/./music`, `/V1/MUSIC`, `/v1\music`, `/v1/x/../music`, and a leading space.

`other` is now only a built-in string that starts with `/` and contains no `%`, `\`, `//`, `/./`, `/../`, whitespace or control character, and is not a music path. Music is recognised case-insensitively and still has to be the exact path `/v1/music` to reach the flight. Speech, Scribe, sound-generation and subscription stay `other`.

`el_client.py` sha256 is now `d3e3b32c43d9347b6de05928cb594980d567b220224d5bb0025881a69eec2a2a`. The reviewed commit's hash `aabdc7502bf6edcedb735e32427a89046d9794c0cea6c90eabb8d793b9692bb5` stays in `jobs/reviews/J3162/HASHES.txt`. The pinned guard and subscription shape are unchanged (`930d9877…`, `ba290b64…`).

Offline, fixture desks only: 4 routing tests, 23 flight tests, 11 guard tests, all passed. No account call, no network, no live lock or store. Activation stays false. The pricing evidence still does not establish a 3,000-credit, £0 bound. v01/v02 stay rejected, J2035/J2171 held. £0. Nothing for Ben.
