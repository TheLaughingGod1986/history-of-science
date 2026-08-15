#!/usr/bin/env python3
"""YouTube / social delivery encode — constant frame rate H.264.

Orbit Shorts were shipping with Apple `h264_videotoolbox` plus `-r 30` and no
`fps` filter. That encoder writes irregular timestamps (VFR). YouTube, TikTok
and Instagram then transcode the picture with dropped/duplicated frames while
AAC audio plays smoothly — the lag viewers commented on.

Delivery masters must be:
  - libx264 (software), never VideoToolbox / NVENC / QSV for upload files
  - constant frame rate (`fps=` filter + `-fps_mode cfr` + x264 force-cfr)
  - yuv420p High@4.1
  - +faststart

Audio is copied when it is already AAC 48 kHz stereo so VO/mix is unchanged.
"""
from __future__ import annotations

import json
import shutil
import subprocess
from fractions import Fraction
from pathlib import Path
from typing import Any

DELIVERY_FPS = 30
STANDARD_RATES = (
    Fraction(24, 1),
    Fraction(25, 1),
    Fraction(30, 1),
    Fraction(50, 1),
    Fraction(60, 1),
    Fraction(24000, 1001),
    Fraction(30000, 1001),
)
VIDEOTOOLBOX_MARKERS = ("videotoolbox", "h264_videotoolbox", "hevc_videotoolbox")


def parse_rate(value: str | None) -> Fraction | None:
    if not value or value in {"0/0", "N/A"}:
        return None
    try:
        return Fraction(value)
    except (ZeroDivisionError, ValueError):
        return None


def rate_to_ffmpeg(rate: Fraction) -> str:
    if rate.denominator == 1:
        return str(rate.numerator)
    return f"{rate.numerator}/{rate.denominator}"


def choose_delivery_fps(
    r_frame_rate: str | None,
    avg_frame_rate: str | None,
    *,
    vertical: bool = False,
) -> Fraction:
    """Keep a standard CFR rate when the source already has one; else 30.

    Shorts always deliver at 30 fps (platform convention). Long-form keeps
    24/25/30/60 when that is already the declared rate so we do not introduce
    pulldown judder on cinematic masters.
    """
    if vertical:
        return Fraction(DELIVERY_FPS, 1)
    declared = parse_rate(r_frame_rate) or parse_rate(avg_frame_rate)
    if declared is not None:
        for standard in STANDARD_RATES:
            if abs(float(declared) - float(standard)) < 0.08:
                return standard
    return Fraction(DELIVERY_FPS, 1)


def is_variable_frame_rate(
    r_frame_rate: str | None,
    avg_frame_rate: str | None,
    *,
    tolerance: float = 0.08,
) -> bool:
    r = parse_rate(r_frame_rate)
    avg = parse_rate(avg_frame_rate)
    if r is None or avg is None or float(r) <= 0 or float(avg) <= 0:
        return True
    return abs(float(r) - float(avg)) > tolerance


def encoder_is_videotoolbox(tags: dict[str, Any] | None, encoder_name: str | None = None) -> bool:
    blob = " ".join(
        str(x).lower()
        for x in (
            (tags or {}).get("encoder"),
            (tags or {}).get("ENCODER"),
            encoder_name,
        )
        if x
    )
    return any(marker in blob for marker in VIDEOTOOLBOX_MARKERS)


def fps_mode_args() -> list[str]:
    """ffmpeg 5+ flag; 6.1 in CI understands this."""
    return ["-fps_mode", "cfr"]


def x264_cfr_params(fps: Fraction) -> str:
    keyint = max(24, int(round(float(fps) * 2)))
    return f"keyint={keyint}:min-keyint={keyint}:scenecut=0:force-cfr=1"


def video_timescale(fps: Fraction) -> int:
    if fps.denominator == 1:
        return int(fps.numerator) * 1000
    return int(fps.numerator)


def libx264_cfr_video_args(fps: Fraction) -> list[str]:
    return [
        *fps_mode_args(),
        "-r",
        rate_to_ffmpeg(fps),
        "-c:v",
        "libx264",
        "-preset",
        "medium",
        "-crf",
        "18",
        "-profile:v",
        "high",
        "-level",
        "4.1",
        "-pix_fmt",
        "yuv420p",
        "-x264-params",
        x264_cfr_params(fps),
        "-video_track_timescale",
        str(video_timescale(fps)),
        "-movflags",
        "+faststart",
    ]


def shorts_encode_args(*, fps: int = DELIVERY_FPS) -> list[str]:
    """Drop-in replacement for the old VideoToolbox + `-r 30` block."""
    rate = Fraction(fps, 1)
    return [
        *libx264_cfr_video_args(rate),
        "-c:a",
        "aac",
        "-b:a",
        "256k",
        "-ar",
        "48000",
        "-ac",
        "2",
    ]


def cfr_filter_tail(fps: Fraction = Fraction(DELIVERY_FPS, 1)) -> str:
    return f"fps={rate_to_ffmpeg(fps)},format=yuv420p,setsar=1"


