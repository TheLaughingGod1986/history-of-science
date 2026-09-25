# History of Science — studio

Production repo for **History of Science** ([@HistoryOfScienceYT](https://www.youtube.com/@HistoryOfScienceYT)): premium 3D cartoon films about how we discovered what we know, narrated in Ben's British voice, with the Explorer as a side character. Discovery. Wonder. Proof.

Separate channel and repo from Orbit With Ben.

**Agents and new collaborators: start with [`AGENTS.md`](AGENTS.md).** It lists the docs in force, the commands, where Ben signs off, and what never to do.

| Need | Go to |
|---|---|
| What to make, the week, hooks, how we measure | `00_Brand/Channel-Setup/HOS_STRATEGY.md` |
| How to build and ship a long or a Short | `00_Brand/Channel-Setup/STUDIO_PLAYBOOK.md` |
| Titles and thumbnails | `00_Brand/Channel-Setup/THUMBNAIL_AND_TITLE_RULES.md` |
| The Explorer | `01_Character/CHARACTER_BIBLE.md` |
| Where the channel stands, and why | `00_Brand/Channel-Setup/audits/HOS_STUDIO_AUDIT_2026-09-25/AUDIT.md` |
| Latest numbers | `00_Brand/Channel-Setup/audits/weekly/<date>/REPORT.md` (every Monday) |
| What to do next | `00_Brand/Channel-Setup/IMPROVEMENTS_BACKLOG.md` |
| Old docs, rules, scripts and the Orbit leftovers | `_archive/` (history only) |

## Repo map

```
AGENTS.md                     Start here (any agent)
00_Brand/
  Brand-Guidelines/           Brand snapshot, Showrunner brief studio block
  Channel-Setup/              Docs in force, backlog, templates, channel metadata
    tools/                    Weekly audit, Shorts ship gate, thumb preview
    audits/                   Current audit, Shorts log, weekly reports
    Meta/ Threads/ TikTok/ social/   Social mirror ops (TikTok paused)
01_Character/                 The Explorer: bible, master sheet, generation reference
02_Video-Projects/NNN_Slug/   One folder per film (start from _template_NNN_Episode-Slug)
04_Audio/tools/               VO settings, Flow Veo, CFR export, SFX and music beds
07_Content-Ops/               Ops app + CLIs: script review, episode gate, YouTube upload, retitle
docs/                         Tech notes
_archive/                     Superseded material, kept for history
```

## Content Ops quick start

```bash
cd 07_Content-Ops
cp .env.example .env      # fill in locally; never commit secrets
npm install
npm run dev
```

## Film folders

```
02_Video-Projects/NNN_Slug/
  01_Script/          master script + part scripts
  02_Voiceover/       VO text and masters
  04_Generated-Clips/ raw Veo takes (never edited, never deleted)
  07_Edit-Project/    plate boards (parts/part-NN_plates_v01.json), part status, builders
  08_Thumbnail/       thumbs and Short covers
  09_Final-Export/    <slug>_full_v0N.mp4
  10_Shorts/          Short scripts and cuts
  11_Upload-Package/  vidIQ audit, topic score, titles, descriptions, upload results
  production-status.md
```

## Naming

```
<project>_<part-or-scene>_<asset>_v<NN>.<ext>
hos_003_part01_rough_v03.mp4
hos_001_germs_full_v02.mp4
```

Versions only go up. If v02 fails, the next attempt is v03; v02 is never reused or overwritten. Raw generations are never edited or deleted: mark a reject in the part's status file and leave the file. Media stays out of git; record paths and sha256 instead.
