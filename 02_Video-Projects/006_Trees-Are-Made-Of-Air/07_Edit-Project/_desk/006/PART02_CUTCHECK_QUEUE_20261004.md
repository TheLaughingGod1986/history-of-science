# Part 02 overnight cut-checker — queued (advisory)

Authority: Claude #180 5981276239.

## Rough ready
- `07_Edit-Project/_precheck/hos_006_part02_keep_spine_rough_v01.mp4` (KEEP spine only)
- Meta: `_precheck/part02_assemble/ROUGH_META.json`
- Includes: 01, 02→09 stand-in, 03–06t2 (covers CUT 07), 08 trim 3.5s, 09, 10, 13
- **Excluded:** PENDING 12 + 14–22 until Claude KEEP/FAIL on `uat_pending/` quads

## Checker
- Tool: `_vision_precheck_v01.py` (Part 01 pilot) — advisory only; adapt paths or run freezedetect pass on the rough overnight.
- Reminder: after Tdarr window / alongside Wan-LTX queue (~22:19). Do not block UAT.

## Blocking full Part 02 rough
Claude UAT on ten pending sheets. After KEEP/FAIL, rebuild rough and re-run checker.
