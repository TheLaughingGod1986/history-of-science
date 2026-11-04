# Durable desk deliveries — 3 November 2026

The old inbox advanced its per-agent watermark on delivery, including failed worker runs. A subsequent inbox omitted the unfinished message. This change separates discovery from completion: actionable messages are persisted before dispatch and redelivered until a trusted, linked outcome is acknowledged. `done` notifications do not create reply loops.

Post an outcome using `hos_desk.py post ... --reply-to <original-id>` then `hos_desk.py ack <original-id> --as <agent> --ref <outcome-comment-id>`. Ack verifies the outcome is on the current desk, from the trusted account and correct agent, later than the original, for the same film/stage, and includes the exact reply_to. It accepts review/approval/blocked/done handoffs; this is delivery acknowledgement, not proof of media approval. Existing media and Ben approval gates still apply.

Pending state survives a worker failure or restart. State updates are serialized and atomic; corrupt state fails visibly rather than discarding pending work. Per-agent dispatch locking prevents two watchers delivering the same inbox concurrently. An unavailable worker retains its pending message. `inbox --recover-since-id <id>` supports deliberate recovery of messages skipped by the previous version; acknowledged IDs stay excluded. This does not automatically replay all historical requests.

Remaining live validation: run two successive inbox polls on the Mini; confirm an unfinished task remains visible and a linked outcome clears it; check role succession addresses the intended recipient. Existing historical watermarks cannot prove whether an old task was completed; review history before replaying it. This PR does not claim a completed end-to-end Mini/media/YouTube run.
