# Production status — 001 How Did We Discover Germs?

| Step | Status |
|---|---|
| Topic score | DONE |
| Cluster plan | DONE |
| Pre-build VidIQ audit | SIGNED (live VidIQ re-score before upload) |
| Master script | `germs_script_master_v01.md` |
| Script review | **PASS 90.4** |
| Episode gate | **PASS** |
| Part 01 VO | DONE · ~84s Ben Orbit Narrator |
| Part 01 Veo | **PARTIAL** — 3/10 plates (Gemini 429 quota). Explorer deferred. |
| Part 01 rough | `hos_001_part01_partial_v01.mp4` (~23s picture under VO open) |
| Parts 02–05 | Blocked on Ben UAT + Veo quota recovery |
| Broadcast + Shorts | Later |

## Artifacts

- VO: `/opt/cursor/artifacts/part01_invisible_enemy_v01.mp3`
- Partial rough: `/opt/cursor/artifacts/hos_001_part01_partial_v01.mp4`
- Style test (locked): `/opt/cursor/artifacts/hos_explorer_style_test_30s_v01.mp4`

## Blocker

Gemini Developer API **RESOURCE_EXHAUSTED** after plates 01–03. Resume `_build_part01_rough_v01.py` when quota resets (skip-existing keeps the three good plates).

**Do not start Part 02 until Ben passes Part 01.**
