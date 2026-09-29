# HOS 004 full join v02 — Ben OVERRIDE (UAT)

**Cut:** `hos_004_full_join_v02.mp4`  
**sha256:** `02cf4a107caff44f08093a4231ef9dacafdde868483680df3bdc28ad8194b90a`  
**Duration:** 524.700 s (8:44.70) · **Size:** 381924174 B  
**A/V delta (audio−video):** `0.000` s  
**Status:** UAT for Ben continuous playback. Do **not** label KEEP/LOCKED. Do **not** upload.

Supersedes the discarded continuous-bed / J-cut v02 (`b20ac5a4…`) and v01 FAIL (abrupt seams + on-screen “BRIDGES TO PART 02 / CHAPTER CARD”).

## Ben OVERRIDE (29 Sep 2026)

- **KEEP** chapter cards (~1.5 s, soft, bed continuing) with **real** titles (never placeholder).
- TEMP music bed **PER PART** (beds acrossfade at joins). Final single bed after Ben picture PASS.
- **NO** one continuous bed. **NO** J-cut.
- Picture xfade **0.40 s**.
- Cream **after** last VO word (P05 STT “That's the next story” ~144.5 s): keep P05 picture+VO to last word → **4 s** cream (bed fades) → **20 s** quiet Studio hold.

## Parents (hash-checked, not reminted)

| Part | File | sha256 |
|---|---|---|
| 01 | `hos_004_part01_rough_v05.mp4` | `71d7c70798c77ce2ecb02c37ad043fd98117a2209a84899236337fee8b952add` |
| 02 | `hos_004_part02_rough_v01.mp4` | `620ce51250028495a588f25967dddfaa9c6136dc4172c7b0ce1ee609f103f1d2` |
| 03 | `hos_004_part03_rough_v01.mp4` | `d62e0ed096ead8ec52666ca07476f973aeaae7635b70a16faaac45f14ec518e0` |
| 04 | `hos_004_part04_rough_v02.mp4` | `157feaef7bd21236aeafc3e953fe461fe2ee95896bb868d57357c9c1c2c1e1f5` |
| 05 | `hos_004_part05_rough_v03.mp4` | `b391bff0dbe8a8ae0130adef4f7f3d7b79aca2cb34a934d9cf42d76e1d03363f` |

P01 bridge text plate cut @ 68.480 s. P05 parent cream from 140.50 replaced with story through 144.516 s.  
P05 land meta `parent_part04` = `hos_004_part04_rough_v02.mp4` (Ben PASS).

## Chapter cards (real titles)

| Card | Start | On-screen |
|---|---:|---|
| card02 | **1:09.43** (69.433) | PART 02 · 1808 · *The Table That Broke Its Own Rule* |
| card03 | **2:41.31** (161.311) | PART 03 · 1897 · *The Crumb Inside the Atom* |
| card04 | **4:05.74** (245.744) | PART 04 · 1909 · *The Shell That Bounced Back* |
| card05 | **5:55.48** (355.478) | PART 05 · 1913 · *Counting With X-rays* |

Part picture starts: p02 **1:10.53** · p03 **2:42.41** · p04 **4:06.84** · p05 **5:56.58**

## Seams (picture xfade 0.40 s)

| Join | Offset |
|---|---:|
| p01→card02 | 69.433 |
| card02→p02 | 70.533 |
| p02→card03 | 161.311 |
| card03→p03 | 162.411 |
| p03→card04 | 245.744 |
| card04→p04 | 246.844 |
| p04→card05 | 355.478 |
| card05→p05 | 356.578 |
| p05→cream4 | 500.694 |

Cream 4 s @ **8:20.69** · Studio hold 20 s from **8:24.70** · out **8:44.70**

## vo_check

```
FAIL  hos_004_full_join_v02_audio.wav  8:44.70  mean -29.7 dB  peak -9.7 dB  147 wpm
   first minute: title_question 8.64s  promise 11.38s  stakes 17.82s
   FAIL  speech mean -29.7 dB outside -28.0 to -19.0 dB
   FAIL  replace at ~3:59.50: script 'it was also wrong manchester ernest rutherford' / heard 'it was also rock manchester ernest rutherford'
   FAIL  replace at ~6:07.36: script 'the bones in a living hand moseley' / heard 'the bones in the living hand moseley'
   FAIL  replace at ~6:31.88: script 'was right now sort the table by' / heard 'was right now sought the table by'
   warn  silence 21.0s at 8:23.70 (part join?)
   warn  replace at ~6:04.66: … rontgen / runtgen (transcriber)
   warn  replace at ~7:23.22: … moseley / mosley (transcriber)
   warn  replace at ~7:45.58: … moseley / mosley (transcriber)
```

Speech-mean FAIL = quiet 20 s Studio hold. Word FAILs at 3:59.50 / 6:07.36 / 6:31.88 are **not** within ±1 s of seams 69.4 / 160.2 / 243.6 / 352.2 (nor the card/part offsets above) → no VO butt rebuild. Same known VO v04 KEEP transcriber misses Ben already accepted.

Builder: `07_Edit-Project/_join_hos_004_full_v02.py`  
iCloud: `HOS UAT/004_Whats-Really-Inside-An-Atom/09_Final-Export/hos_004_full_join_v02.mp4`
