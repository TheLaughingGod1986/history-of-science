# 005 upload: long scheduled as `0IfXGSX7Ypw` (Grok → Claude, 2 Oct 2026)

**Done.** *The Tied Arm That Proved Your Blood Circulates* is uploaded to @HistoryOfScienceYT as **`0IfXGSX7Ypw`** (https://youtu.be/0IfXGSX7Ypw). It is private and scheduled for **Thu 29 Oct 2026 18:00 UK** (`2026-10-29T18:00:00Z`) as a normal publish, not a Premiere. Ben's approvals ("All ok", your comment 5948928013) and every check below are recorded in `production-status.md` on `grok/hos-005-blood-script`.

## What's set

- Master `hos_005_master_v01.mp4` (sha `84476e06…`).
- Title as approved; description v02 with chapters; 7 tags; Education; English (UK) for both languages; playlist *How Did We Discover…?*.
- **Not made for kids** (API `madeForKids: false`; Studio re-read after every save). Age restriction none. **Altered content: "Yes, AI was used"** (by eye; the audit warns because the API doesn't report it).
- **Thumbnail A v02** (ONE TIGHT BAND, `356f9ea5…`), set via the API (200, maxres).
- **Captions:** a script-locked SRT (`11_Upload-Package/Captions/hos_005_master_v01.en.srt`, 137 cues, built from the VO retime of script v02), inserted as en-GB and **serving**.
- **Test & Compare:** Thumbnail only, A v02 + B v02 (IT GOES ROUND, `17672532…`), saved. Studio accepts the test on a scheduled video but marks it **Ineligible: "Your video is not public"**, so it can't start until 29 Oct 18:00.
- **End screen** on the 20 s hold, 8:26:16–8:46:16: Subscribe + specific video *How Did We Discover Germs?* (`_C92tIJCk8A`), which the last line sets up. The video element is top left, clear of the card's words. Verified on reopen.
- Settings: paid promotion No; caption certification "never aired on US TV"; Education type Concept overview; Academic system England; comment moderation Basic; automatic places Off.
  - Level: Key stage 4 won't persist (reads None after reopen, the same as 004).
  - Exam: GCSE Biology isn't in Studio's list.
  - Both are left blank.
  - Places Off went in the same save as moderation (the click registered late). Visibility and Audience read fine after that save too.

Screenshots attached: the visibility panel (scheduled 29 Oct 18:00, Premiere unticked) and the end screen.

## Checks (pasted)

```
PASS  channel UCXp7HkBIl1LgaznXuZHJyRg
```

`npm run lint:package -- --film 005` (before the upload, and again after adding `youtubeId`):

```
PASS  02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/11_Upload-Package/PACKAGE_MANIFEST.json
```

`npm run channel:audit`:

```
PASS  long  0IfXGSX7Ypw  private 2026-10-29 18:00 UK  The Tied Arm That Proved Your Blood Circulates
   warn  [ai-disclosure] Data API omits altered/synthetic — confirm Yes in Studio (Altered content)
23 videos, 0 errors.
```

Shorts B and C re-gated on their approved dates (files unchanged). **No Short uploaded**; they wait for Ben on covers and titles.

```
PASS  hos_005_s02_the_tied_arm_v01.mp4  dur=25.83s  audio=-21.6dB  motion=19.22  dhash=070f46033fa90e0e   (--air-date 2026-11-08)
PASS  hos_005_s03_never_saw_v01.mp4  dur=24.83s  audio=-21.7dB  motion=17.01  dhash=0f0f0d1f6e030f0f   (--air-date 2026-11-15)
```

## For the 29 Oct 18:05 jobs

1. **Test & Compare** should read Running. If it still says Ineligible, re-arm Thumbnail only with A + B v02.
2. **Pinned comment:** not posted, so I need the open-question text from you.
3. **Cards:** none yet (the playbook says two). Proposal: *How Did We Discover Germs?* at about 8:14 ("That is where the story of germs begins"), plus one more of your choice. Tell me the targets and times.
4. Point the older longs' end screens at `0IfXGSX7Ypw`.

## Sun 1 Nov and Tue 3 Nov: back-catalogue picks (from `SHORTS_LOG.md`)

001 had a Short on 20 Oct and 002 on 18 Oct. 004 has had only the gold Short (16 Oct). 003 hasn't had one since 27 Sep. **The one built Short that hasn't aired, 004's `s03_her_ring` v05, can't be used:** it's the wedding-ring idea, already public as `zI_eD3vFWmE`. So both slots need a new Short cut from KEEP plates, which means a Shorts script for Ben (sign-off 3).

- **Sun 1 Nov → 004** *What's Really Inside an Atom?* (`GHZDsiH7L7A`): Rutherford's shell that came back off tissue paper (the gold foil plates in Part 04). No live Short uses it. Fallback: the pea in a football stadium.
- **Tue 3 Nov → 003** *How Did We Discover X-rays?* (`frP_YrNShsU`): "He called it X, for unknown", the locked-door tests with a book, a hand and metal. It sits close to the live accident and bones Shorts, so it needs a live-page check first. Fallback: a new 002 or 001 idea.

Also still open: `clV6E10NLPw` (001, 20 Oct) has the wrong Related.

## Tooling notes (not fixed here)

- **Uploader override bug:** `loadYouTubePackage` spreads `{...manifest, ...overrides}`, and CLI flags that aren't given come through as `undefined`, which wipes the manifest's title, schedule, thumbnail and playlist ("No title found"). I worked around it by passing every value as a flag. It needs a small fix PR (drop undefined keys).
- `npm run youtube:package` doesn't load `.env` (DATABASE_URL undefined), and `.env` keeps `PUBLISHING_DRY_RUN` on. The live run was `PUBLISHING_DRY_RUN=false npx tsx --env-file=.env scripts/youtube-package-upload.ts …`.
- `thumbnails.set` returns 403 while the video is still processing; a retry a minute later worked. The uploader could retry it.
- The Studio Chrome (:9460) had a frozen 001 edit tab left from 1 Oct that blocked Playwright's CDP attach. There was no dialog on it, so I closed the tab; nothing changed on YouTube.

**Git:** committed as `7ff1bff` on `grok/hos-005-blood-script` (no media). [PR #184](https://github.com/TheLaughingGod1986/history-of-science/pull/184) is open and mergeable. The film record should be on `main` by tomorrow, and the merge is your call or Ben's.

Evidence: `11_Upload-Package/Schedule/PACKAGE_UPLOAD_RESULT_2026-10-02.json`, `11_Upload-Package/evidence_2026-10-02_studio/*.json`; screenshots on the Mini in `~/.local/share/cursor-mac-mini-hos-worker/artifacts/DESK_2026-10-02_005_upload/`.
