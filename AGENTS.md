# AGENTS.md — History of Science studio

> **Handover (12 Oct 2026):** read `HANDOVER.md` first; master index in orbit-with-ben `HANDOVER.md`.

Read this first, whatever agent you are (Cursor, Claude Code, Codex or others). It says what this repo is, which docs are in force, and what never to do.

**Then read `studio/RULES.md`.** It holds this channel's own rules: the docs in force, the contract each stage must pass, what its films teach, look and sound like, how they are packaged, and the lines it adds to the Never list below. Both files are in force. Where they disagree, this file wins.

**The week (Ben, 7 Nov 2026):** **1 long + 4 Shorts a week** (was 1 long + 3 Shorts). Thursday 18:00 London for the long (normal publish, no Premiere); Shorts at 11:30 on Saturday (go-public-day Short for the new long; Thursday 11:30 would air before the long), Friday, Sunday and Tuesday. Never more than one Short a day; never a Short before its long is public; fill gaps only with ready approved cuts. Full table: `STUDIO_PLAYBOOK.md` §1 / `HOS_STRATEGY.md` → *The week*.

**Not this repo:** Orbit With Ben (`orbit-with-ben`, `@OrbitWithBen`) is a separate channel and repo. Never upload, schedule or post HOS work there, or Orbit work here.

## Docs in force

This file first. Then the channel's rules file, `studio/RULES.md`, and the docs it lists in its own order of precedence. Where one of the channel's docs and this file disagree, this file wins. Anything not listed there, and everything in `_archive/`, is history only.

## Where things live

| Path | What |
|---|---|
| `00_Brand/Channel-Setup/` | The docs above, `VIDEO_BACKLOG.json`, `CHANNEL_META.json`, `PRE_BUILD_VIDIQ_AUDIT_TEMPLATE.md`, `templates/`, channel description and keywords |
| `00_Brand/Channel-Setup/tools/` | `weekly_public_audit.py`, `gate_shorts_open.py` (Shorts ship gate), `thumb_preview.py`, `style_sheet.py`, `vo_check.py`, `public_search.py`, `neighbours.py` (TED-Ed/education neighbours), `hos_desk.py` (the Claude ↔ Grok desk) |
| `00_Brand/Channel-Setup/style/` | The live approved thumbnails and covers, as images: the style reference set |
| `07_Content-Ops/src/lib/hos-contract/` | The release contract as code (`rules.ts`): what `lint:package` and `channel:audit` enforce |
| `00_Brand/Channel-Setup/audits/` | The current audit, `SHORTS_LOG.md`, `weekly/` reports, the Studio Chrome launcher |
| `00_Brand/Channel-Setup/{Meta,TikTok,social}/` | Social: bios, the TikTok block file and the uniqueness/destination guards (posting is Buffer, below). Social posts go through Buffer only (HOS org, `BUFFER_HOS_API_KEY`). Direct TikTok uploads stay paused (`TikTok/TIKTOK_UPLOAD_BLOCK.json`); TikTok through Buffer is allowed (Ben, 5 Oct 2026). |
| `00_Brand/Brand-Guidelines/` | Brand snapshot, the Showrunner brief studio block |
| `01_Character/` | The Explorer bible, master sheet and generation reference |
| `02_Video-Projects/NNN_Slug/` | One folder per film. Start from `_template_NNN_Episode-Slug/`. |
| `04_Audio/tools/` | `orbit_voice.py` (VO settings), `orbit_flow_veo_ui.py` (Flow Veo), `orbit_cfr_delivery.py` (CFR export), SFX and music beds. The `orbit_` names are historical; the tools are shared. |
| `07_Content-Ops/` | Next.js ops app and CLIs: script review, episode gate, YouTube package upload, retitle, pinned comments |
| `docs/` | Tech notes (Veo, playback fixes, publishing adapters, affiliate) |
| `_archive/` | Superseded docs, rules, one-off scripts, old audits and the Orbit leftovers. **Ignore unless asked.** |

