# J0866 — HOS 001 Short `s11_curved_flask_v02` upload record

Gemini covering Chief-authorized job `J0866` on 23 October 2026 (`£0` spend).

- **Video:** `1-BZaFIMwYU`, **What Is the Pasteur Swan Neck Flask Experiment?** (`https://youtu.be/1-BZaFIMwYU`)
- **State:** absent → **Private** with `publishAt=2026-10-27T11:30:00Z` (**Tuesday 27 October 2026, 11:30 London / 11:30 UTC**, GMT).
- **Authority:** Chief-created `J0866`, Chief PASS `J0854`, approved `hos_001_s11_curved_flask_v02.mp4` (`22.367 s`, SHA-256 `f60e1c53ab0c7e9ac69728ec03c409be08203a01f3cf33fd6c043d5cf9f02882`).
- **Slot:** Next free HOS weekday Short slot at 11:30 London after the HOS 001 long (`_C92tIJCk8A`, public since 3 Sep 2026). Calendar checked against live YouTube API (`channel:audit`, 44 videos) and standalone test reservations:
  - Fri 23 Oct 11:30 UK: `LCZRHUyTiq0` (*What Are Cathode Rays?*)
  - Mon 26 Oct 11:30 UK: `OnJ8MFu0Mi0` (*How Did John Snow Stop Cholera?*, standalone S3)
  - **Tue 27 Oct 11:30 UK (`2026-10-27T11:30:00Z`):** **free Tuesday HOS Short slot → `1-BZaFIMwYU`**
  - Wed 28 Oct 11:30 UK: `vEg_tLIm0Co` (*Are Marie Curie's Notebooks Still Radioactive?*, standalone S4)
  - Fri 30 Oct 11:30 UK: `1lszTrYRp-8` (*Your Heart Pumps More Blood Than You Have*)
- **API readback (`API_READBACK_1-BZaFIMwYU.json`):** `uploadStatus=processed`, `privacyStatus=private`, `publishAt=2026-10-27T11:30:00Z`, `madeForKids=false`, `selfDeclaredMadeForKids=false`, `defaultLanguage=en-GB`, `defaultAudioLanguage=en-GB`, `categoryId=27` (Education), `hasCustomThumbnail=true`, 6 tags.
- **Studio readback (`STUDIO_READBACK_1-BZaFIMwYU.json`, CDP `:9460`):**
  - `Related video` set to `_C92tIJCk8A` (*How Did We Discover Germs?*) and verified after fresh reload (`"afterChunk": "Related video How Did We Discover Germs? Subtitles"`, `relatedSet: true`).
  - Audience: `No, it's not Made for Kids` (`checked: true`).
  - Altered / synthetic content: `Yes` (`checked: true`).
- **Records updated in HOS repo:**
  - `02_Video-Projects/001_How-Did-We-Discover-Germs/10_Shorts/11_Upload-Package/s11_curved_flask/PACKAGE_MANIFEST.json`
  - `02_Video-Projects/001_How-Did-We-Discover-Germs/10_Shorts/SHORTS_RELEASE.json`
  - `02_Video-Projects/001_How-Did-We-Discover-Germs/10_Shorts/SHORTS_UPLOAD_INDEX.json`
  - `00_Brand/Channel-Setup/audits/SHORTS_LOG.md`
  - `00_Brand/Channel-Setup/audits/shorts_open_library/library.json` (+ `frames/1-BZaFIMwYU.jpg`)
  - `00_Brand/Channel-Setup/social/UPLOADS.json`
- **HOS Buffer mirror registration:**
  - Recorded in HOS `00_Brand/Channel-Setup/social/UPLOADS.json` (`buffer: "held until public, then the full film"`).
  - Once `orbit-with-ben` PR #260 (`J0817`) is merged:
    ```bash
    cd /Users/benjaminoats/YouTube/orbit-with-ben/07_Content-Ops && npx tsx scripts/buffer-mirror.ts register --channel hos --video 1-BZaFIMwYU --media "/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/HOS UAT/001_How-Did-We-Discover-Germs/10_Shorts/hos_001_s11_curved_flask_v02.mp4" --long _C92tIJCk8A --hook "Pasteur's curved glass flask kept boiled broth clear until dust touched the liquid." --question "What did the swan-neck flask experiment prove?" --alt "A glowing swan-neck glass flask of clear broth in Pasteur's 1860s laboratory; hook caption CURVED GLASS."
    ```

## Pasted check outputs

```text
PASS  hos_001_s11_curved_flask_v02.mp4  dur=22.37s  audio=-22.6dB  motion=10.29  dhash=a18d868b13391c1c
   sheet /var/folders/1z/ymtxygjd7cnfrxjv7sqgmww40000gn/T/hos_shorts_gate/hos_001_s11_curved_flask_v02_open_sheet.jpg
SKIP  02_Video-Projects/001_How-Did-We-Discover-Germs/11_Upload-Package/PACKAGE_MANIFEST.json  (long already public; use channel:audit)
PASS  02_Video-Projects/001_How-Did-We-Discover-Germs/10_Shorts/SHORTS_RELEASE.json
PASS  Short 1-BZaFIMwYU  private 2026-10-27 11:30 UK  What Is the Pasteur Swan Neck Flask Experiment?
44 videos, 0 errors.
ALL CHECKS PASS
```
