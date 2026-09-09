#!/usr/bin/env python3
"""Assemble HOS 002 Part 04 rough v20 — Flow Ultra remint v20 (bible 43d9405).

Parent FAIL: hos_002_part04_rough_v19.mp4
  sha256 05fb0a2b34dba1a8347ab74b2abc987fd406bef356b82b55f1a0e8ddb88cc6b5
UAT HARD FAIL parent v19: EXPLORER scalp/cards/lamp + PUBLISH ~118–127 continuous playback horizontal ghost/jitter (paint fallback).

Remint (Flow Ultra gallery mp4 ONLY): 06 · 08 · 08b · 09 · 09b · 10 · 11 · 11b
  Ben override FAIL v19 stills: unfinished Explorer · lava bulbs (A PREDICTION) ·
  unfinished 1:44 / FAMILY FIRST / publish overhead 2D.
KEEP: written cards ~40 where still clean; earlier locked plates unchanged.

NO PAINT. Scores → CoS. Do not declare PASS. Do not ping Ben.
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
LABEL_DIR = PROJ / "04_Generated-Clips/part04/refs/v06_side_labels"
VO = PROJ / "02_Voiceover/part04_empty_chairs_v01.wav"
BED = PROJ / "05_Music/hos_002_part01_curious_workshop_v02_norm.wav"
OUT = PROJ / "09_Final-Export/hos_002_part04_rough_v20.mp4"
PARENT_V19 = PROJ / "09_Final-Export/hos_002_part04_rough_v19.mp4"
PARENT_V19_SHA = "69d48f6e5fac419df5c23c17df5d0ef628cb4e8d533ba085bb3c8a173016bcdf"

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

REMINT_V20_IDS = {
    "06_explorer_leaves_gap",
    "08_prediction_navigation",
    "08b_navigation_walk",
    "09_risk_bet",
    "09b_risk_hold",
    "10_family_before_weight",
    "11_publish_gaps",
    "11b_wait_and_hunt",
}
KEEP_V18_IDS = set()  # family reminted in v20 (Ben flat/lava override)
KEEP_V16_IDS = set()
KEEP_V15_IDS = set()  # 09/09b reminted in v20 (Ben lava-chair override)
KEEP_V13_IDS = {
    "04_sort_atomic_weight",
    "05_columns_families",
}
KEEP_V12_IDS = {
    "05b_families_settle",
    "07_eka_placeholders",
}
KEEP_V11_IDS = {
    "07b_eka_names_rotate",
}
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
    if pid in REMINT_V20_IDS:
        clip = RAW_V20 / f"{pid}_v20.mp4"
        # Flow gallery mp4 must be real (~≥400KB). Refuse paint-tiny leftovers.
        if clip.exists() and clip.stat().st_size >= 400_000:
            return clip, "v20_flow_ultra_remint"
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
    v18_sha = require_sha(PARENT_V19, PARENT_V19_SHA, "v19 parent")
    v17_parent = PROJ / "09_Final-Export/hos_002_part04_rough_v17.mp4"
    v17_sha = require_sha(v17_parent, "e4cc41d8cf050f6726e6b3d5cbbbff10285656c588f3a758b4a29e1ec1f998fd", "v17 parent")
    v16_sha = require_sha(KEEP_V16_PARENT, KEEP_V16_PARENT_SHA, "v16 parent")
    require_sha(KEEP_V15_PARENT, KEEP_V15_PARENT_SHA, "v15 parent")
    require_sha(KEEP_V14_PARENT, KEEP_V14_PARENT_SHA, "v14 parent")
    require_sha(KEEP_V13_PARENT, KEEP_V13_PARENT_SHA, "v13 parent")
    require_sha(KEEP_V12_PARENT, KEEP_V12_PARENT_SHA, "v12 parent")
    require_sha(KEEP_V11_PARENT, KEEP_V11_PARENT_SHA, "v11 parent")

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
    reminted = [pid for pid, src in zip(ordered_ids, sources) if src == "v20_flow_ultra_remint"]
    plate06 = RAW_V20 / "06_explorer_leaves_gap_v20.mp4"
    plate06_sha = sha256(plate06) if plate06.exists() else None
    plate10 = RAW_V18 / "10_family_before_weight_v18.mp4"
    plate10_sha = sha256(plate10) if plate10.exists() else None
    plate11 = RAW_V20 / "11_publish_gaps_v20.mp4"
    plate11_sha = sha256(plate11) if plate11.exists() else None
    plate11b = RAW_V20 / "11b_wait_and_hunt_v20.mp4"
    plate11b_sha = sha256(plate11b) if plate11b.exists() else None
    print(
        f"LANDED {OUT}\n"
        f"  path={OUT}\n"
        f"  bytes={bytes_n}\n"
        f"  sha256={digest}\n"
        f"  duration={dur:.3f}\n"
        f"  reminted={reminted}\n"
        f"  plate06_sha256={plate06_sha}\n"
        f"  plate10_sha256={plate10_sha}\n"
        f"  plate11_sha256={plate11_sha}\n"
        f"  plate11b_sha256={plate11b_sha}\n"
        f"  explorer_picture={explorer_start:.2f}–{explorer_end:.2f}\n"
        f"  plate09b_picture={plate09b_start:.2f}–{plate09b_end:.2f}\n"
        f"  plate10_picture={plate10_start:.2f}–{plate10_end:.2f}\n"
        f"  plate11_picture={plate11_start:.2f}–{plate11_end:.2f}\n"
        f"  plate11b_picture={plate11b_start:.2f}–{plate11b_end:.2f}\n"
        f"  keep_p03_sha={p03_sha}\n"
        f"  parent_v19_sha={v18_sha}\n"
        f"  parent_v17_sha={v17_sha}\n"
        f"  parent_v16_sha={v16_sha}\n",
        flush=True,
    )

    methods = {
        pid: "Flow Ultra Veo 3.1 Fast I2V + real gallery mp4 harvest (NO paint)"
        for pid in reminted
    }
    flow_meta_path = PROJ / "07_Edit-Project/part04_mint_flow_v20_meta.json"
    flow_jobs = {}
    if flow_meta_path.exists():
        try:
            flow_jobs = json.loads(flow_meta_path.read_text()).get("flow_job_ids", {})
        except Exception:
            flow_jobs = {}
    meta_path = PROJ / "07_Edit-Project/part04_rough_v20_land_meta.json"
    meta_path.write_text(
        json.dumps(
            {
                "cut": OUT.name,
                "path": str(OUT.relative_to(PROJ)),
                "bytes": bytes_n,
                "duration_s": dur,
                "sha256": digest,
                "bible_main": "43d9405",
                "parent_v19": PARENT_V19.name,
                "parent_v19_sha256": v18_sha,
                "parent_v17": v17_parent.name,
                "parent_v17_sha256": v17_sha,
                "parent_v16": KEEP_V16_PARENT.name,
                "parent_v16_sha256": v16_sha,
                "reminted_plates": reminted,
                "plate_sha256": {pid: plate_sha[pid] for pid in reminted},
                "plates": {
                    pid: {
                        "path": str((RAW_V20 / f"{pid}_v20.mp4").relative_to(PROJ)),
                        "sha256": plate_sha[pid],
                        "bytes": (RAW_V20 / f"{pid}_v20.mp4").stat().st_size,
                    }
                    for pid in reminted
                },
                "methods": methods,
                "flow_job_ids": flow_jobs,
                "kept_from_v18": sorted(KEEP_V18_IDS),
                "kept_from_v15": sorted(KEEP_V15_IDS),
                "uat_blocker": (
                    "UAT HARD FAIL bible 43d9405 — PUBLISH ~118–127 continuous "
                    "horizontal ghost/jitter from paint fallback"
                ),
                "fail_times": {"publish_ghost_window": [118, 127], "explorer": [46, 53]},
                "timeline": {
                    "plate09b_picture_s": [plate09b_start, plate09b_end],
                    "plate10_picture_s": [plate10_start, plate10_end],
                    "plate11_picture_s": [plate11_start, plate11_end],
                    "plate11b_picture_s": [plate11b_start, plate11b_end],
                    "explorer_picture_s": [explorer_start, explorer_end],
                },
                "plate06_sha256": plate06_sha,
                "plate10_sha256": plate10_sha,
                "plate11_sha256": plate11_sha,
                "plate11b_sha256": plate11b_sha,
                "flow_account": "benoats@googlemail.com",
                "no_paint_fallback": True,
                "p03_untouched_sha256": p03_sha,
                "hos_uat": str(ICLOUD / OUT.name),
                "watch": "WATCH_part04_v20.txt",
                "doc": "PART04_V20_FLOW.md",
                "status": (
                    "LANDED_FOR_UAT — do not declare PASS; scores → CoS; no Ben ping"
                ),
            },
            indent=2,
        )
        + "\n"
    )

    ICLOUD.mkdir(parents=True, exist_ok=True)
    dest = ICLOUD / OUT.name
    subprocess.run(["cp", "-f", str(OUT), str(dest)], check=True)
    watch = ICLOUD / "WATCH_part04_v20.txt"
    watch.write_text(
        "WATCH THIS FILE ONLY (Part 04 rough v20 — Flow Ultra remint):\n"
        f"  {OUT.name}\n\n"
        "CoS / Picture→UAT gates for this cut:\n"
        "- Parent FAIL v18 sha 05fb0a2b… — bible 43d9405 PUBLISH continuous ghost "
        "(paint fallback caused it).\n"
        "- Reminted 06 / 08 / 08b / 09 / 09b / 10 / 11 / 11b via Flow Ultra Veo I2V + "
        "real gallery mp4 harvest.\n"
        "- NO PAINT FALLBACK. NO temporal-median.\n"
        "- KEEP: written cards ~40 · earlier locked plates (01–05 / 05b / 07 / 07b).\n"
        "- Spot ~48 Explorer: finished 3D crown, no scalp holes, clean cards, clean lamp.\n"
        "- Spot A PREDICTION: SOLID lamps — no lava/fire drip from the bulb.\n"
        "- Spot ~1:44 / FAMILY FIRST / PUBLISH: finished 3D cartoon, not flat unfinished 2D.\n"
        "- Part 01–03 LOCKED. Flow account benoats@googlemail.com.\n"
        "- Do NOT declare PASS here. Scores → CoS. No Ben ping.\n\n"
        "Reject with stills from THIS file only.\n"
        f"keep_p03_sha={p03_sha}\n"
        f"parent_v19_sha={v18_sha}\n"
        f"parent_v17_sha={v17_sha}\n"
        f"reminted={','.join(reminted)}\n"
        f"explorer_picture={explorer_start:.3f}-{explorer_end:.3f}\n"
        f"plate10_picture={plate10_start:.3f}-{plate10_end:.3f}\n"
        f"plate11_picture={plate11_start:.3f}-{plate11_end:.3f}\n"
        f"plate11b_picture={plate11b_start:.3f}-{plate11b_end:.3f}\n"
        f"sha256={digest}\nbytes={bytes_n}\nduration={dur:.3f}\n"
    )
    (PROJ / "07_Edit-Project/WATCH_part04_v20.txt").write_text(watch.read_text())
    (ICLOUD / "ZZ_OPEN_PART04_V20_ONLY.txt").write_text(
        "Part 04 current cut = hos_002_part04_rough_v20.mp4\n"
        "Part 01–03 LOCKED keepers.\n"
        "v18 paint FAIL → v20 Flow Ultra remint — watch v20 only.\n"
    )
    (ICLOUD / "PART04_NEXT.txt").write_text(
        "Part 04 rough remint LANDED: hos_002_part04_rough_v20.mp4\n"
        "Watch WATCH_part04_v20.txt · PART04_V20_FLOW.md\n"
        "Scores → CoS. Do not declare PASS. Do not ping Ben.\n"
    )
    print(f"ICLOUD {dest}", flush=True)
    print(f"WATCH {watch}", flush=True)
    print(f"META {meta_path}", flush=True)


if __name__ == "__main__":
    main()
