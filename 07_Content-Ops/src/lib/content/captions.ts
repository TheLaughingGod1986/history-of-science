export type CaptionCue = {
  index: number;
  startSeconds: number;
  endSeconds: number;
  text: string;
};

export type CaptionExport = {
  srt: string;
  vtt: string;
  plain: string;
  burnedInScript: string;
  wordTimings: { word: string; start: number; end: number }[];
  positioningNotes: string;
};

function pad(n: number, width = 2): string {
  return String(n).padStart(width, "0");
}

export function formatSrtTime(seconds: number): string {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = Math.floor(seconds % 60);
  const ms = Math.round((seconds % 1) * 1000);
  return `${pad(h)}:${pad(m)}:${pad(s)},${pad(ms, 3)}`;
}

export function formatVttTime(seconds: number): string {
  return formatSrtTime(seconds).replace(",", ".");
}

export function splitTranscriptIntoCues(
  transcript: string,
  startSeconds = 0,
  endSeconds?: number,
): CaptionCue[] {
  const words = transcript.trim().split(/\s+/).filter(Boolean);
  if (!words.length) return [];
  const total = endSeconds && endSeconds > startSeconds ? endSeconds - startSeconds : Math.max(20, words.length * 0.35);
  const chunkSize = 6;
  const cues: CaptionCue[] = [];
  let idx = 0;
  for (let i = 0; i < words.length; i += chunkSize) {
    const chunk = words.slice(i, i + chunkSize);
    const localStart = startSeconds + (i / words.length) * total;
    const localEnd = startSeconds + (Math.min(i + chunkSize, words.length) / words.length) * total;
    cues.push({
      index: ++idx,
      startSeconds: Number(localStart.toFixed(3)),
      endSeconds: Number(localEnd.toFixed(3)),
      text: chunk.join(" "),
    });
  }
  return cues;
}

export function exportCaptions(input: {
  transcript: string;
  startSeconds?: number;
  endSeconds?: number;
}): CaptionExport {
  const cues = splitTranscriptIntoCues(
    input.transcript,
    input.startSeconds ?? 0,
    input.endSeconds,
  );

  const srt = cues
    .map(
      (c) =>
        `${c.index}\n${formatSrtTime(c.startSeconds)} --> ${formatSrtTime(c.endSeconds)}\n${c.text}\n`,
    )
    .join("\n");

  const vtt =
    "WEBVTT\n\n" +
    cues
      .map(
        (c) =>
          `${formatVttTime(c.startSeconds)} --> ${formatVttTime(c.endSeconds)}\n${c.text}\n`,
      )
      .join("\n");

  const plain = input.transcript.trim();
  const burnedInScript = cues
    .map((c) => `[${formatVttTime(c.startSeconds)}] ${c.text}`)
    .join("\n");

  const words = input.transcript.trim().split(/\s+/).filter(Boolean);
  const span =
    (input.endSeconds ?? (input.startSeconds ?? 0) + words.length * 0.35) -
    (input.startSeconds ?? 0);
  const wordTimings = words.map((word, i) => {
    const start = (input.startSeconds ?? 0) + (i / Math.max(words.length, 1)) * span;
    const end = (input.startSeconds ?? 0) + ((i + 1) / Math.max(words.length, 1)) * span;
    return { word, start: Number(start.toFixed(3)), end: Number(end.toFixed(3)) };
  });

  return {
    srt,
    vtt,
    plain,
    burnedInScript,
    wordTimings,
    positioningNotes: [
      "Max two lines on screen.",
      "Keep captions in the middle-safe zone — avoid bottom 12% (platform controls) and top 10% (UI).",
      "Highlight scientific terms with weight, not excessive animation.",
      "Prefer correct punctuation; do not flood the frame with words.",
    ].join(" "),
  };
}
