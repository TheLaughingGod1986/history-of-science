import { describe, expect, it } from "vitest";
import {
  assessPlaybackHealth,
  encoderIsVideoToolbox,
  isVariableFrameRate,
  parseFrameRate,
  validateForPlatform,
  type ProbeResult,
} from "../src/lib/publishing/media/ffprobe";

describe("CFR / playback-lag probe", () => {
  it("parses rational frame rates", () => {
    expect(parseFrameRate("30/1")).toBe(30);
    expect(parseFrameRate("30000/1001")).toBeCloseTo(29.97, 2);
    expect(parseFrameRate("0/0")).toBeUndefined();
  });

  it("flags VFR when avg and r disagree", () => {
    expect(isVariableFrameRate("30/1", "24/1")).toBe(true);
    expect(isVariableFrameRate("30/1", "30/1")).toBe(false);
    expect(isVariableFrameRate("0/0", "30/1")).toBe(true);
  });

  it("detects VideoToolbox encoder tags", () => {
    expect(encoderIsVideoToolbox("h264_videotoolbox")).toBe(true);
    expect(encoderIsVideoToolbox("Lavc60.31.102 libx264")).toBe(false);
  });

  it("blocks the VideoToolbox + VFR combo that caused social stutter", () => {
    const health = assessPlaybackHealth({
      streams: [
        {
          codec_type: "video",
          codec_name: "h264",
          width: 1080,
          height: 1920,
          r_frame_rate: "30/1",
          avg_frame_rate: "24/1",
          pix_fmt: "yuv420p",
          tags: { encoder: "h264_videotoolbox" },
        },
        { codec_type: "audio", codec_name: "aac" },
      ],
    });
    expect(health.variableFrameRate).toBe(true);
    expect(health.videoToolbox).toBe(true);
    expect(health.errors.some((e) => /Variable frame rate/.test(e))).toBe(true);
    expect(health.errors.some((e) => /Hardware encoder/.test(e))).toBe(true);

    const probe: ProbeResult = {
      ok: false,
      errors: health.errors,
      warnings: health.warnings,
      durationSeconds: 40,
      variableFrameRate: true,
      videoToolbox: true,
    };
    const check = validateForPlatform("youtube_shorts", probe);
    expect(check.ok).toBe(false);
  });

  it("accepts CFR libx264 Shorts", () => {
    const health = assessPlaybackHealth({
      streams: [
        {
          codec_type: "video",
          codec_name: "h264",
          width: 1080,
          height: 1920,
          r_frame_rate: "30/1",
          avg_frame_rate: "30/1",
          pix_fmt: "yuv420p",
          tags: { encoder: "Lavc libx264" },
        },
        { codec_type: "audio", codec_name: "aac" },
      ],
    });
    expect(health.errors).toEqual([]);
    expect(health.variableFrameRate).toBe(false);

    const probe: ProbeResult = {
      ok: true,
      errors: [],
      warnings: [],
      durationSeconds: 40,
      width: 1080,
      height: 1920,
      variableFrameRate: false,
      videoToolbox: false,
      hasAudio: true,
    };
    expect(validateForPlatform("youtube_shorts", probe).ok).toBe(true);
  });
});
