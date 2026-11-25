# HOS publishing runtime repair — J3519

The Mini had stale Prisma 6.19.0 dependencies against the existing 7.10.1 lockfile and schema. Restored locked dependencies with npm ci (task-local cache), then successfully generated Prisma Client 7.10.1. No dependency or lockfile change, migration, database write, upload, schedule, Studio change or spend.

The audit's token refresh previously wrote connection state, despite being a read-only audit. It now requests an explicit read-only refresh: credentials refresh in memory and neither successful refresh nor invalid_grant changes a database row. Ordinary publishing callers retain their existing persistence behavior.

Validation on 24 Nov 2026:
- Prisma generate: exit 0, client 7.10.1 generated in the shared Mini runtime.
- channel:audit with PostgreSQL default_transaction_read_only=on: exit 0; 68 videos, 0 errors. Existing Studio-only disclosure and finish warnings remain warnings.
- J3512's exact prepared Short A package dry run: exit 0, ok:true, private, publishAt null, no request sent. The pre-19-Nov approved 23.3 s cut retains its duration warning. Description/tags/cover/Related approvals remain J3512's work.
- Full check_all.sh: ALL CHECKS PASS.
- Token and HOS contract tests: 33 passed, including success/failure no-write checks and ordinary publishing persistence.
- NAS scratch offload: no eligible old scratch; no media moved or deleted.

Uploads remain exclusively with J3500, J3501, J3511 and J3512. This repair is not a packaging approval.
