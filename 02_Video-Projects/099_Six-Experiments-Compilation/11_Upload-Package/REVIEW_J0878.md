# J0878 — HOS 6-film compilation v02 upload package + Private upload, parked for Chief

Gemini worker, 23 Oct 2026. Follows Chief's reopen ruling on J0878 (slot `Thu 10 Dec 2026 18:00 UK` / `2026-12-10T18:00:00.000Z`, first Thursday with no new HOS long; one `Sources (<chapter name>):` line per film in the compilation description). £0 spend, no generation credits, no HOS Buffer post.

## 1. Title & Thumbnail (£0 cover-builder)

- **Title:** `How Did Experiments Explain Blood, Germs and Atoms?` (52 chars; positive question naming the subjects; neighbour phrase `blood` in title, opening description, and tags).
- **Cover hook:** `FLASK PROOF` (`compilation_thumb_v01.jpg`, sha256 `f239c89b8c8b53d318d8d936beb78fcd377f203f484d33c78b98c4f63ac96d80`). Built at £0 with `build_cover_v01.py`, cleanly reconstructing the dark library bookcase left band from `00_Brand/Channel-Setup/style/long/001_how_did_we_discover_germs.jpg` with the clean swan-neck flask plate and small Explorer at lower left, and setting `FLASK` (cream) / `PROOF` (gold) in Didot bold with ornamental dividers.
- **Preview & Style sheets:**
  - `python3 00_Brand/Channel-Setup/tools/thumb_preview.py long .../compilation_thumb_v01.jpg --out .../PHONE_v01.jpg` -> exit 0 (`PHONE_v01.jpg`, readable at 168×94, clear of duration badge and off the flask/Explorer).
  - `python3 00_Brand/Channel-Setup/tools/style_sheet.py long .../compilation_thumb_v01.jpg --out .../STYLE_v01.jpg` -> exit 0 (`STYLE_v01.jpg`, matches live house look).

## 2. Description, Chapters & 6-Film Sources

- **Chapters (`CHAPTERS_v02.txt` / `DESCRIPTION_DRAFT_v01.txt`):**
  ```
  0:00 Six discoveries, one question
  0:53 The Hidden Circle
  9:23 Built From Air
  17:57 The Invisible Enemy
  24:14 The Empty Chairs
  33:22 A Light Through Skin
  40:27 Inside the Atom
  ```
- **Sources (`DESCRIPTION_DRAFT_v01.txt`):** Six `Sources (<chapter name>):` paragraphs built from each source film's `01_Script` `FACT_NOTES` / `SOURCES.md` (005 Harvey, 006 Photosynthesis, 001 Germs, 002 Periodic Table, 003 X-rays, 004 Atom), followed by the synthetic disclosure line:
  `Pictures: AI-generated 3D scenes. Narration uses a synthetic version of Ben’s voice. Facts: every number is checked against the sources listed above.`

## 3. Release Contract (`lint:package`) & Dry Run

`cd 07_Content-Ops && npm run lint:package -- --film 099` (`LINT_v01.txt`):

```
> content-ops@0.1.0 lint:package
> tsx scripts/package-lint.ts --film 099

PASS  02_Video-Projects/099_Six-Experiments-Compilation/11_Upload-Package/PACKAGE_MANIFEST.json
   warn  [captions] no captionsFile (captions from the script)
```

`cd 07_Content-Ops && npm run youtube:package -- --package ../02_Video-Projects/099_Six-Experiments-Compilation/11_Upload-Package --video /Volumes/data/mac-mini-archive/mini-tmp-scratch/2026-10-23/hos_comp_j0175_prep0540/hos_compilation_full_v02.mp4 --dry-run` (`DRY_RUN_v01.txt`, `PACKAGE_UPLOAD_RESULT_2026-10-23T21-03-08-236Z.json`):
- `ok: true`, `dryRun: true`, `scheduledFor: "2026-12-10T18:00:00.000Z"`, `privacy: "private"`.

## 4. Private Upload & YouTube Data API Read-Back

- **Receipt:** `PACKAGE_UPLOAD_RESULT_2026-10-23T21-09-09-542Z.json`
- **YouTube ID:** **`uAomPaOBrM8`** (`https://youtu.be/uAomPaOBrM8`, Studio: `https://studio.youtube.com/video/uAomPaOBrM8/edit`)
- **API Read-back (`YOUTUBE_READBACK_v01.json`):**
  - `id`: `"uAomPaOBrM8"`
  - `snippet.title`: `"How Did Experiments Explain Blood, Germs and Atoms?"`
  - `snippet.categoryId`: `"27"` (Education)
  - `snippet.defaultLanguage`: `"en-GB"`, `snippet.defaultAudioLanguage`: `"en-GB"`
  - `contentDetails.duration`: `"PT49M19S"`, `definition`: `"hd"`, `hasCustomThumbnail`: `true`
  - `status.uploadStatus`: `"uploaded"`, `status.privacyStatus`: `"private"`, `status.publishAt`: `"2026-12-10T18:00:00Z"`, `status.madeForKids`: `false`, `status.selfDeclaredMadeForKids`: `false`
- **Note for Chief on aborted first upload attempt (`Hmw4iMDfWFE`):**
  - An interrupted first upload attempt at `2026-10-23T21:04:07Z` created a 0-second stub `Hmw4iMDfWFE` (`contentDetails.duration: "P0D"`, `hasCustomThumbnail: false`, `privacyStatus: "private"`, `publishAt: "2026-12-10T18:00:00Z"`) two minutes before `uAomPaOBrM8` (`PT49M19S`, HD, custom thumbnail set) succeeded at `2026-10-23T21:06:06Z`.
  - Per the Never list and worker rules (never delete a video; never retitle or change `publishAt` on an existing video ID without Chief's instruction), `Hmw4iMDfWFE` was left untouched. Chief should clear `publishAt` and append `(duplicate)` to the title of `Hmw4iMDfWFE` (keeping it Private draft) so `npm run channel:audit` (`CHANNEL_AUDIT_AFTER_v01.txt`) clears the `title.duplicate-live` finding between `uAomPaOBrM8` and `Hmw4iMDfWFE`.
- **NAS Master:** Kept on NAS at `/Volumes/data/mac-mini-archive/mini-tmp-scratch/2026-10-23/hos_comp_j0175_prep0540/hos_compilation_full_v02.mp4` (`8282ffa8eb09e3a7cf1420562d70e14a428a0ae0489b3fdeccf5e4aeffe98490`, 49:18). No scratch deleted.
- **Measurement plan:** Updated in `docs/STANDALONE_SHORTS_TEST_2026-10/TEST_LOG.md` for the 4-week window following `Thu 10 Dec 2026 18:00Z` (`10 Dec 2026 18:00Z` – `7 Jan 2027 18:00Z`).
