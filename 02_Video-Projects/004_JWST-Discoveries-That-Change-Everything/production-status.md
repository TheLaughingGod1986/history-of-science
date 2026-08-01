# Video 004 — JWST Discoveries That Change Everything

**Status:** Title A locked · VO **16.4 min** · captions ✓ · SFX pack ✓ · music bed plan ready · **Omni CG 5/24** — **BLOCKED: ElevenLabs Image/Video credits** (upgrade wall). Resume CG when credits refresh.  
**Folder:** `02_Video-Projects/004_JWST-Discoveries-That-Change-Everything`  
**Scheduled slot:** Thu **28 Aug 2026 · 19:00 UK**  
**Format:** Full CG · Orbit *in* scene + **chapter cards restored**

## Carry forward from V003 feedback (~95%)

| Keep | Change for V004 |
|------|-----------------|
| Audio / VO settings spot-on | Same Ben Orbit Narrator lock ✓ |
| Orbit in *every* scene | Keep full-CG travelogue |
| Visuals / intro / outro | Same brand sting + like/subscribe CTA |
| Wonder tone, no fearbait | Same |
| — | **Chapter cards** ✓ (6 locked stills) |
| — | **Scene SFX from script cues** ✓ (new workflow) |
| — | **VO → SRT captions** ✓ (new workflow) |

## Locked

**Title A:** What the James Webb Telescope Discovered That Changes Everything | Orbit's Cosmic Journey  
**Score sheet:** `11_Upload-Package/Titles/VIDIQ_TITLE_SCORE_SHEET.md` — fill live vidIQ scores when research profile is logged in (gate ≥90).

**VO master:** `02_Voiceover/05_Master/jwst_voiceover_v01_ivc_kDch_master.wav` (**16.4 min**)  
**Captions:** `02_Voiceover/06_Captions/jwst-voiceover-v01-ivc-kdch-master.srt`

## Production order

1. ~~Script MASTER + chapter-card stills~~  
2. ~~Title A lock + narration + VO~~  
3. ~~Individual Omni prompts (8 scenes × A/B/C)~~  
4. ~~Script SFX cues + generate pack + VO captions~~ *(new workflow)*  
5. **Next:** CG gen hero-first (`03_Animation-Prompts/03_Generation-Logs/jwst_generation_queue_v01.md`) → VO-locked edit with chapter cards + SFX/captions → full music bed when Music credits allow → thumbs → Shorts  

## Assets

| Asset | Path |
|-------|------|
| Script MASTER | `01_Script/jwst_script_master_v01.md` *(8 `[SFX:]` cues)* |
| Narration only | `01_Script/jwst_narration_only_v01.txt` |
| **VO master v01** | `02_Voiceover/05_Master/jwst_voiceover_v01_ivc_kDch_master.wav` |
| **Captions SRT** | `02_Voiceover/06_Captions/jwst-voiceover-v01-ivc-kdch-master.srt` |
| VO report | `02_Voiceover/vo_generation_report_v01.json` |
| **SFX pack** | `06_Sound-Effects/generated_v01/` (8 clips + manifest) |
| Music (existing beds) | `05_Music/jwst_score_ambient_v16.wav` · `jwst_score_cinematic_v19.wav` |
| Music plan (3 min bed) | `05_Music/jwst_score_bed_v01_plan.json` — *generate when Music credits refresh* |
| Soft sting | `05_Music/jwst_score_bed_sting_v01.mp3` |
| Omni prompts | `03_Animation-Prompts/02_Individual-Prompts/` |
| Gen queue | `03_Animation-Prompts/03_Generation-Logs/jwst_generation_queue_v01.md` |
| Chapter cards | `04_Generated-Clips/03_Polished/chapter_cards/` |
| vidIQ score sheet | `11_Upload-Package/Titles/VIDIQ_TITLE_SCORE_SHEET.md` |
| Ranking | `11_Upload-Package/RANKING_STRATEGY_v01.md` |
| Shorts cluster | `10_Shorts/SHORTS_CLUSTER.md` |

### VO settings (locked)

Ben Orbit Narrator `kDch6ACCIpqgQ0NsU9kk` · `eleven_v3` · stab 0.34 · sim 0.78 · style 0.42 · speed 1.04

## Gen order (hero first)

1. 04 galaxies too early · 05 black holes too soon · 02 meet JWST  
2. 06 textbook gap · 03 dawn map · 07 what changes  
3. 01 hook · 08 close  

Ref: `01_Orbit-Character/05_Seedance-References/orbit-seedance-reference-v01.png`

## Edit notes (when CG unblocks)

- Duck existing ambient/cinematic beds under VO; drop scene SFX on markers from script.  
- Sync captions from `06_Captions/*.srt`.  
- When Music credits return: `python3 04_Audio/tools/generate_music_bed.py … --generate` using `jwst_score_bed_v01_plan.json` prompt.  
- Still: re-score Title ABC in vidIQ before upload package final.
