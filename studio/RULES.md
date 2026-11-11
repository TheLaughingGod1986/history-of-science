# History of Science: this channel's rules

Read `AGENTS.md` first. It holds the rules that are not this channel's alone: the desk, who does what, the status board, Ben's check-in, uploads, secrets, git. This file adds History of Science's own: the docs in force, the contract each stage must pass, what its films teach, look and sound like, how they are packaged, and the lines it adds to the Never list. Both are in force. Where they disagree, `AGENTS.md` wins.

**The channel:** History of Science (`@HistoryOfScienceYT`, `UCXp7HkBIl1LgaznXuZHJyRg`). Premium 3D cartoon films about how we discovered what we know, narrated in Ben's British voice, with the Explorer as a side character. Discovery. Wonder. Proof.

**The job:** make 7–9 minute discovery films that hold people, and Shorts that send them there. Why the channel is where it is: `00_Brand/Channel-Setup/audits/HOS_STUDIO_AUDIT_2026-09-25/AUDIT.md`.

## How the studio plugs this channel in

The studio engine (in orbit-with-ben today; see its `docs/MULTI_CHANNEL_PLAN.md`) reads this folder to plug this channel in:

- `channel.json`: who the channel is (slug `hos`, label `HOS`, YouTube handle), where its film state lives
  (`00_Brand/Channel-Setup/PIPELINE.json`), its share of the studio's production places, and how its pictures are
  made (`picture_route: flow_only`, which means Flow on the AI Ultra credits and never the priced Vertex route).
- This file: where an agent working on a History of Science job finds the channel's own rules.

Studio-wide rules always come first: the Ben gate, no spending past £0, never delete on the NAS, and Studio sign-ins
are Ben's. They live in orbit-with-ben's `AGENTS.md`. A channel can add rules, never remove one.

To change how the studio treats this channel, change `channel.json` here through a PR. The engine picks it up on its
next pull.

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

**Proof-first first 30 seconds (experiment HOS-2026-11-E2, Chief h47, 5 Nov 2026).** Applies at picture and edit on longs 008, 009 and 010 only. Spend stays inside each film's existing budget. Locked VO is unchanged. Plates already marked KEEP are used in the edit; this experiment does not authorise a remint. Films 004–007 and 011 onward keep the standing 4–6 s picture change.

The locked first-minute milestones stay: the answer image by 0:05, the title question by 0:08, the promise by 0:15, the stakes by 0:25, and the first real fact before 0:45. Part 01 still has no chapter card, no intro and no title card. The Explorer stays out of the first minute.

On those three films the opening adds three picture rules:

1. **Cuts.** From 0:00 to 0:30 every visual cut is under 4.5 s, there are at least 7 distinct moving plates, and no hold runs over 4.5 s. That pace replaces the standing 4–6 s picture-change band inside this window only. After 0:30 the 4–6 s band returns. A card still does not hold still for more than 4 s, and two full-frame teach graphics still do not run back to back.
2. **Proof.** From 0:05 to 0:15 the picture is the physical proof or the apparatus (the instrument, the sample, the hands on it), already moving. The answer image by 0:05 is that proof. An exterior establishing shot (a building, a street, a landscape or a campus) does not fill this window.
3. **Early DATA+SCALE.** The first animated DATA graphic, with its SCALE comparison, is on screen between 0:25 and 0:40. House style: ink on period paper or a cream teach card, drawing on with the spoken number, one idea, 4 words or fewer, over a moving plate. On a VO-locked film it rides a number already spoken. The SCALE is the comparison already on the DATA marker, sourced in `FACT_NOTES`. It counts as one of the film's DATA moments.

**Review gate (008–010 only),** scored PASS or FAIL in the desk report with the Teach and Polish gates:

1. **CUTS:** 0:00–0:30 has at least 7 distinct moving plates and no hold over 4.5 s.
2. **PROOF:** 0:05–0:15 is the apparatus or the physical proof.
3. **EARLY:** the first animated DATA+SCALE graphic is on screen between 0:25 and 0:40, and it matches `FACT_NOTES`.

Any FAIL goes back to the plate board or the edit before Ben's watch.

**Read (not a ship gate).** A long is scored once it has at least 100 Studio views. Under that, 0:30 retention and average percentage viewed are recorded and left unscored. **Pass:** 0:30 retention at least 60%, and days 0–13 average percentage viewed at least 22% (views-weighted across the longs that have crossed 100 views). **Stop and revert** this experiment for any 008–010 edit that is not yet locked if a cut built to it hits a UAT hard fail, or if a scored long's 0:30 retention is under 40%. An uploaded file stays as it aired. Readouts 3 Dec 2026 and 3 Jan 2027. The log is orbit-with-ben `05_Analytics/tests/HOS_LONG_TESTS.md` and `05_Analytics/LEARNINGS.md` → *HOS-2026-11-E2*.

