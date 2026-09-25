# Episode template

Copy this folder to start a new long:

```bash
cp -R 02_Video-Projects/_template_NNN_Episode-Slug 02_Video-Projects/004_<Slug>
```

Full steps: `00_Brand/Channel-Setup/STUDIO_PLAYBOOK.md`. Stop for Ben's OK at every sign-off in `AGENTS.md`.

## Order

1. **Topic** (`STUDIO_PLAYBOOK.md` §2): fill `11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md` and `TOPIC_OPPORTUNITY_SCORE.md` (template in `00_Brand/Channel-Setup/templates/`). Ben picks.
2. **Script:** write `01_Script/<slug>_script_master_v01.md` from `episode_script_draft_v01.md`, then split it into five part scripts.
3. **Gates** (both before any VO or picture spend):
   ```bash
   cd 07_Content-Ops
   npm run review:script -- --file ../02_Video-Projects/<NNN_Slug>/01_Script/<master>.md   # ≥90
   npm run gate:episode -- --project ../02_Video-Projects/<NNN_Slug>                     # PASS
   ```
4. **VO** per part: Ben Orbit Narrator → `02_Voiceover/`.
5. **Plate boards** per part: `07_Edit-Project/parts/part-NN_plates_v01.json` (copy the example).
6. **Picture:** Flow Veo 3.1, one plate at a time until the first KEEP, plate UAT on continuous playback, assemble last (`STUDIO_PLAYBOOK.md` §5).
7. **Assemble** parts → `09_Final-Export/<slug>_full_v0N.mp4` with the cream end card (§7).
8. **Thumbnails** (`08_Thumbnail/`), **Shorts** (`10_Shorts/`), checklist, then the YouTube package upload (§9). Normal publish, Thursday 18:00, no Premiere.

Keep `production-status.md` current on `main`.
