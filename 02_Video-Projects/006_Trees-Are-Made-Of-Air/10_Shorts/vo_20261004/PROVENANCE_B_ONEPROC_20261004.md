# HOS 006 Short B — one-process provenance (4 Oct 2026 ~18:02 London)

Claude hold on #180 comment **5982339769**. Single shell pid ran ffprobe + sha256 + `vo_check_py312.sh` (loudness/silence + faster-whisper words) for all three takes. **No parallel TTS writers** during the run.

## Three-row table (measured)

| take/label | path | duration | sha256 | vo_check | whisper word-check | notes |
|---|---|---:|---|---|---|---|
| v03_cb45356 | `~/_desk/006/shorts_vo_20261004/vo/t2_mint_fixed_vo_v03.mp3` (same bytes on repo `vo_20261004/`) | **23.200000 s** | `cb45356fd60363aad92ba97a05b2fb8cbe7b6b61d7b4bb411ded8f4f9aa3f0bf` | mean −21.0 / peak −1.2; loudness+silence OK; **PASS** | **56/56 PASS** | bitrate 128429; no title spoken |
| v03b_0f10992 | `~/_desk/006/shorts_vo_20261004/vo/t2_mint_fixed_vo_v03b.mp3` (same bytes on repo) | **23.200000 s** | `0f1099262037b62ea2b2a003ce86e196458fa983e9ca97877afb5600e97c7479` | mean −21.3 / peak −1.5; loudness+silence OK; **PASS** | **56/56 PASS** | bitrate 99278; safer peak headroom |
| OVERWRITE_f11b88 | `~/_desk/006/shorts_vo_20261004/vo/t2_mint_fixed_vo_v03_OVERWRITE_21s.mp3` (desk only) | **21.600000 s** | `f11b88bc8919647f3d50fc30f44c83caab088dbb378be0613aa1512085d6a36a` | mean −20.7 / peak −0.8; **FAIL** peak | 56/56 PASS words | **Do not use** — race overwrite |

## Name map (desk = repo for live stems)

| filename | desk sha | repo sha | dur |
|---|---|---|---|
| `t2_mint_fixed_vo_v03.mp3` | cb45356… | cb45356… | 23.20 s |
| `t2_mint_fixed_vo_v03b.mp3` | 0f10992… | 0f10992… | 23.20 s |
| `t2_mint_fixed_vo_v03_OVERWRITE_21s.mp3` | f11b88… | MISSING | 21.60 s |

## Lock recommendation

Both **v03** and **v03b** are consistent (≥23 s, 56/56, no title). **Lock B = v03b** (`0f10992…`) — safer peak (−1.5 vs −1.2) and matches Claude PASS 5982291115. No Short B retake.

Run log: `/Users/benjaminoats/_desk/handoff/hos006_short_b_provenance_run_20261004.log`
