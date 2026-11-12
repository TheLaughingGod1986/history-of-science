# J2578: which rules moved to `studio/RULES.md`, and which stayed

History of Science's rule book is two files from this change, as Orbit With Ben's has been since its J2527:

- `AGENTS.md`: the rules that are not this channel's alone (the desk, who does what, the status board, Ben's check-in, uploads, secrets, network details, git). They stay here until the studio has its own repo.
- `studio/RULES.md`: History of Science's own rules.

Both are in force. Where they disagree, `AGENTS.md` wins.

## How it was done

`jobs/reviews/J2578/move.py` made the move. It reads both files at main (`aba45ecb`), writes both, and checks the result:

```
old AGENTS.md: 416 lines; old studio/RULES.md: 18 lines (343 with text in all)
new AGENTS.md: 179 lines; new studio/RULES.md: 272 lines
lines moved to the channel file: 197 with text
lines of the old pointer file dropped on purpose: 4
lost or changed: 0
added and declared: 12
added and NOT declared: 0
```

One rule decided every case: **a line is never cut in two.** Each line went whole to one file, so no word could change. A line moved only if it is about this channel alone: its films, its Explorer, its picture and voice routes, its titles, its accounts, its own docs.

## What moved

| From `AGENTS.md` | Lines (old) | Now in `studio/RULES.md` |
|---|---|---|
| **The channel**, **The job** | 7, 9 | under the title |
| Docs in force | 15 to 27 | "Docs in force (in order of precedence)" |
| Definition of done (the contract) | 76 to 90 | the same heading |
| Teach on screen | 92 to 146 | the same heading |
| Polish pass | 147 to 208 | the same heading |
| Reference lessons | 209 to 277 | the same heading |
| Packaging | 278 to 286 | the same heading |
| Never: Channels | 364 | "Never (this channel's additions)" |
| Never: Publishing, four lines (Premiere, Made for Kids, the Explorer at frame 0, burned-in subscribe graphics) | 371, 372, 376, 377 | the same |
| Never: Titles | 378 | the same |
| Never: Picture, with its eight lines | 380 to 388 | the same |
| Never: Voice, TikTok, Social | 389 to 391 | the same |

The old `studio/RULES.md` was an 18-line pointer. Its lines about `channel.json` and about studio-wide rules coming first are kept, under "How the studio plugs this channel in". Its title and the paragraph that said the rules were in `AGENTS.md` are dropped, since that is no longer true (4 lines).

## What stayed, where the plan said otherwise

The plan (`docs/RULES_SPLIT.md` in orbit-with-ben, "What History of Science's own rules file should hold") listed three things to move that this change leaves in `AGENTS.md`. Each is for the Chief to confirm or overrule.

1. **Ben's check-in stays whole.** Read line by line, all but one of its lines are not this channel's alone: who decides, what only Ben does, spend, "four a month on each channel". The exception is the Test B line (search-titled Shorts, from 007 on). The section is also copied whole into the Cursor rule and the playbook; taking one line out would change those copies. So it stays whole.
2. **The Never list's Studio line stays.** It holds both kinds in one line: the `/go/` link rule, which is this channel's, and the "Run a new test?" rule, which is the studio's. A line that holds both kinds stays in `AGENTS.md`, where a studio rule can never be lost.
3. **The week** (publish days and times) stays, as J2578's brief says.

Also staying, as planned: Where things live, Commands, The desk, Who does what, Status board, the Never list's Uploads, three shared Publishing lines (one Short a day, 40 seconds, silent files), Secrets and Network details, Git, Missing footage fallback, Studio core, Changing the rules.

## What is new (12 lines, all declared in `move.py`)

- In `AGENTS.md`: the pointer to `studio/RULES.md` in the first screen; a short "Docs in force" paragraph where the list stood; one line under the Never list and one under "Changing the rules", each saying where the channel's part is.
- In `studio/RULES.md`: the title, the opening paragraph, two headings, one line under the channel's Never list, and the **Publishing** header (needed in both files).
- **One new rule line**, in the channel's Never list: a Short must not ship with a shot that does not fill the 9:16 frame. The shared gate (`gate_shorts_open.py`) has failed such a Short since 10 Nov 2026, and no rule file here said so.

## What else changed, so the two files are read

- `scripts/sync_rules.py` reads both files. A marker names its file: `<!-- SYNC: studio/RULES.md#Teach on screen (Ben, 11 Oct 2026) -->`. The copies of Teach on screen and Polish pass in `.cursor/rules/hos-studio.mdc` and `STUDIO_PLAYBOOK.md` now name `studio/RULES.md`. **The copied text itself did not change by a character**: `sync_rules.py --check` passed before anything was regenerated.
- `.github/workflows/rules-check.yml` also runs when `studio/RULES.md` changes.
- Entry points name both files: `CLAUDE.md`, the always-on Cursor rule, the session hook, and the desk worker's prompt in `hos_desk.py`.
- Pointers that named a moved section now name `studio/RULES.md`: two Cursor rules, `HOS_STRATEGY.md`, the Showrunner brief template, two workflow comments, `atempo_check.py`'s description.
- Not changed: records (audits, ideas, live fixes) that quote "`AGENTS.md` Never list" or a moved section. They say what was true when they were written. A shared file's comment (`shorts-gate.ts`, "AGENTS.md → Packaging 5") is also left: shared files are changed from orbit-with-ben.
- No runner, plan, scope or any file a live picture job pins was touched.