def probe_json(path: Path) -> dict[str, Any]:
    if not shutil.which("ffprobe"):
        raise RuntimeError("ffprobe is required")
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration,size,bit_rate:"
            "stream=index,codec_type,codec_name,width,height,"
            "avg_frame_rate,r_frame_rate,nb_frames,duration,pix_fmt,profile,"
            "sample_rate,channels:"
            "stream_tags=encoder",
            "-of",
            "json",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def _stream(data: dict[str, Any], kind: str) -> dict[str, Any] | None:
    for stream in data.get("streams") or []:
        if stream.get("codec_type") == kind:
            return stream
    return None


def assess_playback_health(
    data: dict[str, Any],
    *,
    vertical: bool | None = None,
) -> dict[str, Any]:
    """Pure function so unit tests can feed fixture JSON (no ffmpeg required)."""
    video = _stream(data, "video")
    audio = _stream(data, "audio")
    errors: list[str] = []
    warnings: list[str] = []
    if video is None:
        errors.append("No video stream")
        return {
            "ok": False,
            "variable_frame_rate": True,
            "videotoolbox": False,
            "errors": errors,
            "warnings": warnings,
        }

    width = int(video.get("width") or 0)
    height = int(video.get("height") or 0)
    is_vertical = bool(vertical) if vertical is not None else (height > width > 0)
    r_rate = video.get("r_frame_rate")
    avg_rate = video.get("avg_frame_rate")
    vfr = is_variable_frame_rate(r_rate, avg_rate)
    toolbox = encoder_is_videotoolbox(video.get("tags"), video.get("codec_name"))
    pix = (video.get("pix_fmt") or "").lower()
    encoder = (video.get("tags") or {}).get("encoder") or video.get("codec_name")

    if vfr:
        errors.append(
            f"Variable frame rate (r={r_rate} avg={avg_rate}). "
            "YouTube/TikTok/IG transcode this as stuttery video with smooth audio."
        )
    if toolbox:
        errors.append(
            f"Hardware encoder {encoder!r} is not safe for social upload. Use libx264 CFR."
        )
    if pix and pix not in {"yuv420p", "yuvj420p"}:
        errors.append(f"Pixel format {pix} is not yuv420p (platforms glitch on 422/444).")
    if video.get("codec_name") not in {None, "h264"}:
        warnings.append(f"Video codec is {video.get('codec_name')}, expected h264")

    v_dur = float(video.get("duration") or 0) or None
    a_dur = float(audio.get("duration") or 0) if audio else None
    if v_dur and a_dur and abs(v_dur - a_dur) > 0.12:
        warnings.append(f"Audio/video duration drift: video={v_dur:.3f}s audio={a_dur:.3f}s")

    fps = choose_delivery_fps(r_rate, avg_rate, vertical=is_vertical)
    return {
        "ok": not errors,
        "variable_frame_rate": vfr,
        "videotoolbox": toolbox,
        "r_frame_rate": r_rate,
        "avg_frame_rate": avg_rate,
        "pix_fmt": pix or None,
        "encoder": encoder,
        "width": width or None,
        "height": height or None,
        "vertical": is_vertical,
        "delivery_fps": rate_to_ffmpeg(fps),
        "has_audio": audio is not None,
        "audio_codec": audio.get("codec_name") if audio else None,
        "audio_rate": int(audio["sample_rate"]) if audio and audio.get("sample_rate") else None,
        "audio_channels": audio.get("channels") if audio else None,
        "video_duration": v_dur,
        "audio_duration": a_dur,
        "errors": errors,
        "warnings": warnings,
    }


def assess_file(path: Path) -> dict[str, Any]:
    health = assess_playback_health(probe_json(path))
    health["path"] = str(path)
    return health


def _can_copy_audio(health: dict[str, Any]) -> bool:
    return (
        bool(health.get("has_audio"))
        and health.get("audio_codec") == "aac"
        and health.get("audio_rate") in {44100, 48000}
        and int(health.get("audio_channels") or 0) in {1, 2}
    )


def remaster_cfr(
    src: Path,
    dest: Path,
    *,
    fps: Fraction | None = None,
    copy_audio: bool | None = None,
) -> dict[str, Any]:
    """Re-encode picture to strict CFR. Audio is copied when already AAC.

    Duration is taken from the source so a YouTube Studio *Replace* keeps
    the same timeline (views, comments, URL stay on the original video id).
    """
    if not shutil.which("ffmpeg"):
        raise RuntimeError("ffmpeg is required")
    src = Path(src)
    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    health = assess_file(src)
    rate = fps or Fraction(health["delivery_fps"])
    keep_audio = _can_copy_audio(health) if copy_audio is None else copy_audio

    vf = cfr_filter_tail(rate)
    cmd = [
        "ffmpeg",
        "-y",
        "-hide_banner",
        "-loglevel",
        "error",
        "-i",
        str(src),
        "-map",
        "0:v:0",
        "-vf",
        vf,
        *libx264_cfr_video_args(rate),
    ]
    if health.get("has_audio"):
        cmd += ["-map", "0:a:0"]
        if keep_audio:
            cmd += ["-c:a", "copy"]
        else:
            cmd += ["-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2"]
    else:
        cmd += ["-an"]

    tmp = dest.with_suffix(dest.suffix + ".tmp.mp4")
    cmd.append(str(tmp))
    subprocess.run(cmd, check=True)
    tmp.replace(dest)
    after = assess_file(dest)
    return {"source": health, "output": after, "copied_audio": bool(keep_audio and health.get("has_audio"))}


def needs_remaster(health: dict[str, Any]) -> bool:
    return not health.get("ok")
