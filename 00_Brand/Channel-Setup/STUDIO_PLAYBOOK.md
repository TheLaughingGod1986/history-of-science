# History of Science — studio playbook

How to make a History of Science film, from topic to the week after it's live. Written 25 Sep 2026. It replaces:
- the UAT bible house lock (8–9 Sep);
- the studio plate-library lock and runbook (9–10 Sep);
- the house VO and teach lock (7 Sep);
- the teaching density, silent-readable picture and no-DNA-helix locks (20–21 Sep, previously only on branches);
- the Part 01 style baseline, microbe, open/out and Explorer locks;
- Growth System v2, the retention lock, the long-form gate and the Omni playbook;
- the 34 old Cursor rules.

Those are in `_archive/` for history only. Every rule they held that still applies is below.

**What to make** (the week, hooks, measure) is `HOS_STRATEGY.md`. **Titles and thumbnails** are `THUMBNAIL_AND_TITLE_RULES.md`. This file is **how** to build and ship. Where they overlap, the order of precedence is in `AGENTS.md`.

---

## 1. The week

| Slot (UK) | What |
|---|---|
| Thu 18:00 | One long, 7–9 min, **normal publish (no Premiere)** |
| Fri · Sun · Tue 11:30 | Three Shorts, 22–27 s. Friday promotes the new long; Sunday and Tuesday promote two other films. |

- Never more than one Short a day. Never a Short before its long is public.
- Never a second long on a subject that already has a public long.

## 2. Pick the topic (before any script)

1. **Use the channel's data:** the latest `audits/weekly/<date>/REPORT.md` and `audits/SHORTS_LOG.md`.
2. **The lane** (`HOS_STRATEGY.md`): a familiar thing, and the moment we found out the truth about it. One person to follow, one room to set it in, one proof.
3. **Competition check:** search the exact title signed out. If the top five are all channels with millions of subscribers, narrow the angle.
4. **Score it:** `templates/TOPIC_OPPORTUNITY_SCORE.md`.
5. **Pre-build vidIQ audit:** copy `PRE_BUILD_VIDIQ_AUDIT_TEMPLATE.md` to the project's `11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md`.
6. **Scaffold:** copy `02_Video-Projects/_template_NNN_Episode-Slug/` to `02_Video-Projects/NNN_Slug/`.
7. **Ben picks.**

## 3. Script

### Long (7–9 min, about 1,000–1,300 spoken words, 5 parts)

- **First 3 s of picture:** the story itself. No logo, no bumper, no title card. A place-and-year stamp is fine.
- **Sentence one is the promise.** By 30 s the viewer knows the old belief, that it is about to break, and why it matters.
- **5 acts, one per part,** told as cause and effect. Each act: entry, show, one teach, turn, exit.
- **Clear before clever** (Ben, 7 Sep). A first-time viewer can say the one idea out loud after each beat:
  - name the thing (person, element, tool, place) in plain words;
  - say what it is and why it mattered in the same breath;
  - concrete nouns when teaching; poetry only after the fact is clear;
  - one idea at a time; change the beat before attention drops.
- **Always answer why the discovery was groundbreaking:** what became possible that was impossible before.
- **The Explorer is in 1–3 beats per film** (about every 3–5 scenes), walking through, touching a prop, reacting, then leaving.
- **Every number and claim is sourced.** Sources go in the description.
- **No goodbye, no subscribe ask in the script.** The last line hands off to the next film.
- **Markers:** every scene carries `[VISUAL MUST: …]` and `[TEACH: …]`. Explorer beats carry `[EXPLORER ACTS: …]`. Acts start with `[CHAPTER CARD: …]`.
- **Gates (both before any voice or picture spend):**
  ```bash
  cd 07_Content-Ops && npm run review:script -- --file <script.md>        # 90 or more
  npm run gate:episode -- --project ../02_Video-Projects/<NNN_Slug>       # PASS
  ```

### Short (22–27 s, about 55–65 words)

