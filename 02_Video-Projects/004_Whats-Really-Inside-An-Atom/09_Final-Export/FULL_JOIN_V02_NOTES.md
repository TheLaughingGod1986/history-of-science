# HOS 004 full join v02 — seamless seams (UAT)

**Cut:** `hos_004_full_join_v02.mp4`
**sha256:** `b20ac5a4ae8941884383fba4df50403c6718d24b742abc8ab81f8333ea6791da`
**Duration:** 522.067 s · **Size:** 377133093 B
**Status:** UAT for Ben after v01 FAIL (abrupt seams + bridge text card). Do **not** label KEEP/LOCKED. Do **not** upload.

## Fixes vs v01

- Removed P01 `17_ledger_bridge` (on-screen “BRIDGES TO PART 02 / CHAPTER CARD”); extended plate 16.
- No chapter / bridge cards.
- VO gaps ~0.45 s between parts (match in-part line gaps).
- One continuous TEMP bed (acrossfaded part beds) + sidechain duck — no bed restart at seams.
- J-cut: next VO leads picture by ~0.50 s; picture dissolve 0.50 s.
- Cream card then 20 s Studio end hold.

## Parents (hash-checked, not reminted)

| Part | File | sha256 |
|---|---|---|
| 01 | `hos_004_part01_rough_v05.mp4` | `71d7c70798c77ce2ecb02c37ad043fd98117a2209a84899236337fee8b952add` |
| 02 | `hos_004_part02_rough_v01.mp4` | `620ce51250028495a588f25967dddfaa9c6136dc4172c7b0ce1ee609f103f1d2` |
| 03 | `hos_004_part03_rough_v01.mp4` | `d62e0ed096ead8ec52666ca07476f973aeaae7635b70a16faaac45f14ec518e0` |
| 04 | `hos_004_part04_rough_v02.mp4` | `157feaef7bd21236aeafc3e953fe461fe2ee95896bb868d57357c9c1c2c1e1f5` |
| 05 | `hos_004_part05_rough_v03.mp4` | `b391bff0dbe8a8ae0130adef4f7f3d7b79aca2cb34a934d9cf42d76e1d03363f` |

## Seams

| Seam | Next VO in | Dissolve in | Next picture full |
|---|---:|---:|---:|
| 01→02 | 1:10.25 (70.245) | 1:10.77 (70.767) | 1:11.27 (71.267) |
| 02→03 | 2:41.83 (161.834) | 2:42.87 (162.867) | 2:43.37 (163.367) |
| 03→04 | 4:06.01 (246.014) | 4:07.57 (247.567) | 4:08.07 (248.067) |
| 04→05 | 5:55.47 (355.471) | 5:57.53 (357.533) | 5:58.03 (358.033) |

| Cream card | 8:18.03 (498.033) |
| 20 s Studio hold | 8:22.07 (502.067) |
| Film out | 8:42.07 (522.067) |

A/V sync delta (audio−video): `0.0`

Builder: `07_Edit-Project/_join_hos_004_full_v02.py`
