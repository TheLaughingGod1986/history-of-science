# Visual Remaster v02 — 001 Will We Ever Meet Aliens?

**Goal:** Every VO idea gets a matching, mysterious, premium visual.  
**Feel:** Pixar warmth × Nat Geo awe × careful alien mystery (not conspiracy cinema).  
**Status:** Remaster plan + prompt pack ready · generate → select → rebuild EDL → export `aliens_broadcast_v02.mp4`

---

## Diagnosis (current `aliens_broadcast_v01`)

| Problem | Evidence | Fix |
|---------|----------|-----|
| **Generic space wallpaper** | Long nebula / starfield holds while VO names fleets, megastructures, city lights, zoo | VO-locked shots: show the *named* thing |
| **Cuts too long** | Many segments 14–22s on one plate | Target **3–7s** per idea in mystery sections |
| **Orbit overused as PiP** | Explaining Orbit almost continuous | Orbit only on emotional beats; full-frame mystery elsewhere |
| **Too “Earth science doc”** | Radio dishes / abstract grids dominate | Lead with **alien worlds, craft, stations, artifacts, glimpses** |
| **Mystery undersold** | Silence spoken over pretty stars | Silence = *absence of expected lights* (dark exoplanet nightside, empty fleet lane) |

What already works (keep): cinematic grade, Orbit brand, some megastructure / network plates as supporting texture — not as the whole film.

---

## Visual grammar (non-negotiable)

### 1. Picture-lock rule
If the VO says it, the audience should *see a version of it within ~1 second*:

| VO phrase | Must show |
|-----------|-----------|
| crowded sky / billions of stars | dense Milky Way |
| where is everybody? | smash to emptiness / dark nightside |
| city lights on exoplanets | glowing alien city grid on nightside — then cut to **none** |
| megastructures | Dyson-swarm / ring / orbital lattice silhouette |
| visiting fleets | distant formation lights, no Hollywood armada close-up |
| carefully quiet / zoo | Earth observed through soft “glass” / one-way veil |
| ship at fraction of light speed | tiny craft, centuries of stars drifting |
| spectrum / fingerprint / molecule | atmospheric spectral ribbons / data-as-beauty |
| Wow! signal | single bright pulse → void |
| icy moons / microbe | Europa-like ice + subsurface glow |
| face to faceplate | Orbit + distant silhouette (never handshake CGI) |

### 2. Alien imagery rules (brand-safe mystery)

**Do**
- Alien **planets** with wrong skies, glass-rain limbs, violet oceans, double suns  
- **Spacecraft** as silhouettes / running lights  
- **Stations** as impossible architecture  
- **Artifacts** as rings, monoliths, abandoned beacons  
- **Glimpses** of beings: shadow on ridge, shape behind frosted glass, tiny figure on station rim — 1–2 seconds max  

**Don’t**
- Grey alien close-ups, abduction horror, conspiracy glyphs, UFO over landmarks  
- Blood / body horror  
- Readable alien language text / logos  
- Constant “proving aliens exist” energy — we show *possibility*, not certainty  

### 3. Orbit usage

| Mode | When |
|------|------|
| **Full-frame Orbit** | Intro “I’m Orbit”, ending reflection |
| **PiP Orbit** | Curious / shocked / thoughtful on key turns only (~20–30% of runtime) |
| **No Orbit** | Pure mystery B-roll for fleets, cities, artifacts, glimpses |

### 4. Edit rhythm

- Cold open + Fermi list: **3–5s** cuts  
- Explanations montage: **4–6s**  
- Detection / science: **5–8s**  
- Ending: slower **8–12s** holds  

Music: keep ambient bed; add **one** low pulse under “where is everybody?” and Wow! beat.

---

## Remaster deliverables

| File | Role |
|------|------|
| `VISUAL_REMASTER_v02.md` | This bible |
| `VO_LOCKED_SHOTLIST_v02.json` | Section → shot map |
| `04_Remaster-v02/_PASTE_READY/` | Seedance prompts (priority batch) |
| `GENERATION_QUEUE_v02.md` | Order + status |
| Later: `SECTION_EDL_v02.json` + `aliens_broadcast_v02.mp4` | After clips land |

---

## Priority generation batch (do these first)

**Batch A — Fermi list (highest retention impact)**  
A1 exoplanet city lights · A2 empty nightside · A3 megastructure · A4 fleet silhouette · A5 radio silence void  

**Batch B — Explanations**  
B1 rare intelligence timeline · B2 short-lived civ lights dying · B3 zoo observation veil · B4 early party / young rocky worlds  

**Batch C — Contact imagination**  
C1 slow ship · C2 spectral fingerprint world · C3 Wow pulse · C4 Europa under-ice · C5 artifact beacon · C6 silhouette glimpse  

**Batch D — Polish**  
D1 title mystery plate · D2 ending quiet invitation sky  

Est. ~16–20 clips × 5s Seedance. Generate **≥2 takes** on A1–A4 and C6.

---

## Rebuild steps (after generation)

1. Download all takes → `04_Generated-Clips/01_Raw/broll_mystery_v02/`  
2. Select best → `02_Selected/` then polish trim → `03_Polished/broll_mystery_v02/`  
3. Build `SECTION_EDL_v02.json` from shotlist timings  
4. `python3 _build_polished_broadcast.py` (point at v02 EDL)  
5. CapCut pass: captions optional, title card, end screen  
6. Compare side-by-side v01 vs v02 at Fermi section — ship only if picture-lock clear  

---

## Success criteria

- Viewer can mute and still *feel* “aliens / silence / distance / search”  
- Every major VO noun has a matching plate within 1s  
- At least **8** distinct alien-civilisation images (city, craft, station, artifact, glimpse, megastructure, weird world, under-ice)  
- Orbit guide, not wallpaper  
- Still: wonder over certainty — no conspiracy tone
