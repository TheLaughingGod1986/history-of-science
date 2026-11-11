Codex covering J2642: chained-reading reconciliation completed for every qualifying take.

26 posted events appended through SharedFlowAccounting.reconcile_posted under the existing writer lock: 2,600 credits. Unposted and total liability: 3,400 → 800 credits. Eight takes remain unposted, detailed below. No browser, generation, spend, submit, bypass or stage approval.

Each pair uses recorded Configured UI before Create observations in orbit-with-ben/05_Analytics/ai_spend/ledger.jsonl, or the daily UI reader; the original charged UI balance agrees. Timestamps increase, the fall is exactly 100, and the original account.jsonl contains no other accounting event between qualifying pairs. Endpoint charge/intent belongs to the next reading and is not an intervening charge. Reservations/releases at the endpoint are conservatively retained. The 20:29:45Z same-take verification at 14,590 was excluded.

The day balance fell 4,450 (14,890 → 10,440). Recorded net Flow spend is 4,600, less rods 100 and unexplained 50 = 4,450. No film 010 posting changed.

Posted takes (both reading line numbers refer to the spend log above):

| Charge | Before → after | Lines |
|---|---:|---|
| HOS:009:P02:10_how_high:t1 | 14890 → 14790 | 620 → 622 |
| HOS:009:P03:07_ball_to_moon:t1 | 14790 → 14690 | 622 → 625 |
| HOS:009:P01:05_heavens_map_c1:t1 | 14690 → 14590 | 625 → 627 |
| HOS:009:P01:07_night_field_c1:t1 | 14590 → 14490 | 627 → 630 |
| HOS:009:P02:01_cambridge_closes_c1:t1 | 14490 → 14390 | 630 → 632 |
| HOS:009:P02:03_christmas_birth_c1:t1 | 14390 → 14290 | 632 → 634 |
| HOS:009:P02:05_working_alone_c1:t1 | 14290 → 14190 | 634 → 637 |
| HOS:009:P02:08_the_apple_c1:t1 | 14190 → 14090 | 637 → 639 |
| HOS:009:P02:11_explorer_apple_c1:t1 | 14090 → 13990 | 639 → 641 |
| HOS:009:P03:01_really_falling_c1:t1 | 13990 → 13890 | 641 → 643 |
| HOS:009:P03:05_shot_orbit_c1:t1 | 13890 → 13790 | 643 → 645 |
| HOS:009:P03:05_shot_orbit_c2:t1 | 13790 → 13690 | 645 → 647 |
| HOS:009:P04:05_minute_second_c1:t1 | 13690 → 13590 | 647 → 649 |
| HOS:009:P04:05_minute_second_c2:t1 | 13590 → 13490 | 649 → 651 |
| HOS:009:P04:08_halley_visit_c1:t2 | 13490 → 13390 | 655 → 657 |
| HOS:009:P04:08_halley_visit_c2:t1 | 13390 → 13290 | 657 → 659 |
| HOS:009:P05:04_comet_1758_c1:t1 | 13290 → 13190 | 659 → 661 |
| HOS:009:P05:05_iss_orbit_c1:t1 | 13190 → 13090 | 661 → 663 |
| HOS:009:P05:05_iss_orbit_c2:t1 | 13090 → 12990 | 663 → 667 |
| HOS:008:P02:02_salon_spark:J2241:t1 | 12890 → 12790 | 669 → 671 |
| HOS:008:P03:01_points_desk:J2241:t1 | 12790 → 12690 | 671 → 673 |
| HOS:008:P02:02_salon_spark:J2241:t2 | 12090 → 11990 | 693 → 695 |
| HOS:008:P02:02_salon_spark:J2241:t3 | 11890 → 11790 | 697 → 699 |
| HOS:009:P03:01_really_falling_c1:t2 | 11590 → 11490 | 704 → 706 |
| HOS:009:P02:08_the_apple_c1:t2 | 11490 → 11390 | 706 → 708 |
| HOS:009:P03:01_really_falling_c1:t3 | 10840 → 10740 | 721 → 723 |

Unposted takes:

- HOS:009:P05:06_iss_apple_c1:t1: 12990 at 2026-11-11T05:08:17+00:00 → 12890 at 2026-11-11T06:40:44+00:00 (spend lines 667 → 669). test 2: intervening ledger events.
  - 2026-11-11T05:53:45+00:00 release J2033
  - 2026-11-11T06:39:44+00:00 reserve J2241

- HOS:008:P05:13_rods_spread:J2241:t1: 12690 at 2026-11-11T06:45:09+00:00 → 12690 at 2026-11-11T08:12:34+00:00 (spend lines 673 → 675). unchanged balance; existing reversal API is policy-refusal only, not a generic failed-take refund.

- HOS:008:P05:13_rods_spread:J2241:t2: 12690 at 2026-11-11T08:12:34+00:00 → 12590.0 at 2026-11-11T08:30:20Z (spend lines 675 → 679). test 2: intervening ledger events.
  - 2026-11-11T08:13:52+00:00 release J2241

- HOS:008:P03:01_points_desk:J2241:t2: 11990 at 2026-11-11T09:40:01+00:00 → 11890 at 2026-11-11T10:30:19+00:00 (spend lines 695 → 697). test 2: intervening ledger events.
  - 2026-11-11T09:41:11+00:00 release J2575
  - 2026-11-11T10:29:33+00:00 reserve J2589

