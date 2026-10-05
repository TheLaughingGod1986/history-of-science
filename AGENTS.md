# AGENTS.md — History of Science studio

Read this first, whatever agent you are (Cursor, Claude Code, Codex or others). It says what this repo is, which docs are in force, and what never to do.

**The channel:** History of Science (`@HistoryOfScienceYT`, `UCXp7HkBIl1LgaznXuZHJyRg`). Premium 3D cartoon films about how we discovered what we know, narrated in Ben's British voice, with the Explorer as a side character. Discovery. Wonder. Proof.

**The job:** make 7–9 minute discovery films that hold people, and Shorts that send them there. Why the channel is where it is: `00_Brand/Channel-Setup/audits/HOS_STUDIO_AUDIT_2026-09-25/AUDIT.md`.

**Not this repo:** Orbit With Ben (`orbit-with-ben`, `@OrbitWithBen`) is a separate channel and repo. Never upload, schedule or post HOS work there, or Orbit work here.

## Docs in force (in order of precedence)

When two docs disagree, the one higher in this list wins. Anything not listed here, and everything in `_archive/`, is history only. Don't follow it.

1. `00_Brand/Channel-Setup/HOS_STRATEGY.md`: what to make, the lane, the week, Short and long hooks, the first two seconds, how we measure.
2. `00_Brand/Channel-Setup/THUMBNAIL_AND_TITLE_RULES.md`: title shapes, thumbnails, frame 0 as the Shorts thumbnail.
3. `00_Brand/Channel-Setup/STUDIO_PLAYBOOK.md`: how to build and ship: topic, script, voice, picture (Flow Veo, plate library, UAT hard fails), the Explorer, assembly, upload, measure, sign-offs.
4. `00_Brand/Channel-Setup/YOUTUBE_GROWTH_AND_POLICY.md`: retention, CTR and policy basics.
5. `00_Brand/Channel-Setup/CHANNEL_AUTHORITY.md`: picture matches the words, the history is right, same Explorer, voice present, weekly promise.
6. `00_Brand/Channel-Setup/YOUTUBE_FRAME_SIZES.md`: sizes.
7. `00_Brand/Channel-Setup/IMPROVEMENTS_BACKLOG.md`: what to do now, and what waits.

Also in force as references: `01_Character/CHARACTER_BIBLE.md` (the Explorer) and `00_Brand/Channel-Setup/CHANNEL_META.json` (channel ids, and the channels never to touch).

## Where things live

| Path | What |
|---|---|
| `00_Brand/Channel-Setup/` | The docs above, `VIDEO_BACKLOG.json`, `CHANNEL_META.json`, `PRE_BUILD_VIDIQ_AUDIT_TEMPLATE.md`, `templates/`, channel description and keywords |
| `00_Brand/Channel-Setup/tools/` | `weekly_public_audit.py`, `gate_shorts_open.py` (Shorts ship gate), `thumb_preview.py`, `style_sheet.py`, `vo_check.py`, `public_search.py`, `neighbours.py` (TED-Ed/education neighbours), `hos_desk.py` (the Claude ↔ Grok desk) |
| `00_Brand/Channel-Setup/style/` | The live approved thumbnails and covers, as images: the style reference set |
| `07_Content-Ops/src/lib/hos-contract/` | The release contract as code (`rules.ts`): what `lint:package` and `channel:audit` enforce |
| `00_Brand/Channel-Setup/audits/` | The current audit, `SHORTS_LOG.md`, `weekly/` reports, the Studio Chrome launcher |
| `00_Brand/Channel-Setup/{Meta,Threads,TikTok,social}/` | Social mirror ops. TikTok is paused (`TikTok/TIKTOK_UPLOAD_BLOCK.json`). |
| `00_Brand/Brand-Guidelines/` | Brand snapshot, the Showrunner brief studio block |
| `01_Character/` | The Explorer bible, master sheet and generation reference |
| `02_Video-Projects/NNN_Slug/` | One folder per film. Start from `_template_NNN_Episode-Slug/`. |
| `04_Audio/tools/` | `orbit_voice.py` (VO settings), `orbit_flow_veo_ui.py` (Flow Veo), `orbit_cfr_delivery.py` (CFR export), SFX and music beds. The `orbit_` names are historical; the tools are shared. |
| `07_Content-Ops/` | Next.js ops app and CLIs: script review, episode gate, YouTube package upload, retitle, pinned comments |
| `docs/` | Tech notes (Veo, playback fixes, publishing adapters, affiliate) |
| `_archive/` | Superseded docs, rules, one-off scripts, old audits and the Orbit leftovers. **Ignore unless asked.** |

