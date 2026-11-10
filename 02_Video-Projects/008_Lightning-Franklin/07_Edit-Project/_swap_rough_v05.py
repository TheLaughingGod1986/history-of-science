#!/usr/bin/env python3
"""J1248: diagnostic rough v05 = rough v04 with 5 FIX code-graphic rows swapped.

Uses code_graphics_v04 for:
  P2:15 likeness_fire, P3:03 rod_cloud, P3:04 letter_crosses,
  P4:06 same_thing (restore ELECTRICITY label on sequential plates),
  P5:10 metal_easy (METAL CONDUCTS stroke/contrast).
Same pause trims / timeline lengths as v04. Re-runs polish_gate + picture_qa
+ music_gate note. £0. No music bed. No upload. Never overwrite v02/v03/v04.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import shutil
import subprocess as sp
import sys
import traceback
from pathlib import Path

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

asm.CG_DIR = EDIT_DIR / "code_graphics_v04"
asm.CG_DIR_FALLBACK = EDIT_DIR / "code_graphics_v03"

WORK = Path("/Volumes/data/mac-mini-archive/tmp-render-scratch/j1248-hos008-rough-v05")
PRECHECK = MEDIA_DIR / "07_Edit-Project/_precheck/rough_v05"
DESK = EDIT_DIR / "_desk/008/rough_v05"
V04_PRE = MEDIA_DIR / "07_Edit-Project/_precheck/rough_v04"
V04_MP4 = V04_PRE / "hos_008_rough_v04.mp4"
V04_CUTS = V04_PRE / "cuts_rough_v04.json"
V04_POOL = V04_PRE / "pool_rough_v04.json"
V04_PAUSE = V04_PRE / "PAUSE_TRIM_v03.json"

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
    "06_same_thing": {
        "kind": "sequential_plus_label",
        "alpha": "code_graphic_008_p4_06_same_thing.mov",
        "asset": "overlay_06_same_thing.mp4",
    },
    "10_metal_easy": {
        "kind": "overlay",
        "alpha": "code_graphic_008_p5_10_metal_easy.mov",
        "plates": [("05", "06_rod_fitting", "full")],
        "asset": "overlay_10_metal_easy.mp4",
    },
}

OVERLAY_EVIDENCE = [
    "15_likeness_fire",
    "04_letter_crosses",
    "06_same_thing",
    "08_looking_path",
    "10_metal_easy",
]
# Also grab rod_cloud (full-frame CG) mid stills via its cut window.
CG_EVIDENCE = ["03_rod_cloud"]
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


def build_same_thing_with_label(mint: dict, use_s: float, out: Path) -> Path:
    """Sequential jar/knuckle plates + ELECTRICITY alpha overlay (J1241 FIX)."""
    base = out.with_suffix(".seq.mp4")
    asm.build_sequential_same_thing(mint, use_s, base)
    alpha_path = asm.cg_file("code_graphic_008_p4_06_same_thing.mov")
    tmp = out.with_suffix(".building.mp4")
    filt = (
        f"[0:v]scale={W}:{H}:flags=lanczos,fps={FPS},format=rgba[base];"
        f"[1:v]scale={W}:{H}:flags=lanczos,fps={FPS},format=rgba[ov];"
        f"[base][ov]overlay=0:0:format=auto,format=yuv420p[v]"
    )
    sp.run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-t", f"{use_s:.3f}", "-i", str(base),
            "-t", f"{use_s:.3f}", "-i", str(alpha_path),
            "-filter_complex", filt, "-map", "[v]", "-an",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "17",
            "-t", f"{use_s:.3f}", "-movflags", "+faststart", str(tmp),
        ],
        check=True,
    )
    tmp.replace(out)
    base.unlink(missing_ok=True)
    print(f"  sequential+label 06_same_thing: {probe_dur(out):.2f}s", flush=True)
    return out


def build_fix_assets(mint: dict) -> dict[str, Path]:
    asset_dir = WORK / "special_assets"
    asset_dir.mkdir(parents=True, exist_ok=True)
    out: dict[str, Path] = {}
    cuts = {c["row"]: c for c in json.loads(V04_CUTS.read_text())}
    for pid, meta in FIX_ROWS.items():
        cut = cuts[pid]
        use_s = float(cut["timeline_out"]) - float(cut["timeline_in"])
        dst = asset_dir / meta["asset"]
        dst.unlink(missing_ok=True)
        if meta["kind"] == "overlay":
            asm.build_overlay_composite(pid, meta, mint, use_s, dst)
        elif meta["kind"] == "sequential_plus_label":
            build_same_thing_with_label(mint, use_s, dst)
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
    cuts = json.loads(V04_CUTS.read_text())
    by = {c["row"]: c for c in cuts}
    work = WORK / "splice"
    work.mkdir(parents=True, exist_ok=True)
    events = sorted(
        ((float(by[pid]["timeline_in"]), float(by[pid]["timeline_out"]), pid) for pid in FIX_ROWS),
        key=lambda x: x[0],
    )
    segments: list[tuple[str, Path | None, float, float]] = []
    cursor = 0.0
    master_dur = probe_dur(V04_MP4)
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
        want = max(0.0, b - a)
        if kind == "keep":
            sp.run(
                [
                    "ffmpeg", "-y", "-v", "error",
                    "-i", str(V04_MP4),
                    "-ss", f"{a:.4f}", "-t", f"{want:.4f}",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k",
                    "-avoid_negative_ts", "make_zero",
                    str(out),
                ],
                check=True,
            )
        else:
            aud = work / f"aud_{i:02d}.m4a"
            sp.run(
                [
                    "ffmpeg", "-y", "-v", "error",
                    "-i", str(V04_MP4),
                    "-ss", f"{a:.4f}", "-t", f"{want:.4f}",
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
        got = probe_dur(out)
        if abs(got - want) > 0.35:
            raise RuntimeError(f"seg {i} {kind} duration {got:.3f}s != want {want:.3f}s ({a:.3f}-{b:.3f})")
        parts.append(out)
        print(f"  seg {i} {kind} {a:.3f}-{b:.3f} -> {got:.3f}s (want {want:.3f})", flush=True)

    lst = work / "concat.txt"
    lst.write_text("".join(f"file '{p}'\n" for p in parts))
    raw = work / "hos_008_rough_v05_raw.mp4"
    sp.run(
        [
            "ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
            str(raw),
        ],
        check=True,
    )
    out_mp4 = WORK / "hos_008_rough_v05.mp4"
    shutil.copy2(raw, out_mp4)
    print(f"spliced master {out_mp4} dur={probe_dur(out_mp4):.3f}", flush=True)
    return out_mp4


def update_cuts(assets: dict[str, Path]) -> list[dict]:
    cuts = json.loads(V04_CUTS.read_text())
    for c in cuts:
        if c["row"] in assets:
            p = assets[c["row"]]
            c["source"] = p.name
            c["source_path"] = str(p)
            c["source_sha256"] = sha256_file(p)
            c["disposition"] = f"J1248 v04 FIX swap (£0, {p.name})"
    return cuts


def extract_evidence(master: Path, cuts: list[dict], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    by = {c["row"]: c for c in cuts}
    for row in OVERLAY_EVIDENCE:
        c = by[row]
        tin, tout = float(c["timeline_in"]), float(c["timeline_out"])
        for pct in (25, 50, 75):
            t = tin + (tout - tin) * (pct / 100.0)
            dest = out_dir / f"overlay_{row}_p{pct}.jpg"
            sp.run(
                ["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.3f}", "-i", str(master),
                 "-frames:v", "1", "-q:v", "2", str(dest)],
                check=True,
            )
            print(f"  evidence {dest.name} @{t:.2f}s", flush=True)
    # P4:06 spoken ELECTRICITY at +5.14s into the row.
    c = by["06_same_thing"]
    tin = float(c["timeline_in"])
    spoken_t = tin + 5.14
    dest = out_dir / "overlay_06_same_thing_spoken_electricity.jpg"
    sp.run(
        ["ffmpeg", "-y", "-v", "error", "-ss", f"{spoken_t:.3f}", "-i", str(master),
         "-frames:v", "1", "-q:v", "2", str(dest)],
        check=True,
    )
    print(f"  evidence {dest.name} @{spoken_t:.2f}s (spoken +5.14)", flush=True)
    for row in CG_EVIDENCE:
        c = by[row]
        tin, tout = float(c["timeline_in"]), float(c["timeline_out"])
        for pct in (25, 50, 75):
            t = tin + (tout - tin) * (pct / 100.0)
            dest = out_dir / f"cg_{row}_p{pct}.jpg"
            sp.run(
                ["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.3f}", "-i", str(master),
                 "-frames:v", "1", "-q:v", "2", str(dest)],
                check=True,
            )
            print(f"  evidence {dest.name} @{t:.2f}s", flush=True)
    for row in WARN_ROWS:
        c = by[row]
        tin, tout = float(c["timeline_in"]), float(c["timeline_out"])
        t = (tin + tout) / 2.0
        dest = out_dir / f"warn_{row}.jpg"
        sp.run(
            ["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.3f}", "-i", str(master),
             "-frames:v", "1", "-q:v", "2", str(dest)],
            check=True,
        )
        print(f"  warn {dest.name} @{t:.2f}s", flush=True)


def run_gates(master: Path, cuts: list[dict], out_dir: Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    cuts_path = out_dir / "cuts_rough_v05.json"
    cuts_path.write_text(json.dumps(cuts, indent=2) + "\n")
    pool_path = out_dir / "pool_rough_v05.json"
    shutil.copy2(V04_POOL, pool_path)
    shutil.copy2(V04_PAUSE, out_dir / "PAUSE_TRIM_v03.json")

    sheet = out_dir / "contact_rough_v05.jpg"
    asm.contact_sheet(master, cuts, out_dir, sheet)

    polish_json = out_dir / "polish_gate_rough_v05.json"
    polish = sp.run(
        [sys.executable, str(OWB_ROOT / "scripts/polish_gate.py"), str(master),
         "--cuts", str(cuts_path), "--out", str(polish_json)],
        capture_output=True, text=True,
    )
    (out_dir / "polish_gate_rough_v05.txt").write_text(polish.stdout + polish.stderr)
    print(polish.stdout[-800:], flush=True)

    pq_dir = out_dir / "picture_qa_rough_v05"
    picture = sp.run(
        [sys.executable, str(OWB_ROOT / "scripts/picture_qa.py"), str(master),
         "--cuts", str(cuts_path), "--pool", str(pool_path), "--out-dir", str(pq_dir)],
        capture_output=True, text=True,
    )
    (out_dir / "picture_qa_rough_v05.txt").write_text(picture.stdout + picture.stderr)
    print(picture.stdout[-800:], flush=True)

    music_note = {
        "status": "SKIPPED_NO_BED",
        "reason": "No new bed without Chief OK (AGENTS.md credit hold / job brief).",
        "version": "rough_v05",
    }
    (out_dir / "music_gate_rough_v05.json").write_text(json.dumps(music_note, indent=2) + "\n")
    (out_dir / "music_gate_rough_v05.txt").write_text("SKIPPED_NO_BED\n")

    return {
        "polish_rc": polish.returncode,
        "picture_rc": picture.returncode,
        "polish_tail": (polish.stdout + polish.stderr)[-400:],
        "picture_tail": (picture.stdout + picture.stderr)[-400:],
    }


def safe_copy(src: Path, dst: Path) -> None:
    """Copy via a sibling temp file. iCloud UAT rejects in-place wb and some reads (errno 11)."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.resolve() == dst.resolve():
        return
    try:
        if dst.exists() and src.stat().st_size == dst.stat().st_size and src.stat().st_size > 8_000_000:
            return
    except OSError:
        pass
    tmp = dst.with_name(dst.name + ".partial")
    if tmp.exists():
        tmp.unlink()
    shutil.copy2(src, tmp)
    os.replace(tmp, dst)