## Polish pass (Astrum ref, 11 Oct 2026)

Ben, 11 Oct 2026 22:17, sent Astrum's *What Is It Like on the Surface of a Black Hole Planet?* (`PxJSOWyYWkc`, 27 min, 1.1M views) as a style reference for both channels: *"let me know what you think we can incorporate into our workflow."* Chief adopted five of its techniques the same night. They apply to every picture part and edit started after 11 Oct 2026, in the HOS house style. **Where an Astrum technique meets a HOS lock, the HOS lock wins**: the premium 3D cartoon look, white Didot italic, one label at a time, no flat poster or UI cards, the UAT hard fails and the first-minute timings all stand.

**Not adopted:** Astrum's long shot holds (6–8 s, some 15 s). The picture still changes every 4–6 s, except the HOS-2026-11-E2 window on 008–010 (cuts under 4.5 s from 0:00 to 0:30). No card holds still for more than 4 s, and length still comes from narration, not holds.

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
- **008–010 first 30 seconds (HOS-2026-11-E2).** From 0:00 to 0:30 the picture cuts in under 4.5 s, with at least 7 distinct moving plates, and 0:05–0:15 is the apparatus or the physical proof. The first animated DATA+SCALE graphic lands between 0:25 and 0:40. Milestones in the bullet above stay. Full rule, review scores and the stop line: *Teach on screen* → *Proof-first first 30 seconds*.
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

## Reference lessons (HOTU + SEA, 11 Oct 2026)

Chief studied two more reference channels on 11 Oct 2026. *History of the Universe* (HOTU) was read through `cqGhCCDC_Sw`, *Have We Finally Proven Einstein Wrong?*, and SEA through `7oR0Pmd-WIk`, *Higgs Boson: The God Particle*. The evidence is in `/workspace/hotu-pack/TAKEAWAYS.md` and `/workspace/sea-pack/TAKEAWAYS.md` on the box. Ben delegates creative calls to Chief and the AIs, and these are Chief's calls. They add to *Teach on screen*, *Polish pass* and *Packaging*.

**These HOS locks win wherever a lesson meets them:**
- **The first-minute timings:** the answer image by 0:05, the title question by 0:08, the promise by 0:15, the stakes by 0:25, the first real fact before 0:45. On 008–010 the opening cut, the apparatus window and the first DATA+SCALE graphic also follow *Teach on screen* → *Proof-first first 30 seconds* (HOS-2026-11-E2). These milestones stay.
- **The 22–27 s / under-40 s Shorts lock**, and the yellow hook word on the frame-0 caption.
- **The house look:** the premium 3D cartoon look, white Didot italic, one label at a time, no flat poster, UI card or photoreal card.
- **The Explorer's limits:** never in the first minute, 1–3 beats.
- **The ending:** no goodbye or subscribe ask; the last line hands off to the next film.
- **The UAT hard fails and the Never list.**

**1. Craft lessons (Claude writes them into scripts and plate boards; Chief scores them at review).**
- **Structure.**
  - Each part opens cold, on a period quote, a scene or a question.
  - Each part ends on a question the next part answers.
  - At about 60% of the runtime comes a midpoint twist: "Case closed? Wrong."
  - Near the end, raise the scariest idea, explain it away, then give a short sign-off. That's the existing hand-off line and cream end card, not a goodbye.
