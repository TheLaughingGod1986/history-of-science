#!/usr/bin/env python3
"""HOS 003 full polish v01 — join KEEP Parts 01–05 per HOS_003_FULL_JOIN_BRIEF_v01.

No remint. Soft starfield chapter cards. Soft music outro (no hard silence).
"""
from __future__ import annotations

import hashlib
import json
import math
import random
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

PROJ = Path(__file__).resolve().parents[1]
EXP = PROJ / "09_Final-Export"
EDIT = PROJ / "07_Edit-Project"
WORK = EDIT / "_full_join_v01_work"
CARDS = WORK / "cards"
ICLOUD = (
    Path.home()
    / "Library/Mobile Documents/com~apple~CloudDocs/HOS UAT"
    / "hos_003_full_polish_v01.mp4"
)
OUT = EXP / "hos_003_full_polish_v01.mp4"
META = EDIT / "hos_003_full_polish_v01_land_meta.json"
BED = (
    PROJ.parents[0]
    / "001_How-Did-We-Discover-Germs/05_Music/hos_001_part04_lab_bed_v06.wav"
)
DIDOT = "/System/Library/Fonts/Supplemental/Didot.ttc"
GEORGIA = "/System/Library/Fonts/Supplemental/Georgia.ttf"

BREATH = 1.50
CARD_DUR = 3.60
XFADE = 0.55
OUTRO_HOLD = 18.0
MUSIC_FADE = 10.0
PIC_FADE = 2.0
P05_TRIM = 81.50  # before baked black tail
TITLE_HOLD = 3.40
BED_VOL_CARD = 0.28
BED_VOL_OUTRO = 0.30
FPS = 24

LOCK = [
    {
        "id": "01",
        "name": "hos_003_part01_rough_v03.mp4",
        "sha": "d9d82de54962a36ae86c94a17b34764109d0fa1a1b8a383d9edc21dc3cc9f11a",
        "card_after": None,
    },
    {
        "id": "02",
        "name": "hos_003_part02_rough_v03.mp4",
        "sha": "c95daf407bf336e0bf14b163c341a568a4efa7659644b34d5b503362d623260d",
        "card_after": "The Cardboard",
    },
    {
        "id": "03",
        "name": "hos_003_part03_rough_v02.mp4",
        "sha": "572d498f7b70cd00fc18c68eac1a17c98b4a89b5a6c473772b12fb42053fd262",
        "card_after": "Bones Without a Knife",
    },
    {
        "id": "04",
        "name": "hos_003_part04_rough_v03.mp4",
        "sha": "d2b5946221343cb3012077d44b970f91d6002039c73c06ceb06d2972189b8508",
        "card_after": "Bertha’s Ring",
    },
    {
        "id": "05",
        "name": "hos_003_part05_rough_v02.mp4",
        "sha": "d1db0f31a220fe6d79f083ea6f285a74217b5b3940641ca7b615cf5659821169",
        "card_after": "A New Kind of Seeing",
    },
]
# card_after on item N is the card BETWEEN part N-1 and part N.
# Rewire: cards after P01,P02,P03,P04
CARDS_ORDER = [
    "The Cardboard",
    "Bones Without a Knife",
    "Bertha’s Ring",
    "A New Kind of Seeing",
]

ENC = [
    "-c:v", "libx264", "-pix_fmt", "yuv420p",
    "-profile:v", "high", "-level", "4.0",
    "-preset", "fast", "-crf", "18",
    "-r", str(FPS),
    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
    "-movflags", "+faststart",
]


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def probe(p: Path) -> float:
    return float(
        subprocess.check_output(
            [
                "ffprobe", "-v", "error", "-show_entries", "format=duration",
                "-of", "default=nw=1:nk=1", str(p),
            ],
            text=True,
        ).strip()
    )


def ff(*args: str) -> None:
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *args], check=True)


def font(size: int, italic: bool = True) -> ImageFont.FreeTypeFont:
    try:
        # Didot.ttc index 1 often italic
        return ImageFont.truetype(DIDOT, size, index=1 if italic else 0)
    except OSError:
        return ImageFont.truetype(GEORGIA, size)