- **Two lines, then one hard fact** (`HOS_STRATEGY.md` → *Short hook*).
- **The first two seconds:** start mid-action; the named thing at frame 0, moving; the first words are the claim; a visible change by 1 s; a 2–4 word hook caption on frame 0; the Explorer never at frame 0.
- **The promoted film's exact live title** on screen at 9–14 s. The last 4 s loop back to the opening picture. Captions throughout.
- Shorts are cut from the film's own picture and VO wherever possible. The long-form reviewer caps Shorts below 90; don't pad a Short to chase it.

## 4. Voice

- **ElevenLabs "Ben Orbit Narrator" only.** Voice id `kDch6ACCIpqgQ0NsU9kk`. Settings from `04_Audio/tools/orbit_voice.py`.
- British spelling and pronunciation. Warm, upbeat, clear. Never a trailer voice.
- **VO before picture.** Speech around −19 to −28 dB mean. **A silent or stripped narration never ships.**
- Never use a video model's own speech as VO.

## 5. Picture

### Engine

| Job | Tool |
|---|---|
| Moving plates | **Google Flow, Veo 3.1**, start-frame image-to-video: `python3 04_Audio/tools/orbit_flow_veo_ui.py --start-frame <still.jpg> --prompt "…" --out <clip.mp4>` |
| Fragile light (lamps, flasks, glows, anything emissive) | **Veo 3.1 Quality**. Never Fast. |
| Low-risk motion garnish | Veo 3.1 Fast |
| Fallback, only when Flow is broken | Gemini API `orbit_gemini_veo.py` with `veo-3.1-lite-generate-preview` or `veo-3.1-generate-preview` (not the Fast API model: its quota 429s) |

- **Auth:** the Mac Mini CDP worker on `benoats@googlemail.com` (AI Ultra) only. Never `benoats86` or a prepaid-dry account for HOS Veo. If Flow asks for a passkey or signs out, stop and report; don't work around it.
- **Daily Flow limits** can block even with credits left. Wait for the reset. Never ship Ken Burns or a still push as a substitute.
- No Omni, Seedance, Kling or ElevenLabs Image & Video on HOS.

### Plate library (how a part gets made)

1. **Plate board first.** Each part has `07_Edit-Project/parts/part-NN_plates_v01.json`: one plate per VO beat with `vo_land` (the line it lands on), `prompt`, `explorer`, `side_label`, plus the part's `forbidden` and `always_fails` lists.
2. **Seed each plate from the last KEEP plate** in the same set (and the Explorer sheet when he is in it). Say "same Würzburg lab" or "same 1895 ward" for continuity; **never "same DNA" or "lab DNA" in a Veo prompt** (it paints a helix).
3. **One plate at a time until the first KEEP,** then mint the easier plates in parallel.
4. **After two FAILs with the same framing, change the framing or start frame.** Don't just prompt harder.
5. **Plate UAT on continuous playback,** start, middle and end of the clip, never from a still. Crop-reject anything off-model at the edges.
6. **Assemble a rough cut only when every plate has passed.**
7. **Never paint-patch** (temporal median, brightness paint) Explorer, desks or light sources. Remint instead.
8. Showrunner briefs include the studio block from `00_Brand/Brand-Guidelines/HOS_SHOWRUNNER_BRIEF_TEMPLATE_STUDIO.md`.

### The look

- **Premium finished 3D cartoon** (Animistry-class), warm cinematic light, period worlds. Not photoreal, not flat 2D, not modern-hospital inserts in a Victorian minute. One style per part.
- **Picture tells the VO with the sound off** (Ben, 21 Sep). If the line names a cover, a glow, a test, a hand, a ring, that action is on screen in that window, not 5–10 s later. Pretty B-roll under a teaching line fails.
- **Teach labels** (Ben, 20 Sep): when the VO introduces a person, a place or year, a tool, a science idea or a why-it-matters turn, put an elegant white Didot italic **side label** (1–4 words, one at a time) or a short teach card on that beat. Labels support the picture; they don't replace it. No flat poster or UI cards. Never two labels at once.
- **Continuous motion.** Never end or pad on a still, a still-zoom or a freeze.
- **Silent picture.** Strip Veo audio. No readable text or logos in generated plates, except the Explorer's locked book title. Text is added in the edit.
- **Never:** reuse a cutscene inside one film, loop scenery to pad, slow-mo stretch, freeze-pad, or Ken-Burns a card.

