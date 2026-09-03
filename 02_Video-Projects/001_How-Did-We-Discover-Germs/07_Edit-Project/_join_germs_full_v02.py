#!/usr/bin/env python3
"""Join LOCKED Parts 01–05 → v02. Concat only. No remint. Not LOCKED.

Unlocks (Ben, 2 Sep 2026):
  1) 02→03: finish clipped 02 clause, 0.4s breath, 10f dissolve, 03 VO after.
  2) End: last 05 sentence + 0.4s breath, hold last picture, 16f dissolve,
     card ~2s, fade words ~1.75s, short empty brown.
  3) Audio only: kill the <1ms scratch at ~47.155 inside locked Part 01.
Other splices stay hard cuts. Do not recut 01–05 picture.
"""
from __future__ import annotations

import hashlib
import json
import struct
import subprocess
import tempfile
import wave
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
EXP = PROJ / "09_Final-Export"
ICLOUD = Path(
    "/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/HOS UAT"
)
ALIGN05 = PROJ / "02_Voiceover/part05_clean_hands_v01_align.json"
VO02 = PROJ / "02_Voiceover/part02_seeing_tiny_world_v01.mp3"
BED02 = PROJ / "05_Music/hos_001_part02_ominous_ward_v09_norm.wav"
SWIFT = PROJ / "07_Edit-Project/_render_hos_end_card.swift"
OUT = EXP / "hos_001_germs_full_v02.mp4"

DISSOLVE = 10 / 24
END_DISSOLVE = 16 / 24
BREATH = 0.40
P02_CLAUSE_END = 78.92
VO_SCALE = 0.698
BED_SCALE = 0.105
CARD_HOLD = 2.00
WORD_FADE = 1.75
BROWN_HOLD = 0.70
CLICK_A = 47.152
CLICK_B = 47.160
SR = 48000

LOCK = [
    {
        "id": "01",
        "name": "hos_001_part01_rough_v21.mp4",
        "sha": "23f7f002255f913f4e1509b8ac6167248830bb1cb5105986c7b8f171814053b5",
    },
    {
        "id": "02",
        "name": "hos_001_part02_rough_v12.mp4",
        "sha": "b82cb96383ab7233d312087309aa455fe999a0e8609a7dfe3389ab178dd03f27",
    },
    {
        "id": "03",
        "name": "hos_001_part03_rough_v14.mp4",
        "sha": "a007e1330e85556ab8912f5b5a57f6bb8a69f2ba4ebdce44cb20e4071d9a8428",
    },
    {
        "id": "04",
        "name": "hos_001_part04_rough_v23.mp4",
        "sha": "afe44645ddcfbc649baca52a7720e083d48125d5fd6ca32606b3fb2c951fe763",
    },
    {
        "id": "05",
        "name": "hos_001_part05_rough_v03.mp4",
        "sha": "7aec17d498f65aaa3312f0d8f04e4411fa5debeff5eb646b5effa61d3f54e194",
    },
]

