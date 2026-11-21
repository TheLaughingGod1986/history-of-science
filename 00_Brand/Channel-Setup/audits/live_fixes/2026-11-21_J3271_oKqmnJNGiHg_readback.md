# Live description fix read-back: `oKqmnJNGiHg` (J3271, 21 Nov 2026)

Authorised by the Acting Chief ruling on `J3269` (`2026-11-21_J3269.md`, Fix 1). Done by `claudecode` (Mac mini worker). Cost: £0, 0 credits.

## What changed

One line of the description on the public Short `oKqmnJNGiHg` (*How Was Phosphorus Discovered?*), through the YouTube Data API (`videos.update`, `part=snippet` only, the live snippet sent back with the new description), at `2026-11-21T04:28:06Z`.

| | Line 7 of the description |
|---|---|
| Before | `Los Alamos National Laboratory, Phosphorus: https://periodic.lanl.gov/15.shtml` (HTTP 404) |
| After | `Royal Society of Chemistry, Periodic Table — Phosphorus: https://periodic-table.rsc.org/element/15/phosphorus` (HTTP 200) |

Nothing else was sent: no `status` part, so privacy and schedule could not change. No Studio click was made.

## Read-back

**YouTube Data API (`videos.list`, `snippet,status,contentDetails`), after the change:**

| Field | Value | Result |
|---|---|---|
| description | exact match to `2026-11-21_J3269.md` lines 50–58 (473 characters) | changed as approved |
| title | `How Was Phosphorus Discovered?` | unchanged |
| tags | `Hennig Brand`, `alchemy`, `history of chemistry`, `phosphorus`, `phosphorus discovery`, `white phosphorus` (6) | unchanged |
| categoryId | `27` (Education) | unchanged |
| defaultLanguage / defaultAudioLanguage | `en-GB` / `en-GB` | unchanged |
| privacyStatus / publishAt | `public` / none | unchanged |
| publishedAt | `2026-10-21T10:30:16Z` | unchanged |
| madeForKids / selfDeclaredMadeForKids | `false` / `false` | unchanged |

The update call's own immediate read still returned the old text (read-after-write lag); a second read about a minute later returned the new text, and the description-only script then reported `already_described` (exact string match).

**`channel-audit.ts` against the live API, after the change:** `68 videos, 0 errors` (exit 0); `PASS  Short oKqmnJNGiHg  public  How Was Phosphorus Discovered?`.

**Live public pages, fetched signed out after the change:**

| Check | `/watch?v=oKqmnJNGiHg` | `/shorts/oKqmnJNGiHg` |
|---|---|---|
| Page title | `How Was Phosphorus Discovered? - YouTube` | same |
| `periodic-table.rsc.org/element/15/phosphorus` present | yes | yes |
| `periodic.lanl.gov` present | no (0) | no (0) |
| Related video pill (`reelCarouselButtonViewModel` → `/watch?v=AL_-qlWko_g`) | not shown on watch pages | **yes, `AL_-qlWko_g`** |
| AI disclosure (`howThisWasMadeSectionViewModel`) | present | present |
| `isPrivate` / `isUnlisted` | false / false | false / false |
| keywords | the same 6 tags | the same 6 tags |

`Altered content = Yes` is read from the public "How this was made" section; the Data API returned no `containsSyntheticMedia` field for this video, so that setting is evidenced by the public badge only.

## Not done

Nothing was renamed, rescheduled, made private or deleted. No other video was touched.
