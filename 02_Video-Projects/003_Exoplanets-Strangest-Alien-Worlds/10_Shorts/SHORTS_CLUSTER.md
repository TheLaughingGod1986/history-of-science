# Shorts Cluster — Video 003 Exoplanets

**Long-form:** Alien Worlds: The Strangest Planets We've Ever Found | Orbit's Cosmic Journey  
**Channel:** Orbit with Ben · @OrbitWithBen  
**Cluster:** 6 Shorts · ~40–50s each · **pillar first**  
**Style:** Same full-CG travelogue as the long — Orbit *in* scene, picture matches VO, Pixar-warm × hard astrophysics  
**On-screen text:** yellow/white lowercase kinetic captions (`SHORTS_ONSCREEN_TEXT_STYLE.md`) — builders `*_shorts_v02.py`  
**Strategy:** `00_Brand/Channel-Setup/PUBLISHING_AND_SHORTS_STRATEGY.md`

## Publish order (pillar-first)

| When (UK) | Asset |
|-----------|--------|
| **Thu 21 Aug 2026 · 19:00** | **Long-form public first** |
| Thu 21 Aug · 21:00 | **S01** — glass rain sideways (strongest hook) |
| Fri 22 Aug · 12:30 | **S02** — diamond world |
| Sat 23 Aug · 12:30 | **S03** — three suns |
| Sun 24 Aug · 12:30 | **S04** — hottest nights |
| Mon 25 Aug · 12:30 | **S05** — eyeball planets |
| Tue 26 Aug · 12:30 | **S06** — could any host life? |

Do **not** publish any Short before the long is public.

## Cluster map

| ID | Hook | Source scene | Working title |
|----|------|--------------|---------------|
| S01 | The planet where it rains glass sideways | 05 | `exoplanets_short-01_glass-rain_v01.mp4` |
| S02 | A world made of diamond? | 04 | `exoplanets_short-02_diamond_v01.mp4` |
| S03 | Three suns in the sky | 06 | `exoplanets_short-03_three-suns_v01.mp4` |
| S04 | The hottest nights in the universe | 07 | `exoplanets_short-04_hot-jupiter_v01.mp4` |
| S05 | Eyeball planets explained | 08 | `exoplanets_short-05_eyeball_v01.mp4` |
| S06 | Could any of these host life? | 09 | `exoplanets_short-06_habitability_v01.mp4` |

## Soft ending / Related

- End card: `WATCH THE FULL STORY →`
- Related video → this long-form once public
- Replace `{{LONG_VIDEO_URL}}` after long URL is live

## Builder (after long master + VO timestamps lock)

- v01 (legacy chrome): `_build_exoplanets_shorts_v01.py`
- **v02 (TikTok kinetic captions):** `_build_exoplanets_shorts_v02.py`  
  `python3 _build_exoplanets_shorts_v02.py` or pass a slug e.g. `glass-rain`

## Cutscene rules

Unique plates · no loops · Orbit character bed may loop · no Ken Burns on text cards
