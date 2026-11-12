# J2481 — HOS 009 Flow Page Reader Repair (10 Nov 2026)

## 1. Summary

- **Job**: `J2481` (`HOS:009` picture)
- **Submissions / Spend**: **`0` submissions**, **`0` plates generated**, **`0` credits spent** (`14,890 Google Flow credits` before and after read-only probe; `£0`).
- **Scope**:
  1. **Model reader (`CREATE_EVIDENCE_JS`, `STILL_EVIDENCE_JS`)**: Reads enabled `button[aria-label='Select model family']` (stripping trailing `arrow_drop_down` and leading `🍌 `) in addition to legacy `[aria-selected="true"],[aria-checked="true"],[aria-pressed="true"],select option:checked`. Fails closed (`models: []`) if any `Select model family` button displays an unknown model name outside the explicit allowlist (`Veo 3.1 - Quality`, `Veo 3.1 - Fast`, `Veo 3.1 - Lite` for video; `Nano Banana 2`, `Nano Banana 2.1` for still reader parsing).
  2. **Aspect reader**: Maps exact radio button strings (`"crop_16_9 16:9"` / `"16:9"`, `"crop_9_16 9:16"` / `"9:16"`, `"crop_landscape 4:3"` / `"4:3"`, `"crop_square 1:1"` / `"1:1"`, `"crop_portrait 3:4"` / `"3:4"`) and refuses any unknown or non-`16:9` aspect.
  3. **Balance step (`BALANCE_EVIDENCE_JS`, `read_live_balance`)**: Matches both `"<N> Google Flow credits"` and legacy `"<N> AI credits"`, reads and validates the balance in its own step before `Settings trigger` is opened (closing `Account details` afterward because the two CDK overlays are mutually exclusive), and carries the validated integer balance into `read_live_evidence` / `guarded_create` / `read_live_still_evidence` / `guarded_still_create`.
  4. **Plan-driven `style_refs` (`_flow_still_v01.py`)**: Removed the hardcoded HOS 006 `MEDIA_CLIPS` / `STYLE_REFS` constants. `style_refs_from_plan(plan_path, media_root)` resolves relative `style_refs` from the film's plan JSON (`PICTURE_PLAN_v04.json` for HOS 009; `PICTURE_PLAN_v01.json` for HOS 006) under `media_root` and rejects missing or path-traversal entries.
  5. **`REQUIRED_STILL_MODEL` kept at `"Nano Banana 2"`**: Per J2481 brief, `"Nano Banana 2.1"` is **not** added to `REQUIRED_STILL_MODEL` (`read_live_still_evidence` still fails closed on `"Nano Banana 2.1"` until the Chief's price pass).

## 2. Live Read-Only Flow Verification (CDP `:9222`, 0 Submissions)

Executed against live Flow (`https://flow.google.com/project/13d84783-a17a-495c-bacd-0cf0e736f6f4`) via `open_flow_page` (`cdp_tabs.reuse_page`), submitting nothing:

```json
{
  "url": "https://flow.google.com/project/13d84783-a17a-495c-bacd-0cf0e736f6f4",
  "balance_before": 14890,
  "balance_after": 14890,
  "video_raw_evidence": {
    "host": "flow.google.com",
    "models": [
      "Veo 3.1 - Quality"
    ],
    "outputs": [
      "x1"
    ],
    "aspects": [
      "16:9"
    ],
    "durations": [
      "8s"
    ],
    "accounts": [
      "<REDACTED_ACCOUNT>"
    ],
    "prices": [
      "Generating will use 100 credits"
    ],
    "balances": [],
    "ultra": true,
    "create_count": 0
  },
  "still_raw_evidence": {
    "host": "flow.google.com",
    "models": [
      "Nano Banana 2.1"
    ],
    "outputs": [
      "x1"
    ],
    "aspects": [
      "16:9"
    ],
    "accounts": [
      "<REDACTED_ACCOUNT>"
    ],
    "prices": [
      "Generating will use 0 credits"
    ],
    "balances": [],
    "ultra": true,
    "create_count": 0
  },
  "still_guard_result": "GuardError: live Flow still selected controls/account/entitlement/zero-price are missing or changed",
  "image_model_menu_items": [
    "🍌 Nano Banana 2.1 crop_16_9 x1",
    "image Image",
    "🍌 Nano Banana 2.1 arrow_drop_down",
    "🍌 Nano Banana Pro",
    "🍌 Nano Banana 2 Lite",
    "🍌 Nano Banana 2.1"
  ]
}
```

## 3. Chief Price Pass Report: `"🍌 Nano Banana 2.1"`

- **What Flow shows as its cost per image**: **`"Generating will use 0 credits"`** (`0` credits per `x1` `16:9` image on Ultra).
- **Whether it is the same model tier the HOS 009 plan priced**: **Yes.** In the live Flow Image model family menu, the three tiers are now `🍌 Nano Banana Pro`, `🍌 Nano Banana 2 Lite`, and `🍌 Nano Banana 2.1` (default). `Nano Banana 2` is no longer listed separately; Google Flow upgraded/renamed the standard 0-credit `Nano Banana 2` slot in-place to `🍌 Nano Banana 2.1` at the same `0`-credit Ultra price (`PICTURE_PLAN_v04.json` / `TRANCHE2_SCOPE_J2026.json` priced start stills at `0` credits).
- **Current guard status**: `REQUIRED_STILL_MODEL` in `_mint_flow_v05_tranche2.py` remains `"Nano Banana 2"`, so `read_live_still_evidence` fails closed until the Chief approves `"Nano Banana 2.1"`.

## 4. Verification Output

- `python3 -m unittest discover -s tests -p "test_hos009_tranche2_runner.py" -v`: **`Ran 64 tests in 4.424s — OK`** (covers both `jobs/reviews/J2033/LIVE_DOM_CAPTURE_2026-11-10.json` and legacy DOM fixtures, balance carry, fail-closed unknown models/aspects/balances, and plan-based `style_refs`).
- `00_Brand/Channel-Setup/tools/check_all.sh 02_Video-Projects/009_The-Falling-Moon-Gravity`: **`ALL CHECKS PASS`**.