def safe_write(dst: Path, text: str) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    tmp = dst.with_name(dst.name + ".partial")
    if tmp.exists():
        tmp.unlink()
    tmp.write_text(text)
    os.replace(tmp, dst)


def safe_copytree(src: Path, dst: Path) -> None:
    dst.mkdir(parents=True, exist_ok=True)
    for p in src.rglob("*"):
        if p.name.startswith("._"):
            continue
        rel = p.relative_to(src)
        target = dst / rel
        if p.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        elif p.is_file():
            safe_copy(p, target)


def deliver(master: Path, pack_dir: Path, evidence_dir: Path, gates: dict) -> dict:
    PRECHECK.mkdir(parents=True, exist_ok=True)
    DESK.mkdir(parents=True, exist_ok=True)
    uat = UAT_ROOT / "HOS-008_Lightning-Franklin_rough_v05"
    nas = NAS_FILM / "07_Edit-Project/_desk/008/rough_v05"
    uat.mkdir(parents=True, exist_ok=True)
    nas.mkdir(parents=True, exist_ok=True)

    files = [
        master.name,
        "cuts_rough_v05.json",
        "pool_rough_v05.json",
        "PAUSE_TRIM_v03.json",
        "contact_rough_v05.jpg",
        "polish_gate_rough_v05.json",
        "polish_gate_rough_v05.txt",
        "picture_qa_rough_v05.txt",
        "music_gate_rough_v05.json",
        "music_gate_rough_v05.txt",
    ]
    for name in files:
        src = pack_dir / name if name != master.name else master
        if not src.exists() and name == master.name:
            src = master
        if src.exists():
            for dest_root in (PRECHECK, DESK, uat, nas, pack_dir):
                dest_root.mkdir(parents=True, exist_ok=True)
                dst = dest_root / (master.name if name == master.name else name)
                safe_copy(src, dst)

    pq = pack_dir / "picture_qa_rough_v05"
    for dest_root in (PRECHECK, DESK, uat, nas):
        if pq.exists():
            safe_copytree(pq, dest_root / "picture_qa_rough_v05")
        if evidence_dir.exists():
            safe_copytree(evidence_dir, dest_root / "composite_evidence_v05")

    fix_sheet = EDIT_DIR / "code_graphics_v04" / "CONTACT_SHEET_FIX5.jpg"
    if fix_sheet.exists():
        for dest_root in (PRECHECK, DESK, uat, nas, evidence_dir):
            safe_copy(fix_sheet, dest_root / "CONTACT_SHEET_FIX5.jpg")

    summary = {
        "version": "rough_v05",
        "job": "J1248",
        "source_master": str(V04_MP4),
        "source_sha256": sha256_file(V04_MP4),
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
    (pack_dir / "ROUGH_V05_SUMMARY.json").write_text(json.dumps(summary, indent=2) + "\n")
    for dest_root in (PRECHECK, DESK, uat, nas):
        safe_copy(pack_dir / "ROUGH_V05_SUMMARY.json", dest_root / "ROUGH_V05_SUMMARY.json")
        sums = []
        for p in sorted(dest_root.iterdir()):
            if not p.is_file() or p.name in {"SHA256SUMS.txt"} or p.name.endswith(".partial") or p.name.startswith("._"):
                continue
            try:
                digest = sha256_file(p)
            except OSError:
                src = pack_dir / p.name
                digest = sha256_file(src if src.exists() else master)
            sums.append(f"{digest}  {p.name}\n")
        safe_write(dest_root / "SHA256SUMS.txt", "".join(sums))
    delivered = {
        "job": "J1248",
        "version": "rough_v05",
        "master_sha256": summary["master_sha256"],
        "duration_s": summary["duration_s"],
        "gates": {
            "polish": "PASS" if gates["polish_rc"] == 0 else "FAIL",
            "picture_qa": "PASS" if gates["picture_rc"] == 0 else "FAIL",
            "music": "SKIPPED_NO_BED",
        },
        "paths": summary["deliver"],
        "composite_evidence": "composite_evidence_v05/",
        "fix_rows": list(FIX_ROWS),
        "note": "Parked for Chief: graphics + composite evidence. No finished-film PASS. No music bed.",
    }
    for dest_root in (PRECHECK, DESK, uat, nas, pack_dir):
        safe_write(dest_root / "DELIVERED.json", json.dumps(delivered, indent=2) + "\n")
    print(json.dumps(summary, indent=2), flush=True)
    return summary


def main() -> int:
    WORK.mkdir(parents=True, exist_ok=True)
    if not V04_MP4.exists():
        raise FileNotFoundError(V04_MP4)
    if not (EDIT_DIR / "code_graphics_v04" / "MANIFEST.json").exists():
        raise FileNotFoundError("code_graphics_v04 missing — run _build_code_graphics_v04.py first")
    print("Loading mint index…", flush=True)
    mint = asm.load_mint_index()
    print(f"KEEP Flow clips: {len(mint)}", flush=True)
    print("Building 5 FIX special assets from code_graphics_v04…", flush=True)
    assets = build_fix_assets(mint)
    print("Splicing into rough v04…", flush=True)
    master = splice_master(assets)
    if probe_dur(master) > 540.5:
        raise RuntimeError(f"runtime {probe_dur(master):.3f}s > 540s lock")
    cuts = update_cuts(assets)
    pack = WORK / "pack"
    pack.mkdir(parents=True, exist_ok=True)
    shutil.copy2(master, pack / master.name)
    evidence = pack / "composite_evidence_v05"
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
