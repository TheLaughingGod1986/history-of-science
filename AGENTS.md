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
| `00_Brand/Channel-Setup/tools/` | `weekly_public_audit.py`, `gate_shorts_open.py` (Shorts ship gate), `thumb_preview.py` |
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
cd 07_Content-Ops && npm run review:script -- --file <script.md>          # long script must score ≥90
cd 07_Content-Ops && npm run gate:episode -- --project ../02_Video-Projects/<NNN_Slug>
python3 00_Brand/Channel-Setup/tools/gate_shorts_open.py check <short.mp4> --air-date YYYY-MM-DD
python3 00_Brand/Channel-Setup/tools/thumb_preview.py long|short <thumb.jpg> --out <sheet.jpg>
python3 04_Audio/tools/orbit_flow_veo_ui.py --start-frame <still.jpg> --prompt "…" --out <clip.mp4>
cd 07_Content-Ops && npm run youtube:package -- --package <…/11_Upload-Package> --video <mp4> --dry-run
cd 07_Content-Ops && npx tsx --env-file=.env scripts/retitle-videos.ts --file <fixes.json> --dry-run
cd 07_Content-Ops && npx tsx --env-file=.env scripts/update-pinned-comment.ts --dry-run
python3 00_Brand/Channel-Setup/tools/weekly_public_audit.py          # every Monday
```

The Python tools need `ffmpeg`/`ffprobe` and Pillow. The YouTube scripts need `07_Content-Ops/.env` (see `.env.example`). Never print or commit its values.

## Stop and ask Ben at each of these points

1. Topic
2. Long script (after it reaches 90)
3. Short scripts
4. Voice
5. Moving picture (never judge from stills)
6. Thumbnails
7. Anything that goes public, is renamed, or is deleted

## Never

- **Channels:** upload, schedule or post to Orbit With Ben, OpptiAI or the empty `@HistoryOfScience`. HOS is `@HistoryOfScienceYT` only.
- **Uploads:**
  - Swap the file on an existing YouTube id (no Studio Replace).
  - Re-upload an idea that already went public.
  - Delete a video. The old id goes private instead.
- **Publishing:**
  - Premiere a long (until subscribers are in the hundreds).
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
  - Veo Fast on fragile light (lamps, flasks, glows). Use Quality.
  - Paint-patching a plate instead of reminting it.
  - "Same DNA" or "lab DNA" in a Veo prompt.
  - Ken Burns or a still push when Flow is capped. Wait for the reset.
- **Voice:** a video model's speech as VO, or any voice other than Ben Orbit Narrator.
- **TikTok:** upload or retry while it's paused.
- **Secrets:** commit or print them.

## Git

Film records (status, upload results, schedules) land on `main` within a day, so an agent starting from `main` sees what is live. One branch per job, closed when the job ends.

## Changing the rules

Change the doc in force (1–7 above) and its Cursor rule in the same commit, with the date and the evidence. Don't add a new "locked" doc that restates or contradicts one of them. Move anything it supersedes to `_archive/`.
