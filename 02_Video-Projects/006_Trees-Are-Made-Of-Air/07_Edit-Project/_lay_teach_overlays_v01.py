#!/usr/bin/env python3
"""J0351: lay the 21 silent teach overlays onto hos_006_full_join_v01.

VO is copied. No music bed. No mint. The three pairs that share a film clock
are sequenced, not stacked (TEACH_OVERLAYS_v01.md and each row's lay note):

- Stephen Hales, then the Teddington 1727 timeline
- chapter card Bubbles in the Sunlight, then the Near London 1779 timeline
- de Saussure, then the Geneva 1804 timeline

Jean Senebier's card is cut at the de Saussure start so the two lower thirds
do not sit on each other. Saussure stays on its baked plate time.
"""
from __future__ import annotations

import json
import subprocess as sp
import sys
from pathlib import Path

EDIT = Path(__file__).resolve().parent
RENDER = EDIT / "teach_overlays_v01" / "TEACH_OVERLAYS_RENDER_v01.json"
# Media is not in git. The approved copies live on the NAS (sha checked against the render JSON).
# Local copies of the NAS masters (sha matched TEACH_OVERLAYS_RENDER_v01.json / the join sha).
# The share was busy, so the encode reads these and does not re-probe the NAS.
MEDIA = Path("/private/tmp/j0351-lay/media")
JOIN = MEDIA / "hos_006_full_join_v01.mp4"
OV_DIR = MEDIA / "overlays"
OUT = Path("/private/tmp/j0351-lay/hos_006_full_join_v01_teach.mp4")
LAY_JSON = Path("/private/tmp/j0351-lay/LAY_TIMES_v01.json")


def duration(path: Path) -> float:
    return float(sp.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        text=True,
    ).strip())


def schedule(rows: list[dict]) -> list[dict]:
    items = []
    for row in rows:
        path = OV_DIR / row["file"]
        dur = duration(path)
        start = float(row["film_s"])
        items.append({
            "id": row["id"],
            "file": row["file"],
            "path": str(path),
            "layout": row["layout"],
            "lay": row.get("lay") or "",
            "film_s": start,
            "start": start,
            "dur": dur,
            "end": start + dur,
            "note": "",
        })
    by = {i["id"]: i for i in items}

    def move_after(item_id: str, after_id: str, why: str) -> None:
        item = by[item_id]
        item["start"] = by[after_id]["end"]
        item["end"] = item["start"] + item["dur"]
        item["note"] = why

    move_after("timeline_d2", "who_hales", "after the Stephen Hales card; not stacked")
    move_after("timeline_d4", "ch_bubbles", "after Bubbles in the Sunlight; not stacked")
    # Senebier's tail crosses the Saussure start. Keep Saussure on its plate time.
    if by["who_senebier"]["end"] > by["who_saussure"]["start"]:
        by["who_senebier"]["end"] = by["who_saussure"]["start"]
        by["who_senebier"]["note"] = "ends as the de Saussure card starts, so the two cards are not stacked"
    move_after("timeline_d6", "who_saussure", "after the de Saussure card; not stacked")

    ordered = sorted(items, key=lambda i: (i["start"], i["id"]))
    for a, b in zip(ordered, ordered[1:]):
        if b["start"] < a["end"] - 1e-3:
            raise SystemExit(f"still overlapping: {a['id']} [{a['start']:.3f}-{a['end']:.3f}] and {b['id']} [{b['start']:.3f}-{b['end']:.3f}]")
    return ordered


def base_frames() -> int:
    raw = sp.check_output(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=nb_frames",
         "-of", "csv=p=0", str(JOIN)],
        text=True,
    ).strip()
    return int(raw)


def segments(ordered: list[dict], nframes: int) -> list[tuple]:
    """Replace base frames with each overlay. Returns (kind, start_frame, end_frame, item or None)."""
    segs = []
    cursor = 0
    for item in ordered:
        a = int(round(item["start"] * 24))
        b = int(round(item["end"] * 24))
        if a >= nframes:
            break
        if a < cursor:
            a = cursor
        if b <= a:
            raise SystemExit(f"empty window for {item['id']}")
        b = min(b, nframes)
        if a > cursor:
            segs.append(("base", cursor, a, None))
        segs.append(("ov", a, b, item))
        cursor = b
    if cursor < nframes:
        segs.append(("base", cursor, nframes, None))
    total = sum(b - a for _, a, b, _ in segs)
    if total != nframes:
        raise SystemExit(f"segment frames {total} != base {nframes}")
    return segs


