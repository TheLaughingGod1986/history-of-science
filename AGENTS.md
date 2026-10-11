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
| `00_Brand/Channel-Setup/{Meta,TikTok,social}/` | Social: bios, the TikTok block file and the uniqueness/destination guards (posting is Buffer, below). Social posts go through Buffer only (HOS org, `BUFFER_HOS_API_KEY`). Direct TikTok uploads stay paused (`TikTok/TIKTOK_UPLOAD_BLOCK.json`); TikTok through Buffer is allowed (Ben, 5 Oct 2026). |
| `00_Brand/Brand-Guidelines/` | Brand snapshot, the Showrunner brief studio block |
| `01_Character/` | The Explorer bible, master sheet and generation reference |
| `02_Video-Projects/NNN_Slug/` | One folder per film. Start from `_template_NNN_Episode-Slug/`. |
| `04_Audio/tools/` | `orbit_voice.py` (VO settings), `orbit_flow_veo_ui.py` (Flow Veo), `orbit_cfr_delivery.py` (CFR export), SFX and music beds. The `orbit_` names are historical; the tools are shared. |
| `07_Content-Ops/` | Next.js ops app and CLIs: script review, episode gate, YouTube package upload, retitle, pinned comments |
| `docs/` | Tech notes (Veo, playback fixes, publishing adapters, affiliate) |
| `_archive/` | Superseded docs, rules, one-off scripts, old audits and the Orbit leftovers. **Ignore unless asked.** |

