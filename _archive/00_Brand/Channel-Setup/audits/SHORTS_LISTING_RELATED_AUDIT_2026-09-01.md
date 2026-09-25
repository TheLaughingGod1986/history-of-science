# Shorts listing + Related pill audit (1 Sep 2026, ~16:45 UK)

Pulled live via yt-dlp JSON + Shorts HTML (`id.reel_multi_format_link` overlay) + Playwright on the keeper. Channel: **Orbit with Ben** (`UC_esArsDKd3GJvOkeO0DUog`). Data API cannot set Related; the pill is **Studio-only**.

## Verdict

The Last Star **Related pills point at the correct long** (`REXYxuLOBoI`). Titles on the dump trio are unique. Everything else on those three live Shorts is **thin vs the earlier Last Star winners**.

| Layer | Last Star winners (`DN4L1DkerMM`, `PV50PX-bE4g`, `wIh3armF7_k`) | Dump trio (`9lLZMy8rBJo` keeper + two pending unpublish) | Wed punch-07 (not uploaded) | Europa cluster |
|---|---|---|---|---|
| Title | Unique punch, not the long title | Unique punch (keeper OK; `KX-XU_AODoI` VO still says the long title) | Unique: *Star Recycling Isn't Perfect* | Titles planned only |
| Description | Punch first + “Watch the full film — {title}:” + URL + hashtags | **Stripped** to long title + URL only. No punch, no hashtags | Now winner-parity in index (was missing hashtags) | Not written until cuts exist |
| Tags | **24–25 / ~440 chars** (budget 500) | **10 / ~171–194 chars** | Now **27 / 485 chars** in index | Not written |
| Cover | `maxresdefault.jpg` (often captioned Orbit — do not copy for new covers) | Captioned `oar2` frames; keeper garbled **science has / notriclosed** | 1080×1920 no-caption still on disk | None |
| Related pill | Overlay → Last Star long | Overlay → Last Star long | Cannot exist until upload + Studio Related | Cannot exist until upload |
| `/go/` | None (correct) | None (correct) | None (correct) | Must stay zero |

**Index JSON is not what YouTube is serving** on the dump trio. Slot 06 already has the winner-shape description/tags; live `9lLZMy8rBJo` does not.

## Related pill (Studio overlay)

Public Shorts HTML marker: `accessibilityId: id.reel_multi_format_link` + `BUTTON_VIEW_MODEL_STYLE_OVERLAY`. Parent id appears **9×** on pages that have a pill (overlay + description), not description-only.

| Short | Live title | Overlay label | Target | Pass? |
|---|---|---|---|---|
| `9lLZMy8rBJo` | What Remains After the Last Star Dies? | *What Happens When the Last Star Dies? \| Orbit's Cosmic Journey* | `REXYxuLOBoI` | **Video yes** · label has series suffix |
| `CkSECfUfH2Y` | The Sky Is Already Running Out of Light | same | `REXYxuLOBoI` | Video yes (unpublish anyway — mute-test fail) |
| `KX-XU_AODoI` | The Day the Last Star Goes Out | same | `REXYxuLOBoI` | Video yes (unpublish anyway — long-title VO) |
| `DN4L1DkerMM` | The Universe Is Running Out of New Stars | same | `REXYxuLOBoI` | **Pass** |
| `PV50PX-bE4g` / `wIh3armF7_k` | (winners; HTML not re-fetched this pass) | expected same | `REXYxuLOBoI` in description | Treat as pass from prior scrape |
| `QptlHs1HuYI` | The Galaxy Should Be Crowded — It's Silent | *Why Haven't We Found Aliens Yet? The Fermi Paradox Explained* | `Mo93x0fxB1Q` | Correct Fermi long · **wrong week** (unpublish) |
| `GjcZB8826J8` / `MDvAKtmKauw` | Alien Worlds Shorts | *Alien Worlds: The Strangest Planets We've Ever Found* | `b8-X_FyJnHM` | Correct Alien Worlds long |
| `Q16DKNvq2OY` | Earth, Seen From the Dark | **no overlay** | none | **Fail** — no Related, no film URL |
| Wed punch-07 | not live | — | must set `REXYxuLOBoI` after upload | pending |
| Europa 01–08 | not live | — | must set `NbW5G1BpPY0` | blocked (no master) |

Playwright on `https://www.youtube.com/shorts/9lLZMy8rBJo`: heading = Short title; clickable pill = long title → `/watch?v=REXYxuLOBoI`.