**Social posting (5 Oct 2026; register-at-upload J1202, 30 Oct 2026):** HOS Shorts go out through **Buffer via HOS Showrunner** only (`BUFFER_HOS_API_KEY`, HOS Buffer org). Never the Orbit Buffer org or the Buffer connector. YouTube stays in Studio. Long films are never cross-posted via Buffer. HOS Threads posting stops until Ben adds a Threads channel. **Every Short upload/swap registers** the final master into Orbit `social/hos/UPLOADS.json` at upload time (`youtube:package` `afterUpload`, or `buffer-mirror.ts register --channel hos …`); the daily `check --channel hos` mirrors when Public/scheduled. Never end an upload with only "Buffer held until public". Old Meta/Threads/TikTok CDP auto-post trees are under `_archive/00_Brand/Channel-Setup/`. Details: `STUDIO_PLAYBOOK.md` §12.

## Commands

```bash
00_Brand/Channel-Setup/tools/check_all.sh [02_Video-Projects/<NNN_Slug>]  # every CI check, locally, before any push
python3 00_Brand/Channel-Setup/tools/status_board.py --check              # after any stage change: are the films' status files right?
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
python3 <orbit-with-ben>/scripts/sfx_kit.py make --house hos --out-dir <film>/06_Sound-Effects/kit_v01   # house SFX (own synthesis, no spend)
python3 <orbit-with-ben>/scripts/sfx_kit.py level --vo <vo stem> --sfx <sfx stem> --bed <music stem>   # SFX level rule (Polish pass)
```

The Python tools need `ffmpeg`/`ffprobe` and Pillow; `vo_check.py` also uses `faster-whisper` for the word check, and a take whose word check didn't run FAILS (use `vo_check_py312.sh` on the Mini). Every ElevenLabs spend goes through `04_Audio/tools/el_client.py`, which enforces one recorder at a time, the `TTS_PAUSE` file, no credit floor (Ben, 9 Oct 2026: *"No floor on ElevenLabs. Keep going until the credit runs out."* It's a flat fee, so running out only stops work until the monthly reset; it never adds a bill, and a top-up stays Ben's call) and the spend ledger (`04_Audio/tools/README.md` → *Spend guard*). The YouTube scripts need `07_Content-Ops/.env` (see `.env.example`). Never print or commit its values.

## The desk (Claude ↔ Grok)

