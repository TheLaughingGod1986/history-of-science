# History of Science — Explorer style test (~30s)

**Purpose:** Quick look at 3D cartoon worlds + sparse Explorer side-character.  
**Not** a shippable Short — visual R&D only.

## VO (~28–32s · British · upbeat)

In an old library of discoveries, every shelf holds a question someone once dared to ask.
Our Explorer dusts a forgotten volume, reads a line — and the idea lights up.
Science isn't a straight road. It's curiosity, walking the stacks, one book at a time.

## Picture plan (4 × ~8s Veo → soft-join ≈ 30s)

| # | Scene | Explorer? |
|---|---|---|
| 1 | Dusty grand library · warm shafts of light · shelves of old books (story plate — **no** Explorer) | No |
| 2 | Explorer walks an aisle · picks a dusty book · blows dust · opens it | Yes |
| 3 | CU book pages / floating gold atom idea · curious wonder (story plate) | No |
| 4 | Explorer think → eureka point · glowing atom · then steps aside as shelves fill the frame | Yes |

Cadence matches channel lock: story leads; Explorer in ~half the beats only.

## Build

```bash
# needs GEMINI_API_KEY (optional ELEVENLABS_API_KEY for VO)
pip install -q google-genai
python3 02_Video-Projects/000_Explorer-Style-Test/07_Edit-Project/_build_explorer_style_test_30s.py
```

Output: `09_Final-Export/hos_explorer_style_test_30s_v01.mp4`