### Hard fails on every cut (the UAT bible)

Any one of these fails the cut. Check them on continuous playback.

1. **Consistency:** the Explorer's scale and teal coat, the props, the period and the 3D cartoon style match the locked earlier parts.
2. **Picture explains the VO** (the mute test above).
3. **Explorer round glasses** whenever he is visible.
4. **Explorer face and hair finished:** a full crown of hair, no bald patch, no melted face smear, no black dots in the scalp.
5. **Lamps are a clean warm glow.** No flame spit, smoke, or molten "lava" drip under the bulb. Frame lamps so the underside bulb and shade cup aren't visible.
6. **Readable cards.** Cards and papers carry readable writing or symbols. Blank hero cards and garbled letters fail.
7. **Late shots sharp and finished.** No heavy blur, no unfinished desks, no horizontal ghosting or double exposure on lamps, flasks or grids.
8. **Finished quality.** Nothing flat, under-shaded or half-built that reads as unfinished animation.
9. **No DNA helix** anywhere unless the film is about DNA: no double helix, helix props or helix garnish behind the Explorer.
10. **Microbes are faceless:** rods, spheres, spirals; soft glow; slightly ominous. No eyes, smiles or mascot germs, no gore. Sparse, and only when the VO needs them. Always moving.
11. **No Orbit robot,** ever.

## 6. The Explorer (character lock)

- **Bible:** `01_Character/CHARACTER_BIBLE.md`. **Sheet:** `01_Character/01_Master-References/hos-explorer-character-sheet-v01.jpg`. **Generation reference:** `01_Character/05_Generation-References/hos-explorer-reference-v01.jpg`. Attach it to every Explorer plate.
- **Look:** a young boy, messy wavy brown hair, round thin gold glasses, **teal long coat**, gold atom pin, tan waistcoat, brown bow tie, rolled brown trousers, brown boots, satchel, brass compass. Optional blue book *IDEAS · OBSERVE · QUESTION · DISCOVER*.
- **Role:** a side character. The story is the star. Mute test: the story reads without him.
- **Dosage:** longs, 1–3 beats (about every 3–5 scenes), walking through, touching one or two props, reacting, then leaving. Shorts, never at frame 0. Long thumbs, only as a tested variant.
- **Reject:** twins, clones or reflections; no glasses; wrong coat or age; flat 2D; parked centre-frame through a VO block; a second face.

## 7. Assembly and the open and out

- **Normalise every input to 1920×1080, 30 fps constant (CFR), stereo** before concat. Never VFR "original" frame rate; that is the social-playback stutter (`docs/PLAYBACK_LAG_FIX.md`, `04_Audio/tools/orbit_cfr_delivery.py`). Probe after: audio and video durations must match.
- **A remint is picture only.** Take video from the remint and audio from the locked part (`-map 0:v:0 -map 1:a:0`).
- **Bed parity** across parts: about −20 dB mean under VO.
- **Open:** no branded intro. The film opens on part 01's story picture.
- **Chapter cards:** the part number and title, soft, about 1.5 s, music continuing.
- **Out:** after the last line, a quiet 3–4 s cream-on-brown end card:
  > **History of Science**
  > **DISCOVERY. WONDER. PROOF.**

  Subscribe and the next film live in the **Studio end screen only**. Never burn subscribe or like graphics into the picture.
- **Export** to `09_Final-Export/<slug>_full_v0N.mp4`.
- **Shorts gate on every Short export:**
  ```bash
  python3 00_Brand/Channel-Setup/tools/gate_shorts_open.py check <short.mp4> --air-date YYYY-MM-DD
  ```
  It fails on no narration or near-silence, 40 s or longer, or an opening frame too close to any Short within 14 days. It warns on a still-looking first second: treat that as a re-cut of the opening. After upload, register it: `gate_shorts_open.py add --id … --date … --title … --file <mp4> --status scheduled`.
- **Watch it once on a phone with the sound on** before it goes anywhere.

## 8. Titles and thumbnails

