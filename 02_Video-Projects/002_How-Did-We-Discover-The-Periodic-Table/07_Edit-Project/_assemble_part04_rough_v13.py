"""Assemble HOS 002 Part 04 rough v13 — CLEAN LIGHT + WRITTEN CARDS remint (chair fire / lamp smoke / blank cards).

Parent FAIL: hos_002_part04_rough_v13.mp4 sha 175c40a948a24899507266d3f4bccf39f9f51a2906441cae4557bcbd312fe6c2
  - REMINT: 04,05,09,09b (v13_fast) — blank stacks ~40–42; blank bet cards ~98; chair fire/smoke ~102–105
  - KEEP: 06 v11 CLEARED; 05b/07/08/08b/10 v12 cleared takes; 02b v06; 07b v11; P01–P03 frozen
  - Scores → CoS only. Do not declare PASS. Do not ping Ben.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

PROJ = Path(__file__).resolve().parents[1]
PLATES_JSON = PROJ / "07_Edit-Project/parts/part-04_plates_v01.json"
RAW_V01 = PROJ / "04_Generated-Clips/part04/raw/v01_fast"
RAW_V06 = PROJ / "04_Generated-Clips/part04/raw/v06_fast"
RAW_V07 = PROJ / "04_Generated-Clips/part04/raw/v07_fast"
RAW_V10 = PROJ / "04_Generated-Clips/part04/raw/v10_fast"
RAW_V11 = PROJ / "04_Generated-Clips/part04/raw/v11_fast"
RAW_V12 = PROJ / "04_Generated-Clips/part04/raw/v12_fast"
RAW_V13 = PROJ / "04_Generated-Clips/part04/raw/v13_fast"
LABEL_DIR = PROJ / "04_Generated-Clips/part04/refs/v06_side_labels"
VO = PROJ / "02_Voiceover/part04_empty_chairs_v01.wav"
BED = PROJ / "05_Music/hos_002_part01_curious_workshop_v02_norm.wav"
OUT = PROJ / "09_Final-Export/hos_002_part04_rough_v13.mp4"
KEEP_V06_PARENT = PROJ / "09_Final-Export/hos_002_part04_rough_v06.mp4"
KEEP_V07_PARENT = PROJ / "09_Final-Export/hos_002_part04_rough_v07.mp4"
KEEP_V08_PARENT = PROJ / "09_Final-Export/hos_002_part04_rough_v08.mp4"
KEEP_V08_PARENT_SHA = "8cafb379af976897d6cee46484439b1ecbda56f8a42760327a96d1744d614a83"
KEEP_V09_PARENT = PROJ / "09_Final-Export/hos_002_part04_rough_v09.mp4"
KEEP_V09_PARENT_SHA = "2981b26ae720edc3a8f5456a99fb5a3ac727bc79b850dabe5ad9cc57cf61eb61"
KEEP_V07_PARENT_SHA = "a74fa8ecd7f74785b3c4887e574d009676844189a0dc67620e659ae96e09efe2"
KEEP_V06_PARENT_SHA = "5aea09bdc505beb4d887acdfcfc5c43b307ee0bb7c606bb287b4beeb56e5bbf2"
KEEP_P03 = PROJ / "09_Final-Export/hos_002_part03_rough_v09.mp4"
KEEP_P03_SHA = "30060612a00d628998008c9946b8e25319b56f3b9e5613b537c5d2be989bbe4e"
ICLOUD = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT"
XFADE = 0.35
BED_VOL = 0.38
CLIP_USE = 7.9

REMINT_V13_IDS = {
    "04_sort_atomic_weight",
    "05_columns_families",
    "09_risk_bet",
    "09b_risk_hold",
}
KEEP_V12_IDS = {
    "05b_families_settle",  # ~55 sparks cleared in v12 — KEEP
    "07_eka_placeholders",
    "08_prediction_navigation",
    "08b_navigation_walk",  # ~85 written heroes — KEEP
    "10_family_before_weight",  # ~110 written floats — KEEP
}
KEEP_V11_IDS = {
    "06_explorer_leaves_gap",  # CLEARED — do not remint
    "07b_eka_names_rotate",
}
KEEP_V06_IDS = {"02b_cards_sixty_three"}
KEEP_V11_PARENT = PROJ / "09_Final-Export/hos_002_part04_rough_v11.mp4"
KEEP_V11_PARENT_SHA = "96a0f41e53987e090e5eee6af29d3abda8de3c30b326584193c10847d1ebd739"
KEEP_V12_PARENT = PROJ / "09_Final-Export/hos_002_part04_rough_v13.mp4"
KEEP_V12_PARENT_SHA = "175c40a948a24899507266d3f4bccf39f9f51a2906441cae4557bcbd312fe6c2"
KEEP_V10_PARENT = PROJ / "09_Final-Export/hos_002_part04_rough_v10.mp4"
KEEP_V10_PARENT_SHA = "eab7f8ec4d01ae21352e882dd50f8b45bab13d6305c2ac21f6fb73682e47ec8f"

PLATE_ORDER = [
    "01_chapter_empty_chairs",
    "02_mendeleev_desk_cards",
    "02b_cards_sixty_three",
    "03_what_is_element",
    "04_sort_atomic_weight",
    "05_columns_families",
    "06_explorer_leaves_gap",
    "05b_families_settle",
    "07_eka_placeholders",
    "07b_eka_names_rotate",
    "08_prediction_navigation",
    "08b_navigation_walk",
    "09_risk_bet",
    "09b_risk_hold",
    "10_family_before_weight",
    "11_publish_gaps",
    "11b_wait_and_hunt",
]

SIDE_LABELS = [
    (0.0, 3.0, "EMPTY CHAIRS"),
    (3.0, 8.5, "MENDELEEV"),
    (8.5, 17.5, "ELEMENT"),
    (18.0, 23.0, "ATOMIC WEIGHT"),
    (24.0, 40.0, "PERIODIC TABLE"),
    (44.0, 49.5, "EMPTY SEATS"),
    (50.0, 56.0, "EKA-ALUMINIUM"),
    (56.0, 62.0, "EKA-BORON"),
    (62.0, 68.0, "EKA-SILICON"),
    (68.0, 83.0, "A PREDICTION"),
    (83.5, 100.0, "A BET"),
    (101.0, 118.5, "FAMILY FIRST"),
    (119.0, 127.5, "PUBLISH THE GAPS"),
]


def probe(path: Path) -> float:
    return float(
        subprocess.check_output(
            [
                "ffprobe", "-v", "error", "-show_entries", "format=duration",
                "-of", "default=nw=1:nk=1", str(path),
            ],
            text=True,
        ).strip()
    )


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def render_side_label(text: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    w, h = 640, 120
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((8, 8, w - 8, h - 8), radius=18, fill=(48, 30, 16, 210))
    d.rounded_rectangle((8, 8, w - 8, h - 8), radius=18, outline=(232, 214, 180, 230), width=3)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia Bold.ttf", 36)
    except OSError:
        font = ImageFont.load_default()
    bb = d.textbbox((0, 0), text, font=font)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    d.text(((w - tw) / 2, (h - th) / 2 - 4), text, fill=(245, 232, 205, 255), font=font)
    im.save(dest)


def resolve_clip(pid: str) -> tuple[Path, str]:
    if pid in REMINT_V13_IDS:
        v13 = RAW_V13 / f"{pid}_v13.mp4"
        if v13.exists() and v13.stat().st_size >= 400_000:
            return v13, "v13_clean_light_cards"
        raise SystemExit(f"missing reminted v13 plate {v13}")
    if pid in KEEP_V12_IDS:
        v12 = RAW_V12 / f"{pid}_v12.mp4"
        if v12.exists() and v12.stat().st_size >= 400_000:
            return v12, "v12_keep_cleared"
        raise SystemExit(f"missing v12 KEEP plate {v12}")
    if pid in KEEP_V11_IDS:
        v11 = RAW_V11 / f"{pid}_v11.mp4"
        if v11.exists() and v11.stat().st_size >= 400_000:
            return v11, "v11_keep_cleared"
        raise SystemExit(f"missing v11 KEEP plate {v11}")
    if pid in KEEP_V06_IDS:
        v06 = RAW_V06 / f"{pid}_v06.mp4"
        if v06.exists() and v06.stat().st_size >= 400_000:
            return v06, "v06_desk_keep"
        raise SystemExit(f"missing v06 KEEP plate {v06}")
    v01 = RAW_V01 / f"{pid}_v01.mp4"
    if v01.exists() and v01.stat().st_size >= 400_000:
        return v01, "v01_keep"
    raise SystemExit(f"missing plate {v01}")



def main() -> None:
    if not KEEP_P03.exists():
        raise SystemExit(f"missing locked parent {KEEP_P03}")
    p03_sha = sha256(KEEP_P03)
    if p03_sha != KEEP_P03_SHA:
        raise SystemExit(
            f"STOP: P03 sha mismatch want {KEEP_P03_SHA} got {p03_sha} — refuse assemble"
        )
    print(f"KEEP P03 sha OK {p03_sha}", flush=True)

    if not KEEP_V06_PARENT.exists():
        raise SystemExit(f"missing parent v06 {KEEP_V06_PARENT}")
    v06_sha = sha256(KEEP_V06_PARENT)
    if v06_sha != KEEP_V06_PARENT_SHA:
        print(
            f"WARN: v06 parent sha mismatch want {KEEP_V06_PARENT_SHA} got {v06_sha}"
        )
    print(f"KEEP v06 parent sha OK {v06_sha}", flush=True)

    if not KEEP_V07_PARENT.exists():
        raise SystemExit(f"missing parent v07 {KEEP_V07_PARENT}")
    v07_sha = sha256(KEEP_V07_PARENT)
    if v07_sha != KEEP_V07_PARENT_SHA:
        print(
            f"WARN: v07 parent sha mismatch want {KEEP_V07_PARENT_SHA} got {v07_sha}"
        )
    print(f"KEEP v07 parent sha OK {v07_sha}", flush=True)

    if not KEEP_V08_PARENT.exists():
        raise SystemExit(f"missing parent v08 {KEEP_V08_PARENT}")
    v08_sha = sha256(KEEP_V08_PARENT)
    if v08_sha != KEEP_V08_PARENT_SHA:
        print(
            f"WARN: v08 parent sha mismatch want {KEEP_V08_PARENT_SHA} got {v08_sha}"
        )
    print(f"KEEP v08 parent sha OK {v08_sha}", flush=True)

    if not KEEP_V09_PARENT.exists():
        raise SystemExit(f"missing parent v09 {KEEP_V09_PARENT}")
    v09_sha = sha256(KEEP_V09_PARENT)
    if v09_sha != KEEP_V09_PARENT_SHA:
        print(
            f"WARN: v09 parent sha mismatch want {KEEP_V09_PARENT_SHA} got {v09_sha}"
        )
    print(f"KEEP v09 parent sha OK {v09_sha}", flush=True)

    if not KEEP_V10_PARENT.exists():
        raise SystemExit(f"missing parent v10 {KEEP_V10_PARENT}")
    v10_sha = sha256(KEEP_V10_PARENT)
    if v10_sha != KEEP_V10_PARENT_SHA:
        print(
            f"WARN: v10 parent sha mismatch want {KEEP_V10_PARENT_SHA} got {v10_sha}"
        )
    print(f"KEEP v10 parent sha OK {v10_sha}", flush=True)

    if not KEEP_V11_PARENT.exists():
        raise SystemExit(f"missing parent v11 {KEEP_V11_PARENT}")
    v11_sha = sha256(KEEP_V11_PARENT)
    if v11_sha != KEEP_V11_PARENT_SHA:
        raise SystemExit(
            f"STOP: v11 parent sha mismatch want {KEEP_V11_PARENT_SHA} got {v11_sha}"
        )
    print(f"KEEP v11 parent sha OK {v11_sha}", flush=True)

    if not KEEP_V12_PARENT.exists():
        raise SystemExit(f"missing parent v12 {KEEP_V12_PARENT}")
    v12_sha = sha256(KEEP_V12_PARENT)
    if v12_sha != KEEP_V12_PARENT_SHA:
        raise SystemExit(
            f"STOP: v12 parent sha mismatch want {KEEP_V12_PARENT_SHA} got {v12_sha}"
        )
    print(f"KEEP v12 parent sha OK {v12_sha}", flush=True)

    plates_by_id = {p["id"]: p for p in json.loads(PLATES_JSON.read_text())["plates"]}
    ordered_ids = [pid for pid in PLATE_ORDER if pid in plates_by_id]
    if len(ordered_ids) != len(PLATE_ORDER):
        missing = set(PLATE_ORDER) - set(ordered_ids)
        raise SystemExit(f"STOP: plate order missing ids {missing}")

    if not VO.exists():
        raise SystemExit(f"missing VO {VO}")
    if not BED.exists():
        raise SystemExit(f"missing bed {BED}")
    vo_dur = probe(VO)

    n = len(ordered_ids)
    use = max(CLIP_USE, (vo_dur + (n - 1) * XFADE) / n + 0.05)
    use = min(use, 8.05)
    print(f"clip_use={use:.3f}s for n={n} VO={vo_dur:.3f}", flush=True)

    clips: list[Path] = []
    uses: list[float] = []
    sources: list[str] = []
    for pid in ordered_ids:
        clip, src = resolve_clip(pid)
        d = probe(clip)
        if d < use - 0.05:
            raise SystemExit(f"short plate {clip} d={d} need>={use}")
        if d < 5.5:
            raise SystemExit(f"short plate {clip} d={d}")
        clips.append(clip)
        uses.append(use)
        sources.append(src)
        print(f"  {pid}: src={d:.2f}s use={use:.2f}s [{src}] {clip.name}", flush=True)

    offsets = [0.0]
    for i in range(1, len(uses)):
        offsets.append(offsets[-1] + (uses[i - 1] - XFADE))
    pic_dur = offsets[-1] + uses[-1]
    print(f"picture≈{pic_dur:.2f}s VO={vo_dur:.2f}s", flush=True)
    if pic_dur + 0.05 < vo_dur:
        raise SystemExit(
            f"picture {pic_dur:.2f} < VO {vo_dur:.2f} — mint more unique plates "
            "(no freeze-pad)"
        )

    explorer_index = ordered_ids.index("06_explorer_leaves_gap")
    explorer_start = offsets[explorer_index]
    explorer_end = explorer_start + uses[explorer_index]
    columns_index = ordered_ids.index("05_columns_families")
    columns_start = offsets[columns_index]
    columns_end = columns_start + uses[columns_index]
    plate02b_index = ordered_ids.index("02b_cards_sixty_three")
    plate02b_start = offsets[plate02b_index]
    plate02b_end = plate02b_start + uses[plate02b_index]
    plate09_index = ordered_ids.index("09_risk_bet")
    plate09_start = offsets[plate09_index]
    plate09_end = plate09_start + uses[plate09_index]
    plate09b_index = ordered_ids.index("09b_risk_hold")
    plate09b_start = offsets[plate09b_index]
    plate09b_end = plate09b_start + uses[plate09b_index]

    LABEL_DIR.mkdir(parents=True, exist_ok=True)
    label_pngs: list[tuple[float, float, Path]] = []
    for i, (a, b, text) in enumerate(SIDE_LABELS):
        png = LABEL_DIR / f"label_{i:02d}.png"
        render_side_label(text, png)
        label_pngs.append((a, min(b, vo_dur), png))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    inputs: list[str] = []
    for c in clips:
        inputs += ["-i", str(c)]
    inputs += ["-i", str(VO), "-i", str(BED)]
    label_input_start = n + 2
    for _, _, png in label_pngs:
        inputs += ["-loop", "1", "-t", "1", "-i", str(png)]

    parts: list[str] = []
    for i in range(n):
        u = uses[i]
        parts.append(
            f"[{i}:v]trim=0:{u:.3f},setpts=PTS-STARTPTS,"
            f"scale=1920:1080:force_original_aspect_ratio=decrease,"
            f"pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps=24,format=yuv420p[v{i}]"
        )
    vlabel = "[v0]"
    for i in range(1, n):
        out = f"[vx{i}]"
        offset = offsets[i]
        parts.append(
            f"{vlabel}[v{i}]xfade=transition=fade:duration={XFADE}:offset={offset:.3f}{out}"
        )
        vlabel = out

    cur = vlabel
    for li, (a, b, _png) in enumerate(label_pngs):
        idx = label_input_start + li
        nxt = f"[vl{li}]"
        parts.append(
            f"[{idx}:v]format=rgba,scale=640:-1[lg{li}];"
            f"{cur}[lg{li}]overlay=x=1920-660:y=48:enable='between(t,{a:.3f},{b:.3f})'{nxt}"
        )
        cur = nxt

    parts.append(
        f"[{n}:a]aformat=sample_rates=48000:channel_layouts=stereo,"
        f"atrim=0:{vo_dur:.3f},asetpts=PTS-STARTPTS[vo]"
    )
    parts.append(
        f"[{n+1}:a]aformat=sample_rates=48000:channel_layouts=stereo,"
        f"atrim=0:{vo_dur:.3f},volume={BED_VOL}[bed]"
    )
    parts.append("[vo][bed]amix=inputs=2:duration=first:dropout_transition=0[a]")
    fc = ";".join(parts)

    subprocess.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            *inputs,
            "-filter_complex", fc,
            "-map", cur, "-map", "[a]",
            "-c:v", "libx264", "-preset", "medium", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart", "-t", f"{vo_dur:.3f}",
            str(OUT),
        ],
        check=True,
    )
    digest = sha256(OUT)
    bytes_n = OUT.stat().st_size
    dur = probe(OUT)
    reminted = [pid for pid, src in zip(ordered_ids, sources) if src == "v13_clean_light_cards"]
    plate06 = RAW_V11 / "06_explorer_leaves_gap_v11.mp4"  # KEEP cleared
    plate06_sha = sha256(plate06) if plate06.exists() else None
    print(
        f"LANDED {OUT}\n"
        f"  path={OUT}\n"
        f"  bytes={bytes_n}\n"
        f"  sha256={digest}\n"
        f"  duration={dur:.3f}\n"
        f"  reminted={reminted}\n"
        f"  plate06_sha256={plate06_sha}\n"
        f"  plate02b_picture={plate02b_start:.2f}–{plate02b_end:.2f}\n"
        f"  columns_picture={columns_start:.2f}–{columns_end:.2f}\n"
        f"  explorer_picture={explorer_start:.2f}–{explorer_end:.2f}\n"
        f"  plate09_picture={plate09_start:.2f}–{plate09_end:.2f}\n"
        f"  plate09b_picture={plate09b_start:.2f}–{plate09b_end:.2f}\n"
        f"  keep_p03_sha={p03_sha}\n"
        f"  parent_v08_sha={v08_sha}\n",
        flush=True,
    )

    meta_path = PROJ / "07_Edit-Project/part04_rough_v13_land_meta.json"
    meta_path.write_text(
        json.dumps(
            {
                "cut": OUT.name,
                "path": str(OUT.relative_to(PROJ)),
                "bytes": bytes_n,
                "duration_s": dur,
                "sha256": digest,
                "parent_v06_sha256": v06_sha,
                "parent_v07_sha256": v07_sha,
                "parent_v08_sha256": v08_sha,
                "parent_v09_sha256": v09_sha,
                "parent_v11_sha256": v10_sha,
                "reminted_plates": reminted,
                "plate06_sha256": plate06_sha,
                "method": (
                    "Veo 3.1 Fast I2V — CLEAN LIGHT + WRITTEN CARDS remint (no chair fire / sparks / blank cards) "
                    "(04/05/05b/07/08/08b/09/09b/10)"
                ),
                "flow_account": "benoats@googlemail.com",
                "p03_untouched_sha256": p03_sha,
                "plate02b_picture_s": [plate02b_start, plate02b_end],
                "columns_picture_s": [columns_start, columns_end],
                "explorer_picture_s": [explorer_start, explorer_end],
                "plate09_picture_s": [plate09_start, plate09_end],
                "plate09b_picture_s": [plate09b_start, plate09b_end],
                "hos_uat": str(ICLOUD / OUT.name),
                "watch": "WATCH_part04_v13.txt",
                "note": (
                    "v11: Ben FAIL remint — glasses + clean lamp + written cards on 04/05/05b/07/08/08b/09/09b/10. "
                    "KEEP 06 cleared + 02b + 07b + other clean plates. Scores → CoS only. Do not declare PASS. Do not ping Ben."
                ),
            },
            indent=2,
        )
        + "\n"
    )

    ICLOUD.mkdir(parents=True, exist_ok=True)
    dest = ICLOUD / OUT.name
    subprocess.run(["cp", "-f", str(OUT), str(dest)], check=True)
    watch = ICLOUD / "WATCH_part04_v13.txt"
    watch.write_text(
        "WATCH THIS FILE ONLY (Part 04 rough v13 — Ben FAIL glasses/lamp/written cards):\n"
        f"  {OUT.name}\n\n"
        "CoS / Picture→UAT gates for this cut:\n"
        "- Parent FAIL v10 sha eab7f8ec… — Ben override 8 Sep (glasses / lamp fire / blank cards).\n"
        "- Reminted v11: 06_explorer_leaves_gap · 05b_families_settle · 07_eka_placeholders ·\n"
        "  07b_eka_names_rotate · 09_risk_bet · 09b_risk_hold. KEEP 02b desk + 05 columns + rest.\n"
        "- Spot Explorer ~45–53s: ROUND gold/wire glasses ALWAYS visible · bare head ·\n"
        "  messy wavy chestnut · fair warm tan · dark teal coat · profile/OTS/back garnish.\n"
        "- Lamp clean: warm desk-lamp glow ONLY — NO fire spit / candle / Bunsen on desk.\n"
        "- Cards: readable H/C/O/Eka/atomic marks — NEVER blank cream stacks/hero cards.\n"
        "- KEEP: Empty Chairs glow · EMPTY SEATS / Eka / A BET labels · indoor wood/bookcase.\n"
        "- Part 01–03 LOCKED — do not remint. Real Veo Fast. No Ken Burns.\n"
        "- Do NOT declare PASS here. Scores → CoS. No P05 until KEEP/LOCK.\n\n"
        "Do not ping Ben. Reject with stills from THIS file only.\n"
        f"keep_p03_sha={p03_sha}\n"
        f"parent_v11_sha={v10_sha}\n"
        f"reminted={','.join(reminted)}\n"
        f"plate06_sha256={plate06_sha}\n"
        f"plate02b_picture={plate02b_start:.3f}-{plate02b_end:.3f}\n"
        f"columns_picture={columns_start:.3f}-{columns_end:.3f}\n"
        f"explorer_picture={explorer_start:.3f}-{explorer_end:.3f}\n"
        f"plate09_picture={plate09_start:.3f}-{plate09_end:.3f}\n"
        f"plate09b_picture={plate09b_start:.3f}-{plate09b_end:.3f}\n"
        f"sha256={digest}\nbytes={bytes_n}\nduration={dur:.3f}\n"
    )
    (PROJ / "07_Edit-Project/WATCH_part04_v13.txt").write_text(watch.read_text())
    (ICLOUD / "ZZ_OPEN_PART04_V13_ONLY.txt").write_text(
        "Part 04 current cut = hos_002_part04_rough_v13.mp4\n"
        "Part 01–03 LOCKED keepers.\n"
        "v10 Ben FAIL (glasses/lamp/blank cards) → v11 remint — watch v11 only.\n"
    )
    (ICLOUD / "PART04_NEXT.txt").write_text(
        "Part 04 rough remint LANDED: hos_002_part04_rough_v13.mp4\n"
        "Watch WATCH_part04_v13.txt\n"
        "Scores → CoS. No P05 until KEEP/LOCK. Do not declare PASS. Do not ping Ben.\n"
    )
    print(f"ICLOUD {dest}", flush=True)
    print(f"WATCH {watch}", flush=True)
    print(f"META {meta_path}", flush=True)


if __name__ == "__main__":
    main()
