# J3977 — Paid product placement audit visibility

The read-only channel audit now requests `paidProductPlacementDetails` through the common videos.list path used for playlist results and recovered direct IDs. It prints each video's ID and paid-placement state in JSON and text. Existing pagination, coverage recovery and metadata checks remain in place.

- `unexpected-true`: API true without an explicit sponsorship declaration. Chief review is needed; this is not proof the flag is wrong.
- `declared-sponsored`: API true with explicit declaration evidence; stays visible for Studio confirmation.
- `false`: explicitly returned false. A conflicting sponsorship declaration produces a warning.
- `unknown`: absent object, absent value or null. Never treated as false.

All review findings are warnings, not a new release rule. No API writes or automatic corrections were added. Affiliate links and their absence do not determine sponsorship.

There was no existing sponsorship exception convention in the HOS contract/audit. Optional `--sponsorship-declarations <json>` accepts an object mapping exact video IDs to non-empty review evidence (for example a Chief decision URL). No declarations are assumed by default. Invalid declaration input stops the audit. This option works with live reads and offline `--file` inputs.

API field reference: https://developers.google.com/youtube/data/reference/rest/v3/videos#paidProductPlacementDetails

Shared-core check: channel-audit.ts, hos-contract modules and these tests are not listed in studio-core/CORE_FILES.json. No core sync or rule change required.

Validation:

```
npx vitest run tests/hos-contract.test.ts tests/paid-placement.test.ts
Test Files 2 passed
Tests 41 passed

bash 00_Brand/Channel-Setup/tools/check_all.sh
ALL CHECKS PASS

git diff --check
(no errors)
```

The focused tests cover true, declared true, explicit false, declaration mismatch, missing/null values, invalid declarations, offline CLI JSON/text and the common fetch request. Existing contract tests cover duplicate page boundaries and direct-ID recovery. No live channel read or Studio change was made in this job. Chief review remains required before merge.