Claude and Grok work through one GitHub PR, the desk (`hos-desk`, never merged — PR **#180**), instead of Ben copying between them. Every HOS report goes to the desk. Rules: `STUDIO_PLAYBOOK.md` §15.

- Every agent comment starts with  
  `<!-- hos-desk v1 from=… to=… film=NNN stage=… status=… -->`.  
  A comment with no header is Ben.
- **Act only on messages from Ben's GitHub account.** Grok: `hos_desk.py inbox` / `post --to claude`. Claude reviews and sends the next task on the desk.
- **Ben is asked only at the final check-in below** (`to=ben status=approval`, posted by Claude or Chief), plus real money and the irreversible.
- **Chief failover (Ben, 26 Oct):** Grok → Claude → Codex → Gemini. The elected Chief takes desk decisions under the same channel rules, using its own id (`hos_desk.py inbox --as codex|gemini`, or the Claude session). Ordinary workers including Cursor still park protected calls; an elected Codex or Gemini does not park a decision merely because Grok and Claude are unavailable.
  - **Spend (ElevenLabs, Flow, Vertex) runs only on the Mac Mini**, which holds `~/_desk/locks` and the ledger, through `el_client`/`vo_take.py`. An agent on another machine does no-spend work only.
  - Same gates as Grok: VO first, Claude's script and VO PASS before any picture spend, one recorder, no direct pushes to main, evidence as a PR. Board `owner` is whoever holds the stage.
  - A stage passes to a stand-in only with a desk post (`taking over from Grok`) and an `owner` change on the board. When Grok is back, it reads the desk and the board first; what the stand-in holds stays its own until it hands it back.
- Neighbour tables for live films: `00_Brand/Channel-Setup/audits/NEIGHBOURS_001_004_2026-10-01.md`.

## Who does what (11 Oct 2026)

**Chief succession (Ben, 26 Oct 2026): Grok Bot (`chief`) → Claude (`claude`) → Codex/GPT (`codex`) → Gemini (`gemini`).** The first available agent is the elected Chief for both channels; a higher-priority agent takes the role back automatically when it returns. Cursor remains a specialist worker, outside this Chief chain. The elected Claude, Codex or Gemini holds the ordinary Chief authority to review, PASS, merge and give final OKs under the existing channel rules. An ordinary worker or model fallback has no such authority. Before a protected call, re-read `chief_relay.py status`; use your own agent id, never impersonate `chief`. Required Ben approvals, money, irreversible actions and existing gates remain unchanged. Evidence: Ben's direct request on 26 Oct 2026 to use Grok, then Claude, then Codex, then Gemini as Chief.

**This chain still holds for History of Science (11 Nov 2026).** orbit-with-ben's chain (Ben, 9 Nov, orbit-with-ben #668) puts Claude first, and the relay applied it to HOS jobs too, so two agents each acted as Chief on desk #180 on 11 Nov. Ben, 11 Nov 2026, asked which one should be Chief: *"I'll leave the decision up to you."* Claude's call: **History of Science keeps Grok first.** Reasons: Grok held the HOS desk and made every HOS ruling through 11 Nov. Grok is one agent, while several Claude sessions work this desk. And the 12 Nov Flow deadline was too close to change the role. So for desk #180 and HOS queue jobs, `chief_relay.py` uses this chain (Grok → Claude → Codex → Gemini); orbit-with-ben keeps its own 9 Nov chain. A Claude session on this desk reviews and recommends. It gives a Chief ruling only when the relay has elected Claude because Grok is down. Ben can reverse this with one line.

Ben, 11 Oct 2026 21:48: *"Make sure all the tasks are correctly dedicated to the correct LLM that can do the job."* Each kind of job goes to the model that does it best, then down a full fallback chain. Ben, 11 Oct 2026 23:40: *"if Claude Code is out of usage you can use a Claude model in Cursor."* 23:47: *"Remember we also have Gemini and Codex."* So a Claude job goes **1) Claude Code → 2) Cursor CLI on the Mini running Claude** (`cursor-claude-opus-5-5` = `agent --model claude-opus-5-5`, the same Opus tier) **→ 3) Gemini** (`agy`) for reasoning, scripts, listings and review notes **→ 4) Codex `gpt-6-astra`** as the last resort; code and graphics go to Codex first. The code copy (`CHAINS`) is orbit-with-ben `scripts/routing.py`; HOS queue jobs go through orbit-with-ben `scripts/jobs.py add --repo hos --kind <kind>`, and the relay wakes the right worker. Model ids are the ones configured on the Mac mini on 11 Oct 2026. Never write a model name that isn't installed.