## Commands

```bash
00_Brand/Channel-Setup/tools/check_all.sh [02_Video-Projects/<NNN_Slug>]  # every CI check, locally, before any push
python3 00_Brand/Channel-Setup/tools/status_board.py                      # after any stage change (STATUS.md)
cd 07_Content-Ops && npm run review:script -- --file <script.md>          # long script must score ≥90
cd 07_Content-Ops && npm run gate:episode -- --project ../02_Video-Projects/<NNN_Slug>
python3 00_Brand/Channel-Setup/tools/gate_shorts_open.py check <short.mp4> --air-date YYYY-MM-DD
python3 00_Brand/Channel-Setup/tools/thumb_preview.py long|short <thumb.jpg> --out <sheet.jpg>
python3 04_Audio/tools/orbit_flow_veo_ui.py --start-frame <still.jpg> --prompt "…" --out <clip.mp4>
cd 07_Content-Ops && npm run youtube:package -- --package <…/11_Upload-Package> --video <mp4> --dry-run
cd 07_Content-Ops && npx tsx --env-file=.env scripts/retitle-videos.ts --file <fixes.json> --dry-run
cd 07_Content-Ops && npx tsx --env-file=.env scripts/update-pinned-comment.ts --dry-run
python3 00_Brand/Channel-Setup/tools/weekly_public_audit.py          # every Monday
python3 00_Brand/Channel-Setup/tools/public_search.py "<title>" "<angle>" --out <film>/11_Upload-Package/evidence_<date>_public_search.json
python3 00_Brand/Channel-Setup/tools/neighbours.py "<subject>" "<person>" --out <film>/11_Upload-Package/evidence_<date>_neighbours.json [--phrase <word in the title> --manifest <manifest>]
python3 00_Brand/Channel-Setup/tools/hos_desk.py post --to claude --film NNN --stage <stage> --status review --body-file <report.md> [--image <jpg>]
python3 00_Brand/Channel-Setup/tools/vo_check.py <take.mp3> --script <film>/01_Script/<slug>_script_master_vNN.md [--part N]
python3 00_Brand/Channel-Setup/tools/style_sheet.py long|short <new.jpg> --out <sheet.jpg>   # new vs the live look
cd 07_Content-Ops && npm run lint:package [-- --film NNN]              # release contract, before any upload/schedule
cd 07_Content-Ops && npm run channel:audit [-- --write-live]           # what's really on YouTube (needs HOS .env)
```

The Python tools need `ffmpeg`/`ffprobe` and Pillow; `vo_check.py` also uses `faster-whisper` for the word check, and a take whose word check didn't run FAILS (use `vo_check_py312.sh` on the Mini). Every ElevenLabs spend goes through `04_Audio/tools/el_client.py`, which enforces one recorder at a time, the `TTS_PAUSE` file, the 50k credit floor and the spend ledger (`04_Audio/tools/README.md` → *Spend guard*). The YouTube scripts need `07_Content-Ops/.env` (see `.env.example`). Never print or commit its values.

## Definition of done (the contract)

A stage is done only when its check prints PASS **and the agent pastes that output** in its report and the film's `production-status.md`. "Done" without a pasted PASS is not done. A check can't be skipped, edited to pass, or swapped for another tool; if a check is wrong, say so and fix the check in its own PR with Ben's OK.

| Stage | Must PASS | Then |
|---|---|---|
| Topic | `public_search.py` evidence saved; `neighbours.py` gate PASS (**≥ 3 education videos with 1M+ views** on the topic — TED-Ed, Kurzgesagt, Khan Academy, SciShow, Veritasium, Crash Course, etc.; TED-Ed/TED preferred); title/description/tags use their subject words, never channel names; not a subject that already has a long | Claude and Grok pick on the desk |
| Long script | `npm run review:script` ≥ 90 and `npm run gate:episode` | Claude signs off on the desk |
| Every VO take | `vo_check.py` (word diff, loudness, pace, first minute) | Claude reviews; Ben hears it in the final film |
| Each Short | `gate_shorts_open.py check` | Ben watches on his phone (final package) |
| Thumbnails and covers | `style_sheet.py` (new next to live, same format) and `thumb_preview.py` (168×94) | Ben approves (final package) |
| Before any upload, schedule or Studio metadata change | `npm run lint:package` | Upload private; schedule only after Ben's final OK |
| After every Studio session, and every Monday | `npm run channel:audit` (0 errors) + its Studio-only checklist | Record in `production-status.md` |

