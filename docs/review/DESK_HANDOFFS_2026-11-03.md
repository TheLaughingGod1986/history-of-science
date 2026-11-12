# Durable desk deliveries — 3 November 2026

The old inbox advanced its per-agent watermark on delivery, including failed worker runs. A subsequent inbox omitted the unfinished message. This change separates discovery from completion: actionable messages are persisted before dispatch and redelivered until a trusted, linked outcome is acknowledged. `done` notifications do not create reply loops.

Post an outcome using `hos_desk.py post ... --reply-to <original-id>` then `hos_desk.py ack <original-id> --as <agent> --ref <outcome-comment-id>`. Ack verifies the outcome is on the current desk, from the trusted account and correct agent, later than the original, for the same film/stage, and includes the exact reply_to. It accepts review/approval/blocked/done handoffs; this is delivery acknowledgement, not proof of media approval. Existing media and Ben approval gates still apply.

Pending state survives a worker failure or restart. State updates are serialized and atomic; corrupt state fails visibly rather than discarding pending work. Per-agent dispatch locking prevents two watchers delivering the same inbox concurrently. An unavailable worker retains its pending message. `inbox --recover-since-id <id>` supports deliberate recovery of messages skipped by the previous version; acknowledged IDs stay excluded. This does not automatically replay all historical requests.

Remaining live validation: run two successive inbox polls on the Mini; confirm an unfinished task remains visible and a linked outcome clears it; check role succession addresses the intended recipient. Existing historical watermarks cannot prove whether an old task was completed; review history before replaying it. This PR does not claim a completed end-to-end Mini/media/YouTube run.

## Chief-role routing (6 Nov 2026)

`to=chief` is the elected Chief's desk id: Grok, otherwise Claude, Codex or Gemini, read from the relay's `current.json` (or `HOS_DESK_ELECTED` in a test). Cursor is not in that chain and cannot post as `chief`. A comma-separated `to` list matches each named person once. A list that includes `chief` is one role copy for the current holder, not a second copy for every successor.

The first role-aware poll sets `last_role` to the newest comment id and delivers nothing older. `--recover-id` admits one older role message and does not rewind the watermark. A message already assigned to a stand-in stays there when the election changes; `handback` is how that one message returns. Ack still requires a trusted later outcome.

Messages that were already pending when this code first runs are recorded in `run_fence` and are not handed to `cursor-agent`. New literal mail still redelivers until it is acknowledged. Role mail is written for the elected id and never starts the worker.

`refresh` does not restart launchd unless the installed desk file contains this code and no worker child is running. Historical watermarks are not reset. J1754's inventory file was not on disk, so this change recovers no historical ids.
