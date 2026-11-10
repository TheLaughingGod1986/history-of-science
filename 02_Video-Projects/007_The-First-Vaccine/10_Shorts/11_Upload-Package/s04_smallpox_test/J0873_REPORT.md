# J0873 — HOS 007 Short `s04_smallpox_test_v01` upload record

Gemini covering Chief-authorized job `J0873` on 23 October 2026 (`£0` spend).

- **Video:** `-I_GHK-GcFs`, **What Was the Edward Jenner Experiment?** (`https://youtu.be/-I_GHK-GcFs`)
- **State:** absent → **Private** with `publishAt=2026-11-13T11:30:00Z` (**Friday 13 November 2026, 11:30 London / 11:30 UTC**, GMT).
- **Authority:** Chief-created `J0873`, Chief PASS `J0865`, approved `hos_007_s04_smallpox_test_v01.mp4` (`26.133 s`, SHA-256 `3daff43d04bcebf538cd4c405a8eeb723a7329f425bec536d876cb7c69d696af`, HOS `994d5a7b`).
- **Slot:** First free HOS weekday Short slot at 11:30 London on or after Fri 13 Nov (after the HOS 007 long *Why Vaccines Are Named After a Cow* airs Thu 12 Nov 18:00 London, `2026-11-12T18:00:00Z`). Calendar checked against live YouTube API (`channel:audit`, 45 videos) and standalone test reservations:
  - Sun 8 Nov 11:30 UK: `mTY67qet7cM` (*One Tight Band Proved Your Blood Goes Round*)
  - Mon 9 Nov 11:30 UK: standalone S7 (*Who Discovered That Plants Produce Oxygen?*)
  - Wed 11 Nov 11:30 UK: standalone S8 (*Who First Measured Blood Pressure?*)
  - Thu 12 Nov 18:00 UK: HOS 007 long (*Why Vaccines Are Named After a Cow*)
  - **Fri 13 Nov 11:30 UK (`2026-11-13T11:30:00Z`):** **free Friday HOS Short slot → `-I_GHK-GcFs`**
  - Sun 15 Nov 11:30 UK: `x_3L_IdYgEc` (*The Blood Vessels Finer Than a Hair*)
  - Mon 16 Nov 11:30 UK: `-sa2t7dAtCk` (*What Is Dalton's Atomic Theory?*)
- **API readback (`API_READBACK_-I_GHK-GcFs.json`):** `uploadStatus=processed`, `privacyStatus=private`, `publishAt=2026-11-13T11:30:00Z`, `madeForKids=false`, `selfDeclaredMadeForKids=false`, `defaultLanguage=en-GB`, `defaultAudioLanguage=en-GB`, `categoryId=27` (Education), `hasCustomThumbnail=true`, 6 tags.
- **Studio readback (`STUDIO_READBACK_-I_GHK-GcFs.json`, CDP `:9460`):**
  - Audience: `No, it's not Made for Kids` (`checked: true`).
  - Altered / synthetic content: `Yes` (`checked: true`).
  - `Related video`: `None` (`007` long not uploaded yet; set `Related video` → the `007` long once it has an id, before the Short goes public on Fri 13 Nov 11:30Z).
- **Records updated in HOS repo:**
  - `02_Video-Projects/007_The-First-Vaccine/10_Shorts/11_Upload-Package/s04_smallpox_test/PACKAGE_MANIFEST.json`
  - `02_Video-Projects/007_The-First-Vaccine/10_Shorts/SHORTS_RELEASE.json`
  - `02_Video-Projects/007_The-First-Vaccine/10_Shorts/SHORTS_UPLOAD_INDEX.json`
  - `00_Brand/Channel-Setup/audits/SHORTS_LOG.md`
  - `00_Brand/Channel-Setup/audits/shorts_open_library/library.json` (+ `frames/-I_GHK-GcFs.jpg`)
  - `00_Brand/Channel-Setup/social/UPLOADS.json`
- **HOS Buffer mirror registration:**
  - Recorded in HOS `00_Brand/Channel-Setup/social/UPLOADS.json` (`buffer: "held until public, then the full film (set long id once 007 long is uploaded)"`).
  - Once `orbit-with-ben` PR #260 (`J0817`) is merged and the 007 long has a YouTube id:
    ```bash
    cd /Users/benjaminoats/YouTube/orbit-with-ben/07_Content-Ops && npx tsx scripts/buffer-mirror.ts register --channel hos --video -I_GHK-GcFs --media "/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/HOS UAT/007_The-First-Vaccine/10_Shorts/hos_007_s04_smallpox_test_v01.mp4" --long <007_long_id> --hook "On 1 July 1796, Edward Jenner tested whether cowpox protected a boy from smallpox — and no disease followed." --question "What did Edward Jenner's first vaccine test prove?" --alt "A mahogany lancet case with ivory-handled steel lancets on Edward Jenner's study table in 1796; hook caption THE FIRST TEST."
    ```

## Pasted check outputs

```text
PASS  hos_007_s04_smallpox_test_v01.mp4  dur=26.13s  audio=-24.1dB  motion=18.05  dhash=86e766dfda1e867f
   sheet /var/folders/1z/ymtxygjd7cnfrxjv7sqgmww40000gn/T/hos_shorts_gate/hos_007_s04_smallpox_test_v01_open_sheet.jpg
PASS  02_Video-Projects/007_The-First-Vaccine/11_Upload-Package/PACKAGE_MANIFEST.json
   warn  [captions] no captionsFile (captions from the script)
PASS  02_Video-Projects/007_The-First-Vaccine/10_Shorts/SHORTS_RELEASE.json
   warn  [related] What Was the Edward Jenner Experiment?: Related video not set yet (set it to the 007 long once that long is public)
PASS  Short -I_GHK-GcFs  private 2026-11-13 11:30 UK  What Was the Edward Jenner Experiment?
45 videos, 0 errors.
ALL CHECKS PASS
```