def make_starfield(title: str, dest_png: Path, subtitle: str | None = None) -> None:
    w, h = 1920, 1080
    rng = random.Random(hash(title) & 0xFFFFFFFF)
    im = Image.new("RGB", (w, h), (8, 10, 22))
    px = im.load()
    # soft vertical space gradient
    for y in range(h):
        t = y / (h - 1)
        r = int(8 + 18 * t)
        g = int(10 + 12 * (1 - abs(t - 0.45)))
        b = int(22 + 40 * (1 - t) + 20 * t)
        for x in range(0, w, 4):
            px[x, y] = (r, g, b)
            if x + 1 < w:
                px[x + 1, y] = (r, g, b)
            if x + 2 < w:
                px[x + 2, y] = (r, g, b)
            if x + 3 < w:
                px[x + 3, y] = (r, g, b)
    # stars
    for _ in range(420):
        x = rng.randint(0, w - 1)
        y = rng.randint(0, h - 1)
        bright = rng.randint(140, 255)
        size = rng.choice([1, 1, 1, 2])
        for dy in range(size):
            for dx in range(size):
                if x + dx < w and y + dy < h:
                    px[x + dx, y + dy] = (bright, bright, min(255, bright + 20))
    im = im.filter(ImageFilter.GaussianBlur(radius=0.6))
    d = ImageDraw.Draw(im)
    fnt = font(78, italic=True)
    # soft glow under text
    tb = d.textbbox((0, 0), title, font=fnt)
    tw, th = tb[2] - tb[0], tb[3] - tb[1]
    x0 = (w - tw) / 2
    y0 = h * 0.42 if not subtitle else h * 0.38
    for ox, oy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
        d.text((x0 + ox, y0 + oy), title, font=fnt, fill=(210, 220, 255))
    d.text((x0, y0), title, font=fnt, fill=(245, 248, 255))
    if subtitle:
        sf = font(36, italic=True)
        sb = d.textbbox((0, 0), subtitle, font=sf)
        sw = sb[2] - sb[0]
        d.text(((w - sw) / 2, y0 + th + 28), subtitle, font=sf, fill=(180, 190, 220))
    # tiny house mark
    mf = font(22, italic=False)
    mark = "History of Science"
    mb = d.textbbox((0, 0), mark, font=mf)
    d.text(((w - (mb[2] - mb[0])) / 2, h - 70), mark, font=mf, fill=(120, 130, 160))
    dest_png.parent.mkdir(parents=True, exist_ok=True)
    im.save(dest_png, quality=95)


def still_to_mp4(png: Path, dest: Path, dur: float, bed_vol: float) -> None:
    """Loop still + bed under (never silent)."""
    ff(
        "-loop", "1", "-t", f"{dur:.3f}", "-i", str(png),
        "-stream_loop", "-1", "-i", str(BED),
        "-filter_complex",
        f"[0:v]fps={FPS},format=yuv420p,setsar=1[v];"
        f"[1:a]volume={bed_vol},atrim=0:{dur:.3f},asetpts=PTS-STARTPTS,"
        f"afade=t=in:d=0.35,afade=t=out:st={max(0, dur-0.45):.3f}:d=0.45[a]",
        "-map", "[v]", "-map", "[a]",
        "-t", f"{dur:.3f}",
        *ENC,
        str(dest),
    )


def normalize_part(src: Path, dest: Path) -> None:
    ff(
        "-i", str(src),
        "-vf", f"fps={FPS},scale=1920:1080:force_original_aspect_ratio=decrease,"
        "pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,format=yuv420p",
        "-af", "aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo",
        *ENC,
        str(dest),
    )


def burn_open_title(src: Path, dest: Path, title_png: Path) -> None:
    """Strong intro: overlay film title for first TITLE_HOLD seconds, then fade out."""
    fade_st = max(0.0, TITLE_HOLD - 0.7)
    ff(
        "-i", str(src),
        "-i", str(title_png),
        "-filter_complex",
        f"[1:v]format=rgba,fade=t=out:st={fade_st:.3f}:d=0.7:alpha=1[ov];"
        f"[0:v][ov]overlay=0:0:eof_action=pass[v]",
        "-map", "[v]", "-map", "0:a",
        *ENC,
        str(dest),
    )


def freeze_breath(src: Path, dest: Path, dur: float) -> None:
    """Last frame hold + bed under (music continues; no dead silence)."""
    d = probe(src)
    ss = max(0.0, d - 0.05)
    still = dest.with_suffix(".png")
    ff("-ss", f"{ss:.3f}", "-i", str(src), "-frames:v", "1", str(still))
    still_to_mp4(still, dest, dur, BED_VOL_CARD)


