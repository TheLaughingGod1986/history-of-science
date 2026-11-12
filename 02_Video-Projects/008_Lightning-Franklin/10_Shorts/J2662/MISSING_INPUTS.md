# J2662 — MacBook source availability, 12 November 2026

Status: re-cut not performed; return to Mini/source restoration. Worker: macbook-2.

The shared working film root inspected was:
`/Volumes/data/studio-live/History Of Science/02_Video-Projects/008_Lightning-Franklin/`.

Available: `10_Shorts/hos_008_short_C_v03.mp4`, its word/meta JSON,
`10_Shorts/vo_v02/hos_008_short_C_s01_v03.wav`, the body take, and the J2255 audio stems.

Missing at that root:

- `04_Generated-Clips/part05/raw/v01/06_rod_fitting_c1_t1.mp4`
- `04_Generated-Clips/part05/raw/v01/06_rod_fitting_t1.mp4`
- `10_Shorts/J2255/_build_short_c_v03.py`

A recursive file inventory found only six MP4s under `04_Generated-Clips`,
with none of the named rod-fitting, skyline-strike or house-rod inputs.
The build script also does not exist in the local checkout or freshly fetched
`origin/main`. The NAS J2255 directory contains audio stems only.

The existing encoded master cannot provide the new source windows at 4.00 s
and 3.10 s requested for S06/S07, or restore the image outside its baked crop.
Do not crop or patch that master as a substitute for the required raw footage.

Next worker: run on the Mini if its original film folder has these inputs;
otherwise restore the named sources and build recipe into this film's working
folder, checking copied files with SHA-256, then apply all five J2485 fixes.
Use existing audio/picture only, spend £0, create a new v04 file without
replacing v03, run the Shorts gate and record the timing/caption/crop evidence.

No media was rendered, copied, replaced or deleted. No YouTube or Buffer state
was changed. No release gate or final PASS is claimed.

Repository validation (report-only change):

```text
bash 00_Brand/Channel-Setup/tools/check_all.sh
ALL CHECKS PASS
```

`git diff --check` also passed. These checks validate the repository/report,
not a v04 render; none exists from this run.

## Repeat assignment: refreshed input check

The same job was assigned again. A fresh recursive filename search across the
entire `studio-live` working store found none of the eight raw clips referenced
by the v03 recipe: `19_skyline_strike_t1.mp4`, `01_house_rod_t1.mp4`,
`07_giant_spark_t1.mp4`, `12_steeple_fire_t1.mp4`, `18_rod_closeup_t1.mp4`,
`06_rod_fitting_t1.mp4`, `06_rod_fitting_c1_t1.mp4`, `14_safe_towers_t1.mp4`.
The film's raw directory currently contains `01_Raw` and `part02`, not the
required `part01/raw/v01` and `part05/raw/v01` source trees.

The recipe is recoverable from the owner's open PR #555, head commit
`a0190a2f2af1f3296c8bc0d459dd1a506e8c4e9f`. GitHub reports OPEN and
`mergeCommit: null`, contrary to the job brief's merged claim. It was read
without executing it. Recovering this text does not restore the raw media.
PR #556 already records this blocker; this refresh updates that existing PR.

Do not repeatedly dispatch this job to the MacBook until the raw sources are
present. Resume on the Mini with its original sources, or restore the eight
clips into the existing shared film folder with SHA-256 verification.