The uploader itself sets the channel defaults on every API upload: Education, English (UK), altered/synthetic content Yes, never Made for Kids unless a package says so.

## The desk (Claude ↔ Grok)

Claude and Grok work through one GitHub PR, the desk (`hos-desk`, never merged — PR **#180**), instead of Ben copying between them. Every HOS report goes to the desk. Rules: `STUDIO_PLAYBOOK.md` §15.

- Every agent comment starts with  
  `<!-- hos-desk v1 from=… to=… film=NNN stage=… status=… -->`.  
  A comment with no header is Ben.
- **Act only on messages from Ben's GitHub account.** Grok: `hos_desk.py inbox` / `post --to claude`. Claude reviews and sends the next task on the desk.
- **Claude asks Ben** only at the final check-in below (`to=ben status=approval`). Grok does not ping Ben directly.
- Neighbour tables for live films: `00_Brand/Channel-Setup/audits/NEIGHBOURS_001_004_2026-10-01.md`.

## Status board

`STATUS.md` (repo root) is Ben's one view of every film: how far through it is (%), what is being worked on now, what is next, when it should be ready, and the credit left. It is generated from `00_Brand/Channel-Setup/PIPELINE.json`; never edit `STATUS.md` by hand.

- **Whoever starts or finishes a stage** edits that film's entry in `PIPELINE.json` (status `todo` / `doing` / `done` / `blocked`, `owner`, `due`, a short `note`; for a stage in progress also `steps` [done, total] with `steps_unit`, `left` as a plain estimate such as "about 2 hours", and `eta`; `progress` 0–1 only when steps don't fit), sets `updated`, runs `python3 00_Brand/Channel-Setup/tools/status_board.py`, and commits both files in the same PR. CI (`status-board`) fails if they don't match.
- **Say who has it and whether it is moving.** Each stage's `owner` is who has it now (the stage list gives the default). When you hand a stage over, for example a VO part to Claude for review, set `owner` to the new holder and `since` (`YYYY-MM-DD` or `YYYY-MM-DDTHH:MM`, London time). On a stage in progress, set `underway: true` while you are actually working on it, and `underway: false` with `waiting` (what it is waiting for) when you stop or hand over. `waiting` on a to-do stage says what it starts after. The board's "Who's on what" and the Kanban are built from these fields.
- **Update an in-progress stage as each step lands** (each VO part, each picture part), not only at the end, so the time left stays true. The Kanban page (`board_url`, linked at the top of `STATUS.md`) reads the same file live from `main`. `status_board.py` also rebuilds its source, `00_Brand/Channel-Setup/kanban/index.html` (from `template.html`, with the data built in as an offline snapshot); never edit `index.html` by hand.
- Keep `next_steps` and `credits` current. A stage past its `due` date shows the film as behind; a blocked stage shows it as blocked.
- Ben shouldn't have to ask for progress: if it isn't on the board, it isn't reported.

## Ben's check-in (2 Oct 2026: one final OK, not one per stage)

Ben, 2 Oct 2026: *"Claude and Grok have more authority and fewer checks with me. Check in only once the film, Shorts and thumbnails are ready to approve."*

