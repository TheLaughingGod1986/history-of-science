# J2324 — PR450 repair delivery

7 November 2026, Codex. Scope: repair J1809's three code defects. This is a worker delivery, not a merge or live-refresh approval.

- Refresh discovers launchd's PID and the OS process tree, rejects descendants, active/invalid desk leases, missing or malformed process evidence, and mismatched installed source. It holds a refresh lock and every recipient's dispatch lock across a second PID/idle inspection, kickstart and confirmation. Watcher startup records its actual PID, code version and loaded SHA-256. A restart is confirmed only against the new launchd PID and that exact loaded hash, with evidence in `~/.hos_desk/refresh-result.json`.
- First upgraded literal poll fences all recipients against the same full snapshot, including previously unseen historical literal mail above saved watermarks. Watermarks only increase; bulk `--recover-since-id` is refused. `--recover-id` admits one specifically reviewed unresolved message. Historical classification against later outcomes, queue and stages remains required before any live recovery.
- Pending role mail is shown repeatedly until trusted acknowledgement, including after restart and explicit handback to a Chief who has never polled. Literal delivery cannot run or fence a role copy. Cursor remains excluded from Chief succession and role dispatch.

Validation: `python3 -m unittest scripts/test_hos_desk_handoffs.py`: 20 tests PASS. `python3 -m py_compile 00_Brand/Channel-Setup/tools/hos_desk.py` and `git diff --check`: PASS. Tests mock GitHub, launchd, process snapshots and process launches; no live restart or replay occurred. Prior regression expectations that encoded historical replay or one-time-only role display were corrected; worker retry, trusted ack, routing and classification coverage remain.

Next: elected Chief reviews the corrected PR450 head. J1809 remains held. After review/merge, separately authorise an idle refresh and controlled live delivery/ack with PID/hash evidence. No historical IDs have been recovered. No media, production, publishing or spend approval is granted.
