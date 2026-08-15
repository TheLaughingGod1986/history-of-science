import { execFile } from "child_process";
import { promisify } from "util";
import fs from "fs/promises";

const execFileAsync = promisify(execFile);

const VIDEOTOOLBOX_MARKERS = ["videotoolbox", "h264_videotoolbox", "hevc_videotoolbox"];

export type ProbeResult = {
  ok: boolean;
  errors: string[];
  warnings: string[];
  durationSeconds?: number;
  width?: number;
  height?: number;
  aspectRatio?: string;
  videoCodec?: string;
  audioCodec?: string;
  sizeBytes?: number;
  frameRate?: number;
  rFrameRate?: number;
  avgFrameRate?: number;
  variableFrameRate?: boolean;
  videoToolbox?: boolean;
  pixelFormat?: string;
  encoder?: string;
  hasAudio?: boolean;
};

type ProbeStream = {
  codec_type?: string;
  codec_name?: string;
  width?: number;
  height?: number;
  avg_frame_rate?: string;
  r_frame_rate?: string;
  pix_fmt?: string;
  tags?: { encoder?: string };
};

type ProbeJson = {
  format?: { duration?: string; size?: string };
  streams?: ProbeStream[];
};

export function parseFrameRate(value?: string): number | undefined {
  if (!value || value === "0/0" || !value.includes("/")) return undefined;
  const [a, b] = value.split("/").map(Number);
  if (!b) return undefined;
  const n = a / b;
  return Number.isFinite(n) && n > 0 ? n : undefined;
}

export function isVariableFrameRate(rFrameRate?: string, avgFrameRate?: string, tolerance = 0.08): boolean {
  const r = parseFrameRate(rFrameRate);
  const avg = parseFrameRate(avgFrameRate);
  if (r == null || avg == null) return true;
  return Math.abs(r - avg) > tolerance;
}

export function encoderIsVideoToolbox(encoder?: string, codecName?: string): boolean {
  const blob = `${encoder || ""} ${codecName || ""}`.toLowerCase();
  return VIDEOTOOLBOX_MARKERS.some((m) => blob.includes(m));
}

export function assessPlaybackHealth(data: ProbeJson): {
  errors: string[];
  warnings: string[];
  video?: ProbeStream;
  audio?: ProbeStream;
  variableFrameRate: boolean;
  videoToolbox: boolean;
  frameRate?: number;
  rFrameRate?: number;
  avgFrameRate?: number;
  pixelFormat?: string;
  encoder?: string;
} {
  const errors: string[] = [];
  const warnings: string[] = [];
  const video = data.streams?.find((s) => s.codec_type === "video");
  const audio = data.streams?.find((s) => s.codec_type === "audio");
  const rFrameRate = parseFrameRate(video?.r_frame_rate);
  const avgFrameRate = parseFrameRate(video?.avg_frame_rate);
  const encoder = video?.tags?.encoder || video?.codec_name;
  const vfr = isVariableFrameRate(video?.r_frame_rate, video?.avg_frame_rate);
  const toolbox = encoderIsVideoToolbox(video?.tags?.encoder, video?.codec_name);
  const pix = (video?.pix_fmt || "").toLowerCase();

  if (!video) errors.push("No video stream");
  if (vfr && video) {
    errors.push(
      `Variable frame rate (r=${video.r_frame_rate} avg=${video.avg_frame_rate}). ` +
        "YouTube/TikTok/IG transcode this as stuttery video with smooth audio.",
    );
  }
  if (toolbox) {
    errors.push(`Hardware encoder ${encoder} is not safe for social upload. Use libx264 CFR.`);
  }
  if (pix && pix !== "yuv420p" && pix !== "yuvj420p") {
    errors.push(`Pixel format ${pix} is not yuv420p (platforms glitch on 422/444).`);
  }
  if (!audio) warnings.push("No audio track detected");

  return {
    errors,
    warnings,
    video,
    audio,
    variableFrameRate: vfr,
    videoToolbox: toolbox,
    frameRate: avgFrameRate ?? rFrameRate,
    rFrameRate,
    avgFrameRate,
    pixelFormat: pix || undefined,
    encoder,
  };
}

export async function probeVideo(filePath: string): Promise<ProbeResult> {
  try {
    const stat = await fs.stat(filePath);
    if (stat.size === 0) {
      return { ok: false, errors: ["Video file is zero bytes"], warnings: [], sizeBytes: 0 };
    }
  } catch {
    return { ok: false, errors: [`Video file missing or unreadable: ${filePath}`], warnings: [] };
  }

  try {
    const { stdout } = await execFileAsync(
      "ffprobe",
      [
        "-v",
        "error",
        "-show_entries",
        "format=duration,size:stream=codec_type,codec_name,width,height,avg_frame_rate,r_frame_rate,pix_fmt:stream_tags=encoder",
        "-of",
        "json",
        filePath,
      ],
      { timeout: 30_000 },
    );
    const data = JSON.parse(stdout) as ProbeJson;
    const health = assessPlaybackHealth(data);
    const durationSeconds = data.format?.duration ? Number(data.format.duration) : undefined;
    const width = health.video?.width;
    const height = health.video?.height;
    let aspectRatio: string | undefined;
    const warnings = [...health.warnings];
    if (width && height) {
      const g = gcd(width, height);
      aspectRatio = `${width / g}:${height / g}`;
      if (Math.abs(width / height - 9 / 16) > 0.05) {
        warnings.push(`Aspect ${aspectRatio} is not close to 9:16`);
      }
    }
    return {
      ok: health.errors.length === 0,
      errors: health.errors,
      warnings,
      durationSeconds,
      width,
      height,
      aspectRatio,
      videoCodec: health.video?.codec_name,
      audioCodec: health.audio?.codec_name,
      sizeBytes: data.format?.size ? Number(data.format.size) : undefined,
      frameRate: health.frameRate,
      rFrameRate: health.rFrameRate,
      avgFrameRate: health.avgFrameRate,
      variableFrameRate: health.variableFrameRate,
      videoToolbox: health.videoToolbox,
      pixelFormat: health.pixelFormat,
      encoder: health.encoder,
      hasAudio: Boolean(health.audio),
    };
  } catch (err) {
    return {
      ok: false,
      errors: [
        `ffprobe unavailable or failed: ${err instanceof Error ? err.message : "unknown"}`,
      ],
      warnings: [],
    };
  }
}

function gcd(a: number, b: number): number {
  return b === 0 ? a : gcd(b, a % b);
}

export function validateForPlatform(
  platform: string,
  probe: ProbeResult,
): { ok: boolean; errors: string[]; warnings: string[] } {
  const errors = [...probe.errors];
  const warnings = [...probe.warnings];
  if (!probe.ok) return { ok: false, errors, warnings };

  const duration = probe.durationSeconds || 0;
  if (platform === "youtube_longform") {
    if (duration < 3) errors.push("Video shorter than 3 seconds");
    return { ok: errors.length === 0, errors, warnings };
  }
  if (["youtube_shorts", "tiktok", "instagram_reels", "facebook_reels"].includes(platform)) {
    if (duration < 3) errors.push("Video shorter than 3 seconds");
    if (duration > 60 && platform === "youtube_shorts") {
      warnings.push("YouTube Shorts typically perform best under 60s");
    }
    if (duration > 90 && platform === "instagram_reels") {
      errors.push("Instagram API Reels commonly limited to ~90 seconds");
    }
  }
  return { ok: errors.length === 0, errors, warnings };
}
