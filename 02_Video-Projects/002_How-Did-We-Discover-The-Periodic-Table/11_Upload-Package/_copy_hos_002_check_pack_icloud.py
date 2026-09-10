#!/usr/bin/env python3
"""Copy HOS 002 check pack to iCloud for Ben/CoS review.

Full film, ABC thumbs, pill Shorts, listings. Does not upload to YouTube.
"""
from __future__ import annotations

import shutil
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
ICLOUD = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT/002_CHECK"
PKG = PROJ / "11_Upload-Package"
THUMB = PROJ / "08_Thumbnail/Selected"
SHORTS = PROJ / "10_Shorts"
COVERS = PROJ / "08_Thumbnail/Shorts"
FULL = PROJ / "09_Final-Export/hos_002_periodic_table_full_v01.mp4"


def copyf(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    print(f"  {dest.relative_to(ICLOUD)}  {dest.stat().st_size}", flush=True)


def main() -> None:
    if not FULL.exists():
        raise SystemExit(f"missing {FULL}")
    ICLOUD.mkdir(parents=True, exist_ok=True)
    print("ICLOUD", ICLOUD, flush=True)

    copyf(PKG / "CHECK_PACK.md", ICLOUD / "00_READ_ME.md")
    copyf(PKG / "Titles/periodic_table_long_title_abc_v01.txt", ICLOUD / "LISTINGS/titles.txt")
    copyf(PKG / "Descriptions/periodic_table_long_description_v01.txt", ICLOUD / "LISTINGS/description.txt")
    copyf(PKG / "Tags/periodic_table_long_tags_v01.txt", ICLOUD / "LISTINGS/tags.txt")
    copyf(PKG / "Chapters/periodic_table_long_chapters_v01.txt", ICLOUD / "LISTINGS/chapters.txt")
    copyf(PKG / "Shorts/SHORTS_LISTINGS_v01.json", ICLOUD / "LISTINGS/shorts_listings.json")
    copyf(PKG / "Pinned-Comments/periodic_table_long_pinned-comment_v01.txt", ICLOUD / "LISTINGS/pinned.txt")

    copyf(FULL, ICLOUD / "FULL/hos_002_periodic_table_full_v01.mp4")
    copyf(PROJ / "08_Thumbnail/LIVE_THUMB_LOCK.md", ICLOUD / "THUMBS/LIVE_THUMB_LOCK.md")
    for name in (
        "hos_002_thumb_A_gallium_live_v02.jpg",
        "hos_002_thumb_B_empty_seats_live_v02.jpg",
        "hos_002_thumb_C_empty_slot_live_v02.jpg",
    ):
        copyf(THUMB / name, ICLOUD / "THUMBS" / name)

    for name in (
        "hos_002_s01_empty_chairs_punch_pill_v01.mp4",
        "hos_002_s02_predict_metal_punch_pill_v01.mp4",
        "hos_002_s03_gallium_punch_pill_v01.mp4",
        "hos_002_s04_tellurium_punch_pill_v01.mp4",
        "hos_002_s05_other_table_punch_pill_v01.mp4",
    ):
        copyf(SHORTS / name, ICLOUD / "SHORTS" / name)
    for name in (
        "hos_002_s01_empty_chairs_cover_live_v02.jpg",
        "hos_002_s02_predict_metal_cover_live_v02.jpg",
        "hos_002_s03_gallium_cover_live_v02.jpg",
        "hos_002_s04_tellurium_cover_live_v02.jpg",
        "hos_002_s05_other_table_cover_live_v02.jpg",
    ):
        src = COVERS / name
        if src.exists():
            copyf(src, ICLOUD / "SHORTS_COVERS" / name)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