def make_outro(src: Path, dest: Path) -> None:
    """Trim black tail, hold last picture OUTRO_HOLD with music fade, picture fade last PIC_FADE."""
    trimmed = WORK / "p05_trimmed.mp4"
    ff("-i", str(src), "-t", f"{P05_TRIM:.3f}", *ENC, str(trimmed))
    still = WORK / "p05_hold.png"
    ff("-ss", f"{P05_TRIM - 0.08:.3f}", "-i", str(trimmed), "-frames:v", "1", str(still))
    hold = WORK / "p05_hold_seg.mp4"
    # hold with bed; music fades over MUSIC_FADE ending at OUTRO_HOLD; picture fades last PIC_FADE
    fade_start = max(0.0, OUTRO_HOLD - MUSIC_FADE)
    pic_fade_st = max(0.0, OUTRO_HOLD - PIC_FADE)
    ff(
        "-loop", "1", "-t", f"{OUTRO_HOLD:.3f}", "-i", str(still),
        "-stream_loop", "-1", "-i", str(BED),
        "-filter_complex",
        f"[0:v]fps={FPS},format=yuv420p,setsar=1,"
        f"fade=t=out:st={pic_fade_st:.3f}:d={PIC_FADE:.3f}[v];"
        f"[1:a]volume={BED_VOL_OUTRO},atrim=0:{OUTRO_HOLD:.3f},asetpts=PTS-STARTPTS,"
        f"afade=t=in:d=0.4,afade=t=out:st={fade_start:.3f}:d={MUSIC_FADE:.3f}[a]",
        "-map", "[v]", "-map", "[a]",
        "-t", f"{OUTRO_HOLD:.3f}",
        *ENC,
        str(hold),
    )
    # soft xfade from trimmed P05 into hold
    da = probe(trimmed)
    offset = max(0.05, da - XFADE)
    ff(
        "-i", str(trimmed),
        "-i", str(hold),
        "-filter_complex",
        f"[0:v][1:v]xfade=transition=fade:duration={XFADE:.3f}:offset={offset:.3f}[v];"
        f"[0:a][1:a]acrossfade=d={XFADE:.3f}[a]",
        "-map", "[v]", "-map", "[a]",
        *ENC,
        str(dest),
    )


def xfade_join(a: Path, b: Path, dest: Path) -> None:
    da = probe(a)
    offset = max(0.05, da - XFADE)
    ff(
        "-i", str(a),
        "-i", str(b),
        "-filter_complex",
        f"[0:v][1:v]xfade=transition=fade:duration={XFADE:.3f}:offset={offset:.3f}[v];"
        f"[0:a][1:a]acrossfade=d={XFADE:.3f}[a]",
        "-map", "[v]", "-map", "[a]",
        *ENC,
        str(dest),
    )