**Social posting (5 Oct 2026):** HOS Shorts go out through **Buffer via HOS Showrunner** only (`BUFFER_HOS_API_KEY`, HOS Buffer org). Never the Orbit Buffer org or the Buffer connector. YouTube stays in Studio. Long films are never cross-posted via Buffer. HOS Threads posting stops until Ben adds a Threads channel. Old Meta/Threads/TikTok CDP auto-post trees are under `_archive/00_Brand/Channel-Setup/`. Details: `STUDIO_PLAYBOOK.md` §12.

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
python3 <orbit-with-ben>/scripts/sfx_kit.py make --house hos --out-dir <film>/06_Sound-Effects/kit_v01   # house SFX (own synthesis, no spend)
python3 <orbit-with-ben>/scripts/sfx_kit.py level --vo <vo stem> --sfx <sfx stem> --bed <music stem>   # SFX level rule (Polish pass)
```

The Python tools need `ffmpeg`/`ffprobe` and Pillow; `vo_check.py` also uses `faster-whisper` for the word check, and a take whose word check didn't run FAILS (use `vo_check_py312.sh` on the Mini). Every ElevenLabs spend goes through `04_Audio/tools/el_client.py`, which enforces one recorder at a time, the `TTS_PAUSE` file, no credit floor (Ben, 9 Oct 2026: *"No floor on ElevenLabs. Keep going until the credit runs out."* It's a flat fee, so running out only stops work until the monthly reset; it never adds a bill, and a top-up stays Ben's call) and the spend ledger (`04_Audio/tools/README.md` → *Spend guard*). The YouTube scripts need `07_Content-Ops/.env` (see `.env.example`). Never print or commit its values.

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

## Teach on screen (Ben, 11 Oct 2026)

Ben, 11 Oct 2026 21:45, for every future video on both channels: *"add more graphs and charts when needed, more overlays, more animations, and more interesting facts to explain about dates, explain about the people we're mentioning, and make it more educational and more useful."* This applies to every script signed off and every picture part started after 11 Oct 2026. It builds on the teach labels (Ben, 20 Sep; `STUDIO_PLAYBOOK.md` §5 *The look*) and changes no locked rule. The premium 3D cartoon house style, white Didot italic, one label at a time, and "no flat poster or UI cards" all stand.

**Script.** Mark these inside the scene's `[VISUAL MUST: … · LABEL: …]`, the same way LABEL is marked, so `review:script` doesn't count them and `gate:episode` doesn't change. Chief counts them at script review (`grep -o "DATA:" <script> | wc -l`, and the same for each marker).
- **DATA: at least 3 in every long (aim for 3–5).** Wherever the VO gives a number, a measurement, a scale, a before-and-after or how something was measured, add `· DATA: <what the graphic shows>`. It's shown as an animated graphic in the house style: an ink chart that draws itself on period paper, a brass scale or gauge, a size comparison, or a counter. Every DATA number is in `FACT_NOTES` with its source.
- **A timeline in every long.** Every HOS film is a story of dates, so each long gets one animated timeline of its key dates. It builds as each date is said, it counts as one DATA moment, and later dates drop onto it.
- **WHO: a card for every named person at first mention.** Use `· WHO: <name> (<born>–<died>) — <role, 4 words or fewer>`, with the role as it was in the scene's year ("physics professor", not "Nobel laureate" before 1901). Later mentions get no card.
- **WHEN: every date or era that's said.** Add `· WHEN: <place, year>` for a place-and-year stamp (already allowed in the first 3 s), or a marker dropping onto the timeline.
- **FACT: 2–4 per long.** Each is one surprising, sourced fact, said in a line and shown as a card: `· FACT: <card text, 4 words or fewer>`. Make it a "huh, I didn't know that" beat, never a list.
- **Pictures are facts too.** All WHO, WHEN, DATA and FACT text goes on the script's new-claims list and is sourced in `FACT_NOTES` before picture, like any spoken claim.
- **Shorts (22–27 s): at most one overlay** (a fact card, a date stamp or a one-number scale), and only where it helps the line being said. It adds no words and no seconds, so the Short stays at 22–27 s and 55–65 words. It never appears in the first 2 s (frame 0 has the hook caption only) or over the 9–14 s title, and it stays inside the 16:9 centre band.

**Picture.**
- **All text is added in the edit,** never by Veo: plates carry no readable text, and garbled card text is a hard fail. In the plate board, the card's text goes in `side_label`, and a DATA graphic is named in the part's edit notes.
- **House style only.** Cards and charts are white Didot italic over the moving plate, or a soft cream-on-brown teach card that matches the end card, inked or drawn on. They're never a flat poster, a UI panel, a modern slide or infographic look, or photoreal. One label or card at a time; a WHO card counts as one (the name on line one, the years and role on line two, lower third, on screen 3–4 s while the name is spoken).
- **Everything animates.** A chart draws in time with the spoken number. A card fades or inks in over about 0.3–0.6 s, then out again. An overlay counts toward continuous motion only when it animates over a moving plate, never over a still or a freeze. No card holds still for more than 4 s, and a card is never Ken-Burned (that Never still stands). Never two full-frame teach graphics back to back: a moving plate comes between them.
- The text stays off the hero object and the Explorer, and the cards never cover the picture that explains the line (the mute test still applies).

**Review gate.** Chief's frame review and stills check score each item PASS or FAIL in the desk report, alongside the UAT hard fails, before the cut goes to Ben's watch:
1. **DATA:** a long has 3 or more animated data moments, including the timeline. Each matches its line, reads with the sound off, and shows the same number as `FACT_NOTES`.
2. **WHO:** every named person has a card at first mention, with sourced years and a role right for the year.
3. **WHEN:** every spoken date or era has a stamp or a timeline marker.
4. **FACT:** a long has 2–4 fact beats, each one sourced.
5. **STYLE:** house style, white Didot italic or a cream teach card, 4 words or fewer per label, one at a time, added in the edit, with no flat poster or UI card, off the hero and the Explorer. A Short's overlay sits inside the 16:9 band, clear of 0–2 s and the 9–14 s title.
6. **MOTION:** every overlay and chart animates in over moving picture, none holds still for more than 4 s, and no two full-frame teach graphics run back to back.

A Short is scored on 5 and 6 only, plus whichever of 1–4 its single overlay is, if it has one. Any FAIL goes back to the plate board or edit before Ben's watch.

**What it applies to.**
- **All four markers before VO:** 009 and 010. Their scripts are signed off but have no VO yet, so the markers go inside `[VISUAL MUST]` with no spoken word changed, the score is unchanged, and the new card text is fact-checked into `FACT_NOTES`. New FACT lines wait for the next script.
- **Cards and timeline added in the edit:** 006 (picture under way, edit not started), 007 and 008 (VO locked, picture not started). They ride lines that are already recorded, with no VO change.
- **Every rule from the start:** topics picked after 11 Oct (011 on).
- **No rework:** 004 and 005 are finished and scheduled.

## Polish pass (Astrum ref, 11 Oct 2026)

Ben, 11 Oct 2026 22:17, sent Astrum's *What Is It Like on the Surface of a Black Hole Planet?* (`PxJSOWyYWkc`, 27 min, 1.1M views) as a style reference for both channels: *"let me know what you think we can incorporate into our workflow."* Chief adopted five of its techniques the same night. They apply to every picture part and edit started after 11 Oct 2026, in the HOS house style. **Where an Astrum technique meets a HOS lock, the HOS lock wins**: the premium 3D cartoon look, white Didot italic, one label at a time, no flat poster or UI cards, the UAT hard fails and the first-minute timings all stand.

**Not adopted:** Astrum's long shot holds (6–8 s, some 15 s). The picture still changes every 4–6 s, no card holds still for more than 4 s, and length still comes from narration, not holds.

**1. Sound design (SFX).**
- **Three kinds, where the shot calls for them,** on top of the period foley we already lay (ward walla, glass, wood):
  - a low rumble under a violent or huge moment (an eruption, a storm, a blast, a vast reveal);
  - a soft whoosh on a fast camera move or a dive (into a lens, through a room);
  - a pen-tap tick when a card, chart line or timeline marker inks in. It's never a digital UI blip, because HOS has no UI look.
- **Source: our own house kit.** Run orbit-with-ben `python3 scripts/sfx_kit.py make --house hos --out-dir <film>/06_Sound-Effects/kit_v01` (it writes `rumble_low`, `whoosh_soft` and `tick_ink`). It synthesises the sounds itself, so there are no samples, no licence to track and no spend. The Mac mini has no licensed SFX library (checked 11 Oct).
  - A free library may be added only if its licence allows commercial YouTube use with no attribution. Record it in the film's `06_Sound-Effects/SOURCES.md`. Nothing is bought.
  - ElevenLabs SFX (`generate_sfx_from_script.py`) spends the shared credit through `el_client`, so it waits for the 30 Oct reset and Chief's OK.
  - Never use Veo's own audio (silent picture).
- **Restraint:** no whoosh on plain cuts or on every card, at most one tick every 0.5 s, and no cartoon whooshes or comedy stings.
- **Level rule.** SFX sit under the VO, like the bed. Keep VO, music and SFX as separate stems for each part, and orbit-with-ben `python3 scripts/sfx_kit.py level --vo <vo stem> --sfx <sfx stem> --bed <music stem> --minutes <length>` must PASS:
  - the SFX stem is at least 12 LU under the VO's integrated loudness;
  - while the VO speaks, the SFX and the bed are each at least 10 LU under the VO;
  - in a VO pause, the SFX stay at least 6 LU under the VO's integrated loudness.

  The VO's −19 to −28 dB mean and bed parity (about −20 dB mean under the VO across parts) stay as they are.

**2. Music by part.**
- Each part's music follows what the part does: an ambient drone under wonder and discovery beats, and a light rhythmic or arpeggiated cue (plucked strings, a soft harpsichord or celesta figure that suits the period) under the "how it works" teach.
- **Credit hold:** until the 30 Oct reset, no new bed starts without Chief's OK. So the free way is one bed whose prompt asks for both moods, with its sections laid at the part cards. A second cue counts as a new bed.
- The music changes at a part or chapter card with a 2–4 s crossfade. The music covers the full runtime, never drops out, and keeps bed parity.
- Shorts keep one bed for their full length (R8).

**3. Explainer look.** For a mechanism (how a lens bends light, why a vaccine works), use the *Teach on screen* house style, not a new picture style: an inked diagram that draws itself on period paper, or a cream-on-brown teach card.
- **No glowing grid, no flat UI, poster or infographic look.** That's Orbit's look, and the HOS lock wins.
- The plates keep **one style per part**. The diagram is a teach graphic inside it, never a second rendering style.
- Text is added in the edit (never by Veo), and garbled letters still hard-fail.
- One label at a time. Never two full-frame teach graphics back to back: a moving plate comes between them.

**4. Script.**
- **Every big number gets a scale.** Give it a plain comparison or an everyday analogy in the same or the next sentence ("smaller than a grain of salt"). Mark it on its DATA marker: `· DATA: <graphic> · SCALE: <comparison>`. The comparison goes on the new-claims list and into `FACT_NOTES` like any spoken claim, and it's right for the year in the scene.
- **The hook doesn't change.** HOS keeps its first-minute timings, which are stricter than Astrum's question by 0:50: the answer image by 0:05, the title question by 0:08, the promise by 0:15, the stakes by 0:25, and the first real fact before 0:45.
- **Word counts don't change:** about 1,200–1,300 spoken words, and `review:script` at 90 or more. An analogy replaces words; it doesn't add them. Shorts stay at 55–65 words.

**5. Finishing.**
- **Crossfades** of 0.5–1.5 s between scenes where the move suits (a change of place or year). Hard cuts elsewhere; they're not required on every cut. A crossfade never stretches a shot past the 4–6 s picture change, and part cards keep their 0.5–0.8 s breath before the crossfade.
- **Fine film grain** only on dark gradients that band (night skies, dim rooms, lamp fall-off). It's a uniform layer in the edit, never paint-patching, and never an old-film or scratched look over the 3D cartoon.
- **Depth of field:** only the gentle background softness asked for in the plate prompt. No blur added in post, never on the hero object or the Explorer, and never on late shots. UAT hard fail 7 (no heavy blur) wins.
- **Corner credit labels:** none on our own 3D cartoon plates (the altered-content setting on upload covers that). A real archive image (a photograph, painting or manuscript) gets a small credit line in white Didot italic, bottom-left. It waits while any other label or card is on screen, because one label at a time wins. Shorts carry none.

**Review gate.** Chief adds six items to the frame review and stills check, scored PASS or FAIL in the desk report alongside the UAT hard fails:
1. **SFX:** `sfx_kit.py level` PASSes for each part, and the rumbles, whooshes and ink ticks sit on shots that call for them.
2. **MUSIC:** the music changes between wonder and teach parts at least once, at a card, with full-runtime cover and bed parity.
3. **GRAIN:** dark gradients show no banding, and no grain reads as an old-film effect.
4. **SCALE:** every DATA number has its SCALE comparison, spoken and in `FACT_NOTES` (`grep -c "SCALE:"` is at least the DATA count).
5. **EXPLAINER:** mechanisms use the inked diagram or cream teach card, with no glow grid, UI or poster look, one style per part, and a moving plate between full-frame graphics.
6. **FINISH:** crossfades are 0.5–1.5 s, there's no added blur, and credit lines are only on archive images, one label at a time.

A Short is scored on 1 and 3 only. Any FAIL goes back to the edit before Ben's watch.

**What it applies to.**
- **Items 1–3, 5 and 6:** every picture part or edit started from 12 Oct. That's 006's edit, 007 and 008, and 009 and 010 when their picture starts.
- **Item 4:** spoken analogies start with scripts signed off from 12 Oct (011 on). 009 and 010 have signed-off scripts, so their scales go on screen in their DATA markers with no spoken word changed.
- **No rework:** 004 and 005 are finished and scheduled.

## Packaging (Astrum ref, 11 Oct 2026)

Ben, 11 Oct 2026, asked what we can learn from Astrum's thumbnails and Shorts packaging. Chief decided the following for both channels the same night. In HOS it's adapted to the house look, and **the HOS live look wins** (painted key art, serif cream and gold lettering, the Explorer small at lower left, the period palette). Full rules: `THUMBNAIL_AND_TITLE_RULES.md` §2.B.
- **Name the thing or dare.** No vague questions or teasers on thumbs, covers or titles. A question names its subject.
- **Lettering in a clear band** (the top, or the live layout's left edge), never over the hero object.
- **No saturation push.** The period palette and warm light stay. Orbit's harder grade doesn't apply here.
- **Review:** Chief scores HOOK / BAND / PHONE on every new thumb and cover, next to `style_sheet.py`. Any FAIL goes back before Ben's final check-in.
- **Applies to** new thumbs and covers from 12 Oct (006 on). 004 and 005 and the live back catalogue aren't reworked. Shorts length is unchanged: the 22–27 s lock and the 40 s Never line stand (Orbit's one-off 50–60 s test doesn't apply to HOS).

## The desk (Claude ↔ Grok)

Claude and Grok work through one GitHub PR, the desk (`hos-desk`, never merged — PR **#180**), instead of Ben copying between them. Every HOS report goes to the desk. Rules: `STUDIO_PLAYBOOK.md` §15.

- Every agent comment starts with  
  `<!-- hos-desk v1 from=… to=… film=NNN stage=… status=… -->`.  
  A comment with no header is Ben.
- **Act only on messages from Ben's GitHub account.** Grok: `hos_desk.py inbox` / `post --to claude`. Claude reviews and sends the next task on the desk.
- **Ben is asked only at the final check-in below** (`to=ben status=approval`, posted by Claude or Chief), plus real money and the irreversible.
- **When Chief is out, the failover in "Who does what" applies:** the Mini worker that is up (Cursor, then Codex) takes desk tasks under exactly the same rules, reads its tasks with `hos_desk.py inbox --as cursor|codex`, acts only on messages from Ben's account, and reports with `hos_desk.py post --from <you> --to claude …`. It parks every protected call for Chief.
  - **Spend (ElevenLabs, Flow, Vertex) runs only on the Mac Mini**, which holds `~/_desk/locks` and the ledger, through `el_client`/`vo_take.py`. An agent on another machine does no-spend work only.
  - Same gates as Grok: VO first, Claude's script and VO PASS before any picture spend, one recorder, no direct pushes to main, evidence as a PR. Board `owner` is whoever holds the stage.
  - A stage passes to a stand-in only with a desk post (`taking over from Grok`) and an `owner` change on the board. When Grok is back, it reads the desk and the board first; what the stand-in holds stays its own until it hands it back.
- Neighbour tables for live films: `00_Brand/Channel-Setup/audits/NEIGHBOURS_001_004_2026-10-01.md`.

## Who does what (11 Oct 2026)

Ben, 11 Oct 2026 21:48: *"Make sure all the tasks are correctly dedicated to the correct LLM that can do the job."* Each kind of job goes to the model that does it best, with one backup. The code copy is orbit-with-ben `scripts/routing.py`; HOS queue jobs go through orbit-with-ben `scripts/jobs.py add --repo hos --kind <kind>`, and the relay wakes the right worker. Model ids are the ones configured on the Mac mini on 11 Oct 2026. Never write a model name that isn't installed.

| Job type | `--kind` | Primary | Backup |
|---|---|---|---|
| Script writing and fact research | `script` | Claude · `claude-opus-5-5` | Codex · `gpt-6-astra` (draft only; Claude or Chief locks it) |
| Sources and claims check | `facts` | Gemini via `agy` · `gemini-agy`, run by the Mini worker | Claude · `claude-opus-5-5` (quote check against the sources) |
| Script review, reasoning, Short scripts, shot lists | `review` | Claude · `claude-opus-5-5` | Codex · `gpt-6-astra` (advisory; Chief decides) |
| Voice-over | `vo` | ElevenLabs `eleven_v3`, Ben Orbit Narrator, API only through `el_client.py`, `vo_check.py` after; run by Cursor | the same, run by Codex. No other voice: out of credit means wait for the reset |
| Stills, plates and thumbnail key art | `image` | Flow Nano Banana 2 · `flow-nano-banana-2` (0 credits); then Vertex `gemini-2.5-flash-image`; run by Cursor. Any symbol or number fixed by hand | the same, run by Codex |
| Charts, graphs, overlays, people cards, date call-outs, cover composers | `chart` | Codex · `gpt-6-astra` (our own code graphics in Python/ffmpeg) | Cursor · `cursor-auto` |
| Video generation | `video` | Flow Veo 3.1 · `flow-veo-3.1` (Quality for fragile light, Fast for garnish), on the Mini's Flow browser | Vertex Veo `veo-3.1-fast-generate-001` / `veo-3.1-generate-001` when Flow is broken or out of credit |
| Picture assembly, ffmpeg, code and tools | `assembly` | Cursor · `cursor-auto` | Codex · `gpt-6.1-sol` |
| Frame review and QA (after every check PASSes) | `qa` | Claude · `claude-opus-5-5` | Codex · `gpt-6-astra` (advisory) |
| Titles, descriptions, tags, SEO | `listing` | Claude · `claude-opus-5-5` (Gemini checks any fact in it) | Codex · `gpt-6-astra` |
| Studio and Flow browser tasks | `studio` | Chief · `grok` | Cursor · `cursor-auto` |
| Merges, final OK, PASS, `AGENTS.md`, the Never list | `chief` | Chief · `grok` | none: parked for Chief |

- **Chief (Grok Bot) owns reviews, PASS, merges, final OKs, `AGENTS.md` and the Never list (Ben, 9–10 Oct).** Claude reviews and recommends; Chief makes the call. **Real money and anything irreversible stay with Ben**, and so does his per-film watch.
- **Failover, then hand back (Ben).** When the primary hits its limit, the backup takes the job. Once the primary is up again, the next job of that kind goes back to it. When Claude hits its usage limit, Chief re-adds its waiting job as `--kind <kind> --for codex`, then back to Claude after its reset.
- **A stand-in never makes a protected call:** no final OK or PASS, no merge, no change to `AGENTS.md` or the Never list, no spend past the written rules, nothing irreversible. It parks it for Chief on the desk (`status=blocked`, "parked for Chief: …") or with `jobs.py block … --reason "parked for Chief: …"`.
- **"GPT-Astra" is Codex's `gpt-6-astra`.** It's a reasoning and coding model on Ben's Codex plan, not an image generator: it writes the code that draws charts, cards and cover text. Pixels come from Flow or Vertex (above). No Omni, Seedance or Kling on HOS, whatever the table says elsewhere.
- **Who runs the desk's `to=grok` tasks:** `hos_desk.py inbox --watch 120 --run` on the Mini (launchd `com.hos.desk`) starts Cursor's CLI (`cursor-agent`, `~/.hos_desk/run_agent.sh`) as Grok's worker. Grok Bot reads the desk itself and makes the Chief calls.

## Status board

`STATUS.md` (repo root) is Ben's one view of every film: how far through it is (%), what is being worked on now, what is next, when it should be ready, and the credit left. It is generated from `00_Brand/Channel-Setup/PIPELINE.json`; never edit `STATUS.md` by hand.

- **Whoever starts or finishes a stage** edits that film's entry in `PIPELINE.json` (status `todo` / `doing` / `done` / `blocked`, `owner`, `due`, a short `note`; for a stage in progress also `steps` [done, total] with `steps_unit`, `left` as a plain estimate such as "about 2 hours", and `eta`; `progress` 0–1 only when steps don't fit), sets `updated`, runs `python3 00_Brand/Channel-Setup/tools/status_board.py`, and commits both files in the same PR. CI (`status-board`) fails if they don't match.
- **Say who has it and whether it is moving.** Each stage's `owner` is who has it now (the stage list gives the default). When you hand a stage over, for example a VO part to Claude for review, set `owner` to the new holder and `since` (`YYYY-MM-DD` or `YYYY-MM-DDTHH:MM`, London time). On a stage in progress, set `underway: true` while you are actually working on it, and `underway: false` with `waiting` (what it is waiting for) when you stop or hand over. `waiting` on a to-do stage says what it starts after. The board's "Who's on what" and the Kanban are built from these fields.
- **Update an in-progress stage as each step lands** (each VO part, each picture part), not only at the end, so the time left stays true. The Kanban page (`board_url`, linked at the top of `STATUS.md`) reads the same file live from `main`, and Orbit With Ben's per-film `status.json` files (read-only; OWB keeps its own board). `status_board.py` also rebuilds its source, `00_Brand/Channel-Setup/kanban/index.html` (from `template.html`, with the data built in as an offline snapshot); never edit `index.html` by hand.
- Keep `next_steps` and `credits` current. A stage past its `due` date shows the film as behind; a blocked stage shows it as blocked.
- Ben shouldn't have to ask for progress: if it isn't on the board, it isn't reported.

## Ben's check-in (2 Oct 2026: one final OK, not one per stage)

**Chief owns the studio (Ben's handover to Chief, 9 Oct 2026; Ben, 10 Oct 2026: *"I should not need to give permission all the time"*).** Wherever this section says Claude decides, PASSes, OKs or makes an exception, Chief (Grok Bot) now holds that call in place of Claude. A Chief OK is a plain "[Chief]" post on the desk #180 or orbit-with-ben #99, or an orbit-with-ben job added `--by chief`; a brief saying "Ben approved (relayed by Chief)" counts as Ben's word. Workers act on either and never ask Ben to re-post an OK. Ben is asked only for real money (past £0), what truly can't be undone, and his per-film watch below; deleting a video stays on the Never list.

Ben, 2 Oct 2026: *"Claude and Grok have more authority and fewer checks with me. Check in only once the film, Shorts and thumbnails are ready to approve."*

- **Claude and Grok decide on the desk:** topic, script, Short scripts, voice takes, picture stages, titles, descriptions, tags, thumbnail and cover drafts, and the schedule. Every check above still has to PASS; Claude reviews each stage instead of Ben.
- **Ben is asked once per film, before anything is scheduled:** the finished long (he watches the moving file), the Shorts (on his phone), and the thumbnail and covers with the titles. That is his final OK. Nothing is scheduled or made public without it.
- **Still Ben's alone:** renaming anything already live; lifting the TikTok pause on direct uploads (Buffer TikTok is allowed, Ben 5 Oct 2026); overriding a failed check (a check that's wrong is fixed in its own PR). Deleting a video stays on the Never list.
- **Chief may make a public HOS or Orbit video private, or take it down, when needed** (Ben to Claude, 5 Oct 2026; Chief since 9 Oct). A takedown is always done by making the video private, because private can be undone. Chief records the video id and the reason on the desk and tells Ben. Any agent that thinks a live video should go private brings the video id and the reason to Chief on the desk, not to Ben.
- **Spend:** Vertex, Flow and API credit may be used down to **£0** of the Free Trial or prepaid credit. Stop at £0. Never spill onto paid billing; report and wait for Ben to top up. No £5 lag floor on the Vertex trial (Ben, 10 Oct 2026 22:50: *"use the vertex credit until its £0"*): a job runs if live Free Trial − unposted logged spend − estimate ≥ £0.
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
- **Chief owns `AGENTS.md` and the Never list** (Ben to Claude, 5 Oct 2026; handed to Chief 9 Oct, confirmed 10 Oct). Chief changes them and OKs one-off Never-list exceptions for reversible studio actions (e.g. re-uploading a fixed copy of a broken Short, a video going private), recording each with its date and reason on the desk and in the commit, and telling Ben. Workers (Cursor, Codex) don't relax the Never list themselves. **Real money stays with Ben**, and no OK covers deleting a video.

## Never

- **Channels:** upload, schedule or post to Orbit With Ben, OpptiAI or the empty `@HistoryOfScience`. HOS is `@HistoryOfScienceYT` only.
- **Uploads:**
  - Swap the file on an existing YouTube id (no Studio Replace).
  - Re-upload an idea that already went public. (A fixed copy of a broken, e.g. silent, Short may go up on Chief's OK; the broken id goes private.)
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
- **Studio:** a `/go/` link or pinned comment on a Short; `/go/` on a long that doesn't name the product in the film. Pressing **Continue** on "Run a new test? Your current test will be deleted" when a Test & Compare is already set: Cancel and leave it (004, 9 Oct).
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
- **TikTok:** a direct upload or retry (browser/CDP or API) while `TIKTOK_UPLOAD_BLOCK.json` is paused. HOS TikTok goes through Buffer only (Ben, 5 Oct 2026).
- **Social:** post HOS via the Orbit Buffer org or the Buffer connector; revive archived Meta/Threads/TikTok `live_shorts_to_*` / launchd auto-post.
- **Secrets:** commit or print them.

## Git

Never commit video or audio (`.mp4`, `.mov`, `.wav`, `.mp3`, `.aiff`…), not even with `git add -f`: record the path and sha256 instead; the `No media in git` check fails any PR that adds one. Film records (status, upload results, schedules) land on `main` within a day, so an agent starting from `main` sees what is live. One branch per job, closed when the job ends.

## Changing the rules

Only Chief changes `AGENTS.md` and the Never list (see "Ben's check-in"; Claude until 9 Oct); other agents propose changes on the desk. Change the doc in force (1–7 above) and its Cursor rule in the same commit, with the date and the evidence. Don't add a new "locked" doc that restates or contradicts one of them. Move anything it supersedes to `_archive/`.