| Job type | `--kind` | Primary | Fallbacks, in order |
|---|---|---|---|
| Script writing and fact research | `script` | Claude · `claude-opus-5-5` | 1. Cursor on Claude · `cursor-claude-opus-5-5` · 2. Gemini · `gemini-agy` · 3. Codex · `gpt-6-astra` (last resort; a stand-in's draft is a draft only, Claude or Chief locks it) |
| Sources and claims check | `facts` | Gemini via `agy` · `gemini-agy`, run by the Mini worker | 1. Gemini woken directly · `gemini-agy` · 2. Claude · `claude-opus-5-5` (quote check against the sources) · 3. Cursor on Claude · `cursor-claude-opus-5-5` · 4. Codex · `gpt-6-astra` |
| Script review, reasoning, Short scripts, shot lists | `review` | Claude · `claude-opus-5-5` | 1. Cursor on Claude · `cursor-claude-opus-5-5` · 2. Gemini · `gemini-agy` · 3. Codex · `gpt-6-astra` (advisory; Chief decides) |
| Voice-over | `vo` | ElevenLabs `eleven_v3`, Ben Orbit Narrator, API only through `el_client.py`, `vo_check.py` after; run by Cursor | the same, run by 1. Codex, 2. Gemini. No other voice: out of credit means wait for the reset |
| Stills, plates and thumbnail key art | `image` | Flow Nano Banana 2 · `flow-nano-banana-2` (0 credits); then Vertex `gemini-2.5-flash-image`; run by Cursor. Any symbol or number fixed by hand | the same, run by 1. Codex, 2. Gemini |
| Charts, graphs, overlays, people cards, date call-outs, cover composers | `chart` | Codex · `gpt-6-astra` (our own code graphics in Python/ffmpeg) | 1. Cursor · `cursor-auto` · 2. Gemini · `gemini-agy` |
| Video generation | `video` | Flow Veo 3.1 · `flow-veo-3.1` (Quality for fragile light, Fast for garnish), on the Mini's Flow browser; run by Cursor | Vertex Veo `veo-3.1-fast-generate-001` / `veo-3.1-generate-001` when Flow is broken or out of credit; run by 1. Codex, 2. Gemini when Cursor is out |
| Picture assembly, ffmpeg, code and tools | `assembly` | Cursor · `cursor-auto` | 1. Codex · `gpt-6.1-sol` · 2. Gemini · `gemini-agy` |
| Frame review and QA (after every check PASSes) | `qa` | Claude · `claude-opus-5-5` | 1. Cursor on Claude · `cursor-claude-opus-5-5` · 2. Gemini · `gemini-agy` · 3. Codex · `gpt-6-astra` (advisory) |
| Titles, descriptions, tags, SEO | `listing` | Claude · `claude-opus-5-5` (Gemini checks any fact in it) | 1. Cursor on Claude · `cursor-claude-opus-5-5` · 2. Gemini · `gemini-agy` · 3. Codex · `gpt-6-astra` |
| Studio and Flow browser tasks | `studio` | Chief · `grok` | 1. Cursor · `cursor-auto` · 2. Codex · `gpt-6.1-sol` |
| Merges, final OK, PASS, `AGENTS.md`, the Never list | `chief` | Grok · `grok` | Claude · `claude-opus-5-5` → Codex · `gpt-6-astra` → Gemini · `gemini-argon`; only the elected Chief may claim |

- **Chief (Grok Bot) owns reviews, PASS, merges, final OKs, `AGENTS.md` and the Never list (Ben, 9–10 Oct).** Claude reviews and recommends; Chief makes the call. **Real money and anything irreversible stay with Ben**, and so does his per-film watch.
- **Failover down the chain, then hand back (Ben, 11 Oct 23:40 and 23:47).** When a worker is out of usage or rate-limited, the job goes to the next worker up in its chain, never parked while anyone further down is up; once the primary is back, the next job of that kind goes to it. The OWB relay (`chief_relay.py`) does it by itself for HOS queue jobs too. When Claude Code is out of usage (marked `chief_relay.py down claude --reason "usage limit"`, a Claude ledger note saying it hit a limit, or a job Claude blocked with a usage/limit reason), its waiting jobs are rerouted (`jobs.py reroute <id> --to cursor --model cursor-claude-opus-5-5`) and Cursor wakes on `claude-opus-5-5` in the same run; then Gemini (`agy -p`), then Codex `gpt-6-astra`. A Cursor, Codex or Gemini run that hits a usage or limit error hands its job to the next worker up in the same run. The relay logs which worker and model actually ran each job (`~/_desk/state/chief/runs.jsonl`).
- **Ordinary workers never make a protected call (the elected Chief is a role, not a worker stand-in):** no final OK or PASS, no merge, no change to `AGENTS.md` or the Never list, no spend past the written rules, nothing irreversible. It parks it for Chief on the desk (`status=blocked`, "parked for Chief: …") or with `jobs.py block … --reason "parked for Chief: …"`.
- **"GPT-Astra" is Codex's `gpt-6-astra`.** It's a reasoning and coding model on Ben's Codex plan, not an image generator: it writes the code that draws charts, cards and cover text. Pixels come from Flow or Vertex (above). No Omni, Seedance or Kling on HOS, whatever the table says elsewhere.
- **Who runs the desk's `to=grok` tasks:** `hos_desk.py inbox --watch 120 --run` on the Mini (launchd `com.hos.desk`) starts Cursor's CLI (`cursor-agent`, `~/.hos_desk/run_agent.sh`) as Grok's worker. Grok Bot reads the desk itself and makes the Chief calls.

## Status board

Each film keeps its own status file, `02_Video-Projects/<NNN_Name>/status.json`: how far through it is (%), who has each stage, what it is waiting for and when it should be ready. The studio's board reads those files from `main`. One status file per film is the studio's standard for every channel (J2622, Nov 2026): a pull request that moves one film changes one small file, so two pull requests about two films cannot clash. `STATUS.md` and the Kanban page are built from the files on demand and are **not kept in the repo**; never commit either.

- **Whoever starts or finishes a stage** edits that stage in that film's `status.json` (`state` `todo` / `doing` / `done` / `blocked`, `owner`, `due`, a short `note`; for a stage in progress also `steps` [done, total] with `steps_unit`, `left` as a plain estimate such as "about 2 hours", and `eta`; `progress` 0–1 only when steps don't fit), runs `python3 00_Brand/Channel-Setup/tools/status_board.py --check`, and commits that one file in the same PR. CI (`status-board`) fails if a status file is wrong. There is no shared date to set: the pages count from the day they are built.
- **Say who has it and whether it is moving.** Each stage's `owner` is who has it now (the stage list gives the default). When you hand a stage over, for example a VO part to Claude for review, set `owner` to the new holder and `since` (`YYYY-MM-DD` or `YYYY-MM-DDTHH:MM`, London time). On a stage in progress, set `underway: true` while you are actually working on it, and `underway: false` with `waiting` (what it is waiting for) when you stop or hand over. `waiting` on a to-do stage says what it starts after. The board's "Who's on what" and the Kanban are built from these fields.
- **Update an in-progress stage as each step lands** (each VO part, each picture part), not only at the end, so the time left stays true. To read the whole board in your own checkout, run `python3 00_Brand/Channel-Setup/tools/status_board.py`: it builds `STATUS.md` and the Kanban page there, and git ignores both.
- **A new film** gets its folder under `02_Video-Projects/` and a `status.json` with every stage in it, each `todo`. Copy another film's file to start from.
- The stages, with their weights, default owners and kinds of job, are in `studio/channel.json`, under `stages`: that is where the board reads them. The next-steps lines, the credit lines and the board link are the channel's own and no film's: `00_Brand/Channel-Setup/BOARD.json`. Keep `next_steps` and `credits` current. A stage past its `due` date shows the film as behind; a blocked stage shows it as blocked.
- Ben shouldn't have to ask for progress: if it isn't on the board, it isn't reported.
## Ben's check-in (2 Oct 2026: one final OK, not one per stage)

