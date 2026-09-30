#!/usr/bin/env python3
"""HOS 001 S06 — Lister carbolic spray Short punch cut.

Ben 12:30 script B. Frame 0: carbolic spray over the table, moving.
No wounds on screen. Related target _C92tIJCk8A (upload later — not this script).
VO → vo_check → this cut → gate_shorts_open → iCloud → STOP.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
VENV_PY = HERE / "_venv" / "bin" / "python"
if VENV_PY.exists() and Path(sys.executable) != VENV_PY:
    os.execv(str(VENV_PY), [str(VENV_PY), str(Path(__file__).resolve())])

from PIL import Image, ImageDraw, ImageFont  # noqa: E402

REPO = Path("/Users/benjaminoats/YouTube/History Of Science")
PROJ = HERE.parent
PLATES = PROJ / "04_Generated-Clips/part05/raw/v01_fast_probe"
VO_DIR = HERE / "vo_s06"
WORK = HERE / "_work" / "s06_carbolic_spray"
OUT = HERE / "hos_001_s06_carbolic_spray_punch_v01.mp4"
ICLOUD = Path.home() / (
    "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT/"
    "001_How-Did-We-Discover-Germs/10_Shorts"
)
ART = Path.home() / ".local/share/cursor-mac-mini-hos-worker/artifacts"
AGENT = Path.home() / (
    "Library/Application Support/Cursor/AgentStores/"
    "cursor_agent_stores/bc-958ae0f3-be07-568f-a2ab-eb7f422d8839/files/artifacts"
)
GATE = REPO / "00_Brand/Channel-Setup/tools/gate_shorts_open.py"
VO_CHECK = REPO / "00_Brand/Channel-Setup/tools/vo_check.py"
SCRIPT_MD = VO_DIR / "s06_carbolic_spray_script_for_check.md"
VO_WAV = VO_DIR / "hos_001_s06_carbolic_spray_vo_v01.wav"
VO_ALIGN = VO_DIR / "hos_001_s06_carbolic_spray_vo_v01_align.json"

FONT = "/System/Library/Fonts/Supplemental/Didot.ttc"
CTA_FONT = "/System/Library/Fonts/Supplemental/Times New Roman.ttf"
W, H = 1080, 1920
FPS = 30
CREAM = (245, 232, 210, 255)
INK = (28, 26, 28, 255)
YEL = (255, 214, 70, 255)
VF = "scale=1920:1080,crop=608:1080:656:0,scale=1080:1920:flags=lanczos,setsar=1"
EASE = 0.40  # trim Veo ease-in so frame 0 is mid-action spray
BED_VOL = 0.06
AIR_DATE = "2026-10-20"
HOOK = "THE SPRAY"
PARENT = "How Did We Discover Germs?"
CTA = "watch the full film →"

# Prefer spray (no wounds) + protocol + cleaner theatre wins — skip bloody old_theatre
PLATE_SEQ = [
    PLATES / "02_spray_scrub_v01c.mp4",
    PLATES / "03_protocol_v01b.mp4",
    PLATES / "05_theatre_wins_v02.mp4",
    PLATES / "07_a_map_v01.mp4",
]


def probe(p: Path) -> float:
    return float(
        subprocess.check_output(
            [
                "ffprobe", "-v", "error", "-show_entries", "format=duration",
                "-of", "csv=p=0", str(p),
            ],
            text=True,
        ).strip()
    )


def ff(*a: str) -> None:
    subprocess.run(
        ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *a], check=True
    )


def load_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def wrap(text: str, font: ImageFont.FreeTypeFont, max_w: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    cur = ""
    for w in words:
        trial = (cur + " " + w).strip()
        if font.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def words_from_align(align_path: Path) -> list[dict]:
    raw = json.loads(align_path.read_text())
    chars = raw.get("characters") or []
    starts = raw.get("character_start_times_seconds") or []
    ends = raw.get("character_end_times_seconds") or []
    if not chars:
        return []
    words: list[dict] = []
    buf = ""
    w_start = None
    w_end = None
    for ch, s, e in zip(chars, starts, ends):
        if ch.isspace():
            if buf:
                words.append({"w": buf, "start": w_start, "end": w_end})
                buf = ""
                w_start = w_end = None
            continue
        if w_start is None:
            w_start = float(s)
        w_end = float(e)
        buf += ch
    if buf:
        words.append({"w": buf, "start": w_start, "end": w_end})
    return words


def chunk_words(words: list[dict]) -> list[dict]:
    if not words:
        return []
    chunks = []
    i = 0
    while i < len(words):
        start = words[i]["start"]
        j = i
        while j < len(words):
            dur = words[j]["end"] - start
            n = j - i + 1
            if n > 1 and (dur > 1.55 or n > 5):
                break
            j += 1
        end = words[j - 1]["end"]
        if end - start < 0.45 and j < len(words):
            j = min(len(words), j + 1)
            end = words[j - 1]["end"]
        text = " ".join(w["w"] for w in words[i:j])
        chunks.append({"text": text, "start": start, "end": end})
        i = j
    return chunks


def draw_caption(text: str, *, hook: bool = False) -> Path:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    font = load_font(FONT, 64 if not hook else 78)
    lines = wrap(text, font, int(W * 0.86))
    y = int(H * 0.72)
    for line in lines:
        tw = int(font.getlength(line))
        x = (W - tw) // 2
        fill = YEL if hook else CREAM
        for dx, dy in ((3, 3), (2, 2), (1, 1)):
            d.text((x + dx, y + dy), line, font=font, fill=INK)
        d.text((x, y), line, font=font, fill=fill)
        y += int(font.size * 1.15)
    path = WORK / "caps" / f"cap_{abs(hash(text)) % 10_000_000}.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path)
    return path


def build_picture(target_dur: float) -> Path:
    WORK.mkdir(parents=True, exist_ok=True)
    parts = []
    # Open: spray mid-action (skip ease-in), loop if needed for first ~4s uniqueness later via gate
    open_src = PLATE_SEQ[0]
    open_trim = max(0.0, EASE)
    open_use = min(probe(open_src) - open_trim, 7.2)
    open_out = WORK / "open.mp4"
    ff(
        "-ss", str(open_trim), "-i", str(open_src), "-t", str(open_use),
        "-vf", VF, "-an", "-r", str(FPS), "-pix_fmt", "yuv420p", str(open_out),
    )
    parts.append(open_out)
    filled = probe(open_out)
    pi = 1
    while filled < target_dur + 0.3 and pi < len(PLATE_SEQ) * 3:
        src = PLATE_SEQ[1 + ((pi - 1) % (len(PLATE_SEQ) - 1))]
        need = min(probe(src) - 0.15, target_dur - filled + 0.5)
        if need < 0.4:
            break
        out = WORK / f"seg_{pi:02d}.mp4"
        ff(
            "-ss", "0.15", "-i", str(src), "-t", str(need),
            "-vf", VF, "-an", "-r", str(FPS), "-pix_fmt", "yuv420p", str(out),
        )
        parts.append(out)
        filled += probe(out)
        pi += 1
    # Loop open onto end (last ~4s = first ~4s) for Shorts loop
    loop_t = min(4.0, probe(open_out))
    loop_out = WORK / "loop_tail.mp4"
    ff(
        "-i", str(open_out), "-t", str(loop_t),
        "-c", "copy", str(loop_out),
    )
    # Concat story then trim to target, then append loop
    lst = WORK / "concat_story.txt"
    lst.write_text("".join(f"file '{p}'\n" for p in parts))
    story = WORK / "story.mp4"
    ff("-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(story))
    story_trim = WORK / "story_trim.mp4"
    ff("-i", str(story), "-t", str(max(0.5, target_dur - loop_t)), "-c", "copy", str(story_trim))
    lst2 = WORK / "concat_all.txt"
    lst2.write_text(f"file '{story_trim}'\nfile '{loop_out}'\n")
    pic = WORK / "picture.mp4"
    ff("-f", "concat", "-safe", "0", "-i", str(lst2), "-c", "copy", str(pic))
    # Final hard trim to target_dur
    pic2 = WORK / "picture_final.mp4"
    ff("-i", str(pic), "-t", str(target_dur), "-c", "copy", str(pic2))
    return pic2


def overlay_captions(pic: Path, chunks: list[dict], dur: float) -> Path:
    # Hook 0.12 → first chunk; parent 9–14; CTA last 4s
    overlays = []
    # hook
    hook_png = draw_caption(HOOK, hook=True)
    overlays.append((hook_png, 0.12, min(2.2, dur - 0.2)))
    for ch in chunks:
        if ch["end"] <= 0.2:
            continue
        png = draw_caption(ch["text"])
        overlays.append((png, max(0.12, ch["start"]), min(dur - 0.05, ch["end"] + 0.08)))
    # parent title card
    if dur > 14:
        parent_png = draw_caption(PARENT)
        overlays.append((parent_png, 9.0, 14.0))
    # CTA
    cta_png = draw_caption(CTA)
    overlays.append((cta_png, max(0.5, dur - 4.0), dur - 0.05))

    # Build filter
    inputs = ["-i", str(pic)]
    filter_parts = []
    last = "[0:v]"
    for i, (png, start, end) in enumerate(overlays):
        inputs += ["-i", str(png)]
        out = f"[v{i}]"
        filter_parts.append(
            f"{last}[{i+1}:v]overlay=0:0:enable='between(t,{start:.3f},{end:.3f})'{out}"
        )
        last = out
    filt = ";".join(filter_parts) if filter_parts else None
    out = WORK / "pic_caps.mp4"
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *inputs]
    if filt:
        cmd += ["-filter_complex", filt, "-map", last]
    else:
        cmd += ["-map", "0:v"]
    cmd += ["-an", "-r", str(FPS), "-pix_fmt", "yuv420p", str(out)]
    subprocess.run(cmd, check=True)
    return out


def mux(pic: Path, vo: Path, dur: float) -> Path:
    out = OUT
    # Quiet bed optional — skip if missing
    ff(
        "-i", str(pic), "-i", str(vo),
        "-filter_complex",
        f"[1:a]apad=whole_dur={dur:.3f},atrim=0:{dur:.3f},volume=1.0[a]",
        "-map", "0:v", "-map", "[a]",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        "-t", str(dur), "-r", str(FPS), "-pix_fmt", "yuv420p",
        "-movflags", "+faststart", str(out),
    )
    return out


def caption_sheet(chunks: list[dict], dur: float) -> Path:
    lines = [
        f"# S06 The carbolic spray — caption sheet",
        f"",
        f"- Title: The spray that stopped surgery killing patients",
        f"- Hook: {HOOK}",
        f"- Duration: {dur:.2f}s",
        f"- Air: Tue 20 Oct 2026 11:30",
        f"- Related (when upload): `_C92tIJCk8A`",
        f"- Frame 0: carbolic spray over table (moving). No wounds.",
        f"",
        f"## Captions",
        f"",
    ]
    lines.append(f"| t | text |")
    lines.append(f"|---|---|")
    lines.append(f"| 0.12 | {HOOK} |")
    for ch in chunks:
        lines.append(f"| {ch['start']:.2f}–{ch['end']:.2f} | {ch['text']} |")
    lines.append(f"| 9.00–14.00 | {PARENT} |")
    lines.append(f"| {max(0, dur-4):.2f}–{dur:.2f} | {CTA} |")
    path = VO_DIR / "s06_carbolic_spray_caption_sheet_v01.md"
    path.write_text("\n".join(lines) + "\n")
    return path


def main() -> int:
    if not VO_WAV.exists():
        raise SystemExit(f"STOP: missing VO {VO_WAV} — generate VO first")
    WORK.mkdir(parents=True, exist_ok=True)
    # vo_check
    print("vo_check…", flush=True)
    vc = subprocess.run(
        [
            "python3", str(VO_CHECK), str(VO_WAV),
            "--script", str(SCRIPT_MD), "--part", "1", "--json",
        ],
        capture_output=True,
        text=True,
    )
    (WORK / "vo_check.json").write_text(vc.stdout or vc.stderr or "")
    print(vc.stdout[:800] if vc.stdout else vc.stderr[:800], flush=True)
    if vc.returncode != 0:
        raise SystemExit(f"vo_check FAIL rc={vc.returncode}")

    dur = probe(VO_WAV)
    print(f"VO dur={dur:.3f}s", flush=True)
    if dur < 22.0:
        raise SystemExit(f"STOP: VO {dur:.2f}s < 22s — add a short line and re-gen")
    if dur > 27.5:
        print(f"WARN VO {dur:.2f}s > 27s", flush=True)

    words = words_from_align(VO_ALIGN) if VO_ALIGN.exists() else []
    chunks = chunk_words(words)
    sheet = caption_sheet(chunks, dur)
    print("caption_sheet", sheet, flush=True)

    pic = build_picture(dur)
    print("picture", pic, "dur", probe(pic), flush=True)
    capped = overlay_captions(pic, chunks, dur)
    final = mux(capped, VO_WAV, dur)
    print("OUT", final, "dur", probe(final), flush=True)

    print("gate…", flush=True)
    g = subprocess.run(
        ["python3", str(GATE), "check", str(final), "--air-date", AIR_DATE],
        capture_output=True,
        text=True,
    )
    print(g.stdout or g.stderr, flush=True)
    (WORK / "gate.txt").write_text((g.stdout or "") + (g.stderr or ""))
    if g.returncode != 0:
        raise SystemExit(f"gate FAIL rc={g.returncode}")

    ICLOUD.mkdir(parents=True, exist_ok=True)
    import shutil

    for dest_dir in (ICLOUD, ART, AGENT):
        dest_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(final, dest_dir / final.name)
        shutil.copy2(sheet, dest_dir / sheet.name)
    shutil.copy2(final, ART / "BEN_1230_hos_001_s06_carbolic_spray_punch_v01.mp4")
    shutil.copy2(sheet, ART / "BEN_1230_s06_carbolic_spray_caption_sheet_v01.md")
    shutil.copy2(final, AGENT / "BEN_1230_hos_001_s06_carbolic_spray_punch_v01.mp4")

    # Frame 0 still for Ben
    f0 = ART / "BEN_1230_s06_frame0.jpg"
    ff("-i", str(final), "-frames:v", "1", str(f0))
    shutil.copy2(f0, AGENT / f0.name)

    meta = {
        "ok": True,
        "out": str(final),
        "duration_s": probe(final),
        "air_date": AIR_DATE,
        "title": "The spray that stopped surgery killing patients",
        "related": "_C92tIJCk8A",
        "upload": False,
        "caption_sheet": str(sheet),
        "gate": "PASS",
    }
    (WORK / "BUILD.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
