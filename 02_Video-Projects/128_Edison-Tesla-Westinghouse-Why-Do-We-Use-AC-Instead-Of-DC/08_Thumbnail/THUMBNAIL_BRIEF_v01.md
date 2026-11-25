# Thumbnail Brief v01 — HOS:128 *Why Do We Use AC Instead of DC? (Edison vs Tesla)*

- **Stage:** £0 pre-build brief (`J3734`, 25 Nov 2026). **NOT rendered packaging PASS** — zero Flow/image generation before Chief VO PASS (`J3670`, `studio/RULES.md` Never list).
- **Target air:** Thu 7 Jan 2027 18:00 London (Ben watch Mon 4 Jan 2027).
- **House rules:** Painted 3D cartoon period palette (no Orbit saturation push), serif cream & one gold hook word in clear left/top band (never over hero object), Explorer small at lower-left (`CHARACTER_BIBLE.md`), **cover text never repeats title** (`§2.5`), hand-verified lettering (`§2.6`), `style_sheet.py` + `thumb_preview.py` (`168×94`) + `packaging_panel.py` after VO PASS.

## Thumbnail Concepts (Test & Compare A / B / C)

1. **Thumb A (Primary — Physics Stakes):**
   - **Cover text (3 words, clear top-left band):** `WASTED AS` *(cream serif)* / **`HEAT`** *(gold serif)*
   - **Key art (Flow Nano Banana 2, 0 cr post-VO):** Warm 1882 Manhattan workshop-to-street split: heavy glowing-red copper DC feeder cable overheating in a trench beside a crisp gleaming brass AC transformer lifting a thin golden line across a sunlit twilight city skyline. Explorer small at lower-left holding his brass compass. No readable text in generated art.
2. **Thumb B (Rivalry / Scale):**
   - **Cover text (3 words, clear top-left band):** **`22 MILES`** *(gold serif)* / `AWAY` *(cream serif)*
   - **Key art (Flow Nano Banana 2, 0 cr post-VO):** Dramatic Niagara Falls turquoise plunge into massive brass 5,000-hp generators feeding glowing lines across twilight hills toward a brightly lit distant city. Explorer small at lower-left with open blue notebook.
3. **Thumb C (Third T&C Arm per §2.9):**
   - **Cover text (2 words, clear top-left band):** **`HIGH`** *(gold serif)* / `VOLTAGE` *(cream serif)*
   - **Key art (Flow Nano Banana 2, 0 cr post-VO):** Close-up on a gleaming 1886 brass-and-copper closed-core transformer ring glowing cleanly on a warm oak workbench while an industrialist and engineer silhouette frame the background. Explorer small at lower-left.

## Post-VO Gate Checklist
- [ ] Generate key art with Flow Nano Banana 2 (`0` cr) only after `J3670` VO PASS.
- [ ] Composite cream + gold serif lettering in Python/Pillow (`§2.6` exact glyph check).
- [ ] Run `style_sheet.py long <thumb.jpg>` and `thumb_preview.py long <thumb.jpg>` (`168×94` phone readability).
- [ ] Run independent `packaging_panel.py` critique + Chief HOOK/BAND/PHONE PASS before Ben watch.