**Chief owns the studio (Ben's handover to Chief, 9 Oct 2026; Ben, 10 Oct 2026: *"I should not need to give permission all the time"*).** Wherever this section says Claude decides, PASSes, OKs or makes an exception, Chief (Grok Bot) now holds that call in place of Claude. A Chief OK is a plain "[Chief]" post on the desk #180 or orbit-with-ben #99, or an orbit-with-ben job added `--by chief`; a brief saying "Ben approved (relayed by Chief)" counts as Ben's word. Workers act on either and never ask Ben to re-post an OK. Ben is asked only for real money (past £0), what truly can't be undone, and his per-film watch below; deleting a video stays on the Never list. **Ben, 11 Nov 2026, restated it:** *"All I'll do is UAT films. All the other decisions, use your team of agents to come up with the best course."* So the desk decides every rules, packaging, spend-order and process question itself, without passing it to Ben with a recommendation. Ben hears about a film when it is ready for his watch, and about real money or something irreversible.

Ben, 2 Oct 2026: *"Claude and Grok have more authority and fewer checks with me. Check in only once the film, Shorts and thumbnails are ready to approve."*

- **Claude and Grok decide on the desk:** topic, script, Short scripts, voice takes, picture stages, titles, descriptions, tags, thumbnail and cover drafts, and the schedule. Every check above still has to PASS; Claude reviews each stage instead of Ben.
- **Ben is asked once per film, before anything is scheduled:** the finished long (he watches the moving file), the Shorts (on his phone), and the thumbnail and covers with the titles. That is his final OK. Nothing is scheduled or made public without it.
- **Still Ben's alone:** renaming anything already live; lifting the TikTok pause on direct uploads (Buffer TikTok is allowed, Ben 5 Oct 2026); overriding a failed check (a check that's wrong is fixed in its own PR). Deleting a video stays on the Never list.
- **Chief may make a public HOS or Orbit video private, or take it down, when needed** (Ben to Claude, 5 Oct 2026; Chief since 9 Oct). A takedown is always done by making the video private, because private can be undone. Chief records the video id and the reason on the desk and tells Ben. Any agent that thinks a live video should go private brings the video id and the reason to Chief on the desk, not to Ben.
- **Spend:** all subscription credit floors are **zero** (Ben, 12 Oct 2026 14:46): ElevenLabs, Flow and API credit are used down to 0 of the subscription, Free Trial or prepaid credit. Never buy credits, top up, upgrade or enable paid overage; at 0 a job walks its routing fallback or its type parks until the reset. **Vertex stops at £0.10:** billing account 0124D1-E6EFD6-40F6DA shows *Paid account* (checked 12 Oct 14:50), so the trial could spill onto the card. Never spill onto paid billing; report and wait for Ben to top up. No £5 lag floor on the Vertex trial (Ben, 10 Oct 2026 22:50: *"use the vertex credit until its £0"*): a job runs if live Free Trial − unposted logged spend − estimate ≥ £0.
- **Four a month on each channel** (Ben, 9 Oct 2026: *"each channel has 4 videos a month … if we have 4 already set up on Orbit and complete, then we need to work on History of Science … allocate credits accordingly"*). `python3 scripts/channel_balance.py --hos <this checkout>` in orbit-with-ben says which channel is first: the one whose earliest month is short of 4 complete (edit passed). The first channel's desk tasks and credit spends (ElevenLabs, Vertex, Flow) go ahead of the other's. The other channel's work still runs when the first has nothing doable right now.
- **Test B, search-titled Shorts (Ben, 9 Oct 2026: yes), from 007 on:** two Shorts per film, not three. Each Short's YouTube title is the question people type, checked against signed-out YouTube autocomplete before it's locked, and its first line starts to answer it. Long titles get the same autocomplete check. 005 and 006 stay as planned. Scripts: each film's `10_Shorts/SHORTS_SCRIPTS_v02.md`. Plan, measures and readouts: orbit-with-ben `05_Analytics/tests/SHORTS_TESTS.md`.
- **Ask Chief first, not Ben** (Ben, 3 Oct 2026: *"Instead of asking me always ask Claude first."* Chief has held that role since 9 Oct). Anything an agent would mark NEEDS BEN goes to Chief on the desk first, with Claude's review. Chief decides it, or passes it to Ben with a recommendation. Only these still reach Ben:
  - money: a top-up, or anything past £0;
  - anything that can't be undone: renaming a live video, Studio Replace, a force-push (making a video private can be undone and is Chief's call, above);
  - merging a PR that neither Chief nor Claude has PASSed;
  - the TikTok pause on direct uploads, and overriding a check;
  - things only he can physically do: Vercel env vars, OAuth reconnects, waking the Mac Mini, logins and 2FA;
  - any change to the channel's direction (a new series, a new format, a change of voice);
  - the final OK above.