Follow `THUMBNAIL_AND_TITLE_RULES.md`. Check every thumb with `python3 00_Brand/Channel-Setup/tools/thumb_preview.py long|short <thumb> --out <sheet>`. The plate is the strongest frame from the film's own master; text always comes from the edit, never from the model. Short covers: see `02_Video-Projects/001_How-Did-We-Discover-Germs/08_Thumbnail/_compose_hos_short_cover_safe_v02.py` for the feed-safe composer.

## 9. Upload and Studio finish

1. **Upload through the Data API package:**
   `cd 07_Content-Ops && npm run youtube:package -- --package <…/11_Upload-Package> --video <mp4> --dry-run` first.
   - Private with `publishAt`; explicit `privacyStatus` and `madeForKids: false`.
   - Altered or synthetic content: **yes**.
   - Channel: **`@HistoryOfScienceYT` only.** `CHANNEL_META.json` lists the channels never to touch (Orbit With Ben, OpptiAI, the empty `@HistoryOfScience`).
2. **Long:**
   - normal publish, Thursday 18:00, **no Premiere**;
   - description: the real subject first, then chapters, then sources;
   - Test & Compare with 3 thumbs;
   - end screen: the best related long + Subscribe;
   - captions from the VO script;
   - one pinned comment with the film's open question: `npx tsx --env-file=.env scripts/update-pinned-comment.ts --create --video <id> --question "…?"`, then pin it in Studio (the API can't pin).
3. **Short:**
   - Studio **Related video** → the exact live long it promotes. This is the only Short → long link.
   - custom cover; no pinned comment; zero `/go/`.
4. **One video = one upload.**
   - Never swap the file on a live id, never re-upload an idea that already went public.
   - A recut gets a new id. The old one goes private, never deleted.
   - Fix problems **before** upload.
5. **Title-only changes:** `npx tsx --env-file=.env scripts/retitle-videos.ts --file <fixes.json> --dry-run` (keeps the description, tags and schedule).
6. **Studio-only jobs** (Related, Test & Compare, end screens, covers) go through the desktop Studio CDP launcher `00_Brand/Channel-Setup/audits/start_studio_chrome_cdp.sh`. Never Replace.

## 10. Measure

- **Every Monday:** `python3 00_Brand/Channel-Setup/tools/weekly_public_audit.py` writes `audits/weekly/<date>/REPORT.md`.
- **Every Short at 48 h:** stayed-to-watch from Studio, logged with its frame 0 in `audits/SHORTS_LOG.md`.
- **Every long at 7 days:** impressions, CTR (past about 500 impressions), average percentage viewed (aim for about 50%), and views from Shorts.
- **Every Monday after the report:** refresh pinned comments with `update-pinned-comment.ts` (dry run first).
- **A weak upload is a result, not a re-upload.**

## 11. Affiliate (longs only)

- A `/go/` link only when that film names the product in VO or on screen. One product per film, late, after the wonder line.
- **Shorts:** zero links. Never invent ASINs. Never commit the Amazon tag.
- Details: `docs/AFFILIATE_MONETISATION_SYSTEM.md`.

## 12. Social

- **TikTok is paused** and HOS has no TikTok account: `TikTok/TIKTOK_UPLOAD_BLOCK.json` has `"paused": true`. No uploads, retries or "test one" until Ben lifts it.
- **Instagram and Threads** (`@historyofscienceyt`): each Short at most once per platform, never before its long is public, never on an Orbit account (`social/uniqueness.py`). Facebook: no HOS Page yet; the Page in the Meta portfolio is Orbit's.

## 13. Ben signs off

Stop and wait for Ben's OK at each of these:
1. topic;
2. long script (after it reaches 90);
3. Short scripts;
4. voice (listen);
5. moving picture (UAT on the moving cut, never stills);
6. thumbnails;
7. anything that goes public, is renamed or is deleted.

Ping Ben only after UAT has passed. If a cut fails after that ping, withdraw it. Docs-only PRs may merge; picture PRs wait for Ben's UAT.

## 14. Git

- **Land every film record on `main`** within a day: status, upload results, schedule. An agent starting from main must see what is live.
- One branch per job, merged or closed when the job ends. A STOP (quota, auth, missing VO) is a line in the part's `PARTNN_STATUS.md` on main, not a branch left open.
- Media stays out of git (`.gitignore`); record paths and sha256 instead.
