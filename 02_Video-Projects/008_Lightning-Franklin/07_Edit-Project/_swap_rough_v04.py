#!/usr/bin/env python3
"""J1241: diagnostic rough v04 = rough v03 with 4 FIX code-graphic rows swapped.

Uses code_graphics_v03 for P2:15 / P3:03 / P3:04 / P3:15 only. Same pause trims /
timeline lengths as v03. Re-runs polish_gate + picture_qa + music_gate note.
£0. No music bed. No upload.
"""
from __future__ import annotations

import hashlib
import json
import math
import shutil
import subprocess as sp
import sys
import traceback
from pathlib import Path

# Reuse helpers / constants from the v03 assembler.
import importlib.util

EDIT_DIR = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("asm_v03", EDIT_DIR / "_assemble_rough_v03.py")
asm = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(asm)

W, H, FPS = asm.W, asm.H, asm.FPS
MEDIA_DIR = asm.MEDIA_DIR
OWB_ROOT = asm.OWB_ROOT
UAT_ROOT = asm.UAT_ROOT
NAS_FILM = asm.NAS_FILM

# Point the assembler helpers at v03 graphics.
asm.CG_DIR = EDIT_DIR / "code_graphics_v03"
asm.CG_DIR_FALLBACK = EDIT_DIR / "code_graphics_v02"

WORK = Path("/Volumes/data/mac-mini-archive/tmp-render-scratch/j1241-hos008-rough-v04")
PRECHECK = MEDIA_DIR / "07_Edit-Project/_precheck/rough_v04"
DESK = EDIT_DIR / "_desk/008/rough_v04"
V03_PRE = MEDIA_DIR / "07_Edit-Project/_precheck/rough_v03"
V03_MP4 = V03_PRE / "hos_008_rough_v03.mp4"
V03_CUTS = V03_PRE / "cuts_rough_v03.json"
V03_POOL = V03_PRE / "pool_rough_v03.json"
V03_PAUSE = V03_PRE / "PAUSE_TRIM_v03.json"

FIX_ROWS = {
    "15_likeness_fire": {
        "kind": "overlay",
        "alpha": "code_graphic_008_p2_15_likeness_fire.mov",
        "plates": [("02", "12_notebook_list", "tail")],
        "asset": "overlay_15_likeness_fire.mp4",
    },
    "03_rod_cloud": {
        "kind": "cg",
        "file": "code_graphic_008_p3_03_rod_cloud.mp4",
        "asset": "cg_03_rod_cloud.mp4",
    },
    "04_letter_crosses": {
        "kind": "overlay",
        "alpha": "code_graphic_008_p3_04_letter_crosses.mov",
        "plates": [("03", "07_slow_news", "full")],
        "asset": "overlay_04_letter_crosses.mp4",
    },
    "15_wet_dry": {
        "kind": "cg",
        "file": "code_graphic_008_p3_15_wet_dry.mp4",
        "asset": "cg_15_wet_dry.mp4",
    },
}

# Overlay evidence + WARN plate rows for composite frames (job step 3).
OVERLAY_EVIDENCE = [
    "15_likeness_fire",
    "04_letter_crosses",
    "06_same_thing",
    "08_looking_path",
    "10_metal_easy",
]
WARN_ROWS = [
    "13_ring_the_bells_c1",
    "15_wet_dry",
    "19_kite_climb",
    "06_same_thing",
    "02_wire_bells",
    "18_rod_closeup",
]


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def probe_dur(p: Path) -> float:
    return float(
        sp.check_output(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(p)],
            text=True,
        ).strip()
    )


