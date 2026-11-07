# HOS 099 — audit handoff, 4 November 2026

Codex acting Chief, J1917. This note records checker/audit evidence only; it does not approve the film or replace Ben’s watch.

Ben-approved checker [PR365](https://github.com/TheLaughingGod1986/history-of-science/pull/365) merged normally at `8cb5a749a0729ded7389f35617de8108b5cbbb2e`, from reviewed head `fab39c33ed51a0906b3ec2a637141601ff1d118b`. Five GitHub checks succeeded; desk-reopen was appropriately skipped. Fresh local contract tests: 28/28 PASS; core: 56 shared files PASS; rules and diff whitespace PASS. Merged-main checker files match the reviewed head exactly.

On the authenticated Mac mini, from a clean worktree of that merged main, `npm run channel:audit` exited 0 on 4 November at approximately 01:17 UTC. The live channels.list identity guard accepted HOS `UCXp7HkBIl1LgaznXuZHJyRg`; this was not an offline fixture. Exact relevant output:

```text
PASS  long  uAomPaOBrM8  private 2026-12-10 18:00 UK  How Did Experiments Explain Blood, Germs and Atoms?
   warn  [ai-disclosure] Data API omits altered/synthetic — confirm Yes in Studio (Altered content)
62 videos, 0 errors.
core OK (56 shared files)
rules OK
```

The full owner-view log stays local at `~/_desk/logs/J1917-channel-audit.txt`, SHA-256 `90268bf9982b4a1b65ad1d4e559aec96822be85f6bdd56c1472565bebc19787f`. No private analytics were collected or published. Warnings remain: ai-disclosure=62, embeddable=13, tags.count=6. They were not suppressed. The checker fix removes repeated identical IDs, and still rejects duplicate titles on distinct IDs.

J0998’s approved fix and postmerge audit are complete. Its original 4/4 milestone history must be retained.

J0999’s original 5/5 worker milestones remain historical evidence, not blanket Studio approval. Reviewed `REVIEW_J0999.md` and `STUDIO_READBACK_J0999.json` at PR358 commit `c26a79bdbe22dd0207a7073ab582c3c686282555`: saved end screen 48:58:06–49:18:06 with Subscribe, GHZDsiH7L7A and playlist PLEbpfUzWzcXU; Altered content Yes; Not Made for Kids; paid promotion false; unchanged title/privacy/schedule/test. No Studio write was repeated.

The checker-approval hold is satisfied. J0999 remains unfinished because the full required Studio-only checklist is not documented: cards, education fields, automatic places, comments/moderation and Studio timezone; public-only pinned comment/Test & Compare must be explicitly marked pending until public where applicable. Its existing PR358 also remains open and contains a broad historical branch, so it was not merged wholesale under the narrow PR365 approval. The next worker on J0999 must verify only the missing items read-only, preserve all completed settings, and land narrowly scoped evidence/production records through normal Chief review. Any needed metadata change requires its own lint and authorization. No new Ben approval is needed for this read-only verification.

No upload, schedule, retitle, privacy, Buffer, generation or credit action occurred in J1917. The separate Franklin watch-link permission remains untouched.

## J0999 read-only Studio checklist — 4 November 2026

Codex specialist worker, not acting Chief. Reused the HOS Studio tab on CDP 9460 and confirmed `window.ytcfg.get("CHANNEL_ID")` = `UCXp7HkBIl1LgaznXuZHJyRg`. Target was `uAomPaOBrM8`; no changes were saved. Main checkout was left untouched; this evidence branch starts at HOS main `69f880bd`.

The missing checklist is now inspected, and reveals corrections that need Chief scope before any further writes:

| Item | Saved readback | Required next action |
|---|---|---|
| Cards | Empty editor: “Select a type of card to begin”, empty card track, Save disabled | Chief scopes two relevant cards after first minute |
| Education | Category Education; Type None; Academic system Other; Level None; Exam blank | Concept overview/explainer, England and appropriate offered level/course under playbook §9 |
| Automatic places | Checked/on | Turn off after authorization and package lint |
| Chapters / concepts | Both checked/on | Preserve |
| Comments | On; Moderation None; Anyone; Top; likes shown | Basic moderation / hold potentially inappropriate for review |
| Studio time zone | Selected `(GMT+0000) Local Time` | Explicit London is not verified; Chief scopes correction. Current UTC offset equals London, but that does not prove a London selection |
| Caption certification | None | Review against “never aired on TV” requirement |
| Paid promotion | Neither Yes nor No radio selected in current DOM | Historical API false is not proof of an explicit saved No; Chief checks/sets No |

Confirmed unchanged relevant settings: AI use Yes checked; Not Made for Kids checked; no age restriction checked; both languages English (United Kingdom); video/audio remixing, embedding and subscriber notification checked. Playlist displays “How Did We Discover…? | History of Science”. Visibility remains Scheduled, 10 Dec 2026 at 18:00 UK / 18:00 UTC, Premiere unchecked. Title remains “How Did Experiments Explain Blood, Germs and Atoms?”.

Reopened the saved end-screen editor after page reload: Subscribe: History of Science; Video: What's Really Inside an Atom?; Playlist: How Did We Discover…? | History of Science (6 videos). Time inputs remain `48:58:06`–`49:18:06`; Save disabled. The exact target IDs are established by historical PR358 evidence and were not re-resolved from this UI. Closed editor with Discard changes; no edits were made.

Pinned comment and running Test & Compare are **pending until public**, not passed. No test was started, reset or otherwise changed. Older-long end-screen updates remain a post-public action. No audio or moving-video review is claimed.

Fresh authenticated merged-main `channel:audit` exited 0: **62 videos, 0 errors**. This code result does not cover the Studio-only gaps above. Audit used the clean worktree with existing local dependencies and the existing HOS credential file; no secrets were recorded. The first attempt lacked a dependency path; linking the existing ignored node_modules resolved it without installing anything.

Raw DOM readbacks, screenshots and full audit output stay locally in `/Users/benjaminoats/_desk/jobs/J0999/evidence-2026-11-04/`; SHA-256 manifest is `J0999_EVIDENCE_2026-11-04.json`. Screenshots are still evidence only. No upload, schedule, retitle, privacy, Buffer, credit, merge or metadata action occurred. J0999 stays parked for Chief to review this narrow evidence PR and scope the checklist corrections; historical 5/5 milestones are retained, not film approval.

## J2199 checklist writes — 6 November 2026

Cursor worker, not Chief. Channel `UCXp7HkBIl1LgaznXuZHJyRg`, video `uAomPaOBrM8`, CDP 9460, one reused Studio tab. `npm run lint:package -- --film 099` exited 0 with "No packages found" (this compilation has no package manifest). Title, privacy, publishAt, end screen, playlists, AI disclosure and Not Made for Kids were not edited. Premiere stayed off. Pinned comment and Test & Compare were not started.

Reloaded readback of what saved:

| Item | Reloaded value |
|---|---|
| Visibility | Scheduled |
| Type | Concept overview |
| Academic system | England |
| Automatic places | Off |
| Automatic chapters / concepts | On / On |
| Moderation | Basic. Comments On, Anyone, Top, likes shown |
| Caption certification | This content has never aired on television in the US |
| Paid promotion | No |

What did not save, so it is not a pass:

- Level. Key stage 4 and Year 10 both showed in the control, then a reload still read Level None. Exam was left blank because no single GCSE subject covers blood, germs and atoms.
- Time zone. The saved selection is still `(GMT+0000) Local Time`. Choosing `(GMT+00:00) London` updates the control, and the clock stays 18:00 on 10 Dec 2026 with Premiere off, but Done stays disabled, so the London choice was discarded.
- Cards. The editor was empty and nothing was saved. The two cards not written are 00:17:57 *How Did We Discover Germs?* (`_C92tIJCk8A`) and 00:24:14 *How Did We Discover the Periodic Table?* (`AL_-qlWko_g`).

Schedule left in place: 10 Dec 2026, 18:00, Premiere off. Screenshots and the SHA manifest are in `J2199_READBACK_2026-11-06.json` and on the desk at `/Users/benjaminoats/_desk/jobs/J2199/evidence`. This note is evidence for Chief. It is not a film approval.