- **People** (HOS's strongest fit).
  - Every named person gets the WHO year card plus a **cut-out portrait with gentle parallax**: a sourced archive painting or engraving, credited, over a moving plate.
  - **Rivalries** are told with back-and-forth portrait cuts (HOTU's Einstein vs Bohr), and a witness quote where there is one.
  - Year first, then one sourced human detail, then the idea.
- **Hard ideas.**
  - Put a quirky, concrete, sourced anecdote just before the hard idea.
  - Show hard maths as a physical object in the house look: a brass slider that stops at a limit and then breaks past it, or a map of inked icons that light up one by one.
  - Make big numbers tangible on a scale card.
  - Jump between micro and macro scale.
  - **Scanned old diagrams with light traced through them** suit HOS: a real archive diagram (credited, one label at a time), with a warm ink or candle-gold trace, never a neon glow grid.
- **On screen.**
  - Keywords appear as they're spoken, with a plain-English sub-line, inked in white Didot, one label at a time, 4 words or fewer.
  - Years that fill the screen are the WHEN stamp.
  - Give every shot a slow push-in or pull-out, through the Veo camera move. Never a still push or Ken Burns when Flow is capped (Never list), and never on a teach card.
  - Use a recurring **"case file desk" chapter card**, painted in the house 3D world (a period desk with the case folder, never a UI card), with a low wooden or bass thud.
- **Sound.**
  - SFX on name cards and photo reveals (the house ink tick).
  - Music follows the emotion and changes by part (*Polish pass*). Near-silence at the key reveal is allowed, but for 6 s at most, so the music gate's gap rule still passes.
  - Cut to a human reaction at the emotional peak: an archive face, or the Explorer outside the first minute.
- **Banned (weak spots):**
  - **The same photo or plate used 5 or more times** in a film (a Chief FAIL);
  - **generic glowing-dot or particle filler** standing in for a real subject;
  - **holding back the answer.**

**2. Packaging rules.**
- **Cover text never repeats the title**, from new thumbs on (those not yet made from 006 on). The main thumb no longer paints the title in: it carries 2–3 words that add to it, in the same serif lettering with one gold word (`THUMBNAIL_AND_TITLE_RULES.md` §2.5). The lettering style is unchanged; only the words change.
- **Titles need a big subject plus one hook:**
  - a famous nickname (*Semmelweis: The Doctor Who Saved Mothers*);
  - the viewer inside the subject ("your hands", "your bones");
  - a journey to the edge.

  Catalogue labels fail (§1 rule 11).
- **Descriptions** carry, in order:
  1. the first line answering the title;
  2. chapters named as story beats (*Bohr vs Einstein*, not *Quantum Theory*);
  3. sources;
  4. archive image credits;
  5. **one honest line on how the film is made**, for example *"Pictures: AI-generated 3D scenes, with archive images credited below. Facts: every claim is checked against the sources listed."*

  Never claim "no AI", and never name the AI checkers. Say a person checked the facts only when one actually did. The altered-content setting stays on.

**3. Shorts rules.**
- **The myth-bust opener is an allowed format.** Line 1 is the belief ("You were taught Newton's apple hit his head"), and **"No"** or the reversal lands by about 0:15, inside 22–27 s and the first-two-seconds rules.
- **No straight trailers.** A Short is never a clip trimmed from the long. It has its own open, frame 0, caption, title and loop, and it stands alone.

**4. Graphics go to Codex** (`--kind chart`, `gpt-6-astra`, per *Who does what*): the limit slider, the lit-up icon map, the number scale card, the traced-diagram graphic and the case-file card. Each is built in the house look and rendered per row in the edit.

**5. Suggestions to test, not rule changes.** The no-cover-text Test & Compare and the near-black cap refinement are Orbit tests (orbit-with-ben AGENTS.md). HOS covers keep their painted lettering, and HOS has no near-black cap to refine.

**Applies to:** scripts signed off from 12 Oct (011 on) for structure and people. 009 and 010 get only on-screen items with no spoken change, and 006–008 get edit-stage items. Packaging applies to every new upload package. 004 and 005 aren't reworked.

## Packaging (Astrum ref, 11 Oct 2026)

Ben, 11 Oct 2026, asked what we can learn from Astrum's thumbnails and Shorts packaging. Chief decided the following for both channels the same night. In HOS it's adapted to the house look, and **the HOS live look wins** (painted key art, serif cream and gold lettering, the Explorer small at lower left, the period palette). Full rules: `THUMBNAIL_AND_TITLE_RULES.md` §2.B.
- **Name the thing or dare.** No vague questions or teasers on thumbs, covers or titles. A question names its subject.
- **Lettering in a clear band** (the top, or the live layout's left edge), never over the hero object.
- **No saturation push.** The period palette and warm light stay. Orbit's harder grade doesn't apply here.
- **Review:** Chief scores HOOK / BAND / PHONE on every new thumb and cover, next to `style_sheet.py`. Any FAIL goes back before Ben's final check-in.
- **Applies to** new thumbs and covers from 12 Oct (006 on). 004 and 005 and the live back catalogue aren't reworked. Shorts length is unchanged: the 22–27 s lock and the 40 s Never line stand (Orbit's one-off 50–60 s test doesn't apply to HOS).

## Never (this channel's additions)

These add to the Never list in `AGENTS.md`. They remove nothing from it.

- **Channels:** upload, schedule or post to Orbit With Ben, OpptiAI or the empty `@HistoryOfScience`. HOS is `@HistoryOfScienceYT` only.
- **Publishing:**
  - Premiere a long (until subscribers are in the hundreds).
  - Leave any video or Short marked **Made for Kids**. Re-check Audience after every Studio save (`STUDIO_PLAYBOOK.md` §9).
  - Put the Explorer at frame 0 of a Short.
  - Burn subscribe or like graphics into a film. Subscribe lives in the Studio end screen.
  - Ship a Short with a shot that does not fill the 9:16 frame: black bars, a flat band, or a blurred or mirrored copy above and below a picture band. `gate_shorts_open.py` fails it at the opening and over the whole Short (10 Nov 2026).
- **Titles:** hashtags, series suffixes, hedged claims, or a title that copies a live video.
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
