

---

# Word-check + B retake — 4 Oct 2026 ~17:50 London (Grok)

faster-whisper `Systran/faster-whisper-small.en` under Python 3.13 venv
`/Users/benjaminoats/agent-tools/whisper-venv-313` (PyAV 19 broke `metadata_errors`;
audio decoded via ffmpeg→numpy). Model cache reused.

## Word-check table

| Take | Dur | vs script | Spoken title? | Verdict |
|---|---|---|---|---|
| A `t1_willow_air_vo_v02.mp3` | 22.64 s | body 1.000 vs #205 (no title) | YES after body | **KEEP audio — trim title** |
| B `t2_mint_fixed_vo_v02.mp3` | 20.00 s | 0.883 vs #205 | YES; missing close | **FAIL** |
| B `t2_mint_fixed_vo_v02b.mp3` | 18.82 s | 0.883 vs #205 | YES; missing close | **FAIL** |
| B `t2_mint_fixed_vo_v03.mp3` | 23.20 s | 1.000 vs #205 | NO; close present | **PASS** (vo_check loudness PASS mean −21.0 / peak −1.2) |
| C `t3_bubbles_sunlight_vo_v01.mp3` | 24.16 s | 1.000 after ASR norms | NO | **PASS / provisional KEEP** |

## Transcripts (faster-whisper)

**A v02:** A tree is built from thin air. One man spent five years proving the soil wasn't feeding it. He planted a willow in 200 pounds of dried soil and gave it only water. Five years later the tree weighed 169 pounds and the soil had lost just two ounces. The willow tree that was made of air

**B v02 / v02b:** …same air. The willow tree that was made of air  *(no Somehow-close)*

**B v03:** A sprig of mint repaired the air. Joseph Priestley burned a candle in a sealed jar until the flame died and no new flame would light. He slid in a sprig of mint and waited. Ten days later a candle burned bright in that same air. Somehow the little green plant had made the air good again.

**C v01:** leaves only make oxygen in the light. In 1779 a Dutch doctor called Jan Ingenhaus put fresh leaves in jars of water by a sunny window. Tiny silver bubbles rose from the green leaves. Moved the jar into the shade and the bubbles stopped. Back into the sun and they started again. Plants run on sunlight.
*(ASR: Ingenhaus≈Ingenhousz, Moved≈Move)*

## A trim tip

- ElevenLabs align: **`ounces.` ends 19.920 s**; spoken title starts **20.180 s** (`The Willow…Air.` ends 22.640 s).
- Whisper word end for `ounces.` ≈ 19.62 s (looser).
- **Edit trim:** cut VO after `two ounces.` @ **~19.92 s** (keep ≤20.0 s); do not re-record. ~4 s silent/picture loop → ~24 s Short.

## C — how "1779" was read

- Whisper emits a single token `1779` @ **3.58–4.70 s** (p=0.999), not digit-words.
- ElevenLabs char-align maps `1779,` @ **3.520–4.800 s** (~1.28 s span).
- Clip ASR still normalises to digits even with a "seventeen seventy-nine" prompt (Whisper year normalisation).
- Duration + English year TTS default ⇒ spoken as **year-style ("seventeen seventy-nine")**, not "one seven seven nine". No FAIL.

## B retake

- Path: `/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/006_Trees-Are-Made-Of-Air/10_Shorts/vo_20261004/t2_mint_fixed_vo_v03.mp3` (+ desk copy under `_desk/006/shorts_vo_20261004/vo/`)
- Script: #205 / `t2_mint_fixed_v03.txt` (291 chars / 57 wc; closing line present; **no title**)
- Voice: Ben Orbit Narrator `kDch6ACCIpqgQ0NsU9kk` / `eleven_v3` / stability 0.34 / sim 0.78 / style 0.42 / speed 1.04
- Meta: `VO_META_v03.json`; align: `t2_mint_fixed_vo_v03_align.json`
- sha256: `cb45356fd60363aad92ba97a05b2fb8cbe7b6b61d7b4bb411ded8f4f9aa3f0bf`

## Credits (Creator, refreshed ~17:50 London)

- used **112420** / limit **209536** → remaining **97116**
- (v03 mint logged laggy 109976→109976 at mint; refresh caught up)

## 007

- Script on disk + main: `02_Video-Projects/007_The-First-Vaccine/01_Script/vaccine_script_master_v01.md` (~2712 words)
- VO folder empty except README: `…/007_The-First-Vaccine/02_Voiceover/`
- **Not started** this turn — 006 word-check + B retake completed first per Claude order.

## Whisper artefacts

`/Users/benjaminoats/_desk/006/shorts_vo_20261004/wordcheck_20261004/*_whisper.json`

## Next step

1. Edit A: trim after 19.92 s.  
2. Use B v03 as the B VO.  
3. C KEEP.  
4. Start 007 long VO from `vaccine_script_master_v01.md` into `007_The-First-Vaccine/02_Voiceover/` (Creator credit OK; still no Pro / no video).