**Pill copy follows the long’s Studio title.** Live long is still `What Happens When the Last Star Dies? | Orbit's Cosmic Journey`. Strip the suffix **on the long** and every Last Star pill label cleans up. HeyHistorically bar wants the tempting film title, not a series tag.

Related cannot be set or patched without an `@OrbitWithBen` Studio session.

## Live listing vs winner pattern (Last Star)

**Winner description shape** (`DN4L1DkerMM`, 226 views):

```
{punch line}

Watch the full film — What Happens When the Last Star Dies?:
https://www.youtube.com/watch?v=REXYxuLOBoI

#LastStar #HeatDeath #Cosmology #Space #Shorts #OrbitWithBen
```

Zero `/go/` on Shorts. Long `REXYxuLOBoI` may keep the Katie Mack affiliate block; do not copy it onto Shorts.

**Dump trio live description (all three):**

```
What Happens When the Last Star Dies? | Orbit's Cosmic Journey
https://www.youtube.com/watch?v=REXYxuLOBoI
```

Keeper live tags (10): `astronomy shorts, bounce cosmology, could the universe start again, empty universe, heat death remnants, last star dies, new inflation, orbit with ben, space shorts, what remains after the last star dies` — off-brief vs heat-death cluster.

Winner tags (24 / 440): astronomy, astrophysics, black dwarf, cosmology, cosmos, deep time, degenerate era, dying stars, end of the universe, far future of the universe, fate of the universe, heat death explained, heat death of the universe, last light in the universe, orbit with ben, orbit's cosmic journey, red dwarf stars, red dwarfs, science documentary, space documentary, star death explained, stellar evolution, the last star in the universe, what happens when the last star dies.

## Covers

| Asset | What YouTube is using | Gate |
|---|---|---|
| Keeper `9lLZMy8rBJo` | Captioned ringed-planet frame: **science has / notriclosed** | Fail — garbled caption on cover |
| Dump sky `CkSECfUfH2Y` | Captioned frame | Fail for new covers (unpublish) |
| Winner `DN4L1DkerMM` | Orbit CU + **galaxies recycle** | Older pattern; new covers = **no mascot, no caption**, Studio **desktop** custom cover (never Data API `thumbnails.set`) |
| Punch-07 | Not live. Still: `10_Shorts/08_Covers/last-star_punch-07_cover.jpg` (1080×1920, galaxy dust, no Orbit, no text) | Ready to upload as custom cover |

## Studio paste — patch keeper `9lLZMy8rBJo` (when logged in)

Title (keep): `What Remains After the Last Star Dies?`

Description (replace live two-liner):

```
After the last star dies, the universe keeps going — black dwarfs, black holes, and deep time stranger than you think.

Watch the full film — What Happens When the Last Star Dies?:
https://www.youtube.com/watch?v=REXYxuLOBoI

#LastStar #HeatDeath #Cosmology #Space #Shorts #OrbitWithBen
```

Tags (replace the 10 live tags with the 24 winner tags from slot 06 / `DN4L1DkerMM`).

Cover: Studio desktop → custom image from a **no-caption** frame (not the garbled oar2). Related already points at `REXYxuLOBoI` — leave it.

Also: unpublish `CkSECfUfH2Y`, `KX-XU_AODoI`, `Q16DKNvq2OY`, `QptlHs1HuYI`. Strip `| Orbit's Cosmic Journey` from long `REXYxuLOBoI`.

## Wednesday punch-07 (scheduled)

Live ID **`n2WbOfJhOwc`** — Studio on Mac mini 1 Sep evening. Public **2 Sep 2026 11:30 UK**.

- Title: Star Recycling Isn't Perfect
- Related: `REXYxuLOBoI` (pill label includes `| Orbit's Cosmic Journey`)
- madeForKids: false
- Cover: `08_Covers/last-star_punch-07_cover.jpg`
- Tags: 24 chips, 494/500 (dropped leftover mass / stellar recycling / star recycling)
- Pin: pending until public (Studio comment post failed while private)
- Zero `/go/`

## Europa (Thu 3 Sep morning onward)

`EUROPA_SHORTS_CLUSTER_v01.json` now has listing templates (description/tags/hashtags/related). **No files, no YouTube IDs, no pills** until the 16:9 master is on disk and each cut is uploaded. Related target is always premiere id `NbW5G1BpPY0`. Zero `/go/`.
