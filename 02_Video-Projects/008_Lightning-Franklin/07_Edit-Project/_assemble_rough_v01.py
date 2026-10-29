#!/usr/bin/env python3
"""HOS 008 — Rough v01 assembler (J1213).

Lays all 112 KEEP board rows (101 Flow KEEP + 11 £0 code graphics) to the locked
part VO per parts/*_plates_v03.json. Composites the five moving-plate alpha
overlays onto their minted plates. No music bed (Chief OK required; credit hold).
Runs polish_gate + picture_qa per part and on the full join; writes contact sheets.
£0 spend. Parks for Chief — Ben's watch only after Chief PASS.

J1193 (code-graphic motion review) had not landed at start; pack notes that hold.
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

import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1920, 1080, 24
FONT = "/System/Library/Fonts/Supplemental/Didot.ttc"
BROWN = (61, 41, 28)
CREAM = (245, 232, 210, 255)
GOLD = (242, 208, 122, 255)
SHADOW = (36, 22, 12)

EDIT_DIR = Path(__file__).resolve().parent
FILM_DIR = EDIT_DIR.parent
HOS_ROOT = FILM_DIR.parent.parent
OWB_ROOT = Path("/Users/benjaminoats/YouTube/orbit-with-ben")
MEDIA_DIR = Path(
    "/Users/benjaminoats/YouTube/hos-008-lightning/02_Video-Projects/008_Lightning-Franklin"
)
CG_DIR = EDIT_DIR / "code_graphics_v01"
WORK = Path("/private/tmp/j1213-hos008-rough-v01")
PRECHECK = MEDIA_DIR / "07_Edit-Project/_precheck/rough_v01"
DESK = EDIT_DIR / "_desk/008/rough_v01"
UAT_ROOT = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT"
NAS_FILM = Path(
    "/Volumes/data/mac-mini-archive/YouTube/History Of Science/02_Video-Projects/008_Lightning-Franklin"
)

# Five moving-plate overlay rows (alpha MOV over minted KEEP plates).
OVERLAY_COMPOSITES = {
    "15_likeness_fire": {
        "part": 2,
        "alpha": "code_graphic_008_p2_15_likeness_fire.mov",
        "plates": [("02", "12_notebook_list", "tail")],
    },
    "04_letter_crosses": {
        "part": 3,
        "alpha": "code_graphic_008_p3_04_letter_crosses.mov",
        "plates": [("03", "07_slow_news", "full")],
    },
    "06_same_thing": {
        "part": 4,
        "alpha": "code_graphic_008_p4_06_same_thing.mov",
        "plates": [("02", "08_jar_spark", "left"), ("04", "02_knuckle_spark", "right")],
    },
    "08_looking_path": {
        "part": 5,
        "alpha": "code_graphic_008_p5_08_looking_path.mov",
        "plates": [("01", "16_question_sky", "full")],
    },
    "10_metal_easy": {
        "part": 5,
        "alpha": "code_graphic_008_p5_10_metal_easy.mov",
        "plates": [("05", "06_rod_fitting", "full")],
    },
}


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def probe_dur(p: Path) -> float:
    return float(
        sp.check_output(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
            text=True,
        ).strip()
    )


def font(size: int, italic: bool = True) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT, size, index=1 if italic else 0)


def fit_font(text: str, max_w: int, size: int, floor: int = 28, italic: bool = True) -> ImageFont.FreeTypeFont:
    f = font(size, italic=italic)
    while size > floor and f.getbbox(text)[2] > max_w:
        size -= 2
        f = font(size, italic=italic)
    return f


def ease(x: float) -> float:
    x = max(0.0, min(1.0, x))
    return x * x * (3.0 - 2.0 * x)


def prog(t: float, a: float, b: float) -> float:
    return ease((t - a) / (b - a)) if b > a else 1.0


def card_alpha(t: float, start: float, end: float, fade: float = 0.36) -> float:
    if t < start or t > end:
        return 0.0
    inn = prog(t, start, start + fade)
    out = 1.0 - prog(t, end - fade, end)
    return max(0.0, min(inn, out))


def load_mint_index() -> dict[tuple[str, str], Path]:
    log = json.loads((EDIT_DIR / "FLOW_MINT_LOG_v03.json").read_text())
    out: dict[tuple[str, str], Path] = {}
    for _k, v in log["takes"].items():
        if v.get("status") != "KEEP":
            continue
        part = str(v["part"]).zfill(2)
        plate = v["plate"]
        fp = Path(v["file"])
        if not fp.exists():
            cand = MEDIA_DIR / f"04_Generated-Clips/part{part}/raw/v01/{plate}_t1.mp4"
            if cand.exists():
                fp = cand
            else:
                raise FileNotFoundError(f"KEEP file missing for P{part}:{plate}: {v['file']}")
        out[(part, plate)] = fp
    return out


def flow_clip(mint: dict[tuple[str, str], Path], part: str | int, plate: str) -> Path:
    p = str(part).zfill(2)
    if (p, plate) in mint:
        return mint[(p, plate)]
    cand = MEDIA_DIR / f"04_Generated-Clips/part{p}/raw/v01/{plate}_t1.mp4"
    if cand.exists():
        return cand
    raise FileNotFoundError(f"No Flow KEEP for P{p}:{plate}")


def draw_side_label(frame: Image.Image, text: str, t_local: float, use_s: float) -> Image.Image:
    """House cream Didot italic stamp, bottom centre; fades in/out; one label at a time."""
    # Hold label for min(3.6s, use_s - 0.4) starting 0.15s into the plate.
    start = 0.15
    end = min(use_s - 0.25, start + 3.6)
    if end <= start + 0.6:
        end = use_s - 0.1
    a = card_alpha(t_local, start, end, fade=0.35)
    if a <= 0.01:
        return frame
    im = frame.convert("RGBA")
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    slide = int((1.0 - prog(t_local, start, start + 0.4)) * 18)
    f = fit_font(text, 1500, 58, 34)
    sc = (*SHADOW, int(230 * a))
    d.text(
        (W / 2, 940 + slide),
        text,
        font=f,
        fill=(GOLD[0], GOLD[1], GOLD[2], int(255 * a)),
        anchor="mm",
        stroke_width=4,
        stroke_fill=sc,
    )
    return Image.alpha_composite(im, layer).convert("RGB")


def build_overlay_composite(pid: str, meta: dict, mint: dict, use_s: float, out: Path) -> Path:
    """Composite alpha overlay onto moving plate(s) via ffmpeg filters (fast)."""
    if out.exists():
        try:
            if abs(probe_dur(out) - use_s) < 0.15 and out.stat().st_size > 200_000:
                return out
        except Exception:
            pass
        out.unlink(missing_ok=True)
    out.parent.mkdir(parents=True, exist_ok=True)
    alpha_path = CG_DIR / meta["alpha"]
    assert alpha_path.exists(), f"missing alpha {alpha_path}"
    plates = meta["plates"]
    tmp = out.with_suffix(".building.mp4")

    if len(plates) == 1:
        part, plate, mode = plates[0]
        src = flow_clip(mint, part, plate)
        dur = probe_dur(src)
        start = max(0.0, dur - use_s - 0.05) if mode == "tail" else 0.0
        # Soft lift (eq) then overlay alpha MOV; force 24fps / exact length.
        filt = (
            f"[0:v]scale={W}:{H}:flags=lanczos,fps={FPS},"
            f"eq=brightness=0.04:contrast=0.96,format=rgba[base];"
            f"[1:v]scale={W}:{H}:flags=lanczos,fps={FPS},format=rgba[ov];"
            f"[base][ov]overlay=0:0:format=auto,format=yuv420p[v]"
        )
        cmd = [
            "ffmpeg", "-y", "-v", "error",
            "-ss", f"{start:.3f}", "-t", f"{use_s:.3f}", "-i", str(src),
            "-t", f"{use_s:.3f}", "-i", str(alpha_path),
            "-filter_complex", filt, "-map", "[v]", "-an",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "17",
            "-t", f"{use_s:.3f}", "-movflags", "+faststart", str(tmp),
        ]
    else:
        # P4:06 left/right split of two KEEP plates under the alpha divider.
        left = flow_clip(mint, plates[0][0], plates[0][1])
        right = flow_clip(mint, plates[1][0], plates[1][1])
        filt = (
            f"[0:v]scale={W}:{H}:flags=lanczos,fps={FPS},eq=brightness=0.04:contrast=0.96,crop={W//2}:{H}:0:0[L];"
            f"[1:v]scale={W}:{H}:flags=lanczos,fps={FPS},eq=brightness=0.04:contrast=0.96,crop={W//2}:{H}:{W//2}:0[R];"
            f"[L][R]hstack=inputs=2,format=rgba[base];"
            f"[2:v]scale={W}:{H}:flags=lanczos,fps={FPS},format=rgba[ov];"
            f"[base][ov]overlay=0:0:format=auto,format=yuv420p[v]"
        )
        cmd = [
            "ffmpeg", "-y", "-v", "error",
            "-t", f"{use_s:.3f}", "-i", str(left),
            "-t", f"{use_s:.3f}", "-i", str(right),
            "-t", f"{use_s:.3f}", "-i", str(alpha_path),
            "-filter_complex", filt, "-map", "[v]", "-an",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "17",
            "-t", f"{use_s:.3f}", "-movflags", "+faststart", str(tmp),
        ]
    sp.run(cmd, check=True)
    tmp.replace(out)
    print(f"  overlay {pid}: {probe_dur(out):.2f}s {out.stat().st_size} bytes", flush=True)
    return out


def prepare_special_assets(mint: dict) -> dict[str, Path]:
    asset_dir = WORK / "special_assets"
    asset_dir.mkdir(parents=True, exist_ok=True)
    out: dict[str, Path] = {}
    man = {r["row"].split(":", 1)[1]: r for r in json.loads((EDIT_DIR / "CODE_GRAPHICS_v01_MANIFEST.json").read_text())}

    # Full-frame code graphics: retime 30fps -> 24fps to exact use_s
    for pid, row in man.items():
        if pid in OVERLAY_COMPOSITES:
            continue
        src = CG_DIR / row["spec"]["file"]
        assert src.exists(), f"missing CG {src}"
        use_s = float(row["use_s"])
        dst = asset_dir / f"cg_{pid}.mp4"
        if not dst.exists() or abs(probe_dur(dst) - use_s) > 0.2:
            sp.run(
                [
                    "ffmpeg", "-y", "-v", "error", "-i", str(src),
                    "-an", "-vf", f"scale={W}:{H}:flags=lanczos,fps={FPS}",
                    "-t", f"{use_s:.3f}",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p",
                    str(dst),
                ],
                check=True,
            )
        out[pid] = dst

    # Moving-plate overlays
    for pid, meta in OVERLAY_COMPOSITES.items():
        use_s = float(man[pid]["use_s"])
        dst = asset_dir / f"overlay_{pid}.mp4"
        build_overlay_composite(pid, meta, mint, use_s, dst)
        out[pid] = dst
    return out


def resolve_source(
    part_no: int,
    plate: dict,
    mint: dict,
    special: dict[str, Path],
) -> tuple[Path, float, str, str]:
    pid = plate["id"]
    q = plate["quality"]
    if q in ("Quality", "Fast"):
        src = flow_clip(mint, part_no, pid)
        upscale = 1.0 if q == "Quality" else 1.5  # recorded for pool; we scale to 1080
        return src, 0.0, f"scale={W}:{H}:flags=lanczos,fps={FPS}", f"KEEP Flow {q} t1 (J1191)"
    if q == "code_graphic":
        src = special[pid]
        return src, 0.0, f"scale={W}:{H}:flags=lanczos,fps={FPS}", f"Code graphic v01 (£0, {src.name})"
    raise ValueError(f"Unknown quality {q} on P{part_no}:{pid}")


def contact_sheet(video: Path, cuts: list[dict], out_dir: Path, path: Path) -> None:
    cols, tw, th = 6, 320, 180
    rows = (len(cuts) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw, rows * (th + 28)), (28, 22, 18))
    d = ImageDraw.Draw(sheet)
    f = font(14, italic=False)
    for i, c in enumerate(cuts):
        mid = (c["timeline_in"] + c["timeline_out"]) / 2.0
        jpg = out_dir / f"_cs_{i:03d}.jpg"
        sp.run(
            [
                "ffmpeg", "-y", "-v", "error", "-ss", f"{mid:.3f}", "-i", str(video),
                "-frames:v", "1", "-vf", f"scale={tw}:{th}", str(jpg),
            ],
            check=True,
        )
        x, y = (i % cols) * tw, (i // cols) * (th + 28)
        sheet.paste(Image.open(jpg), (x, y))
        t = c["film_t"]
        d.text((x + 4, y + th + 4), f"{c['row'][:20]} {int(t // 60)}:{t % 60:05.2f}", font=f, fill=(240, 232, 215))
        jpg.unlink(missing_ok=True)
    sheet.save(path, quality=88)


def assemble_part(part_no: int, mint: dict, special: dict[str, Path]) -> dict:
    pstr = f"{part_no:02d}"
    board = json.loads((EDIT_DIR / "parts" / f"part-{pstr}_plates_v03.json").read_text())
    vo_path = FILM_DIR / board["vo_file"]
    assert vo_path.exists(), vo_path
    assert sha256_file(vo_path) == board["vo_sha256"], f"VO sha mismatch part {pstr}"

    slug = f"part{pstr}_rough_v01"
    name = f"hos_008_{slug}"
    out_dir = WORK / slug
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)
    seg_dir = out_dir / "segs"
    seg_dir.mkdir()

    t0 = float(board["vo_film_start_s"])
    end = float(board["part_end_film_s"])
    plates = board["plates"]
    cuts = []
    segs = []
    cur_frames = 0

    for k, p in enumerate(plates):
        nxt = float(plates[k + 1]["t_s"]) if k + 1 < len(plates) else end
        f_in = round((float(p["t_s"]) - t0) * FPS)
        f_out = round((nxt - t0) * FPS)
        n_frames = f_out - f_in
        assert n_frames > 0, f"P{pstr}:{p['id']} non-positive frames"

        src, start_s, vf, disp = resolve_source(part_no, p, mint, special)
        src_dur = probe_dur(src)
        need = n_frames / FPS
        if start_s + need > src_dur + 0.08:
            start_s = max(0.0, round(src_dur - need - 0.04, 3))

        seg_path = seg_dir / f"seg_{k:02d}_{p['id']}.mp4"
        label = (p.get("side_label") or "").strip()
        t_in_part = f_in / FPS
        t_out_part = f_out / FPS

        if not label:
            sp.run(
                [
                    "ffmpeg", "-y", "-v", "error", "-ss", f"{start_s:.3f}", "-i", str(src),
                    "-an", "-vf", vf, "-frames:v", str(n_frames),
                    "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-pix_fmt", "yuv420p", "-r", str(FPS),
                    str(seg_path),
                ],
                check=True,
            )
        else:
            dec = sp.Popen(
                [
                    "ffmpeg", "-v", "error", "-ss", f"{start_s:.3f}", "-i", str(src),
                    "-frames:v", str(n_frames), "-vf", vf,
                    "-f", "rawvideo", "-pix_fmt", "rgb24", "-",
                ],
                stdout=sp.PIPE,
            )
            enc = sp.Popen(
                [
                    "ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pixel_format", "rgb24",
                    "-video_size", f"{W}x{H}", "-framerate", str(FPS), "-i", "-", "-an",
                    "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-pix_fmt", "yuv420p", "-r", str(FPS),
                    str(seg_path),
                ],
                stdin=sp.PIPE,
            )
            assert dec.stdout and enc.stdin
            last = None
            use_s = t_out_part - t_in_part
            for f_idx in range(n_frames):
                buf = dec.stdout.read(W * H * 3)
                if len(buf) == W * H * 3:
                    im = Image.frombytes("RGB", (W, H), buf)
                    last = im
                elif last is not None:
                    im = last
                else:
                    im = Image.new("RGB", (W, H), BROWN)
                im = draw_side_label(im, label, f_idx / FPS, use_s)
                enc.stdin.write(im.tobytes())
            dec.stdout.close()
            dec.wait()
            enc.stdin.close()
            if enc.wait() != 0:
                raise RuntimeError(f"label encode failed {seg_path}")

        cuts.append(
            {
                "row": p["id"],
                "film_t": round(float(p["t_s"]), 2),
                "timeline_in": round(t_in_part, 4),
                "timeline_out": round(t_out_part, 4),
                "frames": n_frames,
                "upscale": 1.0 if p["quality"] == "Quality" else (1.0 if p["quality"] == "code_graphic" else 1.5),
                "side_label": label or None,
                "source": src.name,
                "source_path": str(src),
                "source_sha256": sha256_file(src),
                "framing": {"offset": round(start_s, 3)},
                "disposition": disp,
                "quality": p["quality"],
            }
        )
        segs.append(seg_path)
        cur_frames += n_frames
        print(f"  P{pstr} {k+1}/{len(plates)} {p['id']} {n_frames}f", flush=True)

    concat_txt = out_dir / "concat.txt"
    concat_txt.write_text("".join(f"file '{s}'\n" for s in segs))
    pic_mp4 = out_dir / "picture_only.mp4"
    sp.run(
        ["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(concat_txt), "-c", "copy", str(pic_mp4)],
        check=True,
    )
    total_s = cur_frames / FPS
    cut_mp4 = out_dir / f"{name}.mp4"
    sp.run(
        [
            "ffmpeg", "-y", "-v", "error", "-i", str(pic_mp4), "-i", str(vo_path),
            "-map", "0:v", "-map", "1:a", "-c:v", "copy",
            "-af", "apad", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
            "-t", f"{total_s:.3f}", "-movflags", "+faststart", str(cut_mp4),
        ],
        check=True,
    )
    shutil.rmtree(seg_dir, ignore_errors=True)
    pic_mp4.unlink(missing_ok=True)

    fd = sp.run(
        ["ffmpeg", "-i", str(cut_mp4), "-vf", "freezedetect=n=-60dB:d=0.8", "-map", "0:v", "-f", "null", "-"],
        stderr=sp.PIPE, text=True,
    ).stderr
    freeze = [ln for ln in fd.splitlines() if "lavfi.freezedetect" in ln]
    (out_dir / "freezedetect.log").write_text("\n".join(freeze) + ("\n" if freeze else ""))

    cuts_path = out_dir / f"cuts_{slug}.json"
    cuts_path.write_text(json.dumps(cuts, indent=2) + "\n")
    pool = []
    seen = set()
    for c in cuts:
        if c["source"] in seen:
            continue
        seen.add(c["source"])
        title = (
            "HOS house code graphic / overlay composite (£0)"
            if c["source"].startswith(("cg_", "overlay_", "code_graphic"))
            else "Flow Veo 3.1 clip, KEEP (J1191)"
        )
        pool.append({"file": c["source"], "title": title})
    pool_path = out_dir / f"pool_{slug}.json"
    pool_path.write_text(json.dumps(pool, indent=2) + "\n")

    sheet_path = out_dir / f"contact_{slug}.jpg"
    contact_sheet(cut_mp4, cuts, out_dir, sheet_path)

    # Gates
    pg_json = out_dir / f"polish_gate_{slug}.json"
    pq_dir = out_dir / f"picture_qa_{slug}"
    pq_dir.mkdir(exist_ok=True)
    polish = sp.run(
        [
            sys.executable, str(OWB_ROOT / "scripts/polish_gate.py"),
            str(cut_mp4), "--cuts", str(cuts_path), "--out", str(pg_json),
        ],
        capture_output=True, text=True,
    )
    (out_dir / f"polish_gate_{slug}.txt").write_text(polish.stdout + polish.stderr)
    picture = sp.run(
        [
            sys.executable, str(OWB_ROOT / "scripts/picture_qa.py"),
            str(cut_mp4), "--cuts", str(cuts_path), "--pool", str(pool_path),
            "--out-dir", str(pq_dir),
        ],
        capture_output=True, text=True,
    )
    (out_dir / f"picture_qa_{slug}.txt").write_text(picture.stdout + picture.stderr)

    meta = {
        "part": part_no,
        "slug": slug,
        "authority": "J1213 after J1191 PASS; PR #374 MERGED; J1193 code-graphic review still open at assemble start",
        "vo": str(vo_path),
        "vo_sha256": board["vo_sha256"],
        "picture_s": round(total_s, 4),
        "frames": cur_frames,
        "rows": len(cuts),
        "mp4": str(cut_mp4),
        "sha256": sha256_file(cut_mp4),
        "polish_gate_exit": polish.returncode,
        "picture_qa_exit": picture.returncode,
        "freeze_lines": len(freeze),
        "no_music": True,
        "j1193_note": "J1193 not landed; overlays used as delivered in CODE_GRAPHICS_v01 (P5:11 SAFE PATH DOWN fix applied)",
    }
    (out_dir / f"ROUGH_META_part{pstr}_v01.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(f"DONE part {pstr}: {total_s:.2f}s sha={meta['sha256'][:12]} polish={polish.returncode} pq={picture.returncode}", flush=True)
    return meta


def join_full(part_metas: list[dict]) -> dict:
    out_dir = WORK / "full_join_v01"
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)
    concat = out_dir / "concat.txt"
    lines = []
    all_cuts = []
    offset = 0.0
    pool = []
    seen = set()
    for m in part_metas:
        pstr = f"{m['part']:02d}"
        slug = f"part{pstr}_rough_v01"
        mp4 = WORK / slug / f"hos_008_{slug}.mp4"
        lines.append(f"file '{mp4}'\n")
        cuts = json.loads((WORK / slug / f"cuts_{slug}.json").read_text())
        for c in cuts:
            row = dict(c)
            row["part"] = m["part"]
            row["timeline_in"] = round(c["timeline_in"] + offset, 4)
            row["timeline_out"] = round(c["timeline_out"] + offset, 4)
            all_cuts.append(row)
            if c["source"] not in seen:
                seen.add(c["source"])
                pool.append({"file": c["source"], "title": c["disposition"]})
        offset += m["picture_s"]
    concat.write_text("".join(lines))
    out_mp4 = out_dir / "hos_008_rough_v01.mp4"
    sp.run(
        ["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(concat), "-c", "copy", "-movflags", "+faststart", str(out_mp4)],
        check=True,
    )
    cuts_path = out_dir / "cuts_rough_v01.json"
    cuts_path.write_text(json.dumps(all_cuts, indent=2) + "\n")
    pool_path = out_dir / "pool_rough_v01.json"
    pool_path.write_text(json.dumps(pool, indent=2) + "\n")
    sheet = out_dir / "contact_rough_v01.jpg"
    contact_sheet(out_mp4, all_cuts, out_dir, sheet)

    pg_json = out_dir / "polish_gate_rough_v01.json"
    pq_dir = out_dir / "picture_qa_rough_v01"
    pq_dir.mkdir(exist_ok=True)
    polish = sp.run(
        [sys.executable, str(OWB_ROOT / "scripts/polish_gate.py"), str(out_mp4), "--cuts", str(cuts_path), "--out", str(pg_json)],
        capture_output=True, text=True,
    )
    (out_dir / "polish_gate_rough_v01.txt").write_text(polish.stdout + polish.stderr)
    picture = sp.run(
        [
            sys.executable, str(OWB_ROOT / "scripts/picture_qa.py"),
            str(out_mp4), "--cuts", str(cuts_path), "--pool", str(pool_path), "--out-dir", str(pq_dir),
        ],
        capture_output=True, text=True,
    )
    (out_dir / "picture_qa_rough_v01.txt").write_text(picture.stdout + picture.stderr)

    # music_gate: VO-only rough — no bed laid (credit hold until Chief OK). Record skip.
    music_note = {
        "status": "SKIPPED_NO_BED",
        "reason": "J1213: no music bed without Chief OK (ElevenLabs credit hold to 30 Oct). VO-only rough.",
        "video": str(out_mp4),
        "duration_s": probe_dur(out_mp4),
    }
    (out_dir / "music_gate_rough_v01.json").write_text(json.dumps(music_note, indent=2) + "\n")
    (out_dir / "music_gate_rough_v01.txt").write_text(
        "SKIPPED_NO_BED: no music bed without Chief OK; VO-only rough per J1213.\n"
    )

    digest = sha256_file(out_mp4)
    summary = {
        "film": "008_Lightning-Franklin",
        "job": "J1213",
        "version": "rough_v01",
        "mp4": str(out_mp4),
        "sha256": digest,
        "duration_s": probe_dur(out_mp4),
        "rows": len(all_cuts),
        "parts": part_metas,
        "polish_gate_exit": polish.returncode,
        "picture_qa_exit": picture.returncode,
        "music_gate": music_note,
        "j1193": "not landed at assemble; noted",
        "pr_374": "MERGED before assemble",
    }
    (out_dir / "ROUGH_V01_SUMMARY.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(f"FULL JOIN {summary['duration_s']:.2f}s sha={digest}", flush=True)
    return summary


def deliver(summary: dict) -> None:
    """Copy master + manifests to PRECHECK, DESK, UAT, NAS (sha checked)."""
    src = Path(summary["mp4"])
    digest = summary["sha256"]
    targets = []

    PRECHECK.mkdir(parents=True, exist_ok=True)
    DESK.mkdir(parents=True, exist_ok=True)
    for dest_dir in (PRECHECK, DESK):
        dst = dest_dir / src.name
        shutil.copy2(src, dst)
        assert sha256_file(dst) == digest
        shutil.copy2(WORK / "full_join_v01" / "ROUGH_V01_SUMMARY.json", dest_dir / "ROUGH_V01_SUMMARY.json")
        shutil.copy2(WORK / "full_join_v01" / "cuts_rough_v01.json", dest_dir / "cuts_rough_v01.json")
        shutil.copy2(WORK / "full_join_v01" / "contact_rough_v01.jpg", dest_dir / "contact_rough_v01.jpg")
        for name in (
            "polish_gate_rough_v01.json",
            "polish_gate_rough_v01.txt",
            "picture_qa_rough_v01.txt",
            "music_gate_rough_v01.json",
            "music_gate_rough_v01.txt",
        ):
            p = WORK / "full_join_v01" / name
            if p.exists():
                shutil.copy2(p, dest_dir / name)
        targets.append(str(dst))

    if UAT_ROOT.exists():
        uat = UAT_ROOT / "008_Lightning-Franklin_rough_v01"
        uat.mkdir(parents=True, exist_ok=True)
        dst = uat / src.name
        shutil.copy2(src, dst)
        assert sha256_file(dst) == digest
        (uat / "SHA256SUMS.txt").write_text(f"{digest}  {src.name}\n")
        shutil.copy2(WORK / "full_join_v01" / "ROUGH_V01_SUMMARY.json", uat / "ROUGH_V01_SUMMARY.json")
        shutil.copy2(WORK / "full_join_v01" / "contact_rough_v01.jpg", uat / "contact_rough_v01.jpg")
        targets.append(str(dst))

    if NAS_FILM.exists():
        nas = NAS_FILM / "07_Edit-Project" / "rough_v01"
        nas.mkdir(parents=True, exist_ok=True)
        dst = nas / src.name
        sp.run(["rsync", "-a", str(src), str(dst)], check=True)
        assert sha256_file(dst) == digest
        (nas / "SHA256SUMS.txt").write_text(f"{digest}  {src.name}\n")
        shutil.copy2(WORK / "full_join_v01" / "ROUGH_V01_SUMMARY.json", nas / "ROUGH_V01_SUMMARY.json")
        targets.append(str(dst))

    summary["delivered"] = targets
    (WORK / "full_join_v01" / "ROUGH_V01_SUMMARY.json").write_text(json.dumps(summary, indent=2) + "\n")
    (DESK / "DELIVERED.json").write_text(json.dumps({"sha256": digest, "targets": targets}, indent=2) + "\n")
    print("DELIVERED", targets, flush=True)


def main() -> int:
    WORK.mkdir(parents=True, exist_ok=True)
    print("Loading mint index…", flush=True)
    mint = load_mint_index()
    print(f"KEEP Flow clips: {len(mint)}", flush=True)
    print("Preparing code graphics + 5 overlay composites…", flush=True)
    special = prepare_special_assets(mint)
    print(f"Special assets: {len(special)}", flush=True)

    metas = []
    for part in range(1, 6):
        print(f"=== Assemble part {part:02d} ===", flush=True)
        metas.append(assemble_part(part, mint, special))

    print("=== Full join ===", flush=True)
    summary = join_full(metas)
    print("=== Deliver ===", flush=True)
    deliver(summary)
    print("ALL DONE", flush=True)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception:
        traceback.print_exc()
        raise SystemExit(1)