def build_fix_assets(mint: dict) -> dict[str, Path]:
    asset_dir = WORK / "special_assets"
    asset_dir.mkdir(parents=True, exist_ok=True)
    out: dict[str, Path] = {}
    cuts = {c["row"]: c for c in json.loads(V03_CUTS.read_text())}
    for pid, meta in FIX_ROWS.items():
        cut = cuts[pid]
        use_s = float(cut["timeline_out"]) - float(cut["timeline_in"])
        dst = asset_dir / meta["asset"]
        dst.unlink(missing_ok=True)
        if meta["kind"] == "overlay":
            asm.build_overlay_composite(pid, meta, mint, use_s, dst)
        else:
            src = asm.cg_file(meta["file"])
            sp.run(
                [
                    "ffmpeg", "-y", "-v", "error", "-i", str(src),
                    "-an", "-vf", f"scale={W}:{H}:flags=lanczos,fps={FPS}",
                    "-t", f"{use_s:.4f}",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p",
                    str(dst),
                ],
                check=True,
            )
            print(f"  cg {pid}: {probe_dur(dst):.3f}s -> target {use_s:.3f}s", flush=True)
        # Force exact frame count match to the cut.
        frames = int(cut["frames"])
        exact = asset_dir / f"exact_{meta['asset']}"
        sp.run(
            [
                "ffmpeg", "-y", "-v", "error", "-i", str(dst),
                "-vf", f"fps={FPS},scale={W}:{H}:flags=lanczos",
                "-frames:v", str(frames),
                "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p",
                str(exact),
            ],
            check=True,
        )
        exact.replace(dst)
        out[pid] = dst
        print(f"  ready {pid}: frames={frames} dur={probe_dur(dst):.3f}", flush=True)
    return out


def splice_master(assets: dict[str, Path]) -> Path:
    """Replace the four FIX segments in rough v03; keep audio from v03."""
    cuts = json.loads(V03_CUTS.read_text())
    by = {c["row"]: c for c in cuts}
    work = WORK / "splice"
    work.mkdir(parents=True, exist_ok=True)
    # Build ordered splice list: keep / replace / keep ...
    events = sorted(
        ((float(by[pid]["timeline_in"]), float(by[pid]["timeline_out"]), pid) for pid in FIX_ROWS),
        key=lambda x: x[0],
    )
    segments: list[tuple[str, Path | None, float, float]] = []
    cursor = 0.0
    master_dur = probe_dur(V03_MP4)
    for tin, tout, pid in events:
        if tin > cursor + 0.001:
            segments.append(("keep", None, cursor, tin))
        segments.append(("fix", assets[pid], tin, tout))
        cursor = tout
    if cursor < master_dur - 0.01:
        segments.append(("keep", None, cursor, master_dur))

    parts: list[Path] = []
    for i, (kind, src, a, b) in enumerate(segments):
        out = work / f"seg_{i:02d}.mp4"
        if kind == "keep":
            # Re-encode keeps so concat stays frame-accurate (copy drifts on keyframes).
            sp.run(
                [
                    "ffmpeg", "-y", "-v", "error",
                    "-ss", f"{a:.4f}", "-to", f"{b:.4f}", "-i", str(V03_MP4),
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k",
                    str(out),
                ],
                check=True,
            )
        else:
            # Replacement video + original audio underlay from the same window.
            aud = work / f"aud_{i:02d}.m4a"
            sp.run(
                [
                    "ffmpeg", "-y", "-v", "error",
                    "-ss", f"{a:.4f}", "-to", f"{b:.4f}", "-i", str(V03_MP4),
                    "-vn", "-c:a", "aac", "-b:a", "192k", str(aud),
                ],
                check=True,
            )
            sp.run(
                [
                    "ffmpeg", "-y", "-v", "error",
                    "-i", str(src), "-i", str(aud),
                    "-map", "0:v:0", "-map", "1:a:0",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k", "-shortest",
                    str(out),
                ],
                check=True,
            )
        parts.append(out)
        print(f"  seg {i} {kind} {a:.3f}-{b:.3f} -> {probe_dur(out):.3f}s", flush=True)

    # Re-encode concat (copy across mixed codecs is fragile after -c copy keeps).
    lst = work / "concat.txt"
    lst.write_text("".join(f"file '{p}'\n" for p in parts))
    raw = work / "hos_008_rough_v04_raw.mp4"
    sp.run(
        [
            "ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
            str(raw),
        ],
        check=True,
    )
    out_mp4 = WORK / "hos_008_rough_v04.mp4"
    shutil.copy2(raw, out_mp4)
    print(f"spliced master {out_mp4} dur={probe_dur(out_mp4):.3f}", flush=True)
    return out_mp4


def update_cuts(assets: dict[str, Path]) -> list[dict]:
    cuts = json.loads(V03_CUTS.read_text())
    for c in cuts:
        if c["row"] in assets:
            p = assets[c["row"]]
            c["source"] = p.name
            c["source_path"] = str(p)
            c["source_sha256"] = sha256_file(p)
            c["disposition"] = f"J1241 v03 FIX swap (£0, {p.name})"
    return cuts


