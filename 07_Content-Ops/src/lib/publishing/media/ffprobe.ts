import { execFile } from "child_process";
import { promisify } from "util";
import fs from "fs/promises";

const execFileAsync = promisify(execFile);

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
  hasAudio?: boolean;
};

export async function probeVideo(filePath: string): Promise<ProbeResult> {
  const errors: string[] = [];
  const warnings: string[] = [];
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
        "format=duration,size:stream=codec_type,codec_name,width,height,avg_frame_rate",
        "-of",
        "json",
        filePath,
      ],
      { timeout: 30_000 },
    );
    const data = JSON.parse(stdout) as {
      format?: { duration?: string; size?: string };
      streams?: Array<{
        codec_type?: string;
        codec_name?: string;
        width?: number;
        height?: number;
        avg_frame_rate?: string;
      }>;
    };
    const video = data.streams?.find((s) => s.codec_type === "video");
    const audio = data.streams?.find((s) => s.codec_type === "audio");
    const durationSeconds = data.format?.duration ? Number(data.format.duration) : undefined;
    const width = video?.width;
    const height = video?.height;
    let aspectRatio: string | undefined;
    if (width && height) {
      const g = gcd(width, height);
      aspectRatio = `${width / g}:${height / g}`;
      if (Math.abs(width / height - 9 / 16) > 0.05) {
        warnings.push(`Aspect ${aspectRatio} is not close to 9:16`);
      }
    }
    let frameRate: number | undefined;
    if (video?.avg_frame_rate && video.avg_frame_rate.includes("/")) {
      const [a, b] = video.avg_frame_rate.split("/").map(Number);
      if (b) frameRate = a / b;
    }
    if (!audio) warnings.push("No audio track detected");
    return {
      ok: errors.length === 0,
      errors,
      warnings,
      durationSeconds,
      width,
      height,
      aspectRatio,
      videoCodec: video?.codec_name,
      audioCodec: audio?.codec_name,
      sizeBytes: data.format?.size ? Number(data.format.size) : undefined,
      frameRate,
      hasAudio: Boolean(audio),
    };
  } catch (err) {
    return {
      ok: false,
      errors: [
        `ffprobe unavailable or failed: ${err instanceof Error ? err.message : "unknown"}`,
      ],
      warnings,
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
