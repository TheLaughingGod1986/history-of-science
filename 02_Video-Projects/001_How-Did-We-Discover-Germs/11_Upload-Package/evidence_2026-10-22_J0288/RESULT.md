# J0288 — HOS 001 Germs (`_C92tIJCk8A`) thumbnail-only Test & Compare armed (`T009`)

- **Date:** 2026-10-22 ~02:42 London (`01:42Z`), Gemini covering on CDP `:9460` (`@HistoryOfScienceYT`, channel `UCXp7HkBIl1LgaznXuZHJyRg` verified).
- **Authority:** Chief KEEP on J0279 (`fbcbc6f` on branch `cursor/j0279-germs-thumb-b`) + J0288 brief (`df9c2144c`, reopened by Chief 15 Oct & 21 Oct).
- **Prior test state (captured before arming):**
  - Mode: Title and thumbnail (`1 October 2026 at 23:25 to 16 October 2026 at 00:04`).
  - Status: **`Test finished. Not enough impressions to declare a winner.`**
  - Variant A: *How Did We Discover Germs?* — watch-time share `—` (`Now visible to all viewers`).
  - Variant B: *What proved germs were real?* — watch-time share `—`.
  - Reach tab snapshot (`3 Sept 2026 – Now`): 35 thumbnail impressions, 8.6% CTR, 7 views, 5 unique viewers (funnel 3 Sept–20 Oct: 38 impressions, 5.3% from YouTube recommendations, 7.9% CTR, 3 engaged views, 4:46 average view duration, 0.24 watch time hours).
- **New test armed (`T009` in `05_Analytics/tests/THUMB_LEDGER.json`):**
  - Mode: **Thumbnail only** (2 variants).
  - Variant A: existing live thumbnail (`HOW DID WE DISCOVER GERMS?`).
  - Variant B: `germs_B_invisible_life_v02.jpg` (`INVISIBLE LIFE?`, 1280×720, 267,906 bytes, sha256 `46b9e18d02affb51bf2c33b362562d732811a162447e44bdfd33957adaedbc61`, maker `cursor` J0279 v02).
  - Saved and reloaded `https://studio.youtube.com/video/_C92tIJCk8A/edit`.
  - Reopened `View test report`: confirmed **`Thumbnail only · A/B test report · Test running…`** (`Estimated time remaining: 13 days 23 hours…`), both variants showing title *How Did We Discover Germs?*.
  - Unchanged: Title (`How Did We Discover Germs?`), Visibility (`Public`), Audience (`No, it's not 'Made for Kids'`).
  - Read-back date in `THUMB_LEDGER.json` (`T009`): **`2026-11-05`** (14 days on).
  - Local screenshots saved in `/Users/benjaminoats/_desk/J0288/artifacts/` (`01_edit_page.png` through `11_confirm_test_running.png`). No spend (`£0`).

## Post-session `npm run channel:audit`

```
PASS  long  _C92tIJCk8A  public  How Did We Discover Germs?
   warn  [ai-disclosure] Data API omits altered/synthetic — confirm Yes in Studio (Altered content)

43 videos, 0 errors.
```
