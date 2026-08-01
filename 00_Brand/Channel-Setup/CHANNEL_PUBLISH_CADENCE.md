# Orbit with Ben — publish cadence

Timezone: **Europe/London**  
Canonical strategy: `PUBLISHING_AND_SHORTS_STRATEGY.md`  
Source of truth: `OPTIMAL_PUBLISH_SCHEDULE.json`  
Latest audit: `audits/CHANNEL_AUDIT_2026-08-01.md`  
Updated: **2026-08-01**

## Cadence rule

| Cadence | Slot | Time UK | Why |
|---------|------|---------|-----|
| **1 long-form / week** | **Thursday** | **19:00** | Pillar first · UK evening · US afternoon |
| **5–7 Shorts / week** | **Thu evening → Wed** | **21:00** (Day 1) · **12:30** (Days 2–7) | Support the pillar · midday discovery |

**Cluster:** Long first → Short #1 after 1–3h → one Short per day for Days 2–7.

Never publish a teaser Short before the long is public.  
Never dump the full Shorts cluster on Day 1.  
Never use fearbait titles (even if vidIQ scores them higher).

---

## Cold-start override (until ≥500 views or ≥20 subs)

From audit 2026-08-01: Shorts **~99 views / peak VPH ~53** vs long **5 views**.  
→ **Zero Short gaps.** Judge topics by Short velocity. Next pillar = **black hole** (kw ~586K · title score 98).

Re-run `vidiq_subscriber_insights` before moving clocks.

---

## Weekly pattern

```
Thu 19:00  →  Long-form (pillar)
Thu 21:00  →  Short #1 (strongest hook)
Fri 12:30  →  Short #2
Sat 12:30  →  Short #3
Sun 12:30  →  Short #4
Mon 12:30  →  Short #5
Tue 12:30  →  Short #6
Wed 12:30  →  Short #7 (optional) + schedule next pillar
```

Default ops volume: **6 Shorts / long** (acceptable range **5–7**).

---

## Launch window (live · audited 2026-08-01)

| When | Asset | Status |
|------|-------|--------|
| **Live** | **V001 — Why Haven't We Found Aliens Yet?** | Public · `Mo93x0fxB1Q` · 5 views |
| **Live** | **Short #1 — Where Is Everybody? The Fermi Paradox** | Public · `z-DLqoSoEBo` · ~99 views · wonder title locked |
| **Sat 1 Aug 2026 · 12:30** | Short #2 — Space Is Rude About Distance | Scheduled · `UWwNKYf_aU8` |
| **Sun 2 Aug · 12:30** | Short #3 — What If Aliens Are Watching Us? | Scheduled · `MO19iXYCu0c` |
| **Mon 3 Aug · 12:30** | Short #4 — What If the First Alien Clue Is Already Here? | Scheduled · `--CxhjNqtSY` |

Confirm every schedule on Studio `/video/{id}/edit`. Every Short: Related → long + pin full-film comment before public.

---

## Content flywheel (every long)

5–7 Shorts · 3 X · 3 Threads · 2 LinkedIn · 3 Facebook · 1 Reddit · 1 Community poll · 1 Community image · (future: email + blog)

**Shorts auto-mirrors (when live on YouTube):**
- TikTok → `TikTok/AUTO_POST.md` (@orbitwithben)
- Instagram Reels + Facebook Page Reels → `Meta/AUTO_POST.md`

Template: `CONTENT_FLYWHEEL_TEMPLATE.md` · Checklist: `RELEASE_WEEK_CHECKLIST.md`

---

## Capacity

| Now (ops) | Later (aspirational) |
|-----------|----------------------|
| 4 longs / month · 20–28 Shorts / month | 2 longs / week when library + retention proven (≈ months 6–9+) |