def av_ok(p: Path) -> tuple[float, float]:
    v = float(
        subprocess.check_output(
            [
                "ffprobe", "-v", "error", "-select_streams", "v:0",
                "-show_entries", "stream=duration", "-of", "default=nw=1:nk=1", str(p),
            ],
            text=True,
        ).strip()
        or "nan"
    )
    a = float(
        subprocess.check_output(
            [
                "ffprobe", "-v", "error", "-select_streams", "a:0",
                "-show_entries", "stream=duration", "-of", "default=nw=1:nk=1", str(p),
            ],
            text=True,
        ).strip()
        or "nan"
    )
    return v, a


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    CARDS.mkdir(parents=True, exist_ok=True)
    if not BED.exists():
        raise SystemExit(f"STOP: missing bed {BED}")

    print("HASH CHECK", flush=True)
    parts: list[Path] = []
    for item in LOCK:
        p = EXP / item["name"]
        if not p.exists():
            raise SystemExit(f"STOP: missing {p}")
        got = sha256(p)
        if got != item["sha"]:
            raise SystemExit(f"STOP: hash mismatch {item['name']} got {got}")
        print(f"  OK {item['id']} {got[:12]}… {probe(p):.3f}s", flush=True)
        parts.append(p)

    # normalize
    norms: list[Path] = []
    for item, src in zip(LOCK, parts):
        dest = WORK / f"norm_{item['id']}.mp4"
        print(f"NORM {item['id']}", flush=True)
        normalize_part(src, dest)
        norms.append(dest)

    # open title overlay on P01 (strong — picture under title)
    title_png = CARDS / "open_title.png"
    make_starfield("How Did We Discover X-rays?", title_png)
    # make transparent-ish overlay: use starfield only as soft plate? Better: text-only overlay.
    # Rebuild open title as dark translucent band text for burn-in on live picture.
    w, h = 1920, 1080
    ov = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    # soft vignette bar
    bar = Image.new("RGBA", (w, 220), (6, 8, 18, 150))
    ov.paste(bar, (0, int(h * 0.38)), bar)
    fnt = font(64, italic=True)
    title = "How Did We Discover X-rays?"
    tb = d.textbbox((0, 0), title, font=fnt)
    tw = tb[2] - tb[0]
    d.text(((w - tw) / 2, h * 0.44), title, font=fnt, fill=(245, 248, 255, 255))
    title_ov = CARDS / "open_title_ov.png"
    ov.save(title_ov)
    p01 = WORK / "p01_titled.mp4"
    print("OPEN TITLE burn-in P01", flush=True)
    burn_open_title(norms[0], p01, title_ov)

    # chapter cards
    card_mp4s: list[Path] = []
    for i, title in enumerate(CARDS_ORDER):
        png = CARDS / f"card_{i+1:02d}.png"
        mp4 = CARDS / f"card_{i+1:02d}.mp4"
        print(f"CARD {title}", flush=True)
        make_starfield(title, png)
        still_to_mp4(png, mp4, CARD_DUR, BED_VOL_CARD)
        card_mp4s.append(mp4)

    # breaths from each of P01–P04
    breaths: list[Path] = []
    for i in range(4):
        b = WORK / f"breath_{i+1:02d}.mp4"
        src = p01 if i == 0 else norms[i]
        print(f"BREATH after P{i+1:02d}", flush=True)
        freeze_breath(src, b, BREATH)
        breaths.append(b)

    # P05 with soft outro
    p05_out = WORK / "p05_outro.mp4"
    print("OUTRO from P05", flush=True)
    make_outro(norms[4], p05_out)

    # Build segment chain
    segs: list[Path] = [p01]
    for i in range(4):
        segs.append(breaths[i])
        segs.append(card_mp4s[i])
        segs.append(p05_out if i == 3 else norms[i + 1])

    print("SEGS " + " | ".join(s.name for s in segs), flush=True)
    acc = segs[0]
    for idx, nxt in enumerate(segs[1:], start=1):
        dest = WORK / f"acc_{idx:02d}.mp4"
        print(f"XFADE → {dest.name} (+{nxt.name})", flush=True)
        xfade_join(acc, nxt, dest)
        acc = dest

    OUT.parent.mkdir(parents=True, exist_ok=True)
    if OUT.exists():
        OUT.unlink()
    acc.replace(OUT)
    # if replace across FS fails, copy
    if not OUT.exists():
        ff("-i", str(acc), "-c", "copy", str(OUT))

    sh = sha256(OUT)
    dur = probe(OUT)
    v, a = av_ok(OUT)
    if abs(v - a) > 0.35:
        raise SystemExit(f"STOP: A/V mismatch v={v} a={a}")
    # end audio must not be silence
    end_check = subprocess.run(
        [
            "ffmpeg", "-sseof", "-3", "-t", "3", "-i", str(OUT),
            "-af", "volumedetect", "-f", "null", "-",
        ],
        capture_output=True,
        text=True,
    )
    mean_line = [ln for ln in end_check.stderr.splitlines() if "mean_volume" in ln]
    print("END_AUDIO", mean_line[-1] if mean_line else "?", flush=True)
    mean_db = None
    if mean_line:
        try:
            mean_db = float(mean_line[-1].split(":")[-1].replace("dB", "").strip())
        except ValueError:
            mean_db = None
    if mean_db is not None and mean_db < -55:
        raise SystemExit(f"STOP: outro too silent {mean_line}")

    ICLOUD.parent.mkdir(parents=True, exist_ok=True)
    ICLOUD.write_bytes(OUT.read_bytes())

    report = {
        "cut": OUT.name,
        "path": str(OUT),
        "icloud": str(ICLOUD),
        "bytes": OUT.stat().st_size,
        "sha256": sh,
        "duration_s": dur,
        "av": {"v": v, "a": a},
        "brief": "HOS_003_FULL_JOIN_BRIEF_v01.md",
        "parts": [
            {"file": x["name"], "sha256": x["sha"]} for x in LOCK
        ],
        "cards": CARDS_ORDER,
        "breath_s": BREATH,
        "xfade_s": XFADE,
        "outro_hold_s": OUTRO_HOLD,
        "bed": BED.name,
        "ts": datetime.now(timezone.utc).isoformat(),
        "note": "P05 soft spectrum parked; no remint; no Ben ping mid-cut",
    }
    META.write_text(json.dumps(report, indent=2) + "\n")
    land = {
        "project": "HOS 003 Invisible Bones",
        "cut": "full_polish_v01",
        "path": str(OUT),
        "sha256": sh,
        "duration_s": dur,
        "icloud": str(ICLOUD),
        "status": "LANDED — QA → UAT",
        "ts": report["ts"],
    }
    (EDIT / "ASSEMBLE_LAND.json").write_text(json.dumps(land, indent=2) + "\n")
    print(f"LANDED {OUT}", flush=True)
    print(f"SHA256 {sh}", flush=True)
    print(f"DUR {dur:.3f}", flush=True)
    print(f"BYTES {OUT.stat().st_size}", flush=True)
    print(f"ICLOUD {ICLOUD}", flush=True)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
