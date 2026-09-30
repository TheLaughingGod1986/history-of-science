# Style references

The live, Ben-approved look, as images. Every new long thumbnail or Shorts cover is compared against these before it goes to Ben (`THUMBNAIL_AND_TITLE_RULES.md` §2 and §4):

```bash
python3 00_Brand/Channel-Setup/tools/style_sheet.py long  <new.jpg> [more.jpg] --out <sheet.jpg>
python3 00_Brand/Channel-Setup/tools/style_sheet.py short <new_cover.jpg> --out <sheet.jpg>
```

| Folder | Format | Lettering |
|---|---|---|
| `long/` | 16:9 long thumbnails | Serif painted lettering, cream + one gold punch word, gold flourishes; painted 3D scene, one giant hero object right, the Explorer small lower left |
| `shorts/` | 9:16 Shorts covers | Chunky rounded gold/cream, thick outline, one small teal middle word; painted scene, the Explorer as a small reaction |

- `long/` holds the four live long thumbnails (001–004), pulled 30 Sep 2026.
- `shorts/` must hold the live covers. The public API only serves a Short's video frame, not its custom cover, so copy the approved cover files in from `HOS UAT/…/10_Shorts/` (at least the eight on the 30 Sep sheet: empty chairs, predicted a metal, gallium, tellurium, other table, HOW so SMALL?, EVERY eighth ELEMENT?, THE carbolic SPRAY).
- When a new thumbnail or cover is approved and goes live, add it here. When the look changes on purpose, Ben says so, and the old references move to `_archive/`.
