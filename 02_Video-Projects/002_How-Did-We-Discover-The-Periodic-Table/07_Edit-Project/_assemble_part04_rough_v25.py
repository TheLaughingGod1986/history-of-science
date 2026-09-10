#!/usr/bin/env python3
"""Assemble HOS 002 Part 04 rough v25 — kill repeating moon-desk still-life.

Parent: hos_002_part04_rough_v24.mp4
  sha256 4dea0a7219ad7a1f1878006c6a1c4511ddb9930225b700ce0a3186b2a666cbcd

Ben UAT on v24: the moon-window / flasks / lamp / blank-cards still-life still
plays two or three times. 07 + 07b + 08 were visually the same still.

v25:
  07b → unused unique v12 eka-placeholder cards (not the moon-desk; no fire)
  08  → T2V Quality walk toward one vacant glowing chair (navigation)
  07b T2V try1/try2 FAIL chair-fire / card-fire — do not assemble
KEEP 07 v20 (one remaining eka desk), 08b FAIL, 09 WIN, 09b try14.
NO PAINT. Scores → CoS. Do not declare PASS.
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
RAW_V11 = PROJ / "04_Generated-Clips/part04/raw/v11_fast"
RAW_V12 = PROJ / "04_Generated-Clips/part04/raw/v12_fast"
RAW_V13 = PROJ / "04_Generated-Clips/part04/raw/v13_fast"
RAW_V15 = PROJ / "04_Generated-Clips/part04/raw/v15_fast"
RAW_V16 = PROJ / "04_Generated-Clips/part04/raw/v16_fast"
RAW_V17 = PROJ / "04_Generated-Clips/part04/raw/v17_fast"
RAW_V18 = PROJ / "04_Generated-Clips/part04/raw/v18_fast"
RAW_V20 = PROJ / "04_Generated-Clips/part04/raw/v20_fast"
RAW_V20Q = PROJ / "04_Generated-Clips/part04/raw/v20_quality"
RAW_V22Q = PROJ / "04_Generated-Clips/part04/raw/v22_quality"
RAW_V24Q = PROJ / "04_Generated-Clips/part04/raw/v24_quality"
RAW_V25Q = PROJ / "04_Generated-Clips/part04/raw/v25_quality"
LABEL_DIR = PROJ / "04_Generated-Clips/part04/refs/v06_side_labels"
VO = PROJ / "02_Voiceover/part04_empty_chairs_v01.wav"
# Looped bed: usable workshop body (~0–84s) soft-crossfaded to cover full VO.
BED = PROJ / "05_Music/hos_002_part01_curious_workshop_v02_loop130_norm.wav"
OUT = PROJ / "09_Final-Export/hos_002_part04_rough_v25.mp4"
PARENT_V20 = PROJ / "09_Final-Export/hos_002_part04_rough_v20.mp4"
PARENT_V20_SHA = "1cd8249ad635b5f8339dc5fb155c9483c090ea4c6969efab19572ffa14d6d45b"
PARENT_V21 = PROJ / "09_Final-Export/hos_002_part04_rough_v21.mp4"
PARENT_V21_SHA = "868a012c5f52fa7f412a076cf26593f9cd700f3c03299cd14ff7010eb6804963"
PARENT_V22 = PROJ / "09_Final-Export/hos_002_part04_rough_v22.mp4"
PARENT_V22_SHA = "78039206d044fd9ee61aed5dd3aa491fa697c32b2896ae7311a175db630b13d3"
PARENT_V23 = PROJ / "09_Final-Export/hos_002_part04_rough_v23.mp4"
PARENT_V23_SHA = "7beae93d10a87066731ae58bc39039eabda625154aa7f0aa3e7c4d9f6e5e5b5f"
PARENT_V24 = PROJ / "09_Final-Export/hos_002_part04_rough_v24.mp4"
PARENT_V24_SHA = "4dea0a7219ad7a1f1878006c6a1c4511ddb9930225b700ce0a3186b2a666cbcd"

KEEP_V16_PARENT = PROJ / "09_Final-Export/hos_002_part04_rough_v16.mp4"
KEEP_V16_PARENT_SHA = "7e083fc440879209bbc69459fbaf21dc29dbfc1f77b370ec92ee931bec82cb3c"
KEEP_V15_PARENT = PROJ / "09_Final-Export/hos_002_part04_rough_v15.mp4"
KEEP_V15_PARENT_SHA = "cd7a57b2979478a34ac7cc5fe5639aa156ae603b437674ccd724ab3fe994748c"
KEEP_V14_PARENT = PROJ / "09_Final-Export/hos_002_part04_rough_v14.mp4"
KEEP_V14_PARENT_SHA = "fa62ab22d0f7cbd4f208e5200c9b8b471c23595237b4d7d2dd18e6f47dabad4f"
KEEP_V13_PARENT = PROJ / "09_Final-Export/hos_002_part04_rough_v13.mp4"
KEEP_V13_PARENT_SHA = "27828f216c289d36aaeae7311c545cdf0fb829381ff110c528cc40008710cd6a"
KEEP_V12_PARENT = PROJ / "09_Final-Export/hos_002_part04_rough_v12.mp4"
KEEP_V12_PARENT_SHA = "175c40a948a24899507266d3f4bccf39f9f51a2906441cae4557bcbd312fe6c2"
KEEP_V11_PARENT = PROJ / "09_Final-Export/hos_002_part04_rough_v11.mp4"
KEEP_V11_PARENT_SHA = "96a0f41e53987e090e5eee6af29d3abda8de3c30b326584193c10847d1ebd739"
KEEP_P03 = PROJ / "09_Final-Export/hos_002_part03_rough_v09.mp4"
KEEP_P03_SHA = "30060612a00d628998008c9946b8e25319b56f3b9e5613b537c5d2be989bbe4e"
ICLOUD = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT"
XFADE = 0.35
BED_VOL = 0.38
CLIP_USE = 7.9

# CoS KEEP remints — hard sha gate. Paint banned.
KEEP_REMINTS: dict[str, tuple[Path, str]] = {
    "05_columns_families": (
        RAW_V22Q / "05_columns_families_v22_try2B.mp4",
        "49437e7e4004c224b021409e15ebb50fb06b74737adfe2b6c0bc0a61bfae8caa",
    ),
    "06_explorer_leaves_gap": (
        RAW_V20 / "06_explorer_leaves_gap_v20_try8.mp4",
        "fd4627d29e8087ff50baca163fc0dd155d2a19eb5127dc1c3c7379e9525c7a70",
    ),
    "07b_eka_names_rotate": (
        RAW_V12 / "07_eka_placeholders_v12.mp4",
        "450a044431a7a140bace8b019bffe9e4f7c74184df9489c3452dbb032333f74f",
    ),
    "08_prediction_navigation": (
        RAW_V25Q / "08_prediction_navigation_v25_try1.mp4",
        "b189ef879fc303063a5b32dfd1cb420baff9e8a61d3c6345f3268aa927982cb0",
    ),
    "08b_navigation_walk": (
        RAW_V24Q / "08b_navigation_walk_v24_try1.mp4",
        "83fc2c4325ba16b46851a8668a4f8de91858457b35eb8ca6cdd7680b287827a3",
    ),
    "09_risk_bet": (
        RAW_V24Q / "09_risk_bet_v24_try1.mp4",
        "4e15c3b6c1212b84bd61a050c6db3fa64c2158bad38ec77390743a22b1055ad1",
    ),
    "09b_risk_hold": (
        RAW_V20Q / "09b_risk_hold_v20_try14.mp4",
        "47a6bdebed079d46e48950d3b544388a807c79258d1114b39ab596ebf6f44c38",
    ),
    "10_family_before_weight": (
        RAW_V22Q / "10_family_before_weight_v22_try1.mp4",
        "49240cbb4fab760e710f24051d822c61f0b8c1236684fc697016db325ab81b78",
    ),
    "11_publish_gaps": (
        RAW_V20 / "11_publish_gaps_v20_try9.mp4",
        "97d0c419fdf7720f366140a9fb2b024a29580a2db51a434e7afb425a19f8cc72",
    ),
    "11b_wait_and_hunt": (
        RAW_V20 / "11b_wait_and_hunt_v20_try1.mp4",
        "5602762e82fd40eb654b25a5d3e5260e8baf79707fb19ecf8b58ede67cb3075e",
    ),
}

# Other reminted slots stay on v20 canonical Flow harvest (not the four KEEP swaps).
REMINT_V20_IDS = {
    "07_eka_placeholders",
}
KEEP_V18_IDS = set()
KEEP_V16_IDS = set()
KEEP_V15_IDS = set()
KEEP_V13_IDS = {
    "04_sort_atomic_weight",
}
KEEP_V12_IDS = {
    "05b_families_settle",
}
KEEP_V11_IDS = set()
KEEP_V06_IDS = {"02b_cards_sixty_three"}

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
    if pid in KEEP_REMINTS:
        clip, want = KEEP_REMINTS[pid]
        if not clip.exists() or clip.stat().st_size < 400_000:
            raise SystemExit(f"STOP: missing KEEP remint Flow plate {clip}")
        got = sha256(clip)
        if got != want:
            raise SystemExit(f"STOP: KEEP remint {pid} sha mismatch want {want} got {got}")
        # Refuse paint-tiny leftovers if someone swapped a paint file onto this path.
        if clip.stat().st_size < 400_000:
            raise SystemExit(f"STOP: paint-banned — KEEP remint too small {clip}")
        return clip, "v22_keep_remint_uat"
    if pid in REMINT_V20_IDS:
        clip = RAW_V20 / f"{pid}_v20.mp4"
        if clip.exists() and clip.stat().st_size >= 400_000:
            return clip, "v20_flow_ultra_keep"
        raise SystemExit(f"missing reminted Flow v20 plate {clip}")
    if pid in KEEP_V18_IDS:
        v18 = RAW_V18 / f"{pid}_v18.mp4"
        if v18.exists() and v18.stat().st_size >= 80_000:
            return v18, "v18_keep_family"
        raise SystemExit(f"missing v18 KEEP plate {v18}")
    if pid in KEEP_V16_IDS:
        v16 = RAW_V16 / f"{pid}_v16.mp4"
        if v16.exists() and v16.stat().st_size >= 400_000:
            return v16, "v16_keep_family"
        raise SystemExit(f"missing v16 KEEP plate {v16}")
    if pid in KEEP_V15_IDS:
        v15 = RAW_V15 / f"{pid}_v15.mp4"
        if v15.exists() and v15.stat().st_size >= 400_000:
            return v15, "v15_keep_cleared"
        raise SystemExit(f"missing v15 KEEP plate {v15}")
    if pid in KEEP_V13_IDS:
        v13 = RAW_V13 / f"{pid}_v13.mp4"
        if v13.exists() and v13.stat().st_size >= 400_000:
            return v13, "v13_keep_cleared"
        raise SystemExit(f"missing v13 KEEP plate {v13}")
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


def require_sha(path: Path, want: str, label: str, *, hard: bool = True) -> str:
    if not path.exists():
        raise SystemExit(f"missing {label} {path}")
    got = sha256(path)
    if got != want:
        msg = f"{label} sha mismatch want {want} got {got}"
        if hard:
            raise SystemExit(f"STOP: {msg}")
        print(f"WARN: {msg}", flush=True)
    else:
        print(f"KEEP {label} sha OK {got}", flush=True)
    return got


def main() -> None:
    p03_sha = require_sha(KEEP_P03, KEEP_P03_SHA, "P03")
    v20_sha = require_sha(PARENT_V20, PARENT_V20_SHA, "v20 parent")
    v21_sha = require_sha(PARENT_V21, PARENT_V21_SHA, "v21 parent")
    v22_sha = require_sha(PARENT_V22, PARENT_V22_SHA, "v22 parent")
    v23_sha = require_sha(PARENT_V23, PARENT_V23_SHA, "v23 parent")
    v24_sha = require_sha(PARENT_V24, PARENT_V24_SHA, "v24 parent")
    parent_v19 = PROJ / "09_Final-Export/hos_002_part04_rough_v19.mp4"
    v19_sha = require_sha(
        parent_v19,
        "69d48f6e5fac419df5c23c17df5d0ef628cb4e8d533ba085bb3c8a173016bcdf",
        "v19 parent",
    )
    v17_parent = PROJ / "09_Final-Export/hos_002_part04_rough_v17.mp4"
    v17_sha = require_sha(
        v17_parent,
        "e4cc41d8cf050f6726e6b3d5cbbbff10285656c588f3a758b4a29e1ec1f998fd",
        "v17 parent",
    )
    v16_sha = require_sha(KEEP_V16_PARENT, KEEP_V16_PARENT_SHA, "v16 parent")
    require_sha(KEEP_V15_PARENT, KEEP_V15_PARENT_SHA, "v15 parent")
    require_sha(KEEP_V14_PARENT, KEEP_V14_PARENT_SHA, "v14 parent")
    require_sha(KEEP_V13_PARENT, KEEP_V13_PARENT_SHA, "v13 parent")
    require_sha(KEEP_V12_PARENT, KEEP_V12_PARENT_SHA, "v12 parent")
    require_sha(KEEP_V11_PARENT, KEEP_V11_PARENT_SHA, "v11 parent")

    # Hard-gate KEEP remints before build.
    for pid, (path, want) in KEEP_REMINTS.items():
        require_sha(path, want, f"KEEP remint {pid}")

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
    plate_sha: dict[str, str] = {}
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
        plate_sha[pid] = sha256(clip)
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
    plate07b_index = ordered_ids.index("07b_eka_names_rotate")
    plate07b_start = offsets[plate07b_index]
    plate07b_end = plate07b_start + uses[plate07b_index]
    plate08_index = ordered_ids.index("08_prediction_navigation")
    plate08_start = offsets[plate08_index]
    plate08_end = plate08_start + uses[plate08_index]
    plate08b_index = ordered_ids.index("08b_navigation_walk")
    plate08b_start = offsets[plate08b_index]
    plate08b_end = plate08b_start + uses[plate08b_index]
    plate09_index = ordered_ids.index("09_risk_bet")
    plate09_start = offsets[plate09_index]
    plate09_end = plate09_start + uses[plate09_index]
    plate09b_index = ordered_ids.index("09b_risk_hold")
    plate09b_start = offsets[plate09b_index]
    plate09b_end = plate09b_start + uses[plate09b_index]
    plate10_index = ordered_ids.index("10_family_before_weight")
    plate10_start = offsets[plate10_index]
    plate10_end = plate10_start + uses[plate10_index]
    plate11_index = ordered_ids.index("11_publish_gaps")
    plate11_start = offsets[plate11_index]
    plate11_end = plate11_start + uses[plate11_index]
    plate11b_index = ordered_ids.index("11b_wait_and_hunt")
    plate11b_start = offsets[plate11b_index]
    plate11b_end = plate11b_start + uses[plate11b_index]

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
    keep_swapped = [pid for pid, src in zip(ordered_ids, sources) if src == "v22_keep_remint_uat"]
    v20_kept = [pid for pid, src in zip(ordered_ids, sources) if src == "v20_flow_ultra_keep"]
    print(
        f"LANDED {OUT}\n"
        f"  path={OUT}\n"
        f"  bytes={bytes_n}\n"
        f"  sha256={digest}\n"
        f"  duration={dur:.3f}\n"
        f"  keep_remints={keep_swapped}\n"
        f"  v20_kept_remints={v20_kept}\n"
        f"  plate05_sha256={plate_sha.get('05_columns_families')}\n  plate06_sha256={plate_sha.get('06_explorer_leaves_gap')}\n  plate10_sha256={plate_sha.get('10_family_before_weight')}\n"
        f"  plate07b_sha256={plate_sha.get('07b_eka_names_rotate')}\n"
        f"  plate08_sha256={plate_sha.get('08_prediction_navigation')}\n"
        f"  plate08b_sha256={plate_sha.get('08b_navigation_walk')}\n"
        f"  plate09_sha256={plate_sha.get('09_risk_bet')}\n"
        f"  plate09b_sha256={plate_sha.get('09b_risk_hold')}\n"
        f"  plate10_sha256={plate_sha.get('10_family_before_weight')}\n"
        f"  plate11_sha256={plate_sha.get('11_publish_gaps')}\n"
        f"  plate11b_sha256={plate_sha.get('11b_wait_and_hunt')}\n"
        f"  explorer_picture={explorer_start:.2f}–{explorer_end:.2f}\n"
        f"  plate07b_picture={plate07b_start:.2f}–{plate07b_end:.2f}\n"
        f"  plate08_picture={plate08_start:.2f}–{plate08_end:.2f}\n"
        f"  plate08b_picture={plate08b_start:.2f}–{plate08b_end:.2f}\n"
        f"  plate09_picture={plate09_start:.2f}–{plate09_end:.2f}\n"
        f"  plate09b_picture={plate09b_start:.2f}–{plate09b_end:.2f}\n"
        f"  plate10_picture={plate10_start:.2f}–{plate10_end:.2f}\n"
        f"  plate11_picture={plate11_start:.2f}–{plate11_end:.2f}\n"
        f"  plate11b_picture={plate11b_start:.2f}–{plate11b_end:.2f}\n"
        f"  keep_p03_sha={p03_sha}\n"
        f"  parent_v24_sha={v24_sha}\n"
        f"  parent_v23_sha={v23_sha}\n"
        f"  parent_v22_sha={v22_sha}\n"
        f"  parent_v20_sha={v20_sha}\n"
        f"  parent_v19_sha={v19_sha}\n"
        f"  parent_v17_sha={v17_sha}\n"
        f"  parent_v16_sha={v16_sha}\n",
        flush=True,
    )

    meta_path = PROJ / "07_Edit-Project/part04_rough_v25_land_meta.json"
    meta_path.write_text(
        json.dumps(
            {
                "cut": OUT.name,
                "path": str(OUT.relative_to(PROJ)),
                "bytes": bytes_n,
                "duration_s": dur,
                "sha256": digest,
                "parent_v24": PARENT_V24.name,
                "parent_v24_sha256": v24_sha,
                "parent_v23": PARENT_V23.name,
                "parent_v23_sha256": v23_sha,
                "parent_v22": PARENT_V22.name,
                "parent_v22_sha256": v22_sha,
                "parent_v20": PARENT_V20.name,
                "parent_v20_sha256": v20_sha,
                "parent_v19": parent_v19.name,
                "parent_v19_sha256": v19_sha,
                "bed": {
                    "path": str(BED.relative_to(PROJ)),
                    "note": "looped usable workshop body (~0-84s) soft-crossfade to cover VO",
                },
                "keep_remints": {
                    pid: {
                        "path": str(KEEP_REMINTS[pid][0].relative_to(PROJ)),
                        "sha256": plate_sha[pid],
                        "bytes": KEEP_REMINTS[pid][0].stat().st_size,
                    }
                    for pid in keep_swapped
                },
                "v20_kept_remints": {
                    pid: {
                        "path": str((RAW_V20 / f"{pid}_v20.mp4").relative_to(PROJ)),
                        "sha256": plate_sha[pid],
                        "bytes": (RAW_V20 / f"{pid}_v20.mp4").stat().st_size,
                    }
                    for pid in v20_kept
                },
                "plate_sha256": plate_sha,
                "no_paint_fallback": True,
                "plate_library_locked": True,
                "timeline": {
                    "plate07b_picture_s": [plate07b_start, plate07b_end],
                    "plate08_picture_s": [plate08_start, plate08_end],
                    "plate08b_picture_s": [plate08b_start, plate08b_end],
                    "plate09_picture_s": [plate09_start, plate09_end],
                    "plate09b_picture_s": [plate09b_start, plate09b_end],
                    "plate10_picture_s": [plate10_start, plate10_end],
                    "plate11_picture_s": [plate11_start, plate11_end],
                    "plate11b_picture_s": [plate11b_start, plate11b_end],
                    "explorer_picture_s": [explorer_start, explorer_end],
                },
                "p03_untouched_sha256": p03_sha,
                "hos_uat": str(ICLOUD / OUT.name),
                "watch": "WATCH_part04_v25.txt",
                "ben_uat_v24": {
                    "moon_desk": "07+07b+08 were the same still-life; 07b→v12 eka cards, 08→walk to chair",
                    "07b_t2v": "try1/try2 FAIL fire — not assembled",
                },
                "status": (
                    "LANDED_FOR_UAT — Ben fix: kill repeating moon-desk; "
                    "do not declare PASS"
                ),
            },
            indent=2,
        )
        + "\n"
    )

    ICLOUD.mkdir(parents=True, exist_ok=True)
    dest = ICLOUD / OUT.name
    subprocess.run(["cp", "-f", str(OUT), str(dest)], check=True)
    watch_body = (
        "WATCH THIS FILE ONLY (Part 04 rough v25 — moon-desk still-life no longer repeats):\n"
        f"  {OUT.name}\n\n"
        "Ben UAT fix vs v24:\n"
        "- The moon-window / flasks / lamp / blank-cards still-life was playing on 07 + 07b + 08.\n"
        "- 07b is now unused unique v12 eka-placeholder cards (not that still-life).\n"
        "- 08 is a walk toward one vacant glowing chair (A PREDICTION / navigation).\n"
        "- 07 still uses the night desk once under EKA-SILICON (~60–68s).\n"
        "- 08b FAIL + 09 WIN + 09b try14 unchanged. Explorer + music unchanged.\n\n"
        "CoS / Picture→UAT gates for this cut:\n"
        "- KEEP remints:\n"
        "  · 05_columns_families try2B Quality sha 49437e7e…e8caa\n"
        "  · 06_explorer_leaves_gap try8B sha fd4627d2…5c7a70\n"
        "  · 07b_eka_names_rotate v12 eka-cards sha 450a0444…33f74f\n"
        "  · 08_prediction_navigation v25 try1 walk sha b189ef87…982cb0\n"
        "  · 08b_navigation_walk v24 try1 FAIL sha 83fc2c43…827a3\n"
        "  · 09_risk_bet v24 try1 WIN sha 4e15c3b6…055ad1\n"
        "  · 09b_risk_hold try14 Quality sha 47a6bdeb…44c38\n"
        "  · 10_family_before_weight try1A Quality sha 49240cbb…81b78\n"
        "  · 11_publish_gaps try9 sha 97d0c419…8cc72\n"
        "  · 11b_wait_and_hunt try1 sha 5602762e…3075e\n"
        "- Scrub ~68–83s: 07b cards then 08 walk — not the moon-desk twice.\n"
        "- NO PAINT FALLBACK. Part 01–03 LOCKED. Do NOT declare PASS.\n\n"
        "Reject with stills from THIS file only.\n"
        f"keep_p03_sha={p03_sha}\n"
        f"parent_v24_sha={v24_sha}\n"
        f"parent_v23_sha={v23_sha}\n"
        f"parent_v22_sha={v22_sha}\n"
        f"parent_v20_sha={v20_sha}\n"
        f"parent_v21_sha={v21_sha}\n"
        f"keep_remints={','.join(keep_swapped)}\n"
        f"explorer_picture={explorer_start:.3f}-{explorer_end:.3f}\n"
        f"plate07b_picture={plate07b_start:.3f}-{plate07b_end:.3f}\n"
        f"plate08_picture={plate08_start:.3f}-{plate08_end:.3f}\n"
        f"plate08b_picture={plate08b_start:.3f}-{plate08b_end:.3f}\n"
        f"plate09_picture={plate09_start:.3f}-{plate09_end:.3f}\n"
        f"plate09b_picture={plate09b_start:.3f}-{plate09b_end:.3f}\n"
        f"plate10_picture={plate10_start:.3f}-{plate10_end:.3f}\n"
        f"plate11_picture={plate11_start:.3f}-{plate11_end:.3f}\n"
        f"plate11b_picture={plate11b_start:.3f}-{plate11b_end:.3f}\n"
        f"plate05_sha256={plate_sha.get('05_columns_families')}\n"
        f"plate06_sha256={plate_sha.get('06_explorer_leaves_gap')}\n"
        f"plate07b_sha256={plate_sha.get('07b_eka_names_rotate')}\n"
        f"plate08_sha256={plate_sha.get('08_prediction_navigation')}\n"
        f"plate08b_sha256={plate_sha.get('08b_navigation_walk')}\n"
        f"plate09_sha256={plate_sha.get('09_risk_bet')}\n"
        f"plate10_sha256={plate_sha.get('10_family_before_weight')}\n"
        f"plate09b_sha256={plate_sha.get('09b_risk_hold')}\n"
        f"plate11_sha256={plate_sha.get('11_publish_gaps')}\n"
        f"plate11b_sha256={plate_sha.get('11b_wait_and_hunt')}\n"
        f"bed={BED.name}\n"
        f"sha256={digest}\nbytes={bytes_n}\nduration={dur:.3f}\n"
    )
    watch = ICLOUD / "WATCH_part04_v25.txt"
    watch.write_text(watch_body)
    (PROJ / "07_Edit-Project/WATCH_part04_v25.txt").write_text(watch_body)
    (ICLOUD / "ZZ_OPEN_PART04_V25_ONLY.txt").write_text(
        "Part 04 current cut = hos_002_part04_rough_v25.mp4\n"
        "Part 01–03 LOCKED keepers.\n"
        "Ben fix: moon-desk still-life no longer repeats — watch v25 only.\n"
    )
    (ICLOUD / "PART04_NEXT.txt").write_text(
        "Part 04 rough assemble LANDED: hos_002_part04_rough_v25.mp4\n"
        "Watch WATCH_part04_v25.txt\n"
        "Ben UAT: moon-desk still-life no longer repeats. Scores → CoS. Do not declare PASS.\n"
    )
    (PROJ / "07_Edit-Project/PART04_NEXT.txt").write_text(
        "Part 04 rough assemble LANDED: hos_002_part04_rough_v25.mp4\n"
        "Watch WATCH_part04_v25.txt\n"
        "Ben UAT: moon-desk still-life no longer repeats. Scores → CoS. Do not declare PASS.\n"
    )
    print(f"ICLOUD {dest}", flush=True)
    print(f"WATCH {watch}", flush=True)
    print(f"META {meta_path}", flush=True)


if __name__ == "__main__":
    main()
