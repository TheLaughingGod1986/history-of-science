# J0906 — HOS 007 Short `s05_vacca_jesty_v02` build & upload record

Gemini covering Chief-authorized job `J0906` on 24 October 2026 (`£0` spend).

- **Video:** `4WUs0beKn0A`, **Why Is It Called a Vaccine?** (`https://youtu.be/4WUs0beKn0A`)
- **State:** absent → **Private** with `publishAt=2026-11-17T11:30:00Z` (**Tuesday 17 November 2026, 11:30 London / 11:30 UTC**, GMT).
- **Authority:** Chief-created `J0906`, Chief PASS with one fix on `J0898`.
- **v02 Fix (`_build_short_s05_vacca_jesty_v01.py`):** Re-wrapped the 9–14 s title banner to two lines `'Why Vaccines Are'` (`508.9 px` wide, `x=285.6..794.4 px`) / `'Named After a Cow'` (`542.4 px` wide, `x=268.8..811.2 px`) inside title-safe; nothing else changed. Built `hos_007_s05_vacca_jesty_v02.mp4` (`24.167 s`, 60 words, SHA-256 `89a9a1668d7470acb27e5a93a77641aaeeaf6aed053fa418d899c776f4d3b88e`) and copied to iCloud `HOS UAT/007_The-First-Vaccine/10_Shorts/hos_007_s05_vacca_jesty_v02.mp4`.
- **Slot:** First free HOS Short slot after `2026-11-13T11:30Z`. Calendar checked against live YouTube API (`channel:audit`, 48 videos):
  - Thu 12 Nov 18:00 UK: HOS 007 long (*Why Vaccines Are Named After a Cow*)
  - Fri 13 Nov 11:30 UK: `-I_GHK-GcFs` (*What Was the Edward Jenner Experiment?*, HOS 007 `s04`)
  - Sun 15 Nov 11:30 UK: `x_3L_IdYgEc` (*The Blood Vessels Finer Than a Hair*, HOS 005 Short C)
  - Mon 16 Nov 11:30 UK: `-sa2t7dAtCk` (*What Is Dalton's Atomic Theory?*, HOS 004 `s05`)
  - **Tue 17 Nov 11:30 UK (`2026-11-17T11:30:00Z`):** **first free HOS Short slot → `4WUs0beKn0A`**
- **API readback (`API_READBACK_4WUs0beKn0A.json`):** `uploadStatus=processed`, `privacyStatus=private`, `publishAt=2026-11-17T11:30:00Z`, `madeForKids=false`, `selfDeclaredMadeForKids=false`, `defaultLanguage=en-GB`, `defaultAudioLanguage=en-GB`, `categoryId=27` (Education), `hasCustomThumbnail=true`, 6 tags.
- **Studio readback (`STUDIO_READBACK_4WUs0beKn0A.json`, CDP `:9460`):**
  - Audience: `No, it's not Made for Kids` (`checked: true`).
  - Altered / synthetic content: `Yes` (`checked: true`).
  - `Related video`: `None` (`007` long not uploaded yet; added `4WUs0beKn0A` to `J0875` so `Related video` → the `007` long is set once it has an id, before the Short goes public on Tue 17 Nov 11:30Z).
- **Records updated in HOS repo:**
  - `02_Video-Projects/007_The-First-Vaccine/10_Shorts/_build_short_s05_vacca_jesty_v01.py`
  - `02_Video-Projects/007_The-First-Vaccine/10_Shorts/SHORT_s05_vacca_jesty_v02.json`
  - `02_Video-Projects/007_The-First-Vaccine/10_Shorts/qa_s05_vacca_jesty_v02/`
  - `02_Video-Projects/007_The-First-Vaccine/10_Shorts/11_Upload-Package/s05_vacca_jesty/PACKAGE_MANIFEST.json`
  - `02_Video-Projects/007_The-First-Vaccine/10_Shorts/SHORTS_RELEASE.json`
  - `02_Video-Projects/007_The-First-Vaccine/10_Shorts/SHORTS_UPLOAD_INDEX.json`
  - `02_Video-Projects/007_The-First-Vaccine/11_Upload-Package/LAUNCH_PLAN.md`
  - `00_Brand/Channel-Setup/audits/SHORTS_LOG.md`
  - `00_Brand/Channel-Setup/audits/shorts_open_library/library.json` (+ `frames/4WUs0beKn0A.jpg`)
  - `00_Brand/Channel-Setup/social/UPLOADS.json`
- **HOS Buffer mirror registration (`J0875`):**
  - Recorded in HOS `00_Brand/Channel-Setup/social/UPLOADS.json` (`buffer: "held until public, then the full film (set long id once 007 long is uploaded, J0875)"`).
  - Once `orbit-with-ben` PR #260 (`J0817`) is merged and the 007 long has a YouTube id:
    ```bash
    cd /Users/benjaminoats/YouTube/orbit-with-ben/07_Content-Ops && npx tsx scripts/buffer-mirror.ts register --channel hos --video 4WUs0beKn0A --media "/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/HOS UAT/007_The-First-Vaccine/10_Shorts/hos_007_s05_vacca_jesty_v02.mp4" --long <007_long_id> --hook "Twenty-two years before Edward Jenner's 1798 book, Benjamin Jesty tried cowpox — and from vacca, Latin for cow, came vaccination." --question "Why are vaccines named after a cow?" --alt "A dairy cow in a golden Dorset meadow at sunset; hook caption NOT THE FIRST."
    ```

## Pasted check outputs

```text
BUILT s05_vacca_jesty v02 24.167 s 60 words sha 89a9a1668d74 captions {'ok': True, 'changes': 18, 'ratio': 1.0} handovers_ok=True (sampled 10/17)
PASS  hos_007_s05_vacca_jesty_v02.mp4  dur=24.17s  audio=-24.1dB  motion=16.17  dhash=727d2edf57490736
   sheet /var/folders/1z/ymtxygjd7cnfrxjv7sqgmww40000gn/T/hos_shorts_gate/hos_007_s05_vacca_jesty_v02_open_sheet.jpg
PASS  hos_007_s05_vacca_jesty_v02.mp4  0:24.17  mean -24.1 dB  peak -4.7 dB  146 wpm
polish gate PASS: 0 of 8 rows failed, 1 to look at -> 02_Video-Projects/007_The-First-Vaccine/10_Shorts/qa_s05_vacca_jesty_v02/polish_gate_s05_vacca_jesty_v02.json
picture QA PASS: 0 of 8 cuts fail, 1 to look at -> 02_Video-Projects/007_The-First-Vaccine/10_Shorts/qa_s05_vacca_jesty_v02/picture_qa_s05_vacca_jesty_v02/PICTURE_QA.md, 02_Video-Projects/007_The-First-Vaccine/10_Shorts/qa_s05_vacca_jesty_v02/picture_qa_s05_vacca_jesty_v02/picture_qa_review.jpg
freezedetect: 0 events []
PASS  02_Video-Projects/007_The-First-Vaccine/11_Upload-Package/PACKAGE_MANIFEST.json
   warn  [captions] no captionsFile (captions from the script)
PASS  02_Video-Projects/007_The-First-Vaccine/10_Shorts/SHORTS_RELEASE.json
   warn  [related] What Was the Edward Jenner Experiment?: Related video not set yet (set it to the 007 long once that long is public)
   warn  [related] Why Is It Called a Vaccine?: Related video not set yet (set it to the 007 long once that long is public)
PASS  Short 4WUs0beKn0A  private 2026-11-17 11:30 UK  Why Is It Called a Vaccine?
48 videos, 0 errors.
```