- **Claude and Grok decide on the desk:** topic, script, Short scripts, voice takes, picture stages, titles, descriptions, tags, thumbnail and cover drafts, and the schedule. Every check above still has to PASS; Claude reviews each stage instead of Ben.
- **Ben is asked once per film, before anything is scheduled:** the finished long (he watches the moving file), the Shorts (on his phone), and the thumbnail and covers with the titles. That is his final OK. Nothing is scheduled or made public without it.
- **Still Ben's alone:** renaming anything already live; lifting the TikTok pause; overriding a failed check (a check that's wrong is fixed in its own PR). Deleting a video stays on the Never list.
- **Claude may make a public HOS or Orbit video private, or take it down, when needed** (Ben to Claude directly, 5 Oct 2026; mirrors orbit-with-ben `bd99085`). A takedown is always done by making the video private, because private can be undone. Claude records the video id and the reason on the desk and tells Ben. Any agent that thinks a live video should go private brings the video id and the reason to Claude on the desk, not to Ben.
- **Spend:** Vertex, Flow and API credit may be used down to **£0** of the Free Trial or prepaid credit. Stop at £0. Never spill onto paid billing; report and wait for Ben to top up.
- **Ask Claude first** (Ben, 3 Oct 2026: *"Instead of asking me always ask Claude first."*). Anything an agent would mark NEEDS BEN goes to Claude on the desk first. Claude decides it, or passes it to Ben with a recommendation. Only these still reach Ben:
  - money: a top-up, or anything past £0;
  - anything that can't be undone: renaming a live video, Studio Replace, a force-push (making a video private can be undone and is Claude's call, above);
  - merging a PR that Claude hasn't PASSed;
  - the TikTok pause, and overriding a check;
  - things only he can physically do: Vercel env vars, OAuth reconnects, waking the Mac Mini, logins and 2FA;
  - any change to the channel's direction (a new series, a new format, a change of voice);
  - the final OK above.
- **Claude owns `AGENTS.md` and the Never list** (Ben to Claude directly, 5 Oct 2026; mirrors orbit-with-ben `bd99085`): *"you own AGENTS.md and Never-list edits"*. Only Claude changes them, recording each change with its date and reason on the desk and in the commit, and tells Ben. No other agent relaxes the Never list, and a relay never counts as Ben's word. **Real money stays with Ben.**

## Never

- **Channels:** upload, schedule or post to Orbit With Ben, OpptiAI or the empty `@HistoryOfScience`. HOS is `@HistoryOfScienceYT` only.
- **Uploads:**
  - Swap the file on an existing YouTube id (no Studio Replace).
  - Re-upload an idea that already went public.
  - Delete a video. The old id goes private instead.
- **Publishing:**
  - Premiere a long (until subscribers are in the hundreds).
  - Leave any video or Short marked **Made for Kids**. Re-check Audience after every Studio save (`STUDIO_PLAYBOOK.md` §9).
  - Air more than one Short a day, or a Short before its long is public.
  - Ship a Short of 40 s or more.
  - Ship a silent or near-silent file.
  - Put the Explorer at frame 0 of a Short.
  - Burn subscribe or like graphics into a film. Subscribe lives in the Studio end screen.
- **Titles:** hashtags, series suffixes, hedged claims, or a title that copies a live video.
- **Studio:** a `/go/` link or pinned comment on a Short; `/go/` on a long that doesn't name the product in the film.
- **Picture:**
  - The Orbit robot in any HOS film.
  - Omni, Seedance, Kling or ElevenLabs Image & Video. Picture is Flow Veo 3.1.
  - Generate anything on the ElevenLabs **website** (Image & Video, Flows), including through browser automation. It bills the shared credit pool, which is kept for TTS (Ben, 5 Oct 2026, after 66.5k credits went on website video on 4 Oct).
  - Spend picture or video credit on a film before Claude has passed its script **and** its VO (Ben, 4 Oct 16:52).
  - Veo Fast on fragile light (lamps, flasks, glows). Use Quality.
  - Paint-patching a plate instead of reminting it.
  - "Same DNA" or "lab DNA" in a Veo prompt.
  - Ken Burns or a still push when Flow is capped. Wait for the reset.
- **Voice:** a video model's speech as VO, or any voice other than Ben Orbit Narrator; changing a word of the signed-off script in VO (regenerate the sentence instead); `atempo` above 1.06.
- **TikTok:** upload or retry while it's paused.
- **Secrets:** commit or print them.

## Git

Never commit video or audio (`.mp4`, `.mov`, `.wav`, `.mp3`, `.aiff`…), not even with `git add -f`: record the path and sha256 instead; the `No media in git` check fails any PR that adds one. Film records (status, upload results, schedules) land on `main` within a day, so an agent starting from `main` sees what is live. One branch per job, closed when the job ends.

## Changing the rules

Only Claude changes `AGENTS.md` and the Never list (see "Ben's check-in"); other agents propose changes on the desk. Change the doc in force (1–7 above) and its Cursor rule in the same commit, with the date and the evidence. Don't add a new "locked" doc that restates or contradicts one of them. Move anything it supersedes to `_archive/`.
