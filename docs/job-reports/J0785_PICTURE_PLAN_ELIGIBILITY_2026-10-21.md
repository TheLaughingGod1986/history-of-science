# J0785 — HOS picture-plan prerequisite check

Codex, 21 October 2026. Advisory findings only; no stage approval.

The job requires a film with locked VO and no picture plan. None was found on main (`2db81a21`).

| Film | Latest tracked plan | Rows |
|---|---|---:|
| 006 | `006_Trees-Are-Made-Of-Air/07_Edit-Project/PICTURE_PLAN_v01.json` | 92 |
| 007 | `007_The-First-Vaccine/07_Edit-Project/PICTURE_PLAN_v02.json` | 96 |
| 008 | `008_Lightning-Franklin/07_Edit-Project/PICTURE_PLAN_v03.json` | 112 |
| 009 | `009_The-Falling-Moon-Gravity/07_Edit-Project/PICTURE_PLAN_v04.json` | 90 |
| 010 | `010_Alvarez-Clay-Line-Dinosaurs/07_Edit-Project/PICTURE_PLAN_v02.json` | 72 |

HOS 006 picture is already complete according to the pipeline. HOS 007–010 already have priced plans and part boards. HOS 013 has no tracked locked VO directory; its production-status.md says VO waits Chief review. Later script drafts do not supply a locked take to plan from.

The shared HOS checkout additionally contains newer local planning files (009 v05, 010 v03 and 013 pre-VO v02). They were not copied into this clean branch or treated as merged authority. The local 013 plan explicitly waits for long VO lock before Scribe retiming.

## Handoff

Parked for Chief: price pass; no eligible unplanned film with locked VO. Chief should identify an existing plan needing price review, or supply the next film and approved locked VO before new board work. Existing boards were not duplicated. No film stage or owner was changed because no eligible film was selected.

No generation, spend, upload, scheduling or YouTube changes. No film stage marked complete.

## Validation

`git diff --check` succeeded. Required check_all.sh ran; full result was SOME CHECKS FAILED. Contract tests and package-lint could not run in the clean worktree because vitest/tsx dependencies are absent from the offline npm cache. See the accompanying check log. No test was changed.

## Disk preflight

9.1 GiB free; NAS mounted via NFS. Inspected named scratch folders are v01 working folders; no version older than current and previous was established. Active files were preserved. Disk remains below the 20 GB target; archive work needs a claimed film stage and verified obsolete versions.
