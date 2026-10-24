# J0896 — HOS compilation stub (`Hmw4iMDfWFE`) de-scheduled & retitled + 3-object £0 cover (`compilation_thumb_v02.jpg`) set on `uAomPaOBrM8`, parked for Chief

Gemini worker, 24 Oct 2026. Implements Chief's ruling on J0878 (`J0896`). £0 spend, 0 generation credits.

## 1. Aborted Stub `Hmw4iMDfWFE` — `publishAt` Cleared & Retitled (Kept Private, Not Deleted)

- **Video ID:** `Hmw4iMDfWFE` (0-second stub from interrupted first upload attempt)
- **Action:** Cleared `publishAt` so it stays a private draft and never goes public on 10 Dec, and retitled to `DUPLICATE STUB - do not publish (J0878)`. Not deleted (deleting is Ben's call).
- **API Read-back (`YOUTUBE_READBACK_stub.json`):**
  - `id`: `"Hmw4iMDfWFE"`
  - `snippet.title`: `"DUPLICATE STUB - do not publish (J0878)"`
  - `status.privacyStatus`: `"private"`
  - `status.publishAt`: *absent* (no scheduled publish time)
  - `contentDetails.duration`: `"P0D"`

## 2. Three-Object £0 Cover (`compilation_thumb_v02.jpg`) & PHONE/STYLE Sheets

- **Builder:** `02_Video-Projects/099_Six-Experiments-Compilation/11_Upload-Package/build_cover_v02.py` (£0 deterministic compositor).
- **Cover (`compilation_thumb_v02.jpg`):**
  - **Three objects in HOS library house style:**
    1. **Swan-neck flask** with sterile golden broth on the left-center table (`001` germs).
    2. **Gold-foil nuclear atom** with glowing golden nucleus, 3 orbital rings, and electron spheres in center-upper (`004` atoms).
    3. **Tied arm** with bright red arterial blood stopped above the tight linen tourniquet band and swollen blue forearm veins on the right (`005` blood), open hand below the atom, clear of the bottom-right duration badge.
  - **Hook text:** `6 / EXPERIMENTS` (`6` in gold punch, `EXPERIMENTS` in cream Georgia Bold serif display with dark ink outline and drop shadow), centered in the upper-left ornament column (`box=[52, 83, 477, 285]`) between the top and bottom gold scroll flourishes, above the canonical Explorer (`y>=328`), and completely off all three hero objects.
- **Phone & Style Sheets (pasted outputs):**
  - `python3 00_Brand/Channel-Setup/tools/thumb_preview.py long .../compilation_thumb_v02.jpg --out .../PHONE_v02.jpg`
    ```
    /Users/benjaminoats/_desk/worktrees/j0878-comp-pkg/02_Video-Projects/099_Six-Experiments-Compilation/11_Upload-Package/PHONE_v02.jpg
    ```
  - `python3 00_Brand/Channel-Setup/tools/style_sheet.py long .../compilation_thumb_v02.jpg --out .../STYLE_v02.jpg`
    ```
    /Users/benjaminoats/_desk/worktrees/j0878-comp-pkg/02_Video-Projects/099_Six-Experiments-Compilation/11_Upload-Package/STYLE_v02.jpg  (1 new vs 4 live long references)
    ```

## 3. Set on `uAomPaOBrM8` via `thumbnails.set` & Read-Back (`YOUTUBE_READBACK_v02.json`)

- **Package lint (`LINT_v02.txt`):**
  ```
  PASS  02_Video-Projects/099_Six-Experiments-Compilation/11_Upload-Package/PACKAGE_MANIFEST.json
     warn  [captions] no captionsFile (captions from the script)
  ```
- **`thumbnails.set` on `uAomPaOBrM8`:** HTTP `200` (`youtube#thumbnailSetResponse`).
- **API Read-back (`YOUTUBE_READBACK_v02.json`):**
  - `id`: `"uAomPaOBrM8"`
  - `snippet.title`: `"How Did Experiments Explain Blood, Germs and Atoms?"`
  - `status.privacyStatus`: `"private"` (unchanged)
  - `status.publishAt`: `"2026-12-10T18:00:00Z"` (unchanged)
  - `contentDetails.hasCustomThumbnail`: `true`
- **Channel Audit (`CHANNEL_AUDIT_AFTER_v02.txt`):**
  ```
  PASS  long  uAomPaOBrM8  private 2026-12-10 18:00 UK  How Did Experiments Explain Blood, Germs and Atoms?
  PASS  long  Hmw4iMDfWFE  private  DUPLICATE STUB - do not publish (J0878)
  ...
  47 videos, 0 errors.
  ```