def extract_evidence(master: Path, cuts: list[dict], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    by = {c["row"]: c for c in cuts}
    # Overlay rows at 25/50/75% of their timeline window.
    for row in OVERLAY_EVIDENCE:
        c = by[row]
        tin, tout = float(c["timeline_in"]), float(c["timeline_out"])
        for pct in (25, 50, 75):
            t = tin + (tout - tin) * (pct / 100.0)
            dest = out_dir / f"overlay_{row}_p{pct}.jpg"
            sp.run(
                [
                    "ffmpeg", "-y", "-v", "error",
                    "-ss", f"{t:.3f}", "-i", str(master), "-frames:v", "1",
                    "-q:v", "2", str(dest),
                ],
                check=True,
            )
            print(f"  evidence {dest.name} @{t:.2f}s", flush=True)
    # WARN plate mid-frames at film times (use timeline midpoint when present).
    for row in WARN_ROWS:
        c = by[row]
        tin, tout = float(c["timeline_in"]), float(c["timeline_out"])
        t = (tin + tout) / 2.0
        dest = out_dir / f"warn_{row}.jpg"
        sp.run(
            [
                "ffmpeg", "-y", "-v", "error",
                "-ss", f"{t:.3f}", "-i", str(master), "-frames:v", "1",
                "-q:v", "2", str(dest),
            ],
            check=True,
        )
        print(f"  warn {dest.name} @{t:.2f}s", flush=True)


def run_gates(master: Path, cuts: list[dict], out_dir: Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    cuts_path = out_dir / "cuts_rough_v04.json"
    cuts_path.write_text(json.dumps(cuts, indent=2) + "\n")
    pool_src = V03_POOL
    pool_path = out_dir / "pool_rough_v04.json"
    shutil.copy2(pool_src, pool_path)
    shutil.copy2(V03_PAUSE, out_dir / "PAUSE_TRIM_v03.json")

    # Contact sheet via v03 helper.
    sheet = out_dir / "contact_rough_v04.jpg"
    asm.contact_sheet(master, cuts, out_dir, sheet)

    polish_json = out_dir / "polish_gate_rough_v04.json"
    polish = sp.run(
        [
            sys.executable,
            str(OWB_ROOT / "scripts/polish_gate.py"),
            str(master),
            "--cuts", str(cuts_path),
            "--out", str(polish_json),
        ],
        capture_output=True,
        text=True,
    )
    (out_dir / "polish_gate_rough_v04.txt").write_text(polish.stdout + polish.stderr)
    print(polish.stdout[-800:], flush=True)

    pq_dir = out_dir / "picture_qa_rough_v04"
    picture = sp.run(
        [
            sys.executable,
            str(OWB_ROOT / "scripts/picture_qa.py"),
            str(master),
            "--cuts", str(cuts_path),
            "--pool", str(pool_path),
            "--out-dir", str(pq_dir),
        ],
        capture_output=True,
        text=True,
    )
    (out_dir / "picture_qa_rough_v04.txt").write_text(picture.stdout + picture.stderr)
    print(picture.stdout[-800:], flush=True)

    music_note = {
        "status": "SKIPPED_NO_BED",
        "reason": "No new bed without Chief OK until 30 Oct ElevenLabs reset (AGENTS.md).",
        "version": "rough_v04",
    }
    (out_dir / "music_gate_rough_v04.json").write_text(json.dumps(music_note, indent=2) + "\n")
    (out_dir / "music_gate_rough_v04.txt").write_text("SKIPPED_NO_BED\n")

    return {
        "polish_rc": polish.returncode,
        "picture_rc": picture.returncode,
        "polish_tail": (polish.stdout + polish.stderr)[-400:],
        "picture_tail": (picture.stdout + picture.stderr)[-400:],
    }


def deliver(master: Path, pack_dir: Path, evidence_dir: Path, gates: dict) -> dict:
    PRECHECK.mkdir(parents=True, exist_ok=True)
    DESK.mkdir(parents=True, exist_ok=True)
    uat = UAT_ROOT / "HOS-008_Lightning-Franklin_rough_v04"
    nas = NAS_FILM / "07_Edit-Project/_desk/008/rough_v04"
    uat.mkdir(parents=True, exist_ok=True)
    nas.mkdir(parents=True, exist_ok=True)

    files = [
        master.name,
        "cuts_rough_v04.json",
        "pool_rough_v04.json",
        "PAUSE_TRIM_v03.json",
        "contact_rough_v04.jpg",
        "polish_gate_rough_v04.json",
        "polish_gate_rough_v04.txt",
        "picture_qa_rough_v04.txt",
        "music_gate_rough_v04.json",
        "music_gate_rough_v04.txt",
    ]
    # Copy pack artefacts next to master first.
    for name in files:
        src = pack_dir / name if name != master.name else master
        if not src.exists() and name == master.name:
            src = master
        if src.exists():
            for dest_root in (PRECHECK, DESK, uat, nas, pack_dir):
                dest_root.mkdir(parents=True, exist_ok=True)
                dst = dest_root / (master.name if name == master.name else name)
                if src.resolve() != dst.resolve():
                    shutil.copy2(src, dst)

    # picture_qa dir + evidence
    pq = pack_dir / "picture_qa_rough_v04"
    for dest_root in (PRECHECK, DESK, uat, nas):
        if pq.exists():
            d = dest_root / "picture_qa_rough_v04"
            if d.exists():
                shutil.rmtree(d)
            shutil.copytree(pq, d)
        ev = dest_root / "composite_evidence_v04"
        if evidence_dir.exists():
            if ev.exists():
                shutil.rmtree(ev)
            shutil.copytree(evidence_dir, ev)

    # FIX contact sheet from graphics pack
    fix_sheet = EDIT_DIR / "code_graphics_v03" / "CONTACT_SHEET_FIX4.jpg"
    if fix_sheet.exists():
        for dest_root in (PRECHECK, DESK, uat, nas, evidence_dir):
            shutil.copy2(fix_sheet, dest_root / "CONTACT_SHEET_FIX4.jpg")

    summary = {
        "version": "rough_v04",
        "job": "J1241",
        "source_master": str(V03_MP4),
        "source_sha256": sha256_file(V03_MP4),
        "master": str(master),
        "master_sha256": sha256_file(master),
        "duration_s": probe_dur(master),
        "fix_rows": list(FIX_ROWS),
        "gates": gates,
        "deliver": {
            "precheck": str(PRECHECK),
            "desk": str(DESK),
            "uat": str(uat),
            "nas": str(nas),
        },
        "note": "Parked for Chief: graphics + composite evidence. No finished-film PASS.",
    }
    (pack_dir / "ROUGH_V04_SUMMARY.json").write_text(json.dumps(summary, indent=2) + "\n")
    for dest_root in (PRECHECK, DESK, uat, nas):
        shutil.copy2(pack_dir / "ROUGH_V04_SUMMARY.json", dest_root / "ROUGH_V04_SUMMARY.json")
        sums = []
        for p in sorted(dest_root.iterdir()):
            if p.is_file() and p.name != "SHA256SUMS.txt":
                sums.append(f"{sha256_file(p)}  {p.name}\n")
        (dest_root / "SHA256SUMS.txt").write_text("".join(sums))
    print(json.dumps(summary, indent=2), flush=True)
    return summary


def main() -> int:
    WORK.mkdir(parents=True, exist_ok=True)
    if not V03_MP4.exists():
        raise FileNotFoundError(V03_MP4)
    print("Loading mint index…", flush=True)
    mint = asm.load_mint_index()
    print(f"KEEP Flow clips: {len(mint)}", flush=True)
    print("Building 4 FIX special assets from code_graphics_v03…", flush=True)
    assets = build_fix_assets(mint)
    print("Splicing into rough v03…", flush=True)
    master = splice_master(assets)
    cuts = update_cuts(assets)
    pack = WORK / "pack"
    pack.mkdir(parents=True, exist_ok=True)
    shutil.copy2(master, pack / master.name)
    evidence = pack / "composite_evidence_v04"
    print("Extracting composite evidence frames…", flush=True)
    extract_evidence(master, cuts, evidence)
    print("Running gates…", flush=True)
    gates = run_gates(master, cuts, pack)
    print("Delivering…", flush=True)
    deliver(master, pack, evidence, gates)
    print("ALL DONE", flush=True)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception:
        traceback.print_exc()
        raise SystemExit(1)