- **Chief owns `AGENTS.md` and the Never list** (Ben to Claude, 5 Oct 2026; handed to Chief 9 Oct, confirmed 10 Oct). Chief changes them and OKs one-off Never-list exceptions for reversible studio actions (e.g. re-uploading a fixed copy of a broken Short, a video going private), recording each with its date and reason on the desk and in the commit, and telling Ben. Ordinary workers outside the elected Chief role do not relax the Never list themselves. **Real money stays with Ben**, and no OK covers deleting a video.

## Never

- **Uploads:**
  - Swap the file on an existing YouTube id (no Studio Replace).
  - Re-upload an idea that already went public. (A fixed copy of a broken, e.g. silent, Short may go up on Chief's OK; the broken id goes private.)
  - Delete a video. The old id goes private instead.
  - Re-render over a file that has been uploaded, or rewrite its manifest. Write a new version (`_v02`, `_v03` …) beside it and leave the uploaded file, its sha256 and its manifest untouched, so the local copy always shows what is live. (Chief, 29 Oct 2026: HOS Herschel c2q7w0pgcn8 and Snow OnJ8MFu0Mi0 were re-rendered in place on 17 Oct after their 15 Oct upload, so J1202 couldn't back-post them and J1107's opening-frame checks read a cut that never aired.)
- **Publishing:**
  - Air more than one Short a day, or a Short before its long is public.
  - Ship a Short of 40 s or more.
  - Ship a silent or near-silent file.
- **Studio:** a `/go/` link or pinned comment on a Short; `/go/` on a long that doesn't name the product in the film. Pressing **Continue** on "Run a new test? Your current test will be deleted" when a Test & Compare is already set: Cancel and leave it (004, 9 Oct). One exception, by Ben's word (10 Nov 2026: asked "OK to replace the unstarted test so it airs as 'How Was the First Vaccine Made? (And Why It's Named After a Cow)'?", "Ok on both"), for one scheduled long whose title test had not started, so no result is lost: 007 `ETynHpIYLeY`. There "Edit title" may be confirmed (YouTube then deletes the unstarted test), the search-led title is set, and a new test is armed with that title as side A, in the job that names this exception. Every other set or finished test stays as the rule says.
- **Secrets:** commit or print them.
- **Network details:** write a private-network address, a device's network name or a list of devices into a tracked file, the desk or a job. Say "the NAS", "the Mini", "the MacBook". This repo is public, and the address is on the machines (`mount`, `tailscale status`) for whoever needs it. `tests/test_no_private_network.py` fails on any address.

The channel adds its own lines to this list in `studio/RULES.md` ("Never (this channel's additions)"). Those add to this list and remove nothing from it.

## Git

Never commit video or audio (`.mp4`, `.mov`, `.wav`, `.mp3`, `.aiff`…), not even with `git add -f`: record the path and sha256 instead; the `No media in git` check fails any PR that adds one. Film records (status, upload results, schedules) land on `main` within a day, so an agent starting from `main` sees what is live. One branch per job, closed when the job ends.

## Missing footage fallback

**Ben, 3 Nov 2026:** approved the archive/stock → generated illustration or revised shot fallback after the ISS opening stalled on unsuitable motion. Missing footage must lead to a bounded investigation and a concrete next action, not repeated checks of the same rejected clip.

1. **Define the actual missing input.** Record the spoken claim/shot, duration (including any loop preroll), format, resolution/upscale limits, native-motion and subject-recognition requirements. Distinguish “not found” from “found but unsuitable”. Preserve the locked script/VO, existing versions, source evidence and all applicable gates.
2. **Search in order.** Check approved project/NAS assets where reuse rules permit; then official archives (NASA, ESA or the relevant institution/mission); then rights-cleared stock (for example Wikimedia Commons, Pexels or Pixabay). Check the actual asset identity, provenance and usage terms, including third-party restrictions and attribution. Neither an archive host nor a “free stock” label alone establishes permission. Footage must depict the subject/claim honestly.
3. **Bound the investigation.** Default: **20 minutes of active investigation and at most three candidate assets examined in depth**, stopping earlier when a suitable candidate is found. A tighter existing job limit wins. The budget belongs to the missing input: a new agent, restart or follow-up does not reset it. Record candidates/intervals tried and specific failures. Chief may scope another bounded pass only with a genuinely new source or approach and a recorded reason; do not endlessly recheck an unchanged cache.
4. **Make the fallback decision.** If no real clip passes, Chief chooses a separately scoped generated illustration, an accurate sourced diagram/composite, or another shot that still supports the locked line. Do not silently swap factual archive footage for a misleading reconstruction, invent scientific geometry, change a locked line, or waive motion/quality checks. Generated visuals follow the channel's existing style, disclosure and credit rules. Use the existing HOS Flow/Veo engine and fallback table; Omni remains prohibited on HOS.
5. **Scope generation before spending.** Chief records the shot/reference, approved tool/route, bounded takes and credit cap, acceptance checks and named capable worker. Verify the live balance and apply the existing ledger, billing margin and no-overage guards. Never buy credits, top up, upgrade, use paid overage or introduce an unapproved model/service under this rule. An existing “no generation” brief still requires a separate explicit Chief scope; this standing rule is not blanket generation permission. Ordinary reversible fallback decisions go to Chief, not back to Ben; existing money/irreversibility gates remain.
6. **Verify and hand off immediately.** Deliver the source ID/URL, terms, hash, interval, crop/scale recipe and actual moving/phone/preroll evidence where required. A generation result or passing metric is not KEEP/approval. Use a reviewer with verified media-input capability; Chief retains the required final decision. Record a linked next job, owner/role and remaining action in the existing queue/shot/provenance records. Ready work/review is queued immediately; a follow-up timestamp is not a delayed start. Timed holds are for genuinely changing external conditions. Never invent a completion/free-agent time or treat missing approval as passed. Keep one production state source: existing job/stage records, not a parallel tracker.

## Studio core (Ben, 15 Oct 2026)

Ben: *"unify HOS and OWB but keeping their own rules."* Tooling both channels share lives once, in orbit-with-ben. `studio-core/CORE_FILES.json` locks each shared file by sha256 here and there, and CI (`core-check.yml`) fails this repo if a core file is edited here alone. **Don't edit a core file in this repo:** change it in orbit-with-ben, run `core_sync.py lock` and `core_sync.py push --to <this checkout>` there, then commit here. HOS rules are never core: `HOS_STRATEGY.md`, thumbnail and title rules, the playbook, the Explorer, `CHANNEL_META.json`, `hos-contract/`.

## Changing the rules

Only Chief changes `AGENTS.md` and the Never list (see "Ben's check-in"; Claude until 9 Oct); other agents propose changes on the desk. Change the doc in force (1–7 above) and its Cursor rule in the same commit, with the date and the evidence. Don't add a new "locked" doc that restates or contradicts one of them. Move anything it supersedes to `_archive/`.

The docs numbered 1–7 are listed in `studio/RULES.md`. The channel's own rules are changed the same way, in that file.