def video_duration(path: Path) -> float:
    return float(sp.check_output(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=duration", "-of", "csv=p=0", str(path)],
        text=True,
    ).strip())


def video_frames(path: Path) -> int:
    return int(sp.check_output(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=nb_frames", "-of", "csv=p=0", str(path)],
        text=True,
    ).strip())


def ffmpeg_cmd(ordered: list[dict], out: Path, limit_s: float | None) -> list[str]:
    # split+trim+concat dropped the picture at 296 s (7,110 of 12,187 frames)
    # while the audio ran on. These cards are opaque full frames (the plate is
    # baked in), so one overlay chain with eof_action=pass covers each window
    # and leaves every other base frame in place.
    cmd = ["ffmpeg", "-y", "-v", "error", "-stats", "-i", str(JOIN)]
    for item in ordered:
        cmd += ["-i", item["path"]]
    # PTS-STARTPTS and fps=24 on this join both drop the picture at 4:56
    # (7,112 of 12,187 frames). format= keeps every frame. Cards are shifted
    # onto the join's own timestamps.
    parts = ["[0:v]format=yuv420p[v0]"]
    for i, item in enumerate(ordered):
        start = float(item["start"])
        end = float(item["end"])
        parts.append(
            f"[{i + 1}:v]fps=24,setpts=PTS-STARTPTS+{start:.6f}/TB,format=yuv420p[o{i}]"
        )
        parts.append(
            f"[v{i}][o{i}]overlay=x=0:y=0:eof_action=pass:repeatlast=0:shortest=0:"
            f"enable='between(t,{start:.6f},{end:.6f})'[v{i + 1}]"
        )
    last = f"v{len(ordered)}"
    cmd += ["-filter_complex", ";".join(parts), "-map", f"[{last}]", "-map", "0:a",
            "-c:a", "copy", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
            "-pix_fmt", "yuv420p", "-r", "24"]
    if limit_s:
        cmd += ["-t", f"{limit_s:.3f}"]
    else:
        cmd += ["-movflags", "+faststart"]
    cmd.append(str(out))
    return cmd


def main() -> int:
    if not JOIN.exists():
        raise SystemExit(f"missing join: {JOIN}")
    data = json.loads(RENDER.read_text())
    if len(data["rows"]) != 21:
        raise SystemExit(f"expected 21 rows, got {len(data['rows'])}")
    ordered = schedule(data["rows"])
    OUT.parent.mkdir(parents=True, exist_ok=True)
    LAY_JSON.write_text(json.dumps({
        "job": "J0351",
        "master": str(JOIN),
        "master_sha256": data["master_sha256"],
        "audio": "copy of full_join_v01; no bed",
        "rows": [{k: v for k, v in item.items() if k != "path"} | {"shifted": item["start"] != item["film_s"]} for item in ordered],
    }, indent=2) + "\n")
    for item in ordered:
        mark = " *" if item["note"] else ""
        print(f"{item['id']:16} {item['start']:7.3f}-{item['end']:7.3f}{mark} {item['note']}")
    if "--check" in sys.argv:
        print(f"wrote {LAY_JSON}")
        return 0
    limit = None
    if "--test" in sys.argv:
        limit = 55.0
        out = OUT.with_name("teach_lay_test_55s.mp4")
    else:
        out = OUT
    cmd = ffmpeg_cmd(ordered, out, limit)
    print("encoding", out)
    sp.check_call(cmd)
    vdur = video_duration(out)
    nframes = video_frames(out)
    print("wrote", out, f"video {vdur:.3f}s", f"frames {nframes}")
    if not limit and (vdur < 500 or nframes < 12000):
        raise SystemExit(f"picture is short ({vdur:.1f}s, {nframes} frames); the join is 507.8s / 12187 frames")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
