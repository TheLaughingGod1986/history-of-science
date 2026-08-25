export const CHANNEL_NAME = "History of Science";
export const CHANNEL_HANDLE = "@HistoryOfScience";
export const DEFAULT_TIMEZONE = "Europe/London";

export type PlatformId =
  | "youtube_shorts"
  | "tiktok"
  | "instagram_reels"
  | "instagram_feed"
  | "facebook_reels"
  | "facebook_page"
  | "x"
  | "threads";

export type PlatformConfig = {
  id: PlatformId;
  label: string;
  shortLabel: string;
  color: string;
  supportsVideo: boolean;
  maxTitleLength?: number;
  maxCaptionLength?: number;
  recommendedHashtags: number;
  defaultMethod: "manual" | "api" | "scheduled_export" | "third_party";
  connectionStatus: "manual_only" | "available" | "unavailable" | "expired";
};

export const PLATFORMS: Record<PlatformId, PlatformConfig> = {
  youtube_shorts: {
    id: "youtube_shorts",
    label: "YouTube Shorts",
    shortLabel: "YT",
    color: "#FF0033",
    supportsVideo: true,
    maxTitleLength: 60,
    maxCaptionLength: 5000,
    recommendedHashtags: 4,
    defaultMethod: "manual",
    connectionStatus: "manual_only",
  },
  tiktok: {
    id: "tiktok",
    label: "TikTok",
    shortLabel: "TT",
    color: "#25F4EE",
    supportsVideo: true,
    maxCaptionLength: 2200,
    recommendedHashtags: 4,
    defaultMethod: "manual",
    connectionStatus: "manual_only",
  },
  instagram_reels: {
    id: "instagram_reels",
    label: "Instagram Reels",
    shortLabel: "IG",
    color: "#E1306C",
    supportsVideo: true,
    maxCaptionLength: 2200,
    recommendedHashtags: 4,
    defaultMethod: "manual",
    connectionStatus: "manual_only",
  },
  instagram_feed: {
    id: "instagram_feed",
    label: "Instagram Feed",
    shortLabel: "IG·F",
    color: "#C13584",
    supportsVideo: false,
    maxCaptionLength: 2200,
    recommendedHashtags: 4,
    defaultMethod: "manual",
    connectionStatus: "manual_only",
  },
  facebook_reels: {
    id: "facebook_reels",
    label: "Facebook Reels",
    shortLabel: "FB",
    color: "#1877F2",
    supportsVideo: true,
    maxCaptionLength: 2200,
    recommendedHashtags: 3,
    defaultMethod: "manual",
    connectionStatus: "manual_only",
  },
  facebook_page: {
    id: "facebook_page",
    label: "Facebook Page",
    shortLabel: "FB·P",
    color: "#0866FF",
    supportsVideo: false,
    maxCaptionLength: 5000,
    recommendedHashtags: 2,
    defaultMethod: "manual",
    connectionStatus: "manual_only",
  },
  x: {
    id: "x",
    label: "X",
    shortLabel: "X",
    color: "#8B98A5",
    supportsVideo: true,
    maxCaptionLength: 280,
    recommendedHashtags: 2,
    defaultMethod: "manual",
    connectionStatus: "manual_only",
  },
  threads: {
    id: "threads",
    label: "Threads",
    shortLabel: "Th",
    color: "#A8B4C0",
    supportsVideo: false,
    maxCaptionLength: 500,
    recommendedHashtags: 2,
    defaultMethod: "manual",
    connectionStatus: "manual_only",
  },
};

export const VIDEO_PLATFORMS: PlatformId[] = [
  "youtube_shorts",
  "tiktok",
  "instagram_reels",
  "facebook_reels",
];

/** Text / feed posts (not Reels). */
export const TEXT_PLATFORMS: PlatformId[] = ["x", "threads", "instagram_feed", "facebook_page"];

export const ALL_PLATFORM_IDS = Object.keys(PLATFORMS) as PlatformId[];