ENC = [
    "-c:v", "libx264", "-pix_fmt", "yuv420p",
    "-profile:v", "baseline", "-level", "3.1", "-bf", "0",
    "-preset", "fast", "-crf", "18",
    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
    "-movflags", "+faststart", "-brand", "mp42",
]


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def probe_dur(p: Path) -> float:
    r = subprocess.run(
        [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(p),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(r.stdout.strip())


def last_phoneme_05() -> float:
    a = json.loads(ALIGN05.read_text())
    chars = a["characters"]
    ends = a["character_end_times_seconds"]
    for i in range(len(chars) - 1, -1, -1):
        if chars[i].strip():
            return float(ends[i])
    raise SystemExit("STOP: no last phoneme in Part 05 align")


def ff(*args: str) -> None:
    subprocess.run(["ffmpeg", "-y", *args], check=True)


def wav_to_list(p: Path) -> tuple[int, int, list[tuple[int, int]]]:
    with wave.open(str(p), "rb") as w:
        ch, sw, sr, n = w.getnchannels(), w.getsampwidth(), w.getframerate(), w.getnframes()
        if sw != 2 or sr != SR or ch != 2:
            raise SystemExit(f"STOP: wav {p} must be 48k stereo s16 ({ch}/{sw}/{sr})")
        raw = w.readframes(n)
    frames = list(struct.iter_unpack("<hh", raw))
    return sr, n, frames


def list_to_wav(p: Path, frames: list[tuple[int, int]]) -> None:
    with wave.open(str(p), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(b"".join(struct.pack("<hh", *fr) for fr in frames))


def declick_p01(src_wav: Path, dest: Path) -> tuple[float, int, int]:
    sr, n, frames = wav_to_list(src_wav)
    a = int(round(CLICK_A * sr))
    b = int(round(CLICK_B * sr))
    if a < 2 or b >= n - 2 or b <= a:
        raise SystemExit("STOP: click window out of range")
    before = max(abs(frames[i][0]) for i in range(a - 48, a))
    peak = max(abs(frames[i][0]) for i in range(a, b))
    L0, R0 = frames[a - 1]
    L1, R1 = frames[b]
    span = b - a
    out = frames[:]
    for i in range(span):
        t = (i + 1) / (span + 1)
        out[a + i] = (
            int(L0 + (L1 - L0) * t),
            int(R0 + (R1 - R0) * t),
        )
    after = max(abs(out[i][0]) for i in range(a, b))
    list_to_wav(dest, out)
    print(
        f"DECLICK {CLICK_A:.3f}-{CLICK_B:.3f} peak {peak} → {after} "
        f"(pre {before})",
        flush=True,
    )
    if after > 900:
        raise SystemExit(f"STOP: click still hot after interpolate ({after})")
    return CLICK_A, peak, after


def encode_seg(path: Path, extra: list[str]) -> None:
    ff(*extra, *ENC, str(path))


def main() -> None:
    paths: list[Path] = []
    durs: list[float] = []
    print("HASH CHECK", flush=True)
    for item in LOCK:
        exp = EXP / item["name"]
        if not exp.exists():
            raise SystemExit(f"STOP: missing {exp}")
        got = sha256(exp)
        if got != item["sha"]:
            raise SystemExit(f"STOP: hash mismatch {item['name']} {got}")
        print(f"  OK {item['id']} {got} {exp.stat().st_size}", flush=True)
        paths.append(exp)
        durs.append(probe_dur(exp))

    p05_last = last_phoneme_05()
    p02_file = durs[1]
    if P02_CLAUSE_END <= p02_file:
        raise SystemExit("STOP: clause end is inside locked 02 — check measure")
    p02_until_breath = P02_CLAUSE_END + BREATH
    p02_hold = p02_until_breath - p02_file
    p02_ext = p02_until_breath + DISSOLVE
    p05_until_breath = p05_last + BREATH
    p05_ext = p05_until_breath + END_DISSOLVE
    print(
        f"P02 file={p02_file:.3f} clause={P02_CLAUSE_END:.3f} "
        f"breath+hold={p02_until_breath:.3f} ext={p02_ext:.3f} hold={p02_hold:.3f}",
        flush=True,
    )
    print(
        f"P05 last={p05_last:.3f} breath={p05_until_breath:.3f} "
        f"ext={p05_ext:.3f} file={durs[4]:.3f}",
        flush=True,
    )

    work = Path(tempfile.mkdtemp(prefix="hos_join_v02_"))
    print(f"WORK {work}", flush=True)

    p01_wav = work / "p01.wav"
    p01_clean = work / "p01_clean.wav"
    ff("-i", str(paths[0]), "-vn", "-ac", "2", "-ar", "48000", "-c:a", "pcm_s16le", str(p01_wav))
    declick_p01(p01_wav, p01_clean)

    p01s = work / "p01.mp4"
    encode_seg(
        p01s,
        ["-i", str(paths[0]), "-i", str(p01_clean), "-map", "0:v", "-map", "1:a",
         "-t", f"{durs[0]:.6f}"],
    )

    p02_wav = work / "p02.wav"
    vo_rest = work / "vo02_rest.wav"
    bed_rest = work / "bed02_rest.wav"
    tail = work / "p02_tail.wav"
    p02_ext_wav = work / "p02_ext.wav"
    ff("-i", str(paths[1]), "-vn", "-ac", "2", "-ar", "48000", "-c:a", "pcm_s16le", str(p02_wav))
    tail_t = p02_ext - p02_file
    ff(
        "-ss", f"{p02_file:.6f}", "-i", str(VO02),
        "-t", f"{P02_CLAUSE_END - p02_file:.6f}",
        "-ac", "2", "-ar", "48000", "-c:a", "pcm_s16le", str(vo_rest),
    )
    ff(
        "-ss", f"{p02_file:.6f}", "-i", str(BED02),
        "-t", f"{tail_t:.6f}",
        "-ac", "2", "-ar", "48000", "-c:a", "pcm_s16le", str(bed_rest),
    )
    vo_len = P02_CLAUSE_END - p02_file
    ff(
        "-i", str(vo_rest), "-i", str(bed_rest),
        "-filter_complex",
        f"[0:a]volume={VO_SCALE:.3f},apad=pad_dur={tail_t:.6f}[vo];"
        f"[1:a]volume={BED_SCALE:.3f}[bed];"
        f"[vo][bed]amix=inputs=2:duration=first:normalize=0,"
        f"afade=t=in:d=0.012,atrim=0:{tail_t:.6f},asetpts=PTS-STARTPTS[a]",
        "-map", "[a]", "-c:a", "pcm_s16le", str(tail),
    )
    ff(
        "-i", str(p02_wav), "-i", str(tail),
        "-filter_complex",
        f"[0:a][1:a]concat=n=2:v=0:a=1,atrim=0:{p02_ext:.6f},asetpts=PTS-STARTPTS[a]",
        "-map", "[a]", "-c:a", "pcm_s16le", str(p02_ext_wav),
    )
    p02s = work / "p02.mp4"
    encode_seg(
        p02s,
        [
            "-i", str(paths[1]), "-i", str(p02_ext_wav),
            "-filter_complex",
            f"[0:v]tpad=stop_mode=clone:stop_duration={p02_ext - p02_file:.6f},"
            f"trim=0:{p02_ext:.6f},setpts=PTS-STARTPTS,fps=24,format=yuv420p,setsar=1[v];"
            f"[1:a]atrim=0:{p02_ext:.6f},asetpts=PTS-STARTPTS[a]",
            "-map", "[v]", "-map", "[a]",
        ],
    )

    p02p03 = work / "p02p03.mp4"
    encode_seg(
        p02p03,
        [
            "-i", str(p02s), "-i", str(paths[2]),
            "-filter_complex",
            f"[0:v]fps=24,format=yuv420p,setsar=1[v0];"
            f"[1:v]fps=24,format=yuv420p,setsar=1[v1];"
            f"[v0][v1]xfade=transition=fade:duration={DISSOLVE:.6f}:"
            f"offset={p02_until_breath:.6f}[v];"
            f"[0:a]atrim=0:{p02_ext:.6f},asetpts=PTS-STARTPTS[a0];"
            f"[1:a]atrim=0:{durs[2] - DISSOLVE:.6f},asetpts=PTS-STARTPTS[a1];"
            f"[a0][a1]concat=n=2:v=0:a=1[a]",
            "-map", "[v]", "-map", "[a]",
        ],
    )

    p04s = work / "p04.mp4"
    encode_seg(p04s, ["-i", str(paths[3]), "-t", f"{durs[3]:.6f}"])

    png = work / "end_card.png"
    brown = work / "brown.png"
    bin_path = Path("/tmp/render_hos_end_card")
    subprocess.run(["swiftc", "-O", "-o", str(bin_path), str(SWIFT)], check=True)
    subprocess.run([str(bin_path), str(png)], check=True)
    ff(
        "-f", "lavfi", "-i", "color=c=0x3D291C:s=1280x720:r=24",
        "-frames:v", "1", str(brown),
    )
    card_after = END_DISSOLVE + CARD_HOLD + WORD_FADE + BROWN_HOLD
    p05_hold = max(0.0, p05_ext - durs[4])
    p05s = work / "p05card.mp4"
    encode_seg(
        p05s,
        [
            "-i", str(paths[4]),
            "-loop", "1", "-t", f"{card_after + 1:.3f}", "-i", str(png),
            "-loop", "1", "-t", f"{WORD_FADE + BROWN_HOLD + 1:.3f}", "-i", str(brown),
            "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
            "-filter_complex",
            f"[0:v]tpad=stop_mode=clone:stop_duration={p05_hold + 0.05:.6f},"
            f"trim=0:{p05_ext:.6f},setpts=PTS-STARTPTS,fps=24,format=yuv420p,setsar=1[v5];"
            f"[1:v]fps=24,format=yuv420p,setsar=1[card];"
            f"[2:v]fps=24,format=yuv420p,setsar=1[br];"
            f"[v5][card]xfade=transition=fade:duration={END_DISSOLVE:.6f}:"
            f"offset={p05_until_breath:.6f}[to_card];"
            f"[to_card][br]xfade=transition=fade:duration={WORD_FADE:.6f}:"
            f"offset={p05_until_breath + END_DISSOLVE + CARD_HOLD:.6f}[v];"
            f"[0:a]atrim=0:{p05_until_breath:.6f},asetpts=PTS-STARTPTS[a5];"
            f"[3:a]atrim=0:{card_after:.6f},asetpts=PTS-STARTPTS[sil];"
            f"[a5][sil]concat=n=2:v=0:a=1[a]",
            "-map", "[v]", "-map", "[a]",
            "-t", f"{p05_until_breath + card_after:.6f}",
        ],
    )

    lst = work / "concat.txt"
    segs = [p01s, p02p03, p04s, p05s]
    lst.write_text("".join(f"file '{p}'\n" for p in segs))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    ff("-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy",
       "-movflags", "+faststart", "-brand", "mp42", str(OUT))

    splice_12 = durs[0]
    splice_23 = splice_12 + p02_until_breath
    splice_23_land = splice_23 + DISSOLVE
    splice_34 = splice_12 + probe_dur(p02p03)
    splice_45 = splice_34 + durs[3]
    card_in = splice_45 + p05_until_breath
    card_land = card_in + END_DISSOLVE
    card_words_out = card_land + CARD_HOLD
    card_brown = card_words_out + WORD_FADE
    card_out = card_brown + BROWN_HOLD

    print(f"SAVED {OUT}", flush=True)
    print(f"SIZE {OUT.stat().st_size}", flush=True)
    print(f"SHA256 {sha256(OUT)}", flush=True)
    print(f"DUR {probe_dur(OUT):.3f}", flush=True)
    print(f"SPLICE_12 {splice_12:.3f}", flush=True)
    print(f"SPLICE_23_DISSOLVE {splice_23:.3f}", flush=True)
    print(f"SPLICE_23_LAND {splice_23_land:.3f}", flush=True)
    print(f"SPLICE_34 {splice_34:.3f}", flush=True)
    print(f"SPLICE_45 {splice_45:.3f}", flush=True)
    print(f"CARD_IN {card_in:.3f}", flush=True)
    print(f"CARD_LAND {card_land:.3f}", flush=True)
    print(f"CARD_HOLD_END {card_words_out:.3f}", flush=True)
    print(f"CARD_BROWN {card_brown:.3f}", flush=True)
    print(f"CARD_OUT {card_out:.3f}", flush=True)
    if ICLOUD.parent.exists():
        ICLOUD.mkdir(parents=True, exist_ok=True)
        subprocess.run(["cp", "-f", str(OUT), str(ICLOUD / OUT.name)], check=False)
        print(f"ICLOUD {ICLOUD / OUT.name}", flush=True)


if __name__ == "__main__":
    main()
