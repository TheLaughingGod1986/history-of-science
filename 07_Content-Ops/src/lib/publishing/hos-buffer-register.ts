/**
 * J1202: register a HOS Short into Orbit's social/hos/UPLOADS.json at upload time so the daily
 * `buffer-mirror.ts check --channel hos` (orbit-with-ben) can mirror it when YouTube shows it
 * Public/scheduled. Longs are never registered. Does not post to Buffer.
 */
import crypto from "crypto";
import fs from "fs";
import path from "path";

export type HosSocialCopy = { hook?: string; question?: string; alt?: string; coverMs?: number };

export type HosBufferRegisterInput = {
  /** History of Science repo root (this checkout). */
  hosRepoRoot: string;
  videoId: string;
  mediaPath: string;
  longId?: string | null;
  standalone?: boolean;
  social?: HosSocialCopy | null;
  /** Override Orbit checkout; default: sibling `orbit-with-ben` or env OWB_ROOT. */
  owbRoot?: string;
  now?: Date;
};

export type HosUploadRecord = {
  kind: "short";
  file: string;
  sha256: string;
  long?: string;
  standalone?: boolean;
  social?: HosSocialCopy;
  registeredAt: string;
  note?: string;
};

export type HosUploadsRegistry = { version: 1; videos: Record<string, HosUploadRecord & Record<string, unknown>> };

export function resolveOwbRoot(hosRepoRoot: string, override?: string): string {
  if (override) return path.resolve(override);
  if (process.env.OWB_ROOT) return path.resolve(process.env.OWB_ROOT);
  return path.resolve(hosRepoRoot, "..", "orbit-with-ben");
}

export function hosUploadsPath(owbRoot: string): string {
  return path.join(owbRoot, "00_Brand/Channel-Setup/social/hos/UPLOADS.json");
}

function loadRegistry(file: string): HosUploadsRegistry {
  if (!fs.existsSync(file)) return { version: 1, videos: {} };
  return JSON.parse(fs.readFileSync(file, "utf8")) as HosUploadsRegistry;
}

function sha256File(filePath: string): string {
  const hash = crypto.createHash("sha256");
  hash.update(fs.readFileSync(filePath));
  return hash.digest("hex");
}

/**
 * Write (or update) one Short in Orbit social/hos/UPLOADS.json. Absolute media paths stay absolute when
 * they sit outside the Orbit repo (HOS masters, HOS UAT).
 */
export function registerHosShortForBuffer(input: HosBufferRegisterInput): {
  owbRoot: string;
  uploadsFile: string;
  entry: HosUploadRecord;
} {
  const media = path.resolve(input.mediaPath);
  if (!fs.existsSync(media) || !fs.statSync(media).isFile()) {
    throw new Error(`HOS Buffer register: media not found: ${media}`);
  }
  if (!input.longId && !input.standalone) {
    throw new Error("HOS Buffer register: a Short needs longId or standalone: true");
  }

  const owbRoot = resolveOwbRoot(input.hosRepoRoot, input.owbRoot);
  const uploadsFile = hosUploadsPath(owbRoot);
  if (!fs.existsSync(path.dirname(uploadsFile))) {
    throw new Error(`HOS Buffer register: Orbit social/hos missing at ${path.dirname(uploadsFile)} (set OWB_ROOT)`);
  }

  const relToOwb = path.relative(owbRoot, media);
  const file = relToOwb.startsWith("..") ? media : relToOwb;
  const now = (input.now ?? new Date()).toISOString();
  const sha256 = sha256File(media);

  const reg = loadRegistry(uploadsFile);
  const prev = (reg.videos[input.videoId] ?? {}) as Partial<HosUploadRecord>;
  const entry: HosUploadRecord = {
    kind: "short",
    file,
    sha256,
    registeredAt: now,
    ...(input.longId ? { long: input.longId } : {}),
    ...(input.standalone ? { standalone: true } : {}),
    ...(input.social || prev.social
      ? { social: { ...(prev.social ?? {}), ...(input.social ?? {}) } }
      : {}),
    note: "J1202: registered at HOS upload for daily check --channel hos (no Buffer post from the upload hook)",
  };
  for (const k of Object.keys(entry) as (keyof HosUploadRecord)[]) {
    if (entry[k] === undefined) delete entry[k];
  }

  reg.videos[input.videoId] = { ...prev, ...entry };
  fs.writeFileSync(uploadsFile, JSON.stringify(reg, null, 2) + "\n");
  return { owbRoot, uploadsFile, entry };
}