- HOS:008:P03:01_points_desk:J2241:t3: 11790 at 2026-11-11T10:32:26+00:00 → 11690 at 2026-11-11T12:21:17+00:00 (spend lines 699 → 702). test 2: intervening ledger events.
  - 2026-11-11T10:33:46+00:00 release J2589
  - 2026-11-11T12:20:16+00:00 reserve J2598

- HOS:008:P02:02_salon_spark:J2241:t4: 11690 at 2026-11-11T12:21:17+00:00 → 11590 at 2026-11-11T14:13:07+00:00 (spend lines 702 → 704). test 2: intervening ledger events.
  - 2026-11-11T12:22:42+00:00 release J2598
  - 2026-11-11T14:13:07+00:00 reserve J2583

- HOS:009:P04:05_minute_second_c1:t2: 11390 at 2026-11-11T14:17:42+00:00 → 11290 at 2026-11-11T15:10:37+00:00 (spend lines 708 → 711). test 2: intervening ledger events.
  - 2026-11-11T14:19:11+00:00 release J2583

- HOS:009:P04:05_minute_second_c1:t3: 10740 at 2026-11-11T15:33:26+00:00 → 10640 at 2026-11-11T19:08:53+00:00 (spend lines 723 → 726). test 2: intervening ledger events.
  - 2026-11-11T15:37:05+00:00 release J2626

Rods: no existing per-key refund/release found. The only existing reversal is reverse_policy_refusal (policy_refused, POLICY_REFUSED); its documented condition is a content-policy refusal. J2241/Chief evidence describes failure with refund promised, rather than policy refusal. Per the brief’s explicit stop-on-this-take allowance, no generic refund or new evidence kind was invented and no reversal was appended. Chief can scope a reviewed general failed-take refund path or explicitly determine applicability of the existing policy-specific method.

All account and spend events in the film 010 clay window (inclusive 15:19:39Z–15:31:18Z), retained for Chief ruling:

```json
{
  "account": [
    {
      "amount": 100,
      "at": "2026-11-11T15:19:39+00:00",
      "id": "HOS:010:P05:12_clay_callback:t1",
      "kind": "intent",
      "reservation": "HOS010_TWELVE_PLATES_J2270"
    },
    {
      "at": "2026-11-11T15:19:39+00:00",
      "id": "HOS:010:P05:12_clay_callback:t1",
      "kind": "charged"
    },
    {
      "at": "2026-11-11T15:21:00+00:00",
      "id": "HOS:010:P05:12_clay_callback:t1",
      "kind": "posted"
    },
    {
      "at": "2026-11-11T15:31:18+00:00",
      "cap": 200,
      "film": "HOS:009",
      "id": "J2626",
      "kind": "reserve"
    },
    {
      "amount": 100,
      "at": "2026-11-11T15:31:18+00:00",
      "id": "HOS:009:P03:01_really_falling_c1:t3",
      "kind": "intent",
      "reservation": "J2626"
    },
    {
      "at": "2026-11-11T15:31:18+00:00",
      "id": "HOS:009:P03:01_really_falling_c1:t3",
      "kind": "charged"
    }
  ],
  "spend": [
    {
      "at": "2026-11-11T15:19:39+00:00",
      "by": "gemini",
      "charge": "HOS:010:P05:12_clay_callback:t1",
      "id": "flow:read:HOS:010:P05:12_clay_callback:t1",
      "kind": "record",
      "left": 10890,
      "note": "Configured UI before Create",
      "pool": "flow",
      "source": "shared-flow",
      "line": 719
    },
    {
      "amount": 100,
      "at": "2026-11-11T15:19:39+00:00",
      "by": "gemini",
      "charge": "HOS:010:P05:12_clay_callback:t1",
      "film": "HOS:010",
      "id": "flow:spend:HOS:010:P05:12_clay_callback:t1",
      "kind": "spend",
      "pool": "flow",
      "source": "shared-flow",
      "what": "HOS:010:P05:12_clay_callback:t1",
      "line": 720
    },
    {
      "at": "2026-11-11T15:31:18+00:00",
      "by": "codex",
      "charge": "HOS:009:P03:01_really_falling_c1:t3",
      "id": "flow:read:HOS:009:P03:01_really_falling_c1:t3",
      "kind": "record",
      "left": 10840,
      "note": "Configured UI before Create",
      "pool": "flow",
      "source": "shared-flow",
      "line": 721
    },
    {
      "amount": 100,
      "at": "2026-11-11T15:31:18+00:00",
      "by": "codex",
      "charge": "HOS:009:P03:01_really_falling_c1:t3",
      "film": "HOS:009",
      "id": "flow:spend:HOS:009:P03:01_really_falling_c1:t3",
      "kind": "spend",
      "pool": "flow",
      "source": "shared-flow",
      "what": "HOS:009:P03:01_really_falling_c1:t3",
      "line": 722
    }
  ]
}
```

Next: J2644 may run its fresh dry-run as the brief permits despite unposted exceptions. Chief decides the seven test-2 exceptions, rods reversal applicability and the film 010 unexplained 50. This job gives no production approval.

Verification: runner parser accepted the before and after ledgers; 26 new posted events, zero changes to spend log, unposted 800. Detailed per-take evidence and hashes: CHAINED_RESULT.json. Prior stopped-run records are retained.
